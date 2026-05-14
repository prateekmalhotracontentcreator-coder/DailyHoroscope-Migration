# EverydayHoroscope -- Project Status

> Last updated: 14 May 2026

> **KE Sprint 2 (arbitration runtime) -- pending brief submission. Ingest freeze in effect.**

---

## TL;DR

| Layer | Status |
|---|---|
| Infrastructure (Vercel + Render + Docker) | ✅ Live |
| Panchang Module (full) | ✅ Live & verified |
| Vedic Calculator backend | ✅ Live |
| Tarot backend (78 cards + reminders) | ✅ Live |
| Numerology backend (Ankjyotish premium) | ✅ Live |
| Tarot frontend UI | ✅ Live |
| Numerology frontend UI | ✅ Live |
| Kundali / Birth Chart UI | ✅ Live (BirthChartPage + BrihatKundliPage) |
| Razorpay subscription / paywall | ✅ Test keys active |
| Lumina (Spiritual Companion) | ✅ Live -- 9-tab layout |
| Palmistry (Hasta Rekha) | ✅ Live -- AI-powered, hand anatomy SVG |
| Careers Page | ✅ Live at /careers |
| SEO (OG tags, GA4, JSON-LD, GSC, Bing) | ✅ Live |
| Admin Console (subscribers, email, scheduler) | ✅ Live |
| Facebook Page posting | ✅ Live |
| WhatsApp notifications | 🔜 Pending Meta BSP setup |
| Instagram posting | 🔜 Pending IG Business Account ID |
| Razorpay live keys | 🔜 Pending Play Store readiness |

---

## Module Status Detail

### ✅ Panchang Module -- COMPLETE
File: `frontend/src/pages/PanchangPage.jsx`
Engine: `backend/panchang_router.py` (v8-swiss)

All features live:
- 5 Panchang limbs, 8 timing windows, Sunrise/Moonrise with seconds
- True Choghadiya (8 daylight + 8 night slots, planetary rulers)
- Amrit Kalam, Special Yogas (Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga)
- 91 city catalogue, TZ-aware location picker
- Monthly calendar, Festivals & Vrats
- Panchang share card (WhatsApp/Facebook/Instagram/Save/Copy)
- Full SEO + JSON-LD on all 7 routes

### ✅ Tarot Module -- COMPLETE
File: `frontend/src/pages/TarotPage.jsx`
Backend: `backend/tarot_router.py` + `frontend/public/tarot_cards.json`

Features live:
- 78-card SVG deck, flip animation
- Daily Draw, 3-card spread, Celtic Cross (premium-gated)
- Card detail modal (upright + reversed meaning)
- Reminder setup UI, History tab

### ✅ Numerology Module -- COMPLETE
File: `frontend/src/pages/NumerologyPage.jsx`
Backend: `backend/numerology_router.py`

Features live:
- 11 computed number tiles (Life Path, Expression, Soul Urge, etc.)
- Lo Shu grid visualisation
- Premium Ankjyotish report (7-day remediation)
- 4 tabs: Select / Generate / Report / History

### ✅ Kundali / Birth Chart Module -- COMPLETE
Files: `frontend/src/pages/BirthChartPage.jsx`, `BrihatKundliPage.jsx`, `KundaliMilanPage.jsx`
Backend: `backend/vedic_calculator.py`

Features live:
- Birth details form (date/time/place)
- D1 chart, planet positions, Navamsa, Dasha timeline
- Kundali Milan (compatibility matching)
- Brihat Kundli extended report

### ✅ Lumina Module -- LIVE (Phase 1 complete, Phase 2 pending)
File: `frontend/src/pages/LuminaPage.jsx`

Features live:
- 9-tab layout (Home / Bible / Manifest / Marketplace / Spiritual / Devotion / Community / Journal / Chat)
- 4-pointed sparkle star logo
- GlassCard gold-tinted tiles (bg-gold/[0.04])
- Daily verse with hardcoded fallback (Joshua 1:8) -- shows "OFFLINE -- FEATURED" badge when API unavailable
- 21-day Manifestation Journal
- Devotion Points gamification: 750pt hero, streak/chapters/days stats, gold progress bar, 5 reward tiers (redeem UI)
- Marketplace Vision tab (Kingdom Vision / AI Blueprint)
- Community Hub placeholder tiles (Circle / Global Prayer Chain / Bridge)
- 6-item FAQ

**Phase 2 pending (Codex Commission A & beyond):**
- Full gold/illuminating theme pass -- tiles need gradient glow, text auto-alignment
- Community Hub real backend (Circle, Prayer Chain, Bridge endpoints)
- TTS audio for 21-day manifestation
- AI wallpapers

### ✅ Palmistry Module (Hasta Rekha) -- LIVE (Phase 1 complete, Phase 2 pending)
File: `frontend/src/pages/PalmistryPage.jsx`

Features live:
- AI-powered palm reading (multi-question flow)
- Comprehensive anatomical hand SVG (HandIllustration component)
  - Right hand palm-up: Heart/Head/Life/Fate/Sun lines
  - 7 planetary mounts labeled
  - Per-question highlighting (highlighted line = red, non-highlighted = dimmed)
  - Renders for: life_line, heart_line, head_line, fate_line, dominant_mount, thumb_type, finger_style, hand_texture, special_marks
- Hasta Rekha card on Home.jsx

**Phase 2 pending (Codex Commission B):**
- High-quality illustrated palm SVG as static asset (`frontend/public/palm_anatomy.svg`)
- Palm photo upload + Claude Vision analysis (process-and-discard pattern)
- AES-256 encryption for stored reports

### ✅ Horoscope Pages -- LIVE
Files: `DailyHoroscope.jsx`, `WeeklyHoroscope.jsx`, `MonthlyHoroscope.jsx`

