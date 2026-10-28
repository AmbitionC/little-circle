#!/usr/bin/env python3
"""儿歌：按 story.json 的 song 段落用 ElevenLabs Music 生成歌，拿回每个词的时间戳，给 sbv.py 切卡和逐词高亮。

只用标准库（听写质检要 faster-whisper，可选）。key 从环境变量 ELEVENLABS_API_KEY 读。

    python3 song.py ../../episodes/m01-big-small              # 出 3 版（story.json 的 song.variants）→ out/m01/song/v1–v3
    python3 song.py ../../episodes/m01-big-small --variants 1 # 只再出 1 版（编号接着往后排）
    python3 song.py ../../episodes/m01-big-small --check      # 听写每一版，对照歌词、核对每段时长，给出推荐
    python3 song.py ../../episodes/m01-big-small --pick 2     # 选第 2 版：写成 song.mp3 + song_words.json，路径写回 story.json

歌词从 song.sections 读：写了 pages 的段落，歌词就是那几页 lines 的 en；没写 pages 的段落（前奏、尾奏）用自己的 lines。
每段的时长就是卡片时长，music_v2_5 会严格照着来。生成的音频只留在本机 out/ 下（仓库公开，不提交）。
"""
import argparse, difflib, email, glob, json, os, re, shutil, ssl, subprocess, sys, time
import urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
API = os.environ.get("ELEVENLABS_API_BASE", "https://api.elevenlabs.io").rstrip("/")


def lyrics(story, sec):
    if sec.get("pages"):
        pages = {os.path.splitext(p["image"])[0]: p for p in story["pages"]}
        return [ln["en"] for k in sec["pages"] for ln in pages[k]["lines"]]
    return sec.get("lines", [])


def plan(story, model):
    """作曲计划。music_v2_5 / v2 用 chunks，music_v1 用 sections，两种格式不能混。"""
    song = story["song"]
    styles, neg = song.get("styles", []), song.get("negative", [])
    secs = song["sections"]
    if model == "music_v1":
        return {"positive_global_styles": styles, "negative_global_styles": neg, "sections": [
            {"section_name": s["name"], "duration_ms": int(s["seconds"] * 1000), "lines": lyrics(story, s),
             "positive_local_styles": [s["direction"]] if s.get("direction") else [], "negative_local_styles": []}
            for s in secs]}
    chunks = []
    for s in secs:
        text = f"[{s['name']}]\n" + (f"{{{s['direction']}}}\n" if s.get("direction") else "") + "\n".join(lyrics(story, s))
        chunks.append({"text": text.strip(), "duration_ms": int(s["seconds"] * 1000),
                       "positive_styles": styles + ([s["direction"]] if s.get("direction") else []),
                       "negative_styles": neg})
    return {"chunks": chunks}


