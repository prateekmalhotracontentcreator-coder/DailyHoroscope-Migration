from __future__ import annotations

from typing import Any

from love_prompt_common import payload_json, try_claude_generation


def _build_prompt(report: Any) -> str:
    output = report.output_payload
    phase = output.moon_phase.phase_name
    cycle_day = output.moon_phase.cycle_day
    illumination = output.moon_phase.illumination_pct
    days_to_full = output.moon_phase.days_to_full_moon
    days_to_new = output.moon_phase.days_to_new_moon
    nakshatra = output.moon_nakshatra.name
    pada = output.moon_nakshatra.pada
    lord = output.moon_nakshatra.lord
    natal_sign = output.natal_context.natal_moon_sign
    transit_house = output.natal_context.transit_house
    return f"""
You are writing a premium Vedic Lunar Cycle Wellness report for Everyday Horoscope.
The user's astronomical data is already computed. Your job is enrichment, not calculation.

Current lunar snapshot:
- Phase: {phase} (cycle day {cycle_day}/30, illumination {illumination}%)
- Days to Full Moon: {days_to_full} | Days to New Moon: {days_to_new}
- Moon Nakshatra: {nakshatra} Pada {pada} (lord: {lord})
- User's Natal Moon Sign: {natal_sign}
- Moon is currently transiting their {transit_house}th natal house

Existing summary line: {report.summary}
Existing output payload: {payload_json(report)}

RULES:
1. Reference the specific phase name, nakshatra name, natal sign, and house number explicitly in the prose.
2. `phase_wellness_note`: 3 paragraphs. Cover (a) what this phase energetically means for the body and mood, (b) what activities or decisions it supports and which it does not, (c) how this interacts with the user's natal Moon in {natal_sign}.
3. `nakshatra_wellness_note`: 2 paragraphs. Cover (a) the quality and character of {nakshatra} and how it colours the emotional field, (b) specific wellness implications for this nakshatra transit through the {transit_house}th house.
4. `weekly_rhythm`: exactly 3 strings. Each string must be a concrete scheduling or pacing principle for the week.
5. `recommended_practices`: exactly 3 items. Each item has `practice_name` (3 to 5 words) and `description` (2 to 3 sentences describing what to do, when, and why it works for this phase and nakshatra combination).
6. `caution_note`: exactly 2 sentences. One thing to genuinely watch for this week and one reframe.
7. `action_tracker`: exactly 7 items, one per day Monday through Sunday. Each item must have `day`, `intention` (3 to 7 words), and `action` (one concrete sentence describing one specific thing to do or avoid).
8. `summary`: one compelling sentence under 25 words summarising this week's lunar quality for the user.

TONE:
- Warm, intimate, precise, grounded, and practically useful.
- Never generic astrology boilerplate.
- Never use phrases like "the universe is guiding you" or "listen to your heart".
- Speak to actual rhythms, practices, and decisions.

Return valid JSON only with keys:
summary, phase_wellness_note, nakshatra_wellness_note, weekly_rhythm,
recommended_practices, caution_note, action_tracker
""".strip()


