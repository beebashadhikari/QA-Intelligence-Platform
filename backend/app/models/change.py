from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base


class Change(Base):
    __tablename__ = "changes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    change_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    release_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    impact_score: Mapped[float] = mapped_column(
        nullable=False,
    )

    business_critical: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )