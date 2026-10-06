from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_request: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    release_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    final_status: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    confidence: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    tool_calls = relationship(
        "AgentToolCall",
        back_populates="agent_run",
        cascade="all, delete-orphan",
    )