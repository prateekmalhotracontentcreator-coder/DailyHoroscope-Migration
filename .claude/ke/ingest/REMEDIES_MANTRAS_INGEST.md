# REMEDIES_MANTRAS_INGEST.md  (Jyotish Remedies & Mantras -- Book E)
> Last updated: 2026-05-08

## Coverage
100 Mantra Remedies (IDs 1-100, science_id: jyotish_remedies_mantras)
Total Rules: 100 | Auto-Approved: 45 | PHR: 50 | Flagged: 0

## Scripts Run
| Script | Purpose | Status |
|---|---|---|
| ingest_remedies_v1.py | 100 Mantra Remedies ingest | ✅ Done |
| patch_remedies_flags.py | Flag fixes | ✅ Done |
| validate_rules.py | Validation sweep | ✅ Done |

## Schema Fields
`id, remedy_area, deity, severity, mantra, yantra, paksha, tithi_day, season, frequency,
donation_item, process_direction, attire_color, muhurta, guidance,
trigger_birth_chart, trigger_ke_inference`

## Open Issues
1. **PHR triage pending** -- 50 PHR rules, no NLM session done yet
2. **Ingest script reference** -- use `ingest_remedies_v1.py` as template for Part B scripts

## Status
INGESTED ✅ | PHR triage: PENDING
