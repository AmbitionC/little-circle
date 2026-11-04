# X00 · Mia's Zoo Day 米娅的动物园（跑通链路用的测试集）

> 专属绘本线（x）｜虚构孩子 Mia（photo_character.py fake 出的假照片，不是真人）｜家长收料单 `profile.json`｜主角：[[kid]]（米娅）＋ 客串 [[nutty]]｜2–3 岁｜9:16 竖版｜关键帧钩子 + 8 页 + 今日单词复习 3 页 + 片尾，目标 50–55 秒（专属绘本给家长自己看，不受账号 50 秒上限约束，但也别拖）｜日常模式（全关键帧）｜eleven_v3 配音｜中英字幕
>
> 2026-11-04 写。用途只有一个：把「照片 → 角色卡 → 出图 → 配音 → 成片 → PDF」整条链路跑一遍，把坑修掉。正式第一单是 x01（用户女儿的动物园）。

## 1. 概要

- **家长给的一段话**（profile.json）：周六带米娅去动物园，看了长颈鹿、大象、猴子，最喜欢喂羊：一开始躲在后面不敢，羊舔了她的手，她笑了半天。
- **三句话**：① Mia 和栗栗逛动物园，长颈鹿好高、大象喷水、猴子学她动作；② 到了喂羊区，羊走过来，Mia 躲到栗栗背后；栗栗示范喂，Mia 自己伸手，羊舔了她的手，痒得大笑；③ 傍晚坐在长椅上对动物们说再见，Mia 说：我会喂羊啦。
- **今日单词**：giraffe 长颈鹿 · elephant 大象 · feed 喂
- **张力**：小（专属绘本的主线是「真实经历 + 一个小勇敢」）：p05 不敢（谷）→ p06 看栗栗做 → p07 自己做到（峰）。家长描述里的真实细节（躲在后面、羊舔手、笑了半天）原样保留，AI 只补了栗栗示范和前面三种动物的小互动。
- **互动**：p03 大象喷水 `Again, elephant!` 宝宝会跟着喊；p04 和猴子做同样动作（家长让宝宝也把手放头上）；p07 `It tickles!` 挠痒。
- **台词**：钩子 1 句 + 正片 13 句，每句 3–5 词；复习 3 个词不算。
- **出场**：[[kid]]、[[nutty]]；动物（长颈鹿、大象、猴子、羊）不是系列角色，直接写在提示词里；家长不入画。

## 2. 开头钩子（关键帧，约 3 秒）

- **大字标题**：米娅的动物园 · 专属英文绘本
- **小字**：用孩子自己的照片做的绘本 · 中英字幕
- **旁白**：`[gasps] A zoo day!`　动物园的一天！
- **钩子首帧出图提示词**：
  ```
  a big round wooden zoo entrance gate with a simple carved animal shape on top and no text, bright morning light, a few big soft tree shapes; [[kid]] stands at the gate holding [[nutty]]'s paw, both looking up at the arch with sparkling excited eyes and open-mouthed smiles, the child bouncing on her toes, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
  ```

## 3. 分页表

| 页 | 画面 | 台词 `speaker: English / 中文` | 运镜 | 音效 |
|---|---|---|---|---|
| p01 | 进门，Mia 拉着栗栗往前冲 | kid: Let's go, Nutty! / 走吧，栗栗！ | in | 脚步 |
| p02 | 长颈鹿高到画面顶，两人仰头 | kid: Wow! So tall! / 哇！好高！ · nutty: Hello, giraffe! / 你好，长颈鹿！ | up | — |
| p02b | 长颈鹿低头到 Mia 面前 | （无） | — | whoosh |
| p03 | 大象喷水，两人闭眼笑 | narrator: Splash! A big elephant! / 哗！一头大大象！ · kid: Again, elephant! / 再来一次，大象！ | left | splash(whoosh) |
| p04 | 猴子和 Mia 同一个动作 | kid: Look! A monkey! / 看！一只猴子！ · nutty: He copies you! / 他在学你！ | in | pop |
| p05 | 喂羊区，Mia 躲到栗栗后面 | kid: It's so big... / 它好大…… | right | — |
| p06 | 栗栗示范喂羊 | nutty: Feed the sheep! Like this. / 喂羊！像这样。 | in | chomp |
| p07 | Mia 自己喂，羊舔手，大笑 | kid: It tickles! / 好痒！ · nutty: You did it, Mia! / 你做到啦，米娅！ | out | sparkle |
| p08 | 傍晚长椅，挥手再见 | kid: Bye-bye, animals! / 再见，动物们！ · kid: I can feed the sheep! / 我会喂羊啦！ | in | — |
| r1–r3 | 复习：giraffe（p02b）· elephant（p03）· feed（p07） | 角色各说一遍，停 1.5 秒跟读 | — | ding |

