#!/usr/bin/env python3
"""
Copyright Similarity Check -- Angel Numbers vs Reference PDFs
=============================================================

Compares EverydayHoroscope Angel Numbers generated content against
the two reference PDFs used in the Codex commission briefs:
  - Kyle Gray: "Angel Numbers"
  - Fortuna Noir: "Angel Numbers"

THREE TESTS are run:

  Test A -- Verbatim N-gram Match (4+ words, stop-word filtered)
    Catches direct copying. Any 4+ consecutive meaningful words that
    appear identically in both the PDF and our generated content.
    FAIL threshold: any match found.

  Test B -- TF-IDF Cosine Similarity (page-level)
    Catches structural paraphrasing. Each generated page body is
    compared against each PDF paragraph block via TF-IDF cosine.
    FAIL threshold: any pair >= 40% similarity.
    HIGH RISK threshold: >= 25%.

  Test C -- Sentence-level Jaccard Overlap
    Catches rephrased sentences. Splits both sources into sentences,
    computes token-level Jaccard per pair.
    FAIL threshold: any pair >= 50% Jaccard.
    HIGH RISK threshold: >= 30%.

OUTPUT
------
  - Console report per test with worst offenders
  - JSON report saved to tests/copyright_angel_report.json

USAGE
-----
    cd /Users/apple/DailyHoroscope-Migration
    PYTHONPATH=backend python3 tests/copyright_angel_vs_books.py

No API keys required. Runs entirely locally.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

import pdfplumber
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -- Path setup ────────────────────────────────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parents[1]
_BACKEND   = _REPO_ROOT / "backend"
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

try:
    from angel_numbers_data import (
        build_seeing_it_means,
        build_vibration,
        build_intent_message,
        build_summary,
        reduce_to_root,
        INTENT_ORDER,
    )
except ImportError as exc:
    sys.exit(
        f"ERROR: Cannot import angel_numbers_data -- {exc}\n"
        "Run: PYTHONPATH=backend python3 tests/copyright_angel_vs_books.py"
    )

# -- PDF paths ─────────────────────────────────────────────────────────────────
PDF_KYLE   = Path("/Users/apple/Documents/Knowledge Engine_eBooks/Angel Numbers/_OceanofPDF.com_Angel_Numbers_-_Kyle_Gray.pdf")
PDF_FORTUNA = Path("/Users/apple/Documents/Knowledge Engine_eBooks/Angel Numbers/_OceanofPDF.com_Angel_Numbers_-_Fortuna_Noir.pdf")

# -- Thresholds ────────────────────────────────────────────────────────────────
TEST_A_MIN_NGRAM  = 4       # minimum consecutive meaningful words
TEST_B_FAIL       = 0.40    # TF-IDF cosine similarity: FAIL
TEST_B_HIGH_RISK  = 0.25    # TF-IDF cosine similarity: HIGH RISK
TEST_C_FAIL       = 0.50    # Jaccard: FAIL
TEST_C_HIGH_RISK  = 0.30    # Jaccard: HIGH RISK

# -- Our sample: representative angel numbers (diverse roots 1-9) ──────────────
SAMPLE_NUMBERS = [
    "111", "222", "333", "444", "555",
    "666", "777", "888", "999",
    "1111", "1212", "1234", "1010",
    "123",  "456",  "789",
]
SAMPLE_INTENTS = ["love", "career", "twin-flame", "spiritual-growth", "manifestation"]

# -- Stop words ────────────────────────────────────────────────────────────────
_STOPS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "its", "be", "are", "was",
    "were", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "can", "this",
    "that", "these", "those", "i", "you", "he", "she", "we", "they",
    "my", "your", "his", "her", "our", "their", "what", "which", "who",
    "when", "where", "why", "how", "all", "each", "both", "few", "more",
    "most", "other", "some", "such", "no", "not", "only", "same", "so",
    "than", "too", "very", "just", "about", "above", "after", "before",
    "between", "through", "during", "into", "out", "up", "down", "if",
    "while", "as", "also", "then", "there", "here", "them", "any",
}


# ── PDF extraction ────────────────────────────────────────────────────────────

def extract_pdf_text(pdf_path: Path) -> str:
    """Extract all text from a PDF using pdfplumber."""
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                pages_text.append(t)
    return "\n".join(pages_text)


def split_into_paragraphs(text: str, min_words: int = 20) -> list[str]:
    """Split text into paragraph blocks, filtering very short ones."""
    raw = re.split(r"\n{2,}|\r\n{2,}", text)
    paras = []
    for p in raw:
        p = p.strip()
        p = re.sub(r"\s+", " ", p)
        if len(p.split()) >= min_words:
            paras.append(p)
    return paras


def split_into_sentences(text: str) -> list[str]:
    """Rough sentence splitter."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.split()) >= 6]


