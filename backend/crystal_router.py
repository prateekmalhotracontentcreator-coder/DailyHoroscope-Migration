from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from crystal_data import (
    INTENTION_BOOSTERS,
    PLANET_CRYSTAL_MAP,
    get_crystal_docs,
    get_crystal_list_payload,
    get_intention_docs,
)
from vedic_calculator import SIGN_LORDS, calculate_vedic_chart


router = APIRouter(tags=["crystals"])


class CrystalCalculatorRequest(BaseModel):
    date: str
    time: str = "12:00"
    place: str = "New Delhi"
    intention: str | None = Field(default="clarity-focus")


def _get_db(request: Request):
    return request.app.state.db


def _clean_doc(doc: dict | None) -> dict | None:
    if not doc:
        return None
    doc.pop("_id", None)
    return doc


def _merge_crystal_doc(local_doc: dict, db_doc: dict | None) -> dict:
    payload = {**local_doc}
    if db_doc:
        payload.update(db_doc)
    pair_slugs = payload.get("pairs_well_with") or []
    payload["pair_cards"] = [
        {
            "slug": slug,
            "display_name": get_crystal_docs()[slug]["display_name"],
            "tagline": get_crystal_docs()[slug]["tagline"],
            "color": get_crystal_docs()[slug]["color"],
        }
        for slug in pair_slugs
        if slug in get_crystal_docs()
    ]
    payload["intention_cards"] = [
        {
            "slug": slug,
            "display": get_intention_docs()[slug]["display"],
        }
        for slug in payload.get("best_intentions", [])
        if slug in get_intention_docs()
    ]
    return payload


def _merge_intention_doc(local_doc: dict, db_doc: dict | None) -> dict:
    payload = {**local_doc}
    if db_doc:
        payload.update(db_doc)
    payload["top_crystal_cards"] = [
        {
            "slug": slug,
            "display_name": get_crystal_docs()[slug]["display_name"],
            "tagline": get_crystal_docs()[slug]["tagline"],
            "color": get_crystal_docs()[slug]["color"],
            "chakras": get_crystal_docs()[slug]["chakras"],
        }
        for slug in payload.get("top_crystals", [])
        if slug in get_crystal_docs()
    ]
    return payload


def _normalize_planet(value: str | None) -> str:
    if not value:
        return ""
    return value.split("(")[0].strip()


def _build_primary_reason(primary_planet: str, current_dasha: dict, lagna_lord: str) -> str:
    if primary_planet and current_dasha.get("planet") == primary_planet:
        return f"{primary_planet} Mahadasha is active, so the primary Vedic gemstone focuses that planet's lessons and strengths."
    if primary_planet == lagna_lord:
        return f"{primary_planet} rules the lagna in this chart, making its gemstone a strong anchor for overall stability and alignment."
    return f"{primary_planet} is the clearest planetary focus in this chart right now, so its gemstone becomes the primary recommendation."


def _is_weak_planet(plain_name: str, payload: dict) -> bool:
    house = int(payload.get("house") or 0)
    dignity = str(payload.get("dignity") or "").lower()
    shadbala = payload.get("shadbala") or {}
    if dignity == "debilitated":
        return True
    if plain_name in {"Rahu", "Ketu"}:
        return house in {8, 12}
    return house in {6, 8, 12} and not bool(shadbala.get("is_strong"))


def _planet_secondary_reason(planet: str, payload: dict, crystal_name: str) -> str:
    house = payload.get("house")
    dignity = str(payload.get("dignity") or "").lower()
    if dignity == "debilitated":
        return f"{planet} is debilitated in this chart, so {crystal_name} is suggested as a gentler support stone."
    return f"{planet} sits in house {house}, so {crystal_name} is suggested to stabilize that planetary theme."


def _placement_tip(intention: str | None) -> str:
    if intention == "sleep":
        return "Wear or carry the primary gemstone during the day, then place your support crystals near the bed or under the pillow at night."
    if intention in {"career-success", "abundance-money", "clarity-focus"}:
        return "Wear the primary gemstone or keep it on the right side of your desk, and place support crystals near your workspace for daily reinforcement."
    return "Wear the primary gemstone if appropriate, and carry the support crystals in a pouch or place them where this intention shows up most in daily life."


async def _fetch_crystal_doc(request: Request, slug: str) -> dict | None:
    local_doc = get_crystal_docs().get(slug)
    if not local_doc:
        return None
    db_doc = _clean_doc(await _get_db(request).crystals.find_one({"slug": slug}, {"_id": 0}))
    return _merge_crystal_doc(local_doc, db_doc)


async def _fetch_intention_doc(request: Request, slug: str) -> dict | None:
    local_doc = get_intention_docs().get(slug)
    if not local_doc:
        return None
    db_doc = _clean_doc(await _get_db(request).crystal_intentions.find_one({"slug": slug}, {"_id": 0}))
    return _merge_intention_doc(local_doc, db_doc)


