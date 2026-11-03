#!/usr/bin/env python3
"""把 Freesound 下来的原始音效收进系列音效库：切头尾、统一电平、记下出处和授权。

  # 单个音效（一下就完的）：默认按 sfx_probe 的建议切掉前面空白和长尾，峰值归一到 -1 dBFS
  python3 sfx_import.py assets/sfx/fs/fs_59315_looking_in_bushes-wav.mp3 rustle
  python3 sfx_import.py <原始文件> twig --skip 0.05 --dur 0.5
  # 环境底声（铺整段的）：切 60 秒，按响度归一到 -28 dBFS RMS，首尾各淡 1 秒
  python3 sfx_import.py assets/sfx/fs/fs_577623_forest-with-small-river-birds-and-nature.mp3 amb_forest --bed --skip 20

产物：assets/sfx/<name>.wav（48k 单声道，不进仓库），出处追加到 series/sfx_sources.csv（进仓库，查授权用）。
文件名里有 fs_<id> 时，从 sound skill 的搜索缓存（~/.cache/sfx-sources/index.json）读标题、作者、授权、下载量。
只收 CC0：非 CC0 会报错停下（商用要署名或不许商用），确实要用就加 --allow-by 并在发布文案里署名。
"""
import argparse, csv, datetime, json, os, re, subprocess, sys
from pathlib import Path

import numpy as np

SR = 48000
ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "assets" / "sfx"
SOURCES = ROOT / "series" / "sfx_sources.csv"
INDEX = Path.home() / ".cache" / "sfx-sources" / "index.json"
FIELDS = ["name", "kind", "source", "id", "title", "author", "license", "stats", "skip", "dur", "url", "desc", "added"]


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def save(path, a):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                          "-c:a", "pcm_s16le", str(path)], stdin=subprocess.PIPE)
    p.communicate(a.astype(np.float32).tobytes())


def suggest(a):
    """和 sfx_probe 同一套：起音 / 有效尾 = 超过峰值 -30 dB 的第一帧 / 最后一帧（10 毫秒一帧）。"""
    hop = int(0.01 * SR)
    n = len(a) // hop
    d = 20 * np.log10(np.sqrt(np.mean(a[: n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-9)
    on = np.nonzero(d > d.max() - 30)[0]
    skip = max(0.0, on[0] * 0.01 - 0.02)
    return skip, min(len(a) / SR, (on[-1] + 1) * 0.01 + 0.15) - skip


def meta_for(src):
    m = re.search(r"fs_(\d+)", Path(src).name)
    if not m:
        return {"source": "local", "id": "", "license": "?"}
    try:
        r = json.loads(INDEX.read_text()).get(f"fs:{m[1]}", {})
    except (OSError, ValueError):
        r = {}
    return {"source": "freesound", "id": m[1], "title": r.get("title", ""), "author": r.get("author", ""),
            "license": r.get("license", "?"), "stats": r.get("stats", ""), "desc": r.get("desc", ""),
            "url": f"https://freesound.org/s/{m[1]}/"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("name", help="库里的名字，story.json 用 ../../assets/sfx/<name>.wav 引用")
    ap.add_argument("--skip", type=float, help="从原始文件第几秒开始用（默认按起音自动）")
    ap.add_argument("--dur", type=float, help="用几秒（默认到有效尾；--bed 默认 60）")
    ap.add_argument("--bed", action="store_true", help="环境底声：按响度归一、首尾淡 1 秒")
    ap.add_argument("--peak", type=float, default=-1.0, help="单个音效的峰值 dBFS（默认 -1）")
    ap.add_argument("--allow-by", action="store_true", help="允许 Attribution 授权（发布时要署名）")
    ap.add_argument("--force", action="store_true", help="覆盖库里同名文件")
    a = ap.parse_args()

    meta = meta_for(a.src)
    lic = meta.get("license", "?")
    if meta["source"] == "freesound" and lic != "CC0" and not (a.allow_by and lic == "BY"):
        sys.exit(f"授权是 {lic}，不收（只收 CC0；BY 要加 --allow-by 并署名；BY-NC 不能商用）")
    out = LIB / f"{a.name}.wav"
    if out.exists() and not a.force:
        sys.exit(f"{out} 已存在，加 --force 覆盖")

    x = load(a.src)
    if a.bed:
        skip, dur = a.skip or 0.0, a.dur or 60.0
    else:
        s0, d0 = suggest(x)
        skip = s0 if a.skip is None else a.skip
        dur = d0 if a.dur is None else a.dur
    y = x[int(skip * SR): int((skip + dur) * SR)].copy()
    dur = len(y) / SR
    if a.bed:
        y *= 10 ** (-28 / 20) / (np.sqrt(np.mean(y ** 2)) or 1e-6)
        f = min(int(1.0 * SR), len(y) // 4)
        y[:f] *= np.linspace(0, 1, f)
        y[-f:] *= np.linspace(1, 0, f)
        y = np.clip(y, -0.98, 0.98)
    else:
        y *= 10 ** (a.peak / 20) / (np.abs(y).max() or 1e-6)
        f = min(int(0.04 * SR), len(y) // 4)          # 切口淡出，不出咔哒声
        y[-f:] *= np.linspace(1, 0, f)
        g = min(int(0.003 * SR), len(y) // 4)
        y[:g] *= np.linspace(0, 1, g)
    LIB.mkdir(parents=True, exist_ok=True)
    save(out, y)

    rows = []
    if SOURCES.exists():
        with SOURCES.open(encoding="utf-8") as fh:
            rows = [r for r in csv.DictReader(fh) if r["name"] != a.name]
    rows.append(dict(meta, name=a.name, kind="bed" if a.bed else "oneshot", skip=f"{skip:.2f}", dur=f"{dur:.2f}",
                     added=datetime.date.today().isoformat()))
    with SOURCES.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: r["name"]))
    print(f"{out.relative_to(ROOT)}  {dur:.2f}s  skip {skip:.2f}  {lic}  {meta.get('title', '')}")


if __name__ == "__main__":
    main()
