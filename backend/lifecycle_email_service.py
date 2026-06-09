from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
import os
from typing import Any, Optional
import uuid

from notification_email_service import RESEND_API_URL, _post_json
from notification_whatsapp_service import send_whatsapp_text


_DB = None
_SCHEDULER = None


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def configure_runtime(*, db, scheduler) -> None:
    global _DB, _SCHEDULER
    _DB = db
    _SCHEDULER = scheduler


PRODUCT_CONTENT = {
    "birth_chart": {
        "focus": "Turn to the Dasha Timeline section first.",
        "link": "/birth-chart",
        "stage2_note": "Revisit the Dasha Timeline and the Moon-sign emotional pattern together. That pairing usually reveals what is active right now, not just what is natal.",
        "stage3_pitch": "Premium unlocks Brihat Kundli Pro and deeper chart guidance beyond the first reading.",
    },
    "brihat_kundli": {
        "focus": "Start with the Yoga analysis in Section 4.",
        "link": "/horoscope/monthly",
        "stage2_note": "Your Brihat reading becomes more useful when you compare its yogas against this month's transits and themes. Look for repetition, not isolated symbolism.",
        "stage3_pitch": "Premium turns Brihat Kundli into an ongoing guidance system with recurring monthly transit support.",
    },
    "kundali_milan": {
        "focus": "Focus first on the Guna Milan score and the remedies around it.",
        "link": "/lk-remedies",
        "stage2_note": "By Day 3, most seekers benefit from reviewing not just the score, but the friction points and the remedies attached to them. The remedy layer often matters as much as the number.",
        "stage3_pitch": "Premium helps you move from match score to full partner-chart context and compatibility timing.",
    },
    "subscription": {
        "focus": "Your Premium access is now live -- explore all modules.",
        "link": "/the-strategist",
        "stage2_note": "The fastest way to feel the value of Premium is to move across modules. Open a second tool this week and compare how the insights connect.",
        "stage3_pitch": "",
    },
    "numerology": {
        "focus": "Your Life Path number is the best place to begin.",
        "link": "/numerology",
        "stage2_note": "Return to your Life Path reading and compare it against your daily choices this week. Numerology becomes far more practical when you read it as timing and behaviour, not only identity.",
        "stage3_pitch": "Premium expands numerology insight into a wider Vedic guidance journey.",
    },
    "longevity": {
        "focus": "Start with Chapter 3 and the Ayurvedic body-type overlay.",
        "link": "/the-longevity-report",
        "stage2_note": "Three days later, the report becomes easier to absorb if you read the constitutional and timing sections together. That usually turns the material into an action plan.",
        "stage3_pitch": "Premium adds more recurring guidance layers around timing, health rhythm, and chart interpretation.",
    },
    "default": {
        "focus": "Log in and explore your dashboard.",
        "link": "/",
        "stage2_note": "Take a second pass through your purchase with fresh eyes. The first read gives orientation; the second usually reveals the instruction hidden inside it.",
        "stage3_pitch": "Premium opens the rest of the temple -- more modules, more timing tools, and continuous guidance.",
    },
}


def _product_meta(product_type: str) -> dict[str, str]:
    return PRODUCT_CONTENT.get(product_type, PRODUCT_CONTENT["default"])


def _public_base_url() -> str:
    return (
        os.environ.get("FRONTEND_URL")
        or os.environ.get("PUBLIC_BASE_URL")
        or "https://www.everydayhoroscope.in"
    ).rstrip("/")


def _build_stage_payload(
    *,
    stage_number: int,
    user_name: str,
    product_type: str,
    product_name: str,
) -> tuple[str, str]:
    meta = _product_meta(product_type)
    base_url = _public_base_url()
    link_url = f"{base_url}{meta['link']}"
    user_name = user_name or "Seeker"
    product_name = product_name or "reading"

    if stage_number == 1:
        subject = f"Your {product_name} is ready -- {user_name}"
        html = (
            f"<p>Your order is confirmed. Here is how to access your {product_name}:</p>"
            f'<p><a href="{base_url}">{base_url}</a></p>'
            f"<p><strong>What to focus on:</strong> {meta['focus']}</p>"
            "<p>In alignment,<br/>The EverydayHoroscope Temple</p>"
        )
        return subject, html

    if stage_number == 2:
        subject = f"A deeper read on your {product_name} -- {user_name}"
        html = (
            f"<p>Three days ago, you received your {product_name}.</p>"
            f'<p>Return here: <a href="{link_url}">{link_url}</a></p>'
            f"<p>{meta['stage2_note']}</p>"
            "<p>In alignment,<br/>The EverydayHoroscope Temple</p>"
        )
        return subject, html

    subject = f"What comes after your {product_name} -- {user_name}"
    html = (
        f"<p>Your {product_name} gave you a single window into your cosmic blueprint.</p>"
        "<p>Premium members get the fuller picture -- recurring reports, live transits, and weekly guidance.</p>"
        f"<p>{meta['stage3_pitch']}</p>"
        f'<p><a href="{base_url}/pricing">{base_url}/pricing</a></p>'
        "<p>Current offer: ₹1,599/month · cancel anytime.</p>"
        "<p>In alignment,<br/>The EverydayHoroscope Temple</p>"
    )
    return subject, html


