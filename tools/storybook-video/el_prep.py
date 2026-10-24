#!/usr/bin/env python3
"""ElevenLabs 一次性准备：选角候选音色、保存选中的音色、音效库、背景音乐。

只用标准库，macOS 自带的 python3 就能跑。key 从环境变量 ELEVENLABS_API_KEY 读取。

    python3 el_prep.py cast                  # 四个角色各生成 3 个候选，存到 out/casting/
    python3 el_prep.py cast nutty            # 只给 Nutty 再出 3 个（编号接着往后排）
    python3 el_prep.py pick narrator=2 nutty=1 hazel=3 bun=2
                                             # 保存选中的候选，Voice ID 自动写进 series/cast.json
    python3 el_prep.py pick narrator=<VoiceID>  # 也可以直接填网页上现成音色的 ID
    python3 el_prep.py sfx                   # 生成 14 个音效到 assets/sfx/（已存在的跳过）
    python3 el_prep.py bgm                   # 生成 3 首背景音乐到 assets/bgm/
    python3 el_prep.py all                   # cast + sfx + bgm
    加 --force 覆盖已有文件（订阅付费档后重新生成可商用版本时用）
"""
import base64
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
API = os.environ.get("ELEVENLABS_API_BASE", "https://api.elevenlabs.io").rstrip("/")
CAST_JSON = os.path.join(ROOT, "series", "cast.json")
CASTING_DIR = os.path.join(ROOT, "out", "casting")
SFX_DIR = os.path.join(ROOT, "assets", "sfx")
BGM_DIR = os.path.join(ROOT, "assets", "bgm")

# 选角说明：描述与 docs/elevenlabs-workflow.md 1.2 节一致；试音文本接口要求 100–1000 字符
ROLES = {
    "narrator": {
        "name": "Lili Narrator",
        "description": "A warm, gentle female storyteller with a soft American accent, speaking slowly "
                       "and clearly to a three-year-old at bedtime, smiling, calm and cozy.",
        "text": "Once upon a time, in a cozy little forest, Nutty the squirrel finds a big, big acorn. "
                "Can he open it? Let's count together: one, two, three. Good night, little one.",
    },
    "nutty": {
        "name": "Lili Nutty",
        "description": "A cheerful, high-pitched cartoon squirrel character, playful and bouncy, curious "
                       "and excited, very clear American English, like the sidekick in an animated "
                       "preschool show.",
        "text": "Wow! Look at this big, big acorn! It's mine! Hi, I'm Nutty! I love acorns, I love "
                "jumping, and I love my friends. Ready? Let's go, go, go!",
    },
    "hazel": {
        "name": "Lili Hazel",
        "description": "A sweet, gentle, slightly shy cartoon hedgehog girl, soft and warm, high-pitched, "
                       "kind and polite, clear American English.",
        "text": "Hello, I'm Hazel. I am so hungry. Can I have some, please? Thank you, Nutty! "
                "You are so kind. Let's share it together, okay?",
    },
    "bun": {
        "name": "Lili Bun",
        "description": "A soft, cuddly cartoon bunny boy, a little slow and shy, round gentle tone, "
                       "clear pronunciation.",
        "text": "Hi, I'm Bun. One, two, three! I have an orange carrot! Crunch, crunch. Yummy! "
                "Do you want one too? Here you go, my friend.",
    },
}

# 音效库：文件名 → (描述, 时长秒)；与 docs/elevenlabs-workflow.md 1.3 节一致
SFX = {
    "pop":        ("cute cartoon pop, short and bright", 0.6),
    "bonk":       ("soft cartoon wooden bonk on the head, funny, not painful", 0.8),
    "crack":      ("a nut shell cracking open, crisp, cartoon style", 1.0),
    "whoosh":     ("gentle soft whoosh transition", 1.2),
    "sparkle":    ("magical twinkling sparkle chime", 1.5),
    "ding":       ("single bright bell ding, idea moment", 1.0),
    "boing":      ("springy cartoon boing", 1.0),
    "chomp":      ("cute cartoon chomp and munch", 1.5),
    "tummy":      ("funny little tummy rumble, cartoon", 1.5),
    "snore":      ("tiny cute cartoon snore", 2.5),
    "leaves":     ("footsteps rustling through autumn leaves", 2.5),
    "page":       ("soft storybook page turn", 1.0),
    "jingle_in":  ("music box jingle C5 E5 G5 C6, cheerful, 2 seconds", 2.0),
    "jingle_out": ("music box jingle C6 G5 E5 C5, gentle ending, 2 seconds", 2.0),
}

