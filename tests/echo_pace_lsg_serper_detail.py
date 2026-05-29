#!/usr/bin/env python3
"""
ECHO/PACE Layer G -- Detailed Serper Validation Report
=======================================================

Runs the same 4 Google queries used by echo_pace_lsg_scan.py Layer G,
but prints FULL organic results for each query so Temple Team can verify
findings directly against what Google returned.

Output per query:
  - Exact query string sent to Serper
  - All organic hits returned (title + URL + snippet)
  - Hit count and duplication verdict

USAGE
-----
    cd /path/to/DailyHoroscope-Migration
    Serper_Default_key=YOUR_KEY python3 tests/echo_pace_lsg_serper_detail.py

    # Save to file for sharing:
    Serper_Default_key=YOUR_KEY python3 tests/echo_pace_lsg_serper_detail.py \
        --output tests/lsg_serper_detail_report.json

Credits used: ~4 Serper credits (same as the main scanner).
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
    from lo_shu_router import (
        NUMBER_CLASSICAL_ASSOCIATIONS,
        NUMBER_DEEP_DIVE_BLUEPRINTS,
        NUMBER_REFERENCE,
    )
except ImportError as exc:
    sys.exit(f"ERROR: Cannot import lo_shu_router -- {exc}\nRun from repo root.")

# ── Thresholds (must match main scanner) ─────────────────────────────────────
LG_BLOCKED = 0.40
LG_WATCH   = 0.20

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
    "use","used","using","make","made","single","often","usually","repeat",
    "when","repeats","number","numbers","lo","shu","grid","become","becomes",
}


# ── Content builders (identical to main scanner) ─────────────────────────────

def _tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-z]{3,}\b", text.lower())


def _sample_phrase(body: str) -> str | None:
    tokens = [t for t in _tokenize(body) if t not in _STOPS]
    if len(tokens) < 10:
        return None
    return " ".join(tokens[5:13])


def _number_page_body(n: int) -> str:
    parts = []
    bp = NUMBER_DEEP_DIVE_BLUEPRINTS.get(n, {})
    ca = NUMBER_CLASSICAL_ASSOCIATIONS.get(n, {})
    nr = NUMBER_REFERENCE.get(n, {})
    for f in ("intro", "present_once", "repeat_guidance"):
        v = bp.get(f, "")
        if v:
            parts.append(v)
    for tip in bp.get("balancing_tips", []):
        parts.append(tip)
    life_theme = ca.get("life_theme", "")
    if life_theme:
        parts.append(life_theme)
    body_area = ca.get("body_area", "")
    if body_area:
        parts.append(f"body area {body_area}")
    parts.append(nr.get("planet", ""))
    parts.append(nr.get("archetype", ""))
    return " ".join(filter(None, parts))


def _classical_body(n: int) -> str:
    ca = NUMBER_CLASSICAL_ASSOCIATIONS.get(n, {})
    nr = NUMBER_REFERENCE.get(n, {})
    parts = [
        ca.get("life_theme", ""),
        ca.get("element", ""),
        ca.get("direction", ""),
        ca.get("body_area", ""),
        ca.get("family_role", ""),
        " ".join(ca.get("colours", [])),
        nr.get("planet", ""),
        nr.get("archetype", ""),
        nr.get("day", ""),
    ]
    return " ".join(filter(None, parts))


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
    query_label: str,
    number: int,
    phrase: str,
    data: dict,
    report_records: list,
) -> None:
    organic = (data or {}).get("organic") or []
    hits    = len(organic)
    dup_rate = min(hits / 10, 1.0)

    if dup_rate > LG_BLOCKED:
        verdict_icon = "❌  BLOCKED"
    elif dup_rate > LG_WATCH:
        verdict_icon = "⚠️   WATCH"
    else:
        verdict_icon = "✅  PASS"

    print(f"\n{'─'*68}")
    print(f"  {query_label}  ·  Number {number}")
    print(f"{'─'*68}")
    print(f"  Exact query sent to Google via Serper:")
    print(f"  \"{phrase}\"")
    print()
    print(f"  Organic hits returned: {hits} / 10  →  {verdict_icon}")
    print()

    if organic:
        print(f"  Results:")
        for idx, result in enumerate(organic, 1):
            title   = result.get("title",   "(no title)")
            link    = result.get("link",    "(no URL)")
            snippet = result.get("snippet", "(no snippet)")
            print(f"  [{idx:02d}]  {title}")
            print(f"        URL:     {link}")
            print(f"        Snippet: {snippet[:160].strip()}")
            print()
    else:
        print("  No organic results returned -- Google found 0 pages matching this phrase.")
        print()

    # Knowledge graph note if present
    kg = data.get("knowledgeGraph")
    if kg:
        print(f"  Knowledge Graph: {kg.get('title', '')} -- {kg.get('description', '')[:120]}")
        print()

    report_records.append({
        "query_label": query_label,
        "number": number,
        "phrase": phrase,
        "hits": hits,
        "dup_rate": round(dup_rate, 3),
        "verdict": verdict_icon.strip(),
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


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="ECHO/PACE Layer G -- Detailed Serper Validation"
    )
    parser.add_argument(
        "--output",
        default="tests/lsg_serper_detail_report.json",
        help="Path for the detailed JSON report",
    )
    args = parser.parse_args()

    serper_key = (
        os.getenv("Serper_Default_key") or os.getenv("SERPER_API_KEY") or ""
    ).strip()
    if not serper_key:
        sys.exit(
            "ERROR: Serper key not set.\n"
            "Run as: Serper_Default_key=YOUR_KEY python3 tests/echo_pace_lsg_serper_detail.py"
        )

    print("=" * 68)
    print("  ECHO/PACE Layer G -- Detailed Serper Validation")
    print(f"  Run at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("  Queries: 4 total  (~4 Serper credits)")
    print("=" * 68)
    print()
    print("  This report shows the FULL Google organic results for each query")
    print("  sampled in Layer G of the main ECHO/PACE scanner.")
    print()
    print("  Duplication thresholds (same as main scanner):")
    print(f"    ✅  PASS    ≤ {LG_WATCH:.0%} of returned results match our content")
    print(f"    ⚠️   WATCH  {LG_WATCH:.0%}-{LG_BLOCKED:.0%}")
    print(f"    ❌  BLOCKED > {LG_BLOCKED:.0%}")
    print()
    print("  A PASS means Google returned 0 pages containing this phrase --")
    print("  the content is not duplicated anywhere on the indexed web.")

    report_records: list[dict] = []
    all_statuses: list[str] = []
    errors: list[str] = []

    # ── The 4 queries (identical sampling logic to main scanner, sample=2) ──
    query_specs = [
        ("Blueprint Prose",      1, _number_page_body(1)),
        ("Blueprint Prose",      2, _number_page_body(2)),
        ("Classical WATCH-1",    1, _classical_body(1)),
        ("Classical WATCH-1",    2, _classical_body(2)),
    ]

    for label, number, body in query_specs:
        phrase = _sample_phrase(body)
        if not phrase:
            msg = f"  ⚠️   {label} · Number {number} -- body too short to sample"
            print(msg)
            errors.append(msg)
            continue
        try:
            data = serper_search(phrase, serper_key)
        except Exception as exc:
            msg = f"  ❌  Serper error ({label} · Number {number}): {exc}"
            print(msg)
            errors.append(msg)
            continue
        print_query_block(label, number, phrase, data, report_records)
        dup_rate = report_records[-1]["dup_rate"]
        if dup_rate > LG_BLOCKED:
            all_statuses.append("BLOCKED")
        elif dup_rate > LG_WATCH:
            all_statuses.append("WATCH")
        else:
            all_statuses.append("PASS")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 68)
    print("  LAYER G SUMMARY")
    print("=" * 68)
    for rec in report_records:
        icon = "✅" if rec["dup_rate"] <= LG_WATCH else ("⚠️" if rec["dup_rate"] <= LG_BLOCKED else "❌")
        print(
            f"  {icon}  {rec['query_label']:20s}  Number {rec['number']}  "
            f"hits={rec['hits']}/10  dup={rec['dup_rate']:.0%}  →  {rec['verdict']}"
        )

    print()
    if "BLOCKED" in all_statuses:
        overall = "❌  BLOCKED -- humanise flagged fields before integration"
    elif "WATCH" in all_statuses:
        overall = "⚠️   WATCH -- review flagged queries; consider humanising before integration"
    else:
        overall = "✅  PASS -- all Layer G queries clear; LSG-1 safe to integrate"
    print(f"  OVERALL: {overall}")

    if errors:
        print()
        print("  Errors encountered:")
        for e in errors:
            print(f"  {e}")

    # ── Save JSON report ──────────────────────────────────────────────────────
    full_report = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "layer": "G",
        "description": "Detailed Serper validation for ECHO/PACE Layer G",
        "thresholds": {"pass": LG_WATCH, "watch": LG_WATCH, "blocked": LG_BLOCKED},
        "overall": overall,
        "queries": report_records,
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as fh:
        json.dump(full_report, fh, indent=2)
    print()
    print(f"  Full report (with all URLs + snippets) saved to: {args.output}")
    print("=" * 68)

    return 1 if "BLOCKED" in all_statuses else 0


if __name__ == "__main__":
    sys.exit(main())
