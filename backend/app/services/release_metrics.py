from sqlalchemy.orm import Session

from backend.app.models.release import Release
from backend.app.services.metrics import (
    calculate_blocked_rate,
    calculate_failure_rate,
    calculate_pass_rate,
)


def calculate_release_metrics(
    db: Session,
    release_version: str,
) -> dict:
    release = (
        db.query(Release)
        .filter(
            Release.release_version == release_version
        )
        .first()
    )

    if release is None:
        raise ValueError(
            f"Release {release_version} was not found."
        )

    return {
        "release_version": release.release_version,
        "total_tests": release.total_tests,
        "passed_tests": release.passed_tests,
        "failed_tests": release.failed_tests,
        "blocked_tests": release.blocked_tests,
        "pass_rate": calculate_pass_rate(
            release.total_tests,
            release.passed_tests,
        ),
        "failure_rate": calculate_failure_rate(
            release.total_tests,
            release.failed_tests,
        ),
        "blocked_rate": calculate_blocked_rate(
            release.total_tests,
            release.blocked_tests,
        ),
    }