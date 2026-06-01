# ECHO/PACE Scan Results -- RUD-1 / CRY-1 / FAITH-20K
> Scan date: 2026-05-31 | Run by: Claude Code
> Scripts: `tests/echo_pace_rud_scan.py` · `tests/echo_pace_cry_scan.py` · `tests/echo_pace_faith_scan.py`

---

## Gate Reference

| Layer | Criterion | PASS | FLAGGED | BLOCKED |
|---|---|---|---|---|
| L1 | TF-IDF cosine worst pair | < 50% | 50-69% | ≥ 70% |
| L2 | 4-gram (stop-filtered) in > 15% of pages | 0 violations | -- | Any violation |
| L3 | Jaccard heading similarity | < 60% | ≥ 60% | -- |
| Layer G | Google hits for exact phrase | ≤ 1 | 2-4 | > 4 |

Layer G not run (no SERPER_API_KEY in this session). Run separately before seeding.

---

## 1. Rudraksha -- RUD-1

### Verdict: 🟡 CONDITIONAL PASS (L1 ✅ / L2 ❌ / L3 ⚠️)

L1 passes across all 4 page types. L2 and L3 both fail -- structural boilerplate requires variation before seeding.

| Page Type | Pages | L1 Score | L1 Status | L2 Violations | L3 Violations |
|---|---|---|---|---|---|
| MUKHI | 21 | 27.0% | PASS ✅ | 10 (100% freq) | 10 (100% Jaccard) |
| PLANET | 9 | 8.4% | PASS ✅ | 10 (100% freq) | 10 (71% Jaccard) |
| PROBLEM | 20 | 29.0% | PASS ✅ | 10 (100% freq) | 10 (75% Jaccard) |
| SIGN | 12 | 4.7% | PASS ✅ | 10 (100% freq) | 10 (71% Jaccard) |

**Global L1 worst: 29.0% -- PASS**

### L2 Root Cause
All violations appear at **100% frequency** (in every page of that type). Source: `_faq_items()` in `rudraksha_content.py` -- the FAQ answer templates use fixed structural phrases that appear verbatim on every page. Examples:

```
"mukhi rudraksha generally chosen"       -- MUKHI FAQ boilerplate
"worn personal guidance commonly"        -- MUKHI FAQ boilerplate
"clear purpose instead layering"         -- PLANET FAQ boilerplate
"here mukhi rudraksha supported"         -- PROBLEM FAQ boilerplate
"yes better combine primary"             -- SIGN FAQ boilerplate
```

Fix required: Inject **at least 5 variant phrasings** per FAQ answer template in `_faq_items()` and select one per page using a seed hash (same approach as Angel Numbers INTENT_STYLES fix).

### L3 Root Cause
Meta title templates follow `"{N} Mukhi Rudraksha - Benefits, Mantra & Wearing Guide"`. The digit (1, 2, 3...) is a 1-character token filtered by the scanner's `len > 2` rule → the titles become lexically identical after tokenisation → 100% Jaccard for MUKHI.

Fix required: Use **word-form numbers** in meta titles (e.g., "One Mukhi Rudraksha", "Seven Mukhi Rudraksha") rather than digits, OR add a unique keyword per type (e.g., planet name in PLANET pages is already distinct enough but template framing needs work).

### Open Actions
- [ ] Issue RUD-L2 fix commission to Codex: vary FAQ answer phrases in `_faq_items()` (5+ variants per answer, hash-selected)
- [ ] Fix meta_title format for MUKHI pages: switch digit to word-form number
- [ ] Re-run scan after delivery -- must clear L2 (0 violations) and L3 (< 60%)
- [ ] Wire App.js routes after scan passes
- [ ] Run Layer G before seeding

---

## 2. Crystal Healing -- CRY-1

### Verdict: 🟡 CONDITIONAL PASS (L1 ✅ / L2 ❌ / L3 ⚠️)

