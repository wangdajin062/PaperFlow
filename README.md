# PaperFlow - 科研论文写作工作流编排引擎

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![CI](https://github.com/wangdajin062/PaperFlow/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Node](https://img.shields.io/badge/node-18+-green)
![Electron](https://img.shields.io/badge/electron-33-blueviolet)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

一个 Windows 桌面工具，通过可视化节点编辑器编排科研论文写作工作流，整合多模型 AI 并支持一键调用 VS Code。

## 功能

- **可视化工作流编辑**: 基于 ReactFlow 的拖拽式节点编辑器，支持 Prompt / Code / Output 三种节点
- **多模型整合**: 集成 Claude、GPT、Gemini、DeepSeek 四种 LLM 提供商
- **论文写作模板**: 内置 9 节点完整科研论文写作工作流模板（文献综述→提纲→代码→Method→Results→审阅→摘要）
- **拓扑排序执行**: 自动按依赖顺序执行工作流节点，支持变量插值 `{{node_id}}`
- **VS Code 集成**: 工作流中可直接打开 VS Code 编辑代码文件
- **工作流持久化**: SQLite 存储，支持保存/加载多个工作流
- **系统托盘**: 最小化到系统托盘，随时唤醒
- **Windows 安装包**: 提供 NSIS 安装程序，一键安装

## 快速开始

### 前置条件

- Python 3.11+
- Node.js 18+
- npm
- (可选) VS Code

### 安装

```bash
# 1. 后端
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Windows
pip install -r requirements.txt

# 2. 前端
cd ../frontend
npm install

# 3. Electron
cd ../electron
npm install
```

### 运行（开发模式）

终端 1 — 后端 API:
```bash
cd backend
source .venv/Scripts/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8765
```

终端 2 — 前端开发服务器:
```bash
cd frontend
npm run dev
```

终端 3 — Electron 桌面壳:
```bash
cd electron
npm run dev
```

浏览器访问 `http://localhost:5173` 即可使用 Web 版。

### 运行（生产模式）

```bash
cd frontend
npm run build
cd ../electron
npm start
```

### 构建 Windows 安装包

```bash
cd frontend
npm run build
cd ../electron
npm run dist:win
```

安装包输出至 `electron/release/PaperFlow-Setup-0.1.0.exe`

## 项目结构

```
paper-flow/
├── backend/                  # Python FastAPI 后端
│   ├── main.py              # FastAPI 入口，CORS，生命周期
│   ├── api/                 # REST API 路由
│   │   ├── workflows.py     # 工作流 CRUD
│   │   ├── execution.py     # 工作流执行
│   │   └── models.py        # 模型配置
│   ├── engine/              # 工作流执行引擎
│   │   ├── executor.py      # 拓扑排序执行器
│   │   ├── context.py       # 节点间数据传递
│   │   └── nodes.py         # Pydantic 模型
│   ├── providers/           # LLM 提供商适配
│   │   ├── base.py          # 抽象基类 + 工厂
│   │   ├── claude.py        # Anthropic Claude
│   │   ├── openai.py        # OpenAI GPT
│   │   ├── gemini.py        # Google Gemini
│   │   └── deepseek.py      # DeepSeek
│   ├── services/            # 外部服务
│   │   └── vscode.py        # VS Code 集成
│   ├── storage/             # 持久化层
│   │   └── db.py            # SQLite (aiosqlite)
│   ├── tests/               # pytest 测试 (31 项)
│   └── requirements.txt
├── frontend/                # React + ReactFlow 前端
│   ├── src/
│   │   ├── components/      # UI 组件
│   │   ├── nodes/           # 自定义 ReactFlow 节点
│   │   ├── templates/       # 工作流模板
│   │   └── utils/           # API 客户端
│   └── package.json
├── electron/                # Electron 桌面壳
│   ├── main.js             # 主进程 (后端管理、系统托盘、IPC)
│   ├── preload.js           # 预加载脚本
│   └── package.json         # electron-builder 配置
├── .github/workflows/       # CI/CD (lint + test on push)
└── scripts/                 # 构建脚本
```

## API 文档

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/workflows` | GET | 获取所有工作流 |
| `/api/workflows` | POST | 创建工作流 |
| `/api/workflows/{id}` | GET | 获取单个工作流 |
| `/api/workflows/{id}` | PUT | 更新工作流 |
| `/api/workflows/{id}` | DELETE | 删除工作流 |
| `/api/execution/run` | POST | 执行工作流 |
| `/api/execution/stop` | POST | 停止执行 |
| `/api/vscode/open` | POST | 在 VS Code 中打开文件 |

## 使用流程

1. **启动应用** — 开发模式启动后端 + 前端 + Electron
2. **拖拽节点** — 从左侧面板拖拽 Prompt / Code / Output 节点到画布
3. **配置节点** — 点击节点，在右侧面板配置提示词、模型、API Key、文件路径等
4. **连接节点** — 从节点输出点拖拽到另一个节点输入点，建立依赖关系
5. **执行工作流** — 点击"Run"，引擎按拓扑顺序自动执行
6. **查看结果** — 右侧面板显示每个节点的输出
7. **加载模板** — 点击"模板"按钮载入内置论文写作工作流

## 技术栈

| 层 | 技术 |
|------|------|
| 后端 | Python 3.14, FastAPI, aiosqlite, Uvicorn |
| LLM | Anthropic Claude, OpenAI GPT, Google Gemini, DeepSeek |
| 前端 | React 18, TypeScript, ReactFlow 11, Vite 6 |
| 桌面 | Electron 33, electron-builder 26, NSIS |
| 质量 | ruff, ESLint, Prettier, pytest |

## 开发

```bash
# 安装开发依赖
cd backend && pip install -r requirements-dev.txt

# 运行测试 (31 项)
cd backend && python -m pytest tests/ -v

# 代码检查
cd backend && ruff check
cd frontend && npx eslint src/ --ext .ts,.tsx

# 类型检查
cd frontend && npx tsc --noEmit
```
