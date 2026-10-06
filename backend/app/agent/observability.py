from time import perf_counter

from sqlalchemy.orm import Session

from backend.app.services.agent_observability import (
    complete_agent_run as save_completed_agent_run,
    create_agent_run as save_agent_run,
    record_tool_call as save_tool_call,
)


def create_agent_run(
    db: Session,
    user_request: str,
    release_version: str,
    model: str,
) -> int:
    run = save_agent_run(
        db=db,
        user_request=user_request,
        release_version=release_version,
        model=model,
    )

    return run.id


def record_tool_call(
    db: Session,
    run_id: int,
    tool_name: str,
    arguments: dict,
    duration_ms: float,
    success: bool,
) -> None:
    save_tool_call(
        db=db,
        agent_run_id=run_id,
        tool_name=tool_name,
        arguments=arguments,
        duration_ms=duration_ms,
        success=success,
    )


def complete_agent_run(
    db: Session,
    run_id: int,
    status: str,
    confidence: str,
) -> None:
    save_completed_agent_run(
        db=db,
        agent_run_id=run_id,
        status=status,
        confidence=confidence,
    )


def start_timer() -> float:
    return perf_counter()


def elapsed_ms(start_time: float) -> float:
    return (
        perf_counter() - start_time
    ) * 1000