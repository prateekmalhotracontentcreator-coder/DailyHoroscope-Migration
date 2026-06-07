#!/usr/bin/env python3
"""
echo_pace_faith_daily_ai_preview.py
====================================
Pre-flight ECHO/PACE gate for the Faith DAILY AI seeder.

Generates all 144 DAILY pages via Claude Haiku IN MEMORY (no DB write),
merges AI-generated fields (summary / guidance / message) into the template
page, then runs L1 / L2 / L3 compliance checks on the MERGED result.

This is what real users will see after seeding -- the router overlays
stored fields on top of the template, so the merged page is the ground truth.

PASS criteria (same gates as all other Faith modules):
  L1  TF-IDF cosine < 50%       (was 91% with template alone)
  L2  0 four-gram violations     (template: PASS after Pass 5)
  L3  0 title Jaccard > 60%      (template: 77% FAIL -- titles unchanged)

Note: L3 will still reflect template title repetition (titles are not
seeded by this script). That is expected and tracked as FAITH-OP-8.

Usage
-----
  cd /path/to/DailyHoroscope-Migration
  ANTHROPIC_API_KEY="sk-..." python tests/echo_pace_faith_daily_ai_preview.py

  # Save output:
  ANTHROPIC_API_KEY="sk-..." python tests/echo_pace_faith_daily_ai_preview.py \
      --log-file tests/logs/echo_faith_daily_ai_YYYY-MM-DD.log

Cost: ~$0.10 for 144 pages (Haiku -- no DB writes, pure preflight check)
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from itertools import combinations
from math import log, sqrt
from pathlib import Path

import anthropic

_BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(_BACKEND))

from faith_seo_data import SIGN_INDEX, MONTH_INDEX, build_daily_pages

# ── Scanner constants (identical to echo_pace_faith_scan.py) ─────────────────

STOP = set("a an the is are was were be been being have has had do does did will would could should may might shall can need am i we you he she it they them their this that these those of in on at to for with by from about as into through during before after above below between but or and not no nor so yet both either neither each every all any few more most other some such only own same than too very just".split())

HAIKU_MODEL = "claude-haiku-4-5"
CONCURRENT  = 5
_JSON_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)

# ── Logging ───────────────────────────────────────────────────────────────────

_LOG_FILE: Path | None = None

def _log(msg: str = "") -> None:
    print(msg)
    if _LOG_FILE:
        with _LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(msg + "\n")


# ── Prompt builder (mirrors seed_faith_daily_haiku.py exactly) ───────────────

def _build_prompt(page: dict) -> str:
    sign        = SIGN_INDEX[page["sign_slug"]]
    month       = MONTH_INDEX[page["month_slug"]]
    sign_name   = sign["name"]
    month_name  = month["name"]
    element     = sign["element"]
    ruler       = sign["ruler"]
    growth_edge = sign["growth_edge"]
    seasonal_focus = sign["seasonal_focus"]
    daily_practice = sign["daily_practice"]
    month_energy   = month["month_energy"]
    seasonal_note  = month["seasonal_note"]
    gita_ref  = page["gita_reference"]
    gita_text = page["gita_text"]
    bible_ref  = page["bible_reference"]
    bible_text = page["bible_text"]

    return (
        "You write unique SEO spiritual content for a Faith devotional website.\n"
        "Every sentence must be SPECIFIC to this exact sign-month combination -- nothing interchangeable with any other page.\n\n"
        "CRITICAL RULE: The context fields below are THEMATIC GUIDANCE only. "
        "Do NOT quote, paraphrase, or echo their exact wording in your output. "
        "Generate your own fresh language that captures the same spirit.\n\n"
        f"PAGE: {sign_name} x {month_name}\n"
        f"Sign: {element} element, ruled by {ruler}\n"
        f"Sign growth theme: {growth_edge}\n"
        f"Sign seasonal focus: {seasonal_focus}\n"
        f"Sign daily practice theme: {daily_practice}\n"
        f"Month energy: {month_energy}\n"
        f"Month seasonal note: {seasonal_note}\n\n"
        f"Gita verse assigned: {gita_ref}\n"
        f'Gita text: "{gita_text}"\n\n'
        f"Bible verse assigned: {bible_ref}\n"
        f'Bible text: "{bible_text}"\n\n'
        "Return valid JSON only (no markdown fences, no extra keys):\n"
        "{\n"
        f'  "summary": "90-105 words. What {month_name} means spiritually for {sign_name}. Name {element} energy and this month\'s specific energy. No generic forecast language. Your own words throughout.",\n'
        f'  "gita_application": "70-85 words. How {gita_ref} speaks to {sign_name}\'s core challenge in {month_name}. Quote at least one phrase from the verse text. Express the growth theme in your own language -- do not echo the context fields.",\n'
        f'  "bible_application": "70-85 words. How {bible_ref} addresses {sign_name}\'s seasonal focus in {month_name}. Quote at least one phrase from the verse text. Express the seasonal theme in your own language -- do not echo the context fields.",\n'
        f'  "month_focus": "80-95 words. The primary spiritual discipline for {sign_name} in {month_name}. Address the sign\'s core growth challenge and this month\'s energy -- expressed entirely in your own words. Practical, not poetic."\n'
        "}"
    )


# ── AI call (mirrors seeder) ──────────────────────────────────────────────────

async def _call(client, prompt: str, label: str, sem: asyncio.Semaphore) -> dict | None:
    async with sem:
        try:
            resp = await client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=900,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = _JSON_FENCE.sub("", resp.content[0].text).strip()
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            _log(f"  ❌ JSON parse [{label}]: {exc}")
            return None
        except anthropic.RateLimitError:
            _log(f"  ⚠️  Rate limit [{label}] -- retrying after 10s")
            await asyncio.sleep(10)
            return None
        except Exception as exc:
            _log(f"  ❌ API error [{label}]: {exc}")
            return None


# ── Generate + merge all 144 pages in memory ──────────────────────────────────

async def generate_merged_pages(
    api_key: str, template_pages: list[dict]
) -> list[dict]:
    client = anthropic.AsyncAnthropic(api_key=api_key)
    sem    = asyncio.Semaphore(CONCURRENT)

    merged: list[dict]        = [None] * len(template_pages)  # type: ignore[list-item]
    errors: list[str]         = []

    async def _one(idx: int, page: dict) -> None:
        label   = f"{page['sign_slug']}/{page['month_slug']}"
        content = await _call(client, _build_prompt(page), label, sem)
        if content is None:
            errors.append(label)
            merged[idx] = page          # fall back to raw template on error
            return

        gita_app  = str(content.get("gita_application") or "").strip()
        bible_app = str(content.get("bible_application") or "").strip()

        # Produce a merged dict exactly as the router would serve it
        m = dict(page)
        m["summary"]          = str(content.get("summary") or "").strip()
        m["gita_application"] = gita_app
        m["bible_application"]= bible_app
        m["guidance"]         = f"{gita_app} {bible_app}".strip()
        m["month_focus"]      = str(content.get("month_focus") or "").strip()
        m["message"]          = m["month_focus"]
        merged[idx] = m
        _log(f"  ✓ {label}")

    await asyncio.gather(*[_one(i, p) for i, p in enumerate(template_pages)])

    if errors:
        _log(f"\n  ⚠️  {len(errors)} pages fell back to template: {errors[:5]}")
    return merged


# ── ECHO / PACE layers (copied verbatim from echo_pace_faith_scan.py) ─────────

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
        dot  = sum(a[w] * b.get(w, 0) for w in a)
        na   = sqrt(sum(v**2 for v in a.values()))
        nb   = sqrt(sum(v**2 for v in b.values()))
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
    return sorted([(g, c/total) for g, c in gram_docs.items() if c/total > threshold],
                  key=lambda x: -x[1])[:10]

def _jaccard_check(titles: list[str], threshold: float = 0.60) -> list[tuple[str, str, float]]:
    sets = [set(_tokenise(t)) - STOP for t in titles]
    violations = []
    for i, j in combinations(range(len(sets)), 2):
        u = sets[i] | sets[j]
        score = len(sets[i] & sets[j]) / len(u) if u else 0
        if score > threshold:
            violations.append((titles[i], titles[j], score))
    return sorted(violations, key=lambda x: -x[2])[:10]

def _daily_body(page: dict) -> str:
    """Matches echo_pace_faith_scan._daily_body exactly."""
    parts = []
    for f in ("summary", "message", "guidance", "body", "intro", "reflection"):
        if page.get(f) and isinstance(page[f], str):
            parts.append(page[f])
    return " ".join(filter(None, parts))

def _title(page: dict) -> str:
    return page.get("meta_title", page.get("title", ""))

def run_echo_pace(pages: list[dict]) -> dict:
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

    _log(f"\n── DAILY pages (AI-merged, {len(pages)} pages) ──────────────────────────")
    _log(f"  L1 TF-IDF worst pair : {worst_l1:.1%}  {l1_status}  (template baseline was 91%)")
    if not l1_pass:
        _log(f"     Worst: {wli}")
        _log(f"       vs:  {wlj}")
    _log(f"  L2 N-gram violations : {len(violations_l2)}  {l2_status}")
    for g, pct in violations_l2[:5]:
        _log(f"     {g!r:55s} {pct:.0%}")
    _log(f"  L3 Jaccard > 60%     : {len(violations_l3)}  {l3_status}  (titles unchanged -- FAITH-OP-8)")
    for t1, t2, j in violations_l3[:3]:
        _log(f"     {t1[:45]!r} vs {t2[:45]!r} = {j:.0%}")

    return {
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
            f"# Faith DAILY AI ECHO/PACE Preview -- {datetime.now().isoformat()}\n",
            encoding="utf-8",
        )
        _log(f"Log: {_LOG_FILE.resolve()}")

    _log("=" * 65)
    _log("ECHO // PACE AI Preview -- Faith DAILY (144 pages)")
    _log("Generates content via Haiku in-memory. No DB writes.")
    _log("L1 gate: < 50%  |  L2 gate: 0 violations  |  L3 titles (informational)")
    _log("=" * 65)

    template_pages = build_daily_pages()
    _log(f"\nTemplate pages loaded: {len(template_pages)}")
    _log(f"Model: {HAIKU_MODEL}  |  Concurrent: {CONCURRENT}")
    _log(f"\nGenerating AI content for all {len(template_pages)} pages...\n")

    merged_pages = await generate_merged_pages(args.api_key, template_pages)

    result = run_echo_pace(merged_pages)

    _log("\n" + "=" * 65)
    l1_ok = result["l1"]["pass"]
    l2_ok = result["l2"]["pass"]
    _log(f"VERDICT:")
    _log(f"  L1: {result['l1']['status']}  ({result['l1']['worst']:.1%})")
    _log(f"  L2: {result['l2']['status']}  ({result['l2']['violations']} violations)")
    _log(f"  L3: {result['l3']['status']}  ({result['l3']['violations']} title pairs)  [informational]")

    if l1_ok and l2_ok:
        _log("\n✅  CLEAR TO SEED -- run the full batch:")
        _log("    PYTHONPATH=backend python backend/scripts/seed_faith_daily_haiku.py --type all --log-file auto")
    else:
        _log("\n🔴  DO NOT SEED -- fix violations above before running full batch.")
    _log("=" * 65)

    if _LOG_FILE:
        print(f"\n📄 Full log saved → {_LOG_FILE.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pre-flight ECHO/PACE gate for Faith DAILY AI seeder."
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("ANTHROPIC_API_KEY"),
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        help="Path to save full output log. Use 'auto' for timestamped name.",
    )
    args = parser.parse_args()

    if args.log_file == "auto":
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        args.log_file = str(
            Path(__file__).parent / "logs" / f"echo_faith_daily_ai_{ts}.log"
        )

    if not args.api_key:
        print("ERROR: ANTHROPIC_API_KEY not set (--api-key or env var)")
        sys.exit(1)

    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
