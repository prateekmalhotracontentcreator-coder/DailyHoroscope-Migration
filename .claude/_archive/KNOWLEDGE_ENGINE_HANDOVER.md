# Knowledge Engine — Session Handover
Date: 18 April 2026

## Non-Negotiable Rule
`approval_status = "approved"` is the ONLY status that reaches live users.
Flow: `pending_review` → validated → `auto_approved` / `pending_human_review` → co-founder promotes to `approved`.
**Decision standing:** Do NOT promote anything yet. Promote only after full multi-book ingest is complete.

---

## ⚠️ Critical Workflow Rule — Always Run Scripts from Main

**Always run ingest/validate scripts from the main repo directory:**
```
cd ~/DailyHoroscope-Migration
python3 backend/scripts/ingest_bphs_dasha_v1.py ...
```
**Never run from a worktree path.** Worktrees are for code editing only.

**Workflow:**
1. Claude Code edits script in worktree
2. Commit + merge to main
3. Run script from `~/DailyHoroscope-Migration/`

---

## Current DB State — 18 April 2026

| Source | Chapter | Topic | Rules | auto_approved | pending_review | flagged | Batch ID |
|---|---|---|---|---|---|---|---|
| BPHS Vol 1 | Ch 12-18 | Houses 1-7 | 241 | 58% | 33% | 12% | bphs-ch12..18-v2-20260414 |
| BPHS Vol 1 | Ch 19-23 | Houses 8-12 | 119 | 59% | 33% | 8% | bphs-ch19..23-v2-20260415 |
| BPHS Vol 1 | Ch 24 | Bhava Lords | 376 | 71% | 20% | 9% | bphs-ch24-v2-20260416 |
| BPHS Vol 2 | Ch 47 | Mahadasha by Planet | 93 | 82% | 14% | 4% | bphs-ch47-dasha-20260416 |
| BPHS Vol 2 | Ch 48 | Dasha of House Lords | 46 | 74% | 24% | 2% | bphs-ch48-dasha-20260416 |
| BPHS Vol 2 | Ch 52 | Antardasha in Sun MD | 93 | 83% | 14% | 3% | bphs-ch52-dasha-20260416 |
| BPHS Vol 2 | Ch 53 | Antardasha in Moon MD | 68 | 76% | 18% | 6% | bphs-ch53-dasha-20260417 |
| BPHS Vol 2 | Ch 53 patch | Venus Antardasha supplement | 4 | — | 100% | — | bphs-ch53-venus-patch-20260417 |
| **TOTAL** | | | **1,040** | **~70%** | **~23%** | **~7%** | |

**MongoDB collections:** `import_batches` · `interpretation_rules` · `science_registry` ✅

**Ch 53 patch note:** 4 rules are `codex_supplement` / `confidence.base = 0.65` / `pending_human_review` — require expert Vedic review before promotion. Slokas 53-55 genuinely absent from RS Santhanam edition.

---

## MongoDB Collections — Full State

| Collection | Documents | Purpose |
|---|---|---|
| `interpretation_rules` | 1,040 | All ingested rules |
| `import_batches` | per-batch | Ingest audit log |
| `science_registry` | 4 | Science hierarchy for Sprint 2 arbitration |

**science_registry seed (inserted 18 Apr):**
| rank | science_id | contradiction_policy |
|---|---|---|
| 1 | vedic_astrology | backbone_or_primary_lead |
| 2 | numerology | secondary_supportive |
| 3 | palmistry | secondary_specialist |
| 4 | tarot | reflective_advisory |

---

## Scripts Available (all in `backend/scripts/`)

