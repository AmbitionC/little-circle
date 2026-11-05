# M03 · Twinkle, Twinkle, Little Star 小星星，摘星星（老儿歌对话版）

> 2026-11-05 用户说 m02 拔萝卜对话版「流量还可以」，要再找一首。候选和播放依据见共享文件夹 `little-circle/song-topics-2026-11.md`，用户在卡片上选了**小星星**（B 站头部单集 222 万）。
> 模式同 m02 对话版：背景音乐是英文演唱版（用户 11-05 改），角色用简短英文对话讲故事，目标 45 秒。
> 版权：旋律是 18 世纪法国民歌 *Ah! vous dirai-je, maman*，英文词是 Jane Taylor 1806 年的诗，都是公有领域；我们不用任何频道的编曲和录音，伴奏本机自己合成。
> 实际做法：ElevenLabs Music 唱不出原调，取它生成的人声逐音节修到原谱，伴奏本机 SF2 合成。详见 HANDOFF.md。
> 画风：系列默认日系手绘简洁版（不是 m02 的国风特别版），夜景。

## 0. 人性 × 这一集怎么用

| 人性 | 这一集怎么用 | 拉动哪个数据 |
|---|---|---|
| 熟悉感 | 一开口就是家长哼了几十年的小星星旋律 | 2 秒跳出率 |
| 好奇 | 钩子大字「皮皮能摘到星星吗？」，答案到 p06 才揭晓 | 完播率、评论（猜答案） |
| 最小的赢（换个法） | 最大的 Bruno 举到踮脚也够不着，最后靠 Bun 的点子：星星装进了一桶水里 | 完播率、收藏 |
| 隔屏互动 | p03 Bun 转身对镜头："Can you reach up?" 宝宝跟着举手喊 Up | 家长拍娃晒、转发 |
| 彩蛋 | 皮皮睡着后 Bruno 把那桶水喝了，"Bruno! My STAR!"，抬头真星星还在 | 看到最后、评论 |
| 睡前场景 | 结尾皮皮说 Good night, star.，家长睡前可以反复放 | 收藏、重复播放 |

## 1. 概要

- **Logline**：皮皮睡不着，想要天上那颗最亮的星星。自己跳够不着；Bruno 把他举过头顶、踮脚也够不着，晃了几下三个人一起摔进软软的落叶堆。Bun 耳朵一竖想到办法，拎来一桶水，星星就"住"进了水桶里。皮皮抱着水桶说晚安。彩蛋：Bruno 把水喝了。
- **家长钩子**：皮皮能摘到星星吗？
- **今日单词**：star 星星 · up 上 · good night 晚安（全片 star ×5、up ×7、good night ×1，复习页再说一遍）
- **用了哪些手法**：三次阶梯（自己跳 → 被举高 → 再踮脚 → 摔倒）；反转（够不着的东西换个办法"拿到"）；角色口头禅（Bruno "I am big!"、Bun "I have an idea!"）；隔屏互动（p03）；彩蛋（p08）。
- **道理**：够不着的时候，换个办法想一想。
- **常理和安全**：不叠罗汉（孩子会学）；Bruno 只是把皮皮举过头顶，摔是往后倒进大落叶堆，落叶噗地扬起来，没人受伤；水桶是小木桶，水不洒；星星倒影要在桶正中、亮、有闪光。

## 2. 台词和音乐

