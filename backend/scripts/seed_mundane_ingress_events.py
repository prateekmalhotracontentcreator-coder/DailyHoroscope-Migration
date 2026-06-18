"""
Seed 17-year Planetary Ingress calendar (2020-01-01 → 2036-12-31)
into mundane_ingress_events collection.

Planets: Saturn, Jupiter, Rahu, Ketu, Mars, Sun

Dry-run (default): prints all detected ingresses.
Live:              --live flag upserts into DB on (planet, to_sign, ingress_date_utc) key.

Expected output: ~130-160 ingress events over 17 years.

Run from project root:
    python3 backend/scripts/seed_mundane_ingress_events.py
    python3 backend/scripts/seed_mundane_ingress_events.py --live
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

# Compute range
RANGE_START = swe.julday(2020, 1, 1, 0.0)
RANGE_END   = swe.julday(2036, 12, 31, 23.99)

# Planet configurations: (name, swe_id, scan_step_days)
# Slow planets need small steps to catch retrograde re-entries precisely.
# Sun needs fine steps for sankranti (monthly sign change).
PLANET_CONFIGS = [
    ("Saturn",  swe.SATURN,    0.25),   # ~29 years/revolution → ~2.5 years/sign
    ("Jupiter", swe.JUPITER,   0.25),   # ~12 years → ~1 year/sign
    ("Rahu",    swe.MEAN_NODE, 0.25),   # ~18 years (retrograde) → ~1.5 years/sign
    ("Ketu",    None,          0.25),   # Always Rahu + 180°
    ("Mars",    swe.MARS,      0.1),    # ~2 years/revolution → ~1.5-8 months/sign
    ("Sun",     swe.SUN,       0.05),   # ~1 year → ~1 month/sign (Sankranti)
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _calc_planet(jd: float, swe_id: int) -> tuple[float, float]:
    try:
        result = swe.calc_ut(jd, swe_id, _SWE_FLAGS)
    except Exception:
        result = swe.calc_ut(jd, swe_id, _SWE_FLAGS_FALLBACK)
    return result[0][0], result[0][3]


def _sign_index(lon: float) -> int:
    return int(lon // 30) % 12


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


# ── Ingress Detection ─────────────────────────────────────────────────────────

def detect_ingresses(planet_name: str, swe_id: int | None, step_days: float) -> list[dict]:
    """
    Scan the range and detect each sign boundary crossing.
    For Ketu: derived from Rahu + 180°.
    Returns sorted list of ingress event dicts.
    """
    ingresses = []

    def _get_lon(jd: float) -> float:
        if planet_name == "Ketu":
            rahu_lon, _ = _calc_planet(jd, swe.MEAN_NODE)
            return (rahu_lon + 180.0) % 360.0
        else:
            lon, _ = _calc_planet(jd, swe_id)
            return lon

    def _get_speed(jd: float) -> float:
        if planet_name == "Ketu":
            _, speed = _calc_planet(jd, swe.MEAN_NODE)
            return -speed  # Ketu speed = negative of Rahu speed
        else:
            _, speed = _calc_planet(jd, swe_id)
            return speed

    jd = RANGE_START
    prev_lon = _get_lon(jd)
    prev_sign = _sign_index(prev_lon)
    seen_crossings: set[str] = set()  # deduplicate by (from_sign, to_sign, approx_date)

    while jd <= RANGE_END:
        jd += step_days
        curr_lon = _get_lon(jd)
        curr_sign = _sign_index(curr_lon)

        if curr_sign == prev_sign:
            prev_lon = curr_lon
            continue

        # Sign boundary crossed -- binary search to pinpoint
        lo, hi = jd - step_days, jd
        # Determine direction of crossing
        # Account for 360/0 wrap
        lon_diff = (curr_lon - prev_lon) % 360
        if lon_diff > 180:
            lon_diff -= 360  # retrograde crossing

        target_boundary = (curr_sign * 30.0) if lon_diff >= 0 else (prev_sign * 30.0)

        for _ in range(30):
            mid = (lo + hi) / 2
            mid_lon = _get_lon(mid)
            mid_sign = _sign_index(mid_lon)
            if mid_sign == prev_sign:
                lo = mid
            else:
                hi = mid

        precise_jd = (lo + hi) / 2
        if not (RANGE_START <= precise_jd <= RANGE_END):
            prev_lon = curr_lon
            prev_sign = curr_sign
            continue

        precise_lon = _get_lon(precise_jd)
        from_sign = SIGNS[prev_sign]
        to_sign = SIGNS[curr_sign]  # curr_sign is always the new sign after the crossing

        # Deduplicate key
        approx_day = _jd_to_utc_iso(precise_jd)[:10]
        dedup_key = f"{from_sign}→{to_sign}@{approx_day}"
        if dedup_key in seen_crossings:
            prev_lon = curr_lon
            prev_sign = curr_sign
            continue
        seen_crossings.add(dedup_key)

        utc_iso = _jd_to_utc_iso(precise_jd)
        speed = _get_speed(precise_jd)
        retrograde_re_entry = speed < 0

        # Approximate duration in current sign
        # Find next ingress from same planet to estimate days
        # We'll fill this with an approximation based on planet
        duration_days = _approx_duration(planet_name)

        # Ingress degree (should be 0° of to_sign)
        ingress_degree = precise_lon

        ingresses.append({
            "planet": planet_name,
            "from_sign": from_sign,
            "to_sign": to_sign,
            "ingress_date_utc": utc_iso,
            "ingress_date_ist": _ist_from_utc_iso(utc_iso),
            "ingress_degree": round(ingress_degree, 4),
            "retrograde_re_entry": retrograde_re_entry,
            "duration_days_approx": duration_days,
            "active": True,
        })

        prev_lon = curr_lon
        prev_sign = curr_sign

    return ingresses


def _approx_duration(planet: str) -> int:
    """Approximate days in a sign for the planet (rough average)."""
    return {
        "Saturn":  900,   # ~2.5 years
        "Jupiter": 365,   # ~1 year
        "Rahu":    548,   # ~18 months
        "Ketu":    548,
        "Mars":    60,    # ~2 months average (can be 1.5-8 months)
        "Sun":     30,    # ~1 month
    }.get(planet, 30)


# ── Print Summary ─────────────────────────────────────────────────────────────

def print_summary(all_events: list[dict]) -> None:
    print("\n" + "=" * 80)
    print("PLANETARY INGRESS CALENDAR -- GATE 5 MANUAL VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total ingress events: {len(all_events)}")
    print()

    for planet in ["Saturn", "Jupiter", "Rahu", "Ketu", "Mars", "Sun"]:
        planet_events = [e for e in all_events if e["planet"] == planet]
        print(f"--- {planet} ({len(planet_events)} ingresses) ---")
        for e in planet_events:
            retro_flag = " [R]" if e["retrograde_re_entry"] else ""
            print(f"  {e['ingress_date_utc'][:16]}  {e['from_sign']:<14} → {e['to_sign']:<14}{retro_flag}")
        print()
    print("=" * 80)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Seed mundane planetary ingress events")
    parser.add_argument("--live", action="store_true", help="Write to DB (default: dry-run)")
    args = parser.parse_args()

    all_events: list[dict] = []
    for planet_name, swe_id, step_days in PLANET_CONFIGS:
        print(f"Computing {planet_name} ingresses ...")
        try:
            events = detect_ingresses(planet_name, swe_id, step_days)
            print(f"  → {len(events)} ingresses found")
            all_events.extend(events)
        except Exception as exc:
            print(f"  ERROR computing {planet_name}: {exc}")

    all_events.sort(key=lambda e: e["ingress_date_utc"])
    print_summary(all_events)

    if not args.live:
        print("DRY-RUN complete. Pass --live to upsert into horoscope_db.mundane_ingress_events")
        return

    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        print("ERROR: MONGO_URL env var not set.")
        sys.exit(1)

    client = pymongo.MongoClient(mongo_url)
    db = client["horoscope_db"]
    col = db["mundane_ingress_events"]
    col.create_index(
        [("planet", 1), ("to_sign", 1), ("ingress_date_utc", 1)],
        unique=True,
        background=True,
    )
    col.create_index([("planet", 1)], background=True)
    col.create_index([("ingress_date_utc", 1)], background=True)

    upserted = 0
    errors = 0
    for doc in all_events:
        try:
            col.update_one(
                {
                    "planet": doc["planet"],
                    "to_sign": doc["to_sign"],
                    "ingress_date_utc": doc["ingress_date_utc"],
                },
                {"$set": doc},
                upsert=True,
            )
            upserted += 1
        except Exception as exc:
            print(f"  ERROR upserting {doc['planet']} → {doc['to_sign']} @ {doc['ingress_date_utc']}: {exc}")
            errors += 1

    print(f"\n✅ Upserted {upserted} ingress events into horoscope_db.mundane_ingress_events")
    if errors:
        print(f"⚠ {errors} upsert error(s)")
    client.close()


if __name__ == "__main__":
    main()
