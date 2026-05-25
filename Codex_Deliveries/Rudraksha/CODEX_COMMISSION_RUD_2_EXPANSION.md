# RUD-2 Commission Brief -- Rudraksha Expansion (Textbook-Decoded Pages)
> Thread: Rudraksha Codex Thread (same thread as RUD-1)
> Commission ID: RUD-2
> Date: 2026-05-26
> Status: READY TO ISSUE
> Prerequisite: RUD-1 integrated ✅

---

## Objective

RUD-1 built the structural foundation (21 mukhi pages, hub, calculator).

**RUD-2 adds three new page categories decoded from the Rudraksha source book:**

1. **Planet-Rudraksha pages** -- "Best Rudraksha for [Planet]" (9 pages)
2. **Problem-Area pages** -- "Rudraksha for [Specific Problem]" (20 pages)
3. **Sign-Rudraksha pages** -- "Best Rudraksha for [Rashi/Sign]" (12 pages)

**Total new pages: 41**  
**New sitemap total: 23 (RUD-1) + 41 (RUD-2) = 64 pages**

---

## Source Material

All content must be original Codex writing. Use these as decoded reference data -- no direct quotes.

```
Primary textbook:
/Users/apple/Documents/Knowledge Engine_eBooks/Rudraksha/Rudraksha-Revealed-1-Mukhi-21-Mukhi.pdf_compressed-1.pdf

Supporting reference:
/Users/apple/Documents/Knowledge Engine_eBooks/Text Books/tantra-mantra-yantra.pdf
```

---

## Page Category 1 -- Planet-Rudraksha Pages (9 pages)

### URL Pattern
```
/rudraksha/for/planet/{planet-slug}
```

### Planets & Primary Mukhis (from Vedic tradition)
| Planet | Slug | Primary Mukhi | Secondary Mukhi |
|---|---|---|---|
| Sun | `sun` | 1 Mukhi | 12 Mukhi |
| Moon | `moon` | 2 Mukhi | -- |
| Mars | `mars` | 3 Mukhi | -- |
| Mercury | `mercury` | 4 Mukhi | -- |
| Jupiter | `jupiter` | 5 Mukhi | -- |
| Venus | `venus` | 6 Mukhi | 13 Mukhi |
| Saturn | `saturn` | 7 Mukhi | 14 Mukhi |
| Rahu | `rahu` | 8 Mukhi | 18 Mukhi |
| Ketu | `ketu` | 9 Mukhi | -- |

### Page Content Template
- H1: `Rudraksha for [Planet] -- Best Mukhi & How to Wear It`
- Intro: Planet's role in Vedic astrology, why Rudraksha can strengthen it (2-3 sentences)
- **Primary Mukhi card** (large): Which mukhi, ruling deity, benefits, wearing rules
- **Secondary Mukhi card** (if applicable): Alternative or supplementary
- **Wearing instructions**: Metal (silver/gold/copper), thread colour, mantra, day to energise, finger
- **Who needs this**: Signs of a weakened planet that this Rudraksha addresses
- **Contraindications**: Who should NOT wear without consultation
- **FAQ accordion**: 5 Q&As
- CTA → `/rudraksha/calculator`
- Meta title: `Rudraksha for [Planet] -- Best Mukhi Beads | EverydayHoroscope`

---

## Page Category 2 -- Problem-Area Pages (20 pages)

Decoded from the Rudraksha textbook's section on ailments and life challenges addressed by specific mukhis.

### URL Pattern
```
/rudraksha/for/problem/{problem-slug}
```

### Problem Areas & Slugs
| Problem | Slug | Key Mukhis |
|---|---|---|
| Depression / Low Mood | `depression` | 1, 7 Mukhi |
| Debt / Financial Stress | `financial-stress` | 7, 8 Mukhi |
| Career Block | `career-block` | 6, 11 Mukhi |
| Relationship Problems | `relationship-problems` | 2, 14 Mukhi |
| Fear and Anxiety | `fear-anxiety` | 5, 9 Mukhi |
| Anger Management | `anger` | 3, 12 Mukhi |
| Low Immunity / Frequent Illness | `low-immunity` | 5, 6 Mukhi |
| Blood Pressure / Heart Issues | `heart-blood-pressure` | 12 Mukhi |
| Memory and Concentration | `memory-concentration` | 4 Mukhi |
| Negative Energy / Black Magic | `negative-energy` | 8, 10 Mukhi |
| Evil Eye Protection | `evil-eye` | 10, 11 Mukhi |
| Legal / Court Case Issues | `legal-issues` | 14, 17 Mukhi |
| Marriage Delays | `marriage-delay` | 2, 13 Mukhi |
| Childlessness / Fertility | `fertility` | 9 Mukhi |
| Addiction | `addiction` | 1, 3 Mukhi |
| Insomnia | `insomnia` | 2, 5 Mukhi |
| Digestive / Stomach Issues | `digestive-issues` | 3 Mukhi |
| Skin Problems | `skin-issues` | 4 Mukhi |
| Spiritual Growth | `spiritual-growth` | 1, 21 Mukhi |
| Business Success | `business-success` | 7, 8, 11 Mukhi |

