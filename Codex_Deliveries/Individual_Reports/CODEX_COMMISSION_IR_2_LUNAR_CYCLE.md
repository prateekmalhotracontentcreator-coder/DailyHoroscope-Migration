# Commission IR-2 -- Lunar Cycle Wellness Backend

> EverydayHoroscope · Stack: FastAPI, pyswisseph 2.10.x, MongoDB (Motor async)
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Backend API: https://everydayhoroscope-api.onrender.com
> Date issued: 2026-05-16

---

## Context

This is a backend-only commission. All Phase 2 Individual Report routers are built and live **except one**:
the **Lunar Cycle Wellness** report (`contract item 8-C`). Every other Phase 2 router has a deployed file in the repo.
This commission closes that single gap.

**What already exists (do NOT modify or duplicate):**

| File | Purpose |
|---|---|
| `backend/vedic_shared_utils.py` | Shared helpers: `get_db`, `get_user_email`, `build_natal_snapshot`, `build_transit_snapshot`, `get_report_collection`, `build_report_document` |
| `backend/encounter_window_router.py` | **Primary pattern reference** -- copy the exact file structure |
| `backend/intimacy_vitality_router.py` | Secondary pattern reference |
| `backend/server.py` | Main FastAPI app -- add 2 lines here (import + include_router) |
| `frontend/src/pages/reports/LoveReportsPage.jsx` | Frontend hub -- add 1 entry to `LOVE_REPORTS` array here |

---

## What to Build

### File 1: `backend/lunar_cycle_router.py`

**Router prefix:** `/api/reports/lunar-cycle`
**Tags:** `["reports", "love"]`
**Collection field:** `report_type: "lunar_cycle_wellness"` in `individual_reports` collection

**Model this file on `encounter_window_router.py` exactly.** Follow the same:
- Import pattern (`vedic_shared_utils`, prompt service)
- `StrictModel(BaseModel)` with `model_config = ConfigDict(extra="forbid")`
- `get_db` + `get_report_collection` pattern
- `get_user_email` for auth (optional -- unauthenticated users can generate but not save)
- `build_natal_snapshot` for birth chart data
- `build_transit_snapshot` for current moon position
- `build_report_document` for the stored document
- History endpoint: `GET /api/reports/lunar-cycle/history`

#### Endpoint 1 -- Generate Report
```
POST /api/reports/lunar-cycle/generate
```

**Request body:**
```json
{
  "date_of_birth": "YYYY-MM-DD",
  "time_of_birth": "HH:MM",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": "Asia/Kolkata",
  "city_name": "New Delhi",
  "reference_date": null
}
```
(`reference_date` defaults to today UTC if null)

