# X01 · Yuanyuan's Zoo Day 圆圆的杭州动物园（专属绘本第一单）

> 专属绘本线（x）｜真实孩子（用户女儿圆圆，1 岁半，英文名用拼音 Yuanyuan；照片上的小翅膀不画，家长 11-06 定）｜家长收料单 `profile.json`（不进仓库）｜主角：[[kid]] 一个人（11-06 用户定：专属绘本不带栗栗，松鼠在旁边很出戏；第二个声音用旁白）｜受众 1–3 岁｜9:16 竖版｜关键帧钩子 + 9 页 + 今日单词复习 3 页 + 片尾，目标 45–50 秒｜日常模式（全关键帧）｜eleven_v3 配音｜中英字幕
>
> 2026-11-06 写。家长给的顺序：金鱼馆 → 海狮表演 → 大象 → 老虎 → 豹子 → 小猴子和大猩猩 → 其他动物。剧本严格按这个顺序走。杭州动物园实情（本地宝 2026-03 更新）：有金鱼园、海狮馆、大象馆、长颈鹿馆、两栖爬虫馆，室外有虎、狮、熊、小熊猫、黑猩猩等；**全园禁止投喂**，所以剧本里没有喂动物。海狮表演的具体节目没查到，按常见节目写（拍鳍、顶球、拍水落水），家长看了可以改。

## 1. 概要

- **家长给的一段话**：带圆圆去杭州动物园，先看金鱼，然后看海狮表演，再看大象、老虎、豹子、小猴子和大猩猩。
- **三句话**：① 圆圆进园，先到金鱼馆，红金鱼游到玻璃前，圆圆拍手；② 海狮馆：海狮突然钻出水面"Arf! Arf!"，圆圆捂住脸从指缝里看；海狮拍鳍，旁白带她拍手，圆圆跟着拍；海狮顶球、落水溅水花，圆圆笑开了；③ 接着大象喷水、老虎打哈欠、豹子趴在石头上、小猴子学她动作、大猩猩坐着安静地看她，傍晚坐长椅上说再见。
- **今日单词**：sea lion 海狮 · elephant 大象 · tiger 老虎
- **张力**：小。p02 海狮突然冒头（谷，捂脸）→ p03 海狮拍鳍、旁白带着拍手、圆圆跟着拍（转）→ p04 海狮顶球落水，大笑（峰）→ 后半段轻松逛园收尾。
- **互动**：p01 `Fish!` 指着喊；p03 `Clap, clap!` 家长带圆圆一起拍手；p05 `Again!` 跟着喊；p06 `Roar!` 跟老虎一起吼。
- **台词**：钩子 1 句 + 正片 17 句；圆圆的台词 1–2 个词（1 岁多说不了长句，家长念给她听也顺口），旁白 3–5 词。总长按 45–50 秒排，超了先砍 hold 和复习页 lead。
- **出场**：只有 [[kid]]；金鱼、海狮、大象、老虎、豹子、猴子、大猩猩直接写在提示词里；家长不入画；画面里不出现其他游客，也不出现栗栗或任何系列角色。
- **孩子形象**：角色卡由 `photo_character.py describe → cards → pick` 从家长照片生成，不在这里写外貌。照片上的翅膀装饰不画进角色（家长定）。

## 2. 开头钩子（关键帧，约 3 秒）

- **大字标题**：圆圆的动物园 · 专属英文绘本
- **小字**：用孩子自己的照片做的绘本 · 中英字幕
- **旁白**：`[excited] A zoo day!`　动物园的一天！
- **钩子首帧出图提示词**：
  ```
  a big round wooden zoo entrance gate with a simple carved animal shape on top and no text, bright morning light, a few big soft tree shapes; [[kid]] stands alone at the gate looking up at the arch with big sparkling excited eyes and an open-mouthed smile, both little arms raised high, bouncing on her toes, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, the characters fill the frame naturally and are centered vertically, faces between 25% and 65% of the image height, the scene continues all the way to the bottom edge with no empty band, nothing important in the bottom 15%
  ```

## 3. 分页表

