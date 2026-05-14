from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from admin_utils import require_admin

router = APIRouter(prefix="/api/remedies", tags=["remedies"])


class RemedyReportRequest(BaseModel):
    focus_area: str
    date_of_birth: str
    time_of_birth: str = "12:00"
    place_of_birth: str = "New Delhi"
    timezone_offset: str = "+05:30"


class RemedySuggestRequest(BaseModel):
    trigger: str
    planet: str | None = None
    house: int | None = None
    affliction: str | None = None
    dasha_planet: str | None = None
    antardasha_planet: str | None = None
    life_domain: str | None = None
    nakshatra: str | None = None
    oracle_answer_id: str | None = None
    verdict: str | None = None
    gender: Literal["male", "female", "neutral"] | None = None
    intensity: Literal["mild", "moderate", "severe"] = "moderate"
    remedy_type_filter: Literal["ritual", "behavioral", "both"] = "both"


class RemedyStatusUpdateRequest(BaseModel):
    collection: Literal["interpretation_rules", "knowledge_rules", "krishna_prashnavali_remedies"]
    science_id: str
    record_id: str
    approval_status: Literal["approved", "pending_human_review", "flagged"]

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

INTERPRETATION_SCIENCE_META: dict[str, dict[str, str]] = {
    "jyotish_remedies_dhana": {
        "collection": "interpretation_rules",
        "tradition": "jyotish",
        "category": "dana",
        "action_type": "weekly",
    },
    "jyotish_remedies_gemstones": {
        "collection": "interpretation_rules",
        "tradition": "jyotish",
        "category": "gemstone",
        "action_type": "ongoing",
    },
    "jyotish_remedies_crystals": {
        "collection": "interpretation_rules",
        "tradition": "crystal",
        "category": "crystal",
        "action_type": "daily",
    },
    "jyotish_remedies_chakra": {
        "collection": "interpretation_rules",
        "tradition": "chakra",
        "category": "breathwork",
        "action_type": "daily",
    },
    "jyotish_remedies_mantras": {
        "collection": "interpretation_rules",
        "tradition": "jyotish",
        "category": "mantra",
        "action_type": "daily",
    },
}

COLLECTION_SUMMARY_META: list[dict[str, str]] = [
    *(
        {
            "collection": meta["collection"],
            "science_id": science_id,
            "tradition": meta["tradition"],
        }
        for science_id, meta in INTERPRETATION_SCIENCE_META.items()
    ),
    {
        "collection": "knowledge_rules",
        "science_id": "jyotish_lk_remedies",
        "tradition": "lal_kitab",
    },
    {
        "collection": "krishna_prashnavali_remedies",
        "science_id": "krishna_prashnavali_remedies",
        "tradition": "krishna_bhakti",
    },
]

REMEDY_CONFIDENCE = {
    "LOW": 0.35,
    "MEDIUM": 0.6,
    "HIGH": 0.82,
}

DIGNITY_SCORE = {
    "debilitated": 0,
    "enemy": 1,
    "neutral": 2,
    "friendly": 3,
    "own_sign": 4,
    "moolatrikona": 5,
    "exalted": 6,
}


def _get_db(request: Request):
    return request.app.state.db


def _clean_rule(doc: dict) -> dict:
    doc.pop("_id", None)
    return doc


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _confidence_to_float(value: Any) -> float:
    if isinstance(value, (int, float)):
        try:
            return round(float(value), 2)
        except Exception:
            return 0.5
    return REMEDY_CONFIDENCE.get(str(value or "").upper(), 0.5)


def _normalize_planet_name(value: str | None) -> str:
    if not value:
        return ""
    return value.split("(")[0].strip()


def _flatten_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("english_block", "sanskrit_block"):
            payload = value.get(key)
            if payload:
                return str(payload).strip()
        return " ".join(str(v).strip() for v in value.values() if v)
    if isinstance(value, list):
        return " ".join(_flatten_text(item) for item in value if item)
    return "" if value is None else str(value).strip()


def _text_blob(doc: dict) -> str:
    parts: list[str] = []
    for key in ("rule_id", "science_id", "approval_status", "focus_area", "primary_planet"):
        if doc.get(key):
            parts.append(str(doc[key]))
    for bucket in ("condition", "interpretation", "remedy", "metadata", "title", "ritual_remedy", "behavioral_display_hint", "mantra"):
        payload = doc.get(bucket)
        text = _flatten_text(payload)
        if text:
            parts.append(text)
    tags = doc.get("tags") or doc.get("metadata", {}).get("tags")
    if tags:
        parts.extend(str(tag) for tag in tags)
    return " | ".join(parts).lower()


def _action_type_from_duration(value: Any) -> str:
    if isinstance(value, int):
        if value <= 1:
            return "one_time"
        if value <= 7:
            return "weekly"
        return "ongoing"
    text = str(value or "").strip().lower()
    if not text:
        return "ongoing"
    if "one" in text or "once" in text:
        return "one_time"
    if "week" in text or "saturday" in text:
        return "weekly"
    if "daily" in text or "day" in text:
        return "daily"
    return "ongoing"


def _ease_from_action_type(action_type: str) -> str:
    if action_type in {"one_time", "behavioral"}:
        return "easy"
    if action_type == "weekly":
        return "medium"
    return "advanced" if action_type == "ongoing" else "medium"


def _build_context_summary(body: RemedySuggestRequest) -> str:
    parts = [body.trigger.replace("_", " ").title()]
    if body.planet:
        parts.append(body.planet)
    if body.dasha_planet:
        parts.append(f"Dasha {body.dasha_planet}")
    if body.house:
        parts.append(f"House {body.house}")
    if body.affliction:
        parts.append(body.affliction.replace("_", " "))
    if body.life_domain:
        parts.append(body.life_domain.replace("_", " "))
    return " — ".join(parts)


def _science_alias_to_query(collection_name: str | None) -> tuple[str, str | None]:
    alias = str(collection_name or "").strip().lower()
    if alias in {"", "all"}:
        return "", None
    if alias in REMEDY_TYPES:
        return "interpretation_rules", REMEDY_TYPES[alias]
    if alias in {"lk", "knowledge_rules"}:
        return "knowledge_rules", "jyotish_lk_remedies"
    if alias in {"kp", "krishna_prashnavali_remedies"}:
        return "krishna_prashnavali_remedies", "krishna_prashnavali_remedies"
    if alias == "interpretation_rules":
        return "interpretation_rules", None
    raise HTTPException(status_code=404, detail=f"Unknown collection alias: {collection_name}")


def _normalize_interpretation_rule(doc: dict) -> dict:
    science_id = str(doc.get("science_id", ""))
    meta = INTERPRETATION_SCIENCE_META.get(science_id, {})
    remedy = doc.get("remedy", {})
    interpretation = doc.get("interpretation", {})
    duration = (
        remedy.get("frequency")
        or remedy.get("recharge_freq")
        or remedy.get("activation", {}).get("day")
        or remedy.get("start_day")
        or ""
    )
    description = (
        _flatten_text(remedy.get("guidance"))
        or _flatten_text(interpretation.get("detailed"))
        or _flatten_text(remedy.get("trigger_ke_inference"))
        or _flatten_text(remedy.get("trigger_birth_chart"))
    )
    title = (
        _flatten_text(interpretation.get("summary"))
        or _flatten_text(remedy.get("remedy_area"))
        or _flatten_text(doc.get("rule_id"))
    )
    action_type = meta.get("action_type") or _action_type_from_duration(duration)
    return {
        "remedy_id": doc.get("rule_id") or f"{science_id}-{remedy.get('id', '')}",
        "tradition": meta.get("tradition", "jyotish"),
        "category": meta.get("category", "ritual"),
        "action_type": action_type,
        "remedy_type": "ritual",
        "title": title,
        "description": description,
        "duration": str(duration or "As guided"),
        "ease": _ease_from_action_type(action_type),
        "confidence": _confidence_to_float(doc.get("confidence")),
        "source_collection": "interpretation_rules",
        "science_id": science_id,
        "raw": doc,
    }


def _normalize_lk_rule(doc: dict) -> dict:
    duration = doc.get("frequency_days") or ""
    action_type = _action_type_from_duration(duration)
    title = _flatten_text(doc.get("focus_area")) or f"LK Remedy {doc.get('id')}"
    description_parts = [
        _flatten_text(doc.get("ritual_act")),
        _flatten_text(doc.get("ke_inference")),
    ]
    prohibited = _flatten_text(doc.get("prohibited_act"))
    if prohibited:
        description_parts.append(f"Avoid: {prohibited}")
    return {
        "remedy_id": f"lk-{doc.get('id')}",
        "tradition": "lal_kitab",
        "category": "ritual",
        "action_type": action_type,
        "remedy_type": "ritual",
        "title": title,
        "description": " ".join(part for part in description_parts if part),
        "duration": f"{duration} days" if isinstance(duration, int) and duration > 0 else str(duration or "As guided"),
        "ease": _ease_from_action_type(action_type),
        "confidence": max(0.45, min(0.95, float(doc.get("severity_scale", 3)) / 5)),
        "source_collection": "knowledge_rules",
        "science_id": "jyotish_lk_remedies",
        "raw": doc,
    }


