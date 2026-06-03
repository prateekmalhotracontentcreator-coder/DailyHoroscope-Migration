"""
strategist_notification_service.py
STR-2H · Notification Trigger Service
Doc 11 · 03 Jun 2026

Seven condition evaluators for the Strategist module.
Each function checks whether a trigger should fire for a given user and returns
a typed event dict that the NotificationEngine delivers via the existing
notification_trigger_router.py channels (push · bell · toast).

Channel intent per spec:
  push  -- time-critical / off-app moments
  bell  -- persistent in-app feed (seeker finds later)
  toast -- only when already in-app

Delivery rules:
  golden_hour_open    → push + toast    · once per day
  hurdle_raised       → bell + push     · dedup per hurdle_id
  golden_hour_egress  → push + toast    · once per day · suppressed if ritual logged
  ritual_reminder     → push only       · daily at user reminder time · skip if logged
  verdict_change      → bell + push     · fire on flip only
  mission_complete    → toast + bell    · dedup per mission_id
  dasha_transition    → bell + push     · fire on boundary date only

Usage (from a cron task or user-interaction hook):
    from strategist_notification_service import evaluate_golden_hour_open
    events = await evaluate_golden_hour_open(db, user_id, sunset_iso)
    for event in events:
        await dispatch_str_notification(request, event)
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

logger = logging.getLogger(__name__)

IST = timezone(timedelta(hours=5, minutes=30))
GOLDEN_BUFFER_SECS = 30 * 60   # 30 min before sunset
EGRESS_BUFFER_SECS = 5 * 60    # 5 min before sunset


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


async def _ritual_logged_today(db, user_id: str) -> bool:
    """Return True if today's ritual is already logged for this user."""
    today = datetime.now(IST).date()
    try:
        doc = await db.ritual_logs.find_one({
            "user_id": str(user_id),
            "date": today.isoformat(),
        })
        return doc is not None
    except Exception:
        return False


async def _already_fired_today(db, user_id: str, trigger_type: str) -> bool:
    """Dedup guard -- returns True if this trigger already fired today for user."""
    today = datetime.now(IST).date().isoformat()
    try:
        doc = await db.str_notification_log.find_one({
            "user_id": str(user_id),
            "trigger_type": trigger_type,
            "date": today,
        })
        return doc is not None
    except Exception:
        return False


async def _mark_fired(db, user_id: str, trigger_type: str, meta: dict | None = None) -> None:
    today = datetime.now(IST).date().isoformat()
    try:
        await db.str_notification_log.insert_one({
            "user_id": str(user_id),
            "trigger_type": trigger_type,
            "date": today,
            "fired_at": datetime.now(timezone.utc).isoformat(),
            "meta": meta or {},
        })
    except Exception as exc:
        logger.warning("str_notification_log write failed: %s", exc)


# ─────────────────────────────────────────────────────────────────────────────
# Trigger 1 · golden_hour_open
# Fire condition: now == sunset_iso − 30 min · WarRoomState ingress to GOLDEN_HOUR
# Channel: push + toast · once per day
# ─────────────────────────────────────────────────────────────────────────────

async def evaluate_golden_hour_open(
    db,
    user_id: str,
    sunset_iso: str | None,
    *,
    now: datetime | None = None,
    window_secs: int = 120,
) -> list[dict[str, Any]]:
    """
    Returns a trigger event if now is within `window_secs` of the golden-hour
    ingress (sunset − 30 min) and has not fired today.
    """
    sunset = _parse_iso(sunset_iso)
    if not sunset:
        return []

    now = now or datetime.now(timezone.utc)
    ingress = sunset - timedelta(seconds=GOLDEN_BUFFER_SECS)

    if not (ingress - timedelta(seconds=window_secs) <= now <= ingress + timedelta(seconds=window_secs)):
        return []

    if await _already_fired_today(db, user_id, "str_golden_hour_open"):
        return []

    await _mark_fired(db, user_id, "str_golden_hour_open")
    return [{
        "trigger_key": "str-golden-hour-open",
        "user_id": str(user_id),
        "channels": ["push", "toast"],
        "action_url": "/strategist/war-room",
        "copy": {
            "title": "Your Golden Hour opens",
            "body": "The ritual window is open for the next thirty minutes. Perform today's remedy while the sky favours it.",
        },
        "meta": {"sunset_iso": sunset_iso},
    }]


