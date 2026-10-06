from sqlalchemy.orm import Session

from backend.app.models.change import Change
from backend.app.models.defect import Defect
from backend.app.models.execution import TestExecution
from backend.app.services.risk_engine import calculate_risk


def analyze_risk(
    db: Session,
    release_version: str,
) -> list[dict]:

    changes = (
        db.query(Change)
        .filter(
            Change.release_version == release_version
        )
        .all()
    )

    results = []

    for change in changes:

        defects = (
            db.query(Defect)
            .filter(
                Defect.release_version == release_version,
                Defect.module == change.module,
            )
            .all()
        )

        executions = (
            db.query(TestExecution)
            .filter(
                TestExecution.release_version == release_version,
            )
            .all()
        )

        module_executions = [
            execution
            for execution in executions
            if any(
                execution.test_case_id == test_case_id
                for test_case_id in _test_case_ids_for_module(
                    db,
                    change.module,
                )
            )
        ]

        high_defects = sum(
            1
            for defect in defects
            if defect.severity.lower()
            in {"critical", "high"}
        )

        failed_tests = sum(
            1
            for execution in module_executions
            if execution.status.lower() == "failed"
        )

        flaky_tests = sum(
            1
            for execution in module_executions
            if execution.is_flaky
        )

        historical_defect_score = min(
            len(defects) * 25,
            100,
        )

        failure_score = min(
            failed_tests * 40,
            100,
        )

        instability_score = min(
            flaky_tests * 50,
            100,
        )

        business_criticality_score = (
            100
            if change.business_critical
            else 40
        )

        assessment = calculate_risk(
            area=change.module,
            change_score=change.impact_score,
            historical_defect_score=historical_defect_score,
            business_criticality_score=business_criticality_score,
            failure_score=failure_score,
            instability_score=instability_score,
        )

        results.append(
            {
                "area": assessment.area,
                "score": assessment.score,
                "level": assessment.level,
                "reasons": assessment.reasons,
                "change_id": change.change_id,
                "high_severity_defects": high_defects,
                "failed_tests": failed_tests,
                "flaky_tests": flaky_tests,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results


def _test_case_ids_for_module(
    db: Session,
    module: str,
) -> set[str]:

    from backend.app.models.case import TestCase

    test_cases = (
        db.query(TestCase)
        .filter(TestCase.module == module)
        .all()
    )

    return {
        test.test_case_id
        for test in test_cases
    }