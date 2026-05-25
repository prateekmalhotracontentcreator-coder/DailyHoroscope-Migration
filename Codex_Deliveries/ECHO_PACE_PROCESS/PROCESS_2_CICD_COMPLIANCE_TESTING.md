# ECHO // PACE Process 2 -- CI/CD Compliance Testing
> Automated gate: prevents high-similarity content from reaching production
> Source: GAI ECHO//PACE Compliance Consultation V2
> Applies to: ALL SEO modules with 100+ programmatically generated pages
> Last updated: 2026-05-26

---

## What This Solves

Every push to `main` auto-deploys to Render + Vercel. Without a compliance gate, a bad Codex delivery (templated prose, copied definitions) can seed 4,680 near-duplicate pages to production and trigger a Google Helpful Content penalty before anyone notices.

This process creates a two-layer defence:
1. **Local pre-seed check** -- run manually before seeding any module to MongoDB
2. **GitHub Actions gate** -- auto-runs on every push to `main`, blocks merge if similarity ceiling is breached

**Similarity ceiling: 30%** across any two pages within the same module.

---

## Layer 1 -- Local Pre-Seed Compliance Script

**File:** `backend/scripts/verify_tarot_compliance.py`
**Run:** `python3 backend/scripts/verify_tarot_compliance.py`

This script is already created in the repo. It:
- Loads real data from `tarot_seo_data.py`
- Simulates the OLD (templated) vs NEW (anchor-flipped) layout
- Computes cross-page TF-IDF cosine similarity
- Asserts similarity < 30% before allowing seed to proceed

**Expected output (passing):**
```
========================================
 ECHO // PACE COMBINATION BENCHMARK
========================================
❌ BEFORE QUICK FIX:  ~85% similarity
✅ AFTER QUICK FIX:   ~22% similarity
----------------------------------------
🎉 SUCCESS: Structural fix drops below 30% threshold
========================================
```

**If it fails:** Do not seed. Apply Process 1 (anchor flip + intent-matched field) and re-run.

---

## Layer 2 -- GitHub Actions Automated Gate

**File:** `.github/workflows/echo_pace_compliance.yml`

Triggers on every push to `main` and every pull request targeting `main`. Runs the Python compliance test suite. If any module breaches the 30% ceiling, the push is blocked and the developer sees:

```
❌ FAILED E.C.H.O. POLICY: similarity 34.2% -- exceeds 30% ceiling
```

The green merge button turns gray. No deploy happens.

---

## Module-by-Module Compliance Configuration

Each module gets its own test class inheriting from the base. Parameters to set per module:

| Module | Test File | Similarity Ceiling | Fields Tested | Stop Words Added |
|---|---|---|---|---|
| **Tarot (TAR-M4)** | `tests/test_tarot_compliance.py` | 30% | purpose, synthesis, card_context | tarot, card, spread, upright, reversed, arcana |
| **Angel Numbers** | `tests/test_angel_compliance.py` | 30% | seeing_it_means, vibration, message | angel, number, seeing, energy, meaning |
| **Festival-Region** | `tests/test_festival_compliance.py` | 40% | summary | festival, region, celebration, ritual |
| **Crystal** | `tests/test_crystal_compliance.py` | 30% | purpose, chakra_note, care | crystal, healing, chakra, energy, stone |
| **Rudraksha** | `tests/test_rudraksha_compliance.py` | 35% | meta_description | rudraksha, mukhi, bead, mantra, wearing |

---

## How to Add a New Module Test

Copy this template into `tests/test_{module}_compliance.py`:

```python
import unittest
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text

class TestModuleCompliance(unittest.TestCase):

    MODULE_NAME      = "module_name"          # ← Change
    SIMILARITY_CEIL  = 30.0                   # ← Adjust per module
    SAMPLE_SIZE      = 20                     # ← Pages to sample in test

    @classmethod
    def setUpClass(cls):
        # Module-specific boilerplate to strip before vectorization
        module_boilerplate = ["word1", "word2"]   # ← Change
        cls.stop_words = list(text.ENGLISH_STOP_WORDS.union(module_boilerplate))
        cls.vectorizer = TfidfVectorizer(
            stop_words=cls.stop_words,
            ngram_range=(1, 2),
            min_df=1,
            max_features=30_000
        )

    def _load_pages(self) -> list[str]:
        """Load SAMPLE_SIZE representative page body texts."""
        # ← Import and build page texts from module data
        raise NotImplementedError

    def test_cross_page_similarity_below_ceiling(self):
        pages = self._load_pages()
        tfidf = self.vectorizer.fit_transform(pages)
        sim = cosine_similarity(tfidf)
        # Exclude self-similarity (diagonal)
        n = len(pages)
        worst = max(
            sim[i][j]
            for i in range(n) for j in range(i + 1, n)
        ) * 100
        self.assertLess(
            worst, self.SIMILARITY_CEIL,
            f"❌ {self.MODULE_NAME}: {worst:.1f}% similarity exceeds {self.SIMILARITY_CEIL}% ceiling"
        )
        print(f"✅ {self.MODULE_NAME}: worst pair = {worst:.1f}% -- below {self.SIMILARITY_CEIL}% ceiling")
```

---

## GitHub Actions Workflow Reference

**File:** `.github/workflows/echo_pace_compliance.yml`

```yaml
name: "ECHO // PACE Content Compliance Gate"

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  compliance-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          pip install scikit-learn numpy

      - name: Run ECHO compliance tests
        run: |
          python -m pytest tests/test_tarot_compliance.py -v
```

Add additional test files to the final run command as modules are built:
```
python -m pytest tests/test_tarot_compliance.py tests/test_angel_compliance.py -v
```

---

## Scan Threshold Reference

| Status | Cosine Score | Action |
|---|---|---|
| 🔴 **BLOCKED** | ≥70% vs source EPUB | Send back to Codex for full rewrite. Do not seed. |
| 🟡 **FLAGGED** | 50-69% vs source EPUB | Human review before proceeding. |
| ✅ **CLEAN** | <50% vs source EPUB AND no 4+ word n-gram match | Safe through ECHO//PACE pipeline. |
| 🔴 **CI FAIL** | ≥30% cross-page internal | Block deploy. Apply Process 1 anchor-flip fix. |
| ✅ **CI PASS** | <30% cross-page internal | Deploy proceeds. |

---

## When to Run Each Check

| Check | Tool | When |
|---|---|---|
| Source textbook plagiarism (Layers 1-3) | `backend/scripts/textbook_plagiarism_scan.py` | After every Codex delivery, before integration |
| Cross-page internal similarity | `backend/scripts/verify_{module}_compliance.py` | Before seeding any module to MongoDB |
| Automated CI gate | GitHub Actions | Auto on every push -- no manual trigger needed |
