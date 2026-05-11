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

    gates = diagnosis.get("gates", {})
    gate1 = gates.get("gate1_karmic_debt", {})
    gate2 = gates.get("gate2_house_awakening", {})
    gate3 = gates.get("gate3_year_cycle", {})
    gate4 = gates.get("gate4_mercury_scan", {})
    gate5 = gates.get("gate5_geographical", {})
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

    # Last Gate 0 for scoreboard
    now = datetime.now(timezone.utc)
    last_kp = await db.kp_sessions.find_one(
        {"user_email": user_email, "context": "strategist_gate0"},
        sort=[("created_at", -1)],
    )
    gate0_verdict = last_kp.get("verdict") if last_kp else None
    gate0_days_since = None
    if last_kp and last_kp.get("created_at"):
        delta = now - last_kp["created_at"].replace(tzinfo=timezone.utc) if last_kp["created_at"].tzinfo is None else now - last_kp["created_at"]
        gate0_days_since = max(0, delta.days)

    score = prob["score"]
    streak_tier = (
        "No Streak" if ritual_streak == 0 else
        "Building" if ritual_streak < 7 else
        "Momentum" if ritual_streak < 15 else
        "Established" if ritual_streak < 30 else
        "Iron Discipline"
    )
    if score >= 85:
        next_threshold = None
        next_label = "Sovereign — peak reached"
    elif score >= 75:
        next_threshold = 85
        next_label = "85% — Sovereign Dominance"
    elif score >= 60:
        next_threshold = 75
        next_label = "75% — PRAY gate clears"
    else:
        next_threshold = 60
        next_label = "60% — NO gate clears"

    scoreboard = {
        "conquest_score": score,
        "score_tier": prob["tier"],
        "score_directive": prob["directive"],
        "streak_days": ritual_streak,
        "streak_tier": streak_tier,
        "karmic_debt_cleared": not active_pitru_rin,
        "gate0_last_verdict": gate0_verdict,
        "gate0_days_since": gate0_days_since,
        "next_threshold": next_threshold,
        "next_threshold_label": next_label,
        "points_to_next": (next_threshold - score) if next_threshold else 0,
    }

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
            "year_lord": gate3.get("planet", ""),
        },
        "scoreboard": scoreboard,
        "gate_summaries": [
            {
                "gate": 1,
                "name": "Karmic Debt",
                "status": gate1.get("status", "UNKNOWN"),
                "narrative": gate1.get("narrative", ""),
            },
            {
                "gate": 2,
                "name": "House Awakening",
                "status": gate2.get("status", "UNKNOWN"),
                "narrative": gate2.get("narrative", ""),
                "dormant_count": len(gate2.get("dormant_houses", [])),
            },
            {
                "gate": 3,
                "name": "Year Cycle",
                "status": "ACTIVE",
                "narrative": gate3.get("narrative", ""),
                "planet": gate3.get("planet", ""),
                "age_range": gate3.get("age_range", ""),
            },
            {
                "gate": 4,
                "name": "Mercury Scan",
                "status": gate4.get("status", "UNKNOWN"),
                "narrative": gate4.get("narrative", ""),
            },
            {
                "gate": 5,
                "name": "Geographical",
                "status": "ACTIVE",
                "narrative": gate5.get("narrative", ""),
                "direction": gate5.get("user_direction", ""),
            },
        ],
    }


@router.get("/dashboard")
async def dashboard(request: Request):
    db = get_db(request)
    user_email = get_user_email(request)
    state = await _build_war_room_state(db, user_email)
    return state


