---
name: kids-english-story-video
description: Make one publish-ready episode of the 栗栗学英语 (Forest Friends) toddler English video — talk line (story / word / daily-phrase episodes with ElevenLabs voices) or song line (AI nursery song with word cards) — themed script, comic review, Codex CLI images and keyframes, sbv.py render, covers and publishing pack, with a quality gate and self-fix at every stage, in the fixed series style.
---

# 栗栗学英语 · 森林小伙伴 · 幼儿英语启蒙动态绘本

用户（Haoo）在做面向 3–6 岁（主打 3 岁左右）的原创英语启蒙绘本短视频，竖版发抖音（主）、小红书（辅）、视频号。商业路线是：短视频 → 粉丝群 → 卖电子绘本 / 打印包。

这份 skill 记录每一集从剧本到发布的固定做法。**最终产物是能直接发布的成品包**（第 8 节），不是样片或半成品：用户确认剧本之后，Claude 一路做完，每一步过质检关口（第 9 节），不合格自己修，只把成品和极少数只有用户能做的事交给用户。第 1 集《Nutty's Big Acorn》（2026-10-21，全程可灵）2 秒跳出率 66.7%、完播率 1.6%，所以从 2026-10-22 起改成**混合方案**：开头 5 秒可灵钩子 + 其余页面用 `sbv.py` 做动态绘本。下文以混合方案为准。

**2026-10-29 起按视频类型分册**（用户要求把口语类和儿歌类拆开）：本文件只放各类型都一样的公共部分；类型不同的地方写在两个分册里，开工先看第 3 节选类型，再读对应分册：

- 口语线（有配音的故事 / 认知 / 生活口语）→ [skill-type-talk.md](skill-type-talk.md)
- 儿歌线（AI 儿歌 + 卡片）→ [skill-type-song.md](skill-type-song.md)。**2026-10-30 起暂停**（用户："儿歌流程先停掉"），用户说恢复之前不做新儿歌

**做哪一集、哪天发**（选题来源、筛选、节日热点、选题库、周排期）→ [skill-topics.md](skill-topics.md)，选题库在 `series/topic-bank.md`（2026-10-30 起）。

全程用简体中文跟用户沟通，说大白话，给能直接复制的命令，一次只给要做的那几步。

## 0. 开工前必做

1. 工作都在仓库 `AmbitionC/little-circle` 里做（用户本机是 `~/code/little-circle`）。**先读 `HANDOFF.md`**，看当前进度、ElevenLabs 档位、`series/cast.json` 里 Voice ID 填了没有。
2. 需要时再读：`docs/brand.md`（账号、角色、简介、平台分工）、`docs/elevenlabs-workflow.md`（配音流程和交付标准）、`tools/storybook-video/README.md`（story.json 全部字段）、`milestones/M1-*.md`（本月判据和每周节奏）。仓库文档和本 skill 冲突时，**以仓库里更新日期更近的为准**，并在汇报里说一句。
3. **从选题库领题**（`series/topic-bank.md`，规则见 [skill-topics.md](skill-topics.md)），不临时现想；再看本文第 11 节的剧集表和 `tracking/videos.csv`，避免主题、单词、句型重复。**按第 3 节定这一集是哪条线、哪个子类，读对应分册。**
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
| 其他角色 | 狐狸、小熊、小老鼠、知更鸟、猫头鹰、浣熊、小鹿、獾、水獭……各有一个鲜明性格和一个小标志，轮流当主角（2026-10-28 用户要求不只三个），**设定和出图原文见 `series/characters.md`**；新角色第一次出场前跑 `codex_images.py refs --only <id>` |
| 主角团 | 栗栗 Nutty 红松鼠（绿色针织围巾，抱大栗子）、Hazel 小刺猬（黄色小背带裤，老实可爱、有点害羞的小男孩）、Bun 小灰兔（红色小背心，软萌慢半拍）；旁白是温柔女声。每集可加一个新朋友 |
| 角色参考图 | `series/refs/nutty.png`、`hazel.png`、`bun.png`（Codex 出的全身设定图；2026-10-28 按日系手绘画风重出）。出图时自动带上，整季不换；用户定了新头像就替换这几个文件 |
| 画幅 | 竖版 9:16，1080×1920，30fps，H.264，AAC |
| 画风 | **日系手绘动画**（2026-10-28 用户从 5 组样图里挑定，替换 10-27 的精致数字插画）：干净的赛璐璐上色角色，柔和描边，大而有神的眼睛，圆润可爱的比例；背景是细腻的手绘森林，蓝天白云，光线温暖通透，带点怀旧电影感，颜色清爽明亮。不要 3D 渲染感、不要水彩纸纹、不要厚涂毛发 |
| 结构 | [可选 0.4 秒静止封面] → 钩子 4–5 秒（第 1 帧就叠给家长看的大字标题）→ 绘本页 / 歌词卡 → 片尾卡（最后 0.6 秒淡出）。**不再做 3 秒片头**（它占掉了决定去留的前 2 秒）。各线的页数和时长见分册 |
| 每集几版 | **只出完整版**（2026-10-29 用户：片子本来就三四十秒，精华版没必要），口语线、儿歌线都一样 |
| 声音 | 全英文。口语线：只从 `series/cast.json` 读音色（ElevenLabs），整季不换，**模型用 `eleven_v3`，每句都写语气标签**（口语分册第 7 节），不能平铺直叙。儿歌线：ElevenLabs Music 作曲演唱，同样不能像机器人（儿歌分册第 4 节） |
| 字幕 | 中英双语，**不要底板**（2026-10-28 用户要求：底部会被抖音标题和简介挡住）。`subtitle_mode: outline`：白字加粗描边（英文描边是角色色压暗、中文描边深棕）加柔和阴影，当前词变黄 #FFD640。英文 70px 在上，中文 46px 在下。**中心 y=1320、x=510**（略偏左，躲开抖音右侧点赞栏），最宽 820px。旧的奶油底板还能用 `subtitle_mode: card` 切回 |
| 字体 | 英文 Fredoka SemiBold；中文 Noto Sans CJK SC（ttc index 2）。Mac 上没装时 sbv.py 自动换 Arial Rounded / 苹方 |
| 色板 | 奶油 #FFF8E8、棕 #5C3418、浅棕 #6E543E、橙 #E8892B、叶绿 #7A9A4A |
| 角色字幕色 | 旁白 #4A3426 (74,52,38)、Nutty #B24E16 (178,78,22)、Hazel #A06800 (160,104,0)、Bun #AC382C (172,56,44) |
| 角标 | 故事段左上角 (24,40) 半透明系列徽章，72% 透明度；钩子和片尾不放 |
| 转场 | 页间 0.35 秒叠化；冲击镜头用 `cut: true` 硬切 |
| 背景音乐 | 口语线用 `assets/bgm/` 三首整季复用：bgm_play 俏皮 / bgm_calm 安静 / bgm_happy 庆祝；有人说话时自动压低一半。儿歌线不加 |
| 响度 | -16 LUFS（±1），峰值不超过 -1.5 dBFS |
| 更新 | 2026-10-30 起按周排期，默认每天 19:30 一条口语线（[skill-topics.md](skill-topics.md) 第 1 节）；做不过来退回二、四、六 |
| 成本 | 单条现金 ≤20 元（可灵每集约 120 灵感值，最多 2 个片段）；出图走用户 ChatGPT 订阅额度，不另花钱；第 3 周起单条制作 ≤3 小时；当月总现金 ≤300 元 |

系列徽章文字用 **「栗栗学英语」**（2026-10-27 定）：视频角标写 `"badge_text": "栗栗学英语 · 森林故事"`（或 `· 认知小绘本`），封面徽章由 `brand.py` 画。仓库示例里的旧名 "Forest Friends English · 森林小伙伴英语" 不再用。

## 3. 视频类型：两条线、五个子类（2026-10-29）

**怎么分**：按**声音怎么来**分成两条线，因为这决定了剧本格式、音频流程、时长、版本数和质检，分开写才不会互相干扰；线下面再按**一集教什么**分子类，子类只换选题来源和写法侧重，流程完全复用，不另立 skill。

| 线 | 子类 | 编号 · 合集 | 一集教什么 | 状态 |
|---|---|---|---|---|
| 口语线（[分册](skill-type-talk.md)）：角色说台词、旁白讲故事，ElevenLabs 配音 + 背景音乐 + 音效 | 森林故事 | `s` · 森林故事 | 一个道理（求助、勇敢、分享），靠一个主线词讲出来 | 在做：s02、s04 |
| | 认知小绘本 | `c` · 认知小绘本 | 一组同类词（水果、颜色、身体、天气） | 剧本已写：c01–c05 |
| | 生活口语 | `d` · 栗栗的一天（暂定） | 一句家长每天能对孩子说的话（洗手、穿鞋、收玩具） | 待试 1 集 |
| 儿歌线（[分册](skill-type-song.md)）：一首 AI 儿歌就是全部声音，卡片按小节切 | 单词卡儿歌 | `m` · 栗栗唱儿歌 | 一组词，每张卡一个词 + 一个动作 | **暂停**（10-30），m01 成品保留待发 |
| | 动作儿歌 | `m` · 栗栗唱儿歌 | 一组身体动作或一段日常流程，跟着做 | **暂停**（10-30） |

**为什么只拆这两条线、不拆更细**〔分析〕：头部儿童英语频道（Super Simple、CoComelon、Pinkfong、Peppa、Bluey、嘟嘟英语绘本馆、托比和朋友）的内容基本落在"故事 / 认知 / 日常 / 儿歌 / 动作歌 / 字母拼读"几类里。前四类在制作上其实只有两种：有配音的和唱出来的；认知、日常和故事的差别在选题，不在流程。拆成五份 skill，公共部分要改五处，很快就会漂。

**不做的类型**：
- 字母和自然拼读：适合 4 岁以上，跟 2–3 岁定位不符。
- 一页一问一答的纯单词卡：2026-10-26 用户否掉了（没有主线，留不住人）。
- 朗读现成绘本：有版权，红线。
- 真人出镜跟读：孩子不出镜，主播出镜成本高，也不是我们的强项。

**新子类怎么上**：生活口语和动作儿歌各先做 1 集，和同线的老子类比 2 秒跳出率、完播率、收藏率（记 `tracking/videos.csv`，"本条改动的变量"写子类）。数据不比老子类差才继续，不行就从这张表删掉。

