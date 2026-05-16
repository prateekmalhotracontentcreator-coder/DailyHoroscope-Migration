# Individual Reports × 12 Areas of Life -- Master Map
> EverydayHoroscope · Arc Angel Complement Architecture
> Created: 2026-05-16
>
> **Design principle:** The IR suite is architected to mirror Arc Angel's 12-area dashboard exactly --
> one deep-dive natal/transit report per area of life.  The 12 Vedic houses provide the framework.
> 6 reports are live; 6 are pending definition and commissioning.

---

## Status Key

| Badge | Meaning |
|---|---|
| ✅ LIVE | Router deployed, frontend card present, accessible to premium users |
| 🟡 DELIVERED | Backend delivered locally; Temple review / integration pending |
| 🔴 PENDING | Area identified; report design and commission brief not yet written |

---

## 12 Areas of Life × Individual Reports

| # | Vedic House | Area of Life | Report Name | Report Slug | Phase | Status |
|---|---|---|---|---|---|---|
| 1 | House 1 -- Lagna | **Self, Identity & Life Journey** | Life Cycles Report | `life-cycles` | Phase 1 | ✅ LIVE |
| 2 | House 2 -- Dhana | **Wealth, Values & Abundance** | *(Wealth & Abundance Blueprint)* | `wealth-blueprint` | Phase 3 | 🔴 PENDING |
| 3 | House 3 -- Sahaja | **Communication, Courage & Planning** | Retrograde Survival Guide | `retrograde-survival` | Phase 1 | ✅ LIVE |
| 4 | House 4 -- Sukha | **Home, Emotional Foundation & Inner Rhythm** | Lunar Cycle Wellness | `lunar-cycle` | Phase 2 | ✅ LIVE |
| 5 | House 5 -- Putra | **Romance, Creativity & Intelligence** | *(Romance & Creative Intelligence)* | `romance-creative` | Phase 3 | 🔴 PENDING |
| 6 | House 6 -- Ari | **Health, Daily Rhythm & Service** | *(Vitality & Health Report)* | `vitality-health` | Phase 3 | 🔴 PENDING |
| 7 | House 7 -- Kalatra | **Partnerships, Marriage & Relating** | *(Partnership & Marriage Window)* | `partnership-window` | Phase 3 | 🔴 PENDING |
| 8 | House 8 -- Randhra | **Transformation, Hidden Self & Occult** | Shadow Self Report | `shadow-self` | Phase 1 | ✅ LIVE |
| 9 | House 9 -- Dharma | **Dharma, Higher Purpose & Wisdom** | *(Dharma & Soul Purpose Report)* | `dharma-purpose` | Phase 3 | 🔴 PENDING |
| 10 | House 10 -- Karma | **Career, Status & Public Life** | Career Blueprint | `career-blueprint` | Phase 1 | ✅ LIVE |
| 11 | House 11 -- Labha | **Gains, Aspirations & Social Network** | *(Gains & Network Activator)* | `gains-network` | Phase 3 | 🔴 PENDING |
| 12 | House 12 -- Vyaya | **Karma, Past Lives & Liberation** | Karmic Debt Report | `karmic-debt` | Phase 1 | ✅ LIVE |

---

## Summary Scorecard

| Category | Count |
|---|---|
| ✅ Live | **6** (Houses 1, 3, 4, 8, 10, 12) |
| 🔴 Pending Definition | **6** (Houses 2, 5, 6, 7, 9, 11) |
| **Total** | **12** |

---

## Live Reports -- Design Notes

| Report | House | Why This Mapping |
|---|---|---|
| **Life Cycles** | H1 -- Self & Identity | Vimshottari Dasha maps the entire arc of the self -- each planetary period shapes how identity, vitality, and life direction evolve over time. House 1 is the body and the soul's journey through this incarnation. |
| **Retrograde Survival Guide** | H3 -- Communication & Planning | Mercury retrogrades (the most frequent and felt) disrupt H3 themes: communication, logistics, short travel, contracts, and mental planning. The guide is fundamentally about navigating disrupted cognitive and communication cycles. |
| **Lunar Cycle Wellness** | H4 -- Home & Emotional Foundation | The Moon rules Cancer (natural House 4). Emotional rhythm, inner security, sleep, and body sensitivity are H4 themes. Lunar Cycle Wellness tracks those exact rhythms across the 30-day cycle -- a Moon-ruled report belongs to the Moon's house. |
| **Shadow Self** | H8 -- Transformation & Hidden Self | House 8 governs the unconscious, hidden psychological patterns, taboo, and what must be confronted before transformation is possible. The Shadow Self report excavates exactly these natal placements. |
| **Career Blueprint** | H10 -- Career & Public Life | House 10 (Karma Bhava) is the universal house of profession, reputation, and public standing. The Career Blueprint draws on 10th lord, Atmakaraka, and dasha timing -- a direct H10 reading. |
| **Karmic Debt** | H12 -- Karma & Liberation | House 12 governs loss, foreign lands, hidden enemies, and most critically, the weight carried from prior lifetimes. Karmic Debt reads these natal signatures and their resolution pathways. |

---

## Pending Reports -- Proposed Scope

| Report | House | Core Vedic Inputs | Arc Angel Area |
|---|---|---|---|
| **Wealth & Abundance Blueprint** | H2 -- Dhana | 2nd lord placement, Dhana yogas, Jupiter/Venus, wealth Dasha windows | Wealth & Values |
| **Romance & Creative Intelligence** | H5 -- Putra | 5th lord, Putrakaraka, Venus, creativity windows, romantic timing | Romance & Creativity |
| **Vitality & Health Report** | H6 -- Ari | 6th lord, Mars/Saturn influence, health vulnerability patterns, daily rhythm | Health & Daily Life |
| **Partnership & Marriage Window** | H7 -- Kalatra | 7th lord, Darakaraka, Venus, Upapada Lagna, marriage Dasha timing | Partnerships |
| **Dharma & Soul Purpose Report** | H9 -- Dharma | 9th lord, Jupiter, Atmakaraka, dharmic path, guru influence, past-life blessings | Higher Purpose |
| **Gains & Network Activator** | H11 -- Labha | 11th lord, gains timing, aspiration fulfillment windows, social network strength | Gains & Aspirations |

---

## Architecture Notes

- All 6 pending reports are **natal-first** (single birth chart input), following the Phase 1 pattern
- Computation layer: `vedic_shared_utils.py` + `vedic_calculator.py` -- no new utility functions required
- Claude enrichment: follow `love_prompt_common.py` / `try_claude_generation()` pattern
- Frontend: all 12 cards will live at `/reports` (IndividualReportsPage.jsx, PremiumRoute)
- Pending reports are scoped as Phase 3 -- brief drafting begins after IR-3 (8 Love landing pages) is integrated
- Love Bundle reports (Encounter Window, Love Weather, Date Night, etc.) are **NOT** part of the 12-IR suite -- they are a parallel product tracking a separate relationship-intelligence thread at `/love-reports`

---

## Version History

| Version | Date | Change | By |
|---|---|---|---|
| v1.0 | 2026-05-16 | Initial map created -- 6 live mapped, 6 pending scoped | CC |
