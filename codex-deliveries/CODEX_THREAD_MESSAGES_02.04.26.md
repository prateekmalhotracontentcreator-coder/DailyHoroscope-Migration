# Codex Thread Messages — 2 April 2026

> **Prepared by:** Temple Team
> **Purpose:** Ready-to-send messages for each active Codex thread. Copy-paste directly into each thread.
> **Note:** Codex does not have direct GitHub access. All contract content is included inline below.

---

---

## THREAD A: TAROT

---

**Subject: Tarot Module — Post-Integration Action Brief**

Temple Team here. We've reviewed your post-integration audit note (TAROT_POST_INTEGRATION_AUDIT_NOTE_2026-04-01.md) and the QA sweep results. Good work surfacing these clearly. Here is Temple's action directive.

---

### What is confirmed working — no changes needed

- `reading.scenes` path is correctly live (TAR-11 / TAR-12 class of fixes confirmed shipped ✅)
- Bookmark call using `POST /tarot/bookmark` with the expected body shape ✅
- Core Daily Draw, spread functionality, and archive UI ("Opening your archive…") ✅

---

### Action 1 — Premium Surfaces: Expose the Full Package (P1)

**Finding confirmed by Temple QA:** The live `/tarot` surface does not expose the premium spread access flow. The following are not visible to users:
- `/tarot/favorable-periods` — not surfaced
- `/tarot/offers` — not surfaced
- Spread access/gate flow — not triggered
- "Favorable Periods" or "Begin Premium Reading" UI strings — not rendered

**Temple directive:**
- Deliver an updated `TarotPage.jsx` that wires the premium spread access gate into the live UI flow
- The Razorpay paywall is already integrated on the Temple side. Codex must ensure the UI correctly checks subscription status and renders premium surfaces when active (or the paywall CTA when not)
- If the `/tarot/favorable-periods` route requires a backend endpoint that was delivered in the Codex package but not yet registered in Temple's `main.py`, include a clear note in the delivery handoff flagging which router needs to be registered
- Favorable Periods: if this is a transit-based feature, confirm which pyswisseph call drives it and ensure the endpoint is present in the delivery

---

### Action 2 — History: Resolve Hybrid State (P1)

**Finding confirmed:** The live bundle contains two history path assumptions — the newer archive path and an older `/tarot/history` `e.data.history || []` read. This is a fragile state.

**Temple directive:**
- Deliver a clean `TarotPage.jsx` (or the relevant history component) that uses one canonical history path only — the newer archive/bookmark model
- Remove any residual references to the old `e.data.history || []` pattern
- Confirm in the delivery note which MongoDB collection history is written to and the document shape

---

### Action 3 — SEO Metadata: Route-Specific Tags (P2)

**Finding confirmed:** `/tarot` page title, canonical, and OG tags are serving generic homepage metadata.

**Temple directive:**
- Add the `<SEO>` component call to `TarotPage.jsx` with:
  - **Title:** `Free Tarot Reading — Daily Draw & Spreads | EverydayHoroscope`
  - **Description:** `Get your free daily tarot card draw and multi-card spreads. Cosmic guidance powered by the 78-card Rider-Waite deck. EverydayHoroscope.`
  - **Canonical:** `https://www.everydayhoroscope.in/tarot`
  - **JSON-LD:** `SoftwareApplication` or `WebPage` type with tarot-specific keywords
- Same treatment for any sub-routes (`/tarot/spreads`, `/tarot/history`)

---

### Delivery format

- Deliver updated `TarotPage.jsx` (and any sub-components if relevant) to `codex-deliveries/`
- Include `TAROT_CYCLE2_HANDOFF_NOTES.md` with: (a) premium surface wiring instructions, (b) history collection name + document shape, (c) any backend endpoints that need registering in `main.py`

Temple will review and integrate. No phased delivery needed — send all fixes in one drop.

---

---

## THREAD B: NUMEROLOGY

---

**Subject: Numerology Module — Post-Integration Action Brief**

Temple Team here. We have reviewed your post-integration audit note (NUMEROLOGY_POST_INTEGRATION_AUDIT_NOTE_2026-04-01.md) and the QA sweep results. Here is Temple's action directive.

---

### Core finding

The Numerology backend and report generation are confirmed live. The gap is on the **report renderer**: after a report is generated, the frontend does not render the full structured output. The following are missing or broken in the current live UI:

1. **`ContinueJourney` flow** — the guided next-step flow after report generation is not rendering
2. **Lo Shu Grid** — the numerological grid is not displayed; data appears to be arriving from the API but the frontend component is not rendering it
3. **Structured report section tables** — report output sections (guidance notes, remedy tables, number breakdowns) are not laid out as structured tables/cards; they appear as plain text or missing entirely
4. **`favorable_timing` section** — this section appears to be failing; Temple suspects a backend compute issue or a missing field in the response shape

---

### Action 1 — Report Renderer: Full Section Rendering (P1)

**Temple directive:**
- Deliver an updated `NumerologyPage.jsx` (or the relevant report-view component) that correctly renders all report sections from the API response:
  - Lo Shu Grid as a 3×3 visual grid with the user's numbers placed
  - Structured guidance tables per report section (not plain text)
  - Remedy section rendered as a formatted card (mantra / gemstone / ritual)
  - Number breakdown grid (Life Path, Expression, Soul Urge etc.) rendered as the numbers tile layout
- If there is a separate report-view component (`NumerologyReportPage.jsx` or similar), deliver it as a standalone file

---

### Action 2 — `ContinueJourney` Flow (P1)

**Temple directive:**
- The `ContinueJourney` component or flow (post-report CTA that guides the user to their next report or premium upsell) is not rendering
- Deliver the component that implements this flow
- It should appear at the bottom of every generated report view
- If this depends on subscription status (premium vs free), ensure the logic handles both states

---

### Action 3 — `favorable_timing` Section (P1)

**Temple directive:**
- Investigate and fix the `favorable_timing` failure
- If the backend is not returning this field, fix the router
- If the frontend is not rendering it, fix the component
- Deliver both the router fix (if needed) and the updated renderer

---

### Action 4 — SEO Metadata (P2)

- Add route-specific `<SEO>` component to `NumerologyPage.jsx`:
  - **Title:** `Free Numerology Report — Life Path, Karmic Debt & Name Analysis | EverydayHoroscope`
  - **Description:** `Discover your numerology profile — Life Path number, Karmic Debt, Name Correction, and more. Free Vedic numerology reports on EverydayHoroscope.`
  - **Canonical:** `https://www.everydayhoroscope.in/numerology`
  - **JSON-LD:** `SoftwareApplication` type with numerology keywords

---

### Delivery format

- Deliver `NumerologyPage.jsx` + any sub-components to `codex-deliveries/`
- If the backend router needs a fix (for `favorable_timing`), deliver the updated `numerology_router.py`
- Include `NUMEROLOGY_CYCLE2_HANDOFF_NOTES.md` with: (a) component hierarchy explanation, (b) API response shape changes if any, (c) any backend router registration changes

One drop, Temple reviews in one pass.

---

---

## THREAD C: LAGNA KUNDALI

---

**Subject: Lagna Kundali — Cycle 2 Acknowledged + Cycle 3 Brief**

Temple Team here. Two things in this message: (1) Cycle 2 delivery acknowledgment, (2) Cycle 3 brief to bring Lagna Kundali to full functional and premium delivery standard.

---

### Part 1 — Cycle 2 Acknowledgment

Temple has reviewed the Cycle 2 delivery files:
- `CONTRACT_8A_kundali_router_v2.py`
- `CONTRACT_8A_KundaliPage_v2.jsx`

Temple has integrated the following items from the Cycle 2 dropin directly into the live codebase. No further Codex action needed on these:

| Item | Status |
|---|---|
| `_build_lagna_chart()` backend function + Pydantic models in `panchang_router.py` | ✅ Temple integrated |
| Lagna Chart card on Panchang Today/Tomorrow tabs | ✅ Temple integrated |
| Lunar Month label row in Five Limbs card | ✅ Temple integrated |
| Quick-date strip on Panchang date views | ✅ Temple integrated |
| Full Lagna Kundali tab at `/panchang/lagna` with North Indian D1 chart | ✅ Temple integrated |

The following are confirmed present in the Cycle 2 files but **not yet integrated** — they are next in Temple's queue:
- Full `kundali_router.py` (standalone birth chart endpoint, separate from Panchang)
- Full replacement `KundaliPage.jsx` (`/lagna-kundali` standalone page)

Temple will action these. No change needed from Codex on these files unless Cycle 3 items supersede them (see below).

---

### Part 2 — Cycle 3 Brief

The Cycle 2 audit (31 March + 1 April 2026) identified the following open items. Temple is issuing this as the Cycle 3 brief. The goal is **full functional + premium delivery standard** for the Lagna Kundali module.

---

#### P1-A — Upagraha: Replace Placeholder Math (Backend)

**Issue:** `Gulika` and `Mandi` are returning values from the angular seed placeholder method. The live API currently sets `supported: true` and `pending_verification: null`, presenting these as production-valid when they are not. On the live fixture (15 Jun 1990, 14:30, Mumbai), Gulika returns Sagittarius and Mandi returns Capricorn — these conflict with the JHora benchmark Temple supplied.

**Action required:**
1. Implement the BPHS Ashtama-Yama method using `swe.rise_trans` as planned
2. Validate output against Temple's JHora fixture before flipping `pending_verification: null`
3. Until the JHora benchmark match is confirmed, set `supported: false` and `pending_verification: true` for both Gulika and Mandi

**Acceptance criterion:** Fixture (15 Jun 1990, 14:30, Mumbai) returns Gulika and Mandi matching the Temple JHora reference. `pending_verification` flips to `null` only after that match.

---

#### P1-B — Unknown Birth-Time: Functional Restriction (Backend, preferred)

**Issue:** When `time_precision: "unknown"`, the backend currently returns Bhav Chalit, Yoga, Vimshottari Dasha, Shadbala, and Bhavabala in full with only a low-reliability note. The spec requires Lagna-sensitive layers to be disabled, not just warned.

**Action required:**
- When `time_precision === "unknown"`, omit or null these fields in the API response: `bhav_chalit`, `yoga_list`, `vimshottari_dasha`, `shadbala`, `bhavabala`
- Return a structured `meta.restricted_layers` field explaining what was omitted and why
- If the backend change is deferred, the frontend must suppress those tabs entirely and render "Birth time required for this analysis" — not a warning over populated data

---

#### P2-A — Ashtaka Varga / Shadbala / Bhavabala: Frontend Rendering

**Issue:** The live API already returns numeric payloads for these three layers. The frontend renders generic pending-state cards instead of the approved tables.

**Action required:**
- Replace the pending-state placeholders with rendering components that consume the existing API payload:
  - **Ashtaka Varga:** Sarva Ashtaka Varga table + per-planet Bindus
  - **Shadbala:** Per-planet strength table with total and ratio columns
  - **Bhavabala:** Per-house strength table
- This is a pure frontend task. No backend change required.

---

#### P2-B — SEO Metadata: Route-Specific (Frontend)

**Action required:**
- Add `<SEO>` component to the Lagna Kundali page:
  - **Title:** `Lagna Kundali — Free Vedic Birth Chart & Ascendant Calculator | EverydayHoroscope`
  - **Description:** `Calculate your Lagna Kundali online — free Vedic birth chart with D1 Rashi chart, ascendant degree, Bhav Chalit, Yoga registry, and Vimshottari Dasha. Powered by Swiss Ephemeris.`
  - **Canonical:** `https://www.everydayhoroscope.in/lagna-kundali`
  - **JSON-LD:** `SoftwareApplication` type with Vedic astrology keywords

---

#### P3 — Chart Orientation Toggle: North / South / East (Frontend)

**Action required:**
- Add a 3-way toggle to the chart toolbar: `North | South | East`
- Chart SVG re-renders in the selected style:
  - **North Indian:** Diamond grid (current)
  - **South Indian:** Fixed-sign square grid (sign names fixed to cells, planets placed)
  - **East Indian:** Bengali square layout
- Default: North Indian. Persist selection to `localStorage`

---

#### Premium Layer — Share Card + Save (New addition)

To bring Lagna Kundali to **premium delivery standard** on par with the Panchang and Horoscope modules:

**Action required:**
- Add a **Share Card** to the Lagna Kundali page: a 900px offscreen card (same pattern as `PanchangShareCard` / `HoroscopeShareCard` in `ShareCard.jsx`) capturing:
  - User's name (if available from auth), birth date, birth time, city
  - Ascendant sign + degree
  - Sun and Moon sign + house
  - Current Maha Dasha + Antar Dasha
  - EverydayHoroscope branding footer
- **Share Buttons:** WhatsApp, Instagram, Save Card (download), Copy Link — same `ShareButtons` component pattern
- **Save Chart:** `POST /api/kundali/save` endpoint (already in scope per Contract 8A). Ensure the UI has a working "Save Chart" button for authenticated users. Saved charts accessible via `GET /api/kundali/my-charts`.

**Note on Temple imports:** The `ShareButtons` component exists in `frontend/src/components/ShareCard.jsx`. Codex must **not import** from this file directly. Codex should deliver a self-contained share card implementation within the `KundaliPage.jsx` file (or a separate `KundaliShareCard` component in the deliverables), following the same visual and behavioral pattern.

---

### Delivery format

Deliver together in one drop to `codex-deliveries/`:
- `CONTRACT_8A_kundali_router_v3.py` — with P1-A and P1-B fixes
- `CONTRACT_8A_KundaliPage_v3.jsx` — with P2-A, P2-B, P3, and Premium layer (Share Card + Save)
- `LAGNA_KUNDALI_CYCLE3_HANDOFF_NOTES.md` — fixture test results, JHora match confirmation for Upagraha, component hierarchy

Temple will review all three in one pass before integration.

---

---

## THREAD D: PANCHANG

---

**Subject: Panchang — Temple Integration Complete, Thread Status Update**

Temple Team here. This is a status close-out note for the Panchang thread.

---

### Confirmation: 3 Dropin Items Integrated by Temple

You correctly identified in your April 1 response (PANCHANG_FEATURE_COMPLETION_RESPONSE_2026-04-01.md) that the three items from the Panchang brief were already present in the Codex dropin layer. The gap was on the Temple side. Temple has now integrated all three:

| Item | Status |
|---|---|
| `_build_lagna_chart()` backend function + Pydantic models | ✅ Live on Render |
| Lagna Chart card (Panchang Today/Tomorrow) + Lunar Month row | ✅ Live on Vercel |
| Quick-date strip on date views | ✅ Live on Vercel |
| Full Lagna Kundali tab (`/panchang/lagna`) with North Indian D1 chart | ✅ Live on Vercel |

These are all live and verified on production as of 2 April 2026.

---

### Thread Status: Paused

The Panchang engine is stable and production-grade. There are no open Codex action items on this thread.

**You also correctly noted** that the Horoscope language-extension files were not present in the Panchang workspace. That is correct — language capability across the web app is a separate contract being issued to a new thread (see Language thread).

Temple will raise new items in this thread if the Panchang engine needs further development. Until then, no action required from Codex.

---

---

## THREAD E: INDIVIDUAL REPORTS + KUNDALI

---

**Subject: Individual Reports — Contract Update (2 April 2026)**

Temple Team here. This message issues a contract update to the Individual Reports workstream. Please read the full update below before proceeding.

---

### 1. D-Decision Updates

Three decisions from the original contract (30 March 2026) are updated:

**D5 Update:** The natal-only Phase 1 rule applies to this thread only. The Love & Engagement Module (new separate thread) has transit-based reports approved from the start. No change to Individual Reports Phase 1.

