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
    dates_since_sign_entry,
    dates_until_sign_exit,
    get_db,
    get_report_collection,
    get_user_email,
    house_lord_for_house,
    shortest_arc,
)


router = APIRouter(prefix="/api/reports/intimacy-vitality", tags=["reports", "love"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class IntimacyVitalityGenerateRequest(StrictModel):
    date_of_birth: str
    time_of_birth: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city_name: str | None = None
    lookahead_days: int = 60
    reference_date: str | None = None


class IntimacyWindow(StrictModel):
    trigger_basis: str
    start_date: str
    peak_date: str
    end_date: str
    note: str


class IntimacyVitalityOutput(StrictModel):
    natal_intimacy_signature: str
    current_vitality_phase: str
    peak_windows: list[IntimacyWindow] = Field(default_factory=list)
    energy_navigation_tips: list[str] = Field(default_factory=list)
    remedies: list[str] = Field(default_factory=list)


class IntimacyVitalityReport(StrictModel):
    id: str
    document_type: str
    report_type: str
    report_slug: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    input_payload: dict[str, Any]
    output_payload: IntimacyVitalityOutput
    summary: str


class IntimacyVitalityGenerateResponse(StrictModel):
    report: IntimacyVitalityReport


class IntimacyVitalityHistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    summary: str
    created_at: datetime


class IntimacyVitalityHistoryResponse(StrictModel):
    items: list[IntimacyVitalityHistoryItem] = Field(default_factory=list)
    page: int
    limit: int
    has_more: bool


def _report_collection(request: Request):
    return get_report_collection(get_db(request))


def _user(request: Request) -> str:
    return get_user_email(request)


def _current_date(payload: IntimacyVitalityGenerateRequest) -> date:
    if payload.reference_date:
        return date.fromisoformat(payload.reference_date)
    return datetime.now(timezone.utc).astimezone(ZoneInfo(payload.timezone)).date()


def _build_windows(payload: IntimacyVitalityGenerateRequest) -> tuple[IntimacyVitalityOutput, dict[str, Any]]:
    natal = build_natal_snapshot(
        date_text=payload.date_of_birth,
        time_text=payload.time_of_birth,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    start_date = _current_date(payload)
    eighth_lord = house_lord_for_house(8, natal["ascendant_sign"])
    signature = (
        f"Your intimacy style is shaped by the {natal['houses']['8']} house and its lord {eighth_lord}, with Venus and Mars showing how affection, desire, and trust are expressed."
    )
    today_transit = build_transit_snapshot(start_date, payload.timezone, bodies=("Mars", "Venus"))
    current_mars = today_transit["planets"]["Mars"]["longitude"]
    natal_venus = natal["planets"]["Venus"]["longitude"]
    mars_vs_venus = shortest_arc(current_mars, natal_venus)
    if mars_vs_venus <= 3.0:
        phase = "Current phase: Mars is tightly engaging your Venus - confidence and chemistry are rising."
    elif today_transit["planets"]["Mars"]["sign"] == natal["houses"]["8"]:
        phase = "Current phase: Mars is in your natal 8th house - a strong intimacy and vitality cycle is active."
    else:
        phase = "Current phase: The field is steadier today - conserve energy and build with consistency."

    raw_windows: list[dict[str, Any]] = []
    timezone_name = payload.timezone
    eighth_sign = natal["houses"]["8"]
    for offset in range(payload.lookahead_days):
        day = start_date + timedelta(days=offset)
        transit = build_transit_snapshot(day, timezone_name, bodies=("Mars", "Venus"))
        mars_longitude = transit["planets"]["Mars"]["longitude"]
        orb = shortest_arc(mars_longitude, natal_venus)
        if orb <= 3.0:
            basis = "Mars conjunct natal Venus" if orb <= 2.0 else "Mars tightly near natal Venus"
            raw_windows.append(
                {
                    "basis": basis,
                    "date": day.isoformat(),
                    "note": f"Transiting Mars is {orb:.1f}° from your natal Venus - momentum, passion, and confidence are elevated.",
                }
            )
        if abs(shortest_arc(mars_longitude, natal_venus) - 120.0) <= 3.0:
            raw_windows.append(
                {
                    "basis": "Mars trine natal Venus",
                    "date": day.isoformat(),
                    "note": "Mars is in a supportive trine to your Venus - boldness flows more naturally.",
                }
            )
        if transit["planets"]["Mars"]["sign"] == eighth_sign:
            entry_start = dates_since_sign_entry("Mars", day, timezone_name, eighth_sign)
            entry_end = dates_until_sign_exit("Mars", day, timezone_name, eighth_sign)
            raw_windows.append(
                {
                    "basis": "Mars in natal 8th house",
                    "date": day.isoformat(),
                    "window_start": entry_start,
                    "window_end": entry_end,
                    "note": "Mars has entered your natal 8th house - intensity, courage, and deeper connection are activated.",
                }
            )

    merged: list[dict[str, Any]] = []
    for item in raw_windows:
        if merged and merged[-1]["basis"] == item["basis"]:
            previous_end = date.fromisoformat(merged[-1]["end_date"])
            current_date = date.fromisoformat(item["date"])
            if current_date == previous_end + timedelta(days=1):
                merged[-1]["end_date"] = item["date"]
                continue
        merged.append(
            {
                "basis": item["basis"],
                "start_date": item.get("window_start", item["date"]),
                "end_date": item.get("window_end", item["date"]),
                "peak_date": item["date"],
                "note": item["note"],
            }
        )

    peak_windows = [
        IntimacyWindow(
            trigger_basis=item["basis"],
            start_date=item["start_date"],
            peak_date=item["peak_date"],
            end_date=item["end_date"],
            note=item["note"],
        )
        for item in merged[:4]
    ]
    tips = [
        "Choose a direct but calm tone when Mars is active.",
        "Use rest and recovery on low-energy days so peak days feel sharper.",
        "Treat the 8th-house window as private and intentional, not performative.",
    ]
    output = IntimacyVitalityOutput(
        natal_intimacy_signature=signature,
        current_vitality_phase=phase,
        peak_windows=peak_windows,
        energy_navigation_tips=tips,
        remedies=[
            "Keep a steady movement routine to channel Mars constructively.",
            "Use red or deep rose accents when you want to amplify confidence.",
            "Prioritise honest communication over dramatic escalation.",
        ],
    )
    input_payload = {
        "date_of_birth": payload.date_of_birth,
        "time_of_birth": payload.time_of_birth,
        "latitude": payload.latitude,
        "longitude": payload.longitude,
        "timezone": payload.timezone,
        "city_name": payload.city_name,
        "lookahead_days": payload.lookahead_days,
        "reference_date": payload.reference_date,
    }
    return output, {"input_payload": input_payload, "eighth_lord": eighth_lord}


@router.post("/generate", response_model=IntimacyVitalityGenerateResponse)
async def generate_intimacy_vitality_report(
    payload: IntimacyVitalityGenerateRequest,
    request: Request,
) -> IntimacyVitalityGenerateResponse:
    user_email = _user(request)
    output, meta = _build_windows(payload)
    report = IntimacyVitalityReport(
        **build_report_document(
            user_email=user_email,
            report_type="intimacy_vitality_forecast",
            report_slug="intimacy-vitality",
            input_payload=meta["input_payload"],
            output_payload=output.model_dump(mode="python"),
            summary="Intimacy and vitality are mapped through your 8th-house signature and the nearest Mars timing windows.",
        )
    )
    await _report_collection(request).insert_one(report.model_dump(mode="python"))
    return IntimacyVitalityGenerateResponse(report=report)


@router.get("/history", response_model=IntimacyVitalityHistoryResponse)
async def intimacy_vitality_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
) -> IntimacyVitalityHistoryResponse:
    user_email = _user(request)
    collection = _report_collection(request)
    query = base_history_query(user_email, "intimacy_vitality_forecast")
    skip = (page - 1) * limit
    cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    total = await collection.count_documents(query)
    items = [
        IntimacyVitalityHistoryItem(
            id=doc["id"],
            report_type=doc["report_type"],
            report_slug=doc["report_slug"],
            summary=doc["summary"],
            created_at=doc["created_at"],
        )
        for doc in docs
    ]
    return IntimacyVitalityHistoryResponse(items=items, page=page, limit=limit, has_more=skip + limit < total)
