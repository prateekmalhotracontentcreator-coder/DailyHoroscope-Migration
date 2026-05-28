# GAI Brief -- M3-FIX-2: Festival × Region Summary Compliance Fix
> ECHO // PACE Process 1 application for Festival-Region module
> Filed: 2026-05-26 | Module: M3 Festival-Region | Ceiling: 40%

---

## The Problem in One Line

The `summary` field in the festival-region page builder has a structural flaw: any content that is *per-festival* repeats identically across all 30 regions, and any content that is *per-region* repeats identically across all 16 festivals. The TF-IDF worst-pair similarity is currently **71-78%** against a ceiling of 40%.

---

## What We Tried (and Why It Failed)

### Attempt 1 -- Short festival action phrase
Each festival got a 7-10 word action phrase (`"lighting diyas and sharing mithai through the neighbourhood"`).
- Result: 71% worst-pair
- Problem: phrase is ~10 words, shared region content is ~30 words. Region vocabulary dominates TF-IDF vectors → same-region pages score ~71%.

### Attempt 2 -- Long FESTIVAL_SPIRIT paragraph (~50 words per festival)
Each festival got a unique ~50-word paragraph describing its specific rituals (diyas, pichkaris, holika dahan, etc.).
- Result: 78% worst-pair
- Problem: the paragraph is now 95% of the text and identical across all 30 regions for the same festival. The short region anchor (~20 words) can't differentiate them → same-festival pages score ~78%.

### Root cause
The problem **cannot be solved with the current two-field approach** (festival text + region text). Any single field length that makes festival vocabulary dominate creates a same-festival similarity problem, and any length that makes region vocabulary dominate creates a same-region similarity problem.

---

## The Data Available (Read-Only -- No Schema Changes Required)

### FESTIVAL_META (16 festivals -- only these 2 fields are useful)
| slug | season |
|---|---|
| diwali | light, prosperity, and renewal |
| holi | colour, play, and spring release |
| navratri | devotion, dance, and Shakti worship |
| durga-puja | goddess celebration, artistry, and community worship |
| ganesh-chaturthi | auspicious beginnings and Ganapati devotion |
| janmashtami | bhakti, midnight worship, and Krishna leela |
| maha-shivaratri | night vigil, mantra, and inward stillness |
| makar-sankranti | harvest, sunlight, and transition |
| pongal | harvest gratitude and household abundance |
| onam | harvest joy, floral beauty, and family reunion |
| baisakhi | harvest thanksgiving and collective celebration |
| eid-ul-fitr | gratitude, prayer, and family feasting |
| christmas | joy, prayer, and generous gathering |
| gurupurab | guru remembrance, kirtan, and seva |
| ram-navami | dharma, maryada, and devotional celebration |
| hanuman-jayanti | strength, devotion, and protection |

### REGION_META (30 regions -- 4 useful fields per region)
| slug | zone | food | marker |
|---|---|---|---|
| andhra-pradesh | south | pulihora and laddus | temple processions and decorated entrances |
| arunachal-pradesh | northeast | community sweets and festive rice dishes | community halls and family gatherings |
| assam | east | pitha, payas, and festive rice offerings | music, prayer, and neighbourhood visits |
| bihar | north | thekua, kheer, and seasonal savouries | ghat visits and family puja routines |
| chhattisgarh | central | rice sweets and home-style prasad | community puja and local fairs |
| goa | west | coconut sweets and festive savouries | home altars and neighbourhood celebration routes |
| gujarat | west | fafda, jalebi, and festive thalis | garba grounds and bright rangoli work |
| haryana | north | halwa, puri, and farm-style festive meals | family courtyards and temple offerings |
| himachal-pradesh | north | sweet rice, prasad, and mountain-style meals | village temples and hillside processions |
| jharkhand | east | seasonal sweets and simple ceremonial meals | community grounds and family prayer circles |
| karnataka | south | kosambari, payasa, and temple-style prasada | flower decorations and early-morning puja |
| kerala | south | payasam, banana chips, and elaborate festive spreads | floral designs and household lamp lighting |
| madhya-pradesh | central | poha-style snacks, sweets, and prasad | mandir visits and old-city processions |
| maharashtra | west | modak, puran poli, and festive snacks | society pandals and family aarti gatherings |
| manipur | northeast | community feasts and seasonal sweets | cultural performance and temple participation |
| meghalaya | northeast | festive rice dishes and local sweets | church halls, homes, and community spaces |
| mizoram | northeast | shared festive meals and sweet offerings | community halls and neighbourhood visits |
| nagaland | northeast | community meals and celebratory desserts | collective singing and family hosting |
| odisha | east | khaja, pitha, and temple mahaprasad | alpona art and neighbourhood mandaps |
| punjab | north | kada prasad, festive rotis, and sweets | gurdwara seva and community langar |
| rajasthan | west | ghevar, dal-baati spreads, and festive mithai | courtyard lamps and royal-colour decoration |
| sikkim | northeast | shared sweets and festive rice dishes | community prayer and hillside celebrations |
| tamil-nadu | south | sweet pongal, sundal, and temple prasadam | kolam art, brass lamps, and dawn rituals |
| telangana | south | paramannam, laddus, and festive savouries | Bonalu-style community devotion and floral decor |
| tripura | east | festive rice offerings and sweets | family courtyards and community pandals |
| uttar-pradesh | north | peda, kachori, and traditional prasad | ghat rituals and temple crowds |
| uttarakhand | north | singori, halwa, and temple offerings | hill temples and family vrat observance |
| west-bengal | east | sandesh, khichuri bhog, and festive sweets | pandals, dhaak rhythms, and artistic decorations |
| nri-london | diaspora | potluck sweets and temple prasada | weekend community events and cultural centres |
| nri-new-york | diaspora | shared festive meals and mandir prasad | temple halls, family Zooms, and community gatherings |

