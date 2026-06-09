# CC New Thread Commission
## Premium Reports & Modules Audit -- Structure, Pricing & Legal Disclaimers
> **Issued:** 2026-06-08 | **Owner:** Claude Code New Thread
> **Type:** Research + Planning (no code changes without co-founder sign-off)
> **Output:** Structured tables + recommendations. Present output to co-founder for decisions.

---

## 0. Read First

Before doing anything else, read:
1. `CLAUDE.md` -- project architecture, env vars, commit format
2. `frontend/src/App.js` -- all routes (the source of truth for what exists)
3. `frontend/src/pages/system/PricingPage.jsx` -- current pricing tiers

---

## 1. Commission Scope

You are asked to produce **three structured deliverables** and present them to the co-founder for decisions. Do not make any code changes unless explicitly instructed.

### Deliverable 1 -- Master Premium Inventory Table
A single table listing every premium report and premium module in the app.
For each row, include these columns (defined in Section 3 below).

### Deliverable 2 -- Report Structure Proposals
For each **report** (not module), propose:
- How many named sections it should contain
- Approximate word / page count per section
- Total estimated page count of the PDF output
- Recommended one-time price (₹ INR)
- Rationale for pricing (complexity, value delivered, comparable products)

### Deliverable 3 -- Legal Disclaimer Strategy
Propose where and how legal disclaimers should appear across:
- All SEO landing pages (report and module landings)
- All generated report PDFs
- All premium module result pages (Strategist, Lumina, KP Oracle, etc.)
Produce a single recommended disclaimer text block, plus placement rules.

---

## 2. How to Discover the Full Inventory

### Step 1 -- Scan App.js for all routes
```bash
grep -E "path=.*report|path=.*kundali|path=.*lumina|path=.*strategist|path=.*palmistry|path=.*arc-angel|path=.*ritual|path=.*longevity|path=.*krishna|path=.*tarot|path=.*numerology|path=.*lagna|path=.*lk" frontend/src/App.js
```

### Step 2 -- Confirm SEO landing page existence
For each route, check if a public (non-gated) SEO landing page exists:
- Landing pages are in `frontend/src/pages/reports/landing/`
- Module landing pages are top-level in `frontend/src/pages/`
- Cross-check: is the route inside a `<PremiumRoute>`, `<ProtectedRoute>`, `<SeoResourceGate>`, or public?

### Step 3 -- Read existing report structure files
For the major reports, read these files to understand current section structure:
```
frontend/src/pages/kundali/BrihatKundliPage.jsx        ← 40+ page report, all sections
frontend/src/pages/kundali/BirthChartPage.jsx           ← Birth chart sections
frontend/src/pages/kundali/KundaliMilanPage.jsx         ← Kundali Milan sections
frontend/src/pages/reports/IndividualReportsPage.jsx    ← Report library overview
frontend/src/pages/longevity/LongevityReportPage.jsx    ← Longevity sections
frontend/src/pages/lumina/LuminaPage.jsx                ← Lumina tabs (9 tabs)
frontend/src/pages/strategist/StrategistWarRoomPage.jsx ← Strategist sections
frontend/src/pages/kp/KrishnaOraclePage.jsx             ← KP Oracle sections
```

### Step 4 -- Read existing landing page content files
```
frontend/src/pages/reports/landing/reportLandingContent.jsx   ← All report copy
frontend/src/pages/reports/category/reportCategoryData.js     ← Category definitions
frontend/src/pages/system/PricingPage.jsx                     ← Current tier pricing
```

---

## 3. Master Inventory Table -- Column Definitions

Build one comprehensive table. Separate reports from modules with a divider row.

| Column | Definition |
|---|---|
| **#** | Sequential number |
| **Name** | Display name of the report or module |
| **Route(s)** | All URL paths in App.js |
| **Type** | `Report` or `Module` |
| **Gate** | `PremiumRoute` / `ProtectedRoute` / `SeoResourceGate` / `Public` |
| **SEO Landing Page** | `Yes` (path) or `No` |
| **Current Price** | As shown in PricingPage.jsx or "Included in Premium" |
| **Current Section Count** | Count from reading the page file (approximate is fine) |
| **PDF Output?** | `Yes` / `No` / `Partial` |
| **Status** | `Live` / `Built -- Not Launched` / `Partial` |
| **Notes** | Any anomalies, gaps, or observations |

