#!/usr/bin/env python3
"""用本机 Codex CLI（ChatGPT 登录，内置 image_gen）按 script.md 的出图提示词批量出图。

  python3 codex_images.py refs                         # 先出三个角色的参考图 → series/refs/
  python3 codex_images.py sheets                       # 角色设定图（正面+侧面+三表情）→ series/sheets/，给人看
  python3 codex_images.py styles                       # 画风对比：series/style_tests.json → out/style_test/
  python3 codex_images.py styles --styles-config style_tests_guofeng.json   # 国风特别版样图 → out/style_tests_guofeng/
  python3 codex_images.py ../../episodes/c01-fruits    # 出一集：p01–p06、kling_first、cover
  python3 codex_images.py ../../episodes/c0[1-3]-* -j 2  # 多集，两张并行
  python3 codex_images.py ../../episodes/s03-sleepy --comic   # 漫画剧本：每三格一张横版漫画，剧本确认前给用户看
  python3 codex_images.py ../../episodes/c18-peekaboo --comic-all   # 漫画剧本画全部格子（每个动作关键帧一格），看分镜够不够
  python3 codex_images.py ../../episodes/s05-xxx --check      # 只查角色写法，不出图

角色一致性：script.md 里写 [[pip]] 会展开成角色表里的整句英文描述，并自动带上 series/refs/pip.png；
每次出图还会把这个角色最容易画丢的细节（KEEP）和同框身高比例（SIZES）一起交代给 Codex。
出图前自动检查（提到角色却没用描述、用了旧描述、缺参考图），没过不出图；出完拼 qc/characters.jpg 对比参考图。

关键帧（做动画用，不花可灵灵感值）：script.md 里写 **p01b.png** ← p01.png，下面代码块只写"改哪里"。
脚本先出底图，再把底图当第一张参考图，让 Codex 只改动作、其余不动，出同一镜头的下一张画。

单集自己的角色（专属绘本线 x：孩子本人）：集目录里放 characters.json（photo_character.py pick 会写），
里面的角色和系列角色一样用 [[id]]，参考图从集目录 refs/<id>.png 取，不进 series/refs。

已有的图跳过；script.md 里某张图的提示词改了，会自动重出那一张。--force 全部重出，--only p02,p05 只出这几张。
图会裁成 1080×1920 存进集目录，原图路径和提示词指纹记在 images.json。
"""
import argparse, glob, hashlib, json, os, re, subprocess, sys, tempfile, threading, time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REFS = os.path.join(ROOT, "series", "refs")
CODEX_HOME = os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex"))
W, H = 1080, 1920

STYLE = ("Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, "
         "simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details, "
         "a limited harmonious palette, the characters brighter and sharper than the background, one clear focal point, no text, no watermark")
# 画风参考图（用户给的样张，只留在本机，不进仓库）：每张图都带上，锁住画风
STYLE_DIR = os.path.join(ROOT, "series", "style")
# 角色固定描述（和 Skill 5.2 节一字不差），出现在提示词里就带上对应参考图
CHARACTERS = {
    # 2026-10-30 角色升级：每句加了一个夸张部位（剪影钩子）；同日第二版加了「活人感」：衣服的来历、磨损和小瑕疵。六件套见 series/characters.md
    "nutty": "a small red squirrel with a huge fluffy tail even bigger than his whole body with a little twig stuck in it, round bright eyes and a tiny gap between his two front teeth, wearing a too-long hand-knitted green scarf with one unraveling end and a loose thread, and a small patched cloth nut pouch on a strap with a hole at the bottom",
    "hazel": "a round ball-shaped little hedgehog boy with a wide puffy crown of soft brown spines with one small red leaf stuck on them, rosy cheeks, wearing slightly too-big tiny yellow overalls with one strap slipping off his shoulder and a round blue patch on one knee",
    "bun": "a nimble little light-gray bunny girl with child proportions like her friends, long narrow upright rabbit ears tapered to a soft point, about as long as her head, bright clever eyes with a lively sparkle, a white fluffy cotton-tail, wearing a small red vest with a little carrot-shaped badge and a tiny magnifying glass on a string around her neck",
    # 其他森林伙伴（性格见 series/characters.md）；refs 只出用到的：codex_images.py refs --only pip,bruno
    "pip": "a tiny gray mouse with huge round pink ears even bigger than his head, a small nibbled notch in his left ear, a pink nose and one long thin unbroken pink tail growing from behind his bottom, wearing a hand-me-down blue-and-white striped shirt too big for him with the sleeves rolled up",
    "bruno": "a big chubby brown bear cub, twice as tall as his friends, with broad square shoulders, a round soft tummy, small round ears and a little red bee-sting bump on the tip of his nose, wearing a little orange neckerchief with sticky golden honey drip stains",
    "fern": "a cute little orange fox kit with soft rounded cartoon proportions like her friends, always standing upright on two legs, not a squirrel, with a pointed fox snout, tall smooth triangular fox ears, black stocking legs with a scuffed dusty patch on one knee and a long fluffy fox tail with a white tip held low, a slightly crinkled red maple leaf tucked behind one ear",
    "ruby": "a tiny ball-shaped fluffy baby robin with a puffed-up orange-red chest, a messy tuft of baby fluff sticking up on her head with a bit of nest straw caught in it, and stubby little wings too small to fly with one feather bent the wrong way",
    "ollie": "a small round brown owl with big amber eyes and tiny round glasses",
    "rocky": "a little raccoon with a black eye mask and a striped bushy tail, wearing tiny blue rubber gloves",
    "dot": "a gentle little fawn with very long thin wobbly legs, white spots on her back and big soft ears, wearing a small pink flower behind one ear",
    "bo": "a little badger with a black-and-white striped face, big digging claws and a smudge of dirt on his nose",
    "wiggles": "a little brown otter with a sleek shiny coat and long whiskers, hugging his favorite small round pebble to his chest",
}
# 升级前的旧描述：已出过图的旧集 script.md 里还是这几句，照样认得出、带上参考图
OLD_DESC = {
    "nutty": "a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf",
    "hazel": "a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls",
    "bun": ("a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest",
            # 10-30 版（一耳耷拉、半眯眼），11-01 用户嫌成人化换掉；旧集重出图仍认得
            "a fluffy light-gray bunny with very long ears, her left ear standing straight up tall and her right ear flopped down over her right eye, sleepy half-closed eyes and a messy tuft of bed-head fur sticking up between her ears, wearing a small red vest buttoned up wrong so it hangs crooked, hugging a worn little stuffed carrot toy",
            # 11-01 上午幼态版（用户嫌太幼、耳朵像老鼠）
            "a chubby little light-gray bunny girl with toddler proportions, a big round head and a short round body, two soft medium-length ears both standing straight up with pink insides, big round shiny baby eyes like her friends, rosy round cheeks and a messy tuft of bed-head fur sticking up between her ears, wearing a small red vest buttoned up wrong so it hangs crooked, hugging a worn little stuffed carrot toy"),
    "pip": "a tiny gray mouse with big round pink ears, a pink nose and a thin curly tail, wearing a little blue-and-white striped shirt",
    "bruno": "a big chubby brown bear cub with a round soft tummy and small round ears, wearing a little orange neckerchief",
    "ruby": "a tiny round fluffy baby robin with an orange-red chest and stubby little wings",
    "fern": "a slim young orange fox, not a squirrel, with a long pointed fox snout, tall smooth triangular fox ears, black stocking legs and a long fluffy fox tail with a white tip held low, a red maple leaf tucked behind one ear",
}
# 参考图不再全员"正面站好、张嘴笑"：每个角色用自己的招牌姿势和默认表情
POSES = {
    "nutty": "hugging a big shiny chestnut with an eager toothy grin, his huge tail puffed up high behind him",
    "hazel": "shyly opening his little arms for a hug, a small hopeful smile, his spines softly raised",
    "bun": "one paw raised with a finger up as if she just had a great idea, both ears perked straight up, a bright clever grin, light on her toes, "
           "standing with both feet on the ground, a small chubby five-year-old child body with a big head and short stubby legs, "
           "the same size and proportions as a little hedgehog friend, simple round dark eyes with a white highlight, no eyelashes",
    "pip": "clutching the end of his own long unbroken tail nervously with wide worried eyes, one huge ear turned to the side listening",
    "bruno": "proudly patting his round tummy with both paws, chin up, big confident grin",
    "fern": "striking a ta-da pose standing upright on both feet, one paw raised high, chin up, tail fluffed proudly, a cheeky showing-off smile",
    "ruby": "flapping her stubby wings hard with a determined face, her feet just barely off the ground",
    "ollie": "turning his head almost all the way around, one wing raised like a know-it-all",
    "rocky": "scrubbing a little apple with his gloved paws, very serious about getting it clean",
    "dot": "wobbling on her long thin legs, trying to keep her balance, a surprised little smile",
    "bo": "proudly holding up his big digging claws, a smudge of dirt on his nose",
    "wiggles": "hugging his favorite pebble tightly, a blissful happy face",
}
REF_PROMPT = ("character reference sheet of {desc}, one single full-body view, {pose}, "
              "plain warm cream paper background, nothing else in the picture, " + STYLE + ", vertical 9:16")
# 角色设定图：给人看的，不进出图流程（一张图里多个视图，当参考图会让 Codex 画出好几个同一角色）
SHEET_PROMPT = ("character model sheet of {desc}, laid out on one wide sheet with plain warm cream paper background: "
                "on the left a large full-body front view, then a small full-body side view, then three head close-ups "
                "with exactly three clearly different expressions: {faces}. Only these five views, each fully inside the picture, nothing cropped or repeated. The same character in every view, consistent colors "
                "and proportions. " + STYLE + ". Absolutely no text, no labels, no arrows")
FACES = {
    "nutty": "an eager toothy grin; a puzzled face scratching his head with his tail curled like a question mark; a happy 'yum' face with closed eyes",
    "hazel": "a shy hopeful smile; a startled face with all spines popped straight out; a blissful face being hugged",
    "bun": "a bright clever 'I have an idea!' grin with one finger raised; an eager confident smile mid-hop with ears streaming back; a focused knowing smile peering through her little magnifying glass with BOTH eyes wide open, the other eye not closed",
    "pip": "worried with his huge ears covering his face; listening with one ear turned; a proud brave smile",
    "bruno": "a big confident grin; terrified of a tiny bee near his nose; tearing up with joy holding a honey pot",
    "fern": "a cheeky ta-da wink; embarrassed after tripping with her tail hidden behind her; a big honest laugh",
    "ruby": "a determined frown while flapping; puffed up into an angry little red ball; a delighted 'I did it' smile",
}


def old_descs(k):
    """某角色所有旧描述（一个或多个）。"""
    o = OLD_DESC.get(k, ())
    return (o,) if isinstance(o, str) else tuple(o)


def char_ids(text):
    """提示词里点名了哪些角色（新旧描述都认）。"""
    return [k for k, d in CHARACTERS.items() if d in text or any(x in text for x in old_descs(k))]


# 单集自己的角色（characters.json）：id → 参考图绝对路径；没登记的角色都在 series/refs/
EP_REFS = {}


