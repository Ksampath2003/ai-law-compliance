"""
Claude API wrapper with retry logic and structured output helpers.
"""
import json
from typing import Optional
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
MODEL = "claude-sonnet-4-20250514"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_claude(prompt: str, system: str = "", max_tokens: int = 1024) -> str:
    messages = [{"role": "user", "content": prompt}]
    kwargs = {"model": MODEL, "max_tokens": max_tokens, "messages": messages}
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text


def call_claude_json(prompt: str, system: str = "", max_tokens: int = 1024) -> dict:
    """Call Claude and parse the response as JSON."""
    sys_with_json = (system + "\n\nRespond ONLY with valid JSON. No markdown, no explanation.").strip()
    raw = call_claude(prompt, system=sys_with_json, max_tokens=max_tokens)
    # Strip accidental markdown fences
    clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    return json.loads(clean)
