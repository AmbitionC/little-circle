# 交接记录

> 最近更新：2026-10-30（**选题升级：新分册 skill-topics.md + 选题库；儿歌线暂停（m01 产物保留）**；**s04 用户定稿：「这一版还不错」，Bruno 定为 Chintu，待用户发布**；剧本写法升级见第 0 节；s04 加「谁在说话」：每句张嘴帧 + 镜头靠向说话人 + 字幕旁圆头像，qa 全部通过；Bruno 配音第三轮，暂用 Chintu）。上一次：2026-10-29（s04 第一版成品；新角色音色写进 cast.json）。之前的工作在云端会话里完成；从这里开始，在用户 Mac 上的本地会话接着做。
> 新会话请先读完本页，再按需读 [README.md](README.md)、[milestones/M1-2026-11.md](milestones/M1-2026-11.md) 和 `docs/`。

## 0. 最新：万圣节 s05《Trick or Treat!》剧本（2026-10-31）

- 用户当天点题："生成一个万圣节主题的剧本，重点让小朋友学会 trick or treat，看怎么做得非常有吸引力"。选题库 c11 提前到今年，改成森林故事 s05：`episodes/s05-trick-or-treat/`（script.md + story.json）。
- 设计：钩子是三人身后的大圆黑影；栗栗袋子漏糖（宝宝先发现）；p05 宝宝一起喊 Trick or treat；反转是 Bruno 扮成老鼠、一路帮大家捡糖。Trick or treat 配固定"敲门 + 伸篮子"动作，说 5 次。对标拆解在 script.md 第 0 节（Super Simple 敲门儿歌、Peppa Pumpkin Party、Go Away Big Green Monster、Blue's Clues 戏剧反讽）。
- 10-31 第 2 版（用户："能不能更有趣一点？看看怎么做成爆款……怎么利用人性"）：黑影改成"猜猜它是谁"的巨型老鼠影子（谜底 Bruno 戴老鼠耳朵），p05 栗栗对着镜头敲门让宝宝敲屏幕，片尾彩蛋皮皮戴熊耳朵 "I am big!"；script.md 第 0 节是人性 × 设计 × 数据表，第 6 节 H3 候选镜头（钩子、糖果雨，先报价），第 7 节发布打法。
- 状态：第 2 版剧本 + 漫画剧本给用户确认中；确认后在 Mac 上出图出片。sfx 时间点要等图出来再对；库里没有敲门声。

## 0. 试接 MiniMax H3 做动作镜头（2026-10-31）

- 用户要试 MiniMax H3，**渠道是七七八AI（ai778.cc）中转**，接口 `https://api.lk888.ai/v1/media/generate` + `/v1/media/status`，模型 `minimax-h3`（`mode` = shouweizhen 首尾帧 / cankaosheng 参考生），图片可 base64 内联。文档 https://ai778.cc/apidoc#model/minimax-h3 不用登录就能看；价格要登录才显示。
- 脚本：`tools/storybook-video/minimax_video.py`，不带 `--go` 只报价不花钱；提交后 task_id 先记进集目录 `minimax.json`，断了用 `--status <id>` 接着查。
- key 放 Mac `~/.zshrc` 的 `AI778_API_KEY`。云端容器连不上 api.lk888.ai（代理拦），实测要在 Mac 上跑。
- 中转站下单即扣，失败自动退款；视频常见 5~60 分钟出。
- **10-31 第一条试跑完成**：s04 钩子 `kling_first.png → h04.png`（提示词 `episodes/s04-brave/h3_hook.txt`），768P 5 秒，**接口返回 cost 3.795（单位没核实；若是元≈0.76 元/秒，比官方贵约 50%）**，约 5 分钟出片。成片 768×1344、5.17 秒、24fps、带音轨，存 Mac `episodes/s04-brave/h3_hook.mp4`（不提交）。角色没融化没走样，首尾帧贴合；缺点是「树枝下沉、Ruby 一只脚悬空」那一下没做出来，紧张感偏弱。**用户看完说「先这样吧，还是有点贵」，H3 暂停**；动作照旧用关键帧动画。日后重启：先查站上其他 H3 型号单价和 cost 单位（3.795 单位没核实），只给 1–2 个动作镜头用、4 秒起。
- Mac 上 `~/.zshrc` 还没有 key（权限拦了代写），这次是弹框临时输入的；长期用要用户自己 `open -e ~/.zshrc` 加 `export AI778_API_KEY=...`。

