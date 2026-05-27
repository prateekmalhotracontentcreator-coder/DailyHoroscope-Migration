# ANGEL-2 Commission Brief -- Angel Numbers Generator Rewrite (Quality Fix)
> Thread: Angel Numbers Codex Thread (same thread as ANGEL-1)
> Commission ID: ANGEL-2
> Date: 2026-05-26
> Status: READY TO ISSUE
> Prerequisite: ANGEL-1 delivered ✅

---

## Context -- Why This Brief Exists

ANGEL-1 delivered `backend/angel_numbers_data.py` -- a generator that builds 1,000 core
number records and 9,000 intent records programmatically. A content audit found severe
template repetition that creates duplicate content at scale, which is harmful for SEO and
will be detected by Google's Helpful Content system.

**No router, frontend, or wiring changes are needed. This brief touches ONE file:**
`backend/angel_numbers_data.py`

There is NO copyright risk -- the content is entirely Codex-generated.
The problem is mechanical template repetition at scale.

---

## Audit Findings

### Finding 1 -- `seeing_it_means` field: 1 unique ending across ALL 1,000 records 🔴

Every single one of 1,000 core number records ends `seeing_it_means` with the identical sentence:

> *"...it is a nudge to keep moving with intention instead of scattering your focus."*

1,000 pages. 1 closing sentence. Google sees this as thin, duplicate content.

### Finding 2 -- `vibration` field: 8 unique endings across 1,000 records 🔴

722 of 1,000 records share the most common `vibration` ending:
> *"...It asks you to notice what is ready to shift, stabilize, or begin."*

### Finding 3 -- Intent `message` field: identical across all 9 intents per number 🔴

9,000 intent records. Only 1,000 unique `message` bodies.
The `message` for number 111/love is **word-for-word identical** to 111/career, 111/twin-flame,
etc. The intent does not affect the message at all.

Every single one of 9,000 intent `message` fields ends with:
> *"...this means choosing the response that feels both spiritually clean and practically sustainable."*

9,000 pages. 1 closing sentence.

### Finding 4 -- `action_steps` in intent records: 81 unique sets across 9,000 records 🟡

9,000 intent records share only 81 unique `action_steps` combinations. Heavy repetition.

---

## The Fix -- Generator-Level Rewrites

The data is built by Python generator functions. The fix must happen at the generator level
-- change the functions that build the content, so every re-run produces more varied output.
Do NOT try to patch individual records -- the data is generated dynamically.

### Fix 1 -- `seeing_it_means` ending variety

The `seeing_it_means` field for each number must conclude with a sentence unique to that
number's root meaning and pattern type. Build a lookup of 9-12 varied closing sentences
keyed by root digit (1-9) and pattern type (pure amplification, mirrored, cascading, etc.)
so no two pattern types share the same closing.

**Minimum requirement:** At least 30 distinct closing sentences in rotation.
No closing sentence should appear more than 40 times across 1,000 records.

### Fix 2 -- `vibration` field endings

Same approach -- the `vibration` field must not end with the same sentence across hundreds
of records. Build a set of at least 15 distinct closing phrases keyed by the number's
numerological quality (initiator, bridge, messenger, builder, seeker, harmoniser, seeker,
authority, completion).

### Fix 3 -- Intent `message` must be intent-specific 🔴 (most important)

The `message` field in intent records must vary meaningfully by intent, not just by number.
Currently the message for 111/love and 111/career is identical -- only the affirmation and
action steps differ slightly.

**The fix:** Build 9 distinct `message` templates -- one per intent -- that frame the number's
energy through the lens of that specific life area. The core numerological meaning stays
consistent, but the expression, examples, and framing must shift for each intent.

Examples of what should differ between intents for the same number:
- **love**: language of emotional honesty, reciprocity, vulnerability, partnership
- **career**: language of timing, opportunity, professional courage, financial clarity
- **twin-flame**: language of soul recognition, mirroring, reunion/separation cycles
- **manifestation**: language of alignment, vibrational match, co-creation
- **health**: language of nervous system, energy levels, body signals, lifestyle rhythm
- **spiritual-growth**: language of inner work, awareness, expansion, higher self
- **family**: language of roots, dynamics, forgiveness, generational patterns
- **protection**: language of boundaries, discernment, energetic safety
- **new-beginnings**: language of thresholds, release, starting conditions

### Fix 4 -- `action_steps` variety in intent records

Action steps must be intent-specific. The three `action_steps` for 333/love must give
relationship-specific actions, not generic "move before doubt hardens" advice.

Build a matrix of action step templates: 9 root digits × 9 intents = 81 base templates,
then vary by pattern type. Each step should be a concrete, context-specific instruction --
not a reworded version of the generic message.

### Fix 5 -- Remove the universal closing sentence

This sentence must be eliminated from all 9,000 intent records:
> *"...this means choosing the response that feels both spiritually clean and practically sustainable."*

It currently ends every single `message` field. Replace with endings unique to the number +
intent combination.

---

## Deliverable -- Updated `angel_numbers_data.py`

Deliver the complete updated `backend/angel_numbers_data.py`.

