# Codex Commission: GRW-2 -- Post-Purchase Email Lifecycle Automation
> **Module:** Growth -- Email Automation
> **Issued:** 2026-06-08 | **Priority:** High -- directly impacts subscription conversion
> **Depends on:** Nothing. Resend + APScheduler already live.

---

## 1. What This Builds

A **3-stage post-purchase lifecycle email sequence** that fires automatically after any Razorpay payment verification. No manual admin action needed.

| Stage | Trigger | Goal |
|---|---|---|
| Stage 1 -- Delivery | Immediately on payment | Confirm purchase, deliver access link, set expectations |
| Stage 2 -- Re-engage | 3 days after payment | Deep-link to relevant content, rebuild value perception |
| Stage 3 -- Upsell | 7 days after payment | Convert one-time buyer to Premium subscriber |

---

## 2. Files to Create / Modify

```
backend/lifecycle_email_service.py     ← NEW -- all sequence logic
backend/server.py                      ← Hook into existing verify_payment endpoint
frontend/src/pages/admin/AdminDashboard.jsx  ← New "Lifecycle" sub-tab inside Notifications
```

Do NOT modify: `notification_email_service.py` (call it, never edit it).

---

## 3. New Collection -- `lifecycle_sequences`

```python
{
  "sequence_id":   str,           # uuid
  "user_email":    str,
  "user_name":     str,
  "product_type":  str,           # "report" | "subscription" | "birth_chart" | "kundali_milan" etc.
  "product_name":  str,           # e.g. "Brihat Kundli Pro"
  "payment_id":    str,           # Razorpay order/payment ID
  "started_at":    datetime,
  "stages": {
    "stage_1": {"status": "sent"|"pending"|"failed", "sent_at": datetime|None},
    "stage_2": {"status": "sent"|"pending"|"failed", "scheduled_at": datetime, "sent_at": datetime|None},
    "stage_3": {"status": "sent"|"pending"|"failed", "scheduled_at": datetime, "sent_at": datetime|None},
  },
  "cancelled":     bool,          # admin can cancel a sequence
  "unsubscribed":  bool           # user opted out -- skip remaining stages
}
```

---

## 4. `backend/lifecycle_email_service.py`

### 4a -- `create_sequence(db, user_email, user_name, product_type, product_name, payment_id)`

Creates a `lifecycle_sequences` document. Schedules Stage 2 and Stage 3 as APScheduler jobs with the sequence_id as job ID. Sends Stage 1 immediately via `notification_email_service.send_email()`.

### 4b -- `send_stage(db, sequence_id, stage_number)`

Called by APScheduler for stages 2 and 3.
- Check `lifecycle_sequences` doc: if `cancelled=True` or `unsubscribed=True` → skip, log `skipped`.
- Send email via `notification_email_service.send_email()`.
- Update the stage status to `sent` with timestamp.

### 4c -- Email content per stage

Content is **parameterised** by `product_type`. Use these templates as starting points -- Codex should refine copy to match the EverydayHoroscope temple tone (warm, spiritual, authoritative):

**Stage 1 -- Delivery (immediate)**
```
Subject: Your {product_name} is ready -- {user_name}
Body:
  Your order is confirmed. Here is how to access your {product_name}:
  [Access your report / module] → https://www.everydayhoroscope.in

  What to focus on: [1 sentence personalised to product_type -- see mapping below]

  In alignment,
  The EverydayHoroscope Temple
```

**Stage 2 -- Re-engage (Day 3)**
```
Subject: A deeper read on your {product_name} -- {user_name}
Body:
  Three days ago, you received your {product_name}.
  [Editorial link relevant to product_type -- see mapping below]
  [1 paragraph on what to look for in their chart/report at this point]

  In alignment,
  The EverydayHoroscope Temple
```

**Stage 3 -- Upsell (Day 7)**
```
Subject: What comes after your {product_name} -- {user_name}
Body:
  Your {product_name} gave you a single window into your cosmic blueprint.
  Premium members get the full picture -- unlimited reports, live transits, weekly guidance.

  Upgrade now: https://www.everydayhoroscope.in/pricing

  Current offer: ₹1,599/month · cancel anytime.

  In alignment,
  The EverydayHoroscope Temple
```

**Product type → content mapping** (Codex to fill in sensible editorial links and personalisation):

| product_type | Stage 1 focus line | Stage 2 link | Stage 3 pitch angle |
|---|---|---|---|
| `birth_chart` | "Turn to the Dasha Timeline section first" | `/birth-chart` tool | Unlock Brihat Kundli Pro |
| `brihat_kundli` | "Start with the Yoga analysis -- Section 4" | `/horoscope/monthly` | Unlock Premium monthly guidance |
| `kundali_milan` | "Focus on the Guna Milan score and its remedies" | `/lk-remedies` | Unlock Premium for your partner's full chart |
| `subscription` | "Your Premium access is now live -- explore all modules" | `/the-strategist` | (no upsell -- already subscribed) |
| `numerology` | "Your Life Path number unlocks everything else" | `/numerology` | Unlock Premium for full chart |
| `longevity` | "Start with Chapter 3: the Ayurvedic body type overlay" | `/the-longevity-report` | Unlock Premium |
| `default` | "Log in and explore your dashboard" | `/` | Upgrade to Premium |

### 4d -- APScheduler job registration

```python
# Add to server.py startup (extend existing scheduler):
scheduler.add_job(
    run_lifecycle_stage,
    'date',
    run_date=scheduled_at,
    args=[db, sequence_id, stage_number],
    id=f"lifecycle_{sequence_id}_stage{stage_number}",
    replace_existing=True
)
```

---

## 5. Hook into `verify_payment` -- `server.py`

In the existing `POST /api/payment/verify` handler (around line 1857):

After the payment is confirmed and the subscription/report is created, add:

```python
# Fire lifecycle sequence (non-blocking)
asyncio.create_task(
    lifecycle_email_service.create_sequence(
        db=db,
        user_email=verified_user_email,
        user_name=verified_user_name,
        product_type=order_type,    # derive from the razorpay order metadata
        product_name=order_name,
        payment_id=razorpay_payment_id
    )
)
```

Do NOT await -- fire and forget. If this fails it must not break payment verification.

---

## 6. Admin UI -- Lifecycle Sub-Tab

New sub-tab `lifecycle` inside the Notifications tab. Label: "Lifecycle Sequences".

**View:** A filterable table of all active sequences.

| Column | Value |
|---|---|
| User | Email + name |
| Product | Product name |
| Started | Date |
| Stage 1 | ✅ sent / ⏳ pending / ❌ failed |
| Stage 2 | ✅ sent / ⏳ 3d / ❌ failed |
| Stage 3 | ✅ sent / ⏳ 7d / ❌ failed |
| Actions | [Cancel] |

**Cancel button:** Sets `cancelled=True` in DB. Any pending APScheduler jobs for this sequence are removed. Shows confirmation toast.

**Filter bar:** All · Active · Completed · Cancelled

Fetch from new admin endpoint: `GET /api/admin/lifecycle-sequences?status=all&limit=100`

---

## 7. New Admin Endpoints -- `server.py`

```python
GET  /api/admin/lifecycle-sequences         # list with filter + pagination
POST /api/admin/lifecycle-sequences/{id}/cancel  # set cancelled=True + remove jobs
```

---

## 8. Acceptance Gates (7)

| Gate | Test |
|---|---|
| G-01 | Completing a test Razorpay payment creates a `lifecycle_sequences` document in MongoDB |
| G-02 | Stage 1 email arrives in test inbox within 60 seconds of payment |
| G-03 | Stage 2 APScheduler job is registered with correct `run_date` (now + 3 days) |
| G-04 | Stage 3 APScheduler job is registered with correct `run_date` (now + 7 days) |
| G-05 | Cancelling a sequence via Admin UI sets `cancelled=True` and removes both APScheduler jobs |
| G-06 | `subscription` product_type: Stage 3 email is NOT sent (no upsell to existing subscriber) |
| G-07 | Admin Lifecycle sub-tab loads, shows table, filter works |

---

## 9. Constraints

- Stage 1 send must be non-blocking -- never delay payment confirmation response
- All sends via existing `notification_email_service.py` -- no direct Resend API calls
- `subscription` product_type: skip Stage 3 entirely
- Respect `notification_preferences` opt-out if that collection has an email opt-out for the user
- Commit: `feat(growth): GRW-2 post-purchase lifecycle email automation`