| 页 | 画面 | 台词 `speaker: English / 中文` | 运镜 | 音效 |
|---|---|---|---|---|
| p01 | 金鱼馆，大玻璃缸里红金鱼游到圆圆面前，圆圆拍玻璃 | kid: Fish! Fish! / 鱼！鱼！ · narrator: A red goldfish! / 一条红金鱼！ | in | 水泡 |
| p01b | 金鱼吐泡泡，圆圆鼻子贴到玻璃上 | （无） | — | pop |
| p02 | 海狮馆看台，海狮突然从水里钻出来叫，圆圆捂住脸从指缝里看 | narrator: Arf! Arf! A sea lion! / 嗷！嗷！一只海狮！ · kid: Oh... / 哦…… | in | splash |
| p02b | 海狮歪头看她，圆圆放下手露出半张脸 | （无） | — | — |
| p03 | 海狮坐直拍鳍，圆圆看得入神 | narrator: Clap, clap! Like this! / 拍拍手！像这样！ | in | 掌声 |
| p03b | 圆圆也拍起手来，海狮更起劲 | kid: Clap, clap! / 拍拍手！ | — | 掌声 |
| p04 | 海狮鼻尖顶着红球，圆圆大笑 | narrator: Ball on the nose! / 球顶在鼻子上！ · kid: Yay! / 耶！ | out | sparkle |
| p04b | 海狮甩球跳进水里，水花溅上看台 | narrator: Good job, sea lion! / 真棒，海狮！ | — | splash |
| p05 | 大象馆，大象喷水，两人闭眼笑 | narrator: Splash! A big elephant! / 哗！一头大大象！ · kid: Again! / 再来！ | left | whoosh |
| p05b | 水花成一道弧落在两人头上 | （无） | — | — |
| p06 | 老虎馆，老虎趴在大石头上张大嘴打哈欠 | narrator: A tiger! Roar! / 老虎！吼！ · kid: Roar! / 吼！ | in | 低吼 |
| p07 | 豹子趴在高高的树枝上，尾巴垂下来，圆圆指着身上的斑点 | narrator: A leopard! Spots, spots! / 一只豹子！斑点，斑点！ | up | — |
| p08 | 小猴子学圆圆把手放头上，大猩猩坐在后面安静地看 | kid: Monkey! / 猴子！ · narrator: He copies you! / 他在学你！ | in | pop |
| p08b | 猴子换成挠耳朵，圆圆也挠耳朵 | （无） | — | — |
| p09 | 傍晚长椅，圆圆朝海狮池挥手 | kid: Bye-bye, sea lion! / 再见，海狮！ · narrator: What a day! / 多棒的一天！ | in | — |
| r1–r3 | 复习：sea lion（p04）· elephant（p05）· tiger（p06） | 角色各说一遍，停 1.5 秒跟读 | — | ding |

## 4. 出图提示词（角色一律写 `[[kid]]`，codex_images.py 自动展开并带参考图；全片没有栗栗）

**p01.png**
```
inside a goldfish hall, one big clear glass tank filling the background with calm pale blue water, a single plump bright red-and-white goldfish with a long flowing tail swimming right up to the glass; [[kid]] stands alone at the tank with both small hands pressed flat on the glass, big eyes wide and mouth open in delight, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, the characters fill the frame naturally and are centered vertically, faces between 25% and 65% of the image height, the scene continues all the way to the bottom edge with no empty band, nothing important in the bottom 15%
```

**p02.png**
```
inside a sea lion show arena, a big blue pool with a low curved white wall and a few empty rows of simple stone seats behind, a sleek dark brown sea lion bursting up out of the water at the lower left with its mouth wide open barking and water drops flying; [[kid]] sits on the low front seat on the right side of the picture, her face around the vertical middle of the image, startled, both small hands resting on her cheeks with her big round eyes fully visible and wide open, the empty seat rows filling the space above her head, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, the characters fill the frame naturally and are centered vertically, faces between 25% and 65% of the image height, the scene continues all the way to the bottom edge with no empty band, nothing important in the bottom 15%
```

**p03.png**
```
inside the sea lion show arena, the sleek dark brown sea lion sits up tall on the pool edge clapping its two front flippers together with a happy open mouth; [[kid]] stands at the low pool wall watching the sea lion closely with her own small hands half raised ready to clap and a curious little smile, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, the characters fill the frame naturally and are centered vertically, faces between 25% and 65% of the image height, the scene continues all the way to the bottom edge with no empty band, nothing important in the bottom 15%
```

**p04.png**
```
inside the sea lion show arena, the sleek dark brown sea lion balances a bright red ball on the tip of its nose, head tilted up proudly, water drops sparkling around it; [[kid]] stands at the low pool wall laughing with her whole face and both arms thrown up high, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, the characters fill the frame naturally and are centered vertically, faces between 25% and 65% of the image height, the scene continues all the way to the bottom edge with no empty band, nothing important in the bottom 15%
```

**p05.png**
```
a big friendly gray elephant standing in a shallow blue pool behind a low stone wall, lifting its trunk and spraying a wide fan of sparkling water drops up into the air; [[kid]] stands at the wall squeezing her eyes shut and laughing as a few drops land on her, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, the characters fill the frame naturally and are centered vertically, faces between 25% and 65% of the image height, the scene continues all the way to the bottom edge with no empty band, nothing important in the bottom 15%
```