The generator functions must produce:
- `seeing_it_means`: at least 30 distinct closing sentences across 1,000 records
- `vibration`: at least 15 distinct closing phrases
- `message` (intent): intent-specific framing -- 9 meaningfully different approaches
- `action_steps` (intent): intent-specific actions -- not generic
- No universal closing sentence appearing across all records

**Verify before delivering:**
```bash
python3 -c "
from angel_numbers_data import iter_core_records, iter_intent_records
core = list(iter_core_records())
intents = list(iter_intent_records())

# Check variety
seeing_endings = set(r['seeing_it_means'][-80:] for r in core)
msg_endings = set(r['message'][-100:] for r in intents)
unique_msgs = len(set(r['message'] for r in intents))

print('Core records:', len(core))
print('Unique seeing_it_means endings:', len(seeing_endings))
print('Intent records:', len(intents))
print('Unique message endings:', len(msg_endings))
print('Unique message bodies:', unique_msgs)
assert len(core) == 1000
assert len(intents) == 9000
assert len(seeing_endings) >= 30, 'Not enough variety in seeing_it_means'
assert unique_msgs >= 8000, 'Intent messages not sufficiently varied'
print('All checks passed.')
"
```

---

## What Must NOT Change

- Total record counts: 1,000 core + 9,000 intent = 10,001 with hub
- The `get_core_numbers()` function and its number list logic
- The `INTENT_ORDER` list
- `build_sitemap_paths()`, `sitemap_page_count()`, `PAGE_SIZE`
- `iter_core_records()` and `iter_intent_records()` function signatures
- All structural fields: `number`, `display`, `headline`, `slug`, `canonical_url`,
  `meta_title`, `meta_description`, `key_themes`, `related_numbers`, `faq`, `intent`,
  `display_name`, `all_intents`

---

## Addendum -- Temple Team Review 2026-05-27

### Additional Requirement 1 -- Manifestation How-To Layer

Every number's `manifestation` intent record must include a `how_to_manifest` field
containing **specific, practical activation steps** -- not generic affirmations.

The content must answer: *"What does a person actually DO with this angel number?"*

Required variety of practical actions (rotate across records):
- Write the number in a manifestation journal / notebook
- Open a dedicated Manifestation Book and record the date, number, and intention
- Speak the number aloud 3× while holding a clear intention in mind
- Set a phone reminder at the time that matches the number (e.g. 1:11 PM for 111)
- Write the number + a one-sentence intention on a piece of paper and place it under a candle
- Meditate for the number of minutes matching the root digit (e.g. 3 minutes for 111)
- Create a vision board anchor -- write the number at the top and place the board in sight

These are not suggestions -- at least 5 distinct action types must appear across the 1,000
manifestation records. No single action type should appear in more than 30% of records.

The `how_to_manifest` field must be added to the `build_intent_summary()` output for the
`manifestation` intent ONLY. No other intent requires this field.

**Data structure addition for manifestation intent records:**
```python
{
    # existing fields ...
    "how_to_manifest": str,  # 60-100 words, specific practical steps
}
```

### Additional Requirement 2 -- ECHO // PACE 3-Layer Compliance Gate (Mandatory)

After the rewrite, run the full 3-layer compliance test and confirm ALL layers PASS:

```bash
PYTHONPATH=backend python3 backend/scripts/verify_angel_numbers_compliance.py
```

| Layer | Method | Pass Threshold |
|---|---|---|
| Layer 1 | TF-IDF Cosine (body fields) | < 40% all clusters (FLAGGED ≥50%, BLOCKED ≥70%) |
| Layer 2 | N-gram phrase match (stop-word filtered) | No 4+ consecutive meaningful words in > 15% of records |
| Layer 3 | Jaccard heading / key_themes match | Jaccard < 75% across any number pair |

**Current baseline scores (pre-rewrite):**
- Layer 1: 72--82% BLOCKED across all clusters ❌
- Layer 2: "lesson slows reaction cycle" appears in 98% of records ❌
- Layer 3: Identical key_themes across number families (100% Jaccard) ❌

**All 3 layers must show PASS in the test output. Paste the full test output in your delivery confirmation. Delivery will not be accepted without it.**

---

## Acceptance Checklist

- [ ] `seeing_it_means` endings: ≥30 distinct across 1,000 core records
- [ ] `vibration` endings: ≥15 distinct across 1,000 core records
- [ ] `message` bodies: ≥8,000 unique across 9,000 intent records
- [ ] `message` for same number differs meaningfully across all 9 intents
- [ ] `action_steps` are intent-specific (not generic for all intents)
- [ ] Universal closing sentence eliminated from `message` field
- [ ] `how_to_manifest` field present in all manifestation intent records (≥5 distinct action types)
- [ ] Layer 1 PASS: all clusters < 40% TF-IDF cosine
- [ ] Layer 2 PASS: no 4-gram phrase in > 15% of records
- [ ] Layer 3 PASS: key_themes Jaccard < 75% across all number pairs
- [ ] Full 3-layer test output pasted in delivery confirmation
- [ ] `len(list(iter_core_records())) == 1000` ✅
- [ ] `len(list(iter_intent_records())) == 9000` ✅
- [ ] `python3 -m py_compile backend/angel_numbers_data.py` passes
- [ ] No changes to any other file
