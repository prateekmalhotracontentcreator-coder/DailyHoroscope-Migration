# Google Search Console -- URL Registration Document
> EverydayHoroscope · Generated: 2026-05-26
> Use this document to manually register new URL groups in GSC (Sitemaps tab + URL Inspection).
> Submit the sitemap-index first, then use URL Inspection for spot-checking priority pages.

---

## Step 1 -- Submit Sitemap Index (covers everything below automatically)

**GSC → Sitemaps → Add sitemap:**
```
https://www.everydayhoroscope.in/sitemap-index.xml
```

This single file references all sub-sitemaps below. Once submitted, GSC will crawl all groups.

---

## Step 2 -- Individual Sitemap URLs (for direct submission / monitoring)

| Sitemap URL | Page Count | Module |
|---|---|---|
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/panchang` | ~2,226 | Panchang (318 cities × 7 days) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/choghadiya` | ~1,272 | Choghadiya (318 cities × 4 periods) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/horoscope` | 36 | Daily/Weekly/Monthly (12 signs × 3) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/compatibility` | 144 | Sign Compatibility pairs |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/remedies` | 12 | Dosha Remedy pages |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/transits` | 78 | Planet-in-Sign transit pages |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/festivals` | 480 | Festival × Region pages |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/traits` | 432 | Character Placement pages |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/crystals` | 72 | Crystal Healing pages |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/lo-shu-grid` | ~20 | Lo Shu Grid pages |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/rudraksha` | 23 | Rudraksha pages |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/zibu` | 89 | Zibu Symbols pages |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=1` | 1,000 | Angel Numbers (page 1) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=2` | 1,000 | Angel Numbers (page 2) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=3` | 1,000 | Angel Numbers (page 3) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=4` | 1,000 | Angel Numbers (page 4) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=5` | 1,000 | Angel Numbers (page 5) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=6` | 1,000 | Angel Numbers (page 6) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=7` | 1,000 | Angel Numbers (page 7) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=8` | 1,000 | Angel Numbers (page 8) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=9` | 1,000 | Angel Numbers (page 9) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=10` | 1,000 | Angel Numbers (page 10) |
| `https://everydayhoroscope-api.onrender.com/api/seo/sitemap/angel-numbers?page=11` | 1 | Angel Numbers (page 11 -- hub only) |

---

## Step 3 -- Priority Pages for URL Inspection (spot-check these first)

Use **GSC → URL Inspection → Request Indexing** on these high-value pages:

### Crystal Healing
```
https://www.everydayhoroscope.in/crystals
https://www.everydayhoroscope.in/crystals/amethyst
https://www.everydayhoroscope.in/crystals/ruby
https://www.everydayhoroscope.in/crystals/for/love-relationships
https://www.everydayhoroscope.in/crystals/for/protection
https://www.everydayhoroscope.in/crystals/calculator
```

### Rudraksha
```
https://www.everydayhoroscope.in/rudraksha
https://www.everydayhoroscope.in/rudraksha/1-mukhi
https://www.everydayhoroscope.in/rudraksha/5-mukhi
https://www.everydayhoroscope.in/rudraksha/14-mukhi
https://www.everydayhoroscope.in/rudraksha/calculator
```

### Lo Shu Grid
```
https://www.everydayhoroscope.in/lo-shu-grid
https://www.everydayhoroscope.in/lo-shu-grid/calculator
https://www.everydayhoroscope.in/lo-shu-grid/missing-5
https://www.everydayhoroscope.in/lo-shu-grid/arrow/action
```

### Zibu Symbols
```
https://www.everydayhoroscope.in/zibu
https://www.everydayhoroscope.in/zibu/abundance
https://www.everydayhoroscope.in/zibu/gratitude
```

### Angel Numbers
```
https://www.everydayhoroscope.in/angel-numbers
https://www.everydayhoroscope.in/angel-numbers/111
https://www.everydayhoroscope.in/angel-numbers/222
https://www.everydayhoroscope.in/angel-numbers/444
https://www.everydayhoroscope.in/angel-numbers/1111
https://www.everydayhoroscope.in/angel-numbers/111/love
https://www.everydayhoroscope.in/angel-numbers/111/twin-flame
https://www.everydayhoroscope.in/angel-numbers/444/career
```

### SEO Programmatic Pages (M1-M3)
```
https://www.everydayhoroscope.in/transits/jupiter-in-aries
https://www.everydayhoroscope.in/transits/saturn-in-capricorn
https://www.everydayhoroscope.in/festivals/diwali/delhi
https://www.everydayhoroscope.in/festivals/holi/mumbai
https://www.everydayhoroscope.in/traits/aries/sun/first-house
https://www.everydayhoroscope.in/traits/scorpio/moon/eighth-house
```

