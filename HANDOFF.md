# 交接记录

> 最近更新：2026-10-29（s04《小老鼠皮皮好勇敢》成品做完，两版 qa 全部通过，待发布；新角色 Pip、Bruno、Ruby、Fern 音色写进 cast.json）。上一次：2026-10-27（s02 成品；新增 qa.py、brand.py）。之前的工作在云端会话里完成；从这里开始，在用户 Mac 上的本地会话接着做。
> 新会话请先读完本页，再按需读 [README.md](README.md)、[milestones/M1-2026-11.md](milestones/M1-2026-11.md) 和 `docs/`。

## 0. 最新：儿歌集上线第一首（2026-10-29）

- 新合集「栗栗唱儿歌」，第一首是 m01《Big and Small!》，44 秒，成片已过质检。集目录在 `episodes/m01-big-small/`，做法写在 skill 第 3.2 节。
- 工具：`tools/storybook-video/song.py`（ElevenLabs Music 生成、听写质检、选定）；`sbv.py` 和 `qa.py` 都加了儿歌模式。
- 成品在用户 Mac 的 `~/code/little-circle-songs/out/m01/`（这一首在单独目录里做，没放进主工作区）。
- 用户要做的两件事：
  - 在 `~/.zshrc` 里加上 `OSS_ACCESS_KEY_ID`、`OSS_ACCESS_KEY_SECRET`，否则 `oss_publish.py` 跑不了。
  - 把 Fredoka.ttf 放进 `tools/storybook-video/fonts/`；现在英文字用的是系统里的 Arial Rounded。

## 1. 现在在哪

M1 第 0 周（准备周，10-24 ～ 10-25），M1 正式周期是 10-26 ～ 11-22。

- 三个平台已统一改名「栗栗学英语」。
- ElevenLabs 已注册（**目前是免费档**），API key 已配到用户 Mac 的 `~/.zshrc`。
- 音效库已生成，但用的是免费档，不能商用，订阅后要重做。
- **选角和背景音乐卡在付费档**，等用户订阅 Starter。

## 2. 已完成的东西在哪

| 内容 | 位置 |
|---|---|
| 完整调研：哇叽星球拆解、版权风险、原创路线、短视频起号、私域、老师观点对照 | [docs/research-2026-10.md](docs/research-2026-10.md) |
| 竞品：嘟嘟英语绘本馆（初步） | [docs/competitor-dudu-2026-10.md](docs/competitor-dudu-2026-10.md) |
| 账号与品牌：名字、角色、头像提示词、简介三版、平台分工 | [docs/brand.md](docs/brand.md) |
| M1 目标、判据、每周待办 | [milestones/M1-2026-11.md](milestones/M1-2026-11.md) |
| ElevenLabs 流程与交付标准 | [docs/elevenlabs-workflow.md](docs/elevenlabs-workflow.md) |
| 系列技能的"混合方案"补充（开头 5 秒可灵 + 其余动态绘本） | [docs/series-skill-addendum.md](docs/series-skill-addendum.md) |
| 动态绘本出片工具 | [tools/storybook-video/](tools/storybook-video/)（`sbv.py` 出片、`qa.py` 成片质检、`brand.py` 封面） |
| ElevenLabs 一次性准备脚本 | `tools/storybook-video/el_prep.py` |
| Codex CLI 批量出图（读 script.md 提示词，带角色参考图，出 1080×1920） | `tools/storybook-video/codex_images.py`；用法和踩坑见 [docs/skill-kids-english-story-video.md](docs/skill-kids-english-story-video.md) 5.3 节。c01–c03 的图已在用户 Mac 上出好（本地，不提交） |
| 系列 Skill 最新全文（10-27 加了成品清单和 9 道质量关口，待用户在卡片上保存） | [docs/skill-kids-english-story-video.md](docs/skill-kids-english-story-video.md) |
| 程序化八音盒背景音乐 | `tools/storybook-video/make_bgm.py` |
| 角色音色表（Voice ID 还没填） | [series/cast.json](series/cast.json)；订阅前出样片用 `series/cast_kokoro.json` |
| 首批 5 条认知短片剧本 + story.json | [episodes/](episodes/README.md) |
| 数据记录 | `tracking/videos.csv`（第 1 集基线已填）、`tracking/sales.csv` |

## 3. ElevenLabs 现状

