# The Strategist -- Full Build Spec
> For: Claude Code Account 2
> Status: READY TO BUILD
> Last updated: 2026-05-09
> Source docs: 7. Lal Kitab_Career_The Strategist_Master Document (1).md + The Strategist Module_LLM Specific Q&A_GAI.md

---

## 1. What The Strategist Is

Top Menu Bar module replacing "Career Plus" drop-in. A **business intelligence war room** that pulls from:
- Lal Kitab Remedies Engine (`jyotish_lk_remedies`) -- IDs 308-668
- LK Standalone Module (`lk_user_profiles`, `lk_tracker`)
- Lal Kitab core rules (existing `knowledge_rules` collection)
- Astrology Package (`vedic_calculator.py` -- MANDATORY single source for all live data)
- Phase 2 (deferred): KP Astrology, Numerology

**Persona:** "Bloomberg Terminal for Karma" -- cyberpunk war room aesthetic, mission-based language.

---

## 2. ID Architecture (Strategist Collection)

> Last reconciled: 2026-05-12 | Source: Master Inventory List (GAI) + verify_strategist_complete.py

| Block | IDs | Count | Content | Status |
|---|---|---|---|---|
| CEO Forecast | 701-720 | 20 | Quarterly goal-setting, long-term visioning | ✅ LIVE |
| Battle Cadence | 721-750 | 30 | Daily/weekly/monthly tactical rhythms | ✅ LIVE |
| Strategic Pivot | 751-800 | 50 | Digbala-based market entry, location shifts | ✅ LIVE |
| The Garrison | 801-850 | 50 | Staffing archetypes, loyalty anchors, HR audits | ✅ LIVE (ID 817 gap-filled) |
| Technical Siege | 851-900 | 50 | Legacy hard-tech: redundancy, security, tech-debt | ✅ LIVE |
| The War Chest | 901-951 | 51 | Legacy finance: equity, cap-tables, exit readiness | ✅ LIVE |
| Hurdle Library | 952-975 | 24 | Retrograde/eclipse/combustion alerts | ✅ LIVE |
| Digital Siege | 976-1025 | 50 | SEO monopoly, algorithmic warfare | ✅ LIVE |
| Sales Warfare | 1026-1075 | 50 | Rival displacement, VVIP acquisition | ✅ LIVE |
| Peak Reach / Oracle State | 1076-1125 | 50 | Global monopolisation, succession, Oracle State | ✅ LIVE |
| Success Algorithm | 1022 | 1 | Score synthesizer + 4-tier narrative (within Digital Siege range) | ✅ LIVE |
| Salvage Patch | 1126-1137 | 12 | Operational hurdles (Account 2 addition) | ✅ LIVE |
| Reserved | 1138-1200 | -- | Future industry-specific modules | -- |
| **Universal Surrogates V2** | **1201-1225** | **25** | Biological relative fallbacks -- full 9-param schema | ✅ LIVE |
| ~~Universal Surrogates V1~~ | ~~651-675~~ | ~~25~~ | **DEPRECATED** -- superseded by 1201-1225 | ❌ Retired |

**Total active records (lalkitab_strategist): 462** ✅ verified 2026-05-12
**Grand Total with jyotish_lk_remedies (361): 823 active records** ✅ verified 2026-05-12

**Surrogate note (UPDATED):** V1 surrogates (651-675) are retired (`approval_status: "deprecated"`). All backend surrogate queries must point to **1201-1225**. V2 batch has full 9-parameter schema including `pivot_logic`, `trigger_condition`, `kpi_target` -- required for the live dashboard.

**science_id:** `"lalkitab_strategist"`
**collection:** `knowledge_rules`

---

## 3. Strategist Record Schema

```json
{
  "id": 953,
  "science_id": "lalkitab_strategist",
  "mission_name": "Operation Solar South (Sun in H10)",
  "mission_objective": "Authority Expansion & Brand Dominance",
  "trigger_condition": "Transit_Sun_H10",
  "strategy": "The 'Royal Mandate' Invasion",
  "decision_logic": "Sun in H10 is peak professional authority...",
  "pivot_logic": "H10 public image + Rahu = scandal...",
  "pivot_action": "Launch high-ticket certification...",
  "kpi_target": "Institutional Partnership growth & Media Mentions",
  "remedy_id": 586,
  "approval_status": "pending_human_review"
}
```

