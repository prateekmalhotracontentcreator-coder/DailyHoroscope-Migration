# Love Module — Frontend + SEO Commission
> Prepared by Temple · 2 April 2026
> Codex thread: Love Bundle

---

## Backend Status (already live on Render)

All 9 Love Bundle routers are registered and deployed. Route summary:

### 8 Report Endpoints (same pattern as Individual Reports)
| Report | POST generate | GET history |
|---|---|---|
| Love Weather | `/api/reports/love-weather/generate` | `/api/reports/love-weather/history` |
| Encounter Window | `/api/reports/encounter-window/generate` | `/api/reports/encounter-window/history` |
| Date Night | `/api/reports/date-night/generate` | `/api/reports/date-night/history` |
| Digital Dating | `/api/reports/digital-dating/generate` | `/api/reports/digital-dating/history` |
| Intimacy & Vitality | `/api/reports/intimacy-vitality/generate` | `/api/reports/intimacy-vitality/history` |
| Venus Retrograde | `/api/reports/venus-retrograde/generate` | `/api/reports/venus-retrograde/history` |
| Soulmate Timing | `/api/reports/soulmate-timing/generate` | `/api/reports/soulmate-timing/history` |
| Soul Connection | `/api/reports/soul-connection/generate` | `/api/reports/soul-connection/history` |

### Ritual Engine Endpoints (subscription product)
| Action | Endpoint |
|---|---|
| Enroll | `POST /api/ritual-engine/enroll` |
| Daily check | `POST /api/ritual-engine/check` |
| Dashboard | `GET /api/ritual-engine/dashboard` |
| History | `GET /api/ritual-engine/history` |
| Unenroll | `DELETE /api/ritual-engine/unenroll` |

All report endpoints and `/api/ritual-engine/dashboard` require auth (`withCredentials: true`).
`/api/ritual-engine/check` is called by APScheduler, not the user directly.

---

## Environment

```
REACT_APP_BACKEND_URL — already set in Vercel
```

All axios calls use `{ withCredentials: true }`.

---

## Pages to Build

### Page 1: LovePage (`/love`) — Public Landing + Report Hub

**Purpose:** Public-facing marketing + report generator entry point. Converts visitors to subscribers. Authenticated users jump straight to generating reports.

**Layout (single scrolling page, no sub-router needed):**

1. **Hero section**
   - Headline: "Your Love Intelligence. Powered by Vedic Astrology."
   - Sub: "Eight precision reports and a live Ritual Engine that tracks your Venus transits, Mars windows, and lunar love score — every single day."
   - CTA buttons: "Explore Reports" (scrolls to report grid) + "Activate Ritual Engine" (scrolls to ritual engine section if logged in, else to login)

2. **Report grid** (8 tiles, 4×2 or 2×4 responsive)
   Each tile shows: icon, report name, one-line description, "Generate" button.
   Clicking "Generate" → navigates to `/love-reports?reportType=<slug>&tab=generate` (protected route).

   Report tile content:
   | slug | label | one-liner |
   |---|---|---|
   | `love-weather` | Love Weather | 90-day romantic forecast with best and caution dates |
   | `encounter-window` | Encounter Window | Upcoming transit windows most likely to spark new meetings |
   | `date-night` | Date Night Planner | Best dates in the next 30 days for a memorable outing |
   | `digital-dating` | Digital Dating Edge | Optimise your profile and message timing with your chart |
   | `intimacy-vitality` | Intimacy & Vitality | Mars–Venus windows for depth and physical connection |
   | `venus-retrograde` | Venus Retrograde | How the current retrograde is affecting your love life |
   | `soulmate-timing` | Soulmate Timing | Jupiter and Dasha windows for long-term partnership |
   | `soul-connection` | Soul Connection | Karmic and evolutionary patterns in your relationships |

3. **Ritual Engine section** (below report grid)
   - Headline: "The Ritual Engine — Your Daily Love Intelligence Feed"
   - Description: "Subscribe once. Every morning the engine evaluates your Venus transits, Mars activations, and Moon–Venus angle against your natal chart. You receive only what is astrologically active for you today."
   - Five trigger cards (compact, visual):
     - 🌹 **First Date Magnet** — Venus within 3° of natal Sun, Ascendant, or 7th lord
     - 🔥 **Steamy Encounter** — Mars trine natal Venus or entering your natal 8th
     - 🌕 **Ex-Recovery Window** — Mercury or Venus retrograde crossing natal 5th/7th
     - 🌿 **Long-Term Love Portal** — Jupiter entering natal 7th or trining Ascendant
     - 💛 **Love Battery Score** — Daily Moon–natal Venus angle (always-on)
   - CTA: "Activate Ritual Engine" → opens enrollment modal if not subscribed, or navigates to `/ritual-engine` if already subscribed

4. **Footer CTA strip**: "Ready to see your Love Weather?" → `/love-reports`

---

### Page 2: LoveReportsPage (`/love-reports`) — Protected

**Purpose:** Generate + view all 8 love reports. Same 4-tab pattern as `IndividualReportsPage.jsx`.

**Tabs:** Select → Generate → Report → History

**Tab 1 — Select:**
- 8 report type cards in a grid (same labels and one-liners as above)
- Each card has a radio-style selection state
- Selected report activates "Continue to Generate" button → moves to Generate tab

**Tab 2 — Generate:**
- Shows selected report name at top
- Birth input form fields:
  - Date of Birth (date picker or text, YYYY-MM-DD)
  - Time of Birth (HH:MM, 24h)
  - City (preset dropdown from 91-city list — copy from existing IndividualReportsPage city picker) + manual lat/lng/timezone fields toggle
  - City Name (text, optional)
- For `love-weather` only: additional "Lookahead Days" field (default 90, range 30–180)
- "Generate Report" button → POST to `/api/reports/<slug>/generate`
- Loading state: "Calculating your {report label}..."
- On success: auto-advance to Report tab + cache full response in localStorage key `love_reports_cache_v1`

**Tab 3 — Report:**
- Renders the `output_payload` from the generate response
- Each report type gets its own output renderer:

  **Love Weather** — `output_payload: { arc_summary, monthly_ratings[], key_dates[], action_guidance, remedies[] }`
  - Arc summary card (prominent)
  - Monthly ratings table (month, average_score as bar, rating badge, theme, best_date, caution_date)
  - Key dates strip (top 5 dates as compact cards with score and theme)
  - Action guidance card
  - Remedies list

  **Encounter Window** — `output_payload: { windows[], summary, action_note }`
  - Summary card
  - Windows list (each: trigger_type, start_date, end_date, intensity badge, description, ritual_suggestion)
  - Action note

  **Date Night** — `output_payload: { best_dates[], summary, ritual_note }`
  - Summary card
  - Best dates grid (date, day_of_week, score, theme, suggested_activity)
  - Ritual note

  **Digital Dating** — `output_payload: { profile_insight, best_times[], message_timing, aura_note, remedies[] }`
  - Profile insight card
  - Best times list (day_of_week or description, quality, reason)
  - Message timing card
  - Aura note + Remedies

  **Intimacy & Vitality** — `output_payload: { phase, windows[], vitality_score, lunar_note, remedies[] }`
  - Phase card (prominent)
  - Vitality score bar
  - Windows list (start_date, end_date, intensity, description)
  - Lunar note + Remedies

  **Venus Retrograde** — `output_payload: { retrograde_active, active_house, personal_impact, shadow_themes[], reframe, remedies[] }`
  - Retrograde status badge (active/dormant)
  - Personal impact card
  - Shadow themes list
  - Reframe card
  - Remedies

  **Soulmate Timing** — `output_payload: { jupiter_window, dasha_summary, readiness_score, composite_note, remedies[] }`
  - Jupiter window card (dates + description)
  - Dasha summary card
  - Readiness score bar
  - Composite note + Remedies

  **Soul Connection** — `output_payload: { karmic_theme, evolutionary_north, relational_pattern, shadow_invitation, integration_path, remedies[] }`
  - All five sections as stacked cards
  - Remedies

**Tab 4 — History:**
- Fetches all 8 history endpoints in parallel: `Promise.all(LOVE_REPORTS.map(r => axios.get(...)))`
- Shows combined list sorted by `created_at` descending
- Each history item: report label badge, date, summary, "View Report" button
- "View Report": checks localStorage cache for full output, if found renders in Report tab; if not, shows summary card with note that full detail requires regeneration on this device

