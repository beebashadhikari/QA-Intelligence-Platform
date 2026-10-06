from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas.dashboard import (
    ReleaseReadinessDashboard,
)
from backend.app.services.dashboard import (
    build_release_dashboard,
)


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/release/{release_version}",
    response_model=ReleaseReadinessDashboard,
)
def get_release_dashboard(
    release_version: str,
    db: Session = Depends(get_db),
):
    try:
        return build_release_dashboard(
            db=db,
            release_version=release_version,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )