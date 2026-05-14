from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field

from admin_utils import require_admin
from punya_rewards_service import (
    adjust_punya_balance,
    get_admin_punya_overview,
    get_punya_config,
    get_punya_leaderboard,
    get_user_punya_ledger,
    get_user_punya_summary,
    get_user_spin_history,
    award_punya_action,
    spin_punya_wheel,
    update_punya_config,
)


router = APIRouter(tags=["punya-rewards"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PunyaActionClaimRequest(StrictModel):
    action_code: str
    reference_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class PunyaSpinRequest(StrictModel):
    spin_mode: Literal["auto", "free", "paid"] = "auto"


class PunyaAdminAdjustRequest(StrictModel):
    user_id: str
    user_email: str
    amount: int
    note: str


class PunyaConfigUpdateRequest(StrictModel):
    spin_cost_points: int | None = None
    daily_free_spin_enabled: bool | None = None
    wheel_segments: list[dict[str, Any]] | None = None
    action_rules: dict[str, dict[str, Any]] | None = None
    login_streak_milestones: list[dict[str, int]] | None = None


def _get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")
    return db


def _get_user_identity(request: Request) -> tuple[str, str, str]:
    user = getattr(request.state, "user", None)
    if not isinstance(user, dict):
        raise HTTPException(status_code=401, detail="Authentication required")
    user_id = str(user.get("user_id") or "").strip()
    user_email = str(user.get("email") or "").strip()
    user_name = str(user.get("name") or "").strip()
    if not user_id or not user_email:
        raise HTTPException(status_code=401, detail="Authenticated user identity unavailable")
    return user_id, user_email, user_name


@router.get("/api/punya/config/public")
async def get_public_punya_config(request: Request):
    config = await get_punya_config(_get_db(request))
    return {
        "currency_name": config.get("currency_name", "Punya Points"),
        "spin_cost_points": config.get("spin_cost_points", 50),
        "daily_free_spin_enabled": config.get("daily_free_spin_enabled", True),
        "wheel_segments": [
            {
                "segment_id": segment.get("segment_id"),
                "label": segment.get("label"),
                "prize_type": segment.get("prize_type"),
                "prize_value": segment.get("prize_value"),
            }
            for segment in (config.get("wheel_segments") or [])
            if segment.get("active", True)
        ],
        "action_rules": config.get("action_rules") or {},
    }


@router.get("/api/punya/summary")
async def get_punya_summary(request: Request):
    user_id, user_email, user_name = _get_user_identity(request)
    return await get_user_punya_summary(_get_db(request), user_id=user_id, user_email=user_email, user_name=user_name)


@router.get("/api/punya/ledger")
async def get_punya_ledger(request: Request, limit: int = Query(default=30, ge=1, le=100)):
    user_id, _, _ = _get_user_identity(request)
    return {"transactions": await get_user_punya_ledger(_get_db(request), user_id=user_id, limit=limit)}


@router.get("/api/punya/spins")
async def get_punya_spins(request: Request, limit: int = Query(default=20, ge=1, le=100)):
    user_id, _, _ = _get_user_identity(request)
    return {"spins": await get_user_spin_history(_get_db(request), user_id=user_id, limit=limit)}


@router.get("/api/punya/leaderboard")
async def get_punya_leaderboard_route(request: Request):
    db = _get_db(request)
    public_config = await get_punya_config(db)
    return {
        "leaderboard": await get_punya_leaderboard(db, limit=10),
        "currency_name": public_config.get("currency_name", "Punya Points"),
    }


@router.post("/api/punya/actions/claim")
async def claim_punya_action(request: Request, payload: PunyaActionClaimRequest):
    user_id, user_email, _ = _get_user_identity(request)
    result = await award_punya_action(
        _get_db(request),
        user_id=user_id,
        user_email=user_email,
        action_code=payload.action_code,
        reference_id=payload.reference_id,
        metadata=payload.metadata,
    )
    return result


@router.post("/api/punya/spin")
async def spin_punya(request: Request, payload: PunyaSpinRequest):
    user_id, user_email, _ = _get_user_identity(request)
    return await spin_punya_wheel(
        _get_db(request),
        user_id=user_id,
        user_email=user_email,
        spin_mode=payload.spin_mode,
    )


@router.get("/api/admin/punya/config")
async def get_admin_punya_config(request: Request):
    db = _get_db(request)
    await require_admin(request, db)
    return await get_punya_config(db)


@router.put("/api/admin/punya/config")
async def put_admin_punya_config(request: Request, payload: PunyaConfigUpdateRequest):
    db = _get_db(request)
    await require_admin(request, db)
    update_payload = {key: value for key, value in payload.model_dump().items() if value is not None}
    return await update_punya_config(db, update_payload)


@router.get("/api/admin/punya/overview")
async def get_admin_punya_overview_route(request: Request, limit: int = Query(default=20, ge=5, le=100)):
    db = _get_db(request)
    await require_admin(request, db)
    return await get_admin_punya_overview(db, limit=limit)


@router.post("/api/admin/punya/adjust")
async def post_admin_punya_adjust(request: Request, payload: PunyaAdminAdjustRequest):
    db = _get_db(request)
    await require_admin(request, db)
    admin_actor = "admin"
    admin_session = getattr(request.state, "admin", None)
    if isinstance(admin_session, dict):
        admin_actor = str(admin_session.get("username") or "admin")
    return await adjust_punya_balance(
        db,
        user_id=payload.user_id,
        user_email=payload.user_email,
        amount=payload.amount,
        note=payload.note,
        admin_actor=admin_actor,
    )
