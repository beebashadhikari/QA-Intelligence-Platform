from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.quality_health import (
    calculate_quality_health,
)


router = APIRouter(
    prefix="/api/releases",
    tags=["Quality"],
)


@router.get("/{release_version}/quality")
def get_quality_health(
    release_version: str,
    db: Session = Depends(get_db),
):
    try:
        return calculate_quality_health(
            db,
            release_version,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )