from __future__ import annotations

from typing import Any

from love_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Venus Retrograde report for Everyday Horoscope.

Rules:
- Retrograde status and natal context are already computed.
- Do not recalculate astrology.
- Keep language reflective, supportive, and non-deterministic.
- No internal notes.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- personal_impact
- healing_focus
- best_practice
- remedies
- section_summaries
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    return {
        "summary": report.summary,
        "personal_impact": f"{report.output_payload.personal_impact} This phase is best read as a review of values, pacing, and emotional honesty.",
        "healing_focus": f"{report.output_payload.healing_focus} Reflection is more powerful here than urgency.",
        "best_practice": report.output_payload.best_practice,
        "remedies": list(report.output_payload.remedies),
        "section_summaries": [section.summary for section in report.output_payload.sections],
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    report.summary = str(content.get("summary") or report.summary)
    for field in ("personal_impact", "healing_focus", "best_practice"):
        if content.get(field):
            setattr(report.output_payload, field, str(content[field]))
    remedies = content.get("remedies")
    if isinstance(remedies, list) and remedies:
        report.output_payload.remedies = [str(item) for item in remedies if str(item).strip()]
    section_summaries = content.get("section_summaries")
    if isinstance(section_summaries, list):
        for section, summary in zip(report.output_payload.sections, section_summaries):
            if str(summary).strip():
                section.summary = str(summary)
    return report


async def enrich_venus_retrograde_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=650)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
