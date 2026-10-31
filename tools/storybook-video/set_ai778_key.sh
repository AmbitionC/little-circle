#!/bin/bash
# 弹一个隐藏输入框，把七七八AI 的 AK 写进 ~/.zshrc（全局生效）。旧的 AI778_API_KEY 行会先删掉，key 不会打印出来。
#   bash ~/code/little-circle/tools/storybook-video/set_ai778_key.sh
set -e
k=$(osascript -e 'text returned of (display dialog "把七七八AI 的 AK 粘贴到这里" default answer "" with hidden answer with title "AI778 API Key" giving up after 600)' 2>/dev/null) || { echo "取消了，什么都没改"; exit 1; }
k=$(printf '%s' "$k" | tr -d '[:space:]"'"'"'“”‘’')
[ -n "$k" ] || { echo "没粘贴内容，什么都没改"; exit 1; }
touch ~/.zshrc
cp ~/.zshrc ~/.zshrc.bak-ai778
grep -v '^export AI778_API_KEY=' ~/.zshrc.bak-ai778 > ~/.zshrc || true
printf 'export AI778_API_KEY=%s\n' "$k" >> ~/.zshrc
zsh -lic 'echo ${AI778_API_KEY:+已写好：新开的终端都能读到 AI778_API_KEY（长度 ${#AI778_API_KEY}）}'
echo "旧文件备份在 ~/.zshrc.bak-ai778，确认没问题可以删掉"
