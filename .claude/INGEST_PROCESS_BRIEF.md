# Knowledge Engine — Full Ingest & Validation Process Brief
**Version:** 7 May 2026
**Purpose:** Step-by-step reference for any new Claude Code session picking up ingest work.
**Read this before writing or running any ingest script.**

---

## The Non-Negotiable Rule

> **NEVER upload rules directly to MongoDB without completing Steps 1–3 first.**
> Dry run → Save JSON → Review → Upload → Validate → Patch → Commit.
> Every step exists for a reason. Skipping any step wastes credits fixing problems downstream.

---

## The Complete 7-Step Workflow

### STEP 1 — Dry Run (mandatory before every upload)

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

### STEP 2 — Review the JSON (optional but recommended for complex batches)

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
- `science_id` is correct (`"mundane_jyotish"` for mundane, `"jyotish"` for natal)
- `approval_status` is `"pending_review"` (the validator will update this)
- Key data fields are populated (not empty dicts or None where data is expected)

---

### STEP 3 — Upload to MongoDB

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
- Both are safe — the upsert pattern is idempotent

**If you see `Inserted 0 / Updated 0`:** The rule_ids already exist unchanged. Check if the script is building the correct data.

---

### STEP 4 — Validate

```bash
python3 backend/scripts/validate_rules.py \
  --batch-id [your-batch-id-here] \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

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
| `auto_approved` | Validator passed — content is clean | None |
| `pending_human_review` | Validator had minor doubts but didn't flag | Co-founder review queue |
| `flagged` | Validator found a problem | MUST investigate — see Step 5 |
| Contradictions | Two rules give conflicting outputs | MUST investigate — see Step 5 |

**For mundane science_id filter:**
```bash
python3 backend/scripts/validate_rules.py \
  --science-id mundane_jyotish \
  --batch-id [your-batch-id] \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

---

### STEP 5 — Inspect Flagged Rules and Contradictions

**If flagged rules exist — run this query:**
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

**If contradiction pairs exist — run this query:**
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

### STEP 6 — Write and Run a Patch Script

Once you understand why rules were flagged, write a patch script.

**Three types of flags — classify before patching:**

| Flag type | Description | Resolution |
|---|---|---|
| **Truncation false flag** | Validator read buffer cut off mid-sentence. Content IS complete in DB. | Patch to `pending_human_review` |
| **Content validity dispute** | Validator applies classical Vedic frame to folk/mundane rules. Rule IS in source. | Patch to `pending_human_review` |
| **Structural false flag** | Validator questions schema patterns already addressed in design. | Patch to `pending_human_review` |
| **Genuine flag** | Rule has a real problem — missing data, wrong content, source gap. | Fix the script and re-upload first |
| **False contradiction** | Two rules appear to conflict but have mutually exclusive conditions. | Clear contradiction fields with resolution note |

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
    "False flag — [type]: [explanation of why it's wrong]. "
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

**Running the patch script — always inspect first:**
```bash
# Inspect (no changes):
python3 backend/scripts/patch_[name]_vN_flags.py --mongo-url "$MONGO_URL"

# Apply (only after confirming output looks right):
python3 backend/scripts/patch_[name]_vN_flags.py --mongo-url "$MONGO_URL" --patch
```

---

### STEP 7 — Commit All Files

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

git commit -m "chore(ingest): [source] vN — [topic] (N rules)"
```

**Always update `INGEST_NOTES.md` before committing:**
- Add a chapter/version section with: topic, batch_id, rule count, validation result, design notes
- Update the cumulative totals table
- Update the pending chapters list

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
        "summary": "ch28-rule-slug",                 # NEVER prose — prevents truncation flags
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
    "source_chapter":   "Gaur Ch 5 — ...",
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
| **Truncation artifact** | Flag says "truncated mid-sentence ('...text cu')" but you can see full text in script | `pending_human_review` — buffer artifact |
| **Classical vs folk frame** | Validator says "not standard Vedic principle" for Lal Kitab / mundane rules | `pending_human_review` — different tradition |
| **Structural objection** | Validator questions AND/OR gates, two-house conditions already designed intentionally | `pending_human_review` — schema is correct |
| **Non-classical practice** | Validator disputes folk astronomy, physiognomy, farmer's almanac rules | `pending_human_review` — source-confirmed |
| **False contradiction** | Two rules appear opposite but have mutually exclusive triggers/conditions | Clear contradiction fields with resolution note |

**Genuine flags (fix the script, don't just patch):**
- Missing source data (field is empty when it should have content)
- Wrong chapter — rule content doesn't match the chapter it's in
- Duplicate rule_id — two rules with the same ID
- Calculation error in a formula or lookup table

---

## Environment Setup

```bash
# Required for all MongoDB operations — set before running any script
export MONGO_URL="mongodb+srv://..."

# Verify it's set
echo $MONGO_URL   # Should print the full connection string, not empty
```

---

## Current State (as of 7 May 2026)

| Collection | Documents |
|---|---|
| `interpretation_rules` (jyotish — Lal Kitab) | **467 rules** across Ch 19–29 |
| `interpretation_rules` (mundane_jyotish) | **290 rules** across v1–v19 |
| `mundane_engine_specs` | **96 specs** across v1–v19 |
| `mundane_geo_entities` | **29 entities** |

**For full chapter-by-chapter breakdown:** read `backend/scripts/INGEST_NOTES.md`

---

## Quick Checklist Before Every Session

- [ ] `MONGO_URL` is exported in terminal (`echo $MONGO_URL` not empty)
- [ ] Read `CLAUDE.md` for project context
- [ ] Read `INGEST_NOTES.md` for current ingest state
- [ ] Know the batch_id you're working with
- [ ] Dry run before every upload
- [ ] Validate after every upload
- [ ] Inspect every flagged rule before patching
- [ ] Update `INGEST_NOTES.md` before committing
- [ ] Commit after every completed batch
