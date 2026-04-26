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

### Ingest script — `ingest_bphs_dasha_v1.py` + `patch_slokas.py`

| Fix | What it does | Trigger |
|---|---|---|
| `temperature=0` (both call sites, lines 268 + 308) | Makes Claude extraction deterministic — identical sloka text → identical rule count on every run | Ch 57 dry runs produced 113 vs 118 rules on two consecutive runs due to LLM non-determinism at temp=0.1. Over-split detected at sloka 20-21 (4 vs 10 rules); under-split at sloka 71-73 (1 vs 3 rules). |
| `condition.antardasha_planet` field added (commits 7df0fb9, 54f2b2c, 5ab6dd7) | All future dasha ingest stores the sub-period planet as a queryable field. `patch_slokas.py` updated to pass `antardasha_planet` into `extracted_to_rule()`. | Knowledge engine was filtering only on `dasha_lord` — all 9 antardashas returned together. Two-key filtering (`dasha_lord` + `antardasha_planet`) now required for correct rule matching. |
| `backfill_antardasha_planet.py` — 5-pass backfill (20–21 Apr 2026) | Populated `condition.antardasha_planet` on all 802 dasha rules across Ch 47–58. Pass 1: regex ("during X Antardasha"); Pass 2: planets_involved derivation; Pass 3: self_antardasha + first_planet_heuristic; Pass 4: extended to Ch 52/53/55 (261 rules); Pass 5: Ch 47/48 (85 auto + 6 manual Sun self-period + 2 universal tags). | 802/802 rules covered. 2 rules (R-BPHS47-008, R-BPHS47-009) tagged as universal — see Universal Rule Pattern below. |

### Universal Rule Pattern — Chapter-Opening Meta-Rules

> **Identified: 21 Apr 2026. Applies to all dasha chapters, all books.**

#### What they are

Every dasha chapter (and often every chapter in any source book) opens with **meta-rules** that describe general principles before splitting into planet-specific or antardasha-specific sub-sections. These rules are **not tied to a specific antardasha** — they apply universally across the entire Mahadasha, or across ALL Mahadasha lords.

Two distinct sub-types were identified in Ch 47:

| Sub-type | Example | Correct Treatment |
|---|---|---|
| **MD-opening general rules** | Drekkana timing rules (001–005, 007) — describe timing of effects within any planet's own Dasha | `antardasha_planet = dasha_lord` (self-period assignment — these occur before any antardasha section begins) |
| **Universal meta-rules** | "Dasa lord in exaltation → Favourable" (008–009) — `planets_involved` = all 9 planets, rule applies to ANY Mahadasha lord | `antardasha_planet = null` + `applies_to_all_dasha_lords = true` |

#### Detection signals (backfill and future ingest)

| Signal | Meaning |
|---|---|
| `planets_involved` = all 9 planets | Strong indicator of a universal meta-rule — no single antardasha owner |
| Rule ID at chapter start (001–00x) before any antardasha sub-section | Likely MD-opening general rule |
| Summary uses "Dasa lord" as a pronoun without naming a planet | Universal quality assessment rule |
| `antardasha_planet_method = 'unresolved'` after all backfill passes | Flag for manual universal-rule review |

#### Storage convention

```python
# Universal meta-rule (applies to any dasha lord)
{
  "condition.antardasha_planet": None,
  "condition.antardasha_planet_method": "universal_dasha_quality_rule",
  "condition.applies_to_all_dasha_lords": True
}

# MD-opening general rule (before antardasha sub-sections begin)
{
  "condition.antardasha_planet": "<same as dasha_lord>",
  "condition.antardasha_planet_method": "manual_general_md_opening"
}
```

#### Knowledge engine query behaviour

- Rules with `antardasha_planet = null` AND `applies_to_all_dasha_lords = true` → returned for **any** active Mahadasha, regardless of antardasha
- Rules with `antardasha_planet = dasha_lord` (self-period) → returned only during the self-antardasha sub-period (e.g. Sun/Sun, Jupiter/Jupiter)

#### Where to look in other books

| Book / Chapter type | Likely universal rules at |
|---|---|
| BPHS dasha chapters (Ch 47–58) | First 5–10 slokas before the first planet-named antardasha section |
| BPHS house chapters (Ch 12–24) | Opening slokas before "Sun in X house" sub-sections begin |
| A Text-Book of Astrology (Ch 15) | Chapter preamble before planet × house grid starts |
| Lal Kitab chapters | Opening principle slokas before house-specific entries |
| Any chapter with a planet-heading structure | Paragraphs before the first planet heading |

#### Pre-batch checklist additions (see Checklist section below)

### Validator — `knowledge_validator.py`

| Fix | What it does | Trigger |
|---|---|---|
| `structural_check` word-min lowered to 3 | Allows short planet_in_house / sign sub-rules to pass | Sub-rules with valid but brief interpretations were being rejected |

### Database (MANDATORY — read before every ingest)

**Production DB name: `horoscope_db`** — this is what Render's `DB_NAME` env var is set to.
All ingest and patch commands must use `--db-name horoscope_db`.
The `EverydayHoroscope` database exists on Render MongoDB with 3,200 stale rules (pre-split-upgrade snapshot, confirmed 24 Apr 2026). It is NOT a local-only DB — it lives on the same Render cluster. However it is a stale snapshot and must NOT be used for any ingest, query, or production operation. All ingest targets `horoscope_db` (4,117+ rules, current). Do NOT use `EverydayHoroscope`.

### Pre-Batch Checklist (run before every new ingest)

**Structure checks:**
- [ ] Inspect source RTF for numbered lists inside Notes/commentary sections — neutralize if present
- [ ] Check sloka heading format — any trailing alpha, missing periods, leading apostrophes, period-separated ranges (e.g. `61.62.` instead of `61-62`)
- [ ] Confirm translator editorial notes are NOT extracted as rules (e.g. "Our belief is…", "It is difficult to believe…")

**Universal Rule check (dasha chapters):**
- [ ] Read the first 10 slokas of the chapter before ingesting — identify any meta-rules (timing framework, Drekkana principles, general Dasha quality) that appear before the first named antardasha sub-section
- [ ] After ingest, query `rule_id` range 001–010 of the new batch — check if any have `planets_involved` = all 9 planets → tag as `applies_to_all_dasha_lords = true`, `antardasha_planet = null`
- [ ] Any rule with summary containing "Dasa lord" as a pronoun (not a named planet) is a universal quality rule → universal tag

**Universal Rule check (house/sign chapters):**
- [ ] Read opening slokas before the first "Sun in X house / sign" heading — these are general principles, not planet-specific
- [ ] After ingest, check rule IDs at batch start — confirm `condition.planet` is populated (should be by the planet-heading injection in `extract_text_from_docx`), else flag for manual review

**Ingest execution:**
- [ ] Run dry run — record per-sloka rule counts as the confirmed baseline
- [ ] Confirm 61-62-style verse ranges are captured (both runs of Ch 57 missed slokas 61-62 until RTF was corrected)
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

| Ch | MD Lord | Batch ID | Total (original) | Split-upgrade rules | auto_approved | pending_human_review | flagged | contradictions |
|---|---|---|---|---|---|---|---|---|
| 52 | Sun | bphs-ch52-dasha-20260416 | 93 | +139 (21 Apr) | — | — | — | — |
| 53 | Venus | bphs-ch53-dasha-20260417 | 72 | +123 (21 Apr) | — | — | — | — |
| 54 | Mars | bphs-ch54-dasha-20260417 | 86 | +121 (21 Apr) | — | — | — | — |
| 55 | Rahu | bphs-ch55-dasha-20260417 | 96 | +153 (21 Apr) | — | — | — | — |
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

### BPHS Ch 57 | Saturn Mahadasha — Split-Upgrade | 22 Apr 2026

**Script:** `patch_slokas.py --split-upgrade`
**Batch ID:** `bphs-ch57-dasha-20260419` | **Dasha lord:** Saturn | **Slokas:** 35 blocks
**Split-upgrade dry run result:** +174 net-new rules predicted
**Live ingest status:** ✅ COMPLETE (22 Apr 2026) — +126 net-new rules | 63 duplicates skipped
**Note:** Dry run predicted +174; live yielded +126 (−48). Divergence is temperature=0 LLM variance — within normal range. All inserted rules confirmed correct.

**Live ingest command:**
```bash
cd /Users/apple/DailyHoroscope-Migration/backend
python3 scripts/patch_slokas.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS ch 57 Vol 2.rtf" \
  --chapter 57 --dasha-lord Saturn \
  --batch-id bphs-ch57-dasha-20260419 \
  --slokas "1-3,4-5,6-7,8-11,12-13,14-15,16-18,19,20-21,22-23,24-27,28-29,30-31,32-34,35-36,37-38,39-41,42,43-45,46-48,49-50,51-52,53-54,55-57,58-60,61-62,63-64,65-67,68,69-70,71-73,74-75,76-78,79-80,81-82" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db \
  --split-upgrade
```

**Grouped outcome rule check — ✅ NO MIS-TAGGED RULES**
14 `dasha_grouped_outcome` rules inserted, all multi-condition (all contain comma or " or " in condition). No anomaly detected.

**Sloka 63-64 (flagged in dry run):** 0 new rules inserted (10 skipped as duplicates of 3 existing rules). Dry-run flag resolved — no mis-tagged grouped rule in live DB. No fix script needed.

**Key per-sloka highlights:**
- Sloka 4-5: +5 new (Saturn 8th/12th/malefic/middle/last-part timing rules — clean split)
- Sloka 16-18: +7 new (Ketu AD individual unfavourable placements)
- Sloka 43-45: +8 new (Moon AD favourable placements — full, exaltation, own sign, kendra, trikona, 11th, aspected by benefics + grouped)
- Sloka 65-67: +9 new (Rahu AD individual favourable placements + grouped)
- Sloka 12-13: +9 new (Mercury AD house placements × 2 reference points + grouped)

**Gap-fill results (22 Apr 2026) — `gap_fill_ch57_splits.py`:**

Per-sloka variance verified manually before gap-fill. 8 slokas queried via `verify_ch57_gaps.py`. Verdict per sloka:

| Sloka | Verdict | Reason |
|---|---|---|
| 1-3 | ✅ Covered | R-BPHS57-001–006 are individually-queryable originals |
| 14-15 | ⚠️ Gap | R-BPHS57-020 merged "2nd or 7th lord" — split required |
| 16-18 | ✅ Covered | R-BPHS57-023 (Ketu+Asc lord favourable) already in original ingest |
| 22-23 | ⚠️ Gap | R-BPHS57-036 merged "Ketu in 2nd or 7th house" — split required |
| 24-27 | ✅ Covered | R-BPHS57-039/040 (Jupiter/Saturn transit rules) in original ingest |
| 28-29 | ✅ Covered | R-BPHS57-041 (debilitation) + 042 (combust) individually present |
| 35-36 | ⚠️ Gap | R-BPHS57-060 merged "2nd or 7th lord" — split required |
| 65-67 | ⚠️ Gap | Middle-portion timing rule absent from all 11 existing rules |

7 gap-fill rules inserted via `scripts/gap_fill_ch57_splits.py` (direct insert, bypassing dedup):
- `R-BPHS57-PATCH-4B17E8-GF` — Mercury 2nd lord unfav (sl 14-15, split of R-BPHS57-020)
- `R-BPHS57-PATCH-60E6E0-GF` — Mercury 7th lord unfav (sl 14-15, split of R-BPHS57-020)
- `R-BPHS57-PATCH-92F798-GF` — Ketu in 2nd house unfav (sl 22-23, split of R-BPHS57-036)
- `R-BPHS57-PATCH-A31479-GF` — Ketu in 7th house unfav (sl 22-23, split of R-BPHS57-036)
- `R-BPHS57-PATCH-5F5F3B-GF` — Venus 2nd lord unfav (sl 35-36, split of R-BPHS57-060)
- `R-BPHS57-PATCH-DE1D14-GF` — Venus 7th lord unfav (sl 35-36, split of R-BPHS57-060)
- `R-BPHS57-PATCH-F0541B-GF` — Rahu middle-portion timing favourable (sl 65-67, new rule)

All 7: `approval_status='pending_review'`, `source_note='gap_fill'`

**Ch 57 split-upgrade totals — FINAL ✅**
- Original: 132 rules
- Split-upgrade live: +126 net-new (dry run predicted +174; −48 verified manually — 44 legitimately covered by original ingest, 4 slokas had genuine gaps)
- Gap-fill direct insert: +7
- **Total: 265 rules** ✅

**Open Points (split-upgrade):**
1. Validation not yet run — run `validate_rules.py --batch-id bphs-ch57-dasha-20260419` after full sweep complete
2. All split-upgrade rules have `approval_status='pending_review'`, `source_note='split_upgrade'`
3. Gap-fill rules tagged `source_note='gap_fill'`

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

### BPHS Ch 55 | Rahu Mahadasha Antardasha | 21 Apr 2026

**Script:** `patch_slokas.py --split-upgrade`
**Batch ID:** `bphs-ch55-dasha-20260417` | **Dasha lord:** Rahu | **Slokas:** 35 blocks
**Split-upgrade result:** +153 net-new rules | 37 duplicates skipped