# 背景音乐：与 docs/elevenlabs-workflow.md 1.4 节一致
BGM = {
    "bgm_play":  "playful music box and pizzicato strings, 90 BPM, C major, light and bouncy, "
                 "preschool cartoon, instrumental, no vocals, seamless loop",
    "bgm_calm":  "soft music box lullaby, sparse, slow, warm and cozy bedtime, "
                 "instrumental, no vocals, seamless loop",
    "bgm_happy": "happy glockenspiel and ukulele with light shakers, celebration, 90 BPM, "
                 "instrumental, no vocals, seamless loop",
}
BGM_MS = 60000


def api(path, body, want_json=True, retries=3):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("没读到 ELEVENLABS_API_KEY。先执行 source ~/.zshrc，或新开一个终端窗口。")
    req = urllib.request.Request(API + path, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
            return json.loads(data) if want_json else data
        except urllib.error.HTTPError as err:
            raw = err.read().decode("utf-8", "replace")
            if err.code in (409, 429) and attempt < retries:
                time.sleep(5 * (attempt + 1))
                continue
            raise ApiError(err.code, raw)
        except urllib.error.URLError as err:
            if isinstance(err.reason, ssl.SSLError):
                sys.exit("证书校验失败。如果 python3 是从 python.org 装的，双击运行 "
                         "/Applications/Python 3.x/Install Certificates.command 后再试。")
            if attempt < retries:
                time.sleep(3 * (attempt + 1))
                continue
            sys.exit(f"连不上 ElevenLabs：{err.reason}")


class ApiError(Exception):
    def __init__(self, code, raw):
        self.code, self.raw = code, raw
        try:
            detail = json.loads(raw).get("detail", raw)
        except ValueError:
            detail = raw
        if isinstance(detail, dict):
            self.status = detail.get("status", "")
            self.message = detail.get("message", raw)
        else:
            self.status, self.message = "", json.dumps(detail, ensure_ascii=False)[:500]
        super().__init__(f"HTTP {code} {self.status}: {self.message}")

    def hint(self):
        m = re.search(r"missing the permission (\w+)", self.message)
        if m or self.status == "missing_permissions":
            perm = m.group(1) if m else "（见上面的报错）"
            return f"key 缺少权限 {perm}：到 API Keys 里给这个 key 打开对应权限（或新建一个 key 替换 ~/.zshrc 里那行）。"
        if self.status in ("feature_unavailable", "limited_access") or "paid plan" in self.message:
            return "免费档不能通过接口用这个功能，订阅 Starter 后再跑。"
        if self.code == 401:
            return "key 无效：检查 ~/.zshrc 里那行是否完整，然后 source ~/.zshrc。"
        if self.code == 402 or self.status in ("quota_exceeded", "payment_required"):
            return "额度不够，或者当前档位不支持这个功能。"
        return ""


def report(what, err):
    print(f"  ✗ {what}：{err}")
    if err.hint():
        print(f"    → {err.hint()}")


def load_previews():
    path = os.path.join(CASTING_DIR, "previews.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_previews(data):
    with open(os.path.join(CASTING_DIR, "previews.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cmd_cast(roles):
    os.makedirs(CASTING_DIR, exist_ok=True)
    data = load_previews()
    for role in roles or ROLES:
        brief = ROLES[role]
        assert 100 <= len(brief["text"]) <= 1000, f"{role} 的试音文本需 100–1000 字符"
        print(f"· {role}：生成候选音色…")
        try:
            res = api("/v1/text-to-voice/design",
                      {"voice_description": brief["description"], "text": brief["text"]})
        except ApiError as err:
            report(role, err)
            if err.code in (401, 402, 403):
                break
            continue
        items = data.setdefault(role, [])
        for p in res.get("previews", []):
            n = len(items) + 1
            fname = f"{role}-{n}.mp3"
            with open(os.path.join(CASTING_DIR, fname), "wb") as f:
                f.write(base64.b64decode(p["audio_base_64"]))
            items.append({"n": n, "generated_voice_id": p["generated_voice_id"], "file": fname})
            print(f"  ✓ out/casting/{fname}")
        save_previews(data)
    if not data:
        return
    print(f"\n试听：open {os.path.relpath(CASTING_DIR)}  （Finder 里选中文件按空格）")
    print("选好后：python3 tools/storybook-video/el_prep.py pick narrator=2 nutty=1 hazel=3 bun=2")


def set_cast_voice(role, voice_id):
    with open(CAST_JSON, encoding="utf-8") as f:
        text = f.read()
    pat = re.compile(r'("%s"\s*:\s*\{[^{}]*?"voice"\s*:\s*)"[^"]*"' % re.escape(role))
    new, count = pat.subn(lambda m: m.group(1) + json.dumps(voice_id), text, count=1)
    if not count:  # 排版不认识时退回整份重写
        data = json.loads(text)
        data[role]["voice"] = voice_id
        new = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with open(CAST_JSON, "w", encoding="utf-8") as f:
        f.write(new)


def cmd_pick(args):
    data = load_previews()
    for arg in args:
        role, _, choice = arg.partition("=")
        if role not in ROLES or not choice:
            sys.exit(f"看不懂 {arg!r}，写成 角色=编号，例如 nutty=2；角色只能是 {', '.join(ROLES)}")
        if choice.isdigit():
            hit = [p for p in data.get(role, []) if p["n"] == int(choice)]
            if not hit:
                sys.exit(f"out/casting/ 里没有 {role}-{choice}.mp3，先跑 cast")
            print(f"· 保存 {role}-{choice}…")
            try:
                res = api("/v1/text-to-voice", {
                    "voice_name": ROLES[role]["name"],
                    "voice_description": ROLES[role]["description"],
                    "generated_voice_id": hit[0]["generated_voice_id"],
                    "labels": {"series": "lili", "role": role},
                    "played_not_selected_voice_ids": [p["generated_voice_id"] for p in data[role]
                                                      if p["n"] != int(choice)],
                })
            except ApiError as err:
                report(role, err)
                continue
            voice_id = res["voice_id"]
        else:
            voice_id = choice  # 网页上现成音色的 Voice ID
        set_cast_voice(role, voice_id)
        print(f"  ✓ {role} → {voice_id}（已写入 series/cast.json）")


def cmd_sfx(names, force):
    os.makedirs(SFX_DIR, exist_ok=True)
    for name in names or SFX:
        prompt, secs = SFX[name]
        out = os.path.join(SFX_DIR, name + ".mp3")
        if os.path.exists(out) and not force:
            print(f"  - 已有 assets/sfx/{name}.mp3，跳过")
            continue
        try:
            audio = api("/v1/sound-generation", {"text": prompt, "duration_seconds": secs,
                                                 "prompt_influence": 0.5}, want_json=False)
        except ApiError as err:
            report(name, err)
            if err.code in (401, 402, 403):
                break
            continue
        with open(out, "wb") as f:
            f.write(audio)
        print(f"  ✓ assets/sfx/{name}.mp3")


def cmd_bgm(names, force):
    os.makedirs(BGM_DIR, exist_ok=True)
    for name in names or BGM:
        out = os.path.join(BGM_DIR, name + ".mp3")
        if os.path.exists(out) and not force:
            print(f"  - 已有 assets/bgm/{name}.mp3，跳过")
            continue
        print(f"· {name}：生成中（每首约 1 分钟）…")
        try:
            audio = api("/v1/music", {"prompt": BGM[name], "music_length_ms": BGM_MS,
                                      "force_instrumental": True}, want_json=False)
        except ApiError as err:
            report(name, err)
            print("    → 生成不了的话，先用 make_bgm.py 的程序化八音盒顶上。")
            if err.code in (401, 402, 403):
                break
            continue
        with open(out, "wb") as f:
            f.write(audio)
        print(f"  ✓ assets/bgm/{name}.mp3")


def main(argv):
    force = "--force" in argv
    argv = [a for a in argv if a != "--force"]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, rest = argv[0], argv[1:]
    if cmd == "cast":
        bad = [r for r in rest if r not in ROLES]
        if bad:
            sys.exit(f"没有角色 {bad}，可选：{', '.join(ROLES)}")
        cmd_cast(rest)
    elif cmd == "pick":
        cmd_pick(rest)
    elif cmd == "sfx":
        cmd_sfx([n for n in rest if n in SFX] or None, force)
    elif cmd == "bgm":
        cmd_bgm([n for n in rest if n in BGM] or None, force)
    elif cmd == "all":
        print("== 1/3 选角候选 =="); cmd_cast([])
        print("\n== 2/3 音效库 =="); cmd_sfx(None, force)
        print("\n== 3/3 背景音乐 =="); cmd_bgm(None, force)
    else:
        sys.exit(f"不认识的命令 {cmd!r}，用 -h 看用法")


if __name__ == "__main__":
    main(sys.argv[1:])
