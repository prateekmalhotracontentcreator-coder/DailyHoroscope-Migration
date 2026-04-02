# EverydayHoroscope — New Contract: Notification Engine

> **Issued by:** Temple Team
> **Date:** 2 April 2026
> **To:** CODEX — New Thread
> **Governing reference:** `CODEX_WAYS_OF_WORKING.md` applies in full
> **Scope:** Web-app wide — serves all modules (Panchang, Horoscope, Individual Reports, Love & Engagement, Tarot, Numerology)

---

## 1. Purpose of This Thread

This thread commissions the **EverydayHoroscope Notification Engine** — a unified, modular notification infrastructure that powers delivery of personalised alerts, report-ready pings, auspicious window reminders, and engagement messages across all channels.

**Why a dedicated contract:**
- The existing Admin Console (Temple-built) handles ad-hoc subscriber email via Resend. That is not the same as a scalable, templated, multi-channel notification service.
- Every new module (Love & Engagement, Individual Reports, Panchang) will need to fire notifications — daily forecast drops, report generation complete, encounter window alerts, date-night score reminders. Without a shared engine, this becomes N ad-hoc implementations.
- This contract creates a single Codex-delivered notification service layer. Temple wires all scheduling and lifecycle orchestration.

**Governing decisions from CONTRACT_APPOINTMENT_INDIVIDUAL_REPORTS_AND_KUNDALI.md that apply here:**
- D4: Scheduling, triggers, and lifecycle remain Temple-side (APScheduler). Codex delivers the notification service infrastructure only — not the scheduler.
- D9: Notification logs write to MongoDB via `request.app.state.db`
- D10: Route prefix for notification endpoints: `/api/notifications/`
- D11: Platform/Temple boundary is firm. Codex delivers callable endpoints. Temple calls them.

---

## 2. First Step Required from CODEX

**Before building anything, CODEX must deliver a Brief Idea + Engineering Structure document for this module.**

The document should cover:
1. **Channel-by-channel design** — How each delivery channel (email, WhatsApp, web push, in-app) is implemented: what libraries, what payload structure, what fallback
2. **Template system design** — How notification content is parameterised per module, per report type, and per user segment
3. **Endpoint map** — All proposed `/api/notifications/` endpoints with request/response shapes
4. **MongoDB schema** — Collections, document shapes for preferences, logs, push subscriptions
5. **Proposed additions** — Any notification patterns or features Codex recommends that Temple has not specified
6. **Risk flags** — Channel dependencies (WhatsApp BSP not yet selected), browser push API surface, any concerns

Temple Team will review, give feedback, and confirm the final scope before CODEX builds.

**Document to deliver:** `NOTIFICATION_ENGINE_BRIEF_IDEA_CODEX.md`

---

## 3. Scope: Delivery Channels

### 3.1 Email (Transactional + Marketing)

**Current state:** Resend integration is live in `admin_router.py` (Temple-built). That is an admin send-now flow, not a service-callable template layer.

**What CODEX delivers:**
- `notification_email_service.py` — A callable internal service (not a router) with functions:
  - `send_transactional_email(to, template_id, context)` — single-user, triggered by report events
  - `send_bulk_email(audience_filter, template_id, context)` — list-based, called by Temple scheduler
- Template registry: a Python dict mapping `template_id` → subject + body generator function. All templates inline (no external template service).
- Templates required at launch:
  - `report_ready` — "Your {report_name} is ready to view"
  - `encounter_window_alert` — "Your next encounter window opens {date}"
  - `love_weather_weekly` — "Your 90-day love forecast is in"
  - `daily_panchang_digest` — Subject: today's Tithi + Nakshatra; body: sunrise, key timings, special yoga
  - `date_night_score` — "Tonight's Love Battery: {score}%"
  - `welcome` — Post-registration welcome with feature highlights

**Environment variables (already set on Render):** `RESEND_API_KEY`, `FROM_EMAIL`

---

### 3.2 WhatsApp (Meta Cloud API)

**Current state:** Env vars pending BSP setup (`WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_ACCESS_TOKEN`). Not yet live.

**What CODEX delivers:**
- `notification_whatsapp_service.py` — Callable internal service with:
  - `send_whatsapp_template(to_phone, template_name, template_params)` — sends a pre-approved Meta template message
  - `send_whatsapp_text(to_phone, message)` — plain text within 24-hour session window
