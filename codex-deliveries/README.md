# Codex Deliveries — Staging Folder

**Purpose:** Staging area for all Codex contract deliveries.

Files uploaded here are **not live**. Each file is validated by Claude against the current production `backend/` version before being moved and deployed. Nothing in this folder touches the live app until explicitly integrated.

---

## How to use this folder

1. Upload the Codex-delivered file into this folder on GitHub
2. Tell Claude which contract has arrived
3. Claude reads, diffs, and validates against the live backend file
4. If it passes — Claude moves it to `backend/` and deploys
5. If it fails — Claude flags the exact issue before anything touches production

---

## Contract Status

| # | Contract | File | Status |
|---|---|---|---|
| 1 | vedic_calculator.py — flatlib → pyswisseph | `vedic_calculator.py` | ⏳ Awaiting delivery |
| 2 | panchang_router.py — pyswisseph engine upgrade | `panchang_router.py` | ⏳ Awaiting delivery |
| 3 | Premium Ankjyotish Numerology tile | `numerology_router.py` | ⏳ Awaiting delivery |
| 4 | Full 78-card Tarot deck assets | `tarot_cards.json` | ⏳ Awaiting delivery |
| 4b | Tarot router — DEFAULT_CARDS expanded to 78 | `tarot_router.py` | ⏳ Awaiting delivery |
| 5 | Panchang per-date endpoint | `panchang_router.py` | ⏳ Awaiting delivery |
| 6 | Tarot daily reminder — 3 data endpoints | `tarot_router.py` | ⏳ Awaiting delivery |
| 7 | Astro-Tarot fusion — Temple integration | TBD | 🔒 Future — pending premium tier 3 proposal |

---

## Validation Checklist (Claude runs this before integrating)

### For all `.py` router files
- [ ] Python 3.12 compatible — no `datetime.UTC`, no deprecated syntax
- [ ] `from __future__ import annotations` at top
- [ ] `timezone.utc` used — never `datetime.UTC`
- [ ] `request.app.state.db` for database access
- [ ] `request.state.user.get("email")` for auth
- [ ] All existing route signatures unchanged
- [ ] All existing Pydantic model fields unchanged
- [ ] No imports from Temple App source files
- [ ] Pydantic v2 with `ConfigDict`

### For `vedic_calculator.py` specifically
- [ ] No flatlib imports remaining
- [ ] `import swisseph as swe` present
- [ ] `swe.set_sid_mode(swe.SIDM_LAHIRI)` used
- [ ] `FLG_SWIEPH | FLG_SIDEREAL` flags used
- [ ] `calculate_vedic_chart()` return keys identical to current live version
- [ ] `calculate_ashtakoot()`, `check_mangal_dosha()`, `generate_north_indian_chart_svg()`, `geocode_place()` untouched
- [ ] Validated against 3 reference birth charts before deploying

### For `panchang_router.py` specifically
- [ ] No handcrafted `_julian_day`, `_sun_longitude`, `_moon_longitude`, `_sunrise_sunset_local` functions
- [ ] `swe.julday()`, `swe.calc_ut()`, `swe.rise_trans()` used
- [ ] All three route handlers unchanged: `/daily`, `/calendar/{year}/{month}`, `/festivals`
- [ ] All name tables unchanged: `TITHI_NAMES`, `NAKSHATRA_NAMES`, `YOGA_NAMES`, `KARANA_NAMES`, `RASHI_NAMES`
- [ ] `_day_quality_windows()` logic untouched
- [ ] `ENGINE_VERSION` incremented

### For `tarot_router.py` (Contract 4)
- [ ] `DEFAULT_CARDS` expanded to 78 entries
- [ ] All 22 Major Arcana IDs use slug format (`the-fool` through `the-world`)
- [ ] All 56 Minor Arcana IDs use `{suit}-{rank}` format (`wands-ace`, `cups-07`, etc.)
- [ ] Each card entry has `suit` and `rank` fields
- [ ] No Astro-Tarot fusion code present
- [ ] No dispatch reminder route present
- [ ] No scheduler helper functions present
- [ ] All existing routes, models, helpers identical to live file

### For `tarot_router.py` (Contract 6 — applied on top of Contract 4)
- [ ] Exactly three reminder routes added: `POST /set`, `GET /`, `DELETE /`
- [ ] Reminder document uses Temple model: `reminder_time`, `frequency`, `timezone`, `enabled`
- [ ] No `hour_utc`, `minute_utc`, `channel`, `focus_area`, `next_run_at`, `last_sent_on` fields
- [ ] No dispatch route
- [ ] No APScheduler helper

### For `tarot_cards.json`
- [ ] Flat JSON object — no manifest wrapper, no `deck` object, no `cards[]` array
- [ ] Exactly 78 keys
- [ ] All 22 Major Arcana keys present with correct slugs
- [ ] All 56 Minor Arcana keys use `{suit}-{rank}` format
- [ ] Each value is a complete SVG string starting with `<svg`
- [ ] All SVGs use `viewBox="0 0 200 300"`
- [ ] Background `#0f0d0a`, gold `#C5A059`, text `#f5f0e8`

---

*Do not manually edit files in `backend/` directly. All Codex deliveries go through this folder first.*
