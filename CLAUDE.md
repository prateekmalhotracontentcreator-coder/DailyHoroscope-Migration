# EverydayHoroscope -- Claude Code Working Guide
> Last updated: 2026-05-14 | Full reference: `.claude/REFERENCE.md`

---

## 1. Project

| | |
|---|---|
| Live | https://www.everydayhoroscope.in |
| API | https://everydayhoroscope-api.onrender.com |
| Repo | `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration` |
| Frontend | React → Vercel (~2 min deploy) |
| Backend | FastAPI → Render Docker (~3 min deploy) |
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

> **INGEST FREEZE in effect (14 May 2026).** No new chapters until KE Phase 1.2 Sprint 2 (arbitration runtime) is delivered. Validation re-runs on existing batches still allowed. All ingest targets `horoscope_db`. Do NOT use stale `EverydayHoroscope` DB.

---

## 8. Current Build Focus

| Module | Spec | Status |
|---|---|---|
| LK Standalone Remedies | `.claude/briefs/lk/LK_STANDALONE_MODULE_SPEC.md` | ✅ Live |
| The Strategist | `.claude/_archive/briefs/THE_STRATEGIST_SPEC.md` | ✅ Live |
| Remedies Engine Phase 1 | `.claude/briefs/remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` | 🔜 Next commission |
| Legal Pages (seed) | `backend/scripts/seed_policies_v1.py` | 🔜 Run with Render MONGO_URL |
| SEO / Technical SEO | User to share thread findings | 🔜 Pending |

KP Remedy: bundle-native remedies live. Engine-fallback (conditional) still pending -- see HANDOVER_2026-05-14.md.

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

## 10. Premium Gating

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

## Compact Instructions

When compacting this conversation, produce the absolute minimum summary possible -- 5 lines or fewer. Do NOT summarize chat history, completed tasks, code written, errors fixed, or files changed. Only preserve:
1. The single task currently in progress (if any), in one sentence.
2. Any explicit user instruction given in the last message that hasn't been acted on yet.

Do not include architecture notes, file paths, pending backlogs, or any other context -- all of that is already in CLAUDE.md and `.claude/REFERENCE.md` and will be reloaded automatically.
