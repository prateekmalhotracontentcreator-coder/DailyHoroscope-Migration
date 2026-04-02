from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    build_natal_snapshot,
    build_report_document,
    build_vimshottari_timeline,
    current_dasha_periods,
    dasha_planet_quality,
    get_db,
    get_report_collection,
    get_user_email,
    house_lord_for_house,
    house_topic,
    local_datetime,
    truncate_text,
    truncate_words,
)


router = APIRouter(prefix="/api/reports/life-cycles", tags=["reports"])


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


class TransitionItem(StrictModel):
    planet: str
    date: str
    theme: str


class LifeCyclesOutput(StrictModel):
    report_type: Literal["life_cycles"] = "life_cycles"
    current_chapter: str
    current_sub_chapter: str
    chapter_quality: str
    upcoming_transitions: list[TransitionItem]
    this_decade_arc: str
    remedies: Remedies


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: BirthInput
    output_payload: LifeCyclesOutput
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


def _remedies(planet: str) -> Remedies:
    mantra_map = {
        "Sun": "Om Suryaya Namah",
        "Moon": "Om Som Somaya Namah",
        "Mars": "Om Angarakaya Namah",
        "Mercury": "Om Bum Budhaya Namah",
        "Jupiter": "Om Brim Brihaspataye Namah",
        "Venus": "Om Shum Shukraya Namah",
        "Saturn": "Om Sham Shanicharaya Namah",
        "Rahu": "Om Rahave Namah",
        "Ketu": "Om Ketave Namah",
    }
    return Remedies(
        mantra=RemedyDetail(
            text=mantra_map[planet],
            transliteration=mantra_map[planet].lower(),
            practice=truncate_text(f"Chant 108 times on the weekday aligned to {planet.lower()} during the current major period.", 60),
        ),
        gemstone=GemstoneDetail(stone="Yellow Sapphire" if planet == "Jupiter" else "Moonstone", purpose=truncate_text("May support steadier alignment.", 20)),
        ritual=truncate_text(f"At the start of each week, name one action that honors the lesson of your current {planet} period.", 40),
    )


def _build_output(payload: BirthInput) -> tuple[dict, LifeCyclesOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date,
        time_text=payload.time,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    birth_local = local_datetime(payload.date, payload.time, payload.timezone)
    timeline = build_vimshottari_timeline(natal["planets"]["Moon"]["longitude"], birth_local)
    current = current_dasha_periods(timeline, date.today())
    maha = current["maha_dasha"]
    antar = current["antar_dasha"]
    maha_house = natal["planets"].get(maha["planet"], {}).get("house")
    antar_house = natal["planets"].get(antar["planet"], {}).get("house")
    current_chapter = truncate_words(
        f"You are in {maha['planet']} Maha Dasha from {maha['start']} to {maha['end']}, a chapter emphasizing {house_topic(maha_house) if maha_house else 'the planet’s core agenda'}.",
        60,
    )
    current_sub = truncate_words(
        f"The current Antar Dasha of {antar['planet']} sharpens attention toward {house_topic(antar_house) if antar_house else 'a more specific sub-theme'}.",
        40,
    )
    chapter_quality = truncate_words(
        f"This period leans toward {dasha_planet_quality(maha['planet'])}, asking for maturity rather than speed.",
        40,
    )
    transitions: list[TransitionItem] = []
    maha_index = timeline["maha_dashas"].index(maha)
    for future in timeline["maha_dashas"][maha_index + 1 : maha_index + 4]:
        transitions.append(
            TransitionItem(
                planet=future["planet"],
                date=future["start"],
                theme=truncate_words(f"{future['planet']} opens a fresh chapter around {house_topic(natal['planets'].get(future['planet'], {}).get('house', 9))}.", 25),
            )
        )
    this_decade_arc = truncate_words(
        f"This decade is shaped by a transition from {maha['planet'].lower()} lessons into the next defining chapter, with long-term meaning tied to {house_lord_for_house(9, natal['ascendant_sign']).lower()} values and lived responsibility.",
        80,
    )
    output = LifeCyclesOutput(
        current_chapter=current_chapter,
        current_sub_chapter=current_sub,
        chapter_quality=chapter_quality,
        upcoming_transitions=transitions,
        this_decade_arc=this_decade_arc,
        remedies=_remedies(maha["planet"]),
    )
    summary = truncate_text(
        f"Life Cycles report: current Maha Dasha {maha['planet']}, current Antar Dasha {antar['planet']}, next transition on {transitions[0].date if transitions else maha['end']}.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_life_cycles_report(payload: BirthInput, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="life_cycles",
        report_slug="life-cycles",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    return GenerateResponse(report=ReportEnvelope(**document))


@router.get("/history", response_model=HistoryResponse)
async def get_life_cycles_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "life_cycles"}).sort("created_at", -1).to_list(length=50)
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