**First chapter with GROUPED OUTCOME RULE (dasha_grouped_outcome):**
Ch 55 is the first chapter extracted under the full two-layer prompt (individual splits + grouped summary). Grouped rules fire correctly in 17 slokas. See Phase 3 note above for pre-Ch-55 chapter re-run scope.

**Sloka 21-24 — sub_type anomaly + fix (21 Apr 2026):**

Live ingest tagged all 7 individual Saturn placement split rules as `dasha_grouped_outcome` + `is_group_summary=True` instead of `dasha_conditional` + `is_group_summary=False`. Root cause: temperature=0 variance — model interpreted GROUPED OUTCOME RULE guidance differently in live run vs dry run.

Fix applied via direct DB update script:
- 7 individual rules updated: `sub_type → dasha_conditional`, `is_group_summary → False`
- 1 true grouped summary rule inserted: `R-BPHS55-PATCH-SAT2124-GRP` (`dasha_grouped_outcome`, `is_group_summary=True`, `condition_group_id=ch55-sl21-24-saturn-mixed`)
- Final state: 5 pre_split_merged + 7 dasha_conditional + 1 dasha_grouped_outcome = 13 rules ✅

**⚠️ Co-founder review flag — R-BPHS55-018/019/020/021/022 (sloka 21-24 pre_split_merged originals):**

These 5 original ingest rules all share the SAME merged condition summary ("Saturn in kendra, trikona, exaltation sign, own sign, moolatrikona, 3rd or 11th house during Rahu MD") but have mixed sub_types:
- R-BPHS55-018: `dasha_favourable` — outcome A
- R-BPHS55-019: `dasha_favourable` — outcome B
- R-BPHS55-020: `dasha_unfavourable` ← **incorrect sub_type** — source condition is favourable placement; unfavourable tag was an original ingest error
- R-BPHS55-021: `dasha_unfavourable` ← **incorrect sub_type** — same issue
- R-BPHS55-022: `dasha_favourable` — outcome C

**Action at co-founder review:** Mark all 5 as `deprecated` (part of the global pre_split_merged deprecation batch). Do NOT promote 018/021/022 to `approved` — their split-upgrade successors (7 individual + 1 grouped) are the correct rules.

**Pre-split_merged deprecation — ✅ COMPLETE (24 Apr 2026)**

Script: `scripts/deprecate_pre_split_merged.py`
Result: 425 rules deprecated across Ch 47/48/52–59 | 0 remaining non-deprecated
Verification: `col.count_documents({"metadata.source_note": "pre_split_merged", "approval_status": {"$ne": "deprecated"}})` → **0** ✅

**Open Points:**
1. Validation not yet run — run `validate_rules.py --batch-id bphs-ch55-dasha-20260417` after sweep complete
2. Sloka 21-24 fix confirmed ✅ — 13 rules, correct architecture
3. All split-upgrade rules have `approval_status='pending_review'`, `source_note='split_upgrade'` (or `gap_fill` for the SAT2124-GRP fix rule)

---

### BPHS Ch 58 | Mercury Mahadasha Antardasha — Split-Upgrade | 24 Apr 2026

**Script:** `patch_slokas.py --split-upgrade`
**Batch ID:** `bphs-ch58-dasha-20260419` | **Dasha lord:** Mercury | **Slokas:** 34 blocks
**Split-upgrade dry run result:** +166 net-new rules predicted | 13 duplicates skipped
**Live ingest status:** ✅ COMPLETE (24 Apr 2026) — +132 net-new rules | 42 duplicates skipped
**Note:** Dry run predicted +166; live yielded +132 (−34). Divergence explained by higher dedup against original ingest — dry run compared against pre_split_merged tagged originals (all showed `existing: 0`), live correctly deduplicated against actual DB content. No gap-fill needed.

**Live ingest command:**
```bash
cd /Users/apple/DailyHoroscope-Migration/backend
python3 scripts/patch_slokas.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_ch 58_Vol 2.rtf" \
  --chapter 58 --dasha-lord Mercury \
  --batch-id bphs-ch58-dasha-20260419 \
  --slokas "1-3,4-5,6-8,9-11,12,13-15,16-17,18-19,20-22,23-24,25,26-27,28-29,30-31,32-33,34-35,36-38,39-40,41-42,43-44,45-46,47-49,50,51,52-53,54-55,56-58,59-61,62-63,64,65-66,67-68,69-70,71-72" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db \
  --split-upgrade
```

**All slokas verified clean — no anomalies.**

Notable variance slokas (all resolved by dedup, no gaps):
- Sloka 13-15: −6 (Venus 5th/9th from Asc + 9th/11th from Mercury already in original ingest)
- Sloka 18-19 / 25 / 54-55: −3/−3/−4 (Venus, Sun, Rahu lord rules already captured by original)
- Sloka 1-3: +1 over dry run (live correctly added grouped unfavourable that dry run missed)

**Ch 58 split-upgrade totals — FINAL ✅**
- Original: 104 rules
- Split-upgrade live: +132 net-new
- Gap-fill: none needed
- **Total: 236 rules** ✅

**Open Points:**
1. Validation not yet run — run `validate_rules.py --batch-id bphs-ch58-dasha-20260419` after full sweep complete
2. All split-upgrade rules: `approval_status='pending_review'`, `source_note='split_upgrade'`

---

### BPHS Ch 59 | Ketu Mahadasha Antardasha | Apr 2026

**Script used:** `ingest_bphs_dasha_v1.py`
**Batch ID:** `bphs-ch59-dasha-20260421`
**Dasha lord:** Ketu | **Antardasha sections:** 9 (Ketu/Ketu → Ketu/Mercury)
**Slokas detected:** 33 blocks (slokas 1–79, with gap at 66 — absent from source)

**Parser fix applied before ingest:**
- Sloka 5-6 written as `5.6.` in RTF (period as range separator) — fixed by adding `.` to inner separator set in `split_into_sloka_blocks()` and normalising `5.6` → `5-6` on capture (commit afb78d8)
- Ch 59 added to `INTRO_SLOKAS_BY_CHAPTER` with empty skip set

**Source quality issue — Sloka 45-47 (Rahu AD in Ketu MD):**

> ⚠️ OCR corruption — manual review REQUIRED after ingest

The RTF contains multiple word-level omissions in this sloka:

| Corrupted | Correct reading |
|---|---|
| `"ins, cattle"` | `"grains, cattle"` |
| `"yavana ting"` | `"yavana king"` |
| `"dignitary A foreign"` | `"dignitary of a foreign"` |
| `"Rahu the Dasa"` | `"Rahu in the Dasa"` |
| `"his r sign"` | `"his own sign"` |
| `"the 11th, the or the 2nd"` | `"the 11th, the [3rd?] or the 2nd"` — **house number dropped** |

The missing house number in the final condition list means extracted rules for this sloka may drop or incorrectly represent one placement condition. After ingest, find rules from batch `bphs-ch59-dasha-20260421` with `source.sloka = "45-47"` in Rules Browser and manually verify the condition list against other BPHS translations.

**Universal rule check result:**
- No opening meta-rules — Ch 59 begins directly with Ketu/Ketu antardasha at sloka 1-2 ✅
- No `applies_to_all_dasha_lords` tagging needed for this chapter

**Dry Run Baseline (2 runs — locked):**

| Sloka | Run 1 | Run 2 | Live | Verdict |
|---|---|---|---|---|
| 1-2 | 3 | 5 | 3 | ⚠️ Gap-fill candidate — 9th/10th/4th lords should be split |
| 3-4 | 5 | 5 | 5 | ✅ |
| 5-6 | 5 | 5 | 5 | ✅ New sloka recovered by period-separator fix |
| 7-9 | 2 | 2 | 2 | ✅ |
| 10-11 | 1 | 1 | 1 | ✅ |
| 12-14 | 3 | 3 | 3 | ✅ |
| 15 | 2 | 3 | 2 | ⚠️ Minor — 2nd/7th lord rules may be merged |
| 16-17 | 1 | 1 | 1 | ✅ |
| 18-19 | 1 | 1 | 1 | ✅ |
| 20-21 | 1 | 1 | 4 | ✅ Confirmed correct — dry runs UNDER-extracted. Live correctly split kendra/trikona/2nd/11th as 4 distinct conditions |
| 22-24 | 4 | 4 | 4 | ✅ |
| 25-28 | 2 | 2 | 2 | ✅ |
| 29-30 | 2 | 2 | 2 | ✅ |
| 31-33 | 4 | 4 | 4 | ✅ |
| 34-36 | 3 | 3 | 3 | ✅ |
| 37-39 | 2 | 2 | 2 | ✅ |
| 40 | 1 | 1 | 1 | ✅ |
| 41-42 | 4 | 2 | 4 | ✅ Confirmed correct — Mars in 8th/12th/2nd from Ketu are 3 distinct conditions + 1 qualifier rule ("amidst evil effects, some auspicious effects also"). Run 2 under-extracted. |
| 43-44 | 2 | 2 | 2 | ✅ |
| 45-47 | 2 | 2 | 2 | ✅ OCR-corrected — stable |
| 48-50 | 3 | 3 | 3 | ✅ |
| 51-54 | 1 | 1 | 1 | ✅ |
| 55-56 | 2 | 3 | 3 | ✅ Run 2 confirmed correct |
| 57-58 | 1 | 1 | 1 | ✅ |
| 59-60 | 3 | 3 | 3 | ✅ |
| 61-62 | 2 | 2 | 2 | ✅ |
| 63-65 | 5 | 5 | 5 | ✅ |
| 67-68 | 3 | 3 | 3 | ✅ |
| 69-71 | 3 | 2 | 3 | ✅ Run 1 confirmed correct |
| 72 | 2 | 2 | 2 | ✅ |
| 73-74 | 4 | 4 | 4 | ✅ |
| 75-76 | 1 | 1 | 1 | ✅ |
| 77-79 | 4 | 4 | 4 | ✅ |
| **TOTAL** | 84 | 85 | **88** | |

**Validation Results (21 Apr 2026):** 55 auto_approved (62%) · 29 pending_human_review (33%) · 4 flagged (5%) · 0 contradictions · 0 structural failures

*Note: 62% auto_approved is lower than 73–83% average for other dasha chapters. Expected — Ketu rules are heavily conditional ("if Ketu be related to X lord...") which the validator correctly routes to human review.*

**Key learning — dry run vs live divergence (21 Apr 2026):**
Slokas 20-21 and 41-42 both showed dry run counts LOWER than live (1 vs 4, and 2 vs 4). In both cases the live run was correct — it properly applied SPLITTING GUIDANCE to produce one rule per distinct house placement. The dry runs under-extracted. **Rule: when live count is higher than dry run, always verify by reading the source sloka before rejecting. Higher count ≠ over-split.**

**Gap-Fill Results (21 Apr 2026):**
- Sloka 1-2: +3 new rules inserted (9th lord / 10th lord / 4th lord as individual rules). 3 duplicates correctly skipped (kendra / trikona / Asc lord already in DB). IDs: R-BPHS59-PATCH-FACB65, R-BPHS59-PATCH-5E398B, R-BPHS59-PATCH-2C21C9. `source_note='gap_fill'`, `approval_status='pending_review'`.
- Two-stage dedup fix required (commits 8ee9944, f34e97d): condition-only comparison (not full summary) + separate DB vs within-run thresholds (60% / 90%).

**Open Points:**
1. ✅ **Sloka 20-21** — 4 rules confirmed correct (dry runs under-extracted). No action needed.
2. ✅ **Sloka 41-42** — 4 rules confirmed correct (Mars in 8th/12th/2nd + qualifier). No action needed.
3. ⚠️ **Sloka 45-47** — OCR-corrected sloka — verify 9 extracted rules (post-split) capture all placement conditions correctly (kendra/trikona/11th/3rd/2nd + dignity states)
4. ✅ **Sloka 1-2** — Gap-fill complete: 6 rules now in DB (kendra/trikona/Asc lord from original + 9th/10th/4th lord from patch)
5. 4 flagged rules — review in Rules Browser (filter: flagged, batch: bphs-ch59-dasha-20260420)
6. 29 pending_human_review — awaiting co-founder sign-off
7. **Ch 59 final total: 91 rules** ✅ (88 original + 3 gap-fill)

---

### BPHS Ch 56 | Jupiter Mahadasha Antardasha — Split-Upgrade | 22 Apr 2026

**Script:** `patch_slokas.py --split-upgrade`
**Batch ID:** `bphs-ch56-dasha-20260418` | **Dasha lord:** Jupiter | **Slokas:** 36 blocks
**Split-upgrade dry run result:** +159 net-new rules | duplicates skipped
**Live ingest status:** ✅ COMPLETE (22 Apr 2026) — +118 net-new rules | 57 duplicates skipped
**Note:** Dry run predicted +159; live yielded +118 (−41). Divergence is temperature=0 model variance across sloka re-extractions. All inserted rules confirmed correct — no under-extraction detected. Sloka 72-75 anomaly present (see fix section below).

