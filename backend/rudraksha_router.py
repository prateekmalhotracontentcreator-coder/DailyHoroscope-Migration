from __future__ import annotations

import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from rudraksha_content import (
    RUDRAKSHA_MUKHIS,
    RUDRAKSHA_MUKHIS_BY_NUMBER,
    get_planet_rudraksha_document,
    get_problem_rudraksha_document,
    get_sign_rudraksha_document,
)
from vedic_calculator import SIGN_ORDER, calculate_graha_drishti, calculate_vedic_chart


router = APIRouter(prefix="/api/rudraksha", tags=["rudraksha"])

BENEFIC_ASPECTORS = {"Jupiter", "Venus", "Mercury", "Moon"}
CLASSICAL_PLANETS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
PLANET_TO_PRIMARY_MUKHI = {
    "Sun": 1,
    "Moon": 2,
    "Mars": 3,
    "Mercury": 4,
    "Jupiter": 5,
    "Venus": 6,
    "Saturn": 7,
    "Rahu": 8,
    "Ketu": 9,
}
PLANET_TO_RECOMMENDATIONS = {
    "Sun": [1, 12],
    "Moon": [2],
    "Mars": [3],
    "Mercury": [4],
    "Jupiter": [5],
    "Venus": [6],
    "Saturn": [7, 14],
    "Rahu": [8],
    "Ketu": [9],
}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RudrakshaCalculatorRequest(StrictModel):
    date: str
    time: str
    place: str


def _db(request: Request):
    db = getattr(getattr(request.app, "state", None), "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available on request.app.state.db.")
    return db


def _clean_document(document: dict[str, Any]) -> dict[str, Any]:
    payload = dict(document)
    payload.pop("_id", None)
    return payload


async def _load_all_mukhis(request: Request) -> list[dict[str, Any]]:
    try:
        documents = await _db(request).rudraksha_mukhis.find({}, {"_id": 0}).sort("mukhi", 1).to_list(length=50)
    except Exception:
        documents = []
    return documents or [dict(item) for item in RUDRAKSHA_MUKHIS]


async def _load_single_mukhi(request: Request, mukhi: int) -> dict[str, Any] | None:
    try:
        document = await _db(request).rudraksha_mukhis.find_one({"mukhi": mukhi}, {"_id": 0})
    except Exception:
        document = None
    return _clean_document(document) if document else dict(RUDRAKSHA_MUKHIS_BY_NUMBER.get(mukhi) or {})


async def _load_slug_document(
    request: Request,
    collection_name: str,
    slug: str,
    fallback_loader,
) -> dict[str, Any] | None:
    try:
        collection = _db(request)[collection_name]
        document = await collection.find_one({"slug": slug}, {"_id": 0})
    except Exception:
        document = None

    if document:
        return _clean_document(document)

    fallback = fallback_loader(slug)
    return dict(fallback) if fallback else None


def _planet_payload(chart: dict[str, Any], planet: str) -> dict[str, Any]:
    for key, payload in (chart.get("planets") or {}).items():
        plain_name = str(key).split("(")[0].strip()
        if plain_name == planet:
            return payload
    raise KeyError(f"Planet payload not found for {planet}")


def _planet_sign_index(chart: dict[str, Any], planet: str) -> int:
    payload = _planet_payload(chart, planet)
    return SIGN_ORDER.index(payload["sign"]) + 1


def _graha_drishti_map(chart: dict[str, Any]) -> dict[str, list[int]]:
    positions: dict[str, int] = {}
    for key in (chart.get("planets") or {}):
        plain_name = str(key).split("(")[0].strip()
        try:
            positions[plain_name] = _planet_sign_index(chart, plain_name)
        except Exception:
            continue
    return calculate_graha_drishti(positions)


def _benefic_support(chart: dict[str, Any], planet: str, drishti_map: dict[str, list[int]]) -> list[str]:
    target_sign = _planet_sign_index(chart, planet)
    supporters: list[str] = []
    for aspector in BENEFIC_ASPECTORS:
        if aspector == planet:
            continue
        aspected_signs = drishti_map.get(aspector) or []
        if target_sign in aspected_signs:
            supporters.append(aspector)
    return supporters


def _is_planet_weak(chart: dict[str, Any], planet: str, drishti_map: dict[str, list[int]]) -> bool:
    payload = _planet_payload(chart, planet)
    if payload.get("dignity") == "debilitated":
        return True
    house = int(payload.get("house") or 0)
    if house in {6, 8, 12} and not _benefic_support(chart, planet, drishti_map):
        return True
    return False


def _current_mahadasha(chart: dict[str, Any]) -> str:
    current = chart.get("current_dasha") or {}
    return str(current.get("planet") or "").strip()


def _atmakaraka(chart: dict[str, Any]) -> str:
    highest_planet = ""
    highest_degree = -1.0
    for planet in CLASSICAL_PLANETS:
        payload = _planet_payload(chart, planet)
        degree = float(payload.get("degree") or 0.0)
        if degree > highest_degree:
            highest_planet = planet
            highest_degree = degree
    return highest_planet


