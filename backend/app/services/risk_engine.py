from dataclasses import dataclass


@dataclass
class RiskAssessment:
    area: str
    score: float
    level: str
    reasons: list[str]


def calculate_risk(
    *,
    area: str,
    change_score: float,
    historical_defect_score: float,
    business_criticality_score: float,
    failure_score: float,
    instability_score: float,
) -> RiskAssessment:

    score = (
        change_score * 0.25
        + historical_defect_score * 0.20
        + business_criticality_score * 0.25
        + failure_score * 0.20
        + instability_score * 0.10
    )

    score = round(score, 2)

    if score >= 75:
        level = "HIGH"
    elif score >= 50:
        level = "MEDIUM"
    else:
        level = "LOW"

    reasons = []

    if change_score >= 75:
        reasons.append(
            "Significant recent changes detected."
        )

    if historical_defect_score >= 75:
        reasons.append(
            "Area has a strong history of defects."
        )

    if business_criticality_score >= 75:
        reasons.append(
            "Area is business critical."
        )

    if failure_score >= 75:
        reasons.append(
            "Recent test failures are elevated."
        )

    if instability_score >= 75:
        reasons.append(
            "Test instability or flakiness is elevated."
        )

    return RiskAssessment(
        area=area,
        score=score,
        level=level,
        reasons=reasons,
    )