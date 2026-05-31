# Thread Brief -- 300 Horoscopes Vol 1 KE Ingest
## Status · Open Items · Immediate Next Action

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31
> For: 300 Horoscopes Vol 1 Ingest Thread
> Status: **✅ READY -- All 3 previously blocked rules cleared 2026-05-31. Priority 2 ingest.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_300HOROSCOPES_INGEST.md` for all 300 Horoscopes Vol 1 KE Ingest.

---

## What This Thread Owns

"Three Hundred Important Combinations" Vol 1 -- 57 natal chart interpretation rules based on benchmark horoscopes. Priority 2 in the approved ingest sequence (run after 300 Combinations).

---

## Canonical Output Folder

```
/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode/
```

OCR report: `H300_OCR_Issues_Report.docx`
Duplicate report: `H300_DuplicateCandidateReport.md`

---

## Rule Count

| Metric | Value |
|---|---|
| Total rules | 57 |
| Active rules | 57 |
| Previously blocked rules | 3 (all cleared ✅ 2026-05-31) |
| Duplicate candidates | 47 total (29 merge-safe, 16 keep-both, 2 TT decision at approval) |

---

## Previously Blocked Rules -- Now Cleared (2026-05-31)

| Rule | Issue | Resolution |
|---|---|---|
| h300-s01-016 | Nakshatra Pada table accuracy | ✅ All 12 signs match PDF exactly. Abbreviated names correctly expanded. |
| h300-s04-004 | Empty-level-skip in node sequencing | ✅ p.28 confirms text-native: "Hence Rahu will give result in the following order" |
| h300-s04-005 | Cumulative level activation | ✅ p.28 confirms: "give result of Jupiter, Saturn and Mars... respectively" -- all active levels listed simultaneously |

All 3 former blockers are validated directly from PDF. These rules ingest with full confidence.

---

## Duplicate Report Summary

File: `H300_DuplicateCandidateReport.md`

| Category | Count | Action |
|---|---|---|
| Merge-safe duplicates | 29 | Ingest the canonical rule; mark duplicate as superseded |
| Keep-both (complementary) | 16 | Ingest both; cross_text_matches populated by dedup script |
| Needs TT decision | 2 | Ingest with `pending_review:true`; TT resolves at approval stage |

**The 2 TT-decision items do NOT block ingest.** Ingest them as `pending_human_review` with a flag note. TT reviews when approving.

---

## ⚠️ Phase 2 Schema Learnings -- Apply Before Writing Script

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). Apply from the start.**

**Run schema audit on decode folder:**
```bash
python3 << 'EOF'
import json
from pathlib import Path
FOLDER = Path("/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode/")
for f in sorted(FOLDER.glob("*.json"))[:4]:
    data = json.loads(f.read_text())
    rules = data.get("rules", data) if isinstance(data, dict) else data
    if not isinstance(rules, list) or not rules: continue
    r = rules[0]
    interp = r.get("interpretation") or {}
    print(f"\n=== {f.name} ===")
    print(f"  keys: {list(r.keys())[:10]}")
    print(f"  interpretation.detailed: {repr((interp.get('detailed') or '')[:80])}")
    print(f"  condition dict: {isinstance(r.get('condition'), dict)}")
EOF
```

**Ingest script checklist:**
- [ ] `source["batch_id"] = BATCH_ID` inside `inject_fields()` -- NOT just top-level `ingest_batch_id`
- [ ] `interpretation.detailed` and `interpretation.summary` non-empty on every rule
- [ ] `condition` is a non-empty dict on every rule
- [ ] Pre-upload local structural check: `Issues: 0`

**Three-bucket triage for validation results:**
- Bucket A: Artifact only → `auto_approved`; Bucket B: Validator error → PHR; Bucket C: Genuine → flagged TT/GAI

---

## Ingest Instructions

**Step 1 -- Pre-ingest dedup:**
```bash
python3 backend/ke_dedup_script.py \
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode/" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/" \
  --output-report dedup_h300_vs_bphs_vol1.md \
  --threshold 0.82
```
Also run against 300 Combinations if already ingested.

**Step 2 -- Inject on every rule:**
```python
rule["approval_status"]    = "pending_human_review"
rule["ingested_at"]        = datetime.now(timezone.utc).isoformat()
rule["ingest_batch_id"]    = "300_horoscopes_vol1_v1"
rule["source_book"]        = "300 Horoscopes Vol 1"
rule["source"]["batch_id"] = "300_horoscopes_vol1_v1"  # MANDATORY -- validate_rules.py queries this
```

**Step 3 -- Special field handling:**
- The 2 TT-decision duplicate candidates: set `pending_review: true` + add `decode_notes` describing the conflict
- 6 superseded rules (documented in `H300_S04_Nodes_Diagnostic.md`): set `active: false` before insert
- 47 cross-book flags: leave `cross_text_matches: null` -- dedup script will populate post-ingest

---

## Open Items (non-blocking)

| Item | Detail | Action |
|---|---|---|
| 2 TT duplicate decisions | Ambiguous whether to merge or keep | Ingest with `pending_review:true`. TT decides at approval stage. |
| 47 cross-book flags | Against SBC + Longevity books | Informational only. Do not block ingest. |
| 15 test vectors | Present in decode folder | Validate ingest correctness against test vectors post-insert |

---

## Post-Ingest Dedup Targets

| Target | Expected Overlap |
|---|---|
| BPHS Vol 1 | Moderate -- benchmark chart interpretation methods |
| 300 Combinations | Low-moderate -- both Raman but different rule types |
| Longevity Unnatural Death | Low but watch for death-timing rules |

---

## Immediate Next Action

1. Confirm 6 superseded rules from `H300_S04_Nodes_Diagnostic.md` have `active:false` set
2. Run dedup against BPHS Vol 1 and 300 Combinations local folders
3. Run ingest script (dry-run first → review → upload)
4. Verify: `db.interpretation_rules.count_documents({"source_book": "300 Horoscopes Vol 1"})` → expect 57
5. Note 2 TT-decision rules in `import_batches` record for tracking

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