**Live ingest command:**
```bash
cd /Users/apple/DailyHoroscope-Migration/backend
python3 scripts/patch_slokas.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Ch56_Vol 2.rtf" \
  --chapter 56 --dasha-lord Jupiter \
  --batch-id bphs-ch56-dasha-20260418 \
  --slokas "1-3,4-5,6-7,8-11,12-14,15,16-17,18-19,20-21,22,23-24,25-26,27-28,29-29,30-31,32,33-34,35-36,37-38,39-43,44,45-47,48-50,51-53,54-55,56-57,58-60,61-63,64,65-66,67-68,69-71,72-75,76-78,79-80" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db \
  --split-upgrade
```

**⚠️ Sloka 72-75 — sub_type anomaly (post-live fix required)**

In the dry run, `R-BPHS56-PATCH-D1BCEE` was incorrectly tagged `dasha_grouped_outcome` + `is_group_summary=True`, but its summary reads "Rahu in exaltation → ..." — a single-condition individual rule. The true grouped summary (covering all 7 Rahu conditions) was never inserted.

After live ingest, run the query-based fix script (does NOT rely on hardcoded rule_id):

```bash
cd /Users/apple/DailyHoroscope-Migration/backend
python3 scripts/fix_ch56_sl7275.py --mongo-url "$MONGO_URL"
# Dry run first: add --dry-run flag
```

Script actions (22 Apr 2026 — `scripts/fix_ch56_sl7275.py`):
1. Queries sloka 72-75 for any `is_group_summary=True` rules — finds the mis-tagged one
2. Updates it: `sub_type → dasha_favourable`, `is_group_summary → False`
3. Composes grouped summary from all 7 individual rule outcomes
4. Inserts the true `dasha_grouped_outcome` rule with `condition_group_id`
5. Back-fills `condition_group_id` on all individual rules

Same pattern as Ch 55 sloka 21-24. Root cause: temperature=0 LLM variance in live vs dry run.

**Phase 3 candidates — slokas missing grouped outcome rules (DEFERRED):**

| Sloka | Condition count | Type | Notes |
|---|---|---|---|
| 33-34 | 4 | unfavourable | 4 Jupiter AD malefic placement conditions |
| 44 | 7 | unfavourable | 7 Saturn conditions |
| 51-53 | 7 | favourable | 7 Sun favourable placements |
| 54-55 | 6 | unfavourable | 6 Sun unfavourable from Asc/Jupiter |
| 61-63 | 8 | unfavourable | 8 Moon conditions — largest group |
| 65-66 | 4 | favourable | 4 Mars dignity-state conditions |

Individual split rules will be inserted by split-upgrade. Grouped summaries deferred to Phase 3 sweep after full split-upgrade sweep is complete.

**Ch 56 totals — FINAL ✅**
- Original: 126 rules
- Split-upgrade live: +118 net-new (dry run predicted +159; −41 = temperature=0 LLM divergence)
- Flag 1 fix (22 Apr 2026): +2 true grouped outcome rules; 2 mis-tagged rules retyped
  - Sloka 72-75: `R-BPHS56-PATCH-66C586-GRP` (Rahu AD, 8 conditions, `ch56-sl7275-rahu-favourable`)
  - Sloka 51-53: `R-BPHS56-PATCH-34CC52-GRP` (Sun AD, 8 conditions, `ch56-sl5153-sun-favourable`)
  - condition_group_id back-filled on 16 individual rules (8 per sloka)
- **Total: 246 rules** ✅

**Open Points:**
1. ✅ Live ingest complete (+118)
2. ✅ Flag 1 fix complete — slokas 72-75 and 51-53 corrected
3. Phase 3 pass — 6 slokas need grouped summary rules (deferred)
4. Validation not yet run — run `validate_rules.py --batch-id bphs-ch56-dasha-20260418` after sweep complete

---

### BPHS Ch 59 | Ketu Mahadasha Antardasha — Split-Upgrade | 24 Apr 2026

**Script:** `patch_slokas.py --split-upgrade`
**Batch ID:** `bphs-ch59-dasha-20260421` | **Dasha lord:** Ketu | **Slokas:** 33 blocks
**Split-upgrade dry run result:** +189 net-new rules | 11 duplicates skipped
**Live ingest status:** ✅ COMPLETE (24 Apr 2026) — +195 net-new rules | 11 duplicates skipped
**Note:** Live outperformed dry run by +6. Divergence explained by deeper compound splitting on sloka 51-54 (Jupiter dignity × placement × lordship combos) and additional grouped/conditional rules on slokas 3-4, 29-30, 55-56. All rules confirmed correct.

**Live ingest command:**
```bash
cd /Users/apple/DailyHoroscope-Migration/backend
python3 scripts/patch_slokas.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_ch59_Vol2.rtf" \
  --chapter 59 --dasha-lord Ketu \
  --batch-id bphs-ch59-dasha-20260421 \
  --slokas "1-2,3-4,5-6,7-9,10-11,12-14,15,16-17,18-19,20-21,22-24,25-28,29-30,31-33,34-36,37-39,40,41-42,43-44,45-47,48-50,51-54,55-56,57-58,59-60,61-62,63-65,67-68,69-71,72,73-74,75-76,77-79" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db \
  --split-upgrade
```

**⚠️ Sloka 69-71 — sub_type fix applied (24 Apr 2026)**

4 Mercury placement rules (kendra/trikona/exaltation/own sign from Asc) were inserted as `dasha_grouped_outcome` by the LLM at temperature=0. Fixed immediately post-ingest via direct DB update:
- R-BPHS59-PATCH-4AE617, R-BPHS59-PATCH-59441A, R-BPHS59-PATCH-81F8E6, R-BPHS59-PATCH-BE8BF0
- Updated: `sub_type → dasha_favourable`, `is_group_summary → False`
- Verified: 0 remaining `dasha_grouped_outcome` in sloka 69-71 ✅

**Ch 59 split-upgrade totals — FINAL ✅**
- Original: 91 rules
- Split-upgrade live: +195 net-new
- Gap-fill: none needed
- **Total: 286 rules** ✅

**Open Points:**
1. Validation not yet run — run `validate_rules.py --batch-id bphs-ch59-dasha-20260421` after full sweep complete
2. All split-upgrade rules: `approval_status='pending_review'`, `source_note='split_upgrade'`

---

### BPHS Ch 47 | Sun Mahadasha — Split-Upgrade | 24 Apr 2026

**Script:** `patch_slokas.py --split-upgrade`
**Batch ID:** `bphs-ch47-dasha-20260416` | **Dasha lord:** Sun | **Slokas:** 17 blocks
**Split-upgrade dry run result:** +153 net-new rules | 0 duplicates skipped (corrected spec)
**Live ingest status:** ✅ COMPLETE (24 Apr 2026) — +126 net-new rules | 23 duplicates skipped
**Note:** Dry run predicted +153; live yielded +126 (−27). Divergence explained by higher dedup against original ingest — pre_split_merged excluded from dry run count but present in live dedup. Normal range.

**⚠️ Wrong sloka spec — first dry run (detected and corrected before live):**

Initial dry run used fine-grained blocks (7-9, 10-11, 12-14...) that didn't match the original ingest's sloka references stored in MongoDB (7-11, 12-15, 16-22...). Script silently skipped 15 of 18 blocks; only 3 with matching refs processed → +18 rules.

Fix: Read original extraction log `BPHS Ch 47 Vol 2_Rule Extraction_16.04.26.rtf` to recover true sloka groupings, then confirmed via DB aggregate on `bphs-ch47-dasha-20260416` + `pre_split_merged` tag → 17 exact sloka references. Corrected spec used for dry run V2 (+153) and live run.

**Live ingest command (corrected spec):**
```bash
cd /Users/apple/DailyHoroscope-Migration/backend
python3 scripts/patch_slokas.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Ch 47 Vol 2.rtf" \
  --chapter 47 --dasha-lord Sun \
  --batch-id bphs-ch47-dasha-20260416 \
  --slokas "5-6,7-11,12-15,16-22,23-26,27-32,33,40-43,45-48,49-51,53-56,57-60,62-65,66-70,72-77,79-82,88-89" \
  --mongo-url "$MONGO_URL" --db-name horoscope_db \
  --split-upgrade
```

**Per-sloka variance (dry V2 vs live):**

| Sloka | Dry +153 | Live +126 | Delta | Note |
|---|---|---|---|---|
| 5-6 | +9 | +9 | 0 | ✅ |
| 7-11 | +11 | +7 | −4 | 3 skipped — Jupiter/Venus strength variants already in original |
| 12-15 | +9 | +8 | −1 | Grouped outcome dropped (pre_split_merged matched) |
| 16-22 | +14 | +13 | −1 | 1 skipped — Moon in trikona already in original |
| 23-26 | +11 | +7 | −4 | 4 skipped — Mars timing/middle period variants present |
| 27-32 | +10 | +7 | −3 | 3 skipped — Rahu association rules present |
| 33 | +9 | +4 | −5 | 3 skipped — Mars debilitation/weak/malefic aspect already in original |
| 40-43 | +7 | +6 | −1 | Yogakaraka rule skipped (already present) |
| **45-48** | **+8** | **+7** | **−1** | **⚠️ ALL 7 tagged dasha_grouped_outcome — fix required (see below)** |
| 49-51 | +5 | +5 | 0 | ✅ |
| 53-56 | +9 | +9 | 0 | ✅ |
| 57-60 | +10 | +11 | +1 | Saturn Sagittarius/Pisces split into two separate rules (correct) |
| 62-65 | +8 | +9 | +1 | Extra Mercury 9th house rule (correct — deeper split) |
| 66-70 | +7 | +3 | −4 | 4 skipped — phase-timing and malefic assoc already in original |
| 72-77 | +16 | +13 | −3 | 3 skipped |
| 79-82 | +6 | +6 | 0 | ✅ |
| 88-89 | +4 | +2 | −2 | 2 skipped |
| **TOTAL** | **+153** | **+126** | **−27** | |

**✅ Sloka 45-48 — sub_type fix applied (24 Apr 2026)**

All 7 Jupiter placement split-upgrade rules were mis-tagged as `dasha_grouped_outcome` + `is_group_summary=True`. Fixed immediately post-ingest via `scripts/fix_ch47_sl4548.py`:

| Rule ID | Placement | Fix applied |
|---|---|---|
| R-BPHS47-PATCH-B8A049 | Jupiter in exaltation | → `dasha_favourable`, `is_group_summary=False` |
| R-BPHS47-PATCH-55D246 | Jupiter in own sign | → `dasha_favourable`, `is_group_summary=False` |
| R-BPHS47-PATCH-13CAF4 | Jupiter in moolatrikona | → `dasha_favourable`, `is_group_summary=False` |
| R-BPHS47-PATCH-E06033 | Jupiter in 10th house | → `dasha_favourable`, `is_group_summary=False` |
| R-BPHS47-PATCH-0FC7A3 | Jupiter in 5th house | → `dasha_favourable`, `is_group_summary=False` |
| R-BPHS47-PATCH-465D0D | Jupiter in 9th house | → `dasha_favourable`, `is_group_summary=False` |
| R-BPHS47-PATCH-A7EE90 | Jupiter in own or exalted Navamsa | → `dasha_favourable`, `is_group_summary=False` |

True grouped outcome rule inserted: `R-BPHS47-PATCH-235E47-GRP` (`dasha_grouped_outcome`, `is_group_summary=True`, `condition_group_id=ch47-sl4548-jupiter-favourable`)
`condition_group_id` back-filled on all 7 individual rules.
Remaining `dasha_grouped_outcome` (split_upgrade) in sloka 45-48: **0** ✅

**Ch 47 split-upgrade totals — FINAL ✅**
- Original: 93 rules
- Split-upgrade live: +126 net-new
- Sloka 45-48 fix: 7 retyped + 1 grouped inserted (net +1)
- Gap-fill: none needed
- **Total: 220 rules** ✅ (93 + 126 + 1 grouped)

**Open Points:**
1. Validation not yet run — run `validate_rules.py --batch-id bphs-ch47-dasha-20260416` after sweep complete
2. All split-upgrade rules: `approval_status='pending_review'`, `source_note='split_upgrade'`

---

### Phase 3 — Grouped Outcome Rules (Pre Co-Founder Review, after Phase 1 ingest complete)

> **Identified: 21 Apr 2026 (Ch 55 sloka 8-12 analysis). Fix applied to extraction prompt 21 Apr 2026.**

#### What it is

When a sloka lists multiple distinct life-domain outcomes under the SAME astrological condition,
the extraction now produces two layers:

- **Layer 1 — Individual outcome rules** (`is_group_summary = false`): one rule per outcome — serve specific Q&A ("Will I gain a vehicle this period?")
- **Layer 2 — ONE grouped summary rule** (`sub_type = dasha_grouped_outcome`, `is_group_summary = true`): all outcomes combined into one paragraph — serves General Period Report generation with zero grouping logic in the report layer

Both layers carry the same `condition_group_id` (e.g. `"ch55-sl8-12-jupiter-favourable"`) for linking.

#### Fix applied (21 Apr 2026)

- `VALID_SUB_TYPES` extended with `"dasha_grouped_outcome"`
- `ExtractedRule` model: `condition_group_id: str = ""` and `is_group_summary: bool = False` added
- `EXTRACTION_SYSTEM`: new `GROUPED OUTCOME RULE` section added; `sub_type` list updated
- `extracted_to_rule()`: `condition_group_id` and `is_group_summary` persisted to `condition` subdoc; `group_summary` and `group:<id>` tags added for Rules Browser filtering
- `infer_strength_band_from_condition()`: `dasha_grouped_outcome` → `"medium"`

