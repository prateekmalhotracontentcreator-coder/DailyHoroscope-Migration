#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tarot_seo_data import (  # noqa: E402
    get_card,
    get_intention,
    get_spread,
    list_card_summaries,
    list_intention_summaries,
    list_spread_summaries,
)


async def seed() -> None:
    load_dotenv(ROOT / ".env")

    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "horoscope_db")

    if not mongo_url:
        print("ERROR: MONGO_URL environment variable is required")
        sys.exit(1)

    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    # ── Spreads ──────────────────────────────────────────────────────────
    spread_slugs = [item["slug"] for item in list_spread_summaries()]
    for slug in spread_slugs:
        doc = get_spread(slug)
        if doc:
            await db.tarot_spreads.update_one(
                {"slug": slug}, {"$set": doc}, upsert=True
            )
    print(f"Seeded {len(spread_slugs)} documents into 'tarot_spreads'.")

    # ── Cards ─────────────────────────────────────────────────────────────
    card_slugs = [item["slug"] for item in list_card_summaries()]
    for slug in card_slugs:
        doc = get_card(slug)
        if doc:
            await db.tarot_cards.update_one(
                {"slug": slug}, {"$set": doc}, upsert=True
            )
    print(f"Seeded {len(card_slugs)} documents into 'tarot_cards'.")

    # ── Intentions ────────────────────────────────────────────────────────
    intention_slugs = [item["slug"] for item in list_intention_summaries()]
    for slug in intention_slugs:
        doc = get_intention(slug)
        if doc:
            await db.tarot_intentions.update_one(
                {"slug": slug}, {"$set": doc}, upsert=True
            )
    print(f"Seeded {len(intention_slugs)} documents into 'tarot_intentions'.")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
