# ECHO // PACE Process 3 -- Sitemap Architecture
> Split-sitemap strategy to protect crawl budget and signal content depth
> Source: GAI ECHO//PACE Compliance Consultation V2
> Applies to: ALL modules with 200+ pages
> Last updated: 2026-05-26

---

## The Core Problem

Dumping all 5,000+ page URLs into a single `sitemap.xml` signals to Google that the content is a bulk programmatic dump. Crawlers will throttle budget, partially index, and classify low-priority pages as orphaned.

Additionally, without correct priority hierarchy, crawlers cannot distinguish between high-value hub pages and deep long-tail combination pages -- they allocate crawl budget uniformly and miss the important pages.

---

## The Multi-File Sitemap Architecture

```
sitemap-index.xml
    │
    ├── sitemap-core.xml          ← Hub pages, section hubs (priority 0.9-1.0)
    ├── sitemap-tarot-core.xml    ← 100 spreads + 78 cards + 20 intent pages
    ├── sitemap-tarot-love.xml    ← TAR-M4 combination pages: Love category
    ├── sitemap-tarot-career.xml  ← TAR-M4 combination pages: Career category
    ├── sitemap-tarot-health.xml  ← TAR-M4 combination pages: Health category
    ├── sitemap-tarot-general.xml ← TAR-M4 combination pages: General category
    ├── sitemap-angel.xml         ← 1,000 angel core + 9,000 intent pages
    ├── sitemap-festivals.xml     ← 480 festival-region pages
    ├── sitemap-rudraksha.xml     ← Planet + sign + mukhi pages
    └── sitemap-panchang.xml      ← Daily + city + calendar pages
```

**Rule:** No single child sitemap should exceed 1,000 URLs. Split into sub-files if needed.

---

## Priority Hierarchy (All Modules)

| Page Type | Priority | Change Frequency |
|---|---|---|
| Homepage | `1.0` | daily |
| Section hub (`/tarot/`, `/angel-numbers/`) | `0.9` | weekly |
| Core intent pages (`/tarot/for/love`, `/angel/111/love`) | `0.8` | weekly |
| Individual card / number / crystal pages | `0.7` | monthly |
| Combination pages (`/tarot/cards/the-tower/love-reading`) | `0.4` | monthly |
| Supporting / niche pages | `0.3` | monthly |

**Never mark all pages at `1.0`** -- crawlers ignore priority signals when everything is equal.

---

## Tarot Sitemap Split (Current + TAR-M4)

### Currently Live (199 pages → `sitemap-tarot-core.xml`)
```
/tarot/spreads                          priority 0.9
/tarot/spread/{slug}        × 100       priority 0.7
/tarot/card/{slug}          × 78        priority 0.7
/tarot/for/{slug}           × 20        priority 0.8
```

### TAR-M4 Combinations (4,680 pages → 4 child sitemaps)
```
sitemap-tarot-love.xml     → 78 cards × 9 love spreads    = 702 pages  (priority 0.4)
sitemap-tarot-career.xml   → 78 cards × 14 career spreads = 1,092 pages (priority 0.4)
sitemap-tarot-health.xml   → 78 cards × 8 health spreads  = 624 pages  (priority 0.4)
sitemap-tarot-general.xml  → 78 cards × 29 general spreads = 2,262 pages (priority 0.4)
                                                   TOTAL:  4,680 pages
```

---

## Angel Numbers Sitemap Split

```
sitemap-angel-core.xml     → 900 core number pages         priority 0.7
sitemap-angel-love.xml     → 1,000 love intent pages       priority 0.4
sitemap-angel-career.xml   → 1,000 career intent pages     priority 0.4
sitemap-angel-twin.xml     → 1,000 twin-flame pages        priority 0.4
sitemap-angel-manifest.xml → 1,000 manifestation pages     priority 0.4
sitemap-angel-misc.xml     → 5,000 remaining intent pages  priority 0.3
```

---

## Orphan Page Prevention (Critical)

Combination pages that only exist in XML -- never linked internally -- are classified by Google as "Discovered -- Currently Not Indexed" and progressively deprioritised.

**Rule:** Every combination page must be reachable via at least one internal link on a parent page.

### Implementation per module:

**Tarot:** On each `/tarot/card/{card-slug}` page, add a "Spread Readings" section with links to the top 10 combination pages for that card.

**Angel Numbers:** On each `/angel-numbers/{number}` core page, add a "Explore by Intent" grid with links to all 9 intent pages for that number.

**Festival-Region:** On each `/festivals/{festival-slug}` page, add a "By Region" pill grid linking to all 30 regional variants.

---

## Sitemap Registration

All child sitemaps must be listed in `sitemap-index.xml`. The index file is served at:
`https://www.everydayhoroscope.in/sitemap-index.xml`

This file is already submitted to:
- ✅ Google Search Console
- ✅ Bing Webmaster Tools

**After adding new child sitemaps:** Re-submit the index URL in GSC and Bing (no change to the URL -- just click "Resubmit" for the existing `sitemap-index.xml` entry, which will pick up new child entries automatically).

---

## Sitemap Generator Script

**File:** `backend/scripts/generate_sitemaps.py`

The script must:
1. Load all live slugs from each MongoDB collection
2. Group combination pages by intent category
3. Write child XML files into `frontend/public/sitemaps/`
4. Rewrite `frontend/public/sitemap-index.xml` to reference all children

Run post-seed, before each production push:
```bash
python3 backend/scripts/generate_sitemaps.py
```

---

## Critical Governance Rules

1. **Never include 404 or 301 redirects** in sitemap files -- exclude any URL that the backend returns a non-200 for.
2. **Keep combination pages at priority 0.4** -- this signals long-tail terminal articles to crawlers and preserves budget for hub pages.
3. **Split early** -- add a new child sitemap when any existing child exceeds 1,000 URLs, even if Google's limit is 50,000. Smaller, topically coherent sitemaps index faster.
4. **Match `lastmod` to actual content change dates** -- do not set all `lastmod` to today's date on every generate run. Only update `lastmod` for pages whose content actually changed.

---

## Current Sitemap State

| File | Content | Status |
|---|---|---|
| `frontend/public/sitemap-index.xml` | Index file | ✅ Live -- references child sitemaps |
| `sitemap/panchang` | Panchang city pages | ✅ Live |
| `sitemap/tarot` (core) | Hub + spreads + cards + intentions | ✅ Live -- needs TAR-M4 children added |
| `sitemap/angel` | Angel number pages | ✅ Live -- needs intent split |
| `sitemap/festivals` | Festival-region pages | ✅ Live |
| `sitemap/rudraksha` | Rudraksha pages | ✅ Live |

**Next action after TAR-M4 seed:** Add 4 intent-split tarot combination sitemaps and update index.
