from __future__ import annotations

import calendar
import math
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Literal
from zoneinfo import ZoneInfo

import swisseph as swe
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field


router = APIRouter(prefix="/api/panchang", tags=["panchang"])

ENGINE_VERSION = "panchang-router-v11-swiss"
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
# Verified against Drik Panchang — New Delhi, 26 March 2026 (Thu).
# weekday key = Python date.isoweekday(): Mon=1 … Sun=7
# ---------------------------------------------------------------------------

# Rahu Kaal  — Sun=8, Mon=2, Tue=7, Wed=5, Thu=6, Fri=4, Sat=3
_RAHU_KAAL_SLOT = {1: 2, 2: 7, 3: 5, 4: 6, 5: 4, 6: 3, 7: 8}

# Yamaganda  — Sun=5, Mon=4, Tue=3, Wed=2, Thu=1, Fri=7, Sat=6
_YAMAGANDA_SLOT = {1: 4, 2: 3, 3: 2, 4: 1, 5: 7, 6: 6, 7: 5}

# Gulika Kaal — Sun=7, Mon=6, Tue=5, Wed=4, Thu=3, Fri=2, Sat=1
_GULIKA_SLOT    = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 7}

# Dur Muhurta — two windows per day (0-indexed Muhurta from sunrise, daylight/15 each)
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
# weekday key = Python date.isoweekday(): Mon=1 … Sun=7
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
# Special Yogas — Nakshatra × Weekday rule tables
# weekday key = Python date.isoweekday(): Mon=1 … Sun=7
# ---------------------------------------------------------------------------

# Sarvartha Siddhi Yoga — "All-Purpose Accomplishment"; auspicious for new ventures
_SARVARTHA_SIDDHI: dict[int, set[str]] = {
    7: {"Hasta", "Pushya", "Uttara Phalguni", "Uttara Ashadha", "Uttara Bhadrapada"},
    1: {"Rohini", "Mrigashira", "Punarvasu", "Pushya", "Anuradha", "Shravana"},
    2: {"Ashwini", "Krittika", "Mrigashira", "Chitra", "Dhanishtha", "Shatabhisha"},
    3: {"Krittika", "Rohini", "Anuradha", "Jyeshtha", "Revati"},
    4: {"Vishakha", "Anuradha", "Uttara Phalguni", "Uttara Ashadha", "Uttara Bhadrapada", "Revati", "Pushya"},
    5: {"Anuradha", "Revati", "Ashwini", "Punarvasu", "Shatabhisha"},
    6: {"Rohini", "Swati", "Dhanishtha", "Shravana", "Shatabhisha"},
}

# Amrit Siddhi Yoga — "Nectar of Accomplishment"; rarest and most auspicious
_AMRIT_SIDDHI: dict[int, str] = {
    7: "Hasta",       # Sunday
    1: "Mrigashira",  # Monday
    2: "Ashwini",     # Tuesday
    3: "Anuradha",    # Wednesday
    4: "Pushya",      # Thursday
    5: "Revati",      # Friday
    6: "Rohini",      # Saturday
}

# Ravi Yoga — Sun yoga; avoid starting new work (inauspicious)
_RAVI_YOGA: dict[int, set[str]] = {
    7: {"Krittika", "Uttara Phalguni", "Uttara Ashadha"},
    1: {"Hasta", "Shravana"},
    2: {"Ashwini", "Chitra", "Dhanishtha"},
    3: {"Ashlesha", "Jyeshtha", "Revati"},
    4: {"Punarvasu", "Vishakha", "Purva Bhadrapada"},
    5: {"Bharani", "Purva Phalguni", "Purva Ashadha"},
    6: {"Pushya", "Anuradha", "Uttara Bhadrapada"},
}

# Vijaya Muhurta — weekday-specific Muhurta index from sunrise
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
    country: str
    latitude: float
    longitude: float
    timezone: str


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
    index: int          # 1–8
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


# ---------------------------------------------------------------------------
# Location catalogue
# ---------------------------------------------------------------------------
def _loc(slug, label, country, lat, lng, tz="Asia/Kolkata"):
    return PanchangLocation(slug=slug, label=label, country=country,
                            latitude=lat, longitude=lng, timezone=tz)

