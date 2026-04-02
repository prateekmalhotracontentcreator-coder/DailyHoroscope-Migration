from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    build_natal_snapshot,
    build_report_document,
    build_transit_snapshot,
    get_db,
    get_report_collection,
    get_user_email,
    house_entry_from_longitude,
    house_topic,
    truncate_text,
)


router = APIRouter(prefix="/api/reports/retrograde-survival", tags=["reports"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BirthInput(StrictModel):
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city_name: str | None = None


class GenerateRequest(StrictModel):
    check_date: str | None = None
    planet: Literal["Mercury", "Venus", "Mars"] | None = None
    birth_data: BirthInput | None = None


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


class RetrogradePlanetOutput(StrictModel):
    planet: str
    start_date: str
    end_date: str
    transit_house: int | None = None
    life_area: str
    what_to_expect: str
    navigation_tips: list[str]
    what_to_avoid: list[str]
    remedies: Remedies


class RetrogradeSurvivalOutput(StrictModel):
    report_type: Literal["retrograde_survival"] = "retrograde_survival"
    mode: Literal["general", "personal"]
    active_retrogrades: list[RetrogradePlanetOutput]


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: GenerateRequest
    output_payload: RetrogradeSurvivalOutput
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


def _retro_window(check_date: date, timezone_name: str, planet: str) -> tuple[str, str] | None:
    today = build_transit_snapshot(check_date, timezone_name, bodies=(planet,))
    if not today["planets"][planet]["retrograde"]:
        return None
    start = check_date
    end = check_date
    for offset in range(1, 181):
        target = check_date - timedelta(days=offset)
        if not build_transit_snapshot(target, timezone_name, bodies=(planet,))["planets"][planet]["retrograde"]:
            start = target + timedelta(days=1)
            break
    for offset in range(1, 181):
        target = check_date + timedelta(days=offset)
        if not build_transit_snapshot(target, timezone_name, bodies=(planet,))["planets"][planet]["retrograde"]:
            end = target - timedelta(days=1)
            break
    return start.isoformat(), end.isoformat()


def _remedies(planet: str) -> Remedies:
    remedy_map = {
        "Mercury": ("Om Bum Budhaya Namah", "Emerald", "communication clarity"),
        "Venus": ("Om Shum Shukraya Namah", "Rose Quartz", "heart-led review"),
        "Mars": ("Om Angarakaya Namah", "Red Jasper", "disciplined courage"),
    }
    mantra_text, stone, purpose = remedy_map[planet]
    return Remedies(
        mantra=RemedyDetail(
            text=mantra_text,
            transliteration=mantra_text.lower(),
            practice=truncate_text(f"Chant 108 times during the {planet} retrograde period when emotions are hardest to read clearly.", 60),
        ),
        gemstone=GemstoneDetail(stone=stone, purpose=truncate_text(f"May support {purpose}.", 20)),
        ritual=truncate_text(f"Pause one recurring {planet.lower()}-pattern this week and replace it with a slower, cleaner response.", 40),
    )


def _planet_output(planet: str, start_date: str, end_date: str, transit_house: int | None) -> RetrogradePlanetOutput:
    area = truncate_text(house_topic(transit_house) if transit_house else f"{planet.lower()} themes in general life rhythm", 20)
    expect_map = {
        "Mercury": "Mercury retrograde tends to activate review, crossed wires, and unfinished conversations.",
        "Venus": "Venus retrograde often reopens questions of value, attraction, and emotional pacing.",
        "Mars": "Mars retrograde can slow momentum and expose where force has replaced strategy.",
    }
    tips_map = {
        "Mercury": ["Re-read messages twice.", "Delay non-urgent agreements.", "Back up important notes."],
        "Venus": ["Review old desires slowly.", "Keep spending simple.", "Choose honesty over charm."],
        "Mars": ["Conserve energy deliberately.", "Finish old battles first.", "Train patience before action."],
    }
    avoid_map = {
        "Mercury": ["Rushed decisions", "Ambiguous promises", "Unverified details"],
        "Venus": ["Impulse commitment", "Image-driven spending", "Old fantasy loops"],
        "Mars": ["Needless arguments", "Pride-based pushing", "Hot reaction cycles"],
    }
    return RetrogradePlanetOutput(
        planet=planet,
        start_date=start_date,
        end_date=end_date,
        transit_house=transit_house,
        life_area=area,
        what_to_expect=truncate_text(expect_map[planet], 50),
        navigation_tips=[truncate_text(item, 20) for item in tips_map[planet]],
        what_to_avoid=[truncate_text(item, 20) for item in avoid_map[planet]],
        remedies=_remedies(planet),
    )


def _build_output(payload: GenerateRequest) -> tuple[dict | None, RetrogradeSurvivalOutput, str]:
    timezone_name = payload.birth_data.timezone if payload.birth_data else "Asia/Kolkata"
    check_date = date.fromisoformat(payload.check_date) if payload.check_date else datetime.now().date()
    natal = None
    if payload.birth_data:
        natal = build_natal_snapshot(
            date_text=payload.birth_data.date,
            time_text=payload.birth_data.time,
            latitude=payload.birth_data.latitude,
            longitude=payload.birth_data.longitude,
            timezone_name=payload.birth_data.timezone,
            city_name=payload.birth_data.city_name,
        )
    planets = [payload.planet] if payload.planet else ["Mercury", "Venus", "Mars"]
    outputs = []
    for planet in planets:
        window = _retro_window(check_date, timezone_name, planet)
        if not window:
            continue
        transit_house = None
        if natal:
            transit = build_transit_snapshot(check_date, timezone_name, bodies=(planet,))
            transit_house = house_entry_from_longitude(transit["planets"][planet]["longitude"], natal["ascendant_sign"])
        outputs.append(_planet_output(planet, window[0], window[1], transit_house))
    output = RetrogradeSurvivalOutput(mode="personal" if natal else "general", active_retrogrades=outputs)
    summary = truncate_text(
        f"Retrograde Survival guide for {check_date.isoformat()} with {len(outputs)} active retrograde period(s) in view.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_retrograde_survival(payload: GenerateRequest, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="retrograde_survival",
        report_slug="retrograde-survival",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    if natal:
        document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    envelope_data = {k: v for k, v in document.items() if k not in ("natal_snapshot", "_id")}
    return GenerateResponse(report=ReportEnvelope(**envelope_data))


@router.get("/history", response_model=HistoryResponse)
async def get_retrograde_survival_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "retrograde_survival"}).sort("created_at", -1).to_list(length=50)
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
