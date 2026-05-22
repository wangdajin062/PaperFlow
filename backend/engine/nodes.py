
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
    source_handle: str | None = None
    target_handle: str | None = None


class WorkflowDef(BaseModel):
    id: str
    name: str
    description: str = ""
    nodes: list[WorkflowNode] = []
    edges: list[WorkflowEdge] = []
