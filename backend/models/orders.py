from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RazorpayOrderLedger(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str = Field(alias="_id")
    user_id: str
    user_email: str
    report_type: str
    report_id: Optional[str] = None
    amount_paise: int
    current_state: str
    ts_cart_add: Optional[datetime] = None
    ts_checkout_init: Optional[datetime] = None
    ts_gateway_open: Optional[datetime] = None
    ts_pmt_success: Optional[datetime] = None
    ts_fulfill_done: Optional[datetime] = None
    ts_comm_sent: Optional[datetime] = None
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    error_log: Optional[str] = None
    order_context: Dict[str, Any] = Field(default_factory=dict)
    generated_report_id: Optional[str] = None


class ForceHealOrderRequest(BaseModel):
    order_id: str
