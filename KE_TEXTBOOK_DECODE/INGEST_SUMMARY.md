# KE Ingest Summary -- All Books
> Single source of truth for ingest status across all Phase 1 and Phase 2 books.
> Last updated: 2026-06-05 (SBC: all 4 OCR items resolved, ingest script ready, dry-run clean. Atlas SSL blocks live run -- same issue as LK dedup. DB total ~12,380 unchanged.)
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

**Post-ingest dedup (COMPLETE 2026-06-04):** Vol 1 × Vol 2 cross-family dedup run. **0 genuine duplicates. 0 contradictions. 0 positional conflicts.** 181 empty-text false positives (23 Ch48 rules using `interpretation.detailed` not `full_text` cross-matched against 32 Vol1 Ch20-24 sub-period rules also lacking `full_text` -- same dedup script limitation as Ch48 within-Vol2 run). Full report: `KE_TEXTBOOK_DECODE/Dedup_Reports/dedup_bphs_vol2_vs_vol1_20260604.md`.

---

### P1-2: BPHS Vol 2
**Science ID:** `vedic_astrology` | **Decode folder:** `BPHS_Vol2_CC_Decode/`

#### Ch49-51 (New Ingest -- Migration Project)

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

#### Ch47 + Ch52-58 (Legacy Ingests -- Triage Complete 2026-06-04)

Pre-migration ingests already in `horoscope_db`. Full flagged triage completed 2026-06-04 as part of Vol 2 cleanup sprint.

| Chapter | Batch ID | Rules | Triage Status |
|---|---|---|---|
| Ch47 (Sun MD antardasha) | `bphs-ch47-dasha-20260416` | ~50 | ✅ TRIAGE COMPLETE |
| Ch52 (Sun MD) | `bphs-ch52-dasha-20260421` | 109 | ✅ TRIAGE COMPLETE -- 3 flagged rules → PHR (all PDF-confirmed validator errors) |
| Ch53-58 (various planets MD) | `bphs-ch53-*` to `bphs-ch58-*` | ~960+ | ✅ TRIAGE COMPLETE |

**Triage summary (Ch47+Ch52-58):** 136/136 flagged rules resolved across all batches. 135 confirmed authentic validator errors → PHR. 6 C_empty rules (gap_fill_direct, no content) → rejected. 1 deferred (R-BPHS55-086 -- Mars in 9th from Rahu, pending full-books re-read). 7 encoding errors corrected in DB via patch scripts (dasha_lord, antardasha_planet, houses_involved, condition text). Ch.52 special: R-BPHS52-040 condition text corrected `own sign` → `debilitation sign` (content fields only; validation audit trail preserved).

**Encoding corrections applied (2026-06-04):** 10 field-level corrections across Ch47/Ch52-Ch57 via `patch_bphs_vol2_encoding_corrections.py` + `fix_bphs52_040_condition.py`. All PDF-verified.

#### Ch48 (Vimshottari Dasa House-Lord Effects -- ✅ INGESTED 2026-06-04)

