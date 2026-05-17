from __future__ import annotations

"""
EverydayHoroscope -- Vedic Calculation Engine
Proprietary IP of SkyHound Studios
Powered by Swiss Ephemeris

Architecture:
  Layer 1 (this file): Mathematical calculation -- deterministic, always same result
  Layer 2 (Claude prompts): Interpretation -- human-readable insights from calculated positions
"""

import math
from datetime import datetime, timedelta, timezone
import logging
import swisseph as swe

try:
    from geopy.geocoders import Nominatim
except ImportError:
    Nominatim = None


class const:
    SUN = "SUN"
    MOON = "MOON"
    MERCURY = "MERCURY"
    VENUS = "VENUS"
    MARS = "MARS"
    JUPITER = "JUPITER"
    SATURN = "SATURN"
    NORTH_NODE = "NORTH_NODE"
    SOUTH_NODE = "SOUTH_NODE"
    ASC = "ASC"
    RETROGRADE = "Retrograde"

PLANET_IDS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.NORTH_NODE, const.SOUTH_NODE
]

PLANET_SWE_IDS = {
    const.SUN: swe.SUN,
    const.MOON: swe.MOON,
    const.MERCURY: swe.MERCURY,
    const.VENUS: swe.VENUS,
    const.MARS: swe.MARS,
    const.JUPITER: swe.JUPITER,
    const.SATURN: swe.SATURN,
    const.NORTH_NODE: swe.MEAN_NODE,
}

PLANET_NAMES = {
    const.SUN: 'Sun (Surya)',
    const.MOON: 'Moon (Chandra)',
    const.MERCURY: 'Mercury (Budha)',
    const.VENUS: 'Venus (Shukra)',
    const.MARS: 'Mars (Mangal)',
    const.JUPITER: 'Jupiter (Brihaspati)',
    const.SATURN: 'Saturn (Shani)',
    const.NORTH_NODE: 'Rahu',
    const.SOUTH_NODE: 'Ketu',
}

SIGN_NAMES = {
    'Aries': 'Aries (Mesha)', 'Taurus': 'Taurus (Vrishabha)',
    'Gemini': 'Gemini (Mithuna)', 'Cancer': 'Cancer (Karka)',
    'Leo': 'Leo (Simha)', 'Virgo': 'Virgo (Kanya)',
    'Libra': 'Libra (Tula)', 'Scorpio': 'Scorpio (Vrishchika)',
    'Sagittarius': 'Sagittarius (Dhanu)', 'Capricorn': 'Capricorn (Makara)',
    'Aquarius': 'Aquarius (Kumbha)', 'Pisces': 'Pisces (Meena)',
}

SIGN_ORDER = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

SIGN_LORDS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury',
    'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury',
    'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter',
    'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter',
}

SIGN_ELEMENTS = {
    'Aries': 'Fire', 'Leo': 'Fire', 'Sagittarius': 'Fire',
    'Taurus': 'Earth', 'Virgo': 'Earth', 'Capricorn': 'Earth',
    'Gemini': 'Air', 'Libra': 'Air', 'Aquarius': 'Air',
    'Cancer': 'Water', 'Scorpio': 'Water', 'Pisces': 'Water',
}

# ── Planetary dignity tables ──────────────────────────────────────────────────

# Exaltation: sign + degree of maximum exaltation
EXALTATION_DATA = {
    'Sun':     ('Aries',       10),
    'Moon':    ('Taurus',       3),
    'Mars':    ('Capricorn',   28),
    'Mercury': ('Virgo',       15),
    'Jupiter': ('Cancer',       5),
    'Venus':   ('Pisces',      27),
    'Saturn':  ('Libra',       20),
}

# Debilitation sign = 7th from exaltation (opposite)
DEBILITATION_SIGNS = {
    planet: SIGN_ORDER[(SIGN_ORDER.index(sign) + 6) % 12]
    for planet, (sign, _) in EXALTATION_DATA.items()
}

# Moolatrikona: sign, start degree, end degree
MOOLATRIKONA_DATA = {
    'Sun':     ('Leo',          0, 20),
    'Moon':    ('Taurus',       3, 30),
    'Mars':    ('Aries',        0, 12),
    'Mercury': ('Virgo',       16, 20),
    'Jupiter': ('Sagittarius',  0, 10),
    'Venus':   ('Libra',        0, 15),
    'Saturn':  ('Aquarius',     0, 20),
}

# Own signs per planet (Moolatrikona sign always included)
OWN_SIGNS = {
    'Sun':     ['Leo'],
    'Moon':    ['Cancer'],
    'Mars':    ['Aries', 'Scorpio'],
    'Mercury': ['Gemini', 'Virgo'],
    'Jupiter': ['Sagittarius', 'Pisces'],
    'Venus':   ['Taurus', 'Libra'],
    'Saturn':  ['Capricorn', 'Aquarius'],
}

# Parashari natural friendship
_FRIENDS = {
    'Sun':     ['Moon', 'Mars', 'Jupiter'],
    'Moon':    ['Sun', 'Mercury'],
    'Mars':    ['Sun', 'Moon', 'Jupiter'],
    'Mercury': ['Sun', 'Venus'],
    'Jupiter': ['Sun', 'Moon', 'Mars'],
    'Venus':   ['Mercury', 'Saturn'],
    'Saturn':  ['Mercury', 'Venus'],
}
_ENEMIES = {
    'Sun':     ['Venus', 'Saturn'],
    'Moon':    [],
    'Mars':    ['Mercury'],
    'Mercury': ['Moon'],
    'Jupiter': ['Mercury', 'Venus'],
    'Venus':   ['Sun', 'Moon'],
    'Saturn':  ['Sun', 'Moon', 'Mars'],
}

# Combustion orbs in degrees (Parashari -- direct motion)
COMBUSTION_ORBS = {
    'Moon':    12,
    'Mars':    17,
    'Mercury': 14,
    'Jupiter': 11,
    'Venus':   10,
    'Saturn':  15,
}


def get_planet_dignity(planet: str, sign: str, degree: float) -> str:
    """Return Parashari dignity: exalted / moolatrikona / own_sign /
    friendly / neutral / enemy / debilitated.
    Nodes and unrecognised planets return 'neutral'."""
    if planet not in EXALTATION_DATA:
        return 'neutral'
    # Exaltation
    if sign == EXALTATION_DATA[planet][0]:
        return 'exalted'
    # Debilitation
    if sign == DEBILITATION_SIGNS[planet]:
        return 'debilitated'
    # Moolatrikona
    mt_sign, mt_start, mt_end = MOOLATRIKONA_DATA[planet]
    if sign == mt_sign and mt_start <= degree <= mt_end:
        return 'moolatrikona'
    # Own sign (non-Moolatrikona portion)
    if sign in OWN_SIGNS.get(planet, []):
        return 'own_sign'
    # Friendship with sign lord
    sign_lord = SIGN_LORDS.get(sign, '')
    if sign_lord in _FRIENDS.get(planet, []):
        return 'friendly'
    if sign_lord in _ENEMIES.get(planet, []):
        return 'enemy'
    return 'neutral'


def is_planet_combust(planet: str, planet_lon: float, sun_lon: float) -> bool:
    """True when planet is within its combustion orb of the Sun.
    Sun, Rahu, and Ketu are never combust."""
    if planet not in COMBUSTION_ORBS:
        return False
    orb = COMBUSTION_ORBS[planet]
    diff = abs(planet_lon - sun_lon) % 360
    if diff > 180:
        diff = 360 - diff
    return diff <= orb

