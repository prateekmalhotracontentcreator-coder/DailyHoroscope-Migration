from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

try:
    from backend.kp_engine import KPChart, ReportInput, compute_kp_chart
except ImportError:  # pragma: no cover
    from kp_engine import KPChart, ReportInput, compute_kp_chart  # type: ignore


router = APIRouter(prefix="/api/kp", tags=["kp-chart"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class KPBirthChartRequest(StrictModel):
    date_of_birth: str
    time_of_birth: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    place_label: str | None = None
    reference_date: str | None = None


@router.post("/birth-chart")
async def get_kp_birth_chart(payload: KPBirthChartRequest) -> dict[str, Any]:
    engine_payload = ReportInput(
        date_of_birth=payload.date_of_birth,
        time_of_birth=payload.time_of_birth,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_name=payload.timezone,
        place_label=payload.place_label,
        reference_date=payload.reference_date,
    )
    return compute_kp_chart(engine_payload)
