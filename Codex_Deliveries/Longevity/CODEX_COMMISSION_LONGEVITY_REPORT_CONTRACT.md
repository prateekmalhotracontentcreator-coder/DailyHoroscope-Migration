# Contract: Ayur Jyotish -- Longevity & Health Analysis Report
> Client: EverydayHoroscope (SkyHound Studios)
> Platform: https://www.everydayhoroscope.in
> Backend: FastAPI on Render · Frontend: React 18 on Vercel
> Repo: github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration
> Astronomy Engine: pyswisseph 2.10.x (Lahiri ayanamsa, Swiss Ephemeris)

---

## 1. Module Overview

Build a **premium Longevity & Health Analysis Report** ("Ayur Jyotish") that combines two
complementary astrological systems to produce a comprehensive life-health narrative:

| System | Role | Priority |
|---|---|---|
| **KP (Krishnamurti Paddhati)** Astrology | Primary analysis engine -- sub-lord theory for precise house signification | 1st |
| **Traditional Vedic (Parashari)** Astrology | Supporting layer -- classical drishti, yogas, dasha context | 2nd |

**What the report covers (7 sections):**
1. Longevity Classification (Alpayu / Madhyayu / Poornayu)
2. Constitutional Health Profile (Prakriti mapping from planetary Nadi)
3. Vulnerable Body Systems & Organs (house-sign-planet mapping)
4. Disease Susceptibility Windows (Dasha × Transit triggers)
5. Critical Period Alerts (Maraka dasha, 22nd Drekkana, 64th Navamsa)
6. Remedial & Preventive Guidance (gemstones, mantras, lifestyle)
7. Quality of Life Forecast (decadal outlook across health, vitality, mental wellness)

**Monetisation:** This is a **premium-gated** report (Pro tier, ₹499/mo or one-time ₹999).

---

## 2. KP Astrology Engine -- Backend Additions

### 2a. New file: `backend/kp_engine.py`

KP extends the existing Vedic chart with **sub-lord theory**. For each of the 12 house cusps
and 9 planets, compute:

#### KP Sub-Lord Chain
```
Cusp/Planet longitude (sidereal, Lahiri)
  → Sign Lord (rashi adhipati)
    → Star Lord (nakshatra adhipati -- 1 of 27 nakshatras)
      → Sub-Lord (subdivide nakshatra by Vimshottari dasha proportions)
```

**Sub-Lord Calculation Algorithm:**
1. Each nakshatra spans 13°20' (800').
2. Divide this span into 9 unequal sub-divisions proportional to Vimshottari Dasha years:
   - Ketu: 7/120, Venus: 20/120, Sun: 6/120, Moon: 10/120, Mars: 7/120,
     Rahu: 18/120, Jupiter: 16/120, Saturn: 19/120, Mercury: 17/120
3. The sub-lord is the planet whose sub-division contains the longitude.
4. Optionally compute Sub-Sub-Lord (same recursive subdivision within the sub).

**Required functions:**
```python
def compute_kp_sublord(longitude_deg: float) -> dict:
    """
    Returns: {
        "sign_lord": "Mars",
        "star_lord": "Ketu",
        "sub_lord": "Venus",
        "sub_sub_lord": "Saturn",  # optional depth
        "nakshatra": "Ashwini",
        "pada": 2,
        "sub_index": 1,
        "longitude": 4.5678
    }
    """

def compute_kp_cusps(jd_ut: float, lat: float, lon: float) -> list[dict]:
    """
    Compute Placidus house cusps (KP uses Placidus, not equal-house).
    For each of 12 cusps, return sign_lord, star_lord, sub_lord.
    Uses swe.houses() with Placidus system.
    """

def get_kp_significators(planet: str, kp_cusps: list, kp_planets: list) -> dict:
    """
    For a given planet, determine which houses it signifies:
      Level 1: Houses the planet occupies (by star lord's owned houses)
      Level 2: Houses the planet owns
      Level 3: Houses aspected by the planet (Vedic drishti)
      Level 4: Star lord's significations (recursive)
    Returns: { "level_1": [8, 12], "level_2": [1, 6], ... }
    """
```

