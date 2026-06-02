# Knowledge Engine -- Full Ingest & Validation Process Brief
**Version:** 2026-06-02 · **Freeze notice updated:** 2026-06-01
**Purpose:** Step-by-step reference for any new Claude Code session picking up ingest work.
**Read this before writing or running any ingest script.**

> ~~**FREEZE ACTIVE (14 May 2026).**~~ **FREEZE LIFTED ✅ (2026-05-17).** KE-Sprint2 arbitration runtime closed -- all 5 gates passed. Co-founder approval confirmed 2026-05-22. Ingest of new chapters may proceed. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.

---

## The Non-Negotiable Rule

> **NEVER upload rules directly to MongoDB without completing Steps 1-3 first.**
> Dry run → Save JSON → Review → Upload → Validate → Patch → Commit.
> Every step exists for a reason. Skipping any step wastes credits fixing problems downstream.

---

## STEP 0 -- Source Schema Audit (mandatory before writing any ingest script)

**Learned from BPHS Vol 1 Phase 2 (2026-06-01).** The decoded JSON files for a single book can use multiple different schemas. If the ingest script does not map them correctly, the validator will fail every rule on structural checks -- costing a full re-upload cycle.

### Run this audit on every new book before writing the ingest script

```python
python3 << 'EOF'
import json
from pathlib import Path

FOLDER = Path("/Users/apple/Documents/Knowledge Engine_eBooks/[BOOK]_CC_Decode/")

# Sample first rule from each file
for f in sorted(FOLDER.glob("*.json"))[:6]:
    data = json.loads(f.read_text())
    rules = data.get("rules", data) if isinstance(data, dict) else data
    if not isinstance(rules, list) or not rules:
        continue
    r = rules[0]
    interp = r.get("interpretation") or {}
    print(f"\n=== {f.name} ===")
    print(f"  Format: {'dict {rules:[...]}' if isinstance(data, dict) else 'list [...]'}")
    print(f"  Keys: {list(r.keys())}")
    print(f"  interpretation.detailed: {repr((interp.get('detailed') or '')[:60])}")
    print(f"  claim type: {type(r.get('claim')).__name__} | {repr(str(r.get('claim',''))[:60])}")
    print(f"  full_text: {repr(str(r.get('full_text',''))[:60])}")
    print(f"  result: {repr(str(r.get('result',''))[:60])}")
    print(f"  condition present: {isinstance(r.get('condition'), dict)}")
    print(f"  conditions present: {bool(r.get('conditions'))}")
EOF
```

### What to look for

| Field check | If missing/wrong | Fix required in ingest script |
|---|---|---|
| `interpretation.detailed` or `interpretation.summary` | Source uses `claim`, `full_text`, `result`, or `summary` instead | Add `_map_interpretation()` helper -- see BPHS Phase 2 script for all 4 schema patterns |
| `condition` is a dict | Source uses `conditions` (list) | Add `_map_condition()` -- use `conditions[0]` or synthetic `{"type": rule.get("type")}` |
| JSON root is `{"rules": [...]}` | `ke_dedup_script.py` and count scripts assume list format | Use format detection: `data.get("rules", data) if isinstance(data, dict) else data` |
| `source.chapter` missing | Dict-format files often omit it | Inject `source["chapter"] = chapter_num` from loop context |

### Mandatory fields the validator checks (structural_check in knowledge_validator.py)

```python
# All three must pass or the rule is rejected before Claude even sees it:
1. interpretation.detailed or interpretation.summary -- non-empty, ≥ 8 words
2. interpretation.detailed (or summary) -- last char in ".!?\"')"  (no truncation)
3. condition -- non-empty dict
```

### Pre-upload local validation (run against saved JSON, before upload)

```python
python3 << 'EOF'
import json, re
from pathlib import Path

YOGA_SCHEMA_TYPES = frozenset({"yoga_combination", "general_principle", "dosha"})
rules = json.loads(Path("backend/scripts/[name]_rules.json").read_text())

issues = []
for r in rules:
    interp = r.get("interpretation") or {}
    detailed = (interp.get("detailed") or "").strip()
    summary  = (interp.get("summary") or "").strip()
    text = detailed or summary
    cond_type = (r.get("condition") or {}).get("type", "")

    if not text:
        issues.append((r["rule_id"], "empty_interpretation"))
    elif len(text.split()) < (3 if cond_type in ("planet_in_house_in_sign","planet_in_house_special") else 8):
        issues.append((r["rule_id"], "too_short"))
    elif cond_type not in YOGA_SCHEMA_TYPES and text[-1] not in ".!?\"')":
        issues.append((r["rule_id"], f"truncated_text (ends '{text[-1]}')"))
    if not isinstance(r.get("condition"), dict) or not r.get("condition"):
        issues.append((r["rule_id"], "missing_condition"))

print(f"Total rules: {len(rules)} | Issues: {len(issues)}")
for rid, reason in issues[:20]:
    print(f"  {rid}: {reason}")
EOF
```