| 页 | 画面 | 台词 | 音乐 |
|---|---|---|---|
| hook | kling_first.png：皮皮躺在叶子小床上，睁大眼看天上最亮的星星 → h02.png：坐起来指着星星 → h03.png：踮脚伸手，星星还远着 → h04.png：星星一闪，皮皮双手捧脸 | **pip**：`Look! A star!`<br>看！一颗星星！ | 八音盒单音起头 Twinkle 第一句 |
| p01 | p01.png：皮皮蹲下准备跳 → p01b.png：跳起来伸手 → p01c.png：一屁股坐地上，耳朵耷拉 → p01d.png：再跳一次，跳得更高 | **pip**：`I want it! Up! Up!`<br>我要它！上！上！ | 主旋律第 2 句，跳的两下各配一个上行小音 |
| p02 | p02.png：Bruno 拍肚子 → p02b.png：把皮皮举过头顶 → p02c.png：踮脚，脸憋圆，星星还是远 → p02d.png：仰拍皮皮只差指尖 → p02e.png：Bruno 开始晃 | **bruno**：`I am big! Up you go!`<br>我个子大！上去吧！<br>**pip**：`Up... up... too far!`<br>上……上……太远啦！ | 加低音和轻打击 |
| p03 | p03.png：Bun 蹦进来 → p03b.png：转身对镜头，两手高高举起 → p03c.png：踮脚蹦起来喊 UP | **bun**：`Can you reach up? Up, up, UP!`<br>你能够到吗？上，上，上！ | 三个 Up 一个比一个高，句后留 1.2 秒给宝宝跟喊 |
| p04 | p04.png：Bruno 踮脚晃 → p04d.png：往另一边歪 → p04b.png：三个往后倒进落叶堆 → p04e.png：叶子飘下来落在头上 → p04c.png：皮皮抱膝，难过 | **all**：`Whoa... whoa... OOPS!`<br>哎……哎……哎呀！<br>**pip**：`No star...`<br>没有星星了…… | Whoa 两下音乐跟着歪；OOPS 那一小节**伴奏停**；No star 只留八音盒一个长音 |
| p05 | p05.png：Bun 一只耳朵"叮"地竖起、竖手指 → p05b.png：拎着一小桶水跑回来 | **bun**：`I have an idea!`<br>我有个好主意！ | 叮一声，旋律回来 |
| p06 | p06.png：三个趴在桶边往里看 → p06b.png：正上方俯拍水桶，画面只有桶和星星倒影（硬切）→ p06d.png：一根小手指从桶沿伸进来点水，星星晃了 → p06e.png：水静下来，星星更亮 → p06c.png：皮皮抱着水桶，脸被映成金色 | **bun**：`Look!`<br>看！<br>**pip**：`My star! My little star!`<br>我的星星！我的小星星！ | 揭晓那一下钢片琴刮奏 + 风铃，接 Twinkle 副句最满的一段 |
| p07 | p07.png：皮皮挨着水桶睡着，Bruno 给他盖一片大叶子 → p07b.png：Bruno 和 Bun 手指放嘴边踮脚走开 | **pip**：`Good night, star.`<br>晚安，星星。 | 放慢、变轻，像摇篮曲 |
| p08 | p08.png：彩蛋：Bruno 回来捧起水桶咕咚咕咚喝 → p08d.png：Bruno 腮帮子鼓成球 → p08b.png：皮皮惊醒坐直，指着他（硬切）→ p08c.png：Bruno 鼓着腮帮子、下巴滴水，皮皮叉腰，天上真星星还在闪 | **sfx**：`Gulp, gulp!`<br>咕咚咕咚！<br>**pip**：`Bruno! My STAR!`<br>Bruno！我的星星！ | 喝水时音乐停，喊完一个滑稽低音 |

片尾复习卡：star 星星 · up 上 · good night 晚安（不说 Bye-bye），旋律最后一句收在主音上。

**时长**：用户 11-05 定 **45 秒**（qa 卡 43–47）。13 句、约 40 个词；超了先砍各页 hold 和片尾留白，不砍 p03 的跟喊停顿。

**关键帧**：用户 11-05 要求再补 10 张（24 → 34），按动作密度非线性加：钩子 +1、p01 跳 +1、p02 举高 +2、p03 跟喊 +1、p04 晃和摔 +2、p06 揭晓 +2、p08 喝水 +1；p05、p07 是平缓段不加。

**背景音乐**（用户 11-05：「背景音乐选英文版本的小星星」）：用 ElevenLabs Music 新生成一首英文演唱的 *Twinkle, Twinkle, Little Star*（Jane Taylor 1806 年原词，公有领域；不用任何频道的编曲和录音），八音盒 + 钢片琴伴奏、温暖女声轻唱，和台词一起排：有台词时压低，空档和片尾抬起来。OOPS 和喝水那两处照样停。

## 3. 出图提示词

> 画风是系列默认的日系手绘简洁版，夜景写在每页的场景里。主图写 `**p01.png**`，关键帧写 `**p01b.png** ← p01.png`，只写要改什么。

- **钩子首帧出图提示词**：
  ```
  a quiet forest clearing at night under a deep calm navy-blue sky with only a few soft small stars and one big bright golden five-pointed star high up in the top of the sky, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[pip]] lies on his back on a small soft bed of leaves in the middle of the clearing, wide awake, eyes sparkling as he looks up at the big golden star twinkling high above him, the star shines with little sparkle rays, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
  ```

**h02.png** ← kling_first.png
```
the mouse has sat up and points up at the big golden star with one tiny finger, mouth open in an excited 'o'
```

**h03.png** ← kling_first.png
```
the mouse stands up on his tiptoes and stretches both little arms up toward the star as high as he can, the star is still very very far above him
```

**h04.png** ← h03.png
```
the big golden five-pointed star above flashes brighter with a sparkle burst, the mouse's eyes reflect its light, he gasps with both hands on his cheeks
```

**p01.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with only a few soft small stars and one big bright golden five-pointed star high up in the top of the sky, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[pip]] crouches low in the middle of the clearing, knees bent, ready to jump, looking up at the big golden star with a determined face, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p01b.png** ← p01.png
```
the mouse jumps up as high as he can with both arms reaching up, a little jump, the star still far far above him
```

