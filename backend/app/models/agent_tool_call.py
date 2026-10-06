from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class AgentToolCall(Base):
    __tablename__ = "agent_tool_calls"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    agent_run_id: Mapped[int] = mapped_column(
        ForeignKey("agent_runs.id"),
        nullable=False,
        index=True,
    )

    tool_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    arguments: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    duration_ms: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    agent_run = relationship(
        "AgentRun",
        back_populates="tool_calls",
    )