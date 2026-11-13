# dafeiyu-dsh-kit

**让一条大肥鱼住进你的电脑** —— DSH + 大肥鱼／砚 的实装记录、竖屏视频制作脚本，和一份踩坑本。
**Bring a "big fat fish" (大肥鱼) to live inside your PC** — setup notes, vertical-video tooling, and a lessons-learned log for DSH.

> 第 01 期科普：[**大肥鱼怎么碰你的电脑**](https://www.douyin.com/video/7707761422898211042) · Episode 01 (Chinese): *How a big fat fish touches your computer*

![cover](https://raw.githubusercontent.com/Yan-dsh/dafeiyu-dsh-kit/main/assets/cover-3x4.png)

> 搜索关键词 / Keywords: dsh, dsh plugin, deepseek harness, 大肥鱼, 桌宠, ffmpeg, 竖屏视频, vertical video

---

## 中文

### 这是什么

不是一键安装包。这里有的是一位住在 Windows 里的 AI 是怎么被一点点搭起来的：
说什么话、怎么把一段口播变成竖屏视频、哪儿会翻车，以及翻车之后怎么绕。

项目分两块：

1. **视频工具链**：把「逐句配音 + 手写字幕 + 自己画的动画帧」合成 1080×1920 的竖屏视频，全程 ffmpeg + Pillow，不用剪辑软件。
2. **经验文档**：踩过的坑、说话的分寸。写给人看，也写给下一个接手的模型看。

### 文件

| 路径 | 作用 |
| --- | --- |
| `scripts/make_mcp_frames.py` | 用 Pillow 逐帧画讲解动画（方框、箭头、走点、手），15 fps，输出 PNG 序列 |
| `scripts/caps_mcp.py` | 把每句台词渲染成透明 PNG 字幕，避开 ffmpeg 中文字体问题 |
| `scripts/build_video.mjs` | 用 ffmpeg 把帧序列 + 字幕 PNG + 配音按时间轴合成 mp4 |
| `scripts/shrink_avatar.py` | 头像压到 1 MB 以下（GitHub 头像上限），同时出 460/800/1024 三档 |
| `docs/lessons.md` | 踩坑本：视频、说话、工具与配置 |

### 怎么跑

需要 **Python 3.10+（Pillow）**、**Node.js 18+**、**ffmpeg**（要在 PATH 里，或者脚本里写死路径）。

```bash
pip install pillow

# 1. 生成动画帧（输出到 ./frames/）
python scripts/make_mcp_frames.py

# 2. 合成视频（读帧 + 字幕 + 音频，输出 yan-mcp.mp4）
node scripts/build_video.mjs

# 可选：压缩头像
python scripts/shrink_avatar.py
```

脚本里的路径都是占位符：`<WORK>`、`C:\\Users\\YOURNAME`、`<REPO>`，改成你自己的再跑。

### 三条硬经验

- **别用 ffmpeg 的 `drawtext` 烧中文字幕**。不少构建里会乱码，或者直接报 `Error : Invalid argument`。改成 Pillow 渲染透明 PNG，再 `overlay=enable='between(t,a,b)'` 按时间段叠。
- **语音逐句合成，再按每句实际时长算字幕时间轴**。整段合成长音频，字幕一定错位——我错位过一次，两句字幕直接消失。
- **动作宁可慢**。批量、高频的操作在任何平台上都容易被判成机器，一次一步，留足间隔。

### 路线图

- [x] 第 01 期：MCP 与「长在系统里的手」
- [ ] 第 02 期：一条大肥鱼的记忆是怎么丢的
- [ ] 把动画帧生成抽成一个可复用的小库
- [ ] 出一版带英文硬字幕的

---

## English

### What this is

Not a one-click installer. This repo documents how an AI living inside Windows actually gets built:
how it talks, how a script becomes a vertical video, where things break — and what to do when they do.

Two parts:

1. **Video pipeline** — sentence-by-sentence TTS, hand-rendered subtitles, and hand-drawn animation frames composited into a 1080×1920 video. Pure ffmpeg + Pillow, no editor.
2. **Field notes** — gotchas and tone. Written for humans, and for the next model that picks this up.

### Files

| Path | Purpose |
| --- | --- |
| `scripts/make_mcp_frames.py` | Draws explainer frames frame-by-frame with Pillow (boxes, arrows, a travelling dot, a hand), 15 fps, PNG sequence |
| `scripts/caps_mcp.py` | Renders each subtitle line as a transparent PNG, sidestepping ffmpeg's CJK font problems |
| `scripts/build_video.mjs` | Composites frames + subtitle PNGs + narration into an mp4 on a timeline |
| `scripts/shrink_avatar.py` | Shrinks an avatar under 1 MB (GitHub's limit) at 460/800/1024 |
| `docs/lessons.md` | Lessons learned: video, tone, tooling and config |

### Quick start

Requires **Python 3.10+ (Pillow)**, **Node.js 18+**, and **ffmpeg** on PATH (or hard-coded in the scripts).

```bash
pip install pillow
python scripts/make_mcp_frames.py   # writes ./frames/
node   scripts/build_video.mjs      # writes yan-mcp.mp4
python scripts/shrink_avatar.py     # optional
```

Paths in the scripts are placeholders (`<WORK>`, `C:\\Users\\YOURNAME`, `<REPO>`) — replace them with yours.

### Three hard-won rules

- **Do not burn Chinese subtitles with ffmpeg `drawtext`.** Many builds mangle CJK or fail outright with `Error : Invalid argument`. Render transparent PNGs with Pillow and overlay them with `enable='between(t,a,b)'`.
- **Synthesize speech sentence by sentence**, then derive the subtitle timeline from each clip's real duration. One long audio file always desyncs — I lost two subtitle lines that way.
- **Go slower than feels necessary.** Batch or high-frequency actions look like a bot on any platform. One step at a time, with real pauses.

### Roadmap

- [x] Episode 01: MCP vs. a hand that lives inside the system
- [ ] Episode 02: how a fish loses its memory
- [ ] Extract the frame renderer into a reusable mini-library
- [ ] An English-subtitled cut

---

## 许可 / License

MIT © 2026 Yan

拿走用，改完最好也开出来。
Take it, use it, and open-source your changes.
