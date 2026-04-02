from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any, Literal
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    build_natal_snapshot,
    build_transit_snapshot,
    get_db,
    get_report_collection,
    get_user_email,
    now_utc,
    planet_house_from_longitude,
)


router = APIRouter(prefix="/api/reports/venus-retrograde", tags=["venus-retrograde"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class VenusRetrogradeGenerateRequest(StrictModel):
    date_of_birth: str
    time_of_birth: str
    timezone: str = "Asia/Kolkata"
    latitude: float
    longitude: float
    city_name: str | None = None


class VenusRetrogradeSection(StrictModel):
    section_id: str
    title: str
    summary: str
    body: str


class VenusRetrogradeOutput(StrictModel):
    natal_venus_sign: str
    natal_venus_house: int
    natal_venus_retrograde: bool
    transit_date: str
    transiting_venus_sign: str
    transiting_venus_house: int
    transiting_venus_retrograde: bool
    retrograde_house_signs: list[str]
    personal_impact: str
    healing_focus: str
    best_practice: str
    remedies: list[str]
    sections: list[VenusRetrogradeSection]


class VenusRetrogradeReport(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    input_payload: VenusRetrogradeGenerateRequest
    output_payload: VenusRetrogradeOutput
    summary: str


class VenusRetrogradeGenerateResponse(StrictModel):
    report: VenusRetrogradeReport


class VenusRetrogradeHistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    summary: str
    created_at: datetime


class VenusRetrogradeHistoryResponse(StrictModel):
    items: list[VenusRetrogradeHistoryItem] = Field(default_factory=list)
    total: int


def _collection(request: Request):
    return get_report_collection(get_db(request))


def _build_output(payload: VenusRetrogradeGenerateRequest) -> tuple[dict[str, Any], VenusRetrogradeOutput, str]:
    today = datetime.now(ZoneInfo(payload.timezone)).date()
    natal = build_natal_snapshot(
        date_text=payload.date_of_birth,
        time_text=payload.time_of_birth,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    transit = build_transit_snapshot(today, payload.timezone, bodies=("Venus",))
    venus = natal["planets"]["Venus"]
    transiting_venus = transit["planets"]["Venus"]
    retrograde_house_signs = [natal["houses"]["5"], natal["houses"]["7"]]
    active_house = transiting_venus["sign"] if transiting_venus["retrograde"] and transiting_venus["sign"] in retrograde_house_signs else None
    personal_impact = (
        f"Your natal Venus sits in {venus['sign']} in the {venus['house']}th house, so Venus retrograde periods tend to press on love, self-worth, and relational pacing."
    )
    healing_focus = (
        f"When Venus moves retrograde through {retrograde_house_signs[0]} or {retrograde_house_signs[1]}, review old patterns before starting new romantic commitments."
    )
    if transiting_venus["retrograde"] and active_house:
        best_practice = f"Venus is retrograde in your {active_house} house zone right now, so pause, revise, and simplify before making fresh romantic commitments."
    else:
        best_practice = "Pause, revise, and simplify. Let desire become clearer before you decide what to pursue."
    remedies = [
        "Slow your pace on beauty, dating, and spending decisions during Venus retrograde weeks.",
        "Use journaling to name the kind of affection you actually want instead of what you think you should want.",
        "Lean on soothing rituals, soft music, and deliberate rest when relational confusion rises.",
    ]
    sections = [
        VenusRetrogradeSection(
            section_id="impact",
            title="Personal Impact",
            summary=personal_impact,
            body="This section explains how Venus retrograde themes interact with your natal Venus placement and relationship style.",
        ),
        VenusRetrogradeSection(
            section_id="healing",
        title="Healing Focus",
        summary=healing_focus,
        body="Venus retrograde is best used for reflection, correction, and re-evaluation rather than major launches.",
        ),
    ]
    output = VenusRetrogradeOutput(
        natal_venus_sign=venus["sign"],
        natal_venus_house=venus["house"],
        natal_venus_retrograde=venus["retrograde"],
        transit_date=today.isoformat(),
        transiting_venus_sign=transiting_venus["sign"],
        transiting_venus_house=planet_house_from_longitude(transiting_venus["longitude"], natal["ascendant_sign"]),
        transiting_venus_retrograde=transiting_venus["retrograde"],
        retrograde_house_signs=retrograde_house_signs,
        personal_impact=personal_impact,
        healing_focus=healing_focus,
        best_practice=best_practice,
        remedies=remedies,
        sections=sections,
    )
    summary = f"Venus retrograde will feel most personal through your {venus['sign']} Venus, with today's transit falling in {transiting_venus['sign']}."
    return natal, output, summary


@router.post("/generate", response_model=VenusRetrogradeGenerateResponse)
async def generate_venus_retrograde_report(payload: VenusRetrogradeGenerateRequest, request: Request) -> VenusRetrogradeGenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    now = now_utc()
    report = VenusRetrogradeReport(
        id=str(uuid4()),
        report_type="venus_retrograde_personal_impact",
        report_slug="venus-retrograde",
        user_email=user_email,
        created_at=now,
        updated_at=now,
        input_payload=payload,
        output_payload=output,
        summary=summary,
    )
    document = report.model_dump(mode="python")
    document["natal_snapshot"] = natal
    await _collection(request).insert_one(document)
    return VenusRetrogradeGenerateResponse(report=report)


@router.get("/history", response_model=VenusRetrogradeHistoryResponse)
async def get_venus_retrograde_history(request: Request) -> VenusRetrogradeHistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "report_type": "venus_retrograde_personal_impact"}).sort("created_at", -1).to_list(length=50)
    return VenusRetrogradeHistoryResponse(
        items=[
            VenusRetrogradeHistoryItem(
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
