from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
import os
from typing import Any
from urllib.parse import quote

import httpx

try:
    from google.oauth2.credentials import Credentials as GoogleCredentials
    from google.auth.transport.requests import Request as GoogleRequest
    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False


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

COMPETITOR_DOMAINS = [
    "astrotalk.com",
    "ganeshaspeaks.com",
    "astroyogi.com",
    "prokerala.com",
    "astrosage.com",
    "mpanchang.com",
    "bejandaruwalla.com",
    "clickastro.com",
]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _gsc_site_url() -> str:
    return os.environ.get("GSC_SITE_URL", "https://www.everydayhoroscope.in").rstrip("/")


async def _get_gsc_token_doc(db) -> dict[str, Any] | None:
    return await db.admin_oauth_tokens.find_one({"service": "gsc"}, {"_id": 0})


async def _get_gsc_access_token(db) -> str | None:
    token_doc = await _get_gsc_token_doc(db)
    if not token_doc:
        return None
    if not GOOGLE_LIBS_AVAILABLE:
        return token_doc.get("access_token")

    client_id = os.environ.get("GSC_CLIENT_ID", "")
    client_secret = os.environ.get("GSC_CLIENT_SECRET", "")
    refresh_token = token_doc.get("refresh_token")
    if not client_id or not client_secret or not refresh_token:
        return token_doc.get("access_token")

    creds = GoogleCredentials(
        token=token_doc.get("access_token"),
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=token_doc.get("scopes") or ["https://www.googleapis.com/auth/webmasters.readonly"],
    )
    if not creds.valid:
        creds.refresh(GoogleRequest())
        await db.admin_oauth_tokens.update_one(
            {"service": "gsc"},
            {
                "$set": {
                    "access_token": creds.token,
                    "token_expiry": creds.expiry,
                    "updated_at": _utc_now(),
                }
            },
        )
    return creds.token


def _normalize_domain(url: str) -> str:
    value = (url or "").lower()
    value = value.replace("https://", "").replace("http://", "")
    return value.split("/")[0].lstrip("www.")


async def fetch_gsc_index_health(db) -> dict[str, Any]:
    access_token = await _get_gsc_access_token(db)
    if not access_token:
        raise RuntimeError("GSC not connected")

    site_url = _gsc_site_url()
    encoded_site = quote(site_url, safe="")
    end_date = _utc_now().date()
    start_date = end_date - timedelta(days=30)

    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient(timeout=45) as client:
        page_rows_response = await client.post(
            f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query",
            headers=headers,
            json={
                "startDate": start_date.isoformat(),
                "endDate": end_date.isoformat(),
                "dimensions": ["page"],
                "rowLimit": 500,
            },
        )
        page_rows_response.raise_for_status()
        page_rows = (page_rows_response.json() or {}).get("rows") or []

        query_rows_response = await client.post(
            f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query",
            headers=headers,
            json={
                "startDate": start_date.isoformat(),
                "endDate": end_date.isoformat(),
                "dimensions": ["query"],
                "rowLimit": 20,
            },
        )
        query_rows_response.raise_for_status()
        query_rows = (query_rows_response.json() or {}).get("rows") or []

        candidate_pages = sorted(
            page_rows,
            key=lambda row: int(row.get("impressions", 0)),
            reverse=True,
        )[:50]

        flagged_urls: list[dict[str, Any]] = []
        indexed = crawled_not_indexed = excluded = errors = 0
        for row in candidate_pages:
            url = ((row.get("keys") or [None])[0]) or ""
            inspect_response = await client.post(
                "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                headers=headers,
                json={"inspectionUrl": url, "siteUrl": site_url},
            )
            if inspect_response.status_code >= 400:
                errors += 1
                flagged_urls.append(
                    {
                        "url": url,
                        "verdict": "FAIL",
                        "coverage_state": f"Inspection error {inspect_response.status_code}",
                        "indexing_state": "ERROR",
                        "impressions_30d": int(row.get("impressions", 0)),
                        "clicks_30d": int(row.get("clicks", 0)),
                    }
                )
                continue
            result = ((((inspect_response.json() or {}).get("inspectionResult") or {}).get("indexStatusResult")) or {})
            verdict = result.get("verdict", "NEUTRAL")
            coverage_state = result.get("coverageState", "Unknown")
            indexing_state = result.get("indexingState", "")

            lowered = f"{coverage_state} {indexing_state}".lower()
            if "indexed" in lowered and "not indexed" not in lowered:
                indexed += 1
            elif "crawled" in lowered and "not indexed" in lowered:
                crawled_not_indexed += 1
            elif "excluded" in lowered:
                excluded += 1
            elif verdict == "FAIL":
                errors += 1

            flagged_urls.append(
                {
                    "url": url,
                    "verdict": verdict,
                    "coverage_state": coverage_state,
                    "indexing_state": indexing_state,
                    "impressions_30d": int(row.get("impressions", 0)),
                    "clicks_30d": int(row.get("clicks", 0)),
                }
            )

    data = {
        "summary": {
            "total_urls_checked": len(flagged_urls),
            "indexed": indexed,
            "crawled_not_indexed": crawled_not_indexed,
            "excluded": excluded,
            "errors": errors,
        },
        "flagged_urls": flagged_urls,
        "top_queries": [
            {
                "query": ((row.get("keys") or [""])[0]),
                "clicks": int(row.get("clicks", 0)),
                "impressions": int(row.get("impressions", 0)),
                "position": float(row.get("position", 0)),
            }
            for row in query_rows[:20]
        ],
    }

    document = {
        "cache_key": "gsc_index_health",
        "fetched_at": _utc_now(),
        "data": data,
    }
    await db.intelligence_cache.update_one(
        {"cache_key": "gsc_index_health"},
        {"$set": document},
        upsert=True,
    )
    return document


