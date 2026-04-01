from __future__ import annotations

import logging
import re
from collections import Counter
from datetime import date, datetime, timezone
from typing import Any, Literal
from uuid import uuid4

_log = logging.getLogger("numerology")

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field
from numerology_prompt_service import enrich_numerology_report_with_claude
from vedic_calculator import calculate_vedic_chart


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
    "premium_ankjyotish_report",
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
    time_of_birth: str | None = None
    place_of_birth: str | None = None
    current_popular_name: str | None = None
    partner_full_birth_name: str | None = None
    partner_date_of_birth: str | None = None
    digital_identifier: str | None = None
    residential_number: str | None = None
    business_name: str | None = None
    candidate_name: str | None = None
    lagna_sign: str | None = None
    moon_sign: str | None = None
    nakshatra_name: str | None = None
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
    document_type: Literal["report", "premium_ankjyotish_report"] = "report"
    report_type: str
    report_slug: str
    tile_code: str
    user_email: str
    full_birth_name: str
    date_of_birth: str
    time_of_birth: str | None = None
    place_of_birth: str | None = None
    current_popular_name: str | None = None
    partner_full_birth_name: str | None = None
    partner_date_of_birth: str | None = None
    digital_identifier: str | None = None
    residential_number: str | None = None
    business_name: str | None = None
    candidate_name: str | None = None
    lagna_sign: str | None = None
    moon_sign: str | None = None
    nakshatra_name: str | None = None
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
    NumerologyTilePreview(tile_code="premium_ankjyotish_report", name="Premium Ankjyotish Report", description="Generate a premium life-analysis report combining core numerology, Lo Shu, karmic audit, Vedic cross-reference, lucky elements, and a 7-day remediation plan."),
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
        return _build_number(raw), {"digit_sum": raw}
    month_reduced = _reduce_number(dob.month)
    day_reduced = _reduce_number(dob.day)
    year_reduced = _reduce_number(dob.year)
    raw = month_reduced + day_reduced + year_reduced
    return _build_number(raw), {"month_raw": dob.month, "month_reduced": month_reduced, "day_raw": dob.day, "day_reduced": day_reduced, "year_raw": dob.year, "year_reduced": year_reduced, "grouped_total": raw}


def _calculate_personal_year(date_of_birth: str, target_year: int) -> tuple[NumerologyNumberValue, dict[str, int]]:
    dob = _parse_date(date_of_birth)
    bm = _reduce_number(dob.month)
    bd = _reduce_number(dob.day)
    ty = _reduce_number(target_year)
    raw = bm + bd + ty
    return _build_number(raw), {"birth_month_reduced": bm, "birth_day_reduced": bd, "target_year_reduced": ty, "total": raw}


def _calculate_lo_shu(date_of_birth: str) -> dict[str, Any]:
    digits = [int(char) for char in date_of_birth if char.isdigit() and char != "0"]
    counts = Counter(digits)
    normalized_counts = {str(n): counts.get(n, 0) for n in range(1, 10)}
    missing_numbers = [n for n in range(1, 10) if counts.get(n, 0) == 0]
    repeated_numbers = [n for n in range(1, 10) if counts.get(n, 0) > 1]
    planes = {name: all(counts.get(n, 0) > 0 for n in nums) for name, nums in PLANE_NUMBERS.items()}
    return {"digits_used": digits, "counts": normalized_counts, "missing_numbers": missing_numbers, "repeated_numbers": repeated_numbers, "planes": planes}


def _detect_karmic_debts(values: list[int]) -> list[int]:
    return sorted({v for v in values if v in KARMIC_DEBT_NUMBERS})


def _score_compatibility(primary: int, secondary: int) -> dict[str, Any]:
    diff = abs(primary - secondary)
    if primary == secondary:
        return {"score": 0.92, "band": "strong", "difference": diff}
    if diff in (1, 2):
        return {"score": 0.76, "band": "supportive", "difference": diff}
    if diff in (3, 4):
        return {"score": 0.58, "band": "mixed", "difference": diff}
    return {"score": 0.42, "band": "frictional", "difference": diff}


def _monthly_highlights(py: int) -> list[str]:
    return [f"Months that echo {py} may feel more aligned for visible action and clearer momentum.", "Use quieter periods for preparation, review, and course-correction rather than forcing timing.", "Decision quality improves when you follow the rhythm of the year instead of treating every month the same."]


def _report_base(payload: NumerologyGenerateRequest, user_email: str, report_type: str, report_slug: str) -> dict[str, Any]:
    now = _now()
    return {"id": str(uuid4()), "document_type": "report", "report_type": report_type, "report_slug": report_slug, "tile_code": payload.tile_code, "user_email": user_email, "full_birth_name": payload.full_birth_name, "date_of_birth": payload.date_of_birth, "time_of_birth": payload.time_of_birth, "place_of_birth": payload.place_of_birth, "current_popular_name": payload.current_popular_name, "partner_full_birth_name": payload.partner_full_birth_name, "partner_date_of_birth": payload.partner_date_of_birth, "digital_identifier": payload.digital_identifier, "residential_number": payload.residential_number, "business_name": payload.business_name, "candidate_name": payload.candidate_name, "lagna_sign": payload.lagna_sign, "moon_sign": payload.moon_sign, "nakshatra_name": payload.nakshatra_name, "language": payload.language, "focus_area": payload.focus_area, "numerology_system": payload.numerology_system, "reduction_method": payload.reduction_method, "target_year": payload.target_year, "is_premium": True, "bookmarked": False, "created_at": now, "updated_at": now}


def _calculate_personal_month(py: int, month: int) -> NumerologyNumberValue:
    return _build_number(py + _reduce_number(month))


def _calculate_personal_day(pm: int, day: int) -> NumerologyNumberValue:
    return _build_number(pm + _reduce_number(day))


def _build_lo_shu_grid_payload(date_of_birth: str) -> dict[str, Any]:
    loshu = _calculate_lo_shu(date_of_birth)
    counts = {int(k): v for k, v in loshu["counts"].items()}
    rows = [[{"number": 4, "count": counts.get(4, 0)}, {"number": 9, "count": counts.get(9, 0)}, {"number": 2, "count": counts.get(2, 0)}], [{"number": 3, "count": counts.get(3, 0)}, {"number": 5, "count": counts.get(5, 0)}, {"number": 7, "count": counts.get(7, 0)}], [{"number": 8, "count": counts.get(8, 0)}, {"number": 1, "count": counts.get(1, 0)}, {"number": 6, "count": counts.get(6, 0)}]]
    plane_analysis = {"mental": loshu["planes"]["mental_4_9_2"], "emotional": loshu["planes"]["emotional_3_5_7"], "practical": loshu["planes"]["practical_8_1_6"], "will": loshu["planes"]["will_9_5_1"], "action": loshu["planes"]["action_2_7_6"]}
    return {"grid_rows": rows, "present_numbers": [n for n in range(1, 10) if counts.get(n, 0) > 0], "missing_numbers": loshu["missing_numbers"], "repeated_numbers": loshu["repeated_numbers"], "plane_analysis": plane_analysis}


def _timing_forecast_lines(year: int, py: int) -> list[str]:
    return [f"{year}: Personal Year {py}", f"{year + 1}: Personal Year {_reduce_number(py + 1)}", f"{year + 2}: Personal Year {_reduce_number(py + 2)}"]


def _lucky_elements_table(lp: int, expr: int, soul: int) -> dict[str, Any]:
    element_map = {1: "Fire", 2: "Water", 3: "Air", 4: "Earth", 5: "Air", 6: "Earth", 7: "Water", 8: "Earth", 9: "Fire", 11: "Air", 22: "Earth", 33: "Fire"}
    color_map = {1: ["Red", "Crimson"], 2: ["Pearl White", "Silver"], 3: ["Yellow", "Gold"], 4: ["Green", "Olive"], 5: ["Sky Blue", "Mint"], 6: ["Cream", "Rose"], 7: ["Sea Green", "Indigo"], 8: ["Charcoal", "Navy"], 9: ["Maroon", "Copper"], 11: ["Electric Blue", "White"], 22: ["Forest Green", "Slate"], 33: ["Saffron", "Gold"]}
    day_map = {1: "Sunday", 2: "Monday", 3: "Thursday", 4: "Saturday", 5: "Wednesday", 6: "Friday", 7: "Monday", 8: "Saturday", 9: "Tuesday", 11: "Thursday", 22: "Saturday", 33: "Friday"}
    return {"dominant_element": element_map.get(lp, "Balanced"), "supportive_colors": color_map.get(expr, ["Gold", "White"]), "supportive_day": day_map.get(soul, "Thursday"), "lucky_numbers": [str(n) for n in sorted({lp, expr, soul})]}


def _remediation_plan(base: int) -> list[dict[str, str]]:
    themes = ["clarity and journaling", "home and workspace order", "discipline and follow-through", "gratitude and relationship repair", "service and generosity", "silence and spiritual reflection", "alignment review and reset"]
    return [{"day": f"Day {i + 1}", "focus": f"Number {base} alignment", "practice": t} for i, t in enumerate(themes)]


def _build_life_path_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    lp, lp_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    sections = [NumerologyReportSection(section_id="life_path_blueprint", title="Life Path Blueprint", summary=f"Your Life Path {lp.reduced} points to the major rhythm shaping how you move through growth, effort, and direction.", body="This number acts as the main directional anchor for the report and should be read as the broader pattern of development."), NumerologyReportSection(section_id="expression_potential", title="Expression & Potential", summary=f"Your Expression number {core['expression'].reduced} reflects how your natural capacities tend to manifest in visible life.", body="This number is derived from the full birth name and shows how ability, output, and public potential can take shape."), NumerologyReportSection(section_id="inner_drivers", title="Heart And Personality", summary=f"Soul Urge {core['soul_urge'].reduced} reveals inner motivation, while Personality {core['personality'].reduced} reflects outer presentation.", body="Together these numbers explain the relationship between private desire and outer style.")]
    return NumerologyReportPayload(**_report_base(payload, user_email, "numerology_core_profile", "life-path-soul-mission"), computed_values={"life_path": lp, "expression": core["expression"], "soul_urge": core["soul_urge"], "personality": core["personality"]}, calculation_trace={"life_path": lp_trace}, report_sections=sections, summary=f"This profile centers on Life Path {lp.reduced}, supported by Expression {core['expression'].reduced}, Soul Urge {core['soul_urge'].reduced}, and Personality {core['personality'].reduced}.", guidance="Use the Life Path as the primary directional number and treat the name-derived values as supporting context.", remedy_note="If later reports show repeated friction between path and expression, the next layer to explore is timing, name alignment, or Lo Shu remediation.")


