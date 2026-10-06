from backend.app.schemas.release import ReleaseData
from backend.app.services.release_engine import evaluate_release


def create_release(**overrides):
    data = {
        "release_version": "2.4.0",
        "total_tests": 248,
        "passed_tests": 231,
        "failed_tests": 9,
        "blocked_tests": 0,
        "critical_defects": 0,
        "high_defects": 0,
        "medium_defects": 0,
        "low_defects": 0,
        "regression_status": "PASSED",
        "smoke_status": "PASSED",
    }

    data.update(overrides)

    return ReleaseData(**data)


def test_release_is_ready():
    release = create_release()

    result = evaluate_release(release)

    assert result["status"] == "READY"
    assert result["blockers"] == []
    assert result["warnings"] == []


def test_critical_defect_blocks_release():
    release = create_release(
        critical_defects=1,
    )

    result = evaluate_release(release)

    assert result["status"] == "NOT_READY"
    assert "Open critical defects exist." in result["blockers"]


def test_failed_smoke_blocks_release():
    release = create_release(
        smoke_status="FAILED",
    )

    result = evaluate_release(release)

    assert result["status"] == "NOT_READY"
    assert "Smoke testing has not passed." in result["blockers"]


def test_warnings_make_release_conditional():
    release = create_release(
        blocked_tests=8,
        high_defects=2,
    )

    result = evaluate_release(release)

    assert result["status"] == "CONDITIONAL"

    assert "8 tests remain blocked." in result["warnings"]

    assert "2 high-severity defects exist." in result["warnings"]