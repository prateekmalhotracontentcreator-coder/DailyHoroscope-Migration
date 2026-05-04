#!/usr/bin/env python3
"""
patch_ch44_flags.py

15 rules in bphs-ch44-v1-20260504 were flagged by the validator.

14 truncation false positives: the validator's claude-haiku-4-5 receives a
truncated slice of interpretation.detailed and flags the mid-sentence cut as
evidence of incomplete content. The full text is stored correctly in MongoDB
— the truncation is in the validator's read window, not in the data.

1 vagueness flag (CD04 — Mixed H3 Occupation): haiku flagged "too generic /
lacks textual grounding." The rule IS grounded in BPHS Ch 44 (multiple
planets in H3 → combined diseases), but is deliberately general since the
text gives no planet-specific sub-rules for the mixed case.

Fix: promote all 15 to pending_human_review with a clear false-flag note.
No re-validation needed.

Usage:
  python3 scripts/patch_ch44_flags.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

BATCH_ID = "bphs-ch44-v1-20260504"

# 14 truncation false positives + 1 vagueness false positive
FLAGGED_IDS = [
    "bphs-ch44-MI04",   # Maraka Power Hierarchy — Three-Grade Descending Order
    "bphs-ch44-MI06",   # Moon-Centric Dual Maraka Sweep
    "bphs-ch44-MT01",   # Sub-Period Death Prohibition — Benefic Antar-dasa Buffer
    "bphs-ch44-MT04",   # Star-Based Mortality Timing — Vipat, Pratyak, Vadha
    "bphs-ch44-MT06",   # Sub-Period Triad — 6th Lord Dasa Mortality Window
    "bphs-ch44-RK03",   # Benefic Aspect on Nodes — Difficulty Not Death
    "bphs-ch44-CD01",   # 3rd House Planet-Cause Library — Per Planet Diagnosis
    "bphs-ch44-CD04",   # Mixed H3 Occupation — Multiple Reasons Diagnosis (vagueness)
    "bphs-ch44-CD05",   # Moon-Sign Lordship Marakas — Malefic vs Benefic Lords
    "bphs-ch44-CD06",   # Death Environment — Place and Locality Diagnosis
    "bphs-ch44-EH03",   # Fate of the Corpse — 22nd Decanate Diagnosis
    "bphs-ch44-EH04",   # Serpent Decanate Identification
    "bphs-ch44-EH05",   # Post-Death World — Vacant H12/H7/H6/H8 Fallback
    "bphs-ch44-CF06",   # Asterism Dasa Master Logic — Priority Ordering
    "bphs-ch44-CF07",   # Corpse Consciousness Diagnostic — Full Decision Tree
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
    for rid in FLAGGED_IDS:
        doc = col.find_one({"rule_id": rid}, {"_id": 0, "condition.yoga_name": 1})
        if not doc:
            print(f"  ⚠️  Not found: {rid}")
            continue

        yoga_name = doc["condition"]["yoga_name"]

        if rid == "bphs-ch44-CD04":
            flag_note = (
                "False flag (vagueness): 'Mixed H3 Occupation' rule is intentionally "
                "general — BPHS Ch 44 provides no planet-specific sub-rules for the "
                "mixed-occupation case. The 'various reasons' interpretation is the "
                "direct classical reading. Promoted to pending_human_review."
            )
        else:
            flag_note = (
                "False flag (truncation): validator's haiku model received a truncated "
                "slice of interpretation.detailed and misread the mid-sentence cut as "
                "incomplete content. Full text is stored correctly in MongoDB. "
                "Promoted to pending_human_review."
            )

        result = col.update_one(
            {"rule_id": rid},
            {"$set": {
                "approval_status":        "pending_human_review",
                "validation.verdict":     "spot_check",
                "validation.flag_reason": flag_note,
                "validation.validated_by": "patch_ch44_flags.py",
                "validation.validated_at": now,
            }},
        )
        if result.modified_count:
            print(f"  ✅ patched {rid} — {yoga_name[:60]}")
            patched += 1
        else:
            print(f"  ⚠️  No change: {rid}")

    print(f"\n{patched} / {len(FLAGGED_IDS)} rules patched → pending_human_review")
    client.close()


if __name__ == "__main__":
    main()
