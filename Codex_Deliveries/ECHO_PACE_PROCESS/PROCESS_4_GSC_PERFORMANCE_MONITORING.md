# ECHO // PACE Process 4 -- GSC Performance Monitoring
> Search Console health monitoring framework for all SEO modules
> Source: GAI ECHO//PACE Compliance Consultation V2
> Applies to: ALL live SEO modules
> Last updated: 2026-05-26

---

## Overview

After seeding a module to production, Google's indexation pipeline passes each page through several classification stages. Knowing what each status means -- and what to do about it -- determines how quickly the 5,000+ pages reach ranking position.

This process defines:
1. What each GSC status means for programmatic content
2. Module-specific regex filters for the GSC Performance tab
3. A daily monitoring checklist
4. The automated sitemap ping to trigger rapid re-crawl

---

## The Three Critical GSC Indexing Statuses

### I. "Discovered -- Currently Not Indexed" 🟡

**What it means:** Google's crawler found the URL (via sitemap or link) but chose not to crawl it yet to conserve resources.

**Why it happens for us:** Combination pages that only exist in the sitemap XML with no internal links pointing to them. Crawlers treat these as low-confidence orphaned URLs.

**Fix:**
- Add "Explore by Spread" / "Explore by Intent" internal link grids to parent pages (Process 3 -- Orphan Page Prevention)
- Verify the page appears in at least 2 internal cross-links before reporting to GSC

**Module-specific:**
| Module | Parent Page | Add Links To |
|---|---|---|
| TAR-M4 combinations | `/tarot/card/{slug}` | Top 10 spread combinations for that card |
| Angel intent pages | `/angel-numbers/{number}` | All 9 intent pages for that number |
| Festival-region | `/festivals/{festival}` | All 30 regional pages for that festival |

---

### II. "Crawled -- Currently Not Indexed" 🔴

**What it means:** Google crawled the page but filtered it out as low-value, duplicate, or programmatic noise. This is the highest-risk status -- it means the content has been seen and consciously rejected.

**Why it happens for us:** Cross-page similarity ≥30% (ECHO Process 2 failure), templated opening sentences, or pages where 80%+ of text is shared with sister pages.

**Fix:**
1. Run `backend/scripts/verify_{module}_compliance.py` on the affected pages
2. If cross-page similarity ≥30%: apply Process 1 (anchor flip + intent field)
3. Re-seed affected records to MongoDB
4. Use GSC "Request Indexing" on a representative sample (10 pages) after fix
5. Wait 2-3 weeks for full re-crawl cycle

**Early warning signal:** If more than 5% of a module's pages land in "Crawled -- Not Indexed" within 30 days of seeding, the content generation strategy needs Process 1 applied.

---

### III. "Excluded by 'noindex' tag" 🟠

**What it means:** The page has a `<meta name="robots" content="noindex">` tag or `X-Robots-Tag: noindex` header.

**Why it happens for us:** Render staging config accidentally deploying with noindex headers, or a React route missing the SEO component.

**Fix:**
- Check `frontend/src/components/SEO.jsx` -- all SEO routes must include the SEO component with `index, follow`
- Check Vercel environment variables -- `REACT_APP_NOINDEX` must not be set in production
- Verify live URL: `curl -I https://www.everydayhoroscope.in/tarot/spread/{slug} | grep -i robots`

---

## GSC Custom Regex Filters -- Performance Tab

Open GSC → Performance → Pages → Filter: Page → Custom (Regex)

### Tarot Module Filters

| Intent | Regex | Purpose |
|---|---|---|
| All tarot pages | `^https://www\.everydayhoroscope\.in/tarot/` | Full tarot performance |
| Spread pages | `/tarot/spread/` | Core spread ranking |
| Card pages | `/tarot/card/` | Core card ranking |
| Combination: Love | `/tarot/cards/.*love\|.*soulmate\|.*twin\|.*relationship` | Love intent cluster |
| Combination: Career | `/tarot/cards/.*career\|.*job\|.*business\|.*money` | Career intent cluster |
| Combination: Health | `/tarot/cards/.*health\|.*healing\|.*anxiety\|.*fitness` | Health intent cluster |

### Angel Numbers Filters

| Intent | Regex | Purpose |
|---|---|---|
| All angel pages | `/angel-numbers/` | Full module performance |
| Core number pages | `/angel-numbers/[0-9]+$` | Root number ranking |
| Love intent | `/angel-numbers/.*love` | Love intent cluster |
| Twin flame | `/angel-numbers/.*twin` | Twin flame cluster |
| Manifestation | `/angel-numbers/.*manifestation` | Manifestation cluster |

