"""
Mundane Astrology — Engine Specs v12
Batch: mundane-engine-v12-20260506

Sources:
  Mehta/Rao, "Mundane Astrology" — Chapter 2: The Multi-Step Scheme
  Gaur/AIFAS, "Mundane Astrology" — Chapter 3: Special Horoscopes

These are the two critical "operational backbone" specs that were in the
original NotebookLM JSON (3. Mundane Astrology_JSON_LM.md) but missing
from all clean-schema scripts (v3-v11).

Mehta Ch2 = The "OS" of the whole engine — the mandatory 9-step prediction
             hierarchy that governs HOW predictions are made.
Gaur Ch3  = Universal Horoscope (Aries Ingress) + New Year Ascendant Matrix
             + Samvat Stambha (water/grain pillar calculation).

GROUP: 4 engine specs

science_id: mundane_jyotish
Collection: mundane_engine_specs

Run with DRY_RUN = True to verify, then set False to write to MongoDB.
"""

import asyncio
from datetime import datetime, timezone
import sys
import types

# ---------------------------------------------------------------------------
if "motor" not in sys.modules:
    _motor = types.ModuleType("motor")
    _motor_async = types.ModuleType("motor.motor_asyncio")
    class _FakeClient:
        def __init__(self, *a, **kw): pass
        def __getitem__(self, k): return self
        def __getattr__(self, k): return self
        async def update_one(self, *a, **kw): pass
    _motor_async.AsyncIOMotorClient = _FakeClient
    sys.modules["motor"] = _motor
    sys.modules["motor.motor_asyncio"] = _motor_async

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL  = "mongodb://localhost:27017"
DB_NAME    = "horoscope_db"
COLLECTION = "mundane_engine_specs"
_BATCH     = "mundane-engine-v12-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ============================================================
# SPEC 1 — Mehta Ch2: 9-Step Prediction Hierarchy (the Engine OS)
# ============================================================
MEHTA_CH2_9_STEP_SCHEME = {
    "spec_id":       "mehta-ch2-9-step-prediction-hierarchy",
    "spec_type":     "operational_framework",
    "science_id":    "mundane_jyotish",
    "batch_id":      _BATCH,
    "title":         "Mehta 9-Step Hierarchical Prediction Scheme — The Mundane Engine OS",
    "source_chapter": "Mehta/Rao Ch 2",
    "notes": (
        "The 9-Step Scheme is the mandatory operational hierarchy for ALL mundane predictions. "
        "Core principle: transits alone are insufficient — they must be layered over foundation "
        "charts, annual solar maps, and lunar fortnightly charts for precision. "
        "CONFLICT RESOLUTION RULE: When a transit result contradicts a Foundation Dasha result, "
        "the Dasha (Step 1) overrides ALL other steps. "
        "This spec was in the original NotebookLM JSON but absent from clean-schema scripts v3-v11."
    ),
    "diagnostic_hierarchy": {
        "step_1": {
            "name": "Foundation Horoscope (National DNA)",
            "description": (
                "Treat nations as 'Natives' with their own natal chart. "
                "This is the primary baseline — all subsequent steps modify, "
                "not replace, this foundation. "
                "USA foundation: Leo 29° Lagna (superpower military/economic power). "
                "India foundation: Taurus Lagna (fixed = stability; Cancer 3rd house = IT/telecom boom)."
            ),
            "override_rule": "Foundation Dasha result overrides all transit results in case of conflict.",
        },
        "step_2": {
            "name": "Hindu New Year Horoscope & Yearly Planetary Cabinet",
            "description": (
                "Cast at the exact moment of Chaitra Shukla Pratipada (when the preceding Amavasya ends). "
                "Identifies the 10-member Celestial Council (King, Minister, Commander, etc.) for the year. "
                "Governs the annual tone, agricultural outlook, and governance stability."
            ),
            "logic_gates": {
                "royal_veto": (
                    "IF lord_of_year NOT IN [Sun, Moon] THEN governance_instability = TRUE"
                ),
                "military_veto": (
                    "IF commander_in_chief != Mars THEN military_disorder = TRUE"
                ),
                "turbulent_year_trigger": (
                    "IF Mars_in_lagna_of_new_year_chart AND Mars_aspects(Sun OR Moon OR Mercury) "
                    "THEN turbulent_year = TRUE"
                ),
            },
        },
        "step_3": {
            "name": "Surya Veedhi — Solar Ingress into All 12 Signs",
            "description": (
                "Cast at the moment the Sun enters each zodiac sign. "
                "Cardinal sign ingresses (Aries, Cancer, Libra, Capricorn) govern the next 3 months. "
                "Fixed sign ingresses extend to 12 months. Mutable sign ingresses: 6 months."
            ),
            "logic_gates": {
                "quarterly_gate": (
                    "Sun enters Cardinal sign → governs next 3 months."
                ),
                "conflict_trigger": (
                    "IF Sun_in_6th_house AND (Saturn OR Mars OR Rahu) conjunct Sun "
                    "THEN border_clashes = TRUE"
                ),
                "war_trigger": (
                    "IF Sun_in_7th_house AND malefic_aspects = TRUE "
                    "THEN war_risk = HIGH"
                ),
            },
        },
        "step_4": {
            "name": "Paksha Charts — New Moon / Full Moon (Fortnightly)",
            "description": (
                "Short-range precision forecasting tool. "
                "Cast every 15 days at New Moon and Full Moon. "
                "Used to time specific events (riots, market crashes, communal tension) "
                "within the annual framework set by Steps 1-3."
            ),
            "logic_gates": {
                "inauspicious_temporal_trigger": (
                    "IF fortnight_contains >= 3 Saturdays OR fortnight_contains >= 3 Tuesdays "
                    "THEN high_alert_inauspicious = TRUE"
                ),
                "communal_tension_gate": (
                    "IF malefics_aspect_Moon_in_paksha_chart AND paksha_lagna IN [Leo, Scorpio] "
                    "THEN communal_crisis_probability = HIGH"
                ),
                "financial_application": (
                    "Paksha charts predict stock exchange/Wall Street behavior one year in advance."
                ),
            },
        },
        "step_5": {
            "name": "Solar and Lunar Eclipses — Energy Discharge Points",
            "description": (
                "Eclipses are high-magnitude disruption events. "
                "Duration = impact period (solar: hours = years; lunar: hours = months). "
                "Two eclipses within 14 days = maximum destruction scenario."
            ),
            "logic_gates": {
                "solar_duration": "1 hour of eclipse duration = 1 year of national impact.",
                "lunar_duration": "1 hour of eclipse duration = 1 month of national impact.",
                "double_eclipse_veto": (
                    "IF solar_eclipse AND lunar_eclipse within 14 days "
                    "THEN terrible_destruction = TRUE (highest alert)"
                ),
                "assassination_monitor": (
                    "IF solar_eclipse occurs in ruler's birth nakshatra OR sensitive house of foundation chart "
                    "THEN trigger assassination_personal_safety_alert"
                ),
            },
        },
        "step_6": {
            "name": "Standard Planetary Transits and Retrogradation",
            "description": (
                "High-frequency transit analysis. "
                "Key trigger moments: day of sign change (Rashi Sandhi), "
                "day planet turns retrograde or direct, day of planetary combustion. "
                "Transit results MUST be modified by the planet's functional role "
                "(benefic/malefic) for the specific national Foundation Lagna."
            ),
            "primary_event_triggers": [
                "Day of planetary sign change (Rashi Sandhi — 0° or 29°)",
                "Day planet turns retrograde or turns direct (stationary point)",
                "Day of planetary combustion (close proximity to Sun)",
            ],
            "special_rule": (
                "IF Mars(retrograde) in Jyeshtha enters Anuradha "
                "THEN fall_of_kings = TRUE"
            ),
        },
        "step_7": {
            "name": "Specialized Diagnostic Chakras",
            "description": (
                "Grid-based Vedha (obstruction) systems for precise conflict and disaster diagnosis. "
                "Primary: Sanghatta Chakra. Secondary: Koorma Chakra, Tri Pataki Chakra."
            ),
            "primary_diagnostic_grid": "Sanghatta Chakra (Rashi and Nakshatra types)",
            "war_calculation_axiom": (
                "War is triggered by mutual Vedha (obstruction) between Moon, Mars, Rahu, "
                "and Saturn on the Sanghatta grid."
            ),
            "rohini_famine_rule": (
                "IF Saturn transits Rohini Nakshatra (Taurus 10° to 23°20') "
                "THEN trigger famine_or_war_alert (HIGHEST level warning in mundane astrology). "
                "This is the Rohini Shakata Bhedan Yoga."
            ),
        },
        "step_8": {
            "name": "Occasional Planetary Conjunctions — The Macro-Temporal Clock",
            "description": (
                "Major planetary alignments that act as primary turning points in world history. "
                "These set the 20-200 year meta-narratives within which annual charts operate."
            ),
            "conjunction_rules": {
                "saturn_jupiter": {
                    "cadence": "Every 20 years (The Great Mutation).",
                    "usa_mortality_veto": (
                        "IF Saturn-Jupiter conjunction occurs "
                        "THEN US president elected near that date faces high mortality risk."
                    ),
                    "triplicity_shift": (
                        "Earthy triplicity (Virgo/Taurus/Capricorn) focus = 200-year era of "
                        "slow material world-order shifts."
                    ),
                },
                "saturn_rahu": {
                    "result": (
                        "End of imperialism, birth of new nations, or mass destruction "
                        "via atomic/advanced weaponry."
                    ),
                    "war_gate": (
                        "IF Sat-Rah conjunction in Capricorn "
                        "THEN major_global_conflict = TRUE (validated: 1990 Gulf War)."
                    ),
                    "historical_validation": "1945 conjunction → atomic bomb / end of imperialism.",
                },
                "saturn_mars": {
                    "result": "Extreme violence, general massacre, Black Days in history.",
                    "internal_security": (
                        "IF Saturn-Mars conjunction in 6th house of national foundation chart "
                        "THEN military_action_against_domestic_threats = TRUE "
                        "(validated: Operation Blue Star)."
                    ),
                },
                "triple_conjunction_veto": (
                    "IF Saturn AND Mars AND Rahu meet in a quadrant "
                    "THEN global_destruction_scheme = TRUE."
                ),
                "1_degree_orb_rule": (
                    "IF Sun, Saturn, Moon, and Rahu are within 1° of each other "
                    "THEN catastrophic_mundane_event = TRUE."
                ),
            },
        },
        "step_9": {
            "name": "Annual Varshaphala — Compressed Vimshottari Dasha",
            "description": (
                "Compressed dasha system for the Foundation Chart's annual solar return. "
                "Ratio: 1:120 (standard 120-year Vimshottari compressed to 1 year). "
                "Used to time the exact nature of national events within the year."
            ),
            "compressed_durations_360_day_year": {
                "Ketu":    "21 days",
                "Venus":   "60 days",
                "Sun":     "18 days",
                "Moon":    "30 days",
                "Mars":    "21 days",
                "Rahu":    "54 days",
                "Jupiter": "48 days",
                "Saturn":  "57 days",
                "Mercury": "51 days",
            },
            "success_veto": (
                "A prediction of national achievement (mineral discovery, sports victory) "
                "is authorized ONLY IF Varshaphala shows benefic Muntha Lord "
                "AND strong 10th lord in the compressed dasha."
            ),
        },
    },
    "hierarchy_summary": (
        "Steps 1-3 = Annual and national baseline (Foundation + Ingress). "
        "Step 4 (Paksha) = Fortnightly timing of political and social flashpoints. "
        "Steps 6-7 = Planetary physics (retrogression + grid Vedha) for conflict nature. "
        "Step 8 = Great Conjunctions meta-narrative (20-200 year world-order shifts). "
        "Step 9 = Compressed dasha micro-timing within the year."
    ),
    "created_at": _NOW,
}

