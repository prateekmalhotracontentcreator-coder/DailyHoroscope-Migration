#!/usr/bin/env python3
"""
Phase 4 -- Layer A: Engine Accuracy (lagna + moon sign verification)
Runs vedic_calculator.py computation against all test vectors in a given book.
Populates chart_verification.lagna_computed, moon_sign_computed, engine_matches_book.

Usage:
  cd /Users/apple/DailyHoroscope-Migration
  python3 KE_TEXTBOOK_DECODE/phase4_layer_a.py --book 300h1
  python3 KE_TEXTBOOK_DECODE/phase4_layer_a.py --book 300h2
  python3 KE_TEXTBOOK_DECODE/phase4_layer_a.py --book longevity_unnatural
  python3 KE_TEXTBOOK_DECODE/phase4_layer_a.py --book longevity_astro_system
  python3 KE_TEXTBOOK_DECODE/phase4_layer_a.py --book 765_horoscopes
  python3 KE_TEXTBOOK_DECODE/phase4_layer_a.py --book all
"""

import sys, os, json, argparse, logging
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
import swisseph as swe
from vedic_calculator import (
    _parse_datetime_to_jd, _lon_to_sign, _calc_planet, _calc_ascendant, _setup_swe,
    geocode_place
)

BOOKS = {
    '300h1':                'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h1/',
    '300h2':                'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h2/',
    'longevity_unnatural':  'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_unnatural/',
    'longevity_astro_system': 'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_astro_system/',
    '765_horoscopes':       'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/765_horoscopes/',
}

# KP books use Krishnamurti ayanamsha; Vedic (765H) uses Lahiri
KP_BOOKS = {'300h1', '300h2', 'longevity_unnatural', 'longevity_astro_system'}

