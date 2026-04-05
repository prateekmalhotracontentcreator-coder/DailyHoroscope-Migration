from __future__ import annotations

from typing import Any

from love_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Intimacy and Vitality report for Everyday Horoscope.

Rules:
- Windows, phases, and natal signatures are already computed.
- Do not recalculate transits or scores.
- Keep tone sensual-but-refined, emotionally intelligent, and non-explicit.
- No internal notes.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- natal_intimacy_signature
- current_vitality_phase
- peak_window_notes
- energy_navigation_tips
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    return {
        "summary": report.summary,
        "natal_intimacy_signature": f"{report.output_payload.natal_intimacy_signature} The strongest results come when trust and timing deepen together rather than being rushed.",
        "current_vitality_phase": f"{report.output_payload.current_vitality_phase} Read this as a tone map for energy, confidence, and emotional availability.",
        "peak_window_notes": [item.note for item in report.output_payload.peak_windows],
        "energy_navigation_tips": list(report.output_payload.energy_navigation_tips),
        "remedies": list(report.output_payload.remedies),
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    report.summary = str(content.get("summary") or report.summary)
    if content.get("natal_intimacy_signature"):
        report.output_payload.natal_intimacy_signature = str(content["natal_intimacy_signature"])
    if content.get("current_vitality_phase"):
        report.output_payload.current_vitality_phase = str(content["current_vitality_phase"])
    peak_notes = content.get("peak_window_notes")
    if isinstance(peak_notes, list):
        for item, note in zip(report.output_payload.peak_windows, peak_notes):
            if str(note).strip():
                item.note = str(note)
    for field in ("energy_navigation_tips", "remedies"):
        value = content.get(field)
        if isinstance(value, list) and value:
            setattr(report.output_payload, field, [str(item) for item in value if str(item).strip()])
    return report


async def enrich_intimacy_vitality_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report))
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
