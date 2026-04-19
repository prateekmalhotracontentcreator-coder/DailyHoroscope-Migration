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

### Database (MANDATORY — read before every ingest)

**Production DB name: `horoscope_db`** — this is what Render's `DB_NAME` env var is set to.
All ingest and patch commands must use `--db-name horoscope_db`.
The `EverydayHoroscope` database was a local-only mistake; 3,200 rules were migrated to `horoscope_db` on 20 Apr 2026. Do NOT use `EverydayHoroscope` again.

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

### BPHS Ch 52-57 | Antardasha Chapters (Dasha of each planet) | Apr 2026

**Script used:** `ingest_bphs_dasha_v1.py`

| Ch | MD Lord | Batch ID | Total | auto_approved | pending_human_review | flagged | contradictions |
|---|---|---|---|---|---|---|---|
| 52 | Sun | bphs-ch52-dasha-* | — | — | — | — | — |
| 53 | Moon | bphs-ch53-dasha-* | — | — | — | — | — |
| 54 | Mars | bphs-ch54-dasha-20260417 | 86 | — | — | — | — |
| 55 | Rahu | bphs-ch55-dasha-* | — | — | — | — | — |
| 56 | Jupiter | bphs-ch56-dasha-20260418 | 126 | 103 (83%) | 16 (13%) | 5 (4%) | 0 pairs |
| **57** | **Saturn** | **bphs-ch57-dasha-20260419** | **132** | **103 (79%)** | **18 (14%)** | **9 (7%)** | **0 pairs** |

**Ch 57 Dry Run Notes (V2 — locked baseline):**
- 35 slokas / 120 rules / temperature=0 locked
- Confirmed per-sloka baseline:

| Sloka | Rules | Note |
|---|---|---|
| 1-3 | 6 | 6 condition-specific rules — verify distinctiveness in Rules Browser post-ingest |
| 4-5 | 3 | |
| 6-7 | 2 | |
| 8-11 | 5 | |
| 12-13 | 2 | Translator note ("It is difficult to believe…") correctly excluded |
| 14-15 | 2 | |
| 16-18 | 2 | Sat/Ketu negative even when well-placed — confirmed |
| 19 | 4 | |
| 20-21 | 4 | Over-split to 10 at temp=0.1; resolved at temp=0 |
| 22-23 | 2 | |
| 24-27 | 3 | |
| 28-29 | 3 | |
| 30-31 | 3 | |
| 32-34 | 8 | |
| 35-36 | 2 | |
| 37-38 | 2 | |
| 39-41 | 9 | |
| 42 | 2 | |
| 43-45 | 3 | |
| 46-48 | 3 | Translator note ("Our belief is…") correctly excluded |
| 49-50 | 3 | |
| 51-52 | 1 | |
| 53-54 | 2 | |
| 55-57 | 6 | |
| 58-60 | 5 | |
| **61-62** | **4** | **Was missing in V1 runs — RTF fixed + re-run confirmed capture** |
| 63-64 | 1 | |
| 65-67 | 2 | |
| 68 | 1 | Sign-placement rule (Rahu in Aries/Virgo/Cancer etc.) |
| 69-70 | 2 | |
| 71-73 | 3 | Under-split to 1 at temp=0.1; resolved at temp=0 |
| 74-75 | 3 | |
| 76-78 | 9 | |
| 79-80 | 5 | |
| 81-82 | 3 | |
| **TOTAL** | **120** | |

---

**Ch 57 Live Ingest Notes:**
- Live ingest produced 130 rules vs dry-run baseline of 120 (+10) despite temperature=0
- Diverging slokas: 8-11 (+1), 20-21 (+4), 30-31 (+5)
- 30-31 is highest priority for Rules Browser review — likely outcome over-splitting (8 rules from a 2-verse sloka)
- temperature=0 reduces but does not eliminate API variance — per-sloka baseline check remains essential
- `dasha_conditional: 1` from dry run absorbed into favourable/unfavourable in live run

**Gap-Fill Results (20 Apr 2026):**
- Sloka 51-52: +0 new (existing rule already covered)
- Sloka 63-64: +2 new (R-BPHS57-PATCH-29A148, R-BPHS57-PATCH-EC9BB1 — distinct Rahu conditions)
- **Ch 57 final total: 132 rules**