def ref_path(k):
    """角色 k 的参考图：单集角色在集目录里，系列角色在 series/refs/。"""
    return EP_REFS.get(k) or os.path.join(REFS, f"{k}.png")


def ref_by_name(basename):
    """images.json 里记的是参考图文件名；反查它现在在哪（单集角色的在集目录）。"""
    k = os.path.splitext(basename)[0]
    return EP_REFS.get(k) or os.path.join(REFS, basename)


def load_episode_characters(ep):
    """集目录里有 characters.json 就把这一集自己的角色并进角色表（专属绘本线：孩子本人，photo_character.py pick 生成）。
    每条：{"desc": 整句英文描述, "keep": 必保细节, "size": 身高（Pip=1）, "names": 名字/称呼的正则, "pose": 参考图姿势, "ref": 参考图相对集目录路径}。"""
    path = os.path.join(ep, "characters.json")
    if not os.path.exists(path):
        return
    data = json.load(open(path, encoding="utf-8"))
    for k, v in data.items():
        if k.startswith("_"):
            continue
        CHARACTERS[k] = v["desc"]
        if v.get("keep"):
            KEEP[k] = v["keep"]
        if v.get("size"):
            SIZES[k] = v["size"]
        if v.get("names"):
            NAMES[k] = v["names"]
        if v.get("pose"):
            POSES[k] = v["pose"]
        EP_REFS[k] = os.path.abspath(os.path.join(ep, v.get("ref", f"refs/{k}.png")))
    print(f"这一集自己的角色：{', '.join(k for k in data if not k.startswith('_'))}（参考图在集目录 refs/）")


def char_refs(text):
    if not EP_CHAR_REFS:
        return []
    return [ref_path(k) for k in char_ids(text) if os.path.exists(ref_path(k))]


# 角色一致性（2026-10-31 用户："这些形象怎么能集成到 skill，保证每次视频生成的一致性"）
# 每张图带上参考图之外，再把这几样逐条点给 Codex：最容易被画丢的标志细节、同框时的身高比例
KEEP = {
    "nutty": "huge tail bigger than his body with a little twig in it, tooth gap, too-long green scarf with an unraveling end, patched nut pouch with a hole",
    "hazel": "ball-shaped body, small red leaf stuck in his spines, yellow overalls with one strap slipped off the shoulder, round blue knee patch",
    "bun": "long narrow upright rabbit ears about as long as her head (NOT big round mouse ears), child proportions like Nutty and Hazel with short legs (not a baby, not a grown-up), bright clever eyes with no eyelashes and no winking, red vest with a carrot badge, tiny magnifying glass on a string, white cotton-tail",
    "pip": "ears bigger than his head with a notch in the left ear, ONE continuous unbroken tail (no bandage), oversized striped shirt with rolled sleeves",
    "bruno": "about twice as tall as the small friends, square shoulders, red bee-sting bump on his nose, honey stains on the orange neckerchief",
    "fern": "rounded cute proportions standing on two legs, crinkled red maple leaf behind one ear, black stocking legs with one dusty knee, white tail tip",
    "ruby": "tiny round ball body, messy head fluff with a bit of straw, orange-red chest, one bent wing feather, cannot fly",
}
# 体型阶梯：数字是大约多少个"小个子"高（Pip、Ruby 记 1）
SIZES = {"ruby": 1, "pip": 1, "nutty": 1.4, "hazel": 1.3, "bun": 1.35, "fern": 1.8, "bruno": 2.6}
# 剧本里可以只写 [[pip]]，出图前展开成整句英文描述（不用再手抄长句，也就不会抄错）
TOKEN = re.compile(r"\[\[(\w+)\]\]")
# 提示词里出现这些词却没带上对应描述，多半是角色写漏了，会画成路人动物
NAMES = {"nutty": r"\bnutty\b|squirrel", "hazel": r"\bhazel\b|hedgehog", "bun": r"\bbun\b|bunny|rabbit",
         "pip": r"\bpip\b|\bmouse\b", "bruno": r"\bbruno\b|\bbear\b", "fern": r"\bfern\b|\bfox\b",
         "ruby": r"\bruby\b|robin", "ollie": r"\bollie\b|\bowl\b", "rocky": r"\brocky\b|raccoon",
         "dot": r"\bdot\b|fawn|\bdeer\b", "bo": r"\bbo\b|badger", "wiggles": r"\bwiggles\b|otter"}


def expand(text):
    def one(m):
        k = m.group(1).lower()
        if k not in CHARACTERS:
            sys.exit(f"script.md 里的 [[{m.group(1)}]] 不是已知角色（{', '.join(CHARACTERS)}）")
        return CHARACTERS[k]
    return TOKEN.sub(one, text)


# 全员统一年龄感（2026-11-01 Bun 两次被否：一次成人化，一次太幼态）：都是五岁左右的小朋友
AGE_NOTE = ("All the animal friends are little children about five years old: child proportions with a big head and short legs, "
            "simple round eyes with a white highlight, no eyelashes, no winking, no half-closed eyes, "
            "never a grown-up figure and never a chubby baby (Bruno is just a bigger child). ")


def consistency_note(ids):
    """附在出图请求后面：逐个角色点名要保留的细节；两人以上同框时说明身高比例。"""
    note = AGE_NOTE if any(k in KEEP for k in ids) else ""
    keep = [f"{k}: {KEEP[k]}" for k in ids if k in KEEP]
    if keep:
        note += ("Must-keep details for each character (check every one before finishing): " + "; ".join(keep) + ". "
                 "Props a character holds in the reference pose (like a chestnut) appear only if the prompt asks for them, "
                 "but everything in the character description always stays. ")
    sized = [k for k in ids if k in SIZES]
    if len(sized) >= 2:
        note += ("Keep the series' height ladder when they stand together: "
                 + ", ".join(f"{k} about {SIZES[k]}x" for k in sorted(sized, key=SIZES.get)) + " (Pip = 1x). ")
    return note


