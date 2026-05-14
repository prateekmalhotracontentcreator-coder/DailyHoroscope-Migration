# Commission I — Build Order
> To: Codex
> From: EverydayHoroscope / Temple Team (Prateek + Claude)
> Date: 10 April 2026
> Status: **ARCHITECTURE LOCKED — THIS IS THE BUILD ORDER**
> Contract: `CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` (read in full before starting)

---

## 1. Context

We have completed three rounds of advisory consultation — your simulation and arbitration responses, reviewed in full by the Temple Team. The contract is now locked. This document is the transition from advisory to build.

**What to read before starting, in this order:**
1. `CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` — full spec, all 22 sections
2. `CODEX_PARAPHRASE_WIM.md` — paraphrase pipeline instructions (governs `extract_book.py`)
3. `CODEX_COMMISSION_I_BRIEF.md` — background + advisory questions (context only — decisions already made)

---

## 2. What We Accepted from Your Advisory Response

We accepted the following recommendations without modification:

| Topic | Your recommendation | Status |
|---|---|---|
| Embedded passages Phase 1 | Lock embedded; add `passage_ref_id: null` for Phase 2 migration | ✅ Locked (TD-11) |
| MongoDB collections for author_voices + narrative_bridges | Confirmed — not seeded JSON | ✅ Locked (TD-03) |
| Strategy C stale-read refresh | Accepted; import endpoint returns `index_refreshed` separately | ✅ Locked (TD-12) |
| New rule schema fields | claim_axis, claim_scope, claim_polarity, timing_bias, strength_band, subject_scope | ✅ Locked (TD-15) |
| Contradiction detection formula | C = 0.40×polarity + 0.35×timing + 0.15×strength + 0.10×authority_overlap | ✅ Locked (TD-16) |
| Supersession table + confidence-delta + MCDA hybrid | Accepted as runtime architecture | ✅ Locked (TD-17) |
| tension_block JSON structure | Accepted as specified | ✅ Locked (TD-20) |
| Representation mode thresholds | synthesis/tension/honest_uncertainty thresholds accepted | ✅ Locked (TD-21) |
| Defer Bayesian/D-S to Phase 3 | Accepted — re-evaluation now flagged for Phase 2 (see Section 3) | ✅ Locked (TDF-03) |

---

## 3. What the Temple Team Modified or Added

These are the decisions that **differ from your advisory recommendations**. Design to these exactly.

### 3a — Backbone Science Is Module-Determined, Not Fixed [CRITICAL]

You recommended Vedic Astrology as the static lead science across all reports. The Temple Team overrides this.

**Locked decision (TD-13):** The backbone science is determined by which report module the user opens:

| Module | Backbone science | Behaviour |
|---|---|---|
| Brihat Kundali / Jyotish Report | vedic_astrology | Astrology leads |
| Numerology Report | numerology | Numerology leads |
| Palmistry Report | palmistry | Palmistry leads |
| KP Report | kp | KP leads |
| Daily Guidance | vedic_astrology | Astrology leads |

Every report evaluation must accept `backbone_science_id` in the request context. Secondary sciences serve as precision layers — not competitors. The supersession table governs secondary science priority only.

**Strategic reason:** Users who believe in Numerology or Palmistry as their primary tool must feel that science is sovereign in its own module. This is the platform's differentiation.

### 3b — Tranche Filter Is Phase 1 Full Build [CRITICAL]

You suggested deferring the Tranche Filter rule engine to Phase 2. The Temple Team overrides this.

**Locked decision (TD-18):** The Tranche Filter is a **Phase 1 full rule engine build** — not a passthrough.

The filter sits between contradiction detection and the narrative engine. It applies If-Then rules based on user circumstance data to suppress false negatives before the evidence packet is sent to Claude. Example:

```python
IF family_wealth_tier = "high" AND claim_axis = "financial_security"
THEN dampen effective_confidence of negative financial claims from secondary sciences by 0.40
```

Seeded rules must cover at minimum: financial_security, partnership_stability, career_growth, health_vitality.

