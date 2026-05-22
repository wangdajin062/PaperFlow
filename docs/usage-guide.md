# PaperFlow 使用指南

## 界面概览

PaperFlow 启动后，主界面分为三个区域：

```
┌──────────────────────────────────────────────────┐
│  工具栏 (Toolbar)                                 │
│  [New] [Save] [Load] [Run] [Stop] [Templates]    │
├──────────┬───────────────────────────┬────────────┤
│          │                           │            │
│ 节点面板  │     工作流画布            │  配置面板   │
│ (Node     │     (ReactFlow)          │  (Node     │
│  Palette) │     拖拽、连接、编辑      │   Config)  │
│          │                           │            │
│ Prompt   │                           │  Provider  │
│ Code     │                           │  Model     │
│ Output   │                           │  Prompt    │
│          │                           │  /FilePath │
│          │                           │            │
└──────────┴───────────────────────────┴────────────┘
```

---

## 节点类型

有三种节点，分别对应工作流中的不同角色：

### 1. Prompt 节点

向 LLM 发送提示词并获取回复。

| 配置项 | 说明 |
|--------|------|
| Label | 节点显示名称 |
| Provider | LLM 提供商（Claude / GPT / Gemini / DeepSeek） |
| Model | 具体模型名 |
| Prompt | 发送给模型的提示词内容 |
| System Prompt | 系统提示词（设定角色和行为） |

提示词中可以用 `{{node_id}}` 引用前置节点的输出。引擎执行时会自动替换为实际内容。

**示例：**
```
请总结以下论文的核心贡献：
{{lit-review}}
```

### 2. Code 节点

表示要编写的代码文件。执行时会打开 VS Code 或标记为待编写。

| 配置项 | 说明 |
|--------|------|
| Label | 节点显示名称 |
| File Path | 代码文件保存路径 |
| Description | 代码任务描述 |

### 3. Output 节点

工作流的最终输出节点，汇总并展示结果。

| 配置项 | 说明 |
|--------|------|
| Label | 节点显示名称 |
| Format | 输出格式（markdown / text） |

### 4. Start 节点

每个工作流的起点，提供初始输入数据。

---

## 基本操作

### 创建工作流

1. **拖拽节点**：从左侧节点面板拖拽节点到画布
2. **配置节点**：点击节点，在右侧面板填写配置
3. **连接节点**：从节点右侧输出点拖拽到另一个节点左侧输入点
4. **保存工作流**：点击工具栏 Save 按钮

### 执行工作流

1. 点击 **Run** 按钮
2. 引擎按拓扑顺序自动执行：
   - 先执行没有依赖的节点
   - 前置节点完成后自动执行后续节点
3. 每个节点执行时会显示进度状态
4. 执行完成后，最终输出显示在 Output 节点

### 变量插值

在 Prompt 节点的提示词中使用 `{{node_id}}` 引用其他节点的输出：

```
提纲：
{{outline}}

代码：
{{code-exp}}
```

引擎会自动将 `{{outline}}` 替换为 `outline` 节点的输出内容。

### 加载模板

1. 点击工具栏 **Templates** 按钮
2. 选择预设模板（如"科研论文写作工作流"）
3. 模板会自动加载到画布

---

## 内置模板：科研论文写作工作流

这是系统内置的 9 节点模板，覆盖论文写作全流程：

```
Start → Literature Review → Outline → Experiments Code → Method Section
                                                          ↓
                                           Results & Discussion
                                                  ↓
                                          Review & Polish
                                                  ↓
                                          Abstract & Title
                                                  ↓
                                          Final Output
```

| 步骤 | 节点类型 | 说明 |
|------|----------|------|
| 1 | Start | 输入论文主题或相关文献 |
| 2 | Literature Review | Prompt 节点，生成文献综述 |
| 3 | Outline | Prompt 节点，生成论文提纲 |
| 4 | Experiments Code | Code 节点，打开 VS Code 编写实验代码 |
| 5 | Method Section | Prompt 节点，根据提纲+代码撰写 Method |
| 6 | Results & Discussion | Prompt 节点，撰写结果与讨论 |
| 7 | Review & Polish | Prompt 节点，审阅润色全文 |
| 8 | Abstract & Title | Prompt 节点，生成标题和摘要 |
| 9 | Final Output | Output 节点，输出最终论文 |

模板中节点间的变量插值关系：

