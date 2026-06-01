# Thread Brief -- BPHS Vol 2 KE Ingest
## Status · Open Items · Immediate Next Action

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31
> For: BPHS Vol 2 Ingest Thread
> Status: **🟡 AWAITING GAI -- Ingest + validation complete 2026-06-01. 7 rules pending GAI triage response.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_BPHS_VOL2_INGEST.md` for all BPHS Vol 2 KE Ingest.

---

## What Is Already In MongoDB (do not re-ingest)

Chapters 47, 48, and 52-60 of BPHS Vol 2 are **already ingested** (confirmed from `.claude/ke/ingest/BPHS_VOL2_INGEST.md`, last updated 2026-05-08):

| Metric | Value |
|---|---|
| Chapters already in MongoDB | Ch47, Ch48, Ch52-Ch60 |
| Total rules (Phase 1) | ~2,227 |
| Auto-approved | ~1,092 |
| Pending human review | ~582 |
| Flagged (pending triage) | ~190 |

Ch49-51 were originally excluded by co-founder decision. That exclusion is **superseded** -- A1 explicitly cleared Ch49-51 for ingest (confirmed 2026-05-31). This thread ingests Ch49-51 only.

---

## What This Thread Owns (New -- Ch49-51 only)

BPHS Vol 2, Chapters 49-51 -- the Navamsa Dasa chapters (249 new rules). These are the ONLY chapters not yet in MongoDB. Vol 2 expansion beyond Ch51 is a separate future sprint -- NOT part of this thread's scope.

---

## Canonical Output Folder

```
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/
```

All rule JSON files for Ch49, Ch50, Ch51 are present in this folder. Do NOT write to `BPHS Vol 2 Decode/` or `BPHS Vol 2/` -- those are raw source folders.

---

## Rule Count (confirmed 2026-05-31)

| Chapter | Title | Rules | Active | Notes |
|---|---|---|---|---|
| Ch49 | Navamsa Dasa -- Sign Outcomes | 154 | 153 | 1 source gap rule (active:false, source_gap:true) |
| Ch50 | Navamsa Dasa -- Planet States | 73 | 73 | Combustion thresholds → BPHS Ch07 |
| Ch51 | Navamsa Bhoga | 22 | 22 | Rule 020 provisional:true (algorithm verify pending) |
| **Total** | | **249** | **248** | |

---

## What Has Been Done

| Action | Date | Result |
|---|---|---|
| Ch49-51 initial decode | Prior session | 249 rules extracted |
| 10 OCR items resolved | 2026-05-31 | All 10 applied via `apply_vol2_encode.py` |
| Ch49 placeholder rules replaced | 2026-05-31 | 5 OCR placeholders → active rules; 134→154 total |
| bphs2-ch49-gemini-pada-8-gap | 2026-05-31 | SOURCE GAP confirmed -- active:false, source_gap:true |
| Ch50 rule 041 | 2026-05-31 | decode_notes + Ch07 combustion cross-ref added |
| Ch51 rule 020 | 2026-05-31 | provisional:true + decode_notes added |
| Dedup: Vol2 vs Vol1 local | 2026-06-01 | 0 duplicates, 0 contradictions (515K pairs) |
| Dedup: Vol2 vs MongoDB (8,618 rules) | 2026-06-01 | 0 duplicates, 0 contradictions (3M pairs) |
| 249 rules ingested to MongoDB | 2026-06-01 | approval_status: pending_review, batch: bphs-vol2-ch49-51-v1 |
| Validation Stage 1 (structural) | 2026-06-01 | 0 failures / 249 |
| Validation Stage 2 (Claude quality) | 2026-06-01 | 98 auto_approved, 131 PHR, 20 flagged |
| Validation Stage 3 (contradictions) | 2026-06-01 | 5 pairs detected (all false positives -- complementary polarity rules) |
| Bucket A triage (13 rules) | 2026-06-01 | 13 truncation-artifact rules patched to auto_approved |
| GAI query brief prepared | 2026-06-01 | 7 flagged rules + 1 ambiguous contradiction pair sent to GAI for review |

**GAI resolution log:** `BPHS_Vol2_CC_Decode/BPHS_Vol2_GAI_Resolutions.md`

---

## Resolved OCR Items (all 10 cleared 2026-05-31)

| ID | Chapter | Resolution |
|---|---|---|
| Ch49-Virgo | Ch49 | ✅ 9 individual outcomes confirmed (PDF p.598-599) |
| Ch49-Libra | Ch49 | ✅ 9 individual outcomes confirmed |
| Ch49-Gemini-P7 | Ch49 | ✅ Taurus Amsa / weapon injury (PDF p.597) |
| Ch49-Gemini-P9 | Ch49 | ✅ Gemini Amsa / enjoyment (PDF p.597) |
| Ch49-Gemini-P8 | Ch49 | 🚨 SOURCE GAP -- absent from Santhanam text. active:false, source_gap:true |
| Ch49-Scorpio | Ch49 | ✅ Cancer/Leo Amsa confirmed |
| Ch49-Aquarius | Ch49 | ✅ Aries/Taurus Amsa confirmed |
| Ch49-Remedies | Ch49 | ✅ Generic Shanti Karma only -- no specific deities in text |
| Ch50-Combust | Ch50 | ✅ BPHS Ch07 thresholds apply; Ch50 does not specify degrees |
| Ch51-Bhoga | Ch51 | ✅ Provisional accept -- algorithm verified mathematically |

---

## ⚠️ Phase 2 Schema Learnings -- Apply Before Writing Script

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). These failures cost a full re-upload cycle. Apply from the start.**

**Run schema audit before writing the ingest script:**
```bash
python3 << 'EOF'
import json
from pathlib import Path
FOLDER = Path("/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/")
for f in sorted(FOLDER.glob("*.json")):
    data = json.loads(f.read_text())
    rules = data.get("rules", data) if isinstance(data, dict) else data
    if not isinstance(rules, list) or not rules: continue
    r = rules[0]
    interp = r.get("interpretation") or {}
    print(f"\n=== {f.name} ===")
    print(f"  keys: {list(r.keys())[:10]}")
    print(f"  interpretation.detailed: {repr((interp.get('detailed') or '')[:80])}")
    print(f"  condition dict: {isinstance(r.get('condition'), dict)} | conditions list: {bool(r.get('conditions'))}")
