#!/usr/bin/env python3
"""
audit_decode_folders.py
--------------------------------------------------------------------
Pre-ingest audit: count rules in all 7 KE decode folders.
Run before any ingest to verify expected rule counts.

Usage:
    python3 backend/scripts/audit_decode_folders.py

Output: table of files, rule counts, active counts per book.
"""

import json
import glob
import os
from pathlib import Path

BOOKS = {
    "BPHS_Vol1": "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode",
    "BPHS_Vol2": "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode",
    "300_Combinations": "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode",
    "300_Horoscopes": "/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredHoroscopes_CC_Decode",
    "Longevity_Unnatural": "/Users/apple/Documents/Knowledge Engine_eBooks/LongevityUnnatural_CC_Decode",
    "Medical_Astrology": "/Users/apple/Documents/Knowledge Engine_eBooks/MedicalAstrology_CC_Decode",
    "Phaladeepika": "/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode",
}

SKIP_FRAGMENTS = ("Contradictions", "NLM_Extract", "OCR", "_archive", "_ARCHIVED")


def should_skip(filename: str) -> bool:
    return any(frag in filename for frag in SKIP_FRAGMENTS)


def main() -> None:
    grand_total = 0
    grand_active = 0

    for book, folder in BOOKS.items():
        files = sorted(glob.glob(f"{folder}/**/*Rules*.json", recursive=True))
        total_rules = 0
        active_rules = 0
        file_list = []

        for f in files:
            basename = os.path.basename(f)
            if should_skip(basename):
                continue
            try:
                raw = json.load(open(f, encoding="utf-8"))
                rules = raw.get("rules", raw) if isinstance(raw, dict) else raw
                rules = [r for r in rules if isinstance(r, dict)]
                active = [r for r in rules if r.get("active", True) is not False]
                missing_ids = [r for r in active if not r.get("rule_id")]
                total_rules += len(rules)
                active_rules += len(active)
                warn = f"  ⚠  {len(missing_ids)} missing rule_id" if missing_ids else ""
                file_list.append(
                    f"    {basename}: {len(rules)} total / {len(active)} active{warn}"
                )
            except Exception as e:
                file_list.append(f"    ERROR {basename}: {e}")

        grand_total += total_rules
        grand_active += active_rules
        print(f"\n{'='*60}")
        print(f"BOOK: {book}")
        print(f"  Files: {len(files)} | Total rules: {total_rules} | Active: {active_rules}")
        for line in file_list:
            print(line)

    print(f"\n{'='*60}")
    print(f"GRAND TOTAL: {grand_total} rules ({grand_active} active) across 7 books")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
