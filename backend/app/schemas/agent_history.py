from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AgentRunSummary(BaseModel):
    id: int
    user_request: str
    release_version: str
    model: str
    started_at: datetime
    completed_at: datetime | None
    final_status: str | None
    confidence: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class AgentToolCallResponse(BaseModel):
    id: int
    agent_run_id: int
    tool_name: str
    arguments: dict
    duration_ms: float
    success: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class AgentRunDetail(AgentRunSummary):
    tool_calls: list[AgentToolCallResponse] = []