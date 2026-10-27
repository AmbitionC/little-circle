---
name: kids-english-story-video
description: Make one publish-ready episode of the 栗栗学英语 (Forest Friends) toddler English video — themed script, Codex CLI images, Kling hook, ElevenLabs voices, sbv.py render, covers and publishing pack — with a quality gate and self-fix at every stage, in the fixed series style.
---

# 栗栗学英语 · 森林小伙伴 · 幼儿英语启蒙动态绘本

用户（Haoo）在做面向 3–6 岁（主打 3 岁左右）的原创英语启蒙绘本短视频，竖版发抖音（主）、小红书（辅）、视频号。商业路线是：短视频 → 粉丝群 → 卖电子绘本 / 打印包。

这份 skill 记录每一集从剧本到发布的固定做法。**最终产物是能直接发布的成品包**（第 8 节），不是样片或半成品：用户确认剧本之后，Claude 一路做完，每一步过质检关口（第 9 节），不合格自己修，只把成品和极少数只有用户能做的事交给用户。第 1 集《Nutty's Big Acorn》（2026-10-21，全程可灵）2 秒跳出率 66.7%、完播率 1.6%，所以从 2026-10-22 起改成**混合方案**：开头 5 秒可灵钩子 + 其余页面用 `sbv.py` 做动态绘本。下文以混合方案为准。

全程用简体中文跟用户沟通，说大白话，给能直接复制的命令，一次只给要做的那几步。

## 0. 开工前必做

1. 工作都在仓库 `AmbitionC/little-circle` 里做（用户本机是 `~/code/little-circle`）。**先读 `HANDOFF.md`**，看当前进度、ElevenLabs 档位、`series/cast.json` 里 Voice ID 填了没有。
2. 需要时再读：`docs/brand.md`（账号、角色、简介、平台分工）、`docs/elevenlabs-workflow.md`（配音流程和交付标准）、`tools/storybook-video/README.md`（story.json 全部字段）、`milestones/M1-*.md`（本月判据和每周节奏）。仓库文档和本 skill 冲突时，**以仓库里更新日期更近的为准**，并在汇报里说一句。
3. 看本文第 11 节的剧集表和 `tracking/videos.csv`，避免主题、单词、句型重复。
4. 做完一段工作，回去更新 `HANDOFF.md`。改动直接提交并推送到默认分支，不开分支、不走 PR。

## 1. 红线（每集都检查）

- **不要让用户把 API key 发进聊天。** key 在用户 Mac 的 `~/.zshrc`（`ELEVENLABS_API_KEY`）。Voice ID 不是密钥，可以发、可以提交。Codex 用的是用户自己的 ChatGPT 登录（`~/.codex/auth.json`），不要读、不要贴。
- **仓库是公开的**，不提交：key；生成的音频（`assets/sfx/`、`assets/bgm/`、`out/` 已忽略）；孩子或买家的个人信息（`tracking/sales.csv` 只写匿名摘要）。
- 不搬运有版权的绘本、角色、歌曲。全部原创 + AI 出图。
- 抖音、小红书上**不出现微信号、二维码、网址**，谐音和暗号也不行。简介、字幕、片尾卡、评论区都算。
- 发布时勾选"内容由 AI 生成"声明。孩子不出镜。
- **ElevenLabs 免费档生成的音频不能商用。** 要发布的配音、音效、音乐必须在付费订阅期间生成；订阅后先删 `out/.cache`，音效、音乐用 `el_prep.py sfx --force`、`bgm --force` 重做。
- 订阅、付款、充值灵感值都由用户自己操作。批量花积分前先跟用户确认。
- 能力边界：**绘本页图片由 Claude 在用户 Mac 上调本机 Codex CLI 出**（第 5 节），可灵钩子见第 5.4 节：能自动就自动，不能就给用户一份可直接照填的网页操作单。其余环节照做，不等它。

## 2. 系列规范（每集不变）

| 项目 | 规范 |
| --- | --- |
| 账号名 | **栗栗学英语**（三个平台统一） |
| 系列名 | 森林小伙伴；合集分「认知小绘本」「森林故事」 |
| 主角团 | 栗栗 Nutty 红松鼠（绿色针织围巾，抱大栗子）、Hazel 小刺猬（黄色小背带裤，老实可爱、有点害羞的小男孩）、Bun 小灰兔（红色小背心，软萌慢半拍）；旁白是温柔女声。每集可加一个新朋友 |
| 角色参考图 | `series/refs/nutty.png`、`hazel.png`、`bun.png`（Codex 出的全身设定图；2026-10-27 按新画风重出）。出图时自动带上，整季不换；用户定了新头像就替换这几个文件 |
| 画幅 | 竖版 9:16，1080×1920，30fps，H.264，AAC |
| 画风 | 精致数字绘本插画（2026-10-27 起，替换原来的水彩手绘）：毛发细腻蓬松，大而亮的圆眼睛带高光，圆滚滚的萌系比例，表情开心夸张；阳光明媚的森林，苔藓、蕨类、小野花、红顶蘑菇，暖金色阳光加柔和光斑；颜色明亮饱和，边缘干净，细节丰富。不要水彩纸纹、不要粗笔触 |
| 结构 | [可选 0.4 秒静止封面] → 可灵钩子 5 秒（第 1 帧就叠给家长看的大字标题）→ 绘本页 → 片尾卡 3.5 秒（最后 0.6 秒淡出）。**不再做 3 秒片头**（它占掉了决定去留的前 2 秒） |
| 每集两版 | 推荐流精华版：`--max-pages 4`，约 20–35 秒，停在悬念上，片尾写"完整版在主页合集"；完整版：进合集，供搜索和睡前跟读 |
| 配音 | 全英文。只从 `series/cast.json` 读音色（ElevenLabs），整季不换。旁白慢速温暖，角色音高拉开 |
| 字幕 | 中英双语，奶油色圆角底板。英文在上 70px、按角色上色；中文在下 42px、棕灰色；当前词浅橙高亮底 #FFDD9E。中心 y=1640，被抖音底部文案挡住就上调到约 1450（`style.subtitle_center`） |
| 字体 | 英文 Fredoka SemiBold；中文 Noto Sans CJK SC（ttc index 2）。Mac 上没装时 sbv.py 自动换 Arial Rounded / 苹方 |
| 色板 | 奶油 #FFF8E8、棕 #5C3418、浅棕 #6E543E、橙 #E8892B、叶绿 #7A9A4A |
| 角色字幕色 | 旁白 #4A3426 (74,52,38)、Nutty #B24E16 (178,78,22)、Hazel #A06800 (160,104,0)、Bun #AC382C (172,56,44) |
| 角标 | 故事段左上角 (24,40) 半透明系列徽章，72% 透明度；钩子和片尾不放 |
| 转场 | 页间 0.35 秒叠化；冲击镜头用 `cut: true` 硬切 |
| 背景音乐 | `assets/bgm/` 三首整季复用：bgm_play 俏皮 / bgm_calm 安静 / bgm_happy 庆祝；有人说话时自动压低一半 |
| 响度 | -16 LUFS（±1），峰值不超过 -1.5 dBFS |
| 更新 | 每周二、四、六 19:00 |
| 成本 | 单条现金 ≤20 元（可灵每集约 120 灵感值，最多 2 个片段）；出图走用户 ChatGPT 订阅额度，不另花钱；第 3 周起单条制作 ≤3 小时；当月总现金 ≤300 元 |

系列徽章文字用 **「栗栗学英语」**（2026-10-27 定）：视频角标写 `"badge_text": "栗栗学英语 · 森林故事"`（或 `· 认知小绘本`），封面徽章由 `brand.py` 画。仓库示例里的旧名 "Forest Friends English · 森林小伙伴英语" 不再用。

## 3. 每集都要有一个主题（2026-10-26 用户定的硬要求）

用户原话："你做的是视频，要有一个主题，不是纯互动，要么教一个词和派生词，串成一个剧本，要么就是教一个道理。" 所以**不再做"一页一问一答"的认知卡片**。两个合集都按同一种写法，区别只在主题：

- **认知小绘本**：一个主线词或一组词（水果、数数、颜色、天气……）放进一件小事里。例：c01 栗栗越吃越饿 → 吃成球滚下山（hungry / full）；c03 Hazel 滚进落叶堆变成彩色"树叶怪"（颜色）。
- **森林故事**：一个道理（求助、分享、打喷嚏捂嘴、排队……），用一个主线词讲出来。例：s02 用 help 讲"遇到困难要开口"。
- 最好两者合一：一个道理，靠一个主线词讲出来；主线词全片出现 5 次以上，带上它的变化（help me / I can help / helper）。

**固定结构**：可灵钩子 5 秒 → 8 页动态绘本（`p01.png`…`p08.png`）→ 片尾 3.5 秒。完整版约 40–55 秒；`--max-pages 4` 出 20–35 秒的推荐流精华版，**停在悬念上**（例："Hazel 喊出 Help，谁会来帮他？"）。

- 起（p01–p02）：主角遇到问题或想要一样东西。
- 承（p02–p04）：自己搞不定、出糗，笑点最密。
- 转（p04–p06）：换个做法，或朋友来了。
- 合（p06–p08）：解决，大家一起笑；最后一页主角对镜头说一句寓意，再接旁白 `The end. Bye-bye!`。

