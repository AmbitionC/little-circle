# M04 · The Big Shadow 小老鼠上灯台：灯影大怪兽（国风水彩 · H3 全视频版 v2）

> 2026-11-08 第二版。第一版（猫来帮忙、一起滚下来，见 git 历史 1ea11df）用户看漫画剧本：「有点一般没新意」。原因：照着童谣顺序走，只换一个"猫其实是好人"的结局，这是儿童片最常见的套路，家长一眼猜到。用户在新方向里选了 **D 灯影大怪兽**。
> 模式：**全片 H3 真视频**（8 段），复习卡用关键帧。画风中国水彩（`style.json`），角色沿用第一版已过质检的小老鼠和大橘猫（`characters.json` + `refs/`，不用重出）。
> 素材：清代北方民间童谣「小老鼠，上灯台，偷油吃，下不来，喵喵喵，猫来了，叽里咕噜滚下来」，公有领域。背景音乐乐器弹老调（民间曲调；**发布前再核一次**，核不清换原创旋律）。

## 0. 对标和人性

**对标（B 站按播放排序，2026-11-07 在用户 Mac 上不登录查）**：《【儿歌】小老鼠上灯台-叽里咕噜滚下来》231 万；宝宝巴士版 139 万；共青团中央 26 秒短版 109 万。抖音站内数据云端拿不到。

**新意**：前半段照童谣走（上灯台 → 偷油吃 → 猫来了），家长以为要演"滚下来"；猫冒头那一下，**灯把小老鼠的影子投成墙上的大怪兽，被吓跑的是猫**。小老鼠发现"那是我！"，开始比手影逗猫，最后两个和影子一起跳舞，才轮到原童谣的"叽里咕噜滚下来"——滚到了猫肚子上。灯台是童谣自带的道具，影子也是灯自带的，反转在题内。

| 人性 | 怎么用 | 拉动哪个数据 |
|---|---|---|
| 熟悉感 / 接龙 | 钩子大字「小老鼠上灯台……墙上那是谁？」，前半段照原童谣，家长自动接下一句 | 2 秒跳出率、评论区接龙 |
| 期待落空 | 家长等着"猫来了、滚下来"，结果被吓跑的是猫 | 完播率、"没想到"评论 |
| 大小反差 | 最小的小老鼠有最大的影子；最大的猫吓成一团毛球 | 笑 |
| 隔屏互动 | S6 大字「宝宝也来比一比！」：对着台灯比小兔手影，家长最好拍、最好晒；评论区比手影 | 拍娃晒、转发、评论 |
| 国风怀旧 | 手影、皮影是家长小时候的玩意，水彩暖光夜景 | 收藏、转发 |
| 彩蛋 | 跳着跳着脚一滑，终于"叽里咕噜滚下来"，正好落在猫肚子上 | 看到最后 |

## 1. 概要

- **Logline**：夜里，小老鼠爬上灯台偷油吃，吃得圆滚滚。大橘猫冒出头来 "Meow!"，小老鼠吓得举起手——灯把他的影子投到墙上，变成一个大怪兽！被吓跑的是猫，钻进垫子底下发抖。小老鼠回头一看：那是我的影子！他比出小兔、小鸟手影，猫好奇地探出头来扑影子，两个一起和影子跳舞。跳着跳着脚一滑，叽里咕噜滚下来，落在猫的软肚子上，哈哈大笑。
- **今日单词**：up 上 · big 大 · small 小（up ×3、big ×4、small ×2，外加 bunny、bird、meow）
- **道理**：小小的我也可以很"大"；吓人的东西看清了就不怕了（影子只是光）。
- **用了哪些手法**：老童谣前半段原样（熟悉）+ 中途反转（期待落空）；大小反差；隔屏互动（手影）；童谣原句做彩蛋收尾。
- **常理和安全**：火苗小、在油碟靠外一侧，小老鼠从不碰火，比手影时手在火苗前方一段距离；灯台全程不倒；猫不露牙不露爪，炸毛是滑稽不是凶；滚下来落在软肚子上，没人受伤。
- **不吓人**：怪兽影子是软灰色、圆耳朵圆肚子，轮廓可爱；出现时音乐是"哇哦"不是惊悚音效，下一秒就是猫滑稽地炸毛。

