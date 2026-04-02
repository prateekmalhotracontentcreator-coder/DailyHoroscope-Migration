from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any, Literal
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    build_natal_snapshot,
    compute_ritual_check,
    get_db,
    get_engine_log_collection,
    get_engine_subscription_collection,
    get_user_email,
    now_utc,
)


router = APIRouter(prefix="/api/ritual-engine", tags=["ritual-engine"])

DEFAULT_TRIGGERS = [
    "first_date_magnet",
    "steamy_encounter",
    "ex_recovery",
    "long_term_love",
    "lunar_daily_score",
]

TriggerType = Literal[
    "first_date_magnet",
    "steamy_encounter",
    "ex_recovery",
    "long_term_love",
    "lunar_daily_score",
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NatalData(StrictModel):
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city_name: str | None = None


class EnrollRequest(StrictModel):
    user_email: str
    natal_data: NatalData
    triggers_opted_in: list[TriggerType] = Field(default_factory=lambda: list(DEFAULT_TRIGGERS))


class CheckRequest(StrictModel):
    user_email: str
    check_date: str | None = None


class UnenrollRequest(StrictModel):
    user_email: str


class EnrollResponse(StrictModel):
    ok: bool = True
    user_email: str
    subscribed: bool
    triggers_opted_in: list[TriggerType]
    updated_at: datetime


class TriggerLogEntry(StrictModel):
    id: str
    user_email: str
    trigger_type: str
    check_date: str
    intensity: str | None = None
    orb_degrees: float | None = None
    alignment_description: str
    ritual_suggestion: str | None = None
    notification_worthy: bool
    active_from: str | None = None
    active_until: str | None = None
    fired_at: datetime
    love_battery_percent: int | None = None
    score_category: str | None = None
    moon_natal_venus_angle: float | None = None
    action_note: str | None = None


class LoveBatteryCard(StrictModel):
    trigger_type: Literal["lunar_daily_score"] = "lunar_daily_score"
    check_date: str
    love_battery_percent: int
    score_category: str
    moon_natal_venus_angle: float
    alignment_description: str
    action_note: str
    notification_worthy: bool


class RitualCheckResponse(StrictModel):
    user_email: str
    check_date: str
    love_battery: LoveBatteryCard
    active_triggers: list[TriggerLogEntry] = Field(default_factory=list)
    notification_worthy_triggers: list[str] = Field(default_factory=list)
    coach_summary: str
    next_upcoming_trigger: dict[str, Any] | None = None


class RitualDashboardResponse(StrictModel):
    love_battery: LoveBatteryCard
    active_triggers: list[TriggerLogEntry] = Field(default_factory=list)
    next_upcoming_trigger: dict[str, Any] | None = None
    recent_history: list[TriggerLogEntry] = Field(default_factory=list)


class RitualHistoryResponse(StrictModel):
    items: list[TriggerLogEntry] = Field(default_factory=list)


class UnenrollResponse(StrictModel):
    ok: bool = True
    user_email: str
    subscribed: bool
    updated_at: datetime


def _parse_date(value: str | None, timezone_name: str) -> date:
    if value:
        try:
            return date.fromisoformat(value)
        except ValueError as err:
            raise HTTPException(status_code=400, detail="check_date must use YYYY-MM-DD") from err
    return datetime.now(ZoneInfo(timezone_name)).date()


def _normalize_email(value: str) -> str:
    return value.strip().lower()


def _subscription_doc(payload: EnrollRequest) -> dict[str, Any]:
    now = now_utc()
    return {
        "user_email": _normalize_email(payload.user_email),
        "subscribed": True,
        "subscribed_since": now,
        "natal_data": payload.natal_data.model_dump(),
        "triggers_opted_in": payload.triggers_opted_in,
        "last_checked": None,
        "updated_at": now,
    }


def _natal_from_subscription(subscription: dict[str, Any]) -> dict[str, Any]:
    natal_data = subscription.get("natal_data") or {}
    return build_natal_snapshot(
        date_text=str(natal_data.get("date")),
        time_text=str(natal_data.get("time")),
        latitude=float(natal_data.get("latitude")),
        longitude=float(natal_data.get("longitude")),
        timezone_name=str(natal_data.get("timezone") or "Asia/Kolkata"),
        city_name=natal_data.get("city_name"),
    )


async def _load_active_subscription(collection, user_email: str) -> dict[str, Any]:
    subscription = await collection.find_one({"user_email": _normalize_email(user_email)})
    if not subscription or not subscription.get("subscribed"):
        raise HTTPException(status_code=404, detail="Active ritual subscription not found")
    return subscription


async def _persist_check_result(log_collection, result: dict[str, Any]) -> None:
    love_battery = {
        "user_email": result["user_email"],
        "trigger_type": "lunar_daily_score",
        "check_date": result["check_date"],
        "intensity": None,
        "orb_degrees": result["love_battery"].get("aspect_orb"),
        "alignment_description": result["love_battery"]["alignment_description"],
        "ritual_suggestion": None,
        "notification_worthy": result["love_battery"]["notification_worthy"],
        "active_from": result["check_date"],
        "active_until": result["check_date"],
        "fired_at": now_utc(),
        "love_battery_percent": result["love_battery"]["love_battery_percent"],
        "score_category": result["love_battery"]["score_category"],
        "moon_natal_venus_angle": result["love_battery"]["moon_natal_venus_angle"],
        "action_note": result["love_battery"]["action_note"],
    }
    await log_collection.update_one(
        {"user_email": love_battery["user_email"], "trigger_type": "lunar_daily_score", "check_date": love_battery["check_date"]},
        {"$set": love_battery, "$setOnInsert": {"id": f"{love_battery['user_email']}-lunar_daily_score-{love_battery['check_date']}"}},
        upsert=True,
    )
    for trigger in result["active_triggers"]:
        await log_collection.update_one(
            {"user_email": trigger["user_email"], "trigger_type": trigger["trigger_type"], "check_date": trigger["check_date"]},
            {"$set": trigger, "$setOnInsert": {"id": trigger["id"]}},
            upsert=True,
        )


def _to_trigger_entry(document: dict[str, Any]) -> TriggerLogEntry:
    return TriggerLogEntry(
        id=str(document.get("id")),
        user_email=str(document.get("user_email")),
        trigger_type=str(document.get("trigger_type")),
        check_date=str(document.get("check_date")),
        intensity=document.get("intensity"),
        orb_degrees=document.get("orb_degrees"),
        alignment_description=str(document.get("alignment_description") or ""),
        ritual_suggestion=document.get("ritual_suggestion"),
        notification_worthy=bool(document.get("notification_worthy")),
        active_from=document.get("active_from"),
        active_until=document.get("active_until"),
        fired_at=document.get("fired_at") if isinstance(document.get("fired_at"), datetime) else now_utc(),
        love_battery_percent=document.get("love_battery_percent"),
        score_category=document.get("score_category"),
        moon_natal_venus_angle=document.get("moon_natal_venus_angle"),
        action_note=document.get("action_note"),
    )


def _to_check_response(result: dict[str, Any]) -> RitualCheckResponse:
    return RitualCheckResponse(
        user_email=result["user_email"],
        check_date=result["check_date"],
        love_battery=LoveBatteryCard(**result["love_battery"]),
        active_triggers=[_to_trigger_entry(item) for item in result["active_triggers"]],
        notification_worthy_triggers=result["notification_worthy_triggers"],
        coach_summary=result["coach_summary"],
        next_upcoming_trigger=result.get("next_upcoming_trigger"),
    )


@router.post("/enroll", response_model=EnrollResponse)
async def enroll_ritual_engine(payload: EnrollRequest, request: Request) -> EnrollResponse:
    db = get_db(request)
    collection = get_engine_subscription_collection(db)
    document = _subscription_doc(payload)
    await collection.update_one(
        {"user_email": document["user_email"]},
        {"$set": document, "$setOnInsert": {"created_at": now_utc()}},
        upsert=True,
    )
    return EnrollResponse(
        user_email=document["user_email"],
        subscribed=True,
        triggers_opted_in=document["triggers_opted_in"],
        updated_at=document["updated_at"],
    )


@router.post("/check", response_model=RitualCheckResponse)
async def run_ritual_check(payload: CheckRequest, request: Request) -> RitualCheckResponse:
    db = get_db(request)
    subscription_collection = get_engine_subscription_collection(db)
    log_collection = get_engine_log_collection(db)
    subscription = await _load_active_subscription(subscription_collection, payload.user_email)
    natal_snapshot = _natal_from_subscription(subscription)
    check_date = _parse_date(payload.check_date, natal_snapshot["input"]["timezone"])
    result = compute_ritual_check(
        user_email=_normalize_email(payload.user_email),
        check_date=check_date,
        natal_snapshot=natal_snapshot,
        opted_in=subscription.get("triggers_opted_in") or DEFAULT_TRIGGERS,
    )
    await _persist_check_result(log_collection, result)
    await subscription_collection.update_one(
        {"user_email": _normalize_email(payload.user_email)},
        {"$set": {"last_checked": datetime.combine(check_date, datetime.min.time(), tzinfo=timezone.utc), "updated_at": now_utc()}},
    )
    return _to_check_response(result)


@router.get("/dashboard", response_model=RitualDashboardResponse)
async def get_ritual_dashboard(request: Request) -> RitualDashboardResponse:
    user_email = get_user_email(request)
    db = get_db(request)
    subscription_collection = get_engine_subscription_collection(db)
    log_collection = get_engine_log_collection(db)
    subscription = await _load_active_subscription(subscription_collection, user_email)
    natal_snapshot = _natal_from_subscription(subscription)
    today = datetime.now(ZoneInfo(natal_snapshot["input"]["timezone"])).date().isoformat()
    love_battery_doc = await log_collection.find_one(
        {"user_email": user_email, "trigger_type": "lunar_daily_score", "check_date": today}
    )
    if love_battery_doc is None:
        result = compute_ritual_check(
            user_email=user_email,
            check_date=date.fromisoformat(today),
            natal_snapshot=natal_snapshot,
            opted_in=subscription.get("triggers_opted_in") or DEFAULT_TRIGGERS,
        )
        await _persist_check_result(log_collection, result)
        love_battery = LoveBatteryCard(**result["love_battery"])
        active_triggers = [_to_trigger_entry(item) for item in result["active_triggers"]]
        next_upcoming = result.get("next_upcoming_trigger")
    else:
        love_battery = LoveBatteryCard(
            check_date=str(love_battery_doc["check_date"]),
            love_battery_percent=int(love_battery_doc["love_battery_percent"]),
            score_category=str(love_battery_doc["score_category"]),
            moon_natal_venus_angle=float(love_battery_doc["moon_natal_venus_angle"]),
            alignment_description=str(love_battery_doc["alignment_description"]),
            action_note=str(love_battery_doc.get("action_note") or ""),
            notification_worthy=bool(love_battery_doc["notification_worthy"]),
        )
        active_docs = await log_collection.find(
            {"user_email": user_email, "check_date": today, "trigger_type": {"$ne": "lunar_daily_score"}}
        ).sort("trigger_type", 1).to_list(length=10)
        active_triggers = [_to_trigger_entry(item) for item in active_docs]
        next_upcoming = compute_ritual_check(
            user_email=user_email,
            check_date=date.fromisoformat(today),
            natal_snapshot=natal_snapshot,
            opted_in=subscription.get("triggers_opted_in") or DEFAULT_TRIGGERS,
        ).get("next_upcoming_trigger")
    recent_docs = await log_collection.find({"user_email": user_email}).sort("fired_at", -1).limit(20).to_list(length=20)
    return RitualDashboardResponse(
        love_battery=love_battery,
        active_triggers=active_triggers,
        next_upcoming_trigger=next_upcoming,
        recent_history=[_to_trigger_entry(item) for item in recent_docs[:7]],
    )


@router.get("/history", response_model=RitualHistoryResponse)
async def get_ritual_history(request: Request) -> RitualHistoryResponse:
    user_email = get_user_email(request)
    collection = get_engine_log_collection(get_db(request))
    docs = await collection.find({"user_email": user_email}).sort("check_date", -1).limit(90).to_list(length=90)
    thirty_day_cutoff = datetime.now(timezone.utc).date().toordinal() - 30
    filtered = [
        _to_trigger_entry(item)
        for item in docs
        if date.fromisoformat(str(item["check_date"])).toordinal() >= thirty_day_cutoff
    ]
    return RitualHistoryResponse(items=filtered)


@router.delete("/unenroll", response_model=UnenrollResponse)
async def unenroll_ritual_engine(payload: UnenrollRequest, request: Request) -> UnenrollResponse:
    collection = get_engine_subscription_collection(get_db(request))
    user_email = _normalize_email(payload.user_email)
    result = await collection.update_one(
        {"user_email": user_email},
        {"$set": {"subscribed": False, "updated_at": now_utc()}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Subscription not found")
    updated_at = now_utc()
    return UnenrollResponse(user_email=user_email, subscribed=False, updated_at=updated_at)
