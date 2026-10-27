# C05 · Bun's Rainy Picnic 小兔的下雨野餐

> 认知小绘本（带剧情）｜主线：天气 sunny / rainy / windy，用"野餐遇上雨"串成一个故事｜主角：Bun（小灰兔）｜2–3 岁英语启蒙｜9:16 竖版｜可灵钩子 5 秒 + 8 页动态绘本 + 片尾 3.5 秒，完整版约 45 秒，精华版（前 4 页）约 25 秒｜全英文配音｜中英字幕

> 2026-10-26 按新标准重写：每集一个主题（一个词串成故事，或讲一个道理），不做一页一问一答；台词按 2–3 岁写。依据见 [docs/benchmark-story-2026-10.md](../../docs/benchmark-story-2026-10.md)。

## 1. 概要

**一句话剧情**：Bun 在大晴天野餐，一滴雨砸在鼻尖上，接着下起大雨。Bun 把两只长耳朵翻过来盖在头上当伞，一阵风把 Bun 吹得飘了起来。Hazel 和栗栗举着大叶子跑来，三个挤在叶子下面等雨停，天上出了彩虹。

- **主题**：认天气；下雨也能开开心心（"Rain or sun, let's play!"）
- **今日单词**（封面、置顶评论用）：sunny 晴天 · rainy 下雨 · windy 刮风（本集还有 rainbow 彩虹）
- **重复句型**：`It's sunny!` / `It's rainy!` / `It's windy!`
- **台词量**：全片 11 句，每句 3–5 个词，每页最多两句。
- **童趣**：雨点"啪"地砸在 Bun 鼻尖上，Bun 眼睛对成斗鸡眼；Bun 把长耳朵翻过来当伞；一阵风把 Bun 连人带耳朵吹得飘起来；三个小伙伴挤在一片叶子下。
- **互动**：第 2 页旁白问 "What is that?"，停 1.5 秒让宝宝喊 "Rain!"；结尾 Bun 问宝宝 "Sunny or rainy?"。

## 2. 开头钩子（可灵 5 秒）

- **大字标题（给家长看，第 1 帧就出现）**：晴天、下雨、刮风，英语怎么说？
- **小字**：3岁英语启蒙 · 跟 Bun 学天气
- **备选标题**：小兔把耳朵当伞，结果被风吹走了！
- **旁白**（0.6 秒进）：`Bun has a picnic!` Bun 在野餐！
- **可灵首帧出图提示词**：
  ```
  a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest, sitting happily on a red checkered picnic blanket with carrot sandwiches, bright sunshine, sunny meadow at the edge of a forest, one small gray cloud far away, close-up, polished digital children's picture book illustration, richly detailed soft fluffy fur with fine strands, big glossy round eyes with bright catchlights, chubby cute proportions, joyful expressive faces, lush sunlit forest with moss, ferns, little wildflowers and red-capped mushrooms, warm golden sunlight with soft bokeh, bright saturated warm colors, crisp clean edges, high detail, no text, no watermark, vertical 9:16
  ```
- **可灵尾帧**：直接用 p01.png。
- **可灵提示词**：小灰兔 Bun 坐在红格子野餐布上，开心地晃着耳朵吃胡萝卜三明治，阳光很好，远处一朵小灰云慢慢飘过来。精致数字绘本插画风格（毛发细腻、大眼睛、暖色阳光），保持角色外形和颜色不变，动作轻柔、幅度小。
- **负面提示词**：变形，多余肢体，脸部扭曲，画面闪烁，写实风格，文字，水印
- **参数**：图生视频，5 秒，9:16，1080p，不开原生音频，导出为 `kling01.mp4`。

## 3. 分镜

