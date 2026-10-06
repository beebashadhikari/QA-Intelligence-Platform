from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas.qa_intelligence import (
    QAIntelligenceResponse,
)
from backend.app.services.qa_intelligence import (
    analyze_qa_intelligence,
)


router = APIRouter(
    prefix="/api/qa-intelligence",
    tags=["QA Intelligence"],
)


@router.get(
    "/{release_version}",
    response_model=QAIntelligenceResponse,
)
def get_qa_intelligence(
    release_version: str,
    db: Session = Depends(get_db),
):
    try:
        return analyze_qa_intelligence(
            db=db,
            release_version=release_version,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )