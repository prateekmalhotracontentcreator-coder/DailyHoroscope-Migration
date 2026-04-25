#!/usr/bin/env python3
"""
ingest_tba_ch16_v1.py

A Text-Book of Astrology — Chapter 16:
"Planetary Combinations or Yogas"

Two content types in one chapter:

  Type A — Named Yogas (Gaja Kesari, Hansa, Vipreet Rajyoga, etc.)
    Each yoga has a formation condition + native effects.
    → 1 rule per yoga (occasionally 2–3 for multi-variant yogas like Vipreet Rajyoga)

  Type B — Category Yoga Groups (Arishta, Wealth, Marriage, Progeny, etc.)
    Bullet-point rules under category headings (Long life / Timely Marriage / etc.)
    → 1 rule per bullet point

Rule ID   :  tba16-{INDEX:03d}
Batch ID  :  tba-ch16-v1-YYYYMMDD
source.sloka: yoga name slug (e.g., "gaja-kesari-yoga") for Type A;
              "cat-{category_slug}" for Type B

Usage:
    python3 scripts/ingest_tba_ch16_v1.py \\
        --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/TBA- Ch 16_Planetary Combinations or Yogas.rtf" \\
        --mongo-url "$MONGO_URL" --db-name horoscope_db \\
        [--dry-run] [--model claude-haiku-4-5]

Requires:
    ANTHROPIC_API_KEY set in environment
    pip install anthropic pydantic pymongo
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
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
from pymongo.errors import AutoReconnect

# ── Constants ──────────────────────────────────────────────────────────────────

SCIENCE   = "vedic_astrology"
BOOK      = "A Text-Book of Astrology"
BOOK_ID   = "tba_ch16"
CHAPTER   = "16"
CHAP_NAME = "Planetary Combinations or Yogas"

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
           "Saturn", "Rahu", "Ketu"]
PLANET_SET = set(p.lower() for p in PLANETS)

VALID_CONDITION_TYPES = {
    "yoga_combination",  # named yoga — formation condition
    "general_principle", # category bullet (Arishta / Wealth / Marriage etc.)
    "dosha",             # Kendradhipati Dosha
}

VALID_SUB_TYPES = {
    "yoga_formation",   # Type A — how the yoga forms
    "yoga_result",      # Type A — what it produces (used when split from formation)
    "benefic_rule",     # beneficial condition from a category group
    "malefic_rule",     # adverse condition from a category group
    "neutral_rule",     # neutral / conditional rule from category group
    "dosha_rule",       # dosha condition
}

DOMAIN_MAP = {
    "longevity": "longevity",
    "low morale": "mental_health",
    "deafness": "health",
    "dumbness": "health",
    "speech": "health",
    "eye": "health",
    "wealth": "wealth",
    "speculation": "wealth",
    "gambling": "wealth",
    "co-borns": "family",
    "conveyance": "material",
    "progeny": "children",
    "marriage": "relationships",
    "sun": "general",
    "moon": "general",
    "general": "general",
    "dosha": "general",
    "pancha": "general",
}

# ── Pydantic models ────────────────────────────────────────────────────────────

PHYSICAL_CATEGORIES = {
    "body_build",       # physique, limbs, chest, proportions
    "height",           # tall, short, medium height
    "facial_features",  # face shape, eyes, forehead, nose
    "complexion",       # skin tone — fair, ruddy, dark, wheatish
    "body_marks",       # specific marks/symbols on body (lotus, conch, etc.)
    "voice",            # voice quality — eloquent, stammering, unclear, defective
    "disability",       # blindness, deafness, dumbness, other physical disability
    "health",           # long-lived, sickly, robust, prone to illness
    "behavioral",       # observable traits — polite, daring, stubborn, generous, charitable
    "taste",            # food, material, or sensory preferences
}

class PhysicalMarker(BaseModel):
    category: str       # one of PHYSICAL_CATEGORIES
    description: str    # verbatim or close-verbatim text from the source
    polarity: str       # "positive" | "negative" | "neutral"

class YogaRule(BaseModel):
    yoga_name: str             # e.g. "Gaja Kesari Yoga" | "Long life" | bullet slug
    condition_summary: str     # ≤20 words: the if-clause
    result_summary: str        # ≤20 words: the effect (non-physical outcomes)
    full_condition: str        # complete condition text (verbatim)
    full_result: str           # complete result/effect text (verbatim)
    condition_type: str        # yoga_combination | general_principle | dosha
    sub_type: str              # yoga_formation | benefic_rule | malefic_rule | neutral_rule | dosha_rule
    planets_involved: list[str]
    houses_involved: list[int]
    is_benefic: bool           # True = beneficial yoga/result, False = adverse
    physical_markers: list[PhysicalMarker]  # physical appearance, voice, disability, behavioral markers

class SectionExtraction(BaseModel):
    rules: list[YogaRule]

# ── System prompts ─────────────────────────────────────────────────────────────

_PHYSICAL_MARKER_INSTRUCTIONS = """\
PHYSICAL MARKERS — extract ALL physical appearance, disability, voice, and behavioural observations
into the physical_markers list. This is a separate, dedicated extraction layer.

