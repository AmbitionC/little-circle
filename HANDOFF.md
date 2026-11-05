# 交接记录

> 最近更新：2026-11-05（**m03 小星星对话版剧本 + 漫画剧本，待用户确认**）。再上一次：2026-11-04 晚（**专属绘本线 x00 在 Mac 上整条跑通，成片 45.6 秒 qa 全过，下一步等 x01 的照片**）。再上一次：2026-11-03 晚（**声音设计升级：装好全局 sound skill，新分册 docs/skill-sound-design.md，sbv.py 加环境底声层，c18 试听版待用户听**）。再上一次：2026-11-03（**m02 拔萝卜按原谱做英文翻唱试听，待用户挑版本；原谱署名包恩珠，版权未核实**）。再上一次：2026-11-02 晚（**m02 拔萝卜英文儿歌（国风特别版）成片 48 秒，待发布**）。再上一次：2026-11-01 晚（**c18 躲猫猫成片 49.8 秒，待发布**；**s05 第 3 版日常模式成片：全关键帧、不混 H3，待用户手机终检和发布**，见第 0 节最上面）。再上一次：2026-11-01（s05 H3 版）。再上一次：2026-10-31（**全量同步进默认分支，接手方法见下一节**；s05 万圣节剧本第 2 版；H3 试跑后暂停）。再上一次：2026-10-30（**选题升级：新分册 skill-topics.md + 选题库；儿歌线暂停（m01 产物保留）**；**s04 用户定稿：「这一版还不错」，Bruno 定为 Chintu，待用户发布**；剧本写法升级见第 0 节；s04 加「谁在说话」：每句张嘴帧 + 镜头靠向说话人 + 字幕旁圆头像，qa 全部通过；Bruno 配音第三轮，暂用 Chintu）。上一次：2026-10-29（s04 第一版成品；新角色音色写进 cast.json）。之前的工作在云端会话里完成；从这里开始，在用户 Mac 上的本地会话接着做。
> 新会话请先读完本页，再按需读 [README.md](README.md)、[milestones/M1-2026-11.md](milestones/M1-2026-11.md) 和 `docs/`。

## 0. 最新：m03 小星星对话版，漫画剧本待用户确认（2026-11-05）

- 用户 11-05：m02 拔萝卜对话版「流量还可以」，再找一首。B 站按播放查了候选（共享文件夹 `little-circle/song-topics-2026-11.md`），用户选**小星星**（旋律 18 世纪法国民歌，公有领域）。
- 剧本 `episodes/m03-twinkle-star/script.md` + `story.json`（草稿，at 是估值；配音后照 m02 的 prep_talk / bgm_talk 流程按小节重算，伴奏八音盒/钢片琴弹主旋律）。画风系列默认日系手绘简洁版，夜景。
- 漫画剧本 24 格：https://claude.ai/artifact/LKWbCKTZ2Ctttr2bF8qibF （Mac `out/m03/comic.html`）。漫画里星星四角/五角不统一、水桶大小不一，提示词已补（c4f65f3），正式出图时生效；p06b 俯拍在漫画里没体现（comic_all_jobs 把它当同镜头），正式出图单独看。comic_page 把钩子台词说话人显示成「旁白」，小问题未修。
- 下一步：用户确认剧本 → 正式出图 → 配音 + 合成伴奏 → sbv → qa（≤50 秒）。

## 0. 最新：专属绘本线 x00 整条跑通（2026-11-04 晚）

