#!/usr/bin/env python3
"""
BPHS Vol 1 — Effects of Houses (Chapters 12–23)
ingest_bphs_houses_v2.py

AI-assisted extraction: each sloka is sent to Claude API which splits it into
individual if→then prediction rules. One rule per distinct astrological condition.

Rule ID:  R-BPHS{CHAPTER}-{INDEX:03d}
  source.sloka  tracks which sloka the rule came from.

Usage:
  python3 scripts/ingest_bphs_houses_v2.py \
    --rtf "~/Documents/Knowledge Engine_eBooks/BPHS Ch 13 Vol 1.rtf" \
    --house 2 --chapter 13 \
    --mongo-url "$MONGO_URL" --db-name EverydayHoroscope \
    [--dry-run]

Requires:
  ANTHROPIC_API_KEY set in environment
  pip install anthropic pydantic pymongo
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import anthropic
except ImportError:
    print("ERROR: pip install anthropic")
    sys.exit(1)

try:
    from pydantic import BaseModel
except ImportError:
    print("ERROR: pip install pydantic")
    sys.exit(1)

from pymongo import MongoClient

# ── Constants ──────────────────────────────────────────────────────────────────

SCIENCE = "vedic_astrology"
BOOK    = "Brihat Parashara Hora Shastra"
BOOK_ID = "bphs_vol1"

CHAPTER_NAMES: dict[int, str] = {
    12: "Effects of First House",    13: "Effects of Second House",
    14: "Effects of Third House",    15: "Effects of Fourth House",
    16: "Effects of Fifth House",    17: "Effects of Sixth House",
    18: "Effects of Seventh House",  19: "Effects of Eighth House",
    20: "Effects of Ninth House",    21: "Effects of Tenth House",
    22: "Effects of Eleventh House", 23: "Effects of Twelfth House",
}

HOUSE_LIFE_DOMAINS: dict[int, str] = {
    1: "health",        2: "wealth",
    3: "relationships", 4: "home",
    5: "children",      6: "health",
    7: "relationships", 8: "longevity",
    9: "fortune",       10: "career",
    11: "wealth",       12: "spirituality",
}

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
           "Saturn", "Rahu", "Ketu"]

VALID_SUB_TYPES = {
    "lord_placement", "planet_occupation", "aspect_rule",
    "combination", "birth_special", "general_principle",
}

SKIP_HEADINGS = {
    "decanates and bodily limbs", "decanates", "bodily limbs",
    "limbs", "center",
}

# ── Pydantic models ────────────────────────────────────────────────────────────

class ExtractedRule(BaseModel):
    condition_summary: str   # ≤20 words: the if-clause
    result_summary: str      # ≤20 words: the then-clause / outcome
    full_condition: str      # complete condition text
    full_result: str         # complete result/effect text
    sub_type: str            # lord_placement | planet_occupation | aspect_rule | combination | birth_special | general_principle
    planets: list[str]       # canonical planet names
    houses: list[int]        # house numbers as integers

class SlokaExtraction(BaseModel):
    rules: list[ExtractedRule]

# ── AI extraction prompts ──────────────────────────────────────────────────────

EXTRACTION_SYSTEM = """\
You are a Vedic astrology rule extractor working on BPHS (Brihat Parashara Hora Shastra).

Given a sloka (verse), extract each distinct astrological prediction rule as a separate
structured object. A prediction rule is a specific if→then statement:
  if [astrological condition] → then [life outcome or effect]

RULES:
1. Split compound slokas — each distinct condition→outcome pair is one rule.
2. "Or / alternatively" conditions yielding the SAME outcome = one rule (combine them).
3. Opposite outcomes from different conditions = separate rules.
   Example: "if lord in angle → wealth" and "if lord in 6th/8th/12th → poverty" = 2 rules.
4. Notes section: extract a new rule from Notes ONLY if it contains a genuinely distinct
   condition NOT already stated in the main sloka text. Notes are primarily commentary.
5. Keep condition and result text close to the original wording.
6. Canonical planet names: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu.
7. sub_type must be exactly one of:
   lord_placement    — about where a house lord is placed
   planet_occupation — about which planet occupies a house
   aspect_rule       — involves aspect or conjunction
   combination       — multi-planet yoga or special combination
   birth_special     — unusual birth circumstances (twins, coiled birth, etc.)
   general_principle — overarching principle not fitting above
"""

EXTRACTION_PROMPT = """\
Chapter {chapter} (House {house}), Sloka {sloka} — {heading}

Text:
{text}