---

## What We Need From GAI

**Deliver one of these two solutions:**

---

### Solution A -- Per-Combination Synthesis Dictionary (Preferred)

Provide a Python dict `FESTIVAL_REGION_SUMMARY` with **480 unique entries** (16 festivals × 30 regions), each containing a 2-3 sentence summary (40-70 words) that meets these rules:

1. **Every sentence references BOTH the festival AND the region** -- never a sentence that could apply to any other festival in the same region, or any other region for the same festival.
2. **No templated sentence structures** -- don't repeat "In {region}, {festival} centres on..." across multiple entries.
3. **Festival-specific vocabulary leads** -- the festival's unique ritual language (dhaak, pichkaris, sindoor khela, visarjan, pookalam, langar, etc.) must dominate the first sentence.
4. **Region-specific food + marker appear in different syntactic positions** across entries -- not always "families gather around {food}".
5. **TF-IDF worst-pair similarity < 40%** across the full 480 entries (using the same stop-word set as PROCESS_2: 'festival', 'celebration', 'region', 'local', 'ritual', 'community', 'family', 'observance').

**Expected format:**
```python
FESTIVAL_REGION_SUMMARY: dict[tuple[str, str], str] = {
    ("diwali", "west-bengal"): "...",
    ("diwali", "punjab"): "...",
    ("diwali", "tamil-nadu"): "...",
    # ... all 480 combinations
}
```

The builder then becomes:
```python
def _festival_summary(festival_slug: str, region_slug: str) -> str:
    return FESTIVAL_REGION_SUMMARY.get(
        (festival_slug, region_slug),
        f"{FESTIVAL_META[festival_slug]['name']} in {REGION_META[region_slug]['name']}."
    )
```

---

### Solution B -- Structural Fix to the Builder (If A is Not Feasible)

If providing 480 unique entries is not feasible, deliver a revised `_festival_summary()` function that:

1. Uses a minimum of **3 independent data dimensions** per combination -- e.g., `(festival_slug, zone, food_index_by_hash, marker_index_by_hash)` to create semantic distance even from limited catalog data.
2. Achieves **< 40% worst-pair TF-IDF** on the full 480 pages.
3. Is verified against the compliance script (see Process 2) before delivery.

You must run the verification yourself and include the output showing:
```
Worst-pair similarity (full 480 pages): XX.X%  [ceiling: 40%]  ✅ PASS
```

---

## Compliance Verification Command

Deliver this output with your solution (run against the full 480 docs):

```python
# Test harness -- run in DailyHoroscope-Migration root
import sys, random
sys.path.insert(0, 'backend')
from seo_m3_builders import build_festival_region_doc
from seo_m3_catalog import FESTIVAL_META, REGION_META
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text as sk_text

random.seed(42)
festival_slugs = list(FESTIVAL_META.keys())
region_slugs = list(REGION_META.keys())
all_pages = [
    build_festival_region_doc(f, r)['summary']
    for f in festival_slugs for r in region_slugs
]

STOP = list(sk_text.ENGLISH_STOP_WORDS.union(
    {'festival','celebration','region','local','ritual','community','family','observance','celebrate','india','day'}
))
vec = TfidfVectorizer(stop_words=STOP, ngram_range=(1,2), min_df=1, max_features=30000)
sample = random.sample(all_pages, 60)
mat = vec.fit_transform(sample)
sim = cosine_similarity(mat)
n = len(sample)
worst = max(sim[i][j] for i in range(n) for j in range(i+1, n)) * 100
print(f'Unique summaries: {len(set(all_pages))}/480')
print(f'Worst-pair similarity (60-page sample): {worst:.1f}%  [ceiling: 40%]')
print('PASS' if worst < 40 else 'FAIL')
```

---

## Files to Deliver

| File | Content |
|---|---|
| `backend/seo_m3_builders.py` -- `_festival_summary()` function | Updated function only (not the whole file) |
| OR `backend/seo_m3_festival_summaries.py` | Standalone `FESTIVAL_REGION_SUMMARY` dict if Solution A |
| Compliance output | Paste of the verification script output showing PASS |

---

## Constraints

- Do NOT change `FESTIVAL_META` or `REGION_META` schemas -- they are used by other builders
- Do NOT change any function other than `_festival_summary()`
- The builder is in `backend/seo_m3_builders.py` -- the function signature stays the same: `def _festival_summary(festival_slug: str, region_slug: str) -> str:`
- The returned string must be 40-80 words (the current summary field length target)
- All 480 combinations must be covered -- no KeyError on any valid festival × region pair

---

## Context: Why This Matters

These 480 pages are in sitemap-festivals.xml at priority 0.4. "Crawled -- Currently Not Indexed" status appears when Google's crawler sees >30-40% cross-page similarity in programmatic content. The summary field is the highest-weight field in the page's TF-IDF fingerprint (it appears in the meta_description and above-the-fold copy). Fixing it to <40% worst-pair is the single action that moves the module from "crawled, not indexed" risk to safe indexing territory.

Reference: `Codex_Deliveries/ECHO_PACE_PROCESS/PROCESS_1_COMBINATION_PAGE_ARCHITECTURE.md`