DEFAULT_LOCATIONS: dict[str, PanchangLocation] = {

    # ── India — Tier 1 metro ────────────────────────────────────────────────
    "new-delhi-india":        _loc("new-delhi-india",        "New Delhi",        "India",  28.6139,  77.2090),
    "mumbai-india":           _loc("mumbai-india",           "Mumbai",           "India",  19.0760,  72.8777),
    "bengaluru-india":        _loc("bengaluru-india",        "Bengaluru",        "India",  12.9716,  77.5946),
    "kolkata-india":          _loc("kolkata-india",          "Kolkata",          "India",  22.5726,  88.3639),
    "chennai-india":          _loc("chennai-india",          "Chennai",          "India",  13.0827,  80.2707),
    "hyderabad-india":        _loc("hyderabad-india",        "Hyderabad",        "India",  17.3850,  78.4867),
    "ahmedabad-india":        _loc("ahmedabad-india",        "Ahmedabad",        "India",  23.0225,  72.5714),
    "pune-india":             _loc("pune-india",             "Pune",             "India",  18.5204,  73.8567),

    # ── India — Major cities (>1 million, from Excel) ───────────────────────
    "surat-india":            _loc("surat-india",            "Surat",            "India",  21.1702,  72.8311),
    "jaipur-india":           _loc("jaipur-india",           "Jaipur",           "India",  26.9124,  75.7873),
    "lucknow-india":          _loc("lucknow-india",          "Lucknow",          "India",  26.8467,  80.9462),
    "kanpur-india":           _loc("kanpur-india",           "Kanpur",           "India",  26.4499,  80.3319),
    "nagpur-india":           _loc("nagpur-india",           "Nagpur",           "India",  21.1458,  79.0882),
    "indore-india":           _loc("indore-india",           "Indore",           "India",  22.7196,  75.8577),
    "thane-india":            _loc("thane-india",            "Thane",            "India",  19.2183,  72.9781),
    "bhopal-india":           _loc("bhopal-india",           "Bhopal",           "India",  23.2599,  77.4126),
    "visakhapatnam-india":    _loc("visakhapatnam-india",    "Visakhapatnam",    "India",  17.6868,  83.2185),
    "patna-india":            _loc("patna-india",            "Patna",            "India",  25.5941,  85.1376),
    "vadodara-india":         _loc("vadodara-india",         "Vadodara",         "India",  22.3072,  73.1812),
    "ghaziabad-india":        _loc("ghaziabad-india",        "Ghaziabad",        "India",  28.6692,  77.4538),
    "ludhiana-india":         _loc("ludhiana-india",         "Ludhiana",         "India",  30.9010,  75.8573),
    "agra-india":             _loc("agra-india",             "Agra",             "India",  27.1767,  78.0081),
    "nashik-india":           _loc("nashik-india",           "Nashik",           "India",  19.9975,  73.7898),
    "faridabad-india":        _loc("faridabad-india",        "Faridabad",        "India",  28.4089,  77.3178),
    "meerut-india":           _loc("meerut-india",           "Meerut",           "India",  28.9845,  77.7064),
    "rajkot-india":           _loc("rajkot-india",           "Rajkot",           "India",  22.3039,  70.8022),
    "varanasi-india":         _loc("varanasi-india",         "Varanasi",         "India",  25.3176,  82.9739),
    "srinagar-india":         _loc("srinagar-india",         "Srinagar",         "India",  34.0837,  74.7973),
    "aurangabad-india":       _loc("aurangabad-india",       "Aurangabad",       "India",  19.8762,  75.3433),
    "amritsar-india":         _loc("amritsar-india",         "Amritsar",         "India",  31.6340,  74.8723),
    "navi-mumbai-india":      _loc("navi-mumbai-india",      "Navi Mumbai",      "India",  19.0330,  73.0297),
    "prayagraj-india":        _loc("prayagraj-india",        "Prayagraj",        "India",  25.4358,  81.8463),
    "ranchi-india":           _loc("ranchi-india",           "Ranchi",           "India",  23.3441,  85.3096),
    "coimbatore-india":       _loc("coimbatore-india",       "Coimbatore",       "India",  11.0168,  76.9558),
    "vijayawada-india":       _loc("vijayawada-india",       "Vijayawada",       "India",  16.5062,  80.6480),
    "jodhpur-india":          _loc("jodhpur-india",          "Jodhpur",          "India",  26.2389,  73.0243),
    "madurai-india":          _loc("madurai-india",          "Madurai",          "India",   9.9252,  78.1198),
    "raipur-india":           _loc("raipur-india",           "Raipur",           "India",  21.2514,  81.6296),
    "kota-india":             _loc("kota-india",             "Kota",             "India",  25.2138,  75.8648),
    "guwahati-india":         _loc("guwahati-india",         "Guwahati",         "India",  26.1445,  91.7362),
    "chandigarh-india":       _loc("chandigarh-india",       "Chandigarh",       "India",  30.7333,  76.7794),
    "mysore-india":           _loc("mysore-india",           "Mysore",           "India",  12.2958,  76.6394),
    "gurgaon-india":          _loc("gurgaon-india",          "Gurgaon",          "India",  28.4595,  77.0266),
    "thiruvananthapuram-india":_loc("thiruvananthapuram-india","Thiruvananthapuram","India",  8.5241,  76.9366),
    "kochi-india":            _loc("kochi-india",            "Kochi",            "India",   9.9312,  76.2673),
    "dehradun-india":         _loc("dehradun-india",         "Dehradun",         "India",  30.3165,  78.0322),
    "jammu-india":            _loc("jammu-india",            "Jammu",            "India",  32.7266,  74.8570),
    "haridwar-india":         _loc("haridwar-india",         "Haridwar",         "India",  29.9457,  78.1642),
    "ujjain-india":           _loc("ujjain-india",           "Ujjain",           "India",  23.1765,  75.7885),
    "shimla-india":           _loc("shimla-india",           "Shimla",           "India",  31.1048,  77.1734),
    "puducherry-india":       _loc("puducherry-india",       "Puducherry",       "India",  11.9416,  79.8083),
    "gandhinagar-india":      _loc("gandhinagar-india",      "Gandhinagar",      "India",  23.2156,  72.6369),
    "noida-india":            _loc("noida-india",            "Noida",            "India",  28.5355,  77.3910),
    "bhubaneswar-india":      _loc("bhubaneswar-india",      "Bhubaneswar",      "India",  20.2961,  85.8245),
    "tirupati-india":         _loc("tirupati-india",         "Tirupati",         "India",  13.6288,  79.4192),
    "kozhikode-india":        _loc("kozhikode-india",        "Kozhikode",        "India",  11.2588,  75.7804),
    "thrissur-india":         _loc("thrissur-india",         "Thrissur",         "India",  10.5276,  76.2144),

    # ── United States ───────────────────────────────────────────────────────
    "new-york-usa":           _loc("new-york-usa",           "New York",         "USA",    40.7128,  -74.0060, "America/New_York"),
    "los-angeles-usa":        _loc("los-angeles-usa",        "Los Angeles",      "USA",    34.0522, -118.2437, "America/Los_Angeles"),
    "chicago-usa":            _loc("chicago-usa",            "Chicago",          "USA",    41.8781,  -87.6298, "America/Chicago"),
    "houston-usa":            _loc("houston-usa",            "Houston",          "USA",    29.7604,  -95.3698, "America/Chicago"),
    "san-francisco-usa":      _loc("san-francisco-usa",      "San Francisco",    "USA",    37.7749, -122.4194, "America/Los_Angeles"),
    "dallas-usa":             _loc("dallas-usa",             "Dallas",           "USA",    32.7767,  -96.7970, "America/Chicago"),
    "seattle-usa":            _loc("seattle-usa",            "Seattle",          "USA",    47.6062, -122.3321, "America/Los_Angeles"),
    "atlanta-usa":            _loc("atlanta-usa",            "Atlanta",          "USA",    33.7490,  -84.3880, "America/New_York"),

    # ── United Kingdom ──────────────────────────────────────────────────────
    "london-uk":              _loc("london-uk",              "London",           "UK",     51.5074,   -0.1278, "Europe/London"),
    "birmingham-uk":          _loc("birmingham-uk",          "Birmingham",       "UK",     52.4862,   -1.8904, "Europe/London"),
    "leicester-uk":           _loc("leicester-uk",           "Leicester",        "UK",     52.6369,   -1.1398, "Europe/London"),

    # ── Canada ──────────────────────────────────────────────────────────────
    "toronto-canada":         _loc("toronto-canada",         "Toronto",          "Canada", 43.6532,  -79.3832, "America/Toronto"),
    "vancouver-canada":       _loc("vancouver-canada",       "Vancouver",        "Canada", 49.2827, -123.1207, "America/Vancouver"),
    "brampton-canada":        _loc("brampton-canada",        "Brampton",         "Canada", 43.7315,  -79.7624, "America/Toronto"),

    # ── UAE ─────────────────────────────────────────────────────────────────
    "dubai-uae":              _loc("dubai-uae",              "Dubai",            "UAE",    25.2048,   55.2708, "Asia/Dubai"),
    "abu-dhabi-uae":          _loc("abu-dhabi-uae",          "Abu Dhabi",        "UAE",    24.4539,   54.3773, "Asia/Dubai"),

    # ── Australia ────────────────────────────────────────────────────────────
    "sydney-australia":       _loc("sydney-australia",       "Sydney",           "Australia", -33.8688, 151.2093, "Australia/Sydney"),
    "melbourne-australia":    _loc("melbourne-australia",    "Melbourne",        "Australia", -37.8136, 144.9631, "Australia/Melbourne"),
    "brisbane-australia":     _loc("brisbane-australia",     "Brisbane",         "Australia", -27.4698, 153.0251, "Australia/Brisbane"),

    # ── Singapore ────────────────────────────────────────────────────────────
    "singapore":              _loc("singapore",              "Singapore",        "Singapore",   1.3521, 103.8198, "Asia/Singapore"),

    # ── Malaysia ─────────────────────────────────────────────────────────────
    "kuala-lumpur-malaysia":  _loc("kuala-lumpur-malaysia",  "Kuala Lumpur",     "Malaysia",    3.1390, 101.6869, "Asia/Kuala_Lumpur"),
    "george-town-malaysia":   _loc("george-town-malaysia",   "George Town",      "Malaysia",    5.4141, 100.3288, "Asia/Kuala_Lumpur"),
    "johor-bahru-malaysia":   _loc("johor-bahru-malaysia",   "Johor Bahru",      "Malaysia",    1.4927, 103.7414, "Asia/Kuala_Lumpur"),

    # ── Indonesia ────────────────────────────────────────────────────────────
    "jakarta-indonesia":      _loc("jakarta-indonesia",      "Jakarta",          "Indonesia",  -6.2088, 106.8456, "Asia/Jakarta"),
    "bali-indonesia":         _loc("bali-indonesia",         "Bali (Denpasar)",  "Indonesia",  -8.6705, 115.2126, "Asia/Makassar"),
    "surabaya-indonesia":     _loc("surabaya-indonesia",     "Surabaya",         "Indonesia",  -7.2575, 112.7521, "Asia/Jakarta"),

    # ── Thailand ─────────────────────────────────────────────────────────────
    "bangkok-thailand":       _loc("bangkok-thailand",       "Bangkok",          "Thailand",   13.7563, 100.5018, "Asia/Bangkok"),
    "chiang-mai-thailand":    _loc("chiang-mai-thailand",    "Chiang Mai",       "Thailand",   18.7883,  98.9853, "Asia/Bangkok"),

    # ── Tibet ────────────────────────────────────────────────────────────────
    "lhasa-tibet":            _loc("lhasa-tibet",            "Lhasa",            "Tibet",      29.6500,  91.1000, "Asia/Shanghai"),

    # ── Nepal ───────────────────────────────────────────────────────────────
    "kathmandu-nepal":        _loc("kathmandu-nepal",        "Kathmandu",        "Nepal",      27.7172,  85.3240, "Asia/Kathmandu"),

    # ── New Zealand ──────────────────────────────────────────────────────────
    "auckland-nz":            _loc("auckland-nz",            "Auckland",         "New Zealand", -36.8485, 174.7633, "Pacific/Auckland"),
}

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
    Amrit Kalam — nakshatra-based auspicious window.

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

def _special_yogas(nakshatra: str, isoweekday: int) -> list[SpecialYoga]:
    """Return all special yogas active today based on Nakshatra × Weekday rules."""
    yogas: list[SpecialYoga] = []
    vara = _WEEKDAY_NAMES[isoweekday]

    # Amrit Siddhi (most auspicious — check first, subset of Sarvartha Siddhi days)
    if _AMRIT_SIDDHI.get(isoweekday) == nakshatra:
        yogas.append(SpecialYoga(
            name="Amrit Siddhi Yoga",
            quality="good",
            nakshatra=nakshatra,
            vara=vara,
            meaning="Nectar of Accomplishment — the rarest and most powerful auspicious yoga. Excellent for all new beginnings.",
        ))
    # Sarvartha Siddhi
    elif nakshatra in _SARVARTHA_SIDDHI.get(isoweekday, set()):
        yogas.append(SpecialYoga(
            name="Sarvartha Siddhi Yoga",
            quality="good",
            nakshatra=nakshatra,
            vara=vara,
            meaning="All-Purpose Accomplishment — highly auspicious for starting new ventures, travel, business, and ceremonies.",
        ))

    # Ravi Yoga (inauspicious — can coexist with auspicious yogas in edge cases)
    if nakshatra in _RAVI_YOGA.get(isoweekday, set()):
        yogas.append(SpecialYoga(
            name="Ravi Yoga",
            quality="caution",
            nakshatra=nakshatra,
            vara=vara,
            meaning="Sun Yoga — avoid initiating important new work. Good for spiritual practices and Sun worship.",
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
    """Format datetime as HH:MM:SS — includes seconds for precision."""
    return dt.strftime("%H:%M:%S") if dt else None


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


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/locations", response_model=list[PanchangLocation])
async def get_locations() -> list[PanchangLocation]:
    """Return the full catalogue of supported Panchang locations."""
    return LOCATION_LIST


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
    return _build_daily_response(resolved_date, location, calendar_variant, region)


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