L1 passes -- crystal pages borderline at 47.7% (must not regress past 50%). L2 and L3 fail -- boilerplate in caution/FAQ fields.

| Page Type | Pages | L1 Score | L1 Status | L2 Violations | L3 Violations |
|---|---|---|---|---|---|
| CRYSTAL | 50 | 47.7% | PASS ✅ ⚠️ borderline | 10 (100% freq) | 10 |
| INTENTION | 20 | 20.8% | PASS ✅ | 10 (100% freq) | 1 |

**Global L1 worst: 47.7% -- PASS (but within 2.3% of FLAGGED gate)**

### L2 Root Cause
All violations at 100% frequency. Source: structural boilerplate in `_build_faq()` and caution/cleansing fields. Examples:

```
"option stone soft porous"               -- caution field boilerplate (water cleansing caveat)
"use emotional spiritual balancing"      -- FAQ answer template
"spiritual balancing simple cleansing"   -- FAQ answer overlap
"where theme shows strongly"             -- INTENTION page boilerplate
"feels balanced weekly cleansing"        -- INTENTION FAQ boilerplate
```

Fix required: Same as RUD -- introduce **5+ variant phrasings** for FAQ template phrases in `_build_faq()` and for structural caution/cleansing copy.

### L3 Root Cause
Title pattern `"{Crystal Name} Crystal - Healing Properties, Chakra & Uses | EverydayHoroscope"` -- overlapping for "Hessonite Garnet" vs "Garnet" (88% Jaccard), "Yellow Sapphire" vs "Blue Sapphire" (78%), etc. The suffix is fixed and the only differentiator is the crystal name.

Partially acceptable (crystal-type names are the differentiator Google expects here), but the `| EverydayHoroscope` suffix adds shared tail weight. Recommendation: vary the suffix per crystal rather than using a fixed pipe brand.

### Open Actions
- [ ] Issue CRY-L2 fix commission to Codex: vary FAQ + caution phrase templates (5+ variants each)
- [ ] Improve meta_title suffix variation for crystal pages (avoid identical tail)
- [ ] Monitor L1 crystal score -- must stay < 50% after rework
- [ ] Wire App.js routes after scan passes
- [ ] Run Layer G before seeding

---

## 3. Faith & Scripture -- FAITH-20K

### Verdict: 🔴 BLOCKED (L1 ❌ / L2 ❌ / L3 ⚠️)

Three of four page types are L1 BLOCKED. Root cause is structural -- same-situation pages across chapters share fixed boilerplate in `summary`, `hook`, and `application` fields. This is the same pool-exhaustion failure mode as Angel Numbers ANGEL-1.

| Page Type | Pages | Sample | L1 Score | L1 Status | L2 | L3 |
|---|---|---|---|---|---|---|
| GITA | 10,500 | 3,480 | 100.0% | BLOCKED ❌ | FAIL | FLAGGED |
| BIBLE | 6,000 | 100 | 81.7% | BLOCKED ❌ | FAIL | FLAGGED |
| TRANSIT | 156 | all | 99.5% | BLOCKED ❌ | FAIL | FLAGGED |
| DAILY | 144 | all | 50.0% | PASS ✅ (on-gate) | FAIL | FLAGGED |

**Global L1 worst: 100.0% -- CRITICAL BLOCK**

### L1 Root Cause -- Gita (100%)
The Gita page generator in `get_gita_page()` fills `summary`, `hook`, and `application` from situation-level constants (`situation['hook']`, `situation['hidden_fear']`, `situation['practice_shift']`). These values are identical for every verse in the same situation (15 situations × N chapters). Result: all pages for "Relationship Breakdown" share the same non-verse-specific text -- only the chapter:verse number changes. TF-IDF cosine = 1.0 within any same-situation cluster.

Evidence from L2 violations:
```
"ask denial asks truer"          -- from the FIXED hook template: "It does not ask for denial. It asks for a truer next step"
"emotional honesty specific spiritual"  -- from FIXED hook: "emotional honesty, and a specific spiritual response"
```

