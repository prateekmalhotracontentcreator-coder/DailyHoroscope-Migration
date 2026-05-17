# Commission IR-4 -- 6 New Individual Reports (Phase 3 Natal Suite)

> EverydayHoroscope · Stack: FastAPI + React 18 + Tailwind CSS + MongoDB
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Live app: https://www.everydayhoroscope.in
> Issued: 2026-05-18
> Reference map: `Codex_Deliveries/Individual_Reports/IR_12_AREAS_OF_LIFE_MAP.md`

---

## Context & Objective

The Temple IR suite is built around Arc Angel's 12-area dashboard -- one deep-dive natal report per area of life. 6 of the 12 are already live. This commission delivers the remaining **6 natal reports** to complete the full suite.

**Already live (do NOT touch):**
| Report | Slug | Router |
|---|---|---|
| Life Cycles | `life-cycles` | `life_cycles_router.py` |
| Retrograde Survival | `retrograde-survival` | `retrograde_survival_router.py` |
| Lunar Cycle Wellness | `lunar-cycle` | `lunar_cycle_router.py` |
| Shadow Self | `shadow-self` | `shadow_self_router.py` |
| Career Blueprint | `career-blueprint` | `career_blueprint_router.py` |
| Karmic Debt | `karmic-debt` | `karmic_debt_router.py` |

**This commission builds (all 6 new):**
| Report | Slug | Vedic House |
|---|---|---|
| Wealth & Abundance Blueprint | `wealth-blueprint` | House 2 -- Dhana |
| Romance & Creative Intelligence | `romance-creative` | House 5 -- Putra |
| Vitality & Health Report | `vitality-health` | House 6 -- Ari |
| Partnership & Marriage Window | `partnership-window` | House 7 -- Kalatra |
| Dharma & Soul Purpose Report | `dharma-purpose` | House 9 -- Dharma |
| Gains & Network Activator | `gains-network` | House 11 -- Labha |

---

## Architecture Rules (Mandatory -- Read Before Writing Any Code)

1. **All 6 reports are natal-only** -- single birth chart input. No real-time transits, no second person.
2. **All computation via `vedic_calculator.py` + `vedic_shared_utils.py`** -- do NOT add duplicate dasha or chart functions.
3. **Pattern to follow:** `karmic_debt_router.py` + `karmic_debt_prompt_service.py` (the reference pair). Each new report = one router file + one prompt service file.
4. **Claude enrichment:** each router must call a prompt service using the `try_claude_generation()` pattern (see `karmic_debt_prompt_service.py`). If Claude is unavailable, fall back to deterministic content.
5. **Arc Angel hook:** every `generate` endpoint must call `await register_arc_angel_report_run(db, user_email, "{slug}")` after successful generation (imported from `knowledge_engine`).
6. **MongoDB:** use `get_report_collection(db, "{slug}")` for storage. Collections auto-created on first write.
7. **Do NOT modify** `vedic_shared_utils.py`, `vedic_calculator.py`, `knowledge_engine.py`, or any existing router.
8. **Frontend:** add all 6 new report cards to `REPORT_CONFIGS` in `IndividualReportsPage.jsx` (existing page at `/reports`). Do not create a new page.
9. **Public SEO landing pages:** 6 new landing pages following the shell pattern from `IR_LANDING_SHELL.jsx` / IR-1 pattern.

---

## Deliverables

### D1 -- 6 Backend Routers

One file per report in `backend/`:

| File | Prefix | Collection |
|---|---|---|
| `wealth_blueprint_router.py` | `/api/reports/wealth-blueprint` | `wealth_blueprint_reports` |
| `romance_creative_router.py` | `/api/reports/romance-creative` | `romance_creative_reports` |
| `vitality_health_router.py` | `/api/reports/vitality-health` | `vitality_health_reports` |
| `partnership_window_router.py` | `/api/reports/partnership-window` | `partnership_window_reports` |
| `dharma_purpose_router.py` | `/api/reports/dharma-purpose` | `dharma_purpose_reports` |
| `gains_network_router.py` | `/api/reports/gains-network` | `gains_network_reports` |

Each router must expose exactly:
- `POST /api/reports/{slug}/generate` -- generates and stores the report
- `GET /api/reports/{slug}/history` -- returns last 10 reports for the user

### D2 -- 6 Prompt Service Files

One file per report in `backend/`:

| File |
|---|
| `wealth_blueprint_prompt_service.py` |
| `romance_creative_prompt_service.py` |
| `vitality_health_prompt_service.py` |
| `partnership_window_prompt_service.py` |
| `dharma_purpose_prompt_service.py` |
| `gains_network_prompt_service.py` |

Each must follow the `try_claude_generation()` pattern from `karmic_debt_prompt_service.py`:
- Build a structured prompt from natal data
- Call Claude claude-sonnet-4-5 (or env var `KNOWLEDGE_ENGINE_CLAUDE_MODEL`)
- Return enriched content or deterministic fallback

### D3 -- server.py Registration

Add 6 import + `app.include_router()` lines in `backend/server.py`. Pattern (copy existing):
```python
from wealth_blueprint_router import router as wealth_blueprint_router
# ... (all 6)
app.include_router(wealth_blueprint_router)
# ... (all 6)
```

Do not change any existing router registrations.

### D4 -- Frontend: REPORT_CONFIGS entries (IndividualReportsPage.jsx)

Add 6 entries to the `REPORT_CONFIGS` array in `frontend/src/pages/reports/IndividualReportsPage.jsx`.

**Append after the existing 5 entries (do not reorder existing):**

```jsx
{
  type: "wealth_blueprint",
  slug: "wealth-blueprint",
  name: "Wealth & Abundance Blueprint",
  shortName: "Wealth Blueprint",
  color: "#c8930a",
  icon: "◈",
  hook: "See the wealth signals, abundance timing, and Dhana yogas written into your Vedic chart.",
  description: "A Vedic wealth reading for Dhana yogas, 2nd house strength, Jupiter/Venus influence, and key abundance windows.",
},
{
  type: "romance_creative",
  slug: "romance-creative",
  name: "Romance & Creative Intelligence",
  shortName: "Romance & Creativity",
  color: "#d4538a",
  icon: "✦",
  hook: "Unlock the romantic and creative intelligence wired into your 5th house.",
  description: "A Vedic reading for romantic timing, creative gifts, 5th lord strength, and the windows where both peak together.",
},
{
  type: "vitality_health",
  slug: "vitality-health",
  name: "Vitality & Health Report",
  shortName: "Vitality & Health",
  color: "#2a9d6f",
  icon: "⬡",
  hook: "Read the health rhythm your chart encodes and the periods that need the most care.",
  description: "A Vedic health reading for 6th house analysis, Mars/Saturn influence, vulnerable patterns, and daily rhythm guidance.",
},
{
  type: "partnership_window",
  slug: "partnership-window",
  name: "Partnership & Marriage Window",
  shortName: "Partnership Window",
  color: "#6b4fbd",
  icon: "◇",
  hook: "Find the Vedic marriage timing and see the partnership pattern your 7th house reveals.",
  description: "A Vedic partnership reading for Darakaraka, 7th lord, Upapada Lagna, and marriage/commitment dasha windows.",
},
{
  type: "dharma_purpose",
  slug: "dharma-purpose",
  name: "Dharma & Soul Purpose Report",
  shortName: "Dharma & Purpose",
  color: "#1e5fa8",
  icon: "☉",
  hook: "Trace the dharmic thread running through your chart to the purpose this life is asking you to fulfill.",
  description: "A Vedic dharma reading for 9th lord, Jupiter strength, Atmakaraka path, and the soul-level direction already written in your chart.",
},
{
  type: "gains_network",
  slug: "gains-network",
  name: "Gains & Network Activator",
  shortName: "Gains & Network",
  color: "#d46f22",
  icon: "◆",
  hook: "See the aspiration fulfillment windows and the social leverage points your 11th house encodes.",
  description: "A Vedic gains reading for 11th lord strength, Saturn's role in aspiration, key gains dasha windows, and network activation timing.",
},
```

Also update the `fetchReports` call to include all 6 new slugs in the history fetch (same pattern as existing 5).

### D5 -- Frontend: 6 Public SEO Landing Pages

**Files** in `frontend/src/pages/reports/landing/`:
```
WealthBlueprintLandingPage.jsx
RomanceCreativeLandingPage.jsx
VitalityHealthLandingPage.jsx
PartnershipWindowLandingPage.jsx
DharmaPurposeLandingPage.jsx
GainsNetworkLandingPage.jsx
```

**Pattern:** Follow the IR-1 landing page shell pattern exactly. Each page must have:
- Hero section with report name, hook, and CTA → `/reports`
- "What this report reveals" -- 4-5 bullet points specific to that report
- "Your Vedic foundation" -- house + key planets (report-specific)
- "Who this is for" -- 2-3 audience lines
- Testimonial placeholder block
- SEO `<title>` and meta description (use `SEO.jsx` component)
- CTA: "Generate My [Report Name] →" → `/reports`

**Routes in `App.js`:**
```jsx
<Route path="/wealth-blueprint-report"     element={<WealthBlueprintLandingPage />} />
<Route path="/romance-creative-report"     element={<RomanceCreativeLandingPage />} />
<Route path="/vitality-health-report"      element={<VitalityHealthLandingPage />} />
<Route path="/partnership-window-report"   element={<PartnershipWindowLandingPage />} />
<Route path="/dharma-purpose-report"       element={<DharmaPurposeLandingPage />} />
<Route path="/gains-network-report"        element={<GainsNetworkLandingPage />} />
```

All public (no auth required).

**`sitemap.xml` additions** -- append 6 URLs:
```xml
<url><loc>https://www.everydayhoroscope.in/wealth-blueprint-report</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
<url><loc>https://www.everydayhoroscope.in/romance-creative-report</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
<url><loc>https://www.everydayhoroscope.in/vitality-health-report</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
<url><loc>https://www.everydayhoroscope.in/partnership-window-report</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
<url><loc>https://www.everydayhoroscope.in/dharma-purpose-report</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
<url><loc>https://www.everydayhoroscope.in/gains-network-report</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
```

---

## Report-by-Report Vedic Spec

### Report 1 -- Wealth & Abundance Blueprint (`wealth-blueprint`)

**House:** 2 -- Dhana Bhava (Wealth, Values, Accumulation)

**Vedic Inputs (all from `vedic_calculator.py` + `vedic_shared_utils.py`):**
- 2nd house lord: sign, house placement, strength
- Dhana Yogas: check for Raja/Dhana yoga combinations (2nd/11th lord conjunction, Jupiter-2nd/11th connection, Venus-2nd connection)
- Jupiter placement: sign, house, aspect on 2nd house
- Venus placement: sign, house, aspect on 2nd/11th
- Current Mahadasha/Antardasha lord and its relationship to 2nd/11th house
- Upcoming dasha periods involving 2nd/11th lord or Jupiter/Venus

**Report Sections:**
1. **Your Wealth Foundation** -- 2nd lord analysis, Dhana yogas present, inherent chart wealth potential (strong/moderate/developing)
2. **Jupiter & Venus: Your Abundance Allies** -- their placement and influence on wealth accumulation
3. **Active Wealth Dasha Windows** -- current and upcoming dasha periods most favourable for financial growth (next 3-5 years)
4. **Wealth Activation Practices** -- remedies aligned to 2nd lord and Jupiter/Venus (mantra, colour, day)
5. **Key Insight** -- 1-paragraph synthesis of the chart's wealth story

**Deterministic fallback:** If Claude unavailable, return structured analysis of each section with plain Vedic logic.

---

### Report 2 -- Romance & Creative Intelligence (`romance-creative`)

**House:** 5 -- Putra Bhava (Romance, Creativity, Intelligence, Children)

**Vedic Inputs:**
- 5th house lord: sign, house, strength
- Putrakaraka (planet with 5th highest degrees after Atmakaraka/Amatyakaraka/etc.)
- Venus placement: sign, house, navamsha
- Sun placement: intelligence and self-expression signal
- 5th house occupants (planets in 5th)
- Current and upcoming dasha periods involving 5th lord, Venus, Sun

**Report Sections:**
1. **Your Creative Blueprint** -- 5th lord analysis, creative strengths encoded in the chart
2. **The Romantic Pattern** -- Venus + 5th house story; how you love and attract
3. **Intelligence & Gifts** -- Putrakaraka and Sun analysis; type of intelligence (analytical, creative, intuitive)
4. **Peak Romance & Creativity Windows** -- favourable dasha periods (next 3-5 years)
5. **Practices to Activate** -- remedies for 5th lord and Venus
6. **Key Insight** -- 1-paragraph synthesis

---

### Report 3 -- Vitality & Health Report (`vitality-health`)

**House:** 6 -- Ari Bhava (Health, Daily Discipline, Service)

**Vedic Inputs:**
- Ascendant (Lagna): body type and constitution indicator
- 6th house lord: sign, house, strength
- Mars placement: energy, inflammation patterns
- Saturn placement: chronic tendency, endurance, discipline
- Sun placement: vitality and immune signal
- Moon placement: emotional body, sleep pattern
- Planets in 6th house
- Current Mahadasha lord and its health implications

**Report Sections:**
1. **Your Vedic Constitution** -- Lagna-based body type and natural strengths/vulnerabilities
2. **The 6th House Story** -- 6th lord analysis; disease tendency patterns encoded
3. **Mars & Saturn: The Health Shapers** -- their placement and what it signals about energy, inflammation, chronic patterns
4. **Dasha Health Trajectory** -- current and upcoming dasha periods and their health implications (which periods need more care)
5. **Daily Rhythm Guidance** -- Ayurvedic-style daily practices aligned to the chart
6. **Remedies & Fortification** -- remedies for 6th lord, Mars, Saturn
7. **Key Insight** -- 1-paragraph synthesis

---

### Report 4 -- Partnership & Marriage Window (`partnership-window`)

**House:** 7 -- Kalatra Bhava (Partnerships, Marriage, Business Relations)

**Vedic Inputs:**
- 7th house lord: sign, house, strength, aspects
- Darakaraka: planet with lowest degrees (7th significator in Jaimini)
- Venus placement: sign, house, navamsha
- Upapada Lagna (UL): 12th from Arudha Lagna -- marriage manifestation point
- Planets in 7th house
- Current and upcoming dasha periods involving 7th lord, Darakaraka, Venus

**Report Sections:**
1. **Your Partnership Blueprint** -- 7th lord analysis; the kind of partner and relationship your chart calls for
2. **Darakaraka: Your Soul's Partner Signal** -- the planet that describes your life partner's qualities
3. **Venus in Your Chart** -- love language, attraction pattern, relationship style
4. **Upapada Lagna** -- the manifestation point of marriage; its strength and implications
5. **Marriage & Commitment Windows** -- favourable dasha periods for partnership/marriage (next 5 years); periods requiring patience
6. **Remedies for Partnership Alignment** -- aligned to 7th lord, Venus, Darakaraka
7. **Key Insight** -- 1-paragraph synthesis

---

### Report 5 -- Dharma & Soul Purpose Report (`dharma-purpose`)

**House:** 9 -- Dharma Bhava (Higher Purpose, Wisdom, Guru, Past-Life Blessings)

**Vedic Inputs:**
- 9th house lord: sign, house, strength
- Jupiter placement: sign, house, aspects (natural ruler of dharma)
- Atmakaraka: planet with highest degrees -- the soul's signifier
- Atmakaraka's navamsha placement (Swamsha) for deeper soul purpose
- Planets in 9th house
- Current and upcoming dasha periods involving 9th lord, Jupiter, Atmakaraka

**Report Sections:**
1. **Your Dharmic Foundation** -- 9th lord analysis; the life path and higher purpose encoded
2. **Jupiter: Your Wisdom Anchor** -- Jupiter's placement and its dharmic guidance for this life
3. **Atmakaraka: Soul's Calling** -- the planet that governs the soul's primary lesson and direction
4. **Past-Life Blessings** -- 9th house occupants and what they bring forward from prior lifetimes
5. **Dharma Activation Windows** -- dasha periods when the soul's purpose becomes most alive and accessible
6. **Practices to Honour Your Path** -- remedies aligned to 9th lord, Jupiter, Atmakaraka
7. **Key Insight** -- 1-paragraph synthesis

---

### Report 6 -- Gains & Network Activator (`gains-network`)

**House:** 11 -- Labha Bhava (Gains, Aspirations, Social Network, Elder Siblings)

**Vedic Inputs:**
- 11th house lord: sign, house, strength
- Saturn placement: natural ruler of H11; gains through discipline and network
- Planets in 11th house (each adds a distinct gains channel)
- 11th lord's relationship to Ascendant lord (mutual support = enhanced gains)
- Current and upcoming dasha periods involving 11th lord, Saturn, or planets in 11th

**Report Sections:**
1. **Your Gains Blueprint** -- 11th lord analysis; the channels through which abundance flows most naturally
2. **Saturn's Role in Your Network** -- Saturn's placement and how discipline and persistence unlock your aspirations
3. **Active Gains Channels** -- planets in 11th house and what each one activates (friends, profession, creativity, etc.)
4. **Aspiration Fulfillment Windows** -- dasha periods most aligned to manifesting goals (next 3-5 years)
5. **Network Activation Guidance** -- practical Vedic guidance on which relationships and networks to cultivate
6. **Remedies for Gains** -- remedies aligned to 11th lord and Saturn
7. **Key Insight** -- 1-paragraph synthesis

---

## Backend Router Contract (Applies to All 6)

Each router must match this exact contract:

### Imports
```python
from __future__ import annotations
from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field
from knowledge_engine import register_arc_angel_report_run
from {slug_snake}_prompt_service import enrich_{slug_snake}_with_claude
from vedic_shared_utils import (
    atmakaraka_planet,
    build_natal_snapshot,
    build_report_document,
    get_db,
    get_report_collection,
    get_user_email,
    house_topic,
    truncate_text,
    truncate_words,
)
```

### Models
```python
class BirthInput(StrictModel):
    date: str          # "YYYY-MM-DD"
    time: str          # "HH:MM"
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city_name: str | None = None

class GenerateResponse(StrictModel):
    report_id: str
    report_type: str   # = "{slug}"
    generated_at: str
    # + report-specific fields (sections 1-N as strings)

class HistoryResponse(StrictModel):
    reports: list[GenerateResponse]
```

### Endpoints
```python
@router.post("/generate", response_model=GenerateResponse)
async def generate_{slug_snake}_report(payload: BirthInput, request: Request):
    db = get_db(request)
    user_email = await get_user_email(request, db)
    # 1. Build natal snapshot via vedic_shared_utils
    # 2. Run deterministic Vedic analysis
    # 3. Enrich with Claude via prompt service (try_claude_generation pattern)
    # 4. Store in MongoDB via build_report_document + get_report_collection
    # 5. Register Arc Angel hook:
    await register_arc_angel_report_run(db, user_email, "{slug}")
    return report

@router.get("/history", response_model=HistoryResponse)
async def get_{slug_snake}_history(request: Request):
    db = get_db(request)
    user_email = await get_user_email(request, db)
    collection = get_report_collection(db, "{collection_name}")
    # Return last 10 reports for user_email
```

---

## Acceptance Criteria

CC will verify each of the following before integration:

### Backend (per report × 6)
- [ ] `python3 -m py_compile backend/{name}_router.py backend/{name}_prompt_service.py` -- 0 errors
- [ ] `POST /api/reports/{slug}/generate` returns 200 with all required section fields populated
- [ ] `GET /api/reports/{slug}/history` returns 200 with `reports` list
- [ ] Arc Angel `register_arc_angel_report_run` called on generate
- [ ] Claude fallback: if prompt service fails, deterministic content returned (no 500)
- [ ] No functions duplicated from `vedic_shared_utils.py` or `vedic_calculator.py`

### server.py
- [ ] All 6 routers imported and registered with `app.include_router()`
- [ ] No existing router registrations changed

### Frontend
- [ ] `REPORT_CONFIGS` in `IndividualReportsPage.jsx` has all 11 entries (5 existing + 6 new)
- [ ] Report history fetch includes all 6 new slugs
- [ ] `npm run build` (or `npx craco build`) exits 0 -- no type errors or missing imports
- [ ] 6 new landing pages render with correct content and CTA links to `/reports`
- [ ] 6 new routes in `App.js` -- all public (no auth wrapper)
- [ ] `sitemap.xml` includes 6 new URLs

---

## Files to Deliver

**Backend (12 new files):**
```
backend/wealth_blueprint_router.py
backend/wealth_blueprint_prompt_service.py
backend/romance_creative_router.py
backend/romance_creative_prompt_service.py
backend/vitality_health_router.py
backend/vitality_health_prompt_service.py
backend/partnership_window_router.py
backend/partnership_window_prompt_service.py
backend/dharma_purpose_router.py
backend/dharma_purpose_prompt_service.py
backend/gains_network_router.py
backend/gains_network_prompt_service.py
```

**Modified files:**
```
backend/server.py          -- 6 new import + include_router lines only
frontend/src/App.js        -- 6 new public routes only
frontend/src/pages/reports/IndividualReportsPage.jsx  -- REPORT_CONFIGS + history fetch
frontend/public/sitemap.xml -- 6 new <url> entries
```

**Frontend landing pages (6 new files):**
```
frontend/src/pages/reports/landing/WealthBlueprintLandingPage.jsx
frontend/src/pages/reports/landing/RomanceCreativeLandingPage.jsx
frontend/src/pages/reports/landing/VitalityHealthLandingPage.jsx
frontend/src/pages/reports/landing/PartnershipWindowLandingPage.jsx
frontend/src/pages/reports/landing/DharmaPurposeLandingPage.jsx
frontend/src/pages/reports/landing/GainsNetworkLandingPage.jsx
```

**Total: 18 new files + 4 modified files**

---

## What to NOT Change

- `vedic_shared_utils.py` -- shared utility layer, immutable
- `vedic_calculator.py` -- core computation engine, immutable
- `knowledge_engine.py` -- interpretation layer, immutable (only import from it)
- Any existing router or prompt service file
- `IndividualReportsPage.jsx` styling, layout, generation logic -- only add to `REPORT_CONFIGS` and extend the history fetch

---

## Reference Files (Read These First)

Before writing any code, read these existing files in the repo:

| File | What to Learn |
|---|---|
| `backend/karmic_debt_router.py` | Exact router pattern: imports, models, endpoints, Arc Angel hook |
| `backend/karmic_debt_prompt_service.py` | Prompt service pattern: `try_claude_generation()`, structured prompt, fallback |
| `backend/vedic_shared_utils.py` | All available helper functions -- use these, don't recreate |
| `frontend/src/pages/reports/IndividualReportsPage.jsx` | `REPORT_CONFIGS` structure + `fetchReports` pattern |
| `frontend/src/pages/reports/landing/KarmicDebtLandingPage.jsx` | Landing page shell + SEO component usage |

---

*Commission IR-4 -- EverydayHoroscope · Prepared 2026-05-18*
