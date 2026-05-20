# KE SBC Macro Layer -- Architecture Brief
> **Status:** DRAFT -- Architecture confirmed via GAI. Awaiting TT scope-in decision for Ch 15 + Ch 20 decode.
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

## 4. Macro Output Format (Sector-by-Sector Condition Map)

Computed at session time from active `mundane_jyotish` + `sbc_macro` rules:

```json
{
  "macro_snapshot": {
    "computed_at": "2026-05-20T18:00:00Z",
    "epoch_ref": "era-2025-2028-saturn-pisces",

    "sector_map": {
      "financial_markets": {
        "baseline_bias": -0.4,
        "sbc_modifier": -0.8,
        "net_score": -0.7,
        "polarity": "critical_bearish",
        "active_signals": ["sbc-mcr-001", "mnd-jyt-042"]
      },
      "geopolitical_stability": {
        "baseline_bias": -0.2,
        "sbc_modifier": -0.3,
        "net_score": -0.4,
        "polarity": "stress",
        "active_signals": ["sbc-mcr-019"]
      },
      "public_health": {
        "baseline_bias": 0.8,
        "sbc_modifier": 0.0,
        "net_score": 0.8,
        "polarity": "expansion",
        "active_signals": ["mnd-jyt-005"]
      },
      "commodity_markets": {
        "baseline_bias": -0.3,
        "sbc_modifier": -0.5,
        "net_score": -0.5,
        "polarity": "bearish",
        "active_signals": ["sbc-ch15-mcr-007"]
      }
    }
  }
}
```

---

## 5. World Map Studio -- Architecture Note

World Map Studio (future KE Codex module) is the home for Q3:
- Country/location-level macro condition maps -- computed and stored
- Live updates as planetary transits change
- Each location has a macro profile that **refines the Mundane Score**
- Output feeds into the individual overlay (Layer 3 above)

**Critical open point: Steering Ratio**
The sensitivity of the macro layer vs. birth chart must be calibrated so macro conditions do not suppress or override individual birth chart signals entirely.

TT decision needed:
- What is the maximum macro modifier weight? (Suggested ceiling: ±0.5 on any individual α score)
- Does a severe macro event (e.g., global war) hard-cap individual positive predictions? Or soften them?
- Is the Steering Ratio fixed, or user-configurable per report type?

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

## 9. Ch 15 + Ch 20 Decode -- What Needs to Happen

### Ch 15 -- Commodity Prices (Teji-Mandi)
- **Rules to extract:** ~50 rules on commodity price direction (Teji = bullish, Mandi = bearish)
- **science_id:** `sbc_macro`
- **sector mapping:** `commodity_markets`
- **Lookup collection needed:** `sbc_commodity_coordinates` (commodities → star/sign/planet significators)
- **Not a trading tool** -- macro condition signal only

### Ch 20 -- Financial Markets / Speculation
- **Rules to extract:** ~148 rules (Natal Speculation Yogas 58 + Lead-Lag engine 50 + Primary Market allotment)
- **science_id:** `sbc_macro`
- **sector mapping:** `financial_markets`, `crypto_assets`, `primary_markets`
- **Key open question:** Phonetic mapping for international asset names (e.g., "Bitcoin" → "Ba" phonetic) -- methodology TBD

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