| 页 | 段落 | 画面 | 台词 | 音效 | 运镜 |
|---|---|---|---|---|---|
| p01 | 起 | 大晴天，Bun 在红格子野餐布上开心地晃耳朵 | **Bun**：It's sunny! Let's play!<br>晴天！一起玩吧！ | — | 缓推 |
| p02 | 承 | 笑点：一滴大雨点"啪"地砸在 Bun 鼻尖上，Bun 眼睛对成斗鸡眼 | **Bun**：Oh! What is that?<br>哦！那是什么？<br>**旁白**：What is it? Hmm?<br>是什么呢？嗯？（停 1.5 秒，等宝宝喊 Rain） | pop | 硬切（`cut`）+ 上移 |
| p03 | 承 | 大雨哗哗下，Bun 的耳朵耷拉下来，三明治都湿了 | **Bun**：It's rainy! I'm wet!<br>下雨了！我湿了！ | leaves | 下移 |
| p04 | 转 | 笑点：Bun 灵机一动，把两只长耳朵翻过来盖在头上当伞 | **Bun**：Look! Ear umbrella!<br>看！耳朵雨伞！ | ding | 缓推 |
| p05 | 转 | 笑点：一阵大风吹来，耳朵像翅膀一样张开，Bun 被吹得飘离地面 | **旁白**：Whoosh! It's windy!<br>呼——刮风啦！<br>**Bun**：Help! I'm flying!<br>救命！我飞起来啦！ | whoosh | 硬切（`cut`）+ 上移 |
| p06 | 合 | Hazel 和栗栗举着一片超大的树叶跑来，把 Bun 拉下来 | **Hazel**：Come here, Bun!<br>Bun，快过来！ | — | 左移 |
| p07 | 合 | 三个小伙伴挤在大叶子下，雨停了，天上出现彩虹 | **栗栗**：Look! A rainbow!<br>看！彩虹！ | sparkle | 缓拉 |
| p08 | 寓意 | 三个小伙伴在彩虹下跳，Bun 对着镜头笑 | **Bun**：Rain or sun, let's play!<br>下雨晴天，都能玩！<br>**旁白**：The end. Bye-bye!<br>讲完啦，拜拜！ | ding | 缓推 |

精华版（`--max-pages 4`）停在第 4 页"耳朵雨伞"，悬念是"风来了会怎样？"。

## 4. 出图提示词

每张都把角色设定图当参考图上传，锁住长相（`codex_images.py` 认到角色原文会自动带上 `series/refs/` 里的参考图）。单独出原图，9:16，至少 1080×1920；下方四分之一留给字幕，脸不要放在那里。

