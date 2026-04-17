# EverydayHoroscope — Codex Master Roadmap
> **Single source of truth for all Codex commissions, technical decisions, and implementation gaps.**
> Owner: Prateek Malhotra + Temple Team
> Last updated: 17 April 2026 — Codex Phase 1.2 sprint plan confirmed; TD-26/TD-27 specs received; Ch 53 ingested

---

## Document Registry — One Document Per Type

| Document | Location | Purpose | Update cadence |
|---|---|---|---|
| `CLAUDE.md` | root | Claude Code session guide, infra, key files | Per major feature |
| `PROJECT_STATUS.md` | root | Live feature status across the whole product | Per release |
| `KNOWLEDGE_ENGINE_HANDOVER.md` | root | KE ingest progress, DB state, next session tasks | Every KE session |
| `KNOWLEDGE_ENGINE_ROADMAP.md` | root | Chapter ingest queue, RTF conversion queue, scripts | Per ingest batch |
| `KNOWLEDGE_ENGINE_STRATEGY.md` | root | Architecture philosophy, book coverage, quality decisions | Per strategic decision |
| `CODEX_MASTER_ROADMAP.md` | root | **This file** — Commission registry, TD tracker, Gap tracker | Every session |
| `TECH_STRATEGY.md` | root | 3-layer report model, Vector DB decision, language tiers, scoring | Per architecture decision |
| `CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` | `.claude/` | Full locked architecture contract (TD-01 to TD-25) | Only via formal TD addition |
| `CODEX_WAYS_OF_WORKING.md` | `codex-deliveries/` | Codex engagement protocol, completed commissions log | Per Codex engagement |

**Rule: No session creates its own version of any document above. All updates go directly to these canonical files.**

---

## Commission Registry

### Active / In-Progress

| Commission | Name | Contract | Status | Est. Hours | Dependency |
|---|---|---|---|---|---|
| **I** | Jyotish Knowledge Engine | `CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` | Architecture LOCKED — Build Phase 1.1 complete; Phase 1.2 blocked on G-01/G-03/G-05–G-08 | 125–150h | None |
| **I-Q** | Questionnaire (β/γ inputs) | `CODEX_COMMISSION_I_BRIEF.md` §TD-25 | Schema locked (Phase 1); UI + computation deferred | Separate | Commission I |
| **I-K** | Kota Chakra + Parents Data | `CODEX_COMMISSION_I_BRIEF.md` §TD-22 | Schema Phase 1; full integration Phase 2 | Separate | Commission I |
| **H** | Ayur Jyotish (Longevity Report) | `CODEX_LONGEVITY_REPORT_CONTRACT.md` | Pending — must build after Commission I | ~48h | Commission I |
| **J** | World Context Engine (macro α) | TBD — Commission J brief needed | Phase 2; Commission I builds hooks only | TBD | Commission I complete |

### Frontend Commissions — Pending Build

| Commission | Name | Contract | Status |
|---|---|---|---|
| **F-1** | Individual Reports + Kundali UI | `CONTRACT_APPOINTMENT_INDIVIDUAL_REPORTS_AND_KUNDALI.md` | Pending |
| **F-2** | Love Engagement Module | `CONTRACT_LOVE_ENGAGEMENT_MODULE.md` | Pending |
| **F-3** | Notification Engine | `CONTRACT_NOTIFICATION_ENGINE.md` | Pending |
| **F-4** | Astro-Tarot Fusion router | (no contract yet) | Pending |

### Completed Commissions

| # | Deliverable | File | Status |
|---|---|---|---|
| 1 | vedic_calculator.py (flatlib → pyswisseph) | `backend/vedic_calculator.py` | ✅ Live |
| 2 | panchang_router.py (pyswisseph engine) | `backend/panchang_router.py` | ✅ Live v11-swiss |
| 3 | Premium Ankjyotish Numerology | `backend/numerology_router.py` | ⚠️ Backend live; report render investigation pending |
| 4 | Tarot 78-card SVG bundle | `frontend/public/tarot_cards.json` | ✅ Live |
| 4b | Tarot router DEFAULT_CARDS → 78 | `backend/tarot_router.py` | ✅ Live |
| 5 | Panchang per-date endpoint | `backend/panchang_router.py` | ✅ Live |
| 6 | Tarot daily reminder (3 endpoints) | `backend/tarot_router.py` | ✅ Live |

