# ElevenLabs 配音与音频工作流

目标：用好 ElevenLabs 的三项能力——**角色配音、音效、背景音乐**，并且每一集都达到下面的交付标准。

## 0. 总体安排

| 用什么 | 在哪用 | 做什么 |
|---|---|---|
| ElevenLabs **网页** | 浏览器 | 选角试听、设计音色（必须用耳朵听，所以在网页做） |
| **API key + `tools/storybook-video/sbv.py`** | 你的 Mac（推荐），或配好 key 的云端会话 | 每集批量配音，拿到每个词的时间戳，直接出片 |
| **官方技能包** `elevenlabs/skills` | 本地 Claude Code | 一次性生成系列音效库和背景音乐，以后需要时再补 |
| 官方 MCP 连接器（可选） | claude.ai 或 Claude Code | 写剧本时临时试听某一句；不用于批量出片 |

## 1. 一次性准备（第 0 周做完，约 3 小时）

### 1.1 账号与 key（15 分钟）

1. 订阅 **Starter**。免费档不能商用。
2. 新建 API key：
   - 权限只勾这三项：文字转语音、读取音色、音效。如果要生成音乐，再加上音乐。
   - 设置每月额度上限。
3. 把 key 配到环境变量里，不要发进聊天，也不要提交进仓库：
   - **本机**：执行 `echo 'export ELEVENLABS_API_KEY=你的key' >> ~/.zshrc && source ~/.zshrc`
   - **云端会话**：在会话标题栏打开云环境菜单 → Edit → Network secrets，新增 `ELEVENLABS_API_KEY`。新开的会话才会读到。
4. 本机安装官方技能包：`npx skills add elevenlabs/skills`
5. （可选）安装官方 MCP：
   - 执行 `claude mcp add --transport http elevenlabs https://api.elevenlabs.io/v1/mcp`
   - 然后在 Claude Code 里输入 `/mcp`，完成登录。

### 1.2 选角：每个角色一个固定音色（约 1.5 小时）

在网页的 Voice Design 里，用英文描述生成候选音色。每个角色出 3 个，用下面的试音句逐个听。也可以在 Voice Library 里筛选"角色 / 动画"类音色。

| 角色 | Voice Design 描述 | 试音句 |
|---|---|---|
| 旁白 narrator | A warm, gentle female storyteller with a soft American accent, speaking slowly and clearly to a three-year-old at bedtime, smiling, calm and cozy. | Nutty finds a big, big acorn. Can he open it? |
| 栗栗 Nutty（小松鼠） | A cheerful, high-pitched cartoon squirrel character, playful and bouncy, curious and excited, very clear American English, like the sidekick in an animated preschool show. | Wow! Look at this big, big acorn! It's mine! |
| Hazel（小刺猬） | A sweet, gentle, slightly shy cartoon hedgehog girl, soft and warm, high-pitched, kind and polite, clear American English. | I am so hungry. Can I have some, please? |
| Bun（小兔子） | A soft, cuddly cartoon bunny boy, a little slow and shy, round gentle tone, clear pronunciation. | One, two, three! I have an orange carrot! |

挑选时注意：
- **用手机外放听**，音量调到睡前那么小。孩子就是这样看视频的。
- **三个角色的音高要拉开**，闭上眼睛也能分清谁在说话。
- 如果描述里写"child"被拒绝，就改写成"cartoon character, high-pitched, playful"。

选定后，把四个 Voice ID 填进 [`series/cast.json`](../series/cast.json)。**整季不换音色**，每集的 story.json 只写 `"cast": "../../series/cast.json"`（相对路径）。

`cast.json` 里的参数是起点，试音时按下面的方向微调：

| 参数 | 往大调 | 往小调 |
|---|---|---|
| stability（稳定度） | 更平稳、更像同一个人 | 情绪更丰富，但容易飘 |
| style（风格强度） | 更夸张 | 更朴素 |
| speed（语速） | 更快 | 更慢；旁白建议 0.85–0.9，给 3 岁孩子听 |

### 1.3 系列音效库（约 30 分钟，用技能包或网页的 Sound Effects 生成）

文件统一放在 `assets/sfx/`，story.json 里按文件名引用。

| 文件名 | 生成描述（英文） |
|---|---|
| pop.mp3 | cute cartoon pop, short and bright |
| bonk.mp3 | soft cartoon wooden bonk on the head, funny, not painful |
| crack.mp3 | a nut shell cracking open, crisp, cartoon style |
| whoosh.mp3 | gentle soft whoosh transition |
| sparkle.mp3 | magical twinkling sparkle chime |
| ding.mp3 | single bright bell ding, idea moment |
| boing.mp3 | springy cartoon boing |
| chomp.mp3 | cute cartoon chomp and munch |
| tummy.mp3 | funny little tummy rumble, cartoon |
| snore.mp3 | tiny cute cartoon snore |
| leaves.mp3 | footsteps rustling through autumn leaves |
| page.mp3 | soft storybook page turn |
| jingle_in.mp3 | music box jingle C5 E5 G5 C6, cheerful, 2 seconds |
| jingle_out.mp3 | music box jingle C6 G5 E5 C5, gentle ending, 2 seconds |

