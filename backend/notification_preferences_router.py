from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict


router = APIRouter(prefix="/api/notifications", tags=["notifications"])

NotificationType = Literal[
    "report_ready",
    "encounter_window",
    "love_weather_weekly",
    "daily_panchang_digest",
    "date_night_score",
    "welcome",
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ChannelPreferences(StrictModel):
    email: bool = True
    whatsapp: bool = False
    push: bool = True
    in_app: bool = True


class TypePreferences(StrictModel):
    report_ready: bool = True
    encounter_window: bool = True
    love_weather_weekly: bool = True
    daily_panchang_digest: bool = True
    date_night_score: bool = True
    welcome: bool = True


class NotificationPreferencesPayload(StrictModel):
    timezone: str = "UTC"
    channels: ChannelPreferences = ChannelPreferences()
    types: TypePreferences = TypePreferences()
    whatsapp_phone: str | None = None
    quiet_hours_start: str | None = None
    quiet_hours_end: str | None = None


class NotificationPreferencesResponse(NotificationPreferencesPayload):
    user_email: str
    updated_at: datetime


class NotificationPreferencesUpdateResponse(StrictModel):
    ok: bool = True
    preferences: NotificationPreferencesResponse


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")
    return db


def _get_user_email(request: Request) -> str:
    user = getattr(request.state, "user", None)
    if not isinstance(user, dict) or not user.get("email"):
        raise HTTPException(status_code=401, detail="Authentication required")
    return str(user["email"]).strip().lower()


def _collection(db):
    collection = getattr(db, "notification_preferences", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="notification_preferences collection unavailable")
    return collection


def _default_preferences(user_email: str) -> NotificationPreferencesResponse:
    return NotificationPreferencesResponse(
        user_email=user_email,
        timezone="UTC",
        channels=ChannelPreferences(),
        types=TypePreferences(),
        whatsapp_phone=None,
        quiet_hours_start=None,
        quiet_hours_end=None,
        updated_at=_now(),
    )


@router.get("/preferences", response_model=NotificationPreferencesResponse)
async def get_notification_preferences(request: Request) -> NotificationPreferencesResponse:
    db = _get_db(request)
    user_email = _get_user_email(request)
    document = await _collection(db).find_one({"user_email": user_email})
    if not document:
        return _default_preferences(user_email)
    return NotificationPreferencesResponse.model_validate(document)


@router.put("/preferences", response_model=NotificationPreferencesUpdateResponse)
async def put_notification_preferences(
    payload: NotificationPreferencesPayload,
    request: Request,
) -> NotificationPreferencesUpdateResponse:
    db = _get_db(request)
    user_email = _get_user_email(request)
    now = _now()
    document = {
        "user_email": user_email,
        "timezone": payload.timezone,
        "channels": payload.channels.model_dump(),
        "types": payload.types.model_dump(),
        "whatsapp_phone": payload.whatsapp_phone,
        "quiet_hours_start": payload.quiet_hours_start,
        "quiet_hours_end": payload.quiet_hours_end,
        "created_at": now,
        "updated_at": now,
    }
    existing = await _collection(db).find_one({"user_email": user_email}, {"created_at": 1})
    if existing and existing.get("created_at"):
        document["created_at"] = existing["created_at"]

    await _collection(db).update_one({"user_email": user_email}, {"$set": document}, upsert=True)
    return NotificationPreferencesUpdateResponse(
        preferences=NotificationPreferencesResponse.model_validate(document),
    )
