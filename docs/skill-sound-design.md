# 分册：声音设计（音效、环境底声、选材品味）

> 2026-11-03 建。用户："把 sound 这个 skill 彻底吸收到视频生成的 skill 里……增加一些音效，增强音效方面的品味，提高视频整体质量。"
> 适用于口语线（儿歌线的歌就是全部声音，不加）。配乐分段的做法见 [skill-type-talk.md](skill-type-talk.md) 7.1 节，本分册管音乐以外的声音。

## 1. 先记住这几条（品味）

1. **三层各干各的活**：人声讲故事 → 音效把画面"按实" → 音乐和环境底声给情绪和空间。任何一层抢了人声，都算失败。
2. **真实的世界，卡通的角色**：角色身上发生的事（被砸、弹起、变魔法、灵光一闪）用卡通音（ElevenLabs 做的 pop、boing、bonk、sparkle、ding、tada）；世界里的东西（草、落叶、灌木、树枝、水、木门、纸）用真实录音（Freesound）。全卡通听着像玩具，全真实又不像动画，混着用才对味。
3. **有画面依据才加**：每个音效都要对着画面上看得见的动作或换图，没有依据的不加。一页最多 2 个，一集 15–25 个就够。少而准，胜过满。
4. **落点比音色重要**：冲击音的起音要正好压在换图那一帧（`at` 减掉起音，用 `sfx_probe.py` 量）；预备音（whoosh、吸气）在落点之前结束。差 0.1 秒，耳朵就觉得"不跟手"。
5. **每个场景要有"空气"**：森林里永远有鸟、风、远处的水，一条很轻的环境底声铺满整场，孩子不会注意到，但没有它画面就像贴在白墙上。换场景才换底声。
6. **静音也是音效**：反转前 0.3–0.5 秒把音乐和底声一起抽掉，让人屏住气，再让 sting 和欢快音乐一起进。复习页底声压低，跟读空档要安静。
7. **给 2–3 岁耳朵的边界**：不要突然很响（峰值统一、一个音效不能比人声响）、不要刺耳高频、不要吓人的声音（尖叫、打雷、狼嚎、惊悚 drone、"eerie / horror / cinematic" 类）、不用真实孩子的哭声和笑声（角色的笑由配音来，真实儿童录音也有隐私顾虑）。
8. **重复就是品牌**：同一个动作整季用同一个声音（Pip 冒出来 = pop，反转 = tada，片头 jingle_in）。新声音进库起名字，以后按名字复用，不每集临时找。
9. **节奏音效跟着剧情加速**：蓄力和寻找段用会重复的声音（脚步、心跳、灌木沙沙），一次比一次近、一次比一次快，到反转那一下停。

## 2. 音效库和出处

- 库在 `assets/sfx/`（不进仓库）。出处和授权记在 **`series/sfx_sources.csv`**（进仓库）：Freesound 编号、作者、授权、下载量和评分、切了哪一段。
- ElevenLabs 生成的卡通音：清单在 `el_prep.py` 的 `SFX`，`docs/elevenlabs-workflow.md` 1.3 节。
- Freesound 真实录音（2026-11-03 第一批，全部 CC0）：

| 名字 | 是什么 | 怎么用 |
|---|---|---|
| `amb_forest_birds.wav` | 瑞典森林清晨鸟叫（Zoom H6 实录），60 秒 | 森林场景默认底声 |
| `amb_forest_stream.wav` | 森林小溪 + 鸟叫，60 秒 | 有水、河边的场景 |
| `rustle_bush.wav` | 在灌木里翻找的沙沙声，4.8 秒 | 躲、找、钻进灌木；用 `dur` 截短 |
| `rustle_quick.wav` | 拨一下灌木，2.8 秒 | 探头、冒出来前的一下 |
| `steps_grass.wav` | 草地脚步，2.5 秒 | 走路、靠近 |
| `twig.wav` | 树枝咔嚓一声，0.6 秒 | 踩断树枝、紧张段的意外声 |

- **待补**（用到时再找，找到按第 3 节进库）：小雨、风吹树梢、夜里虫鸣（睡前集）、水花、咬苹果、木门敲门（实录版，和 ElevenLabs 的 `knock` 对比）、翻纸页（实录）、轻心跳、拔萝卜时根离开土那一下、一屁股坐在草地上。

## 3. 缺一个声音时怎么找（sound skill）

1. **先查库**：`series/sfx_sources.csv` 和 `assets/sfx/` 里有没有能用的，能复用就复用（第 1 节第 8 条）。
2. **卡通音缺** → 在 `el_prep.py` 的 `SFX` 加一条，`el_prep.py sfx <名字>` 生成（付费档期间）。
3. **真实声音缺** → 用全局 sound skill（`~/.agents/skills/sound`）在 Freesound 搜：
   ```bash
   S=~/.agents/skills/sound/scripts/sfx.py
   /usr/bin/python3 $S freesound "bush rustle" --license cc0 -n 8          # 加 --urls 给用户试听
   /usr/bin/python3 $S get assets/sfx/fs fs:59315 fs:106114               # 一次 get 多个，并发下载
   ```
   - 搜索词用**英文的具体东西 + 材质 + 动作**："footsteps grass"、"twig snap"、"wooden door knock"，不要 "walking sound"。
   - **只用 CC0**（`--license cc0`）。BY 要署名、BY-NC 不能商用，都不用。
   - 我们听不到，靠听过的人留下的证据挑：下载量高、**评分人数多**（★4.4(380) 比 ★4.9(6) 可信）、描述里写清楚录的是什么、用什么录的（Zoom、Sound Devices、具体话筒）。描述是别的东西、写着 "made with my mouth / built-in mic"、带 "cinematic / dark / eerie / horror" 的不要。
   - 热门不等于合适：先看时长，下载后用 `sfx_probe.py` 看形状。
   - Freesound 每个连接限速约 80 KB/s，一条 3–6 分钟的环境录音要下 5–7 分钟，放后台跑。网络走终端代理（`127.0.0.1:7897`）。**不要跑 sound skill 里的 `clash_freesound.py --fix`**，它会改作者自己的 ClashX 配置。
