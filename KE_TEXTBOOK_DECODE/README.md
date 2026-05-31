# KE Textbook Decode & Ingest
## Complete Reference for All Book Decode Activities

> EverydayHoroscope -- Knowledge Engine
> Last updated: 2026-05-29

---

## What This Folder Is For

This folder contains all documentation for decoding classical Vedic astrology texts into the Knowledge Engine rule database. It is the single reference point for:
- NLM decode threads starting a new book
- Temple Team managing decode progress and schema decisions
- Engineers building the ingest, dedup, and contradiction detection pipeline

---

## Folder Structure

```
KE_TEXTBOOK_DECODE/
├── README.md                          ← You are here -- start here for any new work
├── KE_Book_Decode_Process_Technical.md ← Full technical process guide (read first)
├── KE_NewBook_Thread_Start_Template.md ← Copy-paste template for issuing a new decode thread
├── KE_Ingest_Sequence_Approved.md      ← Approved ingest order for all books
├── KE_NewBooks_A2_Planning_Task.md     ← A2 planning: next 10 books + priority
├── KNOWLEDGE_ENGINE_ROADMAP.md         ← KE product roadmap
├── KNOWLEDGE_ENGINE_STRATEGY.md        ← KE strategy document
│
├── Decode_Guides/                      ← One guide per book (active decode threads use these)
│   ├── KE_Longevity_Decode_Guide.md
│   ├── KE_MedicalAstrology_Decode_Guide.md
│   ├── KE_DestinyNumerology_Decode_Guide.md
│   ├── KE_ThreeHundredHoroscopes_Decode_Guide.md
│   ├── BPHS_Vol1_Decode_Guide.md
│   ├── BPHS_Vol2_JSON_Conversion_Guide.md
│   ├── KP_Astrology_Decode_Guide.md
│   └── Phaladeepika_Decode_Guide.md
│
├── Thread_Briefs/                      ← Status briefs for active decode threads
│   ├── THREAD_BRIEF_PHALADEEPIKA_NLM.md   ← IN PROGRESS -- 11 chapters / 605 rules · Next: Adhyaya XV
│   ├── THREAD_BRIEF_BPHS_VOL1_DECODE.md   ← PARTIALLY COMPLETE -- Ch11-Ch24 done
│   └── THREAD_BRIEF_KP_DECODE.md          ← PRIMARY DECODE COMPLETE -- claim_axis pass pending
│
└── Schema_Docs/                        ← Schema decisions + encoding standards
    ├── PD_SCHEMA_FLAGS_GAI_CONSULTATION.md  ← Original 8 flags raised pre-Phaladeepika
    ├── PD_SCHEMA_FLAGS_ANSWERS.md           ← Resolved answers to all 8 flags
    ├── KE_CONTRADICTION_PAIR_SCHEMA.md      ← Encoding standard for contradiction pairs
    └── KE_RETROACTIVE_IMPACT_ASSESSMENT_PD1.md ← Impact of schema amendment on existing rules
```

---

## Key Scripts (for Engineers / New Threads)

| Script | Location | Purpose |
|---|---|---|
| `ke_dedup_script.py` | `backend/ke_dedup_script.py` | Cross-text dedup + contradiction detection (TF-IDF cosine similarity) |
| `ke_schema_constants.py` | `backend/ke_schema_constants.py` | Schema enum constants -- single source of truth |
| `knowledge_schema.py` | `backend/knowledge_schema.py` | Pydantic validation models for rule documents |
| `vedic_calculator.py` | `backend/vedic_calculator.py` | `compute_neechabhanga_flags()` -- pre-processor for Neechabhanga rules |

---

## Active Ingest Thread -- Current Status (as of 2026-05-30)

**KE Ingest Thread** owns Phase 1 + Phase 2 ingest. Handover guide: `Handover_Guides/HANDOVER_KE_INGEST_THREAD.md`

| Phase | Status |
|---|---|
| KE Freeze | ✅ LIFTED 2026-05-22 |
| Phase 2 decode | ✅ COMPLETE -- all 10 books decoded, OCR reports ready |
| Phase 1 ingest | 🟠 READY TO START -- 300 Combinations is Priority 1, no blockers |
| Phase 2 ingest | 🟡 AFTER Phase 1 sequence |

