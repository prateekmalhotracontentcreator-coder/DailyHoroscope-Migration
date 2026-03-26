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

ENGINE_VERSION = "panchang-router-v5-swiss"
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
# Traditional Vedic timing slot tables
# ---------------------------------------------------------------------------
# Python's date.weekday(): Monday=0 ... Sunday=6
# Vedic tables are indexed by weekday in the same Monday=0 convention.
#
# Slot index = which 1/8th daylight block (0-indexed from sunrise) the period
# occupies.  slot_0 = sunrise..sunrise+1kaal, slot_1 = next kaal, etc.
#
# Rahu Kaal slots  (traditional mnemonic: "Mother Saw Father Wearing The Turban Smartly")
#   Mon=1, Sat=2, Fri=3, Wed=4, Thu=5, Tue=6, Sun=7
#   → Python weekday mapping: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
_RAHU_KAAL_SLOT = {0: 1, 1: 6, 2: 4, 3: 5, 4: 3, 5: 2, 6: 7}

# Yamaganda slots (traditional: Sun=5, Mon=4, Tue=3, Wed=2, Thu=6, Fri=8, Sat=7)
# Converting to 0-indexed (subtract 1) and capping at 7:
#   Sun→4, Mon→3, Tue→2, Wed→1, Thu→5, Fri→7, Sat→6
#   Python weekday: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
_YAMAGANDA_SLOT = {0: 3, 1: 2, 2: 1, 3: 5, 4: 7, 5: 6, 6: 4}

# Gulika (Mandi) slots  (traditional: Sun=7, Mon=6, Tue=5, Wed=4, Thu=3, Fri=2, Sat=1)
# 0-indexed: Sun→6, Mon→5, Tue→4, Wed→3, Thu→2, Fri→1, Sat→0
_GULIKA_SLOT = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1, 5: 0, 6: 6}

# Dur Muhurta — two inauspicious periods per day, each ~48 min.
# Expressed as minutes from sunrise.  Values from Drik Panchang reference.
# (offset_from_sunrise_min, duration_min)
# Mon: 11:51-12:39 ≈ midday block; mapping to offsets from sunrise at 6:18 = 333 min
# Traditional fixed clock offsets converted to "approx slot" approach:
# Simpler and more accurate: Dur Muhurta occupies specific 48-min windows
# referenced from solar noon rather than sunrise.
# We use (offset_before_noon_min, offset_after_noon_min) pattern:
_DUR_MUHURTA_OFFSETS: dict[int, list[tuple[int, int]]] = {
    # (start_offset_from_sunrise_minutes, duration_minutes)
    # Sun
    6: [(120, 48), (510, 48)],
    # Mon  
    0: [(330, 48)],
    # Tue
    1: [(45, 48), (570, 48)],
    # Wed
    2: [(240, 48)],
    # Thu
    3: [(240, 48)],
    # Fri
    4: [(45, 48)],
    # Sat
    5: [(330, 48), (570, 48)],
}


class PanchangLocation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    slug: str
    label: str
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


DEFAULT_LOCATIONS: dict[str, PanchangLocation] = {
    "new-delhi-india": PanchangLocation(
        slug="new-delhi-india", label="New Delhi, India",
        latitude=28.6139, longitude=77.2090, timezone="Asia/Kolkata",
    ),
    "mumbai-india": PanchangLocation(
        slug="mumbai-india", label="Mumbai, India",
        latitude=19.0760, longitude=72.8777, timezone="Asia/Kolkata",
    ),
    "bengaluru-india": PanchangLocation(
        slug="bengaluru-india", label="Bengaluru, India",
        latitude=12.9716, longitude=77.5946, timezone="Asia/Kolkata",
    ),
    "kolkata-india": PanchangLocation(
        slug="kolkata-india", label="Kolkata, India",
        latitude=22.5726, longitude=88.3639, timezone="Asia/Kolkata",
    ),
    "new-york-usa": PanchangLocation(
        slug="new-york-usa", label="New York, USA",
        latitude=40.7128, longitude=-74.0060, timezone="America/New_York",
    ),
    "london-uk": PanchangLocation(
        slug="london-uk", label="London, UK",
        latitude=51.5074, longitude=-0.1278, timezone="Europe/London",
    ),
    "dubai-uae": PanchangLocation(
        slug="dubai-uae", label="Dubai, UAE",
        latitude=25.2048, longitude=55.2708, timezone="Asia/Dubai",
    ),
    "singapore": PanchangLocation(
        slug="singapore", label="Singapore",
        latitude=1.3521, longitude=103.8198, timezone="Asia/Singapore",
    ),
    "toronto-canada": PanchangLocation(
        slug="toronto-canada", label="Toronto, Canada",
        latitude=43.6532, longitude=-79.3832, timezone="America/Toronto",
    ),
    "sydney-australia": PanchangLocation(
        slug="sydney-australia", label="Sydney, Australia",
        latitude=-33.8688, longitude=151.2093, timezone="Australia/Sydney",
    ),
    "kathmandu-nepal": PanchangLocation(
        slug="kathmandu-nepal", label="Kathmandu, Nepal",
        latitude=27.7172, longitude=85.3240, timezone="Asia/Kathmandu",
    ),
    "riyadh-saudi-arabia": PanchangLocation(
        slug="riyadh-saudi-arabia", label="Riyadh, Saudi Arabia",
        latitude=24.6877, longitude=46.7219, timezone="Asia/Riyadh",
    ),
}

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
        return PanchangLocation(slug=slug, label="Custom Location", latitude=lat, longitude=lng, timezone=tz_name)
    return DEFAULT_LOCATIONS["new-delhi-india"]


