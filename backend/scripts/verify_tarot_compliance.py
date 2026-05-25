#!/usr/bin/env python3
"""
ECHO // PACE Compliance Verifier -- Tarot Module
================================================
Benchmarks cross-page similarity for tarot combination pages.

Tests two architectural approaches:
  BEFORE (template): "[Card] energy meets [Spread] intent. [Full upright def]"
  AFTER  (compliant): Spread-purpose-led + elemental synthesis + 1 intent sentence

The 'after' approach simulates what TAR-M4 Codex will generate:
  - Each page LEADS with the spread's unique purpose (different per spread)
  - Card contribution = 1 intent-matched sentence (not the full 3-sentence upright)
  - Elemental intersection synthesis = unique per card×spread combination

Similarity ceiling: 30% cross-page worst-pair score.

Usage:
    python3 backend/scripts/verify_tarot_compliance.py

Exit 0 = PASS   (compliant architecture -- safe to issue TAR-M4)
Exit 1 = FAIL   (fix required before seeding)
"""
from __future__ import annotations
import sys
import random
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text as sk_text

# ── Config ────────────────────────────────────────────────────────────────────
SIMILARITY_CEILING = 30.0
SAMPLE_CARDS   = 8
SAMPLE_SPREADS = 8

TAROT_BOILERPLATE = [
    "tarot", "card", "spread", "upright", "reversed", "reading",
    "arcana", "querent", "suit", "wands", "cups", "swords", "pentacles",
    "position", "layout", "draw", "deck",
]
CUSTOM_STOP = list(sk_text.ENGLISH_STOP_WORDS.union(TAROT_BOILERPLATE))
vectorizer = TfidfVectorizer(stop_words=CUSTOM_STOP, ngram_range=(1, 2),
                              min_df=1, max_features=30_000)

# ── Elemental synthesis vocabulary (card suit × spread category) ──────────────
# Each combination produces a unique introductory phrase
ELEMENT_PHRASES = {
    ("fire",    "love"):    "passionate fire meets the heart's deepest map",
    ("fire",    "career"):  "ambitious fire channels into professional momentum",
    ("fire",    "health"):  "vital fire energy redirects toward physical renewal",
    ("fire",    "general"): "fire's drive illuminates the core of this question",
    ("water",   "love"):    "emotional depth surfaces through this reading's flow",
    ("water",   "career"):  "intuitive water finds its path through career terrain",
    ("water",   "health"):  "restorative water energy addresses the body's signals",
    ("water",   "general"): "water's wisdom reveals what lies beneath the surface",
    ("air",     "love"):    "clarity and truth reframe this relationship's pattern",
    ("air",     "career"):  "sharp mental focus cuts through professional confusion",
    ("air",     "health"):  "analytical air energy diagnoses what needs attention",
    ("air",     "general"): "air's precision names the exact nature of this moment",
    ("earth",   "love"):    "grounded earth energy stabilises this relationship's foundation",
    ("earth",   "career"):  "practical earth aligns effort with sustainable progress",
    ("earth",   "health"):  "earth's steadiness supports the body's long recovery",
    ("earth",   "general"): "earth's patience clarifies what requires immediate action",
    ("major",   "love"):    "archetypal force reshapes the entire romantic landscape",
    ("major",   "career"):  "a major life force accelerates this career transition",
    ("major",   "health"):  "deep archetypal energy initiates a healing threshold",
    ("major",   "general"): "a powerful cycle turns and reframes the whole situation",
}

def card_element(card_name: str) -> str:
    name = card_name.lower()
    if any(w in name for w in ["wand", "fire", "aries", "leo", "sagittarius"]): return "fire"
    if any(w in name for w in ["cup", "water", "pisces", "cancer", "scorpio"]): return "water"
    if any(w in name for w in ["sword", "air", "gemini", "libra", "aquarius"]): return "air"
    if any(w in name for w in ["pentacle", "coin", "earth", "taurus", "virgo", "capricorn"]): return "earth"
    return "major"  # Major Arcana

def rotate_label(concept: str, slug: str) -> str:
    from tarot_seo_data import POSITION_SYNONYMS
    idx = int(hashlib.md5(slug.encode()).hexdigest(), 16) % 5
    return POSITION_SYNONYMS.get(concept, ["Position"])[idx]

# ── Data loaders ──────────────────────────────────────────────────────────────
from tarot_seo_data import (
    list_card_summaries, get_card,
    get_spread, SPREAD_INTENT_CATEGORY,
    PRIORITIZED_SPREAD_SLUGS,
)

