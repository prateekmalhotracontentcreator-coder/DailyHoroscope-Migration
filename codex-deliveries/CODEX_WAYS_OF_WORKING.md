# EverydayHoroscope — Ways of Working with CODEX

> **Single source of truth for all CODEX engagements.**
> Compiled by Temple Team — 29 March 2026
> Supersedes all prior individual constraint notes and partial response documents.

---

## 1. Platform Identity

**EverydayHoroscope is the Temple.**

Each spiritual guidance system is a sibling module inside that temple. CODEX builds individual module pillars. Temple Team integrates, deploys, and operates the live platform.

| Layer | Value |
|---|---|
| Platform name | EverydayHoroscope |
| Live URL | https://www.everydayhoroscope.in |
| Backend API | https://everydayhoroscope-api.onrender.com |
| Repo | `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration` |
| Frontend | React 18 on Vercel |
| Backend | FastAPI on Render (Docker) |
| Database | MongoDB Atlas (Motor async driver) |
| AI Layer | Claude API |

---

## 2. Engagement Model

### Core Rule: CODEX Delivers — Temple Integrates

CODEX is responsible for:
- Building each module as a self-contained drop-in artifact
- Validating deliverables in an isolated Python 3.12 environment
- Producing all required handoff documentation
- NOT attempting to integrate into live Temple App source files

Temple Team is responsible for:
- Receiving and reviewing all drop-in artifacts via `codex-deliveries/` staging folder
- Integrating the module into the live app
- Wiring routes, styling, auth, and collections
- End-to-end testing on staging and production
- Providing sign-off before any deliverable touches production

### Staging Protocol

1. CODEX uploads files to the `codex-deliveries/` folder
2. Temple Team reads, diffs, and validates against the live backend
3. If validation passes → Temple Team moves to `backend/` and deploys
4. If validation fails → Temple Team flags exact issue before anything touches production
5. **Nothing in `codex-deliveries/` touches the live app until explicitly integrated by Temple Team**

---

## 3. Approved Technical Constraints

These are binding. All CODEX deliveries must comply.

### 3.1 Python Target

| Setting | Value |
|---|---|
| **Local validation target** | Python `3.12` |
| **Datetime rule** | Always use `timezone.utc` — never `datetime.UTC` |
| **Local validation deps** | `fastapi`, `pydantic` v2, `uvicorn` only |
| **System Python** | Do NOT modify |

Approved local setup:
```bash
brew install python@3.12
python3.12 -m venv .venv
source .venv/bin/activate
pip install fastapi pydantic uvicorn
```

Compile check pattern (sandbox restriction):
```bash
PYTHONPYCACHEPREFIX='/tmp/pycache' python3.12 -m py_compile yourfile.py
```

### 3.2 Backend Delivery Shape

- **One standalone `APIRouter` file per module** — no multi-file slices for core delivery
- No standalone FastAPI app instance — `APIRouter` only
- No imports from any Temple App source file
- Pydantic v2 with `ConfigDict` — no Pydantic v1 `class Config` style
- `from __future__ import annotations` at top of every file

### 3.3 Router Prefixes

| Module | Prefix |
|---|---|
| Panchang | `/api/panchang` |
| Tarot | `/api/tarot` |
| Numerology | `/api/numerology` |
| Future modules | `/api/{module-name}` |

### 3.4 MongoDB Collections — Single Collection Rule

Each module writes to **one primary collection only**:

| Module | Collection |
|---|---|
| Panchang | `panchang_data` |
| Tarot | `tarot_readings` |
| Numerology | `numerology_results` |
| Future modules | `{module}_results` or `{module}_data` |

- One document per generated report
- `user_email` as the user link key
- Auxiliary state (bookmarks, lifecycle, reminders) stored in same primary collection using `doc_type` field
- **No writes to any existing Temple App collection**
- Read-only access to existing Temple collections permitted if explicitly declared in handoff notes

### 3.5 Auth Pattern

```python
# Approved auth resolution
user_email = request.state.user.get("email")

# Database handle
db = request.app.state.db
```

Fallbacks for isolated local testing only (not for Temple production):
- `X-User-Email` header
- explicit `user_email` request field/query param

### 3.6 What CODEX Must NOT Request

- Existing Temple App source files
- Database credentials or connection strings
- Production dependency lists
- Access to existing backend modules
- Access to live server configurations

---

## 4. Module Delivery Checklist

Every CODEX delivery must include:

### Backend (Required)
- [ ] One standalone `APIRouter` file (e.g., `numerology_router.py`)
- [ ] Python 3.12 syntax — `from __future__ import annotations`, `timezone.utc`, Pydantic v2
- [ ] Single-collection persistence pattern
- [ ] All route signatures stable and documented
- [ ] `py_compile` passes cleanly
- [ ] Deterministic engine self-check passes (where applicable)

### Documentation (Required)
- [ ] `MODULE_TEMPLE_HANDOFF_NOTES.md` — delivery summary, collection rule, read dependencies, integration assumptions
- [ ] `MODULE_TEMPLE_CONTRACT_HANDOFF.md` — contract alignment details
- [ ] Updates to `CROSS_MODULE_BUILD_HANDOVER_ISSUES.md` — any new env/handover findings

### Documentation (Recommended)
- [ ] `MODULE_LOGIC_SOURCE_OF_TRUTH.md`
- [ ] `MODULE_TECHNICAL_IMPLEMENTATION_PLAN.md`
- [ ] Router integration guide
- [ ] Styling integration guide

### Frontend (Where Applicable)
- [ ] Drop-in page components (JSX)
- [ ] Module stylesheet
- [ ] Route integration guide

---

## 5. Module Status — As of 29 March 2026

| Module | Backend Delivered | Frontend Delivered | Live in Production |
|---|---|---|---|
| Panchang | ✅ v11-swiss (Temple) | ✅ PanchangPage.jsx | ✅ |
| Tarot | ✅ tarot_router.py (78 cards + reminders) | ✅ TarotPage.jsx | ✅ |
| Numerology | ✅ numerology_router.py (incl. premium Ankjyotish) | ✅ NumerologyPage.jsx | ✅ |
| Birth Chart / Kundali | ✅ vedic_calculator.py | ✅ BirthChartPage.jsx + BrihatKundliPage.jsx | ✅ |
| Astro-Tarot Fusion | 🔜 Prompt Pack + Engineering Note exists | ❌ Not started | ❌ |
| Palmistry | ❌ Not started | ❌ Not started | ❌ |
| Face Reading | ❌ Not started | ❌ Not started | ❌ |
| Compatibility | ❌ Not started | ❌ Not started | ❌ |

---

## 6. Panchang — Important Version Note

**The dropin/backend/panchang_router.py in CODEX workspace is v3-swiss.**
**Production is currently v11-swiss.**

The CODEX dropin version is **8 versions behind production**. It must not be used as a reference for integration or further Panchang work without a full sync.

If CODEX needs an updated Panchang reference, Temple Team will provide the current version.

---

## 7. Output Constraints Summary

All module outputs must comply with `OUTPUT_CONSTRAINTS_MATRIX.md`.

Key rules:
- **Tarot**: Hard word limits per output key. `card_scene_lines` must be exact arrays. No Astro-Tarot fusion code in the core `tarot_router.py` Temple delivery.
- **Numerology**: Hard word limits per output key. `premium_ankjyotish_report` included in the delivery.
- **Panchang**: Deterministic engine is source of truth. AI must not override calendar values.
- **All modules**: Safe language rules apply — no guaranteed outcomes, no deterministic language for sensitive life events.

For full constraint tables see `OUTPUT_CONSTRAINTS_MATRIX.md`.

---

## 8. Platform Framework Rules

Every new module must answer two questions before work begins:

1. What does it uniquely contribute as a sibling pillar inside the temple?
2. What does it reuse from the shared platform operating system?

All modules share:
- Auth (session/JWT cookie, `withCredentials: true`, no localStorage token storage)
- Premium entitlement logic
- Admin console pattern
- AI governance (safe prompting, structured outputs, premium tone)
- Lifecycle and personalization layer

Each module owns independently:
- Symbolic system
- Feature logic and reading flow
- Data schema extensions
- Prompt templates and output contracts

---

## 9. Astro-Tarot Fusion — Status & Next Steps

Specification complete:
- `ASTRO_TAROT_FUSION_ENGINEERING_NOTE.md` — architecture, layered approach, output contract
- `ASTRO_TAROT_FUSION_PROMPT_PACK.md` — 5 prompts (Lite Daily, Premium Spread, Signature, Favorable Window, Product Bridge)
- `ASTRO_TAROT_VEDIC_CROSS_REFERENCE_UI_SPEC.md` — UI specification

Key architectural principle:
- **Layer 1**: Deterministic Vedic calculation (Swiss Ephemeris engine — Temple side)
- **Layer 2**: Tarot symbolic layer (CODEX)
- **Layer 3**: AI fusion interpreter (CODEX prompts, Temple-side Claude API call)

**Rule**: The model must never invent astrology. It may only interpret deterministic Vedic signals that are explicitly provided in the request payload.

Next deliverable for CODEX: `tarot_router_platform_fusion.py` — the complete fusion router implementation (currently a placeholder/stub).

---

## 10. Environment Issues — Resolved & Ongoing

| Issue | Status | Resolution |
|---|---|---|
| Python 3.9.6 in CODEX workspace | ✅ Resolved | Use Python 3.12 venv per approved contract |
| `datetime.UTC` not available in 3.9 | ✅ Resolved | Always use `timezone.utc` |
| Missing `pydantic` in CODEX workspace | ✅ Resolved | Install `fastapi pydantic uvicorn` in 3.12 venv |
| Sandbox cache write restrictions | ✅ Resolved | Use `PYTHONPYCACHEPREFIX='/tmp/pycache'` |
| Host app router not in CODEX workspace | ✅ Accepted | CODEX delivers; Temple integrates |
| Host CSS entrypoint not in CODEX workspace | ✅ Accepted | CODEX delivers styling; Temple wires |
| PDF extraction tooling unavailable | 🔜 Ongoing | Use text-ready versions where possible |
| Research files in mixed formats (RTF in .md) | 🔜 Ongoing | Validate file encoding early in each module thread |

---

## 11. Communication Protocol

| Item | Owner | Notes |
|---|---|---|
| Contract initiation | Temple Team | Temple defines scope and contract terms |
| Module spec documents | CODEX | PRD, UX Blueprint, Engineering Spec, Prompt Pack |
| Backend delivery | CODEX | Single router file + handoff docs |
| Frontend delivery | CODEX | Drop-in JSX pages + stylesheet + integration guide |
| Integration and wiring | Temple Team | Routes, auth, CSS, collections |
| End-to-end testing | Temple Team | Staging + production |
| Sign-off | Temple Team | Required before deployment |
| Discrepancy flagging | Temple Team | Via updated `CODEX_INCONSISTENCIES.md` |
| New constraint discoveries | CODEX | Via updated `CROSS_MODULE_BUILD_HANDOVER_ISSUES.md` |

---

## 12. Do Not Repeat List

Lessons learned — do not repeat these mistakes:

1. **Do not use `datetime.UTC`** — always `timezone.utc`
2. **Do not deliver multi-file backend slices** as the primary Temple artifact — one router file only
3. **Do not write to multiple MongoDB collections** — one primary collection per module
4. **Do not embed Astro-Tarot fusion code in the core `tarot_router.py`** — keep fusion in `tarot_router_platform_fusion.py`
5. **Do not assume CODEX workspace Python matches production** — always validate in an isolated 3.12 venv
6. **Do not reference the dropin panchang_router.py as current** — production is v11-swiss; dropin is v3-swiss
7. **Do not modify system Python** in the CODEX workspace
