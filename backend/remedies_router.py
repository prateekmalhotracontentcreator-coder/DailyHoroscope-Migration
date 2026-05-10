from __future__ import annotations

from typing import Any
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/remedies", tags=["remedies"])


class RemedyReportRequest(BaseModel):
    focus_area: str
    date_of_birth: str
    time_of_birth: str = "12:00"
    place_of_birth: str = "New Delhi"
    timezone_offset: str = "+05:30"

REMEDY_TYPES: dict[str, str] = {
    "dana":      "jyotish_remedies_dhana",
    "gemstones": "jyotish_remedies_gemstones",
    "crystals":  "jyotish_remedies_crystals",
    "chakra":    "jyotish_remedies_chakra",
    "mantras":   "jyotish_remedies_mantras",
}

GEMSTONE_PLANET_META: list[dict] = [
    {"planet": "Sun",     "gemstone": "Ruby (Manik)",          "metal": "Gold",   "color": "#e11d48"},
    {"planet": "Moon",    "gemstone": "Pearl (Moti)",           "metal": "Silver", "color": "#94a3b8"},
    {"planet": "Mars",    "gemstone": "Red Coral (Moonga)",     "metal": "Gold",   "color": "#f97316"},
    {"planet": "Mercury", "gemstone": "Emerald (Panna)",        "metal": "Gold",   "color": "#22c55e"},
    {"planet": "Jupiter", "gemstone": "Yellow Sapphire (Pukhraj)","metal":"Gold",  "color": "#eab308"},
    {"planet": "Venus",   "gemstone": "Diamond (Heera)",        "metal": "Gold",   "color": "#e879f9"},
    {"planet": "Saturn",  "gemstone": "Blue Sapphire (Neelam)", "metal": "Silver", "color": "#6366f1"},
    {"planet": "Rahu",    "gemstone": "Hessonite (Gomed)",      "metal": "Silver", "color": "#a16207"},
    {"planet": "Ketu",    "gemstone": "Cat's Eye (Lahsuniya)",  "metal": "Gold",   "color": "#71717a"},
]

CHAKRA_META: list[dict] = [
    {"chakra": "Root (Muladhara)",       "color": "#ef4444", "bija": "LAM",  "planet": "Mars / Saturn"},
    {"chakra": "Sacral (Svadhisthana)",  "color": "#f97316", "bija": "VAM",  "planet": "Moon / Venus"},
    {"chakra": "Solar Plexus (Manipura)","color": "#eab308", "bija": "RAM",  "planet": "Sun / Mars"},
    {"chakra": "Heart (Anahata)",        "color": "#22c55e", "bija": "YAM",  "planet": "Venus / Moon"},
    {"chakra": "Throat (Vishuddha)",     "color": "#3b82f6", "bija": "HAM",  "planet": "Mercury / Jupiter"},
    {"chakra": "Third Eye (Ajna)",       "color": "#6366f1", "bija": "OM",   "planet": "Saturn / Moon"},
    {"chakra": "Crown (Sahasrara)",      "color": "#a855f7", "bija": "AUM",  "planet": "Jupiter / Ketu"},
]

DANA_TILE_ICONS: dict[str, str] = {
    "Vitality/Soul": "sun", "Wealth": "coins", "Marriage": "heart",
    "Children": "baby", "Health": "activity", "Career": "briefcase",
    "Property": "home", "Enemies": "shield", "Longevity": "clock",
    "Spirituality": "sparkles", "Education": "book", "Travel": "globe",
    "Luck": "star", "Mental Peace": "wind",
}


def _get_db(request: Request):
    return request.app.state.db


def _clean_rule(doc: dict) -> dict:
    doc.pop("_id", None)
    return doc


# ── Tiles ──────────────────────────────────────────────────────────────────────

@router.get("/{remedy_type}/tiles")
async def get_tiles(remedy_type: str, request: Request) -> dict[str, Any]:
    if remedy_type not in REMEDY_TYPES:
        raise HTTPException(status_code=404, detail=f"Unknown remedy type: {remedy_type}")

    if remedy_type == "gemstones":
        return {"type": remedy_type, "tiles": GEMSTONE_PLANET_META}

    if remedy_type == "chakra":
        return {"type": remedy_type, "tiles": CHAKRA_META}

    db = _get_db(request)
    science_id = REMEDY_TYPES[remedy_type]

    # Distinct remedy areas with counts
    pipeline = [
        {"$match": {"science_id": science_id}},
        {"$group": {
            "_id": "$remedy.remedy_area",
            "count": {"$sum": 1},
            "severity": {"$first": "$remedy.severity"},
            "yoga_group": {"$first": "$condition.yoga_group_label"},
        }},
        {"$sort": {"_id": 1}},
    ]
    areas = await db.interpretation_rules.aggregate(pipeline).to_list(None)
    tiles = [
        {
            "focus": a["_id"],
            "count": a["count"],
            "severity": a.get("severity", ""),
            "yoga_group": a.get("yoga_group", ""),
            "icon": DANA_TILE_ICONS.get(str(a["_id"]).split("/")[0].strip(), "gem"),
        }
        for a in areas if a["_id"]
    ]
    return {"type": remedy_type, "tiles": tiles}


