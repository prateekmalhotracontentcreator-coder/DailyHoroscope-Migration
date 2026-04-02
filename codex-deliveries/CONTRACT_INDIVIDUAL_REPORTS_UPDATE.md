# EverydayHoroscope — Contract Update: Individual Reports + Kundali Workstream

> **Issued by:** Temple Team
> **Date:** 2 April 2026
> **To:** CODEX — Existing Individual Reports Thread
> **Supersedes (in part):** `CONTRACT_APPOINTMENT_INDIVIDUAL_REPORTS_AND_KUNDALI.md` (30 March 2026)
> **Governing reference:** `CODEX_WAYS_OF_WORKING.md` applies in full
> **Status:** All D1–D11 decisions from the original contract remain binding unless explicitly updated below

---

## 1. Purpose of This Update

This document issues two significant updates to the Individual Reports workstream:

1. **Priority re-ordering:** Love & Bonding is elevated to **parallel-track priority** alongside Phase 1 natal reports. It is no longer Phase 2 content.
2. **D-Decision updates:** Three decisions are revised (D5, D6, D8) to reflect the Love & Engagement Module contract now running as a separate parallel thread.
3. **Phase 1 acceleration:** CODEX is asked to build all Phase 1 natal reports simultaneously (standalone files, one drop) rather than sequentially one at a time.

**Commercial context:** Love and bonding-related content is the highest-converting category among our single-user base. The original contract sequenced love content into Phase 2 (after natal reports). That sequencing is no longer correct — we are elevating love content to immediate parallel delivery.

---

## 2. D-Decision Updates

The following decisions from the original contract are updated. All other decisions (D1, D2, D3, D7, D9, D10, D11) remain unchanged. D2 and D3 are explicitly re-confirmed below, given the three new parallel threads now open alongside this workstream.

---

### D5 — Update: Transit-based reports approved for Love module immediately

**Original decision (30 March 2026):** Natal-only in Phase 1. Transit-based deferred to Phase 2.

**Updated decision:** This rule applies to the **Individual Reports thread only**. The Love & Engagement Module (separate thread, issued 2 April 2026) has transit-based reports approved from the start. Use `swe.calc_ut()` with the current date for all Love module transit data.

Individual Reports Phase 1 (natal-only reports: Karmic Debt, Career Blueprint, Shadow Self, Retrograde Survival, Life Cycles) — this constraint still applies. No change.

---

### D6 — Update: Synastry approved for Love module Phase 2

**Original decision (30 March 2026):** Synastry (two-person data) deferred to Phase 3. Not in first or second wave.

**Updated decision:** Deep Synastry is now approved as a **Phase 2 item within the Love & Engagement Module thread** (issued 2 April 2026). Temple will handle consent and storage design separately. Codex delivers the compute endpoint only.

This does not affect the Individual Reports thread. Single-user reports only here. Phase 3 designation for synastry in the Individual Reports thread is retired — synastry is now covered by the Love module thread.

---

### D8 — Update: Intimacy & Vitality confirmed for Love module

**Original decision (30 March 2026):** "Intimacy & Vitality Forecast" reframed from "Sexual Vitality" — deferred to Phase 2.

**Updated decision:** Confirmed for the Love & Engagement Module thread (Phase 1 of that thread). The exact name "Intimacy & Vitality Forecast" and the tone framing (energy, passion, confidence, romantic connection — not explicit) are locked. Full spec in `CONTRACT_LOVE_ENGAGEMENT_MODULE.md`.

This report is removed from the Individual Reports Phase 2 queue. It is owned by the Love module thread.

---

### D2 — Audio/Video Analysis and NotebookLM-Style Flows: Remains Deferred Entirely

**Context for re-confirmation:** The new Love & Engagement Module thread includes a Ritual Trigger Engine with a `coach_summary` field — a synthesised daily coaching message derived from the user's active astrological alignments. The new Notification Engine thread includes personalised push notification copy. Neither of these constitutes NotebookLM-style synthesis or audio/video analysis.

The opening of the Love module thread, the Notification Engine thread, and the Ritual Trigger Engine subscription product does **not** reopen D2 in any form.

**D2 decision stands without modification:** Deferred entirely. Platform exploration only. Not a Temple contract at any stage of any currently active workstream.

