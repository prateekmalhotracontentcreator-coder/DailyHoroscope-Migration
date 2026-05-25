# Commission SHC -- Self-Healing Diagnostics Dashboard

> EverydayHoroscope · Stack: FastAPI + React 18 + Tailwind CSS + MongoDB (Motor async) + pyswisseph 2.10.x
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Live app: https://www.everydayhoroscope.in
> Issued: 2026-05-25
> **3 phases delivered sequentially. Complete SHC-1 acceptance before starting SHC-2. Complete SHC-2 acceptance before starting SHC-3.**

---

## Purpose

Build a Self-Healing Diagnostics Dashboard inside the existing Admin Console (`/admin/dashboard`).
The dashboard gives the admin a real-time, per-user view of:
- Every action a user took on the site (Part 1 -- Telemetry)
- Every stage of their payment and report generation (Part 2 -- Razorpay Lifecycle Ledger)
- GST accounting across all customer and supplier transactions (Part 3 -- GST Ledger)

It must also self-heal: stuck AI generation jobs are automatically detected and re-queued.

---

## Architecture Rules (Mandatory -- all 3 phases)

1. **FastAPI + Motor async only** -- all new endpoints use `async def`. No `pymongo` sync calls.
2. **New MongoDB collections** -- do NOT write to existing `payments`, `users`, or `subscribers` collections.
3. **APScheduler** -- extend the existing scheduler in `server.py`. Do NOT create a separate scheduler instance.
4. **Admin Console tab** -- all UI lives in a new "Self-Heal" tab added to the existing `/admin/dashboard` page. Do NOT create a new route.
5. **Theme** -- follow existing Admin Console styling. Use Tailwind classes only. No new CSS files.
6. **Razorpay** -- the current flow uses client-side `verify_payment()`. SHC-2 adds a parallel server-side webhook endpoint. Do NOT modify the existing `verify_payment` function.
7. **Environment variables** -- all secrets via `os.environ.get()`. Add new vars to the Render env list in the acceptance checklist, do not hardcode.
8. **No breaking changes** -- the existing Admin Console tabs (Subscribers, Compose, Scheduled, History, Social Media) must render identically.

---

## Current State (read before coding)

### Razorpay (server.py)
- `POST /api/payments/create-order` → creates order in `db.payments` collection, returns `razorpay_order_id`
- `verify_payment()` → called from frontend after Razorpay Checkout JS succeeds -- client-driven, not server webhook
- **No server-side webhook endpoint exists.** SHC-2 builds one from scratch.

### APScheduler (server.py)
- Already running: scheduled email notifications, social post tasks
- Pattern: `scheduler.add_job(fn, 'cron', hour=X, minute=Y, id='job_id')`

### Admin Console (frontend)
- File: `frontend/src/pages/admin/AdminDashboard.jsx` (or equivalent admin page)
- Existing tabs: Overview · System · Users · Reports · Payments · Messages · Blog · Notifications
- Add one new tab: **Self-Heal**

---

## Part 1 (SHC-1) -- Telemetry Engine + Diagnostics Admin View

### Objective
Capture every user action on the site. Give the admin a per-user timeline showing pages visited, clicks, time on page, errors, and payment status -- so support disputes can be triaged from one screen.

---

### 1A -- New MongoDB Collection: `user_diagnostics`

```python
# backend/models/diagnostics.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, List, Optional

class TelemetryEvent(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    page_url: str
    event_type: str   # PAGE_VIEW | CLICK | INPUT | ERROR | RAZORPAY_POPUP_OPEN | API_ERROR_4XX | CRITICAL_BACKEND_CRASH
    metadata: Dict[str, Any] = {}

class UserDiagnosticProfile(BaseModel):
    id: str = Field(alias="_id")         # matches user_id / auth user ID
    last_updated: datetime
    is_claim_flagged: bool = False        # admin can set True on dispute
    event_stream: List[TelemetryEvent] = []
```

**Index commands** (run at app startup in `db/indexing.py` or inline in `server.py`):
```python
await db["user_diagnostics"].create_index(
    [("_id", 1), ("last_updated", -1)],
    name="idx_user_lookup_timeline"
)
await db["user_diagnostics"].create_index(
    [("event_stream.timestamp", -1)],
    name="idx_event_time"
)
```

---

### 1B -- Backend: FastAPI Middleware + Log Endpoint

**Middleware** -- add to `server.py` after app initialisation:

```python
# Catches all 4xx/5xx responses and unhandled exceptions → logs to user_diagnostics
class SelfHealingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        user_id = request.cookies.get("session_user_id") or "ANONYMOUS"
        start = datetime.utcnow()
        try:
            response = await call_next(request)
            if response.status_code >= 400 and user_id != "ANONYMOUS":
                await _append_diagnostic_event(user_id, {
                    "page_url": request.url.path,
                    "event_type": f"API_ERROR_{response.status_code}",
                    "metadata": {
                        "method": request.method,
                        "latency_ms": (datetime.utcnow() - start).total_seconds() * 1000
                    }
                })
            return response
        except Exception as exc:
            if user_id != "ANONYMOUS":
                await _append_diagnostic_event(user_id, {
                    "page_url": request.url.path,
                    "event_type": "CRITICAL_BACKEND_CRASH",
                    "metadata": {
                        "exception_class": exc.__class__.__name__,
                        "error_message": str(exc)[:500]
                    }
                })
            raise

async def _append_diagnostic_event(user_id: str, payload: dict):
    payload["timestamp"] = datetime.utcnow()
    try:
        await db["user_diagnostics"].update_one(
            {"_id": user_id},
            {
                "$set": {"last_updated": datetime.utcnow()},
                "$push": {"event_stream": {"$each": [payload], "$slice": -500}}
            },
            upsert=True
        )
    except Exception as e:
        print(f"[Diagnostics] DB write failed: {e}")

app.add_middleware(SelfHealingMiddleware)
```

**Log endpoint** -- frontend fires this fire-and-forget:

```python
@app.post("/api/diagnostics/log", status_code=202)
async def log_telemetry(event: TelemetryEvent, user_id: str):
    await _append_diagnostic_event(user_id, event.model_dump())
    return {"status": "queued"}
```

**Admin read endpoint:**

```python
@app.get("/api/admin/diagnostics/{user_id}")
async def get_user_diagnostics(user_id: str):
    doc = await db["user_diagnostics"].find_one({"_id": user_id})
    if not doc:
        raise HTTPException(404, "No telemetry found for this user")
    return doc

@app.patch("/api/admin/diagnostics/{user_id}/flag")
async def flag_dispute(user_id: str, flagged: bool):
    await db["user_diagnostics"].update_one(
        {"_id": user_id},
        {"$set": {"is_claim_flagged": flagged, "last_updated": datetime.utcnow()}}
    )
    return {"status": "updated"}
```

---

### 1C -- Frontend: `src/diagnostics/telemetry.js`

```js
import axios from 'axios';
const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

export const logEvent = (userId, eventType, pageUrl, metadata = {}) => {
  // Fire-and-forget -- never await this
  axios.post(`${BACKEND}/api/diagnostics/log`, {
    user_id: userId,
    event_type: eventType,
    page_url: pageUrl,
    metadata,
    timestamp: new Date().toISOString()
  }, { withCredentials: true }).catch(() => {});
};

// Call on every route change (wire into App.js useEffect on location)
export const logPageView = (userId, pageUrl, prevUrl) =>
  logEvent(userId, 'PAGE_VIEW', pageUrl, { referrer: prevUrl });

// Call on Razorpay overlay open
export const logRazorpayOpen = (userId, reportType, amount) =>
  logEvent(userId, 'RAZORPAY_POPUP_OPEN', window.location.pathname, { reportType, amount });
```

Wire `logPageView` into `App.js`:
```jsx
// In App.js -- inside a useEffect that watches location
import { logPageView } from './diagnostics/telemetry';
// Call logPageView(user?.id, location.pathname, prevPath) on every location change
```

---

### 1D -- Frontend: `DiagnosticsTab.jsx` (new tab inside Admin Console)

New file: `frontend/src/components/admin/DiagnosticsTab.jsx`

**Features:**
1. **Search bar** -- enter any User ID or email → fetches `/api/admin/diagnostics/{userId}`
2. **User header** -- User ID, last active timestamp, flag badge (green "Verified" / red "Dispute Flagged"), toggle flag button
3. **Event stream log** -- scrollable table: timestamp · event_type chip (red for ERROR, amber for RAZORPAY, blue for PAGE_VIEW) · page_url · metadata JSON (truncated 80 chars)
4. **Quick stats row** -- total events · unique pages · error count · last payment status (pulled from `db.payments` cross-reference)
5. **Flag/Unflag button** -- calls `PATCH /api/admin/diagnostics/{userId}/flag`

Style: `bg-slate-900 border border-amber-500/30 rounded-xl` -- match existing Admin Console card style.

---

### SHC-1 Acceptance Checklist

- [ ] `user_diagnostics` MongoDB collection created with correct indexes
- [ ] Middleware logs 4xx/5xx API errors to the collection without breaking normal request flow
- [ ] `POST /api/diagnostics/log` returns `202` for valid payload
- [ ] `GET /api/admin/diagnostics/{userId}` returns full event stream
- [ ] `PATCH /api/admin/diagnostics/{userId}/flag` toggles `is_claim_flagged`
- [ ] `telemetry.js` exists and `logPageView` is wired in `App.js`
- [ ] DiagnosticsTab renders inside Admin Console as a new "Self-Heal" tab
- [ ] Existing Admin Console tabs render identically
- [ ] Build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` → 0 errors

---

## Part 2 (SHC-2) -- Razorpay Lifecycle Ledger

> Complete SHC-1 acceptance before starting SHC-2.

### Objective
Track every payment from Cart → Payment → Report Generation → Email Confirmation as one row per order. Self-heal stuck orders automatically. Add a server-side Razorpay webhook as the authoritative payment source.

---

### 2A -- New MongoDB Collection: `orders_ledger`

```python
class RazorpayOrderLedger(BaseModel):
    id: str = Field(alias="_id")          # internal order_id / cart_id
    user_id: str
    user_email: str
    report_type: str                       # e.g. "Lal_Kitab_43_Days"
    amount_paise: int
    current_state: str                     # CART_ADD | CHECKOUT_INIT | GATEWAY_OPEN | PAID | FULFILLED | COMM_SENT | FAILED

    # State transition timestamps
    ts_cart_add: Optional[datetime] = None
    ts_checkout_init: Optional[datetime] = None
    ts_gateway_open: Optional[datetime] = None
    ts_pmt_success: Optional[datetime] = None
    ts_fulfill_done: Optional[datetime] = None
    ts_comm_sent: Optional[datetime] = None

    # Provider IDs
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    error_log: Optional[str] = None
```

**Indexes:**
```python
await db["orders_ledger"].create_index(
    [("current_state", 1), ("ts_cart_add", -1)],
    name="idx_funnel_state"
)
await db["orders_ledger"].create_index(
    [("razorpay_order_id", 1)],
    unique=True, sparse=True,
    name="idx_razorpay_webhook_match"
)
await db["orders_ledger"].create_index(
    [("current_state", 1)],
    partialFilterExpression={"current_state": "PAID"},
    name="idx_stuck_fulfillment"
)
await db["orders_ledger"].create_index(
    [("user_id", 1), ("ts_cart_add", -1)],
    name="idx_user_orders"
)
```

---

### 2B -- State Transition Hooks

Instrument the existing `create-order` endpoint to write the initial ledger row:

```python
# In the existing POST /api/payments/create-order handler
# After razorpay_client.order.create() succeeds, ADD:
await db["orders_ledger"].insert_one({
    "_id": str(ObjectId()),
    "user_id": request.user_id or request.user_email,
    "user_email": request.user_email,
    "report_type": request.report_type,
    "amount_paise": amount_paise,
    "current_state": "CART_ADD",
    "razorpay_order_id": razorpay_order["id"],
    "ts_cart_add": datetime.utcnow()
})
```

Advance to `GATEWAY_OPEN` when the frontend fires:
```python
@app.post("/api/diagnostics/order/{razorpay_order_id}/gateway-open")
async def mark_gateway_open(razorpay_order_id: str):
    await db["orders_ledger"].update_one(
        {"razorpay_order_id": razorpay_order_id},
        {"$set": {"current_state": "GATEWAY_OPEN", "ts_gateway_open": datetime.utcnow()}}
    )
    return {"status": "ok"}
```

---

### 2C -- Server-Side Razorpay Webhook Endpoint

```python
import hmac, hashlib

RAZORPAY_WEBHOOK_SECRET = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "")

@app.post("/api/webhooks/razorpay", status_code=200)
async def razorpay_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_razorpay_signature: str = Header(...)
):
    raw_body = await request.body()
    expected = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, x_razorpay_signature):
        raise HTTPException(403, "Signature mismatch")

    payload = await request.json()
    if payload.get("event") == "order.paid":
        entity = payload["payload"]["payment"]["entity"]
        rzp_order_id = entity.get("order_id")
        rzp_payment_id = entity.get("id")

        updated = await db["orders_ledger"].find_one_and_update(
            {"razorpay_order_id": rzp_order_id},
            {"$set": {
                "current_state": "PAID",
                "razorpay_payment_id": rzp_payment_id,
                "ts_pmt_success": datetime.utcnow()
            }},
            return_document=True
        )
        if updated:
            background_tasks.add_task(_fulfil_order, updated["_id"])

    return {"status": "acknowledged"}

async def _fulfil_order(order_id: str):
    """Re-runs Claude AI report generation for a given order. Marks FULFILLED on success."""
    try:
        order = await db["orders_ledger"].find_one({"_id": order_id})
        if not order:
            return
        # --- insert existing Claude generation call here for order["report_type"] ---
        # On success:
        await db["orders_ledger"].update_one(
            {"_id": order_id},
            {"$set": {"current_state": "FULFILLED", "ts_fulfill_done": datetime.utcnow()}}
        )
    except Exception as e:
        await db["orders_ledger"].update_one(
            {"_id": order_id},
            {"$set": {"error_log": str(e)[:500]}}
        )
