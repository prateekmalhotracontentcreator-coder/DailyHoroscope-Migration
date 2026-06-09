#!/usr/bin/env python3
"""
Phase 4A -- 765H Dasha Balance: Lahiri vs KP Krishnamurti Ayanamsha Comparison
-------------------------------------------------------------------------------
Read-only (no JSON writes). Runs the same dasha balance computation twice --
once with Lahiri, once with KP Krishnamurti -- and produces a side-by-side
comparison report.

Usage (from repo root):
  python3 KE_TEXTBOOK_DECODE/phase4_layer_a_765h_dasha_compare.py

Output:
  KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs/phase4_aya_compare_{ts}.log
"""

from __future__ import annotations
import sys, json, argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / 'backend'))

import swisseph as swe
from vedic_calculator import (
    _parse_datetime_to_jd, _lon_to_sign, _calc_planet,
    calculate_vimshottari_dasha, geocode_place, get_nakshatra,
)

# ── Config ───────────────────────────────────────────────────────────────────
TV_DIR   = REPO_ROOT / 'KE_TEXTBOOK_DECODE/Test_Vectors/JSON/765_horoscopes'
LOG_DIR  = REPO_ROOT / 'KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

TOLERANCE_DAYS = 1.0
DAYS_PER_YEAR  = 365.25
DAYS_PER_MONTH = 365.25 / 12

SYSTEMS = {
    'lahiri': swe.SIDM_LAHIRI,
    'kp':     swe.SIDM_KRISHNAMURTI,
}

_gc: dict = {}

# ── Tee logging ───────────────────────────────────────────────────────────────
ts       = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')
log_path = LOG_DIR / f"phase4_aya_compare_{ts}.log"

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

# ── Helpers ───────────────────────────────────────────────────────────────────

def ymd_to_days(y: int, m: int, d: int) -> float:
    return y * DAYS_PER_YEAR + m * DAYS_PER_MONTH + d

def tz_str(offset_hours, lon_fallback=None) -> str:
    if offset_hours is None:
        offset_hours = round((lon_fallback or 0) / 15.0 * 2) / 2
    sign = '+' if offset_hours >= 0 else '-'
    mt = int(abs(offset_hours) * 60)
    h, m = divmod(mt, 60)
    return f"{sign}{h:02d}:{m:02d}"

def compute_moon(jd: float, swe_mode: int) -> float:
    """Return sidereal Moon longitude under the given ayanamsha."""
    swe.set_sid_mode(swe_mode)
    lon, _ = _calc_planet(jd, swe.MOON)
    return lon

