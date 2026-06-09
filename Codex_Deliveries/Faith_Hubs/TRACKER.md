# Faith & Scripture -- Module Tracker
> Path: `Codex_Deliveries/Faith_Hubs/TRACKER.md`
> Last updated: 2026-06-07 IST · v1.6

---

## Branch Migration Notice

- Faith work no longer belongs on `codex/everyday-horoscope/zibu-symbols`
- authoritative runtime baseline is now `/Users/apple/DailyHoroscope-Migration` on `main` at `86e53af`
- future Codex delivery branches must use `codex/faith/{commission}`
- the old zibu-symbols Faith worktree is stale for Faith and should not be used as a baseline

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 MAIN BASELINE CONFIRMED -- Pass 5 copied to `main`; `L2` ✅ all types; next Codex scope awaits `FAITH-REWRITE-2` |
| **Backend** | ✅ Delivered + registered in `server.py` |
| **Frontend routes** | ✅ Existing Faith route tree remains live; no new frontend handoff in this notice |
| **Mongo seed** | CC-owned / Render-run only -- `seed_faith_daily_haiku.py` is present in `main`; not a Codex seeding action |
| **ECHO/PACE scan** | ✅ Pass 5 baseline confirmed by Temple Team: `L2 PASS` all 4 types; `L1` still failing for `GITA`, `BIBLE`, and `TRANSIT`; `DAILY` handled through AI seeder path |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **FAITH-1** | Core hub structure | ✅ DELIVERED | `CODEX_COMMISSION_FAITH_1.md` |
| **FAITH-1A** | Hub enhancement | ✅ DELIVERED | `CODEX_COMMISSION_FAITH_1A.md` |
| **FAITH-20K** | 10,500 Gita + 6,000 Bible + 156 Transit + 144 Daily pages | ✅ DELIVERED (generator in repo) | `CODEX_COMMISSION_FAITH_20K.md` |
| **FAITH-HUBS** | Faith hub pages | ✅ DELIVERED | `CODEX_COMMISSION_FAITH_HUBS.md` |
| **FAITH-REWRITE** | L1 fix: verse-specific anchoring for Gita/Bible/Transit/Daily | 🟠 PARTIAL -- Pass 5 baseline copied into `main`. **L2 now PASS all 4 types** ✅. Remaining structural `L1` work for `GITA` / `BIBLE` / `TRANSIT` moves to the next commission path. | prior staging work now superseded by `main` |

---

## Open Points

| ID | Description | Owner | Status |
|---|---|---|---|
| FAITH-OP-1 | Issue FAITH-REWRITE commission (CRITICAL -- Gita L1=100%, Bible L1=82%, Transit L1=100%) | TT/CC | ✅ ISSUED -- Pass 1 + Pass 2 brief in staging worktree |
| FAITH-OP-2 | Draft FAITH-REWRITE Pass 2 brief: full per-function architectural fix spec | CC | ✅ CLOSED 2026-06-04 -- `FAITH_REWRITE_PASS2_BRIEF.md` in staging worktree. |
| FAITH-OP-3 | Do NOT seed any Faith collections from Codex threads | CC | ✅ CLOSED -- Temple Team confirmed CC owns the Render seeder run. Codex should not seed from this thread. |
| FAITH-OP-4 | Re-run ECHO/PACE scan after FAITH-REWRITE delivery | CC | ✅ RUN 2026-06-06 (Pass 5) |
| FAITH-OP-5 | Issue FAITH-REWRITE Pass 4 to Codex (or CC direct fix) | TT/CC | ✅ CLOSED -- CC executed Pass 5 direct edits. L2 now PASS all types. |
| FAITH-OP-6 | Run Layer G before any future Faith collection seed handoff | CC | PENDING -- still required in the next accepted rewrite / seeder cycle |
| FAITH-OP-7 | Strategic decision on L1 | TT/CC | ✅ DECISION MADE -- `DAILY` resolves through AI seeder; `GITA` / `BIBLE` / `TRANSIT` move to `FAITH-REWRITE-2` |
| FAITH-OP-8 | L3 title Jaccard fixes: GITA 81.82%, TRANSIT 66.67%, DAILY 77.78% all above 60% threshold. BIBLE passes. | CC | PENDING -- now expected under `FAITH-REWRITE-2` or later Temple-directed follow-up |
| FAITH-OP-9 | Lumina verse cache (`lumina_verse_cache`): 14 pre-generated verse breakdowns (7 Bible + 7 Gita). Eliminates live Anthropic API calls on `/api/lumina/daily-verse`. Cache-check wired in `lumina_router.py` v1.1.0. Run `--type lumina` seed. | CC | 🟡 READY TO RUN by CC alongside DAILY batch when Temple schedules it |
| FAITH-OP-10 | Faith branch migration enforcement: retire `codex/everyday-horoscope/zibu-symbols` for Faith and use `codex/faith/{commission}` going forward. | TT/Codex | ✅ CLOSED -- documented in Temple handoff and tracker |
| FAITH-OP-11 | Start next structural rewrite only from `main` baseline commit `86e53af` and await `CODEX_COMMISSION_FAITH_REWRITE_2.md`. | Codex | 🟡 OPEN -- next expected commission state |

