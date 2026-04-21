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
    "dasha_remedy", "general_principle", "dasha_grouped_outcome",
}

# ── Pydantic models ────────────────────────────────────────────────────────────

class ExtractedRule(BaseModel):
    condition_summary: str   # ≤20 words: the if-clause
    result_summary: str      # ≤20 words: the then-clause / outcome
    full_condition: str      # complete condition text
    full_result: str         # complete result/effect text
    sub_type: str            # dasha_favourable | dasha_unfavourable | dasha_conditional | dasha_remedy | general_principle | dasha_grouped_outcome
    planets: list[str]       # canonical planet names involved
    houses: list[int]        # house numbers mentioned
    dignity_state: str = ""  # primary condition type: exaltation|own_sign|moolatrikona|friendly_sign|neutral_sign|enemy_sign|debilitation|kendra|trikona|upachaya|11th|3rd|2nd|8th|6th|12th|7th|combust|retrograde|malefic_aspect|benefic_aspect|yogakaraka|maraka_lord|dusthana_lord|general
    planet_context_note: str = ""  # short qualitative note e.g. "Exaltation: highest dignity" or "8th house: crisis and obstacles"
    condition_group_id: str = ""   # links same-condition rules together for grouped outcome query (e.g. "ch55-sl8-12-jupiter-favourable")
    is_group_summary: bool = False # True only on the single grouped summary rule; individual outcome rules = False

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
    dignity_state: str = ""  # primary condition type (same vocabulary as ExtractedRule)
    planet_context_note: str = ""  # short qualitative note

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
   dasha_favourable      — favourable/auspicious Dasha effects (exaltation, own sign, kendra, etc.)
   dasha_unfavourable    — unfavourable/inauspicious Dasha effects (debilitation, 6/8/12, etc.)
   dasha_conditional     — mixed or conditional effects (if aspected by benefic, etc.)
   dasha_remedy          — remedy or mitigation advice
   general_principle     — overarching timing principle not fitting above
   dasha_grouped_outcome — ONE grouped summary rule combining all outcomes from same-condition individual rules (see GROUPED OUTCOME RULE below)

SPLITTING GUIDANCE — one rule per independently queryable astrological condition.
Each rule must be matchable to a specific state in a user's chart at query time.

ALWAYS SPLIT into separate rules:

  1. SPECIFIC HOUSE NUMBERS — each house is a distinct, independently queryable position
       "in the 6th, 8th, or 12th"              → 3 rules (one per house)
       "in kendra, trikona, the 11th, the 3rd, or the 2nd"
                                                → 5 rules (kendra as one, trikona as one, 11th, 3rd, 2nd each separate)
       "in the 2nd or the 7th from Ascendant"  → 2 rules

  2. PLANETARY DIGNITY STATES — each carries a different strength level for the knowledge engine
       "in exaltation, own sign, or friend's sign"  → 3 rules
       "in debilitation or enemy sign"              → 2 rules
       "in exaltation" → strength_band: "high"
       "in own sign"   → strength_band: "high"
       "in friend's sign" → strength_band: "medium"
       "in enemy sign" → strength_band: "low"
       "in debilitation" → strength_band: "low"

  3. DIFFERENT CONDITION TYPES — qualitatively different astrological states
       debilitation / combustion / malefic aspect / maraka lordship → separate rules
       "from the Ascendant" vs "from the Dasha lord" → separate rules
       Example: "if Jupiter be in debilitation, combust, in 6th/8th/12th, or aspected by Saturn"
                → 4 rules (debilitation, combust, 6th + 8th + 12th as 3, malefic aspect)

KEEP AS ONE RULE:

  1. NAMED HOUSE CATEGORIES (abstract groups, no specific number)
       "in kendra"   → one rule (covers 1st/4th/7th/10th as a strength category)
                        strength_band: "high"
       "in trikona"  → one rule (covers 1st/5th/9th as a strength category)
                        strength_band: "high"
       "in upachaya" → one rule   strength_band: "medium"

  2. COMPOUND CONDITIONS requiring ALL parts simultaneously
       "combust AND in 8th house" → one rule (both must be true together)
       "in debilitation AND in the 12th" → one rule

  3. ADDITIVE QUALIFIERS that modify a parent condition (append to that rule, not a new split)
       "if also associated with the lord of the 9th" → qualifier on the parent rule

  4. LORDSHIP QUALIFIER COMPOUND RULES (MANDATORY — always extract as a standalone rule):
       If the source text combines a placement list WITH a lordship qualifier, extract ONE
       additional compound rule capturing BOTH parts together. Do NOT silently absorb the
       lordship qualifier into condition text or drop it.

       Example source: "Sun in kendra, trikona or 11th, associated with lord of 10th → great gain"
         → Rule A: "Sun in kendra → great gain"           (individual placement — from ALWAYS SPLIT rule 1)
         → Rule B: "Sun in trikona → great gain"          (individual placement)
         → Rule C: "Sun in 11th → great gain"             (individual placement)
         → Rule D: "Sun in kendra/trikona/11th associated with lord of 10th → great gain"
                                                          (compound: placement list + lordship qualifier)
       Rule D is a DISTINCT condition — it fires only when BOTH placement AND lordship are true.
       It is NOT a collision with Rules A/B/C — it carries additional astrological specificity.

       Lordship qualifier signals: "associated with lord of X", "with lord of X", "aspected by
       lord of X", "combined with lord of X", "as lord of X and Y", "with lords of Xth and Yth"

