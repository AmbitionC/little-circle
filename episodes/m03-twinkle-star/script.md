# M03 · The Little Star Falls Down 小星星掉下来了（老儿歌对话版 v2）

> 2026-11-05 第二版。第一版「摘星星」用户看完说：「背景音乐一会大一会小的，其次视频上有明显卡顿感，最后一个是故事本身不太有吸引力」，选了新故事。第一版剧本见 git 历史（2459d48）。
> 模式同 m02 对话版：背景是公有领域老儿歌 *Twinkle, Twinkle, Little Star*（18 世纪法国民歌旋律 + Jane Taylor 1806 年词），角色用简短英文对话讲故事，目标 45 秒。画风系列默认日系手绘简洁版，夜景。

## 0. 这一版改了什么

| 第一版的问题 | 原因 | 这一版怎么改 |
|---|---|---|
| 故事不吸引人 | 没有利害（只是"想要"）；水里倒影的反转 2–3 岁看不懂；歌和故事没关系 | 星星掉下来、越来越暗、回不了家（有急事）；**大家一起唱 Twinkle 把它唱亮**，歌就是解决办法（同 m02 大家一起喊 Pull）；Bruno 肚子当蹦床弹回天上，第一次砸到他鼻子（笑点） |
| 背景音乐忽大忽小 | 演唱人声每句台词开关一次，压 22 dB 再抬回，全片跳 22 次 | 全片乐器版旋律一个固定电平，不随台词起落；演唱只放在 p05 整段和片尾 |
| 画面卡顿 | 换图快慢不匀（8 处半秒内连切、p03 近 4 秒不动、片尾静止 2.5 秒），运镜幅度小 | 28 张图按每 1.3–1.8 秒一张排匀；镜头一直缓慢地动；同镜头内角色位置锁住只改动作；片尾也有动 |

## 0.1 人性 × 这一集怎么用

| 人性 | 怎么用 | 拉动哪个数据 |
|---|---|---|
| 熟悉感 | 家长哼了几十年的小星星旋律；p05 一开口就是原词 | 2 秒跳出率 |
| 着急 / 想帮忙 | 钩子：星星从天上掉下来，大字「小星星掉下来了！」；越来越暗 | 完播率 |
| 隔屏互动 | p04b Bun 对镜头 "Sing with us!"，宝宝跟着唱；p07 一起喊 UP | 家长拍娃晒、转发 |
| 大个子出糗 | Bruno 扔不上去 "Oops!"；肚子弹偏砸到自己鼻子 | 笑、评论 |
| 彩蛋 | Bruno 被砸的鼻子变成金色小星星 "My nose is a star!"（呼应他鼻尖的小红包） | 看到最后 |
| 睡前 | 皮皮挥手 "Good night, little star!" | 收藏、重复播放 |

## 1. 概要

- **Logline**：夜里一颗小星星掉进森林，越来越暗，回不了家。Bruno 扔、Bun 跳，都送不上去，星星快灭了。Bun 想到办法：大家一起唱 Twinkle, Twinkle，把它唱亮！亮起来的星星在 Bruno 的肚子上一弹，第一次砸到 Bruno 鼻子，第二次大家一起喊 UP，飞回了天上。皮皮说晚安，星星眨眼。彩蛋：Bruno 的鼻子变成了小星星。
- **家长钩子**：小星星掉下来了，怎么送它回家？
- **今日单词**：star 星星 · up 上 · good night 晚安（star 片中 + 演唱 ×3，up ×7）
- **用了哪些手法**：三次阶梯（扔 → 跳 → 唱亮再弹）；歌即解法；大个子出糗；隔屏互动；口头禅（Bruno "I am big!"、Bun "I have an idea!"）；彩蛋回扣角色特征。
- **道理**：大家一起，再难的事也能做到。
- **常理和安全**：小星星是巴掌大的道具角色（皮皮头那么大，两只小圆眼睛、小嘴巴），不说话，只靠表情和亮度；砸鼻子是软软一下、没受伤；蹦床是 Bruno 自己的肚子（角色设定"软得像蹦床"）。

## 2. 台词和音乐

