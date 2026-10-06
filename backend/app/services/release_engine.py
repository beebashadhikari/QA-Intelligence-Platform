from backend.app.schemas.release import ReleaseData


def evaluate_release(release: ReleaseData) -> dict:
    blockers: list[str] = []
    warnings: list[str] = []

    # Critical defects are release blockers.
    if release.critical_defects > 0:
        blockers.append(
            "Open critical defects exist."
        )

    # Smoke testing must pass.
    if release.smoke_status.lower() != "passed":
        blockers.append(
            "Smoke testing has not passed."
        )

    # Blocked tests are warnings for now.
    if release.blocked_tests > 0:
        warnings.append(
            f"{release.blocked_tests} tests remain blocked."
        )

    # High-severity defects require review.
    if release.high_defects > 0:
        warnings.append(
            f"{release.high_defects} high-severity defects exist."
        )

    # Determine overall release status.
    if blockers:
        status = "NOT_READY"
    elif warnings:
        status = "CONDITIONAL"
    else:
        status = "READY"

    return {
        "release_version": release.release_version,
        "status": status,
        "blockers": blockers,
        "warnings": warnings,
    }