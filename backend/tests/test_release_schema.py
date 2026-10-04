import pytest

from backend.app.schemas.release import ReleaseData


def test_valid_release():
    release = ReleaseData(
        release_version="2.4.0",
        total_tests=248,
        passed_tests=231,
        failed_tests=9,
        blocked_tests=8,
        critical_defects=0,
        high_defects=2,
        medium_defects=7,
        low_defects=12,
        regression_status="PASSED",
        smoke_status="PASSED",
    )

    assert release.release_version == "2.4.0"
    assert release.total_tests == 248


def test_invalid_test_counts():
    with pytest.raises(ValueError):
        ReleaseData(
            release_version="2.4.0",
            total_tests=100,
            passed_tests=80,
            failed_tests=30,
            blocked_tests=0,
            critical_defects=0,
            high_defects=0,
            medium_defects=0,
            low_defects=0,
            regression_status="PASSED",
            smoke_status="PASSED",
        )