#!/usr/bin/env python3
"""
Phase 4C -- Layer C: Interpretation Quality (LLM-as-Judge)
──────────────────────────────────────────────────────────
Layer B confirms the RIGHT TOPICS fire. Layer C confirms the interpretation
TEXT is accurate and faithful to the source textbook.

A rule can correctly fire on claim_axis="career" but have generic, wrong,
or context-mismatched interpretation text. Layer B cannot catch this.
Layer C (LLM-as-Judge ≥4.5/5) is the mandatory gate before KE-OP-4
(co-founder sign-off).

For each evaluated test vector this script:
  1. Re-computes the Vedic chart from birth data
  2. Re-runs _condition_matches against the rule corpus
  3. Samples ≤MAX_RULES_PER_VECTOR fired rules (true positives first)
  4. Calls Claude as judge for each (rule, vector) pair with a rubric prompt
  5. Scores on 5 dimensions (each 1-5): accuracy, specificity, fidelity,
     contextual_fit, overall
  6. Writes per-rule scores to rule_evaluation.layer_c in each vector JSON
  7. Produces summary statistics and a gate result

Rubric (each dimension 1-5):
  accuracy        - Is the interpretation text factually correct for this
                    chart configuration? (Does Saturn in 8H really give X?)
  specificity     - Is the prediction specific enough to be actionable?
                    5 = precise, 1 = could apply to almost anyone
  fidelity        - Does the rule text faithfully represent the textbook
                    observation without distortion or added meaning?
  contextual_fit  - Given this person's documented life outcomes (author
                    observations), does the interpretation make sense for them?
  overall         - Holistic quality score

Gate: average overall ≥ 4.5/5 across all judged rules.

Usage (from repo root):
  MONGO_URL="..." ANTHROPIC_API_KEY="..." python3 KE_TEXTBOOK_DECODE/phase4_layer_c.py
  MONGO_URL="..." ANTHROPIC_API_KEY="..." python3 KE_TEXTBOOK_DECODE/phase4_layer_c.py --book 300h1
  MONGO_URL="..." ANTHROPIC_API_KEY="..." python3 KE_TEXTBOOK_DECODE/phase4_layer_c.py --book all --max-rules 3
  MONGO_URL="..." ANTHROPIC_API_KEY="..." python3 KE_TEXTBOOK_DECODE/phase4_layer_c.py --dry-run  (chart + matching only, no LLM calls)

Environment:
  MONGO_URL        required -- Render MongoDB connection string
  ANTHROPIC_API_KEY required (unless --dry-run)

Options:
  --book           one of: 300h1 | 300h2 | longevity_unnatural | longevity_astro_system | all
  --max-rules N    max rules to judge per vector (default: 5)
  --max-vectors N  max vectors to process per book (default: unlimited)
  --model          claude model to use as judge (default: claude-sonnet-4-6)
  --dry-run        skip LLM calls, report what would be judged
  --no-write       skip writing scores back to vector JSON files
"""

from __future__ import annotations
import sys, os, json, asyncio, argparse, re, random
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from collections import defaultdict

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "backend"))

import swisseph as swe
from motor.motor_asyncio import AsyncIOMotorClient
from vedic_calculator import (
    _parse_datetime_to_jd, _lon_to_sign, _calc_planet, _calc_ascendant,
    _setup_swe, get_house_number, get_nakshatra, geocode_place,
    calculate_vimshottari_dasha, get_current_dasha,
    is_planet_combust, get_planet_dignity,
    DASHA_ORDER,
)
from knowledge_engine import extract_chart_facts, _condition_matches

try:
    from mundane_engine import mundane_scan as _mundane_scan
    _MUNDANE_AVAILABLE = True
except ImportError:
    _MUNDANE_AVAILABLE = False
    async def _mundane_scan(*_a, **_kw):  # type: ignore[misc]
        return {"fired_rules": [], "triple_confirmation": False,
                "mundane_polarity": None, "top_mundane_factor": None}

# ── Config ──────────────────────────────────────────────────────────────────
BOOKS = {
    "300h1":                  "KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h1/",
    "300h2":                  "KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h2/",
    "longevity_unnatural":    "KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_unnatural/",
    "longevity_astro_system": "KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_astro_system/",
}
KP_BOOKS = {"300h1", "300h2", "longevity_unnatural", "longevity_astro_system"}

DB_NAME          = "horoscope_db"
RULES_COLLECTION = "interpretation_rules"
RULE_STATUSES    = ["approved", "auto_approved", "pending_human_review"]

# Condition types that are engine setup docs or methodology notes -- not interpretation
# rules. They exist in the collection but must not be evaluated by Layer C.
LAYER_C_EXCLUDED_COND_TYPES = frozenset({
    "engine_specification",
    "methodology",
    "transit_rule",
    "transit_vedha",
    "transit_condition",
    "transit",
    "remedy_trigger",        # handled by Remedies Engine, not KE
})

DEFAULT_MODEL    = "claude-sonnet-4-6"
LAYER_C_GATE     = 4.5       # average overall score required to pass
MAX_CONCURRENT   = 4         # max parallel LLM calls

# ── Mundane engine config ─────────────────────────────────────────────────────
# Fixed at run start so every vector in a run uses the same macro snapshot.
_RUN_QUERY_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

NATIONALITY_TO_CC: dict[str, str] = {
    "american":    "US",
    "indian":      "IN",
    "british":     "GB",
    "french":      "FR",
    "german":      "DE",
    "chinese":     "CN",
    "japanese":    "JP",
    "russian":     "RU",
    "australian":  "AU",
    "canadian":    "CA",
    "italian":     "IT",
    "brazilian":   "BR",
    "south korean": "KR",
    "saudi":       "SA",
    "pakistani":   "PK",
}

def _get_query_config(vector: dict) -> tuple[str, str]:
    """Return (country_code, query_date) for mundane engine queries on this vector."""
    nat = ((vector.get("subject") or {}).get("nationality") or "").lower().strip()
    cc  = NATIONALITY_TO_CC.get(nat, "IN")  # default India -- home of classical texts
    return cc, _RUN_QUERY_DATE

LOG_DIR = REPO_ROOT / "KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ── AXIS_NORM (mirrors phase4_layer_b.py) ────────────────────────────────────
AXIS_NORM = {
    "career_growth":        "career",
    "career_timing":        "career",
    "career_trend":         "career",
    "career_status":        "career",
    "general":              "general",
    "general_trend":        "general",
    "general_fortune":      "general",
    "wealth_trend":         "wealth",
    "financial_security":   "wealth",
    "career_finance":       "career",
    "financial":            "wealth",
    "property":             "wealth",
    "marriage_timing":      "marriage",
    "relationship_quality": "marriage",
    "relationships_trend":  "marriage",
    "relationships":        "marriage",
    "partnership_stability":"marriage",
    "romance":              "marriage",
    "spouse":               "marriage",
    "compatibility":        "marriage",
    "health_vitality":      "health",
    "health_trend":         "health",
    "medical":              "health",
    "accident_risk":        "health",
    "longevity_trend":      "longevity",
    "longevity":            "longevity",
    "spiritual_growth":     "spirituality",
    "spirituality_trend":   "spirituality",
    "spirituality_dharma":  "spirituality",
    "children":             "children",
    "progeny":              "children",
    "education_trend":      "education",
    "education":            "education",
    "enemies_adversaries":  "enemies",
    "enemies":              "enemies",
    "legal_status":         "enemies",
    "legal":                "enemies",
    "past_lives":           "past_lives",
    "destiny":              "past_lives",
    "life_path":            "past_lives",
    "travel_pattern":       "travel",
    "travel":               "travel",
    "learning_outcome":     "education",
    "social":               "social",
    "social_network":       "social",
    "family":               "family",
    "family_life":          "family",
    "family_relationships": "family",
}

def _norm_axis(ax: str) -> str:
    return AXIS_NORM.get(ax, ax)


# ── Tee logging ───────────────────────────────────────────────────────────────
ts       = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
log_path = LOG_DIR / f"phase4_layer_c_{ts}.log"