- 跑通了 fake → describe → cards → pick → 出图 → sbv → qa → brand → PDF。14 张图一次出完（单张约 1 分钟，两张 4 分多），没有重出。成片 `out/x00/x00_mia_zoo.mp4` 45.6 秒，-16.1 LUFS，qa 全部通过（`out/x00/qc_full.txt`）；720p 预览 `out/x00/x00_preview.mp4`。
- 角色卡出了两轮：第一轮 desc 写 dark brown，画成中棕，和照片的近黑差得明显；改 near-black 后第二轮才像，选第 2 版。
- 修的坑（细节见分册第 7 节）：describe 的 desc 句尾句号和手持玩具；`[clearly]` 被念成清嗓子（口语分册已改）；qa 短句误报；p05 运镜把孩子裁掉半张脸；封面中文标题压头发（`--crop-3x4 0.1`）；AI 标识原来根本没落实（新增 story.json 的 `ai_note`，片尾写在 `ending.subline`）。
- 配音约 500 字符（按送配音的文本算；这把 key 查 `/v1/user/subscription` 返回 401，查不到账户用量）。
- 没解决、不挡路：3:4 封面写着「EP.00 第0集」，专属绘本没有集数概念；PDF 封面只有文字，9:16 的图在 A4 上只占约一半页面；复习页大字压在 p07 孩子的头发上（没挡眼睛）；孩子借 bun 的声音，qa 量出和 Nutty 基频都顶到 500 Hz，靠语速差 25% 过关，要人耳听。
- 下一步：等用户把照片放进 `episodes/x01-zoo/photos/`、填 `profile.json`，按分册跑 x01。

## 0. 专属绘本线（x）工具和 skill 已写（2026-11-04 下午）

- 用户 11-04 定：生图继续用本机 Codex 流程（不接 API）；实体书、个体户先不管；目标是第一条推广验证视频；视频生成复用原 skill，新起一个 skill 把链路跑通。
- 新东西：分册 [docs/skill-photo-storybook.md](docs/skill-photo-storybook.md)；`tools/storybook-video/photo_character.py`（fake / describe / cards / pick / purge：照片 → 外貌描述 → 3 版角色卡 → 登记成集内角色 `[[kid]]` + 集内 cast.json + 头像 → 删原照片）；`codex_images.py` 支持集目录 `characters.json`（集内角色、集内参考图 `refs/kid.png`）；`sbv.py` 的 `style.avatar_dir` 可写一串目录。
- 测试集 `episodes/x00-demo/`（虚构孩子 Mia，`photo_character.py fake` 出假照片）：script.md、story.json、profile.json 已写；真实第一单 `episodes/x01-zoo/`（用户女儿的动物园）只有 `profile.example.json`，等用户把照片放进 `episodes/x01-zoo/photos/`、填 `profile.json`。
- .gitignore 新增：`episodes/x*/photos/`、`profile.json`、`characters.json`、`character_draft.json`（孩子信息不进公开仓库）。

## 0. 最新：新产品线「照片变专属英文绘本」规划（2026-11-04）

- 用户 11-04 提出：家长发孩子照片 + 一句话 → 英文绘本 + 动画视频 + 可打印版，后续按 credit 收费；先做成品、录屏口播演示、发布验证需求。
- 规划见 [docs/plan-photo-storybook-2026-11.md](docs/plan-photo-storybook-2026-11.md)（完整版是 Claude Doc，链接在文件里）。要点：先两周手工代做验证（11-05～11-19），判据写死；照片 → 角色卡用国内模型；出图要换成 API 后端；等用户拍板 6 件事后开工。
- 尚未动代码。开工第一步是 `tools/storybook-video/photo_character.py` 和剧本提示词模板。

## 接手方法（2026-10-31 全量同步后）

- **唯一主线**：GitHub `AmbitionC/little-circle` 的默认分支 `claude/funny-franklin-ucpap0`。skill、角色图鉴（`series/characters.md` + `series/refs/`、`series/sheets/`、`series/refs/avatars/` 当前版参考图）、出图/出片/H3 脚本（`tools/storybook-video/`）、各集剧本（`episodes/*/script.md` + `story.json`，含 s05 万圣节第 2 版）、首月计划和 M1 判据都在这条分支上。旧的 `claude/project-thread-*` 分支已全部合进来，不用再看。
- **仓库是公开的**：不提交任何 key（ElevenLabs、七七八AI 都从环境变量读，key 只放 Mac `~/.zshrc`），也不提交剧集图片、视频、音效（见 `.gitignore`）。图和片只在用户 Mac 的 `~/code/little-circle/` 里，云端会话拿不到，需要出图出片就在 Mac 上跑。
- **skill 正文**在 `docs/skill-kids-english-story-video.md`，分册 `docs/skill-type-talk.md`（口语）、`docs/skill-type-song.md`（儿歌，暂停）、`docs/skill-topics.md`（选题）、`docs/story-psychology-reference.md`（方法论）。共享文件夹 `/mnt/project-files` 里的同名副本是 10-24 ～ 10-28 的旧版，以仓库为准。
- **只留在 Mac、不进仓库的**：旧参考图备份 `series/refs_old_1030/`、`series/refs_v1_1030/`；出图日志 `images.json`、`.codex_images.log`；公司层面的计划（共享文件夹 `company-plan/`，含收入测算，不放公开仓库）。
- **开工前**：`git pull origin claude/funny-franklin-ucpap0`；改完按功能小步提交，直推这条分支。
- **当前进度**：s04 定稿待用户发布；s05 万圣节第 3 版（日常模式、全关键帧）成片做完待发布（11-01 晚）；儿歌线暂停。
- `git stash` 里有一条 10-31 的 HANDOFF 备份（H3 试跑记录），内容已合进下面的 H3 一节，可以丢掉。

