# EverydayHoroscope — Ways of Working with CODEX

> **Single source of truth for all CODEX engagements.**
> Compiled by Temple Team — 29 March 2026
> Sources: CODEX_MASTER_RESPONSE_MARCH2026.md · CROSS_MODULE_BUILD_HANDOVER_ISSUES.md ·
> TEMPLE_APP_MODULE_DELIVERY_CONTRACT.md · CLAUDE_ENVIRONMENT_REVIEW_SUMMARY.md ·
> EVERYDAY_HOROSCOPE_MODULAR_PLATFORM_FRAMEWORK.md · Prior engagement chat history
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
| Backend | FastAPI on Render (Docker, Python 3.12) |
| Database | MongoDB Atlas — `horoscope_db` |
| AI Engine | Claude Sonnet 4 via Anthropic API |
| Email | Resend — noreply@everydayhoroscope.in |
| Payments | Razorpay (new test keys active Mar 2026; live keys pending Play Store) |

---

## 2. Engagement Model

### Core Rule: CODEX Delivers — Temple Team Integrates

> *"You deliver, we integrate."* — Response to Codex_Env Constraints.txt

**CODEX is responsible for:**
- Building each module as a self-contained drop-in artifact
- Validating deliverables in an isolated Python 3.12 environment
- Producing all required handoff documentation
- **NOT** attempting to integrate into live Temple App source files

**Temple Team is responsible for:**
- Receiving and reviewing all drop-in artifacts via `codex-deliveries/` staging folder
- Integrating the module into the live app
- Wiring routes, styling, auth, and collections
- End-to-end testing on staging and production
- Providing sign-off before any deliverable touches production

### Staging Protocol

1. CODEX maintains all deliverable files in the **dedicated CODEX workspace folder** (Documents/New project or New project 2)
2. CODEX maintains **document nomenclature and version control** within that folder — each file must be clearly named and versioned before handoff
3. Temple Team receives the deliverables, reviews, and diffs against the live backend
4. If validation passes → Temple Team moves to `backend/` and deploys; file is also committed to `codex-deliveries/` in the GitHub repo for version history
5. If validation fails → Temple Team flags exact issue before anything touches production
6. **Nothing touches the live app until explicitly integrated and signed off by Temple Team**

---

## 3. Ownership Model — Three Lanes

Defined in `CODEX_MASTER_RESPONSE_MARCH2026.md` Section 8. **This is the operating model.**

### Lane 1 — Temple Team (Claude) Owns End-to-End

No CODEX input required. Temple Team executes these independently.

| Item | Notes |
|---|---|
| PDF download — Numerology reports | Adapts existing `pdf_generator.py` pattern (live for Birth Chart + Brihat Kundli) |
| PDF download — Tarot readings | Same pattern; landscape layout with portrait card assets from Contract 4 |
| Share function — Numerology and Tarot | `ShareModal` live; wire to `report_id` from each module |
| Payment gating — Numerology and Tarot | Same Razorpay pattern live on Birth Chart and Brihat Kundli |
| Tarot cinematic redesign | Full `TarotPage.jsx` redesign — portrait card layout, dark aesthetic, flip animations |
| Tarot XP / gamification display | XP data already returned by `tarot_router.py`; build points table and level UI |
| Tarot TTS narration (Premium) | Browser Web Speech API — no backend needed |
| Numerology AI interpretation layer | Claude API call added to report display — no new backend endpoint needed |
| SEO rich pages — Tarot / Numerology / Panchang | FAQ pages, card pages, Life Path articles, festival pages, schema markup |
| Onboarding guided tour | 5-step overlay coach marks, first-visit detection via localStorage |
| Logo, brand identity, design system | Locked and live |
| Docker and runtime upgrades | Mechanical step after each CODEX delivery. Temple Team only |
| Facebook Page posting | ✅ Live — one-click from Panchang + Horoscope pages + Admin Console |
| YouTube posting | ✅ Live — share card → MP4 → YouTube Shorts via Admin Console |
| Admin Console social media tab | ✅ Live |
| WhatsApp notifications | 🔜 Live backend; pending phone verification + Meta payment method |

### Lane 2 — Joint (CODEX Backend First, Temple Team Builds Frontend)

Temple Team does not begin frontend work until the backend contract is confirmed live.

| Item | CODEX Delivers | Temple Team Builds |
|---|---|---|
| Tarot card illustrations | Contract 4 — 78-card `tarot_cards.json` | Wire assets into `TarotPage.jsx` ✅ Done |
| Panchang interactive calendar | Contract 5 — `/api/panchang/date/{date}` | Interactive calendar UI with linked date pages ✅ Done |
| Festival pages | Festival data in `/festivals` endpoint | Active festival page links and SEO pages |
| Panchang NavBar dropdown | Panchang sub-routes | Frontend routing — dropdown items to live pages |
| Tarot daily reminder | Contract 6 — 3 reminder endpoints | Browser notification permission UI, time picker |
| **Astro-Tarot Fusion** | **Contract 7 — `tarot_router_platform_fusion.py`** | **Vedic Cross-Reference UI block in reading pages** |

### Lane 3 — CODEX Backend Only

Purely backend tasks; no frontend dependency until delivered.

| Contract | Status |
|---|---|
| `vedic_calculator.py` flatlib → pyswisseph | ✅ Delivered + Live |
| `panchang_router.py` pyswisseph upgrade | ✅ Delivered + Live (v11-swiss in production) |
| Premium Ankjyotish Numerology tile | ✅ Delivered + Live |
| Tarot Major Arcana SVG assets (78-card bundle) | ✅ Delivered + Live |
| Panchang per-date endpoint | ✅ Delivered + Live |
| Tarot daily reminder — 3 endpoints | ✅ Delivered + Live |
| **Astro-Tarot Fusion router** | **🔜 Pending — stub exists** |

---

## 4. Approved Technical Constraints

These are binding. All CODEX deliveries must comply.

### 4.1 Python Target

| Setting | Value | Source |
|---|---|---|
| **Local validation target** | Python `3.12` | Response to Codex_Env Constraints.txt |
| **Datetime rule** | Always use `timezone.utc` — never `datetime.UTC` | Confirmed in both constraint responses |
| **Local validation deps** | `fastapi`, `pydantic` v2, `uvicorn` only | Approved venv pattern |
| **System Python** | Do NOT modify | All constraint docs |

> *"Your existing mitigation — timezone.utc — is correct and consistent with our codebase. Please keep it."*
> — Response to Codex_Env Constraints.txt

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

### 4.2 Backend Delivery Shape

- **One standalone `APIRouter` file per module** — no multi-file slices for core delivery
- No standalone FastAPI app instance — `APIRouter` only
- No imports from any Temple App source file
- Pydantic v2 with `ConfigDict` — no Pydantic v1 `class Config` style
- `from __future__ import annotations` at top of every file

### 4.3 Router Prefixes

| Module | Prefix |
|---|---|
| Panchang | `/api/panchang` |
| Tarot | `/api/tarot` |
| Numerology | `/api/numerology` |
| Future modules | `/api/{module-name}` |

### 4.4 MongoDB Collections — Single Collection Rule

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

### 4.5 Auth Pattern — Live and Proven

From `CODEX_MASTER_RESPONSE_MARCH2026.md` Section 3:

```python
# SessionUserMiddleware in server.py populates this before every request:
request.state.user = {
    "email": "user@example.com",
    "name": "User Name",
    "user_id": "user_abc123",
    "picture": None
}

# Correct access pattern in every module router:
user_email = request.state.user.get("email")

# Database handle:
db = request.app.state.db
```

The `_resolve_user_email()` fallback helper (accepting `X-User-Email` header or explicit `user_email` field) is **approved to remain** for isolated local validation convenience. Primary production path is always `request.state.user.get("email")`.

### 4.6 What CODEX Must NOT Request

- Existing Temple App source files
- Database credentials or connection strings
- Production dependency lists
- Access to existing backend modules
- Access to live server configurations

> *"Your module code should stand on its own. We test integration end-to-end on our side."*
> — Response to Codex_Env Constraints.txt

---

## 5. Module Delivery Checklist

Every CODEX delivery must include:

### Backend (Required)
- [ ] One standalone `APIRouter` file (e.g., `numerology_router.py`)
- [ ] `from __future__ import annotations` at top
- [ ] `timezone.utc` — never `datetime.UTC`
- [ ] Pydantic v2 with `ConfigDict`
- [ ] Python 3.12 syntax validated
- [ ] Single-collection persistence pattern
- [ ] All route signatures stable and documented
- [ ] `py_compile` passes cleanly
- [ ] Deterministic engine self-check passes (where applicable)
- [ ] **No Astro-Tarot fusion code in core `tarot_router.py`** — fusion code goes in `tarot_router_platform_fusion.py` only
- [ ] **No APScheduler or dispatch routes** — scheduler lives in `server.py`, Temple Team side only
- [ ] **No `hour_utc`/`minute_utc`/`channel`/`focus_area`/`next_run_at`/`last_sent_on` fields** in reminder documents (use `reminder_time`, `frequency`, `timezone`, `enabled`)

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

## 6. Contract Status — As of 29 March 2026

| # | Contract | Deliverable | Status | Python |
|---|---|---|---|---|
| 1 | vedic_calculator.py — flatlib → pyswisseph | `vedic_calculator.py` | ✅ Live | 3.12 |
| 2 | panchang_router.py — pyswisseph engine | `panchang_router.py` | ✅ Live (v11-swiss) | 3.12 |
| 3 | Premium Ankjyotish Numerology tile | `numerology_router.py` | ⚠️ Delivered — backend live, report not rendering in app (under investigation) | 3.12 |
| 4 | Tarot 78-card SVG bundle | `tarot_cards.json` | ✅ Live — digital asset visual refinement is a follow-up item, not a contract blocker | N/A |
| 4b | Tarot router DEFAULT_CARDS → 78 | `tarot_router.py` | ✅ Live | 3.12 |
| 5 | Panchang per-date endpoint | `panchang_router.py` | ✅ Live | 3.12 |
| 6 | Tarot daily reminder — 3 endpoints | `tarot_router.py` | ✅ Live | 3.12 |
| 7 | **Astro-Tarot Fusion router** | `tarot_router_platform_fusion.py` | **🔜 Pending** | 3.12 |
| 8 | Future modules (Palmistry, etc.) | TBD | 🔒 Pending scoping | 3.12 |

---

## 7. Panchang — Critical Version Note

> **⚠️ The CODEX dropin `panchang_router.py` is v3-swiss. Production is v11-swiss. Do NOT use the dropin version as a reference.**

**Reference snapshot shared — 30 March 2026:** `REFERENCE_vedic_calculator.py` is available in the `codex-deliveries/` folder. This is the shared astronomical engine that both Panchang and Kundali modules rely on. All natal and positional computations required for Contract 8A (Lagna Kundali) flow through this file. CODEX does not need `panchang_router.py` itself.

**Key functions in `vedic_calculator.py` relevant to Contract 8A:**
- `calculate_vedic_chart(date_of_birth, time_of_birth, place_of_birth)` — returns full natal chart including lagna, moon sign, nakshatra, planets, houses, dashas
- `geocode_place(place)` — converts city name to lat/lon (91-city catalogue built in; falls back to geopy)
- `generate_north_indian_chart_svg(houses, lagna_sign)` — renders the North Indian diamond SVG (Temple may extend this for the Kundali UI)
- `calculate_vimshottari_dasha(birth_date, moon_longitude)` — Vimshottari Dasha periods
- `get_nakshatra(moon_longitude)` — Nakshatra name, lord, pada
- `get_current_dasha(dashas)` — current Maha + Antar Dasha

---

## 8. Tarot Reminder Contract — Exact Specification

From `CODEX_MASTER_RESPONSE_MARCH2026.md` Section 7 + prior engagement chat history:

