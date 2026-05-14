# LK Standalone Module -- Build Spec
> For: Claude Code Account 2
> Status: READY TO BUILD
> Last updated: 2026-05-09

---

## 1. What This Is

Branch 1 of the Lal Kitab split. Standalone report-style pages accessible independently from The Strategist. These surface LK Remedy Engine data as user-facing reports.

**Does NOT require:** Strategist War Room, transit live computation, subscription (has own free/premium gate)

---

## 2. Data Layer (Already Live -- Do NOT Rebuild)

| Collection | science_id | Records | Status |
|---|---|---|---|
| `knowledge_rules` | `jyotish_lk_remedies` | 361 | ✅ Live, 12/12 verified |
| `knowledge_rules` | `jyotish_remedies_dhana` | 100 | ✅ Live |
| `knowledge_rules` | `jyotish_remedies_gemstones` | 98 | ✅ Live |
| `knowledge_rules` | `jyotish_remedies_crystals` | 100 | ✅ Live |
| `knowledge_rules` | `jyotish_remedies_chakra` | 7 | ✅ Live |
| `interpretation_rules` | various | multiple | ✅ Live |

**Verification scripts:** `backend/scripts/verify_lk_remedies_v1.py` (12/12 PASS)

---

## 3. New MongoDB Collections Required

### `lk_user_profiles`
```json
{
  "user_id": "string",
  "age": 36,
  "natal_chart": {"Sun": 1, "Moon": 4, "Mercury": 10, ...},
  "family_census": {
    "father": "living|deceased|unknown",
    "mother": "living|deceased|unknown",
    "brother": "living|deceased|unknown",
    "sister": "living|deceased|unknown",
    "grandfather_paternal": "living|deceased|unknown",
    "grandfather_maternal": "living|deceased|unknown"
  },
  "location_slug": "new-delhi",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

### `lk_tracker`
```json
{
  "user_id": "string",
  "remedy_id": 659,
  "science_id": "jyotish_lk_remedies",
  "start_date": "ISODate",
  "last_completed_date": "ISODate",
  "streak_days": 7,
  "status": "active|broken|complete",
  "day_log": [
    {"day": 1, "date": "ISODate", "completed": true, "within_window": true, "prohibited_avoided": true}
  ]
}
```

---

## 4. Backend Routes (FastAPI)

All routes prefix: `/api/lk/`

| Method | Route | Input | Output | Notes |
|---|---|---|---|---|
| POST | `/onboard` | age, natal_chart{}, family_census{}, location_slug | lk_user_profile doc | Upsert on user_id |
| POST | `/diagnose` | user_id | 5-gate diagnostic report JSON | See §5 |
| POST | `/conflict-check` | user_id, planned_action | conflict gate record or CLEAR | Queries IDs 616-625 |
| GET | `/tracker/{user_id}` | -- | all active tracker docs | |
| POST | `/tracker/log` | user_id, remedy_id, completed, within_window, prohibited_avoided | updated tracker doc | Binary cycle: miss = reset streak |
| POST | `/debt-audit` | user_id | debt profile + relative availability | Queries IDs 601-615 |
| GET | `/remedies` | science_id, filters | paginated remedy records | Standard query |

---

## 5. The 5-Gate Diagnostic Report (Core Output Format)

`POST /api/lk/diagnose` runs this sequence and returns:

```json
{
  "user_id": "string",
  "generated_at": "ISODate",
  "gates": {
    "gate1_karmic_debt": {
      "status": "WARNING|CLEAR",
      "records": [...],
      "priority_count": 12,
      "narrative": "Ancestral Debt active. Stabilize roots before transit gains."
    },
    "gate2_house_awakening": {
      "status": "DORMANT|ACTIVE",
      "dormant_houses": [10],
      "awakening_records": [...],
      "narrative": "H10 dormant. Activate H2 first."
    },
    "gate3_year_cycle": {
      "planet": "Saturn",
      "age_range": "36-41",
      "records": [...],
      "narrative": "Saturn Justice phase. Settlement, not expansion."
    },
    "gate4_mercury_scan": {
      "status": "EMPTY_VESSEL|RAHU_COLLISION|CLEAR",
      "records": [...],
      "narrative": "Mercury solitary in H10. Filling the Vessel required."
    },
    "gate5_geographical": {
      "user_direction": "South",
      "records": [...],
      "substitution_applied": false,
      "narrative": "South direction aligned. Directional Realignment active."
    }
  },
  "conflict_gates_active": [...],
  "execution_roadmap": [
    {"days": "1-7", "task": "Clear Kanya Rin (Gate 1)", "remedy_id": 622},
    {"days": "8", "task": "House Awakening H10 (Gate 2)", "remedy_id": 645},
    {"days": "9-52", "task": "43-Day Mercury Anchor (Gate 4)", "remedy_id": 659}
  ],
  "safety_gates_fired": [...]
}
```

**Gate query logic:**
- Gate 1: `science_id: "jyotish_lk_remedies", id: {$in: [483..615, 611..614]}`, filter sev≥4 as priority
- Gate 2: IDs 636-650 (House Awakening Matrix), match dormant houses from natal_chart
- Gate 3: IDs 526-575, filter by age→planet mapping (see §6)
- Gate 4: IDs 626-635, Mercury status from natal_chart
- Gate 5: IDs 505-525, 651-655, match direction + user location_slug

---

## 6. Age → 35-Year Cycle Planet Mapping

```python
YEAR_CYCLE = [
    (0, 8, "Ketu"), (9, 28, "Venus"), (29, 34, "Sun"),
    (35, 44, "Moon"), (45, 51, "Mars"), (52, 69, "Rahu"),
    (70, 85, "Jupiter"), (86, 104, "Saturn"), (105, 121, "Mercury")
]
def get_year_lord(age):
    for start, end, planet in YEAR_CYCLE:
        if start <= age <= end:
            return planet
