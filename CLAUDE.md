# EverydayHoroscope — Claude Code Working Guide

> READ THIS FIRST. This file is the single source of truth for every Claude Code session.
> Last updated: 29 March 2026

---

## 1. Project Identity

| Field | Value |
|---|---|
| Product | **EverydayHoroscope** — India's premium Vedic astrology platform |
| Live URL | https://www.everydayhoroscope.in |
| Backend API | https://everydayhoroscope-api.onrender.com |
| Repo | `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration` |
| Main branch | `main` (deploy-on-push) |

---

## 2. Infrastructure

| Layer | Platform | Deploy trigger | Approx time |
|---|---|---|---|
| Frontend (React) | **Vercel** | `git push main` | ~2 min |
| Backend (FastAPI) | **Render** (Docker) | `git push main` | ~3 min |
| Astronomy engine | **pyswisseph 2.10.x** — Swiss Ephemeris | bundled in backend | — |
| Database | **MongoDB** (Motor async driver) | Render env: MONGO_URL, DB_NAME | — |
| Payments | Razorpay | Render env: RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET | — |
| Email | Resend | Render env: RESEND_API_KEY, FROM_EMAIL | — |

---

## 3. Key File Locations

```
DailyHoroscope-Migration/
├── backend/
│   ├── server.py                  # ⭐ Main FastAPI app — all routers, social/YouTube/WhatsApp
│   ├── panchang_router.py         # ⭐ Panchang engine v8-swiss (primary active file)
│   ├── vedic_calculator.py        # Birth chart / Kundali engine
│   ├── tarot_router.py            # Tarot reading + reminder endpoints
│   ├── numerology_router.py       # Numerology + Ankjyotish premium report
│   ├── Dockerfile                 # python:3.12.9-slim + gcc + ffmpeg
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── PanchangPage.jsx      # ⭐ Panchang UI (primary active file)
│       │   ├── TarotPage.jsx         # Tarot draws + spreads
│       │   ├── NumerologyPage.jsx    # Numerology reports
│       │   ├── BirthChartPage.jsx    # Kundali / Birth Chart
│       │   ├── BrihatKundliPage.jsx  # Extended Kundali report
│       │   ├── DailyHoroscope.jsx    # Daily horoscope + share card
│       │   ├── WeeklyHoroscope.jsx   # Weekly horoscope + share card
│       │   └── MonthlyHoroscope.jsx  # Monthly horoscope + share card
│       └── components/
│           ├── SEO.jsx
│           └── ShareCard.jsx         # PanchangShareCard + HoroscopeShareCard + ShareButtons
├── frontend/public/
│   ├── sitemap.xml
│   ├── index.html                 # GSC + Bing meta verification tags
│   └── tarot_cards.json           # 78-card SVG bundle
├── CLAUDE.md                      # ← you are here
└── PROJECT_STATUS.md              # full progress tracker
```

---

## 4. Current Engine State

### Panchang Engine: `panchang-router-v8-swiss`
File: `backend/panchang_router.py`

**What it computes (all via pyswisseph swe.rise_trans + swe.calc_ut):**
- Sunrise, Sunset (with seconds) — verified vs Drik Panchang ±1 min
- Moonrise, Moonset (with seconds)
- Tithi (lunar day) + end time
- Nakshatra + end time
- Yoga + end time
- Karana + end time
- Paksha, Lunar month, Samvat, Sun/Moon signs
- Amrit Kalam (Nakshatra-based auspicious window)
- Special Yogas: Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga (Nakshatra × Weekday rules)
- True Choghadiya: 8 equal daylight + 8 nighttime slots with planetary rulers

**Timing windows (sorted chronologically, includes Amrit Kalam):**
- ✅ Brahma Muhurta (96 min pre-sunrise)
- ✅ Amrit Kalam (Nakshatra-based)
- ⛔ Rahu Kaal (kaal-based, weekday-specific)
- ⛔ Yamaganda (kaal-based)
- 🔶 Gulika Kaal (kaal-based)
- ⛔ Dur Muhurta × 2 (muhurta-based)
- ✅ Abhijit Muhurta (solar noon ± 24 min)
- ✅ Vijaya Muhurta (muhurta-based, weekday-specific)

