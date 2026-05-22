# PaperFlow - 科研论文写作工作流编排引擎

![Version](https://img.shields.io/badge/version-0.1.0-blue)

一个 Windows 桌面工具，通过可视化节点编辑器编排科研论文写作工作流，整合多模型 AI 并支持一键调用 VS Code。

## 功能

- **可视化工作流编辑**: 基于 ReactFlow 的拖拽式节点编辑器
- **多模型整合**: 集成 Claude、GPT、Gemini、DeepSeek
- **论文写作模板**: 内置完整的科研论文写作工作流模板
- **VS Code 集成**: 工作流中可直接打开 VS Code 编辑代码
- **开机自启**: 注册为 Windows 自启动应用
- **系统托盘**: 最小化到系统托盘，随时唤醒

## 快速开始

### 前置条件

- Python 3.11+
- Node.js 18+
- npm

### 安装

```bash
# 1. 后端
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# 2. 前端
cd ../frontend
npm install

# 3. Electron
cd ../electron
npm install
```

### 运行

**开发模式:**

```bash
scripts\dev.bat
```

这会同时启动后端 (http://localhost:8765) 和前端开发服务器 (http://localhost:5173)。

**生产模式 (Electron):**

```bash
cd frontend
npm run build
cd ../electron
npm start
```

### 开机自启

```bash
cd backend
..\.venv\Scripts\python ..\scripts\register-startup.py
```

## 项目结构

```
paper-flow/
├── backend/     # Python FastAPI 后端
├── frontend/    # React + ReactFlow 前端
├── electron/    # Electron 桌面壳
└── scripts/     # 工具脚本
```

## 使用流程

1. 启动应用
2. 从左侧拖拽节点到画布（Prompt / Code / Output）
3. 配置每个节点（提示词、模型选择、文件路径）
4. 连接节点创建工作流
5. 点击"运行"执行整个工作流
6. 在右侧面板查看结果和对话记录
7. Code 节点可一键在 VS Code 中打开编辑
