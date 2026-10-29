#!/usr/bin/env python3
"""封面图（9:16 视频封面 + 3:4 小红书封面）。代码来自系列 Skill 附录 A，字体改成本机能找到的。

用法（在本目录下）：
    python brand.py ../../episodes/s02-help/story.json --ep 2 \
        --words help=帮忙 push=推 ball=球 --out ../../out/s02
key_art 默认用 story.json 同目录的 cover.png；标题取 story.json 的 title_en / title_zh。
"""
import argparse
import json
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
EN_FONTS = [os.path.join(HERE, "fonts/Fredoka.ttf"),
            "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
# (路径, 粗体 index, 中等 index)
ZH_FONTS = [("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 2, 2),
            ("/System/Library/Fonts/Hiragino Sans GB.ttc", 2, 2),
            ("/System/Library/Fonts/STHeiti Medium.ttc", 0, 0)]
BRAND = dict(series_zh='栗栗学英语',
    tagline_zh='幼儿英语启蒙 · 中英字幕 · 3岁+',
    cream=(255, 248, 232), cream_txt=(255, 246, 222), brown=(92, 52, 24), brown_soft=(110, 84, 62),
    orange=(232, 137, 43), green=(122, 154, 74), ink=(60, 30, 10))


def fr(size, weight='Bold'):
    for p in EN_FONTS:
        if os.path.exists(p):
            f = ImageFont.truetype(p, size)
            try:
                f.set_variation_by_name(weight)
            except (OSError, ValueError):
                pass
            return f
    raise SystemExit("找不到英文字体")


def zh(size, medium=False):
    for p, bold, med in ZH_FONTS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size, index=med if medium else bold)
    raise SystemExit("找不到中文字体")


def text_block(text, font, fill, stroke=0, stroke_fill=None, shadow=0):
    bb = font.getbbox(text, stroke_width=stroke); pad = 20 + shadow
    im = Image.new('RGBA', (bb[2]-bb[0]+pad*2, bb[3]-bb[1]+pad*2), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad-bb[0], pad-bb[1]), text, font=font, fill=fill+(255,),
                            stroke_width=stroke, stroke_fill=(stroke_fill or fill)+(255,))
    if not shadow: return im
    a = im.getchannel('A').filter(ImageFilter.GaussianBlur(shadow/2))
    sh = Image.new('RGBA', im.size, BRAND['ink']+(0,)); sh.putalpha(a.point(lambda v: int(v*0.45)))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, int(shadow*0.6))); out.alpha_composite(im)
    return out


def paste_c(dst, im, cx, cy): dst.alpha_composite(im, (int(cx-im.width/2), int(cy-im.height/2)))


