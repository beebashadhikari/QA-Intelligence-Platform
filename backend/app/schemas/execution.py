from enum import Enum

from pydantic import BaseModel


class ExecutionStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class TestExecution(BaseModel):
    test_case_id: str
    release_version: str

    status: ExecutionStatus

    environment: str | None = None
    duration_seconds: float | None = None

    is_flaky: bool = False
    failure_reason: str | None = None