#!/usr/bin/env python3
"""
ECHO/PACE 3-Layer Scanner -- Tarot SEO Module
============================================

Runs all three quality layers against tarot_seo_data.py content and
produces a pass/fail report. New thread runs this script; TT reviews
the output -- no manual admin panel required.

LAYER 1  TF-IDF Cosine (inter-page body fields)
         BLOCKED >= 70% any pair | FLAGGED 50-69% | PASS < 50%
         Confirms no two pages are structurally near-copies.

LAYER 2  N-gram phrase match (stop-word filtered)
         Flags any 4+ consecutive meaningful words shared by 3+ pages.
         Indicates possible verbatim source copying or rigid templates.

LAYER 3  Jaccard heading match
         Checks spread/card/intention titles against a corpus of known
         generic headings. Flagged headings need humanised <title> tags
         even if the body content is original.

LAYER G  Google duplication spot-check (Serper API, 4 samples per type)
         Searches Google for exact phrases from each page type.
         BLOCKED > 40% matched words | WATCH 20-40% | PASS <= 20%
         Requires SERPER_API_KEY environment variable.

USAGE
-----
    # From repo root:
    cd /path/to/DailyHoroscope-Migration

    # Layers 1-3 only (no API key needed):
    python tests/echo_pace_tarot_scan.py

    # All 4 layers (requires Serper key from Render env):
    SERPER_API_KEY=your_key python tests/echo_pace_tarot_scan.py

    # Save report to custom path:
    python tests/echo_pace_tarot_scan.py --output /tmp/tarot_report.json

OUTPUT
------
    Console: per-layer result per page type
    File:    tests/echo_pace_tarot_report.json (or --output path)

WHEN TO RE-RUN
--------------
    - After TAR-SEO-1 integration (now)
    - After TAR-SEO-2 content rewrite of tarot_seo_data.py
    - After any GAI optimisation pass that modifies content fields
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from itertools import combinations
from typing import Any

# ── Path setup ────────────────────────────────────────────────────────────────
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BACKEND = os.path.join(_REPO_ROOT, "backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

try:
    from tarot_seo_data import CARDS, INTENTIONS, MAJOR_MEANINGS, SPREADS
except ImportError as exc:
    sys.exit(f"ERROR: Cannot import tarot_seo_data -- {exc}\nRun from repo root.")

# ── Thresholds -- TAROT STRICT MODE ──────────────────────────────────────────
# Tarot is a HIGH RISK / HIGH STAKE / HIGH BENEFIT module (199 pages, core SEO).
# Thresholds are deliberately stricter than the generic ECHO/PACE defaults.
# Do NOT relax these without explicit TT sign-off.
#
# Generic default → Tarot strict → Rationale
# L1 BLOCKED:   70% → 60%   Tarot pages are long-form; 60% cosine = near-copy at page scale
# L1 FLAGGED:   50% → 40%   Forces review earlier; 40%+ on 199 pages = real Google risk
# L2 MIN_DOCS:   3  →  2    Template language appearing in 2+ pages is a flag on 199-page set
# LG BLOCKED:   40% → 25%   199 pages of tarot content -- Google indexes all; stricter duplication gate
# LG WATCH:     20% → 10%   Early warning at 10% given volume and competitive tarot SEO landscape
# LG SAMPLES:    2  →  5    5 samples per type (spread across suits/categories) = meaningful coverage

L1_BLOCKED  = 0.60   # STRICT: was 0.70 -- any pair ≥ 60% must be rewritten
L1_FLAGGED  = 0.40   # STRICT: was 0.50 -- pairs 40-59% require manual review + justification
L2_NGRAM    = 4      # minimum consecutive meaningful words to flag
L2_MIN_DOCS = 2      # STRICT: was 3 -- phrase in 2+ docs triggers review on a 199-page set
L3_JACCARD  = 0.60   # heading similarity vs generic corpus → FLAGGED
LG_BLOCKED  = 0.25   # STRICT: was 0.40 -- Google duplication ceiling for high-volume module
LG_WATCH    = 0.10   # STRICT: was 0.20 -- early warning threshold
LG_SAMPLES  = 5      # STRICT: was 2 -- 5 samples per page type, spread across suits/categories

# ── Stop words ────────────────────────────────────────────────────────────────
_STOPS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with",
    "by","from","is","it","its","be","are","was","were","been","being",
    "have","has","had","do","does","did","will","would","could","should",
    "may","might","can","this","that","these","those","i","you","he","she",
    "we","they","my","your","his","her","our","their","what","which","who",
    "when","where","why","how","all","each","both","few","more","most",
    "other","some","such","no","not","only","same","so","than","too","very",
    "just","about","above","after","before","between","through","during",
    "into","out","up","down","if","while","as","also","then","there","here",
    "them","any","one","two","three","four","five","six","seven","eight",
    "nine","ten","across","without","within","upon","over","under","toward",
    "already","even","still","back","again","once","always","never","often",
    "use","used","using","make","made","making","want","need","help",
}

# ── Generic tarot heading corpus (Layer 3) ────────────────────────────────────
_GENERIC_HEADINGS = [
    "celtic cross spread","three card spread","past present future",
    "horseshoe spread","relationship spread","career spread",
    "yes no spread","daily tarot reading","the fool","the magician",
    "the high priestess","the empress","the emperor","the hierophant",
    "the lovers","the chariot","strength","the hermit",
    "wheel of fortune","justice","the hanged man","death","temperance",
    "the devil","the tower","the star","the moon","the sun",
    "judgement","the world","ace of wands","ace of cups",
    "ace of swords","ace of pentacles","love","career","money",
    "health","spirituality","relationships","new beginnings",
    "decision making","self discovery","spiritual growth","forgiveness",
    "loss grief","past lives","friendship","pregnancy","legal matters",
    "travel","manifestation","anxiety","breakup",
]


# ════════════════════════════════════════════════════════════════════════════
# Content extractors
# ════════════════════════════════════════════════════════════════════════════

def _spread_body(s: dict) -> str:
    """Extract all meaningful body text from a spread record."""
    return " ".join(filter(None, [
        s.get("purpose", ""),
        s.get("when", ""),
        s.get("use", ""),
        s.get("overview", ""),
        s.get("guidance", ""),
    ]))

def _card_body(slug: str, card: dict) -> str:
    """Extract body text from a card record (major + minor arcana)."""
    parts = []
    # Major arcana -- rich content from MAJOR_MEANINGS
    if slug in MAJOR_MEANINGS:
        mm = MAJOR_MEANINGS[slug]
        parts += [mm.get("upright",""), mm.get("reversed",""), mm.get("imagery","")]
    # Minor arcana and any card dict
    for f in ("upright","reversed","imagery","description","guidance","interpretation"):
        v = card.get(f, "")
        if v and v not in parts:
            parts.append(v)
    return " ".join(filter(None, parts))

def _intention_body(slug: str, v: dict) -> str:
    """Extract body text from an intention record."""
    parts = [v.get("chapter", ""), v.get("label", "")]
    for f in ("description","intro","guidance","overview"):
        val = v.get(f, "")
        if val:
            parts.append(val)
    # Append card meanings for context richness check
    for card_slug in v.get("best_cards", [])[:3]:
        if card_slug in MAJOR_MEANINGS:
            parts.append(MAJOR_MEANINGS[card_slug].get("upright",""))
    return " ".join(filter(None, parts))

def _heading(record: Any, key: str = "name") -> str:
    if isinstance(record, dict):
        return (record.get("title") or record.get("name") or
                record.get("label") or record.get("slug") or "").lower()
    return str(record).lower()


# ════════════════════════════════════════════════════════════════════════════
# Layer 1 -- TF-IDF Cosine
# ════════════════════════════════════════════════════════════════════════════

def _tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-z]{3,}\b", text.lower())

def _tfidf_vectors(docs: list[str]) -> list[dict[str, float]]:
    tokenized = [_tokenize(d) for d in docs]
    N = len(docs)
    df: Counter = Counter()
    for toks in tokenized:
        df.update(set(toks))
    idf = {t: math.log((N + 1) / (f + 1)) + 1 for t, f in df.items()}
    vectors = []
    for toks in tokenized:
        tf = Counter(toks)
        total = len(toks) or 1
        vectors.append({t: (c / total) * idf[t] for t, c in tf.items()})
    return vectors

def _cosine(v1: dict, v2: dict) -> float:
    common = set(v1) & set(v2)
    if not common:
        return 0.0
    dot = sum(v1[t] * v2[t] for t in common)
    m1 = math.sqrt(sum(x * x for x in v1.values()))
    m2 = math.sqrt(sum(x * x for x in v2.values()))
    return dot / (m1 * m2) if m1 and m2 else 0.0

def layer1(docs: list[str], names: list[str], label: str) -> tuple[str, dict]:
    print(f"\n{'─'*60}")
    print(f"LAYER 1 · TF-IDF Cosine -- {label} ({len(docs)} items)")
    print(f"{'─'*60}")
    vecs = _tfidf_vectors(docs)
    blocked, flagged = [], []
    peak = 0.0
    for i, j in combinations(range(len(docs)), 2):
        sim = _cosine(vecs[i], vecs[j])
        peak = max(peak, sim)
        if sim >= L1_BLOCKED:
            blocked.append((names[i], names[j], sim))
        elif sim >= L1_FLAGGED:
            flagged.append((names[i], names[j], sim))

    if blocked:
        status = "BLOCKED"
        print(f"  ❌  BLOCKED -- {len(blocked)} pair(s) >= {L1_BLOCKED:.0%}")
        for a, b, s in blocked[:5]:
            print(f"      {a[:38]} ↔ {b[:38]}  {s:.1%}")
    elif flagged:
        status = "FLAGGED"
        print(f"  ⚠️   FLAGGED -- {len(flagged)} pair(s) in 50-69% range")
        for a, b, s in flagged[:3]:
            print(f"      {a[:38]} ↔ {b[:38]}  {s:.1%}")
    else:
        status = "PASS"
        print(f"  ✅  PASS -- 0 pairs >= {L1_FLAGGED:.0%}")

    print(f"  Peak similarity: {peak:.1%}")
    return status, {"blocked_pairs": len(blocked), "flagged_pairs": len(flagged), "peak": round(peak, 3)}


# ════════════════════════════════════════════════════════════════════════════
# Layer 2 -- N-gram phrase match
# ════════════════════════════════════════════════════════════════════════════

def _ngrams(text: str, n: int) -> set[str]:
    tokens = re.findall(r"\b[a-z]+\b", text.lower())
    meaningful = [(i, t) for i, t in enumerate(tokens) if t not in _STOPS]
    result = set()
    for idx in range(len(meaningful) - n + 1):
        group = meaningful[idx : idx + n]
        # Only count if tokens appear within a tight window (no huge gaps)
        if group[-1][0] - group[0][0] <= n + 4:
            result.add(" ".join(t for _, t in group))
    return result

def layer2(docs: list[str], label: str) -> tuple[str, dict]:
    print(f"\n{'─'*60}")
    print(f"LAYER 2 · N-gram Phrase Match (>={L2_NGRAM} words) -- {label}")
    print(f"{'─'*60}")
    doc_ngrams = []
    for doc in docs:
        phrases: set[str] = set()
        for n in range(L2_NGRAM, 9):
            phrases |= _ngrams(doc, n)
        doc_ngrams.append(phrases)

    freq: Counter = Counter()
    for phrases in doc_ngrams:
        for p in phrases:
            freq[p] += 1

    flagged = [(p, c) for p, c in freq.items() if c >= L2_MIN_DOCS]
    flagged.sort(key=lambda x: -x[1])

    if flagged:
        status = "FLAGGED"
        print(f"  ⚠️   {len(flagged)} phrase(s) appear in >= {L2_MIN_DOCS} docs")
        print(f"  Top offenders (review manually -- shared tarot terms expected):")
        for phrase, cnt in flagged[:10]:
            print(f"      [{cnt} docs] \"{phrase}\"")
        if len(flagged) > 10:
            print(f"      ... and {len(flagged)-10} more")
        print()
        print(f"  NOTE: Flag only if phrase is verbatim from a source book.")
        print(f"  Shared tarot vocabulary (e.g. 'upright meaning reversed') is normal.")
    else:
        status = "PASS"
        print(f"  ✅  PASS -- No {L2_NGRAM}+ word phrases appear in >= {L2_MIN_DOCS} docs")

    return status, {"flagged_phrases": len(flagged),
                    "top_5": [p for p, _ in flagged[:5]]}


# ════════════════════════════════════════════════════════════════════════════
# Layer 3 -- Jaccard heading match
# ════════════════════════════════════════════════════════════════════════════

def _jaccard(a: str, b: str) -> float:
    sa, sb = set(_tokenize(a)), set(_tokenize(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

def layer3(headings: list[str], label: str) -> tuple[str, dict]:
    print(f"\n{'─'*60}")
    print(f"LAYER 3 · Jaccard Heading Match -- {label}")
    print(f"{'─'*60}")
    flagged = []
    for h in headings:
        clean = h.replace("-", " ")
        for generic in _GENERIC_HEADINGS:
            score = _jaccard(clean, generic)
            if score >= L3_JACCARD:
                flagged.append((h, generic, score))
                break

    if flagged:
        print(f"  ℹ️   {len(flagged)} heading(s) score >= {L3_JACCARD:.0%} vs generic corpus")
        print(f"  These are expected for tarot. Ensure page <title> is humanised")
        print(f"  (not a verbatim generic like 'The Fool Tarot Card Meaning').")
        for h, g, s in flagged[:10]:
            print(f"      \"{h}\" ↔ \"{g}\"  {s:.0%}")
        status = "INFO"
    else:
        status = "PASS"
        print(f"  ✅  PASS -- No headings match generic corpus at >= {L3_JACCARD:.0%}")

    return status, {"matched_headings": len(flagged),
                    "sample": [h for h, _, _ in flagged[:5]]}


# ════════════════════════════════════════════════════════════════════════════
# Layer G -- Google duplication (Serper)
# ════════════════════════════════════════════════════════════════════════════

def _extract_sample_phrase(body: str) -> str | None:
    """Pull an 8-word stop-word-filtered phrase, skipping the opening."""
    tokens = [t for t in _tokenize(body) if t not in _STOPS]
    if len(tokens) < 10:
        return None
    return " ".join(tokens[6:14])  # skip generic opening words

def layer_google(
    records: list[tuple[str, str]],  # [(name, body_text), ...]
    label: str,
    serper_key: str,
    sample: int = 4,
) -> tuple[str, dict]:
    import urllib.request

    print(f"\n{'─'*60}")
    print(f"LAYER G · Google Duplication -- {label} ({sample} samples)")
    print(f"{'─'*60}")

    results = []
    for name, body in records[:sample]:
        phrase = _extract_sample_phrase(body)
        if not phrase:
            print(f"  ⚠️   {name[:40]} -- body too short to sample")
            continue

        payload = json.dumps({"q": f'"{phrase}"', "num": 10}).encode()
        try:
            req = urllib.request.Request(
                "https://google.serper.dev/search",
                data=payload,
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read())
            hits = len((data or {}).get("organic") or [])
        except Exception as exc:
            print(f"  ⚠️   Serper error for \"{phrase[:40]}\": {exc}")
            continue

        dup_rate = min(hits / 10, 1.0)
        icon = "✅" if dup_rate <= LG_WATCH else ("⚠️" if dup_rate <= LG_BLOCKED else "❌")
        print(f"  {icon}  [{hits}/10 hits] \"{phrase[:55]}\"")
        results.append({"phrase": phrase, "hits": hits, "dup_rate": round(dup_rate, 3)})

    if not results:
        print("  ⚠️   No samples could be checked.")
        return "SKIP", {}

    avg = sum(r["dup_rate"] for r in results) / len(results)
    peak = max(r["dup_rate"] for r in results)
    status = "BLOCKED" if peak > LG_BLOCKED else ("WATCH" if avg > LG_WATCH else "PASS")
    icon = {"BLOCKED": "❌", "WATCH": "⚠️", "PASS": "✅"}[status]
    print(f"\n  {icon}  Avg {avg:.0%} · Peak {peak:.0%} -- {status}")
    print(f"  Thresholds: BLOCKED>{LG_BLOCKED:.0%} | WATCH>{LG_WATCH:.0%}")
    return status, {"avg_dup_rate": round(avg, 3), "peak_dup_rate": round(peak, 3),
                    "samples_checked": len(results), "results": results}


# ════════════════════════════════════════════════════════════════════════════
# Diversity samplers for Layer G (ensures meaningful coverage)
# ════════════════════════════════════════════════════════════════════════════

def _diverse_spread_sample(spreads: list, n: int) -> list:
    """Pick n spreads spread across chapter categories, not just the first n."""
    by_chapter: dict[str, list] = {}
    for s in spreads:
        ch = s.get("chapter", "Other")
        by_chapter.setdefault(ch, []).append(s)
    chapters = list(by_chapter.keys())
    result = []
    idx = 0
    while len(result) < n and idx < max(len(v) for v in by_chapter.values()):
        for ch in chapters:
            bucket = by_chapter[ch]
            if idx < len(bucket):
                result.append(bucket[idx])
            if len(result) >= n:
                break
        idx += 1
    return result[:n]

def _suit_diverse_card_sample(card_items: list, n: int) -> list:
    """Pick cards across suits: major arcana, wands, cups, swords, pentacles."""
    suits = {
        "major": [], "wands": [], "cups": [], "swords": [], "pentacles": [],
    }
    for slug, card in card_items:
        for suit in suits:
            if suit in slug:
                suits[suit].append((slug, card))
                break
        else:
            suits["major"].append((slug, card))

    result = []
    # Take one from each suit first, then fill up
    for suit_list in suits.values():
        if suit_list and len(result) < n:
            # pick from middle of suit, not the ace (most-scraped card in each suit)
            idx = len(suit_list) // 2
            result.append(suit_list[idx])
    # fill remaining slots from most-content-rich (major arcana) if needed
    for slug, card in suits["major"]:
        if len(result) >= n:
            break
        if (slug, card) not in result:
            result.append((slug, card))
    return result[:n]


# ════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(description="ECHO/PACE Tarot SEO Scanner")
    parser.add_argument("--output", default="tests/echo_pace_tarot_report.json")
    args = parser.parse_args()

    # Render env var name: Serper_Default_key
    serper_key = (os.getenv("Serper_Default_key") or os.getenv("SERPER_API_KEY") or "").strip()

    print("=" * 60)
    print("ECHO/PACE SCANNER -- Tarot SEO Module  [STRICT MODE]")
    print(f"SPREADS: {len(SPREADS)} · CARDS: {len(CARDS)} · INTENTIONS: {len(INTENTIONS)}")
    print(f"Thresholds: L1 BLOCKED≥{L1_BLOCKED:.0%}/FLAGGED≥{L1_FLAGGED:.0%} · "
          f"L2 min_docs={L2_MIN_DOCS} · LG BLOCKED>{LG_BLOCKED:.0%}/WATCH>{LG_WATCH:.0%}")
    if not serper_key:
        print("⚠️   Serper key not set -- Layer G will be skipped.")
        print("    To enable (key name in Render: Serper_Default_key):")
        print("    Serper_Default_key=your_key python3 tests/echo_pace_tarot_scan.py")
        print("    Layer G uses ~6 Serper credits (2 samples × 3 page types).")
        print("    Only run Layer G once Layers 1-3 are clean.")
    print("=" * 60)

    report: dict[str, Any] = {}
    all_statuses: list[str] = []

    # ── Spreads ───────────────────────────────────────────────────────────────
    spread_docs   = [_spread_body(s) for s in SPREADS]
    spread_names  = [s.get("title", s.get("slug", "")) for s in SPREADS]
    s1_st, s1     = layer1(spread_docs, spread_names, "Spreads (100)")
    s2_st, s2     = layer2(spread_docs, "Spreads")
    s3_st, s3     = layer3([n.lower().replace("-"," ") for n in spread_names], "Spreads")
    report["spreads"] = {"L1": s1, "L2": s2, "L3": s3}
    all_statuses += [s1_st, s2_st]

    # ── Cards ─────────────────────────────────────────────────────────────────
    card_items  = list(CARDS.items()) if isinstance(CARDS, dict) else \
                  [(c.get("slug", str(i)), c) for i, c in enumerate(CARDS)]
    card_docs   = [_card_body(slug, card) for slug, card in card_items]
    card_names  = [slug for slug, _ in card_items]
    c1_st, c1   = layer1(card_docs, card_names, "Cards (78)")
    c2_st, c2   = layer2(card_docs, "Cards")
    c3_st, c3   = layer3([s.replace("-"," ") for s in card_names], "Cards")
    report["cards"] = {"L1": c1, "L2": c2, "L3": c3}
    all_statuses += [c1_st, c2_st]

    # ── Intentions ────────────────────────────────────────────────────────────
    int_items   = list(INTENTIONS.items()) if isinstance(INTENTIONS, dict) else \
                  [(i.get("slug",""), i) for i in INTENTIONS]
    int_docs    = [_intention_body(slug, v) for slug, v in int_items]
    int_names   = [slug for slug, _ in int_items]
    i1_st, i1   = layer1(int_docs, int_names, "Intentions (20)")
    i2_st, i2   = layer2(int_docs, "Intentions")
    i3_st, i3   = layer3([s.replace("-"," ") for s in int_names], "Intentions")
    report["intentions"] = {"L1": i1, "L2": i2, "L3": i3}
    all_statuses += [i1_st, i2_st]

    # ── Layer G ── only runs if L1-L3 are clean (quota protection) ──────────────
    l123_blocked = "BLOCKED" in all_statuses
    print(f"\n{'─'*60}")
    if not serper_key:
        print("LAYER G · Google Duplication -- SKIPPED (no Serper_Default_key)")
        print("  Once Layers 1-3 are fully clean, set key and re-run to complete check.")
        report["layer_g"] = "SKIPPED_NO_KEY"
    elif l123_blocked:
        print("LAYER G · Google Duplication -- SKIPPED (L1-L3 have BLOCKED items)")
        print("  Fix BLOCKED issues first. Saves Serper quota -- no point checking Google")
        print("  duplication on content that is already internally broken.")
        report["layer_g"] = "SKIPPED_L123_BLOCKED"
    else:
        credit_cost = LG_SAMPLES * 3
        print(f"LAYER G · Running STRICT MODE -- {LG_SAMPLES} samples × 3 page types")
        print(f"  Threshold: BLOCKED >{LG_BLOCKED:.0%} | WATCH >{LG_WATCH:.0%} (strict -- standard is 40%/20%)")
        print(f"  Approx Serper credits used: ~{credit_cost}")
        print(f"{'─'*60}")

        # Spreads: sample across spread categories (not just first N)
        spread_sample = _diverse_spread_sample(SPREADS, LG_SAMPLES)
        sg_st, sg = layer_google(
            [(s.get("title",""), _spread_body(s)) for s in spread_sample],
            "Spreads (category-diverse)", serper_key, sample=LG_SAMPLES)

        # Cards: sample one per suit (major, wands, cups, swords, pentacles)
        card_sample = _suit_diverse_card_sample(card_items, LG_SAMPLES)
        cg_st, cg = layer_google(
            [(slug, _card_body(slug, card)) for slug, card in card_sample],
            "Cards (suit-diverse)", serper_key, sample=LG_SAMPLES)

        # Intentions: spread across topic clusters
        ig_st, ig = layer_google(
            [(slug, _intention_body(slug, v)) for slug, v in int_items],
            "Intentions", serper_key, sample=LG_SAMPLES)

        report["layer_g"] = {
            "spreads": sg, "cards": cg, "intentions": ig,
            "thresholds": {"blocked": LG_BLOCKED, "watch": LG_WATCH, "samples": LG_SAMPLES},
        }
        all_statuses += [sg_st, cg_st, ig_st]

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"  Spreads    L1:{s1_st:8} L2:{s2_st:8} L3:{s3_st:8}")
    print(f"  Cards      L1:{c1_st:8} L2:{c2_st:8} L3:{c3_st:8}")
    print(f"  Intentions L1:{i1_st:8} L2:{i2_st:8} L3:{i3_st:8}")
    if serper_key and not l123_blocked:
        print(f"  Layer G    Spreads:{sg_st:8} Cards:{cg_st:8} Intentions:{ig_st:8}")
    elif l123_blocked:
        print(f"  Layer G    SKIPPED -- fix L1-L3 BLOCKED items first")
    else:
        print(f"  Layer G    SKIPPED -- set Serper_Default_key to run")

    active = [s for s in all_statuses if s != "SKIP"]
    if "BLOCKED" in active:
        verdict = "❌  BLOCKED -- Fix issues above before proceeding."
    elif "FLAGGED" in active:
        verdict = "⚠️   FLAGGED -- Review flagged items. If all are tarot vocabulary, proceed."
    else:
        verdict = "✅  PASS -- All layers clear. Safe to proceed to TAR-SEO-2."

    print(f"\n  VERDICT: {verdict}")
    report["verdict"] = verdict

    with open(args.output, "w") as fh:
        json.dump(report, fh, indent=2)
    print(f"  Report saved: {args.output}")
    print()
    print("NEXT STEP: Share this output with TT for sign-off, then activate TAR-SEO-2.")
    print("After TAR-SEO-2 content swap -- re-run this script to confirm no regression.")

    return 1 if "BLOCKED" in active else 0


if __name__ == "__main__":
    sys.exit(main())