**Location catalogue: 318 cities across 81 countries/regions**
India, USA, Canada, Mexico, Brazil, Argentina, Chile, Peru, Colombia, Venezuela,
Ecuador, Bolivia, Paraguay, Uruguay, UK, Ireland, France, Germany, Spain, Italy,
Netherlands, Belgium, Switzerland, Austria, Portugal, Sweden, Norway, Denmark,
Finland, Poland, Czech Republic, Hungary, Romania, Greece, Turkey, Russia, Ukraine,
Israel, UAE, Saudi Arabia, Qatar, Kuwait, Bahrain, Oman, Egypt, South Africa,
Nigeria, Kenya, Ethiopia, Morocco, Algeria, Tunisia, Ghana, Tanzania, Uganda,
Nepal, Sri Lanka, Bangladesh, Pakistan, Afghanistan, China, Hong Kong, Taiwan,
Japan, South Korea, Singapore, Malaysia, Indonesia, Thailand, Vietnam, Philippines,
Cambodia, Laos, Myanmar, Mongolia, Tibet, Australia, New Zealand, Fiji,
Papua New Guinea, Samoa

**API routes:**
- `GET /api/panchang/locations` — full catalogue
- `GET /api/panchang/daily?date=YYYY-MM-DD&location_slug=xxx`
- `GET /api/panchang/date/{date}`
- `GET /api/panchang/calendar/{year}/{month}`
- `GET /api/panchang/festivals?year=YYYY`

---

## 5. Accuracy Benchmark (New Delhi, 26 March 2026, Thursday)

| Field | Our Engine | Drik Panchang | Status |
|---|---|---|---|
| Sunrise | 06:18:23 | 06:18 | ✅ |
| Sunset | 18:35:xx | 18:36 | ✅ ~1 min |
| Tithi | Shukla Ashtami | Shukla Ashtami | ✅ |
| Nakshatra | Ardra | Ardra | ✅ |
| Yoga | Shobhana | Shobhana | ✅ |
| Rahu Kaal | 01:58 PM | 01:59 PM | ✅ |
| Yamaganda | 06:18 AM | 06:18 AM | ✅ |
| Abhijit | 12:02 PM | 12:02 PM | ✅ |
| Dur Muhurta | 10:24 AM | 10:24 AM | ✅ |
| Vijaya Muhurta | 02:30 PM | 02:30 PM | ✅ |
| Moonrise | 11:59 AM | 11:59 AM | ✅ |

---

## 6. Frontend State

### PanchangPage.jsx ✅ Live
- 6-tab sub-nav: Today / Tomorrow / Tithi / Choghadiya / Calendar / Festivals
- Location picker (318 cities across 81 countries, searchable by name/country/TZ abbreviation)
- TZ abbreviation badge on picker button + dropdown rows (IST/EST/GST/MYT etc.)
- 2×2 Sun/Moon card grid (Sunrise · Sunset · Moonrise · Moonset) with seconds
- Five Limbs card (Tithi/Nakshatra/Yoga/Karana/Vara) with end times
- Timing Windows card — **Auspicious** (green header) / **Inauspicious** (red header) sub-groups incl. Amrit Kalam
- "Now" indicator on current active window
- Special Yogas card (Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga)
- Choghadiya tab — 8 daylight + 8 nighttime slots with planetary rulers and quality badges
- Observances card (Ekadashi, Purnima, festivals etc.)
- Monthly calendar with Tithi per cell + festival dot
- Date-specific Panchang view with breadcrumb
- Full SEO + JSON-LD schema on all 7 routes
- localStorage persistence for selected city
- **Share card** — `PanchangShareCard` + `ShareButtons` (WhatsApp/Facebook/X/Instagram/YouTube/Save/Copy)
- **Post to Facebook Page** — one-click from share buttons (requires admin login)

### TarotPage.jsx ✅ Live
- 3 tabs: Daily Draw / Spreads / History
- Flipping card animation, 78-card SVG deck from `tarot_cards.json`
- Multi-card spread grid, bookmark/history tracking