每集 3 个"今日单词"（封面、评论区置顶、发布文案都用这 3 个）。对标依据见仓库 `docs/benchmark-story-2026-10.md`（小猪佩奇 Muddy Puddles、Little Blue Truck、Dear Zoo、鸽子系列、嘟嘟英语绘本馆）。

需要角色真的动起来的高潮页，可以再出一个 5 秒可灵片段（kling02），每集最多两个。**sbv.py 目前还不支持把视频片段当某一页插入**，要用的话先补这个功能，或者把高潮动作直接放进钩子。

## 4. 写剧本

**英文台词**（用户明确要求，最重要；观众按 **2–3 岁** 写）：

- 全片 **11–13 句**，每句 **3–5 个词**，每页最多两句。宁可少，不要多。
- 是简单完整的短句，不要一两个词的碎片（"Mine!" 太单薄），也不要长句。
- 只用幼儿高频词。每集重复 1–2 个句型，比如 `Help me, please!` / `I can help!`。叫声、数数这种重复的词只重复两三遍。
- 例子：`My red ball! It's stuck!` `Help! Help me, please!` `I can help, too!` `One, two, three... push!` `I am full! No more!`

**互动长在剧情里**：每集一处让宝宝喊出来、找出来、做出来的时刻，比如替害羞的 Hazel 喊 "Help!"、在画里找偷胡萝卜的栗栗、一起捂嘴。在旁白那句加 `"gap": 1.5` 留出时间。不要单独做"旁白提问 → 等抢答 → 回答"的循环。

**童趣**（用户每集都会问）：每 2–3 页一个**看画面就懂**的笑点，最好一集有一个能让孩子笑出声的反转。好用的：摔进泥里 / 落叶堆、东西大得抱不住、吃成球滚下山、刺"嘭"地全炸开、喷嚏把朋友吹飞、耳朵当伞被风吹走、角色故意说错让宝宝纠正。不要靠语言理解的梗。写完在 script.md 概要里单列一行"童趣"，逐条写出来。

**钩子大字标题**（写给家长看，不是给孩子）：一句话说清"孩子能得到什么"或戳中家长场景，12 字以内。例："3岁宝宝认水果，跟栗栗说英文""孩子不肯分享？今晚讲这个"。副标题固定类似"3岁英语启蒙 · 中英字幕"。每 5 集一批，只改一个变量时，钩子标题就是最常改的那个。

**剧本 md 的固定章节**（`episodes/<编号>-<slug>/script.md`）：

1. 标题 + 一行规格（片型、主题、观众、时长、页数、今日单词）
2. 一句话剧情 + 出场角色 + 核心句型
3. 钩子：大字标题、副标题、旁白问句、**可灵首帧出图提示词（放在代码块里）**、可灵尾帧、可灵提示词
4. 分页表（页 | 画面 | 台词 `speaker: English / 中文` | 运镜 | 音效）
5. 出图提示词（第 5 节）
6. 配音清单
7. 发布文案（第 10 节）

**出图脚本靠格式读提示词，下面两条必须照写**，否则那张图出不来：