## 0. 最新：声音设计升级，c18 加底声试听版待听（2026-11-03 晚）

- 用户要求把小红书 RedSkill 商店的 sound skill（Freesound 搜音效）装到全局，并"彻底吸收"进视频 skill、提高音效品味。
- 装好：`redskill` CLI 在 `~/.local/bin`（Anaconda 的 python3 是 3.7 太旧，包装脚本改成 `/usr/bin/python3`）；sound 在 `~/.agents/skills/sound`，软链到 `~/.claude/skills`、`~/.codex/skills`。SKILL.md 改了脚本路径、删了"B 站 30 元满血版"推销段；`clash_freesound.py --fix` 不要跑（改作者的 ClashX 配置）。原版备份 `SKILL.md.orig`。
- 新分册 **`docs/skill-sound-design.md`**：九条品味规则（卡通音配角色、真实录音配世界、每个场景铺底声、静音也是音效、2–3 岁耳朵的边界……）、找音流程、story.json 写法、质检表。主 skill 和口语分册已链过去。
- sbv.py：顶层 `ambience`（环境底声，单独一层，写法同 `bgm.cues`，默认比人声低 24 dB，`style.amb_rel_db`）；音效加 `skip` / `dur`。不写这两个字段时，混音和改之前逐采样一致（c18 新旧代码对比，差 0）。
- 新工具：`sfx_probe.py`（听不到就看能量曲线：起音、峰值、尾巴）、`sfx_import.py`（Freesound 原始文件切头尾、统一电平进 `assets/sfx/`，出处和授权记进 `series/sfx_sources.csv`，只收 CC0）。
- 第一批 CC0 库：`amb_forest_birds`、`amb_forest_stream`、`rustle_bush`、`rustle_quick`、`steps_grass`、`twig`（原始文件在 `assets/sfx/fs/`）。
- 试听：`out/c18_amb/c18_peekaboo_amb.mp4` = c18 正片同一套配音 + 森林鸟叫底声（反转前和音乐一起抽掉、复习页压低）+ p03、彩蛋页换成真实灌木沙沙声（`episodes/c18-peekaboo/story_amb.json`，不提交）。底声比整体低约 26–28 dB，-15.8 LUFS。用户 11-03 听后说「先这样」：**下一集起口语线默认加底声，音量 volume 1.0**。用户问 sound 会不会选背景音乐：不会，只管音效。
- 踩坑：配音缓存在 `--out` 目录下，换新输出目录会整集重配（这次多花了约三集的 ElevenLabs 字数）。试声音先拷正片 `.cache` 并临时去掉 key，分册第 4 节末尾有命令。

## 0. 最新：m02 拔萝卜英文对话版成片，待发布（2026-11-03 晚）

