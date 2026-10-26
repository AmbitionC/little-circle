---
name: kids-english-story-video
description: Make one episode of the 栗栗学英语 (Forest Friends) toddler English video, cognition short or story, from script and story.json to Codex CLI images, Kling hook, ElevenLabs voices, sbv.py render, checks, publishing copy and tracking, in the fixed series style.
---

# 栗栗学英语 · 森林小伙伴 · 幼儿英语启蒙动态绘本

用户（Haoo）在做面向 3–6 岁（主打 3 岁左右）的原创英语启蒙绘本短视频，竖版发抖音（主）、小红书（辅）、视频号。商业路线是：短视频 → 粉丝群 → 卖电子绘本 / 打印包。

这份 skill 记录每一集从剧本到发布的固定做法。第 1 集《Nutty's Big Acorn》（2026-10-21，全程可灵）2 秒跳出率 66.7%、完播率 1.6%，所以从 2026-10-22 起改成**混合方案**：开头 5 秒可灵钩子 + 其余页面用 `sbv.py` 做动态绘本。下文以混合方案为准。

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
- 能力边界：**绘本页图片由 Claude 在用户 Mac 上调本机 Codex CLI 出**（第 5 节），不用再让用户手动出图；可灵钩子视频还是用户在可灵里做（除非接了可灵 MCP）。

## 2. 系列规范（每集不变）

| 项目 | 规范 |
| --- | --- |
| 账号名 | **栗栗学英语**（三个平台统一） |
| 系列名 | 森林小伙伴；合集分「认知小绘本」「森林故事」 |
| 主角团 | 栗栗 Nutty 红松鼠（绿色针织围巾，抱大栗子）、Hazel 小刺猬（黄色小背带裤，老实可爱、有点害羞的小男孩）、Bun 小灰兔（红色小背心，软萌慢半拍）；旁白是温柔女声。每集可加一个新朋友 |
| 角色参考图 | `series/refs/nutty.png`、`hazel.png`、`bun.png`（2026-10-24 用 Codex 出的全身设定图）。出图时自动带上，整季不换；用户定了新头像就替换这几个文件 |
| 画幅 | 竖版 9:16，1080×1920，30fps，H.264，AAC |
| 画风 | 水彩 + 水粉绘本插画，手绘笔触，纸纹，暖光，复古童书感 |
| 结构 | [可选 0.4 秒静止封面] → 可灵钩子 5 秒（第 1 帧就叠给家长看的大字标题）→ 绘本页 → 片尾卡 3.5 秒（最后 0.6 秒淡出）。**不再做 3 秒片头**（它占掉了决定去留的前 2 秒） |
| 每集两版 | 推荐流精华版：`--max-pages 3`，约 20–40 秒，片尾写"完整版在主页合集"；完整版：进合集，供搜索和睡前跟读 |
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

系列徽章的文字以 `docs/brand.md` 为准。仓库示例里还是旧名 "Forest Friends English · 森林小伙伴英语"；用户还没定新徽章文字前，照旧用它，并在交付时提醒一句。

## 3. 两种片型

### 3.1 认知小绘本（M1 主力，依据：对标账号最火的是"切蔬菜"这类认知内容）

- 一个主题一集：水果、数数、颜色、身体部位、天气、动物、食物……
- 可灵钩子 5 秒 + 6 页（`p01.png`…`p06.png`），每页一个词，一张图一个主角动作。完整版约 40 秒，`--max-pages 3` 精华版约 20 秒。
- 固定页序：
  1. 钩子（可灵 5 秒）：最抓眼的画面，比如栗栗咬一口超大苹果。旁白一句问题："What does Nutty have?"
  2. 第 1–5 页，每页三拍：**旁白提问 → 停约 1 秒等宝宝抢答（在提问句上加 `"gap": 1.2`，`gap` 是这句说完后的停顿）→ 角色回答**。同一个句型重复，例如 `What is it?` → `It's a red apple! I like apples!`。颜色、数数穿插进去。
  3. 第 6 页复习：几样东西同框一起念一遍，再向屏幕前的宝宝提问（比如 `What do you like?`），最后旁白 `The end. Bye-bye!`
- 每集 3 个"今日单词"（封面、评论区置顶、发布文案都用这 3 个）；如果一集超过 3 个词，挑最重要的 3 个当今日单词。

### 3.2 森林故事（剧情片，对照组）

