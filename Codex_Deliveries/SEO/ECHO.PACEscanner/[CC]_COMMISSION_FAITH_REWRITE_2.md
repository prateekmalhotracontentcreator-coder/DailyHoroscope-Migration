---
title: "[CC] Commission -- Faith Rewrite 2"
version: v1.0
date: 2026-06-12
status: ISSUED
authored_by: CC (Claude Code / ECHO.PaceScanner)
github_issue: https://github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration/issues/1
full_brief: Codex_Deliveries/Faith_Hubs/CODEX_COMMISSION_FAITH_REWRITE_2.md
delivery_branch: codex/faith/rewrite-2
baseline: main at 86e53af
---

# [CC] Commission -- Faith Rewrite 2

> **Full brief:** [`Codex_Deliveries/Faith_Hubs/CODEX_COMMISSION_FAITH_REWRITE_2.md`](../Faith_Hubs/CODEX_COMMISSION_FAITH_REWRITE_2.md)
>
> This file is the CC index entry. Read the full brief above before starting work.

---

## Summary

The Faith Hub (GITA 10,500 pages / BIBLE 6,000 pages / TRANSIT 156 pages) passes L2 after Pass 5 (2026-06-07) but still fails L1 and L3. This commission addresses the remaining structural failures using three strategies directed by Temple Team (2026-06-12):

1. Mix AI-seeded unique content + generator redesign
2. Timing SEO upload strategy -- non-similar page batches
3. Expand verse range -- Bible pool has only 174 unique verses for 6,000 pages (min 12 per bucket)

---

## Pass 5 Baseline (what's already done -- do not redo)

| Type | L1 | L2 | L3 |
|---|---|---|---|
| GITA | 91.25% ❌ | PASS ✅ | 81.82% ❌ |
| BIBLE | 78.35% ❌ | PASS ✅ | 50.00% ✅ |
| TRANSIT | 84.60% ❌ | PASS ✅ | 66.67% ❌ |
| DAILY | AI seeder path | PASS ✅ | PASS ✅ |

---

## Six Deliverables (see full brief for specs)

| # | Deliverable | File | Priority |
|---|---|---|---|
| 1 | Expand Bible verse pool: ≥ 30 unique verses per source bucket (currently min 12; worst verse shared by 163 pages) | `backend/assets/faith/` (Bible verse JSON) | HIGH -- single biggest L1 lever for Bible |
| 2 | `symbolic_clause` fix in `_bible_hermeneutical()` -- 8 distinct `symbolic_forms` instead of one shared variable | `backend/faith_bible_data.py` | HIGH |
| 3 | Replace situation-constant full phrases with single tokens in `_gita_hook()` + `_gita_application()`; 4-variant `_how_to_apply_steps()` | `backend/faith_gita_data.py` | HIGH |
| 4 | `_sign_modifier()` -- inject fire/earth/air/water vocabulary to differentiate the 12 sign pages per planet | `backend/faith_seo_data.py` | MEDIUM |
| 5 | AI seeder Phase 2 -- extend existing seeder to Transit (156 pages, ~$0.05) | `backend/scripts/seed_faith_daily_haiku.py` | MEDIUM |
| 6 | `generate_upload_batches.py` -- NEW: batch planner for GITA/BIBLE/TRANSIT ensuring non-similar pages per batch | `backend/scripts/generate_upload_batches.py` | MEDIUM |

---

## Acceptance Targets

| Type | L1 target | L3 target | L2 (must not regress) |
|---|---|---|---|
| GITA | < 85% | < 65% | PASS |
| BIBLE | < 72% | PASS | PASS |
| TRANSIT | < 78% | < 62% | PASS |

Bible verse gate: max 30 pages per unique verse (down from current 163).

---

## Branch

`codex/faith/rewrite-2` -- branch from `main` at `86e53af` only.

---

*[CC]_COMMISSION_FAITH_REWRITE_2 · Echo.PaceScanner · CC Authored · v1.0 · 2026-06-12*
