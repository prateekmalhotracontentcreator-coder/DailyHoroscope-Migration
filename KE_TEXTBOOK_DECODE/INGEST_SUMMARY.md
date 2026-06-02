# KE Ingest Summary -- All Books
> Single source of truth for ingest status across all Phase 1 and Phase 2 books.
> Last updated: 2026-06-01
> KE Freeze: ✅ LIFTED 2026-05-22

---

## Ingest Strategy

1. **BPHS Vol 1 and Vol 2 go first** -- foundational traditional Vedic astrology texts. All other books are checked against BPHS as the primary authority.
2. **Close all open points before ingest** -- no book enters MongoDB with unresolved HIGH items.
3. **Pre-ingest dedup** -- run `ke_dedup_script.py` between new book's local JSON folder and each previously ingested book's local JSON folder. No MongoDB export needed (local folders = source of truth).
4. **Contradiction pair identification** -- automated by dedup script. GAI/NLM proposes resolution for each flagged pair. No prescribed arbiter -- GAI advises, TT decides.
5. **All rules enter as** `pending_human_review`. Co-founder sign-off required before any rule reaches `approved` status.

---

## Phase 1 -- Foundation Ingest (BPHS First)

### P1-1: BPHS Vol 1
**Science ID:** `jyotish` | **Decode folder:** `BPHS_CC_Decode/`

| Metric | Value |
|---|---|
| Chapters decoded | 37 of 45 (Ch01-02 mythology; Ch27/43/44 dedicated sprints pending; Ch34/40 absorbed) |
| Ingest status | ✅ **FULLY INGESTED -- 2026-06-01** |
| Phase 1 (Ch12-44) | ~1,069 rules · ✅ In MongoDB · all 5 NLM issues CLOSED |
| Phase 2 (Ch03-11, Ch25-33) | 696 rules · ✅ In MongoDB · batch `bphs-vol1-phase2-v1-20260601` |
| **Total rules in MongoDB** | **~1,765** |
| Phase 2 breakdown | 491 auto_approved (71%) · 170 PHR (24%) · 35 flagged TT/GAI (5%) · 0 contradictions |
| GAI session | 2026-05-30 -- all 10 HIGH items resolved; encode pass applied 2026-05-31 |
| GAI resolution log | `BPHS_CC_Decode/BPHS_Vol1_GAI_Resolutions.md` |
| Engine code | `BPHS_CC_Decode/BPHS_Vol1_Engine_Core.py` (validated ✅) |
| 35 flagged (TT/GAI) | 12 Dhwaja (Ch25) · 5 formula conflicts (Ch26/28) · 6 doctrinal (Ch03/04/30/32/33) · 5 non-standard (Ch32/33) · 3 factual errors (Ch32) · 4 extreme outcomes (Ch33) |
| Post-ingest dedup | Run against BPHS Vol 2 after Vol 2 is ingested |

**Resolved Items (all 6 HIGH cleared 2026-05-30):**

| ID | Issue | Resolution |
|---|---|---|
| ~~TT-CH28-03~~ | Ishta Phala formula | ✅ Arithmetic: `(Uchcha + Cheshta − 2) × 5`. Sanskrit explicit. |
| ~~TT-CH28-01~~ | Uchcha Rasmi denominator | ✅ 180°. Formula: `(lon − deb) / 180 × 8`. Validated. |
| ~~TT-CH30-01~~ | Upa Pada computation | ✅ Arudha of 12th house. Parity rules are Chaukamba commentary only. |
| ~~TT-CH31-01~~ | Argala obstruction counting | ✅ Reading A -- from ORIGINAL house. Jaimini Sutras corroborate. |
| ~~TT-CH06-01~~ | Trimsamsa even-sign reversal | ✅ Interpretation (b) -- BOTH planet order AND degree widths reversed. |
| ~~TT-CH09-01~~ | Balarishta age threshold | ✅ 24 years per BPHS Sanskrit. Note 12y in other texts in UI. |
| ~~TT-CH06-03~~ | Bhamsa D27 starting sign | ✅ Modality-based: Movable→Aries, Fixed→Cancer, Mutable→Libra. |
| ~~TT-CH28-04~~ | Subhanka values | ✅ Neutral = 8, Extreme friend = 22. Full 9-entry table confirmed. |
| ~~TT-CH09-04~~ | Gandanta zone breadth | ✅ Both sides -- last 3°20' water sign + first 3°20' fire sign. |
| ~~TT-CH06-05~~ | Ch05/Ch06 rule ownership | ✅ Slokas 21-24 belong to Ch05. Ingest as Ch05 rules. |

