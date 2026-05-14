# Handover Brief -- 2026-05-11 (Evening)
> Supersedes: HANDOVER_2026-05-11.md

---

## What Is Live (Updated 2026-05-12)

| Module | Status | Notes |
|---|---|---|
| LK Standalone (Onboard → Report → Tracker → Browse) | ✅ LIVE | Full UX pass done 2026-05-11 |
| All 5 Remedy Modules (Dana, Gemstones, Crystal, Chakra, Mantra) | ✅ LIVE | 3-view paid report flow |
| LK Onboard -- birth details → auto-compute Jyotish + LK chart | ✅ LIVE | Auth fixed |
| The Strategist War Room + Missions + Report + Surrogate | ✅ LIVE | Phase 2A-2I verified live |
| Notification Engine (all channels) | ✅ LIVE | |
| Panchang, Tarot, Numerology, Birth Chart, Horoscopes | ✅ LIVE | |
| KP Oracle (`/krishna-prashnavali`) | ✅ LIVE | v2 bundle active; Phase 2 runtime wiring complete (commit `81bea2f`) |
| KP Phase 2 Runtime Wiring | ✅ LIVE | behavioral_remedy + remedy_ref resolved via Remedies Engine; ritual_remedy + ritual_mantra in summary_report |
| Strategist Patch Ingest (22 records) | ✅ LIVE | IDs 1011-1020 + 1126-1137 in knowledge_rules; approval_status=pending_human_review |

---

## Phase 2 UX Fixes -- Completed This Session (All Deployed)

Last commit batch: `118649e` -- covers all items below.

### Auth Fix (All Pages)
- Root cause: app uses HTTP-only session cookies (`credentials: 'include'`), but LK/Strategist pages were using `localStorage.getItem('token')` (always empty)
- Fix applied to 9 files: `LKOnboardPage.jsx`, `LKReportPage.jsx`, `LKDebtAuditPage.jsx`, `LKTrackerPage.jsx`, `LKBrowsePage.jsx`, `StrategistPage.jsx`, `StrategistMissionsPage.jsx`, `StrategistReportPage.jsx`, `StrategistSurrogatePage.jsx`, `StrategistActionPlanPage.jsx`

### Strategist Page
- Background: removed `WAR_ROOM_BG` gradient constants; outer div now `bg-background`
- Layout order: War banner → Conquest Gauge + Layer 1 (AstrologyStrip) → Gate 0 → Layer 2 (LK 5-Gate) → Layer 3 (Missions)
- Redo Setup button: always visible when not loading; `Link` to `/lk-remedies/onboard`
- Data fetch lifted into Dashboard component -- both `gate0/status` and `dashboard` fetched there

### LK Report Page (`LKReportPage.jsx`)
- `GATE_CONTEXT` object: per-gate `what` and `why` narrative
- `GateCard` rewritten as collapsible accordion; shows context block + narrative result
- Back button: `← The Strategist`
- Tracker add: replaced `alert()` with bottom-sheet toast (`fixed inset-0 z-50`)
- Toast calls `POST /api/lk/tracker/start` to initialise tracker, then navigates to `/lk-remedies/tracker`
- Uses `useNavigate` for programmatic navigation

### LK Debt Audit Page (`LKDebtAuditPage.jsx`)
- Full rewrite -- was crashing due to `}, [token])` where `token` was removed
- `DebtCard` now collapsible accordion with expand/collapse toggle
- `DEBT_LABELS` mapping: `Mitra Rin` → `Social Circle / Friend Debt` etc.
- Shows relative availability, surrogate ritual vs primary remedy
- Back button: `← Diagnostic Report`
- Better empty state and error state

### LK Tracker Page (`LKTrackerPage.jsx`)
- Replaced `localStorage.getItem('token')` + JWT decode with `useAuth()` hook
- Empty state: directs user to Diagnostic Report first
- Back link at top in both empty and active states
- Log button: disabled until all 3 checkboxes checked

### Backend (`lk_remedies_router.py`)
- New endpoint: `POST /api/lk/tracker/start`
- Initialises tracker with `streak_days: 0, status: "active"`, no day log entry
- Returns `already_exists` if tracker already present (idempotent)