4. **看形状**（听不到就看能量曲线）：
   ```bash
   cd ~/code/little-circle && export PATH=~/Downloads/Anaconda3/anaconda3/envs/sbv-ffmpeg/bin:$PATH
   tools/storybook-video/.venv/bin/python tools/storybook-video/sfx_probe.py assets/sfx/fs/*.mp3
   tools/storybook-video/.venv/bin/python tools/storybook-video/sfx_probe.py --curve assets/sfx/fs/fs_59315*.mp3
   ```
   每个文件给出起音、峰值、有效尾和建议的 `skip / dur`。`--curve` 打印每 0.1 秒的能量条，能看出有几下、间隔多少、尾巴多长。
5. **进库**（切头尾、统一电平、记出处）：
   ```bash
   tools/storybook-video/.venv/bin/python tools/storybook-video/sfx_import.py assets/sfx/fs/fs_59315_looking_in_bushes-wav.mp3 rustle_bush
   tools/storybook-video/.venv/bin/python tools/storybook-video/sfx_import.py assets/sfx/fs/fs_577623_*.mp3 amb_forest_stream --bed --skip 20
   ```
   单个音效峰值统一到 -1 dBFS（和 ElevenLabs 那套差不多响，`gain` 可以照旧用 0.3–0.55）；底声（`--bed`）切 60 秒、按响度统一、首尾淡 1 秒。非 CC0 会拒收。出处自动写进 `series/sfx_sources.csv`，**记得提交这个文件**。

## 4. 写进剧本和 story.json

- **script.md**：分页表的"音效"一列写名字和落点（"p03 rustle_bush 开场、boing 在 Pip 冒头"）；配乐表后面加一行**底声**（哪段用哪条、哪里抽掉）。
- **音效**（页面 `sfx`，和以前一样）：`{"file": "../../assets/sfx/rustle_bush.wav", "at": 0.1, "gain": 0.35, "dur": 2.2}`
  - 新字段 `skip`（从音效第几秒开始用）、`dur`（最多用几秒，切口自动淡出），用来临时截一段，不用另存文件。
  - 台词期间的音效 `gain` ≤0.35；开口前的音效在第一个词前 0.3 秒结束（页面 `lead` 默认 0.5 秒）。
- **环境底声**（顶层 `ambience`，单独一层，不进人声轨，所以不会触发压音乐）：
  ```json
  "ambience": {"cues": [
    {"page": 0, "file": "../../assets/sfx/amb_forest_birds.wav", "volume": 1.0, "fade": 1.0},
    {"page": 6, "offset": -0.35, "file": null, "fade": 0.2},
    {"page": 6, "file": "../../assets/sfx/amb_forest_birds.wav", "volume": 1.0, "skip": 12, "fade": 0.3},
    {"page": 9, "file": "../../assets/sfx/amb_forest_birds.wav", "volume": 0.5, "skip": 25, "fade": 0.6}
  ]}
  ```
  字段和 `bgm.cues` 一样（`page` 0 是钩子，`offset`、`file: null` 静音、`fade`、`skip`）。`volume: 1.0` = 比人声低 24 dB（`style.amb_rel_db`），说话时和音乐一起再压 6 dB。只写 `"file"` 就整片一条。
  - 反转前的静音：底声的 `null` 和配乐的 `null` 放在同一个 `offset`。
  - 复习页压到 0.5 或关掉；紧张段可以换更安静的一条或压到 0.6。

**试声音别重配音（2026-11-03 踩过）**：配音缓存在 `--out` 目录下的 `.cache`，换一个新的输出目录就会把整集重新送 ElevenLabs，花额度而且每次念法不一样，没法对比。试音效、底声时，先把正片的缓存拷过去，并临时去掉 key，缓存没命中就报错而不是扣费：

```bash
cp -R out/c18/.cache out/c18_try/ && (unset ELEVENLABS_API_KEY; cd tools/storybook-video && .venv/bin/python sbv.py ../../episodes/c18-peekaboo/story_try.json --out ../../out/c18_try)
```

## 5. 质检（声音这一关）

| 检查什么 | 合格线 | 不合格怎么修 |
|---|---|---|
| 落点 | 每处换图配的冲击音，起音和换图帧差 ≤0.05 秒（抽帧 + `sfx_probe.py` 的起音时间对一下） | 调 `at` |
| 盖台词 | 音效不压住任何一句的第一个词；faster-whisper 逐句听写不因音效出错 | 挪到句前 0.3 秒或句后，或降 `gain` |
| 底声 | 没台词的地方能听出"在森林里"，但第一反应听到的是音乐；量出来底声比人声低 20–28 dB | 调 `volume` 或 `style.amb_rel_db` |
| 静音点 | 反转前音乐和底声同时空 0.3–0.5 秒 | 两条 cues 的 `offset` 对齐 |
| 边界 | 没有比人声响的音效、没有吓人的声音、没有真实孩子的声音 | 换音或降 `gain` |
| 授权 | 这集用到的 Freesound 音效全在 `series/sfx_sources.csv`，全是 CC0 | 补记录或换音 |
| 耳朵 | 关掉画面只听一遍：能听出每页在发生什么；再手机外放听一遍 | 按上面几行修 |
