"""
Seed 10-year Eclipse + Lunation calendar (2026-06-17 → 2036-12-31)
into mundane_eclipse_events collection.

Dry-run (default): prints all computed events.
Live:              --live flag upserts into DB on event_date_utc key.

Expected output: ~240 lunations + ~40-50 eclipses = ~290 total events.

Run from project root:
    python3 backend/scripts/seed_mundane_eclipse_events.py
    python3 backend/scripts/seed_mundane_eclipse_events.py --live
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone

import swisseph as swe
import pymongo

# ── Setup ─────────────────────────────────────────────────────────────────────

swe.set_sid_mode(swe.SIDM_LAHIRI)
_SWE_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
_SWE_FLAGS_FALLBACK = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishtha", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

# Compute range
RANGE_START = swe.julday(2026, 6, 17, 0.0)
RANGE_END   = swe.julday(2036, 12, 31, 23.99)

# Eclipse type flags returned by pyswisseph
_SOLAR_ECLIPSE_TYPES = {
    swe.ECL_TOTAL:          "total",
    swe.ECL_ANNULAR:        "annular",
    swe.ECL_ANNULAR_TOTAL:  "hybrid",
    swe.ECL_PARTIAL:        "partial",
}
_LUNAR_ECLIPSE_TYPES = {
    swe.ECL_TOTAL:      "total",
    swe.ECL_PARTIAL:    "partial",
    swe.ECL_PENUMBRAL:  "penumbral",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _calc_planet(jd: float, swe_id: int) -> tuple[float, float]:
    try:
        result = swe.calc_ut(jd, swe_id, _SWE_FLAGS)
    except Exception:
        result = swe.calc_ut(jd, swe_id, _SWE_FLAGS_FALLBACK)
    return result[0][0], result[0][3]


def _lon_to_sign_degree(lon: float) -> tuple[str, float]:
    sign = SIGNS[int(lon // 30) % 12]
    degree_in_sign = lon % 30.0
    return sign, degree_in_sign


def _lon_to_nakshatra(lon: float) -> tuple[str, int]:
    nak_width = 360.0 / 27
    nak_index = int(lon / nak_width) % 27
    pada = int((lon % nak_width) / (nak_width / 4)) + 1
    return NAKSHATRAS[nak_index], pada


def _jd_to_utc_iso(jd: float) -> str:
    y, mo, d, h = swe.revjul(jd)
    total_secs = h * 3600
    hh = int(total_secs // 3600)
    mm = int((total_secs % 3600) // 60)
    ss = int(total_secs % 60)
    return f"{int(y):04d}-{int(mo):02d}-{int(d):02d}T{hh:02d}:{mm:02d}:{ss:02d}Z"


def _ist_from_utc_iso(utc_iso: str) -> str:
    dt = datetime.strptime(utc_iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    ist = dt + timedelta(hours=5, minutes=30)
    return ist.strftime("%Y-%m-%dT%H:%M:%SZ")


def _eclipse_type_flag(ret_flag: int, type_map: dict) -> str:
    for flag, label in type_map.items():
        if ret_flag & flag:
            return label
    return "unknown"


# ── Solar Eclipses ────────────────────────────────────────────────────────────

def compute_solar_eclipses() -> list[dict]:
    """Compute all solar eclipses in range using swe.sol_eclipse_when_glob."""
    events = []
    jd = RANGE_START
    while jd < RANGE_END:
        try:
            # ifltype=0 means any eclipse type; backward=0 means forward search
            result = swe.sol_eclipse_when_glob(jd + 0.1, swe.FLG_MOSEPH, 0)
        except Exception:
            try:
                result = swe.sol_eclipse_when_glob(jd + 0.1, swe.FLG_SWIEPH, 0)
            except Exception as exc:
                print(f"  Solar eclipse search failed at JD {jd:.1f}: {exc}")
                jd += 30
                continue

        ret_flag = result[0]
        tret = result[1]
        eclipse_jd = tret[0]  # maximum eclipse time

        if eclipse_jd <= jd or eclipse_jd >= RANGE_END:
            break

        utc_iso = _jd_to_utc_iso(eclipse_jd)

        # Get Sun position at eclipse maximum
        sun_lon, _ = _calc_planet(eclipse_jd, swe.SUN)
        sign, deg_in_sign = _lon_to_sign_degree(sun_lon)
        nak, pada = _lon_to_nakshatra(sun_lon)
        eclipse_type = _eclipse_type_flag(ret_flag, _SOLAR_ECLIPSE_TYPES)

        # Saros series: not directly available via sol_eclipse_when_glob;
        # use eclipse_jd modulo approximate saros period (6585.3211 days) as placeholder
        saros_series = None  # Cannot compute without extended ephemeris details

        doc = {
            "event_type": "solar_eclipse",
            "event_date_utc": utc_iso,
            "event_date_ist": _ist_from_utc_iso(utc_iso),
            "sign": sign,
            "degree_in_sign": round(deg_in_sign, 4),
            "absolute_degree": round(sun_lon, 4),
            "nakshatra": nak,
            "nakshatra_pada": pada,
            "saros_series": saros_series,
            "eclipse_type": eclipse_type,
            "eclipse_magnitude": None,
            "eclipse_path_countries": [],
            "active": True,
        }
        events.append(doc)
        jd = eclipse_jd + 20  # advance past this eclipse (min gap ~28 days)

    return events


# ── Lunar Eclipses ────────────────────────────────────────────────────────────

def compute_lunar_eclipses() -> list[dict]:
    """Compute all lunar eclipses in range using swe.lun_eclipse_when."""
    events = []
    jd = RANGE_START
    while jd < RANGE_END:
        try:
            result = swe.lun_eclipse_when(jd + 0.1, swe.FLG_SWIEPH, 0)
        except Exception:
            try:
                result = swe.lun_eclipse_when(jd + 0.1, swe.FLG_MOSEPH, 0)
            except Exception as exc:
                print(f"  Lunar eclipse search failed at JD {jd:.1f}: {exc}")
                jd += 30
                continue

        ret_flag = result[0]
        tret = result[1]
        eclipse_jd = tret[0]  # greatest eclipse time

        if eclipse_jd <= jd or eclipse_jd >= RANGE_END:
            break

        utc_iso = _jd_to_utc_iso(eclipse_jd)

        # Moon position at eclipse = opposite Sun (lunar eclipse = Full Moon)
        moon_lon, _ = _calc_planet(eclipse_jd, swe.MOON)
        sign, deg_in_sign = _lon_to_sign_degree(moon_lon)
        nak, pada = _lon_to_nakshatra(moon_lon)
        eclipse_type = _eclipse_type_flag(ret_flag, _LUNAR_ECLIPSE_TYPES)

        doc = {
            "event_type": "lunar_eclipse",
            "event_date_utc": utc_iso,
            "event_date_ist": _ist_from_utc_iso(utc_iso),
            "sign": sign,
            "degree_in_sign": round(deg_in_sign, 4),
            "absolute_degree": round(moon_lon, 4),
            "nakshatra": nak,
            "nakshatra_pada": pada,
            "saros_series": None,
            "eclipse_type": eclipse_type,
            "eclipse_magnitude": None,
            "eclipse_path_countries": [],
            "active": True,
        }
        events.append(doc)
        jd = eclipse_jd + 20  # advance past this eclipse

    return events


# ── New & Full Moons ──────────────────────────────────────────────────────────

def compute_lunations() -> list[dict]:
    """
    Scan Moon-Sun elongation to detect new moons (0°) and full moons (180°).
    Uses binary search refinement for hr:min:sec precision.
    """
    events = []

    def _elongation(jd: float) -> float:
        sun_lon, _ = _calc_planet(jd, swe.SUN)
        moon_lon, _ = _calc_planet(jd, swe.MOON)
        return (moon_lon - sun_lon) % 360.0

    # Scan daily; Moon moves ~13°/day, so sample every 0.5 days
    step = 0.5
    jd = RANGE_START
    prev_elong = _elongation(jd)

    while jd < RANGE_END:
        jd += step
        if jd >= RANGE_END:
            break
        curr_elong = _elongation(jd)

        for target in [0.0, 180.0]:
            # Check if we crossed the target (accounting for 0°/360° wrap)
            crossed = False
            if target == 0.0:
                # New moon: elongation goes from high (close to 360) to low (close to 0)
                # OR from some value through 0
                if prev_elong > 350 and curr_elong < 10:
                    crossed = True
                elif prev_elong < 180 and curr_elong < prev_elong:
                    pass  # Not a new moon crossing
            if target == 180.0:
                if prev_elong < 180.0 and curr_elong >= 180.0:
                    crossed = True

            if crossed:
                # Binary search to pinpoint the exact moment
                lo, hi = jd - step, jd
                for _ in range(20):
                    mid = (lo + hi) / 2
                    e = _elongation(mid)
                    if target == 0.0:
                        if e > 180:
                            lo = mid
                        else:
                            hi = mid
                    else:
                        if e < target:
                            lo = mid
                        else:
                            hi = mid
                precise_jd = (lo + hi) / 2
                utc_iso = _jd_to_utc_iso(precise_jd)

                event_type = "new_moon" if target == 0.0 else "full_moon"
                if event_type == "new_moon":
                    ref_lon, _ = _calc_planet(precise_jd, swe.SUN)
                else:
                    ref_lon, _ = _calc_planet(precise_jd, swe.MOON)

                sign, deg_in_sign = _lon_to_sign_degree(ref_lon)
                nak, pada = _lon_to_nakshatra(ref_lon)

                doc = {
                    "event_type": event_type,
                    "event_date_utc": utc_iso,
                    "event_date_ist": _ist_from_utc_iso(utc_iso),
                    "sign": sign,
                    "degree_in_sign": round(deg_in_sign, 4),
                    "absolute_degree": round(ref_lon, 4),
                    "nakshatra": nak,
                    "nakshatra_pada": pada,
                    "saros_series": None,
                    "eclipse_type": None,
                    "eclipse_magnitude": None,
                    "eclipse_path_countries": [],
                    "active": True,
                }
                events.append(doc)

        prev_elong = curr_elong

    return events


def _improved_lunations() -> list[dict]:
    """
    More reliable lunation detection using backward/forward step pairs.
    Moon phase angle: 0 = new moon, 180 = full moon.
    """
    events = []

    def _phase(jd: float) -> float:
        sun, _ = _calc_planet(jd, swe.SUN)
        moon, _ = _calc_planet(jd, swe.MOON)
        return (moon - sun) % 360.0

    # Start a bit before range to catch exact first lunation
    jd = RANGE_START - 30
    phase_prev = _phase(jd)

    while jd < RANGE_END + 30:
        jd += 0.25  # 6-hour steps for good resolution
        phase_curr = _phase(jd)

        # Detect new moon crossing (phase goes through 0 / 360)
        for target, etype in [(0.0, "new_moon"), (180.0, "full_moon")]:
            crossed = False
            if target == 0.0:
                if phase_prev > 355.0 and phase_curr < 5.0:
                    crossed = True
            elif target == 180.0:
                if phase_prev < 180.0 and phase_curr >= 180.0:
                    crossed = True

            if crossed and RANGE_START <= jd <= RANGE_END:
                lo, hi = jd - 0.25, jd
                for _ in range(30):
                    mid = (lo + hi) / 2
                    p = _phase(mid)
                    if target == 0.0:
                        if p > 180:
                            lo = mid
                        else:
                            hi = mid
                    else:
                        if p < target:
                            lo = mid
                        else:
                            hi = mid
                precise_jd = (lo + hi) / 2
                if not (RANGE_START <= precise_jd <= RANGE_END):
                    continue
                utc_iso = _jd_to_utc_iso(precise_jd)
                ref_lon, _ = _calc_planet(precise_jd, swe.SUN if etype == "new_moon" else swe.MOON)
                sign, deg = _lon_to_sign_degree(ref_lon)
                nak, pada = _lon_to_nakshatra(ref_lon)
                events.append({
                    "event_type": etype,
                    "event_date_utc": utc_iso,
                    "event_date_ist": _ist_from_utc_iso(utc_iso),
                    "sign": sign,
                    "degree_in_sign": round(deg, 4),
                    "absolute_degree": round(ref_lon, 4),
                    "nakshatra": nak,
                    "nakshatra_pada": pada,
                    "saros_series": None,
                    "eclipse_type": None,
                    "eclipse_magnitude": None,
                    "eclipse_path_countries": [],
                    "active": True,
                })

        phase_prev = phase_curr

    # Deduplicate: merge events within 0.5 days of each other
    events.sort(key=lambda e: e["event_date_utc"])
    deduped = []
    prev_utc = ""
    for ev in events:
        if not deduped or ev["event_date_utc"][:10] != prev_utc[:10] or ev["event_type"] != deduped[-1]["event_type"]:
            deduped.append(ev)
            prev_utc = ev["event_date_utc"]
    return deduped


# ── Print Summary ─────────────────────────────────────────────────────────────

def print_summary(events: list[dict]) -> None:
    eclipses = [e for e in events if "eclipse" in e["event_type"]]
    lunations = [e for e in events if "eclipse" not in e["event_type"]]
    print("\n" + "=" * 80)
    print("ECLIPSE & LUNATION CALENDAR -- GATE 5 MANUAL VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total events: {len(events)} ({len(eclipses)} eclipses + {len(lunations)} lunations)")
    print("\n--- ECLIPSES ---")
    for e in eclipses:
        print(f"  {e['event_type']:<15} {e['event_date_utc'][:16]}  "
              f"{e['sign']:<14} {e['degree_in_sign']:.2f}°  {e.get('eclipse_type','?')}")
    print(f"\n--- LUNATIONS (first 20 of {len(lunations)}) ---")
    for e in lunations[:20]:
        print(f"  {e['event_type']:<12} {e['event_date_utc'][:16]}  {e['sign']:<14} {e['degree_in_sign']:.2f}°")
    if len(lunations) > 20:
        print(f"  ... {len(lunations) - 20} more lunations")
    print("=" * 80)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Seed mundane eclipse + lunation events")
    parser.add_argument("--live", action="store_true", help="Write to DB (default: dry-run)")
    args = parser.parse_args()

    print("Computing solar eclipses ...")
    solar = compute_solar_eclipses()
    print(f"  → {len(solar)} solar eclipses found")

    print("Computing lunar eclipses ...")
    lunar = compute_lunar_eclipses()
    print(f"  → {len(lunar)} lunar eclipses found")

    print("Computing new/full moons ...")
    lunations = _improved_lunations()
    print(f"  → {len(lunations)} lunation events found")

    all_events = solar + lunar + lunations
    all_events.sort(key=lambda e: e["event_date_utc"])
    print_summary(all_events)

    if not args.live:
        print("DRY-RUN complete. Pass --live to upsert into horoscope_db.mundane_eclipse_events")
        return

    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        print("ERROR: MONGO_URL env var not set.")
        sys.exit(1)

    client = pymongo.MongoClient(mongo_url)
    db = client["horoscope_db"]
    col = db["mundane_eclipse_events"]
    col.create_index([("event_date_utc", 1)], unique=True, background=True)
    col.create_index([("event_type", 1)], background=True)
    col.create_index([("sign", 1)], background=True)

    upserted = 0
    errors = 0
    for doc in all_events:
        try:
            col.update_one(
                {"event_date_utc": doc["event_date_utc"], "event_type": doc["event_type"]},
                {"$set": doc},
                upsert=True,
            )
            upserted += 1
        except Exception as exc:
            print(f"  ERROR upserting {doc['event_date_utc']}: {exc}")
            errors += 1

    print(f"\n✅ Upserted {upserted} events into horoscope_db.mundane_eclipse_events")
    if errors:
        print(f"⚠ {errors} upsert error(s)")
    client.close()


if __name__ == "__main__":
    main()