**选题**：每集的题从选题库领，来源（母题、家长烦恼、一日流程、认知词组、国内外节日、在线搜的热点……）、筛选标准、不重复规则和每周排期都在 [skill-topics.md](skill-topics.md)。

**所有类型都要有一个主题**（2026-10-26 用户定的硬要求）。用户原话："你做的是视频，要有一个主题，不是纯互动，要么教一个词和派生词，串成一个剧本，要么就是教一个道理。" 最好两者合一：一个道理，靠一个主线词讲出来；主线词全片出现 5 次以上，带上它的变化（help me / I can help / helper）。

## 4. 写剧本（公共部分；台词、结构、歌词等差异见分册）

**写剧本前先读两份 reference**：`docs/story-psychology-reference.md`（为什么：选题打分、8 页情绪曲线、红线）和 `docs/script-craft-global-hits.md`（怎么写：Bluey、Peppa、Gruffalo、Mo Willems、Eric Carle 等 11 个爆款的写法和 12 条可选手法）。script.md 概要里要有"三句话""选题打分""情绪曲线""家长任务"这几行，范例见 `episodes/s04-brave/script.md`。

`script-craft-global-hits.md` 是**工具箱，不是硬性要求**（2026-10-29 用户原话："并不是硬性要求，还是要和选题搭配，选最适合的"）。每集按选题挑 2–4 条最合适的手法用上（比如能输的规则、先写结尾埋伏笔、三次阶梯、出糗的是大个子），在概要里写一行"用了哪些手法"，不用逐条打勾。

**童趣**（用户每集都会问，两条线都要）：每 2–3 页一个**看画面就懂**的笑点，最好一集有一个能让孩子笑出声的反转。好用的：摔进泥里 / 落叶堆、东西大得抱不住、吃成球滚下山、刺"嘭"地全炸开、喷嚏把朋友吹飞、耳朵当伞被风吹走、角色故意说错让宝宝纠正。不要靠语言理解的梗。写完在 script.md 概要里单列一行"童趣"，逐条写出来。

**钩子大字标题**（写给家长看，不是给孩子）：一句话说清"孩子能得到什么"或戳中家长场景，12 字以内。例："3岁宝宝认水果，跟栗栗说英文""孩子不肯分享？今晚讲这个"。副标题固定类似"3岁英语启蒙 · 中英字幕"。每 5 集一批，只改一个变量时，钩子标题就是最常改的那个。

**出图脚本靠格式读提示词，下面两条必须照写**，否则那张图出不来：

