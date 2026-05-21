# Commission IR-5 -- 12 Areas of Life Enhancement Layer

> EverydayHoroscope · Stack: FastAPI + React 18 + Tailwind CSS + MongoDB (Motor async) + pyswisseph 2.10.x
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Live app: https://www.everydayhoroscope.in
> Issued: 2026-05-22
> **Depends on IR-4 being integrated first.** Do NOT begin until all 6 IR-4 routers are live.

---

## Context & Objective

The Individual Reports suite has 12 reports (6 live, 6 delivered via IR-4) mapping to the 12 Vedic houses. This commission adds three new analytical layers to all 12 reports:

1. **Donut Chart % (Structural Resilience Score)** -- a single percentage summarising the house's strength
2. **10-Year Vimshottari × Transit Horizon** -- chronological auspicious/inauspicious flag timeline
3. **Graha Drishti Matrix** -- Vedic planetary aspect calculations per report's primary house

These enhance existing reports -- they do NOT replace or restructure them.

---

## Architecture Rules (Mandatory)

1. **ALL computation via `vedic_calculator.py` + `pyswisseph`** -- do NOT add dasha calculation functions elsewhere
2. **Pure Vedic framework only** -- no Western planets (no Uranus, Neptune, Pluto). Substitutions:
   - Uranus → **Rahu** (disruption, unconventional intelligence)
   - Neptune → **Ketu** (transcendence, spiritual dissolution)
   - Pluto → **8th House Lord / Mars configurations**
3. **Graha Drishti uses Whole Sign, sign-to-sign aspects** -- not degree-based
4. **Do NOT modify** existing report routers. Add new endpoints only.
5. **Claude enrichment** follows existing `try_claude_generation()` pattern in `karmic_debt_prompt_service.py`
6. **MongoDB:** Motor async, existing patterns -- no new DB connections

---

## Deliverable 1 -- Backend: Three New Calculation Engines

Add these three functions to `backend/vedic_calculator.py`:

### 1A -- `calculate_donut_resilience(house_data: dict) -> int`

```python
def calculate_donut_resilience(house_data: dict) -> int:
    """
    Calculates the Structural Resilience % for any focus area house.
    Formula: Base (50%) + Dignity Modifier (max ±30%) + Aspect Modifier (max ±20%)
    Capped strictly between 5% and 95%.

    Args:
        house_data (dict):
            {
                "essential_dignity": str,  # "Exalted" | "Moolatrikona" | "Own Sign" | "Neutral" | "Enemy Sign" | "Debilitated"
                "benefic_aspects_count": int,  # count of Jupiter/Venus aspects on house lord
                "malefic_aspects_count": int   # count of Saturn/Mars/Rahu/Ketu aspects on house lord
            }
    Returns:
        int: percentage 5-95
    """
    dignity_weights = {
        "Exalted": 30, "Moolatrikona": 25, "Own Sign": 20,
        "Neutral": 0, "Enemy Sign": -15, "Debilitated": -30
    }
    resilience_score = 50
    resilience_score += dignity_weights.get(house_data.get("essential_dignity", "Neutral"), 0)
    aspect_modifier = (house_data.get("benefic_aspects_count", 0) * 10) - (house_data.get("malefic_aspects_count", 0) * 10)
    aspect_modifier = max(-20, min(20, aspect_modifier))
    resilience_score += aspect_modifier
    return max(5, min(95, resilience_score))
```

### 1B -- `calculate_graha_drishti(planet_positions: dict) -> dict`

```python
def calculate_graha_drishti(planet_positions: dict) -> dict:
    """
    Computes Vedic Graha Drishti (Planetary Aspects) using Whole Sign system.
    Universal 7th aspect for all planets.
    Special aspects: Saturn (3rd, 10th), Mars (4th, 8th), Jupiter/Rahu/Ketu (5th, 9th).

    Args:
        planet_positions (dict): { "Planet": sign_index_1_to_12 }
            e.g. {"Saturn": 1, "Mars": 4, "Jupiter": 8, "Rahu": 3, "Ketu": 9}
    Returns:
        dict: { "Planet": [list of aspected sign indices] }
    """
    special_aspects = {
        "Saturn": [3, 10], "Mars": [4, 8],
        "Jupiter": [5, 9], "Rahu": [5, 9], "Ketu": [5, 9]
    }
    drishti_map = {}
    for planet, current_sign in planet_positions.items():
        target_houses = [7]
        if planet in special_aspects:
            target_houses.extend(special_aspects[planet])
        aspected_signs = []
        for house in target_houses:
            target_sign = (current_sign + house - 1) % 12
            aspected_signs.append(12 if target_sign == 0 else target_sign)
        drishti_map[planet] = sorted(aspected_signs)
    return drishti_map
```

