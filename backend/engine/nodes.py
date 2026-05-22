from typing import Optional
from pydantic import BaseModel


class WorkflowNode(BaseModel):
    id: str
    type: str  # "prompt" | "code" | "output" | "start"
    position: dict  # {"x": float, "y": float}
    data: dict = {}  # 节点具体数据


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
