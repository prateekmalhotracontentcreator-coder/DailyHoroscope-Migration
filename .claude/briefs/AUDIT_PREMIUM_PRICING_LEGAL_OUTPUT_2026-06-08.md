# Premium Reports & Modules Audit -- Pricing & Legal
> **Produced:** 2026-06-08 | **Commission:** CC_COMMISSION_PREMIUM_AUDIT_PRICING_LEGAL_2026-06-08  
> **Type:** Research output -- no code changes. All items require co-founder sign-off before action.

---

## Section 1 -- Master Inventory Table

> **Gate legend:** PR = PremiumRoute | ProtR = ProtectedRoute | SeoRG = SeoResourceGate | Pub = Public route (no gate -- tool or page handles auth inline if needed)

### Part A -- Reports

| # | Name | Route(s) | Type | Gate | SEO Landing Page | Current Price | Section Count | PDF Output? | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Brihat Kundli Pro | `/brihat-kundli` | Report | PR | No | ₹1,499 one-time | 9 (see §3) | Yes | Live | Most comprehensive report; 40+ pages claimed in PricingPage |
| 2 | Birth Chart | `/birth-chart` | Report | PR | No | ₹799 one-time | 6 (see §3) | Yes | Live | ₹799 on PricingPage. PremiumRoute gates |
| 3 | Kundali Milan | `/kundali-milan` | Report | PR | No | ₹1,199 one-time¹ | 5 (see §3) | Yes | Live | ¹ PricingPage says ₹1,199; KundaliMilanPage.jsx line 69 says ₹999. **Price discrepancy -- needs fix** |
| 4 | Longevity Report | `/longevity`, `/longevity-report`, `/longevity/report/:id` | Report | Pub + ProtR (saved) | Yes -- `/the-longevity-report` | Not on PricingPage | 7 (see §3) | Partial | Live | Publicly accessible tool (no gate), saved reports are ProtR. No price shown -- unclear monetisation |
| 5 | Numerology Report | `/numerology/report/:reportId` | Report | PR | No | Included in Premium | 11 types (see §3) | Yes | Live | 11 distinct report types generated from /numerology tile menu |
| 6 | Love Reports | `/love-reports` (hub) + 9 individual landing pages | Report | PR (hub) + Pub (individual landings) | Yes -- `/love` (hub landing) + each individual landing below | Included in Premium | 9 sub-reports (see §3) | Partial | Live | Sub-report landings are public SEO pages. Hub tool is PremiumRoute. |
| 7 | Lagna Kundali | `/lagna-kundali`, `/lagna-kundali/chart/:id` | Report | SeoRG | No (gated landing) | Login required | Same as Kundali chart | No | Live | SeoResourceGate = login + free registration unlocks. Not a PDF report |
| 8 | LK Reports | `/lk-remedies/report`, `/lk-remedies/debt-audit` | Report | ProtR | Partial -- `/lal-kitab-remedies` (module SEO landing) | Login required (free) | ~5 sections | Partial | Live | Public `/lal-kitab-remedies` is module landing, not report landing |
| 9 | Karmic Debt Report | `/karmic-debt-report` | Report | None (public landing) | Yes -- `/karmic-debt-report` | N/A | ~4-5 (inferred) | Unknown | Built -- Not Launched | Landing exists, no generation tool route confirmed in App.js |
| 10 | Career Blueprint Report | `/career-blueprint-report` | Report | None (public landing) | Yes -- `/career-blueprint-report` | N/A | ~4-5 (inferred) | Unknown | Built -- Not Launched | Same |
| 11 | Shadow Self Report | `/shadow-self-report` | Report | None (public landing) | Yes -- `/shadow-self-report` | N/A | ~4-5 (inferred) | Unknown | Built -- Not Launched | Same |
| 12 | Retrograde Survival Report | `/retrograde-survival-report` | Report | None (public landing) | Yes -- `/retrograde-survival-report` | N/A | ~4 (inferred) | Unknown | Built -- Not Launched | Same |
| 13 | Life Cycles Report | `/life-cycles-report` | Report | None (public landing) | Yes -- `/life-cycles-report` | N/A | ~4-5 (inferred) | Unknown | Built -- Not Launched | Same |
| 14 | Wealth Blueprint Report | `/wealth-blueprint-report` | Report | None (public landing) | Yes -- `/wealth-blueprint-report` | N/A | ~5 (inferred) | Unknown | Built -- Not Launched | Same |
| 15 | Romance Creative Report | `/romance-creative-report` | Report | None (public landing) | Yes -- `/romance-creative-report` | N/A | ~4 (inferred) | Unknown | Built -- Not Launched | Same |
| 16 | Vitality Health Report | `/vitality-health-report` | Report | None (public landing) | Yes -- `/vitality-health-report` | N/A | ~4-5 (inferred) | Unknown | Built -- Not Launched | Same |
| 17 | Partnership Window Report | `/partnership-window-report` | Report | None (public landing) | Yes -- `/partnership-window-report` | N/A | ~4 (inferred) | Unknown | Built -- Not Launched | Same |
| 18 | Dharma Purpose Report | `/dharma-purpose-report` | Report | None (public landing) | Yes -- `/dharma-purpose-report` | N/A | ~5 (inferred) | Unknown | Built -- Not Launched | Same |
| 19 | Gains Network Report | `/gains-network-report` | Report | None (public landing) | Yes -- `/gains-network-report` | N/A | ~4 (inferred) | Unknown | Built -- Not Launched | Same |
| 20 | Encounter Window | `/encounter-window-report` (landing) + inside `/love-reports` | Report | Pub landing + PR tool | Yes -- `/encounter-window-report` | Included in Premium | ~3-4 | No | Live (in love hub) | Dual-entry: standalone SEO landing + love hub sub-report |
| 21 | Love Weather | `/love-weather-report` (landing) + inside `/love-reports` | Report | Pub landing + PR tool | Yes -- `/love-weather-report` | Included in Premium | ~3-4 | No | Live (in love hub) | Same dual-entry |
| 22 | Date Night | `/date-night-report` (landing) + inside `/love-reports` | Report | Pub landing + PR tool | Yes -- `/date-night-report` | Included in Premium | ~3 | No | Live (in love hub) | Same |
| 23 | Intimacy & Vitality | `/intimacy-vitality-report` (landing) + inside `/love-reports` | Report | Pub landing + PR tool | Yes -- `/intimacy-vitality-report` | Included in Premium | ~3-4 | No | Live (in love hub) | Same |
| 24 | Venus Retrograde | `/venus-retrograde-report` (landing) + inside `/love-reports` | Report | Pub landing + PR tool | Yes -- `/venus-retrograde-report` | Included in Premium | ~3-4 | No | Live (in love hub) | Same |
| 25 | Soulmate Timing | `/soulmate-timing-report` (landing) + inside `/love-reports` | Report | Pub landing + PR tool | Yes -- `/soulmate-timing-report` | Included in Premium | ~3-4 | No | Live (in love hub) | Same |
| 26 | Soul Connection | `/soul-connection-report` (landing) + inside `/love-reports` | Report | Pub landing + PR tool | Yes -- `/soul-connection-report` | Included in Premium | ~3-4 | No | Live (in love hub) | Same |
| 27 | Lunar Cycle Wellness | `/lunar-cycle-wellness` (landing) + inside `/love-reports` | Report | Pub landing + PR tool | Yes -- `/lunar-cycle-wellness` | Included in Premium | ~3-4 | No | Live (in love hub) | Same |

---

### Part B -- Modules

| # | Name | Route(s) | Type | Gate | SEO Landing Page | Current Price | Features/Tabs | PDF Output? | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| M1 | The Strategist | `/the-strategist`, `/strategist`, `/strategist/*` (8 sub-routes) | Module | Pub landing + ProtR (all sub-routes) | Yes -- `/the-strategist` | Included in Premium | 5 gates + War Room + Executive + Missions + Report + Action Plan | Partial | Live | All sub-routes are ProtectedRoute. Landing is public |
| M2 | KP Oracle (Krishna Prashnavali) | `/krishna-prashnavali` | Module | Pub (inline PremiumGate) | No | Included in Premium | Oracle grid + KP chart + Verdicts + Sacred Remedy | No | Live | Public route; page handles premium gate inline via PremiumGateCard |
| M3 | Lumina | `/lumina` | Module | Pub (inline PremiumGate) | No | Included in Premium | 9 tabs: Home, Bible, Manifest, Marketplace, Spiritual, Devotion, Community, Journal, Chat | No | Live | Public route; inline premium gate for premium features |
| M4 | Palmistry (Hasta Rekha) | `/palmistry` | Module | Pub (inline PremiumGate) | No | Included in Premium | 12-Q assessment + AI palm reading + 5 sections | No | Live | Public route; PremiumGateCard inline |
| M5 | Tarot | `/tarot`, `/tarot/history` (history = PR) | Module | Pub tool + PR (history) | Yes -- `/the-tarot` | Included in Premium (history gated) | 78-card deck, spreads, daily draw, journal, history | No | Live | History is gated; tool is public |
| M6 | Numerology | `/numerology`, `/numerology/report/:id` (report = PR) | Module | Pub tool + PR (report) | No (tool IS the page) | Included in Premium (report gated) | 11 report tiles | Yes | Live | Module page at `/numerology` is public; report output is PremiumRoute |
| M7 | Arc Angel | `/arc-angel` | Module | ProtR | No | Included in Premium (login req.) | 12 life domains | No | Live | Requires login only -- not premium-gated (ProtectedRoute not PremiumRoute) |
| M8 | Ritual Engine | `/ritual-engine` | Module | PR | No | Included in Premium | Unknown (file not read) | No | Live | PremiumRoute confirmed |
| M9 | LK Standalone | `/lk-remedies`, `/lk-remedies/onboard`, `/lk-remedies/report`, `/lk-remedies/tracker`, `/lk-remedies/debt-audit`, `/lk-remedies/remedies` | Module | ProtR (most routes) + Pub (remedies browse) | Partial -- `/lal-kitab-remedies` (module SEO landing) | Login required (free) | 5 gates + 6-module flow | Partial | Live | `/lal-kitab-remedies` is the public SEO landing. Report/Onboard are ProtectedRoute |
| M10 | My Reports | `/my-reports` | Module | PR | No | Included in Premium | Library/hub | No | Live | Hub for saved reports, no generation |

