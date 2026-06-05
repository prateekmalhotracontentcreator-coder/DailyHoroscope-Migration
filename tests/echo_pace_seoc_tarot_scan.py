#!/usr/bin/env python3
"""
ECHO/PACE 3-Layer Scanner -- SEO-C Series + Tarot SEO (TAR-SEO-1/2)
====================================================================
SEO-C pages (~17 editorial/hub pages across 8 commissions):
  C1  Legal pages        (5 pages)  -- noindex, excluded from scan
  C2  Rashi + Nakshatra  (2 pages)  -- static meta layer
  C3  Name Compatibility (1 page)   -- static meta layer
  C4  Ekadashi/Amav/Purn (3 pages)  -- static meta + description
  C5  Marriage Muhurat   (1 page)   -- static meta layer
  C6  Report Categories  (4 pages)  -- static meta layer
  C7  Celebrity Hub      (2 pages)  -- static meta layer
  C8  Love Calculator    (1 page)   -- static meta layer
  C9  Angel Numbers Hub  (1 page)   -- static meta layer

Tarot SEO (TAR-SEO-1/2):
  Spreads    (100 pages) -- tarot_seo_data.get_spread()
  Cards      (78 pages)  -- tarot_seo_data.get_card()
  Intentions (20 pages)  -- tarot_seo_data.get_intention()

PAID API MAP:
  All SEO-C pages  → NO  (static content / pyswisseph / MongoDB read)
  All Tarot pages  → NO  (static data generator, no LLM on render)

USAGE
-----
  cd /path/to/DailyHoroscope-Migration
  python tests/echo_pace_seoc_tarot_scan.py
  SERPER_API_KEY=xxx python tests/echo_pace_seoc_tarot_scan.py
"""
from __future__ import annotations

import json, os, re, sys
from collections import Counter
from itertools import combinations

_BACKEND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _BACKEND)

from tarot_seo_data import (
    list_spread_summaries, get_spread,
    list_card_summaries, get_card,
    list_intention_summaries, get_intention,
)

STOP = set("a an the is are was were be been being have has had do does did will would could should may might shall can need am i we you he she it they them their this that these those of in on at to for with by from about as into through during before after above below between but or and not no nor so yet both either neither each every all any few more most other some such only own same than too very just".split())

# ── ECHO/PACE core ─────────────────────────────────────────────────────────────

def _tok(text: str) -> list[str]:
    return [w for w in re.sub(r"[^a-z\s]", " ", text.lower()).split() if len(w) > 2]

def _tfidf_score(texts: list[str], labels: list[str]) -> tuple[float, str, str]:
    from math import log, sqrt
    n = len(texts)
    if n < 2:
        return 0.0, "", ""
    tok = [_tok(t) for t in texts]
    df: Counter[str] = Counter()
    for toks in tok:
        for w in set(toks):
            df[w] += 1
    idf = {w: log(n / df[w]) for w in df}
    vecs = [{w: (Counter(t)[w] / max(len(t), 1)) * idf[w] for w in Counter(t)} for t in tok]
    worst, wli, wlj = 0.0, "", ""
    from math import sqrt
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
        for g in set(ngrams(_tok(text))):
            gram_docs[g] += 1
    return sorted([(g, c/total) for g, c in gram_docs.items() if c/total > threshold], key=lambda x: -x[1])[:10]

def _jaccard_check(titles: list[str], threshold: float = 0.60) -> list[tuple[str, str, float]]:
    sets = [set(_tok(t)) - STOP for t in titles]
    viols = []
    for i, j in combinations(range(len(sets)), 2):
        u = sets[i] | sets[j]
        sc = len(sets[i] & sets[j]) / len(u) if u else 0
        if sc > threshold:
            viols.append((titles[i], titles[j], sc))
    return sorted(viols, key=lambda x: -x[2])[:10]

