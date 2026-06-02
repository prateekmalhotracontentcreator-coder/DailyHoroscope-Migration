# Thread Brief -- Destiny Numerology KE Ingest
## Status · Open Items · Immediate Next Action

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31
> For: Destiny Numerology Ingest Thread
> Status: **🟠 NEAR READY -- OCR pass required before ingest. 2 CRITICAL + 10 HIGH items outstanding.**

---

## One-Liner

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_DESTINY_NUMEROLOGY_INGEST.md` for all Destiny Numerology KE Ingest.

---

## What This Thread Owns

"Your Destiny Is in Your Name & DOB" -- 189 decoded rules across Ch01-Ch15. Priority 3 in the approved ingest sequence. Cannot ingest until 2 CRITICAL and 10 HIGH OCR items are resolved via NLM/GAI pass.

---

## Canonical Output Folder

```
/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/
```

OCR report: `Book_Wide_OCR_Inconsistencies_Report.docx` -- read this before any action.

---

## Rule Count

| Metric | Value |
|---|---|
| Total rules (Ch01-15) | 189 |
| Chapters decoded | 15 of ~20 |
| Schema | `name_options[]` array with `preferred` / `valid` / `rejected` values |
| `computation_verified` field | Added to Ch15 test vector rules |

---

## OCR Issues -- CRITICAL (must resolve before ingest)

| ID | Chapter | Issue |
|---|---|---|
| CRITICAL-1 | Ch17 (future sprint) | Number 3 Amethyst gemstone assignment -- contradicts standard numerology |
| CRITICAL-2 | Ch19 (future sprint) | Two element systems conflict -- fire/water assignments differ between chapters |

> Note: Ch17 and Ch19 are not yet decoded (future sprint). These CRITICAL items do not block the Ch01-15 ingest -- they affect chapters outside the current decoded set. Ch01-15 can be ingested once the 10 HIGH items are cleared.

---

## OCR Issues -- HIGH (must resolve before Ch01-15 ingest)

| Count | Source | Action |
|---|---|---|
| 10 HIGH items | `Book_Wide_OCR_Inconsistencies_Report.docx` | NLM/GAI pass on each item |
| 12 additional (Ch15 companion report) | Ch15 companion OCR report | NLM/GAI pass |

**Total to resolve before ingest: 10 HIGH items (29 main + Ch15 companion combined list -- 10 are HIGH priority).**

Send the `Book_Wide_OCR_Inconsistencies_Report.docx` to the NLM/GAI decode thread with instruction: "Resolve all HIGH items. Reference the PDF directly for each. Provide resolution in the same format as `LU_PDF_Validation_Results.md`."

---

## Ch15 Test Vectors -- Status

| Metric | Value |
|---|---|
| Total test vectors | 50 |
| Reviewed | 5 ✅ |
| Remaining | 45 (go-ahead given 2026-05-22) |
| Schema finalized | `name_options[]` with controlled vocabulary |
| `computation_verified` field | Added to Ch15 test vector rules |

**Wait for all 50 Ch15 test vectors to be confirmed before ingesting Ch15 rules.** Ch01-Ch14 can proceed once HIGH items are cleared.

---

## ⚠️ Phase 2 Schema Learnings -- Apply Before Writing Script

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). Destiny Numerology uses a custom `name_options[]` schema -- the standard schema audit is especially important here.**

**Run schema audit on decode folder before writing the script:**
```bash
python3 << 'EOF'
import json
from pathlib import Path
FOLDER = Path("/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/")
for f in sorted(FOLDER.glob("*.json"))[:4]:
    data = json.loads(f.read_text())
    rules = data.get("rules", data) if isinstance(data, dict) else data
    if not isinstance(rules, list) or not rules: continue
    r = rules[0]
    interp = r.get("interpretation") or {}
    print(f"\n=== {f.name} ===")
    print(f"  keys: {list(r.keys())[:10]}")
    print(f"  interpretation.detailed: {repr((interp.get('detailed') or '')[:80])}")
    print(f"  condition dict: {isinstance(r.get('condition'), dict)} | name_options: {bool(r.get('name_options'))}")
