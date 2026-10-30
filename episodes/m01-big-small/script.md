# M01 · Big and Small! 大大小小，唱起来！

> 栗栗唱儿歌｜主题：反义词 big / small、tall / short、fast / slow｜主角：栗栗（Nutty）＋ Hazel、Bun，客串一只小蜗牛｜2–3 岁英语启蒙｜9:16 竖版｜前奏关键帧钩子 4 秒 + 8 张歌词卡 + 尾奏片尾 4 秒，全片约 44 秒｜ElevenLabs Music 原创儿歌（不配音）｜中英字幕，唱到哪个词哪个词变黄
>
> 2026-10-28 写。形式参考用户发来的抖音「英文儿歌合集」录屏（一首 AI 儿歌 + 一组单词卡，按小节切换），角色、画风、出图、漫画剧本、质检和交付全部沿用森林故事那一套（skill 儿歌分册 docs/skill-type-song.md）。和录屏不同的地方：竖屏；用我们自己的三个角色；每张卡 2 小节（4 秒）而不是 1 小节，给 2–3 岁孩子留出跟唱、跟做动作的时间；卡片之间串了一个小反转。

## 1. 概要

**三句话**：

1. **Logline**：栗栗、Bun 和 Hazel 用一首歌比大小、比高矮、比快慢；最矮的 Hazel 一直踮脚也看不见，最后爬到 Bun 的头顶，一下子变成了最高的那个，大家手拉手唱 "We are friends!"。
2. **家长钩子**（第 0 帧大字）：唱一遍就会的反义词儿歌
3. **孩子会学的一句话**：`Big and small! Short and tall!`

- **主题**：认识三对反义词。每个词都配一个动作，孩子边唱边做：big 张开双臂，small 手指捏一点点，tall 踮脚伸高，short 蹲下，fast 原地快跑，slow 慢慢走。
- **今日单词**：big 大 · small 小 · tall 高（备选 fast 快 / slow 慢）
- **重复句型**：`Big, big, big!` `Small, small, small!` 每个词连唱三遍，再接一句 `It's a big acorn!` 或 `Bun is so tall!`。副歌 `Big and small! Short and tall!` 把前面的词串起来。
- **歌词量**：18 句（片尾再加一句 Bye-bye），每句 1–4 个词。全是画面一指就懂的词。
- **童趣**：
  - p01：栗栗抱着比自己还大的橡果，抱不住，往后倒。
  - p02：小得像豆子的橡果顶在鼻尖上，他看成了斗鸡眼。
  - p03：Bun 的耳朵伸得快碰到云，耳朵尖上还站着一只小鸟。
  - p06：Hazel 陪蜗牛慢慢爬，爬着爬着就趴在地上睡着了，鼻子吹出一个小泡泡。
  - p07（反转）：最矮的 Hazel 爬上了 Bun 的头顶，变成最高的那个。
- **互动**：整首歌就是互动，每个词配一个动作。最好玩的是唱到 slow 时歌声跟着放慢、唱到 fast 时变快，孩子会跟着慢下来、快起来。
- **情绪曲线**：前奏+（招手） p01+（抱不动，笑） p02+（斗鸡眼） p03+ p04−（Hazel 看不见，小失落） p05++（快跑，最热闹） p06−（慢下来，睡着了，笑） p07+++（反转，Hazel 变最高） p08++（大家手拉手唱副歌）
- **家长任务**：给孩子认反义词，还能让孩子动起来。看完和宝宝玩"我说你做"：说 big 宝宝张开手，说 small 宝宝缩成一团。
- **版本**：只出一个完整版（44 秒），不出精华版，因为歌要听完整才好听。

**选题打分**（满分 20，≥14 才写）：**18 分**。原始需求 2（大和小、比个子），日常诱因 1（比个子、分东西，但不是每天都会遇到），家长任务 2（认知 + 动起来），主线词可指认 2，重复空间 2（每个词至少唱 3 遍），视觉反转 2（最矮的变成最高的），情绪弧线 1（儿歌的弧线天生比较平，靠 p04 → p07 补），互动点 2（每个词一个动作），新鲜度 2（新形式），安全感 2。

