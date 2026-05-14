#!/usr/bin/env python3
"""
ingest_mundane_engine_specs_v21.py

Engine specs for Gopal Chapter 11 — How to Predict Rains
Batch: mundane-engine-v21-20260508

1 spec:
  gopal-ch11-rain-forecasting-engine
    Full seasonal rain forecasting framework — drought classification,
    Rahu Transit Veto (4 signs), SW/NE monsoon windows, Dhana Chakra,
    Tajika ingress 4th-house audit, Prasna Marga income-vs-expense
    balance gate, 2002 drought case study.

Complementary layer to Gaur Ch5/6 (v16, batch mundane-interp-v16-20260507):
  - Gaur Ch5/6: day-specific / entry-nakshatra level (Ardra Entry,
    Rohini Samudra Chakra, Trinadi, Saptnadi)
  - Gopal Ch11: seasonal / annual macro level (Rahu transit, Tajika chart,
    Prasna Marga)
  Zero overlap confirmed before authoring.

Usage:
  # Dry run (default):
  python3 backend/scripts/ingest_mundane_engine_specs_v21.py

  # Live upload:
  python3 -c "
  import asyncio, os
  exec(open('backend/scripts/ingest_mundane_engine_specs_v21.py').read().replace('DRY_RUN   = True', 'DRY_RUN   = False'))
  asyncio.run(run())
  "
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"   # overridden by exec-replace pattern
DB_NAME   = "horoscope_db"
BATCH_ID  = "mundane-engine-v21-20260508"
DRY_RUN   = True

NOW = datetime.now(timezone.utc).isoformat()

SPECS = [
    {
        "spec_id":   "gopal-ch11-rain-forecasting-engine",
        "batch_id":  BATCH_ID,
        "source":    "Gopalakrishnan — Mundane Astrology, Chapter 11: How to Predict Rains",
        "scope":     "seasonal_and_annual",
        "created_at": NOW,
        "updated_at": NOW,

        "complementary_layer_note": (
            "This spec operates at the seasonal/annual macro level and is "
            "designed to complement Gaur Ch5/6 (v16) which operates at the "
            "day-specific entry-nakshatra level (Ardra Entry, Rohini Samudra "
            "Chakra, Trinadi, Saptnadi). Zero rule overlap."
        ),

        # ── Drought Classification ─────────────────────────────────────────
        "drought_severity_matrix": {
            "meteorological": (
                "Rainfall deficiency > 20% compared to long-period normal. "
                "Primary indicator: measured against IMD baseline for the region."
            ),
            "hydrological": (
                "Depletion of surface water bodies — rivers, reservoirs, and "
                "groundwater aquifers dry up even if some rain falls. "
                "Triggered when rains are erratic rather than absent."
            ),
            "agricultural": (
                "Inadequate soil moisture resulting in acute crop stress and "
                "yield failure. May occur even when meteorological drought is "
                "absent, if rains fall at wrong crop stages."
            ),
            "severity_triage": (
                "Meteorological drought → trigger rainfall-alert rules. "
                "Hydrological drought → activate reservoir-monitoring rules. "
                "Agricultural drought → activate crop-stress and price-surge rules."
            ),
        },

        # ── Monsoon Windows ────────────────────────────────────────────────
        "monsoon_windows": {
            "south_west_monsoon": {
                "window":  "June to September (Aashadh–Bhadrapad)",
                "coverage": "~75% of India's annual rainfall",
                "entry_check": (
                    "Sun ingress Gemini (June 15 ±2 days) is the primary "
                    "diagnostic moment for SW monsoon strength."
                ),
            },
            "north_east_monsoon": {
                "window":  "October to December (Ashwin–Margsheersh)",
                "coverage": "Primary for Tamil Nadu, coastal Andhra, Kerala",
                "entry_check": (
                    "Sun ingress Libra (October 17 ±2 days) is the primary "
                    "diagnostic moment for NE monsoon strength."
                ),
            },
        },

        # ── Rahu Transit Veto ──────────────────────────────────────────────
        "rahu_transit_veto": {
            "disruptive_signs": ["Taurus", "Scorpio", "Leo", "Capricorn"],
            "mechanism": (
                "Rahu's transit through any of these four fixed/structural "
                "signs disrupts the national water cycle. The effect operates "
                "at the macro level — it skews the seasonal distribution rather "
                "than eliminating rainfall entirely."
            ),
            "priority_ranking": {
                "rank_1_critical": (
                    "Taurus (Rishabha) — historically produces the most severe "
                    "hydrological disruption; validated by 2002 national drought."
                ),
                "rank_2_severe": (
                    "Scorpio (Vrichika) — mirror axis of Taurus; severe NE "
                    "monsoon disruption and southern drought risk."
                ),
                "rank_3_moderate": (
                    "Leo (Simha) — fixed fire sign; excess heat, reduced cloud "
                    "formation, and deficient SW monsoon onset."
                ),
                "rank_4_moderate": (
                    "Capricorn (Makara) — fixed earth sign; cold disruption of "
                    "NE monsoon; Himalayan watershed stress."
                ),
            },
            "amplifier": (
                "IF Rahu is in Taurus or Scorpio AND current National Dasha/Bhukti "
                "lord is Saturn → elevate to CRITICAL RAINFALL ALERT. "
                "Saturn amplifies Rahu's disruptive effect on the water cycle."
            ),
        },

        # ── Dhana Chakra ───────────────────────────────────────────────────
        "dhana_chakra": {
            "description": (
                "A nakshatra-based moisture gauge. Monitor planets in specific "
                "moisture-bearing nakshatras at the moment of SW or NE monsoon "
                "onset (Sun ingress chart). More planets in watery nakshatras "
                "= higher moisture forecast."
            ),
            "watery_nakshatras": [
                "Rohini", "Ardra", "Punarvasu", "Ashlesha",
                "Magha", "Uttara Phalguni", "Hasta", "Chitra",
                "Anuradha", "Jyeshtha", "Moola", "Uttara Ashadha",
                "Shravana", "Dhanishtha", "Satabhisha", "Uttara Bhadrapada",
                "Revati",
            ],
            "diagnostic": (
                "Count planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, "
                "Saturn, Rahu, Ketu) in watery nakshatras at ingress moment. "
                "Score ≥ 5: Good monsoon. Score 3–4: Normal. Score ≤ 2: Deficient."
            ),
        },

        # ── Tajika Ingress Chart Audit ────────────────────────────────────
        "tajika_ingress_audit": {
            "primary_chart": (
                "Sun ingress chart for the start of the monsoon season "
                "(June 15 ± 2 days for SW monsoon; Oct 17 ± 2 days for NE). "
                "Cast for capital city (New Delhi for national forecast)."
            ),
            "4th_house_audit": {
                "positive_signal": (
                    "4th house contains Moon or Venus, OR 4th lord is in a "
                    "watery sign (Cancer, Scorpio, Pisces), OR unafflicted "
                    "Jupiter aspects the 4th house → Positive rainfall forecast."
                ),
                "negative_signal": (
                    "4th house contains Mars or Saturn without benefic aspect, "
                    "OR 4th lord is Retrograde in a fiery sign → Rain deficiency "
                    "alert for that ingress period."
                ),
            },
            "prasna_balance_gate": {
                "method": "Prasna Marga income-vs-expense analogy",
                "income_house": "2nd house (Rain Income — cloud formation capacity)",
                "expense_house": "12th house (Evaporation/Loss — dissipation of moisture)",
                "positive": (
                    "IF 2nd-house benefic strength > 12th-house malefic strength "
                    "→ Rain income exceeds evaporation expense → Good rainfall."
                ),
                "negative": (
                    "IF 12th-house malefic strength > 2nd-house strength → "
                    "Evaporation/waste exceeds actual precipitation → "
                    "Negative Rainfall Balance: seasonal deficit expected."
                ),
            },
            "agricultural_stress_check": {
                "trigger": (
                    "Mars in 4th house of Sun ingress chart AND 12th lord in 1st "
                    "house → Socio-economic alert: significant crop stress likely; "
                    "potential for famine-like conditions in rain-dependent states."
                ),
            },
        },

        # ── Narada Samhita Yearly Ruler ───────────────────────────────────
        "narada_samhita_rainfall_by_lord": {
            "description": (
                "The planetary ruler of the Samvatsar year (Narada Samhita) "
                "sets the macro-level rainfall expectation for that year. "
                "Use as background modifier before applying Rahu veto or "
                "Tajika ingress audit."
            ),
            "planet_rainfall_quality": {
                "Sun":     "Scanty rain; heat and disease.",
                "Moon":    "Plentiful rains; cheap grains. Best moisture year.",
                "Mars":    "Plentiful grains but wars; peace breached. Adequate rain.",
                "Mercury": "Satisfactory rains; good harvest. Balanced year.",
                "Jupiter": "Medium grain production; rains adequate but not excessive.",
                "Venus":   "Excessive rains; floods possible. Agricultural surplus.",
                "Saturn":  "Famine/misery; deficient rain in most years.",
                "Rahu":    "Crops destroyed; people weak. Drought risk elevated.",
                "Ketu":    "Plentiful rains/grains; generally positive moisture year.",
            },
        },

        # ── Case Study: 2002 National Drought ────────────────────────────
        "case_study_2002_drought": {
            "ingress_date":    "June 15, 2002",
            "ingress_chart":   "Sun ingress Gemini — SW Monsoon onset chart",
            "active_vectors":  {
                "rahu_position":     "Transiting Taurus (Rishabha) — Rank 1 Critical",
                "tajika_10th_house": "Saturn + Mercury in 10th of ingress chart (governance/authority afflicted)",
                "moisture_score":    "Low — Dhana Chakra watery nakshatra count below threshold",
            },
            "result":          "Severe pan-India drought; 29 of 35 meteorological subdivisions below normal.",
            "validation_note": (
                "Vindication of Hindu mundane astrology. Rahu-Taurus transit was "
                "the dominant macro trigger. Saturn in 10th of ingress chart "
                "confirmed government response would be reactive rather than "
                "preventive (drought relief delays)."
            ),
        },
    }
]


async def run() -> None:
    mongo_url = MONGO_URL
    import os
    if os.environ.get("MONGO_URL"):
        mongo_url = os.environ["MONGO_URL"]

    client = AsyncIOMotorClient(mongo_url)
    col    = client[DB_NAME]["mundane_engine_specs"]

    inserted = updated = 0
    for spec in SPECS:
        if DRY_RUN:
            print(f"  DRY  {spec['spec_id']}")
            continue
        result = await col.update_one(
            {"spec_id": spec["spec_id"]},
            {"$set":    spec},
            upsert=True,
        )
        if result.upserted_id:
            print(f"  INS  {spec['spec_id']}")
            inserted += 1
        else:
            print(f"  UPD  {spec['spec_id']}")
            updated += 1

    if DRY_RUN:
        print(f"\nDRY RUN complete — {len(SPECS)} spec(s) would be upserted")
    else:
        print(f"\nInserted {inserted} / Updated {updated} specs → {DB_NAME}.mundane_engine_specs")

    client.close()


if __name__ == "__main__":
    asyncio.run(run())
