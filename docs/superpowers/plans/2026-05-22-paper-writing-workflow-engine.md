# PaperFlow — 科研论文写作工作流编排引擎 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个 Windows 桌面工具，通过可视化节点编辑器编排科研论文写作工作流，整合 Claude/GPT/Gemini/DeepSeek 多模型，并支持一键调用 VS Code。

**Architecture:** Python FastAPI 后端（LLM API 编排 + SQLite 存储）+ React/ReactFlow 前端（可视化节点编辑器）+ Electron 壳（系统托盘、开机自启、VS Code 集成）。前后端通过 REST API 通信，Electron 管理桌面生命周期。

**Tech Stack:** Python 3.14+, FastAPI, SQLite, React 18, ReactFlow 11, TypeScript, Vite, Electron 33, httpx, pydantic

---

## 项目结构

```
C:\Users\wangd\paper-flow\
├── backend/                    # Python FastAPI 后端
│   ├── main.py                 # FastAPI 入口，uvicorn 启动
│   ├── requirements.txt
│   ├── api/
│   │   ├── __init__.py
│   │   ├── workflows.py        # 工作流 CRUD API
│   │   ├── execution.py        # 工作流执行 API
│   │   └── models.py           # 模型配置 API
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── executor.py         # 工作流执行引擎
│   │   ├── nodes.py            # 节点类型定义（Prompt/Code/Output/Start）
│   │   └── context.py          # 执行上下文（跨节点数据传递）
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py             # LLM 提供商抽象基类
│   │   ├── claude.py           # Anthropic Claude
│   │   ├── openai.py           # OpenAI GPT
│   │   ├── gemini.py           # Google Gemini
│   │   └── deepseek.py         # DeepSeek
│   ├── storage/
│   │   ├── __init__.py
│   │   └── db.py               # SQLite 数据库初始化 + 基本操作
│   └── services/
│       ├── __init__.py
│       └── vscode.py           # VS Code 集成（打开文件/文件夹）
├── frontend/                   # React + ReactFlow 前端
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── main.tsx            # React 入口
│   │   ├── App.tsx             # 根组件（布局：画布 + 侧栏）
│   │   ├── types/
│   │   │   └── workflow.ts     # TypeScript 类型定义
│   │   ├── components/
│   │   │   ├── WorkflowEditor.tsx    # ReactFlow 画布主组件
│   │   │   ├── NodePalette.tsx       # 左侧节点拖拽面板
│   │   │   ├── ChatPanel.tsx         # 右侧对话面板
│   │   │   ├── NodeConfigPanel.tsx   # 节点配置面板
│   │   │   ├── ModelSelector.tsx     # 模型选择下拉
│   │   │   └── Toolbar.tsx           # 顶部工具栏（运行/保存/导出）
│   │   ├── nodes/
│   │   │   ├── PromptNode.tsx        # 提示词节点（自定义渲染）
│   │   │   ├── CodeNode.tsx          # 代码节点（VS Code 按钮）
│   │   │   └── OutputNode.tsx        # 输出节点（结果显示）
│   │   └── utils/
│   │       └── api.ts               # 后端 API 调用封装
│   └── styles/
│       └── index.css                 # 全局样式
├── electron/                   # Electron 桌面壳
│   ├── main.js                 # 主进程（窗口、系统托盘、开机自启）
│   ├── preload.js              # 预加载脚本（IPC 桥接）
│   └── package.json
├── scripts/
│   ├── dev.bat                 # 开发环境一键启动
│   └── startup-setup.bat       # 开机自启注册
└── docs/
    └── superpowers/
        └── plans/
            └── 2026-05-22-paper-writing-workflow-engine.md  # 本文件
```

---

### Task 1: 项目脚手架和开发环境

**Files:**
- Create: `C:\Users\wangd\paper-flow\backend\requirements.txt`
- Create: `C:\Users\wangd\paper-flow\backend\__init__.py`
- Create: `C:\Users\wangd\paper-flow\scripts\dev.bat`
- Create: `C:\Users\wangd\paper-flow\scripts\startup-setup.bat`
- Create: `C:\Users\wangd\paper-flow\.gitignore`

- [ ] **Step 1: 创建 requirements.txt**

```txt
fastapi==0.115.6
uvicorn[standard]==0.34.0
httpx==0.28.1
pydantic==2.10.4
aiofiles==24.1.0
aiosqlite==0.20.0
anthropic==0.49.0
openai==1.58.1
google-genai==1.2.0
python-multipart==0.0.18
```

- [ ] **Step 2: 创建 `.gitignore`**

```gitignore
node_modules/
dist/
.env
__pycache__/
*.pyc
*.pyo
*.db
.vite/
```

- [ ] **Step 3: 创建 `scripts/dev.bat`**

```bat
@echo off
echo Starting PaperFlow development environment...
echo.

:: Start backend
start "PaperFlow-Backend" cmd /c "cd /d %~dp0..\backend && python -m uvicorn main:app --reload --port 8765"

:: Start frontend
start "PaperFlow-Frontend" cmd /c "cd /d %~dp0..\frontend && npm run dev"

echo Backend starting on http://localhost:8765
echo Frontend starting on http://localhost:5173
```

- [ ] **Step 4: 创建 `scripts/startup-setup.bat`**

```bat
@echo off
echo Adding PaperFlow to Windows startup...
set STARTUP_DIR="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set SCRIPT_PATH="%~dp0..\electron\node_modules\.bin\electron.cmd"
set WORK_DIR="%~dp0..\electron"

:: Create shortcut using PowerShell
powershell -Command ^
  $WshShell = New-Object -ComObject WScript.Shell; ^
  $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\PaperFlow.lnk'); ^
  $Shortcut.TargetPath = '%PROGRAMFILES%\nodejs\node.exe'; ^
  $Shortcut.Arguments = '%WORK_DIR%\node_modules\.bin\electron %WORK_DIR%'; ^
  $Shortcut.WorkingDirectory = '%WORK_DIR%'; ^
  $Shortcut.Save()
echo Done. PaperFlow will start automatically on next boot.
```

- [ ] **Step 5: 初始化 Python 虚拟环境**

Run:
```bash
cd C:\Users\wangd\paper-flow
python -m venv backend\.venv
```

Expected: `.venv/` 目录创建成功

- [ ] **Step 6: 安装 Python 依赖**

Run:
```bash
cd C:\Users\wangd\paper-flow\backend
.venv\Scripts\pip install -r requirements.txt
```

Expected: 所有依赖安装成功

---

### Task 2: SQLite 存储层

**Files:**
- Create: `backend/storage/__init__.py`
- Create: `backend/storage/db.py`

- [ ] **Step 1: 编写 db.py**

```python
import aiosqlite
import json
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent.parent / "paperflow.db"


async def get_db() -> aiosqlite.Connection:
    db = await aiosqlite.connect(str(DB_PATH))
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    return db


async def init_db():
    db = await get_db()
    try:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS workflows (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                nodes TEXT NOT NULL DEFAULT '[]',
                edges TEXT NOT NULL DEFAULT '[]',
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS model_configs (
                id TEXT PRIMARY KEY,
                provider TEXT NOT NULL,
                api_key TEXT NOT NULL DEFAULT '',
                model_name TEXT NOT NULL DEFAULT '',
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS chat_history (
                id TEXT PRIMARY KEY,
                workflow_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS execution_logs (
                id TEXT PRIMARY KEY,
                workflow_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                started_at TEXT,
                finished_at TEXT,
                output TEXT DEFAULT '{}',
                FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE CASCADE
            );
        """)
        await db.commit()
    finally:
        await db.close()


# --- Workflow CRUD ---

async def list_workflows() -> list[dict]:
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM workflows ORDER BY updated_at DESC")
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
    finally:
        await db.close()


async def get_workflow(workflow_id: str) -> Optional[dict]:
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM workflows WHERE id = ?", (workflow_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def save_workflow(workflow: dict) -> dict:
    db = await get_db()
    try:
        await db.execute(
            """INSERT INTO workflows (id, name, description, nodes, edges, updated_at)
               VALUES (?, ?, ?, ?, ?, datetime('now'))
               ON CONFLICT(id) DO UPDATE SET
                 name=excluded.name, description=excluded.description,
                 nodes=excluded.nodes, edges=excluded.edges,
                 updated_at=datetime('now')""",
            (
                workflow["id"],
                workflow["name"],
                workflow.get("description", ""),
                json.dumps(workflow.get("nodes", [])),
                json.dumps(workflow.get("edges", [])),
            ),
        )
        await db.commit()
        return await get_workflow(workflow["id"])
    finally:
        await db.close()


async def delete_workflow(workflow_id: str):
    db = await get_db()
    try:
        await db.execute("DELETE FROM workflows WHERE id = ?", (workflow_id,))
        await db.commit()
    finally:
        await db.close()
```

- [ ] **Step 2: 编写 `backend/storage/__init__.py`**

```python
from .db import init_db, list_workflows, get_workflow, save_workflow, delete_workflow

__all__ = ["init_db", "list_workflows", "get_workflow", "save_workflow", "delete_workflow"]
```

- [ ] **Step 3: 验证数据库初始化**

Run:
```bash
cd C:\Users\wangd\paper-flow\backend
.venv\Scripts\python -c "import asyncio; from storage import init_db; asyncio.run(init_db()); print('DB initialized')"
```