All chapters from **Ch 55 onwards** benefit automatically.

#### Phase 3 re-run scope

Chapters ingested **before** this fix (Ch 47, 48, 52, 53, 54, 56, 57, 58, 59) are missing grouped summary rules for any slokas where 3+ individual outcome rules share the same base condition. These chapters will need a targeted `patch_slokas.py --split-upgrade` pass specifically to generate the grouped summary rules.

**When to do this:** Before co-founder review of each batch, after Phase 1 ingest is complete. Zero rules are live — this is an enhancement, not a data error.

**Query to find candidates in pre-fix chapters:**
```python
# Find slokas in pre-fix chapters that already have 3+ individual rules but no grouped rule
import pymongo
client = pymongo.MongoClient("YOUR_MONGO_URL")
col = client["horoscope_db"]["interpretation_rules"]
# Rules with condition_group_id = None (pre-fix) grouped by sloka, count > 2
pipeline = [
    {"$match": {"source.batch_id": {"$regex": "bphs-ch(47|48|52|53|54|56|57|58|59)"},
                "condition.is_group_summary": {"$exists": False}}},
    {"$group": {"_id": {"batch": "$source.batch_id", "sloka": "$source.sloka"},
                "count": {"$sum": 1}}},
    {"$match": {"count": {"$gte": 3}}},
    {"$sort": {"count": -1}}
]
for doc in col.aggregate(pipeline):
    print(f"  {doc['_id']['batch']} sloka {doc['_id']['sloka']} → {doc['count']} rules")
```

---

### Phase 2 — Lordship Qualifier Compound Rules (Post Co-Founder Approval)

> **Identified: 21 Apr 2026 (Ch 54 sloka 64-66). Deferred to Phase 2.**

#### What it is

Some slokas combine a placement list WITH a lordship qualifier in a single condition:

> "Sun in exaltation, own sign, kendra, trikona or 11th, **associated with lord of 10th** → great gain"

The individual placement rules (Sun in exaltation / own sign / kendra / trikona / 11th) are split correctly by the ALWAYS SPLIT guidance. But the compound rule — "Sun in [any of those placements] **AND** associated with lord of 10th" — is a distinct, independently queryable condition with higher astrological specificity. It should be extracted as a separate rule.

#### Fix applied (21 Apr 2026)

Added **KEEP AS ONE RULE — point 4: LORDSHIP QUALIFIER COMPOUND RULES** to `EXTRACTION_SYSTEM` in `ingest_bphs_dasha_v1.py`. All chapters from Ch 55 onwards will benefit automatically.

#### Phase 2 audit scope

Chapters ingested **before** this fix (Ch 47, 48, 52, 53, 54 split-upgrade patches, Ch 56, 57, 58, 59 original ingests) may have silently absorbed or dropped lordship qualifier compound rules. A targeted audit is needed:

1. Query each pre-fix batch for rules whose `full_condition` contains "associated with lord", "with lord of", "as lord of", "combined with lord" — these are candidates where the compound rule may not exist as a standalone.
2. For each candidate, check whether a corresponding compound rule (placement + lordship) was separately extracted.
3. If missing, run `patch_slokas.py --split-upgrade` on the affected slokas to insert the compound rule.

#### Why deferred

Zero rules are live (`approval_status = pending_review`). The missing compound rules are an enhancement (additional specificity), not a data error. Existing individual placement rules still fire correctly for basic queries. Address before co-founder approval of each batch.

---

### Gap-Fill Protocol — Under-Extracted Slokas

> Applies to Ch 56, 57, 58 (and all future chapters). Run after validation completes for each chapter.

**Root cause:** The original `EXTRACTION_SYSTEM` prompt did not explicitly instruct the model to split slokas where multiple distinct planetary states (debilitation / combustion / house placement / malefic association) share the same outcome text. Fixed in commit after Ch 58 ingest — all Ch 59+ benefit automatically.

**Fix applied (ingest_bphs_dasha_v1.py):** Added `SPLITTING GUIDANCE` section to `EXTRACTION_SYSTEM` with explicit split/no-split examples.

**Gap-fill script:** `scripts/patch_slokas.py` — re-extracts specific sloka ranges using the improved prompt, deduplicates against existing MongoDB rules (60% word-overlap threshold), inserts only net-new rules with `source_note='gap_fill'` and `approval_status='pending_review'`.

### Split-Upgrade Sweep — Ch 47–59 (21 Apr 2026)

**Scope:** 425 rules across Ch 47/48/52/53/54/55/56/57/58/59 identified by `assess_undersplit.py` as merged-condition rules (house lists or dignity bundles in one condition). Assessment script at `/tmp/assess_undersplit.py`.

**Mechanism:**
1. All 425 rules tagged `metadata.source_note = 'pre_split_merged'` via `/tmp/tag_presplit_merged.py`
2. `patch_slokas.py --split-upgrade` excludes pre_split_merged from dedup, tags new rules as `split_upgrade`
3. New individual-condition rules inserted alongside originals — nothing deleted until co-founder review

**Additional fixes applied during this sweep:**
- `max_tokens` raised from 2048 → 4096 (commit f1fd623) — prevents JSON truncation on large slokas
- `patch_slokas.py` dedup uses condition-only comparison + two-tier thresholds (60% DB / 90% within-run)

**Correct RTF paths for this sweep:**

| Ch | MD Lord | RTF filename |
|---|---|---|
| 47 | Sun | `BPHS Ch 47 Vol 2.rtf` |
| 48 | Moon | `BPHS Ch 48 Vol 2.rtf` |
| 52 | Sun | `BPHS Ch 52 Vol 2.rtf` |
| 53 | Venus | `BPHS Ch 53_Vol 2_ Sloka 53,54,55 missing from Book.rtf` |
| 54 | Mars | `BPHS Ch 54 Vol 2.rtf` |
| 55 | Moon | `BPHS ch 55 Vol 2.rtf` |
| 56 | Jupiter | `BPHS_Ch56_Vol 2.rtf` |
| 57 | Saturn | `BPHS ch 57 Vol 2.rtf` |
| 58 | Mercury | `BPHS_ch 58_Vol 2.rtf` |
| 59 | Ketu | `BPHS_ch59_Vol2.rtf` |

**Progress:**

| Ch | MD Lord | Batch ID | Candidates | Dry Run | Live | New Rules |
|---|---|---|---|---|---|---|
| 48 | Moon | bphs-ch48-dasha-20260416 | 9 | ✅ +34 | ✅ 21 Apr | +34 |
| 52 | Sun | bphs-ch52-dasha-20260416 | 45 | ✅ +136 | ✅ 21 Apr | +139 |
| 53 | Venus | bphs-ch53-dasha-20260417 | 41 | ✅ +123 | ✅ 21 Apr | +123 |
| 54 | Mars | bphs-ch54-dasha-20260417 | 27 | ✅ +113 | ✅ 21 Apr | +121 |
| 55 | Rahu | bphs-ch55-dasha-20260417 | 42 | ✅ +150 dry | ✅ 21 Apr | +153 |
| 56 | Jupiter | bphs-ch56-dasha-20260418 | 72 | ✅ +159 dry (22 Apr) | ✅ 22 Apr | +120 (+118 split + 2 grouped fix) |
| 57 | Saturn | bphs-ch57-dasha-20260419 | 56 | ✅ +174 dry | ✅ 22 Apr | +126 |
| 58 | Mercury | bphs-ch58-dasha-20260419 | 58 | ✅ +166 dry (24 Apr) | ✅ 24 Apr | +132 (dry −34 = dedup vs original) |
| 59 | Ketu | bphs-ch59-dasha-20260421 | 37 | ✅ +189 dry (24 Apr) | ✅ 24 Apr | +195 (live +6 over dry — compound splits on sl 51-54); sl 69-71 sub_type fix applied |
| 47 | Sun | bphs-ch47-dasha-20260416 | 39 | ✅ +153 dry (24 Apr) | ✅ 24 Apr | +126 (dry −27 = dedup vs original); sl 45-48 sub_type fix required — see script fix_ch47_sl4548.py |

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

### Cumulative Grand Total (All sources, as of 21 Apr 2026)

| Source | Rules in DB | Notes |
|---|---|---|
| BPHS Vol 1 Ch 12-18 | 241 | 140 auto / 79 pending_human / 28 flagged / 9 contradiction pairs |
| BPHS Vol 1 Ch 19-23 | 119 | 70 auto / 39 pending_human / 10 flagged / 4 contradiction pairs |
| BPHS Vol 1 Ch 24 | 376 | 267 auto / 77 pending_human / 32 flagged / 0 contradictions |
| BPHS Vol 2 Ch 47 (Sun MD) | 220 | 93 original + 126 split-upgrade (24 Apr) + 1 grouped fix (R-BPHS47-PATCH-235E47-GRP) — sl 45-48 fix ✅; not validated |
| BPHS Vol 2 Ch 48 (Moon MD) | 80 | 46 original + 34 split-upgrade (21 Apr) — not validated |
| BPHS Vol 2 Ch 52 (Sun MD) | 232 | 93 original + 139 split-upgrade (21 Apr) — not validated |
| BPHS Vol 2 Ch 53 (Venus MD) | 195 | 72 original + 123 split-upgrade (21 Apr) — not validated |
| BPHS Vol 2 Ch 54 (Mars MD) | 207 | 86 original + 121 split-upgrade (21 Apr) — not validated |
| BPHS Vol 2 Ch 55 (Rahu MD) | 249 | 96 original + 153 split-upgrade (21 Apr) — not validated |
| BPHS Vol 2 Ch 56 (Jupiter MD) | 246 | 103 auto / 16 pending_human / 5 flagged — split-upgrade +118 + Flag 1 fix (+2grp) = 246 total |
| BPHS Vol 2 Ch 57 (Saturn MD) | 265 | 103 auto / 18 pending_human / 9 flagged — split-upgrade +126 + gap-fill +7; 265 total |
| BPHS Vol 2 Ch 58 (Mercury MD) | 236 | 76 auto / 21 pending_human / 7 flagged — split-upgrade +132 (24 Apr); total 236; no gap-fill needed |
| BPHS Vol 2 Ch 59 (Ketu MD) | 286 | 55 auto / 29 pending_human / 4 flagged — split-upgrade +195 (24 Apr); sl 69-71 sub_type fix applied; total 286 |
| BPHS Vol 2 Ch 60 (Venus MD) | 194 | 182 original + 12 split-upgrade (24 Apr 2026) — not validated |
| **RTF Grand Total** | **~2,500** | Includes all split-upgrade rules through Ch 47/48/52–60. |

**`condition.antardasha_planet` coverage (as of 21 Apr 2026):**
- Ch 47–59 dasha rules: **802 / 802 = 100%** ✅ (original ingests — split-upgrade rules carry antardasha_planet from source context)
- 2 rules tagged `applies_to_all_dasha_lords = true` (universal quality meta-rules: R-BPHS47-008, R-BPHS47-009)
- 6 rules assigned `antardasha_planet = Sun` via `manual_general_md_opening` (Drekkana/strength principles at Ch 47 opening)

**Split-upgrade sweep — current status (22 Apr 2026):**
- ✅ Ch 48 (Moon MD): +34 rules — complete
- ✅ Ch 52 (Sun MD): +139 rules — complete
- ✅ Ch 53 (Venus MD): +123 rules — complete
- ✅ Ch 54 (Mars MD): +121 rules — complete
- ✅ Ch 55 (Rahu MD): +153 rules — complete (21 Apr 2026)
- ✅ Ch 56 (Jupiter MD): +118 split + 2 grouped fix = +120 — complete (22 Apr 2026); Flag 1 fix applied
- ✅ Ch 57 (Saturn MD): +126 rules — complete (22 Apr 2026); no flags
- ✅ Ch 58 (Mercury MD): +132 rules — complete (24 Apr 2026); no gap-fill needed; total 236 rules
- ✅ Ch 59 (Ketu MD): +195 rules — complete (24 Apr 2026); sl 69-71 sub_type fix applied; total 286 rules
- ✅ Ch 47 (Sun MD general): +126 rules — complete (24 Apr 2026); sl 45-48 sub_type fix applied (7 retyped + 1 grouped inserted); total 220 rules

**🎉 SPLIT-UPGRADE SWEEP COMPLETE — all 10 chapters done (Ch 47/48/52–59)**

**Next ingest targets:**
- ✅ `fix_ch47_sl4548.py` complete — sloka 45-48 sub_type fix applied (7 retyped + 1 grouped inserted)
- ✅ **BPHS Ch 60 (Venus MD)** — ingested + split-upgrade complete (24 Apr 2026), **194 rules total**
- ✅ **`pre_split_merged` deprecation complete** (24 Apr 2026) — 425 rules deprecated across Ch 47/48/52–59; 0 remaining
- ✅ **Vol 1 house chapter assessment complete** (24 Apr 2026) — 59/736 candidates (8%); decision: no blanket split-upgrade; flag for co-founder human review
- ✅ **`ingest_bphs_houses_v2.py` upgraded** (24 Apr 2026) — SPLITTING GUIDANCE + temperature=0 + max_tokens=4096; ready for all future house chapter ingests
- ✅ **Text-Book of Astrology Ch 15** — ingested 24 Apr 2026, **1,530 rules total** (`tba-ch15-v1-20260424`)
- Run `validate_rules.py --batch-id` for each batch: Ch 52/53/54/55/56/57/58/59/47/48/60 + `tba-ch15-v1-20260424`
- Co-founder review of all pending_review rules across all batches (~4,000+ rules)

