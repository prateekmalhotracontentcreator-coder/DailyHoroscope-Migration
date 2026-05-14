from __future__ import annotations

from typing import Any

from love_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Encounter Window report for Everyday Horoscope.

Rules:
- The transit windows have already been computed.
- Do not recalculate dates, orbs, or window logic.
- Keep language warm, premium, grounded, and non-deterministic.
- No developer-facing notes.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- headline
- personalized_context
- window_notes
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    return {
        "summary": report.summary,
        "headline": report.output_payload.current_status.headline if report.output_payload.current_status.active else "A meaningful opening is ahead, and this report shows where your strongest encounter windows begin to gather.",
        "personalized_context": f"{report.output_payload.personalized_context} When one of these windows opens, the goal is not to force connection, but to become more available to what already feels naturally responsive.",
        "window_notes": [f"{item.note} Use this span for visibility, soft confidence, and simple social movement." for item in report.output_payload.peak_windows],
        "remedies": list(report.output_payload.remedies),
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    report.summary = str(content.get("summary") or report.summary)
    report.output_payload.current_status.headline = str(content.get("headline") or report.output_payload.current_status.headline)
    report.output_payload.personalized_context = str(content.get("personalized_context") or report.output_payload.personalized_context)
    notes = content.get("window_notes")
    if isinstance(notes, list):
        for item, note in zip(report.output_payload.peak_windows, notes):
            if str(note).strip():
                item.note = str(note)
    remedies = content.get("remedies")
    if isinstance(remedies, list) and remedies:
        report.output_payload.remedies = [str(item) for item in remedies if str(item).strip()]
    return report


async def enrich_encounter_window_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report))
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
