#!/usr/bin/env python3
"""
BPHS Vol 2 — Effects of Dasas (Chapters 47, 48, 52-60)
ingest_bphs_dasha_v1.py

AI-assisted extraction: each sloka group is sent to Claude API which splits it into
individual if→then prediction rules. One rule per distinct astrological condition.

Supports three chapter types:
  Ch 47   — dasha_planet  : per-planet Mahadasha effects (condition = planet + dignity/placement)
  Ch 48   — dasha_of_house_lord : Dasha of lord of each house
  Ch 52-60 — antardasha   : Mahadasha × Antardasha sub-period effects

Rule ID:  R-BPHS{CHAPTER}-{INDEX:03d}
  source.sloka  tracks which sloka the rule came from.

Usage (Ch 47):
  python3 scripts/ingest_bphs_dasha_v1.py \
    --rtf "~/Documents/Knowledge Engine_eBooks/BPHS Ch 47 Vol 2.rtf" \
    --chapter 47 \
    --mongo-url "$MONGO_URL" --db-name EverydayHoroscope \
    [--dry-run]

Usage (Ch 52, Saturn Mahadasha):
  python3 scripts/ingest_bphs_dasha_v1.py \
    --rtf "..." --chapter 52 --dasha-lord Sun \
    --mongo-url "$MONGO_URL" --db-name EverydayHoroscope

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
BOOK_ID = "bphs_vol2"

CHAPTER_NAMES: dict[int, str] = {
    47: "Effects of Dasas",
    48: "Dasas of Lords of Various Houses",
    52: "Antardasha in Sun Mahadasha",
    53: "Antardasha in Moon Mahadasha",
    54: "Antardasha in Mars Mahadasha",
    55: "Antardasha in Rahu Mahadasha",
    56: "Antardasha in Jupiter Mahadasha",
    57: "Antardasha in Saturn Mahadasha",
    58: "Antardasha in Mercury Mahadasha",
    59: "Antardasha in Ketu Mahadasha",
    60: "Antardasha in Venus Mahadasha",
}

# Ch 52-60: which Mahadasha lord each chapter covers
ANTARDASHA_CHAPTER_LORD: dict[int, str] = {
    52: "Sun", 53: "Moon", 54: "Mars",   55: "Rahu",
    56: "Jupiter", 57: "Saturn", 58: "Mercury", 59: "Ketu", 60: "Venus",
}

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
           "Saturn", "Rahu", "Ketu"]

# Patterns to detect which planet's Dasha section we're in.
# Multiple patterns needed because Ch 47 uses several heading forms:
#   "Effects of the Sun's Vimsottari Dasa"  (possessive, planet before Dasa)
#   "Effects of the Vimsottari Dasa of the Moon"  (planet after "Dasa of")
#   "effects of the Dasa of Jupiter"  (short form)
#   "Dasa of Saturn"  (bare reference in transition slokas)
_PLANET_SECTION_PATTERNS = [
    re.compile(r"Effects\s+of\s+(?:the\s+)?(\w+)'s\s+(?:Vimsottari\s+)?Dasa",        re.IGNORECASE),
    re.compile(r"Effects\s+of\s+(?:the\s+)?(?:Vimsottari\s+)?Dasa\s+of\s+(?:the\s+)?(\w+)", re.IGNORECASE),
    re.compile(r"Dasa\s+of\s+(?:the\s+)?(\w+)",                                       re.IGNORECASE),
]

# Transition phrases like "I will now come to the effects of the Dasa of the Moon"
# that mark a forward shift to a NEW planet's section within the same sloka.
# These override the position-map result for that sloka.
_TRANSITION_RE = re.compile(
    r'(?:will\s+now\s+(?:come\s+to|describe)|going\s+to\s+describe|now\s+describe)'
    r'.{0,60}'
    r'(?:Vimsottari\s+)?Dasa\s+of\s+(?:the\s+)?(\w+)',
    re.IGNORECASE,
)

def detect_transition_planet(text: str) -> str | None:
    """
    Detect the forward-looking planet in transition slokas like:
    'after describing the Sun Dasa in brief, I will now come to the effects of
     the Vimsottari Dasa of the Moon.'
    Returns the NEW planet (Moon) not the old one (Sun).
    """
    m = _TRANSITION_RE.search(text[:500])
    if m:
        name = m.group(1).strip().title()
        if name in PLANETS:
            return name
    return None

VALID_SUB_TYPES = {
    "dasha_favourable", "dasha_unfavourable", "dasha_conditional",
    "dasha_remedy", "general_principle",
}

# ── Pydantic models ────────────────────────────────────────────────────────────

class ExtractedRule(BaseModel):
    condition_summary: str   # ≤20 words: the if-clause
    result_summary: str      # ≤20 words: the then-clause / outcome
    full_condition: str      # complete condition text
    full_result: str         # complete result/effect text
    sub_type: str            # dasha_favourable | dasha_unfavourable | dasha_conditional | dasha_remedy | general_principle
    planets: list[str]       # canonical planet names involved
    houses: list[int]        # house numbers mentioned

class SlokaExtraction(BaseModel):
    rules: list[ExtractedRule]


class HouseLordExtractedRule(BaseModel):
    condition_summary: str   # ≤20 words: the if-clause
    result_summary: str      # ≤20 words: the then-clause / outcome
    full_condition: str      # complete condition text
    full_result: str         # complete result/effect text
    sub_type: str            # dasha_favourable | dasha_unfavourable | dasha_conditional | dasha_remedy | general_principle
    planets: list[str]       # canonical planet names involved
    houses: list[int]        # all house numbers mentioned in the rule
    house_of_lord: int | None  # which house's lord is running the Dasha (1-12); None for multi-house/general rules

class HouseLordSlokaExtraction(BaseModel):
    rules: list[HouseLordExtractedRule]


# ── AI extraction prompts ──────────────────────────────────────────────────────

EXTRACTION_SYSTEM = """\
You are a Vedic astrology rule extractor working on BPHS Vol 2 (Brihat Parashara Hora Shastra).

Given a Dasha sloka (verse), extract each distinct astrological prediction rule as a separate
structured object. A prediction rule is a specific if→then statement:
  if [astrological condition during Dasha] → then [life outcome or effect]

RULES:
1. Split compound slokas — each distinct condition→outcome pair is one rule.
2. "Or / alternatively" conditions yielding the SAME outcome = one rule (combine them).
3. Opposite outcomes from different conditions = separate rules.
4. Keep condition and result text close to the original wording.
5. Canonical planet names: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu.
6. sub_type must be exactly one of:
   dasha_favourable   — favourable/auspicious Dasha effects (exaltation, own sign, kendra, etc.)
   dasha_unfavourable — unfavourable/inauspicious Dasha effects (debilitation, 6/8/12, etc.)
   dasha_conditional  — mixed or conditional effects (if aspected by benefic, etc.)
   dasha_remedy       — remedy or mitigation advice
   general_principle  — overarching timing principle not fitting above
"""

EXTRACTION_PROMPT = """\
Chapter {chapter} — {chapter_name}
Dasha lord: {dasha_lord}
Sloka: {sloka}

Text:
{text}

Extract all distinct prediction rules for this Dasha period.
"""

HOUSE_LORD_EXTRACTION_SYSTEM = """\
You are a Vedic astrology rule extractor working on BPHS Vol 2 Chapter 48 — Dasas of Lords of Various Houses.

This chapter describes the effects experienced when the lord of a particular house (1st through 12th)
runs its Vimshottari Mahadasha period. The "if" clause is always which house's lord is running the Dasha,
possibly combined with placement or combination conditions.

Extract each distinct prediction rule as a separate structured object.

RULES:
1. Split compound slokas — each distinct condition→outcome pair is one rule.
   e.g. "Lord of 1st → well-being; Lord of 2nd → distress" = TWO rules.
2. "Or / alternatively" conditions yielding the SAME outcome = one rule (combine them).
3. Opposite outcomes from different conditions = separate rules.
4. Keep condition and result text close to the original wording.
5. Canonical planet names: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu.
6. house_of_lord: the house number (1-12) whose lord is running the Dasha.
   Set to null for rules that apply to multiple lords together (e.g. "Lord of kendra and trikona combined")
   or for general timing principles not tied to a specific house.