**What to compute (all via pyswisseph):**
1. **Current moon phase** -- using `swe.calc_ut()` for Sun and Moon longitudes → compute phase angle → derive phase name (New Moon, Waxing Crescent, First Quarter, Waxing Gibbous, Full Moon, Waning Gibbous, Last Quarter, Waning Crescent) and illumination %
2. **Moon nakshatra** -- current moon longitude → nakshatra (1-27) + pada (1-4) + nakshatra lord
3. **Days to next significant phase** -- next New Moon, Full Moon (pyswisseph `swe.pheno_ut` or manual calculation)
4. **Natal moon sign** -- from birth data (Moon's natal rashi)
5. **Transit moon vs natal moon** -- house transit (which natal house is moon transiting now)
6. **Cycle day** -- day count within current lunar cycle (1-30)

**LLM enrichment** -- delegate to `lunar_cycle_prompt_service.py` (see File 2):
- Pass the computed moon data
- Receive: `phase_wellness_note`, `nakshatra_wellness_note`, `weekly_rhythm` (3-4 bullet array), `recommended_practices` (array of 3 items: practice_name + description), `caution_note`

**Response schema:**
```json
{
  "report_id": "uuid",
  "report_type": "lunar_cycle_wellness",
  "reference_date": "2026-05-16",
  "moon_phase": {
    "phase_name": "Waxing Gibbous",
    "illumination_pct": 72,
    "cycle_day": 11,
    "days_to_full_moon": 4,
    "days_to_new_moon": 18
  },
  "moon_nakshatra": {
    "name": "Hasta",
    "pada": 3,
    "lord": "Moon",
    "longitude": 163.4
  },
  "natal_context": {
    "natal_moon_sign": "Vrishabha",
    "transit_house": 5
  },
  "wellness": {
    "phase_wellness_note": "string",
    "nakshatra_wellness_note": "string",
    "weekly_rhythm": ["string", "string", "string"],
    "recommended_practices": [
      { "practice_name": "string", "description": "string" }
    ],
    "caution_note": "string"
  },
  "generated_at": "ISO-8601"
}
```

#### Endpoint 2 -- History
```
GET /api/reports/lunar-cycle/history?limit=10&skip=0
```
Same pattern as `encounter_window_router.py` history endpoint.

---

### File 2: `backend/lunar_cycle_prompt_service.py`

Create alongside the router. Model on `encounter_window_prompt_service.py`.

Function signature:
```python
async def enrich_lunar_cycle_with_claude(moon_data: dict) -> dict:
    """
    Receives computed moon phase + nakshatra + natal context.
    Returns wellness enrichment keys:
      phase_wellness_note, nakshatra_wellness_note, weekly_rhythm (list),
      recommended_practices (list of dicts), caution_note
    """
```

The system prompt should instruct Claude to act as a Vedic wellness advisor
interpreting the lunar cycle through the lens of moon phase + nakshatra + natal moon sign.
Keep each text field under 120 words. `weekly_rhythm` should be exactly 3 bullet strings.
`recommended_practices` should be exactly 3 items, each with `practice_name` + `description`.

---

### File 3: Server.py additions (2 lines only)

**Line ~line 80 (imports section):**
```python
from lunar_cycle_router import router as lunar_cycle_router
```

**Line ~line 2072 (after `app.include_router(intimacy_vitality_router)`):**
```python
app.include_router(lunar_cycle_router)
```

---

### File 4: `frontend/src/pages/reports/LoveReportsPage.jsx` -- 1 entry added

Add to `LOVE_REPORTS` array (insert after `intimacy_vitality_forecast` entry):
```javascript
{
  type: "lunar_cycle_wellness",
  slug: "lunar-cycle",
  label: "Lunar Cycle Wellness",
  description: "Your personal wellness rhythm across the 30-day moon cycle",
  accent: "#7b5ea7",
  tint: "rgba(123, 94, 167, 0.12)",
  icon: "☽"
},
```

The LoveReportsPage already has full generate + display logic for all report types via the `LOVE_REPORTS` config array. **No other frontend changes needed** -- the page dynamically renders based on the array.

---

## Constraints

- **Do NOT modify `vedic_calculator.py`** -- all moon computation goes directly via pyswisseph in the router
- **Do NOT duplicate** any function already in `vedic_shared_utils.py`
- **Do NOT add new Python dependencies** -- pyswisseph is already in `requirements.txt`
- Python 3.12, FastAPI, Motor (async MongoDB) -- same versions as all other routers
- All times stored UTC, displayed in user's local timezone

---

## Acceptance Criteria

- [ ] `POST /api/reports/lunar-cycle/generate` returns valid JSON matching schema above
- [ ] Moon phase name + illumination % correct for today's date (verify against timeanddate.com)
- [ ] Nakshatra derived correctly from moon longitude (verify against Drik Panchang)
- [ ] History endpoint returns past reports for authenticated user
- [ ] LoveReportsPage shows "Lunar Cycle Wellness" card after adding to LOVE_REPORTS array
- [ ] Backend Render deploy logs show no import errors
- [ ] `lunar_cycle_router` registered and accessible at `/api/reports/lunar-cycle/generate`
