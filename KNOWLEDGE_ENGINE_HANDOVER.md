# Knowledge Engine — Session Handover
**EverydayHoroscope | Co-Founder Working Document**
Last updated: 14 April 2026
For: Starting a new Claude Code chat session

---

## 1. What This Document Is

The chat has compressed twice. This document captures the complete state of
Commission I (Knowledge Engine) so the next session can pick up without
reconstructing context.

**Companion documents already in the repo:**
- `KNOWLEDGE_ENGINE_STRATEGY.md` — full objectives, phase 1 book table, issues log, agreed next steps
- `CLAUDE.md` — project identity, infrastructure, file locations, environment variables

---

## 2. The Prediction Engine — Three-Layer Architecture

This is the agreed mental model. Every decision made in this commission maps to it.

```
Layer 1 — NATAL (static, permanent)
  planet_in_house              — inherent effect of planet in that house (all of life)
  planet_in_house_in_sign      — same, refined by zodiac sign
  planet_in_house_special      — same, modified by state (exalted/debilitated/own/enemy)
  Source: Chapter 15, A Text Book of Astrology ✅ BUILT

Layer 2 — DASHA (dynamic, changes every 6–20 years)
  dasha_planet_from_house      — what events arrive when planet X runs its Mahadasha
                                  and sits natally in house Y
  antardasha_compound          — sub-period compounding (Maha lord × Antar lord)
  Source: BPHS Dasha chapters ❌ NOT YET BUILT
  (highest priority next ingest — transforms engine from personality descriptor
   to timed event predictor)

Layer 3 — TRANSIT (real-time, future phase)
  transit_planet_over_natal_house
  Source: future Phase 2
```

**Event Prediction Formula:**
```
Event = Natal Condition (what) × Dasha Activation (when) × Transit Trigger (now)
```

---

## 3. Knowledge Engine — Script Inventory

All scripts live in `backend/scripts/`.

| Script | Purpose | Status |
|---|---|---|
| `batch_ingest.py` | CLI: processes PDF/DOCX per book config → MongoDB | ✅ Working |
| `extract_book.py` | Core extraction: text → Claude/GPT → rule documents | ✅ Working |
| `ingest_chapter15.py` | Dedicated RTF parser for Ch 15 (Option B) | ✅ Working |
| `validate_rules.py` | 4-stage validation pipeline → approval_status | ✅ Working |
| `review_book.py` | Full book review: approved/flagged breakdown | ✅ Working |
| `review_approved.py` | Auto-approved rules only, per book | ✅ Working |
| `peek_rules.py` | Diagnostic: sample rules, error placeholder count | ✅ Working |
| `BOOKS_MASTER_CONFIG.json` | Master list of all 8 Phase 1 books | ✅ Ready |

---

## 4. Book Config Files

| Config file | Book | Chapters | Notes |
|---|---|---|---|
| `a_text_book_of_astrology.json` | A Text Book of Astrology | 12 | Ch 15 now points to `.docx` |
| `bphs.json` | Brihat Parashara Hora Shastra | 1 (full PDF) | Single-file, max_rules=500 |
| `phaladeepika.json` | Phaladeepika | 1 (full PDF) | Single-file, max_rules=500 |
| `lal_kitab.json` | Lal Kitab | 29 chapters | Fully mapped per chapter |
| `longevity_astro_system.json` | Longevity & Astro System | Multiple | ✅ Ingested |
| `300_horoscopes_vol1.json` | 300 Important Horoscopes Vol I | Multiple | ✅ Ingested |
| `longevity_unnatural_death.json` | Longevity & Un-Natural Death | Multiple | ✅ Ingested |
| `300_important_combinations_bv_raman.json` | 300 Important Combinations | 1 (full PDF) | ✅ Ingested |

---

## 5. MongoDB Collections

| Collection | Contents | Approximate Count |
|---|---|---|
| `interpretation_rules` | All extracted rules (all books) | ~946 (Phase 1 V2) + 622 (Ch 15 Option B, pending insert) |
| `import_batches` | One doc per ingest batch; tracks import_status | 1 per chapter per book |

