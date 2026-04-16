# Knowledge Engine — Ingest Roadmap
Last updated: 16 April 2026

---

## Current State

| Source | Chapters ingested | Rules in DB | Status |
|---|---|---|---|
| BPHS Vol 1 | Ch 12-23 (Houses 1-12) | 360 | Validated |
| BPHS Vol 2 | None | 0 | Pending |
| A Text Book of Astrology | None | 0 | Pending |

**Approval gate:** All 360 rules sit at `auto_approved` or `pending_human_review`.
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

### BPHS Vol 1 — Ch 24: Effects of Bhava Lords
- **What:** 12 house lords × 12 placements = 144 lord×house combinations
- **Why Tier 1:** Direct complement to Ch 12-23. Together these two layers form the complete house-based prediction engine.
- **Script:** Extend existing `ingest_bphs_houses_v2.py` (remove chapter 12-23 range restriction, add Ch 24 to CHAPTER_NAMES)
- **House arg:** N/A for lord chapters — needs `condition.type = lord_placement` (already a valid sub_type)
- **Est. rules:** ~144
- **RTF status:** Needs conversion from Vol 1 book

### BPHS Vol 2 — Ch 48: Dasas of Lords of Various Houses
- **What:** Effects when you run the Dasha of the lord of each house (Ascendant lord Dasha, 2nd lord Dasha ... 12th lord Dasha)
- **Why Tier 1:** Highest-value Dasha chapter for the prediction engine — directly ties houses to timing
- **Condition type needed:** `dasha_of_house_lord` (new type — lord of house N is running Dasha)
- **Script:** New `ingest_bphs_dasha_v1.py` required
- **Est. rules:** ~100-120
- **RTF status:** Needs conversion

### BPHS Vol 2 — Ch 47: Effects of Dasas (Mahadasha by Planet)
- **What:** Per-planet Mahadasha effects based on dignity and placement (already have RTF — `BPHS Ch 47 Vol 2.rtf`)
- **Why Tier 1:** Layer 2 timing engine — when is a planet's period active and what does it bring
- **Condition type needed:** `dasha_planet` (which planet's Mahadasha is running + its dignity/placement)
- **Script:** Same new `ingest_bphs_dasha_v1.py`
- **Est. rules:** ~70-90
- **RTF status:** ✅ Ready (`BPHS Ch 47 Vol 2.rtf`)
- **Parser note:** Sloka `34-39:` uses colon separator — add `:` to sloka regex before ingesting

---

## Tier 2 — Precision Layer

### BPHS Vol 2 — Ch 52-60: Antardasha Effects (9 chapters)
- **What:** Sub-period effects for each Mahadasha × Antardasha combination (9 planet pairs per chapter × 9 chapters)
- **Why Tier 2:** Precision timing layer — high rule count but more granular than Tier 1
- **Chapters:**

| Ch | Dasha lord | Antardasha planets covered |
|---|---|---|
| 52 | Sun | Sun/Moon/Mars/Rahu/Jupiter/Saturn/Mercury/Ketu/Venus |
| 53 | Moon | Moon/Mars/Rahu/Jupiter/Saturn/Mercury/Ketu/Venus/Sun |
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

## Immediate Next Steps (this session)

1. Add `:` to sloka regex separator in `ingest_bphs_houses_v2.py` (needed for Ch 47 sloka 34-39)
2. Build `ingest_bphs_dasha_v1.py` for Ch 47 / 48 / 52-60
3. Ingest and validate Ch 47 (RTF ready)
4. Convert Ch 24 RTF → ingest → validate
5. Convert Ch 48 RTF → ingest → validate

---

## Approval Milestone

**Target before co-founder review:**
- BPHS Vol 1 complete (Ch 12-24) ✅ Ch 12-23 done, Ch 24 pending
- BPHS Vol 2 Tier 1 complete (Ch 47-48)
- A Text Book Ch 15 ingested (cross-validation baseline)

Estimated rules at that milestone: **~750 rules**
Current: 360 rules