Expected: `DB initialized` 输出，`paperflow.db` 文件创建成功

- [ ] **Step 4: Commit**

```bash
git -C C:\Users\wangd\paper-flow init
git -C C:\Users\wangd\paper-flow add backend/storage/ backend/__init__.py backend/requirements.txt .gitignore
git -C C:\Users\wangd\paper-flow commit -m "feat: add SQLite storage layer with workflow CRUD"
```

---

### Task 3: LLM 提供商抽象层 + 各模型实现

**Files:**
- Create: `backend/providers/__init__.py`
- Create: `backend/providers/base.py`
- Create: `backend/providers/claude.py`
- Create: `backend/providers/openai.py`
- Create: `backend/providers/gemini.py`
- Create: `backend/providers/deepseek.py`

- [ ] **Step 1: 编写抽象基类 `base.py`**

```python
from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    def __init__(self, api_key: str, model_name: str = ""):
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    async def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        ...

    @abstractmethod
    async def chat_stream(self, prompt: str, system_prompt: Optional[str] = None):
        """Async generator yielding text chunks."""
        yield ""  # pragma: no cover

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...

    @staticmethod
    def get_provider(provider: str, api_key: str, model_name: str = "") -> "LLMProvider":
        from .claude import ClaudeProvider
        from .openai import OpenAIProvider
        from .gemini import GeminiProvider
        from .deepseek import DeepSeekProvider

        mapping = {
            "claude": ClaudeProvider,
            "openai": OpenAIProvider,
            "gemini": GeminiProvider,
            "deepseek": DeepSeekProvider,
        }
        cls = mapping.get(provider)
        if not cls:
            raise ValueError(f"Unknown provider: {provider}")
        return cls(api_key, model_name)
```

- [ ] **Step 2: 编写 `providers/claude.py`**

```python
from typing import Optional
from anthropic import AsyncAnthropic
from .base import LLMProvider


class ClaudeProvider(LLMProvider):
    @property
    def provider_name(self) -> str:
        return "claude"

    async def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        client = AsyncAnthropic(api_key=self.api_key)
        kwargs = {
            "model": self.model_name or "claude-sonnet-4-20250514",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        resp = await client.messages.create(**kwargs)
        return resp.content[0].text

    async def chat_stream(self, prompt: str, system_prompt: Optional[str] = None):
        client = AsyncAnthropic(api_key=self.api_key)
        kwargs = {
            "model": self.model_name or "claude-sonnet-4-20250514",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        async with client.messages.stream(**kwargs) as stream:
            async for text in stream.text_stream:
                yield text
```

- [ ] **Step 3: 编写 `providers/openai.py`**

```python
from typing import Optional
from openai import AsyncOpenAI
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    @property
    def provider_name(self) -> str:
        return "openai"

    async def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        client = AsyncOpenAI(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        resp = await client.chat.completions.create(
            model=self.model_name or "gpt-4o",
            messages=messages,
        )
        return resp.choices[0].message.content or ""

    async def chat_stream(self, prompt: str, system_prompt: Optional[str] = None):
        client = AsyncOpenAI(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        stream = await client.chat.completions.create(
            model=self.model_name or "gpt-4o",
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

- [ ] **Step 4: 编写 `providers/gemini.py`**

```python
from typing import Optional
from google import genai
from .base import LLMProvider


class GeminiProvider(LLMProvider):
    @property
    def provider_name(self) -> str:
        return "gemini"

    async def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        client = genai.Client(api_key=self.api_key)
        model = self.model_name or "gemini-2.0-flash"
        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": system_prompt + "\n\n" + prompt}]})
        else:
            contents.append({"role": "user", "parts": [{"text": prompt}]})
        resp = client.models.generate_content(model=model, contents=contents)
        return resp.text or ""

    async def chat_stream(self, prompt: str, system_prompt: Optional[str] = None):
        client = genai.Client(api_key=self.api_key)
        model = self.model_name or "gemini-2.0-flash"
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        resp = client.models.generate_content_stream(model=model, contents=contents)
        for chunk in resp:
            if chunk.text:
                yield chunk.text
```

- [ ] **Step 5: 编写 `providers/deepseek.py`**

```python
from typing import Optional
from openai import AsyncOpenAI
from .base import LLMProvider


DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"