LOG_DIR = Path('KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)


_geocode_cache = {}

def tz_offset_to_str(offset_hours, lon_fallback=None) -> str:
    """Convert float offset (e.g. 5.5) to '+05:30'. If None, derive from longitude."""
    if offset_hours is None:
        # Derive from geographic longitude (solar time approximation)
        offset_hours = round((lon_fallback or 0) / 15.0 * 2) / 2  # round to nearest 0.5h
    sign = '+' if offset_hours >= 0 else '-'
    total_minutes = int(abs(offset_hours) * 60)
    h, m = divmod(total_minutes, 60)
    return f"{sign}{h:02d}:{m:02d}"


def compute_lagna_moon(bd: dict):
    """
    Returns (lagna_sign, moon_sign, error_msg).
    Falls back to geocoding if lat/lon missing.
    Derives timezone from longitude if tz_offset_hours is None.
    """
    date = bd.get('date')
    time_raw = bd.get('time_local') or (bd.get('time_utc') or '').split('T')[-1][:5]
    lat = bd.get('latitude')
    lon_geo = bd.get('longitude')
    tz_hours = bd.get('timezone_offset_hours')
    place = bd.get('place', '')

    if not date:
        return None, None, 'no_date'
    if not time_raw:
        return None, None, 'no_time'
    if bd.get('time_confidence') == 'unknown':
        return None, None, 'time_unknown'

    # Geocode fallback if coords missing
    if (lat is None or lon_geo is None) and place:
        if place in _geocode_cache:
            lat, lon_geo = _geocode_cache[place]
        else:
            try:
                lat, lon_geo = geocode_place(place)
                _geocode_cache[place] = (lat, lon_geo)
            except Exception as e:
                return None, None, f'geocode_fail:{str(e)[:60]}'

    if lat is None or lon_geo is None:
        return None, None, 'no_coords'

    # Normalise time to HH:MM
    time_str = str(time_raw)[:5]
    tz_str = tz_offset_to_str(tz_hours, lon_fallback=lon_geo)

    try:
        # Ayanamsha already set per book by set_ayanamsha() in run_book()
        jd = _parse_datetime_to_jd(date, time_str, tz_str)
        asc_lon = _calc_ascendant(jd, lat, lon_geo)
        lagna = _lon_to_sign(asc_lon)
        moon_lon, _ = _calc_planet(jd, swe.MOON)
        moon = _lon_to_sign(moon_lon)
        return lagna, moon, None
    except Exception as e:
        return None, None, str(e)[:120]


def normalise_sign(s):
    """Lowercase + strip for comparison."""
    return s.strip().lower() if s else None


def set_ayanamsha(book_key: str):
    """Set correct ayanamsha for each book."""
    if book_key in KP_BOOKS:
        swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    else:
        swe.set_sid_mode(swe.SIDM_LAHIRI)


def run_book(book_key: str, base_dir: str, log_lines: list) -> dict:
    folder = Path(base_dir) / book_key if not os.path.isabs(book_key) else Path(book_key)
    # Resolve relative to repo root
    repo_root = Path(__file__).parent.parent
    tv_dir = repo_root / BOOKS[book_key]
    files = sorted([f for f in tv_dir.iterdir() if f.name.startswith('tv_') and f.name.endswith('.json')])
    set_ayanamsha(book_key)
    ayanamsha_label = 'Krishnamurti' if book_key in KP_BOOKS else 'Lahiri'
    log_lines.append(f"  Ayanamsha: {ayanamsha_label}")

    stats = {'total': len(files), 'computed': 0, 'matched': 0,
             'mismatched': 0, 'skipped': 0, 'errors': 0}
    mismatches = []

    for fpath in files:
        with open(fpath) as f:
            try:
                vec = json.load(f)
            except json.JSONDecodeError as e:
                log_lines.append(f"  JSON_ERROR {fpath.name}: {e}")
                stats['errors'] += 1
                continue

        # Skip vectors excluded from Layer A test set
        if vec.get('excluded_from_layer_a'):
            stats['excluded'] = stats.get('excluded', 0) + 1
            continue

        bd = vec.get('birth_data', {})
        cv = vec.get('chart_verification', {})

        # Skip if time_confidence unknown and no time
        tc = bd.get('time_confidence', '')
        if tc == 'unknown' or not bd.get('time_local'):
            vec.setdefault('chart_verification', {})['skip_reason'] = 'no_time'
            stats['skipped'] += 1
            with open(fpath, 'w') as f:
                json.dump(vec, f, indent=2)
            continue

        lagna_computed, moon_computed, err = compute_lagna_moon(bd)

        if err:
            vec.setdefault('chart_verification', {})['computation_error'] = err
            stats['errors'] += 1
            log_lines.append(f"  COMPUTE_ERR {fpath.name}: {err}")
            with open(fpath, 'w') as f:
                json.dump(vec, f, indent=2)
            continue

        stats['computed'] += 1
        lagna_stated = cv.get('lagna_stated_in_book')
        moon_stated = cv.get('moon_sign_stated_in_book')

        lagna_match = normalise_sign(lagna_computed) == normalise_sign(lagna_stated) if lagna_stated else None
        moon_match = normalise_sign(moon_computed) == normalise_sign(moon_stated) if moon_stated else None
        engine_matches = lagna_match if lagna_stated else None

        vec.setdefault('chart_verification', {}).update({
            'lagna_computed':    lagna_computed,
            'moon_sign_computed': moon_computed,
            'engine_matches_book': engine_matches,
            'mismatch_notes': '' if engine_matches in (True, None) else
                f"Engine={lagna_computed} Book={lagna_stated}",
        })
        vec.setdefault('test_status', {})['chart_computed'] = True

        if engine_matches is True:
            stats['matched'] += 1
        elif engine_matches is False:
            stats['mismatched'] += 1
            # Classify severity: 1 sign off = border case; >2 signs = likely data error
            SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
                     'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
            try:
                diff = min(abs(SIGNS.index(lagna_computed) - SIGNS.index(lagna_stated)),
                           12 - abs(SIGNS.index(lagna_computed) - SIGNS.index(lagna_stated)))
                severity = 'border_case' if diff == 1 else 'probable_data_error'
            except (ValueError, TypeError):
                diff = -1
                severity = 'unknown'
            vec['chart_verification']['mismatch_severity'] = severity
            mismatches.append({
                'file': fpath.name,
                'vector_id': vec.get('vector_id'),
                'subject': vec.get('subject', {}).get('name', '?'),
                'stated': lagna_stated,
                'computed': lagna_computed,
                'diff_signs': diff,
                'severity': severity,
                'birth': f"{bd.get('date')} {bd.get('time_local')} tz={bd.get('timezone_offset_hours')} {bd.get('place', '')}",
            })

        with open(fpath, 'w') as f:
            json.dump(vec, f, indent=2)

    # Accuracy rate
    if stats['computed'] and (stats['matched'] + stats['mismatched']) > 0:
        tested = stats['matched'] + stats['mismatched']
        acc = round(stats['matched'] / tested * 100, 1)
        stats['accuracy_pct'] = acc
    else:
        stats['accuracy_pct'] = None

    stats['mismatches'] = mismatches
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--book', required=True, help='Book key or "all"')
    args = parser.parse_args()

    books_to_run = list(BOOKS.keys()) if args.book == 'all' else [args.book]
    if args.book != 'all' and args.book not in BOOKS:
        print(f"Unknown book: {args.book}. Options: {list(BOOKS.keys())}")
        sys.exit(1)

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_path = LOG_DIR / f"phase4_layer_a_{args.book}_{ts}.log"
    log_lines = [f"Phase 4A -- Layer A Engine Accuracy Run", f"Timestamp: {ts}", ""]

    overall = {}
    for book in books_to_run:
        log_lines.append(f"=== BOOK: {book} ===")
        stats = run_book(book, BOOKS[book], log_lines)
        overall[book] = stats

        log_lines.append(f"  Total TVs:   {stats['total']}")
        log_lines.append(f"  Excluded:    {stats.get('excluded', 0)}  (removed from test set)")
        log_lines.append(f"  In scope:    {stats['total'] - stats.get('excluded', 0)}")
        log_lines.append(f"  Computed:    {stats['computed']}")
        log_lines.append(f"  Matched:     {stats['matched']}")
        log_lines.append(f"  Mismatched:  {stats['mismatched']}")
        log_lines.append(f"  Skipped:     {stats['skipped']}  (no time)")
        log_lines.append(f"  Errors:      {stats['errors']}")
        acc = stats.get('accuracy_pct')
        log_lines.append(f"  Accuracy:    {acc}%  {'✅' if acc and acc >= 99 else '⚠️' if acc else '--'}")
        log_lines.append("")

        border = sum(1 for m in stats['mismatches'] if m.get('severity') == 'border_case')
        data_err = sum(1 for m in stats['mismatches'] if m.get('severity') == 'probable_data_error')
        if stats['mismatches']:
            log_lines.append(f"  Mismatch breakdown: {border} border_case (1 sign) · {data_err} probable_data_error (>1 sign)")
            log_lines.append("  MISMATCHES:")
            for m in stats['mismatches']:
                log_lines.append(f"    [{m.get('severity','?')}] {m['vector_id']} | {m['subject']} | stated={m['stated']} computed={m['computed']} diff={m.get('diff_signs')}sign(s)")
                log_lines.append(f"      birth: {m['birth']}")
            log_lines.append("")

    # Summary
    log_lines.append("=== SUMMARY ===")
    total_v = sum(s['total'] for s in overall.values())
    total_c = sum(s['computed'] for s in overall.values())
    total_m = sum(s['matched'] for s in overall.values())
    total_mm = sum(s['mismatched'] for s in overall.values())
    total_sk = sum(s['skipped'] for s in overall.values())
    tested = total_m + total_mm
    overall_acc = round(total_m / tested * 100, 1) if tested > 0 else None
    log_lines.append(f"  Total vectors:     {total_v}")
    log_lines.append(f"  Computed:          {total_c}")
    log_lines.append(f"  Lagna matched:     {total_m}/{tested}  ({overall_acc}%)")
    log_lines.append(f"  Skipped (no time): {total_sk}")
    log_lines.append(f"  Target ≥99%:       {'✅ PASS' if overall_acc and overall_acc >= 99 else '⚠️ NEEDS REVIEW'}")
    log_lines.append("")
    log_lines.append(f"Log written to: {log_path}")

    with open(log_path, 'w') as f:
        f.write('\n'.join(log_lines))

    # Print summary to stdout
    for line in log_lines[-15:]:
        print(line)
    print(f"\nFull log: {log_path}")


if __name__ == '__main__':
    main()
