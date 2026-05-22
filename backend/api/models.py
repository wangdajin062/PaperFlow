import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from storage.db import get_db

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
