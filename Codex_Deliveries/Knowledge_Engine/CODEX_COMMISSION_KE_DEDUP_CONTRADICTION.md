# CODEX COMMISSION: KE-DEDUP-CONTRADICTION-1
## Knowledge Engine -- Cross-Text Dedup & Contradiction Detection Script

> Commission ID: KE-DEDUP-CONTRADICTION-1
> Date: 2026-05-28
> Status: READY TO ISSUE
> Thread: Knowledge Engine Codex Thread
> Prerequisite: At least 2 complete text decode folders available in output directories

---

## Why This Commission Exists

The Knowledge Engine will ingest 10+ classical Vedic astrology texts. Rules from different texts frequently overlap (same rule worded differently) or contradict (same condition, opposite outcome). Without automated detection:

- The rule base inflates with duplicates that appear as independent evidence when they are the same claim repeated
- Contradictions are invisible -- the rule engine will fire both a "Jupiter in 11th = wealth" rule and a "Jupiter in 11th = financial loss" rule from two different texts with no signal to the reviewer
- Contradiction detection currently happens manually, chapter by chapter, within a single text only

This script extends detection cross-text, runs automatically after any two decode folders are available, and writes machine-readable links directly into the rule JSON files.

---

## Deliverable -- `backend/ke_dedup_script.py`

A standalone Python script (no FastAPI, no server dependency). Run from the command line. Reads Rules.json files from two or more decode folders, computes similarity, writes results back to the JSON files, and produces a summary report.

---

## Input / Output Spec

### Inputs (command-line arguments)

```bash
python ke_dedup_script.py \
  --folder-a "/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_CC_Decode" \
  --folder-b "/Users/apple/Documents/Knowledge Engine_eBooks/Phaladeepika_CC_Decode" \
  --threshold 0.82 \
  --output-report "/Users/apple/Documents/Knowledge Engine_eBooks/Dedup_Reports/BPHS_vs_PD_dedup_report.json"
```

| Argument | Type | Required | Description |
|---|---|---|---|
| `--folder-a` | str | Yes | Path to first decode folder (e.g. BPHS) |
| `--folder-b` | str | Yes | Path to second decode folder (e.g. Phaladeepika) |
| `--threshold` | float | No | Similarity score above which a pair is flagged. Default: 0.82 |
| `--output-report` | str | Yes | Path to write the summary JSON report |
| `--dry-run` | flag | No | If set, print matches but do NOT write to source JSON files |
| `--update-files` | flag | No | If set, write `cross_text_matches` entries back to source Rules.json files |

---

### Rules.json file loading

Each folder may contain:
- `*_Rules.json` -- standard single-file format (JSON array of rule objects)
- `*_Rules_Part1.json`, `*_Rules_Part2.json` etc. -- split-file format (also JSON arrays)

The script must load ALL files matching `*_Rules*.json` from each folder. Parse each file as a JSON array. Build a flat list of all rule objects per folder, retaining the source file path for write-back.

---

### Similarity computation

#### Step 1 -- Build text representation for each rule

For each rule, build a comparison string by concatenating:
```python
compare_text = f"{rule['condition'].get('type','')} {rule['condition'].get('planet','')} {rule['condition'].get('house','')} {rule['condition'].get('sign','')} {rule.get('full_text','')}"
```

Use `full_text` as the primary signal. Condition fields ensure that rules about different planets/houses don't score high on text alone.

#### Step 2 -- TF-IDF cosine similarity

Use `sklearn.feature_extraction.text.TfidfVectorizer` + `sklearn.metrics.pairwise.cosine_similarity`.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
all_texts = [rule["_compare_text"] for rule in all_rules_a + all_rules_b]
tfidf_matrix = vectorizer.fit_transform(all_texts)

n_a = len(all_rules_a)
matrix_a = tfidf_matrix[:n_a]
matrix_b = tfidf_matrix[n_a:]

