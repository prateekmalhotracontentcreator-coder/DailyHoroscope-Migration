"""
patch_longevity_triage.py
Triage patch for batch longevity_58ch_v1 -- 29 flagged rules.

Bucket A (18): Truncation artifacts -- detailed text cut off mid-sentence.
  Action: approval_status -> pending_human_review + truncation_artifact: True

Bucket B (11): Validator framework error -- validator applied BPHS/classical
  standards to KP methodology rules (KP sublord chain / Placidus / DBA
  signification are a legitimate independent system, not BPHS deviations).
  Action: approval_status -> pending_human_review + validator_error: True

Contradiction pair lon-cs-005/006: Complementary Aparimita conditions,
  not a genuine contradiction. Cross-reference added to both.

Bucket C: 0 genuine issues.

Run:
  python3 backend/scripts/patch_longevity_triage.py --mongo-url "$MONGO_URL"
"""

from __future__ import annotations
import argparse
import os
from datetime import datetime, timezone
from pymongo import MongoClient

# ---------------------------------------------------------------------------
BUCKET_A = [
    "kp-ch10-009", "kp-ch11-002", "kp-ch11-003", "kp-ch11-006",
    "kp-ch12-007", "kp-ch14-002", "kp-ch14-004", "kp-ch15-004",
    "kp-ch15-007", "kp-ch15-009", "kp-ch16-004", "kp-ch16-006",
    "kp-ch16-009", "kp-ch18-009", "kp-ch18-011",
    "lon-cs-013",  "lon-cs-014",  "lon-cs-015",
]

BUCKET_B = [
    "kp-ch05-007", "kp-ch05-008", "kp-ch05-009", "kp-ch05-010",
    "kp-ch05-012", "kp-ch05-013", "kp-ch05-015",
    "kp-ch18-007", "kp-ch18-008", "kp-ch18-010", "kp-ch19-001",
]

# Contradiction pair: lon-cs-005 <-> lon-cs-006
# Both treated as Bucket B; complementary Aparimita conditions.
CONTRA_PAIR = ["lon-cs-005", "lon-cs-006"]
CONTRA_NOTE = (
    "lon-cs-005 and lon-cs-006 are complementary Aparimita Aayu conditions: "
    "005 specifies isolation requirement, 006 specifies punya override. "
    "Not a doctrinal contradiction. Validator framework error."
)
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Triage patch for longevity_58ch_v1")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL"), required=False)
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing")
    args = parser.parse_args()

    if not args.mongo_url:
        raise SystemExit("ERROR: --mongo-url required or set MONGO_URL env var")

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]
    col = db["interpretation_rules"]
    now = datetime.now(timezone.utc).isoformat()

    a_ok = b_ok = c_ok = 0

    # --- Bucket A -----------------------------------------------------------
    print(f"\nBucket A -- truncation artifacts ({len(BUCKET_A)} rules)")
    for rid in BUCKET_A:
        doc = col.find_one({"rule_id": rid}, {"approval_status": 1, "_id": 0})
        if not doc:
            print(f"  [WARN] {rid} not found in DB")
            continue
        if args.dry_run:
            print(f"  [DRY]  {rid} -> pending_human_review + truncation_artifact:True")
        else:
            col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status": "pending_human_review",
                    "truncation_artifact": True,
                    "triage_note": "Bucket A: detailed text truncated mid-sentence in source decode. Doctrinal content sound.",
                    "triaged_at": now,
                }},
            )
            print(f"  [OK]   {rid} -> pending_human_review + truncation_artifact:True")
            a_ok += 1

    # --- Bucket B -----------------------------------------------------------
    print(f"\nBucket B -- validator framework error ({len(BUCKET_B)} rules)")
    for rid in BUCKET_B:
        doc = col.find_one({"rule_id": rid}, {"approval_status": 1, "_id": 0})
        if not doc:
            print(f"  [WARN] {rid} not found in DB")
            continue
        if args.dry_run:
            print(f"  [DRY]  {rid} -> pending_human_review + validator_error:True")
        else:
            col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status": "pending_human_review",
                    "validator_error": True,
                    "triage_note": (
                        "Bucket B: validator applied classical BPHS standards to KP methodology. "
                        "KP sublord chain, Placidus house division, and DBA signification are a "
                        "legitimate independent system. Flag is a framework mismatch, not a "
                        "doctrinal error in context."
                    ),
                    "triaged_at": now,
                }},
            )
            print(f"  [OK]   {rid} -> pending_human_review + validator_error:True")
            b_ok += 1

    # --- Contradiction pair: lon-cs-005 / lon-cs-006 ------------------------
    print(f"\nContradiction pair -- Bucket B cross-reference")
    for rid in CONTRA_PAIR:
        other = [r for r in CONTRA_PAIR if r != rid][0]
        doc = col.find_one({"rule_id": rid}, {"approval_status": 1, "_id": 0})
        if not doc:
            print(f"  [WARN] {rid} not found in DB")
            continue
        if args.dry_run:
            print(f"  [DRY]  {rid} -> pending_human_review + validator_error:True + cross_reference:{other}")
        else:
            col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status": "pending_human_review",
                    "validator_error": True,
                    "cross_reference": other,
                    "triage_note": CONTRA_NOTE,
                    "triaged_at": now,
                }},
            )
            print(f"  [OK]   {rid} -> pending_human_review + validator_error:True + cross_reference:{other}")
            c_ok += 1

    # --- Summary ------------------------------------------------------------
    if args.dry_run:
        print(f"\n[DRY RUN] No changes written.")
        print(f"  Would patch: {len(BUCKET_A)} Bucket A + {len(BUCKET_B)} Bucket B + {len(CONTRA_PAIR)} contra-pair rules")
    else:
        print(f"\nTriage complete:")
        print(f"  Bucket A patched : {a_ok} / {len(BUCKET_A)}")
        print(f"  Bucket B patched : {b_ok} / {len(BUCKET_B)}")
        print(f"  Contra pair      : {c_ok} / {len(CONTRA_PAIR)}")
        print(f"  Bucket C         : 0 (no genuine issues)")

        # Verify final state
        counts = {}
        for status in ["auto_approved", "pending_human_review", "flagged", "pending_review"]:
            counts[status] = col.count_documents({
                "source.batch_id": "longevity_58ch_v1",
                "approval_status": status,
            })
        print(f"\nFinal DB state for batch longevity_58ch_v1:")
        for k, v in counts.items():
            if v:
                print(f"  {k:30s}: {v}")
        print(f"  {'TOTAL':30s}: {sum(counts.values())}")

    client.close()


if __name__ == "__main__":
    main()