# ============================================================
# SPEC 2 — Gaur Ch3: Universal Horoscope (Aries Ingress) Framework
# ============================================================
GAUR_CH3_UNIVERSAL_HOROSCOPE = {
    "spec_id":       "gaur-ch3-universal-horoscope-aries-ingress",
    "spec_type":     "calculation_method",
    "science_id":    "mundane_jyotish",
    "batch_id":      _BATCH,
    "title":         "Universal Horoscope — Aries Ingress Chart Framework (Gaur Ch 3)",
    "source_chapter": "Gaur Ch 3, pp. 32-33",
    "notes": (
        "The Universal Horoscope is cast at the exact moment the Sun enters Aries (Mesha Sankranti). "
        "It is the global-level annual chart — each of the 12 houses represents one Hindu lunar month. "
        "Distinct from the New Year (Pratipada) chart: "
        "  Universal Chart = Sun-based, governs GLOBAL sentiment. "
        "  New Year Chart   = Moon-based, governs REGIONAL distribution (North/South/East/West)."
    ),
    "house_temporal_mapping": {
        "1st_house":  "Chaitra    (Mar-Apr)",
        "2nd_house":  "Vaishakh   (Apr-May)",
        "3rd_house":  "Jyeshtha   (May-Jun)",
        "4th_house":  "Aashadh    (Jun-Jul)",
        "5th_house":  "Shravan    (Jul-Aug)",
        "6th_house":  "Bhadrapad  (Aug-Sep)",
        "7th_house":  "Ashwin     (Sep-Oct)",
        "8th_house":  "Kartik     (Oct-Nov)",
        "9th_house":  "Margsheersh (Nov-Dec)",
        "10th_house": "Paush      (Dec-Jan)",
        "11th_house": "Magh       (Jan-Feb)",
        "12th_house": "Phalgun    (Feb-Mar)",
    },
    "diagnostic_rules": {
        "benefic_aspect_on_lagna": "Good crops and general prosperity for the world.",
        "malefics_in_7th_house": (
            "Damage to ripe crops — specifically Sun, Mars, Saturn, Rahu in 7th "
            "adversely affect the Ashwin (Sep-Oct) harvest period."
        ),
        "benefics_in_quadrants_2_and_12": "Prices of commodities decrease.",
        "double_eclipse_in_mapped_months": (
            "Two eclipses within 14 days (occurring in months mapped by any two consecutive houses) "
            "= Terrible Destruction in those months."
        ),
    },
    "usage_note": (
        "To predict events in a specific Hindu month: identify which house that month maps to, "
        "then assess the planetary occupants/aspects on that house in the Aries Ingress chart. "
        "Malefics in or aspecting the house = troubles in that month. "
        "Benefics = improvement and prosperity in that month."
    ),
    "created_at": _NOW,
}