HOUSE_NAMES = {
    1: 'Lagna (Self, Personality, Body)',
    2: 'Dhana (Wealth, Family, Speech)',
    3: 'Sahaja (Siblings, Courage, Communication)',
    4: 'Sukha (Home, Mother, Happiness)',
    5: 'Putra (Children, Intelligence, Past Life Merits)',
    6: 'Ripu (Enemies, Disease, Debt)',
    7: 'Kalatra (Spouse, Partnerships, Business)',
    8: 'Mrityu (Longevity, Transformation, Hidden Matters)',
    9: 'Dharma (Luck, Father, Higher Learning)',
    10: 'Karma (Career, Status, Authority)',
    11: 'Labha (Gains, Friends, Aspirations)',
    12: 'Vyaya (Losses, Moksha, Foreign Lands)',
}

# ─── Nakshatra Data ───────────────────────────────────────────────────────────

NAKSHATRAS = [
    {'name': 'Ashwini', 'lord': 'Ketu', 'dasha_years': 7},
    {'name': 'Bharani', 'lord': 'Venus', 'dasha_years': 20},
    {'name': 'Krittika', 'lord': 'Sun', 'dasha_years': 6},
    {'name': 'Rohini', 'lord': 'Moon', 'dasha_years': 10},
    {'name': 'Mrigashira', 'lord': 'Mars', 'dasha_years': 7},
    {'name': 'Ardra', 'lord': 'Rahu', 'dasha_years': 18},
    {'name': 'Punarvasu', 'lord': 'Jupiter', 'dasha_years': 16},
    {'name': 'Pushya', 'lord': 'Saturn', 'dasha_years': 19},
    {'name': 'Ashlesha', 'lord': 'Mercury', 'dasha_years': 17},
    {'name': 'Magha', 'lord': 'Ketu', 'dasha_years': 7},
    {'name': 'Purva Phalguni', 'lord': 'Venus', 'dasha_years': 20},
    {'name': 'Uttara Phalguni', 'lord': 'Sun', 'dasha_years': 6},
    {'name': 'Hasta', 'lord': 'Moon', 'dasha_years': 10},
    {'name': 'Chitra', 'lord': 'Mars', 'dasha_years': 7},
    {'name': 'Swati', 'lord': 'Rahu', 'dasha_years': 18},
    {'name': 'Vishakha', 'lord': 'Jupiter', 'dasha_years': 16},
    {'name': 'Anuradha', 'lord': 'Saturn', 'dasha_years': 19},
    {'name': 'Jyeshtha', 'lord': 'Mercury', 'dasha_years': 17},
    {'name': 'Mula', 'lord': 'Ketu', 'dasha_years': 7},
    {'name': 'Purva Ashadha', 'lord': 'Venus', 'dasha_years': 20},
    {'name': 'Uttara Ashadha', 'lord': 'Sun', 'dasha_years': 6},
    {'name': 'Shravana', 'lord': 'Moon', 'dasha_years': 10},
    {'name': 'Dhanishtha', 'lord': 'Mars', 'dasha_years': 7},
    {'name': 'Shatabhisha', 'lord': 'Rahu', 'dasha_years': 18},
    {'name': 'Purva Bhadrapada', 'lord': 'Jupiter', 'dasha_years': 16},
    {'name': 'Uttara Bhadrapada', 'lord': 'Saturn', 'dasha_years': 19},
    {'name': 'Revati', 'lord': 'Mercury', 'dasha_years': 17},
]