---

## Technical Decision Tracker (TD-01 → TD-25 + Deferred)

### Round 1 Decisions — All LOCKED

| TD | Topic | Decision | Implemented |
|---|---|---|---|
| TD-01 | Cross-science scoring model | 3-layer: fixed weights + qualitative tier multipliers + α/β/γ contextual | ⚠️ Partial — Layer 1 weights ✅; tier multipliers ✗ (G-02); α/β/γ not wired (G-01) |
| TD-02 | AI Paraphrase pipeline | Codex leads via WIM; Claude reviews flagged passages only | ⬜ Phase 2 |
| TD-03 | author_voices + narrative_bridges | Stay as MongoDB collections | ✅ |
| TD-04 | Library Console scope | Full 5-tab spec; no Phase 2 deferral | ✅ Schema; ⬜ UI build |
| TD-05 | Excerpt policy | AI-generated equivalents only — no verbatim copyrighted text | ✅ Policy; note: astrological if-then rules are facts not copyright |
| TD-06 | Citation policy | Internal Test Console only; end-user reports attribute generically | ✅ Policy |
| TD-07 | Science Arbitration | Schema-ready Phase 1; framework confirmed | ⚠️ Schema ✅; runtime absent (G-03/G-05/G-06) |
| TD-08 | Schema simulation | 3 simulations requested before locking | ✅ Complete |
| TD-09 | Revised effort estimate | 125–150h accepted for lean Phase 1 | ✅ |
| TD-10 | World Context Engine | Commission J separate; Commission I builds hooks | ⬜ Hooks exist (alpha field); Commission J not started |

### Round 2 Decisions — All LOCKED

| TD | Topic | Decision | Implemented |
|---|---|---|---|
| TD-11 | Rule document structure | Embedded paraphrased passages Phase 1; migration-ready field added | ✅ |
| TD-12 | Index refresh strategy | Strategy C (stale-read tolerant) | ✅ |
| TD-13 | Backbone science | Module-determined, not static Vedic | ✅ `_backbone_adjusted_weight()` |
| TD-14 | Supersession table scope | Secondary science priority only | ⚠️ Schema ✅; runtime lookup absent (G-04) |
| TD-15 | New rule schema fields | 7 required: claim_axis, claim_scope, claim_polarity, timing_bias, strength_band, subject_scope, authority_override | ✅ All in schema |
| TD-16 | Contradiction detection | C = 0.40×polarity + 0.35×timing + 0.15×strength + 0.10×authority; flag if C ≥ 0.55 | ✗ Not implemented (G-03) |
| TD-17 | Arbitration framework | Supersession → confidence-delta → representation mode | ✗ Not implemented (G-04/G-05) |
| TD-18 | Tranche layer | Full rule engine Phase 1 with If-Then tranche filter | ✅ `tranche_filter.py` complete |
| TD-19 | Questionnaire-driven β/γ | Schema Phase 1; UI is Commission I-Q | ✅ Schema; ⬜ Computation |
| TD-20 | tension_block JSON | Evidence packet structure per Section 17.3 | ⚠️ Schema ✅; builder absent (G-06) |
| TD-21 | Representation mode thresholds | synthesis C<0.30; tension 0.30–0.75; honest_uncertainty C>0.75 | ✗ Not implemented (G-05) |
| TD-22 | Kota Chakra / Parents data | Schema Phase 1; full integration Phase 2 (Commission I-K) | ✅ Schema |

### Additional Locks

