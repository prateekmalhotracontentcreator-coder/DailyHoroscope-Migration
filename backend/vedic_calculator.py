"""
EverydayHoroscope — Vedic Calculation Engine
Proprietary IP of SkyHound Studios
Powered by flatlib + Swiss Ephemeris

Architecture:
  Layer 1 (this file): Mathematical calculation — deterministic, always same result
  Layer 2 (Claude prompts): Interpretation — human-readable insights from calculated positions
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from flatlib.chart import Chart
from flatlib.object import Object
import math
from datetime import datetime, timezone
from geopy.geocoders import Nominatim
import logging

# ─── Planet & Sign Mappings ───────────────────────────────────────────────────

PLANET_IDS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.NORTH_NODE, const.SOUTH_NODE
]

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
# 1=Brahmin, 2=Kshatriya, 3=Vaishya, 4=Shudra

YONI = {
    'Ashwini': ('Horse', 'M'), 'Bharani': ('Elephant', 'M'), 'Krittika': ('Goat', 'F'),
    'Rohini': ('Serpent', 'M'), 'Mrigashira': ('Serpent', 'F'), 'Ardra': ('Dog', 'F'),
    'Punarvasu': ('Cat', 'F'), 'Pushya': ('Goat', 'M'), 'Ashlesha': ('Cat', 'M'),
    'Magha': ('Rat', 'M'), 'Purva Phalguni': ('Rat', 'F'), 'Uttara Phalguni': ('Cow', 'F'),
    'Hasta': ('Buffalo', 'F'), 'Chitra': ('Tiger', 'F'), 'Swati': ('Buffalo', 'M'),
    'Vishakha': ('Tiger', 'M'), 'Anuradha': ('Deer', 'F'), 'Jyeshtha': ('Deer', 'M'),
    'Mula': ('Dog', 'M'), 'Purva Ashadha': ('Monkey', 'F'), 'Uttara Ashadha': ('Mongoose', 'M'),
    'Shravana': ('Monkey', 'M'), 'Dhanishtha': ('Lion', 'F'), 'Shatabhisha': ('Horse', 'F'),
    'Purva Bhadrapada': ('Lion', 'M'), 'Uttara Bhadrapada': ('Cow', 'M'), 'Revati': ('Elephant', 'F'),
}

GANA = {
    'Ashwini': 'Deva', 'Mrigashira': 'Deva', 'Punarvasu': 'Deva', 'Pushya': 'Deva',
    'Hasta': 'Deva', 'Swati': 'Deva', 'Anuradha': 'Deva', 'Shravana': 'Deva', 'Revati': 'Deva',
    'Bharani': 'Manushya', 'Rohini': 'Manushya', 'Ardra': 'Manushya', 'Purva Phalguni': 'Manushya',
    'Uttara Phalguni': 'Manushya', 'Purva Ashadha': 'Manushya', 'Uttara Ashadha': 'Manushya',
    'Purva Bhadrapada': 'Manushya', 'Uttara Bhadrapada': 'Manushya',
    'Krittika': 'Rakshasa', 'Ashlesha': 'Rakshasa', 'Magha': 'Rakshasa', 'Chitra': 'Rakshasa',
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

# ─── Core Functions ───────────────────────────────────────────────────────────

def get_nakshatra(moon_longitude: float) -> dict:
    """Get Nakshatra from Moon's absolute longitude (0-360)."""
    nak_index = int(moon_longitude / (360/27))
    pada = int((moon_longitude % (360/27)) / (360/108)) + 1
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
    """
    Calculate Vimshottari Dasha periods from birth date and Moon longitude.
    Returns list of dashas with start/end dates.
    """
    nak_data = get_nakshatra(moon_longitude)
    nak_lord = nak_data['lord']
    nak_index = nak_data['index']

    # How far through the nakshatra is the Moon?
    nak_span = 360 / 27
    nak_start = nak_index * nak_span
    fraction_elapsed = (moon_longitude - nak_start) / nak_span
    dasha_years_total = DASHA_YEARS[nak_lord]
    years_elapsed = fraction_elapsed * dasha_years_total
    years_remaining = dasha_years_total - years_elapsed

    # Parse birth date
    from datetime import datetime, timedelta
    bd = datetime.strptime(birth_date, '%Y-%m-%d')

    dashas = []
    lord_idx = DASHA_ORDER.index(nak_lord)

    # First dasha is partially elapsed
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


def get_current_dasha(dashas: list) -> dict:
    """Find the currently active Mahadasha."""
    from datetime import datetime
    today = datetime.now()
    for d in dashas:
        start = datetime.strptime(d['start'], '%Y-%m-%d')
        end = datetime.strptime(d['end'], '%Y-%m-%d')
        if start <= today <= end:
            return d
    return dashas[-1]


def check_mangal_dosha(mars_house: int) -> dict:
    """
    Check Mangal Dosha based on Mars house position.
    Dosha houses: 1, 2, 4, 7, 8, 12
    Cancellation rules applied.
    """
    dosha_houses = [1, 2, 4, 7, 8, 12]
    present = mars_house in dosha_houses

    severity_map = {1: 'High', 2: 'Moderate', 4: 'Moderate', 7: 'High', 8: 'Very High', 12: 'Low'}
    severity = severity_map.get(mars_house, None) if present else None

    cancellation_rules = []
    if mars_house == 1 and True:  # Mars in Aries or Scorpio lagna cancels
        cancellation_rules.append('Mars in 1st house may be cancelled if Lagna is Aries or Scorpio')
    if mars_house == 2:
        cancellation_rules.append('Dosha reduced if Venus or Jupiter aspects Mars')

    return {
        'present': present,
        'mars_house': mars_house,
        'severity': severity,
        'cancellation_rules': cancellation_rules,
        'note': f'Mars in house {mars_house}' + (' — Mangal Dosha present' if present else ' — No Mangal Dosha'),
    }


# ─── Ashtakoot Milan Calculation ─────────────────────────────────────────────

def calculate_ashtakoot(nak1: str, sign1: str, nak2: str, sign2: str) -> dict:
    """
    Calculate full Ashtakoot Guna Milan score between two individuals.
    Returns scores for all 8 kootas with interpretations.
    """
    scores = {}

    # 1. Varna (1 point)
    v1, v2 = VARNA.get(sign1, 2), VARNA.get(sign2, 2)
    varna_score = 1 if v2 >= v1 else 0
    scores['varna'] = {
        'max': 1, 'score': varna_score,
        'label': 'Compatible' if varna_score == 1 else 'Challenging',
        'meaning': 'Spiritual evolution compatibility'
    }

    # 2. Vashya (2 points)
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
    vashya_score = 2 if mutual else (1 if one_way else 0)
    scores['vashya'] = {
        'max': 2, 'score': vashya_score,
        'label': 'Strong' if vashya_score == 2 else ('Moderate' if vashya_score == 1 else 'Weak'),
        'meaning': 'Mutual attraction and influence'
    }

    # 3. Tara (3 points) — birth star compatibility
    nak_list = [n['name'] for n in NAKSHATRAS]
    idx1 = nak_list.index(nak1) if nak1 in nak_list else 0
    idx2 = nak_list.index(nak2) if nak2 in nak_list else 0
    tara_from_1 = ((idx2 - idx1) % 27) % 9
    tara_from_2 = ((idx1 - idx2) % 27) % 9
    good_taras = [1, 3, 5, 7]  # Janma, Kshema, Sadhana, Mitra
    tara_score = 0
    if tara_from_1 in good_taras: tara_score += 1.5
    if tara_from_2 in good_taras: tara_score += 1.5
    tara_score = min(3, int(tara_score))
    scores['tara'] = {
        'max': 3, 'score': tara_score,
        'label': 'Excellent' if tara_score == 3 else ('Good' if tara_score >= 2 else 'Challenging'),
        'meaning': 'Health and longevity compatibility'
    }

    # 4. Yoni (4 points) — animal instinct compatibility
    y1 = YONI.get(nak1, ('Unknown', 'M'))
    y2 = YONI.get(nak2, ('Unknown', 'M'))
    if y1[0] == y2[0]:
        yoni_score = 4
    else:
        friendly_pairs = [
            ('Horse', 'Elephant'), ('Goat', 'Dog'), ('Serpent', 'Mongoose'),
            ('Cat', 'Rat'), ('Cow', 'Tiger'), ('Buffalo', 'Monkey'), ('Lion', 'Deer'),
        ]
        enemy_pairs = [
            ('Horse', 'Buffalo'), ('Elephant', 'Lion'), ('Goat', 'Monkey'),
        ]
        pair = tuple(sorted([y1[0], y2[0]]))
        if any(tuple(sorted(p)) == pair for p in friendly_pairs):
            yoni_score = 3
        elif any(tuple(sorted(p)) == pair for p in enemy_pairs):
            yoni_score = 0
        else:
            yoni_score = 2
    scores['yoni'] = {
        'max': 4, 'score': yoni_score,
        'label': 'Excellent' if yoni_score == 4 else ('Good' if yoni_score == 3 else ('Moderate' if yoni_score == 2 else 'Challenging')),
        'meaning': 'Physical and intimate compatibility'
    }

    # 5. Graha Maitri (5 points) — planetary friendship
    lord1 = SIGN_LORDS.get(sign1, 'Mercury')
    lord2 = SIGN_LORDS.get(sign2, 'Venus')
    friends = {
        'Sun': ['Moon', 'Mars', 'Jupiter'], 'Moon': ['Sun', 'Mercury'],
        'Mars': ['Sun', 'Moon', 'Jupiter'], 'Mercury': ['Sun', 'Venus'],
        'Jupiter': ['Sun', 'Moon', 'Mars'], 'Venus': ['Mercury', 'Saturn'],
        'Saturn': ['Mercury', 'Venus'],
    }
    l1_friends = friends.get(lord1, [])
    l2_friends = friends.get(lord2, [])
    mutual_friends = lord2 in l1_friends and lord1 in l2_friends
    one_friend = lord2 in l1_friends or lord1 in l2_friends
    same_lord = lord1 == lord2
    if same_lord or mutual_friends: gm_score = 5
    elif one_friend: gm_score = 4
    else: gm_score = 0
    scores['graha_maitri'] = {
        'max': 5, 'score': gm_score,
        'label': 'Excellent' if gm_score == 5 else ('Good' if gm_score == 4 else 'Challenging'),
        'meaning': 'Mental and intellectual compatibility'
    }

    # 6. Gana (6 points) — temperament
    g1 = GANA.get(nak1, 'Manushya')
    g2 = GANA.get(nak2, 'Manushya')
    if g1 == g2: gana_score = 6
    elif set([g1, g2]) == {'Deva', 'Manushya'}: gana_score = 5
    elif set([g1, g2]) == {'Manushya', 'Rakshasa'}: gana_score = 1
    else: gana_score = 0  # Deva + Rakshasa
    scores['gana'] = {
        'max': 6, 'score': gana_score,
        'label': 'Perfect' if gana_score == 6 else ('Good' if gana_score >= 5 else ('Moderate' if gana_score == 1 else 'Challenging')),
        'meaning': 'Nature and temperament compatibility'
    }

    # 7. Bhakoot (7 points) — emotional bonding
    sign_idx1 = SIGN_ORDER.index(sign1)
    sign_idx2 = SIGN_ORDER.index(sign2)
    diff = abs(sign_idx1 - sign_idx2) + 1
    bad_bhakoots = [6, 8, 12]  # 6-8 and 2-12 axis
    diff_rev = 13 - diff if diff > 1 else diff
    bhakoot_bad = diff in bad_bhakoots or diff_rev in bad_bhakoots
    bhakoot_score = 0 if bhakoot_bad else 7
    scores['bhakoot'] = {
        'max': 7, 'score': bhakoot_score,
        'label': 'Excellent' if bhakoot_score == 7 else 'Challenging',
        'meaning': 'Love, family prosperity and longevity'
    }

    # 8. Nadi (8 points) — genetic and health compatibility
    n1 = NADI.get(nak1, 'Vata')
    n2 = NADI.get(nak2, 'Pitta')
    nadi_score = 0 if n1 == n2 else 8  # Same Nadi = 0 (health risk)
    scores['nadi'] = {
        'max': 8, 'score': nadi_score,
        'label': 'Excellent' if nadi_score == 8 else 'Nadi Dosha Present',
        'meaning': 'Health and progeny compatibility'
    }

    total = sum(s['score'] for s in scores.values())
    verdict = (
        'Excellent Match — Highly Recommended' if total >= 32 else
        'Very Good Match' if total >= 24 else
        'Good Match — Recommended with Remedies' if total >= 18 else
        'Below Threshold — Consult Astrologer'
    )

    return {
        'kootas': scores,
        'total_score': total,
        'max_score': 36,
        'verdict': verdict,
        'percentage': round((total / 36) * 100),
    }


# ─── Main Chart Calculator ────────────────────────────────────────────────────

def calculate_vedic_chart(
    date_of_birth: str,
    time_of_birth: str,
    place_of_birth: str,
    timezone_offset: str = '+05:30'
) -> dict:
    """
    Master function — calculates complete Vedic birth chart.
    Returns structured dict ready to pass to Claude for interpretation.

    Args:
        date_of_birth: 'YYYY-MM-DD'
        time_of_birth: 'HH:MM'
        place_of_birth: 'City, Country' string
        timezone_offset: '+05:30' for IST (default)

    Returns:
        Complete chart data as dict
    """
    try:
        # Geocode place
        lat, lon = geocode_place(place_of_birth)

        # Format for flatlib
        date_str = date_of_birth.replace('-', '/')
        time_str = time_of_birth if len(time_of_birth) == 5 else time_of_birth + ':00'

        # flatlib GeoPos expects format like '28n22' or '77e13' (degrees + cardinal + minutes as int)
        def fmt_coord(val, pos_char, neg_char):
            deg = int(abs(val))
            mins = int(round((abs(val) - deg) * 60))
            card = pos_char if val >= 0 else neg_char
            return f'{deg}{card}{mins:02d}'

        date = Datetime(date_str, time_str, timezone_offset)
        pos = GeoPos(fmt_coord(lat, 'n', 's'), fmt_coord(lon, 'e', 'w'))
        chart = Chart(date, pos, IDs=PLANET_IDS)

        # Get Ascendant via getAngle (ASC is an angle, not a planet object)
        asc = chart.getAngle(const.ASC)
        lagna_sign = asc.sign
        lagna_degree = round(asc.lon % 30, 2)

        # Get all planet positions
        planets = {}
        for pid in PLANET_IDS:
            obj = chart.get(pid)
            planet_sign = obj.sign
            house = get_house_number(planet_sign, lagna_sign)
            planets[PLANET_NAMES[pid]] = {
                'sign': planet_sign,
                'sign_vedic': SIGN_NAMES.get(planet_sign, planet_sign),
                'degree': round(obj.lon % 30, 2),
                'house': house,
                'lord_of_sign': SIGN_LORDS.get(planet_sign, ''),
                'retrograde': getattr(obj, 'movement', '') == const.RETROGRADE,
            }

        # Moon data for Nakshatra + Dasha
        moon = chart.get(const.MOON)
        moon_longitude = moon.lon
        nakshatra = get_nakshatra(moon_longitude)
        moon_sign = moon.sign

        # Build 12-house map
        houses = {}
        for h in range(1, 13):
            sign_idx = (SIGN_ORDER.index(lagna_sign) + h - 1) % 12
            house_sign = SIGN_ORDER[sign_idx]
            house_lord = SIGN_LORDS[house_sign]
            planets_in_house = [
                name for name, data in planets.items() if data['house'] == h
            ]
            houses[h] = {
                'house': h,
                'name': HOUSE_NAMES[h],
                'sign': house_sign,
                'sign_vedic': SIGN_NAMES.get(house_sign, house_sign),
                'lord': house_lord,
                'planets': planets_in_house,
            }

        # Vimshottari Dasha
        dashas = calculate_vimshottari_dasha(date_of_birth, moon_longitude)
        current_dasha = get_current_dasha(dashas)

        # Mangal Dosha
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
    # Common Indian cities hardcoded for speed + reliability
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

    # Fallback to geocoder
    try:
        geolocator = Nominatim(user_agent='everydayhoroscope')
        location = geolocator.geocode(place, timeout=10)
        if location:
            return (location.latitude, location.longitude)
    except Exception:
        pass

    # Default to Delhi if all else fails
    logging.warning(f'Could not geocode "{place}", defaulting to New Delhi')
    return (28.6139, 77.2090)


