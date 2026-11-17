"""m07 成片：写 episodes/m07-two-tigers/story_final.json + 唱段静音字幕 wav + 全片配乐 bgm_final.wav（人声唱段 + SF2 伴奏，固定电平）。"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
sys.path.insert(0, "../../tools/storybook-video"); import sbv
import song_final as F
from sf2play import SF2
SR = 44100; EP = "../../episodes/m07-two-tigers/"; OUT = os.path.abspath("lines_final"); os.makedirs(OUT, exist_ok=True)
fin = json.load(open("song/final.json"))
# ---------- 唱段：按谱的词结构把音符段分回词，再分成歌词句 ----------
def words_of(vdef, segs):
    out, k = [], 0
    for w, syl in vdef:
        n = sum(len(s) for s in syl); g = segs[k:k + n]; k += n
        if g: out.append({"w": w, "s": g[0][0], "e": g[-1][1]})
    return out
V = [F.V1, F.V2S, F.V3S]
verse_words, verse_audio = [], []
for vi in range(3):
    x = sf.read(fin["verses"][vi]["file"])[0]; ws = words_of(V[vi], fin["verses"][vi]["segs"])
    if vi == 1:   # 叫醒段剪掉 morning bells are ringing：从 morning 起点剪到 ding 起点
        i0 = next(i for i, w in enumerate(ws) if w["w"] == "morning"); i1 = next(i for i, w in enumerate(ws) if w["w"] == "ding")
        a, b = ws[i0]["s"] - .03, ws[i1]["s"] - .03; cut = b - a
        f = int(.03 * SR); xa = x[:int(a * SR)].copy(); xb = x[int(b * SR):].copy()
        xa[-f:] *= np.linspace(1, 0, f); xb[:f] *= np.linspace(0, 1, f); x = np.r_[xa, xb]
        ws = ws[:i0] + [dict(w, s=w["s"] - cut, e=w["e"] - cut) for w in ws[i1:]]
    verse_words.append(ws); verse_audio.append(x)
LY = [[("Two little tigers, two little tigers,", 6), ("Run so fast, run so fast!", 6), ("One has got no ears, one has got no tail.", 10), ("How strange! How strange!", 4)],
      [("Are you sleeping, are you sleeping,", 6), ("Bruno? Bruno?", 2), ("Ding, dang, dong!", 3)],
      [("Now we've got our ears, now we've got our tail.", 10), ("Hooray! Hooray!", 2)]]
ZH = [["两只小老虎，两只小老虎，", "跑得快，跑得快！", "一只没有耳朵，一只没有尾巴。", "真奇怪！真奇怪！"],
      ["你在睡觉吗，你在睡觉吗，", "Bruno？Bruno？", "叮、当、咚！"],
      ["耳朵找到了，尾巴也找到了。", "好耶！好耶！"]]
def sung(vi):
    """→ [(line dict, 起, 止)]，起止是这段人声里的秒数"""
    ws, k, out = verse_words[vi], 0, []
    for (en, n), zh in zip(LY[vi], ZH[vi]):
        g = ws[k:k + n]; k += n; s, e = g[0]["s"], g[-1]["e"] + .05
        p = os.path.join(OUT, f"sung_{vi}_{k}.wav"); sf.write(p, np.zeros(int((e - s) * SR)), SR)
        toks = en.split(); words = [{"w": toks[i] if i < len(toks) else w["w"], "s": w["s"] - s, "e": w["e"] - s} for i, w in enumerate(g)]
        out.append(({"speaker": "song", "en": en, "zh": zh, "audio": os.path.relpath(p, os.path.abspath(EP)), "words": words, "gain": 0}, s, e))
    return out
S1, S2, S3 = sung(0), sung(1), sung(2)
def sung_page(items, tail_to=None):
    """一页里的唱段：lead = 第一句起点，句间 gap = 下一句起点 - 本句止；hold 补到 tail_to（这段人声的结尾）"""
    lines = []
    for i, (ln, s, e) in enumerate(items):
        if i + 1 < len(items): ln = dict(ln, gap=items[i + 1][1] - e)
        lines.append(ln)
    return lines, items[0][1], (tail_to - items[-1][2]) if tail_to is not None else 0.0
F_ = "../../assets/sfx/"
cast = {k: v for k, v in json.load(open(EP + "cast.json")).items() if not k.startswith("_")}
def L(sp, en, zh, say, talk, where, **kw): return dict({"speaker": sp, "en": en, "zh": zh, "say": say, "talk": talk, "where": where}, **kw)
P = []
l, lead, _ = sung_page(S1[:2]); P.append({"image": "h01.png", "cut": True, "lead": lead, "hold": S1[2][1] - S1[1][2], "motion": "in", "lines": l,
  "word": {"en": "Two Little Tigers", "zh": "两只老虎 · 英文版"}, "frames": [{"image": "h01b.png", "line": 0, "offset": 2.0, "tween": 0}, {"image": "h02.png", "line": 1, "offset": 1.4, "tween": 0, "shake": True}],
  "sfx": [{"file": F_ + "steps_grass.wav", "at": .2, "gain": .25, "dur": 2.0}]})
P[-1]["sfx"].append({"file": F_ + "rustle_quick.wav", "at": 0, "gain": .4, "_rel": ("line", 1, 1.4)})
l, _, hold = sung_page(S1[2:], len(verse_audio[0]) / SR); P.append({"image": "p01.png", "cut": True, "lead": 0.0, "hold": hold, "motion": "in", "lines": l,
  "word": {"en": "Where's the tail?", "zh": "谁的尾巴不见了？"}, "frames": [{"image": "p01b.png", "line": 1, "offset": 0, "tween": 0}]})
P.append({"image": "p02.png", "cut": True, "lead": .15, "hold": .1, "motion": "in", "lines": [
  L("tigo", "My tail! Where's my tail?", "我的尾巴！我的尾巴在哪儿？", "[worried] My tail! Where's my tail?", {"p02.png": "p02_tigo.png"}, [.66, .52], gap=.2),
  L("mimi", "Oh! My ears!", "哦！我的耳朵！", "[surprised] Oh! My ears!", {"p02.png": "p02_mimi.png"}, [.32, .47])],
  "sfx": [{"file": F_ + "pop.mp3", "at": 3.0, "gain": .35}]})
P.append({"image": "p03.png", "cut": True, "lead": .3, "hold": .15, "motion": "in", "lines": [
  L("tigo", "There! Bruno! Wake up!", "在那儿！Bruno！快醒醒！", "There! Bruno! Wake up!", {"p03.png": "p03_tigo.png"}, [.18, .50])],
  "sfx": [{"file": F_ + "snore.mp3", "at": 0, "gain": .35}]})
P.append({"image": "p04.png", "cut": True, "seconds": 2.1, "motion": "in", "lines": [], "word": {"en": "Zzz... HONK!", "zh": "叫不醒！"},
  "frames": [{"image": "p04x1.png", "at": .45, "tween": 0}, {"image": "p04b.png", "at": .9, "tween": 0, "shake": True}, {"image": "p04x2.png", "at": 1.5, "tween": 0}],
  "sfx": [{"file": F_ + "snore.mp3", "at": .05, "gain": .4}, {"file": F_ + "whoosh.mp3", "at": .85, "gain": .3}, {"file": F_ + "thump.mp3", "at": 1.5, "gain": .25}]})
P.append({"image": "p05.png", "cut": True, "lead": .15, "hold": .45, "motion": "in", "lines": [
  L("mimi", "I have an idea! Let's sing!", "我有办法！我们来唱歌！", "[excited] I have an idea! Let's sing!", {"p05.png": "p05_mimi.png"}, [.58, .60])],
  "frames": [{"image": "p05b.png", "line": 0, "offset": 1.95, "tween": 0}], "sfx": [{"file": F_ + "ding.mp3", "at": .25, "gain": .3}]})
l, lead, hold = sung_page(S2, len(verse_audio[1]) / SR)
P.append({"image": "p06a.png", "cut": True, "lead": lead, "hold": hold, "motion": "in", "lines": l, "word": {"en": "Wake up, Bruno!", "zh": "宝宝一起唱，叫醒 Bruno！"},
  "frames": [{"image": "p06b.png", "line": 1, "offset": 0, "tween": 0}, {"image": "p06c.png", "line": 2, "offset": 0, "tween": 0}]})
P.append({"image": "p06c.png", "cut": True, "lead": .7, "hold": .15, "motion": "in", "lines": [
  L("bruno", "I'm awake!", "我醒啦！", "[surprised] I'm awake!", {"p07.png": "p07_bruno.png"}, [.39, .34], gap=.2),
  L("tigo", "My tail!", "我的尾巴！", "[happy] My tail!", {"p07.png": "p07_tigo.png"}, [.77, .58])],
  "frames": [{"image": "p07x1.png", "at": .05, "tween": 0}, {"image": "p07.png", "at": .4, "tween": 0, "shake": True}], "sfx": [{"file": F_ + "boing.mp3", "at": .4, "gain": .35}]})
P.append({"image": "p08.png", "cut": True, "lead": .15, "hold": .15, "motion": "in", "lines": [
  L("bruno", "Sorry, Tigo!", "对不起，Tigo！", "[sheepish] Sorry, Tigo!", {"p08.png": "p08_bruno.png"}, [.57, .35])]})
P.append({"image": "p09.png", "cut": True, "lead": .2, "hold": .2, "motion": "in", "lines": [
  L("mimi", "My ears!", "我的耳朵！", "[surprised] My ears!", {"p09.png": "p09_mimi.png"}, [.44, .70])],
  "sfx": [{"file": F_ + "thump.mp3", "at": .1, "gain": .3}]})
l, lead, hold = sung_page(S3, len(verse_audio[2]) / SR)
P.append({"image": "p08.png", "cut": True, "lead": lead, "hold": hold + .3, "motion": "in", "lines": l, "word": {"en": "tail · ears · wake up", "zh": "尾巴 · 耳朵 · 醒醒"}, "frames": [{"image": "p08b.png", "line": 1, "offset": 0, "tween": 0}]})
# 台词加快 1.15 倍（保持音高），写成 audio + words
CACHE = os.path.abspath("../m07/.cache")
for pg in P:
    for ln in pg["lines"]:
        if ln["speaker"] == "song": continue
        w, words = sbv.synthesize(ln["say"], dict(cast[ln["speaker"]]), CACHE)
        dst = os.path.join(OUT, os.path.basename(w).replace(".wav", "_t115.wav"))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", w, "-af", "atempo=1.15", dst], check=True)
        ln["audio"] = os.path.relpath(dst, os.path.abspath(EP)); ln["words"] = [{"w": x["w"], "s": x["s"] / 1.15, "e": x["e"] / 1.15} for x in words]
# 修正 h01 的 rustle 时间（第 2 句起点 + 1.4）
p0 = P[0]; t2 = p0["lead"] + sbv.probe_duration(os.path.join(EP, p0["lines"][0]["audio"])) + p0["lines"][0].get("gap", .3) + 1.3
for s_ in p0["sfx"]:
    if s_.pop("_rel", None): s_["at"] = round(t2, 2)
# ---------- 时间线（全部硬切，页首尾相接）----------
def dur(pg):
    if not pg["lines"]: return pg.get("seconds", 3)
    cur = pg.get("lead", .5); end = cur
    for ln in pg["lines"]:
        d = sbv.probe_duration(os.path.join(EP, ln["audio"])) if ln.get("audio") else sbv.probe_duration(
            sbv.level_line(sbv.synthesize(ln["say"], dict(cast[ln["speaker"]]), os.path.abspath("../m07/.cache"))[0], os.path.abspath("../m07/.cache"), -15))
        end = cur + d; cur = end + ln.get("gap", .3)
    return end + pg.get("hold", 0)
starts, t = [], 0.0
for pg in P: starts.append(t); t += dur(pg)
ENDING = 0.7; total = t + ENDING
print("页时长", [round(dur(p), 2) for p in P], "合计", round(total, 1))
# ---------- 配乐：人声唱段 + SF2 伴奏（唱段跟歌手节奏，其余按 120 BPM 弹原曲），固定电平 ----------
base = fin["base"]; BEAT = .5; SFo = SF2("../sf2/GeneralUser.sf2"); N = int((total + 1) * SR)
acc = np.zeros((N, 2)); voc = np.zeros(N)
def put(inst, key, vel, at, d, g=1.0):
    z = SFo.note(*inst, key, vel, d, 0.0) * g; i = int(at * SR); j = min(N, i + len(z))
    if 0 <= i < N: acc[i:j] += z[:j - i]
TUNE = [n for ph in [F.A, F.A, F.B, F.B, F.C, F.C, F.D, F.D] for n in ph]
I = [0, 4, 7]; Vc = [-5, -1, 2]
sung_ranges = []
for pi, vi in [(0, 0), (6, 1), (10, 2)]:
    t0 = starts[pi]; x = verse_audio[vi]; i = int(t0 * SR); voc[i:i + len(x)] += x[:N - i]
    segs = fin["verses"][vi]["segs"]
    if vi == 1:   # 剪过的段：按剪后的词起点弹
        ons = [(w["s"]) for w in verse_words[1]]; notes = [(F.V2S, )]
    ws = verse_words[vi]
    for k, w in enumerate(ws):
        put((0, 9), base + 12 + {"two":0}.get("", 0), 0, 0, 0)  # 占位，不发声
    # 旋律：按词的起点和谱上的音
    seq = [(w["s"], n) for w, (word, syl) in zip(ws, [x for x in V[vi] if not (vi == 1 and x[0] in ("morning", "bells", "are", "ringing") and False)]) for n in [syl[0][0]]]
    sung_ranges.append((t0, t0 + len(x) / SR))
# 旋律和和弦：唱段按歌手实际的音符段；台词段按 120 BPM 循环原曲
def mel_from(vi, t0):
    segs = fin["verses"][vi]["segs"]
    if vi == 1:
        ws = verse_words[1]; keep = []
        cut_a = next(w["s"] for w in ws if w["w"] == "ding")
        # 剪掉 morning…ringing 那几个音：用剪后的词起点重新对应
        orig = words_of(F.V2S, segs); i0 = next(i for i, w in enumerate(orig) if w["w"] == "morning"); i1 = next(i for i, w in enumerate(orig) if w["w"] == "ding")
        a, b = orig[i0]["s"] - .03, orig[i1]["s"] - .03
        segs = [s for s in segs if s[1] <= a + .02] + [(s[0] - (b - a), s[1] - (b - a), *s[2:]) for s in segs if s[0] >= b - .02]
    for sa, sb, m, bt, w in segs: put((0, 9), base + m + 12, 64, t0 + sa, (sb - sa) * 1.05, .45)
    for k in range(0, len(segs), 4):
        at = t0 + segs[k][0]; ch = Vc if (k // 4) % 4 == 3 else I
        put((0, 45), base + ch[0] - 12, 74, at, .5)
        for e, mm in enumerate(ch + [ch[1]]): put((0, 8), base + mm + 12, 48, at + e * .25, .25)
for pi, vi in [(0, 0), (6, 1), (10, 2)]: mel_from(vi, starts[pi])
free = []; prev = 0.0
for a, b in sung_ranges: free.append((prev, a)); prev = b
free.append((prev, total))
for a, b in free:
    tt, k = a + .1, 0
    while tt < b - .3:
        m, bt = TUNE[k % len(TUNE)]; put((0, 9), base + m + 12, 50, tt, bt * BEAT * 1.05, .35)
        if k % 4 == 0:
            ch = I; put((0, 45), base + ch[0] - 12, 60, tt, .5)
            for e, mm in enumerate(ch + [ch[1]]): put((0, 8), base + mm + 12, 40, tt + e * .25, .25)
        tt += bt * BEAT; k += 1
a_ = acc.mean(axis=1); a_ /= np.abs(a_).max() + 1e-9
mix = a_ * .3 + voc / (np.abs(voc).max() + 1e-9) * .9
fl = int(1.0 * SR); mix[-fl:] *= np.linspace(1, 0, fl)
sf.write("bgm_final.wav", mix / np.abs(mix).max() * .9, SR)
# ---------- story ----------
st = json.load(open(EP + "story.json"))
story = {"output_name": "m07_two_tigers", "title_en": "Two Little Tigers", "title_zh": "两只老虎",
 "_说明": "2026-11-17 成片：关键帧 + 张嘴帧；三段唱（钩子 / 叫醒 / 片尾）柔修 + 童声叠层，唱词字幕用静音 wav（speaker song）；配乐 out/m07/bgm_final.wav 全片固定电平。H3 线路下线，p4、p7 用关键帧补帧。",
 "series": {"badge_text": "栗栗学英语 · 英文儿歌", "badge_alpha": .72},
 "style": {"speaker_colors": {"tigo": [200, 100, 30], "mimi": [150, 90, 160], "bruno": [120, 72, 30], "song": [190, 130, 20]},
           "tail": 0, "bgm_rel_db": -6.0, "bgm_duck_db": 0, "kb_linear": True, "avatar_dir": ["refs/avatars", "../../series/refs/avatars"]},
 "cast": "cast.json", "pages": P, "ending": {"headline": "tail 尾巴 · ears 耳朵 · wake up 醒醒", "subline": "和宝宝一起唱：Two little tigers!", "seconds": ENDING, "motion": True},
 "ai_note": "画面和配音由 AI 生成", "loudness": {"I": -16, "TP": -1.5}, "target_seconds": 50,
 "ambience": {"cues": [{"page": 0, "file": "../../assets/sfx/amb_forest_birds.wav", "volume": .8, "fade": 1.0}]},
 "bgm": {"file": "../../out/m07/bgm_final.wav", "volume": .2}}
json.dump(story, open(EP + "story_final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("写好 story_final.json，总长约", round(total, 1))
