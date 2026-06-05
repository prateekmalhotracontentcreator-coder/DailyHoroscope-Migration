from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

import swisseph as swe


swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)  # KP system requires Newcomb/Krishnamurti ayanamsha -- not Lahiri (AYA-1)

SIDEREAL_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
KP_MODEL_VERSION = "kp-longevity-1.0.0"
DEFAULT_LOOKAHEAD_DAYS = 540

SIGN_ORDER = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

SIGN_LORDS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

PLANET_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
}

DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

NAKSHATRAS = [
    {"name": "Ashwini", "lord": "Ketu"},
    {"name": "Bharani", "lord": "Venus"},
    {"name": "Krittika", "lord": "Sun"},
    {"name": "Rohini", "lord": "Moon"},
    {"name": "Mrigashira", "lord": "Mars"},
    {"name": "Ardra", "lord": "Rahu"},
    {"name": "Punarvasu", "lord": "Jupiter"},
    {"name": "Pushya", "lord": "Saturn"},
    {"name": "Ashlesha", "lord": "Mercury"},
    {"name": "Magha", "lord": "Ketu"},
    {"name": "Purva Phalguni", "lord": "Venus"},
    {"name": "Uttara Phalguni", "lord": "Sun"},
    {"name": "Hasta", "lord": "Moon"},
    {"name": "Chitra", "lord": "Mars"},
    {"name": "Swati", "lord": "Rahu"},
    {"name": "Vishakha", "lord": "Jupiter"},
    {"name": "Anuradha", "lord": "Saturn"},
    {"name": "Jyeshtha", "lord": "Mercury"},
    {"name": "Mula", "lord": "Ketu"},
    {"name": "Purva Ashadha", "lord": "Venus"},
    {"name": "Uttara Ashadha", "lord": "Sun"},
    {"name": "Shravana", "lord": "Moon"},
    {"name": "Dhanishtha", "lord": "Mars"},
    {"name": "Shatabhisha", "lord": "Rahu"},
    {"name": "Purva Bhadrapada", "lord": "Jupiter"},
    {"name": "Uttara Bhadrapada", "lord": "Saturn"},
    {"name": "Revati", "lord": "Mercury"},
]

EXALTATION_SIGNS = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",
}

DEBILITATION_SIGNS = {
    "Sun": "Libra",
    "Moon": "Scorpio",
    "Mars": "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus": "Virgo",
    "Saturn": "Aries",
}

BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

SIGN_BODY_PARTS = {
    "Aries": {"system": "Head, brain, scalp, upper face", "dosha": "Pitta"},
    "Taurus": {"system": "Throat, thyroid, jaw, cervical region", "dosha": "Kapha"},
    "Gemini": {"system": "Lungs, shoulders, nerves, bronchial system", "dosha": "Vata"},
    "Cancer": {"system": "Chest, breasts, stomach, fluids", "dosha": "Kapha"},
    "Leo": {"system": "Heart, spine, circulation, vitality core", "dosha": "Pitta"},
    "Virgo": {"system": "Intestines, pancreas, assimilation, gut health", "dosha": "Vata"},
    "Libra": {"system": "Kidneys, lower back, endocrine balance", "dosha": "Vata"},
    "Scorpio": {"system": "Reproductive organs, colon, elimination, hidden pathology", "dosha": "Pitta"},
    "Sagittarius": {"system": "Liver, hips, thighs, sciatic region", "dosha": "Pitta"},
    "Capricorn": {"system": "Bones, knees, joints, teeth, chronic depletion", "dosha": "Vata"},
    "Aquarius": {"system": "Circulation, calves, ankles, nervous signaling", "dosha": "Vata"},
    "Pisces": {"system": "Feet, lymph, immune sensitivity, sleep restoration", "dosha": "Kapha"},
}

PLANET_HEALTH_DOMAINS = {
    "Sun": "heart, vitality, fever states, vision, blood pressure",
    "Moon": "fluids, hormones, digestion, sleep, emotional regulation",
    "Mars": "blood, inflammation, injuries, surgery, acute flare-ups",
    "Mercury": "nerves, skin, respiration, cognition, gut-brain signaling",
    "Jupiter": "liver, pancreas, metabolism, fat regulation, growth syndromes",
    "Venus": "kidneys, reproductive health, sugar balance, fertility",
    "Saturn": "bones, joints, chronic disease, depletion, nerve compression",
    "Rahu": "toxicity, strange syndromes, allergies, compulsive stress patterns",
    "Ketu": "deficiency states, hidden pain, psychosomatic drains, sudden drops",
}

HOUSE_HEALTH_DOMAINS = {
    1: "constitution, resilience, baseline vitality",
    2: "face, mouth, food patterns, maraka potential",
    3: "respiration, effort tolerance, shoulders, nervous courage",
    4: "chest, lungs, heart emotional baseline",
    5: "heart rhythm, digestion, recovery intelligence",
    6: "disease tendency, infection, treatment load, chronic complaints",
    7: "reproductive interface, maraka potential, vitality exchange",
    8: "longevity, surgeries, hidden disease, crisis periods",
    9: "healing grace, prevention, recovery through guidance",
    10: "skeletal load, stress burden, life management",
    11: "circulation, restoration through networks and support",
    12: "sleep, hospitalization, immunity leakage, losses of vitality",
}

PRAKRITI_DESCRIPTIONS = {
    "Vata": "The chart shows a stronger Vata signature, so irregular routines, overwork, anxiety, dryness, sleep disruption, and nervous depletion need earlier correction than they would in a steadier constitution.",
    "Pitta": "The chart carries a stronger Pitta signature, so heat, inflammation, acidity, blood pressure spikes, impatience, and over-driven productivity need regular cooling and regulation.",
    "Kapha": "The chart leans Kapha, so congestion, water retention, sluggish metabolism, sugar imbalance, and comfort-led inertia are the patterns to manage before they become entrenched.",
}

