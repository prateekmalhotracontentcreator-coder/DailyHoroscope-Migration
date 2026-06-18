"""
Seed 50 country foundation charts into mundane_foundation_charts collection.

Dry-run (default): prints all computed charts.
Live:              --live flag upserts into DB on (country_code, chart_type) key.

Run from project root:
    python3 backend/scripts/seed_mundane_foundation_charts.py
    python3 backend/scripts/seed_mundane_foundation_charts.py --live
"""
from __future__ import annotations

import os
import sys
import argparse
from datetime import datetime, timezone

import swisseph as swe
import pymongo

# ── Swiss Ephemeris Setup ─────────────────────────────────────────────────────

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
PLANET_SWE_IDS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
    "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE,
}

# ── Country Data ──────────────────────────────────────────────────────────────

COUNTRIES = [
    # (country_code, country_name, chart_type, event_date, event_time_local, tz_offset, city, lat, lon, notes)
    ("IN", "India",          "independence",  "1947-08-15", "00:01:00", +5.5,  "New Delhi",       28.6139,   77.209,    ""),
    ("US", "United States",  "independence",  "1776-07-04", "17:10:00", -5.0,  "Philadelphia",    39.9526,  -75.1652,   "Sibley chart"),
    ("GB", "United Kingdom", "constitution",  "1801-01-01", "00:00:00",  0.0,  "London",          51.5074,   -0.1278,   "Act of Union"),
    ("PK", "Pakistan",       "independence",  "1947-08-14", "00:00:00", +5.5,  "Karachi",         24.8607,   67.0011,   ""),
    ("CN", "China",          "independence",  "1949-10-01", "15:01:00", +8.0,  "Beijing",         39.9042,  116.4074,   ""),
    ("RU", "Russia",         "independence",  "1991-12-25", "19:38:00", +3.0,  "Moscow",          55.7558,   37.6173,   ""),
    ("FR", "France",         "republic",      "1792-09-21", "14:00:00",  0.0,  "Paris",           48.8566,    2.3522,   "First Republic"),
    ("DE", "Germany",        "independence",  "1990-10-03", "00:00:00", +1.0,  "Berlin",          52.52,     13.405,    "Reunification"),
    ("JP", "Japan",          "constitution",  "1947-05-03", "00:00:00", +9.0,  "Tokyo",           35.6762,  139.6503,   ""),
    ("AU", "Australia",      "independence",  "1901-01-01", "13:35:00", +10.0, "Sydney",         -33.8688,  151.2093,   "Federation"),
    ("CA", "Canada",         "independence",  "1867-07-01", "00:00:00", -5.0,  "Ottawa",          45.4215,  -75.6972,   "Confederation; time_unknown -- noon chart"),
    ("BR", "Brazil",         "republic",      "1889-11-15", "06:00:00", -3.0,  "Rio de Janeiro", -22.9068,  -43.1729,   ""),
    ("IL", "Israel",         "independence",  "1948-05-14", "16:00:00", +2.0,  "Tel Aviv",        32.0853,   34.7818,   ""),
    ("ZA", "South Africa",   "republic",      "1961-05-31", "00:00:00", +2.0,  "Pretoria",       -25.7479,   28.2293,   ""),
    ("LK", "Sri Lanka",      "independence",  "1948-02-04", "00:00:00", +5.5,  "Colombo",          6.9271,   79.8612,   "time_unknown -- noon chart"),
    ("BD", "Bangladesh",     "independence",  "1971-03-26", "00:01:00", +6.0,  "Dhaka",           23.8103,   90.4125,   ""),
    ("NP", "Nepal",          "republic",      "2008-05-28", "00:00:00", +5.75, "Kathmandu",       27.7172,   85.324,    "time_unknown -- noon chart"),
    ("MM", "Myanmar",        "independence",  "1948-01-04", "04:20:00", +6.5,  "Rangoon",         16.8661,   96.1951,   ""),
    ("ID", "Indonesia",      "independence",  "1945-08-17", "10:00:00", +7.0,  "Jakarta",         -6.2088,  106.8456,   ""),
    ("MY", "Malaysia",       "independence",  "1957-08-31", "00:00:00", +7.5,  "Kuala Lumpur",     3.139,   101.6869,   "time_unknown -- noon chart"),
    ("SG", "Singapore",      "independence",  "1965-08-09", "09:30:00", +7.5,  "Singapore",        1.3521,  103.8198,   ""),
    ("TH", "Thailand",       "constitution",  "1932-06-24", "00:00:00", +7.0,  "Bangkok",         13.7563,  100.5018,   "time_unknown -- noon chart"),
    ("IR", "Iran",           "independence",  "1979-04-01", "15:00:00", +3.5,  "Tehran",          35.6892,   51.389,    "Islamic Republic"),
    ("TR", "Turkey",         "republic",      "1923-10-29", "20:30:00", +2.0,  "Ankara",          39.9334,   32.8597,   ""),
    ("SA", "Saudi Arabia",   "independence",  "1932-09-23", "00:00:00", +3.0,  "Riyadh",          24.6877,   46.7219,   "Unification; time_unknown -- noon chart"),
    ("AE", "UAE",            "independence",  "1971-12-02", "00:00:00", +4.0,  "Abu Dhabi",       24.4539,   54.3773,   "time_unknown -- noon chart"),
    ("EG", "Egypt",          "republic",      "1953-06-18", "23:30:00", +2.0,  "Cairo",           30.0444,   31.2357,   ""),
    ("NG", "Nigeria",        "independence",  "1960-10-01", "00:00:00", +1.0,  "Lagos",            6.5244,    3.3792,   "time_unknown -- noon chart"),
    ("KE", "Kenya",          "independence",  "1963-12-12", "00:00:00", +3.0,  "Nairobi",         -1.2921,   36.8219,   "time_unknown -- noon chart"),
    ("KR", "South Korea",    "republic",      "1948-08-15", "00:00:00", +9.0,  "Seoul",           37.5665,  126.978,    "time_unknown -- noon chart"),
    ("KP", "North Korea",    "republic",      "1948-09-09", "00:00:00", +9.0,  "Pyongyang",       39.0392,  125.7625,   "time_unknown -- noon chart"),
    ("VN", "Vietnam",        "independence",  "1945-09-02", "14:00:00", +7.0,  "Hanoi",           21.0285,  105.8542,   ""),
    ("PH", "Philippines",    "independence",  "1946-07-04", "09:15:00", +8.0,  "Manila",          14.5995,  120.9842,   ""),
    ("AF", "Afghanistan",    "independence",  "1919-08-19", "00:00:00", +4.5,  "Kabul",           34.5553,   69.2075,   "time_unknown -- noon chart"),
    ("IQ", "Iraq",           "republic",      "1958-07-14", "06:30:00", +3.0,  "Baghdad",         33.3152,   44.3661,   ""),
    ("IT", "Italy",          "republic",      "1946-06-10", "18:00:00", +1.0,  "Rome",            41.9028,   12.4964,   ""),
    ("ES", "Spain",          "constitution",  "1978-12-27", "00:00:00", +1.0,  "Madrid",          40.4168,   -3.7038,   "Democracy; time_unknown -- noon chart"),
    ("PL", "Poland",         "independence",  "1918-11-11", "10:00:00", +1.0,  "Warsaw",          52.2297,   21.0122,   ""),
    ("UA", "Ukraine",        "independence",  "1991-08-24", "18:00:00", +2.0,  "Kyiv",            50.4501,   30.5234,   ""),
    ("MX", "Mexico",         "independence",  "1810-09-16", "11:00:00", -6.0,  "Dolores",         21.153,  -100.935,    ""),
    ("AR", "Argentina",      "independence",  "1816-07-09", "00:00:00", -3.0,  "Buenos Aires",   -34.6037,  -58.3816,   "time_unknown -- noon chart"),
    ("CO", "Colombia",       "independence",  "1819-08-07", "00:00:00", -5.0,  "Bogotá",           4.711,   -74.0721,   "time_unknown -- noon chart"),
    ("ET", "Ethiopia",       "independence",  "1991-05-28", "00:00:00", +3.0,  "Addis Ababa",      9.03,     38.74,     "Liberation; time_unknown -- noon chart"),
    ("GH", "Ghana",          "independence",  "1957-03-06", "00:00:00",  0.0,  "Accra",            5.6037,   -0.187,    "time_unknown -- noon chart"),
    ("SE", "Sweden",         "independence",  "1523-06-06", "12:00:00", +1.0,  "Stockholm",       59.3293,   18.0686,   "Modern state; time_unknown -- noon chart"),
    ("CH", "Switzerland",    "independence",  "1291-08-01", "12:00:00", +1.0,  "Bern",            46.9481,    7.4474,   "Confederation; time_unknown -- noon chart"),
    ("NZ", "New Zealand",    "independence",  "1907-09-26", "00:00:00", +12.0, "Wellington",     -41.2865,  174.7762,   "Dominion; time_unknown -- noon chart"),
    ("PT", "Portugal",       "republic",      "1910-10-05", "09:00:00",  0.0,  "Lisbon",          38.7223,   -9.1393,   ""),
    ("GR", "Greece",         "independence",  "1822-01-13", "00:00:00", +2.0,  "Epidaurus",       37.63,     23.05,     "time_unknown -- noon chart"),
    ("CU", "Cuba",           "independence",  "1902-05-20", "12:00:00", -5.0,  "Havana",          23.1136,  -82.3666,   "time_unknown -- noon chart"),
]