## 0. 最新：角色升级（2026-10-30）

- 用户要求角色像疯狂动物城一样有鲜明记忆点、不要千篇一律的动物。按用户确认的方案，每个角色补了六件套：反差、剪影钩子、情绪器官、口头禅、想要、小毛病，还有体型阶梯 XS–XL。方法和依据在 [docs/character-design.md](docs/character-design.md)，设定在 [series/characters.md](series/characters.md)，skill 第 5.2 节同步改了。
- 出图描述每句加了一个夸张部位；旧描述 `codex_images.py` 也还认得（`OLD_DESC`），旧集重出图不受影响。参考图改成招牌姿势，新增 `codex_images.py sheets` 出设定图到 `series/sheets/`（只给人看，不进出图流程）。
- 7 张参考图、设定图、头像在用户 Mac 上重出了两轮（第二轮修了 Bun 的耳朵和 Fern 的比例），已提交。旧参考图备份在用户 Mac 的 `series/refs_old_1030/`（未提交）。
- 同日第二版（用户："衣服，装饰，甚至是一些小缺点这些，要有真实感和活人感"）：每个角色加了衣服来历和磨损、和性格对得上的小瑕疵、随身小物（见角色表「活人感细节」），参考图、设定图、头像全部重出（7921abf），第一版备份在用户 Mac 的 `series/refs_v1_1030/`。
- 10-31：Pip 去掉尾巴绷带（用户说像尾巴断了），重出。用户确认图鉴定稿。
- 10-31 角色一致性进 skill（5.2 节「角色一致性」）：剧本写 `[[id]]` 自动展开描述 + 带参考图；每张图附必保细节 `KEEP` 和同框身高 `SIZES`；出图前 `--check` 没过不出图；出完拼 `qc/characters.jpg` 对比。s04、s02 检查出各有路人动物没带参考图（旧集，不改）。
- 图鉴网页：https://claude.ai/artifact/JfVDc75EjRdgw5pMRKVHkR 。2026-10-30 之前已发布和定稿的集不重做，下一集起用新设定。

## 0. 最新：选题升级 + 儿歌线暂停（2026-10-30）

- 新分册 [docs/skill-topics.md](docs/skill-topics.md)：口语线的选题来源（含国内外节日、每周在线搜热点）、筛选标准、不重复规则、每周日排期；儿歌线选题写在第 9 节，**可以用公有领域经典儿歌做素材**（用户 10-30 定，用前逐首核版权）。
- 选题库和排期样例在 [series/topic-bank.md](series/topic-bank.md)：口语 7 条库存 + 19 条候选，11-02 起两周排期（10-30 用户已确认）；儿歌候选 12 条。
- 发布节奏：用户想日更，默认每天 19:30 一条口语；原计划一天两条（加一条儿歌），**儿歌线 10-30 起暂停生产**，skill 里保留。
- 用户先让删 m01 产物，后又改口全部保留：仓库 `episodes/m01-big-small/` 已从 git 历史恢复，共享文件夹 `m01-song/` 已从网页和仓库拷回。Mac 上 `~/code/little-circle-songs` 没动。
- s04 第三个今日单词 10-30 改成 step（和 s02 的 help 错开），文案已改；**封面上的今日单词要在 Mac 上用 `brand.py --words brave=勇敢 scared=害怕 step=一步` 重出**；首次搜国内热点时云端读不到抖音，靠搜索结果。

## 0. 最新：skill 按视频类型分册（2026-10-29）