**p01c.png** ← p01.png
```
the mouse has landed on his bottom on the grass, ears drooping, looking up at the star with a little frown
```

**p01d.png** ← p01.png
```
the mouse jumps again even higher with all his might, legs tucked, both arms and fingers stretched up, his big ears flying up, the star still far above
```

**p02.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with only a few soft small stars and one big bright golden five-pointed star high up in the top of the sky, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bruno]] walks up next to [[pip]] and pats his own round tummy proudly with a big confident grin, chin up, the mouse looks up at him hopefully, sizes: the bear is about three times as tall as the mouse, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p02b.png** ← p02.png
```
the bear lifts the tiny mouse high up above his head with both paws, the mouse stretches both arms up toward the star
```

**p02c.png** ← p02.png
```
the bear stands on his tiptoes lifting the mouse as high as he can, the bear's cheeks puffed with effort, the mouse stretches up, the big golden star is still far far above them
```

**p02d.png** ← p02b.png
```
a completely new close-up camera angle from low down looking up: the tiny mouse fills the upper middle of the frame and stretches one arm up so hard that only his fingertips reach, tongue poking out in effort, the big golden star still far away above him in the night sky; his feet stand on the bear's two big furry paws, and the bear's two long furry arms run all the way down to the very bottom edge of the image, solid fur with no fade, filling the lower part of the frame
```

**p02e.png** ← p02c.png
```
the bear still holds the tiny mouse high above his head with both paws, exactly as before, but now he starts to wobble: he leans to one side with one foot lifting off the ground, little wobble lines, both of them with big surprised eyes, the mouse grabbing at the air
```

**p03.png** ← p02c.png
```
the bear keeps holding the tiny mouse high above his head with both paws, exactly as before, the mouse stays up there and does not come down; [[bun]] hops in from the left side next to the bear, turning to face the viewer, sizes: the bear about twice as tall as the bunny
```

**p03b.png** ← p03.png
```
the bunny stands facing the viewer and looks straight into the camera, stretching both of her arms straight up high with an eager encouraging face, inviting the viewer to reach up too; behind her the bear keeps holding the mouse high above his head, unchanged
```

**p03c.png** ← p03b.png
```
the bunny now jumps up on her tiptoes facing the viewer, both arms stretched as high as they go, mouth wide open shouting, ears straight up, full of energy; the bear keeps holding the mouse high above his head, unchanged
```

**p04.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with only a few soft small stars and one big bright golden five-pointed star high up in the top of the sky, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bruno]] wobbles on his tiptoes holding [[pip]] high above his head, leaning to one side, both of them with big worried eyes, [[bun]] beside them with her paws up in alarm, little wobble lines, sizes: the bear about twice as tall as the bunny, the mouse about two thirds of the bunny's height, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p04b.png** ← p04.png
```
all three tumble backward into the big soft heap of fallen leaves, leaves puffing up softly around them, surprised funny faces, nobody hurt
```

**p04c.png** ← p04.png
```
the three sit in the soft leaf heap with leaves on their heads, the tiny mouse hugs his knees and looks up at the far star, sad, his big ears drooping
```

**p04d.png** ← p04.png
```
the bear tips the other way now, one foot in the air, still firmly gripping the mouse in both paws high above his head, the mouse is not thrown and stays in the bear's paws, flailing his little arms, the bunny reaching out to help
```

**p04e.png** ← p04b.png
```
the three lie in the soft leaf heap as the puffed-up leaves float gently down onto their heads and noses, they blink, dazed and a little funny
```

**p05.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with only a few soft small stars and one big bright golden five-pointed star high up in the top of the sky, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bun]] sits in the soft leaf heap next to [[bruno]] and [[pip]]; suddenly one of the bunny's long ears springs straight up with a little 'ping' and she raises one finger with a bright clever smile, sizes: the bear about twice as tall as the bunny, the mouse about two thirds of the bunny's height, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p05b.png** ← p05.png
```
the bunny hops back fast carrying a small round wooden bucket about as tall as the bunny's knees, full of still water with both paws, careful not to spill, the bear and the mouse watch her, curious
```

**p06.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with only a few soft small stars and one big bright golden five-pointed star high up in the top of the sky, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[bruno]], [[bun]] and [[pip]] lean over a small round wooden bucket about as tall as the bunny's knees, full of still water on the grass and peek into it, sizes: the bear about twice as tall as the bunny, the mouse about two thirds of the bunny's height, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p06b.png**
```
a shot taken from directly overhead, camera pointing straight down at the ground: we look straight down into a small round wooden bucket full of still dark night-blue water, the bucket's rim is a perfect circle, seen from exactly above so no outside wall of the bucket is visible, the circle is about 85 percent of the image width and its center is 38 percent down from the top of the image, the big bright golden five-pointed star shines exactly in the center of the water as a twinkling reflection with soft sparkle rays, around the bucket only soft dark grass, the lower 35 percent of the image is plain soft dark grass with nothing on it, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, no characters at all, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16
```

