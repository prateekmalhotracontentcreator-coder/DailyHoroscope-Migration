from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from numerology_router import NumerologyReportPayload


DEFAULT_CLAUDE_MODEL = os.getenv("NUMEROLOGY_CLAUDE_MODEL", "claude-3-5-sonnet-latest")


def _computed_dump(report: NumerologyReportPayload) -> dict[str, Any]:
    dumped: dict[str, Any] = {}
    for key, value in report.computed_values.items():
        model_dump = getattr(value, "model_dump", None)
        dumped[key] = model_dump() if callable(model_dump) else value
    return dumped


def _build_prompt(report: NumerologyReportPayload, intro: str, rules: list[str], output_keys: list[str]) -> str:
    lines = [
        intro,
        "",
        "Rules:",
        *[f"- {rule}" for rule in rules],
        "",
        "Input:",
        f"- Tile code: {report.tile_code}",
        f"- Focus area: {report.focus_area}",
        f"- Computed values: {json.dumps(_computed_dump(report), ensure_ascii=True)}",
        f"- Calculation trace: {json.dumps(report.calculation_trace, ensure_ascii=True)}",
        "",
        "Return valid JSON only with keys:",
        *[f"- {key}" for key in output_keys],
    ]
    return "\n".join(lines).strip()


def _build_core_profile_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Numerology core-profile report for the Everyday Horoscope platform.",
        [
            "Numerology is backed by deterministic engine logic.",
            "Do not recalculate any numbers.",
            "Keep language premium, calm, practical, and non-deterministic.",
            "Do not make guaranteed claims.",
        ],
        [
            "hero_summary",
            "section_summaries",
            "practical_guidance",
            "remedy_note",
        ],
    )


def _build_name_correction_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Numerology name correction and energy-alignment report for the Everyday Horoscope platform.",
        [
            "Name-alignment values are already computed.",
            "Do not recalculate any numbers.",
            "Keep language premium, practical, and non-deterministic.",
            "Do not imply a name change guarantees success, marriage, money, or fame.",
        ],
        [
            "hero_summary",
            "baseline_summary",
            "current_name_summary",
            "alignment_summary",
            "practical_guidance",
            "caution_note",
        ],
    )


def _build_timing_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Numerology timing report for the Everyday Horoscope platform.",
        [
            "Timing values are already computed.",
            "Do not recalculate any numbers.",
            "Keep language premium, composed, practical, and non-deterministic.",
            "Do not make guaranteed claims about dates or outcomes.",
        ],
        [
            "hero_summary",
            "year_theme",
            "monthly_highlights",
            "action_guidance",
            "caution_guidance",
        ],
    )


def _build_karmic_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Numerology karmic debt and Lo Shu remediation report for the Everyday Horoscope platform.",
        [
            "Karmic and Lo Shu values are already computed.",
            "Do not recalculate any numbers.",
            "Frame karmic debt as lesson patterns, not punishments.",
            "Frame remedies as supportive and optional, never guaranteed.",
        ],
        [
            "hero_summary",
            "debt_summary",
            "loshu_summary",
            "remedy_guidance",
            "caution_guidance",
        ],
    )


def _build_relationship_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Numerology relationship compatibility report for the Everyday Horoscope platform.",
        [
            "Compatibility values are already computed.",
            "Do not recalculate any numbers.",
            "Explain harmony and friction without certainty or fear.",
            "Treat mixed compatibility as an invitation to understand pace, communication, and adjustment.",
        ],
        [
            "hero_summary",
            "harmony_summary",
            "friction_summary",
            "practical_adjustments",
            "timing_note",
        ],
    )


def _build_career_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Numerology career guidance report for the Everyday Horoscope platform.",
        [
            "Career values are already computed.",
            "Do not recalculate any numbers.",
            "Keep the guidance practical, premium, and non-deterministic.",
            "Do not claim a single job title is guaranteed by numerology.",
        ],
        [
            "hero_summary",
            "talent_summary",
            "direction_summary",
            "environment_summary",
            "practical_guidance",
        ],
    )


def _build_digital_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Numerology digital vibration report for the Everyday Horoscope platform.",
        [
            "Digital-vibration values are already computed.",
            "Do not recalculate any numbers.",
            "Keep language practical, premium, and non-deterministic.",
            "Do not claim guaranteed luck.",
        ],
        [
            "hero_summary",
            "vibration_summary",
            "compatibility_summary",
            "practical_guidance",
            "caution_note",
        ],
    )


