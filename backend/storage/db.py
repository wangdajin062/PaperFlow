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

            CREATE TABLE IF NOT EXISTS refs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL DEFAULT '',
                authors TEXT NOT NULL DEFAULT '[]',
                year TEXT DEFAULT '',
                journal TEXT DEFAULT '',
                volume TEXT DEFAULT '',
                number TEXT DEFAULT '',
                pages TEXT DEFAULT '',
                doi TEXT DEFAULT '',
                abstract TEXT DEFAULT '',
                keywords TEXT NOT NULL DEFAULT '[]',
                url TEXT DEFAULT '',
                ref_type TEXT DEFAULT 'article',
                raw_data TEXT DEFAULT '',
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
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


# --- Reference CRUD ---

import uuid


def _row_to_ref(row: aiosqlite.Row) -> dict:
    d = dict(row)
    for field in ("authors", "keywords"):
        if isinstance(d.get(field), str):
            d[field] = json.loads(d[field])
    return d


async def list_refs() -> list[dict]:
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM refs ORDER BY created_at DESC")
        rows = await cursor.fetchall()
        return [_row_to_ref(r) for r in rows]
    finally:
        await db.close()


async def save_ref(ref: dict) -> dict:
    ref_id = ref.get("id") or str(uuid.uuid4())
    db = await get_db()
    try:
        await db.execute(
            """INSERT INTO refs (id, title, authors, year, journal, volume, number,
                                 pages, doi, abstract, keywords, url, ref_type, raw_data)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 title=excluded.title, authors=excluded.authors,
                 year=excluded.year, journal=excluded.journal,
                 volume=excluded.volume, number=excluded.number,
                 pages=excluded.pages, doi=excluded.doi,
                 abstract=excluded.abstract, keywords=excluded.keywords,
                 url=excluded.url, ref_type=excluded.ref_type""",
            (
                ref_id,
                ref.get("title", ""),
                json.dumps(ref.get("authors", []), ensure_ascii=False),
                ref.get("year", ""),
                ref.get("journal", ""),
                ref.get("volume", ""),
                ref.get("number", ""),
                ref.get("pages", ""),
                ref.get("doi", ""),
                ref.get("abstract", ""),
                json.dumps(ref.get("keywords", []), ensure_ascii=False),
                ref.get("url", ""),
                ref.get("ref_type", "article"),
                ref.get("raw_data", ""),
            ),
        )
        await db.commit()
        cursor = await db.execute("SELECT * FROM refs WHERE id = ?", (ref_id,))
        row = await cursor.fetchone()
        return _row_to_ref(row) if row else {}
    finally:
        await db.close()


async def delete_ref(ref_id: str) -> bool:
    db = await get_db()
    try:
        cursor = await db.execute("DELETE FROM refs WHERE id = ?", (ref_id,))
        await db.commit()
        return cursor.rowcount > 0
    finally:
        await db.close()


async def delete_all_refs() -> int:
    db = await get_db()
    try:
        cursor = await db.execute("DELETE FROM refs")
        await db.commit()
        return cursor.rowcount
    finally:
        await db.close()