def _layer_g(samples: list[tuple[str, str]]) -> None:
    import urllib.request
    key = os.environ.get("SERPER_API_KEY", "")
    if not key:
        return
    print("\n── Layer G: Google Serper spot-check ────────────────────────")
    for phrase, label in samples:
        phrase = phrase[:110].strip()
        rb = json.dumps({"q": f'"{phrase}"', "num": 10}).encode()
        req = urllib.request.Request("https://google.serper.dev/search", data=rb,
                                     headers={"X-API-KEY": key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                hits = len(json.loads(r.read()).get("organic", []))
                st = "BLOCKED ❌" if hits > 4 else ("WATCH ⚠️" if hits > 1 else "PASS ✅")
                print(f"  [{st}] hits={hits:2d} | {label}: {phrase[:55]}")
        except Exception as e:
            print(f"  ERROR: {e}")

def _scan(docs: list[dict], body_fn, title_fn, label: str,
          layer_g_samples: list | None = None) -> dict:
    if len(docs) < 2:
        print(f"\n── {label} ({len(docs)} pages) ── SKIP (< 2 pages, no L1/L2/L3 meaningful)")
        return {"label": label, "n": len(docs), "l1": {"score": 0, "status": "N/A"}, "l2": {"violations": 0, "status": "N/A"}, "l3": {"violations": 0, "status": "N/A"}}
    bodies = [body_fn(d) for d in docs]
    titles = [title_fn(d) for d in docs]
    labels = [title_fn(d)[:50] for d in docs]

    worst, wli, wlj = _tfidf_score(bodies, labels)
    l1st = "BLOCKED ❌" if worst >= 0.70 else ("FLAGGED ⚠️" if worst >= 0.50 else "PASS ✅")
    viols_l2 = _ngram_check(bodies)
    l2st = "PASS ✅" if not viols_l2 else "FAIL ❌"
    viols_l3 = _jaccard_check(titles)
    l3st = "PASS ✅" if not viols_l3 else "FLAGGED ⚠️"

    print(f"\n── {label} ({len(docs)} pages) ──────────────────")
    print(f"  L1: {worst:.1%}  {l1st}")
    if worst >= 0.50:
        print(f"     Worst: {wli[:60]!r}")
        print(f"       vs:  {wlj[:60]!r}")
    print(f"  L2: {len(viols_l2)} violations  {l2st}")
    for g, pct in viols_l2[:3]:
        print(f"     {g!r:55s} {pct:.0%}")
    print(f"  L3: {len(viols_l3)} pairs > 60%  {l3st}")
    for t1, t2, j in viols_l3[:3]:
        print(f"     {t1[:40]!r} vs {t2[:40]!r} = {j:.0%}")

    if layer_g_samples and os.environ.get("SERPER_API_KEY"):
        _layer_g(layer_g_samples)

    return {
        "label": label, "n": len(docs),
        "l1": {"score": round(worst, 4), "status": l1st},
        "l2": {"violations": len(viols_l2), "status": l2st, "top": [g for g, _ in viols_l2[:3]]},
        "l3": {"violations": len(viols_l3), "status": l3st},
    }

# ── SEO-C static page definitions ─────────────────────────────────────────────
SEO_C_PAGES = [
    # C2 -- Calculators
    {"commission": "SEO-C2", "meta_title": "Rashi Calculator - Find Your Vedic Moon Sign",
     "body": "Find your Rashi (Vedic moon sign) instantly with our free calculator. Enter your birth date, time, and place to discover your moon sign, its ruling planet, nakshatra, and Vedic personality insights."},
    {"commission": "SEO-C2", "meta_title": "Nakshatra Calculator - Find Your Birth Star",
     "body": "Discover your Nakshatra (birth star) with our free Vedic astrology calculator. Enter your birth details to get your Nakshatra, ruling deity, planetary lord, gana, and compatibility insights."},
    # C3 -- Name Compatibility
    {"commission": "SEO-C3", "meta_title": "Name Compatibility Calculator - Vedic Numerology Match",
     "body": "Calculate name compatibility using Vedic numerology. Enter two names to find your numerological match score, destiny number alignment, and cosmic relationship reading."},
    # C4 -- Devotional dates
    {"commission": "SEO-C4", "meta_title": "Ekadashi 2026 - Next Date, Fasting Rules and Significance",
     "body": "Ekadashi falls on the 11th lunar day of both the waxing and waning moon. In Vaishnava practice it is one of the most respected fasting observances for purification, devotion, and mental discipline. When is the next Ekadashi in 2026? Get the exact date, Panchang details, fasting rules, and what to eat and avoid during Ekadashi vrat."},
    {"commission": "SEO-C4", "meta_title": "Amavasya 2026 - Next Date, Rituals and Puja Muhurat",
     "body": "Amavasya is the new moon day and the final tithi of the lunar month. It is widely observed for ancestor remembrance, introspection, and quiet ritual work. When is the next Amavasya in 2026? Get the exact date, Pitru Tarpan muhurat, rituals and Panchang for Amavasya."},
    {"commission": "SEO-C4", "meta_title": "Purnima 2026 - Next Full Moon Date, Fasting and Significance",
     "body": "Purnima marks the full moon and the 15th tithi of the bright lunar fortnight. It is associated with fullness, clarity, devotion, and spiritually heightened lunar energy. When is the next Purnima in 2026? Get the date, Panchang, fasting rules and puja muhurat."},
    # C5 -- Marriage Muhurat
    {"commission": "SEO-C5", "meta_title": "Shubh Vivah Muhurat 2026 - Auspicious Hindu Marriage Dates",
     "body": "Complete list of auspicious Hindu marriage dates for 2026. Vedic Panchang-verified muhurat with Tithi, Nakshatra, and monthly breakdown for your wedding planning."},
    # C6 -- Report Categories
    {"commission": "SEO-C6", "meta_title": "Kundali Reports - Vedic Birth Chart Analysis",
     "body": "Explore our range of personalised Kundali reports. Get deep Vedic birth chart analysis covering your Lagna, planetary positions, dasha periods, and life predictions."},
    {"commission": "SEO-C6", "meta_title": "Career Astrology Reports - Vedic Career Guidance",
     "body": "Discover your career path through Vedic astrology. Our career reports analyse your 10th house, ruling planets, dasha periods, and professional strengths."},
    {"commission": "SEO-C6", "meta_title": "Love & Relationship Astrology Reports",
     "body": "Get personalised love and relationship insights through Vedic astrology. Our reports cover your 7th house, Venus placement, compatibility factors, and relationship timing."},
    {"commission": "SEO-C6", "meta_title": "Numerology Reports - Name & Birth Number Analysis",
     "body": "Uncover your life path through numerology. Our reports cover your destiny number, name number, personal year cycle, and karmic debt numbers."},
    # C7 -- Celebrity Hub
    {"commission": "SEO-C7", "meta_title": "Celebrity Horoscopes - Vedic Birth Charts",
     "body": "Explore Vedic birth charts of Bollywood stars, cricketers, politicians, and global icons. Calculated with KP Jyotish - Moon sign, Dasha, Nakshatra, and more."},
    {"commission": "SEO-C7", "meta_title": "Celebrity Vedic Horoscope - Full Birth Chart Analysis",
     "body": "View the complete Vedic birth chart for this celebrity. Includes Lagna, Moon sign, Nakshatra, current Dasha period, and planetary strengths calculated via KP Jyotish."},
    # C8 -- Love Calculator
    {"commission": "SEO-C8", "meta_title": "Love Compatibility Calculator - Vedic Numerology Match",
     "body": "Find your love compatibility score instantly. Enter two names or birth dates to calculate your cosmic connection - powered by Vedic numerology."},
    # C9 -- Angel Numbers Hub
    {"commission": "SEO-C9", "meta_title": "Angel Numbers Guide - Meanings, Messages & Symbolism",
     "body": "Your complete guide to angel numbers. Discover the spiritual meaning of repeating number sequences from 111 to 999. Understand the messages your guides are sending through numbers."},
]

def _seoc_body(d: dict) -> str:
    return d["body"]

def _seoc_title(d: dict) -> str:
    return d["meta_title"]

# ── Tarot body extractors ──────────────────────────────────────────────────────

def _spread_body(d: dict) -> str:
    parts = []
    for f in ("purpose", "how_to", "when_to_use", "chapter"):
        if d.get(f) and isinstance(d[f], str):
            parts.append(d[f])
    for pos in d.get("positions", []):
        if isinstance(pos, dict):
            parts.append(pos.get("meaning", "") or pos.get("theme", ""))
    for fq in d.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    sr = d.get("sample_reading", {})
    if isinstance(sr, dict):
        parts.extend(str(v) for v in sr.values() if isinstance(v, str))
    return " ".join(filter(None, parts))

def _spread_title(d: dict) -> str:
    return d.get("meta_title", d.get("title", ""))

def _card_body(d: dict) -> str:
    parts = []
    for f in ("upright", "reversed", "love", "career", "health", "imagery"):
        if d.get(f) and isinstance(d[f], str):
            parts.append(d[f])
    return " ".join(filter(None, parts))

def _card_title(d: dict) -> str:
    if d.get("meta_title"):
        return d["meta_title"]
    name = d.get("name", d.get("slug", ""))
    arcana = d.get("arcana", "")
    return f"{name} Tarot Card - {arcana} Meaning & Guide"

def _intention_body(d: dict) -> str:
    parts = []
    for f in ("intro", "sample_walkthrough"):
        if d.get(f) and isinstance(d[f], str):
            parts.append(d[f])
    for fq in d.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    for c in d.get("caution_cards", []):
        if isinstance(c, dict):
            parts.append(c.get("note", ""))
    return " ".join(filter(None, parts))

def _intention_title(d: dict) -> str:
    return d.get("meta_title", d.get("label", ""))

# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 68)
    print("ECHO // PACE Scan -- SEO-C Series + Tarot SEO (TAR-SEO-1/2)")
    print("L1: < 50% PASS | 50-69% FLAGGED | >= 70% BLOCKED")
    print("L2: no 4-gram in > 15% pages | L3: Jaccard < 60%")
    print("Paid API: All modules below → NO (static content / pyswisseph)")
    print("=" * 68)

    results = []

    # ── SEO-C: all pages pooled (14 pages excl legal noindex) ─────────────────
    print("\nScanning SEO-C editorial pool (14 pages)...")
    r = _scan(SEO_C_PAGES, _seoc_body, _seoc_title, "SEO-C ALL PAGES POOLED (14 pages)",
              layer_g_samples=[
                  (SEO_C_PAGES[0]["body"][:100], "Rashi Calculator"),
                  (SEO_C_PAGES[3]["body"][:100], "Ekadashi"),
              ])
    results.append(r)

    # ── SEO-C sub-groups (same-commission similarity check) ───────────────────
    from itertools import groupby
    for commission, group in groupby(SEO_C_PAGES, key=lambda d: d["commission"]):
        pages = list(group)
        if len(pages) < 2:
            continue
        r = _scan(pages, _seoc_body, _seoc_title, f"{commission} sub-group ({len(pages)} pages)")
        results.append(r)

    # ── Tarot: Spreads ────────────────────────────────────────────────────────
    print("\nBuilding Tarot Spread docs (100 pages)...")
    spread_docs = [get_spread(s["slug"]) for s in list_spread_summaries() if get_spread(s["slug"])]
    r = _scan(spread_docs, _spread_body, _spread_title, "TAROT SPREADS (100 pages)",
              layer_g_samples=[(_spread_body(spread_docs[0])[:100], spread_docs[0].get("meta_title","")[:50])])
    results.append(r)

    # ── Tarot: Cards ──────────────────────────────────────────────────────────
    print("\nBuilding Tarot Card docs (78 pages)...")
    card_docs = [get_card(c["slug"]) for c in list_card_summaries() if get_card(c["slug"])]
    r = _scan(card_docs, _card_body, _card_title, "TAROT CARDS (78 pages)",
              layer_g_samples=[(_card_body(card_docs[0])[:100], _card_title(card_docs[0])[:50])])
    results.append(r)

    # ── Tarot: Intentions ─────────────────────────────────────────────────────
    print("\nBuilding Tarot Intention docs (20 pages)...")
    intent_docs = [get_intention(i["slug"]) for i in list_intention_summaries() if get_intention(i["slug"])]
    r = _scan(intent_docs, _intention_body, _intention_title, "TAROT INTENTIONS (20 pages)")
    results.append(r)

    # ── Global summary ────────────────────────────────────────────────────────
    print("\n" + "=" * 68)
    print("GLOBAL SUMMARY")
    print("=" * 68)
    print(f"{'Module':<45} {'L1':>7} {'L1 Status':>15} {'L2':>6} {'L3':>6}")
    print("-" * 68)
    for r in results:
        l1 = f"{r['l1']['score']:.1%}" if isinstance(r['l1']['score'], float) and r['l1']['score'] > 0 else "N/A"
        print(f"{r['label'][:45]:<45} {l1:>7} {r['l1']['status']:>15} {r['l2']['violations']:>6} {r['l3']['violations']:>6}")
    print("=" * 68)

if __name__ == "__main__":
    main()