class Tee:
    def __init__(self, fp: Path):
        self._f = open(fp, "w", encoding="utf-8")
    def write(self, d: str):
        sys.__stdout__.write(d); self._f.write(d)
    def flush(self):
        sys.__stdout__.flush(); self._f.flush()
    def close(self):
        self._f.close()

tee = Tee(log_path)
sys.stdout = tee


# ── Chart builder (mirrors phase4_layer_b.py) ─────────────────────────────────
_geocode_cache: dict = {}

def tz_str_from_offset(offset_hours: float, lon_fallback: float = 0.0) -> str:
    sign = "+" if offset_hours >= 0 else "-"
    total_min = int(abs(offset_hours) * 60)
    h, m = divmod(total_min, 60)
    return f"{sign}{h:02d}:{m:02d}"


def build_chart(bd: dict, use_kp: bool) -> tuple[Optional[dict], str]:
    """Build chart dict using pyswisseph directly -- exact mirror of phase4_layer_b.py."""
    date = bd.get("date")
    t    = str(bd.get("time_local") or "")[:5]
    if not date or not t or t in ("", "None", "00:00"):
        return None, "no_time"

    tz_off = bd.get("timezone_offset_hours")
    lat    = bd.get("latitude")
    lon    = bd.get("longitude")

    if lat is None or lon is None:
        place = bd.get("place") or ""
        if place and place not in _geocode_cache:
            try:
                _geocode_cache[place] = geocode_place(place)
            except Exception:
                _geocode_cache[place] = None
        coords = _geocode_cache.get(place)
        if not coords:
            return None, "no_coords"
        lat, lon = coords  # geocode_place returns (lat, lon) tuple

    if tz_off is None:
        tz_off = lon / 15.0

    tz_str = tz_str_from_offset(float(tz_off), lon_fallback=lon)

    try:
        if use_kp:
            swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
        else:
            swe.set_sid_mode(swe.SIDM_LAHIRI)

        jd         = _parse_datetime_to_jd(date, t, tz_str)
        asc_lon    = _calc_ascendant(jd, lat, lon)
        lagna_sign = _lon_to_sign(asc_lon)

        sun_lon, _ = _calc_planet(jd, swe.SUN)

        PLANET_MAP = {
            'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS,
            'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER,
            'Venus': swe.VENUS, 'Saturn': swe.SATURN,
            'Rahu': swe.MEAN_NODE, 'Ketu': None,
        }
        planets: dict = {}
        for pname, swe_id in PLANET_MAP.items():
            if pname == 'Ketu':
                rahu_lon, _ = _calc_planet(jd, swe.MEAN_NODE)
                p_lon = (rahu_lon + 180.0) % 360
                speed = 0.0
            else:
                p_lon, speed = _calc_planet(jd, swe_id)
            p_sign   = _lon_to_sign(p_lon)
            deg      = round(p_lon % 30, 2)
            house    = get_house_number(p_sign, lagna_sign)
            nak_data = get_nakshatra(p_lon)
            dignity  = get_planet_dignity(pname, p_sign, deg)
            combust  = is_planet_combust(pname, p_lon, sun_lon) if pname not in ('Sun', 'Rahu', 'Ketu') else False
            retro    = speed < 0 and pname not in ('Rahu', 'Ketu')
            planets[pname] = {
                'sign': p_sign, 'degree': deg, 'house': house,
                'nakshatra': nak_data.get('name'), 'dignity': dignity,
                'retrograde': retro, 'combust': combust,
                'longitude': round(p_lon, 4),
            }

        sign_list = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
                     'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
        lagna_idx = sign_list.index(lagna_sign)
        houses    = {h: sign_list[(lagna_idx + h - 1) % 12] for h in range(1, 13)}

        moon_lon      = planets['Moon']['longitude']
        dashas        = calculate_vimshottari_dasha(date, moon_lon)
        current_dasha = get_current_dasha(dashas)

        chart = {
            'lagna': {'sign': lagna_sign, 'degree': round(asc_lon % 30, 2)},
            'planets': planets, 'houses': houses,
            'moon_longitude': moon_lon, 'current_dasha': current_dasha,
            'layers': {'vimshottari_dasha': {'dasha_lord': current_dasha.get('planet', '')}},
        }
        return chart, ""
    except Exception as e:
        return None, str(e)[:120]


