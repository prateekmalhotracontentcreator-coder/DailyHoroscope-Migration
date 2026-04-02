from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from typing import Any, Callable
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import HTTPException, Request
import swisseph as swe


SIDEREAL_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
swe.set_sid_mode(swe.SIDM_LAHIRI)

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
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
}

NAKSHATRAS = [
    {"name": "Ashwini", "lord": "Ketu", "dasha_years": 7},
    {"name": "Bharani", "lord": "Venus", "dasha_years": 20},
    {"name": "Krittika", "lord": "Sun", "dasha_years": 6},
    {"name": "Rohini", "lord": "Moon", "dasha_years": 10},
    {"name": "Mrigashira", "lord": "Mars", "dasha_years": 7},
    {"name": "Ardra", "lord": "Rahu", "dasha_years": 18},
    {"name": "Punarvasu", "lord": "Jupiter", "dasha_years": 16},
    {"name": "Pushya", "lord": "Saturn", "dasha_years": 19},
    {"name": "Ashlesha", "lord": "Mercury", "dasha_years": 17},
    {"name": "Magha", "lord": "Ketu", "dasha_years": 7},
    {"name": "Purva Phalguni", "lord": "Venus", "dasha_years": 20},
    {"name": "Uttara Phalguni", "lord": "Sun", "dasha_years": 6},
    {"name": "Hasta", "lord": "Moon", "dasha_years": 10},
    {"name": "Chitra", "lord": "Mars", "dasha_years": 7},
    {"name": "Swati", "lord": "Rahu", "dasha_years": 18},
    {"name": "Vishakha", "lord": "Jupiter", "dasha_years": 16},
    {"name": "Anuradha", "lord": "Saturn", "dasha_years": 19},
    {"name": "Jyeshtha", "lord": "Mercury", "dasha_years": 17},
    {"name": "Mula", "lord": "Ketu", "dasha_years": 7},
    {"name": "Purva Ashadha", "lord": "Venus", "dasha_years": 20},
    {"name": "Uttara Ashadha", "lord": "Sun", "dasha_years": 6},
    {"name": "Shravana", "lord": "Moon", "dasha_years": 10},
    {"name": "Dhanishtha", "lord": "Mars", "dasha_years": 7},
    {"name": "Shatabhisha", "lord": "Rahu", "dasha_years": 18},
    {"name": "Purva Bhadrapada", "lord": "Jupiter", "dasha_years": 16},
    {"name": "Uttara Bhadrapada", "lord": "Saturn", "dasha_years": 19},
    {"name": "Revati", "lord": "Mercury", "dasha_years": 17},
]

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

