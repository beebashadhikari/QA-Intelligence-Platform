from backend.app.database import SessionLocal
from backend.app.services.release_analysis import (
    analyze_release,
)


def test_analyze_release_from_database():
    db = SessionLocal()

    try:
        result = analyze_release(
            db,
            "2.4.0",
        )

        assert result["release_version"] == "2.4.0"

        assert result["metrics"]["pass_rate"] == 93.15
        assert result["metrics"]["failure_rate"] == 3.63
        assert result["metrics"]["blocked_rate"] == 3.23

        assert result["status"] == "CONDITIONAL"

        assert len(result["blockers"]) == 0

        assert (
            "8 tests remain blocked."
            in result["warnings"]
        )

        assert (
            "2 high-severity defects exist."
            in result["warnings"]
        )

    finally:
        db.close()


def test_missing_release():
    db = SessionLocal()

    try:
        try:
            analyze_release(
                db,
                "999.999",
            )

            assert False, "Expected ValueError"

        except ValueError as error:
            assert "999.999" in str(error)

    finally:
        db.close()