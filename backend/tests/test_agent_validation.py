from backend.app.agent.validation import validate_agent_response
from backend.app.schemas.agent import (
    AgentAnalyzeResponse,
)


def make_response(
    confidence: str,
    missing_evidence: list[str],
) -> AgentAnalyzeResponse:
    return AgentAnalyzeResponse(
        release_version="2.4.0",
        message="Is the release ready?",
        assessment="Release requires review.",
        status="CONDITIONAL",
        facts=[
            "Two high-severity defects exist."
        ],
        risks=[],
        recommendations=[],
        missing_evidence=missing_evidence,
        confidence=confidence,
        human_decision=(
            "Human release approval is required."
        ),
    )


def test_high_confidence_is_downgraded_when_important_evidence_is_missing():
    response = make_response(
        confidence="HIGH",
        missing_evidence=[
            "Performance testing results",
            "Production incident history",
        ],
    )

    validated = validate_agent_response(response)

    assert validated.confidence == "MEDIUM"


def test_medium_confidence_remains_medium():
    response = make_response(
        confidence="MEDIUM",
        missing_evidence=[
            "Performance testing results",
        ],
    )

    validated = validate_agent_response(response)

    assert validated.confidence == "MEDIUM"


def test_high_confidence_with_complete_evidence_is_preserved():
    response = make_response(
        confidence="HIGH",
        missing_evidence=[],
    )

    validated = validate_agent_response(response)

    assert validated.confidence == "HIGH"