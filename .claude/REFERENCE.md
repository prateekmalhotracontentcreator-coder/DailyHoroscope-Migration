# REFERENCE.md -- Full Detail Archive
> Read only when needed. NOT auto-loaded at session start.
> Extracted from CLAUDE.md 2026-05-09 to reduce session token baseline.

---

## Panchang Engine Detail

**What it computes:** Sunrise/Sunset/Moonrise/Moonset (with seconds), Tithi, Nakshatra, Yoga, Karana, Paksha, Lunar month, Samvat, Sun/Moon signs, Amrit Kalam, Special Yogas (Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga), True Choghadiya (8 daylight + 8 night slots).

**Timing windows:** Brahma Muhurta (96 min pre-sunrise) | Amrit Kalam | Rahu Kaal | Yamaganda | Gulika Kaal | Dur Muhurta ×2 | Abhijit Muhurta | Vijaya Muhurta

**Accuracy benchmark (New Delhi, 26 Mar 2026):** Sunrise 06:18 ✅ | Tithi Shukla Ashtami ✅ | Nakshatra Ardra ✅ | Yoga Shobhana ✅ | Rahu Kaal 01:58 PM ✅ | Abhijit 12:02 PM ✅ | Moonrise 11:59 AM ✅

---

## Frontend Pages Detail

- **PanchangPage.jsx** -- 6-tab sub-nav (Today/Tomorrow/Tithi/Choghadiya/Calendar/Festivals), 318-city picker with TZ badge, Five Limbs card, Timing Windows, Special Yogas, Share card, Facebook post
- **TarotPage.jsx** -- 3 tabs (Daily Draw/Spreads/History), flipping animation, 78-card SVG deck
- **NumerologyPage.jsx** -- 10 report types, computed numbers grid, remedy notes
- **BirthChartPage.jsx + BrihatKundliPage.jsx** -- Full Kundali UI, backend: vedic_calculator.py
- **Horoscope Pages (Daily/Weekly/Monthly)** -- Share cards, element-based theming, Facebook post
- **Admin Console (/admin/dashboard)** -- Overview/System/Users/Reports/Payments/Messages/Blog/Notifications tabs. Notifications: Subscribers / Compose / Scheduled / History / Social Media

---

## Share Cards (ShareCard.jsx)

**PanchangShareCard:** 900px, offscreen render (left: -9999px), gold header, Sun/Moon 4-col row, Five Limbs 3×2, Auspicious/Inauspicious timing tables, Special Yoga badge, footer.

**HoroscopeShareCard:** 900px, sign symbol in element-colored circle, sign name/dates/element/type badge, overview (first 2 sentences), lucky elements, footer.

**ShareButtons:** WhatsApp / Facebook / X / Instagram / YouTube / Save Card / Copy Link. Mobile: Web Share API. Desktop: canvas.toDataURL(). iOS: canvas.toBlob() → window.open(). html2canvas with onclone (no flash).

---

## YouTube Integration

OAuth: Google Cloud → refresh token in MongoDB `app_settings.youtube_refresh_token`.
Pipeline: PNG → ffmpeg (`-preset veryfast -threads 1 -crf 18 -tune stillimage`, 30s) → MP4 → YouTube Data API v3 resumable upload.
BackgroundTasks (async, ~2-4 min). Check: studio.youtube.com → Content.
Routes: `/api/admin/youtube/status|auth-url|callback|disconnect`

---

## WhatsApp Integration

Meta Cloud API v22.0. Template: `everydayhoroscope_update` with `{{customer_name}}` + `{{update_content}}`.
Phone `+91 96431 10001` (ID: `1062698816928895`) -- **PENDING**: complete OTP in WhatsApp Manager + add payment method.
WABA ID: `754513054261096`. Token: must be WhatsApp-specific (not FB System User token).

---

## Meta / Social Credentials

| Credential | Value |
|---|---|
| Meta App ID | 1594770155009283 |
| Business Manager ID | 878532341248169 |
| Facebook Page ID | 1084672598054073 |
| FB System User | EverydayHoroscope Bot (never-expires token) |
| YouTube | OAuth connected via Admin Console |
| WhatsApp Phone ID | 1062698816928895 -- Pending |
| WhatsApp WABA ID | 754513054261096 |
| Instagram Business ID | Pending (Meta dashboard loading issue) |

---

## Codex Workflow

1. Claude Code drafts commission brief
2. Prateek submits to Codex → receives code
3. Prateek pastes output here
4. Claude Code: aligns theme, wires Router + server.py, fixes quotes, verifies build, commits

**Smart quote fix:**
```bash
node -e "
let f=require('fs'),p='frontend/src/pages/TargetFile.jsx';
let c=f.readFileSync(p,'utf8');
c=c.replace(/"/g,'\"').replace(/"/g,'\"')
   .replace(/'/g,\"'\").replace(/'/g,\"'\");
f.writeFileSync(p,c);console.log('Done');"
```

Build verify: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`

---

## Architecture Rule -- Commission Brief Checklist

Before ANY Codex brief:
1. Verify item exists in CPath-1 (CONTRACT.md §21)
2. Confirm exact item number and phase
3. Confirm dependencies complete
4. Read locked spec in CONTRACT.md (TD-xx)
5. Read docx mockup if exists (`.claude/` folder)
6. State: "All dasha/astronomical data from `vedic_calculator.py`"
7. State: "Do NOT add dasha functions to `knowledge_engine.py`"

---

## Completed Features (as of 2026-05-09)

Panchang ✅ | Choghadiya ✅ | Amrit Kalam ✅ | Special Yogas ✅ | Panchang share card ✅ | Horoscope share cards ✅ | Share download (desktop+mobile+iOS) ✅ | Facebook posting ✅ | YouTube posting ✅ | Tarot ✅ | Numerology ✅ | Kundali ✅ | Razorpay ✅ | SEO/GA4 ✅ | GSC ✅ | Bing ✅ | Admin Console full ✅ | Email (Resend) ✅ | Scheduled notifications ✅ | Social Media tab ✅

## Pending

WhatsApp 🔜 (OTP) | Instagram 🔜 (Account ID) | Scheduled social auto-post 🔜 | Razorpay live keys 🔜

---

## Local Dev

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn server:app --reload --port 8000

# Frontend
cd frontend && npm install && npm start
# .env.local: REACT_APP_BACKEND_URL=http://localhost:8000
```