- 用户 11-03：「放弃找大人唱的思路……保留背景音乐，然后用一个乐器作为唱歌的主旋律……动画人物用英文对话方式」→「剧本能不能更有意思一点」→「画面为啥不动呢，你不要图省事」。剧本 v3 见 `episodes/m02-pull-radish/script.md`、台词 `dialogue_v3.json`（删了 p03「I'm coming!」、p07「Pip did it!」，p01 缩成「Wow! A BIG radish!」，为压时长）。
- 画面 27 张全部重出（旧 22 张在 `out/m02/old_images_v1/`），一次过、没有重出。
- 音乐：本机 `out/m02_talk/`（不进仓库）。`prep_talk.py` 先配音、按 98 BPM 小节排每句并写 story.json + `plan.json`；`bgm_talk.py` 按 plan 用 SF2 音色合成伴奏（木琴照原谱弹主旋律）：Heave-ho!/PULL! 那一小节伴奏停，萝卜拔出来插一小节刮奏+镲，最后和弦落片尾卡。**story.json 的 lead/gap/hold 和 lines 的 audio 都是脚本算的，改台词要重跑 prep_talk.py → bgm_talk.py → sbv.py**。配音加快 5%（atempo），合喊是几个人分别配音再叠。
- 11-03 晚两轮改：用户「背景音乐……可以调大一点点」「以后视频都不要超过 50 秒，控制在 45 秒左右」→ `bgm_rel_db` 改 -8（只改这一集），p01–p04 段音乐再局部压 2 dB（写在 bgm_talk.py）；删 p02「...Oh no!」、p08「Hooray!」，p05 改「Ha ha! So small!」，宝宝跟喊停顿 0.8 秒；停奏不再等小节线（喊的词落在哪一小节就停哪一小节，落在后半段连停两小节）。修了 prep_talk.py 的一个错位 bug（句后停顿没算进 gap，后半段比音乐小节慢 2 秒）。现在 **49.2 秒**，空档音乐比台词低 5–10 dB。
- 成片 `out/m02_talk/m02_pull_radish_talk.mp4`，56.2 秒，qa 格式/响度/字幕对齐/角色声音通过；发音可疑 9 句多为 Heave-ho 连字符、笑声、音效、拟声，**要人耳听的是 p04 合喊和复习页的 Pull 在混音里像 "Pole"**。`qa.py` 改了：合喊、音效句（不在 cast 里的说话人）不参与角色声音比较，预先处理好的 `audio` 句直接用。
- 交付页 https://claude.ai/artifact/BMzteCB53NXtULMZCFqHiM ，顶部有版权提示：背景旋律照原曲《拔萝卜》简谱（署名包恩珠），**发布前先确认授权**。之前的儿歌版原片 `out/m02/m02_pull_radish.mp4` 没动。
- **只有用户能做的**：确认版权、手机终检、点发布。

## 0. 最新：m02 拔萝卜原调英文翻唱，试听中（2026-11-03）

