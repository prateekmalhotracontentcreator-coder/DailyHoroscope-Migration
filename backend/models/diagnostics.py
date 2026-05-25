from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TelemetryEvent(BaseModel):
    timestamp: datetime = Field(default_factory=utc_now)
    page_url: str
    event_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TelemetryLogRequest(TelemetryEvent):
    user_id: Optional[str] = None


class UserDiagnosticProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    last_updated: datetime = Field(default_factory=utc_now)
    is_claim_flagged: bool = False
    event_stream: List[TelemetryEvent] = Field(default_factory=list)


class DiagnosticFlagRequest(BaseModel):
    flagged: bool
