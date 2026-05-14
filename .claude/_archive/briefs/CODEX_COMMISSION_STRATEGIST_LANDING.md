# Codex Commission Brief -- The Strategist: Premium Landing + War Room Visual Rebuild
> Issued: 2026-05-14 | Priority: P1 -- Flagship Product
> Commission type: New public landing page + Visual rebuild of existing War Room

---

## IMPORTANT CONTEXT -- READ FIRST

The Strategist module has been fully built by the Temple Team (Account 2). All backend routes, API endpoints, state logic, Gate 0 oracle, Conquest Gauge, Scoreboard, Layer badges, and verdict flows are **working and live**.

**Your job is NOT to rebuild the logic. Your job is to make it look and feel like a premium web app** -- the same quality bar as the Longevity Report and KP Standalone pages in this codebase.

Additionally, you will build a new public SEO landing page at `/the-strategist`.

---

## Product Pitch (use this language throughout)

> **"Premium Integrated Vedic Career Mentor"**
> *823 rules. 6 intelligence layers. One war room.*
> *Bloomberg Terminal for Karma -- built for founders, executives, and serious decision-makers.*

---

## 1. Deliverables

### Deliverable A -- New Public Landing Page
**File to create:** `frontend/src/pages/TheStrategistLandingPage.jsx`
**Route:** `/the-strategist`
**Access:** Fully public -- no login required. Google-indexed.

### Deliverable B -- War Room Visual Rebuild
**File to enhance:** `frontend/src/pages/StrategistPage.jsx` (already exists)
**Route:** `/strategist`
**Access:** Premium users only (gate already coded -- do not touch the auth logic)

**Existing file has two components you will enhance:**
- `StrategistLanding` -- the logged-out public view inside StrategistPage (replace with your rebuilt version)
- `Dashboard` -- the logged-in War Room (visual uplift only -- keep ALL logic)

---

## 2. Visual Standard -- This Is Your Bar

Study these files in the Temple App before writing a single line:
```
frontend/src/pages/LongevityReportPage.jsx   ← study this
frontend/src/pages/KrishnaOraclePage.jsx     ← study this
```

**What makes them feel like web apps:**
- Full-bleed animated hero (star fields, gradient overlays, depth)
- Progressive, narrated reveal -- sections appear as user scrolls or completes steps
- State machine feel -- user always knows which step they are on
- Rich data cards with real numbers (not placeholder text)
- Mobile-first -- every panel works perfectly at 375px
- Smooth transitions between states (CSS transitions, not abrupt swaps)
- Gold accents used precisely -- not everywhere, but where they matter

---

## 3. Theme Tokens (mandatory)

```css
bg-background          /* page background */
bg-card                /* card surface */
text-foreground        /* primary text */
text-muted-foreground  /* secondary text */
text-gold / border-gold / bg-gold   /* #c5a059 accent */
```

**GlassCard:**
```jsx
<div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6">
```

**Cyberpunk War Room states (Strategist-specific):**
```
OFFENSIVE_GOLD:     background gold glow, ⚔️ icon active
GOLDEN_HOUR:        animated amber→red pulse, countdown timer prominent
DEFENSIVE_MIDNIGHT: dark navy overlay, 🌙 icon, rituals locked badge
```

Fonts: `font-cinzel` (headings), `font-playfair` (body, italics)

---

## 4. The Complete System (context for Codex)

### 4.1 What The Strategist Is

A **Premium Integrated Vedic Career Mentor** -- a business intelligence war room for founders, executives, and professionals. It integrates three ancient sciences into a single live dashboard:

1. **Krishna Prashnavali** -- Oracle clearance before any strategic mission (Gate 0)
2. **Lal Kitab Diagnostics** -- 5-gate karmic analysis of career, wealth, relationships, and timing
3. **Vedic Birth Chart** -- Live dasha period, transits, Shadbala/Digbala planetary strength

**Knowledge base:** 823 active rules in MongoDB:
- `jyotish_lk_remedies` -- 361 LK remedy records (IDs 308-668)
- `lalkitab_strategist` -- 462 mission/hurdle/surrogate records (IDs 701-1225)

### 4.2 The 6 Layers

