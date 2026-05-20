# Commission Brief: SEO-C5 -- Marriage Muhurat Page

**Commission ID:** SEO-C5  
**Track:** C -- Codex Feature Builds  
**Priority:** Tier 2 -- Phase 4  
**Date:** 2026-05-20  
**Status:** READY TO ISSUE  

---

## What to Build

A public marriage muhurat page showing auspicious wedding dates for the current year.

| Route | What it shows |
|---|---|
| `/muhurat/marriage` | List of auspicious marriage dates for 2026, with Panchang details per date |

High-intent search traffic ("shubh vivah muhurat 2026", "marriage dates 2026"). Upsells to premium personalised consultation.

---

## Files to Create

### Frontend
- `frontend/src/pages/muhurat/MarriageMuhuratPage.jsx`

### Backend
Add one endpoint to `backend/panchang_router.py`. No new file.

---

## Route Wiring (App.js)

```jsx
import { MarriageMuhuratPage } from './pages/muhurat/MarriageMuhuratPage';

<Route path="/muhurat/marriage" element={<MarriageMuhuratPage />} />
```

---

## Backend

### New endpoint -- add to `panchang_router.py`

```
GET /api/panchang/muhurat/marriage?year=2026
```

Returns a list of auspicious marriage dates for the given year.

### Calculation logic

Marriage muhurat dates are determined by these Vedic criteria -- hardcode the logic using existing Panchang data:

**Auspicious Tithis for marriage:** 2 (Dwitiya), 3 (Tritiya), 5 (Panchami), 7 (Saptami), 10 (Dashami), 11 (Ekadashi), 13 (Trayodashi) -- Shukla Paksha only

**Auspicious Nakshatras for marriage:** Rohini, Mrigashira, Magha (after 1st Pada), Uttara Phalguni, Hasta, Swati, Anuradha, Mula (after 1st Pada), Uttara Ashadha, Uttara Bhadrapada, Revati

**Inauspicious months (no marriage):** Adhik Maas (leap month), Kharmas (Sun in Sagittarius or Pisces)

**Inauspicious periods:** Holashtak (8 days before Holi), Pitru Paksha (16 days of Shradh), 3 days after Ekadashi

**Algorithm:**
1. Iterate through all dates in the year
2. For each date, use existing `_day_indexes()` function to get Tithi + Nakshatra
3. Filter by auspicious Tithi (Shukla Paksha only) AND auspicious Nakshatra
4. Exclude inauspicious periods
5. Return sorted list of qualifying dates with their Tithi + Nakshatra

```python
@router.get("/panchang/muhurat/marriage")
async def get_marriage_muhurat(year: int = Query(default=2026)):
    """Returns auspicious marriage dates for the given year."""
    results = []
    # Use New Delhi as reference location (national standard)
    location = get_location_by_slug("new-delhi")
    start = date(year, 1, 1)
    end = date(year, 12, 31)
    current = start
    while current <= end:
        # Use existing _day_indexes() or daily Panchang computation
        # Check if date meets auspicious criteria
        # Append qualifying dates to results
        current += timedelta(days=1)
    return {"year": year, "muhurat_dates": results, "count": len(results)}
```

Each result object:
```json
{
  "date": "2026-02-14",
  "day_of_week": "Saturday",
  "tithi": "Panchami",
  "nakshatra": "Rohini",
  "quality": "Highly Auspicious",
  "notes": "Rohini Nakshatra -- especially favoured for marriage"
}
```

**⚠️ Use existing Panchang computation functions -- do NOT add new astronomical libraries.**

---

## UI Layout

```
[Page header: "Shubh Vivah Muhurat 2026"]
[Subtitle: "Auspicious Hindu marriage dates for 2026, according to Vedic Panchang"]

[Summary card -- GlassCard]
  ├── "X auspicious marriage dates found in 2026"
  └── Quick stats: most auspicious month, next upcoming date

[Month filter tabs]
  └── Jan | Feb | Mar | ... | Dec (tabs to filter the list)

[Date list -- one card per date]
  ├── Date (large) + Day of week
  ├── Tithi badge + Nakshatra badge
  ├── Quality indicator: ⭐⭐⭐ Highly Auspicious / ⭐⭐ Auspicious
  ├── Brief note (e.g. "Rohini Nakshatra -- Lord Brahma's favourite for marriage")
  └── "View full Panchang →" link → /panchang/date/{YYYY-MM-DD}

[What makes a date auspicious? -- info card]
  └── Brief explanation of Tithi + Nakshatra criteria

[FAQ accordion]
  ├── "How are marriage muhurat dates calculated?"
  ├── "Which Nakshatra is best for marriage?"
  ├── "Which months are inauspicious for marriage in 2026?"
  └── "Can I get a personalised muhurat for my birth chart?"

[Upsell CTA]
  ├── "Get a personalised marriage muhurat based on both partners' birth charts"
  ├── "Considers your Lagna, Dasha timing, and 7th house sub-lord"
  └── [Get Personalised Consultation] → /birth-chart (or /kundali-milan)
```

---

## SEO Requirements

- **Title:** `Shubh Vivah Muhurat 2026 -- Auspicious Hindu Marriage Dates | EverydayHoroscope`
- **Description:** `Complete list of auspicious Hindu marriage dates for 2026. Vedic Panchang-verified muhurat with Tithi, Nakshatra, and monthly breakdown for your wedding planning.`
- **JSON-LD:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Which are the auspicious marriage dates in 2026?",
      "acceptedAnswer": { "@type": "Answer", "text": "There are [X] auspicious Vivah Muhurat dates in 2026..." }
    }
  ]
}
```
- **FAQ schema required** -- "vivah muhurat 2026" queries dominate this niche and FAQ rich results significantly boost CTR

---

## Visual Spec

- Month tabs: gold underline on active tab, `text-gold` for active month
- Date cards: GlassCard with gold-left-border accent (`border-l-4 border-gold/60`)
- Tithi badge: `bg-gold/15 text-gold border border-gold/30`
- Nakshatra badge: `bg-indigo-500/15 text-indigo-400 border border-indigo-400/30`
- Quality stars: gold star icons (Lucide `Star` filled/unfilled)
- "Highly Auspicious" dates: card has stronger gold background `bg-gold/[0.08]`
- No custom CSS -- Tailwind only

---

## ⚠️ Critical Notes

1. **All data from `panchang_router.py`** -- use existing Panchang computation; no new astronomical libraries
2. **New Delhi as reference** -- marriage muhurat is computed for a standard reference location; note on the page that "Muhurat times may vary by 10-30 minutes depending on your city"
3. **Year param** -- default to current year; also accept `?year=2027` for next-year planning
4. **Performance** -- computing 365 days of Panchang will be slow if done naively. Cache the result in MongoDB with key `marriage_muhurat_{year}`. Compute once, serve from cache. Invalidate manually if needed.
5. **Smart quote fix** -- run on `MarriageMuhuratPage.jsx`
6. **Lazy load** -- component can be lazy-loaded

---

## Acceptance Criteria

- [ ] `/muhurat/marriage` loads with a list of dates for current year
- [ ] Dates are filtered by auspicious Tithi (Shukla Paksha) + Nakshatra criteria
- [ ] Month filter tabs work correctly
- [ ] Each date links to `/panchang/date/{date}`
- [ ] FAQ schema present
- [ ] Page title and meta description match spec
- [ ] No console errors
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
