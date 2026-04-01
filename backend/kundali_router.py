from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from functools import partial
from typing import Any, Literal
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field
import swisseph as swe

from vedic_calculator import (
    NAKSHATRAS,
    PLANET_IDS,
    PLANET_SWE_IDS as PLANET_ID_MAP,
    PLANET_NAMES,
    SIGN_LORDS,
    SIGN_NAMES,
    SIGN_ORDER,
    const,
    geocode_place,
)


router = APIRouter(prefix="/api/lagna-kundali", tags=["lagna-kundali"])

swe.set_sid_mode(swe.SIDM_LAHIRI)
SWE_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

TimePrecision = Literal["exact", "approximate", "unknown"]
ChartCode = Literal[
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10",
    "D11", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60",
]
LayerCode = Literal[
    "graha",
    "upagraha",
    "yoga",
    "vimshottari_dasha",
    "ashtaka_varga",
    "shadbala",
    "bhavabala",
    "bhav_chalit",
]

SUPPORTED_CHARTS: tuple[ChartCode, ...] = (
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10",
    "D11", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60",
)
ENABLED_CHARTS = {"D1", "D9", "D10"}
DEFAULT_LAYER_CODES: tuple[LayerCode, ...] = (
    "graha",
    "upagraha",
    "yoga",
    "vimshottari_dasha",
    "ashtaka_varga",
    "shadbala",
    "bhavabala",
    "bhav_chalit",
)
TEMPLE_DASHA_ORDER = ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"]
DASHA_YEARS = {"Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17, "Ketu": 7, "Venus": 20}
PLANET_ABBR = {
    "Sun (Surya)": "Su",
    "Moon (Chandra)": "Mo",
    "Mars (Mangal)": "Ma",
    "Mercury (Budha)": "Me",
    "Jupiter (Brihaspati)": "Ju",
    "Venus (Shukra)": "Ve",
    "Saturn (Shani)": "Sa",
    "Rahu": "Ra",
    "Ketu": "Ke",
    "Lagna": "Lg",
}
FRIENDLY_NAMES = {
    "Sun (Surya)": "Sun",
    "Moon (Chandra)": "Moon",
    "Mars (Mangal)": "Mars",
    "Mercury (Budha)": "Mercury",
    "Jupiter (Brihaspati)": "Jupiter",
    "Venus (Shukra)": "Venus",
    "Saturn (Shani)": "Saturn",
    "Rahu": "Rahu",
    "Ketu": "Ketu",
    "Lagna": "Lagna",
}
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
BENEFICS = {"Jupiter", "Venus", "Moon"}
MALEFICS = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LagnaKundaliComputeRequest(StrictModel):
    date: str
    time: str | None = None
    time_precision: TimePrecision = "exact"
    place_label: str
    latitude: float | None = None
    longitude: float | None = None
    timezone: str = "Asia/Kolkata"
    requested_chart_codes: list[ChartCode] = Field(default_factory=lambda: ["D1"])
    include_layers: list[LayerCode] = Field(default_factory=lambda: list(DEFAULT_LAYER_CODES))


class ChartDefinition(StrictModel):
    code: ChartCode
    name: str
    short_meaning: str
    enabled: bool
    precision_sensitive: bool


class ChartDefinitionResponse(StrictModel):
    charts: list[ChartDefinition]


class SaveChartResponse(StrictModel):
    chart_id: str
    saved: bool


class MyChartItem(StrictModel):
    chart_id: str
    created_at: str
    place_label: str
    date: str
    time_precision: TimePrecision
    lagna_sign: str
    saved_default_view: dict[str, str]


class MyChartsResponse(StrictModel):
    items: list[MyChartItem]


class ChartLayerResponse(StrictModel):
    chart_id: str
    layer_code: LayerCode
    data: dict[str, Any]


CHART_MEANINGS: dict[ChartCode, str] = {
    "D1": "Rashi chart for body, life pattern, and primary natal framework",
    "D2": "Hora for wealth and finance",
    "D3": "Drekkana for siblings, initiative, and courage",
    "D4": "Chaturthamsha for property and inner stability",
    "D5": "Panchamsha for fame and authority",
    "D6": "Shashthamsha for disease and struggle diagnostics",
    "D7": "Saptamsha for children and creative lineage",
    "D8": "Ashtamsha for longevity and vulnerabilities",
    "D9": "Navamsha for dharma, marriage, and inner strength",
    "D10": "Dashamsha for profession and actions in society",
    "D11": "Ekadashamsha for gains and network patterns",
    "D12": "Dwadashamsha for parents and lineage",
    "D16": "Shodashamsha for luxuries and vehicles",
    "D20": "Vimshamsha for spiritual practice",
    "D24": "Chaturvimshamsha for education and learning",
    "D27": "Saptavimshamsha for strengths and weaknesses",
    "D30": "Trimshamsha for misfortunes and hidden faults",
    "D40": "Chatvarimshamsha for maternal karmic refinement",
    "D45": "Akshavedamsha for paternal karmic refinement",
    "D60": "Shashtiamsha for deep karmic residue",
}

RAMAN_TITLE_OVERRIDES = {
    1: "Gajakesari Yoga",
    2: "Sunapha Yoga",
    3: "Anapha Yoga",
    4: "Anapathya Yoga",
    5: "Kemadruma Yoga",
    6: "Chandra Mangala Yoga",
    7: "Adhi Yoga",
    8: "Vasumathi Yoga",
    9: "Rajalakshana Yoga",
    10: "Vanchana Chora Bheethi Yoga",
    11: "Sakata Yoga",
    12: "Amala Yoga",
    13: "Parvata Yoga",
    14: "Kahala Yoga",
    15: "Vesi Yoga",
    16: "Vasi Yoga",
    17: "Obhayachari Yoga",
    18: "Hamsa Yoga",
    19: "Malavya Yoga",
    20: "Sasa Yoga",
    21: "Ruchaka Yoga",
    22: "Bhadra Yoga",
    23: "Budha-Aditya Yoga",
    24: "Mahabhagya Yoga",
    25: "Pushkala Yoga",
    26: "Lakshmi Yoga",
    27: "Gauri Yoga",
    28: "Bharathi Yoga",
    29: "Chapa Yoga",
    30: "Sreenatha Yoga",
    44: "Sankha Yoga",
    45: "Bheri Yoga",
    46: "Mridanga Yoga",
    47: "Parijatha Yoga",
    48: "Gaja Yoga",
    49: "Kalanidhi Yoga",
    50: "Amsavatara Yoga",
    51: "Harihara Brahmi Yoga",
    52: "Kusuma Yoga",
    53: "Matsya Yoga",
    54: "Kurma Yoga",
    55: "Devendra Yoga",
    56: "Makuta Yoga",
    57: "Chandika Yoga",
    58: "Jaya Yoga",
    59: "Vidyut Yoga",
    60: "Gandharva Yoga",
    61: "Siva Yoga",
    62: "Vishnu Yoga",
    63: "Brahma Yoga",
    64: "Indra Yoga",
    65: "Ravi Yoga",
    66: "Garuda Yoga",
    67: "Go Yoga",
    68: "Gola Yoga",
    69: "Thrilochana Yoga",
    70: "Kulavardhana Yoga",
    103: "Duryoga",
    104: "Daridra Yoga",
    106: "Sarala Yoga",
    107: "Vimala Yoga",
    108: "Sareera Soukhya Yoga",
    109: "Dehapushti Yoga",
    112: "Amaranantha Dhana Yoga",
    123: "Kusuma Yoga",
    125: "Lakshmi Yoga",
    126: "Mahabhagya Yoga",
    128: "Malavya Yoga",
    133: "Madhya Vayasi Dhana Yoga",
    134: "Anthya Vayasi Dhana Yoga",
    135: "Balya Dhana Yoga",
    138: "Matrumooladdhana Yoga",
    139: "Putramooladdhana Yoga",
    140: "Satrumooladdhana Yoga",
    141: "Kalatramooladdhana Yoga",
    143: "Ayatnadhanalabha Yoga",
    157: "Asatyavadi Yoga",
    159: "Bhaskara Yoga",
    161: "Saraswathi Yoga",
    162: "Budha Yoga",
    171: "Annadana Yoga",
    172: "Parannabhojana Yoga",
    174: "Sarpaganda Yoga",
    177: "Bhratruvriddhi Yoga",
    182: "Parakrama Yoga",
    183: "Yuddha Praveena Yoga",
    187: "Uttama Griha Yoga",
    201: "Sahodareesangama Yoga",
    205: "Pretasapa Yoga",
    216: "Pitrusapa Sutakshaya Yoga",
    217: "Matrusapa Sutakshaya Yoga",
    218: "Bhratrusapa Sutakshaya Yoga",
    224: "Aputra Yoga",
    225: "Ekaputra Yoga",
    226: "Satputra Yoga",
    231: "Buddhimaturya Yoga",
    232: "Theevrabuddhi Yoga",
    234: "Thrikalagnana Yoga",
    235: "Putra Sukha Yoga",
    238: "Bahu Stree Yoga",
    239: "Satkalatra Yoga",
    241: "Bhagya Yoga",
    245: "Raja Yoga Group 1",
    246: "Raja Yoga Group 2",
    247: "Raja Yoga Group 3",
    248: "Raja Yoga Group 4",
    249: "Raja Yoga Group 5",
    250: "Raja Yoga Group 6",
    251: "Raja Yoga Group 7",
    252: "Raja Yoga Group 8",
    253: "Raja Yoga Group 9",
    254: "Raja Yoga Group 10",
    255: "Raja Yoga Group 11",
    256: "Raja Yoga Group 12",
    257: "Raja Yoga Group 13",
    258: "Raja Yoga Group 14",
    259: "Raja Yoga Group 15",
    260: "Raja Yoga Group 16",
    261: "Raja Yoga Group 17",
    262: "Raja Yoga Group 18",
    263: "Siracheda Yoga",
    264: "Galakarna Yoga",
    265: "Vrana Yoga",
    266: "Sisnavyadhi Yoga",
    272: "Karascheda Yoga",
    274: "Durmarana Yoga",
    275: "Yuddhe Marana Yoga",
    281: "Putrakalatraheena Yoga",
    283: "Vamsacheda Yoga",
    285: "Angaheena Yoga",
    286: "Swetakushta Yoga",
    287: "Pisacha Grastha Yoga",
    295: "Khalawata Yoga",
    297: "Rajabhrashta Yoga",
    300: "Gohanta Yoga",
}
EXECUTABLE_RAMAN_RULES = {1, 2, 3, 5, 6, 7, 11, 12, 17, 23}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_longitude(value: float) -> float:
    return value % 360.0


def _sign_from_longitude(longitude: float) -> str:
    return SIGN_ORDER[int(_normalize_longitude(longitude) // 30)]


def _sign_num(sign: str) -> int:
    return SIGN_ORDER.index(sign) + 1


def _is_odd_sign(sign: str) -> bool:
    return (_sign_num(sign) % 2) == 1


def _degree_in_sign(longitude: float) -> float:
    return round(_normalize_longitude(longitude) % 30.0, 4)


def _friendly_name(planet_key: str) -> str:
    return FRIENDLY_NAMES.get(planet_key, planet_key)


def _planet_swe_id(planet_id: str) -> int:
    return PLANET_ID_MAP[planet_id]


def _planet_longitude_and_speed(jd_ut: float, planet_id: str) -> tuple[float, float]:
    if planet_id == const.SOUTH_NODE:
        north_lon, north_speed = _planet_longitude_and_speed(jd_ut, const.NORTH_NODE)
        return _normalize_longitude(north_lon + 180.0), north_speed
    result = swe.calc_ut(jd_ut, _planet_swe_id(planet_id), SWE_FLAGS)[0]
    return _normalize_longitude(result[0]), result[3]


def _ascendant_longitude(jd_ut: float, latitude: float, longitude: float) -> float:
    _, ascmc = swe.houses(jd_ut, latitude, longitude, b"W")
    ayanamsa = swe.get_ayanamsa_ut(jd_ut)
    return _normalize_longitude(ascmc[0] - ayanamsa)


def _parse_input_datetime(payload: LagnaKundaliComputeRequest) -> tuple[str, str, datetime]:
    time_text = payload.time or "12:00"
    try:
        local_naive = datetime.strptime(f"{payload.date} {time_text}", "%Y-%m-%d %H:%M")
        local_dt = local_naive.replace(tzinfo=ZoneInfo(payload.timezone))
    except Exception as err:  # pragma: no cover - invalid runtime input
        raise HTTPException(status_code=400, detail=f"Invalid date/time or timezone: {err}") from err
    return payload.date, time_text, local_dt


def _to_julian_day(payload: LagnaKundaliComputeRequest) -> tuple[str, str, float]:
    date_text, time_text, local_dt = _parse_input_datetime(payload)
    utc_dt = local_dt.astimezone(timezone.utc)
    hour_ut = utc_dt.hour + (utc_dt.minute / 60.0) + (utc_dt.second / 3600.0)
    return date_text, time_text, swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour_ut)


def _resolve_coordinates(payload: LagnaKundaliComputeRequest) -> tuple[float, float]:
    if payload.latitude is not None and payload.longitude is not None:
        return payload.latitude, payload.longitude
    try:
        return geocode_place(payload.place_label)
    except Exception as err:  # pragma: no cover - depends on integration geocoder
        raise HTTPException(status_code=400, detail=f"Unable to resolve place coordinates: {err}") from err


def _reliability_notes(time_precision: TimePrecision) -> dict[str, Any]:
    if time_precision == "exact":
        return {"overall": "high", "notes": []}
    if time_precision == "approximate":
        return {
            "overall": "medium",
            "notes": [
                "Birth time is approximate. Bhav Chalit, divisional charts, Yoga matching, and strength layers should be read cautiously.",
            ],
        }
    return {
        "overall": "low",
        "notes": [
            "Birth time is unknown. Lagna-sensitive layers and house-sensitive layers should not be treated as precise.",
        ],
    }


def _get_house_number(planet_sign: str, lagna_sign: str) -> int:
    return ((SIGN_ORDER.index(planet_sign) - SIGN_ORDER.index(lagna_sign)) % 12) + 1


def _get_nakshatra(longitude: float) -> dict[str, Any]:
    index = int(_normalize_longitude(longitude) / (360 / 27))
    pada = int((_normalize_longitude(longitude) % (360 / 27)) / (360 / 108)) + 1
    nak = NAKSHATRAS[index]
    return {
        "index": index,
        "name": nak["name"],
        "lord": nak["lord"],
        "pada": pada,
        "dasha_years": nak["dasha_years"],
    }


def _dignity(planet_name: str, sign: str) -> str:
    if planet_name in {"Rahu", "Ketu", "Lagna"}:
        return "special"
    if EXALTATION_SIGNS.get(planet_name) == sign:
        return "exalted"
    if DEBILITATION_SIGNS.get(planet_name) == sign:
        return "debilitated"
    if SIGN_LORDS.get(sign) == planet_name:
        return "own_sign"
    return "neutral"


def _build_d1_positions(jd_ut: float, asc_lon: float) -> dict[str, Any]:
    lagna_sign = _sign_from_longitude(asc_lon)
    positions: dict[str, Any] = {}
    positions["Lagna"] = {
        "longitude": asc_lon,
        "sign": lagna_sign,
        "degree_in_sign": _degree_in_sign(asc_lon),
        "house": 1,
        "nakshatra": _get_nakshatra(asc_lon),
        "retrograde": False,
        "combust": False,
        "dignity": "special",
    }
    for planet_id in PLANET_IDS:
        longitude, speed = _planet_longitude_and_speed(jd_ut, planet_id)
        sign = _sign_from_longitude(longitude)
        name = PLANET_NAMES[planet_id]
        positions[name] = {
            "longitude": longitude,
            "sign": sign,
            "degree_in_sign": _degree_in_sign(longitude),
            "house": _get_house_number(sign, lagna_sign),
            "nakshatra": _get_nakshatra(longitude),
            "retrograde": speed < 0,
            "combust": False,
            "dignity": _dignity(_friendly_name(name), sign),
        }
    return positions


def _divisional_sign(longitude: float, chart_code: ChartCode) -> str | None:
    sign = _sign_from_longitude(longitude)
    sign_index = SIGN_ORDER.index(sign)
    degree = _normalize_longitude(longitude) % 30
    if chart_code == "D9":
        part = min(8, int(degree / (30 / 9)))
        if sign in {"Aries", "Cancer", "Libra", "Capricorn"}:
            start = sign_index
        elif sign in {"Taurus", "Leo", "Scorpio", "Aquarius"}:
            start = (sign_index + 8) % 12
        else:
            start = (sign_index + 4) % 12
        return SIGN_ORDER[(start + part) % 12]
    if chart_code == "D10":
        part = min(9, int(degree / 3))
        start = sign_index if _is_odd_sign(sign) else (sign_index + 8) % 12
        return SIGN_ORDER[(start + part) % 12]
    return None


def _build_divisional_chart(base_positions: dict[str, Any], chart_code: ChartCode) -> dict[str, Any]:
    if chart_code == "D1":
        raise ValueError("D1 should be built via the base position builder")
    lagna_sign = _divisional_sign(base_positions["Lagna"]["longitude"], chart_code)
    if lagna_sign is None:
        raise HTTPException(status_code=404, detail=f"{chart_code} is registered but not yet enabled for computation")
    grahas = []
    for planet_name, position in base_positions.items():
        div_sign = _divisional_sign(position["longitude"], chart_code)
        if div_sign is None:
            continue
        grahas.append({
            "code": planet_name,
            "name": _friendly_name(planet_name),
            "abbr": PLANET_ABBR.get(planet_name, planet_name[:2]),
            "sign": div_sign,
            "sign_num": _sign_num(div_sign),
            "degree_in_sign": position["degree_in_sign"],
            "house_whole_sign": _get_house_number(div_sign, lagna_sign),
        })
    houses = []
    for house_num in range(1, 13):
        house_sign = SIGN_ORDER[(SIGN_ORDER.index(lagna_sign) + house_num - 1) % 12]
        houses.append({
            "house_num": house_num,
            "sign": house_sign,
            "sign_num": _sign_num(house_sign),
            "lord": SIGN_LORDS[house_sign],
        })
    return {
        "code": chart_code,
        "name": CHART_MEANINGS[chart_code].split(" for ")[0],
        "focus_area": CHART_MEANINGS[chart_code],
        "lagna": {
            "sign": lagna_sign,
            "sign_num": _sign_num(lagna_sign),
            "degree_in_sign": base_positions["Lagna"]["degree_in_sign"],
            "nakshatra": base_positions["Lagna"]["nakshatra"]["name"],
            "pada": base_positions["Lagna"]["nakshatra"]["pada"],
        },
        "houses": houses,
        "grahas": grahas,
    }


def _build_d1_chart(base_positions: dict[str, Any]) -> dict[str, Any]:
    lagna_sign = base_positions["Lagna"]["sign"]
    houses = []
    grahas = []
    for planet_name, position in base_positions.items():
        grahas.append({
            "code": planet_name,
            "name": _friendly_name(planet_name),
            "abbr": PLANET_ABBR.get(planet_name, planet_name[:2]),
            "longitude": round(position["longitude"], 4),
            "sign": position["sign"],
            "sign_num": _sign_num(position["sign"]),
            "degree_in_sign": round(position["degree_in_sign"], 4),
            "nakshatra": position["nakshatra"]["name"],
            "pada": position["nakshatra"]["pada"],
            "retrograde": position["retrograde"],
            "combust": position["combust"],
            "house_whole_sign": position["house"],
            "dignity": position["dignity"],
        })
    for house_num in range(1, 13):
        house_sign = SIGN_ORDER[(SIGN_ORDER.index(lagna_sign) + house_num - 1) % 12]
        houses.append({
            "house_num": house_num,
            "sign": house_sign,
            "sign_num": _sign_num(house_sign),
            "lord": SIGN_LORDS[house_sign],
        })
    return {
        "code": "D1",
        "name": "Rashi",
        "focus_area": CHART_MEANINGS["D1"],
        "lagna": {
            "sign": lagna_sign,
            "sign_num": _sign_num(lagna_sign),
            "longitude": round(base_positions["Lagna"]["longitude"], 4),
            "degree_in_sign": round(base_positions["Lagna"]["degree_in_sign"], 4),
            "nakshatra": base_positions["Lagna"]["nakshatra"]["name"],
            "pada": base_positions["Lagna"]["nakshatra"]["pada"],
        },
        "houses": houses,
        "grahas": grahas,
    }


def _build_bhav_chalit(base_positions: dict[str, Any]) -> dict[str, Any]:
    lagna_lon = base_positions["Lagna"]["longitude"]
    house_one_start = _normalize_longitude(lagna_lon - 15.0)
    house_cusps = []
    graha_shifts = []
    for house_num in range(1, 13):
        midpoint = _normalize_longitude(lagna_lon + (house_num - 1) * 30.0)
        start = _normalize_longitude(midpoint - 15.0)
        end = _normalize_longitude(midpoint + 15.0)
        house_cusps.append({
            "house_num": house_num,
            "midpoint_longitude": round(midpoint, 4),
            "start_longitude": round(start, 4),
            "end_longitude": round(end, 4),
        })
    for planet_name, position in base_positions.items():
        if planet_name == "Lagna":
            continue
        bhav_house = int((_normalize_longitude(position["longitude"] - house_one_start)) // 30) + 1
        if bhav_house != position["house"]:
            graha_shifts.append({
                "graha": _friendly_name(planet_name),
                "whole_sign_house": position["house"],
                "bhav_chalit_house": bhav_house,
            })
    return {"system": "Equal House with Lagna as Bhava Madhya", "house_cusps": house_cusps, "graha_shifts": graha_shifts}


def _build_graha_layer(base_positions: dict[str, Any], charts: dict[str, Any]) -> dict[str, Any]:
    items = []
    chart_keys = [code for code in ("D1", "D9", "D10") if code in charts]
    bhav_lookup = {shift["graha"]: shift["bhav_chalit_house"] for shift in _build_bhav_chalit(base_positions)["graha_shifts"]}
    for planet_name, position in base_positions.items():
        if planet_name == "Lagna":
            continue
        varga_positions = {}
        for chart_code in chart_keys:
            chart = charts[chart_code]
            for graha in chart["grahas"]:
                if graha["code"] == planet_name:
                    varga_positions[chart_code] = {
                        "sign": graha["sign"],
                        "house": graha["house_whole_sign"],
                    }
                    break
        items.append({
            "code": planet_name,
            "name": _friendly_name(planet_name),
            "abbr": PLANET_ABBR[planet_name],
            "longitude": round(position["longitude"], 4),
            "sign": position["sign"],
            "degree_in_sign": round(position["degree_in_sign"], 4),
            "nakshatra": position["nakshatra"]["name"],
            "pada": position["nakshatra"]["pada"],
            "house_d1": position["house"],
            "house_bhav_chalit": bhav_lookup.get(_friendly_name(planet_name), position["house"]),
            "retrograde": position["retrograde"],
            "combust": position["combust"],
            "dignity": position["dignity"],
            "varga_positions": varga_positions,
        })
    return {"items": items}


def _build_upagraha_layer(base_positions: dict[str, Any]) -> dict[str, Any]:
    lagna_lon = base_positions["Lagna"]["longitude"]
    seed_points = [
        ("GULIKA", "Gulika", lagna_lon + 90.0),
        ("MANDI", "Mandi", lagna_lon + 105.0),
        ("DHUMA", "Dhuma", lagna_lon + 133.3333),
        ("VYATIPATA", "Vyatipata", lagna_lon + 193.3333),
        ("PARIVESHA", "Parivesha", lagna_lon + 223.3333),
        ("INDRACHAPA", "Indrachapa", lagna_lon + 253.3333),
        ("UPAKETU", "Upaketu", lagna_lon + 283.3333),
    ]
    items = []
    for code, name, raw_longitude in seed_points:
        longitude = _normalize_longitude(raw_longitude)
        sign = _sign_from_longitude(longitude)
        items.append({
            "code": code,
            "name": name,
            "longitude": round(longitude, 4),
            "sign": sign,
            "degree_in_sign": round(_degree_in_sign(longitude), 4),
            "house": _get_house_number(sign, base_positions["Lagna"]["sign"]),
            "calculation_basis": "BPHS Ashtama-Yama seed placeholder for Contract 8A backend spine",
            "supported": code in {"GULIKA", "MANDI"},
            "pending_verification": None if code in {"GULIKA", "MANDI"} else "Carry full classical validation before acceptance sign-off.",
        })
    return {"method": "BPHS Ashtama-Yama", "items": items}


def _get_cycle_sequence(start_lord: str) -> list[str]:
    start_index = TEMPLE_DASHA_ORDER.index(start_lord)
    return TEMPLE_DASHA_ORDER[start_index:] + TEMPLE_DASHA_ORDER[:start_index]


def _build_vimshottari(moon_longitude: float, birth_dt: datetime) -> dict[str, Any]:
    nak = _get_nakshatra(moon_longitude)
    start_lord = nak["lord"]
    if start_lord not in TEMPLE_DASHA_ORDER:
        raise HTTPException(status_code=500, detail=f"Unsupported dasha lord mapping for {start_lord}")
    nak_span = 360 / 27
    nak_start = nak["index"] * nak_span
    fraction_elapsed = (_normalize_longitude(moon_longitude) - nak_start) / nak_span
    fraction_remaining = max(0.0, 1.0 - fraction_elapsed)
    sequence = _get_cycle_sequence(start_lord)

    maha_dashas = []
    current_start = birth_dt
    for index, lord in enumerate(sequence):
        years = DASHA_YEARS[lord]
        if index == 0:
            duration_days = 365.25 * years * fraction_remaining
        else:
            duration_days = 365.25 * years
        current_end = current_start + timedelta(days=duration_days)
        maha_dashas.append({
            "planet": lord,
            "start": current_start.isoformat(),
            "end": current_end.isoformat(),
            "years": round(duration_days / 365.25, 4),
        })
        current_start = current_end

    now = _now()
    current_maha = next((item for item in maha_dashas if item["start"] <= now.isoformat() <= item["end"]), maha_dashas[-1])
    antar_dashas = _build_sub_dashas(current_maha["planet"], current_maha["start"], current_maha["end"])
    current_antar = next((item for item in antar_dashas if item["start"] <= now.isoformat() <= item["end"]), antar_dashas[-1])
    pratyantar_dashas = _build_sub_dashas(current_antar["planet"], current_antar["start"], current_antar["end"])
    current_pratyantar = next((item for item in pratyantar_dashas if item["start"] <= now.isoformat() <= item["end"]), pratyantar_dashas[-1])

    return {
        "birth_nakshatra": nak["name"],
        "birth_nakshatra_lord": start_lord,
        "maha_dashas": maha_dashas,
        "current_maha": current_maha,
        "antar_dashas": antar_dashas,
        "current_antar": current_antar,
        "pratyantar_dashas": pratyantar_dashas,
        "current_pratyantar": current_pratyantar,
    }


def _build_sub_dashas(parent_lord: str, start_iso: str, end_iso: str) -> list[dict[str, Any]]:
    start = datetime.fromisoformat(start_iso)
    end = datetime.fromisoformat(end_iso)
    total_seconds = (end - start).total_seconds()
    sub_dashas = []
    cursor = start
    for lord in _get_cycle_sequence(parent_lord):
        share = DASHA_YEARS[lord] / 120.0
        duration = total_seconds * share
        item_end = cursor + timedelta(seconds=duration)
        sub_dashas.append({
            "planet": lord,
            "start": cursor.isoformat(),
            "end": item_end.isoformat(),
            "years": round(duration / (365.25 * 24 * 3600), 6),
        })
        cursor = item_end
    if sub_dashas:
        sub_dashas[-1]["end"] = end.isoformat()
    return sub_dashas


def _ashtaka_varga_layer(base_positions: dict[str, Any]) -> dict[str, Any]:
    houses = []
    for house_num in range(1, 13):
        points = 20 + sum(1 for item in base_positions.values() if item["house"] == house_num)
        houses.append({"house_num": house_num, "points": points})
    bhinna = {}
    for planet_name in [name for name in base_positions if name != "Lagna"]:
        seed = base_positions[planet_name]["house"]
        bhinna[_friendly_name(planet_name).upper()] = [((seed + offset) % 8) + 1 for offset in range(12)]
    return {
        "status": "provisional",
        "pending_verification": "Classical Ashtaka Varga bindu rules still need full validation before Temple acceptance.",
        "sarvashtakavarga": {"houses": houses, "total_points": sum(item["points"] for item in houses)},
        "bhinna_ashtakavarga": bhinna,
    }


def _shadbala_layer(base_positions: dict[str, Any]) -> dict[str, Any]:
    items = []
    for planet_name in [name for name in base_positions if name not in {"Lagna", "Rahu", "Ketu"}]:
        position = base_positions[planet_name]
        strength_seed = position["house"]
        dignity_bonus = 40 if position["dignity"] in {"own_sign", "exalted"} else 10
        item = {
            "graha": _friendly_name(planet_name),
            "sthana_bala": float(60 + dignity_bonus),
            "dig_bala": float(10 + (strength_seed * 2)),
            "kala_bala": float(40 + position["nakshatra"]["pada"] * 3),
            "cheshta_bala": float(45 if position["retrograde"] else 30),
            "naisargika_bala": float(25 + strength_seed),
            "drik_bala": float(20 + (5 if position["dignity"] == "exalted" else 0)),
        }
        item["total"] = round(sum(item[key] for key in ("sthana_bala", "dig_bala", "kala_bala", "cheshta_bala", "naisargika_bala", "drik_bala")), 4)
        item["required_minimum"] = 300.0
        item["strength_band"] = "strong" if item["total"] >= 360 else ("adequate" if item["total"] >= 300 else "weak")
        items.append(item)
    return {
        "status": "provisional",
        "pending_verification": "Shadbala uses a provisional scoring spine in this implementation pass and still requires full classical validation.",
        "items": items,
    }


def _bhavabala_layer(d1_chart: dict[str, Any], shadbala: dict[str, Any]) -> dict[str, Any]:
    shadbala_by_name = {item["graha"]: item for item in shadbala["items"]}
    items = []
    for house in d1_chart["houses"]:
        lord = house["lord"]
        lord_strength = shadbala_by_name.get(lord, {"total": 0.0})
        dig_bala = float(20 + (house["house_num"] % 4) * 10)
        drushti_bala = float(15 + house["house_num"])
        shubha_ashubha = float(10 if house["house_num"] in {1, 4, 7, 10} else 5)
        dina_ratri = 6.0
        karaka = 8.0
        total = round((lord_strength["total"] / 10.0) + dig_bala + drushti_bala + shubha_ashubha + dina_ratri + karaka, 4)
        items.append({
            "house_num": house["house_num"],
            "bhavadhipati_bala": round(lord_strength["total"] / 10.0, 4),
            "bhava_dig_bala": dig_bala,
            "bhava_drushti_bala": drushti_bala,
            "bhava_shubha_ashubha_bala": shubha_ashubha,
            "bhava_dina_ratri_bala": dina_ratri,
            "karaka_strength": karaka,
            "total": total,
        })
    ranked = sorted(items, key=lambda item: item["total"], reverse=True)
    for index, item in enumerate(ranked, start=1):
        item["rank"] = index
        item["strength_band"] = "strong" if item["rank"] <= 4 else ("moderate" if item["rank"] <= 8 else "weak")
    return {
        "status": "provisional",
        "pending_verification": "Bhavabala currently follows the approved component structure but still needs classical rule-depth validation.",
        "items": sorted(ranked, key=lambda item: item["house_num"]),
    }


def _mercury_is_benefic(base_positions: dict[str, Any]) -> bool:
    mercury = base_positions.get("Mercury (Budha)")
    if not mercury:
        return False
    return mercury["dignity"] in {"own_sign", "exalted"} and not mercury["retrograde"]


def _rama_category(index: int) -> str:
    if 71 <= index <= 102:
        return "nabhasa"
    if 112 <= index <= 143:
        return "dhana"
    if 245 <= index <= 263:
        return "raja"
    if index >= 264:
        return "arishta_or_health"
    return "general"


def _match_raman_yoga(index: int, base_positions: dict[str, Any]) -> tuple[bool, list[str]]:
    moon_house = base_positions["Moon (Chandra)"]["house"]
    moon_sign_index = SIGN_ORDER.index(base_positions["Moon (Chandra)"]["sign"])
    jupiter_house = base_positions["Jupiter (Brihaspati)"]["house"]
    evidence: list[str] = []

    if index == 1:
        moon_sign = base_positions["Moon (Chandra)"]["sign"]
        jupiter_sign = base_positions["Jupiter (Brihaspati)"]["sign"]
        distance = ((SIGN_ORDER.index(jupiter_sign) - SIGN_ORDER.index(moon_sign)) % 12) + 1
        matched = distance in {1, 4, 7, 10}
        if matched:
            evidence.append("Jupiter is in a kendra from the Moon sign.")
        return matched, evidence
    if index == 2:
        matched = any(((SIGN_ORDER.index(pos["sign"]) - moon_sign_index) % 12) + 1 == 2 for name, pos in base_positions.items() if name not in {"Lagna", "Sun (Surya)"})
        if matched:
            evidence.append("At least one planet other than the Sun occupies the 2nd from Moon.")
        return matched, evidence
    if index == 3:
        matched = any(((SIGN_ORDER.index(pos["sign"]) - moon_sign_index) % 12) + 1 == 12 for name, pos in base_positions.items() if name not in {"Lagna", "Sun (Surya)"})
        if matched:
            evidence.append("At least one planet other than the Sun occupies the 12th from Moon.")
        return matched, evidence
    if index == 5:
        second = any(((SIGN_ORDER.index(pos["sign"]) - moon_sign_index) % 12) + 1 == 2 for name, pos in base_positions.items() if name not in {"Lagna", "Sun (Surya)"})
        twelfth = any(((SIGN_ORDER.index(pos["sign"]) - moon_sign_index) % 12) + 1 == 12 for name, pos in base_positions.items() if name not in {"Lagna", "Sun (Surya)"})
        matched = not second and not twelfth
        if matched:
            evidence.append("No planet other than the Sun occupies the 2nd or 12th from Moon.")
        return matched, evidence
    if index == 6:
        matched = base_positions["Moon (Chandra)"]["house"] == base_positions["Mars (Mangal)"]["house"]
        if matched:
            evidence.append("Moon and Mars occupy the same house.")
        return matched, evidence
    if index == 7:
        matched = any(
            ((SIGN_ORDER.index(pos["sign"]) - moon_sign_index) % 12) + 1 in {6, 7, 8}
            for name, pos in base_positions.items()
            if _friendly_name(name) in BENEFICS or (_friendly_name(name) == "Mercury" and _mercury_is_benefic(base_positions))
        )
        if matched:
            evidence.append("A benefic occupies the 6th, 7th, or 8th from Moon.")
        return matched, evidence
    if index == 11:
        matched = abs(jupiter_house - moon_house) in {6, 8}
        if matched:
            evidence.append("Moon and Jupiter form a 6/8 relationship by whole-sign houses.")
        return matched, evidence
    if index == 12:
        matched = any(
            pos["house"] == 10 and (_friendly_name(name) in BENEFICS or (_friendly_name(name) == "Mercury" and _mercury_is_benefic(base_positions)))
            for name, pos in base_positions.items()
            if name != "Lagna"
        )
        if matched:
            evidence.append("A benefic occupies the 10th from Lagna.")
        return matched, evidence
    if index == 17:
        matched = any(pos["house"] == 12 for name, pos in base_positions.items() if name not in {"Lagna", "Moon (Chandra)", "Sun (Surya)"})
        if matched:
            evidence.append("A non-luminary planet occupies the 12th from the Sun.")
        return matched, evidence
    if index == 23:
        matched = base_positions["Sun (Surya)"]["house"] == base_positions["Mercury (Budha)"]["house"]
        if matched:
            evidence.append("Sun and Mercury are conjoined by whole-sign placement.")
        return matched, evidence
    return False, []


def _build_yoga_layer(base_positions: dict[str, Any]) -> dict[str, Any]:
    items = []
    for index in range(1, 301):
        matched, evidence = _match_raman_yoga(index, base_positions)
        title = RAMAN_TITLE_OVERRIDES.get(index, f"Raman Combination {index}")
        supported = index in EXECUTABLE_RAMAN_RULES
        items.append({
            "code": f"RAMAN_{index:03d}",
            "name": title,
            "category": _rama_category(index),
            "source": "B.V. Raman - Three Hundred Important Combinations",
            "source_reference": f"Combination {index}",
            "matched": matched if supported else False,
            "supported": supported,
            "pending_verification": None if supported else "Registry slot present from day one; execution logic pending verification or OCR normalization.",
            "evidence": evidence,
        })
    return {
        "registry_count": len(items),
        "supported_count": sum(1 for item in items if item["supported"]),
        "matched_count": sum(1 for item in items if item["matched"]),
        "items": items,
    }


def _chart_definitions() -> list[ChartDefinition]:
    return [
        ChartDefinition(
            code=code,
            name=code,
            short_meaning=CHART_MEANINGS[code],
            enabled=code in ENABLED_CHARTS,
            precision_sensitive=True,
        )
        for code in SUPPORTED_CHARTS
    ]


def _build_payload(payload: LagnaKundaliComputeRequest, include_all_requested: bool = False) -> dict[str, Any]:
    latitude, longitude = _resolve_coordinates(payload)
    date_text, time_text, jd_ut = _to_julian_day(payload)
    asc_lon = _ascendant_longitude(jd_ut, latitude, longitude)
    base_positions = _build_d1_positions(jd_ut, asc_lon)
    charts: dict[str, Any] = {"D1": _build_d1_chart(base_positions)}

    requested = payload.requested_chart_codes or ["D1"]
    requested = [code for code in requested if code in SUPPORTED_CHARTS]
    if include_all_requested:
        for chart_code in requested:
            if chart_code != "D1" and chart_code in ENABLED_CHARTS:
                charts[chart_code] = _build_divisional_chart(base_positions, chart_code)

    moon_longitude = base_positions["Moon (Chandra)"]["longitude"]
    birth_local = _parse_input_datetime(payload)[2]
    layers = {}
    for layer_code in payload.include_layers:
        if layer_code == "graha":
            layers[layer_code] = _build_graha_layer(base_positions, charts)
        elif layer_code == "upagraha":
            layers[layer_code] = _build_upagraha_layer(base_positions)
        elif layer_code == "yoga":
            layers[layer_code] = _build_yoga_layer(base_positions)
        elif layer_code == "vimshottari_dasha":
            layers[layer_code] = _build_vimshottari(moon_longitude, birth_local)
        elif layer_code == "ashtaka_varga":
            layers[layer_code] = _ashtaka_varga_layer(base_positions)
        elif layer_code == "shadbala":
            layers[layer_code] = _shadbala_layer(base_positions)
        elif layer_code == "bhavabala":
            layers[layer_code] = _bhavabala_layer(charts["D1"], _shadbala_layer(base_positions))
        elif layer_code == "bhav_chalit":
            layers[layer_code] = _build_bhav_chalit(base_positions)

    moon_nakshatra = base_positions["Moon (Chandra)"]["nakshatra"]
    dasha = layers.get("vimshottari_dasha") or _build_vimshottari(moon_longitude, birth_local)
    return {
        "chart_id": f"lk_{uuid4().hex}",
        "input": {
            "date": date_text,
            "time": time_text,
            "time_precision": payload.time_precision,
            "place_label": payload.place_label,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": payload.timezone,
        },
        "meta": {
            "ayanamsa": "Lahiri",
            "engine_version": "contract_8a_kundali_router_v2",
            "rules_version": "contract_8a_temple_approved_2026_04_01",
            "computed_at": _now().isoformat(),
            "reliability": _reliability_notes(payload.time_precision),
        },
        "overview": {
            "lagna_sign": charts["D1"]["lagna"]["sign"],
            "lagna_degree": charts["D1"]["lagna"]["degree_in_sign"],
            "lagna_nakshatra": charts["D1"]["lagna"]["nakshatra"],
            "lagna_pada": charts["D1"]["lagna"]["pada"],
            "moon_nakshatra": moon_nakshatra["name"],
            "current_maha_dasha": dasha["current_maha"]["planet"],
            "current_antar_dasha": dasha["current_antar"]["planet"],
        },
        "charts": charts,
        "layers": layers,
        "ui_state_defaults": {
            "left_chart": "D1",
            "right_chart": "D9",
            "orientation": "north",
            "active_tab": "kundali",
        },
    }


def _get_db(request: Request):
    return getattr(request.app.state, "db", None)


def _get_collection(request: Request):
    db = _get_db(request)
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")
    if hasattr(db, "lagna_kundali_results"):
        return getattr(db, "lagna_kundali_results")
    try:
        return db["lagna_kundali_results"]
    except Exception as err:  # pragma: no cover - depends on integration db wrapper
        raise HTTPException(status_code=500, detail=f"lagna_kundali_results collection unavailable: {err}") from err


def _get_user_email(request: Request) -> str:
    state_user = getattr(request.state, "user", None)
    if isinstance(state_user, dict) and state_user.get("email"):
        return str(state_user["email"])
    raise HTTPException(status_code=401, detail="Authentication required")


def _try_get_user_email(request: Request) -> str | None:
    state_user = getattr(request.state, "user", None)
    if isinstance(state_user, dict) and state_user.get("email"):
        return str(state_user["email"])
    return None


@router.get("/chart-definitions", response_model=ChartDefinitionResponse)
async def chart_definitions() -> ChartDefinitionResponse:
    return ChartDefinitionResponse(charts=_chart_definitions())


@router.post("/compute")
async def compute_chart(payload: LagnaKundaliComputeRequest, request: Request) -> dict[str, Any]:
    compute_payload = payload.model_copy(deep=True)
    if not compute_payload.requested_chart_codes:
        compute_payload.requested_chart_codes = ["D1"]
    if compute_payload.requested_chart_codes != ["D1"]:
        compute_payload.requested_chart_codes = ["D1"]
    # Run CPU-bound sync computation in a thread-pool executor so the event loop stays free
    loop = asyncio.get_event_loop()
    doc = await loop.run_in_executor(None, partial(_build_payload, compute_payload, False))
    doc["doc_type"] = "chart_snapshot"
    maybe_user = _try_get_user_email(request)
    if maybe_user:
        doc["user_email"] = maybe_user
    db = _get_db(request)
    if db is not None:
        try:
            snapshot_collection = _get_collection(request)
            await asyncio.wait_for(snapshot_collection.insert_one(doc), timeout=6.0)
        except Exception:
            pass
    return doc


@router.post("/save", response_model=SaveChartResponse)
async def save_chart(payload: LagnaKundaliComputeRequest, request: Request) -> SaveChartResponse:
    user_email = _get_user_email(request)
    doc = _build_payload(payload, include_all_requested=False)
    doc["user_email"] = user_email
    doc["doc_type"] = "chart_report"
    collection = _get_collection(request)
    await collection.insert_one(doc)
    return SaveChartResponse(chart_id=doc["chart_id"], saved=True)


@router.get("/my-charts", response_model=MyChartsResponse)
async def my_charts(request: Request) -> MyChartsResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(request)
    cursor = collection.find({"user_email": user_email, "doc_type": "chart_report"}).sort("meta.computed_at", -1)
    items: list[MyChartItem] = []
    async for doc in cursor:
        items.append(MyChartItem(
            chart_id=doc["chart_id"],
            created_at=doc["meta"]["computed_at"],
            place_label=doc["input"]["place_label"],
            date=doc["input"]["date"],
            time_precision=doc["input"]["time_precision"],
            lagna_sign=doc["overview"]["lagna_sign"],
            saved_default_view=doc.get("ui_state_defaults", {"left_chart": "D1", "right_chart": "D9"}),
        ))
    return MyChartsResponse(items=items)


@router.get("/chart/{chart_id}")
async def get_chart(chart_id: str, request: Request) -> dict[str, Any]:
    user_email = _try_get_user_email(request)
    collection = _get_collection(request)
    filters: list[dict[str, Any]] = [{"chart_id": chart_id, "doc_type": "chart_snapshot"}]
    if user_email:
        filters.append({"chart_id": chart_id, "user_email": user_email, "doc_type": "chart_report"})
    doc = await collection.find_one({"$or": filters})
    if not doc:
        raise HTTPException(status_code=404, detail="Chart not found")
    return doc


@router.get("/chart/{chart_id}/charts/{chart_code}")
async def get_chart_variant(chart_id: str, chart_code: ChartCode, request: Request) -> dict[str, Any]:
    user_email = _try_get_user_email(request)
    collection = _get_collection(request)
    filters: list[dict[str, Any]] = [{"chart_id": chart_id, "doc_type": "chart_snapshot"}]
    if user_email:
        filters.append({"chart_id": chart_id, "user_email": user_email, "doc_type": "chart_report"})
    doc = await collection.find_one({"$or": filters})
    if not doc:
        raise HTTPException(status_code=404, detail="Chart not found")
    if chart_code not in SUPPORTED_CHARTS:
        raise HTTPException(status_code=404, detail="Unsupported chart code")
    if chart_code not in ENABLED_CHARTS:
        return {
            "code": chart_code,
            "enabled": False,
            "pending_verification": "This Varga is registered in the selector but not yet enabled for computation.",
        }
    if chart_code in doc.get("charts", {}):
        return doc["charts"][chart_code]

    recompute_payload = LagnaKundaliComputeRequest(
        date=doc["input"]["date"],
        time=doc["input"]["time"],
        time_precision=doc["input"]["time_precision"],
        place_label=doc["input"]["place_label"],
        latitude=doc["input"]["latitude"],
        longitude=doc["input"]["longitude"],
        timezone=doc["input"]["timezone"],
        requested_chart_codes=["D1", chart_code],
        include_layers=[],
    )
    rebuilt = _build_payload(recompute_payload, include_all_requested=True)
    variant = rebuilt["charts"][chart_code]
    await collection.update_one({"_id": doc["_id"]}, {"$set": {f"charts.{chart_code}": variant}})
    return variant


@router.get("/chart/{chart_id}/layers/{layer_code}", response_model=ChartLayerResponse)
async def get_chart_layer(chart_id: str, layer_code: LayerCode, request: Request) -> ChartLayerResponse:
    user_email = _get_user_email(request)
    collection = _get_collection(request)
    doc = await collection.find_one({"chart_id": chart_id, "user_email": user_email, "doc_type": "chart_report"})
    if not doc:
        raise HTTPException(status_code=404, detail="Chart not found")
    data = doc.get("layers", {}).get(layer_code)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Layer {layer_code} not found on this chart")
    return ChartLayerResponse(chart_id=chart_id, layer_code=layer_code, data=data)
