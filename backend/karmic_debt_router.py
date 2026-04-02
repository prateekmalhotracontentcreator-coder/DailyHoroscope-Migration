from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    atmakaraka_planet,
    build_natal_snapshot,
    build_report_document,
    get_db,
    get_report_collection,
    get_user_email,
    house_topic,
    truncate_text,
    truncate_words,
)


router = APIRouter(prefix="/api/reports/karmic-debt", tags=["reports"])


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


class RetrogradeLesson(StrictModel):
    planet: str
    lesson: str


class KarmicIndicators(StrictModel):
    retrograde_planets: list[str]
    saturn_house: int
    rahu_house: int
    ketu_house: int
    atmakaraka: str
    atmakaraka_degree: float
    debt_activated: bool


class KarmicReportBody(StrictModel):
    headline: str
    karmic_theme: str
    past_life_echo: str
    atmakaraka_insight: str
    retrograde_lessons: list[RetrogradeLesson]
    breaking_the_cycle: str
    remedies: Remedies


class KarmicDebtOutput(StrictModel):
    report_type: Literal["karmic_debt"] = "karmic_debt"
    karmic_indicators: KarmicIndicators
    report: KarmicReportBody


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: BirthInput
    output_payload: KarmicDebtOutput
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


def _remedies(saturn_house: int, rahu_house: int) -> Remedies:
    if saturn_house in {8, 12} or rahu_house in {8, 12}:
        mantra = RemedyDetail(
            text="Om Sham Shanicharaya Namah",
            transliteration="om sham shanicharaya namah",
            practice=truncate_text("Chant 108 times on Saturdays and sit quietly for a few minutes after the final repetition.", 60),
        )
        gemstone = GemstoneDetail(stone="Amethyst", purpose=truncate_text("May support steadiness and inner restraint.", 20))
        ritual = truncate_text("Offer a simple sesame oil lamp on Saturday evening and name one repeating pattern you are ready to release.", 40)
    else:
        mantra = RemedyDetail(
            text="Om Rahave Namah",
            transliteration="om rahave namah",
            practice=truncate_text("Chant 108 times on Saturday or during a quiet dusk period when the mind feels unsettled.", 60),
        )
        gemstone = GemstoneDetail(stone="Rose Quartz", purpose=truncate_text("May soften old emotional loops.", 20))
        ritual = truncate_text("Write one inherited fear on paper and burn it safely as a symbolic release of repetition.", 40)
    return Remedies(mantra=mantra, gemstone=gemstone, ritual=ritual)


def _retrograde_lessons(retrograde_planets: list[str]) -> list[RetrogradeLesson]:
    lesson_map = {
        "Mercury": "Communication karma repeats until speech becomes cleaner, calmer, and more truthful.",
        "Venus": "Old attachment patterns may return until love is chosen with self-respect.",
        "Mars": "Conflict patterns soften when action is disciplined rather than reactive.",
        "Jupiter": "Belief patterns mature when wisdom is practiced rather than preached.",
        "Saturn": "Duty becomes lighter when boundaries are accepted instead of resisted.",
    }
    items = [
        RetrogradeLesson(planet=planet, lesson=truncate_words(lesson_map.get(planet, "This retrograde suggests a lesson that matures through patience and repeated self-observation."), 40))
        for planet in retrograde_planets[:4]
    ]
    return items


def _build_output(payload: BirthInput) -> tuple[dict, KarmicDebtOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date,
        time_text=payload.time,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    planets = natal["planets"]
    retrograde_planets = [name for name, details in planets.items() if details["retrograde"] and name not in {"Rahu", "Ketu"}]
    saturn_house = int(planets["Saturn"]["house"])
    rahu_house = int(planets["Rahu"]["house"])
    ketu_house = int(planets["Ketu"]["house"])
    atmakaraka, atmakaraka_degree = atmakaraka_planet(planets)
    debt_activated = any(house in {4, 8, 12} for house in (saturn_house, rahu_house, ketu_house)) or bool(retrograde_planets)
    indicators = KarmicIndicators(
        retrograde_planets=retrograde_planets,
        saturn_house=saturn_house,
        rahu_house=rahu_house,
        ketu_house=ketu_house,
        atmakaraka=atmakaraka,
        atmakaraka_degree=round(atmakaraka_degree, 2),
        debt_activated=debt_activated,
    )
    headline = truncate_words(f"Your chart points to a karmic lesson around {house_topic(saturn_house).split(',')[0]}.", 15)
    karmic_theme = truncate_words(
        f"Saturn in the {saturn_house}th and the nodal axis across {rahu_house}/{ketu_house} suggest repeating lessons around {house_topic(saturn_house)}.",
        60,
    )
    past_life_echo = truncate_words(
        f"The strongest echo is a habit of carrying unfinished weight in {house_topic(rahu_house)} until trust and detachment are rebuilt consciously.",
        60,
    )
    atmakaraka_insight = truncate_words(
        f"Your Atmakaraka is {atmakaraka}, so the soul grows when {atmakaraka.lower()} qualities are expressed with maturity instead of urgency.",
        50,
    )
    breaking_the_cycle = truncate_words(
        f"The cycle softens when you meet {house_topic(saturn_house)} with patience, cleaner boundaries, and slower decisions.",
        60,
    )
    report = KarmicReportBody(
        headline=headline,
        karmic_theme=karmic_theme,
        past_life_echo=past_life_echo,
        atmakaraka_insight=atmakaraka_insight,
        retrograde_lessons=_retrograde_lessons(retrograde_planets),
        breaking_the_cycle=breaking_the_cycle,
        remedies=_remedies(saturn_house, rahu_house),
    )
    output = KarmicDebtOutput(karmic_indicators=indicators, report=report)
    summary = truncate_text(
        f"Karmic Debt report: Saturn in house {saturn_house}, Rahu in house {rahu_house}, with {len(retrograde_planets)} retrograde lessons active.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_karmic_debt_report(payload: BirthInput, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="karmic_debt",
        report_slug="karmic-debt",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    return GenerateResponse(report=ReportEnvelope(**document))


@router.get("/history", response_model=HistoryResponse)
async def get_karmic_debt_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "karmic_debt"}).sort("created_at", -1).to_list(length=50)
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