Expected: `Issues: 0` before uploading. If not zero -- fix the ingest script first.

---

## The Complete 7-Step Workflow

### STEP 1 -- Dry Run (mandatory before every upload)

```bash
python3 backend/scripts/ingest_[name]_v[N].py \
  --dry-run \
  --save backend/scripts/[name]_v[N]_rules.json
```

**What it does:**
- Builds all rule/spec documents in memory (no DB write)
- Prints rule count, breakdown by sub-type, and all rule IDs
- Saves the full JSON to disk so you can inspect it

**What to check:**
- ✅ Rule count matches what you designed (e.g., "Built 22 rules")
- ✅ Breakdown by sub-type looks right
- ✅ All rule IDs are present and correctly named
- ✅ No Python errors

**If anything is wrong:** Fix the script first. Do not proceed to Step 2.

---

### STEP 2 -- Review the JSON (optional but recommended for complex batches)

```bash
# Spot-check a few entries in the saved JSON
python3 -c "
import json
rules = json.load(open('backend/scripts/[name]_v[N]_rules.json'))
print(f'Total: {len(rules)}')
# Print first and last rule to check structure
import pprint
pprint.pprint(rules[0])
print('...')
pprint.pprint(rules[-1])
"
```

**What to check:**
- `rule_id` / `spec_id` follows the naming convention
- `batch_id` is correct and matches this version
- **`source.batch_id` is set** (nested inside the `source` dict) -- `validate_rules.py` line 51 queries `source.batch_id`, NOT top-level `ingest_batch_id`. Both must be set, with the same value. If missing, the validator finds 0 rules. *(Learned from BPHS Phase 2, 2026-06-01)*
- `science_id` is correct (`"mundane_jyotish"` for mundane, `"jyotish"` for natal)
- `approval_status` is `"pending_review"` -- **NOT `pending_human_review`**. The validator (`validate_rules.py`) queries `approval_status: "pending_review"` (line 47). If you upload with `pending_human_review`, the validator finds 0 rules and silently skips the entire batch. *(Learned from Longevity 58Ch ingest, 2026-06-02)*
- `interpretation.detailed` and/or `interpretation.summary` are non-empty strings (not blank or missing)
- `condition` is a non-empty dict (not `None`, not `{}`, not a list)
- Key data fields are populated (not empty dicts or None where data is expected)

---

### STEP 3 -- Upload to MongoDB

```bash
python3 backend/scripts/ingest_[name]_v[N].py \
  --upload backend/scripts/[name]_v[N]_rules.json \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

**Expected output:**
```
Loaded 22 rules from backend/scripts/[name]_v[N]_rules.json
Inserted 22 / Updated 0 rules → horoscope_db.interpretation_rules
```

- `Inserted N` = new documents (first run)
- `Updated N` = existing documents replaced (re-run after a fix)
- Both are safe -- the upsert pattern is idempotent

**If you see `Inserted 0 / Updated 0`:** The rule_ids already exist unchanged. Check if the script is building the correct data.

---

### STEP 4 -- Validate

> ⚠️ **Pre-check before running:**
> ```bash
> echo $ANTHROPIC_API_KEY   # Must print a key starting with sk-ant-
> echo $MONGO_URL            # Must print the connection string
> ```
> If `ANTHROPIC_API_KEY` is empty, the validator will fail silently or crash. Set it first:
> ```bash
> export ANTHROPIC_API_KEY="sk-ant-..."
> ```

```bash
python3 backend/scripts/validate_rules.py \
  --batch-id [your-batch-id-here] \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

