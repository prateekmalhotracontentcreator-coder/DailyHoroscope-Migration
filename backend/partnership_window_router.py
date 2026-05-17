from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from knowledge_engine import register_arc_angel_report_run
from partnership_window_prompt_service import enrich_partnership_window_with_claude

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
    sign_index,
    truncate_text,
    truncate_words,
)


router = APIRouter(prefix="/api/reports/partnership-window", tags=["reports"])
SIGN_ORDER = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")


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


class PartnershipWindow(StrictModel):
    planet: str
    start: str
    end: str
    description: str


class PartnershipIndicators(StrictModel):
    seventh_lord: str
    seventh_lord_house: int
    darakaraka: str
    venus_house: int
    upapada_sign: str
    planets_in_seventh: list[str]


class PartnershipWindowOutput(StrictModel):
    report_type: Literal["partnership_window"] = "partnership_window"
    partnership_indicators: PartnershipIndicators
    partnership_signature: str
    commitment_pattern: str
    relationship_blocks: str
    readiness_path: str
    partnership_windows: list[PartnershipWindow]
    remedies: Remedies


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: BirthInput
    output_payload: PartnershipWindowOutput
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


def _darakaraka(planets: dict[str, Any]) -> str:
    eligible = [(body, float(details["degree"])) for body, details in planets.items() if body not in {"Rahu", "Ketu"}]
    return min(eligible, key=lambda item: item[1])[0]


def _upapada_sign(natal: dict[str, Any]) -> str:
    houses = natal["houses"]
    twelfth_sign = houses["12"]
    twelfth_lord = house_lord_for_house(12, natal["ascendant_sign"])
    twelfth_lord_sign = str(natal["planets"][twelfth_lord]["sign"])
    distance = (sign_index(twelfth_lord_sign) - sign_index(twelfth_sign)) % 12
    target_index = (sign_index(twelfth_lord_sign) + distance) % 12
    return SIGN_ORDER[target_index]


def _partnership_windows(natal: dict[str, Any]) -> list[PartnershipWindow]:
    birth_local = local_datetime(natal["input"]["date"], natal["input"]["time"], natal["input"]["timezone"])
    timeline = build_vimshottari_timeline(natal["planets"]["Moon"]["longitude"], birth_local)
    current = current_dasha_periods(timeline, date.today())
    favored = {
        house_lord_for_house(5, natal["ascendant_sign"]),
        house_lord_for_house(7, natal["ascendant_sign"]),
        "Venus",
        "Moon",
    }
    items: list[PartnershipWindow] = []
    for maha in timeline["maha_dashas"]:
        if maha["planet"] in favored:
            house_num = int(natal["planets"][maha["planet"]]["house"])
            items.append(
                PartnershipWindow(
                    planet=maha["planet"],
                    start=maha["start"],
                    end=maha["end"],
                    description=truncate_words(
                        f"{maha['planet']} periods often bring stronger focus to commitment, attraction, and partnership through {house_topic(house_num)}.",
                        21,
                    ),
                )
            )
        if len(items) == 3:
            break
    if not items:
        items.append(
            PartnershipWindow(
                planet=current["maha_dasha"]["planet"],
                start=current["maha_dasha"]["start"],
                end=current["maha_dasha"]["end"],
                description=truncate_text("Your current dasha remains the clearest timing signal for relationship readiness and commitment themes.", 112),
            )
        )
    return items


def _partnership_remedies(anchor_planet: str) -> Remedies:
    mantra = RemedyDetail(
        text="Om Kleem Krishnaya Namah",
        transliteration="om kleem krishnaya namah",
        practice=truncate_text("Chant 108 times on Friday while holding one relationship intention rooted in truth rather than fear.", 60),
    )
    gemstone = GemstoneDetail(stone="Rose Quartz", purpose=truncate_text(f"May support a more open {anchor_planet.lower()} expression in closeness and trust.", 22))
    ritual = truncate_text("Light a Friday lamp and write one partnership standard you are ready to honor consistently.", 40)
    return Remedies(mantra=mantra, gemstone=gemstone, ritual=ritual)


def _build_output(payload: BirthInput) -> tuple[dict[str, Any], PartnershipWindowOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date,
        time_text=payload.time,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    planets = natal["planets"]
    seventh_lord = house_lord_for_house(7, natal["ascendant_sign"])
    planets_in_seventh = [name for name, details in planets.items() if int(details["house"]) == 7]
    seventh_aspects = planets_aspecting_house(planets, 7)
    indicators = PartnershipIndicators(
        seventh_lord=seventh_lord,
        seventh_lord_house=int(planets[seventh_lord]["house"]),
        darakaraka=_darakaraka(planets),
        venus_house=int(planets["Venus"]["house"]),
        upapada_sign=_upapada_sign(natal),
        planets_in_seventh=planets_in_seventh,
    )
    partnership_signature = truncate_words(
        f"Your 7th house is led by {seventh_lord}, placed in the {planets[seventh_lord]['house']}th house, so partnership matures through {house_topic(int(planets[seventh_lord]['house']))}.",
        31,
    )
    commitment_pattern = truncate_words(
        f"Planets in or aspecting the 7th ({', '.join(sorted(set(planets_in_seventh + seventh_aspects))) or 'none'}) describe how attraction, devotion, and commitment are tested before they stabilise.",
        30,
    )
    relationship_blocks = truncate_words(
        f"With Venus in house {planets['Venus']['house']} and the Darakaraka pattern moving through {indicators.darakaraka.lower()} themes, pressure often appears when closeness and standards drift apart.",
        31,
    )
    readiness_path = truncate_words(
        f"Your chart favors steadier relationship timing when the Upapada in {indicators.upapada_sign} is honored through patience, clean vows, and fewer rushed emotional decisions.",
        30,
    )
    output = PartnershipWindowOutput(
        partnership_indicators=indicators,
        partnership_signature=partnership_signature,
        commitment_pattern=commitment_pattern,
        relationship_blocks=relationship_blocks,
        readiness_path=readiness_path,
        partnership_windows=_partnership_windows(natal),
        remedies=_partnership_remedies(seventh_lord),
    )
    summary = truncate_text(
        f"Partnership Window: 7th lord {seventh_lord} in house {planets[seventh_lord]['house']}, Venus in house {planets['Venus']['house']}, Upapada in {indicators.upapada_sign}.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_partnership_window(payload: BirthInput, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="partnership_window",
        report_slug="partnership-window",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    report = ReportEnvelope(**document)
    report = await enrich_partnership_window_with_claude(report, {"natal_snapshot": natal})
    document = report.model_dump(mode="python")
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    state_user = getattr(request.state, "user", None) or {}
    if state_user.get("user_id"):
        await register_arc_angel_report_run(get_db(request), str(state_user["user_id"]), document.get("report_type"))
    return GenerateResponse(report=report)


@router.get("/history", response_model=HistoryResponse)
async def get_partnership_window_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "partnership_window"}).sort("created_at", -1).to_list(length=10)
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
