from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from individual_reports_prompt_common import try_claude_generation
from vedic_calculator import (
    SIGN_LORDS,
    SIGN_ORDER,
    build_dasha_timeline,
    calculate_donut_resilience,
    calculate_graha_drishti,
    calculate_vimshottari_dasha,
    generate_10_year_horizon,
    get_current_dasha,
    get_planet_dignity,
)
from vedic_shared_utils import build_natal_snapshot


router = APIRouter(prefix="/api/reports", tags=["reports"])
PROMPT_PATH = Path(__file__).parent / "prompts" / "vedic_12areas_system_prompt.txt"

REPORT_FOCUS_MAP: dict[str, dict[str, Any]] = {
    "life_cycles": {"focus_area": "Self, Identity & Life Journey", "house_number": 1},
    "wealth_blueprint": {"focus_area": "Wealth, Values & Abundance", "house_number": 2},
    "retrograde_survival": {"focus_area": "Communication, Courage & Planning", "house_number": 3},
    "lunar_cycle_wellness": {"focus_area": "Home, Emotional Foundation & Inner Rhythm", "house_number": 4},
    "romance_creative": {"focus_area": "Romance, Creativity & Intelligence", "house_number": 5},
    "vitality_health": {"focus_area": "Health, Daily Rhythm & Service", "house_number": 6},
    "partnership_window": {"focus_area": "Partnerships, Marriage & Relating", "house_number": 7},
    "shadow_self": {"focus_area": "Transformation, Hidden Self & Occult", "house_number": 8},
    "dharma_purpose": {"focus_area": "Dharma, Higher Purpose & Wisdom", "house_number": 9},
    "career_blueprint": {"focus_area": "Career & Work", "house_number": 10},
    "gains_network": {"focus_area": "Gains, Aspirations & Social Network", "house_number": 11},
    "karmic_debt": {"focus_area": "Karma, Past Lives & Liberation", "house_number": 12},
}

BENEFIC_DASHA_LORDS = {"Jupiter", "Venus", "Mercury", "Moon"}
MALEFIC_DASHA_LORDS = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EnhancementBirthData(StrictModel):
    date: str | None = None
    time: str | None = None
    date_of_birth: str | None = None
    time_of_birth: str | None = None
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city_name: str | None = None


class RunningDashaInput(StrictModel):
    start: str
    end: str
    lord: str | None = None
    planet: str | None = None
    status: str | None = None


class EnhancementRequest(StrictModel):
    user_id: str | None = None
    report_type: str | None = None
    birth_data: EnhancementBirthData | None = None
    input_payload: dict[str, Any] | None = None
    focus_area: str | None = None
    house_number: int | None = None
    house_cusp_sign: str | None = None
    house_lord: str | None = None
    house_lord_placement_sign: str | None = None
    essential_dignity: str | None = None
    benefic_aspects_count: int | None = None
    malefic_aspects_count: int | None = None
    natal_cusp_longitude: float | None = None
    planet_positions: dict[str, int] | None = None
    running_dashas: list[RunningDashaInput] | None = None


class HorizonFlag(StrictModel):
    year: str
    status: str
    trigger: str


class EnhancementResponse(StrictModel):
    donut_resilience_percentage: int
    ten_year_horizon_flags: list[HorizonFlag] = Field(default_factory=list)
    graha_drishti_on_house: list[str] = Field(default_factory=list)
    generated_report_markdown: str


def _title_dignity(raw: str) -> str:
    mapping = {
        "exalted": "Exalted",
        "moolatrikona": "Moolatrikona",
        "own_sign": "Own Sign",
        "debilitated": "Debilitated",
        "enemy": "Enemy Sign",
        "enemy_sign": "Enemy Sign",
        "friendly": "Neutral",
        "neutral": "Neutral",
    }
    return mapping.get(raw, "Neutral")


def _read_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8").strip()


def _build_birth_data(payload: EnhancementRequest) -> EnhancementBirthData:
    if payload.birth_data:
        return payload.birth_data
    if payload.input_payload:
        return EnhancementBirthData.model_validate(payload.input_payload)
    raise HTTPException(status_code=400, detail="Birth data or input payload is required for enhanced analysis.")


def _normalized_birth_fields(birth_data: EnhancementBirthData) -> tuple[str, str]:
    date_text = birth_data.date or birth_data.date_of_birth
    time_text = birth_data.time or birth_data.time_of_birth
    if not date_text or not time_text:
        raise HTTPException(status_code=400, detail="Birth date and time are required for enhanced analysis.")
    return date_text, time_text


def _planet_sign_index(sign_name: str) -> int:
    return SIGN_ORDER.index(sign_name) + 1


def _signed_distance(start_sign: str, target_sign: str) -> int:
    return (SIGN_ORDER.index(target_sign) - SIGN_ORDER.index(start_sign)) % 12


def _house_midpoint_longitude(sign_name: str) -> float:
    return (SIGN_ORDER.index(sign_name) * 30.0) + 15.0


