# KE SBC Macro Layer -- Architecture Brief
> **Status:** UPDATED 2026-05-20 -- TT decisions incorporated. Algebraic equation added. Sub-segments expanded. Ch 15/20 decode approach confirmed.
> **Prepared:** 2026-05-20 | **Author:** Claude Code
> **Covers:** science_id: "sbc_macro" · World Map Studio · Dual-track integration with α/γ layers

---

## 1. Decision Record

| Q | Decision | Confirmed By |
|---|---|---|
| Q1 -- Timing | Both natal chart + current transits simultaneously | GAI + TT |
| Q2 -- Integration | Dual-injection: α modifier + standalone γ input | GAI + TT |
| Q3 -- Subject scope | Collective macro score first → overlay on individual. Lives in World Map Studio | GAI + TT |
| Q4 -- Output format | Sector-by-sector condition map (not a single score) | GAI + TT |
| Q5 -- Relationship to Mundane | Separate `science_id: "sbc_macro"` -- distinct from `mundane_jyotish` | GAI + TT |

---

## 1b. Algebraic Equation -- Variables, Modifiers, Weightages

### Master Equation

```
γ_final = (w_α × α_adj) + (w_β × β) + (w_M × M_sector)
```

### Variable Definitions

| Symbol | Name | Formula / Source | Range |
|---|---|---|---|
| **γ_final** | Final synthesis score | Output of γ engine | [−1.0, +1.0] |
| **α_personal** | Personal rule score | Σ(r_i × c_i) / N | [0, 1.0] |
| **α_adj** | Macro-adjusted personal score | α_personal × (1 + δ_M) | [−1.0, +1.0] |
| **δ_M** | Macro environment modifier | Σ(sbc_macro_i) + Σ(mundane_baseline_i) | [−0.5, +0.5] **ceiling** |
| **β** | Questionnaire enrichment | KE-IQ profile score | [0, 1.0] |
| **M_sector** | Active sector macro score | net_score from sector_map | [−1.0, +1.0] |
| **r_i** | Individual rule weight | Encoded per rule in interpretation_rules | [0.1, 1.0] |
| **c_i** | Rule match confidence | Engine match score | [0, 1.0] |
| **N** | Applicable rules count | Rules fired for this chart | Integer |

### Proposed Initial Weightages (to be calibrated via test vectors)

| Weight | Value | Rationale |
|---|---|---|
| **w_α** | 0.60 | Birth chart is always primary signal -- cannot be suppressed below 60% |
| **w_β** | 0.20 | Questionnaire enrichment adds contextual depth |
| **w_M** | 0.20 | Macro environment is real but cannot dominate individual destiny |

### Steering Ratio Constraint (MAC-OP-1 -- confirmed ±0.5 ceiling)

```
δ_M ∈ [−0.5, +0.5]

Effect:
  If δ_M = −0.5 and α_personal = +0.8:
    α_adj = 0.8 × (1 − 0.5) = 0.40   ← macro halves personal prosperity signal
  
  If δ_M = +0.5 and α_personal = +0.8:
    α_adj = 0.8 × (1 + 0.5) = 1.0 (capped) ← macro amplifies but cannot exceed 1.0
```

### Hard Veto Rule (MAC-OP-2 -- confirmed)

```
IF M_sector.polarity == "critical_bearish"
AND α_personal > 0 (positive personal period)
THEN: γ_final ≤ +0.30   ← soft cap -- engine outputs "resilience" not "prosperity"

IF M_sector.polarity == "critical_bearish"  
AND α_personal < 0 (negative personal period)
THEN: no cap -- macro amplifies the negative fully
```

### Output Language Mapping

| γ_final range | Output tone |
|---|---|
| +0.7 to +1.0 | Strong positive prediction |
| +0.4 to +0.7 | Positive with caveats |
| +0.0 to +0.4 | "Steady growth / resilience despite macro contraction" |
| −0.3 to 0.0 | Neutral / mixed -- exercise caution |
| −0.7 to −0.3 | Stress period -- specific remedies |
| −1.0 to −0.7 | Critical -- high caution, detailed remediation |

---

## 2. Three-Layer Macro Stack