def _normalize_kp_rule(doc: dict, remedy_type_filter: str = "both") -> list[dict]:
    results: list[dict] = []
    if remedy_type_filter in {"both", "ritual"}:
        results.append({
            "remedy_id": doc.get("remedy_id"),
            "tradition": "krishna_bhakti",
            "category": "mantra",
            "action_type": "one_time",
            "remedy_type": "ritual",
            "title": _flatten_text(doc.get("title")),
            "description": " ".join(
                part for part in [
                    _flatten_text(doc.get("ritual_remedy")),
                    _flatten_text(doc.get("mantra")),
                ] if part
            ),
            "duration": "Before acting",
            "ease": "easy",
            "confidence": 0.95,
            "source_collection": "krishna_prashnavali_remedies",
            "science_id": "krishna_prashnavali_remedies",
            "behavioral_remedy": _flatten_text(doc.get("behavioral_display_hint")),
            "raw": doc,
        })
    if remedy_type_filter in {"both", "behavioral"}:
        results.append({
            "remedy_id": f"{doc.get('remedy_id')}-behavioral",
            "tradition": "krishna_bhakti",
            "category": "behavioral",
            "action_type": "behavioral",
            "remedy_type": "behavioral",
            "title": _flatten_text(doc.get("title")),
            "description": _flatten_text(doc.get("behavioral_display_hint")),
            "duration": "Reflect before acting",
            "ease": "easy",
            "confidence": 0.9,
            "source_collection": "krishna_prashnavali_remedies",
            "science_id": "krishna_prashnavali_remedies",
            "raw": doc,
        })
    return results


def _document_score(doc: dict, body: RemedySuggestRequest) -> float:
    score = 0.0
    blob = _text_blob(doc)

    if body.planet:
        planet = body.planet.lower()
        if planet in blob:
            score += 3.0
        planets = doc.get("condition", {}).get("planets_involved") or doc.get("condition", {}).get("astrological_mapping", {}).get("planet") or []
        primary_planet = doc.get("primary_planet")
        if isinstance(primary_planet, str) and planet in primary_planet.lower():
            score += 2.5
        if any(planet == str(item).lower() for item in planets):
            score += 2.0

    if body.house:
        if body.house in (doc.get("condition", {}).get("houses_involved") or []):
            score += 1.5
        if doc.get("house") == body.house:
            score += 1.5
        if f"house {body.house}" in blob or f"h{body.house}" in blob:
            score += 0.75

    if body.affliction and body.affliction.lower() in blob:
        score += 1.0
    if body.dasha_planet and body.dasha_planet.lower() in blob:
        score += 1.0
    if body.antardasha_planet and body.antardasha_planet.lower() in blob:
        score += 0.75
    if body.life_domain and body.life_domain.lower() in blob:
        score += 1.0
    if body.nakshatra and body.nakshatra.lower() in blob:
        score += 0.5
    if body.verdict and body.verdict.lower() in blob:
        score += 0.75
    if body.oracle_answer_id and body.oracle_answer_id.lower() in blob:
        score += 3.0

    if body.intensity == "severe":
        severity = doc.get("severity_scale") or doc.get("remedy", {}).get("severity")
        if isinstance(severity, int) and severity >= 4:
            score += 1.0
        elif isinstance(severity, str) and severity.lower() in {"high", "very high"}:
            score += 1.0
    elif body.intensity == "mild":
        severity = doc.get("severity_scale") or doc.get("remedy", {}).get("severity")
        if isinstance(severity, int) and severity <= 2:
            score += 0.75
        elif isinstance(severity, str) and severity.lower() in {"low", "gentle"}:
            score += 0.75

    score += _confidence_to_float(doc.get("confidence"))
    return score