class DeepSeekProvider(LLMProvider):
    @property
    def provider_name(self) -> str:
        return "deepseek"

    async def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        client = AsyncOpenAI(api_key=self.api_key, base_url=DEEPSEEK_BASE_URL)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        resp = await client.chat.completions.create(
            model=self.model_name or "deepseek-chat",
            messages=messages,
        )
        return resp.choices[0].message.content or ""

    async def chat_stream(self, prompt: str, system_prompt: Optional[str] = None):
        client = AsyncOpenAI(api_key=self.api_key, base_url=DEEPSEEK_BASE_URL)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        stream = await client.chat.completions.create(
            model=self.model_name or "deepseek-chat",
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

- [ ] **Step 6: 编写 `providers/__init__.py`**

```python
from .base import LLMProvider

__all__ = ["LLMProvider"]
```

- [ ] **Step 7: 验证 providers**

Run:
```bash
cd C:\Users\wangd\paper-flow\backend
.venv\Scripts\python -c "
from providers.base import LLMProvider
p = LLMProvider.get_provider('claude', 'test-key', 'claude-sonnet-4-20250514')
print(f'Provider: {p.provider_name}, model: {p.model_name}')
assert p.provider_name == 'claude'
print('OK')
"
```

Expected: `Provider: claude, model: claude-sonnet-4-20250514` + `OK`

- [ ] **Step 8: Commit**

```bash
git -C C:\Users\wangd\paper-flow add backend/providers/
git -C C:\Users\wangd\paper-flow commit -m "feat: add LLM provider abstraction with Claude/GPT/Gemini/DeepSeek"
```

---

### Task 4: 工作流执行引擎

**Files:**
- Create: `backend/engine/__init__.py`
- Create: `backend/engine/nodes.py`
- Create: `backend/engine/context.py`
- Create: `backend/engine/executor.py`

- [ ] **Step 1: 编写节点类型定义 `nodes.py`**

```python
from typing import Optional
from pydantic import BaseModel


class WorkflowNode(BaseModel):
    id: str
    type: str  # "prompt" | "code" | "output" | "start"
    position: dict  # {"x": float, "y": float}
    data: dict = {}  # 节点具体数据

    # prompt 节点: data = {"prompt": "...", "system_prompt": "...", "provider": "claude", "model": "..."}
    # code 节点: data = {"file_path": "...", "command": "...", "description": "..."}
    # output 节点: data = {"format": "markdown"}


class WorkflowEdge(BaseModel):
    id: str
    source: str
    target: str
    source_handle: Optional[str] = None
    target_handle: Optional[str] = None


class WorkflowDef(BaseModel):
    id: str
    name: str
    description: str = ""
    nodes: list[WorkflowNode] = []
    edges: list[WorkflowEdge] = []
```

- [ ] **Step 2: 编写执行上下文 `context.py`**

```python
from typing import Any


class ExecutionContext:
    """跨节点传递数据的执行上下文"""

    def __init__(self):
        self._data: dict[str, Any] = {}

    def set_node_output(self, node_id: str, output: Any):
        self._data[node_id] = output

    def get_node_output(self, node_id: str) -> Any:
        return self._data.get(node_id)

    def get_all_outputs(self) -> dict:
        return dict(self._data)

    def get_upstream_outputs(self, node_id: str, edges: list[dict]) -> dict:
        """获取某节点的所有上游节点的输出"""
        upstream_ids = {e["source"] for e in edges if e["target"] == node_id}
        return {uid: self._data.get(uid) for uid in upstream_ids if uid in self._data}
```

- [ ] **Step 3: 编写执行引擎 `executor.py`**

```python
import asyncio
from typing import Optional
from ..providers.base import LLMProvider
from ..storage.db import save_workflow
from .context import ExecutionContext
from .nodes import WorkflowNode


class WorkflowExecutor:
    def __init__(self):
        self.context = ExecutionContext()
        self._stop_requested = False

    def request_stop(self):
        self._stop_requested = True

    async def execute_node(
        self,
        node: WorkflowNode,
        upstream_context: dict,
        provider: Optional[LLMProvider] = None,
    ) -> str:
        if self._stop_requested:
            return "[Execution stopped]"

        node_type = node.type
        data = node.data

        if node_type == "start":
            return "[Start node]"

        elif node_type == "prompt":
            prompt_template = data.get("prompt", "")
            # 用上游输出替换模板中的变量
            prompt = prompt_template
            for uid, output in upstream_context.items():
                placeholder = "{{" + uid + "}}"
                prompt = prompt.replace(placeholder, output or "")

            system_prompt = data.get("system_prompt")
            if provider:
                return await provider.chat(prompt, system_prompt)
            return f"[Mock response for: {prompt[:50]}...]"

        elif node_type == "code":
            description = data.get("description", "")
            return f"[Code task: {description} — open in VS Code]"

        elif node_type == "output":
            content = []
            for uid, out in upstream_context.items():
                content.append(f"--- From {uid} ---\n{out}")
            return "\n\n".join(content)

        return f"[Unknown node type: {node_type}]"

    async def execute(
        self,
        workflow_def: dict,
        provider_map: dict[str, LLMProvider],
        on_node_complete=None,
    ) -> dict:
        """按拓扑顺序执行工作流。provider_map: node_id -> LLMProvider"""
        self._stop_requested = False
        nodes = {n["id"]: WorkflowNode(**n) for n in workflow_def.get("nodes", [])}
        edges = workflow_def.get("edges", [])
        execution_order = self._topological_sort(list(nodes.keys()), edges)
        results = {}

        for node_id in execution_order:
            node = nodes[node_id]
            upstream = self.context.get_upstream_outputs(node_id, edges)
            prov = provider_map.get(node_id)
            output = await self.execute_node(node, upstream, prov)
            self.context.set_node_output(node_id, output)
            results[node_id] = output

            if on_node_complete:
                await on_node_complete(node_id, output)

        return self.context.get_all_outputs()

    def _topological_sort(self, node_ids: list[str], edges: list[dict]) -> list[str]:
        from collections import deque, defaultdict

        in_degree = {nid: 0 for nid in node_ids}
        adj = defaultdict(list)

        for e in edges:
            adj[e["source"]].append(e["target"])
            in_degree[e["target"]] = in_degree.get(e["target"], 0) + 1

        queue = deque([nid for nid, deg in in_degree.items() if deg == 0])
        result = []

        while queue:
            nid = queue.popleft()
            result.append(nid)
            for neighbor in adj[nid]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result
```

- [ ] **Step 4: 编写 `engine/__init__.py`**

```python
from .executor import WorkflowExecutor
from .nodes import WorkflowNode, WorkflowEdge, WorkflowDef

__all__ = ["WorkflowExecutor", "WorkflowNode", "WorkflowEdge", "WorkflowDef"]
```

- [ ] **Step 5: 验证执行引擎**

Run:
```bash
cd C:\Users\wangd\paper-flow\backend
.venv\Scripts\python -c "
import asyncio
from engine import WorkflowExecutor

wf = {
    'id': 'test-1',
    'name': 'Test',
    'nodes': [
        {'id': 'start', 'type': 'start', 'position': {'x': 0, 'y': 0}, 'data': {}},
        {'id': 'prompt-1', 'type': 'prompt', 'position': {'x': 200, 'y': 0}, 'data': {'prompt': 'Write about {{start}}'}},
        {'id': 'output-1', 'type': 'output', 'position': {'x': 400, 'y': 0}, 'data': {}},
    ],
    'edges': [
        {'id': 'e1', 'source': 'start', 'target': 'prompt-1'},
        {'id': 'e2', 'source': 'prompt-1', 'target': 'output-1'},
    ],
}

executor = WorkflowExecutor()
results = asyncio.run(executor.execute(wf, {}))
print('Results:', results)
assert 'start' in results
assert 'prompt-1' in results
assert 'output-1' in results
print('Execution order OK')
"
```

Expected: `Execution order OK` and results dict printed

- [ ] **Step 6: Commit**

```bash
git -C C:\Users\wangd\paper-flow add backend/engine/
git -C C:\Users\wangd\paper-flow commit -m "feat: add workflow execution engine with topological sort"
```

---

### Task 5: VS Code 集成服务

**Files:**
- Create: `backend/services/__init__.py`
- Create: `backend/services/vscode.py`

- [ ] **Step 1: 编写 `vscode.py`**

```python
import subprocess
import shutil
from pathlib import Path
from typing import Optional


def _find_vscode() -> Optional[str]:
    """查找 VS Code 可执行文件路径"""
    candidates = [
        r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        r"C:\Users\wangd\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
        r"C:\Users\wangd\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    # 尝试从 PATH 查找
    return shutil.which("code")


def open_file(file_path: str, line: Optional[int] = None) -> dict:
    """在 VS Code 中打开文件"""
    vscode = _find_vscode()
    if not vscode:
        return {"success": False, "error": "VS Code not found"}

    path = Path(file_path).resolve()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("")

    args = [vscode, str(path)]
    if line is not None:
        args.insert(1, f"--goto")
        args.append(f"{path}:{line}")

    try:
        subprocess.Popen(args, shell=True)
        return {"success": True, "path": str(path)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_folder(folder_path: str) -> dict:
    """在 VS Code 中打开文件夹"""
    vscode = _find_vscode()
    if not vscode:
        return {"success": False, "error": "VS Code not found"}

    path = Path(folder_path).resolve()
    path.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.Popen([vscode, str(path)], shell=True)
        return {"success": True, "path": str(path)}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

- [ ] **Step 2: 编写 `services/__init__.py`**

```python
from .vscode import open_file, open_folder

__all__ = ["open_file", "open_folder"]
```

- [ ] **Step 3: 验证服务 (dry run, 不真正启动 VS Code)**

Run:
```bash
cd C:\Users\wangd\paper-flow\backend
.venv\Scripts\python -c "
from services.vscode import _find_vscode
path = _find_vscode()
print(f'VS Code found at: {path}')
if path:
    print('VS Code is available')
else:
    print('VS Code not in PATH or standard locations')
"
```

Expected: 显示 VS Code 路径或提示未找到（不影响功能）

- [ ] **Step 4: Commit**

```bash
git -C C:\Users\wangd\paper-flow add backend/services/
git -C C:\Users\wangd\paper-flow commit -m "feat: add VS Code integration service"
```

---

### Task 6: FastAPI 后端主入口 + API 路由

**Files:**
- Modify: `backend/main.py`
- Create: `backend/api/__init__.py`
- Create: `backend/api/workflows.py`
- Create: `backend/api/execution.py`
- Create: `backend/api/models.py`

- [ ] **Step 1: 编写 `backend/api/workflows.py`**

```python
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..storage.db import list_workflows, get_workflow, save_workflow, delete_workflow

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


class WorkflowPayload(BaseModel):
    id: str | None = None
    name: str
    description: str = ""
    nodes: list[dict] = []
    edges: list[dict] = []


@router.get("")
async def list_all():
    return await list_workflows()


@router.get("/{workflow_id}")
async def get_one(workflow_id: str):
    wf = await get_workflow(workflow_id)
    if not wf:
        raise HTTPException(404, "Workflow not found")
    return wf


@router.post("")
async def create(payload: WorkflowPayload):
    import json
    wf = {
        "id": payload.id or str(uuid.uuid4()),
        "name": payload.name,
        "description": payload.description,
        "nodes": payload.nodes,
        "edges": payload.edges,
    }
    return await save_workflow(wf)


@router.put("/{workflow_id}")
async def update(workflow_id: str, payload: WorkflowPayload):
    existing = await get_workflow(workflow_id)
    if not existing:
        raise HTTPException(404, "Workflow not found")
    wf = {
        "id": workflow_id,
        "name": payload.name,
        "description": payload.description,
        "nodes": payload.nodes,
        "edges": payload.edges,
    }
    return await save_workflow(wf)


@router.delete("/{workflow_id}")
async def delete(workflow_id: str):
    await delete_workflow(workflow_id)
    return {"ok": True}
```

- [ ] **Step 2: 编写 `backend/api/execution.py`**

```python
import json
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..engine import WorkflowExecutor
from ..providers.base import LLMProvider
from ..storage.db import get_workflow, save_workflow

router = APIRouter(prefix="/api/execution", tags=["execution"])


class ExecuteRequest(BaseModel):
    workflow_id: str
    provider_overrides: dict[str, dict] = {}  # node_id -> {provider, api_key, model_name}


class NodeResult(BaseModel):
    node_id: str
    output: str


@router.post("/run")
async def run_workflow(req: ExecuteRequest):
    wf = await get_workflow(req.workflow_id)
    if not wf:
        raise HTTPException(404, "Workflow not found")

    wf_data = dict(wf)
    wf_data["nodes"] = json.loads(wf_data.get("nodes", "[]"))
    wf_data["edges"] = json.loads(wf_data.get("edges", "[]"))

    # 构建 provider 映射
    provider_map = {}
    for n in wf_data["nodes"]:
        nid = n["id"]
        if nid in req.provider_overrides:
            cfg = req.provider_overrides[nid]
            provider_map[nid] = LLMProvider.get_provider(
                cfg.get("provider", "claude"),
                cfg.get("api_key", ""),
                cfg.get("model_name", ""),
            )
        elif n.get("type") == "prompt":
            data = n.get("data", {})
            if data.get("provider") and data.get("api_key"):
                provider_map[nid] = LLMProvider.get_provider(
                    data["provider"], data["api_key"], data.get("model", ""),
                )

    executor = WorkflowExecutor()
    results = await executor.execute(wf_data, provider_map)
    return {"workflow_id": req.workflow_id, "results": results}


@router.post("/stop")
async def stop_execution():
    # 简化：用全局引用控制
    return {"ok": True}
```

- [ ] **Step 3: 编写 `backend/api/models.py`**

```python
from fastapi import APIRouter
from pydantic import BaseModel
from ..storage.db import get_db

router = APIRouter(prefix="/api/models", tags=["models"])


class ModelConfigPayload(BaseModel):
    id: str | None = None
    provider: str
    api_key: str = ""
    model_name: str = ""


@router.get("")
async def list_configs():
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM model_configs WHERE is_active = 1")
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
    finally:
        await db.close()


@router.post("")
async def save_config(payload: ModelConfigPayload):
    import uuid
    db = await get_db()
    try:
        cfg_id = payload.id or str(uuid.uuid4())
        await db.execute(
            """INSERT INTO model_configs (id, provider, api_key, model_name)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 provider=excluded.provider, api_key=excluded.api_key,
                 model_name=excluded.model_name""",
            (cfg_id, payload.provider, payload.api_key, payload.model_name),
        )
        await db.commit()
        cursor = await db.execute("SELECT * FROM model_configs WHERE id = ?", (cfg_id,))
        row = await cursor.fetchone()
        return dict(row)
    finally:
        await db.close()
```

- [ ] **Step 4: 编写 `api/__init__.py`**

```python
# API routes package
```

- [ ] **Step 5: 编写 `backend/main.py`**

```python
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from storage.db import init_db
from api.workflows import router as workflows_router
from api.execution import router as execution_router
from api.models import router as models_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="PaperFlow API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8765"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflows_router)
app.include_router(execution_router)
app.include_router(models_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8765, reload=True)
```

- [ ] **Step 6: 启动后端并验证 API**

Run:
```bash
cd C:\Users\wangd\paper-flow\backend
.venv\Scripts\python -c "
import asyncio, httpx, json

