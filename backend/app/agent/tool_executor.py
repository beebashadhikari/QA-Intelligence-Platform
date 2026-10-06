from sqlalchemy.orm import Session

from backend.app.agent.tools import (
    get_defects,
    get_quality_health,
    get_recommendations,
    get_release,
    get_release_decision,
    get_risk,
)


TOOL_MAP = {
    "get_release": get_release,
    "get_defects": get_defects,
    "get_risk": get_risk,
    "get_recommendations": get_recommendations,
    "get_quality_health": get_quality_health,
    "get_release_decision": get_release_decision,
}


def execute_tool(
    db: Session,
    tool_name: str,
    arguments: dict,
):
    tool = TOOL_MAP.get(tool_name)

    if tool is None:
        raise ValueError(
            f"Unknown QA tool: {tool_name}"
        )

    release_version = arguments.get(
        "release_version"
    )

    if not release_version:
        raise ValueError(
            "release_version is required."
        )

    return tool(
        db,
        release_version,
    )