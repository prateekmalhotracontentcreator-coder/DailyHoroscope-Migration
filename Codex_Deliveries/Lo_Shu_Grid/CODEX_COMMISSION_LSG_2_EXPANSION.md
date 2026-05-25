# LSG-2 Commission Brief -- Lo Shu Grid Expansion (Textbook-Decoded Pages)
> Thread: Lo Shu Grid Codex Thread (same thread as LSG-1)
> Commission ID: LSG-2
> Date: 2026-05-26
> Status: READY TO ISSUE
> Prerequisite: LSG-1 integrated ✅

---

## Objective

LSG-1 built the structural foundation (hub, calculator, 9 missing number pages, 8 arrow pages).

**LSG-2 adds three new page categories decoded from Lo Shu Grid textbooks:**

1. **Number Deep-Dive pages** -- "Lo Shu Number [1-9]: Meaning, Strengths, Challenges" (9 pages)
2. **Problem-Area pages** -- "Lo Shu Grid for [Problem]" (20 pages -- remedies and focus areas)
3. **Personal Year pages** -- "Lo Shu Personal Year [1-9]: What to Expect" (9 pages)

**Total new pages: 38**  
**New sitemap total: ~20 (LSG-1) + 38 (LSG-2) = ~58 pages**

---

## Source Material

All content must be original Codex writing. Use these decoded sources as reference -- no direct quotes.

```
Primary sources:
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Lo Shu Grid/loshu-grid-1.docx
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Lo Shu Grid/loshu.docx
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Lo Shu Grid/pdfcoffee.com_10-second-lo-shu-pdf-free.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Lo Shu Grid/Lo Shu Grid Missing Numbers and their remedies - Numerology By Nehaa.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Lo Shu Grid/Remedies for Missing Numbers in Numerology _ Lo Shu Grid.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Lo Shu Grid/Missing Number in Numerology_ Understanding Its Impact and How to Address the Gaps in Your Life.pdf
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Lo Shu Grid/sample-english-loshu-prediction-keero-gold.docx

Supporting:
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/Numerology/Numerology-With Tantra, Ayurveda, and Astrology.pdf
```

---

## Page Category 1 -- Number Deep-Dive Pages (9 pages)

### URL Pattern
```
/lo-shu-grid/number/{1-9}
```

These are different from the existing Missing Number pages (`/lo-shu-grid/missing-{N}`). The deep-dive pages explore what it means when a number IS present in the grid -- its positive expression, overexpression (too many occurrences), and balancing guidance.

### Page Content Template
- H1: `Lo Shu Number [N] -- Meaning, Energy & Influence in Your Grid`
- Intro: The number's core archetype in Lo Shu numerology (2-3 sentences)
- **When Number [N] is present** (1 occurrence): Positive traits and life areas strengthened
- **When Number [N] repeats** (2-3 occurrences): Overexpression -- what gets amplified, potential shadow
- **When Number [N] is missing**: Brief cross-link to `/lo-shu-grid/missing-{N}` for full details
- **Planet / Element / Direction**: The classical associations (planet, element, compass direction, colour)
- **Balancing tips**: 3 practical remedies or lifestyle adjustments
- **Famous personalities** (optional): 1-2 notable people with this strong number
- **FAQ accordion**: 4 Q&As
- CTA → `/lo-shu-grid/calculator`
- Meta title: `Lo Shu Number [N] -- Meaning & Grid Influence | EverydayHoroscope`

---

## Page Category 2 -- Problem-Area Pages (20 pages)

Decoded from Lo Shu remedies textbooks. Each page maps a life challenge to Lo Shu grid analysis and remedies.

### URL Pattern
```
/lo-shu-grid/for/{problem-slug}
```

### Problem Areas & Slugs
| Problem | Slug |
|---|---|
| Career Growth Block | `career-growth` |
| Financial Instability | `financial-instability` |
| Relationship Difficulties | `relationship-difficulties` |
| Marriage Delays | `marriage-delays` |
| Health Issues | `health-issues` |
| Lack of Confidence | `lack-of-confidence` |
| Communication Problems | `communication-problems` |
| Chronic Stress / Anxiety | `stress-anxiety` |
| Poor Decision Making | `poor-decisions` |
| Loneliness / Social Isolation | `loneliness` |
| Academic Struggles | `academic-struggles` |
| Business Partnership Problems | `business-partnerships` |
| Family Conflicts | `family-conflicts` |
| Property / Home Issues | `property-issues` |
| Travel and Relocation | `travel-relocation` |
| Lack of Creativity | `creativity-block` |
| Spiritual Disconnection | `spiritual-disconnection` |
| Legal Problems | `legal-problems` |
| Childbirth / Fertility | `fertility` |
| Leadership Challenges | `leadership` |

