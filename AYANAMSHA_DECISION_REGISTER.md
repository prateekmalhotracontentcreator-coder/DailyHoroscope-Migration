# Ayanamsha Decision Register
> EverydayHoroscope · Strategic Computation Reference
> Created: 2026-06-06 | Source: KP vs Lahiri Method -- Based on Use Cases (TT Paper)
> Owner: Temple Team + Claude Code · Review: Required before any ayanamsha change

---

## 1. The Core Distinction

| System | pyswisseph Constant | Value (J2000) | Precision |
|---|---|---|---|
| **Lahiri** (Chitrapaksha) | `swe.SIDM_LAHIRI` = 1 | 23.8571° | ±arcminutes |
| **KP / Newcomb** | `swe.SIDM_KRISHNAMURTI` = 5 | 23.7605° | Sub-lord precision |

**Difference at J2000: −5.795 arcminutes (−0.0966°)**

KP ayanamsha = Lahiri base + Newcomb precession correction. They are NOT the same.
Sub-lord zone widths: 0.5°-2.0°. A 5.8-arcminute error can flip the sub-lord for planets near boundaries.

---

## 2. Module-Level Decision Register

| File | Current State | Required State | Basis |
|---|---|---|---|
| `backend/vedic_calculator.py` | `SIDM_LAHIRI` ✅ | `SIDM_LAHIRI` | Birth chart, Vimshottari dasha, lagna -- standard Vedic |
| `backend/panchang_router.py` | `SIDM_LAHIRI` ✅ | `SIDM_LAHIRI` | Panchang, tithi, nakshatra, yoga -- Hindu calendar standard |
| `backend/kundali_router.py` | `SIDM_LAHIRI` ✅ | `SIDM_LAHIRI` | Kundali Milan / Ashta Koota -- traditional Jyotish |
| `backend/vedic_shared_utils.py` | `SIDM_LAHIRI` ✅ | `SIDM_LAHIRI` | Shared utilities for all Vedic modules |
| `backend/kp_engine.py` | `SIDM_KRISHNAMURTI` ✅ | `SIDM_KRISHNAMURTI` | KP sub-lords, KP cuspal positions -- requires Newcomb. Fixed commit `4400654` 2026-06-06. |

### ✅ AYA-1 FIXED -- `kp_engine.py` line 11
```python
# FIXED (commit 4400654, 2026-06-06):
swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)  # KP system requires Newcomb/Krishnamurti ayanamsha
```
ENGINE_VERSION bumped to `panchang-router-v25-kp-ayanamsha-fix`.

---

## 3. Use-Case Mapping

### Use Lahiri (`swe.SIDM_LAHIRI`) when:
- Computing birth chart placements (rashi, navamsha)
- Running Vimshottari Dasha (mahadasha / antardasha / pratyantar)
- Panchang computations (tithi, nakshatra, yoga, karana)
- Kundali Milan / compatibility scoring
- Longevity report (non-KP mode)
- Any feature using 30° sign divisions only

### Use Krishnamurti (`swe.SIDM_KRISHNAMURTI`) when:
- Computing KP cuspal positions (houses 1-12)
- Assigning KP sub-lords and sub-sub-lords
- Running KP Vimshottari sub-period timing
- KP Prashna (horary) charts
- Any feature using 249 KP sub-lord divisions
- Separating twin charts (arcminute precision required)

---

## 4. Test Vector Ayanamsha Split

| Book | Test Vector Set | Ayanamsha | Reason |
|---|---|---|---|
| 300 Important Combinations (H1) | T3 | Krishnamurti | KP author -- Venkatesh Sharma / Krishnamurti tradition |
| 300 Important Combinations (H2) | T4 | Krishnamurti | Same |
| Longevity Unnatural Deaths | T1 | Krishnamurti | KP Jyotish book |
| Longevity Astro System | T5 | Krishnamurti | KP Jyotish book |
| 765 Notable Horoscopes | T2 | Lahiri | Vedic astrology book -- traditional Jyotish |

Phase 4A Layer A accuracy (as of 2026-06-06):
- T5 (Krishnamurti): 35/36 = **97.2%** ✅
- T1 (Krishnamurti): 66/69 = **95.7%** ✅
- T2 (Lahiri): dasha balance script ready -- pending run

---

## 5. Change Protocol

Any change to ayanamsha in a live backend file requires:
1. **TT sign-off** (co-founder approval) -- changes live user output
2. `ENGINE_VERSION` bump in `panchang_router.py`
3. Regression test on at least 5 known charts per affected module
4. Update this register with new `Current State` entry

**Do NOT** change `SIDM_LAHIRI` → `SIDM_KRISHNAMURTI` in `kp_engine.py` without TT sign-off.

---

## 6. Open Action

| ID | Action | Owner | Priority |
|---|---|---|---|
| ~~AYA-1~~ | ~~Fix `kp_engine.py` line 11: `SIDM_LAHIRI` → `SIDM_KRISHNAMURTI`~~ | ✅ FIXED commit `4400654` 2026-06-06 | -- |
| AYA-2 | Verify KP Oracle sub-lord outputs on 3 known charts post-fix on Render | TT | 🔴 HIGH |
| AYA-3 | Confirm T3/T4 ayanamsha with textbook colophon page | TT | 🟡 MED |

---

*Source paper: `KP vs Lahri Method_Based on Use Cases.md` (TT, 2026-06-06)*
*Computation diff measured: `swe.get_ayanamsa_ut(2451545.0)` → Lahiri=23.857054° KP=23.760470° diff=−0.096584°*
