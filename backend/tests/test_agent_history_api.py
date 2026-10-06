from datetime import datetime, timezone

from fastapi.testclient import TestClient

from backend.app.database import SessionLocal
from backend.app.main import app
from backend.app.models.agent_run import AgentRun
from backend.app.models.agent_tool_call import AgentToolCall


client = TestClient(app)


def create_test_run():
    db = SessionLocal()

    run = AgentRun(
        user_request="Test release readiness",
        release_version="2.4.0",
        model="test-model",
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        final_status="CONDITIONAL",
        confidence="MEDIUM",
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    tool_call = AgentToolCall(
        agent_run_id=run.id,
        tool_name="get_release",
        arguments={
            "release_version": "2.4.0",
        },
        duration_ms=12.5,
        success=True,
        created_at=datetime.now(timezone.utc),
    )

    db.add(tool_call)
    db.commit()

    run_id = run.id

    db.close()

    return run_id


def test_get_agent_runs():
    run_id = create_test_run()

    response = client.get("/api/agent/runs")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(
        run["id"] == run_id
        for run in data
    )


def test_get_agent_run():
    run_id = create_test_run()

    response = client.get(
        f"/api/agent/runs/{run_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == run_id
    assert data["release_version"] == "2.4.0"
    assert data["final_status"] == "CONDITIONAL"
    assert data["confidence"] == "MEDIUM"


def test_get_agent_tool_calls():
    run_id = create_test_run()

    response = client.get(
        f"/api/agent/runs/{run_id}/tool-calls"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    tool_call = data[0]

    assert tool_call["agent_run_id"] == run_id
    assert tool_call["tool_name"] == "get_release"
    assert tool_call["success"] is True


def test_get_missing_agent_run():
    response = client.get(
        "/api/agent/runs/999999"
    )

    assert response.status_code == 404


def test_get_tool_calls_for_missing_run():
    response = client.get(
        "/api/agent/runs/999999/tool-calls"
    )

    assert response.status_code == 404