async def test():
    # 启动服务器
    import uvicorn
    import threading
    from main import app
    
    config = uvicorn.Config(app, host='127.0.0.1', port=8766, log_level='error')
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run)
    thread.daemon = True
    thread.start()
    await asyncio.sleep(2)
    
    # 测试 health
    async with httpx.AsyncClient() as client:
        r = await client.get('http://127.0.0.1:8766/api/health')
        assert r.json() == {'status': 'ok'}, r.text
        
        # 创建 workflow
        wf = {'name': 'Test Paper', 'nodes': [], 'edges': []}
        r = await client.post('http://127.0.0.1:8766/api/workflows', json=wf)
        assert r.status_code == 200, r.text
        wf_id = r.json()['id']
        print(f'Created workflow: {wf_id}')
        
        # 列出 workflows
        r = await client.get('http://127.0.0.1:8766/api/workflows')
        assert len(r.json()) == 1
        print('List workflows: OK')
        
        # 删除
        r = await client.delete(f'http://127.0.0.1:8766/api/workflows/{wf_id}')
        assert r.status_code == 200
        print('Delete: OK')
    
    server.should_exit = True
    print('All API tests passed')

asyncio.run(test())
"
```

Expected: `All API tests passed`

- [ ] **Step 7: Commit**

```bash
git -C C:\Users\wangd\paper-flow add backend/main.py backend/api/
git -C C:\Users\wangd\paper-flow commit -m "feat: add FastAPI backend with workflow CRUD and execution APIs"
```

---

### Task 7: 前端项目脚手架

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/index.html`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/types/workflow.ts`
- Create: `frontend/src/utils/api.ts`
- Create: `frontend/styles/index.css`

- [ ] **Step 1: 创建 `frontend/package.json`**

```json
{
  "name": "paper-flow-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "reactflow": "^11.11.4",
    "lucide-react": "^0.468.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.4",
    "typescript": "^5.6.3",
    "vite": "^6.0.5"
  }
}
```

- [ ] **Step 2: 创建 `frontend/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"]
}
```

- [ ] **Step 3: 创建 `frontend/vite.config.ts`**

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8765',
    },
  },
})
```

- [ ] **Step 4: 创建 `frontend/index.html`**

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PaperFlow - 科研论文写作工作流</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

- [ ] **Step 5: 创建 `frontend/src/types/workflow.ts`**

```ts
export interface WorkflowNode {
  id: string;
  type: 'prompt' | 'code' | 'output' | 'start';
  position: { x: number; y: number };
  data: Record<string, any>;
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  sourceHandle?: string;
  targetHandle?: string;
}

export interface Workflow {
  id: string;
  name: string;
  description: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  created_at?: string;
  updated_at?: string;
}

export interface ModelConfig {
  id: string;
  provider: 'claude' | 'openai' | 'gemini' | 'deepseek';
  api_key: string;
  model_name: string;
  is_active: number;
}

export interface ExecutionResults {
  workflow_id: string;
  results: Record<string, string>;
}

export type NodeType = 'prompt' | 'code' | 'output' | 'start';
```

- [ ] **Step 6: 创建 `frontend/src/utils/api.ts`**

```ts
const API_BASE = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`API error ${res.status}: ${err}`);
  }
  return res.json();
}

export const api = {
  // Workflows
  listWorkflows: () => request<any[]>('/workflows'),
  getWorkflow: (id: string) => request<any>(`/workflows/${id}`),
  createWorkflow: (data: any) =>
    request<any>('/workflows', { method: 'POST', body: JSON.stringify(data) }),
  updateWorkflow: (id: string, data: any) =>
    request<any>(`/workflows/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteWorkflow: (id: string) =>
    request<any>(`/workflows/${id}`, { method: 'DELETE' }),

  // Execution
  runWorkflow: (workflowId: string, providerOverrides?: Record<string, any>) =>
    request<any>('/execution/run', {
      method: 'POST',
      body: JSON.stringify({ workflow_id: workflowId, provider_overrides: providerOverrides || {} }),
    }),

  // Models
  listModelConfigs: () => request<any[]>('/models'),
  saveModelConfig: (data: any) =>
    request<any>('/models', { method: 'POST', body: JSON.stringify(data) }),
};
```

- [ ] **Step 7: 创建 `frontend/src/main.tsx`**

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import '../styles/index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

- [ ] **Step 8: 创建 `frontend/styles/index.css`**

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #root {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  background: #1a1a2e;
  color: #eee;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #2a2a4a;
  font-size: 18px;
  font-weight: 600;
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.toolbar {
  height: 48px;
  background: #fff;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 8px;
}

.toolbar button {
  padding: 6px 14px;
  border: 1px solid #d0d0d0;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.toolbar button:hover {
  background: #f0f0f0;
}

.toolbar button.primary {
  background: #4f46e5;
  color: #fff;
  border-color: #4f46e5;
}

.toolbar button.primary:hover {
  background: #4338ca;
}

.canvas-area {
  flex: 1;
  position: relative;
}

.node-palette {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.palette-item {
  padding: 8px 12px;
  background: #16213e;
  border: 1px solid #2a2a4a;
  border-radius: 6px;
  cursor: grab;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.palette-item:hover {
  background: #1a1a4e;
}

.panel {
  width: 320px;
  background: #fff;
  border-left: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.panel-header {
  padding: 12px 16px;
  border-bottom: 1px solid #e0e0e0;
  font-weight: 600;
  font-size: 14px;
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
}

/* ReactFlow overrides */
.react-flow__node {
  border-radius: 8px !important;
  font-size: 13px !important;
}

.prompt-node {
  background: #e0f2fe;
  border: 2px solid #38bdf8;
  padding: 12px;
  min-width: 180px;
}

.code-node {
  background: #dcfce7;
  border: 2px solid #4ade80;
  padding: 12px;
  min-width: 180px;
}

.output-node {
  background: #fef3c7;
  border: 2px solid #fbbf24;
  padding: 12px;
  min-width: 180px;
}

.start-node {
  background: #e0e7ff;
  border: 2px solid #818cf8;
  padding: 12px;
  min-width: 120px;
  border-radius: 50% !important;
  text-align: center;
}
```

- [ ] **Step 9: 创建 `App.tsx`（骨架 + 布局）**

```tsx
import { useState, useCallback } from 'react';
import { ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';
import Toolbar from './components/Toolbar';
import NodePalette from './components/NodePalette';
import WorkflowEditor from './components/WorkflowEditor';
import ChatPanel from './components/ChatPanel';
import NodeConfigPanel from './components/NodeConfigPanel';

export default function App() {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [chatMessages, setChatMessages] = useState<{ role: string; content: string }[]>([]);

  return (
    <div className="app-layout">
      {/* 左侧边栏 */}
      <div className="sidebar">
        <div className="sidebar-header">📄 PaperFlow</div>
        <NodePalette />
      </div>

      {/* 中间画布 */}
      <div className="main-area">
        <Toolbar
          workflowId={workflowId}
          onWorkflowSaved={(id) => setWorkflowId(id)}
        />
        <div className="canvas-area">
          <ReactFlowProvider>
            <WorkflowEditor
              onNodeSelect={(nodeId) => setSelectedNodeId(nodeId)}
            />
          </ReactFlowProvider>
        </div>
      </div>

      {/* 右侧面板 */}
      <div className="panel">
        {selectedNodeId ? (
          <NodeConfigPanel
            nodeId={selectedNodeId}
            onChatMessage={(msg) => setChatMessages((prev) => [...prev, msg])}
          />
        ) : (
          <ChatPanel messages={chatMessages} />
        )}
      </div>
    </div>
  );
}
```

- [ ] **Step 10: 安装前端依赖**

Run:
```bash
cd C:\Users\wangd\paper-flow\frontend
npm install
```

Expected: node_modules 安装成功，无错误

- [ ] **Step 11: 验证前端构建**

Run:
```bash
cd C:\Users\wangd\paper-flow\frontend
npx tsc --noEmit
```

Expected: 无 TypeScript 错误

