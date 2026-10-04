__test__ = False
from enum import Enum

from pydantic import BaseModel, Field


class TestType(str, Enum):
    FUNCTIONAL = "functional"
    REGRESSION = "regression"
    SMOKE = "smoke"
    INTEGRATION = "integration"
    API = "api"
    PERFORMANCE = "performance"


class TestPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TestCase(BaseModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    module: str = Field(min_length=1)

    test_type: TestType
    priority: TestPriority

    automated: bool = False