# Longevity 58Ch -- KE Ingest Run Order
**Batch ID:** `longevity_58ch_v1`  
**Date:** 2026-06-02  
**Total rules:** ~149 (Ch4: 14 · Ch5: 15 · Ch6-19: ~99 · Ch36-58: 21)  
**DB target:** `horoscope_db.interpretation_rules`  
**DO NOT use stale `EverydayHoroscope` DB**

---

## Prerequisites

```bash
# Verify you have MONGO_URL set
echo $MONGO_URL   # should print the Render connection string

# Verify pymongo is installed
python3 -c "import pymongo; print(pymongo.version)"
```

---

## Step 1 -- Dry Run (Extract + Local Validate + Save JSON)

```bash
python3 backend/scripts/ingest_longevity_58ch.py --dry-run \
  --save /tmp/longevity_58ch_rules/longevity_all_rules_DRY_RUN.json
```

**What this does:**
- Parses Ch4/Ch5 NLM markdown files (unescape + fix invalid JSON)
- Extracts Ch6-Ch19 CC decode rules from ```json blocks
- Loads Ch36-58 case study rules from pre-built JSON
- Transforms ALL rules to canonical KE schema
- Runs local structural validation (check Issues: 0)
- Writes consolidated JSON + per-chapter files to `/tmp/longevity_58ch_rules/`

**Expected output:**
```
  Ch04 NLM         14 rules
  Ch05 NLM         15 rules
  Ch06-19 CC       ~99 rules
  Ch36-58 CS       21 rules
  TOTAL           ~149 rules
  Issues: 0
```

**Stop if Issues > 0 -- read the error messages and report to CC.**

---

## Step 2 -- Export Full MongoDB for Dedup

```bash
MONGO_URL="$MONGO_URL" python3 backend/scripts/export_mongo_for_dedup.py
```

**What this does:** Exports ALL ~10,471 rules from `horoscope_db.interpretation_rules` to `/tmp/mongo_existing_rules_dedup/` (one JSON file per source book).

**Expected output:** Multiple files in `/tmp/mongo_existing_rules_dedup/`

> ⚠️  This compares against the COMPLETE MongoDB, not just one book. This is the correct dedup approach per session bookmark.

---

## Step 3 -- Dedup Longevity vs Full MongoDB

```bash
python3 backend/ke_dedup_script.py \
  --folder-a /tmp/longevity_58ch_rules/ \
  --folder-b /tmp/mongo_existing_rules_dedup/ \
  --output-report dedup_longevity_vs_mongodb_all.md \
  --threshold 0.82
```

**What this does:** Compares all Longevity rules against the full MongoDB export using semantic similarity. High-similarity pairs (≥0.82) are reported as potential duplicates.

**Expected high-overlap books:**
- BPHS Vol 1 Ch43/44 (longevity chapters) -- HIGH overlap expected
- Longevity Unnatural Death (44 rules) -- MODERATE
- KP Astrology textbook -- MODERATE (lon-cs-021, lon-cs-015)

**Review the report.** If duplicates found:
- True duplicates → note them, STILL upload (MongoDB dedup is for tracking, not blocking)
- Near-duplicates from different sources → OK to upload (different doctrinal context)

---

## Step 4 -- Upload to MongoDB

> Only run after reviewing dry-run JSON and dedup report.

```bash
python3 backend/scripts/ingest_longevity_58ch.py \
  --upload /tmp/longevity_58ch_rules/longevity_all_rules_DRY_RUN.json \
  --mongo-url "$MONGO_URL"
```

**Expected output:**
```
  Inserted : ~149
  Updated  : 0
  Errors   : 0
  import_batches log updated for batch longevity_58ch_v1
```

---

## Step 5 -- Post-Upload Structural Validation

```bash
python3 backend/scripts/validate_ingest_batch.py \
  --batch-id longevity_58ch_v1 \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db
```

**What this validates:**
- `source.batch_id == "longevity_58ch_v1"` on every rule
- `interpretation.detailed` and `interpretation.summary` non-empty
- `condition` is a non-empty dict
- `scope` is a valid value
- Returns count of flagged rules

---

## Step 6 -- Triage Flagged Rules (Three-Bucket Method)

After validate_ingest_batch.py, any flagged rules fall into three buckets:

| Bucket | Symptom | Action |
|---|---|---|
| **A -- Artifact** | Truncated interpretation text (ends mid-sentence) | Set `approval_status: auto_approved` in a patch script |
| **B -- Validator Error** | PHR flag but rule is actually correct | Set PHR + add `validator_error: true` flag |
| **C -- Genuine** | Rule has a real doctrinal issue | Keep flagged, escalate to TT/GAI |

Write a patch script if needed. Do NOT manually edit MongoDB.

---

## Step 7 -- Git Commit

```bash
git add backend/scripts/ingest_longevity_58ch.py \
        backend/scripts/LONGEVITY_INGEST_RUN_ORDER.md \
        /tmp/longevity_58ch_rules/longevity_all_rules_DRY_RUN.json

git commit -m "feat(ke): Longevity 58Ch full book ingest -- 149 rules, batch longevity_58ch_v1"
```

Also update:
- `Codex_Deliveries/Knowledge_Engine/TRACKER.md` -- add version row
- `TEMPLE_TRACKER.md` -- update Longevity row status
- `KE_TEXTBOOK_DECODE/INGEST_SUMMARY.md` -- mark Longevity as INGESTED
- `Action Items_ Claude Code.md` -- strike off completed items

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `NLM file not found` | Check path: `/Users/apple/Documents/Knowledge Engine_eBooks/` |
| `CC decode file not found` | Check path: `/Users/apple/Documents/Knowledge Engine_eBooks/Longevity_CC_Decode/` |
| `JSON parse error in Ch5 NLM` | Script auto-fixes `maraka_houses:` bug; if still fails, read the error line number and report |
| `Issues: N > 0` | Do NOT upload until Issues: 0. Read error messages. |
| `MongoDB connection failed` | Verify MONGO_URL env var is set correctly |
| `Inserted: 0, Updated: 0` | Check that upload_path JSON is non-empty |

---

*Prepared by CC Thread -- 2026-06-02*  
*ingest_longevity_58ch.py rev 1.0*
