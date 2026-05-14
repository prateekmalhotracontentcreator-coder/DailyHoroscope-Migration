#!/usr/bin/env python3
"""
fix_ch47_sl4548.py -- Post-ingest fix for Ch 47 split-upgrade sloka 45-48.

Problem:
  All 7 Jupiter placement split-upgrade rules in sloka 45-48 were inserted as
  dasha_grouped_outcome + is_group_summary=True by the LLM at temperature=0.
  Each is a single-condition individual rule (Jupiter in kendra / trikona /
  exaltation / own sign / moolatrikona / 3rd / 11th house), not a grouped summary.

Fix:
  1. Find all dasha_grouped_outcome + split_upgrade rules in sloka 45-48.
  2. Retype each: sub_type → dasha_favourable, is_group_summary → False.
  3. Insert a true grouped outcome rule covering all 7 conditions.
  4. Back-fill condition_group_id on all individual rules.

Usage:
  python3 scripts/fix_ch47_sl4548.py --mongo-url "$MONGO_URL" [--dry-run]

Same pattern as:
  - Ch 55 sloka 21-24 (Saturn AD mis-tagged in Ch 55 split-upgrade)
  - Ch 59 sloka 69-71 (Mercury AD mis-tagged in Ch 59 split-upgrade)
"""

import argparse
import uuid
from datetime import datetime, timezone

import pymongo

BATCH_ID   = "bphs-ch47-dasha-20260416"
DASHA_LORD = "Sun"
CHAPTER    = 47
SLOKA      = "45-48"
AD_PLANET  = "Jupiter"  # antardasha planet for this sloka


