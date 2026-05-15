# Codex Commission -- Remedies Engine
> Issued: 2026-05-11 | Priority: Next after KP migration
> Status: OPEN -- formal commission

---

## ⚠️ ARCHITECTURE RULE -- MANDATORY (read before writing any code)

Do NOT add any dasha, chart, or astronomical computation to `remedies_engine.py`.
All live chart data MUST be sourced by calling:
```python
from vedic_calculator import calculate_vimshottari_dasha, get_current_dasha
```
Any deviation will be rejected and require a re-commission.

---

## What To Build

A standalone backend module (`backend/remedies_engine.py`) that accepts a **context object**
and returns a **curated, cross-tradition remedy pack** (3-7 items) from the app's existing
remedy data collections. This engine is called by ALL Temple App modules -- not KP-only.

---

## Canonical Spec Files (Read All Before Writing)

```
/Users/apple/DailyHoroscope-Migration/.claude/REMEDIES_ENGINE_SPEC_V1.md     ← Full functional spec
/Users/apple/DailyHoroscope-Migration/.claude/CODEX_GREEN_LIGHT_MEMO.md      ← Scope corrections + architecture checks
/Users/apple/Documents/New project/KRISHNA_ORACLE_REMEDY_ENGINE_SCHEMA.md    ← KP-side schema + 4 remedy families + seed packs
/Users/apple/Documents/New project/KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json  ← 36 KP remedy records (ingest-ready)
```

---

## Data Landscape -- Existing Collections (Do NOT Duplicate)

The engine queries EXISTING MongoDB collections. Do NOT create a new `remedies_rules` collection.

| Collection | science_ids present | Content |
|---|---|---|
| `interpretation_rules` | `jyotish_remedies_dhana`, `jyotish_remedies_gemstones`, `jyotish_remedies_crystals`, `jyotish_remedies_chakra`, `jyotish_remedies_mantras` | 5 paid remedy module datasets |
| `knowledge_rules` | `jyotish_lk_remedies` | 666 Lal Kitab remedy records |
| `krishna_prashnavali_remedies` | `krishna_prashnavali_remedies` | 36 KP records -- **not yet ingested; ingest script needed** |

Existing router to be aware of (do NOT conflict): `backend/remedies_router.py` at prefix `/api/remedies`
The new engine will add `POST /api/remedies/suggest` to this same router.

---

## Unified 3-Field Taxonomy (Gap 1 Decision)

Every remedy record queryable by the engine must carry three classification fields.
These map to existing records via the suggest logic -- Codex does NOT need to re-tag existing data.

```
tradition     →  source science         : jyotish | lal_kitab | crystal | chakra | krishna_bhakti | numerology | feng_shui | lo_shu | zibu
category      →  mechanism class        : mantra | puja | ritual | gemstone | yantra | dana | breathwork | dietary | spatial | symbol | color | crystal | behavioral
action_type   →  delivery format        : daily | weekly | one_time | ongoing | behavioral | environmental
```

Compound display label for UI (derived, not stored): `{Tradition}_{Category}_{ActionType}`
Example: `LalKitab_Ritual_OneSaturday` | `Jyotish_Dana_Weekly` | `Krishna_Mantra_108Reps`

---

## Schema -- Suggest Input Context

```json
{
  "trigger": "birth_chart | dasha | daily_horoscope | numerology | krishna_oracle | tarot | strategist | lk_diagnostics",
  "planet": "Saturn",
  "house": 7,
  "affliction": "debilitated | combust | aspected_by_malefic | empty_vessel | rahu_collision",
  "dasha_planet": "Saturn",
  "antardasha_planet": "Rahu",
  "life_domain": "marriage | career | health | wealth | spiritual | family | children | enemies | mental",
  "nakshatra": "Pushya",
  "oracle_answer_id": "optional -- kp slot reference",
  "verdict": "optional -- YES | WAIT | NO | PRAY | WARNING | PATIENCE | SUCCESS | SURRENDER",
  "gender": "male | female | neutral",
  "intensity": "mild | moderate | severe",
  "remedy_type_filter": "optional -- ritual | behavioral | both (default: both)"
}
```

---

## Schema -- Remedy Pack Output

```json
{
  "remedy_pack_id": "uuid",
  "trigger": "birth_chart",
  "context_summary": "Saturn debilitated in 7th house -- marriage domain",
  "remedies": [
    {
      "remedy_id": "string",
      "tradition": "lal_kitab",
      "category": "ritual",
      "action_type": "weekly",
      "remedy_type": "ritual",
      "title": "Feed black dogs on Saturday",
      "description": "Full instruction",
      "duration": "11 Saturdays",
      "ease": "easy | medium | advanced",
      "confidence": 0.87,
      "source_collection": "knowledge_rules",
      "science_id": "jyotish_lk_remedies"
    },
    {
      "remedy_id": "kp-001",
      "tradition": "krishna_bhakti",
      "category": "mantra",
      "action_type": "one_time",
      "remedy_type": "ritual",
      "title": "Recite final verse of Gita Ch.18 three times",
      "description": "...",
      "behavioral_remedy": "Contemplate the final assurance of Gita Chapter 18 before acting.",
      "duration": "Before beginning each task",
      "ease": "easy",
      "confidence": 0.95,
      "source_collection": "krishna_prashnavali_remedies",
      "science_id": "krishna_prashnavali_remedies"
    }
  ],
  "advisory_mode": "supportive | protective | calming | devotional",
  "generated_at": "ISO timestamp"
}
```