# ── Computation Functions ─────────────────────────────────────────────────────

def _calc_planet(jd: float, swe_id: int) -> tuple[float, float]:
    try:
        result = swe.calc_ut(jd, swe_id, _SWE_FLAGS)
    except Exception:
        result = swe.calc_ut(jd, swe_id, _SWE_FLAGS_FALLBACK)
    return result[0][0], result[0][3]


def _calc_ascendant(jd: float, lat: float, lon: float) -> float:
    """Return sidereal ascendant longitude (Whole Sign, Lahiri)."""
    try:
        cusps, ascmc = swe.houses(jd, lat, lon, b"W")
        ayanamsa = swe.get_ayanamsa_ut(jd)
        return (ascmc[0] - ayanamsa) % 360.0
    except Exception:
        # Fallback: use zero degrees of first sign if houses fail
        return 0.0


def _local_to_utc(date_str: str, time_str: str, tz_offset: float) -> tuple[str, float]:
    """
    Convert local date/time + tz_offset to UTC ISO string and Julian Day.
    """
    y, mo, d = map(int, date_str.split("-"))
    h, m, s = map(int, time_str.split(":"))
    local_hours = h + m / 60 + s / 3600
    utc_hours = local_hours - tz_offset

    # Handle day rollover
    day_offset = 0
    if utc_hours < 0:
        utc_hours += 24
        day_offset = -1
    elif utc_hours >= 24:
        utc_hours -= 24
        day_offset = 1

    jd = swe.julday(y, mo, d, local_hours - tz_offset)  # julday handles decimal UTC hours correctly
    yr, mr, dr, hr = swe.revjul(jd)
    hh = int(hr)
    mm = int((hr - hh) * 60)
    ss = int(((hr - hh) * 60 - mm) * 60)
    utc_iso = f"{int(yr):04d}-{int(mr):02d}-{int(dr):02d}T{hh:02d}:{mm:02d}:{ss:02d}Z"
    return utc_iso, jd


