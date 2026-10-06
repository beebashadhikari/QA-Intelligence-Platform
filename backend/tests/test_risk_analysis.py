from backend.app.database import SessionLocal
from backend.app.services.risk_analysis import analyze_risk


def test_risk_analysis():
    db = SessionLocal()

    try:
        results = analyze_risk(
            db,
            "2.4.0",
        )

        assert len(results) > 0

        assert results[0]["area"] in {
            "Payments",
            "Authentication",
            "Catalog",
        }

        assert results[0]["score"] >= 0
        assert results[0]["score"] <= 100

        assert results[0]["level"] in {
            "HIGH",
            "MEDIUM",
            "LOW",
        }

    finally:
        db.close()