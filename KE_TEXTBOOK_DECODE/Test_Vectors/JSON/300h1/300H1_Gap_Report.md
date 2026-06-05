# 300H1 Gap Report
**Batch:** `tv_300h1_decode_v1`  **Generated:** 2026-06-05

## Summary
- Total chapters decoded: 136
- Chapters with decode errors: 0
- Chapters with lagna=null: 55

## Gap Pattern Candidates
> Patterns found in author observations that are **absent** from existing KE rule set.
> These require new rule creation before Layer A/B evaluation can be applied.

| Rank | condition_type | claim_axis | case_count | Example |
|---|---|---|---|---|
| 1 | `kp_star_lord` | `career` | 150 | *It may be noted that Saturn, Jupiter are Mars are posited in own star....* |
| 2 | `kp_signification_chain` | `career` | 10 | *Ketu offers result of Sun (Govt., 09-Central) and 10 (proD....* |
| 3 | `kp_star_lord` | `marriage` | 2 | *Jupiter (05) is in 07 in the star of Rahu indicates marriage through love with a...* |
| 4 | `kp_star_lord` | `longevity` | 1 | *But Venus being lord of 05 and 10, is posited in 081h house and it is in own sta...* |

## Decode Errors
- None

## Fields with High Null Rate
- `birth_data.latitude`: expected ~70% null (chart-embedded OCR)
- `birth_data.time_local`: expected ~40% null (Format B/C chapters)
- `planet_positions_from_table.LAGNA.sign`: 55/136 null (OCR garble on lagna row)

## Recommended Next Steps for TT
1. Run engine verification on 5 sample chapters (Obama, Lincoln, Diana, Shastri, MLK) -- compare lagna/moon
2. Review `kp_star_lord` and `kp_signification_chain` rule candidates -- these are the primary KE gaps
3. Ingest candidate rules to KE after co-founder approval

*Thread 3 · 300 Important Horoscopes Vol 1 Part 1 · Step 2 output*