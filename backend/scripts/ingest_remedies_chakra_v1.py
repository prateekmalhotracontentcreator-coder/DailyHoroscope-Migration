#!/usr/bin/env python3
"""
ingest_remedies_chakra_v1.py -- 7 Chakra Healing Remedies (IDs 301-307)

7 rules, science_id = "jyotish_remedies_chakra"
Collection: horoscope_db.interpretation_rules

Schema fields per source record:
  id, chakra, primary_crystal, bija_mantra, planet, tattva,
  trigger_condition, process

CHS Trigger Formula:
  Chakra Health Score (CHS) = (Shadbala + Bhava Bala + Tattva) / 3
  Blocked   = CHS < 50%
  Imbalanced = CHS 50-79%
  Optimal   = CHS >= 80%
  KE fires this remedy when CHS < 50% (blocked state)

Standard workflow:
  python3 scripts/ingest_remedies_chakra_v1.py --dry-run --save scripts/chakra_rules.json
  python3 scripts/ingest_remedies_chakra_v1.py --upload scripts/chakra_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

Source:
  /Users/apple/Documents/Knowledge Engine_eBooks/
  Remedies + The Strategist/5. 7 Chakra Healing_JSON _ Brief Docs.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE_ID  = "jyotish_remedies_chakra"
BOOK        = "7 Chakra Healing Remedy Library"
BOOK_ID     = "remedies_chakra_v1"
CHAP_NAME   = "7 Chakra Healing Remedies"
BATCH_ID    = f"remedies-chakra-v1-{datetime.now().strftime('%Y%m%d')}"

SOURCE_MD = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/5. 7 Chakra Healing_JSON _ Brief Docs.md"
)

EXPECTED_IDS = set(range(301, 308))   # 301-307  (7 records)

# CHS threshold constants (documented in source brief)
CHS_BLOCKED    = 50    # CHS < 50%  → Blocked   → remedy fires
CHS_IMBALANCED = 80    # CHS 50-79% → Imbalanced
# CHS >= 80%          → Optimal   → no intervention needed

# Planet → chakra mapping
CHAKRA_TRIGGER_MAP: dict[int, dict] = {
    301: {"chakra": "Root (Muladhara)",       "planet": ["Saturn", "Mars"],
          "tags": ["root_chakra_blocked", "saturn_afflicted", "mars_weak"]},
    302: {"chakra": "Sacral (Svadhisthana)",   "planet": ["Moon", "Venus"],
          "tags": ["sacral_chakra_blocked", "moon_afflicted", "venus_weak"]},
    303: {"chakra": "Solar Plexus (Manipura)", "planet": ["Sun", "Mars"],
          "tags": ["solar_plexus_blocked", "sun_weak", "low_shadbala_sun"]},
    304: {"chakra": "Heart (Anahata)",         "planet": ["Venus", "Moon"],
          "tags": ["heart_chakra_blocked", "venus_afflicted"]},
    305: {"chakra": "Throat (Vishuddha)",      "planet": ["Mercury"],
          "tags": ["throat_chakra_blocked", "mercury_combust", "mercury_weak"]},
    306: {"chakra": "Third Eye (Ajna)",        "planet": ["Jupiter", "Ketu"],
          "tags": ["third_eye_blocked", "jupiter_weak", "ketu_afflicted"]},
    307: {"chakra": "Crown (Sahasrara)",       "planet": ["Ketu", "Jupiter"],
          "tags": ["crown_chakra_blocked", "ketu_1st_12th", "jupiter_debilitated"]},
}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE PARSER
# ─────────────────────────────────────────────────────────────────────────────

def _unescape_md(text: str) -> str:
    """Remove markdown bold/italic formatting and fix invalid JSON escapes.

    The Chakra source file wraps every JSON element in **bold** markers
    and uses \< for less-than signs -- both must be cleaned before parsing.
    """
    text = re.sub(r'\*+', '', text)
    text = (text
            .replace('\\[', '[').replace('\\]', ']')
            .replace('\\_', '_').replace('\\{', '{').replace('\\}', '}'))
    # Remove invalid JSON escapes (\< \> etc.)
    text = re.sub(r'\\(?!["\\/bfnrtu])', '', text)
    return text


def _load_source() -> list[dict]:
    """Robust object-by-object scan. Handles bold-formatted Chakra source file."""
    raw = SOURCE_MD.read_text(encoding='utf-8', errors='replace')
    raw = _unescape_md(raw)

    entries: dict[int, dict] = {}
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(raw):
        obj_start = raw.find('{', pos)
        if obj_start == -1:
            break
        try:
            obj, end = decoder.raw_decode(raw, obj_start)
            if isinstance(obj, dict) and 'id' in obj:
                rid = obj['id']
                if isinstance(rid, (int, float)) and float(rid) == int(float(rid)):
                    entries[int(float(rid))] = obj
            pos = end
        except (json.JSONDecodeError, ValueError):
            pos = obj_start + 1

    result = list(entries.values())
    result.sort(key=lambda x: x['id'])
    return result


# ─────────────────────────────────────────────────────────────────────────────
# BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def _build_rules() -> list[dict]:
    entries = _load_source()
    now     = datetime.now(timezone.utc).isoformat()
    rules: list[dict] = []

    for entry in entries:
        rid     = entry['id']
        trig    = CHAKRA_TRIGGER_MAP.get(rid, {
            "chakra": entry.get('chakra', ''),
            "planet": [],
            "tags":   ["chakra_healing"],
        })

        chakra     = entry.get('chakra', trig.get('chakra', ''))
        crystal    = entry.get('primary_crystal', '')
        bija       = entry.get('bija_mantra', '')
        planet     = entry.get('planet', ', '.join(trig['planet']))
        tattva     = entry.get('tattva', '')
        trigger_c  = entry.get('trigger_condition', '')
        process    = entry.get('process', '')

        # CHS trigger description
        chs_trigger = (
            f"KE fires when Chakra Health Score (CHS) < {CHS_BLOCKED}% (Blocked state). "
            f"CHS = (Shadbala + Bhava Bala + Tattva) / 3. "
            f"Planet(s): {planet}. "
            f"Condition: {trigger_c}"
        )

        detailed = (
            f"Chakra: {chakra}\n"
            f"Primary Crystal: {crystal}\n"
            f"Bija Mantra: {bija}\n"
            f"Associated Planet: {planet}\n"
            f"Tattva Element: {tattva}\n\n"
            f"CHS Trigger: CHS < {CHS_BLOCKED}% → Blocked\n"
            f"Trigger Condition: {trigger_c}\n\n"
            f"Healing Process:\n{process}"
        )

        rule: dict = {
            "rule_id":    f"chakra-{rid:03d}",
            "science_id": SCIENCE_ID,
            "source": {
                "book":           BOOK,
                "book_id":        BOOK_ID,
                "chapter":        None,
                "chapter_name":   CHAP_NAME,
                "sloka":          None,
                "batch_id":       BATCH_ID,
                "primary":        BOOK,
                "page_ref":       None,
                "passage_ref_id": None,
            },
            "condition": {
                "type":              "remedy_trigger",
                "sub_type":          "chakra_imbalance",
                "yoga_name":         chakra,
                "yoga_group":        "chakra_imbalance",
                "yoga_group_label":  "Chakra Imbalance",
                "planets_involved":  trig['planet'],
                "houses_involved":   [],
                "yoga_check": {
                    "type":         "chs_evaluation",
                    "checkable":    False,
                    "chs_threshold": CHS_BLOCKED,
                    "chs_formula":  "( Shadbala + Bhava_Bala + Tattva ) / 3",
                },
                "trigger_condition":    chs_trigger,
                "astrological_mapping": {"planet": trig['planet']},
                "trigger_tags":         trig['tags'],
            },
            "interpretation": {
                "summary":  f"{chakra} -- {crystal}",
                "detailed": detailed,
                "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
                "remedy":           [],
                "timing_indicator": False,
                "strength_modifier": None,
            },
            "remedy": {
                "id":               rid,
                "chakra":           chakra,
                "primary_crystal":  crystal,
                "bija_mantra":      bija,
                "planet":           planet,
                "tattva":           tattva,
                "trigger_condition": trigger_c,
                "process":          process,
                "chs_threshold":    CHS_BLOCKED,
                "chs_formula":      "( Shadbala + Bhava_Bala + Tattva ) / 3",
            },
            "metadata": {
                "phase":            2,
                "checkable":        False,
                "yoga_group":       "chakra_imbalance",
                "yoga_group_label": "Chakra Imbalance",
                "remedy_category":  ["chakra", "crystal", "healing"],
                "source_quality":   "PRIMARY",
                "data_quality":     "source",
                "tags":             ["remedy", "chakra", "crystal", chakra.lower().split()[0], planet.lower()[:20]],
                "trigger_category": "chakra_imbalance",
            },
            "confidence":      "HIGH",
            "approval_status": "pending_review",
            "validation": {
                "verdict":      "pending",
                "flag_reason":  None,
                "validated_by": None,
                "validated_at": None,
            },
            "created_at": now,
            "updated_at": now,
        }
        rules.append(rule)

    return rules


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest 7 Chakra Healing Remedies into MongoDB"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--save",    metavar="FILE")
    parser.add_argument("--upload",  metavar="FILE")
    parser.add_argument("--mongo-url", default="")
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    if not args.dry_run and not args.upload:
        parser.print_help()
        sys.exit(1)

    if args.dry_run:
        rules = _build_rules()
        found_ids = {r["remedy"]["id"] for r in rules}
        missing   = sorted(EXPECTED_IDS - found_ids)
        extra     = sorted(found_ids - EXPECTED_IDS)

        print(f"\n{'='*60}")
        print(f"  7 Chakra Healing Remedies -- Dry Run")
        print(f"  Total rules built: {len(rules)}")
        print(f"  Batch ID:          {BATCH_ID}")
        print(f"  Science ID:        {SCIENCE_ID}")
        print(f"  Expected IDs:      301-307 (7 records)")
        print(f"{'='*60}")
        print("\n  Chakra coverage:")
        for r in rules:
            print(f"    ID {r['remedy']['id']:3d}  {r['remedy']['chakra']:<30}  {r['remedy']['primary_crystal']}")
        if missing:
            print(f"\n  ⚠️  Missing IDs: {missing}")
        else:
            print(f"\n  ✅ All 7 chakra IDs present (301-307)")
        if extra:
            print(f"\n  ⚠️  Unexpected IDs: {extra}")
        print()

        if args.save:
            out = Path(args.save)
            out.write_text(json.dumps(rules, indent=2, ensure_ascii=False))
            print(f"  ✅ Saved {len(rules)} rules → {out}\n")
        return

    if args.upload:
        src = Path(args.upload)
        if not src.exists():
            print(f"ERROR: {src} not found -- run --dry-run --save first")
            sys.exit(1)
        rules = json.loads(src.read_text())
        try:
            from pymongo import MongoClient, UpdateOne
        except ImportError:
            print("ERROR: pymongo not installed")
            sys.exit(1)
        if not args.mongo_url:
            print("ERROR: --mongo-url required")
            sys.exit(1)
        client = MongoClient(args.mongo_url)
        col    = client[args.db_name]["interpretation_rules"]
        ops    = [
            UpdateOne({"rule_id": r["rule_id"]}, {"$set": r}, upsert=True)
            for r in rules
        ]
        result = col.bulk_write(ops, ordered=False)
        print(f"\n  ✅ Inserted {result.upserted_count} / "
              f"Updated {result.modified_count} rules "
              f"→ {args.db_name}.interpretation_rules")
        client.close()


if __name__ == "__main__":
    main()