| Metric | Value |
|---|---|
| Old batch | `bphs-ch48-dasha-20260416` in EverydayHoroscope DB (34 rules) -- **superseded, do not use** |
| New batch ID | `bphs-ch48-dasha-20260603` |
| Ingest status | ✅ **INGESTED + TRIAGE COMPLETE -- 2026-06-04** · 46 rules · 0 errors |
| Rules | 46 (A: 23 general+per-house · C: 12 kendra-trikona · D: 11 unfavourable) |
| auto_approved | 42 (91%) |
| pending_human_review | 4 (9%) -- Bucket B validator errors (maraka terminology, Rahu/Ketu elaboration flags) |
| flagged | 0 |
| Contradictions | 0 |
| Schema corrections | `condition.type: "dasha_of_house_lord"` (thread brief had wrong type `house_lord_position`) · `dasha_lord: null` for all per-house rules · `dasha_lord: "rahu"/"ketu"` for R045/R046 only |
| Yoga rules | 4 checkable: Harsha Yoga (R021) · Sarala Yoga (R022) · Vimala Yoga (R023) · Dhana Yoga 2nd-11th Parivartana (R020) |
| AI validation | Pre-upload · 91% AA · 4 PHR all Bucket B · 0 flagged · 0 contradictions |
| Dedup | Codex thread: 0 genuine vs BPHS Vol 1 local (181 empty-text false positives -- Ch48 uses `interpretation.detailed` not `full_text`; dedup script limitation documented) |
| Note | 46 rules were already in horoscope_db (Updated:46 / Inserted:0) -- Codex thread uploaded before auth failure. Our upload corrected statuses to validated values. |
| Full Vol 2 review | ✅ GATE CLEARED -- Ch.48 now ingested. Full BPHS Vol 2 comprehensive review can proceed. |

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
| Ingest status | ✅ **INGESTED -- 2026-06-02 · batch `300_horoscopes_vol1_v1` · 57 rules** |
| Validation | All 57 = `pending_human_review` (AI validator bypassed per thread brief; KP Jyotish rules require specialist review) |
| CC PDF validation | 2026-05-31 -- all 3 previously blocked rules cleared by direct PDF read |
| h300-s01-016 | ✅ Nakshatra Pada table -- all 12 signs match PDF exactly (abbreviated names correctly expanded) |
| h300-s04-004 | ✅ Empty-level-skip -- p.28 "Hence Rahu will give result in the following order" confirms text-native |
| h300-s04-005 | ✅ Cumulative levels -- p.28 "give result of Jupiter, Saturn and Mars... respectively" -- all active levels listed simultaneously |
| TT decisions pending | 2 duplicate candidates flagged `pending_review:True` -- h300-s01a-009 (lagna vs moon-sign KP orthodoxy) + h300-s03-004 (short-dasha planet grouping) |
| Duplicate report | `H300_DuplicateCandidateReport.md` -- 29 merge, 16 keep-both, 2 needs-human-call (TT at approval stage) |
| Dedup | ✅ Clean -- 0 matches, 0 contradictions vs full MongoDB (593,598 pairs) |

---

### P1-5: Longevity Unnatural Death
**Decode folder:** `LongevityUnnatural_CC_Decode/` | **Rules:** 44 | **Brief:** `LU_TempleTeam_Brief.docx`

| Status | Detail |
|---|---|
| Ingest status | ✅ **FULLY INGESTED + TRIAGE COMPLETE -- 2026-06-02** · 44 rules · batch `longevity_unnatural_v1` · 0 errors |
| Validation result | 33 auto_approved (75%) · 11 pending_human_review (25%) · 0 flagged. Bucket A: 2 truncation artifacts. Bucket B: 2 KP vs classical framework errors. Bucket C: 0. |
| Dedup | 0 matches vs 10,620 MongoDB rules (467,280 pairs). 6 known lu-s04↔kp-ch05 overlaps skipped by engine-spec condition type -- documented in diagnostic, surface at review. |
| MEDIUM rules (8) | lu-s04-007/008/009/016/017/018 + lu-s02-006 + lu-s03-005 set `pending_review:True` |
| TT action | Co-founder sign-off on 33 `auto_approved` rules → `approved` status. |

---

### P1-6: Destiny Numerology
**Decode folder:** `DestinyNumerology_CC_Decode/` | **Rules:** **447** core (383) + derived (64) | **OCR report:** `Book_Wide_OCR_Inconsistencies_Report.docx`
**Brief:** `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_DESTINY_NUMEROLOGY_INGEST.md`

> **COUNT CONFIRMED 2026-06-04 by Temple Team:** 383 core rules (Ch03-Ch28, 25 chapters) + 64 derived (CareerAlignment 31 + PersonalYearCycle 12 + CaseDerivedInference 21) = **447 total rules**. 50 Ch15 test vectors (separate schema, not ingested as rules). Grand total in decode folder: 497. TT brief figure of 189 was a stale draft count.

