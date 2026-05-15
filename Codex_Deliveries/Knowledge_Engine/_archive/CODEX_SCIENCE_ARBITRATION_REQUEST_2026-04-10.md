# Codex Advisory Request -- Science Arbitration Mathematical Framework
> To: Codex
> From: EverydayHoroscope / Temple Team
> Date: 10 April 2026
> Re: Commission I -- Jyotish Knowledge Engine (Pre-Build Advisory)
> Status: AWAITING CODEX MATHEMATICAL FRAMEWORK PROPOSAL

---

## Context

The Knowledge Engine blends interpretations across multiple sciences: Vedic Astrology, Numerology, Palmistry, and Tarot. When two sciences make contradictory claims about the same life domain, the engine needs a principled way to decide what the narrative layer receives.

We have defined a `science_registry` collection and a provisional hierarchy. What we have not defined is the **mathematical arbitration mechanism** -- how contradictions are detected, scored, and resolved, and how that resolution is communicated to the user without undermining trust in either science.

We are asking you to propose the framework. This is a mathematical and architectural brief, not a philosophy question.

---

## What Is Already Decided (Do Not Re-Open)

| Decision | Value |
|---|---|
| Sciences in Phase 1 | Vedic Astrology (active), Numerology (active), Palmistry (reserved), Tarot (reserved) |
| Fixed confidence weights | Astrology 40% / Numerology 20% / Palmistry 25% / Tarot 15% |
| Qualitative confidence tiers | LOW 0.60 / MEDIUM 0.80 / HIGH 1.00 / VERIFIED 1.15 |
| Contextual multipliers | α (macro), β (micro), γ (family) -- schema ready Phase 1, values populated Phase 2 (World Context Engine) |
| Science registry schema | `science_id`, `hierarchy_rank`, `authority_domain`, `defers_to`, `contradiction_policy`, `active` |
| Library Console | 5 tabs confirmed -- Science Registry editor is not a Phase 1 tab (managed via contract + seeded JSON initially) |

---

## Section 1 -- Contradiction Detection

Before arbitration can happen, contradictions must be detected. We need a method that works at rule evaluation time, not post-hoc.

### Questions for Codex

**1.1 -- What constitutes a contradiction?**

In Vedic Astrology, Saturn in the 7th house indicates delayed marriage. A Numerology life path 6 might indicate early domestic happiness and strong partnership energy. Are these contradictory, complementary, or orthogonal?

Propose a typology of contradiction types -- at minimum:
- **Directional contradiction** (one says positive outcome, one says negative)
- **Temporal contradiction** (one says early, one says late)
- **Strength contradiction** (one says strong, one says weak -- same direction, different magnitude)
- **Domain overlap ambiguity** (two sciences claim authority over the same domain -- is that itself a contradiction?)

For each type: how is it detected computationally? What fields in the rule schema carry the signal?

**1.2 -- Detection threshold**

Not every divergence should trigger arbitration. Propose a detection threshold -- at what level of divergence (and across what fields) should the engine flag a contradiction vs treat it as complementary?

**1.3 -- Schema fields required**

What fields would need to be added to the `interpretation_rules` schema to make contradiction detection reliable? We currently have `condition`, `category`, `life_domain`, `sentiment`, `strength_score`. Are these sufficient? What is missing?

---

## Section 2 -- Mathematical Framework Candidates

Three candidate frameworks were identified in our internal review. Evaluate each for this use case.

### Framework A -- MCDA (Multi-Criteria Decision Analysis)

Used in policy and engineering to rank alternatives against weighted criteria. Could score each science's claim against domain authority, source confidence, and contextual fit -- return a weighted winner.

**Questions:**
1. Is MCDA appropriate here, or does it assume independence between sciences that does not hold in Jyotish (where Vedic Astrology and Numerology are often treated as complementary, not competing)?
2. Show a worked example: Saturn 7th house (delayed marriage, strength HIGH) vs Life Path 6 (early partnership, confidence MEDIUM). Walk the MCDA calculation and show what score each claim receives.
3. What does MCDA output when the scores are close (within 5%)? Does it collapse to a single winner, or does it return a distribution?

### Framework B -- Bayesian Belief Updating

Each science provides a prior probability for an outcome. Observations (chart positions, numbers, palm lines) update the posterior. The final posterior represents the combined evidence.

**Questions:**
1. What is the prior probability source for each science? We do not have empirical frequency data. Can Bayesian updating work with expert-assigned priors?
2. How does Bayesian updating handle directional contradictions (one science says P(outcome) = 0.8, another says P(¬outcome) = 0.7)?
3. Show a worked example using the same Saturn/Life Path 6 contradiction above. What does the posterior look like?
4. Is Bayesian updating computationally viable at <500ms for 50 matched rules?

### Framework C -- Dempster-Shafer Evidence Theory

D-S is designed for combining evidence from independent sources under uncertainty, without forcing a prior. It explicitly handles the case where evidence is partially conflicting.

