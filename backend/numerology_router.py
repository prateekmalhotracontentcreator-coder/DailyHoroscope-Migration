from __future__ import annotations

import re
from collections import Counter
from datetime import date, datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field


router = APIRouter(prefix="/api/numerology", tags=["numerology"])

MASTER_NUMBERS = {11, 22, 33}
KARMIC_DEBT_NUMBERS = {13, 14, 16, 19}
VOWELS = {"A", "E", "I", "O", "U"}

PYTHAGOREAN_MAP = {
    "A": 1, "J": 1, "S": 1,
    "B": 2, "K": 2, "T": 2,
    "C": 3, "L": 3, "U": 3,
    "D": 4, "M": 4, "V": 4,
    "E": 5, "N": 5, "W": 5,
    "F": 6, "O": 6, "X": 6,
    "G": 7, "P": 7, "Y": 7,
    "H": 8, "Q": 8, "Z": 8,
    "I": 9, "R": 9,
}

CHALDEAN_MAP = {
    "A": 1, "I": 1, "J": 1, "Q": 1, "Y": 1,
    "B": 2, "K": 2, "R": 2,
    "C": 3, "G": 3, "L": 3, "S": 3,
    "D": 4, "M": 4, "T": 4,
    "E": 5, "H": 5, "N": 5, "X": 5,
    "U": 6, "V": 6, "W": 6,
    "O": 7, "Z": 7,
    "F": 8, "P": 8,
}

PLANE_NUMBERS = {
    "mental_4_9_2": (4, 9, 2),
    "emotional_3_5_7": (3, 5, 7),
    "practical_8_1_6": (8, 1, 6),
    "will_9_5_1": (9, 5, 1),
    "action_2_7_6": (2, 7, 6),
}

SUFFIX_PATTERN = re.compile(r"\b(JR|SR|III|II|IV|V)\b\.?", re.IGNORECASE)
NON_ALPHA_PATTERN = re.compile(r"[^A-Z\s]")
NON_DIGIT_PATTERN = re.compile(r"\D")
MULTISPACE_PATTERN = re.compile(r"\s+")

