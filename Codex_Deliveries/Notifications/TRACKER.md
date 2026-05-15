# Notifications -- Module Tracker
> Path: `Codex_Deliveries/Notifications/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- email live, WhatsApp + Instagram blocked on Temple Team |
| **Backend** | APScheduler + Resend + Meta Cloud API v22.0 |
| **Admin Console** | `/admin/dashboard` → Notifications tab (5 sub-tabs: Subscribers · Compose · Scheduled · History · Social Media) |
| **Email** | ✅ via Resend -- working |
| **WhatsApp** | 🔴 Blocked -- phone `+91 96431 10001` (ID: `1062698816928895`) Pending OTP |
| **Instagram** | 🔴 Blocked -- Business Account ID not loading in Meta dashboard |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| NOTIF-1 | Notification Engine (web-app wide) | ✅ INTEGRATED | `CODEX_COMMISSION_NOTIFICATION_ENGINE.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| NOTIF-OP-1 | **M-5: WhatsApp OTP** -- complete OTP for +91 96431 10001 in WhatsApp Manager + add payment method to WABA on Meta | TT | 🟡 MED | Phone ID: `1062698816928895` · WABA ID: `754513054261096` · Token must be WhatsApp-specific (not FB System User token) |
| NOTIF-OP-2 | **M-6: Instagram Business Account ID** -- not loading in Meta dashboard | TT | 🟡 MED | Required to enable Instagram posting from Admin Console |
| NOTIF-OP-3 | WhatsApp template `everydayhoroscope_update` pending Meta approval | TT | 🟡 MED | Template variables: `{{customer_name}}` + `{{update_content}}` |
| NOTIF-OP-4 | Scheduled daily social posts (6 AM auto-post FB + YT) -- Phase 2 | TT | 🟢 LOW | APScheduler ready. Needs endpoint + Admin Console toggle. Parking lot. |

---

## Architecture Notes

- Email: `RESEND_API_KEY` · `FROM_EMAIL = noreply@everydayhoroscope.in`
- WhatsApp: Meta Cloud API v22.0 · `POST /v22.0/{phone_number_id}/messages`
- Facebook + YouTube: Social Media tab in Admin Console already working
- MongoDB collections: `subscribers` · `scheduled_notifications` · `notification_logs` · `social_post_logs`

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-02 | NOTIF-1 integrated. Email via Resend, APScheduler, subscriber management, notification history. Tracker created. | Codex + CC | -- |
