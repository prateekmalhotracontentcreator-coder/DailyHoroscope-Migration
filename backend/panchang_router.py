from __future__ import annotations

import calendar
import logging
import math
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Literal
from zoneinfo import ZoneInfo

import swisseph as swe
from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field

_log = logging.getLogger("panchang")

router = APIRouter(prefix="/api/panchang", tags=["panchang"])

ENGINE_VERSION = "panchang-router-v33-growth-deploy"
CalendarVariant = Literal["amanta", "purnimanta"]
RegionCode = Literal["general", "north_india", "south_india", "western_india"]
ObservanceType = Literal["festival", "vrat", "observance"]
TimingQuality = Literal["good", "neutral", "caution"]

_SWE_INITIALISED = False

def _init_swe() -> None:
    global _SWE_INITIALISED
    if not _SWE_INITIALISED:
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        _SWE_INITIALISED = True

_init_swe()

_SWE_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

# ---------------------------------------------------------------------------
# Traditional Vedic inauspicious timing slot tables
# Verified against Drik Panchang -- New Delhi, 26 March 2026 (Thu).
# weekday key = Python date.isoweekday(): Mon=1 ... Sun=7
# ---------------------------------------------------------------------------

# Rahu Kaal  -- Sun=8, Mon=2, Tue=7, Wed=5, Thu=6, Fri=4, Sat=3
_RAHU_KAAL_SLOT = {1: 2, 2: 7, 3: 5, 4: 6, 5: 4, 6: 3, 7: 8}

# Yamaganda  -- Sun=5, Mon=4, Tue=3, Wed=2, Thu=1, Fri=7, Sat=6
_YAMAGANDA_SLOT = {1: 4, 2: 3, 3: 2, 4: 1, 5: 7, 6: 6, 7: 5}

# Gulika Kaal -- Sun=7, Mon=6, Tue=5, Wed=4, Thu=3, Fri=2, Sat=1
_GULIKA_SLOT    = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 7}

# Dur Muhurta -- two windows per day (0-indexed Muhurta from sunrise, daylight/15 each)
# Thu verified: Muhurtas 5 & 11 → 10:24 AM and 03:19 PM ✓
_DUR_MUHURTA_MUHURTAS: dict[int, tuple[int, int]] = {
    1: (6, 11),   # Monday
    2: (5,  8),   # Tuesday
    3: (7, 13),   # Wednesday
    4: (5, 11),   # Thursday
    5: (9, 10),   # Friday
    6: (1,  7),   # Saturday
    7: (3,  6),   # Sunday
}

# ---------------------------------------------------------------------------
# True Choghadiya tables
# Each weekday has 8 day slots + 8 night slots.
# weekday key = Python date.isoweekday(): Mon=1 ... Sun=7
# ---------------------------------------------------------------------------
_CHOG_QUALITY: dict[str, TimingQuality] = {
    "Amrit": "good", "Shubh": "good", "Labh": "good",
    "Char": "neutral",
    "Udveg": "caution", "Kaal": "caution", "Rog": "caution",
}
_CHOG_RULER: dict[str, str] = {
    "Amrit": "Moon",   "Shubh": "Jupiter", "Labh": "Mercury",
    "Char":  "Venus",  "Udveg": "Sun",     "Kaal": "Saturn", "Rog": "Mars",
}

_DAY_CHOG: dict[int, list[str]] = {
    7: ["Udveg","Char","Labh","Amrit","Kaal","Shubh","Rog","Udveg"],   # Sunday
    1: ["Amrit","Kaal","Shubh","Rog","Udveg","Char","Labh","Amrit"],   # Monday
    2: ["Rog","Udveg","Char","Labh","Amrit","Kaal","Shubh","Rog"],     # Tuesday
    3: ["Labh","Amrit","Kaal","Shubh","Rog","Udveg","Char","Labh"],    # Wednesday
    4: ["Shubh","Rog","Udveg","Char","Labh","Amrit","Kaal","Shubh"],   # Thursday
    5: ["Char","Labh","Amrit","Kaal","Shubh","Rog","Udveg","Char"],    # Friday
    6: ["Kaal","Shubh","Rog","Udveg","Char","Labh","Amrit","Kaal"],    # Saturday
}
_NIGHT_CHOG: dict[int, list[str]] = {
    7: ["Shubh","Amrit","Char","Rog","Kaal","Labh","Udveg","Shubh"],   # Sunday
    1: ["Char","Rog","Kaal","Labh","Udveg","Shubh","Amrit","Char"],    # Monday
    2: ["Kaal","Labh","Udveg","Shubh","Amrit","Char","Rog","Kaal"],    # Tuesday
    3: ["Rog","Kaal","Labh","Udveg","Shubh","Amrit","Char","Rog"],     # Wednesday
    4: ["Udveg","Shubh","Amrit","Char","Rog","Kaal","Labh","Udveg"],   # Thursday
    5: ["Amrit","Char","Rog","Kaal","Labh","Udveg","Shubh","Amrit"],   # Friday
    6: ["Labh","Udveg","Shubh","Amrit","Char","Rog","Kaal","Labh"],    # Saturday
}

# ---------------------------------------------------------------------------
# Special Yogas -- Nakshatra × Weekday rule tables
# weekday key = Python date.isoweekday(): Mon=1 ... Sun=7
# ---------------------------------------------------------------------------

# Sarvartha Siddhi Yoga -- "All-Purpose Accomplishment"; auspicious for new ventures
_SARVARTHA_SIDDHI: dict[int, set[str]] = {
    7: {"Hasta", "Pushya", "Uttara Phalguni", "Uttara Ashadha", "Uttara Bhadrapada"},
    1: {"Rohini", "Mrigashira", "Punarvasu", "Pushya", "Anuradha", "Shravana"},
    2: {"Ashwini", "Krittika", "Mrigashira", "Chitra", "Dhanishtha", "Shatabhisha"},
    3: {"Krittika", "Rohini", "Anuradha", "Jyeshtha", "Revati"},
    4: {"Vishakha", "Anuradha", "Uttara Phalguni", "Uttara Ashadha", "Uttara Bhadrapada", "Revati", "Pushya"},
    5: {"Anuradha", "Revati", "Ashwini", "Punarvasu", "Shatabhisha"},
    6: {"Rohini", "Swati", "Dhanishtha", "Shravana", "Shatabhisha"},
}

# Amrit Siddhi Yoga -- "Nectar of Accomplishment"; rarest and most auspicious
_AMRIT_SIDDHI: dict[int, str] = {
    7: "Hasta",       # Sunday
    1: "Mrigashira",  # Monday
    2: "Ashwini",     # Tuesday
    3: "Anuradha",    # Wednesday
    4: "Pushya",      # Thursday
    5: "Revati",      # Friday
    6: "Rohini",      # Saturday
}

# Ravi Yoga -- Sun yoga; avoid starting new work (inauspicious)
_RAVI_YOGA: dict[int, set[str]] = {
    7: {"Krittika", "Uttara Phalguni", "Uttara Ashadha"},
    1: {"Hasta", "Shravana"},
    2: {"Ashwini", "Chitra", "Dhanishtha"},
    3: {"Ashlesha", "Jyeshtha", "Revati"},
    4: {"Punarvasu", "Vishakha", "Purva Bhadrapada"},
    5: {"Bharani", "Purva Phalguni", "Purva Ashadha"},
    6: {"Pushya", "Anuradha", "Uttara Bhadrapada"},
}

# Vijaya Muhurta -- weekday-specific Muhurta index from sunrise
_VIJAYA_MUHURTA: dict[int, int] = {
    1:  9,   # Monday
    2:  2,   # Tuesday
    3:  7,   # Wednesday
    4: 10,   # Thursday   ← Drik: 02:30 PM ✓
    5:  4,   # Friday
    6:  3,   # Saturday
    7:  6,   # Sunday
}


class PanchangLocation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    slug: str
    label: str
    city_name: str | None = None
    country: str | None = None
    latitude: float
    longitude: float
    timezone: str
    tz_abbr: str | None = None


class PanchangSegment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    index: int
    start: str | None = None
    end: str | None = None