| TD | Topic | Decision | Implemented |
|---|---|---|---|
| TD-23 | Arc Angel — 12 Areas of Life | Left Nav persistent; correlates all modules to 12 Bhavas | ⚠️ Schema ✅; computation absent (G-07/G-08/G-09) |
| TD-24 | Case Study Validation | 1,000+ public figures; 50 Numerology, 300 Longevity, rest other | ⬜ Schema ✅; pipeline not built (G-11) |
| TD-25 | Questionnaire Commission | Separate Phase 1 commission outside Commission I hours | ⬜ Not started |

### Deferred Technical Decisions

| TDF | Topic | Decision | Phase |
|---|---|---|---|
| TDF-P1 | Full Arbitration Runtime | Spec Phase 1; runtime after case study validation | Phase 2 |
| TDF-P2 | MCDA Internal Scoring | Spec locked Phase 1; after empirical calibration | Phase 2 |
| TDF-01 | source_passages collection | Migrate at 3,000 rules | Phase 2 |
| TDF-02 | Double-buffer index refresh | If import frequency grows | Phase 2 |
| TDF-03 | Bayesian/Dempster-Shafer | Re-evaluate after 1,000+ case studies | Phase 2 |
| TDF-04 | Kota Chakra full integration | Commission I-K | Phase 2 |

### New TDs — Specs Received from Codex (17 Apr 2026)

**TD-26 — Country Kundali as Alpha Signal [Phase 2]** `SPEC RECEIVED — AWAITING CONTRACT ENTRY BY CODEX`
- `alpha` stays `float | ContextSignal` Phase 1. No schema change.
- Phase 2: typed `CountryKundaliSignal` subtype under `alpha` umbrella.
- `dasha_alignment` = normalised 0.0–1.0 compatibility between individual's active maha/antara lords and country chart's active mundane period lords. Interim proxy (transit support/stress) allowed before mundane dasha engine ready.
- Weighting: same country=100/0 · abroad <2yr=70/30 · abroad 2–7yr=interpolate · abroad >7yr=30/70
- `alpha_score = (birth_country_alignment × birth_weight) + (residence_country_alignment × residence_weight)`
- Auditability: payload includes source countries, alignments, weighting method, years-lived basis, factor trace.
- Do not build before Commission J.

**TD-27 — Forecast Tier / Life Area Outlook [Phase 2]** `SPEC RECEIVED — AWAITING CONTRACT ENTRY BY CODEX`
- Field: `forecast_tier` · User label: `Life Area Outlook` [FOUNDER CONFIRMATION PENDING]
- Outcome-valence layer — not quality or confidence. Coexists with `representation_mode`, `confidence_tier`, `period_quality`. Must not override any.
- Computed per section/domain only (never per rule, never per full report).
- Weighted polarity: positive rules → +mass; negative → −mass; mixed/neutral → dampen. Weights: `effective_confidence` + backbone priority + scored intensity.
- Bands: `Excellent` · `Very Good` · `Good` · `Cautious` · `Difficult` · `Critical`
- Guardrail: `representation_mode = honest_uncertainty` → suppress Excellent/Critical; collapse to middle bands.
- `period_quality` stays as 3-band layer. `forecast_tier` is finer 6-band overlay, not a replacement.
- Phase 2 internal only first. User-facing after wording validation.

---

## Implementation Gap Tracker

Gaps found by Temple Team audit on 17 April 2026. All are between the locked CONTRACT and the current code.