- 起承转合四段，8–12 页（混合方案下不再做 17–19 个镜头），每页 4–6 秒。
  - 起：认识主角，出现想要的东西或遇到问题。
  - 承：主角做了不太对的选择（独占、害怕、偷懒），连续吃瘪。
  - 转：看到朋友或明白道理，改变主意。
  - 合：大家一起解决，温暖收尾。最后一句由主角对镜头说寓意，再接旁白 `The end. Bye-bye!`。
- 需要角色真的动起来的高潮页，可以再出一个 5 秒可灵片段（kling02），每集最多两个。**sbv.py 目前还不支持把视频片段当某一页插入**，要用的话先补这个功能，或者把高潮动作直接放进钩子。

## 4. 写剧本

**英文台词**（用户明确要求，最重要）：

- 每句都是**简单完整的英文短句，3–8 个词**。不要只有一两个词的碎片（"Mine!" "Ouch!" 太简单），也不要长句。
- 只用幼儿高频词。每集重复 2–3 个句型，比如 It's… / I have… / I like… / Let's… / I can…。
- 穿插颜色（red berries, orange carrot）、数数（One, two, three!）和拟声词。
- 核心句至少出现两次。
- 例子：`Wow! Look at this big, big acorn!` `It's mine! Mine, mine, mine!` `Ouch! It's too hard for my teeth!` `Come in, friends! Let's share!` `I have an orange carrot!` `Sharing is fun! Let's share with friends!`

