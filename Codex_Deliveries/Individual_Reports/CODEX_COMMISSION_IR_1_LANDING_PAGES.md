# Commission IR-1 -- Individual Reports: 5 Public Landing Pages

> EverydayHoroscope · Stack: React 18, Tailwind CSS  
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
> Live app: https://www.everydayhoroscope.in  
> Date issued: 2026-05-14

---

## Context

Five Individual Report types are fully built and live behind authentication at `/reports`:
- The report engine (`IndividualReportsPage.jsx`) generates Vedic astrology reports (Karmic Debt, Career Blueprint, Shadow Self, Retrograde Survival, Life Cycles)
- The tool page (`/reports`) is premium-gated and auth-protected

What is missing: **public SEO-optimised landing pages** for each report type. These are acquisition pages -- they appear in Google search, explain the report, and convert visitors to paid users.

**Reference pattern:** Use `TheStrategistLandingPage.jsx` (`frontend/src/pages/strategist/TheStrategistLandingPage.jsx`) as the UX and structural template for all 5 pages.

---

## What to Build

### 5 new page files
Each in `frontend/src/pages/reports/landing/`:
1. `KarmicDebtLandingPage.jsx`
2. `CareerBlueprintLandingPage.jsx`
3. `ShadowSelfLandingPage.jsx`
4. `RetrogradeSurvivalLandingPage.jsx`
5. `LifeCyclesLandingPage.jsx`

### 5 new routes in `App.js`
```jsx
<Route path="/karmic-debt-report"       element={<KarmicDebtLandingPage />} />
<Route path="/career-blueprint-report"  element={<CareerBlueprintLandingPage />} />
<Route path="/shadow-self-report"       element={<ShadowSelfLandingPage />} />
<Route path="/retrograde-survival-report" element={<RetrogradeSurvivalLandingPage />} />
<Route path="/life-cycles-report"       element={<LifeCyclesLandingPage />} />
```

All public (no auth required).

---

## Report Definitions

These come directly from the existing `REPORT_CONFIGS` in `IndividualReportsPage.jsx`:

### 1 -- Karmic Debt & Past Life
- `slug`: `karmic-debt`
- `color`: `#7f4be0` (purple)
- `icon`: `◎`
- `hook`: "Decode the spiritual loop you keep meeting in different disguises."
- `description`: "A premium Vedic reading for karmic themes, past-life echoes, soul lessons, and release practices."
- Route: `/karmic-debt-report`

### 2 -- Career & Success Blueprint
- `slug`: `career-blueprint`
- `color`: `#c9961f` (gold)
- `icon`: `▲`
- `hook`: "See the work pattern, public calling, and success rhythm written into your chart."
- `description`: "A Vedic career reading for strengths, wealth signals, career timing, and practical next moves."
- Route: `/career-blueprint-report`

### 3 -- Shadow Self & Hidden Qualities
- `slug`: `shadow-self`
- `color`: `#3f7ae0` (blue)
- `icon`: `◐`
- `hook`: "Name the hidden pressure shaping your reactions before it chooses for you."
- `description`: "A deep self-knowledge report for hidden strengths, blind spots, emotional drivers, and integration guidance."
- Route: `/shadow-self-report`

### 4 -- Retrograde Survival Guide
- `slug`: `retrograde-survival`
- `color`: `#e27c33` (orange)
- `icon`: `↺`
- `hook`: "Track the retrograde weather around you and move through it with less chaos."
- `description`: "A timing-led guidance report for Mercury, Venus, and Mars retrogrades with clean, grounded remedies."
- Route: `/retrograde-survival-report`

### 5 -- Pattern of Life Cycles
- `slug`: `life-cycles`
- `color`: `#3fa56a` (green)
- `icon`: `◌`
- `hook`: "Understand the chapter you are in now and the one already rising behind it."
- `description`: "A Vimshottari Dasha report for current chapter, sub-cycle, decade arc, and upcoming transitions."
- Route: `/life-cycles-report`

---

## Page Structure (apply to all 5)

Follow `TheStrategistLandingPage.jsx` as structural reference. Each page contains:

### Section 1 -- Hero
- Full-width section, dark background (`bg-background`)
- Large report icon (the `icon` symbol above, displayed in report color, large font)
- `hook` text as hero headline (large, Playfair Display)
- `description` as subtitle
- Two CTAs:
  - Primary: `"Generate My [Report Name]"` → links to `/reports` (auth-gated tool page)
  - Secondary: `"See Sample Report"` → scrolls to sample section below
- Report color used as accent (border, button outline)

### Section 2 -- What This Report Reveals
Three-column grid of GlassCards (`rounded-xl border border-gold/20 bg-gold/[0.04]`), each with:
- Icon (Lucide)
- Feature title
- One-line description

**Per report -- feature cards:**

**Karmic Debt:** "Past Life Patterns" / "Soul Lesson Mapping" / "Release Practices" / "Karmic Planet Analysis" / "Current Life Mirror" / "Action Remedies"

**Career Blueprint:** "10th House Strength" / "Wealth Signal Planets" / "Career Timing Windows" / "Public Role Mapping" / "Skill Activation Periods" / "Next Move Guidance"

**Shadow Self:** "Hidden Strength Planets" / "Blind Spot Analysis" / "Emotional Driver Mapping" / "12th House Secrets" / "Integration Path" / "Shadow-to-Gift Conversion"

**Retrograde Survival:** "Mercury Retrograde Windows" / "Venus Retrograde Impact" / "Mars Retrograde Guidance" / "Do / Avoid Lists" / "Communication Remedies" / "Retrograde Remedies"