def get_intent_sentence(card: dict, category: str) -> str:
    if category == "love":
        return card.get("love", "")
    elif category == "career":
        return card.get("career", "")
    elif category == "health":
        return card.get("health", "")
    else:
        upright = card.get("upright", "")
        return upright.split(".")[0] + "." if "." in upright else upright[:80]

# ── Page builders ─────────────────────────────────────────────────────────────
def build_old_page(card: dict, spread: dict) -> str:
    """Non-compliant template: generic opener + full upright repeated per page."""
    return (
        f"{card['name']} energy meets the {spread['title']} intent. "
        f"{spread.get('purpose', '')} "
        f"Position 1: Past. {card.get('upright', '')}"
    )

def build_new_page(card: dict, spread: dict, card_slug: str) -> str:
    """
    Compliant architecture (simulates TAR-M4 output):
      1. Spread-purpose-led title (unique per spread)
      2. Elemental intersection synthesis (unique per card×spread)
      3. Rotated position label (unique per slug)
      4. ONE intent-matched card sentence only
    """
    slug = f"{card_slug}-{spread['slug']}"
    category = SPREAD_INTENT_CATEGORY.get(spread["slug"], "general")
    intent_sentence = get_intent_sentence(card, category)
    element = card_element(card["name"])
    phrase = ELEMENT_PHRASES.get((element, category),
                                  f"{element} energy meets {category} guidance")
    past_label = rotate_label("past", slug)

    return (
        f"{spread['title']} with {card['name']}. "
        f"When {phrase}, {spread.get('purpose', '')[:200]} "
        f"{past_label}: {intent_sentence}"
    )

# ── Benchmark ─────────────────────────────────────────────────────────────────
def worst_similarity(pages: list[str]) -> float:
    if len(pages) < 2:
        return 0.0
    mat = vectorizer.fit_transform(pages)
    sim = cosine_similarity(mat)
    n = len(pages)
    return max(sim[i][j] for i in range(n) for j in range(i + 1, n)) * 100

def run_benchmark() -> bool:
    random.seed(42)
    all_cards = list_card_summaries()
    sample_cards = random.sample(all_cards, min(SAMPLE_CARDS, len(all_cards)))

    # Use spreads that cover ALL 4 categories for maximum diversity stress test
    spread_slugs_by_cat = {"love": [], "career": [], "health": [], "general": []}
    for slug in PRIORITIZED_SPREAD_SLUGS:
        cat = SPREAD_INTENT_CATEGORY.get(slug, "general")
        if cat in spread_slugs_by_cat and len(spread_slugs_by_cat[cat]) < 2:
            spread_slugs_by_cat[cat].append(slug)

    selected_spread_slugs = (
        spread_slugs_by_cat["love"] + spread_slugs_by_cat["career"] +
        spread_slugs_by_cat["health"] + spread_slugs_by_cat["general"]
    )[:SAMPLE_SPREADS]

    old_pages, new_pages = [], []
    for card_info in sample_cards:
        card = get_card(card_info["slug"])
        if not card:
            continue
        for spread_slug in selected_spread_slugs:
            spread = get_spread(spread_slug)
            if not spread:
                continue
            old_pages.append(build_old_page(card, spread))
            new_pages.append(build_new_page(card, spread, card_info["slug"]))

    old_worst = worst_similarity(old_pages)
    new_worst = worst_similarity(new_pages)

    print("\n" + "=" * 58)
    print("  ECHO // PACE  COMBINATION PAGE COMPLIANCE BENCHMARK")
    print("=" * 58)
    print(f"  Pages sampled:      {len(new_pages)}  ({SAMPLE_CARDS} cards × {SAMPLE_SPREADS} spreads)")
    print(f"  Similarity ceiling: {SIMILARITY_CEILING}%")
    print("-" * 58)
    print(f"  ❌ BEFORE (template approach):   {old_worst:5.1f}% worst-pair")
    print(f"  ✅ AFTER  (anchor-flip + elemental): {new_worst:5.1f}% worst-pair")
    print("-" * 58)

    if new_worst < SIMILARITY_CEILING:
        print(f"  🎉 PASS -- {new_worst:.1f}% < {SIMILARITY_CEILING}% ceiling")
        print("      TAR-M4 architecture is compliant. Safe to issue to Codex.")
    else:
        print(f"  ❌ FAIL -- {new_worst:.1f}% ≥ {SIMILARITY_CEILING}% ceiling")
        print("      Increase elemental synthesis diversity before seeding.")
    print("=" * 58 + "\n")
    return new_worst < SIMILARITY_CEILING

if __name__ == "__main__":
    passed = run_benchmark()
    sys.exit(0 if passed else 1)
