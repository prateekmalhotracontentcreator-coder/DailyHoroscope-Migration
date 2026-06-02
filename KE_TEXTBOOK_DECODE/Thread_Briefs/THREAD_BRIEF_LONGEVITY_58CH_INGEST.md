# Thread Brief -- Longevity 58 Chapters KE Ingest
## Status · Open Items · Immediate Next Action

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31
> For: Longevity 58 Chapters Ingest Thread
> Status: **🟢 FULLY UNBLOCKED ✅ (2026-06-02) -- Co-founder approved Option B. Ch36-58 rules extracted by CC thread (21 rules). ALL gates cleared. Full ingest sequence ready for A2.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_LONGEVITY_58CH_INGEST.md` for all Longevity (58 Chapters) KE Ingest.

---

## What This Thread Owns

"Longevity" full textbook -- 58 chapters, ~600+ decoded rules covering the complete Vedic longevity astrology system (Aayu calculation, Pindayu, Nisargayu, Amsayu, Maraka timing, Badhaka planets). This is the LAST book in the approved ingest sequence.

**Important distinction:** This is NOT the same as "Longevity & Unnatural Death" (44 rules -- already cleared). This is the complete longevity textbook with ~600+ rules across 58 chapters.

---

## Canonical Output Folder

```
/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/
```

Handover summary: `HANDOVER_SUMMARY_LongevityDecode.md` (in folder)

---

## Rule Count

| Metric | Value |
|---|---|
| Total rules | ~600+ (exact count pending final validation) |
| Chapters | 58 total |
| Ch4/Ch5 decode method | NLM thread |
| Ch6-Ch58 decode method | Claude Code |
| Aayu bucket rules | BLOCKED pending co-founder methodology approval |

---

## ~~THE HARD BLOCK~~ ✅ GATE CLEARED 2026-06-02

~~The ~600 rules include a significant sub-set of **aayu bucket rules**...~~

**Gate cleared.** Co-founder approved Option B with label-based tagging and 66-75 edge case gates on 2026-06-02. Full decision recorded in the Approval Record and Architecture section above.

**Remaining gate before ingest can start:** Ch36-Ch58 Codex commission must be issued (see Decode Status). Ch4-Ch19 ingest can begin immediately without waiting for Ch36-58.

---

## Blocker Resolution Process

1. **TT presents the two methodologies** to the co-founder with a brief summary of the difference and the implications
2. **Co-founder selects one methodology** and provides explicit written approval
3. **Approval text is recorded** in this brief (update the "Approval Record" section below) and in `HANDOVER_SUMMARY_LongevityDecode.md`
4. **This thread then unblocks** -- proceed to dedup and ingest

### Approval Record

```
Date:         2026-06-02
Methodology:  Option B -- Label-Based Tagging with 66-75 Edge Case Gate
Authority:    Prateek Malhotra (Co-Founder)
Statement:    "Go with Option B with Edge Case Management and Rules.
               Instead of Hard Coding the Age Bracket, give Labels (Madhya Aayu, etc).
               For Edge Case -- Keep range as 66-75 which Gated checks -- Dashas, Planets, etc."
GAI Support:  GAI response (SBC_AAYU Chapter_GAI Response.md) corroborates Option B.
               GAI notes 72 years as classical Jyotish boundary (Shashtyamsa/Ashtakavarga
               reductions) -- recorded as the reference midpoint within the 66-75 gate zone.
Recorded by:  Claude Code Main Thread (CC) -- 2026-06-02
```

---

## ✅ Approved Architecture -- Aayu Bucket Methodology

### Core Decision

**Rules use labels only -- no hardcoded year numbers.** Year ranges live in a single centralized config. All ~600 rules tag `aayu_bucket` with a string label. The engine resolves label → year range at runtime via config.

### Label Vocabulary (canonical, use exactly these strings)

| Label | Name | Range (Option B) | Notes |
|---|---|---|---|
| `balarishta` | Infant Mortality | 0-8 yrs | Unchanged in both options |
| `alpa_aayu` | Short Longevity | 8-33 yrs | Unchanged in both options |
| `madhya_aayu` | Middle Longevity | 33-75 yrs | **Option B: wider range** |
| `purna_aayu` | Full Longevity | 75-100 yrs | **Option B: starts at 75** |
| `aparimita_aayu` | Super-Centenarian | 100+ yrs | Unchanged in both options |

### Centralized Config (to be added to `backend/ke_schema_constants.py`)

```python
LONGEVITY_AAYU_CONFIG = {
    "balarishta":    {"min": 0,   "max": 8},
    "alpa_aayu":     {"min": 8,   "max": 33},
    "madhya_aayu":   {"min": 33,  "max": 75},
    "purna_aayu":    {"min": 75,  "max": 100},
    "aparimita_aayu":{"min": 100, "max": None},
}

