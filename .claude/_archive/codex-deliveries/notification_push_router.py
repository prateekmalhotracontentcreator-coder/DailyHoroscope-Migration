from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field


router = APIRouter(prefix="/api/notifications", tags=["notifications"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PushKeys(StrictModel):
    p256dh: str
    auth: str


class PushSubscriptionData(StrictModel):
    endpoint: str
    expirationTime: int | None = None
    keys: PushKeys


class PushSubscribeRequest(StrictModel):
    subscription: PushSubscriptionData
    user_agent: str | None = None
    device_label: str | None = None


class PushUnsubscribeRequest(StrictModel):
    endpoint: str


class PushSubscriptionResponse(StrictModel):
    ok: bool = True
    subscription_id: str | None = None


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
    collection = getattr(db, "push_subscriptions", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="push_subscriptions collection unavailable")
    return collection


@router.post("/push/subscribe", response_model=PushSubscriptionResponse)
async def subscribe_to_push(payload: PushSubscribeRequest, request: Request) -> PushSubscriptionResponse:
    db = _get_db(request)
    user_email = _get_user_email(request)
    now = _now()
    existing = await _collection(db).find_one({"endpoint": payload.subscription.endpoint})
    subscription_id = existing.get("id") if existing else str(uuid4())
    document = {
        "id": subscription_id,
        "user_email": user_email,
        "endpoint": payload.subscription.endpoint,
        "subscription": payload.subscription.model_dump(),
        "user_agent": payload.user_agent,
        "device_label": payload.device_label,
        "is_active": True,
        "last_seen_at": now,
        "updated_at": now,
        "created_at": existing.get("created_at", now) if existing else now,
    }
    await _collection(db).update_one({"endpoint": payload.subscription.endpoint}, {"$set": document}, upsert=True)
    return PushSubscriptionResponse(subscription_id=subscription_id)


@router.delete("/push/unsubscribe", response_model=PushSubscriptionResponse)
async def unsubscribe_from_push(payload: PushUnsubscribeRequest, request: Request) -> PushSubscriptionResponse:
    db = _get_db(request)
    user_email = _get_user_email(request)
    result = await _collection(db).delete_one({"endpoint": payload.endpoint, "user_email": user_email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Push subscription not found")
    return PushSubscriptionResponse()