### NumerologyPage.jsx ✅ Live
- 4 tabs: Select Report / Generate / Report / History
- 10 report types (Life Path, Name Correction, Karmic Debt, Relationship, Career, etc.)
- Computed numbers grid, guidance + remedy notes

### BirthChartPage.jsx + BrihatKundliPage.jsx ✅ Live
- Full Kundali / Birth Chart UI exists (two separate pages)
- Backend: `vedic_calculator.py`

### Horoscope Pages (Daily / Weekly / Monthly) ✅ Live
- **Share card** — `HoroscopeShareCard` + `ShareButtons` on all three pages
- Element-based color theming (Fire/Earth/Air/Water)
- **Post to Facebook Page** — one-click with sign + date caption

### Admin Console (/admin/dashboard) ✅ Live
- Overview, System, Users, Reports, Payments, Messages, Blog, Notifications tabs
- **Notifications tab** — 5 sub-tabs:
  - **Subscribers** — Add/edit/delete (name, email, phone, tags). MongoDB: `subscribers`
  - **Compose** — HTML email, audience filter (all / by tag), send now or schedule
  - **Scheduled** — view/cancel upcoming sends. MongoDB: `scheduled_notifications`
  - **History** — full send log. MongoDB: `notification_logs`
  - **Social Media** — post share cards to Facebook + YouTube; channel checkboxes; image upload or URL; post history log. MongoDB: `social_post_logs`
- Email via Resend ✅ working
- WhatsApp — enabled in UI, backend wired to Meta Cloud API v22.0; **blocked on phone number verification** (status: Pending — needs OTP + payment method on Meta)
- Facebook posting ✅ working (System User token → Page token exchange)
- YouTube posting ✅ working (OAuth via Google Cloud; background task; ~2–4 min upload)
- Instagram — coming soon (Business Account ID pending)

---

## 7. Share Cards (ShareCard.jsx)

### PanchangShareCard
- 900px wide, `position: fixed; left: -9999px; top: 0` (no flash on capture)
- Header: gold branding, date, location
- 4-column Sun/Moon row (Sunrise/Sunset/Moonrise/Moonset)
- 3×2 Five Limbs grid
- Side-by-side Auspicious (green) / Inauspicious (red) timing tables from `day_quality_windows`
- Special Yoga badge + Observance row + Footer

### HoroscopeShareCard
- 900px wide, same offscreen positioning
- Sign symbol in element-colored circle (Fire/Earth/Air/Water)
- Sign name, dates, element, type badge, overview (first 2 sentences), lucky elements, footer

### ShareButtons
- 7 buttons: WhatsApp, Facebook, X, Instagram, YouTube, Save Card, Copy Link
- Mobile: `navigator.share({ files })` Web Share API (native share sheet)
- Desktop: `canvas.toDataURL()` → synchronous anchor click (reliable download)
- iOS Safari: `canvas.toBlob()` → `window.open()` (long-press to save)
- html2canvas capture uses `onclone` option — real DOM never moves, zero flash
- "Post to Page" Facebook button appears when `fbPageCaption` prop is passed

---

## 8. YouTube Integration (server.py)

- **OAuth flow**: Google Cloud OAuth 2.0 → refresh token stored in MongoDB (`app_settings.youtube_refresh_token`)
- **Upload pipeline**: PNG share card → ffmpeg (libx264 veryfast, CRF 18, -tune stillimage, -threads 1, 30s) → MP4 → YouTube Data API v3 resumable upload
- **Background task**: YouTube runs as FastAPI `BackgroundTasks` — response returns immediately, upload happens async (~2–4 min). Check Post History or YouTube Studio to confirm.
- **Key lesson**: ffmpeg with default preset pins CPU at 100% for 30+ sec → Render health-check restart. Fix: `-preset veryfast -threads 1` keeps encode to ~10s.
- **API routes**: `/api/admin/youtube/status`, `/api/admin/youtube/auth-url`, `/api/admin/youtube/callback`, `/api/admin/youtube/disconnect`
- **YouTube Studio**: studio.youtube.com → Content → Videos to verify uploads

---

## 9. WhatsApp Integration (server.py)

- **API**: Meta Cloud API v22.0 — `POST /v22.0/{phone_number_id}/messages`
- **Template**: `everydayhoroscope_update` with named variables `{{customer_name}}` + `{{update_content}}`
- **Current blocker**: Phone number `+91 96431 10001` (ID: `1062698816928895`) status = **Pending**
  - Fix: WhatsApp Manager → Phone Numbers → complete OTP verification
  - Also: add payment method to WABA (Meta requires card on file even for free-tier usage)
- **WABA ID**: `754513054261096`
- **Token**: Must be WhatsApp-specific token from API Setup page (not the Facebook System User token)

---

## 10. Commit Protocol

**Always use this format:**
```
feat(scope): description       # new feature
fix(scope): description        # bug fix
chore(scope): description      # config/deps
docs: description              # documentation only
```

**Never use the GitHub browser editor** — always commit via terminal or Claude Code.

**Before every backend change** — bump ENGINE_VERSION in `panchang_router.py`:
```python
ENGINE_VERSION = "panchang-router-v9-swiss"  # increment version
```

**⚠️ Render rolling deploys kill in-flight background tasks.** Avoid pushing code while a YouTube upload test is in progress — wait for the upload to complete first (check Post History), then push.

---

## 11. Codex Workflow — How External Code Gets Integrated

### What is Codex?
Codex (OpenAI) is a separate AI tool Prateek uses to generate feature code in parallel.
**Codex does NOT have GitHub access** — it cannot see the repo, push code, or read existing files.
Prateek submits a written brief → receives generated code → pastes it here for integration.

### The Workflow
```
Step 1 → Claude Code drafts a Codex Commission Brief (spec: inputs, outputs, file names, style)
Step 2 → Prateek submits brief to Codex → receives generated code
Step 3 → Prateek pastes Codex output into this chat
Step 4 → Claude Code reviews, adapts, and integrates into Temple App:
           - Aligns to Temple App theme (CSS vars, GlassCard pattern)
           - Wires React Router in App.js
           - Registers FastAPI routers in backend/main.py
           - Fixes curly/smart quotes (common Codex output issue)
           - Verifies build: CI=true DISABLE_ESLINT_PLUGIN=true npx craco build
           - Commits to main
```

### Smart Quote Fix (Common Codex Issue)
Codex output often contains Unicode curly quotes that break Babel:
```bash
node -e "
let f=require('fs'),p='frontend/src/pages/TargetFile.jsx';
let c=f.readFileSync(p,'utf8');
c=c.replace(/\u201c/g,'\"').replace(/\u201d/g,'\"')
   .replace(/\u2018/g,\"'\").replace(/\u2019/g,\"'\");
f.writeFileSync(p,c);console.log('Done');"
```

### Temple App Theme (always align Codex output to these tokens)
| Token | Usage |
|---|---|
| `bg-background` | Page background |
| `bg-card` | Card/panel surface |
| `text-foreground` | Primary text |
| `text-muted-foreground` | Secondary text |
| `text-gold` / `border-gold` / `bg-gold` | Gold accent (`#c5a059`) |

**GlassCard:** `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`
**Gold tile:** `bg-gradient-to-br from-gold/15 to-gold/5`

---

## 12. Local Dev Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn server:app --reload --port 8000
# API available at http://localhost:8000

# Frontend
cd frontend
npm install
npm start
# App at http://localhost:3000
# Set REACT_APP_BACKEND_URL=http://localhost:8000 in .env.local
```

---

## 12. Environment Variables

| Variable | Where set | Purpose |
|---|---|---|
| `REACT_APP_BACKEND_URL` | Vercel env | Points frontend to Render API |
| `MONGO_URL` | Render env | MongoDB connection string |
| `DB_NAME` | Render env | MongoDB database name |
| `RAZORPAY_KEY_ID` | Render env | Payments — **new test keys active (29 Mar 2026)** |
| `RAZORPAY_KEY_SECRET` | Render env | Payments — new test keys active |
| `RESEND_API_KEY` | Render env | Email sending ✅ working |
| `FROM_EMAIL` | Render env | Sender address (noreply@everydayhoroscope.in) |
| `FACEBOOK_PAGE_ID` | Render env | `1084672598054073` ✅ confirmed |
| `FACEBOOK_PAGE_ACCESS_TOKEN` | Render env | System User token (never expires) ✅ |
| `YOUTUBE_CLIENT_ID` | Render env | Google Cloud OAuth client ✅ |
| `YOUTUBE_CLIENT_SECRET` | Render env | Google Cloud OAuth secret ✅ |
| `YOUTUBE_REDIRECT_URI` | Render env | `https://everydayhoroscope-api.onrender.com/api/admin/youtube/callback` ✅ |
| `WHATSAPP_PHONE_NUMBER_ID` | Render env | `1062698816928895` — set, but phone Pending |
| `WHATSAPP_BUSINESS_ACCOUNT_ID` | Render env | `754513054261096` — set |
| `WHATSAPP_ACCESS_TOKEN` | Render env | Must be WhatsApp-specific token (not FB System User token) |
| `WHATSAPP_TEMPLATE_NAME` | Render env | `everydayhoroscope_update` (pending Meta approval) |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | Render env | Pending (Instagram loading issue in Meta dashboard) |

---

## 13. Completed Features (as of 29 March 2026)

| Feature | Status |
|---|---|
| Panchang engine (Tithi/Nakshatra/Yoga/Karana/Vara/Sunrise/Moonrise) | ✅ |
| True Choghadiya (8 daylight + 8 night slots, planetary rulers) | ✅ |
| Amrit Kalam (Nakshatra-based window) | ✅ |
| Special Yogas (Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga) | ✅ |
| Panchang share card (WhatsApp/Facebook/Instagram/YouTube/Save) | ✅ |
| Horoscope share cards (Daily/Weekly/Monthly) | ✅ |
| Share card download — desktop + mobile + iOS Safari | ✅ |
| Facebook Page posting — one-click from Panchang + Horoscope pages + Admin Console | ✅ |
| YouTube posting — share card → MP4 → YouTube Shorts via Admin Console | ✅ |
| Tarot frontend (flipping cards, spreads, history) | ✅ |
| Numerology frontend (10 report types) | ✅ |
| Kundali / Birth Chart UI (BirthChartPage + BrihatKundliPage) | ✅ |
| Razorpay subscription / paywall (new test keys active) | ✅ |
| SEO — OG tags, GA4 (G-3HJC8BTHRQ), JSON-LD schema | ✅ |
| Google Search Console — verified + sitemap submitted | ✅ |
| Bing Webmaster Tools — verified + sitemap submitted | ✅ |
| Admin Console — subscriber management | ✅ |
| Admin Console — email notifications via Resend | ✅ |
| Admin Console — scheduled notifications (APScheduler) | ✅ |
| Admin Console — notification history log | ✅ |
| Admin Console — Social Media tab (Facebook + YouTube post + history) | ✅ |

---

## 14. In Progress / Pending

| Task | Status | Blocker |
|---|---|---|
| WhatsApp notifications | 🔜 | Phone `+91 96431 10001` Pending — complete OTP + add payment method on Meta |
| Instagram posting | 🔜 | Instagram Business Account ID not loading in Meta dashboard |
| Scheduled daily social posts (6 AM auto-post to FB + YT) | 🔜 | APScheduler ready, needs endpoint + Admin Console toggle |
| YouTube upload speed | 🔜 | Currently ~2–4 min; improving with veryfast+CRF18 preset (deployed 29 Mar) |
| Razorpay live keys | 🔜 | Upload only when ready for Play Store |

---

## 16. Architecture Rule — Legacy Model (MANDATORY — READ BEFORE TOUCHING ARC ANGEL OR KNOWLEDGE ENGINE)

> **Decision date:** 19 April 2026. This rule is locked and must be respected in every commission brief, every backend route, and every Claude Code session.

### The Rule

**All live astronomical and dasha computations MUST use the Legacy Model (`vedic_calculator.py` + `pyswisseph`). The Knowledge Engine (`knowledge_engine.py`) is the interpretation layer ONLY — it must never replace, duplicate, or bypass the Legacy Model for live data.**

### What "Legacy Model" means

| File | Role | Status |
|---|---|---|
| `backend/vedic_calculator.py` | Computes all live data: Mahadasha timeline, current dasha, birth chart, planetary positions | ✅ Production — do NOT replace |
| `backend/panchang_router.py` | Computes all Panchang data via pyswisseph | ✅ Production — do NOT replace |
| `backend/knowledge_engine.py` | Interprets chart data against curated rules library | 🔒 Interpretation only — zero `approved` rules until co-founder sign-off |

### Key functions in vedic_calculator.py (single source of truth)

```python
calculate_vimshottari_dasha(birth_date, moon_longitude)
# → Returns list of 9 Mahadasha dicts: {planet, start_date, end_date, years, antardashas}

get_current_dasha(dashas)
# → Returns currently active Mahadasha dict

DASHA_ORDER = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']
DASHA_YEARS = {'Ketu':7,'Venus':20,'Sun':6,'Moon':10,'Mars':7,'Rahu':18,'Jupiter':16,'Saturn':19,'Mercury':17}
```

### Integrated Approach (Arc Angel and all future modules)

```
Phase 1 (NOW):   Legacy Model provides dasha baseline → period_quality assigned via
                 planetary benefic/malefic logic in vedic_calculator.py
                 → Knowledge Engine rules are additive only if approval_status = 'approved'
                 → No approved rules yet → Legacy Model is the ONLY signal

Phase 2 (when co-founder approves rules):
                 Legacy Model baseline + Knowledge Engine interpretation layer
                 → KE supplements, never replaces Legacy data
```

### What this means for backend routes

- `GET /api/knowledge-engine/arc-angel-windows` MUST call `vedic_calculator.calculate_vimshottari_dasha()` — NOT any function inside `knowledge_engine.py` that replicates dasha calculation.
- The duplicate `compute_dasha_timeline()` in `knowledge_engine.py` (added by Codex in Sprint 3) MUST be removed and replaced with an import from `vedic_calculator`.
- Period quality (auspicious/inauspicious) defaults to **planetary natural benefic/malefic classification** from the Legacy Model when zero approved KE rules exist.

### Natural Benefic / Malefic baseline (Legacy Model defaults)

| Planet | Quality |
|---|---|
| Jupiter, Venus, Mercury (waxing), Moon (waxing) | Natural Benefic → Auspicious |
| Saturn, Mars, Rahu, Ketu, Sun | Natural Malefic → Inauspicious |
| Mercury (waning), Moon (waning) | Context-dependent → Neutral |

### Commission Brief Checklist (MANDATORY before drafting any Codex brief)

Before drafting ANY new Codex commission brief:
1. ✅ Verify item exists in CPath-1 list (CONTRACT.md Section 21)
2. ✅ Confirm exact item number and phase
3. ✅ Confirm all dependency items are complete
4. ✅ Read the relevant locked spec section in CONTRACT.md (TD-xx)
5. ✅ Read the original docx mockup if one exists (`.claude/` folder)
6. ✅ State explicitly in the brief: "All dasha/astronomical data must come from `vedic_calculator.py`"
7. ✅ State explicitly in the brief: "Do NOT add dasha calculation functions to `knowledge_engine.py`"

---

## 15. Meta / Social API Reference

| Credential | Value | Status |
|---|---|---|
| Meta Developer App | WA-YT Integrator (ID: 1594770155009283) | ✅ |
| Business Manager ID | 878532341248169 | ✅ |
| Facebook Page | EverydayHoroscope | ✅ |
| Facebook Page ID | `1084672598054073` | ✅ confirmed |
| Facebook System User | EverydayHoroscope Bot | ✅ created |
| Facebook Page Access Token | System User token (never expires) | ✅ set on Render |
| YouTube OAuth | Google Cloud Project, OAuth 2.0 Web Client | ✅ connected via Admin Console |
| YouTube Channel | EverydayHoroscope | ✅ connected |
| Instagram Business Account ID | — | 🔜 pending |
| WhatsApp Phone Number ID | `1062698816928895` (+91 96431 10001) | 🔜 Pending verification |
| WhatsApp WABA ID | `754513054261096` | ✅ |
