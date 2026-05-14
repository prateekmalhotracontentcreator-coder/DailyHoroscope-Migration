# Remedies Engine — Full Specification V1
> EverydayHoroscope / Temple App | 25 April 2026
> Status: Draft — for review and Codex module input before commission is opened

---

## 1. Architecture Decision: Standalone Module ✅

**The Remedies Engine must be a standalone module, not embedded within Krishna Prashanavali.**

Rationale:
- It serves ALL Temple App modules: Krishna Prashanavali, Birth Chart, Horoscopes, Dasha reports, Numerology
- Knowledge resources span multiple traditions (Lal Kitab, Crystal Therapy, Feng Shui, Zibu Symbols) that have no dependency on the Prashanavali oracle flow
- A standalone engine can be called by any module via a single API contract — `POST /api/remedies/suggest`
- Krishna Prashanavali includes remedies as part of its answer pack, but draws from this central engine rather than maintaining its own remedy logic

---

## 2. What the Remedies Engine Does

Given a **context object** describing the native's situation (planetary afflictions, active dasha, oracle answer, life domain), the engine returns a **curated remedy pack** of 3–7 remedies drawn from multiple traditions, ranked by relevance and confidence.

```
Input context  →  Remedies Engine  →  Remedy Pack (3-7 items)
```

### Input Context (any combination of):
```json
{
  "trigger": "krishna_oracle | birth_chart | dasha | daily_horoscope | numerology",
  "planet": "Saturn",
  "house": 7,
  "affliction": "debilitated | combust | aspected_by_malefic",
  "dasha_planet": "Saturn",
  "antardasha_planet": "Rahu",
  "life_domain": "marriage | career | health | wealth | spiritual | family",
  "nakshatra": "Pushya",
  "oracle_answer_id": "optional — links to KP answer for context",
  "gender": "male | female | neutral",
  "intensity": "mild | moderate | severe"
}
```

### Output Remedy Pack:
```json
{
  "remedy_pack_id": "uuid",
  "context_summary": "Saturn debilitated in 7th house — marriage domain",
  "remedies": [
    {
      "remedy_id": "R-LK-SAT-001",
      "tradition": "lal_kitab",
      "type": "ritual",
      "title": "Feed black dogs on Saturday",
      "description": "Full instruction text",
      "duration": "11 Saturdays",
      "ease": "easy | medium | advanced",
      "confidence": 0.87,
      "source": "Lal Kitab",
      "tags": ["saturn", "marriage", "weekly_ritual"]
    },
    {
      "remedy_id": "R-CRYS-SAT-003",
      "tradition": "crystal_therapy",
      "type": "gemstone",
      "title": "Wear Blue Sapphire (Neelam)",
      "description": "...",
      "precaution": "Test for 3 days before wearing permanently",
      "ease": "medium",
      "confidence": 0.75,
      "source": "Crystal Therapy"
    },
    ...
  ],
  "generated_at": "ISO timestamp"
}
```

---

## 3. Knowledge Resources

### 3A. Lal Kitab
- **Nature**: Predictive Urdu astrology text, unique remedy system
- **Remedy types**: Ritual-based (feeding animals, giving donations, wearing specific metals)
- **Strength**: Very practical, household-level remedies
- **Ingest status**: OCR batches exist but high rejection rate — needs clean RTF re-ingest
- **Priority**: P1 — most unique remedy content not available elsewhere

### 3B. Crystal Therapy
- **Nature**: Gemstone and crystal healing mapped to planets and chakras
- **Remedy types**: Wearing gemstones, placing crystals, meditation with crystals
- **Strength**: Well-documented, widely practiced
- **Index available**: `Crystal Healing_Index.pdf` in Book Wise TOC folder
- **Ingest status**: Not yet ingested
- **Priority**: P1

### 3C. Feng Shui
- **Nature**: Chinese spatial arrangement system mapped to life domains (wealth, relationships, health)
- **Remedy types**: Placement of objects, colors, directions, water features
- **Strength**: Highly actionable, home/office specific
- **Ingest status**: Not yet ingested
- **Priority**: P2

### 3D. Lo Shu Grid
- **Nature**: 3×3 numerological grid derived from DOB, maps missing numbers to life challenges and remedies
- **Remedy types**: Color therapy, number-based rituals, directional remedies
- **Strength**: Directly computable from birth date — can be auto-triggered
- **Ingest status**: Not yet ingested
- **Priority**: P2

### 3E. Zibu Symbols
- **Nature**: Angelic/spiritual symbols used for intention-setting and energy work
- **Remedy types**: Drawing/meditating on symbols, placing in home
- **Strength**: Spiritual/meditative — unique differentiator
- **Ingest status**: Not yet ingested
- **Priority**: P3

