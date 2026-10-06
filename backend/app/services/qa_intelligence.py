from sqlalchemy.orm import Session

from backend.app.schemas.qa_intelligence import (
    QAIntelligenceResponse,
)
from backend.app.services.defect_analysis import (
    analyze_defects,
)
from backend.app.services.release_analysis import (
    analyze_release,
)
from backend.app.services.recommendation import (
    recommend_tests,
)
from backend.app.services.risk_analysis import (
    analyze_risk,
)
from backend.app.services.quality_health import (
    calculate_quality_health,
)


def analyze_qa_intelligence(
    db: Session,
    release_version: str,
) -> QAIntelligenceResponse:

    release_analysis = analyze_release(
        db,
        release_version,
    )

    defect_analysis = analyze_defects(
        db,
        release_version,
    )

    recommendations = recommend_tests(
        db,
        release_version,
    )

    risk_analysis = analyze_risk(
        db,
        release_version,
    )

    quality_health = calculate_quality_health(
        db,
        release_version,
    )

    return QAIntelligenceResponse(
        release_version=release_version,
        release=release_analysis,
        defects=defect_analysis,
        risk=risk_analysis,
        test_recommendations=recommendations,
        quality_health=quality_health,
    )