from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.agent.agent import run_qa_agent
from backend.app.database import get_db
from backend.app.models.agent_run import AgentRun
from backend.app.models.agent_tool_call import AgentToolCall
from backend.app.schemas.agent import (
    AgentAnalyzeRequest,
    AgentAnalyzeResponse,
)
from backend.app.schemas.agent_history import (
    AgentRunDetail,
    AgentRunSummary,
    AgentToolCallResponse,
)

router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"],
)


@router.post(
    "/analyze",
    response_model=AgentAnalyzeResponse,
)
def analyze_with_agent(
    request: AgentAnalyzeRequest,
    db: Session = Depends(get_db),
):
    try:
        result = run_qa_agent(
            db=db,
            user_request=request.message,
            release_version=request.release_version,
        )

        return result["answer"]

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get(
    "/runs",
    response_model=list[AgentRunSummary],
)
def get_agent_runs(
    db: Session = Depends(get_db),
):
    runs = (
        db.query(AgentRun)
        .order_by(AgentRun.started_at.desc())
        .all()
    )

    return runs


@router.get(
    "/runs/{run_id}",
    response_model=AgentRunDetail,
)
def get_agent_run(
    run_id: int,
    db: Session = Depends(get_db),
):
    run = (
        db.query(AgentRun)
        .filter(AgentRun.id == run_id)
        .first()
    )

    if run is None:
        raise HTTPException(
            status_code=404,
            detail=f"Agent run {run_id} was not found.",
        )

    return run


@router.get(
    "/runs/{run_id}/tool-calls",
    response_model=list[AgentToolCallResponse],
)
def get_agent_tool_calls(
    run_id: int,
    db: Session = Depends(get_db),
):
    run = (
        db.query(AgentRun)
        .filter(AgentRun.id == run_id)
        .first()
    )

    if run is None:
        raise HTTPException(
            status_code=404,
            detail=f"Agent run {run_id} was not found.",
        )

    tool_calls = (
        db.query(AgentToolCall)
        .filter(
            AgentToolCall.agent_run_id == run_id
        )
        .order_by(AgentToolCall.created_at.asc())
        .all()
    )

    return tool_calls