---

## 4. Report Structure Proposals -- Output Format

For each **report** row in the master table, produce this block:

```
### [Report Name]
Route: /...
Current price: ₹X (or N/A)

Proposed sections:
  1. [Section name] -- ~[word count] words / [pages]
  2. ...

Proposed total: ~[N] pages
Proposed price: ₹[X] (one-time) | Rationale: [1-2 sentences]
Premium subscription: Included / Excluded / Discounted to ₹X
```

### Pricing Reference Points (use these as anchors)
Current pricing already live in PricingPage.jsx:
- Birth Chart: ₹799 one-time
- Kundali Milan: ₹1,199 one-time
- Brihat Kundli Pro: ₹1,499 one-time
- Premium Monthly: ₹1,599/month

### Pricing Philosophy to Apply
- Reports that are **inputs-intensive** (birth details, questionnaire) and produce a **unique personalised PDF** should be priced higher.
- Reports that are **evergreen** (no live birth data required) can be priced lower or bundled.
- **Love Bundle** modules (multiple love reports under one product) may warrant a bundle price separate from individual report pricing.
- **Longevity Report** is deeply technical (KP + Dasha + Ayurvedic blend) -- price should reflect this.

---

## 5. Legal Disclaimer Strategy -- What to Produce

### 5a -- Recommended Disclaimer Text
Write one master disclaimer block (150-200 words) that covers:
- Astrological content is for **entertainment and spiritual guidance purposes only**
- Not a substitute for **medical, legal, financial, or psychological professional advice**
- Predictions are **probabilistic**, not guaranteed outcomes
- The platform is not responsible for decisions made based on content
- Content is based on **traditional Vedic astrology** principles
- For the Longevity Report specifically: **not a medical diagnosis**, consult a qualified physician

### 5b -- Placement Rules
For each placement location, specify:
- Whether disclaimer is visible inline or collapsed (accordion/toggle)
- Exact position on page (above CTA / below report output / footer of PDF / etc.)

Locations to cover:
1. Every SEO **report landing page** (before the CTA button)
2. Every SEO **module landing page** (The Strategist, The Tarot, Longevity, etc.)
3. Generated **report PDF** footer (every page of every PDF)
4. **Longevity Report** page -- inline, more prominent (medical proximity concern)
5. **KP Oracle** / **Arc Angel** result page -- inline
6. **Palmistry AI** result -- inline
7. **Global site footer** -- shortened one-liner

### 5c -- Implementation Plan (propose, don't implement)
After co-founder approves the disclaimer text:
- Identify where in the codebase the disclaimer component should live (shared component vs. per-page)
- List which files need to be edited
- Note that PDFs will need a footer template update

---

## 6. Known Premium Reports & Modules (pre-identified for your audit)

This list was compiled from App.js and the pages directory. Verify against the live codebase -- there may be additional items.