**红线自检**：没有吓人的东西；"short" 不是嘲笑 Hazel，他自己想办法看到了，最后变成最高的，大家一起开心；p01 往后倒只是轻轻晃一下；歌是 ElevenLabs Music 原创生成，提示词里不写任何现有歌名、频道名和歌手名，也不照着唱哪首老歌的旋律。

## 2. 开头钩子（前奏 4 秒，关键帧动画，不用可灵）

- **大字标题**（第 1 帧就出现，给家长看）：唱一遍就会的反义词儿歌
- **小字**：3岁英语启蒙 · 边唱边做动作
- **备选标题**：宝宝跟着唱，big 和 small 一下就会了
- **声音**：歌曲前奏，尤克里里加木琴，第 3 秒有一声 "Hey!"。前奏不唱词。
- **画面节拍**（3 张关键帧，跟着拍子换图）：
  - 0.0 秒：栗栗从一颗巨大的橡果后面探出头来，向镜头招手，Hazel 和 Bun 在后面跟着音乐蹦蹦跳跳。（首帧 `kling_first.png`）
  - 2.0 秒：栗栗跳出来，张开双臂。（`h02.png`）
  - 3.0 秒：栗栗转了一圈，尾巴甩起来，后面两个在拍手。（`h03.png`，这时切到 p01）
- **钩子首帧出图提示词**：
  ```
  a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf, peeking out from behind a giant acorn that is three times bigger than him on a sunny forest meadow, one paw waving at the viewer, a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls and a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest bouncing to music in the background, little music notes floating in the air, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, lush richly painted forest backgrounds, bright blue sky with fluffy clouds, gentle warm nostalgic light, clear bright colors, no text, no watermark, vertical 9:16, leave the top 18% of the image as simple open sky with nothing in it, keep every face between 22% and 58% of the image height and the lower 38% simple open ground
  ```

**h02.png** ← kling_first.png
```
the squirrel has stepped out from behind the giant acorn and throws both arms open wide toward the viewer with a big happy grin; the hedgehog and the bunny in the background jump up in the air
```
**h03.png** ← kling_first.png
```
the squirrel spins around next to the giant acorn with his tail swinging, the hedgehog and the bunny in the background clap their paws, more music notes in the air
```

## 3. 分镜

每张卡占 4 秒（2 小节，120 BPM，一拍 0.5 秒），到点硬切。画面上方 18% 留天空，放这张卡的大字单词（英文大字 + 中文小字）；中间是角色；字幕在 y=1320，唱到哪个词，哪个词变黄。主图和关键帧跟着拍子来回切，看起来像在跳舞。

