# 交接记录

> 最近更新：2026-10-26（Starter 已订阅，四个角色音色定了，配音验证通过；Hazel 改成刺猬小男孩）。之前的工作在云端会话里完成；从这里开始，在用户 Mac 上的本地会话接着做。
> 新会话请先读完本页，再按需读 [README.md](README.md)、[milestones/M1-2026-11.md](milestones/M1-2026-11.md) 和 `docs/`。

## 1. 现在在哪

M1 第 0 周（准备周，10-24 ～ 10-25），M1 正式周期是 10-26 ～ 11-22。

- 三个平台已统一改名「栗栗学英语」。
- ElevenLabs **已订阅 Starter**（10-25），API key 在用户 Mac 的 `~/.zshrc`。记得把 key 的额度上限改成 20000。
- 音效 14 个、背景音乐 3 首都已用付费档重做（10-25），可以商用，在用户 Mac 的 `assets/` 下。音乐接口在 Starter 下能用。
- 四个角色的音色都定了，已写进 `series/cast.json`（10-26）：旁白、Nutty、Bun 用的是 3 号候选，Hazel 用的是男孩声音那轮的 6 号。
- **Hazel 改成了老实可爱的刺猬小男孩**（10-26，用户定的）：穿黄色小背带裤，剧本里用 he/his。参考图 `series/refs/hazel.png` 和 c03 的 8 张图已经重出；c04 还没出图，提示词已经改好。
- 配音验证通过（10-26，`example/voice_test.json`）：响度 −15.8 LUFS，真峰值 −4.4 dBFS，1080×1920、30fps，逐词高亮能对上。

## 2. 已完成的东西在哪

| 内容 | 位置 |
|---|---|
| 完整调研：哇叽星球拆解、版权风险、原创路线、短视频起号、私域、老师观点对照 | [docs/research-2026-10.md](docs/research-2026-10.md) |
| 竞品：嘟嘟英语绘本馆（初步） | [docs/competitor-dudu-2026-10.md](docs/competitor-dudu-2026-10.md) |
| 账号与品牌：名字、角色、头像提示词、简介三版、平台分工 | [docs/brand.md](docs/brand.md) |
| M1 目标、判据、每周待办 | [milestones/M1-2026-11.md](milestones/M1-2026-11.md) |
| ElevenLabs 流程与交付标准 | [docs/elevenlabs-workflow.md](docs/elevenlabs-workflow.md) |
| 系列技能的"混合方案"补充（开头 5 秒可灵 + 其余动态绘本） | [docs/series-skill-addendum.md](docs/series-skill-addendum.md) |
| 动态绘本出片工具 | [tools/storybook-video/](tools/storybook-video/)（`sbv.py`） |
| ElevenLabs 一次性准备脚本 | `tools/storybook-video/el_prep.py` |
| Codex CLI 批量出图（读 script.md 提示词，带角色参考图，出 1080×1920） | `tools/storybook-video/codex_images.py`；用法和踩坑见 [docs/skill-kids-english-story-video.md](docs/skill-kids-english-story-video.md) 5.3 节。c01–c03 的图已在用户 Mac 上出好（本地，不提交） |
| 系列 Skill 最新全文（待用户在卡片上保存） | [docs/skill-kids-english-story-video.md](docs/skill-kids-english-story-video.md) |
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

1. ~~订阅 Starter、选角、音效音乐、配音验证~~ ✅ 10-25～10-26 做完，见第 1 节。过程中踩过的坑：
   - 选角描述里不能出现小孩、年龄这类字眼（例如 "to a three-year-old"），否则接口会返回 `blocked_generation`。
   - 用户的 Mac 是 Intel 芯片、macOS 15，`brew install ffmpeg` 没有现成安装包。ffmpeg 6.0 已经用 conda-forge 装进 Anaconda 的单独环境 `sbv-ffmpeg`（带 libx264 和 loudnorm，不带 rubberband，ElevenLabs 这条路用不到）。跑 sbv.py 时，在命令前面加上：
     ```bash
     PATH=~/Downloads/Anaconda3/anaconda3/envs/sbv-ffmpeg/bin:$PATH
     ```
   - 终端里的 `python3` 是 Anaconda 的 3.7，版本太旧。`tools/storybook-video/.venv` 是用 `/usr/bin/python3`（3.9）建的，跑脚本要用 `.venv/bin/python`。
   - 某个角色不满意时，执行 `el_prep.py cast <角色>` 再出 3 个，然后执行 `pick <角色>=<编号>`。只在换季的时候换音色。
5. ~~写首批 5 条认知短片的剧本和 story.json~~ ✅ 10-24 写好，见 [episodes/README.md](episodes/README.md)。
   - 每集目录里的 `script.md` 有出图提示词（p01–p06 + 可灵首帧）和可灵提示词。**用户接下来要做的是出图**：每集 6 张图 + 1 个可灵钩子，先做 c01–c03。
   - 配音直接用 `series/cast.json`，也就是 ElevenLabs 那四个音色。
6. 第 0 周剩下的事：
   - 建合集「认知小绘本」「森林故事」；
   - 确认本月预算：ElevenLabs Starter + 可灵 66 元 + 出图订阅，总共不超过 300 元。
7. 可选：执行 `npx skills add elevenlabs/skills`，安装官方技能包；或者接官方 MCP。

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
