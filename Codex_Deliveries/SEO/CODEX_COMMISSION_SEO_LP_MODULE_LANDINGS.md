# Commission SEO-LP-1 -- 9 Public SEO Landing Pages: Kundali Suite + Premium Modules + Companions

> EverydayHoroscope · Stack: React 18, Tailwind CSS  
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
> Live app: https://www.everydayhoroscope.in  
> Date issued: 2026-06-08

---

## Context

The following revenue-critical products and premium modules are live and fully functional but have **zero public SEO landing pages**. A logged-out Google user or organic visitor has no page to land on. This commission builds 9 dedicated SEO landing pages -- one per product or module -- to create proper organic entry points and conversion funnels.

**The problem:** Every product below has a tool/report page gated behind auth or premium. None has a public marketing page that explains what it is, shows what it delivers, and converts visitors.

---

## Reference Architecture -- Read These Files First

```
frontend/src/pages/strategist/TheStrategistLandingPage.jsx   ← primary structural template
frontend/src/pages/reports/LongevityLanding.jsx               ← reference for technical report landings
frontend/src/pages/tarot/TarotLanding.jsx                     ← reference for tool module landings
frontend/src/pages/lk/LalKitabLandingPage.jsx                 ← reference for multi-gate module landings
frontend/src/pages/system/PricingPage.jsx                     ← pricing anchors (read before writing copy)
frontend/src/App.js                                           ← add all 9 routes here
frontend/public/sitemap.xml                                   ← add all 9 URLs here
```

**Key pattern:** Each landing page is a standalone `.jsx` file (not a shell + content file). It is a public route with no auth gate. The page explains the product, previews the output, and CTA directs to the gated tool page where auth/payment is handled.

---

## Common Page Structure (apply to all 9 pages)

Every page contains exactly these sections in order:

1. **Hero** -- product name, hook headline, one-line description, primary + secondary CTA
2. **What You Get** -- 6 feature cards in a 2×3 or 3×2 grid (GlassCard style)
3. **How It Works** -- 3 numbered steps (enter details → compute → receive)
4. **Preview / Sample** -- blurred or obscured sample of what the output looks like
5. **FAQ** -- 3 questions with accordion reveal
6. **CTA Banner** -- full-width gold-accented closing banner with repeat primary CTA

