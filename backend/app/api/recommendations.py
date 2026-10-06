from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.recommendation import recommend_tests


router = APIRouter(
    prefix="/api/releases",
    tags=["Recommendations"],
)


@router.get("/{release_version}/recommendations")
def get_test_recommendations(
    release_version: str,
    db: Session = Depends(get_db),
):
    try:
        return {
            "release_version": release_version,
            "recommendations": recommend_tests(
                db,
                release_version,
            ),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )