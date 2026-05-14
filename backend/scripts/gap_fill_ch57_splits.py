#!/usr/bin/env python3
"""
gap_fill_ch57_splits.py  --  Direct insert for 7 gap-fill rules in Ch 57.

WHY DIRECT INSERT (not patch_slokas.py):
  Slokas 14-15, 22-23, 35-36 each have a merged "2nd or 7th" original rule.
  patch_slokas.py dedup (60% word-overlap) blocked the two individual splits
  because they share too much text with the merged original. The rules are
  factually correct and needed -- they are inserted here directly, bypassing
  the dedup layer that was the only obstacle.

  Sloka 65-67 is included here too: the middle-portion timing rule is fully
  distinct from all 11 existing rules (no overlap on "middle portion" / timing
  language) but including it here avoids an extra patch_slokas.py re-extraction
  that would redundantly dedup 10 already-present rules.

Rules inserted (7 total):
  14-15  Mercury as 2nd lord → Physical distress     (dasha_unfavourable)
  14-15  Mercury as 7th lord → Physical distress     (dasha_unfavourable)
  22-23  Ketu in 2nd house   → Physical distress     (dasha_unfavourable)
  22-23  Ketu in 7th house   → Physical distress     (dasha_unfavourable)
  35-36  Venus as 2nd lord   → Physical distress     (dasha_unfavourable)
  35-36  Venus as 7th lord   → Physical distress     (dasha_unfavourable)
  65-67  Rahu middle-portion → Cordial relations...    (dasha_favourable)

Split-source rule IDs (the merged originals these replace):
  14-15 → R-BPHS57-020   "Mercury is the Lord of the 2nd or 7th house..."
  22-23 → R-BPHS57-036   "Ketu in the 2nd or 7th from the Ascendant..."
  35-36 → R-BPHS57-060   "Venus is Lord of the 2nd or 7th from Ascendant..."
  65-67 → (absent -- never extracted)

Usage:
  cd /Users/apple/DailyHoroscope-Migration/backend
  python3 scripts/gap_fill_ch57_splits.py --mongo-url "$MONGO_URL" --dry-run
  python3 scripts/gap_fill_ch57_splits.py --mongo-url "$MONGO_URL"
"""

import argparse
import hashlib
from datetime import datetime, timezone

import pymongo


BATCH_ID   = "bphs-ch57-dasha-20260419"
CHAPTER    = 57
DASHA_LORD = "Saturn"
BOOK       = "BPHS"
VOLUME     = 2


def make_rule_id(sloka: str, suffix_seed: str) -> str:
    """Generate a deterministic PATCH rule ID from sloka + seed text."""
    h = hashlib.md5(f"ch57-{sloka}-{suffix_seed}".encode()).hexdigest()[:6].upper()
    return f"R-BPHS57-PATCH-{h}-GF"


# ── Rule definitions ──────────────────────────────────────────────────────────
# Each dict becomes one MongoDB document.  Fields follow the schema used by
# ingest_bphs_dasha_v1.py / patch_slokas.py.

GAP_RULES = [
    # ── Sloka 14-15 ── Mercury as 2nd / 7th lord ─────────────────────────────
    {
        "sloka":              "14-15",
        "sub_type":           "dasha_unfavourable",
        "antardasha_planet":  "Mercury",
        "house":              2,
        "dignity_state":      "general",
        "strength_band":      "medium",
        "full_condition":     "Mercury is Lord of the 2nd house from Ascendant during Saturn Mahadasha",
        "summary":            "Mercury is Lord of the 2nd house from Ascendant during Saturn Mahadasha → Physical distress occurs.",
        "outcome":            "Physical distress occurs.",
        "split_source_id":    "R-BPHS57-020",
    },
    {
        "sloka":              "14-15",
        "sub_type":           "dasha_unfavourable",
        "antardasha_planet":  "Mercury",
        "house":              7,
        "dignity_state":      "general",
        "strength_band":      "medium",
        "full_condition":     "Mercury is Lord of the 7th house from Ascendant during Saturn Mahadasha",
        "summary":            "Mercury is Lord of the 7th house from Ascendant during Saturn Mahadasha → Physical distress occurs.",
        "outcome":            "Physical distress occurs.",
        "split_source_id":    "R-BPHS57-020",
    },

    # ── Sloka 22-23 ── Ketu in 2nd / 7th house ───────────────────────────────
    {
        "sloka":              "22-23",
        "sub_type":           "dasha_unfavourable",
        "antardasha_planet":  "Ketu",
        "house":              2,
        "dignity_state":      "general",
        "strength_band":      "medium",
        "full_condition":     "Ketu in the 2nd house from Ascendant during Saturn Mahadasha",
        "summary":            "Ketu in the 2nd house from Ascendant during Saturn Mahadasha → Physical distress.",
        "outcome":            "Physical distress.",
        "split_source_id":    "R-BPHS57-036",
    },
    {
        "sloka":              "22-23",
        "sub_type":           "dasha_unfavourable",
        "antardasha_planet":  "Ketu",
        "house":              7,
        "dignity_state":      "general",
        "strength_band":      "medium",
        "full_condition":     "Ketu in the 7th house from Ascendant during Saturn Mahadasha",
        "summary":            "Ketu in the 7th house from Ascendant during Saturn Mahadasha → Physical distress.",
        "outcome":            "Physical distress.",
        "split_source_id":    "R-BPHS57-036",
    },

    # ── Sloka 35-36 ── Venus as 2nd / 7th lord ───────────────────────────────
    {
        "sloka":              "35-36",
        "sub_type":           "dasha_unfavourable",
        "antardasha_planet":  "Venus",
        "house":              2,
        "dignity_state":      "general",
        "strength_band":      "medium",
        "full_condition":     "Venus is Lord of the 2nd house from Ascendant during Saturn Mahadasha",
        "summary":            "Venus is Lord of the 2nd house from Ascendant during Saturn Mahadasha → Physical distress occurs.",
        "outcome":            "Physical distress occurs.",
        "split_source_id":    "R-BPHS57-060",
    },
    {
        "sloka":              "35-36",
        "sub_type":           "dasha_unfavourable",
        "antardasha_planet":  "Venus",
        "house":              7,
        "dignity_state":      "general",
        "strength_band":      "medium",
        "full_condition":     "Venus is Lord of the 7th house from Ascendant during Saturn Mahadasha",
        "summary":            "Venus is Lord of the 7th house from Ascendant during Saturn Mahadasha → Physical distress occurs.",
        "outcome":            "Physical distress occurs.",
        "split_source_id":    "R-BPHS57-060",
    },

    # ── Sloka 65-67 ── Rahu middle-portion timing rule ───────────────────────
    # Dry run proposed R-BPHS57-PATCH-A60D7A but live dedup blocked it.
    # Verified absent from all 11 existing sloka 65-67 rules.
    {
        "sloka":              "65-67",
        "sub_type":           "dasha_favourable",
        "antardasha_planet":  "Rahu",
        "house":              None,
        "dignity_state":      "general",
        "strength_band":      "medium",
        "full_condition":     "Rahu in favourable condition during middle portion of Rahu Antardasha in Saturn Mahadasha",
        "summary":            "Rahu in favourable condition during middle portion of Rahu Antardasha in Saturn Mahadasha → Cordial relations with government officials, increase in trade and other auspicious activities.",
        "outcome":            "Cordial relations with government officials, increase in trade and other auspicious activities.",
        "split_source_id":    None,
    },
]


