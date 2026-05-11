from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from lk_diagnostics import run_full_diagnosis
from strategist_engine import (
    DIGBALA_DIRECTIONS,
    SCIENCE_ID,
    calculate_conquest_probability,
    get_active_hurdles,
    get_active_missions,
    get_surrogate,
)
from vedic_shared_utils import get_db, get_user_email

router = APIRouter(prefix="/api/strategist", tags=["strategist"])


def _get_command_planet(natal_chart: dict) -> str:
    """Return the Lagna lord as the command planet (Sun fallback)."""
    asc_house = natal_chart.get("Ascendant", 1)
    house_lords = {
        1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon", 5: "Sun",
        6: "Mercury", 7: "Venus", 8: "Mars", 9: "Jupiter", 10: "Saturn",
        11: "Saturn", 12: "Jupiter",
    }
    return house_lords.get(asc_house, "Sun")


async def _build_war_room_state(db, user_email: str) -> dict:
    profile = await db.lk_user_profiles.find_one({"user_id": user_email}, {"_id": 0})
    if not profile:
        return {"error": "LK profile missing — complete /api/lk/onboard first"}

    natal_chart = profile.get("natal_chart", {})
    age = profile.get("age", 30)

    # Pull cached diagnose or run fresh
    cached = await db.lk_diagnose_cache.find_one({"user_id": user_email}, {"_id": 0})
    if cached:
        diagnosis = cached.get("result", {})
    else:
        diagnosis = await run_full_diagnosis(db, profile)

    gate1 = diagnosis.get("gates", {}).get("gate1_karmic_debt", {})
    active_pitru_rin = gate1.get("active_pitru_rin", False)

    # Tracker streak
    tracker = await db.lk_tracker.find_one(
        {"user_id": user_email, "status": "active"},
        {"streak_days": 1, "remedy_id": 1, "_id": 0},
    )
    ritual_streak = tracker.get("streak_days", 0) if tracker else 0

    # Command planet + Digbala
    command_planet = _get_command_planet(natal_chart)
    success_direction = DIGBALA_DIRECTIONS.get(command_planet, "North")
    location_slug = profile.get("location_slug", "")

    # Surrogate active check
    surrogate_active = False
    family_census = profile.get("family_census", {})
    if active_pitru_rin:
        for rel, status in family_census.items():
            if status in ("deceased", "unknown"):
                surrogate = await get_surrogate(command_planet, rel, "", db)
                if surrogate:
                    surrogate_active = True
                    break

    user_data = {
        "command_planet_strength": 1.0,
        "office_location": location_slug,
        "success_direction": success_direction,
        "active_pitru_rin": active_pitru_rin,
        "surrogate_active": surrogate_active,
        "ritual_streak": ritual_streak,
    }
    transit_data = {"primary_planet_degree": 15}

    prob = calculate_conquest_probability(user_data, transit_data)
    missions = await get_active_missions(natal_chart, {}, db)
    hurdles = await get_active_hurdles(db)

    return {
        "user_id": user_email,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "command_planet": command_planet,
        "success_direction": success_direction,
        "conquest_probability": prob,
        "active_missions_count": len(missions),
        "active_hurdles_count": len(hurdles),
        "ritual_streak": ritual_streak,
        "diagnosis_summary": {
            "pitru_rin_active": active_pitru_rin,
            "year_lord": diagnosis.get("gates", {}).get("gate3_year_cycle", {}).get("planet", ""),
        },
    }


@router.get("/dashboard")
async def dashboard(request: Request):
    db = get_db(request)
    user_email = get_user_email(request)
    state = await _build_war_room_state(db, user_email)
    return state


class MissionsRequest(BaseModel):
    user_id: Optional[str] = None
    date: Optional[str] = None


