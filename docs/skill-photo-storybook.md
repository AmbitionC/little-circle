# 类型三：专属绘本线（x）——孩子照片 + 一段话 → 专属英文绘本 + 动画视频 + 打印版

> 系列 skill 的分册（2026-11-04 起）。公共部分（红线、系列规范、出图、渲染、质检、交付）在 [skill-kids-english-story-video.md](skill-kids-english-story-video.md)，台词、story.json、配音、配乐规则沿用口语分册 [skill-type-talk.md](skill-type-talk.md)。这里只写专属绘本和口语线不一样的地方。背景与商业规划见 [plan-photo-storybook-2026-11.md](plan-photo-storybook-2026-11.md)。

**专属绘本是什么**：家长发 2–4 张孩子的照片和一段话（上周去动物园……），我们把孩子画成系列画风的卡通角色，和栗栗一起演一本 8 页的英文启蒙绘本，交付动画视频 + 可打印 PDF + 角色卡。编号 `x`（x00 是虚构孩子的测试集，x01 起是真实单子）。**成品只给这一家，不发账号**；要在账号里展示，另外征得家长同意，且只用卡通画面。

## 0. 红线（在主文件第 1 节之上再加四条）

1. **照片是不满 14 岁孩子的敏感个人信息**。收料前先发同意话术（第 1 节），家长回「同意」再收。照片只放集目录 `photos/`（已 gitignore），只在本机和 Codex 之间传，不传别的服务、不发进聊天、不进 iCloud 相册。
2. **角色卡确认后 7 天内删原照片**：`photo_character.py <集> purge`，微信里的原图也删。仓库里永远只有卡通角色卡（`refs/kid.png` 也被 gitignore，不会推上去）。
3. 不用孩子真名全名，用小名或英文名；`profile.json`、`characters.json`、`character_draft.json` 都不进仓库（.gitignore 已写）。
4. 成品标 AI 生成（片尾卡和 PDF 版权页一行小字）；画面里不画家长的脸（背影、手可以）。

## 1. 收料（家长 → `episodes/x<NN>-<slug>/`）

同意话术（私信发，家长回「同意」即可）：

> 我是孩子的监护人，同意把发给你的照片只用于制作这一本专属绘本：照片只用来生成卡通形象，生成后 7 天内删除原照片，不用于其他用途、不用于训练模型、不对外公开。成品归我所有；如果要在栗栗学英语账号展示成品里的卡通画面，会另外征得我同意。

要收的东西，填进 `profile.json`（模板 [episodes/x01-zoo/profile.example.json](../episodes/x01-zoo/profile.example.json)）：

- 照片 2–4 张：正脸 1 张（光线好、不戴口罩）、全身 1 张（看衣服和比例）；放 `photos/`。
- 一段话：发生了什么、在哪、孩子最喜欢哪一下、说过什么话。越具体越好，真实细节是这本书比模板书好看的全部理由。
- 小名 / 英文名、年龄、性别；想学的 3 个词（可以我们定）；要不要栗栗客串（默认要）。
- 同意的日期和出处写进 `consent`。

## 2. 照片 → 角色卡（`tools/storybook-video/photo_character.py`，在用户 Mac 上跑）

```bash
cd ~/code/little-circle/tools/storybook-video
python3 photo_character.py ../../episodes/x01-zoo describe     # 看照片写英文外貌描述 → character_draft.json，人工核一遍发型/衣服颜色/标志物
python3 photo_character.py ../../episodes/x01-zoo cards -n 3   # 3 版角色卡候选 → refs/candidates/，contact.jpg 左照片右候选
python3 photo_character.py ../../episodes/x01-zoo pick 2       # 选定：refs/kid.png、characters.json、cast.json、refs/avatars/kid.png
python3 photo_character.py ../../episodes/x01-zoo purge        # 家长确认角色卡后：删原照片和缩略缓存
```

