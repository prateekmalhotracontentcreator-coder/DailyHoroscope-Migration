# Individual Reports — Frontend Commission
# Ready to send to Codex Individual Reports thread

> **Prepared by:** Temple Team — 2 April 2026
> **Copy-paste this message into the Individual Reports Codex thread**

---

---

**Subject: Individual Reports — Phase 1 Backend Confirmed + Frontend Commission**

Temple Team here. Two parts to this message: (1) backend integration confirmation, (2) full frontend commission. Read both before building.

---

## Part 1 — Backend Integration Confirmed

All five Phase 1 routers are live on Render as of commit `dd06ef4`. Render and Vercel are green.

**Confirmed decisions on the 5 divergences from the review note — all accepted for Phase 1:**
- `natal_snapshot` stored on report documents — accepted, useful for QA
- Narrative copy is deterministic and bounded — accepted, tone refinement is Phase 2
- Career Blueprint simplified Dasha heuristics — accepted for Phase 1
- Shadow Self surfaces one primary pressure point — accepted for Phase 1
- Life Cycles simple quality classifier — accepted for Phase 1

No targeted corrections at this time. Phase 2 contract will specify any field-level refinements when issued.

**Thread status on backend:** Complete. No further backend action on Phase 1.

---

## Part 2 — Frontend Commission: Build All Files, One Drop

The 5 reports are live on the API but not accessible to users. There is no frontend UI. This commission covers the complete frontend for all 5 reports. **No Brief Idea step — go straight to build.** The pattern is established (reference: `NumerologyPage.jsx`). Deliver all files in one drop.

Temple integration work will be minimal: copy files to `frontend/src/pages/`, add 2 lines to App.js, add 1 NavBar entry. Everything else Codex builds complete.

---

### Architecture Decision

**Single page: `IndividualReportsPage.jsx`** at route `/reports`

Follow the exact same 4-tab pattern as `NumerologyPage.jsx`:
- **Tab 1 — Select Report:** 5 report cards in a grid, one per report type. Click a card to enter the generate flow for that report.
- **Tab 2 — Generate:** Shared birth details input form + Generate button. Transitions to Tab 3 after successful generation.
- **Tab 3 — Report:** Rendered output of the most recently generated report. Report-type-specific layout (see section below). Share + Save buttons.
- **Tab 4 — History:** All previously generated reports for this user across all 5 types. Click any history item to re-view its output in Tab 3.

URL pattern: `/reports` handles all tabs via internal state. No sub-routes needed. Tab state managed via `useState` — no URL changes between tabs (same as Numerology).

---

### Reference Files (Codex to study — do not import)

- `frontend/src/pages/NumerologyPage.jsx` — overall 4-tab page pattern, form structure, history fetch pattern, auth guard, loading states, toast pattern
- `frontend/src/pages/MyReportsPage.jsx` — existing report history page being extended (see Part 3)
- `frontend/src/pages/BirthChartPage.jsx` — city picker pattern using the 91-city list

---

### Shared Birth Details Input Form (Tab 2)

All 5 reports use the same input form. Build it once as an internal component `BirthInputForm` inside `IndividualReportsPage.jsx`.

Fields:
```
Full Name        — text input (optional, used for personalised output header only)
Date of Birth    — date input (YYYY-MM-DD), required for all reports
Time of Birth    — time input (HH:MM), required for all except Retrograde Survival general mode
City             — searchable dropdown from the 91-city location list (same as Panchang/Numerology)
                   Include city name, timezone abbreviation, country in dropdown rows
                   On city select: auto-populate latitude, longitude, timezone
```

**Retrograde Survival special case:** Add a checkbox "I don't have my birth time" — when checked, hides the time field and city field, and switches to general mode (date-only API call). Label the checkbox: "Generate a general retrograde guide instead (no birth time needed)."

API input shape for all reports (same for all 5):
```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": "Asia/Kolkata",
  "city_name": "New Delhi"
}
```

Retrograde Survival general mode (no birth data):
```json
{
  "check_date": "YYYY-MM-DD"
}
```

---

### API Endpoints

All follow the same pattern:

| Report | Generate | History |
|---|---|---|
| Karmic Debt | `POST /api/reports/karmic-debt/generate` | `GET /api/reports/karmic-debt/history` |
| Career Blueprint | `POST /api/reports/career-blueprint/generate` | `GET /api/reports/career-blueprint/history` |
| Shadow Self | `POST /api/reports/shadow-self/generate` | `GET /api/reports/shadow-self/history` |
| Retrograde Survival | `POST /api/reports/retrograde-survival/generate` | `GET /api/reports/retrograde-survival/history` |
| Life Cycles | `POST /api/reports/life-cycles/generate` | `GET /api/reports/life-cycles/history` |

History endpoints return `{ reports: [...] }`. Each item includes `id`, `report_type`, `generated_at`, and the full output object.

Pass `user_email` via `withCredentials: true` (same auth pattern as Numerology and MyReportsPage).

---

### Tab 1 — Report Selector Grid

5 report cards in a 2-column grid (mobile: 1-column). Each card:
- Icon + accent colour (see config below)
- Report name (bold)
- 1-line commercial hook (see below)
- "Generate" button → sets active report type + switches to Tab 2

**Report card config:**

| Report | Icon (lucide) | Accent | Commercial Hook |
|---|---|---|---|
| Karmic Debt & Past Life | `Infinity` | `text-purple-500` | "Uncover the patterns your soul carries from the past" |
| Career & Success Blueprint | `TrendingUp` | `text-gold` | "Your cosmic career map — purpose, wealth, and peak timing" |
| Shadow Self & Hidden Qualities | `Moon` | `text-blue-500` | "Meet the hidden side of yourself that shapes everything" |
| Retrograde Survival Guide | `RotateCcw` | `text-orange-500` | "Navigate retrograde seasons with clarity, not chaos" |
| Pattern of Life Cycles | `Activity` | `text-green-500` | "Your Dasha blueprint — the chapters your life is written in" |

---

### Tab 3 — Report Output Renderers

Each report type has a distinct output renderer. Build each as a named internal component (`KarmicDebtReport`, `CareerBlueprintReport`, etc.) inside `IndividualReportsPage.jsx`.

**Universal pattern for all reports:**
- Top: Report title + generated date + name (if provided) + city
- Sections rendered as individual `Card` components with gold border and section header
- Remedies section always last — rendered as 3-column grid: Mantra | Gemstone | Ritual
- Bottom: Share button (copy link) + Save confirmation toast

---

#### Karmic Debt & Past Life — Output Renderer

Data path: `report.output`

Section 1 — **Karmic Indicators** (data pills row)
- Retrograde planets at birth → pill per planet (purple badge)
- Saturn house, Rahu house, Ketu house → `H{n}` pill
- Atmakaraka → gold badge with degree
- `debt_activated` → if true, show a red banner: "Karmic Debt Pattern Active"

Section 2 — **Your Karmic Theme** (`report.karmic_theme`)
Section 3 — **Past Life Echo** (`report.past_life_echo`)
Section 4 — **Soul's Deepest Drive** (`report.atmakaraka_insight`)
Section 5 — **Retrograde Lessons** (`report.retrograde_lessons`) — list of `{ planet, lesson }` rendered as small cards
Section 6 — **Breaking the Cycle** (`report.breaking_the_cycle`)
Section 7 — **Remedies** (`report.remedies`)

---

#### Career & Success Blueprint — Output Renderer

Data path: `report.output`

Section 1 — **Career Archetype** (`career_archetype`) — large heading style
Section 2 — **Natural Strengths** (`natural_strengths`)
Section 3 — **Success Formula** (`success_formula`)
Section 4 — **Wealth Signature** (`wealth_signature`)
Section 5 — **Peak Periods** (`peak_periods`) — rendered as a timeline list: planet name + dates + brief description. Gold dot per period.
Section 6 — **Action Guidance** (`action_guidance`) — call-to-action styled card with gold left border
Section 7 — **Remedies** (`remedies`)

---

#### Shadow Self & Hidden Qualities — Output Renderer

Data path: `report.output`

Section 1 — **Your Birth Nakshatra** (`janma_nakshatra`) — large display with Nakshatra name
Section 2 — **Shadow Nakshatra** (`shadow_nakshatra`) — shown as counterpart, slightly dimmed styling
Section 3 — **Hidden Strengths** (`hidden_strengths`) — green accent
Section 4 — **Blind Spots** (`blind_spots`) — amber/caution accent
Section 5 — **Psychological Driver** (`psychological_driver`)
Section 6 — **Integration Path** (`integration_path`) — highlighted card, forward-looking tone
Section 7 — **Remedies** (`remedies`)

---

#### Retrograde Survival Guide — Output Renderer

Data path: `report.output`

Show `mode` badge at top: "Personal Guide" (if personal mode) or "General Guide" (if general mode).

If `active_retrogrades` is empty: show a card "No major retrogrades active for this period — a stable window for moving forward."

For each item in `active_retrogrades`:
- Planet name + retrograde dates (`start_date` → `end_date`) as header
- `life_area` — bold subheader
- `transit_house` — shown as "Transiting your House {n}" pill (only in personal mode)
- `what_to_expect` — paragraph
- `navigation_tips` — bulleted list (✓ styled, green)
- `what_to_avoid` — bulleted list (✗ styled, amber)
- `remedies` — sub-remedies card

---

#### Pattern of Life Cycles — Output Renderer

Data path: `report.output`

Section 1 — **Current Chapter** (`current_chapter`) — large display: Maha Dasha planet + dates + life theme
Section 2 — **Current Sub-Chapter** (`current_sub_chapter`) — Antar Dasha planet + emphasis
Section 3 — **Chapter Quality** (`chapter_quality`) — badge: Expansion (green) / Consolidation (amber) / Challenge (red)
Section 4 — **This Decade Arc** (`this_decade_arc`) — the big-picture narrative, prominent styling
Section 5 — **Upcoming Transitions** (`upcoming_transitions`) — timeline list: date + planet + theme. Max 3 items.
Section 6 — **Remedies** (`remedies`)

---

### Tab 4 — History

Fetch from all 5 history endpoints in parallel (`Promise.all`). Merge and sort by `generated_at` descending.

Each history item card:
- Report type badge (using the same icon + colour config from Tab 1)
- Generated date
- City name (from stored input)
- "View Report" button → loads that report's output into Tab 3 and switches to Tab 3

---

### SEO

Add `<SEO>` component at the top of `IndividualReportsPage.jsx`. Make title and description dynamic based on active report type:

| Active Report | Title | Description |
|---|---|---|
| None selected (default) | `Vedic Astrology Reports — Karmic Debt, Career, Life Cycles \| EverydayHoroscope` | `Free personalised Vedic astrology reports — Karmic Debt, Career Blueprint, Shadow Self, Retrograde Survival, and Life Cycles. Powered by Swiss Ephemeris.` |
| Karmic Debt | `Karmic Debt & Past Life Report — Free Vedic Astrology \| EverydayHoroscope` | `Uncover your karmic patterns — retrograde planets, Saturn and Node placements, Atmakaraka, and soul lessons. Free Vedic report.` |
| Career Blueprint | `Career & Success Blueprint — Vedic Astrology Career Report \| EverydayHoroscope` | `Your cosmic career map — Midheaven sign, 10th house analysis, Dasha peak periods, and wealth signature. Free Vedic report.` |
| Shadow Self | `Shadow Self Report — Vedic Astrology Self-Discovery \| EverydayHoroscope` | `Discover your Janma Nakshatra, shadow counterpart, hidden strengths, and blind spots. Deep self-discovery through Vedic astrology.` |
| Retrograde Survival | `Retrograde Survival Guide — Navigate Mercury & Venus Retrograde \| EverydayHoroscope` | `Personalised retrograde survival guide — active retrogrades, your natal house impact, navigation tips, and rituals.` |
| Life Cycles | `Life Cycles Report — Vimshottari Dasha Timeline \| EverydayHoroscope` | `Your Vimshottari Dasha report — current Maha Dasha, Antar Dasha, decade arc, and upcoming life chapter transitions.` |

Canonical: `https://www.everydayhoroscope.in/reports`

---

## Part 3 — Update `MyReportsPage.jsx`

Deliver an updated `MyReportsPage_v2.jsx` that extends the existing page to include all 5 new individual report types.

**Changes needed:**

**1. Extend `REPORT_CONFIG`** — add 5 new entries:

```js
karmic_debt: {
  icon: Infinity,        // from lucide-react
  color: 'text-purple-500',
  bg: 'bg-purple-500/10',
  border: 'border-purple-500/20',
  label: 'Karmic Debt & Past Life',
  route: '/reports',
},
career_blueprint: {
  icon: TrendingUp,
  color: 'text-gold',
  bg: 'bg-gold/10',
  border: 'border-gold/20',
  label: 'Career & Success Blueprint',
  route: '/reports',
},
shadow_self: {
  icon: Moon,
  color: 'text-blue-500',
  bg: 'bg-blue-500/10',
  border: 'border-blue-500/20',
  label: 'Shadow Self & Hidden Qualities',
  route: '/reports',
},
retrograde_survival: {
  icon: RotateCcw,
  color: 'text-orange-500',
  bg: 'bg-orange-500/10',
  border: 'border-orange-500/20',
  label: 'Retrograde Survival Guide',
  route: '/reports',
},
life_cycles: {
  icon: Activity,
  color: 'text-green-500',
  bg: 'bg-green-500/10',
  border: 'border-green-500/20',
  label: 'Pattern of Life Cycles',
  route: '/reports',
},
```

**2. Change `ReportCard` action for individual report types** — instead of "Download PDF", show a "View Report" button that navigates to `/reports` (the full report page). Individual reports do not have PDF generation in Phase 1.

**3. Update `fetchReports`** — fetch from all 5 new individual report history endpoints in addition to the existing `/api/my-reports`. Merge all results.

**4. Add filter tabs** for new report types — add to the existing filter tab row. Group under "Individual Reports" or add individually, whichever is cleaner with the existing filter UI.

**5. Update `EmptyState` CTA** — add a button: "Individual Reports" → navigates to `/reports`.

**6. Update the "Generate more" CTA** at the bottom — add: "Individual Reports" button → `/reports`.

Deliver as `MyReportsPage_v2.jsx`. Temple will rename and replace the existing file.

---

## Part 4 — App.js and NavBar (Handoff Notes Only)

Do not deliver modified App.js or NavBar files. Instead include in `INDIVIDUAL_REPORTS_FRONTEND_HANDOFF_NOTES.md` the exact code blocks Temple needs to add.

**App.js addition** (one new route):
```jsx
import { IndividualReportsPage } from './pages/IndividualReportsPage';
// Add inside the Routes block:
<Route path="/reports" element={<ProtectedRoute><IndividualReportsPage /></ProtectedRoute>} />
```

**NavBar addition** — provide the exact JSX for the nav item to add to the existing NavBar component. Match the existing NavBar item pattern exactly. Label: "My Reports" or "Reports" — whichever fits the existing NavBar spacing. Icon: `FileText` from lucide-react.

---

## Part 5 — Technical Constraints

| Constraint | Requirement |
|---|---|
| Framework | React 18, React Router v6 |
| Styling | Tailwind CSS — match existing class patterns exactly |
| Components | Use existing `Card`, `Button` from `../components/ui/` |
| Auth | `useAuth()` from `../context/AuthContext` — `user.email` |
| API | `axios` with `withCredentials: true` — same as NumerologyPage |
| Toast | `toast` from `sonner` |
| Icons | `lucide-react` only |
| Backend URL | `const BACKEND_URL = process.env.REACT_APP_BACKEND_URL` |
| No new npm deps | Use only libraries already in the project |
| No Temple source imports | Do not import from any live Temple source file |
| Delivery folder | `codex-deliveries/` |

---

## Files to Deliver

| File | Purpose |
|---|---|
| `IndividualReportsPage.jsx` | Main page — 4 tabs, all 5 report renderers, birth form, history |
| `MyReportsPage_v2.jsx` | Updated MyReportsPage with 5 new report types added |
| `INDIVIDUAL_REPORTS_FRONTEND_HANDOFF_NOTES.md` | App.js route block, NavBar code block, any integration notes |

**One drop. Temple reviews all three files in one pass.**

---

*This commission completes the Individual Reports Phase 1 product. Backend is live. Frontend delivery closes the loop for users.*
