# Codex Commission Brief -- PUN-2: Punya Rewards Home Page + Module Hooks
> Version 1.0 | 2026-05-16 | EverydayHoroscope
> Status: READY TO ISSUE
> Depends on: PUN-1 (INTEGRATED -- all backend endpoints live, PunyaRewardsPage exists)

---

## 1. Context -- What Is Already Built

Do NOT rebuild anything listed here. Read this section before writing a single line of code.

| Asset | Location | Status |
|---|---|---|
| All Punya backend endpoints | `backend/punya_rewards_router.py` | ✅ LIVE |
| `PunyaRewardsPage.jsx` | `frontend/src/pages/rewards/PunyaRewardsPage.jsx` | ✅ LIVE (389 lines) |
| `punyaRewards.js` lib | `frontend/src/lib/punyaRewards.js` | ✅ LIVE |
| Route `/punya-rewards` | `frontend/src/App.js` | ✅ LIVE (ProtectedRoute) |
| Points balance in user dropdown | `frontend/src/components/UserAccountMenu.jsx` | ✅ LIVE (shows `X pts` badge) |

**Key endpoints available (all functional):**
- `GET /api/punya/summary` -- balance, streak, wheel config, daily spin availability
- `GET /api/punya/config/public` -- public wheel config (no auth needed)
- `POST /api/punya/actions/claim` -- award points for an action `{ action_type, reference_id }`
- `POST /api/punya/spin` -- execute spin
- `GET /api/punya/leaderboard` -- weekly top 10

---

## 2. Scope of This Commission

Three deliverables:

### A. Home Page -- Punya Rewards Promotional Section
### B. Module Hooks -- Award Points from Existing Pages
### C. `PunyaRewardsPage.jsx` UX Enhancements

---

## 3A. Home Page Section -- `Landing.jsx`

**File:** `frontend/src/pages/home/Landing.jsx`

Add a dedicated **Punya Rewards promotional section** to the home page. Position: after the existing hero / features section and before the footer CTA. This section must make the gamification layer visible and enticing to logged-in and guest users.

### Section Design Spec

```
┌─────────────────────────────────────────────────────────┐
│  🪙 PUNYA REWARDS                                        │
│  "Earn spiritual merit while you practice"              │
│                                                         │
│  [Spin the Wheel teaser -- static decorative wheel SVG] │
│                                                         │
│  3-column value cards:                                  │
│  ┌──────────────┬──────────────┬──────────────┐        │
│  │ 🌟 Earn      │ 🎡 Spin      │ 🏆 Rise      │        │
│  │ Points daily │ for Rewards  │ Leaderboard  │        │
│  │ from every   │ Premium      │ Top 3 get    │        │
│  │ module you   │ discounts,   │ bonus spins  │        │
│  │ use          │ free reports │ weekly       │        │
│  └──────────────┴──────────────┴──────────────┘        │
│                                                         │
│  For logged-in users:                                   │
│  "You have [X] Punya Points · [Spin Now →]"            │
│                                                         │
│  For guests:                                            │
│  "Sign in to start earning" [Create Free Account →]    │
└─────────────────────────────────────────────────────────┘
```

**Implementation notes:**
- Fetch `GET /api/punya/summary` for logged-in user's balance (show in the section)
- Guest users see static version with CTA to `/login`
- The decorative wheel: static SVG (8 segments, gold gradient, no animation on homepage -- animation lives on `/punya-rewards` only)
- CTA button for logged-in: navigate to `/punya-rewards`
- Use Temple App theme: `bg-gold/[0.04]`, `border-gold/20`, `text-gold`, GlassCard pattern

---

## 3B. Module Hooks -- `POST /api/punya/actions/claim`

Add point-awarding calls to these existing pages. Each call is fire-and-forget (no UI feedback required -- silent background award). Use the existing auth token from `localStorage.getItem('token')`.

**Endpoint:** `POST /api/punya/actions/claim`
```json
{ "action_type": "tarot_daily_draw", "reference_id": "optional-id" }
```

The backend is idempotent per `(user_email, action_type, date)` -- safe to call on every qualifying action without deduplication logic on the frontend.

| File | Action | `action_type` | Trigger point |
|---|---|---|---|
| `frontend/src/pages/tarot/TarotPage.jsx` | Daily card draw | `tarot_daily_draw` | After successful `drawCard()` response |
| `frontend/src/pages/tarot/TarotPage.jsx` | Spread (3+ cards) | `tarot_spread` | After successful spread generation |
| `frontend/src/pages/panchang/PanchangPage.jsx` | Daily panchang view | `panchang_view` | On initial data load for today's tab |
| `frontend/src/pages/horoscope/DailyHoroscope.jsx` | Daily horoscope | `horoscope_daily` | After sign data loads |
| `frontend/src/pages/horoscope/WeeklyHoroscope.jsx` | Weekly horoscope | `horoscope_weekly` | After data loads |
| `frontend/src/pages/horoscope/MonthlyHoroscope.jsx` | Monthly horoscope | `horoscope_monthly` | After data loads |
| `frontend/src/pages/reports/IndividualReportsPage.jsx` | Report generated | `individual_report` | After report generation success |
| `frontend/src/pages/BirthChartPage.jsx` | Birth chart | `birth_chart` | After chart data loads |

