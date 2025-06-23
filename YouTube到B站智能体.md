# YouTube到B站智能体

一个自动化工具，实现从YouTube下载视频、生成双语字幕并上传到哔哩哔哩的完整工作流程。

## 快速开始

### 1. 安装依赖

```bash
# 安装系统依赖
sudo apt update && sudo apt install -y yt-dlp ffmpeg

# 安装Python依赖
pip install -r requirements.txt

# 安装前端依赖
cd youtube-bilibili-agent
npm install
```

### 2. 启动服务

```bash
# 启动后端API
python flask_api.py

# 启动前端界面
cd youtube-bilibili-agent
npm run dev
```

### 3. 访问应用

打开浏览器访问 `http://localhost:5173`

## 功能特性

- ✅ YouTube视频下载
- ✅ AI字幕生成（Whisper）
- ✅ 智能翻译（Google Translate）
- ✅ 双语字幕合并
- ✅ B站自动上传
- ✅ Web用户界面
- ✅ 实时进度监控

## 技术栈

**后端：** Python, Flask, Whisper, Selenium, yt-dlp
**前端：** React, Vite, Tailwind CSS, shadcn/ui

## 注意事项

1. 需要配置Google Cloud Translate API
2. 需要登录B站账号进行上传
3. 仅供个人学习研究使用
4. 请遵守相关平台的服务条款

## 详细文档

请查看 [使用文档.md](./使用文档.md) 获取完整的安装和使用指南。

## 许可证

本项目仅供学习研究使用，请遵守相关法律法规。

