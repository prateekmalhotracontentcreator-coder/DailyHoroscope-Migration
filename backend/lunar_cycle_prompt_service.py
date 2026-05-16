from __future__ import annotations

from typing import Any

from love_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    return f"""
You are enriching a premium Vedic Lunar Cycle Wellness report for Everyday Horoscope.

Rules:
- The moon phase, nakshatra, cycle day, and natal context are already computed.
- Do not recalculate astronomy, dates, or house placements.
- Keep the tone calm, intimate, supportive, and spiritually grounded without sounding absolute.
- Keep each prose field under 120 words.
- `weekly_rhythm` must contain exactly 3 short strings.
- `recommended_practices` must contain exactly 3 items, each with `practice_name` and `description`.
- No internal notes.

Input:
- Existing summary: {report.summary}
- Output payload: {payload_json(report)}

Return valid JSON only with keys:
- summary
- phase_wellness_note
- nakshatra_wellness_note
- weekly_rhythm
- recommended_practices
- caution_note
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    output = report.output_payload
    phase = output.moon_phase.phase_name
    nakshatra = output.moon_nakshatra.name
    natal_sign = output.natal_context.natal_moon_sign
    transit_house = output.natal_context.transit_house
    return {
        "summary": report.summary,
        "phase_wellness_note": (
            f"The {phase} phase is a cue to work with your energy in measured waves. "
            f"Let your body set the pace, and use this part of the cycle to stay attentive to what feels replenishing rather than performative."
        ),
        "nakshatra_wellness_note": (
            f"Today's Moon in {nakshatra} interacts with your natal Moon in {natal_sign}, "
            f"bringing emphasis to the {transit_house}th-house themes now moving through your inner weather. "
            f"Treat this as guidance for rhythm and self-care, not a rigid rule."
        ),
        "weekly_rhythm": [
            "Front-load the week with your most nourishing routines while emotional clarity is easier to access.",
            "Keep one evening light and spacious so the nervous system can settle before the next emotional rise.",
            "Use the strongest moon days for reflection, gentle connection, and body-led pacing rather than over-scheduling.",
        ],
        "recommended_practices": [
            {
                "practice_name": "Moon Journal",
                "description": "Write for ten minutes at night on what your body, mood, and relationships are asking you to notice this week.",
            },
            {
                "practice_name": "Cooling Ritual",
                "description": "Use water, breath, or a simple evening walk to discharge emotional heat and return to steadier inner pacing.",
            },
            {
                "practice_name": "Sacred Rest Window",
                "description": "Protect one quiet window this week for silence, music, or prayer so the lunar cycle has room to integrate inwardly.",
            },
        ],
        "caution_note": (
            "If emotions feel amplified, avoid reading every wave as a final truth. "
            "Slow the pace, reduce noise, and let clarity return before making sensitive decisions."
        ),
    }


def _apply_content(report: Any, content: dict[str, Any]) -> Any:
    report.summary = str(content.get("summary") or report.summary)

    if content.get("phase_wellness_note"):
        report.output_payload.wellness.phase_wellness_note = str(content["phase_wellness_note"])
    if content.get("nakshatra_wellness_note"):
        report.output_payload.wellness.nakshatra_wellness_note = str(content["nakshatra_wellness_note"])
    if content.get("caution_note"):
        report.output_payload.wellness.caution_note = str(content["caution_note"])

    weekly_rhythm = content.get("weekly_rhythm")
    if isinstance(weekly_rhythm, list) and weekly_rhythm:
        cleaned = [str(item) for item in weekly_rhythm if str(item).strip()]
        if cleaned:
            report.output_payload.wellness.weekly_rhythm = cleaned[:3]

    practices = content.get("recommended_practices")
    if isinstance(practices, list) and practices:
        normalized: list[dict[str, str]] = []
        for item in practices:
            if not isinstance(item, dict):
                continue
            practice_name = str(item.get("practice_name") or "").strip()
            description = str(item.get("description") or "").strip()
            if practice_name and description:
                normalized.append({"practice_name": practice_name, "description": description})
        if normalized:
            report.output_payload.wellness.recommended_practices = normalized[:3]

    return report


async def enrich_lunar_cycle_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=750)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
