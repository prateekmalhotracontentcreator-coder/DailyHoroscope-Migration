# Thread Brief -- 300 Combinations KE Ingest
## Status · Open Items · Immediate Next Action

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-31
> For: 300 Combinations Ingest Thread
> Status: **✅ COMPLETE -- Ingested + Triage DONE. 141 AA / 188 PHR / 0 flagged. 2026-06-01.**

---

## One-Liner

✅ **COMPLETE.** 329 rules ingested + triage done. 141 auto_approved / 188 PHR / 0 flagged. All 8 OPs closed. Awaiting co-founder sign-off on 141 auto_approved (TT). Next book: 300 Horoscopes.

> This brief is preserved for schema learnings. See `THREAD_BRIEF_300HOROSCOPES_INGEST.md` for the next ingest.

Refer `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_300COMBINATIONS_INGEST.md` for all 300 Combinations KE Ingest.

---

## What This Thread Owns

"300 Important Combinations" by B.V. Raman -- 300 yoga combination rules extracted and fully decoded. This is **Priority 1** in the approved ingest sequence. It has zero open items and zero blockers. Begin ingest immediately.

---

## Canonical Output Folder

```
/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode/
```

Handover summary: `ThreeHundredCombinations_CC_Decode/HANDOVER_SUMMARY.md` -- read this before running ingest.

---

## Rule Count

| Metric | Value |
|---|---|
| Total rules | 300 |
| Active rules | 300 |
| Open items | None |
| OCR issues | None |
| Blockers | None |

---

## Why Priority 1

- Clean decode. No schema edge cases, no OCR ambiguities.
- Different system from BPHS (300 named yogas) -- minimal cross-text dedup complexity.
- Handover document exists and is complete.
- Running this first validates the ingest pipeline before ingesting larger, more complex books.

---

## ⚠️ Phase 2 Schema Learnings -- Apply Before Writing Script

**Learned from BPHS Vol 1 Phase 2 (2026-06-01). These failures cost a full re-upload cycle. Apply from the start.**

**Run schema audit on decode folder before writing the script:**
```bash
python3 << 'EOF'
import json
from pathlib import Path
FOLDER = Path("/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode/")
for f in sorted(FOLDER.glob("*.json"))[:4]:
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

**Ingest script checklist (check off before running --upload):**
- [ ] `source["batch_id"] = BATCH_ID` inside `inject_fields()` -- NOT just `ingest_batch_id` at top level
- [ ] `interpretation.detailed` and `interpretation.summary` non-empty on every rule
- [ ] `condition` is a non-empty dict on every rule
- [ ] Pre-upload local structural check: `Issues: 0`

**Template helpers:** copy `_map_interpretation()` + `_map_condition()` from `backend/scripts/ingest_bphs_vol1_phase2.py` if needed.

**Three-bucket triage for validation results:**
- Bucket A: Artifact (truncation only) → `auto_approved`
- Bucket B: Validator doctrinal error → PHR + `validator_error:true`
- Bucket C: Genuine flag → stay flagged, TT/GAI queue

---

## Ingest Instructions

**Step 1 -- Read the handover document first:**
```
ThreeHundredCombinations_CC_Decode/HANDOVER_SUMMARY.md
```
It contains the exact script invocation and verification steps.

**Step 2 -- Pre-ingest dedup (run even if no BPHS yet ingested -- save report for later):**
```bash
python3 backend/ke_dedup_script.py \
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode/" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/" \
  --output-report dedup_300comb_vs_bphs_vol1.md \
  --threshold 0.82
```

**Step 3 -- Ingest script pattern (from HANDOVER_SUMMARY.md):**
```bash
python3 scripts/ingest_300_combinations.py \
    --mongo-url "$MONGO_URL" \
    --db-name horoscope_db \
    --dry-run
# Review dry-run output → then:
python3 scripts/ingest_300_combinations.py \
    --mongo-url "$MONGO_URL" \
    --db-name horoscope_db \
    --upload
