# Commission Brief: SEO-C3 -- Compatibility by Name

**Commission ID:** SEO-C3  
**Track:** C -- Codex Feature Builds  
**Priority:** Tier 2 -- Phase 4  
**Date:** 2026-05-20  
**Status:** READY TO ISSUE  

---

## What to Build

A public name compatibility calculator -- two names in, compatibility score out.

| Route | What it does |
|---|---|
| `/compatibility/name` | Enter two names → Chaldean numerology score + compatibility reading |

High mass-appeal, shareable result. Upsells to full Relationship Numerology Report.

---

## Files to Create

### Frontend
- `frontend/src/pages/calculators/NameCompatibilityPage.jsx`

### Backend
Add one lightweight endpoint to `backend/numerology_router.py` (details below). No new file.

---

## Route Wiring (App.js)

```jsx
import { NameCompatibilityPage } from './pages/calculators/NameCompatibilityPage';

<Route path="/compatibility/name" element={<NameCompatibilityPage />} />
```

---

## Backend

### New endpoint -- add to `numerology_router.py`

```
POST /api/numerology/name-compatibility
Body: { "name1": "Priya", "name2": "Arjun" }
Returns: { "name1": "Priya", "name2": "Arjun", "number1": 6, "number2": 9, "score": 78, "band": "high", "summary": "..." }
```

### Calculation logic (use existing `CHALDEAN_MAP` at line 37)

```python
def name_to_chaldean_number(name: str) -> int:
    """Reduce a name to its Chaldean compound number, then to single digit."""
    cleaned = ''.join(c.upper() for c in name if c.isalpha())
    total = sum(CHALDEAN_MAP.get(c, 0) for c in cleaned)
    # Reduce to single digit (keep 11, 22 as master numbers)
    while total > 9 and total not in (11, 22):
        total = sum(int(d) for d in str(total))
    return total

@router.post("/numerology/name-compatibility")
async def name_compatibility(data: dict):
    name1, name2 = data.get("name1","").strip(), data.get("name2","").strip()
    if not name1 or not name2:
        raise HTTPException(status_code=400, detail="Both names required")
    n1 = name_to_chaldean_number(name1)
    n2 = name_to_chaldean_number(name2)
    score, band, summary = _score_name_pair(n1, n2)
    return {"name1": name1, "name2": name2, "number1": n1, "number2": n2,
            "score": score, "band": band, "summary": summary}
```

### `_score_name_pair(n1, n2)` -- compatibility matrix (hardcode in router)

```python
COMPAT_MATRIX = {
    # (number1, number2): (score, band)
    # Harmonious pairs: 1+5, 2+4, 2+8, 3+6, 3+9, 4+8, 5+6, 6+9
    # Challenging: 1+4, 2+3, 4+5, 5+7, 6+8
    # Neutral: everything else
}
# Use symmetric lookup: always sort pair so smaller is first
# Score range: 40-95. Band: "high" (80+), "good" (65-79), "moderate" (50-64), "challenging" (<50)
```

Use a lookup table for the 36 number-pair combinations (1-9 × 1-9). Hardcode scores -- no LLM needed. The summary is a 2-sentence string from a `SUMMARY_MAP` keyed on `(n1, n2)`.

**⚠️ No LLM call for this endpoint.** Pure numerology calculation. Fast, free, unlimited.

---

## UI Layout

```
[Page header: "Name Compatibility Calculator"]
[Subtitle: "Discover your numerological connection -- powered by Chaldean numerology"]

[Input card -- GlassCard]
  ├── Name 1 text input (placeholder: "Your name")
  ├── Name 2 text input (placeholder: "Their name")
  └── [Calculate Compatibility] button (gold)

[Result card -- appears after submit]
  ├── Name 1 → Chaldean number (e.g. "Priya = 6")
  ├── Name 2 → Chaldean number (e.g. "Arjun = 9")
  ├── Large score display: "78% Compatible"
  ├── Band badge: ✨ High Compatibility / ✅ Good / 🔶 Moderate / ⚠️ Challenging
  ├── 2-sentence summary (from backend)
  ├── [Share this result] -- copy link button
  └── [Try different names] -- reset form

[What is Chaldean numerology? -- info card]
  └── 3 sentences explaining the system

[Upsell CTA]
  ├── "Get your full Relationship Numerology Report"
  ├── "Deep analysis of Life Path compatibility, Soul Urge harmony, and communication patterns"
  └── [Unlock Relationship Report] → /numerology (pre-select relationship_compatibility report)

[Related tools]
  ├── "Rashi Calculator →" → /rashi-calculator
  └── "Nakshatra Calculator →" → /nakshatra-calculator
```

---

## Shareability (important for virality)

- Result URL should encode the two names: `/compatibility/name?n1=Priya&n2=Arjun`
- On page load, if URL params present → auto-calculate and show result
- Share button copies the result URL to clipboard
- No share card needed (keep it simple -- link sharing is enough for V1)

---

## SEO Requirements

- **Title:** `Name Compatibility Calculator -- Chaldean Numerology | EverydayHoroscope`
- **Description:** `Find out how compatible two names are using Chaldean numerology. Enter any two names to get your compatibility score, number analysis, and relationship insight.`
- **JSON-LD:** `@type: "WebApplication"`, `applicationCategory: "AstrologyApplication"`
- **FAQ schema:**
  - "How is name compatibility calculated?" → Chaldean system
  - "Is name compatibility accurate?" → guide answer
  - "What does a high compatibility score mean?"

---

## Visual Spec

- Input fields: `border border-gold/30 bg-gold/[0.02] rounded-lg` focus ring in gold
- Result score: large `text-5xl font-cinzel text-gold`
- Band badge: colour-coded pill (`emerald` for high, `sky` for good, `amber` for moderate, `red` for challenging)
- GlassCard for both input and result sections
- No custom CSS -- Tailwind only

---

## ⚠️ Critical Notes

1. **No LLM** -- all calculation is pure Python, no API calls, instant response
2. **Existing `CHALDEAN_MAP`** -- in `numerology_router.py` line 37. Use it directly, do not redeclare
3. **`_score_compatibility` function already exists** in the router -- study its signature before adding `_score_name_pair`; keep consistent style
4. **URL params for sharing** -- encode names in query string so results are shareable via link
5. **Smart quote fix** -- run on `NameCompatibilityPage.jsx` before handover
6. **Lazy load** -- component can be lazy-loaded

---

## Acceptance Criteria

- [ ] `/compatibility/name` loads without 404
- [ ] Form submits and returns result within 1 second (no LLM)
- [ ] Chaldean number shown for each name
- [ ] Score and band displayed correctly
- [ ] URL encodes names -- `/compatibility/name?n1=X&n2=Y` auto-calculates on load
- [ ] Share button copies correct URL
- [ ] Upsell CTA links to `/numerology`
- [ ] FAQ schema present
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