Features live:
- Daily / Weekly / Monthly horoscope
- Element-based color theming (Fire/Earth/Air/Water)
- Share cards (WhatsApp/Facebook/Instagram/Save/Copy)

### ✅ Careers Page -- LIVE
File: `frontend/src/pages/CareersPage.jsx`
Route: `/careers`

4 open roles:
- Frontend Engineer (React) -- Product / Remote India
- Python Backend Engineer (FastAPI) -- Engineering / Remote India
- Vedic Astrologer & Content Lead -- Content / Remote Global
- Growth Marketer -- SEO & Organic -- Growth / Remote India

### ✅ Admin Console -- LIVE
Route: `/admin/dashboard`

Features live:
- Subscriber management (add/edit/delete, tags, MongoDB: `subscribers`)
- Email notifications via Resend
- Scheduled notifications (APScheduler, MongoDB: `scheduled_notifications`)
- Notification history log (MongoDB: `notification_logs`)
- Social Media tab: Facebook Page posting (one-click from Panchang + Horoscope pages + Admin Console)

---

## Codex Commission Queue

> These are the next development commissions to be issued to Codex, in priority order.

### Commission A -- Lumina Gold Theme Pass 🔴 HIGH
- Full color audit of `LuminaPage.jsx`
- Replace any hardcoded greys/blacks with theme tokens (`text-foreground`, `text-muted-foreground`)
- Tiles: `bg-gradient-to-br from-gold/15 to-gold/5` for warm illuminating glow
- No new features -- pure visual polish

### Commission B -- Palm Anatomy Illustration 🔴 HIGH
- Produce `frontend/public/palm_anatomy.svg` -- high-quality illustrated right hand (Tarot card line art style)
- Heart/Head/Life/Fate/Sun lines labeled with leader arrows
- 7 planetary mount ellipse zones labeled
- React component `HandIllustration` with `questionId` prop for per-line highlighting
- Replaces current programmatic SVG in `PalmistryPage.jsx`

### Commission C -- AES-256 Encryption Layer 🟡 MEDIUM
- Add `cryptography` to `requirements.txt`
- Encrypt at write / decrypt at read for `palmistry_reports` + `lumina_prayers` MongoDB collections
- `ENCRYPTION_KEY` env var on Render (32-byte base64)
- Zero UI changes

### Commission D -- Razorpay Subscription Paywall 🟡 MEDIUM
- Build upgrade flow in `PricingPage.jsx`
- Razorpay Checkout JS (test keys already in Render env)
- 3 plans: Free / Basic (₹199/mo) / Pro (₹499/mo)
- Report unlock blur overlay + "Unlock with Pro" CTA on Numerology, Kundali, Brihat reports
- Subscription management in `AccountSettings.jsx`

### Commission E -- WhatsApp Notifications 🟢 WHEN READY
- Blocked on: `WHATSAPP_PHONE_NUMBER_ID` + `WHATSAPP_ACCESS_TOKEN` on Render
- Backend stub already in `admin_router.py`
- Frontend UI stub already in Admin Console Notifications tab

### Commission F -- Instagram Posting 🟢 WHEN READY
- Blocked on: `INSTAGRAM_BUSINESS_ACCOUNT_ID`
- Facebook posting already working -- Instagram is same Meta graph API pattern

### Commission G -- 2 New Strategic Modules 🔴 HIGH (details TBD)
- User to brief in next session
- Full backend router spec + frontend page spec to be drafted

---

## 2 New Strategic Modules

> **To be briefed by Prateek in the next Claude Code session.**
> Codex commission briefs will be drafted once concepts are shared.

---

## Infrastructure Status

### ✅ Fully Live
- React frontend on Vercel: https://www.everydayhoroscope.in
- FastAPI backend on Render: https://everydayhoroscope-api.onrender.com
- Docker: `python:3.12.9-slim`
- pyswisseph 2.10.x as astronomy engine
- Supabase: Auth + DB
- Razorpay: test keys configured

### ✅ Social / Meta
- Facebook Page ID: `1084672598054073` ✅
- Facebook Page Access Token: System User token (never expires) ✅
- Instagram Business Account ID: 🔜 pending
- WhatsApp Phone Number ID: 🔜 pending BSP setup

---

## Manual Steps Pending

| Step | Notes |
|---|---|
| GSC sitemap submission | Submit `sitemap.xml` in Google Search Console dashboard |
| OG image | Upload 1200×630px image to `frontend/public/og-image.png` |
| Razorpay live keys | Upload only when ready for Play Store |
| Instagram Business Account ID | Resolve IG loading issue in Meta Business Manager |
| WhatsApp BSP setup | Select Business Service Provider, obtain Phone Number ID |

---

## Legal / Compliance Documents

Routes live: `/terms` `/privacy` `/subscription-terms` `/refund-policy` `/cookie-policy`
Footer "Legal" column links all 5 pages.
Backend: `GET /api/policies/{type}` serves from `horoscope_db.policies` collection.

**Status: Pages live and indexed (noindex removed). MongoDB seed required.**
Run: `python3 backend/scripts/seed_policies_v1.py --mongo-url "$MONGO_URL" --db-name horoscope_db`

---

## How to Start a Claude Code Session

```bash
# 1. Navigate to repo
cd /Users/apple/DailyHoroscope-Migration

# 2. Pull latest
git pull origin main

# 3. Start Claude Code
claude

# 4. First prompt (always):
"Read CLAUDE.md and PROJECT_STATUS.md, then run git log --oneline -10
so you know exactly where we are. Then ask me what to work on."
```

Claude Code will orient in under 30 seconds, ready to code.
