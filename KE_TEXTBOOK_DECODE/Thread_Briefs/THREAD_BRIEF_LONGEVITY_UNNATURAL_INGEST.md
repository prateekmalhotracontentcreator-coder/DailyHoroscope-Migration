# Thread Brief -- Longevity & Unnatural Death KE Ingest
## Status · Open Items · Immediate Next Action

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31
> For: Longevity Unnatural Death Ingest Thread
> Status: **✅ READY -- All 5 HIGH items resolved 2026-05-31. Priority 2 ingest (alongside 300 Horoscopes).**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_LONGEVITY_UNNATURAL_INGEST.md` for all Longevity Unnatural Death KE Ingest.

---

## What This Thread Owns

"Longevity & Unnatural Death" -- 44 rules + 2 benchmark case studies covering unnatural/premature death indicators. This is Priority 2 in the approved ingest sequence (run alongside 300 Horoscopes Vol 1 after 300 Combinations).

**Important distinction:** This book is NOT the same as "Longevity 58 Chapters" (which is hard-blocked). This book is small (44 rules), fully resolved, and clear to ingest.

---

## Canonical Output Folder

```
/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/
```

Temple Team brief: `LU_TempleTeam_Brief.docx`
PDF validation results: `LU_PDF_Validation_Results.md`

---

## Rule Count

| Metric | Value |
|---|---|
| Total rules | 44 |
| Benchmark case studies | 2 (CS1, CS2) |
| HIGH items | 5 -- all resolved ✅ |
| MEDIUM items | 10 -- ingest with `pending_review:true` |
| LOW items | 6 -- safe to ingest as-is |

---

## HIGH Items -- All Resolved (2026-05-31)

| Rule | Resolution |
|---|---|
| lu-s04-001 ("should") | ✅ Confirmed weighted condition, not hard gate. PDF p.6/p.9. |
| lu-s04-014 (AND/OR logic) | ✅ 06 AND Mars required; maraka OR badhaka either sufficient |
| lu-s04-003/004 (5-level chain) | ✅ 5-level chain confirmed; Level 5 "connected" = conjunction + aspect |
| lu-s04-010 ("lethal planet") | ✅ Must be BOTH maraka AND badhaka simultaneously (AND logic) |
| lu-s04-013 (progressive houses) | ✅ {3, 10, 11} only -- 6th house excluded |

**CS1 benchmark corrections applied:**
- Mercury: 19°Aq12'36" (Sata 4) -- DataTable confirmed
- Jupiter: Fixed 00°Pi60' → 00°Pi59'37" in DataTables

---

## ⚠️ Phase 2 Schema Learnings -- Apply Before Writing Script

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). Apply from the start.**

**Run schema audit on decode folder:**
```bash
python3 << 'EOF'
import json
from pathlib import Path
FOLDER = Path("/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/")
for f in sorted(FOLDER.glob("*.json"))[:3]:
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
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode/" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/" \
  --output-report dedup_longunnat_vs_bphs_vol1.md \
  --threshold 0.82
```
Also run against 300 Combinations and 300 Horoscopes if already ingested.

**Step 2 -- Inject on every rule:**
```python
rule["approval_status"]    = "pending_human_review"
rule["ingested_at"]        = datetime.now(timezone.utc).isoformat()
rule["ingest_batch_id"]    = "longevity_unnatural_v1"
rule["source_book"]        = "Longevity & Unnatural Death"
rule["claim_axis"]         = "longevity"          # All rules in this book
rule["source"]["batch_id"] = "longevity_unnatural_v1"  # MANDATORY -- validate_rules.py queries this
```

**Step 3 -- Special field handling:**
- 10 MEDIUM items: set `pending_review: true`
- 6 LOW items: ingest as-is, no flags
- CS1/CS2 benchmarks: ingest as separate document type if schema supports `rule_type: "benchmark"`, else skip benchmarks and ingest rules only
- All rules should carry `claim_axis: "longevity"` (this is the defining claim axis for this entire book)

---

## Open Items (non-blocking)

| ID | Priority | Detail |
|---|---|---|
| 10 MEDIUM items | 🟡 MED | Various conditional ambiguities. Safe to ingest with `pending_review:true`. TT resolves at approval stage. |
| 6 LOW items | 🟢 LOW | Cosmetic -- no action needed |
| CS1 Jupiter rounding | Cosmetic | Fixed in DataTables. No rule doc change needed. |

---

## Post-Ingest Dedup Targets

| Target | Expected Overlap |
|---|---|
| BPHS Vol 1 Ch43/44 | HIGH -- BPHS longevity/maraka chapters are the primary source for these rules |
| KP Astrology (longevity rules) | Moderate -- KP has specific longevity factors |
| 300 Horoscopes Vol 1 | Low |

---

## Immediate Next Action

1. Run dedup against BPHS Vol 1 and 300 Combinations local folders
2. Add `claim_axis: "longevity"` to all 44 rules
3. Set `pending_review: true` on 10 MEDIUM items
4. Run ingest script (dry-run → review → upload)
5. Verify: `db.interpretation_rules.count_documents({"source_book": "Longevity & Unnatural Death"})` → expect 44

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
