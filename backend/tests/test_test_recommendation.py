from backend.app.database import SessionLocal
from backend.app.services.recommendation import recommend_tests


def test_test_recommendations():
    db = SessionLocal()

    try:
        results = recommend_tests(
            db,
            "2.4.0",
        )

        assert len(results) > 0

        first = results[0]

        assert first["score"] >= 75
        assert first["risk_level"] == "HIGH"

        assert "test_case_id" in first
        assert "title" in first
        assert "module" in first
        assert "reasons" in first

    finally:
        db.close()