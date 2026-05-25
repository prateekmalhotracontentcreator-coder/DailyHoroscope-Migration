#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from crystal_data import CRYSTAL_SLUGS, get_crystal_docs, get_intention_docs  # noqa: E402


async def seed() -> None:
    load_dotenv(ROOT_DIR / ".env")

    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ["DB_NAME"]

    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    crystal_docs = get_crystal_docs()
    intention_docs = get_intention_docs()

    for slug in CRYSTAL_SLUGS:
        await db.crystals.update_one(
            {"slug": slug},
            {"$set": crystal_docs[slug]},
            upsert=True,
        )

    for slug, doc in intention_docs.items():
        await db.crystal_intentions.update_one(
            {"slug": slug},
            {"$set": doc},
            upsert=True,
        )

    print(f"Seeded {len(crystal_docs)} crystal documents into 'crystals'.")
    print(f"Seeded {len(intention_docs)} intention documents into 'crystal_intentions'.")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
