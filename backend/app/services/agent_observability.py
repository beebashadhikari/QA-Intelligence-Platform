from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.app.models.agent_run import AgentRun
from backend.app.models.agent_tool_call import AgentToolCall


def create_agent_run(
    db: Session,
    user_request: str,
    release_version: str,
    model: str,
) -> AgentRun:
    run = AgentRun(
        user_request=user_request,
        release_version=release_version,
        model=model,
        started_at=datetime.now(timezone.utc),
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    return run


def record_tool_call(
    db: Session,
    agent_run_id: int,
    tool_name: str,
    arguments: dict,
    duration_ms: float,
    success: bool,
) -> AgentToolCall:
    tool_call = AgentToolCall(
        agent_run_id=agent_run_id,
        tool_name=tool_name,
        arguments=arguments,
        duration_ms=duration_ms,
        success=success,
        created_at=datetime.now(timezone.utc),
    )

    db.add(tool_call)
    db.commit()
    db.refresh(tool_call)

    return tool_call


def complete_agent_run(
    db: Session,
    agent_run_id: int,
    status: str,
    confidence: str,
) -> AgentRun:
    run = (
        db.query(AgentRun)
        .filter(AgentRun.id == agent_run_id)
        .first()
    )

    if run is None:
        raise ValueError(
            f"Agent run {agent_run_id} was not found."
        )

    run.completed_at = datetime.now(timezone.utc)
    run.final_status = status
    run.confidence = confidence

    db.commit()
    db.refresh(run)

    return run