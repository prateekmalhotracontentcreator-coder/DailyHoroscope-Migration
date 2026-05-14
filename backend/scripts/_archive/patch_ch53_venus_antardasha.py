#!/usr/bin/env python3
"""
Patch batch: Venus Antardasha in Moon Mahadasha — missing slokas 53, 54, 55.

Background
----------
Slokas 53, 54, 55 of BPHS Vol 2 Ch 53 are genuinely absent from the
RS Santhanam edition used for RTF conversion (confirmed by source inspection).
The missing slokas cover: unfavourable conditions for Venus Antardasha in Moon
Mahadasha + one remedy sloka.

Source material confirms:
- Unnumbered para (ingested): favourable Venus in kendra/trikona/11th/exaltation
- Sloka 56 (ingested): favourable Venus with Moon
- Slokas 53-55 (MISSING): unfavourable conditions + remedy

This script inserts 4 rules (3 unfavourable + 1 remedy) constructed via
BPHS cross-chapter interpolation, consistent with Ch 52, 56, 57 Antardasha
patterns for planetary affliction and remedy slokas.

Usage
-----
python3 backend/scripts/patch_ch53_venus_antardasha.py \
    --mongo-url "$MONGO_URL" --db-name EverydayHoroscope

Run from: ~/DailyHoroscope-Migration  (main repo root)
"""

import argparse
import sys
from datetime import datetime, timezone

from pymongo import MongoClient

BATCH_ID    = "bphs-ch53-venus-patch-20260417"
CHAPTER     = 53
DASHA_LORD  = "Moon"
BOOK        = "Brihat Parashara Hora Shastra"
BOOK_ID     = "bphs_vol2"
SCIENCE     = "vedic_astrology"
CHAPTER_NAME = "Antardasha in Moon Mahadasha"

# ── 4 rules for missing slokas 53-55 ──────────────────────────────────────────
# Constructed via BPHS cross-chapter interpolation (Ch 52/56/57 parallel pattern).
# source.edition = "codex_supplement" clearly flags these as supplemented.
# Rule IDs use "53P" prefix to avoid collision with ingested R-BPHS53-xxx IDs.

RULES_DATA = [
    {
        "rule_id":        "R-BPHS53P-001",
        "sloka_ref":      "53-54",   # reconstructed — covers what slokas 53-54 would contain
        "sub_type":       "dasha_unfavourable",
        "condition_summary": "Venus Antardasha in Moon Mahadasha — Venus debilitated, combust, or in enemy sign",
        "result_summary":    "Loss of wealth, mental distress, physical ailments, strained relationships.",
        "full_condition": (
            "In the Antardasha of Venus in the Mahadasha of Moon, "
            "if Venus be in its sign of debilitation (Virgo), or in an inimical sign, "
            "or combust by the Sun."
        ),
        "full_result": (
            "There will be loss of wealth and cattle, mental anxieties, "
            "physical ailments, enmity with kinsmen, distress to wife and children, "
            "and obstacles in travels and undertakings."
        ),
        "planets": ["Moon", "Venus", "Sun"],
        "houses":  [],
        "tags":    [
            "verbatim", "dasha_planet", "chapter53",
            "dasha_moon", "dasha_unfavourable",
            "codex_supplement", "antardasha_venus",
        ],
    },
    {
        "rule_id":        "R-BPHS53P-002",
        "sloka_ref":      "54-55",   # reconstructed
        "sub_type":       "dasha_unfavourable",
        "condition_summary": "Venus Antardasha in Moon Mahadasha — Venus in 6th, 8th or 12th house",
        "result_summary":    "Unnecessary expenditures, humiliation, disharmony in marital life.",
        "full_condition": (
            "In the Antardasha of Venus in the Mahadasha of Moon, "
            "if Venus be placed in the 6th, 8th, or 12th house from the Ascendant."
        ),
        "full_result": (
            "There will be unnecessary expenditures, loss of luxuries and comforts, "
            "humiliation, setbacks in creative and artistic pursuits, "
            "disharmony in marital relations, and ill health to spouse or partner."
        ),
        "planets": ["Moon", "Venus"],
        "houses":  [6, 8, 12],
        "tags":    [
            "verbatim", "dasha_planet", "chapter53",
            "dasha_moon", "dasha_unfavourable",
            "codex_supplement", "antardasha_venus",
        ],
    },
    {
        "rule_id":        "R-BPHS53P-003",
        "sloka_ref":      "55",   # reconstructed
        "sub_type":       "dasha_unfavourable",
        "condition_summary": "Venus Antardasha in Moon Mahadasha — Venus afflicted by malefics",
        "result_summary":    "Sorrow through spouse, separation, loss of pleasures, obstacles.",
        "full_condition": (
            "In the Antardasha of Venus in the Mahadasha of Moon, "
            "if Venus be conjunct or aspected by Saturn, Mars, Rahu, or Ketu."
        ),
        "full_result": (
            "There will be sorrow through wife or partner, separation from loved ones, "
            "loss of sensual pleasures and ornaments, conflicts in relationships, "
            "obstacles in business, and mental disquiet."
        ),
        "planets": ["Moon", "Venus", "Saturn", "Mars", "Rahu", "Ketu"],
        "houses":  [],
        "tags":    [
            "verbatim", "dasha_planet", "chapter53",
            "dasha_moon", "dasha_unfavourable",
            "codex_supplement", "antardasha_venus",
        ],
    },
    {
        "rule_id":        "R-BPHS53P-004",
        "sloka_ref":      "55-remedy",   # reconstructed remedy sloka
        "sub_type":       "dasha_remedy",
        "condition_summary": "Venus Antardasha in Moon Mahadasha — remedy for afflicted Venus",
        "result_summary":    "Propitiate Venus and Moon to mitigate adverse effects.",
        "full_condition": (
            "In the Antardasha of Venus in the Mahadasha of Moon, "
            "when Venus is afflicted (debilitated, combust, in dusthana, or conjunct malefics)."
        ),
        "full_result": (
            "The evil effects may be mitigated by propitiating Venus: "
            "observe Friday fasts, offer white flowers to Goddess Lakshmi, "
            "donate white cloth or curd to women, and recite 'Om Shukraya Namaha' 108 times daily. "
            "Worship of the Moon by offering milk on Mondays also helps pacify the period."
        ),
        "planets": ["Moon", "Venus"],
        "houses":  [],
        "tags":    [
            "verbatim", "dasha_planet", "chapter53",
            "dasha_moon", "dasha_remedy",
            "codex_supplement", "antardasha_venus", "remedy",
        ],
    },
]


def build_rule(data: dict, now_iso: str) -> dict:
    planets   = data["planets"]
    houses    = data["houses"]
    sub_type  = data["sub_type"]
    sloka_ref = data["sloka_ref"]

    summary  = f"{data['condition_summary']} → {data['result_summary']}"
    if len(summary) > 200:
        summary = summary[:197] + "..."

    detailed = (
        f"Condition: {data['full_condition'].rstrip('.')}.  \n\n"
        f"Effect: {data['full_result'].rstrip('.')}."
    )

    return {
        "rule_id":    data["rule_id"],
        "science_id": SCIENCE,
        "source": {
            "book":           BOOK,
            "book_id":        BOOK_ID,
            "chapter":        str(CHAPTER),
            "chapter_name":   CHAPTER_NAME,
            "sloka":          sloka_ref,
            "batch_id":       BATCH_ID,
            "primary":        BOOK,
            "page_ref":       None,
            "passage_ref_id": None,
            "edition":        "codex_supplement",
            "supplement_note": (
                "Slokas 53-55 are absent from the RS Santhanam Vol 2 edition used for "
                "RTF conversion. These rules reconstruct the Venus Antardasha unfavourable "
                "and remedy content via BPHS cross-chapter interpolation (Ch 52/56/57 pattern). "
                "Flagged for expert review before promotion to approved."
            ),
        },
        "condition": {
            "type":             "dasha_planet",
            "dasha_lord":       DASHA_LORD,
            "antardasha_lord":  "Venus",
            "sub_type":         sub_type,
            "sloka":            sloka_ref,
            "planets_involved": planets,
            "houses_involved":  houses,
            "sub_conditions":   [],
            "operator":         "and",
        },
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "MEDIUM"}],
            "remedies":           [],
            "life_domain":        "general",
            "tags":               data["tags"],
        },
        "metadata": {
            "planets_involved": planets,
            "houses_involved":  houses,
            "signs_involved":   [],
            "condition_count":  1,
        },
        "confidence": {
            "base":                  0.65,   # lower than 0.85 — supplement, not verbatim text
            "source_weight":         0.70,
            "cross_book_multiplier": 1.0,
        },
        "approval_status": "pending_human_review",   # supplement → human review required
        "created_at":      now_iso,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Insert Ch 53 Venus Antardasha patch rules (missing slokas 53-55)"
    )
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   required=True)
    parser.add_argument("--dry-run",   action="store_true",
                        help="Print rules without inserting")
    args = parser.parse_args()

    now_iso = datetime.now(timezone.utc).isoformat()
    rules   = [build_rule(d, now_iso) for d in RULES_DATA]

    if args.dry_run:
        import json
        print(f"\n{'='*70}")
        print(f"DRY RUN — {len(rules)} rules would be inserted")
        print(f"Batch ID : {BATCH_ID}")
        print(f"{'='*70}")
        for r in rules:
            print(f"\n  {r['rule_id']}  [{r['condition']['sub_type']}]  sloka {r['source']['sloka']}")
            print(f"  {r['interpretation']['summary'][:100]}")
        print(f"\n{'='*70}")
        return

    client = MongoClient(args.mongo_url)
    db     = client[args.db_name]
    col    = db["interpretation_rules"]

    # Safety: check for existing patch rules to avoid duplicates
    existing_ids = [d["rule_id"] for d in RULES_DATA]
    already = list(col.find({"rule_id": {"$in": existing_ids}}, {"rule_id": 1}))
    if already:
        print(f"\n⚠️  {len(already)} rule(s) already exist in DB with these IDs:")
        for r in already:
            print(f"   {r['rule_id']}")
        print("\nAbort — remove existing rules first or rerun with --dry-run to inspect.")
        sys.exit(1)

    result = col.insert_many(rules)
    print(f"\n✅  Inserted {len(result.inserted_ids)} Venus Antardasha patch rules")
    print(f"   Batch ID        : {BATCH_ID}")
    print(f"   approval_status : pending_human_review (supplement — expert review required)")
    print(f"   IDs             : {', '.join(existing_ids)}")
    print(f"\n   Note: confidence.base = 0.65 (codex_supplement, not verbatim source)")
    print(f"   These rules will appear in Admin > Rules Browser > filter by batch_id")
    print(f"   Promote to approved only after expert Vedic review confirms correctness.\n")


if __name__ == "__main__":
    main()
