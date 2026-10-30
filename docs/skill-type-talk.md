# 类型一：口语线（有配音、有台词的动画绘本）

> 系列 skill 的分册。公共部分（红线、系列规范、出图、漫画剧本确认、渲染、成品交付、发布）在 [skill-kids-english-story-video.md](skill-kids-english-story-video.md)，这里只写口语线和儿歌线不一样的地方。2026-10-29 从主文件拆出来，原有规则原样搬过来，新加了子类表（含待试的生活口语）。

**口语线是什么**：角色说台词、旁白讲故事，声音靠 ElevenLabs 配音 + 背景音乐 + 音效。编号 `s`（森林故事）、`c`（认知小绘本）、`d`（生活口语，待试）。

## 1. 三个子类：选题不同，做法相同

| 子类 | 编号 · 合集 | 一集教什么 | 选题从哪来 | 写法上的差别 | 例子 |
|---|---|---|---|---|---|
| 森林故事 | `s` · 森林故事 | 一个道理，靠一个主线词讲出来 | 孩子的情绪和品格：求助、勇敢、分享、排队、认错 | **张力第一**（第 4 节）：有利害、失败一次比一次糟、最弱的上场、有一下"要完了" | s02 help、s04 brave |
| 认知小绘本 | `c` · 认知小绘本 | 一组同类词（4–6 个） | 水果、颜色、数数、身体、天气、动物 | 词靠"阶梯 + 后果 + 变身"串起来（《好饿的毛毛虫》骨架，`docs/script-craft-global-hits.md` 1.5）；张力可以弱一点，但一定要有一个能笑出声的反转；每个词至少出现 2 次、配一个画面 | c01 hungry/full、c03 颜色 |
| 生活口语（待试） | `d` · 栗栗的一天（暂定） | 一句家长每天都能对孩子说的话 | 一日流程：起床、洗手、吃饭、穿鞋、刷牙、收玩具、出门、睡觉 | 核心句是家长能直接拿来用的祈使句或一问一答（`Wash your hands!` / `All clean!`），全片出现 4 次以上；剧情是角色**不肯做 → 出糗 → 自己想做**；家长任务写成"今天在家也这么说一次" | 还没做 |

**选题从哪来、怎么挑、哪天发**：上表只是各子类的方向；具体来源（含国内外节日、在线搜的热点）、筛选标准、不重复规则、选题库和每周排期见 [skill-topics.md](skill-topics.md)。

**为什么加生活口语**〔分析〕：家长最常见的需求是"在家怎么跟孩子说英语"，这类内容能直接用进生活，最容易让家长收藏、进群，也最接近以后要卖的打印包（日常口语卡）。CoComelon、Super Simple 的大量爆款都是日常流程（洗澡、收玩具、刷牙）。先做 1 集试，数据比故事集差就停。

**合一更好**：一个道理 + 一个主线词，或者一个生活场景 + 一句核心句。子类只决定选题从哪来，下面的结构、台词、配音规则三类都一样。

## 2. 固定结构

可灵或关键帧钩子 5 秒 → 8 页动态绘本（`p01.png`…`p08.png`）→ 片尾 3.5 秒。完整版约 40–55 秒，只出完整版（2026-10-29 用户定，不出精华版）。

- 起（p01–p02）：主角遇到问题或想要一样东西。
- 承（p02–p04）：自己搞不定、出糗，笑点最密。
- 转（p04–p06）：换个做法，或朋友来了。
- 合（p06–p08）：解决，大家一起笑；最后一页主角对镜头说一句寓意，再接旁白 `The end. Bye-bye!`（结尾怎么收可以参考 `docs/script-craft-global-hits.md` 1.10 的勋章仪式，按选题挑）。

每集 3 个"今日单词"（封面、评论区置顶、发布文案都用这 3 个）。对标依据见 `docs/benchmark-story-2026-10.md`（小猪佩奇 Muddy Puddles、Little Blue Truck、Dear Zoo、鸽子系列、嘟嘟英语绘本馆）。

需要角色真的动起来的高潮页，可以再出一个 5 秒可灵片段（kling02），每集最多两个。**sbv.py 目前还不支持把视频片段当某一页插入**，要用的话先补这个功能，或者把高潮动作直接放进钩子。

## 3. 台词

**英文台词**（用户明确要求，最重要；观众按 **2–3 岁** 写）：

