from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    base_history_query,
    build_natal_snapshot,
    build_report_document,
    build_transit_snapshot,
    get_db,
    get_report_collection,
    get_user_email,
    house_lord_for_house,
    shortest_arc,
)


router = APIRouter(prefix="/api/reports/encounter-window", tags=["reports", "love"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EncounterWindowGenerateRequest(StrictModel):
    date_of_birth: str
    time_of_birth: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city_name: str | None = None
    lookahead_days: int = 90
    reference_date: str | None = None


class EncounterWindowPeakWindow(StrictModel):
    trigger_basis: str
    start_date: str
    peak_date: str
    end_date: str
    orb_degrees: float | None = None
    note: str


class EncounterWindowCurrentStatus(StrictModel):
    active: bool
    headline: str
    current_date: str
    next_peak_date: str | None = None


class EncounterWindowOutput(StrictModel):
    current_status: EncounterWindowCurrentStatus
    peak_windows: list[EncounterWindowPeakWindow] = Field(default_factory=list)
    personalized_context: str
    remedies: list[str] = Field(default_factory=list)


class EncounterWindowReport(StrictModel):
    id: str
    document_type: str
    report_type: str
    report_slug: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    input_payload: dict[str, Any]
    output_payload: EncounterWindowOutput
    summary: str


class EncounterWindowGenerateResponse(StrictModel):
    report: EncounterWindowReport


class EncounterWindowHistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    summary: str
    created_at: datetime


class EncounterWindowHistoryResponse(StrictModel):
    items: list[EncounterWindowHistoryItem] = Field(default_factory=list)
    page: int
    limit: int
    has_more: bool


def _report_collection(request: Request):
    return get_report_collection(get_db(request))


def _user(request: Request) -> str:
    return get_user_email(request)


def _current_date(payload: EncounterWindowGenerateRequest) -> date:
    if payload.reference_date:
        return date.fromisoformat(payload.reference_date)
    return datetime.now(timezone.utc).astimezone(ZoneInfo(payload.timezone)).date()


def _build_windows(payload: EncounterWindowGenerateRequest) -> tuple[EncounterWindowOutput, dict[str, Any]]:
    natal = build_natal_snapshot(
        date_text=payload.date_of_birth,
        time_text=payload.time_of_birth,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    start_date = _current_date(payload)
    asc_sign = natal["ascendant_sign"]
    seventh_lord = house_lord_for_house(7, asc_sign)
    targets = [
        ("natal Sun", natal["planets"]["Sun"]["longitude"]),
        ("natal Ascendant", natal["ascendant_longitude"]),
        ("natal 7th house lord", natal["planets"][seventh_lord]["longitude"]),
    ]

    raw_windows: list[dict[str, Any]] = []
    for offset in range(payload.lookahead_days):
        day = start_date + timedelta(days=offset)
        transit = build_transit_snapshot(day, payload.timezone, bodies=("Venus", "Jupiter"))
        venus_longitude = transit["planets"]["Venus"]["longitude"]
        jupiter_sign = transit["planets"]["Jupiter"]["sign"]
        for label, target_longitude in targets:
            orb = shortest_arc(venus_longitude, target_longitude)
            if orb <= 3.0:
                raw_windows.append(
                    {
                        "basis": f"Venus to {label}",
                        "date": day.isoformat(),
                        "orb": round(orb, 2),
                        "description": f"Transiting Venus is {orb:.1f}° from your {label.lower()} - attraction and visibility are heightened.",
                    }
                )
        if jupiter_sign in {natal["houses"]["5"], natal["houses"]["7"]}:
            raw_windows.append(
                {
                    "basis": f"Jupiter in natal {5 if jupiter_sign == natal['houses']['5'] else 7}th house",
                    "date": day.isoformat(),
                    "orb": None,
                    "description": f"Transiting Jupiter is moving through your natal {5 if jupiter_sign == natal['houses']['5'] else 7}th house - expansion is active.",
                }
            )

    merged: list[dict[str, Any]] = []
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in raw_windows:
        grouped.setdefault(item["basis"], []).append(item)
    for basis, items in grouped.items():
        items.sort(key=lambda row: row["date"])
        current = {
            "basis": basis,
            "start_date": items[0]["date"],
            "end_date": items[0]["date"],
            "peak_date": items[0]["date"],
            "orb": items[0].get("orb"),
            "note": items[0]["description"],
        }
        for item in items[1:]:
            previous_end = date.fromisoformat(current["end_date"])
            current_date = date.fromisoformat(item["date"])
            if current_date == previous_end + timedelta(days=1):
                current["end_date"] = item["date"]
                if item.get("orb") is not None and (current.get("orb") is None or item["orb"] < current["orb"]):
                    current["orb"] = item["orb"]
                    current["peak_date"] = item["date"]
                    current["note"] = item["description"]
            else:
                merged.append(current)
                current = {
                    "basis": basis,
                    "start_date": item["date"],
                    "end_date": item["date"],
                    "peak_date": item["date"],
                    "orb": item.get("orb"),
                    "note": item["description"],
                }
        merged.append(current)
    merged.sort(key=lambda item: item["start_date"])

    peak_windows = [
        EncounterWindowPeakWindow(
            trigger_basis=item["basis"],
            start_date=item["start_date"],
            peak_date=item["peak_date"],
            end_date=item["end_date"],
            orb_degrees=item.get("orb"),
            note=item["note"],
        )
        for item in merged[:3]
    ]
    today = start_date.isoformat()
    active_today = [item for item in peak_windows if item.start_date <= today <= item.end_date]
    next_peak = next((item for item in peak_windows if item.start_date >= today), None)
    current_status = EncounterWindowCurrentStatus(
        active=bool(active_today),
        headline="A strong encounter window is active today." if active_today else "No immediate peak window is active today.",
        current_date=today,
        next_peak_date=next_peak.start_date if next_peak else None,
    )
    context = (
        f"Venus windows are strongest when they touch your Sun, Ascendant, or 7th lord; Jupiter adds a broader opening when it reaches your 5th or 7th house."
    )
    output = EncounterWindowOutput(
        current_status=current_status,
        peak_windows=peak_windows,
        personalized_context=context,
        remedies=[
            "Wear pink or white on the strongest Venus dates.",
            "Plan social or dating activity when Jupiter opens your 5th or 7th house.",
            "Keep the first move simple and warm when the window is active.",
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
    return output, {"natal": natal, "input_payload": input_payload}


@router.post("/generate", response_model=EncounterWindowGenerateResponse)
async def generate_encounter_window_report(
    payload: EncounterWindowGenerateRequest,
    request: Request,
) -> EncounterWindowGenerateResponse:
    user_email = _user(request)
    output, meta = _build_windows(payload)
    report = EncounterWindowReport(
        **build_report_document(
            user_email=user_email,
            report_type="encounter_window",
            report_slug="encounter-window",
            input_payload=meta["input_payload"],
            output_payload=output.model_dump(mode="python"),
            summary=(
                output.current_status.headline
                if output.current_status.active
                else "A supportive encounter window is building, with the next opening identified in the timeline."
            ),
        )
    )
    await _report_collection(request).insert_one(report.model_dump(mode="python"))
    return EncounterWindowGenerateResponse(report=report)


@router.get("/history", response_model=EncounterWindowHistoryResponse)
async def encounter_window_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
) -> EncounterWindowHistoryResponse:
    user_email = _user(request)
    collection = _report_collection(request)
    query = base_history_query(user_email, "encounter_window")
    skip = (page - 1) * limit
    cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    total = await collection.count_documents(query)
    items = [
        EncounterWindowHistoryItem(
            id=doc["id"],
            report_type=doc["report_type"],
            report_slug=doc["report_slug"],
            summary=doc["summary"],
            created_at=doc["created_at"],
        )
        for doc in docs
    ]
    return EncounterWindowHistoryResponse(items=items, page=page, limit=limit, has_more=skip + limit < total)
