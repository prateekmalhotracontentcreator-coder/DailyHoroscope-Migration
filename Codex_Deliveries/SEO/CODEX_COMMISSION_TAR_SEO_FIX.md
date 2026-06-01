# Codex Commission: TAR-SEO-FIX -- Tarot SEO Generator Fix (v2)
> Thread: Tarot SEO | File: `backend/tarot_seo_data.py` (single file)
> Issued: 2026-06-02 (v2 -- first delivery replaced old boilerplate with new boilerplate; Cards L3 untouched)
> Scan script: `tests/echo_pace_seoc_tarot_scan.py` | Scan report: `SEO_20K/SEO_TRACKER.md`

---

## Commission Brief (5 lines)

First delivery partially worked but introduced new boilerplate in the same structural positions. Three issues remain: (1) **Spreads L2** -- old phrase `"page reads spread card layout"` gone but replaced by `"reading position carrying separate"` 100% and `"guide explains layout card"` 100% -- these are new shared structural sentences in the spread body; every spread page must have a structurally unique intro AND a unique positional bridge sentence -- use `_hash_index(slug, modulus=8)` to select from ≥8 distinct openers AND ≥8 distinct positional bridge phrases -- do not use any sentence frame shared across more than 2 of the 100 pages. (2) **Cards L3** -- `meta_title` still reads `"X Tarot Card - minor Meaning & Guide"` for all minor arcana -- the word `"minor"` must be replaced with the actual suit name (`"Wands"`, `"Cups"`, `"Swords"`, `"Pentacles"`) so each card title is unique; e.g. `"Ace of Wands Tarot Card -- Wands Suit Guide"`. (3) **Intentions L2+L3** -- `"actually draw reflect respond"` 100% and `"page compares three strong"` 100% are new shared phrases; AND meta_title `"Best Tarot Spreads for X -- Cards, Layouts & Guide"` still shares 75% Jaccard across all 20 pages -- use intention-category vocabulary in the title (e.g. `"Career Tarot Reading -- Spreads, Timing & Guidance"` not `"Best Tarot Spreads for Career"`).

---

## 1. SEO Pages -- Module Overview

| Page Type | URL Pattern | Total Pages | Content Fields Scanned |
|---|---|---|---|
| Spreads | `/tarot/spread/{slug}` | 100 | `purpose`, `how_to`, `when_to_use`, `positions[].meaning`, `sample_reading`, FAQ answers |
| Cards | `/tarot/card/{slug}` | 78 | `upright`, `reversed`, `love`, `career`, `health`, `imagery`, `meta_title` |
| Intentions | `/tarot/for/{slug}` | 20 | `intro`, `sample_walkthrough`, `caution_cards[].note`, FAQ answers, `meta_title` |
| **Total** | | **198** | |

---

## 2. Pages Impacted -- Rework Required

| Page Type | Pages Affected | v1 Issue | v2 Fix Required |
|---|---|---|---|
| Spreads | 100 / 100 | Old intro phrase replaced with new shared phrases: `"reading position carrying separate"` 100%, `"guide explains layout card"` 100% | ≥8 distinct openers + ≥8 distinct positional bridge phrases, hash-selected; no frame shared across >2 pages |
| Cards -- Minor Arcana | 56 / 78 | `meta_title` still `"X Tarot Card - minor Meaning & Guide"` -- suit word not inserted | Replace `"minor"` with actual suit name: `"Ace of Wands Tarot Card -- Wands Suit Guide"` |
| Intentions | 20 / 20 | New shared phrases: `"actually draw reflect respond"` 100%, `"page compares three strong"` 100%; meta_title template unchanged | Delete both phrases; use intention-category vocabulary in meta_title (not `"Best Tarot Spreads for X"`) |

**Phrases that MUST NOT appear on more than 1 page (from v1 re-scan -- delete entirely):**

*Spreads:*
- `"reading position carrying separate"` -- 100%
- `"guide explains layout card"` -- 100%
- `"card reading position carrying"` -- 100%

*Intentions:*
- `"actually draw reflect respond"` -- 100%
- `"page compares three strong"` -- 100%
- `"fit topic while live"` -- 100%

**L1 must NOT regress** -- all 3 page types currently pass L1 (Spreads 33.3%, Cards 34.8%, Intentions 11.7%). Any new boilerplate that raises L1 above 50% is a blocker.

---

## 3. Tests -- Required Before Integration

| Test | Layer | Tool | Pass Criterion | Run Command |
|---|---|---|---|---|
| TF-IDF Cosine | L1 | `tests/echo_pace_seoc_tarot_scan.py` | All 3 types **< 50%** (must not regress) | `python3 tests/echo_pace_seoc_tarot_scan.py` |
| N-gram Match | L2 | `tests/echo_pace_seoc_tarot_scan.py` | Spreads **0** violations · Intentions **0** violations | Same script |
| Jaccard Titles | L3 | `tests/echo_pace_seoc_tarot_scan.py` | Cards **< 60%** · Intentions **< 60%** | Same script |

---

## 4. Scan History

| Scan | Date | Page Type | L1 | L2 Violations | L3 Worst Jaccard | Verdict |
|---|---|---|---|---|---|---|
| Pre-fix | 2026-05-31 | Spreads | 32.9% ✅ | 6 at 87-100% | 70% | L2 FAIL |
| Pre-fix | 2026-05-31 | Cards | 34.8% ✅ | 0 | 75% | L3 FLAGGED |
| Pre-fix | 2026-05-31 | Intentions | 14.2% ✅ | 10 at 100% | 75% | L2+L3 FAIL |
| v1 re-scan | 2026-06-02 | Spreads | 33.3% ✅ | 10 at 100% (new phrases) | 70% | ❌ L2 still failing |
| v1 re-scan | 2026-06-02 | Cards | 34.8% ✅ | 0 | **75%** (unchanged) | ❌ L3 not fixed |
| v1 re-scan | 2026-06-02 | Intentions | 11.7% ✅ | 10 at 100% (new phrases) | 75% | ❌ L2+L3 still failing |
| v2 target | -- | All | < 50% | 0 | < 60% | ✅ |
