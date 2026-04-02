from __future__ import annotations

from collections import defaultdict
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
    get_db,
    get_report_collection,
    get_user_email,
    shortest_arc,
)


router = APIRouter(prefix="/api/reports/love-weather", tags=["reports", "love"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LoveWeatherGenerateRequest(StrictModel):
    date_of_birth: str
    time_of_birth: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city_name: str | None = None
    lookahead_days: int = 90
    reference_date: str | None = None


class LoveWeatherMonthItem(StrictModel):
    month: str
    average_score: int
    rating: str
    theme: str
    best_date: str
    caution_date: str


class LoveWeatherDateItem(StrictModel):
    date: str
    score: int
    theme: str


class LoveWeatherOutput(StrictModel):
    arc_summary: str
    monthly_ratings: list[LoveWeatherMonthItem] = Field(default_factory=list)
    key_dates: list[LoveWeatherDateItem] = Field(default_factory=list)
    action_guidance: str
    remedies: list[str] = Field(default_factory=list)


class LoveWeatherReport(StrictModel):
    id: str
    document_type: str
    report_type: str
    report_slug: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    input_payload: dict[str, Any]
    output_payload: LoveWeatherOutput
    summary: str


class LoveWeatherGenerateResponse(StrictModel):
    report: LoveWeatherReport


class LoveWeatherHistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    summary: str
    created_at: datetime


class LoveWeatherHistoryResponse(StrictModel):
    items: list[LoveWeatherHistoryItem] = Field(default_factory=list)
    page: int
    limit: int
    has_more: bool


def _report_collection(request: Request):
    return get_report_collection(get_db(request))


def _user(request: Request) -> str:
    return get_user_email(request)


def _current_date(payload: LoveWeatherGenerateRequest) -> date:
    if payload.reference_date:
        return date.fromisoformat(payload.reference_date)
    return datetime.now(timezone.utc).astimezone(ZoneInfo(payload.timezone)).date()


def _daily_score(day: date, timezone_name: str, natal: dict[str, Any]) -> tuple[int, str]:
    transit = build_transit_snapshot(day, timezone_name)
    score = 50
    themes: list[str] = []
    fifth_sign = natal["houses"]["5"]
    seventh_sign = natal["houses"]["7"]
    venus_sign = transit["planets"]["Venus"]["sign"]
    jupiter_sign = transit["planets"]["Jupiter"]["sign"]
    mars_sign = transit["planets"]["Mars"]["sign"]
    saturn_sign = transit["planets"]["Saturn"]["sign"]
    if venus_sign in {fifth_sign, seventh_sign}:
        score += 14
        themes.append("Venus is expanding attraction")
    if jupiter_sign in {fifth_sign, seventh_sign}:
        score += 18
        themes.append("Jupiter is amplifying opportunity")
    if mars_sign in {fifth_sign, seventh_sign}:
        score -= 12
        themes.append("Mars is raising heat and urgency")
    if saturn_sign in {fifth_sign, seventh_sign}:
        score -= 14
        themes.append("Saturn is asking for patience")

    targets = [
        natal["planets"]["Venus"]["longitude"],
        natal["ascendant_longitude"],
        natal["planets"][natal["house_lords"]["7"]]["longitude"],
    ]
    for body in ("Venus", "Jupiter", "Mars", "Saturn"):
        longitude = transit["planets"][body]["longitude"]
        for target in targets:
            orb_to_conjunction = shortest_arc(longitude, target)
            if orb_to_conjunction <= 3.0:
                if body in {"Venus", "Jupiter"}:
                    score += 6
                    themes.append(f"{body} is closely supporting the natal pattern")
                else:
                    score -= 5
                    themes.append(f"{body} is pressing the natal pattern")
            orb_to_trine = abs(shortest_arc(longitude, target) - 120.0)
            if orb_to_trine <= 3.0:
                if body in {"Venus", "Jupiter"}:
                    score += 4
                else:
                    score -= 3
            orb_to_sextile = abs(shortest_arc(longitude, target) - 60.0)
            if orb_to_sextile <= 3.0:
                if body in {"Venus", "Jupiter"}:
                    score += 3
                else:
                    score -= 2
            orb_to_square = abs(shortest_arc(longitude, target) - 90.0)
            if orb_to_square <= 3.0 and body in {"Mars", "Saturn"}:
                score -= 3
            orb_to_opp = abs(shortest_arc(longitude, target) - 180.0)
            if orb_to_opp <= 3.0 and body in {"Mars", "Saturn"}:
                score -= 4

    score = max(0, min(100, score))
    return score, "; ".join(dict.fromkeys(themes)) if themes else "Stable romantic weather"


def _build_report(payload: LoveWeatherGenerateRequest) -> tuple[LoveWeatherOutput, dict[str, Any]]:
    natal = build_natal_snapshot(
        date_text=payload.date_of_birth,
        time_text=payload.time_of_birth,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    start_date = _current_date(payload)
    daily_rows: list[dict[str, Any]] = []
    for offset in range(payload.lookahead_days):
        day = start_date + timedelta(days=offset)
        score, theme = _daily_score(day, payload.timezone, natal)
        daily_rows.append({"date": day, "score": score, "theme": theme})

    by_month: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in daily_rows:
        by_month[row["date"].strftime("%Y-%m")].append(row)

    monthly_ratings: list[LoveWeatherMonthItem] = []
    for month_key, rows in sorted(by_month.items()):
        average = round(sum(item["score"] for item in rows) / len(rows))
        if average >= 66:
            rating = "expansion"
            theme = "Supportive movement and openness"
        elif average <= 45:
            rating = "caution"
            theme = "Proceed gently and do not force timing"
        else:
            rating = "neutral"
            theme = "Balanced conditions with a mix of signal and pause"
        best = max(rows, key=lambda item: item["score"])
        caution = min(rows, key=lambda item: item["score"])
        monthly_ratings.append(
            LoveWeatherMonthItem(
                month=month_key,
                average_score=int(average),
                rating=rating,
                theme=theme,
                best_date=best["date"].isoformat(),
                caution_date=caution["date"].isoformat(),
            )
        )

    strongest_days = sorted(daily_rows, key=lambda item: item["score"], reverse=True)[:5]
    key_dates = [
        LoveWeatherDateItem(date=item["date"].isoformat(), score=item["score"], theme=item["theme"])
        for item in strongest_days
    ]
    arc_summary = (
        f"The next {payload.lookahead_days} days trend "
        + (
            "toward romance-friendly expansion"
            if sum(item.average_score for item in monthly_ratings) / max(1, len(monthly_ratings)) >= 66
            else "through a mixed but workable stretch"
            if sum(item.average_score for item in monthly_ratings) / max(1, len(monthly_ratings)) > 45
            else "with a clear need for patience and steady pacing"
        )
        + "."
    )
    output = LoveWeatherOutput(
        arc_summary=arc_summary,
        monthly_ratings=monthly_ratings,
        key_dates=key_dates,
        action_guidance="Move on the strongest dates, keep the middle band relaxed, and treat the caution days as recovery or reflection windows.",
        remedies=[
            "Use light social plans when Venus or Jupiter is active.",
            "Avoid initiating serious conversations on the lowest-score days.",
            "Choose restful routines when Saturn dominates the month.",
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
    return output, {"input_payload": input_payload}


@router.post("/generate", response_model=LoveWeatherGenerateResponse)
async def generate_love_weather_report(
    payload: LoveWeatherGenerateRequest,
    request: Request,
) -> LoveWeatherGenerateResponse:
    user_email = _user(request)
    output, meta = _build_report(payload)
    summary = output.arc_summary
    report = LoveWeatherReport(
        **build_report_document(
            user_email=user_email,
            report_type="love_weather",
            report_slug="love-weather",
            input_payload=meta["input_payload"],
            output_payload=output.model_dump(mode="python"),
            summary=summary,
        )
    )
    await _report_collection(request).insert_one(report.model_dump(mode="python"))
    return LoveWeatherGenerateResponse(report=report)


@router.get("/history", response_model=LoveWeatherHistoryResponse)
async def love_weather_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
) -> LoveWeatherHistoryResponse:
    user_email = _user(request)
    collection = _report_collection(request)
    query = base_history_query(user_email, "love_weather")
    skip = (page - 1) * limit
    cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    total = await collection.count_documents(query)
    items = [
        LoveWeatherHistoryItem(
            id=doc["id"],
            report_type=doc["report_type"],
            report_slug=doc["report_slug"],
            summary=doc["summary"],
            created_at=doc["created_at"],
        )
        for doc in docs
    ]
    return LoveWeatherHistoryResponse(items=items, page=page, limit=limit, has_more=skip + limit < total)