**Life Cycles:** "Current Mahadasha" / "Sub-cycle (Antardasha)" / "Decade Arc Overview" / "Upcoming Transitions" / "Peak Windows" / "Chapter Theme"

### Section 3 -- How It Works
Three numbered steps (horizontal on desktop, vertical on mobile):
1. "Enter your birth details" -- date, time, place
2. "Our Vedic engine computes your chart" -- Swiss Ephemeris precision
3. "Receive your personalised report" -- in plain, actionable English

### Section 4 -- Sample Report Preview
A blurred/partially-revealed sample card showing what the report looks like:
- Use the actual report card structure from `IndividualReportsPage.jsx`
- Overlay a gold `"Premium -- Unlock Full Report"` banner
- CTA below: `"Generate My [Report Name]"` → `/reports`

### Section 5 -- FAQ (3 questions per report)

**Karmic Debt:**
- "Is this about past lives literally?" -- Explain Vedic karmic debt as behavioral patterns, not past-life recall
- "Which planets show karmic debt?" -- Saturn, Rahu/Ketu, retrograde planets
- "How do I clear karmic debt?" -- Remedies and conscious action

**Career Blueprint:**
- "What if I'm between careers?" -- The report reads your innate strengths regardless of current role
- "How accurate is career timing?" -- Mahadasha/Antardasha precision, not prediction
- "Does it cover money?" -- Yes: 2nd, 10th, 11th house wealth signals

**Shadow Self:**
- "Is this like a psychological profile?" -- Blends Vedic and Jungian shadow frameworks
- "What is the 12th house shadow?" -- Hidden enemies, self-undoing patterns
- "Can this change?" -- Integration guidance included

**Retrograde Survival:**
- "When is Mercury retrograde in 2026?" -- Provide dates
- "Should I avoid all decisions during retrograde?" -- No -- explain what to avoid and what is fine
- "Does my natal retrograde planet matter?" -- Yes -- explain natal vs transit retrograde

**Life Cycles:**
- "What is a Mahadasha?" -- Explain Vimshottari simply
- "How long does a Mahadasha last?" -- Variable 6-20 years by planet
- "What if I don't know my birth time?" -- Moon-based approximation explained

### Section 6 -- CTA Banner
Full-width gold-accented banner:
- Headline: "Ready to see what [Report Name] reveals for you?"
- Subline: report `hook`
- CTA: `"Generate My [Report Name] →"` → `/reports`

---

## SEO Requirements

Each page must include the `<SEO>` component (`frontend/src/components/SEO.jsx`) with:

| Report | `title` | `description` | `url` |
|---|---|---|---|
| Karmic Debt | `"Karmic Debt Report -- Past Life & Soul Lessons \| Everyday Horoscope"` | `"Decode your karmic patterns with a personalised Vedic Karmic Debt Report. Past-life echoes, soul lessons, and practical remedies."` | `https://www.everydayhoroscope.in/karmic-debt-report` |
| Career Blueprint | `"Career Blueprint Report -- Vedic Career Reading \| Everyday Horoscope"` | `"Discover your Vedic career strengths, wealth signals, and career timing windows with a personalised Career Blueprint Report."` | `https://www.everydayhoroscope.in/career-blueprint-report` |
| Shadow Self | `"Shadow Self Report -- Hidden Strengths & Blind Spots \| Everyday Horoscope"` | `"Name the hidden pressure shaping your reactions. A deep Vedic self-knowledge report for blind spots and integration guidance."` | `https://www.everydayhoroscope.in/shadow-self-report` |
| Retrograde Survival | `"Retrograde Survival Guide -- Mercury, Venus, Mars \| Everyday Horoscope"` | `"Navigate Mercury, Venus and Mars retrograde with your personalised Retrograde Survival Guide. Vedic timing, remedies, do/avoid lists."` | `https://www.everydayhoroscope.in/retrograde-survival-report` |
| Life Cycles | `"Life Cycles Report -- Vimshottari Dasha \| Everyday Horoscope"` | `"Understand the chapter you are in now. A personalised Vimshottari Dasha report for current cycle, transitions, and peak windows."` | `https://www.everydayhoroscope.in/life-cycles-report` |

Also add JSON-LD structured data (`FAQPage` schema) using the FAQ questions from Section 5.

---

## Styling Constraints

- Theme: `bg-background`, `text-foreground`, `text-muted-foreground`, `text-gold`, `border-gold`
- GlassCard: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`
- Each page uses its own report color (see definitions above) ONLY for accents (icons, badges, CTA button border) -- not as background
- Font: Playfair Display for headings, DM Sans for body (already loaded globally)
- No new npm packages

---

## sitemap.xml Update

Add these 5 URLs to `frontend/public/sitemap.xml` with `<changefreq>monthly</changefreq>` and today's date as `<lastmod>`.

---

## Acceptance Criteria

- [ ] All 5 pages built and routed in `App.js`
- [ ] Each page renders all 6 sections (Hero, Features, How it Works, Sample Preview, FAQ, CTA Banner)
- [ ] SEO component with correct title, description, canonical URL on each page
- [ ] FAQPage JSON-LD schema on each page
- [ ] CTAs link correctly to `/reports` (auth-gated tool page)
- [ ] Report color used correctly (accent only, not background)
- [ ] No console errors, no missing imports
- [ ] 5 URLs added to `sitemap.xml`
- [ ] All code committed to `main`
