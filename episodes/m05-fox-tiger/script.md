# M05 · Look Behind You! 狐假虎威（国风水彩 · H3 全视频版）

> 2026-11-09。小老鼠上灯台两版（m04）用户都嫌「一般、没新意」，说「换个剧本吧……找个中国童话寓言故事也行」，在新三选一里选了**狐假虎威**。
> 模式：**全片 H3 真视频**（8 段），复习卡用关键帧。画风中国水彩（`style.json`，同 m02/m04）。角色全新：小狐狸、大老虎、小鸡（`characters.json`），小兔、小鹿各出现一次，只靠描述。
> 素材：《战国策·楚策》「狐假虎威」，公有领域。背景音乐原创（乐器），不用任何现成曲子。

## 0. 对标和人性

**数据（B 站按播放排序，2026-11-09 在用户 Mac 上不登录查）**：中国寓言照着讲的儿童动画播放都低（《守株待兔》儿童版 14 万、《小猴子下山》5 万）；火的是「老寓言 + 反转」的 1 分钟内短视频：《孔融让梨？》1668 万、《新司马光砸缸》217 万、《新乌鸦吃肉》129 万。所以这一集＝家长人人知道的寓言 + 一个想不到的结尾。抖音站内数据云端拿不到。

| 人性 | 怎么用 | 拉动哪个数据 |
|---|---|---|
| 熟悉感 | 成语家长都知道；钩子一出狐狸前面走、老虎后面跟，就认出来了 | 2 秒跳出率 |
| 信息差（观众知道角色不知道） | 宝宝看得见老虎，狐狸看不见。S3 大字「宝宝快喊：Look behind!」，S4 狐狸对镜头得意时停一拍等宝宝喊 | **隔屏喊、家长拍娃** |
| 大个子反差 | 老虎是个软萌大猫，只会笑着挥手 | 笑 |
| 反转 | 老虎走后狐狸又耍威风，被一只小鸡 "Peep!" 吓上竹子 | 完播、"没想到"评论 |
| 彩蛋 | 小鸡坐上老虎头，狐狸挂在竹子上红着脸 "I am... small." | 看到最后、转发 |

## 1. 概要

- **Logline**：小狐狸在竹林里大摇大摆，小兔、小鹿见了就跑，他以为自己最厉害——其实身后一直跟着一只大老虎。宝宝喊 "Look behind!"，狐狸一回头，吓得蹦起来。老虎笑着挥挥手走了。狐狸又抖起来，结果一只小鸡 "Peep!" 一声，把他吓上了竹子。
- **今日单词**：big 大 · small 小 · look 看 · run 跑（big ×4、look ×3、run ×2、small ×1）
- **道理**：借别人的威风不是真本事（对 2–3 岁：吓唬人不算厉害）。
- **用了哪些手法**：信息差 + 隔屏喊（Look behind）；三次阶梯（兔跑 → 鹿跑 → 狐狸自己被吓）；大个子软萌；最小的赢；口头禅 "I am BIG!"。
- **常理和安全**：老虎全程闭嘴笑、不露牙不露爪，是大毛绒玩具感；没人受伤；狐狸爬竹子是吓的，不是摔的。

## 2. 镜头表（全片约 45 秒）

每段一个 H3 镜头、一个连续动作，首帧是过了质检的水彩图，只给首帧 + 动作提示词；S7（小鸡吓狐狸上竹子）用首尾帧锁住结果。片段各 5 秒，剪到下表时长，转 30fps，丢模型音轨。同一条竹林小路，从前往后走，一条时间线。