---

## Step 4 -- Full URL Lists by Module

### Crystal Healing -- 72 pages

**Hub + Calculator (2):**
```
https://www.everydayhoroscope.in/crystals
https://www.everydayhoroscope.in/crystals/calculator
```

**50 Crystal pages:**
```
https://www.everydayhoroscope.in/crystals/ruby
https://www.everydayhoroscope.in/crystals/pearl
https://www.everydayhoroscope.in/crystals/red-coral
https://www.everydayhoroscope.in/crystals/emerald
https://www.everydayhoroscope.in/crystals/yellow-sapphire
https://www.everydayhoroscope.in/crystals/diamond
https://www.everydayhoroscope.in/crystals/blue-sapphire
https://www.everydayhoroscope.in/crystals/hessonite-garnet
https://www.everydayhoroscope.in/crystals/cats-eye
https://www.everydayhoroscope.in/crystals/amethyst
https://www.everydayhoroscope.in/crystals/rose-quartz
https://www.everydayhoroscope.in/crystals/clear-quartz
https://www.everydayhoroscope.in/crystals/black-tourmaline
https://www.everydayhoroscope.in/crystals/citrine
https://www.everydayhoroscope.in/crystals/lapis-lazuli
https://www.everydayhoroscope.in/crystals/obsidian
https://www.everydayhoroscope.in/crystals/selenite
https://www.everydayhoroscope.in/crystals/malachite
https://www.everydayhoroscope.in/crystals/carnelian
https://www.everydayhoroscope.in/crystals/moonstone
https://www.everydayhoroscope.in/crystals/labradorite
https://www.everydayhoroscope.in/crystals/pyrite
https://www.everydayhoroscope.in/crystals/amazonite
https://www.everydayhoroscope.in/crystals/sodalite
https://www.everydayhoroscope.in/crystals/aventurine
https://www.everydayhoroscope.in/crystals/tigers-eye
https://www.everydayhoroscope.in/crystals/jade
https://www.everydayhoroscope.in/crystals/hematite
https://www.everydayhoroscope.in/crystals/lepidolite
https://www.everydayhoroscope.in/crystals/rhodonite
https://www.everydayhoroscope.in/crystals/fluorite
https://www.everydayhoroscope.in/crystals/aquamarine
https://www.everydayhoroscope.in/crystals/chrysocolla
https://www.everydayhoroscope.in/crystals/sunstone
https://www.everydayhoroscope.in/crystals/bloodstone
https://www.everydayhoroscope.in/crystals/turquoise
https://www.everydayhoroscope.in/crystals/garnet
https://www.everydayhoroscope.in/crystals/onyx
https://www.everydayhoroscope.in/crystals/shungite
https://www.everydayhoroscope.in/crystals/rhodochrosite
https://www.everydayhoroscope.in/crystals/prehnite
https://www.everydayhoroscope.in/crystals/calcite
https://www.everydayhoroscope.in/crystals/apatite
https://www.everydayhoroscope.in/crystals/angelite
https://www.everydayhoroscope.in/crystals/celestite
https://www.everydayhoroscope.in/crystals/kunzite
https://www.everydayhoroscope.in/crystals/kyanite
https://www.everydayhoroscope.in/crystals/larimar
https://www.everydayhoroscope.in/crystals/moldavite
https://www.everydayhoroscope.in/crystals/nuummite
```

**20 Intention pages:**
```
https://www.everydayhoroscope.in/crystals/for/love-relationships
https://www.everydayhoroscope.in/crystals/for/anxiety-stress
https://www.everydayhoroscope.in/crystals/for/protection
https://www.everydayhoroscope.in/crystals/for/abundance-money
https://www.everydayhoroscope.in/crystals/for/clarity-focus
https://www.everydayhoroscope.in/crystals/for/confidence
https://www.everydayhoroscope.in/crystals/for/sleep
https://www.everydayhoroscope.in/crystals/for/grief-healing
https://www.everydayhoroscope.in/crystals/for/spiritual-growth
https://www.everydayhoroscope.in/crystals/for/intuition
https://www.everydayhoroscope.in/crystals/for/creativity
https://www.everydayhoroscope.in/crystals/for/communication
https://www.everydayhoroscope.in/crystals/for/anger-release
https://www.everydayhoroscope.in/crystals/for/trauma-healing
https://www.everydayhoroscope.in/crystals/for/decision-making
https://www.everydayhoroscope.in/crystals/for/chakra-balancing
https://www.everydayhoroscope.in/crystals/for/new-beginnings
https://www.everydayhoroscope.in/crystals/for/fertility
https://www.everydayhoroscope.in/crystals/for/past-life
https://www.everydayhoroscope.in/crystals/for/travel-safety
```