- 每页写成一行 `**p01.png**`，紧跟一个 ``` 代码块，里面只放英文提示词。
- 可灵首帧写在"可灵首帧出图提示词"这几个字后面的代码块里。
- 有"封面关键画面"这一段时，脚本会用最后一页的提示词自动出一张上方留空的 `cover.png`。

用户的习惯：剧本改动时只发更新后的文件；**没让渲染就不要重新渲染**。

## 5. 出图（Codex CLI，Claude 在用户 Mac 上直接跑）

### 5.1 统一风格词（每条提示词末尾都加）

```
polished digital children's picture book illustration, richly detailed soft fluffy fur with fine strands, big glossy round eyes with bright catchlights, chubby cute proportions, joyful expressive faces, lush sunlit forest with moss, ferns, little wildflowers and red-capped mushrooms, warm golden sunlight with soft bokeh, bright saturated warm colors, crisp clean edges, high detail, no text, no watermark, vertical 9:16
```

**画风样张**：用户给的样张放在 Mac 的 `series/style/`（只留本机，`.gitignore` 已忽略，不进公开仓库）。`codex_images.py` 每出一张图都会把样张排在最前面发给 Codex，并告诉它"只学画风，不抄角色和构图"。换画风就换这个文件夹里的图。**画风变了，`series/refs/` 的角色参考图要先用 `codex_images.py refs --force` 重出**，否则旧参考图会把画风拉回去。

页面图再加 `keep the bottom quarter of the image simple and free of faces`（下方四分之一留给字幕，脸放在 y<1450）。

### 5.2 角色固定描述（出现角色名时原文替换，一个字都别改）

- Nutty: `a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf`
- Hazel: `a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls`
- Bun: `a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest`

**出图脚本靠这几句原文认角色**：提示词里出现哪句，就自动把 `series/refs/` 里对应的参考图一起发给 Codex，锁住长相。改了一个字就认不出来，参考图也就不会带上。

### 5.3 怎么出（`tools/storybook-video/codex_images.py`）

原理：脚本对每张图调一次 `codex exec`（用户的 ChatGPT 登录，内置 `image_gen` 工具，不用 OpenAI API key），带上参考图，等图落到 `~/.codex/generated_images/<thread>/` 就收工，再裁成 1080×1920 存进集目录，同时在 `images.json` 记下原图路径和提示词指纹。

```bash
cd ~/code/little-circle/tools/storybook-video
python3 codex_images.py refs                                  # 只在没有参考图、或用户要换角色长相时跑
python3 codex_images.py ../../episodes/c01-fruits             # 出一集：p01–p06、kling_first.png、cover.png
python3 codex_images.py ../../episodes/c0[1-3]-* -j 3         # 多集一起，3 张并行
python3 codex_images.py ../../episodes/c01-fruits --only p02,p05 --force   # 只重出这两张
```

- 已有的图跳过；某张图的提示词在 script.md 里改了，再跑一遍会**只重出那一张**。`--force` 全部重出。
- 网络好时一张约 1.5–3 分钟；用户家里连 OpenAI 常断（Broken pipe），实测 10 张要 1 小时以上。按这个估时间，放后台跑，跑完再汇报。
- 日志在集目录的 `.codex_images.log`。
- 出完抽几张缩小拼图看一遍（角色像不像参考图、下方四分之一有没有脸、有没有乱入文字），不行的用 `--only … --force` 重出，再把结果拼图发给用户挑。

**踩过的坑**（2026-10-24）：

- Codex CLI 太旧（0.142）时，服务器会报"model is not supported / requires a newer version"。先跑 `codex update`，再 `codex exec --skip-git-repo-check "reply with just: ok"` 验证。
- `-i` 后面能跟多个文件，会把提示词也吞掉，导致报 "No prompt provided"。脚本已改成提示词从 stdin 传（参数写 `-`）。
- 网络抖动时 Codex 出完图还会一直重连、不退出。脚本已改成看到图落盘就结束进程。
- 用户 `~/.codex/config.toml` 里的 MCP 服务会报 403 / AuthRequired，是噪音，不影响出图。
- （2026-10-26）多角色图连续失败：三张 2.6MB 参考图一起上传，网络一抖就断。脚本已改成先缩成 768px JPEG 再传。第一轮失败的图用 `-j 2` 重跑。

### 5.4 可灵钩子

- 只做 `kling01.mp4`：图生视频，**5 秒、9:16、1080p、不开原生音频**（原生音频贵 50%，配音由脚本做）。
- 首帧用脚本出的 `kling_first.png`，**尾帧用 `p01.png`**，钩子结束正好落在第 1 页，衔接最顺。
- 提示词用中文，末尾统一加"精致数字绘本插画风格（毛发细腻、大眼睛、暖色阳光），保持角色外形和颜色不变，动作轻柔、幅度小"；负面提示词"变形，多余肢体，脸部扭曲，画面闪烁，写实风格，文字，水印"。
- 首帧图不带字幕和大字，大字由 sbv.py 叠。
- **可灵没有 CLI。** 官方接法是远程 MCP `kling-ai`（`https://kling.ai/mcp/plugin`，OAuth）。它连的是**国际版** kling.ai，跟国内版的账号和灵感值不通用。2026-10-27 实测：国际版余额为 0；不开会员只能出 720p；可灵 4.0 支持首尾帧，不出原生音频；负面提示词没有单独参数，要写进提示词里。
- 所以现在的做法是：用户在**国内版网页**上手动生成，Claude 给一份操作单（首帧、尾帧路径，5 秒，9:16，1080p，关音频，提示词和负面提示词原文），文件存成 `episodes/<集>/kling01.mp4`。用户以后会试着用国内账号登录 MCP，登不上就改走国内开放平台 API：key 放在 `~/.zshrc`，脚本只从环境变量读。**不读、不打印 key。**
- 先用占位开头把其余部分做成成品；kling01.mp4 到位后，抽帧质检，再重渲。
- 每集最多生成 3 次（约 120–360 灵感值）。超过 3 次还不合格，停下来跟用户说。
- **sbv.py 在 `hook.clip` 文件不存在时会报错停下**。可灵还没做好时，用首帧图做一个 5 秒占位（`kling_first.png` 缓推 4 秒 + 叠化到 `p01.png` 1 秒），另存一份临时 story.json 把 `hook.clip` 指过去，先把其余质检做完；`kling01.mp4` 一到，用正式 story.json 重渲、重跑 `qa.py`。占位版不能发布。
  ```bash
  ffmpeg -y -loop 1 -t 5 -i kling_first.png -loop 1 -t 5 -i p01.png -filter_complex "[0]scale=2160:3840,zoompan=z='1+0.08*on/150':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=150:s=1080x1920:fps=30[a];[1]scale=1080:1920,fps=30[b];[a][b]xfade=transition=fade:duration=1:offset=4,format=yuv420p" -t 5 hook_placeholder.mp4
  ```

