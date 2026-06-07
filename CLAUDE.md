# EverydayHoroscope -- Claude Code Working Guide
> Last updated: 2026-05-15 | Full reference: `.claude/REFERENCE.md`

---

## ⭐ SESSION START PROTOCOL -- READ FIRST

Before writing a single line of code, read these files in order:

| # | File | Purpose |
|---|---|---|
| 1 | **`#2_MASTER_TRACKER.md`** | Master dashboard -- module status index. Tells you what is CRITICAL, BLOCKED, or ACTIVE at a glance. |
| 2 | **`Codex_Deliveries/[Module]/TRACKER.md`** | Individual module tracker for the module(s) you are about to work on. Open points, commission status, version history. **Single source of truth for all commissions.** |
| 3 | **`#3_ACTION_TRACKER.md`** | Temple Team (TT) and Claude Code (CC) action items -- what is blocked and on whom. Commission detail is NOT duplicated here -- see module TRACKER. |
| 4 | **`Codex_Deliveries/List_of_Pending_Codex_Commissions.md`** | Commission queue -- what is ready to issue, in progress, or integrated. |

**At the end of every session:** update `Codex_Deliveries/[Module]/TRACKER.md` for every module touched -- add a version history row, update open points, update status badge if it changed. This is mandatory -- no exceptions.

---

## 1. Project

| | |
|---|---|
| Live | https://www.everydayhoroscope.in |
| API | https://everydayhoroscope-api.onrender.com |
| Repo | `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration` |
| Frontend | React → Vercel (~2 min deploy) |
| Backend | FastAPI → Render Docker (~3 min deploy) · **Starter plan (always-on, no cold starts)** |
| DB | MongoDB Motor async -- env: `MONGO_URL`, `DB_NAME=horoscope_db` |

---

## 2. Key Files

```
backend/server.py              # ⭐ Main app -- all routers
backend/panchang_router.py     # ⭐ Panchang engine v8-swiss
backend/vedic_calculator.py    # Birth chart / Dasha engine -- SINGLE SOURCE OF TRUTH
backend/knowledge_engine.py    # Interpretation layer only -- never computes live data
backend/tarot_router.py
backend/numerology_router.py
frontend/src/pages/            # All page components
frontend/src/components/ShareCard.jsx
```

---

## 3. Architecture Rule -- MANDATORY

**All live astronomical and dasha computations: `vedic_calculator.py` + `pyswisseph` ONLY.**
`knowledge_engine.py` is interpretation layer -- never replace or duplicate Legacy Model functions.

```python
# Always call these -- never rewrite:
calculate_vimshottari_dasha(birth_date, moon_longitude)
get_current_dasha(dashas)
DASHA_ORDER = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']
DASHA_YEARS = {'Ketu':7,'Venus':20,'Sun':6,'Moon':10,'Mars':7,'Rahu':18,'Jupiter':16,'Saturn':19,'Mercury':17}
```

**KE approval status -- two distinct levels:**
- `auto_approved` -- AI validation passed. Still co-founder gated. Does NOT reach live users.
- `approved` -- Co-founder signed off. This is the ONLY status that reaches live users.
Zero `approved` rules → Legacy Model is the only signal. Do not confuse these two.

**`compute_dasha_timeline()` in `knowledge_engine.py` (line 829):**
This function reads from a pre-computed `chart["layers"]["vimshottari_dasha"]` dict -- it does NOT call pyswisseph or compute from moon longitude. It is a chart-data reshaper, not a duplicate calculator. However it builds antardasha sub-periods from date arithmetic independently of vedic_calculator. Flag for future refactor to import directly from vedic_calculator. Do not add further dasha logic here.

Natural benefic/malefic: Jupiter/Venus/Mercury(waxing)/Moon(waxing) = Auspicious | Saturn/Mars/Rahu/Ketu/Sun = Inauspicious.

---

## 4. Commit Protocol