Each physical_markers entry has:
  category    = one of: body_build | height | facial_features | complexion | body_marks |
                        voice | disability | health | behavioral | taste
  description = verbatim or close-verbatim text from the source (do not paraphrase)
  polarity    = "positive" (auspicious / favourable trait)
               "negative" (adverse / unfavourable condition: blindness, deafness, stammering, etc.)
               "neutral"  (descriptive only — e.g., "ruddy complexion", "lion like face")

Extraction guidance:
  body_build     → "well proportioned limbs", "strong physique", "well developed chest"
  height         → "tall", "short stature", "medium height" (if mentioned)
  facial_features → "lion like face", "handsome", "attractive body"
  complexion     → "ruddy complex", "fair", "dark"
  body_marks     → "marks of conch, lotus, fish and ankles on legs"
  voice          → "eloquent speaker", "stammers", "speech is not clear", "speech defects"
  disability     → "born blind", "night blindness", "deafness", "dumb", "defective sight"
  health         → "long lived", "healthy", "sickly", "enjoys good health"
  behavioral     → "polite", "generous", "daring", "stubborn", "charitable", "intelligent",
                   "righteous", "wicked", "questionable character"
  taste          → food, drink, material or sensory preferences (sparse in Ch 16)

IMPORTANT:
  - physical_markers = [] if the rule has NO physical/disability/behavioural content
  - Disability rules (blindness, deafness, dumbness, speech defect) ALWAYS have is_benefic = False
    and at least one physical_markers entry with category "disability" or "voice", polarity "negative"
  - Behavioural traits like "polite", "generous", "charitable" → polarity "positive"
  - "Questionable character", "wicked disposition", "covet other's riches" → polarity "negative"
  - "Ruddy complexion", "lion-like face" are neutral descriptors → polarity "neutral"
"""

TYPE_A_SYSTEM = """\
You are a Vedic astrology rule extractor working on "A Text-Book of Astrology", Chapter 16 — Planetary Combinations or Yogas.

You will receive one or more NAMED YOGA descriptions. Each named yoga has:
  - A formation condition ("This yoga is formed when…" / "IF X then yoga is formed")
  - An effect on the native ("The native born in this yoga will…")

For each yoga, extract ONE rule (or multiple if the yoga has clearly distinct variants).

Standard field instructions:
  yoga_name         = exact yoga name (e.g., "Gaja Kesari Yoga")
  condition_summary = ≤20 words summarising the formation condition
  result_summary    = ≤20 words summarising the native's NON-PHYSICAL outcomes (wealth, fame, career, etc.)
  full_condition    = verbatim formation text (how the yoga forms)
  full_result       = verbatim complete effect text (include ALL effects — physical and non-physical)
  condition_type    = "yoga_combination" for named yogas; "dosha" for Kendradhipati Dosha
  sub_type          = "yoga_formation"
  planets_involved  = canonical planet names mentioned (Sun Moon Mars Mercury Jupiter Venus Saturn Rahu Ketu)
  houses_involved   = house numbers mentioned (1–12) — only explicit numbers, do NOT infer
  is_benefic        = True if yoga gives positive/auspicious results overall; False if adverse

Special cases:
  - Vipreet Rajyoga: produce 3 separate rules — Harsha, Saral, Vimal variants
  - Kemadruma Bhanga Yoga: one rule combining all formation conditions
  - Parvata Yoga: one rule with both Phaldeepika + Jatak Parijata variants in full_condition
  - is_benefic = False for: Kemadruma Yoga, Sakata Yoga, Dur Yoga, Daridra Yoga, Andha Yoga, Sasa Yoga

