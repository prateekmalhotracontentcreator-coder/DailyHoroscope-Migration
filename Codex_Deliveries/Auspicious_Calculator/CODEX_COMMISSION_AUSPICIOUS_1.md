# CODEX COMMISSION: AUSPICIOUS-1
## Auspicious / Inauspicious Day Calculator -- Dual-System Engine

> Commission ID: AUSPICIOUS-1
> Date: 2026-05-27
> Status: READY TO ISSUE
> Platform: EverydayHoroscope (https://www.everydayhoroscope.in)
> Thread: New Auspicious Calculator Thread

---

## 1. What We Are Building

A **Dual-System Auspicious Day Calculator** -- the only calculator in India that combines Vedic Muhurta (Panchang-based) and Chinese Tong Shu (Almanac-based) scoring into a single unified calendar output.

The user selects their intent (Career, Marriage, Property, etc.), their city, and optionally their birth date. The engine scores every day in the chosen month across both systems and returns a colour-coded calendar with top picks highlighted.

**Three modules:**

| Module | Location | Description |
|---|---|---|
| Module 1 -- Vedic Wizard | Frontend React | Intent + city + risk filter selection |
| Module 2 -- Chinese Wizard | Frontend React | Birth date + action vector + clash shield |
| Module 3 -- Calculation Engine IP | Backend FastAPI | pyswisseph Panchang + Chinese Day Officer scoring |

---

## 2. Architecture Rules (MANDATORY -- Read Before Writing Any Code)

### Rule A -- Legacy Model is the single source of truth

All live astronomical calculations **MUST** use `pyswisseph` via the existing `panchang_router.py` pattern. This project uses `backend/panchang_router.py` and `backend/vedic_calculator.py` as its production astronomy engines.

- **DO NOT** create a new astronomy engine from scratch. Re-use the existing `swe.calc_ut`, `swe.rise_trans`, and Lahiri Ayanamsa (`swe.set_sid_mode(swe.SIDM_LAHIRI)`) patterns already established in `backend/panchang_router.py`.
- Tithi, Nakshatra, Yoga, Vara (weekday) -- compute using the same formulas in `panchang_router.py`.
- Rahu Kalam, Abhijit Muhurta -- already computed in `panchang_router.py`; import and call those functions rather than rewriting.

### Rule B -- New files only; do not modify existing backend files

Deliver these new files:
```
backend/auspicious_router.py        # FastAPI router + endpoints
backend/auspicious_engine.py        # Scoring engine (Vedic + Chinese)
backend/auspicious_data.py          # Static rule matrices + JSON schemas
frontend/src/pages/auspicious/AuspiciousPage.jsx           # Main page wrapper
frontend/src/pages/auspicious/VedicWizard.jsx               # Module 1
frontend/src/pages/auspicious/ChineseWizard.jsx             # Module 2
frontend/src/pages/auspicious/AuspiciousCalendarGrid.jsx    # Module 3 UI
frontend/src/pages/auspicious/auspiciousApi.js              # API calls
```

**Do NOT modify:** `panchang_router.py`, `vedic_calculator.py`, `server.py`, `App.js`, `NavBar.jsx`, `vercel.json`, or any existing file.

### Rule C -- Theme alignment

Use the EverydayHoroscope gold/cream design system:
- Background: `bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.18),transparent_28%),linear-gradient(180deg,#fffaf0_0%,#f6eddc_52%,#efe3cd_100%)]`
- Gold accent: `text-gold`, `border-gold`, `bg-gold` (CSS var `--gold: #c5a059`)
- Cards: `rounded-[2rem] border border-gold/20 bg-white/80 shadow-sm`
- Text: `text-stone-900` (primary), `text-stone-600` (secondary)
- Font headings: `font-cinzel` or `font-playfair`
- GlassCard: `rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`

No dark backgrounds. No `bg-black/60`, `bg-neutral-900`, `text-white`. Replace all GAI brief dark-theme CSS with the cream/gold theme above.

---

## 3. Backend Specification

### 3.1 File: `backend/auspicious_engine.py`

#### Vedic Scoring

Use `panchang_router.py` patterns to compute for each day:
- `tithi_num` (1-30) -- (moon_long - sun_long) % 360 / 12 + 1
- `nakshatra_num` (1-27) -- moon_long / (360/27) + 1
- `vara` (1-7, 1=Sunday) -- from `datetime.isoweekday()`
- `yoga_num` (1-27) -- (sun_long + moon_long) % 360 / (360/27) + 1

Score each day using the **VEDIC_RULES matrix** (see Section 3.3). Apply blockers:
- Rikta Tithis (4, 9, 14): hard penalty except for `litigation` and `debt_clearance`
- Vyatipata / Vaidhriti Yoga (17, 27): reduce score by 20 points
- Vishti (Bhadra) Karana: flag as soft blocker

Return `vedic_score` (0-100) and `vedic_blockers` list.

#### Chinese Tong Shu Scoring

Implement the **12 Day Officers** using the solar-month Earthly Branch method:

```python
DAY_OFFICERS = [
    "Jian",   # Establish  -- good: job start, contracts
    "Chu",    # Remove     -- good: medical, debt clearance, legal
    "Man",    # Full       -- good: agriculture, harvest
    "Ping",   # Balance    -- neutral
    "Ding",   # Stable     -- good: property, investment, marriage
    "Zhi",    # Initiate   -- good: starting ventures
    "Po",     # Destruction -- bad for most; use only for demolition/debt
    "Wei",    # Danger     -- avoid for financial/legal
    "Cheng",  # Success    -- excellent for business launches
    "Shou",   # Receive    -- good: creative, receiving income
    "Kai",    # Open       -- excellent for education, travel, digital
    "Bi",     # Close      -- bad for most; use only for burials/endings
]
```

Officer cycle: `officer_index = (jd_day_number + month_branch_offset) % 12`

**Chinese Zodiac Clash** (Liu Chong -- 6 animal clashes):
```python
ZODIAC_CLASHES = {
    "Rat": "Horse", "Ox": "Goat", "Tiger": "Monkey",
    "Rabbit": "Rooster", "Dragon": "Dog", "Snake": "Pig",
    "Horse": "Rat", "Goat": "Ox", "Monkey": "Tiger",
    "Rooster": "Rabbit", "Dog": "Dragon", "Pig": "Snake"
}
```
Birth year → Chinese zodiac animal: `animals[(year - 4) % 12]`

If day animal = clash animal of user's birth animal AND `filter_personal_clash=True` → `is_blocked=True`, score = 10.

Return `chinese_score` (0-100) and `chinese_blockers` list.

#### Unified Score

```python
unified_score = round((vedic_score * 0.55) + (chinese_score * 0.45))
```

Tier:
- ≥ 80: `"excellent"` -- gold crown badge 👑
- 60-79: `"good"` -- green dot
- 40-59: `"neutral"` -- amber dot
- < 40 or `is_blocked=True`: `"blocked"` -- red tint

### 3.2 File: `backend/auspicious_router.py`

```python
router = APIRouter(prefix="/api/auspicious", tags=["Auspicious Calculator"])

GET  /api/auspicious/categories          # Returns all 10 categories with display names + Chinese mappings
POST /api/auspicious/calculate-month     # Body: VedicInput + ChineseInput → list of 28-31 day objects
GET  /api/auspicious/top-days            # Query: city_id, category, month, limit=5 → top picks only
```

**`POST /api/auspicious/calculate-month` -- Request body:**
```json
{
  "city_id": "new-delhi",
  "activity_category": "job_start",
  "target_month": "2026-06-01",
  "avoid_retrogrades": true,
  "birth_date": "1990-04-15",
  "activity_vector": "contract",
  "filter_personal_clash": true,
  "system": "dual"
}
```

**Response item (per day):**
```json
{
  "date": "2026-06-05",
  "day_name": "Friday",
  "vedic_score": 85,
  "chinese_score": 90,
  "unified_score": 87,
  "tier": "excellent",
  "is_blocked": false,
  "blockers": [],
  "vedic_details": {
    "tithi": 10, "tithi_name": "Dashami",
    "nakshatra": 12, "nakshatra_name": "Uttara Phalguni",
    "vara": 6, "vara_name": "Friday",
    "yoga": 5, "yoga_name": "Shobhana",
    "abhijit_muhurta": { "start": "12:02", "end": "12:50" },
    "rahu_kalam": { "start": "10:30", "end": "12:00" }
  },
  "chinese_details": {
    "day_officer": "Success (Cheng)",
    "day_animal": "Horse",
    "user_animal": "Horse",
    "is_personal_clash": false,
    "lunar_mansion": "Room (Fang)"
  },
  "recommendation": "Highly auspicious for contract signing and career moves."
}
```

### 3.3 File: `backend/auspicious_data.py`

Define the complete `VEDIC_RULES` dict and `CHINESE_RULES` dict as Python constants. These are the 10 categories:

```python
VEDIC_RULES = {
    "job_start": {
        "display_name": "💼 Corporate Job Entry & Contracts",
        "vara_good": [4, 5, 6],       # Wed=4, Thu=5, Fri=6 (1=Sun)
        "vara_neutral": [2],           # Mon
        "tithi_good": [2, 7, 10, 15],
        "tithi_neutral": [1, 3, 5, 11, 13],
        "tithi_blocked": [4, 9, 14],   # Rikta
        "nakshatra_good": [4, 12, 21, 27],  # Rohini, Uttara Phalguni, Uttara Ashadha, Revati
        "yoga_blocked": [17, 27],      # Vyatipata, Vaidhriti
        "chinese_officer_good": ["Jian", "Cheng", "Kai"],
        "chinese_officer_bad": ["Po", "Bi", "Wei"],
        "chinese_mansion": "Horn (Jiao)",
    },
    "real_estate": {
        "display_name": "🏠 Property & Land Registration",
        "vara_good": [3, 5, 6],       # Tue=3 (Mars=Bhoomi), Thu, Fri
        "vara_neutral": [5, 6],
        "tithi_good": [3, 5, 10, 11],
        "tithi_neutral": [1, 2, 6, 7],
        "tithi_blocked": [4, 9, 14],
        "nakshatra_good": [4, 5, 8],   # Rohini, Mrigashirsha, Pushya
        "yoga_blocked": [17, 27],
        "chinese_officer_good": ["Ding", "Cheng", "Man"],
        "chinese_officer_bad": ["Po", "Wei", "Bi"],
        "chinese_mansion": "Room (Fang)",
    },
    "love_marriage": {
        "display_name": "❤️ Engagement & Marital Rites",
        "vara_good": [2, 6],           # Mon, Fri (Venus)
        "vara_neutral": [1, 5],        # Sun, Thu
        "tithi_good": [5, 7, 13, 15],
        "tithi_neutral": [2, 3, 10, 11],
        "tithi_blocked": [4, 9, 14],
        "nakshatra_good": [4, 5, 15, 27],  # Rohini, Mrigashirsha, Swati, Revati
        "yoga_blocked": [17, 27],
        "chinese_officer_good": ["Cheng", "Ding", "Man"],
        "chinese_officer_bad": ["Po", "Bi"],
        "chinese_mansion": "Heart (Xin)",
    },
    "litigation": {
        "display_name": "⚖️ Legal Filings & Dispute Resolution",
        "vara_good": [3, 7],           # Tue, Sat
        "vara_neutral": [2],
        "tithi_good": [4, 9, 14],      # Rikta is good here
        "tithi_neutral": [6, 11],
        "tithi_blocked": [],           # No Tithi blockers for litigation
        "nakshatra_good": [2, 18, 18], # Bharani, Jyeshtha
        "yoga_blocked": [],
        "chinese_officer_good": ["Chu", "Po"],
        "chinese_officer_bad": ["Cheng", "Kai"],
        "chinese_mansion": "Net (Bi)",
    },
    "medical_surgery": {
        "display_name": "🩺 Elective Medical Procedures",
        "vara_good": [1, 5],           # Sun, Thu
        "vara_neutral": [3, 4],
        "tithi_good": [2, 6, 11],
        "tithi_neutral": [7, 12],
        "tithi_blocked": [15, 30],     # Full Moon / New Moon → bleeding risk
        "nakshatra_good": [1, 13, 22], # Ashwini, Hasta, Shravana
        "yoga_blocked": [17, 27],
        "chinese_officer_good": ["Chu", "Ping"],
        "chinese_officer_bad": ["Cheng", "Jian"],
        "chinese_mansion": "Pleiades (Mao)",
    },
    "digital_launch": {
        "display_name": "🚀 Software & Media Product Release",
        "vara_good": [4, 6],           # Wed (Mercury), Fri
        "vara_neutral": [5],
        "tithi_good": [5, 10, 15],
        "tithi_neutral": [2, 7, 11],
        "tithi_blocked": [4, 9, 14],
        "nakshatra_good": [6, 14, 24], # Ardra, Chitra, Shatabhisha
        "yoga_blocked": [17, 27],
        "chinese_officer_good": ["Kai", "Cheng"],
        "chinese_officer_bad": ["Po", "Bi", "Wei"],
        "chinese_mansion": "Roof (Wei)",
    },
    "agriculture": {
        "display_name": "🌱 Agriculture & New Cultivation",
        "vara_good": [2, 5],           # Mon (Moon), Thu
        "vara_neutral": [1, 4],
        "tithi_good": [1, 3, 8, 10],
        "tithi_neutral": [5, 7],
        "tithi_blocked": [4, 9, 14],
        "nakshatra_good": [4, 3, 17],  # Rohini, Krittika, Anuradha
        "yoga_blocked": [17, 27],
        "chinese_officer_good": ["Man", "Shou"],
        "chinese_officer_bad": ["Po", "Bi"],
        "chinese_mansion": "Willow (Liu)",
    },
    "debt_clearance": {
        "display_name": "🪙 Debt Settlement & Financial Closure",
        "vara_good": [3],              # Tue (Mars cuts debt)
        "vara_neutral": [7],
        "tithi_good": [4, 9],
        "tithi_neutral": [14],
        "tithi_blocked": [15, 30],     # Don't clear debt on Full/New Moon
        "nakshatra_good": [24, 13],    # Shatabhisha, Hasta
        "yoga_blocked": [],
        "chinese_officer_good": ["Po", "Chu"],
        "chinese_officer_bad": ["Cheng", "Man"],
        "chinese_mansion": "Ghost (Gui)",
    },
    "travel": {
        "display_name": "✈️ Long-Distance Travel & Logistics",
        "vara_good": [5, 6],           # Thu, Fri
        "vara_neutral": [4],
        "tithi_good": [2, 7, 11],
        "tithi_neutral": [3, 5],
        "tithi_blocked": [4, 9, 14],
        "nakshatra_good": [1, 7, 22, 27], # Ashwini, Punarvasu, Shravana, Revati
        "yoga_blocked": [17, 27],
        "chinese_officer_good": ["Kai", "Zhi"],
        "chinese_officer_bad": ["Po", "Bi", "Wei"],
        "chinese_mansion": "Astride (Kui)",
    },
    "creative_arts": {
        "display_name": "🎨 Creative Launch & Performance",
        "vara_good": [6],              # Fri (Venus)
        "vara_neutral": [2, 4],
        "tithi_good": [3, 5, 13],
        "tithi_neutral": [7, 10],
        "tithi_blocked": [4, 9, 14, 30], # Amavasya (dark moon) blocks creativity
        "nakshatra_good": [14, 11, 27],  # Chitra, Purva Phalguni, Revati
        "yoga_blocked": [17, 27],
        "chinese_officer_good": ["Shou", "Kai"],
        "chinese_officer_bad": ["Po", "Wei"],
        "chinese_mansion": "Bow (Zhang)",
    },
}
```

---

## 4. Frontend Specification

### 4.1 Page URL and Route

```
/auspicious-calculator
```

Component tree:
```
AuspiciousPage.jsx
  ├── Step 1: VedicWizard.jsx      (city + category + risk toggles)
  ├── Step 2: ChineseWizard.jsx    (birth date + action vector + clash shield)
  └── Step 3: AuspiciousCalendarGrid.jsx  (results calendar)
```

### 4.2 VedicWizard.jsx (Module 1)

3-step flow inside a single card:

1. **Intent selector** -- pill grid showing all 10 categories. Tap to select.
2. **City search** -- searchable dropdown from the app's 318-city catalogue. Uses `GET /api/panchang/locations`.
3. **Risk toggles** (2 switches):
   - "Filter Mercury Retrograde periods" (relevant for digital_launch, job_start, travel)
   - "Exclude Rahu Kalam from recommendations"

Button: `Calculate Vedic Auspicious Days →` → proceeds to ChineseWizard (or skips to results if user clicks "Vedic only").

### 4.3 ChineseWizard.jsx (Module 2)

1. **Birth date picker** -- day/month/year dropdowns. Shows derived Chinese zodiac animal as a badge (e.g., "🐉 Dragon").
2. **Action vector** -- 4 options: "Invest / Build / Marry", "Sign Contracts / Launch", "Medical / Cleansing / Release", "Travel / Explore"
3. **Clash Shield toggle** -- "Filter out my personal clash days" (default: ON)

Button: `Calculate Combined Auspicious Calendar →`

Optional skip: "Use Vedic system only" link that bypasses Chinese input.

### 4.4 AuspiciousCalendarGrid.jsx (Module 3 UI)

**Header row:** Month navigation (← / →), category badge, city badge, "Recalculate" button.

**Calendar grid** -- 7-column × 5-row (standard month layout):

Each day cell shows:
- Date number (large, `font-cinzel`)
- Tier indicator:
  - 👑 Gold border + gold shimmer = Excellent (unified ≥ 80)
  - Green dot = Good (60-79)
  - Amber dot = Neutral (40-59)
  - Red tint + ⚠️ = Blocked
- On hover/tap: expanded tooltip showing:
  - Tithi name + Nakshatra name
  - Day Officer (Chinese)
  - Vedic score / Chinese score
  - Blockers (if any)
  - Abhijit Muhurta window
  - Rahu Kalam window (shown in red)

**Top Picks section** (above calendar): 3 cards showing the top 3 days in the month. Each card:
- Large date number (`font-cinzel` 4xl)
- Day name + Tithi + Nakshatra
- Unified score badge (e.g., "92/100")
- "Why this day?" expandable -- 2-line reason
- Gold shimmer border

**Legend row** at bottom:
- 👑 Excellent (≥80) · 🟢 Good (60-79) · 🟡 Neutral (40-59) · 🔴 Blocked

### 4.5 Page SEO (AuspiciousPage.jsx)

```jsx
<SEO
  title="Auspicious Day Calculator -- Vedic & Chinese Muhurta | EverydayHoroscope"
  description="Find the most auspicious days for career moves, marriage, property purchase, travel and more. Combines Vedic Muhurta (Tithi/Nakshatra/Vara) with Chinese Tong Shu (Day Officers) for the most accurate dual-system guidance."
  url="https://www.everydayhoroscope.in/auspicious-calculator"
/>
```

JSON-LD Schema: `FAQPage` with 5 FAQ items about auspicious days, Muhurta, and the dual system.

---

## 5. Scoring Algorithm (Summary)

```
Vedic Score (0-100):
  Base = 40
  + 20 if vara in vara_good
  + 10 if vara in vara_neutral
  + 20 if tithi in tithi_good
  + 10 if tithi in tithi_neutral
  + 20 if nakshatra in nakshatra_good
  - 30 if tithi in tithi_blocked (for most categories)
  - 20 if yoga in yoga_blocked
  → clamp to [0, 100]

Chinese Score (0-100):
  Base = 60
  + 30 if day_officer in officer_good
  - 35 if day_officer in officer_bad
  = 10 (override) if personal animal clash + filter_personal_clash=True
  → clamp to [0, 100]

Unified Score = round(vedic * 0.55 + chinese * 0.45)

is_blocked = True if:
  - vedic: tithi_blocked AND category not in [litigation, debt_clearance]
  - chinese: day_officer in officer_bad AND officer is Po or Bi (hard reject)
  - chinese: personal animal clash AND filter_personal_clash=True
```

---

## 6. What Must NOT Be Built in This Commission

- No APScheduler cron pre-computation (Phase 2 feature)
- No NASA Space Weather API integration (Phase 2 feature)
- No QRNG / quantum entropy features (future enhancement)
- No GIS/tectonic data integration (future enhancement)
- No user birth chart personalisation beyond Chinese zodiac animal (future)
- No MongoDB writes -- this is a **stateless calculation API** (no caching required in Phase 1)

---

## 7. Delivery Checklist

- [ ] `backend/auspicious_engine.py` -- Vedic + Chinese scoring engine
- [ ] `backend/auspicious_data.py` -- All 10 VEDIC_RULES + CHINESE_RULES constants
- [ ] `backend/auspicious_router.py` -- 3 endpoints (categories, calculate-month, top-days)
- [ ] `frontend/src/pages/auspicious/AuspiciousPage.jsx` -- Page wrapper + SEO + JSON-LD
- [ ] `frontend/src/pages/auspicious/VedicWizard.jsx` -- Module 1 (3-step intent/city/toggle)
- [ ] `frontend/src/pages/auspicious/ChineseWizard.jsx` -- Module 2 (birth date + vector + clash)
- [ ] `frontend/src/pages/auspicious/AuspiciousCalendarGrid.jsx` -- Module 3 calendar UI
- [ ] `frontend/src/pages/auspicious/auspiciousApi.js` -- `fetchCategories()`, `calculateMonth()`, `fetchTopDays()`
- [ ] All 10 activity categories present in VEDIC_RULES
- [ ] Day cell shows Tithi name + Nakshatra name (not just numbers)
- [ ] Top Picks section shows top 3 days with unified score
- [ ] Gold/cream theme -- no dark backgrounds (`bg-black`, `bg-neutral-900`, `text-white`)
- [ ] `python3 -m py_compile backend/auspicious_engine.py auspicious_data.py auspicious_router.py` → PASS
- [ ] `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` → PASS (0 errors)
- [ ] No modifications to any existing file

---

## 8. Integration Note (Temple Team Will Handle)

After delivery, Temple Team will:
1. Add `from auspicious_router import router as auspicious_router` + `app.include_router(auspicious_router)` to `backend/server.py`
2. Add route `{ path: '/auspicious-calculator', element: <AuspiciousPage /> }` to `frontend/src/App.js`
3. Add "Auspicious Calculator" entry to the "Free Calculators" NavBar dropdown

**Codex: do NOT modify server.py, App.js, or NavBar.jsx.**

---

## 9. Reference Files (Read These Before Starting)

Study these existing files for patterns to follow:
- `backend/panchang_router.py` -- pyswisseph computation pattern (swe.calc_ut, Lahiri Ayanamsa, Tithi/Nakshatra/Yoga formulas)
- `frontend/src/pages/angel-numbers/AngelNumbersHubPage.jsx` -- gold/cream UI style reference
- `frontend/src/pages/angel-numbers/angelNumbersApi.js` -- API call pattern to follow

---

*Commission prepared by Temple Team -- EverydayHoroscope, 2026-05-27*
