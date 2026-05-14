from __future__ import annotations

from typing import Any

from love_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Soulmate Timing report for Everyday Horoscope.

Rules:
- Dasha windows are already computed.
- Do not recalculate timing or natal factors.
- Keep language premium, hopeful, grounded, and non-deterministic.
- No internal notes.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- timing_note
- peak_window_notes
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    return {
        "summary": report.summary,
        "timing_note": f"{report.output_payload.timing_note} These windows are best treated as seasons of openness, readiness, and better emotional timing rather than certainty.",
        "peak_window_notes": [item.note for item in report.output_payload.peak_windows],
        "remedies": list(report.output_payload.remedies),
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    report.summary = str(content.get("summary") or report.summary)
    report.output_payload.timing_note = str(content.get("timing_note") or report.output_payload.timing_note)
    peak_notes = content.get("peak_window_notes")
    if isinstance(peak_notes, list):
        for item, note in zip(report.output_payload.peak_windows, peak_notes):
            if str(note).strip():
                item.note = str(note)
    remedies = content.get("remedies")
    if isinstance(remedies, list) and remedies:
        report.output_payload.remedies = [str(item) for item in remedies if str(item).strip()]
    return report


async def enrich_soulmate_timing_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report))
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
