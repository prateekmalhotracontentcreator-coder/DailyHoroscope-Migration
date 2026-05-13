# SESSION START — Read This First
> Max 30 lines. Rewrite at END of every session. Last updated: 2026-05-13

## Current State
- **Active task:** KP remedy display — bundle default + Remedies Engine fallback (NOT YET DONE — backend + frontend fix required)
- **Last completed (Account 2, 2026-05-13):** KP bundle-native revert + on-page SEO content for ALL 13 modules — 4 commits pushed ✅
- **Last completed (Account 1, 2026-05-12 night):** Strategist 22-record approval + SEO Sprints D/E/F — 4 commits pushed ✅

## DB State (horoscope_db — as of 2026-05-11)
| Science | Approved | PHR | Flagged | Notes |
|---|---|---|---|---|
| mundane_jyotish | **326** | 2 (intentional holds) | 0 | 7 tagged `cofounders_review_required=True` |
| jyotish (BPHS Vol 1) | ~628 auto_approved | ~352 PHR | ~95 flagged | NLM triage in progress |
| jyotish (BPHS Vol 2) | 1,092 auto_approved | ~582 PHR | 190 flagged | Pending |
| jyotish (TBA Ch 15+16) | 589 auto_approved | ~639 PHR | 302 flagged | Pending |
| jyotish (Lal Kitab Ch 19–28) | ~275 auto_approved | ~149 PHR | ~10 flagged | Pending |
| jyotish_remedies_mantras | 45 auto_approved | 50 PHR | 0 | Pending |
| knowledge_rules (LK remedies) | **666** records live | — | 5 split_required | Used by LK Standalone + Strategist |
| krishna_prashnavali_remedies | **36 approved** | — | — | Ingested + approved 2026-05-11 |

## Immediate Next Steps (priority order)
1. **KP remedy fix** — bundle as default, Remedies Engine as fallback: reinstate conditional `_resolve_kp_remedy_doc` in `scriptural_oracle_router.py` (only when bundle fields empty + `remedy_ref` exists)
2. **NLM pass** — BPHS Ch 12–23 contradiction pairs (13 pairs) + Ch 15/19 PHR batch
3. **Punya Rewards** — fully built, no App.js route; user reviewing before Temple Team migration
4. **Lagna Kundali tier decision** — currently Premium; user said "still needs a decision"

## DO NOT
- Use `EverydayHoroscope` DB (retired — all 3,796 rules deprecated 25 Apr 2026)
- Approve PHR rules without NLM verification or confirmed false-flag pattern
- Strip analyst-derived content — flag for co-founder review, keep intact
- Run `--apply` without dry-run first
- Use `validate_rules.py` for mundane batches — use `validate_mundane_rules.py`

## Session Start Protocol (READ ONLY THESE 3 FILES — ~2,900 tokens total)
1. This file — SESSION_START.md (active state)
2. .claude/BOOK_STATUS.md (book-level progress)
3. .claude/ingest/<ACTIVE_BOOK>_INGEST.md (detail for current task only)

## Key File Paths
- Book detail: `.claude/ingest/<BOOK>_INGEST.md`
- NLM tracker: `.claude/nlm/BPHS_VOL1_NLM.md`
- Scripts index: `backend/scripts/SCRIPTS_INDEX.md`
- Mundane validator: `backend/scripts/validate_mundane_rules.py`
- Ingest notes (raw log — do NOT read at session start): `backend/scripts/INGEST_NOTES.md`
