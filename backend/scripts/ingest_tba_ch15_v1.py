#!/usr/bin/env python3
"""
ingest_tba_ch15_v1.py

A Text-Book of Astrology — Chapter 15:
"Planets in Different Houses: Prediction"

Two content sections in one chapter:

  Part 1 — Planets in Houses (72 blocks):
    Organised as Planet × House (Sun, Moon, Mars, Mercury, Jupiter, Venus × 12 houses).
    Each block has a general predictions paragraph + "In female horoscope:" sub-section
    + embedded IF conditions.
    Extraction unit: Planet × House block.

  Part 2 — Result of Planets in 12 Signs (108 entries):
    Organised as Planet × Sign (all 9 planets × 12 signs).
    Each entry is one descriptive rule: "IF [Planet] in [Sign]: then [traits]".
    Extraction unit: one API call per planet (12 signs batched together).

Rule ID   :  R-TBA15-{INDEX:03d}
Batch ID  :  tba-ch15-v1-YYYYMMDD
source.sloka: "<Planet>-H<NN>" for house blocks; "<Planet>-S" for sign groups

Usage:
    python3 scripts/ingest_tba_ch15_v1.py \\
        --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/Planets Ch 15- Textbook.rtf" \\
        --mongo-url "$MONGO_URL" --db-name horoscope_db \\
        [--dry-run] [--part {1,2,both}] [--model claude-haiku-4-5]

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

SCIENCE   = "vedic_astrology"
BOOK      = "A Text-Book of Astrology"
BOOK_ID   = "tba_ch15"
CHAPTER   = "15"
CHAP_NAME = "Planets in Different Houses: Prediction"

HOUSE_WORDS: dict[str, int] = {
    "First": 1, "Second": 2, "Third": 3, "Fourth": 4,
    "Fifth": 5, "Sixth": 6, "Seventh": 7, "Eighth": 8,
    "Ninth": 9, "Tenth": 10, "Eleventh": 11, "Twelfth": 12,
}

ORDINAL: dict[int, str] = {
    1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th",
    7: "7th", 8: "8th", 9: "9th", 10: "10th", 11: "11th", 12: "12th",
}

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
           "Saturn", "Rahu", "Ketu"]
PLANET_SET = set(p.lower() for p in PLANETS)

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

HOUSE_DOMAINS: dict[int, str] = {
    1: "health", 2: "wealth", 3: "relationships", 4: "home",
    5: "children", 6: "health", 7: "relationships", 8: "longevity",
    9: "fortune", 10: "career", 11: "wealth", 12: "spirituality",
}

VALID_SUB_TYPES = {
    "planet_occupation",  # planet in house → general effects
    "sign_placement",     # planet in sign → effects (Part 2 or embedded IF in sign)
    "aspect_rule",        # IF aspected by benefic/malefic
    "combination",        # IF conjunct/with another planet (simultaneous)
    "conditional_rule",   # IF [dignity: debilitated/exalted/own sign/weak/strong] → effect
    "general_principle",  # grouped paragraph description
}

# ── Pydantic models ────────────────────────────────────────────────────────────

class ExtractedRule(BaseModel):
    condition_summary: str    # ≤20 words: the if-clause
    result_summary: str       # ≤20 words: the then-clause / outcome
    full_condition: str       # complete condition text
    full_result: str          # complete result/effect text
    sub_type: str             # one of VALID_SUB_TYPES
    planets: list[str]        # other canonical planet names mentioned
    houses: list[int]         # house numbers mentioned
    gender: str               # "neutral" | "female"
    is_group_summary: bool    # True = main paragraph grouped-description rule

class BlockExtraction(BaseModel):
    rules: list[ExtractedRule]

# ── AI prompts ─────────────────────────────────────────────────────────────────

HOUSE_SYSTEM = """\
You are a Vedic astrology rule extractor working on "A Text-Book of Astrology", Chapter 15.

Each block describes effects of a PLANET placed in a specific HOUSE.
The block has two sub-sections:
  1. GENERAL TEXT  — applies to all genders (gender = "neutral")
  2. IN FEMALE HOROSCOPE — applies only to female nativity (gender = "female")

