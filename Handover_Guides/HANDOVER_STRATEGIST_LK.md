# Handover Guide -- The Strategist + Lal Kitab
> Prepared by: Claude Code (Main Thread) → New Dedicated Thread
> Date: 2026-05-29
> Purpose: New thread picks up Strategist Phase 2 CD pipeline + Lal Kitab standalone module commission.

---

## 1. Your Role in the New Thread

You are the **Strategist + Lal Kitab thread**. Your scope is:
- Drive The Strategist Phase 2 Claude Design (CD) pipeline (7 components)
- Integrate CD deliveries into the React app once TT approves each HTML prototype
- Issue and integrate **LK-1** (Lal Kitab Standalone Module) when TT gives batch approval
- Own all open ops gaps listed in Section 5

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

### Build Order (STRICT -- each file must be TT-approved before next starts)

| Order | CD Commission | File | Status |
|---|---|---|---|
| 1 (FIRST) | STR-2F | `STR-2F · ConquestScoreboard.html` | 🔴 SEND NOW -- brief at `CODEX_COMMISSION_STR_2EF_SCOREBOARD_GATES.md` |
| 2 | STR-2E | `STR-2E · LKGateSummaries.html` | 🟡 After 2F approved |
| 3 | STR-2C | `STR-2C · PreFlightBanners.html` | 🟡 After 2E approved |
| 4 | STR-2D | `STR-2D · ScoreGatedReEntry.html` | 🟡 After 2C approved |
| 5 | STR-2I | `STR-2I · PRAYPath.html` | 🟡 After 2D approved |
| 6 | STR-2G | `STR-2G · ActionPlanPage.html` | 🟡 After 2I approved |
| 7 | STR-2B | `STR-2B · Gate0Panel.html` | 🟡 After 2G approved |

**CD delivery format (from `CD_CONFIRMATIONS_STR_PHASE2.md`):**
- One standalone HTML file per component
- 3 theme mode toggle in prototype top bar: `[ light ] [ dark ] [ cr ]`
- Uses token CSS from `CD_CONFIRMATIONS_STR_PHASE2.md` (full CSS block included in that file)
- CC reviews and approves each file before next begins

### Token System
All CSS tokens are in `frontend/src/styles/strategist-tokens.css`. Key tokens:
```
--strategist-gold          #C5A059
--strategist-bg / --strategist-fg
--strategist-card-bg / --strategist-card-border
--strategist-emerald       #3FAA7A
--strategist-red           #E25C4B
```

### Backend Data Available for Phase 2 Components
`GET /api/strategist/dashboard` already returns `scoreboard` + `gate_summaries` objects. No new backend routes needed for Phase 2 CD components. See `CODEX_COMMISSION_STR_2EF_SCOREBOARD_GATES.md` for full response shape.

---

## 5. Open Verification Tasks (TT to action)

| ID | Item | Priority | Notes |
|---|---|---|---|
| STR-OP-3 | Verify DashaTimingBar live data on `/strategist/missions` | 🟠 HIGH | DashaTimingBar backend fix shipped (`667fc34`). Verify date ranges + progress bar rendering on production. |
| STR-OP-5 | Verify War Room live data on `/strategist/war-room` post STR-R01 | 🟠 HIGH | Verify: conquest score gauge non-zero, dasha bars show real planet names, mission board ≥1 card, no-profile users see "War Room Locked" gate. |
| STR-SEO-1 | Strategist routes return generic root metadata | 🟠 HIGH | All Strategist routes (`/strategist`, `/strategist/missions`, `/strategist/war-room`) return generic root OG meta instead of route-specific SEO. Fix: add `<SEO>` component to each page with correct title/description/og:image. |

---

## 6. Lal Kitab Module

### Current State
- **No standalone UI yet** -- LK data currently surfaces only via The Strategist
- MongoDB collections **already seeded:**
  - `lalkitab_strategist` -- 823 records (LK rules + Strategist gates)
  - `jyotish_lk_remedies` -- 361 records (planetary remedies by house)
  - `lk_user_profiles` -- schema exists
- Architecture note: `strategist_engine.py` queries `lalkitab_strategist` -- LK data underpins Strategist's 5-gate karmic diagnostics

### Commission to Issue: LK-1

**Brief:** `Codex_Deliveries/LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md`

**What it builds:**
- Onboarding wizard (birth details → LK profile)
- LK Debt Audit (9 debt types, planetary diagnostics)
- 43-day remedy tracker
- Planetary remedies by house (from `jyotish_lk_remedies`)
- Premium PDF download

**Blocker:** TT must batch-approve `jyotish_lk_remedies` records before issuing. Once approved, issue immediately -- no other dependencies.

**Architecture rules (ENFORCE):**
- All planetary/dasha data from `vedic_calculator.py` ONLY
- Route LK UI to existing MongoDB collections (`jyotish_lk_remedies` + `lalkitab_strategist`) -- do NOT create new ones
- LK-1 is independent of Strategist UI -- do not couple in the same commission

### LK Phase 2 (Parking Lot -- do not build yet)
- Slot 33 → LK Debt Audit cross-module trigger (PRAY verdict surfaces Debt Audit)

---

## 7. Architecture Rules (Mandatory)

1. **All dasha/astronomical data** from `backend/vedic_calculator.py` + `pyswisseph` ONLY
2. **Do NOT** add dasha calculation functions to `strategist_router.py`, `strategist_engine.py`, or `knowledge_engine.py`
3. **Strategist approval behaviour:** `strategist_engine.py` queries ALL rules regardless of `approval_status` -- this is intentional, do not add a filter
4. **Do NOT modify** `StrategistWarRoom.jsx` prop signature or any existing War Room sub-components

---

## 8. A2 Session Context

Account 2 (CC A2) had started work on this module. TT has the session export at:
`/Users/apple/Downloads/LK and Strategist Session Export_CC A2`

**When TT opens the new thread:** TT will share the CD work folders (HTML prototypes already in progress) and the A2 session export for context. Read this guide first, then wait for those files before beginning CD work.

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
4. Read `Codex_Deliveries/Strategist/CODEX_COMMISSION_STR_2EF_SCOREBOARD_GATES.md` (first CD brief to send)
5. Wait for TT to share CD work folders and A2 session export
6. Once TT shares, confirm which CD deliveries are already prototyped vs pending
7. Proceed with Phase 2 pipeline in sequence (2F → sign-off → 2E → sign-off → ...)

---
*Handover prepared: 2026-05-29 by Claude Code Main Thread*
