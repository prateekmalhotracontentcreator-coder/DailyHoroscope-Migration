# Codex Commission Brief -- Shadbala Engine
**Commission type:** Backend engine (Python)
**Target file:** `backend/vedic_calculator.py`
**Estimated output:** ~300-400 lines of pure Python
**Status:** Ready for Codex -- all dependencies documented below

---

## Context

EverydayHoroscope uses a Vedic astrology backend built on `pyswisseph` (Swiss Ephemeris Python binding). The birth chart computation lives in `backend/vedic_calculator.py`. A planet strength quick-win module has already been added (dignity + combustion, commit `4ce54b4`). This commission extends it with the full Parashari Shadbala (six-strength) engine.

**Do NOT touch:** `backend/knowledge_engine.py`, `backend/server.py`, `backend/panchang_router.py`, or any frontend files. Changes are confined entirely to `backend/vedic_calculator.py` (and a new test file).

---

## What Already Exists (do not duplicate)

In `backend/vedic_calculator.py` the following are already defined:

```python
SIGN_ORDER   # list of 12 sign names, Aries first
SIGN_LORDS   # dict: sign → ruling planet (plain name: 'Mars', 'Venus', etc.)
EXALTATION_DATA   # dict: planet → (exaltation_sign, exact_degree)
DEBILITATION_SIGNS  # dict: planet → debilitation_sign
MOOLATRIKONA_DATA   # dict: planet → (mt_sign, start_deg, end_deg)
OWN_SIGNS           # dict: planet → [list of own signs]
_FRIENDS / _ENEMIES # Parashari friendship tables
COMBUSTION_ORBS     # dict: planet → combustion orb in degrees
get_planet_dignity(planet, sign, degree) → str
is_planet_combust(planet, planet_lon, sun_lon) → bool
```

Planet names throughout the codebase use plain English: `'Sun'`, `'Moon'`, `'Mars'`, `'Mercury'`, `'Jupiter'`, `'Venus'`, `'Saturn'`, `'Rahu'`, `'Ketu'`.

The `_calc_planet(jd, swe_id)` helper already exists and returns `(longitude, speed)` in sidereal degrees using Lahiri ayanamsa.

---

## Task

Implement `calculate_shadbala(planets, jd, lat, lon)` -- a function that computes the Parashari Shadbala (six-strength) scores for all 7 classical planets.

### Function signature

```python
def calculate_shadbala(
    planets: dict[str, dict],   # output of the existing birth chart planet loop
                                # each planet dict has: sign, degree, house, retrograde, dignity
    jd: float,                  # Julian Day of birth (already computed in calculate_birth_chart)
    lat: float,                 # birth latitude
    lon: float,                 # birth longitude (geographic)
) -> dict[str, dict]:
    """
    Returns a dict keyed by plain planet name (Sun/Moon/.../Saturn).
    Each value is a dict:
    {
        "sthana_bala":     float,   # Positional strength in Shashtiamsas
        "dig_bala":        float,   # Directional strength in Shashtiamsas
        "kala_bala":       float,   # Temporal strength in Shashtiamsas
        "chesta_bala":     float,   # Motional strength in Shashtiamsas
        "naisargika_bala": float,   # Natural strength in Shashtiamsas
        "drik_bala":       float,   # Aspectual strength in Shashtiamsas
        "total":           float,   # Sum of all six
        "total_rupas":     float,   # total / 60  (Rupas = Shashtiamsas / 60)
        "minimum_rupas":   float,   # required minimum (planet-specific, see below)
        "is_strong":       bool,    # total_rupas >= minimum_rupas
    }
    """
```

### Rahu and Ketu

Do NOT compute Shadbala for Rahu and Ketu -- they are not classical Graha and have no defined Shadbala. Return an empty dict `{}` for them or omit them from the output entirely.

---

## Six Components -- Implementation Specification

### 1. Sthana Bala (Positional Strength)

Five sub-components, all in Shashtiamsas:

**a. Uchcha Bala** (Exaltation Strength)
- Planet at exact exaltation degree → 60 Shashtiamsas
- Planet at exact debilitation degree → 0 Shashtiamsas
- Interpolate linearly between the two based on angular distance from debilitation
- Formula: `uchcha_bala = (180 - |planet_lon - debi_lon|) / 3`  
  where `|planet_lon - debi_lon|` is the shortest arc (max 180°)