| Gap | Description | Linked TD | Risk | Phase 1.2 Blocker | Status |
|---|---|---|---|---|---|
| **G-01** | α/β/γ multipliers never applied in `_score_rule()` | TD-01 | 🔴 HIGH | ✅ Yes | ✅ **DONE** — commit `57e347a`; gate passed 18 Apr |
| **G-02** | Confidence tier multipliers (×0.60→×1.15) not computed | TD-01 | 🟡 MOD | Partial | ⬜ Sprint 2+ (claim clustering first) |
| **G-03** | Contradiction C-score formula absent | TD-16 | 🔴 HIGH | ✅ Yes | 🔄 Sprint 2 |
| **G-04** | Supersession table runtime lookup missing | TD-14/TD-17 | 🟡 MOD | No | 🔄 Sprint 2 — `science_registry` now seeded |
| **G-05** | Representation mode selection absent | TD-21 | 🔴 HIGH | ✅ Yes | 🔄 Sprint 2 |
| **G-06** | Tension block builder from matched rules absent | TD-20 | 🔴 HIGH | ✅ Yes | 🔄 Sprint 2 |
| **G-07** | Arc Angel `period_quality_now` never computed | TD-23 | 🔴 HIGH | ✅ Yes | ⬜ Sprint 3 |
| **G-08** | Arc Angel `period_quality` per domain never assigned | TD-23 | 🔴 HIGH | ✅ Yes | ⬜ Sprint 3 |
| **G-09** | 10-year auspicious/inauspicious window absent | TD-23 | 🔴 HIGH | ✅ Yes | ⬜ Sprint 3 |
| **G-10** | β/γ score computation from questionnaire absent | TD-19/TD-25 | 🟡 MOD | No | ⬜ Commission I-Q |
| **G-11** | Case study validation runner absent | TD-24 | 🟢 LOW | No | ⬜ Phase 1.2 script |
| **G-12** | World Context Engine α population (always 1.0) | TD-10 | 🟢 LOW | No | ⬜ Commission J / Phase 2 |

### Build Sequence for Gaps — CONFIRMED BY CODEX (17 Apr 2026)

**Commission structure:** One Commission I Phase 1.2 package with 3 gated sprint checkpoints.

```
Sprint 1 — Scoring foundation                               [8–12h]  ✅ COMPLETE — 18 Apr 2026
  G-01  Wire α/β/γ into _score_rule()            [knowledge_engine.py]
  Gate: ✅ ALL PASS — neutral 1.0 · floor 0.78 · ceiling 1.22 · alpha-only 1.06 · beta-only 0.95 · gamma-only 1.08
  commit: 57e347a | TD-26 + TD-27 formally locked as Sections 23+24 in CONTRACT

  G-02  Tier multipliers deferred (confirmed again by Codex 18 Apr)
  ⚠️  Convergence-tier multiplier is a per-claim/domain aggregation property.
      Must be built alongside claim clustering in Sprint 2, not bolted onto _score_rule().

Sprint 2 — Arbitration runtime                              [18–26h]  🔄 READY TO BRIEF
  G-03  Contradiction C-score formula             [knowledge_engine.py]
  G-05  Representation mode selector              [knowledge_engine.py]
  G-06  Tension block builder                     [knowledge_engine.py]
  G-04  Supersession table runtime lookup         [knowledge_engine.py]
  ✅  science_registry SEEDED — 4 documents (vedic_astrology/numerology/palmistry/tarot)
      Script: backend/scripts/seed_science_registry.py
      Codex interim fallback map also available: DEFAULT_SUPERSESSION_MAP (in Sprint 2 brief)

Sprint 3 — Arc Angel computation                            [16–24h]  ⬜ After Sprint 2 gate
  G-07  period_quality_now per domain             [knowledge_engine.py + server.py]
  G-08  period_quality per prediction             [knowledge_engine.py]
  G-09  10-year auspicious/inauspicious windows   [knowledge_engine.py]
  ⚠️  Must consume POST-ARBITRATION, POST-CONVERGENCE output — not raw matched rules.

TOTAL Phase 1.2: 42–62h

Sprint 4 — Separate commissions (not Phase 1.2)
  G-10  β/γ from questionnaire                   [Commission I-Q]
  G-11  Case study validation runner             [Phase 1.2 script, Temple Team]
  G-12  World Context Engine α                   [Commission J / Phase 2]
```

**Acceptance gates:**
- Sprint 1 gate: ✅ PASSED 18 Apr — scoring math correct (all 6 test cases)
- Sprint 2 gate: arbitration runtime + tension blocks correct
- Sprint 3 gate: Arc Angel period_quality computation + 10-year windows correct