- Template names (to be pre-approved with Meta BSP before go-live):
  - `report_ready` — report name + CTA link
  - `panchang_daily` — sunrise time + Tithi + Rahu Kaal
  - `encounter_window` — window open/close alert
  - `love_battery_daily` — daily score + emoji
- Graceful degradation: if `WHATSAPP_PHONE_NUMBER_ID` is not set, service logs a warning and returns without error. Temple will enable when BSP is ready.

---

### 3.3 Web Push (Browser Push Notifications)

**Current state:** Not implemented anywhere. New capability.

**What CODEX delivers:**
- `notification_push_service.py` — Callable internal service using the `pywebpush` library:
  - `send_push(subscription_info, title, body, icon, url)` — sends a Web Push notification to one subscription
  - `send_push_bulk(subscriptions, title, body, icon, url)` — sends to a list (Temple passes list from DB)
- MongoDB collection: `push_subscriptions` — stores VAPID subscription objects per user
- Two API endpoints (these ARE public-facing, not internal-only):
  - `POST /api/notifications/push/subscribe` — stores subscription object + links to user email
  - `DELETE /api/notifications/push/unsubscribe` — removes subscription for the user

**VAPID keys:** CODEX to instruct Temple on how to generate VAPID public/private keys and which env vars to add. Do not hardcode keys.

**Frontend note (Temple-side):** Temple will wire the `navigator.serviceWorker` / `PushManager.subscribe()` frontend flow and the `sw.js` service worker. Codex delivers backend only.

---

### 3.4 In-App Notification Feed

**Current state:** No in-app notification bell or feed exists.

**What CODEX delivers:**
- MongoDB collection: `in_app_notifications` — one document per notification per user
- Document shape:
  ```json
  {
    "id": "uuid",
    "user_email": "string",
    "type": "report_ready | encounter_window | panchang_reminder | love_weather",
    "title": "string",
    "body": "string",
    "action_url": "string (relative)",
    "is_read": false,
    "created_at": "iso-8601-utc"
  }
  ```
- API endpoints:
  - `GET /api/notifications/feed` — returns unread + last 30 days of notifications for authenticated user
  - `PATCH /api/notifications/{notification_id}/read` — marks one notification read
  - `PATCH /api/notifications/read-all` — marks all unread as read
- Internal callable function: `create_in_app_notification(db, user_email, type, title, body, action_url)` — used by other services to push into the feed without going through HTTP

---

## 4. Scope: Notification Triggers (Callable Endpoints)

These are HTTP endpoints that Temple's APScheduler will call on a schedule or event. Codex delivers the endpoints; Temple calls them.

| Endpoint | Trigger | What it does |
|---|---|---|
| `POST /api/notifications/trigger/panchang-daily` | Daily at ~5:30 AM per timezone group | Sends daily Panchang digest to opted-in subscribers (email + WhatsApp) |
| `POST /api/notifications/trigger/encounter-window` | Daily check | Identifies users whose Encounter Window opens today; sends email + push + in-app |
| `POST /api/notifications/trigger/love-weather-weekly` | Every Sunday | Sends weekly Love Weather summary to opted-in users |
| `POST /api/notifications/trigger/date-night-score` | Daily (evening, e.g. 6 PM) | Sends Date-Night Love Battery score to opted-in users |
| `POST /api/notifications/trigger/report-ready` | Event-driven (called immediately after report generation) | Sends cross-channel "your report is ready" notification for any report type |

**Payload for all trigger endpoints:**
```json
{
  "audience": "all | tag:{tag_name} | email:{email}",
  "date": "YYYY-MM-DD (optional, defaults to today)"
}
```

**Auth on trigger endpoints:** Protected by a shared secret header `X-Temple-Trigger-Key` (env var: `TEMPLE_TRIGGER_KEY`). Not exposed to frontend. Temple sets this env var.

---

## 5. Scope: User Notification Preferences

**What CODEX delivers:**
- MongoDB collection: `notification_preferences` — one document per user
- Document shape:
  ```json
  {
    "user_email": "string",
    "channels": {
      "email": true,
      "whatsapp": false,
      "push": true,
      "in_app": true
    },
    "types": {
      "panchang_daily": true,
      "encounter_window": true,
      "love_weather": true,
      "date_night_score": false,
      "report_ready": true
    },
    "whatsapp_phone": "string (E.164 format)",
    "timezone": "Asia/Kolkata",
    "updated_at": "iso-8601-utc"
  }
  ```
