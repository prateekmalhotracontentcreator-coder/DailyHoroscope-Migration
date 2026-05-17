from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from knowledge_engine import register_arc_angel_report_run
from romance_creative_prompt_service import enrich_romance_creative_with_claude

from vedic_shared_utils import (
    build_natal_snapshot,
    build_report_document,
    build_vimshottari_timeline,
    current_dasha_periods,
    get_db,
    get_report_collection,
    get_user_email,
    house_lord_for_house,
    house_topic,
    local_datetime,
    planets_aspecting_house,
    truncate_text,
    truncate_words,
)


router = APIRouter(prefix="/api/reports/romance-creative", tags=["reports"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BirthInput(StrictModel):
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city_name: str | None = None


class RemedyDetail(StrictModel):
    text: str
    transliteration: str
    practice: str


class GemstoneDetail(StrictModel):
    stone: str
    purpose: str


class Remedies(StrictModel):
    mantra: RemedyDetail
    gemstone: GemstoneDetail
    ritual: str


class OpeningWindow(StrictModel):
    planet: str
    start: str
    end: str
    description: str


class RomanceIndicators(StrictModel):
    fifth_lord: str
    fifth_lord_house: int
    putrakaraka: str
    venus_house: int
    sun_house: int
    planets_in_fifth: list[str]
    moon_nakshatra: str


class RomanceCreativeOutput(StrictModel):
    report_type: Literal["romance_creative"] = "romance_creative"
    romance_indicators: RomanceIndicators
    romantic_signature: str
    creative_intelligence: str
    heart_blocks: str
    expression_path: str
    opening_windows: list[OpeningWindow]
    remedies: Remedies


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: BirthInput
    output_payload: RomanceCreativeOutput
    summary: str
    created_at: datetime
    updated_at: datetime


class GenerateResponse(StrictModel):
    report: ReportEnvelope


class HistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    summary: str
    created_at: datetime


class HistoryResponse(StrictModel):
    items: list[HistoryItem] = Field(default_factory=list)
    total: int


def _collection(request: Request):
    return get_report_collection(get_db(request))


def _putrakaraka(planets: dict[str, Any]) -> str:
    eligible = [(body, float(details["degree"])) for body, details in planets.items() if body not in {"Rahu", "Ketu"}]
    return min(eligible, key=lambda item: item[1])[0]


def _opening_windows(natal: dict[str, Any]) -> list[OpeningWindow]:
    birth_local = local_datetime(natal["input"]["date"], natal["input"]["time"], natal["input"]["timezone"])
    timeline = build_vimshottari_timeline(natal["planets"]["Moon"]["longitude"], birth_local)
    current = current_dasha_periods(timeline, date.today())
    favored = {
        house_lord_for_house(5, natal["ascendant_sign"]),
        house_lord_for_house(7, natal["ascendant_sign"]),
        "Venus",
        "Moon",
    }
    items: list[OpeningWindow] = []
    for maha in timeline["maha_dashas"]:
        if maha["planet"] in favored:
            house_num = int(natal["planets"][maha["planet"]]["house"])
            items.append(
                OpeningWindow(
                    planet=maha["planet"],
                    start=maha["start"],
                    end=maha["end"],
                    description=truncate_words(
                        f"{maha['planet']} periods tend to open romance, creativity, and self-expression through {house_topic(house_num)}.",
                        18,
                    ),
                )
            )
        if len(items) == 3:
            break
    if not items:
        items.append(
            OpeningWindow(
                planet=current["maha_dasha"]["planet"],
                start=current["maha_dasha"]["start"],
                end=current["maha_dasha"]["end"],
                description=truncate_text("Your current dasha is the clearest timing signal for emotional opening and creative momentum.", 110),
            )
        )
    return items


def _romance_remedies(anchor_planet: str) -> Remedies:
    mantra = RemedyDetail(
        text="Om Shukraya Namah",
        transliteration="om shukraya namah",
        practice=truncate_text("Chant 108 times on Friday before art, writing, or a meaningful romantic conversation.", 60),
    )
    gemstone = GemstoneDetail(stone="Rose Quartz", purpose=truncate_text(f"May support a softer {anchor_planet.lower()} expression in love and creative flow.", 22))
    ritual = truncate_text("Offer flowers or fragrance on Friday and name one desire you want to express more honestly.", 40)
    return Remedies(mantra=mantra, gemstone=gemstone, ritual=ritual)


def _build_output(payload: BirthInput) -> tuple[dict[str, Any], RomanceCreativeOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date,
        time_text=payload.time,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    planets = natal["planets"]
    fifth_lord = house_lord_for_house(5, natal["ascendant_sign"])
    putrakaraka = _putrakaraka(planets)
    planets_in_fifth = [name for name, details in planets.items() if int(details["house"]) == 5]
    fifth_aspects = planets_aspecting_house(planets, 5)
    indicators = RomanceIndicators(
        fifth_lord=fifth_lord,
        fifth_lord_house=int(planets[fifth_lord]["house"]),
        putrakaraka=putrakaraka,
        venus_house=int(planets["Venus"]["house"]),
        sun_house=int(planets["Sun"]["house"]),
        planets_in_fifth=planets_in_fifth,
        moon_nakshatra=str(natal["moon_nakshatra"]["name"]),
    )
    romantic_signature = truncate_words(
        f"Your 5th house is led by {fifth_lord}, now placed in the {planets[fifth_lord]['house']}th house, so romance opens through {house_topic(int(planets[fifth_lord]['house']))}.",
        30,
    )
    creative_intelligence = truncate_words(
        f"Planets in or aspecting the 5th ({', '.join(sorted(set(planets_in_fifth + fifth_aspects))) or 'none'}) show a creative mind that strengthens when pleasure and meaning are allowed to collaborate.",
        30,
    )
    heart_blocks = truncate_words(
        f"When Venus in house {planets['Venus']['house']} or the Sun in house {planets['Sun']['house']} is pressured, affection can become performance, caution, or delayed vulnerability.",
        28,
    )
    expression_path = truncate_words(
        f"Your chart softens when love and creativity are expressed through the Moon's {natal['moon_nakshatra']['name']} nakshatra rhythm: steady feeling, honest play, and fewer disguised desires.",
        32,
    )
    output = RomanceCreativeOutput(
        romance_indicators=indicators,
        romantic_signature=romantic_signature,
        creative_intelligence=creative_intelligence,
        heart_blocks=heart_blocks,
        expression_path=expression_path,
        opening_windows=_opening_windows(natal),
        remedies=_romance_remedies(fifth_lord),
    )
    summary = truncate_text(
        f"Romance & Creative report: 5th lord {fifth_lord} in house {planets[fifth_lord]['house']}, Venus in house {planets['Venus']['house']}, Moon nakshatra {natal['moon_nakshatra']['name']}.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_romance_creative(payload: BirthInput, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="romance_creative",
        report_slug="romance-creative",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    report = ReportEnvelope(**document)
    report = await enrich_romance_creative_with_claude(report, {"natal_snapshot": natal})
    document = report.model_dump(mode="python")
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    state_user = getattr(request.state, "user", None) or {}
    if state_user.get("user_id"):
        await register_arc_angel_report_run(get_db(request), str(state_user["user_id"]), document.get("report_type"))
    return GenerateResponse(report=report)


@router.get("/history", response_model=HistoryResponse)
async def get_romance_creative_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "romance_creative"}).sort("created_at", -1).to_list(length=10)
    return HistoryResponse(
        items=[
            HistoryItem(
                id=item["id"],
                report_type=item["report_type"],
                report_slug=item["report_slug"],
                summary=item["summary"],
                created_at=item["created_at"],
            )
            for item in items
        ],
        total=len(items),
    )