def evaluate(vec: dict, swe_mode: int):
    """
    Returns dict:
      planet_book, planet_engine, planet_match,
      book_days, engine_days, delta_days, tolerance_match, overall_match,
      moon_lon, nakshatra, error
    """
    bd   = vec.get('birth_data', {})
    db   = vec.get('dasha_balance_from_book', {})
    date = bd.get('date')
    t    = str(bd.get('time_local') or '')
    lat  = bd.get('latitude')
    lon  = bd.get('longitude')
    tz_h = bd.get('timezone_offset_hours')

    if not date or not t:
        return {'error': 'no_date_or_time'}

    if lat is None or lon is None:
        place = bd.get('place', '')
        if place in _gc:
            lat, lon = _gc[place]
        elif place:
            try:
                lat, lon = geocode_place(place); _gc[place] = (lat, lon)
            except Exception as e:
                return {'error': f'geocode:{str(e)[:50]}'}
    if lat is None or lon is None:
        return {'error': 'no_coords'}

    try:
        jd       = _parse_datetime_to_jd(date, t[:5], tz_str(tz_h, lon))
        moon_lon = compute_moon(jd, swe_mode)
        nak      = get_nakshatra(moon_lon)
        dashas   = calculate_vimshottari_dasha(date, moon_lon)
        first    = dashas[0]

        ep = first['planet'].upper()
        ed = round(first['years'] * DAYS_PER_YEAR, 3)
        bp = str(db.get('planet', '')).upper()
        bd_days = round(ymd_to_days(
            int(db.get('years', 0) or 0),
            int(db.get('months', 0) or 0),
            int(db.get('days', 0) or 0),
        ), 3)
        delta = round(abs(ed - bd_days), 3)
        pm  = ep == bp
        tm  = delta <= TOLERANCE_DAYS

        return {
            'error': None,
            'planet_book':      bp,
            'planet_engine':    ep,
            'planet_match':     pm,
            'book_days':        bd_days,
            'engine_days':      ed,
            'delta_days':       delta,
            'tolerance_match':  tm,
            'overall_match':    pm and tm,
            'moon_lon':         round(moon_lon, 4),
            'nakshatra':        nak.get('name', ''),
        }
    except Exception as e:
        return {'error': str(e)[:100]}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    files = sorted(f for f in TV_DIR.iterdir()
                   if f.name.startswith('tv_') and f.name.endswith('.json'))

    print("╔══════════════════════════════════════════════════════════════════╗")
    print("  Phase 4A -- 765H Dasha: Lahiri vs KP Krishnamurti Comparison")
    print(f"  Vectors  : {len(files)} | Tolerance: ±{TOLERANCE_DAYS}d | Read-only (no writes)")
    print(f"  Log      : {log_path}")
    print("╚══════════════════════════════════════════════════════════════════╝\n")

    # Per-system counters
    stats = {s: dict(tested=0, matched=0, planet_ok=0, planet_wrong=0,
                     tol_exceeded=0, skipped=0, errors=0)
             for s in SYSTEMS}

    # Per-vector outcome tracking (for cross-system analysis)
    agree_match   = 0   # both match
    agree_miss    = 0   # both miss
    lahiri_only   = 0   # Lahiri matches, KP doesn't
    kp_only       = 0   # KP matches, Lahiri doesn't

    # Planet match tracking
    planet_agree  = 0   # both get the same planet (whether correct or not)
    planet_lah_ok_kp_wrong = 0  # Lahiri correct planet, KP wrong
    planet_kp_ok_lah_wrong = 0  # KP correct planet, Lahiri wrong
    planet_both_wrong = 0

    # Vectors where the two systems disagree on the planet
    planet_flip_cases = []   # KP flips planet vs Lahiri, one of them is correct
    kp_rescues = []          # KP gets correct planet where Lahiri fails
    lah_rescues = []         # Lahiri gets correct planet where KP fails

    # Delta comparison for planet-correct cases
    kp_closer  = 0   # KP delta < Lahiri delta (when both planet correct)
    lah_closer = 0
    equal_delta = 0

    tested_count = 0

    for fpath in files:
        try:
            vec = json.load(open(fpath))
        except Exception:
            continue

        if vec.get('subject', {}).get('mythological'):
            continue
        db = vec.get('dasha_balance_from_book', {})
        if not db or not db.get('planet'):
            continue

        results = {}
        for sys_name, swe_mode in SYSTEMS.items():
            r = evaluate(vec, swe_mode)
            results[sys_name] = r
            s = stats[sys_name]
            if r.get('error'):
                s['errors'] += 1
                continue
            s['tested'] += 1
            if r['overall_match']:      s['matched'] += 1
            if r['planet_match']:       s['planet_ok'] += 1
            else:                       s['planet_wrong'] += 1
            if r['planet_match'] and not r['tolerance_match']:
                                        s['tol_exceeded'] += 1

        r_l = results.get('lahiri', {})
        r_k = results.get('kp', {})

        if r_l.get('error') or r_k.get('error'):
            continue

        tested_count += 1
        vid = vec.get('vector_id', fpath.stem)

        # Agreement on strict match
        if r_l['overall_match'] and r_k['overall_match']:
            agree_match += 1
        elif not r_l['overall_match'] and not r_k['overall_match']:
            agree_miss += 1
        elif r_l['overall_match']:
            lahiri_only += 1
        else:
            kp_only += 1

        # Agreement on planet
        l_pm = r_l['planet_match']
        k_pm = r_k['planet_match']
        l_ep = r_l['planet_engine']
        k_ep = r_k['planet_engine']
        bp   = r_l['planet_book']

        if l_pm and k_pm:
            planet_agree += 1
        elif l_pm and not k_pm:
            planet_lah_ok_kp_wrong += 1
            lah_rescues.append({'vid': vid, 'book': bp, 'lahiri': l_ep, 'kp': k_ep,
                                'l_moon': r_l['moon_lon'], 'k_moon': r_k['moon_lon']})
        elif k_pm and not l_pm:
            planet_kp_ok_lah_wrong += 1
            kp_rescues.append({'vid': vid, 'book': bp, 'lahiri': l_ep, 'kp': k_ep,
                               'l_moon': r_l['moon_lon'], 'k_moon': r_k['moon_lon']})
        else:
            planet_both_wrong += 1
            # Only track if they disagree on the wrong planet too (interesting)
            if l_ep != k_ep:
                planet_flip_cases.append({'vid': vid, 'book': bp,
                                          'lahiri': l_ep, 'kp': k_ep})

        # Delta comparison when both planets are correct
        if l_pm and k_pm:
            l_d = r_l['delta_days']; k_d = r_k['delta_days']
            if abs(l_d - k_d) < 0.01:  equal_delta += 1
            elif k_d < l_d:             kp_closer += 1
            else:                       lah_closer += 1

    # ── Ayanamsha difference at a sample date ────────────────────────────────
    jd_sample = swe.julday(1970, 6, 15, 12.0)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    aya_lah = swe.get_ayanamsa_ut(jd_sample)
    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    aya_kp  = swe.get_ayanamsa_ut(jd_sample)
    aya_diff = round(aya_lah - aya_kp, 4)   # typically negative (KP > Lahiri)

    # ── Print Summary ─────────────────────────────────────────────────────────
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("  SYSTEM COMPARISON -- PER-SYSTEM SCORES")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print(f"  {'Metric':<35} {'LAHIRI':>10} {'KP':>10}")
    print(f"  {'--'*55}")
    for label, key in [
        ('Vectors tested', 'tested'),
        ('✅ Strict match (planet+±1d)', 'matched'),
        ('✅ Planet match (any delta)', 'planet_ok'),
        ('⚠️  Planet wrong', 'planet_wrong'),
        ('⚠️  Tol exceeded (planet OK)', 'tol_exceeded'),
        ('Errors/skipped', 'errors'),
    ]:
        lv = stats['lahiri'][key]
        kv = stats['kp'][key]
        t  = stats['lahiri']['tested'] or 1
        if key in ('matched', 'planet_ok', 'planet_wrong'):
            print(f"  {label:<35} {lv:>5} ({round(lv/t*100,1)}%)  {kv:>5} ({round(kv/t*100,1)}%)")
        else:
            print(f"  {label:<35} {lv:>10} {kv:>10}")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print("  CROSS-SYSTEM AGREEMENT")
    print(f"  {'--'*55}")
    print(f"  Ayanamsha diff (1970-06-15): Lahiri={round(aya_lah,4)}° KP={round(aya_kp,4)}°  Δ={aya_diff}°")
    print(f"  (KP Moon is {abs(aya_diff):.4f}° {'higher' if aya_diff < 0 else 'lower'} than Lahiri Moon)")
    print(f"  {'--'*55}")
    print(f"  Both strict-match (agree ✅)  : {agree_match}")
    print(f"  Both miss (agree ❌)           : {agree_miss}")
    print(f"  Lahiri only strict-match       : {lahiri_only}")
    print(f"  KP only strict-match           : {kp_only}")
    print(f"  {'--'*55}")
    print(f"  Both planet correct            : {planet_agree}")
    print(f"  KP rescues Lahiri planet miss  : {planet_kp_ok_lah_wrong}  ← KP fixes these")
    print(f"  Lahiri rescues KP planet miss  : {planet_lah_ok_kp_wrong}  ← Lahiri fixes these")
    print(f"  Both planet wrong              : {planet_both_wrong}")
    print(f"  {'--'*55}")
    print(f"  Balance delta (planet-correct): KP closer {kp_closer} · Lahiri closer {lah_closer} · Equal {equal_delta}")
    print("╚══════════════════════════════════════════════════════════════════╝")

    if kp_rescues:
        print(f"\nKP RESCUES ({len(kp_rescues)}) -- KP correct planet where Lahiri fails:")
        for r in kp_rescues[:30]:
            diff = round(r['k_moon'] - r['l_moon'], 4)
            print(f"  {r['vid']:30} book={r['book']} lah={r['lahiri']} kp={r['kp']}  "
                  f"l☽={r['l_moon']} k☽={r['k_moon']} Δ☽={diff}°")

    if lah_rescues:
        print(f"\nLAHIRI RESCUES ({len(lah_rescues)}) -- Lahiri correct planet where KP fails:")
        for r in lah_rescues[:30]:
            diff = round(r['k_moon'] - r['l_moon'], 4)
            print(f"  {r['vid']:30} book={r['book']} lah={r['lahiri']} kp={r['kp']}  "
                  f"l☽={r['l_moon']} k☽={r['k_moon']} Δ☽={diff}°")

    if planet_flip_cases:
        print(f"\nBOTH WRONG BUT DISAGREE ({len(planet_flip_cases)}) -- Lahiri and KP pick different wrong planets:")
        for r in planet_flip_cases[:20]:
            print(f"  {r['vid']:30} book={r['book']} lah={r['lahiri']} kp={r['kp']}")

    print(f"\nLog saved → {log_path}")
    sys.stdout = sys.__stdout__
    tee.close()
    print(f"Log saved → {log_path}")


if __name__ == '__main__':
    main()