---

## Remedies Engine Commission -- Status (Updated 2026-05-11 night)

| Item | Status |
|---|---|
| Spec (`REMEDIES_ENGINE_SPEC_V1.md`) | ✅ Written 25 Apr 2026 |
| Green Light Memo (`CODEX_GREEN_LIGHT_MEMO.md`) | ✅ Reviewed 2 May 2026 |
| KP-side schema (`KRISHNA_ORACLE_REMEDY_ENGINE_SCHEMA.md`) | ✅ Delivered by KP Codex |
| KP ingest records (`KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json`) | ✅ 36 temple-reviewed records, ready |
| KP v2 bundle (`KRISHNA_ORACLE_CONTENT_CANONICAL_V2_FOR_TEMPLE.json`) | ✅ `behavioral_remedy` + `remedy_ref` across all 36 slots |
| Commission brief (`.claude/CODEX_COMMISSION_REMEDIES_BRIEF.md`) | ✅ Written and issued to Codex |
| `remedies_router.py` -- 3 new endpoints (`/suggest`, `/rule/{id}`, `/traditions`) | ✅ **Delivered and deployed** |
| `BirthChartPage.jsx` -- Report / Remedies tab set | ✅ **Delivered and deployed** |
| `server.py` -- `planets`+`houses` stored; backfill on re-generate | ✅ **Delivered and deployed** |
| Ingest script `ingest_krishna_prashnavali_remedies_v1.py` | ✅ Delivered -- dry-run verified 36 records clean |
| `krishna_prashnavali_remedies` MongoDB collection | ✅ **36 records ingested + approved** (2026-05-11) |

**Key architecture decisions locked:** Engine queries existing collections only. No new `remedies_rules` collection.
**KP runtime wiring** (`remedy_ref` in KP answer display) = Phase 2.

KP remedies fully live -- ingest + approval completed 2026-05-11. Verdict split: YES:10, PRAY:10, NO:8, WAIT:8.

---

## Phase 2 -- Full Reconciliation (verified 2026-05-12)

All Phase 2 items confirmed live. Handover docs were behind -- prior sessions built 2B-2I without updating docs.

| Step | Task | Status | Key Detail |
|---|---|---|---|
| **2A-1** | KP direct link in NavBar | ✅ Live | Line 88 of `NavBar.jsx`; Blog/Careers Footer-only |
| **2A-2** | Migrate 5 KP files | ✅ Live | All 5 files in live codebase; v1 bundle at `backend/assets/krishna_oracle/krishna_oracle_content.json` |
| **2A-3** | Register route + router | ✅ Live | `App.js` line 78 lazy import + line 225 `ProtectedRoute`; `server.py` line 102 import + line 2085 register |
| **2B** | Gate 0 inline in War Room | ✅ Live | `Gate0Panel` in `StrategistPage.jsx` -- embeds `KrishnaOracleGrid`, calls `POST /api/strategist/gate0/select` which injects live Dasha + transit astro context into the KP oracle reading |
| **2C** | WAIT/NO/PRAY banners | ✅ Live | `VerdictBanner` (all 3 configs), `PreFlightPanel` (WAIT/NO), `PraySurrenderPanel` (PRAY full surrender) |
| **2D** | Score-gated re-entry | ✅ Live | `GET /api/strategist/gate0/status` -- NO: `can_retest` at ≥60%, PRAY: at ≥75%; TTL: YES=7d, WAIT=3d, NO=1d, PRAY=1d |
| **2E** | LK 5-Gate summaries in dashboard | ✅ Live | `gate_summaries` array (gates 1-5 with status + narrative) in `GET /api/strategist/dashboard` response |
| **2F** | Conquest Scoreboard in War Room | ✅ Live | `scoreboard` block: conquest_score, tier, streak, gate0_last_verdict, next_threshold + label, points_to_next |
| **2G** | Unified Action Plan page | ✅ Live | `StrategistActionPlanPage.jsx` + `GET /api/strategist/action-plan` -- prioritised actions with gate0 state, remedy, score |
| **2H** | 7 Strategist notification triggers | ✅ Live | All 7 in `notification_trigger_router.py`: `gate0-expired`, `streak-at-risk`, `streak-milestone`, `score-unlocked`, `mission-activated`, `golden-hour`, `debt-cleared` |
| **2I** | PRAY path -- Mantra + Debt Audit | ✅ Live | `PraySurrenderPanel` calls `GET /api/strategist/surrender-context` -- surfaces featured mantra (Saturn/Ketu tags), gate1 narrative, 3-step surrender sequence, links to Debt Audit + Mantra Remedies |

