import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load the repository .env explicitly (single source of configuration).
load_dotenv(Path(__file__).resolve().parents[3] / ".env")


def get_gemini_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=api_key,
    )


def generate_gemini_response(
    prompt: str,
    model: str,
) -> str:
    client = get_gemini_client()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json"
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text