# ── Query ──────────────────────────────────────────────────────────────────────

@router.get("/{remedy_type}/query")
async def query_remedies(
    remedy_type: str,
    focus: str,
    request: Request,
    limit: int = 20,
) -> dict[str, Any]:
    if remedy_type not in REMEDY_TYPES:
        raise HTTPException(status_code=404, detail=f"Unknown remedy type: {remedy_type}")

    db = _get_db(request)
    science_id = REMEDY_TYPES[remedy_type]

    if remedy_type == "gemstones":
        query = {
            "science_id": science_id,
            "condition.planets_involved": {"$in": [focus]},
        }
    elif remedy_type == "chakra":
        query = {
            "science_id": science_id,
            "remedy.chakra": {"$regex": focus.split("(")[0].strip(), "$options": "i"},
        }
    else:
        query = {
            "science_id": science_id,
            "remedy.remedy_area": {"$regex": focus, "$options": "i"},
        }

    docs = await db.interpretation_rules.find(query, {"_id": 0}).limit(limit).to_list(None)
    return {
        "type": remedy_type,
        "focus": focus,
        "count": len(docs),
        "rules": docs,
    }


# ── All rules (browse mode) ────────────────────────────────────────────────────

@router.get("/{remedy_type}/all")
async def get_all(remedy_type: str, request: Request, limit: int = 100) -> dict[str, Any]:
    if remedy_type not in REMEDY_TYPES:
        raise HTTPException(status_code=404, detail=f"Unknown remedy type: {remedy_type}")

    db = _get_db(request)
    science_id = REMEDY_TYPES[remedy_type]
    docs = await db.interpretation_rules.find(
        {"science_id": science_id}, {"_id": 0}
    ).limit(limit).to_list(None)
    return {"type": remedy_type, "count": len(docs), "rules": docs}


# ── Generate personalised remedy report ────────────────────────────────────────

@router.post("/{remedy_type}/generate-report")
async def generate_report(
    remedy_type: str,
    body: RemedyReportRequest,
    request: Request,
) -> dict[str, Any]:
    if remedy_type not in REMEDY_TYPES:
        raise HTTPException(status_code=404, detail=f"Unknown remedy type: {remedy_type}")

    try:
        from vedic_calculator import calculate_vedic_chart
        chart = calculate_vedic_chart(
            body.date_of_birth,
            body.time_of_birth,
            body.place_of_birth,
            body.timezone_offset,
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Chart computation failed: {str(e)}")

    db = _get_db(request)
    science_id = REMEDY_TYPES[remedy_type]

    if remedy_type == "gemstones":
        query = {
            "science_id": science_id,
            "condition.planets_involved": {"$in": [body.focus_area]},
        }
    elif remedy_type == "chakra":
        query = {
            "science_id": science_id,
            "remedy.chakra": {
                "$regex": body.focus_area.split("(")[0].strip(),
                "$options": "i",
            },
        }
    else:
        query = {
            "science_id": science_id,
            "remedy.remedy_area": {"$regex": body.focus_area, "$options": "i"},
        }

    rules = await db.interpretation_rules.find(query, {"_id": 0}).limit(20).to_list(None)

    planets_raw = chart.get("planets", {})
    chart_summary = [
        {
            "planet": name.split("(")[0].strip(),
            "sign": data.get("sign", ""),
            "house": data.get("house", 0),
            "degree": round(data.get("degree", 0.0), 1),
            "retrograde": data.get("retrograde", False),
            "dignity": data.get("dignity", ""),
        }
        for name, data in planets_raw.items()
    ]

    lagna_raw = chart.get("lagna", {})
    lagna_sign = lagna_raw.get("sign", "") if isinstance(lagna_raw, dict) else str(lagna_raw)

    return {
        "type": remedy_type,
        "focus": body.focus_area,
        "lagna": lagna_sign,
        "chart_summary": chart_summary,
        "rules": rules,
        "count": len(rules),
    }
