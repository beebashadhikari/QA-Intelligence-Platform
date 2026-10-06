from sqlalchemy.orm import Session

from backend.app.schemas.release_decision import ReleaseDecision
from backend.app.services.qa_intelligence import analyze_qa_intelligence


def calculate_release_decision(
    db: Session,
    release_version: str,
) -> ReleaseDecision:

    intelligence = analyze_qa_intelligence(
        db=db,
        release_version=release_version,
    )

    release = intelligence.release
    defects = intelligence.defects
    risks = intelligence.risk
    recommendations = intelligence.test_recommendations

    blocking_factors: list[str] = []
    risk_factors: list[str] = []
    required_actions: list[str] = []
    evidence: list[str] = []

    blocking_factors.extend(release.blockers)

    if release.metrics.blocked_tests > 0:
        blocking_factors.append(
            f"{release.metrics.blocked_tests} tests remain blocked."
        )

    if defects.severity_counts.get("critical", 0) > 0:
        blocking_factors.append(
            "Critical-severity defects remain present."
        )

    high_defects = defects.severity_counts.get("high", 0)

    if high_defects > 0:
        risk_factors.append(
            f"{high_defects} high-severity defects remain present."
        )

    for risk in risks:
        if risk.level in {"HIGH", "MEDIUM"}:
            reason_text = ", ".join(risk.reasons)

            if reason_text:
                risk_factors.append(
                    f"{risk.area} has "
                    f"{risk.level.lower()} risk "
                    f"({risk.score}) because "
                    f"{reason_text}"
                )
            else:
                risk_factors.append(
                    f"{risk.area} has "
                    f"{risk.level.lower()} risk "
                    f"({risk.score})."
                )

    failed_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation.status == "failed"
    ]

    blocked_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation.status == "blocked"
    ]

    high_risk_failures = [
        recommendation
        for recommendation in failed_recommendations
        if recommendation.risk_level == "HIGH"
    ]

    high_risk_blocked = [
        recommendation
        for recommendation in blocked_recommendations
        if recommendation.risk_level == "HIGH"
    ]

    for recommendation in failed_recommendations:
        required_actions.append(
            f"Investigate and rerun "
            f"{recommendation.test_case_id} "
            f"({recommendation.title})."
        )

    for recommendation in blocked_recommendations:
        required_actions.append(
            f"Resolve the blocker for "
            f"{recommendation.test_case_id} "
            f"({recommendation.title}) "
            f"and rerun the test."
        )

    if high_risk_failures:
        risk_factors.append(
            f"{len(high_risk_failures)} "
            f"high-risk test recommendation(s) "
            f"are currently failing."
        )
    elif failed_recommendations:
        risk_factors.append(
            f"{len(failed_recommendations)} "
            f"test recommendation(s) "
            f"are currently failing."
        )

    if high_risk_blocked:
        risk_factors.append(
            f"{len(high_risk_blocked)} "
            f"high-risk test recommendation(s) "
            f"are currently blocked."
        )

    if release.blockers:
        status = "NOT_READY"
    elif defects.severity_counts.get("critical", 0) > 0:
        status = "NOT_READY"
    elif (
        release.metrics.blocked_tests > 0
        or high_defects > 0
        or high_risk_failures
        or high_risk_blocked
    ):
        status = "CONDITIONAL"
    else:
        status = "READY"

    if status == "NOT_READY":
        confidence = "HIGH"
    elif blocking_factors:
        confidence = "MEDIUM"
    elif risk_factors:
        confidence = "MEDIUM"
    else:
        confidence = "HIGH"

    if status == "NOT_READY":
        summary = (
            "The release should not proceed because "
            "blocking quality conditions remain unresolved."
        )
    elif status == "CONDITIONAL":
        summary = (
            "The release may proceed only after the "
            "identified risks, failed tests, and blocking "
            "conditions are reviewed and addressed."
        )
    else:
        summary = (
            "Available QA evidence supports proceeding "
            "with the release."
        )

    evidence.append(
        f"Release {release_version} has "
        f"{release.metrics.total_tests} total tests."
    )

    evidence.append(
        f"Test execution: "
        f"{release.metrics.passed_tests} passed, "
        f"{release.metrics.failed_tests} failed, "
        f"{release.metrics.blocked_tests} blocked."
    )

    evidence.append(
        f"Defect analysis identified "
        f"{defects.total_defects} total defects."
    )

    critical_defects = defects.severity_counts.get("critical", 0)

    if critical_defects > 0:
        evidence.append(
            f"{critical_defects} critical-severity "
            f"defects remain present."
        )

    if high_defects > 0:
        evidence.append(
            f"{high_defects} high-severity "
            f"defects remain present."
        )

    evidence.append(
        f"Test Intelligence evaluated "
        f"{len(recommendations)} prioritized "
        f"test recommendations."
    )

    if high_risk_failures:
        evidence.append(
            f"{len(high_risk_failures)} high-risk "
            f"test recommendation(s) are currently failing."
        )

    if high_risk_blocked:
        evidence.append(
            f"{len(high_risk_blocked)} high-risk "
            f"test recommendation(s) are currently blocked."
        )

    return ReleaseDecision(
        release_version=release_version,
        status=status,
        confidence=confidence,
        summary=summary,
        blocking_factors=blocking_factors,
        risk_factors=risk_factors,
        required_actions=required_actions,
        evidence=evidence,
    )