**API key**：开了 Restrict Key，额度上限 10000。权限有 Text to Speech、Sound Effects、Music Generation、Voice Generation，Voices 设为 Write，其余都是 No access。

**免费档实测**（2026-10-24，`el_prep.py all`）：

| 功能 | 结果 |
|---|---|
| 音效 `/v1/sound-generation` | ✅ 可用，14 个已生成到 `assets/sfx/`（免费档版本，不能商用） |
| 设计音色 `/v1/text-to-voice/design` | ❌ 403 `feature_unavailable`：只对付费档开放 |
| 音乐 `/v1/music` | ❌ 402 `limited_access`：免费用户不能用 |
| 配音 `/v1/text-to-speech/.../with-timestamps` | 还没用真 key 测；`el_prep.py tts` 可以直接测（模拟接口已通过） |

**注意**：
- `sbv.py` 里的 ElevenLabs 配音代码**还没用真实 key 跑过**。第一次跑如果报错，先修这里。
- `el_prep.py` 只用模拟接口测过，在真实接口上只跑通了音效这一项。

## 4. 下一步（按顺序）

1. **用户订阅 Starter**（约 5 美元/月）。付款由用户自己操作。2026-10-24 已定：旁白和角色配音走 ElevenLabs Starter，不换别的 TTS。
   - 理由：免费档生成的音频一律不能商用，换成免费档默认音色也一样，绕开付费档只会多返工一遍。
   - 备胎：Azure 语音免费档（每月 50 万字符、可商用、带逐词时间戳），但音色就是 edge-tts 那套，只在 ElevenLabs 用不了时再接。
2. 订阅后，先在仓库根目录跑配音自检（用默认音色配一句，测通带时间戳的接口，花不到 100 字符）：
   ```bash
   python3 tools/storybook-video/el_prep.py tts
   ```
   看到「时间戳正常」再执行：
   ```bash
   python3 tools/storybook-video/el_prep.py all --force
   ```
   这一条会做三件事：重做可商用的音效；四个角色各生成 3 个候选音色，存到 `out/casting/`；生成 3 首背景音乐，存到 `assets/bgm/`。
   如果 Starter 下音乐仍然报档位不够，先用 `make_bgm.py` 顶上，并记进文档。
3. 用户执行 `open out/casting`，用小音量试听，再报编号。然后执行：
   ```bash
   python3 tools/storybook-video/el_prep.py pick narrator=? nutty=? hazel=? bun=?
   ```
   这一步会把 Voice ID 写进 `series/cast.json`，然后**提交推送**。
   - 某个角色不满意：执行 `cast <角色>`，再出 3 个。
   - 保存时提示自定义音色满了：用网页上默认音色的 ID，写成 `pick narrator=<ID>`。
4. **配音验证**：先确认 `ffmpeg` 已装（`brew install ffmpeg`）。在 `tools/storybook-video` 目录下：
   ```bash
   python3 -m venv .venv && source .venv/bin/activate && pip install pillow numpy
   python3 example/make_demo_assets.py        # 生成 example/p1.png 等演示图
   python sbv.py example/voice_test.json --out out/
   ```
   对照 `docs/elevenlabs-workflow.md` 第 3 节检查：
   - 四个角色的声音能分清；
   - 字幕高亮和发音对得上（确认走的是带时间戳的接口）；
   - 响度 -16 LUFS，峰值不超过 -1.5 dBFS；
   - 画面 1080×1920、30fps。

   字体：没装 Fredoka 时会自动换成 macOS 自带的 Arial Rounded；中文自动找苹方、冬青黑体、华文黑体。
5. ~~写首批 5 条认知短片的剧本和 story.json~~ ✅ 10-24 写好，见 [episodes/README.md](episodes/README.md)。
   - 每集目录里的 `script.md` 有出图提示词（p01–p06 + 可灵首帧）和可灵提示词。**用户接下来要做的是出图**：每集 6 张图 + 1 个可灵钩子，先做 c01–c03。
   - 订阅前可以用 `--cast ../../series/cast_kokoro.json` 出样片看节奏（c01 已用占位图试渲染，完整版 42.9 秒、精华版 25.2 秒，流程通）。
