from typing import Any


def _get_edge_source(e: Any) -> str:
    return e["source"] if isinstance(e, dict) else e.source


def _get_edge_target(e: Any) -> str:
    return e["target"] if isinstance(e, dict) else e.target


class ExecutionContext:
    """Cross-node data passing context with global variable support."""

    def __init__(self):
        self._data: dict[str, Any] = {}
        self._globals: dict[str, str] = {}

    def set_global(self, key: str, value: str):
        """Set a global variable available to all nodes."""
        self._globals[key] = value

    def set_node_output(self, node_id: str, output: Any):
        self._data[node_id] = output

    def get_node_output(self, node_id: str) -> Any:
        return self._data.get(node_id)

    def get_all_outputs(self) -> dict[str, Any]:
        return dict(self._data)

    def get_upstream_outputs(self, node_id: str, edges: list) -> dict:
        """Get outputs from upstream nodes, merged with global variables."""
        upstream_ids = {_get_edge_source(e) for e in edges if _get_edge_target(e) == node_id}
        upstream = {uid: self._data.get(uid) for uid in upstream_ids if uid in self._data}
        # Global variables are available to every node, upstream outputs take priority
        return {**self._globals, **upstream}
