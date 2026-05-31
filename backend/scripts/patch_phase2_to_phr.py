#!/usr/bin/env python3
"""
patch_phase2_to_phr.py
------------------------------------------------------------------------
Phase 2 validation triage -- 33 rules → pending_human_review

Covers two sub-groups:

  BUCKET B (4 rules) -- Validator doctrinal errors
    • bphs1-ch03-045 : Claude says "Moon does not own Cancer; Moon owns only
      Taurus." INCORRECT. Moon owns Cancer in classical Vedic astrology.
    • bphs1-ch25-052/053/054 : Claude says "Chapa not recognised in BPHS Ch25."
      INCORRECT. Ch25 rule-001 explicitly lists Chapa (Indra Dhanus/Koda)
      as one of the seven Upagrahas.

  DATA QUALITY (29 rules) -- Truncated text (summary and/or detailed)
    These rules have incomplete text in the source decode but no doctrinal
    error. TT to reconstruct from source sloka or mark as reconstruction-needed.

Run:
  python3 backend/scripts/patch_phase2_to_phr.py \
    --mongo-url "$MONGO_URL" --db-name horoscope_db          # dry run
  python3 backend/scripts/patch_phase2_to_phr.py \
    --mongo-url "$MONGO_URL" --db-name horoscope_db --apply  # apply
"""

import argparse, os, sys
from datetime import datetime, timezone

# ── Bucket B: validator doctrinal errors ─────────────────────────────────
BUCKET_B = {
    "bphs1-ch03-045": (
        "Validator error: Claude incorrectly stated Moon does not own Cancer. "
        "Moon owns Cancer in classical Vedic astrology. "
        "Rule content may be correct -- TT to verify doctrine."
    ),
    "bphs1-ch25-052": (
        "Validator error: Claude said Chapa is not in BPHS Ch25. "
        "bphs1-ch25-001 explicitly lists Chapa (Indra Dhanus/Koda) as a Ch25 Upagraha. "
        "TT to verify house-wise results are accurate."
    ),
    "bphs1-ch25-053": (
        "Validator error: Claude said Chapa is not in BPHS Ch25. "
        "Chapa IS a listed Ch25 Upagraha. TT to verify house-wise results."
    ),
    "bphs1-ch25-054": (
        "Validator error: Claude said Chapa is not in BPHS Ch25. "
        "Chapa IS a listed Ch25 Upagraha. Note also: 'wicked / very honourable' "
        "internal tension -- TT to verify which descriptor applies."
    ),
}

