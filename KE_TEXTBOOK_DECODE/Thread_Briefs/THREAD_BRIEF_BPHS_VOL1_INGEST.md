# Thread Brief -- BPHS Vol 1 KE Ingest (Phase 2 New Chapters)
## Status · What's Already Done · What This Thread Ingest Now

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-06-01
> For: BPHS Vol 1 Ingest Thread
> Status: **✅ PHASE 2 INGEST COMPLETE (2026-06-01) -- 696 rules in MongoDB. 491 auto_approved · 170 pending_human_review · 35 flagged (TT/GAI review). Phase 1 (Ch12-44) clean -- all 5 NLM issues CLOSED.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_BPHS_VOL1_INGEST.md` for all BPHS Vol 1 KE Ingest.

---

## Master Ingest Process (read before writing any script)

**Full 7-step workflow:**
```
/Users/apple/DailyHoroscope-Migration/.claude/ke/INGEST_PROCESS_BRIEF.md
```

**Book-specific ingest tracking (Phase 1 history + open issues):**
```
/Users/apple/DailyHoroscope-Migration/.claude/ke/ingest/BPHS_VOL1_INGEST.md
```

**Ingest notes and cumulative totals:**
```
/Users/apple/DailyHoroscope-Migration/backend/scripts/INGEST_NOTES.md
```

The 7-step rule: **Dry Run → Save JSON → Review → Upload → Validate → Patch → Commit.** Never skip steps.

---

## What Is Already In MongoDB (Phase 1 -- do not re-ingest)

| Chapters | Script | Rules | Status |
|---|---|---|---|
| Ch12-24 (House Effects + Bhava Lords) | `ingest_bphs_houses.py` + `v2.py` | ~600 | ✅ Ingested |
| Ch27 (Shadbala) | `ingest_bphs_ch27_v1.py` | -- | ✅ Ingested |
| Ch34 (Planetary Combinations) | `ingest_bphs_ch34_v1.py` | -- | ✅ Ingested |
| Ch35-Ch44 (Yoga chapters, incl. Ch40/43/44) | `ingest_bphs_ch35_v1.py → ch44_v1.py` | -- | ✅ Ingested |
| **Total Phase 1** | | **~1,069 rules** | ✅ In MongoDB |

**Do NOT re-run Phase 1 scripts.** The upsert pattern is idempotent but re-running creates unnecessary noise in `import_batches` logs.

---

## What This Thread Ingests Now (Phase 2 -- new NLM-decoded chapters)

These chapters were decoded by the Phase 2 NLM thread and are NOT yet in MongoDB:

| Chapter | Title | Decoded Rules Folder |
|---|---|---|
| Ch03 | Exaltation / Debilitation / Own Sign | `BPHS_CC_Decode/` (3 part files) |
| Ch04 | Aspects, Natural Friends/Enemies | `BPHS_CC_Decode/` |
| Ch05 | Special Ascendants | `BPHS_CC_Decode/` |
| Ch06 | Sixteen Divisions (Vargas) | `BPHS_CC_Decode/` (2 part files) |
| Ch07 | Combustion thresholds | `BPHS_CC_Decode/` |
| Ch08 | Planetary Strengths | `BPHS_CC_Decode/` |
| Ch09 | Evils at Birth (Balarishta) | `BPHS_CC_Decode/` (2 part files) |
| Ch10 | Longevity indicators | `BPHS_CC_Decode/` |
| Ch11 | Judgement of Houses | `BPHS_CC_Decode/` |
| Ch25 | Karakamsha | `BPHS_CC_Decode/` (4 part files) |
| Ch26 | Arudha Padas | `BPHS_CC_Decode/` |
| Ch28 | Ista/Kashta Balas | `BPHS_CC_Decode/` (encode pass applied ✅) |
| Ch29 | Varga Bala | `BPHS_CC_Decode/` (2 part files) |
| Ch30 | Upa Pada | `BPHS_CC_Decode/` (3 part files, encode pass applied ✅) |
| Ch31 | Argala | `BPHS_CC_Decode/` (2 part files, encode pass applied ✅) |
| Ch32 | Bhava Karakas | `BPHS_CC_Decode/` (3 part files) |
| Ch33 | Yogas | `BPHS_CC_Decode/` (7 part files) |

**Canonical decode output folder:**
```
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/
```

---

## Folder Housekeeping -- A2 (Original Decode Thread) to Action Before Ingest

> **⚠️ ACTION FOR A2 THREAD (original decode thread):** Before running the ingest script, verify and archive superseded files. Do NOT proceed to ingest until this step is confirmed complete.

The decode folder contains both bare `_Rules.json` files AND numbered `_Rules_Part*.json` files for the same chapters. The bare files are superseded by the split Part files.

**A2 action:** For each chapter below, confirm the Part files are the canonical final output, then move the bare `_Rules.json` to a `_ARCHIVED/` subfolder inside `BPHS_CC_Decode/`. Do not delete -- TT may want to review diffs.

| Chapter | Move to _ARCHIVED/ (superseded) | Keep as canonical |
|---|---|---|
| Ch16 | `BPHS_Ch16_*_Rules.json` (bare) | `*_Rules_Part1.json`, `*_Rules_Part2.json` |
| Ch17 | `BPHS_Ch17_*_Rules.json` (bare) | `*_Rules_Part1.json`, `*_Rules_Part2.json` |
| Ch18 | `BPHS_Ch18_*_Rules.json` (bare) | `*_Rules_Part1.json` through `Part3.json` |
| Ch20 | `BPHS_Ch20_*_Rules.json` (bare) | `*_Rules_Part1.json`, `*_Rules_Part2.json` |
| Ch24 | `BPHS_Ch24_*_Rules.json` (bare) | `*_Rules_Part1.json` through `Part6.json` |
| Ch32 | `BPHS_Ch32_*_Rules.json` (bare) | `*_Rules_Part1.json`, `*_Rules_Part2.json` |
| Ch33 | `BPHS_Ch33_*_Rules.json` (bare) | `*_Rules_Part1.json` through `Part6.json` |

**After archiving:** Confirm total rule count from Part files only, then proceed to ingest script.

---

## 10 TT Items Resolved (encode pass applied 2026-05-31)

All 10 HIGH items resolved via GAI session 2026-05-30. Applied via `apply_vol1_encode.py`.

| ID | Rule | Resolution |
|---|---|---|
| TT-CH28-01 | Uchcha Rasmi formula | ✅ `(lon−deb)/180×8` |
| TT-CH28-03 | Ishta Phala formula | ✅ `(Uchcha+Cheshta−2)×5` |
| TT-CH28-04 | Subhanka table | ✅ neutral=8, extreme friend=22 |
| TT-CH06-03 | Bhamsa D27 | ✅ Modality-based (Movable→Aries, Fixed→Cancer, Mutable→Libra) |
| TT-CH06-01 | Trimsamsa even-sign | ✅ BOTH order AND widths reversed |
| TT-CH06-05 | Ch05/Ch06 ownership | ✅ Slokas 21-24 → Ch05 |
| TT-CH09-01 | Balarishta threshold | ✅ 24 years per BPHS Sanskrit |
| TT-CH09-04 | Gandanta zone | ✅ Both sides -- 3°20' water + 3°20' fire |
| TT-CH30-01 | Upa Pada formula | ✅ Arudha of 12th house (Chaukamba parity = commentary only) |
| TT-CH31-01 | Argala obstruction | ✅ From ORIGINAL house (Reading A) |

---

## 5 MED Items -- All Closed via PDF (2026-06-01) ✅

All 5 MED items resolved by direct PDF read (Ch06 pp.83-86, Ch09 pp.112-113, Ch30 pp.303-307, Ch31 p.314). Applied to rule JSON files via `apply_med_items_resolve.py`. No `pending_review` flags needed.

| ID | Chapter | Resolution | Rule(s) updated |
|---|---|---|---|
| TT-CH06-02 | Ch06 | ✅ Each Shashtiamsa = **30 minutes of arc** (half a degree). Fractional confirmed. PDF heading: "1/60th part of a sign or half-a-degree each." Formula: (degrees in sign × 2) ÷ 12 → remainder+1. | bphs1-ch06-016 |
| TT-CH09-02 | Ch09 | ✅ Oriental half = 10th cusp → 4th cusp via Lagna (houses 10-11-12-1-2-3). **Cusp-based, NOT sequential houses 1-6.** PDF Notes explicit. | bphs1-ch09-014 |
| TT-CH30-02 | Ch30 | ✅ Sign qualifier IS required. Mars+Saturn must occupy **2nd from Upa Pada** AND that 2nd must be a Mercury sign (nasal to wife) or Mars sign (Aries/Scorpio). Not Upa Pada sign itself. | bphs1-ch30-021, ch30-022 |
| TT-CH30-03 | Ch30 | ✅ Counting from **12th lord's position** confirmed. Count signs from 12th house to 12th lord, then count same from 12th lord forward = Upa Pada. Santhanam example explicit. | bphs1-ch30-001 |
| TT-CH31-02 | Ch31 | ✅ Quarter rule applies to **obstructor's position**, NOT Argala planet. 1st-quarter Argala → cancelled by 4th-quarter obstructor only. 2nd-quarter → 3rd-quarter obstructor. No partial Argala concept. | bphs1-ch31-010 |

**decode_notes and `resolution_status: {"TT-CHXX-XX": "PDF_resolved_2026-06-01"}` applied to all 6 rule objects.**

---

## Phase 2 Ingest Result -- Completed 2026-06-01

| Metric | Value |
|---|---|
| Batch ID | `bphs-vol1-phase2-v1-20260601` |
| Total rules | 696 |
| auto_approved | 491 (71%) |
| pending_human_review | 170 (24%) |
| flagged (TT/GAI) | 35 (5%) |
| contradictions | 0 |

**35 flagged rules -- TT/GAI review required:**

| Sub-group | Count | Chapter(s) | Action needed |
|---|---|---|---|
| Dhwaja as standalone Upagraha | 12 | Ch25 | GAI doctrinal -- not listed in Ch25 Upagraha catalogue rule-001 |
| Formula conflicts | 5 | Ch26, Ch28 | TT to resolve conflicting computation formulas |
| Doctrinal contradictions | 6 | Ch03, Ch04, Ch30, Ch32, Ch33 | GAI doctrinal review |
| Non-standard doctrine | 5 | Ch32, Ch33 | GAI doctrinal review (Anthyakaraka, Mercury-10th, Ketu broad, Sun-music) |
| Factual errors | 3 | Ch32 | Sun/Venus for father, Moon/Mars for mother, wife in 2nd house |
| Extreme Ch33 outcomes | 4 | Ch33 | GAI -- burn house / poison / anatomically specific outcomes |

**Schema bugs fixed during ingest (not in source files -- fixed in ingest script):**
1. `interpretation.*` absent from all source schemas → added `_map_interpretation()` + `_map_condition()` to `inject_fields()`
2. `source.batch_id` not set → validate_rules.py queries this field, ingest was setting only `ingest_batch_id` (top-level)

---

## Phase 1 NLM Status -- Updated 2026-06-01

Live MongoDB inspection (inspect_bphs_phase1_issues.py run 2026-06-01) resolved all 5 previously-tracked Phase 1 issues. Full detail in `BPHS_VOL1_NLM.md`.

| Issue | Previous status | Actual DB state | Action |
|---|---|---|---|
| 13 contradiction pairs Ch12-23 | Open (NLM queue) | ✅ 0 in DB -- resolved in prior session | NLM tracker updated -- closed |
| Ch15 PHR rate 25% | Open | ✅ 0 PHR, 100% auto-approved | NLM tracker updated -- closed |
| Ch19 PHR rate 33% | Open | ✅ 0 PHR, 100% auto-approved | NLM tracker updated -- closed |
| Ch34 flagged=15 | Open -- script pending | ✅ CLOSED 2026-06-01. 12 truncation → PHR. 3 content flags → auto_approved (GAI review). Live DB: flagged = 0. | Done |
| yoga_check 0 across Ch35-41 (197 rules) | Open | ✅ FALSE ALARM -- yoga_check IS populated at `condition.yoga_check`. Inspect script queried wrong field path (`validation.yoga_check`). Data fully present. | Inspect script corrected |

**1 remaining item does NOT block Phase 2 ingest. Run `patch_ch34_flagged.py` independently.**

---

## Ingest Script Instructions

**Script name:** `ingest_bphs_vol1_phase2.py`
**Reference pattern:** `backend/scripts/ingest_bphs_ch35_v1.py`
**Full pattern guide:** `KE_TEXTBOOK_DECODE/A2_INGEST_BRIEF.md` §Reference Ingest Scripts

```python
BATCH_ID  = "bphs-vol1-phase2-v1-20260601"
BOOK_NAME = "BPHS Vol 1"
SCIENCE   = "jyotish"        # NOT "vedic_astrology" -- match existing Phase 1 rules
```

**Step 1 -- Pre-ingest dedup (Strategy A -- rolling dedup against all ingested rules)**

Phase 1 and Phase 2 files share the same BPHS_CC_Decode folder, so use the prep script first:
```bash
# Separate Phase 1 and Phase 2 files into temp folders
python3 backend/scripts/prep_bphs_phase2_dedup_folders.py