**童趣**：每 10 秒左右一个看画面就懂的小笑点：摔进落叶堆、东西大得藏不住、卡门口 POP 一声挤进去、咬到牙、肚子咕噜叫、吓得躲起来、吃撑睡着打呼噜。不要靠语言理解的梗，三岁孩子听不懂。

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
watercolor and gouache children's picture book illustration, hand-painted brush strokes, visible paper grain, soft warm light, cozy vintage storybook feel, no text, no watermark, vertical 9:16
```

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
- 一张约 1.5–3 分钟。24 张 3 并行约 15–20 分钟，放后台跑，跑完再汇报。
- 日志在集目录的 `.codex_images.log`。
- 出完抽几张缩小拼图看一遍（角色像不像参考图、下方四分之一有没有脸、有没有乱入文字），不行的用 `--only … --force` 重出，再把结果拼图发给用户挑。

**踩过的坑**（2026-10-24）：

- Codex CLI 太旧（0.142）时，服务器会报"model is not supported / requires a newer version"。先跑 `codex update`，再 `codex exec --skip-git-repo-check "reply with just: ok"` 验证。
- `-i` 后面能跟多个文件，会把提示词也吞掉，导致报 "No prompt provided"。脚本已改成提示词从 stdin 传（参数写 `-`）。
- 网络抖动时 Codex 出完图还会一直重连、不退出。脚本已改成看到图落盘就结束进程。
- 用户 `~/.codex/config.toml` 里的 MCP 服务会报 403 / AuthRequired，是噪音，不影响出图。

### 5.4 可灵钩子

- 只做 `kling01.mp4`：图生视频，**5 秒、9:16、1080p、不开原生音频**（原生音频贵 50%，配音由脚本做）。
- 首帧用脚本出的 `kling_first.png`，**尾帧用 `p01.png`**，钩子结束正好落在第 1 页，衔接最顺。
- 提示词用中文，末尾统一加"水彩绘本插画风格，保持角色外形和颜色不变，动作轻柔、幅度小"；负面提示词"变形，多余肢体，脸部扭曲，画面闪烁，写实风格，文字，水印"。
- 首帧图不带字幕和大字，大字由 sbv.py 叠。
- 可灵目前还是用户手动做：把每集的 `kling_first.png`、`p01.png` 和 script.md 里的可灵提示词交给用户，导出的视频命名 `kling01.mp4` 放回集目录。用户想让 Claude 直接调可灵，只能在 claude.ai 把可灵的远程 MCP 加成自定义连接器（Customize > Connectors > "+ Add" > "Add custom connector"）。
- **sbv.py 在 `hook.clip` 文件不存在时会报错停下**。可灵还没做好又想先看样片，就临时把 story.json 的 `hook` 删掉。

## 6. 写 story.json

放在 `episodes/<编号>-<slug>/story.json`（认知短片 c01、c02…，剧情片 s01…；例如 `episodes/c01-fruits/`），图和 `kling01.mp4` 放同目录。字段全集见 `tools/storybook-video/README.md`，常用骨架：

```jsonc
{
  "output_name": "c01_fruits",
  "title_en": "Yummy Fruits", "title_zh": "好吃的水果",
  "series": {"badge_text": "Forest Friends English · 森林小伙伴英语", "badge_alpha": 0.72},
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
- 可选：`cover`（钩子前 0.4 秒静止封面帧，可以直接用脚本出的 `cover.png`）、`cut`、`hold`、`zoom`、`parallax`（2.5D 视差，需深度模型）、`fx`（glow / snow / motes，坐标按图标注）。
- 音效文件名见 `docs/elevenlabs-workflow.md` 1.3 节：pop、bonk、crack、whoosh、sparkle、ding、boing、chomp、tummy、snore、leaves、page、jingle_in、jingle_out（`.mp3`）。
- 背景音乐没有时（音乐接口要付费档）：`python3 tools/storybook-video/make_bgm.py assets/bgm/bgm_play.wav 60` 先顶上。
- 写完用 `python3 -c "import json;json.load(open('story.json'))"` 校验，再数一遍每句英文是 3–8 个词。

## 7. 配音与渲染（在用户 Mac 上跑）

一次性准备（ElevenLabs 选角、音效、音乐、cast.json）按 `docs/elevenlabs-workflow.md` 第 1 节和 `el_prep.py` 做，进度看 `HANDOFF.md`。`cast.json` 的 Voice ID 还是"填XXX"、或者还在免费档时，不能出发布版，只能出**样片**，并明说样片不能发布（Kokoro 变调后音质差，已否决用于发布；edge 是非官方接口）。出样片用 Kokoro 音色表，不改 story.json：

```bash
python sbv.py ../../episodes/c01-fruits/story.json --out ../../out/c01 --cast ../../series/cast_kokoro.json
```

（`--cast` 参数和 `series/cast_kokoro.json` 是 2026-10-24 新加的；仓库里还没有的话，先看 `git log` 确认有没有推上来。）

每集出片：

```bash
cd ~/code/little-circle/tools/storybook-video && source .venv/bin/activate
python sbv.py ../../episodes/c01-fruits/story.json --out ../../out/c01               # 完整版
python sbv.py ../../episodes/c01-fruits/story.json --out ../../out/c01 --max-pages 3 # 推荐流精华版
open ../../out/c01
```

- 配音按"文本 + 音色"缓存在 `out/.cache`，改剧本只重配改过的句子，不重复扣费。
- 输出：mp4、srt、A4 打印版 PDF（以后做付费打印包用）。
- 渲染耗时约等于片长 2 倍。长任务开始前说一句在做什么，完成后再汇报，不刷屏。
- `sbv.py` 的 ElevenLabs 代码在 HANDOFF 里标着"还没用真实 key 跑过"时，先用 `example/voice_test.json` 跑一句验证，报错先修脚本。

## 8. 确认后自动跑完（用户的目标）

用户确认了剧本和提示词，就由 Claude 在用户 Mac 上一口气跑完，中间不再找用户，只在两处停：**可灵钩子**（用户手动做）和**交付前手机终检**。

1. 确认关口：用户说"剧本 / 提示词确认"之前，只改文字，不出图、不渲染。
2. 出图：`python3 codex_images.py ../../episodes/<集> [<集>…] -j 3`，放后台。跑完拼一张缩略图自检，不合格的单张重出。
3. 把缩略拼图发给用户看一眼，同时把每集的 `kling_first.png`、`p01.png`、可灵提示词交给用户做 `kling01.mp4`。
4. 用户说图可以、`kling01.mp4` 放进目录后，渲染完整版和精华版（第 7 节），跑第 9 节的检查。
5. 交付：mp4 + 发布文案 + 封面图，记 `tracking/videos.csv`，更新 `HANDOFF.md` 和第 11 节剧集表，提交推送（图片可以提交，音频和 `out/` 不提交）。

## 9. 交付前检查（每集必做）

1. 格式：`ffprobe -v error -show_entries stream=width,height,r_frame_rate -of compact out/c01/xxx.mp4` → 1080×1920、30fps。
2. 响度：`ffmpeg -nostats -i out/c01/xxx.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:"` → I ≈ -16，Peak ≤ -1.5。
3. 第 1 帧：必须是带完整大字标题的钩子画面（或封面帧），不能是黑场。
4. 抽帧看一遍：字幕没盖住角色的脸，大字没挡住主体，没有黑边。
5. 逐句听（对照 `docs/elevenlabs-workflow.md` 第 3 节）：四个角色分得清、没读错、旁白够慢、高亮和发音对得上（抽查 3 句）。
6. **手机终检**（请用户做）：前 2 秒、字幕有没有被抖音底部的作者名和文案挡住、睡前小音量下能不能听清。
7. 交付时说清 3–5 个要点（素材是哪来的、配音用的哪档、可以替换的地方），不逐步复述过程。

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
| c01 | 认知小绘本 | Nutty's Fruit Basket | 栗栗的水果篮 | 水果 | apple, banana, orange | Look! What is this? / It's a/an … | 2026-10-24 剧本好了，Codex 出图中 |
| c02–c03 | 认知小绘本 | c02-carrots Bun 数胡萝卜、c03-colors Hazel 认颜色 | | | 以各目录 script.md 为准 | | 2026-10-24 剧本好了，Codex 出图中 |
| c04–c05 | 认知小绘本 | c04-body 身体部位、c05-weather 天气 | | | 以各目录 script.md 为准 | | 2026-10-24 剧本好了，还没出图 |
| c06 | 认知小绘本 | Who Says Moo? | 谁在哞哞叫 | 动物和叫声（Hazel 主演） | cow, duck, sheep | Listen! Who says …? / It's a …! | 2026-10-26 剧本好了，等确认后出图 |

新的一集开始前先看这张表；做完一集就补进来（通过更新这个 skill），同时记进 `tracking/videos.csv`。

## 附录 A：brand.py（封面图和片尾卡图的独立绘制代码）

sbv.py 已内置字幕卡、角标和片尾卡。下面这份用于另外出**封面图**（9:16 视频封面 + 3:4 小红书封面 1080×1440，`make_cover(key_art, ep, title_en, title_zh, words, size)`，`key_art` 用集目录里的 `cover.png`）和带角色合影的**片尾卡图**（`make_end_card`，出图后填进 story.json 的 `ending.image`）。字体路径按本机改。

```python
import functools, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FREDOKA = 'fonts/Fredoka.ttf'
NOTO, NOTO_MED = ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
                  '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc')
BRAND = dict(series_en='Forest Friends English', series_zh='森林小伙伴英语',
    tagline_zh='幼儿英语启蒙 · 中英字幕 · 3岁+',
    cream=(255, 248, 232), cream_txt=(255, 246, 222), brown=(92, 52, 24), brown_soft=(110, 84, 62),
    orange=(232, 137, 43), green=(122, 154, 74), ink=(60, 30, 10),
    speaker={'narrator': (74, 52, 38), 'nutty': (178, 78, 22), 'hazel': (160, 104, 0), 'bun': (172, 56, 44)})
W, H = 1080, 1920

def fr(size, weight='Bold'):
    f = ImageFont.truetype(FREDOKA, size); f.set_variation_by_name(weight); return f
def zh(size, medium=False):
    return ImageFont.truetype(NOTO_MED if medium else NOTO, size, index=2)

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
    f1, f2 = fr(int(40*scale), 'SemiBold'), zh(int(32*scale))
    t1, t2 = BRAND['series_en'], BRAND['series_zh']; w1, w2 = f1.getlength(t1), f2.getlength(t2)
    ic, gap = int(46*scale), int(18*scale)
    w, h = int(ic+gap+w1+gap*2+3+w2+gap*3), int(78*scale)
    im = pill(w, h, BRAND['cream'], (232, 214, 186)); x, cy = 15+gap*1.4, 15+h/2
    im.alpha_composite(leaf_icon(ic, BRAND['green']), (int(x), int(cy-ic/2)))
    d = ImageDraw.Draw(im); x += ic+gap
    d.text((x, cy), t1, font=f1, fill=BRAND['brown'], anchor='lm'); x += w1+gap
    d.line([(x, cy-h*.25), (x, cy+h*.25)], fill=(214, 190, 160), width=3); x += gap
    d.text((x, cy+2*scale), t2, font=f2, fill=BRAND['brown_soft'], anchor='lm')
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

def make_cover(key_art, ep, title_en, title_zh, words, size=(W, H)):
    cw, ch = size; k = max(cw/key_art.width, ch/key_art.height)
    art = key_art.convert('RGBA').resize((int(key_art.width*k), int(key_art.height*k)), Image.LANCZOS)
    oy, ox = int((art.height-ch)*0.55), (art.width-cw)//2
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

def make_end_card(lineup, next_en=None, next_zh=None):
    """lineup: [(rgba_cutout, x_fraction, height_px), ...]；主角放中间、最后画。"""
    cv = Image.new('RGBA', (W, H), BRAND['cream']+(255,)); rng = np.random.default_rng(1)
    noise = Image.fromarray((rng.normal(0, 1, (H//4, W//4))*18+128).clip(0, 255).astype('uint8')).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3))
    tex = Image.new('RGBA', (W, H), (190, 150, 100, 0)); tex.putalpha(noise.point(lambda v: max(0, v-118)*3)); cv.alpha_composite(tex)
    cv.alpha_composite(gradient((W, H), 0, 120, (232, 190, 130), int(H*0.55), H))
    paste_c(cv, series_badge(), W/2, 150)
    paste_c(cv, text_block('See you next time!', fr(104), BRAND['cream_txt'], 12, BRAND['brown'], 14), W/2, 430)
    paste_c(cv, text_block('下集见！', zh(70), BRAND['orange'], 0, None, 6), W/2, 560)
    if next_en:
        paste_c(cv, pill(int(max(fr(44, 'SemiBold').getlength('Next: '+next_en), zh(32, True).getlength(next_zh or ''))+90), 130, BRAND['cream'], (232, 214, 186)), W/2, 720)
        paste_c(cv, text_block(f'Next: {next_en}', fr(44, 'SemiBold'), BRAND['orange']), W/2, 700)
        paste_c(cv, text_block(next_zh or '', zh(32, True), BRAND['brown_soft']), W/2, 748)
    ground = Image.new('L', (W, 200), 0); ImageDraw.Draw(ground).ellipse([90, 60, W-90, 150], fill=120)
    g = Image.new('RGBA', (W, 200), (120, 80, 40, 0)); g.putalpha(ground.filter(ImageFilter.GaussianBlur(25))); cv.alpha_composite(g, (0, 1600))
    for sp, xf, h in lineup:
        im = sp.resize((int(sp.width*h/sp.height), h), Image.LANCZOS)
        cv.alpha_composite(im, (int(W*xf-im.width/2), int(1715-im.height)))
    paste_c(cv, text_block(BRAND['tagline_zh'], zh(30, True), BRAND['brown_soft']), W/2, 1810)
    return cv.convert('RGB')
```

## 附录 B：第 1 集逐帧手工流水线留下的经验（只在 sbv.py 做不到时参考）

第 1 集是用 PIL 逐帧 + 抠图贴角色做的，已被 sbv.py 取代。还有用的几条：

- **抠图**（角色设定图 → 透明 PNG，做片尾卡合影用；`series/refs/` 是纯奶油底，最好抠）：取格子左上角中位数当底色 BG；`diff = |p-BG|.sum(2)`，`diff<42` 且和边框连通的算背景；封闭的纯底色洞（`diff<14` 且 >250px）也去掉；只留面积 ≥ 最大块 15% 的连通块，`binary_fill_holes`；alpha 做 3×3 腐蚀 + 0.8 高斯模糊。姿势挨在一起时，先手画排除框把邻居刷成底色。贴进场景前按光线调色：白天 ×(1.0,0.97,0.92)，黄昏 ×(0.95,0.82,0.68)，烛光 ×(0.93,0.82,0.65)。
- **放大**：Codex 出的原图是 941×1672，`codex_images.py` 用 Lanczos + `UnsharpMask` 放到 1080×1920，够用。要更清楚用 opencv-contrib 的 EDSR x3（CPU 上一张 3–6 分钟，放后台跑）。
- **虚化背景**要先按 9:16 裁好再模糊，否则顶部露黑带。
- **相机运动**不能露黑边：缩放下限要保证旋转后的视野仍在画布内，震屏改成移相机。
- **停后台任务**别在命令行里 `pkill -f 脚本名`，会把自己也杀掉；用 PID 或 TaskStop。
- 下载后检查文件大小：几百字节的"模型文件"其实是报错 JSON。
