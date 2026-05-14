# EverydayHoroscope — Contract Appointment Note
## New Workstream: Individual Reports + Lagna Kundali Module

> **Issued by:** Temple Team
> **Date:** 30 March 2026
> **To:** CODEX
> **Supersedes:** Initial Conversation with CODEX re the New Contracts.rtf (exploratory only)
> **Governing reference:** `CODEX_WAYS_OF_WORKING.md` applies in full to all contracts below

---

## Part 1 — Governing Decisions: All 11 CODEX Discrepancies Resolved

CODEX raised 11 discrepancy questions before proceeding. All are answered definitively here. These answers are binding for the entire Individual Reports workstream.

---

### D1 — Vedic vs Western system scope

**Decision: Vedic-first only. No external astrology API approved.**

All report computation must use `pyswisseph 2.10.x` with Lahiri ayanamsa (sidereal), consistent with every prior Temple contract. The live `vedic_calculator.py` is the approved natal computation source. No third-party transit or synastry API is approved for Temple delivery at this stage.

Western concepts referenced in the source note (tropical transits, synastry, etc.) may appear in report interpretation language but all underlying computation must remain pyswisseph-based and Vedic-sidereal.

---

### D2 — Audio/Video analysis and NotebookLM-style flows

**Decision: Deferred entirely. Platform exploration only. Not a Temple contract at any stage of this workstream.**

The unofficial GitHub automation wrappers referenced in the source note are not acceptable for Temple delivery. Audio/video analysis introduces compute, dependency, and safety profiles that are outside the current Temple contract. This category stays in platform/master architecture only until separately scoped and explicitly approved by Temple Team.

---

### D3 — "Ask 1 Question" scope

**Decision: Narrowed into fixed deterministic report tiles only.**

"Ask 1 Question" as an open-ended oracle/chat feature is not a Temple contract. It will drift into a generalized Q&A product that does not fit the one-standalone-router-per-report pattern.

If CODEX delivers this concept, it must be scoped as a small set of fixed-category tiles with deterministic logic triggers — for example, `career_question`, `love_question`, `family_question`. Each tile maps to specific natal house and planet combinations with bounded output. This is deferred to Phase 2 after the core natal report suite is proven.

---

### D4 — Trigger engines, daily scores, and push alert lifecycle ideas

**Decision: Platform architecture only. Temple delivery = report generation endpoint only.**

Recurring calculation, scheduling, alerts, encounter window notifications, "love battery" scores, and ritual trigger moments are all valuable product concepts but they are outside the Temple delivery contract. All scheduling, notification dispatch, and lifecycle orchestration live in `server.py` on the Temple side (APScheduler pattern established in existing admin module).

CODEX delivers: `POST /api/reports/{report-slug}/generate` — a single report generation endpoint per contract.

Temple Team wires: all scheduling, triggers, notifications, and lifecycle UI.

---

### D5 — Transit-based reports and data freshness

**Decision: Natal-only reports in Phase 1. Transit-based reports approved for Phase 2, powered by pyswisseph.**

Phase 1 contracts must be natal-chart-only. This means all computation is based on the user's fixed birth data. No real-time or rolling planetary data required.

Phase 2 (after Phase 1 is delivered and validated) will unlock transit-based reports. When that happens, transit computation will use `swe.calc_ut()` with the current date (no external API), consistent with how panchang_router.py already handles real-time positions.

---

### D6 — Synastry and second-person birth data

**Decision: Deferred to Phase 3. Not in first or second wave.**

Single-user reports only for Phase 1 and Phase 2. Deep Synastry: Soul Connection requires a second user's birth data, which introduces storage, consent, and retention questions that are not resolved in the current Temple contract. This is preserved as a Phase 3 contract and will be separately scoped when ready.

---

### D7 — Remedies — scope and tone

**Decision: Approved. Framed as supportive spiritual guidance only. No outcome guarantees.**

Remedies are a strong Vedic differentiator and are explicitly approved for Temple-facing reports. The approved scope for Phase 1:
- **Mantras** (Sanskrit with transliteration, suggested chanting day/count)
- **Gemstones** (cosmic ally framing, "may amplify" language)
- **Rituals** (action-oriented, tied to specific planetary timing)
- **Vastu** (directional/spatial, framed as environmental alignment)

**Approved tone model:** "During this period, the following practices may help you align with supportive energies..."

**Not acceptable:** Guaranteed outcomes, deterministic promises ("you will meet someone"), medical or health claims, or any language that implies the remedy will override free will.

---

### D8 — Sexual Vitality & Peak Forecast

**Decision: Reframed and deferred to Phase 2 as "Intimacy & Vitality Forecast."**

The raw "Sexual Vitality" framing is too direct for the first contract wave and risks tone, trust, and platform safety issues. However, the underlying astrological logic (8th house, Mars/Venus transits, Rahu influence) is sound and commercially strong.

It will be delivered in Phase 2 under the name **"Intimacy & Vitality Forecast"** with framing centred on energy, passion, confidence, and romantic connection — not explicit sexual prediction. Output constraints will be defined before that contract is scoped.

---

### D9 — Collection naming for Individual Reports workstream

**Decision: One shared collection `individual_reports`. One document per generated report. `report_type` field differentiates.**

All individual report artifacts across this workstream write to a single primary collection: **`individual_reports`**.

Each document must include:
```json
{
  "id": "uuid",
  "report_type": "karmic_debt",
  "user_email": "user@example.com",
  "input": { /* birth data used */ },
  "output": { /* structured report sections */ },
  "generated_at": "iso-8601-utc"
}
```

Do not create separate collections per report type. Do not write to any other Temple collection.

---

### D10 — Route prefix convention for Individual Reports

**Decision: Grouped family under `/api/reports/`. One router file per report.**

All individual report artifacts share the `/api/reports/` namespace. Each report gets its own standalone router file and its own sub-path:

| Report | File | Route |
|---|---|---|
| Karmic Debt | `karmic_debt_router.py` | `/api/reports/karmic-debt` |
| Career Blueprint | `career_blueprint_router.py` | `/api/reports/career-blueprint` |
| Shadow Self | `shadow_self_router.py` | `/api/reports/shadow-self` |
| Retrograde Survival | `retrograde_survival_router.py` | `/api/reports/retrograde-survival` |
| Life Cycles (Dasha) | `life_cycles_router.py` | `/api/reports/life-cycles` |
| Future reports | `{report}_router.py` | `/api/reports/{report-slug}` |

Each router file is a standalone `APIRouter` with prefix `/api/reports/{slug}`. Same delivery shape as Tarot and Numerology. Each router registers at minimum:

```
POST /api/reports/{slug}/generate   — generate and save one report
GET  /api/reports/{slug}/history    — fetch saved reports for the logged-in user
```

---

### D11 — Platform vs Temple delivery boundary

**Decision: Confirmed. Temple delivery is a packaging and runtime contract. Rich platform concepts are preserved but must not become assumed Temple requirements.**

The following categories from the source note are explicitly classified as **platform/master architecture only** and are NOT Temple contracts unless separately scoped:
- Audio/video analysis
- NotebookLM-style synthesis
- Push-trigger engines and notification scheduling
- Broader multimodal coaching flows
- Cross-report orchestration
- "Love Battery" daily score as a persistent live feature
- Blended system intelligence without explicit approval

CODEX should preserve these ideas in platform documentation but must not build them into Temple delivery artifacts or assume Temple Team has approved them by virtue of their presence in the source brief.

---

## Part 2 — Contract Prioritization

### Phase 1 — Natal-Only Individual Reports (Priority order)

| Priority | Contract | File | Collection | Notes |
|---|---|---|---|---|
| **1** | Karmic Debt & Past Life Report | `karmic_debt_router.py` | `individual_reports` | Highest Vedic differentiation |
| **2** | Career & Success Blueprint | `career_blueprint_router.py` | `individual_reports` | Strong monetization, broad appeal |
| **3** | Shadow Self & Hidden Qualities | `shadow_self_router.py` | `individual_reports` | Nakshatra-based, deep self-discovery hook |
| **4** | Retrograde Survival Guide | `retrograde_survival_router.py` | `individual_reports` | Episodic — triggered by current retrograde status |
| **5** | The Pattern of Life Cycles | `life_cycles_router.py` | `individual_reports` | Vimshottari Dasha — long-arc life chapter report |

**Deliver in sequence.** Contract 1 (Karmic Debt) is the first deliverable. Do not begin Contract 2 until Contract 1 is validated and confirmed by Temple Team.

---

### Phase 2 — Transit-Based Reports (After Phase 1 validated)

| Priority | Contract | File | Notes |
|---|---|---|---|
| 6 | Encounter Window | `encounter_window_router.py` | Venus/Jupiter transits to 5th/7th house |
| 7 | Seasonal Love Weather | `seasonal_love_router.py` | 90-day transit aggregation |
| 8 | Lunar Cycle Wellness & Rituals | `lunar_cycle_router.py` | Moon phase × natal Moon |
| 9 | Date-Night Score | `date_night_router.py` | Daily Moon×Venus angle (micro-forecast) |
| 10 | Intimacy & Vitality Forecast | `intimacy_vitality_router.py` | Reframed from "Sexual Vitality" — see D8 above |

Temple Team will issue a separate Phase 2 Contract Appointment when Phase 1 delivery is complete.

---

### Phase 3 — Two-Person and Deferred Reports (Future scoping)

| Contract | Notes |
|---|---|
| Deep Synastry: Soul Connection | Requires two birth datasets — separate consent/storage design needed |
| Digital Dating Strategy Report | Mercury/Venus natal analysis — lower priority |
| Ask 1 Question (fixed tiles) | Narrowed tile concept — separately scoped |

---

### Platform-Only (Not a Temple Contract)

| Concept | Status |
|---|---|
| Audio/video analysis | Deferred indefinitely |
| NotebookLM-style synthesis | Deferred indefinitely |
| Push trigger engine / love battery | Platform architecture only |
| Multimodal coaching | Not scoped |

---

## Part 3 — Contract 8A: Lagna Kundali Module

This is a **separate and parallel contract** to the Individual Reports workstream. It is designated Contract 8A as it is an enhancement to the existing Kundali module, not a new individual report.

### Background

The backend `vedic_calculator.py` already computes the full Vedic birth chart (planet positions, houses, nakshatras, Vimshottari Dasha, Navamsa). It is not currently exposed via a public API. A frontend placeholder page (`KundaliPage.jsx`) exists but is not wired to live backend data.

A full contract specification is in `.claude/CODEX_LAGNA_KUNDLI_CONTRACT.md` in the repository. CODEX must read that file as the primary spec.

### Drik Panchang Reference (Screenshots Provided)

The screenshots provided by Temple Team from `drikpanchang.com/jyotisha/kundali/kundali.html` show the target reference UI:

- **Chart layout:** North Indian diamond format, D1 (Rashi) chart + D9 (Navamsha) chart side by side
- **Graha Details tab:** Table with Longitude, Nakshatra, Nakshatra Lord, Nakshatra Sub-Lord — for both Rashi and Navamsha charts
- **Bhava Chalit Details tab:** Table with Bhava number, Residents (planets), Owner (lord), Rashi, Qualities (Cardinal/Fixed/Mutable), Aspected By
- **Divisional chart selector:** Dropdown showing BC (Bhav Chalit), D1 through D60 (including D2-Hora, D3-Drekkana, D4, D5, D6, D7, D8, D9-Navamsha, D10-Dashamsha, D11, D12, D16, D20, D24, D27, D30, D40, D45, D60)

### Scope for Contract 8A (Phase 1 — Core Delivery)

**Backend:** New file `kundali_router.py`
- `POST /api/kundali/compute` — full chart calculation from birth details
- `GET /api/kundali/lagna-now` — current Lagna for a location slug (for Panchang integration)
- `POST /api/kundali/save` — save chart for authenticated user
- `GET /api/kundali/my-charts` — retrieve saved charts

**Frontend:** Replacement `KundaliPage.jsx` with:
- Birth details input form (date, time, city from 91-city list + free-text fallback)
- North Indian Diamond chart SVG (pure React SVG, `NorthIndianChart` component)
- Graha (Planet) Details table — Longitude, Nakshatra, Nakshatra Lord/Sub-Lord
- Bhava Chalit Details table — House, Residents, Owner, Rashi, Qualities, Aspected By
- Navamsa (D9) chart toggle
- Vimshottari Dasha timeline (current Maha + Antar Dasha visual bar)
- Save and Share buttons

**Divisional Charts (D1–D60):** Include the chart type selector dropdown as seen in the Drik Panchang reference. **Phase 1 scope: D1 (Rashi) and D9 (Navamsha) only.** The selector UI may be included with a "Coming Soon" state for D2–D60 to signal the roadmap — or omitted entirely and added in Phase 2. CODEX recommendation welcome.

### Scope Exclusions for Contract 8A

- No `synastry` or second-person data in this contract
- No `Ashtakoot` compatibility in this contract (already live in `vedic_calculator.py` via existing routes)
- No individual prediction reports (those are the Individual Reports workstream above)
- The Lagna Now endpoint is for Panchang integration only — do not build a separate Panchang-facing page

### Technical Constraints (same as all Temple contracts)

- `from __future__ import annotations` at top
- `timezone.utc` — never `datetime.UTC`
- Pydantic v2 with `ConfigDict`
- `request.app.state.db` and `request.state.user.get("email")`
- Python 3.12, no new Python dependencies unless essential
- MongoDB collection: `kundali_charts`
- No imports from Temple source files

### Acceptance Criteria

- Birth chart computes correctly for test case: **15 June 1990, 14:30, Mumbai → Lagna = Tula (Libra) ≈ 14°**
- All 9 grahas + Rahu/Ketu shown in correct houses
- Vimshottari Dasha dates match standard Vedic calculation
- Chart SVG renders without distortion at 320px and 800px width
- Graha Details and Bhava Chalit tables match Drik Panchang reference values for the same birth input
- Page loads in < 3 seconds (chart computation < 500ms backend)
- Works on iOS Safari and Chrome Android

---

## Part 4 — Individual Report Specifications (Phase 1)

### Contract 9-A: Karmic Debt & Past Life Report

**File:** `karmic_debt_router.py`
**Route prefix:** `/api/reports/karmic-debt`
**Collection:** `individual_reports` (with `report_type: "karmic_debt"`)

**Input (POST /api/reports/karmic-debt/generate):**
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

**Deterministic Logic Triggers (pyswisseph, Lahiri ayanamsa):**
- Identify all retrograde planets at birth (any planet with negative daily motion at birth datetime)
- Identify Saturn's natal house position
- Identify Rahu and Ketu natal house positions
- Trigger "unresolved lessons" when: Saturn or Rahu/Ketu occupy the 4th, 8th, or 12th house
- Identify Atmakaraka: the planet at the highest degree in the natal chart (excluding Rahu/Ketu)

**Output Sections:**
```json
{
  "report_type": "karmic_debt",
  "karmic_indicators": {
    "retrograde_planets": ["Saturn", "Mercury"],
    "saturn_house": 8,
    "rahu_house": 12,
    "ketu_house": 6,
    "atmakaraka": "Jupiter",
    "atmakaraka_degree": 27.43,
    "debt_activated": true
  },
  "report": {
    "headline": "string (max 15 words)",
    "karmic_theme": "string (max 60 words — primary life lesson identified from Saturn/Node placement)",
    "past_life_echo": "string (max 60 words — pattern being repeated, sourced from 8th/12th house activations)",
    "atmakaraka_insight": "string (max 50 words — soul's deepest desire/driver)",
    "retrograde_lessons": [
      { "planet": "Saturn", "lesson": "string (max 40 words)" }
    ],
    "breaking_the_cycle": "string (max 60 words — path forward)",
    "remedies": {
      "mantra": { "text": "string", "transliteration": "string", "practice": "string (when/how)" },
      "gemstone": { "stone": "string", "purpose": "string (max 20 words)" },
      "ritual": "string (max 40 words)"
    }
  }
}
```

**Output Constraints:**
- All text fields follow the character limits above
- No deterministic guarantees ("you will", "this means you definitely")
- No medical, legal, or financial claims
- Remedies framed as "may help align" or "supportive practice" — never guaranteed outcomes
- Karmic language stays spiritual/philosophical — not fatalistic

**Trust & Safety Notes:**
- "Past Life" framing is metaphorical/spiritual — never claim literal reincarnation as fact
- "Karmic Debt" must be framed as patterns to grow through, not punishment
- Do not predict death, major illness, or irreversible events

---

### Contract 9-B: Career & Success Blueprint

**File:** `career_blueprint_router.py`
**Route prefix:** `/api/reports/career-blueprint`
**Collection:** `individual_reports` (with `report_type: "career_blueprint"`)

**Deterministic Logic Triggers:**
- Compute Midheaven (MC = 10th house cusp) degree and sign
- Identify 10th house lord and its natal house placement
- Identify planets in or aspecting the 10th house
- Identify 6th house lord (work/service) and 2nd house lord (wealth/income)
- Check if Jupiter or Saturn occupy or aspect the 10th house (amplifiers)

**Output Sections:**
- `career_archetype` — Professional identity from 10th house sign (max 40 words)
- `natural_strengths` — Planets in/aspecting 10th house (max 60 words)
- `success_formula` — MC sign + lord interpretation (max 60 words)
- `wealth_signature` — 2nd house analysis (max 50 words)
- `peak_periods` — Maha Dasha periods favourable for career (list of up to 3 planetary periods with brief description)
- `action_guidance` — Specific, actionable career direction (max 60 words)
- `remedies` — Same structure as Karmic Debt report above

---

### Contract 9-C: Shadow Self & Hidden Qualities

**File:** `shadow_self_router.py`
**Route prefix:** `/api/reports/shadow-self`
**Collection:** `individual_reports` (with `report_type: "shadow_self"`)

**Deterministic Logic Triggers:**
- Compute Janma Nakshatra (birth Nakshatra = Moon's natal Nakshatra)
- Identify the "shadow Nakshatra" — the Nakshatra 7 positions from Janma (traditional Vedic shadow cycle)
- Identify 12th house lord and any planets in the 12th (the unconscious/hidden)
- Identify Atmakaraka (highest-degree planet) for soul-driver interpretation
- Check for planets in debilitation or in enemy signs (shadow energy amplifiers)

**Output Sections:**
- `janma_nakshatra` — Birth Nakshatra name + known qualities (max 40 words)
- `shadow_nakshatra` — The hidden counterpart and what it reveals (max 50 words)
- `hidden_strengths` — Unrealised talents from 12th house analysis (max 50 words)
- `blind_spots` — Patterns driven by Atmakaraka tension (max 50 words)
- `psychological_driver` — Debilitated or enemy-sign planets as suppressed energies (max 50 words)
- `integration_path` — How to work with (not against) shadow tendencies (max 60 words)
- `remedies` — Same structure as above

---

### Contract 9-D: Retrograde Survival Guide

**File:** `retrograde_survival_router.py`
**Route prefix:** `/api/reports/retrograde-survival`
**Collection:** `individual_reports` (with `report_type: "retrograde_survival"`)

**Special note on data inputs:** This report has two modes:
1. **Personal mode** — generates based on user's natal chart + current date (which retrogrades are active now and how they affect THIS user's natal houses)
2. **General mode** — generates for a specific retrograde planet without birth data (general survival guide)

Phase 1 delivers both modes in one router. The `generate` endpoint accepts optional birth data; if absent, returns a general guide.

**Deterministic Logic Triggers:**
- Compute which of Mercury, Venus, Mars are currently retrograde on the requested date (using `swe.calc_ut()`)
- If natal data provided: identify which natal houses the retrograde planet is transiting
- Map the natal house to the life area affected (1st = identity, 5th = romance, 7th = partnerships, etc.)

**Output Sections:**
- `active_retrogrades` — List of currently retrograde planets with start/end dates
- Per retrograde planet:
  - `transit_house` — House affected for this user (if natal data provided)
  - `life_area` — Plain-language area of life (max 20 words)
  - `what_to_expect` — What this retrograde typically activates (max 50 words)
  - `navigation_tips` — 3 concrete tips for this retrograde period (bullet list, each max 20 words)
  - `what_to_avoid` — 2-3 specific cautions (bullet list, each max 20 words)
  - `remedies` — Retrograde-specific remedy (mantra/gemstone/ritual, same structure)

---

### Contract 9-E: The Pattern of Life Cycles

**File:** `life_cycles_router.py`
**Route prefix:** `/api/reports/life-cycles`
**Collection:** `individual_reports` (with `report_type: "life_cycles"`)

**Deterministic Logic Triggers:**
- Compute full Vimshottari Dasha sequence from birth Moon's Nakshatra
- Identify current Maha Dasha (major period) and Antar Dasha (sub-period)
- Identify the planetary nature of both (benefic/malefic, active houses ruled)
- Look ahead to next 3 Maha Dasha transitions with dates

**Output Sections:**
- `current_chapter` — Current Maha Dasha planet, start/end dates, plain-language life theme (max 60 words)
- `current_sub_chapter` — Antar Dasha planet + what this sub-period emphasises (max 40 words)
- `chapter_quality` — Whether this is an expansion, consolidation, or challenge period based on planetary nature (max 40 words)
- `upcoming_transitions` — Next 3 Maha Dasha changes with date + brief theme (max 25 words each)
- `this_decade_arc` — Big-picture narrative for the current ~10-year period (max 80 words)
- `remedies` — Dasha-planet-specific remedy (same structure)

---

## Part 5 — Delivery Protocol for This Workstream

### Sequence

1. **Contract 8A (Lagna Kundali)** — deliver first. This is foundational and independent of the report workstream. Full spec in `.claude/CODEX_LAGNA_KUNDLI_CONTRACT.md`.

2. **Contract 9-A (Karmic Debt)** — first Individual Report. Deliver after Kundali OR in parallel if CODEX has capacity to run two workstreams.

3. **Contracts 9-B through 9-E** — deliver one at a time, in priority order, waiting for Temple Team validation of each before beginning the next.

### Each Delivery Must Include

**For every router file:**
- [ ] `from __future__ import annotations`
- [ ] `timezone.utc` — never `datetime.UTC`
- [ ] Pydantic v2 with `ConfigDict`
- [ ] Python 3.12 `py_compile` passes
- [ ] Single collection `individual_reports` with `report_type` field
- [ ] `request.app.state.db` and `request.state.user.get("email")`
- [ ] No Temple source imports
- [ ] Routes: `POST .../generate` and `GET .../history`
- [ ] Output constraints enforced in the router (truncate/validate field lengths)

**Documentation:**
- [ ] `{REPORT}_TEMPLE_HANDOFF_NOTES.md`
- [ ] Brief self-check: confirm output matches the spec above before delivery

### Staging

All files delivered to `codex-deliveries/` folder on GitHub. Temple Team validates before any file moves to `backend/`.

---

## Part 6 — Key Boundaries Summary

| Item | Approved for Temple Delivery | Platform Only |
|---|---|---|
| pyswisseph Vedic computation | ✅ | — |
| External astrology API | ❌ | Maybe later |
| Natal-only reports | ✅ Phase 1 | — |
| Transit-based reports | ✅ Phase 2 | — |
| Synastry (two persons) | ✅ Phase 3 | — |
| Audio/video analysis | ❌ | Platform only |
| NotebookLM-style synthesis | ❌ | Platform only |
| Push trigger / notification dispatch | ❌ | Temple side (APScheduler) |
| Remedies (spiritual guidance framing) | ✅ | — |
| Outcome guarantees in remedies | ❌ | — |
| "Sexual Vitality" raw framing | ❌ | — |
| "Intimacy & Vitality" reframed | ✅ Phase 2 | — |
| APScheduler in delivered files | ❌ | Temple side only |
| Multiple MongoDB collections | ❌ | — |
| New Python dependencies | ❌ unless essential | — |

---

*This document is the authoritative contract appointment for the Individual Reports workstream and the Lagna Kundali Module (Contract 8A). All prior exploratory conversations are superseded by the decisions above.*

*Next action for CODEX: Begin Contract 8A (Lagna Kundali — full spec in `.claude/CODEX_LAGNA_KUNDLI_CONTRACT.md`) and Contract 9-A (Karmic Debt — spec above). Confirm receipt and flag any further discrepancies before building.*
