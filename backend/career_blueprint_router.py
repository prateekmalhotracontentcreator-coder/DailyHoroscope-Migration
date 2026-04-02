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
    get_db,
    get_report_collection,
    get_user_email,
    house_lord_for_house,
    local_datetime,
    house_topic,
    planets_aspecting_house,
    truncate_text,
    truncate_words,
)


router = APIRouter(prefix="/api/reports/career-blueprint", tags=["reports"])


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


class PeakPeriod(StrictModel):
    planet: str
    start: str
    end: str
    description: str


class CareerBlueprintOutput(StrictModel):
    report_type: Literal["career_blueprint"] = "career_blueprint"
    career_archetype: str
    natural_strengths: str
    success_formula: str
    wealth_signature: str
    peak_periods: list[PeakPeriod]
    action_guidance: str
    remedies: Remedies


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: BirthInput
    output_payload: CareerBlueprintOutput
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


def _career_remedies(planet_name: str) -> Remedies:
    mantra = RemedyDetail(
        text="Om Brim Brihaspataye Namah",
        transliteration="om brim brihaspataye namah",
        practice=truncate_text("Chant 108 times on Thursdays before beginning important professional work.", 60),
    )
    gemstone = GemstoneDetail(stone="Yellow Citrine", purpose=truncate_text("May support confidence and wise expansion.", 20))
    ritual = truncate_text(f"On Thursday morning, write one disciplined step that honors your {planet_name.lower()}-led growth path.", 40)
    return Remedies(mantra=mantra, gemstone=gemstone, ritual=ritual)


def _peak_periods(natal: dict) -> list[PeakPeriod]:
    birth_local = local_datetime(
        natal["input"]["date"],
        natal["input"]["time"],
        natal["input"]["timezone"],
    )
    timeline = build_vimshottari_timeline(natal["planets"]["Moon"]["longitude"], birth_local)
    today = date.today()
    current = current_dasha_periods(timeline, today)
    favored = {
        house_lord_for_house(10, natal["ascendant_sign"]),
        house_lord_for_house(2, natal["ascendant_sign"]),
        house_lord_for_house(6, natal["ascendant_sign"]),
        "Jupiter",
        "Saturn",
    }
    periods = []
    for maha in timeline["maha_dashas"]:
        if maha["planet"] in favored:
            periods.append(
                PeakPeriod(
                    planet=maha["planet"],
                    start=maha["start"],
                    end=maha["end"],
                    description=truncate_words(f"{maha['planet']} periods tend to emphasise {house_topic(natal['planets'][maha['planet']]['house'])}.", 12),
                )
            )
        if len(periods) == 3:
            break
    if not periods:
        periods.append(
            PeakPeriod(
                planet=current["maha_dasha"]["planet"],
                start=current["maha_dasha"]["start"],
                end=current["maha_dasha"]["end"],
                description=truncate_text("Your current dasha remains the clearest career-timing signal in the chart.", 45),
            )
        )
    return periods


def _build_output(payload: BirthInput) -> tuple[dict, CareerBlueprintOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date,
        time_text=payload.time,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    planets = natal["planets"]
    tenth_lord = house_lord_for_house(10, natal["ascendant_sign"])
    second_lord = house_lord_for_house(2, natal["ascendant_sign"])
    sixth_lord = house_lord_for_house(6, natal["ascendant_sign"])
    planets_in_tenth = [name for name, details in planets.items() if details["house"] == 10]
    aspecting_tenth = planets_aspecting_house(planets, 10)
    mc_sign = natal["midheaven_sign"]
    career_archetype = truncate_words(
        f"Your Midheaven in {mc_sign} points to a public path built through {house_topic(10).split(',')[0]} with a distinct {mc_sign.lower()} style.",
        40,
    )
    natural_strengths = truncate_words(
        f"Planets in or aspecting the 10th house ({', '.join(sorted(set(planets_in_tenth + aspecting_tenth))) or 'none'}) show how responsibility, visibility, and leadership express through your chart.",
        60,
    )
    success_formula = truncate_words(
        f"The 10th lord {tenth_lord} sits in your {planets[tenth_lord]['house']}th house, so career success grows when you align work with {house_topic(planets[tenth_lord]['house'])}.",
        60,
    )
    wealth_signature = truncate_words(
        f"Your 2nd lord {second_lord} and 6th lord {sixth_lord} suggest income stabilizes when service, skill, and values stay linked.", 50
    )
    action_guidance = truncate_words(
        f"Move toward roles where {tenth_lord.lower()} qualities can lead publicly, while keeping daily systems strong enough to carry long-range ambition.",
        60,
    )
    output = CareerBlueprintOutput(
        career_archetype=career_archetype,
        natural_strengths=natural_strengths,
        success_formula=success_formula,
        wealth_signature=wealth_signature,
        peak_periods=_peak_periods(natal),
        action_guidance=action_guidance,
        remedies=_career_remedies(tenth_lord),
    )
    summary = truncate_text(
        f"Career Blueprint: MC in {mc_sign}, 10th lord {tenth_lord} in house {planets[tenth_lord]['house']}, with {len(planets_in_tenth)} planets placed in the 10th.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_career_blueprint(payload: BirthInput, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="career_blueprint",
        report_slug="career-blueprint",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    return GenerateResponse(report=ReportEnvelope(**document))


@router.get("/history", response_model=HistoryResponse)
async def get_career_blueprint_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "career_blueprint"}).sort("created_at", -1).to_list(length=50)
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
