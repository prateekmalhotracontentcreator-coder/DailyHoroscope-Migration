from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from knowledge_engine import register_arc_angel_report_run
from vitality_health_prompt_service import enrich_vitality_health_with_claude

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


router = APIRouter(prefix="/api/reports/vitality-health", tags=["reports"])


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


class CareWindow(StrictModel):
    planet: str
    start: str
    end: str
    description: str


class VitalityIndicators(StrictModel):
    lagna_sign: str
    sixth_lord: str
    sixth_lord_house: int
    mars_house: int
    saturn_house: int
    sun_house: int
    moon_house: int
    planets_in_sixth: list[str]


class VitalityHealthOutput(StrictModel):
    report_type: Literal["vitality_health"] = "vitality_health"
    vitality_indicators: VitalityIndicators
    vitality_signature: str
    pressure_pattern: str
    recovery_path: str
    daily_rhythm_guidance: str
    care_windows: list[CareWindow]
    remedies: Remedies


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: BirthInput
    output_payload: VitalityHealthOutput
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


def _care_windows(natal: dict[str, Any]) -> list[CareWindow]:
    birth_local = local_datetime(natal["input"]["date"], natal["input"]["time"], natal["input"]["timezone"])
    timeline = build_vimshottari_timeline(natal["planets"]["Moon"]["longitude"], birth_local)
    current = current_dasha_periods(timeline, date.today())
    favored = {
        house_lord_for_house(1, natal["ascendant_sign"]),
        house_lord_for_house(6, natal["ascendant_sign"]),
        "Sun",
        "Moon",
        "Mars",
        "Saturn",
    }
    items: list[CareWindow] = []
    for maha in timeline["maha_dashas"]:
        if maha["planet"] in favored:
            house_num = int(natal["planets"][maha["planet"]]["house"])
            items.append(
                CareWindow(
                    planet=maha["planet"],
                    start=maha["start"],
                    end=maha["end"],
                    description=truncate_words(
                        f"{maha['planet']} periods tend to make health, recovery, and energy management through {house_topic(house_num)} more important.",
                        20,
                    ),
                )
            )
        if len(items) == 3:
            break
    if not items:
        items.append(
            CareWindow(
                planet=current["maha_dasha"]["planet"],
                start=current["maha_dasha"]["start"],
                end=current["maha_dasha"]["end"],
                description=truncate_text("Your current dasha is the clearest signal for where extra care, pacing, and restoration are needed.", 110),
            )
        )
    return items


def _vitality_remedies(anchor_planet: str) -> Remedies:
    mantra = RemedyDetail(
        text="Om Suryaya Namah",
        transliteration="om suryaya namah",
        practice=truncate_text("Chant 27 or 108 times at sunrise while setting one clear healing intention for the day.", 60),
    )
    gemstone = GemstoneDetail(stone="Carnelian", purpose=truncate_text(f"May support steadier {anchor_planet.lower()} vitality and follow-through.", 18))
    ritual = truncate_text("Keep one sunrise or early-morning reset ritual for breath, hydration, and intention.", 40)
    return Remedies(mantra=mantra, gemstone=gemstone, ritual=ritual)


def _build_output(payload: BirthInput) -> tuple[dict[str, Any], VitalityHealthOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date,
        time_text=payload.time,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    planets = natal["planets"]
    sixth_lord = house_lord_for_house(6, natal["ascendant_sign"])
    planets_in_sixth = [name for name, details in planets.items() if int(details["house"]) == 6]
    sixth_aspects = planets_aspecting_house(planets, 6)
    indicators = VitalityIndicators(
        lagna_sign=str(natal["ascendant_sign"]),
        sixth_lord=sixth_lord,
        sixth_lord_house=int(planets[sixth_lord]["house"]),
        mars_house=int(planets["Mars"]["house"]),
        saturn_house=int(planets["Saturn"]["house"]),
        sun_house=int(planets["Sun"]["house"]),
        moon_house=int(planets["Moon"]["house"]),
        planets_in_sixth=planets_in_sixth,
    )
    vitality_signature = truncate_words(
        f"With {natal['ascendant_sign']} rising and the 6th lord {sixth_lord} in the {planets[sixth_lord]['house']}th house, your vitality depends on how daily strain is processed through {house_topic(int(planets[sixth_lord]['house']))}.",
        34,
    )
    pressure_pattern = truncate_words(
        f"Planets in or aspecting the 6th ({', '.join(sorted(set(planets_in_sixth + sixth_aspects))) or 'none'}) suggest pressure builds when Mars, Saturn, the Sun, or the Moon are pushed without enough rhythm.",
        32,
    )
    recovery_path = truncate_words(
        f"The recovery path asks for steadier systems, especially where house {planets['Moon']['house']} emotional habits and house {planets['Sun']['house']} vitality habits are out of sync.",
        28,
    )
    daily_rhythm_guidance = truncate_words(
        f"Your chart responds best to repeatable care: earlier resets, slower accumulation of stress, and practical routines that honor {house_topic(int(planets[sixth_lord]['house']))}.",
        30,
    )
    output = VitalityHealthOutput(
        vitality_indicators=indicators,
        vitality_signature=vitality_signature,
        pressure_pattern=pressure_pattern,
        recovery_path=recovery_path,
        daily_rhythm_guidance=daily_rhythm_guidance,
        care_windows=_care_windows(natal),
        remedies=_vitality_remedies(sixth_lord),
    )
    summary = truncate_text(
        f"Vitality & Health: 6th lord {sixth_lord} in house {planets[sixth_lord]['house']}, Mars in house {planets['Mars']['house']}, Moon in house {planets['Moon']['house']}.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_vitality_health(payload: BirthInput, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="vitality_health",
        report_slug="vitality-health",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    report = ReportEnvelope(**document)
    report = await enrich_vitality_health_with_claude(report, {"natal_snapshot": natal})
    document = report.model_dump(mode="python")
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    state_user = getattr(request.state, "user", None) or {}
    if state_user.get("user_id"):
        await register_arc_angel_report_run(get_db(request), str(state_user["user_id"]), document.get("report_type"))
    return GenerateResponse(report=report)


@router.get("/history", response_model=HistoryResponse)
async def get_vitality_health_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "vitality_health"}).sort("created_at", -1).to_list(length=10)
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
