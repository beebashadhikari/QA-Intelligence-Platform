from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class Defect(Base):
    __tablename__ = "defects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    defect_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    release_id: Mapped[int | None] = mapped_column(
        ForeignKey("releases.id"),
        nullable=True,
    )

    release_version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    release = relationship(
        "Release",
        back_populates="defects",
    )