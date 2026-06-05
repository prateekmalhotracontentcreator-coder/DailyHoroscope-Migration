# Thread Brief -- Sarvato Bhadra Chakra (SBC) KE Ingest
## Status · Open Items · Immediate Next Action

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31 | Last updated: 2026-06-05 (CC -- all 4 CRITICAL OCR items resolved from source PDFs)
> For: SBC Ingest Thread
> Status: **⛔ BLOCKED ON ATLAS -- Ingest script ready + dry-run clean (Issues: 0). Atlas SSL timeout blocking live run. All content gates cleared. Run when Atlas recovers.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_SBC_INGEST.md` for all Sarvato Bhadra Chakra KE Ingest.

---

## What This Thread Owns

"Sarvato Bhadra Chakra" -- 181 decoded rules for the SBC transit and electional astrology system. Priority 3 in the approved ingest sequence. **Currently blocked** -- requires TT resolution of 7 priority conflicts and NLM/GAI resolution of 4 CRITICAL OCR items before ingest can begin.

---

## Canonical Output Folder

```
/Users/apple/Documents/Knowledge Engine_eBooks/New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/
```

Note: Two SBC folders exist (`1. Sarvato Bhadra Chakra/` and `1. Sarvato Bhadra Chakra_V2/`). Use **V2** only -- it is the canonical corrected output. Do not read from the non-V2 folder.

Master decode summary: `SBC_Master_Decode_Summary.md` (in the V2 folder)
OCR report: `SBC_OCR_Issues_Report.docx`

---

## Rule Count

| Metric | Value |
|---|---|
| Total rules | 181 |
| TT conflict rules | 7 (blocking) |
| Source gap rules | 24 open questions (7 resolved, 17 remaining) |
| CRITICAL OCR items | 4 |

---

## Blockers Status

### ✅ Blocker 0: 6 Architecture / Collection Decisions -- CLEARED 2026-05-20

All 6 lookup collection schemas confirmed in `SBC_Session_Answers_2026-05-20.md`. The `sapt_salaka_coordinates` table data recovered via PDF read (see C-02 below). 14 mirror pairs now encoded in sbc-ch18-004 condition JSON.

| Collection name | Status |
|---|---|
| `vedha_coordinates` | Schema decided ✅ |
| `latta_coordinates` | Schema decided ✅ |
| `upgraha_coordinates` | Schema decided ✅ |
| `planet_significations` | Schema decided ✅ |
| `sbc_geopolitical_coordinates` | Schema decided ✅ |
| `sapt_salaka_coordinates` | Schema decided ✅; 14 mirror pairs encoded in sbc-ch18-004 |

---

### ✅ Blocker 1: 7 TT Priority Conflicts -- CLEARED 2026-05-20

All 7 conflicts reviewed by GAI (all AGREE) and confirmed by TT. Encoding directives in `SBC_Conflict_Resolutions_2026-05-20.md`.

---

### ✅ Blocker 2: 4 CRITICAL OCR Items -- CLEARED 2026-06-05

All 4 items resolved by CC directly reading source PDFs (Ch 10 + Ch 18). JSON source files updated.

| ID | Description | Resolution |
|---|---|---|
| C-01 | Chandra Kalanal index -- position results missing | ✅ Recovered from Ch18 p.151. New rule sbc-ch18-011 added with 28-position result table. Death positions: 1,2,7,8,9,14,15,16,21,22,23,28. Benefic: 4,5,11,12,18,19,25,26. |
| C-02 | Sapt Salaka table -- mirror pairs missing | ✅ Recovered from Ch18 p.152. All 14 mirror pairs (7 N-S + 7 E-W) encoded in sbc-ch18-004 condition block. |
| C-03 | Star rank results positions 11-15, 17, 20-22, 24 missing | ✅ **False alarm.** All positions confirmed present in Ch10 pp.97-98 -- they are 2nd/3rd repetitions of the 9-star cycle. sbc-ch10-023 updated with full 10-27 position table. |
| C-04 | Dhuajadi Swan vs Vrisa Devanagari overlap | ✅ Confirmed: Swan = retroflex series (ट ठ ड ढ ण), Vrisa = dental series (त थ द ध न). sbc-ch18-007 updated with full Devanagari Unicode arrays. |

### 🟠 Blocker 3: 17 Remaining Open Questions (Source Gaps) -- TT ACTION REQUIRED

7 of 24 original open questions (OQ-08-01 through OQ-18-01) have been resolved and documented. 17 remain open.

**Action: TT to review the 17 remaining OQs in `SBC_Master_Decode_Summary.md` -- resolve as either "close with source_gap:true" or "requires NLM/GAI re-read". Once TT completes this, SBC is READY TO INGEST.**

---

## ⚠️ Phase 2 Schema Learnings -- Apply When Unblocked

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). SBC uses custom lookup collections not seen in other books -- schema audit is critical.**

**Ingest script checklist (for when all blockers are cleared):**
- [ ] `source["batch_id"] = BATCH_ID` inside `inject_fields()` -- NOT just top-level `ingest_batch_id`
- [ ] Run schema audit on `Sarvato Bhadra Chakra_V2/` folder first -- custom lookup collections mean the JSON schema may differ from standard rule books
- [ ] `interpretation.detailed` and `interpretation.summary` non-empty -- SBC coordinate/lookup rules may not have standard interpretation fields; add `_map_interpretation()` if needed
- [ ] `condition` is a non-empty dict -- add `_map_condition()` if source uses `conditions` list
- [ ] Pre-upload local structural check: `Issues: 0`
- [ ] The 6 custom lookup collections (`vedha_coordinates`, `latta_coordinates`, etc.) must be seeded BEFORE any rule ingest

**Three-bucket triage for validation results:** A (artifact → `auto_approved`) · B (validator error → PHR) · C (genuine → flagged TT/GAI)

---

## Ingest Instructions (when unblocked)

**Step 1 -- Pre-ingest dedup:**
```bash
python3 backend/ke_dedup_script.py \
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/" \
  --output-report dedup_sbc_vs_bphs_vol1.md \
  --threshold 0.82
```

**Step 2 -- Inject on every rule:**
```python
rule["approval_status"]    = "pending_human_review"
rule["ingested_at"]        = datetime.now(timezone.utc).isoformat()
rule["ingest_batch_id"]    = "sbc_v1"
rule["source_book"]        = "Sarvato Bhadra Chakra"
rule["source"]["batch_id"] = "sbc_v1"  # MANDATORY -- validate_rules.py queries this
```

**Step 3 -- Special handling:**
- Rules with unresolved source gaps: set `source_gap: true` + `pending_review: true`
- Rules where TT adopted one reading: mark rejected reading as `active: false`

---

## Open Items Summary

| Category | Count | Status |
|---|---|---|
| TT priority conflicts | 7 | ✅ CLEARED 2026-05-20 |
| Architecture/collection decisions | 6 | ✅ CLEARED 2026-05-20 |
| CRITICAL OCR items | 4 | ✅ CLEARED 2026-06-05 |
| Remaining source gap OQs | 17 | 🟠 TT ACTION -- close as `source_gap:true` or escalate to NLM/GAI |
| Resolved OQs | 7 | ✅ Done -- documented in SBC_Master_Decode_Summary.md |

---

## Post-Ingest Dedup Targets (when ready)

| Target | Expected Overlap |
|---|---|
| BPHS Vol 1 | Low-moderate -- SBC is a transit/electional system, different from natal BPHS |
| 300 Horoscopes Vol 1 | Low |
| 300 Combinations | Low |

---

## Immediate Next Action

**When Atlas recovers (CC):**
```bash
cd /Users/apple/DailyHoroscope-Migration
python3 backend/scripts/ingest_sbc_v1.py --mongo-url "$MONGO_URL"
```
Then run doctrinal validation:
```bash
python3 backend/validate_rules.py --batch-id sbc_v1_20260605 --mongo-url "$MONGO_URL"
```

**TT (parallel, not blocking):**
1. Open `SBC_Master_Decode_Summary.md`
2. Review 17 remaining source gap OQs -- mark each as `source_gap:true` or escalate to NLM/GAI
3. These can be patched post-ingest via a separate `patch_sbc_source_gaps.py` script

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
