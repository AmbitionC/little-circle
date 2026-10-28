# 森林小伙伴 · 角色表

> 2026-10-28 用户要求："动画人物不要就局限这么三个，那么多动物呢。各自的性格特征等都不一样。"
> 主角团还是栗栗、Hazel、Bun。其他角色轮流当某一集的主角，或者来客串。每个角色只有一个最鲜明的性格，外加一个看得见的小标志（衣服或道具），方便 2–3 岁的孩子一眼认出来。
>
> **英文外形描述**：出图提示词里一字不差地照抄，`codex_images.py` 靠这句原文认角色、自动带上 `series/refs/<id>.png`。新角色第一次出场前，先跑 `codex_images.py refs` 出参考图。
>
> **声音**：在 `series/cast.json` 里给每个角色挑 ElevenLabs 音色。相近的两个角色要拉开距离：基频差 ≥30Hz，或者语速明显不同。

| id | 名字 | 动物 | 性格（一个词） | 招牌动作 / 口头禅 | 适合讲的主题 |
|---|---|---|---|---|---|
| nutty | 栗栗 Nutty | 红松鼠 | 贪吃、冲动、热心 | 抱着大栗子，"Yum!" | 分享、饿和饱、等待 |
| hazel | Hazel | 小刺猬男孩 | 害羞、老实 | 一紧张刺就"嘭"地竖起来 | 求助、交朋友 |
| bun | Bun | 小灰兔 | 软萌、慢半拍 | 一只耳朵耷拉着，咯咯笑 | 午睡、慢慢来 |
| pip | 皮皮 Pip | 小老鼠 | **最小、最胆小**，但心细、跑得快 | 一害怕就抱住自己的尾巴发抖 | **勇敢**、我也能行 |
| bruno | 布鲁诺 Bruno | 小棕熊 | 力气最大、憨、有点自信过头 | 拍肚子说 "I am big!"，肚子软得像蹦床 | 力气不是万能的、温柔 |
| fern | 小芬 Fern | 小狐狸 | 爱炫耀、蹦得高、点子多 | 耳朵后面别着一片红枫叶，爱摆姿势 | 别着急、轮流 |
| ruby | 露比 Ruby | 小知更鸟宝宝 | 好奇、还不太会飞 | "Peep!"，扑腾小翅膀 | 学新本领、跌倒再来 |
| ollie | 奥利 Ollie | 小猫头鹰 | 爱讲道理、白天老打瞌睡 | 推一推小圆眼镜，"Hoo-hoo, I know!" | 晚安、认识夜晚 |
| rocky | 洛奇 Rocky | 小浣熊 | 爱捣蛋、手巧、爱洗东西 | 什么都要洗一洗 | 洗手、整理、说对不起 |
| dot | 朵朵 Dot | 小鹿 | 温柔、跑得快、容易受惊 | 蝴蝶落在鼻子上就不敢动 | 温柔、陌生的东西 |
| bo | 波波 Bo | 小獾 | 爱看书、慢性子、讲究 | 抱着一本小树叶书 | 安静、耐心 |
| wiggles | 扭扭 Wiggles | 小水獭 | 爱玩水、停不下来 | 头顶顶着一块小圆石头 | 洗澡、玩水、排队 |

## 英文外形描述（出图原文）

- pip: `a tiny gray mouse with big round pink ears, a pink nose and a thin curly tail, wearing a little blue-and-white striped shirt`
- bruno: `a big chubby brown bear cub with a round soft tummy and small round ears, wearing a little orange neckerchief`
- fern: `a slim young orange fox, not a squirrel, with a long pointed fox snout, tall smooth triangular fox ears, black stocking legs and a long fluffy fox tail with a white tip held low, a red maple leaf tucked behind one ear`
- ruby: `a tiny round fluffy baby robin with an orange-red chest and stubby little wings`
- ollie: `a small round brown owl with big amber eyes and tiny round glasses`
- rocky: `a little raccoon with a black eye mask and a striped bushy tail, wearing tiny blue rubber gloves`
- dot: `a gentle little fawn with white spots on her back and big soft ears, wearing a small pink flower behind one ear`
- bo: `a little badger with a black-and-white striped face, holding a small leaf book`
- wiggles: `a little brown otter with a sleek shiny coat and long whiskers, balancing a small round pebble on his head`

主角团的三句（栗栗、Hazel、Bun）见 skill 第 5.2 节，那三句不能改。