### 3F. Krishna Prashanavali Resources
- **Nature**: Remedies specific to the 108 oracle answers — puja, mantra, charity
- **Remedy types**: Temple visits, mantras, specific pujas, charitable acts
- **Strength**: Directly tied to oracle readings — highest contextual relevance for KP module
- **Ingest status**: Partially defined in Krishna Oracle spec
- **Priority**: P1 for KP module integration

---

## 4. MongoDB Schema — `remedies_rules` Collection

```json
{
  "remedy_id": "R-LK-SAT-001",
  "science_id": "vedic_astrology",
  "tradition": "lal_kitab | crystal_therapy | feng_shui | lo_shu | zibu | krishna_prashanavali | vedic_classical",
  "type": "ritual | gemstone | mantra | yantra | puja | dietary | spatial | symbol | color",
  "approval_status": "approved | pending_review | deprecated",
  "condition": {
    "planet": "Saturn",
    "house": 7,
    "affliction": ["debilitated"],
    "life_domain": ["marriage", "partnership"],
    "trigger_modules": ["birth_chart", "dasha", "krishna_oracle"],
    "gender": "neutral",
    "intensity": ["moderate", "severe"]
  },
  "remedy": {
    "title": "Feed black dogs on Saturday",
    "description": "Full instruction including timing, materials, and procedure",
    "duration": "11 Saturdays",
    "frequency": "weekly",
    "ease": "easy",
    "cost_level": "free | low | medium | high",
    "precautions": "optional safety notes",
    "expected_benefit": "Pacifies malefic Saturn, improves relationships"
  },
  "source": {
    "primary": "Lal Kitab",
    "chapter": "Saturn Remedies",
    "author": "Pt. Roop Chand Joshi",
    "confidence": 0.87
  },
  "tags": ["saturn", "marriage", "weekly_ritual", "animal_feeding"],
  "metadata": {
    "batch_id": "lal-kitab-remedies-v1-20260425",
    "is_universal": false,
    "is_daily": false
  },
  "created_at": "ISO timestamp"
}
```

---

## 5. Backend API

### File: `backend/remedies_engine.py`

| Method | Route | Purpose |
|---|---|---|
| POST | `/api/remedies/suggest` | Main endpoint — returns remedy pack for given context |
| GET | `/api/remedies/rule/{remedy_id}` | Get single remedy detail |
| GET | `/api/remedies/traditions` | List available traditions and counts |
| GET | `/api/admin/remedies/rules` | Admin: browse all rules with filters |
| POST | `/api/admin/remedies/rules` | Admin: add a new remedy rule |
| PATCH | `/api/admin/remedies/rules/{id}` | Admin: edit/approve a rule |

### Suggestion Logic (`POST /api/remedies/suggest`):
1. Parse context object
2. Query `remedies_rules` where `approval_status = "approved"` and condition fields match
3. Score each match by: condition specificity + confidence + tradition diversity
4. Return top 5–7 remedies, max 2 per tradition (for variety)
5. If fewer than 3 results: fall back to universal planet remedies for that planet

### Caller Integration:
```python
# Any module calls this pattern:
from remedies_engine import get_remedy_pack

pack = await get_remedy_pack({
    "trigger": "birth_chart",
    "planet": "Saturn",
    "house": 7,
    "affliction": "debilitated",
    "life_domain": "marriage"
})
```

---

## 6. Frontend Integration Points

### Krishna Prashanavali
- Answer pack already has a `remedies` section in the spec
- After oracle answer is rendered, call `POST /api/remedies/suggest` with `trigger: "krishna_oracle"` and oracle context
- Display as collapsible "Remedies for You" section below the oracle answer

### Birth Chart / Kundali
- Identify top 3 afflicted planets from chart
- Auto-call remedies suggest for each
- Display on a "Remedies" tab in BirthChartPage

### Daily/Weekly/Monthly Horoscope
- Call remedies suggest with `trigger: "daily_horoscope"`, sign's ruling planet, current dasha (if known)
- Display as "Today's Remedy" card — 1 remedy per day

### Dasha Reports (Arc Angel)
- During a malefic dasha period, auto-append relevant remedies
- Use `trigger: "dasha"`, `dasha_planet`, `life_domain` from period quality

---

## 7. Knowledge Ingestion Pipeline

### Phase 1 — Source Preparation (Gemini + Notebook LM)

**Step 1: OCR PDF → Clean Word Doc (Gemini)**
- Give Gemini each PDF chapter
- Prompt: *"Convert this scanned PDF to a clean plain text document. Preserve all lists, numbered items, and remedy instructions exactly. Do not summarize or paraphrase. Output as plain text with clear section headings."*

**Step 2: Clean Doc → Structured Insights (Notebook LM)**
Use these specific Notebook LM prompts (see Section 8 below):