- 用户听了 11-02 的原创旋律版和 ElevenLabs 按文字“往原调靠”的几版，说「根本就不是拔萝卜的原来的歌曲」。文字提示做不出原调，改成按原谱合成。
- **版权**：两份公开简谱（1=F 2/4）都署名「包恩珠 词曲」，不是佚名。用户决定按翻唱做先听效果。**发布或用于卖电子绘本前要先确认授权**，story.json 里「佚名、保护期已过」的说法不对。
- 做法：旋律数据 + 合成脚本都在本机 `out/m02/cover/`（不进仓库）。伴奏用 numpy 合成（木琴、古筝拨弦、低音、木鱼，98 BPM，50 秒）。人声：ElevenLabs 念每句英文 → Praat PSOLA 整句修时值和音高（`psola.py`）。自检：`check.py`（音高逐音对比）、`check_lines.py`（逐句 Whisper 听写）。
- 结果：Pip 声 113 个音都在半音内、逐句听写 20/33（没听对的基本是 Pull，听成 Paul），有合成味。逐音节 WORLD 修音的老办法字太糊，弃用。
- 卡点：ElevenLabs 没有“按外部旋律唱”的功能；Voice Changer 需要 key 有 Speech to Speech 权限，现在没有。
- 试听页：https://claude.ai/artifact/WrVax94pCBSAb3X4NshKWw 。下一步等用户挑版本，或决定找真人照伴奏版录唱。
- 11-03 下午用户：「开权限那个，你帮我操作，先把背景音乐做好」。
  - 背景音乐重做：免费音色库 GeneralUser GS（许可允许商用；`out/sf2/`，不进仓库），自写的极简 SF2 播放器 `out/m02/cover/sf2play.py`（音准逐个乐器测过，±8 音分），编配脚本 `bgm.py` → `bgm_pure.wav`（纯伴奏）、`bgm_lead.wav`（加木琴旋律）。古筝用 Koto 音色代替；“嘿哟嘿哟”小节停奏留空；三段逐渐加厚。已放到试听页最上面，等用户听。
  - 开 Speech to Speech：Chrome 里已登录、找到 key（lili-mac，末尾和 ~/.zshrc 的对上），但切换权限的点击被本机 Claude Code 安全规则拦下（改 key 权限算授权操作），**要用户自己点**：开发者 → API 密钥 → lili-mac「⋯」→ 编辑 → 语音转语音「访问」→ 保存更改。开好后再做 Voice Changer 人声版。
  - conda 环境 `envs/fsynth` 里装了 fluidsynth（装得慢，最后没用上）。
  - 用户 09:07「我不在电脑边，我授权你替我操作」→ 我在 Chrome 里把 lili-mac 的「语音转语音」改成「访问」并保存，其他不动，接口验证 200。
  - Voice Changer 结果：会把音往说话音高拉低 3–8 个半音，`retune.py` 按谱修回；字更糊（逐句听写 Bun 10/33、Pip 9/33，原 PSOLA 办法 20/33）。三版人声 + 新伴奏（`mixbgm.py`）放进试听页，等用户耳朵判断自然度。

## 0. 最新：m02 拔萝卜英文儿歌（国风特别版）成片，待发布（2026-11-02 晚）

- 用户 11-02：「拔萝卜生成一个视频，要童谣，英文版本，50 秒」，画风是用户看过样图的中国水彩画（`episodes/m02-pull-radish/style.json`，样张从 `out/style_tests_guofeng/` 复制到集目录 `style/`，不进仓库）。这集跳过漫画剧本确认，歌由我们自己挑。
- 出图 22 张一次过，没有重出：中国水彩味（宣纸、晕染、远山）没被参考图拉回日系；Bruno 拉萝卜往后仰、膝盖弯；链条 Bruno 抓叶子 → Bun 抱腰 → Pip 抓背心下摆。
- 歌一共出了 8 版，选了 v8（听写平均 0.97，每段 ≥0.8）。前两轮的问题：v2 第一句 Pull 唱成 "ho ho ho"（qa 的 base.en 和 medium.en 都这么听）；Bridge 的 Pop / Pip 常被唱糊。第三轮在 styles 里加了「每个 Pull! 唱成清楚的英文词，结尾带 L」，好了。坑：`direction` 一行不能超过 200 字符（ElevenLabs 422）。
- 成片 `out/m02/m02_pull_radish.mp4`，48.0 秒，qa 有 3 句标「发音可疑」，人工核过：两句 Heave-ho 是连字符和前一句串窗的问题，Yummy radish 的 -ish 唱得轻（前面 A big radish 是清楚的）。封面 `--crop-3x4 0.1`（默认 0.55 中文标题压熊眼睛）。
- 没有 OSS key，交付页用 Artifact 附带文件（视频压到 13 MB 网页版，原片 44 MB 在 Mac）：https://claude.ai/artifact/8UmDTyhD2jr7M87N88hbdX ，附 v2、v1 两版备选歌。
- **只有用户能做的**：手机终检、点发布。

## 0. 最新：c18 躲猫猫成片，待发布（2026-11-01 晚）

