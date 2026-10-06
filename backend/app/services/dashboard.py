from sqlalchemy.orm import Session

from backend.app.schemas.dashboard import (
    DashboardDecision,
    DashboardDefectSummary,
    DashboardRecommendation,
    DashboardRiskItem,
    DashboardSummary,
    ReleaseReadinessDashboard,
)
from backend.app.services.qa_intelligence import (
    analyze_qa_intelligence,
)
from backend.app.services.release_decision import (
    calculate_release_decision,
)


def build_release_dashboard(
    db: Session,
    release_version: str,
) -> ReleaseReadinessDashboard:

    intelligence = analyze_qa_intelligence(
        db=db,
        release_version=release_version,
    )

    decision = calculate_release_decision(
        db=db,
        release_version=release_version,
    )

    release = intelligence.release
    defects = intelligence.defects
    risks = intelligence.risk
    recommendations = intelligence.test_recommendations
    quality_health = intelligence.quality_health

    high_risk_areas = sum(
        1
        for risk in risks
        if risk.level == "HIGH"
    )

    critical_defects = defects.severity_counts.get(
        "critical",
        0,
    )

    summary = DashboardSummary(
        release_version=release_version,
        readiness_status=decision.status,
        confidence=decision.confidence,
        quality_score=quality_health.score,
        quality_health=quality_health.health,
        pass_rate=release.metrics.pass_rate,
        total_tests=release.metrics.total_tests,
        passed_tests=release.metrics.passed_tests,
        failed_tests=release.metrics.failed_tests,
        blocked_tests=release.metrics.blocked_tests,
        total_defects=defects.total_defects,
        high_risk_areas=high_risk_areas,
        critical_defects=critical_defects,
    )

    dashboard_decision = DashboardDecision(
        status=decision.status,
        confidence=decision.confidence,
        summary=decision.summary,
        blocking_factors=decision.blocking_factors,
        risk_factors=decision.risk_factors,
        required_actions=decision.required_actions,
        evidence=decision.evidence,
    )

    dashboard_risks = [
        DashboardRiskItem(
            area=risk.area,
            score=risk.score,
            level=risk.level,
            reasons=risk.reasons,
            change_id=risk.change_id,
            high_severity_defects=risk.high_severity_defects,
            failed_tests=risk.failed_tests,
            flaky_tests=risk.flaky_tests,
        )
        for risk in risks
    ]

    defect_summary = DashboardDefectSummary(
        total=defects.total_defects,
        critical=defects.severity_counts.get(
            "critical",
            0,
        ),
        high=defects.severity_counts.get(
            "high",
            0,
        ),
        medium=defects.severity_counts.get(
            "medium",
            0,
        ),
        low=defects.severity_counts.get(
            "low",
            0,
        ),
    )

    dashboard_recommendations = [
        DashboardRecommendation(
            test_case_id=recommendation.test_case_id,
            title=recommendation.title,
            module=recommendation.module,
            score=recommendation.score,
            risk_level=recommendation.risk_level,
            status=recommendation.status,
            action=recommendation.action,
        )
        for recommendation in recommendations
    ]

    return ReleaseReadinessDashboard(
        release_version=release_version,
        summary=summary,
        decision=dashboard_decision,
        blockers=release.blockers,
        warnings=release.warnings,
        risks=dashboard_risks,
        defects=defect_summary,
        recommendations=dashboard_recommendations,
    )