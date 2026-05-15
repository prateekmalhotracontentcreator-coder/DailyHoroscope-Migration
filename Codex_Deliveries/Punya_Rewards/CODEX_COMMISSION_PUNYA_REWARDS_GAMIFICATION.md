# Codex Commission Brief -- Offers & Gamification ("Punya Rewards")
> Version 1.0 | 25 April 2026 | EverydayHoroscope

---

## 1. Overview

Build a new **Punya Rewards** section in the EverydayHoroscope top navigation bar. This introduces a gamification layer across the entire app -- users earn **Punya Points** by engaging with astrology modules, and can redeem them via a **Spin the Wheel** game for discounts, free premium reports, or daily blessings.

This is a net-new feature spanning frontend (React), backend (FastAPI), and database (MongoDB).

---

## 2. Navigation & Branding

### Top Menu Bar Entry
- Label: **"Punya Rewards"** (with a ✨ or 🪙 icon)
- Route: `/punya-rewards`
- Position: Between existing nav items, after "Horoscope" or before "Admin"
- Visible to: All users (logged-in users see their point balance; guests see a "Sign in to earn" prompt)

### Currency Name
| Term | Meaning |
|---|---|
| **Punya Points** | The gamification currency (पुण्य = spiritual merit in Sanskrit) |
| **Spin** | One spin of the wheel = costs 50 Punya Points |
| **Daily Blessing** | Free daily spin for logged-in users (no cost) |

---

## 3. Point Earning -- Module Hooks

Punya Points are awarded automatically when users complete actions across modules. The backend must expose a central `POST /api/punya/award` endpoint that all modules call.

| Action | Points Awarded | Frequency Cap |
|---|---|---|
| Daily Tarot draw | +10 | Once per day |
| Complete a Tarot spread (3+ cards) | +25 | Once per day |
| Bookmark a Tarot reading | +5 | No cap |
| View daily Panchang | +5 | Once per day |
| Generate Numerology report | +20 | Once per report |
| Generate Birth Chart / Kundali | +30 | Once per chart |
| Daily Horoscope check | +5 | Once per day |
| Weekly Horoscope check | +10 | Once per week |
| Monthly Horoscope check | +15 | Once per month |
| Share a card (WhatsApp/Facebook/etc.) | +10 | 3x per day |
| Refer a friend (future) | +100 | Per verified referral |
| Login streak -- 7 consecutive days | +50 | Once per streak |

---

## 4. Spin the Wheel

### Mechanics
- Wheel has **8 segments**, each representing a prize
- User clicks "Spin" → animated wheel spins → lands on prize → prize is credited to account
- **Free Daily Spin**: every logged-in user gets 1 free spin per day (resets at midnight IST)
- **Bonus Spins**: purchasable with Punya Points (50 points = 1 additional spin)

### Prize Pool (Admin-configurable)
| Segment | Prize | Probability Weight |
|---|---|---|
| 🌟 10% off next premium report | Discount coupon | 20% |
| 🌟 Free Tarot spread | Unlocks one free spread | 15% |
| 🌟 +50 Punya Points | Bonus points | 20% |
| 🌟 Free Numerology report | Unlocks one free report | 10% |
| 🌟 +100 Punya Points | Bonus points | 10% |
| 🌟 20% off subscription | Discount coupon | 8% |
| 🌟 Free Birth Chart PDF | Unlocks one free PDF | 10% |
| 🌟 Try Again Tomorrow | No prize (soft loss) | 7% |

### Probability Engine
- Server-side only -- never client-side (prevents manipulation)
- `POST /api/punya/spin` returns the result; frontend only animates to the pre-determined segment
- Weights are configurable in MongoDB `punya_config` collection

---

## 5. Leaderboard & Streaks

### Daily Leaderboard
- Top 10 users by Punya Points this week
- Displayed on `/punya-rewards` page
- Resets weekly (Monday midnight IST)
- Prize: Top 3 users get bonus spins

### Login Streak Tracker
- Track consecutive daily logins per user
- Streak badge displayed on user profile
- Milestones: 7 days (+50), 30 days (+200), 90 days (+500)

---

## 6. MongoDB Collections

### `punya_points` (per user)
```json
{
  "user_id": "string",
  "total_points": 0,
  "lifetime_earned": 0,
  "lifetime_spent": 0,
  "daily_spin_used": "2026-04-25T00:00:00Z",
  "login_streak": 0,
  "last_login_date": "2026-04-25",
  "updated_at": "ISO timestamp"
}
```