**Approval status breakdown (Phase 1 V2, OCR pipeline):**
- `auto_approved`: 190 (20%)
- `pending_human_review`: 202 (21%)
- `flagged`: 553 (58%)
- `rejected`: 3 (0%)

**Chapter 15 Option B rules (not yet inserted — dry run only so far):**
- `planet_in_house` base rules: 103
- `planet_in_house_in_sign` sign variants: 346
- `planet_in_house_special` (exalted/debilitated/own/enemy): 173
- **Total: 622 rules**
- batch_id: `a-text-book-ch15-v2-20260414`

---

## 6. Chapter 15 — Option B Architecture (Key Decision)

This is the most important architectural decision made this session. Understand this before touching `ingest_chapter15.py`.

**Why Option B (not A):**
Option A = one rule per planet-house block (103 rules, verbatim, no sub-conditions).
Option B = main rule + sign sub-rules + special-state sub-rules (622 rules total).

Option B was chosen because the sign and special-state sub-rules create
**condition slots** that act as the cross-book spine:

```
R-ATEXTB-SUN-1H-CAN-V-001-02   ← Ch 15 verbatim: "If Sun in Cancer sign eyes small"
                                    ↑ same condition type: planet_in_house_in_sign
R-BPHS-SUN-1H-CAN-001          ← BPHS: "Sun in Cancer ascendant — round face, devoted to mother"
R-LALKITAB-SUN-1H-CAN-001      ← Lal Kitab: "Sun in Cancer — government favour, mother's support"
```

All three rules share condition `{planet: Sun, house: 1, sign: Cancer}`.
The query layer unions them → cross-reference comparison → confidence weighting.

**Rule ID scheme:**
```
R-ATEXTB-SUN-1H-V-001          planet_in_house (main)
R-ATEXTB-SUN-1H-CAN-V-001-02   planet_in_house_in_sign (Cancer)
R-ATEXTB-SUN-1H-EXA-V-001-07   planet_in_house_special (exalted)
R-ATEXTB-SUN-1H-DEB-V-001-06   planet_in_house_special (debilitated)
R-ATEXTB-SUN-1H-OWN-V-001-08   planet_in_house_special (own_sign)
```

**5 missing planet-house combos in the RTF** (genuinely absent — not parser gaps):
Moon H5, Jupiter H8, Saturn H11, Ketu H2, Ketu H12

---

## 7. Key Technical Fixes Applied This Commission

All committed to `main`. Do not re-apply.

| Fix | Commit | Detail |
|---|---|---|
| Duplicate rule IDs across chapters | `f502013` | `rule_index_offset` in ExtractionArgs — book-wide counter passed per chapter |
| Silent OpenAI failures | `208f945` | `except Exception as exc: print(...)` instead of silent None |
| Token truncation (75% of Book 1 flags) | `208f945` | `max_tokens` 900 → 1800 in `paraphrase_with_openai()` |
| Truncation detection | `208f945` | `structural_check()` rejects rules not ending in `.!?"'` |
| Validation prompt for composite conditions | `a0f5d1a` | Claude told composite conditions are valid general principles |
| `.docx` support with heading context | `9d66c32` | `extract_text_from_docx()` prefixes each paragraph with its section heading |
| Chapter 15 Option B | `9d268c5` | 3-tier rule expansion: base + sign variants + special states |

---

## 8. How to Run Things

**Environment setup (must do each terminal session):**
```bash
cd ~/DailyHoroscope-Migration/backend
export OPENAI_API_KEY="sk-proj-..."         # from OpenAI project console
export ANTHROPIC_API_KEY="sk-ant-..."       # for validation
export MONGO_URL="mongodb+srv://..."        # full connection string, no leading space
```

**Insert Chapter 15 Option B rules into MongoDB (622 rules — PENDING):**
```bash
python3 scripts/ingest_chapter15.py \
  --rtf "~/Documents/Knowledge Engine_eBooks/Chapter 15.rtf" \
  --mongo-url "$MONGO_URL" \
  --db-name EverydayHoroscope
# Remove --dry-run is already absent — this will write to MongoDB
# Add --dry-run to preview only
```