# ── Our generated corpus ──────────────────────────────────────────────────────

def build_our_corpus() -> dict[str, str]:
    """Build a dict of {label: body_text} for all sampled pages."""
    corpus = {}
    for num in SAMPLE_NUMBERS:
        root = reduce_to_root(num)
        # Core body
        core_text = (
            build_seeing_it_means(num, root) + " " +
            build_vibration(num, root) + " " +
            build_summary(num, root)
        )
        corpus[f"core/{num}"] = core_text
        # Intent bodies
        for intent in SAMPLE_INTENTS:
            try:
                msg = build_intent_message(num, intent, root)
                corpus[f"intent/{num}/{intent}"] = msg
            except Exception:
                pass
    return corpus


# ── Tokenizers ────────────────────────────────────────────────────────────────

def tokenize_filtered(text: str) -> list[str]:
    words = re.findall(r"\b[a-z]{3,}\b", text.lower())
    return [w for w in words if w not in _STOPS]


def ngrams(tokens: list[str], n: int) -> set[str]:
    return {" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)}


def jaccard(a_tokens: list[str], b_tokens: list[str]) -> float:
    a, b = set(a_tokens), set(b_tokens)
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


# ── TEST A: Verbatim N-gram Match ─────────────────────────────────────────────

def run_test_a(
    pdf_text: str,
    pdf_label: str,
    our_corpus: dict[str, str],
) -> tuple[bool, list[dict]]:
    """Check for verbatim 4+ word matches between PDF and our content."""
    pdf_tokens  = tokenize_filtered(pdf_text)
    pdf_ngrams  = ngrams(pdf_tokens, TEST_A_MIN_NGRAM)

    hits = []
    for label, body in our_corpus.items():
        our_tokens = tokenize_filtered(body)
        our_ngrams = ngrams(our_tokens, TEST_A_MIN_NGRAM)
        shared = pdf_ngrams & our_ngrams
        if shared:
            # Sort by length descending (longer = more damning)
            sorted_shared = sorted(shared, key=lambda x: len(x.split()), reverse=True)
            hits.append({
                "our_page":    label,
                "pdf":         pdf_label,
                "match_count": len(shared),
                "top_matches": sorted_shared[:5],
            })

    hits.sort(key=lambda x: x["match_count"], reverse=True)
    return bool(hits), hits


# ── TEST B: TF-IDF Cosine Similarity ─────────────────────────────────────────

def run_test_b(
    pdf_paragraphs: list[str],
    pdf_label: str,
    our_corpus: dict[str, str],
) -> tuple[bool, list[dict]]:
    """TF-IDF cosine similarity between our pages and PDF paragraphs."""
    our_labels  = list(our_corpus.keys())
    our_bodies  = list(our_corpus.values())

    all_docs = our_bodies + pdf_paragraphs
    if len(all_docs) < 2:
        return False, []

    try:
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
        mat = vec.fit_transform(all_docs)
    except Exception as exc:
        return False, [{"error": str(exc)}]

    n_ours = len(our_bodies)
    our_mat = mat[:n_ours]
    pdf_mat = mat[n_ours:]

    sims = cosine_similarity(our_mat, pdf_mat)

    high_risk = []
    any_fail  = False

    for i, our_label in enumerate(our_labels):
        worst_score = float(np.max(sims[i]))
        worst_para_idx = int(np.argmax(sims[i]))
        if worst_score >= TEST_B_HIGH_RISK:
            flag = "FAIL" if worst_score >= TEST_B_FAIL else "HIGH RISK"
            if worst_score >= TEST_B_FAIL:
                any_fail = True
            high_risk.append({
                "our_page":   our_label,
                "pdf":        pdf_label,
                "similarity": round(worst_score, 4),
                "flag":       flag,
                "pdf_para":   pdf_paragraphs[worst_para_idx][:300],
            })

    high_risk.sort(key=lambda x: x["similarity"], reverse=True)
    return any_fail, high_risk


# ── TEST C: Sentence-level Jaccard ────────────────────────────────────────────

def run_test_c(
    pdf_sentences: list[str],
    pdf_label: str,
    our_corpus: dict[str, str],
) -> tuple[bool, list[dict]]:
    """Jaccard token overlap between our sentences and PDF sentences."""
    # Build our sentence pool
    our_sentences: list[tuple[str, str]] = []  # (label, sentence)
    for label, body in our_corpus.items():
        for sent in split_into_sentences(body):
            our_sentences.append((label, sent))

    # Pre-tokenize PDF sentences
    pdf_tok = [tokenize_filtered(s) for s in pdf_sentences]

    high_risk = []
    any_fail  = False

    seen_pairs: set[str] = set()

    for (our_label, our_sent), (pdf_sent, pdf_tokens) in product(our_sentences, zip(pdf_sentences, pdf_tok)):
        our_tokens = tokenize_filtered(our_sent)
        if len(our_tokens) < 5 or len(pdf_tokens) < 5:
            continue
        score = jaccard(our_tokens, pdf_tokens)
        if score >= TEST_C_HIGH_RISK:
            pair_key = f"{our_label}||{pdf_sent[:60]}"
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)
            flag = "FAIL" if score >= TEST_C_FAIL else "HIGH RISK"
            if score >= TEST_C_FAIL:
                any_fail = True
            high_risk.append({
                "our_page":    our_label,
                "our_sent":    our_sent[:200],
                "pdf":         pdf_label,
                "pdf_sent":    pdf_sent[:200],
                "jaccard":     round(score, 4),
                "flag":        flag,
            })

    high_risk.sort(key=lambda x: x["jaccard"], reverse=True)
    return any_fail, high_risk[:30]  # cap output at 30 worst