---

### Rudraksha -- 23 pages
```
https://www.everydayhoroscope.in/rudraksha
https://www.everydayhoroscope.in/rudraksha/calculator
https://www.everydayhoroscope.in/rudraksha/1-mukhi
https://www.everydayhoroscope.in/rudraksha/2-mukhi
https://www.everydayhoroscope.in/rudraksha/3-mukhi
https://www.everydayhoroscope.in/rudraksha/4-mukhi
https://www.everydayhoroscope.in/rudraksha/5-mukhi
https://www.everydayhoroscope.in/rudraksha/6-mukhi
https://www.everydayhoroscope.in/rudraksha/7-mukhi
https://www.everydayhoroscope.in/rudraksha/8-mukhi
https://www.everydayhoroscope.in/rudraksha/9-mukhi
https://www.everydayhoroscope.in/rudraksha/10-mukhi
https://www.everydayhoroscope.in/rudraksha/11-mukhi
https://www.everydayhoroscope.in/rudraksha/12-mukhi
https://www.everydayhoroscope.in/rudraksha/13-mukhi
https://www.everydayhoroscope.in/rudraksha/14-mukhi
https://www.everydayhoroscope.in/rudraksha/15-mukhi
https://www.everydayhoroscope.in/rudraksha/16-mukhi
https://www.everydayhoroscope.in/rudraksha/17-mukhi
https://www.everydayhoroscope.in/rudraksha/18-mukhi
https://www.everydayhoroscope.in/rudraksha/19-mukhi
https://www.everydayhoroscope.in/rudraksha/20-mukhi
https://www.everydayhoroscope.in/rudraksha/21-mukhi
```

---

### Lo Shu Grid -- 20 pages
```
https://www.everydayhoroscope.in/lo-shu-grid
https://www.everydayhoroscope.in/lo-shu-grid/calculator
https://www.everydayhoroscope.in/lo-shu-grid/missing-1
https://www.everydayhoroscope.in/lo-shu-grid/missing-2
https://www.everydayhoroscope.in/lo-shu-grid/missing-3
https://www.everydayhoroscope.in/lo-shu-grid/missing-4
https://www.everydayhoroscope.in/lo-shu-grid/missing-5
https://www.everydayhoroscope.in/lo-shu-grid/missing-6
https://www.everydayhoroscope.in/lo-shu-grid/missing-7
https://www.everydayhoroscope.in/lo-shu-grid/missing-8
https://www.everydayhoroscope.in/lo-shu-grid/missing-9
https://www.everydayhoroscope.in/lo-shu-grid/arrow/determination
https://www.everydayhoroscope.in/lo-shu-grid/arrow/intellect
https://www.everydayhoroscope.in/lo-shu-grid/arrow/spirituality
https://www.everydayhoroscope.in/lo-shu-grid/arrow/activity
https://www.everydayhoroscope.in/lo-shu-grid/arrow/practicality
https://www.everydayhoroscope.in/lo-shu-grid/arrow/action
https://www.everydayhoroscope.in/lo-shu-grid/arrow/compassion
https://www.everydayhoroscope.in/lo-shu-grid/arrow/sensitivity
```
*(Confirm arrow slugs match those defined in `lo_shu_router.py`)*

---

### Zibu Symbols -- 89 pages
```
https://www.everydayhoroscope.in/zibu
```
*(88 symbol slug URLs -- retrieve full list from: `https://everydayhoroscope-api.onrender.com/api/seo/zibu/symbols` after deploy)*

---

### Angel Numbers -- 10,001 pages
Use the paginated sitemaps directly for GSC submission.
For manual URL inspection, priority numbers:
```
https://www.everydayhoroscope.in/angel-numbers
https://www.everydayhoroscope.in/angel-numbers/111
https://www.everydayhoroscope.in/angel-numbers/222
https://www.everydayhoroscope.in/angel-numbers/333
https://www.everydayhoroscope.in/angel-numbers/444
https://www.everydayhoroscope.in/angel-numbers/555
https://www.everydayhoroscope.in/angel-numbers/666
https://www.everydayhoroscope.in/angel-numbers/777
https://www.everydayhoroscope.in/angel-numbers/888
https://www.everydayhoroscope.in/angel-numbers/999
https://www.everydayhoroscope.in/angel-numbers/1111
https://www.everydayhoroscope.in/angel-numbers/1212
https://www.everydayhoroscope.in/angel-numbers/2222
https://www.everydayhoroscope.in/angel-numbers/4444
https://www.everydayhoroscope.in/angel-numbers/111/love
https://www.everydayhoroscope.in/angel-numbers/111/career
https://www.everydayhoroscope.in/angel-numbers/111/twin-flame
https://www.everydayhoroscope.in/angel-numbers/1111/manifestation
https://www.everydayhoroscope.in/angel-numbers/444/protection
```

---

### SEO-20K M1 -- Transit Pages (78)
Pattern: `https://www.everydayhoroscope.in/transits/{planet}-in-{sign}`

Planets: sun, moon, mercury, venus, mars, jupiter, saturn (7)
Signs: aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces (12) -- but rahu/ketu added → see sitemap for exact list.

Priority spot-checks:
```
https://www.everydayhoroscope.in/transits/jupiter-in-aries
https://www.everydayhoroscope.in/transits/saturn-in-capricorn
https://www.everydayhoroscope.in/transits/venus-in-taurus
https://www.everydayhoroscope.in/transits/moon-in-scorpio
```

---

### SEO-20K M2 -- Compatibility Pages (144)
Pattern: `https://www.everydayhoroscope.in/compatibility/{sign1}-and-{sign2}`

Priority spot-checks:
```
https://www.everydayhoroscope.in/compatibility/aries-and-leo
https://www.everydayhoroscope.in/compatibility/scorpio-and-pisces
https://www.everydayhoroscope.in/compatibility/taurus-and-virgo
https://www.everydayhoroscope.in/compatibility/gemini-and-aquarius
```

---

### SEO-20K M3 -- Festival × Region (480) + Character Placement (432)

**Festival-Region:** `https://www.everydayhoroscope.in/festivals/{festival}/{region}`

Priority spot-checks:
```
https://www.everydayhoroscope.in/festivals/diwali/delhi
https://www.everydayhoroscope.in/festivals/holi/mumbai
https://www.everydayhoroscope.in/festivals/navratri/jaipur
https://www.everydayhoroscope.in/festivals/dussehra/bengaluru
```

**Character Placement:** `https://www.everydayhoroscope.in/traits/{sign}/{point}/{house}`

Priority spot-checks:
```
https://www.everydayhoroscope.in/traits/aries/sun/first-house
https://www.everydayhoroscope.in/traits/scorpio/moon/eighth-house
https://www.everydayhoroscope.in/traits/capricorn/saturn/tenth-house
https://www.everydayhoroscope.in/traits/pisces/jupiter/twelfth-house
```

---

## Seed Script Run Order (Render -- before GSC submission of dynamic modules)

Run these in Render's shell in this order to ensure Mongo is populated before GSC crawls:

```bash
# 1. Crystals
python backend/scripts/seed_crystals.py

# 2. Rudraksha
python backend/scripts/seed_rudraksha.py

# 3. Lo Shu Grid
python backend/scripts/seed_lo_shu.py

# 4. Zibu Symbols
python backend/scripts/seed_zibu_symbols.py

# 5. Angel Numbers (core first, then intents)
python backend/scripts/seed_angel_numbers_core.py
python backend/scripts/seed_angel_numbers_intents.py

# 6. SEO-20K M3 seeds
python backend/scripts/seed_transit_profiles.py
python backend/scripts/seed_festival_regions.py
python backend/scripts/seed_character_placements.py
```

*Note: Angel Numbers and Crystal modules include built-in fallback content -- pages serve without seeding. Rudraksha and Lo Shu may also have fallback. Zibu has built-in fallback catalog. Seeding improves page richness but is not blocking for GSC submission.*

---

## Summary -- Total Pages Built (as of 2026-05-26)

| Module | Pages | Status |
|---|---|---|
| Panchang | ~2,226 | ✅ Live |
| Choghadiya | ~1,272 | ✅ Live |
| Horoscope (D/W/M) | 36 | ✅ Live |
| Compatibility | 144 | ✅ Live |
| Remedies | 12 | ✅ Live |
| SEO-20K M1 (Transits) | 78 | ✅ Live |
| SEO-20K M2 (Compat pairs) | 144 | ✅ Live |
| SEO-20K M3 (Festival+Trait) | 1,020 | ✅ Live |
| Crystal Healing | 72 | ✅ Live |
| Lo Shu Grid | 20 | ✅ Live |
| Rudraksha | 23 | ✅ Live |
| Zibu Symbols | 89 | ✅ Live |
| Angel Numbers | 10,001 | ✅ Live |
| **TOTAL** | **~15,137** | |

*Not counted above: static pages (home, about, tarot, kundali, birth chart, numerology, blog, legal, admin, etc.) -- approximately 50-80 additional pages already in GSC.*
