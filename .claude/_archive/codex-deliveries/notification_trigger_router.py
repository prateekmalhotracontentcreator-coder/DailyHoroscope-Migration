from __future__ import annotations

import os
from datetime import date, datetime, time, timezone
from typing import Any
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from notification_email_service import EMAIL_TEMPLATES, build_email_message, send_transactional_email
from notification_feed_router import create_in_app_notification
from notification_push_service import send_push_bulk
from notification_whatsapp_service import send_whatsapp_template


router = APIRouter(prefix="/api/notifications", tags=["notifications"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TriggerRequest(StrictModel):
    audience: str = "all"
    date: str | None = None
    report_id: str | None = None
    report_name: str | None = None
    action_url: str | None = None
    summary: str | None = None
    score: int | None = None
    tithi: str | None = None
    nakshatra: str | None = None
    sunrise: str | None = None
    special_yoga: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TriggerResults(StrictModel):
    matched_users: int = 0
    email_sent: int = 0
    whatsapp_sent: int = 0
    push_sent: int = 0
    in_app_created: int = 0
    failed: int = 0
    skipped: int = 0


class TriggerResponse(StrictModel):
    ok: bool = True
    trigger: str
    audience: str
    date: str
    results: TriggerResults


TRIGGER_CONFIG = {
    "panchang-daily": {
        "notification_type": "daily_panchang_digest",
        "email_template_id": "daily_panchang_digest",
        "whatsapp_template_name": "panchang_daily",
        "in_app_type": "panchang_reminder",
        "default_action_url": "/panchang",
    },
    "encounter-window": {
        "notification_type": "encounter_window",
        "email_template_id": "encounter_window_alert",
        "whatsapp_template_name": "encounter_window",
        "in_app_type": "encounter_window",
        "default_action_url": "/love",
    },
    "love-weather-weekly": {
        "notification_type": "love_weather_weekly",
        "email_template_id": "love_weather_weekly",
        "whatsapp_template_name": None,
        "in_app_type": "love_weather",
        "default_action_url": "/love",
    },
    "date-night-score": {
        "notification_type": "date_night_score",
        "email_template_id": "date_night_score",
        "whatsapp_template_name": "love_battery_daily",
        "in_app_type": "love_weather",
        "default_action_url": "/love",
    },
    "report-ready": {
        "notification_type": "report_ready",
        "email_template_id": "report_ready",
        "whatsapp_template_name": "report_ready",
        "in_app_type": "report_ready",
        "default_action_url": "/reports",
    },
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")
    return db


def _base_url(request: Request) -> str:
    return getattr(request.app.state, "frontend_url", None) or "https://everydayhoroscope.in"


def _log_collection(db):
    collection = getattr(db, "notification_logs", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="notification_logs collection unavailable")
    return collection


def _preference_collection(db):
    collection = getattr(db, "notification_preferences", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="notification_preferences collection unavailable")
    return collection


def _subscriber_collection(db):
    collection = getattr(db, "subscribers", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="subscribers collection unavailable")
    return collection


def _push_collection(db):
    collection = getattr(db, "push_subscriptions", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="push_subscriptions collection unavailable")
    return collection


def _normalize_email(value: Any) -> str | None:
    if not value:
        return None
    return str(value).strip().lower()


def _extract_subscriber_email(document: dict[str, Any]) -> str | None:
    return _normalize_email(document.get("email") or document.get("user_email"))


def _resolve_trigger_date(payload: TriggerRequest) -> str:
    if payload.date:
        return payload.date
    return date.today().isoformat()


def _parse_hhmm(value: str | None) -> time | None:
    if not value:
        return None
    parts = value.split(":")
    if len(parts) != 2:
        return None
    try:
        return time(hour=int(parts[0]), minute=int(parts[1]))
    except ValueError:
        return None


def _is_quiet_hours(now_local: datetime, start_text: str | None, end_text: str | None) -> bool:
    start = _parse_hhmm(start_text)
    end = _parse_hhmm(end_text)
    if start is None or end is None:
        return False
    current = now_local.time()
    if start == end:
        return False
    if start < end:
        return start <= current < end
    return current >= start or current < end


def _build_context(trigger_key: str, payload: TriggerRequest, request: Request, preference: dict[str, Any], user_email: str) -> dict[str, Any]:
    config = TRIGGER_CONFIG[trigger_key]
    action_url = payload.action_url or config["default_action_url"]
    if action_url.startswith("/"):
        full_action_url = f"{_base_url(request)}{action_url}"
    else:
        full_action_url = action_url
    target_date = _resolve_trigger_date(payload)
    return {
        "user": {
            "email": user_email,
            "timezone": preference.get("timezone") or "UTC",
        },
        "event": {
            "type": config["notification_type"],
            "date": target_date,
            "report_id": payload.report_id,
            "report_name": payload.report_name or "Report",
        },
        "content": {
            "summary": payload.summary,
            "score": payload.score,
            "tithi": payload.tithi,
            "nakshatra": payload.nakshatra,
            "sunrise": payload.sunrise,
            "special_yoga": payload.special_yoga,
        },
        "links": {
            "base_url": _base_url(request),
            "action_url": full_action_url,
        },
        "metadata": payload.metadata,
    }


def _whatsapp_params(trigger_key: str, context: dict[str, Any]) -> list[str]:
    if trigger_key == "report-ready":
        return [str(context["event"]["report_name"]), str(context["event"]["date"])]
    if trigger_key == "panchang-daily":
        return [
            str(context["content"].get("tithi") or ""),
            str(context["content"].get("nakshatra") or ""),
            str(context["content"].get("sunrise") or ""),
        ]
    if trigger_key == "encounter-window":
        return [str(context["event"]["date"])]
    if trigger_key == "date-night-score":
        return [str(context["content"].get("score") or "")]
    return []


async def _write_log(
    db,
    *,
    channel: str,
    status: str,
    notification_type: str,
    user_email: str,
    audience: str,
    dedupe_key: str,
    provider: str | None = None,
    provider_message_id: str | None = None,
    error: str | None = None,
    template_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> None:
    document = {
        "id": str(uuid4()),
        "source": "notification_engine",
        "channel": channel,
        "status": status,
        "notification_type": notification_type,
        "template_id": template_id,
        "user_email": user_email,
        "audience": audience,
        "provider": provider,
        "provider_message_id": provider_message_id,
        "error": error,
        "dedupe_key": dedupe_key,
        "metadata": metadata or {},
        "created_at": _now(),
    }
    await _log_collection(db).insert_one(document)


async def _already_sent(db, dedupe_key: str) -> bool:
    existing = await _log_collection(db).find_one(
        {"source": "notification_engine", "dedupe_key": dedupe_key, "status": "sent"},
        {"id": 1},
    )
    return existing is not None


async def _resolve_audience(db, audience: str) -> list[dict[str, Any]]:
    if audience == "all":
        return await _subscriber_collection(db).find({}).to_list(length=100000)
    if audience.startswith("tag:"):
        tag_name = audience.split(":", 1)[1]
        return await _subscriber_collection(db).find({"tags": {"$in": [tag_name]}}).to_list(length=100000)
    if audience.startswith("email:"):
        email = audience.split(":", 1)[1].strip().lower()
        document = await _subscriber_collection(db).find_one(
            {"$or": [{"email": email}, {"user_email": email}]}
        )
        return [document] if document else []
    raise HTTPException(status_code=400, detail="Unsupported audience selector")


async def _load_preference(db, user_email: str) -> dict[str, Any]:
    preference = await _preference_collection(db).find_one({"user_email": user_email})
    if preference:
        return preference
    return {
        "user_email": user_email,
        "timezone": "UTC",
        "channels": {
            "email": True,
            "whatsapp": False,
            "push": True,
            "in_app": True,
        },
        "types": {
            "report_ready": True,
            "encounter_window": True,
            "love_weather_weekly": True,
            "daily_panchang_digest": True,
            "date_night_score": True,
            "welcome": True,
        },
        "whatsapp_phone": None,
        "quiet_hours_start": None,
        "quiet_hours_end": None,
    }


def _channel_allowed(preference: dict[str, Any], channel: str, notification_type: str) -> bool:
    channels = preference.get("channels") or {}
    types = preference.get("types") or {}
    return bool(channels.get(channel)) and bool(types.get(notification_type, True))


def _local_now(preference: dict[str, Any]) -> datetime:
    timezone_name = preference.get("timezone") or "UTC"
    try:
        tz = ZoneInfo(str(timezone_name))
    except Exception:
        tz = timezone.utc
    return _now().astimezone(tz)


async def _send_for_user(
    db,
    *,
    request: Request,
    trigger_key: str,
    payload: TriggerRequest,
    audience: str,
    subscriber: dict[str, Any],
    results: TriggerResults,
) -> None:
    user_email = _extract_subscriber_email(subscriber)
    if not user_email:
        results.skipped += 1
        return

    config = TRIGGER_CONFIG[trigger_key]
    preference = await _load_preference(db, user_email)
    if not preference.get("types", {}).get(config["notification_type"], True):
        results.skipped += 1
        return

    if _is_quiet_hours(_local_now(preference), preference.get("quiet_hours_start"), preference.get("quiet_hours_end")):
        results.skipped += 1
        return

    dedupe_key = f"{config['notification_type']}:{payload.report_id or _resolve_trigger_date(payload)}:{user_email}"
    if await _already_sent(db, dedupe_key):
        results.skipped += 1
        return

    results.matched_users += 1
    context = _build_context(trigger_key, payload, request, preference, user_email)
    email_message = build_email_message(config["email_template_id"], context)

    if _channel_allowed(preference, "email", config["notification_type"]):
        email_result = await send_transactional_email(
            user_email,
            config["email_template_id"],
            context,
            db=db,
            metadata={"dedupe_key": dedupe_key},
        )
        await _write_log(
            db,
            channel="email",
            status=email_result["status"],
            notification_type=config["notification_type"],
            user_email=user_email,
            audience=audience,
            dedupe_key=dedupe_key,
            provider=email_result.get("provider"),
            provider_message_id=email_result.get("provider_message_id"),
            error=email_result.get("error"),
            template_id=config["email_template_id"],
            metadata=payload.metadata,
        )
        if email_result["status"] == "sent":
            results.email_sent += 1
        elif email_result["status"] == "failed":
            results.failed += 1
        else:
            results.skipped += 1

    if config.get("whatsapp_template_name") and _channel_allowed(preference, "whatsapp", config["notification_type"]):
        phone_number = preference.get("whatsapp_phone")
        if phone_number:
            whatsapp_result = await send_whatsapp_template(
                phone_number,
                config["whatsapp_template_name"],
                _whatsapp_params(trigger_key, context),
                db=db,
                metadata={"dedupe_key": dedupe_key},
            )
            await _write_log(
                db,
                channel="whatsapp",
                status=whatsapp_result["status"],
                notification_type=config["notification_type"],
                user_email=user_email,
                audience=audience,
                dedupe_key=dedupe_key,
                provider=whatsapp_result.get("provider"),
                provider_message_id=whatsapp_result.get("provider_message_id"),
                error=whatsapp_result.get("error"),
                template_id=config.get("whatsapp_template_name"),
                metadata=payload.metadata,
            )
            if whatsapp_result["status"] == "sent":
                results.whatsapp_sent += 1
            elif whatsapp_result["status"] == "failed":
                results.failed += 1
            else:
                results.skipped += 1
        else:
            results.skipped += 1

    if _channel_allowed(preference, "push", config["notification_type"]):
        subscriptions = await _push_collection(db).find({"user_email": user_email, "is_active": True}).to_list(length=100)
        if subscriptions:
            push_result = await send_push_bulk(
                [item["subscription"] for item in subscriptions if item.get("subscription")],
                email_message["subject"],
                email_message["preview_text"],
                "/icons/notification.png",
                context["links"]["action_url"],
                db=db,
                metadata={"tag": config["notification_type"], "data": payload.metadata},
            )
            for endpoint in push_result.get("inactive_endpoints", []):
                await _push_collection(db).update_one({"endpoint": endpoint}, {"$set": {"is_active": False, "updated_at": _now()}})
            await _write_log(
                db,
                channel="push",
                status=push_result["status"],
                notification_type=config["notification_type"],
                user_email=user_email,
                audience=audience,
                dedupe_key=dedupe_key,
                provider="web_push",
                error=push_result.get("error"),
                metadata=payload.metadata,
            )
            if push_result["sent_count"] > 0:
                results.push_sent += push_result["sent_count"]
            if push_result["failed_count"] > 0:
                results.failed += push_result["failed_count"]
            if push_result["skipped_count"] > 0:
                results.skipped += push_result["skipped_count"]

    if _channel_allowed(preference, "in_app", config["notification_type"]):
        document = await create_in_app_notification(
            db,
            user_email,
            config["in_app_type"],
            email_message["subject"],
            email_message["preview_text"],
            context["links"]["action_url"],
            dedupe_key=dedupe_key,
            metadata=payload.metadata,
        )
        in_app_status = "sent" if document else "failed"
        await _write_log(
            db,
            channel="in_app",
            status=in_app_status,
            notification_type=config["notification_type"],
            user_email=user_email,
            audience=audience,
            dedupe_key=dedupe_key,
            provider="mongodb",
            error=None if document else "Failed to create in-app notification",
            metadata=payload.metadata,
        )
        if document:
            results.in_app_created += 1
        else:
            results.failed += 1


async def _run_trigger(trigger_key: str, payload: TriggerRequest, request: Request) -> TriggerResponse:
    db = _get_db(request)
    subscribers = await _resolve_audience(db, payload.audience)
    results = TriggerResults()
    for subscriber in subscribers:
        await _send_for_user(
            db,
            request=request,
            trigger_key=trigger_key,
            payload=payload,
            audience=payload.audience,
            subscriber=subscriber,
            results=results,
        )
    return TriggerResponse(
        trigger=trigger_key.replace("-", "_"),
        audience=payload.audience,
        date=_resolve_trigger_date(payload),
        results=results,
    )


def _require_trigger_key(x_temple_trigger_key: str | None) -> None:
    expected = os.getenv("TEMPLE_TRIGGER_KEY")
    if not expected:
        raise HTTPException(status_code=500, detail="TEMPLE_TRIGGER_KEY is not configured")
    if x_temple_trigger_key != expected:
        raise HTTPException(status_code=403, detail="Invalid trigger key")


@router.post("/trigger/panchang-daily", response_model=TriggerResponse)
async def trigger_panchang_daily(
    payload: TriggerRequest,
    request: Request,
    x_temple_trigger_key: str | None = Header(default=None),
) -> TriggerResponse:
    _require_trigger_key(x_temple_trigger_key)
    return await _run_trigger("panchang-daily", payload, request)


@router.post("/trigger/encounter-window", response_model=TriggerResponse)
async def trigger_encounter_window(
    payload: TriggerRequest,
    request: Request,
    x_temple_trigger_key: str | None = Header(default=None),
) -> TriggerResponse:
    _require_trigger_key(x_temple_trigger_key)
    return await _run_trigger("encounter-window", payload, request)


@router.post("/trigger/love-weather-weekly", response_model=TriggerResponse)
async def trigger_love_weather_weekly(
    payload: TriggerRequest,
    request: Request,
    x_temple_trigger_key: str | None = Header(default=None),
) -> TriggerResponse:
    _require_trigger_key(x_temple_trigger_key)
    return await _run_trigger("love-weather-weekly", payload, request)


@router.post("/trigger/date-night-score", response_model=TriggerResponse)
async def trigger_date_night_score(
    payload: TriggerRequest,
    request: Request,
    x_temple_trigger_key: str | None = Header(default=None),
) -> TriggerResponse:
    _require_trigger_key(x_temple_trigger_key)
    return await _run_trigger("date-night-score", payload, request)


@router.post("/trigger/report-ready", response_model=TriggerResponse)
async def trigger_report_ready(
    payload: TriggerRequest,
    request: Request,
    x_temple_trigger_key: str | None = Header(default=None),
) -> TriggerResponse:
    _require_trigger_key(x_temple_trigger_key)
    if not payload.report_name:
        raise HTTPException(status_code=400, detail="report_name is required for report-ready notifications")
    return await _run_trigger("report-ready", payload, request)