| 页 | 段落 | 画面（主图 → 关键帧） | 台词 | 音效 | 运镜 |
|---|---|---|---|---|---|
| p01 | 主歌一 · big | 栗栗抱着比自己还大的橡果，脸憋得鼓鼓的 → p01b：橡果抱离了地面，他往后仰，快倒了。大字：**big 大** | **唱**：`Big, big, big!`<br>大，大，大！<br>**唱**：`It's a big acorn!`<br>好大的橡果！ | 无，只有歌 | 缓推，每 2 拍换一次图 |
| p02 | 主歌一 · small | 栗栗鼻尖上顶着一颗豆子大的小橡果，看成了斗鸡眼 → p02b：小橡果弹起来，他的眼睛跟着往上看。大字：**small 小** | **唱**：`Small, small, small!`<br>小，小，小！<br>**唱**：`It's a small acorn!`<br>小小的橡果！ | 无 | 缓推到鼻尖 |
| p03 | 主歌二 · tall | Bun 踮着脚往上伸，耳朵快碰到云了，耳朵尖上站着一只小鸟 → p03b：举起双手伸得更高，小鸟飞起来。大字：**tall 高** | **唱**：`Tall, tall, tall!`<br>高，高，高！<br>**唱**：`Bun is so tall!`<br>Bun 好高呀！ | 无 | 上移，从脚看到耳朵尖 |
| p04 | 主歌二 · short | Hazel 躲在一排高草后面踮脚，只露出眼睛和头顶，使劲往外看 → p04b：他一蹦，整张笑脸露出来一下。大字：**short 矮** | **唱**：`Short, short, short!`<br>矮，矮，矮！<br>**唱**：`Hazel is short!`<br>Hazel 矮矮的！ | 无 | 不动，每拍换一次图（蹦一下、落一下） |
| p05 | 主歌三 · fast | 栗栗一溜烟跑过草地，尾巴拖成一条线，身后树叶和尘土飞起来 → p05b：已经冲到另一边，跳在半空。大字：**fast 快** | **唱**（变快）：`Fast, fast, fast!`<br>快，快，快！<br>**唱**：`Nutty is fast!`<br>栗栗跑得快！ | 无 | 左移，每拍换一次图 |
| p06 | 主歌三 · slow | Hazel 趴在草地上，和一只小蜗牛脸对脸，一起慢慢爬 → p06b：蜗牛往前挪了一点点，Hazel 已经趴着睡着了，鼻子吹出一个小泡泡。大字：**slow 慢** | **唱**（放慢）：`Slow, slow, slow...`<br>慢，慢，慢……<br>**唱**：`Snail is slow.`<br>蜗牛慢吞吞。 | 无 | 很慢的缓推，第 2 小节才换图 |
| p07 | 桥段 · 反转 | Hazel 站在 Bun 的头顶、两只耳朵中间，比谁都高，栗栗在下面张大嘴看呆了 → p07b：Hazel 举起双手欢呼，栗栗跳起来拍手。大字：**tall 高** | **唱**：`Up, up, up!`<br>上，上，上！<br>**唱**：`Now Hazel is tall!`<br>现在 Hazel 最高啦！ | 无 | 上移 |
| p08 | 副歌 | 三个小伙伴手拉手围成一圈跳舞，大橡果、小橡果和小蜗牛都在旁边 → p08b：三个一起跳到半空。大字：**big & small 大和小**。这张卡占 8 秒（4 小节） | **唱**：`Big and small!`<br>大和小！<br>**唱**：`Short and tall!`<br>矮和高！<br>**唱**：`We are friends!`<br>我们是好朋友！<br>**唱**：`Hooray!`<br>好耶！ | 无 | 缓拉，每拍换一次图 |

**尾奏**（4 秒）：片尾卡，大字 "Bye-bye! 下次再唱！"，小字 "收藏起来，和宝宝边唱边做动作"。歌里唱一句 `Bye-bye!`，然后音乐收住。

**不加背景音乐和音效**：歌就是全部声音，音效会抢拍子。

## 4. 歌（ElevenLabs Music 作曲计划，在 story.json 的 `song` 里）

- **模型**：`music_v2_5`，按段写歌词和时长，时长会严格照着来，卡片才能踩在拍子上。
- **整体风格**：欢快的幼儿英文儿歌，120 BPM，C 大调；**笑着唱的温暖女声，像在唱给小宝宝听**，副歌加一群小朋友跟唱、喊；强弱对比要大：big 唱得又大又满，small 轻轻小小；尤克里里、木琴、拍手、轻鼓；旋律有起伏、一听就能跟；英文咬字清楚。
- **不要**：说唱、失真、重鼓、电音、长间奏、成人情歌腔、过重修音、**平铺直叙、机器人腔、念白**（2026-10-28 用户要求：不能唱得没感情）。
- **分段**（共 44 秒）：

