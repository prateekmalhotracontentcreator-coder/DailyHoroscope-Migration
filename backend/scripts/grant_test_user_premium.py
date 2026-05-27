"""
grant_test_user_premium.py
---------------------------
One-shot script to grant the test user full premium access on the live DB.

Run on Render shell:
    python3 backend/scripts/grant_test_user_premium.py

Or locally (with MONGO_URL set):
    MONGO_URL="..." DB_NAME="..." python3 backend/scripts/grant_test_user_premium.py
"""

import asyncio
import os
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorClient

# ── Config ─────────────────────────────────────────────────────────────────
MONGO_URL = os.environ.get("MONGO_URL", "")
DB_NAME   = os.environ.get("DB_NAME", "horoscope_db")

# Update this to the actual test user email if different
TEST_USER_EMAIL = os.environ.get("TEST_USER_EMAIL", "prateekmalhotra.contentcreator@gmail.com")


async def main():
    if not MONGO_URL:
        raise EnvironmentError("MONGO_URL env var not set.")

    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    print(f"Connecting to DB: {DB_NAME}")
    print(f"Granting premium to: {TEST_USER_EMAIL}")

    # 1. Update the user document -- set all common premium flags
    result = await db.users.update_one(
        {"email": TEST_USER_EMAIL},
        {"$set": {
            "is_premium": True,
            "is_pro": True,
            "premium": True,
            "plan": "monthly",
            "tier": "premium",
            "has_tarot_access": True,
            "tarot_unlocked": True,
            "tarot_premium": True,
            "has_tarot_premium": True,
            "premium_reports_enabled": True,
            "role": "admin",                        # grants full strategist + tarot access
            "subscription_plan": "monthly",
            "subscription_tier": "premium",
            "updated_at": datetime.now(timezone.utc),
        }}
    )
    print(f"User update: matched={result.matched_count} modified={result.modified_count}")

    if result.matched_count == 0:
        print("WARNING: User not found in users collection.")
        print("Listing all users to verify email...")
        async for u in db.users.find({}, {"email": 1, "_id": 0}):
            print(" -", u.get("email"))
        return

    # 2. Upsert active premium_monthly subscription
    expires = datetime.now(timezone.utc) + timedelta(days=365)
    sub_result = await db.subscriptions.update_one(
        {"user_email": TEST_USER_EMAIL, "subscription_type": "premium_monthly"},
        {"$set": {
            "user_email": TEST_USER_EMAIL,
            "subscription_type": "premium_monthly",
            "status": "active",
            "expires_at": expires,
            "updated_at": datetime.now(timezone.utc),
        }},
        upsert=True
    )
    print(f"Subscription upsert: matched={sub_result.matched_count} upserted_id={sub_result.upserted_id}")

    print()
    print("Done. Test user now has full premium access.")
    print(f"Subscription expires: {expires.strftime('%Y-%m-%d')}")

    client.close()


if __name__ == "__main__":
    asyncio.run(main())