- [ ] **Step 12: Commit**

```bash
git -C C:\Users\wangd\paper-flow add frontend/
git -C C:\Users\wangd\paper-flow commit -m "feat: add React + ReactFlow frontend scaffold"
```

---

### Task 8: 工作流编辑器组件（核心）

**Files:**
- Create: `frontend/src/components/WorkflowEditor.tsx`
- Create: `frontend/src/components/NodePalette.tsx`
- Create: `frontend/src/components/Toolbar.tsx`
- Create: `frontend/src/nodes/PromptNode.tsx`
- Create: `frontend/src/nodes/CodeNode.tsx`
- Create: `frontend/src/nodes/OutputNode.tsx`

- [ ] **Step 1: 编写自定义节点 `PromptNode.tsx`**

```tsx
import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

function PromptNode({ data, selected }: NodeProps) {
  return (
    <div className={`prompt-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 600, marginBottom: 4 }}>Prompt</div>
      <div style={{ fontSize: 12, color: '#555' }}>
        {data.prompt ? data.prompt.substring(0, 60) + (data.prompt.length > 60 ? '...' : '') : '点击配置提示词'}
      </div>
      {data.provider && (
        <div style={{ fontSize: 11, color: '#888', marginTop: 4 }}>
          Model: {data.provider}/{data.model || 'default'}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(PromptNode);
```

- [ ] **Step 2: 编写 `CodeNode.tsx`**

```tsx
import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

function CodeNode({ data, selected }: NodeProps) {
  return (
    <div className={`code-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 600, marginBottom: 4 }}>🧑‍💻 Code</div>
      <div style={{ fontSize: 12, color: '#555' }}>
        {data.description || '点击配置代码任务'}
      </div>
      {data.file_path && (
        <div style={{ fontSize: 11, color: '#888', marginTop: 4 }}>
          File: {data.file_path.split('\\').pop()}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(CodeNode);
```

- [ ] **Step 3: 编写 `OutputNode.tsx`**

```tsx
import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

function OutputNode({ data, selected }: NodeProps) {
  return (
    <div className={`output-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 600, marginBottom: 4 }}>📝 Output</div>
      <div style={{ fontSize: 12, color: '#555' }}>
        {data.output ? data.output.substring(0, 80) + '...' : '等待执行...'}
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(OutputNode);
```

- [ ] **Step 4: 编写核心节点注册 + 保存类型**

在 `frontend/src/components/` 创建 `nodeTypes.ts`:

```ts
import PromptNode from '../nodes/PromptNode';
import CodeNode from '../nodes/CodeNode';
import OutputNode from '../nodes/OutputNode';

export const nodeTypes = {
  prompt: PromptNode,
  code: CodeNode,
  output: OutputNode,
  start: PromptNode, // start 节点复用 prompt 的渲染
};
```

- [ ] **Step 5: 编写 `WorkflowEditor.tsx`**

```tsx
import { useCallback, useRef, useState } from 'react';
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  Connection,
  useNodesState,
  useEdgesState,
  ReactFlowInstance,
  SelectionMode,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { nodeTypes } from './nodeTypes';

interface Props {
  onNodeSelect: (nodeId: string | null) => void;
}

let nodeIdCounter = 0;
function getNewNodeId() {
  return `node_${++nodeIdCounter}_${Date.now()}`;
}

const defaultNodes: Node[] = [
  {
    id: 'start',
    type: 'start',
    position: { x: 300, y: 50 },
    data: { label: 'Start', prompt: '开始' },
  },
];

export default function WorkflowEditor({ onNodeSelect }: Props) {
  const [nodes, setNodes, onNodesChange] = useNodesState(defaultNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const reactFlowInstance = useRef<ReactFlowInstance | null>(null);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => onNodeSelect(node.id),
    [onNodeSelect],
  );

  const onPaneClick = useCallback(() => onNodeSelect(null), [onNodeSelect]);

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      const type = event.dataTransfer.getData('application/reactflow');
      if (!type || !reactFlowInstance.current) return;

      const position = reactFlowInstance.current.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });

      const newNode: Node = {
        id: getNewNodeId(),
        type,
        position,
        data: { label: type === 'prompt' ? 'New Prompt' : type === 'code' ? 'New Code' : 'New Output' },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [setNodes],
  );

  const getWorkflowData = useCallback(() => {
    return { nodes, edges };
  }, [nodes, edges]);

  // 暴露给父组件
  (window as any).__getWorkflowData = getWorkflowData;

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onConnect={onConnect}
      onInit={(instance) => { reactFlowInstance.current = instance; }}
      onNodeClick={onNodeClick}
      onPaneClick={onPaneClick}
      onDragOver={onDragOver}
      onDrop={onDrop}
      nodeTypes={nodeTypes}
      fitView
      selectionMode={SelectionMode.Partial}
    >
      <Background />
      <Controls />
      <MiniMap style={{ width: 150, height: 100 }} />
    </ReactFlow>
  );
}
```

- [ ] **Step 6: 编写 `NodePalette.tsx`**

```tsx
import { DragEvent } from 'react';

const nodeTypes = [
  { type: 'prompt', label: '💬 Prompt', color: '#38bdf8' },
  { type: 'code', label: '🧑‍💻 Code/VS Code', color: '#4ade80' },
  { type: 'output', label: '📝 Output', color: '#fbbf24' },
];

export default function NodePalette() {
  const onDragStart = (event: DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div className="node-palette">
      <div style={{ padding: '8px 12px', fontSize: 12, color: '#888' }}>
        拖拽节点到画布
      </div>
      {nodeTypes.map(({ type, label }) => (
        <div
          key={type}
          className="palette-item"
          draggable
          onDragStart={(e) => onDragStart(e, type)}
        >
          <span>{label}</span>
        </div>
      ))}
    </div>
  );
}
```

- [ ] **Step 7: 编写 `Toolbar.tsx`**

```tsx
import { useState } from 'react';
import { api } from '../utils/api';

interface Props {
  workflowId: string | null;
  onWorkflowSaved: (id: string) => void;
}

export default function Toolbar({ workflowId, onWorkflowSaved }: Props) {
  const [saving, setSaving] = useState(false);
  const [running, setRunning] = useState(false);
  const [name, setName] = useState('未命名工作流');

  const handleSave = async () => {
    setSaving(true);
    try {
      const wfData = (window as any).__getWorkflowData?.();
      if (!wfData) return;

      const payload = {
        id: workflowId || undefined,
        name,
        nodes: wfData.nodes,
        edges: wfData.edges,
      };

      const result = workflowId
        ? await api.updateWorkflow(workflowId, payload)
        : await api.createWorkflow(payload);

      onWorkflowSaved(result.id);
    } finally {
      setSaving(false);
    }
  };

  const handleRun = async () => {
    if (!workflowId) {
      await handleSave();
    }
    setRunning(true);
    try {
      if (workflowId) {
        const result = await api.runWorkflow(workflowId);
        console.log('Execution results:', result);
        alert('工作流执行完成！');
      }
    } catch (err: any) {
      alert('执行失败: ' + err.message);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="toolbar">
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={{
          border: 'none',
          fontSize: 16,
          fontWeight: 600,
          outline: 'none',
          flex: 1,
        }}
      />
      <button onClick={handleSave} disabled={saving}>
        {saving ? '保存中...' : '💾 保存'}
      </button>
      <button className="primary" onClick={handleRun} disabled={running}>
        {running ? '执行中...' : '▶ 运行'}
      </button>
    </div>
  );
}
```

- [ ] **Step 8: 验证 TypeScript 编译**

Run:
```bash
cd C:\Users\wangd\paper-flow\frontend
npx tsc --noEmit
```

Expected: 无 TypeScript 错误

- [ ] **Step 9: Commit**

```bash
git -C C:\Users\wangd\paper-flow add frontend/src/components/ frontend/src/nodes/
git -C C:\Users\wangd\paper-flow commit -m "feat: add workflow editor with custom nodes and drag-drop"
```

---

### Task 9: 节点配置面板 + 对话面板 + 模型选择

**Files:**
- Create: `frontend/src/components/NodeConfigPanel.tsx`
- Create: `frontend/src/components/ChatPanel.tsx`
- Create: `frontend/src/components/ModelSelector.tsx`

- [ ] **Step 1: 编写 `ModelSelector.tsx`**

```tsx
import { useState, useEffect } from 'react';
import { api } from '../utils/api';

const PROVIDERS = [
  { value: 'claude', label: 'Claude (Anthropic)' },
  { value: 'openai', label: 'GPT (OpenAI)' },
  { value: 'gemini', label: 'Gemini (Google)' },
  { value: 'deepseek', label: 'DeepSeek' },
];

interface Props {
  provider: string;
  modelName: string;
  onChange: (provider: string, modelName: string) => void;
}

export default function ModelSelector({ provider, modelName, onChange }: Props) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      <label style={{ fontSize: 12, fontWeight: 600, color: '#555' }}>模型</label>
      <select
        value={provider}
        onChange={(e) => onChange(e.target.value, modelName)}
        style={selectStyle}
      >
        <option value="">-- 选择模型 --</option>
        {PROVIDERS.map((p) => (
          <option key={p.value} value={p.value}>{p.label}</option>
        ))}
      </select>
      {provider && (
        <input
          type="text"
          placeholder="模型名称（留空用默认）"
          value={modelName}
          onChange={(e) => onChange(provider, e.target.value)}
          style={inputStyle}
        />
      )}
    </div>
  );
}