LONGEVITY_EDGE_CASE_ZONE = {
    "min": 66,
    "max": 75,
    "classical_reference_point": 72,   # Shashtyamsa/Ashtakavarga classical boundary (GAI note)
    "gates": ["dasha_activity", "maraka_strength", "ayushkaraka_strength"],
    "default_on_boundary": "higher_bucket",  # If gates inconclusive, assign to Purna
}
```

### Edge Case Zone: 66-75

Rules whose natural outcome falls in the 66-75 year window receive an additional field:

```python
# In the rule's result block:
rule["result"]["aayu_bucket"]    = "madhya_aayu"   # baseline bucket
rule["result"]["edge_case_zone"] = True            # flags this rule as boundary-sensitive
rule["result"]["edge_case_gates"] = [              # gates the engine must check
    "dasha_activity",      # Is a Maraka/Badhaka Dasha active in the 66-75 window?
    "maraka_strength",     # Are Maraka lords strong enough to terminate life?
    "ayushkaraka_strength" # Is Saturn (Ayushkaraka) protective in this period?
]
# Gate resolution logic (for engine team):
# - Strong Maraka/Badhaka Dasha active at 66-75 → pull outcome toward Alpa floor (66)
# - Strong Ayushkaraka (Saturn) active → push outcome toward Purna boundary (75)
# - Both weak / inconclusive → default to 'higher_bucket' (Purna)
```

### What Does NOT Go in Rule Objects

- ❌ No `"min_age": 33` or `"max_age": 75` in any rule
- ❌ No literal year numbers in `interpretation.detailed` or `interpretation.summary` that define bucket boundaries
- ✅ OK to mention years in source-text quotations (e.g. "the author states 33 to 66 years")

### Fuzzy Scoring (future enhancement -- do not block ingest on this)

GAI also recommended a weight-based scoring approach (a chart with heavy Alpa indicators + minor Madhya indicators scores 70% Alpa / 30% Madhya). This is a runtime engine enhancement, NOT an ingest concern. Rules ingest with a single `aayu_bucket` label. The engine team implements scoring separately post-ingest.

---

## Decode Status (for reference -- decode is complete)

| Phase | Status |
|---|---|
| Ch4-Ch5 (NLM) | ✅ Complete |
| Ch6-Ch58 (CC) | ✅ Complete -- all 58 chapters accounted for |
| Handover document | ✅ `HANDOVER_SUMMARY_LongevityDecode.md` present |
| Aayu bucket methodology | ✅ **APPROVED 2026-06-02** -- Option B, label-based, 66-75 edge gate |
| Ch36-Ch58 case study extraction | ✅ **CC THREAD COMPLETE 2026-06-02** -- 21 rules, `Longevity_CaseStudies_Ch36-58_Rules.json` + `_Diagnostic.md` in `Longevity_CC_Decode/` |

The decode work is finished for rule extraction. It is ONLY the governance gate that blocks ingest.

**Note on Ch36-58 case study rules:** A separate Codex commission for extracting structured rules from the case study chapters (Ch36-Ch58) has NOT yet been issued. These chapters contain benchmark birth chart case studies requiring a different extraction approach from the rule chapters. When the aayu bucket gate is cleared, TT must also brief this Codex commission before the full ~600+ rule count can be finalised and ingested.

---

## ⚠️ Phase 2 Schema Learnings -- Apply When Unblocked

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). When the aayu bucket gate is cleared and ingest begins, apply these before writing the script.**

**Ingest script checklist (for when gate clears):**
- [ ] `source["batch_id"] = BATCH_ID` inside `inject_fields()` -- NOT just top-level `ingest_batch_id`; validate_rules.py queries `source.batch_id`
- [ ] Run schema audit on `Longevity_CC_Decode/` folder first -- this book has 58 chapter files, high probability of schema variation
- [ ] `interpretation.detailed` and `interpretation.summary` non-empty on every rule -- add `_map_interpretation()` if needed
- [ ] `condition` is a non-empty dict -- add `_map_condition()` if source uses `conditions` list
- [ ] Pre-upload local structural check: `Issues: 0` before uploading ~600 rules

**Template helpers:** `_map_interpretation()` + `_map_condition()` from `backend/scripts/ingest_bphs_vol1_phase2.py`.

**Three-bucket triage for validation results:** A (artifact → `auto_approved`) · B (validator error → PHR) · C (genuine → flagged TT/GAI)

---

## Ingest Instructions (when unblocked -- do not read until gate cleared)

**Step 1 -- Record approval in HANDOVER_SUMMARY_LongevityDecode.md**

**Step 2 -- Run pre-ingest dedup (extensive -- this book will cross-match many others):**
```bash
# Against BPHS Vol 1 (longevity chapters Ch43/44)
python3 backend/ke_dedup_script.py \
  --folder-a ".../Longevity_CC_Decode/" \
  --folder-b ".../BPHS_CC_Decode/" \
  --output-report dedup_longevity_vs_bphs_vol1.md

