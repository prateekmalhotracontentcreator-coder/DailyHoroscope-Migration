#!/usr/bin/env python3
"""
echo_pace_faith_daily_mongo.py
==============================
ECHO/PACE scanner for Faith DAILY pages -- reads AI-seeded content from
MongoDB and merges it with template output, exactly as the live router does.

Use this AFTER running the seeder (even a partial --limit N batch) to
validate the actual content users will see before running the full batch.

Scan logic (identical thresholds to all other Faith modules):
  L1  TF-IDF cosine  < 50%       PASS  (template alone was 91%)
  L2  4-gram repeat  0 violations PASS
  L3  Jaccard title  < 60%        PASS  (informational -- titles not seeded)

Usage
-----
  # After seeding any batch (e.g. --limit 5):
  MONGO_URL="..." python tests/echo_pace_faith_daily_mongo.py

  # Save log:
  MONGO_URL="..." python tests/echo_pace_faith_daily_mongo.py --log-file auto

  # Only test pages that have been AI-seeded (skip unseeded template pages):
  MONGO_URL="..." python tests/echo_pace_faith_daily_mongo.py --seeded-only
"""
from __future__ import annotations

import argparse
import asyncio
import os
import re
import sys
from collections import Counter
from datetime import datetime
from itertools import combinations
from math import log, sqrt
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient

_BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(_BACKEND))

from faith_seo_data import build_daily_pages

# ── Stop words (identical to echo_pace_faith_scan.py) ────────────────────────

STOP = set("a an the is are was were be been being have has had do does did will would could should may might shall can need am i we you he she it they them their this that these those of in on at to for with by from about as into through during before after above below between but or and not no nor so yet both either neither each every all any few more most other some such only own same than too very just".split())

# ── Logging ───────────────────────────────────────────────────────────────────

_LOG_FILE: Path | None = None

def _log(msg: str = "") -> None:
    print(msg)
    if _LOG_FILE:
        with _LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(msg + "\n")


# ── Merge (mirrors faith_seo_router._merge) ───────────────────────────────────

_SEEDED_FIELDS = (
    "summary", "gita_application", "bible_application",
    "guidance", "month_focus", "message",
)

def _merge(template: dict, stored: dict | None) -> dict:
    """Stored MongoDB fields WIN over template output."""
    merged = dict(template)
    if stored:
        for field in _SEEDED_FIELDS:
            if stored.get(field):
                merged[field] = stored[field]
    return merged


# ── Body extractor (identical to echo_pace_faith_scan._daily_body) ────────────

def _daily_body(page: dict) -> str:
    parts = []
    for f in ("summary", "message", "guidance", "body", "intro", "reflection"):
        if page.get(f) and isinstance(page[f], str):
            parts.append(page[f])
    return " ".join(filter(None, parts))

def _title(page: dict) -> str:
    return page.get("meta_title", page.get("title", ""))


# ── ECHO/PACE core ────────────────────────────────────────────────────────────

def _tokenise(text: str) -> list[str]:
    return [w for w in re.sub(r"[^a-z\s]", " ", text.lower()).split() if len(w) > 2]

def _tfidf_score(texts: list[str], labels: list[str]) -> tuple[float, str, str]:
    n = len(texts)
    tokenised = [_tokenise(t) for t in texts]
    df: Counter[str] = Counter()
    for toks in tokenised:
        for w in set(toks):
            df[w] += 1
    idf = {w: log(n / df[w]) for w in df}
    vecs = [{w: (Counter(toks)[w] / max(len(toks), 1)) * idf[w]
             for w in Counter(toks)} for toks in tokenised]
    worst, wli, wlj = 0.0, "", ""
    for i, j in combinations(range(n), 2):
        a, b = vecs[i], vecs[j]
        dot = sum(a[w] * b.get(w, 0) for w in a)
        na  = sqrt(sum(v**2 for v in a.values()))
        nb  = sqrt(sum(v**2 for v in b.values()))
        if na and nb:
            sim = dot / (na * nb)
            if sim > worst:
                worst, wli, wlj = sim, labels[i], labels[j]
    return worst, wli, wlj

