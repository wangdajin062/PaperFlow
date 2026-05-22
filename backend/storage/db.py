import json
from pathlib import Path

import aiosqlite

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

def _row_to_workflow(row: aiosqlite.Row) -> dict:
    """Convert a DB row to a workflow dict, deserializing JSON fields."""
    d = dict(row)
    if isinstance(d.get("nodes"), str):
        d["nodes"] = json.loads(d["nodes"])
    if isinstance(d.get("edges"), str):
        d["edges"] = json.loads(d["edges"])
    return d


async def list_workflows() -> list[dict]:
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM workflows ORDER BY updated_at DESC")
        rows = await cursor.fetchall()
        return [_row_to_workflow(r) for r in rows]
    finally:
        await db.close()


async def get_workflow(workflow_id: str) -> dict | None:
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM workflows WHERE id = ?", (workflow_id,))
        row = await cursor.fetchone()
        return _row_to_workflow(row) if row else None
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
        cursor = await db.execute("SELECT * FROM workflows WHERE id = ?", (workflow["id"],))
        row = await cursor.fetchone()
        return _row_to_workflow(row) if row else {}
    finally:
        await db.close()


async def delete_workflow(workflow_id: str) -> bool:
    db = await get_db()
    try:
        cursor = await db.execute("DELETE FROM workflows WHERE id = ?", (workflow_id,))
        await db.commit()
        return cursor.rowcount > 0
    finally:
        await db.close()
