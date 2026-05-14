from __future__ import annotations

from typing import Any

from love_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Love Weather report for Everyday Horoscope.

Rules:
- The deterministic astrology has already been computed.
- Do not recalculate any transits, scores, dates, or ratings.
- Keep language warm, premium, supportive, and non-deterministic.
- Do not mention developers, prompts, systems, or internal process.
- Return user-facing copy only.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- arc_summary
- action_guidance
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    return {
        "summary": report.summary,
        "arc_summary": f"{report.output_payload.arc_summary} Think of this period as a changing emotional climate rather than a fixed verdict on what love must do next.",
        "action_guidance": f"{report.output_payload.action_guidance} The strongest dates are best used for visibility and honest warmth, while lower-energy dates can support reflection and clearer pacing.",
        "remedies": list(report.output_payload.remedies),
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    report.summary = str(content.get("summary") or report.summary)
    report.output_payload.arc_summary = str(content.get("arc_summary") or report.output_payload.arc_summary)
    report.output_payload.action_guidance = str(content.get("action_guidance") or report.output_payload.action_guidance)
    remedies = content.get("remedies")
    if isinstance(remedies, list) and remedies:
        report.output_payload.remedies = [str(item) for item in remedies if str(item).strip()]
    return report


async def enrich_love_weather_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report))
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
