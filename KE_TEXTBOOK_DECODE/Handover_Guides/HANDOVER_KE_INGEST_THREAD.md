# Handover Guide -- KE Ingest Thread
> Prepared by: Claude Code (Main Thread)
> Date: 2026-05-30
> Purpose: New dedicated thread runs OCR resolution, ingest, and dedup for all 10 Phase 2 books. Main thread reviews output and approves before any MongoDB writes.

---

## 1. Your Role

You are the **KE Ingest Thread**. You own:
- NLM/GAI OCR verification for each book's issue report
- Running ingest scripts in the approved sequence
- Dedup + contradiction detection after each book pair
- Reporting back to TT for decisions on flagged items

You do NOT own:
- TT decisions on blocked/ambiguous rules (escalate to main thread)
- Co-founder approval on aayu bucket methodology
- Any production activation of rules (all rules enter as `pending_human_review`)

---

## 2. MANDATORY FIRST ACTION -- Before Reading Anything Else

**Execute this immediately on startup:**

Use the Write tool to create this file:
```
Path:    /Users/apple/Documents/Knowledge Engine_eBooks/KE_Ingest_Phase2_Progress.md
Content: # KE Ingest Phase 2 Progress
         Thread started [date].
         All output goes to files. Context window = one-line status only.
```

This anchors your output destination. **ALL progress notes, resolution summaries, and ingest logs go to files. The context window receives one-line status updates only.** This is non-negotiable -- context overflow kills the thread.

---

## 3. Reference Files -- Read in This Order

| Priority | File | What it contains |
|---|---|---|
| 🔴 MUST READ | `KE_TEXTBOOK_DECODE/README.md` | Folder structure, active threads, schema quick ref |
| 🔴 MUST READ | `KE_TEXTBOOK_DECODE/KE_Book_Decode_Process_Technical.md` | Full ingest process -- dry run gate, validator, field requirements |
| 🔴 MUST READ | `KE_TEXTBOOK_DECODE/KE_Ingest_Sequence_Approved.md` | Approved order for all books + blockers per book |
| 🟠 READ | Each book's TempleTeam Brief (paths in Section 6) | Per-book decode summary, ingest queue, next actions |
| 🟡 REFERENCE | `KE_TEXTBOOK_DECODE/Schema_Docs/` | Schema decisions, contradiction encoding, retroactive impact |

---

## 4. Ingest Sequence -- Strict Order

### Phase 1 (approved sequence -- start here)

| Order | Book | Rules | Blocker |
|---|---|---|---|
| **1 -- START NOW** | 300 Combinations | 300 | None -- clean handover, no OCR issues |
| **2** | 300 Horoscopes Vol 1 | 57 (3 blocked) | Flag h300-s01-016, h300-s04-004, h300-s04-005 to TT before ingesting those 3 |
| **2** | Longevity Unnatural Death | 44 | Resolve 5 HIGH OCR items via NLM/GAI first (see Section 5) |
| **3** | Destiny Numerology | 189 | Ch15 test vectors confirmed complete |
| **3** | SBC | 181 | Flag 7 blocking priority conflicts to TT; resolve 24 source gaps |
| **LAST** | Longevity 58 chapters | ~600+ | Do NOT start -- needs explicit TT aayu bucket sign-off |

### Phase 2 (after Phase 1 sequence complete)

| Order | Book | Rules | Blocker |
|---|---|---|---|
| 1 | KP Astrology | 256 / 77 files | Verify entries 248-249; claim_axis retroactive pass |
| 2 | BPHS Vol 1 | 200+ (Ch11-Ch24) | Resolve OCR Category D ambiguities; flag 7 doctrinal items to TT |
| 3 | BPHS Vol 2 | TBD | Work through 9 next actions in BPHS_Vol2_TempleTeam_Brief.docx |
| 4 | Medical Astrology | TBD | Resolve 2 Grade A CRITICAL items first (Chart IX, "17/46") |
| 5 | Phaladeepika | 743 (16 ch) + Tier 4 | Tier 4 decode (3 chapters) still pending; ingest only decoded tiers |

---

## 5. OCR Resolution Protocol

For each book, before ingesting:

1. Read the book's OCR issue report (paths in Section 6)
2. Triage each issue by grade:

| Grade | Action |
|---|---|
| **P0 / CRITICAL / Grade A** | Stop. Flag to TT immediately. Do not ingest affected rules. |
| **P1 / HIGH / Grade B** | Run NLM/GAI verification autonomously. Document resolution. |
| **P2 / MEDIUM / Grade C** | Resolve or document as accepted uncertainty. Proceed. |
| **P3 / LOW / Grade D** | Log and proceed. Zero rule impact. |

3. Write resolution summary to `/Users/apple/Documents/Knowledge Engine_eBooks/[Book]_CC_Decode/OCR_Resolution_Log.md`
4. Report summary to TT (one-line in context: "Book X OCR resolution complete. N items resolved, N flagged to TT.")

### Priority NLM/GAI queries per book

| Book | Critical queries (run first) |
|---|---|
| 300 Horoscopes | Issues 7 (S01 diagram), 13 (TABLE-IV columns E/F), 19 (Ketu aspecting) -- Queries 1-5 in Section 5 of H300_OCR report are copy-paste ready |
| Longevity Unnatural | lu-s04-001 ("must" vs "should"), lu-s04-014 (AND vs OR), lu-s04-003/004 (5-level chain), lu-s04-010 (lethal planet), CS1 Mercury coordinate |
| Numerology | CRITICAL: Ch17 Number 3 Amethyst (HIGH), Ch19 two element systems conflict |
| SBC | C-01 Chandra Kalanal index, C-02 Sapt Salaka table, C-03 Star rank results, C-04 Devanagari consonant groups |
| Medical Astrology | Chart IX zero birth data (bench-004), "17/46" annotation (bench-009) |
| Phaladeepika | Top 8 GAI priorities in Section 5 of Phaladeepika_Inconsistencies_Review.docx |
| KP Astrology | Read T06 page 1 to verify entries 248-249; P2 ambiguous terms F-01 to F-06 |
| BPHS Vol 1 | Category B-E issues in BPHS_Vol1_OCR_Issue_Register.docx |

---

## 6. Book Brief and OCR Report Locations

All paths under `/Users/apple/Documents/Knowledge Engine_eBooks/`

| Book | TempleTeam Brief | OCR Report |
|---|---|---|
| BPHS Vol 2 | `BPHS_Vol2_CC_Decode/BPHS_Vol2_TempleTeam_Brief.docx` | `BPHS_Vol2_CC_Decode/BPHS_Vol2_OCR_Inconsistency_Report.docx` |
| Destiny Numerology | `DestinyNumerology_CC_Decode/` | `DestinyNumerology_CC_Decode/Book_Wide_OCR_Inconsistencies_Report.docx` |
| BPHS Vol 1 | `BPHS_CC_Decode/BPHS_Vol1_TT_Brief.docx` | `BPHS_CC_Decode/BPHS_Vol1_OCR_Issue_Register.docx` |
| Longevity Unnatural | `LongevityUnnatural_CC_Decode/LU_TempleTeam_Brief.docx` | `LongevityUnnatural_CC_Decode/LU_OCR_Inconsistency_Review.docx` |
| 300 Horoscopes | `ThreeHundredHoroscopes_CC_Decode/H300_Temple_Team_Brief.docx` | `ThreeHundredHoroscopes_CC_Decode/H300_OCR_Issues_Report.docx` |
| Phaladeepika | `Phaladeepika_CC_Decode/Phaladeepika_TempleTeam_Brief.docx` | `Phaladeepika_CC_Decode/Phaladeepika_Inconsistencies_Review.docx` |
| KP Astrology | `KP_CC_Decode/KP_Vol3_Temple_Brief.md` | `KP_CC_Decode/KP_T05_OCR_Issues_Report.docx` |
| Medical Astrology | `MedicalAstrology_CC_Decode/MedAstro_TempleTeam_Brief.md` | `MedicalAstrology_CC_Decode/MedAstro_OCR_Issues_Audit.md` |
| Longevity 58 chapters | `Longevity_CC_Decode/HANDOVER_SUMMARY_LongevityDecode.md` | -- |
| SBC | `New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/SBC_Master_Decode_Summary.md` | `New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/SBC_OCR_Issues_Report.docx` |
| 300 Combinations | `ThreeHundredCombinations_CC_Decode/HANDOVER_SUMMARY.md` | -- (no OCR issues) |

---

## 7. TT Escalation Items -- Flag These, Do Not Decide

These require TT sign-off. Flag each one with a one-line note and wait for approval before ingesting the affected rules.

| Book | Item | Decision type |
|---|---|---|
| 300 Horoscopes | h300-s01-016 (blocked rule) | Approve / reject / modify |
| 300 Horoscopes | h300-s04-004 (blocked rule) | Approve / reject / modify |
| 300 Horoscopes | h300-s04-005 (blocked rule) | Approve / reject / modify |
| Longevity Unnatural | lu-s04-001: "must" vs "should" -- is this a hard gate or weighted score? | Architecture decision |
| Longevity Unnatural | lu-s04-014: AND vs OR in weapon death condition | Logic gate decision |
| SBC | 7 blocking priority conflicts from 40-question batch (listed in SBC_Master_Decode_Summary.md) | TT resolves each |
| BPHS Vol 1 | Category D -- 7 doctrinal ambiguities (malefic/benefic antidote paradox, Trimsamsa reversal, etc.) | TT reviews each |
| Longevity 58 chapters | Aayu bucket methodology | Co-founder explicit sign-off required before ingest |

---

## 8. Post-Ingest Protocol (every book)

After each book's ingest script completes:

1. Run dedup: `python3 backend/ke_dedup_script.py --science-id [book_science_id]`
2. Check `import_batches`: count matches expected rule count
3. Verify `interpretation_rules`: all have `approval_status: "pending_human_review"`
4. Write one-line status to TT: "Book X ingested. N rules. N dedup flags. Report at [file path]."
5. Write full dedup report to `/Users/apple/Documents/Knowledge Engine_eBooks/[Book]_CC_Decode/Dedup_Report.md`

**No rules go live until TT explicitly changes approval_status to "approved" per rule set. This is not your decision.**

---

## 9. Ingest Scripts (reference)

| Script | Purpose |
|---|---|
| `backend/ke_dedup_script.py` | TF-IDF cosine dedup + contradiction detection |
| `backend/ke_schema_constants.py` | Schema enum constants |
| `backend/knowledge_schema.py` | Pydantic validation |
| Each book's `ingest_[book].py` | Book-specific ingest (see TempleTeam Brief for script path) |

---

*Handover prepared: 2026-05-30 by Claude Code Main Thread*