```
Layer 1 -- mundane_jyotish (General Ecology / Weather)
    → Broad planetary ingress rules: "Saturn in Pisces → marine sector stress"
    → Already in KE: 328 rules + 102 specs
    → Output: sector baseline biases (-0.4, +0.3, etc.)

        │
        ▼

Layer 2 -- sbc_macro (Precision Laser / Direct Impact)
    → SBC grid + phonetic/Nakshatra intersections: "Mars Vedha on letter B → Bitcoin hit"
    → NEW: Ch 15 + Ch 20 rules decoded into this science_id
    → Output: specific target strikes with polarity + weight_modifier

        │
        ▼

Layer 3 -- Individual natal overlay
    → User's birth chart + current dasha from vedic_calculator.py
    → Macro signals from Layers 1+2 applied as α modifier
    → Final synthesis in γ engine: "personal prosperity capped by macro contraction"
```

---

## 3. science_id: `sbc_macro` -- Rule Schema

```json
{
  "rule_id": "sbc-mcr-001",
  "science_id": "sbc_macro",
  "batch_id": "sbc-ch20-v1",
  "checkable": false,
  "approval_status": "pending_human_review",

  "trigger": {
    "condition": "vedha_intersection",
    "aspect_type": "latitudinal_cross",
    "transiting_planets": ["mars", "rahu"],
    "target_phonetic": "b",
    "target_nakshatra": null
  },

  "macro_effect": {
    "sector": "financial_markets",
    "sub_sector": "crypto_assets",
    "specific_target_phonetic": "b",
    "polarity": "critical_bearish",
    "weight_modifier": -0.8,
    "duration_type": "transit_duration"
  },

  "alpha_modifier": {
    "applies_to_science_ids": ["bphs", "kp", "sbc"],
    "scales_rules_with_axis": ["wealth", "gains", "financial_loss"],
    "modifier_direction": "amplify_negative"
  },

  "gamma_input": {
    "sector_key": "financial_markets",
    "standalone_score": -0.8,
    "injects_into_gamma": true
  },

  "source": {
    "book": "Sarvato Bhadra Chakra V2",
    "chapter": 20,
    "section": "Natal Speculation Yogas"
  }
}
```

---

## 4. Macro Output Format (Sector-by-Sector Condition Map with Sub-Segments)

Computed at session time from active `mundane_jyotish` + `sbc_macro` rules.
Each top-level sector contains sub-segments for granular targeting.

```json
{
  "macro_snapshot": {
    "computed_at": "2026-05-20T18:00:00Z",
    "epoch_ref": "era-2025-2028-saturn-pisces",
    "location_ref": "india",

    "sector_map": {

      "commodity_markets": {
        "net_score": -0.5,
        "polarity": "bearish",
        "active_signals": ["sbc-ch15-mcr-007"],
        "sub_segments": {
          "gold":              { "score": -0.3, "polarity": "mildly_bearish" },
          "silver":            { "score": -0.4, "polarity": "bearish" },
          "crude_oil":         { "score": -0.6, "polarity": "bearish" },
          "natural_gas":       { "score": -0.5, "polarity": "bearish" },
          "agricultural":      { "score": +0.2, "polarity": "mildly_bullish" },
          "metals_industrial": { "score": -0.3, "polarity": "mildly_bearish" }
        }
      },

      "geopolitical_stability": {
        "net_score": -0.4,
        "polarity": "stress",
        "active_signals": ["sbc-mcr-019"],
        "sub_segments": {
          "internal_stability":    { "score": -0.2, "polarity": "mild_stress" },
          "border_neighbours":     { "score": -0.6, "polarity": "high_tension" },
          "international_trade":   { "score": -0.3, "polarity": "caution" },
          "political_leadership":  { "score": -0.1, "polarity": "stable" },
          "military_security":     { "score": -0.5, "polarity": "elevated_alert" }
        }
      },

      "sector_analysis": {
        "net_score": -0.2,
        "polarity": "mixed",
        "note": "Auto sector used as economic health proxy -- strong auto = country rising",
        "sub_segments": {
          "auto_manufacturing":    { "score": +0.3, "polarity": "bullish", "health_proxy": true },
          "technology":            { "score": +0.4, "polarity": "bullish" },
          "banking_finance":       { "score": -0.4, "polarity": "stress" },
          "healthcare_pharma":     { "score": +0.5, "polarity": "expansion" },
          "real_estate":           { "score": -0.3, "polarity": "contraction" },
          "agriculture_food":      { "score": +0.2, "polarity": "stable" },
          "energy_utilities":      { "score": -0.4, "polarity": "stress" },
          "infrastructure":        { "score": +0.1, "polarity": "neutral" }
        }
      },

      "financial_markets": {
        "net_score": -0.7,
        "polarity": "critical_bearish",
        "active_signals": ["sbc-mcr-001", "mnd-jyt-042"],
        "sub_segments": {
          "equity_indices":   { "score": -0.6, "polarity": "bearish" },
          "crypto_assets":    { "score": -0.8, "polarity": "critical_bearish" },
          "bonds_debt":       { "score": -0.3, "polarity": "mild_stress" },
          "forex":            { "score": -0.4, "polarity": "volatile" },
          "primary_markets":  { "score": -0.5, "polarity": "bearish" }
        }
      },

      "public_health": {
        "net_score": +0.8,
        "polarity": "expansion",
        "active_signals": ["mnd-jyt-005"],
        "sub_segments": {
          "epidemic_risk":         { "score": +0.7, "polarity": "low_risk" },
          "mental_health_stress":  { "score": -0.2, "polarity": "mild_stress" },
          "healthcare_access":     { "score": +0.6, "polarity": "improving" }
        }
      }
    }
  }
}
```

