# LSG-1 Commission Brief
> Thread: Lo Shu Grid Codex Thread  
> Module: Lo Shu Grid Calculator + Hub + Missing Number Pages  
> Pages: 1 hub + 1 calculator + 9 missing-number pages + 8 arrow pages = ~20 pages  
> Date: 2026-05-23  
> Status: READY TO BUILD -- decoded rules file available, all engines available

---

## Context

EverydayHoroscope (`everydayhoroscope.in`) is a live React 18 + FastAPI + MongoDB + Tailwind CSS platform. This commission adds the Lo Shu Grid module -- a Chinese numerology birth chart calculator, hub, and a set of SEO pages covering missing numbers and active arrows.

**Repo:** `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
**Stack:** React 18 · FastAPI · MongoDB · Tailwind CSS

**Decoded rules available (use these as the engine data source -- do not re-extract):**
```
/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/Numerology_Ch06_LoShuGrid_Rules.json
/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/Numerology_Ch06_LoShuGrid_DataTables.md
/Users/apple/Documents/Knowledge Engine_eBooks/DestinyNumerology_CC_Decode/Numerology_Ch06_LoShuGrid_Summary.md
```

The Rules JSON contains 17 rules (rule IDs `num-ch06-001` through `num-ch06-017`):
- 1 foundation rule (grid construction)
- 8 present-arrow rules (complete planes = strengths)
- 8 missing-arrow rules (empty planes = weaknesses)
- 2 Rajayoga indicators flagged (4,5,6 and 2,5,8)

All page content must be **original Codex writing** inspired by the decoded rule data -- not copied verbatim from the rules JSON text. Transform `full_text` fields into original SEO copy.

---

## Lo Shu Grid -- How It Works

The Lo Shu Grid is a 3×3 Chinese numerology birth chart. Each cell holds one of the nine digits (1-9):

```
4 | 9 | 2
---------
3 | 5 | 7
---------
8 | 1 | 6
```

To build a person's grid: collect all digits from (1) full date of birth, (2) Basic number (if double-digit), (3) Destiny number, (4) Kua number, (5) Full name number. A digit present in any input is marked in its cell; absent from all inputs = missing number.

**Numerology calculations (all computed in the backend -- not in React):**
- Basic number = single-digit reduction of day of birth (e.g. 29 → 2+9 = 11, also include 11 as double-digit)
- Destiny number = full DOB all digits summed to single digit
- Kua number = year of birth digits summed → add to 10 (for females) or subtract from 11 (for males) → reduce to single digit
- Full name number = sum of all name letter values (Pythagorean A=1...Z=8 system) → reduced to single digit

**Arrows (8 planes + 2 diagonals):**

| Arrow name | Numbers | Direction |
|---|---|---|
| Arrow of Intellect (Mind Plane) | 4, 9, 2 | Top horizontal row |
| Arrow of Willpower (Soul Plane) | 3, 5, 7 | Middle horizontal row |
| Arrow of Activity (Physical Plane) | 8, 1, 6 | Bottom horizontal row |
| Arrow of Thought (Thought Plane) | 4, 3, 8 | Left vertical column |
| Arrow of Will | 9, 5, 1 | Centre vertical column |
| Arrow of the Planner | 2, 7, 6 | Right vertical column |
| Arrow of Determination (Rajayoga 1) | 4, 5, 6 | Left-to-right diagonal |
| Arrow of Compassion (Rajayoga 2) | 2, 5, 8 | Right-to-left diagonal |

---

## Module Architecture

### URL Patterns

| URL | Purpose |
|---|---|
| `/lo-shu-grid/` | Hub page -- what is Lo Shu Grid, how it works, calculator entry |
| `/lo-shu-grid/calculator/` | Full interactive calculator -- DOB + name input → grid render + interpretation |
| `/lo-shu-grid/missing-{N}/` | Missing number pages (1 through 9) -- SEO pages for each missing digit |
| `/lo-shu-grid/arrow/{arrow-slug}/` | Arrow detail pages (8 pages) -- what each complete arrow means |

**Total pages:** 1 hub + 1 calculator + 9 missing-number + 8 arrow = **19 pages**

---

## Backend

### Router File
`backend/lo_shu_router.py`

Register in `backend/server.py` as: `app.include_router(lo_shu_router, prefix="/api")`

### Endpoints

```
POST /api/lo-shu/calculate            → full grid calculation + interpretation
GET  /api/lo-shu/missing/{n}          → SEO content for missing number N
GET  /api/lo-shu/arrow/{slug}         → SEO content for a named arrow
GET  /api/seo/sitemap/lo-shu-grid     → sitemap URLs list
```

### `POST /api/lo-shu/calculate`

**Input:**
```json
{
  "full_name": "Prateek Malhotra",
  "dob": "1990-05-15",
  "gender": "male"
}
```

**Processing (all in `lo_shu_router.py` -- pure numerology math, no vedic_calculator.py needed):**

```python
def lo_shu_calculate(full_name: str, dob: date, gender: str) -> dict:
    # 1. Extract all DOB digits
    dob_str = dob.strftime("%d%m%Y")  # e.g. "15051990"
    digits = [int(d) for d in dob_str if d != '0']  # 0 is not a Lo Shu cell

    # 2. Basic number (day)
    day = dob.day
    basic = reduce_to_single(day)
    if day > 9:
        digits.extend([int(d) for d in str(day)])  # include double-digit digits too

    # 3. Destiny number = sum all DOB digits repeatedly until single digit
    destiny = reduce_to_single(sum(int(d) for d in dob_str if d != '0'))

    # 4. Kua number
    year_sum = reduce_to_single(sum(int(d) for d in str(dob.year)))
    if gender == 'female':
        kua = reduce_to_single(year_sum + 10)
    else:
        kua = reduce_to_single(11 - year_sum)
    digits.append(kua)

    # 5. Name number (Pythagorean)
    name_number = reduce_to_single(sum(PYTHAGOREAN[c.upper()] for c in full_name if c.isalpha()))
    digits.append(name_number)

    # 6. Determine grid: which of 1-9 are present
    grid_present = set(d for d in digits if 1 <= d <= 9)
    grid_missing = set(range(1, 10)) - grid_present

    # 7. Determine active arrows (present) and missing arrows (absent)
    ARROWS = {
        'intellect': ([4, 9, 2], 'Arrow of Intellect'),
        'willpower':  ([3, 5, 7], 'Arrow of Willpower'),
        'activity':   ([8, 1, 6], 'Arrow of Activity'),
        'thought':    ([4, 3, 8], 'Arrow of Thought'),
        'will':       ([9, 5, 1], 'Arrow of Will'),
        'planner':    ([2, 7, 6], 'Arrow of the Planner'),
        'determination': ([4, 5, 6], 'Arrow of Determination -- Rajayoga'),
        'compassion':    ([2, 5, 8], 'Arrow of Compassion -- Rajayoga'),
    }
    active_arrows = [name for slug, (nums, name) in ARROWS.items() if all(n in grid_present for n in nums)]
    missing_arrows = [name for slug, (nums, name) in ARROWS.items() if all(n in grid_missing for n in nums)]

    return {
        "grid": {str(i): (i in grid_present) for i in range(1, 10)},
        "missing_numbers": sorted(list(grid_missing)),
        "present_numbers": sorted(list(grid_present)),
        "active_arrows": active_arrows,
        "missing_arrows": missing_arrows,
        "basic_number": basic,
        "destiny_number": destiny,
        "kua_number": kua,
        "name_number": name_number,
        "interpretations": {
            "active_arrows": [ARROW_INTERPRETATIONS[a] for a in active_arrows],
            "missing_arrows": [MISSING_INTERPRETATIONS[m] for m in grid_missing],
        }
    }