def _weakest_dusthana_lord(chart: dict[str, Any]) -> str | None:
    houses = chart.get("houses") or {}
    candidates: list[tuple[float, str]] = []
    seen: set[str] = set()
    for house_num in (6, 8, 12):
        house = houses.get(house_num) or {}
        lord = str(house.get("lord") or "").strip()
        if not lord or lord in seen:
            continue
        seen.add(lord)
        payload = _planet_payload(chart, lord)
        shadbala = payload.get("shadbala") or {}
        total_rupas = float(shadbala.get("total_rupas") or 0.0)
        candidates.append((total_rupas, lord))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0])
    return candidates[0][1]


def _is_shadbala_weak(chart: dict[str, Any], planet: str) -> bool:
    payload = _planet_payload(chart, planet)
    shadbala = payload.get("shadbala") or {}
    if "is_strong" in shadbala:
        return not bool(shadbala.get("is_strong"))
    return False


def _reason_for_planet(chart: dict[str, Any], planet: str, drishti_map: dict[str, list[int]]) -> str:
    current_mahadasha = _current_mahadasha(chart)
    if current_mahadasha == planet:
        return f"{planet} Mahadasha is active, so this bead supports that planetary current with steadier expression."
    if _is_planet_weak(chart, planet, drishti_map):
        payload = _planet_payload(chart, planet)
        if payload.get("dignity") == "debilitated":
            return f"{planet} appears debilitated in your chart, so this bead is used to support its weaker significations."
        return f"{planet} sits in a difficult house without clear benefic support, so this bead is chosen as a stabilising remedy."
    return f"This bead aligns with {planet}-linked themes in your chart."


def _reason_for_lagna_lord(chart: dict[str, Any], drishti_map: dict[str, list[int]]) -> tuple[str, str] | None:
    lagna = chart.get("lagna") or {}
    lord = str(lagna.get("lord") or "").strip()
    sign = str(lagna.get("sign_vedic") or lagna.get("sign") or "").strip()
    if not lord or not _is_planet_weak(chart, lord, drishti_map):
        return None
    return lord, f"Your Lagna lord {lord} is under strain, so a {PLANET_TO_PRIMARY_MUKHI[lord]}-Mukhi is added to reinforce the chart's foundation through {sign} rising energy."


def _reason_for_rahu(chart: dict[str, Any]) -> str | None:
    lagna = chart.get("lagna") or {}
    if _current_mahadasha(chart) == "Rahu":
        return "Rahu Mahadasha can feel scattered or disruptive, and 8-Mukhi is traditionally chosen for obstacle-clearing support."
    if str(lagna.get("sign") or "") == "Aquarius":
        return "Aquarius rising often benefits from a steadier channel for unconventional or disruptive Rahu-like currents, making 8-Mukhi a useful support."
    return None


def _reason_for_ketu(chart: dict[str, Any]) -> str | None:
    lagna = chart.get("lagna") or {}
    if _current_mahadasha(chart) == "Ketu":
        return "Ketu Mahadasha can intensify detachment and inner churn, so 9-Mukhi is added for courage and spiritual steadiness."
    if str(lagna.get("sign") or "") == "Scorpio":
        return "Scorpio rising can carry intense transformational pressure, and 9-Mukhi is often chosen for protective resilience."
    return None


def _decorate_recommendation(mukhi: int, reason: str, score: int) -> dict[str, Any]:
    payload = dict(RUDRAKSHA_MUKHIS_BY_NUMBER[mukhi])
    instructions = dict(payload["wearing_instructions"])
    return {
        "mukhi": mukhi,
        "name": payload["name"],
        "slug": payload["slug"],
        "reason": reason,
        "score": score,
        "wearing_day": instructions["day"],
        "mantra": instructions["mantra"],
        "wearing_instructions": instructions,
    }