The questionnaire UI that *populates* this data is a separate commission (Commission I-Q). Phase 1 Tranche Filter runs on whatever user context data exists at time of report generation; it gracefully passes through when context is absent.

### 3c — Full Arbitration Runtime and MCDA Are Phase 1 Spec, Phase 2 Runtime

**Locked decisions (TDF-P1, TDF-P2):**
- Full schema and spec for MCDA + supersession + confidence-delta are Phase 1 — design to the full spec.
- Phase 1 *runtime behaviour* uses a simplified execution: backbone science leads; secondary science adds supporting note; surface tension mode if C ≥ 0.55. No full MCDA scoring matrix in Phase 1 runtime.
- Full runtime implementation in Phase 2 once case study validation (Section 20) confirms thresholds empirically.

Build the schema and the interface fully. The runtime logic grows into it.

### 3d — Bayesian Re-Evaluation Moved to Phase 2 (Not Phase 3)

We have 1,000+ published case studies of public figures (known birth data + documented life outcomes). This changes your data maturity assessment. Bayesian likelihood ratios can be estimated from this dataset — not from subjective priors.

The case study validation pipeline (Section 20 of contract) must be built in Phase 1.2. Results from that pipeline are what enable Bayesian to move from Phase 3 to Phase 2. Design the `case_studies` MongoDB collection and validation tooling as specified.

---

## 4. New Features Added — Read These Contract Sections

Three new sections were added to the contract after your advisory. You must read and implement these:

### Section 19 — Arc Angel: 12 Areas of Life User Profile

A persistent left nav panel showing the user's standing across 12 life domains with a 10-year forward horizon. This is the platform's master validation layer — every module report must correlate its output back to the relevant Arc Angel domain(s).

**UI spec:** 4-column table (Domain with landscape-rotated text | Auspicious Periods | Inauspicious Periods | Confidence % as Donut chart). Premium-gated. 10-year horizon.

**12 domains (exact names — do not alter):**
1. Health & Fitness
2. Career & Work
3. Finances
4. Intellectual Life & Learning
5. Emotional Life
6. Spirituality
7. Love Relationships
8. Family Life
9. Social Life & Friendship
10. Adventure & Travel
11. Environment
12. Creativity & Hobbies

**New MongoDB collection required:** `user_arc_angel_profile` — full spec in Section 19.

**Placement in build sequence:** Phase 1.2 (after core engine is live). The computation backend (`scan_chart()` must be running first).

### Section 20 — Case Study Validation Pipeline

1,000+ published case studies are available as the Knowledge Engine's empirical acceptance test suite. Phase 1 books contain approximately 130 structured cases.

**New MongoDB collection required:** `case_studies` — full spec in Section 20.

**Library Console addition:** Case Studies tab (Tab 6) in Phase 1.2 — import structured case study JSON, run batch validation against the live engine, view accuracy scores.

**This is what enables Bayesian calibration in Phase 2.** Build it.

### Section 22 — Report Quality Evaluation Framework

Defines how the first Brihat Kundali report will be evaluated. You must understand this section because it constrains what "done" means for CPath-1 item 6 (the first complete report route).

**Success criteria for the Knowledge Engine Brihat Kundali:**
- Overall rubric score ≥ 18/25 across 5 dimensions
- Classical Grounding ≥ 4/5 — non-negotiable
- Zero unacknowledged internal contradictions
- Case study accuracy ≥ 70% on 10 known-outcome charts
- Arc Angel alignment ≥ 70%

The evaluation methodology uses a blind comparison against the existing direct-LLM Brihat Kundali report on identical birth credentials.

---

## 5. Build Sequence — Mandatory Order

Do not treat the contract as a flat feature list. Build in this sequence.

### CPath-1 (Hours 1–80) — Core Engine: Build These First

| # | Deliverable |
|---|---|
| 1 | MongoDB schemas — all collections, all TD-15 fields, indexes |
| 2 | `extract_book.py` + AI Paraphrase pipeline (per `CODEX_PARAPHRASE_WIM.md`) |
| 3 | In-memory inverted index + `scan_chart()` |
| 4 | `generate_narrative()` + Claude API Narrative Planner |
| 5 | Library Console: Rules Browser + Import endpoint + Approval workflow |
| 6 | One complete Brihat Kundali report API route end-to-end |
| 7 | Phase 1 simplified arbitration runtime (backbone leads; secondary acknowledges; tension if C ≥ 0.55) |
| 8 | Tranche Filter rule engine with seeded domain rules (Phase 1 domains: financial_security, partnership_stability, career_growth, health_vitality) |

CPath-1 is the product. Everything else is built on top of it.

### Phase 1.2 (Hours 80–125)

| # | Deliverable |
|---|---|
| 9 | Coverage Dashboard heatmap (Library Console) |
| 10 | Arc Angel profile computation + `user_arc_angel_profile` collection |
| 11 | Arc Angel left nav panel UI (4-column layout per Section 19) |
| 12 | Remaining report API routes (Numerology, Longevity, etc.) |
| 13 | Case Study extraction + batch validation (50–100 Phase 1 cases) |
| 14 | `user_context_profile` schema + β/γ hook integration |

### Phase 1.3 (Hours 125–150 — if budget holds)

| # | Deliverable |
|---|---|
| 15 | Test Console + Voice Profiles editor (Library Console tabs 4–5) |
| 16 | `science_registry` editor in Library Console |
| 17 | Threshold recalibration using case study results |

### Out of Scope for Commission I (Separate Phase 1 Commissions)

| Commission | Scope |
|---|---|
| Commission I-Q | Questionnaire UI + flow + β/γ population logic |
| Commission I-K | Kota Chakra full calculation (parents birth data engine) |
| Commission J | World Context Engine (α multiplier via global calendars) |

Do not build these inside Commission I. Build the schema hooks and integration interfaces only.

---

## 6. Schema Quick Reference — What Is New vs What You Already Specified

These are the additions / changes the Temple Team made after your advisory. Everything else is as you designed it.

### New fields on every `interpretation_rules` document

```json
{
  "claim_axis": "marriage_timing",
  "claim_scope": "event_timing",
  "claim_polarity": "negative",
  "timing_bias": "late",
  "strength_band": "high",
  "subject_scope": "self",
  "authority_override": null,
  "mutually_exclusive_with": [],
  "passage_ref_id": null
}
```

### New field on every report request context

```json
{
  "backbone_science_id": "vedic_astrology",
  "alpha": 1.0,
  "beta": 1.0,
  "gamma": 1.0
}
```

### New MongoDB collections (Phase 1)

| Collection | Section | Phase |
|---|---|---|
| `science_registry` | 17.1 | CPath-1 |
| `user_arc_angel_profile` | 19 | Phase 1.2 |
| `user_context_profile` | 15 | Phase 1.2 |
| `case_studies` | 20 | Phase 1.2 |

All other collections (`interpretation_rules`, `author_voices`, `narrative_bridges`, `import_batches`) are as previously specified.

---

## 7. What We Need From You Now

Before you start the build, confirm the following:

**7a — Build sequence acceptance**
Do you accept the CPath-1 priority ordering? If any CPath-1 item has a hidden dependency that changes its position, flag it before starting.

**7b — Revised effort estimate**
Given the new additions (Arc Angel, Case Study Pipeline, Evaluation Framework, Tranche Filter as Phase 1 full build), does the 125–150h estimate still hold? If Arc Angel and Case Studies push total effort beyond 150h, tell us what to defer from Phase 1.2 to Phase 1.3 — do not silently expand scope.

**7c — Confirmation of build start**
Confirm you have read:
- [ ] `CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` (all 22 sections)
- [ ] `CODEX_PARAPHRASE_WIM.md`
- [ ] This document

Then begin with CPath-1 item 1: MongoDB schema definitions.

---

> Questions to the Temple Team: direct them back through Prateek as before.
> Amendment Contracts for new books: use `CODEX_LIBRARY_AMENDMENT_TEMPLATE.md`.
> All deliverables committed to `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`, branch `main`.