const selectStyle: React.CSSProperties = {
  padding: '6px 8px',
  borderRadius: 6,
  border: '1px solid #d0d0d0',
  fontSize: 13,
};

const inputStyle: React.CSSProperties = {
  padding: '6px 8px',
  borderRadius: 6,
  border: '1px solid #d0d0d0',
  fontSize: 13,
};
```

- [ ] **Step 2: 编写 `NodeConfigPanel.tsx`**

```tsx
import { useState, useEffect, useCallback } from 'react';
import {
  useNodes,
  useEdges,
  useReactFlow,
} from 'reactflow';
import ModelSelector from './ModelSelector';

interface Props {
  nodeId: string;
  onChatMessage?: (msg: { role: string; content: string }) => void;
}

export default function NodeConfigPanel({ nodeId, onChatMessage }: Props) {
  const { setNodes } = useReactFlow();
  const nodes = useNodes();
  const edges = useEdges();
  const node = nodes.find((n) => n.id === nodeId);

  const [prompt, setPrompt] = useState(node?.data?.prompt || '');
  const [systemPrompt, setSystemPrompt] = useState(node?.data?.system_prompt || '');
  const [provider, setProvider] = useState(node?.data?.provider || '');
  const [modelName, setModelName] = useState(node?.data?.model || '');
  const [apiKey, setApiKey] = useState(node?.data?.api_key || '');

  // 代码节点专用
  const [filePath, setFilePath] = useState(node?.data?.file_path || '');
  const [description, setDescription] = useState(node?.data?.description || '');

  useEffect(() => {
    if (node) {
      setPrompt(node.data?.prompt || '');
      setSystemPrompt(node.data?.system_prompt || '');
      setProvider(node.data?.provider || '');
      setModelName(node.data?.model || '');
      setApiKey(node.data?.api_key || '');
      setFilePath(node.data?.file_path || '');
      setDescription(node.data?.description || '');
    }
  }, [nodeId, node]);

  const updateNodeData = useCallback(
    (key: string, value: any) => {
      setNodes((nds) =>
        nds.map((n) =>
          n.id === nodeId
            ? { ...n, data: { ...n.data, [key]: value } }
            : n,
        ),
      );
    },
    [nodeId, setNodes],
  );

  if (!node) {
    return (
      <div className="panel-content">
        <div style={{ color: '#888', fontSize: 13 }}>选择节点以配置</div>
      </div>
    );
  }

  return (
    <>
      <div className="panel-header">
        配置: {nodeId}
        <span style={{ fontSize: 11, color: '#888', marginLeft: 8 }}>
          ({node.type})
        </span>
      </div>
      <div className="panel-content" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {node.type === 'prompt' && (
          <>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              <label style={labelStyle}>System Prompt（可选）</label>
              <textarea
                value={systemPrompt}
                onChange={(e) => { setSystemPrompt(e.target.value); updateNodeData('system_prompt', e.target.value); }}
                rows={3}
                style={textareaStyle}
                placeholder="设置系统提示词..."
              />
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              <label style={labelStyle}>Prompt 模板</label>
              <textarea
                value={prompt}
                onChange={(e) => { setPrompt(e.target.value); updateNodeData('prompt', e.target.value); }}
                rows={6}
                style={textareaStyle}
                placeholder="输入提示词，使用 {{node_id}} 引用上游输出..."
              />
            </div>

            <ModelSelector
              provider={provider}
              modelName={modelName}
              onChange={(p, m) => { setProvider(p); setModelName(m); updateNodeData('provider', p); updateNodeData('model', m); }}
            />

            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              <label style={labelStyle}>API Key（可选，留空使用全局配置）</label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => { setApiKey(e.target.value); updateNodeData('api_key', e.target.value); }}
                style={inputStyle}
                placeholder="sk-..."
              />
            </div>
          </>
        )}

        {node.type === 'code' && (
          <>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              <label style={labelStyle}>任务描述</label>
              <textarea
                value={description}
                onChange={(e) => { setDescription(e.target.value); updateNodeData('description', e.target.value); }}
                rows={3}
                style={textareaStyle}
                placeholder="描述代码任务..."
              />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              <label style={labelStyle}>文件路径</label>
              <input
                type="text"
                value={filePath}
                onChange={(e) => { setFilePath(e.target.value); updateNodeData('file_path', e.target.value); }}
                style={inputStyle}
                placeholder="C:\projects\paper\experiment.py"
              />
            </div>
            <button
              onClick={async () => {
                const res = await fetch('/api/vscode/open', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ file_path: filePath }),
                });
                const data = await res.json();
                alert(data.success ? '已打开 VS Code' : '打开失败: ' + data.error);
              }}
              style={{
                padding: '8px 16px',
                background: '#0078d4',
                color: '#fff',
                border: 'none',
                borderRadius: 6,
                cursor: 'pointer',
              }}
            >
              在 VS Code 中打开
            </button>
          </>
        )}

        {node.type === 'output' && (
          <div style={{ color: '#888', fontSize: 13 }}>
            输出节点会自动收集上游节点的输出内容。
          </div>
        )}

        {node.type === 'start' && (
          <div style={{ color: '#888', fontSize: 13 }}>
            工作流的起点节点。
          </div>
        )}
      </div>
    </>
  );
}

const labelStyle: React.CSSProperties = {
  fontSize: 12,
  fontWeight: 600,
  color: '#555',
};

const textareaStyle: React.CSSProperties = {
  padding: '8px',
  borderRadius: 6,
  border: '1px solid #d0d0d0',
  fontSize: 13,
  fontFamily: 'monospace',
  resize: 'vertical',
};

const inputStyle: React.CSSProperties = {
  padding: '6px 8px',
  borderRadius: 6,
  border: '1px solid #d0d0d0',
  fontSize: 13,
};
```

- [ ] **Step 3: 编写 `ChatPanel.tsx`**

```tsx
import { useState, useRef, useEffect } from 'react';

interface Message {
  role: string;
  content: string;
}

interface Props {
  messages: Message[];
  onSend?: (message: string) => void;
}

export default function ChatPanel({ messages, onSend }: Props) {
  const [input, setInput] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    onSend?.(input);
    setInput('');
  };

  return (
    <>
      <div className="panel-header">对话记录</div>
      <div
        className="panel-content"
        style={{ display: 'flex', flexDirection: 'column', gap: 8 }}
      >
        {messages.length === 0 && (
          <div style={{ color: '#888', fontSize: 13 }}>
            运行工作流后，对话记录将显示在这里
          </div>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              padding: '8px 12px',
              borderRadius: 8,
              background: msg.role === 'user' ? '#e0e7ff' : '#f5f5f5',
              fontSize: 13,
              lineHeight: 1.5,
            }}
          >
            <div style={{ fontWeight: 600, fontSize: 11, color: '#888', marginBottom: 4 }}>
              {msg.role === 'user' ? 'You' : 'AI'}
            </div>
            {msg.content}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      {onSend && (
        <div style={{ padding: '8px 12px', borderTop: '1px solid #e0e0e0', display: 'flex', gap: 8 }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="输入消息..."
            style={{
              flex: 1,
              padding: '6px 10px',
              borderRadius: 6,
              border: '1px solid #d0d0d0',
              fontSize: 13,
            }}
          />
          <button
            onClick={handleSend}
            style={{
              padding: '6px 12px',
              background: '#4f46e5',
              color: '#fff',
              border: 'none',
              borderRadius: 6,
              cursor: 'pointer',
            }}
          >
            发送
          </button>
        </div>
      )}
    </>
  );
}
```

- [ ] **Step 4: 验证构建**

Run:
```bash
cd C:\Users\wangd\paper-flow\frontend
npx tsc --noEmit
```

Expected: 无 TypeScript 错误

- [ ] **Step 5: Commit**

```bash
git -C C:\Users\wangd\paper-flow add frontend/src/components/NodeConfigPanel.tsx frontend/src/components/ChatPanel.tsx frontend/src/components/ModelSelector.tsx
git -C C:\Users\wangd\paper-flow commit -m "feat: add node config panel, chat panel, and model selector"
```

---

### Task 10: Electron 桌面壳 + 系统托盘 + VS Code IPC

**Files:**
- Create: `electron/package.json`
- Create: `electron/main.js`
- Create: `electron/preload.js`

- [ ] **Step 1: 编写 `electron/package.json`**

```json
{
  "name": "paper-flow-desktop",
  "version": "0.1.0",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "dev": "set NODE_ENV=development && electron ."
  },
  "dependencies": {
    "electron": "^33.3.1"
  }
}
```

- [ ] **Step 2: 编写 `electron/main.js`**

```js
const { app, BrowserWindow, Tray, Menu, nativeImage, ipcMain, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow = null;
let tray = null;
let backendProcess = null;

const BACKEND_URL = 'http://127.0.0.1:8765';
const FRONTEND_DEV_URL = 'http://localhost:5173';
const isDev = process.env.NODE_ENV === 'development';

function startBackend() {
  const backendDir = path.join(__dirname, '..', 'backend');
  const pythonPath = path.join(backendDir, '.venv', 'Scripts', 'python.exe');
  backendProcess = spawn(pythonPath, ['-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8765'], {
    cwd: backendDir,
    stdio: 'pipe',
  });
  backendProcess.stdout.on('data', (data) => console.log(`[Backend] ${data}`));
  backendProcess.stderr.on('data', (data) => console.log(`[Backend] ${data}`));
  backendProcess.on('error', (err) => console.error('Backend error:', err));
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 600,
    title: 'PaperFlow - 科研论文写作工作流',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    show: false,
  });

  mainWindow.loadURL(isDev ? FRONTEND_DEV_URL : `file://${path.join(__dirname, '..', 'frontend', 'dist', 'index.html')}`);

  mainWindow.once('ready-to-show', () => mainWindow.show());

  if (isDev) {
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  }

  mainWindow.on('close', (event) => {
    if (!app.isQuitting) {
      event.preventDefault();
      mainWindow.hide();
    }
  });
}

