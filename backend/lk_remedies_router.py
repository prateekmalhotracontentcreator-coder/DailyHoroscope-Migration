from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any, Literal, Optional

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from lk_diagnostics import (
    run_full_diagnosis,
    run_conflict_check,
    run_debt_audit,
    LK_SCIENCE_ID,
)
from vedic_shared_utils import get_db, get_user_email

router = APIRouter(prefix="/api/lk", tags=["lk-remedies"])


class StrictModel(BaseModel):
    class Config:
        extra = "forbid"


# ── Onboarding ────────────────────────────────────────────────────────────────

class NatalChart(BaseModel):
    Sun: Optional[int] = None
    Moon: Optional[int] = None
    Mercury: Optional[int] = None
    Venus: Optional[int] = None
    Mars: Optional[int] = None
    Jupiter: Optional[int] = None
    Saturn: Optional[int] = None
    Rahu: Optional[int] = None
    Ketu: Optional[int] = None


class FamilyCensus(BaseModel):
    father: Literal["living", "deceased", "unknown"] = "unknown"
    mother: Literal["living", "deceased", "unknown"] = "unknown"
    brother: Literal["living", "deceased", "unknown"] = "unknown"
    sister: Literal["living", "deceased", "unknown"] = "unknown"
    grandfather_paternal: Literal["living", "deceased", "unknown"] = "unknown"
    grandfather_maternal: Literal["living", "deceased", "unknown"] = "unknown"


class OnboardRequest(BaseModel):
    age: int = Field(..., ge=0, le=121)
    natal_chart: NatalChart
    family_census: FamilyCensus
    location_slug: str = "new-delhi"


@router.post("/onboard")
async def onboard(body: OnboardRequest, request: Request):
    db = get_db(request)
    user_email = get_user_email(request)

    profile = {
        "user_id": user_email,
        "age": body.age,
        "natal_chart": body.natal_chart.model_dump(exclude_none=True),
        "family_census": body.family_census.model_dump(),
        "location_slug": body.location_slug,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    existing = await db.lk_user_profiles.find_one({"user_id": user_email})
    if not existing:
        profile["created_at"] = profile["updated_at"]

    await db.lk_user_profiles.update_one(
        {"user_id": user_email},
        {"$set": profile},
        upsert=True,
    )

    return {"ok": True, "profile": profile}


# ── Diagnose ──────────────────────────────────────────────────────────────────

class DiagnoseRequest(BaseModel):
    user_id: Optional[str] = None


@router.post("/diagnose")
async def diagnose(body: DiagnoseRequest, request: Request):
    db = get_db(request)
    user_email = get_user_email(request)
    uid = body.user_id or user_email

    profile = await db.lk_user_profiles.find_one({"user_id": uid}, {"_id": 0})
    if not profile:
        raise HTTPException(
            status_code=404,
            detail="LK profile not found. Complete onboarding first.",
        )

    result = await run_full_diagnosis(db, profile)
    await db.lk_diagnose_cache.update_one(
        {"user_id": uid},
        {"$set": {"result": result, "cached_at": datetime.now(timezone.utc).isoformat()}},
        upsert=True,
    )
    return result


# ── Conflict Check ────────────────────────────────────────────────────────────

VALID_ACTIONS = [
    "building_construction", "foreign_contract", "charity_event",
    "property_investment", "digital_launch", "marriage_ritual",
    "spiritual_retreat", "multiple_remedies",
]


class ConflictRequest(BaseModel):
    planned_action: str
    user_id: Optional[str] = None


@router.post("/conflict-check")
async def conflict_check(body: ConflictRequest, request: Request):
    db = get_db(request)
    get_user_email(request)

    if body.planned_action not in VALID_ACTIONS:
        raise HTTPException(
            status_code=400,
            detail=f"planned_action must be one of {VALID_ACTIONS}",
        )

    return await run_conflict_check(db, body.planned_action)


# ── Debt Audit ────────────────────────────────────────────────────────────────

class DebtAuditRequest(BaseModel):
    user_id: Optional[str] = None


@router.post("/debt-audit")
async def debt_audit(body: DebtAuditRequest, request: Request):
    db = get_db(request)
    user_email = get_user_email(request)
    uid = body.user_id or user_email

    profile = await db.lk_user_profiles.find_one({"user_id": uid}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="LK profile not found.")

    debts = await run_debt_audit(db, profile.get("family_census", {}))
    return {"user_id": uid, "debts": debts, "count": len(debts)}


# ── Tracker ───────────────────────────────────────────────────────────────────

class TrackerLogRequest(BaseModel):
    remedy_id: int
    completed: bool
    within_window: bool = True
    prohibited_avoided: bool = True


@router.get("/tracker/{user_id}")
async def get_tracker(user_id: str, request: Request):
    db = get_db(request)
    get_user_email(request)
    docs = await db.lk_tracker.find(
        {"user_id": user_id}, {"_id": 0}
    ).to_list(None)
    return {"user_id": user_id, "trackers": docs}


@router.post("/tracker/log")
async def log_tracker(body: TrackerLogRequest, request: Request):
    db = get_db(request)
    user_email = get_user_email(request)

    tracker = await db.lk_tracker.find_one(
        {"user_id": user_email, "remedy_id": body.remedy_id, "status": "active"},
        {"_id": 0},
    )

    now = datetime.now(timezone.utc)
    today_str = now.date().isoformat()

    if not tracker:
        tracker = {
            "user_id": user_email,
            "remedy_id": body.remedy_id,
            "science_id": LK_SCIENCE_ID,
            "start_date": now.isoformat(),
            "last_completed_date": None,
            "streak_days": 0,
            "status": "active",
            "day_log": [],
        }

    day_log = tracker.get("day_log", [])
    already_logged = any(e.get("date", "")[:10] == today_str for e in day_log)
    if already_logged:
        return {"ok": True, "message": "Already logged today", "tracker": tracker}

    completed_ok = (
        body.completed and body.within_window and body.prohibited_avoided
    )

    if not completed_ok:
        tracker["status"] = "broken"
        tracker["streak_days"] = 0
        tracker["last_completed_date"] = None
    else:
        tracker["streak_days"] = tracker.get("streak_days", 0) + 1
        tracker["last_completed_date"] = now.isoformat()
        if tracker["streak_days"] >= 43:
            tracker["status"] = "complete"

    day_log.append({
        "day": tracker.get("streak_days", 0),
        "date": now.isoformat(),
        "completed": body.completed,
        "within_window": body.within_window,
        "prohibited_avoided": body.prohibited_avoided,
    })
    tracker["day_log"] = day_log

    await db.lk_tracker.update_one(
        {"user_id": user_email, "remedy_id": body.remedy_id, "status": {"$in": ["active", "broken"]}},
        {"$set": tracker},
        upsert=True,
    )
    return {"ok": True, "tracker": tracker}


# ── Browse Remedies ───────────────────────────────────────────────────────────

@router.get("/remedies")
async def browse_remedies(
    request: Request,
    science_id: str = Query(LK_SCIENCE_ID),
    planet: Optional[str] = Query(None),
    house: Optional[int] = Query(None),
    severity: Optional[int] = Query(None),
    focus_area: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    db = get_db(request)

    q: dict[str, Any] = {"science_id": science_id}
    if planet:
        q["planet"] = planet
    if house is not None:
        q["house"] = house
    if severity is not None:
        q["severity"] = {"$gte": severity}
    if focus_area:
        q["focus_area"] = {"$regex": focus_area, "$options": "i"}

    total = await db.knowledge_rules.count_documents(q)
    docs = await db.knowledge_rules.find(q, {"_id": 0}).skip(skip).limit(limit).to_list(None)
    return {"total": total, "skip": skip, "limit": limit, "records": docs}