### 1.4 背景音乐（三首，整季复用）

用技能包或网页的 Music 生成。统一要求：纯器乐、不要人声、可以循环、60–90 秒。

| 文件名 | 情绪 | 描述 |
|---|---|---|
| bgm_play.mp3 | 俏皮 | playful music box and pizzicato strings, 90 BPM, C major, light and bouncy, preschool cartoon |
| bgm_calm.mp3 | 安静 | soft music box lullaby, sparse, slow, warm and cozy bedtime |
| bgm_happy.mp3 | 庆祝 | happy glockenspiel and ukulele with light shakers, celebration, 90 BPM |

生成的音效和音乐能否商用，以 ElevenLabs 当前条款为准。生成前看一眼套餐说明。

## 2. 每集流程（目标：一集 2–3 小时）

1. **剧本**：Claude 按系列规范写剧本和 story.json，每句台词注明说话角色。
   - 需要情绪的句子，加一个 `say` 字段，带上 v3 语气标签，例如：
     ```json
     {"speaker":"nutty", "en":"Wow! Look at this big acorn!", "say":"[excited] Wow! Look at this big acorn!"}
     ```
   - 字幕只显示 `en`，标签不会出现在画面上。
2. **配音**：运行 `python sbv.py story.json --out out/`，自动逐句配音并拿到时间戳。按句缓存，重跑不会重复扣费。
3. **逐句试听**，对照下面的交付标准：
   - 哪句不满意，就在这句上加 `"take": 2`（再不行改 3）重新生成，其他句子不动。
   - 想换语气就改 `say`，想调语速就改 `cast.json` 里的参数。
4. **加音效**：在页面的 `sfx` 里引用音效库，例如 `{"file":"../../assets/sfx/crack.mp3","at":1.2,"gain":0.55}`。
5. **加音乐**：在 `bgm` 里选三首中的一首。有人说话时，脚本会自动把音乐压低一半。
6. **出片**：再跑一次 sbv.py（配音读缓存，很快），得到视频、字幕文件和打印版 PDF。
7. **自动检查**：
   ```bash
   ffmpeg -nostats -i out/xxx.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:"
   ffprobe -v error -show_entries stream=width,height,r_frame_rate -of compact out/xxx.mp4
   ```
8. **手机终检**：用手机看一遍。重点看三处：前 2 秒、字幕有没有被平台界面挡住、睡前的小音量下能不能听清。
9. **发布**：勾选"内容由 AI 生成"声明，并把数据记进 `tracking/videos.csv`。

## 3. 交付标准

| 项 | 标准 | 怎么检查 |
|---|---|---|
| 角色音色 | 每个角色始终是 `cast.json` 里的同一个音色 | 只从 cast.json 读取，不在单集里改 |
| 发音 | 没有读错、吞字或奇怪的重音；角色名 Nutty、Hazel、Bun 读法前后一致 | 人工逐句听 |
| 语速 | 旁白明显慢于日常说话，3 岁孩子能跟上 | 人工 |
| 情绪 | 和剧本标注一致：开心、惊讶、难过分得出来 | 人工 |
| 音质 | 没有爆音、杂音、电流声，句子不被截断 | 人工 + 峰值检查 |
| 句长 | 每句 3–8 个英文单词（系列规范） | 审剧本时检查 |
| 字幕同步 | 高亮的词和发音对得上，肉眼看不出差 | 抽查 3 句 |
| 混音 | 说话时音乐压低，音效不盖住台词 | 人工 |
| 响度 | -16 LUFS（±1），峰值不超过 -1.5 dBFS | ebur128 检查 |
| 画面格式 | 1080×1920、30fps | ffprobe |
| 合规 | 使用付费档商用授权；发布时勾选 AI 声明 | 发布前确认 |

## 4. 额度预算（Starter：每月约 3 万字符额度）〔估算，按实际用量校准〕

| 项 | 估计用量 |
|---|---|
| 选角试音（一次性） | 3,000–5,000 |
| 每集配音，含重录 | 一集 20–45 秒，约 400–800 字符，按 1.5 倍重录算，约 1,000 |
| 一个月 12–16 集 | 12,000–16,000 |
| 音效、音乐（一次性） | 按官网计价，第 0 周做完后看余额 |

第 0 周结束时，如果剩余额度低于 15,000，有两个选择：
- 减少重录、降低音乐生成次数；
- 升级 Creator（约 22 美元）。升级前先核对，是否会超出当月 300 元的总预算。

## 5. 常见问题

- **v3 的语气标签更生动，但不返回时间戳怎么办？** 脚本会自动改用普通接口，高亮改按声音能量估算。短句的误差通常看不出来。如果某句要求严格同步，就用 v2。
- **某一句怎么都读不对？**
  - 改写成更口语的拼法。
  - 用标点控制停顿，例如加逗号或省略号。
  - 实在不行，拆成两句。
- **想换某个角色的声音？** 只在换季时换，换完更新 `cast.json`，并重配这一季已经发布内容的合集版。
