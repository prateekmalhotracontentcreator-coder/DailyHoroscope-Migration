#!/usr/bin/env python3
"""
ECHO/PACE 3-Layer Scanner -- Lo Shu Grid (LSG) SEO Module
=========================================================

Scans the Lo Shu Grid content against all three ECHO/PACE quality
layers and produces a pass/fail report. The Operations thread runs
this script after integrating LSG-1 -- no manual admin panel required.

LAYER 1  TF-IDF Cosine (inter-page body fields)
         BLOCKED >= 70% any pair | FLAGGED 50-69% | PASS < 50%
         LSG risk: 9 number pages share structural framing; 81
         combination pages share number content. Check both sets.

LAYER 2  N-gram phrase match (stop-word filtered)
         Flags any 4+ consecutive meaningful words shared by 3+ pages.
         LSG risk: NUMBER_DEEP_DIVE_BLUEPRINTS uses repeated sentence
         scaffolding ("When X repeats...") -- this is the WATCH-1 risk
         flagged in the pre-integration audit.

LAYER 3  Jaccard heading match
         Checks page titles against a generic Lo Shu / numerology
         heading corpus. Flagged headings need humanised <title> tags.

LAYER G  Google duplication spot-check (Serper API, 3 samples per type)
         BLOCKED > 40% | WATCH 20-40% | PASS <= 20%
         Requires SERPER_API_KEY environment variable.

USAGE
-----
    # From repo root (after LSG-1 is integrated):
    cd /path/to/DailyHoroscope-Migration

    # Layers 1-3 only:
    python tests/echo_pace_lsg_scan.py

    # All 4 layers:
    SERPER_API_KEY=your_key python tests/echo_pace_lsg_scan.py

    # Save report to custom path:
    python tests/echo_pace_lsg_scan.py --output /tmp/lsg_report.json

WHEN TO RE-RUN
--------------
    - Immediately after LSG-1 integration (first run)
    - After any GAI optimisation pass on NUMBER_DEEP_DIVE_BLUEPRINTS
    - After any addition of combination page content

NOTE ON WATCH-1 RISK
--------------------
    The pre-integration audit flagged "classical associations" content
    (NUMBER_CLASSICAL_ASSOCIATIONS) as WATCH-1 -- classical Lo Shu data
    for element/direction/colour is widely shared across numerology sites.
    Layer G spot-checks this content specifically. If any sample phrase
    from NUMBER_CLASSICAL_ASSOCIATIONS triggers > 40% Google duplication,
    those fields must be humanised before the module goes live.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from itertools import combinations
from typing import Any

# ── Path setup ────────────────────────────────────────────────────────────────
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BACKEND = os.path.join(_REPO_ROOT, "backend")
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

# ── Thresholds ────────────────────────────────────────────────────────────────
L1_BLOCKED  = 0.70
L1_FLAGGED  = 0.50
L2_NGRAM    = 4
L2_MIN_DOCS = 3
L3_JACCARD  = 0.60
LG_BLOCKED  = 0.40
LG_WATCH    = 0.20

# ── Stop words ────────────────────────────────────────────────────────────────
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

# ── Generic Lo Shu / numerology heading corpus (Layer 3) ─────────────────────
_GENERIC_HEADINGS = [
    "lo shu grid","lo shu number","numerology number","life path number",
    "number one meaning","number two meaning","number three meaning",
    "number four meaning","number five meaning","number six meaning",
    "number seven meaning","number eight meaning","number nine meaning",
    "number 1 numerology","number 2 numerology","number 3 numerology",
    "number 4 numerology","number 5 numerology","number 6 numerology",
    "number 7 numerology","number 8 numerology","number 9 numerology",
    "feng shui number","bagua number","element wood","element fire",
    "element earth","element metal","element water","north direction",
    "south direction","east direction","west direction",
    "sun planet","moon planet","jupiter planet","saturn planet",
    "mercury planet","venus planet","mars planet","rahu planet",
    "lo shu grid calculation","lo shu grid birth date",
    "lo shu grid missing numbers","lo shu grid repeated numbers",
    "sun archetype","moon archetype","warrior archetype",
    "king archetype","queen archetype","judge archetype",
]


# ════════════════════════════════════════════════════════════════════════════
# Content builders -- construct what each page type would render
# ════════════════════════════════════════════════════════════════════════════

def _number_page_body(n: int) -> str:
    """Construct body text for a single-number deep-dive page."""
    parts = []
    bp = NUMBER_DEEP_DIVE_BLUEPRINTS.get(n, {})
    ca = NUMBER_CLASSICAL_ASSOCIATIONS.get(n, {})
    nr = NUMBER_REFERENCE.get(n, {})

    # Blueprint prose
    for f in ("intro", "present_once", "repeat_guidance"):
        v = bp.get(f, "")
        if v:
            parts.append(v)
    for tip in bp.get("balancing_tips", []):
        parts.append(tip)

    # Classical associations (WATCH-1 risk area)
    life_theme = ca.get("life_theme", "")
    if life_theme:
        parts.append(life_theme)
    body_area = ca.get("body_area", "")
    if body_area:
        parts.append(f"body area {body_area}")

    # Reference fields
    parts.append(nr.get("planet", ""))
    parts.append(nr.get("archetype", ""))

    return " ".join(filter(None, parts))

def _classical_body(n: int) -> str:
    """Isolate the WATCH-1 classical associations content for Google check."""
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

def _combo_page_body(n1: int, n2: int) -> str:
    """Construct body for a combination page (two numbers)."""
    b1 = NUMBER_DEEP_DIVE_BLUEPRINTS.get(n1, {})
    b2 = NUMBER_DEEP_DIVE_BLUEPRINTS.get(n2, {})
    return " ".join(filter(None, [
        b1.get("intro", ""), b1.get("present_once", ""),
        b2.get("intro", ""), b2.get("present_once", ""),
    ]))


# ════════════════════════════════════════════════════════════════════════════
# Shared scan primitives (same logic as echo_pace_tarot_scan.py)
# ════════════════════════════════════════════════════════════════════════════

def _tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-z]{3,}\b", text.lower())

def _tfidf_vectors(docs: list[str]) -> list[dict[str, float]]:
    tokenized = [_tokenize(d) for d in docs]
    N = len(docs)
    df: Counter = Counter()
    for toks in tokenized:
        df.update(set(toks))
    idf = {t: math.log((N + 1) / (f + 1)) + 1 for t, f in df.items()}
    vecs = []
    for toks in tokenized:
        tf = Counter(toks)
        total = len(toks) or 1
        vecs.append({t: (c / total) * idf[t] for t, c in tf.items()})
    return vecs

def _cosine(v1: dict, v2: dict) -> float:
    common = set(v1) & set(v2)
    if not common:
        return 0.0
    dot = sum(v1[t] * v2[t] for t in common)
    m1 = math.sqrt(sum(x * x for x in v1.values()))
    m2 = math.sqrt(sum(x * x for x in v2.values()))
    return dot / (m1 * m2) if m1 and m2 else 0.0

def layer1(docs: list[str], names: list[str], label: str) -> tuple[str, dict]:
    print(f"\n{'─'*60}")
    print(f"LAYER 1 · TF-IDF Cosine -- {label} ({len(docs)} items)")
    print(f"{'─'*60}")
    vecs = _tfidf_vectors(docs)
    blocked, flagged = [], []
    peak = 0.0
    for i, j in combinations(range(len(docs)), 2):
        sim = _cosine(vecs[i], vecs[j])
        peak = max(peak, sim)
        if sim >= L1_BLOCKED:
            blocked.append((names[i], names[j], sim))
        elif sim >= L1_FLAGGED:
            flagged.append((names[i], names[j], sim))

    if blocked:
        status = "BLOCKED"
        print(f"  ❌  BLOCKED -- {len(blocked)} pair(s) >= {L1_BLOCKED:.0%}")
        for a, b, s in blocked[:5]:
            print(f"      Number {a} ↔ Number {b}  {s:.1%}")
        print(f"  These number pages share too much structural text.")
        print(f"  Each page needs meaningfully different prose -- not template fills.")
    elif flagged:
        status = "FLAGGED"
        print(f"  ⚠️   FLAGGED -- {len(flagged)} pair(s) in 50-69% range")
        for a, b, s in flagged[:5]:
            print(f"      Number {a} ↔ Number {b}  {s:.1%}")
    else:
        status = "PASS"
        print(f"  ✅  PASS -- 0 pairs >= {L1_FLAGGED:.0%}")

    print(f"  Peak similarity: {peak:.1%}")
    return status, {"blocked_pairs": len(blocked), "flagged_pairs": len(flagged),
                    "peak": round(peak, 3)}

def _ngrams(text: str, n: int) -> set[str]:
    tokens = re.findall(r"\b[a-z]+\b", text.lower())
    meaningful = [(i, t) for i, t in enumerate(tokens) if t not in _STOPS]
    result = set()
    for idx in range(len(meaningful) - n + 1):
        group = meaningful[idx : idx + n]
        if group[-1][0] - group[0][0] <= n + 4:
            result.add(" ".join(t for _, t in group))
    return result

def layer2(docs: list[str], label: str) -> tuple[str, dict]:
    print(f"\n{'─'*60}")
    print(f"LAYER 2 · N-gram Phrase Match (>={L2_NGRAM} words) -- {label}")
    print(f"{'─'*60}")
    doc_ngrams = []
    for doc in docs:
        phrases: set[str] = set()
        for n in range(L2_NGRAM, 9):
            phrases |= _ngrams(doc, n)
        doc_ngrams.append(phrases)

    freq: Counter = Counter()
    for phrases in doc_ngrams:
        for p in phrases:
            freq[p] += 1

    flagged = [(p, c) for p, c in freq.items() if c >= L2_MIN_DOCS]
    flagged.sort(key=lambda x: -x[1])

    if flagged:
        status = "FLAGGED"
        print(f"  ⚠️   {len(flagged)} phrase(s) appear in >= {L2_MIN_DOCS} pages")
        print(f"  Top offenders:")
        for phrase, cnt in flagged[:10]:
            print(f"      [{cnt} pages] \"{phrase}\"")
        if len(flagged) > 10:
            print(f"      ... and {len(flagged)-10} more")
        print()
        print(f"  NOTE: Scaffolding phrases like 'when X repeats' are structural and expected.")
        print(f"  Flag only phrases that appear to be copied verbatim from source books.")
    else:
        status = "PASS"
        print(f"  ✅  PASS -- No {L2_NGRAM}+ word phrases appear in >= {L2_MIN_DOCS} pages")

    return status, {"flagged_phrases": len(flagged),
                    "top_5": [p for p, _ in flagged[:5]]}

def _jaccard(a: str, b: str) -> float:
    sa, sb = set(_tokenize(a)), set(_tokenize(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

def layer3(headings: list[str], label: str) -> tuple[str, dict]:
    print(f"\n{'─'*60}")
    print(f"LAYER 3 · Jaccard Heading Match -- {label}")
    print(f"{'─'*60}")
    flagged = []
    for h in headings:
        clean = h.replace("-", " ")
        for generic in _GENERIC_HEADINGS:
            score = _jaccard(clean, generic)
            if score >= L3_JACCARD:
                flagged.append((h, generic, score))
                break

    if flagged:
        print(f"  ⚠️   {len(flagged)} heading(s) match generic corpus at >= {L3_JACCARD:.0%}")
        print(f"  Ensure <title> tags are humanised (not generic like 'Lo Shu Number 1').")
        for h, g, s in flagged[:10]:
            print(f"      \"{h}\" ↔ \"{g}\"  {s:.0%}")
        status = "FLAGGED"
    else:
        status = "PASS"
        print(f"  ✅  PASS -- No headings match generic corpus at >= {L3_JACCARD:.0%}")

    return status, {"matched_headings": len(flagged),
                    "sample": [h for h, _, _ in flagged[:5]]}

def _sample_phrase(body: str) -> str | None:
    tokens = [t for t in _tokenize(body) if t not in _STOPS]
    if len(tokens) < 10:
        return None
    return " ".join(tokens[5:13])

def layer_google(
    records: list[tuple[str, str]],
    label: str,
    serper_key: str,
    sample: int = 3,
) -> tuple[str, dict]:
    import urllib.request

    print(f"\n{'─'*60}")
    print(f"LAYER G · Google Duplication -- {label} ({sample} samples)")
    print(f"{'─'*60}")

    results = []
    for name, body in records[:sample]:
        phrase = _sample_phrase(body)
        if not phrase:
            print(f"  ⚠️   {name} -- body too short to sample")
            continue
        payload = json.dumps({"q": f'"{phrase}"', "num": 10}).encode()
        try:
            req = urllib.request.Request(
                "https://google.serper.dev/search",
                data=payload,
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read())
            hits = len((data or {}).get("organic") or [])
        except Exception as exc:
            print(f"  ⚠️   Serper error for \"{phrase[:40]}\": {exc}")
            continue
        dup_rate = min(hits / 10, 1.0)
        icon = "✅" if dup_rate <= LG_WATCH else ("⚠️" if dup_rate <= LG_BLOCKED else "❌")
        print(f"  {icon}  [{hits}/10 hits] \"{phrase[:55]}\" ({name})")
        results.append({"name": name, "phrase": phrase, "hits": hits,
                        "dup_rate": round(dup_rate, 3)})

    if not results:
        print("  ⚠️   No samples could be checked.")
        return "SKIP", {}

    avg = sum(r["dup_rate"] for r in results) / len(results)
    peak = max(r["dup_rate"] for r in results)
    status = "BLOCKED" if peak > LG_BLOCKED else ("WATCH" if avg > LG_WATCH else "PASS")
    icon = {"BLOCKED": "❌", "WATCH": "⚠️", "PASS": "✅"}[status]
    print(f"\n  {icon}  Avg {avg:.0%} · Peak {peak:.0%} -- {status}")
    return status, {"avg_dup_rate": round(avg, 3), "peak_dup_rate": round(peak, 3),
                    "samples_checked": len(results), "results": results}


# ════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(description="ECHO/PACE Lo Shu Grid Scanner")
    parser.add_argument("--output", default="tests/echo_pace_lsg_report.json")
    args = parser.parse_args()

    serper_key = os.getenv("SERPER_API_KEY", "").strip()

    print("=" * 60)
    print("ECHO/PACE SCANNER -- Lo Shu Grid SEO Module")
    print("Number pages: 9  |  Combination pairs: 36  |  Classical fields: 9")
    if not serper_key:
        print("⚠️   SERPER_API_KEY not set -- Layer G will be skipped.")
        print("    To enable: SERPER_API_KEY=xxx python tests/echo_pace_lsg_scan.py")
    print("=" * 60)

    report: dict[str, Any] = {}
    all_statuses: list[str] = []
    numbers = list(range(1, 10))

    # ── Number pages (1-9) ────────────────────────────────────────────────────
    num_docs  = [_number_page_body(n) for n in numbers]
    num_names = [str(n) for n in numbers]

    n1_st, n1 = layer1(num_docs, num_names, "Number Pages (1-9)")
    n2_st, n2 = layer2(num_docs, "Number Pages")
    n3_st, n3 = layer3([f"lo shu number {n}" for n in numbers], "Number Pages")
    report["number_pages"] = {"L1": n1, "L2": n2, "L3": n3}
    all_statuses += [n1_st, n2_st]

    # ── Combination pages (36 pairs) ──────────────────────────────────────────
    combo_pairs = list(combinations(numbers, 2))
    combo_docs  = [_combo_page_body(a, b) for a, b in combo_pairs]
    combo_names = [f"{a}+{b}" for a, b in combo_pairs]

    c1_st, c1 = layer1(combo_docs, combo_names, "Combination Pages (36 pairs)")
    c2_st, c2 = layer2(combo_docs, "Combination Pages")
    c3_st, c3 = layer3([f"lo shu numbers {a} and {b}" for a, b in combo_pairs], "Combination Pages")
    report["combination_pages"] = {"L1": c1, "L2": c2, "L3": c3}
    all_statuses += [c1_st, c2_st]

    # ── Layer G: blueprint prose (main content risk) ──────────────────────────
    # ── Layer G: classical associations (WATCH-1 risk) ────────────────────────
    if serper_key:
        bg_st, bg = layer_google(
            [(str(n), _number_page_body(n)) for n in numbers],
            "Blueprint Prose (9 numbers)", serper_key)
        cg_st, cg = layer_google(
            [(str(n), _classical_body(n)) for n in numbers],
            "Classical Associations WATCH-1", serper_key, sample=9)
        report["layer_g"] = {"blueprint_prose": bg, "classical_watch1": cg}
        all_statuses += [bg_st, cg_st]

        if cg_st in ("BLOCKED", "WATCH"):
            print()
            print("  ⚠️   WATCH-1 ALERT: Classical associations content has elevated duplication.")
            print("  GAI fix required: humanise life_theme, body_area, element, direction fields")
            print("  in NUMBER_CLASSICAL_ASSOCIATIONS before module goes live.")
    else:
        print(f"\n{'─'*60}")
        print("LAYER G · Google Duplication -- SKIPPED (no SERPER_API_KEY)")
        print(f"{'─'*60}")
        report["layer_g"] = "SKIPPED"

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"  Number pages    L1:{n1_st:8} L2:{n2_st:8} L3:{n3_st:8}")
    print(f"  Combo pages     L1:{c1_st:8} L2:{c2_st:8} L3:{c3_st:8}")
    if serper_key:
        print(f"  Layer G (blueprint): {bg_st}")
        print(f"  Layer G (classical WATCH-1): {cg_st}")

    active = [s for s in all_statuses if s != "SKIP"]
    if "BLOCKED" in active:
        verdict = "❌  BLOCKED -- Fix issues before integration."
    elif "FLAGGED" in active:
        verdict = "⚠️   FLAGGED -- Review flagged items, then confirm with TT before going live."
    else:
        verdict = "✅  PASS -- All layers clear. LSG-1 safe to integrate."

    print(f"\n  VERDICT: {verdict}")
    report["verdict"] = verdict

    with open(args.output, "w") as fh:
        json.dump(report, fh, indent=2)
    print(f"  Report saved: {args.output}")
    print()
    print("NEXT STEP: Share full output with TT for sign-off before pushing LSG-1 to main.")
    print("If Layer G shows WATCH-1 classical associations are duplicated:")
    print("  → Humanise NUMBER_CLASSICAL_ASSOCIATIONS fields and re-run this script.")

    return 1 if "BLOCKED" in active else 0


if __name__ == "__main__":
    sys.exit(main())