EOF
```

**Ingest script checklist:**
- [ ] `source["batch_id"] = BATCH_ID` inside `inject_fields()` -- NOT just top-level `ingest_batch_id`; validate_rules.py queries `source.batch_id`
- [ ] `interpretation.detailed` and `interpretation.summary` are non-empty (add `_map_interpretation()` helper if source uses `claim`, `full_text`, `result` instead)
- [ ] `condition` is a non-empty dict (add `_map_condition()` if source uses `conditions` list)
- [ ] JSON loader handles both `{"rules":[...]}` dict-format and `[...]` list-format
- [ ] Pre-upload local structural check returns `Issues: 0` before uploading

**Copy `_map_interpretation()` + `_map_condition()` from `backend/scripts/ingest_bphs_vol1_phase2.py`** as the starting template for any schema mapping work.

**Three-bucket triage for validation results (post-validate step):**
- Bucket A: Data artifact only (summary truncated, detailed OK) → patch to `auto_approved`
- Bucket B: Validator doctrinal error (validator made a wrong Vedic claim -- cross-check PDF first) → PHR with `validator_error:true` note
- Bucket C: Genuine flag (Codex fabrication, real contradiction, source gap) → stay flagged, TT/GAI queue

---

## Ingest Instructions

**Step 1 -- Pre-ingest dedup (MANDATORY before inserting to MongoDB):**
```bash
python3 backend/ke_dedup_script.py \
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/" \
  --output-report dedup_bphs_vol2_vs_vol1.md \
  --threshold 0.82
