# Thread Brief -- BPHS Vol 1 NLM Decode
## Status Update + Queries + Next Steps

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-28 (corrected -- initial brief contained a critical error)
> For: BPHS Vol 1 Decode Thread (Thread A)
> Status: **PARTIALLY COMPLETE -- Ch11-Ch24 decoded. Remaining chapters TBD.**

---

## CORRECTION -- Initial Brief Was Wrong

The first version of this brief stated "zero decoded rules, freeze confirmed." That was incorrect. Thread A has produced significant decode output. Apologies for the error -- it was written without checking the actual output folder. Correct state is below.

---

## Actual Current State

### Output folder (canonical)
```
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode/
```
This folder exists and contains **86 files** covering Ch11-Ch24.

### What Thread A has decoded

| Chapter | Title | Files present |
|---|---|---|
| Ch11 | Judgement of Houses Contradictions | Rules.json + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch12 | Effects 1st House | Rules.json + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch13 | Effects 2nd House | Rules.json + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch14 | Effects 3rd House | Rules.json + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch15 | Effects 4th House | Rules.json + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch16 | Effects 5th House | Rules.json + Part1/Part2 + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch17 | Effects 6th House | Rules.json + Part1/Part2 + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch18 | Effects 7th House | Rules.json + Part1/Part2/Part3 + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch19 | Effects 8th House | Rules.json + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch20 | Effects 9th House | Rules.json + Part1/Part2 + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch21 | Effects 10th House | Rules.json + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch22 | Effects 11th House | Rules.json + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch23 | Effects 12th House | Rules.json + Summary.md + Diagnostic.md + Contradictions.json + DataTables.md |
| Ch24 | Effects Bhava Lords | Rules.json + Part1-Part6 + Summary.md + Diagnostic.md + DataTables.md |

**Total: 14 chapters decoded. Fresh Eyes assessment doc also present:**
`BPHS_CC_Decode/BPHS_Vol1_ThreadA_FreshEyes.md`

---

## Separate Folder -- Not Decode Output

```
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 1 De-code/
```
This folder contains **6 raw OCR JSON files** (Ch27, Ch34, Ch40, Ch41, Ch43, Ch44). These are scanner output (`pages[].content[].bbox` bounding-box format), NOT decoded KE rules. They are Stage 0 source material only. Thread A should not use these as decode input.

The full BPHS Vol 1 PDF (Santhanam translation) is the correct source:
```
/Users/apple/Documents/Knowledge Engine_eBooks/Maharishi_Parashara_-_Brihat_Parasara_Hora_Sastra_(Vol._1).pdf
```

---

## TT Decision Required -- Before Thread Continues

### Decision 1 -- Folder naming

The thread is writing output to `BPHS_CC_Decode/`. The new spec proposed `BPHS_Vol1_CC_Decode/` (doesn't exist). 

**TT recommendation: Keep `BPHS_CC_Decode/` as the canonical output folder.** Do not migrate. The folder has 86 files and is established. Do not rename or create a parallel folder.

**Thread A: confirm you are writing to `BPHS_CC_Decode/` and continue using it.**

### Decision 2 -- Ch11-Ch24 validity

Thread A decoded Ch11-Ch24 (all 12 House Effect chapters + Bhava Lords). Does this work stand under the current schema?

**TT assessment: Ch11-Ch24 work stands as valid.** The house effect chapters used `planet_in_house` and `yoga_combination` condition types -- both stable schema fields that were not amended by KE-SCHEMA-AMENDMENT-PD1. No retroactive re-encoding is required.

**Exception:** If any rules in Ch11-Ch24 involve longevity or death timing, those rules should have `claim_axis: "longevity"` added (now a valid value per KE-SCHEMA-AMENDMENT-PD1). The Fresh Eyes assessment notes Ch19 (8th House) has longevity rules. Those rules should be updated.

**Thread A: confirm Ch11-Ch24 output is complete and no chapters require a re-read.**

---

## What Remains to be Decoded

The priority sequence below is based on what Phaladeepika dedup needs most (house effects already covered -- thread can now move to remaining chapters):

```
NEXT PRIORITY -- Karaka & Signification chapters
  Ch 2  -- Character & General Significations of Planets
  Ch 3  -- Exaltation, Debilitation, Own Sign (Karaka definitions)
  Ch 4  -- Aspects, Natural Friends/Enemies

THEN -- Yoga chapters (for Phaladeepika Adhyaya VI dedup)
  Ch 34 -- Planetary Combinations (OCR exists in BPHS Vol 1 De-code/ -- use PDF instead)
  Ch 40 -- Royal Association Yogas (OCR exists -- use PDF instead)
  Ch 41 -- Wealth Yogas (OCR exists -- use PDF instead)

THEN -- Dasha chapters (for Phaladeepika Adhyaya XIX dedup)
  Ch 46 -- Vimshottari Dasha Effects
  (and related sub-dasha chapters)

THEN -- Remaining chapters as available
```

---

## Schema Notes

**All KE-SCHEMA-AMENDMENT-PD1 additions are now live.** The following are relevant for remaining BPHS chapters:

| Schema addition | Relevant BPHS chapters |
|---|---|
| `claim_axis: "longevity"` | Retroactive: Ch19 (8th House). Forward: Longevity/Ayurdaya chapters (Ch43, Ch44 when decoded) |
| `engine_dependency: ["ashtakavarga_calculator"]` | Ashtakavarga chapters |
| `engine_dependency: ["kalachakra_dasa_calculator"]` | Kalachakra chapters |
| `condition.type: "neechabhanga_rule"` | Any Neechabhanga rules in Yoga chapters |

**Schema constants:** `backend/ke_schema_constants.py`
**Schema validation:** `backend/knowledge_schema.py`

---

## Open Queries -- Thread A to Confirm

| # | Query | Blocking? |
|---|---|---|
| Q1 | Confirm Ch11-Ch24 output is complete. Any chapters flagged for re-read that haven't been revisited? (FreshEyes flagged Ch14, Ch15, Ch19, Ch22, Ch23 as thin -- were these re-read before closing?) | **Yes** |
| Q2 | Confirm output folder is `BPHS_CC_Decode/` -- is this where all future output will continue to go? | Yes |
| Q3 | Which edition/translation of BPHS Vol 1 is the thread using? (Santhanam / Girish Chand Sharma / other?) Affects sloka citation format. | No |
| Q4 | Confirm `source.sloka` format being used. Proposed: `"chapter.sloka"` e.g. `"12.4"` for Chapter 12 Sloka 4. | No |
| Q5 | For the remaining chapters (Karaka, Yoga, Dasha) -- can the thread proceed using the full PDF as source, or does it need pre-split chapter PDFs? If pre-split PDFs are needed, TT will prepare them. | No |

---

## Dedup Status

The house effect chapters (Ch11-Ch23) are now decoded. This means:

- **Phaladeepika Adhyaya VIII (Planets in 12 Bhavas)** dedup CAN proceed once Adhyaya VIII is decoded -- the BPHS counterpart chapters (Ch12-Ch23) are available
- **Phaladeepika Adhyaya II (Karakas)** dedup CANNOT run yet -- BPHS Karaka chapters not decoded
- **Phaladeepika Adhyaya VI (Yogas)** dedup CANNOT run yet -- BPHS Yoga chapters not decoded

Leave `cross_text_matches: null` on all rules. The automated dedup script will populate this field post-decode.

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-28*
*Corrects the initial brief which incorrectly stated "zero decoded rules, freeze confirmed"*
