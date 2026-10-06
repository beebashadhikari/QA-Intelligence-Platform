from sqlalchemy.orm import Session

from backend.app.models.release import Release
from backend.app.services.dashboard import build_release_dashboard


def get_release_portfolio(
    db: Session,
) -> list[dict]:

    releases = (
        db.query(Release)
        .order_by(Release.id.desc())
        .all()
    )

    portfolio = []

    for release in releases:
        dashboard = build_release_dashboard(
            db,
            release.release_version,
        )

        summary = dashboard.summary

        portfolio.append(
            {
                "release_version": release.release_version,
                "readiness_status": summary.readiness_status,
                "confidence": summary.confidence,
                "quality_score": summary.quality_score,
                "quality_health": summary.quality_health,
                "pass_rate": summary.pass_rate,
                "total_tests": summary.total_tests,
                "passed_tests": summary.passed_tests,
                "failed_tests": summary.failed_tests,
                "blocked_tests": summary.blocked_tests,
                "total_defects": summary.total_defects,
                "critical_defects": summary.critical_defects,
                "high_risk_areas": summary.high_risk_areas,
            }
        )

    return portfolio