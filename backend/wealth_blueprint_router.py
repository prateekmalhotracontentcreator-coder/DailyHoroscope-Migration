from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any, Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from knowledge_engine import register_arc_angel_report_run
from wealth_blueprint_prompt_service import enrich_wealth_blueprint_with_claude

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


router = APIRouter(prefix="/api/reports/wealth-blueprint", tags=["reports"])


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


class WealthWindow(StrictModel):
    planet: str
    start: str
    end: str
    description: str


class WealthIndicators(StrictModel):
    second_lord: str
    second_lord_house: int
    eleventh_lord: str
    eleventh_lord_house: int
    jupiter_house: int
    venus_house: int
    dhana_yoga_count: int
    planets_in_second: list[str]


class WealthBlueprintOutput(StrictModel):
    report_type: Literal["wealth_blueprint"] = "wealth_blueprint"
    wealth_indicators: WealthIndicators
    wealth_signature: str
    dhanayoga_profile: str
    abundance_blocks: str
    prosperity_path: str
    wealth_windows: list[WealthWindow]
    remedies: Remedies


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: BirthInput
    output_payload: WealthBlueprintOutput
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


def _wealth_remedies(anchor_planet: str) -> Remedies:
    mantra = RemedyDetail(
        text="Om Shreem Mahalakshmiyei Namah",
        transliteration="om shreem mahalakshmiyei namah",
        practice=truncate_text("Chant 108 times on Friday before reviewing finances, savings, or long-range plans.", 60),
    )
    gemstone = GemstoneDetail(stone="Yellow Citrine", purpose=truncate_text(f"May support steadier {anchor_planet.lower()}-led confidence around value and growth.", 22))
    ritual = truncate_text("Keep one Friday ritual for gratitude, savings discipline, and a clean money intention.", 40)
    return Remedies(mantra=mantra, gemstone=gemstone, ritual=ritual)


def _wealth_windows(natal: dict[str, Any]) -> list[WealthWindow]:
    birth_local = local_datetime(natal["input"]["date"], natal["input"]["time"], natal["input"]["timezone"])
    timeline = build_vimshottari_timeline(natal["planets"]["Moon"]["longitude"], birth_local)
    current = current_dasha_periods(timeline, date.today())
    favored = {
        house_lord_for_house(2, natal["ascendant_sign"]),
        house_lord_for_house(11, natal["ascendant_sign"]),
        house_lord_for_house(9, natal["ascendant_sign"]),
        "Jupiter",
        "Venus",
    }
    items: list[WealthWindow] = []
    for maha in timeline["maha_dashas"]:
        if maha["planet"] in favored:
            house_num = int(natal["planets"][maha["planet"]]["house"])
            items.append(
                WealthWindow(
                    planet=maha["planet"],
                    start=maha["start"],
                    end=maha["end"],
                    description=truncate_words(
                        f"{maha['planet']} periods tend to increase focus on {house_topic(house_num)} and make wealth-building decisions feel more consequential.",
                        22,
                    ),
                )
            )
        if len(items) == 3:
            break
    if not items:
        items.append(
            WealthWindow(
                planet=current["maha_dasha"]["planet"],
                start=current["maha_dasha"]["start"],
                end=current["maha_dasha"]["end"],
                description=truncate_text("Your current dasha remains the clearest timing signal for wealth consolidation and practical abundance choices.", 120),
            )
        )
    return items


def _dhana_yoga_count(planets: dict[str, Any], ascendant_sign: str) -> int:
    second_lord = house_lord_for_house(2, ascendant_sign)
    fifth_lord = house_lord_for_house(5, ascendant_sign)
    ninth_lord = house_lord_for_house(9, ascendant_sign)
    eleventh_lord = house_lord_for_house(11, ascendant_sign)
    important = [second_lord, fifth_lord, ninth_lord, eleventh_lord]
    count = 0
    for index, planet_name in enumerate(important):
        for other in important[index + 1 :]:
            same_house = int(planets[planet_name]["house"]) == int(planets[other]["house"])
            mutual_aspect = planet_name in planets_aspecting_house(planets, int(planets[other]["house"])) or other in planets_aspecting_house(
                planets, int(planets[planet_name]["house"])
            )
            if same_house or mutual_aspect:
                count += 1
    return count


def _build_output(payload: BirthInput) -> tuple[dict[str, Any], WealthBlueprintOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date,
        time_text=payload.time,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    planets = natal["planets"]
    second_lord = house_lord_for_house(2, natal["ascendant_sign"])
    eleventh_lord = house_lord_for_house(11, natal["ascendant_sign"])
    planets_in_second = [name for name, details in planets.items() if int(details["house"]) == 2]
    dhana_yoga_count = _dhana_yoga_count(planets, natal["ascendant_sign"])
    indicators = WealthIndicators(
        second_lord=second_lord,
        second_lord_house=int(planets[second_lord]["house"]),
        eleventh_lord=eleventh_lord,
        eleventh_lord_house=int(planets[eleventh_lord]["house"]),
        jupiter_house=int(planets["Jupiter"]["house"]),
        venus_house=int(planets["Venus"]["house"]),
        dhana_yoga_count=dhana_yoga_count,
        planets_in_second=planets_in_second,
    )
    wealth_signature = truncate_words(
        f"Your abundance pattern begins with the 2nd lord {second_lord} in the {planets[second_lord]['house']}th house, tying money growth to {house_topic(int(planets[second_lord]['house']))}.",
        32,
    )
    dhanayoga_profile = truncate_words(
        f"The chart shows {dhana_yoga_count} visible wealth-link pattern{'s' if dhana_yoga_count != 1 else ''}, with Jupiter in house {planets['Jupiter']['house']} and Venus in house {planets['Venus']['house']} shaping how prosperity becomes sustainable.",
        34,
    )
    abundance_blocks = truncate_words(
        f"Wealth may tighten when values, speech, or self-worth become disconnected from {house_topic(int(planets[eleventh_lord]['house']))}, especially during rushed decisions around gains.",
        32,
    )
    prosperity_path = truncate_words(
        f"Prosperity grows when the 2nd and 11th house story is handled with patience: accumulate steadily, protect trust, and let {second_lord.lower()} qualities lead long-term choices.",
        34,
    )
    output = WealthBlueprintOutput(
        wealth_indicators=indicators,
        wealth_signature=wealth_signature,
        dhanayoga_profile=dhanayoga_profile,
        abundance_blocks=abundance_blocks,
        prosperity_path=prosperity_path,
        wealth_windows=_wealth_windows(natal),
        remedies=_wealth_remedies(second_lord),
    )
    summary = truncate_text(
        f"Wealth Blueprint: 2nd lord {second_lord} in house {planets[second_lord]['house']}, 11th lord {eleventh_lord} in house {planets[eleventh_lord]['house']}, with {dhana_yoga_count} wealth-link patterns noted.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_wealth_blueprint(payload: BirthInput, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="wealth_blueprint",
        report_slug="wealth-blueprint",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    report = ReportEnvelope(**document)
    report = await enrich_wealth_blueprint_with_claude(report, {"natal_snapshot": natal})
    document = report.model_dump(mode="python")
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    state_user = getattr(request.state, "user", None) or {}
    if state_user.get("user_id"):
        await register_arc_angel_report_run(get_db(request), str(state_user["user_id"]), document.get("report_type"))
    return GenerateResponse(report=report)


@router.get("/history", response_model=HistoryResponse)
async def get_wealth_blueprint_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "wealth_blueprint"}).sort("created_at", -1).to_list(length=10)
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