**Hurdle records add:**
```json
{
  "ui_warning": "High Alert: Authority Eclipse detected. Move to stealth mode."
}
```

**Surrogate records add:**
```json
{
  "surrogate_type": "universal|industry",
  "industry": "Tech|Operations|Legal_Consulting|Leadership|Creative|Sales_Defense|E-commerce",
  "relative_unavailable": "Father|Mother|Sister|Brother|Grandfather|Uncle|Spouse|Son|In-laws"
}
```

---

## 4. Data Sources The Strategist Pulls From

| Data | Source | How |
|---|---|---|
| Live birth chart / natal positions | `vedic_calculator.py` → `calculate_vimshottari_dasha()` | MANDATORY -- never replicate |
| Current dasha | `vedic_calculator.py` → `get_current_dasha()` | MANDATORY |
| Current transits | `vedic_calculator.py` + `panchang_router.py` | Live planetary positions |
| LK User Profile | `lk_user_profiles` collection | Read from LK Standalone module |
| LK Diagnostic Report | `POST /api/lk/diagnose` | Call LK route, embed in Strategist context |
| LK Tracker status | `lk_tracker` collection | Ritual consistency → Success Probability |
| Strategist rules | `knowledge_rules` where `science_id: "lalkitab_strategist"` | Mission + Hurdle + Surrogate records |
| LK Remedy rules | `knowledge_rules` where `science_id: "jyotish_lk_remedies"` | Cross-referenced via `remedy_id` |

---

## 5. Backend Routes

All routes prefix: `/api/strategist/`

| Method | Route | Input | Output |
|---|---|---|---|
| GET | `/dashboard` | user_id | Full war room state JSON |
| POST | `/missions` | user_id, date | Active missions list (transit-triggered) |
| POST | `/hurdles` | user_id | Active hurdle alerts |
| POST | `/probability` | user_id | Success Probability score (ID 1022 algorithm) |
| POST | `/surrogate` | user_id, planet, relative_unavailable, industry | Surrogate bridge record |
| GET | `/report/pdf` | user_id | Premium Executive Intelligence Brief |

---

## 6. Success Probability Algorithm (ID 1022)

```python
def calculate_conquest_probability(user_data: dict, transit_data: dict) -> dict:
    """
    user_data keys: command_planet_strength (float), office_location (str),
                    success_direction (str), active_pitru_rin (bool),
                    surrogate_active (bool), ritual_streak (int)
    transit_data keys: primary_planet_degree (int)
    Returns: {"score": int, "narrative": str, "factors": [...]}
    """
    score = 50
    factors = []

    # 1. Shadbala (live from vedic_calculator.py -- NOT from shadbala_threshold string field)
    if user_data['command_planet_strength'] > 1.2:
        score += 10; factors.append({"factor": "Shadbala", "delta": +10})
    else:
        score -= 5; factors.append({"factor": "Shadbala", "delta": -5})

    # 2. Digbala (office direction vs planet's power direction)
    if user_data['office_location'] == user_data['success_direction']:
        score += 15; factors.append({"factor": "Digbala", "delta": +15})
    else:
        score -= 10; factors.append({"factor": "Digbala", "delta": -10})

    # 3. Karmic Debt (from LK diagnose Gate 1)
    if user_data['active_pitru_rin']:
        score -= 20; factors.append({"factor": "Pitru_Rin", "delta": -20})
        if user_data['surrogate_active']:
            score += 12; factors.append({"factor": "Surrogate_Bridge", "delta": +12})

    # 4. Transit Peak (25°-28° = peak window)
    deg = transit_data['primary_planet_degree']
    if 25 <= deg <= 28:
        score += 5; factors.append({"factor": "Transit_Peak", "delta": +5})

    # 5. Ritual Consistency (from lk_tracker streak)
    streak = user_data['ritual_streak']
    if streak >= 7:
        score += 10; factors.append({"factor": "Ritual_Momentum", "delta": +10})
    elif streak == 0:
        score -= 15; factors.append({"factor": "No_Ritual", "delta": -15})

    score = max(0, min(99, score))

    narratives = {
        "high": "Strategic Sovereign: Empire in high-alignment. Execute Expansion mission immediately.",
        "mid": "Tactical Stagnation: Moderate friction. Settle Mercury debts before next Sales Bid.",
        "low": "Karmic Lockdown: High risk. Withdraw from offensive marketing. Focus Internal Fortress."
    }
    narrative = narratives["high"] if score >= 70 else narratives["mid"] if score >= 40 else narratives["low"]

    return {"score": score, "narrative": narrative, "factors": factors}
```