### 1C -- `generate_10_year_horizon(natal_house_cusp_deg, running_dashas) -> list`

```python
import datetime

def generate_10_year_horizon(natal_house_cusp_deg: float, running_dashas: list) -> list:
    """
    Generates a 10-year Temporal Optimisation Index (TOI) array.
    TOI = Dasha Weight (DW) + Transit Aspect Weight (TAW).

    DW: +30 (benefic dasha lord running), 0 (neutral), -30 (malefic / 6th/8th/12th lord dasha)
    TAW: +20 (Jupiter trine/conjunction to house cusp), -20 (Saturn square/opposition to house cusp)
         -15 (Rahu/Ketu exact conjunction ±2°)

    Status: TOI >= 15 → "Auspicious", TOI <= -15 → "Inauspicious", else → "Stabilized"

    Args:
        natal_house_cusp_deg (float): exact longitude of target house cusp (0-360)
        running_dashas (list): [{"start": date, "end": date, "lord": str, "status": str ("Benefic"|"Malefic"|"Neutral")}]
    Returns:
        list: [{"year": str, "status": str, "trigger": str}] × 10 years
    """
    BENEFIC_PLANETS = {"Jupiter", "Venus", "Mercury", "Moon"}
    MALEFIC_PLANETS = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}

    def get_dasha_weight(check_date):
        for d in running_dashas:
            if d["start"] <= check_date <= d["end"]:
                if d.get("status") == "Benefic" or d["lord"] in BENEFIC_PLANETS:
                    return 30
                elif d.get("status") == "Malefic" or d["lord"] in MALEFIC_PLANETS:
                    return -30
        return 0

    def get_transit_weight(year):
        # In production: replace with actual pyswisseph swe.calc_ut() calls for Jupiter and Saturn
        # for the mid-year evaluation date. This stub returns 0; wire to ephemeris in production.
        return 0  # STUB -- wire to pyswisseph in production

    horizon_flags = []
    start_year = datetime.date.today().year
    for year in range(start_year, start_year + 10):
        eval_date = datetime.date(year, 6, 1)
        toi = get_dasha_weight(eval_date) + get_transit_weight(year)
        if toi >= 15:
            status, trigger = "Auspicious", "Benefic dasha + harmonious planetary configurations active."
        elif toi <= -15:
            status, trigger = "Inauspicious", "Malefic dasha or challenging transit -- consolidate and plan."
        else:
            status, trigger = "Stabilized", "Neutral baseline -- steady progress possible."
        horizon_flags.append({"year": str(year), "status": status, "trigger": trigger})
    return horizon_flags
```

**Production note on `get_transit_weight`:** Wire it to actual `swe.calc_ut()` calls for Jupiter and Saturn longitudes at mid-year, then compute angular distance to `natal_house_cusp_deg` using:
```python
raw_diff = abs(planet_deg - natal_house_cusp_deg)
angular_distance = 180.0 - abs(180.0 - raw_diff)
# Jupiter conjunction/trine (0° or 120° ±3°) → +20
# Saturn conjunction/square/opposition (0°, 90°, 180° ±3°) → -20
# Rahu/Ketu conjunction (0° ±2°) → -15
```

---

## Deliverable 2 -- Backend: New Orchestration Endpoint

Add to `backend/server.py` a new router: `backend/ir_enhancement_router.py`

**Endpoint:** `POST /api/reports/enhanced-analysis`

