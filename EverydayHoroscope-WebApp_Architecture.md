# EverydayHoroscope -- Web Application Architecture
> **Purpose:** Reference document for AI research platforms (GAI, NotebookLM, Claude, Gemini).
> Complete technical, product, and architectural overview of the EverydayHoroscope platform.
> Last updated: 2026-05-16

---

## 1. Product Identity

| Field | Value |
|---|---|
| **Product Name** | EverydayHoroscope |
| **Tagline** | India's Premium Vedic Astrology Platform |
| **Live URL** | https://www.everydayhoroscope.in |
| **Backend API** | https://everydayhoroscope-api.onrender.com |
| **Target Market** | India-first, global Indian diaspora |
| **Business Model** | Freemium -- Razorpay subscription paywall for premium modules |
| **Repository** | `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration` |
| **Main Branch** | `main` (deploy-on-push to Vercel + Render) |

---

## 2. Technology Stack

### 2.1 Frontend

| Layer | Technology | Version / Notes |
|---|---|---|
| Framework | React | 18.x |
| Build Tool | Craco (CRA + custom config) | `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` |
| Routing | React Router | v6 (lazy imports, `<Suspense>`) |
| HTTP Client | Axios | API calls to FastAPI backend |
| Styling | Tailwind CSS + custom CSS variables | Gold/cream design system (`text-gold`, `bg-card`, `GlassCard`) |
| Image Capture | html2canvas | Share card generation (offscreen DOM capture) |
| Hosting | **Vercel** | Deploy trigger: `git push main` (~2 min) |
| Auth Pattern | Cookie-based sessions (`withCredentials: true`) | JWT or session stored in HTTP-only cookie |

**Design System Tokens:**

| Token | Value | Usage |
|---|---|---|
| `bg-background` | Off-white / cream | Page background |
| `bg-card` | Card surface | Panel / card background |
| `text-foreground` | Dark brown | Primary text |
| `text-muted-foreground` | Muted warm grey | Secondary / caption text |
| `text-gold` / `border-gold` | `#c5a059` | Gold accent, CTAs, dividers |
| GlassCard | `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm` | Standard card component |

### 2.2 Backend

| Layer | Technology | Version / Notes |
|---|---|---|
| Framework | **FastAPI** | Python 3.12.9 |
| Astronomy Engine | **pyswisseph** | 2.10.x -- Swiss Ephemeris (Julian Day calculations, `swe.calc_ut`, `swe.rise_trans`) |
| Database Driver | **Motor** | Async MongoDB driver for Python |
| AI / LLM | **Anthropic SDK** | Claude Sonnet (claude-sonnet-4-5) for report enrichment |
| Scheduler | APScheduler | Scheduled notifications and social posts |
| WSGI/ASGI | Uvicorn | Production server inside Docker |
| Containerisation | **Docker** | `python:3.12.9-slim` + `gcc` + `ffmpeg` |
| Hosting | **Render** | Docker deploy, ~3 min on `git push main` |
| Video Processing | ffmpeg | Share card → MP4 for YouTube Shorts |

### 2.3 Database

| Field | Value |
|---|---|
| Engine | **MongoDB** (cloud-hosted) |
| Driver | Motor (async) |
| Connection | `MONGO_URL` environment variable on Render |
| Database name | `DB_NAME` environment variable |

**Key Collections:**

| Collection | Purpose |
|---|---|
| `users` | User accounts, subscription status |
| `individual_reports` | All natal + transit report documents |
| `kp_readings` | KP Oracle reading history |
| `subscribers` | Email/WhatsApp subscriber list |
| `scheduled_notifications` | APScheduler queue |
| `notification_logs` | Email send history |
| `social_post_logs` | Facebook/YouTube post history |
| `app_settings` | YouTube OAuth refresh token, global config |
| `knowledge_rules` | Knowledge Engine curated rule library |
| `jyotish_lk_remedies` | Lal Kitab remedy reference (36 records) |
| `remedy_ref` | KP remedy reference (36 records) |

### 2.4 Third-Party Integrations

| Service | Purpose | Status |
|---|---|---|
| **Razorpay** | Subscription paywall | ✅ Live (test keys) |
| **Resend** | Transactional email | ✅ Live |
| **Meta Graph API** | Facebook Page posting | ✅ Live |
| **YouTube Data API v3** | Video upload (share card → MP4 → Shorts) | ✅ Live |
| **WhatsApp Cloud API v22.0** | Push notifications | 🔜 Pending (phone OTP verification) |
| **Instagram Graph API** | Story / post publishing | 🔜 Pending (Business Account ID) |
| **Google Search Console** | SEO monitoring + sitemap | ✅ Verified |
| **Bing Webmaster Tools** | SEO monitoring | ✅ Verified |
| **GA4** | Analytics (`G-3HJC8BTHRQ`) | ✅ Live |

---

## 3. Infrastructure

```
┌─────────────────────────────────────────────────────────────┐
│                    User (Browser / Mobile)                   │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTPS
                ┌───────────▼────────────┐
                │   Vercel (Frontend)     │
                │   React 18 + Craco     │
                │   everydayhoroscope.in │
                └───────────┬────────────┘
                            │ REST API (Axios)
                ┌───────────▼────────────────────┐
                │   Render (Backend / Docker)     │
                │   FastAPI + Uvicorn             │
                │   everydayhoroscope-api.onrender│
                └────┬──────────────┬────────────┘
                     │              │
          ┌──────────▼──┐    ┌──────▼──────────┐
          │   MongoDB    │    │  Anthropic API   │
          │   (Motor)    │    │  Claude Sonnet   │
          └─────────────┘    └─────────────────┘
                     │
          ┌──────────▼──────────────┐
          │  External APIs           │
          │  Razorpay / Resend       │
          │  Meta / YouTube / WA     │
          └─────────────────────────┘
```

**Deploy Pipeline:**
- `git push main` → Vercel builds React (~2 min) + Render builds Docker (~3 min) simultaneously
- Zero-downtime rolling deploy on both platforms
- ⚠️ Render rolling deploys kill in-flight background tasks (YouTube uploads) -- do not push during active upload

---

## 4. Astronomy Engine

The heart of the platform's accuracy is **pyswisseph 2.10.x** (Python binding to the Swiss Ephemeris C library).

### 4.1 Core Files

| File | Role |
|---|---|
| `backend/panchang_router.py` | Panchang engine v8-swiss -- all Panchang computations |
| `backend/vedic_calculator.py` | Birth chart, Vimshottari Dasha, Shadbala -- natal computations |
| `backend/vedic_shared_utils.py` | Shared utility layer for all report routers |

### 4.2 What the Panchang Engine Computes (all via pyswisseph)

- Sunrise / Sunset (with seconds, verified ±1 min vs Drik Panchang)
- Moonrise / Moonset (with seconds)
- Tithi (lunar day) + end time
- Nakshatra + end time
- Yoga + end time
- Karana + end time
- Paksha, Lunar month, Samvat, Sun sign, Moon sign
- Amrit Kalam (nakshatra-based auspicious window)
- Special Yogas: Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga
- True Choghadiya: 8 daylight + 8 nighttime slots with planetary rulers
- Auspicious windows: Brahma Muhurta, Abhijit Muhurta, Vijaya Muhurta
- Inauspicious windows: Rahu Kaal, Yamaganda, Gulika Kaal, Dur Muhurta × 2
- Location catalogue: 318 cities across 81 countries/regions

### 4.3 Vedic Calculator (Birth Chart Engine)

```python
# Key functions (single source of truth -- never duplicate in other files)

calculate_vimshottari_dasha(birth_date, moon_longitude)
# Returns: list of 9 Mahadasha dicts: {planet, start_date, end_date, years, antardashas}

get_current_dasha(dashas)
# Returns: currently active Mahadasha dict

DASHA_ORDER = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']
DASHA_YEARS = {'Ketu':7,'Venus':20,'Sun':6,'Moon':10,'Mars':7,'Rahu':18,'Jupiter':16,'Saturn':19,'Mercury':17}
```

### 4.4 Accuracy Benchmark (New Delhi, 26 March 2026)

