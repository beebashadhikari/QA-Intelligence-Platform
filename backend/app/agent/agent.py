import json
import os
from pathlib import Path
from time import perf_counter

from dotenv import load_dotenv
from google.genai import types
from sqlalchemy.orm import Session

from backend.app.agent.observability import (
    complete_agent_run,
    create_agent_run,
    record_tool_call,
)
from backend.app.agent.prompts import build_qa_prompt
from backend.app.agent.tool_executor import execute_tool
from backend.app.agent.validation import validate_agent_response
from backend.app.ai.gemini import get_gemini_client
from backend.app.ai.tools import QA_TOOLS
from backend.app.schemas.agent import AgentAnalyzeResponse


# Load the repository .env explicitly so configuration is resolved from
# one known file, never from a stray nested .env.
load_dotenv(Path(__file__).resolve().parents[3] / ".env")


DEFAULT_MODEL = os.getenv(
    "AI_MODEL",
    "gemini-3.5-flash-lite",
)

MAX_TOOL_ROUNDS = 5


def run_qa_agent(
    db: Session,
    user_request: str,
    release_version: str,
) -> dict:

    client = get_gemini_client()

    run_id = create_agent_run(
        db=db,
        user_request=user_request,
        release_version=release_version,
        model=DEFAULT_MODEL,
    )

    prompt = build_qa_prompt(
        user_request=user_request,
        release_version=release_version,
        evidence={
            "release_version": release_version,
        },
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(
                    text=prompt,
                )
            ],
        )
    ]

    for _ in range(MAX_TOOL_ROUNDS):

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.2,
                tools=QA_TOOLS,
            ),
        )

        if not response.candidates:
            raise RuntimeError(
                "Gemini returned no candidates."
            )

        candidate = response.candidates[0]

        if not candidate.content:
            raise RuntimeError(
                "Gemini returned empty content."
            )

        contents.append(
            candidate.content
        )

        function_calls = []

        for part in candidate.content.parts or []:
            if part.function_call:
                function_calls.append(
                    part.function_call
                )

        if not function_calls:

            raw_answer = response.text

            if not raw_answer:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            try:
                parsed_answer = json.loads(
                    raw_answer
                )

            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    "Gemini returned invalid JSON."
                ) from exc

            try:
                validated_answer = AgentAnalyzeResponse(
                    release_version=release_version,
                    message=user_request,
                    **parsed_answer,
                )

                validated_answer = validate_agent_response(
                    validated_answer
                )

            except Exception as exc:
                raise RuntimeError(
                    f"Gemini response failed validation: {exc}"
                ) from exc

            complete_agent_run(
                db=db,
                run_id=run_id,
                status=validated_answer.status,
                confidence=validated_answer.confidence,
            )

            return {
                "release_version": release_version,
                "user_request": user_request,
                "answer": validated_answer,
            }

        for function_call in function_calls:

            tool_name = function_call.name

            arguments = (
                dict(function_call.args)
                if function_call.args
                else {}
            )

            tool_start = perf_counter()

            try:
                tool_result = execute_tool(
                    db=db,
                    tool_name=tool_name,
                    arguments=arguments,
                )

                record_tool_call(
                    db=db,
                    run_id=run_id,
                    tool_name=tool_name,
                    arguments=arguments,
                    duration_ms=(
                        perf_counter() - tool_start
                    ) * 1000,
                    success=True,
                )

            except Exception:
                record_tool_call(
                    db=db,
                    run_id=run_id,
                    tool_name=tool_name,
                    arguments=arguments,
                    duration_ms=(
                        perf_counter() - tool_start
                    ) * 1000,
                    success=False,
                )

                raise

            function_response_part = (
                types.Part.from_function_response(
                    name=tool_name,
                    response={
                        "result": tool_result,
                    },
                )
            )

            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        function_response_part,
                    ],
                )
            )

    raise RuntimeError(
        "Gemini exceeded the maximum number "
        "of QA tool-calling rounds."
    )