| 页 | 画面 | 台词 | 音乐 |
|---|---|---|---|
| hook | kling_first.png：皮皮坐起来，指着一颗拖着光尾巴往下掉的星星 → h02.png：星星噗地落进落叶堆（硬切）→ h03.png：皮皮捧出暗暗的小星星 | **pip**：`Oh! A star fell down!`<br>哇！星星掉下来了！ | 八音盒起头，下落时一串下行音 |
| p01 | p01.png：特写，皮皮双手捧着暗淡、难过的小星星 → p01b.png：星星抬头望着天上的空缺 | **pip**：`It wants to go home.`<br>它想回家。 | 旋律（乐器版，固定音量，下同） |
| p02 | p02.png：Bruno 举着星星准备扔 → p02b.png：使劲往上扔，只高过头一点 → p02c.png：掉回来砸进爪子里（硬切） | **bruno**：`I am big! Up you go!`<br>我个子大！上去吧！<br>**bruno**：`Oops!`<br>哎呀！ | |
| p03 | p03.png：Bun 捧着星星蹲下 → p03b.png：高高跳起 → p03d.png：落地，低头看星星 → p03c.png：落地，星星几乎全暗，三个凑过来 | **bun**：`Up! Up!`<br>上！上！<br>**pip**：`Oh no! It's so dark!`<br>糟了！它好暗！ | 星星变暗时旋律只剩单音 |
| p04 | p04.png：Bun 耳朵"叮"地竖起、竖手指 → p04b.png：转身对镜头招手 | **bun**：`I have an idea! Let's sing!`<br>我有个好主意！我们来唱歌！<br>**bun**：`Sing with us!`<br>和我们一起唱！ | 叮一声 |
| p05 | p05.png：三个围着星星轻轻摇着唱 → p05b.png：星星亮了一点、睁开眼 → p05e.png：一起摇向另一边，又亮一点 → p05c.png：更亮、笑了 → p05f.png：唱得更响，星星离开叶子 → p05d.png：亮到照亮整片空地，飘起来 | （演唱，无台词）`Twinkle, twinkle, little star, how I wonder what you are!` | **整段英文演唱**（8 秒），伴奏渐强，越唱越亮 |
| p06 | p06.png：Bruno 躺下拍肚子 → p06b.png：皮皮把星星放到他肚子上 → p06c.png：肚子一弹，星星往旁边飞 → p06d.png：砸到 Bruno 鼻子（硬切） | **bruno**：`Bounce on my tummy!`<br>在我肚子上弹！<br>**all**：`One, two, three... UP!`<br>一、二、三……上！<br>**bruno**：`Ouch! My nose!`<br>哎哟！我的鼻子！ | 弹的那下一个 boing 音效 |
| p07 | p07.png：再弹一次，星星笔直冲上去 → p07b.png：远景，拖着光尾巴飞向天上的空缺 → p07d.png：Bruno 坐起来张开手，两人跑过去 → p07c.png：回到天上，三个欢呼抱在一起 | **all**：`UP, UP, UP!`<br>上，上，上！ | 一个比一个高，钢片琴上行刮奏 |
| p08 | p08.png：皮皮朝天上挥手 → p08b.png：特写，天上的小星星冲他眨眼 | **pip**：`Good night, little star!`<br>晚安，小星星！ | 放慢、变轻 |
| p09 | p09.png：彩蛋：Bruno 揉鼻子，鼻尖的小包变成金色发光的小星星，Bun 指着笑 → p09b.png：Bruno 斗鸡眼看自己的鼻子，得意地指着 | **bruno**：`My nose is a star!`<br>我的鼻子变成星星啦！ | 一个滑稽的叮 |

片尾复习卡：star 星星 · up 上 · good night 晚安，伴奏上轻声唱最后一句 *Twinkle, twinkle, little star*（复习页没有台词，不抢）。

**时长**：目标 45 秒（qa 卡 43–47）。台词 13 句约 45 词 + 8 秒演唱；超了先砍各页 hold 和片尾，不砍 p04b、p07 的跟唱跟喊停顿。

**换图节奏**：32 张图（补了 p05e、p05f、p03d、p07d 四张过渡帧），按每 1.3–1.8 秒一张排匀；同一页的关键帧角色位置锁住只改动作；不连着半秒内切两张，也不 3 秒以上不换图或不动镜头；片尾复习页也要缓慢运镜。

**音乐**：乐器版（八音盒 + 钢片琴 + 竖琴，本机合成原旋律）全片一个固定电平，台词时不压、不开关；演唱人声沿用第一版修到原调的 v3 人声，只取第一、二句放在 p05，最后一句放在片尾。OOPS（p02 Oops）和砸鼻子不停音乐，只加音效。

## 3. 出图提示词

> 画风是系列默认的日系手绘简洁版（夜景调色）。小星星是道具角色，每次都写全外形。主图写 `**p01.png**`，关键帧写 `**p01b.png** ← p01.png`，只写要改什么。