| Script | Purpose | Key args |
|---|---|---|
| `ingest_bphs_houses_v2.py` | House + Bhava Lord chapters (BPHS Vol 1) | `--rtf --chapter 12-24 --house 1-12 or 0` |
| `ingest_bphs_dasha_v1.py` | Dasha chapters (BPHS Vol 2 Ch 47/48/52-60) | `--rtf --chapter --dasha-lord (optional)` |
| `validate_rules.py` | Run validation on a batch | `--mongo-url --db-name --batch-id` |
| `patch_punctuation.py` | Add terminal punctuation to rules missing it | `--batch-id` |
| `reset_to_pending.py` | Reset rejected rules back to pending_review | `--batch-id` |
| `peek_rules.py` | Quick spot-check of rules in DB | `--batch-id --limit` |
| `patch_ch53_venus_antardasha.py` | Insert Ch 53 Venus patch (4 rules) | `--mongo-url --db-name` |
| `seed_science_registry.py` | Seed science_registry collection | `--mongo-url --db-name` ✅ already run |

**All scripts require:** `ANTHROPIC_API_KEY`, `MONGO_URL`, `DB_NAME=EverydayHoroscope`

---

## RTF Files Location
`/Users/apple/Documents/Knowledge Engine_eBooks/`

| File | Status |
|---|---|
| `BPHS Ch 12-23 Vol 1.rtf` (individual files) | ✅ Ingested |
| `BPHS Ch 24 Vol1.rtf` | ✅ Ingested |
| `BPHS Ch 47 Vol 2.rtf` | ✅ Ingested |
| `BPHS Ch 48 Vol 2.rtf` | ✅ Ingested |
| `BPHS Ch 52 Vol 2.rtf` | ✅ Ingested |
| `BPHS Ch 53_Vol 2_ Sloka 53,54,55 missing from Book.rtf` | ✅ Ingested (+ patch applied) |
| `BPHS Ch 54 Vol 2.rtf` | ✅ **RTF READY — ingest next session** |
| `BPHS Ch 55 Vol 2.rtf` | ✅ **RTF READY — ingest next session** |
| Ch 56-60 | ❌ Needs RTF conversion from PDF |
| A Text Book of Astrology Ch 15, 16 | ❌ Needs RTF conversion |

---

## ⚡ Next Session — Immediate Tasks (Priority Order)

### Priority 1: Process Sprint 2 Codex Response

Sprint 2 response has arrived (user confirmed). Codex delivered commit `9915b60` — +506 lines to `backend/knowledge_engine.py`.

**What was delivered (from commit inspection):**
- `DEFAULT_SUPERSESSION_MAP` — hardcoded fallback for G-04
- `_contradiction_score()` + `_contradiction_components()` — G-03 C-score formula
- `_representation_mode()` — G-05 synthesis/tension/honest_uncertainty selector
- `_build_tension_block()` — G-06 evidence packet builder
- `_resolve_supersession_order()` + `_science_authority_rank()` — G-04 lookup
- `_arbitration_summary()` — aggregation helper
- Full domain helpers: `_polarity_distance()`, `_timing_distance()`, `_strength_distance()`, `_authority_distance()`

**Sprint 2 gate — must verify (5 criteria):**
1. `_contradiction_score(rule_a, rule_b)` returns correct C-score for known opposing/agreeing pairs
2. `_representation_mode(c_scores)` → `synthesis` for C<0.30, `tension` for 0.30–0.75, `honest_uncertainty` for C>0.75
3. `_build_tension_block(rule_a, rule_b, c_score, domain)` returns correctly shaped dict with all required fields
4. Supersession lookup correctly returns highest-ranked science for a given domain
5. `scan_chart()` output includes `representation_mode` and `tension_blocks` in response payload

**Action:** Read the full diff, run gate verification, confirm pass/fail. If passed → immediately issue Sprint 3 brief.

### Priority 2: Ingest Ch 54 — Antardasha in Mars Mahadasha