- 用户要求把 skill 拆成口语类和儿歌类。现在是一个主文件 + 两个分册：主文件 [docs/skill-kids-english-story-video.md](docs/skill-kids-english-story-video.md) 只放公共部分（红线、系列规范、出图、漫画剧本确认、渲染、交付、质检公共几关、发布、剧集表）；口语线 [docs/skill-type-talk.md](docs/skill-type-talk.md)；儿歌线 [docs/skill-type-song.md](docs/skill-type-song.md)。
- 分类：两条线（按声音怎么来）下面五个子类（按一集教什么）：森林故事 s、认知小绘本 c、生活口语 d（待试）、单词卡儿歌 m、动作儿歌 m（待试）。新子类各先做 1 集，看数据再定留不留。
- 原有规则原样搬，没改；原 3.2 节、6.1 节的引用已改指向分册。

## 0. 剧本写法升级（2026-10-29）

- 拆了 Bluey、Peppa Pig、Gruffalo、Mo Willems、Eric Carle、Super Simple、CoComelon、Blue's Clues、Pocoyo、Hey Duggee、Ms Rachel 的剧本方法，写成 [docs/script-craft-global-hits.md](docs/script-craft-global-hits.md)：12 条规则、写剧本的顺序、检查清单，带来源。
- 用户定：这些是 reference，不是硬性要求，每集按选题挑 2–4 条最合适的。skill 第 4 节只引用它，概要写一行"用了哪些手法"。
- `docs/story-psychology-reference.md` 之前只在 j34bgd 分支上，这次一起带进来了（skill 里早就引用它）。

## 0. 最新：儿歌集上线第一首（2026-10-29）

