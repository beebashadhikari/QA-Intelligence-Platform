import os

from dotenv import load_dotenv

from backend.app.ai.gemini import generate_gemini_response


load_dotenv()


if __name__ == "__main__":
    response = generate_gemini_response(
        prompt="Reply with exactly: Gemini connection successful.",
        model=os.getenv(
            "AI_MODEL",
            "gemini-2.5-flash-lite",
        ),
    )

    print("\nGemini response:")
    print(response)