ANTI-COLLISION RULE — NO PARTIAL SPLITS (MANDATORY):

  If you decide to split a list of conditions into individual rules, you MUST:
    a) Generate ALL individual rules — one for every item in the list.
    b) NOT also generate a merged rule covering the same conditions.

  Either split completely OR keep as one merged rule. Never do both.

  WRONG — partial split with merged remnant:
    "Venus in 8th from Sun"          ← individual ✓
    "Venus in 12th from Sun"         ← individual ✓
    "Venus in 6th, 8th, or 12th"    ← merged still present ✗ (6th missing individually)

  RIGHT — complete split, no merged:
    "Venus in 6th from Sun"          ← individual ✓
    "Venus in 8th from Sun"          ← individual ✓
    "Venus in 12th from Sun"         ← individual ✓
    (no merged rule)

  RIGHT — keep merged when splitting is not warranted:
    "Venus in 6th, 8th, or 12th"    ← merged ✓  (one rule, no individuals alongside it)

  Same rule applies to dignity states:
  WRONG: "Jupiter in exaltation" + "Jupiter in own sign" + "Jupiter in exaltation or own sign"
  RIGHT: "Jupiter in exaltation" + "Jupiter in own sign"  (no merged alongside individuals)

strength_band for house positions (unfavourable rules):
  8th house → "high" (most malefic dusthana)
  6th, 12th → "medium"
  2nd, 7th  → "low" (maraka — death-inflicting)

QUALITATIVE CONTEXT — set on every rule without exception.

dignity_state: the single primary astrological condition type for this rule.
  Choose exactly one from this list:
  Dignity states  : exaltation | own_sign | moolatrikona | friendly_sign | neutral_sign | enemy_sign | debilitation
  House categories: kendra | trikona | upachaya
  Specific houses : 2nd | 3rd | 6th | 7th | 8th | 11th | 12th
  Other conditions: combust | retrograde | malefic_aspect | benefic_aspect | yogakaraka | maraka_lord | dusthana_lord
  Default         : general  (use when no specific dignity or house applies)

planet_context_note: one concise phrase (≤12 words) giving the qualitative meaning.
  Use the natural benefic / malefic nature of the planet where relevant.
  Natural benefics : Jupiter, Venus, Mercury (waxing), Moon (waxing)
  Natural malefics : Sun, Mars, Saturn, Rahu, Ketu, Mercury (waning), Moon (waning)

  Examples:
    dignity_state="exaltation"    → "Highest dignity — strongest, most auspicious expression"
    dignity_state="own_sign"      → "Own sign — strong, comfortable, reliable results"
    dignity_state="friendly_sign" → "Friendly sign — moderately favourable placement"
    dignity_state="enemy_sign"    → "Enemy sign — weakened, uncomfortable, reduced results"
    dignity_state="debilitation"  → "Debilitation — weakest dignity, adverse expression"
    dignity_state="kendra"        → "Angular house — strong manifestation of results"
    dignity_state="trikona"       → "Trine house — fortunate, dharmic placement"
    dignity_state="8th"           → "8th house — crisis, obstacles, sudden events"
    dignity_state="6th"           → "6th house — enemies, disease, service"
    dignity_state="12th"          → "12th house — losses, isolation, foreign travel"
    dignity_state="combust"       → "Combust — too close to Sun, significator weakened"
    dignity_state="malefic_aspect"→ "Malefic aspect — adverse planetary influence on period"
    dignity_state="yogakaraka"    → "Yogakaraka — lord of both kendra and trikona, powerful"
    dignity_state="maraka_lord"   → "Maraka lord — 2nd/7th house lord, death-inflicting potential"
    dignity_state="dusthana_lord" → "Dusthana lord — 6th/8th/12th house lord, challenging period"
    dignity_state="general"       → brief summary of the condition in plain language