def leaf_icon(size, col):
    S = size*3; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([S*.18, S*.05, S*.82, S*.95], fill=col+(255,))
    d.line([(S*.5, S*.12), (S*.5, S)], fill=BRAND['cream']+(255,), width=S//14)
    return im.rotate(-30, resample=Image.BICUBIC, expand=True).resize((size, size), Image.LANCZOS)


def pill(w, h, fill, outline=None, alpha=240):
    im = Image.new('RGBA', (w+30, h+30), (0, 0, 0, 0)); sh = Image.new('L', im.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([15, 21, 15+w, 21+h], radius=h//2, fill=90)
    s = Image.new('RGBA', im.size, BRAND['ink']+(0,)); s.putalpha(sh.filter(ImageFilter.GaussianBlur(8))); im.alpha_composite(s)
    ImageDraw.Draw(im).rounded_rectangle([15, 15, 15+w, 15+h], radius=h//2, fill=fill+(alpha,),
                                         outline=(outline+(255,)) if outline else None, width=3)
    return im


def series_badge(scale=1.0):
    """徽章：叶子图标 + 「栗栗学英语」（旧版是 Forest Friends English · 森林小伙伴英语）。"""
    f = zh(int(38*scale)); t = BRAND['series_zh']; tw = f.getlength(t)
    ic, gap = int(46*scale), int(18*scale)
    w, h = int(ic+gap+tw+gap*2.6), int(78*scale)
    im = pill(w, h, BRAND['cream'], (232, 214, 186)); x, cy = 15+gap*1.4, 15+h/2
    im.alpha_composite(leaf_icon(ic, BRAND['green']), (int(x), int(cy-ic/2)))
    ImageDraw.Draw(im).text((x+ic+gap, cy+2*scale), t, font=f, fill=BRAND['brown'], anchor='lm')
    return im


def ep_ribbon(ep, scale=1.0):
    f, fz = fr(int(44*scale)), zh(int(34*scale)); t1, t2 = f'EP.{ep:02d}', f'第{ep}集'
    w, h = int(f.getlength(t1)+fz.getlength(t2)+90*scale), int(66*scale)
    im = pill(w, h, BRAND['orange'], None, 255); d = ImageDraw.Draw(im); cy = 15+h/2
    d.text((15+30*scale, cy), t1, font=f, fill=(255, 255, 255), anchor='lm')
    d.text((15+w-30*scale, cy+2*scale), t2, font=fz, fill=(255, 240, 220), anchor='rm')
    return im


def wrap_title(text, font, maxw):
    if font.getlength(text) <= maxw: return [text]
    words, best = text.split(), None
    for k in range(1, len(words)):
        a, b = ' '.join(words[:k]), ' '.join(words[k:]); m = max(font.getlength(a), font.getlength(b))
        if best is None or m < best[0]: best = (m, [a, b])
    return best[1]


def gradient(size, top_a, bot_a, col, y0, y1):
    w, h = size; g = Image.new('L', (1, h), 0)
    for y in range(h):
        a = top_a if y <= y0 else bot_a if y >= y1 else top_a+(bot_a-top_a)*((y-y0)/(y1-y0))**1.2
        g.putpixel((0, y), int(a))
    layer = Image.new('RGBA', size, col+(0,)); layer.putalpha(g.resize(size)); return layer


def word_chip(en, zh_txt, scale=1.0):
    fe, fz = fr(int(50*scale), 'SemiBold'), zh(int(28*scale), True)
    w, h = int(max(fe.getlength(en), fz.getlength(zh_txt))+70*scale), int(112*scale)
    im = Image.new('RGBA', (w+30, h+30), (0, 0, 0, 0)); sh = Image.new('L', im.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([15, 21, 15+w, 21+h], radius=int(30*scale), fill=110)
    s = Image.new('RGBA', im.size, BRAND['ink']+(0,)); s.putalpha(sh.filter(ImageFilter.GaussianBlur(8))); im.alpha_composite(s)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([15, 15, 15+w, 15+h], radius=int(30*scale), fill=BRAND['cream']+(245,), outline=(232, 214, 186, 255), width=3)
    d.text((15+w/2, 15+h*.38), en, font=fe, fill=BRAND['orange'], anchor='mm')
    d.text((15+w/2, 15+h*.76), zh_txt, font=fz, fill=BRAND['brown_soft'], anchor='mm')
    return im


def make_cover(key_art, ep, title_en, title_zh, words, size=(1080, 1920), crop_y=0.55):
    cw, ch = size; k = max(cw/key_art.width, ch/key_art.height)
    art = key_art.convert('RGBA').resize((int(key_art.width*k), int(key_art.height*k)), Image.LANCZOS)
    oy, ox = int((art.height-ch)*crop_y), (art.width-cw)//2
    cv = art.crop((ox, oy, ox+cw, oy+ch)); s = cw/1080; tall = ch > cw*1.5
    top = int(ch*(0.40 if tall else 0.47))
    cv.alpha_composite(gradient(size, 235, 0, BRAND['cream'], int(top*0.45), top))
    cv.alpha_composite(gradient(size, 0, 190, BRAND['ink'], int(ch*0.72), ch))
    y = 95*s
    b = series_badge(s); paste_c(cv, b, cw/2, y+b.height/2-15); y += b.height+10*s
    r = ep_ribbon(ep, s); paste_c(cv, r, cw/2, y+r.height/2-10); y += r.height+5*s
    ft = fr(int(126*s))
    for line in wrap_title(title_en, ft, cw-120*s):
        t = text_block(line, ft, BRAND['cream_txt'], int(12*s), BRAND['brown'], int(14*s))
        paste_c(cv, t, cw/2, y+t.height/2-25*s); y += t.height-50*s
    tz = text_block(title_zh, zh(int(66*s)), BRAND['brown'], int(8*s), BRAND['cream'], int(8*s))
    paste_c(cv, tz, cw/2, y+tz.height/2+5*s)
    cs = s if tall else s*0.82
    chips = [word_chip(e, z, cs) for e, z in words]
    total = sum(c.width for c in chips)-30*(len(chips)-1); cy_chips = ch-(235 if tall else 175)*s
    if tall:
        paste_c(cv, text_block("Today's words  今日单词", zh(int(30*s), True), BRAND['cream']), cw/2, cy_chips-105*s)
    x = cw/2-total/2
    for c in chips: cv.alpha_composite(c, (int(x), int(cy_chips-c.height/2))); x += c.width-30
    paste_c(cv, text_block(BRAND['tagline_zh'], zh(int(30*s), True), (255, 236, 205)), cw/2, ch-80*s)
    return cv.convert('RGB')


def main():
    ap = argparse.ArgumentParser(description="出封面图：9:16 1080×1920 + 3:4 1080×1440")
    ap.add_argument("story")
    ap.add_argument("--ep", type=int, required=True, help="集数（封面上的 EP.xx）")
    ap.add_argument("--words", nargs="+", required=True, help="今日单词，写成 help=帮忙")
    ap.add_argument("--key-art", help="默认用 story.json 同目录的 cover.png")
    ap.add_argument("--crop-3x4", type=float, default=0.55, help="3:4 封面从原图哪里裁（0=顶部，1=底部），标题压脸时调")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.story))
    with open(a.story) as f:
        cfg = json.load(f)
    art = Image.open(a.key_art or os.path.join(base, "cover.png"))
    words = [w.split("=", 1) for w in a.words]
    os.makedirs(a.out, exist_ok=True)
    name = cfg.get("output_name", "storybook")
    for size, tag, crop_y in (((1080, 1920), "9x16", 0.55), ((1080, 1440), "3x4", a.crop_3x4)):
        p = os.path.join(a.out, f"{name}_cover_{tag}.jpg")
        make_cover(art, a.ep, cfg["title_en"], cfg["title_zh"], words, size, crop_y).save(p, quality=93)
        print(p)


if __name__ == "__main__":
    main()