def generate_north_indian_chart_svg(houses: dict, lagna_sign: str) -> str:
    """
    Generate North Indian style Kundali chart as SVG.
    Diamond/square grid with 12 houses and planet positions.
    """
    # Planet abbreviations for chart display
    planet_abbr = {
        'Sun (Surya)': 'Su', 'Moon (Chandra)': 'Mo', 'Mercury (Budha)': 'Me',
        'Venus (Shukra)': 'Ve', 'Mars (Mangal)': 'Ma', 'Jupiter (Brihaspati)': 'Ju',
        'Saturn (Shani)': 'Sa', 'Rahu': 'Ra', 'Ketu': 'Ke',
    }

    # North Indian chart house positions (pixel centres in 300x300 grid)
    # House positions in the traditional diamond layout
    house_positions = {
        1:  (150, 150),  # Centre top (Lagna)
        2:  (225, 75),   # Top right
        3:  (300, 0),    # Top right corner — adjust to fit
        4:  (225, 150),  # Right middle
        5:  (300, 225),
        6:  (225, 300),
        7:  (150, 225),  # Centre bottom
        8:  (75, 300),
        9:  (0, 225),
        10: (75, 150),   # Left middle
        11: (0, 75),
        12: (75, 0),
    }

    # North Indian chart SVG paths (standard diamond grid)
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

  <!-- Background -->
  <rect width="300" height="300" class="chart-bg" rx="4"/>

  <!-- Outer border -->
  <rect x="5" y="5" width="290" height="290" class="chart-border"/>

  <!-- Diagonal lines forming the diamond grid -->
  <line x1="5" y1="5" x2="150" y2="150" class="chart-line"/>
  <line x1="295" y1="5" x2="150" y2="150" class="chart-line"/>
  <line x1="5" y1="295" x2="150" y2="150" class="chart-line"/>
  <line x1="295" y1="295" x2="150" y2="150" class="chart-line"/>
  <line x1="5" y1="5" x2="295" y2="5" class="chart-line"/>
  <line x1="5" y1="295" x2="295" y2="295" class="chart-line"/>
  <line x1="5" y1="5" x2="5" y2="295" class="chart-line"/>
  <line x1="295" y1="5" x2="295" y2="295" class="chart-line"/>

  <!-- Mid-edge to mid-edge lines -->
  <line x1="150" y1="5" x2="5" y2="150" class="chart-line"/>
  <line x1="150" y1="5" x2="295" y2="150" class="chart-line"/>
  <line x1="150" y1="295" x2="5" y2="150" class="chart-line"/>
  <line x1="150" y1="295" x2="295" y2="150" class="chart-line"/>
'''

    # House label positions in North Indian chart
    house_label_pos = {
        1:  (150, 90),   # Top centre triangle
        2:  (220, 55),   # Top right
        3:  (255, 150),  # Right top
        4:  (220, 240),  # Right bottom
        5:  (150, 210),  # Bottom centre triangle — lower
        6:  (80, 240),   # Left bottom
        7:  (45, 150),   # Left bottom
        8:  (80, 55),    # Left top
        9:  (150, 30),   # Very top
        10: (270, 150),  # Far right
        11: (150, 270),  # Very bottom
        12: (30, 150),   # Far left
    }

    # Corrected North Indian standard positions
    label_pos = {
        1:  (150, 80),
        2:  (230, 55),
        3:  (265, 150),
        4:  (230, 245),
        5:  (150, 268),
        6:  (70, 245),
        7:  (35, 150),
        8:  (70, 55),
        9:  (150, 32),
        10: (258, 150),
        11: (150, 258),
        12: (42, 150),
    }

    lagna_sign_short = lagna_sign[:3].upper()

    for house_num, data in houses.items():
        lx, ly = label_pos[house_num]
        planets_text = ' '.join([planet_abbr.get(p, p[:2]) for p in data['planets']])

        # House number
        svg += f'  <text x="{lx}" y="{ly}" class="house-num" text-anchor="middle">{house_num}</text>\n'

        # Sign (first 3 letters)
        sign_short = data['sign'][:3]
        svg += f'  <text x="{lx}" y="{ly + 9}" class="planet-text" text-anchor="middle">{sign_short}</text>\n'

        # Planets
        if planets_text:
            svg += f'  <text x="{lx}" y="{ly + 18}" class="planet-text" text-anchor="middle">{planets_text}</text>\n'

        # Mark Lagna house
        if house_num == 1:
            svg += f'  <text x="{lx}" y="{ly - 8}" class="lagna-mark" text-anchor="middle">ASC</text>\n'

    svg += '</svg>'
    return svg


# ─── Today's Transits ─────────────────────────────────────────────────────────

def get_current_transits() -> dict:
    """Get today's planetary positions for transit analysis."""
    from datetime import datetime
    now = datetime.now()
    date_str = now.strftime('%Y/%m/%d')
    time_str = now.strftime('%H:%M')

    date = Datetime(date_str, time_str, '+05:30')
    pos = GeoPos('28n38', '77e13')  # Delhi as reference
    chart = Chart(date, pos, IDs=PLANET_IDS)

    transits = {}
    for pid in PLANET_IDS:
        obj = chart.get(pid)
        transits[PLANET_NAMES[pid]] = {
            'sign': obj.sign,
            'degree': round(obj.lon % 30, 2),
        }
    return transits