def _advisory_mode(body: RemedySuggestRequest) -> str:
    verdict = (body.verdict or "").upper()
    if verdict in {"NO", "WARNING"}:
        return "protective"
    if verdict in {"WAIT", "PATIENCE"} or body.intensity == "moderate":
        return "calming"
    if verdict in {"PRAY", "SURRENDER"} or body.trigger == "krishna_oracle":
        return "devotional"
    return "supportive"


async def _query_interpretation_docs(db, body: RemedySuggestRequest) -> list[dict]:
    results: list[dict] = []
    for science_id in INTERPRETATION_SCIENCE_META:
        query: dict[str, Any] = {
            "science_id": science_id,
            "approval_status": "approved",
        }
        filters: list[dict[str, Any]] = []
        if body.planet:
            filters.append({
                "$or": [
                    {"condition.planets_involved": body.planet},
                    {"condition.astrological_mapping.planet": body.planet},
                    {"remedy.trigger_birth_chart": {"$regex": body.planet, "$options": "i"}},
                ]
            })
        if body.house:
            filters.append({
                "$or": [
                    {"condition.houses_involved": body.house},
                    {"condition.astrological_mapping.house": body.house},
                    {"remedy.trigger_birth_chart": {"$regex": f"house {body.house}", "$options": "i"}},
                ]
            })
        if body.life_domain:
            filters.append({
                "$or": [
                    {"remedy.remedy_area": {"$regex": body.life_domain, "$options": "i"}},
                    {"metadata.tags": {"$regex": body.life_domain, "$options": "i"}},
                    {"interpretation.summary": {"$regex": body.life_domain, "$options": "i"}},
                ]
            })
        if filters:
            query["$and"] = filters

        docs = await db.interpretation_rules.find(query, {"_id": 0}).limit(20).to_list(None)
        results.extend(docs)
    return results


async def _query_lk_docs(db, body: RemedySuggestRequest) -> list[dict]:
    query: dict[str, Any] = {
        "science_id": "jyotish_lk_remedies",
        "approval_status": "approved",
    }
    filters: list[dict[str, Any]] = []
    if body.planet:
        filters.append({"primary_planet": {"$regex": body.planet, "$options": "i"}})
    if body.house:
        filters.append({"house": body.house})
    if body.life_domain:
        filters.append({"focus_area": {"$regex": body.life_domain, "$options": "i"}})
    if body.intensity == "severe":
        filters.append({"severity_scale": {"$gte": 4}})
    elif body.intensity == "mild":
        filters.append({"severity_scale": {"$lte": 2}})
    if filters:
        query["$and"] = filters
    return await db.knowledge_rules.find(query, {"_id": 0}).limit(25).to_list(None)


async def _query_kp_docs(db, body: RemedySuggestRequest) -> list[dict]:
    query: dict[str, Any] = {
        "science_id": "krishna_prashnavali_remedies",
        "approval_status": "approved",
    }
    if body.oracle_answer_id:
        query["answer_id"] = body.oracle_answer_id
    elif body.verdict:
        query["verdict_display"] = body.verdict.replace("SUCCESS", "YES").replace("WARNING", "NO").replace("PATIENCE", "WAIT").replace("SURRENDER", "PRAY")
    elif body.life_domain:
        query["tags"] = {"$regex": body.life_domain, "$options": "i"}
    else:
        return []
    return await db.krishna_prashnavali_remedies.find(query, {"_id": 0}).limit(10).to_list(None)


def _normalize_doc(doc: dict, remedy_type_filter: str) -> list[dict]:
    science_id = str(doc.get("science_id", ""))
    if science_id in INTERPRETATION_SCIENCE_META:
        normalized = _normalize_interpretation_rule(doc)
        return [normalized] if remedy_type_filter in {"both", normalized["remedy_type"]} else []
    if science_id == "jyotish_lk_remedies":
        normalized = _normalize_lk_rule(doc)
        return [normalized] if remedy_type_filter in {"both", normalized["remedy_type"]} else []
    if science_id == "krishna_prashnavali_remedies":
        return _normalize_kp_rule(doc, remedy_type_filter)
    return []


def _fallback_universal_planet(entries: list[dict], body: RemedySuggestRequest) -> list[dict]:
    if not body.planet:
        return entries
    planet = body.planet.lower()
    ranked = [
        entry for entry in entries
        if planet in _text_blob(entry.get("raw", {}))
    ]
    return ranked or entries


