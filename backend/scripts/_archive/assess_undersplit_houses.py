#!/usr/bin/env python3
"""
assess_undersplit_houses.py

Scans BPHS house chapter rules (Ch 12-24) for merged-condition rules
that should be split into individually-queryable rules.

Detects two classes of merging:
  A. DIGNITY BUNDLES  -- "Sun in exaltation or own sign → X"
                        Should be 2 rules: Sun in exaltation; Sun in own sign
  B. PLACEMENT LISTS  -- "lord in 6th, 8th or 12th → X"
                        Should be 3 rules: lord in 6th; lord in 8th; lord in 12th
  C. PLANET BUNDLES   -- "Sun or Moon in 3rd house → X"
                        Should be 2 rules: Sun in 3rd; Moon in 3rd
  D. MULTI-CONDITION  -- condition text contains 2+ distinct if-clauses joined by
                        "and" / "also" / semicolons

Usage:
    # Assess only (no DB writes):
    python3 scripts/assess_undersplit_houses.py --mongo-url "$MONGO_URL"

    # Assess + tag candidates as pre_split_merged:
    python3 scripts/assess_undersplit_houses.py --mongo-url "$MONGO_URL" --tag

    # Show detailed rule text for each candidate:
    python3 scripts/assess_undersplit_houses.py --mongo-url "$MONGO_URL" --verbose
"""

import argparse
import re
import pymongo

# ── House chapter batch IDs ────────────────────────────────────────────────────
HOUSE_BATCHES = [
    "bphs-ch12-v2-20260414",
    "bphs-ch13-v2-20260414",
    "bphs-ch14-v2-20260414",
    "bphs-ch15-v2-20260414",
    "bphs-ch16-v2-20260414",
    "bphs-ch17-v2-20260414",
    "bphs-ch18-v2-20260414",
    "bphs-ch19-v2-20260415",
    "bphs-ch20-v2-20260415",
    "bphs-ch21-v2-20260415",
    "bphs-ch22-v2-20260415",
    "bphs-ch23-v2-20260415",
    "bphs-ch24-v2-20260416",   # lord-placement chapter
]

PLANETS = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}

# Dignity states that are frequently bundled together
DIGNITY_BUNDLE_RE = re.compile(
    r"(?:"
    r"exaltation\s+(?:or|and)\s+own\s+sign"
    r"|own\s+sign\s+(?:or|and)\s+exaltation"
    r"|exalted\s+(?:or|and)\s+own"
    r"|moolatrikona\s+(?:or|and)\s+"
    r"|debilitation\s+(?:or|and)\s+combust"
    r"|combust\s+(?:or|and)\s+debilitat"
    r"|(?:exalt|own|moola|debil|combust).{0,30}(?:or|and).{0,30}(?:exalt|own|moola|debil|combust)"
    r")",
    re.IGNORECASE,
)

# House-number lists: "6th, 8th or 12th" / "2nd or 7th" etc.
HOUSE_LIST_RE = re.compile(
    r"\b(?:\d+(?:st|nd|rd|th))\s*[,/]\s*(?:\d+(?:st|nd|rd|th))"
    r"|\b(?:\d+(?:st|nd|rd|th))\s+or\s+(?:\d+(?:st|nd|rd|th))",
    re.IGNORECASE,
)

# Yoga connectors -- planets joined by these words form a SIMULTANEOUS condition (one rule)
# Do NOT split: "Mercury in 3rd while Moon and Saturn conjunct" = one yoga
YOGA_CONNECTOR_RE = re.compile(
    r"\b(?:and|while|with|conjunct|conjunction|along\s+with|together\s+with"
    r"|associated\s+with|joined\s+by|aspected\s+by|join(?:s|ing)?|in\s+aspect)\b",
    re.IGNORECASE,
)

# Alternative connectors -- planets joined by these are genuinely alternative conditions
# SHOULD split: "Venus or Mercury in 2nd" = 2 rules
ALTERNATIVE_PLANET_RE = re.compile(
    r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)"
    r"\s+or\s+"
    r"(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b",
    re.IGNORECASE,
)


def extract_condition(summary: str) -> str:
    """Return the condition part (before ' → ') from a rule summary."""
    if " → " in summary:
        return summary.split(" → ", 1)[0]
    return summary


def is_yoga_condition(condition: str) -> bool:
    """
    Return True if the condition describes a multi-planet yoga (simultaneous
    planetary positions). Yogas must NOT be split -- the whole combination IS
    the condition.
    """
    planet_count = sum(
        1 for p in PLANETS
        if re.search(r"\b" + p + r"\b", condition, re.IGNORECASE)
    )
    if planet_count < 2:
        return False
    # If planets are connected by yoga words, it's a simultaneous condition
    return bool(YOGA_CONNECTOR_RE.search(condition))