def main():
    parser = argparse.ArgumentParser(description="Fix mis-tagged dasha_grouped_outcome rules in Ch 47 sloka 45-48.")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()

    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"\nfix_ch47_sl4548.py  |  Batch: {BATCH_ID}  |  Sloka: {SLOKA}  |  Mode: {mode}")

    client = pymongo.MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    # ── Step 1: Find all rules for this sloka ──────────────────────────────────
    all_rules = list(col.find({
        "source.batch_id": BATCH_ID,
        "source.sloka":    SLOKA,
    }))
    print(f"\nAll rules in DB for sloka {SLOKA}: {len(all_rules)}")
    for r in all_rules:
        sub  = r.get("condition", {}).get("sub_type", "?")
        grp  = r.get("condition", {}).get("is_group_summary", False)
        note = r.get("metadata", {}).get("source_note", "?")
        summ = r.get("interpretation", {}).get("summary", "")[:90]
        print(f"  {r['rule_id']:38s} | {sub:25s} | grp={str(grp):5s} | note={note} | {summ}")

    # ── Step 2: Find the mis-tagged rules ─────────────────────────────────────
    mis_tagged = [
        r for r in all_rules
        if r.get("condition", {}).get("sub_type") == "dasha_grouped_outcome"
        and r.get("metadata", {}).get("source_note") == "split_upgrade"
    ]

    print(f"\nMis-tagged rules to fix: {len(mis_tagged)}")
    if not mis_tagged:
        print("✅ No mis-tagged rules found -- already fixed or pattern differs. Exiting.")
        client.close()
        return

    for r in mis_tagged:
        print(f"  → {r['rule_id']} | {r['interpretation']['summary'][:100]}")

    # Check if a true grouped rule already exists (avoid double-insert)
    existing_grouped = [
        r for r in all_rules
        if r.get("condition", {}).get("is_group_summary") is True
        and r.get("metadata", {}).get("source_note") != "split_upgrade"
    ]
    if existing_grouped:
        print(f"\n✅ A true grouped rule already exists ({existing_grouped[0]['rule_id']}) -- skipping insert.")
        # Still retype the mis-tagged ones
    else:
        print(f"\nNo true grouped rule exists yet -- will insert one.")

    # ── Step 3: Retype mis-tagged rules ───────────────────────────────────────
    print(f"\n--- Retyping {len(mis_tagged)} rules: dasha_grouped_outcome → dasha_favourable ---")
    for r in mis_tagged:
        rule_id = r["rule_id"]
        print(f"  Updating {rule_id}...")
        if not args.dry_run:
            result = col.update_one(
                {"rule_id": rule_id},
                {"$set": {
                    "condition.sub_type":         "dasha_favourable",
                    "condition.is_group_summary":  False,
                }}
            )
            print(f"    ✅ Modified count: {result.modified_count}")
        else:
            print(f"    [DRY RUN] Would update: sub_type → dasha_favourable, is_group_summary → False")

    # ── Step 4: Verify retype ─────────────────────────────────────────────────
    if not args.dry_run:
        remaining = col.count_documents({
            "source.batch_id": BATCH_ID,
            "source.sloka":    SLOKA,
            "condition.sub_type": "dasha_grouped_outcome",
            "metadata.source_note": "split_upgrade",
        })
        print(f"\nRemaining dasha_grouped_outcome (split_upgrade) in sloka {SLOKA}: {remaining} (should be 0)")

    # ── Step 5: Insert true grouped outcome rule (if not exists) ──────────────
    if existing_grouped:
        print(f"\n✅ Skipping grouped insert -- already present.")
    else:
        # Build condition list from mis_tagged rule summaries
        conditions, outcomes = [], []
        for r in mis_tagged:
            summ = r.get("interpretation", {}).get("summary", "")
            if " → " in summ:
                cond    = summ.split(" → ", 1)[0].strip()
                outcome = summ.split(" → ", 1)[1].strip()
                if cond    not in conditions: conditions.append(cond)
                if outcome not in outcomes:   outcomes.append(outcome)

        condition_count    = len(conditions)
        base_condition     = "; ".join(conditions) if conditions else \
                             f"{AD_PLANET} in multiple favourable positions during {DASHA_LORD} Mahadasha"
        combined_outcomes  = "; ".join(outcomes) if outcomes else \
                             f"Favourable period with multiple {AD_PLANET} placement effects."
        grouped_summary    = f"{base_condition} → {combined_outcomes}"

        sloka_key          = SLOKA.replace("-", "")
        condition_group_id = f"ch{CHAPTER}-sl{sloka_key}-{AD_PLANET.lower()}-favourable"
        new_rule_id        = f"R-BPHS{CHAPTER}-PATCH-{uuid.uuid4().hex[:6].upper()}-GRP"

        print(f"\n--- Inserting true grouped outcome rule ---")
        print(f"  New rule_id       : {new_rule_id}")
        print(f"  antardasha_planet : {AD_PLANET}")
        print(f"  condition_count   : {condition_count}")
        print(f"  condition_group_id: {condition_group_id}")
        print(f"  Summary (first 150): {grouped_summary[:150]}...")

        grouped_doc = {
            "rule_id":    new_rule_id,
            "science_id": "vedic_astrology",
            "source": {
                "batch_id": BATCH_ID,
                "chapter":  CHAPTER,
                "sloka":    SLOKA,
                "book":     "BPHS Vol 2",
            },
            "condition": {
                "type":                "dasha_planet",
                "dasha_lord":          DASHA_LORD,
                "antardasha_planet":   AD_PLANET,
                "sub_type":            "dasha_grouped_outcome",
                "sloka":               SLOKA,
                "planets_involved":    [DASHA_LORD, AD_PLANET],
                "houses_involved":     [],
                "sub_conditions":      [],
                "operator":            "or",
                "dignity_state":       "general",
                "planet_context_note": f"{AD_PLANET} in {condition_count} distinct favourable positions during {DASHA_LORD} MD",
                "condition_group_id":  condition_group_id,
                "is_group_summary":    True,
            },
            "interpretation": {
                "summary":            grouped_summary[:500],
                "detailed":           grouped_summary,
                "full_text_passages": [{"text": grouped_summary, "confidence": "HIGH"}],
                "remedies":           [],
                "life_domain":        "general",
                "tags": [
                    "verbatim", "dasha_planet", f"chapter{CHAPTER}",
                    f"dasha_{DASHA_LORD.lower()}", "dasha_grouped_outcome", "ai_extracted",
                    "group_summary", f"group:{condition_group_id}",
                ],
            },
            "metadata": {
                "planets_involved": [DASHA_LORD, AD_PLANET],
                "houses_involved":  [],
                "signs_involved":   [],
                "condition_count":  condition_count,
                "source_note":      "gap_fill",
            },
            "confidence": {
                "base": 0.85, "source_weight": 0.95, "cross_book_multiplier": 1.0,
            },
            "strength_band":   "medium",
            "approval_status": "pending_review",
            "created_at":      datetime.now(timezone.utc).isoformat(),
        }

        if not args.dry_run:
            col.insert_one(grouped_doc)
            print(f"  ✅ Grouped rule inserted: {new_rule_id}")

            # Back-fill condition_group_id on all individual split-upgrade rules in this sloka
            individual_ids = [r["rule_id"] for r in mis_tagged]
            backfill_result = col.update_many(
                {"rule_id": {"$in": individual_ids}},
                {"$set": {"condition.condition_group_id": condition_group_id}}
            )
            print(f"  ✅ Back-filled condition_group_id on {backfill_result.modified_count} individual rules.")
        else:
            print(f"  [DRY RUN] Would insert grouped rule and back-fill {len(mis_tagged)} individual rules.")

    # ── Final summary ─────────────────────────────────────────────────────────
    print(f"\n{'═' * 60}")
    if args.dry_run:
        print(f"[DRY RUN COMPLETE] {len(mis_tagged)} rules would be retyped → dasha_favourable.")
        if not existing_grouped:
            print(f"1 grouped outcome rule would be inserted.")
    else:
        print(f"✅ Fix complete: {len(mis_tagged)} rules retyped → dasha_favourable.")
        if not existing_grouped:
            print(f"✅ 1 true grouped outcome rule inserted.")
    print(f"Review in Admin > Rules Browser → batch {BATCH_ID}, sloka {SLOKA}")
    client.close()


if __name__ == "__main__":
    main()