def post(path, body):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("没读到 ELEVENLABS_API_KEY。先执行 source ~/.zshrc，或新开一个终端窗口。")
    req = urllib.request.Request(API + path, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return r.headers, r.read()
        except urllib.error.HTTPError as err:
            raw = err.read().decode("utf-8", "replace")[:800]
            if err.code in (409, 429) and attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            hint = {401: "key 无效", 402: "额度不够或档位不支持", 403: "key 没开 Music Generation 权限"}.get(err.code, "")
            sys.exit(f"ElevenLabs 返回 {err.code}：{raw}\n{('→ ' + hint) if hint else ''}")
        except urllib.error.URLError as err:
            if isinstance(err.reason, ssl.SSLError):
                sys.exit("证书校验失败：双击运行 /Applications/Python 3.x/Install Certificates.command 后再试。")
            if attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            sys.exit(f"连不上 ElevenLabs：{err.reason}")


def split_multipart(headers, data):
    """/v1/music/detailed 返回 multipart/mixed：一段 JSON 元数据 + 一段音频。"""
    ctype = headers.get("Content-Type", "")
    if "multipart" not in ctype:
        return None, data
    msg = email.message_from_bytes(f"Content-Type: {ctype}\r\n\r\n".encode() + data)
    meta, audio = None, None
    for part in msg.walk():
        if part.is_multipart():
            continue
        body = part.get_payload(decode=True)
        if "json" in part.get_content_type():
            meta = json.loads(body)
        elif body:
            audio = body
    return meta, audio


def find_words(obj):
    """时间戳字段名文档没写死：在元数据里找"一串带文字和起止时间的对象"，统一成 [{w, s, e}]（秒）。"""
    best = []

    def walk(x):
        nonlocal best
        if isinstance(x, list) and x and all(isinstance(i, dict) for i in x):
            keys = set(x[0])
            tk = next((k for k in ("word", "text", "w") if k in keys), None)
            sk = next((k for k in ("start_ms", "start", "start_time", "s", "start_s") if k in keys), None)
            ek = next((k for k in ("end_ms", "end", "end_time", "e", "end_s") if k in keys), None)
            if tk and sk and ek and len(x) > len(best):
                ms = sk.endswith("_ms") or max(float(i[ek]) for i in x) > 1000
                best = [{"w": str(i[tk]).strip(), "s": float(i[sk]) / (1000 if ms else 1),
                         "e": float(i[ek]) / (1000 if ms else 1)} for i in x if str(i[tk]).strip()]
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(obj)
    # 作曲计划里 {…} 写的演唱提示也会混进时间戳（起止相同、不出声），去掉
    out, inside = [], False
    for w in best:
        if w["w"].startswith("{"):
            inside = True
        if not inside and w["e"] > w["s"]:
            out.append(w)
        if w["w"].endswith("}"):
            inside = False
    return out


def song_dir(ep):
    return os.path.join(ROOT, "out", os.path.basename(os.path.abspath(ep)).split("-")[0], "song")


def generate(ep, story, n, model):
    out = song_dir(ep)
    os.makedirs(out, exist_ok=True)
    have = [int(re.findall(r"\d+", os.path.basename(p))[0]) for p in glob.glob(os.path.join(out, "v*.mp3"))]
    body = {"composition_plan": plan(story, model), "model_id": model, "with_timestamps": True}
    total = sum(s["seconds"] for s in story["song"]["sections"])
    for k in range(max(have, default=0) + 1, max(have, default=0) + 1 + n):
        t = time.time()
        print(f"  生成第 {k} 版（{total:g} 秒，{model}）……", flush=True)
        headers, data = post("/v1/music/detailed?output_format=mp3_44100_192", dict(body, seed=k * 7919))
        meta, audio = split_multipart(headers, data)
        if not audio:
            sys.exit(f"返回里没有音频：{(meta or data[:300])}")
        open(os.path.join(out, f"v{k}.mp3"), "wb").write(audio)
        words = find_words(meta or {})
        json.dump({"song_id": headers.get("song-id"), "plan": body["composition_plan"], "words": words, "meta": meta},
                  open(os.path.join(out, f"v{k}.json"), "w"), ensure_ascii=False, indent=1)
        print(f"  ✓ v{k}.mp3  {time.time() - t:.0f}s，时间戳 {len(words)} 个词" +
              ("" if words else "（没拿到，--check 会用 Whisper 补）"))


def norm(s):
    return re.sub(r"[^a-z ]", "", s.lower().replace("-", " ")).split()   # Bye-bye 听写出来是 bye bye


def whisper_words(mp3):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    m = WhisperModel(os.environ.get("SONG_WHISPER", "small.en"), device="cpu", compute_type="int8")
    segs, _ = m.transcribe(mp3, word_timestamps=True, vad_filter=False, language="en")
    return [{"w": w.word.strip(), "s": w.start, "e": w.end} for s in segs for w in s.words]


def check(ep, story):
    """每一版：每段歌词的听写相似度、第一个词落在哪（离段落开头多远）、总时长。按平均相似度排序给推荐。"""
    out = song_dir(ep)
    secs = story["song"]["sections"]
    rows = []
    for mp3 in sorted(glob.glob(os.path.join(out, "v*.mp3")), key=lambda p: int(re.findall(r"\d+", os.path.basename(p))[0])):
        info_path = mp3[:-4] + ".json"
        info = json.load(open(info_path)) if os.path.exists(info_path) else {}
        heard = whisper_words(mp3)
        if heard is None:
            sys.exit("要先装 faster-whisper：.venv/bin/pip install faster-whisper")
        if info.get("meta"):               # 旧文件可能混着 {…} 提示词，重新清一遍
            info["words"] = find_words(info["meta"]) or info.get("words", [])
        if not info.get("words"):          # 接口没给时间戳，就用 Whisper 的词时间
            info["words"], info["words_from"] = heard, "whisper"
            json.dump(info, open(info_path, "w"), ensure_ascii=False, indent=1)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3],
                                   capture_output=True, text=True).stdout or 0)
        t0, sims, report = 0.0, [], []
        for s in secs:
            want = norm(" ".join(lyrics(story, s)))
            got = norm(" ".join(w["w"] for w in heard if t0 - 0.3 <= w["s"] < t0 + s["seconds"] - 0.2))
            if want:
                sim = difflib.SequenceMatcher(None, want, got).ratio()
                sims.append(sim)
                first = next((w["s"] for w in info["words"] if w["s"] >= t0 - 0.3), None)
                lag = f"{first - t0:+.2f}s" if first is not None else "—"
                report.append(f"    {s['name']:<8} 相似度 {sim:.2f}  开口 {lag}  听到：{' '.join(got)[:60]}")
            t0 += s["seconds"]
        avg = sum(sims) / max(len(sims), 1)
        rows.append((avg, os.path.basename(mp3), dur, report))
    for avg, name, dur, report in rows:
        print(f"{name}：平均相似度 {avg:.2f}，时长 {dur:.1f}s（计划 {t0:g}s）")
        print("\n".join(report))
    if rows:
        best = max(rows)
        print(f"推荐：{best[1]}（相似度最高）。合格线：每段 ≥0.6、平均 ≥0.75、时长差 ≤1 秒；还要自己听一遍。")


