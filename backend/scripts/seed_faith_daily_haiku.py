#!/usr/bin/env python3
"""
seed_faith_daily_haiku.py
=========================
Phase-1 offline seeder: generates AI-unique content for Faith DAILY pages
and the Lumina verse cache using Claude Haiku (one call per document).

Architecture
------------
Faith DAILY pages are served via a merge pattern already wired in
faith_seo_router.py (lines 190-204):

    base  = get_daily_page(sign_slug, month_slug)   # template output
    stored = faith_daily_pages.find_one(...)         # this seeder writes here
    return _merge(base, stored)                      # stored fields WIN

This seeder writes only the fields that drive L1 similarity:
  summary, gita_application, bible_application, guidance,
  month_focus, message

The Lumina verse cache is checked in lumina_router.py before live API calls.
Collection: lumina_verse_cache, keyed by {MODE}_{reference-slug}.

Phase scope (this script)
--------------------------
  faith_daily_pages   : 144 docs (12 signs x 12 months)   ~$0.05
  lumina_verse_cache  : 14 docs  (7 Bible + 7 Gita)        ~$0.004
  Total phase 1       : ~$0.06

Later phases (separate scripts):
  Phase 2: faith_transit_pages  (156 docs)   ~$0.05
  Phase 3: faith_bible_pages    (6,000 docs) ~$2.50
  Phase 4: faith_gita_pages     (10,500 docs) ~$4.00

Usage
-----
  # Full phase-1 run (daily + lumina):
  MONGO_URL="..." ANTHROPIC_API_KEY="sk-..." python3 scripts/seed_faith_daily_haiku.py --type all

  # Test: first 5 daily pages, no DB writes:
  ... python3 scripts/seed_faith_daily_haiku.py --limit 5 --dry-run

  # Daily pages only (default):
  ... python3 scripts/seed_faith_daily_haiku.py

  # Lumina verse cache only:
  ... python3 scripts/seed_faith_daily_haiku.py --type lumina

  # On Render shell:
  PYTHONPATH=/app python3 scripts/seed_faith_daily_haiku.py --type all
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path

import anthropic
from motor.motor_asyncio import AsyncIOMotorClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from faith_seo_data import SIGN_INDEX, MONTH_INDEX, build_daily_pages
from lumina_prompt_service import DAILY_SCRIPTURES, _daily_fallback

HAIKU_MODEL = "claude-3-5-haiku-20241022"
CONCURRENT = 5          # conservative: avoids Haiku rate-limit bursts
_JSON_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)


# ── Prompt builders ──────────────────────────────────────────────────────────

def _build_daily_prompt(page: dict) -> str:
    sign = SIGN_INDEX[page["sign_slug"]]
    month = MONTH_INDEX[page["month_slug"]]
    sign_name = sign["name"]
    month_name = month["name"]
    element = sign["element"]
    ruler = sign["ruler"]
    growth_edge = sign["growth_edge"]
    seasonal_focus = sign["seasonal_focus"]
    daily_practice = sign["daily_practice"]
    month_energy = month["month_energy"]
    seasonal_note = month["seasonal_note"]
    gita_ref = page["gita_reference"]
    gita_text = page["gita_text"]
    bible_ref = page["bible_reference"]
    bible_text = page["bible_text"]

    return (
        "You write unique SEO spiritual content for a Faith devotional website.\n"
        "Every sentence must be SPECIFIC to this exact sign-month combination -- nothing interchangeable with any other page.\n\n"
        f"PAGE: {sign_name} x {month_name}\n"
        f"Sign: {element} element, ruled by {ruler}\n"
        f"Sign growth edge: {growth_edge}\n"
        f"Sign seasonal focus: {seasonal_focus}\n"
        f"Sign daily practice: {daily_practice}\n"
        f"Month energy: {month_energy}\n"
        f"Month seasonal note: {seasonal_note}\n\n"
        f"Gita verse assigned: {gita_ref}\n"
        f'Gita text: "{gita_text}"\n\n'
        f"Bible verse assigned: {bible_ref}\n"
        f'Bible text: "{bible_text}"\n\n'
        "Return valid JSON only (no markdown fences, no extra keys):\n"
        "{\n"
        f'  "summary": "90-105 words. What {month_name} means spiritually for {sign_name}. Name {element} energy and this exact month energy explicitly. No generic forecast language.",\n'
        f'  "gita_application": "70-85 words. How {gita_ref} shapes {sign_name} behavior in {month_name}. Use at least one phrase from the verse text. Tie to: {growth_edge}.",\n'
        f'  "bible_application": "70-85 words. How {bible_ref} speaks to {sign_name} in {month_name}. Use at least one phrase from the verse text. Tie to: {seasonal_focus}.",\n'
        f'  "month_focus": "80-95 words. Primary spiritual training for {sign_name} this month. Name {growth_edge} and {month_energy} explicitly. Practical, not poetic."\n'
        "}"
    )


def _build_lumina_prompt(scripture_mode: str, verse: dict) -> str:
    tradition = (
        "Vedic-Bhagavad Gita tradition. Treat the verse as dharmic teaching: disciplined action, inner steadiness, and devotion without attachment to outcomes."
        if scripture_mode == "GITA"
        else "Biblical pastoral tradition. Theologically precise, Spirit-led, emotionally warm. The verse is a covenant promise."
    )
    ref = verse["reference"]
    text = verse["text"]

    return f"""You write the Lumina daily scripture breakdown for Everyday Horoscope.
