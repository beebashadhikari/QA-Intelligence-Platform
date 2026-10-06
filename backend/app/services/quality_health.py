from sqlalchemy.orm import Session

from backend.app.models.case import TestCase
from backend.app.models.defect import Defect
from backend.app.models.execution import TestExecution
from backend.app.models.release import Release


def calculate_quality_health(
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

    executions = (
        db.query(TestExecution)
        .filter(
            TestExecution.release_version
            == release_version
        )
        .all()
    )

    defects = (
        db.query(Defect)
        .filter(
            Defect.release_version
            == release_version
        )
        .all()
    )

    test_cases = db.query(TestCase).all()

    # -------------------------
    # Functional quality
    # -------------------------

    total_executions = len(executions)

    passed_executions = sum(
        1
        for execution in executions
        if execution.status.lower() == "passed"
    )

    functional_score = (
        round(
            (passed_executions / total_executions) * 100,
            2,
        )
        if total_executions
        else 0
    )

    # -------------------------
    # Regression quality
    # -------------------------

    regression_score = (
        100
        if release.regression_status.lower() == "passed"
        else 50
    )

    # -------------------------
    # Defect health
    # -------------------------

    critical = sum(
        1
        for defect in defects
        if defect.severity.lower() == "critical"
        and defect.status.lower()
        not in {"resolved", "closed"}
    )

    high = sum(
        1
        for defect in defects
        if defect.severity.lower() == "high"
        and defect.status.lower()
        not in {"resolved", "closed"}
    )

    defect_score = max(
        0,
        100
        - (critical * 40)
        - (high * 15),
    )

    # -------------------------
    # Automation coverage
    # -------------------------

    automated_tests = sum(
        1
        for test in test_cases
        if test.automated
    )

    automation_score = (
        round(
            (automated_tests / len(test_cases)) * 100,
            2,
        )
        if test_cases
        else 0
    )

    # -------------------------
    # Stability
    # -------------------------

    flaky_tests = sum(
        1
        for execution in executions
        if execution.is_flaky
    )

    stability_score = max(
        0,
        100 - (flaky_tests * 20),
    )

    # -------------------------
    # Overall score
    # -------------------------

    score = round(
        functional_score * 0.25
        + regression_score * 0.25
        + defect_score * 0.20
        + automation_score * 0.15
        + stability_score * 0.15,
        2,
    )

    if score >= 90:
        health = "EXCELLENT"
    elif score >= 80:
        health = "GOOD"
    elif score >= 70:
        health = "FAIR"
    elif score >= 60:
        health = "POOR"
    else:
        health = "CRITICAL"

    return {
        "release_version": release_version,
        "score": score,
        "health": health,
        "components": {
            "functional": functional_score,
            "regression": regression_score,
            "defects": defect_score,
            "automation": automation_score,
            "stability": stability_score,
        },
    }