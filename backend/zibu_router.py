from __future__ import annotations

from copy import deepcopy

from fastapi import APIRouter, HTTPException, Request

from zibu_catalog import ZIBU_SYMBOLS_BY_SLUG, get_all_symbols


router = APIRouter(tags=["seo", "zibu"])


def _collection(request: Request):
    db = getattr(getattr(request.app, "state", None), "db", None)
    if db is None:
        return None
    return db.zibu_symbols


def _hydrate_symbol(document: dict) -> dict:
    slug = str(document.get("slug", "")).strip()
    canonical = ZIBU_SYMBOLS_BY_SLUG.get(slug)
    if canonical is None:
        return deepcopy(document)

    merged = deepcopy(canonical)
    for key, value in document.items():
        if key != "_id":
            merged[key] = value

    complement_docs = []
    for complement_slug in merged.get("complement_symbols", []):
        complement = ZIBU_SYMBOLS_BY_SLUG.get(complement_slug)
        if complement:
            complement_docs.append(
                {
                    "slug": complement["slug"],
                    "display_name": complement["display_name"],
                    "intention": complement["intention"],
                    "tagline": complement["tagline"],
                    "category": complement["category"],
                    "category_label": complement["category_label"],
                }
            )
    merged["complementary_symbols"] = complement_docs
    return merged


async def _load_symbols(request: Request) -> list[dict]:
    collection = _collection(request)
    if collection is None:
        return get_all_symbols()

    try:
        documents = await collection.find({}, {"_id": 0}).sort("symbol_number", 1).to_list(length=200)
    except Exception:
        return get_all_symbols()

    if len(documents) < len(ZIBU_SYMBOLS_BY_SLUG):
        return get_all_symbols()

    hydrated = [_hydrate_symbol(document) for document in documents]
    hydrated.sort(key=lambda item: item.get("symbol_number", 9999))
    return hydrated


@router.get("/zibu/symbols")
async def get_zibu_symbols(request: Request) -> dict:
    symbols = await _load_symbols(request)
    summaries = []
    summary_fields = (
        "slug",
        "display_name",
        "symbol_number",
        "intention",
        "category",
        "category_label",
        "category_short_label",
        "tagline",
        "meta_title",
        "meta_description",
    )
    for symbol in symbols:
        summaries.append({field: symbol[field] for field in summary_fields})
    summaries.sort(key=lambda item: item["symbol_number"])
    return {
        "count": len(summaries),
        "categories": [
            {"key": "love", "label": "Love & Relationships", "short_label": "Love"},
            {"key": "abundance", "label": "Abundance & Money", "short_label": "Abundance"},
            {"key": "healing", "label": "Healing & Release", "short_label": "Healing"},
            {"key": "protection", "label": "Protection & Guidance", "short_label": "Protection"},
            {"key": "spiritual", "label": "Spiritual Growth", "short_label": "Spiritual"},
            {"key": "peace", "label": "Peace & Wellbeing", "short_label": "Peace"},
            {"key": "manifestation", "label": "Manifestation", "short_label": "Manifestation"},
        ],
        "symbols": summaries,
    }


@router.get("/zibu/symbols/{slug}")
async def get_zibu_symbol(slug: str, request: Request) -> dict:
    symbols = await _load_symbols(request)
    for symbol in symbols:
        if symbol.get("slug") == slug:
            hydrated = _hydrate_symbol(symbol)
            if "complementary_symbols" not in hydrated:
                hydrated = _hydrate_symbol(hydrated)
            return hydrated
    raise HTTPException(status_code=404, detail="Zibu symbol not found.")
