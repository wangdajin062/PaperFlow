import logging
from collections import defaultdict, deque
from typing import Any

from providers.base import LLMProvider

from .context import ExecutionContext
from .nodes import WorkflowNode

logger = logging.getLogger(__name__)


def _get_edge_source(e: Any) -> str:
    return e["source"] if isinstance(e, dict) else e.source


def _get_edge_target(e: Any) -> str:
    return e["target"] if isinstance(e, dict) else e.target


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
        provider: LLMProvider | None = None,
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
            logger.warning("Prompt node %s has no provider; returning mock output", node.id)
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

    def _topological_sort(self, node_ids: list[str], edges: list[Any]) -> list[str]:
        in_degree = {nid: 0 for nid in node_ids}
        adj = defaultdict(list)

        for e in edges:
            src, tgt = _get_edge_source(e), _get_edge_target(e)
            adj[src].append(tgt)
            in_degree[tgt] = in_degree.get(tgt, 0) + 1

        queue = deque([nid for nid, deg in in_degree.items() if deg == 0])
        result = []

        while queue:
            nid = queue.popleft()
            result.append(nid)
            for neighbor in adj[nid]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(node_ids):
            raise ValueError(
                "Workflow graph contains a cycle; cannot execute. "
                f"Processed {len(result)}/{len(node_ids)} nodes."
            )

        return result