GROUPED OUTCOME RULE (MANDATORY when 3+ outcomes share one base condition):

  When a sloka lists multiple distinct life-domain outcomes that ALL apply under the SAME
  astrological condition, you MUST produce two layers of rules:

  LAYER 1 — Individual outcome rules (one per outcome, for Q&A lookup):
    - Normal extraction as per SPLITTING GUIDANCE
    - sub_type = dasha_favourable / dasha_unfavourable / etc. (as appropriate)
    - is_group_summary = false
    - condition_group_id = same short identifier across all individual rules in this group
      Format: "ch<N>-sl<SLOKA>-<antardasha_planet_lower>-<favourable|unfavourable>"
      Example: "ch55-sl8-12-jupiter-favourable"

  LAYER 2 — ONE grouped summary rule (for general period report generation):
    - sub_type = "dasha_grouped_outcome"
    - is_group_summary = true
    - condition_group_id = same identifier as Layer 1 rules
    - full_condition = the shared base condition (same as the individual rules)
    - full_result = ALL outcomes combined into one comprehensive paragraph
    - result_summary = "All outcomes: [comma-separated list of 3-5 word outcome phrases]"
    - dignity_state = same as the individual rules' dominant dignity_state

  WHEN to create a grouped rule:
    ✓ 3 or more individual outcome rules sharing the same base condition
    ✓ Outcomes are all simultaneously applicable (not mutually exclusive)
    ✓ Outcomes cover distinct life domains (wealth, health, family, career, etc.)

  DO NOT create a grouped rule when:
    ✗ Fewer than 3 individual rules share the condition
    ✗ Rules have different conditions (correctly split per ALWAYS SPLIT guidance)
    ✗ Outcomes are conditional on each other (those remain dasha_conditional)

  Example (Jupiter AD in Rahu MD, slokas 8-12, Jupiter in kendra/trikona):
    Individual rules (Layer 1, all with condition_group_id="ch55-sl8-12-jupiter-favourable"):
      "Jupiter in kendra → Gain of position, destruction of foes"          is_group_summary=false
      "Jupiter in trikona → Gain of position, destruction of foes"         is_group_summary=false
      "Jupiter in kendra → Gain of conveyance and cows"                    is_group_summary=false
      "Jupiter in kendra → Visit to holy places"                           is_group_summary=false
      "Jupiter in kendra → Happiness from wife and children"               is_group_summary=false

    Grouped summary rule (Layer 2):
      condition_group_id = "ch55-sl8-12-jupiter-favourable"
      sub_type = "dasha_grouped_outcome"
      is_group_summary = true
      full_condition = "Jupiter in kendra or trikona during Rahu Mahadasha"
      full_result = "Gain of position and patience, destruction of foes, gain of conveyance
                    and cows, success in ventures, return to homeland with good deeds, visit
                    to holy places, gain of a village, happiness from wife and children,
                    availability of sweetish preparations daily."
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
                max_tokens=4096,
                temperature=0,
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
                max_tokens=4096,
                temperature=0,
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