| 段 | 时长 | 歌词 | 对应卡片 |
|---|---|---|---|
| Intro | 4 秒 | （纯音乐，第 3 秒小朋友喊 "Hey!"） | 钩子 |
| Verse 1 | 8 秒 | Big, big, big! / It's a big acorn! / Small, small, small! / It's a small acorn! | p01、p02 |
| Verse 2 | 8 秒 | Tall, tall, tall! / Bun is so tall! / Short, short, short! / Hazel is short! | p03、p04 |
| Verse 3 | 8 秒 | Fast, fast, fast! / Nutty is fast! / Slow, slow, slow... / Snail is slow. | p05（唱快）、p06（唱慢） |
| Bridge | 4 秒 | Up, up, up! / Now Hazel is tall! | p07 |
| Chorus | 8 秒 | Big and small! / Short and tall! / We are friends! / Hooray! | p08 |
| Outro | 4 秒 | Bye-bye!（之后音乐收住） | 片尾 |

- **出几版**：一次出 3 版。先用 `song.py --check` 听写，咬字不清、拍子对不上卡片的直接淘汰；剩下最好的两版做成试听网页，由用户用耳朵挑，情绪只能人听。两版都平就改风格词重出，最多两轮。
- **卡点**：生成时要回每个词的时间戳，按时间戳切卡、做逐词高亮；拿不到时间戳就按作曲计划的分段时长切。

## 5. 出图提示词

> 和森林故事一样：主图写 `**p01.png**`，下面接一个代码块；关键帧写 `**p01b.png** ← p01.png`，代码块里只写要改什么。
> 构图要求和故事集不一样：**上方 18% 留天空**放大字单词，脸在 22%–58% 高度，下方 38% 留草地放字幕。

**p01.png**
```
a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf, hugging a giant acorn that is twice as big as he is on a sunny forest meadow, his arms stretched all the way around it, cheeks puffed, wobbling a little under its weight, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, lush richly painted forest backgrounds, bright blue sky with fluffy clouds, gentle warm nostalgic light, clear bright colors, no text, no watermark, vertical 9:16, leave the top 18% of the image as simple open sky with nothing in it, keep every face between 22% and 58% of the image height and the lower 38% simple open ground
```

**p01b.png** ← p01.png
```
the squirrel leans back with the giant acorn lifted a little off the ground, his arms opened wide around it, eyes shut tight, about to tip over
```

**p02.png**
```
a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf, standing on a sunny forest meadow with one tiny acorn the size of a pea balanced on the tip of his nose, both of his eyes comically crossed toward the acorn on his nose tip (funny cross-eyed look), a little surprised smile, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, lush richly painted forest backgrounds, bright blue sky with fluffy clouds, gentle warm nostalgic light, clear bright colors, no text, no watermark, vertical 9:16, leave the top 18% of the image as simple open sky with nothing in it, keep every face between 22% and 58% of the image height and the lower 38% simple open ground
```

**p02b.png** ← p02.png
```
the tiny acorn pops up into the air above his nose with a little sparkle, the squirrel's eyes follow it upward, mouth in a small round 'o'
```

**p03.png**
```
a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest, standing on tiptoes on a sunny forest meadow and stretching up as tall as she can, her long ears pointing straight up so high they almost touch the clouds, a little bird sitting on the tip of one ear, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, lush richly painted forest backgrounds, bright blue sky with fluffy clouds, gentle warm nostalgic light, clear bright colors, no text, no watermark, vertical 9:16, leave the top 18% of the image as simple open sky with nothing in it, keep every face between 22% and 58% of the image height and the lower 38% simple open ground
```

**p03b.png** ← p03.png
```
the bunny stretches even higher with both arms raised over her head and her ears wiggling, the little bird flutters up off her ear
```

**p04.png**
```
a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls, standing on tiptoes behind a row of tall grass on a sunny forest meadow, only his eyes and the top of his head peeking over the grass, trying hard to see, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, lush richly painted forest backgrounds, bright blue sky with fluffy clouds, gentle warm nostalgic light, clear bright colors, no text, no watermark, vertical 9:16, leave the top 18% of the image as simple open sky with nothing in it, keep every face between 22% and 58% of the image height and the lower 38% simple open ground
```

**p04b.png** ← p04.png
```
the hedgehog jumps up high above the grass with arms raised, now his whole happy face shows over the grass for a moment
```