def _build_name_correction_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.current_popular_name:
        raise HTTPException(status_code=400, detail="current_popular_name is required for this tile")
    lp, lp_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    birth_core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    curr_expr = _calculate_expression(payload.current_popular_name, payload.numerology_system, payload.y_mode)
    b2c = _score_compatibility(birth_core["expression"].reduced, curr_expr.reduced)
    p2c = _score_compatibility(lp.reduced, curr_expr.reduced)
    s2c = _score_compatibility(birth_core["soul_urge"].reduced, curr_expr.reduced)
    score = round(b2c["score"] * 0.45 + p2c["score"] * 0.3 + s2c["score"] * 0.25, 2)
    sections = [NumerologyReportSection(section_id="birth_name_baseline", title="Birth Name Baseline", summary=f"Your birth-name blueprint anchors around Expression {birth_core['expression'].reduced} and Soul Urge {birth_core['soul_urge'].reduced}.", body="The birth name acts as the native reference pattern before comparing current-name usage."), NumerologyReportSection(section_id="current_name_vibration", title="Current Name Vibration", summary=f"Your current name usage reduces to {curr_expr.reduced} and reads as {b2c['band']} against the birth-name expression pattern.", body="This layer reflects how the commonly used name may amplify, soften, or create distance from the original birth-name vibration."), NumerologyReportSection(section_id="alignment_guidance", title="Alignment Guidance", summary=f"The current name-alignment score is {score}.", body="Use this score to judge whether the current name appears naturally aligned, mixed, or better suited for refinement.")]
    return NumerologyReportPayload(**_report_base(payload, user_email, "numerology_name_correction", "name-correction-and-energy-alignment"), computed_values={"life_path": lp, "birth_expression": birth_core["expression"], "birth_soul_urge": birth_core["soul_urge"], "current_name_expression": curr_expr}, calculation_trace={"life_path": lp_trace, "birth_to_current": b2c, "path_to_current": p2c, "soul_to_current": s2c, "overall_score": score}, report_sections=sections, summary="This report compares your current name usage with your native numerology blueprint to estimate public-name alignment and energetic fit.", guidance="Use name correction as an alignment exercise rather than a superstition-only decision.", remedy_note="If alignment looks mixed, compare alternate spellings or selective name usage before making a formal change.")


def _build_timing_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    target_year = payload.target_year or _now().year
    py, py_trace = _calculate_personal_year(payload.date_of_birth, target_year)
    lp, lp_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    sections = [NumerologyReportSection(section_id="year_theme", title="Personal Year Theme", summary=f"Your Personal Year {py.reduced} sets the dominant rhythm for {target_year}.", body="This timing layer describes the kind of movement, pace, and opportunity that may be more available during the selected year."), NumerologyReportSection(section_id="life_path_context", title="Life Path Context", summary=f"Your Life Path {lp.reduced} provides the deeper direction that your current year is activating.", body="The Personal Year works best when read alongside the longer arc of the Life Path."), NumerologyReportSection(section_id="monthly_guidance", title="Monthly Guidance", summary="The year should be approached in waves rather than treated as one flat block of time.", body=" ".join(_monthly_highlights(py.reduced)))]
    return NumerologyReportPayload(**_report_base(payload, user_email, "numerology_annual_forecast", "favorable-timing-major-decisions"), target_year=target_year, computed_values={"personal_year": py, "life_path": lp}, calculation_trace={"personal_year": py_trace, "life_path": lp_trace}, report_sections=sections, summary=f"Your timing report centers on Personal Year {py.reduced} for {target_year}, read in the context of Life Path {lp.reduced}.", guidance="Use this year as a timing framework for when to advance, refine, or pause.", remedy_note="If the year feels resistant, the next layers to examine are name alignment, Lo Shu balance, or compatibility with your current environment.", lifecycle_hint=f"Revisit your timing profile during {target_year} to track shifts in momentum and planning windows.")