- API endpoints:
  - `GET /api/notifications/preferences` — fetch current user's preferences
  - `PUT /api/notifications/preferences` — update preferences (full replace)

---

## 6. Scope: Notification Log

**What CODEX delivers:**
- MongoDB collection: `notification_logs` (may already exist from admin module — CODEX must check if it exists and use the same collection, adding a `source: "notification_engine"` field)
- Log document shape:
  ```json
  {
    "id": "uuid",
    "user_email": "string (null for bulk)",
    "channel": "email | whatsapp | push | in_app",
    "template_id": "string",
    "status": "sent | failed | skipped",
    "error": "string (if failed)",
    "triggered_by": "scheduler | event | manual",
    "sent_at": "iso-8601-utc"
  }
  ```
- `GET /api/notifications/log` — returns last 100 log entries (admin-only, checks `request.state.user.get("role") == "admin"`)

---

## 7. Technical Constraints (All Files in This Module)

Same as all Temple contracts — no exceptions:

| Constraint | Requirement |
|---|---|
| Backend language | Python 3.12 |
| Python boilerplate | `from __future__ import annotations` at top |
| Datetime | `timezone.utc` — never `datetime.UTC` |
| Pydantic | v2 with `ConfigDict` |
| Database | `request.app.state.db` for endpoints; `db` parameter for internal service functions |
| Auth | `request.state.user.get("email")` |
| No Temple imports | No imports from any live Temple source file |
| Delivery folder | `codex-deliveries/` |
| Trigger auth | `X-Temple-Trigger-Key` header (env: `TEMPLE_TRIGGER_KEY`) |
| New dependencies | `pywebpush` for Web Push only. All other channels use existing Resend SDK + Meta HTTPS. No other new deps unless essential. |

---

## 8. Files to Deliver

| File | Type | Purpose |
|---|---|---|
| `notification_email_service.py` | Internal service (no router) | Resend-based email with template registry |
| `notification_whatsapp_service.py` | Internal service (no router) | Meta Cloud API WhatsApp delivery |
| `notification_push_service.py` | Internal service (no router) | pywebpush Web Push delivery |
| `notification_preferences_router.py` | FastAPI router | User preference CRUD — `/api/notifications/preferences` |
| `notification_feed_router.py` | FastAPI router | In-app feed — `/api/notifications/feed` + read endpoints |
| `notification_push_router.py` | FastAPI router | Push subscribe/unsubscribe — `/api/notifications/push/` |
| `notification_trigger_router.py` | FastAPI router | Temple-callable trigger endpoints — `/api/notifications/trigger/` |
| `notification_log_router.py` | FastAPI router | Admin-only log viewer — `/api/notifications/log` |
| `NOTIFICATION_ENGINE_TEMPLE_HANDOFF_NOTES.md` | Doc | Wiring guide for Temple: how to register routers, env vars needed, how to call trigger endpoints from APScheduler |

All files delivered together in one drop to `codex-deliveries/`. Temple reviews all in one pass.

---

## 9. Build Approach

Once Temple Team approves the Brief Idea + Engineering Structure:

- CODEX builds all files as a complete standalone drop
- Do not wait for Temple validation of one file before starting the next — build in parallel
- Internal service files (`notification_*_service.py`) must be importable standalone (no FastAPI app-level dependencies in their function signatures — accept `db` and other dependencies as parameters)
- Each router file registers its own `APIRouter`. Temple wires all routers into `main.py`

---

## 10. Proposed Additions (CODEX to Respond)

CODEX is invited to propose additions to the notification engine that Temple has not specified. Examples of directions Temple is open to:
- Notification batching (avoid sending multiple notifications within a short window to the same user)
- Unsubscribe/opt-out link in emails (CAN-SPAM compliance)
- Notification scheduling preferences per user (e.g., "send panchang digest at 6 AM my time")
- WhatsApp session management (24-hour window tracking)
- Any architectural recommendations Codex identifies from experience with this pattern

Include proposed additions in the Brief Idea document.

---

*This thread is the authoritative contract for the EverydayHoroscope Notification Engine. The governing boundary from D4 and D11 of the Individual Reports contract applies: Temple owns all scheduling and lifecycle. Codex delivers the callable service layer.*
