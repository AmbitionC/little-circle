#!/usr/bin/env python3
"""动态绘本视频生成器（storybook video）。

结构：[可选 0.4 秒封面帧] → 开头可灵钩子镜头 → 绘本页（静态图运镜 + 角色配音 + 逐词高亮中英字幕）
      → 片尾卡。同时导出 SRT 字幕和可打印 PDF。

用法：
    python sbv.py story.json --out out/
    python sbv.py story.json --out out/ --max-pages 3     # 推荐流精华版
依赖：Python 3.9+、Pillow、numpy、ffmpeg/ffprobe（需带 rubberband、loudnorm 滤镜）。
配音：kokoro（kokoro-onnx，离线，Apache-2.0）/ elevenlabs / edge（仅样片）/ 每句自带音频文件。
"""
import argparse
import asyncio
import base64
import hashlib
import json
import math
import os
import random
import re
import shutil
import ssl
import subprocess
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
SR = 48000

# 默认风格 = Forest Friends English 系列规范；story.json 的 style 字段可逐项覆盖
DEFAULT_STYLE = {
    "fonts": {
        "en": {"path": "fonts/Fredoka.ttf", "variation": "SemiBold"},
        "zh": {"path": "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", "index": 2},
    },
    "en_size": 70,
    "zh_size": 46,
    # 字幕默认无底板、描边字，放在画面 2/3 高度：避开抖音底部的标题、简介和右侧按钮（2026-10-28 用户要求）
    "subtitle_mode": "outline",
    "subtitle_center": 1320,
    "subtitle_x": 510,
    "subtitle_max_w": 820,
    "sub_fill": [255, 255, 255],
    "sub_highlight": [255, 214, 64],
    "sub_stroke_w": 9,
    "card_fill": [255, 249, 236, 238],
    "card_outline": [232, 214, 186],
    "zh_color": [110, 84, 62],
    "highlight": [255, 221, 158],
    "speaker_colors": {"narrator": [74, 52, 38]},
    "headline_color": [255, 246, 222],
    "accent": [232, 137, 43],
    "stroke": [92, 52, 24],
    "transition": "fade",
    "transition_seconds": 0.35,
    "lead": 0.5,
    "gap": 0.4,
    "tail": 1.0,
    "sparkles": True,
    "badge_pos": [24, 40],
}
FONT_FALLBACKS = {
    "en": ["/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    # (路径, ttc 索引)：冬青黑体 index 0 是最细的 W3，大字标题要用 index 2 的 W6
    "zh": [("/System/Library/Fonts/PingFang.ttc", 0),
           ("/System/Library/Fonts/Hiragino Sans GB.ttc", 2),
           "/System/Library/Fonts/STHeiti Medium.ttc",
           "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"],
}


# ---------- 通用工具 ----------

def run(cmd):
    subprocess.run(cmd, check=True)


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], check=True, capture_output=True, text=True)
    return float(out.stdout.strip())


def decode_audio(path):
    """解码成 48k 单声道 float32。"""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                          "-ar", str(SR), "-"], check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def rgb(c, a=None):
    return tuple(c[:3]) + ((a,) if a is not None else tuple(c[3:4]))


class Fonts:
    """按配置加载字体；支持 ttc 索引和可变字体字重（如 Fredoka SemiBold）。"""

    def __init__(self, spec, base):
        self.spec, self.base, self.cache = spec, base, {}

    def get(self, kind, size, variation=None):
        key = (kind, size, variation)
        if key in self.cache:
            return self.cache[key]
        s = self.spec.get(kind) or {}
        if isinstance(s, str):
            s = {"path": s}
        cands = []
        if s.get("path"):
            p = s["path"]
            cands.append(p if os.path.isabs(p) else os.path.join(self.base, p))
            cands.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), p))
        for path in cands + FONT_FALLBACKS[kind]:
            path, fb_index = path if isinstance(path, tuple) else (path, 0)
            if os.path.exists(path):
                f = ImageFont.truetype(path, size, index=s.get("index", 0) if path in cands else fb_index)
                v = variation or s.get("variation")
                if v and path in cands:
                    try:
                        f.set_variation_by_name(v)
                    except (OSError, ValueError):
                        pass
                self.cache[key] = f
                return f
        raise SystemExit(f"找不到{kind}字体，请在 style.fonts.{kind}.path 指定字体文件")


