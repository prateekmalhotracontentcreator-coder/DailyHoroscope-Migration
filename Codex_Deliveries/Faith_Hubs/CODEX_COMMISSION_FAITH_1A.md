# CODEX COMMISSION: FAITH-1A
## Faith SEO Module -- Quality Audit, Enrichment & ECHO//PACE Compliance

> Commission ID: FAITH-1A
> Date: 2026-05-27
> Status: READY TO ISSUE
> Prerequisite: FAITH-1 delivered and integrated ✅
> Thread: Faith SEO Codex Thread (same thread as FAITH-1)

---

## Context -- What Has Already Been Built

The Faith SEO module is **fully built and integrated** into the EverydayHoroscope live app. Temple Team has reviewed the delivery and confirmed the following phases are complete:

| Phase | Description | Pages | Status |
|---|---|---|---|
| Phase 1A | Transit × Scripture (Transit hub + 12 zodiac daily sign pages) | ~156 | ✅ Integrated |
| Phase 1B | Daily Evergreen (Daily Scripture hub + 12 daily sign pages) | ~144 | ✅ Integrated |
| Phase 2 | Gita × Situation (700 verses × 15 life situations) | 10,500 | ✅ Integrated |
| Phase 3 | Bible × Transition (120 topics × 50 transitions) | 6,000 | ✅ Integrated |
| Growth A | Collections hub + Growth panel + Faith signup endpoint | -- | ✅ Integrated |

**Total: 16,800 pages** (across 5 phases).

**Live routes (all integrated to App.js and server.py):**
```
/faith                          → FaithHubPage
/faith/gita                     → FaithGitaHubPage
/faith/gita/:chapter            → FaithGitaChapterPage
/faith/gita/:chapter/:verse/:situation  → GitaVersePage
/faith/bible                    → FaithBibleHubPage
/faith/bible/:topic             → FaithBibleTopicPage
/faith/bible/:topic/:transition → BibleTopicPage
/faith/transit                  → FaithTransitHubPage
/faith/transit/:planet/:sign    → TransitScripturePage
/faith/daily                    → FaithDailyHubPage
/faith/daily/:sign              → FaithDailySignPage
/faith/daily/:sign/:date        → DailyScripturePage
/faith/collections              → FaithCollectionsHubPage
/faith/collections/:pathway     → FaithCollectionPage
```

**Backend files delivered:**
- `backend/faith_seo_router.py` (271 lines)
- `backend/faith_seo_data.py` (696 lines)
- `backend/faith_gita_data.py` (595 lines)
- `backend/faith_bible_data.py` (1,435 lines)
- `backend/assets/faith/` -- gita_verses.json, bible_promises_source.json, bible_meanings_lexicon.json, bible_supporting_references.json, bible_supporting_references.json

---

## Why FAITH-1A Exists

Temple Team ran the **ECHO // PACE 3-Layer Compliance Test** on samples from the delivered content. While individual cluster tests showed Gita at 10.30% (PASS) and Bible anxiety cluster at 32.81% (PASS after rewrite), Temple Team has identified **4 enrichment gaps** and requires Codex to:

1. Run the full 3-layer compliance test across ALL page types (not just sample clusters) and deliver full test output
2. Enrich Bible pages using 3 partially-used source PDFs (see Section 3)
3. Strengthen Transit × Scripture differentiation (12 zodiac signs must feel genuinely distinct)
4. Add `how_to_apply` field to all Gita verse × situation records

**KPI:** All 4 page types must PASS all 3 ECHO // PACE layers before deploy validation is complete.

---

## Mandatory Reading -- 4 Process Docs

Before beginning any work, read and apply these 4 process documents:

| Doc | File | What It Governs |
|---|---|---|
| PROCESS_5 | `Codex_Deliveries/ECHO_PACE_PROCESS/PROCESS_5_CONTENT_ANCHOR_FRAMEWORK.md` | How to anchor every page to unique, non-templated content |
| PROCESS_6 | `Codex_Deliveries/ECHO_PACE_PROCESS/PROCESS_6_SCHEMA_ORG_TYPES_BY_MODULE.md` | Required Schema.org types per Faith page type |
| PROCESS_7 | `Codex_Deliveries/ECHO_PACE_PROCESS/PROCESS_7_YMYL_CONTENT_QUALITY.md` | YMYL quality standards (Faith is a YMYL category) |
| FAITH_TEMPLATE | `Codex_Deliveries/Faith_Hubs/FAITH_CONTENT_GENERATION_TEMPLATE.md` | Faith-specific content generation rules and framing |

---

## ECHO // PACE 3-Layer Compliance Gate (MANDATORY)

All 4 page types must pass all 3 layers. This is a **hard gate** -- delivery will not be accepted without the full test output.

### Layer 1 -- TF-IDF Cosine Similarity (body fields)

| Page Type | PASS Ceiling | FLAGGED | BLOCKED |
|---|---|---|---|
| Gita verse × situation pages | ≤ 30% | ≥ 35% | ≥ 50% |
| Bible topic × transition pages | ≤ 35% | ≥ 40% | ≥ 55% |
| Transit × Scripture pages | ≤ 40% | ≥ 45% | ≥ 60% |
| Daily Evergreen pages | ≤ 40% | ≥ 45% | ≥ 60% |

Codex's own pre-delivery test confirmed:
- Gita 2:47 sample cluster: **10.30% PASS** ✅
- Bible anxiety cluster: **32.81% PASS** (after rewrite from 41.59%) ✅

These are sample results. FAITH-1A requires a **full-scale test** across all clusters.

### Layer 2 -- N-gram Phrase Match (stop-word filtered)

No 4+ consecutive meaningful words (stop words excluded) should appear in more than **15% of records** within any page type cluster.

Faith-specific stop words to add to the base list:
```
verse, scripture, gita, bible, faith, spiritual, god, lord, divine,
chapter, passage, meaning, guidance, path, soul, heart, love, grace,
peace, truth, life, light, way, teach, wisdom, prayer
```

**FAIL condition:** Any 4-gram phrase appearing in > 15% of sampled pages.

### Layer 3 -- Jaccard Heading / Section Title Match

Section headings, `display_name` fields, and FAQ question text must not be near-verbatim copies across records.

**FAIL condition:** Jaccard similarity ≥ 0.75 across any heading pair within a page type cluster.

### How to Run the Test

```bash
# From repo root
PYTHONPATH=backend python3 backend/scripts/verify_faith_compliance.py
```

If this script does not exist yet, **create it** following the same 3-layer architecture as `backend/scripts/verify_angel_numbers_compliance.py`.

Paste the **full terminal output** in your delivery confirmation. Delivery will not be accepted without it.

---

## Enrichment Task 1 -- Bible Pages: 3 Partially-Used Source PDFs

The Bible module was built primarily from `the_book_of_bible_promises.pdf`. Three additional PDFs were loaded but **only partially enriched**:

| PDF | Content | Enhancement target |
|---|---|---|
| `Bible Meanings.pdf` | Word-level exegesis, Hebrew/Greek root meanings for key Bible terms | Add `word_study` field to Bible topic pages -- 1 key term per topic with its root language meaning |
| `Scripture_for_Every_Moment.pdf` | Situational scripture applications across 50+ life scenarios | Deepen the `application` paragraph on Bible transition pages (currently generic; should reference the specific life scenario from this source) |
| `Magic In The Bible.pdf` | Miracle narratives, symbolic acts, numbers in scripture | Add a `symbolic_note` field to 30% of Bible topic pages where symbolic content is present |

**Specific deliverables:**

**`word_study` field (all 120 Bible topic pages):**
```python
"word_study": {
    "term": "Hesed",               # Key Hebrew/Greek term for this topic
    "language": "Hebrew",
    "root_meaning": "Loyal love that persists regardless of whether it is deserved",
    "relevance": "Understanding hesed reframes this promise from conditional reward to unconditional covenant."
}
```