```
Layer 0 -- Gate 0: Krishna Prashnavali Oracle
  User asks a business/career question.
  Taps 18×18 grid → one of 36 canonical answers.
  Verdict: YES / WAIT / NO / PRAY
  Determines entry path to War Room.

Layer 1 -- Astrology Engine
  Live birth chart from vedic_calculator.py
  Vimshottari Dasha current period + antardasha
  Command planet + power direction (Digbala)
  Feeds Conquest Probability score

Layer 2 -- Lal Kitab 5-Gate Diagnostic
  Gate 1: Karmic Debt (Pitru Rin -- ancestral obligations)
  Gate 2: Dormant House Awakening (untapped potential)
  Gate 3: 35-Year Planetary Cycle (year-lord phase)
  Gate 4: Mercury Scan (Empty Vessel / Rahu collision)
  Gate 5: Geographical Alignment (Digbala direction)

Layer 3 -- Strategist Engine + Notifications
  Active Missions (transit-triggered from 823 rules)
  Hurdle Alerts (retrograde / eclipse / combustion)
  Surrogate Bridge (missing family census member)
  Golden Hour state machine (sunset timer)
  7 push notification triggers (see Section 4.5)

Layer 4 -- Remedies Action Plan
  Unified 43-day roadmap
  Mission pivot actions + LK remedies merged
  Daily ritual log with streak tracking
  Karmic debt clearance bar (X of 9 debts cleared)

Layer 5 -- Output: Premium Report
  PDF Executive Intelligence Brief (Razorpay-gated)
  Conquest Probability + Gate 0 verdict
  7-Day Tactical Battle Plan
  Karmic Remedy Override (surrogate activation)
  Conquest Timeline (probability curve)
```

### 4.3 Gate 0 Verdict Paths (4 routes -- all coded, just display them better)

```
YES   → War Room unlocked immediately
        Banner: "✅ Path is Clear -- Launch Your Mission"
        All 6 layers active

WAIT  → Pre-Flight Mode
        Remedy plan assigned (LK Gate 1 or standard sequence)
        Banner: "⏳ Pre-Flight Mode -- Day X of 43 → Auto-Unlock"
        LK Tracker CTA prominent
        War Room auto-unlocks when remedy plan completes

NO    → Conquest Score threshold required (60%)
        Banner: "🛑 Conquest Score Required -- 60%+ to re-test"
        Progress bar: current score → 60 threshold
        Remedy browsing CTAs
        Re-test Gate 0 when score qualifies

PRAY  → Full Surrender Mode (score threshold: 75%)
        Banner: "🙏 Full Surrender -- Complete Mantra + Debt Audit → 75%"
        3 modules surfaced: Mantra Remedies + LK Debt Audit + 21-day PRAY protocol
        Purple colour treatment throughout
        Score progress bar to 75%
```

### 4.4 Conquest Probability (0-99%)

```
85-99%  Sovereign Dominance  -- "Expansion / All-In"         (green/gold)
60-84%  Operational Friction -- "Patch & Pivot"               (amber)
40-59%  Strategic Siege      -- "Hold Ground / Remedy"        (orange)
0-39%   Karmic Lockdown      -- "Withdraw / Full Reset"       (red)
```

Inputs to the score:
- Shadbala strength (live from vedic_calculator.py -- float, threshold 1.2)
- Digbala alignment (office direction vs planet power direction)
- Active Pitru Rin flag (from LK Gate 1)
- Surrogate active (adds +12 to score)
- Transit peak (25°-28° = peak window, +5)
- Ritual streak (≥7 days = +10; 0 days = −15)

### 4.5 Golden Hour State Machine

```javascript
// Sunset time from GET /api/panchang/daily
const SUNSET_BUFFER_MINS = 30;

OFFENSIVE_GOLD    = now < sunset − 30min
  → War primary: #FFD700 | Rituals: OPEN | CTA: "Launch Offensive"

GOLDEN_HOUR       = sunset − 30min ≤ now ≤ sunset
  → War primary: #FFC42E→#FF3131 (animated) | Countdown timer | CTA: "ACT NOW"

DEFENSIVE_MIDNIGHT = now > sunset
  → War primary: #000B1E | Rituals: LOCKED | Ritual log button disabled
```

### 4.6 7 Notification Triggers (auto -- no user action needed)

