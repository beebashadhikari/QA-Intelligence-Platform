from sqlalchemy.orm import Session

from backend.app.models.defect import Defect


def analyze_defects(
    db: Session,
    release_version: str,
) -> dict:
    defects = (
        db.query(Defect)
        .filter(
            Defect.release_version == release_version
        )
        .all()
    )

    severity_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    status_counts = {
        "open": 0,
        "in_progress": 0,
        "resolved": 0,
        "closed": 0,
    }

    module_counts: dict[str, int] = {}

    for defect in defects:
        severity = defect.severity.lower()
        status = defect.status.lower()

        if severity in severity_counts:
            severity_counts[severity] += 1

        if status in status_counts:
            status_counts[status] += 1

        module_counts[defect.module] = (
            module_counts.get(defect.module, 0) + 1
        )

    return {
        "release_version": release_version,
        "total_defects": len(defects),
        "severity_counts": severity_counts,
        "status_counts": status_counts,
        "module_counts": module_counts,
    }