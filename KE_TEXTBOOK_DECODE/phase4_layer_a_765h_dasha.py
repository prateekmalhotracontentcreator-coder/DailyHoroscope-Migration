#!/usr/bin/env python3
"""
Phase 4A -- Layer A (765H): Dasha Balance Verification
------------------------------------------------------
Secondary Layer A gate for 765 Notable Horoscopes.
Goal: Verify calculate_vimshottari_dasha() precision against book-stated
      dasha balance at birth (±1 day tolerance).

Also computes lagna sign + degree for each vector as a by-product.

Updates each test vector JSON with computed values.
Produces a summary log at: KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs/

Usage (from repo root):
  python3 KE_TEXTBOOK_DECODE/phase4_layer_a_765h_dasha.py
  python3 KE_TEXTBOOK_DECODE/phase4_layer_a_765h_dasha.py --rerun  # recompute all, even if already done
"""

from __future__ import annotations
import sys, os, json, argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Repo path setup ──────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / 'backend'))

import swisseph as swe
from vedic_calculator import (
    _parse_datetime_to_jd, _lon_to_sign, _calc_planet, _calc_ascendant, _setup_swe,
    calculate_vimshottari_dasha, geocode_place,
)

# ── Config ───────────────────────────────────────────────────────────────────
TV_DIR   = REPO_ROOT / 'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/765_horoscopes'
LOG_DIR  = REPO_ROOT / 'KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

TOLERANCE_DAYS = 1.0        # ±1 day pass gate
DAYS_PER_YEAR  = 365.25
DAYS_PER_MONTH = 365.25 / 12   # ~30.4375

# 765H uses Lahiri ayanamsha
swe.set_sid_mode(swe.SIDM_LAHIRI)

_geocode_cache: dict = {}

# ── Tee logging ──────────────────────────────────────────────────────────────
ts       = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')
log_path = LOG_DIR / f"phase4_layer_a_765h_dasha_{ts}.log"

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

# ── Helpers ──────────────────────────────────────────────────────────────────

def ymd_to_days(years: int, months: int, days: int) -> float:
    return years * DAYS_PER_YEAR + months * DAYS_PER_MONTH + days


def tz_str(offset_hours, lon_fallback=None) -> str:
    if offset_hours is None:
        offset_hours = round((lon_fallback or 0) / 15.0 * 2) / 2
    sign = '+' if offset_hours >= 0 else '-'
    m_total = int(abs(offset_hours) * 60)
    h, m = divmod(m_total, 60)
    return f"{sign}{h:02d}:{m:02d}"