async def _send_custom_email(to_email: str, subject: str, html: str) -> dict[str, Any]:
    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("FROM_EMAIL")
    if not api_key or not from_email:
        return {"status": "skipped", "channel": "email", "error": "Missing RESEND_API_KEY or FROM_EMAIL"}

    payload = {
        "from": from_email,
        "to": [to_email],
        "subject": subject,
        "html": f"<html><body style=\"font-family:Arial,sans-serif;line-height:1.6;color:#111827;\">{html}</body></html>",
        "text": subject,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        response_payload = await asyncio.to_thread(_post_json, RESEND_API_URL, payload=payload, headers=headers)
    except Exception as exc:
        return {"status": "failed", "channel": "email", "error": str(exc)}
    return {
        "status": "sent",
        "channel": "email",
        "error": None,
        "provider": "resend",
        "provider_message_id": response_payload.get("id"),
        "subject": subject,
    }


async def _email_allowed(db, user_email: str) -> bool:
    pref = await db.notification_preferences.find_one(
        {"user_email": user_email},
        {"_id": 0, "channels.email": 1},
    )
    if not pref:
        return True
    channels = pref.get("channels") or {}
    return channels.get("email", True) is True


async def _whatsapp_phone_for(db, user_email: str) -> Optional[str]:
    pref = await db.notification_preferences.find_one(
        {"user_email": user_email},
        {"_id": 0, "whatsapp_phone": 1},
    )
    phone = (pref or {}).get("whatsapp_phone")
    if phone:
        return str(phone)
    subscriber = await db.subscribers.find_one({"email": user_email}, {"_id": 0, "phone": 1})
    return (subscriber or {}).get("phone")


async def _set_stage_status(
    db,
    sequence_id: str,
    stage_key: str,
    *,
    status: str,
    sent_at: Optional[datetime] = None,
    error: Optional[str] = None,
) -> None:
    update: dict[str, Any] = {
        f"stages.{stage_key}.status": status,
        "updated_at": _utc_now(),
    }
    if sent_at is not None:
        update[f"stages.{stage_key}.sent_at"] = sent_at
    if error is not None:
        update[f"stages.{stage_key}.error"] = error
    await db.lifecycle_sequences.update_one({"sequence_id": sequence_id}, {"$set": update})


async def send_stage(db, sequence_id: str, stage_number: int) -> dict[str, Any]:
    sequence = await db.lifecycle_sequences.find_one({"sequence_id": sequence_id}, {"_id": 0})
    if not sequence:
        return {"status": "missing", "sequence_id": sequence_id}

    stage_key = f"stage_{stage_number}"
    if sequence.get("cancelled"):
        await _set_stage_status(db, sequence_id, stage_key, status="skipped", error="Sequence cancelled")
        return {"status": "skipped", "reason": "cancelled"}
    if sequence.get("unsubscribed"):
        await _set_stage_status(db, sequence_id, stage_key, status="skipped", error="User unsubscribed")
        return {"status": "skipped", "reason": "unsubscribed"}
    if stage_number == 3 and sequence.get("product_type") == "subscription":
        await _set_stage_status(db, sequence_id, stage_key, status="skipped", error="Subscription upsell skipped")
        return {"status": "skipped", "reason": "subscription_no_upsell"}

    subject, html = _build_stage_payload(
        stage_number=stage_number,
        user_name=sequence.get("user_name") or "Seeker",
        product_type=sequence.get("product_type") or "default",
        product_name=sequence.get("product_name") or "reading",
    )

    email_allowed = await _email_allowed(db, sequence.get("user_email", ""))
    if not email_allowed:
        await db.lifecycle_sequences.update_one(
            {"sequence_id": sequence_id},
            {"$set": {"unsubscribed": True, "updated_at": _utc_now()}},
        )
        await _set_stage_status(db, sequence_id, stage_key, status="skipped", error="Email opt-out")
        return {"status": "skipped", "reason": "email_opt_out"}

    email_result = await _send_custom_email(sequence["user_email"], subject, html)
    sent_at = _utc_now()
    if email_result.get("status") == "sent":
        await _set_stage_status(db, sequence_id, stage_key, status="sent", sent_at=sent_at)
    else:
        await _set_stage_status(
            db,
            sequence_id,
            stage_key,
            status="failed",
            sent_at=sent_at,
            error=email_result.get("error"),
        )
    return email_result


async def run_lifecycle_stage(sequence_id: str, stage_number: int) -> dict[str, Any]:
    if _DB is None:
        return {"status": "failed", "error": "Lifecycle DB runtime not configured"}
    return await send_stage(_DB, sequence_id, stage_number)


async def create_sequence(
    db,
    *,
    user_email: str,
    user_name: str,
    product_type: str,
    product_name: str,
    payment_id: str,
) -> dict[str, Any]:
    sequence_id = str(uuid.uuid4())
    now = _utc_now()
    stage_2_time = now + timedelta(days=3)
    stage_3_time = now + timedelta(days=7)
    unsubscribed = not await _email_allowed(db, user_email)

    document = {
        "sequence_id": sequence_id,
        "user_email": user_email,
        "user_name": user_name or "Seeker",
        "product_type": product_type or "default",
        "product_name": product_name or "reading",
        "payment_id": payment_id,
        "started_at": now,
        "updated_at": now,
        "cancelled": False,
        "unsubscribed": unsubscribed,
        "stages": {
            "stage_1": {"status": "pending", "sent_at": None},
            "stage_2": {"status": "pending", "scheduled_at": stage_2_time, "sent_at": None},
            "stage_3": {
                "status": "skipped" if product_type == "subscription" else "pending",
                "scheduled_at": stage_3_time,
                "sent_at": None,
            },
        },
    }
    await db.lifecycle_sequences.insert_one(document)

    if _SCHEDULER is not None:
        _SCHEDULER.add_job(
            run_lifecycle_stage,
            "date",
            run_date=stage_2_time,
            args=[sequence_id, 2],
            id=f"lifecycle_{sequence_id}_stage2",
            replace_existing=True,
        )
        if product_type != "subscription":
            _SCHEDULER.add_job(
                run_lifecycle_stage,
                "date",
                run_date=stage_3_time,
                args=[sequence_id, 3],
                id=f"lifecycle_{sequence_id}_stage3",
                replace_existing=True,
            )

    await send_stage(db, sequence_id, 1)
    return document


def remove_scheduled_jobs(sequence_id: str) -> None:
    if _SCHEDULER is None:
        return
    for stage_number in (2, 3):
        job_id = f"lifecycle_{sequence_id}_stage{stage_number}"
        try:
            _SCHEDULER.remove_job(job_id)
        except Exception:
            continue


async def cancel_sequence(db, sequence_id: str) -> bool:
    remove_scheduled_jobs(sequence_id)
    result = await db.lifecycle_sequences.update_one(
        {"sequence_id": sequence_id},
        {"$set": {"cancelled": True, "updated_at": _utc_now()}},
    )
    return result.matched_count > 0


async def list_sequences(db, status: str = "all", limit: int = 100) -> list[dict[str, Any]]:
    rows = await db.lifecycle_sequences.find({}, {"_id": 0}).sort("started_at", -1).limit(limit).to_list(limit)
    filtered: list[dict[str, Any]] = []
    for row in rows:
        cancelled = bool(row.get("cancelled"))
        stage_statuses = [((row.get("stages") or {}).get(stage) or {}).get("status") for stage in ("stage_1", "stage_2", "stage_3")]
        is_completed = all(status_value in {"sent", "failed", "skipped"} for status_value in stage_statuses if status_value)
        derived_status = "cancelled" if cancelled else "completed" if is_completed else "active"
        if status != "all" and derived_status != status:
            continue
        row["derived_status"] = derived_status
        filtered.append(row)
    return filtered
