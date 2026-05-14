#!/usr/bin/env python3
"""
ingest_remedies_crystals_v1.py -- Crystal Remedy Library (IDs 201-300)

100 rules, science_id = "jyotish_remedies_crystals"
Collection: horoscope_db.interpretation_rules

Schema fields per source record:
  id, remedy_area, crystal_name, form, primary_chakra, tattva_imbalance,
  trigger_birth_chart, trigger_ke_inference, synergy_grid[], conflict,
  placement, cleansing, programming_mantra, start_day, recharge_freq,
  dos_donts, care, guidance

⚠️  SOURCE BUG: 4. Crystal Remedies_JSON.md contains TWO separate [...] arrays
    (array break between IDs 202 and 203). This script handles this automatically
    by scanning for ALL JSON arrays in the file and merging.

Standard workflow:
  python3 scripts/ingest_remedies_crystals_v1.py --dry-run --save scripts/crystal_rules.json
  python3 scripts/ingest_remedies_crystals_v1.py --upload scripts/crystal_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

Source:
  /Users/apple/Documents/Knowledge Engine_eBooks/
  Remedies + The Strategist/4. Crystal Remedies_JSON.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE_ID  = "jyotish_remedies_crystals"
BOOK        = "Crystal Remedy Library -- 100 Focus Areas"
BOOK_ID     = "remedies_crystals_v1"
CHAP_NAME   = "Crystal Remedies"
BATCH_ID    = f"remedies-crystals-v1-{datetime.now().strftime('%Y%m%d')}"

SOURCE_MD = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/4. Crystal Remedies_JSON.md"
)

EXPECTED_IDS = set(range(201, 301))   # 201-300


# ─────────────────────────────────────────────────────────────────────────────
# TRIGGER MAP  (planet + house signals per remedy ID)
# ─────────────────────────────────────────────────────────────────────────────
TRIGGER_MAP: dict[int, dict] = {
    201: {"cat": "planetary_weakness", "tags": ["rahu_1st_8th", "psychic_shield"],
          "map": {"planet": ["Rahu"], "house": [1, 8]}},
    202: {"cat": "planetary_weakness", "tags": ["ketu_lagna_lord", "grounding"],
          "map": {"planet": ["Ketu"]}},
    203: {"cat": "planetary_weakness", "tags": ["saturn_12th", "fear_removal"],
          "map": {"planet": ["Saturn"], "house": [12]}},
}

CHAKRA_PLANET_MAP = {
    "Root (Muladhara)":      {"planet": ["Saturn", "Mars"], "tags": ["root_chakra"]},
    "Sacral (Svadhisthana)": {"planet": ["Moon", "Venus"],  "tags": ["sacral_chakra"]},
    "Solar Plexus (Manipura)":{"planet": ["Sun", "Mars"],   "tags": ["solar_plexus_chakra"]},
    "Heart (Anahata)":       {"planet": ["Venus", "Moon"],  "tags": ["heart_chakra"]},
    "Throat (Vishuddha)":    {"planet": ["Mercury"],        "tags": ["throat_chakra"]},
    "Third Eye (Ajna)":      {"planet": ["Jupiter", "Ketu"],"tags": ["third_eye_chakra"]},
    "Crown (Sahasrara)":     {"planet": ["Ketu", "Jupiter"],"tags": ["crown_chakra"]},
}

CATEGORY_LABELS = {
    "planetary_weakness": "Planetary Weakness",
    "chakra_imbalance":   "Chakra Imbalance",
    "crystal_remedy":     "Crystal Remedy",
}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE PARSER  (handles split-array bug automatically)
# ─────────────────────────────────────────────────────────────────────────────

def _unescape_md(text: str) -> str:
    """Remove markdown formatting and fix invalid JSON escape sequences.
    Also handles the split-array bug -- object scanning doesn't require valid array structure.
    """
    text = re.sub(r'\*+', '', text)
    text = (text
            .replace('\\[', '[').replace('\\]', ']')
            .replace('\\_', '_').replace('\\{', '{').replace('\\}', '}'))
    text = re.sub(r'\\(?!["\\/bfnrtu])', '', text)
    return text


def _load_source() -> list[dict]:
    """Robust object-by-object scan. Handles split-array bug, bold formatting, last-occurrence wins."""
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

def _infer_trigger(rid: int, chakra: str, tattva: str) -> dict:
    """Fall back to CHAKRA_PLANET_MAP when ID not in explicit TRIGGER_MAP."""
    if rid in TRIGGER_MAP:
        return TRIGGER_MAP[rid]
    chakra_trig = CHAKRA_PLANET_MAP.get(chakra, {})
    return {
        "cat":  "chakra_imbalance",
        "tags": chakra_trig.get("tags", ["crystal_remedy"]),
        "map":  {"planet": chakra_trig.get("planet", [])},
    }


def _build_rules() -> list[dict]:
    entries = _load_source()
    now     = datetime.now(timezone.utc).isoformat()
    rules: list[dict] = []

    for entry in entries:
        rid        = entry['id']
        chakra     = entry.get('primary_chakra', '')
        tattva     = entry.get('tattva_imbalance', '')
        trig       = _infer_trigger(rid, chakra, tattva)
        cat        = trig["cat"]
        cat_label  = CATEGORY_LABELS.get(cat, cat.replace("_", " ").title())

        area       = entry.get('remedy_area', '')
        crystal    = entry.get('crystal_name', '')
        form       = entry.get('form', '')
        trig_bc    = entry.get('trigger_birth_chart', '')
        trig_ke    = entry.get('trigger_ke_inference', '')
        synergy    = entry.get('synergy_grid', [])
        conflict   = entry.get('conflict', '')
        placement  = entry.get('placement', '')
        cleansing  = entry.get('cleansing', '')
        mantra     = entry.get('programming_mantra', '')
        start_day  = entry.get('start_day', '')
        recharge   = entry.get('recharge_freq', '')
        dos_donts  = entry.get('dos_donts', '')
        care       = entry.get('care', '')
        guidance   = entry.get('guidance', '')

        if isinstance(synergy, list):
            synergy_str = ", ".join(synergy)
        else:
            synergy_str = str(synergy)

        detailed = (
            f"Crystal: {crystal} ({form}) | Remedy: {area}\n"
            f"Chakra: {chakra} | Tattva Imbalance: {tattva}\n\n"
            f"Programming Mantra: {mantra}\n"
            f"Placement: {placement}\n"
            f"Start Day: {start_day} | Recharge: {recharge}\n\n"
            f"Cleansing: {cleansing}\n"
            f"Care: {care}\n"
            f"Dos & Don'ts: {dos_donts}\n\n"
            f"Synergy Grid: {synergy_str}\n"
            f"Conflict: {conflict}\n\n"
            f"Guidance: {guidance}\n"
            f"Birth Chart Trigger: {trig_bc}\n"
            f"KE Inference: {trig_ke}"
        )

        planets = trig["map"].get("planet", [])

        rule: dict = {
            "rule_id":    f"crystal-{rid:03d}",
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
                "sub_type":          cat,
                "yoga_name":         area,
                "yoga_group":        cat,
                "yoga_group_label":  cat_label,
                "planets_involved":  planets,
                "houses_involved":   [],
                "yoga_check": {
                    "type":      "remedy_evaluation",
                    "checkable": False,
                },
                "trigger_condition":    trig_bc or "User-requested crystal lookup",
                "astrological_mapping": trig["map"],
                "trigger_tags":         trig["tags"],
            },
            "interpretation": {
                "summary":  area,
                "detailed": detailed,
                "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
                "remedy":           [],
                "timing_indicator": False,
                "strength_modifier": None,
            },
            "remedy": {
                "id":                   rid,
                "remedy_area":          area,
                "crystal_name":         crystal,
                "form":                 form,
                "primary_chakra":       chakra,
                "tattva_imbalance":     tattva,
                "trigger_birth_chart":  trig_bc,
                "trigger_ke_inference": trig_ke,
                "synergy_grid":         synergy if isinstance(synergy, list) else [synergy],
                "conflict":             conflict,
                "placement":            placement,
                "cleansing":            cleansing,
                "programming_mantra":   mantra,
                "start_day":            start_day,
                "recharge_freq":        recharge,
                "dos_donts":            dos_donts,
                "care":                 care,
                "guidance":             guidance,
            },
            "metadata": {
                "phase":            2,
                "checkable":        False,
                "yoga_group":       cat,
                "yoga_group_label": cat_label,
                "remedy_category":  ["crystal", "chakra"],
                "source_quality":   "PRIMARY",
                "data_quality":     "source",
                "tags":             ["remedy", "crystal", "chakra", cat, crystal.lower()[:20]],
                "trigger_category": cat,
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
        description="Ingest Crystal Remedy Library into MongoDB (handles split-array bug)"
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
        from collections import Counter
        cats: Counter = Counter(r["metadata"]["yoga_group"]  for r in rules)
        chakras: Counter = Counter(r["remedy"]["primary_chakra"] for r in rules)

        found_ids = {r["remedy"]["id"] for r in rules}
        missing   = sorted(EXPECTED_IDS - found_ids)
        extra     = sorted(found_ids - EXPECTED_IDS)

        print(f"\n{'='*60}")
        print(f"  Crystal Remedy Library -- Dry Run")
        print(f"  Total rules built:  {len(rules)}")
        print(f"  Batch ID:           {BATCH_ID}")
        print(f"  Science ID:         {SCIENCE_ID}")
        print(f"  ⚠️  Split-array fix:  ACTIVE (scanning all arrays in source)")
        print(f"{'='*60}")
        print("\n  By trigger category:")
        for cat, cnt in sorted(cats.items()):
            print(f"    {cnt:3d}  {cat}")
        print("\n  By chakra:")
        for ch, cnt in sorted(chakras.items()):
            print(f"    {cnt:3d}  {ch}")
        if missing:
            print(f"\n  ⚠️  Missing IDs: {missing}")
        else:
            print(f"\n  ✅ All {len(EXPECTED_IDS)} IDs present")
        if extra:
            print(f"\n  ⚠️  Unexpected IDs: {extra}")

        if rules:
            r = rules[0]["remedy"]
            print(f"\n  Sample -- crystal-{r['id']:03d} ({r['remedy_area']}):")
            print(f"    Crystal:   {r['crystal_name']} ({r['form']})")
            print(f"    Chakra:    {r['primary_chakra']}")
            print(f"    Mantra:    {r['programming_mantra']}")
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
