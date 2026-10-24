#!/usr/bin/env python3
"""生成演示用占位图和假“可灵钩子镜头”。正式使用时换成 GPT image 出的页面图和可灵生成的 5 秒片段。"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IW, IH = 1024, 1536
ZH = next(p for p in ["/System/Library/Fonts/PingFang.ttc",
                      "/System/Library/Fonts/Hiragino Sans GB.ttc",
                      "/System/Library/Fonts/STHeiti Medium.ttc",
                      "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"] if os.path.exists(p))


def scene(draw_extra, name):
    im = Image.new("RGB", (IW, IH))
    d = ImageDraw.Draw(im)
    for y in range(IH):
        k = y / IH
        d.line([(0, y), (IW, y)], fill=(int(24 + 60 * k), int(30 + 50 * k), int(80 + 60 * k)))
    d.ellipse((760, 140, 900, 280), fill=(255, 244, 200))
    for x, y in [(120, 200), (300, 120), (520, 260), (660, 90), (880, 420), (200, 420)]:
        d.ellipse((x, y, x + 10, y + 10), fill=(255, 255, 230))
    d.rectangle((40, 300, 190, 1200), fill=(92, 60, 40))
    d.ellipse((-160, 160, 400, 560), fill=(46, 102, 64))
    d.ellipse((-200, 1050, 1250, 1900), fill=(70, 130, 70))
    draw_extra(d)
    d.text((IW // 2, 40), "DEMO 占位图", font=ImageFont.truetype(ZH, 36), fill=(255, 255, 255), anchor="mt")
    im.save(os.path.join(HERE, name))


def squirrel(d, x, y, color=(214, 120, 48), sad=False, s=1.0):
    def e(a, b, c, dd, fill):
        d.ellipse((x + a * s, y + b * s, x + c * s, y + dd * s), fill=fill)
    e(-170, -160, -20, 120, color)                       # 尾巴
    e(-60, -20, 110, 200, color)                         # 身体
    e(-20, -150, 130, -10, color)                        # 头
    e(-5, -185, 35, -130, color)
    e(85, -185, 125, -130, color)                        # 耳朵
    e(20, -105, 42, -83, (30, 20, 10))
    e(80, -105, 102, -83, (30, 20, 10))                  # 眼睛
    if sad:
        d.arc((x + 35 * s, y - 60 * s, x + 90 * s, y - 25 * s), 200, 340, fill=(30, 20, 10), width=5)
    else:
        d.arc((x + 35 * s, y - 75 * s, x + 90 * s, y - 35 * s), 20, 160, fill=(30, 20, 10), width=5)


def acorn(d, x, y, s=1.0, half=0):
    if half:
        d.pieslice((x, y, x + 120 * s, y + 150 * s), 90 if half == 1 else 270, 270 if half == 1 else 450, fill=(170, 110, 50))
    else:
        d.ellipse((x, y, x + 120 * s, y + 150 * s), fill=(170, 110, 50))
    d.chord((x - 10 * s, y - 30 * s, x + 130 * s, y + 50 * s), 180, 360, fill=(110, 70, 35))


scene(lambda d: (squirrel(d, 420, 1000), acorn(d, 640, 1000, 1.4)), "p1.png")
scene(lambda d: (squirrel(d, 380, 980, s=1.2), acorn(d, 520, 1080, 1.2)), "p2.png")
scene(lambda d: (squirrel(d, 300, 1000), acorn(d, 420, 1120), squirrel(d, 760, 1020, (150, 120, 100), sad=True)), "p3.png")
scene(lambda d: (squirrel(d, 300, 1000), squirrel(d, 760, 1020, (150, 120, 100)), acorn(d, 470, 1110, 1.0, 1), acorn(d, 560, 1110, 1.0, 2)), "p4.png")
scene(lambda d: (squirrel(d, 330, 1000), squirrel(d, 700, 1000, (150, 120, 100)), acorn(d, 430, 1100, 0.8, 1), acorn(d, 640, 1100, 0.8, 2)), "p5.png")

# 假钩子镜头：用第 1 页做快速推近 + 轻微摇晃，模拟可灵输出的 5 秒片段
subprocess.run([
    "ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", os.path.join(HERE, "p1.png"), "-t", "5",
    "-vf", "scale=2048:3072,zoompan=z='min(1.0+0.004*on,1.5)':x='iw/2-(iw/zoom/2)+12*sin(on/4)':"
           "y='ih/2-(ih/zoom/2)+40':d=150:s=1080x1920:fps=30,format=yuv420p",
    "-c:v", "libx264", "-crf", "20", os.path.join(HERE, "hook_demo.mp4")], check=True)
print("占位素材已生成")
