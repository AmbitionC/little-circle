#!/usr/bin/env python3
"""用本机 Codex CLI（ChatGPT 登录，内置 image_gen）按 script.md 的出图提示词批量出图。

  python3 codex_images.py refs                         # 先出三个角色的参考图 → series/refs/
  python3 codex_images.py styles                       # 画风对比：series/style_tests.json → out/style_test/
  python3 codex_images.py ../../episodes/c01-fruits    # 出一集：p01–p06、kling_first、cover
  python3 codex_images.py ../../episodes/c0[1-3]-* -j 2  # 多集，两张并行
  python3 codex_images.py ../../episodes/s03-sleepy --comic   # 漫画剧本：每三格一张横版漫画，剧本确认前给用户看

关键帧（做动画用，不花可灵灵感值）：script.md 里写 **p01b.png** ← p01.png，下面代码块只写"改哪里"。
脚本先出底图，再把底图当第一张参考图，让 Codex 只改动作、其余不动，出同一镜头的下一张画。

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

STYLE = ("Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, gentle warm nostalgic light, clear bright colors, no text, no watermark")
# 画风参考图（用户给的样张，只留在本机，不进仓库）：每张图都带上，锁住画风
STYLE_DIR = os.path.join(ROOT, "series", "style")
# 角色固定描述（和 Skill 5.2 节一字不差），出现在提示词里就带上对应参考图
CHARACTERS = {
    "nutty": "a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf",
    "hazel": "a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls",
    "bun": "a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest",
}
REF_PROMPT = ("character reference sheet of {desc}, one single full-body view standing and facing the viewer, "
              "friendly smile, plain warm cream paper background, nothing else in the picture, " + STYLE + ", vertical 9:16")


def parse_script(path):
    """从 script.md 取出 {文件名: 提示词}：**p01.png** 下面的代码块、可灵首帧、封面关键画面。"""
    text = open(path, encoding="utf-8").read()
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
    text = open(path, encoding="utf-8").read()
    return {name: (src, " ".join(body.split())) for name, src, body in re.findall(
        r"\*\*([\w-]+\.png)\*\*\s*(?:←|<-)\s*([\w-]+\.png)[^\n]*\n```[^\n]*\n(.*?)```", text, re.S)}


KEY_ASK = ("Edit the FIRST attached image. It is one drawing of an animation sequence and you are drawing the NEXT drawing of the "
           "same shot. Keep exactly the same scene, background, camera angle, framing, lighting, colors, art style, line work "
           "and character designs; keep every character in the same place and size unless the change says otherwise. "
           "Change ONLY this: {change}. Same vertical 9:16 size, no text, no watermark.")


def style_refs():
    return sorted(glob.glob(os.path.join(STYLE_DIR, "*.png")) + glob.glob(os.path.join(STYLE_DIR, "*.jpg")))


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


def codex_generate(prompt, refs, log, use_style=True, base=None, shape="vertical portrait image (9:16, the tallest portrait size available)"):
    """跑一次 codex exec，返回生成的原图路径。use_style=False 时不带画风样张（做画风对比用）。
    base：关键帧的底图，排第一张，只改提示词里说的动作（底图本身就带画风和角色，不再带样张）。"""
    ask = (f"Use your built-in image_gen tool exactly once to generate ONE {shape}. "
           "Use this prompt verbatim:\n\n" + prompt + "\n\n")
    styles = style_refs() if use_style and not base else []
    if styles:
        ask += (f"The first {len(styles)} attached image(s) are the STYLE reference for this series. Match their art "
                "style closely: rendering, line work, cel shading, eye style, lighting, color palette and background painting. "
                "Do not copy their characters, poses, composition or scene.\n\n")
    if refs:
        ask += ("The " + ("other " if styles else "") + "attached image(s) are the character reference sheets for this "
                "series. Keep each character's face, body shape, colors and clothing exactly like the reference, "
                "but use the pose, scene and composition from the prompt, not the reference's.\n\n")
    ask += "Do not run shell commands and do not save or copy any files. Just generate the image and finish."
    cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only",
           "-c", "model_reasoning_effort=low", "--json", "-C", REFS if os.path.isdir(REFS) else HERE]
    for r in ([base] if base else []) + styles + refs:
        cmd += ["-i", small_ref(r, 1280 if base else 768)]
    cmd.append("-")  # 提示词走 stdin：-i 会吞掉后面的位置参数
    # 图一落盘就收工：网络抖动时 codex 会在出图后继续重连很久
    with open(log, "a", encoding="utf-8") as f:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=f, text=True)
        p.stdin.write(ask)
        p.stdin.close()
        events = []
        threading.Thread(target=lambda: [events.append(l) or f.write(l) for l in p.stdout], daemon=True).start()
        thread, t0 = None, time.time()
        while time.time() - t0 < 600 and p.poll() is None:
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
    def scene(k):
        x = shots[k].split(", Japanese hand-painted")[0]
        return x.split(", keep every face")[0]
    jobs = {}
    for n in range(0, len(order), 3):
        group = order[n:n + 3]
        panels = " ".join(f"Panel {i + 1}: {scene(k)}." for i, k in enumerate(group))
        prompt = (f"A {len(group)}-panel comic strip laid out left to right, {len(group)} equal tall vertical panels side by side "
                  "separated by clean white gutters, each panel a full scene. " + panels + " Same characters, same art style in every "
                  "panel, " + STYLE + ". Absolutely no text, no speech bubbles, no captions, no panel numbers.")
        refs = [os.path.join(REFS, f"{c}.png") for c, d in CHARACTERS.items()
                if d in prompt and os.path.exists(os.path.join(REFS, f"{c}.png"))]
        jobs[f"comic/sheet{n // 3 + 1}.png"] = (prompt, refs)
    return jobs, order


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
    ap.add_argument("targets", nargs="+", help="refs、styles，或集目录（里面有 script.md）")
    ap.add_argument("-j", "--jobs", type=int, default=2, help="并行张数，默认 2")
    ap.add_argument("--only", type=lambda s: s.split(","), help="只出这几张，如 p02,kling_first")
    ap.add_argument("--force", action="store_true", help="已有的也重出")
    ap.add_argument("--comic", action="store_true", help="只出漫画剧本（三联横版漫画），剧本确认前给用户看")
    args = ap.parse_args()

    failed = 0
    for t in args.targets:
        if t == "styles":
            # 画风对比：series/style_tests.json 里每种画风 × 每个场景各出一张，放 out/style_test/
            cfg = json.load(open(os.path.join(ROOT, "series", "style_tests.json"), encoding="utf-8"))
            outdir = os.path.join(ROOT, "out", "style_test")
            os.makedirs(outdir, exist_ok=True)
            jobs = {f"{k}_{sc}.png": (f"{prompt}, {v['style']}", [])
                    for k, v in cfg["styles"].items() for sc, prompt in cfg["scenes"].items()}
            failed += run_jobs(outdir, jobs, args, use_style=False)
            continue
        if t == "refs":
            os.makedirs(REFS, exist_ok=True)
            jobs = {f"{k}.png": (REF_PROMPT.format(desc=d), []) for k, d in CHARACTERS.items()}
            failed += run_jobs(REFS, jobs, args, frame=False)
            continue
        script = os.path.join(t, "script.md")
        if not os.path.exists(script):
            sys.exit(f"找不到 {script}")
        if args.comic:
            os.makedirs(os.path.join(t, "comic"), exist_ok=True)
            jobs, _ = comic_jobs(script)
            failed += run_jobs(os.path.abspath(t), jobs, args, frame=False,
                               shape="wide landscape image (3:2, the widest landscape size available)")
            continue
        jobs = {}
        for name, prompt in parse_script(script).items():
            refs = [os.path.join(REFS, f"{k}.png") for k, d in CHARACTERS.items()
                    if d in prompt and os.path.exists(os.path.join(REFS, f"{k}.png"))]
            jobs[name] = (prompt, refs)
        failed += run_jobs(os.path.abspath(t), jobs, args)
        # 第二轮：关键帧（底图要先出好）
        keys = {name: (KEY_ASK.format(change=change), [], os.path.join(os.path.abspath(t), src))
                for name, (src, change) in parse_keys(script).items()}
        if keys:
            failed += run_jobs(os.path.abspath(t), keys, args)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
