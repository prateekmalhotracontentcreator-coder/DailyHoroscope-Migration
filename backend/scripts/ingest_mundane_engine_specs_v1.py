#!/usr/bin/env python3
"""
ingest_mundane_engine_specs_v1.py

Mundane Astrology — Procedural Engine Specifications
BATCH_ID: mundane-engine-v1-20260505
TARGET COLLECTION: horoscope_db.mundane_engine_specs

15 spec documents — procedural engines that COMPUTE values (not interpretable rules):

  1.  mehta-9-step-scheme          — Mehta Ch 2: 9-Step Multi-Layer Prediction Scheme
  2.  gaur-celestial-council       — Gaur Ch 2: Annual Cabinet Role Appointments
  3.  gaur-cloud-engine            — Gaur Ch 2: Cloud/Rain formula (Shak Samvat × 8 / 9)
  4.  gaur-snake-engine            — Gaur Ch 2: Geopolitical friction formula ((Shak+2)/12)
  5.  gaur-samvat-stambha          — Gaur Ch 2: 4-Pillar Stambha calculation
  6.  gaur-sanghatta-vedha-matrix  — Gaur Ch 6: Rashi Vedha vectors (12 signs × 3 directions)
  7.  mehta-simhasan-chakra        — Mehta Ch 18: 5-Level Nakshatra authority grid
  8.  mehta-5yr-dasha-table        — Mehta Ch 18: Compressed Vimshottari for governance
  9.  gaur-transit-temporal-sun    — Gaur Ch 10: Sun transit commodity lookup
  10. gaur-transit-temporal-moon   — Gaur Ch 10: Moon transit commodity lookup
  11. gaur-sun-ingress-weekday     — Gaur Ch 10: Sun Sankranti weekday modifiers
  12. gopal-industrial-sector      — Gopal Ch 14: Planetary transit → sector performance
  13. gaur-sarvatobhadra-trade     — Gaur Ch 8/10: SBC Vedha → commodity price engine
  14. mehta-assassination-engine   — Mehta Ch 21: Hazard module diagnostic protocol
  15. mehta-seismic-16factors      — Mehta Ch 11: 16-factor earthquake checklist

Schema decisions (Q13 — School A, locked):
  - These are PROCEDURAL SPECS — not interpretation rules.
  - Collection: mundane_engine_specs  (separate from interpretation_rules)
  - The KE calls these specs to COMPUTE values; interpretation_rules interprets results.
  - science: "mundane_jyotish"
  - spec_id is the primary key (upsert key for upload)
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pymongo import MongoClient

SCIENCE   = "mundane_jyotish"
BATCH_ID  = "mundane-engine-v1-20260505"
COLL_NAME = "mundane_engine_specs"

# ── SPEC DATA ─────────────────────────────────────────────────────────────────

ENGINE_SPECS = [

    # ── 1. Mehta 9-Step Multi-Layer Prediction Scheme ─────────────────────────
    {
        "spec_id":    "mehta-9-step-scheme",
        "spec_type":  "procedural_scheme",
        "title":      "Mehta 9-Step Multi-Layer Mundane Prediction Scheme",
        "source_book": "Mehta/Rao",
        "source_chapter": "Mehta Ch 2",
        "description": (
            "The foundational 9-step evaluation protocol for annual mundane prediction. "
            "Each step is a separate chart/analysis layer; later steps refine earlier ones. "
            "Outputs from all 9 steps are synthesized for the final forecast. "
            "The protocol MUST be run in order — later steps depend on earlier baselines."
        ),
        "spec_data": {
            "step_1": {
                "name": "Foundation Horoscope",
                "description": "National DNA chart — cast for the moment of nation's independence/founding.",
                "purpose": "Establishes the nation's permanent planetary strengths, weaknesses, and karmic patterns.",
                "repeat": "Once per nation — does not change year to year.",
            },
            "step_2": {
                "name": "New Year Chart (Chaitra Shukla Pratipada)",
                "description": "Annual Hindu New Year chart cast for each country's capital.",
                "purpose": "Sets the annual theme — Celestial Cabinet is appointed from this chart.",
                "repeat": "Annually (Chaitra Shukla Pratipada = first day of Hindu new year).",
            },
            "step_3": {
                "name": "Surya Veedhi (Sun Transit Path)",
                "description": "Sun's transit through the 12 signs tracked with weekday-ingress filters.",
                "purpose": "Monthly commodity and weather triggers (Sankranti logic).",
                "repeat": "12 times per year (once per solar ingress).",
            },
            "step_4": {
                "name": "Paksha Charts (Fortnight Charts)",
                "description": "New Moon and Full Moon charts cast for each fortnight.",
                "purpose": "14-day event windows — assassination, flood, drought triggers.",
                "repeat": "26 times per year.",
            },
            "step_5": {
                "name": "Eclipses",
                "description": "Solar and Lunar eclipse charts analyzed by decanate and house.",
                "purpose": "Major long-duration triggers (eclipse effects last 3–36 months).",
                "repeat": "Variable (2–5 eclipses per year).",
            },
            "step_6": {
                "name": "Standard Planetary Transits",
                "description": "Saturn, Jupiter, Mars, Rahu/Ketu sign changes tracked.",
                "purpose": "Medium-term trend shifts (months to years).",
                "repeat": "Per significant transit change.",
            },
            "step_7": {
                "name": "Specialized Chakras",
                "description": "Koorma, Sanghatta, Sarvatobhadra, Simhasan Chakras applied.",
                "purpose": "Geographic and authority-specific precision layer.",
                "repeat": "As needed per forecast question.",
            },
            "step_8": {
                "name": "Occasional Conjunctions",
                "description": "Rare planetary conjunctions (Saturn-Mars, Jupiter-Saturn mutations).",
                "purpose": "Historical mega-events — wars, regime changes, generational shifts.",
                "repeat": "Per occurrence (Saturn-Mars every 2 years; Jupiter-Saturn every 20 years).",
            },
            "step_9": {
                "name": "Annual Varshaphala (Foundation Chart Dasha)",
                "description": "5-Year Compressed Vimshottari Dasha applied to the national foundation chart.",
                "purpose": "Identifies the 'policy lifespan' — which sub-period drives current events.",
                "repeat": "Annually for each nation.",
                "dasha_compression_ratio": "1:120 (1 year = 120 Vimshottari years compressed to 5)",
            },
        },
        "synthesis_sources": ["mehta_rao"],
    },

    # ── 2. Gaur Celestial Council Appointment Logic ───────────────────────────
    {
        "spec_id":    "gaur-celestial-council",
        "spec_type":  "appointment_protocol",
        "title":      "Gaur Annual Celestial Cabinet Appointment Protocol",
        "source_book": "Gaur/AIFAS",
        "source_chapter": "Gaur Ch 2",
        "description": (
            "10 annual cabinet roles assigned to planets based on the weekday lord "
            "at specific solar/lunar ingress events. Once assigned, each planet's "
            "natural significations determine the outcome for that domain in the year. "
            "Afflicted planet in a role = trouble in that domain."
        ),
        "spec_data": {
            "roles": {
                "king":         {"appointed_by": "Weekday lord at Chaitra Shukla Pratipada", "domain": "Overall ruler of the year — national power, king/head of state"},
                "minister":     {"appointed_by": "Weekday lord at Sun's Aries ingress", "domain": "Policy, administration, prime minister equivalent"},
                "sasyesh":      {"appointed_by": "Weekday lord at Sun's Cancer ingress", "domain": "Summer crops — governs agricultural output Jun–Sep"},
                "meghesh":      {"appointed_by": "Weekday lord at Sun's Ardra nakshatra entry", "domain": "Weather/rain secretary — governs monsoon and rainfall"},
                "durgesh":      {"appointed_by": "Weekday lord at Sun's Leo ingress", "domain": "Defence/military — national security and borders"},
                "rasesh":       {"appointed_by": "Weekday lord at Sun's Libra ingress", "domain": "Juices/liquids — water resources, beverages, dairy"},
                "neersesh":     {"appointed_by": "Weekday lord at Sun's Capricorn ingress", "domain": "Water supply — rivers, floods, drought"},
                "dhanesh":      {"appointed_by": "Weekday lord at Sun's Taurus ingress", "domain": "Finance/treasury — national economy and wealth"},
                "phalesh":      {"appointed_by": "Weekday lord at Sun's Gemini ingress", "domain": "Fruits/harvest — crop yield and food abundance"},
                "dhanyesh":     {"appointed_by": "Weekday lord at Sun's Virgo ingress", "domain": "Grains — wheat, rice, cereal production"},
            },
            "interpretation_key": {
                "Sun":     "Authority, kings, leaders — strong = stable governance; afflicted = leadership crisis",
                "Moon":    "Public mood, water, women — strong = prosperity; afflicted = floods or drought",
                "Mars":    "Military, violence, fire — strong = decisive action; afflicted = war, fire, accident",
                "Mercury": "Trade, communications, merchants — strong = commerce boom; afflicted = fraud",
                "Jupiter": "Religion, justice, education — strong = moral prosperity; afflicted = judicial crisis",
                "Venus":   "Luxury, arts, women — strong = cultural flourishing; afflicted = moral decline",
                "Saturn":  "Labour, crops, disease — strong = agricultural stability; afflicted = famine, epidemics",
                "Rahu":    "Foreign elements, manipulation — strong = international gains; afflicted = foreign threat",
                "Ketu":    "Spiritual, fires, hidden forces — afflicted = fires, epidemics, covert destabilization",
            },
        },
        "synthesis_sources": ["gaur_aifas"],
    },

    # ── 3. Cloud Engine ───────────────────────────────────────────────────────
    {
        "spec_id":    "gaur-cloud-engine",
        "spec_type":  "formula",
        "title":      "Gaur Cloud Type / Rainfall Determination Formula",
        "source_book": "Gaur/AIFAS",
        "source_chapter": "Gaur Ch 2",
        "description": (
            "Formula maps Shak Samvat year number to 1 of 9 cloud types. "
            "Cloud type determines rainfall expectation for the year. "
            "Input: Shak Samvat year (= AD year − 78). Output: cloud_type integer 1–9."
        ),
        "spec_data": {
            "formula":       "(Shak_Samvat × 8) mod 9",
            "remainder_0_treated_as": 9,
            "cloud_types": {
                1: {"name": "Pushkara",    "rainfall": "Very heavy rains — flooding possible"},
                2: {"name": "Samvartaka",  "rainfall": "Good general rains — agricultural prosperity"},
                3: {"name": "Bhimnadaka", "rainfall": "Average rains with thunderstorms"},
                4: {"name": "Drona",       "rainfall": "Moderate rains — adequate for crops"},
                5: {"name": "Kala",        "rainfall": "Below average — watch for localised drought"},
                6: {"name": "Neel",        "rainfall": "Sparse rains — drought risk in arid regions"},
                7: {"name": "Varshana",    "rainfall": "Erratic rains — irregular distribution"},
                8: {"name": "Sona",        "rainfall": "Very light rains — famine risk elevated"},
                9: {"name": "Avaha",       "rainfall": "Practically no rains — severe drought year"},
            },
            "shak_samvat_formula": "Shak_Samvat = AD_year − 78",
        },
        "synthesis_sources": ["gaur_aifas"],
    },

    # ── 4. Snake Engine ───────────────────────────────────────────────────────
    {
        "spec_id":    "gaur-snake-engine",
        "spec_type":  "formula",
        "title":      "Gaur Snake Type / Geopolitical Friction Formula",
        "source_book": "Gaur/AIFAS",
        "source_chapter": "Gaur Ch 2",
        "description": (
            "Formula maps Shak Samvat year number to 1 of 12 snake types. "
            "Snake type indicates the nature of geopolitical friction, conflicts, "
            "and international tensions for the year. "
            "Input: Shak Samvat year. Output: snake_type integer 1–12."
        ),
        "spec_data": {
            "formula":       "(Shak_Samvat + 2) mod 12",
            "remainder_0_treated_as": 12,
            "snake_types": {
                1:  {"name": "Ananta",    "friction": "Disputes over territory — border tensions"},
                2:  {"name": "Kulika",    "friction": "Economic rivalry — trade wars and sanctions"},
                3:  {"name": "Vasuki",    "friction": "Political intrigue — coups and power shifts"},
                4:  {"name": "Shankhapala","friction": "Communal unrest — religious or ethnic conflicts"},
                5:  {"name": "Padma",     "friction": "Diplomatic crises — embassy and treaty disputes"},
                6:  {"name": "Mahapadma", "friction": "Military confrontation — arms build-up"},
                7:  {"name": "Takshaka",  "friction": "Assassination risk — targeted political violence"},
                8:  {"name": "Karkota",   "friction": "Natural + man-made disasters — compound crises"},
                9:  {"name": "Shankha",   "friction": "Propaganda and information warfare"},
                10: {"name": "Ghatak",    "friction": "Proxy wars — third-party conflict sponsors"},
                11: {"name": "Vishadhara","friction": "Epidemic or biological threat (poisons/viruses)"},
                12: {"name": "Shesha",    "friction": "Relative calm — residual friction only"},
            },
            "shak_samvat_formula": "Shak_Samvat = AD_year − 78",
        },
        "synthesis_sources": ["gaur_aifas"],
    },

    # ── 5. Samvat Stambha Engine ──────────────────────────────────────────────
    {
        "spec_id":    "gaur-samvat-stambha",
        "spec_type":  "formula",
        "title":      "Gaur Samvat Stambha — 4 Pillar Seasonal Assessment",
        "source_book": "Gaur/AIFAS",
        "source_chapter": "Gaur Ch 2",
        "description": (
            "Stambha = pillar/column. 4 pillars assess Water, Grain/Grass, Wind, and Food "
            "conditions for the year. Each pillar is calculated from the proportional duration "
            "of Pratipada (first lunar day) spent in each season/sign at year start. "
            "High % in a pillar = abundance; Low % = scarcity."
        ),
        "spec_data": {
            "formula": (
                "For each pillar: percentage = "
                "(nakshatra_duration_during_Chaitra_Pratipada / total_Pratipada_duration) × 100"
            ),
            "pillars": {
                "jal_stambha":  {"element": "Water", "governs": "Rainfall, irrigation, rivers, ocean activity"},
                "trin_stambha": {"element": "Grain/Grass", "governs": "Crop yield, grazing, agricultural surplus"},
                "vayu_stambha": {"element": "Wind/Air", "governs": "Storms, cyclones, atmospheric pressure"},
                "anna_stambha": {"element": "Food/Grain", "governs": "Food availability, grain stocks, famine risk"},
            },
            "interpretation": {
                "high_jal":  "Abundant rainfall — flood risk in low-lying areas",
                "low_jal":   "Drought year — water scarcity in arid zones",
                "high_anna": "Food surplus — prices low, public contentment",
                "low_anna":  "Food scarcity — prices high, social unrest risk",
            },
        },
        "synthesis_sources": ["gaur_aifas"],
    },

    # ── 6. Sanghatta Chakra Vedha Matrix ─────────────────────────────────────
    {
        "spec_id":    "gaur-sanghatta-vedha-matrix",
        "spec_type":  "lookup_grid",
        "title":      "Gaur Sanghatta Chakra — Rashi Vedha (Obstruction) Vector Matrix",
        "source_book": "Gaur/AIFAS",
        "source_chapter": "Gaur Ch 6",
        "description": (
            "Each Rashi has 3 Vedha vectors: front (opposite), left flank, right flank. "
            "A malefic transiting a Vedha rashi of another malefic creates the "
            "'Sanghatta' (collision/conflict). When Saturn + Mars + Rahu meet on this grid "
            "= Destruction Scheme (war prerequisite). See interpretation_rules for predictive rules."
        ),
        "spec_data": {
            "vedha_logic": (
                "Vedha = obstruction. A planet in position X creates Vedha pressure on the "
                "three positions listed as its front, left, and right Vedha targets. "
                "When two malefics form mutual Vedha = conflict indicator. "
                "Three malefics (Saturn + Mars + Rahu) in mutual Vedha = Destruction Scheme."
            ),
            "rashi_vedha_vectors": {
                "aries":       {"front": "libra",        "left": "cancer",      "right": "capricorn"},
                "taurus":      {"front": "scorpio",       "left": "leo",         "right": "aquarius"},
                "gemini":      {"front": "sagittarius",   "left": "virgo",       "right": "pisces"},
                "cancer":      {"front": "capricorn",     "left": "libra",       "right": "aries"},
                "leo":         {"front": "aquarius",      "left": "scorpio",     "right": "taurus"},
                "virgo":       {"front": "pisces",        "left": "sagittarius", "right": "gemini"},
                "libra":       {"front": "aries",         "left": "capricorn",   "right": "cancer"},
                "scorpio":     {"front": "taurus",        "left": "aquarius",    "right": "leo"},
                "sagittarius": {"front": "gemini",        "left": "pisces",      "right": "virgo"},
                "capricorn":   {"front": "cancer",        "left": "aries",       "right": "libra"},
                "aquarius":    {"front": "leo",           "left": "taurus",      "right": "scorpio"},
                "pisces":      {"front": "virgo",         "left": "gemini",      "right": "sagittarius"},
            },
            "destruction_scheme": {
                "trigger": "Saturn AND Mars AND Rahu all meet on the Sanghatta grid",
                "result":  "Destruction_Scheme = TRUE — war/large-scale conflict imminent",
                "validation": "Confirmed in multiple historical war outbreaks",
            },
            "rohini_gate": {
                "position":   "Taurus 10° to 23°20' (within Rohini nakshatra)",
                "rule":       "Saturn or malefics in Rohini aspected by Mars = critical war/famine threshold",
                "historical": ["WWI 1914-18", "WWII 1939-45", "1971 Indo-Pak War"],
            },
        },
        "synthesis_sources": ["gaur_aifas", "mehta_rao"],
    },

    # ── 7. Simhasan Chakra ────────────────────────────────────────────────────
    {
        "spec_id":    "mehta-simhasan-chakra",
        "spec_type":  "lookup_grid",
        "title":      "Mehta Simhasan Chakra — 5-Level Nakshatra Authority Grid",
        "source_book": "Mehta/Rao",
        "source_chapter": "Mehta Ch 18",
        "description": (
            "Maps all 27 Nakshatras to 5 levels of authority in the national chart. "
            "Used to assess: (1) which 'layer' of authority is activated when a planet "
            "transits a nakshatra; (2) oath-taking ceremony vetting — Moon or Lagna lord "
            "in high-authority nakshatra = strong governance. "
            "Level 5 (Simhasan) = peak authority; Level 1 (Aadhaar) = public/mass foundation."
        ),
        "spec_data": {
            "levels": {
                "5_simhasan_throne": {
                    "label":      "Simhasan (Throne) — Peak Authority",
                    "lord":       "Mars",
                    "nakshatras": ["Mrigshira", "Chitra", "Dhanishtha"],
                    "result":     "Maximum authority; dominant martial leadership; peak governance power",
                },
                "4_simha_royalty": {
                    "label":      "Simha (Royal Cabinet) — Executive Power",
                    "lords":      ["Moon", "Rahu"],
                    "nakshatras": ["Rohini", "Ardra", "Hasta", "Swati", "Shravan", "Shatbhisha"],
                    "result":     "Martial leadership; decisive executive action; cabinet-level authority",
                },
                "3_patta_ministers": {
                    "label":      "Patta (Council of Ministers) — Policy Strength",
                    "lords":      ["Sun", "Jupiter"],
                    "nakshatras": ["Krittika", "Punarvasu", "Uttaraphalguni", "Vishakha", "Uttarashadh", "Poorvabhadrapad"],
                    "result":     "Policy coherence; ministerial support; judicial authority",
                },
                "2_aasan_bureaucracy": {
                    "label":      "Aasan (Bureaucracy) — Administrative Support",
                    "lords":      ["Venus", "Saturn"],
                    "nakshatras": ["Bharani", "Pushya", "Poorvaphalguni", "Anuradha", "Poorvashadh", "Uttarabhadrapad"],
                    "result":     "Civil service stability; administrative backing for the leader",
                },
                "1_aadhaar_public": {
                    "label":      "Aadhaar (Public Foundation) — Mass Base",
                    "lords":      ["Ketu", "Mercury"],
                    "nakshatras": ["Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Mool", "Revati"],
                    "result":     "Public mood indicator; mass popular support or agitation",
                },
            },
            "usage_notes": [
                "Oath chart vetting: Moon in Simhasan/Simha level = strong leadership mandate",
                "Oath chart: Moon in Aadhaar level = government derives strength from public pressure (populist)",
                "War forecast: Moon + Mars in Simha Nadi = military king — leads nation into conflict",
                "Opposition assessment: Opponent with Moon in Simhasan vs. Moon in Aadhaar = challenger wins",
            ],
        },
        "synthesis_sources": ["mehta_rao"],
    },

    # ── 8. 5-Year Governance Dasha Table ─────────────────────────────────────
    {
        "spec_id":    "mehta-5yr-dasha-table",
        "spec_type":  "lookup_table",
        "title":      "Mehta 5-Year Compressed Vimshottari Dasha for Governance",
        "source_book": "Mehta/Rao",
        "source_chapter": "Mehta Ch 18",
        "description": (
            "Compresses the standard 120-year Vimshottari Dasha into a 5-year government mandate. "
            "Used to time policy shifts, leadership crises, and administrative collapses "
            "within a single parliamentary term. "
            "Formula: Compressed_days = (Vimshottari_years × 5 × 365) / 120"
        ),
        "spec_data": {
            "base_formula":    "Planet_Days = (Vimshottari_Years × 5 × 365) / 120",
            "compressed_periods_days": {
                "ketu":    {"years": 7,  "days": 106},
                "venus":   {"years": 20, "days": 304},
                "sun":     {"years": 6,  "days": 91},
                "moon":    {"years": 10, "days": 152},
                "mars":    {"years": 7,  "days": 106},
                "rahu":    {"years": 18, "days": 274},
                "jupiter": {"years": 16, "days": 244},
                "saturn":  {"years": 19, "days": 289},
                "mercury": {"years": 17, "days": 259},
            },
            "total_days": 1825,
            "total_years": 5,
            "starting_planet": "Planet at Lagna lord at oath-taking — determines first sub-period",
            "usage_examples": [
                "Mars sub-period (106 days): peak military assertion, border tension",
                "Saturn sub-period (289 days): agricultural stress, labour unrest, austerity",
                "Jupiter sub-period (244 days): policy expansion, judicial activity, education reform",
                "Venus sub-period (304 days): cultural growth, diplomatic initiatives, luxury spending",
                "Sun sub-period (91 days): leadership assertion, executive decisions, foreign policy",
            ],
            "varshaphala_ratio": {
                "description": "Annual Varshaphala dasha uses same planets but 1-year compression",
                "formula":     "Annual_days = (Vimshottari_Years × 1 × 360) / 120",
                "annual_values_days": {
                    "ketu": 21, "venus": 60, "sun": 18, "moon": 30,
                    "mars": 21, "rahu": 54, "jupiter": 48, "saturn": 57, "mercury": 51,
                },
            },
        },
        "synthesis_sources": ["mehta_rao"],
    },

    # ── 9. Transit Temporal Matrix — Sun ─────────────────────────────────────
    {
        "spec_id":    "gaur-transit-temporal-sun",
        "spec_type":  "transit_lookup_table",
        "title":      "Gaur Ch 10: Transit of Sun — Sign & Nakshatra Commodity Matrix",
        "source_book": "Gaur/AIFAS",
        "source_chapter": "Gaur Ch 10",
        "description": (
            "Lookup table: Sun transiting each of the 12 signs and 27 Nakshatras → "
            "specific commodities become expensive or cheap. Results materialize within "
            "14–15 days of Sun's entry. Used for monthly agricultural price forecasting."
        ),
        "spec_data": {
            "temporal_offset_days": 14,
            "sign_commodity_matrix": {
                "aries":       {"expensive": ["Gold","Silver","Gur","Sugar","Fruits","Dry fruits","Sesame","Oil","Ghee","Thread"], "cheap": ["Wheat","Pulses"]},
                "taurus":      {"expensive": ["Gold","Silver","Gur","Sugar","Juicy materials","Sesame","Oil","Dry fruits"], "cheap": ["Gram","Barley","Grains","Pulses"]},
                "gemini":      {"expensive": ["Gold","Silver","Gur","Sugar","Juicy materials","Sesame","Oils","Jute materials","Thread","Wheat","Gram","Pulses"]},
                "cancer":      {"expensive": ["Gold","Silver","Metals","Gur","Sugar","Fruits","Dry fruits"], "cheap": ["Wheat","Gram","Barley","Pulses","Moong","Moth","Arhar","Urad"]},
                "leo":         {"expensive": ["Gold","Silver","Gur","Sugar","Juicy materials","Sesame","Oils","Red coloured things","Gems"], "cheap": ["Grains","Pulses"]},
                "virgo":       {"expensive": ["Sesame","Oil materials","Cotton","Coconut"], "cheap": ["Cotton"]},
                "libra":       {"expensive": ["Wheat","Barley","Gram","Gold","Copper","Red sandal","Betelnut"], "cheap": ["Cotton","Silver"]},
                "scorpio":     {"expensive": ["Gold","Silver","Copper","Cotton"], "cheap": ["Red coloured things"]},
                "sagittarius": {"expensive": ["Gold","Silver","Cotton","Thread","Sesame","Oil materials"], "cheap": ["Wheat","Gram","Barley","Grains"]},
                "capricorn":   {"expensive": ["Gur","Sugar","Juicy materials","Cotton","Thread","Oil","Ghee"], "cheap": ["Wheat","Gram","Jute materials"]},
                "aquarius":    {"expensive": ["Gur","Jute materials","Sesame","Oil materials","Ghee","Ground nut"], "cheap": ["Wheat","Gram"]},
                "pisces":      {"expensive": ["Sesame","Oils","Juicy materials","Gur","Cotton","Thread","Gold"], "cheap": ["Grains","Pulses"]},
            },
            "nakshatra_commodity_matrix": {
                "ashwini":        {"expensive": ["Gold","Silver","Copper","Iron","Sesame","Oils","Red sandal","Cotton cloth","Clove","Cardamom","Grains"], "cheap": ["Cotton"]},
                "bharani":        {"expensive": ["Gold","Silver","Copper","Metals","Brass utensils","Wheat","Barley","Gram","Juicy materials","Gur","Ghee","Oil materials"], "cheap": ["Cotton"]},
                "krittika":       {"expensive": ["Gold","Silver","Wheat","Barley","Gram","Moong","Moth","Oil materials","Ghee"]},
                "rohini":         {"expensive": ["Wheat","Barley","Gram","Gur","Oils","Oil materials","Ghee","Woolen clothes","Cotton clothes","Chillies"], "cheap": ["Silver"]},
                "mrigshira":      {"expensive": ["Gold","Silver","Moong","Moth","Urad","Pulses","Gram","Millet","Water-cultivated materials"]},
                "ardra":          {"expensive": ["Wheat","Gram","Rice","Barley","Silver","Cotton","Oil cake"], "cheap": ["Gold"]},
                "punarvasu":      {"expensive": ["Gur","Cotton","Thread","Sesame","Oil materials","Pulses","Grocery materials"]},
                "pushya":         {"expensive": ["Wheat","Barley","Gram","Rice","Sesame","Oils","Gold","Silver","Woolen clothes"], "cheap": ["Cotton","Thread"]},
                "ashlesha":       {"expensive": ["Wheat","Rice","Gram","Urad","Moong","Gold","Silver","Oils","Ghee","Chillies"]},
                "magha":          {"expensive": ["Sesame","Oil materials","Moong","Silver"]},
                "poorvaphalguni": {"expensive": ["Wheat","Gur","Oils","Oil materials","Ghee","Woolen clothes","Cotton clothes","Gold"], "cheap": ["Silver"]},
                "uttaraphalguni": {"expensive": ["Gold","Silver","Iron","Sesame","Oil materials","Ghee","Rice","Urad","Cotton"]},
                "hasta":          {"expensive": ["Barley","Wheat","Gur","Turmeric","Coriander"]},
                "chitra":         {"expensive": ["Gold","Silver","Gram","Pulses","Yarn","Red clothes","Gur"]},
                "swati":          {"expensive": ["Gold","Silver","Gur","Oil materials","Perfumes","Yarn","Silk clothes"]},
                "vishakha":       {"expensive": ["Wheat","Rice","Barley","Pulses","Sesame","Oil materials","Gur"], "cheap": ["Silver"]},
                "anuradha":       {"expensive": ["Wheat","Barley","Woollen clothes"], "cheap": ["Wheat","Gold","Silver"]},
                "jyeshtha":       {"expensive": ["Gold","Silver","Wheat","Barley","Gram","Rice","Oil materials","Perfumes","Gur"], "cheap": ["Cotton"]},
                "mool":           {"cheap": ["Gold","Silver","Cotton","Yarn"]},
                "poorvashadh":    {"expensive": ["Gur","Woolen clothes","Silver","Sesame","Oil materials"]},
                "uttarashadh":    {"expensive": ["Wheat","Gram","Rice","Moong","Urad","Gur","Oil materials","Jute goods"]},
                "shravan":        {"expensive": ["Wheat","Barley","Rice","Gur","Gold","Silver","Yarn"]},
                "dhanishtha":     {"expensive": ["Wheat","Pulses","Gold","Silver","Gems","Cotton","Yarn"]},
                "shatbhisha":     {"expensive": ["Wheat","Sesame","Oil materials","Gur","Gold","Silver","Cotton clothes","Perfumery"]},
                "poorvabhadrapad":{"expensive": ["Wheat","Gram","Pulses","Gur","Oils","Oil materials","Ghee","Gold","Silver","Clothes"]},
                "uttarabhadrapad":{"expensive": ["Wheat","Rice","Gur","Oils"]},
                "revati":         {"expensive": ["Wheat","Gram","Rice","Oil materials","Peanuts","Cotton"]},
            },
        },
        "synthesis_sources": ["gaur_aifas"],
    },

    # ── 10. Transit Temporal Matrix — Moon ───────────────────────────────────
    {
        "spec_id":    "gaur-transit-temporal-moon",
        "spec_type":  "transit_lookup_table",
        "title":      "Gaur Ch 10: Transit of Moon — Sign & Rise Commodity Triggers",
        "source_book": "Gaur/AIFAS",
        "source_chapter": "Gaur Ch 10",
        "description": (
            "Moon transit triggers are short-duration (hours to 2 days). "
            "Moon acts as the IGNITER for Sun-primed commodity signals. "
            "Moon's 'Rise' in a nakshatra fires the final price trigger. "
            "Key role: final confirmation gate before a price event manifests."
        ),
        "spec_data": {
            "role":            "Short-term igniter — confirms Sun-primed commodity signals",
            "duration":        "Hours to 2 days per nakshatra",
            "sign_results": {
                "aries":       {"effect": "Expensive: Gold, metals, red items; Cheap: Grains"},
                "taurus":      {"effect": "Expensive: Milk, ghee, juicy materials, white things; Cheap: Red items"},
                "gemini":      {"effect": "Expensive: All cereals, thread, yarn; stable for most"},
                "cancer":      {"effect": "Expensive: Watery vegetables, fish, seafood; Cheap: Metals"},
                "leo":         {"effect": "Expensive: Gold, gems, expensive cloth; Cheap: Grains, pulses"},
                "virgo":       {"effect": "Expensive: Grains, sesame, cotton; Cheap: Gold, luxury items"},
                "libra":       {"effect": "Expensive: Wheat, barley; Cheap: Oils, silver"},
                "scorpio":     {"effect": "Expensive: Gold, copper, red items; Cheap: Cotton"},
                "sagittarius": {"effect": "Expensive: Gold, silver, ghee, oils; Cheap: Grains"},
                "capricorn":   {"effect": "Expensive: Iron, black items, oils; Cheap: Gold"},
                "aquarius":    {"effect": "Expensive: Oils, sesame, jute; Cheap: Grains"},
                "pisces":      {"effect": "Expensive: Fish, seafood, oils; Cheap: Cotton, thread"},
            },
            "igniter_principle": (
                "The Moon's entry into a nakshatra that matches the Sun's current sign-signal "
                "amplifies the commodity price shift to maximum intensity within 24–48 hours. "
                "Moon opposing the signal = temporary counter-signal (price correction)."
            ),
        },
        "synthesis_sources": ["gaur_aifas"],
    },

    # ── 11. Sun Ingress Weekday Filter ────────────────────────────────────────
    {
        "spec_id":    "gaur-sun-ingress-weekday",
        "spec_type":  "lookup_table",
        "title":      "Gaur Ch 10: Sun Sankranti Weekday Ingress Modifier Matrix",
        "source_book": "Gaur/AIFAS",
        "source_chapter": "Gaur Ch 10",
        "description": (
            "The day-of-week on which the Sun enters a new sign modifies the commodity "
            "price signals for the entire month. Overrides the base sign commodity matrix "
            "when weekday pattern is strong. Applies to all 12 ingresses (Sankrantis). "
            "Muhurti duration also modifies: 45-muhurti ingress = maximum benefic (cheap grains)."
        ),
        "spec_data": {
            "aries_ingress_modifiers": {
                "sun_tue_sat": {"expensive": ["Wheat","Gram","Barley","Majeeth","Saffron"]},
                "mon":         {"expensive": ["Gur","Khand","Oils","Oil materials","Cotton","Cotton clothes"]},
                "thu":         {"cheap":     ["Grains"]},
                "wed_fri":     {"cheap":     ["Grains","White things","Sugar"]},
            },
            "taurus_ingress_modifiers": {
                "sun_tue_sat": {"expensive": ["Grains","Gur","Dry fruits","Grocery"]},
                "mon":         {"expensive": ["Grains"]},
                "wed_thu_fri": {"expensive": ["Oils","Oil materials","Cotton","White things","Sugar"],
                                "cheap":     ["Grains"]},
            },
            "general_muhurti_rule": {
                "45_muhurti": "Maximum benefic ingress — good rainfall and cheap grains assured even in dry seasons",
                "30_muhurti": "Moderate benefic — average yield; prices stable",
                "15_muhurti": "Weak ingress — prices volatile; watch for weather disruption",
            },
            "retrograde_override": (
                "If Saturn is retrograde at the time of any Sankranti, the weekday modifier "
                "is overridden and the result defaults to: 'Prices volatile; agricultural instability.'"
            ),
        },
        "synthesis_sources": ["gaur_aifas"],
    },

    # ── 12. Industrial Sector Engine ─────────────────────────────────────────
    {
        "spec_id":    "gopal-industrial-sector",
        "spec_type":  "transit_lookup_table",
        "title":      "Gopalakrishnan Industrial Sector Performance Engine",
        "source_book": "Gopalakrishnan",
        "source_chapter": "Gopal Ch 14",
        "description": (
            "Maps planetary transits relative to India's national foundation chart to "
            "sectoral performance predictions. Validated against 2006 actual market hits. "
            "Each sector governed by a karaka planet + specific house of the national chart."
        ),
        "spec_data": {
            "sector_mappings": {
                "automotive_mechanical": {
                    "karaka":    "Mars (Energy/Steel/Engineering)",
                    "house":     "4th House of India (Vehicles/Land/Industry)",
                    "rules": [
                        {"condition": "Mars at perigee (closest to Earth)",        "result": "High manufacturing efficiency; auto ancillaries boom"},
                        {"condition": "4th lord strong + aspected by Saturn",       "result": "Entry-level segments outperform luxury; mass-market dominance"},
                        {"condition": "Mars in Upchayya houses (3, 6, 10, 11)",     "result": "Auto ancillaries become export profit centres"},
                    ],
                },
                "information_technology_bpo": {
                    "karaka":    "Mercury (Communications/Networks/Writing)",
                    "house":     "3rd House of India (Networks/Connectivity/Writing)",
                    "rules": [
                        {"condition": "Saturn transits 3rd house of India's Lagna", "result": "India becomes global BPO backbone — ignore all skepticism"},
                        {"condition": "Mercury direct in Airy signs",               "result": "BPO enters specialisation phase (KPO, LPO, research)"},
                        {"condition": "3rd lord conjunct 11th lord",                "result": "Exponential Internet penetration and PC ownership growth"},
                    ],
                    "validation": "2006: IT/BPO trebled despite media predictions of failure",
                },
                "real_estate": {
                    "karaka":    "Saturn (Land/Property/Construction)",
                    "house":     "4th House (Land and Housing)",
                    "rules": [
                        {"condition": "Saturn enters Leo (Simha)",                  "result": "100% growth in property prices; massive housing demand"},
                        {"condition": "Venus as Lagna lord in Rahu axis",           "result": "Explosion of malls, hyper-marts, retail redesign in metros"},
                    ],
                    "validation": "2006-2008: Chennai and major metros saw 100% price surge when Saturn entered Leo",
                },
                "pharmaceuticals_healthcare": {
                    "karaka":    "Jupiter (Healing/Medicine) + Saturn (Chronic disease/service)",
                    "house":     "6th House of India (Service/Disease)",
                    "rules": [
                        {"condition": "6th lord in 10th or 11th house",             "result": "Indian pharma establishes record exports and R&D breakthroughs"},
                        {"condition": "Jupiter aspects 6th house",                  "result": "Large-scale hospital chains achieve international recognition"},
                    ],
                },
                "retail_fmcg": {
                    "karaka":    "Venus (Luxury/Goods) + Mercury (Trade/Commerce)",
                    "house":     "2nd House (Food/Speech) + 11th House (Gains)",
                    "rules": [
                        {"condition": "Mars in 2nd house of Varsha Pravesh",         "result": "FMCG rural markets outperform urban in volume growth"},
                        {"condition": "Mercury Bhukti active with Jupiter in 2nd",   "result": "Banking computerisation and new revenue model boom"},
                    ],
                },
            },
            "pushya_bull_rule": {
                "condition":   "Saturn transits Pushya nakshatra (Cancer 3°20'-16°40')",
                "result":      "Dream bull run: 50-100% growth in equity index expected",
                "sector_winners": ["Banking", "FMCG", "IT", "Telecom"],
                "validation":  "2006: Sensex rose from 6,000 to 12,000+ when Saturn in Pushya",
            },
            "nadi_career_fall_rule": {
                "condition":   "Saturn transits 8th nakshatra from native's natal Jupiter",
                "result":      "Sudden sustained poor form or career break for elite individual",
                "validation":  "Ganguly, Sachin: career decline precisely timed by this rule (2006)",
            },
        },
        "synthesis_sources": ["gopal_modern"],
    },

    # ── 13. Sarvatobhadra Vedha Trade Engine ──────────────────────────────────
    {
        "spec_id":    "gaur-sarvatobhadra-trade",
        "spec_type":  "trade_engine",
        "title":      "Gaur Sarvatobhadra Chakra — Vedha-Based Commodity Price Engine",
        "source_book": "Gaur/AIFAS",
        "source_chapter": "Gaur Ch 8/10",
        "description": (
            "The Sarvatobhadra Chakra is an 81-cell grid. Benefic Vedha on a commodity "
            "nakshatra = prices DECREASE (oversupply or peace signal). "
            "Malefic Vedha = prices INCREASE (scarcity or conflict signal). "
            "Mercury's commodity result is determined by its conjunction partner (not its own quality)."
        ),
        "spec_data": {
            "core_rules": {
                "benefic_vedha": "Benefic planet's Vedha on commodity nakshatra → price DECREASES (supply up / demand satisfied)",
                "malefic_vedha": "Malefic planet's Vedha on commodity nakshatra → price INCREASES (scarcity / tension signal)",
                "mercury_rule":  "Mercury adopts the commodity result of whichever planet it is conjunct — benefic partner = cheap; malefic partner = expensive",
            },
            "yield_price_inverse": {
                "rule":       "High agricultural yield → prices LOW; Low agricultural yield → prices HIGH",
                "mechanism":  "Oversupply in good yield years depresses prices; scarcity in poor years inflates them",
                "application": "Always check yield forecast before commodity price forecast — they are inversely correlated",
            },
            "grid_structure": {
                "dimension":   "9×9 = 81 cells",
                "central_cell": "Nakshatra of the commodity or subject in question",
                "vedha_calc":   "Planets cast Vedha shadows across the grid based on their sign position",
                "benefics":    ["Jupiter", "Venus", "Mercury (benefic partner)", "Moon (bright/waxing)"],
                "malefics":    ["Saturn", "Mars", "Rahu", "Ketu", "Sun", "Mercury (malefic partner)", "Moon (dark/waning)"],
            },
        },
        "synthesis_sources": ["gaur_aifas"],
    },

    # ── 14. Assassination Engine Diagnostic Protocol ─────────────────────────
    {
        "spec_id":    "mehta-assassination-engine",
        "spec_type":  "diagnostic_protocol",
        "title":      "Mehta Political Assassination / Leadership Hazard Engine",
        "source_book": "Mehta/Rao",
        "source_chapter": "Mehta Ch 21",
        "description": (
            "Multi-gate diagnostic protocol for predicting leadership physical jeopardy. "
            "Validated against: Mahatma Gandhi (1948), Indira Gandhi (1984), "
            "Rajiv Gandhi (1991), Lal Bahadur Shastri (1966), JFK (1963), "
            "Baba Gurbachan Singh (1980), Sheikh Mujiburrahman (1975). "
            "Requires layered audit: Foundation Chart → New Year → Solar Ingress → New Moon."
        ),
        "spec_data": {
            "luminary_siege_rule": {
                "rule":        "On the day of assassination, BOTH Sun AND Moon must be afflicted by malefics in transit",
                "significance": "This is the MANDATORY base condition — no assassination without luminary siege",
            },
            "audit_sequence": [
                {"step": 1, "chart": "Foundation/Natal",       "check": "8th-house afflictions, Lagna lord weakness, Sun-Moon siege potential"},
                {"step": 2, "chart": "Hindu New Year",          "check": "10th house (Leader) affliction, 8th house lethality, Luminaries status"},
                {"step": 3, "chart": "Solar Ingress (nearest)", "check": "12th house cluster, Lagna lord affliction, 10th lord martial threat"},
                {"step": 4, "chart": "New Moon (trigger)",      "check": "7th house lunation, 8th house nodes, Luminary final siege confirmation"},
            ],
            "infiltration_gate": {
                "rule":       "Mars in 12th house of Hindu New Year chart = terrorists/assassins have entered the country",
                "directional": {
                    "mars_in_taurus":    "Threat from South direction",
                    "mars_in_aries":     "Threat from East direction",
                    "mars_in_capricorn": "Threat from North direction",
                    "mars_in_cancer":    "Threat from West direction",
                },
                "explosion_multiplier": "If Mars in 12th is ALSO aspected by Rahu = suicide bombing/explosive attack (coefficient 0.98)",
            },
            "terminal_strike_jfk_standard": {
                "rule":       "Lagna Lord + 8th Lord conjunct in 8th House, aspected by 6th Lord",
                "result":     "Terminal assassination — protection systems will fail",
                "validation": "JFK: Mercury (Lagna lord) + Mars (8th lord) in 8th, aspected by Saturn (6th lord)",
            },
            "12th_house_congestion": {
                "rule":       "4+ planets cluster in 12th house of Solar Ingress chart",
                "result":     "Maximum infiltration alert — multiple specialized agents inside borders",
                "validation": "Rajiv Gandhi: Sun, Moon, Mercury, Venus, Rahu all in 12th house of Sun-Taurus ingress",
            },
        },
        "synthesis_sources": ["mehta_rao"],
    },

    # ── 15. Seismic 16-Factor Checklist ──────────────────────────────────────
    {
        "spec_id":    "mehta-seismic-16factors",
        "spec_type":  "diagnostic_protocol",
        "title":      "Mehta Ch 11 — 16-Factor Earthquake Prediction Checklist",
        "source_book": "Mehta/Rao",
        "source_chapter": "Mehta Ch 11",
        "description": (
            "Systematic 16-point checklist for earthquake prediction. "
            "Eclipses are 'forerunners' (pre-conditions); malefic aspects are 'igniters'. "
            "Fixed signs (Taurus/Scorpio) are primary seismic triggers. "
            "Validated against: Bihar 1934, Bhuj 2001, Turkey 1983, China 1976, Mexico 2003."
        ),
        "spec_data": {
            "factors": {
                "01": {"name": "Eclipse Proximity",       "condition": "Earthquake occurs shortly after eclipse — targeting countries where eclipse fell in 4th/10th house"},
                "02": {"name": "Fixed Sign Angles",       "condition": "Planets in fixed signs (TA/LE/SC/AQ) at eclipse moment — triggers if Rising, Setting, or on Meridian/Nadir"},
                "03": {"name": "Malefic Eclipse Linkage", "condition": "Malefic planets form aspects with previous eclipse point — eclipse is forerunner, malefic aspect is igniter"},
                "04": {"name": "Scorpio-Taurus Axis",     "condition": "Major transits/eclipses in Taurus or Scorpio — notoriously seismic signs (Rohini factor)"},
                "05": {"name": "Jupiter-Mercury Friction","condition": "Jupiter in TA/SC conjunct or opposed to Mercury — prolific source of earthquake activity"},
                "06": {"name": "Cardinal Ingress Audit",  "condition": "Malefics in/aspecting 4th house of Aries/Cancer/Libra/Capricorn ingress charts"},
                "07": {"name": "Movable Clustering",      "condition": "Concentration of planets in first 10° of Cardinal signs (Aries/Cancer/Libra/Capricorn)"},
                "08": {"name": "Eclipse Longitude Overlap","condition": "Eclipse longitude aligns with ruling sign/longitude of a specific city → refines 'where'"},
                "09": {"name": "Cometary Proximity",      "condition": "Great comet nearest to Sun or Earth — macro-seismic trigger"},
                "10": {"name": "Diurnal Timing",          "condition": "Window: Midday-to-Sunset OR Midnight-to-Sunrise = peak seismic activity windows"},
                "11": {"name": "Retrogression Factor",    "condition": "Saturn retrograde in fixed signs amplifies seismic risk in its sign zone"},
                "12": {"name": "Perihelion Risk",         "condition": "Earth at perihelion (closest to Sun) increases tidal and seismic stress"},
                "13": {"name": "Mercury-Saturn Link",     "condition": "Mercury-Saturn interconnection OR Mercury behind the Sun = key temporal marker"},
                "14": {"name": "Aries Ingress 4th/8th",  "condition": "Affliction to BOTH 4th and 8th houses in annual Aries Ingress chart"},
                "15": {"name": "Jupiter at Sign Junction","condition": "Jupiter at Rasi Sandhi (0° or 29°) with Venus beginning another sign = double transit instability"},
                "16": {"name": "Mundane House Veto",      "condition": "Final audit: malefics in houses 1, 4, 7, 8, 10, 12 simultaneously"},
            },
            "bhuj_scale_trigger": {
                "condition":   "Saturn + Jupiter conjunct in Taurus, aspected by Mars",
                "result":      "Critical Disaster Warning: Major earthquake (Richter 6+) in 4th house zone",
                "validation":  "2001 Gujarat/Bhuj earthquake",
            },
            "varahamihira_circles": {
                "wind_circle": {
                    "nakshatras": ["Uttaraphalguni","Hasta","Chitra","Swati","Punarvasu","Mrigshira","Ashwini"],
                    "symptoms":   "Strong winds, broken trees, dim Sun",
                },
                "fire_circle": {
                    "nakshatras": ["Pushya","Krittika","Vishakha","Bharani","Magha","Poorvabhadrapad","Poorvaphalguni"],
                    "symptoms":   "Meteors, red horizon, drying lakes",
                },
                "indra_circle": {
                    "nakshatras": ["Abhijit","Shravan","Dhanishtha","Rohini","Jyeshtha","Uttarashadh","Anuradha"],
                    "symptoms":   "Thunder, lightning, heavy rain — kills celebrated men/leaders",
                },
            },
        },
        "synthesis_sources": ["mehta_rao", "gaur_aifas"],
    },
]


# ── Document builder ─────────────────────────────────────────────────────────

def build_all(now: str) -> list[dict]:
    docs = []
    for spec in ENGINE_SPECS:
        doc = {
            "spec_id":       spec["spec_id"],
            "spec_type":     spec["spec_type"],
            "title":         spec["title"],
            "source": {
                "science":           SCIENCE,
                "book":              spec["source_book"],
                "chapter":           spec["source_chapter"],
                "batch_id":          BATCH_ID,
                "synthesis_sources": spec["synthesis_sources"],
            },
            "description": spec["description"],
            "spec_data":   spec["spec_data"],
            "created_at":  now,
            "updated_at":  now,
        }
        docs.append(doc)
    return docs


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--save",     help="Path to write JSON")
    parser.add_argument("--upload",   help="Path to JSON for upload")
    parser.add_argument("--mongo-url")
    parser.add_argument("--db-name",  default="horoscope_db")
    args = parser.parse_args()

    now  = datetime.now(timezone.utc).isoformat()
    docs = build_all(now)

    if args.dry_run or args.save:
        by_type: dict[str, int] = {}
        for d in docs:
            st = d["spec_type"]
            by_type[st] = by_type.get(st, 0) + 1

        print(f"Built {len(docs)} spec documents for batch {BATCH_ID}")
        print(f"Target collection: {COLL_NAME}\n")
        print("Breakdown by spec_type:")
        for st, count in sorted(by_type.items()):
            print(f"  {st:<35}: {count}")
        print("\nSpec IDs:")
        for d in docs:
            print(f"  {d['spec_id']}")

        if args.save:
            with open(args.save, "w") as f:
                json.dump(docs, f, indent=2, default=str)
            print(f"\nSaved → {args.save}")
        print("\nDry run complete.")
        return

    if args.upload:
        if not args.mongo_url:
            raise SystemExit("ERROR: --mongo-url is required with --upload")
        with open(args.upload) as f:
            docs = json.load(f)

        client   = MongoClient(args.mongo_url)
        col      = client[args.db_name][COLL_NAME]
        inserted = updated = 0
        for doc in docs:
            result = col.update_one(
                {"spec_id": doc["spec_id"]},
                {"$set":    doc},
                upsert=True,
            )
            if result.upserted_id:
                inserted += 1
            elif result.modified_count:
                updated += 1
        print(f"Loaded {len(docs)} spec documents from {args.upload}")
        print(f"Inserted {inserted} / Updated {updated} → {args.db_name}.{COLL_NAME}")
        client.close()


if __name__ == "__main__":
    main()
