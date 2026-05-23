# SEO-20K · M3 Commission Brief
> Thread: SEO Codex Thread  
> Extends: `CODEX_COMMISSION_SEO_20K.md` (read that file first for full architecture context)  
> Batches: 4 · 8 · 10  
> Pages: ~990 (108 + 450 + 432)  
> Date: 2026-05-23  
> Status: READY TO BUILD

---

## Context

M1 (Batches 1+2) and M2 (Batches 3+9) are integrated and live. You confirmed M2 delivery; it is committed at `aba7d5c`. This brief commissions M3: the three remaining batches that do not require book-decode source material.

All routing patterns, sitemap architecture, GlassCard UI patterns, SEO component, and MongoDB connection are already established in the repo. Follow exactly the same patterns as M1 and M2 deliveries.

**Repo:** `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
**Stack:** React 18 · FastAPI · MongoDB · Tailwind CSS · pyswisseph  
**Astronomical engines:**
- `backend/vedic_calculator.py` -- birth chart, dasha, planetary positions. Do NOT add calculation logic to any other file.
- `backend/vedic_shared_utils.py` -- transit date helpers (sign ingress/exit). Batch 4 **must** use this file for transit dates (see Batch 4 section below). Do NOT duplicate these functions elsewhere.

---

## Batch 4 -- Transit Profiles

**URL pattern:** `/transits/{planet}-in-{sign}/`  
**Example:** `/transits/saturn-in-aquarius/`  
**Pages:** 9 planets × 12 signs = **108 pages**

**Planets:** Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu  
**Signs:** Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces

**Backend:** `GET /api/seo/transit/{planet}/{sign}` -- returns:
- Transit start/end dates for current occurrence -- use `vedic_shared_utils.dates_since_sign_entry()` and `vedic_shared_utils.dates_until_sign_exit()`
- Next occurrence date -- use `vedic_shared_utils.next_sign_ingress()`
- Current transit snapshot -- use `vedic_shared_utils.build_transit_snapshot()`
- Interpretation content (pre-seeded to MongoDB `transit_profiles` collection)

**⚠️ Transit date functions live in `backend/vedic_shared_utils.py` (lines 572-593), NOT in `vedic_calculator.py`.** Import from there directly:
```python
from vedic_shared_utils import (
    build_transit_snapshot,
    next_sign_ingress,
    dates_until_sign_exit,
    dates_since_sign_entry,
)
```

**Frontend:** `frontend/src/pages/seo/TransitProfilePage.jsx`

**Page content (each page):**
- H1: `{Planet} in {Sign} -- What It Means for You`
- Opening hook: 2-sentence punchy summary (Cinzel-adjacent heading, then Playfair body)
- **Transit dates:** Current/next occurrence with exact start/end dates
- **Key themes:** 5-7 bullet points -- what this transit activates (career, relationships, finances, health, spirituality)
- **For your sign:** Mini-grid -- how each of the 12 rising signs experiences this transit (compact table or 12 pills)
- **Watch for:** 3-4 bullet points -- challenges and cautions
- **Ritual & remedy:** 2-3 practical actions during this transit (mantras, gemstones, timing)
- **FAQ accordion:** 5 questions (How long does this last? Is it good or bad? What should I avoid? etc.)
- **CTA:** "Check if {Planet} is transiting your chart now" → links to `/birth-chart`
- JSON-LD: `Event` schema (transit dates) + `FAQPage`

**SEO metadata formula:**
- Title: `{Planet} in {Sign} {Year} -- Dates, Effects & Remedies | EverydayHoroscope`
- Description: `{Planet} transits {Sign} bringing [2-word theme]. Dates, effects on all 12 signs, and Vedic remedies. Check your personal impact.`

**MongoDB collection:** `transit_profiles` -- seed 108 documents at build time. Each document: `{ planet, sign, themes[], watch_for[], ritual, faq[], meta_title, meta_description }`. Content is original, written by Codex, inspired by Vedic transit principles -- not copied from any source.

---

## Batch 8 -- Festival Region Pages

**URL pattern:** `/festivals/{festivalSlug}/{region}/`  
**Example:** `/festivals/diwali/maharashtra/`  
**Pages:** ~20 festivals × ~25 Indian states + major diaspora regions = **~600 pages** (prioritise top 15 festivals × top 30 regions = 450 pages for this commission)

**Festivals to cover (top 15):** Diwali, Holi, Navratri, Durga Puja, Ganesh Chaturthi, Janmashtami, Makar Sankranti, Pongal, Onam, Baisakhi, Eid-ul-Fitr, Christmas, Gurupurab, Ram Navami, Hanuman Jayanti

**Regions (top 30):** All 28 Indian states + NRI London + NRI New York

**Festival date source -- two tiers (important):**

`panchang_router.py` only has built-in observance rules for **9 festivals**: Diwali, Holi, Janmashtami, Ram Navami, Maha Shivaratri, Ekadashi, Pradosh Vrat, Purnima, Amavasya. Dates for these are computed live from the engine.

The remaining 6 festivals -- Navratri, Durga Puja, Ganesh Chaturthi, Makar Sankranti, Pongal, Onam, Baisakhi, Eid-ul-Fitr, Christmas, Gurupurab, Hanuman Jayanti -- are **not** in the panchang engine. Dates for these must be **pre-seeded in MongoDB** for the current year + next 2 years, then refreshed annually. These festivals follow fixed or well-published calendar rules -- seed their dates as static data in the `festival_region_pages` collection.

**Date source per festival:**

| Festival | Date source |
|---|---|
| Diwali | `panchang_router.py` (Amavasya, month 7) -- live |
| Holi | `panchang_router.py` (Purnima, month 11) -- live |
| Janmashtami | `panchang_router.py` (Tithi 22, month 4) -- live |
| Ram Navami | `panchang_router.py` (Tithi 8, month 0) -- live |
| Maha Shivaratri | `panchang_router.py` (Tithi 28, month 10) -- live |
| Navratri | MongoDB pre-seeded (Ashwin Shukla Pratipada -- approx Oct) |
| Durga Puja | MongoDB pre-seeded (same window as Navratri) |
| Ganesh Chaturthi | MongoDB pre-seeded (Bhadrapada Shukla Chaturthi -- approx Aug/Sep) |
| Makar Sankranti | MongoDB pre-seeded (Jan 14 fixed) |
| Pongal | MongoDB pre-seeded (Jan 14-17 fixed) |
| Onam | MongoDB pre-seeded (Thiruvonam nakshatra -- approx Aug/Sep) |
| Baisakhi | MongoDB pre-seeded (Apr 13/14 fixed) |
| Eid-ul-Fitr | MongoDB pre-seeded (Islamic calendar -- published dates) |
| Christmas | MongoDB pre-seeded (Dec 25 fixed) |
| Gurupurab | MongoDB pre-seeded (Kartik Purnima -- approx Nov) |
| Hanuman Jayanti | MongoDB pre-seeded (Chaitra Purnima -- approx Apr) |

**Backend:** `GET /api/seo/festivals/{slug}/{region}` -- returns:
- Festival date for current year (engine for Tier 1; MongoDB for Tier 2)
- Region-specific customs, names, and variations
- Pre-seeded content from MongoDB `festival_region_pages` collection

**Frontend:** `frontend/src/pages/seo/FestivalRegionPage.jsx`

**Page content:**
- H1: `{Festival} in {Region} {Year} -- Date, Traditions & Celebrations`
- Festival date badge (prominent -- this is the #1 search intent)
- **Local traditions:** 4-6 bullet points specific to that region's customs
- **How it's celebrated:** Step-by-step short list (food, rituals, decorations, greetings)
- **Auspicious timing:** Muhurta for key rituals (pulled from panchang engine)
- **Regional name:** What the festival is called locally
- **Did you know:** 1 interesting regional fact
- **Related pages:** Link to nearby festivals + panchang for that date
- JSON-LD: `Event` schema with regional variant

**Note:** Region-specific customs are original Codex writing based on general cultural knowledge -- not copied from any single source. Each page must feel locally relevant, not generic.

---

## Batch 10 -- Character Placements

**URL pattern:** `/traits/{sign}/{chartPoint}/{house}/`  
**Example:** `/traits/scorpio/moon/7th-house/`  
**Pages:** 12 signs × 3 chart points × 12 houses = **432 pages**

**Chart points:** `sun`, `moon`, `rising`  
**Houses:** `1st-house` through `12th-house`

**Backend:** `GET /api/seo/traits/{sign}/{chartPoint}/{house}` -- returns pre-seeded content from MongoDB `character_placements` collection.

**Frontend:** `frontend/src/pages/seo/CharacterPlacementPage.jsx`

**Page content:**
- H1: `{Sign} {Chart Point} in the {Nth} House -- Personality & Life Themes`
- **Core traits:** 5-6 bullet points -- personality characteristics
- **Life areas activated:** Which domains of life this placement energises
- **Strengths:** 3-4 bullets
- **Shadow side:** 2-3 bullets (challenges to be aware of)
- **Famous people:** 2-3 examples (if verifiable)
- **Compatible placements:** What rising/moon signs harmonise well
- **Vedic perspective:** 2-3 sentences from classical interpretation
- **CTA:** "Find your chart placements" → `/birth-chart`
- JSON-LD: `FAQPage` + `Article`

---

## Technical Requirements (All Batches)

**Follow exactly the patterns from M1/M2:**
- New React pages in `frontend/src/pages/seo/`
- New FastAPI routers in `backend/` -- prefix `/api/seo/`
- Register routers in `backend/server.py`
- New routes in `frontend/src/App.js` (public, no auth gate)
- Sitemap endpoints added to `backend/seo_router.py`
- Cache headers in `frontend/vercel.json` (s-maxage=86400)
- MongoDB seed scripts for all pre-generated content collections
- `SEO` component from `frontend/src/components/SEO.jsx` on every page

**Tailwind / theme:** Use existing GlassCard pattern (`rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`). Gold accent `#c5a059`. No new dependencies.

**Build verification:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` -- must pass clean.

---

## Sitemap Additions

Add to `backend/seo_router.py`:
```python
GET /api/seo/sitemap/transits        # 108 URLs
GET /api/seo/sitemap/festivals       # 450 URLs  
GET /api/seo/sitemap/traits          # 432 URLs
```

Add all three to `frontend/public/sitemap-index.xml`.

---

## Acceptance Checklist

- [ ] 108 Transit Profile pages render with planet/sign data
- [ ] 450 Festival Region pages render with regional customs
- [ ] 432 Character Placement pages render with placement traits
- [ ] All 3 sitemap endpoints return correct URL counts
- [ ] Routes wired in App.js -- all pages HTTP 200
- [ ] Vercel cache headers applied to all 3 route groups
- [ ] MongoDB seed scripts provided for all 3 collections
- [ ] Build clean -- zero errors
- [ ] JSON-LD present on all page types
- [ ] SEO meta title/description formula applied