## 6. 写 story.json

放在 `episodes/<编号>-<slug>/story.json`（认知短片 c01、c02…，剧情片 s01…；例如 `episodes/c01-fruits/`），图和 `kling01.mp4` 放同目录。字段全集见 `tools/storybook-video/README.md`，常用骨架：

```jsonc
{
  "output_name": "c01_fruits",
  "title_en": "Yummy Fruits", "title_zh": "好吃的水果",
  "series": {"badge_text": "栗栗学英语 · 认知小绘本", "badge_alpha": 0.72},
  "style": {"speaker_colors": {"narrator": [74,52,38], "nutty": [178,78,22], "hazel": [160,104,0], "bun": [172,56,44]}},
  "cast": "../../series/cast.json",
  "hook": {"clip": "kling01.mp4", "max_seconds": 5,
           "headline": "3岁宝宝认水果，跟栗栗说英文", "subline": "3岁英语启蒙 · 中英字幕",
           "say": {"speaker": "narrator", "en": "What does Nutty have?", "at": 0.6}},
  "pages": [
    {"image": "p01.png", "motion": "in", "focus": [0.5, 0.6], "lines": [
      {"speaker": "narrator", "en": "Look! What is it?", "zh": "看！这是什么？", "gap": 1.2},
      {"speaker": "nutty", "en": "It's a red apple!", "zh": "是红苹果！"},
      {"speaker": "nutty", "en": "I like red apples!", "zh": "我喜欢红苹果！"}
     ],
     "sfx": [{"file": "../../assets/sfx/chomp.mp3", "at": 2.4, "gain": 0.55}]}
  ],
  "ending": {"headline": "See you next time! 下集见！", "subline": "收藏起来，今晚讲给宝贝听", "seconds": 3.5,
             "feed_headline": "完整版在主页合集", "feed_subline": "认知小绘本 · 第1集"},
  "bgm": {"file": "../../assets/bgm/bgm_play.mp3", "volume": 0.25},
  "loudness": {"I": -16, "TP": -1.5}
}
```

要点：

- `motion` 每页轮换（in / out / left / right / up / down），`focus` 对准角色或道具（占原图宽高的比例）。图出好后看一眼主体位置再调 `focus`。
- `say` 是送去配音的文本，字幕只显示 `en`。**sbv.py 会把 `say` 原样发给配音引擎，不会剥掉方括号标签。** 所以 `[excited]` 这类语气标签只能用在 `cast.json` 里 `model` 是 `eleven_v3` 的角色上；现在 cast.json 是 `eleven_multilingual_v2`，Kokoro 样片也一样，加了标签会被念出来或读怪。没用 v3 时，语气靠标点（! ? …）和 `cast.json` 的 stability / style 调。用 v3 时如果不返回时间戳，脚本会退回普通接口、高亮按能量估算。
- `gap` 是这句之后的停顿（默认 0.4 秒），`hold` 是整页说完后多停几秒。
- 某句要重录：加 `"take": 2`，其他句子不动。
- 某句要小声（害羞、说悄悄话）：加 `"gain": 0.4`，只降这句的音量。multilingual_v2 不认语气标签，光靠标点做不出"小声"（s02 第 3 页实测和大喊一样响）。
- 音效别和台词第一个词撞在一起：页面 `lead` 默认 0.5 秒开口，音效放在 0.3 秒前结束，或放到这句说完之后（s02 第 4 页树叶声原来盖住了 "Help!"）。
- 可选：`cover`（钩子前 0.4 秒静止封面帧，可以直接用脚本出的 `cover.png`）、`cut`、`hold`、`zoom`、`parallax`（2.5D 视差，需深度模型）、`fx`（glow / snow / motes，坐标按图标注）。
- 音效文件名见 `docs/elevenlabs-workflow.md` 1.3 节：pop、bonk、crack、whoosh、sparkle、ding、boing、chomp、tummy、snore、leaves、page、jingle_in、jingle_out（`.mp3`）。
- 背景音乐没有时（音乐接口要付费档）：`python3 tools/storybook-video/make_bgm.py assets/bgm/bgm_play.wav 60` 先顶上。
- 写完用 `python3 -c "import json;json.load(open('story.json'))"` 校验，再数一遍每句英文是 3–5 个词、全片 11–13 句。

## 7. 配音与渲染（在用户 Mac 上跑）

