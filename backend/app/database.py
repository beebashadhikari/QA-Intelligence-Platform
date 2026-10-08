from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Anchor the database file to the repository root so the API, MCP server,
# and tests always use the same database, regardless of the current
# working directory. (A CWD-relative path silently created an empty
# database whenever a process started from another directory.)
REPO_ROOT = Path(__file__).resolve().parents[2]

DATABASE_URL = URL.create(
    "sqlite",
    database=str(REPO_ROOT / "qa_intelligence.db"),
)


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()