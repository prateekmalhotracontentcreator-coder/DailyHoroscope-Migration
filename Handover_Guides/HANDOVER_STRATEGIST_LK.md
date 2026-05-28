# Handover Guide -- The Strategist + Lal Kitab
> Prepared by: Claude Code (Main Thread) → New Dedicated Thread
> Date: 2026-05-29
> Purpose: New thread picks up Strategist Phase 2 CD pipeline + Lal Kitab standalone module commission.

---

## 1. Your Role in the New Thread

You are the **Strategist + Lal Kitab thread**. Your scope is:
- Drive The Strategist Phase 2 Claude Design (CD) pipeline (7 components) -- use CD as **design consultant, visual redesign partner, and feature builder**: visual polish on A2-built components, gap identification during prototype review, and design-first approach for any new features
- Integrate TT-approved CD prototypes into the React app
- Own all LK open gaps (LK-OP-5 through LK-OP-8) -- **LK-1 is already live, do NOT re-issue to Codex**
- Own all open ops gaps listed in Sections 5 and 6

**You do NOT own:** KE, SEO 20K, Book Decode, Tarot, or any other module. Those are separate threads.

**When you start, TT will share CD work folders** (HTML prototypes and design assets already worked on). Read this guide first, then wait for TT to drop those folders.

---

## 2. Reference Files -- Read These on Startup

| Priority | File | What it Contains |
|---|---|---|
| 🔴 MUST READ | `Codex_Deliveries/Strategist/THE_STRATEGIST_FULL_SPEC.md` | Complete product spec for The Strategist -- all gates, phases, UX vision |
| 🔴 MUST READ | `Codex_Deliveries/Strategist/TRACKER.md` | Live commission status (v1.8), all open points |
| 🔴 MUST READ | `Codex_Deliveries/Strategist/CD_CONFIRMATIONS_STR_PHASE2.md` | CD delivery format (file-per-component), 3-mode spec (light/dark/cr), full token CSS |
| 🔴 MUST READ | `Codex_Deliveries/Strategist/CODEX_COMMISSION_STR_2EF_SCOREBOARD_GATES.md` | First CD commission to send -- brief is complete, not yet sent |
| 🟠 READ | `Codex_Deliveries/Strategist/CODEX_COMMISSION_STR_PHASE2_FULL_CD.md` | Full Phase 2 CD scope reference |
| 🟠 READ | `Codex_Deliveries/LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` | LK-1 brief -- full Lal Kitab standalone module spec |
| 🟠 READ | `Codex_Deliveries/LK/TRACKER.md` | LK current status |
| 🟡 REFERENCE | `#5_CODEX_COMMISSION_TABLE.md` (MODULE 6 + MODULE 10) | Master commission table for Strategist + LK |
| 🟡 REFERENCE | `#3_ACTION_TRACKER.md` (M-15 onward) | Open action items relevant to this module |

---

## 3. Current State -- The Strategist

### What is Live (Do NOT re-build)

| Commission | Status | Commit | What It Did |
|---|---|---|---|
| STR-1 | ✅ INTEGRATED | `ba58192` | Premium landing page + War Room visual rebuild |
| STR-2J | ✅ INTEGRATED | `9ad2e0a` | Missions UI -- MissionCard responsive + dasha display |
| STR-R01 | ✅ INTEGRATED | `958df18` | War Room Engine Selector -- wired live engine → `StrategistWarRoom` prop-bag |
| STR-R02 | ✅ INTEGRATED | `bf20389` | Golden Hour Strip -- sunset_iso → 3-window state machine |
| STR-R03 | ✅ INTEGRATED | `bf20389` | Pitru Rin Ledger -- Gate 1 → PitruRinRow shape |
| STR-R04 | ✅ INTEGRATED | `c439691` | Dasha Transition Date -- formatTransitionDate + wire transition prop |
| STR-2A1 | ✅ INTEGRATED | `bf20389` | NavBar + Footer cleanup -- Strategist top-level, dedupe Blog |

### Key Backend Files (READ ONLY -- do not modify unless explicitly scoped)

| File | Role |
|---|---|
| `backend/strategist_router.py` | All Strategist API endpoints including `POST /api/strategist/profile` + `GET /api/strategist/dashboard` |
| `backend/strategist_engine.py` | LK rules engine -- queries `lalkitab_strategist` without `approval_status` filter (intentional) |
| `backend/vedic_calculator.py` | **Single source for all dasha computation** -- NEVER duplicate dasha logic elsewhere |

### Key Frontend Files

| File | Role |
|---|---|
| `frontend/src/pages/strategist/StrategistPage.jsx` | Main Strategist page (`/strategist`) |
| `frontend/src/pages/strategist/StrategistMissionsPage.jsx` | Missions page (`/strategist/missions`) |
| `frontend/src/components/strategist/war-room/StrategistWarRoom.jsx` | War Room component -- do NOT modify prop signature |
| `frontend/src/components/strategist/ControlRoomBackdrop.jsx` | CR dark green matrix backdrop |
| `frontend/src/styles/strategist-tokens.css` | All CSS tokens -- gold, dark navy, card surfaces |

### Live URLs
- `/strategist` -- main page
- `/strategist/missions` -- missions page
- `/strategist/war-room` -- War Room (added STR-R01)

---

## 4. The Strategist Phase 2 -- CD Pipeline (Your Primary Work)

> **⚠️ IMPORTANT CONTEXT:** The Phase 2 FUNCTIONAL FEATURES (2A-2I) were already built by Account 2 (A2 session, 2026-05-09 to 2026-05-13 -- a pure Codex delivery + integration session) and subsequently refined by STR-R01 through R04 in the main thread. **Use CD (Claude Design) as a design consultant and visual redesign partner** across three modes: (1) **Visual redesign** -- replace functional-but-rough A2 implementations with polished, on-brand HTML prototypes; (2) **Gap identification** -- during each prototype review, surface UX gaps, missing states, or edge cases the A2 build missed; (3) **Feature consultation** -- for any new feature scope, engage CD first to get design recommendations and a prototype before issuing to Codex. TT approves each prototype before it is integrated into React.

### Functional State of Phase 2 Components (all live as of 2026-05-13 + main thread refinements)

| Phase | Component | Current State | CD Role |
|---|---|---|---|
| 2B | KP Gate 0 in War Room (inline verdict) | ✅ Functionally live | UI/UX polish + gap check |
| 2C | WAIT/NO/PRAY Pre-Flight banners | ✅ Functionally live | UI/UX polish + gap check |
| 2D | Score-gated re-entry (NO ≥60%, PRAY ≥75%) | ✅ Functionally live | UI/UX polish + gap check |
| 2E | LK 5-Gate summaries in dashboard | ✅ Functionally live | UI/UX polish + gap check |
| 2F | Success & Debt Scoreboard (Layer 6) | ✅ Functionally live | UI/UX polish + gap check |
| 2G | Action Plan page `/strategist/action-plan` | ✅ Functionally live | UI/UX polish + gap check |
| 2I | PRAY path (Mantra + LK Debt Audit) | ✅ Functionally live | UI/UX polish + gap check |

### CD Build Order (STRICT -- each file must be TT-approved before next starts)

| Order | CD Commission | Prototype File | Status |
|---|---|---|---|
| 1 (FIRST) | STR-2F | `STR-2F · ConquestScoreboard.html` | 🔴 SEND NOW -- brief at `CODEX_COMMISSION_STR_2EF_SCOREBOARD_GATES.md` |
| 2 | STR-2E | `STR-2E · LKGateSummaries.html` | 🟡 After 2F approved |
| 3 | STR-2C | `STR-2C · PreFlightBanners.html` | 🟡 After 2E approved |
| 4 | STR-2D | `STR-2D · ScoreGatedReEntry.html` | 🟡 After 2C approved |
| 5 | STR-2I | `STR-2I · PRAYPath.html` | 🟡 After 2D approved |
| 6 | STR-2G | `STR-2G · ActionPlanPage.html` | 🟡 After 2I approved |
| 7 | STR-2B | `STR-2B · Gate0Panel.html` | 🟡 After 2G approved |

**When TT shares CD work folders:** Some of these prototypes may already be designed. Check which files TT drops -- if 2F prototype exists, start review there rather than requesting a fresh CD build.

**CD delivery format (from `CD_CONFIRMATIONS_STR_PHASE2.md`):**
- One standalone HTML file per component
- 3 theme mode toggle: `[ light ] [ dark ] [ cr ]`
- Full token CSS block in `CD_CONFIRMATIONS_STR_PHASE2.md` -- copy into prototype `<style>` tag

### Token System
All CSS tokens are in `frontend/src/styles/strategist-tokens.css`. Key tokens:
```
--strategist-gold          #C5A059
--strategist-bg / --strategist-fg
--strategist-card-bg / --strategist-card-border
--strategist-emerald       #3FAA7A
--strategist-red           #E25C4B
```

