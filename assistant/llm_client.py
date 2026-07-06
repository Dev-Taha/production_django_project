import json
import os

from openai import OpenAI, APIConnectionError, APIStatusError, RateLimitError

BASE_URL = "https://api.together.ai/v1"
MODEL = os.environ.get("ASSISTANT_MODEL", "meta-llama/Llama-3.3-70B-Instruct-Turbo")


class LLMError(Exception):
    """Raised when the AI layer can't produce a response."""


def _client() -> OpenAI:
    key = os.environ.get("TOGETHER_API_KEY")
    if not key:
        raise LLMError("TOGETHER_API_KEY is not set.")
    return OpenAI(
        base_url=BASE_URL,
        api_key=key,
    )


def complete(system: str, user_content: str,
             max_tokens: int = 2000, temperature: float = 0.3) -> str:
    """One-shot completion. Returns plain text."""
    try:
        response = _client().chat.completions.create(
            model=MODEL,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_content},
            ],
        )
    except RateLimitError as e:
        raise LLMError("The AI service is busy. Try again in a moment.") from e
    except APIConnectionError as e:
        raise LLMError("Could not reach the AI service.") from e
    except APIStatusError as e:
        raise LLMError(f"AI service error (status {e.status_code}).") from e

    content = response.choices[0].message.content
    if not content:
        raise LLMError("The AI returned an empty response.")
    return content


def complete_json(system: str, user_content: str, **kwargs) -> dict:
    raw = complete(system, user_content, **kwargs).strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise LLMError("The AI returned malformed output.") from e