@router.post("/missions")
async def missions(body: MissionsRequest, request: Request):
    db = get_db(request)
    user_email = get_user_email(request)
    uid = body.user_id or user_email

    profile = await db.lk_user_profiles.find_one({"user_id": uid}, {"_id": 0})
    natal_chart = profile.get("natal_chart", {}) if profile else {}

    active = await get_active_missions(natal_chart, {}, db)
    return {"user_id": uid, "date": body.date, "missions": active, "count": len(active)}


class HurdlesRequest(BaseModel):
    user_id: Optional[str] = None


@router.post("/hurdles")
async def hurdles(body: HurdlesRequest, request: Request):
    db = get_db(request)
    get_user_email(request)
    active = await get_active_hurdles(db)
    return {"hurdles": active, "count": len(active)}


class ProbabilityRequest(BaseModel):
    user_id: Optional[str] = None
    office_location: Optional[str] = None
    command_planet_strength: Optional[float] = None


@router.post("/probability")
async def probability(body: ProbabilityRequest, request: Request):
    db = get_db(request)
    user_email = get_user_email(request)
    uid = body.user_id or user_email

    profile = await db.lk_user_profiles.find_one({"user_id": uid}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="LK profile not found.")

    natal_chart = profile.get("natal_chart", {})
    command_planet = _get_command_planet(natal_chart)
    success_direction = DIGBALA_DIRECTIONS.get(command_planet, "North")

    cached = await db.lk_diagnose_cache.find_one({"user_id": uid}, {"_id": 0})
    gate1 = cached.get("result", {}).get("gates", {}).get("gate1_karmic_debt", {}) if cached else {}
    active_pitru_rin = gate1.get("active_pitru_rin", False)

    tracker = await db.lk_tracker.find_one({"user_id": uid, "status": "active"}, {"streak_days": 1, "_id": 0})
    streak = tracker.get("streak_days", 0) if tracker else 0

    user_data = {
        "command_planet_strength": body.command_planet_strength or 1.0,
        "office_location": body.office_location or profile.get("location_slug", ""),
        "success_direction": success_direction,
        "active_pitru_rin": active_pitru_rin,
        "surrogate_active": False,
        "ritual_streak": streak,
    }
    transit_data = {"primary_planet_degree": 15}
    result = calculate_conquest_probability(user_data, transit_data)
    result["command_planet"] = command_planet
    result["success_direction"] = success_direction
    return result


class SurrogateRequest(BaseModel):
    planet: str
    relative_unavailable: str
    industry: str = ""


@router.post("/surrogate")
async def surrogate(body: SurrogateRequest, request: Request):
    db = get_db(request)
    get_user_email(request)
    record = await get_surrogate(body.planet, body.relative_unavailable, body.industry, db)
    if not record:
        raise HTTPException(status_code=404, detail="No surrogate record found for this combination.")
    return {"surrogate": record, "surrogate_active": True}


class Gate0RecordRequest(BaseModel):
    row: int
    col: int
    verdict: str  # "YES" | "WAIT" | "NO" | "PRAY"
    answer_slot: int
    report_id: Optional[str] = None


_GATE0_TTL_DAYS: dict[str, int] = {"YES": 7, "WAIT": 3, "NO": 1, "PRAY": 1}


@router.post("/gate0/record")
async def gate0_record(body: Gate0RecordRequest, request: Request):
    db = get_db(request)
    user_email = get_user_email(request)
    now = datetime.now(timezone.utc)
    ttl = _GATE0_TTL_DAYS.get(body.verdict, 1)
    await db.kp_sessions.insert_one({
        "user_email": user_email,
        "verdict": body.verdict,
        "answer_slot": body.answer_slot,
        "report_id": body.report_id,
        "context": "strategist_gate0",
        "created_at": now,
        "expires_at": now + timedelta(days=ttl),
    })
    return {"recorded": True, "verdict": body.verdict, "expires_in_days": ttl}