```

**Admin force-heal endpoint:**
```python
@app.post("/api/admin/self-heal/force-trigger")
async def force_heal(order_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(_fulfil_order, order_id)
    return {"status": "re-queued", "order_id": order_id}
```

---

### 2D -- APScheduler Jobs (add to existing scheduler in server.py)

```python
# Task 1 -- 00:00 UTC: Evict stale carts (abandoned >48h)
@scheduler.scheduled_job('cron', hour=0, minute=0, id='shc_stale_cart_eviction')
async def evict_stale_carts():
    threshold = datetime.utcnow() - timedelta(hours=48)
    await db["orders_ledger"].delete_many({
        "current_state": {"$in": ["CART_ADD", "CHECKOUT_INIT"]},
        "ts_cart_add": {"$lt": threshold}
    })

# Task 2 -- 02:00 UTC: Self-heal PAID but stuck orders (>30 min unfulfilled)
@scheduler.scheduled_job('cron', hour=2, minute=0, id='shc_stuck_order_heal')
async def heal_stuck_orders():
    threshold = datetime.utcnow() - timedelta(minutes=30)
    cursor = db["orders_ledger"].find({
        "current_state": "PAID",
        "ts_pmt_success": {"$lt": threshold}
    })
    async for order in cursor:
        await _fulfil_order(order["_id"])
```

---

### 2E -- Frontend: Order Funnel Panel (inside DiagnosticsTab)

Add a second section to `DiagnosticsTab.jsx` -- **Lifecycle Ledger** -- below the telemetry event stream.

**Search** by User ID → fetches `GET /api/admin/orders/{userId}` (new endpoint -- return all rows from `orders_ledger` for that user, sorted by `ts_cart_add` desc).

**Per-order card** shows:
- Order ID, Report Type, Amount
- 5-step funnel: Cart Added · Form Filled · Gateway Open · Payment Verified · Claude Fulfilled
  - Each step shows timestamp if reached, "Not Reached" if null
  - Step colour: green if timestamp present, red if it's the stuck step (previous step done, this step null for >15 min)
- **"Force Re-Run"** button visible when `current_state === 'PAID'` and `ts_fulfill_done` is null
  - Calls `POST /api/admin/self-heal/force-trigger` with `order_id`

```python
# New admin endpoint needed:
@app.get("/api/admin/orders/{user_id}")
async def get_user_orders(user_id: str):
    cursor = db["orders_ledger"].find(
        {"user_id": user_id},
        sort=[("ts_cart_add", -1)]
    )
    return await cursor.to_list(50)
```

---

### New Environment Variable

| Variable | Where | Value |
|---|---|---|
| `RAZORPAY_WEBHOOK_SECRET` | Render env | From Razorpay Dashboard → Webhooks → Secret |

Register webhook URL in Razorpay Dashboard:
`https://everydayhoroscope-api.onrender.com/api/webhooks/razorpay`
Events: `order.paid`

---

### SHC-2 Acceptance Checklist

- [ ] `orders_ledger` collection created with all 4 indexes
- [ ] `POST /api/payments/create-order` writes initial ledger row (`CART_ADD` state)
- [ ] `POST /api/diagnostics/order/{razorpay_order_id}/gateway-open` advances state to `GATEWAY_OPEN`
- [ ] `POST /api/webhooks/razorpay` validates HMAC signature, rejects mismatched requests with 403
- [ ] Webhook `order.paid` event advances state to `PAID` and triggers `_fulfil_order` background task
- [ ] `_fulfil_order` advances state to `FULFILLED` on success, writes `error_log` on failure
- [ ] `POST /api/admin/self-heal/force-trigger` re-queues any order by ID
- [ ] APScheduler stale-cart job (`shc_stale_cart_eviction`) registered and firing at 00:00 UTC
- [ ] APScheduler stuck-order job (`shc_stuck_order_heal`) registered and firing at 02:00 UTC
- [ ] Lifecycle Ledger panel visible in DiagnosticsTab with Force Re-Run button
- [ ] Existing `verify_payment()` function unchanged
- [ ] Build: 0 errors

---

## Part 3 (SHC-3) -- GST Ledger + Email Sync

> Complete SHC-2 acceptance before starting SHC-3.

### Objective
Maintain a reconciled GST accounting ledger for all customer invoices (B2C) and supplier bills (B2B). Sync the registered support email for automated vendor invoice ingestion and support ticket triage.

---

### 3A -- New MongoDB Collection: `gst_recon_ledger`

```python
class GSTLedgerEntry(BaseModel):
    id: str = Field(alias="_id")               # INV-2026-XXXX
    ledger_type: str                            # DEBIT_CUSTOMER_B2C | CREDIT_SUPPLIER_B2B
    source_order_id: Optional[str] = None       # links to orders_ledger._id for B2C
    party_name: str
    party_gstin: Optional[str] = None           # mandatory for B2B, optional B2C
    transaction_date: datetime
    taxable_value: float
    cgst: float = 0.0
    sgst: float = 0.0
    igst: float = 0.0
    total_invoice_value: float
    reconciliation_status: str = "PENDING_RECON"  # MATCHED | DISCREPANCY_FOUND | PENDING_RECON
    source_email_id: Optional[str] = None       # message ID if ingested from email
    notes: Optional[str] = None
```

**Index:**
```python
await db["gst_recon_ledger"].create_index(
    [("reconciliation_status", 1), ("transaction_date", -1)],
    name="idx_gst_recon_status"
)
await db["gst_recon_ledger"].create_index(
    [("ledger_type", 1), ("transaction_date", -1)],
    name="idx_gst_type_date"
)
```

---

### 3B -- GST Computation on Payment Success

Hook into `_fulfil_order()` (from SHC-2) -- after state advances to `FULFILLED`, generate the B2C invoice:

```python
async def _create_customer_gst_entry(order: dict):
    """
    CGST+SGST if customer state == business registration state (Maharashtra).
    IGST for all other states.
    Assumes 18% GST on digital services.
    """
    amount = order["amount_paise"] / 100
    taxable = round(amount / 1.18, 2)

    # Placeholder: detect customer state from user profile if available
    customer_state = order.get("customer_state", "OTHER")
    business_state = os.environ.get("BUSINESS_STATE", "Maharashtra")

    if customer_state == business_state:
        cgst = round(taxable * 0.09, 2)
        sgst = round(taxable * 0.09, 2)
        igst = 0.0
    else:
        cgst = sgst = 0.0
        igst = round(taxable * 0.18, 2)

    invoice_id = f"INV-{datetime.utcnow().strftime('%Y%m%d')}-{order['_id'][:6].upper()}"

    await db["gst_recon_ledger"].insert_one({
        "_id": invoice_id,
        "ledger_type": "DEBIT_CUSTOMER_B2C",
        "source_order_id": order["_id"],
        "party_name": order.get("user_email", "Unknown"),
        "transaction_date": datetime.utcnow(),
        "taxable_value": taxable,
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "total_invoice_value": amount,
        "reconciliation_status": "MATCHED"
    })
```

---

### 3C -- Vendor Invoice Parser

```python
# backend/services/gst_parser.py
import pdfplumber
import re

def extract_gst_from_pdf(pdf_bytes: bytes) -> dict:
    """
    Extracts GSTIN and total value from a vendor PDF invoice.
    Returns dict with vendor_gstin and total_value.
    """
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        full_text = "".join([p.extract_text() or "" for p in pdf.pages])

    gstin_pattern = r"\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b"
    amount_pattern = r"(?:Total|Grand Total|Amount Due)[:\s]*₹?\s*([\d,]+\.?\d*)"

    gstin_match = re.search(gstin_pattern, full_text)
    amounts = re.findall(amount_pattern, full_text, re.IGNORECASE)

    return {
        "vendor_gstin": gstin_match.group(0) if gstin_match else None,
        "total_value": float(amounts[-1].replace(",", "")) if amounts else 0.0,
        "raw_text_preview": full_text[:500]
    }
```

Add `pdfplumber` to `requirements.txt`.

---

### 3D -- Gmail API Email Ingestion

**New environment variables:**

| Variable | Where | Value |
|---|---|---|
| `GMAIL_CLIENT_ID` | Render env | Google Cloud OAuth client ID |
| `GMAIL_CLIENT_SECRET` | Render env | Google Cloud OAuth secret |
| `GMAIL_REFRESH_TOKEN` | Render env | OAuth refresh token (store after first auth) |
| `SUPPORT_EMAIL` | Render env | e.g. `support@everydayhoroscope.in` |
| `BUSINESS_STATE` | Render env | `Maharashtra` (or your GST registration state) |

**OAuth setup** (same pattern as existing YouTube OAuth in `server.py`):
- Google Cloud Console → create OAuth 2.0 credential → scopes: `gmail.readonly`
- One-time auth flow at `GET /api/admin/gmail/auth-url` + `GET /api/admin/gmail/callback`
- Store refresh token to `db["app_settings"]` key `gmail_refresh_token` (same pattern as YouTube)

**Ingestion function:**
```python
# backend/services/gmail_ingest.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64

async def fetch_vendor_emails(db) -> list:
    """
    Fetches unread emails with PDF attachments from SUPPORT_EMAIL inbox.
    Returns list of {subject, sender, pdf_bytes, message_id} dicts.
    """
    settings = await db["app_settings"].find_one({"_id": "gmail"})
    if not settings or not settings.get("refresh_token"):
        return []

    creds = Credentials(
        token=None,
        refresh_token=settings["refresh_token"],
        client_id=os.environ.get("GMAIL_CLIENT_ID"),
        client_secret=os.environ.get("GMAIL_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token"
    )
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(
        userId="me", q="is:unread has:attachment filename:pdf"
    ).execute()

    emails = []
    for msg_meta in results.get("messages", [])[:20]:  # cap at 20 per run
        msg = service.users().messages().get(userId="me", id=msg_meta["id"]).execute()
        for part in msg.get("payload", {}).get("parts", []):
            if part.get("filename", "").endswith(".pdf"):
                attachment_id = part["body"]["attachmentId"]
                attachment = service.users().messages().attachments().get(
                    userId="me", messageId=msg_meta["id"], id=attachment_id
                ).execute()
                pdf_bytes = base64.urlsafe_b64decode(attachment["data"])
                emails.append({
                    "message_id": msg_meta["id"],
                    "subject": next((h["value"] for h in msg["payload"]["headers"] if h["name"] == "Subject"), ""),
                    "sender": next((h["value"] for h in msg["payload"]["headers"] if h["name"] == "From"), ""),
                    "pdf_bytes": pdf_bytes
                })
    return emails
```

---

### 3E -- APScheduler Jobs (add to existing scheduler)

```python
# Task 3 -- 04:00 UTC: Ingest vendor email attachments
@scheduler.scheduled_job('cron', hour=4, minute=0, id='shc_vendor_email_ingest')
async def ingest_vendor_emails():
    from backend.services.gmail_ingest import fetch_vendor_emails
    from backend.services.gst_parser import extract_gst_from_pdf
    emails = await fetch_vendor_emails(db)
    for email in emails:
        extracted = extract_gst_from_pdf(email["pdf_bytes"])
        if extracted["total_value"] > 0:
            await db["gst_recon_ledger"].insert_one({
                "_id": f"SUP-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{email['message_id'][:6]}",
                "ledger_type": "CREDIT_SUPPLIER_B2B",
                "party_name": email["sender"],
                "party_gstin": extracted["vendor_gstin"],
                "transaction_date": datetime.utcnow(),
                "taxable_value": round(extracted["total_value"] / 1.18, 2),
                "igst": round(extracted["total_value"] * 0.18 / 1.18, 2),
                "total_invoice_value": extracted["total_value"],
                "reconciliation_status": "PENDING_RECON",
                "source_email_id": email["message_id"],
                "notes": email["subject"]
            })

# Task 4 -- 06:00 UTC: GST ledger daily summary
@scheduler.scheduled_job('cron', hour=6, minute=0, id='shc_gst_daily_summary')
async def generate_gst_summary():
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    pipeline = [
        {"$match": {"transaction_date": {"$gte": today - timedelta(days=1), "$lt": today}}},
        {"$group": {
            "_id": "$ledger_type",
            "total_taxable": {"$sum": "$taxable_value"},
            "total_cgst": {"$sum": "$cgst"},
            "total_sgst": {"$sum": "$sgst"},
            "total_igst": {"$sum": "$igst"},
            "total_invoice": {"$sum": "$total_invoice_value"},
            "count": {"$sum": 1}
        }}
    ]
    summary = await db["gst_recon_ledger"].aggregate(pipeline).to_list(10)
    await db["app_settings"].update_one(
        {"_id": "gst_daily_summary"},
        {"$set": {"last_run": datetime.utcnow(), "summary": summary}},
        upsert=True
    )

# Task 5 -- 08:00 UTC: Support ticket triage
@scheduler.scheduled_job('cron', hour=8, minute=0, id='shc_support_triage')
async def triage_support_tickets():
    """
    Fetches unread support emails, cross-matches sender email to user_diagnostics,
    stores pending tickets in db["support_tickets"] for admin review.
    """
    from backend.services.gmail_ingest import fetch_support_emails  # variant: no attachment filter
    # Implementation: store each unread email as a ticket with matched user_id if found
    pass  # scaffold -- flesh out with Gmail API list call filtered to support label
```

---

### 3F -- Frontend: GST Ledger Panel (inside DiagnosticsTab, third section)

Add a third section to `DiagnosticsTab.jsx` -- **GST Ledger**.

**Tabs within this section:** B2C (Customer Invoices) · B2B (Supplier Bills) · Daily Summary

**B2C tab:**
- Table: Invoice ID · Party (email) · Date · Taxable · CGST · SGST · IGST · Total · Status badge
- Status badge: green MATCHED, amber PENDING_RECON, red DISCREPANCY_FOUND
- Paginated -- 20 rows per page. Fetches `GET /api/admin/gst/ledger?type=DEBIT_CUSTOMER_B2C&page=1`

**B2B tab:**
- Same table + GSTIN column
- Fetches `GET /api/admin/gst/ledger?type=CREDIT_SUPPLIER_B2B&page=1`

**Daily Summary tab:**
- Two stat cards: Total B2C collected (₹) · Total B2B paid (₹)
- CGST / SGST / IGST breakdowns per type
- "Last refreshed" timestamp from `app_settings.gst_daily_summary.last_run`

**New admin endpoints:**
```python
@app.get("/api/admin/gst/ledger")
async def get_gst_ledger(type: str, page: int = 1, page_size: int = 20):
    skip = (page - 1) * page_size
    cursor = db["gst_recon_ledger"].find(
        {"ledger_type": type},
        sort=[("transaction_date", -1)],
        skip=skip,
        limit=page_size
    )
    return await cursor.to_list(page_size)

@app.get("/api/admin/gst/summary")
async def get_gst_summary():
    return await db["app_settings"].find_one({"_id": "gst_daily_summary"}) or {}

@app.patch("/api/admin/gst/ledger/{entry_id}/status")
async def update_recon_status(entry_id: str, status: str):
    allowed = ["MATCHED", "DISCREPANCY_FOUND", "PENDING_RECON"]
    if status not in allowed:
        raise HTTPException(400, f"Status must be one of {allowed}")
    await db["gst_recon_ledger"].update_one(
        {"_id": entry_id},
        {"$set": {"reconciliation_status": status}}
    )
    return {"status": "updated"}
```

---

### SHC-3 Acceptance Checklist

- [ ] `gst_recon_ledger` collection created with correct indexes
- [ ] `_create_customer_gst_entry()` called from `_fulfil_order()` -- B2C row created on every fulfilled order
- [ ] `extract_gst_from_pdf()` correctly extracts GSTIN and total amount from a sample PDF
- [ ] `pdfplumber` added to `requirements.txt`
- [ ] Gmail OAuth flow: `GET /api/admin/gmail/auth-url` and `GET /api/admin/gmail/callback` working (same pattern as YouTube OAuth)
- [ ] APScheduler jobs registered: `shc_vendor_email_ingest` (04:00), `shc_gst_daily_summary` (06:00), `shc_support_triage` (08:00)
- [ ] `GET /api/admin/gst/ledger` returns paginated results filterable by type
- [ ] `GET /api/admin/gst/summary` returns daily totals
- [ ] `PATCH /api/admin/gst/ledger/{id}/status` updates reconciliation status
- [ ] GST Ledger panel visible in DiagnosticsTab with B2C / B2B / Daily Summary tabs
- [ ] Build: 0 errors

---

## File Delivery Checklist (all 3 phases)

```
backend/
  models/diagnostics.py          # TelemetryEvent, UserDiagnosticProfile, RazorpayOrderLedger, GSTLedgerEntry
  services/gst_parser.py         # extract_gst_from_pdf()
  services/gmail_ingest.py       # fetch_vendor_emails(), fetch_support_emails()
  db/indexing.py                 # initialize_diagnostic_indexes() -- called at app startup
  (server.py modified)           # middleware, endpoints, APScheduler jobs, webhook handler

frontend/src/
  diagnostics/telemetry.js       # logEvent, logPageView, logRazorpayOpen
  components/admin/
    DiagnosticsTab.jsx            # Telemetry + Lifecycle Ledger + GST Ledger panels
  (App.js modified)              # wire logPageView on location change
  (AdminDashboard.jsx modified)  # add "Self-Heal" tab importing DiagnosticsTab

requirements.txt                 # add: pdfplumber, google-api-python-client, google-auth-oauthlib
```

---

## New Environment Variables Summary

| Variable | Phase | Purpose |
|---|---|---|
| `RAZORPAY_WEBHOOK_SECRET` | SHC-2 | Webhook HMAC validation |
| `GMAIL_CLIENT_ID` | SHC-3 | Gmail OAuth |
| `GMAIL_CLIENT_SECRET` | SHC-3 | Gmail OAuth |
| `GMAIL_REFRESH_TOKEN` | SHC-3 | Gmail OAuth (stored in DB after first auth) |
| `SUPPORT_EMAIL` | SHC-3 | Inbox to monitor |
| `BUSINESS_STATE` | SHC-3 | GST registration state for CGST/SGST vs IGST split |

All must be set in Render environment before deploying the respective phase.

---

*Commission SHC · 3 phases · Self-Healing Diagnostics Dashboard · EverydayHoroscope*
*Issued: 2026-05-25*
