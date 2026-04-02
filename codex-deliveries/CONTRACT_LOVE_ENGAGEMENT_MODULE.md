# EverydayHoroscope — New Contract: Love & Engagement Module

> **Issued by:** Temple Team
> **Date:** 2 April 2026
> **To:** CODEX — New Thread
> **Governing reference:** `CODEX_WAYS_OF_WORKING.md` applies in full
> **Computation engine:** `pyswisseph 2.10.x`, Lahiri ayanamsa, sidereal — same as all Temple contracts

---

## 1. Purpose of This Thread

This thread commissions the **Love & Engagement Module** — a commercially prioritised suite of reports and features centred on romantic timing, compatibility, and personal magnetism.

**Commercial context:** Love and bonding-related content is the highest-converting category among our single-user base. This module is being elevated to parallel-track priority alongside the Individual Reports workstream.

**Governing decisions from CONTRACT_APPOINTMENT_INDIVIDUAL_REPORTS_AND_KUNDALI.md that apply here:**
- D1: Vedic-first, pyswisseph only — no external astrology API
- D7: Remedies approved (mantras, gemstones, rituals, vastu) — supportive framing only
- D9: All artifacts write to `individual_reports` collection with `report_type` field
- D10: Route prefix `/api/reports/` — one router file per report
- D11: CODEX delivers the report generation endpoint. Temple wires all notifications, scheduling, and lifecycle UI.

**Decision updates specific to this thread:**
- **D6 update:** Deep Synastry (two-person data) is now approved for inclusion in this module's scope. Treat it as a Phase 2 item within this thread. Temple will handle consent/storage design separately.
- **D8 update:** "Intimacy & Vitality Forecast" is confirmed for this module under that exact name and tone framing.
- **D5 update:** Transit-based reports are approved for this module from the start (not deferred). Use `swe.calc_ut()` with the current date for transit data.

---

## 2. First Step Required from CODEX

**Before building anything, CODEX must deliver a Brief Idea + Engineering Structure document for this module.**

The document should cover:
1. **Report-by-report overview** — For each proposed report: what it computes, what pyswisseph calls are required, what the output structure looks like (high level)
2. **Data requirements** — Which reports need natal data only vs. transit data vs. two-person data
3. **Shared compute layer** — Are there reusable functions across reports? (e.g., Venus position, 5th/7th house lord) CODEX should design shared utilities that avoid code duplication
4. **Proposed additions** — CODEX is invited to propose additional Love & Engagement reports or features not listed here that would strengthen the module commercially or astrologically
5. **Risk flags** — Any astrological concepts that need Temple clarification before implementation

Temple Team will review this document, give feedback, and confirm the final scope before CODEX builds.

---

## 3. Proposed Report Bundle

The following reports are proposed for this module. CODEX should assess and propose any additions.

### 3.1 Encounter Window *(Transit-based, Single User)*
**Commercial hook:** "When is your next best window to meet someone?"
**Astrological logic:**
- Trigger: Transiting Venus within 3° of natal Sun, natal Ascendant, or 7th House Lord
- Secondary trigger: Transiting Jupiter entering natal 5th or 7th house
- Output: Date windows (next 90 days) when conditions are active
- Report sections: Current window status, next 3 peak windows with dates, personalised context for each, remedies
**File:** `encounter_window_router.py` | **Route:** `/api/reports/encounter-window`

---

### 3.2 Love Weather Forecast *(Transit-based, Single User — Seasonal)*
**Commercial hook:** "Your 90-day romantic forecast — when to move, when to wait."
**Astrological logic:**
- Aggregate transiting planet activity over the natal 5th and 7th houses across the next 90 days
- Score each month: expansion (benefic transits), caution (malefic transits), neutral
- Key planets to monitor: Venus, Jupiter, Mars, Saturn
**Output sections:** 90-day arc summary, month-by-month quality rating, key dates to watch, action guidance, remedies
**File:** `love_weather_router.py` | **Route:** `/api/reports/love-weather`

---

### 3.3 Date-Night Score *(Transit-based, Daily Micro-Forecast)*
**Commercial hook:** "Should I ask them out tonight? Check your cosmic score."
**Astrological logic:**
- Calculate angular distance between Transiting Moon and natal Venus
- 0°, 60°, 120° → High score (favourable)
- 90°, 180° → Low score (cautious)
- Also check: Transiting Venus aspect to natal Mars (passion amplifier)
**Output:** Daily "Love Battery" percentage + 1-line contextual note + suggested action
**File:** `date_night_router.py` | **Route:** `/api/reports/date-night`

---

### 3.4 Digital Dating Strategy Report *(Natal-based, Single User)*
**Commercial hook:** "Your cosmic dating profile — what you attract and what attracts you."
**Astrological logic:**
- 5th house sign + lord: natural romantic style and what you attract
- Venus sign + house: what you desire and how you express affection
- Mars sign + house: what you pursue and physical attraction style
- 7th house sign + lord: long-term partner archetype
**Output sections:** Attraction signature, dating style, ideal partner profile, what to lead with on a first date, red flags to watch for in yourself, remedies
**File:** `digital_dating_router.py` | **Route:** `/api/reports/digital-dating`

---

### 3.5 Intimacy & Vitality Forecast *(Transit-based, Single User)*
**Commercial hook:** "Your peak energy windows — emotional, romantic, and vital."
**Astrological logic:**
- 8th house lord natal position: intimacy style and depth
- Transiting Mars forming trine (120°) or conjunction (0°) to natal Venus
- Transiting Mars entering natal 8th house
- Output: Current energy level assessment + next peak window dates
**Output sections:** Natal intimacy signature, current vitality phase, peak window dates (next 60 days), energy navigation tips, remedies
**Tone:** Energy, passion, confidence, romantic connection. Not explicit.
**File:** `intimacy_vitality_router.py` | **Route:** `/api/reports/intimacy-vitality`

---

### 3.6 Deep Synastry — Soul Connection *(Natal-based, Two Persons)*
**Commercial hook:** "How deep is your connection? The cosmic compatibility deep-dive."
**Astrological logic:**
- Compute natal charts for both persons
- Key synastry overlays: Person A's planets in Person B's houses (and vice versa)
- Key aspects: Conjunction, trine, square, opposition between charts
- Venus–Mars inter-aspects: attraction and passion dynamic
- Moon–Moon and Moon–Sun: emotional compatibility
- Saturn overlays: long-term stability vs. friction
**Output sections:** Connection archetype, attraction dynamic, emotional resonance score, long-term compatibility assessment, growth areas, remedies for both
**Data input:** Two sets of birth data (date, time, location)
**Note:** Temple Team will handle consent and storage design. CODEX delivers the compute endpoint only.
**File:** `soul_connection_router.py` | **Route:** `/api/reports/soul-connection`

---

### 3.7 CODEX to Propose: Additional Reports
CODEX is invited to propose additional Love & Engagement reports that would strengthen this module. Examples of directions Temple Team is open to:
- Venus Retrograde personal impact report
- "Soulmate Timing" — when is the statistically strongest relationship window in your Dasha sequence?
- Rahu/Ketu axis love karma report (nodes in 5th/7th house interpretation)
- Any other commercially strong concept CODEX identifies

Include proposed reports in the Brief Idea document with the same structure: commercial hook, astrological logic, output structure, data requirements.

---

## 4. Technical Constraints (All Reports in This Module)

These apply without exception — same as all Temple contracts:

| Constraint | Requirement |
|---|---|
| Computation | `pyswisseph 2.10.x`, Lahiri ayanamsa, sidereal |
| No external APIs | No third-party astrology or transit API |
| Backend language | Python 3.12 |
| Python boilerplate | `from __future__ import annotations` at top |
| Datetime | `timezone.utc` — never `datetime.UTC` |
| Pydantic | v2 with `ConfigDict` |
| Database | `request.app.state.db`, collection: `individual_reports` |
| Auth | `request.state.user.get("email")` |
| No Temple imports | No imports from any live Temple source file |
| Routes per router | `POST .../generate` + `GET .../history` at minimum |
| Delivery folder | `codex-deliveries/` — Temple validates before moving to `backend/` |

---

## 5. Build Approach

Once Temple Team approves the Brief Idea + Engineering Structure:

- CODEX builds **all approved reports as standalone files** — no phased delivery within this module
- All router files delivered together in a single drop to `codex-deliveries/`
- Temple Team reviews all files in one pass and gives consolidated feedback
- Do not wait for Temple validation of Report A before starting Report B — build in parallel and deliver together

---

## 6. Deliverables from CODEX (Step 1)

**Deadline for Brief Idea document:** As soon as possible — this is the starting gate for the module.

**Document to deliver:** `LOVE_ENGAGEMENT_BRIEF_IDEA_CODEX.md`

Contents:
1. Report-by-report engineering approach (for all 6 proposed + any new proposals)
2. Shared compute layer design
3. Any proposed additions to the bundle
4. Risk flags or clarification questions (before building)

---

*This thread is the authoritative contract for the Love & Engagement Module. The governing decisions from the Individual Reports contract apply in full unless explicitly updated above.*