**Input sources:**
- `command_planet_strength`: from `vedic_calculator.py` Shadbala (existing `CODEX_COMMISSION_SHADBALA_ENGINE.md`)
- `office_location`: from `lk_user_profiles` → location_slug → Digbala direction mapping
- `active_pitru_rin`: from `POST /api/lk/diagnose` gate1 result
- `ritual_streak`: from `lk_tracker` current active record
- `primary_planet_degree`: from `vedic_calculator.py` live transit

---

## 7. Digbala Direction Map

```python
DIGBALA_DIRECTIONS = {
    "Sun": "South", "Moon": "North", "Mercury": "North",
    "Mars": "South", "Jupiter": "NE", "Venus": "SE",
    "Saturn": "West", "Rahu": "SW", "Ketu": "NW"
}
```

User's `office_location` (city) → derive compass quadrant from `lk_user_profiles.natal_chart` command planet → compare with `DIGBALA_DIRECTIONS[command_planet]`.

---

## 8. Mission Trigger Logic

Transit missions fire when: `trigger_condition` matches current planetary position from `vedic_calculator.py`.

```python
TRIGGER_MAP = {
    "Transit_Sun_H10": lambda chart, transits: transits["Sun"]["house"] == 10,
    "Transit_Saturn_H3": lambda chart, transits: transits["Saturn"]["house"] == 3,
    "Transit_Rahu_Conj_Natal_Sun": lambda chart, transits: abs(transits["Rahu"]["longitude"] - chart["Sun"]["longitude"]) < 8,
    "Mercury_Retrograde_H2_Shadow": lambda chart, transits: transits["Mercury"]["retrograde"] and transits["Mercury"]["house"] == 2,
    "Planet_Degree_29": lambda chart, transits: any(p["degree"] >= 29 for p in transits.values()),
    # etc.
}

def get_active_missions(user_natal_chart, current_transits, db):
    active = []
    missions = db.knowledge_rules.find({"science_id": "lalkitab_strategist"})
    for mission in missions:
        trigger = mission.get("trigger_condition")
        if trigger in TRIGGER_MAP and TRIGGER_MAP[trigger](user_natal_chart, current_transits):
            active.append(mission)
    return active
```

---

## 9. Golden Hour UI (ID 1027)

Frontend only. Use sunset time from `GET /api/panchang/daily` (already returns sunset timestamp).

```javascript
// War Room state machine
const SUNSET_BUFFER_MINS = 30;

function getWarRoomState(sunsetTimestamp) {
  const now = Date.now();
  const sunset = new Date(sunsetTimestamp).getTime();
  const buffer = SUNSET_BUFFER_MINS * 60 * 1000;

  if (now < sunset - buffer) return "OFFENSIVE_GOLD";
  if (now >= sunset - buffer && now <= sunset) return "GOLDEN_HOUR";
  return "DEFENSIVE_MIDNIGHT";
}

// CSS vars per state:
// OFFENSIVE_GOLD:    --war-primary: #FFD700; --ritual-status: OPEN
// GOLDEN_HOUR:       --war-primary: #FFC42E; pulse overlay; countdown timer; --ritual-status: URGENT
// DEFENSIVE_MIDNIGHT: --war-primary: #000B1E; --ritual-status: LOCKED; disable ritual log button
```

---

## 10. Frontend Pages

### `/strategist` -- War Room Dashboard
- Real-time state: OFFENSIVE / GOLDEN HOUR / DEFENSIVE
- Success Probability gauge (0-99%)
- Active Missions ticker (transit-triggered)
- Active Hurdle alerts (red overlay)
- Quick-link to LK Diagnostic + 43-Day Tracker status
- Golden Hour countdown (when within 30 min of sunset)

### `/strategist/missions` -- Mission Board
- Grid of active missions with: Mission Name, Objective, Pivot Action, KPI Target, linked Remedy ID
- Each mission card: "Add Remedy to Tracker" button (cross-links to LK Standalone tracker)
- Filter: by planet, by house, by date range