def pick(ep, story_path, story, k):
    out = song_dir(ep)
    src = os.path.join(out, f"v{k}.mp3")
    if not os.path.exists(src):
        sys.exit(f"没有 {src}")
    shutil.copy(src, os.path.join(out, "song.mp3"))
    info = json.load(open(os.path.join(out, f"v{k}.json")))
    json.dump(info.get("words", []), open(os.path.join(out, "song_words.json"), "w"), ensure_ascii=False, indent=1)
    rel = os.path.relpath(out, os.path.abspath(ep))
    story["song"].update({"file": f"{rel}/song.mp3", "words": f"{rel}/song_words.json", "picked": f"v{k}"})
    json.dump(story, open(story_path, "w"), ensure_ascii=False, indent=2)
    print(f"选了 v{k}：{len(info.get('words', []))} 个词的时间戳；story.json 已指向 {rel}/song.mp3")


def main():
    ap = argparse.ArgumentParser(description="儿歌：ElevenLabs Music 生成 + 时间戳")
    ap.add_argument("episode")
    ap.add_argument("--variants", type=int, help="这次出几版（默认 story.json 的 song.variants，或 3）")
    ap.add_argument("--model", help="默认 story.json 的 song.model，或 music_v2_5")
    ap.add_argument("--check", action="store_true", help="听写质检，给推荐")
    ap.add_argument("--pick", type=int, help="选定第几版")
    a = ap.parse_args()
    story_path = os.path.join(a.episode, "story.json")
    story = json.load(open(story_path, encoding="utf-8"))
    if "song" not in story:
        sys.exit("story.json 里没有 song 段")
    if a.pick:
        return pick(a.episode, story_path, story, a.pick)
    if a.check:
        return check(a.episode, story)
    generate(a.episode, story, a.variants or story["song"].get("variants", 3),
             a.model or story["song"].get("model", "music_v2_5"))


if __name__ == "__main__":
    main()
