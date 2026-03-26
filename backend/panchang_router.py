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

ENGINE_VERSION = "panchang-router-v7-swiss"
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


class PanchangDailyResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: str
    location: PanchangLocation
    summary: PanchangSummary
    panchang: PanchangDetail
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


# ---------------------------------------------------------------------------
# Location catalogue — India + global diaspora cities
# ---------------------------------------------------------------------------
DEFAULT_LOCATIONS: dict[str, PanchangLocation] = {
    # ── India ──────────────────────────────────────────────────────────────
    "new-delhi-india": PanchangLocation(
        slug="new-delhi-india", label="New Delhi", country="India",
        latitude=28.6139, longitude=77.2090, timezone="Asia/Kolkata",
    ),
    "mumbai-india": PanchangLocation(
        slug="mumbai-india", label="Mumbai", country="India",
        latitude=19.0760, longitude=72.8777, timezone="Asia/Kolkata",
    ),
    "bengaluru-india": PanchangLocation(
        slug="bengaluru-india", label="Bengaluru", country="India",
        latitude=12.9716, longitude=77.5946, timezone="Asia/Kolkata",
    ),
    "kolkata-india": PanchangLocation(
        slug="kolkata-india", label="Kolkata", country="India",
        latitude=22.5726, longitude=88.3639, timezone="Asia/Kolkata",
    ),
    "chennai-india": PanchangLocation(
        slug="chennai-india", label="Chennai", country="India",
        latitude=13.0827, longitude=80.2707, timezone="Asia/Kolkata",
    ),
    "hyderabad-india": PanchangLocation(
        slug="hyderabad-india", label="Hyderabad", country="India",
        latitude=17.3850, longitude=78.4867, timezone="Asia/Kolkata",
    ),
    "ahmedabad-india": PanchangLocation(
        slug="ahmedabad-india", label="Ahmedabad", country="India",
        latitude=23.0225, longitude=72.5714, timezone="Asia/Kolkata",
    ),
    "pune-india": PanchangLocation(
        slug="pune-india", label="Pune", country="India",
        latitude=18.5204, longitude=73.8567, timezone="Asia/Kolkata",
    ),
    "jaipur-india": PanchangLocation(
        slug="jaipur-india", label="Jaipur", country="India",
        latitude=26.9124, longitude=75.7873, timezone="Asia/Kolkata",
    ),
    "varanasi-india": PanchangLocation(
        slug="varanasi-india", label="Varanasi", country="India",
        latitude=25.3176, longitude=82.9739, timezone="Asia/Kolkata",
    ),
    "lucknow-india": PanchangLocation(
        slug="lucknow-india", label="Lucknow", country="India",
        latitude=26.8467, longitude=80.9462, timezone="Asia/Kolkata",
    ),
    "indore-india": PanchangLocation(
        slug="indore-india", label="Indore", country="India",
        latitude=22.7196, longitude=75.8577, timezone="Asia/Kolkata",
    ),
    # ── United States ───────────────────────────────────────────────────────
    "new-york-usa": PanchangLocation(
        slug="new-york-usa", label="New York", country="USA",
        latitude=40.7128, longitude=-74.0060, timezone="America/New_York",
    ),
    "los-angeles-usa": PanchangLocation(
        slug="los-angeles-usa", label="Los Angeles", country="USA",
        latitude=34.0522, longitude=-118.2437, timezone="America/Los_Angeles",
    ),
    "chicago-usa": PanchangLocation(
        slug="chicago-usa", label="Chicago", country="USA",
        latitude=41.8781, longitude=-87.6298, timezone="America/Chicago",
    ),
    "houston-usa": PanchangLocation(
        slug="houston-usa", label="Houston", country="USA",
        latitude=29.7604, longitude=-95.3698, timezone="America/Chicago",
    ),
    "san-francisco-usa": PanchangLocation(
        slug="san-francisco-usa", label="San Francisco", country="USA",
        latitude=37.7749, longitude=-122.4194, timezone="America/Los_Angeles",
    ),
    "dallas-usa": PanchangLocation(
        slug="dallas-usa", label="Dallas", country="USA",
        latitude=32.7767, longitude=-96.7970, timezone="America/Chicago",
    ),
    "seattle-usa": PanchangLocation(
        slug="seattle-usa", label="Seattle", country="USA",
        latitude=47.6062, longitude=-122.3321, timezone="America/Los_Angeles",
    ),
    "atlanta-usa": PanchangLocation(
        slug="atlanta-usa", label="Atlanta", country="USA",
        latitude=33.7490, longitude=-84.3880, timezone="America/New_York",
    ),
    # ── United Kingdom ──────────────────────────────────────────────────────
    "london-uk": PanchangLocation(
        slug="london-uk", label="London", country="UK",
        latitude=51.5074, longitude=-0.1278, timezone="Europe/London",
    ),
    "birmingham-uk": PanchangLocation(
        slug="birmingham-uk", label="Birmingham", country="UK",
        latitude=52.4862, longitude=-1.8904, timezone="Europe/London",
    ),
    "leicester-uk": PanchangLocation(
        slug="leicester-uk", label="Leicester", country="UK",
        latitude=52.6369, longitude=-1.1398, timezone="Europe/London",
    ),
    # ── Canada ──────────────────────────────────────────────────────────────
    "toronto-canada": PanchangLocation(
        slug="toronto-canada", label="Toronto", country="Canada",
        latitude=43.6532, longitude=-79.3832, timezone="America/Toronto",
    ),
    "vancouver-canada": PanchangLocation(
        slug="vancouver-canada", label="Vancouver", country="Canada",
        latitude=49.2827, longitude=-123.1207, timezone="America/Vancouver",
    ),
    "brampton-canada": PanchangLocation(
        slug="brampton-canada", label="Brampton", country="Canada",
        latitude=43.7315, longitude=-79.7624, timezone="America/Toronto",
    ),
    # ── UAE ─────────────────────────────────────────────────────────────────
    "dubai-uae": PanchangLocation(
        slug="dubai-uae", label="Dubai", country="UAE",
        latitude=25.2048, longitude=55.2708, timezone="Asia/Dubai",
    ),
    "abu-dhabi-uae": PanchangLocation(
        slug="abu-dhabi-uae", label="Abu Dhabi", country="UAE",
        latitude=24.4539, longitude=54.3773, timezone="Asia/Dubai",
    ),
    # ── Australia ────────────────────────────────────────────────────────────
    "sydney-australia": PanchangLocation(
        slug="sydney-australia", label="Sydney", country="Australia",
        latitude=-33.8688, longitude=151.2093, timezone="Australia/Sydney",
    ),
    "melbourne-australia": PanchangLocation(
        slug="melbourne-australia", label="Melbourne", country="Australia",
        latitude=-37.8136, longitude=144.9631, timezone="Australia/Melbourne",
    ),
    "brisbane-australia": PanchangLocation(
        slug="brisbane-australia", label="Brisbane", country="Australia",
        latitude=-27.4698, longitude=153.0251, timezone="Australia/Brisbane",
    ),
    # ── Singapore ────────────────────────────────────────────────────────────
    "singapore": PanchangLocation(
        slug="singapore", label="Singapore", country="Singapore",
        latitude=1.3521, longitude=103.8198, timezone="Asia/Singapore",
    ),
    # ── Nepal ───────────────────────────────────────────────────────────────
    "kathmandu-nepal": PanchangLocation(
        slug="kathmandu-nepal", label="Kathmandu", country="Nepal",
        latitude=27.7172, longitude=85.3240, timezone="Asia/Kathmandu",
    ),
    # ── New Zealand ──────────────────────────────────────────────────────────
    "auckland-nz": PanchangLocation(
        slug="auckland-nz", label="Auckland", country="New Zealand",
        latitude=-36.8485, longitude=174.7633, timezone="Pacific/Auckland",
    ),
}

# Ordered list for the API locations endpoint
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
    sunrise: datetime
    sunset: datetime
    sun_longitude: float
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
        return PanchangLocation(slug=slug, label="Custom Location", country="Custom", latitude=lat, longitude=lng, timezone=tz_name)
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


def _sunrise_sunset_local(
    base_date: date, latitude: float, longitude: float, tz_name: str
) -> tuple[datetime, datetime]:
    tz = ZoneInfo(tz_name)
    local_midnight = datetime(base_date.year, base_date.month, base_date.day, 0, 0, 0, tzinfo=tz)
    jd_start = _datetime_to_jd(local_midnight.astimezone(timezone.utc))
    geopos   = (longitude, latitude, 0.0)
    atpress, attemp = 1013.25, 15.0
    try:
        ret_rise = swe.rise_trans(jd_start, swe.SUN, swe.CALC_RISE, geopos, atpress, attemp)
        sunrise  = _jd_to_local_dt(ret_rise[1][0], tz)
    except Exception:
        sunrise = local_midnight.replace(hour=6, minute=18)
    try:
        ret_set = swe.rise_trans(jd_start + 0.25, swe.SUN, swe.CALC_SET, geopos, atpress, attemp)
        sunset  = _jd_to_local_dt(ret_set[1][0], tz)
    except Exception:
        sunset = local_midnight.replace(hour=18, minute=35)
    return sunrise, sunset


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
    sunrise, sunset = _sunrise_sunset_local(base_date, latitude, longitude, tz_name)
    sun_longitude, moon_longitude = _moment_longitudes(sunrise)
    return DailyAstronomy(sunrise=sunrise, sunset=sunset,
                          sun_longitude=sun_longitude, moon_longitude=moon_longitude)


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


def _day_quality_windows(sunrise: datetime, sunset: datetime, isoweekday: int) -> list[PanchangTimingWindow]:
    daylight_min = max((sunset - sunrise).total_seconds() / 60, 1.0)
    kaal = daylight_min / 8.0

    def kaal_window(slot: int) -> tuple[str, str]:
        return _window_time(sunrise, (slot - 1) * kaal, kaal)

    rahu_start,   rahu_end   = kaal_window(_RAHU_KAAL_SLOT[isoweekday])
    yama_start,   yama_end   = kaal_window(_YAMAGANDA_SLOT[isoweekday])
    gulika_start, gulika_end = kaal_window(_GULIKA_SLOT[isoweekday])
    abhijit_start, abhijit_end = _window_time(sunrise, daylight_min / 2.0 - 24.0, 48.0)
    muhurta_dur = daylight_min / 15.0
    m1_idx, m2_idx = _DUR_MUHURTA_MUHURTAS[isoweekday]
    dur1_start, dur1_end = _window_time(sunrise, m1_idx * muhurta_dur, muhurta_dur)
    dur2_start, dur2_end = _window_time(sunrise, m2_idx * muhurta_dur, muhurta_dur)

    return [
        PanchangTimingWindow(label="Rahu Kaal",       start=rahu_start,    end=rahu_end,    quality="caution"),
        PanchangTimingWindow(label="Yamaganda",        start=yama_start,    end=yama_end,    quality="caution"),
        PanchangTimingWindow(label="Gulika Kaal",      start=gulika_start,  end=gulika_end,  quality="neutral"),
        PanchangTimingWindow(label="Abhijit Muhurta",  start=abhijit_start, end=abhijit_end, quality="good"),
        PanchangTimingWindow(label="Dur Muhurta",      start=dur1_start,    end=dur1_end,    quality="caution"),
        PanchangTimingWindow(label="Dur Muhurta 2",    start=dur2_start,    end=dur2_end,    quality="caution"),
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
            sunrise=astro.sunrise.strftime("%H:%M"),
            sunset=astro.sunset.strftime("%H:%M"),
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
        day_quality_windows=_day_quality_windows(astro.sunrise, astro.sunset, isoweekday),
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
