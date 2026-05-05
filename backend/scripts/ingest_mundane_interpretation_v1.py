#!/usr/bin/env python3
"""
ingest_mundane_interpretation_v1.py

Mundane Astrology — Interpretation Rules
BATCH_ID: mundane-interp-v1-20260505
TARGET COLLECTION: horoscope_db.interpretation_rules
science_id: "mundane_jyotish"  (NEVER "jyotish" — different domain)

152 rules across 11 groups:
  A. Global Tone / Samvatsar          (Gaur Ch 1)          —  8 rules
  B. Celestial Council Outcomes       (Gaur Ch 2)          — 12 rules
  C. Agricultural & Weather           (Gaur Ch 3)          —  8 rules
  D. Koorma Directional Predictions   (Gaur Ch 4/5)        —  9 rules
  E. Transit Key Rules                (Gaur Ch 10)         — 15 rules
  F. Eclipse Rules                    (Raphael Ch 23/24/25)— 12 rules
  G. War & Geopolitical               (Mehta Ch 19 / Gopal Ch 8) — 15 rules
  H. Seismic Engine                   (Mehta Ch 11)        — 12 rules
  I. Governance & Election            (Gopal Ch 4/5 / Mehta Ch 18) — 16 rules
  J. Historical Validation            (Mehta Ch 19/21 / Gopal Ch 14) — 13 rules
  K. Hazard & Special                 (Mehta Ch 21 / Gopal Ch 8) — 12 rules

Schema decisions (locked):
  - science = "mundane_jyotish"
  - all checkable = False (no evaluator wired yet for mundane)
  - interpretation.summary = rule_id slug (never prose — prevents truncation flags)
  - source.book = primary attribution book
  - source.synthesis_sources = all contributing books per rule
  - historical_validation rules: rule_type = "historical_validation"
  - logic_unit format: LU_MA.<group>.<slug>
  - batch_id: mundane-interp-v1-20260505
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pymongo import MongoClient

SCIENCE  = "mundane_jyotish"
BATCH_ID = "mundane-interp-v1-20260505"

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _base(rule_id: str, lu: str, rule_type: str, sub_type: str,
          summary: str, detailed: str, book: str, chapter: int,
          synthesis_sources: list, now: str) -> dict:
    return {
        "rule_id":         rule_id,
        "approval_status": "pending_review",
        "source": {
            "science":           SCIENCE,
            "book":              book,
            "chapter":           chapter,
            "logic_unit":        lu,
            "batch_id":          BATCH_ID,
            "synthesis_sources": synthesis_sources,
        },
        "metadata": {
            "rule_type": rule_type,
            "sub_type":  sub_type,
        },
        "interpretation": {
            "summary":  summary,
            "detailed": detailed,
            "remedies": [],
        },
        "validation": {
            "checkable":    False,
            "yoga_check":   {"type": "manual", "checkable": False},
            "validated_by": None,
            "validated_at": None,
        },
        "created_at": now,
        "updated_at": now,
    }


# ---------------------------------------------------------------------------
# GROUP A — Global Tone / Samvatsar  (Gaur Ch 1)
# ---------------------------------------------------------------------------

def build_group_a(now: str) -> list[dict]:
    rules = []

    # A-1: Samvatsar King signification
    r = _base("mundane-gaur-ch1-samvatsar-king", "LU_MA.global_tone.samvatsar_king",
              "mundane_global_tone", "samvatsar_king",
              "mundane-gaur-ch1-samvatsar-king",
              "The planet that is King of the Samvatsar (Hindu year) governs the overall "
              "national and global tone for that year. Its natural significations manifest "
              "as the dominant theme: Sun-King = strong leadership/authoritarian; "
              "Moon-King = public welfare/emotional; Mars-King = war/violence; "
              "Mercury-King = commerce/communication; Jupiter-King = justice/religion; "
              "Venus-King = culture/luxury/diplomacy; Saturn-King = labour/austerity/disease.",
              "Gaur/AIFAS", 1, ["gaur_aifas"], now)
    r["condition"] = {"condition_type": "samvatsar_king", "extra_cond": {
        "king_results": {
            "Sun":     {"theme": "Authority and power — rulers assert dominance; strong governance",    "risk": "Ego-driven conflict, authoritarian overreach"},
            "Moon":    {"theme": "Public welfare, water, women — popular governments flourish",          "risk": "Emotional instability, floods, indecisiveness"},
            "Mars":    {"theme": "War, courage, manufacturing — military budgets rise",                  "risk": "Violence, fires, border conflicts, surgical strikes"},
            "Mercury": {"theme": "Trade, communications, education — commerce booms",                   "risk": "Fraud, misinformation, market manipulation"},
            "Jupiter": {"theme": "Religion, justice, dharma — moral prosperity",                        "risk": "Judicial crises, religious controversies"},
            "Venus":   {"theme": "Culture, luxury, diplomacy — arts and beauty flourish",               "risk": "Moral decline, excessive luxury spending, political compromise"},
            "Saturn":  {"theme": "Labour, crops, discipline — austerity drives reform",                 "risk": "Famine, epidemics, strikes, agricultural failure"},
            "Rahu":    {"theme": "Foreign influence, disruption — outsiders reshape national policy",   "risk": "Foreign manipulation, identity crises, mass misinformation"},
            "Ketu":    {"theme": "Spiritual upheaval, hidden forces — mystical/covert events",          "risk": "Fires, epidemics, covert destabilization, mass disillusionment"},
        }
    }}
    rules.append(r)

    # A-2: Afflicted King — national crisis flag
    r = _base("mundane-gaur-ch1-king-afflicted", "LU_MA.global_tone.king_afflicted",
              "mundane_global_tone", "affliction_flag",
              "mundane-gaur-ch1-king-afflicted",
              "IF the Samvatsar King planet is afflicted (conjunct or aspected by malefics, "
              "combust, debilitated, or in enemy sign) THEN the domain it governs faces a "
              "national crisis for the year. Severity scales with the number of afflictions.",
              "Gaur/AIFAS", 1, ["gaur_aifas"], now)
    r["condition"] = {"condition_type": "samvatsar_king_afflicted",
                      "extra_cond": {"severity_scale": "1 affliction = moderate; 2 = severe; 3+ = critical national crisis"}}
    rules.append(r)

    # A-3: King + Minister same planet — concentration of power
    r = _base("mundane-gaur-ch1-king-minister-same", "LU_MA.global_tone.king_minister_same",
              "mundane_global_tone", "power_concentration",
              "mundane-gaur-ch1-king-minister-same",
              "IF Samvatsar King and Minister are the same planet (weekday lord at Pratipada "
              "= weekday lord at Aries Ingress) THEN absolute concentration of power. "
              "Strong planet = decisive autocratic governance; afflicted = despotism and instability.",
              "Gaur/AIFAS", 1, ["gaur_aifas", "mehta_rao"], now)
    r["condition"] = {"condition_type": "king_minister_same_planet"}
    rules.append(r)

    # A-4: Benefic King — prosperity year
    r = _base("mundane-gaur-ch1-benefic-king", "LU_MA.global_tone.benefic_king",
              "mundane_global_tone", "prosperity_signal",
              "mundane-gaur-ch1-benefic-king",
              "IF Samvatsar King is a natural benefic (Jupiter, Venus, Mercury-unafflicted, "
              "or waxing Moon) AND the King planet is strong (own sign, exaltation, or "
              "angular) THEN the year delivers national prosperity, abundance, and peace.",
              "Gaur/AIFAS", 1, ["gaur_aifas"], now)
    r["condition"] = {"condition_type": "samvatsar_king",
                      "extra_cond": {"king_quality": "natural_benefic", "king_strength": "strong"}}
    rules.append(r)

    # A-5: Malefic King — turbulence year
    r = _base("mundane-gaur-ch1-malefic-king", "LU_MA.global_tone.malefic_king",
              "mundane_global_tone", "turbulence_signal",
              "mundane-gaur-ch1-malefic-king",
              "IF Samvatsar King is a natural malefic (Saturn, Mars, Rahu, Ketu, Sun) "
              "AND afflicted THEN the year is marked by conflict, hardship, or crisis "
              "in the domain governed by that planet. Saturn-King afflicted = famine/disease. "
              "Mars-King afflicted = war/fires. Rahu-King afflicted = foreign manipulation.",
              "Gaur/AIFAS", 1, ["gaur_aifas"], now)
    r["condition"] = {"condition_type": "samvatsar_king",
                      "extra_cond": {"king_quality": "natural_malefic", "king_strength": "afflicted"}}
    rules.append(r)

    # A-6: Meghesh (Weather Secretary) afflicted — poor monsoon
    r = _base("mundane-gaur-ch1-meghesh-afflicted", "LU_MA.global_tone.meghesh_afflicted",
              "mundane_global_tone", "rainfall_forecast",
              "mundane-gaur-ch1-meghesh-afflicted",
              "IF Meghesh (Weather Secretary — weekday lord at Sun's Ardra ingress) is "
              "afflicted (debilitated, combust, or aspected by Saturn/Mars/Rahu) THEN "
              "monsoon will be deficient: drought risk HIGH for that year. "
              "Strong Meghesh in water sign = abundant rainfall.",
              "Gaur/AIFAS", 1, ["gaur_aifas"], now)
    r["condition"] = {"condition_type": "celestial_council_role",
                      "extra_cond": {"role": "meghesh", "planet_state": "afflicted"}}
    r["interpretation"]["result"] = "Monsoon deficient — drought risk elevated"
    rules.append(r)

    # A-7: Durgesh (Defence) afflicted — border threat
    r = _base("mundane-gaur-ch1-durgesh-afflicted", "LU_MA.global_tone.durgesh_afflicted",
              "mundane_global_tone", "security_forecast",
              "mundane-gaur-ch1-durgesh-afflicted",
              "IF Durgesh (Defence Secretary — weekday lord at Sun's Leo ingress) is "
              "afflicted THEN national defence is compromised for the year: border "
              "incursions, military setbacks, or internal security failures likely. "
              "Mars as strong Durgesh = decisive military strength.",
              "Gaur/AIFAS", 1, ["gaur_aifas"], now)
    r["condition"] = {"condition_type": "celestial_council_role",
                      "extra_cond": {"role": "durgesh", "planet_state": "afflicted"}}
    r["interpretation"]["result"] = "Defence compromised — border/security threat elevated"
    rules.append(r)

    # A-8: Dhanesh (Finance) strong — economic growth year
    r = _base("mundane-gaur-ch1-dhanesh-strong", "LU_MA.global_tone.dhanesh_strong",
              "mundane_global_tone", "economic_forecast",
              "mundane-gaur-ch1-dhanesh-strong",
              "IF Dhanesh (Finance Secretary — weekday lord at Sun's Taurus ingress) is "
              "strong (own sign, exaltation, angular, aspected by Jupiter) THEN national "
              "economy grows: treasury surplus, stock market bullish, foreign investment rises.",
              "Gaur/AIFAS", 1, ["gaur_aifas"], now)
    r["condition"] = {"condition_type": "celestial_council_role",
                      "extra_cond": {"role": "dhanesh", "planet_state": "strong"}}
    r["interpretation"]["result"] = "National economy growing — treasury surplus, markets bullish"
    rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# GROUP B — Celestial Council Outcomes  (Gaur Ch 2)
# ---------------------------------------------------------------------------

def build_group_b(now: str) -> list[dict]:
    rules = []

    council_outcomes = [
        ("sun",     "Sun as King: Rulers assert dominance; decisive executive action; strong centralized government. Risk: authoritarian overreach, ego-driven conflict with neighbours."),
        ("moon",    "Moon as King: Public welfare policies dominate; emotional leadership; women gain prominence. Strong = floods (water abundance); afflicted = drought or public unrest."),
        ("mars",    "Mars as King: Military budgets rise; surgical strikes likely; manufacturing booms. Afflicted = war outbreak, fires, industrial accidents."),
        ("mercury", "Mercury as King: Commerce, trade, and communications lead the year. Media/IT sector dominant. Afflicted = fraud epidemics, market manipulation, misinformation crisis."),
        ("jupiter", "Jupiter as King: Justice, education, and religious harmony prevail. Judiciary active. Afflicted = judicial scandal, religious controversy, educational system failure."),
        ("venus",   "Venus as King: Cultural golden age; diplomatic initiatives; luxury sector booms. Afflicted = moral decline, over-spending, political compromise and corruption."),
        ("saturn",  "Saturn as King: Austerity and labour reforms dominate. Agricultural stability if strong. Afflicted = famine, epidemic, mass strikes, or prolonged drought year."),
        ("rahu",    "Rahu as King: Foreign influence reshapes national policy; outsiders gain power. Strong = international trade gains. Afflicted = foreign manipulation, identity crisis, conspiracy."),
        ("ketu",    "Ketu as King: Spiritual and covert forces active; hidden events shape the year. Afflicted = fires, epidemics, mass religious disillusionment, covert destabilization."),
    ]
    for planet, detailed in council_outcomes:
        rule_id = f"mundane-gaur-ch2-king-{planet}"
        r = _base(rule_id, f"LU_MA.celestial_council.king_{planet}",
                  "mundane_celestial_council", "king_outcome",
                  rule_id, detailed,
                  "Gaur/AIFAS", 2, ["gaur_aifas"], now)
        r["condition"] = {"condition_type": "celestial_council_king",
                          "extra_cond": {"king_planet": planet}}
        rules.append(r)

    # B-10: Minister afflicted
    r = _base("mundane-gaur-ch2-minister-afflicted", "LU_MA.celestial_council.minister_afflicted",
              "mundane_celestial_council", "minister_outcome",
              "mundane-gaur-ch2-minister-afflicted",
              "IF Minister planet (weekday lord at Aries Ingress) is afflicted THEN "
              "administrative machinery breaks down: policy paralysis, bureaucratic "
              "corruption, and failed legislation define the year.",
              "Gaur/AIFAS", 2, ["gaur_aifas"], now)
    r["condition"] = {"condition_type": "celestial_council_minister",
                      "extra_cond": {"planet_state": "afflicted"}}
    rules.append(r)

    # B-11: Sasyesh afflicted — crop failure
    r = _base("mundane-gaur-ch2-sasyesh-afflicted", "LU_MA.celestial_council.sasyesh_afflicted",
              "mundane_celestial_council", "crop_forecast",
              "mundane-gaur-ch2-sasyesh-afflicted",
              "IF Sasyesh (Summer Crops — weekday lord at Sun's Cancer ingress) is "
              "afflicted THEN Kharif (summer crop) season fails: food grain production "
              "below average, prices rise sharply from September onward.",
              "Gaur/AIFAS", 2, ["gaur_aifas"], now)
    r["condition"] = {"condition_type": "celestial_council_role",
                      "extra_cond": {"role": "sasyesh", "planet_state": "afflicted"}}
    r["interpretation"]["result"] = "Kharif crop failure — grain prices rise from September"
    rules.append(r)

    # B-12: Dhanyesh afflicted — grain scarcity
    r = _base("mundane-gaur-ch2-dhanyesh-afflicted", "LU_MA.celestial_council.dhanyesh_afflicted",
              "mundane_celestial_council", "grain_forecast",
              "mundane-gaur-ch2-dhanyesh-afflicted",
              "IF Dhanyesh (Grains — weekday lord at Sun's Virgo ingress) is afflicted "
              "THEN cereal production (wheat, rice) falls below national requirement: "
              "food security risk, potential import dependency.",
              "Gaur/AIFAS", 2, ["gaur_aifas"], now)
    r["condition"] = {"condition_type": "celestial_council_role",
                      "extra_cond": {"role": "dhanyesh", "planet_state": "afflicted"}}
    r["interpretation"]["result"] = "Grain scarcity — cereal import dependency risk"
    rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# GROUP C — Agricultural & Weather  (Gaur Ch 3)
# ---------------------------------------------------------------------------

def build_group_c(now: str) -> list[dict]:
    rules = []

    entries = [
        ("mundane-gaur-ch3-high-jal-stambha",   "jal_high",
         "HIGH Jal Stambha (>50% water pillar at Pratipada) = abundant rainfall year. "
         "Rivers in flood; irrigation surplus; agricultural prosperity. Watch for waterlogging in low-lying areas."),
        ("mundane-gaur-ch3-low-jal-stambha",    "jal_low",
         "LOW Jal Stambha (<20% water pillar at Pratipada) = drought year. "
         "Water scarcity in arid zones; crop failures in rain-fed areas; wells/reservoirs at risk."),
        ("mundane-gaur-ch3-high-anna-stambha",  "anna_high",
         "HIGH Anna Stambha (>50% food pillar) = food surplus year. "
         "Grain prices fall; public contentment rises; agricultural income above average."),
        ("mundane-gaur-ch3-low-anna-stambha",   "anna_low",
         "LOW Anna Stambha (<20% food pillar) = food scarcity year. "
         "Grain prices rise sharply; social unrest risk; government may need to release strategic reserves."),
        ("mundane-gaur-ch3-high-vayu-stambha",  "vayu_high",
         "HIGH Vayu Stambha (>50% wind pillar) = storm/cyclone year. "
         "Coastal regions at cyclone risk; crop damage from strong winds; aviation disruption."),
        ("mundane-gaur-ch3-saturn-ardra",       "saturn_ardra",
         "Saturn transiting Ardra nakshatra (Gemini 6°40'–20°) during monsoon season = "
         "severely deficient rainfall: historic droughts have correlated with this transit. "
         "Priority alert for agriculture and water ministries."),
        ("mundane-gaur-ch3-rohini-protection",  "rohini_protection",
         "IF Rohini nakshatra is UNAFFLICTED (no Saturn, Mars, or Rahu transiting it) "
         "AND the monsoon enters on schedule THEN rainfall will be abundant and well-distributed. "
         "Rohini = the 'King's Eye' — its health determines annual rainfall quality."),
        ("mundane-gaur-ch3-yield-price-inverse","yield_price_inverse",
         "Agricultural yield and food prices are INVERSELY correlated: "
         "High crop yield → prices LOW (oversupply). "
         "Low crop yield → prices HIGH (scarcity premium). "
         "This inverse law overrides all other commodity price signals when yield data is available."),
    ]
    for rule_id, sub, detailed in entries:
        r = _base(rule_id, f"LU_MA.agricultural.{sub}",
                  "mundane_agricultural", sub,
                  rule_id, detailed,
                  "Gaur/AIFAS", 3, ["gaur_aifas", "mehta_rao"], now)
        r["condition"] = {"condition_type": "agricultural_indicator",
                          "extra_cond": {"indicator": sub}}
        rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# GROUP D — Koorma Directional Predictions  (Gaur Ch 4/5)
# ---------------------------------------------------------------------------

def build_group_d(now: str) -> list[dict]:
    rules = []

    zones = [
        ("center-back",   "Krittika/Rohini/Mrigshira", "Central India",     "Central India faces disruption; interior regions affected"),
        ("mouth-east",    "Ardra/Punarvasu/Pushya",    "Eastern region",    "Eastern zones face trouble; eastern neighbours trigger conflict"),
        ("front-right-se","Ashlesha/Magha/P.Phalguni", "South-East",        "South-East direction affected; Sri Lanka, Myanmar, Thailand at risk"),
        ("right-south",   "U.Phalguni/Hasta/Chitra",   "Southern region",   "Southern India/South Asia affected; Tamil Nadu, Kerala, South-East Asia"),
        ("back-right-sw", "Swati/Anuradha/Vishakha",   "South-West",        "South-West affected; Pakistan (inner region), Arabian Sea, Gulf"),
        ("tail-west",     "Jyeshtha/Mool/P.Ashadh",    "Western region",    "Western zones affected; Rajasthan, Gujarat, Pakistan border"),
        ("back-left-nw",  "U.Ashadh/Shravan/Dhanishtha","North-West",       "North-West affected; Punjab, Kashmir, Afghanistan, Pakistan (North)"),
        ("left-north",    "Shatbhisha/P.Bhadra/U.Bhadra","Northern region", "Northern India affected; J&K, China border, Nepal, Himalayas"),
        ("front-left-ne", "Revati/Ashwini/Bharani",    "North-East",        "North-East affected; Bangladesh, Myanmar, China (Assam/Arunachal border)"),
    ]
    for zone_slug, nakshatras, direction, outcome in zones:
        rule_id = f"mundane-gaur-ch4-koorma-{zone_slug}"
        r = _base(rule_id, f"LU_MA.koorma.{zone_slug.replace('-','_')}",
                  "mundane_koorma_directional", "zone_malefic_transit",
                  rule_id,
                  f"IF a malefic planet (Saturn, Mars, Rahu, or Ketu) transits the nakshatras "
                  f"of the Koorma zone '{zone_slug}' ({nakshatras}) THEN the {direction} faces "
                  f"trouble: {outcome}. "
                  f"Benefic transit (Jupiter, Venus) in same zone = prosperity in that direction.",
                  "Gaur/AIFAS", 4, ["gaur_aifas", "mehta_rao"], now)
        r["condition"] = {
            "condition_type": "koorma_zone_transit",
            "extra_cond": {
                "zone_slug":  zone_slug,
                "nakshatras": nakshatras,
                "direction":  direction,
                "malefic_result":  outcome,
                "benefic_result":  f"Prosperity in {direction} — good harvests, peaceful conditions",
                "geo_entity_ref":  f"koorma-{zone_slug}",
            }
        }
        rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# GROUP E — Transit Key Rules  (Gaur Ch 10)
# ---------------------------------------------------------------------------

def build_group_e(now: str) -> list[dict]:
    rules = []

    transit_rules = [
        ("mundane-gaur-ch10-saturn-rohini-drought",
         "Saturn transiting Rohini nakshatra (Taurus 10°–23°20') = CRITICAL DROUGHT SIGNAL. "
         "Rohini is the 'King's Eye' of rainfall; Saturn's cold/dry nature in Rohini "
         "throttles monsoon. Also the Rohini Gate war threshold — see war rules. "
         "Historical: 1971 Indo-Pak war, WWI, WWII all triggered with Saturn in Rohini.",
         "transit_saturn_rohini", "drought_war_gate"),

        ("mundane-gaur-ch10-saturn-retrograde-uttarashadh",
         "Saturn retrograde in Uttarashadha nakshatra (Sagittarius 26°40'–Capricorn 10°) "
         "and moving back into Poorvashadha = SEVERE DROUGHT AND GRAIN CRISIS. "
         "The retrograde motion backward across the Sagittarius/Capricorn junction "
         "signals prolonged disruption to winter crops.",
         "transit_saturn_retrograde_uttarashadh", "drought_signal"),

        ("mundane-gaur-ch10-retrograde-mars-war-veto",
         "Retrograde Mars is a PREREQUISITE for war escalation. "
         "If Mars is DIRECT during border tensions, classify as 'Non-Escalatory Friction' — "
         "conflict will not escalate to full-scale war. "
         "Only retrograde Mars = war outbreak risk (validated: all major Indian wars). "
         "This rule VETOES war predictions when Mars is in direct motion.",
         "transit_mars_retrograde_veto", "war_prerequisite"),

        ("mundane-gaur-ch10-mars-perigee-manufacturing",
         "Mars at perigee (closest approach to Earth) = Manufacturing and mechanical sector BOOM. "
         "Auto-ancillary exports peak. Also triggers the 'South Leadership Replacement' veto: "
         "incumbents in the Southern direction (Mars in southern sign) face electoral defeat.",
         "transit_mars_perigee", "sector_boom"),

        ("mundane-gaur-ch10-jupiter-pushya-bull",
         "Saturn OR Jupiter transiting Pushya nakshatra (Cancer 3°20'–16°40') = "
         "exceptional equity market bull run. 50-100% index growth expected. "
         "Sector winners: Banking, FMCG, IT, Telecom. "
         "Validated: 2006 Sensex rose from 6,000 to 12,000+ during Saturn in Pushya.",
         "transit_saturn_pushya", "market_bull_run"),

        ("mundane-gaur-ch10-saturn-leo-real-estate",
         "Saturn entering Leo (Simha) = Real estate and property market 100% growth phase. "
         "Middle-class obsession with home ownership peaks. Builder stocks surge. "
         "Validated: 2006-2008 metro property surge during Saturn in Leo.",
         "transit_saturn_leo", "real_estate_boom"),

        ("mundane-gaur-ch10-saturn-ketu-leo-oil",
         "Saturn-Ketu conjunction in Leo = Crude oil prices surge to $70+/barrel. "
         "Energy sector pressures; proxy war risks increase. "
         "Validated: 2006 oil price peak.",
         "transit_saturn_ketu_leo", "oil_price_spike"),

        ("mundane-gaur-ch10-rahu-ketu-cancer-capricorn",
         "Rahu-Ketu axis in Cancer-Capricorn = India's critical vulnerability axis activated. "
         "This is the SAME axis as the 1962 China war and 1971 Pakistan war. "
         "Heightened risk of border conflict or leadership crisis for India when nodal "
         "axis falls on Cancer-Capricorn.",
         "transit_rahu_cancer_capricorn", "india_war_axis"),

        ("mundane-gaur-ch10-sun-ardra-rain",
         "Sun entering Ardra nakshatra (Gemini 6°40'–20°) = monsoon season officially "
         "activates (traditional: Ardra Pravesh = onset of rains). "
         "Weekday of Sun's Ardra entry sets the Meghesh for the entire monsoon season. "
         "Saturn/Rahu in Ardra at this point = deficient monsoon despite seasonal onset.",
         "transit_sun_ardra", "monsoon_onset"),

        ("mundane-gaur-ch10-saturn-3rd-india-it",
         "Saturn transiting the 3rd house of India's national foundation chart (Cancer Lagna = 3rd house Virgo) "
         "= IT/BPO sector becomes national economic backbone. "
         "Ignore all media skepticism about sector failure during this transit — the sector thrives. "
         "Validated: India's IT boom during Saturn's transit of India's 3rd house (2003-2006).",
         "transit_saturn_3rd_india", "it_bpo_boom"),

        ("mundane-gaur-ch10-three-day-rule",
         "TEMPORAL INSTABILITY GATE: If a lunar month contains THREE Sundays, Tuesdays, OR Saturdays "
         "(any one of these three weekdays appearing 3 times in the same lunar month) then "
         "the 'Instability Coefficient' rises by 0.80 — high probability of inauspicious "
         "outbreak (conflict, natural disaster, political crisis) during that month.",
         "temporal_three_day_rule", "instability_gate"),

        ("mundane-gaur-ch10-retrograde-famine",
         "Saturn retrograde in Uttarashadha + moving back into Poorvashadha = "
         "severe drought and grain crisis at national scale. "
         "This specific retrograde pattern (crossing the Sagittarius/Capricorn nakshatra boundary "
         "backward) disrupts both monsoon and rabi crops simultaneously.",
         "transit_saturn_retrograde_famine", "famine_signal"),

        ("mundane-gaur-ch10-sun-mool-gold-cheap",
         "Sun transiting Mool nakshatra (Sagittarius 0°–13°20') = Gold and Silver prices FALL. "
         "Cotton and yarn also cheap. Counter-intuitive rule: Mool (root-destroying) sign "
         "suppresses precious metal prices. Buy window for gold accumulation.",
         "transit_sun_mool", "gold_cheap"),

        ("mundane-gaur-ch10-sun-anuradha",
         "Sun transiting Anuradha nakshatra (Scorpio 3°20'–16°40') = Gold, Silver, AND Wheat "
         "ALL simultaneously cheap. Rare multi-commodity cheap window. "
         "Also: woolen clothes expensive in this window.",
         "transit_sun_anuradha", "multi_cheap"),

        ("mundane-gaur-ch10-jupiter-direct-benefic",
         "Jupiter direct in own sign (Sagittarius or Pisces) OR exaltation (Cancer) = "
         "maximum benefic transit year. National dharma, judiciary, and education peak. "
         "Grain prices stable. International diplomacy favourable for the nation whose "
         "Lagna or 9th lord is Jupiter.",
         "transit_jupiter_own_sign", "benefic_peak"),
    ]

    for rule_id, detailed, sub, rule_type in transit_rules:
        r = _base(rule_id, f"LU_MA.transit.{sub}",
                  "mundane_transit", rule_type,
                  rule_id, detailed,
                  "Gaur/AIFAS", 10, ["gaur_aifas", "mehta_rao", "gopal_modern"], now)
        r["condition"] = {"condition_type": "planetary_transit",
                          "extra_cond": {"transit_key": sub}}
        rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# GROUP F — Eclipse Rules  (Raphael Ch 23/24/25)
# ---------------------------------------------------------------------------

def build_group_f(now: str) -> list[dict]:
    rules = []

    eclipse_rules = [
        ("mundane-raphael-ch23-eclipse-leo1",
         "Solar eclipse in Leo 1st decanate (0°–10°) = Death of a famous prince or sovereign; "
         "scarcity of corn. National leaders in Leo-ruled countries at physical risk.",
         "eclipse_leo_1st", "leadership_death_grain"),
        ("mundane-raphael-ch23-eclipse-leo2",
         "Solar eclipse in Leo 2nd decanate (10°–20°) = Many troubles for kings, princes, "
         "and great men; political turbulence at the top. Multi-leader crisis year.",
         "eclipse_leo_2nd", "leader_crisis"),
        ("mundane-raphael-ch23-eclipse-leo3",
         "Solar eclipse in Leo 3rd decanate (20°–30°) = Profanation of holy places; "
         "captivity and ransacking of cities. Religious site attacks; urban conflict.",
         "eclipse_leo_3rd", "religious_site_attacks"),
        ("mundane-raphael-ch23-eclipse-scorpio",
         "Solar or Lunar eclipse in Scorpio = Mass deaths, epidemics, and hidden conspiracies. "
         "Underground movements surface. Scorpio-ruled nations (Norway, Morocco) at risk. "
         "India: Scorpio = 7th house (war/open enemies) — heightened conflict risk.",
         "eclipse_scorpio", "mass_death_epidemic"),
        ("mundane-raphael-ch23-eclipse-taurus",
         "Solar or Lunar eclipse in Taurus = Agricultural disruption; financial system stress. "
         "Taurus-ruled economies (Ireland, Iran, India's Lagna) face wealth shocks. "
         "Rohini Gate activated if eclipse falls between 10°–23°20' Taurus.",
         "eclipse_taurus", "financial_agricultural_stress"),
        ("mundane-raphael-ch23-eclipse-aries",
         "Solar eclipse in Aries = Leadership transitions in Aries-ruled nations "
         "(UK, Germany, France, Japan). Heads of state face electoral defeat or forced removal.",
         "eclipse_aries", "leadership_transition"),
        ("mundane-raphael-ch23-eclipse-cancer",
         "Solar or Lunar eclipse in Cancer = Flooding, maritime disasters, public emotional "
         "crises. India's Sun is in Cancer (Independence Chart) — leadership under extreme pressure.",
         "eclipse_cancer", "flood_leadership_crisis"),
        ("mundane-raphael-ch25-saturn-mars",
         "Saturn-Mars conjunction = War, rioting, and regicide. Frequency: approximately every 2 years. "
         "Intensity magnified if conjunction occurs in Rohini (Taurus) or Aries. "
         "Historical: every major Indo-Pak military confrontation features Saturn-Mars alignment.",
         "conjunction_saturn_mars", "war_regicide"),
        ("mundane-raphael-ch25-jupiter-saturn-20yr",
         "Jupiter-Saturn conjunction (every 20 years) = Generational shift in world order. "
         "The sign of conjunction determines the dominant geopolitical theme for 20 years. "
         "Full mutation cycle: 724 years (complete journey through all elements).",
         "conjunction_jupiter_saturn_20yr", "generational_shift"),
        ("mundane-raphael-ch25-eclipse-4th-8th",
         "Eclipse falling in 4th or 10th house of a national foundation chart = "
         "The nation experiences its most intense disruption of the year in that chart. "
         "4th house = land, domestic stability, agriculture. 10th house = government, leadership.",
         "eclipse_4th_10th_house", "national_disruption"),
        ("mundane-raphael-ch25-eclipse-duration",
         "ECLIPSE DURATION RULE: A solar eclipse's effects last 1 year per hour of totality. "
         "A lunar eclipse's effects last 1 month per hour. "
         "Short eclipses = acute short events. Long eclipses = prolonged national challenges.",
         "eclipse_duration_rule", "effect_duration"),
        ("mundane-raphael-ch25-eclipse-forerunner",
         "Eclipse alone is not the trigger — it is the FORERUNNER. "
         "The malefic planet that subsequently aspects the eclipse degree fires the actual event. "
         "Rule: Eclipse primes the zone; first malefic to aspect that zodiacal degree ignites the outcome.",
         "eclipse_forerunner_igniter", "causal_sequence"),
    ]

    for rule_id, detailed, sub, rule_type in eclipse_rules:
        r = _base(rule_id, f"LU_MA.eclipse.{sub}",
                  "mundane_eclipse", rule_type,
                  rule_id, detailed,
                  "Raphael", 23, ["raphael_west", "mehta_rao"], now)
        r["condition"] = {"condition_type": "eclipse_event",
                          "extra_cond": {"eclipse_key": sub}}
        rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# GROUP G — War & Geopolitical  (Mehta Ch 19 / Gopal Ch 8)
# ---------------------------------------------------------------------------

def build_group_g(now: str) -> list[dict]:
    rules = []

    war_rules = [
        ("mundane-mehta-ch19-rohini-gate",
         "ROHINI GATE — Primary war/famine threshold: "
         "Saturn or malefics transiting Rohini nakshatra (Taurus 10°–23°20') AND aspected by Mars "
         "= war or severe famine imminent. This is the single highest-confidence war indicator. "
         "Historical: WWI (1914-18), WWII (1939-45), 1971 Indo-Pak War all activated Rohini Gate.",
         "war_rohini_gate", 19, "mehta_rao"),

        ("mundane-mehta-ch19-destruction-scheme",
         "DESTRUCTION SCHEME — War prerequisite trigger: "
         "IF Saturn AND Mars AND Rahu all transit into mutual Vedha positions on the Sanghatta grid "
         "THEN Destruction_Scheme = TRUE. This is the foundational war axiom — when these three "
         "malefics 'meet and plan', large-scale conflict becomes near-certain.",
         "war_destruction_scheme", 19, "mehta_rao"),

        ("mundane-mehta-ch19-triple-affliction",
         "WAR TRIPLE AFFLICTION — Mandatory prerequisite: "
         "War requires ALL THREE to be simultaneously afflicted: "
         "(1) Lagna/Lagna lord of the national chart, "
         "(2) Both luminaries (Sun AND Moon), "
         "(3) 7th house or 7th lord (open enemies / war axis). "
         "Partial affliction = border friction only. Full triple affliction = declared war.",
         "war_triple_affliction", 19, "mehta_rao"),

        ("mundane-mehta-ch19-india-cancer-capricorn",
         "INDIA CRITICAL WAR AXIS — Cancer-Capricorn axis is MORE dangerous for India than "
         "the Taurus-Scorpio axis. Malefics afflicting India's Cancer-Capricorn axis = "
         "risk of national humiliation or territorial loss (validated: 1962 China war, 1971). "
         "Taurus-Scorpio axis = secondary war axis (validated: 1965 Pakistan war).",
         "war_india_axis", 19, "mehta_rao"),

        ("mundane-mehta-ch19-victory-monitor",
         "VICTORY MONITOR: IF malefics are in the 6th house (enemies defeated) AND "
         "the Lagna lord is in a Kendra (angular house) THEN despite heavy initial pressure "
         "the nation achieves victory in the conflict. "
         "Validated: 1965 war (Sun in own house Leo Kendra + Saturn as Yogakaraka) and "
         "1999 Kargil (3rd lord/neighbours in 6th in own sign = steel of nerves).",
         "war_victory_monitor", 19, "mehta_rao"),

        ("mundane-mehta-ch19-steel-of-nerves",
         "STEEL OF NERVES — IF the lord of the 3rd house (Neighbours/Adjacent enemies) "
         "occupies the 6th house (Attack/Conflict) in its OWN SIGN "
         "THEN the nation will exhibit 'steel of nerves': successfully repels aggression "
         "despite media/international pressure. Validated: 1999 Kargil operation.",
         "war_steel_of_nerves", 19, "mehta_rao"),

        ("mundane-gopal-ch8-212-rivalry",
         "2/12 LAGNA RIVALRY — Nations whose foundation chart Lagnas are in 2/12 relationship "
         "CANNOT maintain lasting peace. The 2nd/12th relationship creates permanent economic "
         "and territorial friction. "
         "Benchmark: India (Taurus) and Pakistan (Aries) are in 2/12 — "
         "Aries is 12th from Taurus; Taurus is 2nd from Aries. "
         "Any peace treaty between them will break down within 5 years (historically validated).",
         "geopolitical_212_rivalry", 8, "gopal_modern"),

        ("mundane-gopal-ch8-global-chaos",
         "GLOBAL CHAOS PROTOCOL — IF Saturn, Rahu, Mars, Ketu, AND Jupiter all occupy a "
         "single sign simultaneously THEN Result = 'Global Chaos Protocol'. "
         "Mass displacement, multiple simultaneous wars, and systemic institutional collapse occur.",
         "geopolitical_global_chaos", 8, "gopal_modern"),

        ("mundane-gopal-ch8-india-trika-axis",
         "INDIA TRIKA AXIS — Sun transiting Sagittarius, Aries, or Libra "
         "(= 8th, 12th, or 6th house of India's Independence Chart) "
         "activates India's national danger phase. "
         "These are India's Dusthana (harmful) houses — Sun here = national vulnerability window. "
         "Combine with other malefic transits for specific event prediction.",
         "geopolitical_india_trika", 8, "gopal_modern"),

        ("mundane-gopal-ch8-seismic-triad",
         "SEISMIC TRIAD — Saturn in Dhanus/Mesha + Rahu in Meena/Virgo + Jupiter in Simha/Rishaba "
         "simultaneously = Richter 6.0+ earthquake configuration. "
         "This three-planet configuration has historically preceded major seismic events "
         "in the Indian subcontinent.",
         "seismic_triad", 8, "gopal_modern"),

        ("mundane-gopal-ch8-war-perigee-veto",
         "WAR PERIGEE VETO — Mars at perigee (closest approach to Earth) = "
         "war risk rises to CRITICAL regardless of diplomatic treaties or ceasefires. "
         "Physical proximity of Mars amplifies its martial energy; "
         "conflicts that appeared resolved tend to re-ignite during Mars perigee.",
         "war_perigee_veto", 8, "gopal_modern"),

        ("mundane-mehta-ch19-7th-lord-6th",
         "INVASION GATE — IF 7th lord (enemy/war) is in the 6th house (borders) "
         "AND Mars is retrograde THEN serious border incursions or sudden military attack "
         "predicted. The 7th lord in 6th = enemy has entered the border zone. "
         "Retrograde Mars confirms escalation from friction to conflict.",
         "war_invasion_gate", 19, "mehta_rao"),

        ("mundane-mehta-ch19-national-trauma",
         "NATIONAL TRAUMA ALERT — IF Sun AND Moon are both afflicted by Saturn/Nodes "
         "AND the 8th house is simultaneously triggered in the national chart "
         "THEN the nation enters a period of intense agony and difficult government decisions. "
         "Does not necessarily mean war — can be economic collapse, assassination, or natural disaster.",
         "war_national_trauma", 19, "mehta_rao"),

        ("mundane-gopal-ch8-cluster-boss",
         "CLUSTER BOSS GOVERNANCE — IF 3+ planets occupy the 9th house of an oath-taking chart "
         "THEN the leader will not have full autonomy: 'Cluster Bosses' (coalition partners or "
         "external forces) will dominate decisions. Surprisingly stabilising — leader survives "
         "via compromise rather than assertion. Validated: Manmohan Singh 2004.",
         "governance_cluster_boss", 8, "gopal_modern"),

        ("mundane-gopal-ch8-sri-lanka-saturn-kataka",
         "Saturn entering Kataka (Cancer) = 3-year high-risk window for bloodshed and "
         "high-profile assassinations in Sri Lanka and neighboring island/coastal nations. "
         "Validated: Saturn-Cancer transit correlation with Sri Lanka civil war escalations.",
         "geopolitical_sri_lanka_saturn", 8, "gopal_modern"),
    ]

    for rule_id, detailed, sub, chap, book_id in war_rules:
        book_name = "Mehta/Rao" if book_id == "mehta_rao" else "Gopalakrishnan"
        r = _base(rule_id, f"LU_MA.war_geopolitical.{sub}",
                  "mundane_war_geopolitical", sub,
                  rule_id, detailed,
                  book_name, chap, [book_id, "gaur_aifas"], now)
        r["condition"] = {"condition_type": "geopolitical_indicator",
                          "extra_cond": {"indicator_key": sub}}
        rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# GROUP H — Seismic Engine  (Mehta Ch 11)
# ---------------------------------------------------------------------------

def build_group_h(now: str) -> list[dict]:
    rules = []

    seismic_rules = [
        ("mundane-mehta-ch11-bhuj-scale",
         "BHUJ SCALE EARTHQUAKE — IF Saturn and Jupiter are conjunct in Taurus "
         "AND the conjunction is aspected by Mars "
         "THEN Critical Disaster Warning: Major earthquake (Richter 6+) predicted in the "
         "nation whose 4th house falls in Taurus region or whose Lagna is Taurus. "
         "Validated: 2001 Gujarat/Bhuj earthquake (Saturn-Jupiter conjunction in Taurus aspected by Mars).",
         "seismic_bhuj_scale"),
        ("mundane-mehta-ch11-eclipse-nadir",
         "ECLIPSE NADIR TRIGGER — IF eclipse falls in a fixed sign (Taurus/Leo/Scorpio/Aquarius) "
         "AND planets in fixed signs are Rising, Setting, or on the Meridian/Nadir at eclipse moment "
         "THEN high probability of seismic activity within 3 months in that sign's geographic zone.",
         "seismic_eclipse_nadir"),
        ("mundane-mehta-ch11-scorpio-taurus-primary",
         "PRIMARY SEISMIC AXIS — Major transits or eclipses in Taurus or Scorpio = "
         "notoriously seismic sign placements. These two signs represent the Earth's primary "
         "fault-line axis in Vedic mundane theory. Any three-planet pile-up in Taurus or Scorpio "
         "= immediate seismic monitoring alert.",
         "seismic_taurus_scorpio_axis"),
        ("mundane-mehta-ch11-jupiter-mercury-friction",
         "JUPITER-MERCURY SEISMIC FRICTION — Jupiter in Taurus or Scorpio conjunct or "
         "opposed to Mercury = prolific source of earthquake activity. "
         "This specific two-planet configuration has repeatedly preceded earthquake sequences "
         "across India and Asia.",
         "seismic_jupiter_mercury"),
        ("mundane-mehta-ch11-cardinal-clustering",
         "CARDINAL CLUSTER ALARM — Concentration of 3+ planets in the first 10° of any "
         "cardinal sign (Aries/Cancer/Libra/Capricorn) = high friction index. "
         "Combine with eclipse proximity for seismic risk assessment.",
         "seismic_cardinal_cluster"),
        ("mundane-mehta-ch11-aries-ingress-4th-8th",
         "ANNUAL SEISMIC AUDIT — IF the Aries Ingress chart (annual solar chart) shows "
         "affliction to BOTH the 4th house (Land) AND the 8th house (Mass Death) simultaneously "
         "THEN the year carries elevated earthquake risk for the nation in question.",
         "seismic_aries_ingress_dual"),
        ("mundane-mehta-ch11-tsunami-vector",
         "TSUNAMI VECTOR — IF retrograde Saturn or Rahu occupies a Kendra (angular house) "
         "AND Mars or Moon is in a watery sign (Cancer/Scorpio/Pisces) "
         "THEN maritime hazard: high probability of undersea earthquake and subsequent tsunami.",
         "seismic_tsunami_vector"),
        ("mundane-mehta-ch11-indra-circle-leaders",
         "INDRA CIRCLE CASUALTY — IF earthquake occurs when Moon or Sun is in an Indra-circle "
         "nakshatra (Abhijit/Shravan/Dhanishtha/Rohini/Jyeshtha/Uttarashadh/Anuradha) "
         "THEN quake likely results in death of 'celebrated men' or national leaders "
         "in addition to property damage and mass casualties.",
         "seismic_indra_circle"),
        ("mundane-mehta-ch11-rasi-sandhi",
         "RASI SANDHI SEISMIC INSTABILITY — Major malefics at sign junctions (0° or 29° of any sign) "
         "create a 'double transit' instability. If Jupiter is at end of one sign and Venus at "
         "beginning of another simultaneously, the resulting friction amplifies seismic risk.",
         "seismic_rasi_sandhi"),
        ("mundane-mehta-ch11-forerunner-igniter",
         "SEISMIC CAUSAL SEQUENCE — Eclipse alone does NOT cause earthquakes. "
         "Eclipse = forerunner (primes the zone). First malefic to aspect the eclipse degree "
         "= igniter (fires the actual event). "
         "Always identify the eclipse degree AND track subsequent malefic aspects to it.",
         "seismic_forerunner_igniter"),
        ("mundane-mehta-ch11-mercury-saturn-timing",
         "SEISMIC TIMING MARKER — Mercury-Saturn interconnection (conjunction, opposition, or "
         "mutual aspect) OR Mercury moving behind the Sun (combust approaching) = "
         "key temporal marker for upcoming seismic event within 30 days.",
         "seismic_mercury_saturn_timing"),
        ("mundane-mehta-ch11-eclipse-longitude-overlap",
         "GEOGRAPHIC PRECISION — Eclipse longitude that overlaps with the ruling sign/longitude "
         "of a specific city or region refines the earthquake 'where'. "
         "Cross-reference eclipse degree against Koorma Chakra zone nakshatras for directional precision.",
         "seismic_eclipse_longitude"),
    ]

    for rule_id, detailed, sub in seismic_rules:
        r = _base(rule_id, f"LU_MA.seismic.{sub}",
                  "mundane_seismic", sub,
                  rule_id, detailed,
                  "Mehta/Rao", 11, ["mehta_rao", "gaur_aifas"], now)
        r["condition"] = {"condition_type": "seismic_indicator",
                          "extra_cond": {"seismic_key": sub}}
        rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# GROUP I — Governance & Election  (Gopal Ch 4/5 / Mehta Ch 18)
# ---------------------------------------------------------------------------

def build_group_i(now: str) -> list[dict]:
    rules = []

    governance_rules = [
        ("mundane-gopal-ch4-election-10th-lord",
         "ELECTION WINNER RULE — The candidate with the HIGHER frequency of 10th lord strength "
         "across three reference points (Lagna, Chandra Lagna, Karkamsha Lagna) wins the election. "
         "Count each reference: 10th lord in angle/trine = 1 point. Candidate with more points wins. "
         "This is Gopalakrishnan's core election prediction metric.",
         "election_10th_lord_strength", 4, "gopal_modern"),

        ("mundane-gopal-ch5-jaimini-long-life",
         "JAIMINI LONGEVITY — LONG LIFE: Both Lagna lord AND 8th lord in MOVING signs "
         "(Aries, Cancer, Libra, Capricorn). "
         "Applied to national leaders and nations: moving-sign placements = sustained tenure.",
         "election_jaimini_long_life", 5, "gopal_modern"),

        ("mundane-gopal-ch5-jaimini-short-life",
         "JAIMINI LONGEVITY — SHORT LIFE: Both Lagna lord AND 8th lord in FIXED signs "
         "(Taurus, Leo, Scorpio, Aquarius). "
         "Counter-intuitive: fixed signs = short political life despite apparent stability.",
         "election_jaimini_short_life", 5, "gopal_modern"),

        ("mundane-gopal-ch5-jaimini-medium-life",
         "JAIMINI LONGEVITY — MEDIUM LIFE: Both Lagna lord AND 8th lord in DUAL signs "
         "(Gemini, Virgo, Sagittarius, Pisces). "
         "Medium-life leaders: complete partial terms, transition mid-mandate, or serve coalition roles.",
         "election_jaimini_medium_life", 5, "gopal_modern"),

        ("mundane-mehta-ch18-simhasan-war-gate",
         "SIMHASAN WAR GATE — IF Moon in oath chart falls in Simha Nadi (Rohini, Ardra, Hasta, Swati, "
         "Shravan, Shatbhisha) AND conjunct Mars THEN the leader will be like a lion — "
         "decisive military king who leads the nation into territorial conflict. "
         "Validated: Lal Bahadur Shastri 1965 oath chart.",
         "governance_simhasan_war", 18, "mehta_rao"),

        ("mundane-mehta-ch18-short-cabinet",
         "SHORT-LIFE CABINET — IF Lagna lord of oath chart is in 8th house "
         "AND 10th lord is displaced to 12th house "
         "THEN cabinet collapses or resigns within first 12 months. "
         "Validated: Chandrashekhar 1990 — resigned within 7 months.",
         "governance_short_cabinet", 18, "mehta_rao"),

        ("mundane-mehta-ch18-fixed-lagna-stability",
         "FIXED SIGN STABILITY RULE — Oath chart must have a fixed sign Lagna "
         "(Taurus/Leo/Scorpio/Aquarius) for government longevity. "
         "Moving sign = short-lived cabinet. Dual sign = coalition, moderate duration. "
         "This is the SINGLE MOST IMPORTANT Lagna selection criterion for oath timing.",
         "governance_fixed_lagna", 18, "mehta_rao"),

        ("mundane-mehta-ch18-8th-house-veto",
         "8TH HOUSE VETO — The 8th house of the oath chart MUST be vacant. "
         "Any malefic in the 8th (especially Mars) = severe governance trouble or "
         "death/sudden removal of the leader in office. "
         "Validated: Shastri (Mars-afflicted 8th) died in office; Vajpayee 1996 (Saturn+Ketu in 8th) "
         "resigned in 13 days.",
         "governance_8th_house_veto", 18, "mehta_rao"),

        ("mundane-mehta-ch18-raman-libra-rule",
         "RAMAN LIBRA RULE — Libra Lagna aspected by Jupiter in an oath chart "
         "= optimal governance marker for a democratic Head of State. "
         "Leader receives maximum protection and achieves policy goals. "
         "Aquarius Lagna with Saturn in dignity = sustainable democracy alternative.",
         "governance_raman_libra", 18, "mehta_rao"),

        ("mundane-mehta-ch18-cancer-leo-coalition-discord",
         "COALITION DISCORD TRAP — Rising Cancer or Leo Lagna in oath chart "
         "= perpetual coalition bickering because Saturn becomes the 7th lord (Partners). "
         "Saturn = delays, obstruction, enmity — as coalition lord, it guarantees partner betrayal. "
         "Never choose Cancer or Leo for coalition government oath timing.",
         "governance_coalition_discord", 18, "mehta_rao"),

        ("mundane-mehta-ch18-lagna-lord-stronger",
         "LONGEVITY MATHEMATICS — IF Lagna lord's Ashtakvarga bindu score > 8th lord's bindu score "
         "AND Lagna lord is not in 6th/8th/12th THEN government achieves mandate completion. "
         "IF 8th lord is stronger than Lagna lord (as in Mulayam-Mayawati case) = early collapse.",
         "governance_longevity_math", 18, "mehta_rao"),

        ("mundane-mehta-ch18-lagna-lord-afflicted-death",
         "LEADERSHIP DEATH IN OFFICE — IF Lagna lord of oath chart is afflicted by Mars "
         "AND 12th lord occupies 10th house "
         "THEN leader faces terminal risk — high probability of dying in office or "
         "mysterious removal (not electoral defeat). "
         "Validated: Lal Bahadur Shastri 1964 oath chart.",
         "governance_leader_death", 18, "mehta_rao"),

        ("mundane-mehta-ch18-corruption-nexus",
         "CORRUPTION NEXUS — IF Venus (communications/trade) is afflicted by Saturn AND Mars "
         "in the oath chart THEN governance will be marred by high-level bribery, "
         "communications or trade scandals. "
         "Validated: Narasimha Rao's Urea and Mehta (Harshad Mehta) securities scam during his tenure.",
         "governance_corruption_nexus", 18, "mehta_rao"),

        ("mundane-mehta-ch18-economic-liberalization",
         "ECONOMIC LIBERALIZATION SIGNAL — IF the 2nd, 5th, AND 11th lords form a connection "
         "(conjunction, mutual aspect, or exchange) in the oath chart "
         "THEN the administration will oversee major national economic liberalization: "
         "foreign investment, market reform, sustained GDP growth. "
         "Validated: Narasimha Rao 1991 — economic reforms despite minority government.",
         "governance_liberalization", 18, "mehta_rao"),

        ("mundane-mehta-ch18-capricorn-exclusion",
         "CAPRICORN EXCLUSION RULE — Capricorn is NOT recommended as oath-taking Lagna "
         "because: (1) it is a movable/Cardinal sign (short life), "
         "(2) inherent enmity between lord Saturn and 7th lord Moon creates coalition friction. "
         "Avoid Capricorn for both democratic elections and coalition oath ceremonies.",
         "governance_capricorn_exclusion", 18, "mehta_rao"),

        ("mundane-mehta-ch18-bharani-krittika-veto",
         "STELLAR SABOTAGE VETO — If the oath-taking nakshatra is Bharani (presided by Yama/Death) "
         "or Krittika (presided by Agni/Fire) = administration ends violently or in disgrace. "
         "Validated: Vajpayee 1996 oath in Bharani — resigned in 13 days. "
         "Never schedule swearing-in ceremony in Bharani or Krittika.",
         "governance_bharani_krittika", 18, "mehta_rao"),
    ]

    for rule_id, detailed, sub, chap, book_id in governance_rules:
        book_name = "Gopalakrishnan" if book_id == "gopal_modern" else "Mehta/Rao"
        r = _base(rule_id, f"LU_MA.governance.{sub}",
                  "mundane_governance", sub,
                  rule_id, detailed,
                  book_name, chap, [book_id, "mehta_rao"], now)
        r["condition"] = {"condition_type": "governance_indicator",
                          "extra_cond": {"governance_key": sub}}
        rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# GROUP J — Historical Validation  (Mehta Ch 19/21 / Gopal Ch 14)
# ---------------------------------------------------------------------------

def build_group_j(now: str) -> list[dict]:
    rules = []

    validation_records = [
        ("mundane-hist-china-war-1962",
         "HISTORICAL VALIDATION — China War 1962: "
         "Saturn and Ketu conjunct in Capricorn at 11°; Mars in Cancer fully aspected Saturn/Ketu "
         "on October 20, 1962 → outbreak of war with China. "
         "India's Cancer-Capricorn war axis activated. National humiliation followed. "
         "Signature: 7th lord (Sun) and Lagna lord (Venus) both afflicted in 6th house (borders).",
         "hist_china_1962"),

        ("mundane-hist-pakistan-war-1965",
         "HISTORICAL VALIDATION — Pakistan War 1965: "
         "Lagna afflicted by Rahu and Mars; 7th house afflicted by Ketu and Saturn. "
         "Sun in own house Leo (Kendra) and Saturn as Yogakaraka = India's VICTORY despite aggression. "
         "Taurus-Scorpio axis (secondary war axis) activated.",
         "hist_pakistan_1965"),

        ("mundane-hist-pakistan-war-1971",
         "HISTORICAL VALIDATION — Pakistan War 1971 / Birth of Bangladesh: "
         "Saturn retrograde in Rohini (Taurus 13°) + Mars in Aquarius aspecting Saturn = "
         "Rohini Gate activated. Luminaries afflicted by Saturn and 8th lord Mercury. "
         "Outcome: dismemberment of Pakistan, birth of Bangladesh.",
         "hist_pakistan_1971"),

        ("mundane-hist-kargil-1999",
         "HISTORICAL VALIDATION — Kargil War 1999: "
         "Mars-Saturn opposition in 1/7 axis of Hindu New Year chart. "
         "3rd lord (Neighbours) in 6th house (Attack) in own sign = 'Steel of Nerves' — "
         "India repelled aggression successfully. Operation Vijay validated the Steel of Nerves rule.",
         "hist_kargil_1999"),

        ("mundane-hist-indira-gandhi-1984",
         "HISTORICAL VALIDATION — Assassination of Indira Gandhi (Oct 31, 1984): "
         "LUMINARY SIEGE: Sun and Moon both afflicted by Saturn in Annual Chart. "
         "10th house (Prime Minister): malefic Sun aspected by Saturn. "
         "10th lord Moon in 5th aspected by Mars and 8th lord Venus. "
         "No benefics in Kendras. Rahu-Ketu in 2/8 axis afflicting 8th house and India's Lagna lord. "
         "New Moon (Oct 24, 1984): occurred in 7th house (death), luminaries under Saturn siege.",
         "hist_indira_gandhi_1984"),

        ("mundane-hist-rajiv-gandhi-1991",
         "HISTORICAL VALIDATION — Assassination of Rajiv Gandhi (May 21, 1991): "
         "INFILTRATION GATE: Mars in 12th house of Hindu New Year (1991) = terrorists inside borders. "
         "DIRECTIONAL RULE: Mars in Taurus (South sign) → threat from SOUTH (LTTE/Tamil Tigers). "
         "EXPLOSION MULTIPLIER: Mars in 12th aspected by Rahu = suicide bombing (coefficient 0.98). "
         "GENDER MARKER: Venus in 12th Mars configuration = female assassin. All four rules validated.",
         "hist_rajiv_gandhi_1991"),

        ("mundane-hist-mahatma-gandhi-1948",
         "HISTORICAL VALIDATION — Assassination of Mahatma Gandhi (Jan 30, 1948): "
         "PRIMARY TRIGGER: Saturn transiting natal Moon (Sadhe-Sati) and natal Rahu simultaneously. "
         "WEAPON MARKER: Mars prominent in the natal and transit = martyrdom via firearm. "
         "LUMINARY SIEGE: Sun and Moon both afflicted by malefics in transit chart of assassination day.",
         "hist_mahatma_gandhi_1948"),

        ("mundane-hist-bhuj-earthquake-2001",
         "HISTORICAL VALIDATION — Bhuj Earthquake, Gujarat (Jan 26, 2001): "
         "Saturn and Jupiter CONJUNCT in Taurus, aspected by Mars = Bhuj-Scale trigger. "
         "India's 4th house = land/property in Taurus zone. "
         "Result: Richter 7.7 earthquake, 20,000+ deaths. "
         "Seismic 16-factor checklist: Taurus-Scorpio axis (Factor 4), "
         "Jupiter-Mercury friction (Factor 5), Eclipse proximity (Factor 1) all active.",
         "hist_bhuj_2001"),

        ("mundane-hist-sensex-2006",
         "HISTORICAL VALIDATION — Sensex Bull Run 2006: "
         "Saturn in Pushya nakshatra (Cancer) → Sensex rose from 6,000 to 12,000+ (100% gain). "
         "Sector winners: Banking, IT, FMCG, Telecom. "
         "BPO/IT boom DESPITE all media predictions of failure — Saturn in India's 3rd house. "
         "Pushya Bull Rule validated.",
         "hist_sensex_2006"),

        ("mundane-hist-south-cms-2006",
         "HISTORICAL VALIDATION — South Indian CM Replacements 2006: "
         "Mars at perigee (closest to Earth) + Mars in Fixed Sign → "
         "ALL major South Indian Chief Ministers replaced simultaneously: "
         "Jayalalitha (Tamil Nadu), Oommen Chandy (Kerala), Dharam Singh (Karnataka). "
         "South Leadership Veto Rule validated: Mars direction = South → incumbency failure.",
         "hist_south_cms_2006"),

        ("mundane-hist-jfk-1963",
         "HISTORICAL VALIDATION — Assassination of JFK (Nov 22, 1963): "
         "GLOBAL GOLD STANDARD — JFK's chart: Lagna lord Mercury + 8th lord Mars conjunct "
         "in 8th house, aspected by 6th lord Saturn = Terminal Assassination Signature. "
         "This is the engine's benchmark for physical leadership strikes globally. "
         "Proves Vedic mundane principles apply outside Indian context.",
         "hist_jfk_1963"),

        ("mundane-hist-lal-bahadur-shastri-1966",
         "HISTORICAL VALIDATION — Death of Lal Bahadur Shastri (Jan 11, 1966, Tashkent): "
         "FOREIGN SOIL MARKER: Hindu New Year 1965: 10th lord Jupiter in Node axis; "
         "12th house afflicted by Saturn + Mars in 6th (enemies abroad). "
         "Shastri died in Tashkent under mysterious circumstances — Foreign Soil Veto validated. "
         "Chidra Dasha: Mercury/Mercury/Moon = exit period.",
         "hist_shastri_1966"),

        ("mundane-hist-ganguly-sachin-2006",
         "HISTORICAL VALIDATION — Ganguly/Sachin Career Decline 2006: "
         "NADI RULE: Saturn transiting 8th nakshatra from natal Jupiter = "
         "sudden sustained poor form and career break for elite performers. "
         "Both Sourav Ganguly and Sachin Tendulkar experienced form slumps timed precisely "
         "by this Nadi transit rule. Career fall rule validated for individual elite performers.",
         "hist_ganguly_sachin_2006"),
    ]

    for rule_id, detailed, sub in validation_records:
        r = _base(rule_id, f"LU_MA.historical_validation.{sub}",
                  "historical_validation", "empirical_case_study",
                  rule_id, detailed,
                  "Mehta/Rao", 19, ["mehta_rao", "gopal_modern", "gaur_aifas"], now)
        r["condition"] = {"condition_type": "historical_validation",
                          "extra_cond": {"case_ref": sub, "checkable_note": (
                              "Historical validation — chart data fixed to historical dates. "
                              "Use for engine calibration and pattern recognition, not live prediction.")}}
        rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# GROUP K — Hazard & Special Rules  (Mehta Ch 21 / Gopal Ch 8)
# ---------------------------------------------------------------------------

def build_group_k(now: str) -> list[dict]:
    rules = []

    hazard_rules = [
        ("mundane-mehta-ch21-luminary-siege",
         "LUMINARY SIEGE RULE — MANDATORY BASE CONDITION for any assassination prediction: "
         "On the day of the assassination, BOTH the Sun AND the Moon MUST be afflicted "
         "by malefics in transit. If only one luminary is afflicted = serious threat but "
         "not assassination. Both afflicted = assassination event confirmed.",
         "hazard_luminary_siege"),
        ("mundane-mehta-ch21-10th-saturn-affliction",
         "PM JEOPARDY GATE — IF Annual 10th House is afflicted by Sun/Saturn "
         "AND Luminaries are in Node axis "
         "THEN Critical National Security Alert: high probability of violent change in "
         "central leadership. Coefficient: 0.85. Validated: 1984 Indira Gandhi case.",
         "hazard_pm_jeopardy"),
        ("mundane-mehta-ch21-infiltration-gate",
         "INFILTRATION GATE — IF Mars occupies the 12th house of the Hindu New Year chart "
         "THEN terrorists/assassins have entered the country for secret intrigue. "
         "The sign of Mars identifies the direction of infiltration: "
         "Mars in Taurus = South; Aries = East; Capricorn = North; Cancer = West. "
         "Mars in 12th + aspected by Rahu = explosive/suicide attack method (coefficient 0.98).",
         "hazard_infiltration_gate"),
        ("mundane-mehta-ch21-religious-leader-hazard",
         "RELIGIOUS LEADER HAZARD — IF Jupiter (religion karaka) is afflicted by Saturn + Rahu + Mars simultaneously "
         "AND 9th lord is in 8th house "
         "THEN Critical Threat: high probability of assassination of a religious head or "
         "communal icon, leading to riots. "
         "Validated: Baba Gurbachan Singh assassination 1980 — Aries Ingress chart audit.",
         "hazard_religious_leader"),
        ("mundane-mehta-ch21-mystery-plot",
         "MYSTERY PLOT MONITOR — IF the leader is in Chidra Dasha (final sub-period) "
         "AND Mars + Rahu occupy the 12th house "
         "THEN Intelligence Warning: sudden and mysterious end of the leader predicted; "
         "foreign intrigue or poisoning likely. "
         "Validated: Lal Bahadur Shastri — Chidra Dasha Mercury/Mercury/Moon, Tashkent 1966.",
         "hazard_mystery_plot"),
        ("mundane-mehta-ch21-army-coup-saturn-10th",
         "ARMY COUP SIGNATURE — IF Saturn occupies the 10th house of the national leader's chart "
         "AND the 7th house (war/enemies) is aspected by BOTH retrograde Mars AND retrograde Saturn "
         "THEN Army Coup or violent overthrow of the government predicted. "
         "Saturn in 10th = sudden rise followed by terminal fall. "
         "Validated: Sheikh Mujiburrahman 1975.",
         "hazard_army_coup"),
        ("mundane-mehta-ch21-female-assassin",
         "ASSASSIN IDENTIFICATION MARKER — IF Mars is in the 12th house of an ingress/lunation chart "
         "AND Venus is ALSO in the 12th house (conjunct or in same sign as Mars) "
         "THEN the attack will likely involve: (a) an explosive device and/or (b) a female perpetrator. "
         "Validated: Rajiv Gandhi assassination — Venus + Mars in 12th confirmed female bomber.",
         "hazard_female_assassin"),
        ("mundane-mehta-ch21-new-moon-7th",
         "TEMPORAL IGNITION — IF New Moon occurs in the 7th house of the national chart "
         "AND the 8th house is afflicted by Nodes "
         "THEN Fortnightly Stability Alert: violent leadership transition or national tragedy "
         "predicted within 14 days of that New Moon.",
         "hazard_new_moon_7th"),
        ("mundane-gopal-ch8-decentralized-terror",
         "DECENTRALIZED TERROR VETO — When Saturn is in the 12th house of the national coronation chart "
         "security forces must focus on 'spies and secret foes' rather than a standing army. "
         "Terrorism has moved from chain-of-command to cellular operations (Bin Laden model). "
         "Traditional military doctrine insufficient; intelligence-led approach required.",
         "hazard_decentralized_terror"),
        ("mundane-mehta-ch21-12th-house-congestion",
         "12TH HOUSE CONGESTION ALERT — IF 4+ planets cluster in the 12th house of a Solar Ingress chart "
         "THEN Maximum Infiltration Alert: multiple specialized enemy assets have entered the country "
         "for a coordinated strike. National security at highest risk level. "
         "Validated: Rajiv Gandhi — Sun, Moon, Mercury, Venus, Rahu ALL in 12th of Sun-Taurus ingress.",
         "hazard_12th_congestion"),
        ("mundane-mehta-ch21-double-10th-lord-hit",
         "TERMINAL REMOVAL SIGNATURE — IF Mars afflicts the 10th lord (threat to leader's body) "
         "AND the 8th lord (death lord) further afflicts the same 10th lord "
         "THEN Terminal Assassination predicted — both the threat instrument (Mars) and the "
         "death force (8th lord) target the leader simultaneously. "
         "Validated: Rajiv Gandhi 1991 Sun-Taurus ingress.",
         "hazard_double_10th_hit"),
        ("mundane-gopal-ch14-pushya-bull-refinement",
         "PUSHYA BULL RUN REFINEMENT — Pushya Bull Run is most powerful when COMBINED with "
         "India being in Mercury or Venus Mahadasha/Bhukti in its national dasha. "
         "IF (Saturn in Pushya) AND (India in Mercury/Venus/Rahu period) "
         "THEN maximum equity index growth: 50-100% gain within 12-18 months. "
         "Validated: 2006 confluence of Saturn-Pushya + India's Mercury Bhukti.",
         "hazard_pushya_refinement"),
    ]

    for rule_id, detailed, sub in hazard_rules:
        chap = 14 if "ch14" in rule_id else (8 if "ch8" in rule_id else 21)
        book = "Gopalakrishnan" if "gopal" in rule_id else "Mehta/Rao"
        book_id = "gopal_modern" if "gopal" in rule_id else "mehta_rao"
        r = _base(rule_id, f"LU_MA.hazard.{sub}",
                  "mundane_hazard", sub,
                  rule_id, detailed,
                  book, chap, [book_id, "mehta_rao"], now)
        r["condition"] = {"condition_type": "hazard_indicator",
                          "extra_cond": {"hazard_key": sub}}
        rules.append(r)

    return rules


# ---------------------------------------------------------------------------
# Aggregate
# ---------------------------------------------------------------------------

def build_all(now: str) -> list[dict]:
    rules = []
    rules.extend(build_group_a(now))   # A: Global Tone
    rules.extend(build_group_b(now))   # B: Celestial Council
    rules.extend(build_group_c(now))   # C: Agricultural
    rules.extend(build_group_d(now))   # D: Koorma Directional
    rules.extend(build_group_e(now))   # E: Transit Key
    rules.extend(build_group_f(now))   # F: Eclipse
    rules.extend(build_group_g(now))   # G: War & Geopolitical
    rules.extend(build_group_h(now))   # H: Seismic
    rules.extend(build_group_i(now))   # I: Governance
    rules.extend(build_group_j(now))   # J: Historical Validation
    rules.extend(build_group_k(now))   # K: Hazard & Special
    return rules


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--save",     help="Path to write JSON")
    parser.add_argument("--upload",   help="Path to JSON for upload")
    parser.add_argument("--mongo-url")
    parser.add_argument("--db-name",  default="horoscope_db")
    args = parser.parse_args()

    now   = datetime.now(timezone.utc).isoformat()
    rules = build_all(now)

    if args.dry_run or args.save:
        by_group: dict[str, int] = {}
        for r in rules:
            st = r["metadata"]["sub_type"]
            by_group[st] = by_group.get(st, 0) + 1

        print(f"Built {len(rules)} rules for batch {BATCH_ID}")
        print(f"Collection: interpretation_rules  |  science: {SCIENCE}\n")
        print("Breakdown by sub_type:")
        for st, count in sorted(by_group.items()):
            print(f"  {st:<40}: {count}")
        print(f"\nTotal: {len(rules)}")
        print("\nRule IDs:")
        for r in rules:
            print(f"  {r['rule_id']}")

        if args.save:
            with open(args.save, "w") as f:
                json.dump(rules, f, indent=2, default=str)
            print(f"\nSaved → {args.save}")
        print("\nDry run complete.")
        return

    if args.upload:
        if not args.mongo_url:
            raise SystemExit("ERROR: --mongo-url is required with --upload")
        with open(args.upload) as f:
            rules = json.load(f)

        client   = MongoClient(args.mongo_url)
        col      = client[args.db_name]["interpretation_rules"]
        inserted = updated = 0
        for rule in rules:
            result = col.update_one(
                {"rule_id": rule["rule_id"]},
                {"$set":    rule},
                upsert=True,
            )
            if result.upserted_id:
                inserted += 1
            elif result.modified_count:
                updated += 1
        print(f"Loaded {len(rules)} rules from {args.upload}")
        print(f"Inserted {inserted} / Updated {updated} → {args.db_name}.interpretation_rules")
        client.close()


if __name__ == "__main__":
    main()
