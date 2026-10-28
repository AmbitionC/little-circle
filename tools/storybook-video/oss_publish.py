#!/usr/bin/env python3
"""把一集的成品包同步到阿里云 OSS，生成可直接打开的链接，写进 out/<集>/oss.json。

  .venv/bin/pip install oss2                          # 第一次
  .venv/bin/python oss_publish.py ../../out/s02       # 同步 s02

key 只从环境变量读：OSS_ACCESS_KEY_ID、OSS_ACCESS_KEY_SECRET（放在 ~/.zshrc，别发进聊天、别提交）。
bucket / 地域默认和 fe-journey-faas 一致，可用 OSS_BUCKET、OSS_REGION 覆盖。
对象放在 little-circle/<集>/ 下：能设公共读就给永久链接；bucket 禁止公共读时退回 7 天签名链接。
"""
import argparse, glob, json, mimetypes, os, sys

BUCKET = os.environ.get("OSS_BUCKET", "font-end-journey-resources")
REGION = os.environ.get("OSS_REGION", "oss-cn-hangzhou")
PREFIX = "little-circle"
SIGN_SECONDS = 7 * 24 * 3600
# 成品包里要同步的文件（质检留底、字幕、PDF 也一起，方便手机上直接拿）
PATTERNS = ["*.mp4", "*_cover_*.jpg", "publish.txt", "*.srt", "*_print.pdf", "xhs/*"]


def main():
    ap = argparse.ArgumentParser(description="成品包同步到 OSS")
    ap.add_argument("outdir", help="成品目录，如 ../../out/s02")
    args = ap.parse_args()
    try:
        import oss2
    except ImportError:
        sys.exit("缺 oss2：先跑 .venv/bin/pip install oss2")
    kid, secret = os.environ.get("OSS_ACCESS_KEY_ID"), os.environ.get("OSS_ACCESS_KEY_SECRET")
    if not kid or not secret:
        sys.exit("没读到 OSS_ACCESS_KEY_ID / OSS_ACCESS_KEY_SECRET。在 ~/.zshrc 里 export 后，新开终端或 source ~/.zshrc。")
    bucket = oss2.Bucket(oss2.Auth(kid, secret), f"https://{REGION}.aliyuncs.com", BUCKET)

    outdir = os.path.abspath(args.outdir)
    ep = os.path.basename(outdir.rstrip("/"))
    files = sorted({f for p in PATTERNS for f in glob.glob(os.path.join(outdir, p)) if os.path.isfile(f)})
    if not files:
        sys.exit(f"{outdir} 里没有成品文件")
    result, public = {}, True
    for f in files:
        rel = os.path.relpath(f, outdir)
        key = f"{PREFIX}/{ep}/{rel}"
        ctype = mimetypes.guess_type(f)[0] or "application/octet-stream"
        headers = {"Content-Type": ctype + ("; charset=utf-8" if ctype.startswith("text/") else ""),
                   "Content-Disposition": "inline"}
        oss2.resumable_upload(bucket, key, f, headers=headers)
        if public:
            try:
                bucket.put_object_acl(key, oss2.OBJECT_ACL_PUBLIC_READ)
            except oss2.exceptions.OssError:
                public = False          # bucket 开了"阻止公共访问"：后面都用签名链接
        url = (f"https://{BUCKET}.{REGION}.aliyuncs.com/{key}" if public
               else bucket.sign_url("GET", key, SIGN_SECONDS, slash_safe=True))
        result[rel] = url
        print(f"  ✓ {rel}")
    meta = {"bucket": BUCKET, "public": public, "expires_days": None if public else 7, "files": result}
    json.dump(meta, open(os.path.join(outdir, "oss.json"), "w"), ensure_ascii=False, indent=2)
    print(f"同步完成：{len(result)} 个文件，{'公共读永久链接' if public else '7 天签名链接'}，链接写在 {os.path.join(outdir, 'oss.json')}")


if __name__ == "__main__":
    main()
