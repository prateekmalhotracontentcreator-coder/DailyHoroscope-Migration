# EverydayHoroscope — Claude Code Working Guide

> READ THIS FIRST. This file is the single source of truth for every Claude Code session.
> Last updated: 28 March 2026

---

## 1. Project Identity

| Field | Value |
|---|---|
| Product | **EverydayHoroscope** — India's premium Vedic astrology platform |
| Live URL | https://www.everydayhoroscope.in |
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
│   ├── main.py                    # FastAPI app entry, router registration
│   ├── panchang_router.py         # ⭐ Panchang engine v8-swiss (primary active file)
│   ├── vedic_calculator.py        # Birth chart / Kundali engine
│   ├── tarot_router.py            # Tarot reading + reminder endpoints
│   ├── numerology_router.py       # Numerology + Ankjyotish premium report
│   ├── admin_router.py            # ⭐ Admin console — subscribers, notifications, scheduler
│   ├── Dockerfile                 # python:3.12.9-slim
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

**Location catalogue: 91 cities across 13 countries**
India (53 cities), USA (8), UK (3), Canada (3), UAE (2), Australia (3),
Singapore (1), Malaysia (3), Indonesia (3), Thailand (2), Tibet (1),
Nepal (1), New Zealand (1)

**API routes:**
- `GET /api/panchang/locations` — full catalogue
- `GET /api/panchang/daily?date=YYYY-MM-DD&location_slug=xxx`
- `GET /api/panchang/date/{date}`
- `GET /api/panchang/calendar/{year}/{month}`
- `GET /api/panchang/festivals?year=YYYY`
- `GET /api/panchang/tithi` (via daily)
- `GET /api/panchang/choghadiya` (via daily)

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
- Location picker (91 cities, searchable by name/country/TZ abbreviation)
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

### Admin Console (/admin/dashboard) ✅ Live
- Overview, System, Users, Reports, Payments, Messages, Blog, Notifications tabs
- **Notifications tab** — 4 sub-tabs:
  - **Subscribers** — Add/edit/delete (name, email, phone, tags). MongoDB collection: `subscribers`
  - **Compose** — HTML email, audience filter (all / by tag), send now or schedule
  - **Scheduled** — view/cancel upcoming sends. MongoDB collection: `scheduled_notifications`
  - **History** — full send log. MongoDB collection: `notification_logs`
- Email via Resend ✅ working
- WhatsApp channel — UI stub present, backend pending (BSP not yet selected)
- Social media posting — pending (Meta API credentials in progress)

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

---

## 8. Commit Protocol

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

---

## 9. Local Dev Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# API available at http://localhost:8000
# Test: curl http://localhost:8000/api/panchang/daily?location_slug=new-delhi-india

# Frontend
cd frontend
npm install
npm start
# App at http://localhost:3000
# Set REACT_APP_BACKEND_URL=http://localhost:8000 in .env.local
```

---

## 10. Environment Variables

| Variable | Where set | Purpose |
|---|---|---|
| `REACT_APP_BACKEND_URL` | Vercel env | Points frontend to Render API |
| `MONGO_URL` | Render env | MongoDB connection string |
| `DB_NAME` | Render env | MongoDB database name |
| `RAZORPAY_KEY_ID` | Render env | Payments (test keys active) |
| `RAZORPAY_KEY_SECRET` | Render env | Payments (test keys active) |
| `RESEND_API_KEY` | Render env | Email sending ✅ working |
| `FROM_EMAIL` | Render env | Sender address (e.g. noreply@everydayhoroscope.in) |
| `WHATSAPP_PHONE_NUMBER_ID` | Render env | Meta Cloud API — pending |
| `WHATSAPP_BUSINESS_ACCOUNT_ID` | Render env | Meta Cloud API — pending |
| `WHATSAPP_ACCESS_TOKEN` | Render env | Meta Cloud API — pending |
| `FACEBOOK_PAGE_ID` | Render env | `1084672598054073` — confirmed |
| `FACEBOOK_PAGE_ACCESS_TOKEN` | Render env | System User token — obtained, set on Render |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | Render env | Pending (Instagram loading issue) |

---

## 11. Completed Features (as of 28 March 2026)

| Feature | Status |
|---|---|
| Panchang engine (Tithi/Nakshatra/Yoga/Karana/Vara/Sunrise/Moonrise) | ✅ |
| True Choghadiya (8 daylight + 8 night slots, planetary rulers) | ✅ |
| Amrit Kalam (Nakshatra-based window) | ✅ |
| Special Yogas (Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga) | ✅ |
| Panchang share card (WhatsApp/Facebook/Instagram/YouTube/Save) | ✅ |
| Horoscope share cards (Daily/Weekly/Monthly) | ✅ |
| Share card download — desktop + mobile + iOS Safari | ✅ |
| Tarot frontend (flipping cards, spreads, history) | ✅ |
| Numerology frontend (10 report types) | ✅ |
| Kundali / Birth Chart UI (BirthChartPage + BrihatKundliPage) | ✅ |
| Razorpay subscription / paywall | ✅ test keys active |
| SEO — OG tags, GA4 (G-3HJC8BTHRQ), JSON-LD schema | ✅ |
| Google Search Console — verified | ✅ |
| Bing Webmaster Tools — verified | ✅ |
| Sitemap submitted to Bing | ✅ |
| Admin Console — subscriber management | ✅ |
| Admin Console — email notifications via Resend | ✅ |
| Admin Console — scheduled notifications (APScheduler) | ✅ |
| Admin Console — notification history log | ✅ |
| Facebook Page posting — one-click from Panchang + Horoscope pages | ✅ |
| Admin Console — Social Media tab (post + file upload + history) | ✅ |

---

## 12. In Progress / Pending

| Task | Status | Blocker |
|---|---|---|
| Google Search Console sitemap submission | 🔜 | Manual step — submit sitemap.xml in GSC dashboard |
| WhatsApp notifications (Meta Cloud API) | 🔜 | Need WHATSAPP_PHONE_NUMBER_ID + ACCESS_TOKEN on Render |
| Facebook page posting | ✅ | Working — one-click from Panchang/Horoscope pages + Admin Console |
| Instagram posting | 🔜 | Instagram Business Account ID pending (loading issue) |
| Razorpay live keys | 🔜 | Upload only when ready for Play Store |
| Social media Admin Console channels | 🔜 | Depends on Meta API credentials above |

---

## 13. Meta / Social API Reference

| Credential | Value | Status |
|---|---|---|
| Meta Developer App | WA-YT Integrator (ID: 1594770155009283) | ✅ |
| Business Manager ID | 878532341248169 | ✅ |
| Facebook Page | EverydayHoroscope | ✅ |
| Facebook Page ID | `1084672598054073` | ✅ confirmed |
| Facebook System User | EverydayHoroscope Bot | ✅ created |
| Facebook Page Access Token | System User token (never expires) | ✅ obtained |
| Instagram Business Account ID | — | 🔜 pending |
| WhatsApp Phone Number ID | — | 🔜 pending BSP setup |