| 段 | 时长 | 首帧 → H3 动作 | 台词 | 大字 / 音效 |
|---|---|---|---|---|
| S1 钩子 | 5.0 | f1：狐狸昂首朝镜头走，身后老虎踮脚跟着 → **狐狸大摇大摆往前走、尾巴一甩一甩；老虎学着他的步子踮脚跟上**，镜头缓缓后退 | **fox**：`I am BIG!`<br>我最厉害！ | 大字「宝宝，狐狸后面是谁？」；踮脚的"哒、哒"音效 |
| S2 兔跑 | 5.0 | f2：小兔吃胡萝卜抬头 → **小兔耳朵"嘣"地竖起，胡萝卜一丢，转身蹦跑** | **bunny**：`Run!`<br>快跑！ | 胡萝卜落地"咚" |
| S3 鹿跑 | 5.0 | f3：小鹿在溪边抬头 → **小鹿一跃跳过溪水跑远；狐狸拍着胸脯得意** | **fox**：`Ha ha! I am SO big!`<br>哈哈！我太厉害了！ | 大字「宝宝快喊：Look behind!」；溪水哗 |
| S4 隔屏喊 | 5.0 | f4：狐狸叉腰对镜头，老虎在他头顶探出脸 → **狐狸对着镜头得意挑眉；老虎在他身后对镜头眨眨眼、竖手指"嘘"**（锁机位） | **fox**：`Who is big? Me!`<br>谁最厉害？我！<br>（停 1.2 秒等宝宝喊）<br>**fox**：`Look... behind?`<br>看……后面？ | 音乐停，只留竹叶沙沙 |
| S5 回头 | 5.0 | f5：狐狸和老虎脸对脸 → **狐狸慢慢转身，看见大脸，原地蹦起来、毛全炸开；老虎笑眯眯挥挥爪** | **fox**：`TI-TIGER!`<br>老……老虎！<br>**tiger**：`Hi!`<br>嗨！ | 炸毛"噗"、弹簧"嘣" |
| S6 老虎走了 | 5.0 | f6：老虎打着哈欠往小路深处走 → **老虎慢悠悠走远；狐狸拍拍毛，左右看看，又挺起胸** | **fox**：`Phew... I am BIG!`<br>呼……我还是最厉害！ | 音乐回来，变得神气 |
| S7 小鸡 | 5.5 | f7 → f7e（首尾帧）：狐狸昂首走，草里冒出一只小鸡 → **小鸡"啾"一声，狐狸吓得一蹦三尺，噌噌爬上竹子抱紧** | **chick**：`Peep!`<br>啾！<br>**fox**：`Help!`<br>救命！ | 大字「狐狸怕谁？」；"啾" + 爬竹子"嗖嗖" |
| S8 彩蛋 | 5.0 | f8：老虎回来趴着，小鸡坐在老虎头上，狐狸挂在竹子上 → **小鸡在老虎头上蹦一蹦，老虎笑得肚子一颤一颤，狐狸红着脸把耳朵耷下来** | **fox**：`I am... small.`<br>我……是小不点。 | 笑声（走音效层）、滑稽"叮" |
| 复习 | 4.0 | r1（关键帧慢推）：老虎晒太阳睡着，小鸡睡在他头上，狐狸靠着老虎笑 | （无台词） | 复习卡：big 大 · small 小 · look 看；音乐收尾 |

合计约 45 秒。台词 12 句，都在 1–5 个词。超时先砍 S2、S6 的尾巴，不砍 S4 的停顿。

**音乐**：原创，笛子 + 琵琶 + 木鱼的小步舞曲。狐狸走路时木鱼踩在他的步子上，老虎踮脚每一步一个低音"咚"（S1 的笑点：两种步子叠在一起）。S4 停音乐只留竹叶声；S5 一下弹簧音；S7 小鸡"啾"之后全停半拍再接滑稽下行。全片固定电平。
**环境底声**：竹林风声、鸟叫（CC0）。

## 3. H3 动作提示词

> 每段一个文件 `h3_s1.txt`…`h3_s8.txt`，`minimax_video.py <集> s1 --first f1.png --prompt-file h3_s1.txt --duration 5`（不带 --go 只报价）。S7 用 `--first f7.png --last f7e.png --duration 6`。画风句从 `style.json` 的 `video_style` 读。

## 4. 出图提示词

> 先出 `char_fox`、`char_tiger`、`char_chick` 三张角色设计图，挑好后拷成 `refs/fox.png`、`refs/tiger.png`、`refs/chick.png`，再出 f1–f8、f7e、r1。一律大圆眼；老虎全程闭嘴、不露牙爪。

