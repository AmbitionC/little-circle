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
    # 连字符两边并成一个词：Whisper 常把 Peekaboo 写成 "Peek -a -boo"
    return [w for w in re.sub(r"[^a-z0-9' ]", " ", re.sub(r"\s*-\s*", "", s.lower())).split() if w]


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
        if not ls:   # 复习卡这类没台词的页（m06 r1）
            continue
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
    song_mode = (cfg.get("song") or {}).get("file")
    # 配音逐句听写用 small.en：base.en 对 Boo!、Candy! 这种一两个词的带语气短句常听错（2026-11-01 s05）
    model = WhisperModel("base.en" if song_mode else "small.en", device="cpu", compute_type="int8")
    song = (cfg.get("song") or {}).get("file")
    if song:
        segs, _ = model.transcribe(a.mp4, language="en", word_timestamps=True, beam_size=5,
                                   initial_prompt="Hazel, Nutty, Bun. Help me, please! I can help!")
        words = [w for s in segs for w in s.words]
    else:
        # 配音：逐句截出字幕时间段单独听写。整片一次听写会漂（短词 Candy!、Boo! 被吞，下一句的词串进来），
        # 2026-11-01 s05 同一条片子跑两次结果都不一样
        words = []
        for i, s in enumerate(srt):
            a0 = max(0.0, s["start"] - 0.1)
            a1 = min(s["end"], srt[i + 1]["start"] - 0.05) if i + 1 < len(srt) else s["end"]
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a0:.3f}", "-to", f"{a1:.3f}", "-i", a.mp4,
                                  "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], check=True, capture_output=True).stdout
            x = np.frombuffer(raw, dtype=np.float32)
            opts = dict(language="en", word_timestamps=True, beam_size=5,
                        initial_prompt="Hazel, Nutty, Bun, Bruno, Pip, Fern.", condition_on_previous_text=False)
            # 跟读停顿是空白，不加 VAD Whisper 会在空白里编词（"Boo! Boo!"）
            segs = list(model.transcribe(x, vad_filter=True, vad_parameters={"min_silence_duration_ms": 300}, **opts)[0])
            if not segs:
                # VAD 会把 Pip 很尖的大喊整句当成非人声滤掉（c18 "Peekaboo! Here I am!"），空了就不带 VAD 再听一次
                segs = list(model.transcribe(x, **opts)[0])
            for seg in segs:
                for w in seg.words:
                    w.start, w.end = w.start + a0, w.end + a0
                    words.append(w)
    print(f"发音（Whisper {'base.en' if song else 'small.en，逐句'}）" + ("，儿歌：唱歌听写难一些，合格线 0.6" if song else ""))
    bad = []
    for i, (s, ln) in enumerate(zip(srt, lines)):
        got = [w for w in words if s["start"] - 0.15 <= (w.start + w.end) / 2 <= s["end"] + 0.15]
        heard = " ".join(w.word.strip() for w in got)
        want_n, got_n = norm_words(ln["en"]), norm_words(heard)
        ratio = difflib.SequenceMatcher(None, want_n, got_n).ratio()
        ok = ratio >= (0.6 if song else 0.75)
        if not ok and not song:
            # VAD 和系列名字的 prompt 会让短句听丢（x00 "Look! A monkey!" 只听到 Look），不带它们再听一次，取好的那次。
            # 真有杂音（Ahem, giraffe）重听还是不过，不会被放过
            a0 = max(0.0, s["start"] - 0.1)
            a1 = min(s["end"], srt[i + 1]["start"] - 0.05) if i + 1 < len(srt) else s["end"]
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a0:.3f}", "-to", f"{a1:.3f}", "-i", a.mp4,
                                  "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], check=True, capture_output=True).stdout
            segs = model.transcribe(np.frombuffer(raw, dtype=np.float32), language="en", beam_size=5, word_timestamps=True,
                                    condition_on_previous_text=False)[0]
            got2 = [w for g in segs for w in g.words]
            for w in got2:
                w.start, w.end = w.start + a0, w.end + a0
            again = " ".join(w.word.strip() for w in got2)
            r2 = difflib.SequenceMatcher(None, want_n, norm_words(again)).ratio()
            if r2 > ratio:
                got, heard, ratio = got2, again, r2   # got 也换掉：下面字幕对齐用它的首词时间
                ok = ratio >= 0.75
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

    # 7 版式和音量硬检查（2026-11-12 m06：头像跑到字幕下面、说话中途换图嘴不动、老乌龟小 8 dB，截图自查全没发现）
    lay_path = stem + "_layout.json"
    if not song:
        if not os.path.exists(lay_path):
            fails.append(f"没有 {os.path.basename(lay_path)}：用新版 sbv.py 重新合成（它会写每句的画面、张嘴帧和头像位置）")
        else:
            lay = json.load(open(lay_path, encoding="utf-8"))
            page_of = [(ln, p) for p in pages for ln in sbv.page_lines(p)]
            # 7a 头像在字幕左上方（c18 基准）；只有那一页 / 那一句写了 avatar_pos: below 才允许在下面
            print("字幕头像位置（基准：字幕左上方）")
            badav = []
            for i, L in enumerate(lay):
                if not L["avatar"]:
                    continue
                ln, p = page_of[i] if i < len(page_of) else ({}, {})
                below_ok = (ln.get("avatar_pos") or p.get("avatar_pos")) == "below"   # 只认按页 / 按句挪；整集改到下面不算（11-06 就是全局改的）
                ax, ay, asz = L["avatar"]
                if ay + asz > L["subtitle"][1] + 40 and not below_ok:
                    badav.append(i + 1)
            check(not badav, "每句头像都在字幕左上方" if not badav else f"头像不在字幕左上方的句子：{badav}")
            # 7b 每句说话时段里，画面上的每张图都要有张嘴帧
            print("张嘴帧覆盖（说话时段里显示的每张图都要有张嘴帧）")
            for i, L in enumerate(lay):
                ok = L["talk_cover"] >= 0.999
                miss = "、".join(f"{k} {v}s" for k, v in L["no_talk"].items())
                print(f"  {'✅' if ok else '❌'} {i + 1:2d} [{L['speaker']:8s}] {L['en'][:34]!r} 覆盖 {L['talk_cover']:.0%}" + ("" if ok else f"，缺：{miss}"))
                if not ok:
                    fails.append(f"第 {i + 1} 句说话时 {miss} 没有张嘴帧（嘴不动）")
            # 7c 逐句响度：各角色中位数相差 ≤3 dB，单句偏离全片中位数 ≤3 dB
            print("逐句响度（干声）")
            lv = [(L["speaker"], sbv.line_loudness(L["wav"])) for L in lay]
            med = float(np.median([v for _, v in lv]))
            by = {}
            for sp, v in lv:
                by.setdefault(sp, []).append(v)
            spm = {sp: float(np.median(v)) for sp, v in by.items()}
            for sp, v in spm.items():
                print(f"  {sp:8s} {v:6.1f} LUFS（{len(by[sp])} 句）")
            spread = max(spm.values()) - min(spm.values())
            check(spread <= 3, f"各角色响度最大差 {spread:.1f} dB（要求 ≤3）")
            far = [(i + 1, sp, round(v, 1)) for i, (sp, v) in enumerate(lv) if abs(v - med) > 3]
            check(not far, "每句响度离全片中位数都在 3 dB 内" if not far else f"响度偏离超过 3 dB 的句子：{far}")

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
        if spk not in cast:      # 几人齐喊（duo、all）、音效句（sfx）：不是单个角色的声音，不参与比较
            continue
        if ln.get("audio"):      # 预先处理好的配音（如 m02 按小节排好的句子）
            wav = os.path.join(base, ln["audio"])
        else:
            voice = dict(cast[spk])
            if ln.get("take"):
                voice["take"] = ln["take"]
            wav, _ = sbv.synthesize(ln.get("say", ln["en"]), voice, cache)
        x = pcm(wav)
        st = stats.setdefault(spk, {"f0": [], "wps": [], "soft": []})
        # 耳语没有音高，估出来的基频是乱的；这个角色有别的句子时，耳语句不算基频和语速
        if "[whisper" in ln.get("say", ""):
            st["soft"].append((f0(x), len(ln["en"].split()) / (len(x) / SR)))
            continue
        st["f0"].append(f0(x))
        st["wps"].append(len(ln["en"].split()) / (len(x) / SR))
    for st in stats.values():
        if not st["f0"]:
            st["f0"], st["wps"] = [v[0] for v in st["soft"]], [v[1] for v in st["soft"]]
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
