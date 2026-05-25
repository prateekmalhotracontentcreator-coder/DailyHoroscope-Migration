#!/usr/bin/env python3
"""
TextBook Plagiarism Scanner v2
================================
Compares SEO content fields against source EPUB/textbook files using
three independent inspection layers before content is seeded to production.

LAYER 1 -- TF-IDF Cosine Similarity
    Holistic structural similarity. Catches overall template copying and
    near-verbatim paraphrasing even when individual words are swapped.

LAYER 2 -- N-gram Sequential Phrase Match
    Exact phrase check. Flags any SEO sentence containing 4+ consecutive
    words that appear verbatim in the source book. Catches copy-paste that
    escaped the cosine check (e.g. one lifted sentence inside original prose).

LAYER 3 -- Heading / Title Match
    Checks SEO page titles, spread names, category names against EPUB
    headings (h1/h2/h3). Flags exact or near-exact title matches that
    should be AI-humanised to avoid appearing as scraped chapter indexes.

SCORE THRESHOLDS (upgraded from v1):
    BLOCKED  ≥70%   →  Send back to Codex for full rewrite. Do not seed.
    FLAGGED  50-69% →  Human review required before proceeding.
    CLEAN    <50%   →  AND passes n-gram check (no 4+ word sequences copied)
                        → Safe to proceed through ECHO//PACE pipeline.

PUBLIC DOMAIN MODULE FLAG:
    Modules with public_domain_source=True (Bible KJV, Bhagavad Gita) skip
    cosine + n-gram checks on scripture quote fields. Only interpretation /
    commentary fields are scanned. ECHO//PACE humanises only those fields.

Usage:
    python3 scripts/textbook_plagiarism_scan.py --module tarot
    python3 scripts/textbook_plagiarism_scan.py --module tarot --threshold 0.70
    python3 scripts/textbook_plagiarism_scan.py --module faith --epub /path/to/kjv.epub

Dependencies:
    pip install scikit-learn ebooklib beautifulsoup4
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
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


# ── Stop words -- strip boilerplate that creates false positives ─────────────
_ACADEMIC_BOILERPLATE = [
    "chapter", "section", "figure", "table", "index", "appendix",
    "illustrated", "discussed", "concluding", "exercise", "problem",
    "spread", "card", "tarot", "reading", "cards", "position",
]
CUSTOM_STOP_WORDS = list(sk_text.ENGLISH_STOP_WORDS.union(_ACADEMIC_BOILERPLATE))

# ── Threshold defaults ───────────────────────────────────────────────────────
DEFAULT_BLOCK_THRESHOLD  = 0.70   # ≥70% → BLOCKED
DEFAULT_FLAG_THRESHOLD   = 0.50   # 50-69% → FLAGGED
DEFAULT_NGRAM_MIN        = 4      # minimum consecutive words to flag


# ══════════════════════════════════════════════════════════════════════════════
# EPUB PARSING
# ══════════════════════════════════════════════════════════════════════════════

def parse_epub(epub_path: str, min_length: int = 60) -> dict[str, list[str]]:
    """
    Parse EPUB. Returns dict with:
        paragraphs: body text paragraphs (used for cosine + n-gram checks)
        headings:   h1/h2/h3 heading text (used for title match check)
    """
    book = epub.read_epub(epub_path)
    paragraphs: list[str] = []
    headings:   list[str] = []

    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")

        for tag in soup.find_all(["h1", "h2", "h3"]):
            txt = re.sub(r"\s+", " ", tag.get_text(separator=" ").strip())
            if len(txt) > 4:
                headings.append(txt.lower())

        for tag in soup.find_all(["p", "li"]):
            txt = re.sub(r"\s+", " ", tag.get_text(separator=" ").strip())
            if len(txt) >= min_length:
                paragraphs.append(txt)

    return {"paragraphs": paragraphs, "headings": headings}


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 1 -- TF-IDF COSINE SIMILARITY
# ══════════════════════════════════════════════════════════════════════════════

def _cosine_scan(
    epub_paragraphs: list[str],
    seo_entries: list[dict[str, str]],
    block_threshold: float,
    flag_threshold: float,
) -> list[dict[str, Any]]:
    """Return per-entry cosine similarity score and best matching EPUB paragraph."""
    seo_texts = [e["text"] for e in seo_entries]
    all_docs  = epub_paragraphs + seo_texts
    n_epub    = len(epub_paragraphs)

    vectorizer = TfidfVectorizer(
        stop_words=CUSTOM_STOP_WORDS,
        ngram_range=(1, 2),
        min_df=1,
        max_features=30_000,
    )
    tfidf  = vectorizer.fit_transform(all_docs)
    sim    = cosine_similarity(tfidf[n_epub:], tfidf[:n_epub])

    results = []
    for i, entry in enumerate(seo_entries):
        score         = float(np.max(sim[i]))
        best_idx      = int(np.argmax(sim[i]))
        cosine_status = (
            "BLOCKED"  if score >= block_threshold else
            "FLAGGED"  if score >= flag_threshold  else
            "CLEAN"
        )
        results.append({
            **entry,
            "cosine_score":      round(score, 3),
            "cosine_score_pct":  f"{int(score * 100)}%",
            "cosine_status":     cosine_status,
            "best_epub_para":    epub_paragraphs[best_idx],
        })
    return results


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 2 -- N-GRAM SEQUENTIAL PHRASE MATCH
# ══════════════════════════════════════════════════════════════════════════════

_STOP_SET: set[str] = set(sk_text.ENGLISH_STOP_WORDS) | {
    # Extra common connective words that appear in any sentence
    "use", "used", "using", "spread", "card", "cards", "tarot",
    "reading", "readings", "layout", "position", "positions",
}


def _tokenise(text: str, remove_stops: bool = True) -> list[str]:
    """
    Lowercase, strip punctuation, split into word tokens.
    When remove_stops=True, filters out stop words so only MEANINGFUL words
    remain for n-gram matching. This prevents common English phrases like
    'when you want to' from triggering false positives.
    """
    tokens = re.findall(r"\b[a-z]{2,}\b", text.lower())
    if remove_stops:
        tokens = [t for t in tokens if t not in _STOP_SET]
    return tokens


def _build_ngram_set(paragraphs: list[str], n: int) -> set[tuple[str, ...]]:
    """Build a set of all n-grams (as tuples) from the given paragraphs."""
    ngrams: set[tuple[str, ...]] = set()
    for para in paragraphs:
        tokens = _tokenise(para)
        for i in range(len(tokens) - n + 1):
            ngrams.add(tuple(tokens[i: i + n]))
    return ngrams


def _find_longest_match(
    text: str,
    ngram_sets: dict[int, set[tuple[str, ...]]],
    min_n: int,
    max_n: int = 12,
) -> tuple[int, str]:
    """
    Find the longest consecutive word sequence in `text` that appears in the
    EPUB n-gram sets.  Returns (length, matched_phrase).  0 = no match.
    """
    tokens = _tokenise(text)
    best_len    = 0
    best_phrase = ""

    for n in range(max_n, min_n - 1, -1):
        if n not in ngram_sets:
            continue
        for i in range(len(tokens) - n + 1):
            gram = tuple(tokens[i: i + n])
            if gram in ngram_sets[n]:
                if n > best_len:
                    best_len    = n
                    best_phrase = " ".join(gram)
    return best_len, best_phrase


def _ngram_scan(
    epub_paragraphs: list[str],
    seo_entries: list[dict[str, str]],
    min_n: int = DEFAULT_NGRAM_MIN,
) -> list[dict[str, Any]]:
    """Annotate each entry with its longest sequential phrase match from EPUB."""
    # Pre-build n-gram sets for n = min_n ... 12
    print(f"  Building n-gram sets (n={min_n}-12) from {len(epub_paragraphs)} paragraphs...")
    ngram_sets: dict[int, set[tuple[str, ...]]] = {}
    for n in range(min_n, 13):
        ngram_sets[n] = _build_ngram_set(epub_paragraphs, n)

    results = []
    for entry in seo_entries:
        best_len, best_phrase = _find_longest_match(
            entry["text"], ngram_sets, min_n=min_n
        )
        ngram_status = "BLOCKED" if best_len >= min_n else "CLEAN"
        results.append({
            **entry,
            "ngram_longest_match": best_len,
            "ngram_matched_phrase": best_phrase,
            "ngram_status": ngram_status,
        })
    return results


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 3 -- HEADING / TITLE MATCH
# ══════════════════════════════════════════════════════════════════════════════

def _heading_similarity(a: str, b: str) -> float:
    """Simple word-overlap Jaccard similarity between two heading strings."""
    wa = set(re.findall(r"\b[a-z]{3,}\b", a.lower()))
    wb = set(re.findall(r"\b[a-z]{3,}\b", b.lower()))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def _title_scan(
    epub_headings: list[str],
    seo_entries: list[dict[str, str]],
    flag_threshold: float = 0.80,
) -> list[dict[str, Any]]:
    """
    Check SEO title fields against EPUB headings.
    Only processes entries where field='title'.
    """
    results = []
    for entry in seo_entries:
        if entry.get("field") != "title":
            results.append({**entry, "title_status": "SKIP", "title_best_match": "", "title_score": 0.0})
            continue

        seo_title = entry["text"].lower()
        best_score = 0.0
        best_match = ""
        for h in epub_headings:
            score = _heading_similarity(seo_title, h)
            if score > best_score:
                best_score = score
                best_match = h

        title_status = "FLAGGED" if best_score >= flag_threshold else "CLEAN"
        results.append({
            **entry,
            "title_score":      round(best_score, 3),
            "title_best_match": best_match,
            "title_status":     title_status,
        })
    return results


# ══════════════════════════════════════════════════════════════════════════════
# COMBINED SCAN
# ══════════════════════════════════════════════════════════════════════════════

def scan_module(
    epub_data: dict[str, list[str]],
    seo_entries: list[dict[str, str]],
    block_threshold: float = DEFAULT_BLOCK_THRESHOLD,
    flag_threshold:  float = DEFAULT_FLAG_THRESHOLD,
    ngram_min:       int   = DEFAULT_NGRAM_MIN,
    title_threshold: float = 0.80,
    public_domain:   bool  = False,
) -> dict[str, Any]:
    """
    Run all three inspection layers.

    For public_domain modules:
        - Cosine + n-gram checks run ONLY on fields tagged is_interpretation=True
        - Title check still runs on all title fields
        - Scripture quote fields are skipped (they're intentionally verbatim -- that's fine)

    Args:
        epub_data:        output of parse_epub()
        seo_entries:      list of dicts with keys: slug, field, text, label,
                          and optionally is_interpretation (bool)
        block_threshold:  cosine score at/above which entry is BLOCKED
        flag_threshold:   cosine score at/above which entry is FLAGGED
        ngram_min:        minimum consecutive words to flag in n-gram check
        title_threshold:  Jaccard similarity at/above which title is FLAGGED
        public_domain:    if True, only scan is_interpretation=True entries

    Returns:
        dict with full per-entry results + aggregated summary
    """
    epub_paragraphs = epub_data["paragraphs"]
    epub_headings   = epub_data["headings"]

    # For public domain: split into scan-eligible and scripture-skipped
    if public_domain:
        scan_entries  = [e for e in seo_entries if e.get("is_interpretation", False)]
        skip_entries  = [e for e in seo_entries if not e.get("is_interpretation", False)]
    else:
        scan_entries  = seo_entries
        skip_entries  = []

    # Cosine + n-gram only run on BODY content fields (not title fields).
    # Short title strings distort TF-IDF weights when mixed with paragraph text.
    # Titles are handled exclusively by Layer 3 (Jaccard heading match) + Layer 2 (n-gram).
    body_entries  = [e for e in scan_entries  if e.get("field") != "title"]
    title_entries = [e for e in scan_entries  if e.get("field") == "title"]
    # skip_entries are never body/title scanned (public domain scripture)

    print(f"\nLayer 1: TF-IDF Cosine Similarity ({len(body_entries)} body entries)...")
    cosine_results = _cosine_scan(epub_paragraphs, body_entries, block_threshold, flag_threshold)

    print(f"Layer 2: N-gram Sequential Phrase Match (min {ngram_min} words) -- body + titles...")
    # N-gram runs on BOTH body and title content (catches verbatim title copying)
    ngram_body   = _ngram_scan(epub_paragraphs, cosine_results, min_n=ngram_min)
    ngram_titles = _ngram_scan(epub_paragraphs, title_entries,  min_n=ngram_min)

    print(f"Layer 3: Heading / Title Match ({len(seo_entries)} total entries)...")
    # Title scan (Jaccard) runs on ALL entries (body, titles, and skipped scripture)
    title_scan_all = _title_scan(epub_headings, ngram_body + ngram_titles + skip_entries, title_threshold)

    # ── Determine final verdict per entry ────────────────────────────────────
    final_results = []
    for r in title_scan_all:
        cosine_ok  = r.get("cosine_status", "SKIP") in ("CLEAN", "SKIP")
        ngram_ok   = r.get("ngram_status", "SKIP")  in ("CLEAN", "SKIP")
        title_ok   = r.get("title_status", "SKIP")  in ("CLEAN", "SKIP", "SKIP")

        if r.get("cosine_status") == "BLOCKED" or r.get("ngram_status") == "BLOCKED":
            verdict = "BLOCKED"
        elif r.get("cosine_status") == "FLAGGED" or r.get("title_status") == "FLAGGED":
            verdict = "FLAGGED"
        else:
            verdict = "CLEAN"

        final_results.append({**r, "verdict": verdict})

    # ── Aggregate stats ───────────────────────────────────────────────────────
    blocked = [r for r in final_results if r["verdict"] == "BLOCKED"]
    flagged = [r for r in final_results if r["verdict"] == "FLAGGED"]
    clean   = [r for r in final_results if r["verdict"] == "CLEAN"]

    # Break down BLOCKED reason
    blocked_cosine = [r for r in blocked if r.get("cosine_status") == "BLOCKED"]
    blocked_ngram  = [r for r in blocked if r.get("ngram_status")  == "BLOCKED"
                      and r.get("cosine_status") != "BLOCKED"]

    dist = {
        "blocked_total":        len(blocked),
        "blocked_by_cosine":    len(blocked_cosine),
        "blocked_by_ngram":     len(blocked_ngram),
        "flagged_total":        len(flagged),
        "flagged_by_cosine":    sum(1 for r in flagged if r.get("cosine_status") == "FLAGGED"),
        "flagged_by_title":     sum(1 for r in flagged if r.get("title_status")  == "FLAGGED"),
        "clean_total":          len(clean),
        "skipped_public_domain": len(skip_entries),
    }

    blocked.sort(key=lambda x: -x.get("cosine_score", 0))
    flagged.sort(key=lambda x: -x.get("cosine_score", 0))

    return {
        "all":          final_results,
        "blocked":      blocked,
        "flagged":      flagged,
        "clean":        clean,
        "distribution": dist,
        "total":        len(seo_entries),
    }


# ══════════════════════════════════════════════════════════════════════════════
# REPORT PRINTER
# ══════════════════════════════════════════════════════════════════════════════

def print_report(results: dict[str, Any], module: str, thresholds: dict) -> None:
    dist = results["distribution"]
    total = results["total"]

    print(f"\n{'='*72}")
    print(f"TEXTBOOK PLAGIARISM SCAN v2 -- Module: {module.upper()}")
    print(f"Thresholds: BLOCKED≥{int(thresholds['block']*100)}%  FLAGGED≥{int(thresholds['flag']*100)}%  N-gram≥{thresholds['ngram']} words")
    print(f"{'='*72}")

    print(f"""
  Layer 1 + 2 (Cosine + N-gram):
    🔴 BLOCKED -- {dist['blocked_total']:4d} entries  ({dist['blocked_by_cosine']} cosine ≥{int(thresholds['block']*100)}%  |  {dist['blocked_by_ngram']} n-gram phrase)
    🟡 FLAGGED -- {dist['flagged_total']:4d} entries  ({dist['flagged_by_cosine']} cosine 50-69%  |  {dist['flagged_by_title']} title match)
    ✅ CLEAN   -- {dist['clean_total']:4d} entries  (cosine <{int(thresholds['flag']*100)}% AND no {thresholds['ngram']}+ word phrases)
    ⚪ SKIPPED -- {dist['skipped_public_domain']:4d} entries  (public domain scripture -- not scanned)
    ─────────────────────────────────────
    TOTAL: {total} entries""")

    # ── BLOCKED detail ────────────────────────────────────────────────────────
    if results["blocked"]:
        print(f"\n{'─'*72}")
        print("🔴 BLOCKED ENTRIES (top 15) -- Rewrite required:")
        for r in results["blocked"][:15]:
            reason = []
            if r.get("cosine_status") == "BLOCKED":
                reason.append(f"cosine {r['cosine_score_pct']}")
            if r.get("ngram_status") == "BLOCKED":
                reason.append(f"n-gram [{r['ngram_longest_match']} words: \"{r['ngram_matched_phrase'][:40]}\"")
            print(f"\n  [{', '.join(reason)}]")
            print(f"  {r['label'][:60]}")
            print(f"  SEO:  {r['text'][:90]}")
            if r.get("cosine_status") == "BLOCKED":
                print(f"  EPUB: {r['best_epub_para'][:90]}")

    # ── FLAGGED detail ────────────────────────────────────────────────────────
    if results["flagged"]:
        print(f"\n{'─'*72}")
        print("🟡 FLAGGED ENTRIES -- Human review before proceeding:")
        for r in results["flagged"][:10]:
            reason = []
            if r.get("cosine_status") == "FLAGGED":
                reason.append(f"cosine {r['cosine_score_pct']}")
            if r.get("title_status") == "FLAGGED":
                reason.append(f"title match {int(r.get('title_score',0)*100)}%: \"{r['title_best_match'][:40]}\"")
            print(f"  [{', '.join(reason)}] {r['label'][:55]}")

    # ── N-gram summary ────────────────────────────────────────────────────────
    ngram_catches = [r for r in results["blocked"] if r.get("ngram_status") == "BLOCKED"
                     and r.get("cosine_status") != "BLOCKED"]
    if ngram_catches:
        print(f"\n{'─'*72}")
        print(f"N-GRAM EXCLUSIVE CATCHES (passed cosine, caught by phrase check):")
        for r in ngram_catches[:8]:
            print(f"  [{r['ngram_longest_match']} words] {r['label'][:50]}")
            print(f"    Phrase: \"{r['ngram_matched_phrase']}\"")
            print(f"    Text:   {r['text'][:80]}")

    # ── CLEAN sample ──────────────────────────────────────────────────────────
    if results["clean"]:
        print(f"\n{'─'*72}")
        print("✅ CLEAN SAMPLE (lowest cosine -- original prose):")
        for r in results["clean"][:5]:
            print(f"  {r.get('cosine_score_pct','--'):>4} | {r['label'][:60]}")

    # ── Overall verdict ───────────────────────────────────────────────────────
    print(f"\n{'='*72}")
    if dist["blocked_total"] > 0:
        verdict = f"🔴 BLOCKED -- {dist['blocked_total']} entries must be rewritten before seeding."
    elif dist["flagged_total"] > 0:
        verdict = f"🟡 FLAGGED -- {dist['flagged_total']} entries need human review before proceeding."
    else:
        verdict = "✅ CLEAN -- All entries pass. Proceed to ECHO//PACE humanisation pipeline."
    print(f"VERDICT: {verdict}")
    print(f"{'='*72}\n")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE LOADERS
# ══════════════════════════════════════════════════════════════════════════════

def _load_tarot_entries() -> list[dict[str, str]]:
    """Load purpose + when fields from tarot_seo_data.py."""
    from tarot_seo_data import list_spread_summaries, get_spread
    entries = []
    for item in list_spread_summaries():
        # Title check
        entries.append({
            "slug": item["slug"], "field": "title",
            "label": f"{item['title']} [title]", "text": item["title"],
        })
        spread = get_spread(item["slug"])
        if not spread:
            continue
        for field in ("purpose", "when"):
            text = spread.get(field, "")
            if text:
                entries.append({
                    "slug": item["slug"], "field": field,
                    "label": f"{item['title']} [{field}]", "text": text,
                    "is_interpretation": True,
                })
    return entries


def _load_faith_entries() -> list[dict[str, str]]:
    """
    Load Faith module fields.
    Scripture quote fields are marked is_interpretation=False (skipped).
    Commentary/interpretation fields are marked is_interpretation=True (scanned).
    To be implemented when FAITH-1 is delivered.
    """
    raise NotImplementedError(
        "Faith module loader not yet implemented. "
        "Implement after FAITH-1 is delivered from Codex."
    )


SUPPORTED_MODULES: dict[str, dict] = {
    "tarot": {
        "loader": _load_tarot_entries,
        "public_domain": False,
        "default_epub": (
            "/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Tarot/"
            "1001-tarot-spreads-the-complete-book-of-tarot-spreads-for-every-purpose.epub"
        ),
        "description": "Tarot spreads -- purpose + when + title fields vs source EPUB",
    },
    "faith": {
        "loader": _load_faith_entries,
        "public_domain": True,           # KJV Bible = public domain
        "default_epub": None,            # Set via --epub flag
        "description": "Faith module -- only interpretation fields scanned (KJV scripture = public domain)",
    },
    # Future modules:
    # "crystal": {"loader": _load_crystal_entries, "public_domain": False, "default_epub": "..."},
    # "gita":    {"loader": _load_gita_entries,   "public_domain": True,  "default_epub": "..."},
}


# ══════════════════════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="TextBook Plagiarism Scanner v2 -- Three-layer copyright check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--module",   choices=list(SUPPORTED_MODULES.keys()), required=True)
    parser.add_argument("--epub",     type=str, default=None, help="Path to source EPUB (overrides default)")
    parser.add_argument("--block",    type=float, default=DEFAULT_BLOCK_THRESHOLD,  help="Cosine BLOCKED threshold (default 0.70)")
    parser.add_argument("--flag",     type=float, default=DEFAULT_FLAG_THRESHOLD,   help="Cosine FLAGGED threshold (default 0.50)")
    parser.add_argument("--ngram",    type=int,   default=DEFAULT_NGRAM_MIN,        help="Min consecutive words for n-gram flag (default 4)")
    parser.add_argument("--title-threshold", type=float, default=0.80,             help="Title Jaccard similarity threshold (default 0.80)")
    parser.add_argument("--min-para-len",    type=int,   default=60,               help="Min EPUB paragraph length in chars (default 60)")
    args = parser.parse_args()

    mod = SUPPORTED_MODULES[args.module]
    epub_path = args.epub or mod.get("default_epub")

    if not epub_path:
        print(f"ERROR: No EPUB path. Use --epub /path/to/file.epub")
        sys.exit(1)

    print(f"{'='*72}")
    print(f"Module: {args.module.upper()} -- {mod['description']}")
    print(f"Public domain source: {mod['public_domain']}")
    print(f"{'='*72}")

    print(f"\nParsing EPUB: {epub_path}")
    epub_data = parse_epub(epub_path, min_length=args.min_para_len)
    print(f"  Paragraphs: {len(epub_data['paragraphs'])}  |  Headings: {len(epub_data['headings'])}")

    print(f"\nLoading SEO entries...")
    entries = mod["loader"]()
    print(f"  Entries: {len(entries)}")

    thresholds = {
        "block": args.block,
        "flag":  args.flag,
        "ngram": args.ngram,
        "title": args.title_threshold,
    }

    results = scan_module(
        epub_data=epub_data,
        seo_entries=entries,
        block_threshold=args.block,
        flag_threshold=args.flag,
        ngram_min=args.ngram,
        title_threshold=args.title_threshold,
        public_domain=mod["public_domain"],
    )

    print_report(results, args.module, thresholds)


if __name__ == "__main__":
    main()
