# Codex Commission: GRW-3 -- Intelligence Dashboard (GSC + SERPER)
> **Module:** Growth -- SEO & Competitor Intelligence
> **Issued:** 2026-06-08 | **Priority:** Medium-High
> **Env vars needed:** `SERPER_API_KEY` (TT to add to Render), `GSC_CLIENT_ID`, `GSC_CLIENT_SECRET` (TT to add to Render -- same OAuth flow as YouTube)

---

## 1. What This Builds

A new **Intelligence** tab in the Admin Console with two sub-tabs:

| Sub-tab | Data source | Refresh cadence | Purpose |
|---|---|---|---|
| **GSC -- Index Health** | Google Search Console API | Daily (APScheduler) | Shows which programmatic pages are stuck "Crawled - Not Indexed" or excluded |
| **SERPER -- Keyword Intel** | Serper.dev Search API | Weekly (APScheduler) | Shows top ranking keywords, competitor gaps, new competitor pages |

Both panels are read-only in Phase 1 -- data in, no automated content changes.

---

## 2. Files to Create / Modify

```
backend/intelligence_service.py           ← NEW -- all GSC + SERPER logic
backend/server.py                         ← GSC OAuth routes + admin data endpoints + APScheduler jobs
frontend/src/pages/admin/AdminDashboard.jsx ← New "Intelligence" tab
```

New MongoDB collection: `intelligence_cache` -- stores fetched data with timestamps.

---

## 3. GSC Sub-Tab -- Index Health

### 3a -- OAuth Setup (mirrors YouTube OAuth already in server.py)

Env vars: `GSC_CLIENT_ID`, `GSC_CLIENT_SECRET`, `GSC_REDIRECT_URI`

Endpoints to add to server.py:
```
GET  /api/admin/gsc/status        → { connected: bool, site_url: str|null, connected_at: str|null }
GET  /api/admin/gsc/auth-url      → { auth_url: str }
GET  /api/admin/gsc/callback      → handles OAuth code exchange, stores tokens in db.admin_oauth_tokens
POST /api/admin/gsc/disconnect    → removes GSC tokens
```

Scopes needed: `https://www.googleapis.com/auth/webmasters.readonly`

### 3b -- Data fetch function: `fetch_gsc_index_health(db)`

Called by APScheduler daily at 06:00. Fetches from GSC Search Console API v3:
- `searchAnalytics.query` for top 500 URLs by impressions (last 30 days)
- `urlInspection.index.inspect` for up to 50 flagged URLs (rate-limited -- do not exceed)

Stores result in `intelligence_cache` collection:
```python
{
  "cache_key": "gsc_index_health",
  "fetched_at": datetime,
  "data": {
    "summary": {
      "total_urls_checked": int,
      "indexed": int,
      "crawled_not_indexed": int,
      "excluded": int,
      "errors": int
    },
    "flagged_urls": [
      {
        "url": str,
        "verdict": "PASS"|"FAIL"|"NEUTRAL",
        "coverage_state": str,   # "Crawled - currently not indexed" etc.
        "indexing_state": str,
        "impressions_30d": int,
        "clicks_30d": int
      }
    ],
    "top_queries": [
      { "query": str, "clicks": int, "impressions": int, "position": float }
    ]
  }
}
```

### 3c -- Admin UI -- GSC Sub-Tab

**Connection banner:** If not connected → show "Connect Google Search Console" button (same pattern as YouTube OAuth button in Social Media sub-tab).

**Once connected -- 4 data panels:**

Panel 1 -- Index Health Summary (4 stat cards):
```
[Indexed: 18,432]  [Crawled-Not Indexed: 247]  [Excluded: 89]  [Errors: 12]
```

Panel 2 -- Flagged URLs Table (sortable):
```
URL | Coverage State | Impressions | Clicks | Status
/faith/gita/... | Crawled - not indexed | 42 | 0 | ⚠️
```
With "Copy URL" button per row.

Panel 3 -- Top Queries (last 30 days):
```
Query | Clicks | Impressions | Avg Position
```
Top 20 rows.

Panel 4 -- Last fetched timestamp + "Refresh now" button (manual trigger).

---

## 4. SERPER Sub-Tab -- Keyword Intelligence

### 4a -- Fetch function: `fetch_serper_intel(db)`

Called by APScheduler weekly on Monday at 07:00.
Uses `SERPER_API_KEY` env var. Calls `https://google.serper.dev/search`.