async def fetch_serper_intel(db) -> dict[str, Any]:
    api_key = os.environ.get("SERPER_API_KEY", "")
    if not api_key:
        raise RuntimeError("SERPER_API_KEY missing")

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    queries_payload: list[dict[str, Any]] = []
    competitor_counter: Counter[str] = Counter()
    queries_where_we_rank_top10 = 0
    queries_where_we_are_absent = 0

    async with httpx.AsyncClient(timeout=30) as client:
        for query in SEED_QUERIES:
            response = await client.post(
                "https://google.serper.dev/search",
                headers=headers,
                json={"q": query, "num": 10},
            )
            response.raise_for_status()
            organic = (response.json() or {}).get("organic") or []

            our_position = None
            our_url = None
            competitor_results: list[dict[str, Any]] = []
            top_result = None

            for row in organic[:10]:
                url = row.get("link") or row.get("url") or ""
                domain = _normalize_domain(url)
                position = int(row.get("position") or 0)
                title = row.get("title") or ""
                snippet = row.get("snippet") or ""

                if not top_result and domain:
                    top_result = {"domain": domain, "title": title, "url": url}

                if "everydayhoroscope.in" in domain and our_position is None:
                    our_position = position
                    our_url = url

                if domain in COMPETITOR_DOMAINS:
                    competitor_counter[domain] += 1
                    competitor_results.append(
                        {
                            "domain": domain,
                            "position": position,
                            "title": title,
                            "url": url,
                            "snippet": snippet,
                        }
                    )

            if our_position is not None:
                queries_where_we_rank_top10 += 1
            else:
                queries_where_we_are_absent += 1

            queries_payload.append(
                {
                    "query": query,
                    "our_position": our_position,
                    "our_url": our_url,
                    "competitor_results": competitor_results,
                    "top_result": top_result,
                }
            )

    document = {
        "cache_key": "serper_intel",
        "fetched_at": _utc_now(),
        "data": {
            "queries": queries_payload,
            "summary": {
                "queries_where_we_rank_top10": queries_where_we_rank_top10,
                "queries_where_we_are_absent": queries_where_we_are_absent,
                "most_frequent_competitor": competitor_counter.most_common(1)[0][0] if competitor_counter else None,
            },
        },
    }
    await db.intelligence_cache.update_one(
        {"cache_key": "serper_intel"},
        {"$set": document},
        upsert=True,
    )
    return document