---

## Section 2 -- SEO Gap List (Reports/Modules with NO Public SEO Landing Page)

These items have **zero public SEO presence** -- a logged-out Google crawler or organic visitor has no page to land on:

| # | Item | Route(s) | Gate | Gap Impact | Recommended Action |
|---|---|---|---|---|---|
| 1 | **Birth Chart** | `/birth-chart` | PremiumRoute | HIGH -- ₹799 product, largest revenue driver. Zero organic entry point | Create `/the-birth-chart` SEO landing |
| 2 | **Kundali Milan** | `/kundali-milan` | PremiumRoute | HIGH -- ₹1,199 product | Create `/kundali-milan-report` SEO landing |
| 3 | **Brihat Kundli Pro** | `/brihat-kundli` | PremiumRoute | HIGH -- ₹1,499 flagship report | Create `/brihat-kundli-pro` SEO landing |
| 4 | **Numerology** | `/numerology` (tool page doubles as public) | None / inline gate | MEDIUM -- tool page is public but not SEO-optimised as a landing | Dedicated SEO landing or SEO enhancement of current page |
| 5 | **KP Oracle** | `/krishna-prashnavali` | None / inline | MEDIUM -- tool page is public but no dedicated SEO conversion page | Create `/the-krishna-oracle` SEO landing |
| 6 | **Lumina** | `/lumina` | None / inline | MEDIUM -- 9-tab spiritual companion with no dedicated marketing page | Create `/the-lumina` SEO landing |
| 7 | **Palmistry** | `/palmistry` | None / inline | MEDIUM -- AI-photo palm reading, viral potential | Create `/the-palmistry` or `/hasta-rekha` SEO landing |
| 8 | **Arc Angel** | `/arc-angel` | ProtectedRoute | LOW-MED -- login required; landing would also need a register CTA | Create `/the-arc-angel` SEO landing |
| 9 | **Ritual Engine** | `/ritual-engine` | PremiumRoute | LOW -- premium-only, but visible landing would help with conversion | Create `/the-ritual-engine` SEO landing |
| 10 | **Numerology Report** | `/numerology/report/:id` | PremiumRoute | LOW -- report is generated from within numerology tool, so landing = numerology page | No separate landing needed if numerology page is enhanced |
| 11 | **My Reports** | `/my-reports` | PremiumRoute | LOW -- internal hub only, no SEO value needed | No action needed |

**Priority order for landing page creation:** Birth Chart > Brihat Kundli > Kundali Milan > KP Oracle > Palmistry > Lumina > Arc Angel

---

## Section 3 -- Report Structure Proposals

### 1. Brihat Kundli Pro
Route: `/brihat-kundli`  
Current price: ₹1,499 one-time

Confirmed sections (from BrihatKundliPage.jsx):
  1. Personal Trinity -- Ascendant, Moon Sign, Sun Sign with Nakshatra -- ~300 words / 1 page
  2. Janma Kundali -- North Indian Chart (SVG visual) -- 1 page (chart only)
  3. Planetary Positions -- All 9 planets, sign/house/dignity/strength table -- ~400 words / 1.5 pages
  4. Career & Profession -- Rating, best fields, strengths, career timeline -- ~500 words / 2 pages
  5. Love & Relationships -- Rating, partner traits, compatible/challenging signs, marriage timing -- ~400 words / 1.5 pages
  6. Health & Wellbeing -- Vitality rating, body constitution, vulnerable areas, diet -- ~350 words / 1.5 pages
  7. Wealth & Finance -- Rating, income sources, investments, avoidances -- ~350 words / 1.5 pages
  8. Dasha Periods -- Current Mahadasha + Antardasha timeline -- ~500 words / 2 pages
  9. Yogas & Doshas + Remedies (Gemstones, Mantras) -- ~600 words / 2 pages (inferred from PricingPage features)