#### KP Longevity Rules (codified)
```python
LONGEVITY_RULES = {
    "alpayu": {
        "description": "Short life (0-32 years)",
        "conditions": [
            "Sub-lord of 8th cusp signifies 1, 2, 7 (maraka houses) without 5, 9, 11",
            "Sub-lord of Lagna cusp signifies 6, 8, 12 strongly",
            "Saturn + Mars afflict 8th without Jupiter aspect"
        ]
    },
    "madhyayu": {
        "description": "Medium life (33-66 years)",
        "conditions": [
            "Sub-lord of 8th cusp signifies mix of benefic + malefic houses",
            "8th house has both benefic and malefic connections"
        ]
    },
    "poornayu": {
        "description": "Full life (67-100+ years)",
        "conditions": [
            "Sub-lord of 8th cusp signifies 5, 9, 11 (fortune houses)",
            "8th lord well-placed, Jupiter aspects 8th or Lagna",
            "Strong Lagna lord in kendra/trikona"
        ]
    }
}
```

### 2b. Health Mapping Tables

```python
# Sign → Body Part (Kaal Purush mapping)
SIGN_BODY_MAP = {
    "Aries": ["Head", "Brain", "Eyes", "Face"],
    "Taurus": ["Throat", "Neck", "Thyroid", "Vocal cords"],
    "Gemini": ["Arms", "Shoulders", "Lungs", "Nervous system"],
    "Cancer": ["Chest", "Breast", "Stomach", "Uterus"],
    "Leo": ["Heart", "Spine", "Upper back", "Blood circulation"],
    "Virgo": ["Intestines", "Digestive system", "Pancreas", "Lower abdomen"],
    "Libra": ["Kidneys", "Lower back", "Adrenal glands", "Skin"],
    "Scorpio": ["Reproductive organs", "Bladder", "Colon", "Prostate"],
    "Sagittarius": ["Hips", "Thighs", "Liver", "Sciatic nerve"],
    "Capricorn": ["Knees", "Bones", "Joints", "Teeth"],
    "Aquarius": ["Ankles", "Calves", "Circulatory system", "Shins"],
    "Pisces": ["Feet", "Lymphatic system", "Immune system", "Sleep disorders"]
}

# Planet → Disease Domain
PLANET_DISEASE_MAP = {
    "Sun": ["Heart disease", "Eye problems", "Bone disorders", "Vitality loss"],
    "Moon": ["Mental health", "Fluid retention", "Hormonal imbalance", "Insomnia"],
    "Mars": ["Accidents", "Inflammation", "Blood disorders", "Surgical conditions"],
    "Mercury": ["Nervous disorders", "Skin disease", "Speech issues", "Anxiety"],
    "Jupiter": ["Liver disease", "Obesity", "Diabetes", "Tumors (benign)"],
    "Venus": ["Reproductive disorders", "Kidney disease", "Diabetes", "STDs"],
    "Saturn": ["Chronic disease", "Arthritis", "Depression", "Degenerative conditions"],
    "Rahu": ["Mysterious illness", "Poisoning", "Phobias", "Misdiagnosis"],
    "Ketu": ["Sudden ailments", "Surgical events", "Spiritual crises", "Viral infections"]
}

# House → Health Domain
HOUSE_HEALTH_MAP = {
    1: "General vitality, physical constitution, immunity",
    2: "Right eye, face, oral health, diet & nutrition",
    3: "Arms, ears, shoulders, mental courage",
    5: "Stomach, mind, emotional health, progeny-related",
    6: "Disease (primary house), enemies, debts, daily illness",
    7: "Lower abdomen, reproductive, urinary tract",
    8: "Chronic illness, longevity, surgery, death-like experiences",
    11: "Left ear, calves, recovery from illness",
    12: "Hospitalisation, feet, sleep disorders, expenses on health"
}
```

### 2c. Critical Period Detection