def _planet_status(planet_name: str, natal: dict[str, Any]) -> str:
    if planet_name in BENEFIC_DASHA_LORDS:
        return "Benefic"
    if planet_name in MALEFIC_DASHA_LORDS:
        return "Malefic"
    for house_number in (6, 8, 12):
        if SIGN_LORDS[natal["houses"][str(house_number)]] == planet_name:
            return "Malefic"
    return "Neutral"


def _parse_running_dashas(raw_dashas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for dasha in raw_dashas:
        parsed.append(
            {
                "start": datetime.strptime(dasha["start"], "%Y-%m-%d").date(),
                "end": datetime.strptime(dasha["end"], "%Y-%m-%d").date(),
                "lord": dasha.get("lord") or dasha.get("planet"),
                "status": dasha.get("status") or "Neutral",
            }
        )
    return parsed


def _build_payload(payload: EnhancementRequest) -> dict[str, Any]:
    report_type = payload.report_type
    if not report_type:
        raise HTTPException(status_code=400, detail="report_type is required.")
    focus_meta = REPORT_FOCUS_MAP.get(report_type)
    if not focus_meta:
        raise HTTPException(status_code=400, detail=f"Unsupported report_type: {report_type}")

    birth_data = _build_birth_data(payload)
    date_text, time_text = _normalized_birth_fields(birth_data)
    natal = build_natal_snapshot(
        date_text=date_text,
        time_text=time_text,
        latitude=birth_data.latitude,
        longitude=birth_data.longitude,
        timezone_name=birth_data.timezone,
        city_name=birth_data.city_name,
    )
    house_number = int(payload.house_number or focus_meta["house_number"])
    house_sign = str(payload.house_cusp_sign or natal["houses"][str(house_number)])
    house_lord = str(payload.house_lord or natal["house_lords"][str(house_number)])
    house_lord_sign = str(payload.house_lord_placement_sign or natal["planets"][house_lord]["sign"])
    essential_dignity = str(
        payload.essential_dignity
        or _title_dignity(get_planet_dignity(house_lord, house_lord_sign, float(natal["planets"][house_lord]["degree"])))
    )
    planet_positions = payload.planet_positions or {
        name: _planet_sign_index(str(details["sign"]))
        for name, details in natal["planets"].items()
    }
    drishti_map = calculate_graha_drishti(planet_positions)
    target_sign_index = _planet_sign_index(house_sign)
    graha_drishti_on_house = sorted([planet for planet, signs in drishti_map.items() if target_sign_index in signs])

    house_lord_sign_index = _planet_sign_index(house_lord_sign)
    house_lord_aspects = [planet for planet, signs in drishti_map.items() if house_lord_sign_index in signs and planet != house_lord]
    benefic_aspects_count = payload.benefic_aspects_count
    if benefic_aspects_count is None:
        benefic_aspects_count = len([planet for planet in house_lord_aspects if planet in {"Jupiter", "Venus"}])
    malefic_aspects_count = payload.malefic_aspects_count
    if malefic_aspects_count is None:
        malefic_aspects_count = len([planet for planet in house_lord_aspects if planet in {"Saturn", "Mars", "Rahu", "Ketu"}])

    donut_resilience = calculate_donut_resilience(
        {
            "essential_dignity": essential_dignity,
            "benefic_aspects_count": benefic_aspects_count,
            "malefic_aspects_count": malefic_aspects_count,
        }
    )

    if payload.running_dashas:
        running_dashas = [
            {
                "start": row.start,
                "end": row.end,
                "lord": row.lord or row.planet,
                "status": row.status or "Neutral",
            }
            for row in payload.running_dashas
        ]
    else:
        dashas = calculate_vimshottari_dasha(date_text, float(natal["planets"]["Moon"]["longitude"]))
        running_dashas = [
            {
                "start": row["start"],
                "end": row["end"],
                "lord": row["planet"],
                "status": _planet_status(str(row["planet"]), natal),
            }
            for row in dashas
        ]
    parsed_dashas = _parse_running_dashas(running_dashas)
    natal_cusp_longitude = float(payload.natal_cusp_longitude or _house_midpoint_longitude(house_sign))
    horizon_flags = generate_10_year_horizon(natal_cusp_longitude, parsed_dashas)

    current_dasha = get_current_dasha(
        [
            {
                "planet": row["lord"],
                "start": row["start"].isoformat(),
                "end": row["end"].isoformat(),
            }
            for row in parsed_dashas
        ]
    )
    timeline = build_dasha_timeline(date_text, float(natal["planets"]["Moon"]["longitude"]))
    active_antardasha = None
    today = datetime.now().date()
    for maha in timeline:
        maha_start = datetime.strptime(maha["start"], "%Y-%m-%d").date()
        maha_end = datetime.strptime(maha["end"], "%Y-%m-%d").date()
        if maha_start <= today <= maha_end:
            for antar in maha.get("antardashas", []):
                antar_start = datetime.strptime(antar["start"], "%Y-%m-%d").date()
                antar_end = datetime.strptime(antar["end"], "%Y-%m-%d").date()
                if antar_start <= today <= antar_end:
                    active_antardasha = antar
                    break
            break

    active_dasha_layer = {
        "lord": current_dasha.get("planet"),
        "start": current_dasha.get("start"),
        "end": current_dasha.get("end"),
        "antardasha_lord": active_antardasha.get("planet") if active_antardasha else None,
        "antardasha_start": active_antardasha.get("start") if active_antardasha else None,
        "antardasha_end": active_antardasha.get("end") if active_antardasha else None,
    }

    return {
        "metrics": {
            "donut_resilience_percentage": donut_resilience,
            "ten_year_horizon_flags": horizon_flags,
        },
        "vedic_analytics": {
            "focus_area": payload.focus_area or focus_meta["focus_area"],
            "house_number": house_number,
            "sign_on_cusp": house_sign,
            "house_lord": house_lord,
            "lord_placement_sign": house_lord_sign,
            "essential_dignity": essential_dignity,
            "graha_drishti_on_house": graha_drishti_on_house,
            "active_dasha_layer": active_dasha_layer,
        },
    }


def _fallback_markdown(data: dict[str, Any]) -> str:
    metrics = data["metrics"]
    analytics = data["vedic_analytics"]
    flags = metrics["ten_year_horizon_flags"]
    auspicious_years = ", ".join(flag["year"] for flag in flags if flag["status"] == "Auspicious") or "No strongly auspicious year dominates the horizon."
    cautious_years = ", ".join(flag["year"] for flag in flags if flag["status"] == "Inauspicious") or "No strongly adverse year dominates the horizon."
    drishti_text = ", ".join(analytics["graha_drishti_on_house"]) or "No strong graha drishti surfaces as a defining pressure."
    return (
        f"### Page 1\n"
        f"{analytics['focus_area']} is being filtered through House {analytics['house_number']} in {analytics['sign_on_cusp']}, with {analytics['house_lord']} carrying the core load from {analytics['lord_placement_sign']}. "
        f"The Structural Resilience score is {metrics['donut_resilience_percentage']}%, which suggests how naturally stable this area feels before timing is layered on. "
        f"In the next ten years, the clearest supportive windows are: {auspicious_years}. The clearest caution windows are: {cautious_years}.\n\n"
        f"### Page 2\n"
        f"| House Number | Cusp Sign | House Lord | Lord Placement | Essential Dignity |\n"
        f"| --- | --- | --- | --- | --- |\n"
        f"| {analytics['house_number']} | {analytics['sign_on_cusp']} | {analytics['house_lord']} | {analytics['lord_placement_sign']} | {analytics['essential_dignity']} |\n\n"
        f"The house lord modifies this area through its sign placement, so the quality of {analytics['lord_placement_sign']} becomes part of the strategy for this life area. "
        f"Graha Drishti on the house: {drishti_text}. "
        f"The current dasha layer is led by {analytics['active_dasha_layer']['lord']} with Antardasha support from {analytics['active_dasha_layer'].get('antardasha_lord') or 'no distinct sub-period flagged'}.\n\n"
        f"### Page 3\n"
        f"The foundational strengths of this area come from what is already structurally stable in the chart: the house itself, the dignity of its lord, and the type of planets casting aspect pressure on it. "
        f"When the score is moderate or high, the chart usually responds well to consistency, cleaner priorities, and environments that mirror the house's natural theme. "
        f"When pressure rises, recurring loops often come from the very planets casting the strongest conditions on this house.\n\n"
        f"### Page 4\n"
        f"Use the horizon as an operational guide rather than a prediction script: act more boldly in supportive years, and consolidate, simplify, or prepare in cautious years. "
        f"Behavioral changes matter most when they reduce friction with the house lord's nature. "
        f"Traditional Vedic support works best here as daily rhythm, environmental alignment, and disciplined spiritual practice rather than dramatic intervention."
    )


def _build_prompt(data: dict[str, Any]) -> str:
    system_prompt = _read_system_prompt()
    return (
        f"{system_prompt}\n\n"
        "Return valid JSON only with a single key:\n"
        '- "generated_report_markdown": string\n\n'
        f"Payload:\n{json.dumps(data, ensure_ascii=True)}"
    )


@router.post("/enhanced-analysis", response_model=EnhancementResponse)
async def enhanced_analysis(payload: EnhancementRequest) -> EnhancementResponse:
    data = _build_payload(payload)
    content = await try_claude_generation(_build_prompt(data), max_tokens=1800, temperature=0.4)
    markdown = None
    if isinstance(content, dict):
        markdown = content.get("generated_report_markdown") or content.get("markdown") or content.get("report")
    elif isinstance(content, str):
        markdown = content
    if not markdown:
        markdown = _fallback_markdown(data)
    return EnhancementResponse(
        donut_resilience_percentage=int(data["metrics"]["donut_resilience_percentage"]),
        ten_year_horizon_flags=[HorizonFlag(**item) for item in data["metrics"]["ten_year_horizon_flags"]],
        graha_drishti_on_house=list(data["vedic_analytics"]["graha_drishti_on_house"]),
        generated_report_markdown=str(markdown),
    )
