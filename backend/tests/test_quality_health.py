from backend.app.database import SessionLocal
from backend.app.services.quality_health import (
    calculate_quality_health,
)


def test_quality_health():
    db = SessionLocal()

    try:
        result = calculate_quality_health(
            db,
            "2.4.0",
        )

        assert result["release_version"] == "2.4.0"

        assert 0 <= result["score"] <= 100

        assert result["health"] in {
            "EXCELLENT",
            "GOOD",
            "FAIR",
            "POOR",
            "CRITICAL",
        }

        assert "functional" in result["components"]
        assert "regression" in result["components"]
        assert "defects" in result["components"]
        assert "automation" in result["components"]
        assert "stability" in result["components"]

    finally:
        db.close()