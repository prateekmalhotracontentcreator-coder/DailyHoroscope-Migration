from __future__ import annotations

from typing import Any

SCIENCE_ID = "lalkitab_strategist"

DIGBALA_DIRECTIONS: dict[str, str] = {
    "Sun": "South", "Moon": "North", "Mercury": "North",
    "Mars": "South", "Jupiter": "NE", "Venus": "SE",
    "Saturn": "West", "Rahu": "SW", "Ketu": "NW",
}

TRIGGER_MAP: dict[str, Any] = {
    "Transit_Sun_H10":               lambda chart, tr: tr.get("Sun", {}).get("house") == 10,
    "Transit_Saturn_H3":             lambda chart, tr: tr.get("Saturn", {}).get("house") == 3,
    "Transit_Venus_H2_or_H7":        lambda chart, tr: tr.get("Venus", {}).get("house") in (2, 7),
    "Transit_Moon_H12":              lambda chart, tr: tr.get("Moon", {}).get("house") == 12,
    "Transit_Rahu_H6":               lambda chart, tr: tr.get("Rahu", {}).get("house") == 6,
    "Transit_Jupiter_H9":            lambda chart, tr: tr.get("Jupiter", {}).get("house") == 9,
    "Transit_Mars_H1":               lambda chart, tr: tr.get("Mars", {}).get("house") == 1,
    "Transit_Ketu_H8":               lambda chart, tr: tr.get("Ketu", {}).get("house") == 8,
    "Mercury_Retrograde_H2_Shadow":  lambda chart, tr: tr.get("Mercury", {}).get("retrograde") and tr.get("Mercury", {}).get("house") == 2,
    "Planet_Degree_29":              lambda chart, tr: any(p.get("degree", 0) >= 29 for p in tr.values() if isinstance(p, dict)),
    "Transit_Rahu_Conj_Natal_Sun":   lambda chart, tr: abs(tr.get("Rahu", {}).get("longitude", 0) - chart.get("Sun", {}).get("longitude", -999)) < 8,
    "Age 38 Cycle Entry":            lambda chart, tr: True,
}


async def get_active_missions(
    user_natal_chart: dict,
    current_transits: dict,
    db,
    limit: int = 10,
) -> list[dict]:
    missions = await db.knowledge_rules.find(
        {"science_id": SCIENCE_ID},
        {"_id": 0},
    ).to_list(None)

    active = []
    for m in missions:
        trigger = m.get("trigger_condition", "")
        fn = TRIGGER_MAP.get(trigger)
        if fn is None:
            continue
        try:
            if fn(user_natal_chart, current_transits):
                active.append(m)
        except Exception:
            pass
        if len(active) >= limit:
            break

    return active


async def get_active_hurdles(db, limit: int = 5) -> list[dict]:
    hurdles = await db.knowledge_rules.find(
        {"science_id": SCIENCE_ID, "ui_warning": {"$exists": True}},
        {"_id": 0},
    ).limit(limit).to_list(None)
    return hurdles


async def get_surrogate(
    planet: str,
    relative_unavailable: str,
    industry: str,
    db,
) -> dict | None:
    record = await db.knowledge_rules.find_one(
        {
            "science_id": SCIENCE_ID,
            "id": {"$gte": 651, "$lte": 675},
            "$or": [
                {"relative_unavailable": relative_unavailable},
                {"industry": {"$regex": industry, "$options": "i"}},
            ],
        },
        {"_id": 0},
    )
    return record


def calculate_conquest_probability(user_data: dict, transit_data: dict) -> dict:
    score = 50
    factors = []

    strength = user_data.get("command_planet_strength", 1.0)
    if strength > 1.2:
        score += 10
        factors.append({"factor": "Shadbala", "delta": +10, "detail": "Command planet strong"})
    else:
        score -= 5
        factors.append({"factor": "Shadbala", "delta": -5, "detail": "Command planet weak"})

    office_loc = user_data.get("office_location", "")
    success_dir = user_data.get("success_direction", "")
    if office_loc and success_dir and office_loc == success_dir:
        score += 15
        factors.append({"factor": "Digbala", "delta": +15, "detail": "Office aligned with power direction"})
    else:
        score -= 10
        factors.append({"factor": "Digbala", "delta": -10, "detail": "Office not aligned with power direction"})

    if user_data.get("active_pitru_rin"):
        score -= 20
        factors.append({"factor": "Pitru_Rin", "delta": -20, "detail": "Active ancestral debt"})
        if user_data.get("surrogate_active"):
            score += 12
            factors.append({"factor": "Surrogate_Bridge", "delta": +12, "detail": "Surrogate ritual active"})

    deg = transit_data.get("primary_planet_degree", 0)
    if 25 <= deg <= 28:
        score += 5
        factors.append({"factor": "Transit_Peak", "delta": +5, "detail": f"Planet at peak degree {deg}°"})

    streak = user_data.get("ritual_streak", 0)
    if streak >= 7:
        score += 10
        factors.append({"factor": "Ritual_Momentum", "delta": +10, "detail": f"Streak {streak} days"})
    elif streak == 0:
        score -= 15
        factors.append({"factor": "No_Ritual", "delta": -15, "detail": "No ritual streak"})

    score = max(0, min(99, score))

    if score >= 85:
        tier = "Sovereign Dominance"
        directive = "Expansion / All-In"
        narrative = "Strategic Sovereign: Empire in high-alignment. Execute Expansion mission immediately."
    elif score >= 60:
        tier = "Operational Friction"
        directive = "Patch & Pivot"
        narrative = "Tactical Friction: Moderate resistance detected. Settle Mercury debts before next bid."
    elif score >= 40:
        tier = "Strategic Siege"
        directive = "Hold Ground / Remedy"
        narrative = "Siege Mode: Do not expand. Reinforce existing positions and activate remedy cycle."
    else:
        tier = "Karmic Lockdown"
        directive = "Withdraw / Full Reset"
        narrative = "Karmic Lockdown: High karmic friction. Withdraw from offensive marketing. Focus Internal Fortress."

    return {
        "score": score,
        "tier": tier,
        "directive": directive,
        "narrative": narrative,
        "factors": factors,
    }