## 2. 镜头表（全片约 45 秒）

每段一个 H3 镜头、一个连续动作：首帧是过了质检的水彩图，只给首帧 + 动作提示词。S4（影子从小变成大怪兽）和 S8（跳舞 → 滚下来）用首尾帧锁住结果。片段各 5 秒，剪到下表时长，转 30fps，丢模型音轨。

| 段 | 时长 | 首帧 → H3 动作 | 台词 | 大字 / 音效 |
|---|---|---|---|---|
| S1 钩子·上灯台 | 5.0 | f1：小老鼠抱着灯杆往上爬，墙上有他的影子 → **一口气爬到顶，墙上的影子跟着往上爬、越爬越大**，镜头跟着往上摇 | **mouse**：`Up! Up! Up!`<br>上！上！上！ | 大字「小老鼠上灯台……墙上那是谁？」；小爪子哒哒 |
| S2 偷油吃 | 5.0 | f2：坐在油碟边舔爪子 → **蘸一下舔一下，肚子越来越圆，墙上的影子肚子也跟着鼓**（锁机位） | **mouse**：`Yummy!`<br>好吃！ | 吧唧、"噗"一声肚子鼓起 |
| S3 猫来了 | 5.0 | f3：猫头和前爪从桌沿冒出来 → **猫头慢慢升起，眯眼笑着舔舔嘴，喵一声；灯台上的小老鼠僵住** | **cat**：`Meow!`<br>喵！<br>**mouse**：`Uh-oh!`<br>糟了！ | 大字「喵喵喵，猫来了！」；铃铛叮，音乐停一拍 |
| S4 大怪兽 | 5.0 | f3 → f4（首尾帧）：**小老鼠吓得双手一举，墙上的影子"呼"地长成满墙的大怪兽；猫抬头一看，全身毛炸成一个橘色毛球** | **cat**：`So BIG!`<br>好大！ | 低沉的"哇哦"+ 一声滑稽的"噗"炸毛 |
| S5 原来是我 | 5.0 | f5：猫钻在红垫子底下只露屁股和尾巴 → **尾巴发抖；小老鼠回头看墙，挥挥手，墙上的大怪兽也挥手，他笑了**（锁机位） | **mouse**：`Big? ...It's me!`<br>大怪兽？……是我！<br>**mouse**：`I'm small!`<br>我是小不点！ | 小小的"叮"（恍然大悟） |
| S6 比手影 | 5.0 | f6：小老鼠在火苗前比小兔手影 → **两根手指一动一动，墙上的小兔耳朵跟着动，然后换成翅膀，变成一只飞鸟** | **mouse**：`Bunny! ... Bird!`<br>小兔！……小鸟！ | 大字「宝宝也来比一比！」；扑翅声 |
| S7 猫扑影子 | 5.0 | f7：猫扒着墙伸爪够影子鸟 → **影子鸟在墙上飞来飞去，猫跟着左扑右扑，铃铛直晃；小老鼠笑出声** | **cat**：`Meow?`<br>喵？（好奇） | 铃铛、笑声 |
| S8 跳舞·滚下来 | 6.0 | f8 → f8e（首尾帧）：两个和影子一起跳舞 → **小老鼠转圈脚一滑，从灯台上叽里咕噜滚下来，正好落在仰躺的猫的软肚子上**，墙上的影子也滚成一团 | **all**：`Dance!`<br>跳舞！<br>**mouse**：`Whoa!`<br>哇！<br>**all**：`DOWN!`<br>下来啦！ | 大字「叽里咕噜滚下来！」；下行刮奏 + 软软的噗，两人笑声 |
| 复习 | 4.0 | r1（关键帧慢推）：猫仰躺睡，小老鼠蜷在他肚子上睡，墙上一座小山似的影子 | （无台词） | 复习卡：up 上 · big 大 · small 小；乐器把童谣最后一句弹完落在主音 |

合计约 45 秒。台词 13 句，每句 1–3 个词。超时先砍 S2、S7 的尾巴，不砍 S5 的 "It's me!" 和 S8 的 DOWN 停顿。

