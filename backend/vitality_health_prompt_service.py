from __future__ import annotations

from typing import Any

from individual_reports_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Vitality & Health Report for Everyday Horoscope.

Rules:
- The astrology has already been computed.
- Do not recalculate planets, houses, constitutions, or dasha timing.
- Keep the tone supportive, calm, and non-medical.
- Never diagnose, predict illness, or promise outcomes.
- Frame remedies and routines as spiritual and lifestyle support only.
- No internal notes or implementation language.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- vitality_signature
- pressure_pattern
- recovery_path
- daily_rhythm_guidance
- care_windows
- remedies
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    current = report.output_payload
    return {
        "summary": report.summary,
        "vitality_signature": current.vitality_signature,
        "pressure_pattern": current.pressure_pattern,
        "recovery_path": current.recovery_path,
        "daily_rhythm_guidance": f"{current.daily_rhythm_guidance} Use this as supportive rhythm guidance rather than certainty.",
        "care_windows": [item.description for item in current.care_windows],
        "remedies": {
            "mantra_practice": current.remedies.mantra.practice,
            "gemstone_purpose": current.remedies.gemstone.purpose,
            "ritual": current.remedies.ritual,
        },
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    current = report.output_payload
    report.summary = str(content.get("summary") or report.summary)
    for field in ("vitality_signature", "pressure_pattern", "recovery_path", "daily_rhythm_guidance"):
        if content.get(field):
            setattr(current, field, str(content[field]))
    windows = content.get("care_windows")
    if isinstance(windows, list):
        for item, description in zip(current.care_windows, windows):
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


async def enrich_vitality_health_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=900)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
