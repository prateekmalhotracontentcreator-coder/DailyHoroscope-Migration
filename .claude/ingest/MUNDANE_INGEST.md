# MUNDANE_INGEST.md  (Mundane Astrology -- 5 Books)
> Last updated: 2026-05-08

## Coverage
Books: Gaur (Ch 1,2,6,8,9,10,11) · Mehta (Ch 2,7,8,18,22) · Rao · Gopalakrishnan (Ch 3,4,11,14) · Raphael (Ch 8,14,22,26,27,28)
Rules: 328 interpretation rules + 102 engine specs = 430 total
Approved: **326** | PHR: 2 (intentional holds) | Flagged: 0 | Co-founder tagged: 7

## Key Scripts (Final versions only -- many intermediate versions exist v1-v22)
| Script | Purpose | Status |
|---|---|---|
| ingest_mundane_interpretation_v22.py | Final interpretation rules ingest | ✅ Done |
| ingest_mundane_engine_specs_v22.py | Final engine specs ingest | ✅ Done |
| ingest_mundane_geo_entities_v1.py | Geo entity seed data | ✅ Done |
| ingest_mundane_v2_novel_migrate.py | Novel Mundane rule migration | ✅ Done |
| run_mundane_ingest.py | Master runner | ✅ Done |
| validate_mundane_rules.py | Mundane-specific validator (use this, NOT validate_rules.py) | ✅ Done |
| split_mundane_cat_c1_rules.py | Split compound Cat C1 rules | ✅ Done |
| migrate_mundane_v3_v7_conditions.py | v3→v7 condition migration | ✅ Done |
| migrate_dual_mapping_to_engine_specs.py | Dual-mapping migration | ✅ Done |
| tag_cofounder_review_required.py | Tag 7 rules for co-founder review | ✅ --apply done 2026-05-08 |
| approve_mundane_*.py (multiple) | Category-wise approval sweeps | ✅ All done |
| patch_mundane_*.py (multiple) | NLM-driven patches | ✅ All done |

## Co-founder Review Queue (7 rules -- live, tagged)
Query: `col.find({"science_id":"mundane_jyotish","validation.cofounders_review_required":True})`

| Rule ID | Topic |
|---|---|
| mundane-gaur-ch6-ownership-rain-confirm | 24-48h timing window analyst-added |
| gaur-ch8-gold-reserve-banking-crisis-veto | "Sanghatta grid" term source |
| gaur-ch10-jupiter-cancer-sun-aspect-supremacy | "trine" = Western term |
| mundane-mehta-ch22-saturn-dhanesh-treasury-depletion | Source chapter mismatch |
| mundane-gopal-ch3-widow-pm-multiplier | +0.2 weight analyst-derived |
| mundane-gopal-ch4-volatile-nomination-chart | "2 or more planets" threshold |
| mundane-gopal-ch11-rains-rahu-capricorn-moderate | NE monsoon specifics analyst-added |

## Intentional PHR Holds (do NOT touch)
- `mundane-gopal-ch3-trikona-trikona-billionaire` -- natal rule, wrong science_id
- `mundane-mehta-ch22-raja-mantri-enemy-deadlock` -- interpretive synthesis

## ⚠️ Validator Rule
Use `validate_mundane_rules.py` for ALL mundane batches. Never `validate_rules.py`.

## Status
✅ COMPLETE -- 326/328 approved. PHR=2 intentional holds. 7 tagged for co-founder.