- **钩子首帧出图提示词**：
  ```
  a quiet forest clearing at night under a deep calm navy-blue sky with a few soft small stars, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[pip]] sits up on a small bed of leaves in the middle of the clearing, eyes wide, pointing up as a little golden star streaks down across the night sky with a soft sparkly trail, falling toward the leaf heap, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
  ```

**h02.png** ← kling_first.png
```
the little golden star lands in the big leaf heap with a soft puff of golden sparkles, the mouse jumps up in surprise with both hands on his cheeks
```

**h03.png** ← kling_first.png
```
the mouse kneels at the leaf heap and gently lifts out the little fallen star (a small golden five-pointed star about the size of the mouse's head, with two tiny round black eyes and a small mouth), but its gold has faded to a dull pale yellow with almost no glow around it, clearly much dimmer than when it fell, and it looks sad
```

**p01.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with a few soft small stars, soft silver moonlight, one big round soft heap of fallen leaves on the right; close-up: [[pip]] holds the little fallen star (a small golden five-pointed star about the size of the mouse's head, with two tiny round black eyes and a small mouth) gently in his two cupped hands, the star has faded to a dull pale yellow with no bright glow and no rays, it looks sad, a tiny tear in its eye, the mouse looks at it with worried big eyes, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p01b.png** ← p01.png
```
the little star keeps exactly the same five-pointed shape and the same dull pale yellow, it tilts and looks up toward the sky with its small eyes, and the mouse looks up at the sky too, where there is one small empty dark gap among the stars
```

**p02.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with a few soft small stars, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bruno]] stands proudly next to [[pip]], the mouse's hands are empty, and the bear alone holds the little fallen star (a small golden five-pointed star about the size of the mouse's head, with two tiny round black eyes and a small mouth) up high in one big paw above his head ready to throw, the star is a dull faded yellow with no glow, chest puffed, a confident grin, sizes: the bear is about three times as tall as the mouse, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p02b.png** ← p02.png
```
the bear throws the dull faded little star straight up with all his might, the star rises only a little above his head, both of them look up hopefully
```

**p02c.png** ← p02.png
```
the little star, duller and dimmer now, drops back down and bonks softly into the bear's paws, the bear fumbles it with an embarrassed 'oops' face, the mouse covers his mouth
```

**p03.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with a few soft small stars, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bun]] hops in and holds the little fallen star (a small golden five-pointed star about the size of the mouse's head, with two tiny round black eyes and a small mouth) close to her chest in both paws, she squats down very low on the grass with both knees deeply bent, about to spring up, the star is now a very dim brownish yellow with no glow at all, [[bruno]] and [[pip]] watch, sizes: the bear about twice as tall as the bunny, the mouse about two thirds of the bunny's height, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p03b.png** ← p03.png
```
the bunny jumps up high with the very dim brownish yellow little star raised over her head, ears flying, the star still far from the sky
```

**p03c.png** ← p03.png
```
the bunny has landed, the little star in her paws has gone almost completely dark and grey, flickering weakly, all three lean in close with worried faces
```

**p03d.png** ← p03b.png
```
same shot, the bear and the mouse stay exactly where they are: the bunny has just landed on the grass at the same spot, knees bent, she lowers the very dim little star to her chest and looks down at it, ears flopping forward
```

**p04.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with a few soft small stars, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bun]] sits with [[bruno]] and [[pip]] around the little fallen star (a small golden five-pointed star about the size of the mouse's head, with two tiny round black eyes and a small mouth), it has gone almost completely dark, a flat dull grey star with no glow and no light on the ground around it, its eyes closed, which is almost dark; suddenly one of the bunny's long ears springs straight up and she raises one finger with a bright clever smile, sizes: the bear about twice as tall as the bunny, the mouse about two thirds of the bunny's height, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p04b.png** ← p04.png
```
the bunny turns to face the viewer and looks straight into the camera with an inviting smile, one paw beckoning, the other paw on her chest like she is about to sing, the little star stays flat dull grey and dark with no glow
```

**p05.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with a few soft small stars, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bruno]], [[bun]] and [[pip]] sit in a little circle around the little fallen star (a small golden five-pointed star about the size of the mouse's head, with two tiny round black eyes and a small mouth), it has gone almost completely dark, a flat dull grey star with no glow and no light on the ground around it, its eyes closed, resting on a leaf on the grass, swaying gently and singing softly to it with their eyes half closed, little music notes in the air, sizes: the bear about twice as tall as the bunny, the mouse about two thirds of the bunny's height, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p05b.png** ← p05.png
```
the little grey star begins to change: it turns a pale faint yellow with only a very soft small glow and opens its eyes, nothing else moves, the three keep singing
```

**p05c.png** ← p05.png
```
the little star glows bright golden now and smiles, its warm light shining on the three happy singing faces
```

**p05d.png** ← p05.png
```
the little star shines so brightly that it lights up the whole clearing in warm gold, it floats a little above the leaf, the three cheer with arms up
```

**p05e.png** ← p05b.png
```
same shot, nothing moves except: the three lean a little the other way as they sway and sing with mouths open, the little star is now a clear warm yellow with a small soft glow
```

**p05f.png** ← p05c.png
```
same shot, nothing moves except: the three sing louder with big happy mouths, the little star glows even brighter and lifts just off the leaf
```

**p06.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with a few soft small stars, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bruno]] lies flat on his back on the grass and pats his big round soft tummy with both paws, grinning, [[pip]] stands beside him holding the bright glowing little star, [[bun]] watches, sizes: the bear about twice as tall as the bunny, the mouse about two thirds of the bunny's height, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p06b.png** ← p06.png
```
the mouse places the bright little star on top of the bear's round tummy, the bunny counts on her fingers
```