**Routes (exactly these three):**
```
POST   /api/tarot/reminder/set    — save user reminder preference
GET    /api/tarot/reminder        — retrieve current reminder settings
DELETE /api/tarot/reminder        — remove reminder preference
```

**Document structure (`doc_type: "reminder"` in `tarot_readings` collection):**
```json
{
  "id": "uuid",
  "doc_type": "reminder",
  "user_email": "user@example.com",
  "reminder_time": "07:30",
  "frequency": "daily",
  "timezone": "Asia/Kolkata",
  "enabled": true,
  "created_at": "iso",
  "updated_at": "iso"
}
```

**Frequency values:** `"daily"`, `"twice_daily"`, `"weekdays_only"`

**NOT in scope for CODEX delivery:**
- `POST /api/tarot/reminder/dispatch` — NOT a contract route
- APScheduler job — lives in `server.py`, Temple Team side only
- Fields: `hour_utc`, `minute_utc`, `channel`, `focus_area`, `next_run_at`, `last_sent_on` — NOT approved

---

## 9. tarot_cards.json — Exact Format

**Required format (flat object):**
```json
{
  "the-fool":    "<svg viewBox='0 0 200 300' xmlns='http://www.w3.org/2000/svg'>...</svg>",
  "wands-ace":   "<svg viewBox='0 0 200 300' xmlns='http://www.w3.org/2000/svg'>...</svg>",
  "cups-queen":  "<svg viewBox='0 0 200 300' xmlns='http://www.w3.org/2020/svg'>...</svg>"
}
```

**NOT acceptable:**
- Manifest-style JSON with deck metadata wrapper
- `cards[]` array format
- Separate SVG files or ZIP bundles

**Card ID naming:**
- Major Arcana (22): slug format — `the-fool`, `the-magician`, `strength`, `wheel-of-fortune`, etc.
- Minor Arcana (56): `{suit}-{rank}` — `wands-ace`, `cups-07`, `swords-king`, `pentacles-page`

---

## 10. Astro-Tarot Fusion — Next Contract Specification

> **⚠️ Under Review — with Temple Team. Not yet shared with CODEX.**
> This section will be finalised by Temple Team before being issued as a formal contract appointment. CODEX should not treat this as an active brief until a Contract Appointment Note is received.

The following spec documents exist and are under review:
- `ASTRO_TAROT_FUSION_ENGINEERING_NOTE.md` — architecture, layered approach, output contract
- `ASTRO_TAROT_FUSION_PROMPT_PACK.md` — 5 prompts (Lite Daily, Premium Spread, Signature, Favorable Window, Product Bridge)
- `ASTRO_TAROT_VEDIC_CROSS_REFERENCE_UI_SPEC.md` — UI specification

**Key rule (confirmed):** The model must never invent astrology. It may only interpret deterministic Vedic signals explicitly provided in the request.

**Delivery (confirmed):** `tarot_router_platform_fusion.py` — standalone `APIRouter`, prefix `/api/tarot/fusion`, single collection `tarot_readings`, validated Python 3.12.

Contract Appointment Note to follow after Temple Team review.

---

## 11. Output Constraints Summary

All module outputs must comply with `OUTPUT_CONSTRAINTS_MATRIX.md`. Key hard constraints:

| Module | Hard Limit Examples |
|---|---|
| Tarot Daily | `intro_line` max 25w · `card_scene_lines` array 1-2 strings max 35w each · `synthesis` max 60w |
| Tarot Premium Spread | `card_scene_lines` exactly 3 strings · `synthesis` max 90w |
| Numerology Core Profile | `hero_summary` max 50w · `key_takeaways` exactly 3 strings max 28w each |
| Numerology Favorable Timing | `monthly_highlights` array 3-6 strings max 30w each |
| Panchang | Deterministic engine is source of truth — AI must not override calendar values |
| All modules | No guaranteed outcomes · No deterministic language for love/health/death · Remedies soft and non-medical |

---

## 12. Known Issues — Resolution Log

This section is a resolved-issues log so that future CODEX engagements start cleanly without rediscovering past problems. No action needed from Temple Team — all items are either resolved or accepted.

**In plain terms, the issues and their fixes:**

| Issue | What it meant in practice | Status | Fix applied |
|---|---|---|---|
| CODEX workspace was on Python 3.9, production is 3.12 | Code built on 3.9 could silently use features that fail on 3.12 | ✅ Resolved | CODEX always validates using a Python 3.12 virtual environment before delivery |
| Older Python syntax for dates (`datetime.UTC`) | `datetime.UTC` only exists in Python 3.11+; our server is 3.12 but this syntax was still flagged | ✅ Resolved | All code uses `timezone.utc` — this is now a hard rule in the delivery checklist |
| CODEX workspace missing packages (pydantic, fastapi) | CODEX couldn't run their code locally to test it | ✅ Resolved | CODEX installs `fastapi pydantic uvicorn` in the 3.12 venv before each contract |
| CODEX sandbox can't write Python cache files | Minor error during code validation; no functional impact | ✅ Resolved | CODEX uses `PYTHONPYCACHEPREFIX='/tmp/pycache'` as a one-line workaround |
| Live app router files not visible in CODEX workspace | CODEX can't see `server.py`, `main.py`, or existing modules | ✅ Accepted by design | CODEX delivers self-contained files; Temple Team does all integration wiring |
| Live app CSS/styling not visible to CODEX | CODEX can't use existing style classes directly | ✅ Accepted by design | CODEX delivers styling alongside the module; Temple Team wires it to the design system |
| Tarot router had extra code outside contract scope | An early draft included fusion logic and scheduler code not requested | ✅ Resolved before delivery | Removed; fusion lives in `tarot_router_platform_fusion.py` only |
| Tarot reminder API had wrong route structure | Draft used wrong URL path and wrong database field names | ✅ Resolved before delivery | Final delivery matches exact spec (see Section 8) |
| Tarot card JSON was in the wrong format | Draft used a wrapped object instead of the required flat key-value structure | ✅ Resolved before delivery | Final delivery is a flat `{card_id: SVG}` object |
| Tarot Minor Arcana card names were non-standard | Draft used different naming convention for card IDs | ✅ Resolved before delivery | Final delivery uses `{suit}-{rank}` format throughout |

---

## 13. Communication Protocol

| Item | Owner | Notes |
|---|---|---|
| Contract initiation | Temple Team | Temple defines scope and contract terms |
| Module spec documents | CODEX | PRD, UX Blueprint, Engineering Spec, Prompt Pack |
| Backend delivery | CODEX | Single router file + handoff docs to `codex-deliveries/` |
| Frontend delivery | CODEX | Drop-in JSX pages + stylesheet + integration guide |
| Integration and wiring | Temple Team | Routes, auth, CSS, collections |
| End-to-end testing | Temple Team | Staging + production |
| Sign-off | Temple Team | Required before deployment |
| Discrepancy flagging | Temple Team | Via `CODEX_INCONSISTENCIES.md` |
| New constraint discoveries | CODEX | Via `CROSS_MODULE_BUILD_HANDOVER_ISSUES.md` |

---

## 14. Do Not Repeat List

| # | Rule | Source |
|---|---|---|
| 1 | Never use `datetime.UTC` — always `timezone.utc` | Both constraint docs |
| 2 | Never deliver multi-file backend slices as the primary Temple artifact | Delivery contract |
| 3 | Never write to multiple MongoDB collections | Single collection rule |
| 4 | Never embed Astro-Tarot fusion code in `tarot_router.py` | Delayed response + contract |
| 5 | Never add APScheduler or dispatch routes to CODEX deliveries | Delayed response |
| 6 | Never use `hour_utc`/`minute_utc`/`channel`/`focus_area`/`next_run_at`/`last_sent_on` in reminder docs | Delayed response |
| 7 | Never deliver `tarot_cards.json` as manifest-style or `cards[]` array | Delayed response |
| 8 | Never reference dropin panchang_router.py (v3) as current — production is v11 | INC-01 |
| 9 | Never assume CODEX workspace Python matches production — always validate in 3.12 venv | Constraint docs |
| 10 | Never modify system Python | All constraint docs |