**`symbolic_note` field (where applicable -- approximately 36 of 120 topics):**
```python
"symbolic_note": "The number seven appears throughout this passage (seven days, seven priests, seven trumpets) -- in Hebrew tradition, seven marks completeness and divine rest."
```

These fields must be added to `backend/faith_bible_data.py` and exposed through the existing `get_bible_topic_payload()` function.

---

## Enrichment Task 2 -- Gita Pages: `how_to_apply` Field

Every Gita verse × situation record currently has: `verse_text`, `meaning`, `situation_message`, `affirmation`, `action_steps`.

Add a `how_to_apply` field -- a **practical, daily-life instruction** that answers "What do I actually do today with this teaching?"

This is different from `action_steps` (which are general). `how_to_apply` is situation-specific and immediate.

**Structure:**
```python
"how_to_apply": str  # 50-80 words. One concrete practice for today.
                     # Specific to the verse AND the situation combination.
                     # Example format: "Today, when [trigger situation arises], 
                     # [specific action drawn from this verse]. 
                     # You can anchor this by [concrete ritual or phrase]."
```

**Variety requirement:** No two `how_to_apply` texts should share a 4+ word meaningful phrase. The instruction must differ across all 15 situations for the same verse.

---

## Enrichment Task 3 -- Transit × Scripture Differentiation

Current state: 12 zodiac sign transit pages exist but Temple Team observed they feel structurally similar. The core scripture reference changes, but the framing language around the transit meaning is insufficiently differentiated.

