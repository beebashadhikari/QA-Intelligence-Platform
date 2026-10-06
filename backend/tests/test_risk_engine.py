from backend.app.services.risk_engine import calculate_risk


def test_high_risk_area():
    result = calculate_risk(
        area="Payments",
        change_score=90,
        historical_defect_score=80,
        business_criticality_score=95,
        failure_score=85,
        instability_score=70,
    )

    assert result.level == "HIGH"
    assert result.score >= 75
    assert result.area == "Payments"

    assert len(result.reasons) >= 3


def test_medium_risk_area():
    result = calculate_risk(
        area="Catalog",
        change_score=60,
        historical_defect_score=50,
        business_criticality_score=55,
        failure_score=45,
        instability_score=40,
    )

    assert result.level == "MEDIUM"
    assert 50 <= result.score < 75


def test_low_risk_area():
    result = calculate_risk(
        area="Profile",
        change_score=20,
        historical_defect_score=10,
        business_criticality_score=20,
        failure_score=15,
        instability_score=10,
    )

    assert result.level == "LOW"
    assert result.score < 50