MEDICAL_DISCLAIMER = (
    "This Ayur Jyotish report is a spiritual and astrological wellness reading, not a medical diagnosis. "
    "It must never replace consultation with a licensed doctor, mental health professional, or emergency service. "
    "Use it for reflective guidance only, and seek qualified medical care for symptoms, testing, treatment, or urgent concerns."
)


@dataclass
class ReportInput:
    date_of_birth: str
    time_of_birth: str
    latitude: float
    longitude: float
    timezone_name: str
    place_label: str | None = None
    reference_date: str | None = None


def normalize_longitude(value: float) -> float:
    return value % 360.0


def sign_from_longitude(value: float) -> str:
    return SIGN_ORDER[int(normalize_longitude(value) // 30.0)]


def sign_index(sign_name: str) -> int:
    return SIGN_ORDER.index(sign_name)


def degree_in_sign(value: float) -> float:
    return round(normalize_longitude(value) % 30.0, 2)


def format_degree(value: float) -> str:
    degrees = normalize_longitude(value)
    sign_name = sign_from_longitude(degrees)
    sign_degree = degrees % 30.0
    whole = int(sign_degree)
    minutes = int(round((sign_degree - whole) * 60.0))
    if minutes == 60:
        whole += 1
        minutes = 0
    return f"{whole:02d}°{minutes:02d}' {sign_name}"


def local_datetime(date_text: str, time_text: str, timezone_name: str) -> datetime:
    try:
        target_date = date.fromisoformat(date_text)
        hour_text, minute_text = time_text.split(":", 1)
        target_time = time(hour=int(hour_text), minute=int(minute_text))
    except ValueError as err:
        raise ValueError("Invalid date_of_birth or time_of_birth. Expected YYYY-MM-DD and HH:MM.") from err
    try:
        return datetime.combine(target_date, target_time, tzinfo=ZoneInfo(timezone_name))
    except Exception as err:
        raise ValueError("Invalid timezone.") from err


def parse_reference_date(reference_date: str | None, timezone_name: str) -> date:
    if reference_date:
        return date.fromisoformat(reference_date)
    return datetime.now(timezone.utc).astimezone(ZoneInfo(timezone_name)).date()


def julian_day(moment: datetime) -> float:
    moment_utc = moment.astimezone(timezone.utc)
    decimal_hour = moment_utc.hour + (moment_utc.minute / 60.0) + (moment_utc.second / 3600.0)
    return swe.julday(moment_utc.year, moment_utc.month, moment_utc.day, decimal_hour)


def sidereal_longitude_and_speed(jd_ut: float, body: str) -> tuple[float, float]:
    if body == "Ketu":
        rahu_longitude, rahu_speed = sidereal_longitude_and_speed(jd_ut, "Rahu")
        return normalize_longitude(rahu_longitude + 180.0), rahu_speed
    result = swe.calc_ut(jd_ut, PLANET_IDS[body], SIDEREAL_FLAGS)[0]
    return normalize_longitude(result[0]), float(result[3])


def shortest_arc(angle_a: float, angle_b: float) -> float:
    distance = abs(normalize_longitude(angle_a) - normalize_longitude(angle_b))
    return min(distance, 360.0 - distance)


def signed_arc(angle_a: float, angle_b: float) -> float:
    return ((normalize_longitude(angle_a) - normalize_longitude(angle_b) + 180.0) % 360.0) - 180.0


def whole_sign_houses(ascendant_sign: str) -> dict[int, str]:
    start = sign_index(ascendant_sign)
    return {house: SIGN_ORDER[(start + house - 1) % 12] for house in range(1, 13)}


def house_from_sign(sign_name: str, ascendant_sign: str) -> int:
    return ((sign_index(sign_name) - sign_index(ascendant_sign)) % 12) + 1


def house_number_from_cusps(longitude: float, cusps: list[float]) -> int:
    target = normalize_longitude(longitude)
    normalized_cusps = [normalize_longitude(item) for item in cusps]
    for index in range(12):
        start = normalized_cusps[index]
        end = normalized_cusps[(index + 1) % 12]
        span = (end - start) % 360.0
        offset = (target - start) % 360.0
        if offset < span or (index == 11 and offset <= span):
            return index + 1
    return 12


def rotate_dasha_sequence(start_lord: str) -> list[str]:
    start_index = DASHA_ORDER.index(start_lord)
    return DASHA_ORDER[start_index:] + DASHA_ORDER[:start_index]


def get_nakshatra(longitude: float) -> dict[str, Any]:
    span = 360.0 / 27.0
    normalized = normalize_longitude(longitude)
    index = int(normalized // span)
    pada = int((normalized % span) // (span / 4.0)) + 1
    nakshatra = NAKSHATRAS[index]
    return {
        "name": nakshatra["name"],
        "lord": nakshatra["lord"],
        "index": index,
        "pada": pada,
        "start": round(index * span, 6),
        "offset": round(normalized - (index * span), 6),
    }


def _kp_sub_segment(start_lord: str, span: float, offset: float) -> tuple[str, float, float, list[dict[str, Any]]]:
    start = 0.0
    sequence = rotate_dasha_sequence(start_lord)
    segments: list[dict[str, Any]] = []
    chosen_lord = sequence[-1]
    chosen_start = 0.0
    chosen_span = span
    for lord in sequence:
        segment_span = span * (DASHA_YEARS[lord] / 120.0)
        segment = {
            "lord": lord,
            "start": round(start, 6),
            "end": round(start + segment_span, 6),
            "span": round(segment_span, 6),
        }
        segments.append(segment)
        if offset <= start + segment_span or abs(offset - (start + segment_span)) < 1e-9:
            chosen_lord = lord
            chosen_start = start
            chosen_span = segment_span
            break
        start += segment_span
    return chosen_lord, chosen_start, chosen_span, segments


def kp_chain(longitude: float) -> dict[str, Any]:
    normalized = normalize_longitude(longitude)
    sign_name = sign_from_longitude(normalized)
    nakshatra = get_nakshatra(normalized)
    sign_lord = SIGN_LORDS[sign_name]
    star_lord = str(nakshatra["lord"])
    sub_lord, sub_start, sub_span, sub_segments = _kp_sub_segment(star_lord, 360.0 / 27.0, nakshatra["offset"])
    sub_offset = nakshatra["offset"] - sub_start
    sub_sub_lord, sub_sub_start, sub_sub_span, _ = _kp_sub_segment(sub_lord, sub_span, sub_offset)
    return {
        "sign": sign_name,
        "sign_lord": sign_lord,
        "nakshatra": nakshatra["name"],
        "nakshatra_lord": star_lord,
        "pada": nakshatra["pada"],
        "sub_lord": sub_lord,
        "sub_sub_lord": sub_sub_lord,
        "longitude": round(normalized, 4),
        "formatted_longitude": format_degree(normalized),
        "sub_lord_span_degrees": round(sub_span, 6),
        "sub_sub_lord_span_degrees": round(sub_sub_span, 6),
        "sub_sequence": sub_segments,
        "sub_position_degrees": round(sub_offset, 6),
        "sub_sub_position_degrees": round(sub_offset - sub_sub_start, 6),
    }


def placidus_sidereal_cusps(jd_ut: float, latitude: float, longitude: float) -> tuple[list[float], dict[str, float]]:
    tropical_cusps, ascmc = swe.houses(jd_ut, latitude, longitude, b"P")
    ayanamsha = swe.get_ayanamsa_ut(jd_ut)
    sidereal_cusps = [normalize_longitude(value - ayanamsha) for value in tropical_cusps]
    angles = {
        "ascendant": normalize_longitude(ascmc[0] - ayanamsha),
        "midheaven": normalize_longitude(ascmc[1] - ayanamsha),
        "armc": float(ascmc[2]),
        "vertex": normalize_longitude(ascmc[3] - ayanamsha),
    }
    return sidereal_cusps, angles


def build_birth_snapshot(payload: ReportInput) -> dict[str, Any]:
    birth_local = local_datetime(payload.date_of_birth, payload.time_of_birth, payload.timezone_name)
    jd_ut = julian_day(birth_local)
    cusps, angles = placidus_sidereal_cusps(jd_ut, payload.latitude, payload.longitude)
    asc_longitude = angles["ascendant"]
    asc_sign = sign_from_longitude(asc_longitude)
    planets: dict[str, Any] = {}
    for body in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        longitude_value, speed_value = sidereal_longitude_and_speed(jd_ut, body)
        sign_name = sign_from_longitude(longitude_value)
        planets[body] = {
            "longitude": round(longitude_value, 4),
            "formatted_longitude": format_degree(longitude_value),
            "sign": sign_name,
            "degree": degree_in_sign(longitude_value),
            "whole_sign_house": house_from_sign(sign_name, asc_sign),
            "placidus_house": house_number_from_cusps(longitude_value, cusps),
            "retrograde": speed_value < 0,
            "speed": round(speed_value, 5),
            "kp": kp_chain(longitude_value),
        }
    house_signs = {house: sign_from_longitude(cusps[house - 1]) for house in range(1, 13)}
    house_lords = {house: SIGN_LORDS[sign_name] for house, sign_name in house_signs.items()}
    cusp_details = []
    for house in range(1, 13):
        cusp_longitude = cusps[house - 1]
        cusp_sign = house_signs[house]
        cusp_details.append(
            {
                "house": house,
                "longitude": round(cusp_longitude, 4),
                "formatted_longitude": format_degree(cusp_longitude),
                "sign": cusp_sign,
                "sign_lord": SIGN_LORDS[cusp_sign],
                "kp": kp_chain(cusp_longitude),
                "domain": HOUSE_HEALTH_DOMAINS[house],
            }
        )
    return {
        "input": {
            "date_of_birth": payload.date_of_birth,
            "time_of_birth": payload.time_of_birth,
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "timezone": payload.timezone_name,
            "place_label": payload.place_label,
        },
        "model_version": KP_MODEL_VERSION,
        "birth_local": birth_local.isoformat(),
        "julian_day_ut": jd_ut,
        "ayanamsha": round(swe.get_ayanamsa_ut(jd_ut), 6),
        "angles": {
            "ascendant_longitude": round(asc_longitude, 4),
            "ascendant_sign": asc_sign,
            "ascendant_degree": degree_in_sign(asc_longitude),
            "midheaven_longitude": round(angles["midheaven"], 4),
            "midheaven_sign": sign_from_longitude(angles["midheaven"]),
            "midheaven_degree": degree_in_sign(angles["midheaven"]),
        },
        "cusps": cusp_details,
        "house_signs": {str(k): v for k, v in house_signs.items()},
        "house_lords": {str(k): v for k, v in house_lords.items()},
        "whole_sign_houses": {str(k): v for k, v in whole_sign_houses(asc_sign).items()},
        "planets": planets,
        "moon_nakshatra": planets["Moon"]["kp"]["nakshatra"],
    }


def build_vimshottari_timeline(moon_longitude: float, birth_local: datetime, limit_years: int = 120) -> dict[str, Any]:
    nak = get_nakshatra(moon_longitude)
    start_lord = str(nak["lord"])
    nak_span = 360.0 / 27.0
    fraction_elapsed = (normalize_longitude(moon_longitude) - (nak["index"] * nak_span)) / nak_span
    remaining_years = DASHA_YEARS[start_lord] * (1.0 - fraction_elapsed)
    maha_dashas: list[dict[str, Any]] = []
    cursor = birth_local
    first_end = cursor + timedelta(days=remaining_years * 365.25)
    maha_dashas.append(
        {
            "planet": start_lord,
            "start": cursor.date().isoformat(),
            "end": first_end.date().isoformat(),
            "years": round(remaining_years, 2),
        }
    )
    cursor = first_end
    total_years = remaining_years
    start_index = DASHA_ORDER.index(start_lord)
    step = 1
    while total_years < limit_years and len(maha_dashas) < 18:
        lord = DASHA_ORDER[(start_index + step) % len(DASHA_ORDER)]
        years = DASHA_YEARS[lord]
        end = cursor + timedelta(days=years * 365.25)
        maha_dashas.append({"planet": lord, "start": cursor.date().isoformat(), "end": end.date().isoformat(), "years": years})
        cursor = end
        total_years += years
        step += 1
    return {
        "birth_nakshatra": nak["name"],
        "birth_nakshatra_lord": start_lord,
        "maha_dashas": maha_dashas,
    }


def build_antar_dashas(parent_lord: str, start_date_text: str, end_date_text: str) -> list[dict[str, Any]]:
    start_dt = datetime.combine(date.fromisoformat(start_date_text), time.min, tzinfo=timezone.utc)
    end_dt = datetime.combine(date.fromisoformat(end_date_text), time.min, tzinfo=timezone.utc)
    total_days = max(1.0, (end_dt - start_dt).days)
    parent_years = DASHA_YEARS[parent_lord]
    cursor = start_dt
    items: list[dict[str, Any]] = []
    parent_index = DASHA_ORDER.index(parent_lord)
    for offset in range(len(DASHA_ORDER)):
        child = DASHA_ORDER[(parent_index + offset) % len(DASHA_ORDER)]
        portion_days = total_days * (DASHA_YEARS[child] / 120.0)
        child_end = cursor + timedelta(days=portion_days * parent_years)
        items.append({"planet": child, "start": cursor.date().isoformat(), "end": child_end.date().isoformat()})
        cursor = child_end
    items[-1]["end"] = end_dt.date().isoformat()
    return items


def current_dasha_periods(timeline: dict[str, Any], on_date: date) -> dict[str, Any]:
    maha_dasha = timeline["maha_dashas"][-1]
    for maha in timeline["maha_dashas"]:
        if date.fromisoformat(maha["start"]) <= on_date <= date.fromisoformat(maha["end"]):
            maha_dasha = maha
            break
    antar_dashas = build_antar_dashas(maha_dasha["planet"], maha_dasha["start"], maha_dasha["end"])
    antar_dasha = antar_dashas[-1]
    for antar in antar_dashas:
        if date.fromisoformat(antar["start"]) <= on_date <= date.fromisoformat(antar["end"]):
            antar_dasha = antar
            break
    return {
        "maha_dasha": maha_dasha,
        "antar_dasha": antar_dasha,
        "antar_dashas": antar_dashas,
    }


def transit_snapshot(target_date: date, timezone_name: str, *, bodies: tuple[str, ...] | None = None) -> dict[str, Any]:
    bodies = bodies or ("Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
    moment = datetime.combine(target_date, time(hour=12), tzinfo=ZoneInfo(timezone_name))
    jd_ut = julian_day(moment)
    result: dict[str, Any] = {"date": target_date.isoformat(), "julian_day_ut": jd_ut, "planets": {}}
    for body in bodies:
        longitude_value, speed_value = sidereal_longitude_and_speed(jd_ut, body)
        result["planets"][body] = {
            "longitude": round(longitude_value, 4),
            "sign": sign_from_longitude(longitude_value),
            "degree": degree_in_sign(longitude_value),
            "retrograde": speed_value < 0,
            "speed": round(speed_value, 5),
            "kp": kp_chain(longitude_value),
        }
    return result


def planet_strength(planet_name: str, details: dict[str, Any], ascendant_sign: str) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    sign_name = str(details["sign"])
    house_num = int(details["whole_sign_house"])
    if SIGN_LORDS[sign_name] == planet_name:
        score += 3
        reasons.append(f"in own sign ({sign_name})")
    if EXALTATION_SIGNS.get(planet_name) == sign_name:
        score += 4
        reasons.append(f"exalted in {sign_name}")
    if DEBILITATION_SIGNS.get(planet_name) == sign_name:
        score -= 4
        reasons.append(f"debilitated in {sign_name}")
    if house_num in {1, 4, 5, 7, 9, 10}:
        score += 2
        reasons.append(f"well-placed in house {house_num}")
    if house_num in {6, 8, 12}:
        score -= 2
        reasons.append(f"under pressure in house {house_num}")
    if details.get("retrograde"):
        score -= 1
        reasons.append("retrograde")
    if planet_name in BENEFICS and house_num in {1, 5, 9, 10}:
        score += 1
    if planet_name in MALEFICS and house_num in {2, 7, 8, 12}:
        score -= 1
    if house_from_sign(sign_name, ascendant_sign) == 8:
        reasons.append("connected to longevity testing")
    return score, reasons


def house_relevance_for_planet(snapshot: dict[str, Any], planet_name: str) -> dict[str, int]:
    planets = snapshot["planets"]
    houses = snapshot["house_lords"]
    result: dict[str, int] = {str(house): 0 for house in range(1, 13)}
    details = planets[planet_name]
    result[str(int(details["whole_sign_house"]))] += 3
    for house, lord in houses.items():
        if lord == planet_name:
            result[str(int(house))] += 2
    kp = details["kp"]
    for linked_planet in (kp["nakshatra_lord"], kp["sub_lord"], kp["sub_sub_lord"]):
        if linked_planet not in planets:
            continue
        linked = planets[linked_planet]
        result[str(int(linked["whole_sign_house"]))] += 1
        for house, lord in houses.items():
            if lord == linked_planet:
                result[str(int(house))] += 1
    return result


def significators(snapshot: dict[str, Any], target_houses: set[int]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for planet_name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        relevance = house_relevance_for_planet(snapshot, planet_name)
        hit_houses = sorted(house for house in target_houses if relevance[str(house)] > 0)
        if not hit_houses:
            continue
        total = sum(relevance[str(house)] for house in hit_houses)
        items.append(
            {
                "planet": planet_name,
                "houses": hit_houses,
                "score": total,
                "basis": relevance,
                "nakshatra_lord": snapshot["planets"][planet_name]["kp"]["nakshatra_lord"],
                "sub_lord": snapshot["planets"][planet_name]["kp"]["sub_lord"],
            }
        )
    return sorted(items, key=lambda item: (-int(item["score"]), item["planet"]))


def longevity_classification(snapshot: dict[str, Any]) -> dict[str, Any]:
    asc_sign = snapshot["angles"]["ascendant_sign"]
    asc_lord = snapshot["house_lords"]["1"]
    eighth_lord = snapshot["house_lords"]["8"]
    second_lord = snapshot["house_lords"]["2"]
    seventh_lord = snapshot["house_lords"]["7"]
    asc_score, asc_reasons = planet_strength(asc_lord, snapshot["planets"][asc_lord], asc_sign)
    eighth_score, eighth_reasons = planet_strength(eighth_lord, snapshot["planets"][eighth_lord], asc_sign)
    saturn_score, saturn_reasons = planet_strength("Saturn", snapshot["planets"]["Saturn"], asc_sign)
    health_sigs = significators(snapshot, {1, 6, 8, 12})
    maraka_sigs = significators(snapshot, {2, 7, 12})
    cusp1 = snapshot["cusps"][0]["kp"]["sub_lord"]
    cusp8 = snapshot["cusps"][7]["kp"]["sub_lord"]
    cusp2 = snapshot["cusps"][1]["kp"]["sub_lord"]
    cusp7 = snapshot["cusps"][6]["kp"]["sub_lord"]

    score = 56
    score += asc_score * 3
    score += eighth_score * 3
    score += saturn_score * 2
    score += min(8, sum(item["score"] for item in health_sigs[:2]))
    score -= min(12, sum(item["score"] for item in maraka_sigs[:2]))
    if cusp1 in {asc_lord, eighth_lord, "Saturn"}:
        score += 4
    if cusp8 in {asc_lord, eighth_lord, "Saturn"}:
        score += 4
    if cusp2 in {second_lord, seventh_lord, "Saturn", "Mars", "Rahu", "Ketu"}:
        score -= 4
    if cusp7 in {second_lord, seventh_lord, "Saturn", "Mars", "Rahu", "Ketu"}:
        score -= 4

    challenging_planets = 0
    for name in ("Mars", "Saturn", "Rahu", "Ketu"):
        if snapshot["planets"][name]["whole_sign_house"] in {1, 2, 7, 8, 12}:
            challenging_planets += 1
    score -= challenging_planets * 2

    score = max(20, min(92, score))
    if score < 42:
        label = "Alpayu"
        range_label = "traditionally read as the shorter-span class"
    elif score < 68:
        label = "Madhyayu"
        range_label = "traditionally read as the middle-span class"
    else:
        label = "Poornayu"
        range_label = "traditionally read as the fuller-span class"

    confidence_distance = min(abs(score - 42), abs(score - 68))
    confidence = "high" if confidence_distance >= 10 else "medium" if confidence_distance >= 5 else "guarded"
    synthesis = (
        f"The KP longevity balance leans {label}. This comes from the condition of the ascendant lord ({asc_lord}), the 8th lord ({eighth_lord}), "
        f"Saturn as ayush karaka, and the Placidus cusp sub-lords for houses 1, 2, 7, and 8."
    )
    return {
        "label": label,
        "score": score,
        "range_label": range_label,
        "confidence": confidence,
        "summary": synthesis,
        "drivers": [
            {"factor": f"Ascendant lord: {asc_lord}", "score": asc_score, "notes": asc_reasons},
            {"factor": f"8th lord: {eighth_lord}", "score": eighth_score, "notes": eighth_reasons},
            {"factor": "Saturn as ayush karaka", "score": saturn_score, "notes": saturn_reasons},
            {"factor": "Top longevity significators", "score": sum(item["score"] for item in health_sigs[:3]), "notes": [item["planet"] for item in health_sigs[:3]]},
            {"factor": "Maraka pressure", "score": -sum(item["score"] for item in maraka_sigs[:3]), "notes": [item["planet"] for item in maraka_sigs[:3]]},
        ],
        "supporting_planets": health_sigs[:4],
        "maraka_planets": maraka_sigs[:4],
        "cusp_sub_lords": {
            "house_1": cusp1,
            "house_2": cusp2,
            "house_7": cusp7,
            "house_8": cusp8,
        },
    }


def constitutional_health_profile(snapshot: dict[str, Any]) -> dict[str, Any]:
    scores = {"Vata": 0.0, "Pitta": 0.0, "Kapha": 0.0}
    weighted_bodies = {
        "Ascendant": (snapshot["angles"]["ascendant_sign"], 3.0),
        "Moon": (snapshot["planets"]["Moon"]["sign"], 2.5),
        "Sun": (snapshot["planets"]["Sun"]["sign"], 2.0),
    }
    for _, (sign_name, weight) in weighted_bodies.items():
        scores[SIGN_BODY_PARTS[sign_name]["dosha"]] += weight
    planet_doshas = {
        "Sun": "Pitta",
        "Moon": "Kapha",
        "Mars": "Pitta",
        "Mercury": "Vata",
        "Jupiter": "Kapha",
        "Venus": "Kapha",
        "Saturn": "Vata",
        "Rahu": "Vata",
        "Ketu": "Pitta",
    }
    for planet_name, details in snapshot["planets"].items():
        scores[planet_doshas[planet_name]] += 1.0
        scores[SIGN_BODY_PARTS[str(details["sign"])]["dosha"]] += 0.65
    ranking = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    primary = ranking[0][0]
    secondary = ranking[1][0]
    maintenance = {
        "Vata": [
            "Keep meal and sleep times regular instead of letting the schedule fragment.",
            "Use grounding movement, warm cooked food, hydration, and lower stimulation before sleep.",
            "Watch anxiety-driven overwork, travel fatigue, and excessive fasting.",
        ],
        "Pitta": [
            "Reduce heat accumulation through cooling food, breathwork, and steadier pacing.",
            "Avoid turning ambition into inflammation, acidity, or irritability.",
            "Protect the liver, blood pressure, and stress recovery cycles during intense work periods.",
        ],
        "Kapha": [
            "Keep the body moving every day so heaviness does not become stagnation.",
            "Watch sugar, emotional eating, congestion, and long sedentary spells.",
            "Use light dinners, circulation-building exercise, and early intervention for swelling or sluggishness.",
        ],
    }
    return {
        "primary_prakriti": primary,
        "secondary_prakriti": secondary,
        "dosha_scores": {key: round(value, 2) for key, value in scores.items()},
        "summary": f"{PRAKRITI_DESCRIPTIONS[primary]} {PRAKRITI_DESCRIPTIONS[secondary]}",
        "maintenance_priorities": maintenance[primary],
    }


def vulnerable_systems(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    asc_sign = snapshot["angles"]["ascendant_sign"]
    candidates: list[dict[str, Any]] = []
    health_houses = {1, 6, 8, 12}
    for house in sorted(health_houses):
        cusp = snapshot["cusps"][house - 1]
        sign_name = str(cusp["sign"])
        house_lord = str(cusp["sign_lord"])
        house_pressure = 2
        occupants = [planet for planet, details in snapshot["planets"].items() if details["whole_sign_house"] == house]
        malefic_occupants = [planet for planet in occupants if planet in MALEFICS]
        if occupants:
            house_pressure += len(occupants)
        if malefic_occupants:
            house_pressure += len(malefic_occupants)
        lord_house = int(snapshot["planets"][house_lord]["whole_sign_house"])
        if lord_house in {6, 8, 12}:
            house_pressure += 2
        candidates.append(
            {
                "title": f"House {house}: {HOUSE_HEALTH_DOMAINS[house]}",
                "body_system": SIGN_BODY_PARTS[sign_name]["system"],
                "linked_sign": sign_name,
                "linked_house": house,
                "linked_planet": house_lord,
                "severity_score": house_pressure,
                "indicators": [
                    f"Cusp sign {sign_name} rules {SIGN_BODY_PARTS[sign_name]['system']}.",
                    f"House lord {house_lord} sits in house {lord_house}.",
                    *([f"Occupants: {', '.join(occupants)}."] if occupants else ["No natal occupant, so the cusp lord carries more of the story."]),
                ],
                "prevention_focus": f"Monitor {PLANET_HEALTH_DOMAINS[house_lord]} themes and support {SIGN_BODY_PARTS[sign_name]['system']} proactively.",
            }
        )
    for planet_name, details in snapshot["planets"].items():
        if details["whole_sign_house"] not in {6, 8, 12}:
            continue
        candidates.append(
            {
                "title": f"{planet_name} in house {details['whole_sign_house']}",
                "body_system": PLANET_HEALTH_DOMAINS[planet_name],
                "linked_sign": details["sign"],
                "linked_house": int(details["whole_sign_house"]),
                "linked_planet": planet_name,
                "severity_score": 4 + (2 if planet_name in MALEFICS else 0),
                "indicators": [
                    f"{planet_name} occupies the {'disease' if details['whole_sign_house'] == 6 else 'longevity' if details['whole_sign_house'] == 8 else 'loss/rest'} house.",
                    f"It acts through {details['sign']} ({SIGN_BODY_PARTS[details['sign']]['system']}).",
                    f"KP chain: {details['kp']['nakshatra_lord']} -> {details['kp']['sub_lord']} -> {details['kp']['sub_sub_lord']}.",
                ],
                "prevention_focus": f"Preventive care should watch {PLANET_HEALTH_DOMAINS[planet_name]} themes before they become chronic.",
            }
        )
    unique: dict[str, dict[str, Any]] = {}
    for item in sorted(candidates, key=lambda value: (-int(value["severity_score"]), str(value["title"]))):
        key = f"{item['title']}::{item['linked_house']}::{item['linked_planet']}"
        if key not in unique:
            unique[key] = item
    return list(unique.values())[:6]


def dasha_health_intensity(snapshot: dict[str, Any], planet_name: str) -> int:
    relevance = house_relevance_for_planet(snapshot, planet_name)
    return relevance["1"] + relevance["6"] + relevance["8"] + relevance["12"]


def risk_score_for_date(snapshot: dict[str, Any], timeline: dict[str, Any], target_date: date) -> dict[str, Any] | None:
    timezone_name = snapshot["input"]["timezone"]
    transits = transit_snapshot(target_date, timezone_name)
    dasha = current_dasha_periods(timeline, target_date)
    asc_sign = snapshot["angles"]["ascendant_sign"]
    risk = 0
    reasons: list[str] = []
    maha_lord = str(dasha["maha_dasha"]["planet"])
    antar_lord = str(dasha["antar_dasha"]["planet"])
    maha_weight = dasha_health_intensity(snapshot, maha_lord)
    antar_weight = dasha_health_intensity(snapshot, antar_lord)
    risk += maha_weight + antar_weight
    if maha_weight >= 4:
        reasons.append(f"Maha dasha lord {maha_lord} is strongly tied to houses 1/6/8/12.")
    if antar_weight >= 3:
        reasons.append(f"Antar dasha lord {antar_lord} is activating health houses.")

    sensitive_points = {
        "Ascendant": snapshot["angles"]["ascendant_longitude"],
        "Moon": snapshot["planets"]["Moon"]["longitude"],
        "8th cusp": snapshot["cusps"][7]["longitude"],
    }
    for body in ("Mars", "Saturn", "Rahu", "Ketu"):
        details = transits["planets"][body]
        transit_house = house_from_sign(str(details["sign"]), asc_sign)
        if transit_house in {1, 6, 8, 12}:
            risk += 2
            reasons.append(f"Transiting {body} is moving through house {transit_house}.")
        for label, point in sensitive_points.items():
            orb = shortest_arc(float(details["longitude"]), float(point))
            if orb <= 4.0:
                risk += 2 if body in {"Saturn", "Mars"} else 1
                reasons.append(f"Transiting {body} is within {orb:.1f}° of the natal {label}.")

    if risk < 7:
        return None

    severity = "high" if risk >= 12 else "elevated" if risk >= 9 else "watch"
    return {
        "date": target_date.isoformat(),
        "risk_score": risk,
        "severity": severity,
        "maha_dasha": maha_lord,
        "antar_dasha": antar_lord,
        "reasons": reasons[:4],
    }


def merge_risk_windows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not items:
        return []
    ordered = sorted(items, key=lambda item: item["date"])
    windows: list[dict[str, Any]] = []
    current = dict(ordered[0])
    current["start_date"] = current["date"]
    current["end_date"] = current["date"]
    current["peak_score"] = current["risk_score"]
    for item in ordered[1:]:
        previous = date.fromisoformat(current["end_date"])
        target = date.fromisoformat(item["date"])
        if target <= previous + timedelta(days=14):
            current["end_date"] = item["date"]
            if item["risk_score"] >= current["peak_score"]:
                current["peak_score"] = item["risk_score"]
                current["severity"] = item["severity"]
                current["reasons"] = item["reasons"]
                current["maha_dasha"] = item["maha_dasha"]
                current["antar_dasha"] = item["antar_dasha"]
        else:
            windows.append(current)
            current = dict(item)
            current["start_date"] = current["date"]
            current["end_date"] = current["date"]
            current["peak_score"] = current["risk_score"]
    windows.append(current)
    return windows


def disease_susceptibility_windows(snapshot: dict[str, Any], timeline: dict[str, Any], reference_date: date) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for offset in range(0, DEFAULT_LOOKAHEAD_DAYS, 7):
        candidate = risk_score_for_date(snapshot, timeline, reference_date + timedelta(days=offset))
        if candidate:
            hits.append(candidate)
    windows = merge_risk_windows(hits)
    output: list[dict[str, Any]] = []
    for item in windows[:6]:
        output.append(
            {
                "start_date": item["start_date"],
                "end_date": item["end_date"],
                "severity": item["severity"],
                "peak_score": int(item["peak_score"]),
                "dasha": {
                    "maha": item["maha_dasha"],
                    "antar": item["antar_dasha"],
                },
                "headline": f"{item['severity'].title()} sensitivity window under {item['maha_dasha']} / {item['antar_dasha']}.",
                "why_it_matters": item["reasons"],
                "care_note": "Use these windows for earlier testing, sleep protection, reduced overload, and faster medical escalation if symptoms appear.",
            }
        )
    return output


def critical_period_alerts(snapshot: dict[str, Any], timeline: dict[str, Any], reference_date: date) -> list[dict[str, Any]]:
    alerts: list[dict[str, Any]] = []
    asc_point = float(snapshot["angles"]["ascendant_longitude"])
    moon_point = float(snapshot["planets"]["Moon"]["longitude"])
    point_22nd_drekkana = normalize_longitude(asc_point + 210.0)
    point_64th_navamsa = normalize_longitude(moon_point + 210.0)
    maraka_lords = {snapshot["house_lords"]["2"], snapshot["house_lords"]["7"]}

    current = current_dasha_periods(timeline, reference_date)
    for role, lord in (("Maha", current["maha_dasha"]["planet"]), ("Antar", current["antar_dasha"]["planet"])):
        if lord in maraka_lords:
            alerts.append(
                {
                    "type": "Maraka dasha activation",
                    "severity": "elevated",
                    "date": reference_date.isoformat(),
                    "detail": f"{role} dasha lord {lord} is a maraka lord from the 2nd/7th axis.",
                    "support": "Use this as a caution period for preventive health discipline rather than as a fatalistic prediction.",
                }
            )

    for offset in range(DEFAULT_LOOKAHEAD_DAYS):
        target = reference_date + timedelta(days=offset)
        transits = transit_snapshot(target, snapshot["input"]["timezone"], bodies=("Mars", "Saturn", "Rahu", "Ketu"))
        for body in ("Mars", "Saturn", "Rahu", "Ketu"):
            longitude_value = float(transits["planets"][body]["longitude"])
            orb_22 = shortest_arc(longitude_value, point_22nd_drekkana)
            orb_64 = shortest_arc(longitude_value, point_64th_navamsa)
            if orb_22 <= 2.2:
                alerts.append(
                    {
                        "type": "22nd Drekkana contact",
                        "severity": "high" if body in {"Mars", "Saturn"} else "elevated",
                        "date": target.isoformat(),
                        "detail": f"{body} comes within {orb_22:.1f}° of the 22nd Drekkana sensitive point ({format_degree(point_22nd_drekkana)}).",
                        "support": "Treat this as a high-maintenance period for fatigue, accidents, inflammation, and reckless overexertion.",
                    }
                )
            if orb_64 <= 2.0:
                alerts.append(
                    {
                        "type": "64th Navamsa from Moon",
                        "severity": "high" if body in {"Saturn", "Rahu"} else "elevated",
                        "date": target.isoformat(),
                        "detail": f"{body} comes within {orb_64:.1f}° of the Moon's 64th Navamsa point ({format_degree(point_64th_navamsa)}).",
                        "support": "Mental, hormonal, sleep, and immunity patterns may need tighter care when this point is sensitized.",
                    }
                )
        if len(alerts) >= 6:
            break
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in alerts:
        key = f"{item['type']}::{item['date']}::{item['detail']}"
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped[:6]


def decade_quality_forecast(snapshot: dict[str, Any], timeline: dict[str, Any], reference_date: date) -> list[dict[str, Any]]:
    birth_date = date.fromisoformat(snapshot["input"]["date_of_birth"])
    current_age = max(0, int((reference_date - birth_date).days // 365.25))
    decades: list[dict[str, Any]] = []
    for start_age in range(0, 81, 10):
        start_day = birth_date + timedelta(days=int(start_age * 365.25))
        end_age = start_age + 9 if start_age < 80 else 89
        end_day = birth_date + timedelta(days=int((end_age + 1) * 365.25) - 1)
        overlap_score = 50.0
        active_lords: list[str] = []
        for maha in timeline["maha_dashas"]:
            maha_start = date.fromisoformat(maha["start"])
            maha_end = date.fromisoformat(maha["end"])
            if maha_end < start_day or maha_start > end_day:
                continue
            active_lords.append(str(maha["planet"]))
            health_intensity = dasha_health_intensity(snapshot, str(maha["planet"]))
            if str(maha["planet"]) in BENEFICS:
                overlap_score += 6 - (health_intensity * 0.4)
            elif str(maha["planet"]) in MALEFICS:
                overlap_score -= 4 + (health_intensity * 0.45)
            else:
                overlap_score += 1
        overlap_score = max(18, min(86, round(overlap_score)))
        if overlap_score >= 68:
            quality = "supportive"
            focus = "recovery, consolidation, and more graceful functioning"
        elif overlap_score >= 48:
            quality = "mixed"
            focus = "moderation, regular health routines, and better timing"
        else:
            quality = "sensitive"
            focus = "prevention, rest, and earlier intervention"
        unique_lords = ", ".join(dict.fromkeys(active_lords[:4])) or "birth conditioning"
        decades.append(
            {
                "age_band": f"{start_age}-{end_age}" if start_age < 80 else "80+",
                "quality_score": int(overlap_score),
                "quality": quality,
                "focus": focus,
                "dominant_dashas": unique_lords,
                "current_decade": start_age <= current_age <= end_age if start_age < 80 else current_age >= 80,
                "note": f"This decade is primarily colored by {unique_lords}, so health outcomes improve when life pace matches the chart's timing rather than fighting it.",
            }
        )
    return decades


def remedial_guidance(snapshot: dict[str, Any], longevity: dict[str, Any], prakriti: dict[str, Any], vulnerabilities: list[dict[str, Any]]) -> dict[str, Any]:
    supporting = longevity["supporting_planets"][:3]
    maraka = longevity["maraka_planets"][:3]
    primary = prakriti["primary_prakriti"]
    dominant_vulnerability = vulnerabilities[0] if vulnerabilities else None
    mantras = {
        "Saturn": "Om Sham Shanicharaya Namah",
        "Mars": "Om Kraam Kreem Kraum Sah Bhaumaya Namah",
        "Rahu": "Om Raam Rahave Namah",
        "Ketu": "Om Kem Ketave Namah",
        "Sun": "Om Hram Hreem Hraum Suryaya Namah",
        "Moon": "Om Som Somaya Namah",
        "Mercury": "Om Bum Budhaya Namah",
        "Jupiter": "Om Brim Brihaspataye Namah",
        "Venus": "Om Shum Shukraya Namah",
    }
    balancing = {
        "Vata": "prioritize warmth, oiling, nervous-system rest, and predictable routines",
        "Pitta": "prioritize cooling food, hydration, liver care, and de-escalation of conflict",
        "Kapha": "prioritize movement, lighter food, circulation, and reducing stagnation",
    }
    return {
        "preventive_guidance": [
            f"Primary constitutional rule: {balancing[primary]}.",
            "Use the report's elevated windows for checkups, labs, sleep discipline, and reduced physical overreach.",
            "If symptoms are persistent, unusual, rapidly worsening, or severe, move to qualified medical care immediately instead of relying on spiritual timing.",
        ],
        "planetary_remedies": [
            {
                "planet": item["planet"],
                "why": f"{item['planet']} is a key longevity significator through houses {', '.join(str(h) for h in item['houses'])}.",
                "mantra": mantras[item["planet"]],
            }
            for item in supporting
        ],
        "risk_management": [
            {
                "planet": item["planet"],
                "why": f"{item['planet']} is showing maraka or depletion pressure through houses {', '.join(str(h) for h in item['houses'])}.",
                "advice": "Lower excess, avoid avoidable stress peaks, and do not ignore recurring symptoms during its dasha or transit activation.",
            }
            for item in maraka
        ],
        "body_focus": dominant_vulnerability["prevention_focus"] if dominant_vulnerability else "Protect the constitution through sleep, digestion, circulation, and steady medical follow-through.",
    }


def build_summary(snapshot: dict[str, Any], longevity: dict[str, Any], prakriti: dict[str, Any], vulnerabilities: list[dict[str, Any]]) -> str:
    dominant = vulnerabilities[0]["body_system"] if vulnerabilities else "constitution and recovery systems"
    return (
        f"{longevity['label']} longevity signatures are present, with a {prakriti['primary_prakriti']} leaning constitution. "
        f"The chart asks for stronger attention to {dominant}, especially during maraka-linked or health-house dasha activations."
    )


def compute_longevity_report(payload: ReportInput) -> dict[str, Any]:
    snapshot = build_birth_snapshot(payload)
    reference_date = parse_reference_date(payload.reference_date, payload.timezone_name)
    timeline = build_vimshottari_timeline(float(snapshot["planets"]["Moon"]["longitude"]), local_datetime(payload.date_of_birth, payload.time_of_birth, payload.timezone_name))
    dasha_now = current_dasha_periods(timeline, reference_date)
    longevity = longevity_classification(snapshot)
    prakriti = constitutional_health_profile(snapshot)
    vulnerabilities = vulnerable_systems(snapshot)
    susceptibility = disease_susceptibility_windows(snapshot, timeline, reference_date)
    alerts = critical_period_alerts(snapshot, timeline, reference_date)
    decades = decade_quality_forecast(snapshot, timeline, reference_date)
    remedies = remedial_guidance(snapshot, longevity, prakriti, vulnerabilities)
    summary = build_summary(snapshot, longevity, prakriti, vulnerabilities)

    return {
        "engine_version": KP_MODEL_VERSION,
        "generated_for_date": reference_date.isoformat(),
        "medical_disclaimer": MEDICAL_DISCLAIMER,
        "summary": summary,
        "birth_snapshot": snapshot,
        "current_dasha": dasha_now,
        "vimshottari_timeline": timeline,
        "longevity_classification": longevity,
        "constitutional_health_profile": prakriti,
        "vulnerable_systems": vulnerabilities,
        "disease_susceptibility_windows": susceptibility,
        "critical_period_alerts": alerts,
        "remedial_guidance": remedies,
        "decade_quality_forecast": decades,
    }