---

## 5. World Map Studio -- Architecture Note (Internal)

> ⚠️ Internal discussion point only. Fine-tune iteratively -- do not over-engineer Phase 1.

World Map Studio (future KE Codex module) is the home for Q3:
- Country/location-level macro condition maps -- computed and stored
- Live updates as planetary transits change
- Each location has a macro profile that **refines the Mundane Score**
- Output feeds into the individual overlay (Layer 3 above)

**Phase 1 output -- broad advisory remarks only:**
- "Inter-region unrest likely. Proceed carefully in foreign trade."
- "Domestic political pressure. Internal stability score: moderate stress."
- "Commodity cycle turning. Export-linked sectors: caution."

These broad remarks will be fine-tuned iteratively as the engine matures. No precision claims in Phase 1.

**Steering Ratio: CONFIRMED ±0.5 ceiling (MAC-OP-1)**
- Macro cannot suppress birth chart by more than 50%
- w_α = 0.60 minimum weight always preserved
- Severe macro event softens (not eliminates) individual positive predictions -- see Hard Veto Rule in §1b

---

## 6. Dual-Track Integration with α and γ

### α (Alpha) Modification

When a `sbc_macro` rule fires on `financial_markets: critical_bearish (-0.8)`:
- All individual rules with `claim_axis: "wealth"` or `"financial_loss"` have their confidence score scaled by the macro modifier
- A natal rule predicting "sudden financial gain" at α=0.7 becomes α=0.56 (×0.8 downward pressure)
- A natal rule predicting "financial loss" at α=0.6 becomes α=0.84 (macro amplifies the negative)

### γ (Gamma) Standalone Input

The sector map is passed as a standalone context block to the γ synthesis engine:
- γ receives: personal α scores + questionnaire β + macro sector map
- γ output language changes: "immense wealth accumulation" → "steady growth despite macro contraction"
- Hard veto: if macro polarity is `critical_bearish` AND personal dasha is also negative, γ cannot output a net-positive financial prediction

---

## 7. Two MongoDB Collections for Macro Layer

| Collection | Purpose | Update Frequency |
|---|---|---|
| `macro_realtime_ticks` | 15-min cache of active macro signals from live transits | Every 15 min (cron job) |
| `macro_generational_eras` | Pre-computed 50-year epoch baselines (Saturn/Jupiter ingress periods) | Static; updated on ingress only |

### `macro_generational_eras` sample
```json
{
  "_id": "era-2025-2028-saturn-pisces",
  "start_date": "2025-03-29",
  "end_date": "2028-06-02",
  "anchor_planet": "saturn",
  "anchor_sign": "pisces",
  "sector_baselines": {
    "financial_markets": { "bias": -0.4, "description": "Liquidity contraction, banking evolution" },
    "geopolitical_stability": { "bias": -0.6, "description": "Maritime conflicts, border redefining" },
    "commodity_markets": { "bias": -0.3, "description": "Marine commodity pressure, oil volatility" }
  }
}
```