- 每页写成一行 `**p01.png**`，紧跟一个 ``` 代码块，里面只放英文提示词。
- 可灵首帧写在"可灵首帧出图提示词"这几个字后面的代码块里。
- 有"封面关键画面"这一段时，脚本会用最后一页的提示词自动出一张上方留空的 `cover.png`。

用户的习惯：剧本改动时只发更新后的文件；**没让渲染就不要重新渲染**。

### 4.1 漫画剧本：剧本确认前的固定一步（2026-10-28 用户要求）

用户原话："每次和我确认之前，能不能在剧本和分镜的基础上再走一步，生成个漫画剧本，这样我可以更清晰地理解这个故事、角色、细节、分镜和台词。"

所以剧本、分镜和 story.json 写完后，**先出漫画剧本，再找用户确认**：

```bash
cd ~/code/little-circle/tools/storybook-video
python3 codex_images.py ../../episodes/<集> --comic -j 2   # 钩子 + 8 页，每三格一张横版漫画 → episodes/<集>/comic/sheet1-3.png
python3 comic_page.py ../../episodes/<集>                  # 切成单格，配上段落、画面、台词（中英）、音效和运镜 → out/<集号>/comic.html
```

- 漫画只用来看懂故事，是草图，不当成片素材；三格一起画，角色和画风前后对得上。
- 先自己看一遍：每格的动作和剧本对得上，角色认得出，没有字。不对的用 `--comic --only sheet2 --force` 重出。
- 把 `comic.html` 发布成 Artifact（网页），和 script.md 一起交给用户，在消息里写上三句话和选题打分。
- 用户确认之前不出正式的图。用户改了剧本，就重出受影响的那张漫画。

## 5. 出图（Codex CLI，Claude 在用户 Mac 上直接跑）

### 5.1 统一风格词（每条提示词末尾都加）

```
Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees, grass and sky, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16
```

**画面要简洁（2026-10-29 用户定的硬标准，每集都按这个来）**：用户看 s04 原版觉得"视觉元素太多、细节太多，应接不暇"，在简洁版 / 极简版 / 原版三选一里选了**简洁版**。所以：

- 背景只用几块大的柔和色块（树、草地、天空），留大片空白；远山、小镇、满地小花、蘑菇、石子、飘落的叶子这类碎细节都不画，除非剧情要用。
- 色彩收住：柔和的绿、暖棕、奶油色为主，角色比背景亮、比背景清楚，背景对比度低。
- 一张图只有一个视觉焦点；只画提示词点名的角色，不加路人动物。写剧本时一页同框角色尽量 ≤3 个（主角团客串也算），不需要的配角别塞进来。
- 出图后质检多一条：缩到手机大小看，一眼能不能找到主角；找不到就删提示词里的东西再出。
- 对照样张：`out/s04/variant_simple/`（用户选中的那组）已放进 `series/style/` 当画风样张。

夜景集把风格词里的 `big soft shapes of trees, grass and sky` 换成 `big soft shapes of trees and a deep blue night sky with a big round moon and a few soft stars`，`soft greens, warm browns and cream` 换成 `soft night blues, warm lamp yellow and cream`；画面要暖月光、萤火虫、小灯，不能暗、不能吓人（见 s03）。

**画风样张**：用户挑定的样图放在 Mac 的 `series/style/`（只留本机，`.gitignore` 已忽略，不进公开仓库）。`codex_images.py` 每出一张图都会把样张排在最前面发给 Codex，并告诉它"只学画风，不抄角色和构图"。换画风就换这个文件夹里的图。**画风变了，`series/refs/` 的角色参考图要先用 `codex_images.py refs --force` 重出**，否则旧参考图会把画风拉回去。

页面图再加 `keep every face in the upper 55% of the image and the lower 40% simple open ground`（字幕中心在 y≈1320，下面还有抖音标题和简介，所以脸都放在上半部分，下 40% 只留地面、草地这类简单背景）。

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
- 出完抽几张缩小拼图看一遍（角色像不像参考图、下 40% 有没有脸、有没有乱入文字），不行的用 `--only … --force` 重出，再把结果拼图发给用户挑。

**踩过的坑**（2026-10-24）：

- Codex CLI 太旧（0.142）时，服务器会报"model is not supported / requires a newer version"。先跑 `codex update`，再 `codex exec --skip-git-repo-check "reply with just: ok"` 验证。
- `-i` 后面能跟多个文件，会把提示词也吞掉，导致报 "No prompt provided"。脚本已改成提示词从 stdin 传（参数写 `-`）。
- 网络抖动时 Codex 出完图还会一直重连、不退出。脚本已改成看到图落盘就结束进程。
- 用户 `~/.codex/config.toml` 里的 MCP 服务会报 403 / AuthRequired，是噪音，不影响出图。
- （2026-10-26）多角色图连续失败：三张 2.6MB 参考图一起上传，网络一抖就断。脚本已改成先缩成 768px JPEG 再传。第一轮失败的图用 `-j 2` 重跑。

### 5.3.1 关键帧动画（2026-10-28 起默认，不花可灵灵感值）

用户的可灵会员额度用完了，Codex 额度很充足，所以动作都改用 Codex 出关键帧来做，类似日系动画的有限动画（一拍三）：

- **script.md 写法**：主图照旧写 `**p04.png**`；关键帧写 `**p04b.png** ← p04.png`，代码块里只写改哪里（动作、表情、位置），其他都不动。`codex_images.py` 先出主图，再把主图当第一张参考图，让 Codex 只改动作、画出同一镜头的下一张。
- **每页 1–2 张关键帧**，放在最有戏的动作上：张嘴喊、跳起来、被砸、倒下。倒下、鼓起这类动作，一张比一张幅度大（p04b 倒 30°，p04c 倒 60°）。
- **钩子**：首帧 `kling_first.png` 加 3 张关键帧（`h02.png` 起，都以首帧为底），在 story.json 里写 `hook.frames`，不写 `clip`。sbv.py 会做成 4–5 秒的翻页动画：到点硬切、缓推，换图时可以震一下屏。
- **story.json**：
  - `frames`：`[{"image": "p04b.png", "line": 0, "offset": 1.2, "shake": true}]`，在第几句开口后多少秒换成这张，也可以写 `"at"`（秒）。
  - `cycle`：`{"images": ["p02.png", "p02b.png"], "step": 0.25, "line": 0}`，那句台词说话期间来回切，适合嚼东西、晃身子。
  - 换图配一个音效（boing / pop / bonk），落点和换图对齐。
- **连贯（2026-10-29 用户反馈"视频不连贯"后定的）**：
  - sbv.py 会把每张关键帧先对齐到本页底图（背景不跳），换图时用光流补 0.1–0.3 秒中间帧（`tween`，style 里默认 0.22 秒、带 shake 的 0.12 秒）。
  - 光流只适合**小动作**（张嘴、转头、抬手、表情变化）。**大动作**（掉下来、落地、接住、冲出去）补帧会出两张图叠在一起的重影：这种换图写 `"tween": 0` 硬切加震屏，**并且在两张之间多画一张过渡关键帧**（例如 p02b 裂开 → p02d 滑到一半 → p02c 坐地上），一个大动作至少拆成"预备—过程—结果"三张。
  - 说话：主角说重要台词的那张图加一张张嘴帧 `**p04_talk.png** ← p04.png`（"opens his mouth wide talking, nothing else changes"），story.json 写 `"talk": {"p04.png": "p04_talk.png"}`，开口说词时只换嘴那一块来回开合。
  - 运镜：默认统一缓推（`in`），只有剧情动作需要时才用 up / down（爬树、掉下来）；不要每页换方向。
  - 质检：逐帧看每一处换图，有重影就改硬切或加过渡关键帧。
- **谁在说话要一眼看出来（2026-10-29 用户："我们这个严格意义上不算视频，多个角色在一个分镜的时候，谁知道谁在说话？"）**：
  - **每一句角色台词都要有张嘴帧**，不止重要台词。给这句说话时屏幕上那张图出一张：`**p05_bruno.png** ← p05.png`，改动只写 `only the bear opens his mouth wide talking, everyone else keeps their mouth closed, nothing else changes`。story.json 写在那一句上：`"talk": "p05_bruno.png"`（说话期间换了关键帧，就写成 `{"p05.png": "p05_bruno.png", "p05b.png": "p05b_bruno.png"}`）。同一张图两个人轮流说，各出各的张嘴帧。
  - sbv.py 拿张嘴帧算出嘴在哪，然后自动做三件事：镜头往说话的人那边轻轻靠（`speaker_pull`，默认 0.3）；说话人周围亮、远处最多暗 14%（`speaker_spotlight`）；字幕左上角弹出说话人的圆头像，圈是角色色（头像用 `codex_images.py avatars` 出到 `series/refs/avatars/`，新角色出参考图后顺手出头像）。算不出嘴的位置时，在那一句写 `"where": [x, y]`（比例坐标）。
  - 分镜就要帮忙：两人对话时一左一右站，说话的那个更靠前、更大；需要的话说话前加一张"转向对方 / 抬手"的关键帧。
  - 质检：关掉声音看一遍，每一句都能指出是谁在说；指不出来就补张嘴帧或调站位。
- **质检**：关键帧和主图的背景、光线、角色位置要对得上，只有动作变了；对不上就 `--only p04b --force` 重出。抽帧看换图那一下有没有跳画风。

### 5.4 可灵钩子（可选，有灵感值时再用）

- 只做 `kling01.mp4`：图生视频，**5 秒、9:16、1080p、不开原生音频**（原生音频贵 50%，配音由脚本做）。
- 首帧用脚本出的 `kling_first.png`，**尾帧用 `p01.png`**，钩子结束正好落在第 1 页，衔接最顺。
- 提示词用中文，末尾统一加"日系手绘动画风格（赛璐璐角色、柔和描边、手绘背景、通透暖光），保持角色外形和颜色不变，动作轻柔、幅度小"；负面提示词"变形，多余肢体，脸部扭曲，画面闪烁，写实风格，文字，水印"。
- 首帧图不带字幕和大字，大字由 sbv.py 叠。
- **怎么调可灵（2026-10-27 起）**：用国内站官方 CLI `kling`（`npm i -g @klingai/cli-cn --registry=https://registry.npmjs.org`，`kling login` 浏览器授权；skill 在 `~/.agents/skills/kling-cli`）。`kling account` 查余额，`kling who_am_i` 查模型参数。实测命令（在集目录下跑，本地图会自动上传）：
  ```bash
  kling image_to_video --model kling-video-v2_6 --image kling_first.png --tailImage p01.png \
    --duration 5 --resolution 1080p --enable_audio false --prompt "…" --poll 900 > kling.json
  ```
  结果在 `body.generations[0].result.works[0].urlWithoutWatermark`，下载存成 `kling01.mp4`（1080×1920，24fps，5.08 秒）。**价格：可灵 2.6、1080p、5 秒、不开音频 = 25 灵感值/次**，约 80–120 秒出片。可灵 2.6 没有负面提示词参数，写进提示词末尾。可灵 2.6 / 3.0 / 4.0 都支持首尾帧 + 1080p，其他模型的价格还没实测。
  国际版远程 MCP `kling-ai`（kling.ai）跟国内账号、灵感值不通用，不要用。
