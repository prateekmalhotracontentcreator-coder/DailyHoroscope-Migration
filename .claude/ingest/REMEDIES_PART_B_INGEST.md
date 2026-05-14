# REMEDIES_PART_B_INGEST.md  (New Remedies Module -- Part B)
> Last updated: 2026-05-11  |  STATUS: DATA LIVE + APPLICATION LAYER LIVE

---

## Final Confirmed Coverage

| Category | IDs | Records | science_id | Data | App Layer |
|---|---|---|---|---|---|
| Dhana Remedies | 1-100 | 100 | `jyotish_remedies_dhana` | ✅ Live | ✅ Live -- paid 3-view report flow |
| Gemstones | 101-200 | 100 | `jyotish_remedies_gemstones` | ✅ Live | ✅ Live -- paid 3-view report flow |
| Crystal Remedies | 201-300 | 100 | `jyotish_remedies_crystals` | ✅ Live | ✅ Live -- paid 3-view report flow |
| 7 Chakra Healing | 301-307 | 7 | `jyotish_remedies_chakra` | ✅ Live | ✅ Live -- paid 3-view report flow |
| Lal Kitab Remedies | 308-668 | **361** | `jyotish_lk_remedies` | ✅ Live | ✅ Live -- LK Standalone module |
| Mantra Remedies | -- | 100 | `jyotish_remedies_mantras` | ✅ Live | ✅ Live -- paid 3-view report flow |
| Strategist (Career) | 701-1025 | 325 target | `lalkitab_strategist` | ⚠️ Partial -- see STRATEGIST_INGEST.md | ✅ Live -- Phase 1 War Room |
| KP Remedies | TBD | TBD | `krishna_prashnavali_remedies` | ❌ Not yet ingested | ❌ Pending KP migration |

## Application Layer Status (2026-05-11)
- All 5 remedy modules: **3-view paid report flow** live (tiles → birth details → chart-based report)
- Routes: `POST /api/remedies/{type}/generate-report` -- calls `vedic_calculator.py`, queries `interpretation_rules`
- LK Standalone: full module live (Onboard → Report → Tracker → Debt Audit → Browse)
- Mantra module: live at `/mantra-remedies`
- Strategist War Room: Phase 1 live; Phase 2 (KP Gate 0 integration) -- build starting

## Pending Ingest Items
1. **Strategist patch** -- 22 records (IDs 1011-1020 + 1126-1137), dry-run verified clean. Script: `ingest_strategist_patch_v2.py`. Needs explicit user confirmation before running live.
2. **KP Remedies** -- `krishna_prashnavali_remedies` collection not yet ingested. Source: `/Users/apple/Documents/New project/KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json`. Pending Codex updated bundle delivery.

---

---

## LK Remedies -- Final ID Architecture (LOCKED)

| Block | IDs | Count | Source | Notes |
|---|---|---|---|---|
| Core + Gap Fill | 308-615 | 308 | Original + Gap Fill file | All 77 gaps filled |
| Conflict Gates | 616-625 | 10 | Gap Fill | Folded into ke_inference; tagged `record_type: conflict_gate` |
| Extended Module | 626-655 | 30 | Gap Fill | Mercury Empty Vessel + other planets |
| Supplementary | 656-668 | 13 | Sub-IDs renumbered | parent_id field added |
| **Total** | **308-668** | **361** | | |
| Buffer | 669-700 | -- | Reserved | Gap before Strategist |
| Strategist | 701-1027 | ~325 | Separate module | Spec ready -- build pending |

---

## Sub-ID Renumbering Map (Decimal → Integer)

| New ID | Was | Parent ID | Theme |
|---|---|---|---|
| 656 | 357.1 | 357 | Extra Mercury Advisor rule |
| 657 | 357.2 | 357 | Extra Mercury Advisor rule |
| 658 | 382.1 | 382 | Peepal Constraint (last occurrence) |
| 659 | 382.2 | 382 | Mercury Solitary H10 (last occurrence) |
| 660 | 407.1 | 407 | Extra Social / Saturn Building Ban |
| 661 | 525.1 | 525 | Safety buffer rule |
| 662 | 525.2 | 525 | Safety buffer rule |
| 663 | 525.3 | 525 | Safety buffer rule |
| 664 | 525.4 | 525 | Safety buffer rule |
| 665 | 525.5 | 525 | Safety buffer rule |
| 666 | 615.1 | 615 | Extra Karmic Debt rule |
| 667 | 615.2 | 615 | Extra Karmic Debt rule |
| 668 | 615.3 | 615 | Extra Karmic Debt rule |