def _build_residential_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Numerology residential compatibility report for the Everyday Horoscope platform.",
        [
            "Residential values are already computed.",
            "Do not recalculate any numbers.",
            "Keep language practical, premium, and non-deterministic.",
            "Treat the report as a home-fit and environment-alignment signal.",
        ],
        [
            "hero_summary",
            "vibration_summary",
            "compatibility_summary",
            "practical_guidance",
            "caution_note",
        ],
    )


def _build_business_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Numerology business and brand-name optimization report for the Everyday Horoscope platform.",
        [
            "Brand values are already computed.",
            "Do not recalculate any numbers.",
            "Keep language practical, premium, and non-deterministic.",
            "Do not imply a name alone guarantees business success.",
        ],
        [
            "hero_summary",
            "alignment_summary",
            "vibration_summary",
            "practical_guidance",
            "caution_note",
        ],
    )


def _build_baby_name_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Numerology baby-name selection report for the Everyday Horoscope platform.",
        [
            "Name values are already computed.",
            "Do not recalculate any numbers.",
            "Keep language practical, premium, and non-deterministic.",
            "Do not imply one candidate name guarantees the child's future.",
        ],
        [
            "hero_summary",
            "baseline_summary",
            "candidate_summary",
            "practical_guidance",
            "caution_note",
        ],
    )


def _build_premium_ankjyotish_prompt(report: NumerologyReportPayload) -> str:
    return _build_prompt(
        report,
        "You are writing a premium Ankjyotish report for the Everyday Horoscope platform that blends deterministic numerology with Temple-provided Vedic context.",
        [
            "All numerology calculations and Vedic reference fields are already computed.",
            "Do not recalculate any numbers, signs, nakshatras, or timings.",
            "Use Lagna, Moon Sign, and Nakshatra only as interpretive cross-reference layers.",
            "Keep language premium, composed, Vedic-aware, practical, and non-deterministic.",
            "Do not include developer notes, integration instructions, JSON paths, or internal references.",
            "Remedial suggestions must feel grounded, optional, and user-facing.",
        ],
        [
            "hero_summary",
            "core_profile_summary",
            "loshu_summary",
            "karmic_summary",
            "timing_summary",
            "name_summary",
            "vedic_summary",
            "lucky_elements_summary",
            "remediation_intro",
            "guidance",
            "remedy_note",
        ],
    )


def _extract_text_from_claude_response(response: Any) -> str | None:
    content = getattr(response, "content", None)
    if not content:
        return None
    text_parts: list[str] = []
    for item in content:
        text_value = getattr(item, "text", None)
        if text_value:
            text_parts.append(text_value)
    return "\n".join(text_parts).strip() if text_parts else None