- 新合集「栗栗唱儿歌」，第一首是 m01《Big and Small!》，44 秒，成片已过质检。集目录在 `episodes/m01-big-small/`，做法写在 skill 儿歌分册 [docs/skill-type-song.md](docs/skill-type-song.md)。
- 工具：`tools/storybook-video/song.py`（ElevenLabs Music 生成、听写质检、选定）；`sbv.py` 和 `qa.py` 都加了儿歌模式。
- 成品在用户 Mac 的 `~/code/little-circle-songs/out/m01/`（这一首在单独目录里做，没放进主工作区）。
- 用户要做的两件事：
  - 在 `~/.zshrc` 里加上 `OSS_ACCESS_KEY_ID`、`OSS_ACCESS_KEY_SECRET`，否则 `oss_publish.py` 跑不了。
  - 把 Fredoka.ttf 放进 `tools/storybook-video/fonts/`；现在英文字用的是系统里的 Arial Rounded。

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
| 首月计划：12 条排期、涨粉拆周、变现路线、收入测算（对照月入 5 万） | [docs/plan-month1-2026-11.md](docs/plan-month1-2026-11.md) |
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
   - 配音：pip=An3xqcxpNpOHGJcOShlR、bruno=LjHEEZYE6jkpMf6w5IJV（10-29 用户说原来的"像个大人"，改成小熊宝宝声，基频约 290 Hz；旧的成年低音 cyDOS9zMDnV6BWZW4i4j 作废）、ruby=H3183Z9ZcjE80HwRu4PY、fern=tinYNLscXdfZpc4m5ue7（eleven_v3，stability 0.0）。教训：Bruno 是熊宝宝，别为了"低"做成成年男声；描述里写 boy、preschool、young 会被安全过滤拦，写 "cartoon teddy bear character, medium-high voice" 能过。实测基频 Ruby 466 / Pip 384 / Bruno 286 Hz。p07 boing 音效挪到开口前（0 和 0.28 秒），原来压住了 Bruno 说的 "Boing"。p03 小声那句 gain 从 0.3 改 0.7（v3 的 [whispers] 本身就轻，0.3 听不见），和 p04 大喊差 11.7 dB；树枝断那一下比前一秒响 17 dB。p07 Bruno 的 [laughs] 放句首会先笑 1 秒、字幕对不上，挪到句尾。
   - 运镜：p03 改成 in、focus [0.6, 0.8]、zoom 1.25，p08 focus [0.5, 0.7]，让皮皮的脸在字幕上面。
   - 成品在 `out/s04/`（不提交）：完整版 48.8 秒、精华版 26.3 秒，-16.3 / -16.1 LUFS；封面 3:4 用 `--crop-3x4 0.35`。最终网页 https://claude.ai/artifact/KMrSWqF3kokb8QL1QgNNfg （视频是 720p 压缩版；OSS 环境变量没配，用 Artifact 素材存储顶上）。
   - 剩下只有用户能做的：手机终检、点发布、勾 AI 声明。
   - **10-29 晚～10-30 整集重做**（用户反馈：不连贯、画面太满、不要精华版、封面只留 3:4、小熊配音怪）：
     - 画面定为简洁版（以后每集的标准）。`series/style/` 换成简洁版样张 simple_p04/simple_p07，旧的细节风样张挪到 `series/style_detailed/`（不提交）。31 张图全部重出，自检只有 p07 没画出"被接住、弹起来"，改提示词（肚子压扁、两人高高在空中、弹跳弧线）后重出 p07 一串，合格。
     - 连贯：新关键帧 p02d、p03c、p04c、p06c、p07d 排进 frames；张嘴帧 p02/p04/p08_talk；去掉各页的 motion（统一缓推）。逐帧看过：大动作一律 tween 0 硬切 + shake（光流补帧在大动作上会出两张图叠影），只有小动作（p01b、p02b、p05b、p06c、p08b、h02、h04）留补帧，没有重影。
     - 修了 `sbv.py` talk 帧的一个 bug（`for *_, nm in keys` 里 im 未定义）。
     - Bruno 暂用 Little Dude II（音色库 fBD19tfE58bkETeiwUoC，eleven_v3，stability 0.5），实测约 262 Hz。用户说第一批三个（Little Dude II / Berty / Teddy Twinkle）都不好；第二批 6 个候选页 https://claude.ai/artifact/9j7AYUVBqbGkJ3qLzXPRLr ，推荐 Sarah（emSmWzY0c0xtx5IFMCVv）和 Paula Paw（iukn3a1vSSNFmdi5NZS4），等用户挑。试过 multilingual_v2：两个声音都被抬到 330–440 Hz 和皮皮撞，Bruno 继续用 v3。
     - **10-30 谁在说话 + Bruno 第三轮**：角色头像 `series/refs/avatars/` 7 张（已提交）。每句角色台词给屏幕上那张图出张嘴帧（pXX_<角色>.png），挂在 story.json 那一句的 talk 上。用 talk_paste 算出的嘴位置逐张核对：p01b_ruby、p04c_pip、p07c_ruby 两轮都改错了角色（鸟妈妈、背景、熊），删掉，改用 "where"；p07_bruno 第二次对了。关掉声音逐句看，头像 + 镜头靠过去都能指出是谁说的，没露边。
     - Bruno 第三轮只找男孩声（18 个，eleven_v3、stability 0.5、speed 0.9、台词加 [slowly, proudly] 等标签）。Voice Design 只要写孩子气、小熊宝宝就被拦（ElevenLabs 不让生成儿童声音），只能用音色库。整集实测：Teddy Twinkle 377 Hz 和皮皮撞；Nobita 口音重，"Boing" 怎么写都念错；Chintu（aPE0uHZbwrQVPMm3ihPH，约 300 Hz，印度配音演员），"Be brave, Pip!" 用 take 2 才过 qa。**10-30 用户看完这一版说「这一版还不错」，Bruno 定为 Chintu。**
     - 完整版 48.7 秒，-16.4 LUFS，qa 全部通过；封面 3:4 用 `--crop-3x4 0.0`（0.35 时中文标题压住熊的眼睛）。精华版和 9:16 封面不再做。最终网页同上链接（Version 4）。
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