### KP Bundle Note
Live codebase uses **v1 bundle** (`content_status: "canonical"`) with inline `remedy` + `mantra` fields -- required by current `KrishnaCanonicalAnswer` Pydantic schema.
**v2 bundle** is now LIVE at `backend/assets/krishna_oracle/krishna_oracle_content.json` (commit `81bea2f`).
KP Phase 2 runtime wiring complete -- see section below.

---

## KP Phase 2 Runtime Wiring -- Completed 2026-05-12 (commit `81bea2f`)

| Item | Detail |
|---|---|
| Bundle | Swapped v1 → v2 (`canonical-v2-temple-reviewed`, 36 answers) |
| `KrishnaCanonicalAnswer` schema | `remedy` + `mantra` → `Optional` (None in v2); added `behavioral_remedy` + `remedy_ref` |
| `_resolve_kp_remedy_doc()` | New async helper -- queries `krishna_prashnavali_remedies` by `remedy_ref` + `approval_status=approved` |
| `_practical_action_block()` | Uses DB `ritual_remedy`; falls back to inline v1 `remedy` |
| `_summary_report()` | Adds `ritual_remedy` + `ritual_mantra` keys from DB record |
| `select` endpoint | Awaits `_resolve_kp_remedy_doc` if `answer.remedy_ref` present |
| `KrishnaOraclePage.jsx` | Shows `behavioral_remedy` as "Sacred Practice"; `ritual_remedy` + `ritual_mantra` from summary_report; graceful v1 fallback |
| Fallback | If DB lookup returns None -- `practical_action` uses `what_to_do` only; remedy/mantra slots render nothing (no crash) |

---

## Pending Items

- **5 split-required LK rules** -- approved but tagged `split_required=True`:
  `lalkitab-ch21-fam-04`, `lalkitab-ch24-age-childhood-12m`, `lalkitab-ch24-age-infancy-12d`, `lalkitab-ch24-age-shortlife-2y`, `lalkitab-ch24-age-survival-son`
- **Strategist patch 22 records** -- ✅ ingested (modified=22, upserted=0); `approval_status=pending_human_review` -- needs human approval pass before engine serves them

---

## Key Spec Files

```
.claude/THE_STRATEGIST_SPEC.md          ← Full Strategist spec incl. Phase 2 (§P2)
.claude/LK_STANDALONE_MODULE_SPEC.md    ← LK Standalone spec (all built)
.claude/REMEDIES_ENGINE_SPEC_V1.md      ← Remedies Engine (spec done, not commissioned)
.claude/ACCOUNT2_SESSION_START.md       ← Quick-start for Phase 2 sessions
/Users/apple/Documents/New project/cross-thread-audit-pack/common-space/
  TEMPLE_HANDOVER_KP_AND_REMEDIES_2026-05-11.md  ← KP + Remedies full decisions
  TEMPLE_BUILD_BRIEF_KP_REMEDIES_2026-05-11.md   ← Build brief
```

---

## Architecture Rules (MANDATORY)

1. ALL live astronomical/dasha data from `vedic_calculator.py` only -- never replicate
2. `knowledge_rules` collection always filtered by `science_id`
3. All notifications via existing `/api/notifications/trigger/{type}` -- never call push/WA directly
4. Remedies Engine is downstream-only for KP -- never overrides KP answer/verdict
5. Commit format: `feat(scope):` / `fix(scope):` / `chore(scope):`
6. Bump `ENGINE_VERSION` in `panchang_router.py` before any backend change
7. All fetch calls must use `credentials: 'include'` (app uses HTTP-only session cookies, not localStorage tokens)
