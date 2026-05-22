import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from engine import WorkflowExecutor
from providers.base import LLMProvider
from storage.db import get_workflow

router = APIRouter(prefix="/api/execution", tags=["execution"])


class ExecuteRequest(BaseModel):
    workflow_id: str
    provider_overrides: dict[str, dict] = {}


@router.post("/run")
async def run_workflow(req: ExecuteRequest):
    wf_data = await get_workflow(req.workflow_id)
    if not wf_data:
        raise HTTPException(404, "Workflow not found")

    # Build provider map
    provider_map = {}
    for n in wf_data.get("nodes", []):
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
    return {"ok": True}
