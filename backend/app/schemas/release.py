from pydantic import BaseModel, Field, model_validator


class ReleaseData(BaseModel):
    release_version: str = Field(min_length=1)

    total_tests: int = Field(ge=0)
    passed_tests: int = Field(ge=0)
    failed_tests: int = Field(ge=0)
    blocked_tests: int = Field(ge=0)

    critical_defects: int = Field(ge=0)
    high_defects: int = Field(ge=0)
    medium_defects: int = Field(ge=0)
    low_defects: int = Field(ge=0)

    regression_status: str
    smoke_status: str

    @model_validator(mode="after")
    def validate_test_counts(self):
        executed_tests = (
            self.passed_tests
            + self.failed_tests
            + self.blocked_tests
        )

        if executed_tests > self.total_tests:
            raise ValueError(
                "Passed + failed + blocked tests "
                "cannot exceed total tests."
            )

        return self