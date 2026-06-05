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
├── Thread_Briefs/                      ← One brief per book -- paste the one-liner into each dedicated thread
│   ├── THREAD_BRIEF_INDEX.md               ← ⭐ START HERE -- 1-liner per book + status dashboard
│   ├── THREAD_BRIEF_BPHS_VOL1_INGEST.md    ← 🟢 READY -- Ph1 (Ch12-44) in MongoDB. Ph2 (Ch03-11, Ch25-33) ingest now.
│   ├── THREAD_BRIEF_BPHS_VOL2_INGEST.md    ← 🟢 READY -- Ch49-51, 249 rules
│   ├── THREAD_BRIEF_300COMBINATIONS_INGEST.md  ← ✅ READY -- Priority 1, start now
│   ├── THREAD_BRIEF_300HOROSCOPES_INGEST.md    ← ✅ READY -- 57 rules cleared 2026-05-31
│   ├── THREAD_BRIEF_LONGEVITY_UNNATURAL_INGEST.md ← ✅ READY -- 44 rules cleared 2026-05-31
│   ├── THREAD_BRIEF_DESTINY_NUMEROLOGY_INGEST.md  ← 🟠 NEAR READY -- 10 HIGH OCR items pending
│   ├── THREAD_BRIEF_SBC_INGEST.md          ← 🔴 BLOCKED -- TT + OCR decisions needed
│   ├── THREAD_BRIEF_LONGEVITY_58CH_INGEST.md ← 🔴 HARD BLOCKED -- aayu sign-off needed
│   ├── THREAD_BRIEF_KP_DECODE.md           ← 🟡 NEAR READY -- Cat B/C/G/H pending
│   ├── THREAD_BRIEF_MEDICAL_ASTROLOGY_INGEST.md ← 🟢 READY -- all Grade A+B resolved 2026-05-31
│   └── THREAD_BRIEF_PHALADEEPIKA_NLM.md    ← 🟢 READY -- all 28 chapters decoded, 743 rules
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
| 300 Horoscopes Vol 1 | ✅ Complete | 57 | H300_OCR_Issues_Report.docx | Phase 1 -- Priority 2 | ✅ All 3 blocked rules cleared 2026-05-31 |
| Longevity Unnatural Death | ✅ Complete | 44 | LU_OCR_Inconsistency_Review.docx | Phase 1 -- Priority 2 | ✅ All 5 HIGH items resolved 2026-05-31 |
| Destiny Numerology | ✅ Complete | 189 (Ch01-15) | Book_Wide_OCR_Inconsistencies_Report.docx | Phase 1 -- Priority 3 | 🟠 10 HIGH OCR items → NLM/GAI pass needed |
| SBC | ✅ Complete | 181 | SBC_OCR_Issues_Report.docx | Phase 1 -- Priority 3 | 🔴 7 TT conflicts + 4 CRITICAL OCR + 17 source gaps |
| Longevity 58 chapters | ✅ Complete | ~600+ | -- | Phase 1 -- LAST | 🔴 Aayu bucket co-founder sign-off needed |
| KP Astrology | 🟡 Near complete | 256 / 77 files | KP_T05_OCR_Issues_Report.docx | Phase 2 -- P2-1 | Cat B/C/G/H + F-01 to F-06 pending |
| BPHS Vol 1 | 🟢 READY | ~1,456 (37 ch) | BPHS_Vol1_OCR_Issue_Register.docx | Phase 1 -- Foundation | ✅ All 10 TT items resolved + encode pass 2026-05-31 |
| BPHS Vol 2 | 🟢 READY | 249 (Ch49-51) | BPHS_Vol2_OCR_Inconsistency_Report.docx | Phase 1 -- Foundation | ✅ All 10 OCR items resolved + encode pass 2026-05-31 |
| Medical Astrology | 🟢 READY FOR INGEST | TBD | MedAstro_OCR_Issues_Audit.md | Phase 2 -- P2-4 | All Grade A+B resolved 2026-05-31. gai_citation_unverified on B-7/B-8/B-11. |
| Phaladeepika | 🟢 READY FOR INGEST | 743 (28 ch all decoded) | Phaladeepika_Inconsistencies_Review.docx | Phase 2 -- P2-5 | All 6 HIGH resolved 2026-05-31. ~25 MED → pending_review:true |

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
