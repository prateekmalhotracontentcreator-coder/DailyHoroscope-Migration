# Handover Note — Knowledge Engine Ingest Sprint
**Last updated:** 7 May 2026
**Status:** Mundane Astrology Phase 1 (v3–v16) COMPLETE and live in MongoDB

---

## What This Project Is

**EverydayHoroscope** — India's premium Vedic astrology platform.
- Frontend: React on Vercel → https://www.everydayhoroscope.in
- Backend: FastAPI on Render → https://everydayhoroscope-api.onrender.com
- DB: MongoDB (Motor async driver), database: `horoscope_db`
- Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
- Full project context: read `CLAUDE.md` in repo root before doing anything

---

## Key Files

```
backend/scripts/
├── INGEST_NOTES.md                     ← MASTER REFERENCE — full chapter-by-chapter
│                                          log, cumulative tables, all design decisions
├── run_mundane_ingest.py               ← Staged runner for mundane v3–v16+
│                                          Usage: python3 backend/scripts/run_mundane_ingest.py
│                                          (reads $MONGO_URL from env)
├── ingest_mundane_engine_specs_v3.py   ← v3 spec script  (async def main())
├── ingest_mundane_interpretation_v3.py ← v3 rules script (async def main())
├── ingest_mundane_engine_specs_v4.py   ← v4 spec script  (async def run())
├── ...                                 ← v5–v16 same pattern
├── ingest_mundane_engine_specs_v16.py  ← Most recent spec script
└── ingest_mundane_interpretation_v16.py← Most recent rules script
```

**INGEST_NOTES.md is the single source of truth** for all ingest state, cumulative totals, design decisions, and pending work. Always read it first.

---

## Current State — Mundane Astrology (7 May 2026)

### MongoDB collections

| Collection | Documents | Notes |
|---|---|---|
| `mundane_engine_specs` | **72** | v1–v2 (old schema, 15 docs) + v3–v16 (motor schema, 57 docs) |
| `interpretation_rules` (mundane_jyotish) | **209** | v1–v2 (132) + v3–v16 (77) |
| `mundane_geo_entities` | **29** | Foundation charts, Koorma zones, Zodiac geography |

### What v3–v16 covers (all committed, all live)

| Version | Commit | Specs | Rules | Key content |
|---|---|---|---|---|
| v3 | — | 10 | 27 | Celestial Council, Clouds/Snakes, Commodity ownership, Koorma geo |
| v4 | — | 11 | 15 | Mehta 9-step, Cabinet engine, Solar ingress, Paksha, Simhasana |
| v5 | — | 2 | 12 | Seismic 16-factor, Assassination hazard |
| v6 | — | 3 | 11 | Governance/election, Oath-taking muhurta, Foundation chart |
| v7 | — | 3 | 9 | War engine, Geopolitical rivalry, India-Pakistan axis |
| v8 | — | 4 | 11 | Eclipse engine (shadow math + magnitude timing) |
| v9 | — | 5 | 11 | Sun/Moon transit matrices, Ingress weekday, Muhurti filters |
| v10 | — | 1 | 5 | Raphael western eclipse decanate engine |
| v11 | — | 3 | 14 | Historical benchmark matrix (WWI/WWII/9-11), Validation engine |
| v12 | — | 4 | 17 | Saturn transit matrix (signs + nakshatras + navamsh) |
| v13 | fe6a1d7 | 8 | 18 | Koorma grid, Sanghatta Chakra, Rohini War Gate (**4 critical rules**) |
| v14 | b634829 | 4 | 16 | Macro-conjunction engine, Sun/Moon/Saturn transit (**4 critical rules**) |
| v15 | f93f19b | 6 | 14 | Planetary transits (Mars/Mercury/Jupiter/Venus/Rahu), Synthesis engine, Koorma kill-switch |
| v16 | 3a92413 | 8 | 29 | Ardra/Monsoon, Rohini Chakra, Trinadi, Saptnadi, Crops, Material DB, Sarvatobhadra (**5 critical rules**) |

---

## How to Run the Ingest Runner

```bash
# $MONGO_URL must already be exported in your terminal
python3 backend/scripts/run_mundane_ingest.py
# → Shows summary → type "yes" to confirm → runs all found scripts in sequence
```

**Runner is idempotent** — upsert pattern means re-running any script any number of times is safe.

**Adding new versions:** Edit `SCRIPT_PAIRS` list in `run_mundane_ingest.py` to add the new pair.

---

## Schema Pattern — v3–v16 (Motor Async)

### Engine specs (`mundane_engine_specs`)
```python
{
    "spec_id":    "gaur-ch5-ardra-monsoon-engine",   # upsert key
    "spec_type":  "multi_factor_lookup",
    "science_id": "mundane_jyotish",                 # NEVER "jyotish"
    "batch_id":   "mundane-engine-v16-20260506",
    "title":      "...",
    "source":     "gaur_aifas_ch5",
    "description": "...",
    "created_at": "<ISO timestamp>",
    # ... chapter-specific data fields
}
```

### Interpretation rules (`interpretation_rules`)
```python
{
    "rule_id":          "mundane-gaur-ch5-ardra-bumper-harvest",  # upsert key
    "batch_id":         "mundane-interp-v16-20260506",
    "science_id":       "mundane_jyotish",
    "sub_type":         "monsoon_forecast",
    "title":            "...",
    "source_chapter":   "Gaur Ch 5 — ...",
    "condition":        "IF (...) AND (...)",
    "result":           "...",
    "synthesis_sources": ["spec-id-1", "spec-id-2"],
    "checkable":        True,
    "approval_status":  "pending_review",
    "severity":         "critical",   # low / medium / high / critical
    "created_at":       "<ISO timestamp>",
}
```

**Critical rules encoded so far (severity=critical):**
- Rohini War Gate (WWI/WWII/1971 validated)
- Mars-Ketu massacre trigger
- Triple Malefic Destruction Scheme
- 7th-house Vedha war ignition
- Aries 1° paradigm shift
- Saturn-Mars watery sign tsunami
- Saturn-Mars 6th house massacre
- Mars-Ketu terrorism engine (9/11 pattern)
- Rohini Mountain drought (overrides all other monsoon signals)
- Trinadi Rule 8 (no rain — critical atmospheric veto)
- Mars/Venus/Jupiter catastrophic floods
- Sprouting failure (Yoga VIII) — crop destroyed at germination
- Total crop failure (Yoga IX) — malefics in 7th + angular

---

## Pending Next Batches

| Version | Source | Content | Status |
|---|---|---|---|
| **v17** | Gopal Ch3 + Ch14 | Foundation Chart analysis + Dasha timing validation | 🔜 Next |
| **v18** | Gopal Ch4–5, Mehta Ch18–22 | Governance engine — Elections + Oath Taking | 🔜 Queued |
| **v1/v2 migration** | Old pymongo schema scripts | Different field layout — migration decision pending | 🔜 Deferred |

---

## Lal Kitab State (unchanged)

- **467 rules** | 303 auto-approved | 157 pending_human_review | 7 flagged
- Ch 27 open flag: `lalkitab-ch27-corr-mars-benefic` — source column misalignment, needs source verification

---

## Larger Roadmap (per CONTRACT.md)

- Knowledge Engine arc-angel-windows endpoint (CPath-1)
- Arc Angel UI build-out
- Shadbala engine (brief: `.claude/CODEX_COMMISSION_SHADBALA_ENGINE.md`)
- SEO/marketing/web perf sprint (brief: `.claude/CODEX_COMMISSION_SEO_MARKETING_WEBPERF_BRIEF.md`)
- WhatsApp unblock (phone OTP + Meta payment method on `+91 96431 10001`)
- Instagram Business Account ID (pending Meta dashboard)
- Razorpay live keys (when ready for Play Store)

---

## Environment Variables

```bash
export MONGO_URL="mongodb+srv://..."   # From Render env or Prateek's terminal
```
All other env vars live on Render/Vercel — not needed locally unless running the full backend.

---

## Architecture Rule (MANDATORY)

**All live dasha/astronomical computations MUST use `vedic_calculator.py` + `pyswisseph`.**
The Knowledge Engine (`knowledge_engine.py`) is the interpretation layer ONLY.
Never duplicate dasha calculation in `knowledge_engine.py`.
See `CLAUDE.md` Section 16 for full detail — read before touching any KE or Arc Angel code.

---

## How to Start a New Session

1. Read `CLAUDE.md` (project identity, infrastructure, all key file locations)
2. Read `backend/scripts/INGEST_NOTES.md` (full ingest state — Mundane section at bottom)
3. Confirm `$MONGO_URL` is set in terminal
4. Next task: **v17** — Gopal Ch3 Foundation Chart + Ch14 Dasha timing
   Source: `/Users/apple/Documents/Knowledge Engine_eBooks/New Ingest_5 Books/3. Mundane Astrology/3. Mundane Astrology_JSON_LM.md`
   (line ~8984 for Gopal Ch3, line ~13273+ for Ch14 content)