```
strategist-golden-hour     push + in_app    sunset −30 min
strategist-streak-at-risk  push + in_app + whatsapp    sunset −120 min
strategist-streak-broken   push + in_app + email       immediate
strategist-gate0-qualified push + in_app               score hits threshold
strategist-mission-triggered push + in_app             transit match
strategist-debt-cleared    push + in_app + email       Day 43 complete
strategist-wait-unlocked   push + in_app               remedy plan complete
```

### 4.7 Surrogate Bridge

When `lk_user_profiles.family_census[relative] != "living"`:
- User selects: which planet + which relative unavailable + industry
- System queries `lalkitab_strategist` IDs 1201-1225 (Universal Surrogates V2)
- Returns surrogate record with pivot_action
- Activates `surrogate_active = True` → +12 on Conquest Score

---

## 5. Deliverable A -- Public Landing Page (`/the-strategist`)

### 5.1 Positioning

This is the **first thing a Google user sees**. Make it feel like the homepage of a ₹50,000/year SaaS product. Target keywords:
- "Premium Vedic career mentor"
- "Lal Kitab career astrology"
- "Vedic business intelligence"
- "Bloomberg Terminal for Karma"

### 5.2 Page Sections

#### Hero (full-bleed, dark, animated)
- Animated star field background (reuse `StarField` from `Landing.jsx` or build fresh)
- Radial gold glow behind the headline
- Badge: `⚔️ Premium Integrated Vedic Career Mentor`
- Headline (font-cinzel, large): **"The Strategist"**
- Sub-headline (font-playfair): *"Bloomberg Terminal for Karma. 823 Rules. Six Intelligence Layers. One War Room."*
- Body (2 sentences): *"A business intelligence system for founders, executives, and professionals. Your Vedic birth chart powers live missions, strategic timing, and karmic diagnostics -- all in one command centre."*
- CTA (primary, gold): **"Enter the War Room"**
  - If logged in → navigate to `/strategist`
  - If logged out → `navigate('/login', { state: { from: { pathname: '/strategist' } } })`
    ⚠️ Do NOT use `/login?next=` URL query params -- Login.jsx reads `location.state?.from?.pathname` only
- CTA (secondary, outline): **"See How It Works"** → scroll to Section 3

#### Birth Details Teaser Form
- Heading: *"Begin Your Karmic Intelligence Profile"*
- Sub: *"30 seconds. Pre-loaded into your War Room after login."*
- Fields: Name · Date of Birth · Time of Birth · City of Birth
- "I don't know my birth time" toggle (sets `tob_unknown: true`)
- Submit button: **"Start My Intelligence Profile"**
- On submit → save to `localStorage` key `strategist-profile-draft`:
  ```json
  { "name": "", "dob": "", "tob": "", "tob_unknown": false, "city": "", "timestamp": 0 }
  ```
  Then: if logged in → navigate to `/strategist` · if logged out → `navigate('/login', { state: { from: { pathname: '/strategist' } } })`
  Note: new registrations (Register.jsx) always land on `/home` by design -- first-time users set up their LK profile before entering the War Room. Do NOT modify Register.jsx or AuthCallback.jsx.
- Below form: `"Already have an account? Sign in →"` -- link: `navigate('/login', { state: { from: { pathname: '/strategist' } } })`

#### The 6 Layers (How It Works)
- Heading: *"Six Layers of Intelligence. Zero Guesswork."*
- 6 cards in vertical reveal stack. Each card:
  ```
  [Layer badge] [Layer name]
  [2-sentence description]
  ```
  Use Layer 0-5 from Section 4.2 above.
  - Layer 0: gold border, "The Oracle Gate" -- *"Ask Krishna before any campaign. YES unlocks the War Room. WAIT triggers a remedy sequence. NO or PRAY activates specific recovery protocols."*
  - Layer 5: "Premium" badge, CTA link to report

#### War Room States (3-state visual)
- Heading: *"The War Room Never Sleeps"*
- 3 side-by-side tiles:
  ```
  ⚔️ OFFENSIVE           🌅 GOLDEN HOUR          🌙 DEFENSIVE
  Rituals Open           Act Now -- 30min window   Rituals Locked
  #FFD700 glow           #FFC42E→#FF3131 pulse    #000B1E bg
  ```
