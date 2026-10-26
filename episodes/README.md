# 剧集

每集一个目录：`<编号>-<英文slug>/`，里面放 `script.md`（剧本、出图提示词、可灵提示词、配音清单、发布文案）和 `story.json`（给 `sbv.py` 出片用）。
认知短片编号 `c01`、`c02`…；剧情片 `s01`…（已发布的第 1 集算 s01）。图片、视频素材放进同一目录，但不提交（见 `.gitignore`）。

## 首批 5 条认知短片（2026-10-24 写好）

| 编号 | 片名 | 主题 | 今日单词 | 建议 |
|---|---|---|---|---|
| [c01](c01-fruits/script.md) | Nutty's Fruit Basket 栗栗的水果篮 | 认水果 | apple, banana, orange | 第 1 周发 |
| [c02](c02-carrots/script.md) | Bun Counts Carrots 小兔数胡萝卜 | 数数 1–5 | carrot, three, five | 第 1 周发 |
| [c03](c03-colors/script.md) | Hazel's Colorful Spines 小刺猬的彩色背 | 认颜色 | red, yellow, blue | 第 1 周发 |
| [c04](c04-body/script.md) | Touch Your Nose! 栗栗摸一摸 | 身体部位 | head, nose, hands | 第 2 周 |
| [c05](c05-weather/script.md) | What's the Weather? 今天什么天气 | 天气 | sunny, rainy, windy | 第 2 周 |

## 森林故事（剧情片）

| 编号 | 片名 | 主题 | 今日单词 | 建议 |
|---|---|---|---|---|
| [s02](s02-help/script.md) | Help! Hazel's Red Ball 小刺猬的红皮球 | 一个词讲一个道理：help（遇到困难要开口） | help, push, ball | 10-26 写好，先拿它试跑全流程；写法依据见 `docs/benchmark-story-2026-10.md` |

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
