from __future__ import annotations

import json
import os
from typing import Any

DEFAULT_CLAUDE_MODEL = os.getenv("LOVE_CLAUDE_MODEL", "claude-3-5-sonnet-latest")


def extract_text_from_claude_response(response: Any) -> str | None:
    content = getattr(response, "content", None)
    if not content:
        return None
    text_parts: list[str] = []
    for item in content:
        text_value = getattr(item, "text", None)
        if text_value:
            text_parts.append(text_value)
    return "\n".join(text_parts).strip() if text_parts else None


async def try_claude_generation(prompt: str, *, max_tokens: int = 700, temperature: float = 0.5) -> dict[str, Any] | None:
    try:
        from anthropic import AsyncAnthropic  # type: ignore
    except Exception:
        return None

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    client = AsyncAnthropic(api_key=api_key)
    try:
        response = await client.messages.create(
            model=DEFAULT_CLAUDE_MODEL,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception:
        return None

    text = extract_text_from_claude_response(response)
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def payload_json(report: Any) -> str:
    output = report.output_payload.model_dump(mode="python") if hasattr(report.output_payload, "model_dump") else report.output_payload
    return json.dumps(output, ensure_ascii=True)
