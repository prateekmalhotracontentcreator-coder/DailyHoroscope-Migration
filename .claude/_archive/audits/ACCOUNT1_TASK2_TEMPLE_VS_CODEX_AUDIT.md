# Account 1 -- New Thread Brief: Temple vs Codex Audit (PM Role)
> Created: 2026-05-14 | Self-contained -- read this file only to begin
> Do NOT read SESSION_START.md or other handover docs for this task -- they are for the KE/ingest workflow, not this task.

---

## Your Role This Session

You are acting as **Project Manager** for the EverydayHoroscope Temple App.

A team of 18 Codex AI threads has built modules for the app. An audit team has already completed a cross-thread review and produced a master tracker. Your job is to:

1. Read the audit output
2. Compare what Codex delivered vs what is actually live in the Temple App (the repo)
3. Produce a structured **Findings Report** -- gaps, deviations, priority actions
4. Draft parallel work assignments for each gap module

This is **research and reporting only** -- do not write any code, do not modify any files in the repo.

---

## The App

- **Repo:** `/Users/apple/DailyHoroscope-Migration/`
- **Frontend:** `frontend/src/` (React, Vercel)
- **Backend:** `backend/` (FastAPI, Render/Docker)
- **Live URL:** https://www.everydayhoroscope.in
- **Codex reference build:** `/Users/apple/DailyHoroscope-Codex-Test/` (Codex-delivered files, NOT the live repo)

---

## Step 1 -- Read These Files First (in order)

### 1a. Master Tracker (PM control plane -- 18 modules)
```
/Users/apple/Documents/New project/cross-thread-audit-pack/common-space/MASTER_TRACKER.md
```

### 1b. Module Map (folder locations per thread)
```
/Users/apple/Documents/New project/cross-thread-audit-pack/common-space/02_FOR_PRATEEK/TEMPLE_TEAM_COMMON_SPACE_AND_MODULE_MAP_2026-05-13.md
```

### 1c. Individual thread response summaries (06_RESPONSE_SUMMARY.md)
Path pattern:
```
/Users/apple/Documents/New project/cross-thread-audit-pack/common-space/01_FOR_INDIVIDUAL_THREADS/{thread-folder}/06_RESPONSE_SUMMARY.md
```
Read all 18. Thread folders are:
```
01-notification-engine
02-love-bundle-module
03-lumina
04-palmistry
05-longevity
06-numerology
07-onboarding-questionnaire
08-tarot
09-punya-rewards
10-krishna-prashanavali
11-panchang
12-arc-angel
13-individual-reports
14-live-tv
15-knowledge-engine
16-lagna-kundali
17-shadbala-engine
18-remedies-engine
```

---

## Step 2 -- Verify Against the Live Repo

For each of the 5 priority gap modules below, check the **actual Temple repo** (not the Codex test folder) to confirm current state:

| Module | What to check in repo |
|---|---|
| **Punya Rewards** | Does `frontend/src/lib/punyaRewards.js` exist? Is `punya_rewards_router.py` registered in `backend/server.py`? Is there a route in `frontend/src/App.js`? |
| **Live TV** | Is `LiveTVPanel` component in `frontend/src/components/`? Is `useLiveTv` hook present? Is `live_tv_router` imported in `backend/server.py`? |
| **Knowledge Engine** | Is `knowledge_engine.py` wired in `backend/server.py`? Is `migrate_ch41_varga_checkable.py` present in `backend/scripts/`? |
| **Shadbala Engine** | Does `backend/vedic_calculator.py` contain dignity/combustion/Shadbala functions? Or was it rolled back? |
| **Remedies Engine** | Is there a `remedies_engine.py` or equivalent? Is there a commission brief in `MODULE_REMEDIES_ENGINE`? |

Also do a quick pass on the remaining 13 modules -- confirm their routes are in `App.js` and their backend routers are in `server.py`.

---

## Step 3 -- Produce the Findings Report

Create this file when done:
```
/Users/apple/DailyHoroscope-Migration/.claude/TEMPLE_VS_CODEX_FINDINGS_2026-05-14.md
```

Structure it as follows:

### Section A -- Summary Dashboard
| Module | Codex Status | Temple Status | Gap | Priority |
|---|---|---|---|---|

Use these status values:
- Codex: `complete` | `partial` | `not_started`
- Temple: `live` | `integrated_not_live` | `partial` | `missing` | `rolled_back`
- Gap: `none` | `minor` | `major` | `critical`
- Priority: `P1` | `P2` | `P3` | `hold`

### Section B -- Detailed Gap Analysis (one sub-section per gap module)
For each module with Gap = major or critical:
- What Codex delivered
- What Temple currently has
- What is specifically missing
- Exact files missing or broken
- Recommended action (1-3 sentences)
- Dependency / blocker if any

### Section C -- Work Assignment Drafts
For each P1/P2 gap module, draft a one-paragraph task brief suitable for a new Codex thread or Account 2 session. Include: what to build, which files to touch, what done looks like.

### Section D -- Modules Confirmed Clean
List all modules where Temple = live or integrated, Codex = complete, Gap = none. One line each.

### Section E -- Decisions Required from Prateek
List any gaps where the correct action depends on a product decision (e.g. Lumina UX drift -- is the Temple amendment accepted or should it be reverted?).

---

## Known Pre-Findings (from prior audit -- verify and expand)

These are confirmed issues from the MASTER_TRACKER as of 2026-05-13:

### CRITICAL
| Module | Issue |
|---|---|
| Shadbala Engine | Rolled back in Temple; repo copy errors on `_solar_event_jd()`; dignity/combustion functions missing |
| Knowledge Engine | `knowledge_engine.py` runtime wiring missing; `migrate_ch41_varga_checkable.py` absent |

### MAJOR
| Module | Issue |
|---|---|
| Punya Rewards | Missing `punyaRewards.js`; no `server.py`/`App.js`/`AdminDashboard` wiring; not live |
| Live TV | Missing `LiveTVPanel`, `useLiveTv`, Landing mount, `server.py` router registration; not live |
| Remedies Engine | Not commissioned; pre-commission only |

### MINOR / REVIEW NEEDED
| Module | Issue |
|---|---|
| Lumina | Temple frontend drifted from original spec (extra tabs, different styling); intentional or not? |
| Palmistry | Unsupported astrology-overlay copy in Temple frontend; Phase 2 pending |
| Longevity | Contract reconciliation + runtime verification open |
| Numerology | CTA/payload parity decision open |
| Onboarding Questionnaire | Route is Premium-only instead of free-teaser; Arc Angel embed location differs |
| Tarot | Current Temple build is remediation slice only -- fuller v4 frontend not integrated |
| Arc Angel | Panel questionnaire amendment, premium-lock behavior, persistence/dasha-source decisions open |
| Krishna Prashanavali | Production verification + bundle-contract migration open |

### CONFIRMED CLEAN (verify in repo)
| Module | Status |
|---|---|
| Notification Engine | Backend live; partial channel live |
| Love Bundle | Backend + frontend live |
| Panchang | Live, verified |
| Lagna Kundali | Live, reference-build aligned |
| Individual Reports | Live, all 5 report routers confirmed |

---

## Key File Paths for Repo Checks

```bash
# Check if a route exists
grep -n "lal-kitab\|punya\|live-tv\|shadbala\|knowledge-engine" /Users/apple/DailyHoroscope-Migration/frontend/src/App.js

# Check backend router registrations
grep -n "include_router\|import" /Users/apple/DailyHoroscope-Migration/backend/server.py | head -60

# Check if specific files exist
ls /Users/apple/DailyHoroscope-Migration/frontend/src/lib/
ls /Users/apple/DailyHoroscope-Migration/backend/ | grep -E "shadbala|knowledge|remedies|live_tv|punya"

# Check vedic_calculator.py for Shadbala functions
grep -n "shadbala\|digbala\|combustion\|dignity" /Users/apple/DailyHoroscope-Migration/backend/vedic_calculator.py | head -20
```

---

## Deliverable

One file: `/Users/apple/DailyHoroscope-Migration/.claude/TEMPLE_VS_CODEX_FINDINGS_2026-05-14.md`

Prateek will review this findings report and use it to assign work to Account 2 threads and Codex threads on Sunday.

**Do not push any git commits. Do not modify any repo files. Research and report only.**
