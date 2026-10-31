#!/usr/bin/env python3
"""用 MiniMax H3 把一张（或首尾两张）Codex 出好的图做成一段动作镜头，替代可灵钩子。

  python3 minimax_video.py ../../episodes/s05-xxx hook --first h01.png --last p01.png \\
      --prompt "[[pip]] jumps off the rock and lands in front of [[bruno]], ..."      # 只报价，不花钱
  python3 minimax_video.py ../../episodes/s05-xxx hook --first h01.png --last p01.png --prompt-file hook.txt --go

两种出法（H3 的接口二选一，不能混用）：
  首尾帧（默认，有 --first/--last）：首帧是已经过了角色质检的 Codex 图，角色一致性最稳。
  参考图（--ref，没有首帧时用）：提示词里的 [[id]] 自动带上 series/refs/<id>.png，最多 9 张。
两种都会把 [[id]] 展开成角色整句描述，并附上 KEEP 细节和同框身高（和出图同一套，见 codex_images.py）。

不带 --go 只打印请求和预计花费；带 --go 才提交。成片存成 <集目录>/<名字>.mp4，
story.json 里写 "hook": {"clip": "<名字>.mp4"} 就能用（H3 自带声音，默认不用；要留声音加 keep_clip_audio）。
key 只从环境变量 MINIMAX_API_KEY 读；接入地址用 MINIMAX_API_BASE 改（默认国内官方）。
"""
import argparse, base64, json, mimetypes, os, sys, time, urllib.request

from codex_images import REFS, char_ids, consistency_note, expand

BASE = os.environ.get("MINIMAX_API_BASE", "https://api.minimaxi.com").rstrip("/")
MODEL = os.environ.get("MINIMAX_VIDEO_MODEL", "MiniMax-H3")
# 官方国内价（2026-08 发布时公布，元/秒）；第三方渠道价格不同，以渠道为准
PRICE = {"768P": 0.5, "2K": 0.8}
# 画面要求：和出图同一画风；儿童片，动作要清楚、不要镜头乱甩
STYLE = ("Japanese hand-painted 2D animation, cel-shaded characters with soft outlines, calm simple background. "
         "Keep every character exactly as in the input images: same colors, outfit, proportions and details, no morphing. "
         "One clear action, smooth gentle camera, no fast cuts, no text, no subtitles.")


def data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"


def call(method, path, body=None):
    key = os.environ.get("MINIMAX_API_KEY")
    if not key:
        sys.exit("没有 MINIMAX_API_KEY：在 ~/.zshrc 加 export MINIMAX_API_KEY=...，再 source ~/.zshrc（不要把 key 发进聊天）")
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def build(args, epdir):
    prompt = open(args.prompt_file).read() if args.prompt_file else args.prompt
    if not prompt:
        sys.exit("要给 --prompt 或 --prompt-file")
    ids = char_ids(expand(prompt))
    text = f"{expand(prompt).strip()} {STYLE} {consistency_note(ids)}".strip()
    content = [{"type": "text", "text": text}]
    shown = []
    if args.first or args.last:
        for role, name in (("first_frame", args.first), ("last_frame", args.last)):
            if name:
                content.append({"type": "image_url", "image_url": {"url": data_url(os.path.join(epdir, name))}, "role": role})
                shown.append(f"{role}={name}")
    else:
        refs = [os.path.join(REFS, f"{k}.png") for k in ids if os.path.exists(os.path.join(REFS, f"{k}.png"))][:9]
        if not refs:
            sys.exit("没有首尾帧，提示词里也没有带参考图的 [[id]]")
        for p in refs:
            content.append({"type": "image_url", "image_url": {"url": data_url(p)}, "role": "reference_image"})
            shown.append(f"ref={os.path.basename(p)}")
    body = {"model": MODEL, "content": content, "duration": args.duration, "resolution": args.resolution,
            "ratio": "adaptive" if (args.first or args.last) else "9:16"}
    return body, text, shown


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("name", help="输出文件名（不带 .mp4），如 hook")
    ap.add_argument("--first"); ap.add_argument("--last")
    ap.add_argument("--prompt"); ap.add_argument("--prompt-file")
    ap.add_argument("--duration", type=int, default=5, help="4–15 秒")
    ap.add_argument("--resolution", default="768P", choices=list(PRICE))
    ap.add_argument("--go", action="store_true", help="真的提交（花钱）")
    args = ap.parse_args()
    epdir = os.path.abspath(args.episode)

    body, text, shown = build(args, epdir)
    cost = PRICE[args.resolution] * args.duration
    print(f"模型 {MODEL} @ {BASE}\n输入：{', '.join(shown)}\n{args.resolution} {args.duration} 秒，预计约 {cost:.1f} 元（官方价）\n提示词：{text}")
    if not args.go:
        print("\n只报价。确认要花再加 --go。")
        return

    task = call("POST", "/v2/video_generation", body)
    tid = task.get("task_id") or sys.exit(f"提交失败：{task}")
    print(f"已提交 {tid}，每 10 秒查一次")
    while True:
        time.sleep(10)
        t = call("GET", f"/v2/query/video_generation/{tid}").get("task", {})
        st = t.get("status")
        if st == "succeeded":
            break
        if st in ("failed", "cancelled"):
            sys.exit(f"生成失败：{t.get('error') or t}")
        print(f"  {st}")
    out = os.path.join(epdir, f"{args.name}.mp4")
    urllib.request.urlretrieve(t["content"]["url"], out)
    meta = os.path.join(epdir, "minimax.json")
    log = json.load(open(meta)) if os.path.exists(meta) else {}
    log[args.name] = {"task_id": tid, "model": MODEL, "inputs": shown, "resolution": args.resolution,
                      "duration": args.duration, "prompt": text, "at": time.strftime("%Y-%m-%d %H:%M")}
    json.dump(log, open(meta, "w"), ensure_ascii=False, indent=2)
    print(f"完成：{out}（逐帧看一遍：角色走没走样、有没有融化变形，再写进 story.json 的 hook.clip）")


if __name__ == "__main__":
    main()
