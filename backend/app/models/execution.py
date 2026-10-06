from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class TestExecution(Base):
    __tablename__ = "test_executions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    test_case_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    release_id: Mapped[int] = mapped_column(
        ForeignKey("releases.id"),
        nullable=False,
    )

    release_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    environment: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    duration_seconds: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    is_flaky: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    failure_reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    release = relationship(
        "Release",
        back_populates="executions",
    )