#!/usr/bin/env python3
"""
fix_ch56_sl7275.py — Post-ingest fix for Ch 56 mis-tagged dasha_grouped_outcome rules.

Problem (two slokas affected):
  sloka 72-75: R-BPHS56-PATCH-6CC98D tagged dasha_grouped_outcome + is_group_summary=True
               but summary reads "Rahu in exaltation → ..." — single condition, not a summary.
  sloka 51-53: R-BPHS56-PATCH-CAEF2D tagged dasha_grouped_outcome + is_group_summary=True
               but summary reads "Sun in exaltation → ..." — same pattern.

Fix per sloka:
  1. Find all is_group_summary=True rules in the sloka.
  2. Detect which are single-condition mis-tags (no "," or " or " in condition part).
  3. Retype them: sub_type → dasha_favourable, is_group_summary → False.
  4. Build a true grouped outcome rule from the individual split-upgrade rules.
  5. Insert it and back-fill condition_group_id on individuals.

Usage:
  # Fix both slokas (default):
  python3 scripts/fix_ch56_sl7275.py --mongo-url "$MONGO_URL" [--dry-run]

  # Fix one sloka only:
  python3 scripts/fix_ch56_sl7275.py --mongo-url "$MONGO_URL" --sloka 72-75 [--dry-run]
  python3 scripts/fix_ch56_sl7275.py --mongo-url "$MONGO_URL" --sloka 51-53 [--dry-run]
"""

import argparse
import uuid
from datetime import datetime, timezone

import pymongo


BATCH_ID   = "bphs-ch56-dasha-20260418"
DASHA_LORD = "Jupiter"
CHAPTER    = 56

# Slokas known to have the mis-tagged grouped rule pattern
DEFAULT_SLOKAS = ["72-75", "51-53"]


def is_single_condition(summary: str) -> bool:
    """Return True if the condition part (before →) describes only one placement state."""
    cond = summary.split(" → ")[0].strip() if " → " in summary else summary
    # A true grouped summary lists multiple conditions joined by "," or " or "
    return "," not in cond and " or " not in cond.lower()