```
Request body:
{
  "user_id": str,
  "focus_area": str,          # e.g. "Career & Work"
  "house_number": int,         # 1-12
  "house_cusp_sign": str,
  "house_lord": str,
  "house_lord_placement_sign": str,
  "essential_dignity": str,
  "benefic_aspects_count": int,
  "malefic_aspects_count": int,
  "natal_cusp_longitude": float,
  "planet_positions": dict,    # { "Saturn": 1, "Mars": 4, ... } -- sign indices
  "running_dashas": list       # from vedic_calculator.calculate_vimshottari_dasha()
}

Response:
{
  "donut_resilience_percentage": int,
  "ten_year_horizon_flags": list,
  "graha_drishti_on_house": list,
  "generated_report_markdown": str   # 4-page Vedic narrative from Claude
}
```

**Pipeline inside the endpoint:**
1. Call `calculate_graha_drishti(planet_positions)` → find planets aspecting the target house sign
2. Call `calculate_donut_resilience(house_data)` → get percentage
3. Parse dasha date strings to `datetime.date` objects
4. Call `generate_10_year_horizon(natal_cusp_longitude, parsed_dashas)` → get flags
5. Bundle into payload → call Claude with the Vedic system prompt (see Deliverable 4)
6. Return structured response

**All computation must be sourced from `vedic_calculator.py`.** Do NOT recalculate dasha timelines inside this router.

---

## Deliverable 3 -- Focus Area × House Mapping

Use this table in the orchestration router to auto-map `focus_area` to `house_number`:

| Focus Area | Primary House | Secondary House | Vedic Karakas |
|---|---|---|---|
| Health & Fitness | 1 (Body/Vitality) | 6 (Disease/Routine) | Sun, Mars |
| Career & Work | 10 (Status/Karma) | 6 (Daily Labor) | Saturn, Sun |
| Finances | 2 (Liquid Wealth) | 8 (Shared Assets) | Jupiter, Venus |
| Intellectual Life | 3 (Lower Mind) | 9 (Higher Education) | Mercury, **Rahu** (replaces Uranus) |
| Emotional Life | 4 (Mental Peace) | 12 (Subconscious) | Moon |
| Spirituality | 12 (Moksha/Solitude) | 9 (Philosophy) | Jupiter, **Ketu** (replaces Neptune) |
| Love Relationships | 7 (Partnerships) | 5 (Romance) | Venus, Jupiter |
| Family Life | 4 (Home/Roots) | 5 (Children) | Moon, Jupiter |
| Social Life | 11 (Networks) | 3 (Peers) | Jupiter |
| Adventure & Travel | 9 (Foreign Lands) | 5 (Speculation) | Jupiter, Mars |
| Environment | 4 (Physical Space) | 6 (Workplace) | Venus, Saturn |
| Creativity & Hobbies | 5 (Self-Expression) | 1 (Identity) | Venus, **Moon** (replaces Neptune) |

**Western planet substitutions (do NOT use Uranus, Neptune, or Pluto):**
- Uranus → Rahu (disruption, unconventional paths, sudden shifts)
- Neptune → Ketu (Moksha, spiritual dissolution, transcendence) -- or Moon+Venus for Creativity
- Pluto → 8th House Lord + strong Mars configurations

---

## Deliverable 4 -- Claude Vedic System Prompt

Save as: `backend/prompts/vedic_12areas_system_prompt.txt`

