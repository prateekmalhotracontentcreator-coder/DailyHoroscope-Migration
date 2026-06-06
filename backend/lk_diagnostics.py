from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

YEAR_CYCLE = [
    (0, 8, "Ketu"),
    (9, 28, "Venus"),
    (29, 34, "Sun"),
    (35, 44, "Moon"),
    (45, 51, "Mars"),
    (52, 69, "Rahu"),
    (70, 85, "Jupiter"),
    (86, 104, "Saturn"),
    (105, 121, "Mercury"),
]


def get_year_lord(age: int) -> str:
    for start, end, planet in YEAR_CYCLE:
        if start <= age <= end:
            return planet
    return "Mercury"


CONFLICT_ACTION_MAP = {
    "building_construction": [616],
    "foreign_contract": [617],
    "charity_event": [618],
    "property_investment": [619],
    "digital_launch": [620],
    "marriage_ritual": [621],
    "spiritual_retreat": [622],
    "multiple_remedies": [623, 624, 625],
}

GATE1_IDS = list(range(483, 616))
GATE2_IDS = list(range(636, 651))
GATE3_IDS = list(range(526, 576))
GATE4_IDS = list(range(626, 636))
GATE5_IDS = list(range(505, 526)) + list(range(651, 656))
DEBT_IDS = list(range(601, 616))
CONFLICT_IDS = list(range(616, 626))

LK_SCIENCE_ID = "jyotish_lk_remedies"


async def run_gate1(db, natal_chart: dict) -> dict:
    records = await db.knowledge_rules.find(
        {"science_id": LK_SCIENCE_ID, "id": {"$in": GATE1_IDS}},
        {"_id": 0}
    ).to_list(None)

    priority = [r for r in records if r.get("severity", 0) >= 4]
    has_warning = len(priority) > 0

    return {
        "status": "WARNING" if has_warning else "CLEAR",
        "records": records[:10],
        "priority_count": len(priority),
        "active_pitru_rin": has_warning,
        "narrative": (
            "Ancestral Debt active. Stabilize roots before transit gains."
            if has_warning else
            "No critical karmic debt detected."
        ),
    }


async def run_gate2(db, natal_chart: dict) -> dict:
    records = await db.knowledge_rules.find(
        {"science_id": LK_SCIENCE_ID, "id": {"$in": GATE2_IDS}},
        {"_id": 0}
    ).to_list(None)

    occupied = {p: h for p, h in natal_chart.items() if h}
    occupied_houses = set(occupied.values())
    dormant_houses = [h for h in range(1, 13) if h not in occupied_houses]

    matching = [r for r in records if r.get("house") in dormant_houses]
    status = "DORMANT" if dormant_houses else "ACTIVE"

    return {
        "status": status,
        "dormant_houses": dormant_houses,
        "awakening_records": matching[:5],
        "narrative": (
            f"H{dormant_houses[0]} dormant. Activate adjacent houses first."
            if dormant_houses else
            "All houses active. Proceed with expansion."
        ),
    }


async def run_gate3(db, age: int) -> dict:
    planet = get_year_lord(age)
    records = await db.knowledge_rules.find(
        {
            "science_id": LK_SCIENCE_ID,
            "id": {"$in": GATE3_IDS},
            "planet": planet,
        },
        {"_id": 0}
    ).to_list(None)

    if not records:
        records = await db.knowledge_rules.find(
            {"science_id": LK_SCIENCE_ID, "id": {"$in": GATE3_IDS}},
            {"_id": 0}
        ).limit(5).to_list(None)

    age_band = next(
        (f"{s}-{e}" for s, e, p in YEAR_CYCLE if p == planet),
        str(age)
    )

    return {
        "planet": planet,
        "age_range": age_band,
        "records": records[:5],
        "narrative": f"{planet} year-lord phase active (age {age_band}).",
    }


async def run_gate4(db, natal_chart: dict) -> dict:
    records = await db.knowledge_rules.find(
        {"science_id": LK_SCIENCE_ID, "id": {"$in": GATE4_IDS}},
        {"_id": 0}
    ).to_list(None)

    mercury_house = natal_chart.get("Mercury")
    rahu_house = natal_chart.get("Rahu")

    occupied_houses = list(natal_chart.values())
    house_counts: dict[int, int] = {}
    for h in occupied_houses:
        if h:
            house_counts[h] = house_counts.get(h, 0) + 1

    mercury_alone = mercury_house and house_counts.get(mercury_house, 0) == 1
    rahu_collision = mercury_house and rahu_house and mercury_house == rahu_house

    if rahu_collision:
        status = "RAHU_COLLISION"
        narrative = "Mercury-Rahu conjunction detected. Intelligence disrupted."
    elif mercury_alone:
        status = "EMPTY_VESSEL"
        narrative = "Mercury solitary. Filling the Vessel activation required."
    else:
        status = "CLEAR"
        narrative = "Mercury configuration stable."

    return {
        "status": status,
        "mercury_house": mercury_house,
        "records": records[:5],
        "narrative": narrative,
    }