**Batch ingest a single book:**
```bash
python3 scripts/batch_ingest.py \
  --config scripts/bphs.json \
  --books-dir "~/Documents/Knowledge Engine_eBooks/" \
  --mongo-url "$MONGO_URL" \
  --db-name EverydayHoroscope \
  --output-dir ./output \
  --dry-run     # remove for live insert
```

**Batch ingest ALL Phase 1 books:**
```bash
python3 scripts/batch_ingest.py \
  --master scripts/BOOKS_MASTER_CONFIG.json \
  --mongo-url "$MONGO_URL" \
  --db-name EverydayHoroscope \
  --output-dir ./output \
  --dry-run
```

**Validate a batch:**
```bash
python3 scripts/validate_rules.py \
  --mongo-url "$MONGO_URL" \
  --db-name EverydayHoroscope \
  --batch-id "a-text-book-of-astro_001_20260414" \
  --dry-run
```

**Review a book's rules:**
```bash
python3 scripts/review_book.py \
  --mongo-url "$MONGO_URL" \
  --db-name EverydayHoroscope \
  --book "A Text Book of Astrology"
```

**Peek at rules (diagnostic):**
```bash
python3 scripts/peek_rules.py \
  --mongo-url "$MONGO_URL" \
  --db-name EverydayHoroscope \
  --limit 10
```

---

## 9. Open Deliverables — Prioritised

### Immediate (next session)

| # | Task | Detail |
|---|---|---|
| 1 | **Insert Ch 15 Option B rules** | Run `ingest_chapter15.py` without `--dry-run`. Inserts 622 rules. batch_id: `a-text-book-ch15-v2-20260414` |
| 2 | **Re-ingest Book 1 (A Text Book of Astrology)** | With all fixes applied (max_tokens 1800, unique IDs, truncation detection). Delete old batch from `import_batches` first. Expect ~50-60% auto_approved (vs 20% before). |
| 3 | **Validate Ch 15 Option B batch** | Run `validate_rules.py` against `a-text-book-ch15-v2-*` batch after insert. |

### Phase 1 — Remaining Books (in priority order)

| Priority | Book | Why this order |
|---|---|---|
| 🥇 1 | **BPHS** | Most authoritative Vedic text. Contains Layer 2 (Dasha results). Unlocks timed event prediction. |
| 🥈 2 | **Lal Kitab** | 29 chapters, planet×house format matches Ch 15 spine perfectly. Remedies = differentiated product. |
| 🥉 3 | **Phaladeepika** | Classical text, Mahadasha results. Adds Layer 2 alongside BPHS. |
| 4 | **Review Book 1 OCR (pending_human_review)** | 202 rules need quick expert check. Most will resolve with max_tokens fix on re-ingest. |

### Architecture / Schema (medium term)

| # | Task | Detail |
|---|---|---|
| 5 | **Add `dasha_planet_from_house` condition type** | Layer 2 condition schema. Extract from BPHS Dasha chapters. `{type: dasha_planet_from_house, dasha_planet: Sun, natal_house: 1}` |
| 6 | **Build cross-reference query** | For a given (planet, house, sign), return rules from ALL books. Show source, confidence, agreement/disagreement. This is the cross-book spine working. |
| 7 | **Case study validation bench** | Use known charts (JFK, Gandhi, Vivekananda) in the books as accuracy test. Run their natal conditions through extracted rules. Rules that correctly predict known outcomes → promote to HIGH confidence. |
| 8 | **Admin UI — Library filter by tag** | Filter `interpretation_rules` by `tags` field in `/admin/library`. Tags: `verbatim`, `planet_in_house`, `sign_variant`, `special_state`, `chapter15`. |

### Codex Commission Briefs (to prepare)

