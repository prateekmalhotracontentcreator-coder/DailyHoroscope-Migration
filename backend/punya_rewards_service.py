from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import HTTPException


IST = ZoneInfo("Asia/Kolkata")

PUNYA_CONFIG_KEY = "default"
PUNYA_ACCOUNT_COLLECTION = "punya_accounts"
PUNYA_TRANSACTION_COLLECTION = "punya_transactions"
PUNYA_SPIN_COLLECTION = "punya_spins"
PUNYA_CONFIG_COLLECTION = "punya_config"

DEFAULT_ACTION_RULES: dict[str, dict[str, Any]] = {
    "horoscope_daily_view": {
        "label": "Daily Horoscope check",
        "module": "horoscope",
        "points": 5,
        "cap_window": "day",
        "cap_count": 1,
        "enabled": True,
    },
    "horoscope_weekly_view": {
        "label": "Weekly Horoscope check",
        "module": "horoscope",
        "points": 10,
        "cap_window": "week",
        "cap_count": 1,
        "enabled": True,
    },
    "horoscope_monthly_view": {
        "label": "Monthly Horoscope check",
        "module": "horoscope",
        "points": 15,
        "cap_window": "month",
        "cap_count": 1,
        "enabled": True,
    },
    "panchang_daily_view": {
        "label": "Daily Panchang view",
        "module": "panchang",
        "points": 5,
        "cap_window": "day",
        "cap_count": 1,
        "enabled": True,
    },
    "tarot_daily_draw": {
        "label": "Daily Tarot draw",
        "module": "tarot",
        "points": 10,
        "cap_window": "day",
        "cap_count": 1,
        "enabled": True,
    },
    "tarot_spread_complete": {
        "label": "Tarot spread complete",
        "module": "tarot",
        "points": 25,
        "cap_window": "day",
        "cap_count": 1,
        "enabled": True,
    },
    "tarot_bookmark": {
        "label": "Bookmark a Tarot reading",
        "module": "tarot",
        "points": 5,
        "cap_window": "reference",
        "cap_count": 1,
        "enabled": True,
    },
    "numerology_report_generate": {
        "label": "Generate Numerology report",
        "module": "numerology",
        "points": 20,
        "cap_window": "reference",
        "cap_count": 1,
        "enabled": True,
    },
    "birth_chart_generate": {
        "label": "Generate Birth Chart or Kundali",
        "module": "kundali",
        "points": 30,
        "cap_window": "reference",
        "cap_count": 1,
        "enabled": True,
    },
    "share_card": {
        "label": "Share a card",
        "module": "shared",
        "points": 10,
        "cap_window": "day",
        "cap_count": 3,
        "enabled": True,
    },
}

DEFAULT_WHEEL_SEGMENTS: list[dict[str, Any]] = [
    {
        "segment_id": "discount_10",
        "label": "10% off next premium report",
        "prize_type": "coupon",
        "prize_value": "PUNYA10",
        "weight": 20,
        "active": True,
    },
    {
        "segment_id": "free_tarot_spread",
        "label": "Free Tarot spread",
        "prize_type": "unlock",
        "prize_value": "tarot_spread",
        "weight": 15,
        "active": True,
    },
    {
        "segment_id": "bonus_50_points",
        "label": "+50 Punya Points",
        "prize_type": "points",
        "prize_value": 50,
        "weight": 20,
        "active": True,
    },
    {
        "segment_id": "free_numerology",
        "label": "Free Numerology report",
        "prize_type": "unlock",
        "prize_value": "numerology_report",
        "weight": 10,
        "active": True,
    },
    {
        "segment_id": "bonus_100_points",
        "label": "+100 Punya Points",
        "prize_type": "points",
        "prize_value": 100,
        "weight": 10,
        "active": True,
    },
    {
        "segment_id": "discount_20_subscription",
        "label": "20% off subscription",
        "prize_type": "coupon",
        "prize_value": "PUNYA20",
        "weight": 8,
        "active": True,
    },
    {
        "segment_id": "free_birth_chart_pdf",
        "label": "Free Birth Chart PDF",
        "prize_type": "unlock",
        "prize_value": "birth_chart_pdf",
        "weight": 10,
        "active": True,
    },
    {
        "segment_id": "try_again",
        "label": "Try Again Tomorrow",
        "prize_type": "soft_loss",
        "prize_value": None,
        "weight": 7,
        "active": True,
    },
]

DEFAULT_STREAK_MILESTONES: list[dict[str, int]] = [
    {"days": 7, "points": 50},
    {"days": 30, "points": 200},
    {"days": 90, "points": 500},
]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _ist_now() -> datetime:
    return _utc_now().astimezone(IST)


def _ist_date_key(moment: datetime | None = None) -> str:
    current = moment.astimezone(IST) if moment else _ist_now()
    return current.date().isoformat()


def _ist_week_key(moment: datetime | None = None) -> str:
    current = moment.astimezone(IST) if moment else _ist_now()
    monday = current.date() - timedelta(days=current.weekday())
    return monday.isoformat()


def _ist_month_key(moment: datetime | None = None) -> str:
    current = moment.astimezone(IST) if moment else _ist_now()
    return f"{current.year:04d}-{current.month:02d}"


def _window_key(cap_window: str | None, now_utc: datetime) -> str | None:
    if cap_window == "day":
        return _ist_date_key(now_utc)
    if cap_window == "week":
        return _ist_week_key(now_utc)
    if cap_window == "month":
        return _ist_month_key(now_utc)
    return None


def _week_bounds_utc(moment: datetime | None = None) -> tuple[datetime, datetime]:
    current_ist = moment.astimezone(IST) if moment else _ist_now()
    monday_ist = datetime.combine(
        current_ist.date() - timedelta(days=current_ist.weekday()),
        datetime.min.time(),
        tzinfo=IST,
    )
    next_monday_ist = monday_ist + timedelta(days=7)
    return monday_ist.astimezone(timezone.utc), next_monday_ist.astimezone(timezone.utc)


async def ensure_punya_config(db) -> dict[str, Any]:
    collection = getattr(db, PUNYA_CONFIG_COLLECTION)
    existing = await collection.find_one({"config_key": PUNYA_CONFIG_KEY}, {"_id": 0})
    if existing:
        return existing

    now = _utc_now()
    config = {
        "config_key": PUNYA_CONFIG_KEY,
        "currency_name": "Punya Points",
        "spin_cost_points": 50,
        "daily_free_spin_enabled": True,
        "leaderboard_reset": "monday_ist",
        "wheel_segments": DEFAULT_WHEEL_SEGMENTS,
        "action_rules": DEFAULT_ACTION_RULES,
        "login_streak_milestones": DEFAULT_STREAK_MILESTONES,
        "created_at": now,
        "updated_at": now,
    }
    await collection.insert_one(config)
    return {**config}


async def get_punya_config(db) -> dict[str, Any]:
    config = await ensure_punya_config(db)
    config.pop("_id", None)
    return config


async def update_punya_config(db, payload: dict[str, Any]) -> dict[str, Any]:
    current = await get_punya_config(db)
    updated = {
        **current,
        **payload,
        "config_key": PUNYA_CONFIG_KEY,
        "currency_name": "Punya Points",
        "updated_at": _utc_now(),
    }
    await getattr(db, PUNYA_CONFIG_COLLECTION).update_one(
        {"config_key": PUNYA_CONFIG_KEY},
        {"$set": updated},
        upsert=True,
    )
    return updated


async def ensure_punya_account(
    db,
    *,
    user_id: str,
    user_email: str,
    user_name: str | None = None,
) -> dict[str, Any]:
    collection = getattr(db, PUNYA_ACCOUNT_COLLECTION)
    existing = await collection.find_one({"user_id": user_id})
    if existing:
        updates: dict[str, Any] = {}
        if user_email and existing.get("user_email") != user_email:
            updates["user_email"] = user_email
        if user_name and existing.get("user_name") != user_name:
            updates["user_name"] = user_name
        if updates:
            updates["updated_at"] = _utc_now()
            await collection.update_one({"user_id": user_id}, {"$set": updates})
            existing.update(updates)
        existing.pop("_id", None)
        return existing

    now = _utc_now()
    account = {
        "user_id": user_id,
        "user_email": user_email,
        "user_name": user_name or "",
        "balance": 0,
        "lifetime_earned": 0,
        "lifetime_spent": 0,
        "login_streak": 0,
        "last_login_date": None,
        "daily_free_spin_used": None,
        "created_at": now,
        "updated_at": now,
    }
    await collection.insert_one(account)
    return account