```

**Step 4 -- Verify:**
```bash
python3 scripts/validate_rules.py \
    --mongo-url "$MONGO_URL" --db-name horoscope_db \
    --science-id jyotish_300_combinations
```
Expected: 300 rules, all `approval_status: "pending_human_review"`.

---

## Fields to Inject on Every Rule

```python
rule["approval_status"]    = "pending_human_review"
rule["ingested_at"]        = datetime.now(timezone.utc).isoformat()
rule["ingest_batch_id"]    = "300_combinations_v1"
rule["source_book"]        = "300 Important Combinations"
rule["source"]["batch_id"] = "300_combinations_v1"  # MANDATORY -- validate_rules.py queries this
```

---

## Post-Ingest Dedup Targets

| Target | When to run |
|---|---|
| BPHS Vol 1 | When BPHS Vol 1 is ingested (run retroactively) |
| BPHS Vol 2 | When BPHS Vol 2 is ingested (run retroactively) |
| 300 Horoscopes Vol 1 | When ingested -- moderate overlap expected (both Raman) |

---

## Immediate Next Action

1. Read `ThreeHundredCombinations_CC_Decode/HANDOVER_SUMMARY.md`
2. Run dedup against BPHS Vol 1 local folder (save report)
3. Run `--dry-run` → verify 300 rules parsed correctly
4. Run `--upload` → verify 300 rules in MongoDB
5. Confirm `import_batches` record written

---

---

## Post-Ingest Learnings (2026-06-01) -- Forward These to All Future Ingest Threads

### What this book taught us

#### Dual-schema decode files are real
The 300 Combinations folder had TWO distinct schemas in one batch -- NEW (Y001-040, `full_text`+`condition`) and OLD (Y044-300, `results`+`polarity`+`conditions`). The ingest script must detect both and map each to the canonical KE schema. Always run the schema audit snippet before writing the ingest script.

#### `conditions` dict is valid and must NOT be unwrapped
OLD-schema rules in Y123-Y300 range stored `conditions` as a rich nested dict (not a list). This is legitimate -- the dict IS the condition structure. `isinstance(conds, dict) → store directly as condition`. Do NOT try to convert to a list.

#### `results` as list-of-dicts needs flattening
Some rules stored `results` as `[{"effect": "...", "effect_type": "..."}]` (dicts) instead of `["outcome string"]`. Use `extract_effects()` helper to flatten to plain text before building `interpretation.detailed`.

#### `tba: true` is a research flag, not a permanent state
14 rules had `conditions: None` in the source JSON and were marked `tba: true`. But the conditions were FULLY documented in the corresponding `*_Diagnostic.md` Content Gate sections. The fix: read the Diagnostics, encode the conditions, re-validate. **Always check Diagnostics before surrendering.**

#### Bucket B validator textbook mismatch -- most common false flag
The AI validator is trained on BPHS as "standard classical astrology." For rules from B.V. Raman's books (a DIFFERENT author/system), the validator consistently flags correct conditions as "not in standard texts." This is always Bucket B. No rule should be rejected on this basis alone.

#### Condition encoding errors ARE real (Y271)
One rule (Y271 Bandhana) had a genuine encoding error: I wrote `Saturn in 2nd or 12th` when the source description said `Saturn aspects the 2nd/12th house where Sun+Moon are placed`. The AI validator correctly caught this as logically problematic. Read Diagnostic condition descriptions literally before encoding.

#### Speculative metadata must be stripped before validation (Y294)
One rule (Y294 Matibhramana) had `day_night_modifier: true` and an engine_note about which malefic causes epilepsy vs insanity by day/night. This was my interpolation -- not in Raman's text. The Diagnostic showed MEDIUM-LOW confidence. Strip all speculative overlays before submitting for validation.

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-31*
*Updated: 2026-06-01 -- COMPLETE. Triage done. Post-ingest learnings added.*
*KE Freeze LIFTED ✅ 2026-05-22. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.*