These strings appear word-for-word on every one of the 10,500 Gita pages.

### L1 Root Cause -- Bible (81.7%)
Same issue at topic level. `summary` field: `"This page approaches {transition.lower()} through the Bible theme of {topic.lower()}, keeping the promise practical, emotionally honest, and connected to a parallel Vedic bridge."` -- this sentence appears on every Bible page. The only variable is the topic/transition label. TF-IDF cosine within same-topic cluster ≈ 82%.

### L1 Root Cause -- Transit (99.5%)
Transit pages exist in Gita and Bible tradition variants. "Mars Retrograde - Gita" vs "Mars Retrograde - Bible" share most body content (transit description, panchang_layer, practice) with only the verse citation differing. Near-identical cosine.

### Fix Required (Codex Commission -- FAITH-2 or FAITH-REWRITE)
This requires a generator-level rewrite with:
1. **Verse-specific anchoring**: `summary` and `hook` must reference specific verse content (verse translation words, key Sanskrit term from that verse). Must NOT use the same situation boilerplate for every verse.
2. **Situation sub-templating**: At minimum, 5 situation-variant openings per situation, selected by `_hash_index(chapter, verse, situation_slug)`.
3. **Bible topic-specific body**: `summary` must vary by verse content, not just topic+transition label.
4. **Transit tradition separation**: Gita-tradition and Bible-tradition transit pages must have meaningfully different body text beyond just the verse citation.
5. **DAILY**: Currently at exactly 50.0% -- on the gate. A small fix to vary the monthly seasonal framing is sufficient.

### Immediate Ruling
**FAITH-20K pages must NOT be seeded until a compliant generator is delivered and scanned.** The current content is structurally thin -- identical body text across thousands of pages is a Google duplication risk.

### Open Actions
- [ ] Issue FAITH-REWRITE commission to Codex (separate brief to be drafted -- priority CRITICAL)
- [ ] Scope the commission: Gita per-verse anchoring + Bible body variation + Transit tradition separation + Daily seasonal variation
- [ ] Re-run scan after delivery -- all types must clear L1 < 50%
- [ ] Do NOT seed faith_gita_pages, faith_bible_pages, faith_transit_pages, or faith_daily_pages until scan passes
- [ ] DAILY pages: minimal fix may be possible inline (5 seasonal framing variants)

---

## Summary Matrix

| Module | L1 | L2 | L3 | Layer G | Seed OK? | Next Action |
|---|---|---|---|---|---|---|
| RUD MUKHI | 27% ✅ | ❌ | ⚠️ | Pending | ❌ NO | Codex L2/L3 fix |
| RUD PLANET | 8% ✅ | ❌ | ⚠️ | Pending | ❌ NO | Codex L2/L3 fix |
| RUD PROBLEM | 29% ✅ | ❌ | ⚠️ | Pending | ❌ NO | Codex L2/L3 fix |
| RUD SIGN | 5% ✅ | ❌ | ⚠️ | Pending | ❌ NO | Codex L2/L3 fix |
| CRY CRYSTAL | 48% ✅⚠️ | ❌ | ⚠️ | Pending | ❌ NO | Codex L2/L3 fix |
| CRY INTENTION | 21% ✅ | ❌ | ⚠️ | Pending | ❌ NO | Codex L2/L3 fix |
| FAITH GITA | 100% ❌ | ❌ | ⚠️ | Pending | ❌ NO | CRITICAL rewrite |
| FAITH BIBLE | 82% ❌ | ❌ | ⚠️ | Pending | ❌ NO | CRITICAL rewrite |
| FAITH TRANSIT | 100% ❌ | ❌ | ⚠️ | Pending | ❌ NO | CRITICAL rewrite |
| FAITH DAILY | 50% ✅⚠️ | ❌ | ⚠️ | Pending | ❌ NO | Minor fix + rescan |
