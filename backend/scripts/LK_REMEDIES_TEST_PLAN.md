# LK Remedies -- Master Testing & Ingestion Validation Plan
> Created: 2026-05-09 | Status: PRE-INGEST (document before scripts are written)
> Source: GAI Master Query + adapted for our MongoDB/FastAPI KE architecture

---

## 1. Schema Validation Test (Run First -- Blocks Ingest if Fail)

Validate every record in the merged JSON before touching MongoDB.

**What to check:**
- All 18 mandatory fields present
- No decimal IDs (all must be integers after renumbering)
- No duplicate IDs
- `trigger_blind_planet` and `trigger_dormant` are boolean, not string
- `severity_scale` is integer 1-5
- `frequency_days` is integer
- `id` is integer and falls within expected ranges

**Expected ranges after full merge:**
- Core remedies: 308-615
- Conflict gates: 616-625
- Extended module: 626-655
- Supplementary (renumbered sub-IDs): 656-668
- **Total unique IDs: 361**

**Mandatory 18 fields:**
```
id, focus_area, primary_planet, house, shadbala_threshold,
strength_modifier, artificial_planet_fix, trigger_blind_planet,
trigger_dormant, physical_object, ritual_act, prohibited_act,
blood_relation_target, substitute_item, start_day, muhurta_rule,
frequency_days, severity_scale, ke_inference
```

**Additional field for supplementary records (656-668):**
```
parent_id  →  integer pointing to semantic parent (e.g., 656 → parent_id: 357)
```

**Special handling for 616-625 (Conflict Gates):**
- `conflict_rule` and `safety_interlock` content must be folded INTO `ke_inference`
- Resulting `ke_inference` format: "⚠️ SAFETY GATE: [safety_interlock text]. [conflict_rule text]."
- These records must be tagged: `"record_type": "conflict_gate"` (extra field, non-schema)

---

## 2. Destructive Merge Verification Test

Before ingest, confirm correct versions are present in the merged JSON.

**Check these IDs manually -- wrong version = ingest failure:**

| ID | Correct Version | Wrong Version (should NOT appear) | Key Identifier |
|---|---|---|---|
| 505 | "Directional Realignment: East" | "Inheritance Lock" or karmic debt theme | `focus_area` contains "Directional" |
| 506 | "Directional Realignment: South" | Any ancestral/rin theme | Same |
| 507 | "Directional Realignment: West/North" | Inheritance/Sun's Seal | Same |
| 503 | "Success Compass / Strategic Anchors" | "Inheritance Lock: The Sun's Seal" | `focus_area` not "Inheritance Lock" |
| 484 | "Emotional Peace (Matru Rin)" | Any other version | `primary_planet: "Moon"` |
| 485-499 | Reconciled Logic / Rin Matrix | Earlier "Blood Collective" batch | Check `blood_relation_target` fields are populated |
| 659 | Mercury Solitary H10 (was 382.2) | Earlier Saturn/Venus version | `primary_planet: "Mercury"`, `house: 10` |
| 658 | Peepal Constraint (was 382.1) | Earlier version | `prohibited_act` contains "Peepal" |

**MongoDB verification query (run after ingest):**
```python
# Confirm Version 2 for ID 505
db.lk_remedies.find_one({"id": 505}, {"focus_area": 1})
# Expected: focus_area contains "Directional Realignment" or "Geographical Pivot"
# Fail: focus_area contains "Inheritance" or "Sun's Seal"

# Confirm conflict gate IDs are tagged
db.lk_remedies.find({"id": {"$gte": 616, "$lte": 625}}, {"record_type": 1, "ke_inference": 1})
# Expected: all have record_type = "conflict_gate"
```

---

## 3. The Master Test Query (Adapted for our KE)

**Original GAI query:**
> "I am 36 years old. I have Mercury alone in my 10th House. My Saturn is transiting my 7th House, and I am planning to start a major building construction project today in the South direction."

**Our KE inputs (structured):**
```json
{
  "user_age": 36,
  "natal_planets": [{"planet": "Mercury", "house": 10, "is_solitary": true}],
  "transit_planets": [{"planet": "Saturn", "house": 7}],
  "planned_action": "building_construction",
  "direction": "South"
}
```

---

## 4. The 5-Gate Query Sequence (Our MongoDB Implementation)

Gates must execute **in order**. Each gate's result feeds into the final LLM prompt.

### Gate 1 -- Karmic Debt Audit
```python
# Check if user's age triggers a debt cycle
# Age 36 → Saturn cycle (36-41) → check Pitra Rin
gate1_results = db.lk_remedies.find({
    "science_id": "jyotish_lk_remedies",
    "id": {"$in": list(range(483, 501)) + [611, 612, 613, 614]},
    "approval_status": "approved"
})
# Expected: Returns records related to Saturn/ancestral debt triggers
# KE Action: If any record has severity_scale >= 4, flag as PRIORITY WARNING
```

### Gate 2 -- House Awakening (Dormant Planet Check)
```python
gate2_results = db.lk_remedies.find({
    "science_id": "jyotish_lk_remedies",
    "primary_planet": "Mercury",
    "house": 10,
    "trigger_dormant": True,
    "approval_status": "approved"
})
# For solitary Mercury in H10: also fetch supplementary record
gate2_supplementary = db.lk_remedies.find_one({
    "id": 659,   # was 382.2 -- Mercury Solitary H10
    "approval_status": "approved"
})
# Expected: Returns Mercury H10 awakening ritual
# KE Inference trigger: "Manager without a Boss" scenario
```

