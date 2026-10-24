#!/usr/bin/env python3
"""合成一段八音盒背景音乐（C–Am–F–G，90 BPM），纯数学生成，无版权问题。
用法：python make_bgm.py out.wav [秒数]"""
import subprocess
import sys

import numpy as np

SR = 48000
NOTE = {"G3": 196.0, "A3": 220.0, "B3": 246.9, "C4": 261.6, "D4": 293.7, "E4": 329.6, "F4": 349.2,
        "G4": 392.0, "A4": 440.0, "B4": 493.9, "C5": 523.3, "D5": 587.3, "E5": 659.3, "G5": 784.0}
BARS = [("C4", ["C5", "E5", "G5", "E5"]), ("A3", ["A4", "C5", "E5", "C5"]),
        ("F4", ["F4", "A4", "C5", "A4"]), ("G3", ["G4", "B4", "D5", "B4"])]


def bell(f, dur, amp):
    t = np.arange(int(dur * SR)) / SR
    env = np.minimum(t / 0.004, 1) * np.exp(-t / 0.55)
    return amp * env * (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t)
                        + 0.12 * np.sin(2 * np.pi * 3.01 * f * t))


def main():
    out, secs = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 16
    beat = 60 / 90
    n = int(secs * SR) + SR * 2
    mix = np.zeros(n)
    t, i = 0.0, 0
    while t < secs:
        bass, arp = BARS[i % len(BARS)]
        o = int(t * SR)
        b = bell(NOTE[bass] / 2, beat * 4, 0.35)[: n - o]
        mix[o:o + len(b)] += b
        for k in range(8):                      # 每小节 8 个八分音符琶音
            o = int((t + k * beat / 2) * SR)
            if o >= n:
                break
            s = bell(NOTE[arp[k % 4]], 1.5, 0.22 if k % 2 == 0 else 0.15)[: n - o]
            mix[o:o + len(s)] += s
        t += beat * 4
        i += 1
    mix = mix[: int(secs * SR)]
    mix *= 0.2 / np.sqrt(np.mean(mix ** 2))
    fade = int(0.8 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-", out],
                         stdin=subprocess.PIPE)
    p.communicate(mix.astype(np.float64).tobytes())


if __name__ == "__main__":
    main()
