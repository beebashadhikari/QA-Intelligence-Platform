from backend.app.database import SessionLocal
from backend.app.services.release_metrics import (
    calculate_release_metrics,
)


def test_release_metrics_from_database():
    db = SessionLocal()

    try:
        result = calculate_release_metrics(
            db,
            "2.4.0",
        )

        assert result["release_version"] == "2.4.0"
        assert result["total_tests"] == 248
        assert result["passed_tests"] == 231
        assert result["failed_tests"] == 9
        assert result["blocked_tests"] == 8

        assert result["pass_rate"] == 93.15
        assert result["failure_rate"] == 3.63
        assert result["blocked_rate"] == 3.23

    finally:
        db.close()


def test_missing_release():
    db = SessionLocal()

    try:
        try:
            calculate_release_metrics(
                db,
                "999.999",
            )
            assert False, "Expected ValueError"
        except ValueError as error:
            assert "999.999" in str(error)

    finally:
        db.close()