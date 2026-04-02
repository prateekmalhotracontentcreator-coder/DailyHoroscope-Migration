from __future__ import annotations

from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    NAKSHATRAS,
    atmakaraka_planet,
    build_natal_snapshot,
    build_report_document,
    get_db,
    get_report_collection,
    get_user_email,
    planets_with_shadow_pressure,
    truncate_text,
    truncate_words,
)


router = APIRouter(prefix="/api/reports/shadow-self", tags=["reports"])


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


class ShadowSelfOutput(StrictModel):
    report_type: Literal["shadow_self"] = "shadow_self"
    janma_nakshatra: str
    shadow_nakshatra: str
    hidden_strengths: str
    blind_spots: str
    psychological_driver: str
    integration_path: str
    remedies: Remedies


class ReportEnvelope(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    input_payload: BirthInput
    output_payload: ShadowSelfOutput
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


def _remedies(shadow_name: str) -> Remedies:
    return Remedies(
        mantra=RemedyDetail(
            text="Om Namah Shivaya",
            transliteration="om namah shivaya",
            practice=truncate_text("Chant 108 times on Mondays or during introspective evenings to settle inner noise.", 60),
        ),
        gemstone=GemstoneDetail(stone="Moonstone", purpose=truncate_text("May support emotional honesty.", 20)),
        ritual=truncate_text(f"Journal about the traits of {shadow_name} and name one way they can become a strength instead of a fear.", 40),
    )


def _build_output(payload: BirthInput) -> tuple[dict, ShadowSelfOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date,
        time_text=payload.time,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    janma = natal["moon_nakshatra"]
    shadow_index = (int(janma["index"]) + 6) % len(NAKSHATRAS)
    shadow = NAKSHATRAS[shadow_index]
    atmakaraka, _ = atmakaraka_planet(natal["planets"])
    twelfth_planets = [name for name, details in natal["planets"].items() if details["house"] == 12]
    pressure = planets_with_shadow_pressure(natal["planets"])
    janma_text = truncate_words(
        f"{janma['name']} gives your public emotional style a {janma['lord'].lower()}-ruled tone of instinct, sensitivity, and pattern memory.",
        40,
    )
    shadow_text = truncate_words(
        f"Your shadow counterpart is {shadow['name']}, revealing hidden intensity around what you avoid, postpone, or keep private.",
        50,
    )
    hidden_strengths = truncate_words(
        f"Planets in the 12th ({', '.join(twelfth_planets) or 'none'}) suggest quiet strengths in solitude, spiritual repair, and subtle perception.",
        50,
    )
    blind_spots = truncate_words(
        f"Atmakaraka {atmakaraka} can overwork one core desire, so your blind spot appears when growth is chased too hard instead of integrated slowly.",
        50,
    )
    if pressure:
        first = pressure[0]
        psychological_driver = truncate_words(
            f"{first['planet']} in {first['sign']} shows suppressed energy that can leak out as overcompensation until it is named clearly.",
            50,
        )
    else:
        psychological_driver = truncate_words(
            "Your shadow pressure is subtler than dramatic, surfacing more through repetition than crisis.", 50
        )
    integration_path = truncate_words(
        f"Work with the {shadow['name']} side by making space for reflection, rest, and honest feedback before reaction hardens into habit.",
        60,
    )
    output = ShadowSelfOutput(
        janma_nakshatra=janma_text,
        shadow_nakshatra=shadow_text,
        hidden_strengths=hidden_strengths,
        blind_spots=blind_spots,
        psychological_driver=psychological_driver,
        integration_path=integration_path,
        remedies=_remedies(shadow["name"]),
    )
    summary = truncate_text(
        f"Shadow Self report: Janma Nakshatra {janma['name']}, shadow counterpart {shadow['name']}, and Atmakaraka {atmakaraka}.",
        140,
    )
    return natal, output, summary


@router.post("/generate", response_model=GenerateResponse)
async def generate_shadow_self_report(payload: BirthInput, request: Request) -> GenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    document = build_report_document(
        user_email=user_email,
        report_type="shadow_self",
        report_slug="shadow-self",
        input_payload=payload.model_dump(),
        output_payload=output.model_dump(),
        summary=summary,
    )
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    return GenerateResponse(report=ReportEnvelope(**document))


@router.get("/history", response_model=HistoryResponse)
async def get_shadow_self_history(request: Request) -> HistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "document_type": "report", "report_type": "shadow_self"}).sort("created_at", -1).to_list(length=50)
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