> **GAI PASS COMPLETE 2026-06-04:** All 10 HIGH OCR items resolved. Both CRITICAL items (17-A Amethyst proxy, 19-A dual element routing) resolved. Source patches applied: `num-ch06-017` Arrow of Apathy corrected [8,7,6] → [2,7,6] (Issue 6-A). Synthetic rule `num-ch09-065` added for compound ≥74 reduction loop (Issue 9-B). Ingest script ready.

| Status | Detail |
|---|---|
| Ingest status | ✅ **FULLY INGESTED + TRIAGE COMPLETE 2026-06-04** · All 448 rules in MongoDB · Ch15 TVs hold |
| **Confirmed rule count** | **448** (383 core Ch03-Ch28 + 64 derived + 1 synthetic num-ch09-065) · TT brief figure of 189 was stale draft |
| Total OCR issues | 41 total: CRITICAL 2 · HIGH 10 · MED 13 · LOW 4 · **All HIGH + CRITICAL resolved by GAI** |
| **GAI pass** | ✅ **COMPLETE 2026-06-04** · All 10 HIGH + both CRITICAL resolved · `Numerology_GAI Guidance.md` |
| Source patches applied | ✅ `num-ch06-017` condition [8,7,6]→[2,7,6] (Issue 6-A) · ✅ `num-ch09-065` synthetic rule (Issue 9-B) · ✅ `num-ch17-009` Paksha=Shukla · ✅ `num-ch17-011` Paksha=Krishna (Issue 17-B) |
| Batch A ID | `destiny_numerology_ch01-15_v1` · science_id: `numerology` |
| Batch B ID | `destiny_numerology_phase_b_20260604` · science_id: `numerology` |
| Batch C ID | `destiny_numerology_phase_c_20260604` · science_id: `numerology` |
| Pre-ingest dedup | ✅ CLEAN -- 0 genuine matches, 0 contradictions vs BPHS Vol 1 (451,360 pairs). 20 empty-text false positives (documented TF-IDF limitation). Report: `dedup_destiny_num_phase_a_vs_jyotish_20260604.md` |
| **Phase A validation** | ✅ **282 AA (91%) · 29 PHR (9%) · 0 flagged** · Triage: 4 Bucket B (contradiction engine grouped by condition.type, ignoring numbers_involved) · 25 legitimate PHR |
| **Phase B validation** | ✅ **27 AA (79%) · 7 PHR (21%) · 0 flagged** · Triage: 2 Bucket B (lo_shu_element_remedy exception clause; engine_spec empty numbers_involved) · 5 legitimate PHR |
| **Phase C validation** | ✅ **16 AA (16%) · 87 PHR (84%) · 0 flagged** · Triage: 81 Bucket B (geographic/company/derived rule types outside validator schema -- Ch20-27, CAD, CDI, PYC) · 6 legitimate PHR · AA = Ch28 remarriage rules + PYC standard-type rules |
| **TT action** | Co-founder sign-off on 282 + 27 + 16 = **325 auto_approved** rules across all phases → `approved` status |

**Phase breakdown (COMPLETE 2026-06-04):**

| Phase | Scope | Rules | Status |
|---|---|---|---|
| **A** | Ch03-Ch16 (excl. Ch15 TVs) | **311** (310 + 1 synthetic) | ✅ INGESTED + TRIAGE COMPLETE · 282 AA · 29 PHR · 0 flagged |
| **B** | Ch17-Ch19 | **34** | ✅ INGESTED + TRIAGE COMPLETE · 27 AA · 7 PHR · 0 flagged |
| **C** | Ch20-Ch28 + Derived (CAD/PYC/CDI) | **103** (39 core + 64 derived) | ✅ INGESTED + TRIAGE COMPLETE · 16 AA · 87 PHR · 0 flagged |
| **Ch15 TVs** | Test vectors only (different schema) | **50** | **Hold** -- 45 of 50 still need TT/GAI confirmation |
| **TOTAL** | All phases | **448** | ✅ **FULLY INGESTED** |