**All 5 MED items resolved via direct PDF read (2026-06-01) -- all closed:**

| ID | Priority | Chapter | Status |
|---|---|---|---|
| TT-CH30-02 | ✅ CLOSED | Ch30 | Mars+Saturn sign qualifier required; 2nd from Upa Pada must be Mercury or Mars sign |
| TT-CH30-03 | ✅ CLOSED | Ch30 | Count from 12th lord's position (Santhanam example explicit) |
| TT-CH06-02 | ✅ CLOSED | Ch06 | 30 minutes of arc per Shashtiamsa (half a degree -- fractional confirmed) |
| TT-CH09-02 | ✅ CLOSED | Ch09 | Oriental half = 10th cusp → 4th cusp via Lagna (cusp-based, NOT sequential houses 1-6) |
| TT-CH31-02 | ✅ CLOSED | Ch31 | Quarter rule applies to obstructor's position; 1st-quarter Argala cancelled by 4th-quarter obstructor |

**Encode actions applied 2026-05-31 (via `apply_vol1_encode.py`):**
- bphs1-ch28-002: Uchcha Rasmi formula corrected → `(lon−deb)/180×8`. TT-CH28-01 ✅
- bphs1-ch28-007: Ishta Phala arithmetic formula confirmed. TT-CH28-03 ✅
- bphs1-ch28-008: Subhanka full table confirmed (neutral=8, extreme friend=22). TT-CH28-04 ✅
- bphs1-ch06-012: Bhamsa D27 corrected element-based → MODALITY-based (Movable→Aries, Fixed→Cancer, Mutable→Libra). TT-CH06-03 ✅
- bphs1-ch06-013: Trimsamsa even-sign reversal -- BOTH order AND widths reversed confirmed. TT-CH06-01 ✅
- bphs1-ch06-027/028: chapter field 6→5 (slokas belong to Ch05). TT-CH06-05 ✅
- bphs1-ch09-002: Balarishta 24-year threshold confirmed. TT-CH09-01 ✅
- bphs1-ch09-012: Gandanta BOTH sides confirmed -- last 3°20' water + first 3°20' fire. TT-CH09-04 ✅
- bphs1-ch30-001/002: Upa Pada = Arudha of 12th house (base BPHS). Parity rule = Chaukamba commentary only. TT-CH30-01 ✅
- bphs1-ch31-002: Argala obstructors counted from ORIGINAL house (Reading A). TT-CH31-01 ✅

**Post-ingest action (pending):** Run dedup between BPHS Vol 1 Phase 1+2 rules and BPHS Vol 2 (same text family) before or at Vol 2 ingest. Use local JSON folders -- no MongoDB export needed.

---

### P1-2: BPHS Vol 2
**Science ID:** `vedic_astrology` | **Decode folder:** `BPHS_Vol2_CC_Decode/`

| Metric | Value |
|---|---|
| Chapters decoded | 3 (Ch49, Ch50, Ch51 -- Dasa chapters) |
| Total rules (post-encode) | 249 (✅ confirmed 2026-05-31: Ch49:154 + Ch50:73 + Ch51:22) |
| Active rules | 248 (✅ confirmed 2026-05-31) |
| Inactive (source gap) | 1 (bphs2-ch49-gemini-pada-8-gap -- absent from Santhanam translation) |
| Inactive (obsolete placeholder) | 0 (all placeholders replaced with active rules) |
| Max recoverable | 107 of 108 Navamsa Pada rules |
| Ingest status | ✅ **INGESTED + TRIAGE COMPLETE -- 2026-06-01** |
| GAI resolution log | `BPHS_Vol2_CC_Decode/BPHS_Vol2_GAI_Resolutions.md` (PDF-verified 2026-05-31) |

**All 10 OCR items resolved 2026-05-31:**

