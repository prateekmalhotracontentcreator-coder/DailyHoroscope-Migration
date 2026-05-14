"""
verify_ch57_gaps.py  |  Ch 57 split-upgrade gap verification
Queries all existing rules for 8 flagged slokas and prints full summaries.

Usage:
    cd /Users/apple/DailyHoroscope-Migration/backend
    python3 scripts/verify_ch57_gaps.py --mongo-url "$MONGO_URL"
"""

import argparse
import pymongo

BATCH_ID = "bphs-ch57-dasha-20260419"

VERIFY_SLOKAS = {
    "1-3":   "Are the 6 existing rules individually-queryable splits (Saturn in own sign / exaltation / deep exaltation / kendra / trikona / yogakaraka) or one merged rule?",
    "14-15": "Do existing rules cover Mercury as 2nd lord AND Mercury as 7th lord unfavourable?",
    "16-18": "Is 'Ketu related to lord of Ascendant → favourable' present?",
    "22-23": "Do existing rules cover Ketu as 2nd lord AND Ketu as 7th lord unfavourable?",
    "24-27": "Are Jupiter-in-transit and Saturn-in-transit favourable rules present?",
    "28-29": "Are Venus debilitation AND Venus combust rules present (separate from Venus in 6th/8th/12th)?",
    "35-36": "Do existing rules cover Venus as 2nd lord AND Venus as 7th lord unfavourable?",
    "65-67": "Is the middle-portion timing rule present ('Rahu in favourable condition during middle portion → cordial relations')?",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    args = parser.parse_args()

    client = pymongo.MongoClient(args.mongo_url)
    col = client[args.db_name]["interpretation_rules"]

    # ── Probe: find one rule from this batch and inspect its field structure ──
    sample = col.find_one({"source.batch_id": BATCH_ID})
    if not sample:
        print(f"\n⚠️  No rules found for batch_id={BATCH_ID} in {args.db_name}.interpretation_rules")
        print("    Check DB name and batch ID.")
        return

    src = sample.get("source", {})
    print(f"\nField probe (first rule in batch):")
    print(f"  source.batch_id  = {src.get('batch_id')!r}")
    print(f"  source.chapter   = {src.get('chapter')!r}  (type: {type(src.get('chapter')).__name__})")
    print(f"  source.sloka     = {src.get('sloka')!r}")
    print(f"  rule_id          = {sample.get('rule_id')!r}")
    print()

    # Build the sloka query from whatever chapter value is actually stored
    chapter_val = src.get("chapter")

    print(f"Ch 57 Gap Verification  |  batch: {BATCH_ID}")
    print(f"DB: {args.db_name}  |  Querying 8 flagged slokas\n")
    print("=" * 72)

    for sloka, question in VERIFY_SLOKAS.items():
        # Try batch_id + sloka first (most reliable)
        rules = list(col.find(
            {"source.batch_id": BATCH_ID, "source.sloka": sloka},
            {"rule_id": 1, "sub_type": 1, "metadata.source_note": 1,
             "condition.is_group_summary": 1, "interpretation.summary": 1, "_id": 0}
        ).sort("rule_id", 1))

        # Fallback: chapter value + sloka (catches rules from same chapter but different batch label)
        if not rules and chapter_val is not None:
            rules = list(col.find(
                {"source.chapter": chapter_val, "source.sloka": sloka},
                {"rule_id": 1, "sub_type": 1, "metadata.source_note": 1,
                 "condition.is_group_summary": 1, "interpretation.summary": 1, "_id": 0}
            ).sort("rule_id", 1))

        print(f"\n{'═' * 72}")
        print(f"  Sloka {sloka}  |  {len(rules)} rules in DB")
        print(f"  ❓ {question}")
        print(f"{'─' * 72}")

        if not rules:
            print("  (no rules found for this sloka)")
        else:
            for r in rules:
                rule_id     = r.get("rule_id", "?")
                sub_type    = r.get("sub_type", "?")
                source_note = r.get("metadata", {}).get("source_note", "original")
                is_grp      = r.get("condition", {}).get("is_group_summary", False)
                summary     = r.get("interpretation", {}).get("summary", "")

                grp_tag  = " [GRP]" if is_grp else ""
                note_tag = f" [{source_note}]" if source_note else ""
                summary_short = summary[:95] + "..." if len(summary) > 95 else summary

                print(f"  {rule_id:<36} | {sub_type:<22}{grp_tag}{note_tag}")
                print(f"    {summary_short}")

    print(f"\n{'=' * 72}")
    print("Paste this output back for gap-fill decisions.\n")


if __name__ == "__main__":
    main()