**Step 3: Structured Insights → MongoDB (Claude ingest script)**
- Claude reads the Notebook LM output
- Maps each remedy to the `remedies_rules` schema
- Writes ingest script (same pattern as existing BPHS chapter scripts)
- Runs with `--dry-run` first, then `--apply`

### Phase 2 — Validation
- Same `validate_rules.py` pipeline as Knowledge Engine
- Approval threshold: approval_status must be `approved` before surfacing to users
- Initial run: expect 20–40% pending_human_review — lower than KE because remedies are more concrete

---

## 8. Notebook LM Prompts for Each Source

### For Lal Kitab:
```
You are extracting remedy rules from Lal Kitab for a Vedic astrology knowledge engine.

For each remedy in this chapter, extract:
1. Planet the remedy applies to (Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn/Rahu/Ketu)
2. House placement (1-12) if specified
3. Life domain affected (marriage/career/health/wealth/spiritual/family/children/enemies)
4. Specific remedy instruction — exact text, do not paraphrase
5. Duration (e.g., "11 Saturdays", "40 days", "ongoing")
6. Materials or actions required
7. Any precautions mentioned

Output as a JSON array, one object per remedy.
Do NOT group remedies. Each specific instruction = one remedy object.
If a remedy covers multiple planets, create one object per planet.
```

### For Crystal Therapy:
```
You are extracting crystal and gemstone remedy rules for a Vedic astrology knowledge engine.

For each gemstone/crystal remedy:
1. Planet it strengthens or pacifies (Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn/Rahu/Ketu)
2. Gemstone name (both English and Sanskrit/Hindi if given)
3. How to wear/use it (finger, metal, day to wear)
4. Weight in carats if specified
5. Who should/should NOT wear it
6. Expected benefit
7. Precautions

Output as JSON array, one object per gemstone-planet pairing.
```

### For Feng Shui:
```
You are extracting Feng Shui placement remedies for a life-domain remedy engine.

For each Feng Shui remedy:
1. Life domain it addresses (wealth/relationships/health/career/knowledge/family/fame/travel/children)
2. Specific placement instruction (direction, room, object type)
3. Colors associated
4. Objects to place or avoid
5. Timing if relevant (year, season)

Output as JSON array. One object per specific placement instruction.
```

### For Lo Shu Grid:
```
You are extracting Lo Shu Grid remedies based on missing numbers in birth dates.

For each missing number (1-9):
1. Missing number
2. Life area affected when this number is missing
3. Specific remedy to compensate (color to wear, direction to face, number to surround yourself with)
4. Mantra or affirmation if given
5. Expected benefit

Output as JSON array, one object per missing number.
```

---

## 9. Phased Delivery

### Phase 1 — Core Engine (Commission Now)
- `remedies_engine.py` backend with `POST /api/remedies/suggest`
- MongoDB schema + indexes
- Lal Kitab remedies ingested and approved (~200 rules expected)
- Krishna Prashanavali integration (remedies section in answer pack)
- Birth Chart "Remedies" tab

### Phase 2 — Expand Knowledge (After Phase 1)
- Crystal Therapy ingested
- Feng Shui ingested
- Lo Shu Grid ingested
- Daily Horoscope "Today's Remedy" card
- Admin Console — Remedies tab

### Phase 3 — Advanced (Future)
- Zibu Symbols
- Remedy personalization by user history
- Remedy effectiveness tracking (user feedback)
- Premium remedy reports (PDF)

---

## 10. Questions for Codex Modules

Before opening the final commission, the following questions should be sent to each Codex module for input:

**To Krishna Prashanavali Codex:**
1. What fields from the oracle answer context should be passed to the Remedies Engine?
2. How many remedies should appear per oracle answer — 3, 5, or user-selectable?
3. Should remedies be gated behind a premium subscription or free for all?

**To Birth Chart / Kundali Codex:**
1. Which planets/houses should auto-trigger remedies? (All afflicted, or only top 3?)
2. Should the Remedies tab be part of the existing BrihatKundliPage or a separate route?

**To Dasha / Arc Angel Codex:**
1. Should remedies appear for both Mahadasha AND Antardasha, or Mahadasha only?
2. During a beneficial period — should remedies appear at all, or only for malefic periods?

---

## 11. Constraints (All Codex Modules Must Respect)

- All remedy rules must have `approval_status: "approved"` to be surfaced — same gate as Knowledge Engine
- The engine calls `vedic_calculator.py` for any live chart data — do NOT recompute in remedies_engine.py
- Use `update_many` for all MongoDB writes (existing convention)
- AutoReconnect retry with exponential backoff on all DB operations
- Python 3.12, FastAPI, Motor async, no blocking calls in async routes
- No hardcoded remedy text in Python code — all content lives in MongoDB
