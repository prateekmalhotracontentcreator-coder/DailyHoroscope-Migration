# Commission IR-3 -- Love & Transit Reports: 8 Public SEO Landing Pages

> EverydayHoroscope · Stack: React 18, Tailwind CSS
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Live app: https://www.everydayhoroscope.in
> Date issued: 2026-05-16

---

## Dependencies

| Commission | Status | Notes |
|---|---|---|
| IR-2 | ✅ Live | Lunar Cycle backend live at `/api/reports/lunar-cycle` |
| IR-2A | 🟠 In progress | Lunar Cycle rework (Action Tracker + richer content) -- IR-3 landing page copy for Lunar Cycle should reflect the richer output described in IR-2A brief |

---

## Context

Phase 1 Individual Reports (5 natal reports) have public SEO landing pages at:
`/karmic-debt-report`, `/career-blueprint-report`, `/shadow-self-report`,
`/retrograde-survival-report`, `/life-cycles-report`

These were built in IR-1 (integrated commit `825a294`). Use them as the **exact structural template** for this commission.

Phase 2 and Phase 3 reports (Love / Transit reports) are live behind auth at `/love-reports` but have **no public landing pages** -- no SEO entry points, no acquisition funnel.

This commission adds 8 public landing pages for the Love module reports.

---

## Reference Files -- Read These Before Writing Anything

```
frontend/src/pages/reports/landing/ReportLandingPageShell.jsx   ← shell component (reuse as-is)
frontend/src/pages/reports/landing/reportLandingContent.jsx     ← Phase 1 content (extend this file)
frontend/src/pages/reports/landing/KarmicDebtLandingPage.jsx    ← pattern reference (thin wrapper)
frontend/src/pages/reports/LoveReportsPage.jsx                  ← existing premium tool hub
frontend/src/App.js                                             ← add 8 routes here
frontend/public/sitemap.xml                                     ← add 8 URLs here
```

**The shell (`ReportLandingPageShell.jsx`) is already built and handles:** SEO tags, JSON-LD, hero section, features grid, blurred sample section, FAQ accordion, CTA button → `/love-reports`.
All you need to provide is content data per report.

---

## What to Build

### Part A -- Content additions to `reportLandingContent.jsx`

Add 8 new content objects to the existing `REPORT_LANDING_CONTENT` map (or equivalent export) following the same shape as the Phase 1 entries.

**Shape reference (from existing file):**
```javascript
{
  slug: "report-slug",
  reportType: "backend_report_type_key",
  heroTitle: "...",
  heroSubtitle: "...",
  eyebrow: "...",
  features: [
    { icon: "✦", title: "...", body: "..." },
    // 4 features
  ],
  sampleLabel: "Sample insight",
  sampleText: "...",   // blurred preview copy
  faq: [
    { q: "...", a: "..." },
    // 3-4 FAQ items
  ],
  seo: {
    title: "...",
    description: "...",
    url: "https://www.everydayhoroscope.in/[slug]",
    jsonLdType: "SoftwareApplication"
  },
  ctaLabel: "Generate My Report",
  ctaPath: "/love-reports"
}
```

---

### The 8 Reports

Write content for each. The tone is warm, premium, Vedic-astrology-grounded, confident (same register as existing landing pages). Keep hero titles punchy (under 8 words). Features are what the report uniquely reveals. FAQ answers 3-4 common questions a first-time visitor would ask.

#### 1. `slug: "encounter-window-report"` · `reportType: "encounter_window"`
**Label:** Encounter Window
**Concept:** 90-day transit forecast showing windows when new meaningful connections are astrologically most likely -- based on Venus/Jupiter/7th lord transits.

#### 2. `slug: "love-weather-report"` · `reportType: "love_weather"`
**Label:** Seasonal Love Weather
**Concept:** 90-day romantic forecast with best dates and caution dates -- Moon/Venus/Mars cycles mapped to emotional weather patterns.

#### 3. `slug: "lunar-cycle-wellness"` · `reportType: "lunar_cycle_wellness"`
**Label:** Lunar Cycle Wellness
**Concept:** Your personal wellbeing rhythm across the 30-day moon cycle -- phase-by-phase guidance on energy, mood, creativity, and rest aligned to your natal Moon.

#### 4. `slug: "date-night-report"` · `reportType: "date_night_score"`
**Label:** Date Night Score
**Concept:** Daily Love Battery score -- which days this month carry the strongest astrological charge for romantic connection and physical closeness.

#### 5. `slug: "intimacy-vitality-report"` · `reportType: "intimacy_vitality_forecast"`
**Label:** Intimacy & Vitality
**Concept:** Mars-Venus window forecast for moments of depth, confidence, and romantic momentum -- mapped to your personal Mars/Venus positions.