一次性准备（ElevenLabs 选角、音效、音乐、cast.json）按 `docs/elevenlabs-workflow.md` 第 1 节和 `el_prep.py` 做，进度看 `HANDOFF.md`。`cast.json` 的 Voice ID 还是"填XXX"、或者还在免费档时，不能出发布版，只能出**样片**，并明说样片不能发布（Kokoro 变调后音质差，已否决用于发布；edge 是非官方接口）。出样片用 Kokoro 音色表，不改 story.json：

```bash
python sbv.py ../../episodes/c01-fruits/story.json --out ../../out/c01 --cast ../../series/cast_kokoro.json
```

（`--cast` 参数和 `series/cast_kokoro.json` 是 2026-10-24 新加的；仓库里还没有的话，先看 `git log` 确认有没有推上来。）

每集出片：

```bash
cd ~/code/little-circle/tools/storybook-video && source .venv/bin/activate   # .venv 用 /usr/bin/python3（3.9）建；终端里的 python3 是 Anaconda 3.7，太旧
export PATH=~/Downloads/Anaconda3/anaconda3/envs/sbv-ffmpeg/bin:$PATH        # 这台 Intel Mac 上 brew 装不了 ffmpeg，用 conda 环境里的（带 loudnorm，不带 rubberband）
python sbv.py ../../episodes/c01-fruits/story.json --out ../../out/c01               # 完整版
python sbv.py ../../episodes/c01-fruits/story.json --out ../../out/c01 --max-pages 4 # 推荐流精华版
open ../../out/c01
```

- 配音按"文本 + 音色"缓存在 `out/.cache`，改剧本只重配改过的句子，不重复扣费。
- 输出：mp4、srt、A4 打印版 PDF（以后做付费打印包用）。
- 渲染耗时约等于片长 2 倍。长任务开始前说一句在做什么，完成后再汇报，不刷屏。
- `sbv.py` 的 ElevenLabs 代码在 HANDOFF 里标着"还没用真实 key 跑过"时，先用 `example/voice_test.json` 跑一句验证，报错先修脚本。

## 8. 确认剧本后一路做到成品（用户的目标）

用户原话："你自己检查下，有问题自己修复掉。我要的是成品。" 只有一个关口要等用户：**剧本确认**。确认之前只改文字，不出图、不渲染。确认之后，Claude 在用户 Mac 上一口气跑完（Remote Control 会话），每一步过第 9 节的质检，不合格自己修，最后只汇报一次。

1. 出图：`python3 codex_images.py ../../episodes/<集> -j 2`，放后台跑。
2. 可灵钩子：按第 5.4 节出 `kling01.mp4`，没到位就先用占位开头。
3. 渲染：完整版和精华版，用正式的 `story.json`。
4. 封面：`python brand.py ../../episodes/<集>/story.json --ep <集数> --words help=帮忙 push=推 ball=球 --out ../../out/<集>`，出 9:16（1080×1920）和 3:4（1080×1440）两张，徽章是"栗栗学英语"（`brand.py` 就是附录 A 的 `make_cover`，字体改成本机能找到的）。
5. 发布包：`out/<集>/publish.txt`（抖音标题、小红书标题、正文、置顶评论），小红书图文用的图放在 `out/<集>/xhs/`。
6. 收尾：脚本修复提交推送；`tracking/videos.csv` 加一行（状态"待发布"、工时、现金成本）；更新 `HANDOFF.md` 和第 11 节剧集表；`open out/<集>`。

**成品包（交付清单）**，都在 `out/<集>/`：

| 文件 | 用途 |
|---|---|
| `<name>.mp4` | 完整版，进合集 |
| `<name>_feed.mp4`（或 sbv 的精华版命名） | 推荐流精华版 |
| `<name>_cover_9x16.jpg`、`<name>_cover_3x4.jpg` | 抖音封面、小红书封面 |
| `publish.txt` | 标题、正文、话题、置顶评论 |
| `xhs/` | 小红书图文 6–9 页 |
| `<name>.srt`、`<name>_print.pdf` | 字幕、打印小绘本（付费包素材） |
| `<name>_sheet.jpg`、`<name>_frame0.jpg` | 质检留底：每页 2 帧总览、第 0 帧（`qa.py` 生成） |

交付时只讲：成品在哪、每项质检结果、自己修了什么、花了多少（可灵次数、配音字符）、还剩什么只有用户能做（手机终检、点发布）。

## 9. 每个环节的质量把控（不合格自己修，修完重检）

