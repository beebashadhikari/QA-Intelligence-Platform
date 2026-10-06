from backend.app.database import SessionLocal
from backend.app.services.recommendation import recommend_tests


def get_recommendations(release_version: str):
    db = SessionLocal()

    try:
        return recommend_tests(
            db,
            release_version,
        )
    finally:
        db.close()


def test_2_4_0_recommendations_are_sorted_by_score():
    result = get_recommendations("2.4.0")

    scores = [
        recommendation["score"]
        for recommendation in result
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_2_4_0_contains_high_risk_failed_tests():
    result = get_recommendations("2.4.0")

    high_risk_failed = [
        recommendation
        for recommendation in result
        if recommendation["risk_level"] == "HIGH"
        and recommendation["status"] == "failed"
    ]

    assert len(high_risk_failed) > 0


def test_blocked_tests_have_blocking_reason():
    result = get_recommendations("2.4.0")

    blocked = [
        recommendation
        for recommendation in result
        if recommendation["status"] == "blocked"
    ]

    assert len(blocked) > 0

    for recommendation in blocked:
        assert recommendation["blocking_reason"]


def test_recommendations_contain_evidence():
    result = get_recommendations("2.4.0")

    assert len(result) > 0

    for recommendation in result:
        assert recommendation["reasons"]
        assert len(recommendation["reasons"]) > 0


def test_release_context_is_preserved():
    result_22 = get_recommendations("2.2.0")
    result_23 = get_recommendations("2.3.0")
    result_24 = get_recommendations("2.4.0")

    assert result_22 != result_24
    assert result_23 != result_24


def test_2_2_0_contains_expected_top_priority_test():
    result = get_recommendations("2.2.0")

    top = result[0]

    assert top["test_case_id"] == "TC-304"
    assert top["score"] == 100
    assert top["risk_level"] == "HIGH"
    assert top["status"] == "failed"


def test_2_3_0_contains_expected_blocked_test():
    result = get_recommendations("2.3.0")

    blocked = [
        recommendation
        for recommendation in result
        if recommendation["status"] == "blocked"
    ]

    assert len(blocked) == 1

    assert blocked[0]["test_case_id"] == "TC-204"
    assert blocked[0]["blocking_reason"] == (
        "Refund test data unavailable"
    )


def test_2_4_0_contains_expected_top_priority_test():
    result = get_recommendations("2.4.0")

    top = result[0]

    assert top["test_case_id"] == "TC-103"
    assert top["score"] == 85
    assert top["risk_level"] == "HIGH"
    assert top["status"] == "failed"