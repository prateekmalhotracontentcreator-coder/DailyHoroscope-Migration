from __future__ import annotations

from typing import Any

from love_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Digital Dating report for Everyday Horoscope.

Rules:
- Natal placements are already computed.
- Do not recalculate houses, signs, or lordships.
- Keep language warm, modern, practical, and non-deterministic.
- No internal notes or technical explanation.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- attraction_signature
- dating_style
- ideal_partner_profile
- first_date_lead
- self_red_flags
- remedies
- section_bodies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    return {
        "summary": report.summary,
        "attraction_signature": f"{report.output_payload.attraction_signature} The attraction style here works best when it stays polished without becoming guarded.",
        "dating_style": f"{report.output_payload.dating_style} The more natural your pacing feels, the more magnetic the profile becomes.",
        "ideal_partner_profile": f"{report.output_payload.ideal_partner_profile} The strongest matches are usually the ones that make steadiness feel easy, not forced.",
        "first_date_lead": f"{report.output_payload.first_date_lead} Let your first move sound human and unhurried.",
        "self_red_flags": list(report.output_payload.self_red_flags),
        "remedies": list(report.output_payload.remedies),
        "section_bodies": [section.body for section in report.output_payload.sections],
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    report.summary = str(content.get("summary") or report.summary)
    for field in ("attraction_signature", "dating_style", "ideal_partner_profile", "first_date_lead"):
        if content.get(field):
            setattr(report.output_payload, field, str(content[field]))
    for field in ("self_red_flags", "remedies"):
        value = content.get(field)
        if isinstance(value, list) and value:
            setattr(report.output_payload, field, [str(item) for item in value if str(item).strip()])
    section_bodies = content.get("section_bodies")
    if isinstance(section_bodies, list):
        for section, body in zip(report.output_payload.sections, section_bodies):
            if str(body).strip():
                section.body = str(body)
    return report


async def enrich_digital_dating_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report))
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
