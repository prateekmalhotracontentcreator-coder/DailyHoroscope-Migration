#!/usr/bin/env python3
"""
ECHO/PACE 3-Layer Scanner -- Faith & Scripture SEO Module (FAITH-20K)
=====================================================================
Scans all 4 Faith page types against L1/L2/L3 quality gates.

Page types:
  gita    (10,500 pages) -- sampled: 5 chapters x 15 situations = 75
  bible   (6,000 pages)  -- sampled: 10 topics x 10 transitions = 100
  transit (156 pages)    -- all
  daily   (144 pages)    -- all

USAGE
-----
  cd /path/to/DailyHoroscope-Migration
  python tests/echo_pace_faith_scan.py
  SERPER_API_KEY=xxx python tests/echo_pace_faith_scan.py   # Layer G
"""
from __future__ import annotations

import json, os, re, sys, random
from collections import Counter
from itertools import combinations
from math import log, sqrt

_BACKEND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _BACKEND)

from faith_gita_data import build_gita_pages, GITA_SITUATIONS, CHAPTER_TITLES
from faith_bible_data import build_bible_pages, BIBLE_TOPICS, TRANSITIONS
from faith_seo_data import build_transit_pages, build_daily_pages

STOP = set("a an the is are was were be been being have has had do does did will would could should may might shall can need am i we you he she it they them their this that these those of in on at to for with by from about as into through during before after above below between but or and not no nor so yet both either neither each every all any few more most other some such only own same than too very just".split())

# ── Body extractors ───────────────────────────────────────────────────────────

def _gita_body(page: dict) -> str:
    parts = []
    for f in ("summary", "hook", "application", "etymology_intro"):
        if page.get(f) and isinstance(page[f], str):
            parts.append(page[f])
    for item in page.get("etymology_items", []):
        if isinstance(item, dict):
            parts.append(item.get("meaning", "") or item.get("text", ""))
    for fq in page.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    for pp in page.get("practice_prompts", []):
        if isinstance(pp, str):
            parts.append(pp)
    return " ".join(filter(None, parts))

def _bible_body(page: dict) -> str:
    parts = []
    for f in ("summary", "hook", "application", "message", "body", "guidance", "intro"):
        if page.get(f) and isinstance(page[f], str):
            parts.append(page[f])
    for fq in page.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    return " ".join(filter(None, parts))

def _transit_body(page: dict) -> str:
    parts = []
    for f in ("summary", "guidance", "message", "body", "intro", "application"):
        if page.get(f) and isinstance(page[f], str):
            parts.append(page[f])
    for fq in page.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    return " ".join(filter(None, parts))

def _daily_body(page: dict) -> str:
    parts = []
    for f in ("summary", "message", "guidance", "body", "intro", "reflection"):
        if page.get(f) and isinstance(page[f], str):
            parts.append(page[f])
    return " ".join(filter(None, parts))

def _title(page: dict) -> str:
    return page.get("meta_title", page.get("title", ""))

# ── Core ECHO/PACE ────────────────────────────────────────────────────────────

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
        na = sqrt(sum(v**2 for v in a.values()))
        nb = sqrt(sum(v**2 for v in b.values()))
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
    return sorted([(g, c/total) for g, c in gram_docs.items() if c/total > threshold], key=lambda x: -x[1])[:10]

def _jaccard_check(titles: list[str], threshold: float = 0.60) -> list[tuple[str, str, float]]:
    sets = [set(_tokenise(t)) - STOP for t in titles]
    violations = []
    for i, j in combinations(range(len(sets)), 2):
        u = sets[i] | sets[j]
        score = len(sets[i] & sets[j]) / len(u) if u else 0
        if score > threshold:
            violations.append((titles[i], titles[j], score))
    return sorted(violations, key=lambda x: -x[2])[:10]

def scan_type(pages: list[dict], body_fn, label: str, sample_n: int | None = None) -> dict:
    if sample_n and len(pages) > sample_n:
        random.seed(42)
        pages = random.sample(pages, sample_n)

    bodies = [body_fn(p) for p in pages]
    titles = [_title(p) for p in pages]
    labels = [_title(p)[:50] for p in pages]

    worst_l1, wli, wlj = _tfidf_score(bodies, labels)
    l1_status = "BLOCKED ❌" if worst_l1 >= 0.70 else ("FLAGGED ⚠️" if worst_l1 >= 0.50 else "PASS ✅")

    violations_l2 = _ngram_check(bodies)
    l2_status = "PASS ✅" if not violations_l2 else "FAIL ❌"

    violations_l3 = _jaccard_check(titles)
    l3_status = "PASS ✅" if not violations_l3 else "FLAGGED ⚠️"

    print(f"\n── {label} ──────────────────")
    print(f"  L1 TF-IDF worst pair: {worst_l1:.1%}  {l1_status}")
    if worst_l1 >= 0.50:
        print(f"     Worst: {wli[:55]!r}")
        print(f"       vs: {wlj[:55]!r}")
    print(f"  L2 N-gram violations: {len(violations_l2)}  {l2_status}")
    for g, pct in violations_l2[:3]:
        print(f"     {g!r:55s} {pct:.0%}")
    print(f"  L3 Jaccard title pairs > 60%: {len(violations_l3)}  {l3_status}")
    for t1, t2, j in violations_l3[:3]:
        print(f"     {t1[:45]!r} vs {t2[:45]!r} = {j:.0%}")

    return {
        "label": label, "sampled": len(pages),
        "l1": {"worst": round(worst_l1, 4), "status": l1_status},
        "l2": {"violations": len(violations_l2), "status": l2_status, "top": [g for g, _ in violations_l2[:5]]},
        "l3": {"violations": len(violations_l3), "status": l3_status},
    }

