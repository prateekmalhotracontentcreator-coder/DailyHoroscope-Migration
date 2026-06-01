#!/usr/bin/env python3
"""
ECHO/PACE 3-Layer Scanner -- SEO-20K Infrastructure Modules
============================================================
Covers 7 module groups:
  1. Sign Compatibility          (144 pages) -- local pure functions
  2. Remedy Hub                  (12 pages)  -- static JSX DOSHA_CONTENT
  3. Transit Profiles            (108 pages) -- seo_m3_builders
  4. Festival Regions            (480 pages) -- seo_m3_builders
  5. Character Placements        (432 pages) -- seo_m3_builders
  6. Per-Sign Horoscopes (meta)  (36 pages)  -- static JSX PERIOD_META
  7. Festival / Calendar / Hora  (5 pages)   -- static JSX FESTIVAL_DATA

Panchang & Choghadiya are LIVE-API (pyswisseph per city+date).
Content varies per request -- not applicable for static ECHO/PACE.
These are noted in the output with their API type.

PAID API MAP (Anthropic/Claude API calls on live page render):
  Per-Sign Horoscopes   YES -- generate_horoscope_with_llm() (claude-sonnet)
  All others            NO  -- pyswisseph / MongoDB / static data only

USAGE
-----
  cd /path/to/DailyHoroscope-Migration
  python tests/echo_pace_seo20k_scan.py
  SERPER_API_KEY=xxx python tests/echo_pace_seo20k_scan.py   # Layer G
"""
from __future__ import annotations

import json, os, re, sys
from collections import Counter
from itertools import combinations, product
from math import log, sqrt

_BACKEND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _BACKEND)

from seo_m3_catalog import (
    SIGN_SLUGS, PLANET_SLUGS, CHART_POINTS, CHART_POINT_META,
    REGION_SLUGS, FESTIVAL_SLUGS, HOUSES, HOUSE_META,
    PLANET_NAME_MAP, REGION_META, FESTIVAL_META, SIGN_NAME_MAP,
)
from seo_m3_builders import (
    build_character_placement_doc,
    build_transit_profile_doc,
    build_festival_region_doc,
)

STOP = set("a an the is are was were be been being have has had do does did will would could should may might shall can need am i we you he she it they them their this that these those of in on at to for with by from about as into through during before after above below between but or and not no nor so yet both either neither each every all any few more most other some such only own same than too very just".split())

# ── ECHO/PACE core ────────────────────────────────────────────────────────────

def _tok(text: str) -> list[str]:
    return [w for w in re.sub(r"[^a-z\s]", " ", text.lower()).split() if len(w) > 2]

def _tfidf_score(texts: list[str], labels: list[str]) -> tuple[float, str, str]:
    n = len(texts)
    if n < 2:
        return 0.0, "", ""
    tok = [_tok(t) for t in texts]
    df: Counter[str] = Counter()
    for toks in tok:
        for w in set(toks):
            df[w] += 1
    idf = {w: log(n / df[w]) for w in df}
    vecs = [{w: (Counter(t)[w] / max(len(t), 1)) * idf[w] for w in Counter(t)} for t in tok]
    worst, wli, wlj = 0.0, "", ""
    for i, j in combinations(range(n), 2):
        a, b = vecs[i], vecs[j]
        dot = sum(a[w] * b.get(w, 0) for w in a)
        na = sqrt(sum(v**2 for v in a.values()))
        nb = sqrt(sum(v**2 for v in b.values()))
        if na and nb:
            sim = dot / (na * nb)
            if sim > worst:
                worst, wli, wlj = sim, labels[i], labels[j]
    return worst, wli, wlj

def _ngram_check(texts: list[str], n: int = 4, threshold: float = 0.15) -> list[tuple[str, float]]:
    def ngrams(toks):
        f = [w for w in toks if w not in STOP]
        return [" ".join(f[i:i+n]) for i in range(len(f) - n + 1)]
    gram_docs: Counter[str] = Counter()
    total = len(texts)
    for text in texts:
        for g in set(ngrams(_tok(text))):
            gram_docs[g] += 1
    return sorted([(g, c/total) for g, c in gram_docs.items() if c/total > threshold], key=lambda x: -x[1])[:10]