def _ngram_check(texts: list[str], n: int = 4, threshold: float = 0.15) -> list[tuple[str, float]]:
    def ngrams(toks):
        f = [w for w in toks if w not in STOP]
        return [" ".join(f[i:i+n]) for i in range(len(f) - n + 1)]
    gram_docs: Counter[str] = Counter()
    total = len(texts)
    for text in texts:
        for g in set(ngrams(_tokenise(text))):
            gram_docs[g] += 1
    return sorted(
        [(g, c / total) for g, c in gram_docs.items() if c / total > threshold],
        key=lambda x: -x[1],
    )[:10]

def _jaccard_check(titles: list[str], threshold: float = 0.60) -> list[tuple[str, str, float]]:
    sets = [set(_tokenise(t)) - STOP for t in titles]
    violations = []
    for i, j in combinations(range(len(sets)), 2):
        u = sets[i] | sets[j]
        score = len(sets[i] & sets[j]) / len(u) if u else 0
        if score > threshold:
            violations.append((titles[i], titles[j], score))
    return sorted(violations, key=lambda x: -x[2])[:10]

def run_echo_pace(pages: list[dict], label: str, seeded_count: int) -> dict:
    if len(pages) < 2:
        _log(f"\n⚠️  Only {len(pages)} page(s) -- need at least 2 for L1. Seed more pages first.")
        return {}

    bodies = [_daily_body(p) for p in pages]
    titles = [_title(p) for p in pages]
    labels = [f"{p['sign_slug']}/{p['month_slug']}" for p in pages]

    worst_l1, wli, wlj = _tfidf_score(bodies, labels)
    l1_pass   = worst_l1 < 0.50
    l1_status = "PASS ✅" if l1_pass else ("FLAGGED ⚠️" if worst_l1 < 0.70 else "BLOCKED ❌")

    violations_l2 = _ngram_check(bodies)
    l2_pass   = len(violations_l2) == 0
    l2_status = "PASS ✅" if l2_pass else "FAIL ❌"

    violations_l3 = _jaccard_check(titles)
    l3_pass   = len(violations_l3) == 0
    l3_status = "PASS ✅" if l3_pass else "FLAGGED ⚠️"

    _log(f"\n── {label} ──────────────────────────────────────────")
    _log(f"  Pages in corpus  : {len(pages)}  ({seeded_count} AI-seeded / {len(pages)-seeded_count} template only)")
    _log(f"  L1 TF-IDF worst  : {worst_l1:.1%}  {l1_status}  (template baseline: 91.1%)")
    if not l1_pass:
        _log(f"     Worst pair: {wli}")
        _log(f"             vs: {wlj}")
    _log(f"  L2 N-gram        : {len(violations_l2)} violations  {l2_status}")
    for g, pct in violations_l2[:5]:
        _log(f"     {g!r:55s} {pct:.0%}")
    _log(f"  L3 Jaccard       : {len(violations_l3)} pairs > 60%  {l3_status}  [informational -- FAITH-OP-8]")
    for t1, t2, j in violations_l3[:3]:
        _log(f"     {t1[:40]!r} vs {t2[:40]!r} = {j:.0%}")

    return {
        "pages": len(pages), "seeded": seeded_count,
        "l1": {"worst": round(worst_l1, 4), "pass": l1_pass, "status": l1_status},
        "l2": {"violations": len(violations_l2), "pass": l2_pass, "status": l2_status},
        "l3": {"violations": len(violations_l3), "pass": l3_pass, "status": l3_status},
    }


# ── Main ──────────────────────────────────────────────────────────────────────

