#!/usr/bin/env python3
"""
Phase 4B -- Layer B: Rule Accuracy Evaluation (Jaccard Claim-Axis Scoring)
--------------------------------------------------------------------------
For every test vector that has valid birth data + author_observations,
this script:
  1. Computes the full Vedic chart from birth data
  2. Loads auto_approved + approved active rules from MongoDB
  3. Runs condition matching (extract_chart_facts + _condition_matches)
  4. Compares fired rule claim-axes against author observation claim-axes
  5. Scores each vector with Jaccard / Recall / Precision at claim-axis level
  6. Writes results into rule_evaluation block in each vector JSON
  7. Produces a summary Layer B report

Policy (per project):
  - Skip vectors with no birth time
  - Skip vectors with tz=None (timezone unknown -- don't guess)
  - Skip vectors with no author_observations, or all observations gap_flag=True
  - Far mismatches on Layer A (>1 sign off) → still run Layer B if chart computes
  - OCR/missing data → skip gracefully, no error halts the run

Scoring (claim-axis Jaccard):
  - fired_axes  = set of claim_axis values from rules whose condition matches the chart
  - expected_axes = set of claim_axis values from non-gap author_observations
  - Jaccard  = |fired ∩ expected| / |fired ∪ expected|
  - Recall   = |fired ∩ expected| / |expected|      (coverage of author axes)
  - Precision = |fired ∩ expected| / |fired|         (relevance of fired axes)
  - Layer B PASS per vector: Jaccard >= 0.85

Target: ≥85% of tested vectors pass Jaccard gate  (TV_STRATEGY Tier 3)

MONGO_URL environment variable required (Render env var).

Usage (from repo root):
  MONGO_URL="mongodb+srv://..." python3 KE_TEXTBOOK_DECODE/phase4_layer_b.py
  MONGO_URL="..." python3 KE_TEXTBOOK_DECODE/phase4_layer_b.py --book longevity_unnatural
  MONGO_URL="..." python3 KE_TEXTBOOK_DECODE/phase4_layer_b.py --book all
  MONGO_URL="..." python3 KE_TEXTBOOK_DECODE/phase4_layer_b.py --book all --dry-run  (no writes)
"""

from __future__ import annotations
import sys, os, json, asyncio, argparse
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / 'backend'))

import swisseph as swe
from motor.motor_asyncio import AsyncIOMotorClient
from vedic_calculator import (
    _parse_datetime_to_jd, _lon_to_sign, _calc_planet, _calc_ascendant,
    _setup_swe, get_house_number, get_nakshatra, geocode_place,
    calculate_vedic_chart, calculate_vimshottari_dasha, get_current_dasha,
    is_planet_combust, get_planet_dignity,
    DASHA_ORDER,
)
from knowledge_engine import extract_chart_facts, _condition_matches

# ── Config ───────────────────────────────────────────────────────────────────
BOOKS = {
    '300h1':                  'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h1/',
    '300h2':                  'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h2/',
    'longevity_unnatural':    'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_unnatural/',
    'longevity_astro_system': 'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_astro_system/',
}
KP_BOOKS = {'300h1', '300h2', 'longevity_unnatural', 'longevity_astro_system'}

DB_NAME            = 'horoscope_db'
RULES_COLLECTION   = 'interpretation_rules'
# Ruling 2026-06-09: include pending_human_review -- these are structurally valid
# textbook-decoded rules that have passed AI validation at ingest; PHR status means
# only TT review is pending, not that the rules are suspect.
# Excluded: flagged (~995), rejected (~112), deprecated (~745) -- those are correctly out.
# Full tested corpus: approved(326) + auto_approved(~5,892) + PHR(~4,016) ≈ 10,234 rules.
RULE_STATUSES      = ['approved', 'auto_approved', 'pending_human_review']
JACCARD_PASS_GATE  = 0.85

# Rule claim_axis values (ke_schema_constants.py) use granular names like career_growth,
# career_timing, career_trend.  Observation claim_axis values use coarse names like career.
# Normalize fired_axes down to the coarse observation vocabulary before Jaccard scoring.
AXIS_NORM = {
    'career_growth':        'career',
    'career_timing':        'career',
    'career_trend':         'career',
    'general':              'general',
    'general_trend':        'general',
    'wealth_trend':         'wealth',
    'financial_security':   'wealth',
    'marriage_timing':      'marriage',
    'relationship_quality': 'marriage',
    'relationships_trend':  'marriage',
    'partnership_stability':'marriage',
    'health_vitality':      'health',
    'health_trend':         'health',
    'longevity_trend':      'longevity',
    'spiritual_growth':     'spirituality',
    'spirituality_trend':   'spirituality',
    # pass-through (unchanged in observations)
    'longevity':            'longevity',
    'wealth':               'wealth',
    'marriage':             'marriage',
    'health':               'health',
    'spirituality':         'spirituality',
    'children':             'children',
    'education_trend':      'education',
    'enemies_adversaries':  'enemies',
    'past_lives':           'past_lives',
    'travel_pattern':       'travel',
    'learning_outcome':     'education',
}


