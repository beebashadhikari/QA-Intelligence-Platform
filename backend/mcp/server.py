import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

from backend.app import models  # noqa: F401  (registers every table)
from backend.app.database import Base, SessionLocal, engine
from backend.app.services.release_decision import calculate_release_decision


# Load the repository .env so QA_API_BASE_URL, MCP_HOST, and MCP_PORT can
# be configured exactly as documented in the README. Real process
# environment variables still take precedence over .env values.
REPO_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(REPO_ROOT / ".env")


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


def ensure_database() -> None:
    """Create missing tables so the direct-DB tool never fails on a
    fresh database file."""

    Base.metadata.create_all(bind=engine)


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

    except Exception as exc:  # noqa: BLE001 - tool must never raise
        return {
            "error": "QA Intelligence API request failed.",
            "path": path,
            "details": str(exc),
        }


def _version_path(release_version: str, suffix: str = "") -> str:
    """Build a safe URL path segment for a release version."""

    return f"/api/releases/{quote(str(release_version), safe='')}{suffix}"


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
        _version_path(release_version)
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
        _version_path(release_version, "/recommendations")
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
        _version_path(release_version, "/risk")
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
        _version_path(release_version, "/defects")
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
        _version_path(release_version, "/quality")
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
    try:
        ensure_database()

        db = SessionLocal()

        try:
            decision = calculate_release_decision(
                db=db,
                release_version=release_version,
            )

            return decision.model_dump()

        finally:
            db.close()

    except ValueError as exc:
        # Missing release: return the same structured error shape the
        # HTTP-backed tools use instead of raising a tool exception.
        return {
            "error": str(exc),
            "release_version": release_version,
        }

    except Exception as exc:  # noqa: BLE001 - tool must never raise
        return {
            "error": "Release decision could not be calculated.",
            "release_version": release_version,
            "details": str(exc),
        }


if __name__ == "__main__":
    ensure_database()

    server.run(
        transport="streamable-http",
        host=MCP_HOST,
        port=MCP_PORT,
    )