- Sub: *"The War Room state changes with sunset. Golden Hour is your 30-minute execution window."*

#### Conquest Probability (4-tier)
- Heading: *"Your Conquest Score. Recalculated Daily."*
- 4 tier tiles:
  ```
  85-99% Sovereign Dominance    60-84% Operational Friction
  40-59% Strategic Siege        0-39%  Karmic Lockdown
  ```
- Sub: *"Computed from Shadbala strength, Digbala alignment, Karmic Debt, transit peak, and ritual streak."*

#### Gate 0 Paths (4 outcomes)
- Heading: *"Gate 0 -- Ask Krishna Before You Act"*
- 4 outcome tiles:
  ```
  ✅ YES → War Room unlocked    ⏳ WAIT → Pre-Flight remedy plan
  🛑 NO  → Score to 60%         🙏 PRAY → Full Surrender path
  ```
- Sub: *"The 18×18 Krishna Prashnavali grid. One tap. Divine direction."*

#### The 823 Rules (data credibility)
- Heading: *"823 Rules. Mapped to Your Chart."*
- 3 stat tiles: `361` LK Remedy Rules · `462` Strategist Mission Rules · `43` Days per Cycle
- Brief paragraph on the knowledge base

#### Final CTA (gold glow)
- *"Your Karmic War Room is ready."*
- Gold button: **"Enter the War Room →"**
- `"Free account · Premium access from ₹1,599/month"`

### 5.3 SEO (mandatory)

```jsx
<SEO
  title="The Strategist -- Premium Vedic Career Mentor | War Room"
  description="Bloomberg Terminal for Karma. 823 Lal Kitab rules, Krishna Prashnavali oracle, and live Vedic birth chart intelligence -- all in one war room for founders and executives."
  url="https://www.everydayhoroscope.in/the-strategist"
  schema={schema}
/>
```

JSON-LD `schema` prop:
```javascript
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": "https://www.everydayhoroscope.in/the-strategist#webpage",
      "name": "The Strategist -- Premium Integrated Vedic Career Mentor",
      "description": "Bloomberg Terminal for Karma. 823 Lal Kitab rules, Krishna Prashnavali Gate 0 oracle, Conquest Probability scoring, transit-triggered missions, and 43-day remedy roadmap.",
      "url": "https://www.everydayhoroscope.in/the-strategist",
      "isPartOf": { "@id": "https://www.everydayhoroscope.in/#website" },
      "publisher": { "@id": "https://www.everydayhoroscope.in/#organization" },
      "breadcrumb": {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.everydayhoroscope.in" },
          { "@type": "ListItem", "position": 2, "name": "The Strategist", "item": "https://www.everydayhoroscope.in/the-strategist" }
        ]
      }
    },
    {
      "@type": "Service",
      "@id": "https://www.everydayhoroscope.in/the-strategist#service",
      "name": "The Strategist -- Premium Integrated Vedic Career Mentor",
      "description": "Premium career and business intelligence combining Lal Kitab diagnostics, Krishna Prashnavali oracle, and Vedic birth chart analysis into a live war room with 823 rules, Conquest Probability scoring, and 43-day remedy protocols.",
      "provider": { "@id": "https://www.everydayhoroscope.in/#organization" },
      "serviceType": "Vedic Astrology Career Consulting",
      "areaServed": "IN",
      "offers": {
        "@type": "Offer",
        "price": "1599",
        "priceCurrency": "INR",
        "description": "Premium Monthly subscription"
      }
    }
  ]
}
```

---

## 6. Deliverable B -- War Room Visual Rebuild (`/strategist`)

### 6.1 What Already Exists (working -- keep all logic)

