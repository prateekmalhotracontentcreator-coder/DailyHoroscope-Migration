#!/usr/bin/env python3
"""
ECHO/PACE Layer G -- Tarot SEO Detailed Serper Validation Report
=================================================================

Runs 5 Google exact-match queries per page type (Spreads, Cards, Intentions)
and prints FULL organic results for each query so Temple Team can verify
findings directly against what Google returned.

Samples are suit-diverse and category-diverse (not sequential slugs).

Output per query:
  - Page type + sample identifier
  - Exact query string sent to Google via Serper
  - All organic hits returned (title + URL + snippet)
  - Hit count and duplication verdict

USAGE
-----
    cd /Users/apple/DailyHoroscope-Migration
    Serper_Default_key=YOUR_KEY python3 tests/echo_pace_tarot_serper_detail.py

    # Save to custom path:
    Serper_Default_key=YOUR_KEY python3 tests/echo_pace_tarot_serper_detail.py \\
        --output tests/tarot_serper_detail_report.json

Credits used: ~15 Serper credits (5 samples x 3 page types).
Thresholds (STRICT): BLOCKED > 25% | WATCH > 10%  (standard module is 40%/20%)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone

# ── Path setup ────────────────────────────────────────────────────────────────
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BACKEND   = os.path.join(_REPO_ROOT, "backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

try:
    from tarot_seo_data import (
        SPREADS,
        INTENTIONS,
        MAJOR_MEANINGS,
        _build_cards,
    )
except ImportError as exc:
    sys.exit(f"ERROR: Cannot import tarot_seo_data -- {exc}\nRun from repo root.")

# Build cards lookup
_ALL_CARDS = {c["slug"]: c for c in _build_cards()}

# ── Strict thresholds ─────────────────────────────────────────────────────────
LG_BLOCKED = 0.25   # STRICT: standard module is 0.40
LG_WATCH   = 0.10   # STRICT: standard module is 0.20

# ── Stop words (must match main scanner) ─────────────────────────────────────
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
    # tarot-specific boilerplate to strip
    "tarot","card","cards","spread","reading","upright","reversed","suit",
    "wands","cups","swords","pentacles","major","minor","arcana",
}


# ── Content extractors (identical to main scanner) ───────────────────────────

def _spread_body(s: dict) -> str:
    return " ".join(filter(None, [
        s.get("purpose", ""),
        s.get("when", ""),
        s.get("use", ""),
        s.get("overview", ""),
        s.get("guidance", ""),
    ]))


def _card_body(slug: str, card: dict) -> str:
    parts = []
    if slug in MAJOR_MEANINGS:
        mm = MAJOR_MEANINGS[slug]
        parts += [mm.get("upright",""), mm.get("reversed",""), mm.get("imagery","")]
    for f in ("upright","reversed","imagery","description","guidance","interpretation"):
        v = card.get(f, "")
        if v and v not in parts:
            parts.append(v)
    return " ".join(filter(None, parts))


def _intention_body(slug: str, v: dict) -> str:
    parts = [v.get("chapter", ""), v.get("label", "")]
    for f in ("description","intro","guidance","overview"):
        val = v.get(f, "")
        if val:
            parts.append(val)
    for card_slug in v.get("best_cards", [])[:3]:
        if card_slug in MAJOR_MEANINGS:
            parts.append(MAJOR_MEANINGS[card_slug].get("upright",""))
    return " ".join(filter(None, parts))


# ── Phrase sampler ────────────────────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-z]{3,}\b", text.lower())


def _sample_phrase(body: str, offset: int = 5) -> str | None:
    """Extract an 8-token phrase from body text, skipping stop words."""
    tokens = [t for t in _tokenize(body) if t not in _STOPS]
    if len(tokens) < offset + 8:
        # Fall back to shorter offset if body is short
        if len(tokens) < 8:
            return None
        offset = 0
    return " ".join(tokens[offset : offset + 8])


# ── Sample selection (5 per type, suit/category diverse) ─────────────────────

def _spread_samples() -> list[tuple[str, dict]]:
    """5 spreads across diverse categories."""
    by_slug = {s["slug"]: s for s in SPREADS}
    target_slugs = [
        "past-life-love-and-soul-connection",      # love / soul connection
        "launching-freelance-and-solopreneur-gigs",  # career / money
        "settlement-vs-going-to-trial-analysis",  # legal / decision
        "new-moon-rituals-for-fresh-beginnings",  # ritual / spiritual
        "12-month-wheel-of-year-forecast",        # time / annual
    ]
    return [(slug, by_slug[slug]) for slug in target_slugs if slug in by_slug]


def _card_samples() -> list[tuple[str, dict]]:
    """5 cards across suits + Major Arcana."""
    target_slugs = [
        "the-moon",          # Major Arcana
        "queen-of-wands",    # Wands (Court)
        "six-of-cups",       # Cups (pip)
        "knight-of-swords",  # Swords (Court)
        "nine-of-pentacles", # Pentacles (pip)
    ]
    return [(slug, _ALL_CARDS[slug]) for slug in target_slugs if slug in _ALL_CARDS]


def _intention_samples() -> list[tuple[str, dict]]:
    """5 intentions across diverse categories."""
    target_slugs = [
        "love",
        "career",
        "health",
        "spiritual-growth",
        "anxiety",
    ]
    return [(slug, INTENTIONS[slug]) for slug in target_slugs if slug in INTENTIONS]


# ── Serper query ──────────────────────────────────────────────────────────────

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


# ── Printer ───────────────────────────────────────────────────────────────────

def print_query_block(
    page_type: str,
    sample_id: str,
    phrase: str,
    data: dict,
    report_records: list,
) -> str:
    """Print full organic results for one query. Returns verdict string."""
    organic  = (data or {}).get("organic") or []
    hits     = len(organic)
    dup_rate = min(hits / 10, 1.0)

    if dup_rate > LG_BLOCKED:
        verdict = "BLOCKED"
        icon    = "❌"
    elif dup_rate > LG_WATCH:
        verdict = "WATCH"
        icon    = "⚠️ "
    else:
        verdict = "PASS"
        icon    = "✅"

    print(f"\n{'─'*68}")
    print(f"  {page_type}  ·  {sample_id}")
    print(f"{'─'*68}")
    print(f"  Exact query sent to Google via Serper:")
    print(f'  "{phrase}"')
    print()
    print(f"  Organic hits: {hits} / 10  →  {icon} {verdict}")
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
        print("  No organic results -- Google found 0 pages matching this exact phrase.")
        print()

    kg = data.get("knowledgeGraph")
    if kg:
        print(f"  Knowledge Graph: {kg.get('title','')} -- {kg.get('description','')[:120]}")
        print()

    report_records.append({
        "page_type":       page_type,
        "sample_id":       sample_id,
        "phrase":          phrase,
        "hits":            hits,
        "dup_rate":        round(dup_rate, 3),
        "verdict":         verdict,
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

    return verdict


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="ECHO/PACE Layer G -- Tarot SEO Detailed Serper Validation"
    )
    parser.add_argument(
        "--output",
        default="tests/tarot_serper_detail_report.json",
        help="Path for the detailed JSON report",
    )
    args = parser.parse_args()

    serper_key = (
        os.getenv("Serper_Default_key") or os.getenv("SERPER_API_KEY") or ""
    ).strip()
    if not serper_key:
        sys.exit(
            "ERROR: Serper key not set.\n"
            "Run as: Serper_Default_key=YOUR_KEY python3 tests/echo_pace_tarot_serper_detail.py"
        )

    print("=" * 68)
    print("  ECHO/PACE Layer G -- Tarot SEO Detailed Serper Validation")
    print(f"  Run at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("  Queries: 15 total  (~15 Serper credits)")
    print("  Sampling: 5 spreads x 5 cards x 5 intentions (suit/category diverse)")
    print("=" * 68)
    print()
    print("  Full organic results are shown for each query.")
    print("  Duplication thresholds (STRICT -- 199-page high-volume module):")
    print(f"    ✅  PASS    0-{LG_WATCH:.0%}  hits matched")
    print(f"    ⚠️   WATCH  {LG_WATCH:.0%}-{LG_BLOCKED:.0%}  hits matched")
    print(f"    ❌  BLOCKED > {LG_BLOCKED:.0%}  hits matched")
    print()
    print("  A PASS means Google returned 0 pages containing this exact phrase --")
    print("  the content is original and not duplicated anywhere on the indexed web.")
    print()

    report_records: list[dict] = []
    all_verdicts:   list[str]  = []
    errors:         list[str]  = []

    # ── Build query specs ─────────────────────────────────────────────────────

    query_specs: list[tuple[str, str, str]] = []  # (page_type, sample_id, body)

    for slug, s in _spread_samples():
        query_specs.append(("Spread", slug, _spread_body(s)))

    for slug, card in _card_samples():
        query_specs.append(("Card", slug, _card_body(slug, card)))

    for slug, v in _intention_samples():
        query_specs.append(("Intention", slug, _intention_body(slug, v)))

    # ── Run queries ───────────────────────────────────────────────────────────

    for page_type, sample_id, body in query_specs:
        phrase = _sample_phrase(body)
        if not phrase:
            msg = f"  ⚠️   {page_type} · {sample_id} -- body too short to sample"
            print(msg)
            errors.append(msg)
            continue

        try:
            data = serper_search(phrase, serper_key)
        except Exception as exc:
            msg = f"  ❌  Serper error ({page_type} · {sample_id}): {exc}"
            print(msg)
            errors.append(msg)
            continue

        verdict = print_query_block(page_type, sample_id, phrase, data, report_records)
        all_verdicts.append(verdict)

    # ── Summary ───────────────────────────────────────────────────────────────

    print("=" * 68)
    print("  LAYER G SUMMARY")
    print("=" * 68)
    print()

    for page_type in ["Spread", "Card", "Intention"]:
        recs = [r for r in report_records if r["page_type"] == page_type]
        if not recs:
            continue
        print(f"  {page_type.upper()}S")
        for rec in recs:
            icon = "✅" if rec["dup_rate"] <= LG_WATCH else (
                   "⚠️ " if rec["dup_rate"] <= LG_BLOCKED else "❌")
            print(
                f"    {icon}  {rec['sample_id']:<45s}  "
                f"hits={rec['hits']}/10  dup={rec['dup_rate']:.0%}  →  {rec['verdict']}"
            )
        print()

    if errors:
        print("  Errors:")
        for e in errors:
            print(f"    {e}")
        print()

    if "BLOCKED" in all_verdicts:
        overall = "❌  BLOCKED -- rewrite flagged content before indexing proceeds"
    elif "WATCH" in all_verdicts:
        overall = "⚠️   WATCH -- review flagged queries; consider humanising before indexing"
    else:
        overall = "✅  PASS -- all Layer G queries clear; Tarot SEO module is QA-cleared"

    print(f"  OVERALL: {overall}")
    print()

    # ── Save JSON report ──────────────────────────────────────────────────────

    full_report = {
        "run_at":      datetime.now(timezone.utc).isoformat(),
        "module":      "Tarot SEO (TAR-SEO-1 + TAR-SEO-2)",
        "layer":       "G",
        "description": "Detailed Serper validation for ECHO/PACE Layer G -- 15 queries across 3 page types",
        "thresholds":  {"pass_max": LG_WATCH, "watch_max": LG_BLOCKED, "blocked_above": LG_BLOCKED},
        "overall":     overall,
        "queries":     report_records,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w") as fh:
        json.dump(full_report, fh, indent=2)

    print(f"  Full report (with all URLs + snippets) saved to: {args.output}")
    print("=" * 68)

    return 1 if "BLOCKED" in all_verdicts else 0


if __name__ == "__main__":
    sys.exit(main())