### Page Content Template
- H1: `Rudraksha for [Problem] -- Which Mukhi Bead Helps & How to Use It`
- Intro: Why Rudraksha addresses this problem energetically (2-3 sentences)
- **Primary recommendation card** (large): Mukhi number, ruling deity, why it works for this problem
- **Supporting mukhis** (2-3 smaller cards)
- **Combination suggestion**: Can these mukhis be worn together? If so, how?
- **Wearing method**: Thread, metal, mantra, activation ritual
- **Lifestyle tips**: 3 complementary practices
- **FAQ accordion**: 5 Q&As
- CTA → `/rudraksha/calculator`
- Meta title: `Rudraksha for [Problem] -- Best Mukhi Beads | EverydayHoroscope`

---

## Page Category 3 -- Sign-Rudraksha Pages (12 pages)

### URL Pattern
```
/rudraksha/for/sign/{sign-slug}
```

Signs: aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces

### Page Content Template
- H1: `Best Rudraksha for [Sign] -- Mukhi Beads for [Sign] Energy`
- Intro: Sign's nature, ruling planet, typical challenges (2-3 sentences)
- **Primary Rudraksha** (from sign's ruling planet mapping): Large card with full details
- **Secondary Rudraksha** for the sign's shadow qualities
- **Rudraksha to avoid**: Any mukhis that conflict with sign energy
- **Wearing guidance**: Best day, best metal, activation mantra
- **FAQ accordion**: 4 Q&As
- CTA → `/rudraksha/calculator`
- Meta title: `Best Rudraksha for [Sign] -- Mukhi Beads | EverydayHoroscope`

---

## Technical Requirements

### Backend additions to `rudraksha_content.py`

Add three new data dictionaries:
```python
PLANET_RUDRAKSHA_DATA = { "sun": {...}, "moon": {...}, ... }   # 9 planets
PROBLEM_RUDRAKSHA_DATA = { "depression": {...}, ... }           # 20 problems
SIGN_RUDRAKSHA_DATA = { "aries": {...}, ... }                   # 12 signs
```

### Backend additions to `rudraksha_router.py`

```
GET /api/rudraksha/planet/{planet_slug}    → planet rudraksha page data
GET /api/rudraksha/sign/{sign_slug}        → sign rudraksha page data
GET /api/rudraksha/problem/{problem_slug}  → problem rudraksha page data
```

### Sitemap update in `seo_router.py`

Update the existing `/api/seo/sitemap/rudraksha` endpoint. Current: 23 URLs. New: 64 URLs.

New URL patterns to add:
```
/rudraksha/for/planet/{slug}   × 9
/rudraksha/for/sign/{slug}     × 12
/rudraksha/for/problem/{slug}  × 20
```

### New frontend pages

```
frontend/src/pages/rudraksha/RudrakshaPlanetPage.jsx   # /rudraksha/for/planet/:planet
frontend/src/pages/rudraksha/RudrakshaSignPage.jsx     # /rudraksha/for/sign/:sign
frontend/src/pages/rudraksha/RudrakshaProblemPage.jsx  # /rudraksha/for/problem/:problem
```

### App.js route additions

```jsx
<Route path="/rudraksha/for/planet/:planet" element={<RudrakshaPlanetPage />} />
<Route path="/rudraksha/for/sign/:sign" element={<RudrakshaSignPage />} />
<Route path="/rudraksha/for/problem/:problem" element={<RudrakshaProblemPage />} />
```

Add BEFORE the existing `/rudraksha/:mukhi` catch-all route to avoid conflicts.

### Seed script update

Update `backend/scripts/seed_rudraksha.py` to seed planet, sign, and problem collections.

---

## Acceptance Checklist

- [ ] 9 planet pages render at `/rudraksha/for/planet/{slug}` with primary mukhi, wearing instructions, contraindications
- [ ] 20 problem pages render at `/rudraksha/for/problem/{slug}` with primary + supporting mukhis, combination guidance
- [ ] 12 sign pages render at `/rudraksha/for/sign/{slug}` with ruling planet mukhi + shadow mukhi
- [ ] All pages include FAQ accordion, CTA to calculator, SEO component, JSON-LD
- [ ] Sitemap returns 64 URLs
- [ ] No route conflict with existing `/rudraksha/:mukhi` -- planet/sign/problem use nested `/for/` prefix
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`