def _build_karmic_loshu_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    lp, lp_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    karmic = _detect_karmic_debts([lp.raw, core["expression"].raw, core["soul_urge"].raw, core["personality"].raw])
    loshu = _calculate_lo_shu(payload.date_of_birth)
    sections = [NumerologyReportSection(section_id="karmic_debt_indicators", title="Karmic Debt Indicators", summary=f"Detected karmic debt indicators: {', '.join(str(k) for k in karmic) if karmic else 'none'}.", body="Karmic debt numbers are treated as recurring lesson patterns rather than punishments."), NumerologyReportSection(section_id="loshu_pattern_analysis", title="Lo Shu Pattern Analysis", summary=f"Missing numbers: {', '.join(str(n) for n in loshu['missing_numbers']) if loshu['missing_numbers'] else 'none'}. Repeated: {', '.join(str(n) for n in loshu['repeated_numbers']) if loshu['repeated_numbers'] else 'none'}.", body="Lo Shu patterns highlight where balance, repetition, or developmental emphasis may be more visible."), NumerologyReportSection(section_id="remedial_guidance", title="Remedial Guidance", summary="Use remedial steps to create steadier balance in rhythm, awareness, and self-correction.", body="Treat remedial suggestions as supportive practices rather than guarantees.")]
    return NumerologyReportPayload(**_report_base(payload, user_email, "numerology_karmic_loshu", "karmic-debt-loshu-grid-remediation"), computed_values={"life_path": lp, "expression": core["expression"], "soul_urge": core["soul_urge"], "personality": core["personality"]}, calculation_trace={"life_path": lp_trace, "karmic_debts": karmic, "loshu": loshu}, report_sections=sections, summary="This report highlights karmic lesson patterns alongside Lo Shu gaps and repetitions that may point to areas needing more conscious balance.", guidance="Use remedial steps to create steadier balance in environment, rhythm, and self-correction.", remedy_note="Treat remedial suggestions as supportive practices and not as guarantees around health, money, or relationships.")


def _build_relationship_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.partner_full_birth_name or not payload.partner_date_of_birth:
        raise HTTPException(status_code=400, detail="partner_full_birth_name and partner_date_of_birth are required for this tile")
    plp, pltrace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    partnerlp, ptrace = _calculate_life_path(payload.partner_date_of_birth, payload.reduction_method)
    pcore = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    partnercore = _calculate_core_four(payload.partner_full_birth_name, payload.numerology_system, payload.y_mode)
    pc = _score_compatibility(plp.reduced, partnerlp.reduced)
    sc = _score_compatibility(pcore["soul_urge"].reduced, partnercore["soul_urge"].reduced)
    pers = _score_compatibility(pcore["personality"].reduced, partnercore["personality"].reduced)
    overall = round(pc["score"] * 0.4 + sc["score"] * 0.35 + pers["score"] * 0.25, 2)
    sections = [NumerologyReportSection(section_id="compatibility_overview", title="Compatibility Overview", summary=f"The current overall relationship score is {overall}.", body="This is intended as a guide to rhythm and fit rather than a verdict."), NumerologyReportSection(section_id="harmony_zones", title="Harmony Zones", summary=f"Life Path and inner compatibility currently read as {pc['band']} and {sc['band']}.", body="Supportive areas usually appear where values, pace, or emotional needs can meet with less strain."), NumerologyReportSection(section_id="friction_zones", title="Friction Zones", summary=f"Outer-style compatibility currently reads as {pers['band']}.", body="Mixed or frictional areas do not predict failure, but they often indicate where clearer communication matters more.")]
    return NumerologyReportPayload(**_report_base(payload, user_email, "numerology_relationship_compatibility", "relationship-marriage-compatibility"), computed_values={"primary_life_path": plp, "partner_life_path": partnerlp, "primary_soul_urge": pcore["soul_urge"], "partner_soul_urge": partnercore["soul_urge"]}, calculation_trace={"primary_life_path": pltrace, "partner_life_path": ptrace, "path_compat": pc, "soul_compat": sc, "personality_compat": pers, "overall_score": overall}, report_sections=sections, summary=f"This compatibility reading suggests an overall relationship score of {overall}.", guidance="Use the report to identify where patience and emotional pacing may improve the relationship dynamic.", remedy_note="A timing report can add another layer by showing when emotional or practical decisions may be better supported.")


def _build_career_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    lp, lp_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    sections = [NumerologyReportSection(section_id="native_strengths", title="Native Strengths", summary=f"Your strongest visible strengths appear connected to the Expression {core['expression'].reduced} pattern.", body="This layer translates your core profile into ability, visible style, and contribution themes."), NumerologyReportSection(section_id="mission_direction", title="Mission Direction", summary=f"Your longer-range work direction appears connected to the Life Path {lp.reduced} pattern.", body="This should be read as directional guidance rather than a single guaranteed profession."), NumerologyReportSection(section_id="environment_fit", title="Environment Fit", summary=f"Your more sustainable work environment may align with the Personality {core['personality'].reduced} pattern.", body="Use this layer to think about pace, culture, structure, and role environment.")]
    return NumerologyReportPayload(**_report_base(payload, user_email, "numerology_career_guidance", "career-guidance-suitability"), computed_values={"life_path": lp, "expression": core["expression"], "soul_urge": core["soul_urge"], "personality": core["personality"]}, calculation_trace={"life_path": lp_trace}, report_sections=sections, summary="This report translates your core numerology profile into professional strengths, directional themes, and environment fit.", guidance="Use the report to choose roles and work settings that fit both your visible strengths and your longer-term motivational pattern.", remedy_note=None)