async def _try_claude_generation(prompt: str) -> dict[str, Any] | None:
    try:
        from anthropic import AsyncAnthropic  # type: ignore
    except Exception:
        return None

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    client = AsyncAnthropic(api_key=api_key)
    try:
        response = await client.messages.create(
            model=DEFAULT_CLAUDE_MODEL,
            max_tokens=1100,
            temperature=0.45,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception:
        return None

    text = _extract_text_from_claude_response(response)
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def _fallback_core_profile_content(report: NumerologyReportPayload) -> dict[str, Any]:
    life_path = report.computed_values["life_path"].reduced
    expression = report.computed_values["expression"].reduced
    soul_urge = report.computed_values["soul_urge"].reduced
    personality = report.computed_values["personality"].reduced
    return {
        "hero_summary": f"Your core profile centers on Life Path {life_path}, Expression {expression}, Soul Urge {soul_urge}, and Personality {personality}.",
        "section_summaries": {
            "life_path": f"Life Path {life_path} describes the larger rhythm shaping your direction and learning pattern.",
            "expression": f"Expression {expression} reflects how your talents and public output tend to become visible.",
            "soul_urge": f"Soul Urge {soul_urge} points to the deeper motivations that feel personally meaningful.",
            "personality": f"Personality {personality} describes the outer style others may encounter first.",
        },
        "practical_guidance": "Use the Life Path as the anchor, then refine decisions through your name-derived numbers, timing, and environment fit.",
        "remedy_note": "If path and expression feel misaligned, the next layers to explore are timing, Lo Shu balance, or name alignment.",
    }


def _fallback_name_correction_content(report: NumerologyReportPayload) -> dict[str, Any]:
    compat = report.calculation_trace.get("compatibility", {})
    return {
        "hero_summary": "This report compares your current public-name vibration with your birth-name baseline to estimate energetic fit.",
        "baseline_summary": f"Your birth-name baseline centers on Expression {report.computed_values['birth_expression'].reduced} and Soul Urge {report.computed_values['birth_soul_urge'].reduced}.",
        "current_name_summary": f"Your current name usage reduces to {report.computed_values['current_name_expression'].reduced} as a live public-name vibration.",
        "alignment_summary": f"The current overall name-alignment score is {compat.get('overall_score', 'n/a')}.",
        "practical_guidance": "Use this result to compare spelling choices and public identity fit rather than treating one form as magically perfect.",
        "caution_note": "No name correction should be treated as a substitute for timing, effort, or practical life choices.",
    }


def _fallback_timing_content(report: NumerologyReportPayload) -> dict[str, Any]:
    personal_year = report.computed_values["personal_year"].reduced
    return {
        "hero_summary": f"Your Personal Year {personal_year} shapes the rhythm of {report.target_year}.",
        "year_theme": "Treat the year as a numerological season with its own pace, emphasis, and decision style.",
        "monthly_highlights": [
            "Some periods will support visible movement more naturally than others.",
            "Slower phases are often better for review, repair, and preparation.",
            "Use timing as a rhythm guide, not as certainty.",
        ],
        "action_guidance": "Move when the year feels supportive and use quieter windows to refine your approach.",
        "caution_guidance": "Do not treat any single timing signal as a guarantee; it works best alongside practical judgment.",
    }


def _fallback_karmic_content(report: NumerologyReportPayload) -> dict[str, Any]:
    trace = report.calculation_trace
    karmic_debts = trace.get("karmic_debts", [])
    loshu = trace.get("loshu", {})
    missing_numbers = loshu.get("missing_numbers", [])
    repeated_numbers = loshu.get("repeated_numbers", [])
    return {
        "hero_summary": "This report highlights karmic lesson patterns alongside Lo Shu gaps and repetitions that may need more conscious balance.",
        "debt_summary": f"Detected karmic debt indicators: {', '.join(str(item) for item in karmic_debts) if karmic_debts else 'none'}.",
        "loshu_summary": f"Missing numbers: {', '.join(str(item) for item in missing_numbers) if missing_numbers else 'none'}. Repeated numbers: {', '.join(str(item) for item in repeated_numbers) if repeated_numbers else 'none'}.",
        "remedy_guidance": "Use remedial steps to create steadier balance in environment, rhythm, and self-correction rather than expecting sudden transformation.",
        "caution_guidance": "Treat remedial suggestions as supportive practices, not guarantees around health, money, or relationships.",
    }


def _fallback_relationship_content(report: NumerologyReportPayload) -> dict[str, Any]:
    compat = report.calculation_trace.get("compatibility", {})
    return {
        "hero_summary": f"This compatibility reading suggests an overall relationship score of {compat.get('overall_score', 'n/a')}.",
        "harmony_summary": "Supportive compatibility usually appears where values, pace, or emotional needs can meet with less strain.",
        "friction_summary": "Mixed areas do not predict failure, but they do show where communication and pacing matter more.",
        "practical_adjustments": "Use the report to identify where patience, translation, and emotional timing may improve the bond.",
        "timing_note": "A timing report can add another layer by showing when practical or emotional decisions may be better supported.",
    }


def _fallback_career_content(report: NumerologyReportPayload) -> dict[str, Any]:
    clusters = report.calculation_trace.get("career_clusters", {})
    return {
        "hero_summary": "This report translates your numerology profile into professional strengths, direction, and environment fit rather than a rigid career label.",
        "talent_summary": f"Your visible strengths appear connected to the {clusters.get('talent', 'general development')} pattern.",
        "direction_summary": f"Your longer-range work direction appears connected to the {clusters.get('mission', 'general development')} pattern.",
        "environment_summary": f"Your more sustainable work environment may align with the {clusters.get('environment', 'general development')} pattern.",
        "practical_guidance": "Use the report to choose roles and settings that fit both your visible strengths and your deeper motivational pattern.",
    }


def _fallback_digital_content(report: NumerologyReportPayload) -> dict[str, Any]:
    compat = report.calculation_trace.get("compatibility", {})
    return {
        "hero_summary": "This report treats your chosen number as a symbolic vibration and compares it with your native profile.",
        "vibration_summary": f"The number creates a reduced vibration of {report.computed_values['digital_vibration'].reduced}.",
        "compatibility_summary": f"The current overall harmony score is {compat.get('overall_score', 'n/a')}.",
        "practical_guidance": "Use digital-vibration checks as a comparison tool when choosing between multiple numbers.",
        "caution_note": "Do not treat a digital-number result as more important than the broader timing and identity patterns in your full profile.",
    }


def _fallback_residential_content(report: NumerologyReportPayload) -> dict[str, Any]:
    compat = report.calculation_trace.get("compatibility", {})
    return {
        "hero_summary": "This report treats your house number as an environmental vibration and compares it with your native profile.",
        "vibration_summary": f"The home reduces to a residential vibration of {report.computed_values['residential_vibration'].reduced}.",
        "compatibility_summary": f"The current overall home-fit score is {compat.get('overall_score', 'n/a')}.",
        "practical_guidance": "Use residential compatibility as a home-awareness tool alongside comfort, lived experience, and remedial balance.",
        "caution_note": "A mixed result does not automatically mean the home is wrong; it may simply mean balance matters more.",
    }


def _fallback_business_content(report: NumerologyReportPayload) -> dict[str, Any]:
    compat = report.calculation_trace.get("compatibility", {})
    return {
        "hero_summary": "This report compares the brand name with the founder profile to estimate naming fit and symbolic business alignment.",
        "alignment_summary": f"The current founder-to-brand optimization score is {compat.get('overall_score', 'n/a')}.",
        "vibration_summary": f"The business name creates a reduced brand vibration of {report.computed_values['business_expression'].reduced}.",
        "practical_guidance": "Use this as a decision-support layer alongside branding clarity, audience fit, and real-world usability.",
        "caution_note": "A stronger score can support confidence, but no name replaces business model, timing, or execution.",
    }


def _fallback_baby_name_content(report: NumerologyReportPayload) -> dict[str, Any]:
    compat = report.calculation_trace.get("compatibility", {})
    return {
        "hero_summary": "This report compares a candidate name with the child's birth vibration to estimate naming harmony and suitability.",
        "baseline_summary": f"The child's Life Path baseline is {report.computed_values['life_path'].reduced}.",
        "candidate_summary": f"The current name-fit score is {compat.get('overall_score', 'n/a')}.",
        "practical_guidance": "Use this result to compare naming options while also considering family resonance, pronunciation, and long-term comfort.",
        "caution_note": "No candidate name should be treated as a guarantee of the child's future.",
    }


def _fallback_premium_ankjyotish_content(report: NumerologyReportPayload) -> dict[str, Any]:
    lo_shu = report.calculation_trace.get("lo_shu_grid_payload", {})
    karmic = report.calculation_trace.get("karmic_debts", [])
    lucky = report.calculation_trace.get("lucky_elements_table", {})
    vedic = report.calculation_trace.get("vedic_cross_reference", {})
    name_alignment = report.calculation_trace.get("name_alignment")
    return {
        "hero_summary": "This premium Ankjyotish report blends your core numerology with a Vedic cross-reference layer to create a more complete life-alignment reading.",
        "core_profile_summary": (
            f"Life Path {report.computed_values['life_path'].reduced}, Expression {report.computed_values['expression'].reduced}, "
            f"Soul Urge {report.computed_values['soul_urge'].reduced}, and Personality {report.computed_values['personality'].reduced} form the base blueprint."
        ),
        "loshu_summary": (
            f"Missing numbers: {', '.join(str(item) for item in lo_shu.get('missing_numbers', [])) or 'none'}. "
            f"Repeated numbers: {', '.join(str(item) for item in lo_shu.get('repeated_numbers', [])) or 'none'}."
        ),
        "karmic_summary": (
            f"Karmic debt indicators: {', '.join(str(item) for item in karmic) if karmic else 'none'}. "
            "Read them as recurring life lessons rather than punishment."
        ),
        "timing_summary": (
            f"Current timing reads as Personal Year {report.computed_values['personal_year'].reduced}, "
            f"Personal Month {report.computed_values['personal_month'].reduced}, and Personal Day {report.computed_values['personal_day'].reduced}."
        ),
        "name_summary": (
            f"Your current-name alignment reads as {name_alignment.get('band', 'baseline-only')}."
            if isinstance(name_alignment, dict)
            else "No current popular name was supplied, so this section remains anchored to the birth-name baseline."
        ),
        "vedic_summary": (
            f"Lagna {vedic.get('lagna_sign', report.lagna_sign)}, Moon Sign {vedic.get('moon_sign', report.moon_sign)}, "
            f"and Nakshatra {vedic.get('nakshatra_name', report.nakshatra_name)} add a symbolic Vedic layer to the numerology reading."
        ),
        "lucky_elements_summary": (
            f"Dominant element: {lucky.get('dominant_element', 'Balanced')}. "
            f"Supportive day: {lucky.get('supportive_day', 'Thursday')}."
        ),
        "remediation_intro": "Use the seven-day plan as a grounded reset cycle to turn insight into daily action rather than superstition.",
        "guidance": "Let this report guide identity, timing, name usage, and remedial discipline together instead of relying on any one signal in isolation.",
        "remedy_note": "Supportive colors, days, and daily practices work best when they reinforce clarity, consistency, and conscious decision-making.",
    }


def _set_section(report: NumerologyReportPayload, section_id: str, summary: str | None = None, body: str | None = None) -> None:
    for section in report.report_sections:
        if section.section_id != section_id:
            continue
        if summary:
            section.summary = summary
        if body:
            section.body = body
        break


def _apply_core_profile_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    summaries = content.get("section_summaries", {})
    _set_section(report, "life_path_blueprint", summary=summaries.get("life_path"))
    _set_section(report, "expression_potential", summary=summaries.get("expression"))
    inner_summary = " ".join(part for part in [summaries.get("soul_urge"), summaries.get("personality")] if part)
    _set_section(report, "inner_drivers", summary=inner_summary or None)
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("practical_guidance", report.guidance)
    report.remedy_note = content.get("remedy_note", report.remedy_note)
    return report


def _apply_name_correction_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    _set_section(report, "birth_name_baseline", summary=content.get("baseline_summary"))
    _set_section(report, "current_name_reading", summary=content.get("current_name_summary"))
    _set_section(report, "alignment_score", summary=content.get("alignment_summary"), body=content.get("practical_guidance"))
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("practical_guidance", report.guidance)
    report.remedy_note = content.get("caution_note", report.remedy_note)
    return report


def _apply_timing_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    _set_section(report, "timing_overview", summary=content.get("year_theme"))
    highlights = content.get("monthly_highlights")
    body = " ".join(str(item) for item in highlights) if isinstance(highlights, list) else None
    _set_section(report, "timing_windows", body=body)
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("action_guidance", report.guidance)
    report.remedy_note = content.get("caution_guidance", report.remedy_note)
    return report


def _apply_karmic_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    _set_section(report, "karmic_debt", summary=content.get("debt_summary"))
    _set_section(report, "loshu_grid", summary=content.get("loshu_summary"))
    _set_section(report, "remediation", body=content.get("remedy_guidance"))
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("remedy_guidance", report.guidance)
    report.remedy_note = content.get("caution_guidance", report.remedy_note)
    return report


def _apply_relationship_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    _set_section(report, "relationship_overview", summary=content.get("hero_summary"))
    _set_section(report, "harmony", summary=content.get("harmony_summary"))
    _set_section(report, "friction", summary=content.get("friction_summary"))
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("practical_adjustments", report.guidance)
    report.remedy_note = content.get("timing_note", report.remedy_note)
    return report


def _apply_career_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    _set_section(report, "talent_inventory", summary=content.get("talent_summary"))
    _set_section(report, "mission_direction", summary=content.get("direction_summary"))
    _set_section(report, "environment_fit", summary=content.get("environment_summary"))
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("practical_guidance", report.guidance)
    return report


def _apply_digital_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    _set_section(report, "digital_vibration", summary=content.get("vibration_summary"))
    _set_section(report, "compatibility_score", summary=content.get("compatibility_summary"))
    _set_section(report, "practical_takeaways", body=content.get("practical_guidance"))
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("practical_guidance", report.guidance)
    report.remedy_note = content.get("caution_note", report.remedy_note)
    return report


def _apply_residential_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    _set_section(report, "home_vibration", summary=content.get("vibration_summary"))
    _set_section(report, "compatibility_score", summary=content.get("compatibility_summary"))
    _set_section(report, "practical_takeaways", body=content.get("practical_guidance"))
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("practical_guidance", report.guidance)
    report.remedy_note = content.get("caution_note", report.remedy_note)
    return report


def _apply_business_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    _set_section(report, "brand_alignment", summary=content.get("alignment_summary"))
    _set_section(report, "brand_vibration", summary=content.get("vibration_summary"))
    _set_section(report, "practical_takeaways", body=content.get("practical_guidance"))
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("practical_guidance", report.guidance)
    report.remedy_note = content.get("caution_note", report.remedy_note)
    return report


def _apply_baby_name_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    _set_section(report, "birth_baseline", summary=content.get("baseline_summary"))
    _set_section(report, "candidate_fit", summary=content.get("candidate_summary"))
    _set_section(report, "practical_takeaways", body=content.get("practical_guidance"))
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("practical_guidance", report.guidance)
    report.remedy_note = content.get("caution_note", report.remedy_note)
    return report


def _apply_premium_ankjyotish_content(report: NumerologyReportPayload, content: dict[str, Any]) -> NumerologyReportPayload:
    _set_section(report, "core_number_profile", summary=content.get("core_profile_summary"))
    _set_section(report, "lo_shu_grid", summary=content.get("loshu_summary"))
    _set_section(report, "karmic_debt_audit", summary=content.get("karmic_summary"))
    _set_section(report, "timing_window", summary=content.get("timing_summary"))
    _set_section(report, "name_vibration_analysis", summary=content.get("name_summary"))
    _set_section(report, "vedic_cross_reference", summary=content.get("vedic_summary"))
    _set_section(report, "lucky_elements_table", summary=content.get("lucky_elements_summary"))
    _set_section(report, "remediation_plan", body=content.get("remediation_intro"))
    report.summary = content.get("hero_summary", report.summary)
    report.guidance = content.get("guidance", report.guidance)
    report.remedy_note = content.get("remedy_note", report.remedy_note)
    return report


async def enrich_numerology_report_with_claude(report: NumerologyReportPayload) -> NumerologyReportPayload:
    if report.tile_code == "life_path_soul_mission":
        content = await _try_claude_generation(_build_core_profile_prompt(report))
        return _apply_core_profile_content(report, content or _fallback_core_profile_content(report))
    if report.tile_code == "name_correction_energy_alignment":
        content = await _try_claude_generation(_build_name_correction_prompt(report))
        return _apply_name_correction_content(report, content or _fallback_name_correction_content(report))
    if report.tile_code == "favorable_timing":
        content = await _try_claude_generation(_build_timing_prompt(report))
        return _apply_timing_content(report, content or _fallback_timing_content(report))
    if report.tile_code == "karmic_debt_loshu":
        content = await _try_claude_generation(_build_karmic_prompt(report))
        return _apply_karmic_content(report, content or _fallback_karmic_content(report))
    if report.tile_code == "relationship_compatibility":
        content = await _try_claude_generation(_build_relationship_prompt(report))
        return _apply_relationship_content(report, content or _fallback_relationship_content(report))
    if report.tile_code == "career_guidance":
        content = await _try_claude_generation(_build_career_prompt(report))
        return _apply_career_content(report, content or _fallback_career_content(report))
    if report.tile_code == "lucky_digital_vibrations":
        content = await _try_claude_generation(_build_digital_prompt(report))
        return _apply_digital_content(report, content or _fallback_digital_content(report))
    if report.tile_code == "residential_compatibility":
        content = await _try_claude_generation(_build_residential_prompt(report))
        return _apply_residential_content(report, content or _fallback_residential_content(report))
    if report.tile_code == "business_brand_optimization":
        content = await _try_claude_generation(_build_business_prompt(report))
        return _apply_business_content(report, content or _fallback_business_content(report))
    if report.tile_code == "baby_name_selection":
        content = await _try_claude_generation(_build_baby_name_prompt(report))
        return _apply_baby_name_content(report, content or _fallback_baby_name_content(report))
    if report.tile_code == "premium_ankjyotish_report":
        content = await _try_claude_generation(_build_premium_ankjyotish_prompt(report))
        return _apply_premium_ankjyotish_content(report, content or _fallback_premium_ankjyotish_content(report))
    return report
