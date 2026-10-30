# 森林小伙伴 · 角色表

> 2026-10-28 用户要求："动画人物不要就局限这么三个，那么多动物呢。各自的性格特征等都不一样。"
> 2026-10-30 用户要求升级："避免用那种没有特色的动物形象来做角色。比如疯狂动物城里面的动物形象，都有自己鲜明的特征……都有非常明确的记忆点。这个非常关键。"方案（含参考依据）见 [docs/character-design.md](../docs/character-design.md)。
>
> 主角团还是栗栗、Hazel、Bun。其他角色轮流当某一集的主角，或者来客串。名字、物种、音色、衣服颜色都没变；2026-10-30 之前已发布和定稿的集不重做，下一集起用新设定。
>
> **英文外形描述**：出图提示词里一字不差地照抄，`codex_images.py` 靠这句原文认角色、自动带上 `series/refs/<id>.png`。升级前的旧描述也还认得（`OLD_DESC`），旧集重出图不受影响。新角色第一次出场前，先跑 `codex_images.py refs --only <id>` 出参考图，再跑 `sheets --only <id>` 出设定图。
>
> **声音**：在 `series/cast.json` 里给每个角色挑 ElevenLabs 音色。相近的两个角色要拉开距离：基频差 ≥30Hz，或者语速明显不同。
> 男孩角色用男孩声，女孩角色用女孩声，**不用女声配男孩、也不用成年人凑"低沉"**（Bruno 换了三轮才定：成年低音、AI 生成音色、女声配童声都被用户否了，2026-10-30 定为音色库的男孩声 Chintu，憨、实在、约 300 Hz）。ElevenLabs 不允许按描述生成儿童声音，新角色只能从音色库挑：筛 gender=male/female + age=young，放进本集画面里试听再选。

## 角色六件套（每个角色都要写齐）

| 件 | 写什么 |
|---|---|
| 1. 一句话反差 | 这种动物大家印象里是什么样，这个角色偏偏怎么样 |
| 2. 剪影钩子 | 一个夸张的身体部位 + 体型档位 + 主形状（圆＝友好软萌，方＝稳当可靠，三角＝尖锐有劲） |
| 3. 情绪器官 | 一个随情绪变化的部位，正好拿来出关键帧 |
| 4. 口头禅 + 招牌动作 | ≤3 个英文词，宝宝能跟着喊；配一个固定动作 |
| 5. 想要 | 驱动剧情的那件事 |
| 6. 小毛病 | 让他出糗、也让他成长的地方 |

**体型阶梯**（同框时按这个比例画，不再一样高）：XS Ruby、Pip ＜ S Nutty、Hazel、Bun ＜ M Fern ＜ XL Bruno（约是朋友们的两倍高）。

**写剧本时**：这一集的主演，口头禅、情绪器官、想要三样至少各出现一次；客串角色至少亮出口头禅或招牌动作之一。

## 主角团

| id | 名字 | 动物 · 体型 · 形状 | 反差 | 剪影钩子 | 情绪器官 | 口头禅 · 招牌动作 | 想要 / 小毛病 | 适合讲的主题 |
|---|---|---|---|---|---|---|---|---|
| nutty | 栗栗 Nutty（男孩） | 红松鼠 · S · 圆＋大尾巴 | 松鼠是囤粮专家，栗栗**藏完就忘了藏在哪** | 尾巴比整个身体还大 | 尾巴：兴奋时炸成毛球，想不起来时卷成问号 | "Yum!" / "Where is it?" · 抱着大栗子，挠头到处挖 | 吃到最大的栗子 / 急，藏完就忘 | 分享、等待、记住；彩蛋：忘掉的栗子长成小树 |
| hazel | Hazel（男孩） | 刺猬 · S · 圆 | 浑身是刺，**偏偏最想要抱抱** | 圆滚滚一个球，刺比身体宽一圈 | 刺：紧张"嘭"地竖起，开心变软趴下，害怕缩成球 | "Hug?" · 张开小手，又缩回去 | 和大家抱抱 / 一害羞就缩成球滚走 | 求助、交朋友、温柔地碰 |
| bun | Bun（女孩） | 灰兔 · S · 圆＋一长一折的耳朵 | 兔子跑得最快，Bun **走到哪睡到哪** | 一只耳朵永远耷拉着盖住一只眼；半眯的困眼 | 耳朵：开心两只都竖起，困了两只都塌下来 | "Wait for me!" · 打哈欠，咯咯笑 | 跟上大家 / 随时睡着 | 午睡、慢慢来、等等别人 |

## 常驻配角