```
feat(scope): description   # new feature
fix(scope): description    # bug fix
chore(scope): description  # config/deps
docs: description          # docs only
```

- Never use GitHub browser editor
- Before every backend change: bump `ENGINE_VERSION` in `panchang_router.py`
- Never push while YouTube upload in progress (Render rolling deploy kills background tasks)
- Smart quotes are auto-sanitised pre-commit via `scripts/sanitise-smart-quotes.sh`. Run manually after pasting Codex output to inspect diff first.

---

## 5. Theme (Temple App)

```
bg-background | bg-card | text-foreground | text-muted-foreground
text-gold / border-gold / bg-gold  →  #c5a059
GlassCard: rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm
```

Smart quote fix for Codex output: `.claude/REFERENCE.md §Codex`

---

## 6. Key Env Vars

| Var | Value / Notes |
|---|---|
| `MONGO_URL` | Render env |
| `DB_NAME` | `horoscope_db` |
| `REACT_APP_BACKEND_URL` | Vercel env |
| `RAZORPAY_KEY_ID/SECRET` | Render -- test keys active |
| `RESEND_API_KEY` | ✅ working |
| `FACEBOOK_PAGE_ID` | `1084672598054073` |
| `FACEBOOK_PAGE_ACCESS_TOKEN` | System User token (never expires) |
| `YOUTUBE_CLIENT_ID/SECRET` | ✅ OAuth connected |
| `WHATSAPP_PHONE_NUMBER_ID` | `1062698816928895` -- 🔜 Pending OTP |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | 🔜 Pending |

---

## 7. KE Ingest Freeze

> **INGEST FREEZE LIFTED ✅ (confirmed 2026-05-17).** KE-Sprint2 (arbitration runtime) closed -- all 5 acceptance gates passed. Ingest of new chapters may proceed. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.

---

## 8. Current Build Focus

> This section is intentionally brief. The authoritative live state of every module is in **`TEMPLE_TRACKER.md`**. Read that file -- do not rely on a static snapshot here.

**Active hotlist (as of 2026-05-31):**
- ✅ KE-Sprint2 (arbitration runtime) -- CLOSED 2026-05-17, all gates passed, ingest freeze lifted
- 🔴 KE-2A (Yoga Check) -- issue to Codex this week
- 🟠 STR-1 (Strategist War Room visual) -- fully unblocked, issue to Codex
- 🟠 KP-Sprint2 + IR-1 -- issue to Codex Week 1
- 🔧 `/api/remedies/ref/{remedy_ref_id}` endpoint -- Claude Code direct fix, blocks KP-2A
- 🔧 M-1 OG image + M-2 legal pages seed -- Temple Team actions

---

## 8. Panchang Engine

File: `backend/panchang_router.py` | Version: `panchang-router-v8-swiss`
Routes: `/api/panchang/daily` `/api/panchang/locations` `/api/panchang/calendar/{y}/{m}` `/api/panchang/festivals`
318 cities, 81 countries. Sunrise/sunset verified ±1 min vs Drik Panchang.

---

## 9. Platforms Live

Panchang ✅ | Tarot ✅ | Numerology ✅ | Birth Chart ✅ | Horoscopes ✅ | Admin Console ✅
LK Standalone ✅ | All 5 Remedy Modules ✅ | The Strategist ✅ | KP Oracle ✅
Lagna Kundali ✅ | Lumina ✅ | Palmistry ✅ | Arc Angel ✅ | Longevity ✅
Facebook posting ✅ | YouTube posting ✅ | Email (Resend) ✅ | Razorpay test keys ✅
Punya Rewards ✅ (built, route pending user confirmation)
WhatsApp 🔜 (OTP pending) | Instagram 🔜 (Account ID pending)
Legal pages 🔜 (code ready -- seed_policies_v1.py needs running with Render MONGO_URL)

Full feature detail: `.claude/REFERENCE.md`

---

## 10. SEO Content Classification (LOCKED -- do not change without co-founder sign-off)

Two official terminology labels, decided 2026-06-07:

**SEO Resource Content** -- Strategic, deep content libraries where significant build effort has been invested. These pages are gated behind Login + Subscribe (`PremiumRoute`). Not logged in → redirected to `/login`. Logged in, not premium → premium upgrade gate.
| Module | Routes |
|---|---|
| Angel Numbers | `/angel-numbers/*` |
| Lo Shu Grid | `/lo-shu-grid/*` |
| Crystals | `/crystals/*` |
| Rudraksha | `/rudraksha/*` |
| Faith Hubs | `/faith/*` |
| Tarot Library | `/tarot/spreads`, `/tarot/spread/*`, `/tarot/card/*`, `/tarot/for/*` |

**SEO Marketing Content** -- Module and report landing pages, editorial content. Stays fully public. No gate. Includes all `/panchang/*`, report landing pages (`/karmic-debt-report`, `/career-blueprint-report`, etc.), module landing pages (`/the-tarot`, `/the-strategist`, `/lal-kitab-remedies`, `/the-longevity-report`), `/blog/*`, `/festivals/*`, `/celebrity-horoscopes/*`, `/about`, `/contact`, `/pricing`.

**Implementation**: `SeoResourceGate` in `App.js` (component in `PremiumRoute.jsx`).
- Not logged in → soft teaser (page visible, `pointer-events-none`, gradient fade) + `SeoResourceGateCard` with capsule "Login &amp; Subscribe for Premium Content -- It's Free" + Register Free + Login CTAs.
- Logged in (ANY tier, including free) → full access. Free registration unlocks all SEO Resource Content.
- `PremiumRoute` (paid gating) is NOT used for SEO Resource Content.

---

## 11. Premium Gating

`user.is_premium` sourced from `/api/auth/me` → `auth_utils.py` (queries `db.subscriptions`).

**Route-level gate (App.js):**
```jsx
<Route path="/..." element={<PremiumRoute feature="..." description="..."><Page /></PremiumRoute>} />
```

**Inline gate (auth-aware pages -- KP, Strategist, Tarot, Numerology, Palmistry, Lumina):**
```jsx
if (user && !user.is_premium) return <PremiumGateCard feature="..." description="..." />;
```

**Routes currently behind PremiumRoute:**
Weekly Horoscope, Monthly Horoscope, Birth Chart, Kundali Milan, Brihat Kundli,
My Reports, Individual Reports, Love Reports, Ritual Engine, Numerology Report,
Tarot History, Lagna Kundali (×2), Arc Angel, Questionnaire.

Free users: Daily Horoscope, Panchang, Gemstones, Crystals, Blog -- full access.
Logged-out: most pages show public SEO landing (noindex) with auth CTA.

---

## End-of-Session Protocol (MANDATORY)

Before the session closes or context is compacted, Claude Code must:
1. Update **`Codex_Deliveries/[Module]/TRACKER.md`** for every module touched -- add version history row, update open points table, change status badge if applicable. This is the SINGLE SOURCE OF TRUTH for commission status.
2. Update **`#2_MASTER_TRACKER.md`** dashboard row for any module whose status changed.
3. Strike off any completed items in `#3_ACTION_TRACKER.md` (TT/CC action items only -- do NOT add commission detail here).
4. Update commission status in `Codex_Deliveries/List_of_Pending_Codex_Commissions.md` if any commission moved state.

---

## Compact Instructions

When compacting this conversation, produce the absolute minimum summary possible -- 5 lines or fewer. Do NOT summarize chat history, completed tasks, code written, errors fixed, or files changed. Only preserve:
1. The single task currently in progress (if any), in one sentence.
2. Any explicit user instruction given in the last message that hasn't been acted on yet.

Do not include architecture notes, file paths, pending backlogs, or any other context -- all of that is already in CLAUDE.md, `#2_MASTER_TRACKER.md`, and `.claude/REFERENCE.md` and will be reloaded automatically.