The following must not appear in any Codex delivery file across any active thread — Individual Reports, Love & Engagement, Notification Engine, or Lagna Kundali:
- Audio/video analysis pipelines
- FFmpeg-based processing
- NotebookLM-style cross-document synthesis
- Unofficial GitHub automation wrappers referencing audio/video tooling
- Any LLM API call for report content generation

This constraint holds until Temple explicitly issues a new contract authorising it. The `coach_summary` field in the Ritual Trigger Engine is generated deterministically from pyswisseph output using structured conditional logic — not an LLM call. CODEX must implement it that way.

---

### D3 — "Ask 1 Question": Remains Narrowed and Deferred to Phase 2

**Context for re-confirmation:** The Ritual Trigger Engine (Love module thread) operates on 5 named trigger scenarios with fully deterministic astrological logic. This could be mistaken for the "fixed-category tiles" version of Ask 1 Question described in D3. It is not.

The architectural distinction:
- **D3 / Ask 1 Question:** User inputs or selects a question → system interprets the question and returns a contextual astrological answer. User intent drives the interaction. Deferred.
- **Ritual Trigger Engine:** System monitors the user's chart autonomously against live transits and fires when a pre-defined mathematical alignment condition is met. No user question input. No interpretation layer. The system initiates; the user only receives.

These are fundamentally different interaction models. The Ritual Trigger Engine does not constitute, approximate, or unlock D3.

**D3 decision stands without modification:** Narrowed to fixed deterministic report tiles only, deferred to Phase 2 of this workstream. When Temple issues the Phase 2 contract, "Ask 1 Question" will be scoped as a small set of fixed categories (`career_question`, `love_question`, `family_question`) each mapping to specific natal house and planet combinations with bounded, deterministic output. Nothing in the new parallel threads changes this plan.

---

## 3. Phase 1 Scope Confirmation — Individual Reports Thread

The following five natal reports remain the core Phase 1 scope of this thread. No change to specs. Full specs remain in `CONTRACT_APPOINTMENT_INDIVIDUAL_REPORTS_AND_KUNDALI.md` Part 4.

| Priority | Report | File | Route |
|---|---|---|---|
| 1 | Karmic Debt & Past Life | `karmic_debt_router.py` | `/api/reports/karmic-debt` |
| 2 | Career & Success Blueprint | `career_blueprint_router.py` | `/api/reports/career-blueprint` |
| 3 | Shadow Self & Hidden Qualities | `shadow_self_router.py` | `/api/reports/shadow-self` |
| 4 | Retrograde Survival Guide | `retrograde_survival_router.py` | `/api/reports/retrograde-survival` |
| 5 | The Pattern of Life Cycles | `life_cycles_router.py` | `/api/reports/life-cycles` |

**Build approach change:** The original contract asked for sequential delivery (validate Contract 9-A before beginning 9-B). This is updated.

**New instruction:** CODEX should build all five router files simultaneously as standalone files and deliver in a single drop. Temple will review all five in one pass and give consolidated feedback. Do not wait for Temple sign-off on Report 1 before starting Report 2.

This mirrors the build approach confirmed for the Love & Engagement Module thread.

---

## 4. Updated Phase Map Across Threads

The following table reflects the full picture across all three parallel threads as of 2 April 2026:

### Individual Reports Thread — Phase 1 (Active, all natal)

| Report | Status |
|---|---|
| Karmic Debt & Past Life | Build now |
| Career & Success Blueprint | Build now |
| Shadow Self & Hidden Qualities | Build now |
| Retrograde Survival Guide | Build now |
| The Pattern of Life Cycles | Build now |

### Love & Engagement Module Thread — Phase 1 (Active, mostly transit)

| Report | Status |
|---|---|
| Encounter Window | Build after Brief Idea approved |
| Love Weather Forecast | Build after Brief Idea approved |
| Date-Night Score | Build after Brief Idea approved |
| Digital Dating Strategy | Build after Brief Idea approved |
| Intimacy & Vitality Forecast | Build after Brief Idea approved |

### Love & Engagement Module Thread — Phase 2 (After Phase 1)

| Report | Status |
|---|---|
| Deep Synastry — Soul Connection | Phase 2 — two-person data. Brief Idea to include this. |

### Individual Reports Thread — Phase 2 (After Phase 1 validated)

Transit-based individual reports. Temple will issue Phase 2 contract when Phase 1 is validated. The following items from the original Phase 2 queue are **removed** because they now belong to the Love module thread:
- ~~Encounter Window~~ → Love module thread
- ~~Seasonal Love Weather~~ → Love module thread
- ~~Date-Night Score~~ → Love module thread
- ~~Intimacy & Vitality Forecast~~ → Love module thread

**Remaining Individual Reports Phase 2 queue:**
| Report | Notes |
|---|---|
| Lunar Cycle Wellness & Rituals | Moon phase × natal Moon — individual wellness focus |
| Venus Retrograde Personal Impact | Personal natal impact of Venus retrograde cycles |
| Soulmate Timing (Dasha-based) | When is statistically strongest relationship window in Dasha sequence |
| Rahu/Ketu Love Karma | Nodes in 5th/7th house interpretation |

Note: Venus Retrograde Personal Impact, Soulmate Timing, and Rahu/Ketu Love Karma were proposed additions in the Love module brief. Temple is assigning them here to the Individual Reports Phase 2 queue (natal/transit hybrid, single-user) rather than to the Love module thread, to keep scope clean. Codex may comment on this assignment in the Love module Brief Idea document.

---

## 5. Lagna Kundali — Status

Contract 8A (Lagna Kundali) from the original contract has reached **Cycle 2 delivery** (received by Temple, 1 April 2026).

Temple has already integrated the following Cycle 2 items into the live codebase:
- `_build_lagna_chart()` backend function + Pydantic models in `panchang_router.py`
- Lagna Chart card on Panchang Today/Tomorrow tabs (frontend)
- Lunar Month label row in Five Limbs card (frontend)
- Quick-date strip on Panchang date views (frontend)
- Full Lagna Kundali tab (`/panchang/lagna`) with North Indian D1 chart (frontend)

These are live on Render and Vercel as of 2 April 2026.

**Pending on Lagna Kundali:**
- Temple has not yet integrated the full `kundali_router.py` (the standalone birth chart endpoint, separate from Panchang). This is next in queue for Temple integration — awaiting Temple review of the full Cycle 2 dropin.
- Chart orientation toggle (North/South/East Indian formats) — P3 item, Codex has delivered. Temple will integrate in a future cycle.

**No further Lagna Kundali action required from Codex at this time.** Temple will raise a new Cycle 3 brief if needed.

---

## 6. Panchang — Status Note

Temple confirms the following 3 items from the Codex Panchang dropin have been integrated by Temple (not Codex action required):
- `_build_lagna_chart()` backend integration ✅ Temple done
- Lagna Chart card frontend ✅ Temple done
- Lunar Month row + Quick-date strip ✅ Temple done

**No further Panchang action required from Codex.** The Panchang thread is paused pending Temple's own roadmap items.

---

## 7. Shared Compute Layer — Cross-Thread Note

Both the Individual Reports thread and the Love & Engagement Module thread will need common natal chart computation: Venus position, Mars position, house lord calculation, ascendant, Dasha sequence.

CODEX is asked to design a **shared compute utility** (`vedic_shared_utils.py` or similar) that:
- Wraps repeated pyswisseph calls used across multiple report routers
- Is importable by each router file with no circular dependencies
- Does not import from any live Temple source file (including `vedic_calculator.py`)

Include the design of this shared utility in **both** Brief Idea documents (Love module + Individual Reports). If the designs converge, CODEX may propose delivering a single shared file serving both threads.

---

## 8. Priority Order Across All Active Threads

As of 2 April 2026, the priority order for Codex effort is:

| Thread | Step | Priority |
|---|---|---|
| Love & Engagement Module | Deliver `LOVE_ENGAGEMENT_BRIEF_IDEA_CODEX.md` | **Highest — immediate** |
| Notification Engine | Deliver `NOTIFICATION_ENGINE_BRIEF_IDEA_CODEX.md` | **High — parallel with Love brief** |
| Individual Reports | Build all 5 Phase 1 router files (standalone, one drop) | **High — parallel workstream** |
| Lagna Kundali | Await Temple feedback on Cycle 2 `kundali_router.py` | **Paused — Temple reviewing** |

---

## 9. Technical Constraints (No Change)

All constraints from the original contract apply without exception:

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

*This document updates and extends the Individual Reports contract dated 30 March 2026. The original contract remains the authoritative source for all D-decisions and report specs not explicitly revised above. Both documents should be read together.*