### `/strategist/report` -- Executive Intelligence Brief (PDF)
- Premium gate
- Sections: Conquest Probability, Active Missions, Hurdle Alerts, Recommended Remedies, 43-Day Roadmap
- PDF generation: use existing html2canvas → PDF export pattern

### `/strategist/surrogate` -- Surrogate Bridge
- Triggered when family census shows unavailable relative
- User selects: which planet + which relative unavailable + industry
- Returns surrogate record with pivot_action

---

## 11. Surrogate Logic (IDs 1201-1225 -- V2, LOCKED)

> V1 (651-675) is retired. All queries must use 1201-1225.

When `lk_user_profiles.family_census[relative] != "living"`:

```python
def get_surrogate(planet: str, relative: str, industry: str, db) -> dict:
    return db.knowledge_rules.find_one({
        "science_id": "lalkitab_strategist",
        "id": {"$gte": 1201, "$lte": 1225},
        "$or": [
            {"relative_unavailable": relative},
            {"industry": industry}
        ]
    })
```

Surrogate activation → `user_data['surrogate_active'] = True` → `+12` in Success Probability.

---

## 12. Ingest Script Required

**`backend/scripts/ingest_strategist_v1.py`**

Source file: `/Users/apple/Documents/Knowledge Engine_eBooks/Remedies + The Strategist/7. Lal Kitab_Career_The Strategist_Master Document (1).md`
Plus Q&A supplement: `The Strategist Module_LLM Specific Q&A_GAI.md`

Key rules:
- `science_id: "lalkitab_strategist"`
- `collection: "knowledge_rules"`
- Upsert key: `{"id": r["id"], "science_id": "lalkitab_strategist"}`
- Surrogate rows from Q&A: REMAP IDs 651→701, 652→702 ... 675→725
- Keep all `remedy_id` cross-references unchanged (they point to `jyotish_lk_remedies`)
- `approval_status: "pending_human_review"`
- ID 1022 and 1027 are special module configs -- include both

---

## 13. Phase 2 Plug-ins (Deferred -- Do Not Build Now)

| Plugin | science_id | Trigger |
|---|---|---|
| KP Astrology | `kp_astrology` | When KP rules ingested |
| Numerology | `jyotish_numerology` | When Numerology rules ingested |

Architecture: Strategist dashboard has plugin slot. When `science_id` collection has `approval_status: "approved"` records, plugin auto-activates. No code changes needed -- data-driven.

---

## 13b. Success Probability -- 4-Tier Narrative (ID 1022.N)

| Score | Tactical Status | Directive |
|---|---|---|
| 85-99% | Sovereign Dominance | "Expansion / All-In" |
| 60-84% | Operational Friction | "Patch & Pivot" |
| 40-59% | Strategic Siege | "Hold Ground / Remedy" |
| 0-39% | Karmic Lockdown | "Withdraw / Full Reset" |

Premium PDF sections: I. Executive Summary → II. Tactical Battle Plan (7-day) → III. Karmic Remedy Override (active surrogate) → IV. Conquest Timeline (probability curve)

---

## 13c. Strategist Schema Validator (Gate 0 for ingest_strategist_v1.py)

```python
REQUIRED_FIELDS = [
    "id", "science_id", "trigger_condition", "strategy",
    "decision_logic", "pivot_logic", "pivot_action",
    "kpi_target", "remedy_id", "approval_status"
]
SURROGATE_EXTRA = ["surrogate_type", "relative_unavailable"]  # IDs 651-675 only
HURDLE_EXTRA    = ["ui_warning"]                               # IDs 961-975 only
MODULE_IDS      = {1022, 1027}                                 # exempt -- config objects

def validate_strategist_batch(batch: list) -> dict:
    errors = []
    for r in batch:
        rid = r.get("id")
        if rid in MODULE_IDS:
            continue
        missing = [f for f in REQUIRED_FIELDS if f not in r]
        if missing:
            errors.append({"id": rid, "missing": missing})
    return {"total": len(batch), "errors": len(errors), "detail": errors}
```

---

## 14. Architecture Rule (MANDATORY -- From CLAUDE.md §16)

