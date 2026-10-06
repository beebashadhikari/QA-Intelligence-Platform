from backend.app.database import SessionLocal
from backend.app.services.release_decision import (
    calculate_release_decision,
)


def get_decision(release_version: str):
    db = SessionLocal()

    try:
        return calculate_release_decision(
            db=db,
            release_version=release_version,
        )

    finally:
        db.close()


def test_2_4_0_decision_is_conditional():
    decision = get_decision("2.4.0")

    assert decision.status == "CONDITIONAL"
    assert decision.confidence in {
        "HIGH",
        "MEDIUM",
    }


def test_2_4_0_contains_high_risk_test_evidence():
    decision = get_decision("2.4.0")

    assert any(
        "high-risk test recommendation" in factor
        for factor in decision.risk_factors
    )


def test_2_4_0_contains_failed_test_action():
    decision = get_decision("2.4.0")

    assert any(
        "TC-103" in action
        for action in decision.required_actions
    )


def test_2_2_0_has_stronger_risk_evidence():
    decision = get_decision("2.2.0")

    assert decision.status == "NOT_READY"
    assert any(
        "high-risk" in factor.lower()
        for factor in decision.risk_factors
    )


def test_2_3_0_contains_blocked_test_action():
    decision = get_decision("2.3.0")

    assert any(
        "TC-204" in action
        for action in decision.required_actions
    )