def _norm_axis(ax: str) -> str:
    """Normalise a rule claim_axis to the coarse vocabulary used in observations."""
    return AXIS_NORM.get(ax, ax)

LOG_DIR = REPO_ROOT / 'KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

_geocode_cache: dict = {}

# ── Tee logging ───────────────────────────────────────────────────────────────
ts       = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')
log_path = LOG_DIR / f"phase4_layer_b_{ts}.log"

class Tee:
    def __init__(self, fp: Path):
        self._f = open(fp, 'w', encoding='utf-8')
    def write(self, d: str):
        sys.__stdout__.write(d); self._f.write(d)
    def flush(self):
        sys.__stdout__.flush(); self._f.flush()
    def close(self):
        self._f.close()

tee = Tee(log_path)
sys.stdout = tee
print(f"Log saved → {log_path}\n")

# ── Chart builder ─────────────────────────────────────────────────────────────

def tz_str_from_offset(offset_hours: float, lon_fallback: float = 0.0) -> str:
    """Convert numeric tz offset to ±HH:MM string."""
    sign = '+' if offset_hours >= 0 else '-'
    total_min = int(abs(offset_hours) * 60)
    h, m = divmod(total_min, 60)
    return f"{sign}{h:02d}:{m:02d}"


def build_chart(bd: dict) -> tuple[dict | None, str]:
    """
    Build a full Vedic chart dict from birth_data.
    Returns (chart_dict, error_msg) -- error_msg is empty string on success.
    Policy: skip tz=None, skip no time.
    """
    date   = bd.get('date')
    t      = str(bd.get('time_local') or '')[:5]
    lat    = bd.get('latitude')
    lon    = bd.get('longitude')
    tz_h   = bd.get('timezone_offset_hours')
    place  = bd.get('place', '')

    if not date or not t:
        return None, 'no_date_or_time'
    if tz_h is None:
        return None, 'tz_none'

    # Resolve coordinates
    if lat is None or lon is None:
        if place:
            if place in _geocode_cache:
                lat, lon = _geocode_cache[place]
            else:
                try:
                    lat, lon = geocode_place(place)
                    _geocode_cache[place] = (lat, lon)
                except Exception:
                    return None, f'geocode_fail:{place[:40]}'
    if lat is None or lon is None:
        return None, 'no_coords'

    tz_s = tz_str_from_offset(tz_h, lon)

    try:
        # We call calculate_vedic_chart but bypass geocoding by patching place string
        # to use pre-resolved coords. Simpler: build chart manually using core functions.
        jd = _parse_datetime_to_jd(date, t, tz_s)

        # Determine ayanamsha per book (KP vs Lahiri handled at caller level)
        asc_lon   = _calc_ascendant(jd, lat, lon)
        lagna_sign = _lon_to_sign(asc_lon)

        sun_lon, sun_speed = _calc_planet(jd, swe.SUN)

        PLANET_MAP = {
            'Sun':     swe.SUN,
            'Moon':    swe.MOON,
            'Mars':    swe.MARS,
            'Mercury': swe.MERCURY,
            'Jupiter': swe.JUPITER,
            'Venus':   swe.VENUS,
            'Saturn':  swe.SATURN,
            'Rahu':    swe.MEAN_NODE,   # True North Node
            'Ketu':    None,            # Ketu = Rahu + 180
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
                'sign':     p_sign,
                'degree':   deg,
                'house':    house,
                'nakshatra': nak_data.get('name'),
                'dignity':  dignity,
                'retrograde': retro,
                'combust':  combust,
                'longitude': round(p_lon, 4),
            }

        # Build houses dict
        houses: dict = {}
        lagna_idx = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
                     'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'].index(lagna_sign)
        sign_list = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
                     'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
        for h in range(1, 13):
            houses[h] = sign_list[(lagna_idx + h - 1) % 12]

        # Dasha
        moon_lon = planets['Moon']['longitude']
        dashas   = calculate_vimshottari_dasha(date, moon_lon)
        current_dasha = get_current_dasha(dashas)

        chart = {
            'lagna': {'sign': lagna_sign, 'degree': round(asc_lon % 30, 2)},
            'planets': planets,
            'houses':  houses,
            'moon_longitude': moon_lon,
            'current_dasha': current_dasha,
            'layers': {
                'vimshottari_dasha': {
                    'dasha_lord': current_dasha.get('planet', ''),
                },
            },
        }
        return chart, ''

    except Exception as e:
        return None, str(e)[:120]


# ── Scoring ───────────────────────────────────────────────────────────────────

def score_vector(
    chart: dict,
    rules: list[dict],
    observations: list[dict],
) -> dict:
    """
    Returns scoring dict:
      fired_axes, expected_axes, jaccard, recall, precision, layer_b_pass,
      rules_fired_count, rules_tested_count
    """
    # Expected axes from non-gap observations
    expected_axes = {
        obs['claim_axis']
        for obs in observations
        if not obs.get('gap_flag') and obs.get('claim_axis')
    }

    if not expected_axes:
        return {'skip_reason': 'no_scoreable_observations'}

    # Build ChartFacts
    try:
        facts = extract_chart_facts(chart)
    except Exception as e:
        return {'skip_reason': f'extract_facts_error:{str(e)[:60]}'}

    # Match rules
    # Ruling 2026-06-09: both claim_axis (primary) and secondary_axis contribute to fired_axes.
    # A rule firing on a secondary axis that matches an expected axis is a valid hit.
    fired_axes: set[str] = set()
    fired_count = 0
    for rule in rules:
        condition = rule.get('condition', {})
        if not condition:
            continue
        try:
            if _condition_matches(condition, facts):
                fired_count += 1
                # Primary axis
                raw_ax = rule.get('claim_axis') or (rule.get('categories') or [None])[0]
                if raw_ax:
                    fired_axes.add(_norm_axis(str(raw_ax)))
                # Secondary axis (explicit field -- not guesswork from categories)
                sec_ax = rule.get('secondary_axis')
                if sec_ax:
                    fired_axes.add(_norm_axis(str(sec_ax)))
        except Exception:
            continue  # skip malformed conditions

    # Jaccard at claim-axis level
    inter = fired_axes & expected_axes
    union = fired_axes | expected_axes

    jaccard   = round(len(inter) / len(union), 4) if union else 0.0
    recall    = round(len(inter) / len(expected_axes), 4) if expected_axes else 0.0
    precision = round(len(inter) / len(fired_axes), 4) if fired_axes else 0.0

    return {
        'fired_axes':         sorted(fired_axes),
        'expected_axes':      sorted(expected_axes),
        'intersection_axes':  sorted(inter),
        'jaccard':            jaccard,
        'recall':             recall,
        'precision':          precision,
        'layer_b_pass':       jaccard >= JACCARD_PASS_GATE,
        'rules_fired_count':  fired_count,
        'rules_tested_count': len(rules),
    }


# ── Main (async) ─────────────────────────────────────────────────────────────