The existing `StrategistPage.jsx` has these fully working components:
- `WarRoomStateProvider` / `useWarRoom` -- Golden Hour state machine ✅
- `ConquestGauge` -- Conquest Probability display ✅
- `HurdleAlert` -- Hurdle alert component ✅ imported but not currently rendered -- **add it to the Dashboard render output** (see Section 6.3)
- `KrishnaOracleGrid` -- 18×18 Gate 0 grid ✅
- `Gate0Panel` -- Oracle consultation panel ✅
- `VerdictBanner` -- YES/WAIT/NO/PRAY verdict display ✅
- `PraySurrenderPanel` -- Full Surrender mode ✅
- `PreFlightPanel` -- WAIT/NO blocked states ✅
- `Scoreboard` -- Conquest Score + streak + karmic debt ✅
- `OnboardingRequired` -- 3-step setup prompt ✅
- `AstrologyStrip` -- Command planet, Dasha, power direction ✅
- `LKGateStatus` -- 5-gate summary ✅
- `MissionQuickLinks` -- Mission board + tracker links ✅
- `Dashboard` -- Main orchestrator ✅
- `StrategistLanding` -- Logged-out public view (REPLACE with premium quality) ✅

### 6.2 What StrategistLanding Needs (Replace Existing)

The existing `StrategistLanding` inside `StrategistPage.jsx` is functional but visually basic. **Replace it** with a premium web-app quality version matching your `TheStrategistLandingPage.jsx` design language -- but simpler (this is the logged-out view inside the existing route, not the full public landing).

Keep the existing JSX structure, just make it visually on par with Longevity/KP.

### 6.3 Visual Uplift for Dashboard -- Specific Requirements

**War Room Header (upgrade):**
- Full-width banner, not a small rounded card
- Background fills the full header area with state colour:
  ```
  OFFENSIVE_GOLD:     bg gradient → from-gold/20 to-transparent
  GOLDEN_HOUR:        bg gradient → from-orange-500/30 to-red-500/20, animated pulse
  DEFENSIVE_MIDNIGHT: bg-slate-950 with moon icon
  ```
- State label large and centred: `⚔️ OFFENSIVE -- RITUALS OPEN`
- Golden Hour countdown timer: large mono font, prominent, not a small badge

**Module Intro Screen (add -- NEW):**
Show this ONCE when user arrives and has no active Gate 0 verdict:
```
Welcome back, [Name] -- Your War Room is Active
[Birth date] · [Command Planet] · [Current Dasha]
"Your Mission Begins"
[Animated layer badges appearing one by one, 200ms stagger]
CTA: "Consult the Oracle" → scrolls to Gate 0 panel
```
Read `[Name]` from:
1. `localStorage.getItem('strategist-profile-draft')` → `draft.name`
2. Fallback: `user.name` from auth context

**Conquest Gauge (upgrade):**
- Larger -- min 200px diameter or equivalent
- Score number: large, bold, centre of gauge
- 4-tier label BELOW score in matching colour
- Factors breakdown: expandable "How is this calculated?" panel

**Layer Strip (upgrade):**
- Sticky at top of page on scroll
- Active layer: gold background pill
- Locked layers: dimmed with 🔒 icon
- Complete layers: emerald with ✓ icon
- Clicking a badge smooth-scrolls to that panel

**Section dividers:**
- Each layer (L0-L5) clearly demarcated with a divider + layer badge
- User can see all 6 layers on the page -- not collapsed

**Scoreboard (upgrade):**
- Conquest Score: large number, not small
- Progress bar: full width, labelled clearly
- Karmic Debt status: pill badge -- "Cleared ✓" (emerald) or "Active ⚠" (amber)
- Gate 0 last verdict: colour-matched pill (YES=green, WAIT=orange, NO=red, PRAY=purple)
- Streak days: large number with streak fire emoji for 7+ days

**Hurdle Alerts (add -- currently imported but NOT rendered):**
- `HurdleAlert` is imported in `StrategistPage.jsx` line 8 but never placed in the JSX
- Place it in Dashboard between `LKGateStatus` and `MissionQuickLinks`
- Style: amber/red card, full width, visible only when active hurdle alerts exist
- Label: "⚠️ Active Hurdles -- [count]" as section header
- This is Layer 3 (Strategist Engine / Hurdle Alerts)

**Mission Quick Links (upgrade):**
- Mission count: large number tile
- Streak days: large number tile
- Navigation links: full-width cards with icon + label + arrow, not small buttons

**Mobile requirements:**
- All panels stack full width
- Golden Hour countdown: fixed bottom bar during GOLDEN HOUR state
- Sticky layer strip collapses to icons-only on mobile

### 6.4 localStorage Integration