def build_doc(rule: dict, now: datetime) -> dict:
    rule_id = make_rule_id(rule["sloka"], rule["full_condition"])

    doc = {
        "rule_id":   rule_id,
        "sub_type":  rule["sub_type"],
        "source": {
            "book":     BOOK,
            "volume":   VOLUME,
            "chapter":  CHAPTER,
            "sloka":    rule["sloka"],
            "batch_id": BATCH_ID,
        },
        "condition": {
            "dasha_lord":               DASHA_LORD,
            "antardasha_planet":        rule["antardasha_planet"],
            "antardasha_planet_method": "gap_fill_direct",
            "full_condition":           rule["full_condition"],
            "dignity_state":            rule["dignity_state"],
            "strength_band":            rule["strength_band"],
            "is_group_summary":         False,
            "condition_group_id":       "",
        },
        "interpretation": {
            "summary":   rule["summary"],
            "outcome":   rule["outcome"],
            "full_text": rule["summary"],
        },
        "planets_involved": [rule["antardasha_planet"]],
        "metadata": {
            "source_note":    "gap_fill",
            "split_source_id": rule["split_source_id"],
            "inserted_at":    now.isoformat(),
            "inserted_by":    "gap_fill_ch57_splits.py",
        },
        "approval_status": "pending_review",
        "tags":            ["gap_fill", f"ch57-sl{rule['sloka']}"],
    }

    if rule["house"] is not None:
        doc["condition"]["house"] = rule["house"]

    return doc


def already_exists(col, sloka: str, full_condition: str) -> bool:
    """Return True if a rule with this exact full_condition already exists for this sloka."""
    return col.count_documents({
        "source.batch_id":          BATCH_ID,
        "source.sloka":             sloka,
        "condition.full_condition": full_condition,
    }) > 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()

    mode = "DRY RUN" if args.dry_run else "LIVE"
    client = pymongo.MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc)

    print(f"\ngap_fill_ch57_splits.py  |  Batch: {BATCH_ID}  |  Mode: {mode}")
    print(f"Inserting 7 gap-fill rules across slokas 14-15, 22-23, 35-36, 65-67\n")
    print("─" * 68)

    inserted = 0
    skipped  = 0

    for rule in GAP_RULES:
        sloka   = rule["sloka"]
        summary = rule["summary"]
        rule_id = make_rule_id(sloka, rule["full_condition"])

        # Skip if exact full_condition already present (idempotent)
        if already_exists(col, sloka, rule["full_condition"]):
            print(f"  SKIP (already exists)  sl {sloka}: {summary[:70]}...")
            skipped += 1
            continue

        doc = build_doc(rule, now)

        if args.dry_run:
            src = rule.get("split_source_id") or "new rule"
            print(f"  [DRY RUN] Would insert  {rule_id}")
            print(f"    sl {sloka} | {rule['sub_type']} | AD: {rule['antardasha_planet']}")
            print(f"    {summary[:90]}")
            print(f"    split_source: {src}")
        else:
            col.insert_one(doc)
            print(f"  ✅ Inserted  {rule_id}")
            print(f"    sl {sloka} | {rule['sub_type']} | AD: {rule['antardasha_planet']}")
            print(f"    {summary[:90]}")

        inserted += 1
        print()

    print("─" * 68)
    if args.dry_run:
        print(f"[DRY RUN] Would insert {inserted} rules  |  {skipped} already exist\n")
    else:
        print(f"✅ Inserted {inserted} rules  |  {skipped} already existed\n")
        print(f"Review: Admin > Library > Rules Browser → batch {BATCH_ID}")
        print(f"        Filter: source_note = gap_fill\n")


if __name__ == "__main__":
    main()
