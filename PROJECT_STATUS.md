# EverydayHoroscope — Project Status

> Last updated: 26 March 2026  
> Based on 11 chat sessions + 45 commits in `DailyHoroscope-Migration`

---

## TL;DR

| Layer | Status |
|---|---|
| Infrastructure (Vercel + Render + Docker) | ✅ Live |
| Panchang Module (full) | ✅ Live & verified |
| Vedic Calculator backend | ✅ Committed |
| Tarot backend (78 cards + reminders) | ✅ Committed |
| Numerology backend (Ankjyotish premium) | ✅ Committed |
| Tarot frontend UI | ❌ Not started |
| Numerology frontend UI | ❌ Not started |
| Kundali / Birth Chart UI | ❌ Not started |
| Subscription / Paywall | ❌ Not started |
| SEO manual steps (GSC, GA4, OG image) | ⏳ Pending manual action |

---

## Tranche 1 — Backend Foundation

### ✅ Contract 1 — vedic_calculator.py
**Status: COMPLETE**
- Migrated from `flatlib` (Python 3.11 only) to `pyswisseph` (Python 3.12 compatible)
- Computes: birth chart, house positions, planet longitudes, Lagna, Navamsa
- File: `backend/vedic_calculator.py`
- Commit: `43327a2`

### ✅ Contract 2 — panchang_router.py
**Status: COMPLETE — v8-swiss engine**

Full Vedic Panchang API with:
- Swiss Ephemeris precision (pyswisseph swe.rise_trans)
- 5 Panchang limbs (Tithi, Nakshatra, Yoga, Karana, Vara)
- 8 timing windows (Brahma Muhurta, Rahu Kaal, Yamaganda, Gulika, Dur Muhurta ×2, Abhijit, Vijaya)
- Moonrise + Moonset
- 91 city catalogue across 13 countries
- All times with seconds
- 5 REST endpoints + locations endpoint
- Verified vs Drik Panchang (all fields ✅ or within ±1 min)

Commit history:
- `f09d4a0` — v3-swiss initial
- `51013c4` — v5-swiss: swe.rise_trans sunrise
- `f2b72be` — v6-swiss: Yamaganda + Dur Muhurta fixes
- `1dfdaec` — location selector (40 cities)
- `ed23e75` — TZ abbreviations (IST/EST/GST etc.)
- `c05e511` — 91 cities: 53 Indian + Malaysia/Indonesia/Thailand/Tibet
- `2f9c5a3` — v8-swiss: Moonrise/Moonset + Brahma/Vijaya Muhurta
- `42b5d88` — Frontend: 2×2 Sun/Moon cards + Auspicious/Inauspicious headers
- `50d6a5c` — Seconds added to all times

### ✅ Contract 3 — numerology_router.py
**Status: COMPLETE (backend only)**
- 11 numerology tiles
- Premium Ankjyotish report: Lo Shu grid, Vedic cross-reference, lucky elements, 7-day remediation
- File: `backend/numerology_router.py`
- Commit: `1ed9d70`
- **Frontend UI: NOT YET BUILT**

### ✅ Contract 4 — tarot_router.py + tarot_cards.json
**Status: COMPLETE (backend only)**
- Full 78-card deck (22 Major Arcana + 56 Minor Arcana)
- SVG bundle: `frontend/public/tarot_cards.json`
- 3 reminder endpoints (set/get/delete)
- File: `backend/tarot_router.py`
- Commits: `715caff`, `90c1ccc`
- **Frontend UI: NOT YET BUILT**

---

## Tranche 2 — Frontend Modules

### ✅ Panchang Frontend — COMPLETE
File: `frontend/src/pages/PanchangPage.jsx`

All views live:
- Today / Tomorrow Panchang
- Tithi view (with Moonrise/Moonset)
- Choghadiya / Timing Windows (Auspicious + Inauspicious sub-headers)
- Monthly Calendar (Tithi per day, festival dots)
- Festivals & Vrats list
- Date-specific Panchang
- Location picker (91 cities, TZ-aware, localStorage persistence)
- Full SEO + JSON-LD on all 7 routes
- Sitemap updated

**Panchang Pending Enhancements:**

