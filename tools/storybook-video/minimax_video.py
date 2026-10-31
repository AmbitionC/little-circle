#!/usr/bin/env python3
"""用 MiniMax H3 把一张（或首尾两张）Codex 出好的图做成一段动作镜头，替代可灵钩子。走七七八AI（ai778.cc）的中转接口。

  python3 minimax_video.py ../../episodes/s05-xxx hook --first h01.png --last p01.png \\
      --prompt "[[pip]] jumps off the rock and lands in front of [[bruno]], ..."      # 只报价，不花钱
  python3 minimax_video.py ../../episodes/s05-xxx hook --first h01.png --last p01.png --prompt-file hook.txt --go
  python3 minimax_video.py ../../episodes/s05-xxx hook --status 123456                # 断了之后接着查、下载

两种出法（同一个模型 minimax-h3，用 mode 切换，不能混用）：
  首尾帧（默认，有 --first/--last）：首帧是已经过了角色质检的 Codex 图，角色一致性最稳。
  参考生（没有首帧时）：提示词里的 [[id]] 自动带上 series/refs/<id>.png，最多 9 张。
两种都会把 [[id]] 展开成角色整句描述，并附上 KEEP 细节和同框身高（和出图同一套，见 codex_images.py）。

不带 --go 只打印请求和预计花费；带 --go 才提交（中转站下单即扣费，失败自动退款）。
成片存成 <集目录>/<名字>.mp4，story.json 写 "hook": {"clip": "<名字>.mp4"} 就能用
（H3 自带声音，默认不用；要留声音加 keep_clip_audio）。
key 只从环境变量 AI778_API_KEY 读（跑 set_ai778_key.sh 弹框写进 ~/.zshrc，不要发进聊天）；地址用 AI778_API_BASE 改。
接口文档：https://ai778.cc/apidoc#model/minimax-h3 （2026-10-31 查）
"""
import argparse, base64, io, json, os, sys, time, urllib.error, urllib.request

from PIL import Image
from codex_images import REFS, char_ids, consistency_note, expand

BASE = os.environ.get("AI778_API_BASE", "https://api.lk888.ai").rstrip("/")
MODEL = os.environ.get("AI778_VIDEO_MODEL", "minimax-h3")
# 七七八AI 实扣（元/秒）：2026-10-31 s04 钩子 768P 5 秒扣 3.795 元；2K 按文档"约 768P 的 1.6 倍"估。真实扣费以返回的 cost 为准
PRICE = {"768P": 0.76, "2K": 1.21}
# 画面要求：和出图同一画风；儿童片，动作要清楚、不要镜头乱甩
STYLE = ("Japanese hand-painted 2D animation, cel-shaded characters with soft outlines, calm simple background. "
         "Keep every character exactly as in the input images: same colors, outfit, proportions and details, no morphing. "
         "One clear action, smooth gentle camera, no fast cuts, no text, no subtitles.")
TIMEOUT = 75 * 60   # 文档说常见 5~60 分钟，超过 70 分钟多半是上游拥堵


def data_url(path):
    """转成 JPEG 内联（中转站单张 base64 ≤10MB，PNG 原图可能超）。"""
    im = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def call(method, path, body=None):
    key = os.environ.get("AI778_API_KEY")
    if not key:
        sys.exit("没有 AI778_API_KEY：在 ~/.zshrc 加 export AI778_API_KEY=...，再 source ~/.zshrc（不要把 key 发进聊天）")
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"接口报错 {e.code}：{e.read().decode(errors='replace')[:500]}")