Tone: pastoral, warm, scripture-grounded, theologically precise.
Tradition: {tradition}

Verse reference: {ref}
Verse text: "{text}"

Return valid JSON only (no markdown fences):
{{
  "verse_reference": "{ref}",
  "verse_text": "{text}",
  "revelation_context": "2-3 sentences. Historical and theological context of this exact verse.",
  "speak_it": "1 sentence. The reader speaks this aloud as a faith declaration. First person, present tense.",
  "think_it": "1-2 sentences. How to carry this verse as a meditative thought through the day.",
  "do_it": "1-2 sentences. One concrete obedient action this verse calls for today.",
  "prophets_promise": "1-2 sentences. The covenant or dharmic promise embedded in this verse.",
  "daily_application": "2-3 sentences. How this verse meets the reader in an ordinary day right now."
}}"""


# ── Low-level API call ───────────────────────────────────────────────────────

async def _call(
    client: anthropic.AsyncAnthropic,
    prompt: str,
    label: str,
    semaphore: asyncio.Semaphore,
) -> dict | None:
    async with semaphore:
        try:
            response = await client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=900,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = _JSON_FENCE.sub("", response.content[0].text).strip()
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"  ❌ JSON parse error [{label}]: {exc}")
            return None
        except anthropic.RateLimitError:
            print(f"  ⚠️  Rate limit hit [{label}] -- retrying after 10s")
            await asyncio.sleep(10)
            return None
        except Exception as exc:
            print(f"  ❌ API error [{label}]: {exc}")
            return None


# ── DAILY seeder ─────────────────────────────────────────────────────────────

async def seed_daily(
    client: anthropic.AsyncAnthropic,
    collection,
    pages: list[dict],
    semaphore: asyncio.Semaphore,
    dry_run: bool,
) -> tuple[int, int, int]:
    inserted = skipped = errors = 0

    async def _one(page: dict) -> None:
        nonlocal inserted, skipped, errors
        s, m = page["sign_slug"], page["month_slug"]
        label = f"{s}/{m}"

        if not dry_run:
            doc = await collection.find_one({"sign_slug": s, "month_slug": m}, {"ai_generated": 1})
            if doc and doc.get("ai_generated"):
                skipped += 1
                print(f"  ↷  {label} -- already seeded")
                return

        prompt = _build_daily_prompt(page)
        content = await _call(client, prompt, label, semaphore)

        if content is None:
            errors += 1
            return

        gita_app = str(content.get("gita_application") or "").strip()
        bible_app = str(content.get("bible_application") or "").strip()
        doc = {
            "sign_slug": s,
            "month_slug": m,
            "summary": str(content.get("summary") or "").strip(),
            "gita_application": gita_app,
            "bible_application": bible_app,
            "guidance": f"{gita_app} {bible_app}".strip(),
            "month_focus": str(content.get("month_focus") or "").strip(),
            "message": str(content.get("month_focus") or "").strip(),
            "ai_generated": True,
            "model": HAIKU_MODEL,
        }

        if dry_run:
            print(f"  [dry-run] {label}")
            summary_preview = doc["summary"][:90]
            print(f"    summary     : {summary_preview}...")
            print(f"    gita_app    : {gita_app[:60]}...")
            print(f"    bible_app   : {bible_app[:60]}...")
            inserted += 1
        else:
            await collection.update_one(
                {"sign_slug": s, "month_slug": m},
                {"$set": doc},
                upsert=True,
            )
            print(f"  ✓  {label}")
            inserted += 1

    await asyncio.gather(*[_one(p) for p in pages])
    return inserted, skipped, errors


# ── Lumina verse cache seeder ────────────────────────────────────────────────

def _verse_cache_key(scripture_mode: str, reference: str) -> str:
    slug = reference.lower().replace(" ", "-").replace(":", "-")
    return f"{scripture_mode}_{slug}"


async def seed_lumina(
    client: anthropic.AsyncAnthropic,
    collection,
    semaphore: asyncio.Semaphore,
    dry_run: bool,
) -> tuple[int, int, int]:
    inserted = skipped = errors = 0
    all_verses = (
        [("BIBLE", v) for v in DAILY_SCRIPTURES["BIBLE"]]
        + [("GITA", v) for v in DAILY_SCRIPTURES["GITA"]]
    )

    async def _one(mode: str, verse: dict) -> None:
        nonlocal inserted, skipped, errors
        cache_key = _verse_cache_key(mode, verse["reference"])
        label = f"{mode}/{verse['reference']}"

        if not dry_run:
            doc = await collection.find_one({"cache_key": cache_key}, {"ai_generated": 1})
            if doc and doc.get("ai_generated"):
                skipped += 1
                print(f"  ↷  {label} -- already cached")
                return

        prompt = _build_lumina_prompt(mode, verse)
        content = await _call(client, prompt, label, semaphore)

        if content is None:
            errors += 1
            return

        # Required fields -- fall back to static fallback so doc is always complete
        fallback = _daily_fallback(mode)
        required = ("verse_reference", "verse_text", "revelation_context",
                     "speak_it", "think_it", "do_it", "prophets_promise", "daily_application")
        doc = {
            "cache_key": cache_key,
            "scripture_mode": mode,
            "ai_generated": True,
            "model": HAIKU_MODEL,
            **{k: str(content.get(k) or fallback.get(k, "")) for k in required},
        }

        if dry_run:
            print(f"  [dry-run] {label}")
            print(f"    speak_it : {doc['speak_it'][:80]}...")
            inserted += 1
        else:
            await collection.update_one(
                {"cache_key": cache_key},
                {"$set": doc},
                upsert=True,
            )
            print(f"  ✓  {label}")
            inserted += 1

    await asyncio.gather(*[_one(mode, verse) for mode, verse in all_verses])
    return inserted, skipped, errors


# ── Entry point ──────────────────────────────────────────────────────────────

async def _run(args: argparse.Namespace) -> None:
    client = anthropic.AsyncAnthropic(api_key=args.api_key)
    motor_client = AsyncIOMotorClient(args.mongo_url)
    db = motor_client[args.db_name]
    semaphore = asyncio.Semaphore(CONCURRENT)

    do_daily = args.type in ("daily", "all")
    do_lumina = args.type in ("lumina", "all")

    # ── Phase 1A: DAILY ──────────────────────────────────────────────────────
    if do_daily:
        print(f"\n{'─'*60}")
        print("Phase 1A  →  faith_daily_pages  (144 pages)")
        print(f"Model: {HAIKU_MODEL}  |  Concurrent: {CONCURRENT}")
        if args.dry_run:
            print("DRY RUN -- no writes to MongoDB")
        print(f"{'─'*60}")

        pages = build_daily_pages()
        if args.limit:
            pages = pages[: args.limit]
            print(f"(Limited to first {args.limit} pages for testing)")

        coll = db.faith_daily_pages
        await coll.create_index(
            [("sign_slug", 1), ("month_slug", 1)], unique=True, background=True
        )

        ins, skp, err = await seed_daily(client, coll, pages, semaphore, args.dry_run)
        print(f"\n  DAILY  ✓{ins} seeded  ↷{skp} skipped  ❌{err} errors")

    # ── Phase 1B: LUMINA VERSE CACHE ─────────────────────────────────────────
    if do_lumina:
        print(f"\n{'─'*60}")
        print("Phase 1B  →  lumina_verse_cache  (14 verses: 7 Bible + 7 Gita)")
        print(f"Model: {HAIKU_MODEL}  |  Concurrent: {CONCURRENT}")
        if args.dry_run:
            print("DRY RUN -- no writes to MongoDB")
        print(f"{'─'*60}")

        coll = db.lumina_verse_cache
        await coll.create_index("cache_key", unique=True, background=True)

        ins, skp, err = await seed_lumina(client, coll, semaphore, args.dry_run)
        print(f"\n  LUMINA  ✓{ins} seeded  ↷{skp} skipped  ❌{err} errors")

    motor_client.close()
    print("\n✅  Done.\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed Faith DAILY pages + Lumina verse cache via Claude Haiku."
    )
    parser.add_argument(
        "--mongo-url",
        default=os.environ.get("MONGO_URL"),
        help="MongoDB connection string (or set MONGO_URL env var)",
    )
    parser.add_argument(
        "--db-name",
        default=os.environ.get("DB_NAME", "horoscope_db"),
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("ANTHROPIC_API_KEY"),
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)",
    )
    parser.add_argument(
        "--type",
        choices=["daily", "lumina", "all"],
        default="daily",
        help="Which phase to seed (default: daily)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit DAILY pages to first N (for smoke-testing, e.g. --limit 5)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate + print content without writing to MongoDB",
    )

    args = parser.parse_args()

    missing = []
    if not args.mongo_url:
        missing.append("MONGO_URL (--mongo-url or env var)")
    if not args.api_key:
        missing.append("ANTHROPIC_API_KEY (--api-key or env var)")
    if missing:
        for m in missing:
            print(f"ERROR: missing {m}")
        sys.exit(1)

    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