> 🚨 **"Found 0 rules to validate" is a RED FLAG** when a batch was just uploaded.
> It almost always means either:
> 1. Rules were uploaded with `approval_status: pending_human_review` instead of `pending_review` -- patch them first:
>    ```bash
>    python3 - <<'EOF'
>    import pymongo, os
>    db = pymongo.MongoClient(os.environ["MONGO_URL"])["horoscope_db"]
>    r = db["interpretation_rules"].update_many(
>        {"source.batch_id": "YOUR-BATCH-ID", "approval_status": "pending_human_review"},
>        {"$set": {"approval_status": "pending_review"}}
>    )
>    print(f"Patched: {r.modified_count}")
>    EOF
>    ```
>    Then re-run the validator.
> 2. `source.batch_id` was not set on the rules -- the `--batch-id` filter finds nothing.
> **Never accept "Found 0 rules" and move on after a fresh upload.** *(Learned from Longevity 58Ch, 2026-06-02)*

**Expected output:**
```
VALIDATION COMPLETE
  auto_approved                  18  (82%)
  pending_human_review            2  (9%)
  flagged                         2  (9%)
  ----------------------------------------
  Total                          22

  Contradictions: 0 pair(s)
```

**Status meanings:**
| Status | Meaning | Action needed |
|---|---|---|
| `auto_approved` | Validator passed -- content is clean | None |
| `pending_human_review` | Validator had minor doubts but didn't flag | Co-founder review queue |
| `flagged` | Validator found a problem | MUST investigate -- see Step 5 |
| Contradictions | Two rules give conflicting outputs | MUST investigate -- see Step 5 |

**For mundane science_id filter:**
```bash
python3 backend/scripts/validate_rules.py \
  --science-id mundane_jyotish \
  --batch-id [your-batch-id] \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

---

### STEP 5 -- Inspect Flagged Rules and Contradictions

**If flagged rules exist -- run this query:**
```python
python3 -c "
from pymongo import MongoClient
import os
client = MongoClient(os.environ['MONGO_URL'])
col = client['horoscope_db']['interpretation_rules']
flagged = list(col.find(
    {'batch_id': 'YOUR-BATCH-ID', 'approval_status': 'flagged'},
    {'_id': 0, 'rule_id': 1, 'title': 1, 'interpretation': 1, 'validation': 1}
))
for r in flagged:
    print('RULE:', r.get('rule_id') or r.get('spec_id'))
    flag = r.get('validation', {}).get('flag_reason', 'n/a')
    print('FLAG:', flag[:200])
    print()
client.close()
"
```

**If contradiction pairs exist -- run this query:**
```python
python3 -c "
from pymongo import MongoClient
import os
client = MongoClient(os.environ['MONGO_URL'])
col = client['horoscope_db']['interpretation_rules']
contradictions = list(col.find(
    {'batch_id': 'YOUR-BATCH-ID',
     'validation.contradiction_ids': {'\$exists': True, '\$ne': []}},
    {'_id': 0, 'rule_id': 1, 'validation.contradiction_ids': 1,
     'validation.contradiction_summary': 1}
))
for r in contradictions:
    print('RULE:', r.get('rule_id'))
    print('CONTRADICTS:', r['validation'].get('contradiction_ids'))
    print('SUMMARY:', r['validation'].get('contradiction_summary', '')[:200])
    print()