```

---

## 7. Conflict Gate Logic

`POST /api/lk/conflict-check`

Input: `planned_action` -- one of:
`building_construction | foreign_contract | charity_event | property_investment | digital_launch | marriage_ritual | spiritual_retreat | multiple_remedies`

Map to conflict gate IDs 616-625. Return matching record with ke_inference (starts with `"⚠️ SAFETY GATE"`).

**Rule:** If conflict gate fires, UI must show full-screen interstitial BEFORE any remedy output. User must explicitly acknowledge before proceeding.

---

## 8. Karmic Debt Audit

`POST /api/lk/debt-audit`

1. Read `lk_user_profile.family_census`
2. Query IDs 601-615 from `knowledge_rules` where `science_id: "jyotish_lk_remedies"`
3. For each debt record, check if `blood_relation_target` relative is `"deceased"` or `"unknown"` → trigger `substitute_item` instead of primary ritual
4. Return: array of active debts with `{remedy_record, relative_available: bool, use_substitute: bool}`

---

## 9. 43-Day Tracker Rules (Enforced in Backend)

- **Binary cycle**: any day with `completed: false` → `status = "broken"`, `streak_days = 0`
- **Window validation**: `within_window` must be `true` (Sunrise-Sunset per user's city -- use Panchang engine `GET /api/panchang/daily`)
- **Reset cooling**: after break, 3-day wait before restart allowed
- **Post-43 audit**: when `streak_days >= 43` → `status = "complete"`, generate 2-question audit prompt

---

## 10. Frontend Pages

### `/lk-remedies` -- LK Remedies Home
- Intro card + Enter Birth Details CTA → triggers onboarding
- Free preview: Gate 1 summary only

### `/lk-remedies/onboard` -- 3-Step Wizard
- Step 1: Age + Natal Chart (house assignment grid, 9 planets × 12 houses)
- Step 2: Family Census (6 relatives, living/deceased/unknown toggle)
- Step 3: Location (reuse existing city picker from Panchang)

### `/lk-remedies/report` -- Diagnostic Report
- 5 gate sections in sequence (gate-by-gate reveal)
- Status badges: ⚠️ WARNING / 💤 DORMANT / ⚡ ACTIVE / 🔍 SCAN / ✅ CLEAR
- Execution Roadmap card at bottom
- "Add to 43-Day Tracker" button per remedy

### `/lk-remedies/tracker` -- 43-Day Progress
- Progress ring (Day X of 43)
- Phase label (Shift / Friction / Anchor / Lock)
- Daily check-in card: [✓ Ritual done] [✓ Within sunrise-sunset] [✓ Prohibited act avoided]
- Streak count + break alert

### `/lk-remedies/debt-audit` -- Karmic Debt
- Debt type cards (9 Pitra Rin types)
- Per-card: planet, house trigger, symptom list, relative required, remedy, substitute if unavailable
- "Ancestor Voice" narrative tone (solemn, elder-like language)

### `/lk-remedies/remedies` -- Browse Remedies
- Filter by: planet, house, severity, focus_area
- Card grid: remedy title, ritual summary, severity badge, "Start Tracker" CTA

---

## 11. Free vs Premium Gate

| Feature | Free | Premium (Razorpay subscription) |
|---|---|---|
| Onboarding | ✅ | ✅ |
| Gate 1 summary | ✅ | ✅ |
| Full 5-gate report | ❌ | ✅ |
| 43-Day Tracker | ❌ | ✅ |
| Debt Audit full | ❌ | ✅ |
| Conflict Gate check | ✅ (1 per day) | ✅ unlimited |
| Remedy browse | ✅ (limited) | ✅ full |

Paywall trigger: at Gate 2 output, at Tracker activation, at Debt Audit detail.

---

## 12. Theme & Style

Follow CLAUDE.md §11 Temple App Theme:
- `bg-background`, `bg-card`, `text-gold`, `border-gold/20`
- GlassCard: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`
- Status colors: WARNING=amber-500, DORMANT=blue-400, ACTIVE=emerald-500, CLEAR=emerald-400
- Sunrise/sunset timing from existing Panchang engine (no new dependency)

---

## 13. Files to Create

```
backend/
  lk_remedies_router.py     # All /api/lk/* routes
  lk_diagnostics.py         # 5-gate query engine logic

frontend/src/pages/
  LKRemediesPage.jsx        # Home + router
  LKOnboardPage.jsx         # 3-step wizard
  LKReportPage.jsx          # 5-gate diagnostic report
  LKTrackerPage.jsx         # 43-day progress
  LKDebtAuditPage.jsx       # Karmic debt cards
  LKBrowsePage.jsx          # Remedy browser
```

Register router in `backend/server.py`:
```python
from lk_remedies_router import router as lk_router
app.include_router(lk_router, prefix="/api/lk")
```

Add routes in `frontend/src/App.js` under `/lk-remedies/*`.

---

## 14. Key References

- `backend/scripts/verify_lk_remedies_v1.py` -- verification (12/12 PASS)
- `backend/scripts/master_test_query_lk.py` -- 5-gate test (4/4 PASS)
- `backend/panchang_router.py` -- sunrise/sunset for muhurta window
- `backend/vedic_calculator.py` -- birth chart computation (source of natal_chart input)
- `.claude/ingest/REMEDIES_PART_B_INGEST.md` -- full ID architecture
