"""
ingest_mundane_interpretation_v2.py
=====================================
Batch: mundane-interp-v2-20260505
Collection: interpretation_rules
Science: mundane_jyotish

NEW RULES (21):

  Group L — Gopal Ch 2 Heuristic Filters (6 rules)
    mundane-gopal-ch2-10th-lord-triage
    mundane-gopal-ch2-india-lagna-filter
    mundane-gopal-ch2-governance-longevity
    mundane-gopal-ch2-celebrity-authentication
    mundane-gopal-ch2-election-comparative-audit
    mundane-gopal-ch2-saturn-transit-regime-cycle

  Group M — Mehta Ch 10 Macro-Conjunctions (8 rules)
    mundane-mehta-ch10-sat-jup-20yr-mortality
    mundane-mehta-ch10-sat-jup-great-mutation
    mundane-mehta-ch10-sat-jup-aries-1-degree
    mundane-mehta-ch10-sat-rahu-empire-end
    mundane-mehta-ch10-sat-rahu-capricorn-gate
    mundane-mehta-ch10-sat-mar-massacre
    mundane-mehta-ch10-sat-mar-watery-tsunami
    mundane-mehta-ch10-mars-ketu-terror-gate

  Group N — Mehta Ch 6 Diagnostic Rules (4 rules)
    mundane-mehta-ch6-sun-6th-border-war
    mundane-mehta-ch6-eclipse-10th-overthrow
    mundane-mehta-ch6-5th-malefic-assassination
    mundane-mehta-ch6-sat-10th-democracy

  Group O — Raphael Ch 3 Diagnostic Rules (3 rules)
    mundane-raphael-ch3-angular-multiplier
    mundane-raphael-ch3-intellectual-triad
    mundane-raphael-ch3-opposition-4th-trigger

Upsert key: rule_id
All rules: approval_status=pending_review, checkable=False
"""

import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.environ.get("DB_NAME",   "horoscope_db")
BATCH_ID  = "mundane-interp-v2-20260505"
DRY_RUN   = True   # set False to write to MongoDB