PLANET_NATURES = {
    "Sun": "mild_malefic",
    "Moon": "benefic",
    "Mercury": "benefic",
    "Venus": "benefic",
    "Mars": "malefic",
    "Jupiter": "benefic",
    "Saturn": "malefic",
    "Rahu": "malefic",
    "Ketu": "malefic",
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

ENEMY_SIGNS = {
    "Sun": {"Taurus", "Libra", "Capricorn", "Aquarius"},
    "Moon": {"Gemini", "Virgo"},
    "Mars": {"Gemini", "Virgo"},
    "Mercury": {"Cancer"},
    "Jupiter": {"Taurus", "Gemini", "Virgo", "Libra"},
    "Venus": {"Cancer", "Leo"},
    "Saturn": {"Cancer", "Leo", "Scorpio"},
}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")
    return db


def get_user_email(request: Request) -> str:
    user = getattr(request.state, "user", None)
    if not isinstance(user, dict) or not user.get("email"):
        raise HTTPException(status_code=401, detail="Authentication required")
    return str(user["email"]).strip().lower()


def get_report_collection(db):
    collection = getattr(db, "individual_reports", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="individual_reports collection unavailable")
    return collection


def get_engine_subscription_collection(db):
    collection = getattr(db, "ritual_engine_subscriptions", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="ritual_engine_subscriptions collection unavailable")
    return collection


def get_engine_log_collection(db):
    collection = getattr(db, "ritual_engine_trigger_log", None)
    if collection is None:
        raise HTTPException(status_code=500, detail="ritual_engine_trigger_log collection unavailable")
    return collection


def normalize_longitude(value: float) -> float:
    return value % 360.0


def shortest_arc(angle_a: float, angle_b: float) -> float:
    distance = abs(normalize_longitude(angle_a) - normalize_longitude(angle_b))
    return min(distance, 360.0 - distance)


def signed_arc(angle_a: float, angle_b: float) -> float:
    return ((normalize_longitude(angle_a) - normalize_longitude(angle_b) + 180.0) % 360.0) - 180.0


def sign_from_longitude(longitude: float) -> str:
    return SIGN_ORDER[int(normalize_longitude(longitude) // 30)]


def sign_index(sign: str) -> int:
    return SIGN_ORDER.index(sign)


def degree_in_sign(longitude: float) -> float:
    return round(normalize_longitude(longitude) % 30.0, 2)


def local_datetime(date_text: str, time_text: str, timezone_name: str) -> datetime:
    try:
        target_date = date.fromisoformat(date_text)
        hour_text, minute_text = time_text.split(":", 1)
        target_time = time(hour=int(hour_text), minute=int(minute_text))
    except ValueError as err:
        raise HTTPException(status_code=400, detail="Invalid date/time format") from err
    try:
        return datetime.combine(target_date, target_time, tzinfo=ZoneInfo(timezone_name))
    except Exception as err:  # pragma: no cover - timezone data is environment-specific
        raise HTTPException(status_code=400, detail="Invalid timezone") from err


def local_noon(target_date: date, timezone_name: str) -> datetime:
    try:
        return datetime.combine(target_date, time(hour=12), tzinfo=ZoneInfo(timezone_name))
    except Exception as err:  # pragma: no cover
        raise HTTPException(status_code=400, detail="Invalid timezone") from err


def julian_day(moment: datetime) -> float:
    moment_utc = moment.astimezone(timezone.utc)
    hour_value = moment_utc.hour + (moment_utc.minute / 60.0) + (moment_utc.second / 3600.0)
    return swe.julday(moment_utc.year, moment_utc.month, moment_utc.day, hour_value)


def sidereal_longitude_and_speed(jd_ut: float, body: str) -> tuple[float, float]:
    if body == "Ketu":
        rahu_longitude, rahu_speed = sidereal_longitude_and_speed(jd_ut, "Rahu")
        return normalize_longitude(rahu_longitude + 180.0), rahu_speed
    result = swe.calc_ut(jd_ut, PLANET_IDS[body], SIDEREAL_FLAGS)[0]
    return normalize_longitude(result[0]), float(result[3])


def sidereal_longitude(jd_ut: float, body: str) -> float:
    return sidereal_longitude_and_speed(jd_ut, body)[0]


def ascendant_longitude(jd_ut: float, latitude: float, longitude: float) -> float:
    _, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b"W", SIDEREAL_FLAGS)
    return normalize_longitude(ascmc[0])


def midheaven_longitude(jd_ut: float, latitude: float, longitude: float) -> float:
    _, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b"W", SIDEREAL_FLAGS)
    return normalize_longitude(ascmc[1])


def get_house_number(sign_name: str, ascendant_sign: str) -> int:
    return ((sign_index(sign_name) - sign_index(ascendant_sign)) % 12) + 1


def planet_house_from_longitude(planet_longitude: float, ascendant_sign: str) -> int:
    return get_house_number(sign_from_longitude(planet_longitude), ascendant_sign)


def whole_sign_house_signs(ascendant_sign: str) -> dict[int, str]:
    start_index = sign_index(ascendant_sign)
    return {house_num: SIGN_ORDER[(start_index + house_num - 1) % 12] for house_num in range(1, 13)}


def house_lord_for_house(house_num: int, ascendant_sign: str) -> str:
    return SIGN_LORDS[whole_sign_house_signs(ascendant_sign)[house_num]]


def house_sign_longitude_range(ascendant_sign: str, house_num: int) -> tuple[float, float]:
    house_sign = whole_sign_house_signs(ascendant_sign)[house_num]
    start = sign_index(house_sign) * 30.0
    end = start + 30.0
    return start, end


def get_nakshatra(longitude: float) -> dict[str, Any]:
    span = 360.0 / 27.0
    index = int(normalize_longitude(longitude) // span)
    pada = int((normalize_longitude(longitude) % span) // (span / 4.0)) + 1
    nakshatra = NAKSHATRAS[index]
    return {
        "name": nakshatra["name"],
        "lord": nakshatra["lord"],
        "pada": pada,
        "dasha_years": nakshatra["dasha_years"],
        "index": index,
    }


def build_natal_snapshot(
    *,
    date_text: str,
    time_text: str,
    latitude: float,
    longitude: float,
    timezone_name: str,
    city_name: str | None = None,
) -> dict[str, Any]:
    birth_local = local_datetime(date_text, time_text, timezone_name)
    jd_ut = julian_day(birth_local)
    asc_long = ascendant_longitude(jd_ut, latitude, longitude)
    mc_long = midheaven_longitude(jd_ut, latitude, longitude)
    asc_sign = sign_from_longitude(asc_long)
    houses = whole_sign_house_signs(asc_sign)
    planets: dict[str, Any] = {}
    for body in ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"):
        longitude_value, speed_value = sidereal_longitude_and_speed(jd_ut, body)
        sign_name = sign_from_longitude(longitude_value)
        planets[body] = {
            "longitude": longitude_value,
            "sign": sign_name,
            "degree": degree_in_sign(longitude_value),
            "house": get_house_number(sign_name, asc_sign),
            "retrograde": speed_value < 0,
            "speed": speed_value,
            "nakshatra": get_nakshatra(longitude_value),
        }
    return {
        "input": {
            "date": date_text,
            "time": time_text,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone_name,
            "city_name": city_name,
        },
        "julian_day_ut": jd_ut,
        "ascendant_longitude": asc_long,
        "ascendant_sign": asc_sign,
        "ascendant_degree": degree_in_sign(asc_long),
        "midheaven_longitude": mc_long,
        "midheaven_sign": sign_from_longitude(mc_long),
        "midheaven_degree": degree_in_sign(mc_long),
        "houses": houses,
        "house_lords": {house_num: SIGN_LORDS[sign_name] for house_num, sign_name in houses.items()},
        "planets": planets,
        "moon_nakshatra": planets["Moon"]["nakshatra"],
    }


def build_transit_snapshot(target_date: date, timezone_name: str, *, bodies: tuple[str, ...] | None = None) -> dict[str, Any]:
    bodies = bodies or ("Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn")
    moment_local = local_noon(target_date, timezone_name)
    jd_ut = julian_day(moment_local)
    result: dict[str, Any] = {"check_date": target_date.isoformat(), "julian_day_ut": jd_ut, "planets": {}}
    for body in bodies:
        longitude_value, speed_value = sidereal_longitude_and_speed(jd_ut, body)
        result["planets"][body] = {
            "longitude": longitude_value,
            "speed": speed_value,
            "sign": sign_from_longitude(longitude_value),
            "degree": degree_in_sign(longitude_value),
            "retrograde": speed_value < 0,
        }
    return result


def truncate_text(text: str, max_chars: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= max_chars:
        return normalized
    clipped = normalized[: max_chars - 1].rstrip(" ,;:-")
    return f"{clipped}…"


def truncate_words(text: str, max_words: int) -> str:
    normalized = " ".join(text.split())
    words = normalized.split(" ")
    if len(words) <= max_words:
        return normalized
    return " ".join(words[:max_words]).rstrip(" ,;:-") + "…"


def house_topic(house_num: int) -> str:
    topics = {
        1: "identity and self-direction",
        2: "income, values, and voice",
        3: "communication and courage",
        4: "home, roots, and emotional foundation",
        5: "creativity, romance, and self-expression",
        6: "work, pressure, and repair",
        7: "partnerships and commitment",
        8: "intimacy, power, and deep transformation",
        9: "faith, mentors, and worldview",
        10: "career, status, and public path",
        11: "networks, gains, and future hopes",
        12: "rest, retreat, and the unconscious",
    }
    return topics[house_num]


def atmakaraka_planet(planets: dict[str, Any]) -> tuple[str, float]:
    eligible = [(body, details["degree"]) for body, details in planets.items() if body not in {"Rahu", "Ketu"}]
    return max(eligible, key=lambda item: item[1])


def vedic_full_aspects_for_planet(planet_name: str, source_house: int) -> set[int]:
    aspects = {((source_house + 6) % 12) + 1}
    if planet_name == "Mars":
        aspects.update({((source_house + 3) % 12) + 1, ((source_house + 7) % 12) + 1})
    elif planet_name == "Jupiter":
        aspects.update({((source_house + 4) % 12) + 1, ((source_house + 8) % 12) + 1})
    elif planet_name == "Saturn":
        aspects.update({((source_house + 2) % 12) + 1, ((source_house + 9) % 12) + 1})
    elif planet_name in {"Rahu", "Ketu"}:
        aspects.update({((source_house + 4) % 12) + 1, ((source_house + 8) % 12) + 1})
    return aspects


def planets_aspecting_house(planets: dict[str, Any], house_num: int) -> list[str]:
    return [
        planet_name
        for planet_name, details in planets.items()
        if house_num in vedic_full_aspects_for_planet(planet_name, int(details["house"]))
    ]


def house_entry_from_longitude(longitude: float, ascendant_sign: str) -> int:
    return get_house_number(sign_from_longitude(longitude), ascendant_sign)


def classify_planet_condition(planet_name: str, sign_name: str) -> str | None:
    if DEBILITATION_SIGNS.get(planet_name) == sign_name:
        return "debilitated"
    if sign_name in ENEMY_SIGNS.get(planet_name, set()):
        return "enemy_sign"
    return None


def planets_with_shadow_pressure(planets: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for planet_name, details in planets.items():
        if planet_name in {"Rahu", "Ketu"}:
            continue
        condition = classify_planet_condition(planet_name, str(details["sign"]))
        if condition:
            items.append(
                {
                    "planet": planet_name,
                    "sign": details["sign"],
                    "house": details["house"],
                    "condition": condition,
                }
            )
    return items


def closest_aspect(angle: float, aspects: tuple[int, ...] = (0, 60, 90, 120, 180)) -> tuple[int, float]:
    normalized = normalize_longitude(angle)
    matches = [(aspect, shortest_arc(normalized, float(aspect))) for aspect in aspects]
    return min(matches, key=lambda item: item[1])


def aspect_orb(angle_a: float, angle_b: float, target_aspect: float) -> float:
    return abs(shortest_arc(angle_a, angle_b) - target_aspect)


def is_conjunction(angle_a: float, angle_b: float, orb: float) -> bool:
    return shortest_arc(angle_a, angle_b) <= orb


def is_trine(angle_a: float, angle_b: float, orb: float) -> bool:
    return abs(shortest_arc(angle_a, angle_b) - 120.0) <= orb


def orb_label(orb: float, exact_threshold: float = 1.0, close_threshold: float = 3.0) -> str:
    if orb <= exact_threshold:
        return "exact"
    if orb <= close_threshold:
        return "close"
    return "wide"


def smoothstep(edge0: float, edge1: float, value: float) -> float:
    if edge0 == edge1:
        return 0.0
    ratio = max(0.0, min(1.0, (value - edge0) / (edge1 - edge0)))
    return ratio * ratio * (3.0 - 2.0 * ratio)


def clamp_int(value: float, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(round(value))))


def compute_love_battery(moon_longitude: float, natal_venus_longitude: float) -> dict[str, Any]:
    angle = shortest_arc(moon_longitude, natal_venus_longitude)
    aspect, orb = closest_aspect(angle)
    if aspect == 0:
        score = 100.0 - min(25.0, orb * 2.2)
        category = "peak"
        note = "A perfect day for connection."
        description = "The Moon is conjunct your natal Venus"
    elif aspect == 120:
        score = 90.0 - min(12.0, orb * 1.8)
        category = "high"
        note = "Lead with warmth and confidence."
        description = "The Moon is harmonising with your natal Venus through a trine"
    elif aspect == 60:
        score = 84.0 - min(12.0, orb * 1.5)
        category = "high"
        note = "A good day to reach out."
        description = "The Moon is activating your natal Venus through a sextile"
    elif aspect == 90:
        score = 50.0 - min(18.0, orb * 1.5)
        category = "caution"
        note = "Slow down and avoid forcing outcomes."
        description = "The Moon is squaring your natal Venus"
    elif aspect == 180:
        score = 30.0 - min(15.0, orb * 1.5)
        category = "low"
        note = "Choose reflection over pursuit."
        description = "The Moon opposes your natal Venus"
    else:
        score = 58.0 + (smoothstep(0.0, 30.0, 30.0 - min(30.0, orb)) * 7.0)
        category = "neutral"
        note = "Stay steady and nurture what is already present."
        description = "Neutral lunar energy surrounds your natal Venus"
    score_int = clamp_int(score, 15, 100)
    return {
        "love_battery_percent": score_int,
        "score_category": category,
        "moon_natal_venus_angle": round(angle, 1),
        "nearest_aspect": aspect,
        "aspect_orb": round(orb, 1),
        "alignment_description": f"{description} - emotional tone is {'highly receptive' if score_int >= 85 else 'steady' if score_int >= 50 else 'volatile'} today.",
        "action_note": note[:20],
        "notification_worthy": score_int >= 80,
    }


def daterange(start_date: date, end_date: date) -> list[date]:
    if end_date < start_date:
        return []
    return [start_date + timedelta(days=offset) for offset in range((end_date - start_date).days + 1)]


def scan_date_range(start_date: date, days: int, evaluator: Callable[[date], dict[str, Any] | None]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for offset in range(days):
        target = start_date + timedelta(days=offset)
        item = evaluator(target)
        if item:
            results.append(item)
    return results


def merge_consecutive_windows(items: list[dict[str, Any]], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    if not items:
        return []
    ordered = sorted(items, key=lambda item: item["date"])
    windows: list[dict[str, Any]] = []
    current = dict(ordered[0])
    current["start_date"] = current["date"]
    current["end_date"] = current["date"]
    current["peak_orb"] = current.get("orb")
    for item in ordered[1:]:
        same_key = all(item.get(key) == current.get(key) for key in keys)
        previous_date = date.fromisoformat(current["end_date"])
        item_date = date.fromisoformat(item["date"])
        if same_key and item_date == previous_date + timedelta(days=1):
            current["end_date"] = item["date"]
            if item.get("orb") is not None and (current.get("peak_orb") is None or item["orb"] < current["peak_orb"]):
                current["peak_orb"] = item["orb"]
                current["peak_date"] = item["date"]
                current["peak_description"] = item.get("description")
        else:
            current.setdefault("peak_date", current["date"])
            current.setdefault("peak_description", current.get("description"))
            windows.append(current)
            current = dict(item)
            current["start_date"] = current["date"]
            current["end_date"] = current["date"]
            current["peak_orb"] = current.get("orb")
    current.setdefault("peak_date", current["date"])
    current.setdefault("peak_description", current.get("description"))
    windows.append(current)
    return windows


def next_sign_ingress(body: str, from_date: date, timezone_name: str, target_sign: str, max_days: int = 400) -> dict[str, Any] | None:
    previous_sign = None
    for offset in range(max_days + 1):
        target = from_date + timedelta(days=offset)
        transit = build_transit_snapshot(target, timezone_name, bodies=(body,))
        sign_name = transit["planets"][body]["sign"]
        if sign_name == target_sign and previous_sign != target_sign:
            return {"date": target.isoformat(), "days_away": offset, "sign": target_sign}
        previous_sign = sign_name
    return None


def dates_until_sign_exit(body: str, start_date: date, timezone_name: str, active_sign: str, max_days: int = 500) -> str:
    for offset in range(max_days + 1):
        target = start_date + timedelta(days=offset)
        sign_name = build_transit_snapshot(target, timezone_name, bodies=(body,))["planets"][body]["sign"]
        if sign_name != active_sign:
            return (target - timedelta(days=1)).isoformat()
    return (start_date + timedelta(days=max_days)).isoformat()


def dates_since_sign_entry(body: str, from_date: date, timezone_name: str, active_sign: str, max_days: int = 500) -> str:
    for offset in range(max_days + 1):
        target = from_date - timedelta(days=offset)
        sign_name = build_transit_snapshot(target, timezone_name, bodies=(body,))["planets"][body]["sign"]
        if sign_name != active_sign:
            return (target + timedelta(days=1)).isoformat()
    return (from_date - timedelta(days=max_days)).isoformat()


def find_exact_aspect_date(
    *,
    body: str,
    target_longitude: float,
    target_aspect: int,
    start_date: date,
    timezone_name: str,
    max_days: int = 365,
) -> dict[str, Any] | None:
    best: dict[str, Any] | None = None
    for offset in range(max_days + 1):
        target = start_date + timedelta(days=offset)
        body_longitude = build_transit_snapshot(target, timezone_name, bodies=(body,))["planets"][body]["longitude"]
        orb = abs(shortest_arc(body_longitude, target_longitude) - float(target_aspect))
        if best is None or orb < best["orb"]:
            best = {"date": target.isoformat(), "days_away": offset, "orb": round(orb, 2)}
            if orb <= 0.15:
                break
    return best


def normalize_trigger_object(
    *,
    user_email: str,
    trigger_type: str,
    check_date: str,
    intensity: str,
    orb_degrees: float | None,
    alignment_description: str,
    ritual_suggestion: str,
    notification_worthy: bool,
    active_from: str,
    active_until: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    document = {
        "id": str(uuid4()),
        "user_email": user_email,
        "trigger_type": trigger_type,
        "check_date": check_date,
        "intensity": intensity,
        "orb_degrees": round(orb_degrees, 2) if orb_degrees is not None else None,
        "alignment_description": alignment_description,
        "ritual_suggestion": ritual_suggestion,
        "notification_worthy": notification_worthy,
        "active_from": active_from,
        "active_until": active_until,
        "fired_at": now_utc(),
    }
    if extra:
        document.update(extra)
    return document


def compute_first_date_magnet(user_email: str, check_date: date, natal_snapshot: dict[str, Any], transit_snapshot: dict[str, Any]) -> dict[str, Any] | None:
    venus_longitude = transit_snapshot["planets"]["Venus"]["longitude"]
    candidates = [
        ("natal Sun", natal_snapshot["planets"]["Sun"]["longitude"]),
        ("natal Ascendant", natal_snapshot["ascendant_longitude"]),
        ("7th house lord", natal_snapshot["planets"][house_lord_for_house(7, natal_snapshot["ascendant_sign"])]["longitude"]),
    ]
    matches = []
    for label, target_longitude in candidates:
        orb = shortest_arc(venus_longitude, target_longitude)
        if orb <= 5.0:
            matches.append((label, orb))
    if not matches:
        return None
    best_label, best_orb = min(matches, key=lambda item: item[1])
    intensity = "exact" if best_orb <= 1.0 else "close" if best_orb <= 3.0 else "wide"
    return normalize_trigger_object(
        user_email=user_email,
        trigger_type="first_date_magnet",
        check_date=check_date.isoformat(),
        intensity=intensity,
        orb_degrees=best_orb,
        alignment_description=f"Transiting Venus is {best_orb:.1f}° from your {best_label} - your magnetic field is especially noticeable now.",
        ritual_suggestion="Venus Sound Therapy - Chant 'Om Shum Shukraya Namaha' 108 times today. Wear pink or white to amplify your natural magnetism. Step out - you are at your most irresistible.",
        notification_worthy=intensity in {"exact", "close"},
        active_from=check_date.isoformat(),
        active_until=check_date.isoformat(),
        extra={"match_basis": best_label},
    )


def compute_steamy_encounter(user_email: str, check_date: date, natal_snapshot: dict[str, Any], transit_snapshot: dict[str, Any]) -> dict[str, Any] | None:
    mars_longitude = transit_snapshot["planets"]["Mars"]["longitude"]
    natal_venus = natal_snapshot["planets"]["Venus"]["longitude"]
    conjunction_orb = shortest_arc(mars_longitude, natal_venus)
    trine_orb = abs(shortest_arc(mars_longitude, natal_venus) - 120.0)
    eighth_sign = natal_snapshot["houses"][8]
    mars_sign = transit_snapshot["planets"]["Mars"]["sign"]
    best: tuple[str, str, float | None, bool] | None = None
    if conjunction_orb <= 3.0:
        best = ("Mars conjunct natal Venus", "exact" if conjunction_orb <= 2.0 else "wide", conjunction_orb, True)
    if trine_orb <= 3.0 and (best is None or trine_orb < (best[2] or 99.0)):
        best = ("Mars trine natal Venus", "exact" if trine_orb <= 2.0 else "wide", trine_orb, True)
    if mars_sign == eighth_sign:
        ingress_date = dates_since_sign_entry("Mars", check_date, natal_snapshot["input"]["timezone"], eighth_sign)
        days_since_ingress = (check_date - date.fromisoformat(ingress_date)).days
        intensity = "close" if days_since_ingress <= 3 else "wide"
        if best is None or intensity == "close":
            best = ("Mars has entered your natal 8th house", intensity, None, intensity == "close")
    if best is None:
        return None
    label, intensity, orb_value, notify = best
    active_from = check_date.isoformat()
    active_until = check_date.isoformat()
    if label == "Mars has entered your natal 8th house":
        active_from = dates_since_sign_entry("Mars", check_date, natal_snapshot["input"]["timezone"], eighth_sign)
        active_until = dates_until_sign_exit("Mars", check_date, natal_snapshot["input"]["timezone"], eighth_sign)
    return normalize_trigger_object(
        user_email=user_email,
        trigger_type="steamy_encounter",
        check_date=check_date.isoformat(),
        intensity=intensity,
        orb_degrees=orb_value,
        alignment_description=f"{label} - passion, courage, and romantic initiative are running higher than usual.",
        ritual_suggestion="Red Candle Manifestation - Light a red candle and visualise your desire with full clarity. Carry a Garnet or Ruby for confidence and boldness. Act on your instinct - the universe is amplifying your signal.",
        notification_worthy=notify,
        active_from=active_from,
        active_until=active_until,
        extra={"match_basis": label},
    )


def compute_ex_recovery(user_email: str, check_date: date, natal_snapshot: dict[str, Any], transit_snapshot: dict[str, Any]) -> dict[str, Any] | None:
    timezone_name = natal_snapshot["input"]["timezone"]
    fifth_sign = natal_snapshot["houses"][5]
    seventh_sign = natal_snapshot["houses"][7]
    retrograde_hits: list[dict[str, Any]] = []
    for body in ("Venus", "Mercury"):
        transit_body = transit_snapshot["planets"][body]
        if not transit_body["retrograde"]:
            continue
        if transit_body["sign"] in {fifth_sign, seventh_sign}:
            active_from = dates_since_sign_entry(body, check_date, timezone_name, transit_body["sign"])
            active_until = dates_until_sign_exit(body, check_date, timezone_name, transit_body["sign"])
            retrograde_hits.append(
                normalize_trigger_object(
                    user_email=user_email,
                    trigger_type="ex_recovery",
                    check_date=check_date.isoformat(),
                    intensity="close",
                    orb_degrees=None,
                    alignment_description=f"{body} is retrograde in your {'5th' if transit_body['sign'] == fifth_sign else '7th'} house of romance/partnership - old emotions and unfinished stories can resurface.",
                    ritual_suggestion="Full Moon Release - On the next full moon, write the name of an ex or a toxic pattern on paper. Burn it safely to reset and clear your 7th house energy. This window is for releasing, not beginning.",
                    notification_worthy=True,
                    active_from=active_from,
                    active_until=active_until,
                    extra={"planet": body, "active_sign": transit_body["sign"]},
                )
            )
    if retrograde_hits:
        return retrograde_hits[0]
    return None


def compute_long_term_love(user_email: str, check_date: date, natal_snapshot: dict[str, Any], transit_snapshot: dict[str, Any]) -> dict[str, Any] | None:
    jupiter_longitude = transit_snapshot["planets"]["Jupiter"]["longitude"]
    seventh_sign = natal_snapshot["houses"][7]
    jupiter_sign = transit_snapshot["planets"]["Jupiter"]["sign"]
    asc_longitude = natal_snapshot["ascendant_longitude"]
    trine_orb = abs(shortest_arc(jupiter_longitude, asc_longitude) - 120.0)
    if jupiter_sign == seventh_sign:
        ingress_date = dates_since_sign_entry("Jupiter", check_date, natal_snapshot["input"]["timezone"], seventh_sign)
        days_since_ingress = (check_date - date.fromisoformat(ingress_date)).days
        return normalize_trigger_object(
            user_email=user_email,
            trigger_type="long_term_love",
            check_date=check_date.isoformat(),
            intensity="exact" if days_since_ingress <= 7 else "close",
            orb_degrees=0.0,
            alignment_description="Transiting Jupiter has entered your 7th house - a rare long-range partnership season is opening around you.",
            ritual_suggestion="Vastu Reset - Clean the Southwest corner of your bedroom thoroughly. Place a pair of Rose Quartz stones there to anchor the energy of partnership and draw in a lasting bond. This window is rare - act with intention.",
            notification_worthy=True,
            active_from=ingress_date,
            active_until=dates_until_sign_exit("Jupiter", check_date, natal_snapshot["input"]["timezone"], seventh_sign, max_days=450),
            extra={"match_basis": "Jupiter in natal 7th house"},
        )
    if trine_orb <= 5.0:
        intensity = "exact" if trine_orb <= 3.0 else "close"
        return normalize_trigger_object(
            user_email=user_email,
            trigger_type="long_term_love",
            check_date=check_date.isoformat(),
            intensity=intensity,
            orb_degrees=trine_orb,
            alignment_description=f"Transiting Jupiter is forming a supportive trine to your Ascendant with a {trine_orb:.1f}° orb - long-term relationship doors are opening with more grace.",
            ritual_suggestion="Vastu Reset - Clean the Southwest corner of your bedroom thoroughly. Place a pair of Rose Quartz stones there to anchor the energy of partnership and draw in a lasting bond. This window is rare - act with intention.",
            notification_worthy=True,
            active_from=check_date.isoformat(),
            active_until=check_date.isoformat(),
            extra={"match_basis": "Jupiter trine Ascendant"},
        )
    return None


def compose_coach_summary(love_battery: dict[str, Any], active_triggers: list[dict[str, Any]]) -> str:
    if not active_triggers:
        if love_battery["love_battery_percent"] >= 80:
            return "Your emotional radar is unusually strong today. Keep plans light, stay visible, and follow the signal that feels natural."
        if love_battery["love_battery_percent"] <= 40:
            return "Today leans inward. Protect your energy, move slowly with romantic decisions, and let clarity arrive before action."
        return "The field is steady today. Focus on consistency, gentle communication, and strengthening what already feels genuine."
    labels = ", ".join(trigger["trigger_type"].replace("_", " ") for trigger in active_triggers[:2])
    return f"Today carries active love timing through {labels}. Use the moment deliberately, stay grounded, and act where the energy already feels mutual."


def compute_ritual_check(
    *,
    user_email: str,
    check_date: date,
    natal_snapshot: dict[str, Any],
    opted_in: list[str] | None = None,
) -> dict[str, Any]:
    transit_snapshot = build_transit_snapshot(check_date, natal_snapshot["input"]["timezone"])
    opted = set(opted_in or ["first_date_magnet", "steamy_encounter", "ex_recovery", "long_term_love", "lunar_daily_score"])
    love_battery = compute_love_battery(transit_snapshot["planets"]["Moon"]["longitude"], natal_snapshot["planets"]["Venus"]["longitude"])
    love_battery_payload = {
        "trigger_type": "lunar_daily_score",
        "check_date": check_date.isoformat(),
        **love_battery,
    }
    trigger_builders = [
        ("first_date_magnet", compute_first_date_magnet),
        ("steamy_encounter", compute_steamy_encounter),
        ("ex_recovery", compute_ex_recovery),
        ("long_term_love", compute_long_term_love),
    ]
    active_triggers = []
    for trigger_type, builder in trigger_builders:
        if trigger_type not in opted:
            continue
        result = builder(user_email, check_date, natal_snapshot, transit_snapshot)
        if result:
            active_triggers.append(result)
    next_upcoming = find_next_upcoming_trigger(check_date, natal_snapshot, opted_in=list(opted))
    return {
        "user_email": user_email,
        "check_date": check_date.isoformat(),
        "love_battery": love_battery_payload,
        "active_triggers": active_triggers,
        "notification_worthy_triggers": [trigger["trigger_type"] for trigger in active_triggers if trigger["notification_worthy"]] + (["lunar_daily_score"] if "lunar_daily_score" in opted and love_battery["notification_worthy"] else []),
        "coach_summary": compose_coach_summary(love_battery, active_triggers)[:60],
        "next_upcoming_trigger": next_upcoming,
    }


def find_next_upcoming_trigger(check_date: date, natal_snapshot: dict[str, Any], opted_in: list[str] | None = None) -> dict[str, Any] | None:
    timezone_name = natal_snapshot["input"]["timezone"]
    opted = set(opted_in or ["first_date_magnet", "steamy_encounter", "ex_recovery", "long_term_love"])
    candidates: list[dict[str, Any]] = []
    if "first_date_magnet" in opted:
        for label, target_longitude in (
            ("natal Sun", natal_snapshot["planets"]["Sun"]["longitude"]),
            ("natal Ascendant", natal_snapshot["ascendant_longitude"]),
            ("7th house lord", natal_snapshot["planets"][house_lord_for_house(7, natal_snapshot["ascendant_sign"])]["longitude"]),
        ):
            next_date = find_exact_aspect_date(body="Venus", target_longitude=target_longitude, target_aspect=0, start_date=check_date + timedelta(days=1), timezone_name=timezone_name, max_days=120)
            if next_date:
                candidates.append({
                    "trigger_type": "first_date_magnet",
                    "starts_in_days": next_date["days_away"],
                    "preview": f"Venus next perfects a magnetism trigger to your {label} in {next_date['days_away']} days.",
                })
    if "steamy_encounter" in opted:
        next_conj = find_exact_aspect_date(body="Mars", target_longitude=natal_snapshot["planets"]["Venus"]["longitude"], target_aspect=0, start_date=check_date + timedelta(days=1), timezone_name=timezone_name, max_days=120)
        next_trine = find_exact_aspect_date(body="Mars", target_longitude=natal_snapshot["planets"]["Venus"]["longitude"], target_aspect=120, start_date=check_date + timedelta(days=1), timezone_name=timezone_name, max_days=120)
        options = [item for item in (next_conj, next_trine) if item]
        if options:
            best = min(options, key=lambda item: item["days_away"])
            candidates.append({
                "trigger_type": "steamy_encounter",
                "starts_in_days": best["days_away"],
                "preview": f"Mars forms a stronger chemistry angle to your natal Venus in {best['days_away']} days.",
            })
    if "long_term_love" in opted:
        next_jupiter = next_sign_ingress("Jupiter", check_date + timedelta(days=1), timezone_name, natal_snapshot["houses"][7], max_days=450)
        if next_jupiter:
            candidates.append({
                "trigger_type": "long_term_love",
                "starts_in_days": next_jupiter["days_away"],
                "preview": f"Jupiter enters your 7th house in {next_jupiter['days_away']} days - prepare for a major love season.",
            })
    if not candidates:
        return None
    return min(candidates, key=lambda item: item["starts_in_days"])


def build_vimshottari_timeline(moon_longitude: float, birth_local: datetime, limit_years: int = 120) -> dict[str, Any]:
    nak = get_nakshatra(moon_longitude)
    start_lord = str(nak["lord"])
    nak_span = 360.0 / 27.0
    nak_start = nak["index"] * nak_span
    fraction_elapsed = (normalize_longitude(moon_longitude) - nak_start) / nak_span
    remaining_years = DASHA_YEARS[start_lord] * (1.0 - fraction_elapsed)
    maha_dashas: list[dict[str, Any]] = []
    cursor = birth_local
    first_end = cursor + timedelta(days=remaining_years * 365.25)
    maha_dashas.append({"planet": start_lord, "start": cursor.date().isoformat(), "end": first_end.date().isoformat(), "years": round(remaining_years, 2)})
    cursor = first_end
    start_index = DASHA_ORDER.index(start_lord)
    elapsed_years = remaining_years
    step = 1
    while elapsed_years < limit_years and len(maha_dashas) < 18:
        lord = DASHA_ORDER[(start_index + step) % len(DASHA_ORDER)]
        years = DASHA_YEARS[lord]
        end = cursor + timedelta(days=years * 365.25)
        maha_dashas.append({"planet": lord, "start": cursor.date().isoformat(), "end": end.date().isoformat(), "years": years})
        cursor = end
        elapsed_years += years
        step += 1
    return {"birth_nakshatra": nak["name"], "birth_nakshatra_lord": start_lord, "maha_dashas": maha_dashas}


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
    if items:
        items[-1]["end"] = end_dt.date().isoformat()
    return items


def current_dasha_periods(timeline: dict[str, Any], on_date: date) -> dict[str, Any]:
    current_maha = timeline["maha_dashas"][-1]
    for maha in timeline["maha_dashas"]:
        if date.fromisoformat(maha["start"]) <= on_date <= date.fromisoformat(maha["end"]):
            current_maha = maha
            break
    antar_dashas = build_antar_dashas(current_maha["planet"], current_maha["start"], current_maha["end"])
    current_antar = antar_dashas[-1]
    for antar in antar_dashas:
        if date.fromisoformat(antar["start"]) <= on_date <= date.fromisoformat(antar["end"]):
            current_antar = antar
            break
    return {
        "maha_dasha": current_maha,
        "antar_dasha": current_antar,
        "antar_dashas": antar_dashas,
    }


def dasha_planet_quality(planet_name: str) -> str:
    nature = PLANET_NATURES.get(planet_name, "mixed")
    if nature == "benefic":
        return "expansion"
    if nature == "malefic":
        return "challenge"
    return "consolidation"


def build_report_document(
    *,
    user_email: str,
    report_type: str,
    report_slug: str,
    input_payload: dict[str, Any],
    output_payload: dict[str, Any],
    summary: str,
) -> dict[str, Any]:
    now = now_utc()
    return {
        "id": str(uuid4()),
        "document_type": "report",
        "report_type": report_type,
        "report_slug": report_slug,
        "user_email": user_email,
        "input_payload": input_payload,
        "output_payload": output_payload,
        "summary": summary,
        "created_at": now,
        "updated_at": now,
    }


def base_history_query(user_email: str, report_type: str) -> dict[str, Any]:
    return {"user_email": user_email, "document_type": "report", "report_type": report_type}
