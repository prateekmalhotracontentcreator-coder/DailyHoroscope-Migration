# CODEX Engagement — Inconsistencies & Discrepancies

> Compiled by Temple Team — 29 March 2026
> Updated: 29 March 2026 (added INC-10 through INC-13 from newly reviewed source files)
> Sources reviewed: `Response to Codex_Env Constraints.txt` · `CODEX_MASTER_RESPONSE_MARCH2026.md` · `Delayed response to Codex on Infra Updates.rtf`
> These items require resolution or acknowledgment before new contracts proceed.

---

## CRITICAL

### INC-01 — Panchang Dropin Version Is 8 Versions Behind Production

| Field | Value |
|---|---|
| Severity | 🔴 Critical |
| File | `New project/dropin/backend/panchang_router.py` |
| CODEX dropin version | `panchang-router-v3-swiss` |
| Production version | `panchang-router-v11-swiss` |

**Detail:** The panchang_router.py inside the CODEX dropin workspace (New project/dropin/backend) is v3-swiss. The live production engine is v11-swiss — 8 major iterations ahead. It includes Moonrise/Moonset, Brahma Muhurta, Vijaya Muhurta, Amrit Kalam, Special Yogas (Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga), True Choghadiya, 91-city catalogue, and a verified accuracy benchmark against Drik Panchang.

**Resolution required:** If any future CODEX contract references Panchang, Temple Team will provide the current production version (v11-swiss). The dropin version must NOT be used as a reference, base file, or integration target.

---

### INC-02 — PYTHON_VERSION.md Is Outdated and Contradicts Live Dockerfile

| Field | Value |
|---|---|
| Severity | 🔴 Critical |
| File | `/DailyHoroscope-Migration/PYTHON_VERSION.md` |

**What it says:**
- Backend locked to Python 3.11
- Dockerfile is `FROM python:3.11-slim`
- requirements.txt contains `flatlib==0.2.3`
- "Do not target Python 3.12 for local validation environments"

**What is actually true:**
- Dockerfile is `FROM python:3.12.9-slim` (Python 3.12 already in production)
- `flatlib` has been removed; migration to `pyswisseph` is complete (per DELIVERY_STATUS.md)
- `TEMPLE_APP_MODULE_DELIVERY_CONTRACT.md` specifies Python 3.12 as the approved target
- CODEX's own `CROSS_MODULE_BUILD_HANDOVER_ISSUES.md` confirms Python 3.12 target
- `Response to Codex_Env Constraints.txt` explicitly confirms 3.12 as the approved target

**Resolution:** PYTHON_VERSION.md must be updated by Temple Team to reflect the current reality. This document is currently actively misleading for any new CODEX engagement that reads it. *(Action: Temple Team to update or retire PYTHON_VERSION.md.)*

---

### INC-03 — tarot_router_platform_fusion.py Is an Empty Stub

| Field | Value |
|---|---|
| Severity | 🔴 Critical for Astro-Tarot Fusion contract |
| File | `New project 2/dropin/backend/tarot_router_platform_fusion.py` |

**Detail:** The file contains only 1 line (empty/placeholder). The Astro-Tarot Fusion contract was scoped and documented (Engineering Note, Prompt Pack, PRD, UI Spec all exist), but the actual implementation file was never delivered.

Note: Per `TAROT_TEMPLE_CONTRACT4_CONTRACT6_HANDOFF.md`, this was intentionally preserved as a placeholder: *"The richer platform/router exploration has been preserved separately and is not the Temple artifact."* The fusion router is therefore an **outstanding deliverable**, not a defect in a completed contract.

**Resolution:** Astro-Tarot Fusion should be formally scoped as the next pending contract for CODEX to deliver.

---

## MEDIUM

### INC-04 — Desktop and Downloads Folders Not Accessible to Temple Team

| Field | Value |
|---|---|
| Severity | 🟡 Medium |
| Status | ✅ Resolved — 29 March 2026 |
| Files affected | `Response to Codex_Env Constraints.txt` · `CODEX_MASTER_RESPONSE_MARCH2026.md` · `Delayed response to Codex on Infra Updates.rtf` |

**Detail:** These three files were stored in Desktop and Downloads directories, which were inaccessible to Claude Code due to macOS Privacy & Security restrictions.

**Resolution:** All three files moved by Temple Team to `Documents/New project/` on 29 March 2026. All three have been reviewed and their contents incorporated into `CODEX_WAYS_OF_WORKING.md`. See INC-10, INC-11, INC-12, INC-13 for new findings from those files.

---

### INC-05 — TAROT_TEMPLE_HANDOFF_NOTES.md Exists in New project Only, Not New project 2

| Field | Value |
|---|---|
| Severity | 🟡 Medium |
| Location found | `New project/dropin/backend/TAROT_TEMPLE_HANDOFF_NOTES.md` |
| Location missing | `New project 2/dropin/` |

**Detail:** The Tarot handoff notes exist in `New project/dropin/backend/` but not in `New project 2/dropin/`. Since both folders appear to be CODEX workspace snapshots, the newer `New project 2` folder is missing this key handoff document.

**Resolution:** Confirm which folder is the authoritative current workspace. Consolidate into one folder and archive the other.

---

### INC-06 — Two Parallel Workspace Folders with Duplicate Content

| Field | Value |
|---|---|
| Severity | 🟡 Medium |
| Folders | `Documents/New project` and `Documents/New project 2` |

**Detail:** Both folders contain near-identical file structures and document sets (both have the same list of ~60+ files). This creates confusion about which is the authoritative current workspace and which is a prior snapshot.

**Resolution:** Temple Team to confirm:
- Which folder is the **current active workspace** (presumed: `New project 2`)
- Which folder is the **archived prior workspace** (presumed: `New project`)
- Archive the older folder so only one is active

---

## LOW

### INC-07 — CONTRACT Specifies Python 3.12 But CODEX Workspace Was Python 3.9

| Field | Value |
|---|---|
| Severity | 🟢 Low (now resolved) |
| Source | `environmentconstraints.md`, `CLAUDE_ENVIRONMENT_REVIEW_SUMMARY.md` |

**Detail:** The CODEX workspace had Python 3.9.6 at time of earlier module builds. The Temple Team provided the correct target (Python 3.12) in `TEMPLE_APP_MODULE_DELIVERY_CONTRACT.md`.

**Status:** Resolved. CODEX confirmed use of Python 3.12 venv for validation per the approved contract. Both Tarot and Numerology Temple deliverables were validated against Python 3.12.

---

### INC-08 — PROJECT_STATUS.md Has Outdated Front End Status

| Field | Value |
|---|---|
| Severity | 🟢 Low |
| File | `/DailyHoroscope-Migration/PROJECT_STATUS.md` |

**Detail:** PROJECT_STATUS.md (last updated 26 March 2026) still shows Tarot, Numerology, and Kundali frontends as "❌ Not started" and Subscription/Paywall as "❌ Not started." All four are now live in production.

**Status:** Partially resolved — CLAUDE.md has been updated (29 March 2026). PROJECT_STATUS.md needs a separate update pass.

---

### INC-09 — DELIVERY_STATUS.md README Contract Table Was Outdated

| Field | Value |
|---|---|
| Severity | 🟢 Low |
| File | `/DailyHoroscope-Migration/codex-deliveries/README.md` |
| Status | ✅ Resolved — 29 March 2026 |

**Detail:** The contract status table in README.md previously showed all contracts as "⏳ Awaiting delivery" despite contracts 1–6 being delivered and validated.

**Resolution:** README.md updated 29 March 2026. All delivered contracts now show "✅ Delivered, validated, live". Contract 7 shows "🔜 Stub exists — pending CODEX delivery". Contract 8 added as "🔒 Pending contract scoping".

---

## NEW — From Source File Review (29 March 2026)

### INC-10 — CODEX_MASTER_RESPONSE_MARCH2026.md Was Not Referenced as Master Document

| Field | Value |
|---|---|
| Severity | 🟡 Medium |
| Source file | `Documents/New project/CODEX_MASTER_RESPONSE_MARCH2026 (1).md` (dated 25 March 2026) |
| Status | ✅ Resolved — incorporated into CODEX_WAYS_OF_WORKING.md |

**Detail:** `CODEX_MASTER_RESPONSE_MARCH2026.md` is the definitive, comprehensive Temple Team response that supersedes all prior individual constraint responses. It was not previously referenced in any working document as the authoritative source. Key contents not previously captured:

- **Section 3** — Live architecture confirmed: `horoscope_db` database, Claude Sonnet 4 as AI engine, Backend API at `https://everydayhoroscope-api.onrender.com`
- **Section 7** — All contracts with priority and order explicitly stated
- **Section 8** — Three-lane ownership model (Lane 1: Temple Team owns; Lane 2: Joint; Lane 3: CODEX backend only)
- Explicit statement: *"This document supersedes all previous individual responses."*

**Resolution:** All key content incorporated into `CODEX_WAYS_OF_WORKING.md` Sections 1, 3, 4.5, and 6. The master response document itself is now accessible at `Documents/New project/`.

---

### INC-11 — CODEX Self-Identified: tarot_router.py Had Out-of-Scope Code Pre-Delivery

| Field | Value |
|---|---|
| Severity | 🟢 Low (resolved in final delivery) |
| Source | `Documents/New project/Delayed response to Codex on Infra Updates.rtf` |
| Status | ✅ Resolved — confirmed clean in final delivery |