- 用户 11-01 要"基于已有爆款"的选题，挑了躲猫猫（CoComelon Peek A Boo 31 亿播放、Where's Spot、剑桥 2012 捂眼研究）。剧本改了 3 版：第 2 版藏身处改成真能挡住身子的（用户："那么窄的树，怎么挡得住"）；第 3 版总长 50 秒、动作关键帧 11→20 张、钩子大字"画面里藏了 2 只小动物，你找到几只？"（栗栗尾巴在远景叶子堆里一直露着），用户回"ok，你按分镜加倍来吧"。
- 漫画剧本：`codex_images.py --comic-all` 新开关，每个动作关键帧一格（30 格），https://claude.ai/artifact/G13Hcpv5m4CrNWh1mg2gsn 。漫画里 p07b 三次都没画对（提示词先写了 p07 主图场景，模型照主图画），工具这点还没修。
- 正式图 41 张；p08 组按新提示词重出 2 次、p06 组重出 1 次。**p08 皮皮还是站在树干前面、没真藏到树后**，两轮没修好，要改提示词再出。
- 成片 `out/c18/c18_peekaboo.mp4`，49.8 秒，`qa.py` 全部通过（`out/c18/qc_full.txt`）。压时长：hold 0.2、页尾 tail 0.7、复习页 lead 0.3；笑声标签挪到 Peekaboo 后面；Bruno 的 "Where?" 两个 take 都被听成 That!，改成 `[slowly] Wheeere?`。qa.py 两处修：Peek-a-boo 连字符并成一个词；VAD 把 Pip 尖声大喊整句滤掉时不带 VAD 再听一次。
- 封面用钩子首帧（Pip + 叶子堆里的尾巴），`brand.py` 中文大字太宽时在逗号后自动断行。OSS 已同步（`out/c18/oss.json`），发布页 https://claude.ai/artifact/D3DUZuiKMF5kTFy5vDsabj 。
- 11-02 说话帧修正（用户：熊说话树在抖）：`SBV_TALK_DEBUG=目录` 渲染，逐张看红框是否在说话人嘴上。坑：底图里说话人本来就张着嘴（p02/p07b/p08/p09），Codex「张嘴」改不出差别 → 张嘴帧提示词改成**闭嘴**；小老鼠嘴太小、熊近景脸太宽 → 台词写 `where`（两人一起说写两个点）。发布页已换成新片（第 6 版）。
- 11-02 试验「一秒一图」：p04–p05 旁白 3 秒里加 3 张 Codex 关键帧（`out/c18_dense/`，不进正片），对比页 https://claude.ai/artifact/YMLDLZNuBbpuNSv8z1yo3W ，用户看后说「效果变得更好了……这次先这样，下次再尝试升级」：c18 正片保持现版；下一集起动作段一秒一张（说台词时不换图），并试一秒两张做对比（skill 5.3.1 已写）。用户补充：加密要非线性，按镜头动作量和信息密度分高/中/低三档分配张数（skill 5.3.1 有表）。
- **只有用户能做的**：手机终检、点发布。

## 0. 最新：s05 第 3 版，日常模式成片（2026-11-01 晚）

- 用户看了 H3 版："剧本给我的感觉就是不连贯，以后不要用这种混合模式了……现在用日常模式重新生成万圣节的视频"。剧本第 3 版（c3ebe3a）理顺连贯：钩子不闪前，影子只在远处探头；p04 栗栗想拿糖哄 Hazel，才发现袋子空了；p05 敲路边大树；Bruno 从树后跳出来；大木头在 p05 先露面，p08 大家坐上去；彩蛋皮皮站在木头那头。story.json 去掉了所有 clip。**没调 minimax，没花 H3。**
- 出图：`codex_images.py` 按提示词指纹重出了 22 张（kling_first、h02–h04、p04–p09 及关键帧、张嘴帧、cover）。p05b 第一次出成"敲灌木"，改了提示词（拳头贴在大树树干上）后连同 p05b_nutty 重出。质检：影子是圆耳朵的大老鼠、圆软、没有五官；p04 有栗栗和 Hazel；p05 大树、灌木、倒下的大木头都在；p06 Bruno 从树后出来；p08 坐在同一根大木头上，大树在后面。主图按顺序拼起来看，是同一条小路上的一个连续故事。p01–p03 沿用旧图。
- 成片：`out/s05/s05_trick_or_treat.mp4`，61.1 秒，1080×1920 30fps，-16.1 LUFS，`qa.py` 全部通过（`out/s05/qc_full.txt`）。音效时间点：p04 bonk 在 2.4 秒，正好是切 p04b 糖砸鼻子那一下；p05 knock 在 4.1 秒，落在旁白说完、等宝宝敲的 2 秒空档里。H3 版留底在 `out/s05/s05_trick_or_treat_h3.mp4`。
- 封面改用 `h02.png` 做底图（影子比首帧大，标题下面看得见），`--fade 30 --crop-3x4 0.2`。publish.txt 改了一句"看到栗栗敲大树的时候"；`xhs/` 换成新图；`share/` 里有 720p 预览，已发到用户手机。
- 打印 PDF、comic.html 还是旧图，没重出。
- **只有用户能做的**：手机终检、点发布；OSS 上传会被 Mac 的安全检查拦下（"Create Public Surface"），要用户自己在终端跑 `cd ~/code/little-circle/tools/storybook-video && .venv/bin/python oss_publish.py ../../out/s05`。

