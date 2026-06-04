#!/usr/bin/env python3
"""
ECHO/PACE Layer G -- Angel Numbers Detailed Serper Validation Report
=====================================================================

Runs 10 Google exact-match queries across Angel Numbers core pages and
intent pages, then prints FULL organic results for each query so Temple
Team can verify findings against what Google actually returned.

Samples are number-diverse and intent-diverse (not sequential slugs).

Output per query:
  - Page type + sample identifier
  - Exact query string sent to Google via Serper
  - All organic hits returned (title + URL + snippet)
  - Hit count and duplication verdict

USAGE
-----
    cd /Users/apple/DailyHoroscope-Migration
    Serper_Default_key=YOUR_KEY python3 tests/echo_pace_angel_serper_detail.py

    # Save to custom path:
    Serper_Default_key=YOUR_KEY python3 tests/echo_pace_angel_serper_detail.py \\
        --output tests/angel_serper_detail_report.json

Credits used: ~10 Serper credits (4 core samples + 6 intent samples).
Thresholds (match Angel Numbers brief): BLOCKED > 40% | WATCH > 20%
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone

# -- Path setup ────────────────────────────────────────────────────────────────
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BACKEND   = os.path.join(_REPO_ROOT, "backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

try:
    from angel_numbers_data import (
        build_seeing_it_means,
        build_vibration,
        build_intent_message,
        reduce_to_root,
    )
except ImportError as exc:
    sys.exit(
        f"ERROR: Cannot import angel_numbers_data -- {exc}\n"
        "Run from repo root with: Serper_Default_key=YOUR_KEY python3 tests/echo_pace_angel_serper_detail.py"
    )

# -- Thresholds (match Angel Numbers brief gate) ───────────────────────────────
LG_BLOCKED = 0.40
LG_WATCH   = 0.20

# -- Stop words (content words only -- filter out generic angel-number terms) ──
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
    "while", "as", "also", "then", "there", "here", "them", "any", "one",
    "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "across", "without", "within", "upon", "over", "under", "toward",
    "use", "used", "using", "make", "made", "become", "becomes", "often",
    "usually", "repeat", "repeats", "number", "numbers", "angel", "angels",
    "seeing", "seen", "see", "mean", "means", "meaning", "signal", "signals",
    "notice", "noticing", "appear", "appears", "appearing",
}

# -- Query samples ─────────────────────────────────────────────────────────────
# 4 core pages: diverse repeating patterns across digit values
CORE_SAMPLES = ["111", "333", "555", "888"]

# 6 intent pages: diverse numbers AND diverse intents
INTENT_SAMPLES = [
    ("111", "love"),
    ("222", "twin-flame"),
    ("333", "spiritual-growth"),
    ("444", "protection"),
    ("555", "career"),
    ("777", "manifestation"),
]


# -- Content builders ──────────────────────────────────────────────────────────

def _core_body(number: str) -> str:
    """Concatenate the two main prose fields used in L1 compliance for core pages."""
    root = reduce_to_root(number)
    return build_seeing_it_means(number, root) + " " + build_vibration(number, root)


def _intent_body(number: str, intent: str) -> str:
    """Return the intent message field used in L1 compliance for intent pages."""
    root = reduce_to_root(number)
    return build_intent_message(number, intent, root)


# -- Phrase extractor ──────────────────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-z]{3,}\b", text.lower())


def _sample_phrase(body: str) -> str | None:
    """Extract an 8-token content-rich phrase from the middle of the body."""
    tokens = [t for t in _tokenize(body) if t not in _STOPS]
    if len(tokens) < 10:
        return None
    return " ".join(tokens[5:13])


# -- Serper query ──────────────────────────────────────────────────────────────

def serper_search(phrase: str, serper_key: str) -> dict:
    """Send an exact-match phrase query to Serper and return the raw response."""
    payload = json.dumps({"q": f'"{phrase}"', "num": 10}).encode()
    req = urllib.request.Request(
        "https://google.serper.dev/search",
        data=payload,
        headers={
            "X-API-KEY": serper_key,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


# -- Result printer ────────────────────────────────────────────────────────────

def print_query_block(
    query_label: str,
    identifier: str,
    phrase: str,
    data: dict,
    report_records: list,
) -> None:
    organic  = (data or {}).get("organic") or []
    hits     = len(organic)
    dup_rate = min(hits / 10, 1.0)

    if dup_rate > LG_BLOCKED:
        verdict_icon = "BLOCKED"
    elif dup_rate > LG_WATCH:
        verdict_icon = "WATCH"
    else:
        verdict_icon = "PASS"

    verdict_display = (
        f"X  BLOCKED" if verdict_icon == "BLOCKED"
        else f"!   WATCH" if verdict_icon == "WATCH"
        else f"OK  PASS"
    )

    print(f"\n{'─'*68}")
    print(f"  {query_label}  --  {identifier}")
    print(f"{'─'*68}")
    print(f"  Exact query sent to Google via Serper:")
    print(f"  \"{phrase}\"")
    print()
    print(f"  Organic hits returned: {hits} / 10  -->  {verdict_display}")
    print()

    if organic:
        print("  Results:")
        for idx, result in enumerate(organic, 1):
            title   = result.get("title",   "(no title)")
            link    = result.get("link",    "(no URL)")
            snippet = result.get("snippet", "(no snippet)")
            print(f"  [{idx:02d}]  {title}")
            print(f"        URL:     {link}")
            print(f"        Snippet: {snippet[:160].strip()}")
            print()
    else:
        print(
            "  No organic results -- Google found 0 pages matching this phrase.\n"
            "  This is the ideal outcome: content is not duplicated anywhere indexed.\n"
        )

    kg = data.get("knowledgeGraph")
    if kg:
        print(
            f"  Knowledge Graph: {kg.get('title', '')} -- "
            f"{kg.get('description', '')[:120]}"
        )
        print()

    report_records.append({
        "query_label":    query_label,
        "identifier":     identifier,
        "phrase":         phrase,
        "hits":           hits,
        "dup_rate":       round(dup_rate, 3),
        "verdict":        verdict_icon,
        "organic_results": [
            {
                "position": r.get("position"),
                "title":    r.get("title"),
                "link":     r.get("link"),
                "snippet":  r.get("snippet"),
            }
            for r in organic
        ],
    })


# -- Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="ECHO/PACE Layer G -- Angel Numbers Detailed Serper Validation"
    )
    parser.add_argument(
        "--output",
        default="tests/angel_serper_detail_report.json",
        help="Path for the detailed JSON report",
    )
    args = parser.parse_args()

    serper_key = (
        os.getenv("Serper_Default_key") or os.getenv("SERPER_API_KEY") or ""
    ).strip()
    if not serper_key:
        sys.exit(
            "ERROR: Serper key not set.\n"
            "Run as: Serper_Default_key=YOUR_KEY python3 tests/echo_pace_angel_serper_detail.py"
        )

    total_queries = len(CORE_SAMPLES) + len(INTENT_SAMPLES)

    print("=" * 68)
    print("  ECHO/PACE Layer G -- Angel Numbers Detailed Serper Validation")
    print(f"  Run at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Queries: {total_queries} total  (~{total_queries} Serper credits)")
    print("=" * 68)
    print()
    print(f"  Samples: {len(CORE_SAMPLES)} core page(s) + {len(INTENT_SAMPLES)} intent page(s)")
    print()
    print("  Duplication thresholds (match Angel Numbers brief gate):")
    print(f"    OK  PASS    0-{LG_WATCH:.0%} of returned results match our content")
    print(f"    !   WATCH   {LG_WATCH:.0%}-{LG_BLOCKED:.0%}")
    print(f"    X   BLOCKED > {LG_BLOCKED:.0%}")
    print()
    print("  A PASS means Google returned 0 pages containing this phrase --")
    print("  the content is not indexed anywhere else on the open web.")
    print()

    report_records: list[dict] = []
    all_verdicts:   list[str]  = []
    errors:         list[str]  = []

    # ── Core pages ────────────────────────────────────────────────────────────
    print(f"  >>> CORE PAGES ({len(CORE_SAMPLES)} samples)")

    for number in CORE_SAMPLES:
        try:
            body = _core_body(number)
        except Exception as exc:
            msg = f"  !  Core {number} -- body build failed: {exc}"
            print(msg)
            errors.append(msg)
            continue

        phrase = _sample_phrase(body)
        if not phrase:
            msg = f"  !  Core {number} -- body too short to sample"
            print(msg)
            errors.append(msg)
            continue

        try:
            data = serper_search(phrase, serper_key)
        except Exception as exc:
            msg = f"  X  Serper error (Core {number}): {exc}"
            print(msg)
            errors.append(msg)
            continue

        print_query_block(
            query_label=f"Core page",
            identifier=f"Angel Number {number}",
            phrase=phrase,
            data=data,
            report_records=report_records,
        )
        all_verdicts.append(report_records[-1]["verdict"])

    # ── Intent pages ──────────────────────────────────────────────────────────
    print(f"\n  >>> INTENT PAGES ({len(INTENT_SAMPLES)} samples)")

    for number, intent in INTENT_SAMPLES:
        try:
            body = _intent_body(number, intent)
        except Exception as exc:
            msg = f"  !  Intent {number}/{intent} -- body build failed: {exc}"
            print(msg)
            errors.append(msg)
            continue

        phrase = _sample_phrase(body)
        if not phrase:
            msg = f"  !  Intent {number}/{intent} -- body too short to sample"
            print(msg)
            errors.append(msg)
            continue

        try:
            data = serper_search(phrase, serper_key)
        except Exception as exc:
            msg = f"  X  Serper error (Intent {number}/{intent}): {exc}"
            print(msg)
            errors.append(msg)
            continue

        print_query_block(
            query_label=f"Intent page",
            identifier=f"{number} / {intent}",
            phrase=phrase,
            data=data,
            report_records=report_records,
        )
        all_verdicts.append(report_records[-1]["verdict"])

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 68)
    print("  LAYER G SUMMARY -- ANGEL NUMBERS")
    print("=" * 68)
    for rec in report_records:
        icon = (
            "X " if rec["verdict"] == "BLOCKED"
            else "! " if rec["verdict"] == "WATCH"
            else "OK"
        )
        print(
            f"  {icon}  {rec['query_label']:12s}  {rec['identifier']:30s}  "
            f"hits={rec['hits']}/10  dup={rec['dup_rate']:.0%}  -->  {rec['verdict']}"
        )

    print()
    if "BLOCKED" in all_verdicts:
        overall_str = "BLOCKED -- humanise flagged phrases before sign-off"
        overall_icon = "X "
    elif "WATCH" in all_verdicts:
        overall_str = "WATCH -- review flagged queries; consider minor rephrasing"
        overall_icon = "! "
    else:
        overall_str = "PASS -- all Layer G queries clear; Angel Numbers safe to sign off"
        overall_icon = "OK"

    overall_line = f"  {overall_icon}  OVERALL: {overall_str}"
    print(overall_line)

    pass_count    = all_verdicts.count("PASS")
    watch_count   = all_verdicts.count("WATCH")
    blocked_count = all_verdicts.count("BLOCKED")
    print()
    print(f"  Breakdown: {pass_count} PASS  |  {watch_count} WATCH  |  {blocked_count} BLOCKED  "
          f"(of {len(all_verdicts)} completed queries)")

    if errors:
        print()
        print("  Errors encountered:")
        for e in errors:
            print(f"    {e}")

    # ── Save JSON report ──────────────────────────────────────────────────────
    full_report = {
        "run_at":      datetime.now(timezone.utc).isoformat(),
        "layer":       "G",
        "module":      "Angel Numbers",
        "description": "Detailed Serper validation for ECHO/PACE Layer G -- Angel Numbers",
        "thresholds":  {"watch": LG_WATCH, "blocked": LG_BLOCKED},
        "samples": {
            "core":   CORE_SAMPLES,
            "intent": [f"{n}/{i}" for n, i in INTENT_SAMPLES],
        },
        "overall":  overall_str,
        "summary": {
            "pass":    pass_count,
            "watch":   watch_count,
            "blocked": blocked_count,
            "total":   len(all_verdicts),
        },
        "queries": report_records,
    }

    out_path = args.output
    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else ".", exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(full_report, fh, indent=2)

    print()
    print(f"  Full report saved to: {out_path}")
    print("=" * 68)

    return 1 if "BLOCKED" in all_verdicts else 0


if __name__ == "__main__":
    sys.exit(main())
