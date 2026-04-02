from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    build_natal_snapshot,
    build_report_document,
    get_db,
    get_report_collection,
    get_user_email,
    house_lord_for_house,
    now_utc,
)


router = APIRouter(prefix="/api/reports/digital-dating", tags=["digital-dating"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DigitalDatingGenerateRequest(StrictModel):
    date_of_birth: str
    time_of_birth: str
    timezone: str = "Asia/Kolkata"
    latitude: float
    longitude: float
    city_name: str | None = None


class DigitalDatingSection(StrictModel):
    section_id: str
    title: str
    summary: str
    body: str


class DigitalDatingOutput(StrictModel):
    ascendant_sign: str
    fifth_house_sign: str
    fifth_house_lord: str
    venus_sign: str
    venus_house: int
    mars_sign: str
    mars_house: int
    seventh_house_sign: str
    seventh_house_lord: str
    attraction_signature: str
    dating_style: str
    ideal_partner_profile: str
    first_date_lead: str
    self_red_flags: list[str]
    remedies: list[str]
    sections: list[DigitalDatingSection]


class DigitalDatingReport(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    input_payload: DigitalDatingGenerateRequest
    output_payload: DigitalDatingOutput
    summary: str


class DigitalDatingGenerateResponse(StrictModel):
    report: DigitalDatingReport


class DigitalDatingHistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    summary: str
    created_at: datetime


class DigitalDatingHistoryResponse(StrictModel):
    items: list[DigitalDatingHistoryItem] = Field(default_factory=list)
    total: int


def _build_output(payload: DigitalDatingGenerateRequest) -> tuple[dict[str, Any], DigitalDatingOutput, str]:
    natal = build_natal_snapshot(
        date_text=payload.date_of_birth,
        time_text=payload.time_of_birth,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    asc_sign = natal["ascendant_sign"]
    fifth_sign = natal["houses"]["5"]
    seventh_sign = natal["houses"]["7"]
    planets = natal["planets"]
    fifth_lord = house_lord_for_house(5, asc_sign)
    seventh_lord = house_lord_for_house(7, asc_sign)
    venus = planets["Venus"]
    mars = planets["Mars"]
    attraction_signature = f"{venus['sign']} Venus in the {venus['house']}th house draws attention through style, grace, and selectivity."
    dating_style = f"Your 5th house is {fifth_sign}, so romance tends to work best when it stays creative, playful, and lightly expressive."
    ideal_partner_profile = f"You are most drawn to partners with {seventh_sign} qualities and {seventh_lord} themes of {seventh_lord.lower()}."
    first_date_lead = f"Lead with topics that reflect {fifth_lord} and {venus['sign']} - this helps you feel natural instead of overly performative."
    self_red_flags = [
        "Over-editing your own desire until you sound less direct than you feel.",
        "Moving too quickly when Mars is emphasized and later regretting the pace.",
        "Testing for reassurance instead of letting interest build organically.",
    ]
    remedies = [
        "Wear colors that match your Venus sign on days when you want to be seen warmly.",
        "Keep your dating profile clear, current, and lightly playful rather than overloaded.",
        "Use a short pre-date grounding ritual so your tone stays relaxed and authentic.",
    ]
    sections = [
        DigitalDatingSection(
            section_id="attraction_signature",
            title="Attraction Signature",
            summary=attraction_signature,
            body="This section translates Venus, Lagna, and the 5th house into the way attraction tends to flow around you.",
        ),
        DigitalDatingSection(
            section_id="dating_style",
            title="Dating Style",
            summary=dating_style,
            body="The 5th house describes how you flirt, play, and open up to romantic possibility.",
        ),
        DigitalDatingSection(
            section_id="ideal_partner",
            title="Ideal Partner Profile",
            summary=ideal_partner_profile,
            body="The 7th house and its lord describe the style of partnership you naturally respect and seek out.",
        ),
    ]
    output = DigitalDatingOutput(
        ascendant_sign=asc_sign,
        fifth_house_sign=fifth_sign,
        fifth_house_lord=fifth_lord,
        venus_sign=venus["sign"],
        venus_house=venus["house"],
        mars_sign=mars["sign"],
        mars_house=mars["house"],
        seventh_house_sign=seventh_sign,
        seventh_house_lord=seventh_lord,
        attraction_signature=attraction_signature,
        dating_style=dating_style,
        ideal_partner_profile=ideal_partner_profile,
        first_date_lead=first_date_lead,
        self_red_flags=self_red_flags,
        remedies=remedies,
        sections=sections,
    )
    summary = f"Your dating style is shaped by {venus['sign']} Venus, a {fifth_sign} 5th house, and a {seventh_sign} partnership axis."
    return natal, output, summary


def _collection(request: Request):
    return get_report_collection(get_db(request))


@router.post("/generate", response_model=DigitalDatingGenerateResponse)
async def generate_digital_dating_report(payload: DigitalDatingGenerateRequest, request: Request) -> DigitalDatingGenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    now = now_utc()
    report = DigitalDatingReport(
        id=str(uuid4()),
        report_type="digital_dating_strategy",
        report_slug="digital-dating",
        user_email=user_email,
        created_at=now,
        updated_at=now,
        input_payload=payload,
        output_payload=output,
        summary=summary,
    )
    document = report.model_dump(mode="python")
    document["report_type"] = report.report_type
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    return DigitalDatingGenerateResponse(report=report)


@router.get("/history", response_model=DigitalDatingHistoryResponse)
async def get_digital_dating_history(request: Request) -> DigitalDatingHistoryResponse:
    user_email = get_user_email(request)
    collection = _collection(request)
    cursor = collection.find({"user_email": user_email, "report_type": "digital_dating_strategy"}).sort("created_at", -1)
    items = await cursor.to_list(length=50)
    return DigitalDatingHistoryResponse(
        items=[
            DigitalDatingHistoryItem(
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
