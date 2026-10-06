from backend.app.schemas.agent import AgentAnalyzeResponse


def validate_agent_response(
    response: AgentAnalyzeResponse,
) -> AgentAnalyzeResponse:
    """
    Deterministically validate and harden the AI-generated
    QA assessment before returning it to the API consumer.
    """

    missing_evidence = {
        item.strip().lower()
        for item in response.missing_evidence
    }

    confidence = response.confidence

    important_missing_evidence = {
        "performance testing results",
        "production incident history",
    }

    if (
        confidence == "HIGH"
        and missing_evidence.intersection(
            important_missing_evidence
        )
    ):
        confidence = "MEDIUM"

    if (
        response.status in {"READY", "CONDITIONAL"}
        and confidence == "HIGH"
        and response.missing_evidence
    ):
        confidence = "MEDIUM"

    return response.model_copy(
        update={
            "confidence": confidence,
        }
    )