> All live astronomical and dasha computations MUST use `vedic_calculator.py` + `pyswisseph`.
> The Strategist engine MUST call `vedic_calculator.calculate_vimshottari_dasha()` for all dasha data.
> DO NOT add dasha calculation functions to any new router or engine file.
> Knowledge Engine rules are additive only -- they supplement, never replace, Legacy Model data.

---

## 15. Files to Create

```
backend/
  strategist_router.py          # All /api/strategist/* routes
  strategist_engine.py          # Mission trigger, Probability calc, Surrogate logic
  scripts/ingest_strategist_v1.py  # Data ingest from Master Document

frontend/src/pages/
  StrategistPage.jsx            # War Room dashboard
  StrategistMissionsPage.jsx    # Mission board
  StrategistReportPage.jsx      # Executive Intelligence Brief
  StrategistSurrogatePage.jsx   # Surrogate bridge

frontend/src/components/
  WarRoomStateProvider.jsx      # Golden Hour state machine (context)
  ConquestGauge.jsx             # Success Probability gauge
  MissionCard.jsx               # Individual mission display
  HurdleAlert.jsx               # Red overlay hurdle component
```

Register in `backend/server.py`:
```python
from strategist_router import router as strategist_router
app.include_router(strategist_router, prefix="/api/strategist")
```

Add routes in `frontend/src/App.js` under `/strategist/*`.

---

## 16. Key Source Files for Account 2 to Read

```
/Users/apple/Documents/Knowledge Engine_eBooks/Remedies + The Strategist/
  7. Lal Kitab_Career_The Strategist_Master Document (1).md   # Full Strategist spec
  The Strategist Module_LLM Specific Q&A_GAI.md               # IDs 953-1027, surrogate rows
  1. Readme. Brief Note on Remedies + The Strategist Module.md # Module overview

/Users/apple/DailyHoroscope-Migration/backend/
  vedic_calculator.py          # MANDATORY data source
  server.py                    # Router registration
  panchang_router.py           # Sunset time for Golden Hour

/Users/apple/DailyHoroscope-Migration/.claude/
  LK_STANDALONE_MODULE_SPEC.md  # LK Standalone spec (Strategist depends on this)
  CLAUDE.md                    # Architecture rules §16
```

---

## PHASE 2 -- KP + Astrology + LK Full Integration
> Added: 2026-05-11 | Session: Temple Build Planning

---

## P2.1 Six-Layer System Map

