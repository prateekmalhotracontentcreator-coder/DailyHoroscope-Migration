from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Response

from crystal_data import get_crystal_sitemap_urls
from panchang_router import DEFAULT_LOCATIONS
from lo_shu_router import LO_SHU_SITEMAP_URLS
from rudraksha_content import PLANET_RUDRAKSHA_SLUGS, PROBLEM_RUDRAKSHA_SLUGS, SIGN_RUDRAKSHA_SLUGS
from seo_m3_catalog import CHART_POINTS, FESTIVAL_SLUGS, HOUSES, PLANET_SLUGS, REGION_SLUGS, SIGN_SLUGS
from zibu_catalog import list_symbol_summaries as list_zibu_summaries


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
COMPATIBILITY_SIGNS = SIGN_SLUGS
REMEDY_DOSHAS = [
    "shani-sade-sati",
    "manglik-dosha",
    "pitru-dosha",
    "kaal-sarp-dosha",
    "shani-mahadasha",
    "rahu-mahadasha",
    "ketu-mahadasha",
    "guru-chandal-yoga",
    "grahan-yoga",
    "nadi-dosha",
    "gana-dosha",
    "bhakoot-dosha",
]
RUDRAKSHA_SLUGS = [f"{number}-mukhi" for number in range(1, 22)]


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


@router.get("/sitemap/compatibility")
async def get_compatibility_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = []
    for sign1 in COMPATIBILITY_SIGNS:
        for sign2 in COMPATIBILITY_SIGNS:
            canonical_pair = "-and-".join(sorted([sign1, sign2]))
            urls.append((f"{SITE_URL}/compatibility/{canonical_pair}", today))
    return _xml_response(_sitemap_xml(urls))


@router.get("/sitemap/remedies")
async def get_remedies_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = [(f"{SITE_URL}/remedies/{slug}", today) for slug in REMEDY_DOSHAS]
    return _xml_response(_sitemap_xml(urls))


@router.get("/sitemap/transits")
async def get_transits_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = [
        (f"{SITE_URL}/transits/{planet_slug}-in-{sign_slug}", today)
        for planet_slug in PLANET_SLUGS
        for sign_slug in SIGN_SLUGS
    ]
    return _xml_response(_sitemap_xml(urls))


@router.get("/sitemap/festivals")
async def get_festival_region_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = [
        (f"{SITE_URL}/festivals/{festival_slug}/{region_slug}", today)
        for festival_slug in FESTIVAL_SLUGS
        for region_slug in REGION_SLUGS
    ]
    return _xml_response(_sitemap_xml(urls))


@router.get("/sitemap/traits")
async def get_traits_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = [
        (f"{SITE_URL}/traits/{sign_slug}/{chart_point['slug']}/{house['slug']}", today)
        for sign_slug in SIGN_SLUGS
        for chart_point in CHART_POINTS
        for house in HOUSES
    ]
    return _xml_response(_sitemap_xml(urls))


@router.get("/sitemap/crystals")
async def get_crystals_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = [(href, today) for href in get_crystal_sitemap_urls()]
    return _xml_response(_sitemap_xml(urls))


@router.get("/sitemap/lo-shu-grid")
async def get_lo_shu_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = [(href, today) for href in LO_SHU_SITEMAP_URLS]
    return _xml_response(_sitemap_xml(urls))


@router.get("/sitemap/rudraksha")
async def get_rudraksha_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = [
        (f"{SITE_URL}/rudraksha", today),
        (f"{SITE_URL}/rudraksha/calculator", today),
        *[(f"{SITE_URL}/rudraksha/{slug}", today) for slug in RUDRAKSHA_SLUGS],
        *[(f"{SITE_URL}/rudraksha/for/planet/{slug}", today) for slug in PLANET_RUDRAKSHA_SLUGS],
        *[(f"{SITE_URL}/rudraksha/for/problem/{slug}", today) for slug in PROBLEM_RUDRAKSHA_SLUGS],
        *[(f"{SITE_URL}/rudraksha/for/sign/{slug}", today) for slug in SIGN_RUDRAKSHA_SLUGS],
    ]
    return _xml_response(_sitemap_xml(urls))


@router.get("/sitemap/zibu")
async def get_zibu_sitemap() -> Response:
    today = datetime.now(INDIA_TZ).date().isoformat()
    urls = [(f"{SITE_URL}/zibu", today)]
    urls.extend(
        (f"{SITE_URL}/zibu/{symbol['slug']}", today)
        for symbol in list_zibu_summaries()
    )
    return _xml_response(_sitemap_xml(urls))
