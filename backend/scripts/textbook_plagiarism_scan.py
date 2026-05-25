#!/usr/bin/env python3
"""
TextBook Plagiarism Scanner
============================
Compares SEO content fields against source EPUB/textbook files using
TF-IDF + Cosine Similarity to detect verbatim copying before content
is seeded to production.

Usage (standalone):
    python3 scripts/textbook_plagiarism_scan.py \
        --epub "/path/to/source.epub" \
        --module tarot \
        --threshold 0.70

Usage (programmatic):
    from scripts.textbook_plagiarism_scan import scan_module
    results = scan_module(epub_path, seo_texts, labels, threshold=0.70)

Dependencies:
    pip install scikit-learn ebooklib beautifulsoup4

Score interpretation:
    >= 95%  Verbatim -- exact sentence from book. DO NOT SEED. Rewrite required.
    80-94%  High risk -- near-verbatim. Flag for human review before proceeding.
    70-79%  Moderate -- possible paraphrase. Review recommended.
    < 70%   Clean -- original prose. Safe to proceed through ECHO//PACE pipeline.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

try:
    from ebooklib import epub, ITEM_DOCUMENT
    from bs4 import BeautifulSoup
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction import text as sk_text
    import numpy as np
except ImportError as e:
    print(f"ERROR: Missing dependency -- {e}")
    print("Run: pip install scikit-learn ebooklib beautifulsoup4")
    sys.exit(1)


# ── Custom stop words: strip textbook boilerplate that causes false positives ──
_ACADEMIC_BOILERPLATE = [
    "chapter", "section", "figure", "table", "index", "appendix",
    "illustrated", "discussed", "concluding", "exercise", "problem",
    "spread", "card", "tarot", "reading", "cards", "position",
]
CUSTOM_STOP_WORDS = list(sk_text.ENGLISH_STOP_WORDS.union(_ACADEMIC_BOILERPLATE))


def parse_epub(epub_path: str, min_length: int = 60) -> list[str]:
    """Extract clean paragraphs from an EPUB file."""
    book = epub.read_epub(epub_path)
    paragraphs: list[str] = []
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        for tag in soup.find_all(["p", "li"]):
            txt = re.sub(r"\s+", " ", tag.get_text(separator=" ").strip())
            if len(txt) >= min_length:
                paragraphs.append(txt)
    return paragraphs


def scan_module(
    epub_paragraphs: list[str],
    seo_entries: list[dict[str, str]],
    threshold: float = 0.70,
) -> dict[str, Any]:
    """
    Run cosine similarity scan.

    Args:
        epub_paragraphs: list of strings extracted from the source book
        seo_entries: list of dicts with keys: slug, field, text, label
        threshold: similarity score above which entry is flagged

    Returns:
        dict with keys: flagged, clean, score_distribution, summary
    """
    seo_texts = [e["text"] for e in seo_entries]
    n_epub = len(epub_paragraphs)

    vectorizer = TfidfVectorizer(
        stop_words=CUSTOM_STOP_WORDS,
        ngram_range=(1, 2),
        min_df=1,
        max_features=30_000,
    )
    all_docs = epub_paragraphs + seo_texts
    tfidf = vectorizer.fit_transform(all_docs)

    epub_matrix = tfidf[:n_epub]
    seo_matrix  = tfidf[n_epub:]
    similarity  = cosine_similarity(seo_matrix, epub_matrix)

    flagged: list[dict[str, Any]] = []
    clean:   list[dict[str, Any]] = []

    for i, entry in enumerate(seo_entries):
        score = float(np.max(similarity[i]))
        best_para_idx = int(np.argmax(similarity[i]))
        result = {
            **entry,
            "score": round(score, 3),
            "score_pct": f"{int(score * 100)}%",
            "best_epub_match": epub_paragraphs[best_para_idx],
        }
        if score >= threshold:
            flagged.append(result)
        else:
            clean.append(result)

    flagged.sort(key=lambda x: -x["score"])
    clean.sort(key=lambda x: x["score"])

    buckets = {
        "verbatim_95_plus": sum(1 for r in flagged if r["score"] >= 0.95),
        "high_risk_80_94":  sum(1 for r in flagged if 0.80 <= r["score"] < 0.95),
        "moderate_70_79":   sum(1 for r in flagged if 0.70 <= r["score"] < 0.80),
        "clean_below_70":   len(clean),
    }

    return {
        "flagged": flagged,
        "clean": clean,
        "score_distribution": buckets,
        "total": len(seo_entries),
        "flagged_count": len(flagged),
        "clean_count": len(clean),
    }


def _load_tarot_entries() -> list[dict[str, str]]:
    """Load purpose + when fields from tarot_seo_data.py."""
    from tarot_seo_data import list_spread_summaries, get_spread
    entries = []
    for item in list_spread_summaries():
        spread = get_spread(item["slug"])
        if not spread:
            continue
        for field in ("purpose", "when"):
            text = spread.get(field, "")
            if text:
                entries.append({
                    "slug": item["slug"],
                    "field": field,
                    "label": f"{item['title']} [{field}]",
                    "text": text,
                })
    return entries


SUPPORTED_MODULES = {
    "tarot": {
        "loader": _load_tarot_entries,
        "default_epub": (
            "/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Tarot/"
            "1001-tarot-spreads-the-complete-book-of-tarot-spreads-for-every-purpose.epub"
        ),
    },
    # Add future modules here:
    # "faith": {"loader": _load_faith_entries, "default_epub": "..."},
    # "crystal": {"loader": _load_crystal_entries, "default_epub": "..."},
}


def _print_report(results: dict[str, Any], module: str, threshold: float) -> None:
    dist = results["score_distribution"]
    print(f"\n{'='*70}")
    print(f"TEXTBOOK PLAGIARISM SCAN -- Module: {module.upper()}")
    print(f"Threshold: {int(threshold*100)}% | Total fields: {results['total']}")
    print(f"{'='*70}")
    print(f"\nScore Distribution:")
    print(f"  🔴 Verbatim  (≥95%): {dist['verbatim_95_plus']:4d} fields")
    print(f"  🟠 High Risk (80-94%): {dist['high_risk_80_94']:4d} fields")
    print(f"  🟡 Moderate  (70-79%): {dist['moderate_70_79']:4d} fields")
    print(f"  ✅ Clean     (<70%):  {dist['clean_below_70']:4d} fields")
    print(f"\n  TOTAL FLAGGED: {results['flagged_count']} / {results['total']}")

    if results["flagged"]:
        print(f"\n{'─'*70}")
        print("WORST OFFENDERS (top 10):")
        for r in results["flagged"][:10]:
            print(f"\n  {r['score_pct']:>4} | {r['label'][:55]}")
            print(f"       SEO:  {r['text'][:90]}")
            print(f"       EPUB: {r['best_epub_match'][:90]}")

    if results["clean"]:
        print(f"\n{'─'*70}")
        print("CLEAN ENTRIES (lowest similarity -- safe to proceed):")
        for r in results["clean"][:5]:
            print(f"  {r['score_pct']:>4} | {r['label'][:60]}")

    print(f"\n{'='*70}")
    verdict = (
        "🔴 BLOCKED -- Rewrite required before seeding."
        if dist["verbatim_95_plus"] > 0 else
        "🟡 FLAGGED -- Human review recommended before seeding."
        if results["flagged_count"] > 0 else
        "✅ CLEAN -- Content passes plagiarism check. Proceed to ECHO//PACE."
    )
    print(f"VERDICT: {verdict}")
    print(f"{'='*70}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="TextBook Plagiarism Scanner")
    parser.add_argument("--module", choices=list(SUPPORTED_MODULES.keys()), required=True)
    parser.add_argument("--epub", type=str, default=None, help="Path to source EPUB")
    parser.add_argument("--threshold", type=float, default=0.70, help="Flag threshold (default: 0.70)")
    parser.add_argument("--min-para-len", type=int, default=60, help="Min chars per EPUB paragraph")
    args = parser.parse_args()

    mod = SUPPORTED_MODULES[args.module]
    epub_path = args.epub or mod["default_epub"]

    print(f"Parsing EPUB: {epub_path}")
    paragraphs = parse_epub(epub_path, min_length=args.min_para_len)
    print(f"Extracted {len(paragraphs)} paragraphs from source book.")

    print(f"Loading SEO entries for module: {args.module}")
    entries = mod["loader"]()
    print(f"Loaded {len(entries)} SEO content fields.")

    print("Running TF-IDF cosine similarity scan...")
    results = scan_module(paragraphs, entries, threshold=args.threshold)

    _print_report(results, args.module, args.threshold)


if __name__ == "__main__":
    main()
