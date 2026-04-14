#!/usr/bin/env python3
"""
BPHS Vol 1 — Effects of Houses (Chapters 12–23)
ingest_bphs_houses.py

Reusable script for all 12 house-effects chapters.
Each chapter covers the astrological effects and combinations
related to one of the 12 Bhavas (houses).

Condition type: bhava_combination
  — captures house lord placement rules, planet occupation rules,
    aspect rules, and multi-planet combination yogas per house.

Rule ID:  R-BPHS{CHAPTER}-{INDEX:03d}
  e.g.   R-BPHS12-001  (Ch 12 / 1st house, rule 1)
         R-BPHS13-004  (Ch 13 / 2nd house, rule 4)

Usage:
  # Ingest Chapter 12 (1st house)
  python3 scripts/ingest_bphs_houses.py \\
    --rtf "~/Documents/Knowledge Engine_eBooks/BPHS Ch 12 Vol 1.rtf" \\
    --house 1 \\
    --chapter 12 \\
    --mongo-url "$MONGO_URL" \\
    --db-name EverydayHoroscope \\
    [--dry-run]

  # Ingest Chapter 18 (7th house)
  python3 scripts/ingest_bphs_houses.py \\
    --rtf "path/to/BPHS Ch 18 Vol 1.rtf" \\
    --house 7 \\
    --chapter 18 \\
    --mongo-url "$MONGO_URL" \\
    --db-name EverydayHoroscope
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pymongo import MongoClient

# ── Constants ─────────────────────────────────────────────────────────────────

SCIENCE = "vedic_astrology"
BOOK    = "Brihat Parashara Hora Shastra"
BOOK_ID = "bphs_vol1"

CHAPTER_NAMES: dict[int, str] = {
    12: "Effects of First House",   13: "Effects of Second House",
    14: "Effects of Third House",   15: "Effects of Fourth House",
    16: "Effects of Fifth House",   17: "Effects of Sixth House",
    18: "Effects of Seventh House", 19: "Effects of Eighth House",
    20: "Effects of Ninth House",   21: "Effects of Tenth House",
    22: "Effects of Eleventh House",23: "Effects of Twelfth House",
}

HOUSE_LIFE_DOMAINS: dict[int, str] = {
    1:  "health",        2:  "wealth",
    3:  "relationships", 4:  "home",
    5:  "children",      6:  "health",
    7:  "relationships", 8:  "longevity",
    9:  "fortune",       10: "career",
    11: "wealth",        12: "spirituality",
}

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
           "Saturn", "Rahu", "Ketu"]

PLANET_CODES: dict[str, str] = {
    "Sun": "SUN", "Moon": "MOO", "Mars": "MAR",
    "Mercury": "MER", "Jupiter": "JUP", "Venus": "VEN",
    "Saturn": "SAT", "Rahu": "RAH", "Ketu": "KET",
}

# Sections to skip — anatomical reference, not prediction rules
SKIP_HEADINGS = {
    "decanates and bodily limbs", "decanates", "bodily limbs",
    "limbs", "notes", "center",
}

# ── RTF parser ────────────────────────────────────────────────────────────────

def strip_rtf(raw: str) -> str:
    """Convert RTF markup to plain text."""
    text = raw
    # Special chars before control word removal
    text = text.replace("\\'92", "'").replace("\\'93", '"').replace("\\'94", '"')
    text = text.replace("\\'b0", "°")
    text = re.sub(r"\\'[0-9a-f]{2}", '', text)
    # RTF line break: backslash+newline → newline
    text = re.sub(r'\\\n', '\n', text)
    # Named control words that map to whitespace
    text = re.sub(r'\\par\b\s*', '\n', text)
    text = re.sub(r'\\page\b\s*', '\n', text)
    # Remove ALL remaining control words (\ + letters + optional digits + optional space)
    text = re.sub(r'\\[a-z*]+\-?\d*\s?', ' ', text)
    # Remove lone backslashes
    text = re.sub(r'\\[^a-z\n]', '', text)
    text = re.sub(r'\\', '', text)
    # Remove braces last (now just empty structural markers)
    text = text.replace('{', '').replace('}', '')
    # Collapse whitespace within lines
    lines = []
    for line in text.splitlines():
        line = re.sub(r'\s+', ' ', line).strip()
        if line and line != ';':
            lines.append(line)
    return '\n'.join(lines)


def split_into_sloka_blocks(text: str) -> list[tuple[str, str]]:
    """
    Split plain text into (sloka_label, block_text) tuples.
    Handles:
      - Single slokas:  "5. HEADING .."
      - Sloka ranges:   "5-7. HEADING .."
      - OCR artefacts:  "l-2." parsed as "1-2."
    """
    # Normalise OCR artefacts: leading 'l' digit → '1'
    text = re.sub(r'(?m)^\s*l(?=[-\d.])', '1', text)

    # Pattern: one or more digits, optional dash+digits, period, space
    sloka_re = re.compile(
        r'(?m)^[ \t]*(\d+(?:\s*[-–]\s*\d+)?)\.\s+(.+)$'
    )

    matches = list(sloka_re.finditer(text))
    if not matches:
        return []

    blocks: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        label   = m.group(1).strip()
        heading = m.group(2).strip()
        start   = m.end()
        end     = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body    = text[start:end].strip()
        # Merge heading line with body for full rule text
        full_text = heading + " " + body
        blocks.append((label, full_text))
    return blocks


def should_skip(heading_line: str) -> bool:
    """Return True for reference/anatomical sections that are not prediction rules."""
    h = heading_line.lower()
    for skip_phrase in SKIP_HEADINGS:
        if skip_phrase in h:
            return True
    # Body-part diagrams: lines that are just anatomy lists
    if re.match(r'^(left|right)\s+(side|eye|ear|knee|calf|foot|thigh|arm|shoulder|neck)',
                h, re.IGNORECASE):
        return True
    return False


def clean_notes(text: str) -> tuple[str, str]:
    """
    Separate rule text from translator's Notes.
    Returns (rule_text, notes_text).
    """
    notes_re = re.compile(r'\bNotes?\s*:', re.IGNORECASE)
    m = notes_re.search(text)
    if m:
        rule_part  = text[:m.start()].strip()
        notes_part = text[m.start():].strip()
        return rule_part, notes_part
    return text.strip(), ""


def extract_heading(text: str) -> str:
    """
    Extract the CAPS heading from the start of a rule block.
    e.g. "PHYSICAL COMFORTS .. Should the ascendant..." → "PHYSICAL COMFORTS"
    """
    m = re.match(r'^([A-Z][A-Z\s/()]+?)(?:\s*\.{2}|\s*[.;:\'"])', text)
    if m:
        return m.group(1).strip().title()
    # Fallback: first 5 words
    words = text.split()[:5]
    return " ".join(words).title()


def extract_planets(text: str) -> list[str]:
    """Return list of planet names mentioned in text."""
    found = []
    for p in PLANETS:
        if re.search(rf'\b{p}\b', text, re.IGNORECASE):
            found.append(p)
    return found


def infer_sub_type(text: str, heading: str) -> str:
    """
    Classify the rule as one of:
      lord_placement   — about where a house lord is placed
      planet_occupation — about which planet occupies this house
      aspect_rule      — about aspect/conjunction conditions
      combination      — multi-planet yoga
      birth_special    — unusual birth conditions
      general_principle — overarching principles
    """
    t = (text + " " + heading).lower()
    if any(w in t for w in ["lord", "lagna lord", "ascendant lord"]):
        if any(w in t for w in ["born", "twin", "mother", "coil", "navamsa"]):
            return "birth_special"
        return "lord_placement"
    if any(w in t for w in ["in the ascendant", "in the house", "occupy", "in 1st",
                             "in lagna", "benefic in", "malefic in"]):
        return "planet_occupation"
    if any(w in t for w in ["aspect", "conjunct", "aspected by"]):
        return "aspect_rule"
    if any(w in t for w in ["born", "twin", "mother", "coil", "birth"]):
        return "birth_special"
    if len(extract_planets(text)) >= 2:
        return "combination"
    return "general_principle"


# ── Rule builder ──────────────────────────────────────────────────────────────

def make_source(chapter: int, batch_id: str) -> dict:
    chap_name = CHAPTER_NAMES.get(chapter, f"Effects of House {chapter - 11}")
    return {
        "book":           BOOK,
        "book_id":        BOOK_ID,
        "chapter":        str(chapter),
        "chapter_name":   chap_name,
        "batch_id":       batch_id,
        "primary":        BOOK,
        "page_ref":       None,
        "passage_ref_id": None,
    }


def block_to_rule(label: str, raw_text: str, house: int, chapter: int,
                  batch_id: str, index: int) -> dict | None:
    """Convert a sloka block to a rule document. Returns None if block should be skipped."""
    rule_text, notes_text = clean_notes(raw_text)

    # Skip short or anatomical blocks
    if should_skip(rule_text):
        return None
    if len(rule_text.split()) < 6:
        return None

    heading  = extract_heading(rule_text)
    planets  = extract_planets(rule_text + " " + notes_text)
    sub_type = infer_sub_type(rule_text, heading)

    # Combine rule text with notes for the detailed field
    detailed = rule_text
    if notes_text:
        detailed = rule_text + "\n\nNotes: " + notes_text.replace("Notes :", "").strip()

    summary = rule_text.split(".")[0].strip()
    if len(summary) < 20:
        # Use first sentence properly
        m = re.match(r'^(.{20,}?[.!?])', rule_text)
        summary = m.group(1).strip() if m else rule_text[:120]

    rule_id = f"R-BPHS{chapter}-{index:03d}"
    life_domain = HOUSE_LIFE_DOMAINS.get(house, "general")

    tags = ["verbatim", "bhava_combination", f"house{house}", f"chapter{chapter}", sub_type]

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source":     make_source(chapter, batch_id),
        "condition": {
            "type":             "bhava_combination",
            "house":            house,
            "sub_type":         sub_type,
            "sloka":            label,
            "heading":          heading,
            "planets_involved": planets,
            "sub_conditions":   [],
            "operator":         "and",
        },
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        life_domain,
            "tags":               tags,
        },
        "metadata": {
            "planets_involved": planets,
            "houses_involved":  [house],
            "signs_involved":   [],
            "condition_count":  1,
        },
        "confidence": {
            "base":                  0.82,
            "source_weight":         0.95,   # BPHS = highest authority
            "cross_book_multiplier": 1.0,
        },
        "approval_status": "pending_review",
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


def parse_rtf_file(rtf_path: str, house: int, chapter: int,
                   batch_id: str) -> list[dict]:
    """Parse RTF file and return list of rule documents."""
    raw = Path(rtf_path).expanduser().read_text(encoding="utf-8", errors="replace")
    plain = strip_rtf(raw)
    blocks = split_into_sloka_blocks(plain)

    rules: list[dict] = []
    idx = 1
    for label, text in blocks:
        rule = block_to_rule(label, text, house, chapter, batch_id, idx)
        if rule is not None:
            rules.append(rule)
            idx += 1
    return rules


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Ingest BPHS Vol 1 house-effects chapter (Ch 12–23)"
    )
    parser.add_argument("--rtf",       required=True,
                        help="Path to the .rtf file for this chapter")
    parser.add_argument("--house",     required=True, type=int, choices=range(1, 13),
                        metavar="HOUSE", help="House number 1-12")
    parser.add_argument("--chapter",   required=True, type=int, choices=range(12, 24),
                        metavar="CHAPTER", help="BPHS chapter number (12-23)")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   required=True)
    parser.add_argument("--dry-run",   action="store_true",
                        help="Print summary but do NOT write to MongoDB")
    args = parser.parse_args()

    batch_id = f"bphs-ch{args.chapter}-v1-{datetime.now(timezone.utc).strftime('%Y%m%d')}"
    chap_name = CHAPTER_NAMES.get(args.chapter, f"Effects of House {args.house}")

    print(f"\nBPHS Chapter {args.chapter} — {chap_name}")
    print(f"House {args.house}  |  batch_id: {batch_id}")
    print("─" * 60)

    rules = parse_rtf_file(args.rtf, args.house, args.chapter, batch_id)

    if not rules:
        print("⚠  No rules extracted. Check RTF path and file content.")
        return

    # Summary by sub_type
    sub_types: dict[str, int] = {}
    for r in rules:
        st = r["condition"]["sub_type"]
        sub_types[st] = sub_types.get(st, 0) + 1
    for st, count in sub_types.items():
        print(f"  {st:<25} : {count}")
    print(f"  {'─' * 33}")
    print(f"  {'TOTAL':<25} : {len(rules)}")
    print(f"\n  Isolation: approval_status='pending_review' — zero rules reach live users")

    if args.dry_run:
        print("\n[DRY RUN] — no changes written to MongoDB")
        print("\nSample rules:")
        for r in rules[:4]:
            cond = r["condition"]
            print(f"\n  {r['rule_id']}")
            print(f"    sloka     : {cond['sloka']}")
            print(f"    sub_type  : {cond['sub_type']}")
            print(f"    heading   : {cond['heading']}")
            print(f"    planets   : {cond['planets_involved']}")
            print(f"    summary   : {r['interpretation']['summary'][:90]}")
        return

    # ── Insert ────────────────────────────────────────────────────────────────
    client = MongoClient(args.mongo_url)
    db     = client[args.db_name]
    col    = db["interpretation_rules"]

    existing = col.count_documents({"source.batch_id": batch_id})
    if existing:
        print(f"\n⚠  Batch '{batch_id}' already has {existing} rules in MongoDB.")
        print("   Delete those documents first, then re-run without --dry-run.")
        client.close()
        return

    result = col.insert_many(rules, ordered=False)
    print(f"\n✅  Inserted {len(result.inserted_ids)} rules into MongoDB")
    print(f"   batch_id : {batch_id}")
    print(f"\n   Validate with:")
    print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
    print(f"     --db-name EverydayHoroscope --batch-id {batch_id}")
    client.close()


if __name__ == "__main__":
    main()