# ── Data quality: truncated text (summary and/or detailed) ───────────────
DATA_QUALITY = {
    # summary_truncated_detailed_suspect -- Claude couldn't fully evaluate
    "bphs1-ch03-021": "Summary truncated ('also ro'); detailed suspect. TT to verify varna assignments from source sloka.",
    "bphs1-ch03-035": "Summary truncated ('Moon and'); detailed text possibly incomplete. TT to verify from source.",
    "bphs1-ch06-024": "Summary truncated ('fulfillin'); detailed appears complete. TT to verify.",
    "bphs1-ch08-001": "Summary garbled ('Leo, Libra. Wait -- movab'); Capricorn example malformed. TT to reconstruct from source.",
    "bphs1-ch09-010": "Summary truncated (exception clause cut off). Detailed complete but Claude couldn't evaluate full rule. TT to verify.",
    "bphs1-ch03-065": "Summary truncated mid-sentence. TT to reconstruct from source sloka.",  # truncated_needs_reconstruction
    "bphs1-ch10-004": "Summary truncated mid-sentence (Capricorn ascendant exception). TT to reconstruct exception clause.",
    "bphs1-ch10-006": "Summary truncated mid-sentence (malefic aspect rule). TT to reconstruct from source.",
    "bphs1-ch25-001": "Summary and detailed both incomplete (Kala/Gulika classification unresolved). TT to reconstruct from Ch25 sloka.",
    "bphs1-ch25-002": "Summary and detailed both incomplete (classification unclear). TT to reconstruct from source.",
    # detailed_truncated
    "bphs1-ch25-005": "Detailed truncated ('must be balanced against t'). Cannot evaluate. TT to reconstruct.",
    "bphs1-ch26-016": "Detailed severely truncated (ends '('). Incoherent. TT to reconstruct from Ch26 sloka.",
    "bphs1-ch28-007": "Summary truncated ('Reduce Ishta P') and detailed garbled. Both incomplete. TT to reconstruct.",
    "bphs1-ch28-008": "Summary truncated mid-word; detailed incomplete ('respec'). Both truncated. TT to reconstruct.",
    "bphs1-ch29-002": "Detailed truncated ('(8) Marana Pada -- Arudha'). Full list of 12 Padas incomplete. TT to reconstruct.",
    "bphs1-ch30-002": "Detailed cuts off mid-example ('Scorpio (odd) → Libra → Venus in Canc'). TT to complete from source.",
    "bphs1-ch31-025": "Detailed truncated ('If Papargala i'). Argala exception clause incomplete. TT to reconstruct.",
    "bphs1-ch32-026": "Summary truncated ('behal'); detailed also truncated ('pronounce'). Both corrupt. TT to reconstruct.",
    "bphs1-ch32-027": "Summary truncated ('i'); rule logic stated as correct by Claude but text unreadable. TT to reconstruct.",
    "bphs1-ch32-048": "Summary and detailed both truncated. Cannot evaluate. TT to reconstruct from source.",
    "bphs1-ch33-032": "Detailed truncated ('treating venomous and toxic condi'). TT to complete from Ch33 sloka.",
    "bphs1-ch33-033": "Detailed truncated ('involving the native's own dwelling'). TT to complete.",
    "bphs1-ch33-037": "Detailed truncated ('participati'). TT to complete. Note: 'become a thief' outcome -- TT to verify.",
    "bphs1-ch33-058": "Detailed truncated ('The Sun here confers solar f'). TT to reconstruct.",
    "bphs1-ch33-059": "Detailed truncated ('The conjugal intimacy'). TT to reconstruct.",
    "bphs1-ch33-061": "Detailed truncated ('through damp-cold ph'). TT to reconstruct.",
    "bphs1-ch33-064": "Detailed truncated ('or malicious low-born perso'). TT to reconstruct.",
    "bphs1-ch33-065": "Detailed truncated ('This is a high '). TT to reconstruct.",
    "bphs1-ch33-072": "Detailed truncated ('from the Karak'). TT to reconstruct.",
    "bphs1-ch33-074": "Detailed truncated ('Parsahara'). Dangling reference. TT to reconstruct.",
}


def main():
    parser = argparse.ArgumentParser(
        description="Phase 2 triage: 33 rules → pending_human_review"
    )
    parser.add_argument("--mongo-url", default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes (default: dry run)")
    args = parser.parse_args()

    if not args.mongo_url:
        sys.exit("❌ --mongo-url required")

    from pymongo import MongoClient
    col = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10000)[args.db_name]["interpretation_rules"]

    now = datetime.now(timezone.utc).isoformat()
    all_rules = {**BUCKET_B, **DATA_QUALITY}

    print(f"\n{'='*70}")
    print(f"PHR PATCH -- {len(all_rules)} rules → pending_human_review")
    print(f"  Bucket B (validator errors) : {len(BUCKET_B)}")
    print(f"  Data quality (truncated)    : {len(DATA_QUALITY)}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY RUN'}")
    print(f"{'='*70}\n")

    patched = 0
    missing = []

    for rid, note in all_rules.items():
        doc = col.find_one({"rule_id": rid}, {"_id": 0, "approval_status": 1})
        if not doc:
            missing.append(rid)
            print(f"  ⚠  NOT FOUND: {rid}")
            continue

        group = "Bucket B (validator error)" if rid in BUCKET_B else "Data quality"
        print(f"  {rid}  [{group}]")
        if not args.apply:
            print(f"    note: {note[:80]}")

        if args.apply:
            col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":         "pending_human_review",
                    "validation.verdict":      "spot_check",
                    "validation.flag_reason":  note,
                    "validation.validated_at": now,
                }}
            )
            patched += 1
        else:
            patched += 1

    print(f"\n{'─'*70}")
    print(f"  Would patch / Patched : {patched}")
    print(f"  Missing in DB         : {len(missing)}")
    if not args.apply:
        print(f"\n[DRY RUN] No changes written. Re-run with --apply.")
    else:
        print(f"\n✅ Done. {patched} rules → pending_human_review.")


if __name__ == "__main__":
    main()