### Festival-Region Filters

| Intent | Regex | Purpose |
|---|---|---|
| All festival pages | `/festivals/` | Full module performance |
| Diwali cluster | `/festivals/diwali/` | Highest-volume festival |
| South zone | `/festivals/.*/.*andhra\|.*tamil\|.*kerala\|.*karnataka` | South region cluster |
| North zone | `/festivals/.*/.*punjab\|.*delhi\|.*uttar` | North region cluster |

---

## Daily Monitoring Checklist (First 30 Days Post-Seed)

Run this check each morning in GSC after seeding a new module:

```
Day 1-3:   Check "Submitted but not yet indexed" count rising (good -- pages discovered)
Day 3-7:   Check "Indexed -- not submitted in sitemap" (means internal links working)
Day 7-14:  Watch for "Crawled -- Currently Not Indexed" counts -- alert if >5% of module
Day 14-30: Track impressions rising in Performance tab for core pages
Day 30:    Run full Page Indexing Report -- any "Crawled Not Indexed" pages need Process 1
```

**Alert thresholds:**
- "Crawled Not Indexed" > 5% of module → Apply Process 1 immediately
- "Discovered Not Indexed" > 20% after 2 weeks → Add internal cross-links (Process 3)
- Zero impressions after 30 days for any page cluster → Check noindex + sitemap registration

---

## Automated Sitemap Ping

After every seed and every sitemap update, ping Google to queue immediate re-crawl:

```python
# backend/scripts/ping_sitemaps.py
import requests

SITEMAP_INDEX = "https://www.everydayhoroscope.in/sitemap-index.xml"

def ping_google():
    endpoint = f"https://www.google.com/ping?sitemap={SITEMAP_INDEX}"
    r = requests.get(endpoint, timeout=10)
    if r.status_code == 200:
        print("✅ Google ping: sitemap queued for re-crawl")
    else:
        print(f"⚠️  Google ping returned {r.status_code}")

def ping_bing():
    endpoint = f"https://www.bing.com/ping?sitemap={SITEMAP_INDEX}"
    r = requests.get(endpoint, timeout=10)
    if r.status_code == 200:
        print("✅ Bing ping: sitemap queued for re-crawl")
    else:
        print(f"⚠️  Bing ping returned {r.status_code}")

if __name__ == "__main__":
    ping_google()
    ping_bing()
```

Run after every seed: `python3 backend/scripts/ping_sitemaps.py`

---

## Search Console Priority Settings Per Module

These match the sitemap priority values from Process 3 and inform which pages GSC considers highest value:

| URL Pattern | GSC Priority | Expected Indexing Speed |
|---|---|---|
| `/` homepage | 1.0 | Within 24 hours |
| `/tarot/`, `/angel-numbers/` hubs | 0.9 | 1-3 days |
| `/tarot/for/love`, `/angel-numbers/111/love` | 0.8 | 3-7 days |
| `/tarot/card/{slug}`, `/angel-numbers/{number}` | 0.7 | 1-2 weeks |
| `/tarot/cards/{card}/{spread}` combinations | 0.4 | 2-6 weeks |

---

## Module Seeding → GSC Monitoring Sequence

```
1. Codex delivers module content
2. Run textbook plagiarism scan (Process 2, Layer 1-3)
3. Run cross-page compliance test (Process 2, Layer CI)
4. Seed to MongoDB (Render shell: python scripts/seed_{module}.py)
5. Run sitemap generator (generate_sitemaps.py)
6. Push updated sitemaps to main (git push)
7. Run sitemap ping (ping_sitemaps.py)
8. Begin daily GSC monitoring checklist (this document)
9. At Day 7: check Crawled Not Indexed count
10. At Day 30: full Page Indexing Report review
```

---

## Performance Benchmarks -- What Good Looks Like

Based on EverydayHoroscope's current domain authority, expected timelines after seeding:

| Metric | Week 1 | Week 4 | Week 12 |
|---|---|---|---|
| Pages indexed / pages submitted | 10-20% | 40-60% | 70-90% |
| Impressions for core pages | 0-50 | 50-500 | 500-5,000 |
| Average position (core pages) | Not ranked | 30-60 | 15-35 |
| Click-through rate | -- | 0.5-2% | 2-5% |

**Tarot spread pages** will index faster than combination pages (higher priority, more internal links).
**Angel Numbers** core pages (111, 222, 333) will rank faster than 4-digit numbers.
**Festival pages** will spike in impression volume 2-4 weeks before each festival date.
