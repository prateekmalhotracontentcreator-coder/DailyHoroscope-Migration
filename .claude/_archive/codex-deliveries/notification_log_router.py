from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict


router = APIRouter(prefix="/api/notifications", tags=["notifications"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


class NotificationLogItem(StrictModel):
    id: str
    source: str
    channel: str
    status: str
    notification_type: str
    user_email: str | None = None
    provider: str | None = None
    provider_message_id: str | None = None
    error: str | None = None
    created_at: datetime


class NotificationLogResponse(StrictModel):
    items: list[NotificationLogItem]


def _get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")
    return db


def _require_admin(request: Request) -> None:
    user = getattr(request.state, "user", None)
    if not isinstance(user, dict) or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("/log", response_model=NotificationLogResponse)
async def get_notification_log(request: Request) -> NotificationLogResponse:
    _require_admin(request)
    db = _get_db(request)
    collection = getattr(db, "notification_logs", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="notification_logs collection unavailable")
    items = await collection.find({"source": "notification_engine"}).sort("created_at", -1).limit(100).to_list(length=100)
    return NotificationLogResponse(items=[NotificationLogItem.model_validate(item) for item in items])
