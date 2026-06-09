#!/usr/bin/env python3
"""
Phase 4A -- Layer A Dasha Balance Precision Test (T2 -- 765 Notable Horoscopes)
Computes Vimshottari dasha balance at birth using vedic_calculator.py and
compares against dasha_balance_from_book. Target: ±1 day precision.

Usage:
  cd /Users/apple/DailyHoroscope-Migration
  python3 KE_TEXTBOOK_DECODE/phase4_layer_a_dasha_balance.py
"""

import sys, os, json
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
import swisseph as swe
from vedic_calculator import (
    _parse_datetime_to_jd, _calc_planet, calculate_vimshottari_dasha, _setup_swe
)

TV_DIR   = Path('KE_TEXTBOOK_DECODE/Test_Vectors/JSON/765_horoscopes/')
LOG_DIR  = Path('KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs/')
LOG_DIR.mkdir(parents=True, exist_ok=True)

TOLERANCE_DAYS = 1   # ±1 day pass threshold


def tz_to_str(offset_hours) -> str:
    if offset_hours is None:
        return '+05:30'          # 765H is majority Indian -- safe default
    sign = '+' if offset_hours >= 0 else '-'
    h, m = divmod(int(abs(offset_hours) * 60), 60)
    return f"{sign}{h:02d}:{m:02d}"


def balance_to_days(years, months, days) -> float:
    return years * 365.25 + months * 30.4375 + days


def compute_dasha_balance(bd: dict):
    """
    Returns (planet, balance_days_engine, error_msg).
    """
    date     = bd.get('date')
    time_raw = bd.get('time_local') or ''
    tz_hours = bd.get('timezone_offset_hours')

    if not date:
        return None, None, 'no_date'
    if not time_raw or bd.get('time_confidence') == 'unknown':
        return None, None, 'no_time'

    time_str = str(time_raw)[:5]
    tz_str   = tz_to_str(tz_hours)

    try:
        jd = _parse_datetime_to_jd(date, time_str, tz_str)
        moon_lon, _ = _calc_planet(jd, swe.MOON)
        dashas = calculate_vimshottari_dasha(date, moon_lon)
        first  = dashas[0]
        engine_days = first['years'] * 365.25
        return first['planet'].upper(), engine_days, None
    except Exception as e:
        return None, None, str(e)[:120]


def main():
    _setup_swe()   # Lahiri for 765H (Vedic book)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    repo_root = Path(__file__).parent.parent
    tv_dir    = repo_root / TV_DIR
    files     = sorted([f for f in tv_dir.iterdir()
                        if f.name.startswith('tv_') and f.name.endswith('.json')])

    ts       = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_path = repo_root / LOG_DIR / f"phase4_dasha_balance_765h_{ts}.log"
    log      = [f"Phase 4A -- Dasha Balance Precision Test (765H)", f"Timestamp: {ts}",
                f"Tolerance: ±{TOLERANCE_DAYS} day(s)", ""]

    stats = {'total': len(files), 'computed': 0, 'pass': 0,
             'fail': 0, 'skipped': 0, 'errors': 0, 'planet_mismatch': 0}
    fails = []

    for fpath in files:
        with open(fpath) as f:
            try:
                vec = json.load(f)
            except json.JSONDecodeError:
                stats['errors'] += 1
                continue

        if vec.get('excluded_from_layer_a'):
            stats['skipped'] += 1
            continue

        db_book = vec.get('dasha_balance_from_book') or {}
        if not db_book.get('planet'):
            stats['skipped'] += 1
            continue

        bd = vec.get('birth_data') or {}
        planet_engine, balance_days_engine, err = compute_dasha_balance(bd)

        if err:
            vec.setdefault('dasha_balance_verification', {})['error'] = err
            stats['errors'] += 1
            with open(fpath, 'w') as f: json.dump(vec, f, indent=2)
            continue

        stats['computed'] += 1

        # Book balance → days
        book_days = balance_to_days(
            db_book.get('years', 0),
            db_book.get('months', 0),
            db_book.get('days', 0)
        )
        book_planet = (db_book.get('planet') or '').upper()

        diff_days   = abs(balance_days_engine - book_days)
        planet_ok   = planet_engine == book_planet
        balance_ok  = diff_days <= TOLERANCE_DAYS
        passed      = planet_ok and balance_ok

        result = {
            'planet_book':    book_planet,
            'planet_engine':  planet_engine,
            'balance_days_book':   round(book_days, 2),
            'balance_days_engine': round(balance_days_engine, 2),
            'diff_days':      round(diff_days, 2),
            'planet_match':   planet_ok,
            'balance_pass':   balance_ok,
            'layer_a_pass':   passed,
        }
        vec['dasha_balance_verification'] = result
        vec.setdefault('test_status', {})['dasha_balance_computed'] = True

        if passed:
            stats['pass'] += 1
        elif not planet_ok:
            stats['planet_mismatch'] += 1
            fails.append({'file': fpath.name, 'vid': vec.get('vector_id'),
                          'subject': (vec.get('subject') or {}).get('name', '?'),
                          'reason': f"planet_mismatch book={book_planet} engine={planet_engine}",
                          'diff': diff_days})
        else:
            stats['fail'] += 1
            fails.append({'file': fpath.name, 'vid': vec.get('vector_id'),
                          'subject': (vec.get('subject') or {}).get('name', '?'),
                          'reason': f"balance_off by {diff_days:.1f} days  book={book_days:.1f} engine={balance_days_engine:.1f}",
                          'diff': diff_days})

        with open(fpath, 'w') as f: json.dump(vec, f, indent=2)

    # Accuracy
    tested = stats['pass'] + stats['fail'] + stats['planet_mismatch']
    acc    = round(stats['pass'] / tested * 100, 1) if tested > 0 else None

    log.append(f"  Total TVs:        {stats['total']}")
    log.append(f"  Computed:         {stats['computed']}")
    log.append(f"  Skipped:          {stats['skipped']}  (no dasha_balance or excluded)")
    log.append(f"  Errors:           {stats['errors']}")
    log.append(f"  PASS (±1 day):    {stats['pass']}")
    log.append(f"  FAIL (balance):   {stats['fail']}")
    log.append(f"  Planet mismatch:  {stats['planet_mismatch']}")
    log.append(f"  Accuracy:         {acc}%  {'✅' if acc and acc >= 90 else '⚠️'}")
    log.append(f"  Target ≥90%:      {'✅ PASS' if acc and acc >= 90 else '⚠️ NEEDS REVIEW'}")
    log.append("")

    if fails:
        log.append(f"  FAILS (top 30):")
        for item in sorted(fails, key=lambda x: -x['diff'])[:30]:
            log.append(f"    {item['vid']} | {item['subject']} | {item['reason']}")
    log.append("")
    log.append(f"Log: {log_path}")

    with open(log_path, 'w') as f:
        f.write('\n'.join(log))

    for line in log:
        print(line)


if __name__ == '__main__':
    main()