def _jaccard_check(titles: list[str], threshold: float = 0.60) -> list[tuple[str, str, float]]:
    sets = [set(_tok(t)) - STOP for t in titles]
    viols = []
    for i, j in combinations(range(len(sets)), 2):
        u = sets[i] | sets[j]
        sc = len(sets[i] & sets[j]) / len(u) if u else 0
        if sc > threshold:
            viols.append((titles[i], titles[j], sc))
    return sorted(viols, key=lambda x: -x[2])[:10]

def _layer_g(samples: list[tuple[str, str]]) -> None:
    import urllib.request
    key = os.environ.get("SERPER_API_KEY", "")
    if not key:
        return
    print("\n── Layer G: Google Serper spot-check ────────────────────────")
    for phrase, label in samples:
        phrase = phrase[:110].strip()
        rb = json.dumps({"q": f'"{phrase}"', "num": 10}).encode()
        req = urllib.request.Request("https://google.serper.dev/search", data=rb,
                                     headers={"X-API-KEY": key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                hits = len(json.loads(r.read()).get("organic", []))
                st = "BLOCKED ❌" if hits > 4 else ("WATCH ⚠️" if hits > 1 else "PASS ✅")
                print(f"  [{st}] hits={hits:2d} | {label}: {phrase[:55]}")
        except Exception as e:
            print(f"  ERROR: {e}")

def _scan(docs: list[dict], body_fn, title_fn, label: str,
          sample_n: int | None = None, layer_g_samples: list | None = None) -> dict:
    import random
    if sample_n and len(docs) > sample_n:
        random.seed(42)
        docs = random.sample(docs, sample_n)
    bodies = [body_fn(d) for d in docs]
    titles = [title_fn(d) for d in docs]
    labels = [title_fn(d)[:50] for d in docs]

    worst, wli, wlj = _tfidf_score(bodies, labels)
    l1st = "BLOCKED ❌" if worst >= 0.70 else ("FLAGGED ⚠️" if worst >= 0.50 else "PASS ✅")
    viols_l2 = _ngram_check(bodies)
    l2st = "PASS ✅" if not viols_l2 else "FAIL ❌"
    viols_l3 = _jaccard_check(titles)
    l3st = "PASS ✅" if not viols_l3 else "FLAGGED ⚠️"

    print(f"\n── {label} ({len(docs)} pages) ──────────────────")
    print(f"  L1: {worst:.1%}  {l1st}")
    if worst >= 0.50:
        print(f"     Worst: {wli[:55]!r}")
        print(f"       vs:  {wlj[:55]!r}")
    print(f"  L2: {len(viols_l2)} violations  {l2st}")
    for g, pct in viols_l2[:3]:
        print(f"     {g!r:55s} {pct:.0%}")
    print(f"  L3: {len(viols_l3)} pairs > 60% Jaccard  {l3st}")
    for t1, t2, j in viols_l3[:3]:
        print(f"     {t1[:40]!r} vs {t2[:40]!r} = {j:.0%}")

    if layer_g_samples and os.environ.get("SERPER_API_KEY"):
        _layer_g(layer_g_samples)

    return {
        "label": label, "n": len(docs),
        "l1": {"score": round(worst, 4), "status": l1st},
        "l2": {"violations": len(viols_l2), "status": l2st, "top": [g for g, _ in viols_l2[:5]]},
        "l3": {"violations": len(viols_l3), "status": l3st},
    }

# ── Module builders ───────────────────────────────────────────────────────────

# 1. Sign Compatibility (144 pages) -- pure local functions
def _build_compat_docs() -> list[dict]:
    from compatibility_router import (
        SIGN_SLUGS as CSLUGS, SLUG_TO_SIGN,
        _build_summary, _koota_narrative,
        _compatibility_band, KOOTA_NAMES,
    )
    # Fixed max scores per koota (standard Gun Milan weights)
    KOOTA_MAX = {"varna": 1, "vashya": 2, "tara": 3, "yoni": 4,
                 "graha_maitri": 5, "gana": 6, "bhakoot": 7, "nadi": 8}
    docs = []
    for s1, s2 in combinations(CSLUGS, 2):
        n1, n2 = SLUG_TO_SIGN[s1], SLUG_TO_SIGN[s2]
        score = 18.0
        verdict, band_label = _compatibility_band(score)
        summary = _build_summary(n1, n2, verdict, score)
        narratives = []
        for kname, kdisp in KOOTA_NAMES.items():
            max_sc = KOOTA_MAX.get(kname, 4)
            ks = score / len(KOOTA_NAMES)
            narratives.append(_koota_narrative(kname, kdisp, ks, max_sc, n1, n2))
        docs.append({
            "meta_title": f"{n1}-{n2} Compatibility - Gun Milan Score & Analysis",
            "summary": summary,
            "narratives": " ".join(narratives),
        })
    return docs

def _compat_body(d: dict) -> str:
    return f"{d['summary']} {d['narratives']}"

def _compat_title(d: dict) -> str:
    return d["meta_title"]

# 2. Remedy Hub (12 dosha pages) -- static DOSHA_CONTENT from JSX
DOSHA_CONTENT = {
    "shani-sade-sati": {
        "meta_title": "Shani Sade Sati Remedies - Vedic Astrology Guide",
        "summary": "Shani Sade Sati is the seven-and-a-half-year Saturn transit over the 12th, 1st, and 2nd houses from the natal Moon. It is often associated with karmic pressure, delay, responsibility, and emotional heaviness.",
        "context": "Saturn disciplines, it does not destroy. The entire Sade Sati period is a karmic audit, not a punishment. Most people emerge from it with greater clarity about what they were building and why.",
    },
    "manglik-dosha": {
        "meta_title": "Manglik Dosha Remedies - Mars Placement Guide",
        "summary": "Manglik Dosha is linked with Mars occupying sensitive marriage houses. It is commonly discussed for marriage timing, temperament, conflict patterns, and high heat in relationships.",
        "context": "The Manglik label is often over-applied. Context matters: Mars in its own sign, an exalted Mars, or chart-level balancing factors all change the reading significantly.",
    },
    "pitru-dosha": {
        "meta_title": "Pitru Dosha Remedies - Ancestral Karma Guide",
        "summary": "Pitru Dosha is associated with unresolved ancestral karma, family lineage imbalance, or blocked blessings from the paternal line. It is often discussed when family progress feels delayed without a clear external cause.",
        "context": "Pitru Dosha remedies are less about specific gemstones and more about ancestral ritual, service, and conscious acknowledgment of lineage patterns.",
    },
    "kaal-sarp-dosha": {
        "meta_title": "Kaal Sarp Dosha Remedies - Rahu Ketu Axis Guide",
        "summary": "Kaal Sarp Dosha is associated with all grahas falling between Rahu and Ketu. It is traditionally linked with intensity, inner pressure, sudden reversals, and karmic acceleration.",
        "context": "Kaal Sarp can indicate a concentrated karmic path, not necessarily a cursed one. Many accomplished individuals carry this formation in their chart.",
    },
    "shani-mahadasha": {
        "meta_title": "Shani Mahadasha Remedies - Saturn Period Guide",
        "summary": "Shani Mahadasha is Saturn's 19-year period. It emphasizes discipline, realism, accountability, and long-cycle karmic correction.",
        "context": "Saturn Mahadasha is one of the most underestimated dasha periods. Its early years can feel grinding, but its later years often produce solid, lasting results if the work has been done.",
    },
    "rahu-mahadasha": {
        "meta_title": "Rahu Mahadasha Remedies - North Node Period Guide",
        "summary": "Rahu Mahadasha is a transformative period that can amplify ambition, confusion, desire, foreign themes, and sudden changes in direction.",
        "context": "Rahu Mahadasha rewards those who channel its energy into focused output. Undirected, it can scatter attention across too many directions simultaneously.",
    },
    "ketu-mahadasha": {
        "meta_title": "Ketu Mahadasha Remedies - South Node Period Guide",
        "summary": "Ketu Mahadasha often brings detachment, spiritual pull, loss of interest in former goals, and a sharper karmic focus on inner work.",
        "context": "Ketu's period is least understood and most mishandled. It calls for inward movement, not outward pushing. Resistance to that current is the primary source of its difficulty.",
    },
    "guru-chandal-yoga": {
        "meta_title": "Guru Chandal Yoga Remedies - Jupiter Rahu Conjunction Guide",
        "summary": "Guru Chandal Yoga is associated with Jupiter and Rahu joining closely. It may disturb wisdom, guidance, mentors, judgment, or the way belief systems are expressed.",
        "context": "The disturbance is often to established thinking rather than morality. Many reformers and unconventional thinkers carry this formation.",
    },
    "grahan-yoga": {
        "meta_title": "Grahan Yoga Remedies - Eclipse Affliction Guide",
        "summary": "Grahan Yoga is linked with eclipse-style affliction involving the Sun or Moon with Rahu or Ketu. It can show identity fog, emotional swings, and heightened karmic intensity.",
        "context": "Sun-Rahu Grahan Yoga and Moon-Ketu Grahan Yoga have distinct expressions. The former affects ego and authority; the latter affects emotional anchoring and the mother relationship.",
    },
    "nadi-dosha": {
        "meta_title": "Nadi Dosha Remedies - Compatibility Mismatch Guide",
        "summary": "Nadi Dosha is one of the most discussed Ashta-Koota mismatches in marriage matching. It is traditionally linked with vitality, health, and family harmony concerns in compatibility analysis.",
        "context": "Nadi Dosha cancellation conditions exist in traditional texts. A single mismatch score is rarely the complete picture in compatibility analysis.",
    },
    "gana-dosha": {
        "meta_title": "Gana Dosha Remedies - Temperament Mismatch Guide",
        "summary": "Gana Dosha reflects temperament mismatch in Gun Milan. It points to the way two people instinctively react, compromise, and share emotional style.",
        "context": "Deva-Rakshasa pairings often show the most friction but also the most growth. The mismatch is navigable when both partners understand its source.",
    },
    "bhakoot-dosha": {
        "meta_title": "Bhakoot Dosha Remedies - Moon Sign Mismatch Guide",
        "summary": "Bhakoot Dosha is a moon-sign mismatch in Ashta-Koota matching. It is traditionally associated with domestic harmony, family growth, and emotional alignment in marriage.",
        "context": "Bhakoot Dosha cancellation applies when both partners share specific planetary placements. It should be assessed alongside the full chart rather than as a standalone block.",
    },
}

def _remedy_docs() -> list[dict]:
    return [{"slug": k, **v} for k, v in DOSHA_CONTENT.items()]

def _remedy_body(d: dict) -> str:
    return f"{d['summary']} {d.get('context', '')}"

def _remedy_title(d: dict) -> str:
    return d["meta_title"]

# 3. Transit Profiles (108 pages) -- seo_m3_builders
def _build_transit_docs() -> list[dict]:
    docs = []
    for p, s in product(PLANET_SLUGS, SIGN_SLUGS):
        try:
            docs.append(build_transit_profile_doc(p, s))
        except Exception:
            pass
    return docs

def _transit_body(d: dict) -> str:
    parts = []
    for f in ("summary", "overview", "body", "hook", "description"):
        if d.get(f) and isinstance(d[f], str):
            parts.append(d[f])
    for f in ("transit_themes", "watch_for", "remedies"):
        if d.get(f) and isinstance(d[f], list):
            parts.extend(str(x) for x in d[f])
    for fq in d.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    for item in d.get("sign_impacts", []):
        if isinstance(item, dict):
            parts.append(item.get("message", ""))
    return " ".join(filter(None, parts))

def _transit_title(d: dict) -> str:
    return d.get("meta_title", d.get("title", ""))

# 4. Festival Regions (480 pages) -- seo_m3_builders
def _build_festival_docs(sample_n: int = 100) -> list[dict]:
    import random; random.seed(42)
    combos = list(product(FESTIVAL_SLUGS, REGION_SLUGS))
    random.shuffle(combos)
    docs = []
    for f, r in combos[:sample_n]:
        try:
            docs.append(build_festival_region_doc(f, r))
        except Exception:
            pass
    return docs

def _festival_body(d: dict) -> str:
    parts = []
    for f in ("summary", "overview", "body", "description", "hook"):
        if d.get(f) and isinstance(d[f], str):
            parts.append(d[f])
    for f in ("traditions", "steps"):
        if d.get(f) and isinstance(d[f], list):
            parts.extend(str(x) for x in d[f])
    for fq in d.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    return " ".join(filter(None, parts))

def _festival_title(d: dict) -> str:
    return d.get("meta_title", d.get("title", ""))

# 5. Character Placements (432 pages) -- seo_m3_builders
def _build_char_docs(sample_n: int = 120) -> list[dict]:
    import random; random.seed(42)
    combos = list(product(SIGN_SLUGS, [c["slug"] for c in CHART_POINTS], [h["slug"] for h in HOUSES]))
    random.shuffle(combos)
    docs = []
    for s, c, h in combos[:sample_n]:
        try:
            docs.append(build_character_placement_doc(s, c, h))
        except Exception:
            pass
    return docs

def _char_body(d: dict) -> str:
    parts = []
    for f in ("summary", "overview", "body", "description", "hook"):
        if d.get(f) and isinstance(d[f], str):
            parts.append(d[f])
    traits = d.get("traits", {})
    if isinstance(traits, dict):
        for k in ("strengths", "challenges", "life_themes"):
            v = traits.get(k, [])
            if isinstance(v, list):
                parts.extend(str(x) for x in v)
    for fq in d.get("faq", []):
        if isinstance(fq, dict):
            parts.append(fq.get("a", "") or fq.get("answer", ""))
    return " ".join(filter(None, parts))

def _char_title(d: dict) -> str:
    return d.get("meta_title", d.get("title", ""))

# 6. Per-Sign Horoscopes (36 pages) -- static JSX PERIOD_META templates
PERIOD_META = [
    ("tomorrow", s, f"{SIGN_NAME_MAP[s]} Horoscope Tomorrow - Vedic Prediction",
     f"Get your {SIGN_NAME_MAP[s]} horoscope for tomorrow. Vedic astrology prediction for love, career, health and lucky elements.")
    for s in SIGN_SLUGS
] + [
    ("weekly", s, f"{SIGN_NAME_MAP[s]} Weekly Horoscope - This Week's Vedic Forecast",
     f"{SIGN_NAME_MAP[s]} weekly horoscope - your 7-day Vedic forecast for love, career, and wellness. Updated every week.")
    for s in SIGN_SLUGS
] + [
    ("monthly", s, f"{SIGN_NAME_MAP[s]} Monthly Horoscope - May 2026 Vedic Forecast",
     f"{SIGN_NAME_MAP[s]} horoscope for May 2026 - full monthly Vedic forecast covering love, career, health, and auspicious dates.")
    for s in SIGN_SLUGS
]

def _horoscope_docs() -> list[dict]:
    return [{"period": p, "sign": s, "meta_title": t, "description": d}
            for p, s, t, d in PERIOD_META]

def _horoscope_body(d: dict) -> str:
    return f"{d['meta_title']} {d['description']}"

def _horoscope_title(d: dict) -> str:
    return d["meta_title"]

# 7. Festival / Calendar / Hora editorial pages (5 pages) -- static JSX
STATIC_EDITORIAL = [
    {
        "meta_title": "Holi 2026 - Date, Puja Muhurat & Rituals",
        "body": "Holi is the ancient Hindu festival of colours, celebrated on Purnima (full moon) of Phalguna month. It marks the victory of good over evil and the arrival of spring.",
    },
    {
        "meta_title": "Diwali 2026 - Date, Lakshmi Puja Muhurat & Rituals",
        "body": "Diwali is the most celebrated Hindu festival, marking Lord Ram's return to Ayodhya and the victory of light over darkness, on Amavasya of Kartik month.",
    },
    {
        "meta_title": "Karwa Chauth 2026 - Date, Moonrise Time & Puja Muhurat",
        "body": "Karwa Chauth is observed by married Hindu women who fast from sunrise to moonrise, praying for the long life and wellbeing of their husbands.",
    },
    {
        "meta_title": "Indian Festival Calendar 2026 - All Hindu Festivals & Dates",
        "body": "Complete Indian festival calendar for 2026 with all Hindu festivals, auspicious dates, and Panchang-backed tithi timings across all 12 months.",
    },
    {
        "meta_title": "Hora Today - Planetary Hour Calculator by City",
        "body": "Hora is the ancient Vedic system of planetary hours. Each hora hour is ruled by one of the seven classical planets, cycling in a fixed order through day and night.",
    },
]

def _editorial_body(d: dict) -> str:
    return d["body"]

def _editorial_title(d: dict) -> str:
    return d["meta_title"]

# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 68)
    print("ECHO // PACE Scan -- SEO-20K Infrastructure Modules")
    print("L1 gate: < 50% PASS | 50-69% FLAGGED | >= 70% BLOCKED")
    print("L2 gate: no 4-gram in > 15% of pages | L3 gate: Jaccard < 60%")
    print("=" * 68)

    print("\n⚠️  PAID API MAP (Anthropic/Claude called on live page render):")
    print("  Per-Sign Horoscopes (tomorrow/wk/mo)  → YES  (claude-sonnet-4)")
    print("  All other modules below               → NO   (pyswisseph / MongoDB / static data)")

    print("\n⚠️  LIVE-API ONLY (content computed per request -- no static body to scan):")
    print("  City Panchang   → pyswisseph per city+date → L1/L2/L3 N/A (no template duplication risk)")
    print("  Choghadiya      → pyswisseph per city+date → L1/L2/L3 N/A (no template duplication risk)")

    results = []

    # 1. Sign Compatibility
    print("\nBuilding Sign Compatibility docs...")
    try:
        compat_docs = _build_compat_docs()
        r = _scan(compat_docs, _compat_body, _compat_title, "SIGN COMPATIBILITY (144 pages)",
                  layer_g_samples=[(compat_docs[0]["summary"][:100], "compat-aries-taurus")])
        results.append(r)
    except Exception as e:
        print(f"  ERROR building compatibility: {e}")

    # 2. Remedy Hub
    print("\nBuilding Remedy Hub docs (static DOSHA_CONTENT)...")
    remedy_docs = _remedy_docs()
    r = _scan(remedy_docs, _remedy_body, _remedy_title, "REMEDY HUB (12 dosha pages)")
    results.append(r)

    # 3. Transit Profiles
    print("\nBuilding Transit Profile docs (108 planet×sign)...")
    try:
        transit_docs = _build_transit_docs()
        r = _scan(transit_docs, _transit_body, _transit_title, "TRANSIT PROFILES (108 pages)",
                  sample_n=80,
                  layer_g_samples=[(transit_docs[0].get("summary", "")[:100], transit_docs[0].get("meta_title", "")[:50])])
        results.append(r)
    except Exception as e:
        print(f"  ERROR building transit profiles: {e}")

    # 4. Festival Regions (sampled 100/480)
    print("\nBuilding Festival Region docs (sample 100/480)...")
    try:
        festival_docs = _build_festival_docs(sample_n=100)
        r = _scan(festival_docs, _festival_body, _festival_title, "FESTIVAL REGIONS (sample 100/480)")
        results.append(r)
    except Exception as e:
        print(f"  ERROR building festival regions: {e}")

    # 5. Character Placements (sampled 120/432)
    print("\nBuilding Character Placement docs (sample 120/432)...")
    try:
        char_docs = _build_char_docs(sample_n=120)
        r = _scan(char_docs, _char_body, _char_title, "CHARACTER PLACEMENTS (sample 120/432)",
                  layer_g_samples=[(char_docs[0].get("summary", "")[:100], char_docs[0].get("meta_title", "")[:50])])
        results.append(r)
    except Exception as e:
        print(f"  ERROR building character placements: {e}")

    # 6. Per-Sign Horoscopes (template/meta layer only)
    print("\nScanning Per-Sign Horoscope meta templates (36 pages)...")
    horo_docs = _horoscope_docs()
    r = _scan(horo_docs, _horoscope_body, _horoscope_title, "PER-SIGN HOROSCOPES meta-layer (36 pages)")
    results.append(r)

    # 7. Festival / Calendar / Hora editorial (5 pages)
    print("\nScanning Festival / Calendar / Hora editorial (5 pages)...")
    r = _scan(STATIC_EDITORIAL, _editorial_body, _editorial_title, "FESTIVAL / CALENDAR / HORA (5 editorial pages)")
    results.append(r)

    # ── Global summary
    print("\n" + "=" * 68)
    print("GLOBAL SUMMARY")
    print("=" * 68)
    print(f"{'Module':<42} {'L1':>8} {'L1 Status':>15} {'L2 Viols':>9} {'L3 Viols':>9}")
    print("-" * 68)
    for r in results:
        print(f"{r['label'][:42]:<42} {r['l1']['score']:>7.1%} {r['l1']['status']:>15} {r['l2']['violations']:>9} {r['l3']['violations']:>9}")
    print("=" * 68)

if __name__ == "__main__":
    main()