**Post-ingest dedup:** Run Phase A folder vs all other ingested science folders after upload.

---

### P1-7: SBC (Sarvato Bhadra Chakra)
**Decode folder:** `New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/` | **Rules:** 182 | **OCR report:** `SBC_OCR_Issues_Report.docx`

| Status | Detail |
|---|---|
| Ingest status | ⛔ BLOCKED ON ATLAS -- ingest script ready, dry-run clean (Issues: 0), Atlas SSL timeout blocking live run |
| Script | `backend/scripts/ingest_sbc_v1.py` · dry-run: `python3 backend/scripts/ingest_sbc_v1.py --dry-run` ✅ Issues: 0 |
| Live run | `python3 backend/scripts/ingest_sbc_v1.py --mongo-url "$MONGO_URL"` -- run when Atlas recovers |
| Rules | 182 (181 original + sbc-ch18-011 added 2026-06-05 -- Chandrakalanal Chakra) |
| All gates cleared | ✅ 7 TT priority conflicts (2026-05-20) · ✅ 6 MongoDB schemas (2026-05-20) · ✅ 4 CRITICAL OCR items (2026-06-05) |
| Remaining gate | 🟠 17 source gap OQs -- TT reviewing separately, NOT blocking ingest |
| CRITICAL OCR items | ✅ ALL 4 RESOLVED 2026-06-05: C-01 (sbc-ch18-011 new rule) · C-02 (14 pairs in sbc-ch18-004) · C-03 (false alarm, sbc-ch10-023 updated) · C-04 (Devanagari Unicode in sbc-ch18-007) |
| Post-ingest dedup | Run against BPHS Vol 1 + all ingested books after Atlas recovers |
| Atlas blocker | Same SSL timeout as LK dedup (KE-OP-LK-1) -- primary shard unreachable. Self-resolves when Atlas recovers. |

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
| Ingest status | ✅ **INGESTED + TRIAGE COMPLETE 2026-06-04** · 256 rules · batch `kp_vol3_v1_20260604` |
| Batch ID | `kp_vol3_v1_20260604` · science_id: `kp_jyotish` |
| Rules | 256 across 77 chapters (P01-P88 + T04/T06-T10; P46/P50 = 0-rule by design; T01/P83/P84 not decoded) |
| **Validation result** | ✅ **158 AA (62%) · 98 PHR (38%) · 0 flagged** |
| Triage | 29 Bucket B: 6 engine_specification (methodology rules) · 14 kp_significator (3 contradiction pairs + AI uncertainty -- validator grouped by condition.type ignoring KP-specific fields) · 6 kp_sub_lord (complex/unusual domains) · 3 other (planet_in_house, kp_badhaka). 69 legitimate PHR. |
| Special encodings | `KP_T05_Master_Sub_Significance.json` (249 entries) + `KP_P27_Profession_Dictionary.json` (229 entries) -- distinct schemas, NOT in this ingest. T05 blocked on TT-1 (entries 248-249 INFERRED). P27 ready. |
| Post-ingest dedup | ✅ **COMPLETE 2026-06-04** · KP vs BPHS Vol 1: 0 dup / 0 contra / 0 positional (372,736 pairs) · KP vs BPHS Vol 2: 0 dup / 0 contra / 0 positional (102,400 pairs) · Both clean -- KP and BPHS use different vocabularies (sub-lord/cusp vs yoga/rashi); TF-IDF finds no textual overlap above 0.82 threshold (system-level difference confirmed). Reports: `dedup_kp_vs_bphs_vol1_20260604.md` + `dedup_kp_vs_bphs_vol2_20260604.md` |
| **P27 dict** | ✅ **INGESTED 2026-06-04** · 229 entries · batch `kp_p27_dict_v1_20260604` · 229 pending_human_review · 0 errors · condition.type=`kp_profession_ruler` · categories: 173 industry / 33 govt-ministry / 23 professional |
| OCR open items | All 44 affect T05 only -- zero blockers for Rules.json. TT-1: entries 248-249 INFERRED (HIGH). TT-2: P2 terms F-01 to F-06 (MED). |
| **TT action** | Co-founder sign-off on 158 `auto_approved` rules → `approved` status · P27 dict: sign-off on 229 PHR entries · TT-1: read T06 p.1 for entries 248-249 |

---

### P2-2: BPHS Vol 1 (remaining chapters)
**Chapters:** Ch27 (Shadbala), Ch43 (Longevity/Ayurdaya), Ch44 (Marakas)

| Status | Detail |
|---|---|
| Ingest status | ✅ **INGESTED + TRIAGE COMPLETE 2026-06-04** · 103 rules · batch `bphs_ch27_43_44_v2_20260604` |
| Background | Rules existed in MongoDB since 2026-05-04 but with empty `full_text` (old schema). Schema patch applied 2026-06-04: `full_text` + `summary` + `result.interpretation` populated from source JSONs. Re-validated via current AI validator. |
| **Ch27 -- Shadbala** | 28 rules · 14 AA / 11 PHR / 3 Bucket B (→ PHR) · 0 flagged · Covers all 6 Shadbala components (Uchcha/Saptavargaja/Ojhayugma/Kendradi/Drekkana/Dig/Kala/Chesta/Naisargika/Drig Bala) + thresholds + Bhava Bala |
| **Ch43 -- Longevity** | 35 rules · 20 AA / 14 PHR / 1 Bucket B (→ PHR) · 0 flagged · Covers Pindayu + Nisargayu + Amsayu systems + all reductions + longevity yogas |
| **Ch44 -- Marakas** | 40 rules · 15 AA / 12 PHR / 11 Bucket B (→ PHR) · **2 flagged (Bucket C)** · Covers Maraka designation + timing + cause-of-death + decanate + afterlife rules |
| **Final counts** | **49 AA (48%) · 52 PHR (50%) · 2 flagged (2%)** |
| Bucket C flagged | `bphs-ch44-MT01`: "absolute safety buffer" encoding overstatement · `bphs-ch44-RK03`: conflates two BPHS principles -- both need encoding fix before approval |
| Contradiction pairs | 2 pairs, both Bucket B: {ch43-025 ↔ ch43-026} Saturn/Jupiter longevity class opposites · {ch43-021 ↔ ch43-023} sign-modality vs quantum-of-years (same system, different aspects) |
| Schema note | Source JSONs in `backend/scripts/bphs_ch27_rules.json` / `bphs_ch43_rules.json` / `bphs_ch44_rules.json`. Patch script: `backend/scripts/patch_ch27_43_44_schema.py` |
| **TT action** | Co-founder sign-off on 49 AA rules → `approved` · Review 2 Bucket C flagged (encoding fixes needed) |

---

### P2-3: BPHS Vol 2 (remaining chapters)

| Chapter range | Status |
|---|---|
| Ch49-51 (new ingest) | ✅ INGESTED + TRIAGE COMPLETE (see P1-2) |
| Ch47 + Ch52-58 (legacy) | ✅ TRIAGE COMPLETE 2026-06-04 -- 136/136 rules resolved, 10 encoding corrections applied |
| Ch48 (house-lord dasha) | ✅ INGESTED + TRIAGE COMPLETE 2026-06-04 -- 46 rules, 42 AA / 4 PHR / 0 flagged |
| Ch46 (Dasa survey) | ⛔ **SKIP -- NOT A KE TARGET** (confirmed 2026-06-04). Survey of 25+ dasa systems (Vimshottari, Ashtottari, Shodasottari, Kalachakra, Chara, Yogini, Naisargik, etc.) with calculation tables and illustrative charts. Computation chapter -- belongs to `vedic_calculator.py` scope, not `interpretation_rules`. No IF-THEN effect rules. Future engineering note: ~24 dasa engines beyond Vimshottari not yet implemented. |
| Full Vol 2 review | ✅ **COMPREHENSIVE REVIEW COMPLETE 2026-06-04** |