**音乐**：古筝 / 笛子 / 木鱼弹「小老鼠上灯台」老调，全片固定电平；S3 猫冒头停一拍只留铃铛；S4 怪兽出现一个低音"哇哦"（不用惊悚音效）；S6–S8 加快、轻快。
**环境底声**：夜里屋内很轻的虫鸣 + 灯芯噼啪（CC0，`docs/skill-sound-design.md`）。

## 3. H3 动作提示词

> 每段一个文件 `h3_s1.txt`…`h3_s8.txt`，跑 `minimax_video.py <集> s1 --first f1.png --prompt-file h3_s1.txt --duration 5`（不带 --go 只报价）。S4 用 `--first f3.png --last f4.png`，S8 用 `--first f8.png --last f8e.png`。画风句从 `style.json` 的 `video_style` 读。
> **H3 的风险点**：影子要跟着角色动作走（S1、S2、S5、S6）。模型不一定守光影逻辑，跑出来要逐帧看影子和动作对不对得上；对不上的段改用首尾帧锁住影子形状。

## 4. 出图提示词

> 角色设计图沿用第一版（已过质检，`refs/mouse.png`、`refs/cat.png` 不用重出）。主图 f1–f8、f8e、r1 全部按新剧本重出（墙换成一大面浅色素墙，给影子留位置）。眼睛一律大圆眼；猫不露牙。

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
inside a quiet old Chinese room at night; behind the table a big plain smooth pale cream plaster wall that fills most of the background, lit warm gold by the lamp, with a small round paper lattice window high in one corner showing a pale moon; in front a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the near edge of the dish; a soft round red floor cushion on the wooden floor below the table; the lamp is the only light, the rest of the room soft and dim; [[mouse]] is halfway up the thin lamp stem, hugging it and climbing, looking up at the oil dish; on the pale wall behind him a soft grey shadow of the climbing mouse, already a bit bigger than the mouse himself, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f2.png**
```
inside a quiet old Chinese room at night; behind the table a big plain smooth pale cream plaster wall that fills most of the background, lit warm gold by the lamp, with a small round paper lattice window high in one corner showing a pale moon; in front a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the near edge of the dish; a soft round red floor cushion on the wooden floor below the table; the lamp is the only light, the rest of the room soft and dim; [[mouse]] sits on the rim of the oil dish at the top of the lamp with a very round full belly like a little ball, licking his paw happily; on the pale wall behind, his shadow is big and round, about three times his size, a funny round-belly shadow, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f3.png**
```
inside a quiet old Chinese room at night; behind the table a big plain smooth pale cream plaster wall that fills most of the background, lit warm gold by the lamp, with a small round paper lattice window high in one corner showing a pale moon; in front a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the near edge of the dish; a soft round red floor cushion on the wooden floor below the table; the lamp is the only light, the rest of the room soft and dim; [[cat]] pops his round head and front paws up over the edge of the table, looking up at [[mouse]] on top of the lamp with big round curious eyes and a playful smile; the round-bellied mouse freezes on the rim with a shocked face; on the wall behind the mouse his shadow is big; sizes: the cat's head alone is bigger than the whole mouse, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f4.png**
```
inside a quiet old Chinese room at night; behind the table a big plain smooth pale cream plaster wall that fills most of the background, lit warm gold by the lamp, with a small round paper lattice window high in one corner showing a pale moon; in front a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the near edge of the dish; a soft round red floor cushion on the wooden floor below the table; the lamp is the only light, the rest of the room soft and dim; the scared [[mouse]] throws both arms up high and spreads his little fingers, ears straight up, on top of the lamp right in front of the flame; behind him, the whole pale wall is filled by his GIANT soft grey shadow: a huge monster shape with enormous round ears, big spread claws and a big round belly, many times taller than the cat, looming over the room; [[cat]] on the table edge stares up at the wall, his fur puffed up all over like a big orange ball, eyes huge and round with fright, tail bushy, not angry, just very startled and funny, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f5.png**
```
inside a quiet old Chinese room at night; behind the table a big plain smooth pale cream plaster wall that fills most of the background, lit warm gold by the lamp, with a small round paper lattice window high in one corner showing a pale moon; in front a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the near edge of the dish; a soft round red floor cushion on the wooden floor below the table; the lamp is the only light, the rest of the room soft and dim; [[cat]] hides under the soft round red floor cushion below the table, only his fluffy striped tail and his bottom sticking out, trembling, the bell peeking out; on top of the lamp [[mouse]] looks back over his shoulder at the giant shadow on the wall, one arm still raised, a surprised, then delighted face as he realizes it is his own shadow, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f6.png**
```
inside a quiet old Chinese room at night; behind the table a big plain smooth pale cream plaster wall that fills most of the background, lit warm gold by the lamp, with a small round paper lattice window high in one corner showing a pale moon; in front a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the near edge of the dish; a soft round red floor cushion on the wooden floor below the table; the lamp is the only light, the rest of the room soft and dim; close-up: [[mouse]] stands on the rim of the oil dish beside the small flame, holding up his two little paws in front of the light and making a bunny hand-shadow with two fingers up as long ears; on the pale wall a big clear soft grey shadow of a bunny with two long ears; the mouse grins at the shadow proudly, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f7.png**
```
inside a quiet old Chinese room at night; behind the table a big plain smooth pale cream plaster wall that fills most of the background, lit warm gold by the lamp, with a small round paper lattice window high in one corner showing a pale moon; in front a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the near edge of the dish; a soft round red floor cushion on the wooden floor below the table; the lamp is the only light, the rest of the room soft and dim; [[cat]] has crept out from under the cushion and stands up on his hind legs against the wall, reaching one soft round paw up curiously to touch a big flying bird shadow on the pale wall, eyes big and sparkly, a playful smile with mouth closed; on top of the lamp [[mouse]] flaps his two crossed paws in front of the flame making the bird shadow, giggling, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f8.png**
```
inside a quiet old Chinese room at night; behind the table a big plain smooth pale cream plaster wall that fills most of the background, lit warm gold by the lamp, with a small round paper lattice window high in one corner showing a pale moon; in front a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the near edge of the dish; a soft round red floor cushion on the wooden floor below the table; the lamp is the only light, the rest of the room soft and dim; on the pale wall two big soft grey shadows dance together, the round-eared mouse shadow and the big cat shadow holding paws; in front, [[mouse]] dances on the rim of the oil dish with arms up and [[cat]] dances on the floor below on his hind legs, both laughing with closed happy eyes, the cat's mouth closed, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**f8e.png**
```
inside a quiet old Chinese room at night; behind the table a big plain smooth pale cream plaster wall that fills most of the background, lit warm gold by the lamp, with a small round paper lattice window high in one corner showing a pale moon; in front a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the near edge of the dish; a soft round red floor cushion on the wooden floor below the table; the lamp is the only light, the rest of the room soft and dim; the soft round red floor cushion below the table: [[mouse]] has just landed on the round fluffy tummy of [[cat]], who lies on his back on the cushion with paws up, both dizzy with swirly happy eyes and big smiles, the cat's mouth closed; on the pale wall behind, their two shadows lie in a funny heap; the lamp stands safely upright on the table, flame small and calm, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```