### Backend Data Available
`GET /api/strategist/dashboard` already returns `scoreboard` + `gate_summaries` -- no new backend routes needed. See `CODEX_COMMISSION_STR_2EF_SCOREBOARD_GATES.md` for full response shape.

---

## 5. Open Verification Tasks (TT to action)

| ID | Item | Priority | Notes |
|---|---|---|---|
| STR-OP-3 | Verify DashaTimingBar live data on `/strategist/missions` | 🟠 HIGH | DashaTimingBar backend fix shipped (`667fc34`). Verify date ranges + progress bar rendering on production. |
| STR-OP-5 | Verify War Room live data on `/strategist/war-room` post STR-R01 | 🟠 HIGH | Verify: conquest score gauge non-zero, dasha bars show real planet names, mission board ≥1 card, no-profile users see "War Room Locked" gate. |
| STR-SEO-1 | Strategist routes return generic root metadata | 🟠 HIGH | All Strategist routes (`/strategist`, `/strategist/missions`, `/strategist/war-room`) return generic root OG meta instead of route-specific SEO. Fix: add `<SEO>` component to each page with correct title/description/og:image. |

---

## 6. Lal Kitab Module

> ⚠️ **CRITICAL CORRECTION (decoded from A2 session 2026-05-29):** LK-1 is **ALREADY FULLY BUILT AND LIVE**. The A2 session (2026-05-09 to 2026-05-13) built the complete standalone module. Do NOT re-issue LK-1 to Codex. Do NOT rebuild anything.

### What Is Live

| File | Lines | Role |
|---|---|---|
| `backend/lk_diagnostics.py` | 272 | 5-gate engine: Karmic Debt, House Awakening, 35-Year Cycle, Mercury Scan, Geographical |
| `backend/lk_remedies_router.py` | 348 | All LK API endpoints (`/api/lk/*`) |
| `frontend/src/pages/lk/` | 7 pages | Full standalone UI (see below) |

**Router wired in `backend/server.py`:** line 133 (import) + line 3325 (include_router)

**Live URLs:**

| Page | Route | Access |
|---|---|---|
| `LalKitabLandingPage.jsx` | `/lal-kitab-remedies` | Public SEO landing |
| `LKRemediesPage.jsx` | `/lk-remedies` | Free preview hub |
| `LKOnboardPage.jsx` | `/lk-remedies/onboard` | ProtectedRoute |
| `LKReportPage.jsx` | `/lk-remedies/report` | ProtectedRoute |
| `LKTrackerPage.jsx` | `/lk-remedies/tracker` | ProtectedRoute |
| `LKDebtAuditPage.jsx` | `/lk-remedies/debt-audit` | ProtectedRoute |
| `LKBrowsePage.jsx` | `/lk-remedies/remedies` | Public |

**MongoDB collections live:**
- `lalkitab_strategist` -- 823 records (LK rules + Strategist gates)
- `jyotish_lk_remedies` -- 361 records (planetary remedies by house)
- `lk_user_profiles` -- active

### Open Items (your thread owns these)

| # | Item | Priority | Notes |
|---|---|---|---|
| **LK-OP-5** | **Premium PDF download not built** | 🟡 MED | Original LK-1 brief included password-protected PDF (`FirstName+BirthYear+Month` formula). Not implemented in A2 build. |
| **LK-OP-6** | **5 split-required LK rules** | 🟡 MED | `lalkitab-ch21-fam-04` + 4 age/infancy rules tagged `split_required=True`. NLM to review and provide splits. |
| **LK-OP-7** | **96 in-range master doc records not salvaged** | 🟡 MED | Unique master doc IDs not in V2. Add as suffix IDs (800A, 800B, etc.) per agreed protocol if TT approves. |
| **LK-OP-8** | **TT acceptance verify on production** | 🟠 HIGH | Verify: `/lal-kitab-remedies` loads · onboard flow · diagnose returns 5 gates · debt audit · tracker persists · browse 361 records. |

### LK Phase 2 (Parking Lot -- do not build yet)
- **LK-OP-4:** Slot 33 → LK Debt Audit cross-module trigger (PRAY verdict surfaces Debt Audit)

### Architecture Notes
- `lk_diagnostics.py` imports from `vedic_calculator.py` -- NEVER from `knowledge_engine.py`
- Do NOT couple LK-1 UI with The Strategist UI in any future commission

---

## 7. Architecture Rules (Mandatory)

1. **All dasha/astronomical data** from `backend/vedic_calculator.py` + `pyswisseph` ONLY
2. **Do NOT** add dasha calculation functions to `strategist_router.py`, `strategist_engine.py`, or `knowledge_engine.py`
3. **Strategist approval behaviour:** `strategist_engine.py` queries ALL rules regardless of `approval_status` -- this is intentional, do not add a filter
4. **Do NOT modify** `StrategistWarRoom.jsx` prop signature or any existing War Room sub-components

---

## 8. A2 Session Context (133 turns, 2026-05-09 to 2026-05-13)

**What A2 was:** A dedicated Codex delivery + integration session. Account 2 (A2) received Codex-written code briefs, integrated them into the Temple App, ran builds, fixed bugs, and pushed to `main`. It was NOT a design or planning session -- every item below was shipped to production by end of that session.

**Session export folder (read if you need to audit or verify anything A2 built):**
`/Users/apple/Documents/Knowledge Engine_eBooks/LK and Strategist Session Export_CC A2/`
The export is 5803 lines / 133 turns. Use it to trace exact line numbers, bug fixes, or data ingestion runs if a production discrepancy is found.

**What the A2 session delivered and integrated:**
- Ingested 144 LK rules to `jyotish_lk` (NLM-reviewed and approved)
- Added 22 Strategist data patch records (IDs 1011-1020 + 1126-1137), total 823 records live
- Built and integrated Strategist Phase 2A through 2I into the live app:
  - 2A: KP NavBar + route registration
  - 2B: KP Gate 0 wired into War Room (inline verdict)
  - 2C: WAIT/NO/PRAY Pre-Flight banners
  - 2D: Score-gated re-entry (NO ≥60%, PRAY ≥75%)
  - 2E: LK 5-Gate summaries in dashboard
  - 2F: Success & Debt Scoreboard
  - 2G: Action Plan page at `/strategist/action-plan`
  - 2H: 7 notification triggers
  - 2I: PRAY path (Mantra + LK Debt Audit)
- Built and integrated full LK standalone module (7 pages + 2 backend files -- see Section 6)
- Integrated Remedies Engine Phase 1 (36 KP remedies seeded to `krishna_prashnavali_remedies`)
- Added on-page SEO content to Strategist pages
- Added Premium gate to War Room
- Fixed LK Onboarding auth error, Debt Audit crash, Reset Button

**What happened after A2 (main thread, 2026-05-26 to 2026-05-27):**
- STR-R01 through R04 + STR-2A1 + STR-2J refined and extended the A2 build
- STR-2J completed the "2J -- UI Polish" that A2 had noted as pending
- War Room Engine Selector, Golden Hour Strip, Pitru Rin Ledger, Dasha Transition all added

**Key insight:** All functional features exist. CD's job is UI/UX quality and gap identification -- not feature building.

**When TT opens the new thread:** TT will share CD work folders containing HTML prototypes already in progress. Check which prototypes exist before requesting new CD builds.

---

## 9. QA Gap Register Items Assigned to This Thread

| Gap ID | Description | Priority |
|---|---|---|
| STR-SEO-1 | Routes return generic root metadata -- SEO gap | 🟠 High |

---

## 10. Immediate First Actions for New Thread

1. Read `Codex_Deliveries/Strategist/THE_STRATEGIST_FULL_SPEC.md`
2. Read `Codex_Deliveries/Strategist/TRACKER.md`
3. Read `Codex_Deliveries/Strategist/CD_CONFIRMATIONS_STR_PHASE2.md` (token CSS, 3-mode spec, delivery format)
4. Read `Codex_Deliveries/Strategist/CODEX_COMMISSION_STR_2EF_SCOREBOARD_GATES.md` (STR-2F CD brief)
5. **Wait for TT to share CD work folders** -- do not begin CD work until you have reviewed what prototypes already exist
6. Inventory the CD work folders: list which of 2F, 2E, 2C, 2D, 2I, 2G, 2B have existing HTML prototypes
7. For any prototype that exists: review against the brief, then present to TT for sign-off
8. For any prototype not yet built: send the relevant brief to Claude Design
9. Once TT approves each prototype: integrate the visual redesign into the React app
10. **Parallel track (LK):** LK-1 is already live -- do NOT re-issue to Codex. Your LK tasks are: (a) TT acceptance verify on production (LK-OP-8), (b) track PDF gap (LK-OP-5), (c) NLM to split 5 rules (LK-OP-6), (d) 96 salvage records review (LK-OP-7)

---
*Handover prepared: 2026-05-29 by Claude Code Main Thread*