@router.get("/gate0/status")
async def gate0_status(request: Request):
    db = get_db(request)
    user_email = get_user_email(request)
    now = datetime.now(timezone.utc)

    last = await db.kp_sessions.find_one(
        {"user_email": user_email, "context": "strategist_gate0", "expires_at": {"$gt": now}},
        sort=[("created_at", -1)],
    )

    if not last:
        return {"status": "required", "last_verdict": None, "conquest_score": None, "can_retest": False}

    verdict = last.get("verdict", "")

    if verdict == "YES":
        return {"status": "clear", "last_verdict": verdict, "conquest_score": None, "can_retest": False}

    if verdict == "WAIT":
        tracker = await db.lk_tracker.find_one(
            {"user_id": user_email, "status": "active"}, {"streak_days": 1, "_id": 0}
        )
        streak = tracker.get("streak_days", 0) if tracker else 0
        if streak > 0:
            return {"status": "clear", "last_verdict": verdict, "conquest_score": None, "can_retest": False}
        return {"status": "wait_active", "last_verdict": verdict, "conquest_score": None, "can_retest": False}

    # NO or PRAY — check conquest score to determine re-test eligibility
    tracker = await db.lk_tracker.find_one(
        {"user_id": user_email, "status": "active"}, {"streak_days": 1, "_id": 0}
    )
    streak = tracker.get("streak_days", 0) if tracker else 0
    prob = calculate_conquest_probability(
        {"command_planet_strength": 1.0, "office_location": "", "success_direction": "",
         "active_pitru_rin": False, "surrogate_active": False, "ritual_streak": streak},
        {"primary_planet_degree": 15},
    )
    score = prob["score"]
    threshold = 60 if verdict == "NO" else 75
    can_retest = score >= threshold

    if can_retest:
        return {"status": "required", "last_verdict": verdict, "conquest_score": score, "can_retest": True}

    blocked = "no_blocked" if verdict == "NO" else "pray_blocked"
    return {"status": blocked, "last_verdict": verdict, "conquest_score": score, "can_retest": False}


@router.get("/report/pdf")
async def report_pdf(request: Request):
    db = get_db(request)
    user_email = get_user_email(request)
    state = await _build_war_room_state(db, user_email)

    html = f"""
    <html><head><style>
    body {{ font-family: Georgia, serif; background: #0a0a0a; color: #c5a059; padding: 40px; }}
    h1 {{ color: #c5a059; border-bottom: 1px solid #c5a059; padding-bottom: 10px; }}
    h2 {{ color: #d4af70; margin-top: 30px; }}
    .score {{ font-size: 48px; font-weight: bold; color: #FFD700; }}
    .section {{ margin: 20px 0; padding: 15px; border: 1px solid #c5a05940; border-radius: 8px; }}
    </style></head><body>
    <h1>Executive Intelligence Brief</h1>
    <p>Generated: {state.get('generated_at', '')}</p>

    <div class="section">
      <h2>I. Conquest Probability</h2>
      <div class="score">{state['conquest_probability']['score']}%</div>
      <p><strong>{state['conquest_probability']['tier']}</strong> — {state['conquest_probability']['directive']}</p>
      <p>{state['conquest_probability']['narrative']}</p>
    </div>

    <div class="section">
      <h2>II. Command Intelligence</h2>
      <p>Command Planet: <strong>{state.get('command_planet', '')}</strong></p>
      <p>Power Direction: <strong>{state.get('success_direction', '')}</strong></p>
      <p>Ritual Streak: <strong>{state.get('ritual_streak', 0)} days</strong></p>
    </div>

    <div class="section">
      <h2>III. Battlefield Status</h2>
      <p>Active Missions: {state.get('active_missions_count', 0)}</p>
      <p>Active Hurdles: {state.get('active_hurdles_count', 0)}</p>
      <p>Pitru Rin Active: {'Yes' if state.get('diagnosis_summary', {}).get('pitru_rin_active') else 'No'}</p>
    </div>
    </body></html>
    """

    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html, media_type="text/html")
