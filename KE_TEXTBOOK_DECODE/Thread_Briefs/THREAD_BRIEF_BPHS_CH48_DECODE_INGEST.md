# Thread Brief -- BPHS Vol 2 Ch.48 Decode + Ingest
## Status · Schema Design · Immediate Actions

> Prepared by: Claude Code
> Date: 2026-06-03 (last updated: 2026-06-04)
> For: BPHS Vol 2 Ch.48 Decode Thread
> Status: **🟠 DECODE COMPLETE -- 46 rules decoded, dedup clean. BLOCKED on MongoDB credentials for live ingest. TT action required.**

---

## One-Liner

Decode BPHS Vol 2 Chapter 48 ("Distinctive Effects of Vimshottari Dasa Lords") from source RTF into schema-compliant JSON, then ingest to `horoscope_db`. This chapter requires a unique rule category not used in Ch.47/Ch.52-58.

---

## Why This Is a Fresh Decode (Not a Migration)

An old ingest exists in the **EverydayHoroscope DB** (batch `bphs-ch48-dasha-20260416`, 34 rules). Do NOT use or migrate those rules. Issues:

1. `dasha_lord: "Moon"` set on every rule -- wrong. Ch.48 has no fixed dasha_lord; effects depend on which house a planet lords in the natal chart.
2. Condition structure is not typed -- rules are not KE-queryable as house-lord-position conditions.
3. The old decode missed the Harsha/Sarala/Vimala yoga rules' yoga_check treatment.

---

## Chapter Overview

| Field | Value |
|---|---|
| **Chapter** | BPHS Vol 2, Chapter 48 |
| **Title** | Distinctive Effects of the Nakshartra Dasa / Dasas of the lords of various houses (Vimshottari Dasa) |
| **Dasha lord** | NOT a fixed planet -- rules apply to whichever planet lords a specific house in the natal chart |
| **Sloka count** | 20 slokas (slokas 1-20) plus translator's Notes sections |
| **Source RTF** | `/Users/apple/Documents/Knowledge Engine_eBooks/PDF Chapters to RTF/BPHS Ch 48 Vol 2.rtf` |
| **Batch ID (new)** | `bphs-ch48-dasha-20260603` |
| **Target DB** | `horoscope_db` |
| **Estimated rules** | 35-50 |

---

## Source RTF Content Summary

The chapter has four distinct sections:

### Section A -- Per-House Dasa Effects (slokas 1-8)
Basic effects of the dasa of the lord of each house (1st through 12th):
- 1st lord dasa → physical wellbeing
- 2nd lord dasa → distress + possibility of death (maraka)
- 3rd lord dasa → unfavourable effects
- 4th lord dasa → acquisition of house and land
- 5th lord dasa → educational progress + happiness from children
- 6th lord dasa → danger from enemies + ill health
- 7th lord dasa → distress to wife + possibility of native's death (maraka)
- 8th lord dasa → possibility of death + financial losses
- 9th lord dasa → educational improvement + religious mindedness + unexpected gains
- 10th lord dasa → recognition and awards by government
- 11th lord dasa → obstacles in wealth gains + possible diseases
- 12th lord dasa → distress + danger from diseases

Also sloka 1: general principle -- planet in auspicious house/exaltation → favourable dasa; planet in debilitation/inauspicious house → adverse dasa.

Translator's Note (after slokas 2-8): Nuances -- 2nd/7th lords also have positive indications (wealth, marriage) when well placed. 3rd/6th/11th lords in their own house/sign may not give evil. 6th/8th/12th (dusthanas) can give yoga effects (Harsha/Sarala/Vimala -- see Section B).

### Section B -- Harsha, Sarala, Vimala Yogas (part of translator's Notes)
Three yoga exceptions for dusthana lords:
- **Harsha Yoga**: 6th house occupied/aspected by malefics AND 6th lord in dusthana (6th/8th/12th) → happiness, good fortune, strong constitution, overcomes enemies
- **Sarala Yoga**: 8th lord placed in the 6th, 8th, or 12th → long-lived, fearless, prosperous, learning, children, riches
- **Vimala Yoga**: 12th lord in dusthana aspected/associated with malefics → spends little, saves much, good to everyone, happy and independent

### Section C -- Kendra-Trikona Combinations (slokas 9-17)
Yoga principles determining which dasas are favourable:
- Lord of 9th + 10th in conjunction with 5th lord → both dasas beneficial
- Any planet associated with 5th lord → dasa favourable
- 10th + 4th lords associated with 9th lord → dasas favourable
- **Lord of kendra in trikona → dasa extremely favourable**
- **Lord of trikona in kendra → dasa extremely favourable**
- 6th/8th/12th lord associated with trikona lord → dasa becomes favourable
- Planet associated with kendra/trikona lord → dasa favourable
- Planet aspected by kendra lord → dasa favourable
- Planet aspected by trikona lord → dasa favourable
- 9th lord in Ascendant + Ascendant lord in 9th → both dasas extremely beneficial
- 10th lord in Ascendant + Ascendant lord in 10th → both dasas extremely beneficial (kingdom attainment)