client.close()
"
```

---

### STEP 6 -- Write and Run a Patch Script

Once you understand why rules were flagged, write a patch script.

**Five types of flags -- classify before patching:**

| Flag type | Description | Resolution |
|---|---|---|
| **Truncation false flag** | Validator read buffer cut off mid-sentence. Content IS complete in DB. | Patch to `pending_human_review` |
| **Content validity dispute** | Validator applies classical Vedic frame to folk/mundane rules. Rule IS in source. | Patch to `pending_human_review` |
| **Structural false flag** | Validator questions schema patterns already addressed in design. | Patch to `pending_human_review` |
| **Validator doctrinal error** | Validator made a factually wrong doctrinal claim (e.g., "Moon does not own Cancer"; "Chapa not in BPHS Ch25"). Cross-check source PDF before accepting flag. | Patch to `pending_human_review` with note "validator_error: true" |
| **Genuine flag** | Rule has a real problem -- missing data, wrong content, source gap, or Codex fabrication. | Fix the script and re-upload first; or mark flagged with TT/GAI queue note |
| **False contradiction** | Two rules appear to conflict but have mutually exclusive conditions. | Clear contradiction fields with resolution note |
| **System framework mismatch** | Validator applies classical Vedic/BPHS standards to rules from a different doctrinal system (KP, Nadi, Jaimini, etc.). Flags like "not attested in BPHS", "contradicts classical doctrine", "not recognised in Phaladeepika" on KP rules. | Patch to `pending_human_review` + `validator_error: True` + triage_note explaining the system. *(Learned from Longevity 58Ch Ch5/Ch18/Ch19, 2026-06-02)* |

> **Learned from BPHS Phase 2 (2026-06-01):** The validator made doctrinal errors on two rule groups -- (1) flagged Moon-Cancer claiming "Moon does not own Cancer" when Moon IS the lord of Cancer in Vedic astrology; (2) flagged Chapa as "not recognised in BPHS Ch25" when bphs1-ch25-001 explicitly lists Chapa as one of the seven Upagrahas. Always cross-check the source PDF before accepting a validator doctrinal claim. The validator is authoritative on structure and schema; it is NOT authoritative on Vedic astrology doctrine.

**Patch script template:**
```python
#!/usr/bin/env python3
"""
patch_[name]_vN_flags.py
Patches flagged rules in batch [batch-id] to pending_human_review.

[Flagged rules:]
  [rule_id]
    Validator: "[what it said]"
    Resolution: "[why it's a false flag + source confirmation]"
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "your-batch-id-here"

FLAGGED_RULES = {
    "rule-id-1",
    "rule-id-2",
}

REASON = (
    "False flag -- [type]: [explanation of why it's wrong]. "
    "[Source confirmation: where in the source document this is confirmed]. "
    "Promoted to pending_human_review for co-founder source-fidelity confirmation."
)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--patch",     action="store_true")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).isoformat()

    # Inspect
    flagged = list(col.find(
        {"batch_id": BATCH_ID, "approval_status": "flagged"},
        {"_id": 0, "rule_id": 1, "validation.flag_reason": 1},
    ))
    print(f"\nFlagged: {len(flagged)}\n{'─'*60}")
    for r in flagged:
        print(f"  {r['rule_id']}")
        print(f"  Flag: {r.get('validation',{}).get('flag_reason','n/a')[:100]}...")

    if not args.patch:
        print("\n── Inspect-only. Re-run with --patch to apply. ──")
        client.close()
        return

    # Patch
    patched = 0
    for r in flagged:
        rid = r["rule_id"]
        result = col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":         "pending_human_review",
                "validation.verdict":      "spot_check",
                "validation.flag_reason":  REASON,
                "validation.validated_by": "patch_[name]_vN_flags.py",
                "validation.validated_at": now,
            }},
        )
        status = "✅" if result.modified_count else "⚠️  No change"
        print(f"  {status} {rid}")
        if result.modified_count:
            patched += 1

    print(f"\n{patched} / {len(flagged)} patched → pending_human_review")
    client.close()

if __name__ == "__main__":
    main()
```

**Running the patch script -- always inspect first:**
```bash
# Inspect (no changes):
python3 backend/scripts/patch_[name]_vN_flags.py --mongo-url "$MONGO_URL"

# Apply (only after confirming output looks right):
python3 backend/scripts/patch_[name]_vN_flags.py --mongo-url "$MONGO_URL" --patch
```

---

### STEP 7 -- Commit All Files

Only commit after:
- ✅ Dry run passed
- ✅ Upload succeeded
- ✅ Validation run
- ✅ All flagged rules either fixed or patched

```bash
git add backend/scripts/ingest_[name]_vN.py \
        backend/scripts/[name]_vN_rules.json \
        backend/scripts/patch_[name]_vN_flags.py \
        backend/scripts/INGEST_NOTES.md

git commit -m "chore(ingest): [source] vN -- [topic] (N rules)"
```

**Always update `INGEST_NOTES.md` before committing:**
- Add a chapter/version section with: topic, batch_id, rule count, validation result, design notes
- Update the cumulative totals table
- Update the pending chapters list

---

### STEP 7A -- Yoga Chapter Metadata Sync (yoga chapters only)

> **Applies to:** Any ingest batch containing yoga rules (chapters with `condition.yoga_check` objects -- e.g. BPHS Ch35-41, Phaladeepika yoga chapters, 300 Combinations, etc.)

**Background:** The yoga checker sets `condition.yoga_check.checkable` (authoritative). The convenience flag `metadata.yoga_checkable` and the `"yoga_checkable"` tag in `interpretation.tags` must be kept in sync. They can fall out of sync if the yoga checker runs before the metadata backfill, or if rules are re-ingested.

**Run after every yoga chapter ingest and after every patch/re-ingest that touches yoga rules:**

```bash
# Step 7A-1: Dry run -- preview what will be synced
python3 backend/scripts/backfill_metadata_yoga_checkable.py \
  --mongo-url "$MONGO_URL" \
  --dry-run

# Step 7A-2: Apply sync
python3 backend/scripts/backfill_metadata_yoga_checkable.py \
  --mongo-url "$MONGO_URL" \
  --apply
```

**Expected output after apply:**
- `Would patch: 0` on dry run (all in sync)
- `metadata.yoga_checkable` matches `condition.yoga_check.checkable` on every rule
- `interpretation.tags` contains `"yoga_checkable"` on all checkable rules

**Note:** `backfill_metadata_yoga_checkable.py` currently covers Ch35-41 (BPHS Vol 1). When other yoga books are ingested, extend the `CHAPTERS` list in the script or create a book-specific variant.

**Add to commit:**
```bash
git add backend/scripts/backfill_metadata_yoga_checkable.py
```

---

## Naming Conventions

### Batch IDs
```
Lal Kitab natal:   lalkitab-chXX-v1-YYYYMMDD
Mundane specs:     mundane-engine-vN-YYYYMMDD
Mundane rules:     mundane-interp-vN-YYYYMMDD
```

### Rule IDs
```
Lal Kitab:  lalkitab-chXX-[descriptive-slug]
Mundane:    mundane-[source]-chX-[descriptive-slug]
            e.g. mundane-gaur-ch5-ardra-bumper-harvest
```

### Script files
```
ingest_lalkitab_chXX_v1.py
ingest_mundane_engine_specs_vN.py    ← engine specs (mundane_engine_specs collection)
ingest_mundane_interpretation_vN.py  ← interpretation rules (interpretation_rules collection)
patch_[batch]_flags.py
```

---

## Schema Quick Reference

### Lal Kitab / Natal rules (`interpretation_rules`)
```python
{
    "rule_id":         "lalkitab-chXX-[slug]",      # upsert key
    "approval_status": "pending_review",              # validator sets this
    "source": {
        "science":    "jyotish",                     # NEVER "mundane_jyotish"
        "book":       "Lal Kitab",
        "chapter":    28,
        "logic_unit": "LU_28.slug",                  # descriptive, not sequential
        "batch_id":   "lalkitab-ch28-v1-20260505",
    },
    "metadata":        {"rule_type": "...", "sub_type": "..."},
    "interpretation":  {
        "summary": "ch28-rule-slug",                 # NEVER prose -- prevents truncation flags
        "detailed": "Full explanation...",
        "remedies": [],
    },
    "validation":      {"checkable": False, "yoga_check": None,
                        "validated_by": None, "validated_at": None},
    "created_at": now, "updated_at": now,
}
```

### Mundane engine specs (`mundane_engine_specs`)
```python
{
    "spec_id":    "gaur-ch5-ardra-monsoon-engine",   # upsert key
    "spec_type":  "multi_factor_lookup",
    "science_id": "mundane_jyotish",                 # NEVER "jyotish"
    "batch_id":   "mundane-engine-vN-YYYYMMDD",
    "title":      "...",
    "source":     "gaur_aifas_chN",
    "description": "...",
    "created_at": "<ISO timestamp>",
    # ... chapter-specific lookup tables, matrices, etc.
}
```

### Mundane interpretation rules (`interpretation_rules`)
```python
{
    "rule_id":          "mundane-gaur-ch5-ardra-bumper-harvest",  # upsert key
    "batch_id":         "mundane-interp-vN-YYYYMMDD",
    "science_id":       "mundane_jyotish",
    "sub_type":         "monsoon_forecast",
    "title":            "...",
    "source_chapter":   "Gaur Ch 5 -- ...",
    "condition":        "IF (...) AND (...)",
    "result":           "...",
    "synthesis_sources": ["spec-id-1", "spec-id-2"],
    "checkable":        True,
    "approval_status":  "pending_review",
    "severity":         "critical",           # low / medium / high / critical
    "created_at":       "<ISO timestamp>",
}
```

---

## Common False Flag Patterns (do NOT re-validate, just patch)

| Pattern | How to recognise | Resolution |
|---|---|---|
| **Truncation artifact** | Flag says "truncated mid-sentence ('...text cu')" but you can see full text in script | `pending_human_review` -- buffer artifact |
| **Classical vs folk frame** | Validator says "not standard Vedic principle" for Lal Kitab / mundane rules | `pending_human_review` -- different tradition |
| **Structural objection** | Validator questions AND/OR gates, two-house conditions already designed intentionally | `pending_human_review` -- schema is correct |
| **Non-classical practice** | Validator disputes folk astronomy, physiognomy, farmer's almanac rules | `pending_human_review` -- source-confirmed |
| **False contradiction** | Two rules appear opposite but have mutually exclusive triggers/conditions | Clear contradiction fields with resolution note |

**Genuine flags (fix the script, don't just patch):**
- Missing source data (field is empty when it should have content)
- Wrong chapter -- rule content doesn't match the chapter it's in
- Duplicate rule_id -- two rules with the same ID
- Calculation error in a formula or lookup table

---

## Environment Setup

```bash
# Required for all MongoDB operations -- set before running any script
export MONGO_URL="mongodb+srv://..."

# Verify it's set
echo $MONGO_URL   # Should print the full connection string, not empty
```

---

## Current State (as of 7 May 2026)

| Collection | Documents |
|---|---|
| `interpretation_rules` (jyotish -- Lal Kitab) | **467 rules** across Ch 19-29 |
| `interpretation_rules` (mundane_jyotish) | **290 rules** across v1-v19 |
| `mundane_engine_specs` | **96 specs** across v1-v19 |
| `mundane_geo_entities` | **29 entities** |

**For full chapter-by-chapter breakdown:** read `backend/scripts/INGEST_NOTES.md`

---

## Quick Checklist Before Every Session

- [ ] `MONGO_URL` is exported in terminal (`echo $MONGO_URL` not empty)
- [ ] `ANTHROPIC_API_KEY` is exported in terminal (`echo $ANTHROPIC_API_KEY` not empty) -- required for Step 4 validator
- [ ] Read `CLAUDE.md` for project context
- [ ] Read `INGEST_NOTES.md` for current ingest state
- [ ] Know the batch_id you're working with
- [ ] Ingest script sets `approval_status: "pending_review"` (not `pending_human_review`)
- [ ] Dry run before every upload
- [ ] Validate after every upload
- [ ] **If validator says "Found 0 rules" after a fresh upload -- STOP and investigate** (see Step 4 red flag note)
- [ ] Inspect every flagged rule before patching
- [ ] Update `INGEST_NOTES.md` before committing
- [ ] **For yoga chapters:** Run Step 7A (`backfill_metadata_yoga_checkable.py`) after every ingest
- [ ] Commit after every completed batch

---

---

## Dedup Strategy -- Strategy A (Rolling Pre-Ingest Dedup)

**Decision confirmed 2026-06-01.**

Every book is deduped against ALL previously-ingested books before its own ingest. Never ingest first and dedup later.

### Rule
> Before ingesting Book B, run `ke_dedup_script.py` comparing Book B source JSONs against the source JSONs of every book already in MongoDB. Review flagged pairs. Consult GAI/NLM on genuine duplicates. Then ingest.

### Practical execution

`ke_dedup_script.py` requires two **separate folders**. When the new and existing source files share the same decode folder, use `prep_[book]_dedup_folders.py` to separate them into temp dirs first.

```bash
# Step 0 -- Separate source files into temp folders (when needed)
python3 backend/scripts/prep_[book]_phase[N]_dedup_folders.py

# Step 1 -- Run dedup (dry-run first)
python3 backend/ke_dedup_script.py \
  --folder-a /tmp/[new_book_rules]/ \
  --folder-b /tmp/[existing_book_rules]/ \
  --threshold 0.82 \
  --output-report backend/scripts/dedup_reports/dedup_[book_a]_vs_[book_b].json \
  --dry-run

# Step 2 -- Apply (writes cross_text_matches back to source JSONs)
python3 backend/ke_dedup_script.py \
  --folder-a /tmp/[new_book_rules]/ \
  --folder-b /tmp/[existing_book_rules]/ \
  --threshold 0.82 \
  --output-report backend/scripts/dedup_reports/dedup_[book_a]_vs_[book_b].json \
  --update-files

# Step 3 -- Review report, consult GAI/NLM on flagged pairs
# Step 4 -- Mark suppressed duplicates in source JSON (duplicate_candidate: true)
# Step 5 -- Then proceed to ingest (Step 1 of 7-step workflow)
```

### Dedup priority matrix

| New book (to ingest) | Dedup against | Expected overlap | Priority |
|---|---|---|---|
| BPHS Vol 1 Phase 2 | BPHS Vol 1 Phase 1 | Low-moderate (same book, different chapters) | Run |
| BPHS Vol 1 Phase 2 | BPHS Vol 2 | Low (doctrinally separate chapters) | Run |
| Phaladeepika | BPHS Vol 1 (all phases) | **HIGH -- direct commentary** | Critical |
| 300 Combinations | BPHS Vol 1 (all phases) | Moderate | Run |
| 300 Horoscopes | BPHS Vol 1 + 300 Combinations | Low-moderate | Run |
| KP Astrology | BPHS Vol 1 | Low (system differences) | Run -- expect few hits |
| SBC | BPHS Vol 1 | Low (transit/electional vs natal) | Run |
| Longevity 58 Ch | BPHS Vol 1 Ch43/44 + Longevity Unnatural | Moderate | Run |
| Medical Astrology | BPHS Vol 1 | Low | Run |
| Destiny Numerology | None (separate system) | Near-zero | Skip |

### Important: BPHS rule schema and dedup accuracy

`ke_dedup_script.py` compares on: `condition.type + condition.planet + condition.house + condition.sign + full_text` (top-level).

BPHS rules use `interpretation.detailed` (not `full_text`). Comparison runs on **condition fields only**. This means:
- ✅ House-lord rules (planet + house populated) -- dedup works well
- ✅ Exaltation/aspect/shadbala rules -- dedup works well
- ⚠️ Complex yoga rules (condition stored in `condition.notes`) -- dedup is thinner, catches structural overlaps only

For books that DO use `full_text` (LK, Mundane), dedup is more thorough. This is a known limitation -- KOP-02 in the Known Open Points table.

---

## Known Open Points (Process-Level)

| # | Issue | Applies to | Status | Action |
|---|---|---|---|---|
| KOP-01 | `metadata.yoga_checkable` and `interpretation.tags["yoga_checkable"]` can fall out of sync with `condition.yoga_check.checkable` after ingest or re-ingest | All yoga chapter batches (BPHS Ch35-41, 300 Combinations yoga rules, Phaladeepika yoga chapters, etc.) | 🟠 Confirmed on BPHS Vol 1 Ch35-41 (2026-06-01). Fixed via Step 7A. | Run `backfill_metadata_yoga_checkable.py` after every yoga chapter ingest. Step 7A added to workflow. When new yoga books are ingested, extend or clone the backfill script for that book. |
| KOP-02 | Schema Quick Reference in this doc shows `"validation": {"yoga_check": None}` -- this is the Lal Kitab / Mundane schema. BPHS yoga rules use `condition.yoga_check` (rich object) and `metadata.yoga_checkable` (boolean). Two different schema patterns coexist. | BPHS yoga chapters vs LK/Mundane rules | 🟡 By design -- different source books use different schemas. | Do not cross-apply. When inspecting yoga_check, always check `condition.yoga_check` for BPHS yoga rules. Use `validation.yoga_check` schema only for LK/Mundane rules. |
| KOP-03 | `validate_rules.py` filters on `approval_status: "pending_review"`. If an ingest script uploads rules as `pending_human_review`, the validator finds 0 rules and silently skips the batch -- the Anthropic API quality check never runs. | All ingest scripts | 🔴 Root cause confirmed Longevity 58Ch (2026-06-02). **Fixed in process docs: ingest scripts must set `pending_review`.** Patch command added to Step 4 for recovery if wrong status was set. | All future ingest scripts: set `approval_status: "pending_review"` at upload time. The validator promotes passing rules to `auto_approved` and sets `pending_human_review` on borderline ones -- do not pre-empt this by setting PHR at ingest. |
| KOP-04 | The Anthropic API doctrinal validator applies classical Vedic/BPHS doctrine as its reference frame. Rules from other doctrinal systems (KP, Jaimini, Nadi) will generate false flags like "not attested in BPHS" or "contradicts classical doctrine". This is a validator framework limitation, not a rule defect. | KP Astrology, Jaimini, Nadi, any non-BPHS science_id | 🟡 Confirmed on Longevity 58Ch Ch5/Ch18/Ch19 KP rules (2026-06-02) -- 11 Bucket B false flags. | Classify as Bucket B (validator framework error). Patch to `pending_human_review` + `validator_error: True` with triage_note explaining the system mismatch. Do not escalate to TT/GAI. |
