#!/usr/bin/env python3
"""H3 片段进成片前先过这一步（2026-11-12 m06 卡顿后加）：
H3 出的是 24fps，sbv 直接按 30fps 抽帧会每 4 帧重复一帧，看着一顿一顿；用定格补坏帧会停住。
这里按帧号截取、去掉坏帧（眨眼半眯、多出道具），再用运动补帧改速到 30fps，不重复、不定格。

  python3 prep_clip.py <源.mp4> <出.mp4> --from 0 --to 106 --drop 71-80 --speed 1.25
  --to 写到 H3 自己硬切之前（逐帧差值突然很大的那一帧，m06 s6 在第 112 帧硬切到全景）。
截出来的第一帧要和前一张关键帧一样（首尾帧模式的首帧），story.json 里这一页不要写 clip_from，前一页 motion 用 out（收到 1.0 倍）。"""
import argparse, glob, os, shutil, subprocess, tempfile

FF = os.environ.get("FFMPEG", "ffmpeg")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--from", dest="a", type=int, default=0, help="从第几帧开始（0 起）")
    ap.add_argument("--to", dest="b", type=int, default=10 ** 6, help="到第几帧（含）")
    ap.add_argument("--drop", default="", help="去掉的帧，如 71-80,114-123")
    ap.add_argument("--speed", type=float, default=1.0, help="改速，>1 变快")
    a = ap.parse_args()
    drop = set()
    for part in filter(None, a.drop.split(",")):
        x, _, y = part.partition("-")
        drop |= set(range(int(x), int(y or x) + 1))
    tmp = tempfile.mkdtemp()
    src, out = os.path.join(tmp, "a"), os.path.join(tmp, "b")
    os.makedirs(src); os.makedirs(out)
    subprocess.run([FF, "-v", "error", "-y", "-i", a.src, "-q:v", "1", os.path.join(src, "a_%04d.png")], check=True)
    n = len(glob.glob(os.path.join(src, "a_*.png")))
    k = 1
    for i in range(a.a, min(a.b, n - 1) + 1):
        if i not in drop:
            shutil.copy(os.path.join(src, f"a_{i + 1:04d}.png"), os.path.join(out, f"b_{k:04d}.png")); k += 1
    # 先按源节奏补帧到 30*speed fps，再把时间压回 30fps（setpts 放前面 minterpolate 会崩）
    vf = f"minterpolate=fps={30 * a.speed:.3f}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts=PTS/{a.speed:.4f}"
    subprocess.run([FF, "-v", "error", "-y", "-framerate", "24", "-i", os.path.join(out, "b_%04d.png"), "-vf", vf, "-r", "30",
                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", a.dst], check=True)
    shutil.rmtree(tmp)
    print(f"{a.dst}：用了 {k - 1} 帧源帧，速度 {a.speed}")


if __name__ == "__main__":
    main()