def _build_digital_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.digital_identifier:
        raise HTTPException(status_code=400, detail="digital_identifier is required for this tile")
    lp, lp_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    nd = _normalize_number_string(payload.digital_identifier)
    if not nd:
        raise HTTPException(status_code=400, detail="digital_identifier must contain digits")
    dv = _build_number(sum(int(c) for c in nd))
    lpc = _score_compatibility(lp.reduced, dv.reduced)
    sc = _score_compatibility(core["soul_urge"].reduced, dv.reduced)
    overall = round(lpc["score"] * 0.55 + sc["score"] * 0.45, 2)
    sections = [NumerologyReportSection(section_id="digital_vibration", title="Digital Vibration", summary=f"The selected number reduces to {dv.reduced}.", body="This acts as the main symbolic vibration of the chosen digital identifier."), NumerologyReportSection(section_id="compatibility_summary", title="Compatibility Summary", summary=f"The current harmony score is {overall}.", body="Use this as a fit indicator rather than a promise of luck."), NumerologyReportSection(section_id="practical_guidance", title="Practical Guidance", summary="Digital-vibration checks are most useful when comparing multiple choices.", body="Treat the result as one decision-support layer alongside your broader timing and identity patterns.")]
    return NumerologyReportPayload(**_report_base(payload, user_email, "numerology_digital_vibrations", "lucky-digital-vibrations"), computed_values={"life_path": lp, "soul_urge": core["soul_urge"], "digital_vibration": dv}, calculation_trace={"life_path": lp_trace, "digital_vibration": {"normalized_digits": nd, "raw": sum(int(c) for c in nd), "reduced": dv.reduced}, "compatibility": {"life_path": lpc, "soul_urge": sc, "overall_score": overall}}, report_sections=sections, summary="This report treats your chosen digital number as a symbolic vibration and compares it with your native numerology profile.", guidance="Use digital-vibration checks as a practical comparison tool when choosing between multiple numbers.", remedy_note="Do not treat a digital-number result as more important than the broader timing and identity patterns in your full profile.")


def _build_residential_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.residential_number:
        raise HTTPException(status_code=400, detail="residential_number is required for this tile")
    lp, lp_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    nd = _normalize_number_string(payload.residential_number)
    if not nd:
        raise HTTPException(status_code=400, detail="residential_number must contain digits")
    hv = _build_number(sum(int(c) for c in nd))
    lpc = _score_compatibility(lp.reduced, hv.reduced)
    sc = _score_compatibility(core["soul_urge"].reduced, hv.reduced)
    overall = round(lpc["score"] * 0.55 + sc["score"] * 0.45, 2)
    sections = [NumerologyReportSection(section_id="home_vibration", title="Home Vibration", summary=f"The home reduces to a residential vibration of {hv.reduced}.", body="This is the main environmental vibration of the home number."), NumerologyReportSection(section_id="home_fit", title="Environment Fit", summary=f"The current overall home-fit score is {overall}.", body="Use this as an alignment signal rather than a verdict on the home."), NumerologyReportSection(section_id="adjustment_notes", title="Adjustment Notes", summary="A mixed result does not automatically mean the home is wrong.", body="It may simply mean balance, awareness, and remedial support matter more.")]
    return NumerologyReportPayload(**_report_base(payload, user_email, "numerology_residential_compatibility", "residential-house-number-compatibility"), computed_values={"life_path": lp, "soul_urge": core["soul_urge"], "residential_vibration": hv}, calculation_trace={"life_path": lp_trace, "residential_vibration": {"normalized_digits": nd, "raw": sum(int(c) for c in nd), "reduced": hv.reduced}, "compatibility": {"life_path": lpc, "soul_urge": sc, "overall_score": overall}}, report_sections=sections, summary="This report treats your house number as an environmental vibration and compares it with your native numerology profile.", guidance="Use residential compatibility as a home-awareness tool and combine it with lived experience, comfort, and environmental balance.", remedy_note="A mixed result does not automatically mean the home is wrong; it may simply mean balance and remedial support matter more.")