5.1 **s02《Help! Hazel's Red Ball 小刺猬的红皮球》**（10-26，Hazel 主演，用 help 一个词讲"遇到困难要开口"）剧本和 story.json 写好，拿来试跑全流程。用户 10-26 定了新要求：每集要有一个主题（一个词串成故事，或讲一个道理），不做纯问答；台词按 2–3 岁写，全片约 13 句、每句 3–5 词。对标依据见 `docs/benchmark-story-2026-10.md`。Hazel 选了 6 号音色，要先跑 `python3 tools/storybook-video/el_prep.py pick hazel=6` 写进 `series/cast.json`。10-26 用户已确认，开始在 Mac 上出图。10-27 进展：hazel 已写进 cast.json（RAD8sK2svw3uV2PEGgol）；10 张图全部出好并自查合格（总览 episodes/s02-help/contact_sheet.jpg，不提交）；没有可灵钩子的样片已渲染到 out/s02/s02_help.mp4（35 秒，1080×1920 30fps，-16.7 LUFS），等用户听配音、看效果。可灵 kling01.mp4 还要用户自己做，做好后用 story.json 正式出片。注意：Mac 系统 PATH 里没有 ffmpeg，出片前先 `export PATH=~/Downloads/Anaconda3/anaconda3/envs/sbv-ffmpeg/bin:$PATH`（这份 ffmpeg 没有 rubberband，只影响 kokoro 变调）。同一天 c01–c05 也按新标准重写好了（见 episodes/README.md），还没出图。
   **10-27 成品进度**：除可灵钩子外全部做完、质检通过，成品在 `out/s02/`（不提交）：
   - `s02_help.mp4` 完整版 40.5 秒、`s02_help_feed.mp4` 精华版 22.2 秒：1080×1920 30fps，-16.4 / -16.5 LUFS，峰值 -4.4；Whisper 逐句对照 12 句全对；字幕出现 0.6 秒内都有人声。**现在的钩子是占位版**（kling_first.png 缓推 + 叠化到 p01），不能发布。
   - `s02_help_cover_9x16.jpg`、`s02_help_cover_3x4.jpg`（`brand.py`，徽章「栗栗学英语」）；`publish.txt`；`xhs/`（3:4 封面 + p01–p08）；质检留底 `*_sheet.jpg`、`*_frame0.jpg`。
   - 这次修的：sbv.py 中文字体回退到冬青黑体最细的 W3 → 改用 W6；单遍 loudnorm 实测 -17.1 → 改两遍线性校正；新增逐句 `gain`；story.json 第 3 页小声求助 `gain 0.4`、互动停顿 2 秒、第 4 页树叶音效挪到喊完之后（原来盖住了 "Help!"）、末页 hold 1.3；cast.json Bun 的 speed 0.9 → 0.8（原来和 Hazel 基频只差 17 Hz，Bun 还比 Hazel 说得快，改后差 41 Hz）。
   - **10-27 晚按新画风（`series/style/` 样张，精致数字绘本插画）全部重出**：`series/refs/` 三张角色参考图重出并提交；s02 的 10 张图重出，自查一次过（总览 `out/s02/qc/images.jpg`），旧图备份在 `out/s02_old_style/`。占位开头重渲，两版 qa 都“全部通过”；3:4 封面标题压到栗栗的脸，`brand.py` 加了 `--crop-3x4`，s02 用 0.2。
   - **可灵**：国内站 CLI 已装好并登录（`kling` 0.2.3，`@klingai/cli-cn`；skill 在 `~/.agents/skills/kling-cli`），黄金会员，10-27 余额 60 灵感值。可灵 2.6 / 3.0 / 4.0 都支持首尾帧 + 1080p + 不出音频。生成前要用户确认花灵感值。
   - **10-27 可灵钩子做好，s02 成品完成**：国内站 CLI，`kling-video-v2_6` 1080p 5 秒不开音频，25 灵感值/次，生成 2 次（第 1 次 2 秒处背带裤融化变形作废；第 2 次前先把首帧改成“球在半空、低机位”重出），余额剩 10。钩子 0.70 秒球砸进泥坑，配 bonk + pop，旁白挪到 0.95 秒；大字 `headline_y` 改 220，免得压到 Hazel 的脸。完整版 40.5 秒、精华版 22.2 秒，qa 全部通过。成品在 `out/s02/`，可以发布（发之前手机终检）。占位文件已删。
6. 第 0 周剩下的事：
   - 建合集「认知小绘本」「森林故事」；
   - 确认本月预算：ElevenLabs Starter + 可灵 66 元 + 出图订阅，总共不超过 300 元。