def _rank_entries(entries: list[dict]) -> list[dict]:
    entries.sort(key=lambda item: item.get("_score", 0.0), reverse=True)
    selected: list[dict] = []
    counts: dict[str, int] = {}
    seen_ids: set[str] = set()
    for entry in entries:
        remedy_id = str(entry.get("remedy_id"))
        if remedy_id in seen_ids:
            continue
        tradition = str(entry.get("tradition", "unknown"))
        if counts.get(tradition, 0) >= 2:
            continue
        counts[tradition] = counts.get(tradition, 0) + 1
        seen_ids.add(remedy_id)
        entry.pop("_score", None)
        entry.pop("raw", None)
        selected.append(entry)
        if len(selected) >= 7:
            break
    return selected


async def _resolve_remedy_doc(db, remedy_id: str, collection: str = "", science_id: str | None = None) -> tuple[str, dict | None]:
    candidates: list[tuple[str, Any, dict[str, Any]]] = []
    if collection in {"", "interpretation_rules"}:
        query: dict[str, Any] = {"rule_id": remedy_id}
        if science_id:
            query["science_id"] = science_id
        candidates.append(("interpretation_rules", db.interpretation_rules, query))
    if collection in {"", "knowledge_rules"}:
        numeric_part = remedy_id.removeprefix("lk-")
        lk_query: dict[str, Any] = {"science_id": "jyotish_lk_remedies"}
        if science_id:
            lk_query["science_id"] = science_id
        if numeric_part.isdigit():
            lk_query["id"] = int(numeric_part)
        else:
            lk_query["id"] = remedy_id
        candidates.append(("knowledge_rules", db.knowledge_rules, lk_query))
    if collection in {"", "krishna_prashnavali_remedies"}:
        kp_query: dict[str, Any] = {"$or": [{"remedy_id": remedy_id}, {"answer_id": remedy_id}]}
        if science_id:
            kp_query["science_id"] = science_id
        candidates.append(("krishna_prashnavali_remedies", db.krishna_prashnavali_remedies, kp_query))

    for collection_name, coll, query in candidates:
        doc = await coll.find_one(query, {"_id": 0})
        if doc:
            return collection_name, doc
    return "", None


def _status_sort_value(status: str) -> tuple[int, str]:
    order = {
        "flagged": 0,
        "pending_human_review": 1,
        "pending_review": 2,
        "approved": 3,
    }
    return (order.get(status, 9), status)


def _admin_record_from_doc(collection_name: str, doc: dict) -> dict[str, Any]:
    science_id = str(doc.get("science_id", ""))
    approval_status = str(doc.get("approval_status", "unknown"))
    if collection_name == "interpretation_rules":
        normalized = _normalize_interpretation_rule(doc)
        record_id = str(doc.get("rule_id", ""))
    elif collection_name == "knowledge_rules":
        normalized = _normalize_lk_rule(doc)
        record_id = f"lk-{doc.get('id')}"
    else:
        record_id = str(doc.get("remedy_id", ""))
        normalized = {
            "tradition": "krishna_bhakti",
            "category": "behavioral" if _flatten_text(doc.get("behavioral_display_hint")) else "mantra",
            "action_type": "behavioral" if _flatten_text(doc.get("behavioral_display_hint")) else "one_time",
            "title": _flatten_text(doc.get("title")),
            "description": _flatten_text(doc.get("behavioral_display_hint")) or _flatten_text(doc.get("ritual_remedy")),
        }

    updated_at = doc.get("updated_at") or doc.get("created_at") or ""
    return {
        "source_collection": collection_name,
        "science_id": science_id,
        "record_id": record_id,
        "tradition": normalized.get("tradition", "unknown"),
        "category": normalized.get("category", "ritual"),
        "action_type": normalized.get("action_type", "ongoing"),
        "approval_status": approval_status,
        "title": normalized.get("title", ""),
        "description": normalized.get("description", ""),
        "updated_at": updated_at,
        "search_blob": (
            f"{record_id} {science_id} {normalized.get('title', '')} "
            f"{normalized.get('description', '')} {_flatten_text(doc.get('title'))}"
        ).lower(),
        "document": doc,
    }