| Field | Our Engine | Drik Panchang | Result |
|---|---|---|---|
| Sunrise | 06:18:23 | 06:18 | ✅ |
| Sunset | 18:35:xx | 18:36 | ✅ ±1 min |
| Tithi | Shukla Ashtami | Shukla Ashtami | ✅ |
| Nakshatra | Ardra | Ardra | ✅ |
| Rahu Kaal | 01:58 PM | 01:59 PM | ✅ |
| Abhijit | 12:02 PM | 12:02 PM | ✅ |
| Moonrise | 11:59 AM | 11:59 AM | ✅ |

### 4.5 Architecture Rule -- Legacy Model (MANDATORY)

> All live astronomical and dasha computations MUST use the Legacy Model (`vedic_calculator.py` + `pyswisseph`).
> The Knowledge Engine (`knowledge_engine.py`) is the **interpretation layer ONLY** -- it must never replace, duplicate, or bypass the Legacy Model for live data.

---

## 5. Module Catalog

### 5.1 Panchang

| Item | Detail |
|---|---|
| File | `backend/panchang_router.py` |
| Frontend | `frontend/src/pages/PanchangPage.jsx` |
| Status | ✅ Live |
| Routes | `GET /api/panchang/daily`, `/locations`, `/date/{date}`, `/calendar/{year}/{month}`, `/festivals` |
| Features | 6-tab UI (Today/Tomorrow/Tithi/Choghadiya/Calendar/Festivals), 318-city catalogue, share card, Facebook/YouTube posting |

### 5.2 Daily / Weekly / Monthly Horoscope

| Item | Detail |
|---|---|
| Files | `DailyHoroscope.jsx`, `WeeklyHoroscope.jsx`, `MonthlyHoroscope.jsx` |
| Status | ✅ Live |
| Features | Sign-based horoscope, share cards, Facebook posting, element theming (Fire/Earth/Air/Water) |

### 5.3 Tarot

| Item | Detail |
|---|---|
| File | `backend/tarot_router.py`, `frontend/src/pages/TarotPage.jsx` |
| Status | ✅ Live |
| Features | 78-card SVG deck (`tarot_cards.json`), Daily Draw, Spreads, History, flipping animation |

### 5.4 Numerology

| Item | Detail |
|---|---|
| File | `backend/numerology_router.py`, `frontend/src/pages/NumerologyPage.jsx` |
| Status | ✅ Live |
| Features | 10 report types (Life Path, Name Correction, Karmic Debt, Relationship, Career, etc.) |

### 5.5 Birth Chart / Kundali

| Item | Detail |
|---|---|
| Files | `backend/vedic_calculator.py`, `BirthChartPage.jsx`, `BrihatKundliPage.jsx` |
| Status | ✅ Live |
| Features | Full Kundali computation, extended Brihat Kundali report |

### 5.6 Lagna Kundali (Advanced)

| Item | Detail |
|---|---|
| File | `backend/kundali_router.py` |
| Status | ✅ Backend live; Frontend pending (KUN-1) |
| Prefix | `/api/lagna-kundali` |
| Endpoints | `/compute`, `/save`, `/my-charts`, `/chart/{chart_id}`, `/chart-definitions` |

### 5.7 Individual Reports (IR Suite) -- 12 Areas of Life

**Architecture:** One deep-dive report per Vedic house, complementing Arc Angel's 12-area dashboard.

**Phase 1 -- Natal Reports (live at `/reports`):**

| Report | File | House | Status |
|---|---|---|---|
| Life Cycles | `life_cycles_router.py` | H1 -- Self & Identity | ✅ Live |
| Retrograde Survival | `retrograde_survival_router.py` | H3 -- Communication | ✅ Live |
| Shadow Self | `shadow_self_router.py` | H8 -- Transformation | ✅ Live |
| Career Blueprint | `career_blueprint_router.py` | H10 -- Career | ✅ Live |
| Karmic Debt | `karmic_debt_router.py` | H12 -- Karma | ✅ Live |

**Phase 2 -- Transit Reports (live at `/love-reports`):**

| Report | File | House | Status |
|---|---|---|---|
| Lunar Cycle Wellness | `lunar_cycle_router.py` | H4 -- Emotional Foundation | ✅ Live (rework in progress) |

**Phase 3 -- Pending (6 reports, Houses 2/5/6/7/9/11):**

