import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

_client = None


def _load_client():
    global _client

    if _client is None:
        # Load env variables if not already loaded by caller
        ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
        load_dotenv(dotenv_path=ENV_PATH, override=True)

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        _client = genai.Client(api_key=api_key)

    return _client


def call_llm(prompt: str, temperature: float = 0.0, max_new_tokens: int = 512):
    client = _load_client()

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_new_tokens,
            ),
        )
        return response.text
    except Exception as e:
        msg = str(e)
        if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
            raise RuntimeError(
                "Gemini API quota exceeded. Please wait a minute and try again, "
                "or check your quota at https://ai.dev/rate-limit"
            ) from e
        raise