# ─────────────────────────────────────────────────────────────────────────────
# Trigger 2 · hurdle_raised
# Fire condition: engine activates a Hurdle Library record (retrograde/eclipse/combustion)
# Channel: bell + push · dedup per hurdle_id
# ─────────────────────────────────────────────────────────────────────────────

async def evaluate_hurdle_raised(
    db,
    user_id: str,
    hurdle_id: str,
    hurdle_planet: str,
) -> list[dict[str, Any]]:
    """
    Returns a trigger event for a newly-activated hurdle record.
    Caller must supply hurdle_id for dedup; call once per detected hurdle.
    """
    try:
        doc = await db.str_notification_log.find_one({
            "user_id": str(user_id),
            "trigger_type": "str_hurdle_raised",
            "meta.hurdle_id": hurdle_id,
        })
        if doc:
            return []
        await _mark_fired(db, user_id, "str_hurdle_raised", meta={"hurdle_id": hurdle_id, "planet": hurdle_planet})
    except Exception as exc:
        logger.warning("hurdle_raised dedup check failed: %s", exc)
        return []

    body = f"{hurdle_planet} turns against your chart. Pause launches and hold open bids until the sky clears."
    return [{
        "trigger_key": "str-hurdle-raised",
        "user_id": str(user_id),
        "channels": ["bell", "push"],
        "action_url": "/strategist/war-room",
        "copy": {
            "title": "A hurdle has risen",
            "body": body,
        },
        "meta": {"hurdle_id": hurdle_id, "planet": hurdle_planet},
    }]


# ─────────────────────────────────────────────────────────────────────────────
# Trigger 3 · golden_hour_egress
# Fire condition: now == sunset_iso − 5 min · only if ritual not logged · once per day
# Channel: push + toast
# ─────────────────────────────────────────────────────────────────────────────

async def evaluate_golden_hour_egress(
    db,
    user_id: str,
    sunset_iso: str | None,
    *,
    now: datetime | None = None,
    window_secs: int = 120,
) -> list[dict[str, Any]]:
    """
    Returns a trigger event if now is within `window_secs` of sunset − 5 min,
    the ritual is not yet logged, and has not fired today.
    """
    sunset = _parse_iso(sunset_iso)
    if not sunset:
        return []

    now = now or datetime.now(timezone.utc)
    egress = sunset - timedelta(seconds=EGRESS_BUFFER_SECS)

    if not (egress - timedelta(seconds=window_secs) <= now <= egress + timedelta(seconds=window_secs)):
        return []

    # Suppressed if ritual already logged
    if await _ritual_logged_today(db, user_id):
        return []

    if await _already_fired_today(db, user_id, "str_golden_hour_egress"):
        return []

    await _mark_fired(db, user_id, "str_golden_hour_egress")
    return [{
        "trigger_key": "str-golden-hour-egress",
        "user_id": str(user_id),
        "channels": ["push", "toast"],
        "action_url": "/strategist/war-room",
        "copy": {
            "title": "Golden Hour closing",
            "body": "Five minutes remain in today's ritual window. Complete your remedy before sunset locks it.",
        },
        "meta": {"sunset_iso": sunset_iso},
    }]


# ─────────────────────────────────────────────────────────────────────────────
# Trigger 4 · ritual_reminder
# Fire condition: daily at user reminder time · only if ritual not logged · skip if streak credited
# Channel: push only
# ─────────────────────────────────────────────────────────────────────────────