### Reports (dedicated report output pages)
| Name | Route(s) | Notes |
|---|---|---|
| Brihat Kundli Pro | `/brihat-kundli` | ₹1,499 one-time -- 40+ pages |
| Birth Chart | `/birth-chart` | ₹799 one-time |
| Kundali Milan | `/kundali-milan` | ₹1,199 one-time |
| Lagna Kundali | `/lagna-kundali`, `/lagna-kundali/chart/:id` | SeoResourceGate |
| Numerology Report | `/numerology/report/:reportId` | PremiumRoute |
| Love Reports | `/love-reports` | PremiumRoute |
| Longevity Report | `/longevity-report` | KP-based, deep technical |
| Karmic Debt Report | `/karmic-debt-report` | Landing exists |
| Career Blueprint Report | `/career-blueprint-report` | Landing exists |
| Shadow Self Report | `/shadow-self-report` | Landing exists |
| Retrograde Survival Report | `/retrograde-survival-report` | Landing exists |
| Life Cycles Report | `/life-cycles-report` | Landing exists |
| Wealth Blueprint Report | `/wealth-blueprint-report` | Landing exists |
| Romance Creative Report | `/romance-creative-report` | Landing exists |
| Vitality Health Report | `/vitality-health-report` | Landing exists |
| Partnership Window Report | `/partnership-window-report` | Landing exists |
| Dharma Purpose Report | `/dharma-purpose-report` | Landing exists |
| Gains Network Report | `/gains-network-report` | Landing exists |
| Encounter Window Report | `/encounter-window-report` | Landing exists |
| Love Weather Report | `/love-weather-report` | Landing exists |
| Date Night Report | `/date-night-report` | Landing exists |
| Intimacy Vitality Report | `/intimacy-vitality-report` | Landing exists |
| Venus Retrograde Report | `/venus-retrograde-report` | Landing exists |
| Soulmate Timing Report | `/soulmate-timing-report` | Landing exists |
| Soul Connection Report | `/soul-connection-report` | Landing exists |
| Lunar Cycle Wellness | `/lunar-cycle-wellness` | Landing exists |

### Premium Modules (interactive tools, not report PDFs)
| Name | Route(s) | Notes |
|---|---|---|
| The Strategist | `/strategist` + sub-routes | Multiple sub-pages |
| KP Oracle (Krishna Prashnavali) | `/krishna-prashnavali` | Bundle-native remedies |
| Lumina | `/lumina` | 9-tab layout |
| Palmistry (Hasta Rekha) | `/palmistry` | AI photo analysis |
| Tarot | `/tarot` | 78-card deck, spreads, history |
| Numerology | `/numerology` | 10+ report types |
| Arc Angel | `/arc-angel` | Premium + questionnaire |
| Ritual Engine | `/ritual-engine` | PremiumRoute |
| LK Standalone | `/lk/*` | Lal Kitab reports |
| Lagna Kundali | `/lagna-kundali` | Also listed as report |
| Birth Chart (tool) | `/birth-chart` | Also listed as report |
| My Reports | `/my-reports` | Library/hub |

---

## 7. Output Delivery

Present everything in this order:

1. **Section 1: Master Inventory Table** (all rows, all columns)
2. **Section 2: SEO Page Gap List** -- reports/modules that have NO SEO landing page (pull the No rows)
3. **Section 3: Report Structure Proposals** -- one block per report
4. **Section 4: Pricing Recommendations Table** -- compact version of Section 3 for easy co-founder review
5. **Section 5: Legal Disclaimer Recommendation** -- text block + placement rules

Label each section clearly. The co-founder will review each section and provide decisions.

---

## 8. Do Nots

- ❌ Do NOT make any code changes without explicit co-founder instruction
- ❌ Do NOT invent section structures -- base them on what actually exists in the page files
- ❌ Do NOT price reports without reading the current PricingPage.jsx anchors first
- ❌ Do NOT write a disclaimer that makes guarantees about astrological accuracy
- ❌ Do NOT mark a report as having a "SEO landing page" if it only has a gated tool page (PremiumRoute ≠ SEO landing)
- ❌ Do NOT include the KE / MongoDB / ingest work -- this is a frontend/product commission only

---

## 9. Definition: SEO Landing Page vs Tool Page

**SEO Landing Page** = a public, non-gated page that:
- Is NOT wrapped in `<PremiumRoute>`, `<ProtectedRoute>`, or `<SeoResourceGate>`
- Has meaningful content visible to logged-out users
- Has SEO meta tags / JSON-LD schema
- Exists to rank on Google and convert visitors

Examples that qualify: `/the-tarot`, `/the-strategist`, `/the-longevity-report`, `/karmic-debt-report`, `/premium-reports`

**Tool Page** = the actual interactive app, gated behind auth/premium. Does NOT count as "SEO Landing Page exists."

Mark `Yes` only if a genuine SEO landing page exists at a separate public route.
