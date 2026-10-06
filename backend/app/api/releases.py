from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.release import Release
from backend.app.services.release_analysis import analyze_release
from backend.app.services.qa_intelligence import (
    analyze_qa_intelligence,
)
from backend.app.services.release_portfolio import (
    get_release_portfolio,
)

router = APIRouter(
    prefix="/api/releases",
    tags=["Releases"],
)


@router.get("")
def get_releases(
    db: Session = Depends(get_db),
):
    releases = (
        db.query(Release)
        .order_by(Release.id.desc())
        .all()
    )

    return [
        {
            "release_version": release.release_version,
        }
        for release in releases
    ]


@router.get("/portfolio")
def get_release_portfolio_data(
    db: Session = Depends(get_db),
):
    try:
        return get_release_portfolio(
            db=db,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get("/{release_version}")
def get_release(
    release_version: str,
    db: Session = Depends(get_db),
):
    try:
        return analyze_release(
            db,
            release_version,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get("/{release_version}/intelligence")
def get_release_intelligence(
    release_version: str,
    db: Session = Depends(get_db),
):
    try:
        return analyze_qa_intelligence(
            db,
            release_version,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )