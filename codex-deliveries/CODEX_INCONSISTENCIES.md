# CODEX Engagement — Inconsistencies & Discrepancies

> Compiled by Temple Team — 29 March 2026
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
| Files affected | `Response to Codex_Env Constraints.txt` (Desktop), `CODEX_MASTER_RESPONSE_MARCH2026.md` (Downloads), `Delayed response to Codex on Infra Updates.rtf` (Desktop) |

**Detail:** These three files were referenced in the review brief but are stored in Desktop and Downloads directories, which are inaccessible to Claude Code. Their content could not be reviewed.

However, key content from `Response to Codex_Env Constraints.rtf` has already been captured and codified in `TEMPLE_APP_MODULE_DELIVERY_CONTRACT.md` (which cites it as its source). The essential constraints from that document are therefore already in the Ways of Working.

**Resolution:** Move these files to the repo `codex-deliveries/` folder or `Documents/` so they are accessible for future reviews. The CODEX_MASTER_RESPONSE_MARCH2026.md is particularly important — please move it.

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

### INC-09 — DELIVERY_STATUS.md README Still Shows All Contracts as "Awaiting Delivery"

| Field | Value |
|---|---|
| Severity | 🟢 Low |
| File | `/DailyHoroscope-Migration/codex-deliveries/README.md` |

**Detail:** The contract status table in README.md still shows all contracts as "⏳ Awaiting delivery" despite all contracts (1, 2, 3, 4, 4b, 5, 6) being delivered and validated per DELIVERY_STATUS.md.

**Resolution:** Temple Team to update README.md contract table to reflect completed status.

---

## Summary Table

| ID | Description | Severity | Status |
|---|---|---|---|
| INC-01 | Panchang dropin v3 vs production v11 | 🔴 Critical | Action needed |
| INC-02 | PYTHON_VERSION.md contradicts live Dockerfile | 🔴 Critical | Action needed |
| INC-03 | tarot_router_platform_fusion.py is empty stub | 🔴 Critical | Pending contract |
| INC-04 | Desktop/Downloads files not accessible | 🟡 Medium | Move files |
| INC-05 | Tarot handoff notes missing from New project 2 | 🟡 Medium | Consolidate |
| INC-06 | Duplicate workspace folders (New project + New project 2) | 🟡 Medium | Archive older |
| INC-07 | CODEX workspace Python was 3.9 vs contract 3.12 | 🟢 Low | Resolved |
| INC-08 | PROJECT_STATUS.md has outdated frontend status | 🟢 Low | Update needed |
| INC-09 | codex-deliveries/README.md contract table outdated | 🟢 Low | Update needed |