---

## 8. Additional Macro Streams (Recommended by GAI -- For TT Decision)

| Stream | What It Adds | Integration Point | Priority |
|---|---|---|---|
| **KP Ruling Planets** | Binary veto on macro predictions | α-veto layer -- KP Sub-Lords deny/confirm macro signal | 🔴 HIGH -- already in KE |
| **Tajika/Varshaphala** | Annual macro anchor per country/leader natal chart | γ input -- annual theme override | 🟡 MED -- future phase |
| **Bradley Siderograph** | Market turning point curve (numerical planetary aspects) | Standalone γ score for `financial_markets` | 🟡 MED -- future phase |
| **NOAA Kp-index** | Geomagnetic storm activity → human volatility signal | External API → `macro_realtime_ticks` flag | 🟢 LOW -- Phase 3 |
| **VIX / Market Data** | Real-world confirmation of astrological macro signal | Validation layer -- confirms `sbc_macro` fire | 🟢 LOW -- Phase 3 |

---

## 9. Ch 15 + Ch 20 Decode -- Approach Confirmed

> **TT Decision (2026-05-20):** Do NOT decode fresh. Ask CC thread to **review and refine the existing Notebook LM base** for Ch 15 and Ch 20. NLM output is the starting point; CC thread does a review + refinement pass.

### Ch 15 -- Commodity Prices (Teji-Mandi)
- **Approach:** CC thread reviews NLM Ch 15 output, refines into `sbc_macro` rule schema
- **Rules target:** ~50 rules on commodity direction (Teji = bullish, Mandi = bearish)
- **science_id:** `sbc_macro`
- **sector mapping:** `commodity_markets` with sub-segments (Gold, Silver, Oil, Gas, Agricultural, Industrial Metals)
- **Lookup collection needed:** `sbc_commodity_coordinates`
- **Not a trading tool** -- macro condition signal only

### Ch 20 -- Financial Markets / Speculation
- **Approach:** CC thread reviews NLM Ch 20 output, refines into `sbc_macro` rule schema
- **Rules target:** ~148 rules (Natal Speculation Yogas 58 + Lead-Lag engine 50 + Primary Market allotment)
- **science_id:** `sbc_macro`
- **sector mapping:** `financial_markets` with sub-segments (equity, crypto, bonds, forex, primary markets)
- **Phonetic mapping (MAC-OP-3):** International asset names to Sanskrit phonetic root. Methodology to be defined by CC thread during refinement pass.

### Ch 19 -- PM Validation (Test Vectors, not macro)
- Separate pipeline -- see `KE_TestVector_Pipeline_TechSpec.md`

---

## 10. Open Points for TT Decision

| # | Question | Priority |
|---|---|---|
| MAC-OP-1 | Steering Ratio: maximum macro modifier ceiling on individual α score? | 🔴 Blocking |
| MAC-OP-2 | Does a `critical_bearish` macro hard-cap individual positive predictions? | 🔴 Blocking |
| MAC-OP-3 | Phonetic mapping methodology for international names (Bitcoin → Ba)? | 🟠 High |
| MAC-OP-4 | Ch 20 Primary Market allotment rules -- in scope or defer to Phase 2? | 🟠 High |
| MAC-OP-5 | KP Ruling Planets as α-veto -- use existing KP rules or build separate veto layer? | 🟡 Med |
| MAC-OP-6 | World Map Studio: build as separate Codex commission or part of macro ingest? | 🟡 Med |

---

## 11. Commissions Required

| Commission ID | Scope | Dependency | Status |
|---|---|---|---|
| **KE-SBC-MAC-1** | Ch 15 decode → `sbc_macro` rules + `sbc_commodity_coordinates` collection | KE freeze + MAC-OP-3 resolved | READY TO BRIEF when TT approves |
| **KE-SBC-MAC-2** | Ch 20 decode → `sbc_macro` rules (148 rules) | KE freeze + MAC-OP-3 + MAC-OP-4 | After KE-SBC-MAC-1 |
| **KE-MACRO-RT** | `macro_realtime_ticks` cron job + `macro_generational_eras` seed | MAC-OP-1 + MAC-OP-2 resolved | Phase 2 |
| **KE-WORLD-MAP** | World Map Studio -- country/location macro profiles | Full macro layer live | Phase 3 |
