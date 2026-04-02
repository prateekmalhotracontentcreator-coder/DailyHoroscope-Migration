from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    build_natal_snapshot,
    build_report_document,
    build_vimshottari_timeline,
    get_db,
    get_report_collection,
    get_user_email,
    house_lord_for_house,
    local_datetime,
    now_utc,
)


router = APIRouter(prefix="/api/reports/soulmate-timing", tags=["soulmate-timing"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SoulmateTimingGenerateRequest(StrictModel):
    date_of_birth: str
    time_of_birth: str
    timezone: str = "Asia/Kolkata"
    latitude: float
    longitude: float
    city_name: str | None = None


class SoulmateWindow(StrictModel):
    start: str
    end: str
    planet: str
    years: float
    note: str


class SoulmateTimingOutput(StrictModel):
    birth_nakshatra: str
    birth_nakshatra_lord: str
    strongest_relationship_lords: list[str]
    peak_windows: list[SoulmateWindow]
    timing_note: str
    remedies: list[str]


class SoulmateTimingReport(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    input_payload: SoulmateTimingGenerateRequest
    output_payload: SoulmateTimingOutput
    summary: str


class SoulmateTimingGenerateResponse(StrictModel):
    report: SoulmateTimingReport


class SoulmateTimingHistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    summary: str
    created_at: datetime


class SoulmateTimingHistoryResponse(StrictModel):
    items: list[SoulmateTimingHistoryItem] = Field(default_factory=list)
    total: int


def _collection(request: Request):
    return get_report_collection(get_db(request))


def _build_output(payload: SoulmateTimingGenerateRequest) -> tuple[dict[str, Any], SoulmateTimingOutput, str]:
    birth_local = local_datetime(payload.date_of_birth, payload.time_of_birth, payload.timezone)
    natal = build_natal_snapshot(
        date_text=payload.date_of_birth,
        time_text=payload.time_of_birth,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    moon_nakshatra = natal["moon_nakshatra"]
    timeline = build_vimshottari_timeline(natal["planets"]["Moon"]["longitude"], birth_local)
    seventh_lord = house_lord_for_house(7, natal["ascendant_sign"])
    strongest_lords = ["Venus", "Jupiter", seventh_lord]
    peak_windows: list[SoulmateWindow] = []
    for item in timeline["maha_dashas"]:
        if item["planet"] in {"Venus", "Jupiter", "Moon"} or item["planet"] == strongest_lords[2]:
            peak_windows.append(
                SoulmateWindow(
                    start=item["start"],
                    end=item["end"],
                    planet=item["planet"],
                    years=float(item["years"]),
                    note=f"{item['planet']} periods can open relationship themes with more clarity and visibility.",
                )
            )
    peak_windows = peak_windows[:5]
    timing_note = (
        f"Your birth Moon is in {moon_nakshatra['name']} ruled by {moon_nakshatra['lord']}, so Venus and Jupiter-linked dasha periods deserve special attention."
    )
    remedies = [
        "Track Venus, Jupiter, and 7th-lord dasha periods before making major partnership decisions.",
        "Use the more supportive windows for introductions, commitment talks, and relationship planning.",
        "Keep a simple timing journal so your lived experience can refine future predictions.",
    ]
    output = SoulmateTimingOutput(
        birth_nakshatra=moon_nakshatra["name"],
        birth_nakshatra_lord=moon_nakshatra["lord"],
        strongest_relationship_lords=strongest_lords,
        peak_windows=peak_windows,
        timing_note=timing_note,
        remedies=remedies,
    )
    summary = f"Your strongest relationship timing lives in Venus, Jupiter, and 7th-lord dasha periods around {moon_nakshatra['name']}."
    return natal, output, summary


@router.post("/generate", response_model=SoulmateTimingGenerateResponse)
async def generate_soulmate_timing_report(payload: SoulmateTimingGenerateRequest, request: Request) -> SoulmateTimingGenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    now = now_utc()
    report = SoulmateTimingReport(
        id=str(uuid4()),
        report_type="soulmate_timing",
        report_slug="soulmate-timing",
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
    return SoulmateTimingGenerateResponse(report=report)


@router.get("/history", response_model=SoulmateTimingHistoryResponse)
async def get_soulmate_timing_history(request: Request) -> SoulmateTimingHistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "report_type": "soulmate_timing"}).sort("created_at", -1).to_list(length=50)
    return SoulmateTimingHistoryResponse(
        items=[
            SoulmateTimingHistoryItem(
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