**Detail:** CODEX self-identified that an intermediate version of `tarot_router.py` contained out-of-scope code that should not have been there:
- Astro-Tarot fusion logic embedded directly in `tarot_router.py` (should only live in `tarot_router_platform_fusion.py`)
- A `POST /api/tarot/reminder/dispatch` route (not a contracted route)
- APScheduler helper functions (scheduler lives in `server.py` on Temple Team side)

**Resolution:** All three items removed before final delivery. The validated live `tarot_router.py` contains none of these. Rule codified in `CODEX_WAYS_OF_WORKING.md` Section 5 (delivery checklist) and Section 14 items 4 and 5.

---

### INC-12 — CODEX Self-Identified: Reminder API Had Wrong Route Shape and Wrong Document Fields

| Field | Value |
|---|---|
| Severity | 🟢 Low (resolved in final delivery) |
| Source | `Documents/New project/Delayed response to Codex on Infra Updates.rtf` |
| Status | ✅ Resolved — confirmed correct shape in final delivery |

**Detail:** CODEX self-identified two reminder API discrepancies in an intermediate build:

1. **Wrong route**: Built `POST /api/tarot/reminder` instead of contracted `POST /api/tarot/reminder/set`
2. **Wrong document fields**: Used `hour_utc`, `minute_utc`, `channel`, `focus_area`, `next_run_at`, `last_sent_on` — none of which are part of the Temple reminder document model

**Correct contracted shape:**
```
POST   /api/tarot/reminder/set
GET    /api/tarot/reminder
DELETE /api/tarot/reminder
```
Fields: `reminder_time`, `frequency`, `timezone`, `enabled` only.

**Resolution:** Final delivery uses correct routes and document fields. Exact specification codified in `CODEX_WAYS_OF_WORKING.md` Section 8.

---

### INC-13 — CODEX Self-Identified: tarot_cards.json Was Delivered in Wrong Format (Intermediate Build)

| Field | Value |
|---|---|
| Severity | 🟢 Low (resolved in final delivery) |
| Source | `Documents/New project/Delayed response to Codex on Infra Updates.rtf` |
| Status | ✅ Resolved — confirmed correct format in final delivery |

**Detail:** CODEX self-identified that an intermediate version of `tarot_cards.json` used a manifest-style wrapper format instead of the required flat object. Additionally, Minor Arcana card IDs used a non-standard naming convention.

**What was wrong:**
- JSON had a manifest wrapper / `deck` object / `cards[]` array structure
- Minor Arcana IDs did not use the required `{suit}-{rank}` format

**What was required and delivered:**
- Flat JSON object: `{ "card-id": "<svg...>", ... }` — 78 keys, no wrapper
- Major Arcana: slug format (`the-fool`, `the-world`, etc.)
- Minor Arcana: `{suit}-{rank}` format (`wands-ace`, `cups-07`, `swords-king`, `pentacles-page`)

**Resolution:** Final delivery is a flat 78-key object with correct ID format. Exact specification codified in `CODEX_WAYS_OF_WORKING.md` Section 9.

---

## Summary Table

| ID | Description | Severity | Status |
|---|---|---|---|
| INC-01 | Panchang dropin v3 vs production v11 | 🔴 Critical | ⚠️ Action needed |
| INC-02 | PYTHON_VERSION.md contradicts live Dockerfile | 🔴 Critical | ⚠️ Action needed |
| INC-03 | tarot_router_platform_fusion.py is empty stub | 🔴 Critical | 🔜 Pending contract |
| INC-04 | Desktop/Downloads files not accessible | 🟡 Medium | ✅ Resolved |
| INC-05 | Tarot handoff notes missing from New project 2 | 🟡 Medium | ⚠️ Consolidate |
| INC-06 | Duplicate workspace folders (New project + New project 2) | 🟡 Medium | ⚠️ Archive older |
| INC-07 | CODEX workspace Python was 3.9 vs contract 3.12 | 🟢 Low | ✅ Resolved |
| INC-08 | PROJECT_STATUS.md has outdated frontend status | 🟢 Low | ⚠️ Update needed |
| INC-09 | codex-deliveries/README.md contract table outdated | 🟢 Low | ✅ Resolved |
| INC-10 | CODEX_MASTER_RESPONSE_MARCH2026.md not referenced as master document | 🟡 Medium | ✅ Resolved |
| INC-11 | tarot_router.py had out-of-scope fusion/dispatch/scheduler code | 🟢 Low | ✅ Resolved |
| INC-12 | Reminder API had wrong routes and wrong document fields | 🟢 Low | ✅ Resolved |
| INC-13 | tarot_cards.json delivered in manifest format (intermediate build) | 🟢 Low | ✅ Resolved |
