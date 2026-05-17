from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from dharma_purpose_prompt_service import enrich_dharma_purpose_with_claude
from knowledge_engine import register_arc_angel_report_run

from vedic_shared_utils import (
    atmakaraka_planet,
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


router = APIRouter(prefix="/api/reports/dharma-purpose", tags=["reports"])


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


class PurposeWindow(StrictModel):
    planet: str
    start: str
    end: str
    description: str


class DharmaIndicators(StrictModel):
    ninth_lord: str
    ninth_lord_house: int
    jupiter_house: int
    atmakaraka: str
    atmakaraka_degree: float
    planets_in_ninth: list[str]
    moon_nakshatra_lord: str


class DharmaPurposeOutput(StrictModel):
    report_type: Literal["dharma_purpose"] = "dharma_purpose"
    dharma_indicators: DharmaIndicators
    dharma_signature: str
    soul_calling: str
    faith_tests: str
    alignment_path: str
    purpose_windows: list[PurposeWindow]
    remedies: Remedies


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: BirthInput
    output_payload: DharmaPurposeOutput
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


def _purpose_windows(natal: dict[str, Any]) -> list[PurposeWindow]:
    birth_local = local_datetime(natal["input"]["date"], natal["input"]["time"], natal["input"]["timezone"])
    timeline = build_vimshottari_timeline(natal["planets"]["Moon"]["longitude"], birth_local)
    current = current_dasha_periods(timeline, date.today())
    favored = {
        house_lord_for_house(9, natal["ascendant_sign"]),
        "Jupiter",
        atmakaraka_planet(natal["planets"])[0],
    }
    items: list[PurposeWindow] = []
    for maha in timeline["maha_dashas"]:
        if maha["planet"] in favored:
            house_num = int(natal["planets"][maha["planet"]]["house"])
            items.append(
                PurposeWindow(
                    planet=maha["planet"],
                    start=maha["start"],
                    end=maha["end"],
                    description=truncate_words(
                        f"{maha['planet']} periods deepen your purpose through {house_topic(house_num)} and often make mentors, beliefs, and direction more visible.",
                        21,
                    ),
                )
            )
        if len(items) == 3:
            break
    if not items:
        items.append(
            PurposeWindow(
                planet=current["maha_dasha"]["planet"],
                start=current["maha_dasha"]["start"],
                end=current["maha_dasha"]["end"],
                description=truncate_text("Your current dasha is the clearest timing signal for dharma, meaning, and soul-direction work.", 112),
            )
        )
    return items


def _dharma_remedies(anchor_planet: str) -> Remedies:
    mantra = RemedyDetail(
        text="Om Gurave Namah",
        transliteration="om gurave namah",
        practice=truncate_text("Chant 108 times on Thursday before study, prayer, or a decision that asks for moral clarity.", 60),
    )
    gemstone = GemstoneDetail(stone="Yellow Sapphire", purpose=truncate_text(f"May support clearer {anchor_planet.lower()} alignment and faith-led judgment.", 18))
    ritual = truncate_text("Offer gratitude to a teacher, ancestor, or guide each Thursday before beginning important work.", 40)
    return Remedies(mantra=mantra, gemstone=gemstone, ritual=ritual)


def _build_output(payload: BirthInput) -> tuple[dict[str, Any], DharmaPurposeOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date,
        time_text=payload.time,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    planets = natal["planets"]
    ninth_lord = house_lord_for_house(9, natal["ascendant_sign"])
    atmakaraka, atmakaraka_degree = atmakaraka_planet(planets)
    planets_in_ninth = [name for name, details in planets.items() if int(details["house"]) == 9]
    ninth_aspects = planets_aspecting_house(planets, 9)
    indicators = DharmaIndicators(
        ninth_lord=ninth_lord,
        ninth_lord_house=int(planets[ninth_lord]["house"]),
        jupiter_house=int(planets["Jupiter"]["house"]),
        atmakaraka=atmakaraka,
        atmakaraka_degree=round(atmakaraka_degree, 2),
        planets_in_ninth=planets_in_ninth,
        moon_nakshatra_lord=str(natal["moon_nakshatra"]["lord"]),
    )
    dharma_signature = truncate_words(
        f"Your 9th house is led by {ninth_lord}, placed in the {planets[ninth_lord]['house']}th house, so dharma ripens through {house_topic(int(planets[ninth_lord]['house']))}.",
        31,
    )
    soul_calling = truncate_words(
        f"Jupiter in house {planets['Jupiter']['house']} and the Atmakaraka {atmakaraka} describe a soul path that strengthens when wisdom, integrity, and lived conviction are allowed to lead.",
        31,
    )
    faith_tests = truncate_words(
        f"Planets in or aspecting the 9th ({', '.join(sorted(set(planets_in_ninth + ninth_aspects))) or 'none'}) show where meaning can turn into doubt, over-certainty, or teacher wounds before clarity returns.",
        31,
    )
    alignment_path = truncate_words(
        f"The path forward asks for steady practice: trust the Moon's {natal['moon_nakshatra']['lord']}-ruled rhythm, honor mentors, and let {atmakaraka.lower()} qualities mature through action.",
        30,
    )
    output = DharmaPurposeOutput(
        dharma_indicators=indicators,
        dharma_signature=dharma_signature,
        soul_calling=soul_calling,
        faith_tests=faith_tests,
        alignment_path=alignment_path,
        purpose_windows=_purpose_windows(natal),
        remedies=_dharma_remedies(ninth_lord),
    )
    summary = truncate_text(
        f"Dharma & Purpose: 9th lord {ninth_lord} in house {planets[ninth_lord]['house']}, Jupiter in house {planets['Jupiter']['house']}, Atmakaraka {atmakaraka}.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_dharma_purpose(payload: BirthInput, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="dharma_purpose",
        report_slug="dharma-purpose",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    report = ReportEnvelope(**document)
    report = await enrich_dharma_purpose_with_claude(report, {"natal_snapshot": natal})
    document = report.model_dump(mode="python")
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    state_user = getattr(request.state, "user", None) or {}
    if state_user.get("user_id"):
        await register_arc_angel_report_run(get_db(request), str(state_user["user_id"]), document.get("report_type"))
    return GenerateResponse(report=report)


@router.get("/history", response_model=HistoryResponse)
async def get_dharma_purpose_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "dharma_purpose"}).sort("created_at", -1).to_list(length=10)
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