```python
def detect_critical_periods(chart: dict, dashas: list) -> list[dict]:
    """
    Scan Vimshottari Maha + Antar dashas and flag periods where:
    1. Dasha lord is a Maraka (lord of 2nd or 7th)
    2. Dasha lord is Badhaka (obstruction lord per moveable/fixed/dual lagna)
    3. Current transit Saturn/Rahu over natal 8th or Lagna
    4. 22nd Drekkana lord's dasha
    5. 64th Navamsa lord's dasha
    
    Returns list of:
    {
        "period": "Saturn Maha / Mars Antar",
        "start": "2028-06-15",
        "end": "2029-07-20",
        "severity": "high" | "moderate" | "low",
        "trigger": "Maraka + transit Saturn over 8th",
        "body_systems": ["Bones", "Joints", "Blood pressure"],
        "advisory": "Preventive health screening recommended. Avoid risky activities."
    }
    """
```

### 2d. New router: `backend/longevity_router.py`

Register at prefix `/api/longevity` in `server.py`.

#### Endpoint 1 -- Generate Longevity Report
```
POST /api/longevity/report
Auth: Required (Pro tier)
```
Request:
```json
{
  "date": "1990-06-15",
  "time": "14:30",
  "latitude": 19.076,
  "longitude": 72.8777,
  "timezone": "Asia/Kolkata",
  "city_name": "Mumbai"
}
```

Response: See Section 4 (full schema).

#### Endpoint 2 -- Save Report
```
POST /api/longevity/save
Auth: Required
```
Saves encrypted report to MongoDB collection `longevity_reports`.

#### Endpoint 3 -- My Reports
```
GET /api/longevity/my-reports
Auth: Required
```

#### Endpoint 4 -- Health Alerts (lightweight)
```
GET /api/longevity/alerts?user_id=xxx
Auth: Required
```
Returns only active/upcoming critical period alerts for dashboard widgets.

---

## 3. AI Interpretation Layer

After the deterministic KP + Vedic calculations, pass the structured data to Claude API
for narrative generation. This transforms raw astrological data into a readable health report.

### Prompt Architecture
```python
LONGEVITY_SYSTEM_PROMPT = """
You are an expert Vedic and KP astrologer specialising in medical astrology (Ayur Jyotish).
You are writing a professional health analysis report for a client.

RULES:
1. Never diagnose. Use language like "susceptibility", "vulnerability", "tendencies".
2. Always recommend consulting qualified medical professionals.
3. Frame findings as "astrological indications" not medical facts.
4. Be compassionate -- avoid alarmist language for critical periods.
5. Include remedial measures (gemstone, mantra, lifestyle) for every risk area.
6. Respect that this is a belief system -- present with dignity and scholarship.
"""

LONGEVITY_USER_PROMPT = """
Generate a detailed Ayur Jyotish (Longevity & Health) report from this chart data:

Birth: {date} at {time}, {city} ({lat}, {lon})
Lagna: {lagna_sign} at {lagna_degree}°, Nakshatra: {lagna_nakshatra}

KP Analysis:
- 8th Cusp Sub-Lord: {eighth_sublord} → Signifies houses: {eighth_significations}
- 6th Cusp Sub-Lord: {sixth_sublord} → Signifies houses: {sixth_significations}
- Lagna Cusp Sub-Lord: {lagna_sublord} → Signifies houses: {lagna_significations}

Longevity Class: {longevity_class} ({longevity_reasoning})

Vulnerable Systems: {vulnerable_systems_json}
Critical Periods: {critical_periods_json}
Current Dasha: {current_dasha}

Vedic Yogas Present: {yogas_list}
Planetary Dignities: {dignities_json}

Write the report with these 7 sections:
1. Longevity Overview
2. Constitutional Health Profile
3. Vulnerable Body Systems
4. Disease Susceptibility Windows
5. Critical Period Alerts
6. Remedial & Preventive Guidance
7. Quality of Life Forecast (decade-wise)

Use warm, professional tone. 1500-2500 words.
"""
```

---

## 4. API Response Schema

