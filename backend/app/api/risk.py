from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.risk_analysis import analyze_risk


router = APIRouter(
    prefix="/api/releases",
    tags=["Risk"],
)


@router.get("/{release_version}/risk")
def get_release_risk(
    release_version: str,
    db: Session = Depends(get_db),
):
    try:
        return {
            "release_version": release_version,
            "risk": analyze_risk(
                db,
                release_version,
            ),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )