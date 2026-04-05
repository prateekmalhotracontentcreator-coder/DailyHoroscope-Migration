from __future__ import annotations

from typing import Any

from individual_reports_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Career and Success Blueprint report for Everyday Horoscope.

Rules:
- The chart logic is already computed.
- Do not recalculate houses, Midheaven, lords, or Dasha timing.
- Keep language premium, practical, composed, and non-deterministic.
- Do not imply a guaranteed job title, promotion, or financial outcome.
- No internal notes or implementation language.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- career_archetype
- natural_strengths
- success_formula
- wealth_signature
- peak_periods
- action_guidance
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    output = report.output_payload
    return {
        "summary": report.summary,
        "career_archetype": output.career_archetype,
        "natural_strengths": f"{output.natural_strengths} The strongest results come when these strengths are used consistently rather than dramatically.",
        "success_formula": output.success_formula,
        "wealth_signature": output.wealth_signature,
        "peak_periods": [item.description for item in output.peak_periods],
        "action_guidance": output.action_guidance,
        "remedies": {
            "mantra_practice": output.remedies.mantra.practice,
            "gemstone_purpose": output.remedies.gemstone.purpose,
            "ritual": output.remedies.ritual,
        },
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    output = report.output_payload
    report.summary = str(content.get("summary") or report.summary)
    for field in ("career_archetype", "natural_strengths", "success_formula", "wealth_signature", "action_guidance"):
        if content.get(field):
            setattr(output, field, str(content[field]))
    peak_periods = content.get("peak_periods")
    if isinstance(peak_periods, list):
        for item, description in zip(output.peak_periods, peak_periods):
            if str(description).strip():
                item.description = str(description)
    remedies = content.get("remedies")
    if isinstance(remedies, dict):
        if remedies.get("mantra_practice"):
            output.remedies.mantra.practice = str(remedies["mantra_practice"])
        if remedies.get("gemstone_purpose"):
            output.remedies.gemstone.purpose = str(remedies["gemstone_purpose"])
        if remedies.get("ritual"):
            output.remedies.ritual = str(remedies["ritual"])
    return report


async def enrich_career_blueprint_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=700)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