**Questions:**
1. D-S requires a frame of discernment (the set of possible outcomes). For a life domain like "marriage timing" -- what does the frame look like? (Early / On-time / Late / Unlikely?)
2. Show a worked example: Astrology says {Late} with mass 0.75, uncertainty 0.25. Numerology says {Early, On-time} with mass 0.60, uncertainty 0.40. Run the D-S combination rule and show the resulting belief function.
3. D-S is known to produce counterintuitive results when sources are highly conflicting (Zadeh's paradox). How does this manifest in our context, and how should it be handled?
4. Is D-S overkill for Phase 1 (two active sciences)? Would it become valuable at Phase 3 (four sciences active)?

---

## Section 3 -- Supersession Table vs Confidence-Delta Approach

When a contradiction is confirmed, something must win (or both must be surfaced). We have two candidate resolution mechanisms.

### Option A -- Supersession Table (Domain-Specific Hierarchy)

A static lookup: for domain X, science Y leads over science Z. Example:
- Timing of life events → Vedic Astrology leads
- Character and personality → Numerology leads (Life Path is more accessible to users)
- Health → Vedic Astrology + Palmistry (when active)

**Questions:**
1. Design the full supersession table for the four Phase 1 sciences across the eight `category` fields (`general`, `career`, `wealth`, `relationships`, `health`, `education`, `spirituality`, `longevity`). Which science leads in each domain?
2. What happens in domains where the table does not assign a clear leader? Is a default fallback to hierarchy_rank sufficient?
3. How is the supersession table stored and updated? Is this part of `science_registry`, a separate collection, or a configuration file?

### Option B -- Confidence-Delta Arbitration

No fixed hierarchy. The science with the higher effective confidence score wins. Effective confidence = `fixed_weight × confidence_tier × (α × β × γ)`.

If the delta between the top two science scores exceeds a threshold (e.g., Δ > 0.15), the higher scorer wins. If Δ ≤ 0.15, both claims are surfaced in the narrative as complementary perspectives.

**Questions:**
1. Is a fixed delta threshold (0.15) the right approach, or should the threshold vary by domain (e.g., higher threshold for health than for career)?
2. Show a worked example: Astrology effective score = 0.44, Numerology effective score = 0.34. Δ = 0.10. Both are surfaced. What does the narrative engine receive -- a single arbitrated claim, or two claims with a tension flag?
3. What is the failure mode if all sciences have low effective confidence scores (e.g., all below 0.20)? Should the engine surface a "low confidence" flag to the user?

### Temple Team Preference

We lean toward **a hybrid**: Supersession Table as the primary mechanism for clear domain authority (health, longevity, timing) with Confidence-Delta as the tiebreaker when the table does not assign a clear leader.

Do your worked examples support or challenge this? Would you recommend a different architecture?

---

## Section 4 -- Narrative Representation of Contradictions

When a contradiction is surfaced to the narrative layer (Claude API), it must be communicated in a way that is honest without being confusing to the user.

### Questions for Codex

**4.1 -- What does the evidence packet look like?**

When two sciences contradict on domain `relationships`, what exactly should the Narrative Planner send to Claude? Show a sample JSON structure for the `tension_block` that the narrative engine receives.

**4.2 -- Three representation modes**

Propose specific prompt language for each of the three contradiction representation modes:

| Mode | When used | Example narrative output |
|---|---|---|
| **Synthesis** | Sciences point in broadly the same direction with minor divergence | "Both your birth chart and name numerology point toward..." |
| **Tension** | Sciences diverge meaningfully but both have authority | "Your planetary positions suggest X, while your numerological signature points toward Y -- the truth likely lies in..." |
| **Honest Uncertainty** | High contradiction, low overall confidence | "The sciences we have examined offer different perspectives here. We present both without a definitive resolution." |

For each mode: at what confidence-delta range is it triggered? Show the exact threshold logic.

**4.3 -- User trust**

If the engine surfaces contradictions too often, users lose confidence in the platform. If it surfaces them too rarely, it is suppressing real interpretive complexity. What frequency of tension/uncertainty representation do you recommend for a consumer-facing platform?

---

## Section 5 -- Extensibility

The framework must scale from 2 active sciences (Phase 1) to 4 (Phase 3) without schema changes.

### Questions for Codex

1. If Palmistry is activated in Phase 2, how does the Supersession Table expand? Does adding a new science require re-ranking all existing domain assignments?
2. If a new science is added that has no empirical confidence data (e.g., I Ching), how does the framework handle a science with `hierarchy_rank` assigned but no historical accuracy record?
3. What is the maximum number of sciences the framework can handle before the arbitration logic becomes computationally significant at our latency target (<500ms)?

---

## Output Format

Return your response as:

```
## Section 1 -- Contradiction Detection
[Typology, detection threshold, schema fields required]

## Section 2 -- Framework Evaluation
[MCDA worked example | Bayesian worked example | D-S worked example | Your recommendation]

## Section 3 -- Supersession Table
[Full table across 8 domains | Confidence-Delta worked example | Recommendation]

## Section 4 -- Narrative Representation
[tension_block JSON | Prompt language for 3 modes | Threshold logic | Frequency recommendation]

## Section 5 -- Extensibility Notes
[Answers to 3 extensibility questions]

## Overall Recommendation
[Which framework, which supersession mechanism, and why -- in 2-3 paragraphs]
```

We will review your output and issue final arbitration framework decisions before the build contract is signed.

---

> Related documents: `CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` (Section 15: Cross-Science Scoring, Section 17: Science Arbitration) · `CODEX_COMMISSION_I_BRIEF.md` (Question D)