**p05.png**
```
a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf, zooming across a sunny forest meadow at top speed with a happy wide grin, his fluffy tail streaming behind him, a swirl of fallen leaves and dust puffs flying up behind his feet, speed lines in the air, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, lush richly painted forest backgrounds, bright blue sky with fluffy clouds, gentle warm nostalgic light, clear bright colors, no text, no watermark, vertical 9:16, leave the top 18% of the image as simple open sky with nothing in it, keep every face between 22% and 58% of the image height and the lower 38% simple open ground
```

**p05b.png** ← p05.png
```
the squirrel is now at the other side of the meadow mid-leap, legs stretched out in a big running jump, leaves spinning in the air behind him
```

**p06.png**
```
a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls, lying on his tummy on a sunny forest meadow next to a cute little snail with a round spiral shell, face to face with the snail, both of them moving very very slowly, a sleepy happy smile, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, lush richly painted forest backgrounds, bright blue sky with fluffy clouds, gentle warm nostalgic light, clear bright colors, no text, no watermark, vertical 9:16, leave the top 18% of the image as simple open sky with nothing in it, keep every face between 22% and 58% of the image height and the lower 38% simple open ground
```

**p06b.png** ← p06.png
```
the snail has moved forward just a tiny little bit, and the hedgehog has fallen asleep with his head on his paws and a tiny bubble at his nose, peaceful and funny
```

**p07.png**
```
a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls, standing proudly on top of the head of a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest, between her long ears, now taller than everyone, a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf below looking up at him with his mouth open in amazement, sunny forest meadow, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, lush richly painted forest backgrounds, bright blue sky with fluffy clouds, gentle warm nostalgic light, clear bright colors, no text, no watermark, vertical 9:16, leave the top 18% of the image as simple open sky with nothing in it, keep every face between 22% and 58% of the image height and the lower 38% simple open ground
```

**p07b.png** ← p07.png
```
the hedgehog raises both arms high in the air cheering, the bunny smiles and looks up at him with her eyes, the squirrel jumps up clapping
```

**p08.png**
```
a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf, a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls and a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest dancing together in a circle holding paws on a sunny forest meadow, the giant acorn and the tiny acorn and the little snail beside them, all laughing, little music notes floating in the air, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, lush richly painted forest backgrounds, bright blue sky with fluffy clouds, gentle warm nostalgic light, clear bright colors, no text, no watermark, vertical 9:16, leave the top 18% of the image as simple open sky with nothing in it, keep every face between 22% and 58% of the image height and the lower 38% simple open ground
```

**p08b.png** ← p08.png
```
all three jump up together in the air at the same moment with their paws still joined, big laughing faces, the snail raises its little eye stalks
```

## 6. 发布文案

- **抖音标题**：唱一遍就会的反义词儿歌｜big small tall short
- **小红书标题**：反义词英文儿歌｜3岁英语启蒙
- **合集**：栗栗唱儿歌（新建）
- **封面关键画面**：用 p08（三个手拉手跳舞）自动出一张上方留空的 `cover.png`
- **正文**：
```
🎵 栗栗唱儿歌｜Big and Small! 大大小小，唱起来！
栗栗抱大橡果、Bun 伸高高、Hazel 和蜗牛比慢……最矮的 Hazel 最后变成了最高的！

📖 今日单词：big 大｜small 小｜tall 高
🎤 跟唱句子：
Big, big, big! 大，大，大！
It's a small acorn! 小小的橡果！
Big and small! Short and tall! 大和小！矮和高！

💡 亲子小互动：和宝宝玩"我说你做"：说 big 张开双臂，说 small 缩成一团，说 tall 踮脚伸高。

#幼儿英语启蒙 #英语启蒙 #英文儿歌 #儿童英语 #亲子英语 #反义词
```
- **置顶评论**：今日单词 big 大｜small 小｜tall 高。跟宝宝边唱边做动作，唱两遍就会啦！
- 发布时勾选"内容由 AI 生成"。
