# EverydayHoroscope — Claude Code Working Guide

> READ THIS FIRST. This file is the single source of truth for every Claude Code session.
> Last updated: 27 March 2026

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
| Auth / DB | Supabase (Postgres + Auth) | external | — |
| Payments | Razorpay | external | — |

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
│   ├── Dockerfile                 # python:3.12.9-slim
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── PanchangPage.jsx      # ⭐ Panchang UI (primary active file)
│       │   ├── TarotPage.jsx         # Tarot draws + spreads
│       │   ├── NumerologyPage.jsx    # Numerology reports
│       │   ├── BirthChartPage.jsx    # Kundali / Birth Chart
│       │   └── BrihatKundliPage.jsx  # Extended Kundali report
│       └── components/
│           ├── SEO.jsx
│           └── ShareCard.jsx         # PanchangShareCard + HoroscopeShareCard + ShareButtons
├── frontend/public/
│   ├── sitemap.xml
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

### PanchangPage.jsx
**Features live:**
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

---

## 7. Commit Protocol

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

## 8. Local Dev Setup

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

## 9. Environment Variables

| Variable | Where set | Purpose |
|---|---|---|
| `REACT_APP_BACKEND_URL` | Vercel env | Points frontend to Render API |
| `SUPABASE_URL` | Render env | Database connection |
| `SUPABASE_KEY` | Render env | Auth |
| `RAZORPAY_KEY_ID` | Render env | Payments |
| `RAZORPAY_KEY_SECRET` | Render env | Payments |

---

## 10. Completed Features (as of 27 March 2026)

| Feature | Status |
|---|---|
| Panchang engine (Tithi/Nakshatra/Yoga/Karana/Vara/Sunrise/Moonrise) | ✅ |
| True Choghadiya (8 daylight + 8 night slots, planetary rulers) | ✅ |
| Amrit Kalam (Nakshatra-based window) | ✅ |
| Special Yogas (Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga) | ✅ |
| Panchang share card (WhatsApp/Facebook/Instagram/YouTube/Save) | ✅ |
| Horoscope share cards (Daily/Weekly/Monthly) | ✅ |
| Tarot frontend (flipping cards, spreads, history) | ✅ |
| Numerology frontend (10 report types) | ✅ |
| Kundali / Birth Chart UI (BirthChartPage + BrihatKundliPage) | ✅ |
| Razorpay subscription / paywall | ✅ test keys active on Render |
| SEO — OG tags, GA4 (G-3HJC8BTHRQ), JSON-LD schema | ✅ |

## 11. What's Next (in priority order)

### Sprint A — SEO Verification (quick, 1 session)
1. **Google Search Console verification** — add `google-site-verification` meta tag to `frontend/public/index.html`. Tag obtained from GSC dashboard → Verify ownership → HTML tag method.
2. **Bing Webmaster** — add `msvalidate.01` meta tag to `frontend/public/index.html`. Tag from Bing Webmaster Tools → Add site → HTML meta tag.

### Sprint B — Push Notifications
3. **Daily reminders** — WhatsApp (via Interakt/Wati) or email (via Resend/Mailgun) for daily Panchang + horoscope. Needs: user opt-in UI, backend cron job, provider integration.

### Sprint C — Premium Scheduler (larger sprint)
4. **Premium member card send-outs** — cron job that generates Panchang share card images and delivers to subscribed users via WhatsApp/email. Depends on Sprint B provider choice.

### Razorpay
- Test keys active on Render ✅
- Live keys: upload only when ready for Play Store testing
