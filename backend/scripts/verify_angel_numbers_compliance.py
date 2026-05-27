#!/usr/bin/env python3
"""
ECHO // PACE Compliance Verifier -- Angel Numbers Module (3-Layer)
=================================================================

Layer 1 -- TF-IDF Cosine Similarity (body fields)
  Catches overall structural similarity: paraphrasing, template copying.
  BLOCKED  ≥ 70%   Hard reject -- pages will be treated as near-duplicates by Google.
  FLAGGED  50-69%  Review required before publishing.
  PASS     < 50%   Acceptable structural diversity.
  Target   < 40%   EverydayHoroscope E.C.H.O. // P.A.C.E. production ceiling.

Layer 2 -- N-gram Phrase Match (stop-word filtered)
  Catches 4+ consecutive meaningful words appearing verbatim across multiple records.
  Stop words excluded -- no false positives on phrases like "when you want to".
  FAIL: any 4+ word meaningful phrase appearing in > 15% of records.

Layer 3 -- Jaccard Heading / Category Title Match
  Catches intent names, number family labels, and section headings that are
  verbatim duplicates across records. These need AI humanizing before publish.
  FAIL: any heading / category title with Jaccard similarity ≥ 0.75 across records.

Usage:
    PYTHONPATH=backend python3 backend/scripts/verify_angel_numbers_compliance.py

Exit 0 = all 3 layers PASS
Exit 1 = one or more layers FAIL
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text as sk_text

# ── Config ────────────────────────────────────────────────────────────────────
LAYER1_BLOCKED  = 70.0   # Hard reject threshold
LAYER1_FLAGGED  = 50.0   # Flag for review
LAYER1_TARGET   = 40.0   # EverydayHoroscope production ceiling

LAYER2_NGRAM_N  = 4      # Minimum consecutive words to flag
LAYER2_MAX_PCT  = 15.0   # Max % of records that may share the same 4-gram

LAYER3_JACCARD  = 0.75   # Jaccard similarity threshold for headings

SAMPLE_SIZE = 50

ANGEL_STOP_WORDS = [
    "angel", "number", "numbers", "sequence", "repeating", "seeing",
    "sign", "signs", "message", "messages", "universe", "divine", "guidance",
    "numerology", "vibration", "energy", "spiritual", "meaning", "means",
    "notice", "noticing", "alignment", "aligned", "signal", "signals",
    "frequency", "frequencies", "pattern", "patterns", "nudge",
    "life", "time", "you", "your", "this", "that", "when", "what",
    "with", "into", "from", "have", "more", "which", "will", "are",
]
CUSTOM_STOP = set(sk_text.ENGLISH_STOP_WORDS) | set(ANGEL_STOP_WORDS)
CUSTOM_STOP_LIST = list(CUSTOM_STOP)

vectorizer = TfidfVectorizer(
    stop_words=CUSTOM_STOP_LIST,
    ngram_range=(1, 2),
    min_df=1,
    max_features=30_000,
)

INTENT_SLUGS = [
    "love", "career", "twin-flame", "manifestation",
    "health", "spiritual-growth", "family", "protection", "new-beginnings",
]

SAMPLE_NUMBERS = [str(i) for i in range(1, 10000, 10000 // SAMPLE_SIZE)][:SAMPLE_SIZE]


def _root(n: str) -> int:
    s = n
    while len(s) > 1:
        s = str(sum(int(d) for d in s))
    return int(s)


def _import_builders():
    try:
        from angel_numbers_data import (
            build_seeing_it_means,
            build_vibration,
            build_intent_message,
            build_key_themes,
        )
        return build_seeing_it_means, build_vibration, build_intent_message, build_key_themes
    except ImportError:
        print("ERROR: Cannot import angel_numbers_data.")
        print("Run: PYTHONPATH=backend python3 backend/scripts/verify_angel_numbers_compliance.py")
        sys.exit(1)


# ── Layer 1 ───────────────────────────────────────────────────────────────────

def build_text_clusters(builders) -> dict[str, list[str]]:
    build_seeing, build_vib, build_msg, _ = builders
    clusters: dict[str, list[str]] = {}

    # Core cluster
    core = []
    for num in SAMPLE_NUMBERS:
        r = _root(num)
        core.append(build_seeing(num, r) + " " + build_vib(num, r))
    clusters["core"] = core

    # Per-intent clusters
    for slug in INTENT_SLUGS:
        texts = []
        for num in SAMPLE_NUMBERS:
            r = _root(num)
            try:
                texts.append(build_msg(num, slug, r))
            except Exception:
                pass
        if texts:
            clusters[slug] = texts

    return clusters


def run_layer1(clusters: dict[str, list[str]]) -> tuple[bool, list[tuple]]:
    """Returns (any_blocked, results_list)."""
    any_blocked = False
    results = []
    global_worst = 0.0

    for name, texts in sorted(clusters.items()):
        if len(texts) < 2:
            results.append((name, 0.0, "SKIP"))
            continue
        mat = vectorizer.fit_transform(texts)
        sims = cosine_similarity(mat)
        worst = 0.0
        n = len(texts)
        for i, j in combinations(range(n), 2):
            if sims[i, j] > worst:
                worst = sims[i, j]
        score = worst * 100
        if score >= LAYER1_BLOCKED:
            status = "BLOCKED ❌"
            any_blocked = True
        elif score >= LAYER1_FLAGGED:
            status = "FLAGGED ⚠️"
        elif score >= LAYER1_TARGET:
            status = "OVER TARGET ⚠️"
        else:
            status = "PASS ✅"
        if score > global_worst:
            global_worst = score
        results.append((name, score, status))

    results.append(("GLOBAL WORST", global_worst,
                    "BLOCKED ❌" if global_worst >= LAYER1_BLOCKED else
                    "FLAGGED ⚠️" if global_worst >= LAYER1_FLAGGED else
                    "PASS ✅"))
    return any_blocked, results


# ── Layer 2 ───────────────────────────────────────────────────────────────────

def _tokenize_filtered(text: str) -> list[str]:
    words = re.findall(r"[a-z']+", text.lower())
    return [w for w in words if w not in CUSTOM_STOP and len(w) > 2]


def _ngrams(tokens: list[str], n: int) -> list[str]:
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def run_layer2(clusters: dict[str, list[str]]) -> tuple[bool, list[tuple]]:
    """Check for 4+ verbatim n-gram phrases repeated across > LAYER2_MAX_PCT of records."""
    all_texts = []
    for texts in clusters.values():
        all_texts.extend(texts)

    if len(all_texts) < 4:
        return False, [("N/A", 0.0, "SKIP (too few records)")]

    # Count 4-gram frequency across all records
    ngram_counts: Counter = Counter()
    for text in all_texts:
        tokens = _tokenize_filtered(text)
        seen = set(_ngrams(tokens, LAYER2_NGRAM_N))
        for ng in seen:
            ngram_counts[ng] += 1

    total = len(all_texts)
    threshold_count = total * (LAYER2_MAX_PCT / 100)
    violations = [
        (ng, count, (count / total) * 100)
        for ng, count in ngram_counts.most_common(20)
        if count > threshold_count
    ]

    any_fail = bool(violations)
    results = []
    if violations:
        for ng, count, pct in violations[:10]:
            results.append((f'"{ng}"', pct, f"FAIL ❌ ({count}/{total} records = {pct:.1f}%)"))
    else:
        results.append(("No violations found", 0.0, "PASS ✅"))

    return any_fail, results


# ── Layer 3 ───────────────────────────────────────────────────────────────────

def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def run_layer3(builders) -> tuple[bool, list[tuple]]:
    """Check intent display names and key_themes for verbatim / near-verbatim repetition."""
    _, _, _, build_themes = builders

    # Collect key_themes for each sampled number
    themes_by_number: dict[str, list[str]] = {}
    for num in SAMPLE_NUMBERS[:20]:  # 20 is enough for heading check
        r = _root(num)
        try:
            themes = build_themes(num, r)
            if themes:
                themes_by_number[num] = themes
        except Exception:
            pass

    if len(themes_by_number) < 2:
        return False, [("N/A", 0.0, "SKIP (themes not available)")]

    nums = list(themes_by_number.keys())
    violations = []
    worst_score = 0.0

    for i, j in combinations(range(len(nums)), 2):
        a_set = set(t.lower().strip() for t in themes_by_number[nums[i]])
        b_set = set(t.lower().strip() for t in themes_by_number[nums[j]])
        score = _jaccard(a_set, b_set)
        if score > worst_score:
            worst_score = score
        if score >= LAYER3_JACCARD:
            violations.append((f"{nums[i]} vs {nums[j]}", score * 100,
                                f"FAIL ❌ (themes too similar -- need AI humanising)"))

    any_fail = bool(violations)
    results = violations[:5] if violations else [
        (f"Worst pair Jaccard", worst_score * 100,
         f"PASS ✅ (worst={worst_score*100:.1f}% < {LAYER3_JACCARD*100:.0f}%)")
    ]
    return any_fail, results


# ── Main ──────────────────────────────────────────────────────────────────────

def run() -> int:
    print("=" * 68)
    print("ECHO // PACE Compliance Check -- Angel Numbers Module (3 Layers)")
    print(f"L1 Target: <{LAYER1_TARGET}%  |  Flagged: ≥{LAYER1_FLAGGED}%  |  Blocked: ≥{LAYER1_BLOCKED}%")
    print(f"L2 N-gram: {LAYER2_NGRAM_N}+ words verbatim in ≤{LAYER2_MAX_PCT}% records")
    print(f"L3 Jaccard heading: < {LAYER3_JACCARD*100:.0f}%")
    print(f"Sample: {SAMPLE_SIZE} numbers")
    print("=" * 68)

    builders = _import_builders()
    clusters = build_text_clusters(builders)

    # ── Layer 1
    print("\n── LAYER 1: TF-IDF Cosine Similarity (body fields) ─────────────")
    l1_fail, l1_results = run_layer1(clusters)
    print(f"{'Cluster':<25} {'Worst Pair':>12}   Status")
    print("-" * 58)
    for name, score, status in l1_results:
        print(f"  {name:<23} {score:>10.1f}%   {status}")

    # ── Layer 2
    print("\n── LAYER 2: N-gram Phrase Match (stop-word filtered) ────────────")
    l2_fail, l2_results = run_layer2(clusters)
    for phrase, pct, status in l2_results:
        print(f"  {phrase[:40]:<40}   {status}")

    # ── Layer 3
    print("\n── LAYER 3: Jaccard Heading / Key Themes Match ──────────────────")
    l3_fail, l3_results = run_layer3(builders)
    for pair, score, status in l3_results:
        print(f"  {pair:<30}   {status}")

    # ── Verdict
    print("\n" + "=" * 68)
    any_fail = l1_fail or l2_fail or l3_fail
    if any_fail:
        failures = []
        if l1_fail: failures.append("Layer 1 (TF-IDF BLOCKED)")
        if l2_fail: failures.append("Layer 2 (N-gram verbatim phrases)")
        if l3_fail: failures.append("Layer 3 (Jaccard headings)")
        print(f"OVERALL RESULT: FAIL -- {' | '.join(failures)}")
        print("Action: Issue ANGEL-2 commission. All 3 layers must PASS before deploy.")
        return 1
    else:
        print("OVERALL RESULT: PASS -- all 3 layers within tolerance.")
        return 0


if __name__ == "__main__":
    sys.exit(run())
