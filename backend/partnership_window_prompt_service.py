from __future__ import annotations

from typing import Any

from individual_reports_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Partnership & Marriage Window report for Everyday Horoscope.

Rules:
- The astrology has already been computed.
- Do not recalculate houses, karakas, Upapada, or dasha timing.
- Keep language premium, romantic, and non-deterministic.
- Never guarantee marriage, reunion, or relationship outcomes.
- Treat remedies as supportive practices, never promises.
- No internal notes or implementation language.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- partnership_signature
- commitment_pattern
- relationship_blocks
- readiness_path
- partnership_windows
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    current = report.output_payload
    return {
        "summary": report.summary,
        "partnership_signature": current.partnership_signature,
        "commitment_pattern": current.commitment_pattern,
        "relationship_blocks": current.relationship_blocks,
        "readiness_path": f"{current.readiness_path} These windows point to readiness themes, not guaranteed events.",
        "partnership_windows": [item.description for item in current.partnership_windows],
        "remedies": {
            "mantra_practice": current.remedies.mantra.practice,
            "gemstone_purpose": current.remedies.gemstone.purpose,
            "ritual": current.remedies.ritual,
        },
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    current = report.output_payload
    report.summary = str(content.get("summary") or report.summary)
    for field in ("partnership_signature", "commitment_pattern", "relationship_blocks", "readiness_path"):
        if content.get(field):
            setattr(current, field, str(content[field]))
    windows = content.get("partnership_windows")
    if isinstance(windows, list):
        for item, description in zip(current.partnership_windows, windows):
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


async def enrich_partnership_window_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=900)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