For each sub-section, extract TWO layers:

  LAYER 1 — GROUPED DESCRIPTION RULE (is_group_summary = true):
    Summarise the general trait paragraph (the non-IF sentences) as one single rule.
    sub_type = "planet_occupation", gender = "neutral" or "female" accordingly.
    full_condition = "[Planet] in [N]th House"
    This captures the full range of effects in a compact summary.
    Skip this layer if the sub-section has no general trait text (only IF conditions).

  LAYER 2 — INDIVIDUAL IF RULES (is_group_summary = false):
    Each embedded "IF [condition] → [outcome]" = ONE rule. gender = same as its sub-section.

sub_type values:
  planet_occupation — default for planet-in-house effects
  sign_placement    — IF planet is in a specific zodiac sign → effect
  aspect_rule       — IF aspected by benefic/malefic
  combination       — IF conjunct/with another planet (simultaneous conjunction)
  conditional_rule  — IF debilitated / exalted / own sign / weak / strong / combust
  general_principle — grouped/overarching rules not fitting above

SPLITTING GUIDANCE:
A. Sign lists:  "IF in Taurus, Scorpio or Aquarius" → ONE rule per sign (sign_placement)
   ALSO produce one grouped rule for all three signs together.
B. Dignity alternatives: "IF exalted or in own sign" → TWO rules (exalted; own sign).
C. Planet conjunctions: "IF with Saturn and Moon" = ONE combination rule (simultaneous).
D. Alternative planets: "IF with Venus or Mars" = TWO rules (with Venus; with Mars).
E. Female IF conditions: separate rules, gender = "female".

IMPORTANT:
- Canonical planet names: Sun Moon Mars Mercury Jupiter Venus Saturn Rahu Ketu
- gender must be exactly "neutral" or "female" — no other values
- is_group_summary = true ONLY for the main paragraph grouped description rule
- Keep condition and result text close to the original wording
"""

HOUSE_PROMPT = """\
Planet: {planet}
House: {ordinal} House
Source: A Text-Book of Astrology, Chapter 15

GENERAL TEXT (gender = neutral):
{general_text}

IN FEMALE HOROSCOPE (gender = female):
{female_text}

Extract all prediction rules from both sections.
"""

SIGN_SYSTEM = """\
You are a Vedic astrology rule extractor working on "A Text-Book of Astrology", Chapter 15,
Part 2: "Result of Planets in 12 Signs".

Each entry describes a PLANET in one ZODIAC SIGN. Format:
  "IF [Planet] in [Sign] Sign: then the native is [traits]..."

Extract EXACTLY ONE rule per entry with:
  sub_type = "sign_placement"
  gender = "neutral"
  is_group_summary = false
  condition_summary = "[Planet] in [Sign]"
  result_summary = first ≤20 words of the traits
  full_condition = "[Planet] in [Sign] Sign"
  full_result = complete traits text (verbatim from entry)
  planets = any OTHER planets explicitly mentioned in the traits (usually empty)
  houses = []

Canonical planet names: Sun Moon Mars Mercury Jupiter Venus Saturn Rahu Ketu
Canonical sign names: Aries Taurus Gemini Cancer Leo Virgo Libra Scorpio
                      Sagittarius Capricorn Aquarius Pisces
"""

SIGN_PROMPT = """\
Planet: {planet}

Sign entries (extract one rule per entry):

