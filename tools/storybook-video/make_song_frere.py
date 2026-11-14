# 从 out/m07/make_song2.py 拷来：m07 儿歌逐音节修到 Frère Jacques 原谱（依赖 out/m03/sf2play.py、out/sf2/GeneralUser.sf2，在 out/m07 下运行）
"""m07 小老虎版儿歌：每段可以取不同版本的人声，逐音节修到 Frère Jacques 原谱（120 BPM），伴奏用 SF2 按原谱弹。
python make_song2.py v4 v5 v6  → 每个候选：第一段、片尾取该版，叫醒段固定取 v1。→ song/fixed2_<v>.wav、song/mix2_<v>.mp3"""
import json, re, subprocess, sys, difflib
import numpy as np, soundfile as sf, parselmouth, pyworld as pw
from parselmouth.praat import call
sys.path.insert(0, "../m03"); from sf2play import SF2
SR = 44100; BPM = 120; BEAT = 60 / BPM
A = [(0, 1), (2, 1), (4, 1), (0, 1)]; B = [(4, 1), (5, 1), (7, 2)]; C = [(7, .5), (9, .5), (7, .5), (5, .5), (4, 1), (0, 1)]; D = [(0, 1), (-5, 1), (0, 2)]
def W(word, *syl): return (word, list(syl))
TIG = [W("two", [A[0]]), W("little", [A[1]], [A[2]]), W("tigers", [(0, .5)], [(0, .5)])] * 2
CCe = lambda last: [W("now" if last == "x" else "one", [C[0]])]
V1 = TIG + [W("run", [B[0]]), W("so", [B[1]]), W("fast", [B[2]])] * 2 \
   + [W("one", [C[0]]), W("has", [C[1]]), W("got", [C[2]]), W("no", [C[3]]), W("ears", [C[4], C[5]]),
      W("one", [C[0]]), W("has", [C[1]]), W("got", [C[2]]), W("no", [C[3]]), W("tail", [C[4], C[5]])] \
   + [W("how", [D[0]]), W("strange", [D[1], D[2]])] * 2
V1OLD = [W("two", [A[0]]), W("little", [A[1]], [A[2]]), W("friends", [A[3]])] * 2 + V1[len(TIG):]
V2 = [W("are", [A[0]]), W("you", [A[1]]), W("sleeping", [A[2]], [A[3]])] * 2 + [W("bruno", [B[0]], [B[1], B[2]])] * 2 \
   + [W("morning", [C[0]], [C[1]]), W("bells", [C[2]]), W("are", [C[3]]), W("ringing", [C[4]], [C[5]])] * 2 \
   + [W("ding", [D[0]]), W("dang", [D[1]]), W("dong", [D[2]])] * 2
CC = [W("now", [C[0]]), W("weve", [C[1]]), W("got", [C[2]]), W("our", [C[3]]), W("ears", [C[4], C[5]]),
      W("now", [C[0]]), W("weve", [C[1]]), W("got", [C[2]]), W("our", [C[3]]), W("tail", [C[4], C[5]])]
V3OLD = CC + [W("hooray", [D[0]], [D[1], D[2]])] * 2
V3 = TIG + [W("happy", [B[0]], [B[1]]), W("now", [B[2]])] * 2 + V3OLD
SONG = {"v1": [V1OLD, V2, V3OLD], "new": [V1, V3]}     # 每个版本整首的段落结构（用来把时间戳和谱对齐）
OUT = [V1, V2, V3]; GAP = 2.0; T0 = 1.0
hz = lambda m: 440 * 2 ** ((m - 69) / 12); norm = lambda s: re.sub(r"[^a-z]", "", s.lower())

def load(ver):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"song/stems/{ver}/vocals.mp3", "-ac", "1", "-ar", str(SR), f"/tmp/_m07_{ver}.wav"])
    x = sf.read(f"/tmp/_m07_{ver}.wav")[0]
    f0, t = pw.dio(x.astype(np.float64), SR, f0_floor=120, f0_ceil=900, frame_period=10); f0 = pw.stonemask(x.astype(np.float64), f0, t, SR)
    win = int(.02 * SR); env = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, "same"))
    words = json.load(open(f"song/{ver}.json"))["words"]
    struct = SONG["v1"] if ver == "v1" else SONG["new"]
    seq = [w for v in struct for w in v]
    sm = difflib.SequenceMatcher(None, [norm(w["w"]) for w in words], [w for w, _ in seq], autojunk=False)
    pos = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): pos[blk.b + k] = blk.a + k
    offs = np.r_[0, np.cumsum([len(v) for v in struct])]
    return dict(x=x, f0=f0, t=t, env=env, words=words, pos=pos, offs=offs, struct=struct,
                med=12 * np.log2(np.median(f0[f0 > 0]) / 440) + 69)

