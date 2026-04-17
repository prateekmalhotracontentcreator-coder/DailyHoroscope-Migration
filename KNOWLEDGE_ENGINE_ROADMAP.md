# Knowledge Engine — Ingest Roadmap
Last updated: 17 April 2026 — 1,040 rules in DB; Ch 48 + Ch 52 + Ch 53 complete (Ch 53 includes 4-rule Venus Antardasha supplement patch)

---

## Current State

| Source | Chapters ingested | Rules in DB | Status |
|---|---|---|---|
| BPHS Vol 1 | Ch 12-24 (Houses + Bhava Lords) | 736 | Validated |
| BPHS Vol 2 | Ch 47 (Mahadasha by Planet) | 93 | Validated |
| BPHS Vol 2 | Ch 48 (Dasha of House Lords) | 46 | Validated |
| BPHS Vol 2 | Ch 52 (Antardasha in Sun MD) | 93 | Validated |
| BPHS Vol 2 | Ch 53 (Antardasha in Moon MD) | 72 (68+4 patch) | Validated; patch pending human review |
| A Text Book of Astrology | None | 0 | Pending |
| **Total** | | **968+** | |

**Approval gate:** All 829 rules sit at `auto_approved` or `pending_human_review`.
No rules reach live users until co-founder promotes to `approved`.
Decision: promote only after full multi-book ingest is complete.

---

## Rule Estimate by Source

| Source | Chapters targeted | Est. rules |
|---|---|---|
| BPHS Vol 1 remaining | Ch 24, 34, 36, 39, 41 | ~350 |
| BPHS Vol 2 Dasha layer | Ch 47, 48, 52-60 | ~900 |
| A Text Book of Astrology | Ch 15, 16 | ~150 |
| **Grand total (all sources)** | | **~1,750** |

---

## Tier 1 — Ingest Next (Core Prediction Engine)

### BPHS Vol 1 — Ch 24: Effects of Bhava Lords ✅ DONE
- **Rules ingested:** 376 · auto_approved: 71% · flagged: 9% · contradictions: 0
- **batch_id:** bphs-ch24-v2-20260416

### BPHS Vol 2 — Ch 48: Dasas of Lords of Various Houses ✅ DONE
- **Rules ingested:** 46 · auto_approved: 74% · flagged: 2% · contradictions: 5 pairs
- **batch_id:** bphs-ch48-dasha-20260416
- **Condition type:** `dasha_of_house_lord` with `condition.house` 1-12

### BPHS Vol 2 — Ch 47: Effects of Dasas (Mahadasha by Planet) ✅ DONE
- **Rules ingested:** 93 · auto_approved: 82% · flagged: 4% · contradictions: 0
- **batch_id:** bphs-ch47-dasha-20260416
- **Parser fixes shipped:** colon separator, zero-space period, transition planet detection

---

## Tier 2 — Precision Layer

### BPHS Vol 2 — Ch 52-60: Antardasha Effects (9 chapters)
- **What:** Sub-period effects for each Mahadasha × Antardasha combination
- **Why Tier 2:** Precision timing layer — high rule count but more granular than Tier 1
- **Chapters:**

| Ch | Dasha lord | Antardasha planets covered | Status |
|---|---|---|---|
| 52 | Sun | Sun/Moon/Mars/Rahu/Jupiter/Saturn/Mercury/Ketu/Venus | ✅ 93 rules, 83% approved |
| 53 | Moon | Moon/Mars/Rahu/Jupiter/Saturn/Mercury/Ketu/Venus/Sun | ✅ 68 rules (76% approved) + 4 patch rules (Venus Antardasha supplement, `pending_human_review`) |
| 54 | Mars | Mars/Rahu/Jupiter/Saturn/Mercury/Ketu/Venus/Sun/Moon |
| 55 | Rahu | Rahu/Jupiter/Saturn/Mercury/Ketu/Venus/Sun/Moon/Mars |
| 56 | Jupiter | Jupiter/Saturn/Mercury/Ketu/Venus/Sun/Moon/Mars/Rahu |
| 57 | Saturn | Saturn/Mercury/Ketu/Venus/Sun/Moon/Mars/Rahu/Jupiter |
| 58 | Mercury | Mercury/Ketu/Venus/Sun/Moon/Mars/Rahu/Jupiter/Saturn |
| 59 | Ketu | Ketu/Venus/Sun/Moon/Mars/Rahu/Jupiter/Saturn/Mercury |
| 60 | Venus | Venus/Sun/Moon/Mars/Rahu/Jupiter/Saturn/Mercury/Ketu |

- **Script:** Same `ingest_bphs_dasha_v1.py` with `--dasha-lord` arg
- **Est. rules:** ~80 per chapter × 9 = ~720 rules total
- **RTF status:** Needs conversion (9 files)

### BPHS Vol 1 — Ch 34: Yoga Karakas
- **What:** Planet effects per ascendant — all 12 Lagnas. Which planet becomes a Yogakaraka for which ascendant.
- **Condition type:** `yoga_karaka` (planet + ascendant combination)
- **Est. rules:** ~60-80
- **RTF status:** Needs conversion

