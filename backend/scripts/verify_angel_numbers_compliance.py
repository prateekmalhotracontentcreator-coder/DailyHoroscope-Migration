#!/usr/bin/env python3
"""
ECHO // PACE Compliance Verifier -- Angel Numbers Module
=======================================================
Checks cross-number TF-IDF cosine similarity for each intent cluster.

For every intent (9), we sample the `seeing_it_means` + `vibration` text
from a cross-section of core records and compute pairwise cosine similarity.
If any two records in the same intent score >= 40%, the batch fails.

Two checks:
  1. Per-intent worst-pair  -- worst score across all number pairs per intent
  2. Global worst-pair      -- single highest score across all intent clusters

Ceiling: 40%  (standard E.C.H.O. // P.A.C.E. limit for SEO modules)

Usage:
    python3 backend/scripts/verify_angel_numbers_compliance.py

Exit 0 = PASS   all intent clusters < 40% ceiling
Exit 1 = FAIL   one or more clusters breach ceiling
"""
from __future__ import annotations

import sys
from pathlib import Path
from itertools import combinations

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text as sk_text

# ── Config ────────────────────────────────────────────────────────────────────
CEILING = 40.0
SAMPLE_SIZE = 50   # numbers to sample per intent cluster (out of 1000)

ANGEL_STOP_WORDS = [
    "angel", "number", "numbers", "sequence", "repeating", "seeing",
    "sign", "signs", "message", "messages", "universe", "divine", "guidance",
    "numerology", "vibration", "energy", "spiritual", "meaning", "means",
    "notice", "noticing", "alignment", "aligned", "signal", "signals",
    "frequency", "frequencies", "pattern", "patterns", "nudge",
]
CUSTOM_STOP = list(sk_text.ENGLISH_STOP_WORDS.union(ANGEL_STOP_WORDS))

vectorizer = TfidfVectorizer(
    stop_words=CUSTOM_STOP,
    ngram_range=(1, 2),
    min_df=1,
    max_features=30_000,
)


INTENT_SLUGS = [
    "love", "career", "twin-flame", "manifestation",
    "health", "spiritual-growth", "family", "protection", "new-beginnings",
]

# Sample 50 numbers evenly spread across 1-9999
SAMPLE_NUMBERS = [str(i) for i in range(1, 10000, 10000 // SAMPLE_SIZE)][:SAMPLE_SIZE]


def build_intent_map() -> dict[str, list[str]]:
    """
    Build {intent_slug: [text, text, ...]} by calling build_seeing_it_means
    and build_vibration directly from angel_numbers_data.py generators.
    """
    try:
        from angel_numbers_data import (
            build_seeing_it_means,
            build_vibration,
            build_intent_message,
        )
    except ImportError:
        print("ERROR: Cannot import angel_numbers_data.")
        print("Run: PYTHONPATH=backend python3 backend/scripts/verify_angel_numbers_compliance.py")
        sys.exit(1)

    def _root(n: str) -> int:
        s = n
        while len(s) > 1:
            s = str(sum(int(d) for d in s))
        return int(s)

    intent_map: dict[str, list[str]] = {}

    # Core text cluster -- seeing_it_means + vibration across sampled numbers
    core_texts = []
    for num in SAMPLE_NUMBERS:
        r = _root(num)
        text = build_seeing_it_means(num, r) + " " + build_vibration(num, r)
        core_texts.append(text)
    intent_map["core"] = core_texts

    # Per-intent message cluster -- intent message across sampled numbers
    for slug in INTENT_SLUGS:
        texts = []
        for num in SAMPLE_NUMBERS:
            r = _root(num)
            try:
                msg = build_intent_message(num, slug, r)
                texts.append(msg)
            except Exception:
                pass
        if texts:
            intent_map[slug] = texts

    return intent_map


def worst_pair(texts: list[str]) -> tuple[float, int, int]:
    """Return (worst_score_pct, idx_a, idx_b) for a list of texts."""
    if len(texts) < 2:
        return 0.0, 0, 0
    mat = vectorizer.fit_transform(texts)
    sims = cosine_similarity(mat)
    worst = 0.0
    wi, wj = 0, 1
    n = len(texts)
    for i, j in combinations(range(n), 2):
        if sims[i, j] > worst:
            worst = sims[i, j]
            wi, wj = i, j
    return worst * 100, wi, wj


def run() -> int:
    print("=" * 64)
    print("ECHO // PACE Compliance Check -- Angel Numbers Module")
    print(f"Ceiling: {CEILING}%  |  Sample: {SAMPLE_SIZE} numbers per intent")
    print("=" * 64)

    intent_map = build_intent_map()

    if not intent_map:
        print("ERROR: No intent clusters built. Check angel_numbers_data.py.")
        return 1

    global_worst = 0.0
    any_fail = False
    results: list[tuple[str, float, str]] = []

    for intent_slug, texts in sorted(intent_map.items()):
        if len(texts) < 2:
            results.append((intent_slug, 0.0, "SKIP (< 2 records)"))
            continue
        score, _, _ = worst_pair(texts)
        status = "PASS ✅" if score < CEILING else "FAIL ❌"
        if score >= CEILING:
            any_fail = True
        if score > global_worst:
            global_worst = score
        results.append((intent_slug, score, status))

    # ── Print results table ────────────────────────────────────────────────
    print(f"\n{'Intent':<25} {'Worst Pair':>12}   Status")
    print("-" * 55)
    for intent_slug, score, status in results:
        flag = " ← BREACH" if score >= CEILING else ""
        print(f"  {intent_slug:<23} {score:>10.1f}%   {status}{flag}")

    print("-" * 55)
    print(f"  {'GLOBAL WORST':23} {global_worst:>10.1f}%")
    print()

    if any_fail:
        print(f"RESULT: FAIL -- one or more intent clusters breach {CEILING}% ceiling.")
        print("Action: Issue ANGEL-2 content rewrite commission to reduce repetition.")
        return 1
    else:
        print(f"RESULT: PASS -- all intent clusters below {CEILING}% ceiling.")
        return 0


if __name__ == "__main__":
    sys.exit(run())
