from __future__ import annotations

from typing import Any

from individual_reports_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Retrograde Survival Guide for Everyday Horoscope.

Rules:
- Retrograde windows and house mappings are already computed.
- Do not recalculate any transit logic.
- Keep language calm, supportive, practical, and non-deterministic.
- No fear language, no certainty, no internal notes.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- planet_expectations
- navigation_tips
- what_to_avoid
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    output = report.output_payload
    return {
        "summary": report.summary,
        "planet_expectations": [item.what_to_expect for item in output.active_retrogrades],
        "navigation_tips": [item.navigation_tips for item in output.active_retrogrades],
        "what_to_avoid": [item.what_to_avoid for item in output.active_retrogrades],
        "remedies": [
            {
                "mantra_practice": item.remedies.mantra.practice,
                "gemstone_purpose": item.remedies.gemstone.purpose,
                "ritual": item.remedies.ritual,
            }
            for item in output.active_retrogrades
        ],
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    output = report.output_payload
    report.summary = str(content.get("summary") or report.summary)
    expectations = content.get("planet_expectations")
    if isinstance(expectations, list):
        for item, value in zip(output.active_retrogrades, expectations):
            if str(value).strip():
                item.what_to_expect = str(value)
    tips = content.get("navigation_tips")
    if isinstance(tips, list):
        for item, values in zip(output.active_retrogrades, tips):
            if isinstance(values, list) and values:
                item.navigation_tips = [str(entry) for entry in values if str(entry).strip()]
    avoid = content.get("what_to_avoid")
    if isinstance(avoid, list):
        for item, values in zip(output.active_retrogrades, avoid):
            if isinstance(values, list) and values:
                item.what_to_avoid = [str(entry) for entry in values if str(entry).strip()]
    remedies = content.get("remedies")
    if isinstance(remedies, list):
        for item, remedy in zip(output.active_retrogrades, remedies):
            if not isinstance(remedy, dict):
                continue
            if remedy.get("mantra_practice"):
                item.remedies.mantra.practice = str(remedy["mantra_practice"])
            if remedy.get("gemstone_purpose"):
                item.remedies.gemstone.purpose = str(remedy["gemstone_purpose"])
            if remedy.get("ritual"):
                item.remedies.ritual = str(remedy["ritual"])
    return report


async def enrich_retrograde_survival_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=700)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
