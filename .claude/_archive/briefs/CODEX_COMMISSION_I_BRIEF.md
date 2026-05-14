# Codex Advisory Brief — Commission I: Jyotish Knowledge Engine
> To: Codex
> From: EverydayHoroscope / Temple Team (SkyHound Studios)
> Date: 10 April 2026
> Status: PRE-SPEC CONSULTATION — We are seeking your architectural input BEFORE finalising the build contract
> Full Draft Spec: `.claude/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` (shared for your review — not yet final)

---

## Why We Are Writing Before the Contract

Commission H (Longevity Report) is live. Commission I is the **most architecturally significant module in the entire platform** — it becomes the interpretation backbone that every other module calls. We want to do this right, not fast.

Before we finalise the build contract, we want your considered input on:
- Whether our proposed architecture is the right one
- Where you would do things differently
- What risks you see that we may not have spotted
- What questions you need answered before you can scope this accurately

This brief explains what we are building and why. The draft contract document gives you the schema and method signatures we are currently thinking. Please read both and send us your recommendations.

---

## 1. What We Are Building

The **Jyotish Knowledge Engine** is an internal infrastructure module — not a user-facing page. It does one thing: it takes a computed Vedic birth chart and returns a coherent, book-grounded, multi-paragraph interpretation narrative.

Every module on the platform (Kundali, Longevity, Horoscopes, Numerology, Palmistry, Tarot) currently generates interpretations via direct LLM prompting. The Knowledge Engine replaces that with something better: **structured rule matching against a curated library of classical and modern texts**, followed by LLM narrative generation grounded in those matched passages.

The result: interpretations that cite actual book passages, blend multiple authorial voices, surface contradictions honestly, and scale as we add more books — without rewriting any code.

### Architecture in Three Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: NARRATIVE LAYER (Claude API)                      │
│  Receives matched rules + chart context                     │
│  → generates coherent multi-paragraph prose                 │
│  → never bullet points, always full narrative               │
└────────────────────────┬────────────────────────────────────┘
                         │ matched rules + passages + context
┌────────────────────────┴────────────────────────────────────┐
│  Layer 2: RULE ENGINE (Python / FastAPI)                    │
│  Evaluates chart data against rule conditions               │
│  Scores relevance, resolves conflicts between sources       │
│  Filters by category: career / health / relationships etc.  │
└────────────────────────┬────────────────────────────────────┘
                         │ chart positions + dashas + transits
┌────────────────────────┴────────────────────────────────────┐
│  Layer 1: DATA LAYER (MongoDB)                              │
│  Hierarchical Interpretation Database                       │
│  Structured rules extracted from classical + modern texts   │
│  If-Then conditions, multi-source attribution, full passages │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. The Confirmed Workflow — Architecture We Have Decided

This part is settled. We are not asking for input here — we want you to understand the model before advising on the technical details.

### Books Stay on the Workstation. Always.

No book content ever touches the production server. The Library Console has **no file upload feature**. Books are retained on the Temple Team's Mac workstation in OCR format.

### The Data Flow

```
Your Workstation          Codex (local execution)          MongoDB (Live DB)
OCR books stored    →   Amendment Contract issued    →   extraction script runs
                                                                  ↓
                                                      interpretation_rules populated
                                                                  ↓
                                               Library Console (review + approve)
```

### Phase 1 — Full Library Schema from Seed Books

Codex builds the full schema, voice profiles, bridge phrases, and foundational rule set from the Phase 1 seed books (listed below). Everything else grows on top of this without schema changes.

**Phase 1 seed files to be created in `backend/data/`:**
- `seed_rules.json` — extracted rules from Phase 1 books
- `seed_cross_science.json` — cross-science combos (Astrology + Numerology, Phase 1)
- `seed_voices.json` — author voice profiles (classical, modern_analytical, kp_technical, spiritual, popular)
- `seed_bridges.json` — narrative bridge phrases (~30 types)

### Phase 2+ — Amendment Contracts

For every book added after Phase 1, the Temple Team assesses the book internally, fills in the `CODEX_LIBRARY_AMENDMENT_TEMPLATE.md`, and issues a targeted Amendment Contract. Codex extracts and pushes. Temple Team reviews in Library Console and approves or requests corrections. One book, one contract, total editorial control.

---

## 3. Phase 1 Reference Books — Confirmed List

These are the books confirmed for Phase 1 extraction. Files are on the Temple Team workstation in the locations noted. Codex will receive individual Amendment Contracts for each book after Phase 1 schema is established.

### Tier 1 — Core (Mandatory for Phase 1 Schema)

| # | Title | Category | Format Available |
|---|---|---|---|
| 1 | A Text Book of Astrology | Foundational Astrology, Panchang, Charts | Index + Chapter-wise PDF |
| 2 | Lal Kitab | Astrology: Rules and Remedies | Index + Chapter-wise PDF |
| 3 | Longevity and Astro System | Longevity — Basic Concepts, Rule-Based, 30+ Case Studies | Index + Chapter-wise PDF |

### Tier 2 — Core-Optional

| # | Title | Category | Format Available |
|---|---|---|---|
| 4 | Ascendants and Astrological Tables | Astronomical Data, Muhurat Tables, Festival Rules | Index + Chapter-wise PDF |

### Tier 3 — Module Specific

| # | Title | Category | Format Available |
|---|---|---|---|
| 5 | Your Destiny Is In Your Name & DOB | Numerology | Index + Chapter-wise PDF |
| 6 | Vedic Numerology — Ank Jyotish | Numerology | Index + Chapter-wise PDF |
| 7 | Crystal Healing | Remedies / Healing | Crystal knowledge, situational areas, crystal specifics |

### Tier 4 — Classical Foundation Texts (Phase 1 — Core Rule Seed)

These are the texts from which the original seed files were planned. They are **Phase 1 mandatory** — the foundational rule library that all other books build on top of.

| # | Title | Author / Tradition | Category |
|---|---|---|---|
| 10 | Brihat Parashara Hora Shastra (BPHS) | Parashara | Foundational Vedic — all houses, planets, yogas |
| 11 | Phaladeepika | Mantreswara | Classical Vedic — planetary results, house lords |
| 12 | Saravali | Kalyana Varma | Classical Vedic — planetary combinations, results |
| 13 | How to Judge a Horoscope (Vol. 1 & 2) | B.V. Raman | Modern analytical — house-by-house interpretation |

### Tier 5 — Additional (Post-Phase 1 via Amendment Contracts)

| # | Title | Category | Format Available |
|---|---|---|---|
| 14 | A Book of 300 Important Horoscopes Vol. I | Astrology — Star Lord System, Sign Lords, Case Studies | Summary chapter guide + case studies |
| 15 | Longevity and Un-Natural Deaths | Longevity — Nakshatra System, Fundamental Rules + Case Studies | Chapter-wise PDF + case studies |

---

## 4. What We Are Asking of You — Right Now

**Do not start building yet.** We want your considered architectural recommendations first.

### Question A — Schema Design
We have proposed a 4-collection MongoDB schema: `interpretation_rules`, `author_voices`, `narrative_bridges`, `cross_science_combinations`. The full schema is in the draft contract.
- Is this the right data model?
- Would you restructure it — if so, how and why?
- How would you handle rule versioning as books are added?

### Question B — Rule Evaluation Performance
The engine needs to evaluate 300 rules at Phase 1, scaling to 10,000+ rules without schema changes or code deployments.
- What indexing strategy would you recommend on `interpretation_rules`?
- Is MongoDB the right store for this, or would you add a secondary structure (e.g. in-memory index on startup)?
- Target: < 500ms evaluation for up to 1,000 rules per request

### Question C — Extraction Script Design (`extract_book.py`)
This script runs locally on the Temple Team's workstation against OCR text. It must produce structured JSON in our rule schema. The OCR quality varies (marked High/Medium per book).
- What extraction approach would you recommend for pulling structured If-Then rules from OCR text?
- How should the script handle OCR noise (hyphenation, line breaks mid-sentence, column artifacts)?
- Should the extraction be rule-template driven, or LLM-assisted, or hybrid?

### Question D — Cross-Science Scoring
We are proposing: Astrology 40%, Numerology 20%, Palmistry 25% (reserved), Tarot 15% (reserved).
- Is a fixed-weight confidence model the right approach, or would you recommend something more adaptive?
- How should the engine handle cases where only 1 or 2 sciences match (partial confirmation)?

### Question E — Narrative Generation
We want: book-grounded narrative, never bullet points, multi-authorial voice blending, contradictions surfaced honestly.
- What prompt architecture would you recommend for this?
- How do you prevent the LLM from ignoring the provided passages and generating from training data instead?
- How should bridge phrases be injected — as part of the prompt, or as structural anchors the LLM fills in?

### Question F — Library Console Scope
We have spec'd a 5-tab Library Console at `/library` with its own `library_admin` role (separate from `/admin/dashboard`).
- Is there anything in the 5-tab spec (Rules Browser / Rule Editor / Library Import / Coverage Dashboard / Test Console) that you would simplify or restructure for Phase 1?
- What would you defer to Phase 2?

### Question G — Anything We Have Missed
Is there a meaningful risk, dependency, or design consideration we have not raised? Tell us what we are not asking.

---

## 5. How to Respond

Please return:
1. Your answers to Questions A–G above
2. Any assumptions you are making that we should confirm
3. A revised effort estimate once you have reviewed the draft contract
4. Any questions you need answered before you can proceed

Once we have your input, the Temple Team will finalise the contract and issue Commission I formally.

---

## 6. Stack Context

| Layer | Detail |
|---|---|
| Backend | FastAPI on Render (Docker, python:3.12.9-slim) |
| Frontend | React 18 on Vercel |
| Database | MongoDB via Motor (async) — already in stack |
| Astronomy | pyswisseph 2.10.x, Lahiri ayanamsa |
| AI | Claude API (`claude-sonnet-4-6`) |
| Repo | `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration` |
| Main branch | `main` (deploy-on-push to Render + Vercel) |

> No Redis in Phase 1. No new database. No book upload feature anywhere in the application. The Library Console manages rules already in MongoDB — it does not ingest source files.

---

> Full draft schema, method signatures, and acceptance criteria: `.claude/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md`
> Amendment contract template: `.claude/CODEX_LIBRARY_AMENDMENT_TEMPLATE.md`