def check_script(jobs):
    """出图前查一遍，返回必须先改的问题条数：点了名字/物种却没用整句描述（参考图带不上）、缺参考图。
    还在用升级前旧描述的只提示、不拦（旧集重出图照样能用）。"""
    issues, old = 0, set()
    for name, prompt in jobs.items():
        ids = set(char_ids(prompt))
        rest = prompt.lower()
        # 物种词也会出现在别人的描述里（"not a squirrel"），先去掉已识别的描述再找
        for i in ids:
            for d in (CHARACTERS[i],) + old_descs(i):
                rest = rest.replace(d.lower(), "")
        for k, pat in NAMES.items():
            if k not in ids and re.search(pat, rest):
                print(f"  ✗ {name}: 提到了 {k}，但没用整句描述，参考图带不上。改成 [[{k}]]")
                issues += 1
        for k in ids:
            if any(x in prompt for x in old_descs(k)) and CHARACTERS[k] not in prompt:
                old.add(k)
            if not os.path.exists(ref_path(k)):
                hint = "photo_character.py <集> pick N" if k in EP_REFS else f"codex_images.py refs --only {k}"
                print(f"  ✗ {name}: {k} 还没有参考图，先跑 {hint}")
                issues += 1
    if old:
        print(f"  提示：{', '.join(sorted(old))} 用的是旧描述（旧集可以不管；新剧本请改成 [[id]]）")
    return issues


def qc_sheet(epdir, names):
    """把每张出好的图和它带的参考图并排拼成 qc/characters.jpg，一眼对比角色有没有走样。"""
    lock = os.path.join(epdir, "images.json")
    if not os.path.exists(lock):
        return None
    rec = json.load(open(lock, encoding="utf-8"))
    rows = []
    for n in names:
        r = rec.get(n)
        if not r or not r.get("refs") or not os.path.exists(os.path.join(epdir, n)):
            continue
        im = Image.open(os.path.join(epdir, n)).convert("RGB")
        im.thumbnail((360, 640))
        refs = []
        for b in r["refs"]:
            if os.path.exists(ref_by_name(b)):
                x = Image.open(ref_by_name(b)).convert("RGB")
                x.thumbnail((240, 320))
                refs.append(x)
        rows.append((im, refs))
    if not rows:
        return None
    w = max(im.width + 20 + sum(x.width + 10 for x in refs) for im, refs in rows)
    h = sum(im.height + 20 for im, _ in rows)
    sheet = Image.new("RGB", (w, h), "white")
    y = 0
    for im, refs in rows:
        sheet.paste(im, (0, y))
        x0 = im.width + 20
        for x in refs:
            sheet.paste(x, (x0, y))
            x0 += x.width + 10
        y += im.height + 20
    os.makedirs(os.path.join(epdir, "qc"), exist_ok=True)
    dst = os.path.join(epdir, "qc", "characters.jpg")
    sheet.save(dst, quality=85)
    return dst


# 字幕旁的说话人小头像：只要头和一点肩膀，脸占满画面，缩到手机上 130 像素也认得出
AVATAR_PROMPT = ("close-up head-and-shoulders portrait of {desc}, facing the viewer with a friendly smile, the face filling most "
                 "of the square picture and centered, plain soft warm cream background, nothing else in the picture, " + STYLE + ", square 1:1")


def parse_script(path):
    """从 script.md 取出 {文件名: 提示词}：**p01.png** 下面的代码块、可灵首帧、封面关键画面。"""
    text = expand(open(path, encoding="utf-8").read())
    jobs = {}
    for name, body in re.findall(r"\*\*(p\d+\.png)\*\*\s*\n```[^\n]*\n(.*?)```", text, re.S):
        jobs[name] = " ".join(body.split())
    m = re.search(r"(?:可灵|钩子)首帧出图提示词.*?```[^\n]*\n(.*?)```", text, re.S)
    if m:
        jobs["kling_first.png"] = " ".join(m.group(1).split())
    last = sorted(k for k in jobs if k.startswith("p"))
    if last and "封面关键画面" in text:
        base = jobs[last[-1]].replace(", keep every face in the upper 55% of the image and the lower 40% simple open ground", "")
        jobs["cover.png"] = base + ", the characters and props sit in the lower half, the top 40% is clean open sky and soft tree canopy with empty space for a title"
    return jobs


def parse_keys(path):
    """关键帧：{文件名: (底图文件名, 改动说明)}，写法是 **p01b.png** ← p01.png（也认 <-）。"""
    text = expand(open(path, encoding="utf-8").read())
    return {name: (src, " ".join(body.split())) for name, src, body in re.findall(
        r"\*\*([\w-]+\.png)\*\*\s*(?:←|<-)\s*([\w-]+\.png)[^\n]*\n```[^\n]*\n(.*?)```", text, re.S)}


KEY_ASK = ("Edit the FIRST attached image. It is one drawing of an animation sequence and you are drawing the NEXT drawing of the "
           "same shot. Keep exactly the same scene, background, camera angle, framing, lighting, colors, art style, line work "
           "and character designs; keep every character in the same place and size unless the change says otherwise. "
           "Change ONLY this: {change}. Same vertical 9:16 size, no text, no watermark.")


# 单集换画风（国风特别版等）：集目录里放 style.json，见 load_episode_style()
EP_STYLE_REFS = None   # 不为 None 时，用这几张代替 series/style 当画风样张
EP_CHAR_REFS = True    # False 时不带角色参考图（参考图是日系手绘，可能把画风拉回去）