def fix(S, vi, base, tgt, y):
    """把版本 S 的第 vi 段修到原谱，放在输出 y 的 tgt 秒。返回漏掉的词。"""
    x, f0, t, env, words, pos = S["x"], S["f0"], S["t"], S["env"], S["words"], S["pos"]
    v = S["struct"][vi]; segs = []; miss = []
    for j in range(len(v)):
        i = S["offs"][vi] + j
        if i not in pos: miss.append(v[j][0]); continue
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
    a0 = max(0, segs[0][0] - .06); a1 = min(len(x) / SR, segs[-1][1] + .05); seg = x[int(a0 * SR):int(a1 * SR)]; Ld = len(seg) / SR
    man = call(parselmouth.Sound(seg, SR), "To Manipulation", .01, 100, 900)
    dt = call("Create DurationTier", "d", 0, Ld); pt = call("Create PitchTier", "p", 0, Ld); eps = .002
    for sa, sb, m, bt in segs:
        ra, rb = sa - a0, sb - a0; f = np.clip(bt * BEAT / max(.04, rb - ra), .25, 6)
        call(dt, "Add point", ra + eps, f); call(dt, "Add point", max(ra + 2 * eps, rb - eps), f)
        fr = np.where((t >= sa) & (t < sb) & (f0 > 0))[0]
        if len(fr) < 3:
            call(pt, "Add point", ra + .01, hz(base + m)); call(pt, "Add point", max(ra + .02, rb - .01), hz(base + m))
        else:
            st = 12 * np.log2(f0[fr]); dev = np.clip(st - np.median(st), -.6, .6) * .6
            for tt, dd in zip(t[fr][::2], dev[::2]): call(pt, "Add point", tt - a0, hz(base + m) * 2 ** (dd / 12))
    call(dt, "Add point", 0, 1.0); call([pt, man], "Replace pitch tier"); call([dt, man], "Replace duration tier")
    o = call(man, "Get resynthesis (overlap-add)").values[0].copy()
    o /= np.sqrt(np.mean(o ** 2)) + 1e-9; o *= .08                          # 三段电平一致
    p = max(0, int((tgt - (segs[0][0] - a0)) * SR)); n = min(len(o), len(y) - p)
    fl = int(.04 * SR); o[-fl:] *= np.linspace(1, 0, fl); y[p:p + n] += o[:n]
    return miss

def build(tag, pick):
    """pick: [(版本, 该版本里的段号)] × 3"""
    srcs = {v: load(v) for v in {p[0] for p in pick}}
    base = int(round(np.mean([s["med"] for s in srcs.values()]) - 4))
    starts, tt = [], T0
    for v in OUT: starts.append(tt); tt += sum(n[1] for _, syl in v for s in syl for n in s) * BEAT + GAP
    y = np.zeros(int((tt + 1) * SR)); miss = []
    for k, (ver, vi) in enumerate(pick): miss += fix(srcs[ver], vi, base, starts[k], y)
    sf.write(f"song/fixed2_{tag}.wav", y / (np.abs(y).max() + 1e-9) * .9, SR)
    S = SF2("../sf2/GeneralUser.sf2"); L = len(y); acc = np.zeros((L, 2))
    def put(inst, key, vel, at, dur, g=1.0):
        z = S.note(*inst, key, vel, dur, 0.0) * g; i = int(at * SR); j = min(L, i + len(z))
        if i < L: acc[i:j] += z[:j - i]
    GLOCK, CELE, PIZZ = (0, 9), (0, 8), (0, 45); I = [0, 4, 7]; V = [-5, -1, 2]
    for vi, v in enumerate(OUT):
        t0 = starts[vi]; notes = [n for _, syl in v for s in syl for n in s]
        for m, bt in notes: put(GLOCK, base + m + 12, 70, t0, bt * BEAT * 1.1, .5); t0 += bt * BEAT
        nb = int(round(sum(n[1] for n in notes)))
        for b in range(0, nb, 2):
            ch = V if (b // 2) % 4 == 3 else I; at = starts[vi] + b * BEAT
            put(PIZZ, base + ch[0] - 12, 78, at, BEAT)
            for e, m in enumerate(ch + [ch[1]]): put(CELE, base + m + 12, 52, at + e * BEAT / 2, BEAT / 2)
    acc = acc.mean(axis=1); acc /= np.abs(acc).max() + 1e-9
    mix = y / (np.abs(y).max() + 1e-9) * .9 + acc * .35
    sf.write("/tmp/_m07_mix.wav", mix / np.abs(mix).max() * .9, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/_m07_mix.wav", "-af", "loudnorm=I=-16:TP=-1.5", "-b:a", "128k", f"song/mix2_{tag}.mp3"])
    json.dump({"base": base, "starts": starts, "missing": miss}, open(f"song/fixed2_{tag}.json", "w"))
    return {"base": base, "missing": miss}

if __name__ == "__main__":
    for v in sys.argv[1:]: print(v, build(v, [(v, 0), ("v1", 1), (v, 1)]))