```bash
cd ~/DailyHoroscope-Migration
python3 backend/scripts/ingest_bphs_dasha_v1.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Ch 54 Vol 2.rtf" \
  --chapter 54 \
  --mongo-url "$MONGO_URL" --db-name EverydayHoroscope

# Then validate:
python3 backend/scripts/validate_rules.py \
  --mongo-url "$MONGO_URL" --db-name EverydayHoroscope \
  --batch-id bphs-ch54-dasha-YYYYMMDD
```

- Script auto-detects `dasha_lord = "Mars"` via `ANTARDASHA_CHAPTER_LORD[54]`
- No `--dasha-lord` flag needed
- Expected: ~80 rules, ~80% auto_approved

### Priority 3: Ingest Ch 55 — Antardasha in Rahu Mahadasha

```bash
python3 backend/scripts/ingest_bphs_dasha_v1.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Ch 55 Vol 2.rtf" \
  --chapter 55 \
  --mongo-url "$MONGO_URL" --db-name EverydayHoroscope
```

- Script auto-detects `dasha_lord = "Rahu"` via `ANTARDASHA_CHAPTER_LORD[55]`
- Rahu chapters often have edge cases — watch for unusual planet name variants in RTF ("Raahu", "Dragon's Head")
- Expected: ~80 rules

### Priority 4 (if Sprint 2 gate passes): Issue Sprint 3 Brief

**Sprint 3 — Arc Angel computation (G-07/G-08/G-09)**
- G-07: `period_quality_now` per domain (current active Mahadasha × Antardasha quality)
- G-08: `period_quality` per prediction (per-rule quality assignment)
- G-09: 10-year auspicious/inauspicious windows
- Est. 16–24h
- **Critical constraint:** G-07/G-08/G-09 must consume POST-ARBITRATION, POST-CONVERGENCE output — not raw matched rules
- Full brief to write once Sprint 2 gate confirmed passed

---

## Knowledge Engine Phase 1.2 — Sprint Tracker

| Sprint | Gaps | Status | Gate | Commit |
|---|---|---|---|---|
| Sprint 1 | G-01 α/β/γ scoring | ✅ COMPLETE | ✅ All 6 cases passed | `57e347a` |
| Sprint 2 | G-03/G-05/G-06/G-04 arbitration | ✅ DELIVERED | ⬜ **Verify gate next session** | `9915b60` |
| Sprint 3 | G-07/G-08/G-09 Arc Angel | ⬜ After Sprint 2 gate | — | — |

**G-02 (tier multipliers):** Confirmed deferred — requires claim clustering, not a standalone fix. Codex confirmed this twice.

---

## Antardasha Chapters — Full Status

| Ch | Dasha Lord | Status | Batch ID |
|---|---|---|---|
| 52 | Sun | ✅ 93 rules, 83% approved | bphs-ch52-dasha-20260416 |
| 53 | Moon | ✅ 68 rules + 4 patch | bphs-ch53-dasha-20260417 |
| 54 | Mars | ⬜ **RTF ready — ingest next session** | — |
| 55 | Rahu | ⬜ **RTF ready — ingest next session** | — |
| 56 | Jupiter | ❌ RTF needed | — |
| 57 | Saturn | ❌ RTF needed | — |
| 58 | Mercury | ❌ RTF needed | — |
| 59 | Ketu | ❌ RTF needed | — |
| 60 | Venus | ❌ RTF needed | — |

---

## What Was Fixed This Session (18 Apr)

### 1. Lo Shu Grid CSS — FIXED ✅ (commit `878edd3`)
- **Root cause:** `numerology.css` simply did not exist — zero CSS for any numerology BEM class
- **Fix:** Created `frontend/src/numerology.css` — complete stylesheet covering LoShuGrid (3×3 grid), LuckyElementsTable, NumerologyReportPage, chips, remediation plan, remedy card, timing panel
- **Imported** in `App.js` alongside `App.css` and `panchang.css`
- **Deployed** to Vercel — live

### 2. NumerologyReportPage — Already Fixed (April 6, confirmed this session)
- `NumerologyReportPage.jsx` is already the v4 renderer (commit `6253402`, 6 Apr)
- All 4 post-integration gaps addressed: RemedyCard, TimingPanel, SEO, favorable_timing
- No further action needed