def _build_business_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.business_name:
        raise HTTPException(status_code=400, detail="business_name is required for this tile")
    lp, lp_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    be = _calculate_expression(payload.business_name, payload.numerology_system, payload.y_mode)
    f2b = _score_compatibility(core["expression"].reduced, be.reduced)
    p2b = _score_compatibility(lp.reduced, be.reduced)
    overall = round(f2b["score"] * 0.55 + p2b["score"] * 0.45, 2)
    sections = [NumerologyReportSection(section_id="founder_brand_alignment", title="Founder-To-Brand Alignment", summary=f"Founder expression-to-brand compatibility reads as {f2b['band']}.", body="This layer checks whether the brand name appears to amplify, neutralize, or create friction with the founder's visible style."), NumerologyReportSection(section_id="market_vibration", title="Market Vibration", summary=f"The business name reduces to {be.reduced}.", body="The brand number can be read as the outer signal the market receives."), NumerologyReportSection(section_id="optimization_notes", title="Optimization Notes", summary=f"The current founder-to-brand optimization score is {overall}.", body="A stronger score suggests cleaner symbolic fit, while a mixed score may still be workable.")]
    return NumerologyReportPayload(**_report_base(payload, user_email, "numerology_brand_optimization", "business-brand-name-optimization"), computed_values={"life_path": lp, "founder_expression": core["expression"], "business_expression": be}, calculation_trace={"life_path": lp_trace, "compatibility": {"founder_to_brand": f2b, "path_to_brand": p2b, "overall_score": overall}}, report_sections=sections, summary="This report compares the brand name with the founder profile to estimate naming fit, resonance, and symbolic business alignment.", guidance="Use this as a decision-support layer alongside branding clarity, audience fit, and real-world usability.", remedy_note="No name should be treated as a substitute for business model, timing, or execution.")


def _build_baby_name_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    if not payload.candidate_name:
        raise HTTPException(status_code=400, detail="candidate_name is required for this tile")
    lp, lp_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    ce = _calculate_expression(payload.candidate_name, payload.numerology_system, payload.y_mode)
    c2n = _score_compatibility(lp.reduced, ce.reduced)
    s2n = _score_compatibility(core["soul_urge"].reduced, ce.reduced)
    overall = round(c2n["score"] * 0.6 + s2n["score"] * 0.4, 2)
    sections = [NumerologyReportSection(section_id="child_vibration", title="Child Vibration Baseline", summary=f"Life Path {lp.reduced} provides the child's foundational birth vibration for naming comparison.", body="This baseline acts as the core reference point for checking whether a candidate name feels supportive, mixed, or frictional."), NumerologyReportSection(section_id="candidate_name_fit", title="Candidate Name Fit", summary=f"The candidate name reduces to {ce.reduced} and currently reads as {c2n['band']} against the child's Life Path.", body="A strong fit may feel cleaner and more harmonious, while mixed fit may simply call for comparison with alternate options."), NumerologyReportSection(section_id="selection_guidance", title="Selection Guidance", summary=f"The current baby-name suitability score is {overall}.", body="Naming should also consider usability, emotional resonance, family preference, and long-term comfort.")]
    return NumerologyReportPayload(**_report_base(payload, user_email, "numerology_baby_name", "auspicious-baby-name-selection"), computed_values={"life_path": lp, "soul_urge": core["soul_urge"], "candidate_expression": ce}, calculation_trace={"life_path": lp_trace, "compatibility": {"child_path_to_name": c2n, "child_soul_to_name": s2n, "overall_score": overall}}, report_sections=sections, summary="This report compares a candidate name with the child's birth vibration to estimate naming harmony and suitability.", guidance="Use this result to compare naming options while also considering family resonance, pronunciation, and long-term comfort.", remedy_note="No candidate name should be treated as a guarantee of the child's future.")


