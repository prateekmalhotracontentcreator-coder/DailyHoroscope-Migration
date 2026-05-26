#!/usr/bin/env python3
"""
ECHO // PACE Compliance Verifier -- M3 Festival × Region Summaries
=================================================================
Checks cross-festival worst-pair TF-IDF cosine similarity for each region.

For every region (30), we take all festival entries for that region and compute
pairwise cosine similarity. If any two festivals in the same region score >= 40%,
the batch fails -- Google will treat them as near-duplicate programmatic pages.

Two checks:
  1. Per-region worst-pair  -- worst score across all festival pairs for that region
  2. Global worst-pair      -- single highest score across all 30 × n_festival pairs

Ceiling: 40%  (GAI Round 3 target)

Usage:
    python3 backend/scripts/verify_festival_compliance.py

Exit 0 = PASS   all regions < 40% ceiling
Exit 1 = FAIL   one or more regions breach ceiling -- integrate GAI fix before prod
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

from seo_m3_festival_summaries import FESTIVAL_REGION_SUMMARY

# ── Config ────────────────────────────────────────────────────────────────────
CEILING = 40.0

FESTIVAL_BOILERPLATE = [
    "festival", "celebration", "india", "indian", "community", "families",
    "family", "local", "traditional", "households", "neighborhood", "region",
    "seasonal", "auspicious", "gathering", "festive", "cultural", "annual",
    "sharing", "evening", "morning", "prayers", "devotional", "sacred",
    "marks", "mark", "welcomes", "welcoming", "celebrated", "celebrating",
    "gather", "gatherings", "visitors", "visiting", "guests",
]
CUSTOM_STOP = list(sk_text.ENGLISH_STOP_WORDS.union(FESTIVAL_BOILERPLATE))

vectorizer = TfidfVectorizer(
    stop_words=CUSTOM_STOP,
    ngram_range=(1, 2),
    min_df=1,
    max_features=30_000,
)

# ── Build lookup: region → {festival: text} ───────────────────────────────────
def build_region_map() -> dict[str, dict[str, str]]:
    region_map: dict[str, dict[str, str]] = {}
    for (festival, region), text in FESTIVAL_REGION_SUMMARY.items():
        region_map.setdefault(region, {})[festival] = text
    return region_map

# ── Worst-pair similarity for a list of texts ─────────────────────────────────
def worst_pair(texts: list[str]) -> tuple[float, str, str, list[str]]:
    """Returns (score_pct, label_a, label_b, labels_list)."""
    if len(texts) < 2:
        return 0.0, "", "", []
    return 0.0, "", "", []  # replaced below

def worst_pair_labelled(
    entries: dict[str, str]
) -> tuple[float, str, str]:
    festivals = list(entries.keys())
    texts = [entries[f] for f in festivals]
    if len(texts) < 2:
        return 0.0, "", ""
    mat = vectorizer.fit_transform(texts)
    sim = cosine_similarity(mat)
    worst = 0.0
    fa, fb = "", ""
    for i, j in combinations(range(len(festivals)), 2):
        score = sim[i][j] * 100
        if score > worst:
            worst = score
            fa, fb = festivals[i], festivals[j]
    return round(worst, 1), fa, fb

# ── Run ───────────────────────────────────────────────────────────────────────
def run() -> bool:
    region_map = build_region_map()
    regions = sorted(region_map.keys())
    festivals_seen = sorted({f for (f, _) in FESTIVAL_REGION_SUMMARY})

    print("\n" + "=" * 70)
    print("  ECHO // PACE  --  M3 FESTIVAL × REGION COMPLIANCE CHECK")
    print("=" * 70)
    print(f"  Festivals : {len(festivals_seen)}")
    print(f"  Regions   : {len(regions)}")
    print(f"  Entries   : {len(FESTIVAL_REGION_SUMMARY)}")
    print(f"  Ceiling   : {CEILING}%  (cross-festival worst-pair per region)")
    print("-" * 70)

    failures: list[tuple[str, float, str, str]] = []
    all_scores: list[float] = []

    for region in regions:
        entries = region_map[region]
        if len(entries) < 2:
            continue
        score, fa, fb = worst_pair_labelled(entries)
        all_scores.append(score)
        status = "✅" if score < CEILING else "❌"
        if score < CEILING:
            print(f"  {status}  {region:<28}  {score:5.1f}%  ({fa} vs {fb})")
        else:
            print(f"  {status}  {region:<28}  {score:5.1f}%  ← BREACH: {fa} vs {fb}")
            failures.append((region, score, fa, fb))

    global_worst = max(all_scores) if all_scores else 0.0
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0.0

    print("-" * 70)
    print(f"  Global worst-pair : {global_worst:.1f}%")
    print(f"  Average           : {avg_score:.1f}%")
    print(f"  Regions breaching : {len(failures)} / {len(regions)}")
    print("=" * 70)

    if not failures:
        print(f"\n  🎉 PASS -- all {len(regions)} regions under {CEILING}% ceiling.")
        print("      Festival summaries are cross-festival compliant.\n")
    else:
        print(f"\n  ❌ FAIL -- {len(failures)} region(s) breach the {CEILING}% ceiling:\n")
        for region, score, fa, fb in failures:
            print(f"      • {region}: {score:.1f}%  ({fa} vs {fb})")
        print("\n      Request GAI regeneration for the failing festival×region pairs.\n")

    return len(failures) == 0


if __name__ == "__main__":
    passed = run()
    sys.exit(0 if passed else 1)