```

`ARROW_INTERPRETATIONS` and `MISSING_INTERPRETATIONS` are dictionaries hardcoded from the decoded rules JSON -- summaries of the rule `full_text` fields, rewritten as original Codex content. Do NOT copy `full_text` verbatim.

**Output:**
```json
{
  "grid": {"1": true, "2": false, "3": true, "4": false, "5": true, "6": true, "7": false, "8": true, "9": true},
  "missing_numbers": [2, 4, 7],
  "present_numbers": [1, 3, 5, 6, 8, 9],
  "active_arrows": ["Arrow of Will", "Arrow of Activity"],
  "missing_arrows": ["Arrow of Intellect"],
  "basic_number": 6,
  "destiny_number": 3,
  "kua_number": 4,
  "name_number": 7,
  "interpretations": {
    "active_arrows": [
      { "name": "Arrow of Will", "effect": "...", "strength_band": "high" }
    ],
    "missing_arrows": [
      { "number": 2, "effect": "...", "remedy": "..." }
    ]
  }
}
```

### MongoDB Collections

**Collection: `lo_shu_missing_numbers`** -- 9 documents (one per missing digit)

```json
{
  "number": 2,
  "slug": "missing-2",
  "title": "Missing Number 2 in Lo Shu Grid -- What It Means & How to Balance It",
  "ruling_planet": "Moon",
  "ruling_day": "Monday",
  "effect_summary": "1-sentence punchy impact summary",
  "traits_affected": ["emotional sensitivity", "intuition", "cooperation", "patience"],
  "life_areas_impacted": ["relationships", "emotional wellbeing", "teamwork"],
  "remedies": ["Wear white or silver on Mondays", "...", "..."],
  "affirmation": "I am emotionally balanced and open...",
  "faq": [
    { "q": "What does missing number 2 mean in Lo Shu Grid?", "a": "..." },
    { "q": "Is missing 2 bad in numerology?", "a": "..." },
    { "q": "How do I correct missing number 2?", "a": "..." },
    { "q": "Which planet rules number 2 in Lo Shu Grid?", "a": "..." },
    { "q": "What happens when number 2 is missing?", "a": "..." }
  ],
  "related_missing": [1, 7],
  "meta_title": "Missing Number 2 in Lo Shu Grid -- Meaning, Effects & Remedies | EverydayHoroscope",
  "meta_description": "Number 2 missing from your Lo Shu Grid? Discover what it means, which life areas are affected, and simple remedies to balance this energy."
}
```

**Number-Planet reference (use for all 9 pages):**

| Number | Ruling Planet | Ruling Day |
|---|---|---|
| 1 | Sun | Sunday |
| 2 | Moon | Monday |
| 3 | Jupiter | Thursday |
| 4 | Rahu | Saturday |
| 5 | Mercury | Wednesday |
| 6 | Venus | Friday |
| 7 | Ketu | Tuesday |
| 8 | Saturn | Saturday |
| 9 | Mars | Tuesday |

**Collection: `lo_shu_arrows`** -- 8 documents (one per arrow)
Seed from decoded rules JSON rule IDs `num-ch06-002` through `num-ch06-009` (present arrows) -- rewrite `full_text` as original content.

### Seed Scripts
- `backend/scripts/seed_lo_shu.py` -- seeds both collections (9 missing + 8 arrow documents)

---

## Frontend

### Hub Page
**File:** `frontend/src/pages/lo_shu_grid/LoShuHubPage.jsx`

**Page content:**
- H1: `Lo Shu Grid -- Chinese Numerology Birth Chart Explained`
- Intro: What is the Lo Shu Grid? (3-4 sentences, original)
- **Visual grid explainer:** 3×3 grid display (static) with number labels and cell descriptions
- **Calculator CTA:** Gold GlassCard -- "Generate Your Lo Shu Grid" → `/lo-shu-grid/calculator/`
- **Missing numbers section:** "What does a missing number mean?" -- 1-paragraph intro + 9 pills linking to missing number pages
- **Active arrows section:** "What are Lo Shu Arrows?" -- 1-para intro + 8 arrow pills
- **FAQ accordion:** 5 questions (What is Lo Shu Grid? How is it calculated? What are missing numbers? What are arrows? Is Lo Shu accurate?)
- JSON-LD: `FAQPage` + `BreadcrumbList`
- SEO: Title: `Lo Shu Grid -- Chinese Numerology Calculator & Missing Numbers | EverydayHoroscope` · Description: `Discover your Lo Shu Grid birth chart. Calculate your missing numbers, active arrows, and what they reveal about your personality and life path.`

### Calculator Page
**File:** `frontend/src/pages/lo_shu_grid/LoShuCalculatorPage.jsx`

**Page content:**
- H1: `Lo Shu Grid Calculator -- Your Personal Numerology Birth Chart`
- 1-sentence intro
- **Form:**
  - Full name (text input)
  - Date of birth (date picker)
  - Gender (Male / Female -- required for Kua number)
  - Submit: "Generate My Grid"
- **Results panel (after API call):**
  - **Visual grid:** 3×3 interactive grid -- present numbers shown in gold, missing numbers shown as empty/grey outline. Cells are clickable → scroll to interpretation.
  - **Number strip:** Basic / Destiny / Kua / Name number displayed as 4 gold chips
  - **Active Arrows section:** Each active arrow shown as a GlassCard with name + effect summary
  - **Missing Numbers section:** Each missing number shown as a GlassCard with effect + remedy + "Learn more" link to missing number page
  - **Missing Arrows section:** Shown if any
  - **Rajayoga indicator:** If 4,5,6 or 2,5,8 arrows both active → show special emerald "Rajayoga Present" banner
- JSON-LD: `FAQPage`

### Missing Number Page
**File:** `frontend/src/pages/lo_shu_grid/LoShuMissingNumberPage.jsx`

**Page content:**
- H1: `Missing Number {N} in Lo Shu Grid -- What It Means & How to Balance It`
- **Planet badge:** "Ruled by {Planet} · {Day}"
- **Effect summary:** 2-3 sentences -- what this missing number means
- **Traits affected:** 4-5 bullet points
- **Life areas impacted:** Pills
- **Remedies:** 3-4 actionable remedies (colours, days, mantras, habits)
- **Affirmation block:** Gold-bordered italic Playfair
- **Do you have this missing number?** CTA → `/lo-shu-grid/calculator/`
- **FAQ accordion:** 5 questions
- **Related missing numbers:** 2-3 related pages
- JSON-LD: `FAQPage` + `Article`

### Arrow Detail Page
**File:** `frontend/src/pages/lo_shu_grid/LoShuArrowPage.jsx`

**Page content:**
- H1: `{Arrow Name} -- What This Lo Shu Arrow Reveals About You`
- Numbers in this arrow (3 cells shown visually)
- Effect when present: 3-4 sentences
- Effect when missing: 2-3 sentences
- Real-life traits: 4-5 bullets
- Rajayoga badge if applicable (4,5,6 or 2,5,8)
- CTA → calculator
- JSON-LD: `Article`

---

## SEO Metadata Formulas

### Missing Number Pages
- **Title:** `Missing Number {N} in Lo Shu Grid -- {Planet} Energy & Remedies | EverydayHoroscope`
- **Description:** `Number {N} missing from your Lo Shu Grid affects [key trait]. Discover the meaning, life areas impacted, and Vedic remedies to restore balance.`

### Arrow Pages
- **Title:** `{Arrow Name} in Lo Shu Grid -- {1-word theme} | EverydayHoroscope`
- **Description:** `The {Arrow Name} in Lo Shu Grid reveals [effect]. Discover what it means when numbers {N},{N},{N} are all present in your birth chart.`

---

## Routes (App.js additions)

```jsx
<Route path="/lo-shu-grid" element={<LoShuHubPage />} />
<Route path="/lo-shu-grid/calculator" element={<LoShuCalculatorPage />} />
<Route path="/lo-shu-grid/missing-:number" element={<LoShuMissingNumberPage />} />
<Route path="/lo-shu-grid/arrow/:slug" element={<LoShuArrowPage />} />
```

All routes: public, no auth gate.

---

## Sitemap

Add to `backend/seo_router.py`:
```python
GET /api/seo/sitemap/lo-shu-grid   # 19 URLs
```

Add to `frontend/public/sitemap-index.xml`.

---

## Technical Requirements

- New React pages in `frontend/src/pages/lo_shu_grid/` (new subdirectory)
- New FastAPI router: `backend/lo_shu_router.py`
- Register router in `backend/server.py`
- New routes in `frontend/src/App.js` (public, no auth gate)
- Sitemap endpoint added to `backend/seo_router.py`
- Cache headers in `frontend/vercel.json` (s-maxage=86400) for `/lo-shu-grid/*`
- MongoDB seed scripts: `backend/scripts/seed_lo_shu.py`
- `SEO` component from `frontend/src/components/SEO.jsx` on every page
- **No `vedic_calculator.py` needed** -- Lo Shu is pure date/name arithmetic, self-contained in `lo_shu_router.py`

**Tailwind / theme:** GlassCard pattern (`rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`). Gold accent `#c5a059`. No new dependencies.

**Build verification:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` -- must pass clean.

---

## Acceptance Checklist

- [ ] Hub page renders at `/lo-shu-grid/`
- [ ] Calculator page renders at `/lo-shu-grid/calculator/`
- [ ] Calculator POST correctly computes grid for a test DOB + name
- [ ] 9 missing number pages render at `/lo-shu-grid/missing-{N}/`
- [ ] 8 arrow pages render at `/lo-shu-grid/arrow/{slug}/`
- [ ] Rajayoga indicator appears when 4,5,6 or 2,5,8 arrows both active
- [ ] Visual 3×3 grid renders in calculator results (present = gold, missing = grey)
- [ ] Sitemap endpoint returns 19 URLs
- [ ] Routes wired in App.js -- all pages HTTP 200
- [ ] Vercel cache headers applied to `/lo-shu-grid/*`
- [ ] MongoDB seed script seeds all 17 content documents
- [ ] Build clean -- zero errors
- [ ] JSON-LD on all page types
- [ ] SEO meta applied on all pages
- [ ] All content is original Codex writing -- not copied from decoded rules JSON verbatim
