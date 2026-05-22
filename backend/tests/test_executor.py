"""Tests for the workflow execution engine."""

import pytest

from engine.context import ExecutionContext
from engine.executor import WorkflowExecutor
from engine.nodes import WorkflowNode


class TestWorkflowExecutor:
    """Test the WorkflowExecutor class."""

    @pytest.mark.asyncio
    async def test_execute_simple_workflow(self):
        """Execute a Start -> Prompt -> Output workflow."""
        executor = WorkflowExecutor()
        workflow_def = {
            "nodes": [
                {"id": "start", "type": "start", "position": {"x": 0, "y": 0}, "data": {}},
                {
                    "id": "prompt1",
                    "type": "prompt",
                    "position": {"x": 200, "y": 0},
                    "data": {"prompt": "Hello {{start}}", "system_prompt": ""},
                },
                {
                    "id": "output1",
                    "type": "output",
                    "position": {"x": 400, "y": 0},
                    "data": {},
                },
            ],
            "edges": [
                {"id": "e1", "source": "start", "target": "prompt1"},
                {"id": "e2", "source": "prompt1", "target": "output1"},
            ],
        }

        results = await executor.execute(workflow_def, {})
        assert "start" in results
        assert "prompt1" in results
        assert "output1" in results
        assert results["start"] == "[Start node]"
        assert "[Mock response" in results["prompt1"]
        assert "From prompt1" in results["output1"]
        assert "[Start node]" in results["output1"]

    @pytest.mark.asyncio
    async def test_topological_sort_linear(self):
        """Topological sort of a linear graph."""
        executor = WorkflowExecutor()
        order = executor._topological_sort(
            ["a", "b", "c"],
            [
                {"id": "e1", "source": "a", "target": "b"},
                {"id": "e2", "source": "b", "target": "c"},
            ],
        )
        assert order == ["a", "b", "c"]

    @pytest.mark.asyncio
    async def test_topological_sort_diamond(self):
        """Topological sort of a diamond-shaped graph."""
        executor = WorkflowExecutor()
        order = executor._topological_sort(
            ["a", "b", "c", "d"],
            [
                {"id": "e1", "source": "a", "target": "b"},
                {"id": "e2", "source": "a", "target": "c"},
                {"id": "e3", "source": "b", "target": "d"},
                {"id": "e4", "source": "c", "target": "d"},
            ],
        )
        assert order[0] == "a"
        assert order[-1] == "d"
        assert set(order[1:3]) == {"b", "c"}

    @pytest.mark.asyncio
    async def test_cycle_detection(self):
        """Cycle in the graph raises ValueError."""
        executor = WorkflowExecutor()
        with pytest.raises(ValueError, match="contains a cycle"):
            executor._topological_sort(
                ["a", "b", "c"],
                [
                    {"id": "e1", "source": "a", "target": "b"},
                    {"id": "e2", "source": "b", "target": "c"},
                    {"id": "e3", "source": "c", "target": "a"},
                ],
            )

    @pytest.mark.asyncio
    async def test_stop_requested(self):
        """request_stop() halts execution."""
        executor = WorkflowExecutor()
        executor.request_stop()
        result = await executor.execute_node(
            WorkflowNode(id="n1", type="prompt", position={}, data={"prompt": "test"}),
            {},
        )
        assert result == "[Execution stopped]"

    @pytest.mark.asyncio
    async def test_execute_code_node(self):
        """Code node returns VS Code instruction."""
        executor = WorkflowExecutor()
        result = await executor.execute_node(
            WorkflowNode(
                id="n1",
                type="code",
                position={},
                data={"description": "implement algorithm", "file_path": "main.py"},
            ),
            {},
        )
        assert "Code task" in result
        assert "implement algorithm" in result

    @pytest.mark.asyncio
    async def test_execute_unknown_node(self):
        """Unknown node type returns fallback message."""
        executor = WorkflowExecutor()
        result = await executor.execute_node(
            WorkflowNode(id="n1", type="unknown_type", position={}, data={}),
            {},
        )
        assert "Unknown node type" in result

    @pytest.mark.asyncio
    async def test_prompt_template_interpolation(self):
        """Template variables {{node_id}} are replaced with upstream output."""
        executor = WorkflowExecutor()
        result = await executor.execute_node(
            WorkflowNode(
                id="n1",
                type="prompt",
                position={},
                data={"prompt": "Summarize: {{upstream_node}}"},
            ),
            {"upstream_node": "This is a paper about AI."},
        )
        assert "Summarize: This is a paper about AI." in result

    @pytest.mark.asyncio
    async def test_on_node_complete_callback(self):
        """Callback fires for each completed node."""
        executor = WorkflowExecutor()
        completed = []

        async def callback(node_id, output):
            completed.append(node_id)

        await executor.execute(
            {
                "nodes": [
                    {"id": "a", "type": "start", "position": {"x": 0, "y": 0}, "data": {}},
                    {
                        "id": "b",
                        "type": "prompt",
                        "position": {"x": 200, "y": 0},
                        "data": {"prompt": "hi"},
                    },
                ],
                "edges": [{"id": "e1", "source": "a", "target": "b"}],
            },
            {},
            on_node_complete=callback,
        )
        assert completed == ["a", "b"]


class TestExecutionContext:
    """Test the ExecutionContext class."""

    def test_set_and_get(self):
        ctx = ExecutionContext()
        ctx.set_node_output("n1", "output1")
        assert ctx.get_node_output("n1") == "output1"
        assert ctx.get_node_output("nonexistent") is None

    def test_get_upstream_outputs(self):
        ctx = ExecutionContext()
        ctx.set_node_output("a", "result_a")
        ctx.set_node_output("b", "result_b")
        ctx.set_node_output("c", "result_c")

        edges = [
            {"id": "e1", "source": "a", "target": "d"},
            {"id": "e2", "source": "b", "target": "d"},
        ]
        upstream = ctx.get_upstream_outputs("d", edges)
        assert upstream == {"a": "result_a", "b": "result_b"}

    def test_get_all_outputs(self):
        ctx = ExecutionContext()
        ctx.set_node_output("n1", "out1")
        ctx.set_node_output("n2", "out2")
        assert ctx.get_all_outputs() == {"n1": "out1", "n2": "out2"}

    def test_get_all_outputs_is_copy(self):
        ctx = ExecutionContext()
        ctx.set_node_output("n1", "out1")
        outputs = ctx.get_all_outputs()
        outputs["n2"] = "modified"
        assert ctx.get_node_output("n2") is None


class TestWorkflowNode:
    """Test WorkflowNode model."""

    def test_create_prompt_node(self):
        node = WorkflowNode(
            id="n1",
            type="prompt",
            position={"x": 100, "y": 200},
            data={"prompt": "Write a paper", "provider": "claude"},
        )
        assert node.id == "n1"
        assert node.type == "prompt"
        assert node.data["provider"] == "claude"

    def test_default_data(self):
        node = WorkflowNode(id="n1", type="start", position={"x": 0, "y": 0})
        assert node.data == {}

    def test_workflow_def(self):
        from engine.nodes import WorkflowDef, WorkflowEdge

        wf = WorkflowDef(
            id="wf1",
            name="test workflow",
            nodes=[
                WorkflowNode(id="n1", type="start", position={"x": 0, "y": 0}),
            ],
            edges=[
                WorkflowEdge(id="e1", source="n1", target="n2"),
            ],
        )
        assert wf.name == "test workflow"
        assert len(wf.nodes) == 1