- **像不像是这条线的生死线**。候选拼图发给家长挑（替代口语线的漫画剧本确认），家长说「像」才往下走；三版都不像就改 `character_draft.json` 的 `desc`（最常见：发型长度、刘海、衣服颜色写错）再 `cards --force`。
- `keep` 里只放对称的、每页都在的东西（发型、衣服颜色、眼镜、帽子）。单边细节（一只发卡、一只耳环）会换边，不要写进 keep，画面里也别指望它。
- 角色登记在集目录 `characters.json`，剧本里写 `[[kid]]`，`codex_images.py` 会自动展开描述、带 `refs/kid.png`、附 KEEP 和身高（2 岁≈Pip 的 1.2 倍、3 岁 1.45、4 岁 1.7；Bruno 2.6）。系列角色的参考图照旧在 `series/refs/`。
- 孩子的声音先借系列童声（女孩 bun、男孩 hazel，`profile.json` 的 `voice_like` 可改），写在集目录 `cast.json`；正式产品再用 `el_prep.py cast` 按性别设计两个童声。不克隆孩子真声。
- 字幕旁头像：`story.json` 的 `style.avatar_dir` 写 `["refs/avatars", "../../series/refs/avatars"]`（sbv.py 11-04 起支持一串目录）。
- 测试或演示不想用真人：`photo_character.py <集> fake` 会虚构一个孩子出两张假「生活照」（x00 就是这么跑的）。

## 3. 写剧本（和口语线的差别）

结构照口语分册第 2 节：钩子 → 8 页 → 3 页今日单词复习 → 片尾；台词规则照第 3 节（每句 3–5 词、每页 ≤2 句、全片 12–14 句）。专属绘本不发账号，总长 50–55 秒也可以，但别拖。不一样的地方：

- **真实经历是骨架，AI 只补细节**。家长那段话里的每个具体细节（躲在后面、羊舔手、笑了半天）都要进画面或台词，这是家长看到会鼻酸的地方；AI 补的是起承（怎么到的、前面看了什么）和一个小转折。不要把真实经历改成模板故事。
- **张力小一点就够**：一个「不敢 → 看朋友做 → 自己做到」或「找不到 → 找到」的小勇敢，谷在 p05、峰在 p07。不要吓人，不要失败三次。
- **孩子是第一人称主角**，台词大多是孩子说的（`Wow! So tall!` `I can feed the sheep!`），栗栗是陪伴和示范；最后一页由孩子对镜头说一句带今日词的话。
- **今日单词从经历里来**（giraffe / elephant / feed），复习页复用故事里的图，家长日常能用。
- 动物、场所直接写在提示词里（不是系列角色，不用 `[[ ]]`）；场所写泛称，不写真实园名；家长不入画。
- 剧本文件格式同口语线（`script.md` 第 4 节出图提示词、关键帧 `**p02b.png** ← p02.png`），范例 [episodes/x00-demo/script.md](../episodes/x00-demo/script.md)。
- 画风默认系列日系手绘；家长选别的画风时放 `style.json`（写法同 m02），角色卡要在那个画风下重出（`cards --force`）。

## 4. 出图、配音、渲染、质检（照常）

```bash
python3 codex_images.py ../../episodes/x01-zoo --check          # [[kid]] 要能认出来、参考图要在
python3 codex_images.py ../../episodes/x01-zoo -j 2             # 主图 → 关键帧，出完看 qc/characters.jpg
source .venv/bin/activate && export PATH=~/Downloads/Anaconda3/anaconda3/envs/sbv-ffmpeg/bin:$PATH
python sbv.py ../../episodes/x01-zoo/story.json --out ../../out/x01   # mp4、srt、A4 打印 PDF
python qa.py ../../episodes/x01-zoo/story.json ../../out/x01/<name>.mp4 --dur 45 58
python brand.py ../../episodes/x01-zoo/story.json --ribbon 专属绘本 --tagline "<小名>的专属英文绘本 · 中英字幕" --crop-3x4 0 --title-en "Mia's Zoo Day" --title-zh 米娅的动物园 --words giraffe=长颈鹿 elephant=大象 feed=喂 --out ../../out/x01
```

质检在主文件第 9 节和口语分册第 8 节之上加一关：**每张图里孩子像不像角色卡**（发型、衣服颜色、keep 里的细节），`qc/characters.jpg` 逐张看，不像的 `--only pXX --force` 重出；出完抽 3 张给家长看一眼再渲染。

## 5. 交付

成品包：`<name>.mp4`、`<name>_print.pdf`、`<name>.srt`、3:4 封面、`refs/kid.png`（角色卡，家长可留作头像）。交付页照主文件第 8 节做 artifact 页，**只发给这一家**，不同步到账号的 OSS 公开目录。交付时顺带问三件事：愿意付多少、要不要实体书、下一本想做什么场景（规划第 3 节）。记一行 `tracking/orders.csv`（日期、年龄段、场景、是否付费、要不要实体书，不记姓名联系方式）。

## 6. 第一条推广演示视频（11 月目标）