### 3. Sprint 1 G-01 — Gate Verified ✅
- `_contextual_adjustment()` formula confirmed correct via independent gate run
- All 6 test cases passed locally

### 4. science_registry — Seeded ✅
- 4 documents inserted via `seed_science_registry.py`
- Sprint 2 G-04 blocker cleared

---

## Pending Codex Actions

| Action | Detail | Status |
|---|---|---|
| TD-26 + TD-27 in CONTRACT | Country Kundali signal + Forecast Tier | ✅ DONE — Sections 23+24, commit `57e347a` |
| Sprint 1 G-01 | α/β/γ scoring | ✅ DONE |
| Sprint 2 G-03/G-05/G-06/G-04 | Arbitration runtime | ✅ DELIVERED — gate check pending |
| **Sprint 3 brief** | G-07/G-08/G-09 Arc Angel | ⬜ Issue after Sprint 2 gate confirmed |
| Ch 53 Venus patch expert review | 4 `codex_supplement` rules need Vedic expert sign-off before promotion | ⬜ Ongoing |

---

## Open Issues (Pre Co-Founder Review)

1. **82 flagged rules** across all batches — Admin > Rules Browser > filter: flagged → dismiss / edit / escalate
2. **~244 pending_human_review rules** — awaiting co-founder sign-off
3. **25 contradiction pairs** (13 in Ch 12-23; 5 in Ch 48; 3 in Ch 52; 4 in Ch 53) — verify genuine classical contradictions vs validator false positives
4. **4 Ch 53 patch rules** — `codex_supplement`, `pending_human_review` — need Vedic expert review before promotion
5. **Ch 54-60 RTF conversions** — only Ch 54 + Ch 55 available; Ch 56-60 still need PDF→RTF

---

## Approval Milestone Target
Promote to `approved` after full multi-book ingest is complete:
- ✅ BPHS Vol 1 Ch 12-24 (736 rules)
- ✅ BPHS Vol 2 Ch 47-48 (139 rules)
- ✅ BPHS Vol 2 Ch 52-53 (165 rules)
- ⬜ BPHS Vol 2 Ch 54-60 (7 chapters — est. ~560 rules)
- ⬜ A Text Book of Astrology Ch 15 (~100-150 rules cross-validation)

---

## Pending Codex Review (Phase 2 — Do Not Build Yet)

**TD-26 — Country Kundali as Alpha Signal** `LOCKED Phase 2`
- Phase 2: `CountryKundaliSignal` as typed subtype under `alpha` umbrella
- Weighting: same country=100/0 · abroad <2yr=70/30 · 2–7yr=interpolate · >7yr=30/70
- Do not build before Commission J (World Context Engine)

**TD-27 — Forecast Tier / Life Area Outlook** `LOCKED Phase 2`
- Field: `forecast_tier` · User label: **"Life Area Outlook"** (Founder confirmed)
- 6-band valence overlay per domain/section — coexists with `period_quality` and `representation_mode`
- Phase 2 internal only first; user-facing after wording validation

---

## Validation Command Templates

```bash
# Ingest
python3 backend/scripts/ingest_bphs_dasha_v1.py \
  --rtf "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Ch 54 Vol 2.rtf" \
  --chapter 54 \
  --mongo-url "$MONGO_URL" --db-name EverydayHoroscope

# Validate
python3 backend/scripts/validate_rules.py \
  --mongo-url "$MONGO_URL" --db-name EverydayHoroscope \
  --batch-id bphs-ch54-dasha-YYYYMMDD

# Peek rules
python3 backend/scripts/peek_rules.py \
  --mongo-url "$MONGO_URL" --db-name EverydayHoroscope \
  --batch-id bphs-ch54-dasha-YYYYMMDD --limit 10
```
