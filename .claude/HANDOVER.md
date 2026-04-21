# Knowledge Engine — Session Handover
> Last updated: 21 Apr 2026 (end-of-session update — Ch 52/53/54 split-upgrade complete)
> Written at end of Session 4 (context compressed multiple times)
> Next session: read this FIRST before touching any script or DB

---

## ⚠️ How to Keep This Document Current

**This file does NOT auto-update when context exhausts.** Three rules to prevent staleness:

1. **INGEST_NOTES.md is the living operational log** — always accurate because it's committed after every batch. When this doc is stale, INGEST_NOTES.md is the ground truth for what has been done.

2. **Update this doc at milestones, not just session end.** After every chapter ingest + validation, after every architectural decision, after every new script — update Section 4 (Next Steps) and the relevant section. Do not wait until context is nearly full.

3. **Start every new session with:**
   > *"Read `.claude/HANDOVER.md` and `backend/scripts/INGEST_NOTES.md`, then tell me what's pending before we proceed."*
   This forces reconstruction of current state before any action is taken.

---

## 1. Who You Are / What This Project Is

You are the Claude Code agent for **EverydayHoroscope** (https://www.everydayhoroscope.in) — India's premium Vedic astrology platform. The Knowledge Engine is a rules library that will power AI-driven chart interpretations. The user is **Prateek** (founder). His philosophy: *"This is our only shot to success. This work vs. rest of our lives."* Build it right the first time.

**Stack:** FastAPI backend (Render) · React frontend (Vercel) · MongoDB (`horoscope_db`) · Claude API for rule extraction

---

## 2. The Most Important Decision Made This Session

### Splitting Guidance Overhaul — 21 Apr 2026

The extraction prompt (`EXTRACTION_SYSTEM` in `ingest_bphs_dasha_v1.py`) previously said:

```
DO NOT split: "kendra, trikona, or the 11th" → one rule
DO NOT split: "6th, 8th, or 12th" → one rule
DO NOT split: "own sign or exaltation" → one rule
```

**This was wrong.** These are the exact cases that MUST be split. Here is why:

| Case | Why split |
|---|---|
| 6th vs 8th vs 12th | Completely different intensity — 8th = crisis, 6th = manageable adversity, 12th = losses/isolation |
| Exaltation vs own sign vs friend's sign | Different strength levels → different `strength_band` values. Can't modulate effect intensity without this split |
| kendra vs trikona vs 11th vs 3rd vs 2nd | Each house is independently queryable. User with planet in 11th should not get rules for kendra/trikona bundled in |

**New rule (now in the prompt):**

- **ALWAYS SPLIT**: Specific house numbers (each house = one rule) · Dignity states (exaltation/own/friend's/enemy/debilitation = one rule each)
- **KEEP AS ONE**: Named abstract categories (kendra as a group, trikona as a group) · Compound conditions requiring ALL parts simultaneously

**strength_band mapping now in prompt:**

| Condition | strength_band |
|---|---|
| Exaltation | `"high"` |
| Own sign | `"high"` |
| Friend's sign | `"medium"` |
| Enemy sign | `"low"` |
| Debilitation | `"low"` |
| Kendra | `"high"` |
| Trikona | `"high"` |
| 11th / 3rd / 2nd | `"medium"` |
| 8th house | `"high"` (intensity of harm) |
| 6th / 12th | `"medium"` |

This was committed but **NOT YET TESTED with live API**. The test script is at `/tmp/test_splitting.py`. The user needs to run:

```bash
cd /Users/apple/DailyHoroscope-Migration/backend
export ANTHROPIC_API_KEY="sk-ant-..."
python3 /tmp/test_splitting.py
```

Expected output for sloka 45-47: ~9 rules (was 2). For sloka 1-2: ~6 rules (was 3). For sloka 3-4: 1-2 rules (compound — should NOT over-split).

---

## 3. Current Knowledge Engine State

### MongoDB: `horoscope_db` (MANDATORY — never use `EverydayHoroscope`)

### Rules in DB: ~2,180 RTF-sourced rules (all `approval_status = pending_review` or `auto_approved`)
**Split-upgrade rules (+417 added 21 Apr 2026):** Ch 48 (+34), Ch 52 (+139), Ch 53 (+123), Ch 54 (+121) — tagged `source_note = 'split_upgrade'`

### antardasha_planet coverage: **802 / 802 = 100%** across Ch 47–59 ✅
- 2 universal meta-rules: `R-BPHS47-008`, `R-BPHS47-009` → `applies_to_all_dasha_lords: true`

### Chapters ingested (RTF pipeline):

| Source | Batch ID | Original Rules | Split-Upgrade +Rules | Status |
|---|---|---|---|---|
| BPHS Vol 1 Ch 12-18 | bphs-ch12..18-v2-20260414 | 241 | — | ✅ validated |
| BPHS Vol 1 Ch 19-23 | bphs-ch19..23-v2-20260415 | 119 | — | ✅ validated |
| BPHS Vol 1 Ch 24 | bphs-ch24-v2-20260416 | 376 | — | ✅ validated |
| BPHS Vol 2 Ch 47 (Sun MD) | bphs-ch47-dasha-20260416 | 93 | — | ✅ validated — split-upgrade pending |
| BPHS Vol 2 Ch 48 (Moon MD) | bphs-ch48-dasha-20260416 | 46 | +34 ✅ | split-upgrade done, not validated |
| BPHS Vol 2 Ch 52 (Sun MD) | bphs-ch52-dasha-20260416 | 93 | +139 ✅ | split-upgrade done, not validated |
| BPHS Vol 2 Ch 53 (Venus MD) | bphs-ch53-dasha-20260417 | 72 | +123 ✅ | split-upgrade done, not validated |
| BPHS Vol 2 Ch 54 (Mars MD) | bphs-ch54-dasha-20260417 | 86 | +121 ✅ | split-upgrade done, not validated |
| BPHS Vol 2 Ch 55 (Rahu MD) | bphs-ch55-dasha-20260417 | 96 | +153 ✅ | split-upgrade done, not validated |
| BPHS Vol 2 Ch 56 (Jupiter MD) | bphs-ch56-dasha-20260418 | 126 | — | ✅ validated — split-upgrade pending |
| BPHS Vol 2 Ch 57 (Saturn MD) | bphs-ch57-dasha-20260419 | 132 | — | ✅ validated — split-upgrade pending |
| BPHS Vol 2 Ch 58 (Mercury MD) | bphs-ch58-dasha-20260419 | 104 | — | ✅ validated — split-upgrade pending |
| BPHS Vol 2 Ch 59 (Ketu MD) | bphs-ch59-dasha-20260421 | 91 | — | ✅ validated — split-upgrade pending |

---

## 4. Immediate Next Steps (in priority order)

### ✅ Step 0 — strength_band inference — COMPLETE (21 Apr 2026)

`infer_strength_band_from_condition()` added to `ingest_bphs_dasha_v1.py`.
Committed: `19cec9e`. Wired into `extracted_to_rule()` and `_fallback_rule()`.
All rules generated from this point carry `strength_band: "high"|"medium"|"low"`.

### ✅ Step 1 — Test the new SPLITTING GUIDANCE — COMPLETE (21 Apr 2026)

Test output (`/tmp/test_splitting.py`) confirmed:
- Sloka 45-47: 9 rules ✅ (3 dignity + 2 category + 3 house + 1 timing)
- Sloka 1-2: 6 rules ✅ (2 category + 1 Asc lord + 3 individual lords)
- Sloka 3-4: 2 rules ✅ (8th vs 12th split, compound preserved)

### ✅ Step 2 — Gap-fill sweep: Ch 59 sloka 1-2 — COMPLETE (21 Apr 2026)

+3 rules inserted (9th/10th/4th lord). 3 correctly skipped (kendra/trikona/Asc lord already in DB).
Ch 59 total: **91 rules** (88 original + 3 gap-fill). IDs: PATCH-FACB65, PATCH-5E398B, PATCH-2C21C9.

Two dedup fixes committed during this step (required for house-lord variant rules):
- `patch_slokas.py`: condition-only comparison (strip result text before overlap check)
- `patch_slokas.py`: two-tier thresholds — 60% vs DB, 90% within-run (prevents 9th/10th/4th lord blocking each other)

### Step 3 — Split-Upgrade Sweep: ALL Ch 47-59 — **IN PROGRESS**

Sweep mechanism: `patch_slokas.py --split-upgrade` re-extracts all slokas per chapter under the new SPLITTING + ANTI-COLLISION + LORDSHIP QUALIFIER prompt. Dedup (60% DB threshold, excluding `pre_split_merged` originals) ensures only genuinely new individual rules are inserted, tagged `source_note='split_upgrade'`.

**Completed (21 Apr 2026):**
| Ch | MD Lord | New rules | Notes |
|---|---|---|---|
| 48 | Moon | +34 | |
| 52 | Sun | +139 | |
| 53 | Venus | +123 | |
| 54 | Mars | +121 | |
| 55 | Rahu | +153 | First chapter with grouped outcome rules. Sloka 21-24 fix applied — see INGEST_NOTES |
| **Total so far** | | **+570** | |

**Remaining (run in this order):**

```bash
# Ch 55 — Rahu MD (NEXT)
cd /Users/apple/DailyHoroscope-Migration/backend
python3 scripts/patch_slokas.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS ch 55 Vol 2.rtf" \
  --chapter 55 --dasha-lord Rahu \
  --batch-id bphs-ch55-dasha-20260417 \
  --slokas "X" --mongo-url "$MONGO_URL" --db-name horoscope_db --dry-run
# ^ Run with dummy sloka first to get the Available: list, then re-run with all slokas
```

Repeat same pattern for: Ch 56 (Jupiter / bphs-ch56-dasha-20260418 / `BPHS_Ch56_Vol 2.rtf`), Ch 57 (Saturn / bphs-ch57-dasha-20260419 / `BPHS ch 57 Vol 2.rtf`), Ch 58 (Mercury / bphs-ch58-dasha-20260419 / `BPHS_ch 58_Vol 2.rtf`), Ch 59 (Ketu / bphs-ch59-dasha-20260421 / `BPHS_ch59_Vol2.rtf`), Ch 47 (Sun / bphs-ch47-dasha-20260416 / `BPHS Ch 47 Vol 2.rtf`).

### Step 4 — Validate Ch 52/53/54/55 (after split-upgrade done)

Run `validate_rules.py --batch-id <batch-id>` on each once split-upgrade is complete:
```bash
python3 scripts/validate_rules.py --batch-id bphs-ch52-dasha-20260416 --db-name horoscope_db
```

### Step 5 — Next Chapter Ingestion

**BPHS Ch 60** — Prateek has not yet provided RTF. Ask him when sweep is done.

---

## 5. Key Architecture Decisions (locked — do not revisit without strong reason)

### Universal Rule Pattern
Rules at chapter openings before any antardasha sub-section begins:
- **MD-opening general rules** → `antardasha_planet = dasha_lord` (self-period)
- **True universal rules** (all 9 planets in `planets_involved`) → `antardasha_planet = null` + `applies_to_all_dasha_lords = true`
- See INGEST_NOTES.md for full detection signals

### Legacy Model is single source of truth for live data
`vedic_calculator.py` computes all dasha timelines. `knowledge_engine.py` is interpretation layer only. Never add dasha calculation to `knowledge_engine.py`.

### Two-key filtering
Knowledge engine matches rules on BOTH `dasha_lord` AND `antardasha_planet`. Legacy fallback uses `antardasha_lord` field for old rules.

### DB name
Always `horoscope_db`. Never `EverydayHoroscope` (that was a local mistake — 3200 rules were migrated from it on 20 Apr 2026).

---

## 6. Scripts Reference

| Script | Purpose | Key flags |
|---|---|---|
| `ingest_bphs_dasha_v1.py` | Ingest BPHS dasha chapters from RTF | `--chapter --dasha-lord --dry-run` |
| `ingest_bphs_houses_v2.py` | Ingest BPHS house chapters from RTF | `--chapter --house --dry-run` |
| `patch_slokas.py` | Gap-fill under-extracted slokas | `--slokas --dasha-lord --batch-id --dry-run` |
| `validate_rules.py` | Run validator on a batch | `--batch-id` |
| `backfill_antardasha_planet.py` | Backfill `condition.antardasha_planet` | `--dry-run` (Pass 5 complete) |
| `extract_book.py` + `batch_ingest.py` | OCR/PDF pipeline (separate, keep archived) | not for RTF use |

All scripts: `cd /Users/apple/DailyHoroscope-Migration/backend`

---

## 7. Parser Fixes (cumulative — applied to `ingest_bphs_dasha_v1.py`)

| Fix | What | Trigger |
|---|---|---|
| `temperature=0` | Deterministic extraction | Ch 57 non-determinism |
| `condition.antardasha_planet` field | Queryable sub-period planet | KE filtering |
| `SPLITTING GUIDANCE` added | Explicit split/no-split examples | Ch 58 under-extraction |
| `SPLITTING GUIDANCE` OVERHAULED | House-by-house + dignity-by-dignity splits + strength_band mapping | Ch 59 sloka 20-21 analysis — **21 Apr 2026** |
| Period-as-range-separator `5.6.` → `5-6` | `split_into_sloka_blocks()` regex | Ch 59 sloka 5-6 missing |
| Ch 59 added to `INTRO_SLOKAS_BY_CHAPTER` with empty set | No skip-list inheritance | Ch 59 sloka 1-2 |
| `infer_strength_band_from_condition()` + `strength_band` field | `extracted_to_rule()` + `_fallback_rule()` — commit `19cec9e` | `strength_band` was completely absent from dasha pipeline — **21 Apr 2026** |
| **ANTI-COLLISION RULE** added to `EXTRACTION_SYSTEM` | Prevents partial splits: if splitting, must generate ALL individuals AND must NOT also keep a merged rule. Either split completely OR keep merged — never both. | Ch 52 sloka 69-73: Venus 6th missing individually while Venus 6th/8th/12th merged remained — **21 Apr 2026** |
| **LORDSHIP QUALIFIER COMPOUND RULES** added (KEEP AS ONE — point 4) | When source text combines placement list WITH lordship qualifier ("associated with lord of X"), extract individual placement rules per ALWAYS SPLIT PLUS one standalone compound rule capturing placement+lordship | Ch 54 sloka 64-66: compound condition silently absorbed — **21 Apr 2026** |
| `--sloka-filter` flag in dry-run | Shows all rules for a specific sloka label with full field details (dignity_state, strength_band, summary) — enables targeted verification before live ingest | Verification of anti-collision fix in Ch 52 sloka 69-73 — **21 Apr 2026** |
| `strength_band` moderate override in `infer_strength_band_from_condition()` | Checks for "moderate effect/result/at" keywords BEFORE house-based intensity inference — prevents `high` being assigned to rules with explicitly moderated outcomes | Ch 52 fix — **21 Apr 2026** |
| `dignity_state` default changed to `"general"` | Both `extracted_to_rule()` (line 668) and `extracted_to_rule_house_lord()` (line 780): `item.dignity_state or "general"` (was `or ""`) | Remedy rules and uncategorised rules had empty `dignity_state` — **21 Apr 2026** |
| `max_tokens` raised from 2048 → 4096 (commit f1fd623) | Prevents JSON truncation on large slokas with many rules | Ch 52 large sloka extraction — **21 Apr 2026** |

---

## 8. Open Points Across All Chapters

### Ch 12-24 (House chapters)
- 38 flagged rules — not yet reviewed in Rules Browser
- 13 contradiction pairs — not yet resolved
- 197 pending_human_review — awaiting co-founder sign-off
- **Under-split review pending** — same house/dignity bundling issue exists here; assess after dasha split-upgrade sweep is complete

### Ch 47-59 (Dasha chapters)
- **Split-upgrade sweep IN PROGRESS** — Ch 48/52/53/54 done (+417 rules). Ch 55/56/57/58/59/47 still pending.
- **Validation pending** — Ch 52/53/54/55 not yet validated. Run `validate_rules.py` after split-upgrade for each.
- Ch 57 slokas 20-21, 30-31 — over-split suspected, review in Rules Browser after split-upgrade
- Ch 59 sloka 45-47 — OCR-corrupted sloka, verify extracted rules cover all placement conditions
- Ch 59 batch ID in DB is `bphs-ch59-dasha-20260421` (not 20260420 as in some notes)

### ⚠️ Pre-Split_Merged Deprecation — MANDATORY Step 0 Before Co-Founder Review

All `pre_split_merged` original rules across ALL chapters must be deprecated **before Prateek opens Rules Browser for any review**. Without this, he will see:
- 4-5 near-identical merged-condition rows per sloka sitting alongside the correct split rules
- Mixed sub_type errors (e.g. R-BPHS55-020/021 tagged `dasha_unfavourable` on a favourable condition — original ingest error)

**Script (run ONCE after full split-upgrade sweep is complete):**
```python
col.update_many(
    {"metadata.source_note": "pre_split_merged"},
    {"$set": {"approval_status": "deprecated"}}
)
```
Verify with: `col.count_documents({"metadata.source_note": "pre_split_merged", "approval_status": {"$ne": "deprecated"}})` → should return 0.

**Do NOT run mid-sweep** — chapters with pending split-upgrades (56/57/58/59/47) still need their pre_split_merged originals as the only existing coverage until split-upgrade runs.

### Phase 2 — Lordship Qualifier Compound Rules
Chapters ingested before 21 Apr 2026 (Ch 47/48/52/53/54/56/57/58/59) may be missing compound placement+lordship rules. Prompt fix is now in `ingest_bphs_dasha_v1.py`. Audit deferred to after co-founder approval. See INGEST_NOTES.md Phase 2 section for query pattern.

### Ch 48 Schema Gap
34 split-upgrade rules inserted pre-schema-upgrade may lack `dignity_state` or `planet_context_note`. One-shot DB update script needed.

### Co-founder Review Workflow
Not yet commissioned. Prateek must approve before any rule gets `approval_status = 'approved'` (the only status the live backend queries). Zero approved rules currently — Knowledge Engine is interpretation-layer-ready but not live.

### CPath-1 Items
- Item 18: `longevity_router.py` import fail — not addressed
- Item 19: science_registry editor — not addressed
- Commission I-K: Kota Chakra — not addressed

---

## 9. Key Learning — Dry Run vs Live Divergence

> **Higher live count ≠ over-split.** Always verify by reading the source sloka.

Ch 59 slokas 20-21 and 41-42 both showed dry runs (1 and 2 rules) vs live (4 rules each). Both dry runs were WRONG — the live run correctly applied SPLITTING GUIDANCE. The rule: if live count is higher, check the source text. If it lists N distinct house positions or dignity states → N rules is correct.

---

## 10. RTF Files Available

Location: `/Users/apple/Documents/Knowledge Engine_eBooks/`

Confirmed available:
- BPHS Ch 57, 58, 59 Vol 2 ✅
- BPHS Ch 56 Vol 2 ✅

Pending from Prateek:
- BPHS Ch 60 (next in sequence)
- BPHS Ch 52, 53, 54, 55 (in DB but RTF status unclear)
- Lal Kitab, Longevity, Text-Book of Astrology — OCR batches in DB, RTF files not prepared

---

## 11. Git Status

Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
Branch: `main` (deploy-on-push to Vercel + Render)
Last committed: `f07589f` — `feat(ke): add dignity_state and planet_context_note to extraction schema`

**Uncommitted local changes (as of end of Session 4):**
- `backend/scripts/ingest_bphs_dasha_v1.py` — ANTI-COLLISION RULE + LORDSHIP QUALIFIER COMPOUND RULES + `--sloka-filter` flag + moderate strength_band override + `dignity_state` default to "general"
- `.claude/HANDOVER.md` — this document
- `backend/scripts/INGEST_NOTES.md` — Ch 52/53/54 split-upgrade records, grand total update

**Action required at next session start:**
```bash
cd /Users/apple/DailyHoroscope-Migration
git log --oneline -5        # confirm current state
git diff --stat             # confirm uncommitted changes
# then commit the script + doc updates before running any new ingests
```