| ID | Chapter | Resolution |
|---|---|---|
| Ch49-Virgo | Ch49 | ✅ 9 individual outcomes confirmed (PDF p.598-599) |
| Ch49-Libra | Ch49 | ✅ 9 individual outcomes confirmed; sub-sign repeats text-native (PDF p.599) |
| Ch49-Gemini-P7 | Ch49 | ✅ Taurus Amsa / weapon injury (PDF p.597) |
| Ch49-Gemini-P9 | Ch49 | ✅ Gemini Amsa / enjoyment (PDF p.597) |
| Ch49-Gemini-P8 | Ch49 | 🚨 SOURCE GAP -- absent from text. active: false, source_gap: true. See M-38. |
| Ch49-Scorpio | Ch49 | ✅ Cancer/Leo Amsa (financial gains / government opposition) |
| Ch49-Aquarius | Ch49 | ✅ Aries/Taurus Amsa (loss of happiness / death) |
| Ch49-Remedies | Ch49 | ✅ Generic Shanti Karma only -- no specific deities in text |
| Ch50-Combust | Ch50 | ✅ Use BPHS Ch07 thresholds; Ch50 does not specify degrees |
| Ch51-Bhoga | Ch51 | ✅ Provisional accept (algorithm verified mathematically) |

**Encode actions:** ✅ ALL 10 APPLIED 2026-05-31 via `apply_vol2_encode.py`. Ch49: 134→154 rules (5 OCR placeholders replaced, 2 new rules created). Ch50 rule 041: decode_notes + Ch07 combustion ref added. Ch51 rule 020: provisional:true + decode_notes added.

**Post-ingest dedup targets:** BPHS Vol 1 (internal cross-check -- same source text) ✅ Done 2026-06-01: 0 dup, 0 contra (local folder dedup + MongoDB export dedup both clean).

**Validation summary (post-triage):** 118 auto_approved / 131 PHR / 0 flagged. 5 contradiction pairs detected -- all 5 false positives (complementary polarity rules, confirmed by GAI). All triage complete. Awaiting co-founder sign-off.

**Ingest tracker:** `.claude/ke/ingest/BPHS_VOL2_INGEST.md`

---

## Phase 1 -- Additional Books (approved sequence)

### P1-3: 300 Combinations
**Decode folder:** `ThreeHundredCombinations_CC_Decode/` | **Rules:** 329 (incl. intro + strength sections) | **Open items:** See 300_COMBINATIONS_INGEST.md

| Metric | Value |
|---|---|
| Ingest status | ✅ **INGESTED + TRIAGE COMPLETE -- 2026-06-01** |
| Batch ID | `300-combinations-v1-20260601` |
| Rules inserted | 329 (329 active) |
| Dedup | ✅ Clean -- 0 matches, 0 contradictions vs 9,196 MongoDB rules |
| auto_approved | **141** |
| pending_human_review | **188** |
| flagged | **0** |
| pending_review | 0 |
| Contradiction pairs | 3 (all Nabhasa cross-pairs, all strength_dependent -- no rejections needed) |
| Schema note | Two schemas: NEW (Y001-040: full_text/claim_polarity) + OLD (Y044-300: results/polarity/conditions list OR dict). OLD schema patched post-ingest via `patch_300combo_old_schema.py` + `patch_300combo_all_open_items.py`. |
| OP-08 closure | ✅ 14 tba conditions (Y264-Y274, Y292-Y294) encoded from Diagnostics. 4 engine-dep rules (Y130-Y134) → PHR. Y271 condition error corrected. Y294 speculative overlay stripped. All Bucket B → PHR. |
| Key triage learnings | See schema learnings box in `THREAD_BRIEF_300COMBINATIONS_INGEST.md` |
| Ingest tracker | `.claude/ke/ingest/300_COMBINATIONS_INGEST.md` |

---

### P1-4: 300 Horoscopes Vol 1
**Decode folder:** `ThreeHundredHoroscopes_CC_Decode/` | **Rules:** 57 | **OCR report:** `H300_OCR_Issues_Report.docx`

