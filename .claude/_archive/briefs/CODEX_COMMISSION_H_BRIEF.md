# Codex Brief — Commission H: Ayur Jyotish (Longevity & Health Report)
> To: Codex
> From: EverydayHoroscope / SkyHound Studios
> Priority: HIGH
> Estimated Effort: ~48h
> Full Spec: `.claude/CODEX_LONGEVITY_REPORT_CONTRACT.md`

---

We're opening a new premium module for **EverydayHoroscope** — India's Vedic astrology
platform at `https://www.everydayhoroscope.in`.

**The Module:** Ayur Jyotish — a premium Longevity & Health Analysis Report combining
**KP (Krishnamurti Paddhati) Astrology** as the primary engine with **Traditional Vedic
Astrology** as the supporting layer.

## What You'll Build

1. `backend/kp_engine.py` — KP Sub-Lord chain calculator (Placidus cusps, significators,
   longevity classification: Alpayu / Madhyayu / Poornayu)
2. `backend/longevity_router.py` — 4 API endpoints under `/api/longevity`
3. `frontend/src/pages/LongevityReportPage.jsx` — 7-section report UI:
   - Longevity Classification
   - Constitutional Health Profile (Prakriti)
   - Vulnerable Body Systems & Organs
   - Disease Susceptibility Windows (Dasha × Transit triggers)
   - Critical Period Alerts (Maraka, 22nd Drekkana, 64th Navamsa)
   - Remedial & Preventive Guidance
   - Decade-wise Quality of Life Forecast
4. Claude API narrative layer for professional health report generation

## Key Constraints

- Uses existing `pyswisseph`, `anthropic`, Motor MongoDB — no new major dependencies
- KP uses **Placidus** house system (`swe.houses()` with `b'P'`) — not equal-house
- Medical disclaimer mandatory and non-removable on all report views
- Pro-tier paywall gated (₹499/mo or ₹999 one-time)
- Claude model for narrative: `claude-sonnet-4-6`
- Report generation target: < 10s total (< 500ms calculation + < 8s Claude API)

## Build After Commission I

**Build Commission I (Knowledge Engine) first.** The Longevity Report calls
`scan_chart(categories=["health"])` on the Knowledge Engine for its health-category
narratives. Building I first means this report gets multi-source, book-grounded
interpretations automatically.

## Full Specification

Read `.claude/CODEX_LONGEVITY_REPORT_CONTRACT.md` before starting. It contains:
- Complete KP sub-lord algorithm
- Health mapping tables (sign → body parts, planet → disease domains, house → health domains)
- Critical period detection logic
- Full API request/response schema
- Frontend section-by-section spec
- Acceptance criteria checklist
- Dependency map

---

> Stack: FastAPI (Render) + React 18 (Vercel) + MongoDB + pyswisseph 2.10.x
