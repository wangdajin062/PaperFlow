import uuid
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from storage.db import list_workflows, get_workflow, save_workflow, delete_workflow

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
    wf = {
        "id": payload.id or str(uuid.uuid4()),
        "name": payload.name,
        "description": payload.description,
        "nodes": [n.model_dump() if hasattr(n, 'model_dump') else n for n in payload.nodes],
        "edges": [e.model_dump() if hasattr(e, 'model_dump') else e for e in payload.edges],
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
        "nodes": [n.model_dump() if hasattr(n, 'model_dump') else n for n in payload.nodes],
        "edges": [e.model_dump() if hasattr(e, 'model_dump') else e for e in payload.edges],
    }
    return await save_workflow(wf)


@router.delete("/{workflow_id}")
async def delete(workflow_id: str):
    await delete_workflow(workflow_id)
    return {"ok": True}
