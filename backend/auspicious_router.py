from __future__ import annotations

from datetime import date
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

try:
    from backend.auspicious_data import ACTIVITY_VECTORS
    from backend.auspicious_engine import calculate_month, list_categories, top_days
except ImportError:  # pragma: no cover
    from auspicious_data import ACTIVITY_VECTORS  # type: ignore
    from auspicious_engine import calculate_month, list_categories, top_days  # type: ignore


router = APIRouter(prefix="/api/auspicious", tags=["Auspicious Calculator"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AuspiciousMonthRequest(StrictModel):
    city_id: str
    activity_category: str
    target_month: date
    avoid_retrogrades: bool = False
    exclude_rahu_kalam: bool = False
    birth_date: date | None = None
    activity_vector: Literal["build", "contract", "release", "travel"] | None = None
    filter_personal_clash: bool = True
    system: Literal["dual", "vedic", "chinese"] = "dual"


class TimeWindow(StrictModel):
    start: str | None = None
    end: str | None = None


class VedicDetails(StrictModel):
    tithi: int
    tithi_name: str
    nakshatra: int
    nakshatra_name: str
    vara: int
    vara_name: str
    yoga: int
    yoga_name: str
    karana: int
    karana_name: str
    abhijit_muhurta: TimeWindow | None = None
    rahu_kalam: TimeWindow | None = None


class ChineseDetails(StrictModel):
    day_officer: str
    day_animal: str
    user_animal: str | None = None
    is_personal_clash: bool
    lunar_mansion: str


class AuspiciousDayResponse(StrictModel):
    date: str
    day_name: str
    vedic_score: int
    chinese_score: int
    unified_score: int
    tier: Literal["excellent", "good", "neutral", "blocked"]
    is_blocked: bool
    blockers: list[str] = Field(default_factory=list)
    vedic_details: VedicDetails
    chinese_details: ChineseDetails
    recommendation: str


class CategoriesResponse(StrictModel):
    categories: list[dict]
    activity_vectors: list[dict]


@router.get("/categories", response_model=CategoriesResponse)
async def get_categories() -> CategoriesResponse:
    return CategoriesResponse(
        categories=list_categories(),
        activity_vectors=[
            {"slug": slug, "display_name": config["display_name"]}
            for slug, config in ACTIVITY_VECTORS.items()
        ],
    )


@router.post("/calculate-month", response_model=list[AuspiciousDayResponse])
async def post_calculate_month(payload: AuspiciousMonthRequest) -> list[AuspiciousDayResponse]:
    try:
        days = calculate_month(**payload.model_dump())
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    return [AuspiciousDayResponse(**day) for day in days]


@router.get("/top-days", response_model=list[AuspiciousDayResponse])
async def get_top_days(
    city_id: str,
    category: str,
    month: date,
    limit: int = Query(default=5, ge=1, le=10),
    avoid_retrogrades: bool = False,
    exclude_rahu_kalam: bool = False,
    birth_date: date | None = None,
    activity_vector: Literal["build", "contract", "release", "travel"] | None = None,
    filter_personal_clash: bool = True,
    system: Literal["dual", "vedic", "chinese"] = "dual",
) -> list[AuspiciousDayResponse]:
    try:
        days = calculate_month(
            city_id=city_id,
            activity_category=category,
            target_month=month,
            avoid_retrogrades=avoid_retrogrades,
            exclude_rahu_kalam=exclude_rahu_kalam,
            birth_date=birth_date,
            activity_vector=activity_vector,
            filter_personal_clash=filter_personal_clash,
            system=system,
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    return [AuspiciousDayResponse(**day) for day in top_days(days, limit=limit)]