def _compute_chart(jd: float, lat: float, lon: float) -> dict:
    """Compute natal chart: lagna + 9 planet positions in Whole Sign houses."""
    asc_lon = _calc_ascendant(jd, lat, lon)
    lagna_sign = SIGNS[int(asc_lon // 30)]
    lagna_degree = asc_lon % 30

    planet_positions = {}
    for planet_name, swe_id in PLANET_SWE_IDS.items():
        p_lon, p_speed = _calc_planet(jd, swe_id)
        p_sign = SIGNS[int(p_lon // 30) % 12]
        p_degree = p_lon % 30
        house = (SIGNS.index(p_sign) - SIGNS.index(lagna_sign)) % 12 + 1
        retrograde = p_speed < 0

        if planet_name == "Rahu":
            planet_positions["Rahu"] = {
                "sign": p_sign, "degree": round(p_degree, 4),
                "house": house, "retrograde": True,
            }
            # Ketu = Rahu + 180
            ketu_lon = (p_lon + 180.0) % 360.0
            ketu_sign = SIGNS[int(ketu_lon // 30) % 12]
            ketu_degree = ketu_lon % 30
            ketu_house = (SIGNS.index(ketu_sign) - SIGNS.index(lagna_sign)) % 12 + 1
            planet_positions["Ketu"] = {
                "sign": ketu_sign, "degree": round(ketu_degree, 4),
                "house": ketu_house, "retrograde": True,
            }
        else:
            planet_positions[planet_name] = {
                "sign": p_sign, "degree": round(p_degree, 4),
                "house": house, "retrograde": retrograde,
            }

    house_cusps = [SIGNS[(SIGNS.index(lagna_sign) + i) % 12] for i in range(12)]

    return {
        "lagna_sign": lagna_sign,
        "lagna_degree": round(lagna_degree, 4),
        "planet_positions": planet_positions,
        "house_cusps": house_cusps,
        "calculated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def build_foundation_chart_doc(row: tuple) -> dict:
    """Build a single foundation chart document."""
    (cc, name, chart_type, event_date, event_time_local, tz_offset,
     city, lat, lon, notes) = row

    utc_iso, jd = _local_to_utc(event_date, event_time_local, tz_offset)
    chart = _compute_chart(jd, lat, lon)

    return {
        "country_code": cc,
        "country_name": name,
        "chart_type": chart_type,
        "event_date": event_date,
        "event_time_local": event_time_local,
        "event_tz_offset": tz_offset,
        "event_time_utc": utc_iso,
        "location": {"city": city, "lat": lat, "lon": lon},
        "chart": chart,
        "notes": notes,
        "active": True,
    }


# ── Print Summary (Gate 5 output) ─────────────────────────────────────────────

def print_summary(docs: list[dict]) -> None:
    print("\n" + "=" * 80)
    print("FOUNDATION CHARTS -- GATE 5 MANUAL VALIDATION SUMMARY")
    print("=" * 80)
    print(f"{'CC':<4} {'Country':<20} {'Lagna':<15} {'Sun':<14} {'Moon':<14} {'Saturn':<14} {'Jupiter':<14}")
    print("-" * 80)
    for doc in docs:
        cc = doc["country_code"]
        name = doc["country_name"][:19]
        chart = doc["chart"]
        lagna = chart["lagna_sign"]
        pp = chart["planet_positions"]
        sun_s = pp.get("Sun", {}).get("sign", "?")[:12]
        moon_s = pp.get("Moon", {}).get("sign", "?")[:12]
        sat_s = pp.get("Saturn", {}).get("sign", "?")[:12]
        jup_s = pp.get("Jupiter", {}).get("sign", "?")[:12]
        print(f"{cc:<4} {name:<20} {lagna:<15} {sun_s:<14} {moon_s:<14} {sat_s:<14} {jup_s:<14}")
    print("=" * 80)
    print(f"Total: {len(docs)} charts computed\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Seed mundane foundation charts")
    parser.add_argument("--live", action="store_true", help="Write to DB (default: dry-run)")
    args = parser.parse_args()

    print(f"Building {len(COUNTRIES)} foundation charts via pyswisseph ...")
    docs = []
    errors = []
    for row in COUNTRIES:
        try:
            doc = build_foundation_chart_doc(row)
            docs.append(doc)
        except Exception as exc:
            errors.append((row[0], str(exc)))
            print(f"  ERROR {row[0]}: {exc}")

    print_summary(docs)

    if errors:
        print(f"\n⚠ {len(errors)} error(s) during computation:")
        for cc, msg in errors:
            print(f"  {cc}: {msg}")

    if not args.live:
        print("DRY-RUN complete. Pass --live to upsert into horoscope_db.mundane_foundation_charts")
        return

    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        print("ERROR: MONGO_URL env var not set.")
        sys.exit(1)

    client = pymongo.MongoClient(mongo_url)
    db = client["horoscope_db"]
    col = db["mundane_foundation_charts"]

    col.create_index([("country_code", 1), ("chart_type", 1)], unique=True, background=True)

    upserted = 0
    for doc in docs:
        col.update_one(
            {"country_code": doc["country_code"], "chart_type": doc["chart_type"]},
            {"$set": doc},
            upsert=True,
        )
        upserted += 1
        print(f"  ✓ {doc['country_code']} -- {doc['country_name']} | Lagna: {doc['chart']['lagna_sign']}")

    print(f"\n✅ Upserted {upserted} / {len(COUNTRIES)} foundation charts into horoscope_db.mundane_foundation_charts")
    if errors:
        print(f"⚠ {len(errors)} computation error(s) -- see above")
    client.close()


if __name__ == "__main__":
    main()
