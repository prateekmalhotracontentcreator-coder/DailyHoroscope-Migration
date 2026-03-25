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

The existing `_resolve_user_email()` helper in `tarot_router.py` — which accepts `user_email` query param and `X-User-Email` header as local validation fallbacks — is approved and may remain. The primary production path is always `request.state.user.get("email")`.

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

## Section 6 — New Contract: Full 78-Card Tarot Deck Assets + Router Update

**New contract item. Scope updated to full 78-card standard Tarot deck.**

A standard Tarot deck consists of 78 cards: 22 Major Arcana (The Fool through The World) and 56 Minor Arcana across four suits (Wands, Cups, Swords, Pentacles), with 14 cards per suit (Ace, 2–10, Page, Knight, Queen, King). We are building a premium product. Delivering only Major Arcana would produce a noticeably thin draw pool and a substandard experience for any user who knows Tarot. **The full 78-card deck is required from day one.**

### Two Deliverables for This Contract

**Deliverable A: `tarot_cards.json`** — 78 SVG card illustrations as a single JSON bundle.

**Deliverable B: Updated `tarot_router.py`** — `DEFAULT_CARDS` expanded from 5 placeholders to all 78 cards with full metadata. This is the only change to the router. All existing routes, models, logic, and the auth pattern are untouched.

---

### Deliverable A — `tarot_cards.json`

**Format: single JSON file, card ID slug → SVG string.**

```json
{
  "the-fool":              "<svg viewBox='0 0 200 300' xmlns='http://www.w3.org/2000/svg'>...</svg>",
  "the-magician":          "<svg viewBox='0 0 200 300' xmlns='http://www.w3.org/2000/svg'>...</svg>",
  "wands-ace":             "<svg viewBox='0 0 200 300' xmlns='http://www.w3.org/2000/svg'>...</svg>",
  "wands-02":              "<svg viewBox='0 0 200 300' xmlns='http://www.w3.org/2000/svg'>...</svg>",
  ...all 78 cards...
}
```

**Design specification — applies to all 78 cards:**

| Property | Requirement |
|---|---|
| Aspect ratio | Portrait 2:3 — `viewBox="0 0 200 300"` |
| Background | `#0f0d0a` |
| Gold accent | `#C5A059` |
| Text colour | `#f5f0e8` off-white |
| Each card must include | Card name (bottom), central symbolic illustration |
| Major Arcana additionally | Roman numeral at top |
| Minor Arcana additionally | Suit symbol and rank indicator |
| Style | Geometric / symbolic — no photographic elements |

**Minor Arcana design approach — systematic by suit:**

Each suit has a consistent visual language. The central illustration uses the suit's elemental symbol (Wand/torch for Wands, Cup/chalice for Cups, Sword for Swords, Pentacle/coin for Pentacles) with rank expressed through quantity (2 = two symbols, 3 = three, etc.) or through figure type for court cards (Page, Knight, Queen, King).

---

### Card ID Naming Convention

**Major Arcana (22 cards):** slug format — `the-fool`, `the-magician`, etc.

```
the-fool, the-magician, the-high-priestess, the-empress, the-emperor,
the-hierophant, the-lovers, the-chariot, strength, the-hermit,
wheel-of-fortune, justice, the-hanged-man, death, temperance,
the-devil, the-tower, the-star, the-moon, the-sun, judgement, the-world
```

**Minor Arcana (56 cards):** `{suit}-{rank}` format.

Suits: `wands`, `cups`, `swords`, `pentacles`

Ranks: `ace`, `02`, `03`, `04`, `05`, `06`, `07`, `08`, `09`, `10`, `page`, `knight`, `queen`, `king`

Examples: `wands-ace`, `wands-02`, `cups-queen`, `swords-king`, `pentacles-page`

---

### Deliverable B — Updated `tarot_router.py` (DEFAULT_CARDS only)

Expand `DEFAULT_CARDS` from the current 5 placeholder entries to all 78 cards.

**Each card entry structure — unchanged from current pattern, with two new fields added:**

```python
{
    "id": "wands-ace",
    "name": "Ace of Wands",
    "suit": "wands",            # NEW — "major", "wands", "cups", "swords", "pentacles"
    "rank": "ace",              # NEW — "0"–"21" for Major Arcana, "ace"/"02"–"10"/"page"/"knight"/"queen"/"king"
    "upright_keywords": ["initiative", "spark", "breakthrough"],
    "reversed_keywords": ["delay", "blocked energy", "false start"],
    "image_url": None,
}
```

The `suit` and `rank` fields enable Temple-side filtering for spread draws by suit pool if needed in future. They do not change any existing route logic.

**All existing routes, all Pydantic models, all helper functions, all auth patterns — completely untouched.** The only change is `DEFAULT_CARDS`.

---

## Section 7 — All Open Contracts

| # | Contract | Deliverable | Priority | Validate Against |
|---|---|---|---|---|
| 1 | vedic_calculator.py — flatlib → pyswisseph | `vedic_calculator.py` | **HIGH** | Python 3.12 |
| 2 | panchang_router.py — pyswisseph engine upgrade | `panchang_router.py` | **URGENT** | Python 3.12 |
| 3 | Premium Ankjyotish Numerology tile | New tile in `numerology_router.py` | **MEDIUM** | Python 3.12 |
| 4 | Full 78-card Tarot deck | `tarot_cards.json` + updated `tarot_router.py` | **MEDIUM** | N/A (assets) + Python 3.12 (router) |
| 5 | Panchang per-date endpoint | New route in `panchang_router.py` | **MEDIUM** | Python 3.12 |
| 6 | Tarot daily reminder — data endpoints | 3 new routes added to `tarot_router.py` | **LOW** | Python 3.12 |

### Contract 6 — Tarot Daily Reminder: Detailed Spec

**Scope:** Three new route handlers added to the existing `tarot_router.py`. Complete updated file is the delivery artifact.

**Routes to add:**

```
POST   /api/tarot/reminder/set    — save user reminder preference
GET    /api/tarot/reminder        — retrieve current reminder settings
DELETE /api/tarot/reminder        — remove reminder preference
```

**Document structure** (`doc_type: "reminder"`, collection: `tarot_readings`):

```json
{
  "id": "uuid",
  "doc_type": "reminder",
  "user_email": "user@example.com",
  "reminder_time": "07:30",
  "frequency": "daily",
  "timezone": "Asia/Kolkata",
  "enabled": true,
  "created_at": "iso",
  "updated_at": "iso"
}
```

**Frequency values:** `"daily"`, `"twice_daily"`, `"weekdays_only"`

**APScheduler job is explicitly NOT part of this contract.** The scheduler that reads reminder preferences and triggers notifications lives in `server.py` and is owned by the Temple App side.

**Auth:** `request.state.user.get("email")` — same pattern as all other routes in the file.

---

### Recommended Delivery Order

1. **`vedic_calculator.py`** — removes flatlib, triggers Python 3.12 upgrade. All subsequent work lands on a clean 3.12 backend.
2. **`panchang_router.py`** — pyswisseph upgrade, same dependency already validated in step 1.
3. **Premium Numerology tile** — straightforward addition to a stable, live router.
4. **Full 78-card Tarot deck** — `tarot_cards.json` + updated `DEFAULT_CARDS` in `tarot_router.py`. Can run in parallel with any of the above.
5. **Panchang per-date endpoint** — unlocks the interactive calendar frontend build on Temple side.
6. **Tarot daily reminder endpoints** — lowest priority, 3 routes added to existing `tarot_router.py`.

---

## Section 8 — Ownership Model: Codex, Claude, and Joint

Claude (Temple App) acts as the **integrator and product finisher**. Codex is the **backend engine builder**. Items are split into three lanes.

### Lane 1 — Claude Owns End-to-End (No Codex Input Required)

| Item | Notes |
|---|---|
| PDF download — Numerology reports | Adapts existing `pdf_generator.py` pattern |
| PDF download — Tarot readings | Landscape layout with portrait card assets from Contract 4 |
| Share function — Numerology and Tarot | `ShareModal` already live. Wire to `report_id` from each module |
| Payment gating — Numerology and Tarot | Same Razorpay pattern already live on Birth Chart and Brihat Kundli |
| Tarot cinematic redesign | Full `TarotPage.jsx` redesign — portrait card layout, dark aesthetic, flip animations |
| Tarot XP / gamification display | XP data already returned by `tarot_router.py`. Build points table and level UI |
| Tarot TTS narration (Premium) | Browser Web Speech API — no backend needed |
| Numerology AI interpretation layer | Claude API call added to report display — no new backend endpoint needed |
| SEO rich pages — Tarot | FAQ pages, individual card pages, schema markup |
| SEO rich pages — Numerology | Life Path number articles, calculator landing, schema markup |
| SEO rich pages — Panchang | Daily Panchang SEO pages, festival article pages |
| Onboarding guided tour — Tarot | 5-step overlay coach marks, first-visit detection via localStorage |
| APScheduler job — Tarot reminders | Reads reminder docs from `tarot_readings`, triggers notifications. Lives in `server.py` |
| Logo, brand identity, design system | Locked and live |
| Docker and runtime upgrades | Mechanical step after each Codex delivery. Temple side only |

---

### Lane 2 — Joint (Codex Backend First, Claude Integrates Frontend)

| Item | Codex Delivers | Claude Builds |
|---|---|---|
| Tarot card illustrations | Contract 4 — `tarot_cards.json` (78 cards) | Wire SVGs into `TarotPage.jsx` card display and flip animation |
| Panchang interactive calendar | Contract 5 — `/api/panchang/date/{date}` per-date endpoint | Interactive calendar UI with linked date pages and SEO routes |
| Panchang festival pages | Festival data already in `/festivals` endpoint | Active festival page links, individual festival SEO pages |
| Panchang NavBar dropdown | Panchang sub-routes already live | Fix frontend routing — dropdown items link to correct live pages |
| Tarot daily reminder UI | Contract 6 — 3 reminder data endpoints in `tarot_router.py` | Browser notification permission UI, time picker, frequency selector |

---

### Lane 3 — Codex Backend Contracts (Already in Section 7)

| Contract | Section Reference |
|---|---|
| `vedic_calculator.py` flatlib migration | Section 4 |
| `panchang_router.py` pyswisseph upgrade | Section 1 + Section 7 |
| Premium Ankjyotish Numerology tile | Section 5 |
| Full 78-card Tarot deck (`tarot_cards.json` + `tarot_router.py`) | Section 6 |
| Panchang per-date endpoint | Section 7, Contract 5 |
| Tarot daily reminder data endpoints | Section 7, Contract 6 |

---

*This document supersedes all previous individual responses on Python version, Panchang accuracy, and module contracts. It is the single source of truth for the current Codex engagement. The full document is committed to the repository at `CODEX_MASTER_RESPONSE_MARCH2026.md` in the repo root.*
