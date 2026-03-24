# EverydayHoroscope — Codex Master Response
**Date:** 25 March 2026
**From:** Temple App Team (SkyHound Studios)
**Re:** Panchang Accuracy, Python Version Decision, Architecture State, and New Contracts

---

## Section 1 — Answers to Your Four Panchang Questions

### Q1. Is a Swiss-Ephemeris-grade dependency acceptable for Panchang integration?

**Yes — and it is already present.**

The Temple App backend runs `flatlib==0.2.3` in production. Flatlib wraps `pyswisseph`, which is the Python binding for Swiss Ephemeris. This means `pyswisseph` is already installed on every Render deployment. You do not need to introduce any new pip package.

Import it directly:

```python
import swisseph as swe
```

No additions to `requirements.txt` required.

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

Delivery: one standalone `panchang_router.py`. Same file format as the original contract.

### Q3. Does Temple App have its own astronomy source?

No separate source — `pyswisseph` via the existing `flatlib` dependency **is** the approved source. The question is resolved.

### Q4. Should Codex stop at the current structure and hand over a precision-upgrade plan?

**No. Proceed with the full engine replacement.**

The dependency question is resolved. The API shape is frozen. Proceed to full Swiss Ephemeris engine replacement as described above.

---

## Section 2 — Python Version: Management Decision

**We have decided to upgrade the Temple App backend to Python 3.12. This is a firm decision.**

The `vedic_calculator.py` migration contracted in Section 4 is the task that delivers this upgrade. Once that file is delivered and integrated by Temple App, `flatlib` is removed from `requirements.txt` and the backend moves to Python 3.12 permanently.

**All Codex deliveries from this point forward — `panchang_router.py`, `vedic_calculator.py`, and all future module contracts — must be validated against Python 3.12.**

Python 3.12 is the target runtime. There is no ambiguity and no exceptions.

---

## Section 3 — Temple App Architecture: Current Live State

For Codex's reference, here is the production state as of 25 March 2026.

### Infrastructure

| Component | Status | Detail |
|---|---|---|
| Frontend | LIVE | everydayhoroscope.in — Vercel |
| Backend | LIVE | everydayhoroscope-api.onrender.com — Docker, upgrading to Python 3.12 |
| Database | LIVE | MongoDB Atlas — horoscope_db |
| AI Engine | LIVE | Claude Sonnet 4 via Anthropic API |
| Email | LIVE | Resend — noreply@everydayhoroscope.in |
| Payments | LIVE (test keys) | Razorpay — switching to live keys shortly |

### Integrated Modules

| Module | Status | Notes |
|---|---|---|
| Horoscope (Daily / Weekly / Monthly) | LIVE | Claude AI generation + MongoDB caching |
| Birth Chart | LIVE | flatlib + Claude interpretation + PDF download |
| Kundali Milan | LIVE | Ashtakoot + Claude + PDF download |
| Brihat Kundli Pro | LIVE | 40+ page report, full JSON structure |
| Panchang | LIVE — accuracy upgrade pending | 3 endpoints live, awaiting pyswisseph engine upgrade |
| Numerology | LIVE — backend | Frontend wired, auth fixed, reports generating |
| Tarot | LIVE — backend | Daily draw, spreads, history, gamification live |
| Blog | LIVE | Admin CMS + scheduled publishing |
| Authentication | LIVE | Email/password + Google OAuth |
| Admin Panel | LIVE | 7-tab dashboard |

### Auth Pattern — Critical for All Codex Modules

All Codex routers resolve the authenticated user via `request.state.user`. This dict is populated by a `SessionUserMiddleware` running in `server.py` before every request reaches any router:

```python
request.state.user = {
    "email": "user@example.com",
    "name": "User Name",
    "user_id": "user_abc123",
    "picture": None
}
```

`request.state.user.get("email")` is the correct access pattern. This is live and proven with both Numerology and Tarot.

### Module Delivery Contract — Unchanged

- One standalone `APIRouter` file per module
- No imports from any Temple App source file
- Router prefix: `/api/{module_name}`
- Database via `request.app.state.db`
- Auth via `request.state.user`
- One primary collection per module, one document per generated result
- `from __future__ import annotations` at the top of every file
- `timezone.utc` — never `datetime.UTC`
- Pydantic v2 with `ConfigDict`

---

## Section 4 — New Contract: flatlib → pyswisseph Migration

**This is a new contract item and the highest priority task in this engagement.**

### Why This Exists