async def evaluate_ritual_reminder(
    db,
    user_id: str,
    streak_days: int,
    *,
    reminder_time_hhmm: str = "08:00",
    now: datetime | None = None,
    window_secs: int = 180,
) -> list[dict[str, Any]]:
    """
    Returns a trigger event if:
    - It is within `window_secs` of today's reminder time (IST)
    - Today's ritual is not yet logged
    - This trigger has not fired today
    """
    now = now or datetime.now(timezone.utc)
    now_ist = now.astimezone(IST)

    try:
        hour, minute = map(int, reminder_time_hhmm.split(":"))
        reminder_dt = now_ist.replace(hour=hour, minute=minute, second=0, microsecond=0)
    except (ValueError, AttributeError):
        return []

    delta = abs((now_ist - reminder_dt).total_seconds())
    if delta > window_secs:
        return []

    if await _ritual_logged_today(db, user_id):
        return []

    if await _already_fired_today(db, user_id, "str_ritual_reminder"):
        return []

    await _mark_fired(db, user_id, "str_ritual_reminder")
    body = f"Your {streak_days}-day streak is unbroken. A few minutes now keeps the discipline -- and the gain -- intact."
    return [{
        "trigger_key": "str-ritual-reminder",
        "user_id": str(user_id),
        "channels": ["push"],
        "action_url": "/strategist/war-room",
        "copy": {
            "title": "Today's ritual awaits",
            "body": body,
        },
        "meta": {"streak_days": streak_days},
    }]


# ─────────────────────────────────────────────────────────────────────────────
# Trigger 5 · verdict_change
# Fire condition: Gate 0 re-consult returns verdict != stored verdict · flip only
# Channel: bell + push
# ─────────────────────────────────────────────────────────────────────────────

async def evaluate_verdict_change(
    db,
    user_id: str,
    old_verdict: str | None,
    new_verdict: str,
) -> list[dict[str, Any]]:
    """
    Returns a trigger event if the verdict has changed (flip only, not re-confirmation).
    Caller supplies old_verdict (stored) and new_verdict (just received from Gate 0).
    """
    if not old_verdict or old_verdict.upper() == new_verdict.upper():
        return []

    verdict_display = new_verdict.upper()
    body = f"Gate 0 now reads {verdict_display}. Your active path has shifted -- open the war room to see what it asks."
    return [{
        "trigger_key": "str-verdict-change",
        "user_id": str(user_id),
        "channels": ["bell", "push"],
        "action_url": "/strategist/war-room",
        "copy": {
            "title": "Krishna's verdict has changed",
            "body": body,
        },
        "meta": {"from_verdict": old_verdict, "to_verdict": new_verdict},
    }]


# ─────────────────────────────────────────────────────────────────────────────
# Trigger 6 · mission_complete
# Fire condition: mission KPI target marked met · dedup per mission_id · toast + bell
# ─────────────────────────────────────────────────────────────────────────────

async def evaluate_mission_complete(
    db,
    user_id: str,
    mission_id: str,
    mission_name: str,
) -> list[dict[str, Any]]:
    """
    Returns a trigger event when a mission's KPI target is met.
    Dedups per mission_id -- fires once per mission lifetime.
    """
    try:
        doc = await db.str_notification_log.find_one({
            "user_id": str(user_id),
            "trigger_type": "str_mission_complete",
            "meta.mission_id": mission_id,
        })
        if doc:
            return []
        today = datetime.now(IST).date().isoformat()
        await db.str_notification_log.insert_one({
            "user_id": str(user_id),
            "trigger_type": "str_mission_complete",
            "date": today,
            "fired_at": datetime.now(timezone.utc).isoformat(),
            "meta": {"mission_id": mission_id, "mission_name": mission_name},
        })
    except Exception as exc:
        logger.warning("mission_complete dedup check failed: %s", exc)
        return []

    body = f"{mission_name} hit its target. Claim the conquest gain and choose your next move."
    return [{
        "trigger_key": "str-mission-complete",
        "user_id": str(user_id),
        "channels": ["toast", "bell"],
        "action_url": "/strategist/missions",
        "copy": {
            "title": "Mission accomplished",
            "body": body,
        },
        "meta": {"mission_id": mission_id, "mission_name": mission_name},
    }]


