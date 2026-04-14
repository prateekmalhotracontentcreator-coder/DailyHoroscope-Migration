#!/usr/bin/env python3
"""
Dedicated parser + ingest for Chapter 15 — Planets in Different Houses.

Structure of the RTF:
    Planet Name          (single word heading: Sun / Moon / Mars...)
    First House          (house heading)
    <text block>         (raw interpretation)
    In female horoscope: (optional sub-section)
    <female text>

    Second House
    <text block>
    ...

This script:
  1. Strips RTF formatting → clean plain text
  2. Parses the Planet → House → Text structure
  3. Creates one InterpretationRuleDocument per (planet, house) pair
     with paraphrase_mode="none" — text stored verbatim, no AI calls
  4. Inserts into MongoDB alongside (not replacing) existing rules

Usage:
  python3 scripts/ingest_chapter15.py \\
    --rtf "~/Documents/Knowledge Engine_eBooks/Chapter 15.rtf" \\
    --mongo-url "mongodb+srv://..." \\
    --db-name EverydayHoroscope \\
    [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pymongo import MongoClient
from knowledge_schema import InterpretationRuleDocument

# ─── Constants ───────────────────────────────────────────────────────────────

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
           "Saturn", "Rahu", "Ketu"]

HOUSE_WORDS = {
    "first": 1, "second": 2, "third": 3, "fourth": 4,
    "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
    "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12,
}

BOOK     = "A Text Book of Astrology"
CHAPTER  = "Chapter 15 — Planets in Different Houses: Prediction"
SCIENCE  = "vedic_astrology"
BATCH_ID = f"a-text-book-ch15-verbatim-{datetime.now(timezone.utc).strftime('%Y%m%d')}"


# ─── RTF stripper ────────────────────────────────────────────────────────────

def strip_rtf(rtf_text: str) -> str:
    """Convert RTF to plain text — handles Mac TextEdit RTF output."""
    # Remove RTF header and font/colour tables
    text = re.sub(r"^\{\\rtf1.*?\\viewkind0\s*", "", rtf_text, flags=re.DOTALL)
    # Convert explicit page breaks to double newlines
    text = re.sub(r"\\page\s*", "\n\n", text)
    # Convert \cf0, \cf2 colour switches (ignore)
    text = re.sub(r"\\cf\d+\s*", "", text)
    # Convert paragraph style directives to newlines
    text = re.sub(r"\\pard[^\n\\]*", "\n", text)
    # Remove remaining control words with optional parameter
    text = re.sub(r"\\[a-zA-Z]+(-?\d+)?[ ]?", "", text)
    # Remove RTF braces
    text = text.replace("{", "").replace("}", "")
    # Normalise line endings — RTF uses \  for line break
    text = text.replace("\\\n", "\n")
    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ─── Structure parser ─────────────────────────────────────────────────────────

def parse_chapter15(plain_text: str) -> list[dict]:
    """
    Parse the plain text into a list of rule dicts:
    {
        "planet": "Sun",
        "house": 1,
        "text": "<full paragraph>",
        "female_text": "<female horoscope paragraph or ''>",
    }
    """
    planet_pat = re.compile(
        r"^(" + "|".join(PLANETS) + r")$", re.IGNORECASE | re.MULTILINE
    )
    house_pat = re.compile(
        r"^(" + "|".join(HOUSE_WORDS) + r")\s+house$", re.IGNORECASE | re.MULTILINE
    )
    female_pat = re.compile(r"in\s+female\s+horoscope\s*:?", re.IGNORECASE)

    rules: list[dict] = []
    current_planet: str = ""
    current_house: int  = 0
    current_lines: list[str] = []

    def flush() -> None:
        if not current_planet or not current_house or not current_lines:
            return
        full_text = " ".join(current_lines).strip()
        # Split off female horoscope section
        female_match = female_pat.search(full_text)
        if female_match:
            main_text   = full_text[: female_match.start()].strip()
            female_text = full_text[female_match.end() :].strip()
        else:
            main_text   = full_text
            female_text = ""
        rules.append({
            "planet":      current_planet,
            "house":       current_house,
            "text":        main_text,
            "female_text": female_text,
        })

    for line in plain_text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Check for planet heading
        pm = planet_pat.match(line)
        if pm:
            flush()
            current_planet = pm.group(1).capitalize()
            current_house  = 0
            current_lines  = []
            continue

        # Check for house heading
        hm = house_pat.match(line)
        if hm:
            flush()
            current_house = HOUSE_WORDS[hm.group(1).lower()]
            current_lines = []
            continue

        # Content line
        if current_planet and current_house:
            current_lines.append(line)

    flush()  # last block
    return rules


# ─── Rule builder ─────────────────────────────────────────────────────────────

def build_rule(entry: dict, seq: int) -> dict:
    """Convert a parsed entry into a MongoDB-ready dict."""
    planet = entry["planet"]
    house  = entry["house"]
    text   = entry["text"]
    f_text = entry["female_text"]

    # summary = first sentence of the main text
    first_sentence = re.split(r"(?<=[.!?])\s+", text)[0][:250] if text else ""

    # detailed = full text; append female section with clear label
    detailed = text
    if f_text:
        detailed += f"\n\nIn female horoscope: {f_text}"

    planet_short = planet[:3].upper()
    rule_id = f"R-ATEXTB-{planet_short}-{house}H-V-{seq:03d}"

    return {
        "rule_id": rule_id,
        "version": 1,
        "science_id": SCIENCE,
        "approval_status": "pending_review",
        "life_domain": "general",
        "claim_axis": "general_trend",
        "claim_scope": "tendency",
        "claim_polarity": "neutral",
        "timing_bias": "none",
        "strength_band": "medium",
        "subject_scope": "self",
        "condition": {
            "type": "planet_in_house",
            "planet": planet,
            "house": house,
            "sign": "",
            "sub_conditions": [],
            "operator": "and",
        },
        "interpretation": {
            "summary":  first_sentence,
            "detailed": detailed,
            "full_text_passages": [
                {
                    "text":            detailed,
                    "source":          BOOK,
                    "chapter":         CHAPTER,
                    "word_count":      len(detailed.split()),
                    "voice_tone":      "classical",
                    "confidence":      "HIGH",
                    "paraphrase_notes": "verbatim — no paraphrase applied",
                }
            ],
            "positive_aspects":    [],
            "challenging_aspects": [],
            "remedies":            [],
        },
        "categories":   ["general"],
        "source": {
            "primary":          BOOK,
            "chapter":          CHAPTER,
            "author_voice":     "classical",
            "secondary_sources": [],
            "batch_id":         BATCH_ID,
        },
        "modifiers":    [],
        "conflicts_with": [],
        "weight":       1.0,
        "tags":         ["verbatim", "planet_in_house", "chapter15"],
        "active":       True,
    }


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rtf",       required=True, help="Path to Chapter 15.rtf")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   required=True)
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()

    rtf_path = Path(args.rtf).expanduser()
    if not rtf_path.exists():
        sys.exit(f"RTF file not found: {rtf_path}")

    # 1. Read + strip RTF
    raw = rtf_path.read_text(encoding="utf-8", errors="replace")
    plain = strip_rtf(raw)

    # 2. Parse structure
    entries = parse_chapter15(plain)
    print(f"\nParsed {len(entries)} planet-house blocks from RTF\n")

    # 3. Preview table
    print(f"{'PLANET':<12} {'HOUSE':>5}  {'WORDS':>5}  {'FEMALE':>6}  SUMMARY (60 chars)")
    print("-" * 80)
    for e in entries:
        summary = " ".join(e["text"].split())[:60]
        has_f   = "✓" if e["female_text"] else " "
        print(f"{e['planet']:<12} {e['house']:>5}  {len(e['text'].split()):>5}  "
              f"  {has_f}     {summary}...")

    # 4. Build rule documents
    rules = [build_rule(e, i + 1) for i, e in enumerate(entries)]

    # 5. Validate expected count
    print(f"\n{'=' * 60}")
    print(f"Rules built    : {len(rules)}")
    print(f"Expected       : up to 108  (9 planets × 12 houses)")
    missing = set()
    found   = {(r["condition"]["planet"], r["condition"]["house"]) for r in rules}
    for p in PLANETS:
        for h in range(1, 13):
            if (p, h) not in found:
                missing.add((p, h))
    if missing:
        print(f"Missing combos : {len(missing)}")
        for p, h in sorted(missing, key=lambda x: (PLANETS.index(x[0]), x[1])):
            print(f"  {p} in house {h}")
    else:
        print("Missing combos : none — all 108 present ✅")

    if args.dry_run:
        print(f"\n[DRY RUN] — nothing written to MongoDB.")
        print(f"Run without --dry-run to insert {len(rules)} rules.")
        return

    # 6. Insert into MongoDB
    client = MongoClient(args.mongo_url)
    db = client[args.db_name]
    col = db["interpretation_rules"]

    # Check for existing verbatim batch
    existing = col.count_documents({"source.batch_id": BATCH_ID})
    if existing:
        print(f"\n⚠  Batch '{BATCH_ID}' already has {existing} rules in MongoDB.")
        print("   Use --force to re-insert (not yet implemented — delete manually).")
        client.close()
        return

    result = col.insert_many(rules, ordered=False)
    print(f"\n✅  Inserted {len(result.inserted_ids)} rules into MongoDB")
    print(f"   batch_id : {BATCH_ID}")
    print(f"   tags     : verbatim, planet_in_house, chapter15")
    print(f"\n   These sit alongside the existing OCR-extracted rules for comparison.")
    print(f"   Open /admin/library and filter by tag 'verbatim' to review them.")
    client.close()


if __name__ == "__main__":
    main()