# Dedup Phase 2 vs Phase 1 (same book, different chapters)
python3 backend/ke_dedup_script.py \
  --folder-a /tmp/bphs_phase2_rules/ \
  --folder-b /tmp/bphs_phase1_rules/ \
  --threshold 0.82 \
  --output-report backend/scripts/dedup_reports/dedup_bphs_phase2_vs_phase1.json

# Dedup Phase 2 vs BPHS Vol 2 (if Vol 2 decode folder exists)
python3 backend/ke_dedup_script.py \
  --folder-a /tmp/bphs_phase2_rules/ \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/" \
  --threshold 0.82 \
  --output-report backend/scripts/dedup_reports/dedup_bphs_phase2_vs_vol2.json
```

Review both reports. Paste summary to TT/CC before proceeding. Mark any genuine duplicates with `duplicate_candidate: true` in Phase 2 source JSONs.

**Step 2 -- Dry run (mandatory):**
```bash
python3 backend/scripts/ingest_bphs_vol1_phase2.py \
  --dry-run \
  --save backend/scripts/bphs_vol1_phase2_rules.json
```
Verify rule count. Check first and last rule in the saved JSON.

**Step 3 -- Upload:**
```bash
python3 backend/scripts/ingest_bphs_vol1_phase2.py \
  --upload backend/scripts/bphs_vol1_phase2_rules.json \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

