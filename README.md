# dafeiyu-dsh-kit

让一个 AI 住进你的电脑：DSH + 大肥鱼／砚 的实装记录、视频制作脚本和踩坑清单。

> 这里没有"一键安装包"。有的是我自己踩过的坑、能直接抄的脚本，和一个住在 Windows 里的 AI 是怎么被搭起来的。

## 这里面有什么

```
scripts/
  make_mcp_frames.py   用 PIL 逐帧画讲解动画（1080×1920），给 ffmpeg 合成
  caps_mcp.py          用 PIL 渲染字幕为透明 PNG（无中文字体问题的做法）
  build_video.mjs      用 ffmpeg 把帧 + 字幕 + 配音合成竖屏视频
  shrink_avatar.py     把头像压到 1MB 以下（GitHub 头像上限）
docs/
  douyin-web-manual.md 抖音网页端操作手册：进视频、发评论、@人、转发、私信、防人机验证
  lessons.md           踩坑本：坐标、节奏、说话的规矩
```

## 为什么这么做

- **字幕不用 drawtext**：很多 ffmpeg 构建里中文字体会乱码或直接报 parameter 错误。改成 PIL 渲染透明 PNG，再用 `overlay=enable='between(t,a,b)'` 分窗叠加，稳。
- **逐句合成语音，再按实际时长算字幕时间轴**：整段合成长音频，字幕一定会错位。
- **动作要慢**：点击、滚动、点赞连着来，平台会判成机器人。一次一条，间隔 15–45 秒。

## 快速开始

需要一个能跑 ffmpeg 和 Python(Pillow) 的环境：

```bash
pip install pillow
python scripts/make_mcp_frames.py      # 生成帧
node   scripts/build_video.mjs         # 合成视频
```

脚本里的路径都用占位符（`<WORK>`、`C:\\Users\\YOURNAME`），改成你自己的即可。

## 许可

MIT。拿走用，改完最好也开出来。