**r1.png**
```
inside a quiet old Chinese room at night; behind the table a big plain smooth pale cream plaster wall that fills most of the background, lit warm gold by the lamp, with a small round paper lattice window high in one corner showing a pale moon; in front a low dark-red wooden table; on the table stands the oil lamp: a tall slender old bronze lamp stand about six times as tall as the little mouse, with a round flat base, a thin straight stem with one small ring halfway up, and a shallow round dish on top holding golden oil, one small gentle flame on a wick at the near edge of the dish; a soft round red floor cushion on the wooden floor below the table; the lamp is the only light, the rest of the room soft and dim; [[mouse]] sleeps curled up on the round tummy of [[cat]], who sleeps on his back on the red cushion, both peaceful and smiling; on the pale wall behind them a big soft shadow of the two sleeping together like a little hill, the lamp flame small and calm, a cozy warm picture, Chinese watercolor painting style for a children's picture book, soft transparent watercolor washes blooming gently on textured xuan rice paper, delicate fine ink brush outlines, fresh light Chinese palette of peach pink, vermilion, willow green, pale indigo and warm ochre with a warm golden lamp glow, generous empty space, cute rounded proportions and big round gentle eyes with white highlights, simple uncluttered composition with one clear focus, only the characters named in the prompt and no extra animals, no text, no watermark, no seal, no calligraphy, the scene painted all the way to the bottom edge with no blank paper, vertical 9:16, keep every face in the upper 60% of the image
```