---

### Page 3: RitualEnginePage (`/ritual-engine`) — Protected

**Purpose:** Ritual Engine dashboard for subscribed users + enrollment flow for new users.

**If user has no active subscription** (404 from `/api/ritual-engine/dashboard`):
- Enrollment card:
  - Headline: "Activate Your Ritual Engine"
  - Birth data form (same fields as Generate tab: date, time, lat/lng, timezone, city_name)
  - Trigger selector: 5 checkboxes (all checked by default) matching the 5 trigger types
  - "Activate" button → POST `/api/ritual-engine/enroll` with `{ user_email, natal_data, triggers_opted_in }`
  - On success: show success message + load the dashboard view

**If user is subscribed** (200 from `/api/ritual-engine/dashboard`):

Dashboard layout — 3 zones:

1. **Love Battery card** (top, prominent)
   - Large circular or arc progress indicator showing `love_battery_percent` (0–100)
   - Score category badge (e.g. "Magnetic", "Building", "Quiet", "Reflective")
   - Moon–natal Venus angle (degrees)
   - Alignment description text
   - Action note
   - Today's date + "Updated daily"

2. **Active Triggers section**
   - If `active_triggers` is empty: "No planetary triggers active today — your Love Battery is running on baseline lunar current."
   - For each active trigger:
     - Trigger type badge (colour-coded: pink for first_date_magnet, red for steamy_encounter, purple for ex_recovery, green for long_term_love)
     - Intensity badge (exact / close / wide)
     - Orb degrees
     - Alignment description
     - Ritual suggestion (if present)
     - Active from / until dates

3. **Next Upcoming Trigger** (if present)
   - "Coming next:" card
   - Trigger type + estimated date + description

4. **Recent History** accordion (collapsible)
   - Shows last 7 log entries from `recent_history`
   - Each: date, trigger type, love battery %, alignment description

5. **Manage subscription** link
   - "Unenroll" button (with confirmation prompt) → DELETE `/api/ritual-engine/unenroll`

---

## App.js Additions

Import lines to add:
```jsx
import LovePage from './pages/LovePage';
import LoveReportsPage from './pages/LoveReportsPage';
import RitualEnginePage from './pages/RitualEnginePage';
```

Route lines to add (place with Phase 2 modules):
```jsx
<Route path="/love" element={<LovePage />} />
<Route path="/love-reports" element={<ProtectedRoute><LoveReportsPage /></ProtectedRoute>} />
<Route path="/ritual-engine" element={<ProtectedRoute><RitualEnginePage /></ProtectedRoute>} />
```

Remove or replace existing placeholder:
```jsx
{/* Remove this line: */}
<Route path="/love-report" element={<ComingSoonPage title="Love Report" subtitle="Deep compatibility and relationship analysis" eta="Sprint 3" />} />
```

---

## NavBar Addition

Add after the existing nav items (or in a "Tools" dropdown if NavBar uses one):
```jsx
<Link to="/love" className="navbar-link">Love</Link>
```

---

## MyReportsPage Extension

Add 8 new filter tabs and parallel history fetches to the existing `MyReportsPage.jsx`.

### New constants to add alongside existing `INDIVIDUAL_SLUGS`:
```js
const LOVE_REPORT_SLUGS = [
  { type: 'love_weather',         slug: 'love-weather',       label: 'Love Weather' },
  { type: 'encounter_window',     slug: 'encounter-window',   label: 'Encounter Window' },
  { type: 'date_night',           slug: 'date-night',         label: 'Date Night' },
  { type: 'digital_dating',       slug: 'digital-dating',     label: 'Digital Dating' },
  { type: 'intimacy_vitality',    slug: 'intimacy-vitality',  label: 'Intimacy & Vitality' },
  { type: 'venus_retrograde',     slug: 'venus-retrograde',   label: 'Venus Retrograde' },
  { type: 'soulmate_timing',      slug: 'soulmate-timing',    label: 'Soulmate Timing' },
  { type: 'soul_connection',      slug: 'soul-connection',    label: 'Soul Connection' },
];
```

### fetchReports extension:
Extend the existing `Promise.all` to add 8 more parallel fetches:
```js
...LOVE_REPORT_SLUGS.map(r =>
  axios.get(`${API}/reports/${r.slug}/history`, { withCredentials: true })
    .catch(() => ({ data: { items: [] } }))
),
```

### View Report navigation:
For love reports, navigate to:
```
/love-reports?reportType=<type>&reportId=<id>&tab=report
```

---

## SEO Requirements

### LovePage (`/love`) — public, indexable
```html
<title>Love & Relationship Astrology Reports | Everyday Horoscope</title>
<meta name="description" content="Eight Vedic astrology reports for your love life — Love Weather, Encounter Windows, Soulmate Timing, and more. Plus the daily Ritual Engine love score." />
<link rel="canonical" href="https://www.everydayhoroscope.in/love" />
```
Open Graph:
```html
<meta property="og:title" content="Love Intelligence | Everyday Horoscope" />
<meta property="og:description" content="Daily Vedic love scores, 90-day romantic forecasts, and planetary trigger alerts — all from your natal chart." />
<meta property="og:url" content="https://www.everydayhoroscope.in/love" />
<meta property="og:type" content="website" />
```

JSON-LD (WebPage + ItemList for 8 reports):
```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Love & Relationship Astrology Reports",
  "description": "Vedic astrology love reports and daily Ritual Engine score",
  "url": "https://www.everydayhoroscope.in/love",
  "publisher": {
    "@type": "Organization",
    "name": "Everyday Horoscope",
    "url": "https://www.everydayhoroscope.in"
  }
}
```

### LoveReportsPage (`/love-reports`) — protected, noindex
```html
<title>Love Reports | Everyday Horoscope</title>
<meta name="robots" content="noindex, nofollow" />
```

### RitualEnginePage (`/ritual-engine`) — protected, noindex
```html
<title>Ritual Engine Dashboard | Everyday Horoscope</title>
<meta name="robots" content="noindex, nofollow" />
```

---

## Sitemap

Add to `frontend/public/sitemap.xml`:
```xml
<url>
  <loc>https://www.everydayhoroscope.in/love</loc>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>
```

---

## Styling Convention

Follow the same inline style pattern as `IndividualReportsPage.jsx` and `MyReportsPage_v2.jsx`:
- `radial-gradient` gold/earth background
- `rgba(255,251,245,0.88)` card background with `border-radius: 22px` and `box-shadow: 0 18px 46px rgba(74,50,22,0.09)`
- Gold gradient buttons: `linear-gradient(135deg, #b78646 0%, #d8af6a 100%)`
- Font: `Georgia, Times New Roman, serif` for headings
- No new CSS file — inline style objects only

Love-specific accents:
- Rose/pink for love_weather and first_date_magnet: `rgba(183, 60, 100, 0.12)` backgrounds
- Deep burgundy for steamy_encounter / intimacy triggers: `rgba(139, 30, 60, 0.12)`
- Soft purple for soulmate / soul_connection: `rgba(100, 60, 160, 0.12)`
- Gold (existing) for soulmate timing / venus triggers

---

## localStorage Key

Use `love_reports_cache_v1` for caching full generate responses (same pattern as `individual_reports_full_cache_v1` in IndividualReportsPage).

---

## What NOT to Build

- Do NOT build any admin panel changes
- Do NOT build WebSocket or real-time polling — the Ritual Engine dashboard reads a snapshot
- Do NOT implement payment gating — that is handled by the existing paywall/PricingPage
- Do NOT build any audio/video/NotebookLM integration (D2, deferred to Phase 2)

---

## Files to Deliver

1. `LovePage.jsx` — public landing (`/love`)
2. `LoveReportsPage.jsx` — 4-tab report generator (`/love-reports`)
3. `RitualEnginePage.jsx` — Ritual Engine dashboard + enrollment (`/ritual-engine`)
4. `MyReportsPage_love_patch.jsx` — updated `MyReportsPage.jsx` with 8 new love types added
5. `LOVE_FRONTEND_HANDOFF_NOTES.md` — exact App.js/NavBar diff lines + any notes

Verification: `PYTHONPYCACHEPREFIX=/tmp python3 -m py_compile` is not applicable to JSX. Confirm no missing imports, no undefined variables, no broken destructuring.