function createTray() {
  // 创建一个简单的图标（使用原生图像）
  const iconSize = 16;
  const icon = nativeImage.createEmpty();

  // 在实际发布时替换为真实图标文件
  const iconPath = path.join(__dirname, 'icon.png');
  try {
    tray = new Tray(iconPath);
  } catch {
    // 如果图标文件不存在，创建一个简单的
    tray = new Tray(nativeImage.createFromBuffer(
      Buffer.from('iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA', 'base64'),
      { width: 16, height: 16 }
    ));
  }

  const contextMenu = Menu.buildFromTemplate([
    {
      label: '打开 PaperFlow',
      click: () => mainWindow?.show(),
    },
    { type: 'separator' },
    {
      label: '退出',
      click: () => {
        app.isQuitting = true;
        app.quit();
      },
    },
  ]);

  tray.setToolTip('PaperFlow - 科研论文写作工作流');
  tray.setContextMenu(contextMenu);
  tray.on('double-click', () => mainWindow?.show());
}

// IPC: 打开 VS Code
ipcMain.handle('vscode:open', async (_, args) => {
  const { filePath, folderPath } = args;
  try {
    if (folderPath) {
      await shell.openExternal(`vscode://file/${folderPath}`);
    } else if (filePath) {
      await shell.openExternal(`vscode://file/${filePath}`);
    }
    return { success: true };
  } catch (err) {
    return { success: false, error: err.message };
  }
});

app.whenReady().then(() => {
  startBackend();
  createWindow();
  createTray();

  app.on('activate', () => {
    if (mainWindow) mainWindow.show();
  });
});

app.on('window-all-closed', () => {
  // Windows 下不退出
});

app.on('before-quit', () => {
  app.isQuitting = true;
  if (backendProcess) {
    backendProcess.kill();
  }
});
```

- [ ] **Step 3: 编写 `electron/preload.js`**

```js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  openInVSCode: (args) => ipcRenderer.invoke('vscode:open', args),
  platform: process.platform,
});
```

- [ ] **Step 4: 安装 Electron 依赖**

Run:
```bash
cd C:\Users\wangd\paper-flow\electron
npm install
```

Expected: electron 安装成功

- [ ] **Step 5: 验证 Electron 启动（不显示窗口，只验证无报错）**

Run:
```bash
cd C:\Users\wangd\paper-flow\electron
npx electron --version
```

Expected: 输出 Electron 版本号

- [ ] **Step 6: Commit**

```bash
git -C C:\Users\wangd\paper-flow add electron/
git -C C:\Users\wangd\paper-flow commit -m "feat: add Electron desktop shell with system tray and VS Code IPC"
```

---

### Task 11: 开机自启整合 + VS Code API 端点

**Files:**
- Modify: `backend/main.py`（添加 `/api/vscode/open` 端点）
- Modify: `backend/api/__init__.py`
- Create: `electron/icon.png`（占位）

- [ ] **Step 1: 在后端添加 VS Code API 端点**

在 `backend/main.py` 的 `app.include_router` 后添加：

```python
from fastapi import FastAPI
from pydantic import BaseModel
from services.vscode import open_file, open_folder


# ...（现有代码）...

class VSCodeOpenRequest(BaseModel):
    file_path: str | None = None
    folder_path: str | None = None


@app.post("/api/vscode/open")
async def vscode_open(req: VSCodeOpenRequest):
    if req.folder_path:
        return open_folder(req.folder_path)
    if req.file_path:
        return open_file(req.file_path)
    return {"success": False, "error": "file_path or folder_path required"}
```

- [ ] **Step 2: 添加 Windows 开机自启注册（替代之前的手动 .bat）**

创建 `scripts/register-startup.py`:

```python
"""注册 PaperFlow 到 Windows 开机自启"""
import os
import sys
import subprocess
from pathlib import Path

def register():
    project_root = Path(__file__).parent.parent
    electron_dir = project_root / "electron"
    startup_script = electron_dir / "start-paperflow.bat"

    # 创建启动批处理
    bat_content = f"""@echo off
cd /d {electron_dir}
start "" "{electron_dir}\\node_modules\\.bin\\electron.cmd" "{electron_dir}"
"""
    startup_script.write_text(bat_content)

    # 添加到 Startup 文件夹
    startup_dir = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    shortcut_path = startup_dir / "PaperFlow.lnk"

    # 用 PowerShell 创建快捷方式
    ps_cmd = f"""
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
    $Shortcut.TargetPath = '{startup_script}'
    $Shortcut.WorkingDirectory = '{electron_dir}'
    $Shortcut.Save()
    """
    subprocess.run(["powershell", "-Command", ps_cmd], check=True)
    print(f"PaperFlow 已添加到开机自启: {shortcut_path}")

def unregister():
    startup_dir = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    shortcut_path = startup_dir / "PaperFlow.lnk"
    if shortcut_path.exists():
        shortcut_path.unlink()
        print("已移除开机自启")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "unregister":
        unregister()
    else:
        register()
```

- [ ] **Step 3: 验证注册脚本**

Run:
```bash
cd C:\Users\wangd\paper-flow
.venv\Scripts\python scripts\register-startup.py
```

Expected: `PaperFlow 已添加到开机自启: ...`（可随后移除）

Run:
```bash
cd C:\Users\wangd\paper-flow
.venv\Scripts\python scripts\register-startup.py unregister
```

Expected: `已移除开机自启`

- [ ] **Step 4: Commit**

```bash
git -C C:\Users\wangd\paper-flow add backend/main.py scripts/register-startup.py
git -C C:\Users\wangd\paper-flow commit -m "feat: add VS Code API endpoint and Windows auto-start registration"
```

---

### Task 12: 论文写作工作流模板

**Files:**
- Create: `frontend/src/templates/paper-workflow.ts`
- Modify: `frontend/src/components/Toolbar.tsx`（添加模板加载功能）

- [ ] **Step 1: 创建论文写作模板**

```ts
import { Node, Edge } from 'reactflow';

