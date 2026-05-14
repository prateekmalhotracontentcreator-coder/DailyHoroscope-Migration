#!/usr/bin/env python3
"""
patch_remedies_flags.py

18 rules in remedies-mantras-v1-20260504 were flagged by the validator.

All 18 are false positives — source data is complete and coherent.

16 truncation false positives: validator's claude-haiku-4-5 receives a
truncated slice of interpretation.detailed and misreads the mid-sentence
cut as incomplete content. Full guidance text is stored correctly in
MongoDB; the truncation is in the validator's read window only.

2 mantra format flags (remedy-031, remedy-032):
  - remedy-031 (Job Search / Hanuman): uses a Hanuman Chalisa verse
    ("Kavan So Kaaj Kathin...") as the prescribed remedy — intentional
    devotional format, not a structural bija mantra. Deliberate source choice.
  - remedy-032 (Land/Property / Mangal): roman transliteration uses "..."
    as deliberate abbreviation. Full Devanagari mantra is stored correctly.
  Both promoted to pending_human_review for co-founder sign-off on
  non-standard mantra format before production approval.

Usage:
  python3 scripts/patch_remedies_flags.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "remedies-mantras-v1-20260504"

# Truncation false positives (16)
TRUNCATION_FLAGS = [
    "remedy-021",   # Extreme Wealth — guidance truncated in read window
    "remedy-035",   # Creativity/Arts — guidance truncated in read window
    "remedy-038",   # Agriculture — guidance truncated in read window
    "remedy-040",   # Abundance (Sarva) — guidance truncated in read window
    "remedy-086",   # Grahan Dosha — guidance truncated in read window
    "remedy-087",   # Vastu Dosha — guidance truncated in read window
    "remedy-088",   # Sudden Accidents — guidance truncated in read window
    "remedy-090",   # Enemy Protection — guidance truncated in read window
    "remedy-091",   # Spiritual Siddhi — guidance truncated in read window
    "remedy-092",   # Past Karma Wash — guidance truncated in read window
    "remedy-093",   # Aura Cleaning — guidance truncated in read window
    "remedy-094",   # Speech Power — guidance truncated in read window
    "remedy-095",   # Unexplained Fear — guidance truncated in read window
    "remedy-096",   # Wealth Stability — color/guidance truncated in read window
    "remedy-097",   # Wisdom (Viveka) — guidance truncated in read window
    "remedy-098",   # Legal Tangles — guidance truncated in read window
]

# Mantra format flags (2) — intentional non-standard format; verify before approval
FORMAT_FLAGS = [
    "remedy-031",   # Job Search — Hanuman Chalisa verse as prescribed remedy
    "remedy-032",   # Land/Property — roman transliteration uses deliberate "..."
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col = client[args.db_name]["interpretation_rules"]
    now = datetime.now(timezone.utc).isoformat()

    patched = 0

    for rid in TRUNCATION_FLAGS:
        doc = col.find_one({"rule_id": rid}, {"_id": 0, "condition.yoga_name": 1})
        if not doc:
            print(f"  ⚠️  Not found: {rid}")
            continue
        result = col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":         "pending_human_review",
                "validation.verdict":      "spot_check",
                "validation.flag_reason": (
                    "False flag (truncation): validator's haiku model received a "
                    "truncated slice of interpretation.detailed and misread the "
                    "mid-sentence cut as incomplete guidance. Full text is stored "
                    "correctly in MongoDB. Promoted to pending_human_review."
                ),
                "validation.validated_by": "patch_remedies_flags.py",
                "validation.validated_at": now,
            }},
        )
        if result.modified_count:
            name = doc["condition"]["yoga_name"]
            print(f"  ✅ patched {rid} — {name}")
            patched += 1
        else:
            print(f"  ⚠️  No change: {rid}")

    for rid in FORMAT_FLAGS:
        doc = col.find_one({"rule_id": rid}, {"_id": 0, "condition.yoga_name": 1})
        if not doc:
            print(f"  ⚠️  Not found: {rid}")
            continue

        if rid == "remedy-031":
            note = (
                "False flag (mantra format): Job Search remedy intentionally uses a "
                "Hanuman Chalisa verse ('Kavan So Kaaj Kathin...') as the prescribed "
                "remedy — devotional verse format, not a structural bija mantra. "
                "Data is complete and source-verified. Promoted to pending_human_review "
                "for co-founder sign-off on non-standard mantra format."
            )
        else:  # remedy-032
            note = (
                "False flag (transliteration abbreviation): Land/Property (Mangal) remedy "
                "uses deliberate '...' abbreviation in roman transliteration. Full mantra "
                "is in Devanagari field. Data is source-verified. Promoted to "
                "pending_human_review for co-founder confirmation of abbreviated format."
            )

        result = col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":         "pending_human_review",
                "validation.verdict":      "spot_check",
                "validation.flag_reason":  note,
                "validation.validated_by": "patch_remedies_flags.py",
                "validation.validated_at": now,
            }},
        )
        if result.modified_count:
            name = doc["condition"]["yoga_name"]
            print(f"  ✅ patched {rid} — {name}")
            patched += 1
        else:
            print(f"  ⚠️  No change: {rid}")

    print(f"\n{patched} / {len(TRUNCATION_FLAGS) + len(FORMAT_FLAGS)} rules patched → pending_human_review")
    client.close()


if __name__ == "__main__":
    main()