- 全片 **11–13 句**，每句 **3–5 个词**，每页最多两句。宁可少，不要多。（参考：s02 全片 28 个不同的词、s04 30 个。）
- 台词是写来让孩子喊、让角色演的：短、带感叹号、带角色性格（`I am big! I can do it!`），不要描述句（`The bear climbs the tree.`），画面会说的不用台词说。
- 是简单完整的短句，不要一两个词的碎片（"Mine!" 太单薄），也不要长句。
- 只用幼儿高频词。每集重复 1–2 个句型，比如 `Help me, please!` / `I can help!`。叫声、数数这种重复的词只重复两三遍。
- 例子：`My red ball! It's stuck!` `Help! Help me, please!` `I can help, too!` `One, two, three... push!` `I am full! No more!`

**互动长在剧情里**：每集一处让宝宝喊出来、找出来、做出来的时刻，比如替害羞的 Hazel 喊 "Help!"、在画里找偷胡萝卜的栗栗、一起捂嘴。在旁白那句加 `"gap": 1.5` 留出时间。不要单独做"旁白提问 → 等抢答 → 回答"的循环。

## 4. 张力第一（森林故事必须，其他两类尽量）

2026-10-28 用户否掉 s03："一点波澜都没有"。困境要让人揪心，不能只是"困了""饿了"这种小不适。要有利害（谁有危险、会失去什么）、有阻碍升级（前两次尝试更糟）、有最弱的人被推到台前、有一下"要完了"的惊险，然后马上安全解决。写完问自己：家长看到第 3 页会不会想知道"然后呢"。

认知小绘本和生活口语的"利害"可以小一点（吃成球滚下山、鞋子穿反摔一跤），但一定要有"然后呢"。

## 5. 剧本 md 的固定章节

`episodes/<编号>-<slug>/script.md`：

1. 标题 + 一行规格（子类、主题、观众、时长、页数、今日单词）
2. 一句话剧情 + 出场角色 + 核心句型；概要里写"三句话""选题打分""情绪曲线""家长任务""用了哪些手法""童趣"（范例 `episodes/s04-brave/script.md`）
3. 钩子：大字标题、副标题、旁白问句、首帧出图提示词（代码块）、关键帧或可灵提示词
4. 分页表（页 | 画面 | 台词 `speaker: English / 中文` | 运镜 | 音效）
5. 出图提示词（主文件第 5 节）
6. 配音清单
7. 发布文案（主文件第 10 节）

## 6. 写 story.json

放在 `episodes/<编号>-<slug>/story.json`，图和 `kling01.mp4` 放同目录。字段全集见 `tools/storybook-video/README.md`，常用骨架：

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

钩子用关键帧时把 `clip` 换成 `frames`（主文件 5.3.1）。要点：

- `motion` 每页轮换（in / out / left / right / up / down），`focus` 对准角色或道具（占原图宽高的比例）。图出好后看一眼主体位置再调 `focus`。
- `say` 是送去配音的文本，字幕只显示 `en`。每句都要写 `say`，带语气标签（第 7 节）。`sbv.py` 对齐字幕时会去掉 `[...]` 标签。标签只在 `eleven_v3` 下有用；退回 `cast_v2.json`（multilingual_v2）或 Kokoro 样片时标签会被念出来，要先把 `say` 删掉。v3 不返回时间戳时，脚本会退回普通接口，高亮按能量估算。
- `gap` 是这句之后的停顿（默认 0.4 秒），`hold` 是整页说完后多停几秒。
- 某句要重录：加 `"take": 2`，其他句子不动。
- 某句要小声（害羞、说悄悄话）：`say` 里写 `[whispers]`，再加 `"gain": 0.6` 兜底，只降这句的音量（s02 第 3 页用 multilingual_v2 时，小声和大喊一样响）。
- 音效别和台词第一个词撞在一起：页面 `lead` 默认 0.5 秒开口，音效放在 0.3 秒前结束，或放到这句说完之后（s02 第 4 页树叶声原来盖住了 "Help!"）。
- 可选：`cover`（钩子前 0.4 秒静止封面帧，可以直接用脚本出的 `cover.png`）、`cut`、`hold`、`zoom`、`parallax`（2.5D 视差，需深度模型）、`fx`（glow / snow / motes，坐标按图标注）。
- 音效文件名见 `docs/elevenlabs-workflow.md` 1.3 节：pop、bonk、crack、whoosh、sparkle、ding、boing、chomp、tummy、snore、leaves、page、jingle_in、jingle_out（`.mp3`）。
- 背景音乐没有时（音乐接口要付费档）：`python3 tools/storybook-video/make_bgm.py assets/bgm/bgm_play.wav 60` 先顶上。
- 写完用 `python3 -c "import json;json.load(open('story.json'))"` 校验，再数一遍每句英文是 3–5 个词、全片 11–13 句。

