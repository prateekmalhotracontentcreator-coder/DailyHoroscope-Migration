# Codex Commission -- VC-1: Kalachakra & Chara Dasa Computation Engines
> EverydayHoroscope · `vedic_calculator.py` · Commission ID: **VC-1**
> Issued: 2026-06-04 | Owner: Claude Code → Codex

---

## 1. Context

`backend/vedic_calculator.py` is the **single source of truth for all live astronomical and dasha computations**. It currently implements Vimshottari Dasha only:
- `calculate_vimshottari_dasha(birth_date, moon_longitude)` -- 120-year 9-planet cycle
- `build_dasha_timeline(birth_date, moon_longitude)` -- adds antardasha sub-periods
- `get_current_dasha(dashas)` -- returns active period

The Knowledge Engine already has **effect rules for two additional dasa systems** fully ingested in MongoDB (`horoscope_db.interpretation_rules`):
- **Kalachakra Dasa** -- 154 rules, batch `bphs2-ch49-v1-20260526` + `bphs2-ch49-supp-v1-20260527` (BPHS Vol 2 Ch.49)
- **Chara Dasa** -- 73 rules, batch `bphs2-ch50-v1-20260526` + `bphs2-ch50-supp-v1-20260527` (BPHS Vol 2 Ch.50)

These rules are `auto_approved` / `pending_human_review` -- they exist in the KE ready to surface but cannot be activated without the computation engines that determine which dasa is currently active for a native.

This commission builds those two computation engines, patterned after the existing Vimshottari implementation.

---

## 2. Scope

Add to `backend/vedic_calculator.py`:

| Function | Purpose |
|---|---|
| `KALACHAKRA_PERIODS` | Constant dict -- period years per sign (see §4) |
| `KALACHAKRA_NAVAMSA_MAP` | Constant -- starting sign for each Moon Navamsa Pada (108 entries) |
| `calculate_kalachakra_dasha(birth_date, moon_longitude, lagna_longitude)` | Full Kalachakra Mahadasha sequence |
| `build_kalachakra_timeline(birth_date, moon_longitude, lagna_longitude)` | Kalachakra Maha + Antardasha |
| `CHARA_RAHU_FOR_AQ` | Bool constant -- whether to substitute Rahu for Saturn as Aquarius lord in Chara (True per Parasara) |
| `calculate_chara_dasha_durations(planet_positions, lagna_sign)` | Per-sign duration map (step 1 of Chara) |
| `calculate_chara_dasha(birth_date, planet_positions, lagna_sign)` | Full Chara Mahadasha sequence |
| `build_chara_timeline(birth_date, planet_positions, lagna_sign)` | Chara Maha + Antardasha |
| `get_current_kalachakra_dasha(timeline)` | Active Kalachakra period |
| `get_current_chara_dasha(timeline)` | Active Chara period |

Do **NOT** modify any existing function. Do **NOT** touch `knowledge_engine.py` -- engine only, no interpretation layer.

---

## 3. Return Format Requirement -- MUST MATCH VIMSHOTTARI PATTERN

Both engines must return data in the same format as `build_dasha_timeline()` so the rest of the codebase can consume them identically:

```python
# Mahadasha list (from calculate_xxx_dasha):
[
    {
        "sign": "Aries",           # Kalachakra: sign; Chara: sign -- NOT "planet"
        "planet": "Mars",          # The lord of that sign (for KE rule lookup)
        "start": "1990-03-15",
        "end": "1997-03-15",
        "years": 7.0,
    },
    ...
]

# Timeline (from build_xxx_timeline):
[
    {
        "sign": "Aries",
        "planet": "Mars",
        "start": "1990-03-15",
        "end": "1997-03-15",
        "years": 7.0,
        "antardashas": [
            {
                "sign": "Aries",
                "planet": "Mars",
                "start": "1990-03-15",
                "end": "1990-11-15",
            },
            ...
        ],
    },
    ...
]
```

Note: `"planet"` = lord of the current dasa sign (from `SIGN_LORDS`) -- this is the key for KE rule lookup against `condition.dasha_lord` in the ingested rules.

---

## 4. Kalachakra Dasa Engine

### 4.1 Algorithm Overview

Kalachakra ("Wheel of Time") is a Rasi-based dasa system. Instead of 9 nakshatra lords (Vimshottari), it cycles through the 12 Rasis in two directional sweeps.