async def _load_admin_remedy_records(db) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    interpretation_docs = await db.interpretation_rules.find(
        {"science_id": {"$in": list(INTERPRETATION_SCIENCE_META.keys())}},
        {"_id": 0},
    ).to_list(None)
    records.extend(_admin_record_from_doc("interpretation_rules", doc) for doc in interpretation_docs)

    lk_docs = await db.knowledge_rules.find(
        {"science_id": "jyotish_lk_remedies"},
        {"_id": 0},
    ).to_list(None)
    records.extend(_admin_record_from_doc("knowledge_rules", doc) for doc in lk_docs)

    kp_docs = await db.krishna_prashnavali_remedies.find(
        {"science_id": "krishna_prashnavali_remedies"},
        {"_id": 0},
    ).to_list(None)
    records.extend(_admin_record_from_doc("krishna_prashnavali_remedies", doc) for doc in kp_docs)

    records.sort(
        key=lambda item: (
            _status_sort_value(item.get("approval_status", "unknown")),
            str(item.get("updated_at") or ""),
            item.get("record_id", ""),
        )
    )
    return records


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


@router.post("/suggest")
async def suggest_remedies(body: RemedySuggestRequest, request: Request) -> dict[str, Any]:
    db = _get_db(request)

    interpretation_docs, lk_docs, kp_docs = await asyncio.gather(
        _query_interpretation_docs(db, body),
        _query_lk_docs(db, body),
        _query_kp_docs(db, body),
    )

    normalized: list[dict] = []
    for doc in [*interpretation_docs, *lk_docs, *kp_docs]:
        score = _document_score(doc, body)
        for item in _normalize_doc(doc, body.remedy_type_filter):
            item["_score"] = score + item.get("confidence", 0.0)
            normalized.append(item)

    if len(normalized) < 3:
        normalized = _fallback_universal_planet(normalized, body)

    remedies = _rank_entries(normalized)
    return {
        "remedy_pack_id": str(uuid4()),
        "trigger": body.trigger,
        "context_summary": _build_context_summary(body),
        "remedies": remedies,
        "advisory_mode": _advisory_mode(body),
        "generated_at": _utcnow_iso(),
    }


@router.get("/rule/{remedy_id}")
async def get_remedy_rule(
    remedy_id: str,
    request: Request,
    collection: str = Query(default="all"),
) -> dict[str, Any]:
    db = _get_db(request)
    collection_name, science_id = _science_alias_to_query(collection)
    resolved_collection, doc = await _resolve_remedy_doc(db, remedy_id, collection_name, science_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Remedy not found: {remedy_id}")
    normalized = _normalize_doc(doc, "both")
    return {
        "collection": resolved_collection,
        "document": doc,
        "resolved": normalized,
    }


@router.get("/traditions")
async def get_remedy_traditions(request: Request) -> dict[str, Any]:
    db = _get_db(request)
    traditions: list[dict[str, Any]] = []
    for item in COLLECTION_SUMMARY_META:
        collection = getattr(db, item["collection"])
        total = await collection.count_documents({"science_id": item["science_id"]})
        approved = await collection.count_documents({"science_id": item["science_id"], "approval_status": "approved"})
        traditions.append({
            "tradition": item["tradition"],
            "collection": item["collection"],
            "science_id": item["science_id"],
            "total_records": total,
            "approved_records": approved,
        })
    return {
        "generated_at": _utcnow_iso(),
        "traditions": traditions,
    }


@router.get("/admin/records")
async def get_admin_remedy_records(request: Request) -> dict[str, Any]:
    db = _get_db(request)
    await require_admin(request, db)
    records = await _load_admin_remedy_records(db)
    return {
        "generated_at": _utcnow_iso(),
        "total": len(records),
        "records": records,
    }


@router.post("/admin/status")
async def update_admin_remedy_status(
    body: RemedyStatusUpdateRequest,
    request: Request,
) -> dict[str, Any]:
    db = _get_db(request)
    await require_admin(request, db)

    if body.collection == "interpretation_rules":
        query = {"rule_id": body.record_id, "science_id": body.science_id}
        collection = db.interpretation_rules
    elif body.collection == "knowledge_rules":
        numeric_part = body.record_id.removeprefix("lk-")
        query = {
            "science_id": body.science_id,
            "id": int(numeric_part) if numeric_part.isdigit() else body.record_id,
        }
        collection = db.knowledge_rules
    else:
        query = {"remedy_id": body.record_id, "science_id": body.science_id}
        collection = db.krishna_prashnavali_remedies

    update_result = await collection.update_one(
        query,
        {"$set": {"approval_status": body.approval_status, "updated_at": _utcnow_iso()}},
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Remedy record not found")

    updated = await collection.find_one(query, {"_id": 0})
    return {
        "ok": True,
        "record": _admin_record_from_doc(body.collection, updated),
    }


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