DASHA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
DASHA_YEARS = {'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17}

# ─── Ashtakoot Data ───────────────────────────────────────────────────────────

VARNA = {'Aries': 2, 'Taurus': 3, 'Gemini': 4, 'Cancer': 1, 'Leo': 2, 'Virgo': 3, 'Libra': 4, 'Scorpio': 1, 'Sagittarius': 2, 'Capricorn': 3, 'Aquarius': 4, 'Pisces': 1}

YONI = {
    'Ashwini': ('Horse', 'M'), 'Shatabhisha': ('Horse', 'F'),
    'Bharani': ('Elephant', 'M'), 'Revati': ('Elephant', 'F'),
    'Pushya': ('Goat', 'M'), 'Krittika': ('Goat', 'F'),
    'Rohini': ('Serpent', 'M'), 'Mrigashira': ('Serpent', 'F'),
    'Mula': ('Dog', 'M'), 'Ardra': ('Dog', 'F'),
    'Ashlesha': ('Cat', 'M'), 'Punarvasu': ('Cat', 'F'),
    'Magha': ('Rat', 'M'), 'Purva Phalguni': ('Rat', 'F'),
    'Uttara Phalguni': ('Cow', 'F'), 'Uttara Bhadrapada': ('Cow', 'M'),
    'Hasta': ('Buffalo', 'F'), 'Swati': ('Buffalo', 'M'),
    'Vishakha': ('Tiger', 'M'), 'Chitra': ('Tiger', 'F'),
    'Jyeshtha': ('Deer', 'M'), 'Anuradha': ('Deer', 'F'),
    'Purva Ashadha': ('Monkey', 'F'), 'Shravana': ('Monkey', 'M'),
    'Uttara Ashadha': ('Mongoose', 'M'),
    'Dhanishtha': ('Lion', 'F'), 'Purva Bhadrapada': ('Lion', 'M'),
}

GANA = {
    'Ashwini': 'Deva', 'Mrigashira': 'Deva', 'Punarvasu': 'Deva', 'Pushya': 'Deva',
    'Hasta': 'Deva', 'Swati': 'Deva', 'Anuradha': 'Deva', 'Shravana': 'Deva', 'Revati': 'Deva',
    'Bharani': 'Manushya', 'Rohini': 'Manushya', 'Ardra': 'Manushya', 'Purva Phalguni': 'Manushya',
    'Uttara Phalguni': 'Manushya', 'Purva Ashadha': 'Manushya', 'Uttara Ashadha': 'Manushya',
    'Purva Bhadrapada': 'Manushya', 'Uttara Bhadrapada': 'Manushya',
    'Krittika': 'Rakshasa', 'Ashlesha': 'Rakshasa', 'Magha': 'Rakshasa', 'Chitra': 'Manushya',
    'Vishakha': 'Rakshasa', 'Jyeshtha': 'Rakshasa', 'Mula': 'Rakshasa', 'Dhanishtha': 'Rakshasa',
    'Shatabhisha': 'Rakshasa',
}

NADI = {
    'Ashwini': 'Vata', 'Ardra': 'Vata', 'Punarvasu': 'Vata', 'Uttara Phalguni': 'Vata',
    'Hasta': 'Vata', 'Jyeshtha': 'Vata', 'Mula': 'Vata', 'Shatabhisha': 'Vata', 'Purva Bhadrapada': 'Vata',
    'Bharani': 'Pitta', 'Mrigashira': 'Pitta', 'Pushya': 'Pitta', 'Purva Phalguni': 'Pitta',
    'Chitra': 'Pitta', 'Vishakha': 'Pitta', 'Purva Ashadha': 'Pitta', 'Dhanishtha': 'Pitta', 'Uttara Bhadrapada': 'Pitta',
    'Krittika': 'Kapha', 'Rohini': 'Kapha', 'Ashlesha': 'Kapha', 'Magha': 'Kapha',
    'Swati': 'Kapha', 'Anuradha': 'Kapha', 'Uttara Ashadha': 'Kapha', 'Shravana': 'Kapha', 'Revati': 'Kapha',
}

# ─── Swiss Ephemeris Helpers ──────────────────────────────────────────────────

def _setup_swe():
    """Configure Swiss Ephemeris for Lahiri ayanamsha (Vedic)."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)

_setup_swe()

SWE_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

MEAN_DAILY_MOTION = {
    'Sun': 0.9856,
    'Moon': 13.1764,
    'Mars': 0.5240,
    'Mercury': 1.3833,
    'Jupiter': 0.0831,
    'Venus': 1.2000,
    'Saturn': 0.0334,
}

NAISARGIKA_BALA = {
    'Sun': 60.0,
    'Moon': 51.43,
    'Venus': 42.86,
    'Jupiter': 34.29,
    'Mercury': 25.71,
    'Mars': 17.14,
    'Saturn': 8.57,
}

MINIMUM_RUPAS = {
    'Sun': 6.5,
    'Moon': 6.0,
    'Mars': 5.0,
    'Mercury': 7.0,
    'Jupiter': 6.5,
    'Venus': 5.5,
    'Saturn': 5.0,
}

DIG_BALA_HOUSE = {
    'Sun': 10,
    'Mars': 10,
    'Mercury': 1,
    'Jupiter': 1,
    'Moon': 4,
    'Venus': 4,
    'Saturn': 7,
}

CLASSICAL_PLANETS = ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn')
WEEKDAY_LORDS = ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn')
CHALDEAN_SEQUENCE = ('Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars')
DAY_PLANETS = {'Sun', 'Jupiter', 'Venus'}
NIGHT_PLANETS = {'Moon', 'Mars', 'Saturn'}
ODD_SIGN_PLANETS = {'Sun', 'Jupiter', 'Mars'}
EVEN_SIGN_PLANETS = {'Moon', 'Venus'}
KENDRA_HOUSES = {1, 4, 7, 10}
SUCCEDENT_HOUSES = {2, 5, 8, 11}
PARTIAL_ASPECT_HOUSES = {3, 4, 5, 8, 9, 10}


def _parse_datetime_to_jd(date_of_birth: str, time_of_birth: str, timezone_offset: str) -> float:
    """Convert birth date/time/timezone to Julian Day number (UT)."""
    dt = datetime.strptime(f"{date_of_birth} {time_of_birth}", "%Y-%m-%d %H:%M")
    # Parse timezone offset like '+05:30' or '-04:00'
    sign = 1 if timezone_offset[0] != '-' else -1
    parts = timezone_offset.lstrip('+-').split(':')
    tz_hours = sign * (int(parts[0]) + int(parts[1]) / 60)
    dt_ut = dt - timedelta(hours=tz_hours)
    return swe.julday(dt_ut.year, dt_ut.month, dt_ut.day,
                      dt_ut.hour + dt_ut.minute / 60 + dt_ut.second / 3600)


def _lon_to_sign(lon: float) -> str:
    """Convert ecliptic longitude (0-360) to sign name."""
    return SIGN_ORDER[int(lon // 30) % 12]


def _calc_planet(jd: float, swe_id: int) -> tuple[float, float]:
    """Return (sidereal_longitude, speed_lon) for a planet."""
    result = swe.calc_ut(jd, swe_id, SWE_FLAGS)
    lon = result[0][0]
    speed = result[0][3]
    return lon, speed


def _calc_ascendant(jd: float, lat: float, lon: float) -> float:
    """Return sidereal ascendant longitude."""
    # Whole sign houses -- standard for Vedic
    cusps, ascmc = swe.houses(jd, lat, lon, b'W')
    asc_tropical = ascmc[0]
    ayanamsa = swe.get_ayanamsa_ut(jd)
    return (asc_tropical - ayanamsa) % 360


def _clamp(value: float, lower: float = 0.0, upper: float = 60.0) -> float:
    """Clamp a float into the requested range."""
    return max(lower, min(upper, value))


def _round4(value: float) -> float:
    """Round to four decimals for stable intermediate strength math."""
    return round(value, 4)


def _normalized_longitude(value: float) -> float:
    """Wrap a longitude into the 0-360 range."""
    return value % 360.0


def _absolute_sign_longitude(sign: str, degree: float) -> float:
    """Convert sign + intra-sign degree into absolute sidereal longitude."""
    return _normalized_longitude((SIGN_ORDER.index(sign) * 30.0) + degree)


def _shortest_arc_distance(a: float, b: float) -> float:
    """Return the shortest separation between two longitudes."""
    diff = abs(_normalized_longitude(a) - _normalized_longitude(b)) % 360.0
    return min(diff, 360.0 - diff)


def _is_odd_sign(sign: str) -> bool:
    """True for odd zodiac signs with Aries treated as the first odd sign."""
    return SIGN_ORDER.index(sign) % 2 == 0


def _navamsa_sign(planet_lon: float) -> str:
    """Return the navamsa sign using the commission's simplified D9 formula."""
    sign_index = int(_normalized_longitude(planet_lon) // 30.0)
    navamsa_position = int((planet_lon % 30.0) / (30.0 / 9.0))
    d9_sign_index = (sign_index * 9 + navamsa_position) % 12
    return SIGN_ORDER[d9_sign_index]


def _planet_plain_name(display_name: str) -> str:
    """Strip the Sanskrit suffix from display names like 'Sun (Surya)'."""
    return display_name.split('(')[0].strip()


def _planet_display_name(plain_name: str) -> str:
    """Resolve the app's display key for a plain graha name."""
    for display_name in PLANET_NAMES.values():
        if _planet_plain_name(display_name) == plain_name:
            return display_name
    return plain_name


def _get_planet_payload(planets: dict[str, dict], plain_name: str) -> dict:
    """Fetch a planet payload whether the dict is keyed by plain or display names."""
    if plain_name in planets:
        return planets[plain_name]
    return planets.get(_planet_display_name(plain_name), {})


def _is_moolatrikona_position(planet: str, sign: str, degree: float) -> bool:
    """True when a classical planet is inside its Moolatrikona span."""
    if planet not in MOOLATRIKONA_DATA:
        return False
    mt_sign, mt_start, mt_end = MOOLATRIKONA_DATA[planet]
    return sign == mt_sign and mt_start <= degree <= mt_end


def _solar_day_start_jd(jd: float, lon: float) -> float:
    """Approximate local midnight in UT using geographic longitude."""
    solar_offset = lon / 360.0
    local_jd = jd + solar_offset
    return math.floor(local_jd - 0.5) + 0.5 - solar_offset


def _solar_event_jd(jd_start: float, lat: float, lon: float, rsmi: int) -> float:
    """Get the next sunrise or sunset after the given Julian Day."""
    result = swe.rise_trans(
        jd_start,
        swe.SUN,
        rsmi,
        [lon, lat, 0.0],
        1013.25,
        15.0,
    )
    return result[1][0]


def _day_night_context(jd: float, lat: float, lon: float) -> dict[str, float | bool]:
    """Return sunrise/sunset anchors and whether the birth happened during daytime."""
    day_start = _solar_day_start_jd(jd, lon)
    sunrise_today = _solar_event_jd(day_start, lat, lon, swe.CALC_RISE)
    sunset_today = _solar_event_jd(day_start, lat, lon, swe.CALC_SET)
    sunrise_prev = _solar_event_jd(day_start - 1.0, lat, lon, swe.CALC_RISE)
    sunset_prev = _solar_event_jd(day_start - 1.0, lat, lon, swe.CALC_SET)
    sunrise_next = _solar_event_jd(day_start + 1.0, lat, lon, swe.CALC_RISE)

    is_day = sunrise_today <= jd < sunset_today
    if is_day:
        period_start, period_end = sunrise_today, sunset_today
        hora_anchor = sunrise_today
    elif jd < sunrise_today:
        period_start, period_end = sunset_prev, sunrise_today
        hora_anchor = sunrise_prev
    else:
        period_start, period_end = sunset_today, sunrise_next
        hora_anchor = sunrise_today

    return {
        'is_day': is_day,
        'sunrise_today': sunrise_today,
        'sunset_today': sunset_today,
        'sunrise_prev': sunrise_prev,
        'sunrise_next': sunrise_next,
        'sunset_prev': sunset_prev,
        'period_start': period_start,
        'period_end': period_end,
        'hora_anchor': hora_anchor,
    }


def _weekday_index_from_jd(jd: float, lon: float = 0.0) -> int:
    """Return weekday index where 0=Sunday using local-solar adjustment."""
    local_jd = jd + (lon / 360.0)
    return int(local_jd + 1.5) % 7


def _weekday_lord_from_jd(jd: float, lon: float = 0.0) -> str:
    """Return the weekday lord for the supplied Julian Day."""
    return WEEKDAY_LORDS[_weekday_index_from_jd(jd, lon)]


def _signed_lunar_phase_angle(jd: float) -> float:
    """Return Moon-Sun elongation folded into the [-180, 180) range."""
    sun_lon, _ = _calc_planet(jd, swe.SUN)
    moon_lon, _ = _calc_planet(jd, swe.MOON)
    return ((moon_lon - sun_lon + 180.0) % 360.0) - 180.0


def _refine_zero_crossing(
    low_jd: float,
    high_jd: float,
    value_fn,
    iterations: int = 24,
) -> float:
    """Binary-search a zero crossing between two Julian Day endpoints."""
    low_value = value_fn(low_jd)
    for _ in range(iterations):
        mid_jd = (low_jd + high_jd) / 2.0
        mid_value = value_fn(mid_jd)
        if low_value <= 0.0 < mid_value:
            high_jd = mid_jd
        else:
            low_jd = mid_jd
            low_value = mid_value
    return (low_jd + high_jd) / 2.0


def _find_previous_new_moon_jd(jd: float) -> float:
    """Find the Amavasya immediately preceding the birth Julian Day."""
    probe = jd - 35.0
    step = 0.5
    prev_jd = probe
    prev_value = _signed_lunar_phase_angle(prev_jd)
    current_jd = prev_jd + step
    while current_jd <= jd + step:
        current_value = _signed_lunar_phase_angle(current_jd)
        if prev_value <= 0.0 < current_value:
            crossing = _refine_zero_crossing(prev_jd, current_jd, _signed_lunar_phase_angle)
            if crossing <= jd:
                last_crossing = crossing
        prev_jd = current_jd
        prev_value = current_value
        current_jd += step
    if 'last_crossing' in locals():
        return last_crossing
    return jd - 29.5


def _find_previous_mesha_sankranti_jd(jd: float) -> float:
    """Find the last sidereal Aries ingress of the Sun prior to birth."""
    probe = jd - 400.0
    step = 1.0
    prev_jd = probe
    prev_lon, _ = _calc_planet(prev_jd, swe.SUN)
    current_jd = prev_jd + step
    while current_jd <= jd + step:
        current_lon, _ = _calc_planet(current_jd, swe.SUN)
        if current_lon < prev_lon:
            low_jd = prev_jd
            high_jd = current_jd
            for _ in range(24):
                mid_jd = (low_jd + high_jd) / 2.0
                mid_lon, _ = _calc_planet(mid_jd, swe.SUN)
                if mid_lon > 300.0:
                    low_jd = mid_jd
                else:
                    high_jd = mid_jd
            candidate = (low_jd + high_jd) / 2.0
            if candidate <= jd:
                last_ingress = candidate
        prev_jd = current_jd
        prev_lon = current_lon
        current_jd += step
    if 'last_ingress' in locals():
        return last_ingress
    return jd - 365.25


def _planet_declination(jd: float, swe_id: int) -> float:
    """Return a planet's geocentric declination in degrees."""
    result = swe.calc_ut(jd, swe_id, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)
    return result[0][1]


def _hora_lord(jd: float, lon: float, context: dict[str, float | bool]) -> str:
    """Return the hora lord using sunrise as the daily sequence anchor."""
    sunrise_anchor = float(context['hora_anchor'])
    day_lord = _weekday_lord_from_jd(sunrise_anchor, lon)
    sequence_index = CHALDEAN_SEQUENCE.index(day_lord)
    elapsed_hours = max(0, int((jd - sunrise_anchor) * 24.0))
    return CHALDEAN_SEQUENCE[(sequence_index + elapsed_hours) % len(CHALDEAN_SEQUENCE)]


def _aspect_distance(from_house: int, to_house: int) -> int:
    """Return Parashari aspect distance counting from source house."""
    return ((to_house - from_house) % 12) + 1


def _aspect_strength_factor(aspecting_planet: str, from_house: int, to_house: int) -> float:
    """Return 1.0 for a full aspect, 0.5 for a simplified partial, else 0."""
    distance = _aspect_distance(from_house, to_house)
    full_aspects = {7}
    if aspecting_planet == 'Mars':
        full_aspects |= {4, 8}
    elif aspecting_planet == 'Jupiter':
        full_aspects |= {5, 9}
    elif aspecting_planet == 'Saturn':
        full_aspects |= {3, 10}
    if distance in full_aspects:
        return 1.0
    if distance in PARTIAL_ASPECT_HOUSES:
        return 0.5
    return 0.0


def _uchcha_bala(planet: str, longitude: float) -> float:
    """Compute exaltation strength from distance to debilitation."""
    exalted_sign, exalted_degree = EXALTATION_DATA[planet]
    exalted_lon = _absolute_sign_longitude(exalted_sign, exalted_degree)
    debilitation_lon = _normalized_longitude(exalted_lon + 180.0)
    bala = _shortest_arc_distance(longitude, debilitation_lon) / 3.0
    return _round4(_clamp(bala))


def _ojayugma_bala(planet: str, sign: str, longitude: float) -> float:
    """Compute odd/even sign and navamsa bonuses."""
    if planet in {'Mercury', 'Saturn'}:
        return 30.0
    target_odd = planet in ODD_SIGN_PLANETS
    sign_bonus = 15.0 if _is_odd_sign(sign) == target_odd else 0.0
    navamsa_bonus = 15.0 if _is_odd_sign(_navamsa_sign(longitude)) == target_odd else 0.0
    return _round4(sign_bonus + navamsa_bonus)


def _kendradi_bala(house: int) -> float:
    """Compute angular/succedent/cadent positional strength."""
    if house in KENDRA_HOUSES:
        return 60.0
    if house in SUCCEDENT_HOUSES:
        return 30.0
    return 15.0


def _sthana_bala(planet: str, payload: dict, longitude: float) -> float:
    """Aggregate the five positional-strength subcomponents."""
    sign = payload['sign']
    degree = float(payload['degree'])
    components = [
        _uchcha_bala(planet, longitude),
        45.0 if _is_moolatrikona_position(planet, sign, degree) else 0.0,
        30.0 if sign in OWN_SIGNS.get(planet, []) and not _is_moolatrikona_position(planet, sign, degree) else 0.0,
        _ojayugma_bala(planet, sign, longitude),
        _kendradi_bala(int(payload['house'])),
    ]
    return _round4(sum(components))


def _dig_bala(planet: str, house: int) -> float:
    """Compute Dig Bala using the brief's whole-sign approximation."""
    strong_house = DIG_BALA_HOUSE[planet]
    distance = min((house - strong_house) % 12, (strong_house - house) % 12)
    return _round4(_clamp((6 - distance) * 10.0))


def _paksha_bala(planet: str, moon_elongation: float) -> float:
    """Compute waxing/waning phase strength for benefics and malefics."""
    benefics = {'Moon', 'Mercury', 'Jupiter', 'Venus'}
    waxing = moon_elongation <= 180.0
    if waxing:
        base = moon_elongation / 3.0 if planet in benefics else (180.0 - moon_elongation) / 3.0
    else:
        base = (360.0 - moon_elongation) / 3.0 if planet in benefics else (moon_elongation - 180.0) / 3.0
    return _round4(_clamp(base))


def _tribhaga_bala(planet: str, jd: float, context: dict[str, float | bool]) -> float:
    """Compute the three-part day/night segment strength.
    BPHS Ch 27 Sloka 9: Jupiter always receives 60 Virupas.
    Day thirds: Mercury (1st) / Sun (2nd) / Saturn (3rd).
    Night thirds: Moon (1st) / Venus (2nd) / Mars (3rd).
    NOTE: Mercury's 'always 60' applies to Nathonnatha, NOT Tribhaga.
    """
    if planet == 'Jupiter':
        return 60.0
    period_start = float(context['period_start'])
    period_end = float(context['period_end'])
    span = max(period_end - period_start, 1e-9)
    part_index = min(2, int(((jd - period_start) / span) * 3.0))
    if context['is_day']:
        lords = ('Mercury', 'Sun', 'Saturn')
    else:
        lords = ('Moon', 'Venus', 'Mars')
    return 60.0 if planet == lords[part_index] else 0.0


def _ayana_bala(planet: str, jd: float) -> float:
    """Compute solstitial strength using the simplified declination formula."""
    if planet == 'Mercury':
        return 60.0
    declination = _planet_declination(jd, PLANET_SWE_IDS[_planet_constant(planet)])
    direct_bala = _clamp(30.0 + ((declination / 24.0) * 30.0))
    if planet in {'Moon', 'Saturn'}:
        return _round4(_clamp(60.0 - direct_bala))
    return _round4(_clamp(direct_bala))


def _yuddha_bala(_: dict[str, dict]) -> dict[str, float]:
    """Return zeroed planetary-war strength until latitude comparison is added."""
    return {planet: 0.0 for planet in CLASSICAL_PLANETS}


def _chesta_bala(planet: str, payload: dict, speed: float) -> float:
    """Compute motional strength from actual versus mean daily motion."""
    if payload.get('retrograde'):
        return 60.0
    mean_motion = MEAN_DAILY_MOTION[planet]
    bala = (abs(speed) / mean_motion) * 30.0 if mean_motion else 0.0
    return _round4(_clamp(bala))


def _is_waxing_moon(moon_elongation: float) -> bool:
    """True when the Moon is in Shukla Paksha."""
    return moon_elongation <= 180.0


def _is_benefic_aspector(planet: str, moon_elongation: float) -> bool:
    """Return benefic status for Drik Bala using the commission simplification."""
    if planet in {'Jupiter', 'Venus', 'Mercury'}:
        return True
    if planet == 'Moon':
        return _is_waxing_moon(moon_elongation)
    return False


def _drik_bala(planet: str, planets: dict[str, dict], moon_elongation: float) -> float:
    """Compute simplified aspectual strength from benefic and malefic aspects."""
    target_payload = _get_planet_payload(planets, planet)
    target_house = int(target_payload['house'])
    total = 0.0
    contributors = 0
    for aspector in CLASSICAL_PLANETS:
        if aspector == planet:
            continue
        aspector_payload = _get_planet_payload(planets, aspector)
        strength_factor = _aspect_strength_factor(aspector, int(aspector_payload['house']), target_house)
        if strength_factor == 0.0:
            continue
        contributors += 1
        if _is_benefic_aspector(aspector, moon_elongation):
            total += 60.0 if strength_factor == 1.0 else 30.0
        else:
            total -= 30.0 if strength_factor == 1.0 else 15.0
    if contributors == 0:
        return 0.0
    return _round4(_clamp(total / contributors))


def _planet_constant(plain_name: str) -> str:
    """Resolve the internal constant for a classical graha name."""
    for key, display_name in PLANET_NAMES.items():
        if _planet_plain_name(display_name) == plain_name:
            return key
    raise KeyError(f'Unknown planet name: {plain_name}')


def calculate_shadbala(
    planets: dict[str, dict],
    jd: float,
    lat: float,
    lon: float,
) -> dict[str, dict]:
    """Compute Parashari Shadbala totals for the seven classical grahas."""
    context = _day_night_context(jd, lat, lon)
    sun_lon, _ = _calc_planet(jd, swe.SUN)
    moon_lon, _ = _calc_planet(jd, swe.MOON)
    moon_elongation = _normalized_longitude(moon_lon - sun_lon)
    abda_lord = _weekday_lord_from_jd(_find_previous_mesha_sankranti_jd(jd), lon)
    masa_lord = _weekday_lord_from_jd(_find_previous_new_moon_jd(jd), lon)
    vara_lord = _weekday_lord_from_jd(jd, lon)
    hora_lord = _hora_lord(jd, lon, context)
    yuddha_bala = _yuddha_bala(planets)

    positions: dict[str, dict[str, float | dict]] = {}
    for planet in CLASSICAL_PLANETS:
        payload = _get_planet_payload(planets, planet)
        longitude, speed = _calc_planet(jd, PLANET_SWE_IDS[_planet_constant(planet)])
        positions[planet] = {
            'payload': payload,
            'longitude': longitude,
            'speed': speed,
        }

    results: dict[str, dict] = {}
    for planet in CLASSICAL_PLANETS:
        payload = positions[planet]['payload']
        longitude = float(positions[planet]['longitude'])
        speed = float(positions[planet]['speed'])

        nathonnatha = 60.0 if (
            planet == 'Mercury'
            or (context['is_day'] and planet in DAY_PLANETS)
            or ((not context['is_day']) and planet in NIGHT_PLANETS)
        ) else 0.0
        kala_bala = sum([
            nathonnatha,
            _paksha_bala(planet, moon_elongation),
            _tribhaga_bala(planet, jd, context),
            15.0 if planet == abda_lord else 0.0,
            30.0 if planet == masa_lord else 0.0,
            45.0 if planet == vara_lord else 0.0,
            60.0 if planet == hora_lord else 0.0,
            _ayana_bala(planet, jd),
            yuddha_bala[planet],
        ])

        sthana_bala = _sthana_bala(planet, payload, longitude)
        dig_bala = _dig_bala(planet, int(payload['house']))
        chesta_bala = _chesta_bala(planet, payload, speed)
        naisargika_bala = NAISARGIKA_BALA[planet]
        drik_bala = _drik_bala(planet, planets, moon_elongation)
        total = _round4(
            sthana_bala
            + dig_bala
            + kala_bala
            + chesta_bala
            + naisargika_bala
            + drik_bala
        )
        total_rupas = _round4(total / 60.0)
        minimum_rupas = MINIMUM_RUPAS[planet]
        results[planet] = {
            'sthana_bala': _round4(sthana_bala),
            'dig_bala': _round4(dig_bala),
            'kala_bala': _round4(kala_bala),
            'chesta_bala': _round4(chesta_bala),
            'naisargika_bala': _round4(naisargika_bala),
            'drik_bala': _round4(drik_bala),
            'total': total,
            'total_rupas': total_rupas,
            'minimum_rupas': minimum_rupas,
            'is_strong': total_rupas >= minimum_rupas,
        }

    return results


# ─── Core Functions ───────────────────────────────────────────────────────────

def get_nakshatra(moon_longitude: float) -> dict:
    """Get Nakshatra from Moon's sidereal longitude (0-360)."""
    nak_index = int(moon_longitude / (360 / 27))
    pada = int((moon_longitude % (360 / 27)) / (360 / 108)) + 1
    nak = NAKSHATRAS[nak_index]
    return {
        'name': nak['name'],
        'lord': nak['lord'],
        'pada': pada,
        'dasha_years': nak['dasha_years'],
        'index': nak_index,
    }


def get_house_number(planet_sign: str, lagna_sign: str) -> int:
    """Calculate house number from planet sign and Lagna sign."""
    lagna_idx = SIGN_ORDER.index(lagna_sign)
    planet_idx = SIGN_ORDER.index(planet_sign)
    return ((planet_idx - lagna_idx) % 12) + 1


def calculate_vimshottari_dasha(birth_date: str, moon_longitude: float) -> list:
    """Calculate Vimshottari Dasha periods."""
    nak_data = get_nakshatra(moon_longitude)
    nak_lord = nak_data['lord']
    nak_index = nak_data['index']

    nak_span = 360 / 27
    nak_start = nak_index * nak_span
    fraction_elapsed = (moon_longitude - nak_start) / nak_span
    dasha_years_total = DASHA_YEARS[nak_lord]
    years_elapsed = fraction_elapsed * dasha_years_total
    years_remaining = dasha_years_total - years_elapsed

    bd = datetime.strptime(birth_date, '%Y-%m-%d')
    dashas = []
    lord_idx = DASHA_ORDER.index(nak_lord)

    first_end = bd + timedelta(days=years_remaining * 365.25)
    dashas.append({
        'planet': nak_lord,
        'start': bd.strftime('%Y-%m-%d'),
        'end': first_end.strftime('%Y-%m-%d'),
        'years': round(years_remaining, 1),
    })

    current = first_end
    for i in range(1, 9):
        lord = DASHA_ORDER[(lord_idx + i) % 9]
        years = DASHA_YEARS[lord]
        end = current + timedelta(days=years * 365.25)
        dashas.append({
            'planet': lord,
            'start': current.strftime('%Y-%m-%d'),
            'end': end.strftime('%Y-%m-%d'),
            'years': years,
        })
        current = end

    return dashas


def build_dasha_timeline(birth_date: str, moon_longitude: float) -> list[dict]:
    """
    Returns the authoritative Vimshottari dasha timeline with antardasha sub-periods.
    This is the single source of truth for dasha + antardasha data.
    """
    top_level = calculate_vimshottari_dasha(birth_date, moon_longitude)
    timeline: list[dict] = []
    for maha in top_level:
        maha_planet = str(maha["planet"])
        maha_start = datetime.strptime(maha["start"], "%Y-%m-%d")
        maha_end = datetime.strptime(maha["end"], "%Y-%m-%d")
        maha_total_days = max(1, (maha_end - maha_start).days)
        maha_years = DASHA_YEARS[maha_planet]

        lord_idx = DASHA_ORDER.index(maha_planet)
        antardashas: list[dict] = []
        cursor = maha_start
        for i in range(9):
            antar_lord = DASHA_ORDER[(lord_idx + i) % 9]
            antar_years = DASHA_YEARS[antar_lord]
            antar_fraction = antar_years / maha_years
            antar_days = max(1, int(maha_total_days * antar_fraction))
            antar_end = cursor + timedelta(days=antar_days)
            if antar_end > maha_end:
                antar_end = maha_end
            antardashas.append(
                {
                    "planet": antar_lord,
                    "start": cursor.strftime("%Y-%m-%d"),
                    "end": antar_end.strftime("%Y-%m-%d"),
                }
            )
            cursor = antar_end
        if antardashas:
            antardashas[-1]["end"] = maha["end"]

        timeline.append(
            {
                "planet": maha_planet,
                "start": maha["start"],
                "end": maha["end"],
                "years": maha["years"],
                "antardashas": antardashas,
            }
        )
    return timeline


def get_current_dasha(dashas: list) -> dict:
    """Find the currently active Mahadasha."""
    today = datetime.now()
    for d in dashas:
        start = datetime.strptime(d['start'], '%Y-%m-%d')
        end = datetime.strptime(d['end'], '%Y-%m-%d')
        if start <= today <= end:
            return d
    return dashas[-1]


def check_mangal_dosha(mars_house: int) -> dict:
    """Check Mangal Dosha based on Mars house position."""
    dosha_houses = [1, 2, 4, 7, 8, 12]
    present = mars_house in dosha_houses
    severity_map = {1: 'High', 2: 'Moderate', 4: 'Moderate', 7: 'High', 8: 'Very High', 12: 'Low'}
    severity = severity_map.get(mars_house, None) if present else None
    return {
        'has_dosha': present,
        'present': present,
        'mars_house': mars_house,
        'severity': severity,
        'description': f'Mars in House {mars_house} -- ' + (f'{severity} Mangal Dosha' if present else 'No Mangal Dosha'),
        'cancellation_rules': [],
        'cancelled': False,
        'cancellation_reason': '',
        'note': f'Mars in house {mars_house}' + (' -- Mangal Dosha present' if present else ' -- No Mangal Dosha'),
    }


# ─── Ashtakoot Milan ─────────────────────────────────────────────────────────

def calculate_ashtakoot(nak1: str, sign1: str, nak2: str, sign2: str) -> dict:
    """Calculate full Ashtakoot Guna Milan score."""
    scores = {}

    v1, v2 = VARNA.get(sign1, 2), VARNA.get(sign2, 2)
    scores['varna'] = {'max': 1, 'score': 1 if v2 >= v1 else 0, 'label': 'Compatible' if v2 >= v1 else 'Challenging', 'meaning': 'Spiritual evolution compatibility'}

    vashya_map = {
        'Aries': ['Leo', 'Scorpio'], 'Taurus': ['Cancer', 'Libra'],
        'Gemini': ['Virgo'], 'Cancer': ['Scorpio', 'Sagittarius'],
        'Leo': ['Libra'], 'Virgo': ['Gemini', 'Pisces'],
        'Libra': ['Capricorn'], 'Scorpio': ['Cancer'],
        'Sagittarius': ['Pisces'], 'Capricorn': ['Aries', 'Aquarius'],
        'Aquarius': ['Aries'], 'Pisces': ['Capricorn'],
    }
    mutual = sign2 in vashya_map.get(sign1, []) and sign1 in vashya_map.get(sign2, [])
    one_way = sign2 in vashya_map.get(sign1, []) or sign1 in vashya_map.get(sign2, [])
    vashya_score = 2 if mutual else (0.5 if one_way else 0)
    scores['vashya'] = {'max': 2, 'score': vashya_score, 'label': 'Strong' if vashya_score == 2 else ('Moderate' if vashya_score else 'Weak'), 'meaning': 'Mutual attraction and influence'}

    nak_list = [n['name'] for n in NAKSHATRAS]
    idx1 = nak_list.index(nak1) if nak1 in nak_list else 0
    idx2 = nak_list.index(nak2) if nak2 in nak_list else 0
    tara_from_1 = ((idx2 - idx1) % 27) % 9
    tara_from_2 = ((idx1 - idx2) % 27) % 9
    good_taras = [1, 3, 5, 7]
    tara_score = min(3, int((1.5 if tara_from_1 in good_taras else 0) + (1.5 if tara_from_2 in good_taras else 0)))
    scores['tara'] = {'max': 3, 'score': tara_score, 'label': 'Excellent' if tara_score == 3 else ('Good' if tara_score >= 2 else 'Challenging'), 'meaning': 'Health and longevity compatibility'}

    y1 = YONI.get(nak1, ('Unknown', 'M'))
    y2 = YONI.get(nak2, ('Unknown', 'F'))
    if y1[0] == y2[0]:
        yoni_score = 4
    else:
        friendly_pairs = [('Horse', 'Elephant'), ('Goat', 'Dog'), ('Cat', 'Rat'), ('Cow', 'Tiger'), ('Buffalo', 'Monkey'), ('Lion', 'Deer')]
        enemy_pairs = [('Horse', 'Buffalo'), ('Elephant', 'Lion'), ('Goat', 'Monkey')]
        pair = tuple(sorted([y1[0], y2[0]]))
        if any(tuple(sorted(p)) == pair for p in friendly_pairs): yoni_score = 3
        elif any(tuple(sorted(p)) == pair for p in enemy_pairs): yoni_score = 0
        else: yoni_score = 2
    scores['yoni'] = {'max': 4, 'score': yoni_score, 'label': 'Excellent' if yoni_score == 4 else ('Good' if yoni_score == 3 else ('Moderate' if yoni_score == 2 else 'Challenging')), 'meaning': 'Physical and intimate compatibility'}

    lord1, lord2 = SIGN_LORDS.get(sign1, 'Mercury'), SIGN_LORDS.get(sign2, 'Venus')
    friends = {'Sun': ['Moon', 'Mars', 'Jupiter'], 'Moon': ['Sun', 'Mercury'], 'Mars': ['Sun', 'Moon', 'Jupiter'], 'Mercury': ['Sun', 'Venus'], 'Jupiter': ['Sun', 'Moon', 'Mars'], 'Venus': ['Mercury', 'Saturn'], 'Saturn': ['Mercury', 'Venus']}
    neutrals = {'Sun': ['Mercury'], 'Moon': ['Mars', 'Jupiter', 'Venus', 'Saturn'], 'Mars': ['Venus', 'Saturn'], 'Mercury': ['Mars', 'Jupiter', 'Saturn'], 'Jupiter': ['Venus', 'Saturn'], 'Venus': ['Sun', 'Moon', 'Mars', 'Jupiter'], 'Saturn': ['Sun', 'Moon', 'Jupiter']}
    l1f, l2f = friends.get(lord1, []), friends.get(lord2, [])
    l1n, l2n = neutrals.get(lord1, []), neutrals.get(lord2, [])
    if lord1 == lord2 or (lord2 in l1f and lord1 in l2f): gm_score = 5
    elif (lord2 in l1f and lord1 in l2n) or (lord1 in l2f and lord2 in l1n): gm_score = 4
    elif lord2 in l1n and lord1 in l2n: gm_score = 3
    elif (lord2 in l1f and lord1 not in l2f and lord1 not in l2n) or (lord1 in l2f and lord2 not in l1f and lord2 not in l1n): gm_score = 0.5
    else: gm_score = 0
    scores['graha_maitri'] = {'max': 5, 'score': gm_score, 'label': 'Excellent' if gm_score >= 5 else ('Good' if gm_score >= 4 else ('Moderate' if gm_score >= 3 else 'Challenging')), 'meaning': 'Mental and intellectual compatibility'}

    g1, g2 = GANA.get(nak1, 'Manushya'), GANA.get(nak2, 'Manushya')
    if g1 == g2: gana_score = 6
    elif set([g1, g2]) == {'Deva', 'Manushya'}: gana_score = 5
    elif set([g1, g2]) == {'Manushya', 'Rakshasa'}: gana_score = 1
    else: gana_score = 0
    scores['gana'] = {'max': 6, 'score': gana_score, 'label': 'Perfect' if gana_score == 6 else ('Good' if gana_score >= 5 else ('Moderate' if gana_score == 1 else 'Challenging')), 'meaning': 'Nature and temperament compatibility'}

    sign_idx1, sign_idx2 = SIGN_ORDER.index(sign1), SIGN_ORDER.index(sign2)
    fwd = (sign_idx2 - sign_idx1) % 12 + 1
    rev = (sign_idx1 - sign_idx2) % 12 + 1
    bhakoot_bad = fwd in {2, 6, 8, 12} or rev in {2, 6, 8, 12}
    bhakoot_score = 0 if bhakoot_bad else 7
    scores['bhakoot'] = {'max': 7, 'score': bhakoot_score, 'label': 'Excellent' if bhakoot_score == 7 else 'Challenging', 'meaning': 'Love, family prosperity and longevity'}

    n1, n2 = NADI.get(nak1, 'Vata'), NADI.get(nak2, 'Pitta')
    nadi_score = 0 if n1 == n2 else 8
    scores['nadi'] = {'max': 8, 'score': nadi_score, 'label': 'Excellent' if nadi_score == 8 else 'Nadi Dosha Present', 'meaning': 'Health and progeny compatibility'}

    total = sum(s['score'] for s in scores.values())
    verdict = ('Excellent Match -- Highly Recommended' if total >= 32 else 'Very Good Match' if total >= 24 else 'Good Match -- Recommended with Remedies' if total >= 18 else 'Below Threshold -- Consult Astrologer')

    return {'kootas': scores, 'total_score': total, 'max_score': 36, 'verdict': verdict, 'percentage': round((total / 36) * 100)}


# ─── Main Chart Calculator ────────────────────────────────────────────────────

def calculate_vedic_chart(
    date_of_birth: str,
    time_of_birth: str,
    place_of_birth: str,
    timezone_offset: str = '+05:30'
) -> dict:
    """
    Master function -- calculates complete Vedic birth chart using Swiss Ephemeris.

    Args:
        date_of_birth: 'YYYY-MM-DD'
        time_of_birth: 'HH:MM'
        place_of_birth: 'City, Country' string
        timezone_offset: '+05:30' for IST (default)

    Returns:
        Complete chart data as dict
    """
    try:
        lat, lon = geocode_place(place_of_birth)
        jd = _parse_datetime_to_jd(date_of_birth, time_of_birth, timezone_offset)

        asc_lon = _calc_ascendant(jd, lat, lon)
        lagna_sign = _lon_to_sign(asc_lon)
        lagna_degree = round(asc_lon % 30, 2)

        # Sun longitude computed first -- needed for combustion checks
        sun_lon, _ = _calc_planet(jd, swe.SUN)

        planets = {}
        for pid in PLANET_IDS:
            if pid == const.SOUTH_NODE:
                # South Node = North Node + 180
                north_lon, _ = _calc_planet(jd, swe.MEAN_NODE)
                planet_lon = (north_lon + 180.0) % 360
                speed = 0.0
            else:
                planet_lon, speed = _calc_planet(jd, PLANET_SWE_IDS[pid])

            planet_sign = _lon_to_sign(planet_lon)
            degree_in_sign = planet_lon % 30
            house = get_house_number(planet_sign, lagna_sign)
            # Plain name (without Sanskrit suffix) for dignity/combustion lookups
            plain_name = PLANET_NAMES[pid].split('(')[0].strip()
            planets[PLANET_NAMES[pid]] = {
                'sign': planet_sign,
                'sign_vedic': SIGN_NAMES.get(planet_sign, planet_sign),
                'degree': round(degree_in_sign, 2),
                'house': house,
                'lord_of_sign': SIGN_LORDS.get(planet_sign, ''),
                'retrograde': speed < 0,
                'dignity': get_planet_dignity(plain_name, planet_sign, degree_in_sign),
                'combust': is_planet_combust(plain_name, planet_lon, sun_lon),
            }

        shadbala = calculate_shadbala(planets, jd, lat, lon)
        for planet_name, bala in shadbala.items():
            display_name = _planet_display_name(planet_name)
            if display_name in planets:
                planets[display_name]['shadbala'] = bala

        moon_lon, _ = _calc_planet(jd, swe.MOON)
        nakshatra = get_nakshatra(moon_lon)
        moon_sign = _lon_to_sign(moon_lon)

        houses = {}
        for h in range(1, 13):
            sign_idx = (SIGN_ORDER.index(lagna_sign) + h - 1) % 12
            house_sign = SIGN_ORDER[sign_idx]
            house_lord = SIGN_LORDS[house_sign]
            planets_in_house = [name for name, data in planets.items() if data['house'] == h]
            houses[h] = {
                'house': h,
                'name': HOUSE_NAMES[h],
                'sign': house_sign,
                'sign_vedic': SIGN_NAMES.get(house_sign, house_sign),
                'lord': house_lord,
                'planets': planets_in_house,
            }

        dashas = calculate_vimshottari_dasha(date_of_birth, moon_lon)
        current_dasha = get_current_dasha(dashas)

        mars_name = PLANET_NAMES[const.MARS]
        mars_house = planets[mars_name]['house']
        mangal_dosha = check_mangal_dosha(mars_house)

        return {
            'lagna': {
                'sign': lagna_sign,
                'sign_vedic': SIGN_NAMES.get(lagna_sign, lagna_sign),
                'degree': lagna_degree,
                'lord': SIGN_LORDS[lagna_sign],
                'element': SIGN_ELEMENTS.get(lagna_sign, ''),
            },
            'moon_sign': {
                'sign': moon_sign,
                'sign_vedic': SIGN_NAMES.get(moon_sign, moon_sign),
            },
            'nakshatra': nakshatra,
            'moon_longitude': moon_lon,
            'planets': planets,
            'houses': houses,
            'dashas': dashas,
            'current_dasha': current_dasha,
            'mangal_dosha': mangal_dosha,
            'birth_details': {
                'date': date_of_birth,
                'time': time_of_birth,
                'place': place_of_birth,
                'lat': lat,
                'lon': lon,
                'timezone': timezone_offset,
            }
        }

    except Exception as e:
        logging.error(f'Vedic chart calculation error: {str(e)}')
        raise


def geocode_place(place: str) -> tuple:
    """Convert place name to lat/lon. Returns (lat, lon)."""
    city_map = {
        'new delhi': (28.6139, 77.2090), 'delhi': (28.6139, 77.2090),
        'mumbai': (19.0760, 72.8777), 'bangalore': (12.9716, 77.5946),
        'bengaluru': (12.9716, 77.5946), 'kolkata': (22.5726, 88.3639),
        'chennai': (13.0827, 80.2707), 'hyderabad': (17.3850, 78.4867),
        'pune': (18.5204, 73.8567), 'ahmedabad': (23.0225, 72.5714),
        'jaipur': (26.9124, 75.7873), 'lucknow': (26.8467, 80.9462),
        'chandigarh': (30.7333, 76.7794), 'surat': (21.1702, 72.8311),
    }
    place_lower = place.lower().strip()
    for key, coords in city_map.items():
        if key in place_lower:
            return coords

    try:
        if Nominatim:
            geolocator = Nominatim(user_agent='everydayhoroscope')
            location = geolocator.geocode(place, timeout=10)
            if location:
                return (location.latitude, location.longitude)
    except Exception:
        pass

    logging.warning(f'Could not geocode "{place}", defaulting to New Delhi')
    return (28.6139, 77.2090)


def generate_north_indian_chart_svg(houses: dict, lagna_sign: str) -> str:
    """Generate North Indian style Kundali chart as SVG."""
    planet_abbr = {
        'Sun (Surya)': 'Su', 'Moon (Chandra)': 'Mo', 'Mercury (Budha)': 'Me',
        'Venus (Shukra)': 'Ve', 'Mars (Mangal)': 'Ma', 'Jupiter (Brihaspati)': 'Ju',
        'Saturn (Shani)': 'Sa', 'Rahu': 'Ra', 'Ketu': 'Ke',
    }

    label_pos = {
        1: (150, 80), 2: (230, 55), 3: (265, 150), 4: (230, 245),
        5: (150, 268), 6: (70, 245), 7: (35, 150), 8: (70, 55),
        9: (150, 32), 10: (258, 150), 11: (150, 258), 12: (42, 150),
    }

    svg = '''<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" style="max-width:300px;width:100%">
  <defs>
    <style>
      .chart-bg { fill: #0f0d0a; }
      .chart-line { stroke: #C5A059; stroke-width: 0.8; fill: none; }
      .chart-border { stroke: #C5A059; stroke-width: 1.5; fill: none; }
      .planet-text { font-family: serif; font-size: 8px; fill: #C5A059; }
      .house-num { font-family: serif; font-size: 7px; fill: rgba(197,160,89,0.4); }
      .lagna-mark { font-family: serif; font-size: 7px; fill: #f5f0e8; font-weight: bold; }
    </style>
  </defs>
  <rect width="300" height="300" class="chart-bg" rx="4"/>
  <rect x="5" y="5" width="290" height="290" class="chart-border"/>
  <line x1="5" y1="5" x2="150" y2="150" class="chart-line"/>
  <line x1="295" y1="5" x2="150" y2="150" class="chart-line"/>
  <line x1="5" y1="295" x2="150" y2="150" class="chart-line"/>
  <line x1="295" y1="295" x2="150" y2="150" class="chart-line"/>
  <line x1="150" y1="5" x2="5" y2="150" class="chart-line"/>
  <line x1="150" y1="5" x2="295" y2="150" class="chart-line"/>
  <line x1="150" y1="295" x2="5" y2="150" class="chart-line"/>
  <line x1="150" y1="295" x2="295" y2="150" class="chart-line"/>
'''

    for house_num, data in houses.items():
        lx, ly = label_pos[house_num]
        planets_text = ' '.join([planet_abbr.get(p, p[:2]) for p in data['planets']])
        svg += f'  <text x="{lx}" y="{ly}" class="house-num" text-anchor="middle">{house_num}</text>\n'
        svg += f'  <text x="{lx}" y="{ly + 9}" class="planet-text" text-anchor="middle">{data["sign"][:3]}</text>\n'
        if planets_text:
            svg += f'  <text x="{lx}" y="{ly + 18}" class="planet-text" text-anchor="middle">{planets_text}</text>\n'
        if house_num == 1:
            svg += f'  <text x="{lx}" y="{ly - 8}" class="lagna-mark" text-anchor="middle">ASC</text>\n'

    svg += '</svg>'
    return svg


# ─── Today's Transits ─────────────────────────────────────────────────────────

def get_current_transits() -> dict:
    """Get today's planetary positions for transit analysis.

    Returns per planet: sign, degree, house (natural zodiac 1=Aries),
    longitude (0-360), retrograde flag.
    """
    now = datetime.now()
    jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60)

    transits = {}
    for pid in PLANET_IDS:
        if pid == const.SOUTH_NODE:
            north_lon, north_speed = _calc_planet(jd, swe.MEAN_NODE)
            planet_lon = (north_lon + 180.0) % 360
            speed = north_speed  # Ketu moves with Rahu
        else:
            planet_lon, speed = _calc_planet(jd, PLANET_SWE_IDS[pid])
        sign = _lon_to_sign(planet_lon)
        # Natural-zodiac house: Aries=1 ... Pisces=12 (Lal Kitab convention)
        house = SIGN_ORDER.index(sign) + 1
        transits[PLANET_NAMES[pid]] = {
            'sign': sign,
            'degree': round(planet_lon % 30, 2),
            'longitude': round(planet_lon, 4),
            'house': house,
            'retrograde': speed < 0,
        }
    return transits