| id | 名字 | 动物 · 体型 · 形状 | 反差 | 剪影钩子 | 情绪器官 | 口头禅 · 招牌动作 | 想要 / 小毛病 | 适合讲的主题 |
|---|---|---|---|---|---|---|---|---|
| pip | 皮皮 Pip（男孩） | 小老鼠 · XS · 小圆＋两只大圆耳 | 全森林最小，**耳朵却比头还大**，什么声音都第一个听见；胆小是因为听得太多 | 一对比头还大的粉色圆耳朵 | 耳朵：害怕时捂住脸，听到动静一只转过去；害怕时抱住自己的尾巴发抖 | "Me too!" · 小跑着跟在大孩子后面 | 被当成大孩子 / 胆小 | 勇敢、我也能行、我会听 |
| bruno | 布鲁诺 Bruno（男孩） | 小棕熊 · XL · 方＋圆肚子 | 最大最壮，**最爱吃蜂蜜，偏偏最怕蜜蜂** | 朋友们的两倍高，宽方肩膀 | 肚子：拍肚子当鼓，软得像蹦床 | "I am big!" · 拍肚子 | 蜂蜜 / 自信过头，又怕小东西 | 力气不是万能的、温柔、怕也没关系 |
| fern | 小芬 Fern（女孩） | 小狐狸 · M · 三角 | 狐狸印象是狡猾，Fern **什么都写在脸上，最藏不住** | 高高的三角耳、耳后一片红枫叶、白尖大尾巴 | 尾巴：得意时竖成旗子，做错事藏到身后 | "Ta-da!" · 单脚摆造型，摆完常常摔一跤 | 被大家看见 / 爱炫耀、抢先 | 别着急、轮流、说实话 |
| ruby | 露比 Ruby（女孩） | 知更鸟宝宝 · XS · 圆球 | 是只鸟，**偏偏还不会飞** | 一个圆毛球，翅膀小得不像能飞 | 红胸脯：不服气、害羞时鼓成一个红球 | "Peep!" / "I can do it!" · 拼命扑腾，只离地一点点 | 飞起来 / 心急 | 学新本领、跌倒再来 |

## 后备角色（设定先定好，轮到出场再出参考图和设定图）

| id | 名字 | 动物 | 反差 · 记忆点 | 口头禅 | 适合讲的主题 |
|---|---|---|---|---|---|
| ollie | 奥利 Ollie | 小猫头鹰 | 爱讲道理，**每次都说错**；头能转一大圈（猫头鹰真能转约 270 度）；白天老打瞌睡 | "Hoo-hoo, I know!" | 晚安、认识夜晚、不知道也没关系 |
| rocky | 洛奇 Rocky | 小浣熊 | 长得像小强盗（黑眼罩），**偏偏是洁癖**，什么都要洗一洗（浣熊真的爱在水里搓食物） | "Wash, wash!" | 洗手、整理、说对不起 |
| dot | 朵朵 Dot | 小鹿 | 腿最长，**偏偏老打滑**，像刚出生的小鹿站不稳 | "Oops!" | 慢慢来、扶一把、陌生的东西 |
| bo | 波波 Bo | 小獾 | **挖洞专家**，什么问题都想挖个洞解决 | "Dig, dig!" | 找东西、动手试试 |
| wiggles | 扭扭 Wiggles | 小水獭 | 有一块**最爱的小石头**，走哪带哪，一丢就天塌了（海獭真的会把喜欢的石头揣在腋下） | "My rock!" | 安抚物、丢了怎么办、借给朋友 |

## 英文外形描述（出图原文）

主角团三句同时写在 skill 第 5.2 节，两边必须一字不差。

- nutty: `a small red squirrel with a huge fluffy tail even bigger than his whole body, round bright eyes, wearing a little green knitted scarf`
- hazel: `a round ball-shaped little hedgehog boy with a wide puffy crown of soft brown spines, rosy cheeks, wearing tiny yellow overalls`
- bun: `a fluffy light-gray bunny with very long ears, one ear always flopped down over her eye, sleepy half-closed eyes, wearing a small red vest`
- pip: `a tiny gray mouse with huge round pink ears even bigger than his head, a pink nose and a thin curly tail, wearing a little blue-and-white striped shirt`
- bruno: `a big chubby brown bear cub, twice as tall as his friends, with broad square shoulders, a round soft tummy and small round ears, wearing a little orange neckerchief`
- fern: `a slim young orange fox, not a squirrel, with a long pointed fox snout, tall smooth triangular fox ears, black stocking legs and a long fluffy fox tail with a white tip held low, a red maple leaf tucked behind one ear`
- ruby: `a tiny ball-shaped fluffy baby robin with a puffed-up orange-red chest and stubby little wings too small to fly`
- ollie: `a small round brown owl with big amber eyes and tiny round glasses`
- rocky: `a little raccoon with a black eye mask and a striped bushy tail, wearing tiny blue rubber gloves`
- dot: `a gentle little fawn with very long thin wobbly legs, white spots on her back and big soft ears, wearing a small pink flower behind one ear`
- bo: `a little badger with a black-and-white striped face, big digging claws and a smudge of dirt on his nose`
- wiggles: `a little brown otter with a sleek shiny coat and long whiskers, hugging his favorite small round pebble to his chest`

## 参考图和设定图

- `series/refs/<id>.png`：单人全身、招牌姿势和默认表情（不再全员正面张嘴笑），出图时自动带上。姿势写在 `codex_images.py` 的 `POSES`。
- `series/sheets/<id>.png`：设定图，正面 + 侧面 + 三个表情，给人看、写剧本时对照，**不进出图流程**（一张多视图当参考图，Codex 会画出好几个同一角色）。表情写在 `FACES`。
- `series/refs/avatars/<id>.png`：字幕旁的说话人头像，参考图换了要跟着 `avatars --force` 重出。