- Clamp result to [0, 60]

Exaltation longitudes (absolute ecliptic, sidereal):
```
Sun: 10° Aries = 10°    Moon: 3° Taurus = 33°   Mars: 28° Capricorn = 268°
Mercury: 15° Virgo = 165°  Jupiter: 5° Cancer = 95°  Venus: 27° Pisces = 357°
Saturn: 20° Libra = 200°
```
Debilitation = exaltation + 180° (mod 360°).

**b. Moolatrikona Bala**
- Planet in its Moolatrikona sign → 45 Shashtiamsas
- Otherwise → 0
- Use `MOOLATRIKONA_DATA` already defined

**c. Own-Sign Bala (Swakshetra Bala)**
- Planet in own sign (not Moolatrikona portion) → 30 Shashtiamsas
- Planet in Moolatrikona portion → 0 (already counted above)
- Otherwise → 0

**d. Trigonasthana / Ojayugma Rasyamsa Bala** (Odd/Even sign strength)
- Sun, Jupiter, Mars: +15 Shashtiamsas if in odd sign (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius)
- Moon, Venus: +15 if in even sign (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces)
- Mercury, Saturn: +15 regardless of sign
- For navamsa (D9): compute D9 sign from planet longitude. Same odd/even rule, same +15 bonus.
  D9 sign: `navamsa_index = int(planet_lon_from_sign_start * 9 / 30)`, then offset from sign's triplicity group.
  Simplified: `d9_sign_index = (sign_index * 9 + navamsa_position) % 12`
  where `navamsa_position = int((planet_lon % 30) / (30/9))`

**e. Kendradi Bala** (Angular/Succedent/Cadent strength)
- Planet in angular house (1, 4, 7, 10) → 60 Shashtiamsas
- Planet in succedent house (2, 5, 8, 11) → 30 Shashtiamsas
- Planet in cadent house (3, 6, 9, 12) → 15 Shashtiamsas

**Sthana Bala total** = Uchcha + Moolatrikona + Own-Sign + Ojayugma + Kendradi

---

### 2. Dig Bala (Directional Strength)

Each planet has a house of maximum directional strength (full Dig Bala = 60 Shashtiamsas):

```python
DIG_BALA_HOUSE = {
    'Sun': 10, 'Mars': 10,        # strong in 10th
    'Mercury': 1, 'Jupiter': 1,   # strong in 1st
    'Moon': 4, 'Venus': 4,        # strong in 4th
    'Saturn': 7,                  # strong in 7th
}
```

Weak house = opposite (strong_house + 6, wrapping around 12):
```
strong=10 → weak=4,  strong=1 → weak=7,  strong=4 → weak=10,  strong=7 → weak=1
```

Formula: compute angular distance between planet's actual house cusp (in degrees from Ascendant) and the strong-house cusp. Full formula using house cusps:

```
planet_deg_from_asc = (planet_lon - asc_lon) % 360
strong_house_deg = (strong_house - 1) * 30   # whole-sign approximation
weak_house_deg   = (weak_house   - 1) * 30

arc_from_weak = (planet_deg_from_asc - weak_house_deg) % 360
dig_bala = arc_from_weak / 3   # convert 0-360° arc to 0-120 Shashtiamsas... 
# then clamp: if > 60, use 120 - dig_bala (planet approaching weak from other side)
dig_bala = min(dig_bala, 120 - dig_bala)
dig_bala = max(0, min(60, dig_bala))
```

Simpler whole-sign implementation is acceptable:
```
distance_from_strong = |planet_house - strong_house| (shortest path around 12)
dig_bala = (6 - distance_from_strong) * 10  # 6 steps = 0, 0 steps = 60
clamp to [0, 60]
```

---

### 3. Kala Bala (Temporal Strength)

Nine sub-components. All values in Shashtiamsas.

**a. Nathonnatha Bala** (Day/Night strength)
- Day planets (Sun, Jupiter, Venus): 60 during day (sunrise to sunset), 0 at night
- Night planets (Moon, Mars, Saturn): 60 at night, 0 during day
- Mercury: always 60
- Day = birth JD is between sunrise and sunset JD for birth location
- Use `swe.rise_trans()` to get sunrise/sunset for birth JD, lat, lon

**b. Paksha Bala** (Lunar phase strength)
- Moon's elongation from Sun = `(moon_lon - sun_lon) % 360`
- If elongation ≤ 180° (waxing / Shukla Paksha): benefics (Moon, Mercury, Jupiter, Venus) get `elongation / 3` Shashtiamsas; malefics (Sun, Mars, Saturn) get `(180 - elongation) / 3`
- If elongation > 180° (waning / Krishna Paksha): reverse. Malefics get `(elongation - 180) / 3`; benefics get `(360 - elongation) / 3`
- All values clamp to [0, 60]

**c. Tribhaga Bala** (Three-part day/night strength)
- Divide daytime into 3 equal parts; divide nighttime into 3 equal parts
- Part 1 of day → Jupiter gets 60; Part 2 of day → Sun gets 60; Part 3 of day → Saturn gets 60
- Part 1 of night → Moon gets 60; Part 2 of night → Venus gets 60; Part 3 of night → Mars gets 60
- Mercury always gets 60
- All other planets in each period → 0

**d. Abda Bala** (Year lord) -- 15 Shashtiamsas
- Solar year lord = lord of the weekday of the Mesha Sankranti (Sun entering Aries) before birth
- The planet that is lord of the Solar New Year day gets 15 Shashtiamsas; others get 0
- Simplified: compute the Julian Day of the Mesha Sankranti preceding birth, find weekday, assign lord
- Weekday lords: Sun=Sunday, Moon=Monday, Mars=Tuesday, Mercury=Wednesday, Jupiter=Thursday, Venus=Friday, Saturn=Saturday

**e. Masa Bala** (Month lord) -- 30 Shashtiamsas
- Lord of the lunar month (masa) at birth → 30 Shashtiamsas; others → 0
- Lunar month lord = lord of the weekday at the start of the current lunar month (Amavasya/New Moon preceding birth)

**f. Vara Bala** (Weekday lord) -- 45 Shashtiamsas
- Lord of the weekday of birth → 45 Shashtiamsas; others → 0
- Weekday from JD: `weekday = int(jd + 1.5) % 7` where 0=Monday
  Adjust: Sun=0(Sun), Mon=1(Moon), Tue=2(Mars), Wed=3(Mercury), Thu=4(Jupiter), Fri=5(Venus), Sat=6(Saturn)

**g. Hora Bala** (Hora lord) -- 60 Shashtiamsas
- Each hour of the day is ruled by a planet in the Chaldean sequence: Sun, Venus, Mercury, Moon, Saturn, Jupiter, Mars (repeating)
- First hora of Sunday starts with Sun, Monday with Moon, etc.
- Find which hora (hour) of the day birth falls in, identify the ruler → 60 Shashtiamsas; others → 0

**h. Ayana Bala** (Solstitial strength)
- Reflects planet's relationship to the ecliptic
- Sun, Mars, Jupiter, Venus: stronger in Uttarayana (Sun moving north, Capricorn → Gemini); weaker in Dakshinayana
- Moon, Saturn: stronger in Dakshinayana
- Mercury: always gets full Ayana Bala
- Full formula uses the planet's declination. Simplified approach:
  `ayana_bala = 30 + (declination / 24.0 * 30)` where declination is the planet's geocentric declination in degrees
  Use `swe.calc_ut(jd, swe_id, swe.FLG_SWIEPH)` with equatorial coordinates flag to get declination.
  Clamp to [0, 60].

**i. Yuddha Bala** (Planetary war strength)
- When two planets are within 1° of each other, a planetary war (Graha Yuddha) occurs
- The planet with greater latitude wins and gains the loser's Shadbala points in this component
- Only applies to Mars, Mercury, Jupiter, Venus, Saturn (not Sun, Moon, Rahu, Ketu)
- For simplicity: if no planetary war, Yuddha Bala = 0 for all planets
- If war: winner gets loser's total Shadbala (before Yuddha); loser loses those points
- Implement if latitude data is available; otherwise return 0 for all (acceptable simplification)

---

### 4. Chesta Bala (Motional Strength)

Based on the planet's current speed relative to its mean speed:

```python
MEAN_DAILY_MOTION = {
    'Sun':     0.9856,   # degrees/day
    'Moon':   13.1764,
    'Mars':    0.5240,
    'Mercury': 1.3833,
    'Jupiter': 0.0831,
    'Venus':   1.2000,
    'Saturn':  0.0334,
}
```

- Get planet's actual daily speed from `speed` (already returned by `_calc_planet`)
- Chesta Bala = `min(60, abs(speed) / mean_daily_motion * 30)`
- Retrograde planets: retrograde motion counts as full Chesta Bala (they are Vakri = exerting maximum effort)
  → if retrograde: Chesta Bala = 60

---

### 5. Naisargika Bala (Natural Strength)

Fixed hierarchy -- no computation required:

```python
NAISARGIKA_BALA = {
    'Sun':     60.0,
    'Moon':    51.43,
    'Venus':   42.86,
    'Jupiter': 34.29,
    'Mercury': 25.71,
    'Mars':    17.14,
    'Saturn':   8.57,
}
```

---

### 6. Drik Bala (Aspectual Strength)

Based on aspects received from other planets:

Parashari full aspect values (Shashtiamsas contributed per aspecting planet):
```python
ASPECT_STRENGTH = {
    # (aspecting_planet, aspect_type): shashtiamsas
    # Benefic planets (Jupiter, Venus, Mercury waxing, Moon waxing) give positive
    # Malefic planets (Sun, Mars, Saturn, Rahu, Ketu) give negative
}
```

Simplified implementation:
- For each planet P, sum up: +60 for each natural benefic that fully aspects P; +30 for 3/4 aspect; -30 for malefic full aspect; -15 for malefic partial aspect
- Natural benefics: Jupiter, Venus, Mercury (when waxing), Moon (when waxing)
- Natural malefics: Sun, Mars, Saturn
- Drik Bala = total, divide by number of aspecting planets
- Clamp: if negative, use 0; max 60
- Acceptable simplification: Drik Bala = 0 for all if aspect strength data is not available (Phase 2)

---

## Minimum Rupas Thresholds (for is_strong)

```python
MINIMUM_RUPAS = {
    'Sun':     6.5,
    'Moon':    6.0,
    'Mars':    5.0,
    'Mercury': 7.0,
    'Jupiter': 6.5,
    'Venus':   5.5,
    'Saturn':  5.0,
}
```

---

## Integration Point

After implementing `calculate_shadbala()`, add it to `calculate_birth_chart()` in `vedic_calculator.py`:

```python
# Inside calculate_birth_chart(), after the planet loop:
shadbala = calculate_shadbala(planets, jd, lat, lon)
# Add to each planet dict:
for name, bala in shadbala.items():
    if name in planets:
        planets[name]['shadbala'] = bala
```

The `knowledge_engine.py` bridge will pick up `shadbala` automatically in a future session when we extend `ChartFacts` -- no changes needed to knowledge_engine.py now.

---

## Coding standards

- Pure Python -- no new dependencies beyond what is already imported (`swisseph`, `math`, `datetime`)
- All functions must have type annotations and docstrings
- No classes -- functional style matching the existing codebase
- Helper functions prefixed with `_` (private)
- All values clamp to [0, 60] Shashtiamsas unless noted otherwise
- Avoid floating-point traps: use `round(x, 4)` for intermediate values
- Follow the commit format in CLAUDE.md Section 10: `feat(vedic): ...`

---

## Reference files Codex should read before writing

Codex does not have repo access -- paste these sections when submitting the brief:

1. `backend/vedic_calculator.py` lines 1-210 (constants, helpers, `_calc_planet`)
2. `backend/vedic_calculator.py` lines 84-180 (existing dignity constants just added)
3. The `calculate_birth_chart()` function body (lines 415-500 approx)

These give Codex the exact variable names, planet name conventions, and `_calc_planet()` signature.

---

## Deliverable

A single Python code block to be appended to / integrated into `backend/vedic_calculator.py`:
- `MEAN_DAILY_MOTION`, `NAISARGIKA_BALA`, `MINIMUM_RUPAS`, `DIG_BALA_HOUSE` constants
- All private helper functions
- `calculate_shadbala(planets, jd, lat, lon) → dict[str, dict]` public function
- Integration snippet for `calculate_birth_chart()`

No test file needed from Codex -- tests will be written here after integration and review.
