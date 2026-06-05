# KE Rule Ingest -- Approved Sequence

> **KE Freeze LIFTED:** 2026-05-22
> **Approved by:** Prateek Malhotra (Temple Team / Co-Founder)
> **Approval statement:** "Yes, am happy with the effort team has put in. Please proceed with the further Ingest Process. 'Approved'."

---

## What the Freeze Was

The Knowledge Engine was under a governance hold (KE Freeze) pending completion of the **Sprint 2 Arbitration Runtime**. The referee system -- which resolves conflicts between rules before they fire -- was missing. Without it, contradicting rules could both trigger simultaneously and produce incoherent output.

**Sprint 2 gates (all passed 2026-05-17):**

| Gate | What it added | Status |
|---|---|---|
| `_contradiction_score` | Numeric conflict signal between any two rules | ✅ |
| `_build_tension_block` | Surfaces conflict context to the LLM | ✅ |
| `_representation_mode` | Picks how to present conflicting rules (blend / dominant / flag) | ✅ |
| Supersession lookup | Newer rule automatically supersedes older conflicting rule | ✅ |
| `scan_chart()` | Full chart scan that runs arbitration before firing any rule | ✅ |

**What was NOT blocking:**
- No architecture conflict
- No data integrity issue
- No contradictions found in the existing rule sets

**Validation:** 5 gates tested against synthetic chart data. All 5 passed. Co-founder sign-off was the final gate -- now done.

---

## Ingest Rules (Mandatory)

All rules enter as `approval_status: "pending_human_review"`.
Rules do NOT become active in production until a separate co-founder approval per rule set changes status to `"approved"`.

The Legacy Model (`vedic_calculator.py`) remains the ONLY live data source until KE rules reach `"approved"` status. KE interpretation is additive, never replacement.

---

## Ingest Sequence

| Priority | Book | Rules | Script / Handover | Blocker |
|---|---|---|---|---|
| **1 -- FIRST** | 300 Combinations | 300 rules | `HANDOVER_SUMMARY.md` in `/ThreeHundredCombinations_CC_Decode/` | None |
| **2** | 300 Horoscopes Vol1 | 57 rules | `/ThreeHundredHoroscopes_CC_Decode/` -- all output files present | None |
| **2** | Longevity & Unnatural Death | 44 rules | `/Longevity_CC_Decode/` | None |
| **3** | Numerology | 189 rules (Ch01-15) | Ch15 test vectors must complete first (50 cases) | Ch15 TVs in progress |
| **3** | SBC | 181 rules | 24 source gaps must be resolved by Temple Team first | 24 source gaps open |
| **LAST** | Longevity (58 chapters) | ~600+ rules | Awaiting aayu bucket methodology co-founder approval | Aayu bucket sign-off |

---

## Priority 1 -- 300 Combinations (Start Immediately)

**Why first:** Clean handover, no blockers, no cross-book dedup needed (different system -- 300 yogas, not horoscopes).

**Handover location:** `/Users/apple/Documents/Knowledge Engine_eBooks/ThreeHundredCombinations_CC_Decode/`

**Upload script pattern:**
```bash
python3 scripts/ingest_300_combinations.py \
    --upload scripts/combinations_rules.json \
    --mongo-url "$MONGO_URL" --db-name horoscope_db
```

**Verify after ingest:**
```bash
python3 scripts/validate_rules.py \
    --mongo-url "$MONGO_URL" --db-name horoscope_db \
    --science-id jyotish_300_combinations
```

---

## Priority 2 -- 300 Horoscopes + Longevity & Unnatural Death

**300 Horoscopes notes:**
- 6 rules superseded (documented in `H300_S04_Nodes_Diagnostic.md`)
- 47 cross-book flags (against SBC + Longevity) -- do NOT block ingest; flags are informational
- 15 test vectors complete

**Longevity & Unnatural Death notes:**
- 44 rules, 2 benchmarks
- No cross-book conflicts flagged

---

## Priority 3 -- Numerology (after Ch15 TVs complete)

**Ch15 checkpoint status (as of 2026-05-22):**
- 5 cases reviewed ✅
- Remaining 45 cases: go-ahead given
- Schema finalized: `name_options[]` array with controlled vocabulary (`preferred` / `valid` / `rejected`)
- `computation_verified` + `computation_notes` fields added

Wait for decode thread to complete all 50 Ch15 test vectors before ingest.

---

## Priority 3 -- SBC (after 24 source gaps resolved)

**24 source gaps:** OQ (Open Questions) raised during the 40-question batch.
Temple Team to review and resolve each gap before SBC rules are ingested.
Resolved OQs (OQ-08-01 through OQ-18-01): 7 conflicts resolved, documented in SBC thread output.

---

## Last -- Longevity 58 Chapters

Requires co-founder sign-off on the **aayu bucket methodology** (longevity span calculation approach). Do not begin this ingest until that approval is explicitly given.

---

## KE Freeze Lift -- Confirmation Entry

```
Date:       2026-05-22
Event:      KE Freeze LIFTED
Authority:  Prateek Malhotra (Co-Founder / Temple Team)
Gate:       Sprint 2 Arbitration Runtime -- 5/5 gates passed (2026-05-17)
Next step:  Begin ingest with 300 Combinations (Priority 1)
```

---

## Phase 2 Books (ingest after Phase 1 sequence complete)

> Added 2026-05-30. Phase 2 decode is confirmed complete across all 10 books.
> OCR issue reports and TempleTeam briefs are ready for each.
> New KE Ingest Thread owns Phase 2 execution.
> Handover guide: `KE_TEXTBOOK_DECODE/Handover_Guides/HANDOVER_KE_INGEST_THREAD.md`

| Order | Book | Rules | OCR Issues | Blocker |
|---|---|---|---|---|
| P2-1 | KP Astrology | 256 / 77 files | 44 issues (2 P0, 15 P1) | Verify entries 248-249; claim_axis retroactive pass |
| P2-2 | BPHS Vol 1 | 200+ (Ch11-Ch24) | 26 issues (6 HIGH open) | Category D: 7 doctrinal ambiguities → TT decision |
| P2-3 | BPHS Vol 2 | TBD | OCR report ready | Work through 9 next actions in BPHS_Vol2_TempleTeam_Brief.docx |
| P2-4 | Medical Astrology | TBD | 81 issues -- ✅ ALL GRADE A+B RESOLVED 2026-05-31 | 🟢 READY FOR INGEST. Grade C: bench-004 `birth_data_unavailable:true`, Charts XI/XII/XXII `analytical_description_only:true`. gai_citation_unverified on B-7/B-8/B-11 -- Ingest Thread cross-check before co-founder approval. |
| P2-5 | Phaladeepika | 743 (16 ch) + Tier 4 | 102 issues (6 HIGH) | Tier 4 (3 chapters) still pending decode; ingest decoded tiers only |

**Dedup rule:** Run `ke_dedup_script.py` after each Phase 2 book ingested. Cross-text flags against Phase 1 books are expected (documented in each book's output folder).