Proposed total: ~40 pages (PricingPage claim matches)  
Proposed price: ₹1,499 (retain) | Rationale: Most comprehensive product; all birth-data intensive with 9 full sections and PDF. Already competitively priced vs. comparable Vedic report services (₹2,000-₹5,000 range offline).  
Premium subscription: Included (unlimited generation)

---

### 2. Birth Chart
Route: `/birth-chart`  
Current price: ₹799 one-time

Confirmed sections (from BirthChartPage.jsx):
  1. Planetary Positions -- Planet/sign/house table, affliction scores -- ~300 words / 1 page
  2. Birth Chart Visual (BirthChartDisplay) -- North Indian chart SVG -- 1 page
  3. Career Insights -- Top career domains by house/planet -- ~250 words / 1 page
  4. Love & Relationships -- Compatibility highlights from 7th house -- ~250 words / 1 page
  5. Health Overview -- 6th/8th house vulnerabilities -- ~200 words / 0.5 page
  6. Remedies (Remedy Packs from KE) -- Gemstones, mantras, behavioral -- ~400 words / 1.5 pages

Proposed total: ~6 pages  
Proposed price: ₹799 (retain) | Rationale: Entry-level personal report; lighter than Brihat. Good gateway product to upsell Brihat. Already well-priced.  
Premium subscription: Included (unlimited)

---

### 3. Kundali Milan
Route: `/kundali-milan`  
Current price: ₹1,199 on PricingPage / ₹999 shown in-page -- **PRICE DISCREPANCY, fix required**

Confirmed sections (from KundaliMilanPage.jsx + KundaliMilanDisplay component):
  1. Compatibility Score -- Total out of 36 with rating -- ~200 words / 0.5 page
  2. Ashtakoot Guna Breakdown -- All 8 Kootas with scores explained -- ~500 words / 2 pages
  3. Mangal Dosha Analysis -- Both charts assessed -- ~300 words / 1 page
  4. Both North Indian Kundali Charts -- Visual SVGs -- 2 pages
  5. Marriage Timing Guidance + Auspicious Dates -- ~300 words / 1 page
  6. Challenges & Personalised Remedies -- ~350 words / 1.5 pages

Proposed total: ~8 pages  
Proposed price: ₹999 one-time (standardise to in-page price) | Rationale: Two-person input, meaningful depth, but lighter than Brihat. ₹999 is more competitive for the Kundali Milan market (widely available at ₹500-₹1,500 online). Fix the PricingPage/in-page discrepancy -- standardise on ₹999.  
Premium subscription: Included (unlimited)

---

### 4. Longevity Report (Ayur Jyotish)
Route: `/longevity`, `/longevity-report`  
Current price: Not listed on PricingPage -- unclear monetisation

Confirmed sections (from LongevityReportPage.jsx SECTION_PREVIEWS):
  1. Longevity Classification -- KP sub-lord scoring of Ayush potential (houses 1, 2, 7, 8, Saturn) -- ~400 words / 1.5 pages
  2. Constitutional Health Profile (Prakriti) -- Ascendant/Moon/Sun dosha weighting -- ~350 words / 1.5 pages
  3. Vulnerable Body Systems & Organs -- Sign-body, house-health, planet-disease mapping -- ~450 words / 2 pages
  4. Disease Susceptibility Windows -- Dasha × transit windows -- ~400 words / 1.5 pages
  5. Critical Period Alerts -- Maraka triggers, 22nd Drekkana, 64th Navamsa -- ~300 words / 1.5 pages
  6. Remedial & Preventive Guidance -- Mantras, routine, prevention priorities -- ~400 words / 1.5 pages
  7. Decade-wise Quality of Life Forecast -- Life-arc quality map from Dasha dominance -- ~500 words / 2 pages

Proposed total: ~11 pages  
Proposed price: ₹1,299 one-time | Rationale: Most technically intensive of all reports (KP system + pyswisseph + Dasha timing + Ayurvedic mapping). Medical-adjacent = higher perceived value and legal obligation. Comparable "health astrology" products offline run ₹3,000-₹8,000. ₹1,299 is well below that while being above the Birth Chart tier.  
Premium subscription: Discounted to ₹999 (loyalty benefit for premium members)

---

