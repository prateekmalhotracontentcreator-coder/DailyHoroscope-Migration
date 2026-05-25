from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from pymongo import MongoClient, UpdateOne


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from angel_numbers_data import iter_intent_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed angel_number_intents with 9,000 generated records.")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL"))
    parser.add_argument("--db-name", default=os.environ.get("DB_NAME", "horoscope_db"))
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: --mongo-url or MONGO_URL environment variable is required")
        sys.exit(1)

    client = MongoClient(args.mongo_url)
    db = client[args.db_name]
    collection = db.angel_number_intents

    collection.create_index([("number", 1), ("intent", 1)], unique=True)
    operations = [
        UpdateOne(
            {"number": record["number"], "intent": record["intent"]},
            {"$set": record},
            upsert=True,
        )
        for record in iter_intent_records()
    ]
    result = collection.bulk_write(operations, ordered=False)
    print(
        "angel_number_intents seed complete",
        {
            "matched": result.matched_count,
            "modified": result.modified_count,
            "upserted": len(result.upserted_ids),
            "total_records": len(operations),
        },
    )


if __name__ == "__main__":
    main()