| 环节 | 检查什么 | 合格线 | 不合格怎么修 |
|---|---|---|---|
| 剧本 | 主题、结构、台词、童趣、互动 | 有一个主题；8 页起承转合；11–13 句、每句 3–5 词、每页 ≤2 句；每 2–3 页一个笑点；一处互动长在剧情里；角色原文描述一字不差；`codex_images.py` 能读出全部提示词；story.json 能解析 | 改文字，再交用户确认 |
| 出图 | 每张图（拼一张 `qc/images.jpg` 自己看） | 角色像 `series/refs/` 参考图（Hazel：棕刺、黄背带裤男孩）；道具颜色、数量前后一致；笑点动作看得出来；下方四分之一没有脸；没有文字和水印；没有多余肢体；**画风和 `series/style/` 样张一致**（毛发细腻、大眼高光、暖色阳光，不能是水彩纸纹的手绘感） | `--only pXX --force` 重出，最多两轮；还不行就改提示词再出 |
| 可灵 | 抽第 0–4 秒每秒一帧 | 脸不变形、没有多余肢体、不闪、没有文字和水印、道具不凭空消失；结尾能接上 p01 | 改提示词重出，总共 ≤3 次 |
| 配音 | 用 faster-whisper（base.en）把音轨转成文字，逐句对照 en；测每个角色的基频和语速 | 没有读错、漏词、多读；四个角色分得清（相近两个角色的基频差 ≥30Hz，或者语速明显不同）；旁白够慢 | 读错的句子加 `"take": 2` 重录；分不清就调 `cast.json` 的 speed / stability，重录那个角色的句子 |
| 渲染 | ffprobe、ebur128、第 0 帧、每页抽 2 帧拼图（`qc/frames.jpg`） | 1080×1920、30fps；I 在 -16±1 LUFS、Peak ≤ -1.5；第 0 帧是带大字的钩子画面；字幕不挡脸，大字不挡主体，没有黑边；每条字幕出现后 0.6 秒内有人声；完整版 40–55 秒，精华版 20–35 秒 | 调 `focus` / `subtitle_center` / `gap`，然后重渲染 |
| 封面 | 两张封面图 | 标题不压脸；今日单词三个都在；徽章是"栗栗学英语" | 换 key_art 裁切位置，或重出 `cover.png` |
| 发布包 | publish.txt | 没有微信号、二维码、网址（谐音也不行）；带 AI 声明；话题里有"英语启蒙""英文绘本" | 改文案 |

配音和渲染两关用一条命令跑完（在 `tools/storybook-video` 下，ffmpeg 要在 PATH 里，第一次先 `.venv/bin/pip install faster-whisper`）：

```bash
.venv/bin/python qa.py ../../episodes/<集>/story.json ../../out/<集>/<name>.mp4 --dur 40 55
.venv/bin/python qa.py ../../episodes/<集>/story.json ../../out/<集>/<name>_feed.mp4 --dur 20 35 --max-pages 4
```

最后一行写"全部通过"才算过。它查格式、响度、第 0 帧不黑、黑边、Whisper 逐句对照（相似度 ≥0.75）、字幕 0.6 秒内有人声、Hazel 和 Bun 的基频语速、时长；总览图和第 0 帧还要用眼睛看一遍（挡脸只能人看）。另外要听的：剧本里写了"小声""大喊"的句子，音量真的有差别。

**只有用户能做的**：手机终检（前 2 秒、字幕有没有被抖音底部文案挡住、睡前小音量能不能听清），以及点发布、勾 AI 声明。

## 10. 发布与数据

**平台分工**：

| 平台 | 发什么 |
| --- | --- |
| 抖音（主） | 精华版进推荐流；完整版进合集（认知小绘本 / 森林故事）；评论区置顶本集 3 个单词 |
| 小红书（辅） | 图文为主：6–9 页绘本 + 一张单词卡，标题带"3岁英语启蒙""英文绘本"这类搜索词；视频顺手同步。绘本页直接用集目录里的 p01–p06，封面用 cover.png |
| 视频号 | 和抖音同一条视频，勾选原创声明 |

发自己导出的无水印原片，不要把抖音下载的带水印版本发到别处。

**标题**：
- 抖音：钩子大字标题同款，或 `{中文集名}｜3岁英语启蒙绘本动画`
- 小红书（20 字以内）：`{中文集名}｜3岁英语启蒙`

**正文模板**：

```
🌰 {片型合集名}｜{English title} {中文集名}
{一句话：栗栗遇到什么 / 今天认识什么}

📖 今日单词：{word1} {中文}｜{word2} {中文}｜{word3} {中文}
🗣 跟读句子：
{核心句1} {中文}
{核心句2} {中文}

💡 亲子小互动：看完问问宝宝 "{一个问题}"，让宝宝用 "{句型}…" 回答。

#幼儿英语启蒙 #英语启蒙 #儿童英语 #英语绘本 #亲子英语 #{本集主题词}
```

第 1 集示例：