### Section D -- Unfavourable Dasa Conditions (slokas 18-20)
- Dasa of lord of 3rd, 6th, or 11th → unfavourable
- Dasa of planet posited in 3rd, 6th, or 11th → unfavourable
- Dasa of planet in conjunction with lord of 3rd/6th/11th → unfavourable
- Dasa of planet associated with maraka lord (2nd/7th) in the 2nd or 7th → unfavourable
- Dasa of planet posited in 8th → unfavourable
- **Exception**: Rahu and Ketu in 3rd/6th/11th (upachaya houses) → favourable

---

## Schema Requirements

### Critical: `dasha_lord` Must Be Null

These rules do NOT have a fixed `dasha_lord`. The effect depends on which house the currently running planet lords in the user's natal chart. Set:

```json
"dasha_lord": null,
"dasha_type": "vimshottari_any"
```

### Condition Type: `house_lord_position`

For Section A and D rules (per-house effects), use:

```json
"condition": {
  "type": "house_lord_position",
  "house_lord_of": 7,
  "description": "Planet running its dasha is lord of the 7th house"
}
```

For kendra-trikona combination rules (Section C), use:

```json
"condition": {
  "type": "house_lord_position",
  "house_lord_of": "kendra",
  "planet_position": {"house_type": "trikona"},
  "description": "Lord of kendra placed in trikona"
}
```

For yoga rules (Section B), use `checkable: true` and:

```json
"condition": {
  "type": "yoga_check",
  "yoga_name": "Harsha Yoga",
  "description": "6th house occupied/aspected by malefics AND 6th lord in dusthana (6th/8th/12th)"
}
```

### `effect_polarity` Field

Use:
- `"dasha_favourable"` for positive dasa effects
- `"dasha_unfavourable"` for negative dasa effects
- `"dasha_conditional"` for nuanced/qualified effects

### `source` Block

```json
"source": {
  "book": "Brihat Parashara Hora Shastra",
  "volume": 2,
  "chapter": 48,
  "sloka_range": "5-8",
  "batch_id": "bphs-ch48-dasha-20260603",
  "translator": "R. Santhanam"
}
```

### `metadata` Block

```json
"metadata": {
  "science_id": "vedic_jyotish",
  "rule_category": "vimshottari_dasha",
  "subcategory": "house_lord_dasha_effects",
  "checkable": false
}
```

For Harsha/Sarala/Vimala yoga rules:
```json
"metadata": {
  "science_id": "vedic_jyotish",
  "rule_category": "yoga",
  "subcategory": "dusthana_yoga",
  "yoga_name": "Harsha Yoga",
  "checkable": true,
  "yoga_check": {
    "type": "yoga_check",
    "checkable": true,
    "yoga_name": "Harsha Yoga"
  }
}
```

---

## Rule ID Convention

```
R-BPHS48-{sequence_number}-{hex_suffix}
```

Example: `R-BPHS48-001`, `R-BPHS48-002`, etc.

Do NOT reuse old PATCH rule IDs from the old decode (R-BPHS48-PATCH-xxxxxx). These are for the old EverydayHoroscope DB only and are being superseded.

---

## Expected Rule Breakdown

| Section | Count | Notes |
|---|---|---|
| A -- Per-house dasa effects (slokas 1-8) | ~14 | 1 rule per house (12) + 2 general placement rules |
| B -- Harsha/Sarala/Vimala yogas | 3 | yoga_check = true |
| C -- Kendra-trikona combinations (slokas 9-17) | ~12 | Positional yoga rules |
| D -- Unfavourable conditions (slokas 18-20) | ~8 | Dusthana/maraka/upachaya rules |
| **Total** | **~37** | |

---

## Output Files Required

Standard 5-file decode set:

1. `BPHS_Ch48_Vol2_Rules.json` -- rules array
2. `BPHS_Ch48_Vol2_NLM_Extract.md` -- natural language mapping (sloka → rule)
3. `BPHS_Ch48_Vol2_Contradictions.json` -- within-chapter contradictions (likely 0)
4. `BPHS_Ch48_Vol2_Summary.md` -- chapter summary + rule count breakdown
5. `BPHS_Ch48_Vol2_Diagnostic.md` -- decode decisions, schema choices, any OCR issues

Output folder: `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/`

---

## Ingest Process (After Decode)

Standard 7-step process per `INGEST_PROCESS_BRIEF.md`:

1. Schema audit (confirm all required fields present)
2. Dedup vs full MongoDB export
3. Upload via `ingest_from_json_folder.py` or dedicated script, batch_id = `bphs-ch48-dasha-20260603`
4. Post-ingest structural validation
5. Doctrinal validator (Claude quality check)
6. Triage flagged rules (use three-bucket method)
7. Update TRACKER.md + A2_INGEST_LOG.md

