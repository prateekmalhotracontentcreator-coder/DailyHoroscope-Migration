from __future__ import annotations

import calendar
import math
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Literal
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field


router = APIRouter(prefix="/api/panchang", tags=["panchang"])

ENGINE_VERSION = "panchang-router-v1"
CalendarVariant = Literal["amanta", "purnimanta"]
RegionCode = Literal["general", "north_india", "south_india", "western_india"]
ObservanceType = Literal["festival", "vrat", "observance"]
TimingQuality = Literal["good", "neutral", "caution"]


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


DEFAULT_LOCATIONS = {
    "new-delhi-india": PanchangLocation(slug="new-delhi-india", label="New Delhi, India", latitude=28.6139, longitude=77.2090, timezone="Asia/Kolkata"),
    "mumbai-india": PanchangLocation(slug="mumbai-india", label="Mumbai, India", latitude=19.0760, longitude=72.8777, timezone="Asia/Kolkata"),
    "bengaluru-india": PanchangLocation(slug="bengaluru-india", label="Bengaluru, India", latitude=12.9716, longitude=77.5946, timezone="Asia/Kolkata"),
    "kolkata-india": PanchangLocation(slug="kolkata-india", label="Kolkata, India", latitude=22.5726, longitude=88.3639, timezone="Asia/Kolkata"),
}

TITHI_NAMES = ["Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima","Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Amavasya"]
NAKSHATRA_NAMES = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishtha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]
YOGA_NAMES = ["Vishkambha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda","Sukarma","Dhriti","Shoola","Ganda","Vriddhi","Dhruva","Vyaghata","Harshana","Vajra","Siddhi","Vyatipata","Variyana","Parigha","Shiva","Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti"]
KARANA_NAMES = ["Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti","Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti","Shakuni","Chatushpada","Naga","Kimstughna"]
RASHI_NAMES = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya","Tula","Vrischika","Dhanu","Makara","Kumbha","Meena"]
LUNAR_MONTHS = ["Chaitra","Vaishakha","Jyeshtha","Ashadha","Shravana","Bhadrapada","Ashwin","Kartika","Margashirsha","Pausha","Magha","Phalguna"]
OBSERVANCE_RULES = [
    {"slug": "ekadashi", "name": "Ekadashi", "observance_type": "vrat", "tithi_indexes": [10, 25], "month_indexes": None, "priority": 2},
    {"slug": "pradosh-vrat", "name": "Pradosh Vrat", "observance_type": "vrat", "tithi_indexes": [12, 27], "month_indexes": None, "priority": 2},
    {"slug": "purnima", "name": "Purnima", "observance_type": "observance", "tithi_indexes": [14], "month_indexes": None, "priority": 2},
    {"slug": "amavasya", "name": "Amavasya", "observance_type": "observance", "tithi_indexes": [29], "month_indexes": None, "priority": 2},
    {"slug": "maha-shivaratri", "name": "Maha Shivaratri", "observance_type": "festival", "tithi_indexes": [28], "month_indexes": [10], "priority": 3},
    {"slug": "janmashtami", "name": "Janmashtami", "observance_type": "festival", "tithi_indexes": [22], "month_indexes": [4], "priority": 3},
    {"slug": "rama-navami", "name": "Rama Navami", "observance_type": "festival", "tithi_indexes": [8], "month_indexes": [0], "priority": 3},
    {"slug": "holi", "name": "Holi", "observance_type": "festival", "tithi_indexes": [14], "month_indexes": [11], "priority": 3},
    {"slug": "diwali", "name": "Diwali", "observance_type": "festival", "tithi_indexes": [29], "month_indexes": [7], "priority": 3},
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

def _resolve_location(location_slug=None, lat=None, lng=None, tz_name=None):
    if location_slug and location_slug in DEFAULT_LOCATIONS:
        return DEFAULT_LOCATIONS[location_slug]
    if lat is not None and lng is not None and tz_name:
        return PanchangLocation(slug="custom-" + str(round(lat, 3)).replace(".", "-") + "-" + str(round(lng, 3)).replace(".", "-"), label="Custom Location", latitude=lat, longitude=lng, timezone=tz_name)
    return DEFAULT_LOCATIONS["new-delhi-india"]

def _julian_day(moment_utc: datetime) -> float:
    year, month = moment_utc.year, moment_utc.month
    day_fraction = moment_utc.day + (moment_utc.hour + moment_utc.minute / 60 + moment_utc.second / 3600) / 24
    if month <= 2:
        year -= 1
        month += 12
    a = year // 100
    b = 2 - a + a // 4
    return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day_fraction + b - 1524.5

def _sun_longitude(jd: float) -> float:
    t = (jd - 2451545.0) / 36525.0
    l0 = _normalize_angle(280.46646 + t * (36000.76983 + 0.0003032 * t))
    m = _normalize_angle(357.52911 + t * (35999.05029 - 0.0001537 * t))
    m_rad = math.radians(m)
    c = (1.914602 - t * (0.004817 + 0.000014 * t)) * math.sin(m_rad) + (0.019993 - 0.000101 * t) * math.sin(2 * m_rad) + 0.000289 * math.sin(3 * m_rad)
    return _normalize_angle(l0 + c)

def _moon_longitude(jd: float) -> float:
    t = (jd - 2451545.0) / 36525.0
    l0 = _normalize_angle(218.3164477 + 481267.88123421 * t)
    d = _normalize_angle(297.8501921 + 445267.1114034 * t)
    m = _normalize_angle(357.5291092 + 35999.0502909 * t)
    mp = _normalize_angle(134.9633964 + 477198.8675055 * t)
    f = _normalize_angle(93.2720950 + 483202.0175233 * t)
    longitude = l0
    longitude += 6.289 * math.sin(math.radians(mp))
    longitude += 1.274 * math.sin(math.radians(2 * d - mp))
    longitude += 0.658 * math.sin(math.radians(2 * d))
    longitude += 0.214 * math.sin(math.radians(2 * mp))
    longitude -= 0.186 * math.sin(math.radians(m))
    longitude -= 0.114 * math.sin(math.radians(2 * f))
    longitude += 0.059 * math.sin(math.radians(2 * d - 2 * mp))
    longitude += 0.057 * math.sin(math.radians(2 * d - m - mp))
    longitude += 0.053 * math.sin(math.radians(2 * d + mp))
    longitude += 0.046 * math.sin(math.radians(2 * d - m))
    return _normalize_angle(longitude)

def _equation_of_time_and_declination(day_of_year: int):
    gamma = (2 * math.pi / 365) * (day_of_year - 1)
    equation = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
    declination = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)
    return equation, declination

def _sunrise_sunset_local(base_date: date, latitude: float, longitude: float, tz_name: str):
    tz = ZoneInfo(tz_name)
    local_midday = datetime.combine(base_date, time(12, 0), tzinfo=tz)
    day_of_year = local_midday.timetuple().tm_yday
    equation, declination = _equation_of_time_and_declination(day_of_year)
    lat_rad = math.radians(latitude)
    solar_zenith = math.radians(90.833)
    cos_ha = (math.cos(solar_zenith) / (math.cos(lat_rad) * math.cos(declination))) - math.tan(lat_rad) * math.tan(declination)
    cos_ha = max(-1.0, min(1.0, cos_ha))
    hour_angle = math.degrees(math.acos(cos_ha))
    offset_hours = local_midday.utcoffset().total_seconds() / 3600 if local_midday.utcoffset() else 0.0
    solar_noon = (720 - 4 * longitude - equation + offset_hours * 60) / 1440
    sunrise_fraction = solar_noon - hour_angle * 4 / 1440
    sunset_fraction = solar_noon + hour_angle * 4 / 1440
    day_start = datetime.combine(base_date, time.min, tzinfo=tz)
    return day_start + timedelta(days=sunrise_fraction), day_start + timedelta(days=sunset_fraction)

def _moment_longitudes(moment_local: datetime):
    moment_utc = moment_local.astimezone(timezone.utc)
    jd = _julian_day(moment_utc)
    return _sun_longitude(jd), _moon_longitude(jd)

