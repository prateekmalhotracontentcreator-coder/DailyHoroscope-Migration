from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class GSTLedgerEntry(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str = Field(alias="_id")
    ledger_type: str
    source_order_id: Optional[str] = None
    party_name: str
    party_gstin: Optional[str] = None
    transaction_date: datetime = Field(default_factory=utc_now)
    taxable_value: float
    cgst: float = 0.0
    sgst: float = 0.0
    igst: float = 0.0
    total_invoice_value: float
    reconciliation_status: str = "PENDING_RECON"
    source_email_id: Optional[str] = None
    notes: Optional[str] = None
