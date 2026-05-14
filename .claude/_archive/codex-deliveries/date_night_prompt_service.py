from __future__ import annotations

from typing import Any

from love_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Date Night report for Everyday Horoscope.

Rules:
- The daily score and lunar angle are already computed.
- Do not recalculate astrology, percentages, or timing.
- Keep language elegant, concise, user-facing, and non-deterministic.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- alignment_description
- action_note
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    return {
        "summary": report.summary,
        "alignment_description": f"{report.output_payload.alignment_description} Let the tone of the evening stay natural rather than over-planned.",
        "action_note": report.output_payload.action_note if report.output_payload.notification_worthy else "Keep the moment simple, readable, and emotionally light.",
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    report.summary = str(content.get("summary") or report.summary)
    report.output_payload.alignment_description = str(content.get("alignment_description") or report.output_payload.alignment_description)
    report.output_payload.action_note = str(content.get("action_note") or report.output_payload.action_note)
    return report


async def enrich_date_night_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=500, temperature=0.45)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