def is_undersplit(rule: dict) -> tuple[bool, str]:
    """
    Returns (True, reason) if the rule looks like a merged-condition rule
    that should be split into individually-queryable rules.
    (False, '') otherwise.

    Split candidates:
      A. dignity_bundle -- "exaltation or own sign" → 2 rules
      B. house_list     -- "6th, 8th or 12th" → 3 rules
      C. planet_or      -- "Venus or Mercury in 2nd" (alternative planets, same outcome) → 2 rules

    NOT split candidates (even if multiple planets present):
      - Yoga conditions: "Mercury in 3rd while Moon and Saturn conjunct" = 1 yoga rule
      - Compound yogas: "Rahu in 6th and Saturn in 8th from Rahu" = 1 rule
    """
    summary   = rule.get("interpretation", {}).get("summary", "")
    condition = extract_condition(summary)

    # Skip birth_special -- these are always unique combination rules
    sub_type = rule.get("condition", {}).get("sub_type", "")
    if sub_type == "birth_special":
        return False, ""

    # --- Class A: dignity bundle -- "own sign or exaltation" ---
    if DIGNITY_BUNDLE_RE.search(condition):
        return True, "dignity_bundle"

    # --- Class B: house-number list -- "6th, 8th or 12th" ---
    if HOUSE_LIST_RE.search(condition):
        return True, "house_list"

    # --- Class C: alternative planets -- "Venus or Mercury" ---
    # Only flag if it's NOT a yoga (simultaneous) condition
    if ALTERNATIVE_PLANET_RE.search(condition) and not is_yoga_condition(condition):
        return True, "planet_or"

    return False, ""


def main():
    parser = argparse.ArgumentParser(description="Assess undersplit rules in BPHS house chapters.")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--tag",       action="store_true",
                        help="Tag candidates as metadata.source_note='pre_split_merged'")
    parser.add_argument("--verbose",   action="store_true",
                        help="Print rule text for each candidate")
    parser.add_argument("--batch",     default=None,
                        help="Limit to a single batch ID (e.g. bphs-ch12-v2-20260414)")
    args = parser.parse_args()

    client = pymongo.MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    batches = [args.batch] if args.batch else HOUSE_BATCHES

    print(f"\nassess_undersplit_houses.py  |  DB: {args.db_name}  |  Tag: {args.tag}")
    print(f"{'─' * 70}")

    grand_total     = 0
    grand_candidates = 0
    tag_ids         = []

    for batch_id in batches:
        rules = list(col.find(
            {"source.batch_id": batch_id,
             "approval_status": {"$ne": "deprecated"}},
            {"rule_id": 1, "condition": 1, "interpretation": 1, "source": 1}
        ))
        if not rules:
            continue

        candidates = []
        for r in rules:
            flagged, reason = is_undersplit(r)
            if flagged:
                candidates.append((r, reason))

        ch = batch_id.split("-")[1].upper() if "-" in batch_id else batch_id
        pct = 100 * len(candidates) / len(rules) if rules else 0
        print(f"\n{batch_id}")
        print(f"  Total rules : {len(rules):3d}  |  Candidates: {len(candidates):3d}  ({pct:.0f}%)")

        # Breakdown by reason
        reasons: dict[str, int] = {}
        for _, reason in candidates:
            reasons[reason] = reasons.get(reason, 0) + 1
        for reason, cnt in sorted(reasons.items(), key=lambda x: -x[1]):
            print(f"    {reason:20s}: {cnt}")

        if args.verbose:
            for r, reason in candidates:
                summary = r.get("interpretation", {}).get("summary", "")
                print(f"    [{reason:14s}] {r['rule_id']:20s} | {summary[:110]}")

        grand_total      += len(rules)
        grand_candidates += len(candidates)
        tag_ids.extend([r["rule_id"] for r, _ in candidates])

    print(f"\n{'═' * 70}")
    pct_total = 100 * grand_candidates / grand_total if grand_total else 0
    print(f"GRAND TOTAL  |  {grand_total} rules  |  {grand_candidates} candidates  ({pct_total:.0f}%)")
    print(f"{'═' * 70}")

    # ── Optional tagging ───────────────────────────────────────────────────────
    if args.tag and tag_ids:
        print(f"\nTagging {len(tag_ids)} rules as pre_split_merged...")
        result = col.update_many(
            {"rule_id": {"$in": tag_ids},
             "metadata.source_note": {"$ne": "pre_split_merged"}},
            {"$set": {"metadata.source_note": "pre_split_merged"}},
        )
        print(f"✅ Tagged {result.modified_count} rules.")

        # Verify
        verify = col.count_documents({
            "source.batch_id": {"$in": batches},
            "metadata.source_note": "pre_split_merged",
        })
        print(f"   Total pre_split_merged in house batches: {verify}")
    elif args.tag and not tag_ids:
        print("\n✅ No candidates to tag.")

    client.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