| Report | House | Commission |
|---|---|---|
| Wealth & Abundance Blueprint | H2 -- Dhana | IR-4 (to be scoped) |
| Romance & Creative Intelligence | H5 -- Putra | IR-5 |
| Vitality & Health Report | H6 -- Ari | IR-6 |
| Partnership & Marriage Window | H7 -- Kalatra | IR-7 |
| Dharma & Soul Purpose Report | H9 -- Dharma | IR-8 |
| Gains & Network Activator | H11 -- Labha | IR-9 |

**Public Hub:** `/individual-reports` (`PremiumReportsLanding.jsx`)
**Public SEO Landing Pages:** Phase 1 live ✅; Phase 2+3 pending (IR-3)

### 5.8 Love Bundle (8 Reports + Ritual Engine)

**Frontend hub:** `/love-reports` (`LoveReportsPage.jsx`) + `/love` (`LovePage.jsx`)

| Report | File | Status |
|---|---|---|
| Love Weather | `love_weather_router.py` | ✅ Live |
| Encounter Window | `encounter_window_router.py` | ✅ Live |
| Date Night Planner | `date_night_router.py` | ✅ Live |
| Digital Dating Edge | `digital_dating_router.py` | ✅ Live |
| Intimacy & Vitality | `intimacy_vitality_router.py` | ✅ Live |
| Venus Retrograde | `venus_retrograde_router.py` | ✅ Live |
| Soulmate Timing | `soulmate_timing_router.py` | ✅ Live |
| Soul Connection | `soul_connection_router.py` | ✅ Live |

**Ritual Engine:** `ritual_trigger_router.py` at `/api/ritual-engine`
- Subscription-based trigger engine (not individual report generator)
- 5 trigger types: First Date Magnet, Steamy Encounter, Ex-Recovery, Long-Term Love, Love Battery Score
- Frontend: `RitualEnginePage.jsx` at `/ritual-engine`

### 5.9 Knowledge Engine

| Item | Detail |
|---|---|
| Core file | `backend/knowledge_engine.py` |
| Router | `backend/knowledge_router.py` |
| Schema | `backend/knowledge_schema.py` |
| Validator | `backend/knowledge_validator.py` |
| Yoga evaluator | `backend/ke_yoga_evaluator.py` (16 evaluator types) |
| Jaimini module | `backend/ke_jaimini.py` |
| Status | 🔵 Sprint 2 in progress (Arbitration Runtime) |
| Rule approval | Zero approved rules -- Legacy Model is sole signal until co-founder sign-off |

**Phase tracking:**

| Sprint | Scope | Status |
|---|---|---|
| Sprint 1 | α/β/γ scoring wiring | ✅ Complete (`57e347a`) |
| Sprint 2 | Arbitration Runtime (G-03/G-05/G-06/G-04) | 🔵 In Progress |
| Sprint 3 | Arc Angel Computation (G-07/G-08/G-09) | Blocked on Sprint 2 |
| Sprint 4 | Questionnaire β/γ wiring | Separate commission KE-IQ |

### 5.10 Arc Angel

| Item | Detail |
|---|---|
| Frontend | `ArcAngelPanel.jsx` |
| Route | `/arc-angel` (PremiumRoute) |
| Status | ✅ Phase 1 baseline live |
| Concept | Confidence-scored interpretation of 12 Areas of Life from natal chart + Dasha |
| Next | ARC-2 (Confidence % lift + Questionnaire gating + Desktop sidebar) -- depends on KE Sprint 2 |

### 5.11 KP Oracle

| Item | Detail |
|---|---|
| Engine | `backend/kp_engine.py` |
| Status | ✅ Live; KP-Sprint2 (Ask-Question LLM Router) in progress |
| Verdict split | 10 YES / 8 WAIT / 8 NO / 10 PRAY (36 slots -- Vaishnava oracle structure, historically correct) |
| Remedies | 36 records seeded in `remedy_ref` collection |

### 5.12 The Strategist

| Item | Detail |
|---|---|
| Frontend | `StrategistPage.jsx`, `TheStrategistLandingPage.jsx` |
| Status | ✅ Fully live (commit `ba58192`) |
| Features | Missions UI, dasha display, War Room visual |