### Page Content Template
- H1: `Lo Shu Grid for [Problem] -- What Your Grid Reveals & How to Fix It`
- Intro: How Lo Shu grid patterns relate to this problem energetically (2-3 sentences)
- **Grid diagnostic**: Which numbers being missing or over-represented typically correlate with this problem
- **Missing number fix**: Which missing number to address first, and the specific remedy
- **Arrow patterns** that signal this problem (with cross-links to relevant arrow pages)
- **Remedies section**: 4-5 specific Lo Shu remedies (directional, colour, element, activity)
- **Affirmation**: 1 short affirmation aligned with the corrective number
- **FAQ accordion**: 4 Q&As
- CTA → `/lo-shu-grid/calculator`
- Meta title: `Lo Shu Grid for [Problem] -- Analysis & Remedies | EverydayHoroscope`

---

## Page Category 3 -- Personal Year Pages (9 pages)

### URL Pattern
```
/lo-shu-grid/personal-year/{1-9}
```

Personal Year in Lo Shu is calculated from birth date + current year. These pages explain what each Personal Year number means for life themes, opportunities, and cautions.

### Page Content Template
- H1: `Lo Shu Personal Year [N] -- What This Year Means for You`
- Intro: How Personal Year is calculated, what Personal Year [N] represents broadly (2-3 sentences)
- **Year theme**: The overarching energy and focus of this Personal Year
- **Opportunities**: 4-5 areas of life that are favoured
- **Cautions**: 2-3 areas to be careful about
- **Monthly breakdown**: Brief note on how the energy shifts each month (light touch, not full 12-month breakdown)
- **Remedies and amplifiers**: 3 practices to maximise this Personal Year's energy
- **Who is in Personal Year [N] now**: How to calculate it (simple formula shown)
- **CTA**: "Calculate your Lo Shu Grid to see your full personal year analysis" → `/lo-shu-grid/calculator`
- **FAQ accordion**: 4 Q&As
- Meta title: `Lo Shu Personal Year [N] -- What to Expect This Year | EverydayHoroscope`

---

## Technical Requirements

### Backend additions to `lo_shu_router.py`

Add three new data dictionaries:
```python
NUMBER_DEEP_DIVE_DATA = { 1: {...}, 2: {...}, ... 9: {...} }
PROBLEM_LOSHU_DATA = { "career-growth": {...}, ... }
PERSONAL_YEAR_DATA = { 1: {...}, ... 9: {...} }
```

New endpoints:
```
GET /api/lo-shu/number/{n}            → number deep-dive page data (n = 1-9)
GET /api/lo-shu/problem/{slug}        → problem-area page data
GET /api/lo-shu/personal-year/{n}    → personal year page data (n = 1-9)
```

### Sitemap update in `seo_router.py`

Update `/api/seo/sitemap/lo-shu-grid` to include all new URLs.

New patterns to add:
```
/lo-shu-grid/number/{1-9}          × 9
/lo-shu-grid/for/{problem-slug}    × 20
/lo-shu-grid/personal-year/{1-9}  × 9
```

### New frontend pages

```
frontend/src/pages/lo_shu_grid/LoShuNumberPage.jsx        # /lo-shu-grid/number/:n
frontend/src/pages/lo_shu_grid/LoShuProblemPage.jsx       # /lo-shu-grid/for/:problem
frontend/src/pages/lo_shu_grid/LoShuPersonalYearPage.jsx  # /lo-shu-grid/personal-year/:n
```

### App.js route additions

```jsx
<Route path="/lo-shu-grid/number/:n" element={<LoShuNumberPage />} />
<Route path="/lo-shu-grid/for/:problem" element={<LoShuProblemPage />} />
<Route path="/lo-shu-grid/personal-year/:n" element={<LoShuPersonalYearPage />} />
```

Add BEFORE any catch-all routes.

### Seed script update

Update `backend/scripts/seed_lo_shu.py` to seed number deep-dive, problem, and personal year collections.

---

## Acceptance Checklist

- [ ] 9 number pages render at `/lo-shu-grid/number/{1-9}` with presence/overexpression/missing cross-link + remedies
- [ ] 20 problem pages render at `/lo-shu-grid/for/{slug}` with grid diagnostic + missing number fix + arrow patterns + remedies
- [ ] 9 personal year pages render at `/lo-shu-grid/personal-year/{1-9}` with theme, opportunities, cautions, monthly note
- [ ] All pages include FAQ accordion, CTA to calculator, SEO component, JSON-LD
- [ ] Sitemap returns ~58 URLs (existing ~20 + 38 new)
- [ ] No route conflict with existing missing-number or arrow pages
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