@router.get("/action-plan")
async def action_plan(request: Request):
    db = get_db(request)
    user_email = get_user_email(request)
    now = datetime.now(timezone.utc)

    # Profile + diagnosis
    profile = await db.lk_user_profiles.find_one({"user_id": user_email}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="LK profile missing — complete /api/lk/onboard first.")

    natal_chart = profile.get("natal_chart", {})
    age = profile.get("age", 30)

    cached = await db.lk_diagnose_cache.find_one({"user_id": user_email}, {"_id": 0})
    diagnosis = cached.get("result", {}) if cached else await run_full_diagnosis(db, profile)
    gates = diagnosis.get("gates", {})
    gate1 = gates.get("gate1_karmic_debt", {})
    gate4 = gates.get("gate4_mercury_scan", {})
    pitru_rin = gate1.get("active_pitru_rin", False)
    mercury_status = gate4.get("status", "CLEAR")

    # Streak + active remedy
    tracker = await db.lk_tracker.find_one({"user_id": user_email, "status": "active"}, {"_id": 0})
    streak = tracker.get("streak_days", 0) if tracker else 0
    remedy_id = tracker.get("remedy_id") if tracker else None
    active_remedy = None
    if remedy_id:
        rec = await db.knowledge_rules.find_one({"science_id": "jyotish_lk_remedies", "id": remedy_id}, {"_id": 0})
        if rec:
            active_remedy = {
                "remedy_id": remedy_id,
                "rule_text": rec.get("rule_text") or rec.get("ke_inference", ""),
                "planet": rec.get("primary_planet", ""),
                "house": rec.get("house"),
                "streak_days": streak,
            }

    # Gate 0
    last_kp = await db.kp_sessions.find_one(
        {"user_email": user_email, "context": "strategist_gate0"},
        sort=[("created_at", -1)],
    )
    gate0_verdict = last_kp.get("verdict") if last_kp else None
    gate0_days_since = None
    gate0_expired = True
    if last_kp:
        exp = last_kp.get("expires_at")
        if exp:
            exp_aware = exp.replace(tzinfo=timezone.utc) if exp.tzinfo is None else exp
            gate0_expired = now > exp_aware
        created = last_kp.get("created_at")
        if created:
            created_aware = created.replace(tzinfo=timezone.utc) if created.tzinfo is None else created
            gate0_days_since = max(0, (now - created_aware).days)

    # Conquest score
    command_planet = _get_command_planet(natal_chart)
    success_direction = DIGBALA_DIRECTIONS.get(command_planet, "North")
    prob = calculate_conquest_probability(
        {"command_planet_strength": 1.0, "office_location": "", "success_direction": success_direction,
         "active_pitru_rin": pitru_rin, "surrogate_active": False, "ritual_streak": streak},
        {"primary_planet_degree": 15},
    )
    score = prob["score"]

    # Top missions
    missions_list = await get_active_missions(natal_chart, {}, db, limit=3)

    # Priority actions
    actions = []

    if gate0_expired or not gate0_verdict:
        actions.append({
            "priority": 1, "type": "gate0",
            "label": "Gate 0 — Oracle Clearance Required",
            "detail": "Ask Krishna before entering the War Room. No active clearance found.",
            "cta_label": "Enter War Room", "cta_path": "/strategist",
        })
    elif gate0_verdict == "WAIT" and streak == 0:
        actions.append({
            "priority": 1, "type": "remedy",
            "label": "Start LK Tracker — WAIT verdict active",
            "detail": "Oracle asks for patience. Activate your daily remedy streak to unlock the War Room.",
            "cta_label": "Start Tracker", "cta_path": "/lk-remedies/tracker",
        })
    elif gate0_verdict == "NO" and score < 60:
        actions.append({
            "priority": 1, "type": "remedy",
            "label": f"Raise Score to 60% — {60 - score} pts needed",
            "detail": "Oracle blocked entry. Complete remedy cycle to clear the NO gate.",
            "cta_label": "Browse Remedies", "cta_path": "/lk-remedies/remedies",
        })
    elif gate0_verdict == "PRAY" and score < 75:
        actions.append({
            "priority": 1, "type": "surrender",
            "label": f"Full Surrender — {75 - score} pts to re-test",
            "detail": "Complete Mantra practice and LK Debt Audit. Return at 75%.",
            "cta_label": "Mantra Remedies", "cta_path": "/mantra-remedies",
        })

    if pitru_rin:
        actions.append({
            "priority": len(actions) + 1, "type": "debt",
            "label": "Karmic Debt Active — Debt Audit Required",
            "detail": "Ancestral debt is suppressing your score. Run a full LK Debt Audit.",
            "cta_label": "LK Debt Audit", "cta_path": "/lk-remedies/debt-audit",
        })

    if mercury_status in ("EMPTY_VESSEL", "RAHU_COLLISION"):
        actions.append({
            "priority": len(actions) + 1, "type": "mercury",
            "label": f"Mercury Alert — {mercury_status.replace('_', ' ').title()}",
            "detail": gate4.get("narrative", "Mercury configuration requires attention."),
            "cta_label": "LK Remedies", "cta_path": "/lk-remedies/remedies",
        })

    if streak == 0 and not any(a["type"] == "remedy" for a in actions):
        actions.append({
            "priority": len(actions) + 1, "type": "remedy",
            "label": "No Active Remedy Streak",
            "detail": "Begin a daily LK remedy to build Ritual Momentum and raise your Conquest score.",
            "cta_label": "Start Tracker", "cta_path": "/lk-remedies/tracker",
        })

    for m in missions_list:
        actions.append({
            "priority": len(actions) + 1, "type": "mission",
            "label": m.get("title", m.get("trigger_condition", "Active Mission")),
            "detail": m.get("ke_inference") or m.get("rule_text", ""),
            "cta_label": "Mission Board", "cta_path": "/strategist/missions",
        })

    return {
        "generated_at": now.isoformat(),
        "gate0": {"verdict": gate0_verdict, "days_since": gate0_days_since, "expired": gate0_expired},
        "active_remedy": active_remedy,
        "conquest_score": score,
        "score_tier": prob["tier"],
        "score_directive": prob["directive"],
        "streak_days": streak,
        "priority_actions": actions,
    }


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