---

## ECHO/PACE Results (2026-06-04 -- Pass 1 staging baseline)

### Pass 1 baseline -- 2026-06-04

| Page Type | Sample | L1 | L2 | L3 | Verdict |
|---|---|---|---|---|---|
| GITA | chapters 1-5 × 9 situations | 97.00% | FAIL ❌ | FAIL ❌ | BLOCKED ❌ |
| BIBLE | 10 topics × 10 transitions | 77.56% | FAIL ❌ | FAIL ❌ | BLOCKED ❌ |
| TRANSIT | all transit slugs × 2 traditions | 85.45% | FAIL ❌ | FAIL ❌ | BLOCKED ❌ |
| DAILY | 12 signs × 12 months | 64.27% | FAIL ❌ | PASS ✅ | BLOCKED ❌ |

### Pass 5 baseline on `main` -- confirmed 2026-06-07

| Page Type | L1 | L2 | L3 | Verdict |
|---|---|---|---|---|
| GITA | 91.25% ❌ | **PASS ✅** | 81.82% ❌ | `L2` cleared; future structural rewrite still required |
| BIBLE | 78.35% ❌ | **PASS ✅** | 50.00% ✅ | `L2` cleared; `L1` still needs architectural work |
| TRANSIT | 84.60% ❌ | **PASS ✅** | 66.67% ❌ | `L2` cleared; future structural rewrite still required |
| DAILY | 91.10% ❌ | **PASS ✅** | **PASS ✅** | template path still high on `L1`; Temple handoff says daily AI seeder resolves this path |

**Pass 5 root cause / what was fixed (CC 2026-06-06):**
- GITA: `faq_seed` modulus 3→7, then 7→8 approach used via modulus=7. Added 4 new FAQ variants (0→7 total). `practice_prompts` modulus 4→8 with 4 new prompt sets. Fixed consecutive fixed-token sequences in existing prompts.
- BIBLE: `_bible_faq()` modulus 6→7→8. Added explicit selectors 5, 6 + new fallback (selector 7). `_bible_hermeneutical()` modulus 6→8. Added 2 new hermeneutical options.
- TRANSIT: `_transit_faq()` modulus 6→7→8. Added explicit selectors 5, 6 + new fallback (selector 7). All 6 TRANSIT_FAMILY planet `practice` texts rewritten to "Practice [adj noun]." (3 content tokens after stop-filtering) to prevent 15.4%/planet ceiling violations.
- DAILY: `_daily_faq()` modulus 6→7→8. Added explicit selectors 5, 6 + new fallback (selector 7). Removed `element_line` from `_daily_bible_application()` (was doubling `month_energy` appearance, causing L1 regression).

**L1 structural ceiling explanation:**
- GITA 91%: Template boilerplate (~150 shared tokens at IDF 1.5) overwhelms 3 verse-unique focus_words (~17 appearances at IDF 2.0). With 15 situations × 1,167 verses, cosine similarity can never drop below ~85% without AI-generated unique content.
- BIBLE 78%: `_bible_hermeneutical()` shared tokens across transition clusters dominate.
- TRANSIT 85%: Planet-core and watch_for text shared across tradition pages.
- DAILY 91%: Gita+Bible application text concatenation creates high shared vocabulary across same-sign and same-month pages.

**Temple handoff decision now in force:** `DAILY` moves through the AI seeder path under CC / Render. `GITA`, `BIBLE`, and `TRANSIT` remain queued for `FAITH-REWRITE-2`.

### Pass 3 -- 2026-06-05 (delivered, not accepted)

| Page Type | L1 | L2 | L3 | Verdict |
|---|---|---|---|---|
| GITA | 96.22% ❌ | FAIL ❌ | 77.78% ❌ | NOT ACCEPTED |
| BIBLE | 77.47% ❌ (regressed from Pass 2 65.35%) | FAIL ❌ | PASS ✅ | NOT ACCEPTED |
| TRANSIT | 79.33% ❌ | FAIL ❌ | 66.67% ❌ | NOT ACCEPTED |
| DAILY | 68.76% ❌ | FAIL ❌ | 77.78% ❌ | NOT ACCEPTED |

**Pass 3 root cause (CC code-read diagnosis 2026-06-05):**
- GITA 96%: `_gita_hook()` uses `situation['hidden_fear'].lower()` (~8 words) + `situation['practice_shift']` (~8 words) verbatim in 6/8 variants. `_gita_application()` uses `situation['action_focus']` (~6 words) verbatim in ALL 8 variants. These 22 situation-level content words at IDF 2.2 dominate the 3 focus_words at IDF 6.6. Mathematical fix: replace full-phrase fills with `_situation_vocabulary()` single tokens.
- BIBLE 77%: `_bible_hermeneutical()` uses `transition['faith_need']` (~5 words) + `transition['core_pain']` (~6 words) verbatim in 5/6 variants. Transition-level constants dominate for same-transition page clusters.
- TRANSIT 79%: modulus=6 → 12 pages/slot. Skeleton word IDF = 1.8. Fix: expand to modulus=12 (6 pages/slot, IDF 2.5).
- DAILY 69%: `gita['reference']` appears 2× per field (sign-level constant, same for all 12 months). `sign['growth_edge']` appears 2-3× per field. Month-unique fills insufficient.

**Pass 4 brief: `FAITH_REWRITE_PASS4_BRIEF.md` in staging worktree (written 2026-06-05).**

---

## ECHO/PACE Results (2026-05-31 -- original baseline)

Full report: `Codex_Deliveries/ECHO_PACE/ECHO_PACE_SCAN_RUD_CRY_FAITH_2026-05-31.md`

| Page Type | Total | Sample | L1 | L2 | L3 | Verdict |
|---|---|---|---|---|---|---|
| GITA | 10,500 | 3,480 | 100.0% | FAIL ❌ | FLAGGED ⚠️ | BLOCKED ❌ |
| BIBLE | 6,000 | 100 | 81.7% | FAIL ❌ | FLAGGED ⚠️ | BLOCKED ❌ |
| TRANSIT | 156 | all | 99.5% | FAIL ❌ | FLAGGED ⚠️ | BLOCKED ❌ |
| DAILY | 144 | all | 50.0% | FAIL ❌ | FLAGGED ⚠️ | ON-GATE ⚠️ |

### L1 Root Cause -- Gita (100%)
`get_gita_page()` fills `summary`, `hook`, and `application` from `situation['hook']`, `situation['hidden_fear']`, `situation['practice_shift']` -- constants per situation. These strings are **identical for every verse in the same situation** (e.g., all 700+ Gita pages for "Relationship Breakdown" share word-for-word body text). Only the chapter:verse number token changes, which has negligible TF-IDF weight → cosine = 1.0 within cluster.

Key evidence -- the following phrase appears verbatim on every one of the 10,500 Gita pages:
```
"It does not ask for denial. It asks for a truer next step"
```

### L1 Root Cause -- Bible (81.7%)
`summary` field: `"This page approaches {transition} through the Bible theme of {topic}, keeping the promise practical, emotionally honest, and connected to a parallel Vedic bridge."` -- this fixed sentence appears on every Bible page. Verse text contributes some variation, but shared boilerplate vocabulary dominates.

### L1 Root Cause -- Transit (99.5%)
Transit pages exist in Gita and Bible tradition variants. "Mars Retrograde - Gita" vs "Mars Retrograde - Bible" share identical transit-level body content (panchang description, transit_layer, practice text) with only the verse citation differing → near-identical TF-IDF vectors.

### Fix Specification for FAITH-REWRITE Commission
Must address all four areas:

1. **Gita per-verse anchoring**: `hook` and `summary` must incorporate the specific verse's translation keywords (min 2 verse-unique words, not situation boilerplate). Use `_hash_index(chapter, verse_num, situation_slug, modulus=8)` to select from 8 situation sub-templates, each seeded by different verse content.

2. **Bible per-verse body**: `summary` and `emotional_frame` must vary by verse content. At minimum: 5 topic-variant opening sentences, selected by hash. Remove the fixed template sentence.

3. **Transit tradition separation**: Gita-tradition and Bible-tradition transit pages must have meaningfully distinct body text. Currently near-identical. Each tradition must have a minimum of 3 distinct framing approaches per transit family (retrograde, ingress, etc.).

4. **Daily seasonal variation**: `summary` and `message` must have at least 5 monthly framing variants per sign, hash-selected. Currently 12 months × 12 signs share too much seasonal vocabulary.

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.6 | 2026-06-07 | Temple Team branch migration notice synced into tracker. Faith source of truth confirmed on `main` at `86e53af`. Old `codex/everyday-horoscope/zibu-symbols` Faith worktree marked stale. New delivery branch rule set to `codex/faith/{commission}`. Tracker updated to reflect Pass 5 as the authoritative baseline, CC ownership of daily seeding, and `FAITH-REWRITE-2` as the next expected Codex commission. | Codex | Temple handoff |
| v1.5 | 2026-06-06 | AI seeder `backend/scripts/seed_faith_daily_haiku.py` written. Phase 1 scope: 144 DAILY pages (faith_daily_pages) + 14 Lumina verse breakdowns (lumina_verse_cache). Uses Claude Haiku. `lumina_router.py` bumped to v1.1.0 -- `/daily-verse` now checks lumina_verse_cache before live API call. All imports verified locally. Ready to run `--type all --limit 5 --dry-run` on Render to confirm before full batch. FAITH-OP-7 decision closed. FAITH-OP-9 opened. | CC direct | live repo |
| v1.4 | 2026-06-06 | Pass 5 CC direct edits applied to staging worktree. **L2 PASS all 4 types** ✅ -- all L2 4-gram violations cleared. L1 still FAIL (structural ceiling; mathematically unachievable for GITA/DAILY at 91%). Strategic decision needed: relax L1 threshold or accept L2-only gate. L3 PASS for BIBLE only. FAITH-OP-5 closed; FAITH-OP-7, FAITH-OP-8 opened. | CC direct | staging worktree |
| v1.3 | 2026-06-05 | Pass 3 delivered (not accepted). GITA 96.22%, BIBLE 77.47% (regressed), TRANSIT 79.33%, DAILY 68.76% -- all L2 FAIL, all L1 failing. Root cause confirmed by CC code reading: full-phrase situation/transition constants verbatim in scanned fields. Pass 4 brief written with surgical per-function fixes: G1 (hook single tokens), G2 (application single tokens), G3 (faq transit_label), G4 (title 3 focus_words), B1 (hermeneutical extraction helper), T1-T2 (transit modulus 6→12 with 12 variants per function), D1-D3 (daily sign vocab reduction + month fills + modulus 4→8). | CC | `FAITH_REWRITE_PASS4_BRIEF.md` |
| v1.2 | 2026-06-04 | FAITH-REWRITE Pass 2 architectural brief written. Full per-function root-cause analysis for all 4 page types. 9 specific function changes specified. Staging baseline (Pass 1) confirmed: GITA 97%, BIBLE 77.56%, TRANSIT 85.45%, DAILY 64.27%. FAITH-OP-2 closed. | CC | `FAITH_REWRITE_PASS2_BRIEF.md` |
| v1.1 | 2026-05-31 | ECHO/PACE scan run. CRITICAL: Gita L1=100%, Bible L1=82%, Transit L1=100%. All 4 types L2 FAIL. Module BLOCKED. FAITH-REWRITE commission brief required. Tracker created. | CC | `ECHO_PACE_SCAN_RUD_CRY_FAITH_2026-05-31.md` |
| v1.0 | 2026-05 | FAITH-20K generator delivered by Codex (faith_gita_data.py, faith_bible_data.py, faith_seo_data.py). Backend registered. | Codex | `CODEX_COMMISSION_FAITH_20K.md` |