| # | Brief topic | Output |
|---|---|---|
| 9 | BPHS Planet×House rules (all 108) | JSON: `planet_in_house` rules, BPHS source, all 9 planets × 12 houses |
| 10 | BPHS Mahadasha results (all 9 planets × 12 natal houses) | JSON: `dasha_planet_from_house` rules — this is Layer 2 |
| 11 | Panch Mahapurusha Yogas from BPHS | JSON: 5 named yogas with formation conditions + results |
| 12 | Lal Kitab planet×house remedies | JSON: remedies array per (planet, house) — directly into `interpretation.remedies` |

---

## 10. What NOT to Do in the Next Session

- **Do not delete Phase 1 OCR rules from MongoDB** — they are kept alongside Ch 15 Option B for comparison. The `source.batch_id` field isolates them.
- **Do not re-run `ingest_chapter15.py` twice** — the batch_id guard will catch it, but avoid the confusion. Check `import_batches` first.
- **Do not change `BATCH_ID` in `ingest_chapter15.py`** unless intentionally re-ingesting a fresh version. The current batch_id is `a-text-book-ch15-v2-{date}` — the `v2` signals Option B.
- **Do not use the GitHub browser editor** — always commit via terminal or Claude Code (per CLAUDE.md).
- **⚠️ CRITICAL — Do NOT bulk-approve any rules in the Admin Console.** The live web app at everydayhoroscope.in is fully isolated from all Knowledge Engine rules by a hardcoded filter in `backend/knowledge_engine.py` line 47: `APPROVED_RULE_FILTER = {"active": True, "approval_status": "approved"}`. Every ingested rule carries `approval_status: "pending_review"` or `"flagged"` — the live app sees none of them and falls back to its existing GPT-direct narrative. The only action that breaks this isolation is manually promoting a rule to `approval_status: "approved"` via the Admin Console. **Do not do this until the full sequence is complete: all Phase 1 books ingested → case study validation bench run → cross-reference layer verified → co-founder sign-off.**

---

## 11. MongoDB Rule Count Reference

After Ch 15 Option B is inserted, expected state:

| Source | Condition type | Count | Status |
|---|---|---|---|
| Phase 1 OCR (8 books) | mixed | ~946 | pending_review / flagged |
| Ch 15 Option B — base | planet_in_house | 103 | pending_review |
| Ch 15 Option B — signs | planet_in_house_in_sign | 346 | pending_review |
| Ch 15 Option B — states | planet_in_house_special | 173 | pending_review |
| **Total** | | **~1,568** | |

---

## 12. Agreed Strategic Principles

Recorded here so they don't need re-negotiation:

1. **Source fidelity over speed** — every rule traceable to book + chapter. No synthesised rules.
2. **OCR pipeline = discovery layer** — identifies what a book covers; 58% flag rate is acceptable as a triage step, not a production input.
3. **Codex-direct = production layer** — clean, structured, near-zero flag rate for known classical texts.
4. **Chapter 15 verbatim = baseline** — store raw text first, commission paraphrase after reviewing pipeline behaviour.
5. **No production ingest until case study validation** — rules that cannot predict JFK/Gandhi/Vivekananda correctly don't go live.
6. **BPHS first among equals** — most authoritative text; BPHS-approved rules set the confidence floor for cross-book comparison.
7. **Option B cross-book spine** — the `planet_in_house_in_sign` condition type is the unifying key. Every subsequent book's planet×house rules must use the same condition schema to enable cross-reference.
8. **Live app isolation is non-negotiable** — the live web app (everydayhoroscope.in) must function identically to how it did before Knowledge Engine work began, until the full library is built, case studies pass, and co-founders explicitly sign off on going live. The `approval_status: "approved"` gate in `knowledge_engine.py` is the enforcement mechanism. It must not be bypassed.

---

*Document owner: Prateek Malhotra + EverydayHoroscope AI Co-Founder*
*Repo: github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration*
*Next session should start by reading: KNOWLEDGE_ENGINE_HANDOVER.md + KNOWLEDGE_ENGINE_STRATEGY.md + CLAUDE.md*
