# Codex Simulation Request -- Schema Architecture Decisions
> To: Codex
> From: EverydayHoroscope / Temple Team
> Date: 10 April 2026
> Re: Commission I -- Jyotish Knowledge Engine (Pre-Build Advisory)
> Status: AWAITING CODEX SIMULATION OUTPUT

---

## Context

The draft contract proposes a MongoDB schema for the Jyotish Knowledge Engine. Before we lock the schema, we need you to run three simulations and return concrete comparisons. These are architectural decisions that cannot be reversed cheaply once extraction begins.

We are not asking for opinions. We are asking for working simulation outputs with numbers.

---

## Simulation 1 -- Embedded Passages vs Separate `source_passages` Collection

### Background

The current contract spec embeds the source passage inline within each rule document:

```json
{
  "rule_id": "R-SAT-7H-001",
  "condition": { "planet": "saturn", "house": 7 },
  "paraphrase": { "text": "...", "voice_tone": "modern_analytical" },
  "source": {
    "book_slug": "bv-raman-how-to-judge",
    "chapter": "Chapter 7",
    "passage_text": "[original excerpt stored here]"
  }
}
```

Codex's advisory suggested a separate `source_passages` collection with a reference ID -- arguing that multiple rules may quote the same passage, and embedding duplicates at scale.

### What We Need

Run a simulation comparing both approaches at two scale points: **300 rules (Phase 1)** and **3,000 rules (Phase 2+)**.

For each approach and each scale point, report:

| Metric | Embedded | Separate Collection |
|---|---|---|
| Estimated average rule document size (KB) | | |
| Total collection storage estimate (MB) | | |
| Number of MongoDB reads per rule evaluation | | |
| Number of reads per full chart evaluation (50-rule match set) | | |
| Index complexity (what fields need indexing, and why) | | |
| Cross-source citation complexity (same passage, multiple rules) | | |

### Specific Questions

1. At 3,000 rules, how many duplicate passage fragments would you estimate exist if passages are embedded? What is the storage overhead?
2. In the Library Console Rules Browser, an editor clicks a rule to view its source passage. How many MongoDB reads does each approach require for that single action?
3. If we later want to update a passage text (e.g., OCR correction discovered post-import) -- how many rule documents need updating under each approach?
4. **Temple Team position**: We lean toward embedded for Phase 1 (simpler, fewer reads, no join) and migrating to a separate collection if duplication becomes a real problem at Phase 2. Do your numbers support or challenge this?

---

## Simulation 2 -- `author_voices` + `narrative_bridges` as MongoDB Collections vs Seeded JSON

### Background

Codex's advisory recommended serving `author_voices` and `narrative_bridges` from seeded JSON files at startup rather than MongoDB collections -- arguing this reduces read overhead since they are rarely updated.

The Temple Team's position: these belong in MongoDB because the Library Console must allow Temple Team editors to update them without a code deployment or server restart.

### What We Need

Walk through the following two concrete operational scenarios under each approach:

**Scenario A -- Editor updates a voice profile**
A Temple Team editor discovers that the `kp_technical` voice profile has an incorrect bridge phrase. They need to update it.

| Action | MongoDB Collection approach | Seeded JSON approach |
|---|---|---|
| How does the editor make the change? | | |
| Is a code deployment required? | | |
| Is a server restart required? | | |
| Does the change take effect immediately in the Test Console? | | |
| Is the change reflected in the import history / audit log? | | |

**Scenario B -- New voice tone added (Phase 2)**
A new voice tone (`nadi_oracular`) is added for a new book class. 

| Action | MongoDB Collection approach | Seeded JSON approach |
|---|---|---|
| Steps required | | |
| Who can make the change (editor / developer)? | | |
| Time to live (change reflected in narrative engine) | | |

### Specific Questions

1. If `author_voices` and `narrative_bridges` are seeded JSON, what is the warm-up read overhead on server startup? Is this measurable at Phase 1 scale?
2. The Library Console (Section 11 of contract) includes a Voice Profiles editor tab. Under the seeded JSON approach, what does this tab actually do -- does it write back to the JSON file, or is it non-functional?
3. **Temple Team position**: We want editors to be able to update voice profiles and bridge phrases from the Library Console without developer involvement. Does your simulation confirm that MongoDB collections are the correct choice for this requirement?

---

## Simulation 3 -- In-Memory Index Refresh During Concurrent Imports

### Background

The contract proposes an in-memory inverted index built at startup and refreshed after each import batch. Canonical match keys (e.g., `planet_in_house|saturn|7`) allow <500ms rule evaluation without scanning MongoDB.

The open question: what happens during the refresh window when concurrent requests are arriving?

### What We Need

Simulate the following scenario:

**Setup:**
- Server has 2,000 rules loaded in memory
- A Temple Team editor triggers a 150-rule import batch from the Library Console
- The import runs for approximately 8 seconds
- During those 8 seconds, 12 user requests arrive that require rule evaluation

**Simulate three refresh strategies and compare:**

| Metric | Strategy A: Block reads during refresh | Strategy B: Double-buffer (build new index in parallel, swap atomically) | Strategy C: Stale reads allowed (refresh happens after, no block) |
|---|---|---|---|
| User-facing latency during import (those 12 requests) | | | |
| Stale data risk (new rules not yet visible) | | | |
| Implementation complexity | | | |
| Risk of serving a half-built index | | | |
| Recommended for Phase 1? | | | |

### Specific Questions

1. For a 150-rule batch at Phase 1 scale, how long does index rebuild actually take (estimated, in milliseconds)?
2. If the index rebuild takes <200ms, is the stale-read window practically meaningful for our use case (editorial import tool, not real-time trading)?
3. What is the simplest Python implementation of Strategy B (double-buffer) -- can you show a pseudocode pattern that would work with FastAPI's async model?
4. **Temple Team position**: We believe Strategy C (stale reads, async refresh) is acceptable for Phase 1 since imports are infrequent editorial actions, not continuous operations. Does your simulation support this?

---

## Output Format

Return your simulation results as:

```
## Simulation 1 Results
[Table + your recommendation + reasoning]

## Simulation 2 Results
[Table + your recommendation + reasoning]

## Simulation 3 Results
[Table + pseudocode for Strategy B + your recommendation + reasoning]

## Overall Schema Recommendation
[One paragraph -- what you would lock vs what you would defer]
```

We will review your output and lock the schema decisions before issuing the build contract.

---

> Related documents: `CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` (full schema spec) · `CODEX_COMMISSION_I_BRIEF.md` (architectural questions A-G)