# ── Rule text helpers ─────────────────────────────────────────────────────────

def _rule_interpretation(rule: dict) -> str:
    interp = rule.get("interpretation") or {}
    if isinstance(interp, dict):
        detailed = interp.get("detailed") or ""
        brief    = interp.get("brief") or ""
        return detailed if len(detailed) > len(brief) else (brief or detailed)
    return str(interp)


def _format_mundane_ctx(ctx: dict | None, claim_axis: str) -> str:
    """Format mundane engine result for inclusion in judge prompt."""
    if not ctx or ctx.get("error") or not _MUNDANE_AVAILABLE:
        return "(Mundane engine unavailable or no signals for this axis.)"
    triple   = ctx.get("triple_confirmation", False)
    polarity = ctx.get("mundane_polarity") or "neutral"
    top      = ctx.get("top_mundane_factor") or "none identified"
    fired    = ctx.get("fired_rules", [])
    lines    = [
        f"Triple Confirmation active: {'YES -- natal + macro + core event all align' if triple else 'No'}",
        f"Macro polarity for '{claim_axis}': {polarity}",
        f"Top macro factor: {top}",
        f"Active mundane signals ({len(fired)} rules fired):",
    ]
    for r in (fired or [])[:3]:
        interp = (r.get("interpretation") or r.get("description") or "")[:120]
        if interp:
            lines.append(f"  • {interp}")
    if not fired:
        lines.append("  (No mundane rules fired for this axis / date.)")
    return "\n".join(lines)


def _rule_summary(rule: dict) -> str:
    """Compact rule description for the judge prompt."""
    rid   = rule.get("rule_id", "?")
    axis  = rule.get("claim_axis", "?")
    cond  = rule.get("condition") or {}
    book  = (rule.get("source") or {}).get("book") or "?"
    ch    = (rule.get("source") or {}).get("chapter") or "?"
    interp = _rule_interpretation(rule)
    decode = rule.get("decode_notes") or ""
    return (
        f"Rule ID: {rid}\n"
        f"Source: {book} / {ch}\n"
        f"Claim axis: {axis}\n"
        f"Condition type: {cond.get('type','?')}  planet: {cond.get('planet','')}  house: {cond.get('house','')}\n"
        f"Interpretation: {interp[:500]}\n"
        f"Decode notes: {decode[:200]}"
    )


# ── Judge prompt ──────────────────────────────────────────────────────────────

JUDGE_SYSTEM = """You are an expert Vedic astrology evaluator. You are assessing the quality of
interpretation rules extracted from classical Jyotish textbooks for use in an AI-powered
astrology platform. Your task is to evaluate whether a rule's interpretation text is accurate,
specific, and faithful to classical Jyotish teaching.

You must respond with ONLY a valid JSON object. No explanatory text before or after the JSON."""

JUDGE_PROMPT_TEMPLATE = """You are evaluating a Knowledge Engine interpretation rule for quality.

## Test Subject
Name: {subject_name}
Description: {subject_desc}
Life outcomes documented by textbook author: {author_observations}

## Chart (computed by KP/Vedic engine)
Lagna (Ascendant): {lagna}
Moon sign: {moon_sign}
Current Dasha: {dasha_info}

## Mundane Environment (query date: {query_date})
{mundane_context}

## Rule Being Evaluated
{rule_summary}

---

## Evaluation Task

Score the rule on each dimension from 1 to 5 (integers only):

1. **accuracy** (1-5): Is the interpretation text factually accurate for this Vedic chart configuration?
   5 = perfectly accurate per classical Jyotish | 1 = factually wrong or contradicts the chart

2. **specificity** (1-5): Is the prediction specific enough to be useful?
   5 = very specific, names exact domains/outcomes | 1 = so generic it applies to anyone

3. **fidelity** (1-5): Does the interpretation faithfully represent the source textbook observation?
   5 = verbatim or faithful paraphrase | 1 = distorted, meaning changed, or content added

4. **contextual_fit** (1-5): Given this person's documented life outcomes, does firing this rule make sense for them?
   5 = clearly supported by their life story | 1 = rule fires but is irrelevant to their life

5. **overall** (1-5): Holistic interpretation quality score.
   5 = excellent rule, ready for production | 1 = must be rewritten or excluded

Also provide a brief **reasoning** (1-2 sentences) explaining your scores.

Respond with ONLY this JSON (no markdown, no extra text):
{{
  "accuracy": <int>,
  "specificity": <int>,
  "fidelity": <int>,
  "contextual_fit": <int>,
  "overall": <int>,
  "reasoning": "<string>"
}}"""