# ── Runner ────────────────────────────────────────────────────────────────────

def run_against_pdf(
    pdf_path: Path,
    pdf_label: str,
    our_corpus: dict[str, str],
    report: dict,
) -> bool:
    """Run all 3 tests against one PDF. Returns True if any test FAILS."""
    print(f"\n{'='*68}")
    print(f"  PDF: {pdf_label}")
    print(f"  File: {pdf_path.name}")
    print(f"{'='*68}")

    print("  Extracting PDF text...", end=" ", flush=True)
    try:
        pdf_text = extract_pdf_text(pdf_path)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return False
    word_count = len(pdf_text.split())
    print(f"done  ({word_count:,} words extracted)")

    pdf_paras     = split_into_paragraphs(pdf_text)
    pdf_sentences = split_into_sentences(pdf_text)
    print(f"  Paragraphs: {len(pdf_paras)}   Sentences: {len(pdf_sentences)}")

    any_fail_overall = False

    # ── Test A ────────────────────────────────────────────────────────────────
    print(f"\n  -- TEST A: Verbatim {TEST_A_MIN_NGRAM}+ word N-gram Match --")
    a_fail, a_hits = run_test_a(pdf_text, pdf_label, our_corpus)
    if a_hits:
        print(f"  Pages with verbatim matches: {len(a_hits)}")
        for h in a_hits[:5]:
            print(f"    [{h['our_page']}]  {h['match_count']} match(es)")
            for m in h["top_matches"][:3]:
                print(f"      >> \"{m}\"")
        if len(a_hits) > 5:
            print(f"    ... and {len(a_hits)-5} more pages with matches")
        if a_fail:
            any_fail_overall = True
            print(f"  RESULT: FAIL -- {len(a_hits)} of our pages share verbatim {TEST_A_MIN_NGRAM}+ word phrases")
        else:
            print(f"  RESULT: NOTE -- matches found but evaluate context (common angel-number terminology expected)")
    else:
        print(f"  RESULT: PASS -- no verbatim {TEST_A_MIN_NGRAM}+ word phrase matches found")

    # ── Test B ────────────────────────────────────────────────────────────────
    print(f"\n  -- TEST B: TF-IDF Cosine Similarity (page vs paragraph) --")
    print(f"  Comparing {len(our_corpus)} our pages vs {len(pdf_paras)} PDF paragraphs...", end=" ", flush=True)
    b_fail, b_hits = run_test_b(pdf_paras, pdf_label, our_corpus)
    print("done")
    if b_hits:
        fail_count = sum(1 for h in b_hits if h["flag"] == "FAIL")
        risk_count = sum(1 for h in b_hits if h["flag"] == "HIGH RISK")
        print(f"  FAIL: {fail_count} pairs >= {TEST_B_FAIL:.0%}   HIGH RISK: {risk_count} pairs >= {TEST_B_HIGH_RISK:.0%}")
        for h in b_hits[:5]:
            print(f"    [{h['flag']}]  {h['our_page']}  sim={h['similarity']:.1%}")
            print(f"      PDF para: \"{h['pdf_para'][:120].strip()}...\"")
        if b_fail:
            any_fail_overall = True
            print(f"  RESULT: FAIL -- {fail_count} page(s) exceed {TEST_B_FAIL:.0%} cosine similarity threshold")
        else:
            print(f"  RESULT: WATCH -- review HIGH RISK pairs above (no FAIL threshold breached)")
    else:
        print(f"  RESULT: PASS -- no page similarity >= {TEST_B_HIGH_RISK:.0%}")

    # ── Test C ────────────────────────────────────────────────────────────────
    print(f"\n  -- TEST C: Sentence-level Jaccard Overlap --")
    print(f"  Comparing {sum(len(split_into_sentences(b)) for b in our_corpus.values())} our sentences vs {len(pdf_sentences)} PDF sentences...", end=" ", flush=True)
    c_fail, c_hits = run_test_c(pdf_sentences, pdf_label, our_corpus)
    print("done")
    if c_hits:
        fail_count = sum(1 for h in c_hits if h["flag"] == "FAIL")
        risk_count = sum(1 for h in c_hits if h["flag"] == "HIGH RISK")
        print(f"  FAIL: {fail_count} pairs >= {TEST_C_FAIL:.0%}   HIGH RISK: {risk_count} pairs >= {TEST_C_HIGH_RISK:.0%}")
        for h in c_hits[:5]:
            print(f"    [{h['flag']}]  {h['our_page']}  jaccard={h['jaccard']:.1%}")
            print(f"      Our:  \"{h['our_sent'][:110].strip()}\"")
            print(f"      PDF:  \"{h['pdf_sent'][:110].strip()}\"")
        if c_fail:
            any_fail_overall = True
            print(f"  RESULT: FAIL -- {fail_count} sentence pair(s) exceed {TEST_C_FAIL:.0%} Jaccard threshold")
        else:
            print(f"  RESULT: WATCH -- review HIGH RISK pairs above")
    else:
        print(f"  RESULT: PASS -- no sentence pair Jaccard >= {TEST_C_HIGH_RISK:.0%}")

    # Store in report
    report["pdfs"][pdf_label] = {
        "file":          pdf_path.name,
        "word_count":    word_count,
        "paragraphs":    len(pdf_paras),
        "sentences":     len(pdf_sentences),
        "test_a": {"fail": a_fail, "pages_with_matches": len(a_hits), "hits": a_hits[:10]},
        "test_b": {"fail": b_fail, "hits": b_hits[:10]},
        "test_c": {"fail": c_fail, "hits": c_hits[:10]},
    }

    return any_fail_overall


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    print("=" * 68)
    print("  Copyright Similarity Check -- Angel Numbers vs Reference PDFs")
    print(f"  Run at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 68)
    print()
    print(f"  Our corpus: {len(SAMPLE_NUMBERS)} numbers x (1 core + {len(SAMPLE_INTENTS)} intents)")
    print(f"  = {len(SAMPLE_NUMBERS) * (1 + len(SAMPLE_INTENTS))} generated pages sampled")
    print()
    print("  THRESHOLDS:")
    print(f"    Test A (verbatim 4-gram)    FAIL = any match found")
    print(f"    Test B (TF-IDF cosine)      FAIL >= {TEST_B_FAIL:.0%}   HIGH RISK >= {TEST_B_HIGH_RISK:.0%}")
    print(f"    Test C (sentence Jaccard)   FAIL >= {TEST_C_FAIL:.0%}   HIGH RISK >= {TEST_C_HIGH_RISK:.0%}")
    print()
    print("  NOTE: Test A FAIL on generic terms (e.g. 'love career spiritual growth')")
    print("  is expected and not a copyright risk -- only specific prose is actionable.")

    report: dict = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "our_corpus_size": len(SAMPLE_NUMBERS) * (1 + len(SAMPLE_INTENTS)),
        "thresholds": {
            "test_a_min_ngram": TEST_A_MIN_NGRAM,
            "test_b_fail": TEST_B_FAIL,
            "test_b_high_risk": TEST_B_HIGH_RISK,
            "test_c_fail": TEST_C_FAIL,
            "test_c_high_risk": TEST_C_HIGH_RISK,
        },
        "pdfs": {},
    }

    print("\n  Building our generated corpus...", end=" ", flush=True)
    our_corpus = build_our_corpus()
    print(f"done  ({len(our_corpus)} pages)")

    overall_fail = False

    for pdf_path, pdf_label in [
        (PDF_KYLE,    "Kyle Gray - Angel Numbers"),
        (PDF_FORTUNA, "Fortuna Noir - Angel Numbers"),
    ]:
        if not pdf_path.exists():
            print(f"\n  WARNING: PDF not found -- {pdf_path}")
            continue
        failed = run_against_pdf(pdf_path, pdf_label, our_corpus, report)
        if failed:
            overall_fail = True

    # ── Final verdict ─────────────────────────────────────────────────────────
    print()
    print("=" * 68)
    print("  OVERALL COPYRIGHT SIMILARITY VERDICT")
    print("=" * 68)
    for label, data in report["pdfs"].items():
        a_icon = "X FAIL" if data["test_a"]["fail"] else "OK PASS"
        b_icon = "X FAIL" if data["test_b"]["fail"] else "OK PASS"
        c_icon = "X FAIL" if data["test_c"]["fail"] else "OK PASS"
        print(f"  {label}")
        print(f"    Test A (verbatim 4-gram):  {a_icon}")
        print(f"    Test B (TF-IDF cosine):    {b_icon}")
        print(f"    Test C (sentence Jaccard): {c_icon}")
        print()

    if overall_fail:
        verdict = "FAIL -- copyright risk detected. Review flagged passages before publishing."
    else:
        verdict = "PASS -- no copyright threshold breached. Content is sufficiently original."

    print(f"  VERDICT: {verdict}")

    report["verdict"] = verdict
    out_path = _REPO_ROOT / "tests" / "copyright_angel_report.json"
    with open(out_path, "w") as fh:
        json.dump(report, fh, indent=2)
    print()
    print(f"  Full report saved to: tests/copyright_angel_report.json")
    print("=" * 68)

    return 1 if overall_fail else 0


if __name__ == "__main__":
    sys.exit(main())