def style_refs():
    if EP_STYLE_REFS is not None:
        return EP_STYLE_REFS
    return sorted(glob.glob(os.path.join(STYLE_DIR, "*.png")) + glob.glob(os.path.join(STYLE_DIR, "*.jpg")))


def load_episode_style(ep):
    """集目录里有 style.json 就用这一集自己的画风：{"style": 画风词（漫画剧本用）, "style_refs": [相对集目录的样张路径],
    "char_refs": true/false}。样张图片不进仓库（episodes/**/*.png 已忽略），缺了就报错，免得悄悄用回系列样张。"""
    global STYLE, EP_STYLE_REFS, EP_CHAR_REFS
    cfg_path = os.path.join(ep, "style.json")
    if not os.path.exists(cfg_path):
        return
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    STYLE = cfg.get("style", STYLE)
    refs = [os.path.join(ep, r) for r in cfg.get("style_refs", [])]
    missing = [r for r in refs if not os.path.exists(r)]
    if missing:
        sys.exit("这一集的画风样张还没放好：" + "、".join(missing) + "（见 style.json 的说明）")
    EP_STYLE_REFS = refs
    EP_CHAR_REFS = cfg.get("char_refs", True)
    print(f"用这一集自己的画风：{cfg.get('name', '')}，样张 {len(refs)} 张，角色参考图{'带' if EP_CHAR_REFS else '不带'}")


def fingerprint(prompt, refs):
    h = hashlib.sha1(prompt.encode())
    for r in style_refs() + refs:
        h.update(str(os.path.getmtime(r)).encode())
    return h.hexdigest()[:12]


def small_ref(path, size=768):
    """参考图缩成 768px 的 JPEG 再上传：三张 2.6MB 的 PNG 一起传，网络一抖就断（Broken pipe）。关键帧底图用 1280px，细节要对得上。"""
    dst = os.path.join(tempfile.gettempdir(), "codex_refs",
                       f"{os.path.splitext(os.path.basename(path))[0]}_{int(os.path.getmtime(path))}_{size}.jpg")
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        img = Image.open(path).convert("RGB")
        img.thumbnail((size, size), Image.LANCZOS)
        img.save(dst, quality=88)
    return dst


MAX_IMAGES = 5


def lineup(refs, h=640):
    """把几张角色参考图按同样高度横着拼成一张阵容图（顺序和 CHARACTERS 一致）。"""
    order = {f"{k}.png": i for i, k in enumerate(CHARACTERS)}
    refs = sorted(refs, key=lambda r: order.get(os.path.basename(r), 99))
    ims = [Image.open(r).convert("RGB") for r in refs]
    ims = [im.resize((round(im.width * h / im.height), h), Image.LANCZOS) for im in ims]
    gap = 24
    out = Image.new("RGB", (sum(i.width for i in ims) + gap * (len(ims) - 1), h), (255, 255, 255))
    x = 0
    for im in ims:
        out.paste(im, (x, 0))
        x += im.width + gap
    dst = os.path.join(tempfile.gettempdir(), "codex_refs",
                       "lineup_" + "_".join(os.path.splitext(os.path.basename(r))[0] + str(int(os.path.getmtime(r))) for r in refs) + ".jpg")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    out.save(dst, quality=88)
    return dst


def codex_generate(prompt, refs, log, use_style=True, base=None, shape="vertical portrait image (9:16, the tallest portrait size available)"):
    """跑一次 codex exec，返回生成的原图路径。use_style=False 时不带画风样张（做画风对比用）。
    base：关键帧的底图，排第一张，只改提示词里说的动作（底图本身就带画风和角色，不再带样张）。"""
    ask = (f"Use your built-in image_gen tool exactly once to generate ONE {shape}. "
           "Use this prompt verbatim:\n\n" + prompt + "\n\n")
    styles = style_refs() if use_style and not base else []
    # Codex 一次最多收 5 张附图：样张最多 2 张；角色多时拼成一张从左到右的阵容图
    styles = styles[:2]
    room = MAX_IMAGES - len(styles) - (1 if base else 0)
    lineup_note = ""
    if len(refs) > room:
        names = [k for k, _ in CHARACTERS.items() if any(os.path.basename(r) == f"{k}.png" for r in refs)]
        refs = [lineup(refs)]
        lineup_note = ("They are combined into ONE lineup image; from left to right it shows: "
                       + "; ".join(CHARACTERS[n] for n in names) + ". ")
    if styles:
        ask += (f"The first {len(styles)} attached image(s) are the STYLE reference for this series. Match their art "
                "style closely: rendering, line work, cel shading, eye style, lighting, color palette and background painting. "
                "Do not copy their characters, poses, composition or scene.\n\n")
        if EP_STYLE_REFS is not None and refs:
            ask += ("The character reference sheets are drawn in a DIFFERENT art style. Take only each character's identity "
                    "from them (shape, colors, clothing, signature details); paint everything in the style of the STYLE "
                    "reference.\n\n")
    if refs:
        ask += ("The " + ("other " if styles or base else "") + "attached image(s) are the character reference sheets for this "
                "series. " + lineup_note + "Keep each character's face, body shape, colors and clothing exactly like the reference, "
                "but use the pose, scene and composition from the prompt, not the reference's.\n\n")
        ids = [os.path.splitext(os.path.basename(r))[0] for r in refs]
        if lineup_note:
            ids = names
        ask += consistency_note(ids) + "\n\n"
    ask += "Do not run shell commands and do not save or copy any files. Just generate the image and finish."
    images = [(small_ref(r, 1280 if base or os.path.basename(r).startswith("lineup_") else 768))
              for r in ([base] if base else []) + styles + refs]
    return codex_run(ask, images, log)


