from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Response

from panchang_router import DEFAULT_LOCATIONS


router = APIRouter(prefix="/api/seo", tags=["seo"])

SITE_URL = "https://www.everydayhoroscope.in"
INDIA_TZ = ZoneInfo("Asia/Kolkata")
HOROSCOPE_SIGNS = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]
HOROSCOPE_PERIODS = ["tomorrow", "weekly", "monthly"]
CHOGHADIYA_PERIODS = ["today", "tonight", "tomorrow", "tomorrow-night"]


def _sitemap_xml(urls: list[tuple[str, str | None]]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for href, lastmod in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{href}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)


def _xml_response(xml_text: str, ttl_seconds: int = 86400) -> Response:
    return Response(
        content=xml_text,
        media_type="application/xml",
        headers={"Cache-Control": f"s-maxage={ttl_seconds}"},
    )


@router.get("/sitemap/panchang")
async def get_panchang_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date()
    urls: list[tuple[str, str | None]] = []
    for slug in sorted(DEFAULT_LOCATIONS.keys()):
        for offset in range(7):
            current_date = today + timedelta(days=offset)
            urls.append((f"{SITE_URL}/panchang/{slug}/{current_date.isoformat()}", current_date.isoformat()))
    return _xml_response(_sitemap_xml(urls))


@router.get("/sitemap/choghadiya")
async def get_choghadiya_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = [
        (f"{SITE_URL}/choghadiya/{slug}/{period}", today)
        for slug in sorted(DEFAULT_LOCATIONS.keys())
        for period in CHOGHADIYA_PERIODS
    ]
    return _xml_response(_sitemap_xml(urls))


@router.get("/sitemap/horoscope")
async def get_horoscope_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = [
        (f"{SITE_URL}/horoscope/{sign}/{period}", today)
        for sign in HOROSCOPE_SIGNS
        for period in HOROSCOPE_PERIODS
    ]
    return _xml_response(_sitemap_xml(urls))