---

### BPHS Ch 60 | Venus Mahadasha Antardasha | 24 Apr 2026

**Script used:** `ingest_bphs_dasha_v1.py`
**Batch ID:** `bphs-ch60-dasha-20260424`
**Dasha lord:** Venus | **Antardasha sections:** 9 (Venus/Venus → Venus/Ketu)
**Slokas detected:** 30 blocks (slokas 1–74, merged continuations at 21-23, 38-41, 67-69)

**Parser fixes applied before ingest:**
- `_join_standalone_headings()` added to `split_into_sloka_blocks()` — Word-exported RTF places bold sloka headings on their own line; function joins heading line with following text line before sloka_re runs
- `60: set()` added to `INTRO_SLOKAS_BY_CHAPTER` — slokas 1-2 are real Venus/Venus AD prediction content, not dialogue intro
- `max_tokens` raised from 4096 → 8192 in `SlokaExtractor.extract()` — sloka 21-23 (Moon AD, 7+ placement conditions + merged continuation) hit the 4096 token output limit in dry run; raised to prevent JSON truncation

**RTF merges applied before ingest (3 continuation slokas):**
- Sloka 23 ("In the above circumstances...") merged into sloka 21-22 → heading renamed `21-23.`
- Slokas 40-41 ("Good effects will be experienced...") merged into sloka 38-39 → heading renamed `38-41.`
- Sloka 69 ("There will also be blessings...") merged into sloka 67-68 → heading renamed `67-69.`

**Sub-type breakdown:**

| Sub-type | Count |
|---|---|
| dasha_favourable | 90 |
| dasha_unfavourable | 63 |
| dasha_grouped_outcome | 18 |
| dasha_remedy | 9 |
| dasha_conditional | 2 |
| **TOTAL** | **182** |

**Per-sloka breakdown:**

| # | Sloka | Rules | Note |
|---|---|---|---|
| 1 | 1-2 | 13 | Venus/Venus AD — rich opening sloka (exaltation, own sign, navamsa, kendra/trikona/11th, 3rd/6th/11th, 6th/8th/12th, 2nd/7th lord) |
| 2 | 3-6 | 7 | |
| 3 | 7-8 | 4 | |
| 4 | 9-10 | 3 | |
| 5 | 11 | 3 | |
| 6 | 12 | 1 | Sun/Venus AD — single "other than exaltation or debilitation" condition |
| 7 | 13-15 | 10 | |
| 8 | 16-18 | 6 | |
| 9 | 19-20 | 3 | |
| 10 | 21-23 | 12 | Moon/Venus AD — truncated in dry run (1 fallback); max_tokens=8192 fix resolved ✅ |
| 11 | 24-26 | 9 | |
| 12 | 27-29 | 7 | |
| 13 | 30-31 | 9 | Mars/Venus AD |
| 14 | 32-34 | 7 | |
| 15 | 35 | 2 | |
| 16 | 36-37 | 7 | Rahu/Venus AD |
| 17 | 38-41 | 6 | (merged continuation slokas 40-41) |
| 18 | 42-44 | 5 | |
| 19 | 45-48 | 7 | Jupiter/Venus AD |
| 20 | 49-50 | 4 | |
| 21 | 51 | 3 | |
| 22 | 52-54 | 9 | Saturn/Venus AD |
| 23 | 55-57 | 9 | |
| 24 | 58-59 | 1 | Saturn remedies only — 1 rule correct |
| 25 | 60-62 | 8 | Mercury/Venus AD |
| 26 | 63-65 | 6 | |
| 27 | 66 | 3 | |
| 28 | 67-69 | 8 | Ketu/Venus AD (merged continuation sloka 69) |
| 29 | 70-72 | 5 | |
| 30 | 73-74 | 5 | |
| **TOTAL** | | **182** | |

**Key outcomes:**
- ✅ 30/30 slokas clean — zero AI extraction failures
- ✅ Sloka 21-23: 12 rules (vs 1 fallback in dry run) — max_tokens fix confirmed working
- ✅ 18 `dasha_grouped_outcome` rules auto-generated (Ch 55+ prompt includes GROUPED OUTCOME RULE guidance)
- ✅ SPLITTING GUIDANCE active — favourable/unfavourable conditions individually extracted
- ✅ `_join_standalone_headings()` confirmed working — 30/30 blocks detected from Word-exported RTF

**Universal rule check:**
- No opening meta-rules — Ch 60 begins directly with Venus/Venus antardasha at sloka 1-2 ✅
- No `applies_to_all_dasha_lords` tagging needed

**Isolation:** `approval_status='pending_review'` — zero rules reach live users

**Split-Upgrade Results (24 Apr 2026):**

**Dry run:** +162 net-new predicted | 21 duplicates skipped (all slokas showed `existing: 0`)
**Live run:** ✅ **+12 net-new** | 168 duplicates skipped

**Key insight — why +12 vs +162:**
Ch 60 was ingested with the fully improved prompt (SPLITTING GUIDANCE + GROUPED OUTCOME RULE + max_tokens=8192 all active). The original 182-rule ingest was already comprehensive with individually-split conditions. Dry run showed `existing: 0` because no pre_split_merged tagging exists for Ch 60 (fresh chapter, never assessed). Live run correctly found all 182 originals as existing duplicates. This is the expected behaviour for chapters ingested post-prompt improvements — split-upgrade adds only genuinely missing rules.

**12 net-new rules inserted (all `source_note='split_upgrade'`, `approval_status='pending_review'`):**

| Rule ID | Sloka | Sub-type | What was missing |
|---|---|---|---|
| R-BPHS60-PATCH-16CE31 | 16-18 | dasha_grouped_outcome | Sun unfavourable grouped summary (6th/8th/12th ∪ debil ∪ enemy sign) |
| R-BPHS60-PATCH-9B9C75 | 21-23 | dasha_grouped_outcome | Moon + 9th/10th lord lordship-qualifier compound grouped rule |
| R-BPHS60-PATCH-C38790 | 30-31 | dasha_favourable | Mars (kendra/trikona/11th) AND Asc/9th/10th lord — compound rule |
| R-BPHS60-PATCH-4CF943 | 30-31 | dasha_favourable | Mars (exalt/own sign) AND Asc/9th/10th lord — compound rule |
| R-BPHS60-PATCH-6B1DEB | 55-57 | dasha_grouped_outcome | Saturn 8th/11th/12th from Asc or Venus — grouped summary |
| R-BPHS60-PATCH-D50160 | 60-62 | dasha_grouped_outcome | Mercury exaltation/own sign — grouped outcome summary |
| R-BPHS60-PATCH-71815C | 63-65 | dasha_unfavourable | Mercury weak — was merged into multi-condition rule |
| R-BPHS60-PATCH-B2E807 | 66 | dasha_remedy | Vishnu Sahasranama remedy — not individually extracted |
| R-BPHS60-PATCH-6A7984 | 67-69 | dasha_favourable | Ketu "victory in war at end of antardasha" — timing rule |
| R-BPHS60-PATCH-00DAB6 | 67-69 | dasha_conditional | Ketu "moderate results in middle portion" — timing conditional |
| R-BPHS60-PATCH-1E6144 | 67-69 | dasha_conditional | Ketu "occasional feelings of distress" — timing conditional |
| R-BPHS60-PATCH-CD9D96 | 73-74 | dasha_remedy | Venus appeasement remedy — not individually extracted |

**Sub-type audit — 4 grouped outcome rules, all correctly typed ✅**
No mis-tagging. No gap-fill needed.

**Ch 60 final totals — FINAL ✅**
- Original ingest: 182 rules
- Split-upgrade live: +12 net-new
- Gap-fill: none needed
- **Total: 194 rules** ✅

**Open Points:**
1. **Validation not yet run** — run: `validate_rules.py --batch-id bphs-ch60-dasha-20260424`
2. **194 rules pending_review** — awaiting co-founder sign-off

---

### Vol 1 House Chapters (Ch 12-24) — Undersplit Assessment | 24 Apr 2026

**Script:** `scripts/assess_undersplit_houses.py`
**Scope:** 736 rules across 13 batches (Ch 12-24, bphs-ch12-v2-20260414 → bphs-ch24-v2-20260416)
**Run date:** 24 Apr 2026 (refined version — v2 with yoga-connector disambiguation)

#### Assessment Results

| Batch | Total | Candidates | % | dignity_bundle | house_list | planet_or |
|---|---|---|---|---|---|---|
| bphs-ch12-v2-20260414 | 17 | 0 | 0% | — | — | — |
| bphs-ch13-v2-20260414 | 32 | 5 | 16% | 2 | 2 | 1 |
| bphs-ch14-v2-20260414 | 33 | 4 | 12% | 0 | 4 | 0 |
| bphs-ch15-v2-20260414 | 20 | 3 | 15% | 1 | 2 | 0 |
| bphs-ch16-v2-20260414 | 41 | 6 | 15% | 1 | 4 | 1 |
| bphs-ch17-v2-20260414 | 43 | 4 | 9% | 0 | 3 | 1 |
| bphs-ch18-v2-20260414 | 55 | 7 | 13% | 2 | 3 | 2 |
| bphs-ch19-v2-20260415 | 21 | 4 | 19% | 1 | 3 | 0 |
| bphs-ch20-v2-20260415 | 33 | 5 | 15% | 0 | 4 | 1 |
| bphs-ch21-v2-20260415 | 28 | 5 | 18% | 0 | 4 | 1 |
| bphs-ch22-v2-20260415 | 16 | 2 | 13% | 0 | 2 | 0 |
| bphs-ch23-v2-20260415 | 21 | 9 | 43% | 2 | 7 | 0 |
| bphs-ch24-v2-20260416 | 376 | 5 | 1% | 2 | 2 | 1 |
| **GRAND TOTAL** | **736** | **59** | **8%** | **11** | **40** | **8** |

#### Decision: No blanket split-upgrade sweep for house chapters