# Against Longevity Unnatural Death
python3 backend/ke_dedup_script.py \
  --folder-a ".../Longevity_CC_Decode/" \
  --folder-b ".../LongevityUnnatural_CC_Decode/" \
  --output-report dedup_longevity_vs_longunnat.md

# Against KP Astrology (longevity rules)
python3 backend/ke_dedup_script.py \
  --folder-a ".../Longevity_CC_Decode/" \
  --folder-b ".../KP_CC_Decode/" \
  --output-report dedup_longevity_vs_kp.md
```

**Step 3 -- Inject on every rule:**
```python
rule["approval_status"]    = "pending_human_review"
rule["claim_axis"]         = "longevity"
rule["ingest_batch_id"]    = "longevity_58ch_v1"
rule["source_book"]        = "Longevity (58 Chapters)"
rule["source"]["batch_id"] = "longevity_58ch_v1"  # MANDATORY -- validate_rules.py queries this
```

---

## Post-Ingest Dedup Targets (high overlap expected)

| Target | Expected Overlap |
|---|---|
| BPHS Vol 1 Ch43/44 | HIGH -- BPHS is the primary source text |
| Longevity Unnatural Death | Moderate -- same domain, different emphasis |
| KP Astrology longevity rules | Moderate |
| Phaladeepika Adhyaya XIII/XIV | Moderate |

---

## Immediate Next Action (gate cleared -- 2026-06-02)

| Step | Action | Owner |
|---|---|---|
| 1 | Add `LONGEVITY_AAYU_CONFIG` + `LONGEVITY_EDGE_CASE_ZONE` to `backend/ke_schema_constants.py` | CC |
| ~~2~~ | ~~Issue Ch36-Ch58 case study rules Codex commission (separate from main ingest)~~ | ~~TT~~ | ✅ CLOSED -- CC thread extracted 21 rules directly (2026-06-02) |
| 3 | Run dedup: `Longevity_CC_Decode/` vs `BPHS_CC_Decode/` (Ch43/44) and vs `LongevityUnnatural_CC_Decode/` | A2 / CC |
| 4 | Write ingest script -- Ch5 first (aayu framework rules), then Ch4, then Ch6-18 lagna batches | A2 |
| 5 | Apply label-based `aayu_bucket` tags. Mark 66-75 zone rules with `edge_case_zone: true` | A2 (script) |
| 6 | Dry run → local structural check → upload → validate → patch → commit | A2 |
| 7 | Ch36-58 case study rules: separate ingest sprint after Codex commission delivers | Future sprint |

**Ch4-Ch19 ingest can begin immediately. Do NOT wait for Ch36-58 commission.**

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
