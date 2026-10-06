from backend.app.database import SessionLocal
from backend.app.services.defect_analysis import (
    analyze_defects,
)


def test_defect_analysis():
    db = SessionLocal()

    try:
        result = analyze_defects(
            db,
            "2.4.0",
        )

        assert result["release_version"] == "2.4.0"

        assert result["total_defects"] == 4

        assert (
            result["severity_counts"]["critical"]
            == 0
        )

        assert (
            result["severity_counts"]["high"]
            == 2
        )

        assert (
            result["severity_counts"]["medium"]
            == 1
        )

        assert (
            result["severity_counts"]["low"]
            == 1
        )

        assert result["status_counts"]["open"] == 2
        assert result["status_counts"]["in_progress"] == 1
        assert result["status_counts"]["resolved"] == 1

        assert result["module_counts"]["Payments"] == 1
        assert result["module_counts"]["Authentication"] == 1
        assert result["module_counts"]["Orders"] == 1
        assert result["module_counts"]["Catalog"] == 1

    finally:
        db.close()


def test_missing_release_has_no_defects():
    db = SessionLocal()

    try:
        result = analyze_defects(
            db,
            "999.999",
        )

        assert result["total_defects"] == 0
        assert result["severity_counts"]["high"] == 0

    finally:
        db.close()