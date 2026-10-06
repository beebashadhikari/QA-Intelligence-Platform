from sqlalchemy.orm import Session

from backend.app.models.release import Release
from backend.app.services.release_metrics import (
    calculate_release_metrics,
)


def analyze_release(
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

    metrics = calculate_release_metrics(
        db,
        release_version,
    )

    blockers: list[str] = []
    warnings: list[str] = []

    if release.critical_defects > 0:
        blockers.append(
            "Open critical defects exist."
        )

    if release.smoke_status.lower() != "passed":
        blockers.append(
            "Smoke testing has not passed."
        )

    if release.blocked_tests > 0:
        warnings.append(
            f"{release.blocked_tests} tests remain blocked."
        )

    if release.high_defects > 0:
        warnings.append(
            f"{release.high_defects} high-severity defects exist."
        )

    if blockers:
        status = "NOT_READY"
    elif warnings:
        status = "CONDITIONAL"
    else:
        status = "READY"

    return {
        "release_version": release.release_version,
        "status": status,
        "metrics": metrics,
        "blockers": blockers,
        "warnings": warnings,
    }