On mount, read:
```javascript
const draft = JSON.parse(localStorage.getItem('strategist-profile-draft') || 'null');
const sevenDays = 7 * 24 * 60 * 60 * 1000;
const isValid = draft && (Date.now() - draft.timestamp) < sevenDays;
const userName = isValid ? draft.name : user?.name || 'Commander';
```
Use `userName` in the welcome message. Clear the draft after it's been consumed (after first successful War Room load).

---

## 7. Complete User Flow (wire this correctly)

```
GOOGLE → "Premium Integrated Vedic Career Mentor"
             │
             ▼
/the-strategist  [Codex builds -- new file]
  Full-bleed hero · 6-layer overview · Birth details form · War Room states
  · Conquest tiers · Gate 0 paths · CTA
             │ "Enter the War Room" clicked
             ▼
        Logged out? → /login?next=/strategist → /register
        Logged in?  → /strategist directly
             │
             ▼
/strategist  [Account 2 built -- Codex visually rebuilds]
  Premium gate → upgrade prompt for free users
  For premium users:
    ↓
  Module Intro Screen
    "Welcome, [Name] -- Your Mission Begins"
    Animated layer badge reveal
    "Consult the Oracle" CTA
    ↓
  Gate 0: Krishna Prashnavali (18×18 grid)
    ↓
  YES verdict:                   WAIT verdict:
    War Room unlocked              Pre-Flight Mode
    All layers active              Remedy plan assigned
    ↓                              LK Tracker CTA
  NO verdict:                    PRAY verdict:
    Score → 60% required           Full Surrender
    Progress bar                   Mantra + Debt Audit
    Re-test CTA                    Score → 75%
    ↓
  Full War Room Dashboard (Layer 1-5)
    Astrology Strip (command planet, dasha, power direction)
    LK 5-Gate Status (all 5 gates)
    Conquest Gauge (score + tier + factors)
    Mission Quick Links (active count, streak)
    Scoreboard (progress bar, debt cleared, last verdict)
    ↓
  /strategist/missions    → Full Mission Board
  /strategist/surrogate   → Surrogate Bridge (missing family member)
  /strategist/action-plan → 43-Day Roadmap
  /strategist/report      → Executive Intelligence Brief (Premium PDF)

  Background: 7 push notifications auto-fire at the right moments
    🌅 Golden Hour alert (sunset −30 min)
    ⚠️  Streak-at-risk  (sunset −120 min)
    💔  Streak broken (immediate)
    ✅  Gate 0 qualified (score hits threshold)
    ⚔️  Mission triggered (transit match)
    🏆  Debt cleared (Day 43)
    🔓  WAIT unlocked (remedy plan complete)
```

---

## 8. API Endpoints (all live)

```javascript
const BACKEND = process.env.REACT_APP_BACKEND_URL;
// ALL calls must include: credentials: 'include'

// War Room
GET  /api/strategist/dashboard           // full war room state
GET  /api/strategist/gate0/status        // { status, conquest_score, last_verdict }
POST /api/strategist/gate0/select        // { row, col } → verdict + reading
POST /api/strategist/missions            // active missions list
POST /api/strategist/hurdles             // active hurdle alerts
POST /api/strategist/probability         // Conquest Probability score + factors
POST /api/strategist/surrogate           // { planet, relative_unavailable, industry }
GET  /api/strategist/report/pdf          // Premium Executive Intelligence Brief
GET  /api/strategist/surrender-context   // PRAY mode -- mantra + gate1 narrative + steps

// Gate 0 oracle
GET  /api/oracle/krishna-prashnavali/meta  // 18×18 grid matrix

// Panchang (for Golden Hour sunset)
GET  /api/panchang/daily?date=YYYY-MM-DD&location_slug=xxx

// LK Profile (for birth data pre-fill)
GET  /api/lk/profile                     // existing LK onboard data
```

---

## 9. Files to Create / Modify

### Create:
```
frontend/src/pages/TheStrategistLandingPage.jsx   ← Deliverable A
```

### Modify:
```
frontend/src/pages/StrategistPage.jsx   ← Deliverable B (visual rebuild)
frontend/src/App.js                     ← add /the-strategist route
frontend/public/sitemap.xml             ← add /the-strategist URL + REMOVE /strategist entry
```

