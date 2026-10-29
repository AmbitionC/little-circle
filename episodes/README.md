# 剧集

每集一个目录：`<编号>-<英文slug>/`，里面放 `script.md`（剧本、出图提示词、可灵提示词、配音清单、发布文案）和 `story.json`（给 `sbv.py` 出片用）。
认知短片编号 `c01`、`c02`…；剧情片 `s01`…（已发布的第 1 集算 s01）。图片、视频素材放进同一目录，但不提交（见 `.gitignore`）。

## 首批 5 条认知小绘本（2026-10-24 初稿，10-26 按新标准重写）

| 编号 | 片名 | 主线 | 今日单词 | 建议 |
|---|---|---|---|---|
| [c01](c01-fruits/script.md) | Nutty Is Hungry 栗栗好饿呀 | 吃饱了要会说 I am full（顺带认水果、数 1–3） | hungry, full, apple | 第 1 周 |
| [c02](c02-carrots/script.md) | Where Is My Carrot? 小兔数胡萝卜 | 数 1–5，少了一根；想要先问 Can I have one? | carrot, five, four | 第 1 周 |
| [c03](c03-colors/script.md) | Hazel's Colorful Leaves 小刺猬的彩色背 | 落叶粘满刺猬背，认红黄橙 | red, yellow, leaf | 第 1 周 |
| [c04](c04-body/script.md) | Achoo! Cover Your Mouth! 栗栗打喷嚏 | 打喷嚏要捂嘴 | nose, mouth, sneeze | 第 2 周 |
| [c05](c05-weather/script.md) | Bun's Rainy Picnic 小兔的下雨野餐 | 野餐遇上雨，认晴天、下雨、刮风 | sunny, rainy, windy | 第 2 周 |

**统一格式（10-26 起）**：每集一个主题，一个主线词串成故事，或者讲一个道理，不做一页一问一答。可灵钩子 5 秒，第 1 帧就有给家长看的大字标题；接 8 页动态绘本，起承转合，每 2–3 页一个笑点；最后是 3.5 秒片尾。
台词按 2–3 岁写：全片 11–13 句，每句 3–5 个词，每页最多两句。互动长在剧情里，比如让宝宝替角色喊一句、找一找。完整版约 45 秒；`--max-pages 4` 出约 25 秒的推荐流精华版，停在悬念上。
依据见 `docs/benchmark-story-2026-10.md`。c01–c03 之前按旧剧本出过的图要重出：提示词改了，`codex_images.py` 会自动只重出改过的那几张。

## 森林故事（剧情片）

| 编号 | 片名 | 主题 | 今日单词 | 建议 |
|---|---|---|---|---|
| [s02](s02-help/script.md) | Help! Hazel's Red Ball 小刺猬的红皮球 | 一个词讲一个道理：help（遇到困难要开口） | help, push, ball | 10-27 成品做完、质检通过，只差可灵钩子（见 HANDOFF）；写法依据见 `docs/benchmark-story-2026-10.md` |

**统一格式**：可灵钩子 5 秒（第 1 帧就有给家长看的大字标题）→ 6 页动态绘本 → 片尾 3.5 秒。
前 5 页每页一个词：旁白提问，停 1 秒多让宝宝抢答，角色再说答案；第 6 页复习，并向屏幕前的宝宝提一个问题，方便评论区互动。
每句 3–8 个英文单词，每集重复同一个句型。完整版约 40 秒；`--max-pages 3` 出约 25 秒的推荐流精华版。

**第 2 周测"开头钩子"**：每份 `script.md` 第 2 节都写了一个备选标题。c04、c05 发的时候，一条用原标题（问题句），一条换成备选（动作画面），其他不变。

## 出片

在 `tools/storybook-video` 目录下：

```bash
python sbv.py ../../episodes/c01-fruits/story.json --out ../../out/c01                  # 完整版
python sbv.py ../../episodes/c01-fruits/story.json --out ../../out/c01 --max-pages 3    # 精华版
```

- `story.json` 的配音指向 `series/cast.json`（ElevenLabs）。**订阅前**想先看节奏，加 `--cast ../../series/cast_kokoro.json` 用离线音色出样片，样片不发布。
- 音效、音乐引用仓库根目录的 `assets/sfx/`、`assets/bgm/`。还没生成的话，先把 story.json 里的 `sfx` 和 `bgm` 删掉。