def _build_judge_prompt(vector: dict, rule: dict, chart: dict,
                        mundane_ctx: dict | None = None) -> str:
    subj   = vector.get("subject") or {}
    name   = subj.get("name") or "Unknown"
    desc   = subj.get("description") or ""
    obs    = vector.get("author_observations") or []
    obs_text = "; ".join(
        o.get("verbatim", "") for o in obs
        if not o.get("gap_flag") and o.get("verbatim")
    )[:600]
    if not obs_text:
        obs_text = "(no direct observations from textbook author)"

    cv     = chart.get("chart_data", chart) if "chart_data" in chart else chart
    lagna  = (cv.get("lagna") or cv.get("ascendant") or {}).get("sign") or "?"
    moon   = ""
    planets_raw = cv.get("planets") or {}
    if isinstance(planets_raw, dict):
        moon = (planets_raw.get("Moon") or {}).get("sign") or "?"
    else:
        for p in planets_raw:
            if (p.get("name") or "").lower() == "moon":
                moon = p.get("sign") or "?"
                break
    dasha_info = "?"
    try:
        dl = cv.get("layers", {}).get("vimshottari_dasha") or {}
        md = dl.get("mahadasha", {})
        ad = dl.get("antardasha", {})
        dasha_info = f"{md.get('planet','?')} Mahadasha / {ad.get('planet','?')} Antardasha"
    except Exception:
        pass

    claim_axis = rule.get("claim_axis", "")
    _, query_date = _get_query_config(vector)
    mundane_text = _format_mundane_ctx(mundane_ctx, claim_axis)

    return JUDGE_PROMPT_TEMPLATE.format(
        subject_name=name,
        subject_desc=desc[:300],
        author_observations=obs_text,
        lagna=lagna,
        moon_sign=moon,
        dasha_info=dasha_info,
        rule_summary=_rule_summary(rule),
        mundane_context=mundane_text,
        query_date=query_date,
    )


# ── LLM judge call ────────────────────────────────────────────────────────────