### 5. Numerology Report (all 11 types)
Route: `/numerology/report/:reportId`  
Current price: Included in Premium (no standalone price visible)

Confirmed report types (from NumerologyPage.jsx TILE_META):
  1. Life Path & Soul Mission
  2. Name Correction & Energy Alignment
  3. Favorable Timing
  4. Karmic Debt & Lo Shu Grid
  5. Relationship Compatibility
  6. Career Guidance
  7. Lucky Digital Vibrations
  8. Residential Compatibility
  9. Business & Brand Optimization
  10. Auspicious Baby Name
  11. Premium Ankjyotish Report (birth time + place required)

Each report: ~4-6 sections, ~600-900 words per report  
Proposed total per report: ~3-4 pages  
Proposed price: ₹349 one-time per report | ₹999 all-access numerology bundle | Rationale: Lighter than Vedic chart reports; no birth-time required for most types. Good impulse price point. Ankjyotish (premium type requiring birth time) could be ₹499 given added complexity.  
Premium subscription: All types included

---

### 6. Love Reports (hub -- 9 sub-reports)
Route: `/love-reports`  
Current price: Included in Premium

Confirmed sub-reports (from LoveReportsPage.jsx):
  1. Love Weather -- 90-day romantic forecast, best/caution dates
  2. Encounter Window -- Transit windows for new meetings
  3. Date Night -- Daily Love Battery score and timing
  4. Digital Dating -- Profile/message timing optimisation
  5. Intimacy & Vitality -- Mars-Venus windows
  6. Lunar Cycle Wellness -- 30-day moon cycle wellness
  7. Venus Retrograde -- Retrograde relationship themes
  8. Soulmate Timing -- Jupiter + Dasha windows for partnership
  9. Soul Connection -- Karmic/evolutionary relationship patterns

Each report: ~3-4 sections, ~400-600 words  
Proposed total per sub-report: ~2-3 pages  
Proposed price: ₹249 per report | ₹999 Love Bundle (all 9) | Rationale: These are time-based forecasts (not static PDF reports), lower complexity than Vedic chart reports. Bundle pricing drives better conversion for the love category.  
Premium subscription: All 9 included

---

### 7. Karmic Debt Report
Route: `/karmic-debt-report` (SEO landing exists)  
Current price: N/A -- not yet launched

Proposed sections (inferred from category + Vedic tradition):
  1. Karmic Debt Number Identification -- Pythagorean/Vedic numerology scan -- ~300 words / 1 page
  2. Active Karmic Patterns -- What life areas are affected -- ~400 words / 1.5 pages
  3. Root Cause Analysis -- Astrological indicators (Rahu/Ketu + Saturn) -- ~350 words / 1.5 pages
  4. Clearing Protocol -- Practical remediation steps -- ~400 words / 1.5 pages
  5. Karmic Timeline -- When debts peak vs. when clearing accelerates -- ~300 words / 1 page

Proposed total: ~7 pages  
Proposed price: ₹599 one-time | Rationale: Birth-data intensive, actionable, evergreen. Higher perceived value due to "karmic" theme resonance with Indian audience. No real-time computation needed → lower backend cost.  
Premium subscription: Included

---

### 8. Career Blueprint Report
Route: `/career-blueprint-report`  
Current price: N/A

Proposed sections:
  1. Career House Analysis -- 10th house lord, occupants, aspects -- ~350 words / 1.5 pages
  2. Vocational Aptitude Map -- Planet-profession mapping (Sun/Mars/Mercury/Jupiter sectors) -- ~400 words / 1.5 pages
  3. Career Timeline -- Mahadasha/Antardasha career windows -- ~400 words / 1.5 pages
  4. Wealth Potential -- 2nd and 11th house assessment -- ~300 words / 1 page
  5. Action Plan & Remedies -- Practical next steps + gemstone/mantra -- ~350 words / 1.5 pages

Proposed total: ~7 pages  
Proposed price: ₹649 one-time | Rationale: High-intent purchase for professional audience. Career decisions are high-stakes = willingness to pay. Comparable career astrology products run ₹1,500-₹3,000 offline.  
Premium subscription: Included

---

### 9. Shadow Self Report
Route: `/shadow-self-report`  
Current price: N/A

Proposed sections:
  1. Shadow Indicators -- 8th/12th house, Rahu/Ketu, afflicted Moon -- ~350 words / 1.5 pages
  2. Core Wound Pattern -- What drives unconscious behaviour -- ~400 words / 1.5 pages
  3. Psychological Blind Spots -- Projected fears by house/sign -- ~350 words / 1.5 pages
  4. Integration Pathway -- Moving from shadow to strength -- ~400 words / 1.5 pages

Proposed total: ~6 pages  
Proposed price: ₹499 one-time | Rationale: Introspective, niche appeal; smaller audience than career/love but high emotional engagement. Comparable to "inner child" or "shadow work" products (₹800-₹2,000 in therapy-adjacent markets).  
Premium subscription: Included

---

### 10. Retrograde Survival Report
Route: `/retrograde-survival-report`  
Current price: N/A

Proposed sections:
  1. Active Retrogrades in Your Chart -- Natal retrograde planets -- ~250 words / 1 page
  2. Current/Upcoming Transit Retrogrades -- Planetary Rx windows in next 12 months -- ~300 words / 1 page
  3. Impact by Life Domain -- How each Rx affects your natal chart houses -- ~400 words / 1.5 pages
  4. Survival Strategies -- Timing guidance + practical remedies per planet -- ~350 words / 1.5 pages

Proposed total: ~5 pages  
Proposed price: ₹399 one-time | Rationale: Time-sensitive product (retrogrades come and go); lower evergreen shelf life but creates repeat purchase opportunity.  
Premium subscription: Included

---

### 11. Life Cycles Report
Route: `/life-cycles-report`  
Current price: N/A

Proposed sections:
  1. Planetary Periods Overview -- Full Vimshottari Dasha sequence from birth -- ~400 words / 1.5 pages
  2. Current Cycle Deep Dive -- Mahadasha + Antardasha analysis -- ~400 words / 1.5 pages
  3. Upcoming Cycle Forecast -- Next 2 major Dashas -- ~350 words / 1.5 pages
  4. Life Theme Patterns -- Recurring patterns by house/lord sequence -- ~300 words / 1 page
  5. Remedies by Cycle -- What to prioritise in each period -- ~350 words / 1.5 pages

Proposed total: ~7 pages  
Proposed price: ₹549 one-time | Rationale: Birth-data intensive, forward-looking, evergreen. Appeals to planning-oriented users who want a multi-year map.  
Premium subscription: Included

---

### 12. Wealth Blueprint Report
Route: `/wealth-blueprint-report`  
Current price: N/A

Proposed sections:
  1. Wealth Houses -- 2nd, 5th, 9th, 11th house lords and occupants -- ~350 words / 1.5 pages
  2. Dhana Yoga Assessment -- Wealth combinations in the chart -- ~400 words / 1.5 pages
  3. Investment Timing -- Dasha windows most favourable for wealth decisions -- ~350 words / 1.5 pages
  4. Financial Blind Spots -- 6th/8th house threats to wealth -- ~300 words / 1 page
  5. Remedies & Action Protocol -- Practical steps + gemstones -- ~350 words / 1.5 pages

Proposed total: ~7 pages  
Proposed price: ₹649 one-time | Rationale: Same reasoning as Career Blueprint -- high-intent, actionable, decision-supporting.  
Premium subscription: Included

---

### 13-14. Romance Creative Report + Partnership Window Report
Routes: `/romance-creative-report`, `/partnership-window-report`  
Current price: N/A

These are medium-depth love/relationship reports (distinct from the Love Reports hub which is time-based). Proposed structure: ~4-5 sections, ~5 pages each.  
Proposed price: ₹449 one-time each  
Premium subscription: Included

---

### 15-16. Vitality Health Report + Dharma Purpose Report
Routes: `/vitality-health-report`, `/dharma-purpose-report`  
Current price: N/A

Health: ~5 sections (~6 pages). Dharma: ~5 sections (~6 pages).  
Proposed price: Vitality ₹549, Dharma ₹549 one-time  
Premium subscription: Included

**Note on Vitality Health Report:** Should carry the same medical disclaimer as Longevity. Not a medical diagnosis.

---

### 17-18. Gains Network Report + Encounter Window Report (standalone)
Routes: `/gains-network-report`, `/encounter-window-report`  
Current price: N/A / Included in Premium (love hub)

Gains Network (financial networking): ~4 sections, ~5 pages. Proposed ₹399.  
Encounter Window as standalone (differs from love hub sub-report): Same as love hub version. Proposed ₹249 standalone or part of Love Bundle.

---

## Section 4 -- Pricing Recommendations Table

> For co-founder decision. "Retain" = no change. "Proposed" = new price recommendation. "Fix" = existing discrepancy.