async def _append_transaction(
    db,
    *,
    user_id: str,
    user_email: str,
    direction: str,
    amount: int,
    reason_code: str,
    module: str,
    reference_id: str | None = None,
    claim_window: str | None = None,
    claim_window_key: str | None = None,
    claim_reference_id: str | None = None,
    claim_key: str | None = None,
    metadata: dict[str, Any] | None = None,
    transaction_type: str = "action_reward",
) -> dict[str, Any]:
    accounts = getattr(db, PUNYA_ACCOUNT_COLLECTION)
    transactions = getattr(db, PUNYA_TRANSACTION_COLLECTION)

    account = await ensure_punya_account(db, user_id=user_id, user_email=user_email)
    balance_before = int(account.get("balance") or 0)
    delta = amount if direction == "credit" else -amount
    balance_after = balance_before + delta
    if balance_after < 0:
        raise HTTPException(status_code=400, detail="Insufficient Punya Points.")

    now = _utc_now()
    document = {
        "transaction_id": f"punya_txn_{uuid4().hex}",
        "user_id": user_id,
        "user_email": user_email,
        "direction": direction,
        "amount": amount,
        "delta": delta,
        "balance_before": balance_before,
        "balance_after": balance_after,
        "transaction_type": transaction_type,
        "reason_code": reason_code,
        "module": module,
        "reference_id": reference_id,
        "claim_window": claim_window,
        "claim_window_key": claim_window_key,
        "claim_reference_id": claim_reference_id,
        "claim_key": claim_key,
        "metadata": metadata or {},
        "created_at": now,
    }
    await transactions.insert_one(document)

    set_fields = {"balance": balance_after, "updated_at": now}
    increment = {}
    if direction == "credit":
        increment["lifetime_earned"] = amount
    else:
        increment["lifetime_spent"] = amount
    await accounts.update_one({"user_id": user_id}, {"$set": set_fields, "$inc": increment})

    document.pop("_id", None)
    return document


def _claim_query_for_rule(
    *,
    user_id: str,
    action_code: str,
    cap_window: str | None,
    window_key: str | None,
    reference_id: str | None,
) -> dict[str, Any]:
    query = {"user_id": user_id, "reason_code": action_code, "transaction_type": "action_reward"}
    if cap_window == "reference":
        query["claim_reference_id"] = reference_id
    elif cap_window in {"day", "week", "month"}:
        query["claim_window_key"] = window_key
    return query