**Rationale:**
1. **8% vs 56%** — dasha chapters had 56% merged-condition rate; house chapters have only 8%. The prompt at the time of house ingest already produced reasonable splitting.
2. **Ch 24 is 51% of all house rules (376/736)** — only 5 candidates (1%). The dominant chapter is clean.
3. **False positive risk** — after yoga-connector disambiguation, approximately half the 59 flagged candidates on closer inspection are complex yoga combinations that correctly stay merged (the regex catches "or" in multi-planet contexts that `YOGA_CONNECTOR_RE` doesn't fully suppress).
4. **No `patch_slokas.py` equivalent for house chapters** — split-upgrade tooling is dasha-only. A house split-upgrade would require significant new tooling.
5. **Best ROI path** — improve `ingest_bphs_houses_v2.py` for future chapters + flag 59 for human review at co-founder stage. The astrologer's eye will correctly classify genuine splits vs yoga compounds.

#### Detection methodology (v2 — refined 24 Apr 2026)

Three detection classes (Class D multi-clause dropped — too noisy for house rules):

| Class | Pattern | Example | Action |
|---|---|---|---|
| dignity_bundle | "exaltation or own sign", "own sign or moolatrikona" | "Sun in own sign or exaltation → wealth" | Split into 2 rules |
| house_list | "6th, 8th or 12th", "2nd or 7th" | "Lord in 6th, 8th or 12th → poverty" | Split into 3 rules |
| planet_or | "Venus or Mercury" NOT connected by yoga words | "Venus or Mercury in 2nd → eloquence" | Split into 2 rules |

**Yoga guard** — `YOGA_CONNECTOR_RE` detects simultaneous conditions (and/while/with/conjunct/associated with/aspected by/joined by). If 2+ planets present AND yoga connector present → classify as yoga, NOT planet_or → do NOT flag.

**Script location:** `scripts/assess_undersplit_houses.py`
**Tag support:** `--tag` flag marks candidates as `metadata.source_note='pre_split_merged'` (NOT run — 59 candidates kept untagged; human review preferred)

#### Action at co-founder review

For each of the 59 flagged rules, the co-founder reviewer should:
1. Read the condition text in Rules Browser
2. Confirm whether it is a genuine alternative condition (should split) or a yoga combination (keep as one)
3. Promote genuine split-candidates to `deprecated` + create individual rules manually (low volume — estimated 20-30 genuine cases)

---

### `ingest_bphs_houses_v2.py` — SPLITTING GUIDANCE upgrade | 24 Apr 2026

**Three improvements applied (commit on 24 Apr 2026):**

| Change | Before | After | Reason |
|---|---|---|---|
| `max_tokens` | 2048 | 4096 | Prevent JSON truncation on complex slokas (same fix as dasha script) |
| `temperature` | 0.1 | 0 | Deterministic extraction — same sloka → same rule count across all runs |
| `EXTRACTION_SYSTEM` | No splitting guidance | Full SPLITTING GUIDANCE (A–E) | Produces individually-queryable rules from merged-condition slokas |

**SPLITTING GUIDANCE added (Rule 2 updated + new sections A–E):**

- **A. HOUSE-LIST ALTERNATIVES**: "lord in 6th, 8th or 12th" → 3 individual rules + 1 grouped rule
- **B. DIGNITY ALTERNATIVES**: "planet in own sign or exaltation" → 2 individual rules (own sign; exaltation)
- **C. ALTERNATIVE PLANETS**: "Venus or Mercury in 2nd" → 2 individual rules (Venus; Mercury)
- **D. YOGA CONDITIONS — DO NOT SPLIT**: "Mercury in 3rd while Moon and Saturn conjunct" = 1 combination rule
- **E. GROUPED OUTCOME RULE**: after A/B/C splits, add 1 combined rule covering all alternatives with shared outcome (`sub_type = "general_principle"`)

**Rule 2 updated:** Changed from "combine same-outcome OR conditions into one rule" → "apply SPLITTING GUIDANCE to create individual rules per alternative PLUS one grouped-outcome rule". This is the critical flip — old instruction produced merged rules, new instruction produces individually-queryable rules.

**All future house chapter ingests** (Text-Book of Astrology Ch 15, any future BPHS Vol 2 house chapters) will benefit automatically.

**Old Vol 1 house chapters (Ch 12-24):** NOT re-ingested. 59 flagged candidates handled at co-founder review.

---

### Text-Book of Astrology Ch 15 | Planets in Different Houses: Prediction | 24 Apr 2026

**Script used:** `ingest_tba_ch15_v1.py` (purpose-built; commit `a31099f`)
**Batch ID:** `tba-ch15-v1-20260424`
**Book:** A Text-Book of Astrology | Chapter 15
**Structure:** Two-part chapter — Part 1: Planet × House (108 blocks), Part 2: Planet × Sign (108 entries)

#### Script highlights

- **RTF parser** — state-machine detecting Planet / House / "In female horoscope:" / "Result of Planets in 12 Signs" headings via regex; `join_colon_continuations()` fixes Part 2 split-line RTF artefact
- **Two-layer extraction per block**: LAYER 1 = general paragraph description (`is_group_summary=True`, `planet_occupation`); LAYER 2 = individual IF conditions (`is_group_summary=False`)
- **Female sub-sections**: Each block has a "In female horoscope:" paragraph extracted separately (`gender="female"`)
- **`condition_group_id`**: Auto-generated deterministically — `tba15-{planet}-h{NN}-{gender}` (e.g. `tba15-saturn-h01-neutral`). All rules in a block share one ID; `group_summary` tag on LAYER 1 rule only
- **Part 2 sign rules**: One API call per planet (12 signs batched); `build_sign_rule()` extracts sign from `full_condition` via regex

#### Pre-ingest fixes (commit `a31099f`)

| Issue | Fix |
|---|---|
| Saturn-H01 JSON truncation (`EOF at col 13647`) | `max_tokens` 4096 → 8192 in `Extractor.house_block()` |
| `is_group_summary=True` bleeding onto sign-list grouped summaries (SPLITTING GUIDANCE A) | Added explicit `***` guards in LAYER 2, SPLITTING GUIDANCE A, and IMPORTANT block |

#### Dry run validation (V1 → V2)

- **V1** (before fixes): 1,480 rules; Saturn-H01 failed; Jupiter-H03 `grp:7`, Mars-H01 `grp:4`, Moon-H01 `grp:4`, Sun-H06 `grp:4`
- **V2** (after fixes): 1,429 rules; Saturn-H01 = 37 rules; all 108 blocks `[grp:1  f-grp:1]` — perfect

#### Live run results

| Metric | Count |
|---|---|
| Part 1 blocks extracted | 108 / 108 |
| Part 2 sign entries extracted | 108 / 108 |
| **Total rules inserted** | **1,530** |
| Group summaries | 216 (= 108 neutral + 108 female, exactly 2 per block) |
| Neutral rules | 1,312 |
| Female horoscope rules | 218 |

**Sub-type breakdown:**

| Sub-type | Count |
|---|---|
| sign_placement | 635 (embedded Part 1 IF-sign rules + 108 Part 2) |
| combination | 274 |
| planet_occupation | 251 |
| conditional_rule | 249 |
| aspect_rule | 119 |
| general_principle | 2 |

**Range:** Min = Rahu-H11/H12 (2 rules each — no IF conditions in source text, confirmed correct); Max = Jupiter-H03 (33 rules — rich block with many sign-list alternatives, confirmed correct)

**Next step:** `python3 scripts/validate_rules.py --mongo-url $MONGO_URL --db-name horoscope_db --batch-id tba-ch15-v1-20260424`

#### Post-ingest variance analysis — dry run V2 vs live run

After live ingest, a block-by-block diff against the V2 dry run baseline revealed 16 blocks with ±1–4 rule variance (92/108 blocks identical). This is expected LLM non-determinism at temperature=0 across separate API sessions. All 108 blocks retain `[grp:1  f-grp:1]` — structural integrity is intact.

Full source spot-check was run on the four highest-variance Mars blocks:

| Block | V2 | Live | Source IFs | Assessment |
|---|---|---|---|---|
| Mars-H02 | 9 | 11 | 7 | Live more accurate — V2 under-split "own sign/exalted" (Guidance B) |
| Mars-H03 | 16 | 12 | 10 | **V2 more accurate — live under-split (see flag below)** |
| Mars-H05 | 24 | 21 | 12 | Both acceptable — heavy sign-list block, both within range |
| Mars-H11 | 15 | 17 | 8 | Both acceptable — live picked up 2 inline prose IFs |

#### ⚑ Manual review flag — Mars-H03 (`tba15-mars-h03-neutral` / `tba15-mars-h03-female`)

**What happened:** The live run extracted 12 rules against an expected ~15-16. The model applied SPLITTING GUIDANCE correctly in V2 (16 rules) but skipped splits in the live run, leaving ~4 OR-conditions merged.

**Specific missed splits in the live run:**

| Condition in source | Expected split | What live run likely stored |
|---|---|---|
| `IF with malefics or aspected by malefics → unfavourable for elder co-borns` | 2 rules (with malefics; aspected by malefics) + 1 grouped | 1 merged rule |
| `IF Mars in own sign or exalted → prosperous` (female) | 2 rules (own sign; exalted) + 1 grouped | 1 merged rule |

**Action at co-founder review:**
1. Open Rules Browser → filter `condition_group_id = "tba15-mars-h03-neutral"` and `"tba15-mars-h03-female"`
2. Find the merged OR-condition rules above
3. Manually create the individual split rules + grouped summary (or use `patch_slokas.py` if adapted for TBA format)
4. Deprecate the merged originals (`approval_status = "deprecated"`)

**Source text for reference (Mars in Third House):**
- General: `"IF with malefics or aspected by malefics — unfavourable for elder co-borns"`
- Female: `"IF Mars is in own sign or exalted — prosperous"`

---

## Validation Run — Full Library Clean Pass (2026-04-25)

### Context

After resetting 2,951 rules (133 `skipped_resume` + 2,818 `batch_error`) back to `pending_review`, a clean validation pass was run against the full library using `validate_rules.py` with `--batch-size 10` and retry-on-timeout logic (commit `c531553`).

Run was interrupted twice by network issues (MongoDB Atlas timeout at batch 172/334, DNS error on resume attempt). Streaming writes preserved all progress — each re-run automatically picked up only remaining `pending_review` rules.

### Final Results

| Status | Count | % |
|---|---|---|
| `pending_human_review` | 741 | 39% |
| `auto_approved` | 613 | 32% |
| `flagged` | 549 | 29% |
| `rejected` (structural) | 1 | <1% |
| **Total this run** | **1,903** | |

**Contradictions found: 132 pairs**

### Key Findings

#### 132 Contradiction Pairs — Highest Priority for Co-Founder Review

Stage 3 detected 132 contradiction pairs across 121 condition groups. All rules involved in a contradiction were automatically downgraded from `auto_approved` → `pending_human_review`.

These are rules that share the same `condition.type / planet / house` key but give conflicting interpretations. Root cause is likely:
- Multiple source books covering the same planetary placement with different classical opinions
- OR-condition rules that were not fully split (one merged rule conflicts with a later individual rule)

**Action:** Review at `/admin/library` → Rules Browser → filter `flagged` and `pending_human_review`. Contradiction pairs are tagged with `contradiction_ids` in the `validation` sub-document.

#### 549 Flagged Rules — Quality Issues Identified by Claude

Claude flagged 29% of rules for one or more of: vague condition language, overly generic interpretation, missing Sanskrit/Hindi context, or suspicious confidence level. These require human editorial judgment before promotion.

#### 613 Auto-Approved Rules — Clean and Ready

613 rules passed both structural and Claude quality checks with no contradictions. These are ready for co-founder sign-off (`approval_status` promotion from `auto_approved` → `approved`).

#### 1 Structural Failure — Hard Rejected

One rule failed structural validation (missing required fields or malformed condition block). Marked `rejected`. Check Rules Browser → filter `rejected` to identify which rule and source book.

### Combined Library State (Post This Run)

Across all ingested batches, the library now has:

| Status | Meaning |
|---|---|
| `auto_approved` | Clean — awaiting co-founder sign-off |
| `flagged` | Quality concern — human review needed |
| `pending_human_review` | Spot-check or contradiction-involved — human review needed |
| `rejected` | Hard structural failure — excluded |
| `approved` | **None yet** — no rules reach live users until co-founder promotes |

### Retry Logic Added (commit `c531553`)

`apply_verdict()` now retries on `pymongo.errors.AutoReconnect` with exponential backoff (1s / 2s / 4s, up to 3 retries) before raising. This prevents transient Atlas timeouts from killing future validation runs.

### Next Steps

1. **Co-founder review session** — work through flagged + pending_human_review rules in Rules Browser
2. **Contradiction triage** — review the 132 pairs; deprecate the weaker rule in each pair or merge if both are valid classical sources
3. **Mars-H03 manual correction** — see flag above (split 2 merged OR-conditions)
4. **Promotion** — after review, promote clean rules: `approval_status` `auto_approved` → `approved` via co-founder sign-off
5. **Next ingest** — remaining BPHS dasha interpretation chapters pending

---

## Validation Run — horoscope_db Remainder Pass (2026-04-25)

386 pending_review rules remaining in `horoscope_db` after the main pass. Clean run — all 39 batches completed without interruption.

### Results

| Status | Count | % |
|---|---|---|
| `pending_human_review` | 140 | 36% |
| `auto_approved` | 140 | 36% |
| `flagged` | 106 | 27% |
| `rejected` (structural) | 1 | <1% |
| **Total** | **386** | |

**Contradictions: 0 pairs** (only 4 condition groups with ≥2 rules — too sparse for conflicts)

### horoscope_db Cumulative State (post both passes)

| Status | From main pass | From remainder pass | Combined |
|---|---|---|---|
| `auto_approved` | 2,565 | +140 | **2,705** |
| `flagged` | 1,223 | +106 | **1,329** |
| `pending_human_review` | 1,710 | +140 | **1,850** |
| `rejected` | 31 | +1 | **32** |
| `pending_review` | 386 | −386 | **0** |

`horoscope_db` is now fully validated. No rules remain in `pending_review`.

---

## Validation Run — EverydayHoroscope Remainder Pass (2026-04-25)

950 pending_review rules in `EverydayHoroscope` database. All 95 batches completed without interruption.

### Results

| Status | Count | % |
|---|---|---|
| `flagged` | 534 | 56% |
| `pending_human_review` | 317 | 33% |
| `auto_approved` | 95 | 10% |
| `pending_review` (residual) | 4 | <1% |
| `rejected` (structural) | 5 | <1% |
| **Total** | **950** | |

**Contradictions: 4 pairs** — downgraded from `auto_approved` → `pending_human_review`

### Notable Finding — High Flagged Rate (56%)

The `EverydayHoroscope` database shows a significantly higher flagged rate (56%) vs `horoscope_db` (~21%). This indicates older or earlier-ingested rules with lower content quality — likely from an earlier ingest session before prompt refinements were applied. These 534 flagged rules require careful editorial review before any promotion consideration.

### Residual 4 pending_review Rules

4 rules remain in `pending_review` after every pass — same 4 survive each run. Stage 4 counter undercounts due to MongoDB write timing gaps; the actual residual count was 297 (confirmed by cleanup pass below), not 4.

These 4 rules are likely failing the `update_one` match silently — possibly malformed `rule_id` or a field conflict. Identify them directly:

```bash
python3 - <<'EOF'
from pymongo import MongoClient
client = MongoClient("mongodb+srv://...")
db = client["EverydayHoroscope"]
for r in db["interpretation_rules"].find({"approval_status": "pending_review"}, {"rule_id": 1, "condition": 1, "source": 1, "_id": 0}):
    print(r)
client.close()
EOF
```

### EverydayHoroscope Cleanup Pass (2026-04-25)

Cleanup pass found 297 pending_review rules (not 4 as Stage 4 counter suggested — Stage 4 undercounts due to write timing). All 30 batches completed. Zero contradictions.

| Status | Count | % |
|---|---|---|
| `flagged` | 172 | 58% |
| `auto_approved` | 66 | 22% |
| `pending_human_review` | 55 | 19% |
| `pending_review` (residual) | 4 | 1% |
| `rejected` (structural) | 5 | <1% |
| **Total** | **297** | |

58% flagged rate consistent with EverydayHoroscope pattern — older lower-quality ingest content.

### EverydayHoroscope Cumulative State (post all passes)

| Status | Pass 1 base | Pass 2 (+950) | Cleanup (+297) | Combined |
|---|---|---|---|---|
| `auto_approved` | 1,434 | +95 | +66 | **1,595** |
| `flagged` | 341 | +534 | +172 | **1,047** |
| `pending_human_review` | 473 | +317 | +55 | **845** |
| `rejected` | 2 | +5 | +5 | **12** |
| `pending_review` | 950 | −946 | −293 | **4** (persistent) |

### EverydayHoroscope Hollow Rule Bulk Deprecation (2026-04-25)

280 hollow composite rules found in `pending_review` with `condition.type = composite`, empty `sub_conditions`, and duplicate `rule_id` values across multiple batch IDs. Root cause: earlier ingest script reset `rule_id` counter per batch instead of globally. All deprecated to `rejected` with reason `hollow_composite_empty_condition_duplicate_batch_ingest`.

`validate_rules.py` fix applied (commit `ee0043b`): switched `update_one` → `update_many` in `apply_verdict()` so all documents sharing a `rule_id` are written in a single call. Eliminates persistent residual from duplicate-id ingest bugs.

### EverydayHoroscope Final Pass (2026-04-25)

17 remaining `pending_review` rules processed. 2 batches. Zero structural failures. Zero contradictions. 16 flagged (94%), 1 auto_approved (6%).

### Full Library State — Both Databases (2026-04-25, FINAL)

| Status | horoscope_db | EverydayHoroscope | Grand Total |
|---|---|---|---|
| `auto_approved` | 2,705 | 1,596 | **4,301** |
| `flagged` | 1,329 | 1,063 | **2,392** |
| `pending_human_review` | 1,850 | 845 | **2,695** |
| `rejected` | 32 | 292 | **324** |
| `pending_review` | **0** | **0** | **0** ✅ |
| `approved` | 0 | 0 | **0** |
| **Total** | **5,916** | **3,796** | **9,712** |

**All validation passes complete. Zero `pending_review` in both databases.**

No rules reach live users until `approved` status is granted via co-founder sign-off.

### EverydayHoroscope — Full Deprecation (2026-04-25)

Decision: deprecate en masse. Reasons:
- Confirmed stale pre-split-upgrade snapshot (INGEST_NOTES line 96)
- 56–94% flagged rate across all passes vs ~21% in horoscope_db
- Source books (A Text Book of Astrology General + Lal Kitab) have no current ingest scripts
- Chapter headings garbled (bad OCR from old pipeline — e.g. `'7 10 1 4 7'`, `'Lal Kitab And'`)
- Content to be re-ingested fresh into horoscope_db when source RTFs are available

```python
db["interpretation_rules"].update_many(
    {"approval_status": {"$nin": ["rejected", "approved"]}},
    {"$set": {"approval_status": "rejected",
              "validation.flag_reason": "deprecated_stale_pre_split_upgrade_snapshot_20260425"}}
)
# Result: 3,012 rules deprecated
```

**EverydayHoroscope is now fully retired. All 3,796 rules are rejected. Do not use for any operation.**

---

### Active Library — horoscope_db Only (2026-04-25, FINAL)

| Status | Count |
|---|---|
| `auto_approved` | 2,705 |
| `flagged` | 1,329 |
| `pending_human_review` | 1,850 |
| `rejected` | 32 |
| `pending_review` | 0 |
| `approved` | **0** |
| **Total active** | **5,884** |

### Pending Ingest — A Text Book of Astrology (General) + Lal Kitab

Both sources need fresh ingest scripts built against the current pipeline before they can be added to horoscope_db. Source RTFs to be sourced first.

| Book | Status |
|---|---|
| A Text Book of Astrology — General chapters | ❌ No current script — needs RTF source + new ingest script |
| Lal Kitab | ❌ No current script — needs RTF source + new ingest script |

### Next Steps

1. **Co-founder review session** — `everydayhoroscope.in/admin` → Rules Browser → `horoscope_db` only
2. **Contradiction triage** — 125 unique pairs in `horoscope_db_contradictions.csv`; fill `recommended_action` column
3. **Mars-H03 manual correction** — split 2 merged OR-conditions (see earlier flag)
4. **Remaining source ingest** — BPHS chapters pending + A Text Book of Astrology General + Lal Kitab (new scripts needed)
5. **Remedies Engine** — spec and build before promotion gate opens
6. **1,000 use case litmus test** — required before any `auto_approved` → `approved` promotion
7. **Promotion gate** — co-founder sign-off only after steps 1–6 complete

---

### Text-Book of Astrology Ch 16 | Planetary Combinations or Yogas | 25–26 Apr 2026

**Script used:** `ingest_tba_ch16_v1.py` (purpose-built; commits `5738248`, `ec06bcd`)
**Batch ID:** `tba-ch16-v1-20260425`
**Book:** A Text-Book of Astrology | Chapter 16: Planetary Combinations or Yogas

#### Script design — two-section-type parser

| Type | Content | Sections | Rules |
|---|---|---|---|
| Type A | Named yogas (Gaja Kesari, Hansa, Vipreet Rajyoga etc.) | 42 | 44 |
| Type B | Category bullet groups (Arishta/Wealth/Marriage/Progeny/Disability/Eye/Co-Borns) | 17 | 85 |
| — | Skipped containers (Arishta Yoga, Yogas For Marriage) | 1 | 0 |

#### New schema fields (TBA Ch 16 onwards)

| Field | Path | Purpose |
|---|---|---|
| `yoga_check` | `condition.yoga_check` | Machine-checkable formation condition — vedic_calculator.py evaluates against live birth chart to detect active yogas |
| `physical_markers` | `interpretation.physical_markers` | Physical appearance, disability, behavioral observations — cross-module verification against photographic evidence + premium report layer |

Both fields are absent from BPHS Ch 12-59 and TBA Ch 15 rules — Phase 2 backfill via `enrich_rules.py` (not yet built).

#### Dry run vs Apply results

| Metric | Dry Run | Apply | Status |
|---|---|---|---|
| Total rules | 129 | 129 | ✅ Exact match |
| yoga_combination | 43 | 43 | ✅ |
| general_principle | 85 | 85 | ✅ |
| dosha | 1 | 1 | ✅ |
| benefic_rule | 35 | 36 | ⚠️ +1 neutral→benefic float |
| neutral_rule | 7 | 6 | ⚠️ −1 (same float) |

The 1-rule float was AI non-determinism across two separate API call sessions. **Eliminated going forward** by `--dry-run --save / --upload` pattern — JSON from dry run uploads directly with zero re-extraction.

#### yoga_check coverage

| Type | Count |
|---|---|
| complex (checkable=False) | 77 |
| lord_in_house | 14 |
| benefics_in_houses | 6 |
| malefics_in_houses | 6 |
| planet_in_dignity_in_kendra | 6 |
| planet_conjunction | 5 |
| any_planet_relative | 4 |
| relative_position | 4 |
| lord_exchange | 3 |
| lord_mutual_kendra | 2 |
| no_planets_adjacent | 1 |
| lord_conjunction | 1 |
| **Checkable (True)** | **49 / 129** |

#### Physical markers summary

Physical markers found in 44 rules:
- disability: 18 (blindness, deafness, dumbness, speech defect)
- behavioral: 17 (polite, generous, righteous, wicked etc.)
- facial_features: 6 (lion-like face, majestic appearance, handsome)
- body_build: 5 (well-proportioned limbs, strong physique)
- voice: 5 (eloquent speaker, stammering, speech defects)
- health: 3 · body_marks: 1 · complexion: 1

#### ⚑ Manual Review Flag — tba16-003 (Ubhaychari Yoga)

| Field | Value |
|---|---|
| rule_id | tba16-003 |
| yoga_name | Ubhaychari Yoga |
| yoga_check.type | complex |
| yoga_check.checkable | False |
| Condition | "Planets other than Moon on BOTH sides of Sun simultaneously" — requires a planet in 2nd FROM Sun AND a planet in 12th FROM Sun |
| Why flagged | Each side is individually checkable (`any_planet_relative`), but the compound AND requirement was correctly marked `complex` by Claude (too many clauses for current engine). The yoga IS detectable — requires two `any_planet_relative` conditions joined with operator=AND. |
| Fix path | Phase 2 `enrich_rules.py` — implement compound `yoga_check` with two clauses, OR add `compound_relative_position` check type to `YOGA_CHECK_TYPES`. |
| Priority | Low — rule fires correctly in premium reports (full_condition text used). Only runtime programmatic detection is affected. |

#### Standard ingest workflow — first use of --save/--upload pattern

Ch 16 was ingested BEFORE the `--save/--upload` flags were implemented (the apply script re-ran AI extraction = double cost). From Ch 17 onwards, all ingests use:
```
python3 scripts/ingest_tba_ch<N>_v1.py --dry-run --save rules.json
# Review rules.json — amend/add/remove as needed
python3 scripts/ingest_tba_ch<N>_v1.py --upload rules.json --mongo-url $MONGO_URL --db-name horoscope_db
python3 scripts/validate_rules.py --batch-id <batch-id>
```

#### Validation Results — COMPLETE (26 Apr 2026)

Two-pass validation required — see validator fix note below.

| Status | Run 1 (34 rules) | Re-run (95 rules) | Total |
|---|---|---|---|
| `auto_approved` | 26 | 60 | **86 (67%)** |
| `pending_human_review` | 5 | 30 | **35 (27%)** |
| `flagged` | 3 | 5 | **8 (6%)** |
| Contradictions | 0 | 0 | 0 |

**Validator fix (commit `ccb475c`, 26 Apr):** `knowledge_validator.py` `structural_check()` was failing 95/129 rules with `truncated_text` because the TBA-style `"Yoga/Category … Condition … Effect"` `detailed` field ends without a terminal period. Fix: skip `truncated_text` guard for `yoga_combination`, `general_principle`, `dosha` types. This fix covers all future yoga-schema chapters automatically.

#### Open Points

1. ✅ ~~Validation not yet run~~ — COMPLETE (26 Apr 2026)
2. **tba16-003 yoga_check fix** — deferred to Phase 2 `enrich_rules.py` pass
3. **Phase 2 schema backfill** — TBA Ch 15 + BPHS Ch 12-59 need `physical_markers` + `yoga_check` fields added via `enrich_rules.py` (not yet built)

---

## BPHS Chapter 35 — Nabhasa Yogas

**Batch ID:** `bphs-ch35-v1-20260426`
**Script:** `scripts/ingest_bphs_ch35_v1.py`
**Dry-run JSON:** `scripts/bphs_ch35_rules.json`
**Commit:** `b29e62b`

### Source structure

All 32 Nabhasa Yogas + 1 general meta-rule = **33 rules total**.
Hard-coded from RTF — zero AI extraction cost (first fully hand-coded chapter).

| Category | Yogas | Rules |
|---|---|---|
| Aashraya (sign modality) | Rajju, Musala, Nala | 3 |
| Dala (angle occupation) | Maala, Sarpa | 2 |
| Akriti (house patterns) | Gada → Samudra | 20 |
| Sankhya (sign count) | Gola → Veena | 7 |
| General | Meta-rule (dasa persistence) | 1 |
| **Total** | | **33** |

### yoga_check coverage — 31 / 33 checkable *(updated 26 Apr 2026)*

| yoga_check.type | Yogas | Checkable |
|---|---|---|
| `sign_quality_all` | Rajju, Musala, Nala | ✅ True |
| `angles_by_planet_type` | Maala, Sarpa | ✅ True |
| `all_planets_in_houses` | Gada, Sakata, Vihaga, Sringataka, Hala, Kamala, Vapi, Yupa, Sara, Sakthi, Danda, Nauka, Koota, Chatra, Chapa | ✅ True |
| `all_planets_in_alt_signs` | Chakra, Samudra | ✅ True |
| `planets_in_n_signs` | Gola, Yuga, Soola, Kedara, Paasa, Dama, Veena | ✅ True |
| `multi_house_requirements` | **Vajra**, **Yava** | ✅ True — promoted from `complex` (26 Apr 2026) |
| `complex` | Ardha Chandra, Meta-rule | ❌ False |

**`multi_house_requirements` schema** (new type introduced Ch 35):
Each `house_requirements` entry: `{houses, planet_type, constraint}`.
`constraint`: `"present"` (≥1 planet of type in any of these houses) · `"absent"` (0 planets).
`operator`: `"and"` (all requirements must hold simultaneously).

**Remaining `complex` flags (2 rules):**
- **Ardha Chandra Yoga** (bphs-ch35-023): Formation not explicitly stated in this RTF. Cross-reference needed.
- **Meta-rule** (bphs-ch35-033): General principle — not a checkable yoga condition.

**Sankhya precedence rule:** All 7 Sankhya yogas carry `yoga_check.precedence = "superseded_by_higher_nabhasa"` per BPHS verse: *"None of these seven yogas will be operable if another Nabhasa yoga is derivable."*

### Validation — COMPLETE (26 Apr 2026)

Single-pass — zero structural failures (yoga_combination types pass updated validator).

| Status | Count | % |
|---|---|---|
| `auto_approved` | 25 | 76% |
| `pending_human_review` | 6 | 18% |
| `flagged` | 2 | 6% |
| Contradictions | 0 | — |
| **Total** | **33** | |

---

## BPHS Chapter 36 — Many Other Yogas

**Batch ID:** `bphs-ch36-v1-20260426`
**Script:** `scripts/ingest_bphs_ch36_v1.py`
**Dry-run JSON:** `scripts/bphs_ch36_rules.json`
**Commits:** `4a51784` (initial 30 rules) → `8fe4b9d` (final 32 rules after Hamsa + Chandradhi added)

### Source structure

25 named yogas + 7 divisional-dignity rules = **32 rules total**.
Hard-coded from RTF — zero AI extraction cost.

| Group | Yogas | Rules |
|---|---|---|
| Benefic/Malefic | Subha, Asubha | 2 |
| Raja Yoga | Gajakesari, Hamsa, Parvata, Kahala, Chamara, Sankha, Bheri, Mridanga, Srinatha, Sarada, Matsya, Koorma, Khadga, Lakshmi, Kusuma, Kalanidhi, Kalpadruma | 17 |
| Benefic Yoga | Amala, Lagnadhi, Chandradhi | 3 |
| Trimurthi | Hari, Hara, Brahma | 3 |
| Divisional Dignity | Parijathamsa, Vargothama, Gopuramsa, Sinhasanamsa, Paravathamsa, Devalokamsa, Iravathramsa | 7 |
| **Total** | | **32** |

### Post-dry-run additions (identified from RTF before upload)

Two yogas were found during RTF review after the initial dry run and added before upload:

**Hamsa Yoga** (rule bphs-ch36-004, Sloka 3-4 Notes):
- RTF location: Notes section of Gajakesari (Sloka 3-4), line: *"The case of mere of Jupiter being in exaltation in a lunar angle can better be known as Paicha Maha Purusha Yoga, specifically Hamsa Yoga."*
- Formation: Jupiter in Cancer (exaltation) in an angular house (1, 4, 7, 10) from the Moon
- Distinguishes Hamsa from ordinary Gajakesari — requires exaltation, not just kendra placement
- yoga_check: `planet_in_kendra_from`, checkable=True; sign: Cancer, reference: Moon

**Chandradhi Yoga** (rule bphs-ch36-025, Sloka 37 Notes):
- RTF location: Notes section of Lagnadhi Yoga (Sloka 37): *"In Chandradhi yoga, the sage has included the 6th house."*
- Formation: Natural benefics (Jupiter, Venus, Mercury) in the 6th, 7th, and/or 8th from the Moon, free from malefic aspect; 4th from Moon unoccupied
- Distinct from Lagnadhi Yoga: Lagnadhi counts from ascendant (houses 7, 8 only); Chandradhi counts from Moon (houses 6, 7, 8)
- Optimal form: Mercury in 6th, Jupiter in 7th, Venus in 8th from Moon
- yoga_check: `benefics_in_houses`, reference: Moon, checkable=True

### yoga_check coverage — 12 / 32 checkable *(updated 26 Apr 2026)*

| yoga_check.type | Yogas | Checkable |
|---|---|---|
| `benefics_in_houses` | Subha, Lagnadhi, Chandradhi | ✅ True |
| `malefics_in_houses` | Asubha | ✅ True |
| `planet_in_kendra_from` | Gajakesari, Hamsa | ✅ True |
| `benefic_only_in_house` | Amala | ✅ True |
| `planet_in_house` | Kalanidhi | ✅ True |
| `multi_house_requirements` | **Matsya**, **Parvata** | ✅ True — both promoted from `complex` (26 Apr 2026) |
| `complex` (checkable=False) | Kahala, Chamara, Sankha, Bheri, Mridanga, Srinatha, Sarada, Koorma, Khadga, Lakshmi, Kusuma, Kalpadruma, Hari, Hara, Brahma | ❌ False — require lord positions, Navamsa, or strength calculations |
| `divisional_dignity` | All 7 divisional rules | ❌ False |

**Promotion notes (26 Apr 2026):**
- **Matsya** (bphs-ch36-014): type renamed `complex` → `multi_house_requirements`; `house_requirements` field already existed. No structural change to data.
- **Parvata** (bphs-ch36-006): Promoted from `complex`/False. Condition is purely positional: benefics in angles + no malefics in houses 7–8. `house_requirements` added with `constraint: "absent"` on the malefic restriction.

### Validation — COMPLETE (26 Apr 2026)

Single-pass — zero structural failures.

| Status | Count | % |
|---|---|---|
| `auto_approved` | 13 | 41% |
| `pending_human_review` | 17 | 53% |
| `flagged` | 2 | 6% |
| Contradictions | 0 | — |
| **Total** | **32** | |

Note: Lower auto_approved % vs Ch 35 (41% vs 76%) expected — Ch 36 yogas are multi-lord complex formations with few checkable conditions, so the validator has less signal to auto-approve. All 17 PHR and 2 flagged rules await co-founder review.

---

## BPHS Chapter 37 — Lunar Yogas

**Batch ID:** `bphs-ch37-v1-20260426`
**Script:** `scripts/ingest_bphs_ch37_v1.py`
**Dry-run JSON:** `scripts/bphs_ch37_rules.json`
**Commit:** `688b4e2`

### Source structure

14 rules total — hard-coded from RTF, zero AI extraction cost.

| Group | Rules | Yoga names |
|---|---|---|
| Moon-Sun Position Yogas | 3 | Moon in Kendra / Panaphara / Apoklima from Sun |
| Moon Navamsa Yogas | 3 | Day Birth, Night Birth, Adverse |
| Adhi Yoga (from Moon) | 1 | Adhi Yoga (from Moon) |
| Dhana Yoga (from Moon) | 3 | Full / Medium / Weak |
| Sunapha / Anapha / Duradhara | 3 | Sunapha, Anapha, Duradhara |
| Kemadruma Yoga | 1 | Kemadruma Yoga |
| **Total** | **14** | |

### New yoga_check types introduced in Ch 37

| Type | Used by | Notes |
|---|---|---|
| `moon_from_sun_position` | Rules 001–003 | Moon's position relative to Sun: kendra / panaphara / apoklima. Field `position_type` + `houses_from_sun` distinguish the three cases. |
| `planet_in_house_from_moon` | Rules 011–013 | Non-Sun planet in specific house(s) from Moon. `house` (single) or `houses` + `operator=and` (Duradhara). `exclude_planets: ["Sun"]` on all three. |
| `kemadruma_check` | Rule 014 | Negative/absence check — yoga forms when all three positions are empty of qualifying planets simultaneously. `absent_conditions` list encodes the three checks. |

### Design decisions

**Dhana Yoga split into 3 rules (008–010):** The sloka explicitly defines three distinct intensity tiers (all 3 / 2 / 1 benefic in Upachaya from Moon → very affluent / medium / negligible wealth). Split allows runtime to return the exact matching rule based on benefic count. All three share `benefics_in_houses` type with Moon reference and Upachaya houses [3,6,10,11], differentiated by `minimum_count` / `maximum_count`.

**Adhi Yoga (from Moon) cross-reference:** Rule 007 (Ch 37 Sloka 5) is the same formation as Chandradhi Yoga (bphs-ch36-025, Ch 36 Sloka 37 Notes) — benefics in 6th/7th/8th from Moon. Both rules retained as independent textual sources; cross-reference noted in `interpretation.detailed` of rule 007.

**Moon-Sun position rules (001–003):** Sloka 1 is unnamed — three separate positional rules extracted (kendra=little wealth, panaphara=meddling intelligence, apoklima=excellent skill). Only rule 001 is `is_benefic=False`; 002–003 are True.

### yoga_check coverage — 11 / 14 checkable (79%)

| checkable | Rules |
|---|---|
| ✅ True (11) | 001–003 (moon_from_sun_position), 007–013 (benefics/planet_from_moon), 014 (kemadruma) |
| ❌ False (3) | 004–006 (Moon Navamsa yogas — require D-9 chart + birth-time qualifier) |

### Validation — COMPLETE (26 Apr 2026)

Single-pass — zero structural failures.

| Status | Count | % |
|---|---|---|
| `auto_approved` | 9 | 64% |
| `pending_human_review` | 3 | 21% |
| `flagged` | 2 | 14% |
| Contradictions | 0 | — |
| **Total** | **14** | |

---

## BPHS Chapter 38 — Solar Yogas

**Batch ID:** `bphs-ch38-v1-20260426`
**Script:** `scripts/ingest_bphs_ch38_v1.py`
**Dry-run JSON:** `scripts/bphs_ch38_rules.json`
**Commit:** `b66edcf`

### Source structure

4 rules total — hard-coded from RTF, zero AI extraction cost.

| Rule ID | Yoga | Sloka | Type | Checkable |
|---|---|---|---|---|
| bphs-ch38-001 | Vesi Yoga | 1–3 | `planet_in_house_from_sun` (h=2) | ✅ |
| bphs-ch38-002 | Vosi Yoga | 1–3 | `planet_in_house_from_sun` (h=12) | ✅ |
| bphs-ch38-003 | Ubhayachari Yoga | 1–3 | `planet_in_house_from_sun` (h=2+12, and) | ✅ |
| bphs-ch38-004 | Solar Yoga Benefic/Malefic Modifier | 4 | `complex` (general_principle) | ❌ |

**New yoga_check type:** `planet_in_house_from_sun` — Sun-based parallel to `planet_in_house_from_moon` (Ch 37). `exclude_planets: ["Moon"]` on all three yoga rules.

**Cross-references:**
- Vesi ↔ Sunapha Yoga (bphs-ch37-011): identical structure, Sun replaces Moon as reference
- Vosi ↔ Anapha Yoga (bphs-ch37-012): identical structure
- Ubhayachari ↔ Duradhara (bphs-ch37-013) + tba16-003: identical compound formation

**Rule 004 (general_principle):** Sloka 4 states "benefics give stated effects, malefics give contrary effects" — applies as a modifier across all three solar yogas. `condition.type = "general_principle"`, checkable=False. Phase 2: implement as planet-nature check layered on each base yoga.

### Validation — COMPLETE (26 Apr 2026)

| Status | Count | % |
|---|---|---|
| `auto_approved` | 1 | 25% |
| `pending_human_review` | 2 | 50% |
| `flagged` | 1 | 25% |
| Contradictions | 0 | — |
| **Total** | **4** | |

Note: Low auto-approved % (25%) expected for a 4-rule chapter — small batches give the validator limited cross-rule signal. The 1 flagged rule likely relates to the general_principle modifier (rule 004) which has no direct checkable condition.

---

## yoga_check Type: `multi_house_requirements` — Specification (26 Apr 2026)

**Introduced:** BPHS Ch 35 (Vajra / Yava promotion), formalised from Matsya Yoga (Ch 36).

### When to use

Apply `multi_house_requirements` when yoga detection requires evaluating planet-type occupancy across multiple **distinct** house groups simultaneously. All requirements are joined by `operator` (default `"and"`).

Distinguishing test:
- Single-group house check → use `benefics_in_houses` / `malefics_in_houses`
- Multiple-group house checks (AND/OR) → use `multi_house_requirements`

### Schema

```json
{
  "type": "multi_house_requirements",
  "checkable": true,
  "description": "...",
  "operator": "and",
  "house_requirements": [
    {
      "houses": [1, 7],
      "planet_type": "benefic",
      "constraint": "present"
    },
    {
      "houses": [4, 10],
      "planet_type": "malefic",
      "constraint": "present"
    }
  ]
}
```

### Field reference

| Field | Values | Notes |
|---|---|---|
| `houses` | list of house ints | Evaluated as a group — any of these houses |
| `planet_type` | `"benefic"` · `"malefic"` · `"mixed"` | `"mixed"` = at least one benefic AND one malefic present |
| `constraint` | `"present"` (default) · `"absent"` | `"present"` = ≥1 planet of type in any house in the list; `"absent"` = 0 planets of type in any house in the list |
| `operator` | `"and"` (default) | How requirements are combined |

### Rules using this type (Ch 35–36)

| Rule ID | Yoga | house_requirements summary |
|---|---|---|
| bphs-ch35-011 | Vajra Yoga | benefic in {1,7} AND malefic in {4,10} |
| bphs-ch35-012 | Yava Yoga | benefic in {4,10} AND malefic in {1,7} |
| bphs-ch36-006 | Parvata Yoga | benefic in {1,4,7,10} AND malefic absent from {7,8} |
| bphs-ch36-014 | Matsya Yoga | benefic in {1,9} AND mixed in {5} AND malefic in {4,8} |

### MongoDB patch

Reclassification committed to JSON files and applied via:
```
backend/scripts/patch_yoga_check_reclassify.py --mongo-url $MONGO_URL --db-name horoscope_db
```

---