def codex_run(ask, images, log, timeout=600):
    """跑一次 codex exec 出图：ask 是完整的请求文本，images 是已缩好的附图路径（≤ MAX_IMAGES）。返回生成的原图路径。
    photo_character.py 也用它（照片 → 角色卡的请求文本不一样，自己拼）。"""
    cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only",
           "-c", "model_reasoning_effort=low", "--json", "-C", REFS if os.path.isdir(REFS) else HERE]
    for r in images:
        cmd += ["-i", r]
    cmd.append("-")  # 提示词走 stdin：-i 会吞掉后面的位置参数
    # 图一落盘就收工：网络抖动时 codex 会在出图后继续重连很久
    with open(log, "a", encoding="utf-8") as f:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=f, text=True)
        p.stdin.write(ask)
        p.stdin.close()
        events = []
        threading.Thread(target=lambda: [events.append(l) or f.write(l) for l in p.stdout], daemon=True).start()
        thread, t0 = None, time.time()
        while time.time() - t0 < timeout and p.poll() is None:
            time.sleep(2)
            for l in events:
                if '"thread.started"' in l:
                    thread = json.loads(l)["thread_id"]
            if thread and glob.glob(os.path.join(CODEX_HOME, "generated_images", thread, "*.png")):
                time.sleep(3)  # 等文件写完
                break
        if p.poll() is None:
            p.kill()
    pngs = glob.glob(os.path.join(CODEX_HOME, "generated_images", thread or "-", "*.png"))
    if not pngs:
        raise RuntimeError(f"Codex 没出图（thread {thread}），看日志 {log}")
    return max(pngs, key=os.path.getmtime)


def to_frame(src, dst):
    """按 9:16 居中裁切并放大到 1080×1920。参考图保持原样。"""
    img = Image.open(src).convert("RGB")
    s = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - W) // 2, (img.height - H) // 2
    img = img.crop((x, y, x + W, y + H)).filter(ImageFilter.UnsharpMask(2, 40, 2))
    img.save(dst)


def comic_jobs(script):
    """漫画剧本：钩子首帧 + p01–p08 每三格拼一张横版三联漫画（comic/sheet1-3.png），给用户确认剧本用。
    提示词去掉风格词和构图要求，只留画面；三格一起画，角色和画风前后对得上。"""
    shots = parse_script(script)
    order = [k for k in ["kling_first.png"] + [f"p{i:02d}.png" for i in range(1, 13)] if k in shots]
    keys = parse_keys(script)
    def scene(k):
        x = re.split(r", (?:Japanese hand-painted|polished digital children's|Chinese watercolor painting)", shots[k])[0]
        x = x.split(", keep every face")[0]
        # 这一页有关键帧时，漫画画最后一张关键帧那一刻（剧情的转折往往在那里，比如树枝断了），首图只当场景说明
        stem = os.path.splitext(k)[0]
        last = sorted(n for n in keys if re.fullmatch(stem + r"[b-z]\.png", n))
        if last:
            x += f"; draw the moment right after this, when {keys[last[-1]][1]}"
        return x
    jobs = {}
    for n in range(0, len(order), 3):
        group = order[n:n + 3]
        panels = " ".join(f"Panel {i + 1}: {scene(k)}." for i, k in enumerate(group))
        prompt = (f"A {len(group)}-panel comic strip laid out left to right, {len(group)} equal tall vertical panels side by side "
                  "separated by clean white gutters, each panel a full scene. " + panels + " Same characters, same art style in every "
                  "panel, " + STYLE + ". Absolutely no text, no speech bubbles, no captions, no panel numbers.")
        refs = char_refs(prompt)
        jobs[f"comic/sheet{n // 3 + 1}.png"] = (prompt, refs)
    return jobs, order


def comic_all_panels(ep):
    """--comic-all 的格子顺序：钩子首帧 + h02–h04，每页主图 + 这一页所有动作关键帧，按 story.json 里 cycle/frames 出现的先后；
    复习页复用的图跳过。返回 [{"image", "page"（hook / p01…）, "index"（story.json pages 下标）, "lines"（这一格下面写的台词序号）}]。"""
    story = json.load(open(os.path.join(ep, "story.json"), encoding="utf-8"))
    hook = [f["image"] for f in story.get("hook", {}).get("frames", [])]
    panels = [{"image": im, "page": "hook", "lines": [0] if i == 0 and story["hook"].get("say") else []}
              for i, im in enumerate(hook)]
    seen = set(hook)
    for n, page in enumerate(story["pages"]):
        if page["image"] in seen:
            continue
        frames = page.get("frames", [])
        order = [page["image"]] + page.get("cycle", {}).get("images", []) + [f["image"] for f in frames]
        imgs = [im for i, im in enumerate(order) if im not in order[:i]]
        seen.update(imgs)
        # 台词写在它说出时画面上那一格：有 talk（张嘴帧）就用 talk 的底图；否则按 line/offset 或 at 找当时在画面上的那张
        when = {page["image"]: (0, 0)}
        for f in frames:
            if f["image"] not in when:
                when[f["image"]] = (f["line"], f.get("offset", 0)) if "line" in f else (0, f.get("at", 0) - page.get("lead", 0))
        said = {im: [] for im in imgs}
        for i, line in enumerate(page.get("lines", [])):
            at = next((k for k in line.get("talk", {}) if k in said), None)
            if at is None:
                at = max((im for im in imgs if when.get(im, (0, 0)) <= (i, 0)), key=lambda im: when.get(im, (0, 0)))
            said[at].append(i)
        pid = re.match(r"p\d+", page["image"]).group()   # 分镜表里的页号；复习页插在中间时和 pages 下标对不上
        panels += [{"image": im, "page": pid, "index": n, "lines": said[im]} for im in imgs]
    return panels


