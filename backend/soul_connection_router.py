from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from vedic_shared_utils import (
    build_natal_snapshot,
    get_db,
    get_report_collection,
    get_user_email,
    now_utc,
    planet_house_from_longitude,
    shortest_arc,
)


router = APIRouter(prefix="/api/reports/soul-connection", tags=["soul-connection"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BirthData(StrictModel):
    date_of_birth: str
    time_of_birth: str
    timezone: str = "Asia/Kolkata"
    latitude: float
    longitude: float
    city_name: str | None = None


class SoulConnectionGenerateRequest(StrictModel):
    person_a: BirthData
    person_b: BirthData


class SynastrySection(StrictModel):
    section_id: str
    title: str
    summary: str
    body: str


class SoulConnectionOutput(StrictModel):
    connection_archetype: str
    attraction_dynamic: str
    emotional_resonance_score: int
    long_term_compatibility: str
    growth_areas: list[str]
    remedies_for_both: list[str]
    overlays: dict[str, list[str]]
    sections: list[SynastrySection]


class SoulConnectionReport(StrictModel):
    id: str
    document_type: Literal["report"] = "report"
    report_type: str
    report_slug: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    input_payload: SoulConnectionGenerateRequest
    output_payload: SoulConnectionOutput
    summary: str


class SoulConnectionGenerateResponse(StrictModel):
    report: SoulConnectionReport


class SoulConnectionHistoryItem(StrictModel):
    id: str
    report_type: str
    report_slug: str
    summary: str
    created_at: datetime


class SoulConnectionHistoryResponse(StrictModel):
    items: list[SoulConnectionHistoryItem] = Field(default_factory=list)
    total: int


def _collection(request: Request):
    return get_report_collection(get_db(request))


def _planetary_synastry(natal_a: dict[str, Any], natal_b: dict[str, Any]) -> dict[str, list[str]]:
    overlays = {"A in B houses": [], "B in A houses": [], "shared aspect notes": []}
    for body in ("Venus", "Mars", "Moon", "Sun", "Saturn"):
        house_in_b = planet_house_from_longitude(natal_a["planets"][body]["longitude"], natal_b["ascendant_sign"])
        house_in_a = planet_house_from_longitude(natal_b["planets"][body]["longitude"], natal_a["ascendant_sign"])
        overlays["A in B houses"].append(f"{body} sits in B's {house_in_b}th house")
        overlays["B in A houses"].append(f"{body} sits in A's {house_in_a}th house")
    venus_mars_orb = shortest_arc(natal_a["planets"]["Venus"]["longitude"], natal_b["planets"]["Mars"]["longitude"])
    moon_moon_orb = shortest_arc(natal_a["planets"]["Moon"]["longitude"], natal_b["planets"]["Moon"]["longitude"])
    moon_sun_orb = shortest_arc(natal_a["planets"]["Moon"]["longitude"], natal_b["planets"]["Sun"]["longitude"])
    saturn_overlay = shortest_arc(natal_a["planets"]["Saturn"]["longitude"], natal_b["planets"]["Sun"]["longitude"])
    overlays["shared aspect notes"] = [
        f"Venus-Mars orb is {venus_mars_orb:.1f}°",
        f"Moon-Moon orb is {moon_moon_orb:.1f}°",
        f"Moon-Sun orb is {moon_sun_orb:.1f}°",
        f"Saturn overlay orb is {saturn_overlay:.1f}°",
    ]
    return overlays


def _build_output(payload: SoulConnectionGenerateRequest) -> tuple[dict[str, Any], SoulConnectionOutput, str]:
    natal_a = build_natal_snapshot(
        date_text=payload.person_a.date_of_birth,
        time_text=payload.person_a.time_of_birth,
        latitude=payload.person_a.latitude,
        longitude=payload.person_a.longitude,
        timezone_name=payload.person_a.timezone,
        city_name=payload.person_a.city_name,
    )
    natal_b = build_natal_snapshot(
        date_text=payload.person_b.date_of_birth,
        time_text=payload.person_b.time_of_birth,
        latitude=payload.person_b.latitude,
        longitude=payload.person_b.longitude,
        timezone_name=payload.person_b.timezone,
        city_name=payload.person_b.city_name,
    )
    overlays = _planetary_synastry(natal_a, natal_b)
    venus_mars_score = 100 - int(min(70, shortest_arc(natal_a["planets"]["Venus"]["longitude"], natal_b["planets"]["Mars"]["longitude"]) / 2))
    moon_moon_score = 100 - int(min(50, shortest_arc(natal_a["planets"]["Moon"]["longitude"], natal_b["planets"]["Moon"]["longitude"]) / 2))
    moon_sun_score = 100 - int(min(50, shortest_arc(natal_a["planets"]["Moon"]["longitude"], natal_b["planets"]["Sun"]["longitude"]) / 2))
    saturn_score = 100 - int(min(60, shortest_arc(natal_a["planets"]["Saturn"]["longitude"], natal_b["planets"]["Sun"]["longitude"]) / 2))
    emotional_resonance_score = max(20, min(98, int((moon_moon_score + moon_sun_score) / 2)))
    attraction_dynamic = f"Venus-Mars chemistry gives the bond a {venus_mars_score}% heat factor, while Moon contacts shape emotional ease."
    connection_archetype = "Catalytic and growth-oriented if the stronger Saturn themes are handled consciously."
    long_term_compatibility = f"Saturn overlay pressure sits around {saturn_score}%, so the relationship can last when structure and honesty are maintained."
    growth_areas = [
        "Translate strong chemistry into consistent communication.",
        "Make space for the slower person in the pairing when emotions intensify.",
        "Avoid assuming shared feelings mean shared timing.",
    ]
    remedies_for_both = [
        "Have a clear check-in ritual during stressful transits.",
        "Keep practical relationship agreements visible rather than implied.",
        "Use patience as a strategy, not a passive default.",
    ]
    sections = [
        SynastrySection(
            section_id="connection_archetype",
            title="Connection Archetype",
            summary=connection_archetype,
            body="This section summarises the overall feel of the pair based on the relationship between the two natal charts.",
        ),
        SynastrySection(
            section_id="attraction_dynamic",
            title="Attraction Dynamic",
            summary=attraction_dynamic,
            body="Venus-Mars interplay reveals the texture of desire, pursuit, and attraction between the two people.",
        ),
        SynastrySection(
            section_id="emotional_resonance",
            title="Emotional Resonance",
            summary=f"The emotional resonance score lands at {emotional_resonance_score}%, showing how naturally the two people tune in to one another.",
            body="Moon contacts are used here as the primary indicator of emotional fit and daily ease.",
        ),
    ]
    output = SoulConnectionOutput(
        connection_archetype=connection_archetype,
        attraction_dynamic=attraction_dynamic,
        emotional_resonance_score=emotional_resonance_score,
        long_term_compatibility=long_term_compatibility,
        growth_areas=growth_areas,
        remedies_for_both=remedies_for_both,
        overlays=overlays,
        sections=sections,
    )
    summary = f"This synastry pair blends strong attraction with a moderate-to-strong emotional fit and some Saturn-based growth pressure."
    return {"person_a": natal_a, "person_b": natal_b}, output, summary


@router.post("/generate", response_model=SoulConnectionGenerateResponse)
async def generate_soul_connection_report(payload: SoulConnectionGenerateRequest, request: Request) -> SoulConnectionGenerateResponse:
    user_email = get_user_email(request)
    natal, output, summary = _build_output(payload)
    now = now_utc()
    report = SoulConnectionReport(
        id=str(uuid4()),
        report_type="deep_synastry_soul_connection",
        report_slug="soul-connection",
        user_email=user_email,
        created_at=now,
        updated_at=now,
        input_payload=payload,
        output_payload=output,
        summary=summary,
    )
    document = report.model_dump(mode="python")
    document["synastry_snapshot"] = natal
    await _collection(request).insert_one(document)
    return SoulConnectionGenerateResponse(report=report)


@router.get("/history", response_model=SoulConnectionHistoryResponse)
async def get_soul_connection_history(request: Request) -> SoulConnectionHistoryResponse:
    user_email = get_user_email(request)
    items = await _collection(request).find({"user_email": user_email, "report_type": "deep_synastry_soul_connection"}).sort("created_at", -1).to_list(length=50)
    return SoulConnectionHistoryResponse(
        items=[
            SoulConnectionHistoryItem(
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
