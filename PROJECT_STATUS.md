# EverydayHoroscope — Project Status

> Last updated: 8 April 2026
> Based on 13 chat sessions + 50+ commits in `DailyHoroscope-Migration`

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
| Lumina (Spiritual Companion) | ✅ Live — 9-tab layout |
| Palmistry (Hasta Rekha) | ✅ Live — AI-powered, hand anatomy SVG |
| Careers Page | ✅ Live at /careers |
| SEO (OG tags, GA4, JSON-LD, GSC, Bing) | ✅ Live |
| Admin Console (subscribers, email, scheduler) | ✅ Live |
| Facebook Page posting | ✅ Live |
| WhatsApp notifications | 🔜 Pending Meta BSP setup |
| Instagram posting | 🔜 Pending IG Business Account ID |
| Ayur Jyotish (Longevity Report) | 📋 Spec drafted — Commission H |
| Jyotish Narrative Engine | 📋 Spec drafted — Commission I |
| Razorpay live keys | 🔜 Pending Play Store readiness |

---

## Module Status Detail

### ✅ Panchang Module — COMPLETE
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

### ✅ Tarot Module — COMPLETE
File: `frontend/src/pages/TarotPage.jsx`
Backend: `backend/tarot_router.py` + `frontend/public/tarot_cards.json`

Features live:
- 78-card SVG deck, flip animation
- Daily Draw, 3-card spread, Celtic Cross (premium-gated)
- Card detail modal (upright + reversed meaning)
- Reminder setup UI, History tab

### ✅ Numerology Module — COMPLETE
File: `frontend/src/pages/NumerologyPage.jsx`
Backend: `backend/numerology_router.py`

Features live:
- 11 computed number tiles (Life Path, Expression, Soul Urge, etc.)
- Lo Shu grid visualisation
- Premium Ankjyotish report (7-day remediation)
- 4 tabs: Select / Generate / Report / History

### ✅ Kundali / Birth Chart Module — COMPLETE
Files: `frontend/src/pages/BirthChartPage.jsx`, `BrihatKundliPage.jsx`, `KundaliMilanPage.jsx`
Backend: `backend/vedic_calculator.py`

Features live:
- Birth details form (date/time/place)
- D1 chart, planet positions, Navamsa, Dasha timeline
- Kundali Milan (compatibility matching)
- Brihat Kundli extended report

### ✅ Lumina Module — LIVE (Phase 1 complete, Phase 2 pending)
File: `frontend/src/pages/LuminaPage.jsx`

Features live:
- 9-tab layout (Home / Bible / Manifest / Marketplace / Spiritual / Devotion / Community / Journal / Chat)
- 4-pointed sparkle star logo
- GlassCard gold-tinted tiles (bg-gold/[0.04])
- Daily verse with hardcoded fallback (Joshua 1:8) — shows "OFFLINE — FEATURED" badge when API unavailable
- 21-day Manifestation Journal
- Devotion Points gamification: 750pt hero, streak/chapters/days stats, gold progress bar, 5 reward tiers (redeem UI)
- Marketplace Vision tab (Kingdom Vision / AI Blueprint)
- Community Hub placeholder tiles (Circle / Global Prayer Chain / Bridge)
- 6-item FAQ

**Phase 2 pending (Codex Commission A & beyond):**
- Full gold/illuminating theme pass — tiles need gradient glow, text auto-alignment
- Community Hub real backend (Circle, Prayer Chain, Bridge endpoints)
- TTS audio for 21-day manifestation
- AI wallpapers

### ✅ Palmistry Module (Hasta Rekha) — LIVE (Phase 1 complete, Phase 2 pending)
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

### ✅ Horoscope Pages — LIVE
Files: `DailyHoroscope.jsx`, `WeeklyHoroscope.jsx`, `MonthlyHoroscope.jsx`

Features live:
- Daily / Weekly / Monthly horoscope
- Element-based color theming (Fire/Earth/Air/Water)
- Share cards (WhatsApp/Facebook/Instagram/Save/Copy)

### ✅ Careers Page — LIVE
File: `frontend/src/pages/CareersPage.jsx`
Route: `/careers`

4 open roles:
- Frontend Engineer (React) — Product / Remote India
- Python Backend Engineer (FastAPI) — Engineering / Remote India
- Vedic Astrologer & Content Lead — Content / Remote Global
- Growth Marketer — SEO & Organic — Growth / Remote India

### ✅ Admin Console — LIVE
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

### Commission A — Lumina Gold Theme Pass 🔴 HIGH
- Full color audit of `LuminaPage.jsx`
- Replace any hardcoded greys/blacks with theme tokens (`text-foreground`, `text-muted-foreground`)
- Tiles: `bg-gradient-to-br from-gold/15 to-gold/5` for warm illuminating glow
- No new features — pure visual polish

### Commission B — Palm Anatomy Illustration 🔴 HIGH
- Produce `frontend/public/palm_anatomy.svg` — high-quality illustrated right hand (Tarot card line art style)
- Heart/Head/Life/Fate/Sun lines labeled with leader arrows
- 7 planetary mount ellipse zones labeled
- React component `HandIllustration` with `questionId` prop for per-line highlighting
- Replaces current programmatic SVG in `PalmistryPage.jsx`

### Commission C — AES-256 Encryption Layer 🟡 MEDIUM
- Add `cryptography` to `requirements.txt`
- Encrypt at write / decrypt at read for `palmistry_reports` + `lumina_prayers` MongoDB collections
- `ENCRYPTION_KEY` env var on Render (32-byte base64)
- Zero UI changes

### Commission D — Razorpay Subscription Paywall 🟡 MEDIUM
- Build upgrade flow in `PricingPage.jsx`
- Razorpay Checkout JS (test keys already in Render env)
- 3 plans: Free / Basic (₹199/mo) / Pro (₹499/mo)
- Report unlock blur overlay + "Unlock with Pro" CTA on Numerology, Kundali, Brihat reports
- Subscription management in `AccountSettings.jsx`

### Commission E — WhatsApp Notifications 🟢 WHEN READY
- Blocked on: `WHATSAPP_PHONE_NUMBER_ID` + `WHATSAPP_ACCESS_TOKEN` on Render
- Backend stub already in `admin_router.py`
- Frontend UI stub already in Admin Console Notifications tab

### Commission F — Instagram Posting 🟢 WHEN READY
- Blocked on: `INSTAGRAM_BUSINESS_ACCOUNT_ID`
- Facebook posting already working — Instagram is same Meta graph API pattern

### Commission H — Ayur Jyotish: Longevity & Health Report 🔴 HIGH
- **Full spec:** `.claude/CODEX_LONGEVITY_REPORT_CONTRACT.md`
- Premium report using KP Astrology (primary) + Vedic (supporting)
- New backend: `kp_engine.py` (sub-lord chain, Placidus cusps, KP significators)
- New backend: `longevity_router.py` (4 endpoints)
- 7-section report: Longevity Classification, Constitutional Profile, Vulnerable Systems, Disease Windows, Critical Alerts, Remedies, QoL Forecast
- Claude API narrative layer for human-readable report generation
- Frontend: `LongevityReportPage.jsx` — timeline visualisation, risk cards, remedy tabs
- Pro-tier paywall gated (₹499/mo or ₹999 one-time)
- Medical disclaimer mandatory on all views
- **Estimated:** ~48h

### Commission I — Jyotish Narrative Engine 🔴 HIGH
- **Full spec:** `.claude/CODEX_NARRATIVE_ENGINE_CONTRACT.md`
- Internal infrastructure module — powers interpretation across all modules
- 3-layer architecture: Data Layer (MongoDB rules DB) → Rule Engine (Python) → Narrative Layer (Claude API)
- Hierarchical Interpretation Database: 13 condition types, modifiers, conflict resolution, multi-source attribution
- ~200 seed rules from BPHS, Phaladeepika, Saravali
- 30-50 classical yoga detection library
- Admin Console: Rules Browser, Rule Editor, Bulk Import, Coverage Dashboard, Test Console
- Integration points: Kundali, Longevity, Horoscope, future Tarot/Numerology
- Phase 2 roadmap: OCR → Rule extraction pipeline, Redis caching, Celery workers
- **Estimated:** ~62h

### Commission E — WhatsApp Notifications 🟢 WHEN READY
- Blocked on: `WHATSAPP_PHONE_NUMBER_ID` + `WHATSAPP_ACCESS_TOKEN` on Render
- Backend stub already in `admin_router.py`
- Frontend UI stub already in Admin Console Notifications tab

### Commission F — Instagram Posting 🟢 WHEN READY
- Blocked on: `INSTAGRAM_BUSINESS_ACCOUNT_ID`
- Facebook posting already working — Instagram is same Meta graph API pattern

---

## Strategic Modules — Architecture Notes

### Recommended Build Order: I → H
**Commission I (Narrative Engine) should be built first.** It is the interpretation backbone
that Commission H (Longevity Report) will call for health-category narratives. Building I
first means H gets richer, multi-source narratives for free instead of hardcoded text.

### How They Connect
```
Commission I (Narrative Engine)         Commission H (Longevity Report)
┌─────────────────────────┐            ┌─────────────────────────┐
│ interpretation_rules DB │◄───────────│ kp_engine.py computes   │
│ scan_chart(categories=  │            │ sub-lords, significators│
│   ["health"])           │            │ longevity classification│
│ generate_narrative()    │───────────►│ narrative sections 1-7  │
└─────────────────────────┘            └─────────────────────────┘
```

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

All drafted (Word format in repo root):
- `1__TERMS_OF_SERVICE.docx`
- `2__Privacy_Policy.docx`
- `3__SUBSCRIPTION_TERMS.docx`
- `4__Refund___Cancellation_Policy.docx`
- `5__Cookie_Policy.docx`

**Status: Drafted — not yet rendered as pages on site** (pending Commission)

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
