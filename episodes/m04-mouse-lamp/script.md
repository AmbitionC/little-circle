# M04 · Little Mouse, Up! Up! 小老鼠上灯台（国风水彩 · H3 全视频版）

> 2026-11-07。用户：「用 H3 做一版视频，充分发挥视频的优势……想做一个爆款」→ 选「中国童谣 + 中国水彩画风」里的小老鼠上灯台 →「以这个故事为核心，做一定的创新」。
> 模式：**全片 H3 真视频**（8 段，每段一个连续动作），复习卡用关键帧。画风用 11-02 用户看过的中国水彩（`style.json`，样张沿用 m02 的两张，其中一张就是小老鼠灯台）。角色是这一集新画的小老鼠和大橘猫（`characters.json`），不用森林伙伴。
> 素材：清代北方民间童谣「小老鼠，上灯台，偷油吃，下不来，喵喵喵，猫来了，叽里咕噜滚下来」，公有领域。背景音乐用乐器弹这首童谣的老调（民间曲调，常见版本不署作者；**发布前再核一次**，核不清就换原创旋律）。

## 0. 对标和人性

**对标（B 站按播放排序，2026-11-07 在用户 Mac 上不登录查）**：《【儿歌】小老鼠上灯台-叽里咕噜滚下来》231 万；宝宝巴士版 139 万；共青团中央 26 秒短版 109 万。抖音站内数据云端拿不到。

| 人性 | 怎么用 | 拉动哪个数据 |
|---|---|---|
| 熟悉感 / 接龙 | 钩子大字「小老鼠上灯台，下一句是？」，家长脑子里自动接「偷油吃，下不来」 | 2 秒跳出率、评论区接龙 |
| 紧张 → 反转 | 猫来了，所有人以为要抓老鼠；**创新：猫是来帮忙的**，结果自己太胖爬不上去，两个一起叽里咕噜滚下来 | 完播率 |
| 隔屏互动 | 猫冒头时大字「宝宝一起学猫叫！」；滚下来时一起喊 DOWN | 家长拍娃晒、转发 |
| 大个子出糗 | 胖橘猫抱着灯台爬，灯台晃，自己也滚下来 | 笑、评论 |
| 彩蛋 / 循环 | 结尾小老鼠又偷偷溜向灯台，回头对镜头 "Up again?"，猫睁开一只眼 "MEOW!" | 看到最后、重复播放 |
| 怀旧 | 中国水彩 + 老童谣 + 老调乐器 | 家长转发、收藏 |

## 1. 概要

- **Logline**：夜里，小老鼠爬上灯台偷油吃，越吃越圆，下不来了。大橘猫冒出来「喵喵喵」，小老鼠吓坏了。没想到猫是来帮忙的，可他太胖，抱着灯台一爬，灯台一晃，两个叽里咕噜一起滚到软垫子上，抱在一起哈哈大笑。彩蛋：猫睡着了，小老鼠又溜向灯台……猫一只眼睁开。
- **今日单词**：up 上 · down 下 · meow 喵（up ×4、down ×2、meow ×4，外加 yummy、help）
- **道理**：看起来可怕的大个子，也可能是朋友；贪吃会下不来。
- **用了哪些手法**：老童谣原结构（上灯台 → 偷油吃 → 下不来 → 猫来了 → 滚下来）；反转（猫不抓老鼠）；大个子出糗；隔屏互动；循环彩蛋。
- **常理和安全**：火苗很小、在油碟另一边，小老鼠从来不碰火；灯台只晃不倒，最后稳稳站好；猫不露牙、不露爪；滚下来落在软垫子上，没人受伤。

## 2. 镜头表（全片约 45 秒）

每段都是 H3 一个镜头一个动作：首帧是 Codex 出好、过了角色质检的水彩图，只给首帧 + 动作提示词让模型自己演；只有 S6（两个角色一起滚下来）用首尾帧锁住落点。片段各 5 秒，剪到下表时长，转 30fps，丢模型音轨。

| 段 | 时长 | 首帧 → H3 动作 | 台词 | 大字 / 音效 |
|---|---|---|---|---|
| S1 钩子·上灯台 | 5.0 | f1：小老鼠抱着灯台底座往上看 → **一口气顺着灯杆往上爬，镜头跟着往上摇**，爬到顶 | **mouse**：`Up! Up! Up!`<br>上！上！上！ | 大字「小老鼠上灯台，下一句是？」；小爪子哒哒声 |
| S2 偷油吃 | 5.0 | f2：趴在油碟边上闻 → **蘸一下、舔一下，肚子一点点鼓成小皮球**（锁机位） | **mouse**：`Yummy! Yummy!`<br>好吃！好吃！ | 吧唧吧唧、肚子鼓起来"噗"一声 |
| S3 下不来 | 5.0 | f3：俯拍，圆肚子小老鼠往下看 → **伸一只脚下去，肚子卡在碟边一晃，赶紧缩回来抱紧，耳朵耷拉、发抖**，镜头慢推 | **mouse**：`Uh-oh! So high!`<br>糟了！好高！ | 低音一下 |
| S4 猫来了 | 5.0 | f4：桌沿冒出半个猫头 → **猫头慢慢升起、耳朵竖起来，张嘴喵三声**；镜头从猫往上摇到发抖的小老鼠 | **cat**：`Meow! Meow! Meow!`<br>喵！喵！喵！ | 大字「喵喵喵，猫来了！宝宝一起学猫叫」；铃铛叮 |
| S5 反转 | 5.0 | f5：猫站在桌上伸爪 → **猫笑着点头、招手让他下来，小老鼠从碟边慢慢探出头**（锁机位） | **cat**：`I can help!`<br>我来帮你！<br>**mouse**：`Really?`<br>真的吗？ | 音乐转暖 |
| S6 叽里咕噜滚下来 | 6.0 | f6 → f6e（首尾帧）：猫抱着灯杆往上爬，太胖了灯台一晃 → **小老鼠从碟边滑下来，顺着猫的背和尾巴像滑梯一样叽里咕噜滚下去，猫也一松手，两个一起软软地摔到红垫子上**，灯台晃回原位 | **mouse**：`Whoa!`<br>哇！<br>**all**：`DOWN!`<br>下！（停顿等宝宝喊） | 大字「叽里咕噜滚下来！」；滑梯哨音 + 软软的噗 |
| S7 好朋友 | 5.0 | f7：猫抱着小老鼠 → **两个一起哈哈笑，猫轻轻蹭小老鼠的脸，铃铛晃**，镜头慢推 | **mouse**：`Thank you, Cat!`<br>谢谢你，猫咪！<br>（两人笑声走音效层） | 笑声、铃铛 |
| S8 彩蛋 | 5.0 | f8：猫睡着，小老鼠踮脚溜向桌腿，回头对镜头坏笑 → **小老鼠竖手指"嘘"，身后的猫突然睁开一只大圆眼，小老鼠吓一跳**（锁机位） | **mouse**：`Up again?`<br>再上去一次？（悄悄话）<br>**cat**：`MEOW!`<br>喵！ | 一声滑稽的"咚" |
| 复习 | 4.0 | r1（关键帧慢推）：猫仰躺在垫子上睡，小老鼠蜷在他肚子上睡 | （无台词） | 复习卡：up 上 · down 下 · meow 喵；乐器把童谣最后一句弹完落在主音 |

合计约 45 秒。台词 11 句，都在 1–4 个词。超时先砍 S5、S7 的尾巴，不砍 S6 的 DOWN 停顿。

**音乐**：古筝 / 笛子 / 木鱼弹「小老鼠上灯台」老调，全片一个固定电平；S4 猫冒头时停一拍只留铃铛，S6 滚下来加一串下行刮奏，S7 回到完整旋律。
**环境底声**：夜里屋内很轻的虫鸣 + 灯芯噼啪（CC0，`docs/skill-sound-design.md`）。

## 3. H3 动作提示词

> 每段一个文件 `h3_s1.txt`…`h3_s8.txt`，跑 `minimax_video.py <集> s1 --first f1.png --prompt-file h3_s1.txt --duration 5`（不带 --go 只报价）。S6 加 `--last f6e.png`。画风句从 `style.json` 的 `video_style` 读。

## 4. 出图提示词

> 先出两张角色设计图 `char_mouse.png`、`char_cat.png`，挑好后拷成 `refs/mouse.png`、`refs/cat.png`，再出 f1–f8、f6e、r1。主图的眼睛一律写大圆眼（用户 11-06：亚洲 / 小动物角色都不能画窄眼）。

**char_mouse.png**
```
character design sheet of ONE character only, standing front view, full body, centered, plain warm rice-paper background, nothing else: a tiny round grey-brown baby mouse with big round pink-lined ears, big round shiny dark eyes with white highlights (round, not narrow), a little pink nose, short whiskers, a thin long pink tail, wearing a small red Chinese dudou apron with a little gold coin embroidered on it, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**char_cat.png**
```
character design sheet of ONE character only, sitting front view, full body, centered, plain warm rice-paper background, nothing else: a big chubby round orange-and-white tabby cat, round soft face with fluffy cheeks, big round warm amber eyes with white highlights (round, not narrow), a small pink nose, a gentle friendly smile with no teeth showing, soft round paws with no claws, a red string collar with one small golden bell, a big fluffy striped tail; looks cuddly and a bit clumsy, never scary, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**f1.png**
```
inside a quiet old Chinese room at night, a round paper lattice window with a pale full moon behind it, on the left a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the far edge of the dish; a soft round red floor cushion on the floor below the table; warm golden lamp light, the rest of the room soft and dim; [[mouse]] stands on the table at the round base of the oil lamp, both little hands holding the thin stem, looking up at the oil dish far above with big hungry eyes and his tongue peeking out; the camera is low, the lamp stem rises to the top of the picture, the little flame and dish glowing at the top, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**f2.png**
```
inside a quiet old Chinese room at night, a round paper lattice window with a pale full moon behind it, on the left a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the far edge of the dish; a soft round red floor cushion on the floor below the table; warm golden lamp light, the rest of the room soft and dim; close-up at the top of the oil lamp: [[mouse]] has climbed onto the rim of the shallow round dish of golden oil, kneeling on the rim and leaning over the oil, sniffing it with a delighted face, the small flame is on the far side of the dish away from him; behind him the dim room and the moon window, far below, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**f3.png**
```
inside a quiet old Chinese room at night, a round paper lattice window with a pale full moon behind it, on the left a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the far edge of the dish; a soft round red floor cushion on the floor below the table; warm golden lamp light, the rest of the room soft and dim; high angle looking down from the top of the oil lamp: [[mouse]] sits on the rim of the oil dish, his belly now very round and full like a little ball, one foot dangling over the edge, looking down at the far-away table with worried wide eyes, ears drooping, the thin stem dropping steeply away below him, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**f4.png**
```
inside a quiet old Chinese room at night, a round paper lattice window with a pale full moon behind it, on the left a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the far edge of the dish; a soft round red floor cushion on the floor below the table; warm golden lamp light, the rest of the room soft and dim; [[cat]] peeks up over the edge of the table, only the top half of his round head, ears and big round eyes showing above the table edge, looking up at the lamp with curiosity; high above on top of the lamp the round-bellied [[mouse]] freezes and looks down at the cat with shocked eyes; sizes: the cat's head alone is bigger than the whole mouse, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**f5.png**
```
inside a quiet old Chinese room at night, a round paper lattice window with a pale full moon behind it, on the left a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the far edge of the dish; a soft round red floor cushion on the floor below the table; warm golden lamp light, the rest of the room soft and dim; [[cat]] now stands on the table next to the oil lamp, smiling kindly and reaching one soft round paw up toward [[mouse]] at the top of the lamp, the mouse peeks over the rim of the dish, still scared; the cat's head reaches about two thirds of the way up the lamp, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**f6.png**
```
inside a quiet old Chinese room at night, a round paper lattice window with a pale full moon behind it, on the left a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the far edge of the dish; a soft round red floor cushion on the floor below the table; warm golden lamp light, the rest of the room soft and dim; [[cat]] hugs the thin lamp stem with both paws and one leg lifted, trying clumsily to climb it, his chubby body much too heavy, the lamp leans and wobbles to one side, [[mouse]] clings to the rim of the tilting dish with wide eyes, the small flame leaning; the soft round red floor cushion waits on the floor below, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**f6e.png**
```
inside a quiet old Chinese room at night, a round paper lattice window with a pale full moon behind it, on the left a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the far edge of the dish; a soft round red floor cushion on the floor below the table; warm golden lamp light, the rest of the room soft and dim; the soft round red floor cushion on the floor below the table: [[mouse]] and [[cat]] have landed together on it in a soft fluffy heap, the cat lying on his back with his round belly up and paws in the air, the round-bellied mouse sitting on top of the cat's round tummy, both dizzy with swirly happy eyes, a few soft tufts of fur floating; the oil lamp stands safely upright on the table behind them, the flame calm, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**f7.png**
```
inside a quiet old Chinese room at night, a round paper lattice window with a pale full moon behind it, on the left a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the far edge of the dish; a soft round red floor cushion on the floor below the table; warm golden lamp light, the rest of the room soft and dim; on the soft round red floor cushion: [[cat]] sits up holding [[mouse]] gently in his two soft paws like a hug, both laughing with big happy open mouths and closed happy eyes, the cat's bell shining; the oil lamp glows calmly on the table behind them, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**f8.png**
```
inside a quiet old Chinese room at night, a round paper lattice window with a pale full moon behind it, on the left a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the far edge of the dish; a soft round red floor cushion on the floor below the table; warm golden lamp light, the rest of the room soft and dim; the same room later: [[cat]] is curled up asleep on the round red cushion with a peaceful smile; [[mouse]] tiptoes away from him toward the table leg, looking back over his shoulder at the viewer with a sneaky little grin, one finger on his lips; the oil lamp glows on the table above, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```

**r1.png**
```
inside a quiet old Chinese room at night, a round paper lattice window with a pale full moon behind it, on the left a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the far edge of the dish; a soft round red floor cushion on the floor below the table; warm golden lamp light, the rest of the room soft and dim; [[mouse]] sleeps curled up on the round tummy of [[cat]], who sleeps on his back on the red cushion, both peaceful and smiling, the moon in the round window, the lamp flame small and calm on the table, a cozy warm picture with plenty of empty space at the bottom, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, vertical 9:16, keep every face in the upper 60% of the image
```