class PanchangTimingWindow(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str
    start: str
    end: str
    quality: TimingQuality


class PanchangObservance(BaseModel):
    model_config = ConfigDict(extra="ignore")
    slug: str
    name: str
    observance_type: ObservanceType
    date: str
    priority: int = 1
    summary: str


class PanchangLink(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str
    href: str


class PanchangLocationGroup(BaseModel):
    model_config = ConfigDict(extra="ignore")
    country_code: str
    country_name: str
    locations: list[PanchangLocation] = Field(default_factory=list)


class PanchangLocationListResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    groups: list[PanchangLocationGroup] = Field(default_factory=list)


class PanchangSummary(BaseModel):
    model_config = ConfigDict(extra="ignore")
    weekday: str
    tithi: str
    nakshatra: str
    yoga: str
    karana: str
    sunrise: str
    sunset: str
    moonrise: str | None = None
    moonset: str | None = None


class PanchangDetail(BaseModel):
    model_config = ConfigDict(extra="ignore")
    paksha: str
    lunar_month: str
    moon_sign: str
    sun_sign: str
    samvat: str
    tithi: PanchangSegment
    nakshatra: PanchangSegment
    yoga: PanchangSegment
    karana: PanchangSegment


class PanchangLagnaHouse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    house: int
    sign: str
    is_ascendant: bool = False


class PanchangLagnaChart(BaseModel):
    model_config = ConfigDict(extra="ignore")
    ascendant_sign: str
    ascendant_degree: float
    houses: list[PanchangLagnaHouse] = Field(default_factory=list)


class PanchangMeta(BaseModel):
    model_config = ConfigDict(extra="ignore")
    engine_version: str
    generated_at: str
    calendar_variant: CalendarVariant
    region: RegionCode
    persistence_mode: Literal["stateless_v1"]


class SpecialYoga(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str                    # e.g. "Sarvartha Siddhi Yoga"
    quality: TimingQuality       # "good" | "neutral" | "caution"
    nakshatra: str               # triggering nakshatra
    vara: str                    # triggering weekday
    meaning: str                 # one-line description


class PanchangDailyResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: str
    location: PanchangLocation
    summary: PanchangSummary
    panchang: PanchangDetail
    lagna_chart: PanchangLagnaChart | None = None
    special_yogas: list[SpecialYoga] = Field(default_factory=list)
    day_quality_windows: list[PanchangTimingWindow] = Field(default_factory=list)
    observances: list[PanchangObservance] = Field(default_factory=list)
    related_links: list[PanchangLink] = Field(default_factory=list)
    meta: PanchangMeta


class PanchangCalendarDay(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: str
    day: int
    weekday: str
    tithi: str
    observances: list[PanchangObservance] = Field(default_factory=list)


class PanchangCalendarResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    year: int
    month: int
    location: PanchangLocation
    calendar_variant: CalendarVariant
    region: RegionCode
    month_label: str
    days: list[PanchangCalendarDay] = Field(default_factory=list)
    meta: PanchangMeta


class PanchangFestivalListResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    year: int
    month: int | None = None
    location: PanchangLocation
    items: list[PanchangObservance] = Field(default_factory=list)
    meta: PanchangMeta


class ChoghadiyaSlot(BaseModel):
    model_config = ConfigDict(extra="ignore")
    index: int          # 1-8
    name: str           # Amrit / Shubh / Labh / Char / Udveg / Kaal / Rog
    ruler: str          # planet name
    quality: TimingQuality
    start: str          # ISO-format local datetime
    end: str


class ChoghadiyaResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: str
    location: PanchangLocation
    sunrise: str
    sunset: str
    next_sunrise: str
    day_choghadiya: list[ChoghadiyaSlot] = Field(default_factory=list)
    night_choghadiya: list[ChoghadiyaSlot] = Field(default_factory=list)
    meta: PanchangMeta


class HoraSlot(BaseModel):
    model_config = ConfigDict(extra="ignore")
    index: int
    planet: str
    start: str
    end: str
    quality: str
    period: Literal["day", "night"]


class HoraResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: str
    location: PanchangLocation
    sunrise: str
    sunset: str
    next_sunrise: str
    day_hora: list[HoraSlot] = Field(default_factory=list)
    night_hora: list[HoraSlot] = Field(default_factory=list)
    meta: PanchangMeta


class MarriageMuhuratDate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: str
    day_of_week: str
    month: int
    month_label: str
    tithi: str
    nakshatra: str
    lunar_month: str
    quality: Literal["Highly Auspicious", "Auspicious"]
    quality_score: int = Field(default=4, ge=1, le=5)
    notes: str
    panchang_path: str


class MarriageMuhuratMonthSummary(BaseModel):
    model_config = ConfigDict(extra="ignore")
    month: int
    label: str
    count: int


class MarriageMuhuratResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    year: int
    location: PanchangLocation
    count: int
    cached: bool = False
    computed_at: str
    advisory: str
    month_summary: list[MarriageMuhuratMonthSummary] = Field(default_factory=list)
    muhurat_dates: list[MarriageMuhuratDate] = Field(default_factory=list)
    meta: PanchangMeta


# ---------------------------------------------------------------------------
# Location catalogue
# ---------------------------------------------------------------------------
def _build_location_catalog(
    grouped_records: list[tuple[str, str, list[tuple[str, str, float, float, str, str]]]],
) -> tuple[dict[str, "PanchangLocation"], list[dict]]:
    default_locations: dict[str, "PanchangLocation"] = {}
    location_groups: list[dict] = []
    for country_code, country_name, records in grouped_records:
        slugs: list[str] = []
        for slug, city_name, latitude, longitude, timezone_name, tz_abbr in records:
            default_locations[slug] = PanchangLocation(
                slug=slug,
                label=f"{city_name}, {country_name}",
                city_name=city_name,
                country=country_name,
                latitude=latitude,
                longitude=longitude,
                timezone=timezone_name,
                tz_abbr=tz_abbr,
            )
            slugs.append(slug)
        location_groups.append(
            {"country_code": country_code, "country_name": country_name, "slugs": slugs}
        )
    return default_locations, location_groups


GLOBAL_LOCATION_GROUPED_RECORDS: list[tuple[str, str, list[tuple[str, str, float, float, str, str]]]] = [
    ("IN", "India", [
        ("new-delhi-india", "New Delhi", 28.6139, 77.2090, "Asia/Kolkata", "IST"),
        ("mumbai-india", "Mumbai", 19.0760, 72.8777, "Asia/Kolkata", "IST"),
        ("bengaluru-india", "Bengaluru", 12.9716, 77.5946, "Asia/Kolkata", "IST"),
        ("kolkata-india", "Kolkata", 22.5726, 88.3639, "Asia/Kolkata", "IST"),
        ("chennai-india", "Chennai", 13.0827, 80.2707, "Asia/Kolkata", "IST"),
        ("hyderabad-india", "Hyderabad", 17.3850, 78.4867, "Asia/Kolkata", "IST"),
        ("pune-india", "Pune", 18.5204, 73.8567, "Asia/Kolkata", "IST"),
        ("ahmedabad-india", "Ahmedabad", 23.0225, 72.5714, "Asia/Kolkata", "IST"),
        ("surat-india", "Surat", 21.1702, 72.8311, "Asia/Kolkata", "IST"),
        ("jaipur-india", "Jaipur", 26.9124, 75.7873, "Asia/Kolkata", "IST"),
        ("lucknow-india", "Lucknow", 26.8467, 80.9462, "Asia/Kolkata", "IST"),
        ("kanpur-india", "Kanpur", 26.4499, 80.3319, "Asia/Kolkata", "IST"),
        ("nagpur-india", "Nagpur", 21.1458, 79.0882, "Asia/Kolkata", "IST"),
        ("indore-india", "Indore", 22.7196, 75.8577, "Asia/Kolkata", "IST"),
        ("patna-india", "Patna", 25.5941, 85.1376, "Asia/Kolkata", "IST"),
        ("visakhapatnam-india", "Visakhapatnam", 17.6868, 83.2185, "Asia/Kolkata", "IST"),
        ("bhopal-india", "Bhopal", 23.2599, 77.4126, "Asia/Kolkata", "IST"),
        ("ludhiana-india", "Ludhiana", 30.9010, 75.8573, "Asia/Kolkata", "IST"),
        ("agra-india", "Agra", 27.1767, 78.0081, "Asia/Kolkata", "IST"),
        ("nashik-india", "Nashik", 19.9975, 73.7898, "Asia/Kolkata", "IST"),
        ("varanasi-india", "Varanasi", 25.3176, 82.9739, "Asia/Kolkata", "IST"),
        ("meerut-india", "Meerut", 28.9845, 77.7064, "Asia/Kolkata", "IST"),
        ("rajkot-india", "Rajkot", 22.3039, 70.8022, "Asia/Kolkata", "IST"),
        ("vadodara-india", "Vadodara", 22.3072, 73.1812, "Asia/Kolkata", "IST"),
        ("coimbatore-india", "Coimbatore", 11.0168, 76.9558, "Asia/Kolkata", "IST"),
        ("madurai-india", "Madurai", 9.9252, 78.1198, "Asia/Kolkata", "IST"),
        ("faridabad-india", "Faridabad", 28.4089, 77.3178, "Asia/Kolkata", "IST"),
        ("ghaziabad-india", "Ghaziabad", 28.6692, 77.4538, "Asia/Kolkata", "IST"),
        ("vijayawada-india", "Vijayawada", 16.5062, 80.6480, "Asia/Kolkata", "IST"),
        ("kochi-india", "Kochi", 9.9312, 76.2673, "Asia/Kolkata", "IST"),
        ("thiruvananthapuram-india", "Thiruvananthapuram", 8.5241, 76.9366, "Asia/Kolkata", "IST"),
        ("bhubaneswar-india", "Bhubaneswar", 20.2961, 85.8245, "Asia/Kolkata", "IST"),
        ("guwahati-india", "Guwahati", 26.1445, 91.7362, "Asia/Kolkata", "IST"),
        ("amritsar-india", "Amritsar", 31.6340, 74.8723, "Asia/Kolkata", "IST"),
    ]),
    ("US", "United States", [
        ("new-york-usa", "New York", 40.7128, -74.0060, "America/New_York", "ET"),
        ("washington-dc-usa", "Washington, DC", 38.9072, -77.0369, "America/New_York", "ET"),
        ("miami-usa", "Miami", 25.7617, -80.1918, "America/New_York", "ET"),
        ("boston-usa", "Boston", 42.3601, -71.0589, "America/New_York", "ET"),
        ("philadelphia-usa", "Philadelphia", 39.9526, -75.1652, "America/New_York", "ET"),
        ("atlanta-usa", "Atlanta", 33.7490, -84.3880, "America/New_York", "ET"),
        ("detroit-usa", "Detroit", 42.3314, -83.0458, "America/New_York", "ET"),
        ("chicago-usa", "Chicago", 41.8781, -87.6298, "America/Chicago", "CT"),
        ("houston-usa", "Houston", 29.7604, -95.3698, "America/Chicago", "CT"),
        ("dallas-usa", "Dallas", 32.7767, -96.7970, "America/Chicago", "CT"),
        ("san-antonio-usa", "San Antonio", 29.4241, -98.4936, "America/Chicago", "CT"),
        ("minneapolis-usa", "Minneapolis", 44.9778, -93.2650, "America/Chicago", "CT"),
        ("new-orleans-usa", "New Orleans", 29.9511, -90.0715, "America/Chicago", "CT"),
        ("denver-usa", "Denver", 39.7392, -104.9903, "America/Denver", "MT"),
        ("phoenix-usa", "Phoenix", 33.4484, -112.0740, "America/Phoenix", "MST"),
        ("albuquerque-usa", "Albuquerque", 35.0844, -106.6504, "America/Denver", "MT"),
        ("salt-lake-city-usa", "Salt Lake City", 40.7608, -111.8910, "America/Denver", "MT"),
        ("los-angeles-usa", "Los Angeles", 34.0522, -118.2437, "America/Los_Angeles", "PT"),
        ("san-francisco-usa", "San Francisco", 37.7749, -122.4194, "America/Los_Angeles", "PT"),
        ("seattle-usa", "Seattle", 47.6062, -122.3321, "America/Los_Angeles", "PT"),
        ("san-jose-usa", "San Jose", 37.3382, -121.8863, "America/Los_Angeles", "PT"),
        ("las-vegas-usa", "Las Vegas", 36.1699, -115.1398, "America/Los_Angeles", "PT"),
        ("honolulu-usa", "Honolulu", 21.3069, -157.8583, "Pacific/Honolulu", "HST"),
        ("anchorage-usa", "Anchorage", 61.2181, -149.9003, "America/Anchorage", "AKST"),
    ]),
    ("CAN", "Canada", [
        ("toronto-canada", "Toronto", 43.6532, -79.3832, "America/Toronto", "ET"),
        ("montreal-canada", "Montreal", 45.5017, -73.5673, "America/Toronto", "ET"),
        ("ottawa-canada", "Ottawa", 45.4215, -75.6972, "America/Toronto", "ET"),
        ("calgary-canada", "Calgary", 51.0447, -114.0719, "America/Edmonton", "MT"),
        ("edmonton-canada", "Edmonton", 53.5461, -113.4938, "America/Edmonton", "MT"),
        ("vancouver-canada", "Vancouver", 49.2827, -123.1207, "America/Vancouver", "PT"),
        ("winnipeg-canada", "Winnipeg", 49.8951, -97.1384, "America/Winnipeg", "CT"),
        ("halifax-canada", "Halifax", 44.6488, -63.5752, "America/Halifax", "AT"),
    ]),
    ("MEX", "Mexico", [
        ("mexico-city-mexico", "Mexico City", 19.4326, -99.1332, "America/Mexico_City", "CST"),
        ("guadalajara-mexico", "Guadalajara", 20.6597, -103.3496, "America/Mexico_City", "CST"),
        ("monterrey-mexico", "Monterrey", 25.6866, -100.3161, "America/Monterrey", "CST"),
        ("puebla-mexico", "Puebla", 19.0414, -98.2063, "America/Mexico_City", "CST"),
        ("tijuana-mexico", "Tijuana", 32.5149, -117.0382, "America/Tijuana", "PST"),
        ("cancun-mexico", "Cancun", 21.1619, -86.8515, "America/Cancun", "EST"),
        ("merida-mexico", "Merida", 20.9674, -89.5926, "America/Merida", "CST"),
        ("leon-mexico", "Leon", 21.1220, -101.6823, "America/Mexico_City", "CST"),
    ]),
    ("BRA", "Brazil", [
        ("sao-paulo-brazil", "Sao Paulo", -23.5505, -46.6333, "America/Sao_Paulo", "BRT"),
        ("rio-de-janeiro-brazil", "Rio de Janeiro", -22.9068, -43.1729, "America/Sao_Paulo", "BRT"),
        ("brasilia-brazil", "Brasilia", -15.7801, -47.9292, "America/Sao_Paulo", "BRT"),
        ("salvador-brazil", "Salvador", -12.9777, -38.5016, "America/Bahia", "BRT"),
        ("fortaleza-brazil", "Fortaleza", -3.7319, -38.5267, "America/Fortaleza", "BRT"),
        ("recife-brazil", "Recife", -8.0476, -34.8770, "America/Recife", "BRT"),
        ("manaus-brazil", "Manaus", -3.1190, -60.0217, "America/Manaus", "AMT"),
        ("porto-alegre-brazil", "Porto Alegre", -30.0346, -51.2177, "America/Sao_Paulo", "BRT"),
        ("curitiba-brazil", "Curitiba", -25.4284, -49.2733, "America/Sao_Paulo", "BRT"),
        ("belem-brazil", "Belem", -1.4558, -48.4902, "America/Belem", "BRT"),
    ]),
    ("ARG", "Argentina", [
        ("buenos-aires-argentina", "Buenos Aires", -34.6037, -58.3816, "America/Argentina/Buenos_Aires", "ART"),
        ("cordoba-argentina", "Cordoba", -31.4201, -64.1888, "America/Argentina/Cordoba", "ART"),
        ("rosario-argentina", "Rosario", -32.9442, -60.6505, "America/Argentina/Cordoba", "ART"),
        ("mendoza-argentina", "Mendoza", -32.8895, -68.8458, "America/Argentina/Mendoza", "ART"),
    ]),
    ("CHL", "Chile", [
        ("santiago-chile", "Santiago", -33.4489, -70.6693, "America/Santiago", "CLT"),
        ("valparaiso-chile", "Valparaiso", -33.0472, -71.6127, "America/Santiago", "CLT"),
        ("concepcion-chile", "Concepcion", -36.8201, -73.0444, "America/Santiago", "CLT"),
    ]),
    ("PER", "Peru", [
        ("lima-peru", "Lima", -12.0464, -77.0428, "America/Lima", "PET"),
        ("cusco-peru", "Cusco", -13.5319, -71.9675, "America/Lima", "PET"),
        ("arequipa-peru", "Arequipa", -16.4090, -71.5375, "America/Lima", "PET"),
    ]),
    ("COL", "Colombia", [
        ("bogota-colombia", "Bogota", 4.7110, -74.0721, "America/Bogota", "COT"),
        ("medellin-colombia", "Medellin", 6.2442, -75.5812, "America/Bogota", "COT"),
        ("cali-colombia", "Cali", 3.4516, -76.5320, "America/Bogota", "COT"),
        ("barranquilla-colombia", "Barranquilla", 10.9639, -74.7964, "America/Bogota", "COT"),
        ("cartagena-colombia", "Cartagena", 10.3910, -75.4794, "America/Bogota", "COT"),
    ]),
    ("VEN", "Venezuela", [
        ("caracas-venezuela", "Caracas", 10.4806, -66.9036, "America/Caracas", "VET"),
        ("maracaibo-venezuela", "Maracaibo", 10.6545, -71.6440, "America/Caracas", "VET"),
    ]),
    ("ECU", "Ecuador", [
        ("quito-ecuador", "Quito", -0.1807, -78.4678, "America/Guayaquil", "ECT"),
        ("guayaquil-ecuador", "Guayaquil", -2.1709, -79.9224, "America/Guayaquil", "ECT"),
    ]),
    ("BOL", "Bolivia", [
        ("la-paz-bolivia", "La Paz", -16.4897, -68.1193, "America/La_Paz", "BOT"),
        ("santa-cruz-bolivia", "Santa Cruz", -17.7833, -63.1821, "America/La_Paz", "BOT"),
    ]),
    ("PRY", "Paraguay", [
        ("asuncion-paraguay", "Asuncion", -25.2637, -57.5759, "America/Asuncion", "PYT"),
    ]),
    ("URY", "Uruguay", [
        ("montevideo-uruguay", "Montevideo", -34.9011, -56.1645, "America/Montevideo", "UYT"),
    ]),
    ("UK", "United Kingdom", [
        ("london-uk", "London", 51.5072, -0.1276, "Europe/London", "GMT"),
        ("birmingham-uk", "Birmingham", 52.4862, -1.8904, "Europe/London", "GMT"),
        ("manchester-uk", "Manchester", 53.4808, -2.2426, "Europe/London", "GMT"),
        ("glasgow-uk", "Glasgow", 55.8642, -4.2518, "Europe/London", "GMT"),
        ("edinburgh-uk", "Edinburgh", 55.9533, -3.1883, "Europe/London", "GMT"),
        ("belfast-uk", "Belfast", 54.5973, -5.9301, "Europe/London", "GMT"),
    ]),
    ("IRL", "Ireland", [
        ("dublin-ireland", "Dublin", 53.3498, -6.2603, "Europe/Dublin", "GMT"),
        ("cork-ireland", "Cork", 51.8985, -8.4756, "Europe/Dublin", "GMT"),
    ]),
    ("FRA", "France", [
        ("paris-france", "Paris", 48.8566, 2.3522, "Europe/Paris", "CET"),
        ("marseille-france", "Marseille", 43.2965, 5.3698, "Europe/Paris", "CET"),
        ("lyon-france", "Lyon", 45.7640, 4.8357, "Europe/Paris", "CET"),
        ("toulouse-france", "Toulouse", 43.6047, 1.4442, "Europe/Paris", "CET"),
        ("nice-france", "Nice", 43.7102, 7.2620, "Europe/Paris", "CET"),
        ("bordeaux-france", "Bordeaux", 44.8378, -0.5792, "Europe/Paris", "CET"),
        ("lille-france", "Lille", 50.6292, 3.0573, "Europe/Paris", "CET"),
    ]),
    ("DEU", "Germany", [
        ("berlin-germany", "Berlin", 52.5200, 13.4050, "Europe/Berlin", "CET"),
        ("munich-germany", "Munich", 48.1351, 11.5820, "Europe/Berlin", "CET"),
        ("frankfurt-germany", "Frankfurt", 50.1109, 8.6821, "Europe/Berlin", "CET"),
        ("hamburg-germany", "Hamburg", 53.5511, 9.9937, "Europe/Berlin", "CET"),
        ("cologne-germany", "Cologne", 50.9375, 6.9603, "Europe/Berlin", "CET"),
        ("stuttgart-germany", "Stuttgart", 48.7758, 9.1829, "Europe/Berlin", "CET"),
        ("dusseldorf-germany", "Dusseldorf", 51.2277, 6.7735, "Europe/Berlin", "CET"),
        ("leipzig-germany", "Leipzig", 51.3397, 12.3731, "Europe/Berlin", "CET"),
    ]),
    ("ESP", "Spain", [
        ("madrid-spain", "Madrid", 40.4168, -3.7038, "Europe/Madrid", "CET"),
        ("barcelona-spain", "Barcelona", 41.3874, 2.1686, "Europe/Madrid", "CET"),
        ("valencia-spain", "Valencia", 39.4699, -0.3763, "Europe/Madrid", "CET"),
        ("seville-spain", "Seville", 37.3891, -5.9845, "Europe/Madrid", "CET"),
        ("malaga-spain", "Malaga", 36.7213, -4.4214, "Europe/Madrid", "CET"),
        ("bilbao-spain", "Bilbao", 43.2630, -2.9350, "Europe/Madrid", "CET"),
    ]),
    ("ITA", "Italy", [
        ("rome-italy", "Rome", 41.9028, 12.4964, "Europe/Rome", "CET"),
        ("milan-italy", "Milan", 45.4642, 9.1900, "Europe/Rome", "CET"),
        ("naples-italy", "Naples", 40.8518, 14.2681, "Europe/Rome", "CET"),
        ("turin-italy", "Turin", 45.0703, 7.6869, "Europe/Rome", "CET"),
        ("florence-italy", "Florence", 43.7696, 11.2558, "Europe/Rome", "CET"),
        ("bologna-italy", "Bologna", 44.4949, 11.3426, "Europe/Rome", "CET"),
        ("venice-italy", "Venice", 45.4408, 12.3155, "Europe/Rome", "CET"),
    ]),
    ("NLD", "Netherlands", [
        ("amsterdam-netherlands", "Amsterdam", 52.3676, 4.9041, "Europe/Amsterdam", "CET"),
        ("rotterdam-netherlands", "Rotterdam", 51.9244, 4.4777, "Europe/Amsterdam", "CET"),
        ("the-hague-netherlands", "The Hague", 52.0705, 4.3007, "Europe/Amsterdam", "CET"),
        ("eindhoven-netherlands", "Eindhoven", 51.4416, 5.4697, "Europe/Amsterdam", "CET"),
    ]),
    ("BEL", "Belgium", [
        ("brussels-belgium", "Brussels", 50.8503, 4.3517, "Europe/Brussels", "CET"),
        ("antwerp-belgium", "Antwerp", 51.2194, 4.4025, "Europe/Brussels", "CET"),
    ]),
    ("CHE", "Switzerland", [
        ("zurich-switzerland", "Zurich", 47.3769, 8.5417, "Europe/Zurich", "CET"),
        ("geneva-switzerland", "Geneva", 46.2044, 6.1432, "Europe/Zurich", "CET"),
        ("basel-switzerland", "Basel", 47.5596, 7.5886, "Europe/Zurich", "CET"),
    ]),
    ("AUT", "Austria", [
        ("vienna-austria", "Vienna", 48.2082, 16.3738, "Europe/Vienna", "CET"),
        ("salzburg-austria", "Salzburg", 47.8095, 13.0550, "Europe/Vienna", "CET"),
    ]),
    ("PRT", "Portugal", [
        ("lisbon-portugal", "Lisbon", 38.7223, -9.1393, "Europe/Lisbon", "WET"),
        ("porto-portugal", "Porto", 41.1579, -8.6291, "Europe/Lisbon", "WET"),
    ]),
    ("SWE", "Sweden", [
        ("stockholm-sweden", "Stockholm", 59.3293, 18.0686, "Europe/Stockholm", "CET"),
        ("gothenburg-sweden", "Gothenburg", 57.7089, 11.9746, "Europe/Stockholm", "CET"),
        ("malmo-sweden", "Malmo", 55.6050, 13.0038, "Europe/Stockholm", "CET"),
    ]),
    ("NOR", "Norway", [
        ("oslo-norway", "Oslo", 59.9139, 10.7522, "Europe/Oslo", "CET"),
        ("bergen-norway", "Bergen", 60.3913, 5.3221, "Europe/Oslo", "CET"),
        ("trondheim-norway", "Trondheim", 63.4305, 10.3951, "Europe/Oslo", "CET"),
    ]),
    ("DNK", "Denmark", [
        ("copenhagen-denmark", "Copenhagen", 55.6761, 12.5683, "Europe/Copenhagen", "CET"),
        ("aarhus-denmark", "Aarhus", 56.1629, 10.2039, "Europe/Copenhagen", "CET"),
    ]),
    ("FIN", "Finland", [
        ("helsinki-finland", "Helsinki", 60.1699, 24.9384, "Europe/Helsinki", "EET"),
        ("tampere-finland", "Tampere", 61.4978, 23.7610, "Europe/Helsinki", "EET"),
    ]),
    ("POL", "Poland", [
        ("warsaw-poland", "Warsaw", 52.2297, 21.0122, "Europe/Warsaw", "CET"),
        ("krakow-poland", "Krakow", 50.0647, 19.9450, "Europe/Warsaw", "CET"),
        ("wroclaw-poland", "Wroclaw", 51.1079, 17.0385, "Europe/Warsaw", "CET"),
        ("gdansk-poland", "Gdansk", 54.3520, 18.6466, "Europe/Warsaw", "CET"),
        ("poznan-poland", "Poznan", 52.4064, 16.9252, "Europe/Warsaw", "CET"),
    ]),
    ("CZE", "Czech Republic", [
        ("prague-czech-republic", "Prague", 50.0755, 14.4378, "Europe/Prague", "CET"),
        ("brno-czech-republic", "Brno", 49.1951, 16.6068, "Europe/Prague", "CET"),
    ]),
    ("HUN", "Hungary", [
        ("budapest-hungary", "Budapest", 47.4979, 19.0402, "Europe/Budapest", "CET"),
    ]),
    ("ROU", "Romania", [
        ("bucharest-romania", "Bucharest", 44.4268, 26.1025, "Europe/Bucharest", "EET"),
        ("cluj-napoca-romania", "Cluj-Napoca", 46.7712, 23.6236, "Europe/Bucharest", "EET"),
    ]),
    ("GRC", "Greece", [
        ("athens-greece", "Athens", 37.9838, 23.7275, "Europe/Athens", "EET"),
        ("thessaloniki-greece", "Thessaloniki", 40.6401, 22.9444, "Europe/Athens", "EET"),
    ]),
    ("TUR", "Turkey", [
        ("istanbul-turkey", "Istanbul", 41.0082, 28.9784, "Europe/Istanbul", "TRT"),
        ("ankara-turkey", "Ankara", 39.9334, 32.8597, "Europe/Istanbul", "TRT"),
        ("izmir-turkey", "Izmir", 38.4237, 27.1428, "Europe/Istanbul", "TRT"),
        ("antalya-turkey", "Antalya", 36.8969, 30.7133, "Europe/Istanbul", "TRT"),
    ]),
    ("RUS", "Russia", [
        ("moscow-russia", "Moscow", 55.7558, 37.6173, "Europe/Moscow", "MSK"),
        ("saint-petersburg-russia", "Saint Petersburg", 59.9311, 30.3609, "Europe/Moscow", "MSK"),
        ("novosibirsk-russia", "Novosibirsk", 55.0084, 82.9357, "Asia/Novosibirsk", "NOVT"),
        ("yekaterinburg-russia", "Yekaterinburg", 56.8389, 60.6057, "Asia/Yekaterinburg", "YEKT"),
        ("vladivostok-russia", "Vladivostok", 43.1155, 131.8855, "Asia/Vladivostok", "VLAT"),
    ]),
    ("UKR", "Ukraine", [
        ("kyiv-ukraine", "Kyiv", 50.4501, 30.5234, "Europe/Kyiv", "EET"),
        ("odesa-ukraine", "Odesa", 46.4825, 30.7233, "Europe/Kyiv", "EET"),
        ("lviv-ukraine", "Lviv", 49.8397, 24.0297, "Europe/Kyiv", "EET"),
    ]),
    ("ISR", "Israel", [
        ("jerusalem-israel", "Jerusalem", 31.7683, 35.2137, "Asia/Jerusalem", "IST"),
        ("tel-aviv-israel", "Tel Aviv", 32.0853, 34.7818, "Asia/Jerusalem", "IST"),
    ]),
    ("UAE", "United Arab Emirates", [
        ("dubai-uae", "Dubai", 25.2048, 55.2708, "Asia/Dubai", "GST"),
        ("abu-dhabi-uae", "Abu Dhabi", 24.4539, 54.3773, "Asia/Dubai", "GST"),
        ("sharjah-uae", "Sharjah", 25.3463, 55.4209, "Asia/Dubai", "GST"),
        ("ajman-uae", "Ajman", 25.4052, 55.5136, "Asia/Dubai", "GST"),
    ]),
    ("SA", "Saudi Arabia", [
        ("riyadh-saudi-arabia", "Riyadh", 24.7136, 46.6753, "Asia/Riyadh", "AST"),
        ("jeddah-saudi-arabia", "Jeddah", 21.4858, 39.1925, "Asia/Riyadh", "AST"),
        ("mecca-saudi-arabia", "Mecca", 21.3891, 39.8579, "Asia/Riyadh", "AST"),
        ("medina-saudi-arabia", "Medina", 24.5247, 39.5692, "Asia/Riyadh", "AST"),
        ("dammam-saudi-arabia", "Dammam", 26.4207, 50.0888, "Asia/Riyadh", "AST"),
    ]),
    ("QAT", "Qatar", [
        ("doha-qatar", "Doha", 25.2854, 51.5310, "Asia/Qatar", "AST"),
    ]),
    ("KWT", "Kuwait", [
        ("kuwait-city-kuwait", "Kuwait City", 29.3759, 47.9774, "Asia/Kuwait", "AST"),
    ]),
    ("BHR", "Bahrain", [
        ("manama-bahrain", "Manama", 26.2235, 50.5876, "Asia/Bahrain", "AST"),
    ]),
    ("OMN", "Oman", [
        ("muscat-oman", "Muscat", 23.5880, 58.3829, "Asia/Muscat", "GST"),
    ]),
    ("EGY", "Egypt", [
        ("cairo-egypt", "Cairo", 30.0444, 31.2357, "Africa/Cairo", "EET"),
        ("alexandria-egypt", "Alexandria", 31.2001, 29.9187, "Africa/Cairo", "EET"),
        ("giza-egypt", "Giza", 30.0131, 31.2089, "Africa/Cairo", "EET"),
        ("luxor-egypt", "Luxor", 25.6872, 32.6396, "Africa/Cairo", "EET"),
    ]),
    ("ZAF", "South Africa", [
        ("johannesburg-south-africa", "Johannesburg", -26.2041, 28.0473, "Africa/Johannesburg", "SAST"),
        ("cape-town-south-africa", "Cape Town", -33.9249, 18.4241, "Africa/Johannesburg", "SAST"),
        ("durban-south-africa", "Durban", -29.8587, 31.0218, "Africa/Johannesburg", "SAST"),
        ("pretoria-south-africa", "Pretoria", -25.7479, 28.2293, "Africa/Johannesburg", "SAST"),
    ]),
    ("NGA", "Nigeria", [
        ("lagos-nigeria", "Lagos", 6.5244, 3.3792, "Africa/Lagos", "WAT"),
        ("abuja-nigeria", "Abuja", 9.0765, 7.3986, "Africa/Lagos", "WAT"),
        ("kano-nigeria", "Kano", 12.0022, 8.5920, "Africa/Lagos", "WAT"),
        ("port-harcourt-nigeria", "Port Harcourt", 4.8156, 7.0498, "Africa/Lagos", "WAT"),
    ]),
    ("KEN", "Kenya", [
        ("nairobi-kenya", "Nairobi", -1.2921, 36.8219, "Africa/Nairobi", "EAT"),
        ("mombasa-kenya", "Mombasa", -4.0435, 39.6682, "Africa/Nairobi", "EAT"),
    ]),
    ("ETH", "Ethiopia", [
        ("addis-ababa-ethiopia", "Addis Ababa", 8.9806, 38.7578, "Africa/Addis_Ababa", "EAT"),
    ]),
    ("MAR", "Morocco", [
        ("casablanca-morocco", "Casablanca", 33.5731, -7.5898, "Africa/Casablanca", "WET"),
        ("rabat-morocco", "Rabat", 34.0209, -6.8416, "Africa/Casablanca", "WET"),
        ("marrakech-morocco", "Marrakech", 31.6295, -7.9811, "Africa/Casablanca", "WET"),
    ]),
    ("DZA", "Algeria", [
        ("algiers-algeria", "Algiers", 36.7538, 3.0588, "Africa/Algiers", "CET"),
    ]),
    ("TUN", "Tunisia", [
        ("tunis-tunisia", "Tunis", 36.8065, 10.1815, "Africa/Tunis", "CET"),
    ]),
    ("GHA", "Ghana", [
        ("accra-ghana", "Accra", 5.6037, -0.1870, "Africa/Accra", "GMT"),
    ]),
    ("TZA", "Tanzania", [
        ("dar-es-salaam-tanzania", "Dar es Salaam", -6.7924, 39.2083, "Africa/Dar_es_Salaam", "EAT"),
    ]),
    ("UGA", "Uganda", [
        ("kampala-uganda", "Kampala", 0.3476, 32.5825, "Africa/Kampala", "EAT"),
    ]),
    ("NPL", "Nepal", [
        ("kathmandu-nepal", "Kathmandu", 27.7172, 85.3240, "Asia/Kathmandu", "NPT"),
        ("pokhara-nepal", "Pokhara", 28.2096, 83.9856, "Asia/Kathmandu", "NPT"),
    ]),
    ("LKA", "Sri Lanka", [
        ("colombo-sri-lanka", "Colombo", 6.9271, 79.8612, "Asia/Colombo", "IST"),
        ("kandy-sri-lanka", "Kandy", 7.2906, 80.6337, "Asia/Colombo", "IST"),
    ]),
    ("BGD", "Bangladesh", [
        ("dhaka-bangladesh", "Dhaka", 23.8103, 90.4125, "Asia/Dhaka", "BST"),
        ("chittagong-bangladesh", "Chittagong", 22.3569, 91.7832, "Asia/Dhaka", "BST"),
        ("sylhet-bangladesh", "Sylhet", 24.8949, 91.8687, "Asia/Dhaka", "BST"),
        ("khulna-bangladesh", "Khulna", 22.8456, 89.5403, "Asia/Dhaka", "BST"),
    ]),
    ("PAK", "Pakistan", [
        ("karachi-pakistan", "Karachi", 24.8607, 67.0011, "Asia/Karachi", "PKT"),
        ("lahore-pakistan", "Lahore", 31.5204, 74.3587, "Asia/Karachi", "PKT"),
        ("islamabad-pakistan", "Islamabad", 33.6844, 73.0479, "Asia/Karachi", "PKT"),
        ("rawalpindi-pakistan", "Rawalpindi", 33.5651, 73.0169, "Asia/Karachi", "PKT"),
        ("peshawar-pakistan", "Peshawar", 34.0151, 71.5249, "Asia/Karachi", "PKT"),
    ]),
    ("AFG", "Afghanistan", [
        ("kabul-afghanistan", "Kabul", 34.5553, 69.2075, "Asia/Kabul", "AFT"),
    ]),
    ("CHN", "China", [
        ("beijing-china", "Beijing", 39.9042, 116.4074, "Asia/Shanghai", "CST"),
        ("shanghai-china", "Shanghai", 31.2304, 121.4737, "Asia/Shanghai", "CST"),
        ("guangzhou-china", "Guangzhou", 23.1291, 113.2644, "Asia/Shanghai", "CST"),
        ("shenzhen-china", "Shenzhen", 22.5431, 114.0579, "Asia/Shanghai", "CST"),
        ("chengdu-china", "Chengdu", 30.5728, 104.0668, "Asia/Shanghai", "CST"),
        ("chongqing-china", "Chongqing", 29.4316, 106.9123, "Asia/Shanghai", "CST"),
        ("xian-china", "Xi'an", 34.3416, 108.9398, "Asia/Shanghai", "CST"),
        ("wuhan-china", "Wuhan", 30.5928, 114.3055, "Asia/Shanghai", "CST"),
        ("hangzhou-china", "Hangzhou", 30.2741, 120.1551, "Asia/Shanghai", "CST"),
        ("nanjing-china", "Nanjing", 32.0603, 118.7969, "Asia/Shanghai", "CST"),
        ("tianjin-china", "Tianjin", 39.3434, 117.3616, "Asia/Shanghai", "CST"),
        ("harbin-china", "Harbin", 45.8038, 126.5349, "Asia/Shanghai", "CST"),
        ("urumqi-china", "Urumqi", 43.8256, 87.6168, "Asia/Shanghai", "CST"),
    ]),
    ("HKG", "Hong Kong", [
        ("hong-kong", "Hong Kong", 22.3193, 114.1694, "Asia/Hong_Kong", "HKT"),
    ]),
    ("TWN", "Taiwan", [
        ("taipei-taiwan", "Taipei", 25.0330, 121.5654, "Asia/Taipei", "CST"),
        ("kaohsiung-taiwan", "Kaohsiung", 22.6273, 120.3014, "Asia/Taipei", "CST"),
        ("taichung-taiwan", "Taichung", 24.1477, 120.6736, "Asia/Taipei", "CST"),
    ]),
    ("JPN", "Japan", [
        ("tokyo-japan", "Tokyo", 35.6762, 139.6503, "Asia/Tokyo", "JST"),
        ("osaka-japan", "Osaka", 34.6937, 135.5023, "Asia/Tokyo", "JST"),
        ("kyoto-japan", "Kyoto", 35.0116, 135.7681, "Asia/Tokyo", "JST"),
        ("nagoya-japan", "Nagoya", 35.1815, 136.9066, "Asia/Tokyo", "JST"),
        ("sapporo-japan", "Sapporo", 43.0618, 141.3545, "Asia/Tokyo", "JST"),
        ("fukuoka-japan", "Fukuoka", 33.5904, 130.4017, "Asia/Tokyo", "JST"),
        ("hiroshima-japan", "Hiroshima", 34.3853, 132.4553, "Asia/Tokyo", "JST"),
    ]),
    ("KOR", "South Korea", [
        ("seoul-south-korea", "Seoul", 37.5665, 126.9780, "Asia/Seoul", "KST"),
        ("busan-south-korea", "Busan", 35.1796, 129.0756, "Asia/Seoul", "KST"),
        ("incheon-south-korea", "Incheon", 37.4563, 126.7052, "Asia/Seoul", "KST"),
        ("daegu-south-korea", "Daegu", 35.8714, 128.6014, "Asia/Seoul", "KST"),
        ("daejeon-south-korea", "Daejeon", 36.3504, 127.3845, "Asia/Seoul", "KST"),
    ]),
    ("SG", "Singapore", [
        ("singapore-city-singapore", "Singapore", 1.3521, 103.8198, "Asia/Singapore", "SGT"),
    ]),
    ("MYS", "Malaysia", [
        ("kuala-lumpur-malaysia", "Kuala Lumpur", 3.1390, 101.6869, "Asia/Kuala_Lumpur", "MYT"),
        ("johor-bahru-malaysia", "Johor Bahru", 1.4927, 103.7414, "Asia/Kuala_Lumpur", "MYT"),
        ("george-town-malaysia", "George Town", 5.4141, 100.3288, "Asia/Kuala_Lumpur", "MYT"),
        ("kota-kinabalu-malaysia", "Kota Kinabalu", 5.9804, 116.0735, "Asia/Kuala_Lumpur", "MYT"),
    ]),
    ("ID", "Indonesia", [
        ("jakarta-indonesia", "Jakarta", -6.2088, 106.8456, "Asia/Jakarta", "WIB"),
        ("surabaya-indonesia", "Surabaya", -7.2575, 112.7521, "Asia/Jakarta", "WIB"),
        ("bandung-indonesia", "Bandung", -6.9175, 107.6191, "Asia/Jakarta", "WIB"),
        ("medan-indonesia", "Medan", 3.5952, 98.6722, "Asia/Jakarta", "WIB"),
        ("denpasar-indonesia", "Denpasar", -8.6500, 115.2167, "Asia/Makassar", "WITA"),
        ("makassar-indonesia", "Makassar", -5.1477, 119.4327, "Asia/Makassar", "WITA"),
        ("yogyakarta-indonesia", "Yogyakarta", -7.7956, 110.3695, "Asia/Jakarta", "WIB"),
    ]),
    ("THA", "Thailand", [
        ("bangkok-thailand", "Bangkok", 13.7563, 100.5018, "Asia/Bangkok", "ICT"),
        ("chiang-mai-thailand", "Chiang Mai", 18.7883, 98.9853, "Asia/Bangkok", "ICT"),
        ("phuket-thailand", "Phuket", 7.8804, 98.3923, "Asia/Bangkok", "ICT"),
        ("pattaya-thailand", "Pattaya", 12.9236, 100.8825, "Asia/Bangkok", "ICT"),
    ]),
    ("VNM", "Vietnam", [
        ("ho-chi-minh-city-vietnam", "Ho Chi Minh City", 10.8231, 106.6297, "Asia/Ho_Chi_Minh", "ICT"),
        ("hanoi-vietnam", "Hanoi", 21.0278, 105.8342, "Asia/Ho_Chi_Minh", "ICT"),
        ("da-nang-vietnam", "Da Nang", 16.0544, 108.2022, "Asia/Ho_Chi_Minh", "ICT"),
        ("hai-phong-vietnam", "Hai Phong", 20.8449, 106.6881, "Asia/Ho_Chi_Minh", "ICT"),
    ]),
    ("PHL", "Philippines", [
        ("manila-philippines", "Manila", 14.5995, 120.9842, "Asia/Manila", "PHT"),
        ("cebu-philippines", "Cebu", 10.3157, 123.8854, "Asia/Manila", "PHT"),
        ("davao-philippines", "Davao", 7.1907, 125.4553, "Asia/Manila", "PHT"),
        ("quezon-city-philippines", "Quezon City", 14.6760, 121.0437, "Asia/Manila", "PHT"),
    ]),
    ("KHM", "Cambodia", [
        ("phnom-penh-cambodia", "Phnom Penh", 11.5564, 104.9282, "Asia/Phnom_Penh", "ICT"),
    ]),
    ("LAO", "Laos", [
        ("vientiane-laos", "Vientiane", 17.9757, 102.6331, "Asia/Vientiane", "ICT"),
    ]),
    ("MMR", "Myanmar", [
        ("yangon-myanmar", "Yangon", 16.8409, 96.1735, "Asia/Yangon", "MMT"),
        ("mandalay-myanmar", "Mandalay", 21.9588, 96.0891, "Asia/Yangon", "MMT"),
    ]),
    ("MNG", "Mongolia", [
        ("ulaanbaatar-mongolia", "Ulaanbaatar", 47.8864, 106.9057, "Asia/Ulaanbaatar", "ULAT"),
    ]),
    ("TIB", "Tibet", [
        ("lhasa-tibet", "Lhasa", 29.6520, 91.1721, "Asia/Shanghai", "CST"),
        ("shigatse-tibet", "Shigatse", 29.2673, 88.8808, "Asia/Shanghai", "CST"),
    ]),
    ("AUS", "Australia", [
        ("sydney-australia", "Sydney", -33.8688, 151.2093, "Australia/Sydney", "AEST"),
        ("melbourne-australia", "Melbourne", -37.8136, 144.9631, "Australia/Melbourne", "AEST"),
        ("brisbane-australia", "Brisbane", -27.4698, 153.0251, "Australia/Brisbane", "AEST"),
        ("perth-australia", "Perth", -31.9505, 115.8605, "Australia/Perth", "AWST"),
        ("adelaide-australia", "Adelaide", -34.9285, 138.6007, "Australia/Adelaide", "ACST"),
        ("canberra-australia", "Canberra", -35.2809, 149.1300, "Australia/Sydney", "AEST"),
        ("hobart-australia", "Hobart", -42.8821, 147.3272, "Australia/Hobart", "AEST"),
        ("darwin-australia", "Darwin", -12.4634, 130.8456, "Australia/Darwin", "ACST"),
        ("gold-coast-australia", "Gold Coast", -28.0167, 153.4000, "Australia/Brisbane", "AEST"),
    ]),
    ("NZL", "New Zealand", [
        ("auckland-new-zealand", "Auckland", -36.8509, 174.7645, "Pacific/Auckland", "NZST"),
        ("wellington-new-zealand", "Wellington", -41.2866, 174.7756, "Pacific/Auckland", "NZST"),
        ("christchurch-new-zealand", "Christchurch", -43.5321, 172.6362, "Pacific/Auckland", "NZST"),
        ("queenstown-new-zealand", "Queenstown", -45.0312, 168.6626, "Pacific/Auckland", "NZST"),
    ]),
    ("FJI", "Fiji", [
        ("suva-fiji", "Suva", -18.1248, 178.4501, "Pacific/Fiji", "FJT"),
    ]),
    ("PNG", "Papua New Guinea", [
        ("port-moresby-papua-new-guinea", "Port Moresby", -9.4438, 147.1803, "Pacific/Port_Moresby", "PGT"),
    ]),
    ("WSM", "Samoa", [
        ("apia-samoa", "Apia", -13.8507, -171.7514, "Pacific/Apia", "WSST"),
    ]),
]

DEFAULT_LOCATIONS, LOCATION_GROUPS = _build_location_catalog(GLOBAL_LOCATION_GROUPED_RECORDS)
LOCATION_LIST = list(DEFAULT_LOCATIONS.values())


TITHI_NAMES = [
    "Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi",
    "Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi",
    "Trayodashi","Chaturdashi","Purnima",
    "Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi",
    "Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi",
    "Trayodashi","Chaturdashi","Amavasya",
]
NAKSHATRA_NAMES = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
    "Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni",
    "Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha",
    "Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana",
    "Dhanishtha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati",
]
YOGA_NAMES = [
    "Vishkambha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda",
    "Sukarma","Dhriti","Shoola","Ganda","Vriddhi","Dhruva","Vyaghata",
    "Harshana","Vajra","Siddhi","Vyatipata","Variyana","Parigha","Shiva",
    "Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti",
]
KARANA_NAMES = [
    "Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti",
    "Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti",
    "Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti",
    "Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti",
    "Shakuni","Chatushpada","Naga","Kimstughna",
]
RASHI_NAMES = [
    "Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya",
    "Tula","Vrischika","Dhanu","Makara","Kumbha","Meena",
]
LUNAR_MONTHS = [
    "Chaitra","Vaishakha","Jyeshtha","Ashadha","Shravana","Bhadrapada",
    "Ashwin","Kartika","Margashirsha","Pausha","Magha","Phalguna",
]

OBSERVANCE_RULES: list[dict] = [
    {"slug": "ekadashi",       "name": "Ekadashi",        "observance_type": "vrat",       "tithi_indexes": [10, 25], "month_indexes": None, "priority": 2},
    {"slug": "pradosh-vrat",   "name": "Pradosh Vrat",    "observance_type": "vrat",       "tithi_indexes": [12, 27], "month_indexes": None, "priority": 2},
    {"slug": "purnima",        "name": "Purnima",          "observance_type": "observance", "tithi_indexes": [14],     "month_indexes": None, "priority": 2},
    {"slug": "amavasya",       "name": "Amavasya",         "observance_type": "observance", "tithi_indexes": [29],     "month_indexes": None, "priority": 2},
    {"slug": "maha-shivaratri","name": "Maha Shivaratri",  "observance_type": "festival",   "tithi_indexes": [28],     "month_indexes": [10], "priority": 3},
    {"slug": "janmashtami",    "name": "Janmashtami",      "observance_type": "festival",   "tithi_indexes": [22],     "month_indexes": [4],  "priority": 3},
    {"slug": "rama-navami",    "name": "Rama Navami",      "observance_type": "festival",   "tithi_indexes": [8],      "month_indexes": [0],  "priority": 3},
    {"slug": "holi",           "name": "Holi",              "observance_type": "festival",   "tithi_indexes": [14],     "month_indexes": [11], "priority": 3},
    {"slug": "diwali",         "name": "Diwali",            "observance_type": "festival",   "tithi_indexes": [29],     "month_indexes": [7],  "priority": 3},
]


@dataclass(frozen=True)
class DailyAstronomy:
    sunrise:  datetime
    sunset:   datetime
    moonrise: datetime | None
    moonset:  datetime | None
    sun_longitude:  float
    moon_longitude: float


def _normalize_angle(value: float) -> float:
    return value % 360.0


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as err:
        raise HTTPException(status_code=400, detail="Invalid date. Use YYYY-MM-DD.") from err


def _resolve_location(
    location_slug: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
    tz_name: str | None = None,
) -> PanchangLocation:
    if location_slug and location_slug in DEFAULT_LOCATIONS:
        return DEFAULT_LOCATIONS[location_slug]
    if lat is not None and lng is not None and tz_name:
        slug = "custom-" + str(round(lat, 3)).replace(".", "-") + "-" + str(round(lng, 3)).replace(".", "-")
        return PanchangLocation(slug=slug, label="Custom Location", country="Custom",
                                latitude=lat, longitude=lng, timezone=tz_name)
    return DEFAULT_LOCATIONS["new-delhi-india"]


def _datetime_to_jd(dt_utc: datetime) -> float:
    return swe.julday(
        dt_utc.year, dt_utc.month, dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
    )


def _jd_to_local_dt(jd: float, tz: ZoneInfo) -> datetime:
    y, mo, d, hr, mn, sf = swe.jdut1_to_utc(jd, swe.GREG_CAL)
    sc = int(round(sf))
    if sc == 60: mn += 1; sc = 0
    if mn == 60: hr += 1; mn = 0
    return datetime(y, mo, d, hr, mn, sc, tzinfo=timezone.utc).astimezone(tz)


def _sun_longitude(jd: float) -> float:
    result = swe.calc_ut(jd, int(swe.SUN), int(_SWE_FLAGS))
    return _normalize_angle(result[0][0])


def _moon_longitude(jd: float) -> float:
    result = swe.calc_ut(jd, int(swe.MOON), int(_SWE_FLAGS))
    return _normalize_angle(result[0][0])


def _rise_trans_event(
    jd_start: float,
    body: int,
    event_flag: int,
    geopos: tuple[float, float, float],
    tz: ZoneInfo,
    fallback: datetime | None = None,
) -> datetime | None:
    try:
        ret = swe.rise_trans(jd_start, body, event_flag, geopos, 1013.25, 15.0)
        return _jd_to_local_dt(ret[1][0], tz)
    except Exception:
        return fallback


def _sunrise_sunset_moonrise_moonset(
    base_date: date, latitude: float, longitude: float, tz_name: str
) -> tuple[datetime, datetime, datetime | None, datetime | None]:
    tz = ZoneInfo(tz_name)
    local_midnight = datetime(base_date.year, base_date.month, base_date.day, 0, 0, 0, tzinfo=tz)
    jd_start = _datetime_to_jd(local_midnight.astimezone(timezone.utc))
    geopos   = (longitude, latitude, 0.0)
    sunrise  = _rise_trans_event(jd_start,        swe.SUN,  swe.CALC_RISE, geopos, tz,
                                  fallback=local_midnight.replace(hour=6, minute=18))
    sunset   = _rise_trans_event(jd_start + 0.25, swe.SUN,  swe.CALC_SET,  geopos, tz,
                                  fallback=local_midnight.replace(hour=18, minute=35))
    moonrise = _rise_trans_event(jd_start,         swe.MOON, swe.CALC_RISE, geopos, tz)
    moonset  = _rise_trans_event(jd_start + 0.1,  swe.MOON, swe.CALC_SET,  geopos, tz)
    return sunrise, sunset, moonrise, moonset


def _moment_longitudes(moment_local: datetime) -> tuple[float, float]:
    moment_utc = moment_local.astimezone(timezone.utc)
    jd = _datetime_to_jd(moment_utc)
    return _sun_longitude(jd), _moon_longitude(jd)


def _segment_interval(
    base_date: date, latitude: float, longitude: float,
    tz_name: str, metric: str, start_index: int,
) -> tuple[str, str | None]:
    tz = ZoneInfo(tz_name)
    start_local = datetime.combine(base_date, time(0, 0), tzinfo=tz)
    end_local = start_local + timedelta(days=1)
    step = timedelta(minutes=20)
    found_end: datetime | None = None
    cursor = start_local + step
    while cursor <= end_local:
        sun_long, moon_long = _moment_longitudes(cursor)
        if metric == "tithi":
            index = int(_normalize_angle(moon_long - sun_long) // 12)
        elif metric == "nakshatra":
            index = int(moon_long // (360 / 27))
        elif metric == "yoga":
            index = int(_normalize_angle(moon_long + sun_long) // (360 / 27))
        else:
            index = min(int(_normalize_angle(moon_long - sun_long) // 6), 31)
        if index != start_index:
            found_end = cursor
            break
        cursor += step
    return start_local.isoformat(), found_end.isoformat() if found_end else None


def _build_daily_astronomy(
    base_date: date, latitude: float, longitude: float, tz_name: str,
) -> DailyAstronomy:
    sunrise, sunset, moonrise, moonset = _sunrise_sunset_moonrise_moonset(
        base_date, latitude, longitude, tz_name,
    )
    sun_longitude, moon_longitude = _moment_longitudes(sunrise)
    return DailyAstronomy(
        sunrise=sunrise, sunset=sunset,
        moonrise=moonrise, moonset=moonset,
        sun_longitude=sun_longitude, moon_longitude=moon_longitude,
    )


def _tithi_index(sun_longitude: float, moon_longitude: float) -> int:
    return int(_normalize_angle(moon_longitude - sun_longitude) // 12)

def _nakshatra_index(moon_longitude: float) -> int:
    return int(moon_longitude // (360 / 27))

def _yoga_index(sun_longitude: float, moon_longitude: float) -> int:
    return int(_normalize_angle(sun_longitude + moon_longitude) // (360 / 27))

def _karana_index(sun_longitude: float, moon_longitude: float) -> int:
    return min(int(_normalize_angle(moon_longitude - sun_longitude) // 6), 31)

def _paksha_from_tithi(index: int) -> str:
    return "Shukla" if index <= 14 else "Krishna"

def _lunar_month_index(
    sun_longitude: float, moon_longitude: float, calendar_variant: CalendarVariant,
) -> int:
    solar_month = int(sun_longitude // 30)
    lunation    = _tithi_index(sun_longitude, moon_longitude)
    offset      = 1 if calendar_variant == "purnimanta" and lunation < 15 else 0
    return (solar_month + 1 + offset) % 12

def _samvat_label(base_date: date) -> str:
    return f"Vikram {base_date.year + 57} / Shaka {base_date.year - 78}"

def _window_time(anchor: datetime, offset_minutes: float, duration_minutes: float) -> tuple[str, str]:
    start = anchor + timedelta(minutes=offset_minutes)
    end   = start  + timedelta(minutes=duration_minutes)
    return start.isoformat(), end.isoformat()


def _amrit_kalam_window(
    sunrise: datetime, sunset: datetime, moon_longitude: float,
) -> PanchangTimingWindow:
    """
    Amrit Kalam -- nakshatra-based auspicious window.

    Formula (verified vs Drik Panchang, New Delhi 26 Mar 2026 ±1 min):
      offset   = nakshatra_remaining_fraction × daylight / 10
               = 3 Vedic ghatis × remaining nakshatra fraction
      duration = daylight / 8  (one Choghadiya slot)
    """
    nak_span  = 360.0 / 27.0                                      # 13°20' per nakshatra
    nak_start = math.floor(moon_longitude / nak_span) * nak_span
    rem_frac  = (nak_start + nak_span - moon_longitude) / nak_span # fraction of nakshatra remaining

    daylight_min = (sunset - sunrise).total_seconds() / 60.0
    offset_min   = rem_frac * daylight_min / 10.0                 # 3 ghatis × remaining fraction
    duration_min = daylight_min / 8.0

    amrit_start = sunrise + timedelta(minutes=offset_min)
    amrit_end   = amrit_start + timedelta(minutes=duration_min)

    return PanchangTimingWindow(
        label="Amrit Kalam",
        start=amrit_start.isoformat(),
        end=amrit_end.isoformat(),
        quality="good",
    )


def _day_quality_windows(
    sunrise: datetime, sunset: datetime, isoweekday: int, moon_longitude: float
) -> list[PanchangTimingWindow]:
    daylight_min = max((sunset - sunrise).total_seconds() / 60, 1.0)
    kaal         = daylight_min / 8.0
    muhurta_dur  = daylight_min / 15.0

    def kaal_window(slot: int) -> tuple[str, str]:
        return _window_time(sunrise, (slot - 1) * kaal, kaal)

    rahu_start,    rahu_end    = kaal_window(_RAHU_KAAL_SLOT[isoweekday])
    yama_start,    yama_end    = kaal_window(_YAMAGANDA_SLOT[isoweekday])
    gulika_start,  gulika_end  = kaal_window(_GULIKA_SLOT[isoweekday])
    brahma_start,  brahma_end  = _window_time(sunrise, -96.0, 96.0)
    abhijit_start, abhijit_end = _window_time(sunrise, daylight_min / 2.0 - 24.0, 48.0)
    m1_idx, m2_idx = _DUR_MUHURTA_MUHURTAS[isoweekday]
    dur1_start, dur1_end = _window_time(sunrise, m1_idx * muhurta_dur, muhurta_dur)
    dur2_start, dur2_end = _window_time(sunrise, m2_idx * muhurta_dur, muhurta_dur)
    vij_start,  vij_end  = _window_time(sunrise, _VIJAYA_MUHURTA[isoweekday] * muhurta_dur, muhurta_dur)

    return [
        _amrit_kalam_window(sunrise, sunset, moon_longitude),
        PanchangTimingWindow(label="Brahma Muhurta",  start=brahma_start,  end=brahma_end,  quality="good"),
        PanchangTimingWindow(label="Rahu Kaal",        start=rahu_start,    end=rahu_end,    quality="caution"),
        PanchangTimingWindow(label="Yamaganda",        start=yama_start,    end=yama_end,    quality="caution"),
        PanchangTimingWindow(label="Gulika Kaal",      start=gulika_start,  end=gulika_end,  quality="neutral"),
        PanchangTimingWindow(label="Dur Muhurta",      start=dur1_start,    end=dur1_end,    quality="caution"),
        PanchangTimingWindow(label="Dur Muhurta 2",    start=dur2_start,    end=dur2_end,    quality="caution"),
        PanchangTimingWindow(label="Abhijit Muhurta",  start=abhijit_start, end=abhijit_end, quality="good"),
        PanchangTimingWindow(label="Vijaya Muhurta",   start=vij_start,     end=vij_end,     quality="good"),
    ]


def _day_indexes(
    base_date: date, location: PanchangLocation, calendar_variant: CalendarVariant,
) -> tuple[dict, dict]:
    astro = _build_daily_astronomy(
        base_date, location.latitude, location.longitude, location.timezone,
    )
    tithi       = _tithi_index(astro.sun_longitude, astro.moon_longitude)
    nakshatra   = _nakshatra_index(astro.moon_longitude)
    yoga        = _yoga_index(astro.sun_longitude, astro.moon_longitude)
    karana      = _karana_index(astro.sun_longitude, astro.moon_longitude)
    lunar_month = _lunar_month_index(astro.sun_longitude, astro.moon_longitude, calendar_variant)
    indexes = {
        "tithi": tithi, "nakshatra": nakshatra, "yoga": yoga,
        "karana": karana, "lunar_month": lunar_month,
        "sun_sign": int(astro.sun_longitude // 30),
        "moon_sign": int(astro.moon_longitude // 30),
    }
    return indexes, {"astro": astro}


_WEEKDAY_NAMES = {1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"}
_WEEKDAY_HORA_RULER = {
    1: "Moon",
    2: "Mars",
    3: "Mercury",
    4: "Jupiter",
    5: "Venus",
    6: "Saturn",
    7: "Sun",
}
_HORA_SEQUENCE = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
_HORA_QUALITY = {
    "Sun": "Power & Authority",
    "Moon": "Mind & Emotions",
    "Mars": "Energy & Action",
    "Mercury": "Communication & Trade",
    "Jupiter": "Wisdom & Expansion",
    "Venus": "Love & Creativity",
    "Saturn": "Discipline & Labour",
}
_MARRIAGE_AUSPICIOUS_TITHIS = {1, 2, 4, 6, 9, 10, 12}
_MARRIAGE_AUSPICIOUS_NAKSHATRAS = {
    "Rohini",
    "Mrigashira",
    "Magha",
    "Uttara Phalguni",
    "Hasta",
    "Swati",
    "Anuradha",
    "Mula",
    "Uttara Ashadha",
    "Uttara Bhadrapada",
    "Revati",
}
_MARRIAGE_HIGHLY_AUSPICIOUS_NAKSHATRAS = {"Rohini", "Uttara Phalguni", "Hasta", "Revati"}
_MARRIAGE_NOTES = {
    "Rohini": "Rohini Nakshatra is especially favoured for harmony, grace, and family prosperity.",
    "Mrigashira": "Mrigashira supports gentle bonding, adaptability, and a steady emotional rhythm.",
    "Magha": "Magha after the 1st Pada is traditionally preferred for dignified family beginnings.",
    "Uttara Phalguni": "Uttara Phalguni is one of the classic marriage nakshatras for commitment and stability.",
    "Hasta": "Hasta brings skill, warmth, and practical support into the household.",
    "Swati": "Swati supports flexibility, mutual growth, and a balanced partnership.",
    "Anuradha": "Anuradha is cherished for devotion, loyalty, and emotional depth in marriage.",
    "Mula": "Mula after the 1st Pada is used selectively for transformative new beginnings.",
    "Uttara Ashadha": "Uttara Ashadha favours endurance, shared purpose, and long-term dharmic alignment.",
    "Uttara Bhadrapada": "Uttara Bhadrapada supports maturity, steadiness, and spiritual depth.",
    "Revati": "Revati is a soft and prosperous marriage nakshatra associated with protection and blessings.",
}
_MARRIAGE_KHARMAS_SUN_SIGNS = {8, 11}
_MARRIAGE_PITRU_PAKSHA_LUNAR_MONTHS = {5, 6}


def _nakshatra_pada(moon_longitude: float) -> int:
    span = 360.0 / 27.0
    pada_span = span / 4.0
    return int((_normalize_angle(moon_longitude) % span) // pada_span) + 1

def _special_yogas(nakshatra: str, isoweekday: int) -> list[SpecialYoga]:
    """Return all special yogas active today based on Nakshatra × Weekday rules."""
    yogas: list[SpecialYoga] = []
    vara = _WEEKDAY_NAMES[isoweekday]

    # Amrit Siddhi (most auspicious -- check first, subset of Sarvartha Siddhi days)
    if _AMRIT_SIDDHI.get(isoweekday) == nakshatra:
        yogas.append(SpecialYoga(
            name="Amrit Siddhi Yoga",
            quality="good",
            nakshatra=nakshatra,
            vara=vara,
            meaning="Nectar of Accomplishment -- the rarest and most powerful auspicious yoga. Excellent for all new beginnings.",
        ))
    # Sarvartha Siddhi
    elif nakshatra in _SARVARTHA_SIDDHI.get(isoweekday, set()):
        yogas.append(SpecialYoga(
            name="Sarvartha Siddhi Yoga",
            quality="good",
            nakshatra=nakshatra,
            vara=vara,
            meaning="All-Purpose Accomplishment -- highly auspicious for starting new ventures, travel, business, and ceremonies.",
        ))

    # Ravi Yoga (inauspicious -- can coexist with auspicious yogas in edge cases)
    if nakshatra in _RAVI_YOGA.get(isoweekday, set()):
        yogas.append(SpecialYoga(
            name="Ravi Yoga",
            quality="caution",
            nakshatra=nakshatra,
            vara=vara,
            meaning="Sun Yoga -- avoid initiating important new work. Good for spiritual practices and Sun worship.",
        ))

    return yogas


def _observances_for_day(
    base_date: date, indexes: dict, tithi_label: str,
) -> list[PanchangObservance]:
    items: list[PanchangObservance] = []
    for rule in OBSERVANCE_RULES:
        if indexes["tithi"] not in rule["tithi_indexes"]:
            continue
        if rule["month_indexes"] is not None and indexes["lunar_month"] not in rule["month_indexes"]:
            continue
        items.append(PanchangObservance(
            slug=rule["slug"], name=rule["name"],
            observance_type=rule["observance_type"],
            date=base_date.isoformat(), priority=rule["priority"],
            summary=f"{rule['name']} aligns with {tithi_label} in {LUNAR_MONTHS[indexes['lunar_month']]}.",
        ))
    return sorted(items, key=lambda i: (-i.priority, i.name))


def _related_links(base_date: date, location: PanchangLocation) -> list[PanchangLink]:
    prev_date = (base_date - timedelta(days=1)).isoformat()
    next_date = (base_date + timedelta(days=1)).isoformat()
    return [
        PanchangLink(label="Previous Day", href=f"/panchang/date/{prev_date}"),
        PanchangLink(label="Tomorrow",     href=f"/panchang/date/{next_date}"),
        PanchangLink(label="This Month",   href=f"/panchang/calendar/{base_date.year}/{base_date.month}"),
        PanchangLink(label="Festivals",    href=f"/panchang/festivals?year={base_date.year}&month={base_date.month}"),
    ]


def _meta(calendar_variant: CalendarVariant, region: RegionCode) -> PanchangMeta:
    return PanchangMeta(
        engine_version=ENGINE_VERSION,
        generated_at=datetime.now(timezone.utc).isoformat(),
        calendar_variant=calendar_variant,
        region=region,
        persistence_mode="stateless_v1",
    )


def _fmt_hhmmss(dt: datetime | None) -> str | None:
    """Format datetime as HH:MM:SS -- includes seconds for precision."""
    return dt.strftime("%H:%M:%S") if dt else None


def _ascendant_longitude(moment_local: datetime, latitude_deg: float, longitude_deg: float) -> float:
    jd = _datetime_to_jd(moment_local.astimezone(timezone.utc))
    _, ascmc = swe.houses_ex(jd, latitude_deg, longitude_deg, b"W", int(_SWE_FLAGS))
    return _normalize_angle(ascmc[0])


def _build_lagna_chart(
    moment_local: datetime,
    latitude_deg: float,
    longitude_deg: float,
) -> PanchangLagnaChart:
    sidereal_ascendant = _ascendant_longitude(moment_local, latitude_deg, longitude_deg)
    ascendant_sign_index = int(sidereal_ascendant // 30)
    ascendant_degree = round(sidereal_ascendant % 30, 2)
    houses = [
        PanchangLagnaHouse(
            house=house_number,
            sign=RASHI_NAMES[(ascendant_sign_index + house_number - 1) % 12],
            is_ascendant=house_number == 1,
        )
        for house_number in range(1, 13)
    ]
    return PanchangLagnaChart(
        ascendant_sign=RASHI_NAMES[ascendant_sign_index],
        ascendant_degree=ascendant_degree,
        houses=houses,
    )


def _build_daily_response(
    base_date: date,
    location: PanchangLocation,
    calendar_variant: CalendarVariant,
    region: RegionCode,
) -> PanchangDailyResponse:
    indexes, context = _day_indexes(base_date, location, calendar_variant)
    astro: DailyAstronomy = context["astro"]
    paksha     = _paksha_from_tithi(indexes["tithi"])
    tithi_name = f"{paksha} {TITHI_NAMES[indexes['tithi']]}"
    tithi_start,  tithi_end   = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "tithi",     indexes["tithi"])
    nak_start,    nak_end     = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "nakshatra", indexes["nakshatra"])
    yoga_start,   yoga_end    = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "yoga",      indexes["yoga"])
    karana_start, karana_end  = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "karana",    indexes["karana"])
    isoweekday = base_date.isoweekday()
    try:
        lagna_chart = _build_lagna_chart(astro.sunrise, location.latitude, location.longitude)
    except Exception:
        lagna_chart = None
    return PanchangDailyResponse(
        date=base_date.isoformat(),
        location=location,
        summary=PanchangSummary(
            weekday=base_date.strftime("%A"),
            tithi=tithi_name,
            nakshatra=NAKSHATRA_NAMES[indexes["nakshatra"]],
            yoga=YOGA_NAMES[indexes["yoga"]],
            karana=KARANA_NAMES[indexes["karana"]],
            # ── seconds included in sunrise/sunset/moonrise/moonset ──────────
            sunrise=astro.sunrise.strftime("%H:%M:%S"),
            sunset=astro.sunset.strftime("%H:%M:%S"),
            moonrise=_fmt_hhmmss(astro.moonrise),
            moonset=_fmt_hhmmss(astro.moonset),
        ),
        panchang=PanchangDetail(
            paksha=paksha,
            lunar_month=LUNAR_MONTHS[indexes["lunar_month"]],
            moon_sign=RASHI_NAMES[indexes["moon_sign"]],
            sun_sign=RASHI_NAMES[indexes["sun_sign"]],
            samvat=_samvat_label(base_date),
            tithi=PanchangSegment(    name=tithi_name,                               index=indexes["tithi"]     + 1, start=tithi_start,  end=tithi_end),
            nakshatra=PanchangSegment(name=NAKSHATRA_NAMES[indexes["nakshatra"]],    index=indexes["nakshatra"] + 1, start=nak_start,    end=nak_end),
            yoga=PanchangSegment(     name=YOGA_NAMES[indexes["yoga"]],              index=indexes["yoga"]      + 1, start=yoga_start,   end=yoga_end),
            karana=PanchangSegment(   name=KARANA_NAMES[indexes["karana"]],          index=indexes["karana"]    + 1, start=karana_start, end=karana_end),
        ),
        lagna_chart=lagna_chart,
        special_yogas=_special_yogas(NAKSHATRA_NAMES[indexes["nakshatra"]], isoweekday),
        day_quality_windows=_day_quality_windows(astro.sunrise, astro.sunset, isoweekday, astro.moon_longitude),
        observances=_observances_for_day(base_date, indexes, tithi_name),
        related_links=_related_links(base_date, location),
        meta=_meta(calendar_variant, region),
    )


def _build_calendar_response(
    year: int, month: int,
    location: PanchangLocation,
    calendar_variant: CalendarVariant,
    region: RegionCode,
) -> PanchangCalendarResponse:
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12.")
    month_days = calendar.monthrange(year, month)[1]
    days: list[PanchangCalendarDay] = []
    for day_number in range(1, month_days + 1):
        current_date = date(year, month, day_number)
        indexes, _ = _day_indexes(current_date, location, calendar_variant)
        tithi_label = f"{_paksha_from_tithi(indexes['tithi'])} {TITHI_NAMES[indexes['tithi']]}"
        days.append(PanchangCalendarDay(
            date=current_date.isoformat(), day=day_number,
            weekday=current_date.strftime("%A"), tithi=tithi_label,
            observances=_observances_for_day(current_date, indexes, tithi_label),
        ))
    return PanchangCalendarResponse(
        year=year, month=month, location=location,
        calendar_variant=calendar_variant, region=region,
        month_label=datetime(year, month, 1).strftime("%B %Y"),
        days=days, meta=_meta(calendar_variant, region),
    )


def _build_festival_list(
    year: int, location: PanchangLocation,
    month: int | None,
    calendar_variant: CalendarVariant,
    region: RegionCode,
) -> PanchangFestivalListResponse:
    months = [month] if month else list(range(1, 13))
    items: list[PanchangObservance] = []
    for current_month in months:
        month_days = calendar.monthrange(year, current_month)[1]
        for day_number in range(1, month_days + 1):
            current_date = date(year, current_month, day_number)
            indexes, _ = _day_indexes(current_date, location, calendar_variant)
            tithi_label = f"{_paksha_from_tithi(indexes['tithi'])} {TITHI_NAMES[indexes['tithi']]}"
            items.extend(_observances_for_day(current_date, indexes, tithi_label))
    unique_items: dict[tuple, PanchangObservance] = {}
    for item in items:
        unique_items[(item.slug, item.date)] = item
    return PanchangFestivalListResponse(
        year=year, month=month, location=location,
        items=sorted(unique_items.values(), key=lambda i: (i.date, -i.priority, i.name)),
        meta=_meta(calendar_variant, region),
    )


def _build_choghadiya(
    base_date: date, location: PanchangLocation, calendar_variant: CalendarVariant, region: RegionCode,
) -> ChoghadiyaResponse:
    tz = ZoneInfo(location.timezone)
    sunrise, sunset, _, _ = _sunrise_sunset_moonrise_moonset(
        base_date, location.latitude, location.longitude, location.timezone,
    )
    # Next-day sunrise for night slot duration
    next_date = base_date + timedelta(days=1)
    next_sunrise, _, _, _ = _sunrise_sunset_moonrise_moonset(
        next_date, location.latitude, location.longitude, location.timezone,
    )
    isoweekday = base_date.isoweekday()
    day_names   = _DAY_CHOG[isoweekday]
    night_names = _NIGHT_CHOG[isoweekday]

    day_dur_sec   = (sunset      - sunrise).total_seconds() / 8
    night_dur_sec = (next_sunrise - sunset).total_seconds() / 8

    def _make_slots(names: list[str], anchor: datetime, dur_sec: float) -> list[ChoghadiyaSlot]:
        slots = []
        for i, name in enumerate(names):
            start = anchor + timedelta(seconds=i * dur_sec)
            end   = anchor + timedelta(seconds=(i + 1) * dur_sec)
            slots.append(ChoghadiyaSlot(
                index=i + 1,
                name=name,
                ruler=_CHOG_RULER[name],
                quality=_CHOG_QUALITY[name],
                start=start.isoformat(),
                end=end.isoformat(),
            ))
        return slots

    return ChoghadiyaResponse(
        date=base_date.isoformat(),
        location=location,
        sunrise=sunrise.isoformat(),
        sunset=sunset.isoformat(),
        next_sunrise=next_sunrise.isoformat(),
        day_choghadiya=_make_slots(day_names, sunrise, day_dur_sec),
        night_choghadiya=_make_slots(night_names, sunset, night_dur_sec),
        meta=_meta(calendar_variant, region),
    )


def _build_hora_response(
    base_date: date,
    location: PanchangLocation,
    calendar_variant: CalendarVariant,
    region: RegionCode,
) -> HoraResponse:
    sunrise, sunset, _, _ = _sunrise_sunset_moonrise_moonset(
        base_date, location.latitude, location.longitude, location.timezone,
    )
    next_date = base_date + timedelta(days=1)
    next_sunrise, _, _, _ = _sunrise_sunset_moonrise_moonset(
        next_date, location.latitude, location.longitude, location.timezone,
    )

    isoweekday = base_date.isoweekday()
    day_ruler = _WEEKDAY_HORA_RULER[isoweekday]
    start_index = _HORA_SEQUENCE.index(day_ruler)
    planets = [_HORA_SEQUENCE[(start_index + idx) % len(_HORA_SEQUENCE)] for idx in range(24)]

    day_slot_duration = (sunset - sunrise).total_seconds() / 12
    night_slot_duration = (next_sunrise - sunset).total_seconds() / 12

    def _make_slots(
        anchor: datetime,
        duration_seconds: float,
        start_at: int,
        period: Literal["day", "night"],
    ) -> list[HoraSlot]:
        slots: list[HoraSlot] = []
        for offset in range(12):
            start = anchor + timedelta(seconds=offset * duration_seconds)
            end = anchor + timedelta(seconds=(offset + 1) * duration_seconds)
            planet = planets[start_at + offset]
            slots.append(
                HoraSlot(
                    index=start_at + offset + 1,
                    planet=planet,
                    start=start.isoformat(),
                    end=end.isoformat(),
                    quality=_HORA_QUALITY[planet],
                    period=period,
                )
            )
        return slots

    return HoraResponse(
        date=base_date.isoformat(),
        location=location,
        sunrise=sunrise.isoformat(),
        sunset=sunset.isoformat(),
        next_sunrise=next_sunrise.isoformat(),
        day_hora=_make_slots(sunrise, day_slot_duration, 0, "day"),
        night_hora=_make_slots(sunset, night_slot_duration, 12, "night"),
        meta=_meta(calendar_variant, region),
    )


def _build_marriage_muhurat_response(
    year: int,
    calendar_variant: CalendarVariant = "amanta",
    region: RegionCode = "general",
) -> MarriageMuhuratResponse:
    location = DEFAULT_LOCATIONS["new-delhi-india"]
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    day_records: list[dict] = []
    current_date = start_date

    while current_date <= end_date:
        indexes, context = _day_indexes(current_date, location, calendar_variant)
        astro: DailyAstronomy = context["astro"]
        tithi_name = TITHI_NAMES[indexes["tithi"]]
        nakshatra_name = NAKSHATRA_NAMES[indexes["nakshatra"]]
        paksha = _paksha_from_tithi(indexes["tithi"])
        observances = _observances_for_day(current_date, indexes, f"{paksha} {tithi_name}")
        day_records.append({
            "date": current_date,
            "indexes": indexes,
            "paksha": paksha,
            "tithi_name": tithi_name,
            "nakshatra_name": nakshatra_name,
            "nakshatra_pada": _nakshatra_pada(astro.moon_longitude),
            "observances": observances,
        })
        current_date += timedelta(days=1)

    month_starts: list[dict] = []
    for idx, record in enumerate(day_records):
        prev_tithi = day_records[idx - 1]["indexes"]["tithi"] if idx > 0 else None
        if record["indexes"]["tithi"] == 0 and prev_tithi != 0:
            month_starts.append({
                "start": record["date"],
                "lunar_month_index": record["indexes"]["lunar_month"],
            })

    adhik_ranges: list[tuple[date, date]] = []
    for idx, start_info in enumerate(month_starts[:-1]):
        next_info = month_starts[idx + 1]
        if start_info["lunar_month_index"] == next_info["lunar_month_index"]:
            adhik_ranges.append((start_info["start"], next_info["start"] - timedelta(days=1)))

    holi_date = next(
        (
            record["date"]
            for record in day_records
            for observance in record["observances"]
            if observance.slug == "holi"
        ),
        None,
    )
    holashtak_dates = {
        holi_date - timedelta(days=offset)
        for offset in range(1, 9)
    } if holi_date else set()

    ekadashi_dates = {
        record["date"]
        for record in day_records
        if record["indexes"]["tithi"] in {10, 25}
    }
    ekadashi_cooldown_dates: set[date] = set()
    for ekadashi_date in ekadashi_dates:
        for offset in range(1, 4):
            blocked_date = ekadashi_date + timedelta(days=offset)
            if blocked_date.year == year:
                ekadashi_cooldown_dates.add(blocked_date)

    pitru_paksha_dates = {
        record["date"]
        for record in day_records
        if record["paksha"] == "Krishna" and record["indexes"]["lunar_month"] in _MARRIAGE_PITRU_PAKSHA_LUNAR_MONTHS
    }

    def _in_adhik_range(target_date: date) -> bool:
        return any(start <= target_date <= end for start, end in adhik_ranges)

    muhurat_dates: list[MarriageMuhuratDate] = []
    for record in day_records:
        indexes = record["indexes"]
        current_date = record["date"]
        nakshatra_name = record["nakshatra_name"]

        if record["paksha"] != "Shukla":
            continue
        if indexes["tithi"] not in _MARRIAGE_AUSPICIOUS_TITHIS:
            continue
        if nakshatra_name not in _MARRIAGE_AUSPICIOUS_NAKSHATRAS:
            continue
        if nakshatra_name in {"Magha", "Mula"} and record["nakshatra_pada"] == 1:
            continue
        if indexes["sun_sign"] in _MARRIAGE_KHARMAS_SUN_SIGNS:
            continue
        if current_date in holashtak_dates or current_date in ekadashi_cooldown_dates or current_date in pitru_paksha_dates:
            continue
        if _in_adhik_range(current_date):
            continue

        quality = "Highly Auspicious" if nakshatra_name in _MARRIAGE_HIGHLY_AUSPICIOUS_NAKSHATRAS else "Auspicious"
        quality_score = 5 if quality == "Highly Auspicious" else 4
        muhurat_dates.append(MarriageMuhuratDate(
            date=current_date.isoformat(),
            day_of_week=current_date.strftime("%A"),
            month=current_date.month,
            month_label=current_date.strftime("%B"),
            tithi=f"{record['paksha']} {record['tithi_name']}",
            nakshatra=nakshatra_name,
            lunar_month=LUNAR_MONTHS[indexes["lunar_month"]],
            quality=quality,
            quality_score=quality_score,
            notes=_MARRIAGE_NOTES.get(nakshatra_name, "A traditionally supportive marriage combination from the Panchang."),
            panchang_path=f"/panchang/date/{current_date.isoformat()}",
        ))

    month_counts: dict[int, int] = {}
    for item in muhurat_dates:
        month_counts[item.month] = month_counts.get(item.month, 0) + 1

    return MarriageMuhuratResponse(
        year=year,
        location=location,
        count=len(muhurat_dates),
        cached=False,
        computed_at=datetime.now(timezone.utc).isoformat(),
        advisory="Calculated for New Delhi as a national reference. Muhurat timings can shift by 10-30 minutes depending on your city.",
        month_summary=[
            MarriageMuhuratMonthSummary(
                month=month,
                label=datetime(year, month, 1).strftime("%B"),
                count=count,
            )
            for month, count in sorted(month_counts.items())
        ],
        muhurat_dates=muhurat_dates,
        meta=_meta(calendar_variant, region),
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/locations", response_model=list[PanchangLocation])
async def get_locations() -> list[PanchangLocation]:
    """Return the full catalogue of supported Panchang locations (flat list)."""
    return LOCATION_LIST


@router.get("/locations/grouped", response_model=PanchangLocationListResponse)
async def get_locations_grouped() -> PanchangLocationListResponse:
    """Return the location catalogue grouped by country (for city picker components)."""
    return PanchangLocationListResponse(
        groups=[
            PanchangLocationGroup(
                country_code=group["country_code"],
                country_name=group["country_name"],
                locations=[DEFAULT_LOCATIONS[slug] for slug in group["slugs"]],
            )
            for group in LOCATION_GROUPS
        ]
    )


@router.get("/daily", response_model=PanchangDailyResponse)
async def get_daily_panchang(
    date_value: str | None = Query(default=None, alias="date"),
    location_slug: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
    tz: str | None = None,
    calendar_variant: CalendarVariant = "amanta",
    region: RegionCode = "general",
) -> PanchangDailyResponse:
    location = _resolve_location(location_slug=location_slug, lat=lat, lng=lng, tz_name=tz)
    resolved_date = _parse_date(date_value) if date_value else datetime.now(ZoneInfo(location.timezone)).date()
    response = _build_daily_response(resolved_date, location, calendar_variant, region)

    # ── Internal checkpoint PAN-13 ────────────────────────────────────────────
    # Verify all 6 required daily fields are populated in the panchang payload.
    # Runs on every /daily call; logs WARNING for any empty/None field.
    _PAN13_FIELDS = {
        "karana":      getattr(response.panchang.karana, "name", None),
        "paksha":      response.panchang.paksha,
        "lunar_month": response.panchang.lunar_month,
        "moon_sign":   response.panchang.moon_sign,
        "sun_sign":    response.panchang.sun_sign,
        "samvat":      response.panchang.samvat,
    }
    _pan13_missing = [k for k, v in _PAN13_FIELDS.items() if not v]
    if _pan13_missing:
        _log.warning(
            "PAN-13 CHECKPOINT: Missing daily fields %s [date=%s location=%s]",
            _pan13_missing, resolved_date, location.slug,
        )
    else:
        _log.info(
            "PAN-13 OK: All 6 daily fields present [date=%s location=%s]",
            resolved_date, location.slug,
        )
    # ─────────────────────────────────────────────────────────────────────────

    return response


@router.get("/date/{date_value}", response_model=PanchangDailyResponse)
async def get_panchang_by_date(
    date_value: str,
    location_slug: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
    tz: str | None = None,
    calendar_variant: CalendarVariant = "amanta",
    region: RegionCode = "general",
) -> PanchangDailyResponse:
    location = _resolve_location(location_slug=location_slug, lat=lat, lng=lng, tz_name=tz)
    resolved_date = _parse_date(date_value)
    return _build_daily_response(resolved_date, location, calendar_variant, region)


@router.get("/calendar/{year}/{month}", response_model=PanchangCalendarResponse)
async def get_panchang_calendar(
    year: int, month: int,
    location_slug: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
    tz: str | None = None,
    calendar_variant: CalendarVariant = "amanta",
    region: RegionCode = "general",
) -> PanchangCalendarResponse:
    location = _resolve_location(location_slug=location_slug, lat=lat, lng=lng, tz_name=tz)
    return _build_calendar_response(year, month, location, calendar_variant, region)


@router.get("/festivals", response_model=PanchangFestivalListResponse)
async def get_panchang_festivals(
    year: int = Query(default_factory=lambda: datetime.now(timezone.utc).year),
    month: int | None = Query(default=None, ge=1, le=12),
    location_slug: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
    tz: str | None = None,
    calendar_variant: CalendarVariant = "amanta",
    region: RegionCode = "general",
) -> PanchangFestivalListResponse:
    location = _resolve_location(location_slug=location_slug, lat=lat, lng=lng, tz_name=tz)
    return _build_festival_list(year, location, month, calendar_variant, region)


@router.get("/choghadiya", response_model=ChoghadiyaResponse)
async def get_choghadiya(
    date_value: str | None = Query(default=None, alias="date"),
    location_slug: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
    tz: str | None = None,
    calendar_variant: CalendarVariant = "amanta",
    region: RegionCode = "general",
) -> ChoghadiyaResponse:
    location = _resolve_location(location_slug=location_slug, lat=lat, lng=lng, tz_name=tz)
    resolved_date = _parse_date(date_value) if date_value else datetime.now(ZoneInfo(location.timezone)).date()
    return _build_choghadiya(resolved_date, location, calendar_variant, region)


@router.get("/hora", response_model=HoraResponse)
async def get_hora(
    date_value: str | None = Query(default=None, alias="date"),
    location_slug: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
    tz: str | None = None,
    calendar_variant: CalendarVariant = "amanta",
    region: RegionCode = "general",
) -> HoraResponse:
    location = _resolve_location(location_slug=location_slug, lat=lat, lng=lng, tz_name=tz)
    resolved_date = _parse_date(date_value) if date_value else datetime.now(ZoneInfo(location.timezone)).date()
    return _build_hora_response(resolved_date, location, calendar_variant, region)


@router.get("/muhurat/marriage", response_model=MarriageMuhuratResponse)
async def get_marriage_muhurat(
    request: Request,
    year: int = Query(default_factory=lambda: datetime.now(ZoneInfo("Asia/Kolkata")).year, ge=2000, le=2100),
) -> MarriageMuhuratResponse:
    cache_key = f"marriage_muhurat_{year}"
    db = getattr(getattr(request.app, "state", None), "db", None)

    if db is not None:
        try:
            cached_doc = await db.panchang_cache.find_one(
                {"key": cache_key, "engine_version": ENGINE_VERSION},
                {"_id": 0, "payload": 1},
            )
            if cached_doc and cached_doc.get("payload"):
                cached_payload = dict(cached_doc["payload"])
                cached_payload["cached"] = True
                return MarriageMuhuratResponse.model_validate(cached_payload)
        except Exception as exc:
            _log.warning("Marriage muhurat cache read failed for %s: %s", cache_key, exc)

    response = _build_marriage_muhurat_response(year)

    if db is not None:
        try:
            await db.panchang_cache.update_one(
                {"key": cache_key},
                {
                    "$set": {
                        "key": cache_key,
                        "kind": "marriage_muhurat",
                        "year": year,
                        "engine_version": ENGINE_VERSION,
                        "payload": response.model_dump(mode="json"),
                        "updated_at": datetime.now(timezone.utc).isoformat(),
                    }
                },
                upsert=True,
            )
        except Exception as exc:
            _log.warning("Marriage muhurat cache write failed for %s: %s", cache_key, exc)

    return response