""" + _PHYSICAL_MARKER_INSTRUCTIONS

TYPE_B_SYSTEM = """\
You are a Vedic astrology rule extractor working on "A Text-Book of Astrology", Chapter 16 — Planetary Combinations or Yogas.

You will receive a CATEGORY GROUP of astrology conditions — a set of bullet-point rules under a
category heading (e.g., "Long life", "Yogas For Wealth", "Timely Marriage", "Yogas For Deafness").

For each bullet point, extract ONE rule.

Standard field instructions:
  yoga_name         = category heading + bullet index (e.g., "Long life — 1", "Yogas For Deafness — 2")
  condition_summary = ≤20 words: the planetary/house condition described
  result_summary    = ≤20 words: the predicted NON-PHYSICAL outcome
  full_condition    = verbatim condition text (the bullet point as written)
  full_result       = verbatim predicted outcome (may be embedded in the condition — extract it)
  condition_type    = "general_principle"
  sub_type:
    "benefic_rule"  — condition gives a positive/auspicious result
    "malefic_rule"  — condition gives an adverse/negative result
    "neutral_rule"  — mixed or conditional
  planets_involved  = canonical planet names mentioned
  houses_involved   = house numbers mentioned (1–12) — only explicit numbers
  is_benefic        = True if the rule gives a positive result

Category-level defaults:
  "Long life", "Timely Marriage", "Yogas For Wealth", "Yogas For Conveyance",
  "Yogas For Progeny" → sub_type = "benefic_rule", is_benefic = True
  "Short Life", "Late Marriage", "No Marriage", "Yogas For Low Morale",
  "Yogas For Deafness", "Yogas For Dumbness", "Yogas For Speech Defects",
  "Yogas For Eye Troubles" → sub_type = "malefic_rule", is_benefic = False
  "Medium Life" → sub_type = "neutral_rule", is_benefic = False

  - Every bullet = one rule; do NOT merge or skip any
  - Canonical planet names: Sun Moon Mars Mercury Jupiter Venus Saturn Rahu Ketu

