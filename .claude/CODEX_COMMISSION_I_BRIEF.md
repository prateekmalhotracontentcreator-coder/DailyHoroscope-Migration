# Codex Brief — Commission I: Jyotish Knowledge Engine
> To: Codex
> From: EverydayHoroscope / SkyHound Studios
> Priority: HIGH
> Estimated Effort: ~84h
> Full Spec: `.claude/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md`

---

We're building the **internal Knowledge Engine** that becomes the interpretation backbone
for every module on EverydayHoroscope — Kundali, Longevity, Horoscopes, and cross-science
unified readings.

**This is infrastructure, not a user-facing page.** It powers all interpretation across
the platform. Build this before Commission H.

## What You'll Build

### Backend
1. `backend/knowledge_engine.py` — Core engine: rule scanner, scorer, conflict resolver,
   and Claude narrative generator (narrative-first, full prose — never bullet points)
2. `backend/knowledge_router.py` — API endpoints under `/api/knowledge`:
   - `POST /api/knowledge/interpret` — generate interpretation for a chart
   - Rule CRUD (admin): GET / POST / PUT / DELETE `/api/knowledge/rules`
   - `POST /api/knowledge/rules/import` — bulk import from JSON
   - `GET /api/knowledge/rules/stats` — coverage statistics

### MongoDB Collections (4 new)
- `interpretation_rules` — the rule library (13 condition types, full-text book passages)
- `author_voices` — 5 voice profiles (classical, modern_analytical, kp_technical, spiritual, popular)
- `narrative_bridges` — ~30 bridging phrases for stitching multi-source text blocks
- `cross_science_combinations` — ~50 multi-factor confirmation combos (Astrology + Numerology)

### Seed Data Files (in `backend/data/`)

These are the **Phase 1 bootstrap files** — the minimum viable library to launch the
engine. They are NOT the complete library. Additional books will be uploaded progressively
by the content team via the Library Console Import tab as the knowledge library grows.

- `seed_rules.json` — ~300 hand-curated rules (Phase 1 bootstrap only)
- `seed_cross_science.json` — ~50 cross-science combos (astrology + numerology, Phase 1)
- `seed_voices.json` — 5 author voice profiles
- `seed_bridges.json` — ~30 narrative bridge phrases

**Important — Book Upload Architecture:**
The system must be designed from day one to support an **expanding book library**, not
just the Phase 1 seed pack. Books will be provided by the client as OCR'd PDFs/text
files and uploaded progressively via the Library Console. The data model, import pipeline,
and storage schema must accommodate:

- Hundreds of books across traditions (Vedic, KP, Nadi, Western, Numerology, Palmistry, Tarot)
- Each book as a named source with author, tradition, and authenticity score
- Rules extracted from each book tagged back to their exact source + chapter/verse
- The library growing from ~300 rules at launch to potentially 10,000+ rules over time
- No hardcoded book list — sources are data, not code

The Phase 2 OCR → Extraction pipeline (see full spec) is what enables bulk ingestion
of new books without manual rule entry. The Library Console Import tab handles
review and approval of extracted rules before they go live.

### Library Console (standalone — NOT part of Operations Admin Console)
- New page: `frontend/src/pages/LibraryConsolePage.jsx`
- Route: `/library`
- Role: `library_admin` — separate from `admin` role, add to `auth_utils.py`
- **Completely decoupled from `/admin/dashboard`** — different entry point, different role
- **5 tabs:**
  - **Rules Browser** — filterable table, inline edit, active/inactive toggle, priority slider
  - **Rule Editor** — condition builder, full-text passage manager, modifier builder, conflict checker, live preview
  - **Library Import** — JSON upload, validation preview, duplicate detection, import history
  - **Coverage Dashboard** — 12×9 heatmap, gap analysis, category donut chart, source bar chart
  - **Test Console** — input chart → matched rules + narrative side-by-side, voice/depth selectors, citation trail

## Key Design Principles

**Narrative-First (not keyword mapping):**
Rules store 500+ word verbatim book passages alongside summaries. The LLM is grounded
in actual classical text — reducing hallucination and delivering genuinely deep readings.

**Author Voice Blending:**
`generate_narrative(voice_blend="classical+modern_analytical")` — the engine blends
classical Sanskrit-tradition tone with modern psychological astrology for each report type.

**Narrative Bridges:**
When Book A says "wealth" and Book B says "losses" for the same placement, the engine
doesn't discard either. It renders them as "competing energies" using bridging phrases,
producing a nuanced multi-perspective narrative.

**Cross-Science Confirmation:**
Phase 1: Astrology + Numerology unified scoring (Astrology 40%, Numerology 20%,
Palmistry 25% reserved, Tarot 15% reserved). When 2+ sciences confirm the same theme,
confidence score rises. Phase 2 adds Palmistry + Tarot triggers.

## Integration Pattern (how other modules call the engine)

```python
from knowledge_engine import KnowledgeEngine

engine = KnowledgeEngine(db)

# Single science — Kundali report
rules = await engine.scan_chart(chart_data, categories=["career"], max_rules=30)
narrative = await engine.generate_narrative(
    rules, chart_data, report_type="career",
    voice_blend="classical+modern_analytical"
)

# Cross-science — when user has both astro + numerology data
combos = await engine.scan_cross_science(
    astro_chart=chart_data,
    numerology_data={"life_path": 1, "expression": 8},
    categories=["career"]
)
```

## Key Constraints

- MongoDB (Motor async) — already in stack, no new DB
- No Redis in Phase 1 — indexed MongoDB queries sufficient at current scale
- Claude model: `claude-sonnet-4-6` for narrative generation
- Rule evaluation: < 500ms for up to 1000 rules
- Narrative generation: < 8s detailed, < 3s summary
- `library_admin` role must not grant access to `/admin/dashboard` and vice versa

## Full Specification

Read `.claude/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` before starting. It contains:
- Complete MongoDB schema for all 4 collections
- All 13 rule condition types with field definitions
- Author voice profiles and narrative bridge types
- Cross-science combination schema and scoring logic
- `KnowledgeEngine` class method signatures with docstrings
- Yoga detection library (30-50 classical yogas)
- Seed data breakdown (~300 rules, sources, categories)
- Vedic reference rules (aspects, exaltation/debilitation, Moolatrikona,
  planetary friendships, life area mappings, deity/color/direction remedies)
- Library Console tab-by-tab spec
- Phase 1 vs Phase 2 boundary table
- Full acceptance criteria checklist

---

> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Stack: FastAPI (Render) + React 18 (Vercel) + MongoDB + pyswisseph 2.10.x