{entries}
"""

# ── AI Extractor ───────────────────────────────────────────────────────────────

class Extractor:
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

    def house_block(
        self,
        planet: str,
        house_num: int,
        general_text: str,
        female_text: str,
    ) -> list[ExtractedRule]:
        ordinal = ORDINAL[house_num]
        prompt = HOUSE_PROMPT.format(
            planet=planet,
            ordinal=ordinal,
            general_text=general_text.strip() or "(no general text)",
            female_text=female_text.strip() or "(no female horoscope text)",
        )
        try:
            resp = self._get_client().messages.parse(
                model=self.model,
                max_tokens=4096,
                temperature=0,
                system=[{
                    "type": "text",
                    "text": HOUSE_SYSTEM,
                    "cache_control": {"type": "ephemeral"},
                }],
                messages=[{"role": "user", "content": prompt}],
                output_format=BlockExtraction,
            )
            return resp.parsed_output.rules
        except Exception as e:
            print(f"\n  ⚠  AI extraction failed: {e}")
            return []

    def sign_group(
        self,
        planet: str,
        entries: list[tuple[str, str]],
    ) -> list[ExtractedRule]:
        """Extract sign-placement rules for all 12 signs in one API call."""
        lines = "\n".join(
            f"IF {planet} in {sign} Sign: {text}"
            for sign, text in entries
        )
        prompt = SIGN_PROMPT.format(planet=planet, entries=lines)
        try:
            resp = self._get_client().messages.parse(
                model=self.model,
                max_tokens=4096,
                temperature=0,
                system=[{
                    "type": "text",
                    "text": SIGN_SYSTEM,
                    "cache_control": {"type": "ephemeral"},
                }],
                messages=[{"role": "user", "content": prompt}],
                output_format=BlockExtraction,
            )
            return resp.parsed_output.rules
        except Exception as e:
            print(f"\n  ⚠  AI extraction failed: {e}")
            return []


# ── RTF parser ─────────────────────────────────────────────────────────────────

def strip_rtf(raw: str) -> str:
    text = raw
    text = text.replace("\\'92", "'").replace("\\'93", '"').replace("\\'94", '"')
    text = text.replace("\\'b0", "°").replace("\\'a0", " ")
    text = re.sub(r"\\'[0-9a-f]{2}", "", text)
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
        lines.append(line)    # keep blank lines as paragraph separators
    return '\n'.join(lines)


def join_colon_continuations(text: str) -> str:
    """
    RTF splits bold heading and body at font-change points.
    Part 2 entries appear as two lines:
      "IF Sun is placed in Aries Sign"
      ": then the native is..."
    Join lines that start with ':' into the preceding line.
    """
    lines = text.splitlines()
    result: list[str] = []
    for line in lines:
        stripped = line.strip()
        if result and stripped.startswith(':'):
            result[-1] = result[-1].rstrip() + stripped
        else:
            result.append(line)
    return '\n'.join(result)


# Heading detection regexes
PLANET_RE = re.compile(
    r'^(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)$',
    re.IGNORECASE,
)
HOUSE_RE = re.compile(
    r'^(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth)\s+House$',
    re.IGNORECASE,
)
FEMALE_RE = re.compile(r'^In\s+female\s+horoscope\s*[:\s]', re.IGNORECASE)
PART2_RE  = re.compile(r'Result\s+of\s+Planets\s+in\s+12\s+Signs', re.IGNORECASE)

# Part 2 sign entry — handles split-line variant after join_colon_continuations
SIGN_ENTRY_RE = re.compile(
    r'IF\s+\w+\s+(?:is\s+placed\s+in|in)\s+'
    r'(Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|'
    r'Sagittarius|Capricorn|Aquarius|Pisces)\s+Sign\s*:?\s*'
    r'(?:then\s+)?(.+)',
    re.IGNORECASE,
)


def parse_rtf(rtf_path: str) -> tuple[
    list[tuple[str, int, str, str]],      # Part 1: (planet, house_num, general, female)
    dict[str, list[tuple[str, str]]],     # Part 2: planet → [(sign, text), ...]
]:
    """Parse the RTF file into structured blocks for both parts."""
    raw   = Path(rtf_path).expanduser().read_text(encoding="utf-8", errors="replace")
    plain = strip_rtf(raw)
    plain = join_colon_continuations(plain)
    lines = plain.splitlines()

    house_blocks: list[tuple[str, int, str, str]] = []
    sign_groups: dict[str, list[tuple[str, str]]] = {}

    # ── State ──────────────────────────────────────────────────────────────────
    in_part2        = False
    cur_planet: str | None  = None
    cur_house: int | None   = None
    general_lines: list[str] = []
    female_lines: list[str]  = []
    in_female               = False

    def flush_house_block() -> None:
        nonlocal general_lines, female_lines, in_female
        if cur_planet and cur_house is not None:
            gen = " ".join(l for l in general_lines if l).strip()
            fem = " ".join(l for l in female_lines  if l).strip()
            if gen or fem:
                house_blocks.append((cur_planet, cur_house, gen, fem))
        general_lines.clear()
        female_lines.clear()
        in_female = False

    for line in lines:
        line_s = line.strip()

        # ── Detect Part 2 section start ────────────────────────────────────────
        if PART2_RE.search(line_s):
            flush_house_block()
            in_part2   = True
            cur_planet = None
            cur_house  = None
            continue

        # ── Part 2: Planet × Sign ──────────────────────────────────────────────
        if in_part2:
            pm = PLANET_RE.match(line_s)
            if pm:
                cur_planet = pm.group(1).capitalize()
                if cur_planet not in sign_groups:
                    sign_groups[cur_planet] = []
                continue

            sm = SIGN_ENTRY_RE.search(line_s)
            if sm and cur_planet:
                sign     = sm.group(1).capitalize()
                raw_text = sm.group(2).strip()
                # Normalise "the native is X" prefix
                raw_text = re.sub(r'^the\s+native\s+is\s+', 'The native is ', raw_text, flags=re.IGNORECASE)
                sign_groups[cur_planet].append((sign, raw_text))
            continue

        # ── Part 1: Planet × House ─────────────────────────────────────────────

        # Planet heading
        pm = PLANET_RE.match(line_s)
        if pm:
            flush_house_block()
            cur_planet = pm.group(1).capitalize()
            cur_house  = None
            continue

        # House heading
        hm = HOUSE_RE.match(line_s)
        if hm:
            flush_house_block()
            word      = hm.group(1).capitalize()
            cur_house = HOUSE_WORDS.get(word)
            continue

        # Female sub-section marker
        if FEMALE_RE.match(line_s):
            in_female = True
            remainder = FEMALE_RE.sub("", line_s).strip().lstrip(":").strip()
            if remainder:
                female_lines.append(remainder)
            continue

        # Accumulate text
        if cur_planet and cur_house is not None:
            if in_female:
                female_lines.append(line_s)
            else:
                general_lines.append(line_s)

    flush_house_block()   # flush final block
    return house_blocks, sign_groups


# ── Rule builders ──────────────────────────────────────────────────────────────

def _punct(s: str) -> str:
    s = s.strip()
    return s if (s and s[-1] in '.!?"\'') else s + '.'


def _canon_planets(raw: list[str]) -> list[str]:
    """Return only canonical planet names from a list."""
    lookup = {p.lower(): p for p in PLANETS}
    return [lookup[p.lower()] for p in raw if p.lower() in lookup]


def build_house_rule(
    item: ExtractedRule,
    planet: str,
    house_num: int,
    batch_id: str,
    index: int,
) -> dict:
    ordinal    = ORDINAL[house_num]
    block_lbl  = f"{planet}-H{house_num:02d}"
    rule_id    = f"R-TBA15-{index:03d}"
    sub_type   = item.sub_type if item.sub_type in VALID_SUB_TYPES else "planet_occupation"
    planets_in = _canon_planets(item.planets)
    houses_in  = list(dict.fromkeys([house_num] + [h for h in item.houses if isinstance(h, int)]))

    # Auto-generate condition_group_id from structural context (planet × house × gender).
    # All rules from the same block and gender share this ID — both the grouped-description
    # rule (is_group_summary=True) AND every individual IF rule (is_group_summary=False).
    # Format mirrors BPHS pattern: "tba15-{planet}-h{N}-{gender}"
    gender_key       = item.gender if item.gender in ("neutral", "female") else "neutral"
    condition_group_id = f"tba15-{planet.lower()}-h{house_num:02d}-{gender_key}"

    detailed = f"Condition: {_punct(item.full_condition)}\n\nEffect: {_punct(item.full_result)}"
    summary  = f"{item.condition_summary} → {_punct(item.result_summary)}"
    if len(summary) > 200:
        summary = summary[:197] + "..."

    tags = ["verbatim", "planet_occupation", f"house{house_num}",
            f"chapter{CHAPTER}", sub_type, "ai_extracted",
            f"group:{condition_group_id}"]          # on ALL rules — enables group queries
    if item.gender == "female":
        tags.append("female_horoscope")
    if item.is_group_summary:
        tags.append("group_summary")               # only on the grouped-description rule

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source": {
            "book":           BOOK,
            "book_id":        BOOK_ID,
            "chapter":        CHAPTER,
            "chapter_name":   CHAP_NAME,
            "sloka":          block_lbl,
            "batch_id":       batch_id,
            "primary":        BOOK,
            "page_ref":       None,
            "passage_ref_id": None,
        },
        "condition": {
            "type":               "planet_occupation",
            "planet":             planet,
            "house":              house_num,
            "sub_type":           sub_type,
            "sloka":              block_lbl,
            "heading":            f"{planet} in {ordinal} House",
            "planets_involved":   [planet] + planets_in,
            "houses_involved":    houses_in,
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     gender_key,
            "condition_group_id": condition_group_id,
            "is_group_summary":   item.is_group_summary,
        },
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        HOUSE_DOMAINS.get(house_num, "general"),
            "tags":               tags,
        },
        "metadata": {
            "planets_involved":   [planet] + planets_in,
            "houses_involved":    houses_in,
            "signs_involved":     [],
            "condition_count":    1,
            "gender_context":     gender_key,
            "condition_group_id": condition_group_id,
            "is_group_summary":   item.is_group_summary,
        },
        "confidence": {
            "base": 0.85, "source_weight": 0.90, "cross_book_multiplier": 1.0,
        },
        "approval_status": "pending_review",
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


def build_sign_rule(
    item: ExtractedRule,
    planet: str,
    batch_id: str,
    index: int,
) -> dict:
    # Determine sign from full_condition
    sign_m = re.search(
        r'\b(Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|'
        r'Sagittarius|Capricorn|Aquarius|Pisces)\b',
        item.full_condition, re.IGNORECASE,
    )
    sign      = sign_m.group(1).capitalize() if sign_m else "Unknown"
    block_lbl = f"{planet}-S-{sign}"
    rule_id   = f"R-TBA15-{index:03d}"
    sub_type  = "sign_placement"
    planets_in = _canon_planets(item.planets)

    detailed = f"Condition: {_punct(item.full_condition)}\n\nEffect: {_punct(item.full_result)}"
    summary  = f"{item.condition_summary} → {_punct(item.result_summary)}"
    if len(summary) > 200:
        summary = summary[:197] + "..."

    tags = ["verbatim", "sign_placement", f"chapter{CHAPTER}", "ai_extracted"]

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source": {
            "book":           BOOK,
            "book_id":        BOOK_ID,
            "chapter":        CHAPTER,
            "chapter_name":   CHAP_NAME,
            "sloka":          block_lbl,
            "batch_id":       batch_id,
            "primary":        BOOK,
            "page_ref":       None,
            "passage_ref_id": None,
        },
        "condition": {
            "type":             "sign_placement",
            "planet":           planet,
            "sign":             sign,
            "house":            None,
            "sub_type":         sub_type,
            "sloka":            block_lbl,
            "heading":          f"{planet} in {sign}",
            "planets_involved": [planet] + planets_in,
            "houses_involved":  [],
            "sub_conditions":   [],
            "operator":         "and",
            "gender_context":   "neutral",
            "is_group_summary": False,
        },
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        "general",
            "tags":               tags,
        },
        "metadata": {
            "planets_involved": [planet] + planets_in,
            "houses_involved":  [],
            "signs_involved":   [sign],
            "condition_count":  1,
            "gender_context":   "neutral",
            "is_group_summary": False,
        },
        "confidence": {
            "base": 0.85, "source_weight": 0.90, "cross_book_multiplier": 1.0,
        },
        "approval_status": "pending_review",
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest A Text-Book of Astrology Ch 15 — Planets in Houses & Signs"
    )
    parser.add_argument("--rtf",       required=True, help="Path to the RTF file")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   required=True)
    parser.add_argument("--model",     default="claude-haiku-4-5",
                        help="Claude model for extraction (default: claude-haiku-4-5)")
    parser.add_argument("--dry-run",   action="store_true",
                        help="Print summary but do NOT write to MongoDB")
    parser.add_argument("--part",      choices=["1", "2", "both"], default="both",
                        help="Which content part to ingest (default: both)")
    args = parser.parse_args()

    batch_id = f"tba-ch15-v1-{datetime.now(timezone.utc).strftime('%Y%m%d')}"

    print(f"\nA Text-Book of Astrology — Chapter 15  [v1 AI extraction]")
    print(f"Model : {args.model}  |  batch_id : {batch_id}  |  Part : {args.part}")
    print(f"{'─' * 65}")

    # ── Parse RTF ──────────────────────────────────────────────────────────────
    print("\nParsing RTF...")
    house_blocks, sign_groups = parse_rtf(args.rtf)
    print(f"  Part 1 (Planet × House) : {len(house_blocks):3d} blocks detected")
    sign_total = sum(len(v) for v in sign_groups.values())
    print(f"  Part 2 (Planet × Sign)  : {sign_total:3d} sign entries detected "
          f"({len(sign_groups)} planets)")

    if not house_blocks and args.part in ("1", "both"):
        print("\n⚠  No house blocks detected — check RTF path and parser.")

    extractor  = Extractor(model=args.model)
    all_rules: list[dict] = []
    idx = 1

    # ── Part 1: Planet × House ─────────────────────────────────────────────────
    if args.part in ("1", "both"):
        print(f"\n── Part 1: Planets in Houses ({len(house_blocks)} blocks) ──")
        for planet, house_num, general_text, female_text in house_blocks:
            label = f"{planet}-H{house_num:02d}"
            print(f"  {label:15s} extracting...", end=" ", flush=True)
            extracted = extractor.house_block(planet, house_num, general_text, female_text)
            if extracted:
                batch = [
                    build_house_rule(r, planet, house_num, batch_id, idx + j)
                    for j, r in enumerate(extracted)
                ]
                # Quick sub_type audit
                neutral_grp = sum(1 for r in extracted if r.is_group_summary and r.gender == "neutral")
                female_grp  = sum(1 for r in extracted if r.is_group_summary and r.gender == "female")
                if_rules    = sum(1 for r in extracted if not r.is_group_summary)
                print(f"{len(batch):2d} rules  "
                      f"[grp:{neutral_grp}  f-grp:{female_grp}  IF:{if_rules}]")
                all_rules.extend(batch)
                idx += len(batch)
            else:
                print("⚠  failed")

    # ── Part 2: Planet × Sign ──────────────────────────────────────────────────
    if args.part in ("2", "both"):
        print(f"\n── Part 2: Planets in Signs ({len(sign_groups)} planets) ──")
        for planet in PLANETS:   # iterate in canonical order
            if planet not in sign_groups:
                continue
            entries = sign_groups[planet]
            print(f"  {planet:10s} ({len(entries):2d} signs) extracting...", end=" ", flush=True)
            extracted = extractor.sign_group(planet, entries)
            if extracted:
                batch = [
                    build_sign_rule(r, planet, batch_id, idx + j)
                    for j, r in enumerate(extracted)
                ]
                print(f"{len(batch):2d} rules")
                all_rules.extend(batch)
                idx += len(batch)
            else:
                print("⚠  failed")

    # ── Summary ────────────────────────────────────────────────────────────────
    if not all_rules:
        print("\n⚠  No rules extracted. Check RTF path and ANTHROPIC_API_KEY.")
        return

    sub_types: dict[str, int] = {}
    genders: dict[str, int] = {"neutral": 0, "female": 0}
    group_count = 0
    for r in all_rules:
        st = r["condition"]["sub_type"]
        sub_types[st] = sub_types.get(st, 0) + 1
        gc = r["condition"].get("gender_context", "neutral")
        genders[gc] = genders.get(gc, 0) + 1
        if r["condition"].get("is_group_summary"):
            group_count += 1

    print(f"\n{'─' * 65}")
    print("Sub-type breakdown:")
    for st, cnt in sorted(sub_types.items(), key=lambda x: -x[1]):
        print(f"  {st:<22s} : {cnt}")
    print(f"  {'─' * 30}")
    print(f"  {'TOTAL':<22s} : {len(all_rules)}")
    print(f"\nGroup summary rules  : {group_count}")
    print(f"Neutral (all)        : {genders.get('neutral', 0)}")
    print(f"Female horoscope     : {genders.get('female', 0)}")
    print(f"\nIsolation: approval_status='pending_review' — zero rules reach live users")

    if args.dry_run:
        print("\n[DRY RUN] — no changes written to MongoDB")
        print("\nSample rules (first 6):")
        for r in all_rules[:6]:
            c = r["condition"]
            print(f"\n  {r['rule_id']}")
            print(f"    sloka       : {c['sloka']}")
            print(f"    sub_type    : {c['sub_type']}")
            print(f"    gender      : {c.get('gender_context', '—')}")
            print(f"    group_summ  : {c.get('is_group_summary', False)}")
            print(f"    summary     : {r['interpretation']['summary'][:100]}")
        return

    # ── Insert into MongoDB ────────────────────────────────────────────────────
    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]

    existing = col.count_documents({"source.batch_id": batch_id})
    if existing:
        print(f"\n⚠  Batch '{batch_id}' already has {existing} rules in MongoDB.")
        print("   Delete those documents first, then re-run.")
        client.close()
        return

    result = col.insert_many(all_rules, ordered=False)
    print(f"\n✅  Inserted {len(result.inserted_ids)} rules into MongoDB")
    print(f"   batch_id : {batch_id}")
    print(f"\n   Validate with:")
    print(f"   python3 scripts/validate_rules.py --mongo-url $MONGO_URL \\")
    print(f"     --db-name {args.db_name} --batch-id {batch_id}")
    client.close()


if __name__ == "__main__":
    main()