#### 6. `slug: "venus-retrograde-report"` · `reportType: "venus_retrograde_personal_impact"`
**Label:** Venus Retrograde Impact
**Concept:** How the current Venus retrograde is reshaping your relationship themes, past connections, and self-worth -- personalised to your natal Venus.

#### 7. `slug: "soulmate-timing-report"` · `reportType: "soulmate_timing"`
**Label:** Soulmate Timing
**Concept:** Jupiter and Dasha windows most aligned for long-term partnership to crystallise -- a timeline, not just a prediction.

#### 8. `slug: "soul-connection-report"` · `reportType: "deep_synastry_soul_connection"`
**Label:** Soul Connection
**Concept:** Karmic and evolutionary patterns in your relationship history -- Rahu/Ketu axis, 12th house, and past-life echoes surfaced from your natal chart.

---

### Part B -- 8 thin wrapper page files

Create in `frontend/src/pages/reports/landing/`:
1. `EncounterWindowLandingPage.jsx`
2. `LoveWeatherLandingPage.jsx`
3. `LunarCycleWellnessLandingPage.jsx`
4. `DateNightLandingPage.jsx`
5. `IntimacyVitalityLandingPage.jsx`
6. `VenusRetrogradeLandingPage.jsx`
7. `SoulmateLandingPage.jsx`
8. `SoulConnectionLandingPage.jsx`

Each is a one-line wrapper passing the slug to the shell. Pattern from existing `KarmicDebtLandingPage.jsx`:
```jsx
import React from "react";
import ReportLandingPageShell from "./ReportLandingPageShell";
import { REPORT_LANDING_CONTENT } from "./reportLandingContent";

export default function EncounterWindowLandingPage() {
  return <ReportLandingPageShell content={REPORT_LANDING_CONTENT["encounter-window-report"]} />;
}
```

---

### Part C -- App.js additions

Add 8 lazy imports and 8 public routes (no `PremiumRoute` wrapper -- these are public acquisition pages).

**Lazy imports** (add near existing landing page imports):
```javascript
const EncounterWindowLandingPage = lazy(() => import('./pages/reports/landing/EncounterWindowLandingPage'));
const LoveWeatherLandingPage = lazy(() => import('./pages/reports/landing/LoveWeatherLandingPage'));
const LunarCycleWellnessLandingPage = lazy(() => import('./pages/reports/landing/LunarCycleWellnessLandingPage'));
const DateNightLandingPage = lazy(() => import('./pages/reports/landing/DateNightLandingPage'));
const IntimacyVitalityLandingPage = lazy(() => import('./pages/reports/landing/IntimacyVitalityLandingPage'));
const VenusRetrogradeLandingPage = lazy(() => import('./pages/reports/landing/VenusRetrogradeLandingPage'));
const SoulmateLandingPage = lazy(() => import('./pages/reports/landing/SoulmateLandingPage'));
const SoulConnectionLandingPage = lazy(() => import('./pages/reports/landing/SoulConnectionLandingPage'));
```

**Routes** (add alongside existing landing page routes):
```jsx
<Route path="/encounter-window-report" element={<EncounterWindowLandingPage />} />
<Route path="/love-weather-report" element={<LoveWeatherLandingPage />} />
<Route path="/lunar-cycle-wellness" element={<LunarCycleWellnessLandingPage />} />
<Route path="/date-night-report" element={<DateNightLandingPage />} />
<Route path="/intimacy-vitality-report" element={<IntimacyVitalityLandingPage />} />
<Route path="/venus-retrograde-report" element={<VenusRetrogradeLandingPage />} />
<Route path="/soulmate-timing-report" element={<SoulmateLandingPage />} />
<Route path="/soul-connection-report" element={<SoulConnectionLandingPage />} />
```

---

### Part D -- `frontend/public/sitemap.xml` additions

Add 8 `<url>` entries in the existing sitemap following the same `<priority>0.7</priority>` pattern used for the Phase 1 landing pages.

---

## Constraints

- **Do NOT modify any backend files** -- this is frontend-only
- **Do NOT modify `LoveReportsPage.jsx`** -- it is the premium tool, not the landing pages
- **Do NOT add a NavBar entry** -- discovery is via SEO and cross-links from `/love` and `/individual-reports` hub
- All 8 landing pages must use the existing `ReportLandingPageShell` -- do not create a new shell
- CTA on all 8 pages goes to `/love-reports` (the premium tool)
- Follow Temple App gold/cream design system exactly -- the shell handles this, just feed correct content

---

## Acceptance Criteria

- [ ] 8 new routes accessible and returning content (verified in browser)
- [ ] No build errors: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` exits 0
- [ ] SEO `<title>` and `<meta description>` unique per page
- [ ] JSON-LD present on each page
- [ ] 8 new URLs in `sitemap.xml`
- [ ] CTA button on each page navigates to `/love-reports`
- [ ] Pages render correctly at 375px (mobile) and 1440px (desktop)
