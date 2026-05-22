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