async def _run(args: argparse.Namespace) -> None:
    global _LOG_FILE
    if args.log_file:
        _LOG_FILE = Path(args.log_file)
        _LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        _LOG_FILE.write_text(
            f"# Faith DAILY MongoDB ECHO/PACE -- {datetime.now().isoformat()}\n",
            encoding="utf-8",
        )
        _log(f"Log: {_LOG_FILE.resolve()}")

    _log("=" * 65)
    _log("ECHO // PACE -- Faith DAILY (MongoDB-merged)")
    _log("Reads AI content from faith_daily_pages, merges with template.")
    _log("=" * 65)

    # Load template pages
    template_pages = build_daily_pages()
    template_index = {(p["sign_slug"], p["month_slug"]): p for p in template_pages}
    _log(f"\nTemplate pages : {len(template_pages)}")

    # Pull seeded docs from MongoDB
    motor = AsyncIOMotorClient(args.mongo_url)
    db    = motor[args.db_name]
    cursor = db.faith_daily_pages.find(
        {"ai_generated": True},
        {f: 1 for f in ("sign_slug", "month_slug", *_SEEDED_FIELDS)},
    )
    stored_docs = await cursor.to_list(length=None)
    motor.close()

    seeded_count = len(stored_docs)
    _log(f"AI-seeded docs : {seeded_count} in faith_daily_pages")

    if seeded_count == 0:
        _log("\n⚠️  No AI-seeded documents found. Run the seeder first:")
        _log("    python backend/scripts/seed_faith_daily_haiku.py --limit 5")
        return

    # Build stored lookup
    stored_index = {
        (d["sign_slug"], d["month_slug"]): d for d in stored_docs
    }

    # Merge and optionally filter to seeded-only corpus
    if args.seeded_only:
        corpus = [
            _merge(template_index[(s, m)], stored_index[(s, m)])
            for (s, m) in stored_index
            if (s, m) in template_index
        ]
        label = f"DAILY -- AI-seeded pages only ({seeded_count})"
    else:
        corpus = [
            _merge(p, stored_index.get((p["sign_slug"], p["month_slug"])))
            for p in template_pages
        ]
        label = f"DAILY -- all 144 pages (merged)"

    if len(corpus) < 2:
        _log(f"\n⚠️  Only {len(corpus)} page(s) in corpus. Seed more pages or remove --seeded-only.")
        return

    result = run_echo_pace(corpus, label, seeded_count)

    if not result:
        return

    _log("\n" + "=" * 65)
    l1_ok = result["l1"]["pass"]
    l2_ok = result["l2"]["pass"]

    if seeded_count < len(template_pages):
        remaining = len(template_pages) - seeded_count
        _log(f"NOTE: {remaining} pages still on template. L1 score will improve as seeding completes.")

    _log(f"\nVERDICT  (based on {seeded_count}/{len(template_pages)} pages seeded):")
    _log(f"  L1: {result['l1']['status']}  ({result['l1']['worst']:.1%})")
    _log(f"  L2: {result['l2']['status']}  ({result['l2']['violations']} violations)")
    _log(f"  L3: {result['l3']['status']}  ({result['l3']['violations']} pairs)  [informational]")

    if l1_ok and l2_ok:
        if seeded_count < len(template_pages):
            _log(f"\n✅  Partial batch PASS -- proceed with full seeder run:")
            _log( "    python backend/scripts/seed_faith_daily_haiku.py --type all --log-file auto")
        else:
            _log("\n✅  FULL BATCH PASS -- Faith DAILY seeding complete. FAITH-OP-3 RESOLVED.")
    else:
        _log("\n🔴  FAIL -- do NOT run full batch. Review violations above.")
    _log("=" * 65)

    if _LOG_FILE:
        print(f"\n📄 Full log saved → {_LOG_FILE.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ECHO/PACE scanner for Faith DAILY pages (MongoDB-merged)."
    )
    parser.add_argument(
        "--mongo-url",
        default=os.environ.get("MONGO_URL"),
    )
    parser.add_argument(
        "--db-name",
        default=os.environ.get("DB_NAME", "horoscope_db"),
    )
    parser.add_argument(
        "--seeded-only",
        action="store_true",
        help="Run L1/L2/L3 on AI-seeded pages only (excludes unseeded template pages). "
             "Useful for partial batches where template pages would inflate L1.",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        help="Save full output to file. Use 'auto' for timestamped name.",
    )

    args = parser.parse_args()

    if args.log_file == "auto":
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        args.log_file = str(
            Path(__file__).parent / "logs" / f"echo_faith_daily_mongo_{ts}.log"
        )

    if not args.mongo_url:
        print("ERROR: MONGO_URL not set (--mongo-url or env var)")
        sys.exit(1)

    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