def _build_recommendations(chart: dict[str, Any]) -> dict[str, Any]:
    drishti_map = _graha_drishti_map(chart)
    ladder: dict[int, dict[str, Any]] = {}

    def add(mukhi: int, reason: str, score: int) -> None:
        existing = ladder.get(mukhi)
        if existing is None or score > existing["score"]:
            ladder[mukhi] = _decorate_recommendation(mukhi, reason, score)

    for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        if _current_mahadasha(chart) == planet or _is_planet_weak(chart, planet, drishti_map):
            base_reason = _reason_for_planet(chart, planet, drishti_map)
            mapped = PLANET_TO_RECOMMENDATIONS[planet]
            for index, mukhi in enumerate(mapped):
                add(mukhi, base_reason, 100 - (index * 5))

    rahu_reason = _reason_for_rahu(chart)
    if rahu_reason:
        add(8, rahu_reason, 92)

    ketu_reason = _reason_for_ketu(chart)
    if ketu_reason:
        add(9, ketu_reason, 91)

    lagna_lord_reason = _reason_for_lagna_lord(chart, drishti_map)
    if lagna_lord_reason:
        lagna_lord, reason = lagna_lord_reason
        add(PLANET_TO_PRIMARY_MUKHI[lagna_lord], reason, 95)

    weakest_dusthana_lord = _weakest_dusthana_lord(chart)
    if (
        weakest_dusthana_lord
        and weakest_dusthana_lord in PLANET_TO_PRIMARY_MUKHI
        and (
            _is_planet_weak(chart, weakest_dusthana_lord, drishti_map)
            or _is_shadbala_weak(chart, weakest_dusthana_lord)
        )
    ):
        add(
            PLANET_TO_PRIMARY_MUKHI[weakest_dusthana_lord],
            f"Among the 6th, 8th, and 12th house lords, {weakest_dusthana_lord} looks the most strained by shadbala, so its linked bead is added for protective support.",
            83,
        )

    if not ladder:
        add(5, "Your chart does not show a single overwhelming weakness here, so 5-Mukhi is recommended as a steady universal base.", 80)

    ranked = sorted(ladder.values(), key=lambda item: (-item["score"], item["mukhi"]))
    primary = dict(ranked[0])
    primary.pop("score", None)
    secondary = []
    for item in ranked[1:4]:
        payload = dict(item)
        payload.pop("score", None)
        secondary.append(payload)

    universal = {
        "mukhi": 5,
        "name": RUDRAKSHA_MUKHIS_BY_NUMBER[5]["name"],
        "slug": RUDRAKSHA_MUKHIS_BY_NUMBER[5]["slug"],
        "note": "5-Mukhi remains a steady baseline bead for most people and works well as a universal anchor.",
    }

    chart_signals = {
        "lagna": chart.get("lagna", {}).get("sign_vedic") or chart.get("lagna", {}).get("sign"),
        "moon_sign": chart.get("moon_sign", {}).get("sign_vedic") or chart.get("moon_sign", {}).get("sign"),
        "current_mahadasha": _current_mahadasha(chart),
        "atmakaraka": _atmakaraka(chart),
        "weakest_dusthana_lord": weakest_dusthana_lord,
    }

    return {
        "primary": primary,
        "secondary": secondary,
        "universal": universal,
        "wearing_day": primary["wearing_day"],
        "mantra": primary["mantra"],
        "chart_signals": chart_signals,
        "disclaimer": "This recommendation follows Vedic astrology principles and is offered for spiritual guidance only.",
    }


@router.get("/mukhis")
async def get_rudraksha_mukhis(request: Request) -> list[dict[str, Any]]:
    return await _load_all_mukhis(request)


@router.get("/mukhi/{mukhi}")
async def get_rudraksha_mukhi(mukhi: int, request: Request) -> dict[str, Any]:
    if mukhi < 1 or mukhi > 21:
        raise HTTPException(status_code=404, detail="Mukhi not found.")
    document = await _load_single_mukhi(request, mukhi)
    if not document:
        raise HTTPException(status_code=404, detail="Mukhi not found.")
    return document


@router.get("/planet/{planet_slug}")
async def get_rudraksha_planet_page(planet_slug: str, request: Request) -> dict[str, Any]:
    document = await _load_slug_document(
        request,
        "rudraksha_planets",
        planet_slug,
        get_planet_rudraksha_document,
    )
    if not document:
        raise HTTPException(status_code=404, detail="Planet page not found.")
    return document


@router.get("/problem/{problem_slug}")
async def get_rudraksha_problem_page(problem_slug: str, request: Request) -> dict[str, Any]:
    document = await _load_slug_document(
        request,
        "rudraksha_problems",
        problem_slug,
        get_problem_rudraksha_document,
    )
    if not document:
        raise HTTPException(status_code=404, detail="Problem page not found.")
    return document


@router.get("/sign/{sign_slug}")
async def get_rudraksha_sign_page(sign_slug: str, request: Request) -> dict[str, Any]:
    document = await _load_slug_document(
        request,
        "rudraksha_signs",
        sign_slug,
        get_sign_rudraksha_document,
    )
    if not document:
        raise HTTPException(status_code=404, detail="Sign page not found.")
    return document


@router.post("/calculator")
async def calculate_rudraksha(body: RudrakshaCalculatorRequest) -> dict[str, Any]:
    time_of_birth = str(body.time or "").strip() or "12:00"
    place_of_birth = str(body.place or "").strip()
    if not place_of_birth:
        raise HTTPException(status_code=422, detail="place is required.")

    try:
        chart = await asyncio.to_thread(
            calculate_vedic_chart,
            body.date,
            time_of_birth,
            place_of_birth,
            "+05:30",
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Unable to calculate Rudraksha recommendation: {exc}") from exc

    return _build_recommendations(chart)