**Styling (applies to all 9):**
- Background: `bg-background` with subtle radial gradients (follow TheStrategistLandingPage for dark feel)
- Headings: Playfair Display (`font-playfair`)
- Body: DM Sans
- Accent: `text-gold` / `border-gold` / `bg-gold/[0.04]` (#c5a059)
- GlassCard: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`
- Each page may use a secondary accent color for its product icon and badge ONLY -- not as background fill
- No new npm packages
- `<SEO>` component from `frontend/src/components/SEO.jsx` -- include on every page
- `<Footer>` component from `frontend/src/components/Footer.jsx` -- include on every page

---

## Group A -- Kundali Product Suite (3 pages)

These are the three Vedic chart products on the Pricing page. They have explicit prices. CTAs point directly to the gated tool pages. Include the price in the hero badge.

### File locations
```
frontend/src/pages/kundali/BirthChartLandingPage.jsx
frontend/src/pages/kundali/KundaliMilanLandingPage.jsx
frontend/src/pages/kundali/BrihatKundliLandingPage.jsx
```

### Routes to add in App.js (all public, no gate)
```jsx
<Route path="/the-birth-chart"   element={<BirthChartLandingPage />} />
<Route path="/the-kundali-milan" element={<KundaliMilanLandingPage />} />
<Route path="/the-brihat-kundli" element={<BrihatKundliLandingPage />} />
```

---

### A-1 -- Birth Chart Landing Page
**File:** `frontend/src/pages/kundali/BirthChartLandingPage.jsx`  
**Route:** `/the-birth-chart`  
**CTA target:** `/birth-chart` (PremiumRoute -- handles payment/login)

| Field | Value |
|---|---|
| Product name | Vedic Birth Chart |
| Price badge | ₹799 one-time |
| Accent color | Gold (#c5a059) |
| Icon | `⊕` |
| Hook headline | "Every planet at the moment you were born placed itself somewhere for a reason." |
| Subline | "A full Vedic birth chart analysis -- planetary positions, Dasha timing, career & wealth insights, and personalised remedies." |
| Primary CTA label | "Generate My Birth Chart -- ₹799" |
| Secondary CTA label | "See What's Included" (smooth-scrolls to Section 2) |

**Feature cards (Section 2):**
| Title | Body |
|---|---|
| Ascendant & Lagna | Your rising sign and its lord -- the foundation of your Vedic identity, health signposts, and physical constitution. |
| All 9 Planetary Positions | Sign, house, dignity, strength, and retrograde status for Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu. |
| Career & Wealth Signals | 10th house analysis, Dhana Yoga indicators, and the professional strengths written into your planetary placements. |
| Love & Relationships | 7th house lord analysis, compatible and challenging signs, and timing windows most favourable for partnership. |
| Vimshottari Dasha Timeline | Your current Mahadasha and Antardasha period -- what planetary energy is governing your life right now and when it transitions. |
| Personalised Remedies | Gemstone recommendations, Vedic mantras, and behavioural remedies calibrated to your chart's specific afflictions. |

**How It Works (Section 3):**
1. "Enter your birth details" -- date of birth, time, and city. The more precise your birth time, the more accurate your Lagna and house cusps.
2. "Swiss Ephemeris computes your chart" -- planetary longitudes, house cusps, dignities, and Dasha balance calculated to sub-degree precision using pyswisseph.
3. "Receive your Vedic Birth Chart" -- a full chart with planetary table, PDF download, and personalised interpretation across career, love, health, and wealth.

**Sample section (Section 4):** Show a blurred table with columns Planet / Sign / House / Status / Strength, with a gold "Premium -- Unlock Full Chart" overlay banner.

**FAQ (Section 5):**
- "What is a Vedic birth chart?" -- Explain that Jyotish (Vedic astrology) uses the sidereal zodiac and the Lagna (rising sign) as the primary lens, vs. Western astrology's tropical zodiac and Sun sign focus.
- "How is this different from a Western birth chart?" -- Sidereal vs. tropical difference explained; Vedic includes Dasha periods (planetary time cycles) which Western charts do not.
- "What if I don't know my exact birth time?" -- Explain that approximate time still yields meaningful results; Lagna accuracy reduces but planetary positions remain valid. Moon-based analysis available for unknown birth time.

**SEO:**
```
title:       "Vedic Birth Chart Analysis -- Planetary Positions, Dasha & Remedies | Everyday Horoscope"
description: "Generate your personalised Vedic birth chart. All 9 planetary positions, Vimshottari Dasha timeline, career and wealth signals, and gemstone remedies. ₹799 one-time."
url:         "https://www.everydayhoroscope.in/the-birth-chart"
JSON-LD:     FAQPage schema using the 3 FAQ items above
```

---

### A-2 -- Kundali Milan Landing Page
**File:** `frontend/src/pages/kundali/KundaliMilanLandingPage.jsx`  
**Route:** `/the-kundali-milan`  
**CTA target:** `/kundali-milan` (PremiumRoute -- handles payment/login)

| Field | Value |
|---|---|
| Product name | Kundali Milan |
| Price badge | ₹999 one-time |
| Accent color | Rose (#e07080) |
| Icon | `⚭` |
| Hook headline | "Before the wedding, ask the stars what they already know about you two." |
| Subline | "The classical Ashtakoot Guna Milan analysis -- 36 compatibility points, Mangal Dosha assessment, and personalised remedies for both charts." |
| Primary CTA label | "Get Kundali Milan -- ₹999" |
| Secondary CTA label | "See What's Included" (smooth-scroll) |

**Feature cards (Section 2):**
| Title | Body |
|---|---|
| 36-Point Guna Milan | All 8 Kootas (Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi) scored and explained with a total compatibility verdict. |
| Mangal Dosha Assessment | Both charts analysed for Mangal Dosha -- identified, rated by severity, and remedied where applicable. |
| Both North Indian Charts | Full chart SVG for both persons -- planetary positions and house placements side by side. |
| Relationship Strengths | The Koota scores that favour your partnership -- communication, temperament alignment, sexual compatibility, and longevity indicators. |
| Auspicious Wedding Dates | Muhurat guidance for the most favourable dates based on combined chart analysis. |
| Personalised Dosha Remedies | Specific mantra, gemstone, and ritual remedies for any Doshas identified in either chart. |

**How It Works (Section 3):**
1. "Enter birth details for both persons" -- date, time, and city for Person 1 and Person 2. Both must be provided.
2. "Vedic engine computes both charts" -- Ashtakoot scoring, Mangal Dosha identification, planetary positions, and Muhurat windows calculated.
3. "Receive your Kundali Milan report" -- full compatibility analysis with PDF download, dosha remedies, and marriage timing guidance.

**Sample section (Section 4):** Show a blurred score card with an 8-row Koota table and a score total (e.g. "27 / 36") with gold overlay banner.

**FAQ (Section 5):**
- "What is Guna Milan?" -- Explain Ashtakoot system: 8 qualities assessed across both charts, max 36 points, with 18+ traditionally considered a viable match.
- "What score is considered a good match?" -- Traditional guidance: 18-24 = acceptable, 24-32 = good, 32+ = excellent. Explain nuances (Nadi Dosha override, etc.).
- "What happens if Mangal Dosha is present?" -- Explain that Mangal Dosha (Mars in houses 1/2/4/7/8/12) is common and manageable. Remedies and exceptions (mutual Dosha, Jupiter cancellation) are included in the report.

**SEO:**
```
title:       "Kundali Milan -- Vedic Marriage Compatibility Report | Everyday Horoscope"
description: "Classical Ashtakoot Guna Milan compatibility analysis for marriage. 36-point score, Mangal Dosha assessment, auspicious dates, and personalised remedies. ₹999 one-time."
url:         "https://www.everydayhoroscope.in/the-kundali-milan"
JSON-LD:     FAQPage schema
```

---

### A-3 -- Brihat Kundli Pro Landing Page
**File:** `frontend/src/pages/kundali/BrihatKundliLandingPage.jsx`  
**Route:** `/the-brihat-kundli`  
**CTA target:** `/brihat-kundli` (PremiumRoute -- handles payment/login)

| Field | Value |
|---|---|
| Product name | Brihat Kundli Pro |
| Price badge | ₹1,499 one-time |
| Accent color | Purple (#9b59b6) |
| Icon | `◈` |
| Hook headline | "A 40-page life map drawn entirely from your birth moment -- every domain, every planet, every Dasha." |
| Subline | "The most comprehensive Vedic report available. Career, love, health, wealth, Dasha timeline, Yogas, Doshas, and full remedies -- all in a single PDF." |
| Primary CTA label | "Get Brihat Kundli Pro -- ₹1,499" |
| Secondary CTA label | "See What's Inside" (smooth-scroll) |

**Feature cards (Section 2):**
| Title | Body |
|---|---|
| 40+ Page Report | The most comprehensive Vedic life report on EverydayHoroscope -- substantially deeper than the standard Birth Chart. |
| All 9 Planetary Positions | Sign, house, dignity, strength, combust/retrograde status, and Shadbala scores for all 9 Vedic planets. |
| Career, Love & Wealth Deep Dive | Three full-section analyses covering career fields, wealth signals, relationship indicators, health vulnerabilities, and more. |
| Full Dasha Timeline | Current Mahadasha and Antardasha with period predictions, plus the upcoming Dasha sequence for forward planning. |
| Yoga & Dosha Analysis | Raj Yogas, Dhana Yogas, Mangal Dosha, Kaal Sarp, and other significant combinations identified and interpreted. |
| Gemstone, Mantra & Numerology | A complete remediation protocol plus a numerology reading derived from your birth name and date. |

**How It Works (Section 3):**
1. "Enter your birth details" -- date, time, and city. Precise birth time is especially important for Brihat Kundli -- it determines Lagna and all house cusps.
2. "Full Vedic computation runs" -- Lagna, all 9 planets, divisional charts, Shadbala scores, Yoga identification, Dosha detection, and Dasha calculation.
3. "40+ page report generated and PDF produced" -- every major life domain analysed in plain English with actionable remedies and a downloadable PDF.

**Sample section (Section 4):** Show a blurred multi-section report card with section headers visible (Career, Love, Health, Wealth, Dasha) and a purple-toned "Premium" overlay banner.

**FAQ (Section 5):**
- "How is Brihat Kundli different from the Birth Chart?" -- Birth Chart gives a structured overview (~6 pages). Brihat Kundli is a deep multi-section analysis (~40 pages) covering every major domain with career timelines, Dasha predictions, Yoga/Dosha assessment, and full remedies.
- "Do I need a precise birth time?" -- Yes, especially for Brihat Kundli. Lagna (rising sign) changes approximately every 2 hours. An inaccurate Lagna can misattribute house lordships. Even a 15-minute precision greatly improves accuracy.
- "Is the PDF download included?" -- Yes. A formatted PDF of your complete Brihat Kundli report is included with the one-time purchase and available from your account forever.

**SEO:**
```
title:       "Brihat Kundli Pro -- 40-Page Vedic Life Report | Everyday Horoscope"
description: "The most comprehensive Vedic birth report. Career, love, wealth, health, Dasha timeline, Yogas, Doshas, and full remedies in a 40+ page PDF. ₹1,499 one-time."
url:         "https://www.everydayhoroscope.in/the-brihat-kundli"
JSON-LD:     FAQPage schema
```

---

## Group B -- Premium Tool Module Landings (4 pages)

These are interactive tool modules -- not static reports. Pages explain what the tool does, show a feature preview, and CTA to the tool page where auth/premium gate is handled. No price shown -- "Included in Premium" is the value prop.

### File locations
```
frontend/src/pages/kp/KrishnaOracleLandingPage.jsx
frontend/src/pages/palmistry/PalmistryLandingPage.jsx
frontend/src/pages/arc-angel/ArcAngelLandingPage.jsx
frontend/src/pages/rewards/RitualEngineLandingPage.jsx
```

### Routes to add in App.js (all public, no gate)
```jsx
<Route path="/the-krishna-oracle" element={<KrishnaOracleLandingPage />} />
<Route path="/the-palmistry"      element={<PalmistryLandingPage />} />
<Route path="/the-arc-angel"      element={<ArcAngelLandingPage />} />
<Route path="/the-ritual-engine"  element={<RitualEngineLandingPage />} />
```

---

### B-1 -- KP Oracle (Krishna Prashnavali) Landing Page
**File:** `frontend/src/pages/kp/KrishnaOracleLandingPage.jsx`  
**Route:** `/the-krishna-oracle`  
**CTA target:** `/krishna-prashnavali`

| Field | Value |
|---|---|
| Module name | Krishna Prashnavali Oracle |
| Badge | "Vedic Oracle · Premium" |
| Accent color | Amber (#d4a843) |
| Icon | `◉` |
| Hook headline | "Ask one question with complete sincerity. Krishna's grid will answer." |
| Subline | "An ancient Vedic oracle rooted in the Bhagavad Gita -- 324-cell grid, 36 sacred answers, and live astrological fingerprinting from your natal chart." |
| Primary CTA label | "Enter the Oracle" |
| Secondary CTA label | "How It Works" (smooth-scroll) |

**Feature cards (Section 2):**
| Title | Body |
|---|---|
| 18×18 Bhagavad Gita Grid | 324 cells drawn from Srimad Bhagavad Gita. Your selection is guided by sincere intent -- not by chance or random number. |
| Four Sacred Verdicts | YES (Pratibha) · WAIT (Dhairya) · NO (Pratrodha) · PRAY (Bhakti) -- each drawn from Lord Krishna's teachings and matched to a specific chaupai. |
| Live Dasha Fingerprinting | Unlike random oracles, every reading carries your Mahadasha and Antardasha overlay -- the planetary energy governing you at the exact moment of your question. |
| Planetary Transit Overlay | Current transits of major planets are factored into your reading context, deepening the astrological resonance of each answer. |
| Sacred Remedy per Reading | Each of the 36 answers carries its own module-specific sacred remedy and behavioural practice drawn from Lord Krishna's teachings. |
| KP Birth Chart Analysis | Built-in Krishnamurti Paddhati birth chart panel -- your full natal chart computed with Swiss Ephemeris to sub-degree precision. |

**How It Works (Section 3):**
1. "Form your question" -- hold your question clearly in mind. The more specific and sincere, the more precise the guidance. The oracle responds to intent.
2. "Select your cell on the grid" -- choose from the 18×18 Bhagavad Gita grid. Your live Dasha and transits are already overlaid on your chart at this moment.
3. "Receive your verdict and remedy" -- one of 36 canonical answers appears with a sacred chaupai, its meaning, and a personalised remedy for your situation.

**Sample section (Section 4):** Show a blurred oracle verdict card -- show the WAIT verdict badge and a partially visible chaupai text with gold overlay.

**FAQ (Section 5):**
- "What is Krishna Prashnavali?" -- Explain the tradition: rooted in Srimad Bhagavad Gita and Prashna Shastra, 18×18 grid maps to 36 canonical answers. Selection guided by intent, not chance.
- "How is this different from a regular online oracle?" -- Unlike random-number generators, EverydayHoroscope's KP Oracle overlays your live Vedic Dasha, planetary transits, and Yogas -- so every reading carries your actual astrological fingerprint.
- "What does PRAY mean as a verdict?" -- PRAY (Bhakti) = surrender and seek divine alignment before acting. It is not a negative verdict -- it signals that inner preparation and faith must precede action. The sacred remedy guides this process.

**SEO:**
```
title:       "Krishna Prashnavali Oracle -- Vedic Oracle Rooted in Bhagavad Gita | Everyday Horoscope"
description: "Ask the Krishna Prashnavali oracle your most sincere question. 324-cell Bhagavad Gita grid, 36 sacred answers, live Dasha fingerprinting, and sacred remedy for every reading."
url:         "https://www.everydayhoroscope.in/the-krishna-oracle"
JSON-LD:     FAQPage schema
```

---

### B-2 -- Palmistry (Hasta Rekha) Landing Page
**File:** `frontend/src/pages/palmistry/PalmistryLandingPage.jsx`  
**Route:** `/the-palmistry`  
**CTA target:** `/palmistry`

| Field | Value |
|---|---|
| Module name | Palmistry -- Hasta Rekha |
| Badge | "Vedic Palmistry · Premium" |
| Accent color | Terracotta (#c67444) |
| Icon | `◎` |
| Hook headline | "Your hand has been recording your life since birth. It's time to read what it says." |
| Subline | "A 12-question Vedic palmistry assessment -- palm shape, major lines, mounts, and finger type -- interpreted through Hasta Rekha tradition and AI analysis." |
| Primary CTA label | "Read My Palm" |
| Secondary CTA label | "What We Analyse" (smooth-scroll) |

**Feature cards (Section 2):**
| Title | Body |
|---|---|
| Palm Shape & Element Type | Earth, Air, Fire, or Water -- your hand's elemental type sets the foundation for your character and life approach. |
| Life, Heart & Head Lines | The three major lines analysed for length, depth, breaks, and forks -- each revealing vitality, emotional capacity, and intellectual style. |
| Fate Line Analysis | Present or absent, strong or faint -- the Fate Line reveals career destiny, stability, and the role of external forces in your path. |
| Mount Dominance | Which planetary mount is most prominent -- Jupiter, Saturn, Sun, Mercury, Venus, or Moon -- and what it reveals about your dominant drive. |
| Thumb Character | Long or short, flexible or stiff, waisted or straight -- the thumb is the single most revealing feature in Vedic palmistry. |
| Vedic Hasta Rekha Reading | A complete Hasta Rekha interpretation synthesising all 12 indicators into a coherent personalised reading in plain English. |

**How It Works (Section 3):**
1. "Answer 12 questions about your hand" -- no photo upload required. Questions cover palm shape, major lines, mounts, finger type, and thumb form.
2. "Hasta Rekha engine maps your signature" -- your answers are translated into a palmistry profile using classical Vedic Hasta Rekha principles.
3. "Receive your personalised reading" -- a complete interpretation of your hand's astrological signature, including strengths, challenges, and guidance.

**Sample section (Section 4):** Show a blurred palmistry reading card with section labels visible (Life Line, Heart Line, Fate Line) and a terracotta-toned overlay banner.

**FAQ (Section 5):**
- "Do I need to upload a photo of my palm?" -- No. The assessment uses a 12-question format about your hand's observable features -- no photo required, works on any device.
- "How accurate is palmistry?" -- Hasta Rekha (Vedic palmistry) is a centuries-old system of pattern recognition. Like all Vedic tools, it is a probabilistic guidance system -- not a deterministic prediction engine. Accuracy improves when answers are considered carefully.
- "Which hand should I read?" -- For right-handed individuals, the dominant right hand reveals your active path and chosen life; the left reveals your karmic potential and innate tendencies. The assessment prompts you to specify your dominant hand.

**SEO:**
```
title:       "Palmistry Reading -- Vedic Hasta Rekha Hand Analysis | Everyday Horoscope"
description: "A personalised Vedic palmistry reading. Answer 12 questions about your palm shape, major lines, mounts, and thumb type for a complete Hasta Rekha interpretation."
url:         "https://www.everydayhoroscope.in/the-palmistry"
JSON-LD:     FAQPage schema
```

---

### B-3 -- Arc Angel Landing Page
**File:** `frontend/src/pages/arc-angel/ArcAngelLandingPage.jsx`  
**Route:** `/the-arc-angel`  
**CTA target:** `/arc-angel`

| Field | Value |
|---|---|
| Module name | Arc Angel -- 12 Areas of Life |
| Badge | "Vedic Life Map · Premium" |
| Accent color | Teal (#2dd4bf) |
| Icon | `◌` |
| Hook headline | "12 areas of your life. Each one rated, timed, and ready for action." |
| Subline | "Arc Angel reads your Vedic birth chart across all 12 life domains -- with live Dasha timing and Questionnaire-enhanced precision for each area." |
| Primary CTA label | "Open My Life Map" |
| Secondary CTA label | "The 12 Domains" (smooth-scroll) |

**Feature cards (Section 2):**
| Title | Body |
|---|---|
| Health & Fitness | Your body's astrological constitution, vulnerability windows, and best practices based on the 1st and 6th houses. |
| Career & Finances | 10th house career strength, 2nd and 11th house wealth signals, and the current Dasha's professional influence. |
| Love & Family | 7th house partnership indicators, 5th house love potential, 4th house domestic harmony -- with timing overlays. |
| Spirituality & Purpose | 9th house dharma, 12th house moksha potential, and which planetary period is most spiritually active for you right now. |
| Live Dasha Timing | Each of the 12 domains is rated in context of your current Mahadasha and Antardasha -- not static, but live against your life calendar. |
| Questionnaire-Enhanced Precision | Complete the optional questionnaire to unlock deeper β/γ layer analysis -- the more you share, the more precisely Arc Angel reads you. |

**How It Works (Section 3):**
1. "Enter your birth details" -- date, time, and city. Log in to your EverydayHoroscope account to save your profile and unlock all 12 domains.
2. "Arc Angel computes your life map" -- all 12 domains rated from your Vedic chart with Dasha timing applied to each area.
3. "Review your personalised guidance" -- each domain shows a rating, current Dasha influence, and specific action guidance for this phase of your life.

**Sample section (Section 4):** Show a blurred 3-column domain grid with teal-toned domain tiles (Health, Career, Love visible but blurred) and a "Premium -- Unlock Full Map" overlay.

**FAQ (Section 5):**
- "What are the 12 life domains?" -- Health & Fitness, Career & Work, Finances, Intellectual Life, Emotional Life, Spirituality, Love & Relationships, Family Life, Social Life, Adventure & Travel, Environment, Creativity & Hobbies -- each mapped to a specific Vedic house.
- "How is Arc Angel different from a birth chart?" -- A birth chart gives you planetary positions. Arc Angel translates those positions into 12 rated action domains with live Dasha timing -- so you know not just what your chart says, but what to do about it right now.
- "Does it update as my Dasha changes?" -- Yes. Each time your Mahadasha or Antardasha transitions, the domain ratings and guidance update to reflect your new planetary period.

**SEO:**
```
title:       "Arc Angel -- Vedic 12 Areas of Life Analysis | Everyday Horoscope"
description: "Get a live Vedic reading across all 12 areas of your life -- health, career, love, finances, spirituality, family and more -- with Dasha timing for each domain."
url:         "https://www.everydayhoroscope.in/the-arc-angel"
JSON-LD:     FAQPage schema
```

---

### B-4 -- Ritual Engine Landing Page
**File:** `frontend/src/pages/rewards/RitualEngineLandingPage.jsx`  
**Route:** `/the-ritual-engine`  
**CTA target:** `/ritual-engine`

| Field | Value |
|---|---|
| Module name | Ritual Engine |
| Badge | "Vedic Remedies · Premium" |
| Accent color | Crimson (#dc2626) |
| Icon | `◈` |
| Hook headline | "Every planet has a remedy. Your chart has a protocol." |
| Subline | "A personalised Vedic ritual prescription engine -- planetary mantras, gemstones, fasting, and behavioural practices calibrated to your specific chart afflictions." |
| Primary CTA label | "Build My Ritual Protocol" |
| Secondary CTA label | "What It Prescribes" (smooth-scroll) |

**Feature cards (Section 2):**
| Title | Body |
|---|---|
| Planetary Affliction Scan | Identifies which planets in your chart are combust, debilitated, in enemy signs, or under low Shadbala -- the root causes of obstacles in each life domain. |
| Gemstone Protocol | Traditional Vedic gemstone recommendations matched to your chart's strongest benefic planets -- with correct metal, weight, and finger guidance. |
| Mantra & Puja Guidance | Planet-specific Vedic mantras, the correct count, timing, and devotional context for maximum efficacy. |
| Fasting Calendar | Auspicious fasting days derived from your chart's planetary dominants -- aligned to the Hindu calendar and your current Dasha. |
| Behavioural Remedies | Practical daily and weekly actions -- charitable acts, dietary adjustments, directional sleeping -- that reinforce your planetary remediation. |
| Knowledge Engine Personalisation | Powered by EverydayHoroscope's Knowledge Engine -- over 12,000 curated Vedic rules applied to your unique planetary signature. |

**How It Works (Section 3):**
1. "Your chart is scanned for afflictions" -- debilitated planets, combust planets, and Dosha indicators are identified across all 9 Vedic planets.
2. "Ritual protocol is assembled" -- gemstone, mantra, fasting, and behavioural remedies are selected from the Knowledge Engine and matched to your specific afflictions.
3. "Follow your personalised protocol" -- your remediation schedule is delivered in a structured, actionable format you can start immediately.

**Sample section (Section 4):** Show a blurred remedy card with a planet name (Saturn), a gemstone name (Blue Sapphire), and a mantra snippet partially visible -- with a crimson-toned premium overlay.

**FAQ (Section 5):**
- "What is the Ritual Engine?" -- It is a personalised Vedic remediation system that identifies the planetary afflictions in your birth chart and prescribes a specific set of traditional remedies -- mantras, gemstones, fasting, and actions -- to address them.
- "Are gemstone recommendations safe to follow?" -- Gemstone recommendations in Vedic astrology are based on strengthening specific planets. The Ritual Engine follows classical rules -- never recommending a Maraka planet's stone without context. When in doubt, start with mantras and fasting, which carry no risk.
- "How is this different from a generic remedies page?" -- Generic remedy pages list remedies for planets or signs. The Ritual Engine starts from YOUR specific chart -- which planets are afflicted, by how much, and in which houses -- and builds a protocol from that personalised data.

**SEO:**
```
title:       "Ritual Engine -- Personalised Vedic Remedies & Mantra Protocol | Everyday Horoscope"
description: "Get a personalised Vedic ritual protocol based on your birth chart -- gemstone recommendations, planetary mantras, fasting calendar, and behavioural remedies."
url:         "https://www.everydayhoroscope.in/the-ritual-engine"
JSON-LD:     FAQPage schema
```

---

## Group C -- Companion Module Landings (2 pages)

These are the spiritual companion and numerology modules -- broader in scope than single tools. Same landing page format.

### File locations
```
frontend/src/pages/lumina/LuminaLandingPage.jsx
frontend/src/pages/numerology/NumerologyLandingPage.jsx
```

### Routes to add in App.js (all public, no gate)
```jsx
<Route path="/the-lumina"     element={<LuminaLandingPage />} />
<Route path="/the-numerology" element={<NumerologyLandingPage />} />
```

---

### C-1 -- Lumina Spiritual Companion Landing Page
**File:** `frontend/src/pages/lumina/LuminaLandingPage.jsx`  
**Route:** `/the-lumina`  
**CTA target:** `/lumina`

| Field | Value |
|---|---|
| Module name | Lumina -- Spiritual Companion |
| Badge | "Multi-Faith Companion · Premium" |
| Accent color | Violet (#8b5cf6) |
| Icon | `✦` |
| Hook headline | "Scripture, manifestation, and sacred devotion -- in one consecrated space." |
| Subline | "Lumina is your daily spiritual companion -- Bible and Bhagavad Gita readings, manifestation confessions, devotion streaks, scripture-grounded AI chat, and a personal spiritual journal." |
| Primary CTA label | "Open Lumina" |
| Secondary CTA label | "What's Inside" (smooth-scroll) |

**Feature cards (Section 2):**
| Title | Body |
|---|---|
| Bible & Bhagavad Gita Reader | Read from the full Bible (66 books, all chapters) or all 18 chapters of the Bhagavad Gita -- multiple translations available for each. |
| Manifestation Confessions | Speak affirmations aligned to scripture -- Physical Healing, Marketplace Success, Mental Peace, and Spiritual Authority -- with repetition tracking. |
| Devotion Streaks & Rewards | Build daily practice streaks and earn devotion points redeemable for real-world rewards -- coffee coupons, gift cards, and gifted Premium months. |
| Scripture-Grounded AI Chat | Share what is on your heart. Lumina responds with scripture-anchored guidance from both Bhagavad Gita and the Bible -- never generic advice. |
| Spiritual Journal | Record your daily reflections, intentions, and scripture insights. Build a personal spiritual library over time. |
| Sacred Marketplace | Tools and resources for your spiritual journey -- curated, contextualised, and aligned to your current practice level. |

**How It Works (Section 3):**
1. "Choose your tradition" -- start with the Bible, Bhagavad Gita, or both. Lumina holds both with equal reverence.
2. "Build your practice" -- daily Scripture reading, manifestation confessions, devotion streaks, and journal entries accumulate into a living spiritual practice.
3. "Grow in community and wisdom" -- chat with the scripture-grounded AI, track your devotion milestones, and earn rewards for consistency.

**Sample section (Section 4):** Show blurred tabs: Home / Bible / Manifest / Devotion -- with a violet overlay "Premium -- Open Lumina".

**FAQ (Section 5):**
- "What makes Lumina different from a Bible app?" -- Lumina combines two traditions (Bible + Bhagavad Gita), adds AI-guided scripture chat that responds to your personal situation, and includes gamified devotion streaks and a manifestation framework -- a complete spiritual companion, not just a reader.
- "Which scriptures are supported?" -- The full Bible (KJV, NIV, ESV, NASB) and the complete 18-chapter Bhagavad Gita (Sivananda, Prabhupada, Gita Press). More traditions are planned.
- "Do I need to be religious to use Lumina?" -- No. Lumina is designed for anyone on a spiritual journey -- whether that is faith-based, philosophical, or focused purely on meditation and manifestation.

**SEO:**
```
title:       "Lumina -- Bible, Bhagavad Gita & Spiritual Companion App | Everyday Horoscope"
description: "Your daily spiritual companion. Bible and Bhagavad Gita readings, manifestation confessions, devotion streaks, scripture-grounded AI chat, and a personal spiritual journal."
url:         "https://www.everydayhoroscope.in/the-lumina"
JSON-LD:     FAQPage schema
```

---

### C-2 -- Numerology Landing Page
**File:** `frontend/src/pages/numerology/NumerologyLandingPage.jsx`  
**Route:** `/the-numerology`  
**CTA target:** `/numerology`

| Field | Value |
|---|---|
| Module name | Vedic Numerology |
| Badge | "11 Personalised Reports · Premium" |
| Accent color | Blue (#3b82f6) |
| Icon | `∞` |
| Hook headline | "Your name and birth date carry a frequency. Numerology decodes it." |
| Subline | "11 personalised Vedic numerology reports -- Life Path, Name Correction, Career Guidance, Relationship Compatibility, Karmic Debt, and more." |
| Primary CTA label | "Generate My Numerology Report" |
| Secondary CTA label | "All 11 Reports" (smooth-scroll) |

**Feature cards (Section 2):**
| Title | Body |
|---|---|
| Life Path & Soul Mission | Your core number derived from your birth date -- the foundational vibration that shapes your purpose, personality, and life trajectory. |
| Name Correction & Alignment | Is your current name in vibrational harmony with your birth number? Name Correction reveals misalignments and suggests aligned alternatives. |
| Karmic Debt & Lo Shu Grid | Which numbers are missing from your birth date? Missing numbers in the Lo Shu Grid reveal karmic patterns requiring conscious attention. |
| Relationship Compatibility | Numerological compatibility between two birth dates -- communication styles, life path harmony, and karmic intersection points. |
| Career Guidance & Timing | Favourable years, career number cycles, and the vibrational strengths most aligned to specific professional domains. |
| Premium Ankjyotish Report | The most advanced report -- combines Vedic numerology with your Lagna, Moon sign, and Nakshatra for a deeply personalised synthesis. |

**How It Works (Section 3):**
1. "Choose your report type" -- select from 11 report tiles based on what you want to understand. Most reports require only your birth name and date of birth.
2. "Enter your details" -- the Ankjyotish premium report also requires birth time and city for Lagna + Nakshatra computation.
3. "Receive your personalised numerology report" -- generated and saved to your account. Premium members unlock unlimited generation of all 11 types.

**Sample section (Section 4):** Show a blurred Life Path report card with a large number (e.g. "7") and partial reading visible -- blue overlay with "Premium -- Unlock Report".

**FAQ (Section 5):**
- "What is Vedic numerology?" -- Vedic numerology (Ankjyotish) derives meaning from Sanskrit letter values and the vibrational significance of numbers 1-9, rooted in Vedic tradition -- distinct from the Western Pythagorean system (A=1, B=2...) used in most numerology apps.
- "What is the difference between Pythagorean and Vedic numerology?" -- Pythagorean numerology assigns linear values to Latin alphabet letters. Vedic numerology uses Chaldean/Sanskrit letter values, places greater emphasis on birth name vibration alignment, and integrates Nakshatra and Lagna data in advanced analysis.
- "What is the Ankjyotish report?" -- The Premium Ankjyotish report is the most comprehensive -- it combines your Vedic numerology numbers with your Lagna (rising sign), Moon sign, and birth Nakshatra, creating a synthesis unique to your exact birth moment rather than just your date alone.

**SEO:**
```
title:       "Vedic Numerology Reports -- Life Path, Name, Career & More | Everyday Horoscope"
description: "Generate 11 personalised Vedic numerology reports. Life Path, Name Correction, Karmic Debt, Relationship Compatibility, Career Guidance and the advanced Ankjyotish synthesis."
url:         "https://www.everydayhoroscope.in/the-numerology"
JSON-LD:     FAQPage schema
```

---

## App.js -- All 9 Routes (complete block to add)

Add these imports at the top of `App.js` (lazy-loaded):

```jsx
// SEO-LP-1: Module landing pages
const BirthChartLandingPage    = lazy(() => import('./pages/kundali/BirthChartLandingPage'));
const KundaliMilanLandingPage  = lazy(() => import('./pages/kundali/KundaliMilanLandingPage'));
const BrihatKundliLandingPage  = lazy(() => import('./pages/kundali/BrihatKundliLandingPage'));
const KrishnaOracleLandingPage = lazy(() => import('./pages/kp/KrishnaOracleLandingPage'));
const PalmistryLandingPage     = lazy(() => import('./pages/palmistry/PalmistryLandingPage'));
const ArcAngelLandingPage      = lazy(() => import('./pages/arc-angel/ArcAngelLandingPage'));
const RitualEngineLandingPage  = lazy(() => import('./pages/rewards/RitualEngineLandingPage'));
const LuminaLandingPage        = lazy(() => import('./pages/lumina/LuminaLandingPage'));
const NumerologyLandingPage    = lazy(() => import('./pages/numerology/NumerologyLandingPage'));
```

Add these routes (all public, no wrapping gate component):

```jsx
{/* SEO-LP-1: Module SEO Landing Pages */}
<Route path="/the-birth-chart"     element={<BirthChartLandingPage />} />
<Route path="/the-kundali-milan"   element={<KundaliMilanLandingPage />} />
<Route path="/the-brihat-kundli"   element={<BrihatKundliLandingPage />} />
<Route path="/the-krishna-oracle"  element={<KrishnaOracleLandingPage />} />
<Route path="/the-palmistry"       element={<PalmistryLandingPage />} />
<Route path="/the-arc-angel"       element={<ArcAngelLandingPage />} />
<Route path="/the-ritual-engine"   element={<RitualEngineLandingPage />} />
<Route path="/the-lumina"          element={<LuminaLandingPage />} />
<Route path="/the-numerology"      element={<NumerologyLandingPage />} />
```

Place these routes in the public section of App.js, after the existing `/the-strategist` and `/the-tarot` routes for consistency.

---

## sitemap.xml -- 9 URLs to Add

Add these 9 entries to `frontend/public/sitemap.xml`:

```xml
<url><loc>https://www.everydayhoroscope.in/the-birth-chart</loc><changefreq>monthly</changefreq><lastmod>2026-06-08</lastmod></url>
<url><loc>https://www.everydayhoroscope.in/the-kundali-milan</loc><changefreq>monthly</changefreq><lastmod>2026-06-08</lastmod></url>
<url><loc>https://www.everydayhoroscope.in/the-brihat-kundli</loc><changefreq>monthly</changefreq><lastmod>2026-06-08</lastmod></url>
<url><loc>https://www.everydayhoroscope.in/the-krishna-oracle</loc><changefreq>monthly</changefreq><lastmod>2026-06-08</lastmod></url>
<url><loc>https://www.everydayhoroscope.in/the-palmistry</loc><changefreq>monthly</changefreq><lastmod>2026-06-08</lastmod></url>
<url><loc>https://www.everydayhoroscope.in/the-arc-angel</loc><changefreq>monthly</changefreq><lastmod>2026-06-08</lastmod></url>
<url><loc>https://www.everydayhoroscope.in/the-ritual-engine</loc><changefreq>monthly</changefreq><lastmod>2026-06-08</lastmod></url>
<url><loc>https://www.everydayhoroscope.in/the-lumina</loc><changefreq>monthly</changefreq><lastmod>2026-06-08</lastmod></url>
<url><loc>https://www.everydayhoroscope.in/the-numerology</loc><changefreq>monthly</changefreq><lastmod>2026-06-08</lastmod></url>
```

---

## Acceptance Criteria

- [ ] All 9 page files created in correct directories (see file paths above)
- [ ] All 9 routes added to `App.js` as public routes (no gate wrapper)
- [ ] All 9 lazy imports added to `App.js`
- [ ] Every page renders all 6 sections: Hero → Features → How It Works → Sample Preview → FAQ → CTA Banner
- [ ] `<SEO>` component with correct title, description, and canonical URL on every page
- [ ] `FAQPage` JSON-LD structured data on every page using the FAQ items specified above
- [ ] Group A pages (Birth Chart, Kundali Milan, Brihat Kundli) show price in hero badge
- [ ] Group B/C pages (modules) show "Included in Premium" or "Premium" badge -- no price
- [ ] CTAs on each page link to the correct target tool path (as specified per page above)
- [ ] `<Footer>` component included on every page
- [ ] Accent color per page used only for icons, badges, and CTA accents -- not as section backgrounds
- [ ] No console errors, no missing imports, no `undefined` props
- [ ] All 9 URLs added to `frontend/public/sitemap.xml`
- [ ] Build passes (`npm run build` with no errors)
- [ ] All code committed to `main`