**D6 Update:** Deep Synastry (two-person data) is now approved as Phase 2 of the Love & Engagement Module thread. It is removed from Phase 3 of this thread. Single-user only continues to apply here.

**D8 Update:** "Intimacy & Vitality Forecast" is confirmed for the Love & Engagement Module thread (Phase 1). It is removed from the Individual Reports Phase 2 queue. The Love module thread owns it.

All other D-decisions (D1, D2, D3, D7, D9, D10, D11) remain unchanged. D2 and D3 are explicitly re-confirmed below given the new parallel threads now open.

---

**D2 — Audio/Video Analysis and NotebookLM-Style Flows: Remains Deferred Entirely**

The new Love & Engagement Module thread includes a Ritual Trigger Engine with a `coach_summary` field — a synthesised daily coaching message generated from the user's active astrological alignments. This is **not** a NotebookLM-style flow. It is a deterministic text output derived from structured pyswisseph computation. No audio, no video, no large language model synthesis, no cross-document reasoning.

The opening of the Love module thread, the Notification Engine thread, and the Ritual Trigger Engine subscription product does **not** reopen D2 in any form.

D2 remains: **Deferred entirely. Platform exploration only. Not a Temple contract at any stage of any active workstream.**

Audio/video analysis pipelines, FFmpeg-based processing, and NotebookLM-style synthesis must not appear in any Codex delivery file across any active thread — Individual Reports, Love module, Notification Engine, or Lagna Kundali. This holds until Temple explicitly issues a new contract authorising it.

---

**D3 — "Ask 1 Question": Remains Narrowed and Deferred to Phase 2**

The Ritual Trigger Engine (Love module thread) has 5 named trigger scenarios with fully deterministic logic — First Date Magnet, Steamy Encounter, Ex-Recovery, Long-Term Love, Lunar Daily Score. These are **not** the "Ask 1 Question" concept from D3.

The distinction is architectural:
- **D3 / Ask 1 Question:** User inputs or selects a question → system interprets it and returns a contextual answer. Open-ended or semi-open input layer. Deferred.
- **Ritual Trigger Engine:** System monitors the user's chart autonomously and fires when a pre-defined mathematical alignment occurs. No user question input. No interpretation layer. Fully deterministic pyswisseph output.

These are different products. The Ritual Trigger Engine does not constitute or unlock D3.

D3 remains: **Narrowed to fixed deterministic report tiles only, deferred to Phase 2 of this thread.** When Temple issues the Phase 2 contract, "Ask 1 Question" tiles will be scoped as a small set of fixed categories (`career_question`, `love_question`, `family_question`) mapping to specific natal house and planet combinations with bounded output. Nothing in the new parallel threads changes this.

---

### 2. Phase 1 Build Approach — Change

**Original instruction:** Build reports sequentially. Validate Contract 9-A before beginning 9-B.

**Updated instruction:** Build all five Phase 1 router files simultaneously as standalone files. Deliver in a single drop to `codex-deliveries/`. Temple will review all five in one pass and give consolidated feedback.

This matches the build approach confirmed for the Love & Engagement Module thread.

---

### 3. Phase 1 Scope — No Change

The five reports remain as specified in the original contract (Part 4). All specs are unchanged:

| Priority | Report | File | Route |
|---|---|---|---|
| 1 | Karmic Debt & Past Life | `karmic_debt_router.py` | `/api/reports/karmic-debt` |
| 2 | Career & Success Blueprint | `career_blueprint_router.py` | `/api/reports/career-blueprint` |
| 3 | Shadow Self & Hidden Qualities | `shadow_self_router.py` | `/api/reports/shadow-self` |
| 4 | Retrograde Survival Guide | `retrograde_survival_router.py` | `/api/reports/retrograde-survival` |
| 5 | The Pattern of Life Cycles | `life_cycles_router.py` | `/api/reports/life-cycles` |

All technical constraints are unchanged: `pyswisseph 2.10.x`, Lahiri ayanamsa, Python 3.12, `from __future__ import annotations`, `timezone.utc`, Pydantic v2, `individual_reports` collection, `request.app.state.db`, no Temple source imports.

---

### 4. Shared Compute Layer — New Request

Both this thread and the new Love & Engagement Module thread will need common natal chart computation: Venus position, Mars position, house lord calculation, ascendant, Dasha sequence.

Please design a **shared compute utility** (`vedic_shared_utils.py` or equivalent name of your choosing) that:
- Wraps repeated pyswisseph calls used across multiple report routers
- Is importable by each router file without circular dependencies
- Does not import from any live Temple source file (including `vedic_calculator.py`)

Include this utility in the Phase 1 delivery drop. It can be co-developed alongside the five report routers.

---

### 5. Phase 2 Queue — Revised

The Love module items (Encounter Window, Love Weather, Date-Night Score, Intimacy & Vitality) are removed from this thread's Phase 2 queue. They are owned by the Love & Engagement Module thread.

Remaining Individual Reports Phase 2 queue (Temple will issue a separate Phase 2 contract when Phase 1 is validated):

| Report | Notes |
|---|---|
| Lunar Cycle Wellness & Rituals | Moon phase × natal Moon — individual wellness |
| Venus Retrograde Personal Impact | Natal impact of Venus retrograde cycles |
| Soulmate Timing (Dasha-based) | Strongest relationship window in Dasha sequence |
| Rahu/Ketu Love Karma | Nodes in 5th/7th house — love karma interpretation |

---

### 6. Action

Please begin building all five Phase 1 router files in parallel. Deliver as a single drop including `vedic_shared_utils.py` and `{REPORT}_TEMPLE_HANDOFF_NOTES.md` for each file.

---

---

## NEW THREAD i: LOVE & ENGAGEMENT MODULE

---

**Subject: New Contract — Love & Engagement Module**

Temple Team here. This message opens a new contract thread for the Love & Engagement Module — a commercially prioritised suite of reports centred on romantic timing, compatibility, and personal magnetism.

**Commercial context:** Love and bonding-related content is the highest-converting category among our single-user base. This module is being elevated to parallel-track priority alongside the Individual Reports workstream.

---

### Governing Decisions (From Individual Reports Contract — Apply in Full)

- **D1:** Vedic-first, pyswisseph only — no external astrology API
- **D7:** Remedies approved (mantras, gemstones, rituals, vastu) — supportive framing only
- **D9:** All artifacts write to `individual_reports` collection with `report_type` field
- **D10:** Route prefix `/api/reports/` — one router file per report
- **D11:** CODEX delivers the report generation endpoint. Temple wires all notifications, scheduling, and lifecycle UI.

### Decision Updates Specific to This Thread

- **D5 update:** Transit-based reports are approved for this module from the start (not deferred). Use `swe.calc_ut()` with the current date for transit data.
- **D6 update:** Deep Synastry (two-person data) is approved for inclusion as Phase 2 within this thread. Temple will handle consent/storage design separately.
- **D8 update:** "Intimacy & Vitality Forecast" is confirmed for this module under that exact name and tone framing.

---

### Step 1 Required: Brief Idea + Engineering Structure

Before building anything, please deliver **`LOVE_ENGAGEMENT_BRIEF_IDEA_CODEX.md`** covering:

1. **Report-by-report engineering overview** — For each of the 6 proposed reports below: what it computes, what pyswisseph calls are required, what the output structure looks like (high level)
2. **Data requirements** — Which reports need natal data only vs. transit data vs. two-person data
3. **Shared compute layer** — Are there reusable functions across reports? (e.g., Venus position, 5th/7th house lord). Design shared utilities — also consider aligning with the `vedic_shared_utils.py` being designed in the Individual Reports thread.
4. **Proposed additions** — Additional reports or features you recommend beyond the 6 proposed
5. **Risk flags** — Any astrological concepts needing Temple clarification before implementation

Temple Team will review, give feedback, and confirm final scope before you build.

---

### Proposed Report Bundle (6 Reports)

---

**Report 1 — Encounter Window** *(Transit-based, Single User)*
Commercial hook: "When is your next best window to meet someone?"
- Trigger: Transiting Venus within 3° of natal Sun, natal Ascendant, or 7th House Lord
- Secondary: Transiting Jupiter entering natal 5th or 7th house
- Output: Date windows (next 90 days) when conditions are active
- Sections: Current window status, next 3 peak windows with dates, personalised context, remedies
- File: `encounter_window_router.py` | Route: `/api/reports/encounter-window`

---

**Report 2 — Love Weather Forecast** *(Transit-based, Single User — Seasonal)*
Commercial hook: "Your 90-day romantic forecast — when to move, when to wait."
- Aggregate transiting planet activity over natal 5th and 7th houses across next 90 days
- Score each month: expansion (benefic), caution (malefic), neutral
- Key planets: Venus, Jupiter, Mars, Saturn
- Sections: 90-day arc summary, month-by-month quality rating, key dates, action guidance, remedies
- File: `love_weather_router.py` | Route: `/api/reports/love-weather`

---

**Report 3 — Date-Night Score** *(Transit-based, Daily Micro-Forecast)*
Commercial hook: "Should I ask them out tonight? Check your cosmic score."
- Angular distance between Transiting Moon and natal Venus
- 0°, 60°, 120° → High score (favourable); 90°, 180° → Low score (cautious)
- Also check: Transiting Venus aspect to natal Mars (passion amplifier)
- Output: Daily "Love Battery" percentage + 1-line contextual note + suggested action
- File: `date_night_router.py` | Route: `/api/reports/date-night`

---

**Report 4 — Digital Dating Strategy Report** *(Natal-based, Single User)*
Commercial hook: "Your cosmic dating profile — what you attract and what attracts you."
- 5th house sign + lord: natural romantic style and what you attract
- Venus sign + house: what you desire and how you express affection
- Mars sign + house: what you pursue and physical attraction style
- 7th house sign + lord: long-term partner archetype
- Sections: Attraction signature, dating style, ideal partner profile, what to lead with on a first date, red flags in yourself, remedies
- File: `digital_dating_router.py` | Route: `/api/reports/digital-dating`

---

**Report 5 — Intimacy & Vitality Forecast** *(Transit-based, Single User)*
Commercial hook: "Your peak energy windows — emotional, romantic, and vital."
- 8th house lord natal position: intimacy style and depth
- Transiting Mars forming trine (120°) or conjunction (0°) to natal Venus
- Transiting Mars entering natal 8th house
- Output: Current energy level assessment + next peak window dates (next 60 days)
- Sections: Natal intimacy signature, current vitality phase, peak window dates, energy navigation tips, remedies
- **Tone:** Energy, passion, confidence, romantic connection. Not explicit.
- File: `intimacy_vitality_router.py` | Route: `/api/reports/intimacy-vitality`

---

**Report 6 — Deep Synastry: Soul Connection** *(Phase 2 — Two Persons, Natal)*
Commercial hook: "How deep is your connection? The cosmic compatibility deep-dive."
- Compute natal charts for both persons
- Key synastry overlays: Person A's planets in Person B's houses (and vice versa)
- Key aspects: Conjunction, trine, square, opposition between charts
- Venus–Mars inter-aspects: attraction and passion dynamic
- Moon–Moon and Moon–Sun: emotional compatibility
- Saturn overlays: long-term stability vs. friction
- Sections: Connection archetype, attraction dynamic, emotional resonance score, long-term compatibility, growth areas, remedies for both
- Data input: Two birth datasets (date, time, location)
- Note: Temple handles consent and storage design. Codex delivers compute endpoint only.
- File: `soul_connection_router.py` | Route: `/api/reports/soul-connection`

---

### CODEX Proposed Additions

Please include in the Brief Idea document your own proposed additions. Temple is open to:
- Venus Retrograde personal impact report
- "Soulmate Timing" — strongest relationship window in Dasha sequence
- Rahu/Ketu axis love karma (nodes in 5th/7th)
- Any other commercially strong concept you identify

---

### Technical Constraints

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
| Delivery folder | `codex-deliveries/` |

---

### Build Approach (After Brief Idea Approved)

- Build all approved reports as standalone files — no phased delivery
- Deliver all router files in one drop
- Temple reviews all in one pass
- Do not wait for Temple validation of Report A before starting Report B — build in parallel

---

*Deadline for Brief Idea document: as soon as possible. This is the starting gate for the module.*

---

---

## NEW THREAD ii: NOTIFICATION ENGINE

---

**Subject: New Contract — EverydayHoroscope Notification Engine**

Temple Team here. This message opens a new contract thread for the Notification Engine — web-app wide notification infrastructure serving all modules.

---

### Why a Dedicated Contract

The existing Admin Console (Temple-built) handles ad-hoc subscriber email via Resend. That is a send-now admin flow, not a scalable multi-channel notification service. Every new module (Love & Engagement, Individual Reports, Panchang) will need to fire notifications — report-ready pings, encounter window alerts, daily forecast drops. Without a shared engine, this becomes fragmented.

This contract creates a single Codex-delivered notification service layer. Temple wires all scheduling and lifecycle (APScheduler — existing pattern in admin module). This is consistent with D4 and D11 from the Individual Reports contract: Temple owns scheduling, Codex delivers the callable service layer.

---

### Step 1 Required: Brief Idea + Engineering Structure

Before building anything, please deliver **`NOTIFICATION_ENGINE_BRIEF_IDEA_CODEX.md`** covering:

1. **Channel-by-channel design** — How each delivery channel (email, WhatsApp, web push, in-app) is implemented: libraries, payload structure, fallback behaviour
2. **Template system design** — How notification content is parameterised per module, per report type, per user segment
3. **Endpoint map** — All proposed `/api/notifications/` endpoints with request/response shapes
4. **MongoDB schema** — Collections and document shapes for preferences, logs, push subscriptions
5. **Proposed additions** — Notification patterns or features you recommend beyond what's specified
6. **Risk flags** — WhatsApp BSP not yet selected, browser push API surface, any concerns

---

### Scope: 4 Delivery Channels

---

**Channel 1 — Email (Transactional + Marketing)**

Current state: Resend integration is live in Temple's admin module. This is not a service-callable template layer.

Codex delivers `notification_email_service.py` — callable internal service (not a router):
- `send_transactional_email(to, template_id, context)` — single-user, event-triggered
- `send_bulk_email(audience_filter, template_id, context)` — list-based, called by Temple scheduler

Template registry — required templates at launch:
- `report_ready` — "Your {report_name} is ready to view"
- `encounter_window_alert` — "Your next encounter window opens {date}"
- `love_weather_weekly` — "Your 90-day love forecast is in"
- `daily_panchang_digest` — Tithi + Nakshatra subject; sunrise, key timings, special yoga in body
- `date_night_score` — "Tonight's Love Battery: {score}%"
- `welcome` — Post-registration welcome

Env vars already set on Render: `RESEND_API_KEY`, `FROM_EMAIL`

---

**Channel 2 — WhatsApp (Meta Cloud API)**

Current state: Env vars pending BSP setup (`WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_ACCESS_TOKEN`). Not yet live.

Codex delivers `notification_whatsapp_service.py`:
- `send_whatsapp_template(to_phone, template_name, template_params)` — pre-approved Meta template
- `send_whatsapp_text(to_phone, message)` — plain text within 24-hour session window

Required template names (pre-approval with Meta BSP before go-live):
- `report_ready`, `panchang_daily`, `encounter_window`, `love_battery_daily`

**Graceful degradation:** if `WHATSAPP_PHONE_NUMBER_ID` not set, service logs a warning and returns without error.

---

**Channel 3 — Web Push (Browser Push Notifications)**

Current state: Not implemented. New capability.

Codex delivers `notification_push_service.py` using the `pywebpush` library:
- `send_push(subscription_info, title, body, icon, url)`
- `send_push_bulk(subscriptions, title, body, icon, url)`

MongoDB collection: `push_subscriptions` — stores VAPID subscription objects per user.

Public-facing API endpoints:
- `POST /api/notifications/push/subscribe` — stores subscription + links to user email
- `DELETE /api/notifications/push/unsubscribe` — removes subscription

**VAPID keys:** Include instructions for Temple on how to generate VAPID keys and which env vars to set. Do not hardcode.

Note: Temple wires the frontend `navigator.serviceWorker` / `PushManager.subscribe()` flow and `sw.js` service worker. Codex delivers backend only.

---

**Channel 4 — In-App Notification Feed**

MongoDB collection: `in_app_notifications` — one document per notification per user.

Document shape:
```json
{
  "id": "uuid",
  "user_email": "string",
  "type": "report_ready | encounter_window | panchang_reminder | love_weather",
  "title": "string",
  "body": "string",
  "action_url": "string (relative)",
  "is_read": false,
  "created_at": "iso-8601-utc"
}
```

API endpoints:
- `GET /api/notifications/feed` — unread + last 30 days for authenticated user
- `PATCH /api/notifications/{notification_id}/read` — mark one read
- `PATCH /api/notifications/read-all` — mark all read

Internal callable: `create_in_app_notification(db, user_email, type, title, body, action_url)` — used by other services without going through HTTP.

---

### Scope: Temple-Callable Trigger Endpoints

Temple's APScheduler will call these on a schedule. Codex delivers the endpoints:

| Endpoint | When Temple calls it | What it does |
|---|---|---|
| `POST /api/notifications/trigger/panchang-daily` | Daily ~5:30 AM per TZ group | Panchang digest to opted-in subscribers |
| `POST /api/notifications/trigger/encounter-window` | Daily check | Identifies users with open window today; sends email + push + in-app |
| `POST /api/notifications/trigger/love-weather-weekly` | Every Sunday | Weekly Love Weather summary |
| `POST /api/notifications/trigger/date-night-score` | Daily evening | Date-Night Love Battery score |
| `POST /api/notifications/trigger/report-ready` | Event-driven (after report generation) | Cross-channel "your report is ready" |

Trigger payload:
```json
{
  "audience": "all | tag:{tag_name} | email:{email}",
  "date": "YYYY-MM-DD (optional, defaults to today)"
}
```

Trigger auth: `X-Temple-Trigger-Key` header (env var: `TEMPLE_TRIGGER_KEY`). Not exposed to frontend.

---

### Scope: User Notification Preferences

MongoDB collection: `notification_preferences` — one document per user.
- `GET /api/notifications/preferences` — fetch current user's preferences
- `PUT /api/notifications/preferences` — update preferences (full replace)

Preference fields: channel opt-ins (email, whatsapp, push, in_app), notification type opt-ins, WhatsApp phone (E.164), timezone.

---

### Scope: Notification Log

MongoDB collection: `notification_logs` — check if this collection already exists in Temple's admin module. If so, use it and add `source: "notification_engine"` field.
- `GET /api/notifications/log` — last 100 entries, admin-only (`request.state.user.get("role") == "admin"`)

---

### Files to Deliver

| File | Type |
|---|---|
| `notification_email_service.py` | Internal service |
| `notification_whatsapp_service.py` | Internal service |
| `notification_push_service.py` | Internal service |
| `notification_preferences_router.py` | FastAPI router |
| `notification_feed_router.py` | FastAPI router |
| `notification_push_router.py` | FastAPI router |
| `notification_trigger_router.py` | FastAPI router |
| `notification_log_router.py` | FastAPI router |
| `NOTIFICATION_ENGINE_TEMPLE_HANDOFF_NOTES.md` | Doc — router registration, env vars, APScheduler wiring guide |

---

### Technical Constraints

Same as all Temple contracts. `from __future__ import annotations`, `timezone.utc`, Pydantic v2, Python 3.12, `request.app.state.db`, no Temple source imports. New dependency: `pywebpush` only.

Internal service files must be importable standalone — accept `db` and other dependencies as function parameters, not at module level.

---

*Deadline for Brief Idea document: as soon as possible — parallel with the Love module Brief Idea.*

---

---

## NEW THREAD iii: LANGUAGE CAPABILITY ACROSS WEB-APP

---

**Subject: New Contract — Language Capability (Phase 1: Hindi + Routing Extension)**

Temple Team here. This message opens a new contract thread for Language Capability across the EverydayHoroscope web app.

---

### Background

The Panchang module currently has language-prefixed URL routing (e.g., `/hi/panchang`, `/en/panchang`) baked into its navigation structure. This routing pattern exists only on the Panchang module. The rest of the web app — Horoscope pages (Daily, Weekly, Monthly), Tarot, Numerology, Lagna Kundali — has no language routing and no language switcher.

**Phase 1 of this contract** establishes:
1. A global language switcher in the web app NavBar
2. Language-prefixed routing extended to all major pages
3. Hindi as the first non-English language — UI structural labels translated (not AI-generated content)
4. Language preference persisted in `localStorage`

This is a frontend-primary contract. Backend changes are minimal.

---

### Step 1 Required: Brief Idea + Engineering Structure

Before building anything, please deliver **`LANGUAGE_CAPABILITY_BRIEF_IDEA_CODEX.md`** covering:

1. **Routing architecture** — How language-prefixed routes are implemented across all page types without breaking existing routes. Proposed URL structure (e.g., `/hi/horoscope/daily`, `/en/horoscope/daily` or `/horoscope/daily?lang=hi`). Temple preference is path-based (`/hi/...`) for SEO benefit — confirm feasibility.
2. **Translation layer design** — Where translation strings live (a JSON dictionary per language, a context provider, or another pattern). How components consume them. Recommended pattern for maintainability.
3. **Language switcher component** — Design proposal for the NavBar language switcher (dropdown vs. flag icons vs. text toggle). How it interacts with routing.
4. **Scope of Phase 1 translation** — Which UI elements are in scope: navigation labels, section headers, card titles, button text, Five Limbs names, Choghadiya slot names, report section headers. What is explicitly out of scope for Phase 1 (AI-generated report body content, Panchang computed text strings).
5. **SEO implications** — How language-prefixed routes affect `sitemap.xml` and `hreflang` tags. Temple will update the sitemap — Codex should flag what needs to change.
6. **Risk flags** — React Router v6 constraints, existing Panchang language routing conflicts, any concerns.

---

### Phase 1 Scope: Pages in Scope for Language Routing

| Page | Current Route | Phase 1 Language Route |
|---|---|---|
| Daily Horoscope | `/horoscope/daily` | `/hi/horoscope/daily`, `/en/horoscope/daily` |
| Weekly Horoscope | `/horoscope/weekly` | `/hi/horoscope/weekly`, `/en/horoscope/weekly` |
| Monthly Horoscope | `/horoscope/monthly` | `/hi/horoscope/monthly`, `/en/horoscope/monthly` |
| Panchang (Today) | `/panchang` | Already has language routing — extend/align |
| Tarot | `/tarot` | `/hi/tarot`, `/en/tarot` |
| Numerology | `/numerology` | `/hi/numerology`, `/en/numerology` |
| Lagna Kundali | `/lagna-kundali` | `/hi/lagna-kundali`, `/en/lagna-kundali` |

**Phase 1 language support: Hindi (`hi`) + English (`en`) as the baseline pair.**

Phase 2 languages (separate contract, after Phase 1 validated): Bengali, Tamil, Telugu, Gujarati, Marathi, Kannada, Malayalam.

---

### Phase 1 Scope: UI Elements to Translate (Hindi)

**In scope for Phase 1 translation:**
- NavBar labels (Home, Horoscope, Panchang, Tarot, Numerology, Kundali, Login/Profile)
- Sub-navigation labels (Today, Tomorrow, Daily, Weekly, Monthly, etc.)
- Section card headers (Five Limbs, Timing Windows, Auspicious, Inauspicious, Choghadiya, Special Yogas, etc.)
- Five Limbs field names (Tithi, Nakshatra, Yoga, Karana, Vara)
- Choghadiya slot quality labels (Amrit, Shubh, Labh, Char, Udveg, Kaal, Rog)
- Panchang timing window labels (Brahma Muhurta, Rahu Kaal, Abhijit Muhurta, etc.)
- Button labels (Generate Report, Save, Share, View History, etc.)
- Report section headers (Career Archetype, Natural Strengths, etc.)

**Explicitly out of scope for Phase 1:**
- AI-generated or LLM-generated report body text
- Panchang computed strings (sunrise times, tithi names — these are Sanskrit/fixed and do not need translation)
- Horoscope prediction paragraphs
- Any backend content — Phase 1 is frontend label translation only

---

### Phase 1 Scope: Language Switcher

- Global language switcher added to the NavBar (desktop) and mobile menu
- Displays current language code with a flag or short label: `EN | हिं`
- Switching language: updates URL prefix + `localStorage` preference (`everydayhoroscope_lang`)
- On first visit with no preference: default to `en`
- On return visit: read `localStorage` and redirect to appropriate language prefix

---

### Phase 1 Scope: Translation File

- A single `translations.js` (or `translations.json`) file in `frontend/src/locales/`
- Keys: flat or nested English string keys
- Values: `{ en: "English text", hi: "Hindi text" }`
- Temple Team will review the Hindi translations in the delivered file. Codex may use reference translations for standard Vedic terms (Tithi, Nakshatra, etc.) and flag any terms where translation is uncertain.

---

### Technical Constraints

| Constraint | Requirement |
|---|---|
| Frontend framework | React 18, React Router v6 |
| No new npm dependencies | Implement without i18next or react-intl unless strongly justified in Brief Idea |
| No backend changes | Phase 1 is frontend-only |
| Translation file location | `frontend/src/locales/translations.js` |
| Language persistence | `localStorage` key: `everydayhoroscope_lang` |
| URL pattern | Path-based: `/{lang}/...` (e.g., `/hi/panchang`) — consistent with existing Panchang pattern |
| Delivery folder | `codex-deliveries/` |

---

### Build Approach (After Brief Idea Approved)

Once Temple approves the Brief Idea:
- Deliver all Phase 1 files in one drop: updated page files + `translations.js` + NavBar component + `App.js` route changes
- Temple reviews all in one pass
- No phased delivery within Phase 1

---

*This is an entirely new thread. No prior Codex conversation on this topic. Please treat this Brief Idea step as the starting point.*

---

*End of thread messages — 2 April 2026*