### 5.13 Punya Rewards

| Item | Detail |
|---|---|
| Status | ✅ Backend live (PUN-1 integrated); Frontend Phase 2 pending (PUN-2) |
| Commission | PUN-2 -- Home promo + 8 module hooks + SVG wheel upgrade |

### 5.14 Lal Kitab

| Item | Detail |
|---|---|
| Files | `backend/lk_remedies_router.py`, `backend/lk_diagnostics.py` |
| Status | Backend live; LK-1 commission (standalone module) ready to issue |

### 5.15 Longevity Report

| Item | Detail |
|---|---|
| File | `backend/longevity_router.py` |
| Status | Backend scaffolded; full commission (LON-1) Phase 2 |

### 5.16 Lumina

| Item | Detail |
|---|---|
| Files | `backend/lumina_router.py`, `backend/lumina_prompt_service.py` |
| Status | Live |

### 5.17 Live TV

| Item | Detail |
|---|---|
| Files | `backend/live_tv_router.py`, `backend/live_tv_service.py` |
| Status | ✅ Live (Sai Baba Arti, LTV-1) |

### 5.18 Admin Console

| Route | Feature | Status |
|---|---|---|
| `/admin/dashboard` | Overview / System / Users / Reports / Payments / Messages / Blog | ✅ Live |
| Notifications tab | Subscribers, Compose, Scheduled, History, Social Media | ✅ Live |
| Email | Resend integration | ✅ Working |
| Facebook posting | System User token → Page token exchange | ✅ Working |
| YouTube posting | OAuth → ffmpeg → YouTube Data API v3 (background task, ~2-4 min) | ✅ Working |
| WhatsApp | Meta Cloud API v22.0 | 🔜 Pending phone OTP |
| Instagram | Graph API | 🔜 Pending Business Account ID |

---

## 6. AI / LLM Integration Architecture

All AI enrichment follows a single pattern:

```
Computed astronomical data
        ↓
router.py calls prompt_service.py
        ↓
prompt_service builds prompt string
        ↓
love_prompt_common.try_claude_generation(prompt, max_tokens)
        ↓
Anthropic SDK → Claude Sonnet (claude-sonnet-4-5)
        ↓
JSON response parsed + validated
        ↓
Fallback content if Claude fails (always defined)
        ↓
_apply_content() merges into report model
        ↓
Final report returned + saved to MongoDB
```

**Key files:**

| File | Role |
|---|---|
| `backend/love_prompt_common.py` | Shared Claude call helper (`try_claude_generation`, `payload_json`) |
| `backend/individual_reports_prompt_common.py` | Shared helper for Phase 1 natal reports |
| `backend/*_prompt_service.py` | One per report -- builds prompt, defines fallback, applies content |

**Claude model:** `claude-sonnet-4-5` (configurable via `LOVE_CLAUDE_MODEL` env var)

---

## 7. Report Storage Pattern

Every generated report is stored in MongoDB `individual_reports` collection with this document shape:

```json
{
  "id": "uuid-string",
  "document_type": "individual_report",
  "report_type": "lunar_cycle_wellness",
  "report_slug": "lunar-cycle",
  "user_email": "user@example.com",
  "created_at": "2026-05-16T12:00:00Z",
  "updated_at": "2026-05-16T12:00:00Z",
  "input_payload": { "date_of_birth": "...", "latitude": 28.6, ... },
  "output_payload": { ... report-specific fields ... },
  "summary": "One-line summary shown in history list"
}
```

---

## 8. Frontend Routing Architecture

```
/                           → Home
/panchang                   → PanchangPage (free)
/daily-horoscope            → DailyHoroscope (free)
/weekly-horoscope           → WeeklyHoroscope (free)
/monthly-horoscope          → MonthlyHoroscope (free)
/tarot                      → TarotPage (free + premium)
/birth-chart                → BirthChartPage (free)
/brihat-kundali             → BrihatKundliPage (premium)
/numerology                 → NumerologyPage (premium)
/love                       → LovePage -- Love Bundle hub (premium)
/love-reports               → LoveReportsPage -- report generator (premium)
/ritual-engine              → RitualEnginePage (premium)
/reports                    → IndividualReportsPage -- Phase 1 hub (premium)
/individual-reports         → PremiumReportsLanding -- public SEO hub
/arc-angel                  → ArcAngelPanel (premium)
/strategist                 → StrategistPage (premium)
/admin/dashboard            → Admin console (admin auth)

Public SEO Landing Pages (no auth):
/karmic-debt-report         ← Phase 1 (IR-1 ✅)
/career-blueprint-report    ← Phase 1 (IR-1 ✅)
/shadow-self-report         ← Phase 1 (IR-1 ✅)
/retrograde-survival-report ← Phase 1 (IR-1 ✅)
/life-cycles-report         ← Phase 1 (IR-1 ✅)
/encounter-window-report    ← Phase 2 (IR-3 pending)
/love-weather-report        ← Phase 2 (IR-3 pending)
/lunar-cycle-wellness       ← Phase 2 (IR-3 pending)
/date-night-report          ← Phase 2 (IR-3 pending)
/intimacy-vitality-report   ← Phase 2 (IR-3 pending)
/venus-retrograde-report    ← Phase 2 (IR-3 pending)
/soulmate-timing-report     ← Phase 3 (IR-3 pending)
/soul-connection-report     ← Phase 3 (IR-3 pending)
```

---

## 9. Backend Routing Architecture

```
/api/panchang/*             ← panchang_router.py
/api/reports/karmic-debt/*  ← karmic_debt_router.py
/api/reports/career-blueprint/* ← career_blueprint_router.py
/api/reports/shadow-self/*  ← shadow_self_router.py
/api/reports/retrograde-survival/* ← retrograde_survival_router.py
/api/reports/life-cycles/*  ← life_cycles_router.py
/api/reports/lunar-cycle/*  ← lunar_cycle_router.py
/api/reports/love-weather/* ← love_weather_router.py
/api/reports/encounter-window/* ← encounter_window_router.py
/api/reports/date-night/*   ← date_night_router.py
/api/reports/digital-dating/* ← digital_dating_router.py
/api/reports/intimacy-vitality/* ← intimacy_vitality_router.py
/api/reports/venus-retrograde/* ← venus_retrograde_router.py
/api/reports/soulmate-timing/* ← soulmate_timing_router.py
/api/reports/soul-connection/* ← soul_connection_router.py
/api/lagna-kundali/*        ← kundali_router.py
/api/ritual-engine/*        ← ritual_trigger_router.py
/api/knowledge-engine/*     ← knowledge_router.py
/api/kp-oracle/*            ← (kp_engine.py wired in server.py)
/api/lk-remedies/*          ← lk_remedies_router.py
/api/longevity/*            ← longevity_router.py
/api/lumina/*               ← lumina_router.py
/api/live-tv/*              ← live_tv_router.py
/api/admin/*                ← admin_utils.py (via server.py)
/api/notifications/*        ← notification_*.py routers
/api/health                 ← inline health check in server.py
```

**Main app file:** `backend/server.py` (~2190 lines) -- all router registrations, middleware, OAuth flows, YouTube/WhatsApp/Facebook endpoints.

---

## 10. Share Card Architecture

Two share card types, rendered offscreen (`position: fixed; left: -9999px`) to avoid DOM flash:

| Card | File | Dimensions | Capture |
|---|---|---|---|
| PanchangShareCard | `ShareCard.jsx` | 900px wide | html2canvas + `onclone` |
| HoroscopeShareCard | `ShareCard.jsx` | 900px wide | html2canvas + `onclone` |

**Share destinations:** WhatsApp · Facebook · X · Instagram · YouTube · Save Card · Copy Link

**Platform-specific capture:**
- Desktop: `canvas.toDataURL()` → synchronous anchor click (download)
- Mobile: `navigator.share({ files })` Web Share API
- iOS Safari: `canvas.toBlob()` → `window.open()` (long-press to save)

**YouTube pipeline:** PNG share card → ffmpeg (`libx264 veryfast, CRF 18, -tune stillimage, -threads 1, 30s`) → MP4 → YouTube Data API v3 resumable upload (async background task, ~2-4 min)

---

## 11. Authentication & Payments

| Component | Technology | Notes |
|---|---|---|
| Auth | Cookie-based sessions | `withCredentials: true` on all Axios calls |
| PremiumRoute | React component | Wraps premium pages; redirects to paywall if not subscribed |
| Payments | Razorpay | Subscription plans; test keys active (live keys for Play Store) |
| Admin Auth | Separate admin session | `/admin/dashboard` behind admin guard |

---

## 12. Environment Variables

| Variable | Platform | Purpose |
|---|---|---|
| `REACT_APP_BACKEND_URL` | Vercel | Points React to Render API |
| `MONGO_URL` | Render | MongoDB connection string |
| `DB_NAME` | Render | MongoDB database name |
| `ANTHROPIC_API_KEY` | Render | Claude API key for report enrichment |
| `LOVE_CLAUDE_MODEL` | Render | Override Claude model (default: claude-sonnet-4-5) |
| `RAZORPAY_KEY_ID` | Render | Payment gateway |
| `RAZORPAY_KEY_SECRET` | Render | Payment gateway |
| `RESEND_API_KEY` | Render | Email sending |
| `FROM_EMAIL` | Render | `noreply@everydayhoroscope.in` |
| `FACEBOOK_PAGE_ID` | Render | `1084672598054073` |
| `FACEBOOK_PAGE_ACCESS_TOKEN` | Render | Never-expiring System User token |
| `YOUTUBE_CLIENT_ID` | Render | Google Cloud OAuth |
| `YOUTUBE_CLIENT_SECRET` | Render | Google Cloud OAuth |
| `YOUTUBE_REDIRECT_URI` | Render | OAuth callback URL |
| `WHATSAPP_PHONE_NUMBER_ID` | Render | `1062698816928895` (pending OTP) |
| `WHATSAPP_ACCESS_TOKEN` | Render | WhatsApp-specific token (not FB System User) |
| `WHATSAPP_TEMPLATE_NAME` | Render | `everydayhoroscope_update` |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | Render | Pending |

---

## 13. Planned Features (Roadmap)

### 13.1 Auspicious Day / Date Calculator *(Design Phase -- GAI Collaboration)*

A high-precision muhurta calculator leveraging the existing Panchang engine's Swiss Ephemeris accuracy (hr:min:sec data). Two product branches:

**Branch A -- General Yearly Auspicious Days:**
Pre-computed calendar of auspicious dates and time windows for 7 life events:
1. Starting a New Business
2. Wedding / Vivah Muhurta
3. Griha Pravesh (House Warming)
4. Car Purchase / Vehicle Muhurta
5. Property Purchase / Bhumi Puja
6. Starting a New Job
7. Spiritual Work -- Pooja Ceremony, Dana Remedies, Mantra Deeksha

Methodology: Panchang yoga intersections (Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga), Tithi quality, Nakshatra suitability per event type, exclusion of inauspicious windows (Rahu Kaal, Yamaganda, Dur Muhurta).

**Branch B -- Personalised Muhurta (DOB-based):**
Same calendar overlaid with user's natal chart:
- Dasha-lord compatibility with proposed activity
- Transit of Jupiter/Venus/Moon relative to natal Ascendant and relevant house
- Personalised Choghadiya alignment
- Output: ranked auspicious windows with confidence score

**Integration point:** Builds directly on `panchang_router.py` (Branch A data) + `vedic_calculator.py` (Branch B natal overlay). No new astronomy engine required.

### 13.2 Other Planned Commissions

| Commission | Scope | Priority |
|---|---|---|
| IR-3 | 8 Love Report SEO landing pages | 🟠 HIGH |
| ARC-2 | Arc Angel Phase 2 (confidence scoring + questionnaire gating) | 🟠 HIGH (after KE Sprint 2) |
| KP-2B | Ritual Animation + 3-Pillar UX | 🟡 MED |
| KUN-1 | Lagna Kundali frontend (SVG chart + planet table + dasha timeline) | 🟡 MED |
| PUN-2 | Punya Rewards home promo + 8 module hooks | 🟡 MED |
| LK-1 | Lal Kitab standalone module | 🟡 MED |
| LON-1 | Ayur Jyotish Longevity Report | 🟢 Phase 2 |
| PAN-L1 | Panchang regional language pages (Tamil, Telugu, Malayalam) | 🟢 Phase 2 |
| ORACLE-P3 | 5 World Oracle Modules (Bible, Islamic, Taoist, Greek, Sikh) | 🔵 Phase 3 |
| IR-4 to IR-9 | 6 pending Individual Reports (Houses 2/5/6/7/9/11) | 🔵 Phase 3 |

---

## 14. Development Conventions

### Commit Format
```
feat(scope): description       # new feature
fix(scope): description        # bug fix
chore(scope): description      # config/deps
docs: description              # documentation only
```

### Backend Router Pattern (all report routers follow this)
1. `StrictModel(BaseModel)` with `model_config = ConfigDict(extra="forbid")`
2. `build_natal_snapshot()` from `vedic_shared_utils` for birth chart data
3. `build_transit_snapshot()` for current planet positions
4. `build_report_document()` to create the MongoDB document
5. `try_claude_generation()` from `love_prompt_common` for AI enrichment
6. Graceful fallback content always defined
7. Two endpoints: `POST /generate` (unauthenticated OK) + `GET /history` (auth required)

### Smart Quote Fix (Codex output often has Unicode curly quotes)
```bash
node -e "
let f=require('fs'),p='frontend/src/pages/TargetFile.jsx';
let c=f.readFileSync(p,'utf8');
c=c.replace(/"/g,'\"').replace(/"/g,'\"')
   .replace(/'/g,\"'\").replace(/'/g,\"'\");
f.writeFileSync(p,c);console.log('Done');"
```

### Build Verification
```bash
CI=true DISABLE_ESLINT_PLUGIN=true npx craco build
```

---

## 15. Key File Index

```
DailyHoroscope-Migration/
├── backend/
│   ├── server.py                          ⭐ Main FastAPI app (~2190 lines)
│   ├── panchang_router.py                 ⭐ Panchang engine v8-swiss
│   ├── vedic_calculator.py                ⭐ Birth chart + Dasha engine
│   ├── vedic_shared_utils.py              ⭐ Shared utility layer (all routers use this)
│   ├── love_prompt_common.py              ⭐ Shared Claude call helper
│   ├── individual_reports_prompt_common.py ⭐ Phase 1 report shared helper
│   ├── knowledge_engine.py               Knowledge Engine (interpretation only)
│   ├── kp_engine.py                      KP Oracle engine
│   ├── kundali_router.py                 Lagna Kundali (all endpoints live)
│   ├── ritual_trigger_router.py          Ritual Engine (5 trigger types)
│   ├── lunar_cycle_router.py             Lunar Cycle Wellness (Phase 2 IR)
│   ├── [*_router.py]                     One router per report/module
│   ├── [*_prompt_service.py]             One Claude prompt service per report
│   ├── Dockerfile                        python:3.12.9-slim + gcc + ffmpeg
│   └── requirements.txt
├── frontend/src/
│   ├── App.js                            All routes registered here
│   ├── pages/
│   │   ├── PanchangPage.jsx
│   │   ├── reports/
│   │   │   ├── IndividualReportsPage.jsx  Phase 1 hub (/reports)
│   │   │   ├── LoveReportsPage.jsx        Phase 2+3 hub (/love-reports)
│   │   │   ├── LovePage.jsx               Love Bundle landing (/love)
│   │   │   ├── PremiumReportsLanding.jsx  Public hub (/individual-reports)
│   │   │   └── landing/                   Public SEO landing pages
│   │   └── [other pages]
│   └── components/
│       ├── NavBar.jsx
│       ├── SEO.jsx
│       └── ShareCard.jsx
├── frontend/public/
│   ├── sitemap.xml
│   └── tarot_cards.json
├── Codex_Deliveries/                      Commission briefs + trackers
│   ├── MASTER_COMMISSION_TABLE.md
│   ├── List_of_Pending_Codex_Commissions.md
│   └── [Module]/TRACKER.md + briefs
├── EverydayHoroscope-WebApp_Architecture.md  ← this file
└── CLAUDE.md                              Claude Code working guide
```

---

*Document maintained by Temple Team. Update after each major module delivery or architectural decision.*
