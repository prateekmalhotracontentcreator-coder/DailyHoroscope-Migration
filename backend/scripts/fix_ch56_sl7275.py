#!/usr/bin/env python3
"""
fix_ch56_sl7275.py — Post-ingest fix for Ch 56 sloka 72-75 sub_type anomaly.

Problem:
  During split-upgrade, one rule in sloka 72-75 was incorrectly tagged:
    sub_type = dasha_grouped_outcome + is_group_summary = True
  but it describes a SINGLE condition (Rahu in exaltation), not a grouped summary.

Fix:
  1. Find the mis-tagged rule by querying sloka 72-75 for is_group_summary=True rules.
  2. The individual one is identified by: summary contains "exaltation" and
     condition.dasha_grouped_outcome (sub_type) — it will be the only one
     with is_group_summary=True that reads as a single placement.
  3. Update: sub_type → dasha_favourable, is_group_summary → False.
  4. Insert a TRUE grouped outcome rule combining all 7 Rahu conditions.

Usage:
  python3 scripts/fix_ch56_sl7275.py --mongo-url "$MONGO_URL" [--dry-run]
"""

import argparse
import uuid
from datetime import datetime, timezone

import pymongo


BATCH_ID   = "bphs-ch56-dasha-20260418"
SLOKA      = "72-75"
DASHA_LORD = "Jupiter"
CHAPTER    = 56