---

## Suggest Logic (Backend)

1. Parse context object
2. Map `trigger` + `planet` + `life_domain` + `intensity` to relevant collections and science_ids
3. Query each relevant collection with `approval_status: "approved"` filter
4. Score results by: condition match specificity × confidence × tradition diversity
5. Return top 5-7 remedies, max 2 per tradition (for variety)
6. Fallback: if fewer than 3 results, return universal planet remedies for that planet from `knowledge_rules`
7. If `remedy_type_filter` specified, filter before ranking

### Collection routing map (implement in engine):
```python
COLLECTION_MAP = {
    "dana":      ("interpretation_rules", "jyotish_remedies_dhana"),
    "gemstones": ("interpretation_rules", "jyotish_remedies_gemstones"),
    "crystals":  ("interpretation_rules", "jyotish_remedies_crystals"),
    "chakra":    ("interpretation_rules", "jyotish_remedies_chakra"),
    "mantras":   ("interpretation_rules", "jyotish_remedies_mantras"),
    "lk":        ("knowledge_rules",      "jyotish_lk_remedies"),
    "kp":        ("krishna_prashnavali_remedies", "krishna_prashnavali_remedies"),
}
```

---

## New Endpoints (add to existing `remedies_router.py`)

| Method | Route | Purpose |
|---|---|---|
| POST | `/api/remedies/suggest` | Main engine endpoint -- context in, remedy pack out |
| GET | `/api/remedies/rule/{remedy_id}?collection={name}` | Resolve single remedy by ID (used for `remedy_ref` lookups from KP) |
| GET | `/api/remedies/traditions` | List available traditions and record counts |

Router prefix already defined in `remedies_router.py`:
```python
router = APIRouter(prefix="/api/remedies", tags=["remedies"])
```
Register in `server.py` without prefix arg (existing convention).

---

## `behavioral_remedy` Support (Gap 2 -- Full-App Requirement)

The engine must support two remedy types:
- `remedy_type: "ritual"` -- prescribed spiritual/physical practice (mantra, puja, dana, gemstone)
- `remedy_type: "behavioral"` -- internal shift guidance (mindset, habit, speech restraint)

KP records already carry both (`ritual_remedy` + `behavioral_display_hint` in the ingest file).
The suggest output must surface both when present.
No module may hardcode mantras -- all prescriptions come via the engine.

---

## Phase 1 Delivery Scope (This Commission)

Codex delivers:
1. `POST /api/remedies/suggest` endpoint + suggest logic in `remedies_engine.py` (or inline in `remedies_router.py`)
2. `GET /api/remedies/rule/{remedy_id}` -- `remedy_ref` resolver
3. `GET /api/remedies/traditions` -- collection count summary
4. Ingest script for `krishna_prashnavali_remedies` collection (reads `KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json`)
5. "Remedies" tab added to `frontend/src/pages/BirthChartPage.jsx` (calls `/api/remedies/suggest` with chart context)

Codex does NOT run the ingest -- Temple Team runs it post-delivery.

**Phase 1 does NOT include:**
- KP runtime integration (remedy_ref resolution wired into KP answer display) -- Phase 2
- Feng Shui, Lo Shu Grid, Zibu ingestion -- Phase 2
- Admin Console Remedies tab -- Phase 2

---

## Frontend Integration Points (Phase 1: Birth Chart only)

```
frontend/src/pages/BirthChartPage.jsx  →  add "Remedies" tab
```

After chart is computed:
1. Identify top 3 afflicted planets from chart (lowest dignity)
2. For each: `POST /api/remedies/suggest` with `trigger: "birth_chart"`, planet, house, affliction, life_domain
3. Render collapsible "Remedies for You" section per planet

---

## Constraints (All Mandatory)

1. No chart/dasha recomputation in engine -- call `vedic_calculator.py` for all live data
2. `approval_status: "approved"` filter on all queries -- same gate as Knowledge Engine
3. All new pages lazy-loaded in App.js (no new page in Phase 1 -- only a tab added to BirthChartPage)
4. Router prefix defined INSIDE router file; `server.py` registers with no prefix arg
5. Temple App theme: `bg-background`, `text-foreground`, `text-gold`, `border-gold/20`
6. Straight quotes only in JSX (no smart/curly quotes)
7. Python 3.12, FastAPI, Motor async -- no blocking calls in async routes
8. Use `update_many` for all MongoDB writes
9. No hardcoded remedy content in Python -- all content from MongoDB

---

## KP Remedies -- Preservation Note

The 36 KP remedy records in `KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json` are temple-reviewed
and contain Sanskrit + English bilingual content. They must be ingested exactly as structured.
The KP v2 bundle (`KRISHNA_ORACLE_CONTENT_CANONICAL_V2_FOR_TEMPLE.json`) references these via
`remedy_ref` IDs. The `GET /api/remedies/rule/{remedy_id}` endpoint resolves these lookups.