**Inputs:**
- `birth_date: str` -- ISO `YYYY-MM-DD`
- `moon_longitude: float` -- Moon's longitude in degrees (0-360, from pyswisseph)
- `lagna_longitude: float` -- Ascendant longitude in degrees (for 8th-house veto tagging)

**Step 1 -- Navamsa Pada of Moon:**
```python
navamsa_index = int(moon_longitude / (360 / 108))   # 0-107, the Moon's Navamsa Pada in the 108-point wheel
rasi_index = navamsa_index // 9                     # 0-11, which of the 12 Rasis
pada_within_rasi = navamsa_index % 9                # 0-8, which Pada (0=first, 8=ninth)
moon_rasi = SIGN_ORDER[rasi_index]                  # e.g. "Aries"
```

**Step 2 -- Starting Rasi and Direction:**
- If `moon_rasi` is in **Savya group** (Aries, Taurus, Gemini, Cancer, Leo, Virgo): proceed **forward** (Aries→Taurus→...→Pisces→Aries)
- If `moon_rasi` is in **Apasavya group** (Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces): proceed **backward** (Pisces→Aquarius→...→Aries→Pisces)

The starting Rasi IS `moon_rasi`.

**Step 3 -- First dasha balance:**
```python
# Navamsa Pada position within the starting Rasi (0.0 to 1.0)
pada_fraction = pada_within_rasi / 9.0   # how far through this Rasi's dasa we already are at birth
years_total = KALACHAKRA_PERIODS[moon_rasi]
years_elapsed = pada_fraction * years_total
years_remaining = years_total - years_elapsed
```

**Step 4 -- Sequence generation:**
Generate full mahadasha sequence by cycling through all 12 Rasis from `moon_rasi` in the determined direction, then repeating until 100+ years from birth date are covered (sufficient for any lifetime).

**Step 5 -- 8th-sign veto flag (do not alter dates, only tag):**
For any dasha Rasi that is the 8th sign from the native's Lagna, add `"mortality_flag": True` to that dasha entry. This comes from the BPHS rule about the 8th Navamsa Pada veto. **Tag only -- do not suppress or alter.**

### 4.2 Kalachakra Period Constants

These are the standard Parasara BPHS Kalachakra dasa period years per sign. Source: BPHS Vol 2 Ch.46 (Santhanam translation, `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2/BPHS - 2 RSanthanam.pdf`). **Before coding, verify these against the PDF Ch.46 tables -- if any value differs, use the PDF value.**

```python
KALACHAKRA_PERIODS = {
    # Savya group (forward direction)
    "Aries":       7,
    "Taurus":     16,
    "Gemini":      9,
    "Cancer":      7,
    "Leo":         5,
    "Virgo":       8,
    # Apasavya group (reverse direction)
    "Libra":       7,
    "Scorpio":     7,
    "Sagittarius": 9,
    "Capricorn":   4,
    "Aquarius":    7,
    "Pisces":      5,
}
# Total forward (Savya): 52 years | Total reverse (Apasavya): 39 years
# Full 12-sign cycle: 91 years. Two complete forward+reverse cycles = 182 years.
# ⚠️ VERIFY against BPHS Ch.46 PDF before finalising. Multiple recensions exist.
```

### 4.3 Kalachakra Antardasha

The Antardasha (sub-period) within each Kalachakra Mahadasha follows the same directional sequence, with each Antardasha proportioned as:
```
antardasha_years = (antar_rasi_period / total_12_sign_cycle) × maha_years
```
Starting sub-period = the Mahadasha Rasi itself (same as Vimshottari where the Mahadasha planet's antardasha comes first).

---

## 5. Chara Dasa Engine

### 5.1 Algorithm Overview

Chara ("Moveable") Dasa is a Jaimini sign-based system. Every chart has its own unique dasa duration sequence because durations depend on where each sign's lord is placed in the nativity.

**Inputs:**
- `birth_date: str` -- ISO `YYYY-MM-DD`
- `planet_positions: dict` -- `{planet: sign_name}` for all 9 planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu) -- use data from `calculate_vedic_chart()`
- `lagna_sign: str` -- Ascendant sign name

### 5.2 Chara Duration Calculation (per sign)