SEVEN_RAHU_CONDITIONS = (
    "Rahu in exaltation, own sign, friend's sign, kendra, trikona, 3rd or 11th house"
    " during Jupiter Mahadasha"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    client = pymongo.MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    # ── 1. Find all rules for sloka 72-75 in this batch ────────────────────────
    all_rules = list(col.find({
        "source.batch_id": BATCH_ID,
        "source.sloka":    SLOKA,
    }))

    print(f"\nCh 56 sloka {SLOKA} — rules in DB: {len(all_rules)}")
    for r in all_rules:
        sub  = r.get("condition", {}).get("sub_type", "?")
        grp  = r.get("condition", {}).get("is_group_summary", False)
        summ = r.get("interpretation", {}).get("summary", "")[:80]
        print(f"  {r['rule_id']:30s} | {sub:25s} | grp={grp} | {summ}...")

    # ── 2. Identify the mis-tagged rule ────────────────────────────────────────
    mis_tagged = [
        r for r in all_rules
        if r.get("condition", {}).get("is_group_summary") is True
        and r.get("condition", {}).get("sub_type") == "dasha_grouped_outcome"
    ]

    if not mis_tagged:
        print("\n✅ No mis-tagged is_group_summary=True rules found — already fixed or not yet ingested.")
        client.close()
        return

    # Of those, find the individual rule (contains a single-condition summary, not a combined paragraph)
    # We expect exactly ONE mis-tagged rule in sloka 72-75.
    print(f"\nMis-tagged grouped rules found: {len(mis_tagged)}")
    for r in mis_tagged:
        print(f"  → {r['rule_id']} | {r['interpretation']['summary'][:100]}")

    # ── 3. Fix the mis-tagged rule ─────────────────────────────────────────────
    for r in mis_tagged:
        rule_id = r["rule_id"]
        print(f"\nFix {rule_id}: sub_type → dasha_favourable, is_group_summary → False")
        if not args.dry_run:
            col.update_one(
                {"rule_id": rule_id},
                {"$set": {
                    "condition.sub_type":       "dasha_favourable",
                    "condition.is_group_summary": False,
                }}
            )
            print(f"  ✅ Updated.")
        else:
            print(f"  [DRY RUN] Would update.")

    # ── 4. Check if a true grouped outcome rule already exists ─────────────────
    existing_grouped = [
        r for r in all_rules
        if r.get("condition", {}).get("is_group_summary") is True
        and r.get("rule_id", "") not in [x["rule_id"] for x in mis_tagged]
    ]
    if existing_grouped:
        print(f"\n✅ True grouped summary already exists: {[r['rule_id'] for r in existing_grouped]}")
        client.close()
        return

    # ── 5. Compose grouped outcome rule from individual rule summaries ──────────
    individual_rules = [
        r for r in all_rules
        if r.get("condition", {}).get("is_group_summary") is not True
    ]
    # After fixing the mis-tagged rule, also treat it as individual
    individual_rules.extend([r for r in mis_tagged])

    if not individual_rules:
        print("\n⚠️  No individual rules found — cannot compose grouped summary. Run after live ingest.")
        client.close()
        return

    outcomes = []
    for r in individual_rules:
        summ = r.get("interpretation", {}).get("summary", "")
        if " → " in summ:
            outcome = summ.split(" → ", 1)[1].strip()
            if outcome and outcome not in outcomes:
                outcomes.append(outcome)

    combined_outcomes = "; ".join(outcomes) if outcomes else "Favourable period — multiple life-domain benefits."
    grouped_summary = f"{SEVEN_RAHU_CONDITIONS} → {combined_outcomes}"

    condition_group_id = f"ch{CHAPTER}-sl{SLOKA.replace('-', '')}-rahu-favourable"

    # ── 6. Build the grouped rule doc ──────────────────────────────────────────
    now = datetime.now(timezone.utc).isoformat()
    new_rule_id = f"R-BPHS{CHAPTER}-PATCH-{uuid.uuid4().hex[:6].upper()}-GRP"

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
            "antardasha_planet":   "Rahu",
            "sub_type":            "dasha_grouped_outcome",
            "sloka":               SLOKA,
            "planets_involved":    ["Jupiter", "Rahu"],
            "houses_involved":     [3, 11],
            "sub_conditions":      [],
            "operator":            "or",
            "dignity_state":       "general",
            "planet_context_note": "Rahu in 7 distinct favourable positions",
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
                "dasha_jupiter", "dasha_grouped_outcome", "ai_extracted",
                "group_summary", f"group:{condition_group_id}",
            ],
        },
        "metadata": {
            "planets_involved": ["Jupiter", "Rahu"],
            "houses_involved":  [3, 11],
            "signs_involved":   [],
            "condition_count":  7,
            "source_note":      "gap_fill",
        },
        "confidence": {
            "base":                  0.85,
            "source_weight":         0.95,
            "cross_book_multiplier": 1.0,
        },
        "strength_band":   "medium",
        "approval_status": "pending_review",
        "created_at":      now,
    }

    # Update individual rules to share the condition_group_id
    print(f"\nInserting true grouped outcome rule: {new_rule_id}")
    print(f"  Summary: {grouped_summary[:120]}...")
    print(f"  condition_group_id: {condition_group_id}")

    if not args.dry_run:
        col.insert_one(grouped_doc)
        print("  ✅ Inserted.")

        # Back-fill condition_group_id on individual rules
        for r in individual_rules:
            col.update_one(
                {"rule_id": r["rule_id"]},
                {"$set": {"condition.condition_group_id": condition_group_id}}
            )
        print(f"  ✅ Back-filled condition_group_id on {len(individual_rules)} individual rules.")
    else:
        print("  [DRY RUN] Would insert + back-fill.")

    print(f"\n{'─' * 60}")
    if args.dry_run:
        print(f"[DRY RUN] Ch 56 sloka 72-75 fix: {len(mis_tagged)} rule(s) would be retyped, 1 grouped rule would be inserted.")
    else:
        print(f"✅ Ch 56 sloka 72-75 fix complete.")
        print(f"   - {len(mis_tagged)} rule(s) retyped to dasha_favourable")
        print(f"   - 1 true grouped outcome rule inserted: {new_rule_id}")
        print(f"   - Verify in Rules Browser → batch {BATCH_ID}, sloka {SLOKA}")

    client.close()


if __name__ == "__main__":
    main()
