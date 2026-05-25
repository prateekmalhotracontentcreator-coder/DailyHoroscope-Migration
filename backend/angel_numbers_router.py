from __future__ import annotations

from datetime import datetime
from html import escape

from fastapi import APIRouter, HTTPException, Query, Request, Response

from angel_numbers_data import (
    build_hub_payload,
    get_core_record,
    get_intent_record,
    get_sitemap_page,
    normalize_number,
    sitemap_page_count,
    INTENT_ORDER,
)


router = APIRouter(tags=["angel-numbers"])


def _strip_mongo_id(document: dict | None) -> dict | None:
    if not document:
        return None
    cleaned = dict(document)
    cleaned.pop("_id", None)
    return cleaned


def _db(request: Request):
    return getattr(request.app.state, "db", None)


def _xml_response(xml_text: str) -> Response:
    return Response(
        content=xml_text,
        media_type="application/xml",
        headers={"Cache-Control": "s-maxage=86400"},
    )


def _sitemap_xml(urls: list[str]) -> str:
    today = datetime.utcnow().date().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        safe = escape(url)
        lines.append("  <url>")
        lines.append(f"    <loc>{safe}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)


@router.get("/angel-numbers/hub")
async def angel_numbers_hub() -> dict:
    return build_hub_payload()


@router.get("/angel-numbers/{number}")
async def angel_number_detail(number: str, request: Request) -> dict:
    normalized = normalize_number(number)
    if not normalized:
        raise HTTPException(status_code=404, detail="Angel number not found.")

    payload = get_core_record(normalized)
    db = _db(request)
    if db is not None:
        stored = _strip_mongo_id(await db.angel_number_core.find_one({"number": normalized}))
        if stored:
            payload.update(stored)
            payload["intent_summaries"] = get_core_record(normalized)["intent_summaries"]
            payload["faq"] = get_core_record(normalized)["faq"]
            payload["related_numbers"] = get_core_record(normalized)["related_numbers"]
    return payload


@router.get("/angel-numbers/{number}/{intent}")
async def angel_number_intent_detail(number: str, intent: str, request: Request) -> dict:
    normalized = normalize_number(number)
    if not normalized:
        raise HTTPException(status_code=404, detail="Angel number not found.")
    if intent not in INTENT_ORDER:
        raise HTTPException(status_code=404, detail="Intent not found.")

    payload = get_intent_record(normalized, intent)
    db = _db(request)
    if db is not None:
        stored = _strip_mongo_id(
            await db.angel_number_intents.find_one({"number": normalized, "intent": intent})
        )
        if stored:
            payload.update(stored)
            payload["faq"] = get_intent_record(normalized, intent)["faq"]
            payload["related_numbers"] = get_intent_record(normalized, intent)["related_numbers"]
            payload["all_intents"] = get_intent_record(normalized, intent)["all_intents"]
    return payload


@router.get("/sitemap/angel-numbers")
async def angel_numbers_sitemap(page: int = Query(1, ge=1)) -> Response:
    try:
        sitemap = get_sitemap_page(page)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    response = _xml_response(_sitemap_xml(sitemap["urls"]))
    response.headers["X-Sitemap-Page"] = str(sitemap["page"])
    response.headers["X-Sitemap-Page-Count"] = str(sitemap["page_count"])
    return response


@router.get("/angel-numbers/meta/summary")
async def angel_numbers_summary() -> dict:
    counts = build_hub_payload()["counts"]
    return {
        "module": "angel-numbers",
        "core_numbers": counts["core_numbers"],
        "intent_pages": counts["intent_pages"],
        "total_pages": counts["total_pages"],
        "sitemap_pages": sitemap_page_count(),
    }