**⚠️ Phase 1.2 acceptance rubric requires all 3 gates passed:**
Internal Coherence 5/5 + Arc Angel Alignment ≥70% — both fail without G-03/G-05/G-06/G-07/G-08/G-09.

---

## Pending Codex Actions

| Action | Detail | Priority | Status |
|---|---|---|---|
| Add TD-26 to CONTRACT | Spec received 17 Apr | Medium | ✅ DONE — Section 23, commit 57e347a |
| Add TD-27 to CONTRACT | Spec received 17 Apr | Medium | ✅ DONE — Section 24, commit 57e347a |
| Issue Commission I Phase 1.2 Sprint 1 | G-01 α/β/γ wiring | 🔴 High | ✅ DONE — gate passed 18 Apr, commit 57e347a |
| Seed `science_registry` | 4 documents (vedic/numerology/palmistry/tarot) | 🔴 High | ✅ Script ready — run `seed_science_registry.py --mongo-url $MONGO_URL --db-name EverydayHoroscope` |
| **Issue Commission I Phase 1.2 Sprint 2** | G-03/G-05/G-06/G-04 arbitration runtime, 18–26h | 🔴 **High** | **⬜ NEXT — brief below** |
| Commission 3 Numerology defect | Lo Shu Grid CSS missing — flat list instead of 3×3 grid | 🔴 High | ✅ DONE — commit 878edd3, deployed |
| Commission 3 Numerology — focused trace | Codex offered defect note on NumerologyPage.jsx + NumerologyReportPage.jsx failure points | Medium | ⬜ Accept offer |

---

## Commission I Phase 1.2 — Sprint 2 Brief

**To: Codex (Commission I — Jyotish Knowledge Engine)**
**Sprint 2 — Arbitration Runtime | Est. 18–26h**
**Pre-condition: Sprint 1 gate ✅ passed. `science_registry` seeded (or use fallback map below).**

---

**Scope:** Build the full arbitration runtime in `backend/knowledge_engine.py`. Four gaps, tightly coupled — deliver as a single diff.

### G-03 — Contradiction C-score formula (TD-16)

Implement the contradiction scoring function exactly per Section 16 of the CONTRACT:

```
C = 0.40×polarity_delta + 0.35×timing_delta + 0.15×strength_delta + 0.10×authority_delta
Flag as contradiction if C ≥ 0.55
```

- `polarity_delta`: 1.0 if opposing polarity (positive vs negative), 0.5 if mixed, 0.0 if same
- `timing_delta`: 1.0 if same timing window with opposite outcome, else proportionally lower
- `strength_delta`: absolute difference in `strength_band` mapped 0–1
- `authority_delta`: 0.0 if same science, scaled by hierarchy_rank difference
- Input: two matched `InterpretationRuleDocument` objects
- Output: `float` C-score + `bool` is_contradiction

### G-05 — Representation mode selector (TD-21)

Select per domain, after contradiction scoring:
- `synthesis` if convergence C < 0.30
- `tension` if 0.30 ≤ C ≤ 0.75
- `honest_uncertainty` if C > 0.75

Input: list of C-scores for matched rules in a domain. Output: `Literal["synthesis", "tension", "honest_uncertainty"]`

### G-06 — Tension block builder (TD-20)

Build `tension_block` JSON evidence packet per Section 17.3 of the CONTRACT when `representation_mode = "tension"`:

```python
{
  "rule_a_id": str,
  "rule_b_id": str,
  "c_score": float,
  "polarity_delta": float,
  "timing_delta": float,
  "strength_delta": float,
  "authority_delta": float,
  "domain": str,
  "resolution_hint": str   # brief note on which rule has higher authority
}
```

### G-04 — Supersession table runtime lookup (TD-14/TD-17)

Look up `science_registry` to determine which science's rule takes precedence when a contradiction is detected. Use the `DEFAULT_SUPERSESSION_MAP` below as the in-process fallback if the collection lookup fails.

```python
DEFAULT_SUPERSESSION_MAP = {
    "career":        {"career_growth":        ["vedic_astrology", "numerology", "palmistry", "tarot"]},
    "wealth":        {"financial_security":   ["vedic_astrology", "numerology", "tarot", "palmistry"]},
    "relationships": {"partnership_stability": ["vedic_astrology", "numerology", "tarot", "palmistry"],
                      "marriage_timing":       ["vedic_astrology", "numerology", "tarot", "palmistry"]},
    "health":        {"health_vitality":      ["vedic_astrology", "palmistry", "numerology", "tarot"]},
    "general":       {"*":                    ["vedic_astrology", "numerology", "palmistry", "tarot"]},
}
```

### G-02 note — still deferred

Do NOT include tier multipliers (×0.60→×1.15) in Sprint 2. These require claim clustering which is built as part of Sprint 2 output aggregation — Codex to determine the right insertion point once G-03/G-05/G-06 are wired.

---

**Sprint 2 gate (must pass before Sprint 3 brief is issued):**
1. `_contradiction_score(rule_a, rule_b)` returns correct C-score for known opposing/agreeing pairs
2. `_representation_mode(c_scores)` returns correct mode for C < 0.30, 0.30–0.75, > 0.75
3. `_build_tension_block(rule_a, rule_b, c_score, domain)` returns correctly shaped dict
4. Supersession lookup correctly returns highest-ranked science for a given domain
5. `scan_chart()` output includes `representation_mode` and `tension_blocks` in response payload

Deliver as a single diff against `backend/knowledge_engine.py`. Commit to `main`.

---

## Knowledge Base Ingest — Current State

| Batch | Chapter | Rules | auto_approved | pending_review | flagged | Batch ID |
|---|---|---|---|---|---|---|
| BPHS Vol 1 Ch 12-18 | Houses 1-7 | 241 | 58% | 33% | 12% | bphs-ch12..18-v2-20260414 |
| BPHS Vol 1 Ch 19-23 | Houses 8-12 | 119 | 59% | 33% | 8% | bphs-ch19..23-v2-20260415 |
| BPHS Vol 1 Ch 24 | Bhava Lords | 376 | 71% | 20% | 9% | bphs-ch24-v2-20260416 |
| BPHS Vol 2 Ch 47 | Mahadasha by Planet | 93 | 82% | 14% | 4% | bphs-ch47-dasha-20260416 |
| BPHS Vol 2 Ch 48 | Dasha of House Lords | 46 | 74% | 24% | 2% | bphs-ch48-dasha-20260416 |
| BPHS Vol 2 Ch 52 | Antardasha Sun MD | 93 | 83% | 14% | 3% | bphs-ch52-dasha-20260416 |
| BPHS Vol 2 Ch 53 | Antardasha Moon MD | 68 | 76% | 18% | 6% | bphs-ch53-dasha-20260417 |
| **TOTAL** | | **1,036** | **70%** | **23%** | **7%** | |

**Next up:** Ch 53 (Moon MD Antardasha) → Ch 54-60 → A Text Book Ch 15 → Yoga chapters

---

## Report Tier Architecture — Locked 17 Apr 2026

| Tier | Internal register | Source | User pricing |
|---|---|---|---|
| Basic | `simplified` | AI plain English summary | Free / freemium |
| Premium | `modern` | Rule-backed, structured, domain-specific | Paid |
| Pro | `classical` | Our authored classical-style prose (not verbatim Santhanam) + chapter attribution | Premium paid |

**IP note:** Astrological if-then rules are facts — not copyrightable in any jurisdiction. Our extraction methodology, schema, scoring model, and classical paraphrase layer are our IP. AI humanising layer for output prose deferred to Phase 2 (TD-02 / WIM pipeline).

---

*This document supersedes: KNOWLEDGE_ENGINE_ROADMAP.md (ingest detail), KNOWLEDGE_ENGINE_STRATEGY.md (architectural detail) for Commission/TD/Gap tracking only. Those files retain their detailed content for their own purposes.*