**p01.png**
```
a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest, sitting on a red checkered picnic blanket with carrot sandwiches, happily swinging long ears, bright sunshine, sunny meadow at the edge of a forest, polished digital children's picture book illustration, richly detailed soft fluffy fur with fine strands, big glossy round eyes with bright catchlights, chubby cute proportions, joyful expressive faces, lush sunlit forest with moss, ferns, little wildflowers and red-capped mushrooms, warm golden sunlight with soft bokeh, bright saturated warm colors, crisp clean edges, high detail, no text, no watermark, vertical 9:16, keep the bottom quarter of the image simple and free of faces
```
**p02.png**
```
a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest, close-up, a big fat raindrop landing right on the tip of the nose, eyes crossed looking at it, funny face, a gray cloud above, picnic blanket, polished digital children's picture book illustration, richly detailed soft fluffy fur with fine strands, big glossy round eyes with bright catchlights, chubby cute proportions, joyful expressive faces, lush sunlit forest with moss, ferns, little wildflowers and red-capped mushrooms, warm golden sunlight with soft bokeh, bright saturated warm colors, crisp clean edges, high detail, no text, no watermark, vertical 9:16, keep the bottom quarter of the image simple and free of faces
```
**p03.png**
```
a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest, sitting in heavy rain on a soaked picnic blanket, long ears drooping, wet fur, soggy carrot sandwiches, gray rainy sky, meadow at the edge of a forest, polished digital children's picture book illustration, richly detailed soft fluffy fur with fine strands, big glossy round eyes with bright catchlights, chubby cute proportions, joyful expressive faces, lush sunlit forest with moss, ferns, little wildflowers and red-capped mushrooms, warm golden sunlight with soft bokeh, bright saturated warm colors, crisp clean edges, high detail, no text, no watermark, vertical 9:16, keep the bottom quarter of the image simple and free of faces
```
**p04.png**
```
a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest, proudly flipping both long ears forward over the head like an umbrella, rain bouncing off the ears, pleased funny face, rainy meadow at the edge of a forest, polished digital children's picture book illustration, richly detailed soft fluffy fur with fine strands, big glossy round eyes with bright catchlights, chubby cute proportions, joyful expressive faces, lush sunlit forest with moss, ferns, little wildflowers and red-capped mushrooms, warm golden sunlight with soft bokeh, bright saturated warm colors, crisp clean edges, high detail, no text, no watermark, vertical 9:16, keep the bottom quarter of the image simple and free of faces
```
**p05.png**
```
a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest, being lifted off the ground by a strong gust of wind, long ears spread out like wings, surprised funny face, leaves and raindrops swirling, rainy meadow at the edge of a forest, polished digital children's picture book illustration, richly detailed soft fluffy fur with fine strands, big glossy round eyes with bright catchlights, chubby cute proportions, joyful expressive faces, lush sunlit forest with moss, ferns, little wildflowers and red-capped mushrooms, warm golden sunlight with soft bokeh, bright saturated warm colors, crisp clean edges, high detail, no text, no watermark, vertical 9:16, keep the bottom quarter of the image simple and free of faces
```
**p06.png**
```
a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls and a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf running over holding one giant green leaf like an umbrella, pulling a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest down by the paw, rainy meadow at the edge of a forest, polished digital children's picture book illustration, richly detailed soft fluffy fur with fine strands, big glossy round eyes with bright catchlights, chubby cute proportions, joyful expressive faces, lush sunlit forest with moss, ferns, little wildflowers and red-capped mushrooms, warm golden sunlight with soft bokeh, bright saturated warm colors, crisp clean edges, high detail, no text, no watermark, vertical 9:16, keep the bottom quarter of the image simple and free of faces
```
**p07.png**
```
a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf, a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls and a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest squeezed together under one giant green leaf, the rain stopping, a big bright rainbow in the sky, sun coming out, meadow at the edge of a forest, polished digital children's picture book illustration, richly detailed soft fluffy fur with fine strands, big glossy round eyes with bright catchlights, chubby cute proportions, joyful expressive faces, lush sunlit forest with moss, ferns, little wildflowers and red-capped mushrooms, warm golden sunlight with soft bokeh, bright saturated warm colors, crisp clean edges, high detail, no text, no watermark, vertical 9:16, keep the bottom quarter of the image simple and free of faces
```
**p08.png**
```
a fluffy light-gray bunny with long ears, one ear slightly floppy, wearing a small red vest hopping happily and smiling at the viewer, a small red squirrel with a big fluffy tail, round bright eyes, wearing a little green knitted scarf and a round little hedgehog boy with soft brown spines, rosy cheeks, wearing tiny yellow overalls jumping alongside, a bright rainbow behind them, wet sparkling grass, meadow at the edge of a forest, polished digital children's picture book illustration, richly detailed soft fluffy fur with fine strands, big glossy round eyes with bright catchlights, chubby cute proportions, joyful expressive faces, lush sunlit forest with moss, ferns, little wildflowers and red-capped mushrooms, warm golden sunlight with soft bokeh, bright saturated warm colors, crisp clean edges, high detail, no text, no watermark, vertical 9:16, keep the bottom quarter of the image simple and free of faces
```

**封面关键画面**（发布页手动上传当封面）：用 p08 同一场景再出一张，主角在下半部分，上方 40% 是天空或树冠，留给标题。