def build(args, epdir):
    prompt = open(args.prompt_file).read() if args.prompt_file else args.prompt
    if not prompt:
        sys.exit("要给 --prompt 或 --prompt-file")
    ids = char_ids(expand(prompt))
    text = f"{expand(prompt).strip()} {STYLE} {consistency_note(ids)}".strip()
    params = {"duration": str(args.duration), "resolution": args.resolution}
    shown = []
    if args.first or args.last:
        names = [n for n in (args.first, args.last) if n]
        if args.last and not args.first:
            sys.exit("只有尾帧不行：要首帧，或首帧+尾帧")
        params.update(mode="shouweizhen", images=[data_url(os.path.join(epdir, n)) for n in names])
        shown = [f"首帧={args.first}"] + ([f"尾帧={args.last}"] if args.last else [])
    else:
        refs = [os.path.join(REFS, f"{k}.png") for k in ids if os.path.exists(os.path.join(REFS, f"{k}.png"))][:9]
        if not refs:
            sys.exit("没有首尾帧，提示词里也没有带参考图的 [[id]]")
        params.update(mode="cankaosheng", image_url=[data_url(p) for p in refs], aspect_ratio="9:16")
        shown = [f"参考图={os.path.basename(p)}" for p in refs]
    return {"model": MODEL, "prompt": text, "params": params}, text, shown


def wait(tid):
    t0 = time.time()
    while True:
        st = call("GET", f"/v1/media/status?task_id={tid}")
        st = st.get("data", st)
        if st.get("is_final"):
            if st.get("state") != "success":
                sys.exit(f"生成失败（已自动退款）：{st.get('error') or st}")
            return st
        if time.time() - t0 > TIMEOUT:
            sys.exit(f"等了 {TIMEOUT // 60} 分钟还没好，先停。之后用 --status {tid} 接着查")
        print(f"  {st.get('state')} {st.get('progress', '')}", flush=True)
        time.sleep(10)


def save(meta, name, entry):
    """写之前重新读一遍：几条镜头并行跑时，各写各的那一项，不互相覆盖。"""
    log = json.load(open(meta)) if os.path.exists(meta) else {}
    log[name] = entry
    json.dump(log, open(meta, "w"), ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("name", help="输出文件名（不带 .mp4），如 hook")
    ap.add_argument("--first"); ap.add_argument("--last")
    ap.add_argument("--prompt"); ap.add_argument("--prompt-file")
    ap.add_argument("--duration", type=int, default=4, help="4–15 秒；默认最短 4 秒省钱，钩子只用 4.8 秒以内")
    ap.add_argument("--resolution", default="768P", choices=list(PRICE))
    ap.add_argument("--go", action="store_true", help="真的提交（花钱）")
    ap.add_argument("--status", help="已提交的 task_id：只查结果、下载，不重新提交")
    args = ap.parse_args()
    epdir = os.path.abspath(args.episode)
    meta = os.path.join(epdir, "minimax.json")
    log = json.load(open(meta)) if os.path.exists(meta) else {}

    if args.status:
        tid, entry = args.status, log.get(args.name, {})
    else:
        body, text, shown = build(args, epdir)
        cost = PRICE[args.resolution] * args.duration
        print(f"模型 {MODEL} @ {BASE}（{body['params']['mode']}）\n输入：{', '.join(shown)}\n"
              f"{args.resolution} {args.duration} 秒，预计约 {cost:.1f} 元（按七七八AI 实扣估，以返回的 cost 为准）\n提示词：{text}")
        if not args.go:
            print("\n只报价。确认要花再加 --go。")
            return
        r = call("POST", "/v1/media/generate", body)
        tid = r.get("task_id") or (r.get("data") or {}).get("task_id") or sys.exit(f"提交失败：{r}")
        entry = {"task_id": tid, "model": MODEL, "inputs": shown, "resolution": args.resolution,
                 "duration": args.duration, "prompt": text, "at": time.strftime("%Y-%m-%d %H:%M")}
        save(meta, args.name, entry)   # 先记下 task_id，断了也能 --status 接着查
        print(f"已提交 {tid}，每 10 秒查一次（常见 5~60 分钟）")

    t0 = time.time()
    st = wait(tid)
    out = os.path.join(epdir, f"{args.name}.mp4")
    urllib.request.urlretrieve(st["result_url"], out)
    entry.update(task_id=tid, cost=st.get("cost"), result_url=st["result_url"], wait_min=round((time.time() - t0) / 60, 1))
    save(meta, args.name, entry)
    print(f"完成：{out}，实扣 {st.get('cost')}（逐帧看一遍：角色走没走样、有没有融化变形，再写进 story.json 的 hook.clip）")


if __name__ == "__main__":
    main()
