# Knowledge Engine — Ingest Notes
Append a new entry for every batch processed. Never overwrite.

---

## Logic Updates (cumulative — check before starting any new batch)

### Parser — `ingest_bphs_houses_v2.py`

| Fix | What it does | Trigger |
|---|---|---|
| `neutralize_notes_lists()` | Strips numbered sub-items inside Notes sections before sloka parsing | Ch 16/18 were creating phantom slokas 1/2/3/4 from Notes sub-lists |
| Extended sloka regex | Handles: trailing alpha (9-9t, 10-13i), no space after period (3.EXCESSIVE), missing period (23 If...), leading apostrophe (' 34.) | Malformed sloka headings in source RTF |
| `_punct()` helper | Appends '.' to extracted rule text lacking terminal punctuation | Without this, 100% structural rejection on first validation pass |
| Blank-line paragraph boundary in `neutralize_notes_lists()` | Exits Notes context on blank line so real slokas after a Notes block are not accidentally neutralized | Ch 21 slokas 2-7 were being bracketed as Notes sub-items because they appeared within 25 lines of a Notes marker with numbers ≤ 9 |
| `strip_rtf()` preserves blank lines | Blank lines kept as paragraph separators so `neutralize_notes_lists()` can use them as boundaries | Required for the above fix to work — old code filtered all blank lines |
| Sloka regex accepts `,` separator | `[.,]?` instead of `\.?` — handles `14, If...` style headings | Ch 21 sloka 14 used comma instead of period after number |
| Sloka regex accepts `+` range separator | `[-\u2013+]` — handles `14+15` style ranges | Ch 19 sloka `14+15` was not detected; content was misattributed to sloka 8-13 |

### Ingest script — `ingest_bphs_dasha_v1.py`

| Fix | What it does | Trigger |
|---|---|---|
| `temperature=0` (both call sites, lines 268 + 308) | Makes Claude extraction deterministic — identical sloka text → identical rule count on every run | Ch 57 dry runs produced 113 vs 118 rules on two consecutive runs due to LLM non-determinism at temp=0.1. Over-split detected at sloka 20-21 (4 vs 10 rules); under-split at sloka 71-73 (1 vs 3 rules). |

### Validator — `knowledge_validator.py`

| Fix | What it does | Trigger |
|---|---|---|
| `structural_check` word-min lowered to 3 | Allows short planet_in_house / sign sub-rules to pass | Sub-rules with valid but brief interpretations were being rejected |

### Pre-Batch Checklist (run before every new ingest)

- [ ] Inspect source RTF for numbered lists inside Notes/commentary sections — neutralize if present
- [ ] Check sloka heading format — any trailing alpha, missing periods, leading apostrophes, period-separated ranges (e.g. `61.62.` instead of `61-62`)
- [ ] Run dry run — record per-sloka rule counts as the confirmed baseline
- [ ] Confirm 61-62-style verse ranges are captured (both runs of Ch 57 missed slokas 61-62 until RTF was corrected)
- [ ] Confirm translator editorial notes are NOT extracted as rules (e.g. "Our belief is…", "It is difficult to believe…")
- [ ] Live ingest per-sloka counts must match dry-run baseline exactly — any divergence = flag for manual review
- [ ] After ingest, run `patch_punctuation.py` before validating
- [ ] Run `reset_to_pending.py` if any rules were previously rejected
- [ ] Confirm batch IDs in DB before running validator

---

## Batch Log

---

### BPHS Ch 12-18 | Houses 1-7 | Apr 2026

**Batches:**

| Ch | House | Batch ID | Total | auto_approved | pending_human_review | flagged | contradictions |
|---|---|---|---|---|---|---|---|
| 12 | 1st (Lagna) | bphs-ch12-v2-20260414 | 17 | 7 (41%) | 6 (35%) | 4 (24%) | 1 pair |
| 13 | 2nd (Wealth) | bphs-ch13-v2-20260414 | 32 | 22 (69%) | 10 (31%) | 0 | 0 |
| 14 | 3rd (Siblings) | bphs-ch14-v2-20260414 | 33 | 19 (58%) | 8 (24%) | 6 (18%) | 2 pairs |
| 15 | 4th (Mother) | bphs-ch15-v2-20260414 | 20 | 5 (25%) | 10 (50%) | 5 (25%) | 2 pairs |
| 16 | 5th (Children) | bphs-ch16-v2-20260414 | 41 | 18 (44%) | 17 (41%) | 6 (15%) | 2 pairs |
| 17 | 6th (Enemies) | bphs-ch17-v2-20260414 | 43 | 31 (72%) | 8 (19%) | 4 (9%) | 0 |
| 18 | 7th (Marriage) | bphs-ch18-v2-20260414 | 55 | 38 (69%) | 14 (25%) | 3 (5%) | 2 pairs |
| **Total** | | | **241** | **140 (58%)** | **79 (33%)** | **28 (12%)** | **9 pairs** |

**Open Points:**

1. **Ch 15 low auto-approve (25%)** — outlier vs 58% average. Root cause unknown — flag reasons not pulled. Before Ch 19-23 review, inspect Ch 15 flagged rules in Admin > Rules Browser to determine if this is a source quality issue (RTF) or a validator calibration issue.

2. **28 flagged rules across Ch 12-18** — flag reasons not recorded. Need a pass through Admin > Rules Browser (filter: flagged) before co-founder approval to determine: dismiss / edit / escalate.

3. **9 contradiction pairs** — contradiction rule IDs and summaries not captured. Pull these before logic layer integration to check if contradictions are genuine (conflicting classical rules) or validator error.

4. **79 pending_human_review rules** — these are spot_check verdicts awaiting co-founder sign-off. Not live until explicitly promoted to `approved`.

5. **All Ch 12-18 rules ingested from separate RTFs** — Ch 19-23 were delivered as individual RTFs (one per chapter), no splitting needed.

---

### BPHS Ch 19-23 | Houses 8-12 | Apr 2026

**Batches:**

| Ch | House | Batch ID | Total | auto_approved | pending_human_review | flagged | contradictions |
|---|---|---|---|---|---|---|---|
| 19 | 8th (Longevity) | bphs-ch19-v2-20260415 | 21 | 7 (33%) | 10 (48%) | 4 (19%) | 2 pairs |
| 20 | 9th (Fortune) | bphs-ch20-v2-20260415 | 33 | 21 (64%) | 11 (33%) | 1 (3%) | 1 pair |
| 21 | 10th (Career) | bphs-ch21-v2-20260415 | 28 | 18 (64%) | 8 (29%) | 2 (7%) | 0 |
| 22 | 11th (Wealth) | bphs-ch22-v2-20260415 | 16 | 10 (62%) | 5 (31%) | 1 (6%) | 1 pair |
| 23 | 12th (Spirituality) | bphs-ch23-v2-20260415 | 21 | 14 (67%) | 5 (24%) | 2 (10%) | 0 |
| **Total** | | | **119** | **70 (59%)** | **39 (33%)** | **10 (8%)** | **4 pairs** |

**Parser issues found and fixed during this batch:**
- Ch 21: slokas 2-7 not detected (blank-line boundary fix applied)
- Ch 21: sloka 14 used comma separator (comma fix applied)
- Ch 19: sloka 14+15 used `+` range separator (plus fix applied)
- Ch 19 and 21 re-ingested after fixes; Ch 20 re-ingested for sloka attribution correctness

**Open Points:**

1. **Ch 19 low auto-approve (33%)** — second outlier after Ch 15 (25%). Both are complex-topic chapters (8th house longevity, 4th house mother) with multi-condition rules. Pattern suggests validator flags rules with multiple simultaneous planetary conditions. Review flagged rules to confirm before logic layer integration.

2. **10 flagged rules across Ch 19-23** — flag reasons not recorded. Pull from Admin > Rules Browser (filter: flagged) before co-founder approval.

3. **4 contradiction pairs** — rule IDs and summaries not captured. Verify if genuine classical contradictions or validator false positives.

4. **39 pending_human_review rules** — awaiting co-founder sign-off. Not live until promoted to `approved`.

5. **BPHS Vol 1 complete (Ch 12-23, 360 rules total)** — next source is Vol 2. Confirm RTF file availability and chapter range before starting next batch.

---

### BPHS Vol 1 Grand Total (Ch 12-23)

| | Rules | auto_approved | pending_human_review | flagged | contradictions |
|---|---|---|---|---|---|
| Ch 12-18 | 241 | 140 (58%) | 79 (33%) | 28 (12%) | 9 pairs |
| Ch 19-23 | 119 | 70 (59%) | 39 (33%) | 10 (8%) | 4 pairs |
| **Grand Total** | **360** | **210 (58%)** | **118 (33%)** | **38 (11%)** | **13 pairs** |

---

### BPHS Ch 24 | Bhava Lords (all houses) | Apr 2026

**Script used:** `ingest_bphs_houses_v2.py` — extended with `--house 0` lord-placement mode
**Batch:**

| Ch | Topic | Batch ID | Total | auto_approved | pending_human_review | flagged | contradictions |
|---|---|---|---|---|---|---|---|
| 24 | Effects of Bhava Lords | bphs-ch24-v2-20260416 | 376 | 267 (71%) | 77 (20%) | 32 (9%) | 0 pairs |

**Sub-type breakdown:** lord_placement: 370 · aspect_rule: 4 · combination: 2

**Notable:**
- **71% auto_approved** — highest approval rate of any chapter so far (was 58% average for Ch 12-23). Lord-placement rules are cleaner if-then structures than house-occupation rules.
- **0 contradictions** — expected; lord×house combinations are by definition unique pairs.
- **Structural failures: 0/376** — clean ingest, no parser issues.
- 32 flagged rules — pull from Admin > Rules Browser (filter: flagged) before co-founder approval.
- 77 pending_human_review — awaiting co-founder sign-off. Not live until promoted to `approved`.

---

### BPHS Ch 47 | Effects of Dasas (Mahadasha by Planet) | Apr 2026

**Script used:** `ingest_bphs_dasha_v1.py` — new script, first run
**Batch:**

| Ch | Topic | Batch ID | Total | auto_approved | pending_human_review | flagged | contradictions |
|---|---|---|---|---|---|---|---|
| 47 | Effects of Dasas | bphs-ch47-dasha-20260416 | 93 | 76 (82%) | 13 (14%) | 4 (4%) | 0 pairs |

**Sub-type breakdown:** dasha_favourable: 52 · dasha_unfavourable: 28 · general_principle: 7 · dasha_conditional: 5 · dasha_remedy: 1

**By dasha_lord:** Venus: 15 · Mars: 13 · Rahu: 10 · Sun: 9 · Jupiter: 9 · (general): 9 · Saturn: 8 · Moon: 7 · Mercury: 7 · Ketu: 6

**Notable:**
- **82% auto_approved** — highest rate of any batch. Dasha if-then rules are structurally cleaner than house occupation rules.
- **Only 4 flagged rules** — exceptional quality.
- **0 contradictions** — expected; each planet's Dasha section covers distinct conditions.
- **Structural failures: 0/93** — clean ingest.
- 7 slokas skipped: 1, 2 (pure dialogue); 44, 52, 61, 71, 78 (single-sentence planet intros — no prediction content).
- Slokas 40-43 (Rahu continuation) recovered by zero-space period fix (`88-89.Similar` format also caught).
- Sloka 16-22 (Moon transition) correctly attributed via `detect_transition_planet()` forward-looking phrase detection.
- 9 "general" rules (slokas 3-4, 5-6) cover timing framework principles, not planet-specific — dasha_lord left empty.

---

### Cumulative Grand Total (All sources, Ch 12-24 + Ch 47)

| Source | Rules | auto_approved | pending_human_review | flagged | contradictions |
|---|---|---|---|---|---|
| BPHS Vol 1 Ch 12-18 | 241 | 140 (58%) | 79 (33%) | 28 (12%) | 9 pairs |
| BPHS Vol 1 Ch 19-23 | 119 | 70 (59%) | 39 (33%) | 10 (8%) | 4 pairs |
| BPHS Vol 1 Ch 24 | 376 | 267 (71%) | 77 (20%) | 32 (9%) | 0 pairs |
| BPHS Vol 2 Ch 47 | 93 | 76 (82%) | 13 (14%) | 4 (4%) | 0 pairs |
| **Grand Total** | **829** | **553 (67%)** | **208 (25%)** | **74 (9%)** | **13 pairs** |

---
