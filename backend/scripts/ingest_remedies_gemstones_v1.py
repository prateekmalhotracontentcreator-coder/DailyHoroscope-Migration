#!/usr/bin/env python3
"""
ingest_remedies_gemstones_v1.py -- Gemstone Remedy Library (IDs 101-200)

100 rules, science_id = "jyotish_remedies_gemstones"
Collection: horoscope_db.interpretation_rules

Schema fields per source record:
  id, remedy_area, primary_gemstone, severity,
  trigger_birth_chart, trigger_ke_inference,
  synergy_conflict{synergy[], conflict[]},
  metal_finger, purification_process, wearing_mantra,
  rituals_care, dos_donts,
  activation{paksha, day, tithi, muhurta}

Standard workflow:
  python3 scripts/ingest_remedies_gemstones_v1.py --dry-run --save scripts/gemstone_rules.json
  python3 scripts/ingest_remedies_gemstones_v1.py --upload scripts/gemstone_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

Source:
  /Users/apple/Documents/Knowledge Engine_eBooks/
  Remedies + The Strategist/3. Remedies_Gemstones.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE_ID  = "jyotish_remedies_gemstones"
BOOK        = "Gemstone Remedy Library -- 100 Focus Areas"
BOOK_ID     = "remedies_gemstones_v1"
CHAP_NAME   = "Gemstone Remedies"
BATCH_ID    = f"remedies-gemstones-v1-{datetime.now().strftime('%Y%m%d')}"

SOURCE_MD = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/3. Remedies_Gemstones.md"
)

EXPECTED_IDS = set(range(101, 201))   # 101-200


# ─────────────────────────────────────────────────────────────────────────────
# TRIGGER MAP  (planet + house signals per remedy ID)
# ─────────────────────────────────────────────────────────────────────────────
TRIGGER_MAP: dict[int, dict] = {
    101: {"cat": "planetary_weakness", "tags": ["sun_7th_8th", "sun_low_shadbala"],
          "map": {"planet": ["Sun"], "house": [7, 8, 1]}},
    102: {"cat": "planetary_weakness", "tags": ["moon_scorpio", "moon_rahu_saturn"],
          "map": {"planet": ["Moon"]}},
    103: {"cat": "planetary_weakness", "tags": ["mars_4th_8th", "weak_lagna_lord"],
          "map": {"planet": ["Mars"], "house": [4, 8]}},
    104: {"cat": "planetary_weakness", "tags": ["mercury_combust", "mercury_10th_lord_weak"],
          "map": {"planet": ["Mercury"], "house": [10]}},
    105: {"cat": "planetary_weakness", "tags": ["jupiter_debilitated", "jupiter_6th_8th_12th"],
          "map": {"planet": ["Jupiter"], "house": [6, 8, 12]}},
    106: {"cat": "planetary_weakness", "tags": ["venus_debilitated", "venus_6th_8th"],
          "map": {"planet": ["Venus"], "house": [6, 8]}},
    107: {"cat": "planetary_weakness", "tags": ["saturn_1st_3rd_debilitated"],
          "map": {"planet": ["Saturn"], "house": [1, 3]}},
    108: {"cat": "planetary_weakness", "tags": ["rahu_1st_7th_10th", "rahu_conjunct_saturn"],
          "map": {"planet": ["Rahu"], "house": [1, 7, 10]}},
    109: {"cat": "planetary_weakness", "tags": ["ketu_1st_5th_9th"],
          "map": {"planet": ["Ketu"], "house": [1, 5, 9]}},
}

CATEGORY_LABELS = {
    "planetary_weakness":  "Planetary Weakness",
    "house_affliction":    "House Affliction",
    "gem_remedy":          "Gemstone Remedy",
}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE PARSER
# ─────────────────────────────────────────────────────────────────────────────

def _unescape_md(text: str) -> str:
    """Remove markdown formatting and fix invalid JSON escape sequences."""
    text = re.sub(r'\*+', '', text)
    text = (text
            .replace('\\[', '[').replace('\\]', ']')
            .replace('\\_', '_').replace('\\{', '{').replace('\\}', '}'))
    text = re.sub(r'\\(?!["\\/bfnrtu])', '', text)
    return text


def _load_source() -> list[dict]:
    """Robust object-by-object scan. Handles broken arrays, bold formatting, last-occurrence wins."""
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
        rid       = entry['id']
        trig      = TRIGGER_MAP.get(rid, {
            "cat": "gem_remedy",
            "tags": [],
            "map": {},
        })
        cat        = trig["cat"]
        cat_label  = CATEGORY_LABELS.get(cat, cat.replace("_", " ").title())
        area       = entry.get('remedy_area', '')
        gemstone   = entry.get('primary_gemstone', '')
        severity   = entry.get('severity', '')
        trig_bc    = entry.get('trigger_birth_chart', '')
        trig_ke    = entry.get('trigger_ke_inference', '')
        syn_con    = entry.get('synergy_conflict', {})
        metal      = entry.get('metal_finger', '')
        purify     = entry.get('purification_process', '')
        mantra     = entry.get('wearing_mantra', '')
        care       = entry.get('rituals_care', '')
        dos_donts  = entry.get('dos_donts', '')
        activation = entry.get('activation', {})

        act_str = (
            f"Paksha: {activation.get('paksha','')}, "
            f"Day: {activation.get('day','')}, "
            f"Tithi: {activation.get('tithi','')}, "
            f"Muhurta: {activation.get('muhurta','')}"
        )
        synergy_str = ", ".join(syn_con.get('synergy', []))
        conflict_str = ", ".join(syn_con.get('conflict', [])) if isinstance(syn_con.get('conflict'), list) else syn_con.get('conflict', '')

        detailed = (
            f"Remedy: {area} | Gemstone: {gemstone} | Severity: {severity}\n\n"
            f"Wearing Mantra: {mantra}\n"
            f"Metal & Finger: {metal}\n\n"
            f"Activation: {act_str}\n\n"
            f"Purification: {purify}\n"
            f"Care & Rituals: {care}\n"
            f"Dos & Don'ts: {dos_donts}\n\n"
            f"Synergy: {synergy_str}\n"
            f"Conflict: {conflict_str}\n\n"
            f"Birth Chart Trigger: {trig_bc}\n"
            f"KE Inference: {trig_ke}"
        )

        planets = trig["map"].get("planet", [])
        houses  = trig["map"].get("house", [])

        rule: dict = {
            "rule_id":    f"gemstone-{rid:03d}",
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
                "houses_involved":   houses,
                "yoga_check": {
                    "type":      "remedy_evaluation",
                    "checkable": False,
                },
                "trigger_condition":    trig_bc or "User-requested gemstone lookup",
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
                "primary_gemstone":     gemstone,
                "severity":             severity,
                "trigger_birth_chart":  trig_bc,
                "trigger_ke_inference": trig_ke,
                "synergy_conflict": {
                    "synergy":  syn_con.get('synergy', []),
                    "conflict": syn_con.get('conflict', []) if isinstance(syn_con.get('conflict'), list) else [conflict_str] if conflict_str else [],
                },
                "metal_finger":         metal,
                "purification_process": purify,
                "wearing_mantra":       mantra,
                "rituals_care":         care,
                "dos_donts":            dos_donts,
                "activation": {
                    "paksha":  activation.get('paksha', ''),
                    "day":     activation.get('day', ''),
                    "tithi":   activation.get('tithi', ''),
                    "muhurta": activation.get('muhurta', ''),
                },
            },
            "metadata": {
                "phase":            2,
                "checkable":        False,
                "yoga_group":       cat,
                "yoga_group_label": cat_label,
                "remedy_category":  ["gemstone"],
                "source_quality":   "PRIMARY",
                "data_quality":     "source",
                "tags":             ["remedy", "gemstone", cat, gemstone.lower()[:20]],
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
        description="Ingest Gemstone Remedy Library into MongoDB"
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
        cats: Counter = Counter(r["metadata"]["yoga_group"] for r in rules)
        sevs: Counter = Counter(r["remedy"]["severity"]     for r in rules)

        found_ids = {r["remedy"]["id"] for r in rules}
        missing   = sorted(EXPECTED_IDS - found_ids)
        extra     = sorted(found_ids - EXPECTED_IDS)

        print(f"\n{'='*60}")
        print(f"  Gemstone Remedy Library -- Dry Run")
        print(f"  Total rules built: {len(rules)}")
        print(f"  Batch ID:          {BATCH_ID}")
        print(f"  Science ID:        {SCIENCE_ID}")
        print(f"{'='*60}")
        print("\n  By trigger category:")
        for cat, cnt in sorted(cats.items()):
            print(f"    {cnt:3d}  {cat}")
        print("\n  By severity:")
        for sev, cnt in sorted(sevs.items()):
            print(f"    {cnt:3d}  {sev}")
        if missing:
            print(f"\n  ⚠️  Missing IDs: {missing}")
        else:
            print(f"\n  ✅ All {len(EXPECTED_IDS)} IDs present")
        if extra:
            print(f"\n  ⚠️  Unexpected IDs: {extra}")

        if rules:
            r = rules[0]["remedy"]
            print(f"\n  Sample -- gemstone-{r['id']:03d} ({r['remedy_area']}):")
            print(f"    Gemstone:  {r['primary_gemstone']}")
            print(f"    Mantra:    {r['wearing_mantra'][:60]}")
            print(f"    Synergy:   {r['synergy_conflict']['synergy']}")
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