async def run_gate5(db, natal_chart: dict, location_slug: str) -> dict:
    records = await db.knowledge_rules.find(
        {"science_id": LK_SCIENCE_ID, "id": {"$in": GATE5_IDS}},
        {"_id": 0}
    ).to_list(None)

    location_records = [r for r in records if location_slug in str(r.get("location", "")).lower()]
    if not location_records:
        location_records = records[:3]

    return {
        "user_direction": "South",
        "location_slug": location_slug,
        "records": location_records[:5],
        "substitution_applied": len(location_records) == 0,
        "narrative": f"Geographical alignment checked for {location_slug.replace('-', ' ').replace('_', ' ').title()}.",
    }


async def run_conflict_check(db, planned_action: str) -> dict:
    target_ids = CONFLICT_ACTION_MAP.get(planned_action, [])
    if not target_ids:
        return {"status": "CLEAR", "records": [], "planned_action": planned_action}

    records = await db.knowledge_rules.find(
        {"science_id": LK_SCIENCE_ID, "id": {"$in": target_ids}},
        {"_id": 0}
    ).to_list(None)

    safety_fired = [
        r for r in records
        if str(r.get("ke_inference", "")).startswith("⚠️ SAFETY GATE")
    ]

    return {
        "status": "CONFLICT" if safety_fired else "CLEAR",
        "planned_action": planned_action,
        "records": safety_fired or records,
        "requires_acknowledgement": bool(safety_fired),
    }


async def run_debt_audit(db, family_census: dict) -> list[dict]:
    records = await db.knowledge_rules.find(
        {"science_id": LK_SCIENCE_ID, "id": {"$in": DEBT_IDS}},
        {"_id": 0}
    ).to_list(None)

    results = []
    for r in records:
        relation = r.get("blood_relation_target", "")
        available = True
        use_sub = False
        if relation and relation in family_census:
            status = family_census[relation]
            if status in ("deceased", "unknown"):
                available = False
                use_sub = True
        results.append({
            "remedy_record": r,
            "relative_available": available,
            "use_substitute": use_sub,
        })
    return results


async def run_full_diagnosis(db, profile: dict) -> dict:
    natal_chart = profile.get("natal_chart", {})
    age = profile.get("age", 30)
    location_slug = profile.get("location_slug", "new-delhi")
    family_census = profile.get("family_census", {})

    gate1, gate2, gate3, gate4, gate5 = (
        await run_gate1(db, natal_chart),
        await run_gate2(db, natal_chart),
        await run_gate3(db, age),
        await run_gate4(db, natal_chart),
        await run_gate5(db, natal_chart, location_slug),
    )

    roadmap = _build_roadmap(gate1, gate2, gate3, gate4, gate5)

    return {
        "user_id": profile.get("user_id", ""),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gates": {
            "gate1_karmic_debt": gate1,
            "gate2_house_awakening": gate2,
            "gate3_year_cycle": gate3,
            "gate4_mercury_scan": gate4,
            "gate5_geographical": gate5,
        },
        "execution_roadmap": roadmap,
        "safety_gates_fired": [],
    }


def _build_roadmap(g1: dict, g2: dict, g3: dict, g4: dict, g5: dict) -> list[dict]:
    steps = []
    day = 1
    if g1["status"] == "WARNING" and g1["records"]:
        r = g1["records"][0]
        steps.append({"days": f"{day}-{day+6}", "task": "Clear Karmic Debt (Gate 1)", "remedy_id": r.get("id")})
        day += 7
    if g2["status"] == "DORMANT" and g2.get("awakening_records"):
        r = g2["awakening_records"][0]
        steps.append({"days": str(day), "task": "House Awakening (Gate 2)", "remedy_id": r.get("id")})
        day += 1
    if g4["status"] in ("EMPTY_VESSEL", "RAHU_COLLISION") and g4["records"]:
        r = g4["records"][0]
        steps.append({"days": f"{day}-{day+42}", "task": "43-Day Mercury Anchor (Gate 4)", "remedy_id": r.get("id")})
    return steps
