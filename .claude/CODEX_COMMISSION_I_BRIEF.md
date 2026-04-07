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

---

## Book Library — Working Model

**Books do NOT get uploaded into the application.** All source books (OCR format) are
retained on the client's workstation. Codex reads them locally, extracts structured
rules, and populates the MongoDB library directly.

**The workflow is:**
```
Client Workstation          Codex (local execution)        MongoDB (Live DB)
OCR books stored here  →  Amendment Contract issued  →  extraction script runs
                                                               ↓
                                                     interpretation_rules populated
                                                               ↓
                                              Library Console (client reviews + approves)
```

**No book upload feature is required** in the Library Console or anywhere in the
application. The Library Console is purely for reviewing, editing, and managing rules
that are already in the database.

**Phase 1 — 4 Seed Books:**
Codex designs the full library schema and populates it using 4 base resource books
provided by the client. These 4 books establish the schema, the voice profiles, the
bridge phrases, and the foundational rule set.

**Subsequent Books — Amendment Contracts:**
For every additional book, the client conducts an internal assessment of how they
want the library updated, then issues a targeted **Amendment Contract** to Codex.
Each amendment specifies: which book, which modules it covers, what categories to
extract, and any special handling instructions. Codex runs the extraction and updates
the DB. This keeps the client in editorial command at all times.

**10 books are ready** across modules: Vedic Astrology, KP, Numerology, Palmistry,
Tarot. These will be commissioned in batches via Amendment Contracts after Phase 1
is live.

---

## What You'll Build

### Backend
1. `backend/knowledge_engine.py` — Core engine: rule scanner, scorer, conflict resolver,
   and Claude narrative generator (narrative-first, full prose — never bullet points)
2. `backend/knowledge_router.py` — API endpoints under `/api/knowledge`:
   - `POST /api/knowledge/interpret` — generate interpretation for a chart
   - Rule CRUD: GET / POST / PUT / DELETE `/api/knowledge/rules`
   - `POST /api/knowledge/rules/import` — bulk import from pre-extracted JSON
   - `GET /api/knowledge/rules/stats` — coverage statistics
3. `backend/scripts/extract_book.py` — **local-only extraction script** (not deployed to
   Render). Run locally by Codex against OCR book text to produce structured JSON,
   then import that JSON into MongoDB via the import endpoint. This is how new books
   get added — script runs on workstation, result pushed to DB.

### MongoDB Collections (4 new)
- `interpretation_rules` — the rule library (13 condition types, full-text book passages)
- `author_voices` — 5 voice profiles (classical, modern_analytical, kp_technical, spiritual, popular)
- `narrative_bridges` — ~30 bridging phrases for stitching multi-source text blocks
- `cross_science_combinations` — ~50 multi-factor confirmation combos (Astrology + Numerology)

### Phase 1 Seed Data (from 4 base books)
Codex extracts and structures rules from the 4 seed books provided by the client.
Output written to `backend/data/`:
- `seed_rules.json` — rules extracted from 4 seed books (~300 expected)
- `seed_cross_science.json` — ~50 cross-science combos (astrology + numerology)
- `seed_voices.json` — 5 author voice profiles
- `seed_bridges.json` — ~30 narrative bridge phrases

The schema must be designed to grow from ~300 rules (Phase 1) to 10,000+ rules
(as Amendment Contracts bring in all 10 books and beyond) — **without any schema
changes or code deployments.** Sources, books, and traditions are all data, not code.

### Library Console (standalone — NOT part of Operations Admin Console)
- New page: `frontend/src/pages/LibraryConsolePage.jsx`
- Route: `/library`
- Role: `library_admin` — separate from `admin` role, add to `auth_utils.py`
- **Completely decoupled from `/admin/dashboard`** — different entry point, different role
- **No book/file upload feature** — books stay on workstation, rules arrive via import endpoint
- **5 tabs:**
  - **Rules Browser** — filterable table, inline edit, active/inactive toggle, priority slider
  - **Rule Editor** — condition builder, full-text passage manager, modifier builder,
    conflict checker, live preview
  - **Library Import** — import pre-extracted JSON (output of `extract_book.py`),
    validation preview, duplicate detection, import history log
  - **Coverage Dashboard** — 12×9 heatmap, gap analysis, category donut chart,
    source bar chart, cross-science coverage panel
  - **Test Console** — input chart → matched rules + narrative side-by-side,
    voice/depth selectors, citation trail showing which book passages were used

---

## Amendment Contract Model

Each new book after Phase 1 follows this process:

```
1. Client internal assessment → decides categories, depth, special instructions
2. Client issues Amendment Contract (new .md file in .claude/)
3. Codex runs extract_book.py locally against OCR text → produces JSON
4. Codex imports JSON → MongoDB via import endpoint
5. Client reviews new rules in Library Console (Rules Browser + Test Console)
6. Client approves or requests corrections
7. Amendment closed
```

This model means:
- Client always reviews before rules go live
- No book content ever touches the production server
- Each book is a discrete, traceable batch in the import history
- Codex effort per amendment is predictable and scoped

---

## Key Design Principles

**Narrative-First (not keyword mapping):**
Rules store 500+ word verbatim book passages alongside summaries. The LLM is grounded
in actual classical text — reducing hallucination and delivering genuinely deep readings.

**Author Voice Blending:**
`generate_narrative(voice_blend="classical+modern_analytical")` — the engine blends
classical Sanskrit-tradition tone with modern psychological astrology for each report type.

**Narrative Bridges:**
When Book A says "wealth" and Book B says "losses" for the same placement, the engine
renders them as "competing energies" using bridging phrases — nuanced, multi-perspective.

**Cross-Science Confirmation:**
Phase 1: Astrology + Numerology unified scoring (Astrology 40%, Numerology 20%,
Palmistry 25% reserved, Tarot 15% reserved). When 2+ sciences confirm the same theme,
confidence score rises. More sciences added via Amendment Contracts.

---

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

# Cross-science — astro + numerology unified reading
combos = await engine.scan_cross_science(
    astro_chart=chart_data,
    numerology_data={"life_path": 1, "expression": 8},
    categories=["career"]
)
```

---

## Key Constraints

- MongoDB (Motor async) — already in stack, no new DB
- No Redis in Phase 1 — indexed MongoDB queries sufficient at current scale
- Claude model: `claude-sonnet-4-6` for narrative generation
- `extract_book.py` — local script only, never deployed to Render
- Rule evaluation: < 500ms for up to 1000 rules
- Narrative generation: < 8s detailed, < 3s summary
- `library_admin` role must not grant access to `/admin/dashboard` and vice versa
- Schema must support 10,000+ rules without changes — all sources are data, not code

---

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
