from sqlalchemy.orm import Session

from backend.app.services.defect_analysis import analyze_defects
from backend.app.services.quality_health import calculate_quality_health
from backend.app.services.qa_intelligence import analyze_qa_intelligence
from backend.app.services.recommendation import recommend_tests
from backend.app.services.release_analysis import analyze_release
from backend.app.services.release_decision import (
    calculate_release_decision,
)
from backend.app.services.risk_analysis import analyze_risk


def get_release(
    db: Session,
    release_version: str,
) -> dict:
    return analyze_release(
        db,
        release_version,
    )


def get_defects(
    db: Session,
    release_version: str,
) -> dict:
    return analyze_defects(
        db,
        release_version,
    )


def get_risk(
    db: Session,
    release_version: str,
) -> list[dict]:
    return analyze_risk(
        db,
        release_version,
    )


def get_recommendations(
    db: Session,
    release_version: str,
) -> list[dict]:
    return recommend_tests(
        db,
        release_version,
    )


def get_quality_health(
    db: Session,
    release_version: str,
) -> dict:
    return calculate_quality_health(
        db,
        release_version,
    )


def get_qa_intelligence(
    db: Session,
    release_version: str,
) -> dict:
    return analyze_qa_intelligence(
        db,
        release_version,
    )


def get_release_decision(
    db: Session,
    release_version: str,
) -> dict:
    decision = calculate_release_decision(
        db=db,
        release_version=release_version,
    )

    return decision.model_dump()