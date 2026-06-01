#!/usr/bin/env python3
"""
ECHO/PACE 3-Layer Scanner -- Rudraksha SEO Module (RUD-1)
=========================================================
Scans all 4 Rudraksha page types against L1/L2/L3 quality gates.

Page types:
  mukhi    (21 pages)  -- 1 Mukhi through 21 Mukhi
  planet   (9 pages)   -- Sun, Moon, Mars, etc.
  problem  (20 pages)  -- Career, Relationships, etc.
  sign     (12 pages)  -- Aries, Taurus, etc.

USAGE
-----
  cd /path/to/DailyHoroscope-Migration
  python tests/echo_pace_rud_scan.py
  SERPER_API_KEY=xxx python tests/echo_pace_rud_scan.py   # Layer G
"""
from __future__ import annotations

import json, math, os, re, sys
from collections import Counter
from itertools import combinations

_BACKEND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _BACKEND)

from rudraksha_content import (
    get_rudraksha_documents,
    get_planet_rudraksha_documents,
    get_problem_rudraksha_documents,
    get_sign_rudraksha_documents,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

STOP = set("a an the is are was were be been being have has had do does did will would could should may might shall can need am i we you he she it they them their this that these those of in on at to for with by from about as into through during before after above below between but or and not no nor so yet both either neither each every all any few more most other some such only own same than too very just".split())

def _tokenise(text: str) -> list[str]:
    return [w for w in re.sub(r"[^a-z\s]", " ", text.lower()).split() if len(w) > 2]

def _body(doc: dict) -> str:
    parts = []
    for f in ("overview", "rarity", "price_range"):
        if doc.get(f) and isinstance(doc[f], str):
            parts.append(doc[f])
    for f in ("benefits", "cautions", "best_for"):
        if doc.get(f) and isinstance(doc[f], list):
            parts.extend(str(x) for x in doc[f])
    wi = doc.get("wearing_instructions", {})
    if isinstance(wi, dict):
        parts.extend(str(v) for v in wi.values() if isinstance(v, str))
    for fq in doc.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    # planet/problem/sign may use different keys
    for f in ("description", "guidance", "body", "content", "intro", "recommendation"):
        if doc.get(f) and isinstance(doc[f], str):
            parts.append(doc[f])
    return " ".join(parts)

def _title(doc: dict) -> str:
    for f in ("meta_title", "title", "name"):
        if doc.get(f):
            return doc[f]
    return ""

def _tfidf_score(texts: list[str]) -> tuple[float, str, str]:
    """Return worst-pair cosine and the two doc labels."""
    from math import log, sqrt

    n = len(texts)
    tokenised = [_tokenise(t) for t in texts]
    # IDF
    df: Counter[str] = Counter()
    for toks in tokenised:
        for w in set(toks):
            df[w] += 1
    idf = {w: log(n / df[w]) for w in df}
    # TF-IDF vectors
    vecs = []
    for toks in tokenised:
        tf = Counter(toks)
        total = max(len(toks), 1)
        vec = {w: (c / total) * idf[w] for w, c in tf.items()}
        vecs.append(vec)

    worst, wi, wj = 0.0, 0, 1
    for i, j in combinations(range(n), 2):
        a, b = vecs[i], vecs[j]
        dot = sum(a[w] * b.get(w, 0) for w in a)
        na = sqrt(sum(v ** 2 for v in a.values()))
        nb = sqrt(sum(v ** 2 for v in b.values()))
        if na == 0 or nb == 0:
            continue
        sim = dot / (na * nb)
        if sim > worst:
            worst, wi, wj = sim, i, j
    return worst, wi, wj

def _ngram_check(texts: list[str], n: int = 4, threshold: float = 0.15) -> list[tuple[str, float]]:
    """Return 4-grams (stop filtered) appearing in > threshold fraction of docs."""
    def ngrams(toks):
        filtered = [w for w in toks if w not in STOP]
        return [" ".join(filtered[i:i+n]) for i in range(len(filtered) - n + 1)]

    gram_docs: Counter[str] = Counter()
    total = len(texts)
    for text in texts:
        toks = _tokenise(text)
        for g in set(ngrams(toks)):
            gram_docs[g] += 1

    violations = [(g, gram_docs[g] / total) for g in gram_docs if gram_docs[g] / total > threshold]
    return sorted(violations, key=lambda x: -x[1])[:10]

def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def _jaccard_check(titles: list[str], threshold: float = 0.60) -> list[tuple[str, str, float]]:
    """Return title pairs with Jaccard > threshold."""
    sets = [set(_tokenise(t)) - STOP for t in titles]
    violations = []
    for i, j in combinations(range(len(sets)), 2):
        j_score = _jaccard(sets[i], sets[j])
        if j_score > threshold:
            violations.append((titles[i], titles[j], j_score))
    return sorted(violations, key=lambda x: -x[2])[:10]

def _layer_g(samples: list[str], label: str) -> list[dict]:
    """Serper spot-check. Requires SERPER_API_KEY."""
    import urllib.request
    key = os.environ.get("SERPER_API_KEY", "")
    if not key:
        return []
    results = []
    for phrase in samples:
        body = json.dumps({"q": f'"{phrase}"', "num": 10}).encode()
        req = urllib.request.Request(
            "https://google.serper.dev/search",
            data=body,
            headers={"X-API-KEY": key, "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
                hits = len(data.get("organic", []))
                results.append({"phrase": phrase[:80], "hits": hits, "status": "BLOCKED" if hits > 4 else "WATCH" if hits > 1 else "PASS"})
        except Exception as e:
            results.append({"phrase": phrase[:80], "hits": -1, "status": f"ERROR: {e}"})
    return results

# ── Scanner ───────────────────────────────────────────────────────────────────

THRESHOLDS = {"pass": 0.50, "flagged": 0.50, "blocked": 0.70}

def scan_page_type(docs: list[dict], label: str) -> dict:
    bodies = [_body(d) for d in docs]
    titles = [_title(d) for d in docs]
    n = len(docs)

    # L1
    worst_l1, wi, wj = _tfidf_score(bodies)
    l1_status = "BLOCKED ❌" if worst_l1 >= THRESHOLDS["blocked"] else ("FLAGGED ⚠️" if worst_l1 >= THRESHOLDS["flagged"] else "PASS ✅")

    # L2
    violations_l2 = _ngram_check(bodies, n=4, threshold=0.15)
    l2_status = "PASS ✅" if not violations_l2 else "FAIL ❌"

    # L3
    violations_l3 = _jaccard_check(titles, threshold=0.60)
    l3_status = "PASS ✅" if not violations_l3 else "FLAGGED ⚠️"

    print(f"\n── {label} ({n} pages) ──────────────────")
    print(f"  L1 TF-IDF worst pair: {worst_l1:.1%}  {l1_status}")
    if worst_l1 >= THRESHOLDS["flagged"]:
        print(f"     Worst pair: [{titles[wi][:50]!r}] vs [{titles[wj][:50]!r}]")
    print(f"  L2 N-gram violations: {len(violations_l2)}  {l2_status}")
    for g, pct in violations_l2[:3]:
        print(f"     {g!r:50s} {pct:.0%}")
    print(f"  L3 Jaccard title pairs > 60%: {len(violations_l3)}  {l3_status}")
    for t1, t2, j in violations_l3[:3]:
        print(f"     {t1[:40]!r} vs {t2[:40]!r} = {j:.0%}")

    return {
        "label": label,
        "count": n,
        "l1": {"worst": round(worst_l1, 4), "status": l1_status},
        "l2": {"violations": len(violations_l2), "status": l2_status, "top": [g for g, _ in violations_l2[:5]]},
        "l3": {"violations": len(violations_l3), "status": l3_status},
    }

def main() -> None:
    print("=" * 65)
    print("ECHO // PACE Compliance Scan -- Rudraksha Module (RUD-1)")
    print("L1 gate: < 50% PASS | 50-69% FLAGGED | >= 70% BLOCKED")
    print("L2 gate: no 4-gram in > 15% of pages")
    print("L3 gate: title Jaccard < 60%")
    print("=" * 65)

    results = []
    results.append(scan_page_type(get_rudraksha_documents(), "MUKHI pages (21)"))
    results.append(scan_page_type(get_planet_rudraksha_documents(), "PLANET pages (9)"))
    results.append(scan_page_type(get_problem_rudraksha_documents(), "PROBLEM pages (20)"))
    results.append(scan_page_type(get_sign_rudraksha_documents(), "SIGN pages (12)"))

    # Layer G -- stratified sampling: 2 phrases per page type (8 total)
    # Picks a mid-body sentence (15-25 words) to avoid title/meta noise.
    # Targets: worst-L1 pair within each type + 1 random spot-check.
    serper_key = os.environ.get("SERPER_API_KEY", "")
    if serper_key:
        print("\n── Layer G: Google Serper spot-check (8 samples, 2 per type) ──")

        def _pick_sentence(text: str) -> str:
            """Extract first sentence in the 15-25 word range."""
            for sent in re.split(r"(?<=[.!?])\s+", text):
                words = sent.split()
                if 15 <= len(words) <= 25:
                    return sent.strip()
            # fallback: first 20 words
            words = text.split()
            return " ".join(words[:20]).strip()

        mukhis   = get_rudraksha_documents()
        planets  = get_planet_rudraksha_documents()
        problems = get_problem_rudraksha_documents()
        signs    = get_sign_rudraksha_documents()

        # 2 per type: index 0 (worst-L1 anchor) + mid-set spot-check
        raw_samples = [
            ("MUKHI-worst",   _pick_sentence(_body(mukhis[0]))),
            ("MUKHI-spot",    _pick_sentence(_body(mukhis[10]))),
            ("PLANET-worst",  _pick_sentence(_body(planets[0]))),
            ("PLANET-spot",   _pick_sentence(_body(planets[4]))),
            ("PROBLEM-worst", _pick_sentence(_body(problems[0]))),
            ("PROBLEM-spot",  _pick_sentence(_body(problems[10]))),
            ("SIGN-worst",    _pick_sentence(_body(signs[0]))),
            ("SIGN-spot",     _pick_sentence(_body(signs[6]))),
        ]

        # deduplicate blanks / too-short
        samples = [(lbl, s) for lbl, s in raw_samples if len(s.split()) >= 10]

        import urllib.request
        g_blocked = 0
        for lbl, phrase in samples:
            body_req = json.dumps({"q": f'"{phrase}"', "num": 10}).encode()
            req = urllib.request.Request(
                "https://google.serper.dev/search",
                data=body_req,
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
            )
            try:
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = json.loads(r.read())
                    hits = len(data.get("organic", []))
                    status = "BLOCKED" if hits > 4 else "WATCH" if hits > 1 else "PASS"
                    if status == "BLOCKED":
                        g_blocked += 1
                    print(f"  [{status:7s}] hits={hits:2d} | [{lbl}] {phrase[:65]}")
            except Exception as e:
                print(f"  [ERROR  ]         | [{lbl}] {e}")

        print(f"\n  Layer G summary: {g_blocked}/{len(samples)} BLOCKED"
              f"  {'❌ FAIL' if g_blocked else '✅ PASS'}")

    print("\n" + "=" * 65)
    all_l1 = [r["l1"]["worst"] for r in results]
    any_blocked = any(r["l1"]["worst"] >= 0.70 for r in results)
    any_l2_fail = any(r["l2"]["violations"] > 0 for r in results)
    any_l3_flag = any(r["l3"]["violations"] > 0 for r in results)

    print(f"GLOBAL L1 WORST: {max(all_l1):.1%}  |  {'BLOCKED ❌' if any_blocked else 'OK'}")
    print(f"L2 OVERALL: {'FAIL ❌' if any_l2_fail else 'PASS ✅'}")
    print(f"L3 OVERALL: {'FLAGGED ⚠️' if any_l3_flag else 'PASS ✅'}")
    print("=" * 65)

if __name__ == "__main__":
    main()