一条 60–90 秒的录屏加口播，结构在规划文档第 3 节：先给成品 3 秒 → 拖入照片（打码或背影）+ 打一句话 → 角色卡「变身」→ 翻页 + 一段动画 → 打印版 → 号召评论「想要」。素材全部来自 x01 的成品；女儿照片怎么出现由用户定（推荐打码 + 卡通）。不出现微信号、二维码、网址；发布勾 AI 生成声明。

## 7. 已知坑

- `photo_character.py describe` 依赖 `codex exec -o` 把最后一条回复写到文件，老版本 Codex CLI 没有这个参数时会退回从 stdout 里找 JSON；两个都不行就先 `codex update`。
- **发色**（x00）：黑发孩子 describe 常写 dark brown，角色卡就画成中棕，一眼不像。对着照片核，近黑就改成 `near-black`，keep 里写 `almost black, not brown`，再 `cards --force`。
- **手持物不进 desc**（x00）：照片里拿着的玩具写进去，孩子每页都拿着，和牵手、喂东西冲突。describe 提示词已禁；desc 句尾的句号也自动去掉（`[[kid]]` 嵌在句子中间）。
- **复习页别用 `[clearly]`**（x00）：v3 念成 "Ahem, giraffe!" "Mm-hmm elephant"，混音里 qa 还可能听不出来。复习词 `say` 不写标签。`[gasps]` 开口前有约 0.8 秒吸气，句首要对字幕时换 `[excited]`。
- **qa 发音报警先单独听缓存 wav**：`out/<集>/.cache/*.wav` 逐句听写，能分清配音错还是混音窗口误报。qa 现在对不达标的句子会去掉 VAD 和 prompt 重听。
- **看总览图的孩子脸**（x00）：`motion: right/left` 会把靠边的孩子推出画面，qa 查不到。孩子靠边的页用 `"motion": "in"` + `focus` 对准她。
- **3:4 封面**：孩子站得高时中文标题压头发，加 `--crop-3x4 0.1`。
- **AI 标识要自己写**：story.json 顶层 `"ai_note": "本书画面和配音由 AI 生成"`（PDF 封面底部），片尾写进 `ending.subline`。qa 不查这一项。
- ElevenLabs key 没有读账户用量的权限（`/v1/user/subscription` 返回 401），字符数只能按文本估。
- Codex 一次最多 5 张附图：画风样张 2 张 + 照片最多 3 张。照片超过 3 张时只取前 3 张，把正脸和全身放前面。
- **只有脸部裁剪照时 describe 会编衣服**（x01）：它把照片边上的装饰写成衣服细节，发色也写深一档。衣服、发色由人写进 `desc`；`CARD_ASK` 写的是"照片里的衣服"，所以 `notes` 里要写明照片只看脸和头发、衣服以文字为准。
- **角色卡第一轮常见的偏差是头发太厚、眼睛太圆**（x01）：系列画风会把稀疏的婴儿发画成一头蓬发，把杏仁眼画圆。发量、发际线、发色的冷暖、眼型都写具体，再在 `notes` 里写一遍反面。`cards -n 6` 只补 4–6，不覆盖前三版，方便两轮一起比。
- **挑角色卡把头部放大和照片并排看**：contact.jpg 全身图太小，看不出发际线和眼型。系列规定不画睫毛，候选带睫毛的不选。
- **`contact.jpg` 左边是真实照片，绝不上传**（x01）：交付页的候选对比只放 `refs/candidates/kid_N.png` 的缩略图，发布前逐个核对目录里没有带照片的文件。
- **幼儿别写 grin、squished**（x01）：p01b 写 "squished happy grin" 画成露齿咧嘴、脸压变形。写 "small open-mouthed baby smile with no teeth showing"，再写一句脸保持原样。关键帧里人物贴边时，提示词写明整个头在画面内、离边缘远。
- **封面**（x01）：专属绘本用 `brand.py --ribbon 专属绘本`，不用 `--ep`；默认底部小字是「3岁+」，孩子更小时用 `--tagline` 换掉。`script.md` 里有「封面关键画面」就会自动出 `cover.png`，构图取自最后一页、顶部留天空，比用主图当 `--key-art` 好，标题不会盖住动物；`--crop-3x4 0` 让中文标题离开头发。
- **qa 发音报警要看干净 wav**（x01）：混音里被听错的句子，单听缓存 wav 多半是对的；干净 wav 也听错才算真错。"A tiger! Roar!" 的 Roar 在干净 wav 里听成 Run，`say` 写成 `ROAR!` 后听写正确。
- **改 story.json 别用 json.dump 整体重写**：格式全变，diff 几百行。用正则或 sed 只改数值。