---

## All 10 Books -- Decode + Ingest Status

| Book | Decode | Rules | OCR Report | Ingest Priority | Blocker |
|---|---|---|---|---|---|
| 300 Combinations | ✅ Complete | 300 | None | Phase 1 -- Priority 1 | None -- start now |
| 300 Horoscopes Vol 1 | ✅ Complete | 57 | H300_OCR_Issues_Report.docx | Phase 1 -- Priority 2 | 3 blocked rules → TT decision |
| Longevity Unnatural Death | ✅ Complete | 44 | LU_OCR_Inconsistency_Review.docx | Phase 1 -- Priority 2 | 5 HIGH OCR items → NLM/GAI first |
| Destiny Numerology | ✅ Complete | 189 (Ch01-15) | Book_Wide_OCR_Inconsistencies_Report.docx | Phase 1 -- Priority 3 | Ch15 TVs confirmed complete |
| SBC | ✅ Complete | 181 | SBC_OCR_Issues_Report.docx | Phase 1 -- Priority 3 | 7 TT conflicts + 24 source gaps |
| Longevity 58 chapters | ✅ Complete | ~600+ | -- | Phase 1 -- LAST | Aayu bucket co-founder sign-off needed |
| KP Astrology | 🟡 Near complete | 256 / 77 files | KP_T05_OCR_Issues_Report.docx | Phase 2 -- P2-1 | Entries 248-249 verify; claim_axis pass |
| BPHS Vol 1 | 🟡 Partial (Ch11-24) | 200+ | BPHS_Vol1_OCR_Issue_Register.docx | Phase 2 -- P2-2 | Tier 4 decode + Category D TT decision |
| BPHS Vol 2 | ✅ Complete | TBD | BPHS_Vol2_OCR_Inconsistency_Report.docx | Phase 2 -- P2-3 | 9 next actions in brief |
| Medical Astrology | ✅ Complete | TBD | MedAstro_OCR_Issues_Audit.md | Phase 2 -- P2-4 | 2 Grade A CRITICAL resolve first |
| Phaladeepika | 🟡 In progress | 743 (16 ch) | Phaladeepika_Inconsistencies_Review.docx | Phase 2 -- P2-5 | Tier 4 (3 ch) decode pending |

---

## Schema Constants Quick Reference

| Field | Source file | Relevant for |
|---|---|---|
| `VALID_CONDITION_TYPES` | `ke_schema_constants.py` | All decode threads |
| `VALID_CLAIM_AXES` | `ke_schema_constants.py` | Outcome mapping |
| `UPAGRAHA_PLANETS` | `ke_schema_constants.py` | Adhyaya XXV / Upagraha chapters |
| `KALACHAKRA_DASHA_YEARS` | `ke_schema_constants.py` | Adhyaya XXII |
| `VALID_CROSS_TEXT_RELATIONSHIPS` | `ke_schema_constants.py` | Dedup script output |
| `VALID_CONTRADICTION_TYPES` | `ke_schema_constants.py` | Contradiction pair encoding |
| `ENGINE_DEPENDENCY_IDENTIFIERS` | `ke_schema_constants.py` | Tier 6 chapters |

---

## For a New Thread Starting a Book Decode

1. Read `KE_Book_Decode_Process_Technical.md` (the full technical process)
2. Read the relevant `Decode_Guides/[BookName]_Decode_Guide.md`
3. Check `KE_Ingest_Sequence_Approved.md` for the approved chapter order
4. Copy `KE_NewBook_Thread_Start_Template.md` as your thread start message
5. Leave `cross_text_matches: null` on all rules -- dedup script populates this post-decode
6. Populate `claim_polarity` on every rule -- required for automated contradiction detection
7. Produce `*_Rules.json` + `*_Summary.md` + `*_Diagnostic.md` + `*_Contradictions.json` per chapter

---

*All decode output goes to: `/Users/apple/Documents/Knowledge Engine_eBooks/[BookName]_CC_Decode/`*