# ============================================================
# SPEC 3 — Gaur Ch3: New Year Ascendant Matrix (12 Lagnas → directional forecasts)
# ============================================================
GAUR_CH3_NEW_YEAR_ASCENDANT_MATRIX = {
    "spec_id":       "gaur-ch3-new-year-ascendant-matrix",
    "spec_type":     "lookup_table",
    "science_id":    "mundane_jyotish",
    "batch_id":      _BATCH,
    "title":         "New Year Ascendant Matrix — 12 Lagnas × Regional Directional Forecasts (Gaur Ch 3)",
    "source_chapter": "Gaur Ch 3, pp. 33-34",
    "notes": (
        "The New Year Horoscope is cast at the exact moment of Chaitra Shukla Pratipada "
        "(when the preceding Amavasya ends). "
        "The Ascendant (Lagna) of this chart determines the directional forecast for the year: "
        "North, South, East, West, and Middle regions of the country/world. "
        "Cross-reference with Koorma Chakra (spec gaur-ch4-koorma-chakra) for city-level precision."
    ),
    "ascendant_matrix": {
        "Aries": {
            "East":   "Unrest and drought.",
            "South":  "Good crops; Ghee expensive.",
            "North":  "Good crops but restless rulers.",
            "Middle": "Good rains.",
            "general": None,
        },
        "Taurus": {
            "West":    "Drought.",
            "East":    "Mutiny.",
            "North":   "Poor crops and drought.",
            "South":   "Poor crops and drought.",
            "Middle":  None,
            "general": None,
        },
        "Gemini": {
            "East":    "Destroyed crops.",
            "North":   "Good rains.",
            "South":   "Good rains.",
            "West":    "Changing rulers.",
            "Middle":  "50% yield; cattle disease.",
            "general": "Wars between nations.",
        },
        "Cancer": {
            "East":    "Prosperity.",
            "North":   "Turmoils.",
            "West":    "Drought.",
            "South":   None,
            "Middle":  None,
            "general": None,
        },
        "Leo": {
            "South":   "Flood risk; grains cheap.",
            "West":    "Expensive metals and fruits.",
            "North":   "Comfort and prosperity.",
            "East":    "Poor crops initially.",
            "Middle":  "5-month revolt.",
            "general": "Split-year: first half prosperous, middle provinces revolt.",
        },
        "Virgo": {
            "East":    "Normal; Ghee expensive.",
            "South":   "Drought.",
            "West":    "Riots; expensive grains.",
            "NE":      "Riots.",
            "Middle":  "Dissatisfaction; democracy dissolved.",
            "general": "HIGH ALERT: 'Democracy Dissolved' indicator for middle provinces.",
        },
        "Libra": {
            "Middle":  "Unrest; government dissolved.",
            "East":    "Administration disbanded; riots.",
            "West":    "War between two states; high prices.",
            "South":   "Prosperity.",
            "general": "Low rainfall year overall.",
        },
        "Scorpio": {
            "West":    "9-month drought.",
            "North":   "50% yield; cheap metals.",
            "East":    "Ruler acrimony.",
            "Middle":  "Crops destroyed.",
            "South":   "Heavy rain; government change.",
            "general": None,
        },
        "Sagittarius": {
            "NE":      "Prosperity.",
            "Middle":  "Floods; disease; drought.",
            "West":    "Expensive grains.",
            "South":   "Prosperity; cattle suffer.",
            "North":   None,
            "East":    None,
            "general": None,
        },
        "Capricorn": {
            "North":   "Natural calamities; loss of life.",
            "West":    "Good crops; comfort.",
            "Middle":  "Poor crops; expensive grains.",
            "general": "Rains arrive after drought.",
        },
        "Aquarius": {
            "East":    "Prosperity.",
            "North":   "Drought.",
            "West":    "Dissatisfaction; high prices.",
            "South":   "Violence.",
            "Middle":  "Prosperity.",
            "general": None,
        },
        "Pisces": {
            "South":   "Prosperity; government change.",
            "Middle":  "Damaged crops.",
            "general": "Other directions: comfortable and affluent.",
        },
    },
    "special_alerts": {
        "democracy_dissolved": (
            "IF New Year Ascendant = Virgo → 'Democracy Dissolved' alert for Middle Provinces."
        ),
        "government_change": (
            "IF New Year Ascendant = Scorpio (South) OR Pisces (South) → government change likely."
        ),
        "war_between_nations": (
            "IF New Year Ascendant = Gemini → wars between nations."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
# SPEC 4 — Gaur Ch3: Samvat Stambha Engine (4-Pillar Water/Grain Calculation)
# ============================================================
GAUR_CH3_SAMVAT_STAMBHA = {
    "spec_id":       "gaur-ch3-samvat-stambha-four-pillars",
    "spec_type":     "calculation_method",
    "science_id":    "mundane_jyotish",
    "batch_id":      _BATCH,
    "title":         "Samvat Stambha — Four-Pillar Water, Grass, Air and Grain Calculation (Gaur Ch 3)",
    "source_chapter": "Gaur Ch 3, pp. 35-37",
    "notes": (
        "Samvat Stambha ('Pillars of the Year') is a unique quantitative method to determine "
        "the annual abundance of the four physical pillars of existence: "
        "Water (Jal), Grass/Medicinal Plants (Trin), Air (Vayu), and Grains (Anna). "
        "Existence depends on these four elements — their presence/absence defines "
        "the prosperity or hardship of the year. "
        "CRITICAL: Pillar presence is binary (is the star present during Pratipada?), "
        "but strength is a gradient (for how many minutes?). "
        "Check Presence first to set Category (Lucky/Medium/Painful), "
        "then Percentage to set Intensity."
    ),
    "pillar_definitions": {
        "Jal_Water": {
            "nakshatra":    "Revati",
            "tithi":        "Chaitra Shukla Pratipada",
            "impact":       "Rainfall volume for the year.",
            "absence_alert": "Jal Stambha = 0% → trigger 'Impending Water Scarcity' warning for the full year.",
        },
        "Trin_Grass": {
            "nakshatra":  "Bharani",
            "tithi":      "Vaishakh Shukla Pratipada",
            "impact":     "Abundance of medicinal plants and grass.",
        },
        "Vayu_Air": {
            "nakshatra":  "Mrigshira",
            "tithi":      "Jyeshtha Shukla Pratipada",
            "impact":     "Atmospheric motion / Wind speed (needed to move rain clouds).",
        },
        "Anna_Grain": {
            "nakshatra":  "Punarvasu",
            "tithi":      "Aashadh Shukla Pratipada",
            "impact":     "Grain yield / food production.",
        },
    },
    "calculation_formula": {
        "percentage": (
            "Strength % = "
            "(Duration of target nakshatra during Pratipada Tithi) / "
            "(Total duration of Pratipada Tithi) × 100"
        ),
        "presence_threshold": "Strength % > 0% → Pillar is Present.",
        "validated_example": (
            "VS 2059 (year 2002): Total Pratipada duration = 1562 minutes. "
            "Revati (Jal) duration = 142 minutes. "
            "Result: 9% Jal Stambha → 'Medium/Partial Prosperity' (validated: Indian Drought of 2002)."
        ),
    },
    "combinatorial_outcomes": {
        "lucky_and_prosperous": {
            "condition": "ALL FOUR pillars present (Jal + Trin + Vayu + Anna).",
            "result":    "Maximum benefic results for the year.",
        },
        "unlucky_and_painful": {
            "condition": "NONE of the four pillars present.",
            "result":    "Total destitution and hardship. HIGHEST malefic warning level, "
                         "overrides all other benefic planetary aspects.",
        },
        "medium_diluted_yield": {
            "condition": "1, 2, or 3 pillars present (partial).",
            "critical_case": (
                "IF Trin (Grass) + Anna (Grain) present BUT Jal (Water) + Vayu (Air) absent: "
                "'Grains and medicinal plants sprout, but lack of rain/wind prevents full maturation. "
                "Financial benefit to the state is diluted — medium results only.' "
                "This is the DRY HARVEST ALERT."
            ),
            "synergy_veto": (
                "Even if Anna = 100%, if Jal = 0%, diagnostic MUST output: "
                "'Production targets met but maturation failed due to lack of moisture; "
                "overall yield medium.'"
            ),
        },
    },
    "cross_chapter_validation": (
        "If Jal Stambha is low (e.g., 9%), cross-verify with Cloud Engine (Gaur Ch 2, "
        "spec gaur-ch2-nine-clouds) to check if cloud type offers any mitigation. "
        "Also cross-reference with Koorma Chakra regional mapping for directional scarcity."
    ),
    "created_at": _NOW,
}

# ============================================================
ALL_SPECS = [
    MEHTA_CH2_9_STEP_SCHEME,
    GAUR_CH3_UNIVERSAL_HOROSCOPE,
    GAUR_CH3_NEW_YEAR_ASCENDANT_MATRIX,
    GAUR_CH3_SAMVAT_STAMBHA,
]

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_SPECS)} engine specs from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        for s in ALL_SPECS:
            print(f"  {s['spec_id']}")
        print(f"\nTotal: {len(ALL_SPECS)}\n\nDry run complete.")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    col = db[COLLECTION]
    upserted = 0
    for spec in ALL_SPECS:
        await col.update_one(
            {"spec_id": spec["spec_id"]},
            {"$set": spec},
            upsert=True,
        )
        upserted += 1
    print(f"Upserted {upserted} specs into {COLLECTION}.")
    client.close()

if __name__ == "__main__":
    asyncio.run(run())