`flatlib` is an unmaintained library. It is the sole blocker preventing the Temple App from running on Python 3.12. Internally, `flatlib` wraps `pyswisseph` — which means Swiss Ephemeris is already installed in production. This contract removes the dead wrapper and calls `pyswisseph` directly. Delivering this file is what triggers the Python 3.12 upgrade on the Temple side.

### Scope

**One file in, one file out: `vedic_calculator.py`**

All function signatures and return dict structures are frozen. Nothing outside this file changes.

### What flatlib Currently Does — Only Four Import Lines

```python
from flatlib.datetime import Datetime    # → replace with swe.julday()
from flatlib.geopos import GeoPos        # → replace with plain float lat/lon
from flatlib import const                # → replace with swe.SUN, swe.MOON, etc.
from flatlib.chart import Chart          # → replace with swe.calc_ut() per planet
```

Everything else in `vedic_calculator.py` — all Nakshatra tables, Ashtakoot logic, Dasha calculations, Mangal Dosha checks, house calculations, SVG generation — is pure Python and must not be touched.

### Replacement Map

| flatlib | pyswisseph |
|---|---|
| `Datetime(date_str, time_str, tz_offset)` | `swe.julday(year, month, day, hour_ut)` |
| `GeoPos(lat_str, lon_str)` | Plain `float` values — no wrapper needed |
| `Chart(date, pos, IDs=...)` | `swe.calc_ut(jd, planet_id, flags)` per planet |
| `chart.get(pid).sign` | `SIGN_ORDER[int(sidereal_lon // 30)]` |
| `chart.get(pid).lon` | First element of `swe.calc_ut()` return tuple |
| `chart.getAngle(const.ASC).lon` | `swe.houses(jd, lat, lon, b'W')[1][0]` |
| Retrograde check | `speed_lon < 0` — speed is index 3 of `swe.calc_ut()` return |

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
| `const.SOUTH_NODE` | `(MEAN_NODE longitude + 180.0) % 360` |

### Ayanamsha — Critical

All planet longitudes must be **sidereal (Vedic)**, not tropical. Use Lahiri ayanamsha:

```python
swe.set_sid_mode(swe.SIDM_LAHIRI)
flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
result = swe.calc_ut(jd, planet_id, flags)
lon = result[0][0]        # sidereal ecliptic longitude
speed_lon = result[0][3]  # negative value = retrograde
```

### Frozen Contracts — Do Not Change

`calculate_vedic_chart()` must return a dict with exactly these top-level keys:
`lagna`, `moon_sign`, `nakshatra`, `planets`, `houses`, `dashas`, `current_dasha`, `mangal_dosha`, `birth_details`

These functions are pure Python and must not be touched:
`calculate_ashtakoot()`, `check_mangal_dosha()`, `generate_north_indian_chart_svg()`, `geocode_place()`

`get_current_transits()` — migrate using the same pyswisseph pattern as `calculate_vedic_chart()`.

### Delivery

Single standalone `vedic_calculator.py`. No new pip packages — `pyswisseph` is already installed.

Validate against Python 3.12.

### After Delivery — Temple Side Integration Steps

1. Validate delivered file against 3 reference birth charts (Lagna, Moon sign, Nakshatra, Mars house must match)
2. Remove `flatlib==0.2.3` from `requirements.txt`
3. Update `Dockerfile` to `FROM python:3.12-slim`
4. Update `runtime.txt` to `3.12.x`
5. Deploy to Render and confirm clean Docker build
6. Python 3.12 upgrade is complete

---

## Section 5 — New Contract: Premium Numerology Report (Ankjyotish)

**New contract item.**

### Background

The current 10-tile Numerology module is live and working. This contract adds a **Premium Ankjyotish Report** — a comprehensive numerological life analysis positioned alongside Brihat Kundli Pro at ₹999–1,499.

### Inputs

```
full_birth_name: str          # as on birth certificate
date_of_birth: str            # YYYY-MM-DD
time_of_birth: str            # HH:MM
place_of_birth: str
current_popular_name: str     # optional
lagna_sign: str               # provided by Temple App — do not recalculate
moon_sign: str                # provided by Temple App — do not recalculate
nakshatra_name: str           # provided by Temple App — do not recalculate
```

The Temple App provides the three Vedic fields from the existing birth chart engine. Codex does not replicate the Vedic calculator.

### Required Report Sections

| Section | Content |
|---|---|
| Core Number Profile | Life Path, Expression, Soul Urge, Personality — deep interpretation |
| Lo Shu Grid | Full 3×3 grid, missing numbers, plane analysis (Mental / Emotional / Practical) |
| Karmic Debt Audit | All four debt numbers (13, 14, 16, 19) checked, remediation guidance |
| Personal Year + Month + Day | Current timing window, 3-year forward forecast |
| Name Vibration Analysis | Birth name vs current name, alignment score, correction guidance |
| Vedic Cross-Reference | Lagna lord, Moon sign number, Nakshatra lord mapped to numerology patterns |
| Lucky Elements Table | Numbers, colours, days, directions, gemstones — personalised |
| 7-Day Remediation Plan | Daily action: mantra, colour, number therapy |

### Lo Shu Grid — Delivery Format

Deliver as a structured dict. Temple side renders the visual:

```json
{
  "grid": { "row_1": [4, 9, 2], "row_2": [3, 5, 7], "row_3": [8, 1, 6] },
  "present": [1, 2, 5],
  "missing": [3, 4, 6, 7, 8, 9],
  "repeated": { "1": 2 },
  "planes": {
    "mental":    { "numbers": [4, 9, 2], "complete": false },
    "emotional": { "numbers": [3, 5, 7], "complete": true  },
    "practical": { "numbers": [8, 1, 6], "complete": false }
  }
}
```

### Delivery

- Collection: `numerology_results` (existing collection), `document_type: "premium_ankjyotish_report"`
- New tile added to the existing `numerology_router.py` — no new router file
- Tile code: `premium_ankjyotish_report`
- One document per generated report, linked via `user_email`
- Validate against Python 3.12

---

## Section 6 — New Contract: Tarot Major Arcana Digital Card Assets

**New contract item.**

The current Tarot module uses text placeholders for cards. This contract delivers the 22 Major Arcana as real digital SVG assets.

### Specification

| Property | Requirement |
|---|---|
| Scope | 22 Major Arcana — The Fool through The World |
| Format | SVG — one file per card, or single `tarot_cards.json` bundle (`card_id → SVG string`) |
| Aspect ratio | Portrait 2:3 — `viewBox="0 0 200 300"` |
| Background | `#0f0d0a` |
| Gold accent | `#C5A059` |
| Text | `#f5f0e8` off-white |
| Each card must include | Roman numeral (top), card name (bottom), central symbolic illustration |
| Style | Geometric / symbolic — no photographic elements |

### Card IDs — Must Match Existing Router

```
the-fool, the-magician, the-high-priestess, the-empress, the-emperor,
the-hierophant, the-lovers, the-chariot, strength, the-hermit,
wheel-of-fortune, justice, the-hanged-man, death, temperance,
the-devil, the-tower, the-star, the-moon, the-sun,
judgement, the-world
```

**Delivery:** ZIP of 22 SVG files named by card ID, or a single `tarot_cards.json` file.

Temple side handles all frontend integration. Codex delivers assets only.

---

## Section 7 — All Open Contracts

| # | Contract | Deliverable | Priority | Validate Against |
|---|---|---|---|---|
| 1 | vedic_calculator.py — flatlib → pyswisseph | `vedic_calculator.py` | **HIGH** | Python 3.12 |
| 2 | panchang_router.py — pyswisseph engine upgrade | `panchang_router.py` | **URGENT** | Python 3.12 |
| 3 | Premium Ankjyotish Numerology tile | New tile in `numerology_router.py` | **MEDIUM** | Python 3.12 |
| 4 | Tarot Major Arcana SVG assets | 22 SVG files or JSON bundle | **MEDIUM** | N/A — asset delivery |

### Recommended Delivery Order

1. **`vedic_calculator.py`** — Temple App integrates this first, removes flatlib, upgrades Docker to Python 3.12. All subsequent Codex deliveries then land on a 3.12 backend.
2. **`panchang_router.py`** — uses the same pyswisseph already validated in step 1. Clean integration.
3. **Premium Numerology tile** — straightforward addition to a stable, live router.
4. **Tarot card assets** — asset-only delivery, can run in parallel with any of the above.

---

## Section 8 — Temple App Scope (Not Codex)

The following are handled entirely on the Temple side. Codex involvement is not required:

- All frontend React pages, routing, and styling
- PDF generation for Numerology and Tarot reports
- Share function wiring for all modules
- Payment gating for Numerology and Tarot
- SEO pages and rich content for all modules
- Tarot cinematic redesign, portrait card layout, gamification display
- TTS narration layer for Tarot Premium members
- Reminder and scheduler frontend (browser notifications)
- Logo, brand identity, and all design decisions
- Docker and runtime version upgrades after each Codex delivery

---

*This document supersedes all previous individual responses on Python version, Panchang accuracy, and module contracts. It is the single source of truth for the current Codex engagement.*
