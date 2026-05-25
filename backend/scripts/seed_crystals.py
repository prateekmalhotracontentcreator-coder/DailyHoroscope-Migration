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

from crystal_data import (  # noqa: E402
    CRYSTAL_SLUGS,
    get_crystal_docs,
    get_intention_docs,
    get_planet_crystal_docs,
    get_problem_crystal_docs,
    get_sign_crystal_docs,
)


async def seed() -> None:
    load_dotenv(ROOT_DIR / ".env")

    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ["DB_NAME"]

    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    crystal_docs = get_crystal_docs()
    intention_docs = get_intention_docs()
    planet_docs = get_planet_crystal_docs()
    sign_docs = get_sign_crystal_docs()
    problem_docs = get_problem_crystal_docs()

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

    for slug, doc in planet_docs.items():
        await db.crystal_planets.update_one(
            {"slug": slug},
            {"$set": doc},
            upsert=True,
        )

    for slug, doc in sign_docs.items():
        await db.crystal_signs.update_one(
            {"slug": slug},
            {"$set": doc},
            upsert=True,
        )

    for slug, doc in problem_docs.items():
        await db.crystal_problems.update_one(
            {"slug": slug},
            {"$set": doc},
            upsert=True,
        )

    print(f"Seeded {len(crystal_docs)} crystal documents into 'crystals'.")
    print(f"Seeded {len(intention_docs)} intention documents into 'crystal_intentions'.")
    print(f"Seeded {len(planet_docs)} planet documents into 'crystal_planets'.")
    print(f"Seeded {len(sign_docs)} sign documents into 'crystal_signs'.")
    print(f"Seeded {len(problem_docs)} problem documents into 'crystal_problems'.")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