### `punya_transactions` (ledger)
```json
{
  "user_id": "string",
  "type": "earn | spend",
  "amount": 10,
  "reason": "tarot_daily_draw | spin_cost | spin_win | numerology_report | ...",
  "reference_id": "optional -- report_id or spin_id",
  "created_at": "ISO timestamp"
}
```

### `punya_spins` (spin log)
```json
{
  "spin_id": "string",
  "user_id": "string",
  "prize_segment": "10% off next premium report",
  "prize_type": "coupon | points | unlock",
  "prize_value": "PUNYA10",
  "is_free_spin": true,
  "created_at": "ISO timestamp"
}
```

### `punya_config` (admin-controlled)
```json
{
  "wheel_segments": [
    { "label": "10% off report", "prize_type": "coupon", "weight": 20 },
    ...
  ],
  "spin_cost_points": 50,
  "daily_free_spin": true,
  "points_per_action": { "tarot_daily": 10, "panchang_view": 5, ... }
}
```

---

## 7. Backend API Endpoints

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/punya/balance` | Get current user's point balance + streak |
| POST | `/api/punya/award` | Award points for an action (called by other modules) |
| POST | `/api/punya/spin` | Execute a spin (free or paid) |
| GET | `/api/punya/history` | Get user's transaction history (paginated) |
| GET | `/api/punya/leaderboard` | Get weekly top 10 |
| GET | `/api/punya/prizes` | Get available prizes and wheel config |
| GET | `/api/admin/punya/config` | Admin: get wheel config |
| PUT | `/api/admin/punya/config` | Admin: update wheel config |

All endpoints require authentication via `request.state.user` (existing auth middleware).
`POST /api/punya/award` must be idempotent per `(user_id, reason, date)` to prevent double-awarding from retries.

---

## 8. Frontend Pages & Components

### `/punya-rewards` -- Main Page
**Tabs:**
1. **Spin the Wheel** -- animated wheel + daily spin counter + spin button
2. **My Rewards** -- balance, transaction history, active coupons
3. **Leaderboard** -- weekly top 10 with streaks

### Wheel Component (`SpinWheel.jsx`)
- CSS/SVG animated spinning wheel (no external game libraries)
- 8 equal segments with labels and colors
- Spin animation: 3-5 seconds, decelerates naturally
- Server returns target segment index; client animates to it
- Confetti animation on winning segment

### Points Badge (global)
- Small badge in top nav showing current Punya Point balance
- Updates in real-time after earning actions
- Clicking navigates to `/punya-rewards`

### Module Integration
Each module calls `POST /api/punya/award` after the relevant action:
- `TarotPage.jsx` -- after `drawCard()` and `generateSpread()`
- `NumerologyPage.jsx` -- after report generation
- `BirthChartPage.jsx` -- after chart generation
- `DailyHoroscope.jsx`, `WeeklyHoroscope.jsx`, `MonthlyHoroscope.jsx` -- on page view
- `PanchangPage.jsx` -- on daily view

---

## 9. Admin Console Integration

Add a **"Punya Rewards"** tab to the Admin Console (`/admin/dashboard`):
- Sub-tabs: Overview | Wheel Config | User Points | Coupon Codes
- **Overview**: Total points awarded this week, spins today, active users
- **Wheel Config**: Drag to reorder segments, edit labels/prizes/weights, toggle daily free spin
- **User Points**: Search by email, view/adjust balance, view transaction history
- **Coupon Codes**: List of generated coupons, status (claimed/unclaimed), expiry

---

## 10. Tech Stack & Constraints

- **Frontend**: React 18, Tailwind CSS, existing `bg-gold / text-gold / GlassCard` theme tokens
- **Backend**: FastAPI, Python 3.12, Motor (async MongoDB)
- **Database**: MongoDB (Motor async driver) -- existing Atlas cluster
- **Auth**: Use `request.state.user` (existing session middleware) -- do NOT implement new auth
- **No external game SDKs** -- wheel must be pure CSS/SVG/JS animation
- **No Redux** -- use React `useState` / `useContext` only
- **Spin result is server-determined** -- never trust client for prize outcome
- **All monetary values in INR** -- coupons stored as percentage discounts, not absolute amounts
- Follow Temple App theme: `bg-background`, `bg-card`, `text-foreground`, `text-gold`, `border-gold/20`, `GlassCard` pattern

---

## 11. Out of Scope for This Commission
- Actual Razorpay integration for purchasing point packs (use existing paywall)
- Push notifications for streak reminders (APScheduler exists, can be added later)
- Social sharing of prizes
- NFT or blockchain elements
