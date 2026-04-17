#!/usr/bin/env python3
"""
Reset rules in specified batches from 'rejected' back to 'pending_review'
so they can be re-validated after a patch.
"""
import sys
from pymongo import MongoClient

MONGO_URL = sys.argv[1] if len(sys.argv) > 1 else input("MONGO_URL: ")
DB_NAME   = sys.argv[2] if len(sys.argv) > 2 else "EverydayHoroscope"

col = MongoClient(MONGO_URL)[DB_NAME]["interpretation_rules"]

batches = [f"bphs-ch{c}-v2-20260414" for c in [12, 13, 14, 15, 17]]
batches += [f"bphs-ch{c}-v2-20260415" for c in [12, 13, 14, 15, 17]]

r = col.update_many(
    {"source.batch_id": {"$in": batches}, "approval_status": "rejected"},
    {"$set": {"approval_status": "pending_review"}}
)
print(f"Reset {r.modified_count} rules to pending_review")
