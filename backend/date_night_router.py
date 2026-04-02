from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    base_history_query,
    build_natal_snapshot,
    build_report_document,
    build_transit_snapshot,
    clamp_int,
    compute_love_battery,
    get_db,
    get_report_collection,
    get_user_email,
    shortest_arc,
)


router = APIRouter(prefix="/api/reports/date-night", tags=["reports", "love"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DateNightGenerateRequest(StrictModel):
    date_of_birth: str
    time_of_birth: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city_name: str | None = None
    check_date: str | None = None


class DateNightOutput(StrictModel):
    love_battery_percent: int
    score_category: str
    moon_natal_venus_angle: float
    alignment_description: str
    action_note: str
    notification_worthy: bool
    venus_mars_amplifier: dict[str, Any] | None = None


class DateNightReport(StrictModel):
    id: str
    document_type: str
    report_type: str
    report_slug: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    input_payload: dict[str, Any]
    output_payload: DateNightOutput
    summary: str


class DateNightGenerateResponse(StrictModel):
    report: DateNightReport


class DateNightHistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    summary: str
    created_at: datetime


class DateNightHistoryResponse(StrictModel):
    items: list[DateNightHistoryItem] = Field(default_factory=list)
    page: int
    limit: int
    has_more: bool


def _report_collection(request: Request):
    return get_report_collection(get_db(request))


def _user(request: Request) -> str:
    return get_user_email(request)


def _current_date(payload: DateNightGenerateRequest) -> date:
    if payload.check_date:
        return date.fromisoformat(payload.check_date)
    return datetime.now(timezone.utc).astimezone(ZoneInfo(payload.timezone)).date()


def _build_report(payload: DateNightGenerateRequest) -> tuple[DateNightOutput, dict[str, Any]]:
    natal = build_natal_snapshot(
        date_text=payload.date_of_birth,
        time_text=payload.time_of_birth,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    check_date = _current_date(payload)
    transit = build_transit_snapshot(check_date, payload.timezone, bodies=("Moon", "Venus"))
    battery = compute_love_battery(transit["planets"]["Moon"]["longitude"], natal["planets"]["Venus"]["longitude"])
    venus_longitude = transit["planets"]["Venus"]["longitude"]
    natal_mars = natal["planets"]["Mars"]["longitude"]
    amplifier_orb = shortest_arc(venus_longitude, natal_mars)
    amplifier: dict[str, Any] | None = None
    if amplifier_orb <= 5.0:
        amplifier = {
            "aspect": "conjunction" if amplifier_orb <= 3.0 else "supportive passage",
            "orb_degrees": round(amplifier_orb, 2),
            "note": "Transiting Venus is energising your natal Mars - chemistry and initiative are easier to express.",
        }
    score = clamp_int(battery["love_battery_percent"] + (5 if amplifier else 0), 15, 100)
    if score >= 85:
        category = "peak"
    elif score >= 75:
        category = "high"
    elif score >= 55:
        category = "neutral"
    elif score >= 35:
        category = "caution"
    else:
        category = "low"
    output = DateNightOutput(
        love_battery_percent=score,
        score_category=category,
        moon_natal_venus_angle=battery["moon_natal_venus_angle"],
        alignment_description=battery["alignment_description"] + (" " + amplifier["note"] if amplifier else ""),
        action_note=(
            "Ask gently and keep the tone warm." if score >= 80 else "Choose a simple plan and let the mood lead." if score >= 55 else "Keep it low pressure and readable."
        ),
        notification_worthy=score >= 80,
        venus_mars_amplifier=amplifier,
    )
    input_payload = {
        "date_of_birth": payload.date_of_birth,
        "time_of_birth": payload.time_of_birth,
        "latitude": payload.latitude,
        "longitude": payload.longitude,
        "timezone": payload.timezone,
        "city_name": payload.city_name,
        "check_date": payload.check_date,
    }
    return output, {"input_payload": input_payload}


@router.post("/generate", response_model=DateNightGenerateResponse)
async def generate_date_night_report(
    payload: DateNightGenerateRequest,
    request: Request,
) -> DateNightGenerateResponse:
    user_email = _user(request)
    output, meta = _build_report(payload)
    report = DateNightReport(
        **build_report_document(
            user_email=user_email,
            report_type="date_night_score",
            report_slug="date-night",
            input_payload=meta["input_payload"],
            output_payload=output.model_dump(mode="python"),
            summary=f"Love Battery {output.love_battery_percent}% with a {output.score_category} tone for the day.",
        )
    )
    await _report_collection(request).insert_one(report.model_dump(mode="python"))
    return DateNightGenerateResponse(report=report)


@router.get("/history", response_model=DateNightHistoryResponse)
async def date_night_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
) -> DateNightHistoryResponse:
    user_email = _user(request)
    collection = _report_collection(request)
    query = base_history_query(user_email, "date_night_score")
    skip = (page - 1) * limit
    cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    total = await collection.count_documents(query)
    items = [
        DateNightHistoryItem(
            id=doc["id"],
            report_type=doc["report_type"],
            report_slug=doc["report_slug"],
            summary=doc["summary"],
            created_at=doc["created_at"],
        )
        for doc in docs
    ]
    return DateNightHistoryResponse(items=items, page=page, limit=limit, has_more=skip + limit < total)