出图时容易出问题的地方：p02 雨点要落在鼻尖上、看得清；p04、p05 耳朵翻到头上和像翅膀张开，AI 容易画成普通兔子，不像就单张重出；p05 只是轻轻飘起，不要画得像遇险。

## 5. 配音清单

角色音色统一用 `series/cast.json`。订阅前出样片用 `--cast ../../series/cast_kokoro.json`，样片不发布。

| 文件 | 角色 | 台词 | 语气 | 中文 |
|---|---|---|---|---|
| v_hook_narrator | 旁白 | Bun has a picnic! | 轻快 | Bun 在野餐！ |
| v_p01_bun | Bun | It's sunny! Let's play! | 开心 | 晴天！一起玩吧！ |
| v_p02a_bun | Bun | Oh! What is that? | 吃惊 | 哦！那是什么？ |
| v_p02b_narrator | 旁白 | What is it? Hmm? | 放慢，对着镜头 | 是什么呢？嗯？ |
| v_p03_bun | Bun | It's rainy! I'm wet! | 委屈 | 下雨了！我湿了！ |
| v_p04_bun | Bun | Look! Ear umbrella! | 得意 | 看！耳朵雨伞！ |
| v_p05a_narrator | 旁白 | Whoosh! It's windy! | 夸张 | 呼——刮风啦！ |
| v_p05b_bun | Bun | Help! I'm flying! | 又怕又好笑 | 救命！我飞起来啦！ |
| v_p06_hazel | Hazel | Come here, Bun! | 着急又温柔 | Bun，快过来！ |
| v_p07_nutty | 栗栗 | Look! A rainbow! | 惊喜 | 看！彩虹！ |
| v_p08a_bun | Bun | Rain or sun, let's play! | 对着镜头，开心 | 下雨晴天，都能玩！ |
| v_p08b_narrator | 旁白 | The end. Bye-bye! | 温柔 | 讲完啦，拜拜！ |

## 6. 素材清单

放到 `episodes/c05-weather/`：`kling01.mp4`、`p01.png`～`p08.png`（`codex_images.py` 还会出 `kling_first.png`、`cover.png`）。音效和音乐引用仓库根目录的 `assets/sfx/`、`assets/bgm/`（本机生成，不提交）；还没生成的话先把 story.json 里的 `sfx`、`bgm` 删掉也能出片。

## 7. 发布文案

- **抖音标题**：晴天、下雨、刮风，英语怎么说？｜小兔的下雨野餐
- **小红书标题**：小兔的下雨野餐｜3岁英语启蒙绘本
- **正文**：
```
🌰 认知小绘本 第5集｜Bun's Rainy Picnic 小兔的下雨野餐
Bun 在大晴天野餐，突然下起了雨！Bun 把长耳朵当伞，结果一阵风……

📖 今日单词：sunny 晴天｜rainy 下雨｜windy 刮风
🗣 跟读句子：
It's sunny! 晴天！
It's rainy! 下雨了！
It's windy! 刮风啦！

💡 亲子小互动：每天早上拉开窗帘问宝宝 "Sunny or rainy?"，让宝宝用 "It's sunny! / It's rainy!" 回答。

#幼儿英语启蒙 #英语启蒙 #儿童英语 #英语绘本 #亲子英语 #宝宝学天气
（本视频由 AI 辅助生成）
```
- **评论区置顶**：今日单词 sunny / rainy / windy。今天你们那里是什么天气？
- 发布时勾选“内容由 AI 生成”。抖音、小红书不放微信号、二维码、网址。

## 8. 放进“每天放什么”

- **单词音频**：sunny、rainy、windy、rainbow 各一条，外加 "It's sunny! / It's rainy!" 两句。
- **打印小绘本**：p01–p08 加中英字幕排成 A4，`sbv.py` 出片时一起出 PDF。
- **计划表里的一天**（示例）：早上拉开窗帘，一起说今天的天气 → 早饭时放一遍完整版 → 睡前翻打印小绘本，第 2 页一起喊 "Rain!"。
