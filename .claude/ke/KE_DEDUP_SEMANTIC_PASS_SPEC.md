# KE Dedup -- Semantic Pass Specification
> Phase 2 of `ke_dedup_script.py` deduplication pipeline
> Status: **NOT YET IMPLEMENTED** -- spec only
> Created: 2026-06-02 | Author: CC

---

## 1. Why TF-IDF Is Not Enough

The current `ke_dedup_script.py` uses TF-IDF cosine similarity (`sklearn`, bigrams, threshold 0.82).
This catches lexically similar rules well. It cannot catch **same-concept, different-wording** rules.

**Confirmed failure cases (2026-06-02 investigation):**

| Rule A (H300 batch) | Rule B (Phaladeepika) | Jaccard | Why TF-IDF fails |
|---|---|---|---|
| "KP uses 9 planets: Sun Moon Mars Mercury Jupiter Venus Saturn Rahu Ketu" | "The nine grahas in Jyotish are Surya, Chandra, Mangal..." | 0.06 | Different vocabulary (KP vs Sanskrit names) |
| "27 nakshatras divide the zodiac into equal 13°20' segments" | "The lunar mansions number 27, each spanning 800 arc-minutes" | 0.11 | Different units, different framing |
| Aspect rule: "Every planet aspects the 7th house from itself" | "Saptama drishti is the mutual aspect common to all grahas" | 0.17 | Sanskrit vs English + different sentence structure |

These are all `engine_specification` condition type rules with all-null condition fields (planet/house/sign = null).
TF-IDF cannot group them because:
1. Different vocabulary (Sanskrit vs transliterated vs English)
2. All condition fields null → `build_compare_text()` only has `full_text` to work with
3. Jaccard scores 0.06-0.17, well below the 0.82 threshold

---

## 2. Scope of the Problem

Rules affected: **`engine_specification`** condition type, all-null condition fields.

As of 2026-06-02:
- `horoscope_db.interpretation_rules` total: **10,664**
- Estimated `engine_specification` rules: ~300-400 (across BPHS, Phaladeepika, 300 Horoscopes, KP books)
- Cross-book methodology overlaps expected: high (KP methodology rules stated in every KP book;
  classical 9-planet/12-sign lists appear in every Vedic text)

The positional conflict detector (Phase 1.5, implemented 2026-06-02) does NOT address these --
it requires non-null `planet` AND `house`/`sign` fields.

---

## 3. Proposed Architecture

### 3a. Embedding Model Options

| Option | Pros | Cons | Recommended |
|---|---|---|---|
| `sentence-transformers` (local, `all-MiniLM-L6-v2`) | Free, fast, offline, 384-dim | Less accurate for domain-specific text | Phase 2a prototype |
| Claude API (`claude-3-haiku-20240307` embeddings) | High quality, domain-aware | API cost, rate limits | Phase 2b production |
| `text-embedding-3-small` (OpenAI) | Good quality, low cost | Requires OpenAI key | Alternative |

**Recommendation for prototype:** `sentence-transformers` with `all-MiniLM-L6-v2` (free, installable via pip).
Upgrade to Claude API embeddings if prototype F1 is below 0.8 on known duplicate pairs.

### 3b. Pipeline Design

```python
# Phase 2 addition to ke_dedup_script.py

SEMANTIC_SIMILARITY_THRESHOLD = 0.85   # cosine similarity on embedding space
SEMANTIC_SCOPE_TYPES = {"engine_specification"}  # only process these condition types

def get_embeddings(texts: list[str], model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """Load sentence-transformers model and encode texts."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    return model.encode(texts, normalize_embeddings=True)

def detect_semantic_duplicates(
    rules_a: list[RuleRecord],
    rules_b: list[RuleRecord],
    threshold: float = SEMANTIC_SIMILARITY_THRESHOLD,
    scope_types: set[str] = SEMANTIC_SCOPE_TYPES,
) -> list[tuple[RuleRecord, RuleRecord, float, str]]:
    """Find rules from A and B that are semantically equivalent
    despite using different vocabulary."""
    # Filter to scope_types only
    # Build embeddings for filtered sets
    # Compute cosine similarity matrix
    # Return pairs above threshold with relationship = "semantic_duplicate"
    ...
```

### 3c. CLI Integration

New flag: `--semantic-pass` (opt-in, off by default -- requires `sentence-transformers` install)

```bash
python ke_dedup_script.py \
    --folder-a .../BPHS_CC_Decode \
    --folder-b .../ThreeHundredHoroscopes_CC_Decode \
    --threshold 0.82 \
    --output-report report.json \
    --semantic-pass
```

Report JSON gains two new fields:
```json
{
  "semantic_duplicates": 12,
  "semantic_duplicates_detail": [...]
}
```

### 3d. Report Entry Schema

```json
{
  "rule_a_id": "kp-ch19-001",
  "rule_b_id": "h300-s01a-011",
  "similarity_score": 0.91,
  "relationship": "semantic_duplicate",
  "embedding_model": "all-MiniLM-L6-v2",
  "rule_a_full_text": "KP uses 9 planets...",
  "rule_b_full_text": "The nine grahas in Jyotish..."
}
```

---

## 4. Validation Approach

Before production use, validate against known duplicate pairs collected during H300 investigation:

| Pair | Expected | Notes |
|---|---|---|
| h300 "9 planets" vs bphs "9 grahas" | semantic_duplicate | Sanskrit vs English |
| h300 aspect rule vs phaladeepika aspect rule | semantic_duplicate | Different framing |
| h300 nakshatra 13°20' rule vs bphs nakshatra rule | semantic_duplicate | Different units |

Target: F1 >= 0.80 on the known-pair validation set before committing threshold.

---

## 5. Dependencies

```
sentence-transformers>=2.2.0
torch>=2.0.0   # pulled by sentence-transformers
numpy>=1.24.0
```

Add to `backend/requirements.txt` under a `# KE dedup -- semantic pass (optional)` comment block.
These are script-only dependencies -- NOT imported by FastAPI server routes.

---

## 6. Implementation Priority

| Phase | What | When |
|---|---|---|
| Phase 1.5 (DONE 2026-06-02) | Positional conflict detector (planet×house/sign) | ✅ Done |
| Phase 2a | `sentence-transformers` prototype, `engine_specification` scope only | Next KE sprint |
| Phase 2b | Upgrade to Claude API embeddings if F1 < 0.80 | After Phase 2a validation |
| Phase 2c | Extend semantic scope beyond `engine_specification` if useful | TBD |

---

## 7. Open Questions (TT decision)

| # | Question |
|---|---|
| 1 | Should `semantic_duplicate` pairs be written back to JSON `cross_text_matches` like TF-IDF matches? |
| 2 | Threshold: 0.85 is a starting point -- validate against known pairs before committing |
| 3 | When semantic_duplicate is found for two `engine_specification` rules, which book's version is canonical? |