```
BPHS Vol 1 × Vol 2 dedup is essential -- same source text, overlap expected.

**Step 2 -- Write ingest script:**
Pattern from `backend/scripts/ingest_bphs_ch35_v1.py` (see `A2_INGEST_BRIEF.md` §Reference Ingest Scripts).
Target collection: `interpretation_rules`. Batch tracking: `import_batches`.

**Step 3 -- Inject these fields on every rule before insert:**
```python
rule["approval_status"]    = "pending_human_review"
rule["ingested_at"]        = datetime.now(timezone.utc).isoformat()
rule["ingest_batch_id"]    = "bphs-vol2-ch49-51-v1"
rule["source_book"]        = "BPHS Vol 2"
rule["source"]["batch_id"] = "bphs-vol2-ch49-51-v1"  # MANDATORY -- validate_rules.py queries this
```

**Step 4 -- Special handling:**
- `bphs2-ch49-gemini-pada-8-gap`: already has `active:false, source_gap:true` -- include in ingest but do not activate
- Ch51 rule 020: already has `provisional:true` -- include, ingest thread note this for TT review before approval
- Ch50 combustion rules: do NOT override with BPHS Ch07 thresholds in the rule document -- the decode_notes field already carries the cross-reference

---

## Open Items

| ID | Priority | Detail | Status |
|---|---|---|---|
| Ch49-Gemini-P8 | Source Gap | bphs2-ch49-gemini-pada-8-gap -- filed as M-38. TT to source Santhanam full text. | Open |
| Ch51 rule 020 | Provisional | Algorithm verified but not co-founder reviewed. provisional:true in rule. | Open |
| Vol 2 expansion | Future sprint | Ch46-Ch48 and chapters beyond Ch51 -- NOT in scope for this thread. Separate sprint. | Open |
| **GAI query (7 rules)** | **HIGH** | `GAI_Query_BPHS_Vol2_Ch49_51_Flagged_Rules.md` -- 7 flagged rules + 071/072 contradiction pair need GAI verdict. After response: apply Bucket B patches (PHR + validator_error:true) or reject as appropriate. | **Awaiting GAI** |
| 5 false contradiction pairs | Medium | Rules 003/015/046, 015/039, 020/021 -- all complementary polarity rules. Confirm with GAI then clear contradiction flags and restore to auto_approved. | Awaiting GAI confirmation |
| Co-founder approval | Blocker | 111 auto_approved rules await co-founder sign-off for `approved` status and live serving. | Blocked on sign-off |

---

## Post-Ingest Dedup Targets

| Target | Relationship | Expected Overlap |
|---|---|---|
| BPHS Vol 1 | Same source text | Moderate -- Dasa rules are largely unique to Vol 2 |
| Phaladeepika Adhyaya XIX | Vimshottari Dasa chapter | Low -- KP system differences |

---

## Immediate Next Action

1. ✅ Run `ke_dedup_script.py` against BPHS Vol 1 decode folder -- DONE (0 dup, 0 contra)
2. ✅ Review dedup report -- DONE (clean)
3. ✅ Write and run `ingest_bphs_vol2_ch49-51.py` -- DONE (249 rules in MongoDB)
4. ✅ Validate (Stages 1-3) -- DONE (111 auto_approved, 131 PHR, 7 flagged)
5. ✅ Bucket A triage -- DONE (13 rules patched to auto_approved)
6. ⏳ **GAI review** -- Share `KE_TEXTBOOK_DECODE/GAI_Query_BPHS_Vol2_Ch49_51_Flagged_Rules.md` with GAI. After response: apply Bucket B/C decisions.
7. ⏳ **Co-founder approval** -- After GAI triage resolved, present 111+ auto_approved rules for sign-off.

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
