"""
Patch script -- two operations:
1. Insert ID 817 (gap-fill: The Garrison / Human Capital block)
2. Deprecate IDs 651-675 (old surrogates) → add field: retired=True, retired_by=1201
3. Verify IDs 1201-1225 are present (V2 surrogates)

Run: python3 patch_strategist_817_surrogates.py "$MONGO_URL"
"""
import sys
from pymongo import MongoClient

client = MongoClient(sys.argv[1])
col = client['horoscope_db']['knowledge_rules']

# ── 1. Gap-fill ID 817 ─────────────────────────────────────────────────────
# Context: The Garrison block (801-850) -- Staffing archetypes, loyalty anchors, HR audits
# Neighbours: 815 Wisdom-Governance Anchor (Saturn/governance), 816 Community Luxury Experience
#             (Venus/culture), 818 Royal Decree Reset (Sun/authority), 819 Aggressive Territory
#             Capture (Mars/expansion)
# Theme: Mercury -- communication audit, conflict mapping, inter-team mediation
RECORD_817 = {
    "id": 817,
    "science_id": "lalkitab_strategist",
    "mission_name": "The 'Mercury-Map' Conflict Audit",
    "mission_objective": "Human Capital Alignment & Internal Communication Repair",
    "segment": "The Garrison",
    "trigger_condition": "Transit_Mercury_H7",
    "strategy": "The 'Mercury-Bridge' Mediation Protocol",
    "decision_logic": (
        "Mercury transiting H7 exposes fractures in partnerships and inter-team agreements. "
        "This is the diagnostic window to surface hidden loyalty conflicts before they escalate "
        "into authority breakdown (Sun, ID 818) or territorial aggression (Mars, ID 819). "
        "Deploy structured communication audit: map all unresolved agreements, ambiguous "
        "role boundaries, and silent grievances within the core team."
    ),
    "pivot_logic": (
        "If Mercury is retrograde or combust during transit: do NOT initiate new HR agreements. "
        "Shift to internal listening mode only -- document grievances, defer resolution to "
        "Mercury direct. Retrograde Mercury in H7 amplifies misinterpretation risk."
    ),
    "pivot_action": (
        "1. Run structured 1:1 audit with all co-founders and direct reports. "
        "2. Map all verbal agreements not yet formalised in writing. "
        "3. Identify the single most destabilising communication gap. "
        "4. Issue a written 'Clarity Mandate' -- roles, responsibilities, decision rights. "
        "5. Cross-link to Wisdom-Governance Anchor (ID 815) for structural follow-through."
    ),
    "kpi_target": "Zero ambiguous reporting lines within 21 days. All verbal agreements formalised.",
    "remedy_id": 409,
    "approval_status": "approved"
}

result = col.update_one(
    {"id": 817, "science_id": "lalkitab_strategist"},
    {"$setOnInsert": RECORD_817},
    upsert=True
)
if result.upserted_id:
    print("ID 817: INSERTED ✅")
elif result.matched_count:
    print("ID 817: Already exists -- skipped")
else:
    print("ID 817: No action taken")

# ── 2. Retire IDs 651-675 (V1 surrogates -- superseded by 1201-1225) ────────
retire_result = col.update_many(
    {"science_id": "lalkitab_strategist", "id": {"$gte": 651, "$lte": 675}},
    {"$set": {"retired": True, "retired_by_range": "1201-1225", "approval_status": "deprecated"}}
)
print(f"IDs 651-675: Retired {retire_result.modified_count} V1 surrogate records ✅")

# ── 3. Verify IDs 1201-1225 are present and active ────────────────────────
v2_count = col.count_documents({
    "science_id": "lalkitab_strategist",
    "id": {"$gte": 1201, "$lte": 1225}
})
print(f"IDs 1201-1225: {v2_count} V2 surrogate records present [expected 25] {'✅' if v2_count == 25 else '⚠️ CHECK'}")

# ── 4. Final count summary ─────────────────────────────────────────────────
active = col.count_documents({"science_id": "lalkitab_strategist", "approval_status": {"$ne": "deprecated"}})
deprecated = col.count_documents({"science_id": "lalkitab_strategist", "approval_status": "deprecated"})
lk = col.count_documents({"science_id": "jyotish_lk_remedies"})

print()
print("=== FINAL STATE ===")
print(f"lalkitab_strategist -- Active: {active} | Deprecated (651-675): {deprecated}")
print(f"jyotish_lk_remedies -- Total: {lk}")
print(f"Grand Total (active): {active + lk}")
