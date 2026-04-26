#!/usr/bin/env python3
"""
Fix flagged and contradiction-downgraded rules in lalkitab-ch27-v1-20260427.

Actions:
1. Force 5 validator-conservatism flags → pending_human_review
   (source-correct rules flagged because validator applied standard Vedic logic
    to Lal Kitab's mental wave system / extreme-outcome prohibition rules)

2. Patch transfer-h07 grammar error in DB (detailed text garbled)

3. Resolve w10/w38 contradiction downgrade → pending_human_review
   (two mental wave units sharing Venus + House 7 are NOT contradictions —
    they map different psychological traits in the same house section)

4. Leave corr-mars-benefic flagged (Objects field genuinely unverified — correct flag)
"""
import os
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "lalkitab-ch27-v1-20260427"
DB_NAME  = "horoscope_db"

# Rules to force from flagged → pending_human_review (validator conservatism)
FORCE_PHR = [
    "lalkitab-ch27-proh-06",    # Jupiter 10th + Moon 4th → jail; extreme outcome is source-verbatim
    "lalkitab-ch27-proh-10",    # Sun 7th/8th + timing restriction; source-verbatim
    "lalkitab-ch27-wave-w01",   # Venus/Saturn dual attribution; LK mental wave system, not standard Vedic
    "lalkitab-ch27-wave-w03",   # Venus House 3 offspring; custom 42-section mapping, not standard houses
    "lalkitab-ch27-wave-w09",   # Venus House 6 progeny; same — custom section mapping
]

# Contradiction pair to resolve → pending_human_review
CONTRADICTION_PAIR = [
    "lalkitab-ch27-wave-w10",   # Venus House 7, Ambition
    "lalkitab-ch27-wave-w38",   # Venus House 7, Object Recognition
]

# Grammar patch for transfer-h07
TRANSFER_H07_ID    = "lalkitab-ch27-transfer-h07"
TRANSFER_H07_FIXED = (
    "House 7 (spouse/partnership/open enemies) — burying the object in the ground neutralises "
    "the conflicting energy of the planet in the partnership house."
)


def main():
    mongo_url = os.environ.get("MONGO_URL", "").strip()
    if not mongo_url:
        mongo_url = input("Paste MongoDB Atlas URL: ").strip()

    coll = MongoClient(mongo_url)[DB_NAME]["interpretation_rules"]
    now  = datetime.now(timezone.utc).isoformat()

    updated = 0

    # ── 1. Force PHR for validator-conservatism flags ──
    for rule_id in FORCE_PHR:
        res = coll.update_one(
            {"rule_id": rule_id, "source.batch_id": BATCH_ID},
            {"$set": {
                "approval_status": "pending_human_review",
                "validation.verdict":      "spot_check",
                "validation.flag_reason":  "forced_phr: validator_conservatism — rule is source-verbatim (Lal Kitab Ch 27); flagged due to standard Vedic logic vs LK mental wave / extreme-outcome prohibition system.",
                "validation.validated_by": "manual_fix_ch27",
                "validation.validated_at": now,
            }}
        )
        if res.modified_count:
            print(f"✅ {rule_id} → pending_human_review (validator conservatism resolved)")
            updated += 1
        else:
            print(f"⚠️  {rule_id} — not found or already updated")

    # ── 2. Grammar patch for transfer-h07 ──
    res = coll.update_one(
        {"rule_id": TRANSFER_H07_ID, "source.batch_id": BATCH_ID},
        {"$set": {
            "interpretation.detailed":    TRANSFER_H07_FIXED,
            "approval_status":            "pending_human_review",
            "validation.verdict":         "spot_check",
            "validation.flag_reason":     "forced_phr: grammar error in detailed text corrected (was: 'burying grounds and neutralises').",
            "validation.validated_by":    "manual_fix_ch27",
            "validation.validated_at":    now,
        }}
    )
    if res.modified_count:
        print(f"✅ {TRANSFER_H07_ID} → pending_human_review (grammar patched)")
        updated += 1
    else:
        print(f"⚠️  {TRANSFER_H07_ID} — not found or already updated")

    # ── 3. Resolve contradiction pair ──
    for rule_id in CONTRADICTION_PAIR:
        res = coll.update_one(
            {"rule_id": rule_id, "source.batch_id": BATCH_ID},
            {"$set": {
                "approval_status":            "pending_human_review",
                "validation.verdict":         "spot_check",
                "validation.flag_reason":     "forced_phr: false contradiction — mental wave engine permits multiple waves per house/planet; w10 (Ambition) and w38 (Object Recognition) are distinct psychological traits, not competing predictions.",
                "validation.validated_by":    "manual_fix_ch27",
                "validation.validated_at":    now,
            }}
        )
        if res.modified_count:
            print(f"✅ {rule_id} → pending_human_review (false contradiction resolved)")
            updated += 1
        else:
            print(f"⚠️  {rule_id} — not found or already updated")

    # ── Summary ──
    print(f"\n{updated}/8 rules updated.")
    print("Note: lalkitab-ch27-corr-mars-benefic left as flagged (Objects field genuinely unverified).")

    # ── Final counts ──
    print("\n=== POST-FIX STATUS ===")
    for status in ["auto_approved", "pending_human_review", "flagged", "pending_review"]:
        n = coll.count_documents({"source.batch_id": BATCH_ID, "approval_status": status})
        if n:
            print(f"  {status:<30} {n}")
    total = coll.count_documents({"source.batch_id": BATCH_ID})
    print(f"  {'Total':<30} {total}")


if __name__ == "__main__":
    main()