- **5 秒钩子设计原则**（这 5 秒是全片开场、s01 2 秒跳出率 66.7%，杠杆最大）：
  1. **首帧就在动作中间**：`kling_first.png` 不要摆拍，要“正在发生”——道具在半空、靠近镜头，低机位贴地，角色在后面追、表情着急；和 p01 同一地点、同样的光。重出首帧是免费的（Codex），先把首帧做对再花灵感值。
  2. **2 秒内出第一个“哇”**：提示词按秒写节拍（0–1.5 秒大动作 / 1.5–3.5 秒角色反应 / 3.5–5 秒定格成尾帧构图）。道具和水花动作可以大，角色动作要轻、幅度小。
  3. **镜头基本固定**：写明“低机位、只轻微平移，不推拉、不转场、不切镜头”。s02 第 1 次让镜头推近，2 秒处角色衣服融化变形，作废。
  4. **尾帧 = p01**，钩子直接接第 1 页。
  5. **声音是免费的杠杆**：可灵不出音频，逐帧找落点时间，在 `hook.sfx` 里配音效（bonk 起音约 0.06 秒、pop 几乎立刻出声，`at` 要减掉起音）；旁白 `hook.say.at` 放在冲击之后约 0.2 秒，别盖住音效。
  6. 大字在 y=330 左右，首帧里角色的脸要在 y>520，出片后看第 0 帧。
