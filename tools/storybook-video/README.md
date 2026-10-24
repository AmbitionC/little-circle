# 动态绘本视频生成器（sbv.py）

把**一个 5 秒可灵钩子镜头 + 一组绘本分镜图 + 剧本**，自动做成一条竖版成片：

```
[可选 0.4 秒封面帧] → 可灵钩子镜头（叠给家长看的大字标题）
→ 每页绘本：静态图缓慢推拉平移 + 漂浮光点 + 角色配音 + 逐词高亮的中英字幕
→ 片尾卡（最后 0.6 秒淡出）
```

同时输出：
- `xxx.mp4`：1080×1920、30fps、H.264，音频做 -16 LUFS 响度标准化；
- `xxx.srt`：中英字幕文件，可选用；
- `xxx_print.pdf`：A4 打印版绘本（封面 + 每页一图一文）。

加 `--max-pages N` 会再出一条推荐流精华版：只取前 N 页，片尾改成"完整版在主页合集"。

默认样式就是"森林小伙伴英语"系列规范（Fredoka + 思源黑体、角色字幕配色、奶油色字幕卡、0.35 秒叠化），
都可以在 `story.json` 的 `style` 里逐项改。

---

## 1. 安装（Mac）

```bash
brew install ffmpeg                      # 需要带 rubberband 和 loudnorm：ffmpeg -filters | grep -E "rubberband|loudnorm"
python3 -m venv .venv && source .venv/bin/activate
pip install pillow numpy kokoro-onnx soundfile

# Kokoro 配音模型（约 350MB，Apache-2.0，可商用）
mkdir -p models
curl -L -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o models/voices-v1.0.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

# 字体（OFL 开源字体，可商用）
mkdir -p fonts
curl -L -o fonts/Fredoka.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/fredoka/Fredoka%5Bwdth,wght%5D.ttf"
# 中文：装思源黑体 / Noto Sans CJK SC，再把 style.fonts.zh.path 指过去（.ttc 简体是 index 2）
```

## 2. 准备素材（一个文件夹一集）

| 文件 | 要求 |
|---|---|
| `kling01.mp4` | 可灵图生视频，**5 秒、9:16、1080p、不开原生音频**（原生音频贵 50%，配音由脚本做）。建议用**首尾帧**：首帧放最抓人的画面，尾帧放第 1 页绘本图，钩子结束时正好落在第 1 页，衔接最顺。 |
| `p01.png …` | 每页一张分镜图，9:16、至少 1080×1920。**下方四分之一留给字幕**，角色的脸放在 y<1450。横图也能用，会自动放在上半部、背景用同图模糊铺满。 |
| `bgm.wav`（可选） | 背景音乐，有人说话时自动压到一半。 |
| `sfx/*.wav`（可选） | 音效，按页内时间点放。 |

## 3. 写 story.json

参考 `example/story.json`。`example/story_live_scene.json` 是单张图加立体运镜和特效的示例；它用到的 `scene.png`、`bgm.wav` 没有放进仓库，换成你自己的图，或用 `python make_bgm.py bgm.wav 16` 生成背景音乐。最常改的字段：

```jsonc
{
  "output_name": "ep02_xxx",
  "hook": {
    "clip": "kling01.mp4",
    "headline": "孩子不肯分享？今晚讲这个",      // 写给家长看的一句话，第 1 帧就完整显示
    "subline": "3岁英语启蒙 · 中英字幕",
    "say": {"speaker": "narrator", "en": "What did Nutty find?", "at": 0.6}
  },
  "pages": [
    {"image": "p01.png", "motion": "in", "focus": [0.6, 0.65],   // 运镜：in / out / left / right / up / down
     "lines": [
       {"speaker": "narrator", "en": "Nutty finds a big, big acorn.", "zh": "Nutty 捡到一颗大大的橡果。"},
       {"speaker": "nutty", "en": "Wow! Look at this big, big acorn!", "zh": "哇！快看这颗大大的橡果！", "gap": 0.5}
     ],
     "sfx": [{"file": "sfx/pop.wav", "at": 1.2, "gain": 0.55}]}
  ],
  "ending": {"image": "endcard.png", "seconds": 3.5}            // 系列 make_end_card 出的图；不给就用最后一页生成
}
```

其他可选：
- `cover`：`{"image": "cover.png", "seconds": 0.4}`，在钩子前放 0.4 秒静止封面帧。
- 每页的 `cut: true`：冲击镜头用硬切，不叠化。
- 每页的 `hold`：说完后多停几秒。
- 每页的 `zoom`：推拉幅度，默认 1.12。
- 每句的 `audio`：直接用你录好的音频（比如 ElevenLabs 导出的），不走合成。
- 每句的 `say`：给配音用的文本，可以带 v3 语气标签，例如 `[excited] Wow!`；字幕仍然显示 `en`。
- 每句的 `take`：想重录某一句时改成 2、3……，只重新生成这一句。
- `cast` 可以写成路径字符串，例如 `"cast": "../../series/cast.json"`，整个系列共用一份角色音色表。