**Step 4 -- Validate:**
```bash
python3 backend/scripts/validate_rules.py \
  --batch-id bphs-vol1-phase2-v1-20260601 \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

**Step 5 -- Patch any flagged rules** (see `INGEST_PROCESS_BRIEF.md` Step 5-6 for patch script template)

**Step 6 -- Commit:**
```bash
git add backend/scripts/ingest_bphs_vol1_phase2.py \
        backend/scripts/bphs_vol1_phase2_rules.json \
        backend/scripts/INGEST_NOTES.md
git commit -m "chore(ingest): BPHS Vol 1 Phase 2 -- Ch03-Ch11, Ch25-26, Ch28-33 (N rules)"
```

---

## Fields to Inject on Every Rule

```python
rule["approval_status"] = "pending_review"      # matches Phase 1 convention
rule["ingested_at"]     = datetime.now(timezone.utc).isoformat()
rule["ingest_batch_id"] = "bphs-vol1-phase2-v1-20260601"
rule["source_book"]     = "BPHS Vol 1"
```

Special cases:
- Ch19 (8th House) rules involving death/longevity → add `claim_axis: "longevity"`
- 5 MED items (TT-CH30-02 through TT-CH31-02 affected rules) → add `pending_review: True`

---

## Post-Ingest Dedup Targets

BPHS Vol 1 is the primary reference -- every other book deduped against it.

| Book | Expected overlap |
|---|---|
| BPHS Vol 2 | Same source text -- run at same time |
| Phaladeepika | HIGH -- direct commentary on BPHS |
| 300 Combinations | Moderate |
| KP Astrology | System-level differences (not errors) |

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-06-01*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
*INGEST_PROCESS_BRIEF.md freeze notice (14 May 2026) is STALE -- freeze lifted 2026-05-17.*