## 7. 配音要有情绪起伏（原主文件 6.1 节；2026-10-28 用户反馈"没有张力，平铺直叙"）

- `cast.json` 四个角色都用 `eleven_v3`。v3 的 stability 只能是 0.0、0.5、1.0：旁白 0.5（稳、但有起伏），三个角色 0.0（最有表现力）。v3 报错或 Hazel 和 Bun 分不清时，退回 `series/cast_v2.json`（multilingual_v2，stability 压到 0.25–0.35，style 拉到 0.55–0.7），同时去掉 `say` 里的标签。
- **每句都写语气标签**，写在 `say` 开头或句中：`[excited]` `[gasps]` `[whispers]` `[shouting]` `[laughs]` `[giggles]` `[sighs]` `[happily]` `[sadly]` `[curious]` `[warmly]`。
- 一集里要有**对比**：至少一处"小声 → 大喊"（如 s02 第 3 页 `[whispers] Help... help me, please.` 接第 4 页 `[shouting] Help! Help me, please!`），一处数数或蓄力（`[excited] One, two, three... [shouting] push!`），结尾 `[laughs]` 或 `[warmly]` 落下来。
- 旁白不是播音腔，是讲故事：钩子用 `[gasps]` 起，转折处放慢加省略号，高潮提速提音量。
- 标点也算数：`...` 拉长停顿，`!` 提音量，`?` 上扬；`en` 里不用写标签，字幕保持干净。
- 质检要听：钩子第一句有没有"抓人"；小声和大喊音量差 ≥6 dB；整集听下来有没有两句以上读成一个调。

配音准备（选角、音效、音乐、cast.json）按 `docs/elevenlabs-workflow.md` 第 1 节和 `el_prep.py` 做。`cast.json` 的 Voice ID 还是"填XXX"、或者还在免费档时，不能出发布版，只能出**样片**，并明说样片不能发布（Kokoro 变调后音质差，已否决用于发布；edge 是非官方接口）：

```bash
python sbv.py ../../episodes/c01-fruits/story.json --out ../../out/c01 --cast ../../series/cast_kokoro.json
```

配音按"文本 + 音色"缓存在 `out/.cache`，改剧本只重配改过的句子，不重复扣费。

## 8. 质检（口语线独有的几关，公共几关见主文件第 9 节）

| 环节 | 检查什么 | 合格线 | 不合格怎么修 |
|---|---|---|---|
| 剧本 | 主题、结构、台词、童趣、互动 | 选题打分 ≥14、三句话写得出来、情绪曲线谷在 p03 峰在 p07（`docs/story-psychology-reference.md` 第 9 节自检）；概要里写了这一集从 `docs/script-craft-global-hits.md` 挑了哪些手法；漫画剧本网页做好、每格和剧本对得上；有一个主题；8 页起承转合；11–13 句、每句 3–5 词、每页 ≤2 句；每 2–3 页一个笑点；一处互动长在剧情里；角色原文描述一字不差；`codex_images.py` 能读出全部提示词；story.json 能解析 | 改文字，再交用户确认 |
| 可灵 | 抽第 0–4 秒每秒一帧 | 脸不变形、没有多余肢体、不闪、没有文字和水印、道具不凭空消失；结尾能接上 p01 | 改提示词重出，总共 ≤3 次 |
| 配音 | 用 faster-whisper（base.en）把音轨转成文字，逐句对照 en；测每个角色的基频和语速 | 没有读错、漏词、多读；角色分得清（相近两个角色的基频差 ≥30Hz，或者语速明显不同）；旁白够慢；小声和大喊差 ≥6 dB | 读错的句子加 `"take": 2` 重录；分不清就调 `cast.json` 的 speed / stability，重录那个角色的句子 |

`qa.py` 跑完整版（`--dur 40 55`），命令见主文件第 9 节。

## 9. 发布

- 抖音：完整版进对应合集（森林故事 / 认知小绘本 / 栗栗的一天）。
- 正文模板和示例见主文件第 10 节，`{片型合集名}` 填子类合集名。生活口语的"亲子小互动"写成"今天在家也对宝宝说一次 `{核心句}`"。