**Target queries (hardcoded Phase 1 -- expand later):**
```python
SEED_QUERIES = [
    "vedic astrology birth chart online",
    "kundali milan free",
    "daily horoscope today hindi",
    "panchang today",
    "bhagavad gita quotes for life",
    "angel numbers meaning",
    "sade sati calculator",
    "lal kitab remedies",
    "numerology calculator",
    "tarot card reading online free india",
]
```

For each query: fetch top 10 organic results. Extract:
- `domain`, `title`, `url`, `snippet`, `position`

Flag any result from these competitor domains (hardcoded Phase 1):
```python
COMPETITOR_DOMAINS = [
    "astrotalk.com", "ganeshaspeaks.com", "astroyogi.com",
    "prokerala.com", "astrosage.com", "mpanchang.com",
    "bejandaruwalla.com", "clickastro.com"
]
```

Stores in `intelligence_cache`:
```python
{
  "cache_key": "serper_intel",
  "fetched_at": datetime,
  "data": {
    "queries": [
      {
        "query": str,
        "our_position": int|None,       # position of everydayhoroscope.in, null if not in top 10
        "our_url": str|None,
        "competitor_results": [
          { "domain": str, "position": int, "title": str, "url": str }
        ],
        "top_result": { "domain": str, "title": str, "url": str }
      }
    ],
    "summary": {
      "queries_where_we_rank_top10": int,
      "queries_where_we_are_absent": int,
      "most_frequent_competitor": str
    }
  }
}
```

### 4b -- Admin UI -- SERPER Sub-Tab

**Connection status banner:** Check `SERPER_API_KEY` env var on backend. Show "API Key configured ✅" or "SERPER_API_KEY missing -- add to Render env vars".

**Panel 1 -- Summary Cards:**
```
[Ranking Top 10: 3/10 queries]  [Not Ranking: 7/10]  [Top Competitor: astrotalk.com]
```

**Panel 2 -- Query Rankings Table:**
```
Query | Our Position | Our URL | Top Competitor | Their Position
"vedic astrology birth chart" | -- | -- | astrotalk.com | #1
"panchang today" | #3 | /panchang | mpanchang.com | #1
```
Color coding: Our position ≤ 3 = green, 4-10 = amber, absent = red.

**Panel 3 -- Last fetched + "Refresh now" button.**

---

## 5. Admin Endpoints -- `server.py`

```python
GET /api/admin/intelligence/gsc          # returns gsc_index_health cache doc
GET /api/admin/intelligence/gsc/refresh  # manual trigger fetch_gsc_index_health()
GET /api/admin/intelligence/serper       # returns serper_intel cache doc
GET /api/admin/intelligence/serper/refresh  # manual trigger fetch_serper_intel()
```

All require `require_admin` dependency.

---

## 6. APScheduler Jobs

Add to existing scheduler in server.py:
```python
scheduler.add_job(fetch_gsc_index_health,  'cron', hour=6,  minute=0, id='gsc_daily')
scheduler.add_job(fetch_serper_intel,      'cron', day_of_week='mon', hour=7, id='serper_weekly')
```

Both jobs must be wrapped in try/except. On failure: log to `db.notification_logs` with `type="system_error"`.

---

## 7. Acceptance Gates (8)

| Gate | Test |
|---|---|
| G-01 | `GET /api/admin/gsc/status` returns `{ connected: false }` before OAuth |
| G-02 | GSC OAuth flow completes and `GET /api/admin/gsc/status` returns `{ connected: true, site_url: "https://www.everydayhoroscope.in" }` |
| G-03 | `GET /api/admin/intelligence/gsc/refresh` triggers fetch and stores result in `intelligence_cache` |
| G-04 | GSC sub-tab shows index health summary cards with non-null values |
| G-05 | `SERPER_API_KEY` missing → SERPER sub-tab shows "API Key missing" banner, does not crash |
| G-06 | `SERPER_API_KEY` present → `fetch_serper_intel()` stores result in `intelligence_cache` |
| G-07 | SERPER sub-tab shows query rankings table with colour coding |
| G-08 | APScheduler jobs registered without error on server startup |

---

## 8. Constraints

- GSC URL Inspection API: max 2,000 requests/day. Limit `flagged_urls` inspection to 50 per run.
- SERPER API: 2,500 free searches/month. 10 queries × weekly = 40/month. Well within limit.
- Never store raw HTML or full page content -- metadata only.
- All cached data expires after 8 days (TTL index on `fetched_at` field).
- Commit: `feat(growth): GRW-3 intelligence dashboard GSC + SERPER`