```
ROLE AND CONTEXT:
You are the Vedic Jyotish data-enrichment engine for EverydayHoroscope. Transform raw sidereal calculations, Graha Drishti matrices, and Vimshottari Dasha intervals into a premium 4-page dashboard narrative.

OPERATIONAL PRINCIPLES:
1. PURE JYOTISH PARADIGM: Operate within the Sidereal Zodiac framework (Lahiri Ayanamsha). Whole Sign houses. Ignore Western planets (Uranus, Neptune, Pluto) and degree-based aspect lines.
2. VEDIC SUBSTITUTIONS: Rahu = unconventional expansion/disruption. Ketu = Moksha/spiritual transcendence.
3. DATA FIDELITY: Use ONLY the metrics, percentages, and dasha intervals in the incoming payload. Do not alter dates, house positions, or calculation indices.
4. FORMATTING: Output exactly 4 pages using ### Page 1, ### Page 2, ### Page 3, ### Page 4 headers. Markdown tables for chart coordinates. High-density, clear language. No decorative emojis.

INBOUND PAYLOAD FORMAT:
- metrics: { donut_resilience_percentage: int, ten_year_horizon_flags: [{year, status, trigger}] }
- vedic_analytics: { focus_area, house_number, sign_on_cusp, house_lord, lord_placement_sign, graha_drishti_on_house: [planet names], active_dasha_layer: {lord, start, end} }

OUTPUT STRUCTURE:

### Page 1: Executive Summary & Dashboard Metrics
- Core Summary: 3 sentences assessing this life area from house strength, cusp sign, and lord placement.
- Resilience Score: Reference donut_resilience_percentage. Explain what it means for this area's innate stability.
- 10-Year Timeline: Walk through ten_year_horizon_flags chronologically. Name specific years flagged Auspicious or Inauspicious and the strategic implication.

### Page 2: Birth Chart Analytics & House Dynamics
- Core Coordinates Table: Markdown table -- House Number | Cusp Sign | House Lord | Lord Placement | Essential Dignity
- House Lord Analysis: How this lord's placement modifies the area's expression.
- Graha Drishti Matrix: List all planets in graha_drishti_on_house. Jupiter/Venus aspects = expansive/protective. Saturn/Mars/Rahu/Ketu aspects = structural conditions or tests.
- Active Dasha Timing: How the current Mahadasha/Antardasha activates or stalls this house right now.

### Page 3: Deep-Dive -- Foundational Dynamics
- Inherent Strengths & Behavioral Patterns: Natural abilities and defaults driven by this planetary layout.
- Karmic Blocks & Recurring Loops: Patterns implied by malefic aspects or weak lord placement.
- Optimal Environments: Where this chart configuration thrives.

### Page 4: Deep-Dive -- Predictive & Remedial Strategy
- 10-Year Operational Path: Strategic guidance per the dasha transitions and horizon flags.
- Behavioral Adjustments: Practical, non-mystical actions to overcome Page 3 blocks.
- Traditional Vedic Measures: Daily routine changes, environment adjustments, or traditional practices to balance challenging planetary energy.

EXECUTION: Begin directly with ### Page 1. No preamble, no acknowledgments.
```

---

## Deliverable 5 -- Frontend: Enhancement UI Components

### D5A -- `DonutChart.jsx` (new component)

`frontend/src/components/reports/DonutChart.jsx`

- SVG donut ring, percentage filled in gold (`#C5A059`)
- Percentage number in center (large, Cinzel font)
- Label below: "Structural Resilience"
- Accepts prop: `percentage: number`
- Responsive: 140px mobile, 180px desktop

### D5B -- `TenYearTimeline.jsx` (new component)

`frontend/src/components/reports/TenYearTimeline.jsx`

- Horizontal bar showing 10 years
- Green segment = Auspicious, Red segment = Inauspicious, Grey = Stabilized
- Tooltip on hover: `{year}: {trigger}`
- Accepts prop: `flags: [{year, status, trigger}]`

### D5C -- Wire to all 12 Report pages

Add `DonutChart` and `TenYearTimeline` to the top of each report's output page. The backend `POST /api/reports/enhanced-analysis` response populates both components.

Reports to update (add enhancement panels, do NOT change existing content):
- `LifeCyclesPage.jsx`, `RetrogradesurvivalPage.jsx`, `LunarCyclePage.jsx`, `ShadowSelfPage.jsx`, `CareerBlueprintPage.jsx`, `KarmicDebtPage.jsx`
- All 6 IR-4 report pages (once IR-4 is integrated)

---

## Deliverable Summary

| # | File | Type |
|---|---|---|
| D1A | `backend/vedic_calculator.py` (add `calculate_donut_resilience`) | Backend function |
| D1B | `backend/vedic_calculator.py` (add `calculate_graha_drishti`) | Backend function |
| D1C | `backend/vedic_calculator.py` (add `generate_10_year_horizon`) | Backend function |
| D2 | `backend/ir_enhancement_router.py` | New FastAPI router |
| D3 | Focus area mapping (inside D2) | Config table |
| D4 | `backend/prompts/vedic_12areas_system_prompt.txt` | Claude system prompt |
| D5A | `frontend/src/components/reports/DonutChart.jsx` | New React component |
| D5B | `frontend/src/components/reports/TenYearTimeline.jsx` | New React component |
| D5C | 12 report pages (add enhancement panel) | Frontend modification |

**Build verification:** `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` must pass before submitting.