### BPHS Vol 1 — Ch 36: Many Other Yogas
- **What:** Gajakesari, Amala, Parvatha, Chamara, Sankha, Bheri and 15+ named yogas
- **Condition type:** `yoga_combination`
- **Est. rules:** ~60-80
- **RTF status:** Needs conversion

### A Text Book of Astrology — Ch 15: Planets in Different Houses
- **What:** All 9 planets × 12 houses = 108 combinations with prediction rules (p.171-232, ~62 pages)
- **Why here:** Cross-book validation source for BPHS house rules — same content, different author's lens
- **Condition type:** `planet_occupation` (same as existing house chapters)
- **Script:** Extend `ingest_bphs_houses_v2.py` or create `ingest_textbook_v1.py` (different source metadata)
- **Est. rules:** ~100-150
- **RTF status:** Needs conversion

### A Text Book of Astrology — Ch 16: Planetary Combinations / Yogas
- **What:** Important Yogas, Sun/Moon Yogas, Auspicious-Inauspicious Yogas, Panch Maha Purusha Yogas
- **Est. rules:** ~40-60
- **RTF status:** Needs conversion

### BPHS Vol 2 — Ch 75: Panchamahapurusha Yogas
- **What:** 5 named yogas (Ruchaka/Bhadra/Hamsa/Malavya/Sasa) — very clean if-then structure
- **Why here:** High precision, clean rules, good cross-validation with A Text Book Ch 16
- **Est. rules:** ~20-30
- **RTF status:** Needs conversion

---

## Tier 3 — Valuable but Defer

| Ch | Source | What | Est. rules | Note |
|---|---|---|---|---|
| Ch 39 | BPHS Vol 1 | Raja Yogas | ~40 | Kingly combinations — valuable for premium reports |
| Ch 41 | BPHS Vol 1 | Yogas for Wealth | ~50 | High user interest |
| Ch 70 | BPHS Vol 2 | Effects of Ashtakavarga | ~60 | Timing precision layer |
| Ch 84 | BPHS Vol 2 | Remedial measures per planet | ~80 | Premium report content |

---

## Script Development Required

### Work needed before Tier 1 ingest can begin

| Script | Purpose | Effort |
|---|---|---|
| Extend `ingest_bphs_houses_v2.py` | Remove Ch 12-23 range restriction; add Ch 24 to CHAPTER_NAMES; support `--house 0` or no-house mode | Small |
| New `ingest_bphs_dasha_v1.py` | Handle Ch 47, 48, 52-60. New condition types: `dasha_planet`, `dasha_of_house_lord`. Args: `--chapter`, `--dasha-lord` | Medium |
| Extend `validate_rules.py` | Structural check to accommodate new condition types | Small |

### New condition types to define

| Type | Used by | Condition fields |
|---|---|---|
| `dasha_planet` | Ch 47 | `planet` (Mahadasha lord) + `dignity` / `placement` |
| `dasha_of_house_lord` | Ch 48 | `house` (whose lord is running Dasha) + `placement` |
| `antardasha` | Ch 52-60 | `dasha_lord` + `antardasha_lord` + `dignity` / `placement` |
| `yoga_karaka` | Ch 34 | `planet` + `ascendant_sign` |
| `yoga_combination` | Ch 36, 39, 75 | `planets_involved` + `yoga_name` |

---

## RTF Conversion Queue

Files needed before ingest (in priority order):

| Priority | Source | Chapter | Notes |
|---|---|---|---|
| 1 | BPHS Vol 1 | Ch 24 | Bhava Lords — extend existing script |
| 2 | BPHS Vol 2 | Ch 48 | Dasha of house lords |
| 3 | BPHS Vol 2 | Ch 52-60 | 9 Antardasha chapters (bulk conversion) |
| 4 | BPHS Vol 1 | Ch 34, 36 | Yoga chapters |
| 5 | A Text Book of Astrology | Ch 15, 16 | Different book — needs source metadata update |
| 6 | BPHS Vol 1 | Ch 39, 41 | Tier 3 yogas |
| 7 | BPHS Vol 2 | Ch 70, 75, 84 | Tier 3 |

**Ch 47 is already converted** (`BPHS Ch 47 Vol 2.rtf`) — waiting on script only.

---

## Immediate Next Steps (next session)

1. Convert Ch 48 RTF → ingest with `ingest_bphs_dasha_v1.py --chapter 48` → validate
2. Convert Ch 52-60 RTFs (9 Antardasha chapters) → bulk ingest → validate
3. Convert A Text Book of Astrology Ch 15 RTF → ingest → validate (cross-validation baseline)

---

## Approval Milestone

**Target before co-founder review:**
- BPHS Vol 1 complete (Ch 12-24) ✅ Done — 736 rules
- BPHS Vol 2 Tier 1 complete (Ch 47-48) — Ch 47 ✅ done (93 rules), Ch 48 pending
- A Text Book Ch 15 ingested (cross-validation baseline)

Estimated rules at that milestone: **~950 rules**
Current: **829 rules**
