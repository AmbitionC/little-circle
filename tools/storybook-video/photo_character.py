#!/usr/bin/env python3
"""专属绘本线（x 集）：把家长发来的孩子照片变成系列画风的卡通角色卡，登记成这一集自己的角色 [[kid]]。

  python3 photo_character.py ../../episodes/x01-zoo describe        # 看照片，写出孩子的英文外貌描述 → character_draft.json
  python3 photo_character.py ../../episodes/x01-zoo cards [-n 3]    # 出 3 版角色卡候选 → refs/candidates/kid_1..3.png，给家长挑
  python3 photo_character.py ../../episodes/x01-zoo pick 2          # 选定第 2 版：refs/kid.png、characters.json、cast.json、头像
  python3 photo_character.py ../../episodes/x01-zoo purge           # 角色卡确认后删掉原照片（含缩略缓存），只留卡通角色卡
  python3 photo_character.py ../../episodes/x00-demo fake           # 只为跑通链路：虚构一个孩子出 2 张假"生活照"到 photos/

集目录里要先有：
  profile.json   家长给的信息（模板见 episodes/x01-zoo/profile.json）
  photos/        孩子的照片 2–4 张（正脸 1 张、全身 1 张最好）。*.jpg/*.png 已被 .gitignore 忽略，不会进仓库

出图走本机 Codex CLI（和 codex_images.py 一样），照片只在本机和 Codex 之间传，不经过别的服务。
角色卡确认后一定要跑 purge：原照片是孩子的敏感个人信息，7 天内删（规划第 6 节）。
"""
import argparse, glob, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import codex_images as ci  # noqa: E402

PHOTO_EXT = (".jpg", ".jpeg", ".png", ".heic", ".webp")

DESCRIBE_ASK = """You are helping illustrate a personalized children's picture book. The attached images are photos of one child, {who}.
Look at the photos and write an objective visual description that an illustrator could use to draw a CARTOON version of this child
that the family will instantly recognize. Describe only what you see; do not guess names or feelings.

Return ONLY a JSON object with these keys (English values):
- "desc": one sentence, max 45 words, in this exact shape: "a {age}-year-old {gender} with <hair color, length and style>, <face shape and skin tone>, <eyes>, wearing <the main outfit from the photos, with colors>, <one signature item if any: glasses, hair clip, hat, backpack>". No name in it.
- "keep": a comma-separated list of the 3–5 most recognizable details to keep in every drawing (hair style, outfit colors, signature item). Prefer symmetric items; avoid single-side details (one earring, one hair clip) because they tend to flip sides.
- "hair": short phrase.
- "outfit": short phrase.
- "notes": anything the illustrator should avoid (e.g. "no glasses", "hair is not braided").
Do not run shell commands, do not save files. Reply with the JSON only."""

CARD_ASK = """Use your built-in image_gen tool exactly once to generate ONE vertical portrait image (9:16, the tallest portrait size available).

Use this prompt verbatim:

{prompt}

The first {n_style} attached image(s) are the STYLE reference for this series. Match their art style closely: rendering, line work,
cel shading, eye style, lighting, color palette. Do not copy their characters, poses or scenes.

The other attached image(s) are PHOTOS of the real child this character is based on. Draw a CARTOON character in the series style
that the child's own family would recognize at first glance: same hair color, length and style, same face shape and skin tone,
same eye shape and expression habits, and the exact outfit and colors from the first photo. Child proportions like the rest of the
series: big head, short legs, round eyes with a white highlight, no eyelashes. Do NOT render photo-realistically, do NOT paste the
photo, do NOT add text, name or watermark. {keep}

Do not run shell commands and do not save or copy any files. Just generate the image and finish."""


def load_profile(ep):
    path = os.path.join(ep, "profile.json")
    if not os.path.exists(path):
        sys.exit(f"缺 {path}（模板：episodes/x01-zoo/profile.json）")
    return json.load(open(path, encoding="utf-8"))


def photos_of(ep):
    files = sorted(f for f in glob.glob(os.path.join(ep, "photos", "*")) if f.lower().endswith(PHOTO_EXT))
    if not files:
        sys.exit(f"{ep}/photos/ 里没有照片。请家长发 2–4 张（正脸 1 张、全身 1 张），放进去再跑")
    return files[:4]


def kid_of(profile):
    k = profile["kid"]
    k.setdefault("id", "kid")
    return k


