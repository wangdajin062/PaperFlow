"""Tests for the FastAPI endpoints."""

import os
import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from storage.db import init_db, save_workflow

TEST_DB = "test_api_paperflow.db"


def _make_wf(**overrides):
    data = {"id": str(uuid.uuid4()), "name": "test", "nodes": [], "edges": []}
    data.update(overrides)
    return data


@pytest.fixture(autouse=True)
async def setup_db():
    """Use separate test database for API tests."""
    import storage.db as db
    original_db = db.DB_PATH
    db.DB_PATH = TEST_DB

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    await init_db()
    yield

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    db.DB_PATH = original_db


@pytest.fixture
async def client():
    """Create an async test client."""
    from main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_create_workflow(client):
    resp = await client.post(
        "/api/workflows",
        json={
            "name": "API Test Workflow",
            "description": "Created via API",
            "nodes": [
                {"id": "n1", "type": "start", "position": {"x": 0, "y": 0}, "data": {}},
            ],
            "edges": [],
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["name"] == "API Test Workflow"


@pytest.mark.asyncio
async def test_list_workflows(client):
    wf = _make_wf(name="List Test")
    await save_workflow(wf)
    resp = await client.get("/api/workflows")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    names = [w["name"] for w in data]
    assert "List Test" in names


@pytest.mark.asyncio
async def test_get_workflow_by_id(client):
    wf = _make_wf(name="Get Test")
    wf_id = wf["id"]
    await save_workflow(wf)
    resp = await client.get(f"/api/workflows/{wf_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Get Test"


@pytest.mark.asyncio
async def test_get_nonexistent_workflow(client):
    resp = await client.get("/api/workflows/nonexistent")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_workflow(client):
    wf = _make_wf(name="Delete Test")
    wf_id = wf["id"]
    await save_workflow(wf)
    resp = await client.delete(f"/api/workflows/{wf_id}")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_run_workflow_endpoint(client):
    wf = _make_wf(
        name="Run Test",
        nodes=[
            {"id": "n1", "type": "start", "position": {"x": 0, "y": 0}, "data": {}},
            {
                "id": "n2",
                "type": "prompt",
                "position": {"x": 200, "y": 0},
                "data": {"prompt": "test"},
            },
            {
                "id": "n3",
                "type": "output",
                "position": {"x": 400, "y": 0},
                "data": {},
            },
        ],
        edges=[
            {"id": "e1", "source": "n1", "target": "n2"},
            {"id": "e2", "source": "n2", "target": "n3"},
        ],
    )
    wf_id = wf["id"]
    await save_workflow(wf)
    resp = await client.post("/api/execution/run", json={"workflow_id": wf_id})
    assert resp.status_code == 200
    data = resp.json()
    assert data["workflow_id"] == wf_id
    assert "results" in data
    assert "[Start node]" in data["results"].get("n1", "")


@pytest.mark.asyncio
async def test_run_nonexistent_workflow(client):
    resp = await client.post(
        "/api/execution/run",
        json={"workflow_id": "nonexistent"},
    )
    assert resp.status_code == 404