### SEO Deduplication (mandatory -- do alongside sitemap change):
Once `/the-strategist` is the canonical public landing, `/strategist` (logged-out view) must stop being indexed:
1. In `StrategistLanding` (inside `StrategistPage.jsx`, line ~653): add `noindex={true}` to the `<SEO>` component
2. In `sitemap.xml`: **remove** the `/strategist` entry (currently line 54)
3. In `sitemap.xml`: **add** the `/the-strategist` entry at priority 0.95

This prevents Google from seeing two indexable pages with similar Strategist content.

### Do NOT touch:
```
frontend/src/components/WarRoomStateProvider.jsx   ← logic -- leave as-is
frontend/src/components/ConquestGauge.jsx          ← leave as-is
frontend/src/components/HurdleAlert.jsx            ← leave as-is
frontend/src/components/KrishnaOracleGrid.jsx      ← leave as-is
frontend/src/pages/StrategistMissionsPage.jsx      ← leave as-is
frontend/src/pages/StrategistReportPage.jsx        ← leave as-is
frontend/src/pages/StrategistSurrogatePage.jsx     ← leave as-is
frontend/src/pages/StrategistActionPlanPage.jsx    ← leave as-is
backend/strategist_router.py                       ← leave as-is
backend/strategist_engine.py                       ← leave as-is
```

---

## 10. Route Registration (App.js)

```jsx
// Add this import with other lazy imports:
const TheStrategistLandingPage = lazy(() => import('./pages/TheStrategistLandingPage'));

// Add this route BEFORE the existing /strategist route:
<Route path="/the-strategist" element={<TheStrategistLandingPage />} />

// Existing route unchanged:
<Route path="/strategist" element={<StrategistPage />} />
```

---

## 11. Sitemap

Add to `frontend/public/sitemap.xml` in the Vedic Oracles section:
```xml
<url>
  <loc>https://www.everydayhoroscope.in/the-strategist</loc>
  <changefreq>weekly</changefreq>
  <priority>0.95</priority>
</url>
```

---

## 12. Build Verification

```bash
cd frontend
CI=true DISABLE_ESLINT_PLUGIN=true npx craco build
```
Zero errors required. Warnings acceptable.

---

## 13. Commit Format

```
feat(strategist): add premium public landing + war room visual rebuild
```

---

## 14. Definition of Done

**Deliverable A -- `/the-strategist`:**
- [ ] Loads without login -- full page visible
- [ ] Animated hero with star field and gold glow
- [ ] Birth details form saves to `localStorage.strategist-profile-draft`
- [ ] CTA routes to `/login?next=/strategist` when logged out
- [ ] CTA routes to `/strategist` when logged in
- [ ] SEO title, description, canonical URL correct
- [ ] JSON-LD `@graph` (WebPage + Service) in page head
- [ ] `/the-strategist` added to sitemap.xml
- [ ] Route registered in App.js

**Deliverable B -- `/strategist` visual rebuild:**
- [ ] Module Intro Screen shows with personalised welcome on first visit
- [ ] Welcome name reads from localStorage draft or auth context
- [ ] Layer strip sticky and state-aware (locked/active/complete)
- [ ] War Room header fills full width with state-appropriate colour/animation
- [ ] Golden Hour countdown large and prominent (not a small badge)
- [ ] Conquest Gauge enlarged -- score prominent, tier label visible
- [ ] Scoreboard numbers large and legible
- [ ] PRAY / WAIT / NO blocked state panels visually distinct
- [ ] All Gate 0 verdict paths work (existing logic preserved -- visual only)
- [ ] Mobile: all panels stack correctly at 375px
- [ ] Mobile: Golden Hour countdown fixed bottom bar during GOLDEN HOUR
- [ ] HurdleAlert rendered in Dashboard (between LKGateStatus and MissionQuickLinks)
- [ ] `StrategistLanding` has `noindex={true}` on its `<SEO>` component
- [ ] `/strategist` removed from sitemap.xml
- [ ] All logged-out CTAs use `navigate('/login', { state: { from: { pathname: '/strategist' } } })` -- NOT `?next=` URL params

**Both deliverables:**
- [ ] `npx craco build` passes with zero errors
- [ ] No existing logic removed or broken
