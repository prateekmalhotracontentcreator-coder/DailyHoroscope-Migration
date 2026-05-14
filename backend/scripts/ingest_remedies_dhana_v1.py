#!/usr/bin/env python3
"""
ingest_remedies_dhana_v1.py -- Dhana (Charity) Remedy Library (IDs 1-100)

100 rules, science_id = "jyotish_remedies_dhana"
Collection: horoscope_db.interpretation_rules

Schema fields per source record:
  id, remedy_area, deity, severity, mantra, yantra, paksha, tithi_day,
  season, frequency, donation_item, process_direction, attire_color,
  muhurta, guidance, trigger_birth_chart, trigger_ke_inference

Standard workflow:
  python3 scripts/ingest_remedies_dhana_v1.py --dry-run --save scripts/dhana_rules.json
  python3 scripts/ingest_remedies_dhana_v1.py --upload scripts/dhana_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

Source:
  /Users/apple/Documents/Knowledge Engine_eBooks/
  Remedies + The Strategist/2. Dhana_Remedies_JSON.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE_ID  = "jyotish_remedies_dhana"
BOOK        = "Dhana Remedy Library -- 100 Focus Areas"
BOOK_ID     = "remedies_dhana_v1"
CHAP_NAME   = "Dhana (Charity) Remedies"
BATCH_ID    = f"remedies-dhana-v1-{datetime.now().strftime('%Y%m%d')}"

SOURCE_MD = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/2. Dhana_Remedies_JSON.md"
)

EXPECTED_IDS = set(range(1, 101))   # 1-100


# ─────────────────────────────────────────────────────────────────────────────
# TRIGGER MAP  (planet + house signals per remedy ID)
# ─────────────────────────────────────────────────────────────────────────────
TRIGGER_MAP: dict[int, dict] = {
    1:  {"cat": "planetary_weakness", "tags": ["sun_7th", "sun_saturn_conjunction"],
         "map": {"planet": ["Sun"], "house": [7]}},
    2:  {"cat": "planetary_weakness", "tags": ["moon_6th_8th", "moon_rahu_conjunction"],
         "map": {"planet": ["Moon"], "house": [6, 8]}},
    3:  {"cat": "planetary_weakness", "tags": ["mars_4th_8th", "mars_saturn_conjunction"],
         "map": {"planet": ["Mars"], "house": [4, 8]}},
    4:  {"cat": "planetary_weakness", "tags": ["mercury_combust", "mercury_12th"],
         "map": {"planet": ["Mercury"], "house": [12]}},
    5:  {"cat": "planetary_weakness", "tags": ["jupiter_10th", "jupiter_rahu_conjunction"],
         "map": {"planet": ["Jupiter"], "house": [10]}},
    6:  {"cat": "planetary_weakness", "tags": ["venus_6th", "venus_sun_conjunction"],
         "map": {"planet": ["Venus"], "house": [6]}},
    7:  {"cat": "planetary_weakness", "tags": ["saturn_debilitated", "shani_sade_sati"],
         "map": {"planet": ["Saturn"]}},
    8:  {"cat": "planetary_weakness", "tags": ["rahu_6_8_12", "kalsarpa_yoga"],
         "map": {"planet": ["Rahu"], "house": [6, 8, 12]}},
    9:  {"cat": "planetary_weakness", "tags": ["ketu_6_8_12", "kalsarpa_yoga"],
         "map": {"planet": ["Ketu"], "house": [6, 8, 12]}},
}

CATEGORY_LABELS = {
    "planetary_weakness":  "Planetary Weakness",
    "house_affliction":    "House Affliction",
    "wealth_remedy":       "Wealth Remedy",
    "health_remedy":       "Health Remedy",
    "relationship_remedy": "Relationship Remedy",
    "career_remedy":       "Career Remedy",
    "spiritual_remedy":    "Spiritual Remedy",
}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE PARSER
# ─────────────────────────────────────────────────────────────────────────────

def _unescape_md(text: str) -> str:
    """Remove markdown formatting and fix invalid JSON escape sequences.

    Handles:
      - **bold** markers on batch 2+ in source files
      - Markdown bracket/underscore escapes  (\[ \] \_ etc.)
      - Invalid JSON escapes (\< \> etc.) produced by markdown rendering
    """
    # Strip bold/italic markdown markers first
    text = re.sub(r'\*+', '', text)
    # Standard markdown escape sequences → bare characters
    text = (text
            .replace('\\[', '[').replace('\\]', ']')
            .replace('\\_', '_').replace('\\{', '{').replace('\\}', '}'))
    # Remove any remaining invalid JSON escape sequences.
    # Valid JSON string escapes are: \" \\ \/ \b \f \n \r \t \uXXXX
    # Everything else (e.g. \< \> \- \: \.) is invalid -- strip the backslash.
    text = re.sub(r'\\(?!["\\/bfnrtu])', '', text)
    return text


def _load_source() -> list[dict]:
    """Load and parse all remedy entries from the source markdown file.

    Robust object-by-object scan: handles broken arrays, markdown headers
    between batches, and bold formatting on later batches. Last occurrence
    wins for any duplicate id.
    """
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
                    entries[int(float(rid))] = obj   # last occurrence wins
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
        rid = entry['id']
        trig = TRIGGER_MAP.get(rid, {
            "cat": "house_affliction",
            "tags": [],
            "map": {},
        })
        cat        = trig["cat"]
        cat_label  = CATEGORY_LABELS.get(cat, cat.replace("_", " ").title())
        area       = entry.get('remedy_area', '')
        deity      = entry.get('deity', '')
        severity   = entry.get('severity', '')
        mantra     = entry.get('mantra', '')
        yantra     = entry.get('yantra', '')
        paksha     = entry.get('paksha', '')
        tithi_day  = entry.get('tithi_day', '')
        season     = entry.get('season', '')
        frequency  = entry.get('frequency', '')
        donation   = entry.get('donation_item', '')
        process    = entry.get('process_direction', '')
        color      = entry.get('attire_color', '')
        muhurta    = entry.get('muhurta', '')
        guidance   = entry.get('guidance', '')
        trig_bc    = entry.get('trigger_birth_chart', '')
        trig_ke    = entry.get('trigger_ke_inference', '')

        detailed = (
            f"Remedy: {area} | Deity: {deity} | Severity: {severity}\n\n"
            f"Mantra: {mantra}\n"
            f"Yantra: {yantra}\n\n"
            f"Practice Protocol:\n"
            f"  Paksha:    {paksha}\n"
            f"  Timing:    {tithi_day} -- {muhurta}\n"
            f"  Season:    {season}\n"
            f"  Frequency: {frequency}\n"
            f"  Donation:  {donation}\n"
            f"  Process:   {process}\n"
            f"  Attire:    {color}\n\n"
            f"Guidance: {guidance}\n\n"
            f"Birth Chart Trigger: {trig_bc}\n"
            f"KE Inference: {trig_ke}"
        )

        planets = trig["map"].get("planet", [])
        houses  = trig["map"].get("house", [])

        rule: dict = {
            "rule_id":    f"dhana-{rid:03d}",
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
                "trigger_condition": trig_bc or "User-requested remedy lookup",
                "astrological_mapping": trig["map"],
                "trigger_tags": trig["tags"],
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
                "id":                 rid,
                "remedy_area":        area,
                "deity":              deity,
                "severity":           severity,
                "mantra":             mantra,
                "yantra":             yantra,
                "paksha":             paksha,
                "tithi_day":          tithi_day,
                "season":             season,
                "frequency":          frequency,
                "donation_item":      donation,
                "process_direction":  process,
                "attire_color":       color,
                "muhurta":            muhurta,
                "guidance":           guidance,
                "trigger_birth_chart":    trig_bc,
                "trigger_ke_inference":   trig_ke,
            },
            "metadata": {
                "phase":            2,
                "checkable":        False,
                "yoga_group":       cat,
                "yoga_group_label": cat_label,
                "remedy_category":  ["dhana", "charity"],
                "source_quality":   "PRIMARY",
                "data_quality":     "source",
                "tags":             ["remedy", "dhana", "charity", cat, deity.lower()],
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
        description="Ingest Dhana Remedy Library into MongoDB"
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

    # ── DRY RUN ──────────────────────────────────────────────────────────────
    if args.dry_run:
        rules = _build_rules()
        from collections import Counter
        cats: Counter = Counter(r["metadata"]["yoga_group"] for r in rules)
        sevs: Counter = Counter(r["remedy"]["severity"]     for r in rules)

        found_ids  = {r["remedy"]["id"] for r in rules}
        missing    = sorted(EXPECTED_IDS - found_ids)
        extra      = sorted(found_ids - EXPECTED_IDS)

        print(f"\n{'='*60}")
        print(f"  Dhana Remedy Library -- Dry Run")
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

        # Spot-check first entry
        sample = rules[0] if rules else None
        if sample:
            r = sample["remedy"]
            print(f"\n  Sample -- {sample['rule_id']} ({r['remedy_area']}):")
            print(f"    Deity:        {r['deity']}")
            print(f"    Donation:     {r['donation_item']}")
            print(f"    Muhurta:      {r['muhurta']}")
            print(f"    BC Trigger:   {r['trigger_birth_chart']}")
        print()

        if args.save:
            out = Path(args.save)
            out.write_text(json.dumps(rules, indent=2, ensure_ascii=False))
            print(f"  ✅ Saved {len(rules)} rules → {out}\n")
        return

    # ── UPLOAD ───────────────────────────────────────────────────────────────
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
