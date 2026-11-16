# 从 out/m07/soft.py 拷来：儿歌柔修（WORLD，只修偏差>40音分、音头渐进、不拉伸时间）+ 童声叠层 + 原唱对照。在 out/m07 下运行，依赖 make_song_frere.py（即 out/m07/make_song2.py）
"""m07 钩子段去机器味：①柔修（WORLD，只修偏差 >40 音分的音，保留原唱起伏/颤音，音头 60–120ms 渐进；不拉伸时间、保留共振峰）
③在柔修主唱下叠轻的童声合唱；④原唱不修。伴奏按原唱的实际节奏弹原谱。→ song/hook_*.mp3"""
import json, subprocess, sys
import numpy as np, soundfile as sf, pyworld as pw
import make_song2 as M
SR = M.SR; FP = 5.0   # WORLD 帧长 ms
VER = sys.argv[1] if len(sys.argv) > 1 else "v4"

def segments(S, vi):
    """和 make_song2.fix 同样的切法：返回 [(源起, 源止, 相对音高, 拍数)]"""
    words, pos, env = S["words"], S["pos"], S["env"]; v = S["struct"][vi]; segs = []
    for j in range(len(v)):
        i = S["offs"][vi] + j
        if i not in pos: continue
        wi = pos[i]; w = words[wi]; s = w["s"]
        e = words[wi + 1]["s"] if wi + 1 < len(words) and words[wi + 1]["s"] - w["e"] < .6 else w["e"] + .15
        syl = v[j][1]
        if len(syl) == 2:
            p, q = int((s + .3 * (e - s)) * SR), int((s + .75 * (e - s)) * SR); c = (p + env[p:q].argmin()) / SR; spans = [(s, c), (c, e)]
        else: spans = [(s, e)]
        for (ss, se), notes in zip(spans, syl):
            tot = sum(n[1] for n in notes); cur = ss
            for m, bt in notes:
                d = (se - ss) * bt / tot; segs.append((cur, cur + d, m, bt)); cur += d
    return segs

S = M.load(VER); segs = segments(S, 0)
base = int(round(S["med"] - 4))
a0 = max(0, segs[0][0] - .15); a1 = min(len(S["x"]) / SR, segs[-1][1] + .4)
x = S["x"][int(a0 * SR):int(a1 * SR)].astype(np.float64)
f0, t = pw.harvest(x, SR, f0_floor=120, f0_ceil=900, frame_period=FP); sp = pw.cheaptrick(x, f0, t, SR); ap = pw.d4c(x, f0, t, SR)
cents = np.zeros_like(f0); report = []
for sa, sb, m, bt in segs:
    fr = np.where((t >= sa - a0) & (t < sb - a0) & (f0 > 0))[0]
    if len(fr) < 4: continue
    med = 1200 * np.log2(np.median(f0[fr]) / M.hz(base + m))       # 这个音整体偏了多少音分（只看中位数，起伏保留）
    k = med if abs(med) > 40 else 0.0
    report.append(round(float(med)))
    if not k: continue
    ramp = np.ones(len(fr)); rl = int(np.clip((sb - sa) * 1000 * .3, 60, 120) / FP)   # 音头 60–120ms 渐进靠上去
    ramp[:rl] = np.linspace(.35, 1, min(rl, len(fr)))[:len(ramp[:rl])]
    cents[fr] = -k * ramp
# 音和音之间的修正量平滑过渡，避免硬拼接
cents = np.convolve(cents, np.ones(9) / 9, "same")
f1 = np.where(f0 > 0, f0 * 2 ** (cents / 1200), 0)
y = pw.synthesize(f1, sp, ap, SR, FP)
sf.write(f"song/hook_soft_{VER}_dry.wav", y / np.abs(y).max() * .9, SR)
# ③ 童声合唱叠层：同一条柔修人声做 2 个副本，共振峰抬高（像小朋友）、错位 18/31ms、音分 ±7，音量 -9 dB
def chorus(shift_cents, delay_ms, formant):
    n = sp.shape[1]; idx = np.clip((np.arange(n) / formant).astype(int), 0, n - 1); sp2 = np.ascontiguousarray(sp[:, idx])
    z = pw.synthesize(f1 * 2 ** (shift_cents / 1200), sp2, ap, SR, FP); d = int(delay_ms / 1000 * SR)
    return np.r_[np.zeros(d), z][:len(y)]
ch = chorus(+7, 18, 1.18) + chorus(-7, 31, 1.25)
yc = y + ch[:len(y)] * 10 ** (-9 / 20)
# 伴奏：按原唱的实际起点弹原谱
from sf2play import SF2
SF = SF2("../sf2/GeneralUser.sf2"); L = len(y) + SR; acc = np.zeros((L, 2))
def put(inst, key, vel, at, dur, g=1.0):
    z = SF.note(*inst, key, vel, dur, 0.0) * g; i = int(at * SR); j = min(L, i + len(z))
    if 0 <= i < L: acc[i:j] += z[:j - i]
beats = np.cumsum([0] + [b for *_, b in segs]); on = [sa - a0 for sa, *_ in segs]
for (sa, sb, m, bt), o in zip(segs, on): put((0, 9), base + m + 12, 66, o, (sb - sa) * 1.05, .45)
I = [0, 4, 7]; V = [-5, -1, 2]
for k in range(0, int(beats[-1]), 2):
    i = int(np.searchsorted(beats, k)); i = min(i, len(on) - 1); at = on[i]
    ch_ = V if (k // 2) % 4 == 3 else I; put((0, 45), base + ch_[0] - 12, 76, at, .5)
    for e, mm in enumerate(ch_ + [ch_[1]]): put((0, 8), base + mm + 12, 50, at + e * .25, .25)
acc = acc.mean(axis=1); acc /= np.abs(acc).max() + 1e-9
def out(voc, name):
    v = np.r_[voc, np.zeros(L - len(voc))]; mix = v / (np.abs(v).max() + 1e-9) * .9 + acc * .33
    sf.write("/tmp/_h.wav", mix / np.abs(mix).max() * .9, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/_h.wav", "-af", "loudnorm=I=-16:TP=-1.5", "-b:a", "128k", f"song/{name}.mp3"])
out(y, f"hook_soft_{VER}"); out(yc, f"hook_choir_{VER}")
# ④ 原唱不修：原版里钩子那一段（带原伴奏）
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a0:.2f}", "-to", f"{a1 + .5:.2f}", "-i", f"song/{VER}.mp3", "-af", "loudnorm=I=-16:TP=-1.5", "-b:a", "128k", f"song/hook_raw_{VER}.mp3"])
json.dump({"base": base, "offset_cents": report, "fixed": sum(abs(c) > 40 for c in report), "notes": len(report), "a0": a0},
          open(f"song/hook_{VER}.json", "w"))
print(VER, "修了", sum(abs(c) > 40 for c in report), "/", len(report), "个音；偏差音分", report)