### 立体运镜与画面特效（可选，按页开启）

```jsonc
{"image": "p07.png", "motion": "in", "focus": [0.5, 0.55], "zoom": 1.13,
 "parallax": {"amount": 0.035, "dir": [1, 0.2], "dolly": 0.08},   // 按深度做 2.5D 视差：近景动得多、远景动得少
 "fx": [
   {"type": "glow",  "x": 0.395, "y": 0.505, "r": 0.11},                 // 烛光/灯光跳动，坐标是占原图宽高的比例
   {"type": "snow",  "ellipse": [0.2125, 0.272, 0.1435, 0.0957], "n": 110}, // 窗外飘雪：椭圆 [中心x, 中心y, 半宽, 半高]，只下在玻璃上
   {"type": "motes", "x": 0.42, "y": 0.47, "r": 0.28, "n": 20}             // 暖光里漂浮的光尘
 ]}
```

- 视差需要额外装 `pip install onnxruntime opencv-python-headless`，并下载深度模型
  （Depth Anything V2 Small，约 100MB）：
  `curl -L -o models/depth/model.onnx https://huggingface.co/onnx-community/depth-anything-v2-small/resolve/main/onnx/model.onnx`，
  运行时设 `DEPTH_MODEL=models/depth/model.onnx`。每张图的深度只算一次，会缓存。
- 特效坐标要按每张图标注（蜡烛在哪、窗户在哪）。让 Claude 看图写 story.json 时一起给出即可。
- `style.subtitles: false` 可以出一版不带字幕的纯画面。

## 4. 运行

```bash
export KOKORO_MODELS=$PWD/models
python sbv.py episodes/ep02/story.json --out episodes/ep02/out                 # 完整版
python sbv.py episodes/ep02/story.json --out episodes/ep02/out --max-pages 3   # 推荐流精华版
```

- 4 核 CPU 上，渲染耗时约等于视频时长的 2 倍（30 秒片子约 1 分钟）。
- 配音按"文本 + 音色"缓存在 `out/.cache`，改剧本只会重配改过的句子。

## 5. 配音选项（cast 里每个角色单独设）

| provider | 说明 |
|---|---|
| `kokoro` | 离线、免费、可商用。`voice` / `speed` / `pitch`（rubberband 变调，共振峰一起变，更像小孩）。没有词级时间戳，高亮按语音能量 + 字长估算，3–8 词的短句足够准。 |
| `elevenlabs` | 设环境变量 `ELEVENLABS_API_KEY`，`voice` 填 voice_id，`settings` 对应 ElevenLabs 的音色参数。优先用带时间戳的接口，高亮最准；如果某个模型不支持时间戳，会自动退回普通接口，高亮改为估算。完整流程见 [docs/elevenlabs-workflow.md](../../docs/elevenlabs-workflow.md)。**这段代码还没用真实 key 测试过，第一次用请先跑一句。** |
| `edge` | 免费、带词级时间戳，但是非官方接口，**只用来做样片，不要用于发布**。 |

ElevenLabs 的一次性准备（选角候选、保存音色、音效库、背景音乐）用 `el_prep.py`，只依赖标准库，在仓库根目录运行：

```bash
python3 tools/storybook-video/el_prep.py all                     # 候选音色 → out/casting/，音效 → assets/sfx/，音乐 → assets/bgm/
python3 tools/storybook-video/el_prep.py pick narrator=2 nutty=1 hazel=3 bun=2   # 存下选中的候选，写进 series/cast.json
```

生成的音频只留在本机，不提交（仓库是公开的）。

## 6. 发布前自查

1. 第 1 帧是带大字标题的钩子画面，不是黑场。
2. 在抖音的发布预览里看一下：字幕卡有没有被底部的作者名、文案挡住。挡住就把 `style.subtitle_center` 从 1640 往上调（比如 1450）。
3. 勾选"内容由 AI 生成"声明。
4. 封面可以在发布页手动选帧或上传，不必靠视频第一帧。

## 已知限制

- 画面只有镜头运动和光点，角色本身不会动。需要动作的镜头，用可灵单独出 5 秒片段，再作为一页的视频素材插进去（这是下一步可以加的功能）。
- Kokoro 的高亮时间是估算的，长句、语速变化大的句子可能差零点几秒。