| # | Item | Effort |
|---|---|---|
| 1 | True Choghadiya (8 slots with planetary rulers) | Medium |
| 2 | Amrit Kalam | Small |
| 3 | Special Yogas (Sarvartha Siddhi, Ravi Yoga) | Medium |
| 4 | WhatsApp share card | Medium |
| 5 | OG image (1200×630px) to `frontend/public/og-image.png` | Manual |
| 6 | Google Search Console verification + sitemap submit | Manual |
| 7 | GA4 measurement ID in index.html | Manual |
| 8 | Bing Webmaster Tools | Manual |

### ❌ Tarot Frontend — NOT STARTED
**Backend is live.** Frontend needs:
- Card flip animation
- 3-card / Celtic Cross spread layouts
- Card detail modal (meaning, reversed meaning)
- Daily card feature
- Reminder setup UI (links to backend endpoints)
- Premium gating (paid spreads)

### ❌ Numerology Frontend — NOT STARTED
**Backend is live.** Frontend needs:
- Birth date / name input form
- Life Path, Expression, Soul Urge tiles
- Premium Ankjyotish report display
- Lo Shu grid visualization
- 7-day remediation display

### ❌ Kundali / Birth Chart UI — NOT STARTED
**Backend (vedic_calculator.py) is live.** Frontend needs:
- Birth details form (date/time/place)
- Chart wheel SVG renderer
- Planet positions table
- Navamsa chart
- Dasha periods display
- Kundali Milan (compatibility matching)

### ❌ Subscription / Paywall — NOT STARTED
- Razorpay integration
- Premium plan definitions (Free / Basic / Pro)
- Report unlock flow
- Subscription management UI

### ❌ Daily Horoscope Frontend — PARTIAL
- Basic horoscope page exists
- Needs: personalization (birth chart-based), push notifications, email digest

---

## Infrastructure Status

### ✅ Fully Live
- React frontend on Vercel: https://www.everydayhoroscope.in
- FastAPI backend on Render: https://everydayhoroscope-api.onrender.com
- Docker: `python:3.12.9-slim`
- pyswisseph 2.10.x as astronomy engine
- Supabase: Auth + DB
- Razorpay: credentials configured (payment flows not yet built)

### ⏳ Configured but not wired
- `pkg_resources` shim for Razorpay (setuptools fix committed)
- Keep-alive hook (useKeepAlive.js committed)

---

## Legal / Compliance Documents

All committed to repo (Word format):
- Terms of Service: `1__TERMS_OF_SERVICE.docx`
- Privacy Policy: `2__Privacy_Policy.docx`
- Subscription Terms: `3__SUBSCRIPTION_TERMS.docx`
- Refund & Cancellation: `4__Refund___Cancellation_Policy.docx`
- Cookie Policy: `5__Cookie_Policy.docx`

**Status: Drafted, not yet published on site**

---

## Architecture Documents (in repo)

- `vedic_engine_architecture.html` — Vedic engine design spec
- `blueprint_to_reality_map.html` — feature-to-code mapping
- `Top_10_Premium_Reports_Structure.txt` — premium report specs
- `EverydayHoroscope_Handover_March2026_v2.docx` — full handover doc

---

## Suggested Next Sprint Priorities

### Immediate (complete Panchang)
1. True Choghadiya (8 planetary slots) — backend + frontend
2. Amrit Kalam — backend addition only
3. OG image upload + GSC/GA4 wiring (manual)

### Next Module — Tarot (highest user engagement potential)
4. Tarot card flip UI + daily card feature
5. 3-card spread UI
6. Premium gating for Celtic Cross

### Then — Numerology
7. Numerology input form + tile display
8. Premium Ankjyotish report UI

### Then — Kundali
9. Birth chart form + wheel renderer
10. Kundali Milan (compatibility)

### Revenue unlock
11. Razorpay subscription flow
12. Premium report paywall

---

## How to Start a Claude Code Session

```bash
# 1. Navigate to your cloned repo
cd path/to/DailyHoroscope-Migration

# 2. Pull latest
git pull origin main

# 3. Start Claude Code
claude

# 4. First prompt (always):
"Read CLAUDE.md and PROJECT_STATUS.md, then run git log --oneline -10
so you know exactly where we are. Then ask me what to work on."
```

Claude Code will:
- Read CLAUDE.md → knows the full stack, file locations, conventions
- Read PROJECT_STATUS.md → knows what's done and what's next
- Check git log → sees the last 10 commits
- Be fully oriented in under 30 seconds, ready to code
