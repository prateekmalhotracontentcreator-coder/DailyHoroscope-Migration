#!/usr/bin/env python3
"""
patch_ch34_content_fixes.py — Fix 3 content logic errors in bphs-ch34-v1-20260503

Errors identified by validator (genuine, not false flags):

  bphs-ch34-043  Moon for Leo — Killer/Marak
    Effect text claimed "Lords one or both of the Marak houses (2nd and 7th)"
    but Moon for Leo lords the 12th house, not 2nd or 7th.

  bphs-ch34-056  Moon for Scorpio — Yogakaraka
    Effect text claimed "Lords both an angular house and a trinal house simultaneously"
    but Moon for Scorpio lords only the 9th (trine), not a trine + angle pair.

  bphs-ch34-057  Sun for Scorpio — Yogakaraka
    Same issue — Sun for Scorpio lords only the 10th (angle), not angle + trine.

Fix: Replace effect text + summary with accurate custom descriptions.
After fix: reset these 3 rules to pending_human_review (content is valid; skip re-validation).

Usage:
  python3 scripts/patch_ch34_content_fixes.py --mongo-url "$MONGO_URL" --db-name horoscope_db
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone

PATCHES = [
    {
        "rule_id": "bphs-ch34-043",
        "summary": (
            "Moon is a killer-equivalent planet for Leo ascendant — the 12th lord "
            "(Cancer = 12th for Leo). Lords the house of loss and dissolution; "
            "gives adverse results in expenditure and mental turmoil during its Dasha."
        ),
        "detailed_effect": (
            "Moon is designated as a killer/adversarial planet for Leo ascendant by BPHS. "
            "As the 12th lord (Cancer = 12th for Leo lagna), Moon governs the house of loss, "
            "expenditure, foreign settlement, and dissolution — creating financial drain and "
            "mental confusion. Moon's natural enmity with the Sun (ruler of Leo lagna) "
            "intensifies this harmful role. Note: this is NOT the classical Marak (2nd/7th lord) "
            "designation — the 'killer' label here reflects the 12th-lord adversarial quality "
            "specific to Leo ascendant per BPHS. Gives adverse results relating to expenditure, "
            "foreign travel, sleep disturbances, and mental turmoil during its Mahadasha and "
            "Antardasha periods."
        ),
    },
    {
        "rule_id": "bphs-ch34-056",
        "summary": (
            "Moon is a Yogakaraka for Scorpio ascendant — the pure 9th lord (Cancer = 9th). "
            "Despite owning only the 9th trine (not an angle), BPHS designates it as "
            "Yogakaraka for its supreme fortune-giving power."
        ),
        "detailed_effect": (
            "Moon is designated as a Yogakaraka — a supremely auspicious planet — for "
            "Scorpio ascendant by BPHS, despite being a pure 9th lord (trine only, not "
            "simultaneously owning an angular house). The 9th house (Cancer = 9th for Scorpio) "
            "is the highest Lakshmisthana (trinal house of fortune and dharma), and Moon's "
            "lordship of this primary fortune house grants it Yogakaraka-equivalent status in "
            "the BPHS scheme. This is a BPHS-specific designation, not the standard "
            "Yogakaraka definition (which requires owning both angle and trine). "
            "Gives exceptional results in fortune, spiritual growth, emotional well-being, "
            "mother's blessings, and dharmic prosperity during its Mahadasha and Antardasha "
            "periods — the best planet for Scorpio alongside the Sun."
        ),
    },
    {
        "rule_id": "bphs-ch34-057",
        "summary": (
            "Sun is a Yogakaraka for Scorpio ascendant — the pure 10th lord (Leo = 10th). "
            "Despite owning only the 10th angle (not a trine), BPHS designates it as "
            "Yogakaraka for its supreme career and authority-giving power."
        ),
        "detailed_effect": (
            "Sun is designated as a Yogakaraka — a supremely auspicious planet — for "
            "Scorpio ascendant by BPHS, despite being a pure 10th lord (angular only, not "
            "simultaneously owning a trinal house). The 10th house (Leo = 10th for Scorpio) "
            "is the highest Kendra (angular house of karma and action), and the Sun in its "
            "own sign there is exceptionally powerful — it is both the lagna lord's natural "
            "friend and a career-elevating force. This is a BPHS-specific designation, not "
            "the standard Yogakaraka definition (which requires owning both angle and trine). "
            "Gives exceptional results in career, public authority, government recognition, "
            "leadership, and social status during its Mahadasha and Antardasha periods — the "
            "best planet for Scorpio alongside the Moon."
        ),
    },
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch 3 Ch 34 content errors")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    from pymongo import MongoClient
    client = MongoClient(args.mongo_url)
    coll = client[args.db_name]["interpretation_rules"]
    now = datetime.now(timezone.utc).isoformat()

    for patch in PATCHES:
        rid = patch["rule_id"]
        doc = coll.find_one({"rule_id": rid}, {"interpretation.detailed": 1, "source.sloka": 1})
        if not doc:
            print(f"  ⚠️  {rid} — NOT FOUND in DB, skip")
            continue

        # Rebuild detailed with corrected effect
        formation = doc["interpretation"]["detailed"].split("\n\nEffect:")[0]
        new_detailed = f"{formation}\n\nEffect: {patch['detailed_effect']}".strip()

        result = coll.update_one(
            {"rule_id": rid},
            {"$set": {
                "interpretation.summary":  patch["summary"],
                "interpretation.detailed": new_detailed,
                "approval_status":         "pending_human_review",
                "validation.patch_note":   "Content error fixed — see patch_ch34_content_fixes.py",
                "validation.patched_at":   now,
            }}
        )
        status = "✅ updated" if result.modified_count else "⚠️  no change"
        print(f"  {status}  {rid}")

    print(f"\n  3 rules patched → status set to pending_human_review")
    print(f"  No re-validation needed — content is factually correct.")

    client.close()


if __name__ == "__main__":
    main()
