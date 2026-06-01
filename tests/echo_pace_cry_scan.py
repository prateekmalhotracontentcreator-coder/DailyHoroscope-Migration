#!/usr/bin/env python3
"""
ECHO/PACE 3-Layer Scanner -- Crystal Healing SEO Module (CRY-1)
===============================================================
Scans crystal and intention page types against L1/L2/L3 quality gates.

Page types:
  crystal    (50 pages) -- individual crystal profiles
  intention  (20 pages) -- intention-based crystal guides

USAGE
-----
  cd /path/to/DailyHoroscope-Migration
  python tests/echo_pace_cry_scan.py
  SERPER_API_KEY=xxx python tests/echo_pace_cry_scan.py   # Layer G
"""
from __future__ import annotations

import json, math, os, re, sys
from collections import Counter
from itertools import combinations

_BACKEND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _BACKEND)

from crystal_data import get_crystal_docs, get_intention_docs

STOP = set("a an the is are was were be been being have has had do does did will would could should may might shall can need am i we you he she it they them their this that these those of in on at to for with by from about as into through during before after above below between but or and not no nor so yet both either neither each every all any few more most other some such only own same than too very just".split())

# ── Body extractors ───────────────────────────────────────────────────────────

def _crystal_body(doc: dict) -> str:
    parts = [doc.get("tagline", ""), doc.get("caution", ""), doc.get("affirmation", "")]
    hp = doc.get("healing_properties", {})
    if isinstance(hp, dict):
        parts.extend(str(v) for v in hp.values())
    for f in ("how_to_use", "cleansing_methods"):
        if doc.get(f):
            parts.extend(str(x) for x in doc[f])
    for fq in doc.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    wearing = doc.get("wearing", {})
    if isinstance(wearing, dict):
        for k in ("mantra", "activation"):
            if wearing.get(k):
                parts.append(str(wearing[k]))
    return " ".join(filter(None, parts))

def _crystal_title(doc: dict) -> str:
    return doc.get("meta_title", doc.get("display_name", ""))

def _intention_body(doc: dict) -> str:
    parts = []
    for f in ("description", "body", "intro", "guidance", "summary", "message", "affirmation"):
        if doc.get(f) and isinstance(doc[f], str):
            parts.append(doc[f])
    for f in ("crystals", "practices", "steps", "tips"):
        if doc.get(f) and isinstance(doc[f], list):
            parts.extend(str(x) for x in doc[f] if isinstance(x, str))
    for fq in doc.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    return " ".join(filter(None, parts))

def _intention_title(doc: dict) -> str:
    return doc.get("meta_title", doc.get("title", doc.get("display", doc.get("slug", ""))))

# ── Core ECHO/PACE functions ──────────────────────────────────────────────────

def _tokenise(text: str) -> list[str]:
    return [w for w in re.sub(r"[^a-z\s]", " ", text.lower()).split() if len(w) > 2]

def _tfidf_score(texts: list[str], labels: list[str]) -> tuple[float, str, str]:
    from math import log, sqrt
    n = len(texts)
    tokenised = [_tokenise(t) for t in texts]
    df: Counter[str] = Counter()
    for toks in tokenised:
        for w in set(toks):
            df[w] += 1
    idf = {w: log(n / df[w]) for w in df}
    vecs = []
    for toks in tokenised:
        tf = Counter(toks)
        total = max(len(toks), 1)
        vecs.append({w: (c / total) * idf[w] for w, c in tf.items()})

    worst, wlabel_i, wlabel_j = 0.0, "", ""
    for i, j in combinations(range(n), 2):
        a, b = vecs[i], vecs[j]
        dot = sum(a[w] * b.get(w, 0) for w in a)
        na = sqrt(sum(v**2 for v in a.values()))
        nb = sqrt(sum(v**2 for v in b.values()))
        if na == 0 or nb == 0:
            continue
        sim = dot / (na * nb)
        if sim > worst:
            worst, wlabel_i, wlabel_j = sim, labels[i], labels[j]
    return worst, wlabel_i, wlabel_j

def _ngram_check(texts: list[str], n: int = 4, threshold: float = 0.15) -> list[tuple[str, float]]:
    def ngrams(toks):
        filtered = [w for w in toks if w not in STOP]
        return [" ".join(filtered[i:i+n]) for i in range(len(filtered) - n + 1)]
    gram_docs: Counter[str] = Counter()
    total = len(texts)
    for text in texts:
        for g in set(ngrams(_tokenise(text))):
            gram_docs[g] += 1
    return sorted([(g, c/total) for g, c in gram_docs.items() if c/total > threshold], key=lambda x: -x[1])[:10]

def _jaccard_check(titles: list[str], threshold: float = 0.60) -> list[tuple[str, str, float]]:
    sets = [set(_tokenise(t)) - STOP for t in titles]
    violations = []
    for i, j in combinations(range(len(sets)), 2):
        u = sets[i] | sets[j]
        i_sect = sets[i] & sets[j]
        score = len(i_sect) / len(u) if u else 0
        if score > threshold:
            violations.append((titles[i], titles[j], score))
    return sorted(violations, key=lambda x: -x[2])[:10]

def scan_type(docs: list[dict], body_fn, title_fn, label: str) -> dict:
    bodies = [body_fn(d) for d in docs]
    titles = [title_fn(d) for d in docs]
    labels = [title_fn(d)[:40] for d in docs]

    worst_l1, wi, wj = _tfidf_score(bodies, labels)
    l1_status = "BLOCKED ❌" if worst_l1 >= 0.70 else ("FLAGGED ⚠️" if worst_l1 >= 0.50 else "PASS ✅")

    violations_l2 = _ngram_check(bodies)
    l2_status = "PASS ✅" if not violations_l2 else "FAIL ❌"

    violations_l3 = _jaccard_check(titles)
    l3_status = "PASS ✅" if not violations_l3 else "FLAGGED ⚠️"

    print(f"\n── {label} ({len(docs)} pages) ──────────────────")
    print(f"  L1 TF-IDF worst pair: {worst_l1:.1%}  {l1_status}")
    if worst_l1 >= 0.50:
        print(f"     Worst pair: {wi[:45]!r} vs {wj[:45]!r}")
    print(f"  L2 N-gram violations: {len(violations_l2)}  {l2_status}")
    for g, pct in violations_l2[:3]:
        print(f"     {g!r:55s} {pct:.0%}")
    print(f"  L3 Jaccard title pairs > 60%: {len(violations_l3)}  {l3_status}")
    for t1, t2, j in violations_l3[:3]:
        print(f"     {t1[:40]!r} vs {t2[:40]!r} = {j:.0%}")

    return {
        "label": label, "count": len(docs),
        "l1": {"worst": round(worst_l1, 4), "status": l1_status},
        "l2": {"violations": len(violations_l2), "status": l2_status},
        "l3": {"violations": len(violations_l3), "status": l3_status},
    }

def _layer_g(bodies: list[str], labels: list[str]) -> None:
    import urllib.request
    key = os.environ.get("SERPER_API_KEY", "")
    if not key:
        return
    print("\n── Layer G: Google Serper spot-check ────────────────────────")
    for body, label in zip(bodies, labels):
        phrase = body[:120].strip()
        req_body = json.dumps({"q": f'"{phrase}"', "num": 10}).encode()
        req = urllib.request.Request(
            "https://google.serper.dev/search",
            data=req_body,
            headers={"X-API-KEY": key, "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
                hits = len(data.get("organic", []))
                status = "BLOCKED ❌" if hits > 4 else ("WATCH ⚠️" if hits > 1 else "PASS ✅")
                print(f"  [{status}] hits={hits} | {label}: {phrase[:60]}")
        except Exception as e:
            print(f"  ERROR: {e}")

def main() -> None:
    print("=" * 65)
    print("ECHO // PACE Compliance Scan -- Crystal Healing Module (CRY-1)")
    print("L1 gate: < 50% PASS | 50-69% FLAGGED | >= 70% BLOCKED")
    print("L2 gate: no 4-gram in > 15% of pages")
    print("L3 gate: title Jaccard < 60%")
    print("=" * 65)

    crystal_docs = list(get_crystal_docs().values())
    intention_docs = list(get_intention_docs().values())

    results = []
    results.append(scan_type(crystal_docs, _crystal_body, _crystal_title, "CRYSTAL pages (50)"))
    results.append(scan_type(intention_docs, _intention_body, _intention_title, "INTENTION pages (20)"))

    # Layer G
    if os.environ.get("SERPER_API_KEY"):
        samples_bodies = [_crystal_body(crystal_docs[0]), _crystal_body(crystal_docs[24]), _intention_body(intention_docs[0])]
        samples_labels = [_crystal_title(crystal_docs[0]), _crystal_title(crystal_docs[24]), _intention_title(intention_docs[0])]
        _layer_g(samples_bodies, samples_labels)

    print("\n" + "=" * 65)
    all_l1 = [r["l1"]["worst"] for r in results]
    print(f"GLOBAL L1 WORST: {max(all_l1):.1%}  |  {'BLOCKED ❌' if max(all_l1) >= 0.70 else 'OK'}")
    print(f"L2 OVERALL: {'FAIL ❌' if any(r['l2']['violations'] > 0 for r in results) else 'PASS ✅'}")
    print(f"L3 OVERALL: {'FLAGGED ⚠️' if any(r['l3']['violations'] > 0 for r in results) else 'PASS ✅'}")
    print("=" * 65)

if __name__ == "__main__":
    main()