scores = cosine_similarity(matrix_a, matrix_b)  # shape: (n_a, n_b)
```

#### Step 3 -- Classify relationship

For each pair (rule_a, rule_b) where `scores[i][j] >= threshold`:

| Condition | Relationship value |
|---|---|
| Score ≥ 0.95 | `"identical_claim"` |
| Score ≥ 0.90 | `"near_identical"` |
| Score ≥ 0.82 and same condition.type + same planet/house | `"same_principle_different_phrasing"` |
| Score ≥ 0.82 (other) | `"partial_overlap"` |

#### Step 4 -- Contradiction detection

After similarity pass, run a separate contradiction check on all pairs (regardless of similarity score) where:
- `rule_a['condition']['type'] == rule_b['condition']['type']`
- `rule_a['condition'].get('planet') == rule_b['condition'].get('planet')` (if planet field exists on both)
- `rule_a['condition'].get('house') == rule_b['condition'].get('house')` (if house field exists on both)
- `rule_a.get('claim_polarity') != rule_b.get('claim_polarity')` AND both polarities are non-null

If all conditions above are met:
- If polarities are direct opposites (e.g. `"positive"` vs `"negative"`): relationship = `"contradicts"`
- If one polarity is `"mixed"` and the other is `"positive"` or `"negative"`: relationship = `"partial_contradiction"`

**Contradiction pairs are flagged regardless of text similarity score.** A rule can be a contradiction even if the wording is completely different.

---

### Output -- `cross_text_matches` entries

For each flagged pair, add an entry to the `cross_text_matches` list on BOTH rules (bidirectional linking):

```json
{
  "rule_id": "BPHS.Ch12.4.1",
  "similarity_score": 0.91,
  "relationship": "near_identical"
}
```

For contradiction pairs:
```json
{
  "rule_id": "PD.VIII.3.2",
  "similarity_score": 0.44,
  "relationship": "contradicts"
}
```

**Rules for write-back:**
- If `cross_text_matches` is currently `null`, initialise it as an empty list before appending
- If a `cross_text_matches` entry for the same `rule_id` already exists, update it (do not duplicate)
- The script is idempotent -- re-running replaces existing entries rather than appending duplicates
- Only write back if `--update-files` flag is passed

---

### Output -- Summary report JSON

Write a single JSON report file at `--output-report`:

```json
{
  "run_timestamp": "2026-05-28T14:23:00Z",
  "folder_a": "/path/to/BPHS_CC_Decode",
  "folder_b": "/path/to/Phaladeepika_CC_Decode",
  "threshold_used": 0.82,
  "rules_in_a": 312,
  "rules_in_b": 198,
  "pairs_evaluated": 61776,
  "duplicate_candidates": 47,
  "contradiction_pairs": 12,
  "matches": [
    {
      "rule_a_id": "BPHS.Ch12.4.1",
      "rule_b_id": "PD.VIII.3.2",
      "similarity_score": 0.91,
      "relationship": "near_identical",
      "rule_a_full_text": "...",
      "rule_b_full_text": "..."
    }
  ],
  "contradictions": [
    {
      "rule_a_id": "BPHS.Ch19.2.1",
      "rule_b_id": "PD.XIII.5.1",
      "similarity_score": 0.44,
      "relationship": "contradicts",
      "rule_a_polarity": "positive",
      "rule_b_polarity": "negative",
      "shared_condition": {
        "type": "house_lord_in_house",
        "lord_of_house": 8,
        "placed_in_house": 1
      },
      "rule_a_full_text": "...",
      "rule_b_full_text": "..."
    }
  ]
}
```

---

## Dependencies

Add to `backend/requirements.txt` if not already present:
```
scikit-learn>=1.3.0
```

All other dependencies (`json`, `os`, `pathlib`, `argparse`, `datetime`) are Python stdlib.

---

## Error Handling

| Scenario | Behaviour |
|---|---|
| Folder does not exist | Print error and exit with code 1 |
| No `*_Rules*.json` files found in a folder | Print warning, continue (report will show 0 rules for that folder) |
| JSON parse error in a Rules file | Print warning with filename, skip that file, continue |
| Rule object missing `rule_id` | Skip that rule, log to stderr |
| `sklearn` not installed | Print install instruction and exit with code 1 |

---

## File Location

```
backend/ke_dedup_script.py
```

---

## Temple Boundary Rules (DO NOT VIOLATE)

- Do NOT modify `server.py`, `App.js`, `NavBar.jsx`, `panchang_router.py`, or `vedic_calculator.py`
- Do NOT add any FastAPI routes -- this is a standalone script only
- Do NOT add any imports from application modules -- use only stdlib + scikit-learn
- Do NOT write to MongoDB -- output is to JSON files and report only
- The script reads from and writes to local file paths only

---

## Test Cases (include in docstring or comments)

The script should include inline examples or comments showing:
1. Two identical rules from different texts → `identical_claim`
2. Two rules with same planet/house but different wording → `same_principle_different_phrasing`
3. Two rules with same condition but opposite polarity → `contradicts` (regardless of text similarity)
4. Two unrelated rules → no match, no entry added

---

## Acceptance Criteria

- [ ] Script runs without error on any two decode folders containing `*_Rules*.json` files
- [ ] `--dry-run` produces output but makes zero file changes
- [ ] `--update-files` writes `cross_text_matches` entries to source JSON files
- [ ] Idempotent: running twice on the same folders produces identical output (no duplicated entries)
- [ ] Summary report JSON is valid JSON and contains all required fields
- [ ] Contradiction detection fires on same-condition opposite-polarity pairs even with low text similarity
- [ ] Script handles split-file Parts (Part1, Part2, etc.) correctly -- loads all parts

---

*Commission issued by Temple Team -- EverydayHoroscope, 2026-05-28*