**Open Points:**
1. Verify 2 Rahu gap-fill rules are distinct — Rules Browser → filter `source_note: gap_fill`, batch `bphs-ch57-dasha-20260419`
2. Review 9 flagged rules in Rules Browser (filter: flagged, batch: bphs-ch57-dasha-20260419) — check slokas 20-21 and 30-31 for over-split duplicates
3. 18 pending_human_review + 2 gap-fill pending_review — awaiting co-founder sign-off

---

### BPHS Ch 58 | Mercury Mahadasha Antardasha | Apr 2026

**Script used:** `ingest_bphs_dasha_v1.py`
**Batch ID:** `bphs-ch58-dasha-20260419`
**Slokas:** 72 (1–72) | **Antardasha sections:** 9

| Ch | MD Lord | Batch ID | Total | auto_approved | pending_human_review | flagged | contradictions |
|---|---|---|---|---|---|---|---|
| 58 | Mercury | bphs-ch58-dasha-20260419 | 104 | 76 (73%) | 21 (20%) | 7 (7%) | 0 pairs |

*(Gap-fill for sloka 59-61 pending re-run after collection name fix — see Gap-Fill section)*

**Dry Run Baseline (2 runs — locked):**

| # | Sloka | Run 1 | Run 2 | Live | Note |
|---|---|---|---|---|---|
| 1 | 1-3 | 2 | 2 | 2 | |
| 2 | 4-5 | 3 | 3 | 3 | |
| 3 | 6-8 | 2 | 2 | 2 | |
| 4 | 9-11 | 7 | 7 | 7 | |
| 5 | 12 | 3 | 3 | 3 | |
| 6 | 13-15 | 2 | 2 | 2 | |
| 7 | 16-17 | 6 | 6 | 6 | |
| 8 | 18-19 | 2 | 2 | 2 | |
| 9 | 20-22 | 3 | 3 | 3 | |
| 10 | 23-24 | 3 | 3 | 3 | |
| 11 | 25 | 2 | 2 | 2 | |
| 12 | 26-27 | 4 | 4 | 4 | |
| 13 | 28-29 | 6 | 6 | 6 | |
| 14 | 30-31 | 2 | 2 | 2 | |
| 15 | 32-33 | 4 | 4 | 4 | Source typo: "6th, the 6th" should be "6th, the 8th" — rules captured as-is |
| 16 | 34-35 | 2 | 2 | 2 | |
| 17 | 36-38 | 6 | 6 | 6 | |
| 18 | 39-40 | 1 | 1 | 1 | Single condition sloka — 1 rule correct |
| 19 | 41-42 | 5 | 5 | 5 | |
| 20 | 43-44 | 3 | 3 | 3 | |
| 21 | 45-46 | 3 | 3 | 3 | |
| 22 | 47-49 | 3 | 3 | 3 | |
| 23 | 50 | 2 | 2 | 2 | |
| 24 | 51 | 2 | 2 | 2 | |
| 25 | 52-53 | 1 | 1 | 1 | Single condition sloka — 1 rule correct |
| 26 | 54-55 | 2 | 3 | 3 | ±1 remedy variance (Durga + Lakshmi mantras split/merged) |
| 27 | 56-58 | 2 | 2 | 2 | |
| 28 | **59-61** | **6** | **6** | **4** | **⚠️ Live −2 vs dry run — gap-fill candidate** |
| 29 | 62-63 | 1 | 1 | 1 | Single condition sloka — 1 rule correct |
| 30 | 64 | 1 | 1 | 1 | Source: "64-64" typo — captured correctly as sloka 64 |
| 31 | 65-66 | 2 | 2 | 2 | |
| 32 | 67-68 | 1 | 1 | 1 | |
| 33 | 69-70 | 8 | 8 | 8 | |
| 34 | 71-72 | 3 | 3 | 3 | |
| **Total** | | **105** | **106** | **104** | |

**Validation Results (20 Apr 2026):** 76 auto_approved (73%) · 21 pending_human_review (20%) · 7 flagged (7%) · 0 contradictions

**Gap-Fill Results (20 Apr 2026):**
- Sloka 59-61: +0 new — existing 4 rules already cover all conditions. "Live −2 vs dry run" was model variance, not under-extraction.
- **Ch 58 final total: 104 rules** (no gap-fill needed)