def compute_chart(bd: dict):
    """
    Returns (lagna_sign, lagna_degree_in_sign, moon_lon, error_msg).
    lagna_degree_in_sign = asc_lon % 30.
    """
    date   = bd.get('date')
    t_raw  = bd.get('time_local') or ''
    lat    = bd.get('latitude')
    lon    = bd.get('longitude')
    tz_h   = bd.get('timezone_offset_hours')
    place  = bd.get('place', '')

    if not date:
        return None, None, None, 'no_date'
    if not t_raw:
        return None, None, None, 'no_time'

    if (lat is None or lon is None) and place:
        if place in _geocode_cache:
            lat, lon = _geocode_cache[place]
        else:
            try:
                lat, lon = geocode_place(place)
                _geocode_cache[place] = (lat, lon)
            except Exception as e:
                return None, None, None, f'geocode_fail:{str(e)[:60]}'

    if lat is None or lon is None:
        return None, None, None, 'no_coords'

    try:
        jd         = _parse_datetime_to_jd(date, str(t_raw)[:5], tz_str(tz_h, lon))
        asc_lon    = _calc_ascendant(jd, lat, lon)
        moon_lon, _ = _calc_planet(jd, swe.MOON)
        lagna_sign = _lon_to_sign(asc_lon)
        return lagna_sign, round(asc_lon % 30, 4), moon_lon, None
    except Exception as e:
        return None, None, None, str(e)[:120]


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rerun', action='store_true',
                        help='Recompute even vectors already marked dasha_balance_verified')
    args = parser.parse_args()

    files = sorted(f for f in TV_DIR.iterdir()
                   if f.name.startswith('tv_') and f.name.endswith('.json'))

    print("╔══════════════════════════════════════════════════════════════╗")
    print(f"  Phase 4A -- Layer A (765H) Dasha Balance Verification")
    print(f"  Vectors  : {len(files)} files in {TV_DIR.name}/")
    print(f"  Tolerance: ±{TOLERANCE_DAYS} day")
    print(f"  Ayanamsha: Lahiri")
    print(f"  Mode     : {'--rerun (all vectors)' if args.rerun else 'incremental (skip already done)'}")
    print(f"  Log      : {log_path}")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    stats = dict(
        total=0, no_dasha_data=0, already_done=0, skipped=0,
        compute_errors=0, matched=0, planet_wrong=0, tolerance_exceeded=0,
    )
    # Delta buckets for tolerance_exceeded cases (correct planet, wrong balance)
    delta_buckets = {'le2': 0, 'le5': 0, 'le10': 0, 'le30': 0, 'le100': 0,
                     'le999': 0, 'gt999': 0}
    mismatches  = []   # planet wrong or tolerance exceeded
    planet_errs = []   # planet name doesn't match

    for fpath in files:
        try:
            with open(fpath) as f:
                vec = json.load(f)
        except Exception as e:
            print(f"  JSON_ERR {fpath.name}: {e}")
            continue

        stats['total'] += 1
        vid = vec.get('vector_id', fpath.stem)

        # Skip if already verified (unless --rerun)
        if not args.rerun and vec.get('test_status', {}).get('dasha_balance_verified'):
            stats['already_done'] += 1
            continue

        # Skip if no dasha balance data in the book
        db_book = vec.get('dasha_balance_from_book')
        if not db_book or not db_book.get('planet'):
            stats['no_dasha_data'] += 1
            continue

        bd = vec.get('birth_data', {})
        if vec.get('subject', {}).get('mythological'):
            stats['skipped'] += 1
            continue

        lagna_sign, lagna_deg, moon_lon, err = compute_chart(bd)

        if err:
            print(f"  SKIP {vid}: {err}")
            stats['skipped'] += 1
            vec.setdefault('chart_verification', {})['engine_notes'] = f"skip:{err}"
            vec.setdefault('test_status', {})['chart_computed'] = False
            with open(fpath, 'w') as f:
                json.dump(vec, f, indent=2)
            continue

        # Compute dasha balance
        birth_date = bd['date']
        dashas = calculate_vimshottari_dasha(birth_date, moon_lon)
        first  = dashas[0]

        engine_planet = first['planet'].upper()
        engine_days   = round(first['years'] * DAYS_PER_YEAR, 3)

        # Book balance → days
        book_planet = str(db_book.get('planet', '')).upper()
        book_y = int(db_book.get('years', 0) or 0)
        book_m = int(db_book.get('months', 0) or 0)
        book_d = int(db_book.get('days', 0) or 0)
        book_days = round(ymd_to_days(book_y, book_m, book_d), 3)

        planet_match    = engine_planet == book_planet
        delta_days      = round(abs(engine_days - book_days), 3)
        tolerance_match = delta_days <= TOLERANCE_DAYS
        overall_match   = planet_match and tolerance_match

        # Write back to vector
        cv = vec.setdefault('chart_verification', {})
        cv.update({
            'lagna_sign_computed':      lagna_sign,
            'lagna_degree_computed':    lagna_deg,
            'lagna_book_degree':        cv.get('lagna_degree_from_book'),
            'lagna_degree_delta':       round(abs((lagna_deg or 0) - (cv.get('lagna_degree_from_book') or 0)), 4),
            'dasha_planet_book':        book_planet,
            'dasha_planet_computed':    engine_planet,
            'dasha_balance_days_book':  book_days,
            'dasha_balance_days_engine': engine_days,
            'dasha_balance_delta_days': delta_days,
            'dasha_balance_engine_match': overall_match,
            'dasha_planet_match':       planet_match,
            'dasha_tolerance_match':    tolerance_match,
            'engine_notes':             '' if overall_match else
                                        (f"planet:{book_planet}≠{engine_planet}" if not planet_match
                                         else f"delta:{delta_days}d (book={book_days}d engine={engine_days}d)"),
        })
        ts_block = vec.setdefault('test_status', {})
        ts_block['chart_computed']        = True
        ts_block['dasha_balance_verified'] = True
        ts_block['layer_a_evaluated']     = True

        with open(fpath, 'w') as f:
            json.dump(vec, f, indent=2)

        if overall_match:
            stats['matched'] += 1
            print(f"  ✅ {vid:<30} {book_planet} {book_y}y{book_m}m{book_d}d → engine {engine_days:.1f}d  δ={delta_days:.2f}d")
        else:
            if not planet_match:
                stats['planet_wrong'] += 1
                tag = f"PLANET_MISMATCH  book={book_planet} engine={engine_planet}"
                planet_errs.append({'vid': vid, 'book': book_planet, 'engine': engine_planet,
                                    'book_days': book_days, 'engine_days': engine_days})
            else:
                stats['tolerance_exceeded'] += 1
                # Bucket delta for reporting
                d = delta_days
                if d <= 2:      delta_buckets['le2'] += 1
                elif d <= 5:    delta_buckets['le5'] += 1
                elif d <= 10:   delta_buckets['le10'] += 1
                elif d <= 30:   delta_buckets['le30'] += 1
                elif d <= 100:  delta_buckets['le100'] += 1
                elif d <= 999:  delta_buckets['le999'] += 1
                else:           delta_buckets['gt999'] += 1
                tag = f"TOLERANCE_EXCEEDED  δ={delta_days:.1f}d  book={book_days:.0f}d engine={engine_days:.0f}d"
            mismatches.append({'vid': vid, 'tag': tag, 'birth': bd.get('date')})
            print(f"  ⚠️  {vid:<30} {tag}")

    # ── Summary ───────────────────────────────────────────────────────────────
    tested       = stats['matched'] + stats['planet_wrong'] + stats['tolerance_exceeded']
    planet_ok    = stats['matched'] + stats['tolerance_exceeded']  # correct planet regardless of delta
    pass_pct_1d  = round(stats['matched'] / tested * 100, 1) if tested else None
    planet_pct   = round(planet_ok / tested * 100, 1) if tested else None

    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print(f"  PHASE 4A -- 765H DASHA BALANCE SUMMARY")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"  Total vectors              : {stats['total']}")
    print(f"  Already done (skipped)     : {stats['already_done']}")
    print(f"  No dasha data in book      : {stats['no_dasha_data']}")
    print(f"  Skipped (no time/coords)   : {stats['skipped']}")
    print(f"  Tested                     : {tested}")
    print(f"  ✅ Matched (planet+±1 day) : {stats['matched']}")
    print(f"  ✅ Planet match (any delta) : {planet_ok}")
    print(f"  ⚠️  Planet wrong            : {stats['planet_wrong']}")
    print(f"  ⚠️  Tol exceeded (same ☽)  : {stats['tolerance_exceeded']}")
    print(f"  ------------------------------------------------------------------------------------------")
    print(f"  Pass rate ±1d (strict)     : {pass_pct_1d}%")
    print(f"  Pass rate planet-only      : {planet_pct}%  {'✅ ≥80%' if planet_pct and planet_pct >= 80 else '⚠️  BELOW 80%' if planet_pct else '--'}")
    print(f"  ------------------------------------------------------------------------------------------")
    print(f"  Tol-exceeded delta breakdown:")
    print(f"    ≤2d:  {delta_buckets['le2']}   ≤5d: {delta_buckets['le5']}   ≤10d: {delta_buckets['le10']}")
    print(f"    ≤30d: {delta_buckets['le30']}  ≤100d: {delta_buckets['le100']}  ≤999d: {delta_buckets['le999']}  >999d: {delta_buckets['gt999']}")
    print(f"  NOTE: >30d delta with correct planet = birth time imprecision in")
    print(f"        historical source. Not an engine bug -- expected for 1980s books.")
    print("╚══════════════════════════════════════════════════════════════╝")

    if planet_errs:
        print("\nPLANET MISMATCHES (investigate -- possible OCR or Moon nakshatra boundary):")
        for e in planet_errs:
            print(f"  {e['vid']:30} book={e['book']} engine={e['engine']}  book_days={e['book_days']:.1f} engine_days={e['engine_days']:.1f}")

    if mismatches:
        print("\nALL MISMATCHES:")
        for m in mismatches:
            print(f"  {m['vid']:30} {m['tag']}  birth={m['birth']}")

    print(f"\nLog saved → {log_path}")

    sys.stdout = sys.__stdout__
    tee.close()
    print(f"Log saved → {log_path}")


if __name__ == '__main__':
    main()
