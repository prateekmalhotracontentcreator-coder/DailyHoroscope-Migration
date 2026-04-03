# Notification Engine Temple Handoff Notes

## Delivered Files

- `notification_email_service.py`
- `notification_whatsapp_service.py`
- `notification_push_service.py`
- `notification_preferences_router.py`
- `notification_feed_router.py`
- `notification_push_router.py`
- `notification_trigger_router.py`
- `notification_log_router.py`

## Router Registration

Register these routers in `main.py` or the Temple FastAPI app bootstrap:

```python
from notification_feed_router import router as notification_feed_router
from notification_log_router import router as notification_log_router
from notification_preferences_router import router as notification_preferences_router
from notification_push_router import router as notification_push_router
from notification_trigger_router import router as notification_trigger_router

app.include_router(notification_preferences_router)
app.include_router(notification_feed_router)
app.include_router(notification_push_router)
app.include_router(notification_trigger_router)
app.include_router(notification_log_router)
```

All routers use the `/api/notifications` prefix internally.

## Runtime Assumptions

- Python `3.12`
- `from __future__ import annotations`
- FastAPI
- Pydantic v2
- MongoDB exposed on `request.app.state.db`
- authenticated user available on `request.state.user`
- primary auth email path: `request.state.user.get("email")`

## Collections Used

- `notification_preferences`
- `push_subscriptions`
- `in_app_notifications`
- `notification_logs`
- `subscribers`

Expected audience source:

- `subscribers` documents should include `email` or `user_email`
- tag-based sends use `tags: { $in: [tag_name] }`

If Temple's `subscribers` schema differs, update the small email extraction helper in `notification_trigger_router.py`.

## Environment Variables

Required:

- `TEMPLE_TRIGGER_KEY`
- `RESEND_API_KEY`
- `FROM_EMAIL`
- `VAPID_PUBLIC_KEY`
- `VAPID_PRIVATE_KEY`
- `VAPID_SUBJECT`

Optional until WhatsApp goes live:

- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_ACCESS_TOKEN`

Optional app-state value:

- `request.app.state.frontend_url`

If `frontend_url` is not set, links default to `https://everydayhoroscope.in`.

## VAPID Key Generation

Generate VAPID keys once outside source control, then add them to Render env vars.

Example:

```bash
python -m pywebpush --generate-keys
```

Set:

- `VAPID_PUBLIC_KEY`
- `VAPID_PRIVATE_KEY`
- `VAPID_SUBJECT`

Recommended `VAPID_SUBJECT` value:

```text
mailto:noreply@everydayhoroscope.in
```

## APScheduler Call Examples

Temple owns the schedule itself. The examples below show the intended endpoint calls.

### 1. Panchang Daily

```python
import httpx

await httpx.AsyncClient().post(
    "https://your-app.example.com/api/notifications/trigger/panchang-daily",
    headers={"X-Temple-Trigger-Key": TEMPLE_TRIGGER_KEY},
    json={
        "audience": "all",
        "date": "2026-04-02",
        "tithi": "Shukla Panchami",
        "nakshatra": "Rohini",
        "sunrise": "06:14",
        "special_yoga": "Auspicious yoga active in the morning",
    },
)
```

### 2. Encounter Window

```python
await httpx.AsyncClient().post(
    "https://your-app.example.com/api/notifications/trigger/encounter-window",
    headers={"X-Temple-Trigger-Key": TEMPLE_TRIGGER_KEY},
    json={
        "audience": "tag:encounter-window-today",
        "date": "2026-04-02",
        "summary": "A favorable meeting window is open today.",
        "action_url": "/love/encounters",
    },
)
```

### 3. Love Weather Weekly

```python
await httpx.AsyncClient().post(
    "https://your-app.example.com/api/notifications/trigger/love-weather-weekly",
    headers={"X-Temple-Trigger-Key": TEMPLE_TRIGGER_KEY},
    json={
        "audience": "tag:love-weather-weekly",
        "date": "2026-04-05",
        "summary": "The next 90 days favor clarity, honesty, and patient momentum.",
        "action_url": "/love/weather",
    },
)
```

### 4. Date Night Score

```python
await httpx.AsyncClient().post(
    "https://your-app.example.com/api/notifications/trigger/date-night-score",
    headers={"X-Temple-Trigger-Key": TEMPLE_TRIGGER_KEY},
    json={
        "audience": "tag:date-night-score",
        "date": "2026-04-02",
        "score": 82,
        "summary": "A warm evening for reconnection and ease.",
        "action_url": "/love/date-night-score",
    },
)
```

### 5. Report Ready

```python
await httpx.AsyncClient().post(
    "https://your-app.example.com/api/notifications/trigger/report-ready",
    headers={"X-Temple-Trigger-Key": TEMPLE_TRIGGER_KEY},
    json={
        "audience": "email:user@example.com",
        "date": "2026-04-02",
        "report_id": "abc123",
        "report_name": "Compatibility Report",
        "action_url": "/reports/compatibility/abc123",
    },
)
```

## Trigger Layer Behavior

- audience is resolved from `subscribers`
- preferences are read from `notification_preferences`
- quiet hours are checked using `quiet_hours_start`, `quiet_hours_end`, and `timezone`
- dedupe is enforced against successful `notification_logs` entries
- logs are written in the trigger layer, not in the channel services
- channel services return normalized result objects with `status`, `channel`, and `error`

## WhatsApp Behavior

If `WHATSAPP_PHONE_NUMBER_ID` or `WHATSAPP_ACCESS_TOKEN` is missing:

- WhatsApp sends return `status="skipped"`
- no exception is raised
- other channels continue

## Frontend Responsibilities For Push

Temple owns:

- service worker registration
- `PushManager.subscribe()`
- browser permission UX
- delivery of the subscription payload to `POST /api/notifications/push/subscribe`
- service worker notification click handling

## Recommended Indexes

- `notification_preferences.user_email` unique
- `push_subscriptions.endpoint` unique
- `push_subscriptions.user_email`
- `in_app_notifications.user_email`
- `in_app_notifications.dedupe_key` optional unique
- `notification_logs.created_at`
- `notification_logs.dedupe_key`
- `notification_logs.source`