def _layer_g(samples: list[tuple[str, str]]) -> None:
    import urllib.request
    key = os.environ.get("SERPER_API_KEY", "")
    if not key:
        return
    print("\n── Layer G: Google Serper spot-check ────────────────────────")
    for phrase, label in samples:
        phrase = phrase[:120].strip()
        req_body = json.dumps({"q": f'"{phrase}"', "num": 10}).encode()
        req = urllib.request.Request(
            "https://google.serper.dev/search",
            data=req_body,
            headers={"X-API-KEY": key, "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
                hits = len(data.get("organic", []))
                status = "BLOCKED ❌" if hits > 4 else ("WATCH ⚠️" if hits > 1 else "PASS ✅")
                print(f"  [{status}] hits={hits:2d} | {label}: {phrase[:55]}")
        except Exception as e:
            print(f"  ERROR: {e}")

def main() -> None:
    print("=" * 65)
    print("ECHO // PACE Compliance Scan -- Faith & Scripture (FAITH-20K)")
    print("L1 gate: < 50% PASS | 50-69% FLAGGED | >= 70% BLOCKED")
    print("L2 gate: no 4-gram in > 15% of pages")
    print("L3 gate: title Jaccard < 60%")
    print("=" * 65)

    print("\nBuilding page sets (may take a few seconds)...")
    gita_pages = build_gita_pages()
    bible_pages = build_bible_pages()
    transit_pages = build_transit_pages()
    daily_pages = build_daily_pages()

    print(f"  Gita: {len(gita_pages):,}  Bible: {len(bible_pages):,}  Transit: {len(transit_pages)}  Daily: {len(daily_pages)}")

    results = []

    # Gita -- sample cross-situation to catch within-situation repetition
    # Sample strategy: for each of 5 chapters, take all 15 situations
    random.seed(42)
    chapters_sample = list(range(1, min(19, len(CHAPTER_TITLES)+1)))[:5]
    gita_sample = [p for p in gita_pages if p.get("chapter") in chapters_sample]
    results.append(scan_type(gita_sample, _gita_body, f"GITA pages (sample: {len(gita_sample)} of {len(gita_pages):,})", sample_n=100))

    # Bible -- sample: 10 topics x 10 transitions
    topic_slugs = list({p["topic_slug"] for p in bible_pages})[:10]
    trans_slugs = list({p["transition_slug"] for p in bible_pages})[:10]
    bible_sample = [p for p in bible_pages if p["topic_slug"] in topic_slugs and p["transition_slug"] in trans_slugs]
    results.append(scan_type(bible_sample, _bible_body, f"BIBLE pages (sample: {len(bible_sample)} of {len(bible_pages):,})", sample_n=100))

    # Transit + Daily -- all pages
    results.append(scan_type(transit_pages, _transit_body, f"TRANSIT pages ({len(transit_pages)})"))
    results.append(scan_type(daily_pages, _daily_body, f"DAILY pages ({len(daily_pages)})"))

    # Layer G
    if os.environ.get("SERPER_API_KEY"):
        g_samples = []
        if gita_pages:
            p = gita_pages[0]
            g_samples.append((_gita_body(p)[:120], f"Gita {p.get('reference','')}/{p.get('situation_slug','')}"))
        if bible_pages:
            p = bible_pages[0]
            g_samples.append((_bible_body(p)[:120], f"Bible {p.get('topic_slug','')}/{p.get('transition_slug','')}"))
        if transit_pages:
            p = transit_pages[0]
            g_samples.append((_transit_body(p)[:120], f"Transit {p.get('id','')}"))
        _layer_g(g_samples)

    print("\n" + "=" * 65)
    all_l1 = [r["l1"]["worst"] for r in results]
    print(f"GLOBAL L1 WORST: {max(all_l1):.1%}  |  {'BLOCKED ❌' if max(all_l1) >= 0.70 else 'OK'}")
    print(f"L2 OVERALL: {'FAIL ❌' if any(r['l2']['violations'] > 0 for r in results) else 'PASS ✅'}")
    print(f"L3 OVERALL: {'FLAGGED ⚠️' if any(r['l3']['violations'] > 0 for r in results) else 'PASS ✅'}")
    print("=" * 65)

if __name__ == "__main__":
    main()