def _segment_interval(base_date, latitude, longitude, tz_name, metric, start_index):
    tz = ZoneInfo(tz_name)
    start_local = datetime.combine(base_date, time(0, 0), tzinfo=tz)
    end_local = start_local + timedelta(days=1)
    step = timedelta(minutes=20)
    found_end = None
    cursor = start_local + step
    while cursor <= end_local:
        sun_long, moon_long = _moment_longitudes(cursor)
        if metric == "tithi": index = int(_normalize_angle(moon_long - sun_long) // 12)
        elif metric == "nakshatra": index = int(moon_long // (360 / 27))
        elif metric == "yoga": index = int(_normalize_angle(moon_long + sun_long) // (360 / 27))
        else: index = min(int(_normalize_angle(moon_long - sun_long) // 6), 31)
        if index != start_index:
            found_end = cursor
            break
        cursor += step
    return start_local.isoformat(), found_end.isoformat() if found_end else None

def _build_daily_astronomy(base_date, latitude, longitude, tz_name):
    sunrise, sunset = _sunrise_sunset_local(base_date, latitude, longitude, tz_name)
    sun_longitude, moon_longitude = _moment_longitudes(sunrise)
    return DailyAstronomy(sunrise=sunrise, sunset=sunset, sun_longitude=sun_longitude, moon_longitude=moon_longitude)

def _tithi_index(sun_longitude, moon_longitude): return int(_normalize_angle(moon_longitude - sun_longitude) // 12)
def _nakshatra_index(moon_longitude): return int(moon_longitude // (360 / 27))
def _yoga_index(sun_longitude, moon_longitude): return int(_normalize_angle(sun_longitude + moon_longitude) // (360 / 27))
def _karana_index(sun_longitude, moon_longitude): return min(int(_normalize_angle(moon_longitude - sun_longitude) // 6), 31)
def _paksha_from_tithi(index): return "Shukla" if index <= 14 else "Krishna"

def _lunar_month_index(sun_longitude, moon_longitude, calendar_variant):
    solar_month = int(sun_longitude // 30)
    lunation = _tithi_index(sun_longitude, moon_longitude)
    offset = 1 if calendar_variant == "purnimanta" and lunation < 15 else 0
    return (solar_month + 1 + offset) % 12

def _samvat_label(base_date):
    return "Vikram " + str(base_date.year + 57) + " / Shaka " + str(base_date.year - 78)

def _window_time(anchor, offset_minutes, duration_minutes):
    start = anchor + timedelta(minutes=offset_minutes)
    end = start + timedelta(minutes=duration_minutes)
    return start.isoformat(), end.isoformat()

def _day_quality_windows(sunrise, sunset):
    daylight_minutes = int((sunset - sunrise).total_seconds() / 60)
    eighth = max(daylight_minutes // 8, 1)
    rahu_start, rahu_end = _window_time(sunrise, 7 * eighth, eighth)
    yama_start, yama_end = _window_time(sunrise, 4 * eighth, eighth)
    gulika_start, gulika_end = _window_time(sunrise, 5 * eighth, eighth)
    abhijit_start, abhijit_end = _window_time(sunrise, daylight_minutes // 2 - 24, 48)
    dur_start, dur_end = _window_time(sunrise, 2 * eighth, eighth)
    return [
        PanchangTimingWindow(label="Rahu Kaal", start=rahu_start, end=rahu_end, quality="caution"),
        PanchangTimingWindow(label="Yamaganda", start=yama_start, end=yama_end, quality="caution"),
        PanchangTimingWindow(label="Gulika Kaal", start=gulika_start, end=gulika_end, quality="neutral"),
        PanchangTimingWindow(label="Abhijit Muhurta", start=abhijit_start, end=abhijit_end, quality="good"),
        PanchangTimingWindow(label="Dur Muhurta", start=dur_start, end=dur_end, quality="caution"),
    ]

def _day_indexes(base_date, location, calendar_variant):
    astro = _build_daily_astronomy(base_date, location.latitude, location.longitude, location.timezone)
    tithi = _tithi_index(astro.sun_longitude, astro.moon_longitude)
    nakshatra = _nakshatra_index(astro.moon_longitude)
    yoga = _yoga_index(astro.sun_longitude, astro.moon_longitude)
    karana = _karana_index(astro.sun_longitude, astro.moon_longitude)
    lunar_month = _lunar_month_index(astro.sun_longitude, astro.moon_longitude, calendar_variant)
    indexes = {"tithi": tithi, "nakshatra": nakshatra, "yoga": yoga, "karana": karana, "lunar_month": lunar_month, "sun_sign": int(astro.sun_longitude // 30), "moon_sign": int(astro.moon_longitude // 30)}
    return indexes, {"astro": astro}

def _observances_for_day(base_date, indexes, tithi_label):
    items = []
    for rule in OBSERVANCE_RULES:
        if indexes["tithi"] not in rule["tithi_indexes"]: continue
        if rule["month_indexes"] is not None and indexes["lunar_month"] not in rule["month_indexes"]: continue
        items.append(PanchangObservance(slug=rule["slug"], name=rule["name"], observance_type=rule["observance_type"], date=base_date.isoformat(), priority=rule["priority"], summary=rule['name'] + " aligns with " + tithi_label + " in " + LUNAR_MONTHS[indexes['lunar_month']] + "."))
    return sorted(items, key=lambda item: (-item.priority, item.name))

def _related_links(base_date, location):
    previous_day = (base_date - timedelta(days=1)).isoformat()
    next_day = (base_date + timedelta(days=1)).isoformat()
    return [
        PanchangLink(label="Previous Day", href="/panchang/location/" + location.slug + "/date/" + previous_day),
        PanchangLink(label="Tomorrow", href="/panchang/location/" + location.slug + "/date/" + next_day),
        PanchangLink(label="This Month", href="/panchang/calendar/" + str(base_date.year) + "/" + str(base_date.month)),
        PanchangLink(label="Festivals", href="/panchang/festivals?year=" + str(base_date.year) + "&month=" + str(base_date.month)),
    ]

def _meta(calendar_variant, region):
    return PanchangMeta(engine_version=ENGINE_VERSION, generated_at=datetime.now(timezone.utc).isoformat(), calendar_variant=calendar_variant, region=region, persistence_mode="stateless_v1")

def _build_daily_response(base_date, location, calendar_variant, region):
    indexes, context = _day_indexes(base_date, location, calendar_variant)
    astro = context["astro"]
    paksha = _paksha_from_tithi(indexes["tithi"])
    tithi_name = paksha + " " + TITHI_NAMES[indexes["tithi"]]
    tithi_start, tithi_end = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "tithi", indexes["tithi"])
    nak_start, nak_end = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "nakshatra", indexes["nakshatra"])
    yoga_start, yoga_end = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "yoga", indexes["yoga"])
    karana_start, karana_end = _segment_interval(base_date, location.latitude, location.longitude, location.timezone, "karana", indexes["karana"])
    return PanchangDailyResponse(
        date=base_date.isoformat(), location=location,
        summary=PanchangSummary(weekday=base_date.strftime("%A"), tithi=tithi_name, nakshatra=NAKSHATRA_NAMES[indexes["nakshatra"]], yoga=YOGA_NAMES[indexes["yoga"]], karana=KARANA_NAMES[indexes["karana"]], sunrise=astro.sunrise.strftime("%H:%M"), sunset=astro.sunset.strftime("%H:%M")),
        panchang=PanchangDetail(paksha=paksha, lunar_month=LUNAR_MONTHS[indexes["lunar_month"]], moon_sign=RASHI_NAMES[indexes["moon_sign"]], sun_sign=RASHI_NAMES[indexes["sun_sign"]], samvat=_samvat_label(base_date), tithi=PanchangSegment(name=tithi_name, index=indexes["tithi"] + 1, start=tithi_start, end=tithi_end), nakshatra=PanchangSegment(name=NAKSHATRA_NAMES[indexes["nakshatra"]], index=indexes["nakshatra"] + 1, start=nak_start, end=nak_end), yoga=PanchangSegment(name=YOGA_NAMES[indexes["yoga"]], index=indexes["yoga"] + 1, start=yoga_start, end=yoga_end), karana=PanchangSegment(name=KARANA_NAMES[indexes["karana"]], index=indexes["karana"] + 1, start=karana_start, end=karana_end)),
        day_quality_windows=_day_quality_windows(astro.sunrise, astro.sunset),
        observances=_observances_for_day(base_date, indexes, tithi_name),
        related_links=_related_links(base_date, location),
        meta=_meta(calendar_variant, region),
    )

def _build_calendar_response(year, month, location, calendar_variant, region):
    if month < 1 or month > 12: raise HTTPException(status_code=400, detail="Month must be between 1 and 12.")
    month_days = calendar.monthrange(year, month)[1]
    days = []
    for day_number in range(1, month_days + 1):
        current_date = date(year, month, day_number)
        indexes, _ = _day_indexes(current_date, location, calendar_variant)
        tithi_label = _paksha_from_tithi(indexes['tithi']) + " " + TITHI_NAMES[indexes['tithi']]
        days.append(PanchangCalendarDay(date=current_date.isoformat(), day=day_number, weekday=current_date.strftime("%A"), tithi=tithi_label, observances=_observances_for_day(current_date, indexes, tithi_label)))
    return PanchangCalendarResponse(year=year, month=month, location=location, calendar_variant=calendar_variant, region=region, month_label=datetime(year, month, 1).strftime("%B %Y"), days=days, meta=_meta(calendar_variant, region))

def _build_festival_list(year, location, month, calendar_variant, region):
    months = [month] if month else list(range(1, 13))
    items = []
    for current_month in months:
        month_days = calendar.monthrange(year, current_month)[1]
        for day_number in range(1, month_days + 1):
            current_date = date(year, current_month, day_number)
            indexes, _ = _day_indexes(current_date, location, calendar_variant)
            tithi_label = _paksha_from_tithi(indexes['tithi']) + " " + TITHI_NAMES[indexes['tithi']]
            items.extend(_observances_for_day(current_date, indexes, tithi_label))
    unique_items = {}
    for item in items:
        unique_items[(item.slug, item.date)] = item
    return PanchangFestivalListResponse(year=year, month=month, location=location, items=sorted(unique_items.values(), key=lambda item: (item.date, -item.priority, item.name)), meta=_meta(calendar_variant, region))


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
