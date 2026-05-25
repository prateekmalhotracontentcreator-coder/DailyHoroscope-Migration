from __future__ import annotations

from fastapi import APIRouter, HTTPException

from tarot_seo_data import get_card, get_hub, get_intention, get_spread


router = APIRouter(prefix="/tarot-seo", tags=["tarot-seo"])


@router.get("/hub")
async def tarot_seo_hub() -> dict:
    return get_hub()


@router.get("/spread/{slug}")
async def tarot_spread_page(slug: str) -> dict:
    payload = get_spread(slug)
    if not payload:
        raise HTTPException(status_code=404, detail="Tarot spread not found")
    return payload


@router.get("/card/{slug}")
async def tarot_card_page(slug: str) -> dict:
    payload = get_card(slug)
    if not payload:
        raise HTTPException(status_code=404, detail="Tarot card not found")
    return payload


@router.get("/for/{slug}")
async def tarot_intention_page(slug: str) -> dict:
    payload = get_intention(slug)
    if not payload:
        raise HTTPException(status_code=404, detail="Tarot intention page not found")
    return payload