# ─────────────────────────────────────────────────────────────────────────────
# GROUP L — GOPALAKRISHNAN CH 2: HEURISTIC FILTERS (6 rules)
# ─────────────────────────────────────────────────────────────────────────────
GROUP_L = [
    {
        "rule_id": "mundane-gopal-ch2-10th-lord-triage",
        "sub_type": "chart_authentication",
        "title": "Gopal Ch 2 — 10th Lord Triage (Chart Authenticity Veto)",
        "description": (
            "Before analyzing any high-profile mundane chart, the 10th lord must be strong "
            "from at least two of: Lagna, Chandra Lagna, or Karkamsha Lagna. If the 10th house "
            "is vacant and unaspected, flag the chart as 'Potentially Inauthentic'. "
            "E.g., Advani chart with weak 10th lord in 12th → reject as likely incorrect birth data."
        ),
        "condition": {
            "check": "10th lord strength from Lagna / Chandra Lagna / Karkamsha Lagna",
            "pass_threshold": "Strong from at least 2 of 3",
            "fail_output": "Chart flagged as Likely Inauthentic — verify birth data before analysis"
        },
        "source_ref": "Gopalakrishnan Ch 2 — How to Become a Very Good Mundane Astrologer",
        "synthesis_sources": [{"book": "gopal_modern", "chapter": "Ch 2", "label": "Heuristic Logic Engine"}]
    },
    {
        "rule_id": "mundane-gopal-ch2-india-lagna-filter",
        "sub_type": "india_leadership_filter",
        "title": "Gopal Ch 2 — India Alignment Lagna Filter for National Leaders",
        "description": (
            "A leader's Lagna must be harmonious with India's Independence chart (Taurus Lagna). "
            "Tier 1 success lagnas: Cancer, Taurus. "
            "Tier 2 success lagnas: Scorpio, Leo. "
            "Veto lagnas (6/8/12 from India's Taurus): Libra (6th), Sagittarius (8th), Aries (12th). "
            "A candidate with a veto lagna is diagnosed with significantly lower probability of "
            "reaching sustained national power in India."
        ),
        "condition": {
            "tier_1_success": ["Cancer", "Taurus"],
            "tier_2_success": ["Scorpio", "Leo"],
            "veto_lagnas": ["Libra", "Sagittarius", "Aries"],
            "veto_logic": "These are 6th, 8th, and 12th houses relative to India's Taurus Independence Lagna"
        },
        "source_ref": "Gopalakrishnan Ch 2 — Indian Political Lagna Filter",
        "synthesis_sources": [{"book": "gopal_modern", "chapter": "Ch 2", "label": "Heuristic Logic Engine"}]
    },
    {
        "rule_id": "mundane-gopal-ch2-governance-longevity",
        "sub_type": "governance_longevity_math",
        "title": "Gopal Ch 2 — Saturnine Longevity Rule for Indian PM",
        "description": (
            "Saturn is the 10th lord of India (Taurus Lagna). Leaders who are unmarried or widowed "
            "can hold the Indian PM seat for long durations because Saturn (asceticism, solitude) "
            "is naturally empowered. Leaders with a spouse face shorter tenures. "
            "Empirical successes: Nehru (widower), Indira Gandhi (widow), Vajpayee (bachelor). "
            "Empirical short-tenures: Rajiv Gandhi, Lal Bahadur Shastri, V.P. Singh."
        ),
        "condition": {
            "trigger": "Saturn as 10th lord for India (Taurus Lagna chart)",
            "long_tenure_indicator": "Leader is unmarried or widowed",
            "short_tenure_indicator": "Leader has a living spouse",
            "historical_validation": {
                "long_tenure": ["Nehru", "Indira Gandhi", "Vajpayee"],
                "short_tenure": ["Rajiv Gandhi", "Lal Bahadur Shastri", "V.P. Singh"]
            }
        },
        "source_ref": "Gopalakrishnan Ch 2 — Saturnine Power Gate",
        "synthesis_sources": [{"book": "gopal_modern", "chapter": "Ch 2", "label": "Heuristic Logic Engine"}]
    },
    {
        "rule_id": "mundane-gopal-ch2-celebrity-authentication",
        "sub_type": "chart_authentication",
        "title": "Gopal Ch 2 — Celebrity / Leader Chart Authentication Rule",
        "description": (
            "For any celebrity or national leader, the 10th lord must be strong from at least "
            "two of: Lagna, Chandra Lagna, or Karkamsha Lagna. Additionally, the 10th house "
            "must be occupied or aspected. A vacant, unaspected 10th house flags the chart as "
            "potentially inauthentic regardless of other factors. Apply this as the FIRST gate "
            "before any deep analysis."
        ),
        "condition": {
            "gate_1": "10th lord must be strong from min 2 of 3 reference points",
            "gate_2": "10th house must be occupied or aspected by at least one planet",
            "failure_output": "Chart Rejected: Potentially Inauthentic Birth Data"
        },
        "source_ref": "Gopalakrishnan Ch 2 — 10th House Verification",
        "synthesis_sources": [{"book": "gopal_modern", "chapter": "Ch 2", "label": "Heuristic Logic Engine"}]
    },
    {
        "rule_id": "mundane-gopal-ch2-election-comparative-audit",
        "sub_type": "election_winner_logic",
        "title": "Gopal Ch 2 — Election Winner Comparative Strength Audit",
        "description": (
            "To predict between two candidates: compare the strength of the 10th lord from "
            "Lagna, Moon, and Karkamsha for both. Identify who is running a Raja Yoga period "
            "(Kendra/Trikona lords conjunct or in exchange). Veto any candidate running a "
            "6th, 8th, or 12th lord period (Dusthana dasha = near-certain defeat). "
            "Also apply the India Alignment Filter: Libra/Sagittarius/Aries lagna candidates "
            "face structural disadvantage in Indian elections."
        ),
        "condition": {
            "step_1": "Compare 10th lord strength from Lagna + Moon + Karkamsha for both candidates",
            "step_2": "Identify who is in a Raja Yoga period (Kendra/Trikona lord dasha)",
            "step_3": "Veto candidates in a 6th/8th/12th lord dasha — near-certain defeat",
            "step_4": "Apply India Alignment Lagna Filter for national elections"
        },
        "source_ref": "Gopalakrishnan Ch 2 — Election Winner Logic",
        "synthesis_sources": [{"book": "gopal_modern", "chapter": "Ch 2", "label": "Heuristic Logic Engine"}]
    },
    {
        "rule_id": "mundane-gopal-ch2-saturn-transit-regime-cycle",
        "sub_type": "governance_longevity_math",
        "title": "Gopal Ch 2 — Saturn Transit Regime Cycle (4th/8th/12th House Trigger)",
        "description": (
            "Saturn's transit through the 4th, 8th, and 12th houses of a leader's natal chart "
            "triggers the fall of their political regime regardless of administrative success. "
            "Case study: Chandra Babu Naidu — Saturn transiting through 4th/8th/12th houses "
            "caused his political downfall despite technological achievements. "
            "This is the Law of Karma in Office: Saturn's 7.5-year transit cycle (Sade Sati "
            "equivalent for public figures) is the primary timing mechanism for regime change."
        ),
        "condition": {
            "trigger": "Saturn transiting 4th, 8th, or 12th house from leader's natal Moon",
            "result": "High probability of regime change, electoral defeat, or loss of power",
            "veto": "Even technological or administrative success cannot override this Saturn cycle",
            "historical_case": "Chandra Babu Naidu's fall despite IT achievements"
        },
        "source_ref": "Gopalakrishnan Ch 2 — Law of Karma in Office",
        "synthesis_sources": [{"book": "gopal_modern", "chapter": "Ch 2", "label": "Heuristic Logic Engine"}]
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# GROUP M — MEHTA CH 10: MACRO-CONJUNCTIONS (8 rules)
# ─────────────────────────────────────────────────────────────────────────────
GROUP_M = [
    {
        "rule_id": "mundane-mehta-ch10-sat-jup-20yr-mortality",
        "sub_type": "macro_conjunction",
        "title": "Mehta Ch 10 — Saturn-Jupiter 20-Year Conjunction: US Presidential Mortality Gate",
        "description": (
            "The Saturn-Jupiter conjunction occurs every 20 years and marks a turning point "
            "in history where an old order dies and a new order takes over. "
            "Specific US Presidential mortality veto: every US president elected in a "
            "Saturn-Jupiter conjunction year faces a HIGH RISK of dying in office "
            "or not completing their full term. "
            "Examples: Lincoln (1860 cycle), Harding (1920), FDR (1940), JFK (1960)."
        ),
        "condition": {
            "conjunction_type": "Saturn-Jupiter",
            "cadence": "Every 20 years",
            "us_president_gate": "IF (Sat-Jup Conjunction year) AND (US President elected) THEN Mortality_Risk = CRITICAL",
            "general_result": "Major turning point: old political/economic order ends, new order begins",
            "1_degree_orb_rule": "Apply 1-degree orb for maximum impact weighting"
        },
        "ignition_rule": "Conjunction sets the theme; Mars transiting the conjunction degree materializes the actual event.",
        "source_ref": "Mehta/Rao Ch 10 — Conjunction-Opposition Logic",
        "synthesis_sources": [{"book": "mehta_rao", "chapter": "Ch 10", "label": "Macro-Temporal Clock"}]
    },
    {
        "rule_id": "mundane-mehta-ch10-sat-jup-great-mutation",
        "sub_type": "macro_conjunction",
        "title": "Mehta Ch 10 — Saturn-Jupiter Great Mutation: Triplicity Shift (200-Year Era)",
        "description": (
            "The Great Mutation is the first Saturn-Jupiter conjunction in a new triplicity "
            "(e.g., transition from Earth to Air triplicity signs). This event sets the "
            "dominant global theme for the next 200 years. "
            "Current context: Earthy triplicity (Virgo/Taurus/Capricorn) = century of "
            "material/economic restructuring. "
            "Triplicity results: Earthy = material growth, shifts in world financial dominance; "
            "Fiery = wars of ideology and rapid territorial expansion."
        ),
        "condition": {
            "trigger": "First Saturn-Jupiter conjunction in a new triplicity",
            "impact_duration": "200 years",
            "triplicity_results": {
                "earthy": "Material growth, shifts in world financial dominance",
                "fiery": "Wars of ideology and rapid territorial expansion",
                "airy": "Communication revolutions, intellectual/scientific paradigm shifts",
                "watery": "Mass migrations, religious upheavals, emotional collective shifts"
            }
        },
        "source_ref": "Mehta/Rao Ch 10 — Great Mutation / Triplicity Awareness",
        "synthesis_sources": [{"book": "mehta_rao", "chapter": "Ch 10", "label": "Macro-Temporal Clock"}]
    },
    {
        "rule_id": "mundane-mehta-ch10-sat-jup-aries-1-degree",
        "sub_type": "macro_conjunction",
        "title": "Mehta Ch 10 — Saturn-Jupiter at Aries 1°: Century-Level Paradigm Shift",
        "description": (
            "Conjunctions of heavy planets commencing in the FIRST DEGREE OF ARIES are the "
            "most important in all of mundane astrology. This configuration has occurred only "
            "eight times in recorded history and always marks a century-level paradigm shift. "
            "When the engine identifies a heavy planet conjunction at 0°-1° Aries, it must "
            "trigger a 'Century-Level Paradigm Shift' alert — the highest-level predictive "
            "signal in the entire mundane engine."
        ),
        "condition": {
            "trigger": "Any heavy planet conjunction (Saturn-Jupiter, Saturn-Rahu, Saturn-Mars) at 0°-1° Aries",
            "historical_frequency": "Only 8 occurrences in recorded history",
            "output": "Century-Level Paradigm Shift — highest priority predictive signal",
            "priority": "Overrides all standard dasha/transit results"
        },
        "source_ref": "Mehta/Rao Ch 10 — Aries 1-Degree Rule (Historical Priority Gate)",
        "synthesis_sources": [{"book": "mehta_rao", "chapter": "Ch 10", "label": "Macro-Temporal Clock"}]
    },
    {
        "rule_id": "mundane-mehta-ch10-sat-rahu-empire-end",
        "sub_type": "macro_conjunction",
        "title": "Mehta Ch 10 — Saturn-Rahu Conjunction: End of Imperialism / Birth of New Nations",
        "description": (
            "Saturn-Rahu conjunctions mark the end of imperialism, the collapse of colonial systems, "
            "and the birth of new sovereign nation-states. They also coincide with the dawn of "
            "military technology paradigm shifts. "
            "Key example: 1945 Saturn-Rahu conjunction in Gemini → Hiroshima/Nagasaki, "
            "birth of the atomic age, and the dissolution of European colonial empires. "
            "When in Gemini (sign of air/technology/USA): flag Nuclear Escalation or "
            "Global Shift in Military Technology."
        ),
        "condition": {
            "conjunction_type": "Saturn-Rahu",
            "primary_result": "End of imperialism, collapse of colonialism, birth of new nations",
            "technology_gate": "Saturn-Rahu in Gemini = Global Shift in Military Technology / Nuclear Escalation",
            "national_humiliation_gate": "IF (Sat-Rahu in 8th or 12th of a nation's chart) THEN National Setback / Loss of Prestige"
        },
        "synthesis_sources": [{"book": "mehta_rao", "chapter": "Ch 10", "label": "Macro-Temporal Clock"}]
    },
    {
        "rule_id": "mundane-mehta-ch10-sat-rahu-capricorn-gate",
        "sub_type": "macro_conjunction",
        "title": "Mehta Ch 10 — Saturn-Rahu in Capricorn: Major Regime Change / Gulf War Gate",
        "description": (
            "Saturn-Rahu conjunction specifically in Capricorn triggers major regime change "
            "in the Middle East and collapse of existing power structures. "
            "Historical validation: 1991 Gulf War — Sun, Saturn, Moon, Rahu all within 1 degree "
            "in Capricorn → Operation Desert Storm and the redrawing of Middle Eastern power. "
            "The 1-degree cluster rule: if 4+ planets within 1 degree of each other, the "
            "diagnostic must return 'Catastrophic Mundane Event' — weight tripled."
        ),
        "condition": {
            "conjunction_type": "Saturn-Rahu",
            "sign": "Capricorn",
            "result": "Major Regime Change / Collapse of Middle Eastern power structure",
            "multi_planet_cluster": "IF 4+ planets within 1-degree in Capricorn THEN Catastrophic Mundane Event (weight ×3)",
            "historical_case": "1991 Gulf War — Sun/Saturn/Moon/Rahu within 1° in Capricorn"
        },
        "synthesis_sources": [{"book": "mehta_rao", "chapter": "Ch 10", "label": "Macro-Temporal Clock"}]
    },
    {
        "rule_id": "mundane-mehta-ch10-sat-mar-massacre",
        "sub_type": "macro_conjunction",
        "title": "Mehta Ch 10 — Saturn-Mars Conjunction: Black Day / Internal Military Operation",
        "description": (
            "Saturn-Mars conjunction is the most inauspicious alignment in mundane astrology — "
            "the 'Black Day' configuration feared by rulers. It historically triggers mass massacres, "
            "internal military operations, and unprecedented carnage. "
            "Key gates: "
            "(1) Saturn-Mars in 6th house of a national chart → Internal Military Action certain "
            "(e.g., Operation Blue Star 1984, India's 6th house). "
            "(2) Saturn-Mars in a Dual Sign (Gemini/Virgo/Sagittarius/Pisces) → General Massacre "
            "(e.g., Nadir Shah 1739). "
            "Mars acts as the 'Minute Hand' that discharges the energy set by Saturn."
        ),
        "condition": {
            "conjunction_type": "Saturn-Mars",
            "diagnostic_status": "Highly Inauspicious / Deadly",
            "6th_house_gate": "IF (Sat-Mar in 6th house of national chart) THEN Internal Military Action = CERTAIN",
            "dual_sign_gate": "IF (Sat-Mar in Dual Sign) THEN General Massacre = HIGH RISK",
            "historical_cases": [
                {"event": "Nadir Shah Massacre 1739", "geometry": "Saturn-Mars in dual sign, 6th from India Capricorn"},
                {"event": "Operation Blue Star 1984", "geometry": "Saturn-Mars conjunction in India's 6th house"}
            ]
        },
        "synthesis_sources": [{"book": "mehta_rao", "chapter": "Ch 10", "label": "Macro-Temporal Clock"}]
    },
    {
        "rule_id": "mundane-mehta-ch10-sat-mar-watery-tsunami",
        "sub_type": "macro_conjunction",
        "title": "Mehta Ch 10 — Saturn-Mars in Watery Sign: Maritime Disaster / Tsunami Gate",
        "description": (
            "Saturn-Mars conjunction or mutual kendra aspect in Watery Signs (Cancer, Scorpio, Pisces) "
            "triggers maritime disasters, major floods, and tsunami events. "
            "The materialization trigger: Mars afflicting the Moon in a watery sign while "
            "Saturn-Mars are in Graha Yuddha (planetary war). "
            "Historical validation: 2004 Asian Tsunami — Saturn-Mars in Kendra configuration "
            "with watery sign involvement."
        ),
        "condition": {
            "conjunction_type": "Saturn-Mars",
            "sign_requirement": "Watery sign (Cancer, Scorpio, or Pisces)",
            "materialization_trigger": "Mars afflicting Moon in watery sign while Saturn-Mars in Graha Yuddha",
            "result": "Maritime Disaster or Flood-based Tragedy — CRITICAL alert",
            "historical_case": "2004 Asian Tsunami — Saturn-Mars kendra configuration in watery signs"
        },
        "synthesis_sources": [{"book": "mehta_rao", "chapter": "Ch 10", "label": "Macro-Temporal Clock"}]
    },
    {
        "rule_id": "mundane-mehta-ch10-mars-ketu-terror-gate",
        "sub_type": "macro_conjunction",
        "title": "Mehta Ch 10 — Mars-Ketu in Fiery Sign: High-Intensity Terror / Suicide Attack Gate",
        "description": (
            "Mars conjunct Ketu in a Fiery Sign or war-like nakshatra (especially Moola) triggers "
            "high-intensity terrorist events, suicide attacks, and coordinated mass casualties. "
            "Ketu acts like Mars but operates through secrecy; Rahu acts like Saturn with violence. "
            "Geometry for extreme terror: Mars and Ketu within 1-degree orb in Fiery Sign, "
            "opposing a major planet in a national native sign. "
            "Historical anchor: 9/11 WTC — Mars-Ketu in Sagittarius (Moola nakshatra) opposing "
            "Jupiter in Gemini (USA native sign). "
            "Mars-Rahu conjunction in fiery sign = equally dangerous (Rahu amplifies aggression)."
        ),
        "condition": {
            "conjunction_type": "Mars-Ketu (or Mars-Rahu)",
            "sign_requirement": "Fiery sign (Aries, Leo, Sagittarius) — especially Moola nakshatra",
            "1_degree_orb": "Required for maximum impact",
            "opposition_amplifier": "Opposition to major planet in national native sign amplifies 10×",
            "result": "Extreme Terrorist Event / Suicide Attack — CRITICAL alert",
            "historical_anchor": "9/11 WTC (2001) — Mars-Ketu in Sagittarius/Moola opposing Jupiter in Gemini"
        },
        "synthesis_sources": [{"book": "mehta_rao", "chapter": "Ch 10", "label": "Macro-Temporal Clock"}]
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# GROUP N — MEHTA CH 6: HOUSE DIAGNOSTIC RULES (4 rules)
# ─────────────────────────────────────────────────────────────────────────────
GROUP_N = [
    {
        "rule_id": "mundane-mehta-ch6-sun-6th-border-war",
        "sub_type": "hazard_border_conflict",
        "title": "Mehta Ch 6 — Sun in 6th House with Malefic: Border Clash Alert",
        "description": (
            "If the Sun is in the 6th house of a national chart (Ministry of Defense) and "
            "conjunct a malefic (Saturn, Mars, or Rahu), the diagnostic must trigger a "
            "'Serious Border Clash Alert'. The 6th house governs Armed Forces and territorial "
            "attacks. Sun + malefic here energizes the military with a combative, aggressive "
            "national leadership disposition. If Mars is lord of both the 6th AND 7th houses, "
            "open war is a certainty."
        ),
        "condition": {
            "planet": "Sun",
            "house": 6,
            "additional_condition": "Conjunct Saturn, Mars, or Rahu",
            "result": "Serious Border Clash Alert",
            "mars_lords_6_and_7_veto": "IF Mars lords both 6th and 7th THEN Open War = CERTAIN"
        },
        "synthesis_sources": [
            {"book": "mehta_rao", "chapter": "Ch 6", "label": "Houses and their Signification"}
        ]
    },
    {
        "rule_id": "mundane-mehta-ch6-eclipse-10th-overthrow",
        "sub_type": "governance_8th_house_veto",
        "title": "Mehta Ch 6 — Eclipse / Malefic in 10th House: Government Overthrow Sign",
        "description": (
            "An eclipse falling in the 10th house of a national chart is a direct sign of "
            "defeat or overthrow of the government. Any malefic transit or station in the "
            "10th house indicates disgrace, scandals, and illness or death among royalty/heads "
            "of state. The 10th house is the Executive Office (Prime Minister, President); "
            "affliction here directly targets the ruling authority."
        ),
        "condition": {
            "trigger_1": "Eclipse (solar or lunar) falling on 10th house of national chart",
            "trigger_2": "Malefic (Saturn, Rahu, Mars) stationed in 10th house",
            "result": "Government Defeat / Overthrow / Disgrace of Head of State",
            "moon_materialization": "Lunation (New/Full Moon) in 10th acts as Minute Hand materializing eclipse trends"
        },
        "synthesis_sources": [
            {"book": "mehta_rao", "chapter": "Ch 6", "label": "Houses and their Signification"}
        ]
    },
    {
        "rule_id": "mundane-mehta-ch6-5th-malefic-assassination",
        "sub_type": "hazard_pm_jeopardy",
        "title": "Mehta Ch 6 — 5th House Malefics + 10th Lord Afflicted: Assassination / Danger to Ruler",
        "description": (
            "The 5th house is the 8th from the 10th house (Danger to the Ruler position). "
            "If the 5th house contains malefics (especially Saturn, Mars, Rahu) AND the 10th "
            "lord is simultaneously afflicted, the diagnostic triggers a 'Critical Danger to "
            "Ruler' warning — signaling assassination plots, terrorist attacks on officials, "
            "or the sudden political elimination of the head of state."
        ),
        "condition": {
            "trigger_1": "5th house contains one or more malefics (Saturn, Mars, Rahu)",
            "trigger_2": "10th lord is afflicted (by malefic aspect, combustion, or debilitation)",
            "result": "Critical Danger to Ruler — Assassination / Terror / Political Elimination risk",
            "5th_house_role": "8th from 10th = danger zone for the ruler"
        },
        "synthesis_sources": [
            {"book": "mehta_rao", "chapter": "Ch 6", "label": "Houses and their Signification"}
        ]
    },
    {
        "rule_id": "mundane-mehta-ch6-sat-10th-democracy",
        "sub_type": "governance_fixed_lagna",
        "title": "Mehta Ch 6 — Saturn in 10th House: Democracy vs. Dictator Diagnostic",
        "description": (
            "Saturn in the 10th house produces diametrically opposite results based on "
            "the nature of the political system: "
            "(1) In a Republic/Democracy chart: BENEFIC — strengthens democratic institutions, "
            "rule of law, and long-term stable governance. "
            "(2) In a Coup-based/Autocratic chart: FATAL — Saturn undermines the dictator's "
            "authority, causing internal dissent, labor revolts, and eventual overthrow. "
            "Saturn as natural significator of democracy, labor, and the common people acts "
            "against authoritarian power in the 10th house context."
        ),
        "condition": {
            "planet": "Saturn",
            "house": 10,
            "republic_chart_result": "BENEFIC — democracy strengthened, stable long-term governance",
            "coup_chart_result": "FATAL — dictator's authority undermined, internal revolt, eventual overthrow"
        },
        "synthesis_sources": [
            {"book": "mehta_rao", "chapter": "Ch 6", "label": "Houses and their Signification"}
        ]
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# GROUP O — RAPHAEL CH 3: DIAGNOSTIC RULES (3 rules)
# ─────────────────────────────────────────────────────────────────────────────
GROUP_O = [
    {
        "rule_id": "mundane-raphael-ch3-angular-multiplier",
        "sub_type": "house_strength_weighting",
        "title": "Raphael Ch 3 — Angular House Power Multiplier",
        "description": (
            "All mundane diagnoses must apply a power multiplier based on house type: "
            "Angular houses (1, 4, 7, 10) = Strongest — apply FULL diagnostic weight; "
            "Succedent houses (2, 5, 8, 11) = Medium — apply 0.7× weight; "
            "Cadent houses (3, 6, 9, 12) = Weakest — apply 0.4× weight. "
            "Additionally, any planet within 5 degrees of a house cusp is 'Accidentally "
            "Dignified' — its effects are significantly amplified regardless of house type. "
            "Example: A malefic in the 4th house (Angular) triggers a higher Calamity Warning "
            "than the same malefic in the 3rd house (Cadent)."
        ),
        "condition": {
            "angular_houses": [1, 4, 7, 10],
            "succedent_houses": [2, 5, 8, 11],
            "cadent_houses": [3, 6, 9, 12],
            "weight_angular": 1.0,
            "weight_succedent": 0.7,
            "weight_cadent": 0.4,
            "cusp_5_degree_rule": "Planet within 5° of house cusp = Accidentally Dignified; effects amplified"
        },
        "synthesis_sources": [
            {"book": "raphael_west", "chapter": "Ch 3", "label": "Twelve Mundane Houses"}
        ]
    },
    {
        "rule_id": "mundane-raphael-ch3-intellectual-triad",
        "sub_type": "national_mindset_audit",
        "title": "Raphael Ch 3 — Intellectual Triad (Houses 1+3+9): National Mind Synchrony",
        "description": (
            "Houses 1, 3, and 9 form the Intellectual Triad — the synchronized diagnostic "
            "group for the 'Mind of the Nation'. "
            "House 1 = Collective mental state of the people. "
            "House 3 = The Press, newspapers, literary concerns. "
            "House 9 = Religious attitude and higher thought of the populace. "
            "For any query involving National Mood, Press Freedom, Propaganda, or "
            "Religious Harmony, audit all three houses together as a single triad. "
            "If benefics occupy all three: output 'Nation entering period of intellectual "
            "growth, press freedom, and religious harmony.' "
            "If malefics afflict all three: output 'National intellectual crisis, press "
            "censorship, and religious conflict.'"
        ),
        "condition": {
            "trigger_queries": ["National Mood", "Press Freedom", "Propaganda", "Religious Harmony", "Public Opinion"],
            "benefic_triad_result": "Nation entering period of intellectual growth, press freedom, and religious harmony",
            "malefic_triad_result": "National intellectual crisis, press censorship, and religious conflict",
            "shipping_9th": "Malefic in 9th → disruption in international shipping and scientific setbacks"
        },
        "synthesis_sources": [
            {"book": "raphael_west", "chapter": "Ch 3", "label": "Twelve Mundane Houses"}
        ]
    },
    {
        "rule_id": "mundane-raphael-ch3-opposition-4th-trigger",
        "sub_type": "governance_coalition_discord",
        "title": "Raphael Ch 3 — 4th House Opposition Rise Trigger",
        "description": (
            "Raphael explicitly places the Opposition Party in the 4th house. "
            "For queries about 'future of the political opposition', prioritize 4th house "
            "transits above all other factors. "
            "Opposition Rise Gate: IF (4th house lord is strong AND aspected by Jupiter) AND "
            "(10th house / Government is afflicted by malefics) THEN output 'High probability "
            "of Opposition party gaining significant influence or winning public favor.' "
            "Also tracks weather/agriculture (4th house) vs. opposition politics — both are "
            "activated simultaneously by the same transits."
        ),
        "condition": {
            "trigger_1": "4th house lord strong and aspected by Jupiter",
            "trigger_2": "10th house (Government) afflicted by malefics",
            "result": "High probability of Opposition party gaining significant influence or winning public favor",
            "dual_4th_activation": "Same 4th house malefic transit triggers BOTH agricultural crisis AND opposition surge"
        },
        "synthesis_sources": [
            {"book": "raphael_west", "chapter": "Ch 3", "label": "Twelve Mundane Houses"}
        ]
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# COMBINE ALL RULES
# ─────────────────────────────────────────────────────────────────────────────
ALL_RULES = GROUP_L + GROUP_M + GROUP_N + GROUP_O

# ─────────────────────────────────────────────────────────────────────────────
# INGEST
# ─────────────────────────────────────────────────────────────────────────────
async def run():
    now = datetime.now(timezone.utc)
    for rule in ALL_RULES:
        rule["batch_id"]        = BATCH_ID
        rule["science_id"]      = "mundane_jyotish"
        rule["collection"]      = "interpretation_rules"
        rule["rule_type"]       = rule.get("rule_type", "interpretation")
        rule["approval_status"] = "pending_review"
        rule["checkable"]       = False
        rule["ingested_at"]     = now
        if "synthesis_sources" not in rule:
            rule["synthesis_sources"] = []

    if DRY_RUN:
        print(f"\nBuilt {len(ALL_RULES)} rules for batch {BATCH_ID}")
        print(f"Collection: interpretation_rules  |  science: mundane_jyotish\n")
        print("Breakdown by group:")
        print(f"  Group L — Gopal Ch 2 Heuristic Filters  : {len(GROUP_L)}")
        print(f"  Group M — Mehta Ch 10 Macro-Conjunctions : {len(GROUP_M)}")
        print(f"  Group N — Mehta Ch 6 Diagnostic Rules    : {len(GROUP_N)}")
        print(f"  Group O — Raphael Ch 3 Diagnostic Rules  : {len(GROUP_O)}")
        print(f"\nTotal: {len(ALL_RULES)}\n")
        print("Rule IDs:")
        for r in ALL_RULES:
            print(f"  {r['rule_id']}")
        print("\nDry run complete.")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    col = db["interpretation_rules"]
    inserted = updated = 0
    for rule in ALL_RULES:
        result = await col.update_one(
            {"rule_id": rule["rule_id"]},
            {"$set": rule},
            upsert=True
        )
        if result.upserted_id:
            inserted += 1
        else:
            updated += 1
    client.close()
    print(f"Done. Inserted={inserted}  Updated={updated}  Batch={BATCH_ID}")

if __name__ == "__main__":
    asyncio.run(run())
