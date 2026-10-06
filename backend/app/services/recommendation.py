from sqlalchemy.orm import Session

from backend.app.models.case import TestCase
from backend.app.models.defect import Defect
from backend.app.models.execution import TestExecution


def recommend_tests(
    db: Session,
    release_version: str,
) -> list[dict]:
    executions = (
        db.query(TestExecution)
        .filter(
            TestExecution.release_version == release_version
        )
        .all()
    )

    defects = (
        db.query(Defect)
        .filter(
            Defect.release_version == release_version
        )
        .all()
    )

    # Only consider test cases that belong to the
    # selected release through their executions.
    test_case_ids = {
        execution.test_case_id
        for execution in executions
    }

    if not test_case_ids:
        return []

    test_cases = (
        db.query(TestCase)
        .filter(
            TestCase.test_case_id.in_(test_case_ids)
        )
        .all()
    )

    failed_test_ids = {
        execution.test_case_id
        for execution in executions
        if execution.status == "failed"
    }

    blocked_executions = {
        execution.test_case_id: execution
        for execution in executions
        if execution.status == "blocked"
    }

    flaky_test_ids = {
        execution.test_case_id
        for execution in executions
        if execution.is_flaky
    }

    high_risk_modules = {
        defect.module
        for defect in defects
        if defect.severity in {"critical", "high"}
    }

    recommendations = []

    for test in test_cases:
        score = 0
        reasons = []

        execution = blocked_executions.get(
            test.test_case_id
        )

        if test.module in high_risk_modules:
            score += 40
            reasons.append(
                "Module has a critical/high-severity defect."
            )

        if test.test_case_id in failed_test_ids:
            score += 35
            reasons.append(
                "Test has failed in the current release."
            )

        if execution is not None:
            score += 20
            reasons.append(
                "Test is currently blocked."
            )

        if test.test_case_id in flaky_test_ids:
            score += 15
            reasons.append(
                "Test has shown instability."
            )

        if test.priority == "critical":
            score += 10
            reasons.append(
                "Test is business-critical."
            )

        if score == 0:
            continue

        if score >= 75:
            risk_level = "HIGH"
        elif score >= 50:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        if execution is not None:
            action = (
                "Resolve the blocking condition and then rerun the test."
            )

            blocking_reason = (
                execution.failure_reason
                or "Blocking condition was not specified."
            )

        elif test.test_case_id in failed_test_ids:
            action = (
                "Investigate the failure and rerun "
                "the test after corrective action."
            )

            blocking_reason = None

        elif test.test_case_id in flaky_test_ids:
            action = (
                "Investigate test instability and "
                "rerun the test to confirm the result."
            )

            blocking_reason = None

        else:
            action = (
                "Prioritize execution of this test "
                "because of the identified risk."
            )

            blocking_reason = None

        recommendations.append(
            {
                "test_case_id": test.test_case_id,
                "title": test.title,
                "module": test.module,
                "score": score,
                "risk_level": risk_level,
                "reasons": reasons,
                "status": (
                    execution.status
                    if execution is not None
                    else (
                        "failed"
                        if test.test_case_id in failed_test_ids
                        else "recommended"
                    )
                ),
                "action": action,
                "blocking_reason": blocking_reason,
            }
        )

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return recommendations