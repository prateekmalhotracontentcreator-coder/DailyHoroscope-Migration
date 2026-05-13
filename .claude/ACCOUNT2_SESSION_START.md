# Account 2 — Session Start Brief
# EverydayHoroscope: Live App — KP Remedies + SEO Complete
> Last updated: 2026-05-13 | Supersedes all prior versions

---

## Project

EverydayHoroscope (everydayhoroscope.in) — India's Vedic astrology platform.
- Backend: FastAPI on Render (Docker) → `backend/server.py`
- Frontend: React on Vercel → `frontend/src/`
- DB: MongoDB (Motor async) — env var `MONGO_URL`, db `horoscope_db`
- Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`

Read `.claude/CLAUDE.md` first — single source of truth for architecture, env vars, commit format.
Full session detail: `.claude/HANDOVER_2026-05-12.md`

---

## What Is Live (as of 2026-05-13)

| Module | Status | Notes |
|---|---|---|
| LK Standalone (Onboard → Report → Tracker → Browse) | ✅ Live | On-page SEO content added |
| All 5 Remedy Modules (Dana, Gemstones, Crystal, Chakra, Mantra) | ✅ Live | On-page SEO content added |
| The Strategist (War Room + Missions + Report + Surrogate) | ✅ Live | On-page SEO content added |
| KP Oracle (`/krishna-prashnavali`) | ✅ Live | Bundle-native remedies; Engine as fallback (PENDING — see below) |
| **Premium/Free tier system** | ✅ Live | Full gate across all modules |
| **Lagna Kundali — Generate D1** | ✅ Working | On-page SEO content added |
| **On-page SEO — all 13 modules** | ✅ Live | Panchang body-copy pattern, 5 h2 sections each |

---

## Premium Access Tier (locked — do not change without user confirmation)

| Module | Logged Out | Free | Premium |
|---|---|---|---|
| Daily Horoscope / Panchang | ✅ Full | ✅ Full | ✅ Full |
| Gemstones / Crystals / Blog | ✅ Full | ✅ Full | ✅ Full |
| Weekly & Monthly Horoscope | → Login | 🔒 Upgrade | ✅ Full |
| Tarot / Numerology / Palmistry / Lumina / KP / Strategist | ✅ SEO Landing | 🔒 Upgrade | ✅ Full |
| Lagna Kundali / Birth Chart / Kundali Milan / Brihat Kundli | → Login | 🔒 Upgrade | ✅ Full |
| All Reports / Ritual Engine / Arc Angel | → Login | 🔒 Upgrade | ✅ Full |

**Gate pattern:**
```jsx
// Route-level (App.js):
<Route path="/..." element={<PremiumRoute feature="..." description="..."><Page /></PremiumRoute>} />

// Inline (auth-aware pages — KP, Strategist, Tarot, Numerology, Palmistry, Lumina):
if (user && !user.is_premium) return <PremiumGateCard feature="..." description="..." />;
```

---

## New Mandatory Rules (added this session)

**Rule 8 — Payload Hygiene:**
```js
// BAD — spreads UI-only fields (city_slug etc.) into backend models with extra="forbid"
const payload = { ...form };

// GOOD — always whitelist explicitly
const payload = { date: form.date, time: form.time, ... };
```

**Rule 9 — FastAPI 422 Error Handler:**
```js
// FastAPI 422 detail is an array of objects — always guard:
const detail = err?.response?.data?.detail;
setError(typeof detail === "string" ? detail : detail?.[0]?.msg || "Fallback message");
```

---

## Pending Items

### 🔨 First Task Next Session — KP Remedy: Bundle Default + Engine Fallback
User: "Keep KP specific Remedy as Default; Remedies Engine as Fall Back — don't keep any field empty."

**Backend** (`scriptural_oracle_router.py`):
- Reinstate `_resolve_kp_remedy_doc` as CONDITIONAL — call it ONLY when `answer.behavioral_remedy` is None/empty AND `answer.remedy_ref` exists
- `_summary_report`: populate from bundle first; if empty, fill from DB doc
- Bump `ENGINE_VERSION` before change

**Frontend** (`KrishnaOraclePage.jsx`): Current display logic already reads bundle first — no change expected unless null slots persist.

### Needs User Confirmation Before Running
- **Lagna Kundali tier** — currently Premium; user said "still needs a decision"
- **Punya Rewards Page** — built, no App.js route; user reviewing before Temple Team migration

### Data Tasks
- **5 split-required LK rules** — tagged `split_required=True`; not yet split
  IDs: `lalkitab-ch21-fam-04` + 4 others (age/infancy/shortlife/survival)

### SEO Sprints — ALL COMPLETE ✅
- Sprint D (JSON-LD) ✅ | Sprint E (12 sign pages) ✅ | Sprint F (LK landing) ✅
- On-page body-copy SEO: all 13 modules ✅

### Premium UX Phase 2
- "View only" with disabled interactions for free logged-in users (currently full upgrade gate)
- Arc Angel memory persistence for premium users

---

## Mandatory Architecture Rules

1. ALL live astronomical/dasha data from `vedic_calculator.py` + `pyswisseph` — never replicate
2. `knowledge_rules` always filtered by `science_id`
3. All notifications via existing `/api/notifications/trigger/{type}` — never call push/WA directly
4. Remedies Engine is downstream-only for KP — never overrides KP verdict
5. Commit format: `feat(scope):` / `fix(scope):` / `chore(scope):`
6. Bump `ENGINE_VERSION` in `panchang_router.py` before any backend change
7. All fetch calls: `withCredentials: true` / `credentials: 'include'` — app uses HTTP-only session cookies
8. Never spread `...form` into API payloads when backend model uses `extra="forbid"` — whitelist explicitly
9. FastAPI 422 `detail` is an array — always guard with `typeof detail === "string"` before setting error state

---

## Full Spec Files

```
.claude/HANDOVER_2026-05-12.md          ← LATEST — 4-commit session summary + new rules
.claude/THE_STRATEGIST_SPEC.md          ← Full Strategist spec incl. Phase 2
.claude/LK_STANDALONE_MODULE_SPEC.md    ← LK Standalone spec (all built)
.claude/CLAUDE.md                       ← architecture rules, env vars, file map
```