**Pattern to use in each file:**
```javascript
// Add this helper (can be a shared util in src/lib/punyaRewards.js if not already there)
async function awardPunyaPoints(actionType, referenceId = null) {
  try {
    const token = localStorage.getItem('token');
    if (!token) return; // Guest users don't earn points
    const API = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
    await fetch(`${API}/api/punya/actions/claim`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ action_type: actionType, reference_id: referenceId }),
    });
  } catch { /* silent fail */ }
}
```

---

## 3C. `PunyaRewardsPage.jsx` Enhancements

**File:** `frontend/src/pages/rewards/PunyaRewardsPage.jsx`

The existing page has the wheel logic, balance display, leaderboard, and spin history. Enhance as follows:

### Spin Wheel Animation -- Upgrade to SVG
Current implementation uses CSS `transform: rotate()`. Replace the wheel visual with a proper SVG wheel:
- 8 equal segments (45° each), rendered as SVG `<path>` elements
- Gold/jewel color palette: alternate deep gold, amber, saffron, ivory per segment
- Label text inside each segment (truncated to fit)
- Center circle with EverydayHoroscope lotus/star logo placeholder
- Spin animation: CSS `@keyframes` with cubic-bezier deceleration (3.5-5 sec)
- Pointer/indicator: gold triangle fixed at top of wheel, outside SVG

### Daily Blessing Countdown
When `daily_free_spin_available = false`, show countdown to next free spin reset (midnight IST). Display as `HH:MM:SS` live timer.

### Streak Display
Show user's current login streak prominently:
```
🔥 7-day streak → +50 Punya Points bonus earned
```

### Points History Tab
The existing ledger exists. Improve the layout:
- Group by date
- Color-code: green for earn (+), amber for spend (-)
- Show `action_type` as a human-readable label (e.g. `tarot_daily_draw` → "Tarot Daily Draw")

---

## 4. Navigation -- CONFIRMED DESIGN

**Do NOT add Punya Rewards to the top NavBar.**
Punya Rewards is accessible from the **User Account Dropdown only** (UserAccountMenu):
- Already live: "Punya Rewards" link with points badge in the dropdown menu
- Route: `/punya-rewards`

This is intentional. The home page section (3A above) serves as the discovery/advertising surface.

---

## 5. Theme & Constraints

- **No NavBar entry for Punya Rewards** (confirmed by Temple Team)
- Follow Temple App theme tokens exactly: `bg-background`, `bg-card`, `text-foreground`, `text-gold`, `border-gold/20`, GlassCard (`rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`)
- No external animation libraries -- CSS/SVG only
- No Redux -- `useState` / `useContext` only
- All module hook calls are **fire-and-forget** -- never block UI or show error to user

---

## 6. Files to Create / Modify

| File | Action |
|---|---|
| `frontend/src/pages/home/Landing.jsx` | MODIFY -- add Punya Rewards promotional section |
| `frontend/src/pages/rewards/PunyaRewardsPage.jsx` | MODIFY -- SVG wheel, countdown, streak display, improved history |
| `frontend/src/lib/punyaRewards.js` | MODIFY -- add `awardPunyaPoints` helper if not already present |
| `frontend/src/pages/tarot/TarotPage.jsx` | MODIFY -- add 2 module hooks |
| `frontend/src/pages/panchang/PanchangPage.jsx` | MODIFY -- add 1 module hook |
| `frontend/src/pages/horoscope/DailyHoroscope.jsx` | MODIFY -- add 1 module hook |
| `frontend/src/pages/horoscope/WeeklyHoroscope.jsx` | MODIFY -- add 1 module hook |
| `frontend/src/pages/horoscope/MonthlyHoroscope.jsx` | MODIFY -- add 1 module hook |
| `frontend/src/pages/reports/IndividualReportsPage.jsx` | MODIFY -- add 1 module hook |
| `frontend/src/pages/BirthChartPage.jsx` | MODIFY -- add 1 module hook |

**Do NOT modify:**
- `backend/punya_rewards_router.py` -- backend is complete
- `frontend/src/components/UserAccountMenu.jsx` -- Punya link already live
- `frontend/src/App.js` -- route already wired

---

## 7. Validation Before Handoff

Before marking complete, verify:
- [ ] Home page Punya section renders for guest + logged-in users
- [ ] Balance shown correctly from `/api/punya/summary`
- [ ] SVG wheel spins to correct segment on `/punya-rewards`
- [ ] Daily free spin countdown shows when spin already used
- [ ] `awardPunyaPoints` called (check network tab) on: tarot draw, panchang view, daily horoscope load
- [ ] No errors in console from silent-fail module hooks
- [ ] Build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` passes with zero errors