```json
{
  "report_id": "uuid",
  "input": { /* birth details */ },
  "kp_analysis": {
    "cusps": [
      {
        "cusp_num": 1,
        "longitude": 187.45,
        "sign": "Libra",
        "sign_lord": "Venus",
        "star_lord": "Rahu",
        "sub_lord": "Jupiter",
        "significations": [1, 5, 9]
      }
      /* ... 12 cusps */
    ],
    "planet_sublords": [
      {
        "planet": "Sun",
        "longitude": 61.45,
        "sign_lord": "Mercury",
        "star_lord": "Mars",
        "sub_lord": "Saturn",
        "house_significations": { "level_1": [8], "level_2": [11], "level_3": [2, 6] }
      }
      /* ... 9 planets */
    ]
  },
  "longevity": {
    "classification": "Poornayu",
    "range": "67-100+ years",
    "confidence": "strong",
    "reasoning": "Sub-lord of 8th cusp (Jupiter) signifies 5, 9, 11. Lagna lord strong in kendra."
  },
  "health_profile": {
    "prakriti": "Pitta-Vata",
    "dominant_element": "Fire",
    "constitutional_strengths": ["Strong immunity", "Good digestion"],
    "constitutional_weaknesses": ["Prone to inflammation", "Nervous tension"]
  },
  "vulnerable_systems": [
    {
      "body_system": "Heart & Cardiovascular",
      "risk_level": "moderate",
      "astrological_basis": "Sun in 8th house, Leo sign afflicted by Saturn aspect",
      "planets_involved": ["Sun", "Saturn"],
      "houses_involved": [5, 8],
      "preventive_notes": "Regular cardiac screening after age 45"
    }
  ],
  "critical_periods": [
    {
      "period": "Saturn Maha / Mars Antar",
      "start": "2028-06-15",
      "end": "2029-07-20",
      "severity": "moderate",
      "trigger": "Maraka lord dasha + transit Saturn over natal Moon",
      "body_systems": ["Bones", "Blood pressure"],
      "advisory": "Recommended: preventive health screening, avoid risky travel"
    }
  ],
  "remedial_guidance": {
    "gemstones": [
      { "stone": "Yellow Sapphire", "planet": "Jupiter", "finger": "Index", "metal": "Gold", "weight_ct": 3.0 }
    ],
    "mantras": [
      { "mantra": "Om Brim Brihaspataye Namah", "planet": "Jupiter", "count": 108, "day": "Thursday" }
    ],
    "lifestyle": [
      "Morning sun exposure 15 min (Surya Namaskar)",
      "Avoid non-vegetarian food on Saturdays",
      "Pranayama daily -- Anulom Vilom 10 min"
    ],
    "charitable": [
      { "action": "Donate yellow lentils on Thursday", "planet": "Jupiter" }
    ]
  },
  "narrative": "/* Claude-generated 1500-2500 word report (7 sections) */",
  "meta": {
    "engine": "kp-engine-v1 + vedic-calculator",
    "ayanamsa": "Lahiri",
    "house_system": "Placidus (KP)",
    "computed_at": "2026-04-08T10:00:00Z"
  }
}
```

---

## 5. Frontend Deliverables

### File: `frontend/src/pages/LongevityReportPage.jsx`

Route: `/longevity`

#### 5a. Landing / Input Section
- Same birth details form as Kundali (date/time/city)
- Hero section: "Ayur Jyotish -- Your Vedic Health & Longevity Analysis"
- Feature preview cards (7 sections shown as locked cards for free users)
- "Generate Report" CTA → Pro paywall gate if not subscribed
- Trust signals: "Powered by KP + Vedic Astrology", "Swiss Ephemeris precision"

#### 5b. Report Display (7-section layout)

**Section 1 -- Longevity Overview**
- Classification badge (Alpayu / Madhyayu / Poornayu) with color coding
- KP reasoning summary in a callout box
- Confidence indicator (strong / moderate / indicative)

**Section 2 -- Constitutional Health Profile**
- Prakriti badge (Vata / Pitta / Kapha combination)
- Strengths (green) vs Weaknesses (amber) two-column layout
- Dominant element icon

**Section 3 -- Vulnerable Body Systems**
- Cards per system, color-coded by risk (green/amber/red)
- Each card: body system name, risk badge, astrological basis (collapsible), planets & houses
- Body silhouette SVG with highlighted zones (optional Phase 2)

**Section 4 -- Disease Susceptibility Windows**
- Timeline visualisation (horizontal bar chart)
- Each bar = a dasha period, color = risk level
- Hover/tap for details
- "Active Now" indicator if current period has alerts