**char_fox.png**
```
character design sheet of ONE character only, standing on two legs, front view, full body, centered, plain warm rice-paper background, nothing else: a small slim young fox about the height of a small rabbit, bright orange-red fur with a white chest and white tail tip, big pointy ears, big round shiny amber eyes with white highlights (round, not narrow), a small black nose, a big fluffy tail, a tiny red Chinese knot tassel tied around his neck; looks cheeky and a bit show-off, cute not sly, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**char_tiger.png**
```
character design sheet of ONE character only, standing on all fours, front view, full body, centered, plain warm rice-paper background, nothing else: a big chubby friendly tiger, soft orange fur with dark brush-stroke stripes, the Chinese character-like stripe mark of three short lines on his forehead like a classic Chinese painted tiger, big round gentle amber eyes with white highlights (round, not narrow), round soft cheeks, a calm sleepy friendly smile with mouth closed and no teeth showing, big soft round paws with no claws; cuddly like a big plush toy, never scary, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**char_chick.png**
```
character design sheet of ONE character only, front view, full body, centered, plain warm rice-paper background, nothing else: a tiny round fluffy yellow baby chick, smaller than a fist, a little orange beak, big round shiny black eyes with white highlights, two tiny wings, one little tuft of fluff on top of the head, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f1.png**
```
a sunny morning in a calm green bamboo forest, one winding pale dirt path running from the front toward the back, tall soft bamboo stalks on both sides, light mist far behind; [[fox]] struts down the path toward the viewer with his chest puffed out, chin up, big round eyes shining proudly and looking ahead, big tail held high; a few steps behind him on the path [[tiger]] tiptoes after him quietly with a curious friendly smile, the tiger is huge, about four times as tall as the fox, the fox does not see him; SIZE IS VERY IMPORTANT: the tiger is gigantic next to the little fox, about four times as tall as the fox, the fox's head only reaches up to the tiger's knee, and one tiger paw is as big as the fox's whole body, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f2.png**
```
a sunny morning in a calm green bamboo forest, one winding pale dirt path running from the front toward the back, tall soft bamboo stalks on both sides, light mist far behind; beside the path a small fluffy white bunny with long ears and big round pink-and-black eyes sits eating a carrot; she looks up at [[fox]] coming along the path, and behind the fox the big [[tiger]] peeks over his head with a friendly smile; the bunny's ears shoot straight up and her eyes go wide; SIZE IS VERY IMPORTANT: the tiger is gigantic next to the little fox, about four times as tall as the fox, the fox's head only reaches up to the tiger's knee, and one tiger paw is as big as the fox's whole body, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f3.png**
```
a sunny morning in a calm green bamboo forest, one winding pale dirt path running from the front toward the back, tall soft bamboo stalks on both sides, light mist far behind, a small clear stream crossing beside the path; a small spotted baby deer with big round dark eyes has just lifted her head from drinking at the stream, eyes wide, about to leap away; on the path [[fox]] puffs his chest and points to himself proudly; the big [[tiger]] stands quietly right behind the fox, smiling; SIZE IS VERY IMPORTANT: the tiger is gigantic next to the little fox, about four times as tall as the fox, the fox's head only reaches up to the tiger's knee, and one tiger paw is as big as the fox's whole body, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f4.png**
```
a sunny morning in a calm green bamboo forest, one winding pale dirt path running from the front toward the back, tall soft bamboo stalks on both sides, light mist far behind; medium close shot: [[fox]] stands facing the viewer with paws on his hips and a smug grin, chin up; right behind him the big friendly face of [[tiger]] leans down over the fox's head, only a little above it, looking at the viewer with a gentle closed-mouth smile and raised eyebrows like a shared secret; the fox still does not know; SIZE IS VERY IMPORTANT: the tiger is gigantic, his face alone is wider than the whole fox is tall, his chin rests just above the fox's ears and his big body fills the background behind, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f5.png**
```
a sunny morning in a calm green bamboo forest, one winding pale dirt path running from the front toward the back, tall soft bamboo stalks on both sides, light mist far behind; [[fox]] has turned around and is face to face with the big round face of [[tiger]], the fox jumps straight up into the air in fright, all his fur standing on end, tail puffed huge, eyes like big round saucers; the tiger smiles sweetly and lifts one soft paw to wave hello, mouth closed; SIZE IS VERY IMPORTANT: the tiger is gigantic, he crouches low so his face is level with the fox, and his face alone is bigger than the whole fox, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f6.png**
```
a sunny morning in a calm green bamboo forest, one winding pale dirt path running from the front toward the back, tall soft bamboo stalks on both sides, light mist far behind; the big [[tiger]] strolls away down the path toward the misty back with a lazy happy yawn, mouth only a little open with no teeth showing; in front [[fox]] brushes off his fur, looks left and right, then puffs his chest again with a sly grin, alone on the path, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f7.png**
```
a sunny morning in a calm green bamboo forest, one winding pale dirt path running from the front toward the back, tall soft bamboo stalks on both sides, light mist far behind; [[fox]] struts proudly along the path, chin up; in the tall grass beside the path a tiny [[chick]] has just popped up, looking at him; sizes: the chick is smaller than the fox's paw, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f7e.png**
```
a sunny morning in a calm green bamboo forest, one winding pale dirt path running from the front toward the back, tall soft bamboo stalks on both sides, light mist far behind; [[fox]] clings to a tall bamboo stalk high above the path with all four paws, shaking, fur standing up, eyes huge with fright; on the path below the tiny [[chick]] looks up at him with a puzzled tilted head, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f8.png**
```
a sunny morning in a calm green bamboo forest, one winding pale dirt path running from the front toward the back, tall soft bamboo stalks on both sides, light mist far behind; the big [[tiger]] has come back and lies on the path smiling, the tiny [[chick]] sits on top of the tiger's head; both look up at [[fox]] who hangs from the bamboo stalk above with a sheepish blushing face, ears down; the tiger laughs with mouth closed, the chick giggles, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**r1.png**
```
a sunny morning in a calm green bamboo forest, one winding pale dirt path running from the front toward the back, tall soft bamboo stalks on both sides, light mist far behind; peaceful ending: the big [[tiger]] sleeps curled up on the path in the warm sun, the tiny [[chick]] asleep on his head, and [[fox]] sits leaning against the tiger's soft side, smiling sheepishly with his tail wrapped around him, a calm warm picture, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of willow green, bamboo green, peach pink, vermilion, pale indigo and warm ochre, faint ink-wash misty hills far behind, generous empty space, cute rounded proportions and big round gentle eyes with white highlights (never narrow eyes), simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```