```
outline → {{lit-review}}                 (提纲引用文献综述)
code-exp → {{outline}}                    (代码引用提纲)
method-writing → {{outline}} + {{code-exp}}  (Method 引用提纲+代码)
results-writing → {{method-writing}}     (结果引用 Method)
review → {{lit-review}} + {{method-writing}} + {{results-writing}}
abstract-title → {{review}}              (摘要引用全文)
```

---

## 多模型配置

每个 Prompt 节点可以独立选择 LLM 提供商和模型：

| 提供商 | 支持模型（示例） |
|--------|-----------------|
| Claude | claude-sonnet-4-20250514, claude-3-opus-latest |
| OpenAI | gpt-4o, gpt-4-turbo, gpt-3.5-turbo |
| Gemini | gemini-2.0-flash, gemini-1.5-pro |
| DeepSeek | deepseek-chat, deepseek-reasoner |

API Key 通过环境变量配置：

```bash
# .env 文件
ANTHROPIC_API_KEY=sk-...
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
DEEPSEEK_API_KEY=...
```

---

## VS Code 集成

执行到 Code 节点时，系统自动在 VS Code 中打开指定文件。也可以通过菜单手动触发：

- 在画布中双击 Code 节点 → 自动打开 VS Code
- API 端点：`POST /api/vscode/open` → 传入文件路径和行号

---

## 工作流管理

| 操作 | 方式 |
|------|------|
| 新建工作流 | 点击 **New** |
| 保存当前工作流 | 点击 **Save**，输入名称 |
| 加载已有工作流 | 点击 **Load**，从列表选择 |
| 保存工作流为模板 | 保存后可在 Templates 中复用 |
| 删除工作流 | 在 Load 列表中点击删除 |

工作流存储在 SQLite 数据库 `backend/workflows.db` 中。

---

## 常见操作场景

### 场景 1：快速生成论文初稿

1. 加载"科研论文写作工作流"模板
2. 在 Start 节点输入论文主题和相关文献
3. 在 Code 节点设置实验代码路径
4. 配置各 Prompt 节点的 API Key 和模型
5. 点击 Run
6. 等待执行完成，查看 Final Output

### 场景 2：自定义小型工作流

1. 新建空白工作流
2. 拖入一个 Prompt 节点 → 输入"总结这段文字"
3. 拖入一个 Code 节点 → 设置文件路径
4. 连接 Prompt → Code
5. 运行：先 AI 总结，再打开编辑器

### 场景 3：分步执行与调试

1. 点击 Run → 引擎自动执行
2. 每个节点执行后可在右侧面板查看输出
3. 如果某个节点出错，修改配置后可以重新执行单个节点（开发中）
4. 点击 Stop 可终止正在执行的工作流

---

## 快捷键

| 快捷键 | 操作 |
|--------|------|
| Ctrl+S | 保存工作流 |
| Ctrl+Z | 撤销 |
| Delete / Backspace | 删除选中节点或连线 |
| 鼠标拖拽 | 移动画布 |
| 滚轮 | 缩放画布 |

---

## 开发模式

### 环境要求

- Python 3.11+
- Node.js 18+
- npm

### 启动（三个终端）

```bash
# 终端 1: 后端 API
cd backend
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8765

# 终端 2: 前端开发服务器
cd frontend
npm install
npm run dev

# 终端 3: Electron 桌面壳（可选）
cd electron
npm install
npm run dev
```

浏览器访问 `http://localhost:5173` 即可使用 Web 版。

### 测试

```bash
cd backend
python -m pytest tests/ -v    # 运行 31 项测试
```

---

## 常见问题

### Q: 运行时报错 "API Key 未配置"

在 `backend/.env` 文件中添加对应提供商的 API Key。可以用文本编辑器创建 `.env` 文件：

```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### Q: 节点执行后没有输出

检查：
1. 该节点是否有前置节点？确保所有上游节点已执行
2. 提示词是否正确引用了 `{{node_id}}`
3. API Key 是否已配置且有效
4. 查看后端终端日志是否有错误信息

### Q: 如何清空画布重新开始

点击 **New** 按钮，确认后画布将被清空。

### Q: 工作流保存在哪里

SQLite 数据库 `backend/workflows.db`。这是一个本地文件，不会自动同步到云端。

### Q: 模板中的参数如何修改

加载模板后，每个节点都可以单独点击修改配置（Provider、Model、Prompt 等），修改后保存即可覆盖模板参数。