async def _judge_rule(
    client,          # anthropic.AsyncAnthropic
    vector: dict,
    rule:   dict,
    chart:  dict,
    model:  str,
    sem:    asyncio.Semaphore,
    mundane_ctx: dict | None = None,
) -> Optional[dict]:
    """Call Claude to score one (rule, vector) pair. Returns score dict or None."""
    async with sem:
        try:
            prompt = _build_judge_prompt(vector, rule, chart, mundane_ctx)
            resp = await client.messages.create(
                model=model,
                max_tokens=256,
                system=JUDGE_SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()
            # Strip any accidental markdown fences
            raw = re.sub(r"^```json\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            scores = json.loads(raw)
            # Validate shape
            for dim in ("accuracy", "specificity", "fidelity", "contextual_fit", "overall"):
                if dim not in scores:
                    scores[dim] = 0
                scores[dim] = max(1, min(5, int(scores[dim])))
            scores["rule_id"] = rule.get("rule_id", "?")
            scores["claim_axis"] = rule.get("claim_axis", "?")
            return scores
        except Exception as e:
            return {
                "rule_id": rule.get("rule_id", "?"),
                "claim_axis": rule.get("claim_axis", "?"),
                "error": str(e)[:120],
                "accuracy": 0, "specificity": 0,
                "fidelity": 0, "contextual_fit": 0, "overall": 0,
            }


# ── Process one book ──────────────────────────────────────────────────────────

async def process_book(
    book_name: str,
    book_path: str,
    all_rules: list[dict],
    client,
    model: str,
    max_rules_per_vector: int,
    max_vectors: int,
    dry_run: bool,
    no_write: bool,
    skip_judged: bool = False,
    db=None,
) -> dict:
    use_kp    = book_name in KP_BOOKS
    book_dir  = REPO_ROOT / book_path

    vector_files = sorted(
        p for p in book_dir.glob("tv_*.json")
        if p.is_file()
    )

    book_stats = {
        "book": book_name,
        "vectors_processed": 0,
        "vectors_skipped": 0,
        "rules_judged": 0,
        "scores": [],                   # all individual overall scores
        "dimension_totals": defaultdict(float),
        "dimension_counts": defaultdict(int),
        "error_count": 0,
    }

    sem = asyncio.Semaphore(MAX_CONCURRENT)

    processed = 0
    for vf in vector_files:
        if max_vectors and processed >= max_vectors:
            break

        with open(vf, encoding="utf-8") as f:
            vector = json.load(f)

        # Skip if Layer B not evaluated
        re_block = vector.get("rule_evaluation") or {}
        if not re_block.get("evaluated"):
            book_stats["vectors_skipped"] += 1
            continue

        # Skip vectors already judged by Layer C (for batching)
        if skip_judged and re_block.get("layer_c"):
            book_stats["vectors_skipped"] += 1
            continue

        bd = vector.get("birth_data") or {}
        chart, err = build_chart(bd, use_kp)
        if not chart:
            book_stats["vectors_skipped"] += 1
            continue

        # Get expected axes from non-gap observations
        expected_axes = set(
            _norm_axis(o.get("claim_axis") or "")
            for o in (vector.get("author_observations") or [])
            if not o.get("gap_flag") and o.get("claim_axis")
        )
        if not expected_axes:
            book_stats["vectors_skipped"] += 1
            continue

        # Run condition matching to find fired rules
        try:
            facts = extract_chart_facts(chart)
        except Exception:
            book_stats["vectors_skipped"] += 1
            continue

        fired_tp: list[dict] = []   # true positives: fired AND in expected_axes
        fired_fp: list[dict] = []   # false positives: fired but NOT in expected_axes

        for rule in all_rules:
            cond = rule.get("condition") or {}
            # Skip non-interpretation condition types (engine specs, transit, remedies)
            if isinstance(cond, dict) and cond.get("type") in LAYER_C_EXCLUDED_COND_TYPES:
                continue
            try:
                if _condition_matches(cond, facts):
                    norm = _norm_axis(rule.get("claim_axis") or "")
                    if norm in expected_axes:
                        fired_tp.append(rule)
                    else:
                        fired_fp.append(rule)
            except Exception:
                pass

        # Sample: shuffle TPs first so each run explores different rules from
        # the fired set -- prevents broad-firing rules from dominating every vector.
        random.shuffle(fired_tp)
        random.shuffle(fired_fp)
        tp_sample = fired_tp[:max(max_rules_per_vector - 1, 1)]
        fp_sample  = fired_fp[:1]  # one false-positive sample per vector
        sample_rules = tp_sample + fp_sample
        sample_rules = sample_rules[:max_rules_per_vector]

        if not sample_rules:
            book_stats["vectors_skipped"] += 1
            continue

        vid = vector.get("vector_id", vf.stem)
        print(f"  [{book_name}] {vid}: {len(fired_tp)} TP + {len(fired_fp)} FP  →  judging {len(sample_rules)} rules")

        if dry_run:
            book_stats["vectors_processed"] += 1
            processed += 1
            continue

        # ── Mundane context: one query per unique claim_axis ────────────────
        # Calls Mundane V22 Tools (mundane_scan) for each axis in sampled rules
        # so the LLM judge can evaluate Triple Confirmation and macro alignment.
        cc, query_date = _get_query_config(vector)
        axis_mundane: dict[str, dict] = {}
        if db is not None and _MUNDANE_AVAILABLE:
            unique_axes = {_norm_axis(r.get("claim_axis") or "") for r in sample_rules}
            for ax in unique_axes:
                if ax and ax not in axis_mundane:
                    try:
                        axis_mundane[ax] = await _mundane_scan(
                            claim_axis=ax,
                            query_date=query_date,
                            country_code=cc,
                            db=db,
                        )
                    except Exception as me:
                        axis_mundane[ax] = {"error": str(me), "fired_rules": [],
                                            "triple_confirmation": False}
            if any(v.get("triple_confirmation") for v in axis_mundane.values()):
                print(f"    ⭐ Triple Confirmation active for {vid} (cc={cc} date={query_date})")

        # Judge all sampled rules concurrently
        tasks = [
            _judge_rule(client, vector, rule, chart, model, sem,
                        mundane_ctx=axis_mundane.get(_norm_axis(rule.get("claim_axis") or "")))
            for rule in sample_rules
        ]
        results = await asyncio.gather(*tasks)

        rule_scores: list[dict] = []
        for score in results:
            if score is None:
                continue
            if "error" in score:
                book_stats["error_count"] += 1
                print(f"    ⚠️  judge error for {score['rule_id']}: {score['error']}")
                continue
            rule_scores.append(score)
            book_stats["scores"].append(score["overall"])
            book_stats["rules_judged"] += 1
            for dim in ("accuracy", "specificity", "fidelity", "contextual_fit", "overall"):
                if score.get(dim, 0) > 0:
                    book_stats["dimension_totals"][dim] += score[dim]
                    book_stats["dimension_counts"][dim] += 1
            print(f"    {score['rule_id']:40s}  overall={score['overall']}  "
                  f"acc={score['accuracy']} spec={score['specificity']} "
                  f"fid={score['fidelity']} ctx={score['contextual_fit']}  "
                  f"\"{score.get('reasoning','')[:80]}\"")

        # Write back to vector JSON
        if not no_write and rule_scores:
            vector["rule_evaluation"]["layer_c"] = {
                "evaluated_at": ts,
                "model": model,
                "rules_judged": len(rule_scores),
                "avg_overall": round(sum(s["overall"] for s in rule_scores) / len(rule_scores), 2),
                "gate": LAYER_C_GATE,
                "gate_pass": (sum(s["overall"] for s in rule_scores) / len(rule_scores)) >= LAYER_C_GATE,
                "scores": rule_scores,
            }
            with open(vf, "w", encoding="utf-8") as f:
                json.dump(vector, f, indent=2, ensure_ascii=False)

        book_stats["vectors_processed"] += 1
        processed += 1

    return book_stats


# ── Main ──────────────────────────────────────────────────────────────────────

async def main(args: argparse.Namespace) -> None:
    mongo_url   = os.environ.get("MONGO_URL")
    api_key     = os.environ.get("ANTHROPIC_API_KEY")
    dry_run     = args.dry_run
    no_write    = args.no_write or dry_run

    print(f"Log saved → {log_path}\n")
    print("=" * 70)
    print(f"Phase 4C -- Layer C: LLM-as-Judge  [{('DRY RUN' if dry_run else 'LIVE')}]")
    print(f"DB: {DB_NAME} | Model: {args.model}")
    print(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 70)
    print()

    if not mongo_url:
        print("ERROR: MONGO_URL not set.", file=sys.stderr)
        sys.exit(1)
    if not api_key and not dry_run:
        print("ERROR: ANTHROPIC_API_KEY not set. Use --dry-run to skip LLM calls.", file=sys.stderr)
        sys.exit(1)

    # Load Anthropic client
    anthropic_client = None
    if not dry_run:
        try:
            import anthropic as anthropic_sdk
            anthropic_client = anthropic_sdk.AsyncAnthropic(api_key=api_key)
        except ImportError:
            print("ERROR: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
            sys.exit(1)

    # Load rules from MongoDB
    print("Loading rules from MongoDB ...")
    mongo_client = AsyncIOMotorClient(mongo_url)
    db   = mongo_client[DB_NAME]
    coll = db[RULES_COLLECTION]

    all_rules = await coll.find(
        {"active": True, "approval_status": {"$in": RULE_STATUSES}},
        {
            "_id": 0, "rule_id": 1, "claim_axis": 1, "secondary_axis": 1,
            "condition": 1, "interpretation": 1, "decode_notes": 1, "source": 1,
        }
    ).to_list(length=None)
    print(f"Loaded {len(all_rules):,} rules")
    print()

    # Select books to process
    books_to_run: dict[str, str] = {}
    if args.book == "all":
        books_to_run = BOOKS
    elif args.book in BOOKS:
        books_to_run = {args.book: BOOKS[args.book]}
    else:
        print(f"ERROR: unknown book '{args.book}'. Choose: {' | '.join(BOOKS)} | all")
        sys.exit(1)

    # Process books
    all_book_stats: list[dict] = []
    for book_name, book_path in books_to_run.items():
        print(f"\n{'='*50}")
        print(f"BOOK: {book_name}")
        print(f"{'='*50}")
        stats = await process_book(
            book_name=book_name,
            book_path=book_path,
            all_rules=all_rules,
            client=anthropic_client,
            model=args.model,
            max_rules_per_vector=args.max_rules,
            max_vectors=args.max_vectors or 0,
            dry_run=dry_run,
            no_write=no_write,
            skip_judged=args.skip_judged,
            db=db,
        )
        all_book_stats.append(stats)

        # Per-book summary
        print()
        print(f"  Vectors processed : {stats['vectors_processed']}")
        print(f"  Vectors skipped   : {stats['vectors_skipped']}")
        print(f"  Rules judged      : {stats['rules_judged']}")
        if stats["scores"]:
            avg = sum(stats["scores"]) / len(stats["scores"])
            print(f"  Avg overall score : {avg:.2f} / 5.0  ({'✅ PASS' if avg >= LAYER_C_GATE else '❌ FAIL'} -- gate {LAYER_C_GATE})")
            for dim in ("accuracy", "specificity", "fidelity", "contextual_fit"):
                cnt = stats["dimension_counts"][dim]
                if cnt:
                    print(f"  Avg {dim:20s}: {stats['dimension_totals'][dim]/cnt:.2f}")

    # Cross-book summary
    print()
    print("=" * 70)
    print("LAYER C SUMMARY")
    print("=" * 70)
    total_judged = sum(s["rules_judged"] for s in all_book_stats)
    all_scores   = [sc for s in all_book_stats for sc in s["scores"]]
    print(f"  Total rules judged : {total_judged:,}")
    print(f"  Total errors       : {sum(s['error_count'] for s in all_book_stats)}")
    if all_scores:
        overall_avg = sum(all_scores) / len(all_scores)
        gate_pass   = overall_avg >= LAYER_C_GATE
        print(f"  Overall avg score  : {overall_avg:.2f} / 5.0")
        print(f"  Layer C gate ({LAYER_C_GATE}) : {'✅ PASS' if gate_pass else '❌ FAIL'}")
        score_dist = {i: all_scores.count(i) for i in range(1, 6)}
        print(f"  Score distribution : {score_dist}")
    else:
        if dry_run:
            print("  DRY RUN -- no LLM calls made. Re-run without --dry-run to score.")
        else:
            print("  No rules were judged.")
    print()
    print(f"Log → {log_path}")
    tee.close()
    mongo_client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 4C -- Layer C LLM-as-Judge")
    parser.add_argument("--book",        default="all",
                        help="Book to test: 300h1 | 300h2 | longevity_unnatural | longevity_astro_system | all")
    parser.add_argument("--max-rules",   type=int, default=5,
                        help="Max rules to judge per test vector (default: 5)")
    parser.add_argument("--max-vectors", type=int, default=0,
                        help="Max vectors per book (0 = all)")
    parser.add_argument("--model",       default=DEFAULT_MODEL,
                        help=f"Claude model to use as judge (default: {DEFAULT_MODEL})")
    parser.add_argument("--dry-run",     action="store_true",
                        help="Compute charts and matching but skip LLM calls")
    parser.add_argument("--no-write",    action="store_true",
                        help="Do not write scores back to vector JSON files")
    parser.add_argument("--skip-judged", action="store_true",
                        help="Skip vectors that already have layer_c scores (for batching)")
    args = parser.parse_args()
    asyncio.run(main(args))
