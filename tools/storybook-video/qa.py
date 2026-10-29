#!/usr/bin/env python3
"""成片质检：格式、响度、第 0 帧、每页总览图、发音（Whisper 转写对照）、角色基频语速、字幕对齐、时长。

用法（在本目录下，ffmpeg 要在 PATH 里）：
    python qa.py ../../episodes/s02-help/story.json ../../out/s02/s02_help.mp4 --dur 40 55
    python qa.py ../../episodes/s02-help/story.json ../../out/s02/s02_help_feed.mp4 --dur 20 35 --max-pages 4
依赖：faster-whisper（pip install faster-whisper，第一次会下 base.en 模型）。
总览图存在成片旁边：<名字>_sheet.jpg；第 0 帧：<名字>_frame0.jpg。
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw

import sbv

SR = 16000


def sh(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def parse_srt(path):
    def sec(x):
        h, m, s = x.replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    out = []
    for block in open(path).read().strip().split("\n\n"):
        ls = block.splitlines()
        a, b = ls[1].split(" --> ")
        out.append({"start": sec(a), "end": sec(b), "en": ls[2]})
    return out


def frame(mp4, t, path):
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1", path])
    return Image.open(path).convert("RGB")


def pcm(path, a=None, b=None):
    cmd = ["ffmpeg", "-v", "error"]
    if a is not None:
        cmd += ["-ss", f"{a:.3f}", "-to", f"{b:.3f}"]
    raw = subprocess.run(cmd + ["-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def f0(x):
    """自相关估基频，取有声帧的中位数（Hz）。"""
    n, hop, vals = int(0.04 * SR), int(0.01 * SR), []
    lo, hi = int(SR / 600), int(SR / 80)
    rms_all = np.sqrt(np.mean(x ** 2)) + 1e-9
    for i in range(0, len(x) - n, hop):
        fr = x[i:i + n] * np.hanning(n)
        if np.sqrt(np.mean(fr ** 2)) < rms_all * 0.6:
            continue
        ac = np.correlate(fr, fr, "full")[n - 1:]
        if ac[0] <= 0:
            continue
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] / ac[0] > 0.45:
            vals.append(SR / k)
    return float(np.median(vals)) if vals else float("nan")


def norm_words(s):
    return [w for w in re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("-", " ")).split() if w]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("mp4")
    ap.add_argument("--dur", nargs=2, type=float, required=True)
    ap.add_argument("--max-pages", type=int)
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.story))
    cfg = json.load(open(a.story))
    stem = os.path.splitext(a.mp4)[0]
    fails = []

    def check(ok, msg):
        print(("  ✅ " if ok else "  ❌ ") + msg)
        if not ok:
            fails.append(msg)

    # 1 格式 + 时长
    info = json.loads(sh(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", a.mp4]).stdout)
    v = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    dur = float(info["format"]["duration"])
    print("格式 / 时长")
    check(v["width"] == 1080 and v["height"] == 1920, f"分辨率 {v['width']}×{v['height']}")
    check(v["r_frame_rate"] == "30/1", f"帧率 {v['r_frame_rate']}")
    check(a.dur[0] <= dur <= a.dur[1], f"时长 {dur:.1f} 秒（要求 {a.dur[0]:.0f}–{a.dur[1]:.0f}）")

    # 2 响度
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.mp4, "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    summ = r[r.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summ).group(1))
    P = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ).group(1))
    print("响度")
    check(-17 <= I <= -15, f"I = {I} LUFS（要求 -16±1）")
    check(P <= -1.5, f"真峰值 = {P} dBFS（要求 ≤ -1.5）")

    # 3 第 0 帧
    f0img = frame(a.mp4, 0, stem + "_frame0.jpg")
    arr = np.asarray(f0img).astype(float)
    print("第 0 帧")
    check(arr.mean() > 30, f"平均亮度 {arr.mean():.0f}（不黑屏），见 {stem}_frame0.jpg")

    # 4 每页 2 帧总览（按 SRT 把句子分回各页）
    srt = parse_srt(stem + ".srt")
    pages = cfg["pages"][:a.max_pages] if a.max_pages else cfg["pages"]
    lines = [ln for p in pages for ln in sbv.page_lines(p)]
    assert len(srt) == len(lines), f"SRT {len(srt)} 句，story {len(lines)} 句，对不上"
    shots, k, tmp = [], 0, tempfile.mkdtemp()
    for pi, p in enumerate(pages):
        ls = srt[k:k + len(sbv.page_lines(p))]
        k += len(ls)
        for t, tag in ((ls[0]["start"] + 0.5, "a"), (ls[-1]["end"] - 0.5, "b")):
            shots.append((f"p{pi + 1:02d}{tag} {t:.1f}s", frame(a.mp4, t, os.path.join(tmp, f"{pi}{tag}.jpg"))))
    tw, th, cols = 270, 480, 8
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, (th + 30) * rows), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    for i, (lab, im) in enumerate(shots):
        x, y = (i % cols) * tw, (i // cols) * (th + 30)
        sheet.paste(im.resize((tw, th)), (x, y + 30))
        d.text((x + 6, y + 8), lab, fill=(0, 0, 0))
    sheet.save(stem + "_sheet.jpg", quality=90)
    # 黑边：每张抽帧四条边的平均亮度
    edges = [min(np.asarray(im)[:6].mean(), np.asarray(im)[-6:].mean(),
                 np.asarray(im)[:, :6].mean(), np.asarray(im)[:, -6:].mean()) for _, im in shots]
    print("画面")
    check(min(edges) > 25, f"四边最暗处亮度 {min(edges):.0f}（没有黑边）；总览图 {stem}_sheet.jpg（字幕挡脸要人眼看）")

    # 5 发音：Whisper 转写，按 SRT 时间段逐句对照
    from faster_whisper import WhisperModel
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(a.mp4, language="en", word_timestamps=True, beam_size=5,
                               initial_prompt="Hazel, Nutty, Bun. Help me, please! I can help!")
    words = [w for s in segs for w in s.words]
    song = (cfg.get("song") or {}).get("file")
    print("发音（Whisper base.en）" + ("，儿歌：唱歌听写难一些，合格线 0.6" if song else ""))
    bad = []
    for i, (s, ln) in enumerate(zip(srt, lines)):
        got = [w for w in words if s["start"] - 0.15 <= (w.start + w.end) / 2 <= s["end"] + 0.15]
        heard = " ".join(w.word.strip() for w in got)
        want_n, got_n = norm_words(ln["en"]), norm_words(heard)
        ratio = difflib.SequenceMatcher(None, want_n, got_n).ratio()
        ok = ratio >= (0.6 if song else 0.75)
        print(f"  {'✅' if ok else '⚠️'} {i + 1:2d} [{ln.get('speaker', 'narrator'):8s}] {ln['en']!r} → {heard!r} ({ratio:.2f})")
        if not ok:
            bad.append(i + 1)
        # 6 字幕对齐：字幕出现后 0.6 秒内要有词开始
        first = min((w.start for w in got), default=None)
        if first is None or first - s["start"] > 0.6:
            fails.append(f"字幕 {i + 1} 出现后 0.6 秒内没有人声（首词 {first}）")
    if bad:
        fails.append(f"发音可疑的句子：{bad}")
    print("字幕对齐")
    check(not any(f.startswith("字幕") for f in fails), "每条字幕出现后 0.6 秒内都有人声")

    if song:   # 儿歌没有配音，不查角色声音
        print("\n结论：" + ("全部通过" if not fails else "有问题：\n  - " + "\n  - ".join(fails)))
        return 1 if fails else 0

    # 7 角色基频和语速（用配音缓存里的干声）
    cast_path = os.path.join(base, cfg["cast"])
    cast = {k2: v2 for k2, v2 in json.load(open(cast_path)).items() if not k2.startswith("_")}
    cache = os.path.join(os.path.dirname(a.mp4), ".cache")
    stats = {}
    for ln in lines:
        spk = ln.get("speaker", "narrator")
        voice = dict(cast[spk])
        if ln.get("take"):
            voice["take"] = ln["take"]
        wav, _ = sbv.synthesize(ln.get("say", ln["en"]), voice, cache)
        x = pcm(wav)
        st = stats.setdefault(spk, {"f0": [], "wps": []})
        st["f0"].append(f0(x))
        st["wps"].append(len(ln["en"].split()) / (len(x) / SR))
    print("角色声音")
    summary = {}
    for spk, st in stats.items():
        summary[spk] = (float(np.nanmedian(st["f0"])), float(np.mean(st["wps"])))
        print(f"  {spk:8s} 基频 {summary[spk][0]:5.0f} Hz  语速 {summary[spk][1]:.2f} 词/秒（{len(st['f0'])} 句）")
    # 本集出场的角色两两比（旁白除外）：基频差 <30Hz 且语速差 <10% 就算分不清
    roles = [s for s in summary if s != "narrator"]
    for i, a1 in enumerate(roles):
        for a2 in roles[i + 1:]:
            df = abs(summary[a1][0] - summary[a2][0])
            dr = abs(summary[a1][1] - summary[a2][1]) / summary[a1][1]
            check(not (df < 30 and dr < 0.1),
                  f"{a1.title()} 和 {a2.title()} 基频差 {df:.0f} Hz，语速差 {dr:.0%}")

    print("\n结论：" + ("全部通过" if not fails else "有问题：\n  - " + "\n  - ".join(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