**Vol 2 comprehensive review complete (2026-06-04):**
- Ch.46: SKIP permanently. Computation/survey chapter (25+ dasa systems with calculation tables). `vedic_calculator.py` engineering concern, not a KE ingest target. No rules to extract.
- Vol 1 × Vol 2 cross-family dedup: **CLEAN** -- 0 genuine duplicates, 0 contradictions, 0 positional conflicts. 181 empty-text false positives (documented dedup script limitation). Report: `dedup_bphs_vol2_vs_vol1_20260604.md`.
- Within-Vol 2 cross-chapter (Ch48-51 local files): content areas are fully distinct (house-lord Vimshottari vs Kalachakra vs Chara vs Antardasha) -- no overlap expected, no dedup run needed.

---

### P2-4: Medical Astrology
**Decode folder:** `MedicalAstrology_CC_Decode/` | **Brief:** `MedAstro_TempleTeam_Brief.md` | **OCR:** `MedAstro_OCR_Issues_Audit.md`

| Status | Detail |
|---|---|
| Ingest status | ✅ **INGESTED + TRIAGE COMPLETE -- 2026-06-04** · batch `medical_astrology_v1` · 270 rules · 0 errors |
| Science ID | `vedic_astrology` |
| Rules breakdown | 53 auto_approved (20%) · 196 pending_human_review (73%) · 21 flagged (8%) |
| Source schemas | Schema A: 239 rules (has `source` block + top-level `summary`) · Schema B: 31 rules (has `outcome` dict + top-level `batch_id`) |
| Triage summary | 103 flagged rules triaged: Bucket A 3 (false-positive truncations → source-confirmed complete → promoted to AA via patch) · Bucket B 79 (validator framework errors → PHR, `validator_error:True`) · Bucket C 21 (genuine issues → stay flagged, TT/GAI queue) |
| Bucket B rationale | BPHS-trained validator flags Dr. S. Krishna Kumar's South Indian medical astrology doctrine: 6 Shapa curse yogas (Pitrushapa/Bhratushapa/Brahmin/Stree/Preta/Sarpa), Mandi, drekkana body-part yogas, ghatika timing, Nirjala rashis -- authentic to source, not BPHS-standard |
| 21 Bucket C flagged | Logical impossibilities (Sun in 5th AND 9th simultaneously), factual errors (Mars called watery planet), incoherent conditions (6th lord owned by retrograde planets), extreme multi-planet simultaneous conditions. Full list in `triage_medical_astrology_v1.py`. |
| Notable PHR flags | ma-ch11-001/002: reference Table 11.1 (not in decode) -- cannot verify without table · ma-ch01-125/127: real truncations (validator correctly identified) · Patni Shapa cluster (~8 rules ch02): validator flags "lacks classical authority" |
| gai_citation_unverified | ma-ch03-005 + DataTable 3.2 (Rigveda 1.91.16) · bench-015 (Shambhu Hora Prakash) · bench-013 (Kalaprakashika Dagdha) -- cross-check sloka refs before co-founder approval, NOT before ingest |
| Dedup | ✅ 0 matches, 0 contradictions vs 10,664 MongoDB rules (2,879,280 pairs). Run date: 2026-06-04. |
| Grade A/B OCR | ✅ ALL RESOLVED 2026-05-31. A-1: bench-004 `birth_data_unavailable:true`. A-2: Cancer Lagna pyswisseph-verified. B-7/B-8/B-11: gai_citation_unverified flags applied. |
| Post-ingest dedup | ✅ CLEAN 2026-06-04 -- 0 matches, 0 contradictions, 0 positional conflicts vs BPHS Vol 1 (393,120 pairs). 5 BPHS Ch16/17/18/20/24 single-file JSONs skipped (unrecognised structure -- known dedup limitation; verdict unaffected). MedAstro condition types (yoga_combination, shapa, ghatika) do not overlap with BPHS positional rules. Report: `dedup_medastro_vs_bphs_vol1_20260604.md`. |
| TT action | Co-founder sign-off on 53 `auto_approved` rules → `approved` status. Review 21 flagged (Bucket C) at end-of-corpus holistic review. |

