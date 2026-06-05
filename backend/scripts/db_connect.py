"""
Shared MongoDB connection helper for KE patch/ingest scripts.
Reads MONGO_URL from the environment (export MONGO_URL=... in terminal).
All scripts import this instead of duplicating connection logic.

Usage:
    from db_connect import get_collection
    col = get_collection("interpretation_rules")
"""

import os
import sys
from pymongo import MongoClient

_client = None

def get_client() -> MongoClient:
    global _client
    if _client is None:
        mongo_url = os.environ.get("MONGO_URL")
        if not mongo_url:
            print("ERROR: MONGO_URL is not set in the environment.")
            print("       Run:  export MONGO_URL='mongodb+srv://...'")
            print("       Then re-run the script.")
            sys.exit(1)
        _client = MongoClient(mongo_url)
    return _client


def get_db(db_name: str = "horoscope_db"):
    return get_client()[db_name]


def get_collection(collection_name: str, db_name: str = "horoscope_db"):
    return get_db(db_name)[collection_name]