| # | Item | Current Price | Proposed Price | Action | Rationale |
|---|---|---|---|---|---|
| 1 | Brihat Kundli Pro | ₹1,499 one-time | ₹1,499 | Retain | Flagship, correct price point |
| 2 | Birth Chart | ₹799 one-time | ₹799 | Retain | Good entry price |
| 3 | Kundali Milan | ₹1,199 (PricingPage) / ₹999 (in-page) | ₹999 | **Fix discrepancy → standardise to ₹999** | In-page is what users see at purchase; PricingPage must match |
| 4 | Longevity Report | Not on PricingPage | ₹1,299 one-time / ₹999 for Premium members | **Add to PricingPage** | Most technically intensive; medical-adjacent |
| 5 | Numerology Report (per type) | Included in Premium only | ₹349 standalone / ₹999 all-access bundle | **Add standalone option** | Unlock new revenue from non-premium users |
| 6 | Numerology Report -- Ankjyotish type | Included in Premium only | ₹499 standalone | **Add standalone option** | Requires birth time/place, higher complexity |
| 7 | Love Reports -- individual | Included in Premium only | ₹249 per report | **Add standalone option** | Time-sensitive; repeat purchase potential |
| 8 | Love Reports -- bundle (all 9) | Included in Premium | ₹999 Love Bundle | **Add Love Bundle product** | Drives bundle conversion |
| 9 | Karmic Debt Report | N/A | ₹599 | Launch when backend ready | |
| 10 | Career Blueprint Report | N/A | ₹649 | Launch when backend ready | |
| 11 | Shadow Self Report | N/A | ₹499 | Launch when backend ready | |
| 12 | Retrograde Survival Report | N/A | ₹399 | Launch when backend ready | |
| 13 | Life Cycles Report | N/A | ₹549 | Launch when backend ready | |
| 14 | Wealth Blueprint Report | N/A | ₹649 | Launch when backend ready | |
| 15 | Romance Creative Report | N/A | ₹449 | Launch when backend ready | |
| 16 | Vitality Health Report | N/A | ₹549 | Launch when backend ready | Medical disclaimer required |
| 17 | Partnership Window Report | N/A | ₹449 | Launch when backend ready | |
| 18 | Dharma Purpose Report | N/A | ₹549 | Launch when backend ready | |
| 19 | Gains Network Report | N/A | ₹399 | Launch when backend ready | |
| 20 | Premium Monthly | ₹1,599/month | ₹1,599 | Retain | Correct positioning |

---

## Section 5 -- Legal Disclaimer Recommendation

### 5a -- Master Disclaimer Text Block

> **Recommended text (168 words). Use verbatim or adjust tone with co-founder sign-off.**

---

*EverydayHoroscope provides astrological content rooted in traditional Vedic Jyotish and numerological systems for entertainment, spiritual reflection, and personal guidance purposes only.*

*All reports, readings, forecasts, and module outputs -- including birth chart analyses, longevity indicators, health profiles, numerology readings, tarot guidance, palmistry assessments, oracle responses, and relationship compatibility scores -- are generated using classical astrological principles and AI interpretation. They are not a substitute for professional medical, legal, financial, psychological, or any other professional advice.*

*Astrological forecasts and predictions are probabilistic in nature and reflect tendencies, not guaranteed outcomes. EverydayHoroscope is not liable for any decisions, actions, or inactions taken based on content provided through this platform.*

*The Longevity Report and Vitality Health Report identify astrological indicators traditionally associated with health and lifespan. They are NOT medical diagnoses, prognoses, or clinical assessments. Always consult a qualified medical professional for any health-related decisions.*

*Content is generated using classical Vedic astrology (Parashari and Krishnamurti Paddhati systems) with Swiss Ephemeris precision.*

---

### 5b -- Placement Rules

| Location | Disclaimer Version | Visibility | Exact Position |
|---|---|---|---|
| **Every SEO report landing page** (e.g. `/karmic-debt-report`, `/the-longevity-report`) | Short form (2 sentences: entertainment only + not professional advice) | Visible inline, no toggle | Below the last CTA button, before the footer. Small text, `text-muted-foreground text-xs`. |
| **Every SEO module landing page** (`/the-strategist`, `/the-tarot`, `/lal-kitab-remedies`) | Short form | Visible inline | Same: below CTA, above footer |
| **Generated report PDFs** (Brihat Kundli, Birth Chart, Kundali Milan, Longevity) | Full master text block | Full text | Footer of every PDF page -- 8pt font, centred, below a thin rule |
| **Longevity Report page** (`/longevity`, `/longevity-report`) | Extended text (include full medical paragraph explicitly) | Visible inline -- **NOT collapsed** | Directly above the "Generate Report" CTA -- prominent position, not buried. Use an amber/warning-toned card (`bg-amber-500/5 border border-amber-500/20`) |
| **Vitality Health Report** | Same as Longevity | Visible inline | Same position -- above CTA |
| **KP Oracle result page** (`/krishna-prashnavali`) | Short form | Visible inline (below oracle grid) | After verdict card, before sacred remedy section |
| **Arc Angel result page** (`/arc-angel`) | Short form | Visible inline | Below 12-domain output, above remedies |
| **Palmistry result page** (`/palmistry`) | Short form | Visible inline | Below AI reading output |
| **Global site footer** | One-liner: *"All content is for entertainment and spiritual guidance only. Not professional advice."* | Always visible | Pinned to the bottom row of the Footer component, centred, `text-muted-foreground text-xs` |