""" + _PHYSICAL_MARKER_INSTRUCTIONS

# ── RTF parser ─────────────────────────────────────────────────────────────────

def strip_rtf(raw: str) -> list[str]:
    """Return list of clean non-empty lines from RTF source."""
    text = raw
    text = re.sub(r"\\'[0-9a-fA-F]{2}", "", text)
    text = re.sub(r"\\[a-zA-Z*]+[-]?[0-9]*[ ]?", " ", text)
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip().rstrip("\\").strip()
        if line and not re.match(r'^[; ]+$', line):
            lines.append(line)
    return lines


# Known heading strings (used to split sections)
_HEADING_SUFFIXES = re.compile(
    r'^(Arishta|Yogas|Long life|Medium Life|Short Life|Timely Marriage|Late Marriage|'
    r'No Marriage|Panch Maha Purusha|Yogas created by|Auspicious|Important Yogas|'
    r'Planetary Combinations)',
    re.IGNORECASE,
)
_YOGA_HEADING = re.compile(
    r'^([A-Z][A-Za-z\- ]+(?:Yoga|yoga|Dosha|dosha))$'
)
_INTRO_LINES = {
    "Helvetica-Bold; Helvetica;",
    "; ; ; ;",
    "Planetary Combinations or Yogas",
    "Important Yogas in Astrology",
    "A yoga is formed by more than one planet. For interpreting yogas, followings are required:",
    "The good and evil lords in a horoscope",
    "The inherent strengths of planets",
    "The positional strength of planets",
    "Yogas created by Sun",
    "Yogas created by Moon",
    "Panch Maha Purusha Yogas",
}


def is_heading(line: str) -> bool:
    """Return True if this line looks like a section or yoga heading."""
    if line in _INTRO_LINES:
        return True
    if len(line) > 80:
        return False
    if _YOGA_HEADING.match(line):
        return True
    if _HEADING_SUFFIXES.match(line):
        return True
    # Sub-headings for category groups
    if line in ("Long life", "Medium Life", "Short Life",
                "Timely Marriage", "Late Marriage", "No Marriage"):
        return True
    return False


def parse_rtf(rtf_path: str) -> list[dict]:
    """
    Parse RTF into a list of section dicts:
      {
        "heading": str,
        "parent": str | None,   # parent heading (for sub-groups)
        "lines": list[str],
      }
    """
    raw   = Path(rtf_path).expanduser().read_text(encoding="latin-1", errors="replace")
    lines = strip_rtf(raw)

    sections: list[dict] = []
    cur_heading: str | None = None
    cur_parent: str | None  = None
    cur_lines: list[str]    = []

    # Top-level category containers (not standalone sections)
    CONTAINERS = {
        "Arishta Yoga",
        "Yogas For Marriage",
        "Yogas created by Sun",
        "Yogas created by Moon",
        "Panch Maha Purusha Yogas",
    }

    SKIP_LINES = _INTRO_LINES | {
        "Yogas created by Sun",
        "Yogas created by Moon",
        "Panch Maha Purusha Yogas",
    }

    def flush():
        nonlocal cur_heading, cur_parent, cur_lines
        if cur_heading and cur_heading not in SKIP_LINES:
            body = [l for l in cur_lines if l]
            h_lower = cur_heading.lower()
            if body or h_lower.endswith("yoga") or h_lower.endswith("dosha"):
                sections.append({
                    "heading": cur_heading,
                    "parent": cur_parent,
                    "lines": body,
                })
        cur_lines = []

    active_container: str | None = None  # tracks Arishta Yoga / Yogas For Marriage etc.

    for line in lines:
        if line in SKIP_LINES:
            # Update active container context
            if line in CONTAINERS:
                active_container = line
            flush()
            cur_heading = None
            continue

        if is_heading(line):
            flush()
            # Determine parent
            if line in ("Long life", "Medium Life", "Short Life"):
                cur_parent = "Arishta Yoga"
                active_container = "Arishta Yoga"
            elif line in ("Timely Marriage", "Late Marriage", "No Marriage"):
                cur_parent = "Yogas For Marriage"
                active_container = "Yogas For Marriage"
            elif line.startswith("Yogas For ") or line == "Auspicious - Inauspicious Yogas":
                cur_parent = None
                active_container = line
            elif active_container and active_container in CONTAINERS and line not in CONTAINERS:
                # Named yoga within a container (e.g., Vesi Yoga under "Yogas created by Sun")
                cur_parent = active_container
            else:
                cur_parent = None
            cur_heading = line
        else:
            if cur_heading:
                cur_lines.append(line)

    flush()
    return sections


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

    def _call(self, system: str, user_prompt: str) -> list[YogaRule]:
        for attempt in range(3):
            try:
                resp = self._get_client().messages.parse(
                    model=self.model,
                    max_tokens=4096,
                    temperature=0,
                    system=[{
                        "type": "text",
                        "text": system,
                        "cache_control": {"type": "ephemeral"},
                    }],
                    messages=[{"role": "user", "content": user_prompt}],
                    output_format=SectionExtraction,
                )
                return resp.parsed_output.rules
            except Exception as exc:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    print(f"\n  ⚠  AI call failed after 3 attempts: {exc}")
                    return []
        return []

    def extract_type_a(self, sections: list[dict]) -> list[YogaRule]:
        """Extract named yoga rules (Type A) — batch up to 8 per call."""
        parts = []
        for sec in sections:
            body = "\n".join(sec["lines"]) if sec["lines"] else "(see yoga name)"
            parts.append(f"### {sec['heading']}\n{body}")
        prompt = (
            "Extract rules for the following named yogas. "
            "One rule per yoga (or 3 rules for Vipreet Rajyoga variants).\n\n"
            + "\n\n".join(parts)
        )
        return self._call(TYPE_A_SYSTEM, prompt)

    def extract_type_b(self, section: dict) -> list[YogaRule]:
        """Extract category group bullet rules (Type B) — one section per call."""
        heading = section["heading"]
        parent  = section["parent"] or ""
        bullets = "\n".join(f"  - {l}" for l in section["lines"])
        prompt = (
            f"Category: {parent + ' → ' if parent else ''}{heading}\n\n"
            f"Bullet rules to extract (one rule per bullet):\n{bullets}\n\n"
            "Extract one YogaRule per bullet point."
        )
        return self._call(TYPE_B_SYSTEM, prompt)


# ── Section classifier ─────────────────────────────────────────────────────────

# Type B: category groups — bullets only, no named yoga formation text
TYPE_B_HEADINGS = {
    "Long life", "Medium Life", "Short Life",
    "Yogas For Low Morale", "Yogas For Deafness", "Yogas For Dumbness",
    "Yogas For Speech Defects", "Yogas For Eye Troubles",
    "Yogas For Wealth", "Yogas For Sudden Gains Through Speculation Or Gambling",
    "Yogas For Co-Borns", "Yogas For Conveyance", "Yogas For Progeny",
    "Timely Marriage", "Late Marriage", "No Marriage",
    "Auspicious - Inauspicious Yogas",
}

# Sections to skip (meta headings, no rule content)
SKIP_HEADINGS = {
    "Arishta Yoga",       # container only — has intro text but sub-groups carry the rules
    "Yogas For Marriage", # container only
}


def classify(section: dict) -> str:
    """Return 'type_a', 'type_b', or 'skip'."""
    h = section["heading"]
    if h in SKIP_HEADINGS:
        return "skip"
    if h in TYPE_B_HEADINGS:
        return "type_b"
    # Named yogas: end in "Yoga"/"yoga" or "Dosha"/"dosha"
    h_lower = h.lower()
    if h_lower.endswith("yoga") or h_lower.endswith("dosha"):
        return "type_a"
    # Catch-all for category groups not explicitly listed
    if h.startswith("Yogas For "):
        return "type_b"
    return "skip"


# ── Rule builder ───────────────────────────────────────────────────────────────

def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _canon_planets(raw: list[str]) -> list[str]:
    lookup = {p.lower(): p for p in PLANETS}
    return [lookup[p.lower()] for p in raw if p.lower() in lookup]


def _life_domain(section: dict) -> str:
    h = (section["heading"] + " " + (section["parent"] or "")).lower()
    for key, domain in DOMAIN_MAP.items():
        if key in h:
            return domain
    return "general"


def build_rule(
    item: YogaRule,
    section: dict,
    batch_id: str,
    index: int,
    sec_type: str,
) -> dict:
    rule_id        = f"tba16-{index:03d}"
    condition_type = item.condition_type if item.condition_type in VALID_CONDITION_TYPES else (
        "dosha" if "dosha" in item.yoga_name.lower() else
        "yoga_combination" if sec_type == "type_a" else "general_principle"
    )
    sub_type = item.sub_type if item.sub_type in VALID_SUB_TYPES else (
        "yoga_formation" if sec_type == "type_a" else "neutral_rule"
    )
    planets_in = _canon_planets(item.planets_involved)
    houses_in  = [h for h in item.houses_involved if isinstance(h, int) and 1 <= h <= 12]
    life_domain = _life_domain(section)
    heading     = section["heading"]
    parent      = section["parent"] or ""
    sloka_base  = _slug(section["heading"])
    sloka       = f"cat-{sloka_base}" if sec_type == "type_b" else sloka_base

    yoga_name_clean = item.yoga_name.strip()
    condition_group_id = f"tba16-{sloka_base}"

    detailed = (
        f"Yoga/Category: {yoga_name_clean}\n\n"
        f"Condition: {item.full_condition.strip()}\n\n"
        f"Effect: {item.full_result.strip()}"
    )
    summary = f"{item.condition_summary} → {item.result_summary}"
    if len(summary) > 200:
        summary = summary[:197] + "..."

    # ── Physical markers ───────────────────────────────────────────────────────
    raw_markers = item.physical_markers or []
    physical_markers = []
    has_disability = False
    has_appearance = False
    for m in raw_markers:
        cat = m.category if m.category in PHYSICAL_CATEGORIES else "behavioral"
        pol = m.polarity if m.polarity in ("positive", "negative", "neutral") else "neutral"
        physical_markers.append({
            "category":    cat,
            "description": m.description.strip(),
            "polarity":    pol,
        })
        if cat == "disability":
            has_disability = True
        if cat in ("body_build", "height", "facial_features", "complexion", "body_marks"):
            has_appearance = True

    # ── Tags ───────────────────────────────────────────────────────────────────
    tags = [
        "verbatim", "yoga", f"chapter{CHAPTER}", "ai_extracted",
        condition_type, sub_type,
        f"group:{condition_group_id}",
    ]
    if parent:
        tags.append(f"parent:{_slug(parent)}")
    if item.is_benefic:
        tags.append("benefic")
    else:
        tags.append("malefic")
    if physical_markers:
        tags.append("has_physical_markers")
    if has_disability:
        tags.append("disability")
    if has_appearance:
        tags.append("physical_appearance")

    return {
        "rule_id":    rule_id,
        "science_id": SCIENCE,
        "source": {
            "book":           BOOK,
            "book_id":        BOOK_ID,
            "chapter":        CHAPTER,
            "chapter_name":   CHAP_NAME,
            "sloka":          sloka,
            "batch_id":       batch_id,
            "primary":        BOOK,
            "page_ref":       None,
            "passage_ref_id": None,
        },
        "condition": {
            "type":               condition_type,
            "sub_type":           sub_type,
            "sloka":              sloka,
            "heading":            heading,
            "parent_category":    parent or None,
            "yoga_name":          yoga_name_clean,
            "planets_involved":   planets_in,
            "houses_involved":    houses_in,
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     "neutral",
            "condition_group_id": condition_group_id,
            "is_group_summary":   False,
            "is_benefic":         item.is_benefic,
        },
        "interpretation": {
            "summary":            summary,
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        life_domain,
            "tags":               tags,
            # Physical appearance / disability / behavioural markers
            # Queryable separately: db.find({"interpretation.physical_markers.category": "disability"})
            "physical_markers":   physical_markers,
        },
        "metadata": {
            "planets_involved":     planets_in,
            "houses_involved":      houses_in,
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "condition_group_id":   condition_group_id,
            "is_group_summary":     False,
            "has_physical_markers": bool(physical_markers),
            "physical_categories":  sorted({m["category"] for m in physical_markers}),
        },
        "confidence": {
            "base": 0.87, "source_weight": 0.90, "cross_book_multiplier": 1.0,
        },
        "approval_status": "pending_review",
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


# ── MongoDB helpers ────────────────────────────────────────────────────────────

def mongo_update_many(col, docs: list[dict], dry_run: bool) -> int:
    if dry_run or not docs:
        return 0
    inserted = 0
    for attempt in range(3):
        try:
            from pymongo import UpdateOne
            ops = [
                UpdateOne(
                    {"rule_id": d["rule_id"]},
                    {"$setOnInsert": d},
                    upsert=True,
                )
                for d in docs
            ]
            result = col.bulk_write(ops, ordered=False)
            inserted = result.upserted_count
            break
        except AutoReconnect:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise
    return inserted


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest A Text-Book of Astrology Ch 16 — Yogas"
    )
    parser.add_argument("--rtf",       required=True, help="Path to RTF file")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   required=True)
    parser.add_argument("--model",     default="claude-haiku-4-5")
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()

    batch_id = f"tba-ch16-v1-{datetime.now(timezone.utc).strftime('%Y%m%d')}"

    print(f"\nA Text-Book of Astrology — Chapter 16  [v1 AI extraction]")
    print(f"Model : {args.model}  |  batch_id : {batch_id}")
    print(f"{'─' * 65}")

    # ── Parse RTF ──────────────────────────────────────────────────────────────
    print("\nParsing RTF...")
    sections = parse_rtf(args.rtf)
    type_a_secs = [s for s in sections if classify(s) == "type_a"]
    type_b_secs = [s for s in sections if classify(s) == "type_b"]
    skip_secs   = [s for s in sections if classify(s) == "skip"]

    print(f"  Type A (named yogas)     : {len(type_a_secs)} sections")
    print(f"  Type B (category groups) : {len(type_b_secs)} sections")
    print(f"  Skipped (containers)     : {len(skip_secs)} sections")

    if not (type_a_secs or type_b_secs):
        print("\n⚠  No sections detected — check RTF path and parser.")
        return

    extractor  = Extractor(model=args.model)
    all_rules: list[dict] = []
    idx = 1

    # ── Type A: Named yogas — batch 6 per API call ─────────────────────────────
    BATCH_SIZE = 6
    print(f"\n── Type A: Named Yogas ({len(type_a_secs)} sections, batched {BATCH_SIZE}/call) ──")
    a_batches = [type_a_secs[i:i+BATCH_SIZE] for i in range(0, len(type_a_secs), BATCH_SIZE)]
    for batch_num, batch in enumerate(a_batches, 1):
        names = ", ".join(s["heading"] for s in batch)
        print(f"  Batch {batch_num}: {names}")
        print(f"  {'':5s}extracting...", end=" ", flush=True)
        extracted = extractor.extract_type_a(batch)
        if not extracted:
            print("⚠  no rules extracted")
            continue
        # Distribute extracted rules back to sections by yoga_name matching
        for item in extracted:
            # Find matching section (best-effort by yoga_name)
            matched = None
            for sec in batch:
                if item.yoga_name.lower() in sec["heading"].lower() or \
                   sec["heading"].lower() in item.yoga_name.lower():
                    matched = sec
                    break
            if not matched:
                matched = batch[0]  # fallback to first in batch
            rule = build_rule(item, matched, batch_id, idx, "type_a")
            all_rules.append(rule)
            idx += 1
        print(f"{len(extracted)} rules")

    # ── Type B: Category groups — one API call per section ────────────────────
    print(f"\n── Type B: Category Groups ({len(type_b_secs)} sections) ──")
    for sec in type_b_secs:
        label = f"{sec['parent'] + ' → ' if sec['parent'] else ''}{sec['heading']}"
        print(f"  {label[:50]:50s} extracting...", end=" ", flush=True)
        if not sec["lines"]:
            print("(no bullets — skipped)")
            continue
        extracted = extractor.extract_type_b(sec)
        if not extracted:
            print("⚠  no rules extracted")
            continue
        for item in extracted:
            rule = build_rule(item, sec, batch_id, idx, "type_b")
            all_rules.append(rule)
            idx += 1
        print(f"{len(extracted)} rules")

    # ── Summary ────────────────────────────────────────────────────────────────
    if not all_rules:
        print("\n⚠  No rules extracted. Check RTF path and ANTHROPIC_API_KEY.")
        return

    condition_types: dict[str, int] = {}
    sub_types: dict[str, int] = {}
    benefic_count = 0
    for r in all_rules:
        ct = r["condition"]["type"]
        st = r["condition"]["sub_type"]
        condition_types[ct] = condition_types.get(ct, 0) + 1
        sub_types[st]       = sub_types.get(st, 0) + 1
        if r["condition"].get("is_benefic"):
            benefic_count += 1

    print(f"\n{'─' * 65}")
    print("Condition type breakdown:")
    for ct, cnt in sorted(condition_types.items(), key=lambda x: -x[1]):
        print(f"  {ct:<25s} : {cnt}")
    print("\nSub-type breakdown:")
    for st, cnt in sorted(sub_types.items(), key=lambda x: -x[1]):
        print(f"  {st:<25s} : {cnt}")
    print(f"  {'─' * 35}")
    print(f"  {'TOTAL':<25s} : {len(all_rules)}")
    print(f"\nBenefic rules  : {benefic_count}")
    print(f"Adverse rules  : {len(all_rules) - benefic_count}")
    print(f"\nIsolation: approval_status='pending_review' — zero rules reach live users")

    if args.dry_run:
        # Physical marker summary
        pm_rules  = [r for r in all_rules if r["metadata"].get("has_physical_markers")]
        pm_cats: dict[str, int] = {}
        for r in pm_rules:
            for cat in r["metadata"].get("physical_categories", []):
                pm_cats[cat] = pm_cats.get(cat, 0) + 1
        print(f"\nPhysical markers found in {len(pm_rules)} rules:")
        for cat, cnt in sorted(pm_cats.items(), key=lambda x: -x[1]):
            print(f"  {cat:<20s} : {cnt}")

        print("\n[DRY RUN] — no changes written to MongoDB")
        print("\nSample rules (first 8):")
        for r in all_rules[:8]:
            c = r["condition"]
            interp = r["interpretation"]
            markers = interp.get("physical_markers", [])
            print(f"\n  {r['rule_id']}")
            print(f"    yoga_name    : {c.get('yoga_name','—')[:55]}")
            print(f"    type         : {c['type']} / {c['sub_type']}")
            print(f"    planets      : {c['planets_involved']}")
            print(f"    houses       : {c['houses_involved']}")
            print(f"    is_benefic   : {c.get('is_benefic','—')}")
            print(f"    summary      : {interp['summary'][:90]}")
            if markers:
                print(f"    physical_markers ({len(markers)}):")
                for m in markers:
                    print(f"      [{m['category']}/{m['polarity']}] {m['description'][:70]}")
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