Extract all distinct prediction rules.
"""


# ── AI Extractor ───────────────────────────────────────────────────────────────

class SlokaExtractor:
    def __init__(self, model: str = "claude-haiku-4-5"):
        self.model = model
        self._client: anthropic.Anthropic | None = None

    def _get_client(self) -> anthropic.Anthropic:
        if self._client is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError("ANTHROPIC_API_KEY not set in environment")
            self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    def extract(
        self,
        sloka_label: str,
        heading: str,
        rule_text: str,
        notes_text: str,
        chapter: int,
        house: int,
    ) -> list[ExtractedRule]:
        """Extract individual rules from a sloka. Returns empty list on failure."""
        full_text = rule_text
        if notes_text:
            full_text = rule_text + "\n\nNotes:\n" + notes_text.replace("Notes :", "").strip()

        prompt = EXTRACTION_PROMPT.format(
            chapter=chapter,
            house=house,
            sloka=sloka_label,
            heading=heading,
            text=full_text,
        )

        try:
            client = self._get_client()
            response = client.messages.parse(
                model=self.model,
                max_tokens=2048,
                temperature=0.1,
                system=[{
                    "type": "text",
                    "text": EXTRACTION_SYSTEM,
                    "cache_control": {"type": "ephemeral"},
                }],
                messages=[{"role": "user", "content": prompt}],
                output_format=SlokaExtraction,
            )
            return response.parsed_output.rules
        except Exception as e:
            print(f"⚠  AI extraction failed for sloka {sloka_label}: {e}")
            return []


# ── RTF parser (same fixed version as v1) ─────────────────────────────────────

def strip_rtf(raw: str) -> str:
    text = raw
    text = text.replace("\\'92", "'").replace("\\'93", '"').replace("\\'94", '"')
    text = text.replace("\\'b0", "°")
    text = re.sub(r"\\'[0-9a-f]{2}", '', text)
    text = re.sub(r'\\\n', '\n', text)
    text = re.sub(r'\\par\b\s*', '\n', text)
    text = re.sub(r'\\page\b\s*', '\n', text)
    text = re.sub(r'\\[a-z*]+\-?\d*\s?', ' ', text)
    text = re.sub(r'\\[^a-z\n]', '', text)
    text = re.sub(r'\\', '', text)
    text = text.replace('{', '').replace('}', '')
    lines = []
    for line in text.splitlines():
        line = re.sub(r'\s+', ' ', line).strip()
        if line and line != ';':
            lines.append(line)
    return '\n'.join(lines)


def neutralize_notes_lists(text: str) -> str:
    """
    Within Notes sections, replace numbered list items like '1. text' with
    '[1]. text' so the sloka regex won't treat them as sloka headings.

    A Notes section begins at a Notes marker.  Numbered items up to 9 that
    appear within 25 lines of the marker are treated as sub-list items and
    neutralized.  A larger number (or one appearing further away) is assumed
    to be a new real sloka, which exits the Notes context.
    """
    MAX_LIST_NUM    = 9
    MAX_NOTES_LINES = 25

    lines      = text.splitlines()
    notes_re   = re.compile(r'\bNotes?\s*[.,:\'"]\s*', re.IGNORECASE)
    list_re    = re.compile(r'^(\s*)(\d+)(\.\s+)')
    in_notes   = False
    notes_line = 0
    result     = []

    for i, line in enumerate(lines):
        if notes_re.search(line):
            in_notes   = True
            notes_line = i

        if in_notes:
            m = list_re.match(line)
            if m:
                num = int(m.group(2))
                gap = i - notes_line
                if num <= MAX_LIST_NUM and gap <= MAX_NOTES_LINES:
                    # Bracket the number so it won't match the sloka regex
                    line = list_re.sub(r'\1[\2]\3', line, count=1)
                else:
                    # Large number or far from Notes marker → real sloka
                    in_notes = False

        result.append(line)

    return '\n'.join(result)


def split_into_sloka_blocks(text: str) -> list[tuple[str, str]]:
    """
    Split plain text into (sloka_label, block_text) tuples.
    Handles:
      - Single slokas:  "5. HEADING .."
      - Sloka ranges:   "5-7. HEADING .."
      - OCR artefacts:  "l-2." parsed as "1-2."
      - Trailing alpha: "9-9t.", "10-13i."
      - No space after period: "3.EXCESSIVE/"
      - Leading quotes/apostrophes: "' 34. The native..."
    Notes sub-list items (1., 2., ...) are neutralized before matching.
    """
    # Normalise OCR artefacts: leading 'l' digit → '1'
    text = re.sub(r'(?m)^\s*l(?=[-\d.])', '1', text)

    # Neutralize numbered list items inside Notes sections
    text = neutralize_notes_lists(text)

    # Extended pattern handles:
    #   leading quotes/apostrophes, trailing alpha in numbers (9-9t, 10-13i),
    #   no space after period (3.EXCESSIVE), optional period (23 If...),
    #   heading must start uppercase to avoid false positives.
    sloka_re = re.compile(
        r"(?m)^[ \t'\"]*(\d+[a-z]?(?:\s*[-\u2013]\s*\d+[a-z]?)?)\.?\s*([A-Z].+)$"
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
        blocks.append((label, heading + " " + body))
    return blocks


def should_skip(text: str) -> bool:
    h = text.lower()
    for phrase in SKIP_HEADINGS:
        if phrase in h:
            return True
    if re.match(r'^(left|right)\s+(side|eye|ear|knee|calf|foot|thigh|arm|shoulder|neck)',
                h, re.IGNORECASE):
        return True
    return False


def clean_notes(text: str) -> tuple[str, str]:
    # Match "Notes :", "Notes .'", "Notes .", "Note :" etc.
    m = re.compile(r'\bNotes?\s*[.:\'"\s]', re.IGNORECASE).search(text)
    if m:
        return text[:m.start()].strip(), text[m.start():].strip()
    return text.strip(), ""


def extract_heading(text: str) -> str:
    m = re.match(r'^([A-Z][A-Z\s/()]+?)(?:\s*\.{2}|\s*[.;:\'"])', text)
    if m:
        return m.group(1).strip().title()
    return " ".join(text.split()[:5]).title()


# ── Rule builders ──────────────────────────────────────────────────────────────

def make_source(chapter: int, sloka: str, batch_id: str) -> dict:
    return {
        "book":           BOOK,
        "book_id":        BOOK_ID,
        "chapter":        str(chapter),
        "chapter_name":   CHAPTER_NAMES.get(chapter, f"Effects of House {chapter - 11}"),
        "sloka":          sloka,
        "batch_id":       batch_id,
        "primary":        BOOK,
        "page_ref":       None,
        "passage_ref_id": None,
    }


def extracted_to_rule(
    item: ExtractedRule,
    sloka_label: str,
    heading: str,
    house: int,
    chapter: int,
    batch_id: str,
    index: int,
) -> dict:
    rule_id     = f"R-BPHS{chapter}-{index:03d}"
    life_domain = HOUSE_LIFE_DOMAINS.get(house, "general")
    planets     = [p for p in item.planets if p in PLANETS]
    sub_type    = item.sub_type if item.sub_type in VALID_SUB_TYPES else "general_principle"

    detailed = f"Condition: {item.full_condition}\n\nEffect: {item.full_result}"
    summary  = f"{item.condition_summary} → {item.result_summary}"
    if len(summary) > 200:
        summary = summary[:197] + "..."

    houses_involved = list(dict.fromkeys([house] + [h for h in item.houses if isinstance(h, int)]))
    tags = ["verbatim", "bhava_combination", f"house{house}",
            f"chapter{chapter}", sub_type, "ai_extracted"]

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source":     make_source(chapter, sloka_label, batch_id),
        "condition": {
            "type":             "bhava_combination",
            "house":            house,
            "sub_type":         sub_type,
            "sloka":            sloka_label,
            "heading":          heading,
            "planets_involved": planets,
            "houses_involved":  houses_involved,
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
            "houses_involved":  houses_involved,
            "signs_involved":   [],
            "condition_count":  1,
        },
        "confidence": {
            "base":                  0.85,
            "source_weight":         0.95,
            "cross_book_multiplier": 1.0,
        },
        "approval_status": "pending_review",
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


def _fallback_rule(label: str, raw_text: str, house: int, chapter: int,
                   batch_id: str, index: int) -> dict | None:
    """Single-rule fallback when AI extraction returns nothing."""
    rule_text, notes_text = clean_notes(raw_text)
    if should_skip(rule_text) or len(rule_text.split()) < 6:
        return None
    heading  = extract_heading(rule_text)
    detailed = rule_text
    if notes_text:
        detailed = rule_text + "\n\nNotes: " + notes_text.replace("Notes :", "").strip()
    summary = rule_text.split(".")[0].strip()[:200]
    planets = [p for p in PLANETS if re.search(rf'\b{p}\b', raw_text, re.IGNORECASE)]
    return {
        "rule_id":    f"R-BPHS{chapter}-{index:03d}",
        "science_id": SCIENCE,
        "source":     make_source(chapter, label, batch_id),
        "condition": {
            "type": "bhava_combination", "house": house,
            "sub_type": "general_principle", "sloka": label,
            "heading": heading, "planets_involved": planets,
            "houses_involved": [house], "sub_conditions": [], "operator": "and",
        },
        "interpretation": {
            "summary": summary, "detailed": detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies": [], "life_domain": HOUSE_LIFE_DOMAINS.get(house, "general"),
            "tags": ["verbatim", "bhava_combination", f"house{house}", f"chapter{chapter}"],
        },
        "metadata": {
            "planets_involved": planets, "houses_involved": [house],
            "signs_involved": [], "condition_count": 1,
        },
        "confidence": {"base": 0.82, "source_weight": 0.95, "cross_book_multiplier": 1.0},
        "approval_status": "pending_review",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def parse_rtf_file(
    rtf_path: str,
    house: int,
    chapter: int,
    batch_id: str,
    extractor: SlokaExtractor,
) -> list[dict]:
    raw    = Path(rtf_path).expanduser().read_text(encoding="utf-8", errors="replace")
    plain  = strip_rtf(raw)
    blocks = split_into_sloka_blocks(plain)

    rules: list[dict] = []
    idx   = 1
    total = len(blocks)

    for i, (label, text) in enumerate(blocks, 1):
        rule_text, notes_text = clean_notes(text)
        heading = extract_heading(rule_text)

        if should_skip(rule_text) or len(rule_text.split()) < 6:
            print(f"  [{i:2d}/{total}] Sloka {label:6s} — skipped")
            continue

        print(f"  [{i:2d}/{total}] Sloka {label:6s} extracting...", end=" ", flush=True)
        extracted = extractor.extract(label, heading, rule_text, notes_text, chapter, house)

        if extracted:
            batch = [extracted_to_rule(item, label, heading, house, chapter, batch_id, idx + j)
                     for j, item in enumerate(extracted)]
            print(f"{len(batch)} rule(s)")
            rules.extend(batch)
            idx += len(batch)
        else:
            # Fallback to single-rule
            fallback = _fallback_rule(label, text, house, chapter, batch_id, idx)
            if fallback:
                print("1 rule (fallback)")
                rules.append(fallback)
                idx += 1
            else:
                print("skipped (fallback)")

    return rules


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Ingest BPHS house-effects chapter with AI sub-condition extraction"
    )
    parser.add_argument("--rtf",       required=True)
    parser.add_argument("--house",     required=True, type=int,
                        choices=range(1, 13), metavar="HOUSE")
    parser.add_argument("--chapter",   required=True, type=int,
                        choices=range(12, 24), metavar="CHAPTER")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   required=True)
    parser.add_argument("--model",     default="claude-haiku-4-5",
                        help="Claude model for extraction (default: claude-haiku-4-5)")
    parser.add_argument("--dry-run",   action="store_true",
                        help="Print rules but do NOT write to MongoDB")
    args = parser.parse_args()

    batch_id  = f"bphs-ch{args.chapter}-v2-{datetime.now(timezone.utc).strftime('%Y%m%d')}"
    chap_name = CHAPTER_NAMES.get(args.chapter, f"Effects of House {args.house}")

    print(f"\nBPHS Chapter {args.chapter} — {chap_name}  [v2 AI extraction]")
    print(f"House {args.house}  |  model: {args.model}  |  batch_id: {batch_id}")
    print("─" * 60)

    extractor = SlokaExtractor(model=args.model)
    rules     = parse_rtf_file(args.rtf, args.house, args.chapter, batch_id, extractor)

    if not rules:
        print("\n⚠  No rules extracted. Check RTF path and ANTHROPIC_API_KEY.")
        return

    # Summary by sub_type
    sub_types: dict[str, int] = {}
    for r in rules:
        st = r["condition"]["sub_type"]
        sub_types[st] = sub_types.get(st, 0) + 1
    print()
    for st, count in sorted(sub_types.items(), key=lambda x: -x[1]):
        print(f"  {st:<25} : {count}")
    print(f"  {'─' * 33}")
    print(f"  {'TOTAL':<25} : {len(rules)}")
    print(f"\n  Isolation: approval_status='pending_review' — zero rules reach live users")

    if args.dry_run:
        print("\n[DRY RUN] — no changes written to MongoDB")
        print("\nSample rules:")
        for r in rules[:6]:
            c = r["condition"]
            print(f"\n  {r['rule_id']}")
            print(f"    sloka    : {c['sloka']}")
            print(f"    sub_type : {c['sub_type']}")
            print(f"    summary  : {r['interpretation']['summary'][:100]}")
        return

    # Insert
    client = MongoClient(args.mongo_url)
    db     = client[args.db_name]
    col    = db["interpretation_rules"]

    existing = col.count_documents({"source.batch_id": batch_id})
    if existing:
        print(f"\n⚠  Batch '{batch_id}' already has {existing} rules in MongoDB.")
        print("   Delete those documents first, then re-run.")
        client.close()
        return

    result = col.insert_many(rules, ordered=False)
    print(f"\n✅  Inserted {len(result.inserted_ids)} rules into MongoDB")
    print(f"   batch_id : {batch_id}")
    print(f"\n   Validate with:")
    print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
    print(f"     --db-name {args.db_name} --batch-id {batch_id}")
    client.close()


if __name__ == "__main__":
    main()
