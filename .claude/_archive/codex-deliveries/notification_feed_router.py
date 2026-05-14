from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict


router = APIRouter(prefix="/api/notifications", tags=["notifications"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class InAppNotificationItem(StrictModel):
    id: str
    user_email: str
    type: str
    title: str
    body: str
    action_url: str | None = None
    is_read: bool = False
    created_at: datetime


class InAppNotificationFeedResponse(StrictModel):
    items: list[InAppNotificationItem]


class MarkReadResponse(StrictModel):
    ok: bool = True
    updated_count: int | None = None


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")
    return db


def _collection(db):
    collection = getattr(db, "in_app_notifications", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="in_app_notifications collection unavailable")
    return collection


def _get_user_email(request: Request) -> str:
    user = getattr(request.state, "user", None)
    if not isinstance(user, dict) or not user.get("email"):
        raise HTTPException(status_code=401, detail="Authentication required")
    return str(user["email"]).strip().lower()


async def create_in_app_notification(
    db,
    user_email: str,
    notification_type: str,
    title: str,
    body: str,
    action_url: str | None,
    *,
    dedupe_key: str | None = None,
    metadata: dict | None = None,
) -> dict:
    now = _now()
    collection = _collection(db)
    if dedupe_key:
        existing = await collection.find_one({"dedupe_key": dedupe_key})
        if existing:
            return existing
    document = {
        "id": str(uuid4()),
        "user_email": user_email,
        "type": notification_type,
        "title": title,
        "body": body,
        "action_url": action_url,
        "is_read": False,
        "channel_origin": "notification_engine",
        "dedupe_key": dedupe_key,
        "metadata": metadata or {},
        "created_at": now,
    }
    await collection.insert_one(document)
    return document


@router.get("/feed", response_model=InAppNotificationFeedResponse)
async def get_notification_feed(request: Request) -> InAppNotificationFeedResponse:
    db = _get_db(request)
    user_email = _get_user_email(request)
    since = _now() - timedelta(days=30)
    cursor = _collection(db).find(
        {
            "user_email": user_email,
            "$or": [
                {"is_read": False},
                {"created_at": {"$gte": since}},
            ],
        }
    ).sort("created_at", -1)
    items = await cursor.to_list(length=500)
    return InAppNotificationFeedResponse(items=[InAppNotificationItem.model_validate(item) for item in items])


@router.patch("/{notification_id}/read", response_model=MarkReadResponse)
async def mark_notification_read(notification_id: str, request: Request) -> MarkReadResponse:
    db = _get_db(request)
    user_email = _get_user_email(request)
    result = await _collection(db).update_one(
        {"id": notification_id, "user_email": user_email},
        {"$set": {"is_read": True}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return MarkReadResponse()


@router.patch("/read-all", response_model=MarkReadResponse)
async def mark_all_notifications_read(request: Request) -> MarkReadResponse:
    db = _get_db(request)
    user_email = _get_user_email(request)
    result = await _collection(db).update_many(
        {"user_email": user_email, "is_read": False},
        {"$set": {"is_read": True}},
    )
    return MarkReadResponse(updated_count=result.modified_count)