## 0. s05 万圣节成片（2026-11-01，H3 版）

- 用户确认剧本（"OK，先这样。开始生成"），随后改口要用 H3："用H3，我想看看H3能做到多好。30s，720p那一档"。中转站没有 720P，最低是 768P；单条最长 15 秒，所以拆成 6 个 5 秒首尾帧镜头。
- **成品**：用户 Mac 的 `out/s05/`（mp4 62.1 秒、两张封面、publish.txt、xhs/ 10 张、srt、打印 PDF、qc_full.txt），交付副本在 `out/s05/share/`，里面还有 H3 版和纯关键帧版的对比图 `h3_vs_keyframes.jpg`。纯关键帧版留在 `out/s05_kf/`（对应 `story_keyframes.json`，配音是旧 take）。qa 全部通过。
- **H3 结果**（task_id 和提示词都在 `episodes/s05-trick-or-treat/minimax.json`）：每条 768P 5 秒，出片 3.8–5 分钟，接口 cost 都是 0.4555（单位没核实；s04 那条是 3.795，差了 8 倍多，要用户在七七八AI 后台对账）。共提交 8 条，合计 3.644。
  - 比关键帧明显好：p01（刺一根根扎穿床单，连贯自然）、p04（举起袋子从洞里看、糖砸鼻子）、p06（Bruno 笑、发箍滑下来）。
  - 一般：钩子（三个回头、抱成一团是连贯的，但黑影没有"变大"，中间 Bun 一竖一折的耳朵丢了）；p07 第 2 版（糖真的掉到草地上了，最后 0.5 秒栗栗"闪现"到 Bruno 嘴边，和关键帧版那一下硬切差不多）。
  - 不如关键帧：p03 两版都失败（背影走着走着三个转身对脸，又在半秒内跳回背影），这一页用关键帧。
  - 规律：首尾帧的起止姿势差太多（背影 → 回头）就容易乱动；一个镜头只做一个动作最稳；动作常挤在最后 1 秒。
- 本次修的脚本：`sbv.py` 页面 `lead`（开口前留白，给敲门、脚步让位）；`qa.py` 改成逐句截出来用 small.en 听写（整片一次听写会漂、吞短词，同一条片子两次结果不一样），耳语句不算基频；`brand.py` 加 `--title-en/--title-zh/--fade/--zh-size`（封面大字用谜题、别用渐变盖住黑影）；`el_prep.py` thump 提示词（第一版全是 80Hz 以下，像恐怖片低音）；`minimax_video.py` 并行跑时 minimax.json 不再互相覆盖、记出片耗时。
- 配音改动：p05 "Trick... or treat?!" 一句里 v3 只差 2 dB，拆成耳语 + 大喊两句（成片差 12.7 dB）；p04、p06 去掉开头的 [gasps]/[giggles]（先喘/先笑导致字幕早出）；皮皮用 take 5 "I am... BIG!"（原版和栗栗基频太近）。
- **只有用户能做的**：手机终检、点发布（标题用「黑影是谁？万圣节英语小故事」，万圣节当晚已过）；`~/.zshrc` 加 OSS key（这次没同步 OSS）；七七八AI 后台核对 H3 实扣。

## 0. 万圣节 s05《Trick or Treat!》剧本（2026-10-31）