| Status | Detail |
|---|---|
| Ingest status | ✅ READY -- all 57 rules unblocked |
| CC PDF validation | 2026-05-31 -- all 3 previously blocked rules cleared by direct PDF read |
| h300-s01-016 | ✅ Nakshatra Pada table -- all 12 signs match PDF exactly (abbreviated names correctly expanded) |
| h300-s04-004 | ✅ Empty-level-skip -- p.28 "Hence Rahu will give result in the following order" confirms text-native |
| h300-s04-005 | ✅ Cumulative levels -- p.28 "give result of Jupiter, Saturn and Mars... respectively" -- all active levels listed simultaneously |
| Duplicate report | `H300_DuplicateCandidateReport.md` -- 29 merge, 16 keep-both, 2 needs-human-call (TT at approval stage) |
| Post-ingest dedup | Run against BPHS Vol 1 + Vol 2 (when ingested) |

---

### P1-5: Longevity Unnatural Death
**Decode folder:** `LongevityUnnatural_CC_Decode/` | **Rules:** 44 | **Brief:** `LU_TempleTeam_Brief.docx`

| Status | Detail |
|---|---|
| Ingest status | ✅ READY -- all 5 HIGH items resolved by CC PDF validation |
| CC PDF validation | 2026-05-31 -- `LU_PDF_Validation_Results.md` |
| lu-s04-001 | ✅ "should" confirmed (p.6/p.9) -- weighted condition, not hard gate |
| lu-s04-014 | ✅ AND/OR resolved: 06 AND Mars required; maraka OR badhaka either sufficient |
| lu-s04-003/004 | ✅ 5-level chain confirmed; Level 5 "connected" = conjunction + aspect |
| lu-s04-010 | ✅ "Lethal planet" = both maraka AND badhaka simultaneously (AND logic) |
| CS1 Mercury | ✅ 19°Aq12'36" (Sata 4) -- DataTable confirmed correct |
| CS1 Jupiter | ✅ Fixed: 00°Pi60' → 00°Pi59'37" in DataTables |
| lu-s04-013 | ✅ Progressive houses = {3, 10, 11} -- 6th excluded (MEDIUM resolved) |
| Remaining MEDIUM (10) | 🟡 Safe to ingest with pending_review: true |
| Remaining LOW (6) | ✅ Safe to ingest as-is |
| Post-ingest dedup | Run against BPHS Vol 1 + 300 Combinations + 300 Horoscopes |

---

### P1-6: Destiny Numerology
**Decode folder:** `DestinyNumerology_CC_Decode/` | **Rules:** 189 (Ch01-15) | **OCR report:** `Book_Wide_OCR_Inconsistencies_Report.docx`

| Status | Detail |
|---|---|
| Ingest status | 🟠 NEAR READY -- OCR issues to clear first |
| Total OCR issues | 41 (29 main + 12 from Ch15 companion): CRITICAL 2 · HIGH 10 · MED 13 · LOW 4 |
| CRITICAL items | Ch17 Number 3 Amethyst · Ch19 two element systems conflict |
| Action | NLM/GAI resolves CRITICAL + HIGH items → ingest |
| Post-ingest dedup | Run against all previously ingested books |

---

### P1-7: SBC (Sarvato Bhadra Chakra)
**Decode folder:** `New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/` | **Rules:** 181 | **OCR report:** `SBC_OCR_Issues_Report.docx`

| Status | Detail |
|---|---|
| Ingest status | 🔴 BLOCKED -- TT decisions required + source gaps |
| TT decisions needed | 7 blocking priority conflicts from 40-question batch (listed in `SBC_Master_Decode_Summary.md`) |
| Source gaps | 24 open questions -- 7 conflicts resolved, 17 remaining |
| CRITICAL OCR items | C-01 Chandra Kalanal index · C-02 Sapt Salaka table · C-03 Star rank results · C-04 Devanagari consonant groups |
| Action | TT resolves 7 priority conflicts → NLM/GAI resolves C-01 through C-04 → remaining OQs → ingest |
| Post-ingest dedup | Run against BPHS Vol 1 + all ingested books |

---

### P1-8: Longevity 58 Chapters
**Decode folder:** `Longevity_CC_Decode/` | **Rules:** ~600+ | **Handover:** `HANDOVER_SUMMARY_LongevityDecode.md`

