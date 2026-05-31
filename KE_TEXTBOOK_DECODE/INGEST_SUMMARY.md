# KE Ingest Summary -- All Books
> Single source of truth for ingest status across all Phase 1 and Phase 2 books.
> Last updated: 2026-05-30
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
**Science ID:** `vedic_astrology` | **Decode folder:** `BPHS_CC_Decode/`

| Metric | Value |
|---|---|
| Chapters decoded | 37 of 45 |
| Total rules | ~1,456 |
| Active rules | ~1,456 (all active) |
| Chapters skipped | 6 (Ch01, Ch02 mythology; Ch27, Ch43, Ch44 dedicated sprint; Ch34, Ch40 absorbed) |
| Ingest status | 🟢 HIGH ITEMS RESOLVED -- Rule file updates pending, then READY |
| GAI session | 2026-05-30 -- all 10 items resolved in one session |
| GAI resolution log | `BPHS_CC_Decode/BPHS_Vol1_GAI_Resolutions.md` |
| Engine code | `BPHS_CC_Decode/BPHS_Vol1_Engine_Core.py` (validated ✅) |

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

**Remaining MED items (do not block ingest -- resolve post-ingest or in parallel):**

| ID | Priority | Chapter | Issue |
|---|---|---|---|
| TT-CH30-02 | 🟠 MED | Ch30 | Nasal disorder sign qualifier (Mars+Saturn alone or with sign?) |
| TT-CH30-03 | 🟠 MED | Ch30 | Upa Pada computation chain counting method |
| TT-CH06-02 | 🟠 MED | Ch06 | Shashtiamsa formula precision -- integer or fractional degrees |
| TT-CH09-02 | 🟠 MED | Ch09 | Oriental/occidental half definition for Vajra Mushti |
| TT-CH31-02 | 🟠 MED | Ch31 | Quarter-degree Argala rule for 3rd/4th quarters |

**Next step:** Ingest Thread applies GAI resolutions to affected rule JSON files → re-verify with `BPHS_Vol1_Engine_Core.py` → ingest.

**Post-ingest dedup targets:** BPHS Vol 2 (same text family -- dedup before or at ingest)

---

### P1-2: BPHS Vol 2
**Science ID:** `vedic_astrology` | **Decode folder:** `BPHS_Vol2_CC_Decode/`

| Metric | Value |
|---|---|
| Chapters decoded | 3 (Ch49, Ch50, Ch51 -- Dasa chapters) |
| Total rules | 229 |
| Active rules | 224 |
| OCR-limited (inactive) | 5 (Virgo, Libra, Gemini Pada 7/9, Scorpio, Aquarius Padas) |
| Ingest status | 🔴 BLOCKED -- OCR items must close first |
| GAI query file | `BPHS_Vol2_CC_Decode/BPHS_Vol2_GAI_OpenItems_Query.md` |

**Open Items:**

| ID | Priority | Chapter | Issue |
|---|---|---|---|
| Ch49-Virgo | 🔴 HIGH | Ch49 | Virgo Padas 1-9 outcomes -- full block missing |
| Ch49-Libra | 🔴 HIGH | Ch49 | Libra Padas 1-9 outcomes -- full block missing |
| Ch49-Gemini-P7 | 🟠 MED | Ch49 | Gemini Pada 7 sign outcome -- OCR unclear |
| Ch49-Gemini-P9 | 🟠 MED | Ch49 | Gemini Pada 9 -- missing entirely from PDF |
| Ch49-Scorpio | 🟠 MED | Ch49 | Scorpio Padas 1-2 outcomes -- OCR unclear |
| Ch49-Aquarius | 🟠 MED | Ch49 | Aquarius Padas 7-8 outcomes -- OCR unclear |
| Ch49-Remedies | 🟡 LOW | Ch49 | Specific mantra/deity names for malefic Kalachakra periods |
| Ch50-Combust | 🟡 LOW | Ch50 | Confirm combust condition in rule 041 per sloka 61 |
| Ch51-Bhoga | 🟡 LOW | Ch51 | Bhoga Rasi algorithm -- verify correct capture |

**Post-ingest dedup targets:** BPHS Vol 1 (internal cross-check -- same source text)

---

## Phase 1 -- Additional Books (approved sequence)

### P1-3: 300 Combinations
**Decode folder:** `ThreeHundredCombinations_CC_Decode/` | **Rules:** 300 | **Open items:** None

| Status | Detail |
|---|---|
| Ingest status | ✅ READY -- start now, no blockers |
| Action | Run ingest script per `HANDOVER_SUMMARY.md` in decode folder |
| Post-ingest dedup | Run against BPHS Vol 1 + Vol 2 (when ingested) |