```python
CHARA_SIGN_ORDER = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

SIGN_MODALITY = {
    "Aries": "movable", "Cancer": "movable", "Libra": "movable", "Capricorn": "movable",
    "Taurus": "fixed",  "Leo": "fixed",    "Scorpio": "fixed",  "Aquarius": "fixed",
    "Gemini": "dual",   "Virgo": "dual",   "Sagittarius": "dual", "Pisces": "dual",
}

# Parasara school: Rahu substitutes Saturn for Aquarius
# Ketu substitutes Mars for Scorpio
CHARA_SIGN_LORDS = {
    **SIGN_LORDS,
    "Aquarius": "Rahu",   # CHARA_RAHU_FOR_AQ = True
    "Scorpio":  "Ketu",   # Ketu substitution for Scorpio in Parasara Chara
}
```

**Duration rule:**
```python
def chara_duration(sign: str, planet_positions: dict) -> int:
    lord = CHARA_SIGN_LORDS[sign]
    lord_sign = planet_positions[lord]
    sign_idx = CHARA_SIGN_ORDER.index(sign)
    lord_idx = CHARA_SIGN_ORDER.index(lord_sign)

    modality = SIGN_MODALITY[sign]
    if modality == "movable":
        # Count FORWARD from sign to lord's sign (inclusive)
        count = (lord_idx - sign_idx) % 12 + 1
    elif modality == "fixed":
        # Count BACKWARD from sign to lord's sign (inclusive)
        count = (sign_idx - lord_idx) % 12 + 1
    else:  # dual/mutable
        # Take SHORTER of forward and backward counts
        forward  = (lord_idx - sign_idx) % 12 + 1
        backward = (sign_idx - lord_idx) % 12 + 1
        count = min(forward, backward)

    # Exception: if lord is in the same sign as the sign itself
    if lord_sign == sign:
        count = 12

    return count   # years (range 1-12)
```

**Sequence rule:**
Starting from `lagna_sign`, proceed forward (Aries → Pisces → Aries) through all 12 signs. Each sign gets its computed duration. Cycle repeats until sufficient years are covered.

### 5.3 Chara Antardasha

Per BPHS Vol 2 Ch.50 Rule 059 (Slokas 90-91):
> "The Antardasa sequence commences from the Rasi occupied by the lord of the Dasa Rasi, not from the Dasa Rasi itself."

```python
def chara_antardasha_start(maha_sign: str, planet_positions: dict) -> str:
    """Returns the sign from which Chara antardasha sequence starts."""
    lord = CHARA_SIGN_LORDS[maha_sign]
    return planet_positions[lord]   # the sign where the Maha lord sits
```

Antardasha durations use the same `chara_duration()` per sign, proportioned to the Mahadasha total:
```
antar_days = (antar_years / total_12_sign_years) × maha_days
```

### 5.4 Override Flags (from Ch.50 KE rules)

These two veto conditions from BPHS Ch.50 must be flagged as metadata on the dasha entry. **Tag only -- do not alter dates.**

```python
# Rule 052 -- Deep Debilitation veto (Parama Neecha)
# If the Dasa Rasi lord is at its exact debilitation degree (±1°), tag:
"deep_debilitation_veto": True   # authority_override: "overrides_all_benefic_yogas"

# Rule 061 -- Ashtakvarga veto (applied last in pipeline)
# Cannot compute here without Ashtakvarga scores -- leave as None, set by KE pipeline
"ashtakvarga_veto": None
```

---

## 6. Integration with `calculate_vedic_chart()`

Both engines will be called from within `calculate_vedic_chart()`. Add to the chart output dict:

```python
# In calculate_vedic_chart() return payload:
"kalachakra_dasha": build_kalachakra_timeline(date_of_birth, moon_lon, lagna_lon),
"chara_dasha":      build_chara_timeline(date_of_birth, planet_sign_map, lagna_sign),
```

Where `planet_sign_map` is built from the already-computed positions dict inside `calculate_vedic_chart()`:
```python
planet_sign_map = {p: data["sign"] for p, data in planet_positions.items()}
# Must include Rahu and Ketu for Chara sign-lord lookups
```

---

## 7. Files to Modify

| File | Change |
|---|---|
| `backend/vedic_calculator.py` | Add all constants + functions above after line ~1076 (after `get_current_dasha`) |
| **Do NOT touch** | `knowledge_engine.py`, `panchang_router.py`, any router file, any frontend file |

---

## 8. Tests -- `backend/tests/test_dasha_engines.py` (NEW FILE)

Minimum 12 tests. Required:

```python
# Kalachakra
test_kalachakra_moon_in_aries_savya_direction()
    # Moon at 5.0° (Aries Navamsa 1) → first dasha = Aries, direction = forward
test_kalachakra_moon_in_libra_apasavya_direction()
    # Moon at 185.0° (Libra) → direction = backward
test_kalachakra_balance_correct()
    # Moon at mid-Pada → years_remaining ≈ half the Aries period
test_kalachakra_timeline_has_antardashas()
    # build_kalachakra_timeline returns list where each entry has 'antardashas' key
test_kalachakra_8th_sign_mortality_flag()
    # Lagna = Aries → 8th sign = Scorpio → Scorpio dasha entry has mortality_flag=True
test_kalachakra_return_format()
    # Each entry has keys: sign, planet, start, end, years

# Chara
test_chara_duration_movable_sign()
    # Aries, Mars in Scorpio → count forward Aries→Scorpio = 8 years
test_chara_duration_fixed_sign()
    # Taurus, Venus in Libra → count backward Taurus→Libra = 8 years
test_chara_duration_lord_in_own_sign()
    # Any sign where lord is in same sign → 12 years
test_chara_antardasha_starts_from_lord_sign()
    # Chara Aries maha, Mars in Scorpio → antardasha sequence starts from Scorpio
test_chara_timeline_has_antardashas()
    # build_chara_timeline returns list where each entry has 'antardashas' key
test_chara_return_format()
    # Each entry has keys: sign, planet, start, end, years
```

All tests must pass: `python3 -m pytest backend/tests/test_dasha_engines.py -v`

---

## 9. Source References

| System | Primary Source | Location |
|---|---|---|
| Kalachakra period tables | BPHS Vol 2 Ch.46 (Santhanam) | `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2/BPHS - 2 RSanthanam.pdf` |
| Kalachakra effects rules | BPHS Vol 2 Ch.49 | MongoDB `horoscope_db.interpretation_rules` -- batch `bphs2-ch49-v1-20260526` |
| Chara computation rules | BPHS Vol 2 Ch.50 | MongoDB `horoscope_db.interpretation_rules` -- batch `bphs2-ch50-v1-20260526` |
| Chara effects rules | BPHS Vol 2 Ch.50 | Same batch -- `engine_specification` + `yoga_combination` condition types |
| Existing engine pattern | Vimshottari | `backend/vedic_calculator.py` lines 979-1076 |

**CRITICAL for Kalachakra:** Ch.46 of the Santhanam BPHS Vol 2 PDF contains the authoritative period tables. The `KALACHAKRA_PERIODS` dict in §4.2 is a best-estimate from classical sources -- **verify every value against the PDF before finalising.** If the PDF shows different years, the PDF is authoritative.

---

## 10. Acceptance Gates

- [ ] `python3 -m pytest backend/tests/test_dasha_engines.py -v` → all 12+ tests green
- [ ] `calculate_vedic_chart()` returns `kalachakra_dasha` and `chara_dasha` keys -- no regression on existing keys
- [ ] `build_kalachakra_timeline()` return structure is identical to `build_dasha_timeline()` (same key names: `sign`, `planet`, `start`, `end`, `years`, `antardashas`)
- [ ] `build_chara_timeline()` return structure identical
- [ ] Chara: `planet` field in each entry = `SIGN_LORDS[sign]` (standard lord -- NOT Chara substitute lord, which is only for duration calculation)
- [ ] Kalachakra: `planet` field = `SIGN_LORDS[sign]` (standard lord)
- [ ] No `import` of `knowledge_engine` anywhere in the new code
- [ ] `ENGINE_VERSION` in `panchang_router.py` bumped

---

## 11. What This Unlocks

Once this commission is delivered and integrated:
1. **KE engine** can call `build_kalachakra_timeline()` and `build_chara_timeline()` to determine the native's current Kalachakra / Chara period
2. **154 Kalachakra rules** (Ch.49) and **73 Chara rules** (Ch.50) in `horoscope_db` become activatable -- the engine can now look up effects for the current period
3. **Individual Reports** (Brihat Kundali, Strategist, etc.) can expose these dasa systems as premium add-on periods alongside Vimshottari
