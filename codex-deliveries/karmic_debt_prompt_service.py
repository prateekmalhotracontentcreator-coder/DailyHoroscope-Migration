from __future__ import annotations

from typing import Any

from individual_reports_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Karmic Debt and Past Life report for Everyday Horoscope.

Rules:
- The astrology has already been computed.
- Do not recalculate houses, retrogrades, nodes, or Atmakaraka.
- Keep language premium, mysterious, calm, and non-deterministic.
- Treat past-life language as spiritual and metaphorical, never factual.
- Treat remedies as supportive practices, never guarantees.
- No internal notes, no developer language, no warnings about implementation.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- headline
- karmic_theme
- past_life_echo
- atmakaraka_insight
- retrograde_lessons
- breaking_the_cycle
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    current = report.output_payload.report
    return {
        "summary": report.summary,
        "headline": current.headline,
        "karmic_theme": f"{current.karmic_theme} This report is best read as a map of repeating lessons, not a fixed verdict.",
        "past_life_echo": f"{current.past_life_echo} The pattern softens when it is observed without fear.",
        "atmakaraka_insight": current.atmakaraka_insight,
        "retrograde_lessons": [item.lesson for item in current.retrograde_lessons],
        "breaking_the_cycle": current.breaking_the_cycle,
        "remedies": {
            "mantra_practice": current.remedies.mantra.practice,
            "gemstone_purpose": current.remedies.gemstone.purpose,
            "ritual": current.remedies.ritual,
        },
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    current = report.output_payload.report
    report.summary = str(content.get("summary") or report.summary)
    for field in ("headline", "karmic_theme", "past_life_echo", "atmakaraka_insight", "breaking_the_cycle"):
        if content.get(field):
            setattr(current, field, str(content[field]))
    lessons = content.get("retrograde_lessons")
    if isinstance(lessons, list):
        for item, lesson in zip(current.retrograde_lessons, lessons):
            if str(lesson).strip():
                item.lesson = str(lesson)
    remedies = content.get("remedies")
    if isinstance(remedies, dict):
        if remedies.get("mantra_practice"):
            current.remedies.mantra.practice = str(remedies["mantra_practice"])
        if remedies.get("gemstone_purpose"):
            current.remedies.gemstone.purpose = str(remedies["gemstone_purpose"])
        if remedies.get("ritual"):
            current.remedies.ritual = str(remedies["ritual"])
    return report


async def enrich_karmic_debt_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=750)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