| Status | Detail |
|---|---|
| Ingest status | ✅ **FULLY INGESTED -- 2026-06-02** · 149 rules · batch `longevity_58ch_v1` · 0 errors · structural validation CLEAN |
| Decode status | ✅ All 58 chapters accounted for (Ch4/5 via NLM, Ch6-Ch58 via CC) |
| **Aayu methodology** | ✅ **APPROVED: Option B + Label-based tagging + 66-75 edge gate (2026-06-02, Prateek)** |
| Architecture | Labels only: `alpa_aayu`, `madhya_aayu` (33-75), `purna_aayu` (75-100). `LONGEVITY_AAYU_CONFIG` → `ke_schema_constants.py`. Edge zone 66-75: `edge_case_zone:true` + gates (dasha_activity, maraka_strength, ayushkaraka_strength). Classical ref point: 72 yrs (Shashtyamsa). |
| Ch36-58 rules | ✅ **CC THREAD COMPLETE 2026-06-02** -- 21 cross-chart rules extracted. Output: `Longevity_CaseStudies_Ch36-58_Rules.json` + `_Diagnostic.md` in `Longevity_CC_Decode/` |
| Ingest result | Ch4=14, Ch5=15, Ch6-19=99, Ch36-58=21. Total=149. Dedup: 0 matches vs 10,471 MongoDB rules (1.56M pairs). |
| Validation result | 69 auto_approved (46%) · 80 pending_human_review (54%) · 0 flagged. Bucket A: 18 truncation artifacts. Bucket B: 11 validator framework errors (KP vs BPHS). Bucket C: 0. |
| TT action | Co-founder sign-off on 69 `auto_approved` rules → `approved` status. |

---

## Phase 2 -- After Phase 1 BPHS Complete

> Start Phase 2 only after BPHS Vol 1 + Vol 2 are ingested. Each Phase 2 book is deduped against BPHS as its primary cross-reference.

### P2-1: KP Astrology
**Decode folder:** `KP_CC_Decode/` | **Rules:** 256 / 77 files | **Brief:** `KP_Vol3_Temple_Brief.md`

| Status | Detail |
|---|---|
| Ingest status | 🟡 NEAR READY -- Cat B/C/G/H open items remain |
| Completed 2026-05-31 | ✅ Entries 248-249 T05 PDF-verified (T06 p.110) · ✅ claim_axis retroactive pass: 12 rules corrected (P01→physical_appearance, P09-003→legal, P33-002→career_finance, P34-002→career, P55-005→health, P75-001→social_relationships, P77-001→career_growth, T09-003/009→travel, T09-004→education) · 54 remaining general = legitimately methodology/cross-domain |
| Open items | Cat B (8 P1): T05 duplicate/skipped entry numbers -- needs OCR docx or T05 PDF · Cat C (2 P1): Missing Rahu-star stubs Swathi 131-138 / Sathabisha 213-221 · Cat G (1 P1): Conditional vs direct delineation inconsistency · Cat H (3 P1): Formatting inconsistencies · P2 terms F-01 to F-06: GAI/NLM batch pending |
| OCR issues | 44 total: 2 P0 Critical · 15 P1 High · 19 P2 Medium · 8 P3 Low |
| NLM/GAI priority | P2 ambiguous terms F-01 to F-06 |
| Post-ingest dedup | BPHS Vol 1 + Vol 2 (system-level differences expected -- KP vs traditional Jyotish) |
| Note | Many contradictions with BPHS are **system-level** differences (KP sub-lord vs traditional lordship), not doctrinal errors. Tag these appropriately during dedup. |

---

### P2-2: BPHS Vol 1 (remaining chapters -- dedicated sprints)
**Chapters pending:** Ch27 (Shadbala), Ch43 (Longevity), Ch44 (Maraka)
These require dedicated decode sprints. Shadbala is a full engine. Ch43/44 depend on each other.

| Status | Detail |
|---|---|
| Ingest status | ⏸ PENDING -- dedicated sprints not yet issued |
| Action | Issue Ch27 (Shadbala) decode sprint separately. Ch43 + Ch44 to follow as a paired sprint. |

---