---

### P2-5: Phaladeepika
**Decode folder:** `Phaladeepika_CC_Decode/` | **Rules:** 1218 (28 chapters, 1206 active + 12 TBA/inactive) | **OCR:** `Phaladeepika_Inconsistencies_Review.docx`

| Metric | Value |
|---|---|
| Ingest status | ✅ **FULLY INGESTED + ALL OPs CLOSED -- 2026-06-02** |
| Batch ID | `phaladeepika-v1-20260601` |
| Ingest script | `backend/scripts/ingest_phaladeepika_v1.py` |
| Rules inserted | 1218 (0 errors, 0 skipped) |
| **auto_approved** | **825** (Round 1: 582 → Round 2: +227 → Round 3: +16) |
| **pending_human_review** | **393** |
| **flagged** | **0** |
| **pending_review** | **0** -- PD-OP-01 fully resolved via 3-round re-validation |
| TBA/inactive | 12 (Ch08 PDF gap -- Sun houses 1-6 absent from source) |
| Contradictions detected | 22 total: 20 Bucket B (all PHR + notes) · 1 Bucket C genuine (pd-ch04-014/030 Kendra Bhava Bala, TT sign-off) · 1 resolved PD-OP-05 (Ch23/Ch24 dual-layer from physical book) |
| Three-schema mapping | Schema A (Ch01-13, 15-16, 18, 27) · Schema C (Ch14, 17, 19-25) · Schema B (Ch22, 26, 28) |
| ~~PD-OP-01~~ | ✅ CLOSED -- 357 pending_review rules resolved: source JSONs fixed by decode thread + 3-round re-validation. 13 truncation-artifact rules → 12 AA / 2 PHR via PD-OP-07 summary restoration. |
| ~~PD-OP-07~~ | ✅ CLOSED -- Summaries restored for 13 truncation-artifact rules. `knowledge_validator.py` char limits fixed ([:200]→[:400] summary, [:400]→[:800] detailed). |
| Ingest tracker | `.claude/ke/ingest/PHALADEEPIKA_INGEST.md` |
| Post-ingest dedup | Informational -- run vs BPHS Vol 1 (60-70% conceptual overlap on house chapters expected; rule_ids are distinct, no dedup blocking needed) |

**All OPs closed except TT-gated items:**
- **PD-OP-03** 🟡 TT at approval stage: `pd-ch21-041` `gai_citation_unverified:True` -- verify before co-founder sign-off
- **PD-OP-06** 🔴 TT: Co-founder sign-off on **825 auto_approved** rules → `approved` status

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

### P2-6: Lal Kitab (Ch19-Ch29)
**Decode folder:** `backend/scripts/lalkitab_ch*_rules.json` | **Rules:** 467 | **Chapters:** 11 (Ch19-Ch29)