**Required fix:** Each of the 12 transit pages must have:
- A sign-specific **transit framing paragraph** that uses the sign's element (Fire/Earth/Air/Water) and modality (Cardinal/Fixed/Mutable) as the lens through which the transit scripture is interpreted
- Sign-specific **3-step integration practice** (not generic "reflect, pray, act" -- each step must reference that sign's actual character)

**Example: Aries (Fire, Cardinal):**
- Paragraph: frames the transit through urgency, initiation, and the fire element's need for direction
- Steps: (1) Take one bold, declared action before overthinking sets in; (2) Speak your intention aloud -- Aries energy needs to be voiced, not just felt; (3) Channel any frustration into a single focused act of courage rather than scattered effort

**Example: Taurus (Earth, Fixed):**
- Paragraph: frames the transit through patience, embodied trust, and the earth element's need for rootedness
- Steps: (1) Spend 10 minutes outside, barefoot or in contact with something natural; (2) Write down what you are building long-term -- Taurus sustains what others abandon; (3) Eat a nourishing meal slowly and with intention before making any decision

These must vary meaningfully across all 12 signs. Update `backend/faith_seo_data.py` in the `SIGNS` list.

---

## Schema.org Compliance (PROCESS_6)

Confirm these Schema.org types are implemented on each page type. If missing, add them:

| Page Type | Required Schema |
|---|---|
| Gita verse × situation | `Article` + `BreadcrumbList` + `FAQPage` |
| Bible topic × transition | `Article` + `BreadcrumbList` + `FAQPage` |
| Transit × Scripture | `Article` + `BreadcrumbList` |
| Daily Evergreen | `Article` + `BreadcrumbList` |
| Hub pages (Gita, Bible, Transit, Daily) | `CollectionPage` + `BreadcrumbList` + `FAQPage` |
| Faith root hub | `WebPage` + `BreadcrumbList` + `FAQPage` + `Speakable` |

All schema must be valid JSON-LD rendered via the `<SEO>` component.

---

## YMYL Compliance (PROCESS_7)

Faith content is classified as YMYL (Your Money or Your Life -- spiritual guidance category). All page types must comply:

1. **No spiritual claims that imply guaranteed outcomes.** Replace language like "this verse will heal your relationship" with "this verse offers a framework for approaching..."
2. **No medical-adjacent claims** in health or grief transition pages. Replace "scripture heals trauma" with "scripture can offer a stabilising perspective during difficult periods"
3. **Sourcing transparency:** Every Gita verse must cite chapter and verse number. Every Bible verse must cite book, chapter, verse in full (e.g., "Philippians 4:6-7 (NIV)")
4. **Author stance:** Content must be presented as *interpretation* and *spiritual reflection*, not doctrinal authority

---

## Copyright Compliance

- Gita verse text: quoted from public domain translations ONLY (not Prabhupada's purports -- those are Bhaktivedanta Book Trust copyright). Verse text itself is in public domain.
- Bible verse text: NIV text requires permission for large quotations. Limit to maximum 500 NIV words total across the module, or switch to KJV (public domain) or ESV (limited free licence). **Confirm which translation is in use and whether the volume is within licence limits.**
- All commentary, application text, FAQ answers, situation framing: 100% original -- confirm this.

---

## Delivery Checklist

**Compliance gate (mandatory):**
- [ ] `backend/scripts/verify_faith_compliance.py` created (3-layer test script)
- [ ] Full compliance test output pasted in delivery confirmation
- [ ] All 4 page types PASS all 3 layers

**Enrichment deliverables:**
- [ ] `word_study` field added to all 120 Bible topic records in `faith_bible_data.py`
- [ ] `symbolic_note` field added to applicable Bible topics (~36 records)
- [ ] `how_to_apply` field added to all Gita verse × situation records (all 15 situations per verse)
- [ ] `how_to_apply` texts are situation-specific -- no two share a 4+ word phrase
- [ ] Transit × Scripture: all 12 signs have element-and-modality-specific framing paragraphs
- [ ] Transit × Scripture: all 12 signs have sign-specific 3-step integration practice

**Schema compliance:**
- [ ] All page types have correct Schema.org JSON-LD as per PROCESS_6
- [ ] `FAQPage` schema present on all hub pages and verse/topic pages

**Quality compliance:**
- [ ] YMYL language audit complete -- no guaranteed-outcome claims
- [ ] Bible verse translation confirmed + volume within licence
- [ ] All commentary is 100% original (not from Prabhupada or copyrighted Bible commentary)

**Technical:**
- [ ] `python3 -m py_compile backend/faith_seo_data.py faith_gita_data.py faith_bible_data.py` → PASS
- [ ] `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` → PASS
- [ ] No changes to any file outside the Faith module (no server.py, App.js, NavBar.jsx modifications)

---

## KPIs -- Codex Is Accountable For These

| KPI | Target | How to Verify |
|---|---|---|
| Gita L1 TF-IDF similarity | ≤ 30% worst pair | compliance test output |
| Bible L1 TF-IDF similarity | ≤ 35% worst pair | compliance test output |
| Transit L1 TF-IDF similarity | ≤ 40% worst pair | compliance test output |
| Daily L1 TF-IDF similarity | ≤ 40% worst pair | compliance test output |
| L2 N-gram violations | 0 violations | compliance test output |
| L3 Jaccard heading match | < 75% all pairs | compliance test output |
| `how_to_apply` uniqueness | 0 shared 4-grams across 15 situations/verse | spot-check in compliance script |
| Bible `word_study` coverage | 100% of 120 topics | `len([p for p in pages if 'word_study' in p]) == 120` |
| Schema.org coverage | 100% pages have required schema | manual check 3 pages per type |

**Codex must paste the full compliance test terminal output in the delivery thread. Delivery will not be accepted without it.**

---

## What Must NOT Change

- File names and module structure (no renames)
- All existing function signatures: `get_gita_page()`, `get_bible_page()`, `get_faith_hub_payload()`, etc.
- All existing route paths
- Total page counts: 1A+1B (~300), Phase 2 (10,500), Phase 3 (6,000)
- `faith_seo_router.py` -- do not modify endpoints or request/response shapes
- `frontend/src/pages/faith-seo/` component names and props contracts

---

*Commission prepared by Temple Team -- EverydayHoroscope, 2026-05-27*