@router.get("/crystals/list")
async def get_crystal_list() -> dict:
    return get_crystal_list_payload()


@router.get("/crystals/intention/{slug}")
async def get_crystal_intention(slug: str, request: Request) -> dict:
    payload = await _fetch_intention_doc(request, slug)
    if not payload:
        raise HTTPException(status_code=404, detail="Crystal intention page not found.")
    return payload


@router.get("/crystals/{slug}")
async def get_crystal_detail(slug: str, request: Request) -> dict:
    payload = await _fetch_crystal_doc(request, slug)
    if not payload:
        raise HTTPException(status_code=404, detail="Crystal page not found.")
    return payload


@router.post("/crystals/calculator")
async def post_crystal_calculator(body: CrystalCalculatorRequest) -> dict:
    intention = body.intention or "clarity-focus"
    if intention not in get_intention_docs():
        raise HTTPException(status_code=400, detail="Unknown crystal intention.")

    try:
        chart = calculate_vedic_chart(
            date_of_birth=body.date,
            time_of_birth=body.time or "12:00",
            place_of_birth=body.place or "New Delhi",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to calculate crystal recommendations right now.") from exc

    current_dasha = chart.get("current_dasha") or {}
    lagna = chart.get("lagna") or {}
    moon_sign = chart.get("moon_sign") or {}
    lagna_lord = lagna.get("lord") or SIGN_LORDS.get(lagna.get("sign", ""), "")

    dasha_planet = _normalize_planet(current_dasha.get("planet"))
    primary_planet = dasha_planet if dasha_planet in PLANET_CRYSTAL_MAP else lagna_lord
    if primary_planet not in PLANET_CRYSTAL_MAP:
        primary_planet = "Jupiter"

    weak_planets: list[tuple[str, dict]] = []
    for planet_name, payload in (chart.get("planets") or {}).items():
        plain_name = _normalize_planet(planet_name)
        if plain_name not in PLANET_CRYSTAL_MAP or plain_name == primary_planet:
            continue
        if _is_weak_planet(plain_name, payload):
            weak_planets.append((plain_name, payload))

    primary_slug = PLANET_CRYSTAL_MAP[primary_planet]["primary_slug"]
    primary_doc = get_crystal_docs()[primary_slug]
    primary_reason = _build_primary_reason(primary_planet, current_dasha, lagna_lord)

    healing_recommendations = []
    used_slugs = {primary_slug}
    for planet, payload in weak_planets[:2]:
        for slug in PLANET_CRYSTAL_MAP[planet]["secondary_slugs"]:
            if slug in get_crystal_docs() and slug not in used_slugs:
                used_slugs.add(slug)
                healing_recommendations.append(
                    {
                        "crystal": get_crystal_docs()[slug]["display_name"],
                        "slug": slug,
                        "reason": _planet_secondary_reason(planet, payload, get_crystal_docs()[slug]["display_name"]),
                    }
                )
                break

    intention_boosters = []
    for slug in INTENTION_BOOSTERS.get(intention, [])[:2]:
        if slug in get_crystal_docs() and slug not in used_slugs:
            used_slugs.add(slug)
            intention_boosters.append(
                {
                    "crystal": get_crystal_docs()[slug]["display_name"],
                    "slug": slug,
                    "reason": f"{get_intention_docs()[intention]['display']} is one of the main themes you selected, so {get_crystal_docs()[slug]['display_name']} acts as a focused booster.",
                }
            )

    if not healing_recommendations:
        fallback_slug = PLANET_CRYSTAL_MAP[primary_planet]["secondary_slugs"][0]
        healing_recommendations.append(
            {
                "crystal": get_crystal_docs()[fallback_slug]["display_name"],
                "slug": fallback_slug,
                "reason": f"{get_crystal_docs()[fallback_slug]['display_name']} complements the main {primary_planet} recommendation with softer day-to-day support.",
            }
        )

    return {
        "primary_vedic": {
            "crystal": primary_doc["display_name"],
            "slug": primary_slug,
            "reason": primary_reason,
            "wearing": primary_doc.get("wearing", {}),
        },
        "healing_recommendations": healing_recommendations,
        "intention_boosters": intention_boosters,
        "placement_tip": _placement_tip(intention),
        "chart_context": {
            "lagna": lagna.get("sign_vedic", lagna.get("sign", "")),
            "moon_sign": moon_sign.get("sign_vedic", moon_sign.get("sign", "")),
            "current_dasha": current_dasha,
            "weak_planets": [planet for planet, _ in weak_planets],
            "generated_at": datetime.utcnow().isoformat() + "Z",
        },
        "source": "vedic_calculator.py",
    }