def _fallback_content(report: Any) -> dict[str, Any]:
    output = report.output_payload
    phase = output.moon_phase.phase_name
    is_waxing = phase in {"New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous"}
    nakshatra = output.moon_nakshatra.name
    pada = output.moon_nakshatra.pada
    lord = output.moon_nakshatra.lord
    natal_sign = output.natal_context.natal_moon_sign
    transit_house = output.natal_context.transit_house
    return {
        "summary": report.summary,
        "phase_wellness_note": (
            f"The {phase} phase asks you to work with your energy in pulses rather than in one long push. Body, mood, and attention all respond differently here, and the most useful question is not how much you can force, but what kind of rhythm your system can genuinely sustain.\n\n"
            f"In practical terms, {phase} energy is better for {'building, initiating, and gently increasing outward movement' if is_waxing else 'editing, releasing, simplifying, and reducing unnecessary load'}. It is less supportive for emotionally loaded decisions made in haste, especially when you are already overstimulated.\n\n"
            f"Because your natal Moon sits in {natal_sign}, this phase tends to interact with your emotional baseline through comfort, safety, and pacing. Treat that as instruction: regulate first, decide second."
        ),
        "nakshatra_wellness_note": (
            f"The Moon is moving through {nakshatra} Pada {pada}, under the rulership of {lord}, which gives the emotional field a particular texture. {nakshatra} tends to shape how feeling becomes behaviour, so this is less about abstract spirituality and more about how tone, atmosphere, and bodily sensitivity are changing around you.\n\n"
            f"Because this transit is moving through your {transit_house}th natal house while your natal Moon is in {natal_sign}, the wellness message is specific: simplify the part of life that feels emotionally busiest, and make your care practices small enough to repeat without resistance."
        ),
        "weekly_rhythm": [
            "Front-load the week with the decisions that need emotional steadiness, not the ones that can wait until you feel more reactive.",
            "Keep one evening minimally scheduled so the nervous system has room to reset before pressure starts to accumulate.",
            "Use repetition this week: similar sleep timing, similar meals, and one familiar calming ritual will help more than novelty.",
        ],
        "recommended_practices": [
            {
                "practice_name": "Moon Journal",
                "description": f"Write for ten minutes at the same time each evening on mood, energy, and what made you feel more or less regulated. This helps you track how the {phase} phase is actually landing in your body instead of guessing from memory.",
            },
            {
                "practice_name": "Phase-Aligned Reset",
                "description": f"{'Begin the day with one deliberate act of forward motion, like planning, outreach, or focused work.' if is_waxing else 'End the day by closing loops, clearing surfaces, or reducing mental clutter before sleep.'} The point is to cooperate with the phase instead of fighting its direction.",
            },
            {
                "practice_name": "Body Quiet Window",
                "description": f"Protect one 20-minute window this week for quiet, breath, walking, bathing, or prayer with no multitasking. {nakshatra} responds well when the body is given one undisturbed container to settle and integrate.",
            },
        ],
        "caution_note": (
            "If a feeling becomes intense quickly, do not assume it is automatically accurate. "
            "Let the lunar weather settle a little, then return to the situation with more context and a steadier body."
        ),
        "action_tracker": [
            {
                "day": "Monday",
                "intention": "Set the week's anchor",
                "action": "Write one clear intention for the week before checking messages." if is_waxing else "Review last week's open threads before opening anything new.",
            },
            {
                "day": "Tuesday",
                "intention": "Forward motion",
                "action": "Schedule your most demanding task in the morning window." if is_waxing else "Delegate or defer anything non-essential.",
            },
            {
                "day": "Wednesday",
                "intention": "Connection and communication",
                "action": "Initiate a meaningful conversation or collaboration." if is_waxing else "Listen more than you speak in group settings today.",
            },
            {
                "day": "Thursday",
                "intention": "Energy check",
                "action": "Notice your energy at noon and use it as a guide for the rest of the week." if is_waxing else "Protect your afternoon for restorative, solo work.",
            },
            {
                "day": "Friday",
                "intention": "Consolidate gains",
                "action": "Finish what you started and resist opening new projects." if is_waxing else "Close loops rather than beginning anything new.",
            },
            {
                "day": "Saturday",
                "intention": "Nourish the body",
                "action": "Spend 20 minutes outdoors, ideally near water or greenery." if is_waxing else "Extra rest today is not laziness; it is phase-appropriate recovery.",
            },
            {
                "day": "Sunday",
                "intention": "Inner review",
                "action": "Journal briefly on what expanded this week and what drained you." if is_waxing else "Set tomorrow's one priority before the evening ends.",
            },
        ],
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

    action_tracker_raw = content.get("action_tracker")
    if isinstance(action_tracker_raw, list) and action_tracker_raw:
        parsed_days = []
        for item in action_tracker_raw:
            if not isinstance(item, dict):
                continue
            day = str(item.get("day") or "").strip()
            intention = str(item.get("intention") or "").strip()
            action = str(item.get("action") or "").strip()
            if day and intention and action:
                parsed_days.append({"day": day, "intention": intention, "action": action})
        if parsed_days:
            tracker_model = report.output_payload.action_tracker.__class__
            report.output_payload.action_tracker = tracker_model(days=parsed_days[:7])

    return report


async def enrich_lunar_cycle_with_claude(report: Any, context: dict[str, Any]) -> Any:
    content = await try_claude_generation(_build_prompt(report), max_tokens=1800)
    if not isinstance(content, dict):
        content = _fallback_content(report)
    return _apply_content(report, content)
