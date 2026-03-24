# EverydayHoroscope — Codex Master Response
**Date:** 25 March 2026
**From:** Temple App Team (SkyHound Studios)
**Re:** Panchang Accuracy, Python Version, Architecture Updates, and New Contract Requirements

---

## Section 1 — Answers to Your Four Panchang Questions

### Q1. Is a Swiss-Ephemeris-grade dependency acceptable for Panchang integration?

**Yes — and it is already present.**

The Temple App backend runs `flatlib==0.2.3` in production. Flatlib wraps `pyswisseph`, which is the Python binding for Swiss Ephemeris. This means `pyswisseph` is already installed on every Render deployment. You do not need to introduce any new pip package.

Import it directly:
```python
import swisseph as swe
```

No additions to requirements.txt required.

### Q2. Should Codex refactor the Panchang router around that dependency while preserving the current API shape?

**Yes — approved and required.**

Replace the following handcrafted astronomy functions in `panchang_router.py`:
- `_julian_day()`
- `_sun_longitude()`
- `_moon_longitude()`
- `_sunrise_sunset_local()`
- `_moment_longitudes()`

Replace with `pyswisseph` calls:
- `swe.julday()` for Julian Day
- `swe.calc_ut()` for Sun and Moon geocentric apparent longitude
- `swe.set_sid_mode(swe.SIDM_LAHIRI)` for Lahiri ayanamsha
- `swe.rise_trans()` for precise sunrise, sunset, moonrise, moonset
- `swe.get_ayanamsa_ut(jd)` for sidereal conversion

**The entire API contract layer is frozen.** Do not change:
- Any Pydantic model or field name
- The three route handlers: `/daily`, `/calendar/{year}/{month}`, `/festivals`
- Their query parameter signatures
- `TITHI_NAMES`, `NAKSHATRA_NAMES`, `YOGA_NAMES`, `KARANA_NAMES`, `RASHI_NAMES`
- `OBSERVANCE_RULES` and all festival logic
- `_day_quality_windows()` and all timing window logic
- `DEFAULT_LOCATIONS`
- `ENGINE_VERSION` format (increment the version number only)

Delivery: one standalone `panchang_router.py`. Same file format as original contract.

### Q3. Does Temple App have its own astronomy source?

No separate source — `pyswisseph` via the existing flatlib dependency **is** the approved source. The question is resolved.

### Q4. Should Codex stop at the current structure and hand over a precision-upgrade plan?

**No. Proceed with the full engine replacement.**

The dependency constraint is gone. The API shape is frozen. Proceed to full Swiss Ephemeris replacement as described above.

---

## Section 2 — Python Version: Final Position

**The Python version debate is over. Here is the permanent position.**

The `PYTHON_VERSION.md` file is committed to the repository root as the permanent, single source of truth. Reference it in all future conversations.

**Current state:** Python 3.11, locked.

**Why it was 3.11:** `flatlib` wraps `pyswisseph`, a C extension using `PyUnicode_AS_DATA`, removed in Python 3.12. Building on 3.12 fails at the C compile step.

**Future state:** Python 3.12, once `vedic_calculator.py` is migrated off `flatlib` to direct `pyswisseph` calls (see Section 4 below). Once that migration ships, `flatlib` is removed from `requirements.txt`, the 3.11 constraint disappears, and we move to 3.12.

**For all Codex local validation environments until further notice:**
```bash
brew install python@3.11
python3.11 -m venv .venv
source .venv/bin/activate
pip install fastapi pydantic uvicorn
```

We will issue an explicit updated instruction when the Python version changes. Do not act on any other signal.

---

## Section 3 — Temple App Architecture: Current Live State

For Codex's reference, here is the current production state as of 25 March 2026.

### Infrastructure
| Component | Status | Detail |
|---|---|---|
| Frontend | LIVE | everydayhoroscope.in (Vercel) |
| Backend | LIVE | everydayhoroscope-api.onrender.com (Python 3.11, Docker) |
| Database | LIVE | MongoDB Atlas — horoscope_db |
| AI Engine | LIVE | Claude Sonnet 4 via Anthropic API |
| Email | LIVE | Resend — noreply@everydayhoroscope.in |
| Payments | LIVE (test keys) | Razorpay — switching to live keys shortly |

### Integrated Modules
| Module | Status | Notes |
|---|---|---|
| Horoscope (Daily/Weekly/Monthly) | LIVE | Claude AI generation + MongoDB caching |
| Birth Chart | LIVE | flatlib + Claude interpretation + PDF download |
| Kundali Milan | LIVE | Ashtakoot + Claude + PDF download |
| Brihat Kundli Pro | LIVE | 40+ page report, full JSON structure |
| Panchang | LIVE — accuracy upgrade pending | 3 endpoints live, awaiting pyswisseph upgrade |
| Numerology | LIVE — backend | Frontend wired, reports generating |
| Tarot | LIVE — backend | Daily draw, spreads, history, gamification live |
| Blog | LIVE | Admin CMS + scheduled publishing |
| Authentication | LIVE | Email/password + Google OAuth |
| Admin Panel | LIVE | 7-tab dashboard |