- 生成后在 0、0.5、1、1.5、2、3、4、4.9 秒抽帧拼图检查，2 秒前后再逐帧看一遍（变形常出在中段）。
- 先用占位开头把其余部分做成成品；kling01.mp4 到位后，抽帧质检，再重渲。
- 每集最多生成 3 次（可灵 2.6 1080p 约 75 灵感值）。超过 3 次还不合格，停下来跟用户说。
- **sbv.py 在 `hook.clip` 文件不存在时会报错停下**。可灵还没做好时，用首帧图做一个 5 秒占位（`kling_first.png` 缓推 4 秒 + 叠化到 `p01.png` 1 秒），另存一份临时 story.json 把 `hook.clip` 指过去，先把其余质检做完；`kling01.mp4` 一到，用正式 story.json 重渲、重跑 `qa.py`。占位版不能发布。
  ```bash
  ffmpeg -y -loop 1 -t 5 -i kling_first.png -loop 1 -t 5 -i p01.png -filter_complex "[0]scale=2160:3840,zoompan=z='1+0.08*on/150':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=150:s=1080x1920:fps=30[a];[1]scale=1080:1920,fps=30[b];[a][b]xfade=transition=fade:duration=1:offset=4,format=yuv420p" -t 5 hook_placeholder.mp4
  ```

### 5.5 换画风的流程（2026-10-28 起）

用户说画风不对时，不要只改风格词就重出整集（10-27 那次改了词，用户看着"完全没有变化"）。先出样图让用户挑：

1. 候选写在 `series/style_tests.json`：每组有名字、风格词、为什么适合 2–3 岁英语启蒙；场景用两张（三个角色同框站一排、本集第 1 页）。
2. `python3 codex_images.py styles -j 2`，出到 `out/style_test/<风格>_<场景>.png`。这一步**不带**样张和旧的角色参考图，否则会被拉回旧画风。
3. 自己先看一遍（角色认得出、没文字、没多余肢体），再做一个对比网页（Artifact）：每组两张图并排，写上名字和理由，让用户挑。
4. 用户挑定后：把这组的风格词写进 5.1 和 `codex_images.py` 的 `STYLE`，选中的那张放进 `series/style/` 当样张，跑 `refs --force` 重出角色参考图，再出本集的图。

2026-10-28 这一轮的五组：水彩绘本（用户点名要的）、3D 软萌动画、扁平粗线卡通、毛毡黏土手作、日系手绘动画（接近用户发的「一只狐尼克」截图）。**用户选了日系手绘动画**，样图 `out/style_test/anime_*.png` 已放进 `series/style/` 当样张，旧样张移到 `series/style_old/`（同样不提交）。

## 6. 写 story.json 和配音（按类型，见分册）

- 口语线：story.json 骨架和字段要点、配音情绪（原 6.1 节）→ [skill-type-talk.md](skill-type-talk.md) 第 6、7 节。
- 儿歌线：`song` 段、`word`、`cycle` → [skill-type-song.md](skill-type-song.md) 第 3、4 节。
- 两条线通用：放在 `episodes/<编号>-<slug>/story.json`，字段全集见 `tools/storybook-video/README.md`；写完用 `python3 -c "import json;json.load(open('story.json'))"` 校验。

## 7. 渲染（在用户 Mac 上跑）

口语线的配音准备和样片规则见口语分册第 7 节；儿歌线先按儿歌分册第 4 节把歌定下来再渲染。

每集出片：

```bash
cd ~/code/little-circle/tools/storybook-video && source .venv/bin/activate   # .venv 用 /usr/bin/python3（3.9）建；终端里的 python3 是 Anaconda 3.7，太旧
export PATH=~/Downloads/Anaconda3/anaconda3/envs/sbv-ffmpeg/bin:$PATH        # 这台 Intel Mac 上 brew 装不了 ffmpeg，用 conda 环境里的（带 loudnorm，不带 rubberband）
python sbv.py ../../episodes/c01-fruits/story.json --out ../../out/c01               # 完整版
open ../../out/c01
```

- 输出：mp4、srt、A4 打印版 PDF（以后做付费打印包用）。
- 渲染耗时约等于片长 2 倍。长任务开始前说一句在做什么，完成后再汇报，不刷屏。
- `sbv.py` 的 ElevenLabs 代码在 HANDOFF 里标着"还没用真实 key 跑过"时，先用 `example/voice_test.json` 跑一句验证，报错先修脚本。

## 8. 确认剧本后一路做到成品（用户的目标）

用户原话："你自己检查下，有问题自己修复掉。我要的是成品。" 只有一个关口要等用户：**剧本确认**（儿歌线多一个：试听选歌）。确认时交给用户的是剧本加漫画剧本网页（第 4.1 节）。确认之前除了漫画草图，不出图、不渲染。确认之后，Claude 在用户 Mac 上一口气跑完（Remote Control 会话），每一步过第 9 节的质检，不合格自己修，最后只汇报一次。

