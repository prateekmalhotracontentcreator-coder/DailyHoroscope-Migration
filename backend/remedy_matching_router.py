from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict


router = APIRouter(prefix="/api/remedies", tags=["remedy-matching"])

DOSHA_SLUGS = [
    "shani-sade-sati",
    "manglik-dosha",
    "pitru-dosha",
    "kaal-sarp-dosha",
    "shani-mahadasha",
    "rahu-mahadasha",
    "ketu-mahadasha",
    "guru-chandal-yoga",
    "grahan-yoga",
    "nadi-dosha",
    "gana-dosha",
    "bhakoot-dosha",
]

SCIENCE_TYPE_MAP = {
    "jyotish_remedies_gemstones": "gemstone",
    "jyotish_remedies_mantras": "mantra",
    "jyotish_remedies_dhana": "donation",
    "jyotish_remedies_crystals": "crystal",
    "jyotish_remedies_chakra": "ritual",
    "jyotish_lk_remedies": "lk_ritual",
}

TYPE_ORDER = {
    "gemstone": 0,
    "mantra": 1,
    "donation": 2,
    "crystal": 3,
    "ritual": 4,
    "lk_ritual": 5,
}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RemedyMatchItem(StrictModel):
    rule_id: str
    remedy_type: str
    summary: str
    planet: str | None = None
    zodiac_signs: list[str]
    detailed: str


class RemedyMatchResponse(StrictModel):
    dosha: str
    remedies: list[RemedyMatchItem]


def _get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return db


def _flatten_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return " ".join(_flatten_text(item) for item in value if item).strip()
    if isinstance(value, dict):
        for key in ("detailed", "summary", "english_block", "sanskrit_block"):
            if value.get(key):
                return _flatten_text(value[key])
        return " ".join(_flatten_text(item) for item in value.values() if item).strip()
    return "" if value is None else str(value).strip()


def _extract_planet(doc: dict[str, Any]) -> str | None:
    primary = doc.get("primary_planet")
    if primary:
        return str(primary)
    planets = (((doc.get("condition") or {}).get("astrological_mapping") or {}).get("planet") or [])
    if isinstance(planets, list) and planets:
        return ", ".join(str(item) for item in planets[:3])
    return None


def _extract_summary(doc: dict[str, Any]) -> str:
    interpretation = doc.get("interpretation") or {}
    for candidate in (
        interpretation.get("summary"),
        doc.get("focus_area"),
        doc.get("title"),
        (((doc.get("condition") or {}).get("trigger_condition"))),
        doc.get("ke_inference"),
    ):
        text = _flatten_text(candidate)
        if text:
            return text
    return "Remedy guidance available for this affliction."


def _extract_detailed(doc: dict[str, Any]) -> str:
    interpretation = doc.get("interpretation") or {}
    for candidate in (
        interpretation.get("detailed"),
        doc.get("ke_inference"),
        doc.get("trigger_ke_inference"),
        doc.get("remedy"),
    ):
        text = _flatten_text(candidate)
        if text:
            return text
    return _extract_summary(doc)


def _normalize_remedy_type(doc: dict[str, Any]) -> str:
    raw = str(doc.get("remedy_type") or SCIENCE_TYPE_MAP.get(doc.get("science_id", ""), "ritual")).strip().lower()
    if raw == "chakra_ritual":
        return "ritual"
    return raw


def _priority_weight(doc: dict[str, Any]) -> float:
    try:
        return float(doc.get("priority_weight", 0))
    except Exception:
        return 0.0


def _sort_key(item: dict[str, Any]) -> tuple[int, float, str]:
    return (
        TYPE_ORDER.get(item["remedy_type"], 99),
        -_priority_weight(item["_raw"]),
        item["rule_id"],
    )


@router.get("/{dosha_slug}", response_model=RemedyMatchResponse)
async def get_remedies_by_dosha(dosha_slug: str, request: Request) -> RemedyMatchResponse:
    if dosha_slug not in DOSHA_SLUGS:
        raise HTTPException(status_code=404, detail="Dosha remedy page not found")

    db = _get_db(request)

    interpretation_docs = await db.interpretation_rules.find(
        {
            "science_id": {
                "$in": [
                    "jyotish_remedies_mantras",
                    "jyotish_remedies_gemstones",
                    "jyotish_remedies_crystals",
                    "jyotish_remedies_dhana",
                    "jyotish_remedies_chakra",
                ]
            },
            "affliction_tags": dosha_slug,
        },
        {"_id": 0},
    ).to_list(length=500)

    knowledge_docs = await db.knowledge_rules.find(
        {
            "science_id": "jyotish_lk_remedies",
            "affliction_tags": dosha_slug,
        },
        {"_id": 0},
    ).to_list(length=500)

    merged: list[dict[str, Any]] = []
    for doc in [*interpretation_docs, *knowledge_docs]:
        merged.append(
            {
                "rule_id": str(doc.get("rule_id") or doc.get("id") or "unknown-rule"),
                "remedy_type": _normalize_remedy_type(doc),
                "summary": _extract_summary(doc),
                "planet": _extract_planet(doc),
                "zodiac_signs": [str(item) for item in (doc.get("seo_zodiac_sign") or doc.get("zodiac_signs") or [])],
                "detailed": _extract_detailed(doc),
                "_raw": doc,
            }
        )

    merged.sort(key=_sort_key)

    return RemedyMatchResponse(
        dosha=dosha_slug,
        remedies=[
            RemedyMatchItem(
                rule_id=item["rule_id"],
                remedy_type=item["remedy_type"],
                summary=item["summary"],
                planet=item["planet"],
                zodiac_signs=item["zodiac_signs"],
                detailed=item["detailed"],
            )
            for item in merged
        ],
    )
