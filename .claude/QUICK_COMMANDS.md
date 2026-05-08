# Quick Commands — Ready-to-Paste Terminal Scripts
**Repo root:** `/Users/apple/DailyHoroscope-Migration`
**Last updated:** 8 May 2026

---

## ① One-Time Setup Per Terminal Session

Paste these first, every time you open a new terminal:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export MONGO_URL="mongodb+srv://..."
export DB_NAME="horoscope_db"
cd /Users/apple/DailyHoroscope-Migration
```

Verify they're set:
```bash
echo "ANTHROPIC: ${ANTHROPIC_API_KEY:0:10}..."
echo "MONGO:     ${MONGO_URL:0:30}..."
echo "DB:        $DB_NAME"
```

---

## ② Upload v2-Novel Rules (13 rules — Gopal Ch2 / Mehta Ch6 / Raphael Ch3)

Run once to upload the 13 novel mundane rules:

```bash
python3 -c "
import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
exec(open('backend/scripts/ingest_mundane_v2_novel_migrate.py').read().replace('DRY_RUN   = True', 'DRY_RUN   = False'))
asyncio.run(run())
"
```

Expected output:
```
INS mundane-gopal-ch2-10th-lord-triage
...
Inserted 13 / Updated 0 rules → horoscope_db.interpretation_rules
```

---

## ③ Validate a Mundane Batch

Replace `BATCH_ID` and `REPORT_NAME` with your values:

```bash
python3 backend/scripts/validate_mundane_rules.py \
  --mongo-url "$MONGO_URL" \
  --db-name "$DB_NAME" \
  --batch-id mundane-interp-v2-novel-20260508 \
  --report-path backend/scripts/reports/mundane_validation_v2_novel.md
```

**Validate ALL pending mundane rules (no batch filter):**
```bash
python3 backend/scripts/validate_mundane_rules.py \
  --mongo-url "$MONGO_URL" \
  --db-name "$DB_NAME" \
  --report-path backend/scripts/reports/mundane_validation_full.md
```

---

## ④ Validate a Lal Kitab / Natal Batch

```bash
python3 backend/scripts/validate_rules.py \
  --mongo-url "$MONGO_URL" \
  --db-name "$DB_NAME" \
  --batch-id lalkitab-chXX-v1-YYYYMMDD \
  --report-path backend/scripts/reports/lalkitab_chXX_validation.md
```

---

## ⑤ Inspect Flagged Rules After Validation

**Mundane batch:**
```bash
python3 -c "
from pymongo import MongoClient
import os
client = MongoClient(os.environ['MONGO_URL'])
col = client['horoscope_db']['interpretation_rules']
flagged = list(col.find(
    {'batch_id': 'mundane-interp-v2-novel-20260508', 'approval_status': 'flagged'},
    {'_id': 0, 'rule_id': 1, 'validation': 1}
))
print(f'Flagged: {len(flagged)}')
for r in flagged:
    print()
    print('RULE:', r['rule_id'])
    print('FLAG:', r.get('validation', {}).get('flag_reason', 'n/a')[:300])
client.close()
"
```

**Change `batch_id` value** to inspect any other batch.

---

## ⑥ Run a Patch Script

```bash
# Inspect first (no changes):
python3 backend/scripts/patch_SCRIPTNAME.py --mongo-url "$MONGO_URL"

# Apply patch:
python3 backend/scripts/patch_SCRIPTNAME.py --mongo-url "$MONGO_URL" --patch
```

**v20 patch (1 false flag — chasing-victory-trigger):**
```bash
# Inspect:
python3 backend/scripts/patch_mundane_v20_flags.py --mongo-url "$MONGO_URL"

# Apply:
python3 backend/scripts/patch_mundane_v20_flags.py --mongo-url "$MONGO_URL" --patch
```

---

## ⑦ Dry Run Any Ingest Script

```bash
python3 backend/scripts/ingest_SCRIPTNAME.py
# DRY_RUN=True is the default in every script — safe to run as-is
```

---

## ⑧ Upload Any Ingest Script Live

```bash
python3 -c "
import asyncio, os
exec(open('backend/scripts/ingest_SCRIPTNAME.py').read().replace('DRY_RUN   = True', 'DRY_RUN   = False'))
asyncio.run(run())
"
```

For scripts that use `main()` instead of `run()`:
```bash
python3 -c "
import asyncio, os
exec(open('backend/scripts/ingest_SCRIPTNAME.py').read().replace('DRY_RUN   = True', 'DRY_RUN   = False'))
asyncio.run(main())
"
```

---

## ⑨ Check MongoDB Counts

```bash
python3 -c "
from pymongo import MongoClient
import os
client = MongoClient(os.environ['MONGO_URL'])
db = client['horoscope_db']
print('interpretation_rules (mundane_jyotish):', db.interpretation_rules.count_documents({'science_id': 'mundane_jyotish'}))
print('interpretation_rules (jyotish/LK):     ', db.interpretation_rules.count_documents({'source.science': 'jyotish'}))
print('mundane_engine_specs:                  ', db.mundane_engine_specs.count_documents({}))
print('mundane_geo_entities:                  ', db.mundane_geo_entities.count_documents({}))
print()
print('--- Mundane approval_status breakdown ---')
for status in ['pending_review','auto_approved','pending_human_review','flagged','approved']:
    n = db.interpretation_rules.count_documents({'science_id':'mundane_jyotish','approval_status':status})
    if n: print(f'  {status}: {n}')
client.close()
"
```

---

## ⑩ Git — Commit After Each Completed Batch

```bash
git add backend/scripts/ingest_SCRIPTNAME.py \
        backend/scripts/patch_SCRIPTNAME.py \
        backend/scripts/reports/REPORTNAME.md \
        backend/scripts/INGEST_NOTES.md

git commit -m "chore(ingest): [source] vN — [topic] (N rules)"
```

---

## Common Batch IDs for Reference

| Script | Batch ID |
|---|---|
| v22 interp (Ch12 India Native) | `mundane-interp-v22-20260508` |
| v22 specs (Ch12 India Native) | `mundane-engine-v22-20260508` |
| v21 interp (Ch11 Rains) | `mundane-interp-v21-20260508` |
| v21 specs (Ch11 Rains) | `mundane-engine-v21-20260508` |
| v20 interp (Ch10 Sports) | `mundane-interp-v20-20260508` |
| v20 specs (Ch10 Sports) | `mundane-engine-v20-20260508` |
| v2-novel migrate | `mundane-interp-v2-novel-20260508` |
| v19 interp | `mundane-interp-v19-20260507` |
| v19 specs | `mundane-engine-v19-20260507` |
| Lal Kitab Ch29 | `lalkitab-ch29-v1-20260505` |
| Lal Kitab Ch28 | `lalkitab-ch28-v1-20260505` |
| Lal Kitab Ch26 | `lalkitab-ch26-v1-20260505` |
