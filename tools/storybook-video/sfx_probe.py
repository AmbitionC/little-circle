#!/usr/bin/env python3
"""看一眼音效的"形状"：听不到声音时，用能量曲线判断从哪开始响、哪里最响、尾巴多长。

  python3 sfx_probe.py assets/sfx/fs/*.mp3            # 每个文件一行：时长、起音、峰值、有效尾、建议 skip/dur、响度
  python3 sfx_probe.py --curve assets/sfx/bonk.mp3     # 再打印每 0.1 秒的能量条，看有几下、间隔多少

起音 = 第一次超过峰值 -30 dB 的时刻（story.json 的 at 要减掉它，冲击才落在点上）；
有效尾 = 最后一次超过峰值 -30 dB 的时刻；建议 skip/dur 就是把前面空白和后面长尾切掉（前留 0.02 秒、后留 0.15 秒）。
"""
import argparse, os, subprocess, sys

import numpy as np

SR = 48000
HOP = int(0.01 * SR)


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def db_curve(a):
    n = len(a) // HOP
    frames = a[: n * HOP].reshape(n, HOP)
    return 20 * np.log10(np.sqrt(np.mean(frames ** 2, axis=1)) + 1e-9)


def probe(path, curve=False):
    a = load(path)
    dur = len(a) / SR
    d = db_curve(a)
    if not len(d):
        print(f"{os.path.basename(path)}\t空文件")
        return
    peak = d.max()
    on = np.nonzero(d > peak - 30)[0]
    t_on, t_off, t_pk = on[0] * 0.01, (on[-1] + 1) * 0.01, d.argmax() * 0.01
    skip = max(0.0, t_on - 0.02)
    use = min(dur, t_off + 0.15) - skip
    rms = 20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-9)
    print(f"{os.path.basename(path)}\t时长 {dur:.2f}s\t起音 {t_on:.2f}s\t峰值 {t_pk:.2f}s ({peak:.0f} dB)\t"
          f"有效尾 {t_off:.2f}s\t建议 skip {skip:.2f} dur {use:.2f}\t整体 RMS {rms:.0f} dB")
    if curve:
        step = 10   # 0.1 秒一格
        for i in range(0, len(d), step):
            v = d[i:i + step].max()
            bar = "#" * max(0, int((v - (peak - 40)) / 2))
            print(f"  {i * 0.01:6.1f}s {v:6.1f} dB {bar}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--curve", action="store_true", help="打印每 0.1 秒的能量条")
    a = ap.parse_args()
    for f in a.files:
        try:
            probe(f, a.curve)
        except subprocess.CalledProcessError as e:
            print(f"{f}\t解码失败: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
