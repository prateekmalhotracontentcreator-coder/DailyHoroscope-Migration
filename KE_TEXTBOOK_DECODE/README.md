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
│   ├── THREAD_BRIEF_PHALADEEPIKA_NLM.md   ← UNBLOCKED -- Begin Adhyaya II
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

## Active Decode Threads -- Current Status

| Book | Status | Output Folder | Next Action |
|---|---|---|---|
| Phaladeepika | 🟢 UNBLOCKED | `Phaladeepika_CC_Decode/` | Begin Adhyaya II immediately |
| BPHS Vol 1 | 🟡 PARTIAL | `BPHS_CC_Decode/` | Ch11-Ch24 done; confirm Q1/Q2 then continue |
| KP Astrology | 🟡 NEAR COMPLETE | `KP_CC_Decode/` | claim_axis retroactive pass then CLOSED |

---

## Books Decoded -- Ingest Summary

| Book | Chapters Decoded | Rules | Output Folder | Notes |
|---|---|---|---|---|
| KP Astrology | Full (all chapters) | 256 rules / 77 files | `KP_CC_Decode/` | claim_axis longevity pass pending |
| BPHS Vol 1 | Ch11-Ch24 | ~200+ rules | `BPHS_CC_Decode/` | House effects complete; Karaka/Yoga/Dasha pending |
| Longevity (Unnatural) | Multiple chapters | Pending count | `Longevity_CC_Decode/` | -- |
| Medical Astrology | Multiple chapters | Pending count | `MedicalAstrology_CC_Decode/` | -- |

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
