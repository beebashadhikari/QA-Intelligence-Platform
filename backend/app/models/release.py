from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base


class Release(Base):
    __tablename__ = "releases"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    release_version: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    total_tests: Mapped[int] = mapped_column(nullable=False)
    passed_tests: Mapped[int] = mapped_column(nullable=False)
    failed_tests: Mapped[int] = mapped_column(nullable=False)
    blocked_tests: Mapped[int] = mapped_column(nullable=False)

    critical_defects: Mapped[int] = mapped_column(nullable=False)
    high_defects: Mapped[int] = mapped_column(nullable=False)
    medium_defects: Mapped[int] = mapped_column(nullable=False)
    low_defects: Mapped[int] = mapped_column(nullable=False)

    regression_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    smoke_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )