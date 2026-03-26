# EverydayHoroscope — Claude Code Working Guide

> READ THIS FIRST. This file is the single source of truth for every Claude Code session.
> Last updated: 26 March 2026

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
│       │   ├── PanchangPage.jsx   # ⭐ Panchang UI (primary active file)
│       │   ├── TarotPage.jsx
│       │   ├── NumerologyPage.jsx
│       │   └── KundaliPage.jsx
│       └── components/
│           └── SEO.jsx
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

**Timing windows (8 total, sorted chronologically):**
- ✅ Brahma Muhurta (96 min pre-sunrise)
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

## 6. Frontend State (PanchangPage.jsx)

**Features live:**
- 6-tab sub-nav: Today / Tomorrow / Tithi / Choghadiya / Calendar / Festivals
- Location picker (91 cities, searchable by name/country/TZ abbreviation)
- TZ abbreviation badge on picker button + dropdown rows (IST/EST/GST/MYT etc.)
- 2×2 Sun/Moon card grid (Sunrise · Sunset · Moonrise · Moonset) with seconds
- Five Limbs card (Tithi/Nakshatra/Yoga/Karana/Vara) with end times
- Timing Windows card — **Auspicious** (green header) / **Inauspicious** (red header) sub-groups
- "Now" indicator on current active window
- Observances card (Ekadashi, Purnima, festivals etc.)
- Monthly calendar with Tithi per cell + festival dot
- Date-specific Panchang view with breadcrumb
- Full SEO + JSON-LD schema on all 7 routes
- localStorage persistence for selected city

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

## 10. What's Next — Panchang Module

The Panchang module core is complete. Remaining enhancements (in priority order):

1. **True Choghadiya** — 8 equal daylight slots with planetary rulers (Amrit/Shubh/Labh/Char/Udveg/Kaal/Rog). Currently the Choghadiya tab shows Panchang Muhurtas — needs its own calculation.
2. **Amrit Kalam** — Nakshatra-based auspicious window (Drik shows 06:50–08:21 AM for 26 Mar)
3. **Special Yogas** — Sarvartha Siddhi, Ravi Yoga (rule-based Tithi+Nakshatra+Vara combos)
4. **WhatsApp share card** — image card of daily Panchang for sharing
5. **SEO manual steps** — OG image upload, Google Search Console verification, GA4 wiring, Bing Webmaster

## 11. What's Next — Other Modules

See `PROJECT_STATUS.md` for the full Tranche 1 / Tranche 2 breakdown.

Key next modules after Panchang:
- **Tarot frontend** — `tarot_router.py` backend is live, frontend cards + UI needed
- **Numerology frontend** — `numerology_router.py` backend is live, frontend needed
- **Kundali / Birth Chart UI** — `vedic_calculator.py` is live, UI needed
- **Subscription / Paywall** — Razorpay integration for premium reports