---

## What Has Been Done (2026-06-04)

| Action | Date | Result |
|---|---|---|
| Source RTF read and chapter text extracted | 2026-06-04 | Full text: Slokas 1-20 + both translator's notes sections |
| Schema audit: condition type verified | 2026-06-04 | `dasha_of_house_lord` confirmed correct (NOT `house_lord_position`) |
| Fresh decode: 5-file set created | 2026-06-04 | 46 rules, 0 OCR issues, 0 genuine within-chapter contradictions |
| Dedup vs BPHS Vol 1 CC Decode folder | 2026-06-04 | 0 genuine duplicates (181 empty-text false positives -- dedup limitation when `full_text` absent) |
| Dedup vs MongoDB | 2026-06-04 | ❌ BLOCKED -- MongoDB auth failure (credentials rotated since last session) |
| Ingest script written + dry-run validated | 2026-06-04 | `ingest_bphs_ch48_dasha.py` -- 46 rules, 0 structural issues |

---

## Open Points

| # | Item | Owner | Priority |
|---|---|---|---|
| ~~CH48-OP-01~~ | ~~Issue fresh decode commission to Codex~~ | TT | ✅ DONE -- CC completed decode directly 2026-06-04 |
| ~~CH48-OP-02~~ | ~~Confirm condition.type "house_lord_position"~~ | CC | ✅ RESOLVED -- correct type is `dasha_of_house_lord` (confirmed ke_schema_constants.py line 17) |
| CH48-OP-03 | Dedup vs existing BPHS Vol 2 rules in MongoDB | CC | 🔴 BLOCKED -- MongoDB auth failure. TT must provide working credentials. |
| **CH48-OP-04** | **MongoDB credentials renewal + ingest** | **TT** | **🔴 CRITICAL -- Credentials used in prior session no longer work. Provide updated MONGO_URL.** |
| CH48-OP-05 | Run validate_rules.py against batch `bphs-ch48-dasha-20260603` after ingest | CC | 🟠 HIGH -- run immediately after ingest |
| CH48-OP-06 | Co-founder sign-off on auto_approved rules | TT | 🟡 MEDIUM -- after validation + triage |

---

## Ingest Command (Ready to Run)

Once working MONGO_URL is available:
```bash
export MONGO_URL="mongodb+srv://user:pass@cluster0.bqtc8l9.mongodb.net/?appName=Cluster0"
python3 backend/scripts/ingest_bphs_ch48_dasha.py
```

Then validate:
```bash
python3 backend/scripts/validate_rules.py --batch-id bphs-ch48-dasha-20260603
```

---

## Decode Output Files

All in `/Users/apple/Documents/Knowledge Engine_eBooks/BPHS_Vol2_CC_Decode/`:

| File | Status |
|---|---|
| `BPHS_Ch48_Vol2_Rules.json` | ✅ 46 rules, schema-compliant |
| `BPHS_Ch48_Vol2_NLM_Extract.md` | ✅ Full sloka → rule mapping |
| `BPHS_Ch48_Vol2_Contradictions.json` | ✅ 0 genuine, 9 apparent resolved |
| `BPHS_Ch48_Vol2_Summary.md` | ✅ Rule breakdown + design decisions |
| `BPHS_Ch48_Vol2_Diagnostic.md` | ✅ All decode decisions documented |

---

## Decode Highlights

- **46 rules total** -- covers all 20 slokas + translator's notes (maraka nuance, Harsha/Sarala/Vimala yogas, Rahu/Ketu exception)
- **Schema correction:** `dasha_of_house_lord` (not `house_lord_position`) for per-house rules
- **3 yoga rules** with `checkable: true` -- Harsha, Sarala, Vimala yogas (from Phaladeepika Ch.VI)
- **2 Parivartana rules** (036, 037) encoded as `composite` with dual `house_lord_in_house` conditions
- **Rahu/Ketu** encoded with specific `dasha_lord` -- the only planet-specific rules in this chapter
- **0 genuine contradictions** -- all 9 apparent contradictions are resolved complementary pairs or yoga exceptions

---

## Notes

- Old batch `bphs-ch48-dasha-20260416` (EverydayHoroscope DB) is superseded and should be ignored.
- Ch.48 rules are unique in the BPHS Vol 2 corpus -- they are general dasha quality principles, not per-planet antardasha effects. The KE will need to match these rules against a user's chart by checking which house the currently running dasha planet lords.
- Rahu/Ketu upachaya exception (3rd/6th/11th → favourable) encoded as `dasha_lord: "rahu"/"ketu"` with `planet_in_house`-adjacent condition.
- Dedup false positive issue: when Ch48 rules have no `full_text` field, ke_dedup_script.py matches on condition type alone, producing empty-text identical matches. For Ch48, all rules use `interpretation.detailed` -- future sessions should patch `ke_dedup_script.py` to also check `interpretation.detailed` when `full_text` is absent.