- 用户当天点题："生成一个万圣节主题的剧本，重点让小朋友学会 trick or treat，看怎么做得非常有吸引力"。选题库 c11 提前到今年，改成森林故事 s05：`episodes/s05-trick-or-treat/`（script.md + story.json）。
- 设计：钩子是三人身后的大圆黑影；栗栗袋子漏糖（宝宝先发现）；p05 宝宝一起喊 Trick or treat；反转是 Bruno 扮成老鼠、一路帮大家捡糖。Trick or treat 配固定"敲门 + 伸篮子"动作，说 5 次。对标拆解在 script.md 第 0 节（Super Simple 敲门儿歌、Peppa Pumpkin Party、Go Away Big Green Monster、Blue's Clues 戏剧反讽）。
- 10-31 第 2 版（用户："能不能更有趣一点？看看怎么做成爆款……怎么利用人性"）：黑影改成"猜猜它是谁"的巨型老鼠影子（谜底 Bruno 戴老鼠耳朵），p05 栗栗对着镜头敲门让宝宝敲屏幕，片尾彩蛋皮皮戴熊耳朵 "I am big!"；script.md 第 0 节是人性 × 设计 × 数据表，第 6 节 H3 候选镜头（钩子、糖果雨，先报价），第 7 节发布打法。
- 10-31 用户定（全系列）：结尾不再说 The end. Bye-bye!，改成 3 页今日单词复习（每词复用故事里那张图、角色再说一遍、停 1.5 秒跟读），写进 skill 口语分册第 2 节；大字词卡用现成的 `"word"` 字段。
- 10-31 配乐升级：sbv.py 支持 `bgm.cues` 分段配乐（已用假配音测通：分段、静音、交叉淡入都对）；el_prep.py 加了 bgm_halloween、bgm_tiptoe 和 knock、thump、tada 音效（要在 Mac 上生成）；skill 口语分册 7.1 节写了按情绪曲线配乐的规则；s05 配乐表在 script.md 分镜后。
- 状态：10-31 用户确认，11-01 成片（见上一节）。

## 0. 试接 MiniMax H3 做动作镜头（2026-10-31）

- 用户要试 MiniMax H3，**渠道是七七八AI（ai778.cc）中转**，接口 `https://api.lk888.ai/v1/media/generate` + `/v1/media/status`，模型 `minimax-h3`（`mode` = shouweizhen 首尾帧 / cankaosheng 参考生），图片可 base64 内联。文档 https://ai778.cc/apidoc#model/minimax-h3 不用登录就能看；价格要登录才显示。
- 脚本：`tools/storybook-video/minimax_video.py`，不带 `--go` 只报价不花钱；提交后 task_id 先记进集目录 `minimax.json`，断了用 `--status <id>` 接着查。
- key 放 Mac `~/.zshrc` 的 `AI778_API_KEY`。云端容器连不上 api.lk888.ai（代理拦），实测要在 Mac 上跑。
- 中转站下单即扣，失败自动退款；视频常见 5~60 分钟出。
- **10-31 第一条试跑完成**：s04 钩子 `kling_first.png → h04.png`（提示词 `episodes/s04-brave/h3_hook.txt`），768P 5 秒，**接口返回 cost 3.795（单位没核实；若是元≈0.76 元/秒，比官方贵约 50%）**，约 5 分钟出片。成片 768×1344、5.17 秒、24fps、带音轨，存 Mac `episodes/s04-brave/h3_hook.mp4`（不提交）。角色没融化没走样，首尾帧贴合；缺点是「树枝下沉、Ruby 一只脚悬空」那一下没做出来，紧张感偏弱。**用户看完说「先这样吧，还是有点贵」，H3 暂停**；动作照旧用关键帧动画。日后重启：先查站上其他 H3 型号单价和 cost 单位（3.795 单位没核实），只给 1–2 个动作镜头用、4 秒起。
- 补充：中转站 H3 只有 768P / 2K 两档，768P 已是最低；`minimax_video.py` 默认时长已改 4 秒（最短档）。成片手机查看页 https://claude.ai/artifact/SXgFXEbf6tGVVVyvvyPAzR ，task 记录在 `episodes/s04-brave/minimax.json`。
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
