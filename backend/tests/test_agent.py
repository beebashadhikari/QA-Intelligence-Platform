from unittest.mock import MagicMock, patch

from backend.app.agent.agent import run_qa_agent
from backend.app.database import SessionLocal


def test_qa_agent_collects_evidence():
    db = SessionLocal()

    try:
        fake_answer = {
            "assessment": (
                "Release 2.4.0 is conditionally ready "
                "based on the available QA evidence."
            ),
            "status": "CONDITIONAL",
            "facts": [
                "231 of 248 tests passed.",
                "8 tests are blocked.",
                "2 high-severity defects are present.",
            ],
            "risks": [
                {
                    "module": "Payments",
                    "level": "MEDIUM",
                    "score": 60.5,
                    "reason": (
                        "Business-critical module with a recent "
                        "change, high-severity defect, and failed test."
                    ),
                }
            ],
            "recommendations": [
                {
                    "action": "Resolve the Payments defect.",
                    "reason": (
                        "Payments is a business-critical area "
                        "with active quality risk."
                    ),
                    "priority": "HIGH",
                }
            ],
            "missing_evidence": [
                "Performance test results.",
            ],
            "confidence": "MEDIUM",
            "human_decision": (
                "QA and release owners must determine "
                "whether the remaining risk is acceptable."
            ),
        }

        fake_function_call = MagicMock()

        fake_function_call.name = "get_risk"

        fake_function_call.args = {
            "release_version": "2.4.0",
        }

        fake_tool_part = MagicMock()

        fake_tool_part.function_call = (
            fake_function_call
        )

        fake_tool_response = MagicMock()

        fake_tool_response.candidates = [
            MagicMock(
                content=MagicMock(
                    parts=[
                        fake_tool_part,
                    ]
                )
            )
        ]

        fake_final_part = MagicMock()

        fake_final_part.function_call = None

        fake_final_response = MagicMock()

        fake_final_response.candidates = [
            MagicMock(
                content=MagicMock(
                    parts=[
                        fake_final_part,
                    ]
                )
            )
        ]

        fake_final_response.text = (
            __import__("json").dumps(
                fake_answer
            )
        )

        fake_client = MagicMock()

        fake_client.models.generate_content.side_effect = [
            fake_tool_response,
            fake_final_response,
        ]

        with patch(
            "backend.app.agent.agent.get_gemini_client",
            return_value=fake_client,
        ) as mock_client:

            with patch(
                "backend.app.agent.agent.execute_tool",
                return_value=[
                    {
                        "module": "Payments",
                        "risk_level": "MEDIUM",
                        "risk_score": 60.5,
                    }
                ],
            ) as mock_execute_tool:

                result = run_qa_agent(
                    db,
                    "Is release 2.4.0 ready?",
                    "2.4.0",
                )

        assert result["release_version"] == "2.4.0"

        assert result["user_request"] == (
            "Is release 2.4.0 ready?"
        )

        assert "answer" in result

        answer = result["answer"]

        assert answer.status == "CONDITIONAL"

        assert answer.confidence == "MEDIUM"

        assert len(answer.facts) == 3

        assert len(answer.risks) == 1

        assert answer.risks[0].module == "Payments"

        assert answer.risks[0].level == "MEDIUM"

        assert answer.risks[0].score == 60.5

        assert len(answer.recommendations) == 1

        assert (
            answer.recommendations[0].priority
            == "HIGH"
        )

        assert (
            "Performance test results."
            in answer.missing_evidence
        )

        mock_client.assert_called_once()

        assert (
            fake_client
            .models
            .generate_content
            .call_count
            == 2
        )

        mock_execute_tool.assert_called_once_with(
            db=db,
            tool_name="get_risk",
            arguments={
                "release_version": "2.4.0",
            },
        )

    finally:
        db.close()