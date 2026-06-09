#!/usr/bin/env python3
"""
inspect_lk_bucket_c.py
-----------------------
Pull and display the 17 LK Bucket C flagged rules for closing decision.
"""
import os, sys, json
from datetime import datetime, timezone
from pathlib import Path
from pymongo import MongoClient

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    print("ERROR: MONGO_URL not set"); sys.exit(1)

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
ts       = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
log_path = LOG_DIR / f"inspect_lk_bucket_c_{ts}.log"

class Tee:
    def __init__(self, fp: Path):
        self._f = open(fp, "w", encoding="utf-8")
    def write(self, d: str):
        sys.__stdout__.write(d); self._f.write(d)
    def flush(self):
        sys.__stdout__.flush(); self._f.flush()
    def close(self):
        self._f.close()

tee = Tee(log_path)
sys.stdout = tee

print(f"Log saved → {log_path}\n")

mongo = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10_000)
col   = mongo["horoscope_db"]["interpretation_rules"]

BUCKET_C_IDS = [
    "lalkitab-ch20-yog-01",
    "lalkitab-ch20-yog-05",
    "lalkitab-ch20-yog-09",
    "lalkitab-ch20-gp-interact",
    "lalkitab-ch21-gp-05",
    "lalkitab-ch23-geoveto-triangle",
]
# Plus ch24-mortality-* and ch24-age-* -- query by prefix
PREFIX_QUERIES = [
    {"rule_id": {"$regex": "^lalkitab-ch24-mortality"}},
    {"rule_id": {"$regex": "^lalkitab-ch24-age"}},
]

rules = []
# Exact IDs
for rid in BUCKET_C_IDS:
    r = col.find_one({"rule_id": rid})
    if r:
        rules.append(r)
    else:
        print(f"  [WARN] Not found: {rid}")

# Prefix queries
for q in PREFIX_QUERIES:
    for r in col.find(q):
        rules.append(r)

print(f"\n{'='*70}")
print(f"LK BUCKET C -- {len(rules)} rules found")
print(f"{'='*70}\n")

for r in rules:
    rid        = r.get("rule_id", "?")
    status     = r.get("approval_status", "?")
    polarity   = r.get("condition", {}).get("polarity", "?")
    flags      = r.get("validation", {}).get("flag_reasons", [])
    full_text  = r.get("full_text", "") or r.get("interpretation", {}).get("detailed", "")
    summary    = r.get("interpretation", {}).get("summary", "")
    chapter    = r.get("source", {}).get("chapter", "?")
    condition  = r.get("condition", {})
    active     = r.get("active", True)

    print(f"{'─'*70}")
    print(f"ID       : {rid}")
    print(f"Status   : {status}  |  Polarity: {polarity}  |  Active: {active}")
    print(f"Chapter  : {chapter}")
    print(f"Flags    : {flags}")
    print(f"Condition: {json.dumps(condition, indent=None)[:200]}")
    print(f"Summary  : {summary[:200]}")
    print(f"Full text: {full_text[:400]}")
    print()

mongo.close()
print(f"\nTotal: {len(rules)} rules")
sys.stdout = sys.__stdout__
tee.close()
print(f"Log saved → {log_path}")
