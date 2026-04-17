#!/usr/bin/env python3
"""
One-time patch: add terminal period to v2 rule text fields that lack punctuation.
Run BEFORE validating any v2 batch for the first time.
"""
import sys
from pymongo import MongoClient

MONGO_URL = sys.argv[1] if len(sys.argv) > 1 else input("MONGO_URL: ")
DB_NAME   = sys.argv[2] if len(sys.argv) > 2 else "EverydayHoroscope"

TERMINAL = set('.!?"\'')

col = MongoClient(MONGO_URL)[DB_NAME]["interpretation_rules"]

# All v2 batches — extend this list as new chapters are ingested
batches = [f"bphs-ch{c}-v2-20260414" for c in [12, 13, 14, 15, 17]]
# Also cover 20260415 in case the ingest ran on a different UTC date
batches += [f"bphs-ch{c}-v2-20260415" for c in [12, 13, 14, 15, 17]]

fixed = 0
for rule in col.find({"source.batch_id": {"$in": batches}}, {"_id": 1, "interpretation": 1}):
    interp  = rule.get("interpretation", {})
    updates = {}
    for field in ["detailed", "summary"]:
        val = (interp.get(field) or "").strip()
        if val and val[-1] not in TERMINAL:
            updates[f"interpretation.{field}"] = val + "."
    if updates:
        col.update_one({"_id": rule["_id"]}, {"$set": updates})
        fixed += 1

print(f"Fixed {fixed} rules across {len([b for b in batches if '20260414' in b])} batches")