**p06.png**
```
a big orange tiger with bold black stripes lying on a large flat gray rock behind a wide clear glass wall, its mouth open in a huge sleepy yawn showing a pink tongue, looking harmless and round; [[kid]] stands in front of the glass with her own mouth open wide copying the yawn, both little hands up like claws, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, the characters fill the frame naturally and are centered vertically, faces between 25% and 65% of the image height, the scene continues all the way to the bottom edge with no empty band, nothing important in the bottom 15%
```

**p07.png**
```
a slim spotted leopard lying relaxed along a thick high tree branch with its long tail hanging straight down, golden fur with soft dark rosette spots, calm half-closed eyes; [[kid]] stands below at a low wooden fence looking straight up, pointing one finger up at the spots with a wondering open mouth, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, the characters fill the frame naturally and are centered vertically, faces between 25% and 65% of the image height, the scene continues all the way to the bottom edge with no empty band, nothing important in the bottom 15%
```

**p08.png**
```
a small brown monkey sitting on a thick low branch behind a low fence holding one hand on top of its own head with a cheeky grin, and a big gentle black gorilla sitting calmly on the grass further behind with its arms folded, watching kindly; [[kid]] stands facing the monkey with one hand on top of her own head in exactly the same pose, delighted, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, the characters fill the frame naturally and are centered vertically, faces between 25% and 65% of the image height, the scene continues all the way to the bottom edge with no empty band, nothing important in the bottom 15%
```

**p09.png**
```
late afternoon warm golden light on a quiet zoo path, [[kid]] sits alone on a wooden bench swinging her short legs, waving happily toward the distance where the sea lion pool and a small sea lion silhouette show soft and small far in the background, content and a little tired, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes, plenty of open empty space, no small scattered details like flowers, pebbles or signs unless the prompt names them, gentle warm light, a limited harmonious palette of soft greens, warm browns and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters and animals named in the prompt and no extra animals or people, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, the characters fill the frame naturally and are centered vertically, faces between 25% and 65% of the image height, the scene continues all the way to the bottom edge with no empty band, nothing important in the bottom 15%
```

### 关键帧（底图出好后自动出）

**p01b.png** ← p01.png
```
the goldfish blows three little round bubbles right in front of the toddler, she leans in close to the glass with her head and face staying exactly as round and cute as before, eyes wide with delight and a small open-mouthed baby smile with no teeth showing
```

**p02b.png** ← p02.png
```
the sea lion has settled back half in the water and tilts its head curiously at the toddler with a friendly closed mouth, the toddler keeps sitting upright in the same place and size, her head level and not tilted, she lowers her hands to her lap and looks at the sea lion with a small shy closed-mouth smile and big round eyes
```

**p03b.png** ← p03.png
```
the toddler now claps her own small hands together with a big proud open-mouthed smile and bright eyes, and the sea lion claps faster with its mouth open wide
```

**p04b.png** ← p04.png
```
the sea lion has flicked the red ball high into the air and dives into the pool, a big splash of white water bursting up over the wall, the toddler squealing with delight, standing upright in exactly the same place and size as before, not leaning, her whole head and hair well inside the picture and far from the left edge
```

**p05b.png** ← p05.png
```
the elephant's water spray is now a big arc coming right over the wall, big drops landing on the toddler's hair, her laughing even harder
```

**p08b.png** ← p08.png
```
the monkey now scratches behind its own ear with one hand and the toddler scratches behind her own ear in the same way, both looking at each other, the gorilla laughing
```

### 封面关键画面

用 p04（海狮顶球、圆圆大笑）出 `cover.png`，`brand.py --crop-3x4 0 --title-en "Yuanyuan's Zoo Day" --title-zh 圆圆的动物园 --words "sea lion"=海狮 elephant=大象 tiger=老虎`。

## 5. 配音清单

见 story.json 的 `say`：kid 借 bun 的音色（cast.json 由 pick 生成，家长听了嫌不像再换），旁白用系列旁白，原来栗栗的台词全部改给旁白。圆圆的台词都很短，语气标签只用 `[excited]` `[laughing]` `[whispers]`，不用 `[gasps]`（会拖 0.8 秒）、不用 `[clearly]`。p02 小声、p04 大笑形成对比。

## 6. 交付

成品包同主文件第 8 节：mp4、3:4 封面、`_print.pdf`（A4 家用打印版）、srt。专属绘本不发账号，交付页只给家长；发布文案不用写。看过效果后家长确认，再 `photo_character.py purge` 删照片。