### P2-3: BPHS Vol 2 (remaining chapters)
Vol 2 currently only covers Ch49-Ch51. Other chapters (Ch46-Ch48, and beyond Ch51) not yet decoded.

| Status | Detail |
|---|---|
| Ingest status | ⏸ PENDING -- Vol 2 expansion sprint not yet issued |
| Action | Scope and issue a Vol 2 expansion decode sprint after Ch49-51 are ingested. |

---

### P2-4: Medical Astrology
**Decode folder:** `MedicalAstrology_CC_Decode/` | **Brief:** `MedAstro_TempleTeam_Brief.md` | **OCR:** `MedAstro_OCR_Issues_Audit.md`

| Status | Detail |
|---|---|
| Ingest status | 🟢 READY -- All Grade A + Grade B items resolved 2026-05-31 |
| Grade A resolved | ✅ A-1: Chart IX birth data confirmed permanently absent -- bench-004 flagged `birth_data_unavailable:true`, Aquarius Lagna derived from analysis, planetary positions extracted from grid. Not a blocker. · ✅ A-2: "17/46" = Lagna degree notation (Cancer 17°46'), NOT birth time. 17:46 IST → Aquarius Lagna (contradicts analysis). Cancer Lagna fully verified by pyswisseph. Additional: chart DOB "7-9-1958" is one-day print error → Sept 6, 1958 (Moon+Mars in Taurus H11 matches analysis ✓). |
| OCR total | 81 issues: 2 Grade A ✅ · 11 Grade B ✅ (11/11) · 7 Grade C · 61 Grade D |
| Grade B status | ✅ ALL 11 OF 11 CLOSED 2026-05-31. B-7 Shambhu Hora: Shambhu Hora Prakash (शम्भुहोराप्रकाशः) by Punjarajacharya (~15th-16th c. CE, Chowkhamba) confirmed. Rahu-H6 maternal uncle rule verbatim. Applied to bench-015. B-8 Chaturdashi Dagdha: Dagdha = Gemini/Virgo/Sagittarius/Pisces per Kalaprakashika confirmed. Chart XVIII blindness mechanism confirmed (Sun+Moon in Dagdha rashis). Applied to bench-013. B-11 Vedic quote: Rigveda 1.91.16 reconstructed. Applied to ma-ch03-005 + DataTable 3.2. All three carry gai_citation_unverified flags -- Ingest Thread to cross-check specific chapter/sloka refs before co-founder approval. |
| Action | Ingest all chapters with `pending_review:true` for Grade B items with gai_citation_unverified flag + `birth_data_unavailable:true` for bench-004. Grade C benchmark data issues (Charts XI/XII/XXII missing DOBs) -- ingest with `analytical_description_only:true`. Grade D cosmetic -- no action needed. |
| Post-ingest dedup | BPHS Vol 1 (medical astrology principles derive from BPHS planetary significations) |

---

### P2-5: Phaladeepika
**Decode folder:** `Phaladeepika_CC_Decode/` | **Rules:** 1218 (28 chapters, 1206 active + 12 TBA/inactive) | **OCR:** `Phaladeepika_Inconsistencies_Review.docx`

| Metric | Value |
|---|---|
| Ingest status | ✅ **INGESTED + TRIAGE COMPLETE -- 2026-06-01** |
| Batch ID | `phaladeepika-v1-20260601` |
| Ingest script | `backend/scripts/ingest_phaladeepika_v1.py` |
| Rules inserted | 1218 (0 errors, 0 skipped) |
| auto_approved | **582** (48%) |
| pending_human_review | **271** (22%) |
| pending_review | **357** (29%) -- OCR truncation artifacts, PD-OP-01 re-encode |
| flagged | **8** (0.7%) -- genuine Bucket C, TT/GAI queue |
| TBA/inactive | 12 (Ch08 PDF gap -- Sun houses 1-6 absent from source) |
| Contradictions detected | 16 pairs: 13 Bucket B (polar opposites / system-mismatch), 3 Bucket C (genuine condition reversal cluster + threshold mismatch) |
| Three-schema mapping | Schema A (Ch01-13, 15-16, 18, 27: full_text + condition dict) · Schema C (Ch14, 17, 19-25: description + conditions list) · Schema B (Ch22, 26, 28: content + empty conditions → engine_spec fallback) |
| Triage summary | 82 flagged → PHR (Bucket B: ethics flag, truncation artifacts, intended polar-opposite pairs, Ch22 Kalachakra system-mismatch, Ch26 transit flags). 8 remain flagged (Bucket C). |
| PD-OP-01 | 357 truncated_text rules need Codex re-encode pass. Ch08 = 109 rules (highest priority). |
| Ingest tracker | `.claude/ke/ingest/PHALADEEPIKA_INGEST.md` |
| Post-ingest dedup | Informational -- run vs BPHS Vol 1 (60-70% conceptual overlap expected on house chapters; rule_ids are distinct, no dedup blocking needed) |

**6 HIGH OCR items resolved 2026-05-31:**
- pd-ch22-c001 · pd-ch25-c002 · pd-ch26-c004 · pd-ch12-c001 · pd-ch27-c001 · pd-ch21-c003

**8 Remaining Flagged (Bucket C -- TT/GAI Queue):**
pd-ch06-028/030 (Adhama/Varishtha yoga condition reversal) · pd-ch07-024 (logic error) · pd-ch07-028 (negation encoding) · pd-ch07-049 (placeholder, tba:true) · pd-ch18-102 (same-outcome for different planets) · pd-ch21-041 (gai_citation_unverified) · pd-ch08-111 (TBA/inactive)

---

## Contradiction Pair Process Summary

| Stage | Who | What |
|---|---|---|
| Within-text (during decode) | NLM thread | Populates `conflicts_with` + `Contradictions.json` per chapter |
| Cross-text (post-ingest) | Dedup script (automated) | Runs between local JSON folders; writes `cross_text_matches` on both rules |
| Pair identification | Dedup script | Flags `relationship: "contradicts"` or `relationship: "partial_contradiction"` |
| Resolution proposal | GAI / NLM | Reviews each flagged pair; proposes resolution type |
| Resolution decision | TT | Accepts or rejects GAI proposal; records in `Contradictions.json` `reviewer_status` |
| Rule status | TT | Losing rule marked `approval_status: "rejected"`; winner stays `pending_human_review` |

Resolution types (GAI proposes, TT decides):
- `strength_dependent` -- both valid; one fires when planet is strong, other when weak
- `timing_dependent` -- both valid; different life stage or dasha period
- `chart_context_dependent` -- other chart factors determine which fires
- `genuine_disagreement` -- texts genuinely disagree; TT decides which to approve
- `translator_interpolation` -- one rule is commentary, not original sloka

---

## Pre-Ingest Dedup Protocol

> No MongoDB export needed. All source rules live in local JSON decode folders.

```bash
# Run between new book and each previously-ingested book's local folder:
python3 backend/ke_dedup_script.py \
  --folder-a /Users/apple/Documents/Knowledge\ Engine_eBooks/[NewBook]_CC_Decode/ \
  --folder-b /Users/apple/Documents/Knowledge\ Engine_eBooks/[ExistingBook]_CC_Decode/

# Report saves to both folders automatically
```

Run once per existing-book pair. After BPHS Vol 1 + Vol 2 are both ingested, every subsequent book needs one dedup run against BPHS Vol 1 and one against BPHS Vol 2.

---

*Last updated: 2026-06-01 by Claude Code -- Phaladeepika ingest session.*
*P1-1 BPHS Vol 1: ✅ FULLY INGESTED ~1,765 rules.*
*P1-2 BPHS Vol 2 Ch49-51: ✅ INGESTED + TRIAGE COMPLETE (118 auto_approved, 131 PHR, 0 flagged).*
*P1-3 300 Combinations: ✅ INGESTED + TRIAGE COMPLETE (141 auto_approved, 188 PHR, 0 flagged). OP-08 closed 2026-06-01.*
*P2-5 Phaladeepika: ✅ INGESTED + TRIAGE COMPLETE (582 auto_approved, 271 PHR, 357 pending_review OCR-PD-OP-01, 8 flagged). 2026-06-01.*
*Next: P1-4 300 Horoscopes (57 rules) -- no blockers, see THREAD_BRIEF_300HOROSCOPES_INGEST.md.*