# ─────────────────────────────────────────────────────────────────────────────
# Trigger 7 · dasha_transition
# Fire condition: vimshottari calc detects maha/antar boundary crossing
# Channel: bell + push · fire on the date the period turns
# ─────────────────────────────────────────────────────────────────────────────

async def evaluate_dasha_transition(
    db,
    user_id: str,
    from_planet: str,
    to_planet: str,
    transition_date_iso: str,
) -> list[dict[str, Any]]:
    """
    Returns a trigger event when a dasha period boundary is crossed.
    Caller supplies from/to planet names and transition date.
    Dedups per (from_planet, to_planet) pair so it fires at most once per transition.
    """
    dedup_key = f"{from_planet}_{to_planet}_{transition_date_iso[:10]}"
    try:
        doc = await db.str_notification_log.find_one({
            "user_id": str(user_id),
            "trigger_type": "str_dasha_transition",
            "meta.dedup_key": dedup_key,
        })
        if doc:
            return []
        await db.str_notification_log.insert_one({
            "user_id": str(user_id),
            "trigger_type": "str_dasha_transition",
            "date": transition_date_iso[:10],
            "fired_at": datetime.now(timezone.utc).isoformat(),
            "meta": {"dedup_key": dedup_key, "from_planet": from_planet, "to_planet": to_planet},
        })
    except Exception as exc:
        logger.warning("dasha_transition dedup check failed: %s", exc)
        return []

    body = f"{from_planet} yields to {to_planet}. A new chapter of timing begins -- recalibrate your missions to it."
    return [{
        "trigger_key": "str-dasha-transition",
        "user_id": str(user_id),
        "channels": ["bell", "push"],
        "action_url": "/strategist/war-room",
        "copy": {
            "title": "Your dasha has turned",
            "body": body,
        },
        "meta": {"from_planet": from_planet, "to_planet": to_planet, "transition_date": transition_date_iso[:10]},
    }]


# ─────────────────────────────────────────────────────────────────────────────
# Dispatch helper -- sends a resolved trigger event to the push service
# Caller imports and uses this from strategist_router.py or a cron handler.
# ─────────────────────────────────────────────────────────────────────────────

async def dispatch_str_notification(
    db,
    event: dict[str, Any],
    user_email: str,
    push_subscriptions: list[dict] | None = None,
) -> None:
    """
    Route a resolved STR-2H trigger event to in-app notification feed + push.
    user_email: resolved email for the target user (required by notification_feed_router).
    push_subscriptions: list of push subscription objects for this user (optional).
    """
    try:
        from notification_feed_router import create_in_app_notification  # noqa: PLC0415

        copy_ = event.get("copy", {})
        channels = event.get("channels", [])

        if "bell" in channels or "toast" in channels:
            await create_in_app_notification(
                db=db,
                user_email=user_email,
                notification_type=event["trigger_key"].replace("-", "_"),
                title=copy_.get("title", ""),
                body=copy_.get("body", ""),
                action_url=event.get("action_url", "/strategist/war-room"),
                metadata=event.get("meta", {}),
            )

        if "push" in channels and push_subscriptions:
            from notification_push_service import send_push_bulk  # noqa: PLC0415
            payloads = [
                {
                    "subscription": sub,
                    "payload": {
                        "title": copy_.get("title", ""),
                        "body": copy_.get("body", ""),
                        "url": event.get("action_url", "/strategist/war-room"),
                    },
                }
                for sub in push_subscriptions
            ]
            await send_push_bulk(payloads)

    except Exception as exc:
        logger.error("dispatch_str_notification failed for %s: %s", event.get("trigger_key"), exc)