**Open Points:**
1. 7 flagged rules — review in Rules Browser (filter: flagged, batch: bphs-ch58-dasha-20260419)
2. 21 pending_human_review — awaiting co-founder sign-off
3. Source typo sloka 32-33: "6th, the 6th" (should be "6th, the 8th") — captured as-is; flag for human review

---

### Gap-Fill Protocol — Under-Extracted Slokas

> Applies to Ch 56, 57, 58 (and all future chapters). Run after validation completes for each chapter.

**Root cause:** The original `EXTRACTION_SYSTEM` prompt did not explicitly instruct the model to split slokas where multiple distinct planetary states (debilitation / combustion / house placement / malefic association) share the same outcome text. Fixed in commit after Ch 58 ingest — all Ch 59+ benefit automatically.

**Fix applied (ingest_bphs_dasha_v1.py):** Added `SPLITTING GUIDANCE` section to `EXTRACTION_SYSTEM` with explicit split/no-split examples.

**Gap-fill script:** `scripts/patch_slokas.py` — re-extracts specific sloka ranges using the improved prompt, deduplicates against existing MongoDB rules (60% word-overlap threshold), inserts only net-new rules with `source_note='gap_fill'` and `approval_status='pending_review'`.

#### Flagged slokas by chapter

| Ch | MD Lord | Batch ID | Sloka | Live count | Gap-fill result | Status |
|---|---|---|---|---|---|---|
| 57 | Saturn | bphs-ch57-dasha-20260419 | 51-52 | 1 | +0 (already covered) | ✅ Closed |
| 57 | Saturn | bphs-ch57-dasha-20260419 | 63-64 | 1 | +2 (20 Apr 2026) | ✅ Done |
| 58 | Mercury | bphs-ch58-dasha-20260419 | 59-61 | 4 | +0 (already covered) | ✅ Closed |
| 56 | Jupiter | bphs-ch56-dasha-20260418 | 33-34 | 1 | +2 (20 Apr 2026) | ✅ Done |

**Gap-fill commands (run after validation for each chapter):**

```bash
cd /Users/apple/DailyHoroscope-Migration/backend

# Ch 57 — Saturn MD gap-fill
python3 scripts/patch_slokas.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Ch 57 Vol 2.rtf" \
  --chapter 57 \
  --dasha-lord Saturn \
  --batch-id bphs-ch57-dasha-20260419 \
  --slokas "51-52,63-64" \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db \
  --dry-run

# Ch 58 — Mercury MD gap-fill
python3 scripts/patch_slokas.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_ch 58_Vol 2.rtf" \
  --chapter 58 \
  --dasha-lord Mercury \
  --batch-id bphs-ch58-dasha-20260419 \
  --slokas "59-61" \
  --mongo-url "$MONGO_URL" \
  --db-name horoscope_db \
  --dry-run
```

Remove `--dry-run` when satisfied with the dry-run output. New rules appear in Admin > Library > Rules Browser — filter by `source_note: gap_fill`.

---

### Cumulative Grand Total (All sources, as of 20 Apr 2026)

| Source | Rules | auto_approved | pending_human_review | flagged | contradictions |
|---|---|---|---|---|---|
| BPHS Vol 1 Ch 12-18 | 241 | 140 (58%) | 79 (33%) | 28 (12%) | 9 pairs |
| BPHS Vol 1 Ch 19-23 | 119 | 70 (59%) | 39 (33%) | 10 (8%) | 4 pairs |
| BPHS Vol 1 Ch 24 | 376 | 267 (71%) | 77 (20%) | 32 (9%) | 0 pairs |
| BPHS Vol 2 Ch 47 | 93 | 76 (82%) | 13 (14%) | 4 (4%) | 0 pairs |
| BPHS Vol 2 Ch 54 (Mars) | 86 | — | — | — | — |
| BPHS Vol 2 Ch 56 (Jupiter) | 126 | 103 (83%) | 16 (13%) | 5 (4%) | 0 pairs |
| BPHS Vol 2 Ch 57 (Saturn) | 132 | 103 (79%) | 18 (14%) | 9 (7%) | 0 pairs |
| BPHS Vol 2 Ch 58 (Mercury) | 104 | 76 (73%) | 21 (20%) | 7 (7%) | 0 pairs |
| **Grand Total** | **~1,277** | | | | |

---