```
🌰 森林故事｜Nutty's Big Acorn 小松鼠的大橡果
小松鼠栗栗捡到一颗大橡果，想自己一个人吃掉，结果咬不动也打不开……最后他学会了和朋友一起分享。

📖 今日单词：acorn 橡果｜share 分享｜hungry 饿
🗣 跟读句子：
It's mine! 它是我的！
Let's share! 我们一起分享吧！

💡 亲子小互动：看完问问宝宝 "What do you have?"，让宝宝用 "I have…" 回答。

#幼儿英语启蒙 #英语启蒙 #儿童英语 #英语绘本 #亲子英语 #学会分享
```

正文、评论、简介里不放微信号、二维码、网址。勾选 AI 生成声明。

**数据**：每条视频每个平台一行记进 `tracking/videos.csv`（日期、平台、标题、题材、时长、本条改动的变量、播放、2 秒跳出率、5 秒完播率、平均播放秒、完播率、点赞、收藏、分享、评论、新增关注、进群人数、现金成本、制作工时）。每 5 集一批，**一次只改一个变量**（钩子标题、长度、发布时间、形式）。M1 判据写在 `milestones/` 里，期中不改。

## 11. 剧集表

| 编号 | 合集 | 英文名 | 中文名 | 主题 | 今日单词 | 核心句 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| s01 | 森林故事 | Nutty's Big Acorn | 小松鼠的大橡果 | 分享 | acorn, share, hungry | It's mine! / Let's share! / Sharing is fun! | 2026-10-21 已发（全程可灵，基线） |
| c01–c05 | 认知小绘本 | Nutty Is Hungry / Where Is My Carrot? / Hazel's Colorful Leaves / Achoo! Cover Your Mouth! / Bun's Rainy Picnic | | 饿和饱、数数、颜色、打喷嚏捂嘴、天气 | 以各目录 script.md 为准 | | 2026-10-26 按新标准重写（一个主题、8 页、约 11 句），等确认后出图 |
| s02 | 森林故事 | Help! Hazel's Red Ball | 小刺猬的红皮球 | 求助（一个词 help 讲一个道理） | help, push, ball | Help me, please! / I can help! / Thank you! | 2026-10-27 成品做完、全部质检通过，只差可灵钩子；10-27 画风改成精致数字绘本插画，重画中；待发布 |

新的一集开始前先看这张表；做完一集就补进来（通过更新这个 skill），同时记进 `tracking/videos.csv`。

## 附录 A：封面和片尾卡（`tools/storybook-video/brand.py`）

封面用仓库里的 `brand.py`，一条命令就能出两张：9:16（1080×1920，抖音封面）和 3:4（1080×1440，小红书封面）。key_art 用集目录里的 `cover.png`，徽章文字是「栗栗学英语」，字体自动找本机的。系列视觉（色板、徽章、集数条、今日单词卡、渐变）都写在这个文件里，改风格只改这一处。

片尾卡由 sbv.py 自己画。想要带三个角色合影的片尾卡，旧版 `make_end_card` 的代码在 git 历史里（2026-10-26 之前的这份文件）：移进 `brand.py`，徽章换成新名，出好的图填进 story.json 的 `ending.image`。

## 附录 B：第 1 集逐帧手工流水线留下的经验（只在 sbv.py 做不到时参考）

第 1 集是用 PIL 逐帧 + 抠图贴角色做的，已被 sbv.py 取代。还有用的几条：

- **抠图**（角色设定图 → 透明 PNG，做片尾卡合影用；`series/refs/` 是纯奶油底，最好抠）：取格子左上角中位数当底色 BG；`diff = |p-BG|.sum(2)`，`diff<42` 且和边框连通的算背景；封闭的纯底色洞（`diff<14` 且 >250px）也去掉；只留面积 ≥ 最大块 15% 的连通块，`binary_fill_holes`；alpha 做 3×3 腐蚀 + 0.8 高斯模糊。姿势挨在一起时，先手画排除框把邻居刷成底色。贴进场景前按光线调色：白天 ×(1.0,0.97,0.92)，黄昏 ×(0.95,0.82,0.68)，烛光 ×(0.93,0.82,0.65)。
- **放大**：Codex 出的原图是 941×1672，`codex_images.py` 用 Lanczos + `UnsharpMask` 放到 1080×1920，够用。要更清楚用 opencv-contrib 的 EDSR x3（CPU 上一张 3–6 分钟，放后台跑）。
- **虚化背景**要先按 9:16 裁好再模糊，否则顶部露黑带。
- **相机运动**不能露黑边：缩放下限要保证旋转后的视野仍在画布内，震屏改成移相机。
- **停后台任务**别在命令行里 `pkill -f 脚本名`，会把自己也杀掉；用 PID 或 TaskStop。
- 下载后检查文件大小：几百字节的"模型文件"其实是报错 JSON。