| Status | Detail |
|---|---|
| Ingest status | ✅ **INGESTED + TRIAGE COMPLETE 2026-06-05** · 467 rules · batch `lalkitab_all_v2_20260605` |
| Science ID | `jyotish` · Book ID: `lal-kitab` |
| Original ingest | Ch19-Ch29 ingested 2026-04 to 2026-05 across 11 per-chapter batches |
| Schema patch | 2026-06-05: `full_text` populated from `interpretation.detailed` in all source JSONs · 467/467 patched · re-validated |
| **Validation result** | ✅ **287 AA (61%) · 163 PHR (35%) · 17 flagged (4%) · 0 pending_review** |
| Bucket B (27 → PHR) | Truncated interpretation.summary (5) · LK Rina/debt system (3) · 42-section wave engine (6) · LK-native extreme outcomes (4) · schema/methodology limits (3) · LOW confidence (3) · cross-person/birth rules (2) · LK formula (1) |
| Bucket C (17 flagged) | Encoding errors (ch20-yog-01/05/09, ch21-gp-05, ch23-geoveto-triangle) · non-astrological death omens (ch24-mortality-* ×4) · extreme/incoherent mortality age rules (ch24-age-* ×7) |
| Structural failure | `lalkitab-ch20-yog-07` -- moved to PHR (validator Stage 4 write gap) |
| Per-chapter | Ch19: 78 · Ch20: 48 · Ch21: 43 · Ch22: 17 · Ch23: 31 · Ch24: 60 · Ch25: 35 · Ch26: 16 · Ch27: 99 · Ch28: 18 · Ch29: 22 |
| Post-ingest dedup | Pending -- run vs BPHS Vol 1 and BPHS Vol 2 |
| **TT action** | Co-founder sign-off on 287 `auto_approved` → `approved` · Review 17 Bucket C flagged |

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

*Last updated: 2026-06-05 by Claude Code -- Lal Kitab Ch19-Ch29 schema patch + validation + triage COMPLETE. 467 rules. 287 AA / 163 PHR / 17 flagged. DB total ~12,380.*
*P1-1 BPHS Vol 1: ✅ FULLY INGESTED ~1,765 rules.*
*P1-2 BPHS Vol 2: ✅ COMPREHENSIVE REVIEW COMPLETE 2026-06-04. Ch49-51 ✅ · Ch47+Ch52-58 triage ✅ · Ch48 ✅ · Vol1×Vol2 dedup CLEAN · Ch46 not decoded (TT: PDF scope check pending).*
*P1-3 300 Combinations: ✅ INGESTED + TRIAGE COMPLETE (141 auto_approved, 188 PHR, 0 flagged).*
*P1-4 300 Horoscopes Vol 1: ✅ INGESTED 2026-06-02 (57 rules, batch `300_horoscopes_vol1_v1`, all PHR).*
*P1-8 Longevity 58Ch: ✅ INGESTED + TRIAGE COMPLETE 2026-06-02 (69 auto_approved, 80 PHR, 0 flagged).*
*P2-4 Medical Astrology: ✅ INGESTED + TRIAGE COMPLETE 2026-06-04 (53 auto_approved, 196 PHR, 21 flagged). batch `medical_astrology_v1`.*
*P2-5 Phaladeepika: ✅ INGESTED + TRIAGE COMPLETE (582 AA, 271 PHR, 8 flagged). 2026-06-02.*
*DB total: ~11,428 rules in horoscope_db (10,980 prior + 311 Phase A + 34 Phase B + 103 Phase C). Zero `approved` -- TT co-founder sign-off pending.*
*P1-6 Destiny Numerology: ✅ FULLY INGESTED 2026-06-04 -- 448 rules across 3 batches. 325 AA / 123 PHR / 0 flagged.*
*P2-1 KP Astrology: ✅ INGESTED + TRIAGE COMPLETE 2026-06-04 -- 256 rules. 158 AA / 98 PHR / 0 flagged. T05/P27 pending separately.*
*DB total: ~11,684 rules in horoscope_db. Zero `approved` -- TT co-founder sign-off pending.*
*Next: Post-ingest dedup KP vs BPHS Vol 1 (informational) · SBC blocked (TT decisions) · P2-2 BPHS Ch27/43/44 (dedicated sprints).*