async def award_punya_action(
    db,
    *,
    user_id: str,
    user_email: str,
    action_code: str,
    reference_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = await get_punya_config(db)
    rule = (config.get("action_rules") or {}).get(action_code)
    if not rule or not rule.get("enabled", True):
        return {"awarded": False, "reason": "disabled", "amount": 0}

    if action_code not in DEFAULT_ACTION_RULES:
        return {"awarded": False, "reason": "unknown_action", "amount": 0}

    amount = int(rule.get("points") or 0)
    if amount <= 0:
        return {"awarded": False, "reason": "zero_value", "amount": 0}

    now = _utc_now()
    cap_window = rule.get("cap_window")
    cap_count = int(rule.get("cap_count") or 1)
    window_key = _window_key(cap_window, now)
    claim_query = _claim_query_for_rule(
        user_id=user_id,
        action_code=action_code,
        cap_window=cap_window,
        window_key=window_key,
        reference_id=reference_id,
    )

    if cap_window == "reference" and not reference_id:
        raise HTTPException(status_code=400, detail=f"{action_code} requires a reference_id.")

    existing_count = await getattr(db, PUNYA_TRANSACTION_COLLECTION).count_documents(claim_query)
    if existing_count >= cap_count:
        return {"awarded": False, "reason": "cap_reached", "amount": 0}

    claim_key = None
    if cap_count == 1:
        if cap_window == "reference":
            claim_key = f"{action_code}:{reference_id}"
        elif window_key:
            claim_key = f"{action_code}:{window_key}"

    document = await _append_transaction(
        db,
        user_id=user_id,
        user_email=user_email,
        direction="credit",
        amount=amount,
        reason_code=action_code,
        module=str(rule.get("module") or "shared"),
        reference_id=reference_id,
        claim_window=cap_window,
        claim_window_key=window_key,
        claim_reference_id=reference_id if cap_window == "reference" else None,
        claim_key=claim_key,
        metadata=metadata,
        transaction_type="action_reward",
    )
    return {
        "awarded": True,
        "amount": amount,
        "balance_after": document["balance_after"],
        "transaction_id": document["transaction_id"],
    }


async def adjust_punya_balance(
    db,
    *,
    user_id: str,
    user_email: str,
    amount: int,
    note: str,
    admin_actor: str,
) -> dict[str, Any]:
    direction = "credit" if amount >= 0 else "debit"
    absolute_amount = abs(int(amount))
    if absolute_amount == 0:
        raise HTTPException(status_code=400, detail="Adjustment amount must be non-zero.")
    return await _append_transaction(
        db,
        user_id=user_id,
        user_email=user_email,
        direction=direction,
        amount=absolute_amount,
        reason_code="admin_adjustment",
        module="admin",
        metadata={"note": note, "admin_actor": admin_actor},
        transaction_type="admin_adjustment",
    )


async def spend_punya_points(
    db,
    *,
    user_id: str,
    user_email: str,
    amount: int,
    reason_code: str,
    module: str,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return await _append_transaction(
        db,
        user_id=user_id,
        user_email=user_email,
        direction="debit",
        amount=amount,
        reason_code=reason_code,
        module=module,
        metadata=metadata,
        transaction_type="spend",
    )


async def grant_punya_points(
    db,
    *,
    user_id: str,
    user_email: str,
    amount: int,
    reason_code: str,
    module: str,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return await _append_transaction(
        db,
        user_id=user_id,
        user_email=user_email,
        direction="credit",
        amount=amount,
        reason_code=reason_code,
        module=module,
        metadata=metadata,
        transaction_type="system_credit",
    )


async def record_login_streak(
    db,
    *,
    user_id: str,
    user_email: str,
    user_name: str | None = None,
) -> dict[str, Any]:
    config = await get_punya_config(db)
    account = await ensure_punya_account(db, user_id=user_id, user_email=user_email, user_name=user_name)
    today_key = _ist_date_key()
    last_login_key = account.get("last_login_date")
    current_streak = int(account.get("login_streak") or 0)

    if last_login_key == today_key:
        return {"streak": current_streak, "awards": []}

    previous_date = None
    if last_login_key:
        try:
            previous_date = datetime.fromisoformat(f"{last_login_key}T00:00:00+05:30").date()
        except ValueError:
            previous_date = None

    today_date = _ist_now().date()
    if previous_date and previous_date == (today_date - timedelta(days=1)):
        next_streak = current_streak + 1
    else:
        next_streak = 1

    await getattr(db, PUNYA_ACCOUNT_COLLECTION).update_one(
        {"user_id": user_id},
        {"$set": {"login_streak": next_streak, "last_login_date": today_key, "updated_at": _utc_now()}},
    )

    awards = []
    milestones = config.get("login_streak_milestones") or DEFAULT_STREAK_MILESTONES
    for milestone in milestones:
        days = int(milestone.get("days") or 0)
        points = int(milestone.get("points") or 0)
        if days == next_streak and points > 0:
            transaction = await grant_punya_points(
                db,
                user_id=user_id,
                user_email=user_email,
                amount=points,
                reason_code=f"login_streak_{days}",
                module="auth",
                metadata={"streak_days": days, "streak_date": today_key},
            )
            awards.append(
                {
                    "days": days,
                    "points": points,
                    "transaction_id": transaction["transaction_id"],
                }
            )

    return {"streak": next_streak, "awards": awards}


async def get_user_punya_summary(
    db,
    *,
    user_id: str,
    user_email: str,
    user_name: str | None = None,
) -> dict[str, Any]:
    config = await get_punya_config(db)
    account = await ensure_punya_account(db, user_id=user_id, user_email=user_email, user_name=user_name)
    today_key = _ist_date_key()
    leaderboard = await get_punya_leaderboard(db, limit=10)
    public_segments = [
        {
            "segment_id": segment.get("segment_id"),
            "label": segment.get("label"),
            "prize_type": segment.get("prize_type"),
            "prize_value": segment.get("prize_value"),
        }
        for segment in (config.get("wheel_segments") or [])
        if segment.get("active", True)
    ]
    return {
        "currency_name": config.get("currency_name", "Punya Points"),
        "balance": int(account.get("balance") or 0),
        "lifetime_earned": int(account.get("lifetime_earned") or 0),
        "lifetime_spent": int(account.get("lifetime_spent") or 0),
        "login_streak": int(account.get("login_streak") or 0),
        "last_login_date": account.get("last_login_date"),
        "daily_free_spin_available": config.get("daily_free_spin_enabled", True)
        and account.get("daily_free_spin_used") != today_key,
        "daily_free_spin_used": account.get("daily_free_spin_used"),
        "spin_cost_points": int(config.get("spin_cost_points") or 50),
        "wheel_segments": public_segments,
        "leaderboard": leaderboard,
    }


async def get_user_punya_ledger(
    db,
    *,
    user_id: str,
    limit: int = 30,
) -> list[dict[str, Any]]:
    cursor = getattr(db, PUNYA_TRANSACTION_COLLECTION).find(
        {"user_id": user_id},
        {"_id": 0},
    ).sort("created_at", -1).limit(limit)
    rows = await cursor.to_list(length=limit)
    return rows


async def get_user_spin_history(
    db,
    *,
    user_id: str,
    limit: int = 20,
) -> list[dict[str, Any]]:
    cursor = getattr(db, PUNYA_SPIN_COLLECTION).find(
        {"user_id": user_id},
        {"_id": 0},
    ).sort("created_at", -1).limit(limit)
    rows = await cursor.to_list(length=limit)
    return rows


def _pick_weighted_segment(segments: list[dict[str, Any]]) -> dict[str, Any]:
    weighted = [segment for segment in segments if segment.get("active", True) and int(segment.get("weight") or 0) > 0]
    if not weighted:
        raise HTTPException(status_code=400, detail="No active wheel segments are configured.")
    weights = [int(segment.get("weight") or 0) for segment in weighted]
    return random.choices(weighted, weights=weights, k=1)[0]


async def spin_punya_wheel(
    db,
    *,
    user_id: str,
    user_email: str,
    spin_mode: str = "auto",
) -> dict[str, Any]:
    config = await get_punya_config(db)
    account = await ensure_punya_account(db, user_id=user_id, user_email=user_email)
    today_key = _ist_date_key()
    free_available = config.get("daily_free_spin_enabled", True) and account.get("daily_free_spin_used") != today_key

    if spin_mode not in {"auto", "free", "paid"}:
        raise HTTPException(status_code=400, detail="spin_mode must be auto, free, or paid.")

    use_free = free_available and spin_mode in {"auto", "free"}
    if spin_mode == "free" and not free_available:
        raise HTTPException(status_code=400, detail="Daily Blessing already used for today.")

    cost_transaction = None
    if not use_free:
        spin_cost = int(config.get("spin_cost_points") or 50)
        cost_transaction = await spend_punya_points(
            db,
            user_id=user_id,
            user_email=user_email,
            amount=spin_cost,
            reason_code="spin_cost",
            module="punya",
            metadata={"spin_mode": spin_mode},
        )

    segment = _pick_weighted_segment(config.get("wheel_segments") or [])
    spin_id = f"punya_spin_{uuid4().hex}"
    prize_transaction = None
    fulfillment: dict[str, Any] = {}

    if segment.get("prize_type") == "points":
        prize_amount = int(segment.get("prize_value") or 0)
        prize_transaction = await grant_punya_points(
            db,
            user_id=user_id,
            user_email=user_email,
            amount=prize_amount,
            reason_code="spin_prize_points",
            module="punya",
            metadata={"spin_id": spin_id, "segment_id": segment.get("segment_id")},
        )
        fulfillment = {
            "status": "granted",
            "points": prize_amount,
            "transaction_id": prize_transaction["transaction_id"],
        }
    elif segment.get("prize_type") in {"coupon", "unlock"}:
        fulfillment = {
            "status": "pending_fulfillment",
            "value": segment.get("prize_value"),
        }
    else:
        fulfillment = {"status": "no_prize"}

    if use_free:
        await getattr(db, PUNYA_ACCOUNT_COLLECTION).update_one(
            {"user_id": user_id},
            {"$set": {"daily_free_spin_used": today_key, "updated_at": _utc_now()}},
        )

    spin_record = {
        "spin_id": spin_id,
        "user_id": user_id,
        "user_email": user_email,
        "is_free_spin": use_free,
        "spin_mode": "free" if use_free else "paid",
        "spin_cost_points": 0 if use_free else int(config.get("spin_cost_points") or 50),
        "cost_transaction_id": cost_transaction["transaction_id"] if cost_transaction else None,
        "segment_id": segment.get("segment_id"),
        "prize_segment": segment.get("label"),
        "prize_type": segment.get("prize_type"),
        "prize_value": segment.get("prize_value"),
        "prize_transaction_id": prize_transaction["transaction_id"] if prize_transaction else None,
        "fulfillment": fulfillment,
        "created_at": _utc_now(),
    }
    await getattr(db, PUNYA_SPIN_COLLECTION).insert_one(spin_record)
    spin_record.pop("_id", None)

    summary = await get_user_punya_summary(db, user_id=user_id, user_email=user_email)
    return {"spin": spin_record, "summary": summary}


async def get_punya_leaderboard(db, limit: int = 10) -> list[dict[str, Any]]:
    week_key = _ist_week_key()
    week_start_utc, week_end_utc = _week_bounds_utc()
    pipeline = [
        {
            "$match": {
                "direction": "credit",
                "transaction_type": {"$in": ["action_reward", "system_credit"]},
                "created_at": {"$gte": week_start_utc, "$lt": week_end_utc},
            }
        },
        {
            "$group": {
                "_id": "$user_id",
                "user_email": {"$first": "$user_email"},
                "weekly_points": {"$sum": "$amount"},
            }
        },
        {"$sort": {"weekly_points": -1, "_id": 1}},
        {"$limit": limit},
    ]
    rows = await getattr(db, PUNYA_TRANSACTION_COLLECTION).aggregate(pipeline).to_list(length=limit)
    accounts = getattr(db, PUNYA_ACCOUNT_COLLECTION)
    leaderboard = []
    for index, row in enumerate(rows, start=1):
        account = await accounts.find_one({"user_id": row["_id"]}, {"_id": 0, "user_name": 1, "balance": 1})
        leaderboard.append(
            {
                "rank": index,
                "user_id": row["_id"],
                "user_email": row.get("user_email"),
                "user_name": (account or {}).get("user_name") or "Temple User",
                "weekly_points": int(row.get("weekly_points") or 0),
                "balance": int((account or {}).get("balance") or 0),
                "week_start": week_key,
            }
        )
    return leaderboard


async def get_admin_punya_overview(db, *, limit: int = 20) -> dict[str, Any]:
    config = await get_punya_config(db)
    accounts = getattr(db, PUNYA_ACCOUNT_COLLECTION)
    transactions = getattr(db, PUNYA_TRANSACTION_COLLECTION)
    spins = getattr(db, PUNYA_SPIN_COLLECTION)
    total_accounts = await accounts.count_documents({})
    total_transactions = await transactions.count_documents({})
    total_spins = await spins.count_documents({})
    recent_transactions = await transactions.find({}, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(length=limit)
    recent_spins = await spins.find({}, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(length=limit)
    top_accounts = await accounts.find({}, {"_id": 0}).sort("balance", -1).limit(10).to_list(length=10)
    return {
        "config": config,
        "stats": {
            "total_accounts": total_accounts,
            "total_transactions": total_transactions,
            "total_spins": total_spins,
        },
        "top_accounts": top_accounts,
        "recent_transactions": recent_transactions,
        "recent_spins": recent_spins,
        "leaderboard": await get_punya_leaderboard(db, limit=10),
    }