EOF
```

**Ingest script checklist:**
- [ ] `source["batch_id"] = BATCH_ID` inside `inject_fields()` -- NOT just top-level `ingest_batch_id`
- [ ] `interpretation.detailed` and `interpretation.summary` non-empty -- the `name_options[]` schema may NOT pre-populate these; check and add `_map_interpretation()` if needed
- [ ] `condition` is a non-empty dict on every rule
- [ ] `science_id` confirmed: likely `"numerology"` (verify against existing numerology rules in MongoDB)
- [ ] Pre-upload local structural check: `Issues: 0`

**Three-bucket triage for validation results:**
- Bucket A: Artifact → `auto_approved`; Bucket B: Validator error → PHR; Bucket C: Genuine → flagged TT/GAI

---

## Ingest Instructions (when unblocked)

**Step 0 -- Pre-upload AI validation (run on local JSON before touching MongoDB):**
```bash
python3 backend/scripts/validate_rules.py \
  --json-file /tmp/destiny_numerology_dry_run.json \
  --batch-id destiny_numerology_ch01-15_v1
```
Review output: Bucket A (truncation artifacts) → PHR. Bucket B (validator framework mismatch) → PHR + validator_error:True. Bucket C (genuine) → flag for TT. See INGEST_PROCESS_BRIEF.md KOP-03/KOP-04 for triage protocol.

**Step 1 -- Pre-ingest dedup:**
```bash
python3 backend/ke_dedup_script.py \
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/" \
  --output-report backend/scripts/dedup_reports/dedup_numerology_vs_bphs.json \
  --threshold 0.82
```
Note: Numerology and Vedic astrology overlap is expected to be LOW -- different systems.

**Dedup report review:** Check THREE sections in the JSON output:
1. `matches` -- lexical similarity duplicates (threshold 0.82)
2. `contradictions` -- same condition, opposite polarity
3. `positional_conflicts_detail` -- same planet×house or planet×sign, different claimed result (NEW 2026-06-02). Two sub-types: `positional_polarity_conflict` (high confidence) and `positional_alternate_result` (same condition, dissimilar result text). Flag all positional conflicts for TT review.

**Step 2 -- Inject on every rule:**

> ⚠️ CRITICAL (KOP-03): Set `pending_review` -- NOT `pending_human_review`. The AI validator (`validate_rules.py`) queries `approval_status: "pending_review"`. If you set `pending_human_review` at upload, the validator silently finds 0 rules and the AI quality check is skipped entirely.

```python
rule["approval_status"]    = "pending_review"          # NOT pending_human_review -- see KOP-03
rule["ingested_at"]        = datetime.now(timezone.utc).isoformat()
rule["ingest_batch_id"]    = "destiny_numerology_ch01-15_v1"
rule["source_book"]        = "Destiny Numerology"
rule["science_id"]         = "numerology"             # Confirm against existing MongoDB numerology rules
rule["source"]["batch_id"] = "destiny_numerology_ch01-15_v1"  # MANDATORY -- validate_rules.py queries this
```

---

## Open Items

| Priority | Count | Action |
|---|---|---|
| 🔴 CRITICAL | 2 | Ch17/Ch19 items -- affect future chapters only, do NOT block Ch01-15 ingest |
| 🟠 HIGH | 10 (+ 12 from Ch15 companion) | NLM/GAI resolution required → BLOCKS ingest |
| 🟡 MED | 13 | Ingest with `pending_review:true` once HIGH cleared |
| 🟢 LOW | 4 | Cosmetic, no action |
| Ch15 TVs | 50 | Must complete all 50 test vectors before ingesting Ch15 rules |

---

## Immediate Next Action

**For this thread:**
1. Send `Book_Wide_OCR_Inconsistencies_Report.docx` to NLM/GAI decode session
2. Request resolution of all 10 HIGH items (direct PDF reference required)
3. Track responses against the report -- do not proceed until all 10 confirmed

**Unblocked sequence after HIGH items resolved:**
1. Run dedup against BPHS Vol 1
2. Ingest Ch01-Ch14 (Ch15 waits for TVs)
3. When all 50 TVs confirmed: ingest Ch15
4. Mark CRITICAL-1 and CRITICAL-2 as future sprint items -- do not block Phase 1 ingest

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