### Gate 3 -- 35-Year Cycle (Lord of the Year)
```python
# Age 36 → Saturn's cycle
gate3_results = db.lk_remedies.find({
    "science_id": "jyotish_lk_remedies",
    "primary_planet": "Saturn",
    "id": {"$gte": 526, "$lte": 575},
    "approval_status": "approved"
})
# Expected: Saturn cycle records with age-band logic
```

### Gate 4 -- Mercury-Rahu Collision Check
```python
gate4_results = db.lk_remedies.find({
    "science_id": "jyotish_lk_remedies",
    "id": {"$gte": 631, "$lte": 635},
    "primary_planet": "Mercury",
    "approval_status": "approved"
})
# Expected: Mercury-Rahu interaction warnings for solitary Mercury
```

### Gate 5 -- Geographical Pivot (Direction Check)
```python
# South direction specified → Directional Realignment
gate5_results = db.lk_remedies.find({
    "science_id": "jyotish_lk_remedies",
    "id": {"$gte": 505, "$lte": 525},
    "approval_status": "approved"
})
# Filter for South direction in focus_area
# Expected: "Directional Realignment: South" record (ID 506)
# ⚠️ Must NOT return any "Inheritance Lock" or ancestral-themed record for 505-525
```

### Conflict Gate -- Building Construction Check
```python
# Planned action = building_construction → triggers Saturn Building Ban
conflict_check = db.lk_remedies.find_one({
    "science_id": "jyotish_lk_remedies",
    "id": 622,   # Saturn Building Ban conflict gate
    "record_type": "conflict_gate",
    "approval_status": "approved"
})
# Expected: Returns ke_inference containing "⚠️ SAFETY GATE: No new house construction..."
# KE Action: Inject this warning at TOP of response before any remedy is shown
```

---

## 5. Pass / Fail Criteria (Our System)

### PASS -- All 4 must be true:

| Check | Test | Pass Condition |
|---|---|---|
| **P1 -- Destructive Merge** | Query ID 505 `focus_area` | Contains "Directional" -- NOT "Inheritance" |
| **P2 -- Building Ban Fire** | Conflict gate 622 returned | `ke_inference` starts with "⚠️ SAFETY GATE" |
| **P3 -- Mercury Solitary** | ID 659 returned in Gate 2 | `primary_planet: "Mercury"`, `house: 10` |
| **P4 -- Muhurta Rule** | Any returned remedy | `muhurta_rule` is daytime (not "Night" or "After Sunset") for non-Saturn records |

### FAIL -- Any of these = ingest problem:

| Check | Fail Signal | Root Cause |
|---|---|---|
| **F1** | ID 505 `focus_area` = "Inheritance Lock" | Destructive merge failed -- Version 1 present |
| **F2** | Building construction proceeds without warning | Conflict gate 622 not ingested or not tagged |
| **F3** | Mercury H10 returns no solitary-specific record | ID 659 missing or parent_id linkage broken |
| **F4** | Duplicate IDs found in collection | Ingest script didn't dedup before insert |

---

## 6. Muhurta Safety Rule (Hard-coded KE constraint)

Applies to ALL remedy outputs regardless of which gate triggered them:

```python
DAYLIGHT_RULE = "All remedies must be performed between Sunrise and Sunset."
EXCEPTIONS = ["Saturn (after sunset explicitly labelled)", "Rahu (twilight labelled)"]

# Before returning any remedy to user:
if record["muhurta_rule"] in ["Night", "After Sunset"] and record["primary_planet"] not in ["Saturn", "Rahu"]:
    record["muhurta_rule"] = "Sunrise to Sunset (corrected)"
    record["ke_inference"] += " NOTE: Perform only in daylight hours."
```

---

## 7. Post-Ingest Verification Queries

Run these in MongoDB after ingest to confirm health:

```python
# 1. Total count
db.lk_remedies.count_documents({"science_id": "jyotish_lk_remedies"})
# Expected: 361

# 2. No decimal IDs (all must be integers)
db.lk_remedies.find({"id": {"$type": "double"}})
# Expected: 0 results

# 3. No duplicate IDs
pipeline = [{"$group": {"_id": "$id", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}]
list(db.lk_remedies.aggregate(pipeline))
# Expected: []

# 4. Conflict gates tagged correctly
db.lk_remedies.count_documents({"science_id": "jyotish_lk_remedies",
                                  "record_type": "conflict_gate"})
# Expected: 10 (IDs 616-625)

# 5. Supplementary records have parent_id
db.lk_remedies.count_documents({"science_id": "jyotish_lk_remedies",
                                  "id": {"$gte": 656, "$lte": 668}})
# Expected: 13 (all have parent_id field)

# 6. Severity scale within bounds
db.lk_remedies.find({"severity_scale": {"$gt": 5}})
# Expected: 0 results

# 7. All records have approval_status
db.lk_remedies.find({"approval_status": {"$exists": False}})
# Expected: 0 results
```

---

## 8. science_id & Collection Reference

```
Collection:   horoscope_db.knowledge_rules
science_id:   "jyotish_lk_remedies"
ID range:     308-668
record_type:  "remedy" (default) | "conflict_gate" (IDs 616-625)
```

---

## Status
- [ ] Merge JSON prepared (gap fill + originals + Q5 upgrade + renumbered sub-IDs)
- [ ] Schema validation script run against merged JSON
- [ ] Destructive merge verified (ID 505 check)
- [ ] Ingest script written
- [ ] Ingest dry-run
- [ ] Ingest --apply
- [ ] Post-ingest verification queries run
- [ ] Master Test Query executed against live DB
- [ ] All 4 PASS criteria confirmed
