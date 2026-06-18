"""
Mundane Astrology Router -- /api/mundane/* endpoints.
All routes read from pre-seeded mundane_* collections in horoscope_db.
Foundation chart transits computed live via pyswisseph in mundane_engine.py.
"""
from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/mundane", tags=["mundane"])


async def _get_db() -> AsyncIOMotorDatabase:
    from server import db
    return db


# ── Foundation Charts ─────────────────────────────────────────────────────────

@router.get("/foundation-charts")
async def list_foundation_charts(db: AsyncIOMotorDatabase = Depends(_get_db)):
    """List all seeded country codes with their basic chart info."""
    cursor = db["mundane_foundation_charts"].find(
        {"active": True},
        {"_id": 0, "country_code": 1, "country_name": 1, "chart_type": 1, "event_date": 1, "chart.lagna_sign": 1},
        sort=[("country_name", 1)],
    )
    results = []
    async for doc in cursor:
        results.append({
            "country_code": doc["country_code"],
            "country_name": doc["country_name"],
            "chart_type": doc["chart_type"],
            "event_date": doc["event_date"],
            "lagna_sign": doc.get("chart", {}).get("lagna_sign"),
        })
    return {"count": len(results), "charts": results}


@router.get("/foundation-chart/{country_code}")
async def get_foundation_chart(
    country_code: str,
    db: AsyncIOMotorDatabase = Depends(_get_db),
):
    """Get a single country's foundation chart with all 9 planet positions."""
    doc = await db["mundane_foundation_charts"].find_one(
        {"country_code": country_code.upper(), "active": True},
        {"_id": 0},
    )
    if doc is None:
        raise HTTPException(status_code=404, detail=f"Foundation chart not found for {country_code.upper()}")
    return doc


# ── Eclipses & Lunations ──────────────────────────────────────────────────────

@router.get("/eclipses")
async def get_eclipses(
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    type: Optional[str] = Query(None, description="solar_eclipse | lunar_eclipse"),
    db: AsyncIOMotorDatabase = Depends(_get_db),
):
    """Query eclipse events. Optional filters: from, to (YYYY-MM-DD), type."""
    query: dict = {"active": True, "event_type": {"$in": ["solar_eclipse", "lunar_eclipse"]}}
    if type:
        query["event_type"] = type
    _apply_date_filter(query, "event_date_utc", from_date, to_date)

    cursor = db["mundane_eclipse_events"].find(query, {"_id": 0}, sort=[("event_date_utc", 1)])
    events = []
    async for doc in cursor:
        events.append(doc)
    return {"count": len(events), "events": events}


@router.get("/lunations")
async def get_lunations(
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    db: AsyncIOMotorDatabase = Depends(_get_db),
):
    """Query new moon / full moon events."""
    query: dict = {"active": True, "event_type": {"$in": ["new_moon", "full_moon"]}}
    _apply_date_filter(query, "event_date_utc", from_date, to_date)

    cursor = db["mundane_eclipse_events"].find(query, {"_id": 0}, sort=[("event_date_utc", 1)])
    events = []
    async for doc in cursor:
        events.append(doc)
    return {"count": len(events), "events": events}


# ── Planetary Ingresses ───────────────────────────────────────────────────────

@router.get("/ingress")
async def get_ingress(
    planet: Optional[str] = Query(None, description="Saturn | Jupiter | Rahu | Ketu | Mars | Sun"),
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    db: AsyncIOMotorDatabase = Depends(_get_db),
):
    """Query planetary ingress events."""
    query: dict = {"active": True}
    if planet:
        query["planet"] = planet.title()
    _apply_date_filter(query, "ingress_date_utc", from_date, to_date)

    cursor = db["mundane_ingress_events"].find(query, {"_id": 0}, sort=[("ingress_date_utc", 1)])
    events = []
    async for doc in cursor:
        events.append(doc)
    return {"count": len(events), "events": events}


# ── Foundation Chart Transits (Tool D) ───────────────────────────────────────

@router.get("/foundation-transit/{country_code}")
async def get_foundation_transit(
    country_code: str,
    date: Optional[str] = Query(None, description="YYYY-MM-DD (default: today)"),
    db: AsyncIOMotorDatabase = Depends(_get_db),
):
    """
    Compute current planetary transits over a country's foundation chart.
    Cross-referenced against V22 LUTs for interpretation.
    """
    from mundane_engine import get_foundation_chart_transits
    query_date = date or datetime.utcnow().strftime("%Y-%m-%d")
    try:
        result = await get_foundation_chart_transits(country_code.upper(), query_date, db)
    except Exception as exc:
        logger.exception("Foundation transit error for %s: %s", country_code, exc)
        raise HTTPException(status_code=500, detail=str(exc))
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# ── Helper ────────────────────────────────────────────────────────────────────

def _apply_date_filter(query: dict, field: str, from_date: Optional[str], to_date: Optional[str]) -> None:
    date_filter: dict = {}
    if from_date:
        date_filter["$gte"] = from_date
    if to_date:
        date_filter["$lte"] = to_date + "T23:59:59Z"
    if date_filter:
        query[field] = date_filter