7. 可选：执行 `npx skills add elevenlabs/skills`，安装官方技能包；或者接官方 MCP。

5.2 **s04《Brave Little Pip! 小老鼠皮皮好勇敢！》10-29 成品完成，待发布**（用户 10-29 确认剧本后一口气做完）：
   - 出图：Codex 出 23 张（主图 8 + 钩子首帧 + h02–h04 + 关键帧 11 + 封面），全程没花可灵灵感值。第一轮问题：p05 树下画成了 Nutty/Hazel/Bun；h03、p02、p03b、p08 的脸落在下 40%（字幕区）；首帧鸟妈妈的脸在大字下面。改提示词（站上石头、树根、树桩，脸放画面中段）后重出，都已合格。
   - 配音：pip=An3xqcxpNpOHGJcOShlR、bruno=cyDOS9zMDnV6BWZW4i4j、ruby=H3183Z9ZcjE80HwRu4PY、fern=tinYNLscXdfZpc4m5ue7（eleven_v3，stability 0.0）。Bruno 第一轮设计出来不够低沉，描述改成 "very deep bass adult male voice" 重出才选到。实测基频 Ruby 466 / Pip 384 / Bruno 225 Hz。p03 小声那句 gain 从 0.3 改 0.7（v3 的 [whispers] 本身就轻，0.3 听不见），和 p04 大喊差 11.7 dB；树枝断那一下比前一秒响 17 dB。p07 Bruno 的 [laughs] 放句首会先笑 1 秒、字幕对不上，挪到句尾。
   - 运镜：p03 改成 in、focus [0.6, 0.8]、zoom 1.25，p08 focus [0.5, 0.7]，让皮皮的脸在字幕上面。
   - 成品在 `out/s04/`（不提交）：完整版 48.8 秒、精华版 26.3 秒，-16.3 / -16.1 LUFS；封面 3:4 用 `--crop-3x4 0.35`。最终网页 https://claude.ai/artifact/KMrSWqF3kokb8QL1QgNNfg （视频是 720p 压缩版；OSS 环境变量没配，用 Artifact 素材存储顶上）。
   - 剩下只有用户能做的：手机终检、点发布、勾 AI 声明。
   - 脚本修复：`codex_images.py` 关键帧以关键帧为底（h04 ← h03）时等底图先出；`sbv.py` 混音存 float，大喊加 gain 不削波；`qa.py` 本集所有角色两两比基频；`el_prep.py` 加了四个新角色的选角描述。

## 5. 等用户确认或补充

- 实际用的是哪版简介（推荐版本 A），确认后写回 `docs/brand.md`。
- 头像定稿，存一份作为角色参考图。
- 嘟嘟英语绘本馆的补充材料：橱窗商品和价格、交付方式、App 名称、群聊信息。
- 要不要把三个平台的分工写进 M1。分工已经写在 `docs/brand.md` 第 4 节。

## 6. 已定的方向（没有新数据就不推翻）

- **不搬运版权绘本**：走原创 + AI 出图。搬运的民事、刑事风险见调研第四节。
- **先做短视频内容号，不做 App**。M1 的目标是第一次"一买一卖"，不是涨粉。
- **题材先做认知词汇短片**，和剧情片对比数据。依据是嘟嘟最火的是"切蔬菜"。
- **生产方式**：
  - 开头 5 秒用可灵（首尾帧）；
  - 其余页面用 `sbv.py` 做成动态绘本：运镜、深度视差、逐词高亮字幕；
  - 配音、音效、音乐用 ElevenLabs。Kokoro 变调后音质差，已经否决；edge-tts 只做样片。
- **平台**：抖音为主，小红书发图文为辅，视频号同步。
- **引流**：三层漏斗（公域 → 平台内粉丝群和橱窗 → 微信生态）。抖音、小红书上不出现微信号、二维码、网址，谐音和暗号也不行。
- **判据先写死**：M1 判据月中不改，11-23 按数据复盘。

## 7. 用户偏好

- 用简体中文，说大白话，少用术语。给能直接复制的命令，一次只给要做的那几步。
- 代码都放在 `~/code` 下，本仓库是 `~/code/little-circle`。
- 改动直接提交并推送到默认分支，之前一直这样做。
- 老师观点来自用户的知识库 `AmbitionC/life-teachers`（重远、全哥等），调研第六节已经做了对照。需要更多依据时再去查。