def comic_all_jobs(script, ep):
    """漫画剧本（全部格子）：每个动作关键帧一格，三格一张。关键帧那格写成"主图场景 + 这一刻的动作"；
    和上一格是同一镜头的，写成"同一个镜头，只改了……"，三格连起来看就是连贯的动作。"""
    shots = parse_script(script)
    keys = parse_keys(script)
    panels = comic_all_panels(ep)

    def base(im):
        x = re.split(r", (?:Japanese hand-painted|polished digital children's)", shots[im])[0]
        return x.split(", keep every face")[0]

    def chain(im):   # 关键帧一路往回找到主图：[主图, 改动1, 改动2…]
        steps = []
        while im in keys:
            im, change = keys[im][0], keys[im][1]
            steps.insert(0, change)
        return im, steps

    def scene(im, prev):
        if im in shots:
            return base(im)
        if prev and keys[im][0] == prev:
            return f"the same shot as the previous panel, same background and positions, now {keys[im][1]}"
        root, steps = chain(im)
        return base(root) + "; at this moment, " + ", then ".join(steps)

    jobs = {}
    for n in range(0, len(panels), 3):
        group = [p["image"] for p in panels[n:n + 3]]
        parts = " ".join(f"Panel {i + 1}: {scene(im, group[i - 1] if i else None)}." for i, im in enumerate(group))
        prompt = (f"A {len(group)}-panel comic strip laid out left to right, {len(group)} equal tall vertical panels side by side "
                  "separated by clean white gutters, each panel a full scene, read left to right as one continuous moment of the "
                  "story. " + parts + " Same characters, same art style, same places and sizes in every panel, "
                  + STYLE + ". Absolutely no text, no speech bubbles, no captions, no panel numbers.")
        jobs[f"comic/sheet{n // 3 + 1}.png"] = (prompt, char_refs(prompt))
    return jobs, panels


def run_jobs(outdir, jobs, args, frame=True, use_style=True, shape=None):
    lock_path = os.path.join(outdir, "images.json")
    lock = json.load(open(lock_path)) if os.path.exists(lock_path) else {}
    log = os.path.join(outdir, ".codex_images.log")
    todo = []
    for name, job in jobs.items():
        prompt, refs = job[0], job[1]
        base = job[2] if len(job) > 2 else None
        if args.only and not {os.path.splitext(name)[0], os.path.splitext(os.path.basename(name))[0]} & set(args.only):
            continue
        if base and not os.path.exists(base):
            print(f"  ✗ {name}：底图 {os.path.basename(base)} 还没出")
            continue
        fp = fingerprint(prompt, refs + ([base] if base else []))
        dst = os.path.join(outdir, name)
        if not args.force and os.path.exists(dst) and lock.get(name, {}).get("fp") in (fp, None):
            continue
        todo.append((name, prompt, refs, fp, dst, base))
    if not todo:
        print(f"{os.path.relpath(outdir, ROOT)}：都出好了")
        return 0

    def one(job):
        name, prompt, refs, fp, dst, base = job
        t = time.time()
        for attempt in (1, 2):
            try:
                src = (codex_generate(prompt, refs, log, use_style, base, shape) if shape
                       else codex_generate(prompt, refs, log, use_style, base))
                break
            except Exception as e:  # 失败重试一次
                if attempt == 2:
                    print(f"  ✗ {name}：{e}")
                    return None
        to_frame(src, dst) if frame else Image.open(src).save(dst)
        print(f"  ✓ {os.path.relpath(dst, ROOT)}  {time.time() - t:.0f}s")
        return name, {"fp": fp, "source": src, "refs": [os.path.basename(r) for r in refs]}

    print(f"{os.path.relpath(outdir, ROOT)}：要出 {len(todo)} 张")
    with ThreadPoolExecutor(args.jobs) as ex:
        results = list(ex.map(one, todo))
    lock.update(dict(r for r in results if r))
    json.dump(lock, open(lock_path, "w"), ensure_ascii=False, indent=2)
    return sum(r is None for r in results)


