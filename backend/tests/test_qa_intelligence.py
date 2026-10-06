from backend.app.database import SessionLocal
from backend.app.schemas.qa_intelligence import (
    QAIntelligenceResponse,
)
from backend.app.services.qa_intelligence import (
    analyze_qa_intelligence,
)


def test_unified_qa_intelligence():
    db = SessionLocal()

    try:
        result = analyze_qa_intelligence(
            db,
            "2.4.0",
        )

        assert isinstance(
            result,
            QAIntelligenceResponse,
        )

        assert result.release_version == "2.4.0"

        assert (
            result.release.status
            == "CONDITIONAL"
        )

        assert (
            result.release.metrics.pass_rate
            == 93.15
        )

        assert (
            result.defects.total_defects
            == 4
        )

        assert len(
            result.test_recommendations
        ) > 0

        assert len(
            result.risk
        ) > 0

        assert (
            result.quality_health.score
            >= 0
        )

        assert (
            result.quality_health.score
            <= 100
        )

    finally:
        db.close()