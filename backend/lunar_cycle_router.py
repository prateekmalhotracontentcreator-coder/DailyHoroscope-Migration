from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from math import cos, radians
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field

from lunar_cycle_prompt_service import enrich_lunar_cycle_with_claude
from vedic_shared_utils import (
    base_history_query,
    build_natal_snapshot,
    build_report_document,
    build_transit_snapshot,
    get_db,
    get_nakshatra,
    get_report_collection,
    house_entry_from_longitude,
)


router = APIRouter(prefix="/api/reports/lunar-cycle", tags=["reports", "love"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LunarCycleGenerateRequest(StrictModel):
    date_of_birth: str
    time_of_birth: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city_name: str | None = None
    reference_date: str | None = None


class LunarCycleMoonPhase(StrictModel):
    phase_name: str
    illumination_pct: int
    cycle_day: int
    days_to_full_moon: int
    days_to_new_moon: int


class LunarCycleMoonNakshatra(StrictModel):
    name: str
    pada: int
    lord: str
    longitude: float


class LunarCycleNatalContext(StrictModel):
    natal_moon_sign: str
    transit_house: int


class LunarCyclePractice(StrictModel):
    practice_name: str
    description: str


class LunarCycleWellness(StrictModel):
    phase_wellness_note: str
    nakshatra_wellness_note: str
    weekly_rhythm: list[str] = Field(default_factory=list)
    recommended_practices: list[LunarCyclePractice] = Field(default_factory=list)
    caution_note: str


class LunarCycleOutput(StrictModel):
    reference_date: str
    moon_phase: LunarCycleMoonPhase
    moon_nakshatra: LunarCycleMoonNakshatra
    natal_context: LunarCycleNatalContext
    wellness: LunarCycleWellness
    generated_at: datetime


class LunarCycleReport(StrictModel):
    id: str
    document_type: str
    report_type: str
    report_slug: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    input_payload: dict[str, Any]
    output_payload: LunarCycleOutput
    summary: str


class LunarCycleGenerateResponse(StrictModel):
    report: LunarCycleReport


class LunarCycleHistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    summary: str
    created_at: datetime


class LunarCycleHistoryResponse(StrictModel):
    items: list[LunarCycleHistoryItem] = Field(default_factory=list)
    page: int
    limit: int
    has_more: bool


def _report_collection(request: Request):
    return get_report_collection(get_db(request))


def _optional_user_email(request: Request) -> str | None:
    user = getattr(request.state, "user", None)
    if isinstance(user, dict):
        email = str(user.get("email") or "").strip().lower()
        if email:
            return email
    return None


def _required_user_email(request: Request) -> str:
    email = _optional_user_email(request)
    if email:
        return email
    raise HTTPException(status_code=401, detail="Authentication required")


def _current_date(payload: LunarCycleGenerateRequest) -> date:
    if payload.reference_date:
        return date.fromisoformat(payload.reference_date)
    return datetime.now(timezone.utc).astimezone(ZoneInfo(payload.timezone)).date()


def _phase_angle(sun_longitude: float, moon_longitude: float) -> float:
    return (moon_longitude - sun_longitude) % 360.0


def _phase_name(angle: float) -> str:
    if angle < 22.5 or angle >= 337.5:
        return "New Moon"
    if angle < 67.5:
        return "Waxing Crescent"
    if angle < 112.5:
        return "First Quarter"
    if angle < 157.5:
        return "Waxing Gibbous"
    if angle < 202.5:
        return "Full Moon"
    if angle < 247.5:
        return "Waning Gibbous"
    if angle < 292.5:
        return "Last Quarter"
    return "Waning Crescent"


def _illumination_pct(angle: float) -> int:
    return max(0, min(100, round(((1 - cos(radians(angle))) / 2.0) * 100)))


def _angular_distance(angle: float, target: float) -> float:
    return min((angle - target) % 360.0, (target - angle) % 360.0)


def _moon_metrics(target_date: date, timezone_name: str) -> dict[str, Any]:
    transit = build_transit_snapshot(target_date, timezone_name, bodies=("Sun", "Moon"))
    sun_longitude = float(transit["planets"]["Sun"]["longitude"])
    moon_longitude = float(transit["planets"]["Moon"]["longitude"])
    angle = _phase_angle(sun_longitude, moon_longitude)
    return {
        "transit": transit,
        "sun_longitude": sun_longitude,
        "moon_longitude": moon_longitude,
        "phase_angle": angle,
        "phase_name": _phase_name(angle),
        "illumination_pct": _illumination_pct(angle),
        "nakshatra": get_nakshatra(moon_longitude),
    }


def _nearest_phase_day(reference_date: date, timezone_name: str, target_angle: float, *, direction: int) -> tuple[date, dict[str, Any]]:
    best_day = reference_date
    best_metrics = _moon_metrics(reference_date, timezone_name)
    best_distance = _angular_distance(best_metrics["phase_angle"], target_angle)
    for offset in range(1, 31):
        day = reference_date + timedelta(days=offset * direction)
        metrics = _moon_metrics(day, timezone_name)
        distance = _angular_distance(metrics["phase_angle"], target_angle)
        if distance < best_distance:
            best_day = day
            best_metrics = metrics
            best_distance = distance
    return best_day, best_metrics


def _default_wellness(phase_name: str, nakshatra_name: str, transit_house: int) -> LunarCycleWellness:
    return LunarCycleWellness(
        phase_wellness_note=(
            f"{phase_name} days are best used as a rhythm cue. Stay close to the pace that feels emotionally sustainable, "
            "and let your body show you whether this is a moment for gathering energy, expressing it, or releasing it."
        ),
        nakshatra_wellness_note=(
            f"With the Moon in {nakshatra_name}, the emotional field is moving through your {transit_house}th-house themes. "
            "Use that as a lens for reflection and self-care rather than a fixed prediction."
        ),
        weekly_rhythm=[
            "Notice which days feel naturally expansive and place your more visible tasks there.",
            "Keep one lower-stimulation pocket in the week so emotional noise can settle before it compounds.",
            "Use gentle rituals and regular sleep as the foundation for steadier lunar sensitivity.",
        ],
        recommended_practices=[
            LunarCyclePractice(
                practice_name="Evening Check-In",
                description="Spend a few quiet minutes each evening naming your mood, energy, and what helped you feel regulated.",
            ),
            LunarCyclePractice(
                practice_name="Moon-Aligned Rest",
                description="Protect extra rest or softer scheduling around the emotionally fuller parts of the cycle.",
            ),
            LunarCyclePractice(
                practice_name="Water + Breath Reset",
                description="Use a simple hydration, breath, or bathing ritual when emotions feel louder than usual.",
            ),
        ],
        caution_note="Do not force clarity on an emotionally charged day. Let the cycle settle before turning a temporary wave into a permanent conclusion.",
    )


def _build_report(payload: LunarCycleGenerateRequest) -> tuple[LunarCycleOutput, dict[str, Any]]:
    natal = build_natal_snapshot(
        date_text=payload.date_of_birth,
        time_text=payload.time_of_birth,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        city_name=payload.city_name,
    )
    reference_date = _current_date(payload)
    today_metrics = _moon_metrics(reference_date, payload.timezone)
    next_new_day, _ = _nearest_phase_day(reference_date, payload.timezone, 0.0, direction=1)
    next_full_day, _ = _nearest_phase_day(reference_date, payload.timezone, 180.0, direction=1)
    previous_new_day, _ = _nearest_phase_day(reference_date, payload.timezone, 0.0, direction=-1)
    cycle_day = min(30, max(1, (reference_date - previous_new_day).days + 1))

    transit_house = house_entry_from_longitude(
        today_metrics["moon_longitude"],
        natal["ascendant_sign"],
    )
    moon_nakshatra = today_metrics["nakshatra"]
    output = LunarCycleOutput(
        reference_date=reference_date.isoformat(),
        moon_phase=LunarCycleMoonPhase(
            phase_name=today_metrics["phase_name"],
            illumination_pct=today_metrics["illumination_pct"],
            cycle_day=cycle_day,
            days_to_full_moon=max(0, (next_full_day - reference_date).days),
            days_to_new_moon=max(0, (next_new_day - reference_date).days),
        ),
        moon_nakshatra=LunarCycleMoonNakshatra(
            name=str(moon_nakshatra["name"]),
            pada=int(moon_nakshatra["pada"]),
            lord=str(moon_nakshatra["lord"]),
            longitude=round(today_metrics["moon_longitude"], 2),
        ),
        natal_context=LunarCycleNatalContext(
            natal_moon_sign=str(natal["planets"]["Moon"]["sign"]),
            transit_house=int(transit_house),
        ),
        wellness=_default_wellness(
            today_metrics["phase_name"],
            str(moon_nakshatra["name"]),
            int(transit_house),
        ),
        generated_at=datetime.now(timezone.utc),
    )
    input_payload = {
        "date_of_birth": payload.date_of_birth,
        "time_of_birth": payload.time_of_birth,
        "latitude": payload.latitude,
        "longitude": payload.longitude,
        "timezone": payload.timezone,
        "city_name": payload.city_name,
        "reference_date": payload.reference_date,
    }
    return output, {"input_payload": input_payload, "natal": natal, "moon_metrics": today_metrics}


@router.post("/generate", response_model=LunarCycleGenerateResponse)
async def generate_lunar_cycle_report(
    payload: LunarCycleGenerateRequest,
    request: Request,
) -> LunarCycleGenerateResponse:
    user_email = _optional_user_email(request)
    output, meta = _build_report(payload)
    report = LunarCycleReport(
        **build_report_document(
            user_email=user_email or "",
            report_type="lunar_cycle_wellness",
            report_slug="lunar-cycle",
            input_payload=meta["input_payload"],
            output_payload=output.model_dump(mode="python"),
            summary=(
                f"{output.moon_phase.phase_name} energy is shaping your current wellness rhythm, "
                f"with the Moon moving through your natal {output.natal_context.transit_house}th house."
            ),
        )
    )
    report = await enrich_lunar_cycle_with_claude(report, meta)
    if user_email:
        await _report_collection(request).insert_one(report.model_dump(mode="python"))
    return LunarCycleGenerateResponse(report=report)


@router.get("/history", response_model=LunarCycleHistoryResponse)
async def lunar_cycle_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
) -> LunarCycleHistoryResponse:
    user_email = _required_user_email(request)
    collection = _report_collection(request)
    query = base_history_query(user_email, "lunar_cycle_wellness")
    skip = (page - 1) * limit
    cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    total = await collection.count_documents(query)
    items = [
        LunarCycleHistoryItem(
            id=str(doc.get("id")),
            report_type=str(doc.get("report_type")),
            report_slug=str(doc.get("report_slug")),
            summary=str(doc.get("summary") or ""),
            created_at=doc.get("created_at"),
        )
        for doc in docs
    ]
    return LunarCycleHistoryResponse(
        items=items,
        page=page,
        limit=limit,
        has_more=skip + len(items) < total,
    )
