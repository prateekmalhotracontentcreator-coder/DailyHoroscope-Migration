from __future__ import annotations

from typing import Any

from individual_reports_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Romance & Creative Intelligence report for Everyday Horoscope.

Rules:
- The astrology has already been computed.
- Do not recalculate planets, houses, karakas, or dasha timing.
- Keep language intimate, refined, and non-deterministic.
- Blend romance and creativity without sounding generic.
- Treat remedies as supportive practices, never guarantees.
- No internal notes or implementation language.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- romantic_signature
- creative_intelligence
- heart_blocks
- expression_path
- opening_windows
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    current = report.output_payload
    return {
        "summary": report.summary,
        "romantic_signature": current.romantic_signature,
        "creative_intelligence": current.creative_intelligence,
        "heart_blocks": current.heart_blocks,
        "expression_path": f"{current.expression_path} The chart points toward rhythms of opening, not fixed outcomes.",
        "opening_windows": [item.description for item in current.opening_windows],
        "remedies": {
            "mantra_practice": current.remedies.mantra.practice,
            "gemstone_purpose": current.remedies.gemstone.purpose,
            "ritual": current.remedies.ritual,
        },
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    current = report.output_payload
    report.summary = str(content.get("summary") or report.summary)
    for field in ("romantic_signature", "creative_intelligence", "heart_blocks", "expression_path"):
        if content.get(field):
            setattr(current, field, str(content[field]))
    windows = content.get("opening_windows")
    if isinstance(windows, list):
        for item, description in zip(current.opening_windows, windows):
            if str(description).strip():
                item.description = str(description)
    remedies = content.get("remedies")
    if isinstance(remedies, dict):
        if remedies.get("mantra_practice"):
            current.remedies.mantra.practice = str(remedies["mantra_practice"])
        if remedies.get("gemstone_purpose"):
            current.remedies.gemstone.purpose = str(remedies["gemstone_purpose"])
        if remedies.get("ritual"):
            current.remedies.ritual = str(remedies["ritual"])
    return report


async def enrich_romance_creative_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=900)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