---

### P1-4: 300 Horoscopes Vol 1
**Decode folder:** `ThreeHundredHoroscopes_CC_Decode/` | **Rules:** 57 (3 blocked) | **OCR report:** `H300_OCR_Issues_Report.docx`

| Status | Detail |
|---|---|
| Ingest status | 🟠 PARTIAL BLOCKER -- 3 rules need TT decision |
| Blocked rules | h300-s01-016 · h300-s04-004 · h300-s04-005 |
| Action | TT reviews each blocked rule → approve/reject/modify. 54 clean rules can ingest immediately. |
| NLM/GAI priority queries | Issues 7, 13, 19 from OCR report (copy-paste ready in Section 5) |
| Post-ingest dedup | Run against BPHS Vol 1 + Vol 2 (when ingested) |

---

### P1-5: Longevity Unnatural Death
**Decode folder:** `LongevityUnnatural_CC_Decode/` | **Rules:** 44 | **Brief:** `LU_TempleTeam_Brief.docx`

| Status | Detail |
|---|---|
| Ingest status | 🔴 BLOCKED -- 5 HIGH OCR items for NLM/GAI first |
| Key blockers | lu-s04-001 ("must" vs "should" gate) · lu-s04-014 (AND vs OR logic) · lu-s04-003/004 (5-level chain) · lu-s04-010 (lethal planet definition) · CS1 Mercury coordinate |
| Action | NLM/GAI resolves HIGH items → TT decides on lu-s04-001 and lu-s04-014 architecture choices |
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
| Ingest status | 🔴 HARD BLOCKED -- Co-founder sign-off on aayu bucket methodology required |
| Decode status | ✅ All 58 chapters accounted for (Ch4/5 via NLM, Ch6-Ch58 via CC) |
| Blocker | Aayu bucket methodology (longevity span calculation approach) not yet approved |
| Action | TT gives explicit co-founder approval → then ingest begins |
| Note | Do NOT begin this ingest without the explicit sign-off. ~600 rules. |
| Post-ingest dedup | Run against all ingested books -- expected cross-text flags with BPHS Ch43/44 (longevity chapters) |

---

## Phase 2 -- After Phase 1 BPHS Complete

> Start Phase 2 only after BPHS Vol 1 + Vol 2 are ingested. Each Phase 2 book is deduped against BPHS as its primary cross-reference.

### P2-1: KP Astrology
**Decode folder:** `KP_CC_Decode/` | **Rules:** 256 / 77 files | **Brief:** `KP_Vol3_Temple_Brief.md`

| Status | Detail |
|---|---|
| Ingest status | 🟠 NEAR READY |
| Open items | Verify entries 248-249 (read T06 page 1) · claim_axis retroactive pass on ~20 rules |
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
| Ingest status | 🔴 BLOCKED -- 2 Grade A CRITICAL OCR items |
| CRITICAL | Chart IX zero birth data (bench-004 unverifiable) · "17/46" annotation (could change bench-009 entirely) |
| OCR total | 81 issues: 2 Grade A · 11 Grade B · 7 Grade C · 61 Grade D |
| Action | Resolve Grade A items first (NLM/GAI + original chart verification) → then Grade B → ingest |
| Post-ingest dedup | BPHS Vol 1 (medical astrology principles derive from BPHS planetary significations) |

---

### P2-5: Phaladeepika
**Decode folder:** `Phaladeepika_CC_Decode/` | **Rules:** 743 (16 chapters, Tiers 1-3) | **OCR:** `Phaladeepika_Inconsistencies_Review.docx`

| Status | Detail |
|---|---|
| Ingest status | 🔴 BLOCKED -- Tier 4 decode pending + 6 HIGH OCR items |
| Decode status | Tiers 1-3 complete (743 rules / 16 chapters). Tier 4 (3 chapters) still pending. |
| OCR total | 102 issues: 6 HIGH · 27 MED · 69 LOW · 4 unresolved |
| GAI priorities | Top 8 items in Section 5 of OCR report (pre-written queries) |
| Action | Complete Tier 4 decode → resolve 6 HIGH OCR items → ingest Tiers 1-3 first, Tier 4 separately |
| Post-ingest dedup | BPHS Vol 1 (Phaladeepika directly references BPHS -- expect both agreements and contradictions) |
| Note | Cross-text matches with BPHS are expected to be the richest in the entire KE -- Phaladeepika is a commentary tradition on BPHS. |

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

*Last updated: 2026-05-30 by Claude Code Main Thread*