def _build_premium_ankjyotish_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    # Only time_of_birth and place_of_birth are required from the user.
    # lagna_sign, moon_sign, and nakshatra_name are auto-computed via pyswisseph.
    missing = [k for k, v in {"time_of_birth": payload.time_of_birth, "place_of_birth": payload.place_of_birth}.items() if not v]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required fields for premium_ankjyotish_report: {', '.join(missing)}")

    # Auto-compute Vedic markers from birth data unless the caller already supplied them
    lagna_sign = payload.lagna_sign
    moon_sign = payload.moon_sign
    nakshatra_name = payload.nakshatra_name
    if not (lagna_sign and moon_sign and nakshatra_name):
        try:
            chart = calculate_vedic_chart(payload.date_of_birth, payload.time_of_birth, payload.place_of_birth)
            lagna_sign = lagna_sign or chart["lagna"]["sign"]
            moon_sign = moon_sign or chart["moon_sign"]["sign"]
            nakshatra_name = nakshatra_name or chart["nakshatra"]["name"]
        except Exception:
            lagna_sign = lagna_sign or "Unknown"
            moon_sign = moon_sign or "Unknown"
            nakshatra_name = nakshatra_name or "Unknown"

    now = _now()
    lp, lp_trace = _calculate_life_path(payload.date_of_birth, payload.reduction_method)
    core = _calculate_core_four(payload.full_birth_name, payload.numerology_system, payload.y_mode)
    curr_expr = _calculate_expression(payload.current_popular_name, payload.numerology_system, payload.y_mode) if payload.current_popular_name else None
    loshu_payload = _build_lo_shu_grid_payload(payload.date_of_birth)
    karmic = _detect_karmic_debts([lp.raw, core["expression"].raw, core["soul_urge"].raw, core["personality"].raw])
    py, py_trace = _calculate_personal_year(payload.date_of_birth, now.year)
    pm = _calculate_personal_month(py.reduced, now.month)
    pd = _calculate_personal_day(pm.reduced, now.day)
    lucky = _lucky_elements_table(lp.reduced, core["expression"].reduced, core["soul_urge"].reduced)
    remediation = _remediation_plan(lp.reduced)
    name_align = _score_compatibility(core["expression"].reduced, curr_expr.reduced) if curr_expr else None
    vedic_ref = {"lagna_sign": lagna_sign, "moon_sign": moon_sign, "nakshatra_name": nakshatra_name, "cross_reference_note": "These Vedic markers are computed from birth data via pyswisseph and referenced here for symbolic cross-alignment only."}
    sections = [
        NumerologyReportSection(section_id="core_number_profile", title="Core Number Profile", summary=f"Life Path {lp.reduced}, Expression {core['expression'].reduced}, Soul Urge {core['soul_urge'].reduced}, and Personality {core['personality'].reduced} create the main numerological blueprint.", body="This section synthesizes your native directional number, visible expression, private motivation, and outer style into one consolidated core profile."),
        NumerologyReportSection(section_id="lo_shu_grid", title="Lo Shu Grid", summary=f"Missing numbers: {', '.join(str(n) for n in loshu_payload['missing_numbers']) if loshu_payload['missing_numbers'] else 'none'}. Repeated: {', '.join(str(n) for n in loshu_payload['repeated_numbers']) if loshu_payload['repeated_numbers'] else 'none'}.", body="The visual Lo Shu grid is delivered as structured JSON in the report payload for Temple-side rendering."),
        NumerologyReportSection(section_id="karmic_debt_audit", title="Karmic Debt Audit", summary=f"Detected karmic debt numbers: {', '.join(str(k) for k in karmic) if karmic else 'none'}.", body="Karmic debt numbers are treated as recurring learning signatures and are paired with practical remediation framing."),
        NumerologyReportSection(section_id="timing_window", title="Personal Year, Month, And Day Timing", summary=f"Current timing reads as Personal Year {py.reduced}, Personal Month {pm.reduced}, and Personal Day {pd.reduced}.", body="Use this section to understand the immediate timing climate and the broader three-year progression ahead."),
        NumerologyReportSection(section_id="name_vibration_analysis", title="Name Vibration Analysis", summary=(f"Current name usage reduces to {curr_expr.reduced} and reads as {name_align['band']} against the birth-name expression pattern." if curr_expr and name_align else "No current popular name was provided, so this section remains anchored to the birth-name baseline only."), body="This section compares current-name usage with the birth-name blueprint to understand public-name fit and refinement potential."),
        NumerologyReportSection(section_id="vedic_cross_reference", title="Vedic Cross-Reference", summary=f"Lagna {lagna_sign}, Moon Sign {moon_sign}, and Nakshatra {nakshatra_name} are referenced for symbolic cross-alignment.", body="These Vedic markers are auto-computed from your birth details and used as supporting Vedic context within the numerology reading."),
        NumerologyReportSection(section_id="lucky_elements_table", title="Lucky Elements Table", summary=f"Dominant element: {lucky['dominant_element']}; supportive day: {lucky['supportive_day']}.", body="This section consolidates supportive colors, element trends, and repeating number preferences into a quick-reference table."),
        NumerologyReportSection(section_id="remediation_plan", title="7-Day Remediation Plan", summary="A short seven-day cycle is provided to help convert numerological insight into practical daily alignment.", body="Use the seven-day plan as a structured reset rather than as a promise of immediate external change."),
    ]
    base = _report_base(payload, user_email, "numerology_premium_ankjyotish", "premium-ankjyotish-report")
    base["document_type"] = "premium_ankjyotish_report"
    base["lagna_sign"] = lagna_sign
    base["moon_sign"] = moon_sign
    base["nakshatra_name"] = nakshatra_name
    return NumerologyReportPayload(**base, computed_values={"life_path": lp, "expression": core["expression"], "soul_urge": core["soul_urge"], "personality": core["personality"], "personal_year": py, "personal_month": pm, "personal_day": pd}, calculation_trace={"life_path": lp_trace, "personal_year": py_trace, "lo_shu_grid_payload": loshu_payload, "karmic_debts": karmic, "timing_forecast": _timing_forecast_lines(now.year, py.reduced), "lucky_elements_table": lucky, "vedic_cross_reference": vedic_ref, "name_alignment": name_align, "remediation_plan": remediation}, report_sections=sections, summary="This premium Ankjyotish report combines core numerology, Lo Shu, karmic audit, timing, name analysis, and Vedic cross-reference into one structured life-analysis reading.", guidance="Use this premium report as a structured alignment map for identity, timing, remedies, and practical life decisions.", remedy_note="Remedial practices work best when followed consistently over a 7-day cycle. Treat each day's guidance as a gentle reset, not a strict obligation.")