1. 出图：`python3 codex_images.py ../../episodes/<集> -j 2`，放后台跑。主图出完会自动接着出关键帧（第 5.3.1 节）。
2. 钩子：默认用关键帧翻页钩子（`hook.frames`）；有可灵灵感值、用户也同意花时，才按第 5.4 节出 `kling01.mp4`。
3. 渲染：**只出完整版**，用正式的 `story.json`（2026-10-29 用户：片子本来就三四十秒，精华版没必要；口语线、儿歌线都一样）。
4. 封面：`python brand.py ../../episodes/<集>/story.json --ep <集数> --words help=帮忙 push=推 ball=球 --out ../../out/<集>`，出 9:16（1080×1920）和 3:4（1080×1440）两张，徽章是"栗栗学英语"（`brand.py` 就是附录 A 的 `make_cover`，字体改成本机能找到的）。
5. 发布包：`out/<集>/publish.txt`（抖音标题、小红书标题、正文、置顶评论），小红书图文用的图放在 `out/<集>/xhs/`。
6. **同步 OSS，出最终网页**（2026-10-28 用户要求：以后只给一个网页）：`.venv/bin/python oss_publish.py ../../out/<集>`，链接写进 `out/<集>/oss.json`；再发布一个预览网页（Artifact），里面有完整版播放、封面、每个文件的下载按钮（视频直接用 OSS 链接）、按平台分好的标题/正文/话题/置顶评论和一键复制。交付只发这个网页链接，不发本地路径、不让用户自己去文件夹找。OSS key 只从环境变量 `OSS_ACCESS_KEY_ID`、`OSS_ACCESS_KEY_SECRET` 读（在用户 `~/.zshrc` 里），读不到就先用 Artifact 自带的素材存储顶上，并在汇报里说一句。
7. 收尾：脚本修复提交推送；`tracking/videos.csv` 加一行（状态"待发布"、工时、现金成本）；更新 `HANDOFF.md` 和第 11 节剧集表；`open out/<集>`。

**成品包（交付清单）**，都在 `out/<集>/`：

| 文件 | 用途 |
|---|---|
| `<name>.mp4` | 完整版，进合集 |
| `<name>_cover_9x16.jpg`、`<name>_cover_3x4.jpg` | 抖音封面、小红书封面 |
| `publish.txt` | 标题、正文、话题、置顶评论 |
| `xhs/` | 小红书图文 6–9 页 |
| `<name>.srt`、`<name>_print.pdf` | 字幕、打印小绘本（付费包素材） |
| `<name>_sheet.jpg`、`<name>_frame0.jpg` | 质检留底：每页 2 帧总览、第 0 帧（`qa.py` 生成） |

交付时只讲：最终网页链接、每项质检结果、自己修了什么、花了多少（可灵次数、配音字符）、还剩什么只有用户能做（手机终检、点发布）。

## 9. 每个环节的质量把控（不合格自己修，修完重检）

下表是两条线共用的几关。**剧本、配音、可灵**这几关看口语分册第 8 节，**歌、剧本**看儿歌分册第 6 节。

| 环节 | 检查什么 | 合格线 | 不合格怎么修 |
|---|---|---|---|
| 出图 | 每张图（拼一张 `qc/images.jpg` 自己看） | 角色像 `series/refs/` 参考图（Hazel：棕刺、黄背带裤男孩）；道具颜色、数量前后一致；笑点动作看得出来；下 40% 没有脸；没有文字和水印；没有多余肢体；**画风和 `series/style/` 样张一致**（赛璐璐上色、柔和描边、手绘背景、通透暖光；不能有 3D 渲染感或厚涂毛发） | `--only pXX --force` 重出，最多两轮；还不行就改提示词再出 |
| 渲染 | ffprobe、ebur128、第 0 帧、每页抽 2 帧拼图（`qc/frames.jpg`） | 1080×1920、30fps；I 在 -16±1 LUFS、Peak ≤ -1.5；第 0 帧是带大字的钩子画面；字幕不挡脸，大字不挡主体，没有黑边；每条字幕出现后 0.6 秒内有人声；完整版 40–55 秒 | 调 `focus` / `subtitle_center` / `gap`，然后重渲染 |
| 封面 | 两张封面图 | 标题不压脸；今日单词三个都在；徽章是"栗栗学英语" | 3:4 标题压脸就调 `brand.py --crop-3x4`（0=从顶部裁，默认 0.55；s02 用 0.2），或重出 `cover.png` |
| 发布包 | publish.txt | 没有微信号、二维码、网址（谐音也不行）；带 AI 声明；每个标题 ≤20 字；话题 ≤5 个、含"英语启蒙" | 改文案 |

配音（口语线）或听写（儿歌线）和渲染两关用一条命令跑完（在 `tools/storybook-video` 下，ffmpeg 要在 PATH 里，第一次先 `.venv/bin/pip install faster-whisper`）：

```bash
.venv/bin/python qa.py ../../episodes/<集>/story.json ../../out/<集>/<name>.mp4 --dur 40 55
```

最后一行写"全部通过"才算过。它查格式、响度、第 0 帧不黑、黑边、Whisper 逐句对照（相似度 ≥0.75）、字幕 0.6 秒内有人声、Hazel 和 Bun 的基频语速、时长；总览图和第 0 帧还要用眼睛看一遍（挡脸只能人看）。另外要听的：剧本里写了"小声""大喊"的句子，音量真的有差别。

**只有用户能做的**：手机终检（前 2 秒、字幕有没有被抖音标题简介或右侧按钮挡住、睡前小音量能不能听清），以及点发布、勾 AI 声明。

## 10. 发布与数据