async def run(book_filter: str, dry_run: bool) -> None:
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', '')
    if not mongo_url:
        print("❌ MONGO_URL environment variable not set.")
        print("   Set it and re-run:  MONGO_URL='mongodb+srv://...' python3 phase4_layer_b.py")
        return

    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[DB_NAME]

    # Load rules
    print(f"Loading rules (status: {RULE_STATUSES})...")
    cursor = db[RULES_COLLECTION].find(
        {'active': True, 'approval_status': {'$in': RULE_STATUSES}},
        {'_id': 0, 'rule_id': 1, 'condition': 1, 'claim_axis': 1, 'secondary_axis': 1,
         'categories': 1, 'approval_status': 1}
    )
    rules = await cursor.to_list(length=None)
    n_approved  = sum(1 for r in rules if r.get('approval_status') == 'approved')
    n_auto      = sum(1 for r in rules if r.get('approval_status') == 'auto_approved')
    n_phr       = sum(1 for r in rules if r.get('approval_status') == 'pending_human_review')
    print(f"Loaded {len(rules)} rules: {n_approved} approved + {n_auto} auto_approved + {n_phr} pending_human_review\n")

    # Which books to process
    if book_filter == 'all':
        books_to_run = list(BOOKS.items())
    elif book_filter in BOOKS:
        books_to_run = [(book_filter, BOOKS[book_filter])]
    else:
        print(f"Unknown book '{book_filter}'. Choose from: {list(BOOKS.keys())} or 'all'")
        return

    grand_tested = grand_pass = grand_skip = 0
    all_jaccards: list[float] = []
    all_recalls:  list[float] = []

    for book_name, folder in books_to_run:
        tv_dir = REPO_ROOT / folder
        files  = sorted(f for f in tv_dir.iterdir()
                        if f.name.startswith('tv_') and f.name.endswith('.json'))

        # Set ayanamsha per book
        if book_name in KP_BOOKS:
            swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
            aya_label = 'KP Krishnamurti'
        else:
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            aya_label = 'Lahiri'

        print(f"{'─'*60}")
        print(f"  Book: {book_name}  ({len(files)} vectors)  [{aya_label}]")
        print(f"{'─'*60}")

        book_tested = book_pass = book_skip = 0
        book_jaccards: list[float] = []

        for fpath in files:
            try:
                vec = json.load(open(fpath))
            except Exception:
                continue

            vid  = vec.get('vector_id', fpath.stem)
            bd   = vec.get('birth_data', {})
            obs  = vec.get('author_observations', [])

            # Skip if no observations at all
            if not obs:
                book_skip += 1
                continue

            # Build chart -- per policy: skip tz=None / no time
            chart, err = build_chart(bd)
            if err:
                book_skip += 1
                if err not in ('tz_none', 'no_date_or_time'):
                    print(f"  SKIP {vid}: {err}")
                continue

            # Score
            result = score_vector(chart, rules, obs)
            if 'skip_reason' in result:
                book_skip += 1
                continue

            book_tested += 1
            jac = result['jaccard']
            rec = result['recall']
            book_jaccards.append(jac)
            if result['layer_b_pass']:
                book_pass += 1
                mark = '✅'
            else:
                mark = '⚠️ '

            print(f"  {mark} {vid:30} J={jac:.2f} R={rec:.2f} P={result['precision']:.2f} "
                  f"fired={result['rules_fired_count']} "
                  f"axes: {result['intersection_axes']} / {result['expected_axes']}")

            # Write back
            if not dry_run:
                vec.setdefault('rule_evaluation', {}).update({
                    'evaluated':            True,
                    'evaluated_at':         ts,
                    'fired_axes':           result['fired_axes'],
                    'expected_axes':        result['expected_axes'],
                    'intersection_axes':    result['intersection_axes'],
                    'jaccard_score':        jac,
                    'recall_score':         rec,
                    'precision_score':      result['precision'],
                    'layer_b_pass':         result['layer_b_pass'],
                    'rules_fired_count':    result['rules_fired_count'],
                    'rules_tested_count':   result['rules_tested_count'],
                    'rule_statuses_used':   RULE_STATUSES,
                    'false_positive_flag':  (result['precision'] < 0.70
                                             and jac > 0),
                    'notes': ('' if result['layer_b_pass']
                              else f"Low Jaccard: fired={result['fired_axes']} expected={result['expected_axes']}"),
                })
                with open(fpath, 'w') as f:
                    json.dump(vec, f, indent=2)

        # Book summary
        pct_pass = round(book_pass / book_tested * 100, 1) if book_tested else 0.0
        mean_j   = round(sum(book_jaccards) / len(book_jaccards), 3) if book_jaccards else 0.0
        gate_ok  = '✅' if pct_pass >= 85 else '⚠️ '
        print(f"\n  {book_name}: tested={book_tested} pass={book_pass} ({pct_pass}% {gate_ok}) "
              f"skip={book_skip} mean_jaccard={mean_j}\n")

        grand_tested += book_tested
        grand_pass   += book_pass
        grand_skip   += book_skip
        all_jaccards += book_jaccards

    # Grand summary
    grand_pct  = round(grand_pass / grand_tested * 100, 1) if grand_tested else 0.0
    grand_mean = round(sum(all_jaccards) / len(all_jaccards), 3) if all_jaccards else 0.0
    gate_label = '✅ GATE PASSED' if grand_pct >= 85 else '⚠️  BELOW GATE'

    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("  PHASE 4B -- LAYER B RULE ACCURACY SUMMARY")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"  Rules loaded   : {len(rules)} (approved+auto_approved)")
    print(f"  Tested vectors : {grand_tested}")
    print(f"  Skipped        : {grand_skip}  (no time / tz=None / no obs)")
    print(f"  ✅ Pass (J≥{JACCARD_PASS_GATE}) : {grand_pass}")
    print(f"  ⚠️  Fail        : {grand_tested - grand_pass}")
    print(f"  Pass rate      : {grand_pct}%  {gate_label}")
    print(f"  Mean Jaccard   : {grand_mean}")
    print(f"  Target         : ≥85% pass + mean J≥0.85  (TV_STRATEGY Tier 3)")
    print(f"  Dry-run        : {dry_run}")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"\nLog saved → {log_path}")

    client.close()
    sys.stdout = sys.__stdout__
    tee.close()
    print(f"Log saved → {log_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--book',    default='all',
                        help='Book to process: 300h1 | 300h2 | longevity_unnatural | longevity_astro_system | all')
    parser.add_argument('--dry-run', action='store_true',
                        help='Compute and report but do not write back to vector JSONs')
    args = parser.parse_args()
    asyncio.run(run(args.book, args.dry_run))


if __name__ == '__main__':
    main()