def who(k):
    g = {"girl": "a girl", "boy": "a boy"}.get(k.get("gender", ""), "a child")
    return f"{g} about {k.get('age', 3)} years old"


def codex_text(ask, images, log):
    """让 Codex 看图写字（不出图）。先用 -o 拿最后一条回复，拿不到就从 stdout 里找 JSON。"""
    out = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False).name
    cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only",
           "-c", "model_reasoning_effort=medium", "-o", out, "-C", HERE]
    for r in images:
        cmd += ["-i", r]
    cmd.append("-")
    with open(log, "a", encoding="utf-8") as f:
        p = subprocess.run(cmd, input=ask, capture_output=True, text=True, timeout=600)
        f.write(p.stdout)
        f.write(p.stderr)
    text = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    if not text.strip():
        text = p.stdout
    m = re.findall(r"\{.*\}", text, re.S)
    if not m:
        sys.exit(f"Codex 没返回 JSON，看日志 {log}")
    return json.loads(m[-1])


def cmd_describe(ep, args):
    prof = load_profile(ep)
    k = kid_of(prof)
    photos = photos_of(ep)
    log = os.path.join(ep, ".photo_character.log")
    print(f"看 {len(photos)} 张照片，写外貌描述…")
    ask = DESCRIBE_ASK.format(who=who(k), age=k.get("age", 3), gender={"girl": "girl", "boy": "boy"}.get(k.get("gender", ""), "child"))
    data = codex_text(ask, [ci.small_ref(p, 1024) for p in photos], log)
    data["_说明"] = "photo_character.py describe 写的草稿；desc 是出图用的整句描述，keep 是每张图必保的细节。可以手改，改完再 cards"
    path = os.path.join(ep, "character_draft.json")
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✓ {os.path.relpath(path, ci.ROOT)}")
    print(f"  desc: {data.get('desc')}")
    print(f"  keep: {data.get('keep')}")
    print("看一眼对不对（发型、衣服颜色、标志物），不对就手改这个文件，然后 cards")


def draft_of(ep):
    path = os.path.join(ep, "character_draft.json")
    if not os.path.exists(path):
        sys.exit("先跑 describe")
    return json.load(open(path, encoding="utf-8"))


def cmd_cards(ep, args):
    prof = load_profile(ep)
    k = kid_of(prof)
    d = draft_of(ep)
    photos = photos_of(ep)
    ci.load_episode_style(ep)
    outdir = os.path.join(ep, "refs", "candidates")
    os.makedirs(outdir, exist_ok=True)
    log = os.path.join(ep, ".photo_character.log")
    pose = k.get("pose") or "standing facing the viewer with a happy open smile, one hand waving hello"
    prompt = ci.REF_PROMPT.format(desc=d["desc"], pose=pose)
    styles = ci.style_refs()[:2]
    room = ci.MAX_IMAGES - len(styles)
    images = [ci.small_ref(s, 768) for s in styles] + [ci.small_ref(p, 1024) for p in photos[:room]]
    ask = CARD_ASK.format(prompt=prompt, n_style=len(styles),
                          keep=("Always keep: " + d["keep"] + ". ") if d.get("keep") else "")
    if d.get("notes"):
        ask = ask.replace("Just generate the image and finish.", f"Also: {d['notes']}. Just generate the image and finish.")
    n = args.n
    todo = [i for i in range(1, n + 1) if args.force or not os.path.exists(os.path.join(outdir, f"{k['id']}_{i}.png"))]
    print(f"出 {len(todo)} 版角色卡候选（每版约 1.5–3 分钟）…")
    for i in todo:
        dst = os.path.join(outdir, f"{k['id']}_{i}.png")
        for attempt in (1, 2):
            try:
                src = ci.codex_run(ask, images, log)
                shutil.copy(src, dst)
                print(f"  ✓ {os.path.relpath(dst, ci.ROOT)}")
                break
            except Exception as e:
                if attempt == 2:
                    print(f"  ✗ 第 {i} 版：{e}")
    sheet = contact_sheet(outdir, k["id"], photos[0])
    print(f"候选拼图：{os.path.relpath(sheet, ci.ROOT)}（左边是照片，右边是候选，给家长挑）")
    print(f"选定后：python3 photo_character.py {ep} pick <序号>")