```
USER ENTERS THE STRATEGIST
         │
         ▼
╔═══════════════════════════════════════════════════╗
║  LAYER 0 (GATE 0) -- KRISHNA PRASHANAVALI          ║
║  "Should I act on this question?"                 ║
║  • User types question                            ║
║  • Taps 18×18 grid → one of 36 canonical answers  ║
║  • Verdict: YES / WAIT / NO / PRAY                ║
╚═══════════════════════════════════════════════════╝
    │         │         │          │
   YES       WAIT      NO         PRAY
    │         │         │          │
    ▼         ▼         ▼          ▼
 Layer 1   Pre-Flight  Remedy    Full Surrender
           Mode        Plan       Mode (§P2.4)
           ↓ complete  ↓ score
           AUTO-UNLOCK  ≥60% →
           Layer 1     Gate0 re-test
                       ↓ YES/WAIT
                       Layer 1
╔═══════════════════════════════════════════════════╗
║  LAYER 1 -- ASTROLOGY ENGINE                       ║
║  vedic_calculator.py -- MANDATORY                  ║
║  • Birth chart (natal positions)                  ║
║  • Vimshottari Dasha current period               ║
║  • Live transit positions (today)                 ║
║  • Shadbala / Digbala strength scores             ║
║  • Conquest Probability input (feeds ID 1022)     ║
╚═══════════════════════════════════════════════════╝
         │
         ▼
╔═══════════════════════════════════════════════════╗
║  LAYER 2 -- LAL KITAB DIAGNOSTIC (5 Gates)         ║
║  POST /api/lk/diagnose -- embedded in dashboard    ║
║  Gate 1: Karmic Debt (Pitru Rin)                  ║
║  Gate 2: House Awakening                          ║
║  Gate 3: Year Cycle Planet                        ║
║  Gate 4: Mercury Scan                             ║
║  Gate 5: Geographical Alignment                   ║
╚═══════════════════════════════════════════════════╝
         │
         ▼
╔═══════════════════════════════════════════════════╗
║  LAYER 3 -- STRATEGIST ENGINE + NOTIFICATIONS      ║
║  • Active Missions (transit-matched)              ║
║  • Hurdle Alerts (retrograde/eclipse/combustion)  ║
║  • Surrogate Bridge (family census gate)          ║
║  • Golden Hour state machine (sunset timer)       ║
║  • Notification Engine -- 7 Strategist triggers    ║
║    (routes through existing /api/notifications/   ║
║     trigger -- never calls push/WA directly)       ║
╚═══════════════════════════════════════════════════╝
         │
         ▼
╔═══════════════════════════════════════════════════╗
║  LAYER 4 -- REMEDIES ACTION PLAN                   ║
║  Unified merged timeline:                         ║
║  • LK execution_roadmap (days array)              ║
║  • Strategist mission pivot_actions               ║
║  • Surrogate activations                          ║
║  • 43-Day Tracker CTAs                            ║
╚═══════════════════════════════════════════════════╝
         │
         ▼
╔═══════════════════════════════════════════════════╗
║  LAYER 5 -- OUTPUT: PREMIUM REPORT                 ║
║  PDF Executive Brief (Razorpay gate)              ║
║  I. Conquest Probability + Gate 0 verdict         ║
║  II. 7-Day Tactical Battle Plan                   ║
║  III. Karmic Remedy Override (surrogate)          ║
║  IV. Conquest Timeline (probability curve)        ║
╚═══════════════════════════════════════════════════╝
         │
         ▼
╔═══════════════════════════════════════════════════╗
║  LAYER 6 -- WAR ROOM DASHBOARD (live)              ║
║  • State banner: OFFENSIVE/GOLDEN HOUR/DEFENSIVE  ║
║  • Gate 0 status badge                            ║
║  • Conquest Probability gauge (re-calcs on log)   ║
║  • Mission ticker                                 ║
║  • SUCCESS & DEBT TRACKING SCOREBOARD (embedded): ║
║    - Per-remedy: streak, discipline%, debt bar    ║
║    - Collective rituals (one-time)                ║
║    - Global debt clearance bar (X of 9 cleared)  ║
║  • Hurdle alerts                                  ║
║  • Action Plan snapshot (today's task)            ║
║  • Golden Hour countdown (sunset −30 min)         ║
╚═══════════════════════════════════════════════════╝
```

---

## P2.2 Gate 0 -- YES / WAIT / NO / PRAY Flow Logic

### WAIT Flow (Scenario 1 -- Temporal Barrier)
```
WAIT verdict → Pre-Flight Mode activated
Remedy plan assigned (LK Gate 1 or standard sequence)
Remedy plan completes → AUTO-UNLOCK Layer 1
No Gate 0 re-test required.
UI banner: "Pre-Flight Mode -- Day X of 43 → Auto-Unlock"
```

### NO Flow (Scenario 2 -- Directional Barrier)
```
NO verdict → Remedy Plan assigned
Remedy plan completes → Score check (ID 1022)
  Score ≥ 60% → Gate 0 re-test unlocked
  Score < 60% → Continue remedies (show deficit)
Gate 0 re-test:
  Returns YES/WAIT → proceed to Layer 1
  Returns NO again → continue remedy loop
UI banner: "Karmic Hold -- Score: 47/60 needed"
```

### PRAY Flow (Scenario 3 -- Full Surrender Mode)
```
PRAY verdict → Full Surrender Mode
System surfaces 3-module plan:
  1. Mantra Remedies Module (chart-personalised)
  2. LK Debt Audit (Pitru Rin + family census)
  3. 21-day PRAY Protocol (daily devotional schedule)
Score threshold for re-entry: ≥ 75% (harder than NO)
Gate 0 re-test: must return YES or WAIT (not another NO/PRAY)
UI: "Full Surrender -- Complete remedy + score ≥ 75% to re-test"
```