**p06c.png** ← p06.png
```
the tiny mouse hugs the side of the bucket with both arms, his face lit warm gold by the star in the water, a huge happy smile, the bear and the bunny smile at him
```

**p06d.png** ← p06b.png
```
keep the same overhead view and the same bucket: one tiny pink finger reaches in from the top edge of the rim and gently pokes the water, little round ripples spread and the star reflection wobbles
```

**p06e.png** ← p06b.png
```
keep the same overhead view and the same bucket: the water is calm again, the star reflection shines even brighter and perfectly still in the center, with a soft sparkle burst
```

**p07.png**
```
a quiet forest clearing at night under a deep calm navy-blue sky with only a few soft small stars and one big bright golden five-pointed star high up in the top of the sky, soft silver moonlight, one big round soft heap of fallen leaves on the right; [[pip]] sleeps curled up on the grass in the middle of the clearing, next to the small wooden bucket with the star shining in its water, one hand on the bucket, a peaceful smile; one single big soft leaf lies on top of him like a blanket, covering his whole body from his shoulders to his toes, only his head and the hand on the bucket stick out; [[bruno]] kneels behind him gently patting the leaf blanket, [[bun]] watches sweetly, sizes: the bear about twice as tall as the bunny, the mouse about two thirds of the bunny's height, Japanese hand-painted 2D animation film style, clean cel-shaded characters with soft outlines, big expressive eyes, cute rounded proportions, simple calm background painted with a few big soft shapes of trees and a deep blue night sky with a few soft stars, plenty of open empty space, no small scattered details like flowers, mushrooms, pebbles or falling leaves unless the prompt names them, gentle warm light, a limited harmonious palette of soft night blues, warm lamp yellow and cream, the characters brighter and sharper than the background, background softer and lower in contrast, only the characters named in the prompt and no extra animals, one clear focal point, clean uncluttered picture-book composition, no text, no watermark, vertical 9:16, keep every face in the upper 55% of the image and the lower 40% simple open ground
```

**p07b.png** ← p07.png
```
the bear and the bunny are now walking away on tiptoe toward the left edge, mid-step, each with one finger on the lips, looking back; the sleeping mouse under the leaf blanket and the shining bucket stay exactly as they are; the star high in the sky twinkles softly
```

**p08.png** ← p07.png
```
the bunny is gone. the bear has come back alone and stands up behind the sleeping mouse, he holds the same small wooden bucket in both paws, tipped up to his mouth, drinking it thirstily, gulp, eyes closed, the bucket is the same size as before and no longer on the ground; the mouse stays exactly where he was, asleep on the grass under the same big leaf blanket
```

**p08b.png** ← p08.png
```
the tiny mouse has woken up and sits bolt upright on the grass with the leaf blanket slipping down to his lap, eyes huge, pointing up at the bear with one arm; the bear freezes with the bucket still at his mouth
```

**p08d.png** ← p08.png
```
the bear's cheeks now bulge round and full of water, eyes squeezed shut, the bucket tipped to his mouth with a little splash at the rim; the mouse stays asleep under the leaf blanket, unchanged
```

**p08c.png** ← p08.png
```
the bear lowers the empty bucket with puffed-out cheeks still full of water and a guilty sheepish face, water dripping down his chin, the tiny mouse stands on the grass with fists on his hips and the leaf blanket on the ground beside him, high above them the big golden star still twinkles in the sky
```

## 4. 发布文案（草稿，成片后定）

- **抖音标题**：小星星英文版｜star和up
- **小红书标题**：小星星英文故事｜2岁英语启蒙
- **合集**：森林故事
- **封面**：p06c（皮皮抱着发光的水桶）
- **正文**：
```
⭐ 栗栗学英语｜小星星英文对话版
皮皮想摘天上的星星，跳也够不着，大熊举高高也够不着……最后星星居然被装进了水桶里？宝宝猜到了吗？

📖 今日单词：star 星星｜up 上｜good night 晚安
🎤 跟着喊 + 做动作：
Up! Up! 🙌 两只手往上伸，踮起脚
Good night, star. 😴 睡前和宝宝一起说

💡 够不着的时候，换个办法想一想。

#英文绘本 #幼儿英语启蒙 #小星星 #英语启蒙 #睡前故事
```
- **置顶评论**：宝宝跟着喊 Up 了吗？今晚睡前一起说 Good night, star！今日单词 star 星星｜up 上｜good night 晚安
- 发布时勾选"内容由 AI 生成"。
