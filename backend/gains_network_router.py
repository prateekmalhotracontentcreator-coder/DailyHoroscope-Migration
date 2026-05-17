from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from gains_network_prompt_service import enrich_gains_network_with_claude
from knowledge_engine import register_arc_angel_report_run

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


router = APIRouter(prefix="/api/reports/gains-network", tags=["reports"])


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


class GainsWindow(StrictModel):
    planet: str
    start: str
    end: str
    description: str


class GainsIndicators(StrictModel):
    eleventh_lord: str
    eleventh_lord_house: int
    saturn_house: int
    lagna_lord: str
    lagna_lord_house: int
    planets_in_eleventh: list[str]


class GainsNetworkOutput(StrictModel):
    report_type: Literal["gains_network"] = "gains_network"
    gains_indicators: GainsIndicators
    gains_signature: str
    network_style: str
    aspiration_blocks: str
    activation_path: str
    gains_windows: list[GainsWindow]
    remedies: Remedies


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: BirthInput
    output_payload: GainsNetworkOutput
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


def _gains_windows(natal: dict[str, Any]) -> list[GainsWindow]:
    birth_local = local_datetime(natal["input"]["date"], natal["input"]["time"], natal["input"]["timezone"])
    timeline = build_vimshottari_timeline(natal["planets"]["Moon"]["longitude"], birth_local)
    current = current_dasha_periods(timeline, date.today())
    favored = {
        house_lord_for_house(11, natal["ascendant_sign"]),
        house_lord_for_house(2, natal["ascendant_sign"]),
        "Saturn",
        "Jupiter",
    }
    items: list[GainsWindow] = []
    for maha in timeline["maha_dashas"]:
        if maha["planet"] in favored:
            house_num = int(natal["planets"][maha["planet"]]["house"])
            items.append(
                GainsWindow(
                    planet=maha["planet"],
                    start=maha["start"],
                    end=maha["end"],
                    description=truncate_words(
                        f"{maha['planet']} periods tend to widen gains, alliances, and long-range payoff through {house_topic(house_num)}.",
                        18,
                    ),
                )
            )
        if len(items) == 3:
            break
    if not items:
        items.append(
            GainsWindow(
                planet=current["maha_dasha"]["planet"],
                start=current["maha_dasha"]["start"],
                end=current["maha_dasha"]["end"],
                description=truncate_text("Your current dasha is the clearest timing signal for network expansion and practical gains.", 104),
            )
        )
    return items


def _gains_remedies(anchor_planet: str) -> Remedies:
    mantra = RemedyDetail(
        text="Om Sham Shanicharaya Namah",
        transliteration="om sham shanicharaya namah",
        practice=truncate_text("Chant 108 times on Saturday while reflecting on alliances, patience, and long-term goals.", 60),
    )
    gemstone = GemstoneDetail(stone="Amethyst", purpose=truncate_text(f"May support steadier {anchor_planet.lower()}-led discipline around gains and networks.", 22))
    ritual = truncate_text("Make one Saturday offering of time, service, or gratitude to strengthen reciprocal support.", 40)
    return Remedies(mantra=mantra, gemstone=gemstone, ritual=ritual)


def _build_output(payload: BirthInput) -> tuple[dict[str, Any], GainsNetworkOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date,
        time_text=payload.time,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    planets = natal["planets"]
    eleventh_lord = house_lord_for_house(11, natal["ascendant_sign"])
    lagna_lord = house_lord_for_house(1, natal["ascendant_sign"])
    planets_in_eleventh = [name for name, details in planets.items() if int(details["house"]) == 11]
    eleventh_aspects = planets_aspecting_house(planets, 11)
    indicators = GainsIndicators(
        eleventh_lord=eleventh_lord,
        eleventh_lord_house=int(planets[eleventh_lord]["house"]),
        saturn_house=int(planets["Saturn"]["house"]),
        lagna_lord=lagna_lord,
        lagna_lord_house=int(planets[lagna_lord]["house"]),
        planets_in_eleventh=planets_in_eleventh,
    )
    gains_signature = truncate_words(
        f"Your gains story is led by the 11th lord {eleventh_lord} in the {planets[eleventh_lord]['house']}th house, linking fulfillment to {house_topic(int(planets[eleventh_lord]['house']))}.",
        31,
    )
    network_style = truncate_words(
        f"Planets in or aspecting the 11th ({', '.join(sorted(set(planets_in_eleventh + eleventh_aspects))) or 'none'}) show how friends, audiences, and professional circles convert effort into support.",
        30,
    )
    aspiration_blocks = truncate_words(
        f"With Saturn in house {planets['Saturn']['house']} and the Lagna lord in house {planets[lagna_lord]['house']}, gains stall when ambition outruns structure or reciprocity becomes one-sided.",
        30,
    )
    activation_path = truncate_words(
        f"Your chart gains momentum when networks are cultivated slowly, promises are kept, and {eleventh_lord.lower()} qualities shape how you ask, share, and collaborate.",
        30,
    )
    output = GainsNetworkOutput(
        gains_indicators=indicators,
        gains_signature=gains_signature,
        network_style=network_style,
        aspiration_blocks=aspiration_blocks,
        activation_path=activation_path,
        gains_windows=_gains_windows(natal),
        remedies=_gains_remedies(eleventh_lord),
    )
    summary = truncate_text(
        f"Gains & Network: 11th lord {eleventh_lord} in house {planets[eleventh_lord]['house']}, Saturn in house {planets['Saturn']['house']}, Lagna lord {lagna_lord}.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_gains_network(payload: BirthInput, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="gains_network",
        report_slug="gains-network",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    report = ReportEnvelope(**document)
    report = await enrich_gains_network_with_claude(report, {"natal_snapshot": natal})
    document = report.model_dump(mode="python")
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    state_user = getattr(request.state, "user", None) or {}
    if state_user.get("user_id"):
        await register_arc_angel_report_run(get_db(request), str(state_user["user_id"]), document.get("report_type"))
    return GenerateResponse(report=report)


@router.get("/history", response_model=HistoryResponse)
async def get_gains_network_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "gains_network"}).sort("created_at", -1).to_list(length=10)
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