export const PaperWritingWorkflow: { nodes: Node[]; edges: Edge[] } = {
  name: '科研论文写作工作流',
  nodes: [
    {
      id: 'start',
      type: 'start',
      position: { x: 400, y: 0 },
      data: { label: 'Start', prompt: '开始论文写作' },
    },
    {
      id: 'lit-review',
      type: 'prompt',
      position: { x: 200, y: 150 },
      data: {
        label: 'Literature Review',
        prompt: '请帮我总结以下论文的核心贡献和方法论：\n\n{{start}}\n\n要求：\n1. 每篇论文用3句话总结\n2. 指出共同点和差异\n3. 识别研究空白',
        system_prompt: '你是一个顶级的科研助手，擅长文献综述。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'outline',
      type: 'prompt',
      position: { x: 600, y: 150 },
      data: {
        label: 'Outline',
        prompt: '基于以下文献综述结果，请为研究论文设计一个详细的提纲：\n\n{{lit-review}}\n\n论文主题：请根据上下文推断\n\n提纲要求：\n1. 包含Introduction, Method, Experiments, Results, Discussion, Conclusion\n2. 每个部分列出3-5个子要点\n3. 标注每个部分预期使用的模型和方法',
        system_prompt: '你是一个顶级的科研写作助手，擅长论文结构设计。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'code-exp',
      type: 'code',
      position: { x: 200, y: 320 },
      data: {
        label: 'Experiments Code',
        description: '根据论文提纲实现实验代码',
        file_path: 'C:\\Users\\wangd\\projects\\paper\\experiments\\main.py',
      },
    },
    {
      id: 'method-writing',
      type: 'prompt',
      position: { x: 600, y: 320 },
      data: {
        label: 'Method Section',
        prompt: '请根据以下提纲和实验代码，撰写论文的 Method 部分：\n\n提纲：\n{{outline}}\n\n代码：\n{{code-exp}}\n\n要求：\n1. 详细描述方法设计\n2. 包含公式和算法描述（LaTeX格式）\n3. 说明实验设置和参数',
        system_prompt: '你是一个顶级的科研论文写作助手，擅长方法部分写作。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'results-writing',
      type: 'prompt',
      position: { x: 400, y: 480 },
      data: {
        label: 'Results & Discussion',
        prompt: '请根据以下方法描述和实验结果，撰写论文的Results与Discussion部分：\n\n方法：\n{{method-writing}}\n\n要求：\n1. 客观呈现实验结果\n2. 分析和解释发现\n3. 与现有工作进行对比\n4. 指出局限性和未来方向',
        system_prompt: '你是一个顶级的科研论文写作助手。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'review',
      type: 'prompt',
      position: { x: 600, y: 620 },
      data: {
        label: 'Review & Polish',
        prompt: '请对以下论文草稿进行全面审阅和润色：\n\nIntroduction: 请根据已有内容撰写\nRelated Work: {{lit-review}}\nMethod: {{method-writing}}\nResults: {{results-writing}}\n\n审阅要求：\n1. 检查逻辑连贯性\n2. 优化学术表达\n3. 确保各部分风格一致\n4. 检查LaTeX公式正确性',
        system_prompt: '你是一个顶级的论文审稿助手，擅长学术写作润色。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'abstract-title',
      type: 'prompt',
      position: { x: 400, y: 760 },
      data: {
        label: 'Abstract & Title',
        prompt: '基于以下完整的论文内容，请生成标题和摘要：\n\n论文全文：\n{{review}}\n\n要求：\n1. 提供3个候选标题\n2. 摘要控制在200-300字\n3. 包含：背景、问题、方法、结果、结论',
        system_prompt: '你是一个顶级的科研写作助手。请用中文回复。',
        provider: 'claude',
        model: 'claude-sonnet-4-20250514',
      },
    },
    {
      id: 'final-output',
      type: 'output',
      position: { x: 400, y: 900 },
      data: { label: 'Final Output', format: 'markdown' },
    },
  ],
  edges: [
    { id: 'e-start-lit', source: 'start', target: 'lit-review' },
    { id: 'e-lit-outline', source: 'lit-review', target: 'outline' },
    { id: 'e-outline-code', source: 'outline', target: 'code-exp' },
    { id: 'e-outline-method', source: 'outline', target: 'method-writing' },
    { id: 'e-code-method', source: 'code-exp', target: 'method-writing' },
    { id: 'e-method-results', source: 'method-writing', target: 'results-writing' },
    { id: 'e-results-review', source: 'results-writing', target: 'review' },
    { id: 'e-lit-review', source: 'lit-review', target: 'review' },
    { id: 'e-method-review', source: 'method-writing', target: 'review' },
    { id: 'e-review-abstract', source: 'review', target: 'abstract-title' },
    { id: 'e-abstract-output', source: 'abstract-title', target: 'final-output' },
  ],
};
```

- [ ] **Step 2: 修改 Toolbar 添加加载模板按钮**

在 `Toolbar.tsx` 中添加：

```tsx
import { PaperWritingWorkflow } from '../templates/paper-workflow';

// 在组件内部添加:
const handleLoadTemplate = () => {
  const { nodes, edges } = PaperWritingWorkflow;
  // 通过 ReactFlow 实例设置节点和边
  const setNodes = (window as any).__setWorkflowNodes;
  const setEdges = (window as any).__setWorkflowEdges;
  if (setNodes && setEdges) {
    setNodes([...nodes]);
    setEdges([...edges]);
  }
};
```

并在 WorkflowEditor 中暴露 `__setWorkflowNodes` 和 `__setWorkflowEdges`：

```tsx
// 在 WorkflowEditor 组件内添加
(window as any).__setWorkflowNodes = setNodes;
(window as any).__setWorkflowEdges = setEdges;
```

在 Toolbar 的 JSX 中添加按钮：

```tsx
<button onClick={handleLoadTemplate}>
  📋 论文模板
</button>
```

- [ ] **Step 3: 验证 TypeScript 编译**

Run:
```bash
cd C:\Users\wangd\paper-flow\frontend
npx tsc --noEmit
```

Expected: 无 TypeScript 错误

- [ ] **Step 4: Commit**

```bash
git -C C:\Users\wangd\paper-flow add frontend/src/templates/
git -C C:\Users\wangd\paper-flow commit -m "feat: add paper writing workflow template"
```

---

### Task 13: 端到端集成测试

**Files:**
- Create: `scripts/test-e2e.bat`
- No code changes — validate that backend + frontend start and communicate

- [ ] **Step 1: 编写集成测试脚本 `scripts/test-e2e.bat`**

```bat
@echo off
echo PaperFlow E2E Test
echo ==================
echo.

:: 1. 启动后端
echo [1/4] Starting backend...
start "PaperFlow-Backend" /B cmd /c "cd /d %~dp0..\backend && .venv\Scripts\python -m uvicorn main:app --host 127.0.0.1 --port 8765 --log-level error"
timeout /t 3 /nobreak >nul

:: 2. 测试 health endpoint
echo [2/4] Testing health API...
curl -s http://127.0.0.1:8765/api/health
if %ERRORLEVEL% NEQ 0 (
    echo FAILED: Backend not responding
    goto :cleanup
)
echo.

:: 3. 测试 workflow CRUD
echo [3/4] Testing workflow API...
curl -s -X POST http://127.0.0.1:8765/api/workflows -H "Content-Type: application/json" -d "{\"name\":\"E2E Test\",\"nodes\":[],\"edges\":[]}"
echo.
curl -s http://127.0.0.1:8765/api/workflows
echo.

:: 4. 测试前端构建
echo [4/4] Checking frontend build...
cd /d %~dp0..\frontend
call npx tsc --noEmit
if %ERRORLEVEL% EQU 0 (
    echo Frontend TypeScript check: PASSED
) else (
    echo Frontend TypeScript check: FAILED
)

:cleanup
:: 停止后端
echo.
echo Stopping backend...
taskkill /f /fi "WINDOWTITLE eq PaperFlow-Backend" >nul 2>&1
echo Done.
```

- [ ] **Step 2: 运行集成测试**

Run:
```bash
cd C:\Users\wangd\paper-flow
scripts\test-e2e.bat
```

Expected: 所有测试步骤通过

- [ ] **Step 3: Commit**

```bash
git -C C:\Users\wangd\paper-flow add scripts/test-e2e.bat
git -C C:\Users\wangd\paper-flow commit -m "test: add E2E integration test script"
```

---

### Task 14: 最终验证 + README

**Files:**
- Create: `README.md`

- [ ] **Step 1: 编写 README.md**

```markdown
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
```

- [ ] **Step 2: 运行最终验证**

Run:
```bash
cd C:\Users\wangd\paper-flow\backend
.venv\Scripts\python -c "
from storage import init_db
from engine import WorkflowExecutor
from providers.base import LLMProvider
import asyncio

# 验证导入全部正常
print('All imports OK')

# 验证引擎
wf = {
    'id': 'final-test',
    'name': 'Final',
    'nodes': [
        {'id': 'a', 'type': 'start', 'position': {'x': 0, 'y': 0}, 'data': {}},
        {'id': 'b', 'type': 'prompt', 'position': {'x': 200, 'y': 0}, 'data': {'prompt': 'test'}},
        {'id': 'c', 'type': 'output', 'position': {'x': 400, 'y': 0}, 'data': {}},
    ],
    'edges': [
        {'id': 'e1', 'source': 'a', 'target': 'b'},
        {'id': 'e2', 'source': 'b', 'target': 'c'},
    ],
}
executor = WorkflowExecutor()
results = asyncio.run(executor.execute(wf, {}))
assert len(results) == 3
print('Executor: OK')

# 验证拓扑排序
order = executor._topological_sort(['a', 'b', 'c'], [{'source': 'a', 'target': 'b'}, {'source': 'b', 'target': 'c'}])
assert order == ['a', 'b', 'c'], f'Unexpected order: {order}'
print('Topological sort: OK')

# 验证 provider factory
p = LLMProvider.get_provider('claude', 'test-key')
assert p.provider_name == 'claude'
print('Provider factory: OK')

# 验证 providers 列表
for name in ['claude', 'openai', 'gemini', 'deepseek']:
    p = LLMProvider.get_provider(name, 'test-key')
    assert p.provider_name == name
    print(f'  {name}: OK')

print()
print('=== ALL VALIDATIONS PASSED ===')
"
```

Expected: `=== ALL VALIDATIONS PASSED ===`

- [ ] **Step 3: 最终 Commit**

```bash
git -C C:\Users\wangd\paper-flow add README.md
git -C C:\Users\wangd\paper-flow commit -m "docs: add README with setup instructions"
```

---

## 验收清单

- [ ] 后端启动，`/api/health` 返回 `{"status": "ok"}`
- [ ] SQLite 数据库自动初始化，workflow CRUD 正常工作
- [ ] 4 个 LLM 提供商（Claude/GPT/Gemini/DeepSeek）均可正常实例化
- [ ] 工作流执行引擎能按拓扑顺序执行节点
- [ ] VS Code 集成服务能定位并打开 VS Code
- [ ] 前端开发服务器启动，ReactFlow 画布正常显示
- [ ] 拖拽节点到画布，节点之间连线
- [ ] 节点配置面板正确显示不同类型节点的配置项
- [ ] 模型选择器列出所有 4 个提供商
- [ ] 保存/加载工作流持久化到 SQLite
- [ ] 运行工作流，结果传递符合预期
- [ ] Electron 窗口正常显示，系统托盘图标出现
- [ ] VS Code 一键打开（Code 节点）
- [ ] 开机自启注册脚本正常工作
- [ ] 论文写作模板加载后包含完整的写作流程节点
