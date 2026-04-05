from __future__ import annotations

from typing import Any

from individual_reports_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Shadow Self and Hidden Qualities report for Everyday Horoscope.

Rules:
- The chart logic is already computed.
- Do not recalculate Nakshatras, Atmakaraka, or shadow-pressure indicators.
- Keep language psychologically reflective, mysterious, warm, and non-deterministic.
- Do not diagnose, label, or pathologize the user.
- No internal notes or technical wording.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- janma_nakshatra
- shadow_nakshatra
- hidden_strengths
- blind_spots
- psychological_driver
- integration_path
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    output = report.output_payload
    return {
        "summary": report.summary,
        "janma_nakshatra": output.janma_nakshatra,
        "shadow_nakshatra": output.shadow_nakshatra,
        "hidden_strengths": output.hidden_strengths,
        "blind_spots": f"{output.blind_spots} The work here is awareness, not self-judgment.",
        "psychological_driver": output.psychological_driver,
        "integration_path": output.integration_path,
        "remedies": {
            "mantra_practice": output.remedies.mantra.practice,
            "gemstone_purpose": output.remedies.gemstone.purpose,
            "ritual": output.remedies.ritual,
        },
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    output = report.output_payload
    report.summary = str(content.get("summary") or report.summary)
    for field in (
        "janma_nakshatra",
        "shadow_nakshatra",
        "hidden_strengths",
        "blind_spots",
        "psychological_driver",
        "integration_path",
    ):
        if content.get(field):
            setattr(output, field, str(content[field]))
    remedies = content.get("remedies")
    if isinstance(remedies, dict):
        if remedies.get("mantra_practice"):
            output.remedies.mantra.practice = str(remedies["mantra_practice"])
        if remedies.get("gemstone_purpose"):
            output.remedies.gemstone.purpose = str(remedies["gemstone_purpose"])
        if remedies.get("ritual"):
            output.remedies.ritual = str(remedies["ritual"])
    return report


async def enrich_shadow_self_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=700)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
