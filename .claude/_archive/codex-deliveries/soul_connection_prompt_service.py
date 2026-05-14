from __future__ import annotations

from typing import Any

from love_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Soul Connection synastry report for Everyday Horoscope.

Rules:
- The synastry metrics and overlays are already computed.
- Do not recalculate scores, overlays, or astrology.
- Keep language intimate, mature, psychologically aware, and non-deterministic.
- No internal notes or technical commentary.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- connection_archetype
- attraction_dynamic
- long_term_compatibility
- growth_areas
- remedies_for_both
- section_summaries
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    return {
        "summary": report.summary,
        "connection_archetype": f"{report.output_payload.connection_archetype} This connection is best understood as a space for both attraction and conscious growth.",
        "attraction_dynamic": report.output_payload.attraction_dynamic,
        "long_term_compatibility": f"{report.output_payload.long_term_compatibility} Lasting potential here depends on how honestly both people work with timing, pressure, and tenderness.",
        "growth_areas": list(report.output_payload.growth_areas),
        "remedies_for_both": list(report.output_payload.remedies_for_both),
        "section_summaries": [section.summary for section in report.output_payload.sections],
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    report.summary = str(content.get("summary") or report.summary)
    for field in ("connection_archetype", "attraction_dynamic", "long_term_compatibility"):
        if content.get(field):
            setattr(report.output_payload, field, str(content[field]))
    for field in ("growth_areas", "remedies_for_both"):
        value = content.get(field)
        if isinstance(value, list) and value:
            setattr(report.output_payload, field, [str(item) for item in value if str(item).strip()])
    section_summaries = content.get("section_summaries")
    if isinstance(section_summaries, list):
        for section, summary in zip(report.output_payload.sections, section_summaries):
            if str(summary).strip():
                section.summary = str(summary)
    return report


async def enrich_soul_connection_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=800)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