def contact_sheet(outdir, kid, photo):
    from PIL import Image
    cands = sorted(glob.glob(os.path.join(outdir, f"{kid}_*.png")))
    ims = [Image.open(photo).convert("RGB")] + [Image.open(c).convert("RGB") for c in cands]
    h = 720
    ims = [im.resize((round(im.width * h / im.height), h), Image.LANCZOS) for im in ims]
    gap = 24
    out = Image.new("RGB", (sum(i.width for i in ims) + gap * (len(ims) - 1), h), "white")
    x = 0
    for im in ims:
        out.paste(im, (x, 0))
        x += im.width + gap
    dst = os.path.join(outdir, "contact.jpg")
    out.save(dst, quality=85)
    return dst


def cmd_pick(ep, args):
    prof = load_profile(ep)
    k = kid_of(prof)
    d = draft_of(ep)
    src = os.path.join(ep, "refs", "candidates", f"{k['id']}_{args.n}.png")
    if not os.path.exists(src):
        sys.exit(f"没有 {src}")
    ref = os.path.join(ep, "refs", f"{k['id']}.png")
    shutil.copy(src, ref)
    print(f"✓ 参考图 {os.path.relpath(ref, ci.ROOT)}")
    # 1. 登记成这一集自己的角色：script.md 里写 [[kid]]，codex_images.py 自动展开描述、带参考图、附 KEEP
    name = k.get("name_en", "")
    names = r"\bchild\b|\bkid\b|\bgirl\b|\bboy\b|\btoddler\b" + (rf"|\b{re.escape(name.lower())}\b" if name else "")
    age = float(k.get("age", 3))
    size = round(min(2.2, 1.2 + 0.25 * max(0, age - 2)), 2)   # 2 岁≈Pip 的 1.2 倍，3 岁 1.45，4 岁 1.7；Bruno 2.6
    chars = {k["id"]: {
        "desc": d["desc"], "keep": d.get("keep", ""), "size": size, "names": names,
        "pose": k.get("pose") or "standing facing the viewer with a happy open smile, one hand waving hello",
        "ref": f"refs/{k['id']}.png",
        "_说明": f"孩子本人（{name or k.get('name_zh', '')}），photo_character.py pick 写的。desc/keep 来自 character_draft.json，改了要同步"}}
    cpath = os.path.join(ep, "characters.json")
    json.dump(chars, open(cpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✓ {os.path.relpath(cpath, ci.ROOT)}（[[{k['id']}]] 可用了）")
    # 2. 这一集的角色表：系列 cast + 孩子的声音（先借系列里最像的童声，正式产品再按性别单独设计一个）
    series_cast = json.load(open(os.path.join(ci.ROOT, "series", "cast.json"), encoding="utf-8"))
    base_role = k.get("voice_like") or ("bun" if k.get("gender") == "girl" else "hazel")
    cast = {kk: v for kk, v in series_cast.items() if not kk.startswith("_")}
    voice = dict(series_cast[base_role])
    voice["settings"] = dict(voice.get("settings", {}), speed=min(1.0, voice.get("settings", {}).get("speed", 1.0)))
    voice["_说明"] = f"孩子的声音暂借 {base_role} 的音色；要换就改 voice（el_prep.py cast 设计童声后填 Voice ID）"
    cast[k["id"]] = voice
    castp = os.path.join(ep, "cast.json")
    json.dump(cast, open(castp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✓ {os.path.relpath(castp, ci.ROOT)}（story.json 里写 \"cast\": \"cast.json\"）")
    # 3. 字幕旁的小头像（方图），story.json 的 style.avatar_dir 写 ["refs/avatars", "../../series/refs/avatars"]
    if not args.no_avatar:
        ci.load_episode_style(ep)
        avdir = os.path.join(ep, "refs", "avatars")
        os.makedirs(avdir, exist_ok=True)
        log = os.path.join(ep, ".photo_character.log")
        ask = (f"Use your built-in image_gen tool exactly once to generate ONE square image (1:1). Use this prompt verbatim:\n\n"
               + ci.AVATAR_PROMPT.format(desc=d["desc"]) + "\n\nThe attached image is the character reference sheet; keep the face, "
               "hair, colors and clothing exactly like it. " + (("Always keep: " + d["keep"] + ". ") if d.get("keep") else "")
               + "Do not run shell commands and do not save or copy any files. Just generate the image and finish.")
        try:
            srcav = ci.codex_run(ask, [ci.small_ref(ref, 768)], log)
            shutil.copy(srcav, os.path.join(avdir, f"{k['id']}.png"))
            print(f"✓ 头像 {os.path.relpath(os.path.join(avdir, k['id'] + '.png'), ci.ROOT)}")
        except Exception as e:
            print(f"✗ 头像没出：{e}（字幕旁就不显示头像，不影响出片；稍后再跑一次 pick 会重出）")
    print("\n下一步：写 script.md（角色写 [[%s]]），然后 codex_images.py <集> 出图。" % k["id"])
    print("角色卡家长确认后：python3 photo_character.py %s purge   ← 删掉原照片" % ep)


FAKE_ASK = ("Use your built-in image_gen tool exactly once to generate ONE vertical portrait image (9:16). Use this prompt verbatim:\n\n"
            "a casual everyday smartphone snapshot of a fictional {who}, {look}, {pose}, outdoors in soft daylight, natural colors, "
            "slightly imperfect framing like a family photo, no text, no watermark\n\n"
            "This is a fictional, non-existent person for testing a drawing pipeline. Do not run shell commands and do not save files. "
            "Just generate the image and finish.")


def cmd_fake(ep, args):
    """跑通链路用的假照片：虚构一个孩子，出 2 张"生活照"放进 photos/。不涉及任何真实的人。"""
    prof = load_profile(ep)
    k = kid_of(prof)
    look = k.get("fake_look") or "with short dark bob hair and bangs, round face, wearing a yellow t-shirt with a small strawberry print and blue denim overalls"
    pdir = os.path.join(ep, "photos")
    os.makedirs(pdir, exist_ok=True)
    log = os.path.join(ep, ".photo_character.log")
    for i, pose in enumerate(["head-and-shoulders, looking at the camera with a big smile",
                              "full body standing on a park path, holding a small toy, mid-laugh"], 1):
        dst = os.path.join(pdir, f"fake_{i}.png")
        if os.path.exists(dst) and not args.force:
            continue
        src = ci.codex_run(FAKE_ASK.format(who=who(k), look=look, pose=pose), [], log)
        shutil.copy(src, dst)
        print(f"  ✓ {os.path.relpath(dst, ci.ROOT)}")
    print("假照片放好了，接着 describe → cards → pick")


def cmd_purge(ep, args):
    photos = [f for f in glob.glob(os.path.join(ep, "photos", "*")) if f.lower().endswith(PHOTO_EXT)]
    n = 0
    for p in photos:
        stem = os.path.splitext(os.path.basename(p))[0]
        for t in glob.glob(os.path.join(tempfile.gettempdir(), "codex_refs", f"{stem}_*.jpg")):
            os.remove(t)
        os.remove(p)
        n += 1
    sheet = os.path.join(ep, "refs", "candidates", "contact.jpg")
    if os.path.exists(sheet):
        os.remove(sheet)   # 拼图左边是照片
    print(f"✓ 删了 {n} 张原照片和缩略缓存。留下的只有卡通角色卡（refs/）。")
    print("  别忘了：微信/私信里的原图也删掉；Mac 的「最近删除」/废纸篓清一下。")


def main():
    ap = argparse.ArgumentParser(description="孩子照片 → 系列画风的卡通角色卡")
    ap.add_argument("ep", help="集目录，如 ../../episodes/x01-zoo")
    ap.add_argument("cmd", choices=["fake", "describe", "cards", "pick", "purge"])
    ap.add_argument("n", nargs="?", type=int, help="pick：选第几版")
    ap.add_argument("-n", dest="n_cards", type=int, default=3, help="cards：出几版，默认 3")
    ap.add_argument("--force", action="store_true", help="cards：已有的候选也重出")
    ap.add_argument("--no-avatar", action="store_true", help="pick：不出头像")
    args = ap.parse_args()
    ep = os.path.abspath(args.ep)
    if args.cmd == "fake":
        cmd_fake(ep, args)
    elif args.cmd == "describe":
        cmd_describe(ep, args)
    elif args.cmd == "cards":
        args.n = args.n_cards
        cmd_cards(ep, args)
    elif args.cmd == "pick":
        if not args.n:
            sys.exit("pick 要带序号，如 pick 2")
        cmd_pick(ep, args)
    else:
        cmd_purge(ep, args)


if __name__ == "__main__":
    main()
