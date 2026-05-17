from __future__ import annotations

from typing import Any

from individual_reports_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Wealth & Abundance Blueprint report for Everyday Horoscope.

Rules:
- The astrology has already been computed.
- Do not recalculate planets, houses, yogas, or dashas.
- Keep language premium, grounded, and mysterious without overclaiming.
- Keep abundance language practical and spiritual, never guaranteed.
- Treat remedies as supportive practices, never promises.
- No internal notes, no developer language, no implementation warnings.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- wealth_signature
- dhanayoga_profile
- abundance_blocks
- prosperity_path
- wealth_windows
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    current = report.output_payload
    return {
        "summary": report.summary,
        "wealth_signature": current.wealth_signature,
        "dhanayoga_profile": f"{current.dhanayoga_profile} This should be read as a pattern of potential, not a guarantee of outcome.",
        "abundance_blocks": current.abundance_blocks,
        "prosperity_path": current.prosperity_path,
        "wealth_windows": [item.description for item in current.wealth_windows],
        "remedies": {
            "mantra_practice": current.remedies.mantra.practice,
            "gemstone_purpose": current.remedies.gemstone.purpose,
            "ritual": current.remedies.ritual,
        },
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    current = report.output_payload
    report.summary = str(content.get("summary") or report.summary)
    for field in ("wealth_signature", "dhanayoga_profile", "abundance_blocks", "prosperity_path"):
        if content.get(field):
            setattr(current, field, str(content[field]))
    windows = content.get("wealth_windows")
    if isinstance(windows, list):
        for item, description in zip(current.wealth_windows, windows):
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


async def enrich_wealth_blueprint_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=900)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