**Section 5 -- Critical Period Alerts**
- Card per alert, sorted by date
- Severity badge (High = red, Moderate = amber, Low = green)
- Expandable: trigger reasoning, body systems, advisory text
- Calendar export button (.ics) for high-severity alerts

**Section 6 -- Remedial Guidance**
- 4-tab sub-nav: Gemstones / Mantras / Lifestyle / Charitable
- Each tab: card list with actionable items
- Gemstone cards: image placeholder, finger, metal, weight

**Section 7 -- Quality of Life Forecast**
- Decade-wise cards (20s / 30s / 40s / 50s / 60s / 70s+)
- Each: health vitality score (1-10), key themes, dasha context

**Full Narrative Section**
- Collapsible "Read Full Report" at bottom
- Claude-generated prose, rendered as markdown
- Print / PDF / Share buttons

#### 5c. Share & Save
- "Save Report" button (requires login)
- Share card generation (LongevityShareCard) -- summary version
- ShareButtons (WhatsApp/Facebook/X/Save)

#### 5d. Disclaimer
Persistent footer disclaimer on report page:
> "This report is based on astrological calculations and traditional Vedic/KP principles.
> It is not a substitute for professional medical advice, diagnosis, or treatment.
> Always consult qualified healthcare providers for medical decisions."

---

## 6. SEO Requirements

Routes:
- `/longevity` -- landing + input form
- `/longevity/report/:reportId` -- saved report view (auth-gated)

SEO for landing:
- Title: "Ayur Jyotish -- Vedic Longevity & Health Report | Everyday Horoscope"
- Description: "Get your personalised longevity and health analysis using KP & Vedic astrology. Discover vulnerable body systems, critical periods, and remedial guidance."
- JSON-LD: `SoftwareApplication` schema

---

## 7. Technical Constraints

- pyswisseph `swe.houses()` with `b'P'` (Placidus) for KP cusp calculation
- Sub-lord computation is pure math -- no new Python dependencies needed
- Claude API call for narrative: use existing `anthropic` client in `server.py`
- Claude model: `claude-sonnet-4-6` for interpretation (cost-effective for report generation)
- MongoDB collection: `longevity_reports` (encrypted if Commission C is deployed)
- Report generation target: < 10s total (< 500ms calculation + < 8s Claude API)
- **Medical disclaimer** must appear on every report view -- non-removable

---

## 8. Acceptance Criteria

- [ ] KP sub-lord calculation verified for 3 known charts against established KP software
- [ ] Placidus cusps match within ±0.1° of standard KP ephemeris
- [ ] Longevity classification logic produces correct result for 5 test cases
- [ ] Critical period detection flags known Maraka dashas correctly
- [ ] Claude narrative generates in < 8s, reads as professional medical astrology
- [ ] Report page renders correctly at 320px and 800px width
- [ ] Pro paywall gate blocks free users; unlocks correctly for Pro subscribers
- [ ] Medical disclaimer is visible and non-removable
- [ ] Works on iOS Safari and Chrome Android

---

## 9. Dependencies on Other Commissions

| Dependency | Status | Impact |
|---|---|---|
| Commission C (AES-256 Encryption) | Optional | If deployed, reports auto-encrypt at save |
| Commission D (Razorpay Paywall) | Required for monetisation | Pro tier gate; can ship report without paywall initially |
| Existing `vedic_calculator.py` | ✅ Available | Reuse planet positions, Dasha calculations, Nakshatra data |

---

## 10. Estimated Effort

| Component | Hours |
|---|---|
| `kp_engine.py` -- Sub-lord + cusp + significator engine | 8h |
| Health mapping tables + longevity classification | 4h |
| Critical period detection algorithm | 5h |
| `longevity_router.py` -- API endpoints | 4h |
| Claude prompt engineering + narrative pipeline | 4h |
| Frontend: LongevityReportPage (7 sections) | 10h |
| Frontend: Timeline visualisation + risk cards | 5h |
| Share card + SEO + JSON-LD | 3h |
| Testing + validation against KP reference charts | 5h |
| **Total** | **~48h** |
