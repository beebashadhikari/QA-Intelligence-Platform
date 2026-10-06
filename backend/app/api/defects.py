from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.defect_analysis import analyze_defects


router = APIRouter(
    prefix="/api/releases",
    tags=["Defects"],
)


@router.get("/{release_version}/defects")
def get_release_defects(
    release_version: str,
    db: Session = Depends(get_db),
):
    try:
        return analyze_defects(
            db,
            release_version,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )