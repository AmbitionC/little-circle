#!/usr/bin/env python3
"""把漫画剧本拼成一个网页：三联漫画切成单格，每格配上段落、画面、台词（中英）、音效和运镜，给用户确认剧本用。

  python3 codex_images.py ../../episodes/s03-sleepy --comic        # 先出 comic/sheet1-3.png
  python3 comic_page.py ../../episodes/s03-sleepy                  # → out/<集>/comic.html，再发布成 Artifact

格子按白色分隔条自动切；切不出来就按宽度均分。台词从 story.json 读，画面说明从 script.md 的分镜表读。
"""
import argparse, base64, glob, html, io, json, os, re, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
NAMES = {"narrator": "旁白", "nutty": "栗栗", "hazel": "Hazel", "bun": "Bun", "pip": "皮皮", "bruno": "Bruno",
         "fern": "Fern", "ruby": "Ruby", "ollie": "Ollie", "rocky": "Rocky", "dot": "Dot", "bo": "Bo", "wiggles": "Wiggles"}


def split_panels(path, n):
    """找竖向的白色分隔条，切成 n 格；找不到就均分。四周白边一并裁掉。"""
    img = Image.open(path).convert("RGB")
    a = np.asarray(img).astype(np.int16)
    white = (a.min(axis=2) > 232).mean(axis=0) > 0.92        # 这一列几乎全白 = 分隔条
    cols = [i for i in range(len(white)) if not white[i]]
    runs, start = [], None
    for x in range(len(white) + 1):
        ink = x < len(white) and not white[x]
        if ink and start is None:
            start = x
        elif not ink and start is not None:
            if x - start > img.width * 0.12:
                runs.append((start, x))
            start = None
    if len(runs) != n:
        w = img.width / n
        runs = [(int(i * w), int((i + 1) * w)) for i in range(n)]
    out = []
    for x0, x1 in runs:
        p = img.crop((x0, 0, x1, img.height))
        rows = (np.asarray(p).min(axis=2) > 232).mean(axis=1) < 0.92
        ys = np.where(rows)[0]
        if len(ys):
            p = p.crop((0, int(ys[0]), p.width, int(ys[-1]) + 1))
        out.append(p)
    return out, len(cols) > 0


def table_rows(script):
    """分镜表：{'p01': {'段落':…, '画面':…, '音效':…, '运镜':…}}"""
    text = open(script, encoding="utf-8").read()
    rows = {}
    for line in text.splitlines():
        m = re.match(r"\|\s*(p\d+)\s*\|(.*)\|\s*$", line)
        if m:
            cells = [c.strip() for c in m.group(2).split("|")]
            if len(cells) >= 5:
                rows[m.group(1)] = {"段落": cells[0], "画面": cells[1], "音效": cells[3], "运镜": cells[4]}
    beats = re.search(r"\*\*画面节拍\*\*.*?\n((?:\s*- .*\n)+)", text)
    hook = "\n".join(l for l in beats.group(1).splitlines() if "秒" in l) if beats else ""
    hook = re.sub(r"（.*?）|`[^`]*`", "", hook).strip()
    return rows, hook


def jpeg_b64(im, w=720):
    im = im.copy()
    im.thumbnail((w, w * 2), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=84)
    return base64.b64encode(buf.getvalue()).decode()


def md(s):
    s = html.escape(s).replace("&lt;br&gt;", "<br>")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def main():
    ap = argparse.ArgumentParser(description="漫画剧本 → 网页")
    ap.add_argument("episode")
    ap.add_argument("--out", help="默认 out/<集编号>/comic.html")
    args = ap.parse_args()
    ep = os.path.abspath(args.episode)
    story = json.load(open(os.path.join(ep, "story.json"), encoding="utf-8"))
    rows, hook_beats = table_rows(os.path.join(ep, "script.md"))
    sheets = sorted(glob.glob(os.path.join(ep, "comic", "sheet*.png")), key=lambda p: int(re.findall(r"\d+", os.path.basename(p))[0]))
    if not sheets:
        sys.exit("还没有漫画：先跑 codex_images.py <集> --comic")
    keys = ["hook"] + [f"p{i + 1:02d}" for i in range(len(story["pages"]))]
    panels = []
    for i, sh in enumerate(sheets):
        n = min(3, len(keys) - 3 * i)
        panels += split_panels(sh, n)[0]

    cards = []
    for k, im in zip(keys, panels):
        if k == "hook":
            h = story.get("hook", {})
            say = h.get("say", {})
            title, seg = "开头钩子 · 5 秒", "钩子"
            scene = md(hook_beats).replace("\n", "<br>")
            lines = [("旁白", say.get("en", ""), say.get("zh", ""))] if say else []
            extra = f"<p class=big>第 0 帧大字：<b>{html.escape(h.get('headline', ''))}</b><br><span>{html.escape(h.get('subline', ''))}</span></p>"
            meta = ""
        else:
            page = story["pages"][int(k[1:]) - 1]
            r = rows.get(k, {})
            title, seg = f"第 {int(k[1:])} 页", r.get("段落", "")
            scene = md(r.get("画面", ""))
            lines = [(NAMES.get(l.get("speaker", "narrator"), l.get("speaker")), l["en"], l.get("zh", "")) for l in page["lines"]]
            extra = ""
            meta = " · ".join(x for x in [f"音效：{r['音效']}" if r.get("音效") else "", f"运镜：{r['运镜']}" if r.get("运镜") else ""] if x)
        bubbles = "".join(f"<div class=line><span class=who>{html.escape(w)}</span><span class=en>{html.escape(e)}</span>"
                          f"<span class=zh>{html.escape(z)}</span></div>" for w, e, z in lines)
        cards.append(f"""<article class=card>
  <figure><img src="data:image/jpeg;base64,{jpeg_b64(im)}" alt="{html.escape(title)}"></figure>
  <div class=body>
    <header><h2>{html.escape(title)}</h2><span class=seg>{html.escape(seg)}</span></header>
    {extra}<p class=scene>{scene}</p>
    <div class=lines>{bubbles}</div>
    {f'<p class=meta>{html.escape(meta)}</p>' if meta else ''}
  </div>
</article>""")

    page = f"""<!doctype html><html lang=zh-CN><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>{html.escape(re.sub(r"[！!？?。，,]", "", story.get('title_zh', '')))} 漫画剧本</title>
<style>
:root{{--bg:#FFF8E8;--card:#fff;--ink:#3b2a1d;--soft:#6E543E;--accent:#E8892B;--line:#ecdcc2;--bubble:#FFF3DA}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#1d1813;--card:#2a221b;--ink:#f3e7d6;--soft:#c9b49b;--accent:#f0a252;--line:#3d3228;--bubble:#352a20}}}}
:root[data-theme=dark]{{--bg:#1d1813;--card:#2a221b;--ink:#f3e7d6;--soft:#c9b49b;--accent:#f0a252;--line:#3d3228;--bubble:#352a20}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,"PingFang SC","Noto Sans SC",sans-serif}}
main{{max-width:1080px;margin:0 auto;padding:24px 16px 64px}}
h1{{font-size:26px;margin:0 0 4px}}.sub{{color:var(--soft);margin:0 0 24px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}}
figure{{margin:0;background:#000}}figure img{{display:block;width:100%;height:auto}}
.body{{padding:14px 16px 16px}}header{{display:flex;justify-content:space-between;align-items:baseline;gap:8px}}
h2{{font-size:18px;margin:0}}.seg{{color:var(--accent);font-size:13px;font-weight:600}}
.scene{{color:var(--soft);font-size:14px;margin:8px 0}}.big{{margin:8px 0;font-size:15px}}.big span{{color:var(--soft);font-size:13px}}
.line{{background:var(--bubble);border-radius:12px;padding:8px 12px;margin:8px 0}}
.who{{display:block;font-size:12px;color:var(--accent);font-weight:600}}.en{{display:block;font-size:17px;font-weight:600}}
.zh{{display:block;font-size:14px;color:var(--soft)}}.meta{{font-size:12px;color:var(--soft);margin:8px 0 0}}
</style></head><body><main>
<h1>{html.escape(story.get('title_en', ''))} · {html.escape(story.get('title_zh', ''))}</h1>
<p class=sub>漫画剧本：每格是一页的关键画面（草图，不是成片），下面是这一页的台词、音效和运镜。看完觉得没问题，再开始出图做动画。</p>
<div class=grid>{''.join(cards)}</div>
</main></body></html>"""
    out = args.out or os.path.join(ROOT, "out", os.path.basename(ep).split("-")[0], "comic.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(page)
    print(f"漫画剧本网页：{out}（{len(cards)} 格）")


if __name__ == "__main__":
    main()
