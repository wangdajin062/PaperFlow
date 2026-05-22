"""Tests for the SQLite storage layer."""

import os
import uuid

import pytest

from storage.db import (
    DB_PATH,
    delete_workflow,
    get_workflow,
    init_db,
    list_workflows,
    save_workflow,
)

TEST_DB = "test_paperflow.db"


def _make_wf(**overrides):
    """Helper: create a workflow dict with a generated id."""
    data = {"id": str(uuid.uuid4()), "name": "test", "nodes": [], "edges": []}
    data.update(overrides)
    return data


@pytest.fixture(autouse=True)
async def setup_db():
    """Use a separate test database."""
    original_db = DB_PATH
    import storage.db as db

    db.DB_PATH = TEST_DB

    # Clean up before test
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    await init_db()
    yield

    # Clean up after test
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    db.DB_PATH = original_db


@pytest.mark.asyncio
async def test_save_and_get_workflow():
    wf_data = _make_wf(
        name="Test Workflow",
        description="A test workflow",
        nodes=[
            {"id": "n1", "type": "start", "position": {"x": 0, "y": 0}, "data": {}},
            {
                "id": "n2",
                "type": "prompt",
                "position": {"x": 200, "y": 0},
                "data": {"prompt": "Write paper"},
            },
        ],
        edges=[{"id": "e1", "source": "n1", "target": "n2"}],
    )
    wf_id = wf_data["id"]
    result = await save_workflow(wf_data)
    assert result["id"] == wf_id

    retrieved = await get_workflow(wf_id)
    assert retrieved is not None
    assert retrieved["name"] == "Test Workflow"
    assert len(retrieved["nodes"]) == 2
    assert len(retrieved["edges"]) == 1


@pytest.mark.asyncio
async def test_get_nonexistent_workflow():
    result = await get_workflow("nonexistent-id")
    assert result is None


@pytest.mark.asyncio
async def test_list_workflows():
    await save_workflow(_make_wf(name="WF1"))
    await save_workflow(_make_wf(name="WF2"))

    workflows = await list_workflows()
    assert len(workflows) >= 2
    names = [w["name"] for w in workflows]
    assert "WF1" in names
    assert "WF2" in names


@pytest.mark.asyncio
async def test_delete_workflow():
    wf = _make_wf(name="ToDelete")
    wf_id = wf["id"]
    await save_workflow(wf)
    assert await get_workflow(wf_id) is not None

    deleted = await delete_workflow(wf_id)
    assert deleted is True
    assert await get_workflow(wf_id) is None


@pytest.mark.asyncio
async def test_delete_nonexistent_workflow():
    deleted = await delete_workflow("nonexistent")
    assert deleted is False


@pytest.mark.asyncio
async def test_update_workflow():
    wf = _make_wf(name="Original")
    wf_id = wf["id"]
    await save_workflow(wf)

    result = await save_workflow({
        "id": wf_id,
        "name": "Updated",
        "nodes": [],
        "edges": [],
    })
    assert result["id"] == wf_id

    retrieved = await get_workflow(wf_id)
    assert retrieved["name"] == "Updated"


@pytest.mark.asyncio
async def test_workflow_json_fields():
    """Nodes and edges should be properly serialized/deserialized as JSON."""
    nodes = [
        {"id": "n1", "type": "prompt", "position": {"x": 10.5, "y": 20.3}, "data": {"key": "val"}},
    ]
    edges = [{"id": "e1", "source": "n1", "target": "n2"}]

    wf = _make_wf(name="JSON Test", nodes=nodes, edges=edges)
    wf_id = wf["id"]
    await save_workflow(wf)
    retrieved = await get_workflow(wf_id)

    assert retrieved["nodes"][0]["position"]["x"] == 10.5
    assert retrieved["nodes"][0]["data"]["key"] == "val"
    assert retrieved["edges"][0]["source"] == "n1"