7. houses: ALL house numbers mentioned anywhere in the rule (including house_of_lord).
8. sub_type must be exactly one of:
   dasha_favourable   — favourable/auspicious effects during that lord's Dasha
   dasha_unfavourable — unfavourable/inauspicious effects
   dasha_conditional  — mixed or conditional effects (placement-dependent, aspected by benefic, etc.)
   dasha_remedy       — remedy or mitigation advice
   general_principle  — overarching principle about house lord Dasas not tied to one house
"""

HOUSE_LORD_EXTRACTION_PROMPT = """\
Chapter {chapter} — {chapter_name}
Sloka: {sloka}

Text:
{text}

Extract all distinct prediction rules. For each rule identify which house's lord is running the Dasha (house_of_lord 1-12, or null for multi-house/general rules).
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

    def extract_house_lord(
        self,
        sloka_label: str,
        rule_text: str,
        notes_text: str,
        chapter: int,
    ) -> list[HouseLordExtractedRule]:
        """Extract house-lord Dasha rules (Ch 48). Returns empty list on failure."""
        full_text = rule_text
        if notes_text:
            full_text = rule_text + "\n\nNote:\n" + notes_text.strip()

        prompt = HOUSE_LORD_EXTRACTION_PROMPT.format(
            chapter=chapter,
            chapter_name=CHAPTER_NAMES.get(chapter, f"Chapter {chapter}"),
            sloka=sloka_label,
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
                    "text": HOUSE_LORD_EXTRACTION_SYSTEM,
                    "cache_control": {"type": "ephemeral"},
                }],
                messages=[{"role": "user", "content": prompt}],
                output_format=HouseLordSlokaExtraction,
            )
            return response.parsed_output.rules
        except Exception as e:
            print(f"⚠  AI extraction failed for sloka {sloka_label}: {e}")
            return []

    def extract(
        self,
        sloka_label: str,
        rule_text: str,
        notes_text: str,
        chapter: int,
        dasha_lord: str,
    ) -> list[ExtractedRule]:
        """Extract individual rules from a sloka. Returns empty list on failure."""
        full_text = rule_text
        if notes_text:
            full_text = rule_text + "\n\nNote:\n" + notes_text.strip()

        prompt = EXTRACTION_PROMPT.format(
            chapter=chapter,
            chapter_name=CHAPTER_NAMES.get(chapter, f"Chapter {chapter}"),
            dasha_lord=dasha_lord,
            sloka=sloka_label,
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


# ── RTF parser ─────────────────────────────────────────────────────────────────

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
        if line != ';':
            lines.append(line)  # preserve blank lines as paragraph separators
    return '\n'.join(lines)


def split_into_sloka_blocks(text: str) -> list[tuple[str, str, int]]:
    """
    Split plain text into (sloka_label, block_text, sloka_start_pos) tuples.

    Dasha chapter sloka heading formats observed:
      7-11. During the Dasa of the Sun...
      34-39: In order to clarify...       ← colon separator
      78. Now I will describe...
      79-82. Should Venus...
    """
    # Normalise OCR artefacts: leading 'l' digit → '1'
    text = re.sub(r'(?m)^\s*l(?=[-\d.])', '1', text)

    # Dasha sloka pattern — accepts . : or - as separator, also handles single numbers
    # [ \t]* (zero or more) to handle "88-89.Similar" (no space after period)
    # Trailing dash handles RTF OCR artefact "15-16- Effects..." (separator rendered as dash)
    sloka_re = re.compile(
        r"(?m)^[ \t]*(\d+[a-z]?(?:\s*[-\u2013]\s*\d+[a-z]?)?)[.:\-][ \t]*([A-Z].+)$"
    )

    matches = list(sloka_re.finditer(text))
    if not matches:
        return []

    blocks: list[tuple[str, str, int]] = []
    for i, m in enumerate(matches):
        label = m.group(1).strip()
        heading_start = m.group(2).strip()
        start = m.end()
        end   = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body  = text[start:end].strip()
        blocks.append((label, heading_start + " " + body, m.start()))

    return blocks


def build_planet_position_map(text: str) -> list[tuple[int, str]]:
    """
    Pre-scan text for all planet Dasha section headings.
    Returns sorted list of (char_position, planet_name).

    Section headings appear both inside sloka text AND as free text between slokas,
    so this full-text scan is more reliable than per-block detection.
    """
    hits: list[tuple[int, str]] = []
    seen_positions: set[int] = set()
    for pat in _PLANET_SECTION_PATTERNS:
        for m in pat.finditer(text):
            name = m.group(1).strip().title()
            if name in PLANETS and m.start() not in seen_positions:
                # Deduplicate hits within 10 chars of each other
                if not any(abs(pos - m.start()) < 10 for pos, _ in hits):
                    hits.append((m.start(), name))
                    seen_positions.add(m.start())
    hits.sort(key=lambda x: x[0])
    return hits


def clean_notes(text: str) -> tuple[str, str]:
    m = re.compile(r'\bNotes?\s*[.:\'"\s]', re.IGNORECASE).search(text)
    if m:
        return text[:m.start()].strip(), text[m.start():].strip()
    return text.strip(), ""


# Chapter-specific slokas with no prediction content (pure dialog / section headers)
INTRO_SLOKAS_BY_CHAPTER: dict[int, set[str]] = {
    47: {"1", "2"},
    48: set(),  # Ch 48 sloka 1 has real prediction content
}

SKIP_HEADINGS = {
    # Lines that are purely dialog openers with no prediction content
    "maitreya said", "the sage replied",
}

# Short single-sentence slokas that only introduce the next planet's section
# without containing any prediction rules of their own.
_INTRO_ONLY_RE = re.compile(
    r'^\s*(?:Now\s+)?I\s+(?:am\s+going\s+to|will)\s+'
    r'(?:describe(?:\s+to\s+you)?|tell\s+you\s+about)\s+'
    r'(?:to\s+you\s+)?(?:the\s+)?(?:effects\s+of\s+)?(?:the\s+)?Dasa',
    re.IGNORECASE,
)

def should_skip(label: str, text: str, chapter: int = 47) -> bool:
    intro_slokas = INTRO_SLOKAS_BY_CHAPTER.get(chapter, INTRO_SLOKAS_BY_CHAPTER.get(47, set()))
    if label in intro_slokas:
        return True
    h = text.lower()
    for phrase in SKIP_HEADINGS:
        if h.startswith(phrase):
            return True
    # Skip pure planet-section introductions (no prediction content)
    if _INTRO_ONLY_RE.match(text) and len(text.split()) < 40:
        return True
    return len(text.split()) < 6


# ── Rule builders ──────────────────────────────────────────────────────────────

def make_source(chapter: int, sloka: str, batch_id: str) -> dict:
    return {
        "book":           BOOK,
        "book_id":        BOOK_ID,
        "chapter":        str(chapter),
        "chapter_name":   CHAPTER_NAMES.get(chapter, f"Chapter {chapter}"),
        "sloka":          sloka,
        "batch_id":       batch_id,
        "primary":        BOOK,
        "page_ref":       None,
        "passage_ref_id": None,
    }


def extracted_to_rule(
    item: ExtractedRule,
    sloka_label: str,
    dasha_lord: str,
    chapter: int,
    batch_id: str,
    index: int,
) -> dict:
    rule_id  = f"R-BPHS{chapter}-{index:03d}"
    planets  = [p for p in item.planets if p in PLANETS]
    sub_type = item.sub_type if item.sub_type in VALID_SUB_TYPES else "general_principle"

    # Ensure dasha_lord is in planets list
    if dasha_lord and dasha_lord not in planets:
        planets = [dasha_lord] + planets

    def _punct(s: str) -> str:
        s = s.strip()
        return s if (s and s[-1] in '.!?"\'') else s + '.'

    detailed = f"Condition: {_punct(item.full_condition)}\n\nEffect: {_punct(item.full_result)}"
    summary  = f"{item.condition_summary} → {_punct(item.result_summary)}"
    if len(summary) > 200:
        summary = summary[:197] + "..."

    houses_involved = [h for h in item.houses if isinstance(h, int)]
    tags = [
        "verbatim", "dasha_planet", f"chapter{chapter}",
        f"dasha_{dasha_lord.lower()}" if dasha_lord else "dasha_unknown",
        sub_type, "ai_extracted",
    ]

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source":     make_source(chapter, sloka_label, batch_id),
        "condition": {
            "type":             "dasha_planet",
            "dasha_lord":       dasha_lord,
            "sub_type":         sub_type,
            "sloka":            sloka_label,
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
            "life_domain":        "general",
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


def _fallback_rule(
    label: str,
    raw_text: str,
    dasha_lord: str,
    chapter: int,
    batch_id: str,
    index: int,
) -> dict | None:
    """Single-rule fallback when AI extraction returns nothing."""
    rule_text, _ = clean_notes(raw_text)
    if len(rule_text.split()) < 6:
        return None
    summary = rule_text.split(".")[0].strip()[:200]
    planets = [p for p in PLANETS if re.search(rf'\b{p}\b', raw_text, re.IGNORECASE)]
    if dasha_lord and dasha_lord not in planets:
        planets = [dasha_lord] + planets
    return {
        "rule_id":    f"R-BPHS{chapter}-{index:03d}",
        "science_id": SCIENCE,
        "source":     make_source(chapter, label, batch_id),
        "condition": {
            "type": "dasha_planet", "dasha_lord": dasha_lord,
            "sub_type": "general_principle", "sloka": label,
            "planets_involved": planets, "houses_involved": [],
            "sub_conditions": [], "operator": "and",
        },
        "interpretation": {
            "summary": summary, "detailed": rule_text,
            "full_text_passages": [{"text": rule_text, "confidence": "HIGH"}],
            "remedies": [], "life_domain": "general",
            "tags": ["verbatim", "dasha_planet", f"chapter{chapter}"],
        },
        "metadata": {
            "planets_involved": planets, "houses_involved": [],
            "signs_involved": [], "condition_count": 1,
        },
        "confidence": {"base": 0.82, "source_weight": 0.95, "cross_book_multiplier": 1.0},
        "approval_status": "pending_review",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def extracted_to_rule_house_lord(
    item: HouseLordExtractedRule,
    sloka_label: str,
    chapter: int,
    batch_id: str,
    index: int,
) -> dict:
    rule_id  = f"R-BPHS{chapter}-{index:03d}"
    planets  = [p for p in item.planets if p in PLANETS]
    sub_type = item.sub_type if item.sub_type in VALID_SUB_TYPES else "general_principle"
    house_num = item.house_of_lord  # int 1-12 or None

    def _punct(s: str) -> str:
        s = s.strip()
        return s if (s and s[-1] in '.!?"\'') else s + '.'

    detailed = f"Condition: {_punct(item.full_condition)}\n\nEffect: {_punct(item.full_result)}"
    summary  = f"{item.condition_summary} → {_punct(item.result_summary)}"
    if len(summary) > 200:
        summary = summary[:197] + "..."

    houses_involved = [h for h in item.houses if isinstance(h, int)]
    tags = [
        "verbatim", "dasha_of_house_lord", f"chapter{chapter}", sub_type, "ai_extracted",
    ]
    if house_num:
        tags.append(f"house{house_num}")

    condition: dict = {
        "type":             "dasha_of_house_lord",
        "house":            house_num,
        "sub_type":         sub_type,
        "sloka":            sloka_label,
        "planets_involved": planets,
        "houses_involved":  houses_involved,
        "sub_conditions":   [],
        "operator":         "and",
    }

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source":     make_source(chapter, sloka_label, batch_id),
        "condition":  condition,
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        "general",
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


def _fallback_rule_house_lord(
    label: str,
    raw_text: str,
    chapter: int,
    batch_id: str,
    index: int,
) -> dict | None:
    """Single-rule fallback for Ch 48 when AI extraction returns nothing."""
    rule_text, _ = clean_notes(raw_text)
    if len(rule_text.split()) < 6:
        return None
    summary = rule_text.split(".")[0].strip()[:200]
    planets = [p for p in PLANETS if re.search(rf'\b{p}\b', raw_text, re.IGNORECASE)]
    # Detect house number from text e.g. "Lord of the 5th"
    house_match = re.search(r'Lord\s+of\s+(?:the\s+)?(\d+)', raw_text)
    house_num = int(house_match.group(1)) if house_match else None
    return {
        "rule_id":    f"R-BPHS{chapter}-{index:03d}",
        "science_id": SCIENCE,
        "source":     make_source(chapter, label, batch_id),
        "condition": {
            "type": "dasha_of_house_lord", "house": house_num,
            "sub_type": "general_principle", "sloka": label,
            "planets_involved": planets, "houses_involved": [house_num] if house_num else [],
            "sub_conditions": [], "operator": "and",
        },
        "interpretation": {
            "summary": summary, "detailed": rule_text,
            "full_text_passages": [{"text": rule_text, "confidence": "HIGH"}],
            "remedies": [], "life_domain": "general",
            "tags": ["verbatim", "dasha_of_house_lord", f"chapter{chapter}"],
        },
        "metadata": {
            "planets_involved": planets,
            "houses_involved": [house_num] if house_num else [],
            "signs_involved": [], "condition_count": 1,
        },
        "confidence": {"base": 0.82, "source_weight": 0.95, "cross_book_multiplier": 1.0},
        "approval_status": "pending_review",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


# ── RTF ingestion ──────────────────────────────────────────────────────────────

def parse_rtf_file(
    rtf_path: str,
    chapter: int,
    dasha_lord_filter: str | None,
    batch_id: str,
    extractor: SlokaExtractor,
) -> list[dict]:
    raw    = Path(rtf_path).expanduser().read_text(encoding="utf-8", errors="replace")
    plain  = strip_rtf(raw)
    blocks = split_into_sloka_blocks(plain)

    rules: list[dict] = []
    idx   = 1
    total = len(blocks)

    house_lord_mode = (chapter == 48)

    if not house_lord_mode:
        # Pre-scan the entire text for all planet Dasha section headings.
        # This is more reliable than per-block detection because section headings
        # often appear as free text between slokas (ending up in the previous block's body).
        planet_map = build_planet_position_map(plain)  # sorted (pos, planet)
    else:
        planet_map = []

    def _planet_at(sloka_pos: int) -> str:
        """Return the planet whose section most recently started before sloka_pos."""
        if dasha_lord_filter:
            return dasha_lord_filter
        result = ""
        for pos, planet in planet_map:
            if pos <= sloka_pos:
                result = planet
            else:
                break
        return result

    # Track printed section headers to avoid duplicate prints
    last_printed_planet = ""

    for i, (label, text, sloka_pos) in enumerate(blocks, 1):
        if should_skip(label, text, chapter):
            print(f"  [{i:2d}/{total}] Sloka {label:8s} — skipped")
            continue

        rule_text, notes_text = clean_notes(text)

        if house_lord_mode:
            print(f"  [{i:2d}/{total}] Sloka {label:8s} [house lord] extracting...",
                  end=" ", flush=True)
            extracted_hl = extractor.extract_house_lord(label, rule_text, notes_text, chapter)
            if extracted_hl:
                batch = [extracted_to_rule_house_lord(item, label, chapter, batch_id, idx + j)
                         for j, item in enumerate(extracted_hl)]
                print(f"{len(batch)} rule(s)")
                rules.extend(batch)
                idx += len(batch)
            else:
                fallback = _fallback_rule_house_lord(label, text, chapter, batch_id, idx)
                if fallback:
                    print("1 rule (fallback)")
                    rules.append(fallback)
                    idx += 1
                else:
                    print("skipped (fallback)")
            continue

        effective_lord = _planet_at(sloka_pos)

        # Override for transition slokas that shift to a new planet mid-block.
        # e.g. sloka 16-22: "after describing the Sun Dasa... I will now come to
        # the effects of the Vimsottari Dasa of the Moon."
        # The position map gives "Sun" (last header before sloka start), but the
        # actual prediction content is Moon Dasha — use the forward-looking planet.
        transition_planet = detect_transition_planet(text)
        if transition_planet:
            effective_lord = transition_planet

        # For Ch 52-60, use the chapter's fixed Mahadasha lord
        if chapter in ANTARDASHA_CHAPTER_LORD:
            effective_lord = ANTARDASHA_CHAPTER_LORD[chapter]

        # Print section header when planet changes
        if effective_lord and effective_lord != last_printed_planet:
            print(f"\n  ── {effective_lord} Dasa ──")
            last_printed_planet = effective_lord

        print(f"  [{i:2d}/{total}] Sloka {label:8s} [{effective_lord or '?':8s}] extracting...",
              end=" ", flush=True)
        extracted = extractor.extract(label, rule_text, notes_text, chapter, effective_lord)

        if extracted:
            batch = [extracted_to_rule(item, label, effective_lord, chapter, batch_id, idx + j)
                     for j, item in enumerate(extracted)]
            print(f"{len(batch)} rule(s)")
            rules.extend(batch)
            idx += len(batch)
        else:
            fallback = _fallback_rule(label, text, effective_lord, chapter, batch_id, idx)
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
        description="Ingest BPHS Dasha chapters (47, 48, 52-60) with AI rule extraction"
    )
    parser.add_argument("--rtf",        required=True)
    parser.add_argument("--chapter",    required=True, type=int,
                        choices=[47, 48, 52, 53, 54, 55, 56, 57, 58, 59, 60],
                        metavar="CHAPTER",
                        help="BPHS chapter number (47=Mahadasha, 48=HouseLord Dasha, 52-60=Antardasha)")
    parser.add_argument("--dasha-lord", default=None,
                        choices=PLANETS + [None],
                        help="Override Mahadasha lord (auto-detected for Ch 47; required for Ch 48/52-60 if not auto-detected)")
    parser.add_argument("--mongo-url",  required=True)
    parser.add_argument("--db-name",    required=True)
    parser.add_argument("--model",      default="claude-haiku-4-5",
                        help="Claude model for extraction (default: claude-haiku-4-5)")
    parser.add_argument("--dry-run",    action="store_true",
                        help="Print rules but do NOT write to MongoDB")
    args = parser.parse_args()

    batch_id  = f"bphs-ch{args.chapter}-dasha-{datetime.now(timezone.utc).strftime('%Y%m%d')}"
    chap_name = CHAPTER_NAMES.get(args.chapter, f"Chapter {args.chapter}")
    lord_label = args.dasha_lord or ("auto-detect" if args.chapter == 47 else "N/A")

    print(f"\nBPHS Chapter {args.chapter} — {chap_name}  [v1 Dasha extraction]")
    print(f"Dasha lord: {lord_label}  |  model: {args.model}  |  batch_id: {batch_id}")
    print("─" * 60)

    extractor = SlokaExtractor(model=args.model)
    rules     = parse_rtf_file(args.rtf, args.chapter, args.dasha_lord, batch_id, extractor)

    if not rules:
        print("\n⚠  No rules extracted. Check RTF path and ANTHROPIC_API_KEY.")
        return

    # Summary by sub_type and dasha_lord / house
    sub_types: dict[str, int] = {}
    groups: dict[str, int] = {}
    house_lord_mode = (args.chapter == 48)
    for r in rules:
        st = r["condition"]["sub_type"]
        sub_types[st] = sub_types.get(st, 0) + 1
        if house_lord_mode:
            key = f"house{r['condition'].get('house') or 'general'}"
        else:
            key = r["condition"].get("dasha_lord", "unknown")
        groups[key] = groups.get(key, 0) + 1

    print()
    print("  By sub_type:")
    for st, count in sorted(sub_types.items(), key=lambda x: -x[1]):
        print(f"    {st:<30} : {count}")
    print(f"    {'─' * 38}")
    print(f"    {'TOTAL':<30} : {len(rules)}")

    group_label = "house_of_lord" if house_lord_mode else "dasha_lord"
    if len(groups) > 1:
        print(f"\n  By {group_label}:")
        for key, count in sorted(groups.items(), key=lambda x: x[0]):
            print(f"    {key:<20} : {count}")

    print(f"\n  Isolation: approval_status='pending_review' — zero rules reach live users")

    if args.dry_run:
        print("\n[DRY RUN] — no changes written to MongoDB")
        print("\nSample rules:")
        for r in rules[:8]:
            c = r["condition"]
            print(f"\n  {r['rule_id']}")
            print(f"    sloka       : {c['sloka']}")
            if c["type"] == "dasha_of_house_lord":
                print(f"    house       : {c.get('house', '?')}")
            else:
                print(f"    dasha_lord  : {c.get('dasha_lord', '?')}")
            print(f"    sub_type    : {c['sub_type']}")
            print(f"    summary     : {r['interpretation']['summary'][:100]}")
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
