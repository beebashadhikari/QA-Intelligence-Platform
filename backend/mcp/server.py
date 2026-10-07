import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from mcp.server.mcpserver import MCPServer

from backend.app.database import SessionLocal
from backend.app.services.release_decision import calculate_release_decision


API_BASE_URL = os.getenv(
    "QA_API_BASE_URL",
    "http://127.0.0.1:8000",
)

MCP_HOST = os.getenv(
    "MCP_HOST",
    "127.0.0.1",
)

MCP_PORT = int(
    os.getenv(
        "MCP_PORT",
        "8001",
    )
)


server = MCPServer(
    name="QA Intelligence Platform"
)


def get_api_data(path: str) -> dict:
    url = f"{API_BASE_URL}{path}"

    try:
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    except HTTPError as exc:
        return {
            "error": f"QA Intelligence API returned HTTP {exc.code}",
            "path": path,
        }

    except URLError as exc:
        return {
            "error": "Unable to connect to QA Intelligence Platform.",
            "details": str(exc.reason),
        }


@server.tool(
    name="get_release",
    description=(
        "Get the complete release context for a specific release, "
        "including release status, test execution summary, defects, "
        "and quality indicators."
    ),
)
async def get_release(release_version: str) -> dict:
    return get_api_data(
        f"/api/releases/{release_version}"
    )


@server.tool(
    name="get_test_recommendations",
    description=(
        "Get evidence-based test execution recommendations "
        "for a specific release."
    ),
)
async def get_test_recommendations(release_version: str) -> dict:
    return get_api_data(
        f"/api/releases/{release_version}/recommendations"
    )


@server.tool(
    name="get_risk",
    description=(
        "Get module-level risk analysis for a specific release, "
        "including risk scores, code changes, high-severity defects, "
        "and failed tests."
    ),
)
async def get_risk(release_version: str) -> dict:
    return get_api_data(
        f"/api/releases/{release_version}/risk"
    )


@server.tool(
    name="get_defects",
    description=(
        "Get defect information for a specific release, "
        "including severity and defect status."
    ),
)
async def get_defects(release_version: str) -> dict:
    return get_api_data(
        f"/api/releases/{release_version}/defects"
    )


@server.tool(
    name="get_quality_health",
    description=(
        "Get the quality health assessment for a specific release, "
        "including quality score, pass rate, health status, and "
        "execution indicators."
    ),
)
async def get_quality_health(release_version: str) -> dict:
    return get_api_data(
        f"/api/releases/{release_version}/quality"
    )


@server.tool(
    name="get_release_decision",
    description=(
        "Get the deterministic release readiness decision for a "
        "specific release, including blockers, risk factors, "
        "required actions, confidence, and evidence."
    ),
)
async def get_release_decision(release_version: str) -> dict:
    db = SessionLocal()

    try:
        decision = calculate_release_decision(
            db=db,
            release_version=release_version,
        )

        return decision.model_dump()

    finally:
        db.close()


if __name__ == "__main__":
    server.run(
        transport="streamable-http",
        host=MCP_HOST,
        port=MCP_PORT,
    )