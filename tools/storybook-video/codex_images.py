#!/usr/bin/env python3
"""用本机 Codex CLI（ChatGPT 登录，内置 image_gen）按 script.md 的出图提示词批量出图。

  python3 codex_images.py refs                         # 先出三个角色的参考图 → series/refs/
  python3 codex_images.py ../../episodes/c01-fruits    # 出一集：p01–p06、kling_first、cover
  python3 codex_images.py ../../episodes/c0[1-3]-* -j 2  # 多集，两张并行

已有的图跳过；script.md 里某张图的提示词改了，会自动重出那一张。--force 全部重出，--only p02,p05 只出这几张。
图会裁成 1080×1920 存进集目录，原图路径和提示词指纹记在 images.json。
"""
import argparse, glob, hashlib, json, os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REFS = os.path.join(ROOT, "series", "refs")
CODEX_HOME = os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex"))
W, H = 1080, 1920

STYLE = ("watercolor and gouache children's picture book illustration, hand-painted brush strokes, "
         "visible paper grain, soft warm light, cozy vintage storybook feel, no text, no watermark")
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
    m = re.search(r"可灵首帧出图提示词.*?```[^\n]*\n(.*?)```", text, re.S)
    if m:
        jobs["kling_first.png"] = " ".join(m.group(1).split())
    last = sorted(k for k in jobs if k.startswith("p"))
    if last and "封面关键画面" in text:
        base = jobs[last[-1]].replace(", keep the bottom quarter of the image simple and free of faces", "")
        jobs["cover.png"] = base + ", the characters and props sit in the lower half, the top 40% is clean open sky and soft tree canopy with empty space for a title"
    return jobs


def fingerprint(prompt, refs):
    h = hashlib.sha1(prompt.encode())
    for r in refs:
        h.update(str(os.path.getmtime(r)).encode())
    return h.hexdigest()[:12]


def codex_generate(prompt, refs, log):
    """跑一次 codex exec，返回生成的原图路径。"""
    ask = ("Use your built-in image_gen tool exactly once to generate ONE vertical portrait image "
           "(9:16, the tallest portrait size available). Use this prompt verbatim:\n\n" + prompt + "\n\n")
    if refs:
        ask += ("The attached image(s) are the character reference sheets for this series. Keep each character's "
                "face, body shape, colors and clothing exactly like the reference, but use the pose, scene and "
                "composition from the prompt, not the reference's.\n\n")
    ask += "Do not run shell commands and do not save or copy any files. Just generate the image and finish."
    cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only",
           "-c", "model_reasoning_effort=low", "--json", "-C", REFS if os.path.isdir(REFS) else HERE]
    for r in refs:
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


def run_jobs(outdir, jobs, args, frame=True):
    lock_path = os.path.join(outdir, "images.json")
    lock = json.load(open(lock_path)) if os.path.exists(lock_path) else {}
    log = os.path.join(outdir, ".codex_images.log")
    todo = []
    for name, (prompt, refs) in jobs.items():
        if args.only and os.path.splitext(name)[0] not in args.only:
            continue
        fp = fingerprint(prompt, refs)
        dst = os.path.join(outdir, name)
        if not args.force and os.path.exists(dst) and lock.get(name, {}).get("fp") in (fp, None):
            continue
        todo.append((name, prompt, refs, fp, dst))
    if not todo:
        print(f"{os.path.relpath(outdir, ROOT)}：都出好了")
        return 0

    def one(job):
        name, prompt, refs, fp, dst = job
        t = time.time()
        for attempt in (1, 2):
            try:
                src = codex_generate(prompt, refs, log)
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
    ap.add_argument("targets", nargs="+", help="refs，或集目录（里面有 script.md）")
    ap.add_argument("-j", "--jobs", type=int, default=2, help="并行张数，默认 2")
    ap.add_argument("--only", type=lambda s: s.split(","), help="只出这几张，如 p02,kling_first")
    ap.add_argument("--force", action="store_true", help="已有的也重出")
    args = ap.parse_args()

    failed = 0
    for t in args.targets:
        if t == "refs":
            os.makedirs(REFS, exist_ok=True)
            jobs = {f"{k}.png": (REF_PROMPT.format(desc=d), []) for k, d in CHARACTERS.items()}
            failed += run_jobs(REFS, jobs, args, frame=False)
            continue
        script = os.path.join(t, "script.md")
        if not os.path.exists(script):
            sys.exit(f"找不到 {script}")
        jobs = {}
        for name, prompt in parse_script(script).items():
            refs = [os.path.join(REFS, f"{k}.png") for k, d in CHARACTERS.items()
                    if d in prompt and os.path.exists(os.path.join(REFS, f"{k}.png"))]
            jobs[name] = (prompt, refs)
        failed += run_jobs(os.path.abspath(t), jobs, args)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