### Backend enforcement
```python
def evaluate_gate0_reentry(user_id, original_verdict, score, db):
    if original_verdict == "WAIT":
        return {"reentry": "AUTO", "gate0_required": False}
    if original_verdict == "NO":
        threshold = 60
        if score >= threshold:
            return {"reentry": "GATE0_REQUIRED", "gate0_required": True}
        return {"reentry": "CONTINUE_REMEDIES", "deficit": threshold - score}
    if original_verdict == "PRAY":
        threshold = 75
        if score >= threshold:
            return {"reentry": "GATE0_REQUIRED", "gate0_required": True}
        return {"reentry": "FULL_SURRENDER_CONTINUE", "deficit": threshold - score}
```

---

## P2.3 Notification Engine -- Strategist Triggers

**Architecture rule:** All Strategist notifications go through existing `/api/notifications/trigger/{type}`. The Strategist backend calls this internally -- never calls push/WhatsApp services directly.

Add to `TRIGGER_CONFIG` in `notification_trigger_router.py`:

| Trigger type | Channels | Timing |
|---|---|---|
| `strategist-golden-hour` | push, in_app | sunset −30 min |
| `strategist-streak-at-risk` | push, in_app, whatsapp | sunset −120 min |
| `strategist-streak-broken` | push, in_app, email | immediate |
| `strategist-gate0-qualified` | push, in_app | immediate (score hits threshold) |
| `strategist-mission-triggered` | push, in_app | immediate (transit match) |
| `strategist-debt-cleared` | push, in_app, email | immediate (Day 43 complete) |
| `strategist-wait-unlocked` | push, in_app | immediate (remedy plan complete) |

User preference category: `strategist` -- sub-opts: golden_hour, streak_warning, mission_alert.

---

## P2.4 KP Module -- Two Views in Live App

### View 1: Standalone Page
- Route: `/krishna-prashnavali`
- NavBar: **direct top-level link** (not in any dropdown)
- Full standalone oracle flow: question → grid → reading → remedy refs

### View 2: Strategist Gate 0 (embedded)
- Entry via War Room dashboard -- "Consult the Oracle" card
- Does NOT navigate away -- verdict returned inline to War Room
- Verdict stored in `kp_sessions` collection against user_id
- Controls War Room state (Pre-Flight / Full Surrender / Unlocked)

---

## P2.5 NavBar Changes

| Item | Current | Change |
|---|---|---|
| KP Module | Not present | **Add** -- direct NavBar link |
| Blog | NavBar | **Move to Footer** |
| Career | NavBar | **Move to Footer** |

---

## P2.6 Phase 2 Build Sequence

| Phase | Task | Dependency |
|---|---|---|
| 2A-1 | NavBar: add KP link, move Blog + Career to Footer | None |
| 2A-2 | Migrate KP files from Codex test host to live codebase | None |
| 2A-3 | Register `/krishna-prashnavali` route + backend router | 2A-2 |
| 2B | Wire KP Gate 0 into Strategist War Room (inline verdict) | 2A-2 |
| 2C | WAIT/NO/PRAY Pre-Flight banners on War Room | 2B |
| 2D | Score-gated re-entry check + loop logic (NO + PRAY flows) | 2B |
| 2E | Embed LK 5-Gate summaries inline in /api/strategist/dashboard | None |
| 2F | Success & Debt Scoreboard embedded in War Room (Layer 6) | None |
| 2G | Unified Action Plan page /strategist/action-plan | 2E |
| 2H | Add 7 Strategist trigger types to notification_trigger_router | None |
| 2I | PRAY path: surface Mantra + LK Debt Audit in Full Surrender | 2B |
| 2J | UI Polish: mobile layout, mission cards, dasha display | None |

---

## P2.7 KP Content -- Final Confirmed Architecture

- **36 answers** -- retain as-is (no reduction to 15)
- **4 verdicts** -- YES (Pratibha) / WAIT (Dhairya) / NO (Pratrodha) / PRAY (Bhakti)
- **18×18 grid** (324 cells) -- selection mechanism unchanged
- **`behavioral_remedy` field** -- added to all 36 slots (separate from ritual `remedy`)
- **Mantras** -- never hardcoded; all route through Remedies Engine via `remedy_ref`
- **Honorifics** -- Ji/Maa applied to all divine names across all 36 slots
- **Cross-discipline remedies** -- permitted (Saturn × Krishna, etc.)
- **`krishna_prashnavali_remedies`** -- new science_id in Remedies Engine for all KP remedy records