---

## Destructive Merge Rules (Ingest Script Must Enforce)

| IDs | Use | Discard |
|---|---|---|
| 503-507 | Version 2 -- Success Compass / Strategic Anchors | Version 1 -- Inheritance Lock themes |
| 484 | Version 1 -- Emotional Peace / Matru Rin (anchor record) | -- |
| 485-499 | Version 2 -- Reconciled Logic / Rin Matrix | Version 1 -- Blood Collective batch |
| 505-525 | Version 2 -- Directional Realignment (Geographical Pivot) | Version 1 -- Karmic/Ancestral themes |
| 382.1 → 658 | Last occurrence -- Peepal Constraint | Earlier version |
| 382.2 → 659 | Last occurrence -- Mercury Solitary H10 | Earlier version |

**Rule:** For any ID appearing more than once in source files -- last occurrence wins.

---

## Special Schema Rules

### 616-625 (Conflict Gates)
- Fold `conflict_rule` + `safety_interlock` → into `ke_inference`
- Format: `"⚠️ SAFETY GATE: [safety_interlock]. [conflict_rule]."`
- Add extra field: `"record_type": "conflict_gate"`
- Do NOT surface as standalone remedies in UI

### 656-668 (Supplementary)
- Add extra field: `"parent_id": <integer>`
- `record_type`: `"supplementary"`

### All records
- `science_id`: `"jyotish_lk_remedies"`
- `approval_status`: `"pending_human_review"` (standard -- not auto_approved until validated)
- `trigger_blind_planet` and `trigger_dormant`: must be boolean (True/False), not string

---

## Pre-Ingest Checklist

- [x] All 77 original gaps filled
- [x] Duplicate resolution confirmed (last occurrence rule)
- [x] 611-614 upgraded to full 18-dim (GAI Q5 response) -- hardcoded in script
- [x] 616-625 schema decision (fold into ke_inference)
- [x] 626-655 confirmed in scope
- [x] Sub-IDs renumbered 656-668 with parent_id
- [x] Strategist impact deferred -- final list locked first
- [x] Crystal Remedies split array bug -- FIXED (object-scan parser handles it)
- [x] Scripts written and dry-run verified (361 records, all counts match)
- [x] Destructive merge verified (ID 505 = "Directional Realignment" ✅ PASS)
- [x] ID 659 Mercury Solitary H10 = primary_planet Mercury, house 10 ✅ PASS
- [x] ID 615 upgraded to 18-dim ("Karmic Debt: The Master Fallback / Proxy Shield") -- hardcoded
- [x] Gate 0 schema validation: 0 errors ✅
- [x] MongoDB upload executed 2026-05-09 -- all 5 scripts clean
- [x] Post-ingest verification: 12/12 checks passed ✅ 2026-05-09

---

## Known Pre-Ingest Fix Required

### Crystal Remedies -- Split JSON Array Bug
File: `4. Crystal Remedies_JSON.md` contains TWO separate `[...]` arrays.
Fix: Merge into single array before ingest script reads file.

---

## Ingest Scripts to Write (in order)

1. `ingest_remedies_dhana_v1.py` -- IDs 1-100
2. `ingest_remedies_gemstones_v1.py` -- IDs 101-200
3. `ingest_remedies_crystals_v1.py` -- IDs 201-300 (fix split array first)
4. `ingest_remedies_chakra_v1.py` -- IDs 301-307
5. `ingest_lk_remedies_v1.py` -- IDs 308-668 (destructive merge + sub-ID renumber)
6. `ingest_strategist_v1.py` -- IDs 701-1025 (deferred)

## Mandatory Ingest Order
1→2→3→4→5→6 -- do not change order. Strategist (6) depends on LK Remedies (5) being live.

---

## Testing
Test plan: `backend/scripts/LK_REMEDIES_TEST_PLAN.md`
- Schema validation (Gate 0 -- blocks ingest if fail)
- Destructive merge verification (ID 505 content check)
- 5-Gate MongoDB query sequence
- Master Test Query: Mercury H10, Age 36, Saturn transit H7, South direction, building plan
- 4 PASS criteria + 3 FAIL triggers documented

## Status
COMPLETE ✅ 2026-05-09 | 666 records live | 12/12 verification checks passed | PRODUCTION READY