NumerologyTileCode = Literal[
    "life_path_soul_mission",
    "name_correction_energy_alignment",
    "favorable_timing",
    "karmic_debt_loshu",
    "relationship_compatibility",
    "career_guidance",
    "lucky_digital_vibrations",
    "residential_compatibility",
    "business_brand_optimization",
    "baby_name_selection",
]
NumerologySystem = Literal["pythagorean", "chaldean"]
ReductionMethod = Literal["grouping", "raw_sum"]
YMode = Literal["auto", "vowel", "consonant"]
FocusArea = Literal["general", "career", "love", "health", "wealth", "purpose"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NumerologyGenerateRequest(StrictModel):
    tile_code: NumerologyTileCode = "life_path_soul_mission"
    full_birth_name: str
    date_of_birth: str
    current_popular_name: str | None = None
    partner_full_birth_name: str | None = None
    partner_date_of_birth: str | None = None
    digital_identifier: str | None = None
    residential_number: str | None = None
    business_name: str | None = None
    candidate_name: str | None = None
    language: str = "en"
    focus_area: FocusArea = "general"
    numerology_system: NumerologySystem = "pythagorean"
    reduction_method: ReductionMethod = "grouping"
    y_mode: YMode = "auto"
    target_year: int | None = None


class NumerologyNumberValue(StrictModel):
    raw: int
    reduced: int
    master_number: int | None = None


class NumerologyReportSection(StrictModel):
    section_id: str
    title: str
    summary: str
    body: str


class NumerologyReportPayload(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    tile_code: str
    user_email: str
    full_birth_name: str
    date_of_birth: str
    current_popular_name: str | None = None
    partner_full_birth_name: str | None = None
    partner_date_of_birth: str | None = None
    digital_identifier: str | None = None
    residential_number: str | None = None
    business_name: str | None = None
    candidate_name: str | None = None
    language: str = "en"
    focus_area: str
    numerology_system: str
    reduction_method: str
    target_year: int | None = None
    computed_values: dict[str, NumerologyNumberValue]
    calculation_trace: dict[str, Any]
    report_sections: list[NumerologyReportSection]
    summary: str
    guidance: str
    remedy_note: str | None = None
    lifecycle_hint: str | None = None
    is_premium: bool = True
    bookmarked: bool = False
    created_at: datetime
    updated_at: datetime


class NumerologyGenerateResponse(StrictModel):
    report: NumerologyReportPayload


class NumerologyReadingResponse(StrictModel):
    report: NumerologyReportPayload


class NumerologyTilePreview(StrictModel):
    tile_code: str
    name: str
    description: str
    requires_partner_data: bool = False
    requires_target_year: bool = False
    is_premium: bool = True


class NumerologyTileListResponse(StrictModel):
    tiles: list[NumerologyTilePreview] = Field(default_factory=list)


class NumerologyHistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    tile_code: str
    summary: str
    focus_area: str
    created_at: datetime
    bookmarked: bool = False


class NumerologyHistoryResponse(StrictModel):
    items: list[NumerologyHistoryItem] = Field(default_factory=list)
    page: int
    limit: int
    total: int
    has_more: bool


class NumerologyBookmarkRequest(StrictModel):
    bookmarked: bool


class NumerologyBookmarkResponse(StrictModel):
    report_id: str
    bookmarked: bool


class NumerologyFeedbackRequest(StrictModel):
    report_id: str
    feedback_type: Literal["focus_area", "system_preference", "helpful", "not_helpful", "follow_up_interest"]
    value: str


class NumerologyFeedbackResponse(StrictModel):
    message: str


DEFAULT_TILES = [
    NumerologyTilePreview(tile_code="life_path_soul_mission", name="Life Path & Soul Mission", description="Decode your core numbers, direction, and inner drivers through a premium numerology profile."),
    NumerologyTilePreview(tile_code="name_correction_energy_alignment", name="Name Correction & Energy Alignment", description="Compare your birth vibration with your current name usage to understand public-name fit, energetic drift, and correction guidance."),
    NumerologyTilePreview(tile_code="favorable_timing", name="Favorable Timing For Major Decisions", description="Understand your current numerology timing and how the year may support movement, planning, and better decision windows.", requires_target_year=True),
    NumerologyTilePreview(tile_code="karmic_debt_loshu", name="Karmic Debt & Lo Shu Grid Remediation", description="Audit karmic debt indicators, missing numbers, and Lo Shu plane imbalances with clear remedial guidance."),
    NumerologyTilePreview(tile_code="relationship_compatibility", name="Relationship & Marriage Compatibility", description="Compare core relationship numbers to understand harmony, friction, communication rhythm, and growth patterns.", requires_partner_data=True),
    NumerologyTilePreview(tile_code="career_guidance", name="Career Guidance & Suitability", description="Translate your core numerology profile into work style, talent direction, and career-environment guidance."),
    NumerologyTilePreview(tile_code="lucky_digital_vibrations", name="Lucky Digital Vibrations", description="Check how a mobile, vehicle, or other important number harmonizes with your native numerology profile."),
    NumerologyTilePreview(tile_code="residential_compatibility", name="Residential & House Number Compatibility", description="Check how your house or apartment number harmonizes with your native numerology profile and environment fit."),
    NumerologyTilePreview(tile_code="business_brand_optimization", name="Business & Brand Name Optimization", description="Compare a business or brand name with the founder profile to understand market resonance, fit, and naming harmony."),
    NumerologyTilePreview(tile_code="baby_name_selection", name="Auspicious Baby Name Selection", description="Compare a candidate baby name with the child's birth vibration to assess naming harmony and suitability."),
]


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _get_collection(db):
    collection = getattr(db, "numerology_results", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="numerology_results collection unavailable")
    return collection


def _get_user_email(request: Request) -> str:
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    user_email = user.get("email") if isinstance(user, dict) else None
    if not user_email:
        raise HTTPException(status_code=401, detail="Authenticated user email unavailable")
    return str(user_email)


def _get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")
    return db


def _normalize_person_name(name: str) -> dict[str, str]:
    storage_value = MULTISPACE_PATTERN.sub(" ", name.strip())
    mapping_value = storage_value.upper()
    mapping_value = SUFFIX_PATTERN.sub("", mapping_value)
    mapping_value = NON_ALPHA_PATTERN.sub(" ", mapping_value)
    mapping_value = MULTISPACE_PATTERN.sub(" ", mapping_value).strip()
    return {"storage_value": storage_value, "mapping_value": mapping_value}


def _normalize_number_string(value: str) -> str:
    return NON_DIGIT_PATTERN.sub("", value)


def _get_letter_mapping(system: NumerologySystem) -> dict[str, int]:
    return PYTHAGOREAN_MAP if system == "pythagorean" else CHALDEAN_MAP


def _digit_sum(value: int) -> int:
    return sum(int(digit) for digit in str(abs(value)))


def _reduce_number(value: int, preserve_masters: bool = True) -> int:
    current = abs(value)
    while current >= 10:
        if preserve_masters and current in MASTER_NUMBERS:
            return current
        current = _digit_sum(current)
    return current


def _build_number(raw: int) -> NumerologyNumberValue:
    reduced = _reduce_number(raw)
    return NumerologyNumberValue(raw=raw, reduced=reduced, master_number=reduced if reduced in MASTER_NUMBERS else None)


def _is_vowel_character(word: str, index: int, y_mode: YMode) -> bool:
    char = word[index]
    if char in VOWELS:
        return True
    if char != "Y":
        return False
    if y_mode == "vowel":
        return True
    if y_mode == "consonant":
        return False
    return not any(letter in VOWELS for letter in word if letter != "Y")


def _sum_letters(name: str, system: NumerologySystem, selector: str, y_mode: YMode) -> int:
    normalized = _normalize_person_name(name)["mapping_value"]
    mapping = _get_letter_mapping(system)
    total = 0
    for word in [part for part in normalized.split(" ") if part]:
        for index, char in enumerate(word):
            value = mapping.get(char)
            if value is None:
                continue
            is_vowel = _is_vowel_character(word, index, y_mode)
            if selector == "all":
                total += value
            elif selector == "vowels" and is_vowel:
                total += value
            elif selector == "consonants" and not is_vowel:
                total += value
    return total


def _calculate_expression(name: str, system: NumerologySystem, y_mode: YMode) -> NumerologyNumberValue:
    return _build_number(_sum_letters(name, system, "all", y_mode))


def _calculate_soul_urge(name: str, system: NumerologySystem, y_mode: YMode) -> NumerologyNumberValue:
    return _build_number(_sum_letters(name, system, "vowels", y_mode))


def _calculate_personality(name: str, system: NumerologySystem, y_mode: YMode) -> NumerologyNumberValue:
    return _build_number(_sum_letters(name, system, "consonants", y_mode))


def _calculate_core_four(name: str, system: NumerologySystem, y_mode: YMode) -> dict[str, NumerologyNumberValue]:
    return {
        "expression": _calculate_expression(name, system, y_mode),
        "soul_urge": _calculate_soul_urge(name, system, y_mode),
        "personality": _calculate_personality(name, system, y_mode),
    }


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as err:
        raise HTTPException(status_code=400, detail="date_of_birth must use YYYY-MM-DD") from err


def _calculate_life_path(date_of_birth: str, method: ReductionMethod) -> tuple[NumerologyNumberValue, dict[str, int]]:
    dob = _parse_date(date_of_birth)
    if method == "raw_sum":
        raw = sum(int(char) for char in dob.strftime("%Y%m%d"))
        value = _build_number(raw)
        return value, {"digit_sum": raw}

    month_raw = dob.month
    day_raw = dob.day
    year_raw = dob.year
    month_reduced = _reduce_number(month_raw)
    day_reduced = _reduce_number(day_raw)
    year_reduced = _reduce_number(year_raw)
    raw = month_reduced + day_reduced + year_reduced
    value = _build_number(raw)
    trace = {
        "month_raw": month_raw,
        "month_reduced": month_reduced,
        "day_raw": day_raw,
        "day_reduced": day_reduced,
        "year_raw": year_raw,
        "year_reduced": year_reduced,
        "grouped_total": raw,
    }
    return value, trace


def _calculate_personal_year(date_of_birth: str, target_year: int) -> tuple[NumerologyNumberValue, dict[str, int]]:
    dob = _parse_date(date_of_birth)
    birth_month_reduced = _reduce_number(dob.month)
    birth_day_reduced = _reduce_number(dob.day)
    target_year_reduced = _reduce_number(target_year)
    raw = birth_month_reduced + birth_day_reduced + target_year_reduced
    value = _build_number(raw)
    trace = {
        "birth_month_reduced": birth_month_reduced,
        "birth_day_reduced": birth_day_reduced,
        "target_year_reduced": target_year_reduced,
        "total": raw,
    }
    return value, trace


def _calculate_lo_shu(date_of_birth: str) -> dict[str, Any]:
    digits = [int(char) for char in date_of_birth if char.isdigit() and char != "0"]
    counts = Counter(digits)
    normalized_counts = {str(number): counts.get(number, 0) for number in range(1, 10)}
    missing_numbers = [number for number in range(1, 10) if counts.get(number, 0) == 0]
    repeated_numbers = [number for number in range(1, 10) if counts.get(number, 0) > 1]
    planes = {
        plane_name: all(counts.get(number, 0) > 0 for number in plane_digits)
        for plane_name, plane_digits in PLANE_NUMBERS.items()
    }
    return {
        "digits_used": digits,
        "counts": normalized_counts,
        "missing_numbers": missing_numbers,
        "repeated_numbers": repeated_numbers,
        "planes": planes,
    }


def _detect_karmic_debts(values: list[int]) -> list[int]:
    return sorted({value for value in values if value in KARMIC_DEBT_NUMBERS})


def _score_compatibility(primary: int, secondary: int) -> dict[str, Any]:
    difference = abs(primary - secondary)
    if primary == secondary:
        return {"score": 0.92, "band": "strong", "difference": difference}
    if difference in (1, 2):
        return {"score": 0.76, "band": "supportive", "difference": difference}
    if difference in (3, 4):
        return {"score": 0.58, "band": "mixed", "difference": difference}
    return {"score": 0.42, "band": "frictional", "difference": difference}


def _monthly_highlights(personal_year_number: int) -> list[str]:
    return [
        f"Months that echo {personal_year_number} may feel more aligned for visible action and clearer momentum.",
        "Use quieter periods for preparation, review, and course-correction rather than forcing timing.",
        "Decision quality improves when you follow the rhythm of the year instead of treating every month the same.",
    ]


def _report_base(payload: NumerologyGenerateRequest, user_email: str, report_type: str, report_slug: str) -> dict[str, Any]:
    now = _now()
    return {
        "id": str(uuid4()),
        "document_type": "report",
        "report_type": report_type,
        "report_slug": report_slug,
        "tile_code": payload.tile_code,
        "user_email": user_email,
        "full_birth_name": payload.full_birth_name,
        "date_of_birth": payload.date_of_birth,
        "current_popular_name": payload.current_popular_name,
        "partner_full_birth_name": payload.partner_full_birth_name,
        "partner_date_of_birth": payload.partner_date_of_birth,
        "digital_identifier": payload.digital_identifier,
        "residential_number": payload.residential_number,
        "business_name": payload.business_name,
        "candidate_name": payload.candidate_name,
        "language": payload.language,
        "focus_area": payload.focus_area,
        "numerology_system": payload.numerology_system,
        "reduction_method": payload.reduction_method,
        "target_year": payload.target_year,
        "is_premium": True,
        "bookmarked": False,
        "created_at": now,
        "updated_at": now,
    }


def _build_life_path_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    life_path, life_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    sections = [
        NumerologyReportSection(section_id="life_path_blueprint", title="Life Path Blueprint", summary=f"Your Life Path {life_path.reduced} points to the major rhythm shaping how you move through growth, effort, and direction.", body="This number acts as the main directional anchor for the report and should be read as the broader pattern of development."),
        NumerologyReportSection(section_id="expression_potential", title="Expression & Potential", summary=f"Your Expression number {core['expression'].reduced} reflects how your natural capacities tend to manifest in visible life.", body="This number is derived from the full birth name and shows how ability, output, and public potential can take shape."),
        NumerologyReportSection(section_id="inner_drivers", title="Heart And Personality", summary=f"Soul Urge {core['soul_urge'].reduced} reveals inner motivation, while Personality {core['personality'].reduced} reflects outer presentation.", body="Together these numbers explain the relationship between private desire and outer style."),
    ]
    return NumerologyReportPayload(
        **_report_base(payload, user_email, "numerology_core_profile", "life-path-soul-mission"),
        computed_values={"life_path": life_path, "expression": core["expression"], "soul_urge": core["soul_urge"], "personality": core["personality"]},
        calculation_trace={"life_path": life_trace, "expression": core["expression"].model_dump(), "soul_urge": core["soul_urge"].model_dump(), "personality": core["personality"].model_dump()},
        report_sections=sections,
        summary=f"This profile centers on Life Path {life_path.reduced}, supported by Expression {core['expression'].reduced}, Soul Urge {core['soul_urge'].reduced}, and Personality {core['personality'].reduced}.",
        guidance="Use the Life Path as the primary directional number and treat the name-derived values as supporting context for expression, priorities, and communication style.",
        remedy_note="If later reports show repeated friction between path and expression, the next layer to explore is timing, name alignment, or Lo Shu remediation.",
    )


def _build_name_correction_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.current_popular_name:
        raise HTTPException(status_code=400, detail="current_popular_name is required for this tile")
    life_path, life_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    birth_core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    current_expression = _calculate_expression(payload.current_popular_name, payload.numerology_system, payload.y_mode)
    birth_to_current = _score_compatibility(birth_core["expression"].reduced, current_expression.reduced)
    path_to_current = _score_compatibility(life_path.reduced, current_expression.reduced)
    soul_to_current = _score_compatibility(birth_core["soul_urge"].reduced, current_expression.reduced)
    overall_score = round((birth_to_current["score"] * 0.45) + (path_to_current["score"] * 0.3) + (soul_to_current["score"] * 0.25), 2)
    sections = [
        NumerologyReportSection(section_id="birth_name_baseline", title="Birth Name Baseline", summary=f"Your birth-name blueprint anchors around Expression {birth_core['expression'].reduced} and Soul Urge {birth_core['soul_urge'].reduced}.", body="The birth name acts as the native reference pattern before comparing current-name usage."),
        NumerologyReportSection(section_id="current_name_vibration", title="Current Name Vibration", summary=f"Your current name usage reduces to {current_expression.reduced} and reads as {birth_to_current['band']} against the birth-name expression pattern.", body="This layer reflects how the commonly used name may amplify, soften, or create distance from the original birth-name vibration."),
        NumerologyReportSection(section_id="alignment_guidance", title="Alignment Guidance", summary=f"The current name-alignment score is {overall_score}.", body="Use this score to judge whether the current name appears naturally aligned, mixed, or better suited for refinement."),
    ]
    return NumerologyReportPayload(
        **_report_base(payload, user_email, "numerology_name_correction", "name-correction-and-energy-alignment"),
        computed_values={"life_path": life_path, "birth_expression": birth_core["expression"], "birth_soul_urge": birth_core["soul_urge"], "current_name_expression": current_expression},
        calculation_trace={"life_path": life_trace, "birth_to_current": birth_to_current, "path_to_current": path_to_current, "soul_to_current": soul_to_current, "overall_score": overall_score},
        report_sections=sections,
        summary="This report compares your current name usage with your native numerology blueprint to estimate public-name alignment and energetic fit.",
        guidance="Use name correction as an alignment exercise rather than a superstition-only decision. A name should still feel authentic, usable, and socially natural.",
        remedy_note="If alignment looks mixed, compare alternate spellings or selective name usage before making a formal change.",
    )


def _build_timing_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    target_year = payload.target_year or _now().year
    personal_year, py_trace = _calculate_personal_year(payload.date_of_birth, target_year)
    life_path, life_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    sections = [
        NumerologyReportSection(section_id="year_theme", title="Personal Year Theme", summary=f"Your Personal Year {personal_year.reduced} sets the dominant rhythm for {target_year}.", body="This timing layer describes the kind of movement, pace, and opportunity that may be more available during the selected year."),
        NumerologyReportSection(section_id="life_path_context", title="Life Path Context", summary=f"Your Life Path {life_path.reduced} provides the deeper direction that your current year is activating.", body="The Personal Year works best when read alongside the longer arc of the Life Path."),
        NumerologyReportSection(section_id="monthly_guidance", title="Monthly Guidance", summary="The year should be approached in waves rather than treated as one flat block of time.", body=" ".join(_monthly_highlights(personal_year.reduced))),
    ]
    lifecycle_hint = f"Revisit your timing profile during {target_year} to track shifts in momentum and planning windows."
    return NumerologyReportPayload(
        **_report_base(payload, user_email, "numerology_annual_forecast", "favorable-timing-major-decisions"),
        target_year=target_year,
        computed_values={"personal_year": personal_year, "life_path": life_path},
        calculation_trace={"personal_year": py_trace, "life_path": life_trace},
        report_sections=sections,
        summary=f"Your timing report centers on Personal Year {personal_year.reduced} for {target_year}, read in the context of Life Path {life_path.reduced}.",
        guidance="Use this year as a timing framework for when to advance, refine, or pause. The goal is better alignment, not rigid prediction.",
        remedy_note="If the year feels resistant, the next layers to examine are name alignment, Lo Shu balance, or compatibility with your current environment.",
        lifecycle_hint=lifecycle_hint,
    )


def _build_karmic_loshu_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    life_path, life_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    karmic_debts = _detect_karmic_debts([life_path.raw, core["expression"].raw, core["soul_urge"].raw, core["personality"].raw])
    loshu = _calculate_lo_shu(payload.date_of_birth)
    sections = [
        NumerologyReportSection(section_id="karmic_debt_indicators", title="Karmic Debt Indicators", summary=f"Detected karmic debt indicators: {', '.join(str(item) for item in karmic_debts) if karmic_debts else 'none'}.", body="Karmic debt numbers are treated as recurring lesson patterns rather than punishments."),
        NumerologyReportSection(section_id="loshu_pattern_analysis", title="Lo Shu Pattern Analysis", summary=f"Missing numbers: {', '.join(str(item) for item in loshu['missing_numbers']) if loshu['missing_numbers'] else 'none'}. Repeated numbers: {', '.join(str(item) for item in loshu['repeated_numbers']) if loshu['repeated_numbers'] else 'none'}.", body="Lo Shu patterns highlight where balance, repetition, or developmental emphasis may be more visible."),
        NumerologyReportSection(section_id="remedial_guidance", title="Remedial Guidance", summary="Use remedial steps to create steadier balance in rhythm, awareness, and self-correction.", body="Treat remedial suggestions as supportive practices rather than guarantees."),
    ]
    return NumerologyReportPayload(
        **_report_base(payload, user_email, "numerology_karmic_loshu", "karmic-debt-loshu-grid-remediation"),
        computed_values={"life_path": life_path, "expression": core["expression"], "soul_urge": core["soul_urge"], "personality": core["personality"]},
        calculation_trace={"life_path": life_trace, "karmic_debts": karmic_debts, "loshu": loshu},
        report_sections=sections,
        summary="This report highlights karmic lesson patterns alongside Lo Shu gaps and repetitions that may point to areas needing more conscious balance.",
        guidance="Use remedial steps to create steadier balance in environment, rhythm, and self-correction rather than expecting sudden transformation.",
        remedy_note="Treat remedial suggestions as supportive practices and not as guarantees around health, money, or relationships.",
    )


def _build_relationship_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.partner_full_birth_name or not payload.partner_date_of_birth:
        raise HTTPException(status_code=400, detail="partner_full_birth_name and partner_date_of_birth are required for this tile")
    primary_path, primary_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    partner_path, partner_trace = _calculate_life_path(payload.partner_date_of_birth, payload.reduction_method)
    primary_core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    partner_core = _calculate_core_four(payload.partner_full_birth_name, payload.numerology_system, payload.y_mode)
    path_compat = _score_compatibility(primary_path.reduced, partner_path.reduced)
    soul_compat = _score_compatibility(primary_core["soul_urge"].reduced, partner_core["soul_urge"].reduced)
    personality_compat = _score_compatibility(primary_core["personality"].reduced, partner_core["personality"].reduced)
    overall_score = round((path_compat["score"] * 0.4) + (soul_compat["score"] * 0.35) + (personality_compat["score"] * 0.25), 2)
    sections = [
        NumerologyReportSection(section_id="compatibility_overview", title="Compatibility Overview", summary=f"The current overall relationship score is {overall_score}.", body="This is intended as a guide to rhythm and fit rather than a verdict."),
        NumerologyReportSection(section_id="harmony_zones", title="Harmony Zones", summary=f"Life Path and inner compatibility currently read as {path_compat['band']} and {soul_compat['band']}.", body="Supportive areas usually appear where values, pace, or emotional needs can meet with less strain."),
        NumerologyReportSection(section_id="friction_zones", title="Friction Zones", summary=f"Outer-style compatibility currently reads as {personality_compat['band']}.", body="Mixed or frictional areas do not predict failure, but they often indicate where clearer communication and timing become more important."),
    ]
    return NumerologyReportPayload(
        **_report_base(payload, user_email, "numerology_relationship_compatibility", "relationship-marriage-compatibility"),
        computed_values={"primary_life_path": primary_path, "partner_life_path": partner_path, "primary_soul_urge": primary_core["soul_urge"], "partner_soul_urge": partner_core["soul_urge"]},
        calculation_trace={"primary_life_path": primary_trace, "partner_life_path": partner_trace, "path_compat": path_compat, "soul_compat": soul_compat, "personality_compat": personality_compat, "overall_score": overall_score},
        report_sections=sections,
        summary=f"This compatibility reading suggests an overall relationship score of {overall_score}, intended as a guide to rhythm and fit rather than a verdict.",
        guidance="Use the report to identify where patience, translation, and emotional pacing may improve the relationship dynamic.",
        remedy_note="A timing report can add another layer by showing when emotional or practical decisions may be better supported.",
    )


def _build_career_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    life_path, life_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    talent_cluster = f"Expression {core['expression'].reduced}"
    mission_cluster = f"Life Path {life_path.reduced}"
    environment_cluster = f"Personality {core['personality'].reduced}"
    sections = [
        NumerologyReportSection(section_id="native_strengths", title="Native Strengths", summary=f"Your strongest visible strengths appear connected to the {talent_cluster} pattern.", body="This layer translates your core profile into ability, visible style, and contribution themes."),
        NumerologyReportSection(section_id="mission_direction", title="Mission Direction", summary=f"Your longer-range work direction appears connected to the {mission_cluster} pattern.", body="This should be read as directional guidance rather than a single guaranteed profession."),
        NumerologyReportSection(section_id="environment_fit", title="Environment Fit", summary=f"Your more sustainable work environment may align with the {environment_cluster} pattern.", body="Use this layer to think about pace, culture, structure, and role environment."),
    ]
    return NumerologyReportPayload(
        **_report_base(payload, user_email, "numerology_career_guidance", "career-guidance-suitability"),
        computed_values={"life_path": life_path, "expression": core["expression"], "soul_urge": core["soul_urge"], "personality": core["personality"]},
        calculation_trace={"life_path": life_trace, "career_clusters": {"talent": talent_cluster, "mission": mission_cluster, "environment": environment_cluster}},
        report_sections=sections,
        summary="This report translates your core numerology profile into professional strengths, directional themes, and environment fit rather than a rigid career label.",
        guidance="Use the report to choose roles and work settings that fit both your visible strengths and your longer-term motivational pattern.",
        remedy_note=None,
    )


def _build_digital_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.digital_identifier:
        raise HTTPException(status_code=400, detail="digital_identifier is required for this tile")
    life_path, life_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    normalized_digits = _normalize_number_string(payload.digital_identifier)
    if not normalized_digits:
        raise HTTPException(status_code=400, detail="digital_identifier must contain digits")
    digital_raw = sum(int(char) for char in normalized_digits)
    digital_vibration = _build_number(digital_raw)
    life_path_compat = _score_compatibility(life_path.reduced, digital_vibration.reduced)
    soul_compat = _score_compatibility(core["soul_urge"].reduced, digital_vibration.reduced)
    overall_score = round((life_path_compat["score"] * 0.55) + (soul_compat["score"] * 0.45), 2)
    sections = [
        NumerologyReportSection(section_id="digital_vibration", title="Digital Vibration", summary=f"The selected number reduces to {digital_vibration.reduced}.", body="This acts as the main symbolic vibration of the chosen digital identifier."),
        NumerologyReportSection(section_id="compatibility_summary", title="Compatibility Summary", summary=f"The current harmony score is {overall_score}.", body="Use this as a fit indicator rather than a promise of luck."),
        NumerologyReportSection(section_id="practical_guidance", title="Practical Guidance", summary="Digital-vibration checks are most useful when comparing multiple choices.", body="Treat the result as one decision-support layer alongside your broader timing and identity patterns."),
    ]
    return NumerologyReportPayload(
        **_report_base(payload, user_email, "numerology_digital_vibrations", "lucky-digital-vibrations"),
        computed_values={"life_path": life_path, "soul_urge": core["soul_urge"], "digital_vibration": digital_vibration},
        calculation_trace={"life_path": life_trace, "digital_vibration": {"normalized_digits": normalized_digits, "raw": digital_raw, "reduced": digital_vibration.reduced}, "compatibility": {"life_path": life_path_compat, "soul_urge": soul_compat, "overall_score": overall_score}},
        report_sections=sections,
        summary="This report treats your chosen digital number as a symbolic vibration and compares it with your native numerology profile.",
        guidance="Use digital-vibration checks as a practical comparison tool when choosing between multiple numbers.",
        remedy_note="Do not treat a digital-number result as more important than the broader timing and identity patterns in your full profile.",
    )


def _build_residential_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.residential_number:
        raise HTTPException(status_code=400, detail="residential_number is required for this tile")
    life_path, life_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    normalized_digits = _normalize_number_string(payload.residential_number)
    if not normalized_digits:
        raise HTTPException(status_code=400, detail="residential_number must contain digits")
    home_raw = sum(int(char) for char in normalized_digits)
    home_vibration = _build_number(home_raw)
    life_path_compat = _score_compatibility(life_path.reduced, home_vibration.reduced)
    soul_compat = _score_compatibility(core["soul_urge"].reduced, home_vibration.reduced)
    overall_score = round((life_path_compat["score"] * 0.55) + (soul_compat["score"] * 0.45), 2)
    sections = [
        NumerologyReportSection(section_id="home_vibration", title="Home Vibration", summary=f"The home reduces to a residential vibration of {home_vibration.reduced}.", body="This is the main environmental vibration of the home number."),
        NumerologyReportSection(section_id="home_fit", title="Environment Fit", summary=f"The current overall home-fit score is {overall_score}.", body="Use this as an alignment signal rather than a verdict on the home."),
        NumerologyReportSection(section_id="adjustment_notes", title="Adjustment Notes", summary="A mixed result does not automatically mean the home is wrong.", body="It may simply mean balance, awareness, and remedial support matter more."),
    ]
    return NumerologyReportPayload(
        **_report_base(payload, user_email, "numerology_residential_compatibility", "residential-house-number-compatibility"),
        computed_values={"life_path": life_path, "soul_urge": core["soul_urge"], "residential_vibration": home_vibration},
        calculation_trace={"life_path": life_trace, "residential_vibration": {"normalized_digits": normalized_digits, "raw": home_raw, "reduced": home_vibration.reduced}, "compatibility": {"life_path": life_path_compat, "soul_urge": soul_compat, "overall_score": overall_score}},
        report_sections=sections,
        summary="This report treats your house number as an environmental vibration and compares it with your native numerology profile.",
        guidance="Use residential compatibility as a home-awareness tool and combine it with lived experience, comfort, and environmental balance.",
        remedy_note="A mixed result does not automatically mean the home is wrong; it may simply mean balance and remedial support matter more.",
    )


def _build_business_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.business_name:
        raise HTTPException(status_code=400, detail="business_name is required for this tile")
    life_path, life_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    business_expression = _calculate_expression(payload.business_name, payload.numerology_system, payload.y_mode)
    founder_to_brand = _score_compatibility(core["expression"].reduced, business_expression.reduced)
    path_to_brand = _score_compatibility(life_path.reduced, business_expression.reduced)
    overall_score = round((founder_to_brand["score"] * 0.55) + (path_to_brand["score"] * 0.45), 2)
    sections = [
        NumerologyReportSection(section_id="founder_brand_alignment", title="Founder-To-Brand Alignment", summary=f"Founder expression-to-brand compatibility reads as {founder_to_brand['band']}.", body="This layer checks whether the brand name appears to amplify, neutralize, or create friction with the founder's visible style."),
        NumerologyReportSection(section_id="market_vibration", title="Market Vibration", summary=f"The business name reduces to {business_expression.reduced}.", body="The brand number can be read as the outer signal the market receives."),
        NumerologyReportSection(section_id="optimization_notes", title="Optimization Notes", summary=f"The current founder-to-brand optimization score is {overall_score}.", body="A stronger score suggests cleaner symbolic fit, while a mixed score may still be workable."),
    ]
    return NumerologyReportPayload(
        **_report_base(payload, user_email, "numerology_brand_optimization", "business-brand-name-optimization"),
        computed_values={"life_path": life_path, "founder_expression": core["expression"], "business_expression": business_expression},
        calculation_trace={"life_path": life_trace, "compatibility": {"founder_to_brand": founder_to_brand, "path_to_brand": path_to_brand, "overall_score": overall_score}},
        report_sections=sections,
        summary="This report compares the brand name with the founder profile to estimate naming fit, resonance, and symbolic business alignment.",
        guidance="Use this as a decision-support layer alongside branding clarity, audience fit, and real-world usability.",
        remedy_note="A stronger score can support confidence, but no name should be treated as a substitute for business model, timing, or execution.",
    )


def _build_baby_name_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.candidate_name:
        raise HTTPException(status_code=400, detail="candidate_name is required for this tile")
    life_path, life_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    candidate_expression = _calculate_expression(payload.candidate_name, payload.numerology_system, payload.y_mode)
    child_path_to_name = _score_compatibility(life_path.reduced, candidate_expression.reduced)
    child_soul_to_name = _score_compatibility(core["soul_urge"].reduced, candidate_expression.reduced)
    overall_score = round((child_path_to_name["score"] * 0.6) + (child_soul_to_name["score"] * 0.4), 2)
    sections = [
        NumerologyReportSection(section_id="child_vibration", title="Child Vibration Baseline", summary=f"Life Path {life_path.reduced} provides the child's foundational birth vibration for naming comparison.", body="This baseline acts as the core reference point for checking whether a candidate name feels supportive, mixed, or frictional."),
        NumerologyReportSection(section_id="candidate_name_fit", title="Candidate Name Fit", summary=f"The candidate name reduces to {candidate_expression.reduced} and currently reads as {child_path_to_name['band']} against the child's Life Path.", body="A strong fit may feel cleaner and more harmonious, while mixed fit may simply call for comparison with alternate options."),
        NumerologyReportSection(section_id="selection_guidance", title="Selection Guidance", summary=f"The current baby-name suitability score is {overall_score}.", body="Naming should also consider usability, emotional resonance, family preference, and long-term comfort."),
    ]
    return NumerologyReportPayload(
        **_report_base(payload, user_email, "numerology_baby_name", "auspicious-baby-name-selection"),
        computed_values={"life_path": life_path, "soul_urge": core["soul_urge"], "candidate_expression": candidate_expression},
        calculation_trace={"life_path": life_trace, "compatibility": {"child_path_to_name": child_path_to_name, "child_soul_to_name": child_soul_to_name, "overall_score": overall_score}},
        report_sections=sections,
        summary="This report compares a candidate name with the child's birth vibration to estimate naming harmony and suitability.",
        guidance="Use this result to compare naming options while also considering family resonance, pronunciation, and long-term comfort.",
        remedy_note="No candidate name should be treated as a guarantee of the child's future. Use numerology as one thoughtful input among several.",
    )


def _build_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if payload.tile_code == "life_path_soul_mission":
        return _build_life_path_report(payload, user_email)
    if payload.tile_code == "name_correction_energy_alignment":
        return _build_name_correction_report(payload, user_email)
    if payload.tile_code == "favorable_timing":
        return _build_timing_report(payload, user_email)
    if payload.tile_code == "karmic_debt_loshu":
        return _build_karmic_loshu_report(payload, user_email)
    if payload.tile_code == "relationship_compatibility":
        return _build_relationship_report(payload, user_email)
    if payload.tile_code == "career_guidance":
        return _build_career_report(payload, user_email)
    if payload.tile_code == "lucky_digital_vibrations":
        return _build_digital_report(payload, user_email)
    if payload.tile_code == "residential_compatibility":
        return _build_residential_report(payload, user_email)
    if payload.tile_code == "business_brand_optimization":
        return _build_business_report(payload, user_email)
    if payload.tile_code == "baby_name_selection":
        return _build_baby_name_report(payload, user_email)
    raise HTTPException(status_code=400, detail="Unsupported numerology tile")


@router.get("/tiles", response_model=NumerologyTileListResponse)
async def list_numerology_tiles() -> NumerologyTileListResponse:
    return NumerologyTileListResponse(tiles=DEFAULT_TILES)


@router.post("/report/generate", response_model=NumerologyGenerateResponse)
async def generate_numerology_report(payload: NumerologyGenerateRequest, request: Request) -> NumerologyGenerateResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(_get_db(request))
    report = _build_report(payload, user_email)
    await collection.insert_one(report.model_dump(mode="python"))
    return NumerologyGenerateResponse(report=report)


@router.get("/report/{report_id}", response_model=NumerologyReadingResponse)
async def get_numerology_report(report_id: str, request: Request) -> NumerologyReadingResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(_get_db(request))
    report = await collection.find_one({"id": report_id, "user_email": user_email, "document_type": "report"})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return NumerologyReadingResponse(report=NumerologyReportPayload(**report))


@router.get("/history", response_model=NumerologyHistoryResponse)
async def get_numerology_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
    tile_code: str | None = None,
    bookmarked: bool | None = None,
) -> NumerologyHistoryResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(_get_db(request))
    query: dict[str, Any] = {"user_email": user_email, "document_type": "report"}
    if tile_code:
        query["tile_code"] = tile_code
    if bookmarked is not None:
        query["bookmarked"] = bookmarked
    skip = (page - 1) * limit
    cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    total = await collection.count_documents(query)
    items = [
        NumerologyHistoryItem(
            id=doc["id"],
            report_type=doc["report_type"],
            report_slug=doc["report_slug"],
            tile_code=doc["tile_code"],
            summary=doc["summary"],
            focus_area=doc["focus_area"],
            created_at=doc["created_at"],
            bookmarked=doc.get("bookmarked", False),
        )
        for doc in docs
    ]
    return NumerologyHistoryResponse(items=items, page=page, limit=limit, total=total, has_more=skip + limit < total)


@router.post("/history/{report_id}/bookmark", response_model=NumerologyBookmarkResponse)
async def bookmark_numerology_report(request: Request, report_id: str, payload: NumerologyBookmarkRequest) -> NumerologyBookmarkResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(_get_db(request))
    result = await collection.update_one(
        {"id": report_id, "user_email": user_email, "document_type": "report"},
        {"$set": {"bookmarked": payload.bookmarked, "updated_at": _now()}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Report not found")
    return NumerologyBookmarkResponse(report_id=report_id, bookmarked=payload.bookmarked)


@router.post("/feedback", response_model=NumerologyFeedbackResponse)
async def submit_numerology_feedback(request: Request, payload: NumerologyFeedbackRequest) -> NumerologyFeedbackResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(_get_db(request))
    report = await collection.find_one({"id": payload.report_id, "user_email": user_email, "document_type": "report"})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    feedback_doc = {
        "id": str(uuid4()),
        "document_type": "feedback",
        "module": "numerology",
        "user_email": user_email,
        "report_id": payload.report_id,
        "tile_code": report.get("tile_code"),
        "feedback_type": payload.feedback_type,
        "value": payload.value,
        "created_at": _now(),
        "updated_at": _now(),
    }
    await collection.insert_one(feedback_doc)
    return NumerologyFeedbackResponse(message="Feedback received.")