### Auth Pattern (Critical for all Codex modules)

All Codex routers resolve the authenticated user via `request.state.user`.
This is populated by a `SessionUserMiddleware` in `server.py` on every request:

```python
request.state.user = {
    "email": "user@example.com",
    "name": "User Name",
    "user_id": "user_abc123",
    "picture": None
}
```

`request.state.user.get("email")` is the correct pattern. Live and proven with Numerology and Tarot.

### Module Delivery Contract (unchanged)
- One standalone `APIRouter` file per module
- No imports from any Temple App source file
- Router prefix: `/api/{module_name}`
- Database via `request.app.state.db`
- Auth via `request.state.user`
- Collections: one primary collection, one document per generated result
- `from __future__ import annotations` at top of every file
- `timezone.utc` — never `datetime.UTC`
- Pydantic v2 with `ConfigDict`

---

## Section 4 — New Contract: flatlib → pyswisseph Migration

**New contract item. Highest priority dependency task.**

### Why

`flatlib` is unmaintained. It blocks Python 3.12. It uses `pyswisseph` underneath — meaning Swiss Ephemeris is already in production. We are removing the dead wrapper and using `pyswisseph` directly.

### Scope

**One file in, one file out: `vedic_calculator.py`**

Function signatures and return dict structures are frozen.

### What flatlib currently does (only these four imports)

```python
from flatlib.datetime import Datetime    # → swe.julday()
from flatlib.geopos import GeoPos        # → plain float lat/lon
from flatlib import const                # → swe.SUN, swe.MOON, etc.
from flatlib.chart import Chart          # → swe.calc_ut() per planet
```

Everything else in the file is pure Python — untouched.

### Replacement Map

| flatlib | pyswisseph |
|---|---|
| `Datetime(date_str, time_str, tz_offset)` | `swe.julday(year, month, day, hour_ut)` |
| `GeoPos(lat_str, lon_str)` | Plain `float` values — no wrapper |
| `Chart(date, pos, IDs=...)` | `swe.calc_ut(jd, planet_id, flags)` per planet |
| `chart.get(pid).sign` | `SIGN_ORDER[int(sidereal_lon // 30)]` |
| `chart.get(pid).lon` | First element of `swe.calc_ut()` return |
| `chart.getAngle(const.ASC).lon` | `swe.houses(jd, lat, lon, b'W')[1][0]` |
| Retrograde check | `speed_lon < 0` from `swe.calc_ut()` |

### Planet ID Map

| flatlib const | pyswisseph |
|---|---|
| `const.SUN` | `swe.SUN` |
| `const.MOON` | `swe.MOON` |
| `const.MERCURY` | `swe.MERCURY` |
| `const.VENUS` | `swe.VENUS` |
| `const.MARS` | `swe.MARS` |
| `const.JUPITER` | `swe.JUPITER` |
| `const.SATURN` | `swe.SATURN` |
| `const.NORTH_NODE` | `swe.MEAN_NODE` |
| `const.SOUTH_NODE` | `(MEAN_NODE lon + 180.0) % 360` |

### Ayanamsha — Critical

All longitudes must be **sidereal (Vedic)**, not tropical:

```python
swe.set_sid_mode(swe.SIDM_LAHIRI)
flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
result = swe.calc_ut(jd, planet_id, flags)
lon = result[0][0]
speed_lon = result[0][3]  # negative = retrograde
```

### Frozen Contracts — Do Not Change

`calculate_vedic_chart()` return keys:
`lagna`, `moon_sign`, `nakshatra`, `planets`, `houses`, `dashas`, `current_dasha`, `mangal_dosha`, `birth_details`

All other functions (`calculate_ashtakoot`, `check_mangal_dosha`, `generate_north_indian_chart_svg`, `geocode_place`) — **no change**. Pure Python.

`get_current_transits()` — same migration pattern as `calculate_vedic_chart()`.

### Delivery

Single standalone `vedic_calculator.py`. No new pip packages.

### After Delivery — Temple Side Actions

1. Remove `flatlib==0.2.3` from `requirements.txt`
2. `Dockerfile`: `FROM python:3.11-slim` → `FROM python:3.12-slim`
3. `runtime.txt`: update to `3.12.x`
4. `PYTHON_VERSION.md`: update to reflect unblock
5. Validate against 3 reference birth charts before production deploy

---

## Section 5 — New Contract: Premium Numerology Report (Ankjyotish)

**New contract item.**

### Inputs

```
full_birth_name: str          # as on birth certificate
date_of_birth: str            # YYYY-MM-DD
time_of_birth: str            # HH:MM
place_of_birth: str
current_popular_name: str     # optional
lagna_sign: str               # provided by Temple App from birth chart
moon_sign: str                # provided by Temple App from birth chart
nakshatra_name: str           # provided by Temple App from birth chart
```

**Note:** Temple App provides the three Vedic fields. Codex does not replicate the Vedic calculator.

### Required Report Sections

| Section | Content |
|---|---|
| Core Number Profile | Life Path, Expression, Soul Urge, Personality — deep interpretation |
| Lo Shu Grid | Full 3×3 grid, missing numbers, plane analysis |
| Karmic Debt Audit | All four debt numbers (13, 14, 16, 19), remediation |
| Personal Year + Month + Day | Current timing, 3-year forward window |
| Name Vibration Analysis | Birth name vs current name, alignment score, correction guidance |
| Vedic Cross-Reference | Lagna lord, Moon sign, Nakshatra lord mapped to numerology |
| Lucky Elements Table | Numbers, colours, days, directions, gemstones |
| 7-Day Remediation Plan | Daily action: mantra, colour, number therapy |

### Lo Shu Grid Delivery Format

```json
{
  "grid": {"row_1": [4,9,2], "row_2": [3,5,7], "row_3": [8,1,6]},
  "present": [1, 2, 5],
  "missing": [3, 4, 6, 7, 8, 9],
  "repeated": {"1": 2},
  "planes": {
    "mental": {"numbers": [4,9,2], "complete": false},
    "emotional": {"numbers": [3,5,7], "complete": true},
    "practical": {"numbers": [8,1,6], "complete": false}
  }
}
```

### Delivery

- Collection: `numerology_results` (same), `document_type: "premium_ankjyotish_report"`
- New tile added to existing `numerology_router.py`
- Tile code: `premium_ankjyotish_report`
- One document per report, linked via `user_email`

---

## Section 6 — New Contract: Tarot Major Arcana Digital Card Assets

**New contract item.**

### Specification

- **Scope:** 22 Major Arcana cards (The Fool through The World)
- **Format:** SVG — one file per card or single JSON bundle (`card_id → SVG string`)
- **Aspect ratio:** Portrait, 2:3 (`viewBox="0 0 200 300"`)
- **Colours:** Background `#0f0d0a`, gold accent `#C5A059`, off-white text `#f5f0e8`
- **Each card includes:** Roman numeral (top), card name (bottom), central symbolic illustration
- **Style:** Geometric/symbolic — no photographic elements

### Card ID format

`the-fool`, `the-magician`, `the-high-priestess`, `the-empress`, `the-emperor`,
`the-hierophant`, `the-lovers`, `the-chariot`, `strength`, `the-hermit`,
`wheel-of-fortune`, `justice`, `the-hanged-man`, `death`, `temperance`,
`the-devil`, `the-tower`, `the-star`, `the-moon`, `the-sun`,
`judgement`, `the-world`

**Delivery:** ZIP of 22 SVG files named by card ID, or `tarot_cards.json`. Temple side handles all frontend integration.

---

## Section 7 — All Open Contracts Summary

| # | Contract | File | Priority | Status |
|---|---|---|---|---|
| 1 | Panchang pyswisseph engine upgrade | `panchang_router.py` | **URGENT** | Replace handcrafted astronomy. API frozen. |
| 2 | flatlib → pyswisseph migration | `vedic_calculator.py` | **HIGH** | Removes flatlib, unblocks Python 3.12. |
| 3 | Premium Ankjyotish Numerology tile | `numerology_router.py` | **MEDIUM** | Deep report + Lo Shu + Vedic cross-ref. |
| 4 | Tarot Major Arcana SVG assets | Asset delivery (22 SVGs) | **MEDIUM** | Portrait, gold/dark, geometric. |

### Recommended delivery order

1. `vedic_calculator.py` — unlocks Python 3.12 for everything downstream
2. `panchang_router.py` — uses same pyswisseph, validates the migration
3. Premium Numerology tile — stable router, clean addition
4. Tarot card assets — can run in parallel with any backend work

---

## Section 8 — Temple App Scope (Not Codex)

The following are handled entirely on the Temple side:

- All frontend React pages, routing, and styling
- PDF generation for Numerology and Tarot (adapting existing pdf_generator.py)
- Share function for all modules (adapting existing ShareModal)
- Payment gating for Numerology and Tarot
- SEO pages and rich content for all modules
- Tarot cinematic redesign, portrait card layout, gamification display
- TTS narration for Tarot Premium
- Reminder/scheduler frontend (browser notifications)
- Logo, brand, and all design decisions

---

*This document supersedes all previous individual responses on Python version, Panchang accuracy, and module contracts. Reference this as the single source of truth for the current Codex engagement.*
