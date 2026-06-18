#!/usr/bin/env python3
"""
gate5_verification.py
----------------------
KE-MND-1 Gate 5 -- compute precise duration/period data for all 4 events.

Events:
  1. Solar eclipse     2026-08-12  (Cancer 25.81°)
  2. Total solar ecl.  2027-08-02  (Cancer 15.67°)
  3. Saturn ingress    Pisces      2025-03-29
  4. Rahu ingress      Aquarius    2025-05-18

Outputs:
  - For eclipses: eclipse_type, first_contact, greatest, last_contact,
                  partial_duration_minutes, totality/annularity_duration_seconds
  - For ingresses: ingress_date, next_ingress_date (= exit date), duration_days_exact

No MONGO_URL required -- pure pyswisseph computation.

Run:
  python3.12 backend/scripts/gate5_verification.py
"""

from __future__ import annotations
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)
_FLAGS_SID   = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
_FLAGS_FALLB = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_SOLAR_ECLIPSE_TYPES = {
    swe.ECL_TOTAL:         "total",
    swe.ECL_ANNULAR:       "annular",
    swe.ECL_ANNULAR_TOTAL: "hybrid",
    swe.ECL_PARTIAL:       "partial",
}

LOG_DIR = Path("KE_TEXTBOOK_DECODE/Test_Vectors/phase4_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

_buf: list[str] = []
def out(msg: str = "") -> None:
    print(msg, flush=True)
    _buf.append(msg)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _jd_to_utc(jd: float) -> str:
    if not jd or jd == 0.0:
        return "(N/A)"
    y, mo, d, h = swe.revjul(jd)
    ts = h * 3600
    hh = int(ts // 3600)
    mm = int((ts % 3600) // 60)
    ss = int(ts % 60)
    return f"{int(y):04d}-{int(mo):02d}-{int(d):02d}T{hh:02d}:{mm:02d}:{ss:02d}Z"


def _jd_to_ist(jd: float) -> str:
    if not jd or jd == 0.0:
        return "(N/A)"
    utc = datetime.strptime(_jd_to_utc(jd), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    ist = utc + timedelta(hours=5, minutes=30)
    return ist.strftime("%Y-%m-%dT%H:%M:%SZ")


def _lon_to_sign_deg(lon: float) -> tuple[str, float]:
    return SIGNS[int(lon // 30) % 12], lon % 30.0


def _eclipse_type_label(flag: int) -> str:
    for k, v in _SOLAR_ECLIPSE_TYPES.items():
        if flag & k:
            return v
    return "unknown"


def _calc_planet(jd: float, swe_id: int) -> tuple[float, float]:
    try:
        r = swe.calc_ut(jd, swe_id, _FLAGS_SID)
    except Exception:
        r = swe.calc_ut(jd, swe_id, _FLAGS_FALLB)
    return r[0][0], r[0][3]


# ── Eclipse verification ──────────────────────────────────────────────────────

def verify_eclipse(target_date: str) -> None:
    """Scan from the day before target_date and find the first solar eclipse."""
    y, mo, d = map(int, target_date.split("-"))
    jd_start = swe.julday(y, mo, d, 0.0) - 2  # 2-day look-back

    result = swe.sol_eclipse_when_glob(jd_start, _FLAGS_SID, 0, False)
    if result is None:
        out(f"  ERROR: no eclipse found near {target_date}")
        return

    ret_flag = result[0]
    tret     = result[1]

    # tret index semantics for sol_eclipse_when_glob (GLOBAL eclipse):
    #   [0] = time of greatest eclipse
    #   [1] = time of max eclipse duration point (close to [0])
    #   [2] = global partial phase start  (C1 -- first place on Earth sees partial)
    #   [3] = global partial phase end    (C4 -- last place on Earth sees partial)
    #   [4] = global totality band start  (C2 -- first place on path sees totality)
    #   [5] = global totality band end    (C3 -- last place on path sees totality)
    #   [6] = central line first contact
    #   [7] = central line last contact
    eclipse_jd            = tret[0]
    global_partial_start  = tret[2]  # C1 globally
    global_partial_end    = tret[3]  # C4 globally
    global_totality_start = tret[4]  # C2 globally (0 if partial only)
    global_totality_end   = tret[5]  # C3 globally

    etype = _eclipse_type_label(ret_flag)

    sun_lon, _ = _calc_planet(eclipse_jd, swe.SUN)
    sign, deg  = _lon_to_sign_deg(sun_lon)

    global_partial_min = (global_partial_end - global_partial_start) * 1440.0
    global_totality_min = (
        (global_totality_end - global_totality_start) * 1440.0
        if (global_totality_start and global_totality_end and global_totality_start > 0.0)
        else None
    )

    out(f"  eclipse_type:                    {etype}")
    out(f"  greatest_eclipse_utc:            {_jd_to_utc(eclipse_jd)}")
    out(f"  greatest_eclipse_ist:            {_jd_to_ist(eclipse_jd)}")
    out(f"  sun_position (sidereal):         {sign} {deg:.2f}°")
    out(f"  global_partial_start_utc:        {_jd_to_utc(global_partial_start)}")
    out(f"  global_partial_end_utc:          {_jd_to_utc(global_partial_end)}")
    out(f"  global_partial_duration:         {global_partial_min:.1f} min  ({global_partial_min/60:.2f} hrs)")
    if global_totality_min is not None:
        out(f"  global_totality_band_start_utc:  {_jd_to_utc(global_totality_start)}")
        out(f"  global_totality_band_end_utc:    {_jd_to_utc(global_totality_end)}")
        out(f"  global_totality_band_sweep:      {global_totality_min:.1f} min  "
            f"(shadow sweeps Earth over this window)")
    out(f"  NOTE: Single-point totality duration varies by path location.")


# ── Ingress verification ──────────────────────────────────────────────────────

def _sign_index(lon: float) -> int:
    return int(lon // 30) % 12


def verify_ingress(planet_name: str, swe_id: int | None, target_date: str,
                   expected_sign: str, is_ketu: bool = False) -> None:
    """
    Confirm the ingress near target_date, then scan forward to find the
    NEXT ingress (= exit date / duration_days).
    """
    y, mo, d = map(int, target_date.split("-"))
    search_start = swe.julday(y, mo, d, 0.0) - 5
    search_end   = swe.julday(y, mo, d, 0.0) + 10

    def _get_lon(jd: float) -> float:
        if is_ketu:
            rahu_lon, _ = _calc_planet(jd, swe.MEAN_NODE)
            return (rahu_lon + 180.0) % 360.0
        return _calc_planet(jd, swe_id)[0]

    # Find precise ingress near target_date (binary search around ±5 days)
    step = 0.25
    prev_sign = _sign_index(_get_lon(search_start))
    precise_jd = None
    jd = search_start
    while jd <= search_end:
        curr_sign = _sign_index(_get_lon(jd))
        if curr_sign != prev_sign:
            # Narrow down with binary search
            lo, hi = jd - step, jd
            for _ in range(30):
                mid = (lo + hi) / 2
                if _sign_index(_get_lon(mid)) == _sign_index(_get_lon(lo)):
                    lo = mid
                else:
                    hi = mid
            precise_jd = (lo + hi) / 2
            precise_sign = SIGNS[curr_sign]
            break
        prev_sign = curr_sign
        jd += step

    if precise_jd is None:
        out(f"  WARNING: Could not find ingress near {target_date} ±5 days. "
            f"Check if target date is already inside the sign.")
        # Use target date as-is
        precise_jd = swe.julday(y, mo, d, 0.0)
        precise_sign = expected_sign

    # Use precise_sign from binary search (= sign AFTER crossing), not boundary point
    ingress_lon = _get_lon(precise_jd)
    ingress_sign = precise_sign  # sign detected during crossing, not re-derived from midpoint

    out(f"  ingress_date_utc:          {_jd_to_utc(precise_jd)}")
    out(f"  ingress_date_ist:          {_jd_to_ist(precise_jd)}")
    out(f"  ingress_sign (computed):   {ingress_sign}  (expected: {expected_sign})")
    out(f"  boundary_lon:              ~{ingress_lon:.4f}° (at crossing midpoint)")

    # Now find the NEXT ingress for same planet (= exit date)
    scan_jd = precise_jd + 5.0  # start scan 5 days after ingress
    scan_end = precise_jd + 1100.0  # max scan window
    step2 = 0.5
    prev2 = _sign_index(_get_lon(scan_jd))
    exit_jd = None
    jd2 = scan_jd
    while jd2 <= scan_end:
        curr2 = _sign_index(_get_lon(jd2))
        if curr2 != prev2:
            lo2, hi2 = jd2 - step2, jd2
            for _ in range(30):
                mid2 = (lo2 + hi2) / 2
                if _sign_index(_get_lon(mid2)) == _sign_index(_get_lon(lo2)):
                    lo2 = mid2
                else:
                    hi2 = mid2
            exit_jd = (lo2 + hi2) / 2
            exit_sign = SIGNS[curr2]
            break
        prev2 = curr2
        jd2 += step2

    if exit_jd is not None:
        duration_days = exit_jd - precise_jd
        out(f"  exit_date_utc:             {_jd_to_utc(exit_jd)}")
        out(f"  exit_to_sign:              {exit_sign}")
        out(f"  duration_days_exact:       {duration_days:.1f} days  ({duration_days/365.25:.2f} years)")
        out(f"  duration_months_approx:    {duration_days/30.44:.1f} months")
    else:
        out(f"  exit_date: not found in scan window (planet still in sign after 1100 days)")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    from datetime import datetime as dt_now
    ts = dt_now.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    log_path = LOG_DIR / f"gate5_verification_{ts}.log"

    out("gate5_verification.py -- KE-MND-1 Gate 5 Duration/Period Verification")
    out(f"Log → {log_path}")
    out(f"Started: {dt_now.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    out()

    # ── Event 1: Solar eclipse 2026-08-12 ────────────────────────────────
    out("=" * 80)
    out("EVENT 1: Solar Eclipse -- 2026-08-12")
    out("=" * 80)
    verify_eclipse("2026-08-12")
    out()

    # ── Event 2: Total solar eclipse 2027-08-02 ───────────────────────────
    out("=" * 80)
    out("EVENT 2: Total Solar Eclipse -- 2027-08-02")
    out("=" * 80)
    verify_eclipse("2027-08-02")
    out()

    # ── Event 3: Saturn ingress Pisces 2025-03-29 ─────────────────────────
    out("=" * 80)
    out("EVENT 3: Saturn Ingress into Pisces (sidereal) -- 2025-03-29")
    out("=" * 80)
    verify_ingress("Saturn", swe.SATURN, "2025-03-29", "Pisces")
    out()

    # ── Event 4: Rahu ingress Aquarius 2025-05-18 ─────────────────────────
    out("=" * 80)
    out("EVENT 4: Rahu Ingress into Aquarius (sidereal, retrograde) -- 2025-05-18")
    out("=" * 80)
    verify_ingress("Rahu", swe.MEAN_NODE, "2025-05-18", "Aquarius")
    out()

    out("=" * 80)
    out("Gate 5 Summary")
    out("=" * 80)
    out()
    out("Cross-check all 4 against Drik Panchang:")
    out("  • Eclipses: compare greatest_eclipse_ist against Drik Panchang eclipse date + time")
    out("  • Ingresses: compare ingress_date_ist against Drik Panchang sankranti/ingress table")
    out("  • Duration: compare partial_duration_minutes (eclipses) and duration_months (transits)")
    out("  Tolerance: ±1 day for ingresses, ±5 minutes for eclipse maximum")
    out()

    log_path.write_text("\n".join(_buf) + "\n", encoding="utf-8")
    print(f"\nLog → {log_path}", flush=True)


if __name__ == "__main__":
    main()
