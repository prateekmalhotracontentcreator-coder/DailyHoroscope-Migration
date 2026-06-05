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
| ✅ **1 -- COMPLETE** | 300 Combinations | 329 | ✅ INGESTED + TRIAGE COMPLETE 2026-06-01. 141 AA / 188 PHR / 0 flagged. |
| **1 -- START NOW** | 300 Horoscopes Vol 1 | 57 | ✅ All 3 formerly blocked rules cleared (2026-05-31 PDF read). No blockers. |
| **2** | Longevity Unnatural Death | 44 | ✅ All 5 HIGH OCR items resolved (2026-05-31). Ready. |
| **3** | Destiny Numerology | 189 | CRITICAL + HIGH OCR items need NLM/GAI first |
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

---

## 10. Schema Learnings from 300 Combinations Ingest (2026-06-01)

Apply these to every subsequent book ingest.

### L1 -- `tba: true` is temporary, not permanent
Conditions marked `tba: true` because they were `None` in source JSON may still be fully documented in the corresponding Diagnostic file (`*_Diagnostic.md`). **Always read the Diagnostic before marking a rule tba permanently.** In 300 Combinations, 14 rules had `None` conditions in the source JSON but complete conditions in the Diagnostic Content Gate section.

### L2 -- Bucket B: Textbook mismatch is the most common validator error
When the AI validator says "not in standard classical texts" for a rule from B.V. Raman (or any non-BPHS source), it is comparing to BPHS as "standard." This is always Bucket B. Patch to PHR with `validator_error: true` + a note that the rule is from a different textbook. Do NOT reject these rules.

### L3 -- Condition encoding errors are Bucket C, not Bucket B
When an AI validator catches a genuine logical error in the condition structure (e.g., "three planets cannot simultaneously occupy two houses" → actually it correctly identified that Saturn should *aspect* the houses, not *be placed* in them), that is a real Bucket C that requires a condition fix, not a PHR patch. Re-read the original source condition carefully before deciding.

### L4 -- Strip speculative metadata overlays before validation
When adding metadata to condition dicts (e.g., `day_night_modifier`, `engine_note` with specific day/night × afflictor mappings), only include if confirmed in the source text. If the Diagnostic shows MEDIUM-LOW confidence on a note, strip the note from the condition dict and let the plain condition be validated on its own merits.

### L5 -- Old-schema `conditions` can be either a list OR a dict
In 300 Combinations old-schema rules, `conditions` was sometimes a list (simple rules) and sometimes a rich nested dict (complex multi-trigger rules). The ingest script must check `isinstance(conds, dict)` before treating it as a list. Storing a dict directly as `condition` is correct. The OP-02 fix applied this.

### L6 -- `results` as list of dicts needs `extract_effects()` helper
When `results` is a list of dicts with `effect`/`description`/`result` keys (instead of plain strings), the ingest script must use `extract_effects()` to flatten them to plain text before building `interpretation.detailed`. Plain dict repr in the interpretation field will fail AI validation.

---

*Handover prepared: 2026-05-30 by Claude Code Main Thread*
*Updated: 2026-06-01 -- 300 Combinations ✅ COMPLETE, 300 Horoscopes is Priority 1. Schema learnings L1-L6 added.*