class OpenAISlokaExtractor:
    """Drop-in replacement for SlokaExtractor using OpenAI structured outputs.

    Uses client.beta.chat.completions.parse() with the same Pydantic models
    (SlokaExtraction / HouseLordSlokaExtraction) and the same system prompts.
    No prompt caching — EXTRACTION_SYSTEM is delivered as the system message role.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self._client = None

    def _get_client(self):
        try:
            import openai as _openai
        except ImportError:
            raise RuntimeError("openai package not installed — run: pip install openai>=1.40.0")
        if self._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY not set in environment")
            self._client = _openai.OpenAI(api_key=api_key)
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
            response = client.beta.chat.completions.parse(
                model=self.model,
                max_tokens=4096,
                temperature=0,
                messages=[
                    {"role": "system", "content": HOUSE_LORD_EXTRACTION_SYSTEM},
                    {"role": "user",   "content": prompt},
                ],
                response_format=HouseLordSlokaExtraction,
            )
            return response.choices[0].message.parsed.rules
        except Exception as e:
            print(f"⚠  OpenAI extraction failed for sloka {sloka_label}: {e}")
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
            response = client.beta.chat.completions.parse(
                model=self.model,
                max_tokens=4096,
                temperature=0,
                messages=[
                    {"role": "system", "content": EXTRACTION_SYSTEM},
                    {"role": "user",   "content": prompt},
                ],
                response_format=SlokaExtraction,
            )
            return response.choices[0].message.parsed.rules
        except Exception as e:
            print(f"⚠  OpenAI extraction failed for sloka {sloka_label}: {e}")
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
    # Inner [-.+\u2013] also accepts "." as range separator to handle "5.6. Text..." style
    sloka_re = re.compile(
        r"(?m)^[ \t]*(\d+[a-z]?(?:\s*[-\u2013+.]\s*\d+[a-z]?)?)[.:\-][ \t]*([A-Z].+)$"
    )

    matches = list(sloka_re.finditer(text))
    if not matches:
        return []

    blocks: list[tuple[str, str, int]] = []
    for i, m in enumerate(matches):
        # Normalise label: replace inner "." range separator with "-" for consistency
        label = m.group(1).strip().replace(".", "-")
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
    59: set(),  # Ch 59 sloka 1-2 is Ketu/Ketu antardasha — real prediction content, do not skip
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

def infer_strength_band_from_condition(condition_text: str, sub_type: str) -> str:
    """Map condition text to strength_band based on dignity state or house position.

    Dignity states take precedence over house positions.
    Defaults to 'medium' when no signal is found.
    """
    text = condition_text.lower()

    # ── Planetary dignity states ───────────────────────────────────────────────
    if any(x in text for x in ["exaltation", "uchcha", "exalted"]):
        return "high"
    if any(x in text for x in ["own sign", "own house", "swakshetra", "svakshetra"]):
        return "high"
    if any(x in text for x in ["friend's sign", "friendly sign", "friend sign"]):
        return "medium"
    if any(x in text for x in ["enemy sign", "inimical sign", "enemy's sign"]):
        return "low"
    if any(x in text for x in ["debilitation", "neecha", "debilitated"]):
        return "low"

    # ── House positions — favourable / conditional context ─────────────────────
    if sub_type in ("dasha_favourable", "dasha_conditional"):
        if any(x in text for x in ["kendra", "trikona"]):
            return "high"
        if re.search(r"\b(11th|3rd|2nd)\b", text):
            return "medium"

    # ── House positions — unfavourable context ─────────────────────────────────
    if sub_type == "dasha_unfavourable":
        # Explicit moderation language overrides house-based intensity inference.
        # e.g. "moderate effects at commencement" should not inherit "high" from 8th.
        if any(x in text for x in ["moderate effect", "medium effect", "mixed effect",
                                    "moderate result", "moderate at"]):
            return "medium"
        if re.search(r"\b8th\b", text):
            return "high"   # highest intensity of harm
        if re.search(r"\b(6th|12th)\b", text):
            return "medium"
        if re.search(r"\b(2nd|7th)\b", text):
            return "low"

    # ── Remedy rules are inherently low intensity (mitigation, not prediction) ─
    if sub_type == "dasha_remedy":
        return "low"

    # ── Grouped outcome rules: medium by default (aggregated summary, no single intensity) ─
    if sub_type == "dasha_grouped_outcome":
        return "medium"

    return "medium"


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
    antardasha_planet: str | None,
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
    if item.is_group_summary:
        tags.append("group_summary")
    if item.condition_group_id:
        tags.append(f"group:{item.condition_group_id}")

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source":     make_source(chapter, sloka_label, batch_id),
        "condition": {
            "type":                "dasha_planet",
            "dasha_lord":          dasha_lord,
            "antardasha_planet":   antardasha_planet,
            "sub_type":            sub_type,
            "sloka":               sloka_label,
            "planets_involved":    planets,
            "houses_involved":     houses_involved,
            "sub_conditions":      [],
            "operator":            "and",
            "dignity_state":       item.dignity_state or "general",
            "planet_context_note": item.planet_context_note or "",
            "condition_group_id":  item.condition_group_id or None,
            "is_group_summary":    item.is_group_summary,
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
        "strength_band":   infer_strength_band_from_condition(
            item.condition_summary + " " + item.full_condition, sub_type
        ),
        "approval_status": "pending_review",
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


def _fallback_rule(
    label: str,
    raw_text: str,
    dasha_lord: str,
    antardasha_planet: str | None,
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
            "antardasha_planet": antardasha_planet,
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
        "strength_band":   infer_strength_band_from_condition(raw_text, "general_principle"),
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
        "type":                "dasha_of_house_lord",
        "house":               house_num,
        "sub_type":            sub_type,
        "sloka":               sloka_label,
        "planets_involved":    planets,
        "houses_involved":     houses_involved,
        "sub_conditions":      [],
        "operator":            "and",
        "dignity_state":       item.dignity_state or "general",
        "planet_context_note": item.planet_context_note or "",
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
    extractor: "SlokaExtractor | OpenAISlokaExtractor",
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
        antardasha_planet = effective_lord or None

        # Override for transition slokas that shift to a new planet mid-block.
        # e.g. sloka 16-22: "after describing the Sun Dasa... I will now come to
        # the effects of the Vimsottari Dasa of the Moon."
        # The position map gives "Sun" (last header before sloka start), but the
        # actual prediction content is Moon Dasha — use the forward-looking planet.
        transition_planet = detect_transition_planet(text)
        if transition_planet:
            effective_lord = transition_planet
            antardasha_planet = transition_planet

        # For Ch 52-60, use the chapter's fixed Mahadasha lord
        if chapter in ANTARDASHA_CHAPTER_LORD:
            effective_lord = ANTARDASHA_CHAPTER_LORD[chapter]
        else:
            antardasha_planet = None

        # Print section header when planet changes
        if effective_lord and effective_lord != last_printed_planet:
            print(f"\n  ── {effective_lord} Dasa ──")
            last_printed_planet = effective_lord

        print(f"  [{i:2d}/{total}] Sloka {label:8s} [{effective_lord or '?':8s}] extracting...",
              end=" ", flush=True)
        extracted = extractor.extract(label, rule_text, notes_text, chapter, effective_lord)

        if extracted:
            batch = [extracted_to_rule(item, label, effective_lord, antardasha_planet, chapter, batch_id, idx + j)
                     for j, item in enumerate(extracted)]
            print(f"{len(batch)} rule(s)")
            rules.extend(batch)
            idx += len(batch)
        else:
            fallback = _fallback_rule(label, text, effective_lord, antardasha_planet, chapter, batch_id, idx)
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
    parser.add_argument("--sloka-filter", default=None,
                        help="Show full rules only for this sloka label in dry-run (e.g. '69-73')")
    parser.add_argument("--model",        default="claude-haiku-4-5",
                        help="Claude model for extraction (default: claude-haiku-4-5)")
    parser.add_argument("--provider",     choices=["anthropic", "openai"], default="anthropic",
                        help="AI provider: 'anthropic' (default) or 'openai'")
    parser.add_argument("--openai-model", default="gpt-4o-mini",
                        help="OpenAI model when --provider=openai (default: gpt-4o-mini)")
    parser.add_argument("--dry-run",      action="store_true",
                        help="Print rules but do NOT write to MongoDB")
    args = parser.parse_args()

    batch_id  = f"bphs-ch{args.chapter}-dasha-{datetime.now(timezone.utc).strftime('%Y%m%d')}"
    chap_name = CHAPTER_NAMES.get(args.chapter, f"Chapter {args.chapter}")
    lord_label = args.dasha_lord or ("auto-detect" if args.chapter == 47 else "N/A")

    if args.provider == "openai":
        effective_model = args.openai_model
        extractor = OpenAISlokaExtractor(model=effective_model)
    else:
        effective_model = args.model
        extractor = SlokaExtractor(model=effective_model)

    print(f"\nBPHS Chapter {args.chapter} — {chap_name}  [v1 Dasha extraction]")
    print(f"Dasha lord: {lord_label}  |  provider: {args.provider}  |  model: {effective_model}  |  batch_id: {batch_id}")
    print("─" * 60)
    rules     = parse_rtf_file(args.rtf, args.chapter, args.dasha_lord, batch_id, extractor)

    if not rules:
        key_hint = "OPENAI_API_KEY" if args.provider == "openai" else "ANTHROPIC_API_KEY"
        print(f"\n⚠  No rules extracted. Check RTF path and {key_hint}.")
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

        sloka_filter = args.sloka_filter
        if sloka_filter:
            filtered = [r for r in rules if r["condition"].get("sloka") == sloka_filter]
            print(f"\nAll rules for sloka {sloka_filter} ({len(filtered)} rule(s)):")
            display_rules = filtered
        else:
            print("\nSample rules (first 8):")
            display_rules = rules[:8]

        for r in display_rules:
            c = r["condition"]
            print(f"\n  {r['rule_id']}")
            print(f"    sloka         : {c['sloka']}")
            if c["type"] == "dasha_of_house_lord":
                print(f"    house         : {c.get('house', '?')}")
            else:
                print(f"    dasha_lord    : {c.get('dasha_lord', '?')}")
            print(f"    sub_type      : {c['sub_type']}")
            print(f"    dignity_state : {c.get('dignity_state', '—')}")
            print(f"    strength_band : {r.get('strength_band', '—')}")
            print(f"    summary       : {r['interpretation']['summary'][:120]}")
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
