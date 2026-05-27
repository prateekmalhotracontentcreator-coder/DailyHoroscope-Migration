from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import re
import uuid

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from faith_bible_data import get_bible_page, get_bible_page_count, get_bible_topic_payload
from faith_gita_data import get_gita_chapter_payload, get_gita_page, get_gita_page_count
from faith_seo_data import (
    build_daily_pages,
    build_transit_pages,
    get_bible_hub_payload,
    get_daily_hub_payload,
    get_daily_page,
    get_daily_sign_payload,
    get_faith_hub_payload,
    get_gita_hub_payload,
    get_transit_hub_payload,
    get_transit_page,
)

router = APIRouter(prefix="/api/faith", tags=["faith"])
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class FaithSubscribeRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str = Field(min_length=5, max_length=160)
    track: str | None = Field(default=None, max_length=60)
    source_path: str | None = Field(default=None, max_length=200)
    tags: list[str] = Field(default_factory=list)


def _normalize_tag(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", str(value or "").strip().lower())
    return cleaned.strip("-")[:48]


def _collection(request: Request, name: str):
    db = getattr(getattr(request.app, "state", None), "db", None)
    if db is None:
        return None
    return getattr(db, name, None)


def _without_mongo(document: dict | None) -> dict | None:
    if document is None:
        return None
    cleaned = dict(document)
    cleaned.pop("_id", None)
    return cleaned


def _merge(base: dict, stored: dict | None) -> dict:
    merged = deepcopy(base)
    if stored:
        for key, value in stored.items():
            merged[key] = value
    return merged


@router.post("/subscribe")
async def subscribe_to_faith_updates(payload: FaithSubscribeRequest, request: Request) -> dict:
    collection = _collection(request, "subscribers")
    if collection is None:
        raise HTTPException(status_code=503, detail="Subscriber service unavailable.")

    email = payload.email.strip().lower()
    if not EMAIL_PATTERN.match(email):
        raise HTTPException(status_code=400, detail="Please enter a valid email address.")

    name = payload.name.strip()
    if len(name) < 2:
        raise HTTPException(status_code=400, detail="Please enter your name.")

    base_tags = ["faith", "faith-growth", "faith-devotional"]
    if payload.track:
        normalized_track = _normalize_tag(payload.track)
        if normalized_track:
            base_tags.append(f"track-{normalized_track}")
    if payload.source_path:
        normalized_source = _normalize_tag(payload.source_path)
        if normalized_source:
            base_tags.append(f"source-{normalized_source}")

    extra_tags = []
    for item in payload.tags:
        normalized = _normalize_tag(item)
        if normalized:
            extra_tags.append(normalized)
    merged_tags = sorted(set(base_tags + extra_tags))
    now = datetime.now(timezone.utc).isoformat()

    try:
        existing = await collection.find_one({"email": email})
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to save Faith signup right now.") from exc

    if existing:
        current_tags = existing.get("tags", []) if isinstance(existing, dict) else []
        next_tags = sorted(set(current_tags).union(merged_tags))
        update_doc = {
            "name": name,
            "tags": next_tags,
            "active": True,
            "updated_at": now,
        }
        await collection.update_one({"email": email}, {"$set": update_doc})
        return {
            "success": True,
            "status": "updated",
            "message": "Your Faith journey is already active. We refreshed your devotional track.",
        }

    document = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "phone": None,
        "tags": merged_tags,
        "active": True,
        "created_at": now,
    }
    await collection.insert_one(document)
    return {
        "success": True,
        "status": "created",
        "message": "You are on the Faith updates list. We will use this to shape devotional follow-ups.",
    }


@router.get("/hub")
async def get_faith_hub() -> dict:
    return get_faith_hub_payload()


@router.get("/gita/hub")
async def get_gita_hub() -> dict:
    return get_gita_hub_payload()


@router.get("/gita/chapter/{chapter}")
async def get_gita_chapter_hub(chapter: int) -> dict:
    payload = get_gita_chapter_payload(chapter)
    if payload is None:
        raise HTTPException(status_code=404, detail="Gita chapter hub not found.")
    return payload


@router.get("/bible/hub")
async def get_bible_hub() -> dict:
    return get_bible_hub_payload()


@router.get("/bible/topic/{topic_slug}")
async def get_bible_topic_hub(topic_slug: str) -> dict:
    payload = get_bible_topic_payload(topic_slug)
    if payload is None:
        raise HTTPException(status_code=404, detail="Bible topic hub not found.")
    return payload


@router.get("/transit/hub")
async def get_transit_hub() -> dict:
    return get_transit_hub_payload()


@router.get("/daily/hub")
async def get_daily_hub() -> dict:
    return get_daily_hub_payload()


@router.get("/daily/sign/{sign_slug}")
async def get_daily_sign_hub(sign_slug: str) -> dict:
    payload = get_daily_sign_payload(sign_slug)
    if payload is None:
        raise HTTPException(status_code=404, detail="Faith sign hub not found.")
    return payload


@router.get("/daily/{sign_slug}/{month_slug}")
async def get_faith_daily(sign_slug: str, month_slug: str, request: Request) -> dict:
    base = get_daily_page(sign_slug, month_slug)
    if base is None:
        raise HTTPException(status_code=404, detail="Faith daily page not found.")

    collection = _collection(request, "faith_daily_pages")
    if collection is None:
        return base

    try:
        stored = _without_mongo(await collection.find_one({"sign_slug": sign_slug, "month_slug": month_slug}))
    except Exception:
        stored = None
    return _merge(base, stored)


@router.get("/transit/{transit_slug}/{tradition}")
async def get_faith_transit(transit_slug: str, tradition: str, request: Request) -> dict:
    base = get_transit_page(transit_slug, tradition)
    if base is None:
        raise HTTPException(status_code=404, detail="Faith transit page not found.")

    collection = _collection(request, "faith_transit_pages")
    if collection is None:
        return base

    try:
        stored = _without_mongo(await collection.find_one({"transit_slug": transit_slug, "tradition": tradition}))
    except Exception:
        stored = None
    return _merge(base, stored)


@router.get("/gita/{chapter}/{verse}/{situation_slug}")
async def get_faith_gita(chapter: int, verse: int, situation_slug: str, request: Request) -> dict:
    base = get_gita_page(chapter, verse, situation_slug)
    if base is None:
        raise HTTPException(status_code=404, detail="Faith Gita page not found.")

    collection = _collection(request, "faith_gita_pages")
    if collection is None:
        return base

    try:
        stored = _without_mongo(
            await collection.find_one({"chapter": chapter, "verse": verse, "situation_slug": situation_slug})
        )
    except Exception:
        stored = None
    return _merge(base, stored)


@router.get("/bible/{topic_slug}/{transition_slug}")
async def get_faith_bible(topic_slug: str, transition_slug: str, request: Request) -> dict:
    base = get_bible_page(topic_slug, transition_slug)
    if base is None:
        raise HTTPException(status_code=404, detail="Faith Bible page not found.")

    collection = _collection(request, "faith_bible_pages")
    if collection is None:
        return base

    try:
        stored = _without_mongo(
            await collection.find_one({"topic_slug": topic_slug, "transition_slug": transition_slug})
        )
    except Exception:
        stored = None
    return _merge(base, stored)


@router.get("/meta/summary")
async def get_faith_summary() -> dict:
    transit_pages = build_transit_pages()
    daily_pages = build_daily_pages()
    return {
        "module": "faith-hubs",
        "phase_one_status": "live",
        "phase_two_status": "live",
        "phase_three_status": "live",
        "transit_pages": len(transit_pages),
        "daily_pages": len(daily_pages),
        "gita_pages": get_gita_page_count(),
        "bible_pages": get_bible_page_count(),
        "phase_total": len(transit_pages) + len(daily_pages) + get_gita_page_count() + get_bible_page_count(),
    }
