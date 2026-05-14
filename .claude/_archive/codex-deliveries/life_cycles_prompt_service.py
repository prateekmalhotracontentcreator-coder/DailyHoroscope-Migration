from __future__ import annotations

from typing import Any

from individual_reports_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic The Pattern of Life Cycles report for Everyday Horoscope.

Rules:
- Dasha sequencing is already computed.
- Do not recalculate planetary periods, dates, or transitions.
- Keep language expansive, calm, premium, and non-deterministic.
- No guaranteed outcomes and no internal notes.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- current_chapter
- current_sub_chapter
- chapter_quality
- upcoming_transitions
- this_decade_arc
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    output = report.output_payload
    return {
        "summary": report.summary,
        "current_chapter": output.current_chapter,
        "current_sub_chapter": output.current_sub_chapter,
        "chapter_quality": output.chapter_quality,
        "upcoming_transitions": [item.theme for item in output.upcoming_transitions],
        "this_decade_arc": f"{output.this_decade_arc} Let the decade reveal itself through rhythm rather than force.",
        "remedies": {
            "mantra_practice": output.remedies.mantra.practice,
            "gemstone_purpose": output.remedies.gemstone.purpose,
            "ritual": output.remedies.ritual,
        },
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    output = report.output_payload
    report.summary = str(content.get("summary") or report.summary)
    for field in ("current_chapter", "current_sub_chapter", "chapter_quality", "this_decade_arc"):
        if content.get(field):
            setattr(output, field, str(content[field]))
    transitions = content.get("upcoming_transitions")
    if isinstance(transitions, list):
        for item, theme in zip(output.upcoming_transitions, transitions):
            if str(theme).strip():
                item.theme = str(theme)
    remedies = content.get("remedies")
    if isinstance(remedies, dict):
        if remedies.get("mantra_practice"):
            output.remedies.mantra.practice = str(remedies["mantra_practice"])
        if remedies.get("gemstone_purpose"):
            output.remedies.gemstone.purpose = str(remedies["gemstone_purpose"])
        if remedies.get("ritual"):
            output.remedies.ritual = str(remedies["ritual"])
    return report


async def enrich_life_cycles_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=700)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