def main():
    ap = argparse.ArgumentParser(description="用 Codex CLI 按 script.md 出图")
    ap.add_argument("targets", nargs="+", help="refs、sheets、avatars、styles，或集目录（里面有 script.md）")
    ap.add_argument("-j", "--jobs", type=int, default=2, help="并行张数，默认 2")
    ap.add_argument("--only", type=lambda s: s.split(","), help="只出这几张，如 p02,kling_first")
    ap.add_argument("--force", action="store_true", help="已有的也重出")
    ap.add_argument("--check", action="store_true", help="只检查角色写法（[[id]]、整句描述、参考图齐不齐），不出图")
    ap.add_argument("--allow-mismatch", action="store_true", help="角色检查有问题也照样出图（不推荐）")
    ap.add_argument("--comic", action="store_true", help="只出漫画剧本（三联横版漫画），剧本确认前给用户看")
    ap.add_argument("--comic-all", action="store_true", help="漫画剧本画全部格子：钩子 + 每页主图 + 每个动作关键帧，一格一个画面")
    ap.add_argument("--styles-config", default="style_tests.json", help="styles 用哪份画风对比配置（series/ 下的文件名），如 style_tests_guofeng.json，出到 out/<文件名去掉 .json>/")
    ap.add_argument("--variant", help="换一种画法出对比图（series/style_variants.json），出到 out/<集>/variant_<名字>/，不动集目录")
    args = ap.parse_args()

    failed = 0
    for t in args.targets:
        if t == "styles":
            # 画风对比：series/style_tests.json 里每种画风 × 每个场景各出一张，放 out/style_test/
            cfg = json.load(open(os.path.join(ROOT, "series", args.styles_config), encoding="utf-8"))
            sub = "style_test" if args.styles_config == "style_tests.json" else os.path.splitext(args.styles_config)[0]
            outdir = os.path.join(ROOT, "out", sub)
            os.makedirs(outdir, exist_ok=True)
            jobs = {f"{k}_{sc}.png": (f"{prompt}, {v['style']}", [])
                    for k, v in cfg["styles"].items() for sc, prompt in cfg["scenes"].items()}
            failed += run_jobs(outdir, jobs, args, use_style=False)
            continue
        if t == "avatars":
            # 说话人头像：以角色参考图为准，出到 series/refs/avatars/<角色>.png，sbv.py 字幕旁会用
            outdir = os.path.join(REFS, "avatars")
            os.makedirs(outdir, exist_ok=True)
            jobs = {f"{k}.png": (AVATAR_PROMPT.format(desc=d), [os.path.join(REFS, f"{k}.png")])
                    for k, d in CHARACTERS.items() if os.path.exists(os.path.join(REFS, f"{k}.png"))}
            failed += run_jobs(outdir, jobs, args, frame=False, use_style=False, shape="square image (1:1)")
            continue
        if t == "refs":
            os.makedirs(REFS, exist_ok=True)
            jobs = {f"{k}.png": (REF_PROMPT.format(desc=d, pose=POSES[k]) + ". " + AGE_NOTE, []) for k, d in CHARACTERS.items()}
            failed += run_jobs(REFS, jobs, args, frame=False)
            continue
        if t == "sheets":
            # 角色设定图（正面 + 侧面 + 三个表情）：以参考图为准，出到 series/sheets/，给人看、不进出图流程
            outdir = os.path.join(ROOT, "series", "sheets")
            os.makedirs(outdir, exist_ok=True)
            jobs = {f"{k}.png": (SHEET_PROMPT.format(desc=d, faces=FACES[k]) + ". " + AGE_NOTE, [os.path.join(REFS, f"{k}.png")])
                    for k, d in CHARACTERS.items() if k in FACES and os.path.exists(os.path.join(REFS, f"{k}.png"))}
            failed += run_jobs(outdir, jobs, args, frame=False, use_style=False,
                               shape="wide landscape image (3:2, the widest landscape size available)")
            continue
        script = os.path.join(t, "script.md")
        if not os.path.exists(script):
            sys.exit(f"找不到 {script}")
        load_episode_style(t)
        load_episode_characters(t)
        if args.comic or args.comic_all:
            os.makedirs(os.path.join(t, "comic"), exist_ok=True)
            # comic/panels.json 记下每格是哪张图、写哪几句台词，comic_page.py 照它配字；--comic 没有这个文件
            panels_json = os.path.join(t, "comic", "panels.json")
            if args.comic_all:
                jobs, panels = comic_all_jobs(script, t)
                json.dump(panels, open(panels_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            else:
                jobs, _ = comic_jobs(script)
                if os.path.exists(panels_json):
                    os.remove(panels_json)
            failed += run_jobs(os.path.abspath(t), jobs, args, frame=False,
                               shape="wide landscape image (3:2, the widest landscape size available)")
            continue
        # 角色一致性检查：没过不出图，免得白等一小时出一批走样的图
        shots = parse_script(script)
        print(f"检查角色写法：{script}")
        issues = check_script(shots)  # 关键帧只写"改哪里"（the mouse jumps），角色已在底图里，不查
        print(f"  {'没有问题' if not issues else f'{issues} 处问题'}")
        if args.check:
            failed += 1 if issues else 0
            continue
        if issues and not args.allow_mismatch:
            sys.exit("角色检查没过，先改 script.md（或加 --allow-mismatch 硬出）")
        jobs = {}
        for name, prompt in shots.items():
            jobs[name] = (prompt, char_refs(prompt))
        if args.variant:
            v = json.load(open(os.path.join(ROOT, "series", "style_variants.json"), encoding="utf-8"))[args.variant]
            outdir = os.path.join(ROOT, "out", os.path.basename(os.path.abspath(t)).split("-")[0], f"variant_{args.variant}")
            os.makedirs(outdir, exist_ok=True)
            for name, (prompt, refs) in jobs.items():
                for a, b in v["replace"]:
                    prompt = prompt.replace(a, b)
                prompt = prompt.replace(", no text, no watermark", ", " + v["append"] + ", no text, no watermark", 1)
                jobs[name] = (prompt, refs)
            failed += run_jobs(outdir, jobs, args, use_style=False)
            continue
        failed += run_jobs(os.path.abspath(t), jobs, args)
        # 第二轮：关键帧（底图要先出好）
        # 改动说明里点名了新角色（如 h03 镜头下移、露出树下的朋友），就把他们的参考图也带上
        keys = {name: (KEY_ASK.format(change=change),
                       char_refs(change),
                       os.path.join(os.path.abspath(t), src))
                for name, (src, change) in parse_keys(script).items()}
        # 关键帧也可以以关键帧为底（h04 ← h03）：底图还在待出列表里的，等下一轮再出，
        # 否则 --force 时会和底图同一轮并行，拿旧底图去改（s04 的 h04 就这样配错了）
        k_failed = 0
        while keys:
            ready = {n: j for n, j in keys.items() if os.path.basename(j[2]) not in keys} or keys
            k_failed += run_jobs(os.path.abspath(t), ready, args)
            keys = {n: j for n, j in keys.items() if n not in ready}
        failed += k_failed
        qc = qc_sheet(os.path.abspath(t), list(shots))
        if qc:
            print(f"角色对比图：{qc}（每张图右边是它带的参考图，逐个看标志细节在不在）")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