def _datetime_to_jd(dt_utc: datetime) -> float:
    """Convert a UTC datetime to Julian Day number."""
    return swe.julday(
        dt_utc.year, dt_utc.month, dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
    )


def _sun_longitude(jd: float) -> float:
    result = swe.calc_ut(jd, int(swe.SUN), int(_SWE_FLAGS))
    return _normalize_angle(result[0][0])


def _moon_longitude(jd: float) -> float:
    result = swe.calc_ut(jd, int(swe.MOON), int(_SWE_FLAGS))
    return _normalize_angle(result[0][0])


def _sunrise_sunset_local(
    base_date: date, latitude: float, longitude: float, tz_name: str
) -> tuple[datetime, datetime]:
    """
    Compute sunrise and sunset using NOAA solar algorithm.
    Returns local-timezone-aware datetimes.
    """
    tz = ZoneInfo(tz_name)

    def _solar_noon_utc_h(jd: float, lon: float) -> float:
        n = jd - 2451545.0
        L = (280.460 + 0.9856474 * n) % 360.0
        g = math.radians((357.528 + 0.9856003 * n) % 360.0)
        lam = math.radians(L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g))
        eps = math.radians(23.439 - 0.0000004 * n)
        RA = math.degrees(math.atan2(math.cos(eps) * math.sin(lam), math.cos(lam))) / 15.0
        eot = 4 * (L / 15.0 - (RA % 24.0))
        return 12.0 - lon / 15.0 - eot / 60.0

    def _hour_angle(lat_deg: float, jd: float) -> float:
        n = jd - 2451545.0
        L = (280.460 + 0.9856474 * n) % 360.0
        g = math.radians((357.528 + 0.9856003 * n) % 360.0)
        lam = math.radians(L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g))
        eps = math.radians(23.439 - 0.0000004 * n)
        dec = math.asin(math.sin(eps) * math.sin(lam))
        lat = math.radians(lat_deg)
        cos_ha = (math.sin(math.radians(-0.8333)) - math.sin(lat) * math.sin(dec)) / (math.cos(lat) * math.cos(dec))
        return math.degrees(math.acos(max(-1.0, min(1.0, cos_ha))))

    dt_noon_utc = datetime(base_date.year, base_date.month, base_date.day, 12, 0, 0, tzinfo=timezone.utc)
    jd_noon = _datetime_to_jd(dt_noon_utc)
    solar_noon_h = _solar_noon_utc_h(jd_noon, longitude)
    ha_h = _hour_angle(latitude, jd_noon) / 15.0

    def hours_to_dt(h: float) -> datetime:
        total_min = int(round(h * 60))
        hr = (total_min // 60) % 24
        mn = total_min % 60
        return datetime(base_date.year, base_date.month, base_date.day, hr, mn, 0, tzinfo=timezone.utc).astimezone(tz)

    return hours_to_dt(solar_noon_h - ha_h), hours_to_dt(solar_noon_h + ha_h)


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
    return DailyAstronomy(
        sunrise=sunrise, sunset=sunset,
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
    lunation = _tithi_index(sun_longitude, moon_longitude)
    offset = 1 if calendar_variant == "purnimanta" and lunation < 15 else 0
    return (solar_month + 1 + offset) % 12

def _samvat_label(base_date: date) -> str:
    return f"Vikram {base_date.year + 57} / Shaka {base_date.year - 78}"

def _window_time(anchor: datetime, offset_minutes: int, duration_minutes: int) -> tuple[str, str]:
    start = anchor + timedelta(minutes=offset_minutes)
    end = start + timedelta(minutes=duration_minutes)
    return start.isoformat(), end.isoformat()


def _day_quality_windows(sunrise: datetime, sunset: datetime, weekday: int) -> list[PanchangTimingWindow]:
    """
    Compute timing windows using weekday-specific slots per traditional Vedic Panchang.
    weekday: Monday=0, Tuesday=1, ..., Sunday=6  (Python date.weekday())
    Each Kaal = 1/8 of total daylight duration.

    Rahu Kaal slot mapping (verified against Drik Panchang reference):
      Mon=slot1, Sat=slot2, Fri=slot3, Wed=slot4, Thu=slot5, Tue=slot6, Sun=slot7

    Dur Muhurta: per-weekday fixed offsets from sunrise (minutes).
    """
    daylight_minutes = int((sunset - sunrise).total_seconds() / 60)
    slot = max(daylight_minutes // 8, 1)

    rahu_slot    = _RAHU_KAAL_SLOT.get(weekday, 7)
    yamagan_slot = _YAMAGANDA_SLOT.get(weekday, 4)
    gulika_slot  = _GULIKA_SLOT.get(weekday, 6)

    rahu_start,   rahu_end   = _window_time(sunrise, rahu_slot    * slot, slot)
    yama_start,   yama_end   = _window_time(sunrise, yamagan_slot * slot, slot)
    gulika_start, gulika_end = _window_time(sunrise, gulika_slot  * slot, slot)

    # Abhijit Muhurta: 48-min window centred on solar noon
    abhijit_start, abhijit_end = _window_time(sunrise, daylight_minutes // 2 - 24, 48)

    # Dur Muhurta: weekday-specific offset(s) from sunrise
    dur_entries = _DUR_MUHURTA_OFFSETS.get(weekday, [(2 * slot, slot)])
    # Use the first entry for the primary Dur Muhurta display
    dur_offset, dur_dur = dur_entries[0]
    dur_start, dur_end = _window_time(sunrise, dur_offset, dur_dur)

    windows = [
        PanchangTimingWindow(label="Rahu Kaal",      start=rahu_start,   end=rahu_end,   quality="caution"),
        PanchangTimingWindow(label="Yamaganda",      start=yama_start,   end=yama_end,   quality="caution"),
        PanchangTimingWindow(label="Gulika Kaal",    start=gulika_start, end=gulika_end, quality="neutral"),
        PanchangTimingWindow(label="Abhijit Muhurta",start=abhijit_start,end=abhijit_end,quality="good"),
        PanchangTimingWindow(label="Dur Muhurta",    start=dur_start,    end=dur_end,    quality="caution"),
    ]

    # If the weekday has a second Dur Muhurta, append it
    if len(dur_entries) > 1:
        dur2_offset, dur2_dur = dur_entries[1]
        dur2_start, dur2_end = _window_time(sunrise, dur2_offset, dur2_dur)
        windows.append(PanchangTimingWindow(label="Dur Muhurta 2", start=dur2_start, end=dur2_end, quality="caution"))

    return windows


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
    paksha = _paksha_from_tithi(indexes["tithi"])
    tithi_name = f"{paksha} {TITHI_NAMES[indexes['tithi']]}"
    tithi_start,  tithi_end   = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "tithi",     indexes["tithi"])
    nak_start,    nak_end     = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "nakshatra", indexes["nakshatra"])
    yoga_start,   yoga_end    = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "yoga",      indexes["yoga"])
    karana_start, karana_end  = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "karana",    indexes["karana"])
    weekday = base_date.weekday()  # Monday=0 ... Sunday=6
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
        day_quality_windows=_day_quality_windows(astro.sunrise, astro.sunset, weekday),
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
    """Explicit per-date Panchang endpoint. Preferred by calendar deep-links."""
    location = _resolve_location(location_slug=location_slug, lat=lat, lng=lng, tz_name=tz)
    resolved_date = _parse_date(date_value)
    return _build_daily_response(resolved_date, location, calendar_variant, region)


@router.get("/locations")
async def get_panchang_locations() -> dict:
    """Return available location slugs and labels."""
    return {
        "locations": [
            {"slug": loc.slug, "label": loc.label, "timezone": loc.timezone}
            for loc in DEFAULT_LOCATIONS.values()
        ]
    }


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