def fix_sloka(col, sloka: str, dry_run: bool):
    print(f"\n{'═' * 60}")
    print(f"Sloka {sloka}")
    print(f"{'═' * 60}")

    all_rules = list(col.find({
        "source.batch_id": BATCH_ID,
        "source.sloka":    sloka,
    }))
    print(f"Rules in DB: {len(all_rules)}")

    for r in all_rules:
        sub  = r.get("condition", {}).get("sub_type", "?")
        grp  = r.get("condition", {}).get("is_group_summary", False)
        summ = r.get("interpretation", {}).get("summary", "")[:85]
        print(f"  {r['rule_id']:32s} | {sub:25s} | grp={grp} | {summ}...")

    # ── 1. Identify mis-tagged rules ──────────────────────────────────────────
    candidate_grouped = [
        r for r in all_rules
        if r.get("condition", {}).get("is_group_summary") is True
        and r.get("condition", {}).get("sub_type") == "dasha_grouped_outcome"
    ]

    if not candidate_grouped:
        print(f"\n✅ No is_group_summary=True rules found — already fixed or not ingested.")
        return

    mis_tagged = [r for r in candidate_grouped
                  if is_single_condition(r.get("interpretation", {}).get("summary", ""))]
    true_grouped = [r for r in candidate_grouped if r not in mis_tagged]

    print(f"\nGrouped candidates: {len(candidate_grouped)}  |  mis-tagged: {len(mis_tagged)}  |  true grouped: {len(true_grouped)}")
    for r in mis_tagged:
        print(f"  MIS-TAGGED → {r['rule_id']} | {r['interpretation']['summary'][:100]}")
    for r in true_grouped:
        print(f"  TRUE GRP   → {r['rule_id']} | {r['interpretation']['summary'][:100]}")

    # ── 2. Fix mis-tagged rules ───────────────────────────────────────────────
    for r in mis_tagged:
        rule_id = r["rule_id"]
        print(f"\nFix {rule_id}: sub_type → dasha_favourable, is_group_summary → False")
        if not dry_run:
            col.update_one(
                {"rule_id": rule_id},
                {"$set": {
                    "condition.sub_type":        "dasha_favourable",
                    "condition.is_group_summary": False,
                }}
            )
            print("  ✅ Updated.")
        else:
            print("  [DRY RUN] Would update.")

    # ── 3. Skip grouped insert if a true one already exists ───────────────────
    if true_grouped:
        print(f"\n✅ True grouped summary already exists — no insert needed.")
        return

    # ── 4. Compose grouped rule from split-upgrade individuals ────────────────
    individual_rules = [
        r for r in all_rules
        if r.get("condition", {}).get("is_group_summary") is not True
        and r.get("metadata", {}).get("source_note") != "pre_split_merged"
    ]
    individual_rules.extend(mis_tagged)   # re-include mis-tagged (they are individual rules)

    if not individual_rules:
        print("\n⚠️  No split-upgrade individual rules found — run after live ingest.")
        return

    # Auto-detect antardasha_planet and sub_type polarity from individual rules
    antardasha_planets = list({
        r.get("condition", {}).get("antardasha_planet") for r in individual_rules
        if r.get("condition", {}).get("antardasha_planet")
    })
    antardasha_planet = antardasha_planets[0] if len(antardasha_planets) == 1 else DASHA_LORD

    polarities = [r.get("condition", {}).get("sub_type", "") for r in individual_rules]
    polarity   = "favourable" if "dasha_favourable" in polarities else "unfavourable"
    group_type = f"dasha_{polarity}"

    conditions, outcomes = [], []
    for r in individual_rules:
        summ = r.get("interpretation", {}).get("summary", "")
        if " → " in summ:
            cond    = summ.split(" → ", 1)[0].strip()
            outcome = summ.split(" → ", 1)[1].strip()
            if cond    and cond    not in conditions: conditions.append(cond)
            if outcome and outcome not in outcomes:   outcomes.append(outcome)

    condition_count   = len(conditions)
    base_condition    = "; ".join(conditions) if conditions \
                        else f"{antardasha_planet} in multiple positions during {DASHA_LORD} Mahadasha"
    combined_outcomes = "; ".join(outcomes) if outcomes \
                        else f"{polarity.capitalize()} period with multiple effects."
    grouped_summary   = f"{base_condition} → {combined_outcomes}"

    sloka_key          = sloka.replace("-", "")
    condition_group_id = f"ch{CHAPTER}-sl{sloka_key}-{antardasha_planet.lower()}-{polarity}"
    new_rule_id        = f"R-BPHS{CHAPTER}-PATCH-{uuid.uuid4().hex[:6].upper()}-GRP"

    grouped_doc = {
        "rule_id":    new_rule_id,
        "science_id": "vedic_astrology",
        "source": {
            "batch_id": BATCH_ID,
            "chapter":  CHAPTER,
            "sloka":    sloka,
            "book":     "BPHS Vol 2",
        },
        "condition": {
            "type":                "dasha_planet",
            "dasha_lord":          DASHA_LORD,
            "antardasha_planet":   antardasha_planet,
            "sub_type":            "dasha_grouped_outcome",
            "sloka":               sloka,
            "planets_involved":    list({DASHA_LORD, antardasha_planet}),
            "houses_involved":     [],
            "sub_conditions":      [],
            "operator":            "or",
            "dignity_state":       "general",
            "planet_context_note": f"{antardasha_planet} in {condition_count} distinct {polarity} positions",
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
            "planets_involved": list({DASHA_LORD, antardasha_planet}),
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

    print(f"\nInserting true grouped outcome rule: {new_rule_id}")
    print(f"  antardasha_planet : {antardasha_planet}")
    print(f"  condition_count   : {condition_count}")
    print(f"  condition_group_id: {condition_group_id}")
    print(f"  Summary           : {grouped_summary[:120]}...")

    if not dry_run:
        col.insert_one(grouped_doc)
        print("  ✅ Inserted.")
        for r in individual_rules:
            col.update_one(
                {"rule_id": r["rule_id"]},
                {"$set": {"condition.condition_group_id": condition_group_id}}
            )
        print(f"  ✅ Back-filled condition_group_id on {len(individual_rules)} individual rules.")
    else:
        print("  [DRY RUN] Would insert + back-fill.")

    print(f"\n{'─' * 60}")
    if dry_run:
        print(f"[DRY RUN] Sloka {sloka}: {len(mis_tagged)} rule(s) would be retyped, 1 grouped rule would be inserted.")
    else:
        print(f"✅ Sloka {sloka} fix complete: {len(mis_tagged)} retyped, 1 grouped rule inserted ({new_rule_id})")


def main():
    parser = argparse.ArgumentParser(description="Fix mis-tagged dasha_grouped_outcome rules in Ch 56.")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--sloka",     default=None,
                        help="Single sloka to fix (e.g. '72-75'). Omit to fix all known slokas.")
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()

    target_slokas = [args.sloka] if args.sloka else DEFAULT_SLOKAS

    client = pymongo.MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"\nfix_ch56_sl7275.py  |  Batch: {BATCH_ID}  |  Mode: {mode}")
    print(f"Target slokas: {', '.join(target_slokas)}")

    for sloka in target_slokas:
        fix_sloka(col, sloka, args.dry_run)

    print(f"\n{'═' * 60}")
    print(f"Done. Review in Admin > Rules Browser → batch {BATCH_ID}")
    client.close()


if __name__ == "__main__":
    main()