**p06c.png** ← p06.png
```
the bear bounces his tummy like a trampoline, the tummy squishes down and the little star bounces up but sideways, all three eyes follow it
```

**p06d.png** ← p06.png
```
the little star has come down and bonked right onto the bear's nose, the bear's eyes cross looking at it, the bunny and the mouse gasp and giggle
```

**p07.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with a few soft small stars, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bruno]] lies on his back and bounces his round tummy with a big boing, the bright little star shoots straight up high from his tummy with a golden sparkly trail, [[bun]] and [[pip]] jump with arms up, sizes: the bear about twice as tall as the bunny, the mouse about two thirds of the bunny's height, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p07b.png** ← p07.png
```
wide shot: the little star zooms high up into the night sky with a long sparkly trail toward the small empty gap among the stars, the three tiny below look up
```

**p07c.png** ← p07.png
```
the little star has reached its place in the sky and shines among the other stars, the three below cheer and hug, warm happy faces
```

**p07d.png** ← p07b.png
```
same shot, the long sparkly trail fades high in the sky: the bear sits up on the grass with both arms opening wide and laughing, the bunny and the mouse land and run toward him with their arms out
```

**p08.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with a few soft small stars, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[pip]] stands on the grass looking up at the night sky and waves goodbye with one tiny hand, a sleepy happy smile, high above the little golden star shines in its place, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p08b.png**
```
close-up of the night sky: the little golden five-pointed star about half the image width, with two round black eyes and a small smiling mouth, shines in the upper part of the image among a few soft small stars, it winks one eye happily, one eye is a closed happy arc, soft sparkle rays around it, the lower 40% of the image is plain deep navy sky fading into soft dark treetops, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16
```

**p09.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with a few soft small stars, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bruno]] sits up on the grass rubbing his nose, and the tip of his nose has turned into a tiny bright golden five-pointed star shape, clearly star-shaped and glowing, [[bun]] points at it laughing, sizes: the bear about twice as tall as the bunny, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p09b.png** ← p09.png
```
the bear crosses his eyes to look at the tiny golden five-pointed star on the tip of his nose and grins proudly, pointing at it with both paws, the bunny laughs with her paws on her cheeks
```

## 4. 发布文案（草稿，成片后定）

- **抖音标题**：小星星掉下来了｜英文儿歌
- **小红书标题**：小星星英文版｜2岁英语启蒙
- **合集**：森林故事
- **封面**：p05c 或 p05d（三个围着发亮的小星星唱歌）
- **正文**：
```
⭐ 栗栗学英语｜小星星掉下来了 英文对话版
一颗小星星从天上掉下来，越来越暗，回不了家……大熊扔、小兔跳都送不上去，最后大家想了什么办法？宝宝一起唱 Twinkle, twinkle 了吗？

📖 今日单词：star 星星｜up 上｜good night 晚安
🎤 跟着唱 + 做动作：
Twinkle, twinkle, little star ✨ 两只小手一张一合
UP, UP, UP! 🙌 两只手往上举
Good night, little star 😴 睡前挥挥手

💡 大家一起，再难的事也能做到。

#英文绘本 #幼儿英语启蒙 #小星星 #英语启蒙 #睡前故事
```
- **置顶评论**：宝宝跟着唱 Twinkle, twinkle 了吗？今晚睡前一起说 Good night, little star！今日单词 star 星星｜up 上｜good night 晚安
- 发布时勾选"内容由 AI 生成"。
