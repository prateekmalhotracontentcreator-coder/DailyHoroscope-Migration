# Thread Brief -- BPHS Vol 1 NLM Decode
## Status Update + Queries + Next Steps

> Prepared by: Temple Team -- EverydayHoroscope
> Date: 2026-05-28
> For: BPHS Vol 1 Decode Thread
> Status: **FREEZE CONFIRMED -- NLM Decode Commission Required**

---

## Current State -- What Exists

The BPHS Vol 1 folder contains **6 JSON files**. These are NOT decoded KE rules.

They are **raw OCR output** from a document scanning API. Each file's root structure is:

```json
{
  "success_count": <int>,
  "total_count": <int>,
  "version": "...",
  "pages": [
    {
      "page": <int>,
      "content": [
        {
          "text": "...",
          "bbox": [x1, y1, x2, y2],
          "confidence": 0.94
        }
      ]
    }
  ],
  "catalog": {...},
  "metrics": {...}
}
```

This is Stage 0 source material -- pixel-coordinate bounding boxes from a scanning API. There are **zero decoded rules, zero Rules.json files, zero Summary.md files** in this folder.

### What OCR files exist

| File | Chapter | Pages |
|---|---|---|
| `BPHS_Vol1_Ch27_OCR.json` | Chapter 27 | 25 pages |
| `BPHS_Vol1_Ch34_OCR.json` | Chapter 34 | 17 pages |
| `BPHS_Vol1_Ch40_OCR.json` | Chapter 40 | 4 pages |
| `BPHS_Vol1_Ch41_OCR.json` | Chapter 41 | 11 pages |
| `BPHS_Vol1_Ch43_OCR.json` | Chapter 43 | 25 pages |
| `BPHS_Vol1_Ch44_OCR.json` | Chapter 44 | 9 pages |

**Total: 6 chapters OCR'd -- out of 100 chapters in BPHS Vol 1.**

The full BPHS Vol 1 PDF is available at:
```
/Users/apple/Documents/Knowledge Engine_eBooks/Maharishi_Parashara_-_Brihat_Parasara_Hora_Sastra_(Vol._1).pdf
```

---

## Why the Freeze is Legitimate

The thread flagged a freeze because there was nothing to decode from -- the JSON files are scanner output, not sloka text in a format ready for NLM decode. The freeze is correct.

**What's needed before decode can begin:**
1. Sloka text must be extracted from the OCR bounding boxes (or from the full PDF directly)
2. An NLM Decode Commission must be issued -- same format as the KP Astrology commission and the LongevityUnnatural commission
3. The decode thread must receive chapter-level text input, not raw bounding-box JSON

---

## What BPHS Vol 1 Needs to Produce (Output Spec)

The decode must produce the same 3-document output as all other active decode threads:

```
BPHS_Vol1_AdhXX_[ChapterName]_Rules.json      ← KE rule documents (JSON array)
BPHS_Vol1_AdhXX_[ChapterName]_Summary.md      ← chapter doctrinal summary
BPHS_Vol1_AdhXX_[ChapterName]_Diagnostic.md   ← decode decisions + ambiguity log
```

Output folder:
```
/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol1_CC_Decode/
```

(This folder does not yet exist -- create it when the commission is issued.)

---

## Priority Chapters for Phaladeepika Dedup

The chapters with highest expected overlap with Phaladeepika (from Fresh Eyes assessment):

| Phaladeepika Chapter | BPHS Chapter (likely) | Overlap estimate |
|---|---|---|
| Adhyaya VIII -- Planets in 12 Bhavas | BPHS house-effect chapters (est. 15-26 range) | 60-70% |
| Adhyaya II -- Karakas & Significations | BPHS Karaka chapters | High |
| Adhyaya VI -- Pancha Mahapurusha Yogas | BPHS yoga chapters | Moderate |
| Adhyaya XIX -- Vimshottari Dasas | BPHS Dasha chapters | Moderate |

**Critical gap:** The house-effect chapters needed for the Adhyaya VIII dedup (BPHS Ch 15-26 range) are not among the 6 OCR'd chapters. Those chapters are not even at OCR stage yet.

**Consequence:** The Phaladeepika dedup for Adhyaya VIII cannot run until those chapters are both extracted from the full PDF AND fully decoded.

---

## Recommended Decode Priority (once commission is issued)

```
PRIORITY 1 -- Karaka & Signification chapters (dedup for Adhyaya II)
PRIORITY 2 -- Yoga chapters -- Pancha Mahapurusha (dedup for Adhyaya VI)
PRIORITY 3 -- House effect chapters (dedup for Adhyaya VIII -- largest gap)
PRIORITY 4 -- Dasha chapters (dedup for Adhyaya XIX)
PRIORITY 5 -- Remaining chapters
```

This sequence maximises usefulness for the active Phaladeepika decode as quickly as possible.

---

## Schema Notes for This Decode Thread

**All standard KE schema applies.** The following schema additions (from KE-SCHEMA-AMENDMENT-PD1) are relevant to BPHS Vol 1:

| Schema field | Relevant BPHS chapters |
|---|---|
| `claim_axis: "longevity"` | Longevity / Ayurdaya chapters |
| `engine_dependency: ["ashtakavarga_calculator"]` | Ashtakavarga chapters |
| `engine_dependency: ["kalachakra_dasa_calculator"]` | Kalachakra Dasa chapters |

**Schema constants source of truth:** `backend/ke_schema_constants.py`
**Schema validation layer:** `backend/knowledge_schema.py`

**Cross-text matching:** Leave `cross_text_matches: null` on all rules during initial decode. The dedup script will populate this field in a post-decode pass once both BPHS Vol 1 and Phaladeepika rule sets are complete.

---

## Open Queries -- Please Confirm

| # | Query | Action owner |
|---|---|---|
| Q1 | What is the source PDF / edition of BPHS Vol 1 in use? (Maharishi Parasara / Bangalore / Girish Chand Sharma / other?) This affects sloka citation format. | **BPHS decode thread** |
| Q2 | Confirm `source.sloka` format. Proposed: `"chapter.sloka"` e.g. `"34.12"` for Chapter 34 Sloka 12. Is this what the thread is using? | **BPHS decode thread** |
| Q3 | Can the thread extract sloka text directly from the full PDF (at the path above), rather than from the 6 OCR JSON files? The OCR files cover only 6 chapters and the text quality from the PDFs is better than bounding-box OCR for Sanskrit verses. | **BPHS decode thread** |
| Q4 | Which chapters are the thread's highest priority? The Temple Team recommends Karaka → Yoga → House Effects sequence (see above). Confirm whether the thread agrees or has a different sequencing preference. | **BPHS decode thread** |
| Q5 | Does the thread need a Codex NLM Decode Commission brief, or can they proceed using the existing KP Astrology commission as a format template? | **BPHS decode thread to confirm -- Temple Team to issue commission if needed** |

---

## Immediate Next Actions

| Action | Owner | Blocker? |
|---|---|---|
| Confirm text extraction method (PDF direct vs OCR JSON) | BPHS decode thread | Yes -- nothing can start until this is confirmed |
| Confirm chapter priority sequence | BPHS decode thread | Yes |
| Temple Team issues NLM Decode Commission | Temple Team | After thread confirms above |
| Create output folder: `/BPHS_Vol1_CC_Decode/` | Decode thread on first write | No |
| Begin decode: Priority 1 chapters | Decode thread | After commission issued |

**Until the commission is issued and the thread confirms their extraction method, maintain the freeze.**

---

*Brief prepared by Temple Team -- EverydayHoroscope, 2026-05-28*