def _build_report(payload: NumerologyGenerateRequest, user_email: str) -> NumerologyReportPayload:
    builders = {"life_path_soul_mission": _build_life_path_report, "name_correction_energy_alignment": _build_name_correction_report, "favorable_timing": _build_timing_report, "karmic_debt_loshu": _build_karmic_loshu_report, "relationship_compatibility": _build_relationship_report, "career_guidance": _build_career_report, "lucky_digital_vibrations": _build_digital_report, "residential_compatibility": _build_residential_report, "business_brand_optimization": _build_business_report, "baby_name_selection": _build_baby_name_report, "premium_ankjyotish_report": _build_premium_ankjyotish_report}
    builder = builders.get(payload.tile_code)
    if not builder:
        raise HTTPException(status_code=400, detail="Unsupported numerology tile")
    return builder(payload, user_email)


@router.get("/tiles", response_model=NumerologyTileListResponse)
async def list_numerology_tiles() -> NumerologyTileListResponse:
    return NumerologyTileListResponse(tiles=DEFAULT_TILES)


@router.post("/report/generate", response_model=NumerologyGenerateResponse)
async def generate_numerology_report(payload: NumerologyGenerateRequest, request: Request) -> NumerologyGenerateResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(_get_db(request))
    report = _build_report(payload, user_email)
    report = await enrich_numerology_report_with_claude(report)

    # ── Internal checkpoint NUM-01 / NUM-04 ──────────────────────────────────
    # NUM-01: Confirm Claude enrichment ran — summary should not be generic
    #         fallback boilerplate.  We detect the two most common fallback
    #         openers; if either appears, enrichment silently fell back.
    _FALLBACK_MARKERS = ("Your profile centers on Life Path", "This premium Ankjyotish report combines")
    if any(report.summary.startswith(m) for m in _FALLBACK_MARKERS):
        _log.warning(
            "NUM-01 CHECKPOINT: Claude enrichment fell back to static text "
            "[tile=%s user=%s].  Check ANTHROPIC_API_KEY and numerology_prompt_service.",
            payload.tile_code, user_email,
        )
    else:
        _log.info("NUM-01 OK: Claude enrichment active [tile=%s]", payload.tile_code)

    # NUM-04: Confirm remedy_note contains no internal CODEX handoff text.
    _INTERNAL_MARKERS = ("Temple App renders", "structured JSON", "delivery note", "dropin")
    if report.remedy_note and any(m.lower() in report.remedy_note.lower() for m in _INTERNAL_MARKERS):
        _log.error(
            "NUM-04 CHECKPOINT: remedy_note contains internal text — "
            "must NOT reach users.  [tile=%s] remedy_note=%r",
            payload.tile_code, report.remedy_note[:120],
        )
    else:
        _log.info("NUM-04 OK: remedy_note is user-facing [tile=%s]", payload.tile_code)
    # ─────────────────────────────────────────────────────────────────────────

    await collection.insert_one(report.model_dump(mode="python"))
    return NumerologyGenerateResponse(report=report)


@router.get("/report/{report_id}", response_model=NumerologyReadingResponse)
async def get_numerology_report(report_id: str, request: Request) -> NumerologyReadingResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(_get_db(request))
    report = await collection.find_one({"id": report_id, "user_email": user_email})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return NumerologyReadingResponse(report=NumerologyReportPayload(**report))


@router.get("/history", response_model=NumerologyHistoryResponse)
async def get_numerology_history(request: Request, page: int = Query(default=1, ge=1), limit: int = Query(default=10, ge=1, le=50), tile_code: str | None = None, bookmarked: bool | None = None) -> NumerologyHistoryResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(_get_db(request))
    query: dict[str, Any] = {"user_email": user_email, "document_type": {"$in": ["report", "premium_ankjyotish_report"]}}
    if tile_code:
        query["tile_code"] = tile_code
    if bookmarked is not None:
        query["bookmarked"] = bookmarked
    skip = (page - 1) * limit
    cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    total = await collection.count_documents(query)
    items = [NumerologyHistoryItem(id=doc["id"], report_type=doc["report_type"], report_slug=doc["report_slug"], tile_code=doc["tile_code"], summary=doc["summary"], focus_area=doc["focus_area"], created_at=doc["created_at"], bookmarked=doc.get("bookmarked", False)) for doc in docs]
    return NumerologyHistoryResponse(items=items, page=page, limit=limit, total=total, has_more=skip + limit < total)


@router.post("/history/{report_id}/bookmark", response_model=NumerologyBookmarkResponse)
async def bookmark_numerology_report(request: Request, report_id: str, payload: NumerologyBookmarkRequest) -> NumerologyBookmarkResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(_get_db(request))
    result = await collection.update_one({"id": report_id, "user_email": user_email, "document_type": {"$in": ["report", "premium_ankjyotish_report"]}}, {"$set": {"bookmarked": payload.bookmarked, "updated_at": _now()}})
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
    feedback_doc = {"id": str(uuid4()), "document_type": "feedback", "module": "numerology", "user_email": user_email, "report_id": payload.report_id, "tile_code": report.get("tile_code"), "feedback_type": payload.feedback_type, "value": payload.value, "created_at": _now(), "updated_at": _now()}
    await collection.insert_one(feedback_doc)
    return NumerologyFeedbackResponse(message="Feedback received.")
