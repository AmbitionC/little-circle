# 从 out/m07/song_final.py 拷来：m07 成片儿歌逐段挑版本 + 柔修 + 童声叠层（在 out/m07 下运行）
"""m07 成片儿歌：v7–v11（三段：钩子整段 / 叫醒 AABBCD / 片尾 CCDD），逐段挑最像原旋律的版本，柔修 + 轻童声叠层。"""
import json, sys
import numpy as np, soundfile as sf, pyworld as pw
import make_song2 as M
from make_song2 import W, A, B, C, D, TIG, V1, CC
V2S = [W("are", [A[0]]), W("you", [A[1]]), W("sleeping", [A[2]], [A[3]])] * 2 + [W("bruno", [B[0]], [B[1], B[2]])] * 2 \
    + [W("morning", [C[0]], [C[1]]), W("bells", [C[2]]), W("are", [C[3]]), W("ringing", [C[4]], [C[5]])] \
    + [W("ding", [D[0]]), W("dang", [D[1]]), W("dong", [D[2]])]
V3S = CC + [W("hooray", [D[0]], [D[1], D[2]])] * 2
M.SONG["final"] = [V1, V2S, V3S]
SR = M.SR; FP = 5.0

def load(ver):
    old = M.SONG["new"]; M.SONG["new"] = M.SONG["final"]
    try: return M.load(ver)
    finally: M.SONG["new"] = old

def segments(S, vi):
    words, pos, env = S["words"], S["pos"], S["env"]; v = S["struct"][vi]; segs = []; miss = 0
    for j in range(len(v)):
        i = S["offs"][vi] + j
        if i not in pos: miss += 1; continue
        wi = pos[i]; w = words[wi]; s = w["s"]
        e = words[wi + 1]["s"] if wi + 1 < len(words) and words[wi + 1]["s"] - w["e"] < .6 else w["e"] + .15
        syl = v[j][1]
        if len(syl) == 2:
            p, q = int((s + .3 * (e - s)) * SR), int((s + .75 * (e - s)) * SR); c = (p + env[p:q].argmin()) / SR; spans = [(s, c), (c, e)]
        else: spans = [(s, e)]
        for (ss, se), notes in zip(spans, syl):
            tot = sum(n[1] for n in notes); cur = ss
            for m, bt in notes:
                d = (se - ss) * bt / tot; segs.append((cur, cur + d, m, bt, v[j][0])); cur += d
    return segs, miss

def match(S, vi):
    segs, miss = segments(S, vi); f0, t = S["f0"], S["t"]
    meds = []
    for sa, sb, m, *_ in segs:
        fr = np.where((t >= sa) & (t < sb) & (f0 > 0))[0]
        meds.append((12 * np.log2(np.median(f0[fr]) / 440) + 69 - m) if len(fr) >= 3 else None)
    best = (0, None)
    for base in range(48, 76):
        ok = sum(1 for x in meds if x is not None and abs(x - base) < .5)
        if ok > best[0]: best = (ok, base)
    n = len(segs) + miss
    return best[0] / max(n, 1), best[1], miss

if __name__ == "__main__":
    R = {}
    for v in sys.argv[1:]:
        S = load(v); R[v] = [match(S, vi) for vi in range(3)]
        print(v, " | ".join(f"段{vi+1} 匹配 {r[0]:.0%} 调 {r[1]} 漏词 {r[2]}" for vi, r in enumerate(R[v])))
    json.dump(R, open("song/match_final.json", "w"))

def soft_verse(S, vi, base):
    """柔修一段：不拉伸时间，只修偏差 >40 音分的音（音头 60–120ms 渐进），保留起伏和共振峰；加两层轻童声。
    返回 (人声, 段起点在源里的秒数, [(相对起点, 止, 音高, 拍数, 词)])"""
    segs, _ = segments(S, vi)
    a0 = max(0, segs[0][0] - .12); a1 = min(len(S["x"]) / SR, segs[-1][1] + .35)
    x = S["x"][int(a0 * SR):int(a1 * SR)].astype(np.float64)
    f0, t = pw.harvest(x, SR, f0_floor=120, f0_ceil=900, frame_period=FP); sp = pw.cheaptrick(x, f0, t, SR); ap = pw.d4c(x, f0, t, SR)
    cents = np.zeros_like(f0)
    for sa, sb, m, bt, w in segs:
        fr = np.where((t >= sa - a0) & (t < sb - a0) & (f0 > 0))[0]
        if len(fr) < 4: continue
        med = 1200 * np.log2(np.median(f0[fr]) / M.hz(base + m))
        if abs(med) <= 40: continue
        ramp = np.ones(len(fr)); rl = int(np.clip((sb - sa) * 1000 * .3, 60, 120) / FP)
        ramp[:rl] = np.linspace(.35, 1, min(rl, len(fr)))[:len(ramp[:rl])]
        cents[fr] = -med * ramp
    cents = np.convolve(cents, np.ones(9) / 9, "same")
    f1 = np.where(f0 > 0, f0 * 2 ** (cents / 1200), 0)
    y = pw.synthesize(f1, sp, ap, SR, FP)
    def chorus(c, dms, form):
        n = sp.shape[1]; idx = np.clip((np.arange(n) / form).astype(int), 0, n - 1); sp2 = np.ascontiguousarray(sp[:, idx])
        z = pw.synthesize(f1 * 2 ** (c / 1200), sp2, ap, SR, FP); d = int(dms / 1000 * SR); return np.r_[np.zeros(d), z][:len(y)]
    y = y + (chorus(+7, 18, 1.18) + chorus(-7, 31, 1.25))[:len(y)] * 10 ** (-9 / 20)
    return y / (np.abs(y).max() + 1e-9) * .9, a0, [(sa - a0, sb - a0, m, bt, w) for sa, sb, m, bt, w in segs]

def build(ver="v11"):
    S = load(ver); base = int(round(S["med"] - 4)); out = {"ver": ver, "base": base, "verses": []}
    for vi in range(3):
        y, a0, segs = soft_verse(S, vi, base)
        sf.write(f"song/final_v{vi + 1}.wav", y, SR)
        out["verses"].append({"file": f"song/final_v{vi + 1}.wav", "dur": len(y) / SR, "segs": segs})
    json.dump(out, open("song/final.json", "w"), ensure_ascii=False, indent=1); return out