def cover_crop(img, w=W, h=H):
    iw, ih = img.size
    s = max(w / iw, h / ih)
    img = img.resize((math.ceil(iw * s), math.ceil(ih * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


# ---------- 配音 ----------

_KOKORO = None


def tts_kokoro(text, v, out_wav):
    """Kokoro 离线合成，可选 rubberband 变调（共振峰一起变，更像小孩）。"""
    global _KOKORO
    import soundfile as sf
    from kokoro_onnx import Kokoro
    if _KOKORO is None:
        mdir = os.environ.get("KOKORO_MODELS", "models")
        _KOKORO = Kokoro(os.path.join(mdir, "kokoro-v1.0.onnx"), os.path.join(mdir, "voices-v1.0.bin"))
    samples, sr = _KOKORO.create(text, voice=v.get("voice", "af_heart"),
                                 speed=v.get("speed", 0.9), lang=v.get("lang", "en-us"))
    raw = out_wav + ".raw.wav"
    sf.write(raw, samples, sr)
    af = ["highpass=f=70", f"aresample={SR}"]
    if abs(v.get("pitch", 1.0) - 1.0) > 1e-3:
        af.insert(0, f"rubberband=pitch={v['pitch']}:pitchq=quality:formant=shifted")
    run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", ",".join(af), out_wav])
    os.remove(raw)
    return []          # Kokoro 不给词级时间戳，交给 estimate_spans 按语音能量估算


def tts_edge(text, v, out_wav):
    """Edge 在线朗读：免费、带逐词时间戳。非官方接口，只建议做样片，不要用于发布。"""
    import edge_tts
    import edge_tts.communicate as ec
    if os.environ.get("SBV_CAFILE"):
        ec._SSL_CTX = ssl.create_default_context(cafile=os.environ["SBV_CAFILE"])

    async def go():
        c = edge_tts.Communicate(text, v.get("voice", "en-US-AnaNeural"), rate=v.get("rate", "-10%"),
                                 boundary="WordBoundary", proxy=os.environ.get("HTTPS_PROXY") or None)
        words, buf = [], bytearray()
        async for ch in c.stream():
            if ch["type"] == "audio":
                buf.extend(ch["data"])
            elif ch["type"] == "WordBoundary":
                s = ch["offset"] / 1e7
                words.append({"w": ch["text"], "s": s, "e": s + ch["duration"] / 1e7})
        return words, bytes(buf)

    words, data = asyncio.run(go())
    with open(out_wav + ".mp3", "wb") as f:
        f.write(data)
    run(["ffmpeg", "-v", "error", "-y", "-i", out_wav + ".mp3", "-ar", str(SR), out_wav])
    os.remove(out_wav + ".mp3")
    return words


def tts_elevenlabs(text, v, out_wav):
    """ElevenLabs 配音。优先走带时间戳的接口（字符级对齐 → 词级）；
    某个模型不支持时间戳时，退回普通接口，高亮改用能量估算。需环境变量 ELEVENLABS_API_KEY。"""
    import urllib.error
    if not os.environ.get("ELEVENLABS_API_KEY"):
        raise SystemExit("没读到 ELEVENLABS_API_KEY。先执行 source ~/.zshrc，或新开一个终端窗口。")
    api = os.environ.get("ELEVENLABS_API_BASE", "https://api.elevenlabs.io").rstrip("/")
    base = f"{api}/v1/text-to-speech/{v['voice']}"
    body = {"text": text, "model_id": v.get("model", "eleven_multilingual_v2")}
    if "settings" in v:
        body["voice_settings"] = v["settings"]
    if "seed" in v:
        body["seed"] = v["seed"]
    headers = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"}
    data = None
    try:
        req = urllib.request.Request(base + "/with-timestamps?output_format=mp3_44100_128",
                                     data=json.dumps(body).encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.load(r)
        audio = base64.b64decode(data["audio_base64"])
    except urllib.error.HTTPError as err:
        raw = err.read()[:300]
        # 401 key 无效、402 额度、403 权限或档位、404 Voice ID 不对、429 频率：换接口也没用，直接说清楚
        if err.code in (401, 402, 403, 404, 429):
            raise SystemExit(f"ElevenLabs 返回 {err.code}：{raw!r}（检查 key 权限、档位、额度、Voice ID 或频率）")
        print(f"  时间戳接口不可用（{err.code}），改用普通接口：{text[:30]}", flush=True)
        req = urllib.request.Request(base + "?output_format=mp3_44100_128",
                                     data=json.dumps(body).encode(), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                audio = r.read()
        except urllib.error.HTTPError as err2:
            raise SystemExit(f"ElevenLabs 返回 {err2.code}：{err2.read()[:300]!r}")
    with open(out_wav + ".mp3", "wb") as f:
        f.write(audio)
    run(["ffmpeg", "-v", "error", "-y", "-i", out_wav + ".mp3", "-ar", str(SR), out_wav])
    os.remove(out_wav + ".mp3")
    al = (data or {}).get("alignment") or (data or {}).get("normalized_alignment")
    if not al:
        return []
    words, cur, s, e = [], "", None, None
    for ch, cs, ce in zip(al["characters"], al["character_start_times_seconds"],
                          al["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append({"w": cur, "s": s, "e": e})
            cur, s = "", None
        else:
            s = cs if s is None else s
            cur, e = cur + ch, ce
    if cur:
        words.append({"w": cur, "s": s, "e": e})
    return words


PROVIDERS = {"kokoro": tts_kokoro, "edge": tts_edge, "elevenlabs": tts_elevenlabs}


def synthesize(text, voice, cache_dir):
    """返回 (wav 路径, 词时间戳)。按文本和音色缓存，改剧本只重配改过的句子。"""
    key = hashlib.sha1(json.dumps([text, voice, "trim1"], sort_keys=True).encode()).hexdigest()[:16]
    wav, meta = os.path.join(cache_dir, f"{key}.wav"), os.path.join(cache_dir, f"{key}.json")
    if os.path.exists(wav) and os.path.exists(meta):
        with open(meta) as f:
            return wav, json.load(f)
    raw = wav + ".untrimmed.wav"
    words = PROVIDERS[voice.get("provider", "kokoro")](text, voice, raw)
    # 切掉合成音频首尾多余的静音，时间戳同步平移，句子之间的停顿才由 gap 控制
    s0, s1 = speech_bounds(raw)
    a, b = max(0.0, s0 - 0.05), s1 + 0.12
    run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-ss", f"{a:.3f}", "-to", f"{b:.3f}", wav])
    os.remove(raw)
    words = [{"w": x["w"], "s": max(0.0, x["s"] - a), "e": max(0.0, x["e"] - a)} for x in words]
    with open(meta, "w") as f:
        json.dump(words, f)
    return wav, words


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def speech_bounds(path):
    """按能量找出真正开口和收声的时间，去掉合成音频首尾的静音。"""
    a = decode_audio(path)
    hop = SR // 100
    env = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, mode="same"))[::hop]
    on = np.where(env > env.max() * 0.08)[0]
    if len(on) == 0:
        return 0.0, len(a) / SR
    return on[0] / 100, (on[-1] + 1) / 100


def estimate_spans(tokens, s0, s1):
    """没有时间戳时，按字长分配；句末标点后多留一点停顿。"""
    wts = [len(norm(t)) + 1.5 + (2.5 if t[-1:] in ".!?" else 1.2 if t[-1:] in ",;:" else 0)
           for t in tokens]
    spans, acc, tot = [], s0, sum(wts)
    for t, wt in zip(tokens, wts):
        step = (s1 - s0) * wt / tot
        spans.append((acc, acc + step * 0.85))
        acc += step
    return spans


def drop_tags(words):
    """去掉 v3 语气标签（[excited]、[happy gasp] 这类）对应的"词"，它们不出声、也不在字幕里。"""
    out, inside = [], False
    for w in words:
        t = w["w"]
        if t.startswith("["):
            inside = True
        if not inside:
            out.append(w)
        if t.endswith("]"):
            inside = False
    return out


def align_tokens(tokens, words, path):
    """把配音的词时间戳对到字幕词（字幕词带标点）；对不上或没有时间戳的按能量 + 字长估算。"""
    s0, s1 = speech_bounds(path)
    words = drop_tags(words or [])
    if not words:
        return estimate_spans(tokens, s0, s1)
    spans, j = [None] * len(tokens), 0
    for i, t in enumerate(tokens):
        nt = norm(t)
        for k in range(j, min(j + 3, len(words))):
            nw = norm(words[k]["w"])
            if nt and nw and (nw == nt or nt.startswith(nw) or nw.startswith(nt)):
                spans[i], j = (words[k]["s"], words[k]["e"]), k + 1
                break
    i = 0
    while i < len(tokens):
        if spans[i] is not None:
            i += 1
            continue
        k = i
        while k < len(tokens) and spans[k] is None:
            k += 1
        a = spans[i - 1][1] if i > 0 else s0
        b = spans[k][0] if k < len(tokens) else max(a + 0.3, s1)
        spans[i:k] = estimate_spans(tokens[i:k], a, b)
        i = k
    return spans


# ---------- 文字 ----------

def wrap_tokens(tokens, font, max_w):
    """按宽度折行，尽量让两行等长（同系列 wrap_title 的做法）。"""
    if font.getlength(" ".join(tokens)) <= max_w:
        return [list(range(len(tokens)))]
    best = None
    for k in range(1, len(tokens)):
        a, b = " ".join(tokens[:k]), " ".join(tokens[k:])
        m = max(font.getlength(a), font.getlength(b))
        if best is None or m < best[0]:
            best = (m, [list(range(k)), list(range(k, len(tokens)))])
    if best[0] <= max_w:
        return best[1]
    lines, cur = [], []
    for i, t in enumerate(tokens):
        if cur and font.getlength(" ".join(tokens[c] for c in cur + [i])) > max_w:
            lines.append(cur)
            cur = []
        cur.append(i)
    return lines + [cur]


def wrap_zh(text, font, max_w):
    if font.getlength(text) <= max_w:
        return [text]
    lines, cur = [], ""
    for ch in text:
        if cur and font.getlength(cur + ch) > max_w:
            lines.append(cur)
            cur = ""
        cur += ch
    return lines + [cur]


def stroke_text(draw, xy, text, font, fill, stroke, width=8, max_w=980):
    while font.getlength(text) > max_w and font.size > 30:
        font = font.font_variant(size=font.size - 4)
    draw.text(xy, text, font=font, fill=fill, stroke_width=width, stroke_fill=stroke, anchor="mm")


# ---------- 画面元素 ----------

class Sparkles:
    """漂浮的光点，让静态页“活”一点。"""

    def __init__(self, n=14, seed=7):
        rnd = random.Random(seed)
        self.ps = [(rnd.uniform(0, W), rnd.uniform(0, H * 0.75), rnd.uniform(15, 40),
                    rnd.uniform(0.25, 0.6), rnd.uniform(0, 6.28), rnd.uniform(0.6, 1.4)) for _ in range(n)]
        size = 64
        yy, xx = np.mgrid[0:size, 0:size]
        a = np.clip(1 - np.sqrt((xx - 32) ** 2 + (yy - 32) ** 2) / 32, 0, 1) ** 2.2
        self.base = np.dstack([np.full_like(a, 255), np.full_like(a, 246), np.full_like(a, 214), a * 255])

    def draw(self, img, t):
        for x0, y0, speed, amp, ph, sc in self.ps:
            y = (y0 - speed * t) % (H * 0.8)
            x = x0 + 20 * math.sin(t * 0.6 + ph)
            alpha = amp * (0.5 + 0.5 * math.sin(t * 2.2 * sc + ph))
            s = int(28 * sc)
            dx, dy = int(x - s / 2), int(y - s / 2)
            if alpha < 0.05 or dx < 0 or dy < 0 or dx + s > W or dy + s > H:
                continue
            spr = self.base.copy()
            spr[..., 3] *= alpha
            img.alpha_composite(Image.fromarray(spr.astype(np.uint8), "RGBA").resize((s, s)), (dx, dy))


def kb_box(motion, u, iw, ih, rw, rh, focus, zoom=1.12, z0=1.0):
    """Ken Burns 运镜：返回原图坐标下的取景框（亚像素，画面不抖）。"""
    s0 = max(rw / iw, rh / ih)
    vw0, vh0 = rw / s0, rh / s0
    e = ease(u)
    if motion in ("in", "out"):
        k = e if motion == "in" else 1 - e
        z = z0 + (zoom - z0) * k
        cx = iw / 2 + (focus[0] * iw - iw / 2) * k * 0.6
        cy = ih / 2 + (focus[1] * ih - ih / 2) * k * 0.6
    else:
        z = z0 + (zoom - z0) * 0.8
        vw, vh = vw0 / z, vh0 / z
        cx, cy = iw / 2, ih / 2
        if motion == "left":
            cx = (iw - vw / 2) + (vw - iw) * e
        elif motion == "right":
            cx = vw / 2 + (iw - vw) * e
        elif motion == "up":
            cy = (ih - vh / 2) + (vh - ih) * e
        elif motion == "down":
            cy = vh / 2 + (ih - vh) * e
    vw, vh = vw0 / z, vh0 / z
    cx = min(max(cx, vw / 2), iw - vw / 2)
    cy = min(max(cy, vh / 2), ih - vh / 2)
    return (cx - vw / 2, cy - vh / 2, cx + vw / 2, cy + vh / 2)


class Ctx:
    def __init__(self, style, fonts, sparkles, badge, cache_dir):
        self.st, self.fonts, self.sparkles, self.badge = style, fonts, sparkles, badge
        self.cache_dir = cache_dir


# ---------- 片段 ----------

class StillSeg:
    """静止画面（封面帧）。"""

    def __init__(self, img_path, dur):
        self.img, self.dur, self.cut = cover_crop(Image.open(img_path).convert("RGB")), dur, True

    def render(self, t, gt):
        return self.img


class HookSeg:
    """可灵钩子镜头 + 给家长看的大字标题。"""

    def __init__(self, hook, frames_dir, n, ctx):
        self.dir, self.n, self.dur, self.cut = frames_dir, n, n / FPS, hook.get("cut", True)
        st, f = ctx.st, ctx.fonts
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        y = hook.get("headline_y", 330)
        if hook.get("headline"):
            stroke_text(d, (W // 2, y), hook["headline"], f.get("zh", 84), rgb(st["headline_color"]), rgb(st["stroke"]))
        if hook.get("subline"):
            stroke_text(d, (W // 2, y + 115), hook["subline"], f.get("zh", 52), rgb(st["accent"]), (255, 255, 255), 6)
        self.overlay, self.y = ov, y

    def render(self, t, gt):
        i = min(int(t * FPS), self.n - 1)
        frame = Image.open(os.path.join(self.dir, f"h_{i + 1:04d}.jpg")).convert("RGBA")
        # 第 1 帧就要有完整标题（平台默认截第一帧当封面）；结尾 0.3 秒淡出
        a = 1 - ease((t - (self.dur - 0.3)) / 0.3)
        if a > 0:
            ov = self.overlay
            if a < 1:
                arr = np.array(ov)
                arr[..., 3] = (arr[..., 3] * a).astype(np.uint8)
                ov = Image.fromarray(arr)
            frame.alpha_composite(ov)
        return frame.convert("RGB")


_DEPTH = None


def estimate_depth(img, cache_path):
    """Depth Anything V2（ONNX）估单图深度，归一化到 0..1（1 = 最近）。结果缓存成 .npy。"""
    global _DEPTH
    if os.path.exists(cache_path):
        return np.load(cache_path)
    import onnxruntime as ort
    if _DEPTH is None:
        _DEPTH = ort.InferenceSession(os.environ.get("DEPTH_MODEL", "models/depth/model.onnx"),
                                      providers=["CPUExecutionProvider"])
    iw, ih = img.size
    w = 518
    h = max(14, round(w * ih / iw / 14) * 14)
    x = np.asarray(img.resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).transpose(2, 0, 1)[None].astype(np.float32)
    d = _DEPTH.run(None, {_DEPTH.get_inputs()[0].name: x})[0][0]
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)
    np.save(cache_path, d.astype(np.float32))
    return d


def flicker(t, seed=0.0):
    return (0.85 + 0.08 * math.sin(2 * math.pi * 1.7 * t + seed) + 0.05 * math.sin(2 * math.pi * 4.3 * t + 1.3 + seed)
            + 0.03 * math.sin(2 * math.pi * 9.1 * t + 0.4 + seed))


class GlowFX:
    """烛光 / 灯光：火苗一圈暖光随时间跳动，整间屋子跟着轻微明暗。坐标按原图比例给。"""

    def __init__(self, c, iw, ih):
        self.cx, self.cy, self.r = c["x"] * iw, c["y"] * ih, c.get("r", 0.12) * iw
        self.color = np.array(c.get("color", [255, 180, 90]), np.float32) / 255
        self.strength, self.room = c.get("strength", 0.55), c.get("room", 0.05)
        yy, xx = np.mgrid[0:ih, 0:iw].astype(np.float32)
        dist2 = (xx - self.cx) ** 2 + (yy - self.cy) ** 2
        self.core = np.exp(-dist2 / (2 * (self.r * 0.35) ** 2))[..., None] * self.color
        self.halo = np.exp(-dist2 / (2 * self.r ** 2))[..., None] * self.color
        self.roomw = np.exp(-dist2 / (2 * (iw * 0.55) ** 2))[..., None]

    def apply(self, src, t):
        f = flicker(t)
        src *= 1 + self.room * (f - 0.85) / 0.16 * self.roomw
        src += 255 * self.strength * (0.55 * f * self.halo + 0.6 * (f ** 3) * self.core)


class SnowFX:
    """窗外飘雪：只在给定椭圆里、且是玻璃（偏蓝或偏白）的像素上下雪，窗框挡住的地方不画。"""

    def __init__(self, c, iw, ih, src):
        import cv2
        self.cv2 = cv2
        cx, cy, rx, ry = c["ellipse"][0] * iw, c["ellipse"][1] * ih, c["ellipse"][2] * iw, c["ellipse"][3] * ih
        self.x0, self.y0 = int(max(cx - rx, 0)), int(max(cy - ry, 0))
        self.x1, self.y1 = int(min(cx + rx, iw)), int(min(cy + ry, ih))
        h, w = self.y1 - self.y0, self.x1 - self.x0
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        inside = ((xx + self.x0 - cx) / rx) ** 2 + ((yy + self.y0 - cy) / ry) ** 2 <= 1
        patch = src[self.y0:self.y1, self.x0:self.x1]
        glass = patch[..., 2] >= patch[..., 0] - 5
        m = (inside & glass).astype(np.float32)
        self.mask = cv2.GaussianBlur(cv2.erode(m, np.ones((3, 3), np.uint8)), (3, 3), 0.8)
        rnd = random.Random(c.get("seed", 3))
        sc = iw / 941
        self.flakes = [(rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(18, 50) * sc,
                        rnd.uniform(1.0, 2.8) * sc, rnd.uniform(0, 6.28), rnd.uniform(3, 9) * sc)
                       for _ in range(c.get("n", 110))]
        self.h, self.w = h, w

    def apply(self, src, t):
        cv2 = self.cv2
        layer = np.zeros((self.h, self.w), np.uint8)
        for x, y, v, r, ph, sway in self.flakes:
            yy = (y + v * t) % self.h
            xx = x + sway * math.sin(t * 0.9 + ph)
            cv2.circle(layer, (int(xx * 4), int(yy * 4)), max(1, int(r * 4)), 255, -1, cv2.LINE_AA, 2)
        a = cv2.GaussianBlur(layer.astype(np.float32) / 255, (0, 0), 0.7) * self.mask * 0.9
        reg = src[self.y0:self.y1, self.x0:self.x1]
        reg *= 1 - a[..., None]
        reg += a[..., None] * np.array([250, 252, 255], np.float32)


class MotesFX:
    """暖光里漂浮的小光尘。"""

    def __init__(self, c, iw, ih):
        import cv2
        self.cv2 = cv2
        rnd = random.Random(c.get("seed", 5))
        self.cx, self.cy, self.r = c["x"] * iw, c["y"] * ih, c.get("r", 0.25) * iw
        self.ps = [(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(6, 16), rnd.uniform(1.5, 3.5) * iw / 941,
                    rnd.uniform(0, 6.28)) for _ in range(c.get("n", 22))]
        self.iw, self.ih = iw, ih

    def apply(self, src, t):
        cv2 = self.cv2
        layer = np.zeros((self.ih, self.iw), np.uint8)
        for u, v, speed, r, ph in self.ps:
            x = self.cx + u * self.r + 10 * math.sin(t * 0.5 + ph)
            y = self.cy + v * self.r - speed * t
            a = 0.5 + 0.5 * math.sin(t * 2.0 + ph)
            if 0 <= x < self.iw and 0 <= y < self.ih:
                cv2.circle(layer, (int(x * 4), int(y * 4)), max(1, int(r * 4)), int(255 * a), -1, cv2.LINE_AA, 2)
        a = cv2.GaussianBlur(layer.astype(np.float32) / 255, (0, 0), 1.6)[..., None] * 0.7
        src += a * (np.array([255, 226, 160], np.float32) - src)


FX = {"glow": GlowFX, "motes": MotesFX}


class PageSeg:
    """一页绘本：静态图运镜 + 多句配音 + 逐词高亮的中英字幕卡。"""

    def __init__(self, page, idx, lines, ctx, base):
        st = ctx.st
        self.ctx, self.page, self.lines = ctx, page, lines   # lines: [{speaker,en,zh,start,end,tokens,spans}]
        self.cut = page.get("cut", False)
        self.dur = lines[-1]["end"] + st["tail"] + page.get("hold", 0) if lines else page.get("seconds", 3)
        self.img = Image.open(os.path.join(base, page["image"])).convert("RGB")
        self.motion = page.get("motion", ["in", "left", "out", "right"][idx % 4])
        self.focus = page.get("focus", [0.5, 0.42])
        self.zoom = page.get("zoom", 1.12)
        self.zoom_from = page.get("zoom_from", 1.05 if page.get("parallax") else 1.0)
        iw, ih = self.img.size
        if iw / ih <= 0.75:
            self.region, self.bg = (0, 0, W, H), None
        else:   # 横图/方图：放上半部，背景用同图模糊铺满（先按 9:16 裁好再模糊，避免黑带）
            rh = int(W * ih / iw)
            self.region = (0, max(200, 760 - rh // 2), W, rh)
            self.bg = ImageEnhance.Brightness(cover_crop(self.img).filter(ImageFilter.GaussianBlur(40))).enhance(0.6)
        self.cache = {}
        # 可选：画面特效（烛光 / 飘雪 / 光尘）和按深度的 2.5D 视差运镜
        src = np.asarray(self.img).astype(np.float32)
        self.fx = []
        for c in page.get("fx", []):
            self.fx.append(SnowFX(c, iw, ih, src) if c["type"] == "snow" else FX[c["type"]](c, iw, ih))
        self.src = src
        self.par = page.get("parallax")
        if self.par:
            import cv2
            self.cv2 = cv2
            cache = os.path.join(ctx.cache_dir, hashlib.sha1(
                (os.path.abspath(os.path.join(base, page["image"])) + str(os.path.getmtime(os.path.join(base, page["image"])))).encode()).hexdigest()[:16] + ".depth.npy")
            d = estimate_depth(self.img, cache)
            d = cv2.resize(d, (iw, ih), interpolation=cv2.INTER_CUBIC)
            self.depth = cv2.GaussianBlur(d, (0, 0), iw / 300).astype(np.float32)
            fx_, fy_ = self.focus
            self.d_ref = float(self.depth[int(fy_ * (ih - 1)), int(fx_ * (iw - 1))])
            rw, rh = self.region[2], self.region[3]
            self.gv, self.gu = np.mgrid[0:rh, 0:rw].astype(np.float32)

    def warp(self, src_u8, box, t):
        """2.5D 视差：近处的东西位移和放大得多，远处少；以对焦点为基准，主体基本不动。"""
        cv2 = self.cv2
        x0, y0, x1, y1 = box
        rw, rh = self.region[2], self.region[3]
        sx = x0 + self.gu * ((x1 - x0) / rw)
        sy = y0 + self.gv * ((y1 - y0) / rh)
        rel = cv2.remap(self.depth, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE) - self.d_ref
        e = 2 * ease(t / self.dur) - 1
        iw = self.img.size[0]
        amp = self.par.get("amount", 0.03) * iw
        dx, dy = amp * e * self.par.get("dir", [1, 0.25])[0], amp * e * self.par.get("dir", [1, 0.25])[1]
        k = self.par.get("dolly", 0.08) * (e + 1) / 2
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        mx = sx + rel * dx - (sx - cx) * rel * k
        my = sy + rel * dy - (sy - cy) * rel * k
        return Image.fromarray(cv2.remap(src_u8, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT))

    def state(self, t):
        """当前显示哪句字幕、高亮第几个词。字幕早 0.1 秒出现、晚 0.4 秒消失。"""
        for li, ln in enumerate(self.lines):
            nxt = self.lines[li + 1]["start"] - 0.1 if li + 1 < len(self.lines) else ln["end"] + 0.4
            if ln["start"] - 0.1 <= t < max(nxt, ln["start"]):
                a = t - ln["start"]
                for wi, (s, e) in enumerate(ln["spans"]):
                    nxt_w = ln["spans"][wi + 1][0] if wi + 1 < len(ln["spans"]) else e + 0.2
                    if s <= a < max(e, nxt_w):
                        return li, wi
                return li, -1
        return None, None

    def outline_card(self, ln, wi, color, fe, fz):
        """无底板字幕：英文白字、角色色粗描边，当前词黄字；中文白字深描边；整体带柔和投影，亮背景上也看得清。"""
        st = self.ctx.st
        maxw = st.get("subtitle_max_w", 820)
        sw = st.get("sub_stroke_w", 9)
        tokens = ln["tokens"]
        lines = wrap_tokens(tokens, fe, maxw)
        zh_lines = wrap_zh(ln.get("zh", ""), fz, maxw) if ln.get("zh") else []
        le, lz = int(fe.size * 1.2), int(fz.size * 1.45)
        space = fe.getlength(" ")
        widths = [sum(fe.getlength(tokens[i]) for i in l) + space * (len(l) - 1) for l in lines]
        pad = sw * 2 + 16
        pw = int(max(widths + [fz.getlength(z) for z in zh_lines])) + pad * 2
        ph = le * len(lines) + lz * len(zh_lines) + pad * 2
        im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        dark = tuple(int(c * 0.55) for c in color)
        y = pad
        for l, lw in zip(lines, widths):
            x = (pw - lw) / 2
            for i in l:
                fill = rgb(st["sub_highlight"]) if i == wi else rgb(st["sub_fill"])
                d.text((x, y + le / 2), tokens[i], font=fe, fill=fill, anchor="lm",
                       stroke_width=sw, stroke_fill=dark)
                x += fe.getlength(tokens[i]) + space
            y += le
        for z in zh_lines:
            d.text((pw / 2, y + lz / 2), z, font=fz, fill=rgb(st["sub_fill"]), anchor="mm",
                   stroke_width=max(5, sw - 3), stroke_fill=(60, 40, 25))
            y += lz
        shadow = Image.new("RGBA", im.size, (20, 12, 5, 0))
        shadow.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * 0.5)))
        out = Image.new("RGBA", im.size, (0, 0, 0, 0))
        out.alpha_composite(shadow, (0, 4))
        out.alpha_composite(im)
        return out

    def card(self, li, wi):
        key = (li, wi)
        if key in self.cache:
            return self.cache[key]
        st, f = self.ctx.st, self.ctx.fonts
        ln = self.lines[li]
        color = rgb(st["speaker_colors"].get(ln["speaker"], st["speaker_colors"]["narrator"]))
        fe, fz = f.get("en", st["en_size"]), f.get("zh", st["zh_size"], "Medium")
        if st.get("subtitle_mode", "outline") == "outline":
            im = self.outline_card(ln, wi, color, fe, fz)
            self.cache[key] = im
            return im
        maxw = W - 160
        tokens = ln["tokens"]
        lines = wrap_tokens(tokens, fe, maxw)
        zh_lines = wrap_zh(ln.get("zh", ""), fz, maxw) if ln.get("zh") else []
        le, lz = int(fe.size * 1.22), int(fz.size * 1.4)
        space = fe.getlength(" ")
        widths = [sum(fe.getlength(tokens[i]) for i in l) + space * (len(l) - 1) for l in lines]
        pw = int(max(widths + [fz.getlength(z) for z in zh_lines])) + 100
        ph = le * len(lines) + lz * len(zh_lines) + 56
        im = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0))
        sh = Image.new("L", im.size, 0)
        ImageDraw.Draw(sh).rounded_rectangle([20, 26, 20 + pw, 26 + ph], radius=44, fill=110)
        shadow = Image.new("RGBA", im.size, (60, 35, 15, 0))
        shadow.putalpha(sh.filter(ImageFilter.GaussianBlur(10)))
        im.alpha_composite(shadow)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([20, 20, 20 + pw, 20 + ph], radius=44, fill=rgb(st["card_fill"]),
                            outline=rgb(st["card_outline"]), width=3)
        y = 48
        for l, lw in zip(lines, widths):
            x = 20 + (pw - lw) / 2
            for i in l:
                tw = fe.getlength(tokens[i])
                if i == wi:
                    d.rounded_rectangle([x - 10, y - 2, x + tw + 10, y + le - 6], radius=18, fill=rgb(st["highlight"]))
                d.text((x, y + le / 2), tokens[i], font=fe, fill=color, anchor="lm")
                x += tw + space
            y += le
        for z in zh_lines:
            d.text((20 + pw / 2, y + lz / 2 - 2), z, font=fz, fill=rgb(st["zh_color"]), anchor="mm")
            y += lz
        self.cache[key] = im
        return im

    def render(self, t, gt):
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        if self.bg is not None:
            frame.paste(self.bg, (0, 0))
        rx, ry, rw, rh = self.region
        iw, ih = self.img.size
        box = kb_box(self.motion, t / self.dur, iw, ih, rw, rh, self.focus, self.zoom, self.zoom_from)
        if self.fx or self.par:
            src = self.src.copy() if self.fx else self.src
            for fx in self.fx:
                fx.apply(src, t)
            src = np.clip(src, 0, 255).astype(np.uint8)
            region = self.warp(src, box, t) if self.par else Image.fromarray(src).resize((rw, rh), Image.BICUBIC, box=box)
        else:
            region = self.img.resize((rw, rh), Image.BICUBIC, box=box)
        frame.paste(region, (rx, ry))
        if self.ctx.sparkles:
            self.ctx.sparkles.draw(frame, gt)
        li, wi = self.state(t)
        if li is not None and self.ctx.st.get("subtitles", True):
            c = self.card(li, wi)
            cx = self.ctx.st.get("subtitle_x", W // 2) if self.ctx.st.get("subtitle_mode", "outline") == "outline" else W // 2
            frame.alpha_composite(c, (int(cx - c.width / 2), int(self.ctx.st["subtitle_center"] - c.height / 2)))
        if self.ctx.badge is not None:
            frame.alpha_composite(self.ctx.badge, tuple(self.ctx.st["badge_pos"]))
        return frame.convert("RGB")


class EndSeg:
    """片尾：现成的片尾卡图片（系列 make_end_card 出的图），或用最后一页 + 文字生成。最后 0.6 秒淡出。"""

    def __init__(self, ending, last_img, ctx, base):
        self.dur, self.cut, self.ctx = ending.get("seconds", 3.5), False, ctx
        if ending.get("image"):
            self.bg = cover_crop(Image.open(os.path.join(base, ending["image"])).convert("RGB")).convert("RGBA")
        else:
            st, f = ctx.st, ctx.fonts
            img = cover_crop(Image.open(last_img).convert("RGB")).filter(ImageFilter.GaussianBlur(14))
            bg = ImageEnhance.Brightness(img).enhance(0.55).convert("RGBA")
            d = ImageDraw.Draw(bg)
            stroke_text(d, (W // 2, 860), ending.get("headline", ""), f.get("zh", 80), rgb(st["headline_color"]), rgb(st["stroke"]))
            stroke_text(d, (W // 2, 990), ending.get("subline", ""), f.get("zh", 50), rgb(st["accent"]), (255, 255, 255), 6)
            self.bg = bg

    def render(self, t, gt):
        frame = self.bg.copy()
        if self.ctx.sparkles:
            self.ctx.sparkles.draw(frame, gt)
        frame = frame.convert("RGB")
        fade = ease((t - (self.dur - 0.6)) / 0.6)
        return ImageEnhance.Brightness(frame).enhance(1 - fade) if fade > 0 else frame


def transition(a, b, tau, kind):
    e = ease(tau)
    if kind == "slide":   # 翻页感：旧页左移变暗，新页带阴影从右滑入
        out = ImageEnhance.Brightness(a).enhance(1 - 0.45 * e)
        out = out.transform((W, H), Image.AFFINE, (1, 0, W * 0.3 * e, 0, 1, 0))
        bx = int(W * (1 - e))
        sd = Image.fromarray(np.tile(np.linspace(0, 110, 60, dtype=np.uint8), (H, 1)))
        out.paste((0, 0, 0), (max(bx - 60, 0), 0, bx, H), sd.crop((60 - min(60, bx), 0, 60, H)))
        out.paste(b.crop((0, 0, W - bx, H)), (bx, 0))
        return out
    return Image.blend(a, b, e)


def badge_image(series, fonts, base):
    if not series:
        return None
    if series.get("badge_image"):
        b = Image.open(os.path.join(base, series["badge_image"])).convert("RGBA")
    elif series.get("badge_text"):
        f = fonts.get("zh", 34, "Medium")
        tw = int(f.getlength(series["badge_text"]))
        b = Image.new("RGBA", (tw + 60, 68), (0, 0, 0, 0))
        d = ImageDraw.Draw(b)
        d.rounded_rectangle([0, 0, tw + 59, 67], radius=34, fill=(255, 248, 232, 255), outline=(232, 214, 186), width=3)
        d.text((30, 34), series["badge_text"], font=f, fill=(92, 52, 24), anchor="lm")
    else:
        return None
    b.putalpha(b.getchannel("A").point(lambda v: int(v * series.get("badge_alpha", 0.72))))
    return b


# ---------- 主流程 ----------

def page_lines(page):
    if "lines" in page:
        return page["lines"]
    return [{"speaker": page.get("speaker", "narrator"), "en": page["en"], "zh": page.get("zh", "")}]


def build(story_path, out_dir, max_pages=None, sparkle=True, cast_override=None):
    base = os.path.dirname(os.path.abspath(story_path))
    with open(story_path) as f:
        cfg = json.load(f)
    st = json.loads(json.dumps(DEFAULT_STYLE))
    for k, v in (cfg.get("style") or {}).items():
        if isinstance(v, dict) and isinstance(st.get(k), dict):
            st[k].update(v)
        else:
            st[k] = v
    cast = cfg.get("cast") or {"narrator": cfg.get("voice", {"provider": "kokoro", "voice": "af_heart"})}
    if cast_override:           # 命令行 --cast：临时换一份角色表（比如订阅前用 Kokoro 出样片）
        cast = os.path.abspath(cast_override)
    if isinstance(cast, str):   # 指向系列统一的角色表，例如 "../../series/cast.json"
        with open(os.path.join(base, cast)) as f:
            cast = {k: v for k, v in json.load(f).items() if not k.startswith("_")}
    os.makedirs(out_dir, exist_ok=True)
    cache, work = os.path.join(out_dir, ".cache"), os.path.join(out_dir, ".work")
    os.makedirs(cache, exist_ok=True)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)

    fonts = Fonts(st["fonts"], base)
    ctx = Ctx(st, fonts, Sparkles() if sparkle and st["sparkles"] else None,
              badge_image(cfg.get("series"), fonts, base), cache)
    pages = cfg["pages"]
    truncated = max_pages is not None and max_pages < len(pages)
    pages = pages[:max_pages] if truncated else pages
    TR = st["transition_seconds"]

    segs, placements, srt = [], [], []
    t = 0.0

    def add(seg):
        nonlocal t
        if segs:
            prev = segs[-1]
            t = prev.start + prev.dur - (0 if seg.cut else TR)
        seg.start = t
        segs.append(seg)

    if cfg.get("cover", {}).get("image"):
        add(StillSeg(os.path.join(base, cfg["cover"]["image"]), cfg["cover"].get("seconds", 0.4)))

    hook = cfg.get("hook")
    if hook and hook.get("clip"):
        clip = os.path.join(base, hook["clip"])
        hdir = os.path.join(work, "hook")
        os.makedirs(hdir)
        run(["ffmpeg", "-v", "error", "-i", clip, "-t", str(hook.get("max_seconds", 5)),
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
             "-q:v", "2", os.path.join(hdir, "h_%04d.jpg")])
        n = len([x for x in os.listdir(hdir) if x.endswith(".jpg")])
        seg = HookSeg(hook, hdir, n, ctx)
        add(seg)
        if hook.get("say"):
            say = hook["say"]
            wav, _ = synthesize(say.get("say", say["en"]), cast[say.get("speaker", "narrator")], cache)
            placements.append((wav, seg.start + say.get("at", 0.4), 1.0))
        if hook.get("keep_clip_audio"):
            placements.append((clip, seg.start, hook.get("clip_gain", 1.0)))
        for sx in hook.get("sfx", []):
            placements.append((os.path.join(base, sx["file"]), seg.start + sx.get("at", 0), sx.get("gain", 0.55)))

    for i, page in enumerate(pages):
        lines, cur = [], st["lead"]
        for ln in page_lines(page):
            if ln.get("audio"):
                wav, words = os.path.join(base, ln["audio"]), ln.get("words", [])
            else:
                # say：给配音用的文本，可带 v3 语气标签（如 [excited]），字幕仍显示 en；
                # take：想重录某一句时改成 2、3……，换一个缓存键重新生成
                voice = dict(cast[ln.get("speaker", "narrator")])
                if ln.get("take"):
                    voice["take"] = ln["take"]
                wav, words = synthesize(ln.get("say", ln["en"]), voice, cache)
            dur = probe_duration(wav)
            tokens = ln["en"].split()
            lines.append(dict(ln, speaker=ln.get("speaker", "narrator"), start=cur, end=cur + dur,
                              wav=wav, tokens=tokens, spans=align_tokens(tokens, words, wav)))
            cur += dur + ln.get("gap", st["gap"])
        seg = PageSeg(page, i, lines, ctx, base)
        add(seg)
        for ln in lines:
            # gain：单句音量，比如"小声说"的句子写 0.4
            placements.append((ln["wav"], seg.start + ln["start"], ln.get("gain", 1.0)))
            srt.append((seg.start + ln["start"] - 0.1, seg.start + ln["end"] + 0.4, ln["en"], ln.get("zh", "")))
        for sx in page.get("sfx", []):
            placements.append((os.path.join(base, sx["file"]), seg.start + sx.get("at", 0), sx.get("gain", 0.55)))

    if cfg.get("ending", {}) is not None:      # "ending": null 表示不要片尾卡
        ending = dict(cfg.get("ending", {}))
        if truncated:
            ending.pop("image", None)
            ending["headline"] = ending.get("feed_headline", "完整版在主页合集")
            ending["subline"] = ending.get("feed_subline", "")
        add(EndSeg(ending, os.path.join(base, pages[-1]["image"]), ctx, base))
    total = segs[-1].start + segs[-1].dur

    # 音频：人声按时间轴放置；背景音乐在有人说话时压到一半；最后统一响度
    n = int(total * SR) + 1
    voice = np.zeros(n, dtype=np.float32)
    for path, at, gain in placements:
        a = decode_audio(path) * gain
        o = int(at * SR)
        a = a[: max(0, n - o)]
        voice[o:o + len(a)] += a
    mix = voice.copy()
    bgm = cfg.get("bgm") or {}
    if bgm.get("file"):
        m = decode_audio(os.path.join(base, bgm["file"]))
        m = np.tile(m, n // len(m) + 1)[:n]
        win = int(0.25 * SR)
        env = np.convolve(np.abs(voice), np.ones(win) / win, mode="same")
        duck = np.convolve(np.clip(env / 0.01, 0, 1), np.ones(win) / win, mode="same")
        mix += m * bgm.get("volume", 0.25) * (1 - 0.5 * duck)
        fade = int(1.2 * SR)
        mix[-fade:] *= np.linspace(1, 0, fade)
    wav = os.path.join(work, "mix.wav")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1",
                          "-i", "-", wav], stdin=subprocess.PIPE)
    p.communicate(mix.astype(np.float32).tobytes())

    # 画面：逐帧渲染，管道送给 ffmpeg；音频做 -16 LUFS 响度标准化
    loud = cfg.get("loudness", {"I": -16, "TP": -1.5})
    # 两遍 loudnorm：先测混音的实际响度，再按实测值线性校正；单遍动态模式实测会低 1 LU 左右
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", wav, "-af",
                           f"loudnorm=I={loud['I']}:TP={loud['TP']}:LRA=11:print_format=json",
                           "-f", "null", "-"], check=True, capture_output=True, text=True).stderr
    m = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    af = (f"loudnorm=I={loud['I']}:TP={loud['TP']}:LRA=11:measured_I={m['input_i']}:"
          f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}:linear=true,aresample={SR}")
    name = cfg.get("output_name", "storybook") + ("_feed" if truncated else "")
    mp4 = os.path.join(out_dir, f"{name}.mp4")
    enc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-i", wav, "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-af", af,
         "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-shortest", "-movflags", "+faststart", mp4],
        stdin=subprocess.PIPE)
    n_frames = int(round(total * FPS))
    for fi in range(n_frames):
        gt = fi / FPS
        active = [s for s in segs if s.start <= gt < s.start + s.dur]
        if len(active) >= 2:
            a, b = active[-2], active[-1]
            img = transition(a.render(gt - a.start, gt), b.render(gt - b.start, gt),
                             (gt - b.start) / TR, st["transition"])
        else:
            s = active[0] if active else segs[-1]
            img = s.render(min(gt - s.start, s.dur - 1e-3), gt)
        enc.stdin.write(img.tobytes())
        if fi % (FPS * 10) == 0:
            print(f"  渲染 {gt:5.1f}s / {total:.1f}s", flush=True)
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("ffmpeg 编码失败")

    def ts(x):
        ms = int(round(max(x, 0) * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(os.path.join(out_dir, f"{name}.srt"), "w") as f:
        for k, (s, e, en, zh) in enumerate(srt, 1):
            f.write(f"{k}\n{ts(s)} --> {ts(e)}\n{en}\n{zh}\n\n")
    if not truncated:
        export_pdf(cfg, cfg["pages"], base, fonts, os.path.join(out_dir, f"{name}_print.pdf"))
    shutil.rmtree(work, ignore_errors=True)
    print(f"完成：{mp4}（{total:.1f} 秒）")
    return mp4


def export_pdf(cfg, pages, base, fonts, path):
    """A4 竖版 150dpi：封面 + 每页一图一文，可直接打印。"""
    PW, PH, M = 1240, 1754, 90
    ink, soft = (92, 52, 24), (110, 84, 62)
    cover = Image.new("RGB", (PW, PH), (255, 248, 232))
    d = ImageDraw.Draw(cover)
    d.text((PW // 2, 620), cfg.get("title_en", ""), font=fonts.get("en", 96, "Bold"), fill=ink, anchor="mm")
    d.text((PW // 2, 760), cfg.get("title_zh", ""), font=fonts.get("zh", 64), fill=soft, anchor="mm")
    d.text((PW // 2, 880), (cfg.get("series") or {}).get("badge_text", ""), font=fonts.get("zh", 40), fill=soft, anchor="mm")
    sheets = [cover]
    for i, page in enumerate(pages, 1):
        sh = Image.new("RGB", (PW, PH), (255, 255, 255))
        img = Image.open(os.path.join(base, page["image"])).convert("RGB")
        s = min((PW - 2 * M) / img.width, PH * 0.6 / img.height)
        img = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
        sh.paste(img, ((PW - img.width) // 2, M))
        d = ImageDraw.Draw(sh)
        y = M + img.height + 50
        fe, fz = fonts.get("en", 50), fonts.get("zh", 36)
        for ln in page_lines(page):
            toks = ln["en"].split()
            for l in wrap_tokens(toks, fe, PW - 2 * M):
                d.text((PW // 2, y), " ".join(toks[k] for k in l), font=fe, fill=ink, anchor="ma")
                y += 66
            for z in wrap_zh(ln.get("zh", ""), fz, PW - 2 * M) if ln.get("zh") else []:
                d.text((PW // 2, y), z, font=fz, fill=soft, anchor="ma")
                y += 50
            y += 18
        d.text((PW // 2, PH - 60), str(i), font=fz, fill=soft, anchor="mm")
        sheets.append(sh)
    sheets[0].save(path, save_all=True, append_images=sheets[1:], resolution=150)


def main():
    ap = argparse.ArgumentParser(description="动态绘本视频生成器")
    ap.add_argument("story", help="story.json 路径")
    ap.add_argument("--out", default="out", help="输出目录")
    ap.add_argument("--max-pages", type=int, help="只取前 N 页，生成推荐流精华版")
    ap.add_argument("--no-sparkle", action="store_true", help="关闭漂浮光点")
    ap.add_argument("--cast", help="临时替换角色表，例如 ../../series/cast_kokoro.json（只出样片用）")
    a = ap.parse_args()
    build(a.story, a.out, a.max_pages, not a.no_sparkle, a.cast)


if __name__ == "__main__":
    sys.exit(main())