---

### 5c -- Implementation Plan (proposed -- no code changes until co-founder approves)

**Component to create:** `<AstroDisclaimer variant="short" | "full" | "medical" />`
- Lives in: `frontend/src/components/AstroDisclaimer.jsx`
- Three variants: `short` (2 sentences), `full` (master block), `medical` (full block + bolded medical paragraph)
- Footer gets a separate one-liner string, not the component

**Files that need editing once approved:**

| File | Change |
|---|---|
| `frontend/src/components/Footer.jsx` | Add one-liner disclaimer text to bottom row |
| `frontend/src/pages/reports/LongevityLanding.jsx` | Add `<AstroDisclaimer variant="medical" />` above CTA |
| `frontend/src/pages/reports/LongevityReportPage.jsx` | Add `<AstroDisclaimer variant="medical" />` above generate button |
| `frontend/src/pages/reports/landing/VitalityHealthLandingPage.jsx` | Add `<AstroDisclaimer variant="medical" />` above CTA |
| All other report landing pages (17 files in `frontend/src/pages/reports/landing/`) | Add `<AstroDisclaimer variant="short" />` below CTA |
| `frontend/src/pages/strategist/TheStrategistLandingPage.jsx` | Add `<AstroDisclaimer variant="short" />` |
| `frontend/src/pages/lk/LalKitabLandingPage.jsx` | Add `<AstroDisclaimer variant="short" />` |
| `frontend/src/pages/tarot/TarotLanding.jsx` | Add `<AstroDisclaimer variant="short" />` |
| `frontend/src/pages/reports/LongevityLanding.jsx` | Already noted above |
| `frontend/src/pages/kp/KrishnaOraclePage.jsx` | Add `<AstroDisclaimer variant="short" />` after verdict output |
| `frontend/src/pages/arc-angel/ArcAngelPage.jsx` | Add `<AstroDisclaimer variant="short" />` below domain grid |
| `frontend/src/pages/palmistry/PalmistryPage.jsx` | Add `<AstroDisclaimer variant="short" />` below result |
| PDF generation backend (report endpoints) | Add disclaimer text block to PDF footer template -- separate backend commission |

**PDF footer:** requires a backend commission (not this one). The disclaimer text block above is the approved copy to pass to the PDF template.

---

## Anomalies & Flags for Co-Founder Decision

| # | Item | Issue | Recommended Action |
|---|---|---|---|
| A1 | Kundali Milan price discrepancy | PricingPage shows ₹1,199; KundaliMilanPage.jsx line 69 shows ₹999 | Standardise to ₹999 (lower is what user sees at point of sale) |
| A2 | Longevity Report has no price | Tool is public and free to use currently. No Razorpay integration visible | Decide: free forever? one-time purchase? premium-included? |
| A3 | KP Oracle has no gate in App.js | Route is fully public -- no PremiumRoute, no ProtectedRoute. Page handles inline via PremiumGateCard | Confirm intent: is this correct, or should it be ProtectedRoute? |
| A4 | Lumina has no gate in App.js | Same as A3 -- public route, inline gate only | Same question |
| A5 | Arc Angel is ProtectedRoute (login only) but no premium gate | Free registered users can access all 12 arc angel domains. Is this intended? | Confirm whether Arc Angel should require premium |
| A6 | 12 "Built -- Not Launched" report landing pages | These have public SEO pages but no confirmed generation tool route in App.js. They create SEO value but also user disappointment if CTAs lead nowhere | Prioritise building backends for top 5 (Career, Karmic Debt, Life Cycles, Wealth, Dharma) |
| A7 | `/love` (LovePage) vs `/love-reports` (LoveReportsPage) | Two separate public/gated pages for love reports with slight list differences (LovePage has `digital-dating`, LoveReportsPage has `digital_dating_strategy`). Routes confirmed in App.js | Audit for list consistency; consolidate if possible |
| A8 | Weekly/Monthly Horoscope behind PremiumRoute | PricingPage free tier lists "Weekly forecast" and "Monthly outlook" as included in free -- but App.js wraps both in PremiumRoute | This is a promise-gate mismatch. Either update PricingPage or remove PremiumRoute gate |