## 4. 出图提示词（角色一律写 `[[kid]]` `[[nutty]]`，codex_images.py 自动展开并带参考图）

**p01.png**
```
a wide sunny path just inside a zoo entrance, a big round wooden gate arch behind them with no text on it, a few big soft tree shapes; [[kid]] marches ahead pulling [[nutty]] along by the paw with her other arm pointing forward, both beaming with excitement, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p02.png**
```
a very tall giraffe standing behind a low wooden fence, its long spotted neck reaching all the way up to the top of the picture and its head near the top edge looking down kindly; [[kid]] and [[nutty]] stand small at the fence in the middle of the picture, both leaning back with mouths open in amazement, looking straight up at the giraffe, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p03.png**
```
a big friendly gray elephant standing in a shallow blue pool behind a low stone wall, lifting its trunk and spraying a wide fan of sparkling water drops up into the air; [[kid]] and [[nutty]] stand at the wall in the middle of the picture squeezing their eyes shut and laughing as a few drops land on them, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p04.png**
```
a small brown monkey sitting on a thick branch behind a low fence, holding one hand on top of its own head with a cheeky grin; [[kid]] stands facing the monkey with one hand on top of her own head in exactly the same pose, delighted, while [[nutty]] beside her giggles with both paws over his mouth, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p05.png**
```
a small petting pen with a low wooden fence and soft straw on the ground; a big fluffy white sheep with a gentle face walks slowly toward them; [[kid]] hides behind [[nutty]] holding on to his scarf and peeking out with wide worried eyes, while the squirrel holds a little bunch of fresh green leaves and smiles calmly at the sheep, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p06.png**
```
in the petting pen, [[nutty]] stands close to the big fluffy white sheep holding a bunch of green leaves out flat on his open paw while the sheep gently nibbles the leaves; [[kid]] stands a step behind him watching closely with wide curious eyes, her own hands clasped in front of her, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p07.png**
```
in the petting pen, [[kid]] holds a few green leaves out flat on her own open hand and the big fluffy white sheep licks her palm with its pink tongue; she scrunches up her whole face in a huge ticklish laugh with her shoulders up, while [[nutty]] beside her cheers with both paws in the air and his big tail puffed up, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p08.png**
```
late afternoon warm golden light on a quiet zoo path, [[kid]] and [[nutty]] sit side by side on a wooden bench, the child waving happily toward the distance where the tall giraffe stands small and soft far in the background, the squirrel leaning his head against her arm, both content and a little tired, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

### 关键帧（底图出好后自动出）

**p02b.png** ← p02.png
```
the giraffe bends its long neck all the way down so its big gentle face comes right in front of the child, nose almost touching her hair, and both small characters freeze with huge round eyes
```

**p03b.png** ← p03.png
```
the elephant's water spray is now a big arc coming right over the wall, big drops landing on the child's hair and the squirrel's tail hanging soaked and flat, both characters laughing even harder
```

**p06b.png** ← p06.png
```
the sheep has eaten half of the leaves and chews happily with its eyes closed, the squirrel turns his head to grin at the child, and the child takes a small step closer
```

**p07b.png** ← p07.png
```
the child pulls her hand back and hugs it to her chest giggling with her eyes closed, the sheep looks at her hopefully for more, the squirrel claps
```

### 封面关键画面

用 p08（长椅挥手）出 `cover.png`，`brand.py --title-en "Mia's Zoo Day" --title-zh 米娅的动物园 --words giraffe=长颈鹿 elephant=大象 feed=喂`。

## 5. 配音清单

见 story.json 的 `say`：kid 借 bun 的音色（cast.json），旁白用系列旁白。每句带语气标签；p05 小声、p07 大笑形成对比。

## 6. 交付

成品包同主文件第 8 节：mp4、3:4 封面、`_print.pdf`（A4 家用打印版）、srt。专属绘本不发账号，交付页只给家长；发布文案不用写。