**平台分工**：

| 平台 | 发什么 |
| --- | --- |
| 抖音（主） | 完整版直接发：口语线进对应合集（森林故事 / 认知小绘本 / 栗栗的一天），儿歌线进「栗栗唱儿歌」。评论区置顶本集 3 个单词 |
| 小红书（辅） | 图文为主：6–9 页绘本 + 一张单词卡，标题带"3岁英语启蒙""英文绘本"这类搜索词；视频顺手同步。绘本页直接用集目录里的 p01–p06，封面用 cover.png |
| 视频号 | 和抖音同一条视频，勾选原创声明 |

发自己导出的无水印原片，不要把抖音下载的带水印版本发到别处。

**标题**（2026-10-30 用户定：**每个平台的标题都不超过 20 个字**，标点、空格、英文字母都算一个字，写完数一遍）：
- 抖音：钩子大字标题同款，或 `{中文集名}｜3岁英语启蒙`
- 小红书：`{中文集名}｜3岁英语启蒙`

**话题标签**（2026-10-30 用户定：**最多 5 个**）：只挑最贴本集、热度最高的 5 个，不凑数。挑法：先定 1 个本集主题词（如 #勇敢 #学会分享），再从热门的启蒙大词里挑 4 个（#英语启蒙 #幼儿英语启蒙 #英语绘本 #儿童英语 #亲子英语 等，按平台搜索框联想和话题页播放量排）。抖音、小红书各自按自己平台的热度挑。

**正文模板**：

```
🌰 {片型合集名}｜{English title} {中文集名}
{一句话：栗栗遇到什么 / 今天认识什么}

📖 今日单词：{word1} {中文}｜{word2} {中文}｜{word3} {中文}
🗣 跟读句子：
{核心句1} {中文}
{核心句2} {中文}

💡 亲子小互动：看完问问宝宝 "{一个问题}"，让宝宝用 "{句型}…" 回答。

#英语启蒙 #幼儿英语启蒙 #英语绘本 #亲子英语 #{本集主题词}
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

#英语启蒙 #幼儿英语启蒙 #英语绘本 #亲子英语 #学会分享
```

正文、评论、简介里不放微信号、二维码、网址。勾选 AI 生成声明。

**数据**：每条视频每个平台一行记进 `tracking/videos.csv`（日期、平台、标题、题材、时长、本条改动的变量、播放、2 秒跳出率、5 秒完播率、平均播放秒、完播率、点赞、收藏、分享、评论、新增关注、进群人数、现金成本、制作工时）。每 5 集一批，**一次只改一个变量**（钩子标题、长度、发布时间、形式）。M1 判据写在 `milestones/` 里，期中不改。

## 11. 剧集表

| 编号 | 线 · 合集 | 英文名 | 中文名 | 主题 | 今日单词 | 核心句 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| s01 | 口语 · 森林故事 | Nutty's Big Acorn | 小松鼠的大橡果 | 分享 | acorn, share, hungry | It's mine! / Let's share! / Sharing is fun! | 2026-10-21 已发（全程可灵，基线） |
| c01–c05 | 口语 · 认知小绘本 | Nutty Is Hungry / Where Is My Carrot? / Hazel's Colorful Leaves / Achoo! Cover Your Mouth! / Bun's Rainy Picnic | | 饿和饱、数数、颜色、打喷嚏捂嘴、天气 | 以各目录 script.md 为准 | | 2026-10-26 按新标准重写（一个主题、8 页、约 11 句），等确认后出图 |
| m01 | 儿歌 · 栗栗唱儿歌 | Big and Small! | 大大小小，唱起来！ | 反义词 big/small、tall/short、fast/slow | big, small, tall | Big, big, big! / Big and small! Short and tall! | 2026-10-29 成品完成、qa 全部通过；10-30 儿歌线暂停，产物全部保留，先不发布 |
| s04 | 口语 · 森林故事 | Brave Little Pip! | 小老鼠皮皮好勇敢！ | 勇敢（害怕也可以勇敢） | brave, scared, help | I am scared. / Be brave! / I am scared, but I am brave! | 2026-10-30 定稿待发布（用户：「这一版还不错」）。重做两轮后定下三条标准：简洁画面、关键帧对齐 + 大动作加过渡帧、谁在说话（张嘴帧 + 镜头靠向 + 字幕头像）；只出完整版、封面只留 3:4；Bruno 用男孩声 Chintu |
| s03 | 口语 · 森林故事 | Nutty Is NOT Sleepy! | 栗栗才不困呢！ | 困了就说晚安（sleepy → Good night） | sleepy, good night, snore | I am not sleepy! / I am sleepy, too. / So sleepy... Good night! | 2026-10-28 用户否掉（"一点波澜都没有"）：困了不算困境，没有张力 |
| s02 | 口语 · 森林故事 | Help! Hazel's Red Ball | 小刺猬的红皮球 | 求助（一个词 help 讲一个道理） | help, push, ball | Help me, please! / I can help! / Thank you! | 2026-10-27 成品做完、全部质检通过，只差可灵钩子；10-28 换 v3 语气配音、字幕上移去底板；画风定为日系手绘，重画中；钩子要等充值后按新画风重出；待发布 |

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
