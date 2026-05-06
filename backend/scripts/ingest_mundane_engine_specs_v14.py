"""
Mundane Astrology — Engine Specs v14
Batch: mundane-engine-v14-20260506

Sources:
  Mehta Ch 10  — Macro-Conjunction Engine (Saturn-Jupiter, Saturn-Rahu, Saturn-Mars,
                 Mars-Jupiter, Mars-Rahu/Ketu; judging protocol; historical benchmark matrix)
  Gaur Ch 10   — Transit Price Matrix: Sun (sign + constellation + weekday ingress + muhurti)
  Gaur Ch 10   — Transit Price Matrix: Moon (sign + rise-in-constellation)
  Gaur Ch 10   — Transit Price Matrix: Saturn (sign w/ navamsh, constellation w/ pad,
                 direct/retrograde motion, special retrograde triggers)

4 engine specs in this batch.

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
_BATCH     = "mundane-engine-v14-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ============================================================
# SPEC 1: Mehta Ch 10 — Macro-Conjunction Engine
# ============================================================

MEHTA_CH10_MACRO_CONJUNCTION = {
    "spec_id":        "mehta-ch10-macro-conjunction-engine",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "macro_temporal_engine",
    "title":          "Macro-Conjunction Engine — Saturn-Jupiter, Saturn-Rahu, Saturn-Mars, Mars-Ketu/Rahu",
    "source_chapter": "Mehta/Rao Ch 10",
    "description": (
        "The meeting of heavy planets signals the death of old orders and the birth of new ones. "
        "This spec defines the 'Macro-Clock' — the logic gates for major planetary alignments "
        "that act as primary turning points in the history of nations and the world order. "
        "Dramatic events rarely happen at the moment of conjunction; they materialize when Mars "
        "conjoins or aspects the pre-existing conjunction/opposition degree (Ignition Rule)."
    ),
    "judging_protocol": {
        "step_1_planetary_nature":   "Determine if involved planets are malefic (unleash evil forces) or benefic (give good results).",
        "step_2_role_signification": "Audit specific roles: Mars = deployment of troops / violent death; Saturn = confusion / dislocation; Jupiter = new order / resurrection.",
        "step_3_spatial_audit":      "Identify signs and nakshatras involved and the houses they rule in the national chart.",
        "step_4_temporal_chart":     "Construct a horoscope for the exact moment of conjunction for the specific nation.",
        "step_5_orb_rule":           "Apply 1-degree orb limit; houses in which the conjunction falls are the primary impact zones.",
    },
    "historical_priority_gate": {
        "aries_1_degree_rule": (
            "Conjunctions commencing in the first degree of Aries are THE MOST IMPORTANT — "
            "these have only occurred eight times in known history. "
            "Trigger: 'Century-Level Paradigm Shift' alert (highest-level signal in the engine)."
        ),
    },
    "conjunction_profiles": {
        "saturn_jupiter_cycle": {
            "cadence":               "Every 20 years, moving through triplicities in retrograde order.",
            "great_mutation":        "First conjunction in a new triplicity (e.g., Earthy → Airy); permanent impact for next 200 years.",
            "signification_jupiter": [
                "Religion", "Philosophy", "Judiciary", "Finances", "Capitalism", "Treaties",
                "External Affairs", "Ambassadors", "Prosperity/Peace", "International Cooperation",
                "Birth Rate", "Resurrection/New Order", "Royalty", "Constitutional Governments",
            ],
            "signification_saturn":  [
                "Death", "National Calamities", "Contraction", "Diseases", "War",
                "Loss/Gain of Territory", "Agitation", "Strikes", "Labor Classes",
                "Democracy", "Farmers", "Miners", "Dictators", "Rulers of the Country",
            ],
            "primary_mundane_result": "Turning points where an old order dies and a new order takes over.",
            "mortality_veto":         (
                "IF Sat-Jup Conjunction occurs AND US President is elected near that date "
                "THEN Mortality_Risk = CRITICAL (High Probability: President will not complete full term)."
            ),
            "triplicity_results": {
                "earthy":  "Material growth, shifts in world financial dominance.",
                "fiery":   "Wars of ideology and rapid territorial expansion.",
                "airy":    "Technology revolutions, communications upheaval, democratic movements.",
                "watery":  "Maritime disasters, epidemics, mass displacement.",
            },
        },
        "saturn_rahu_logic": {
            "signification_rahu":   ["Muslims", "Foreigners", "Electronics", "Aggression", "Spies", "Political Plots"],
            "mundane_result":       "End of imperialism, collapse of colonialism, birth of new nation-states.",
            "modern_trigger":       "Linked to dawn of Atomic/Nuclear age (e.g., Hiroshima/Nagasaki 1945 — Sat-Rahu in Gemini).",
            "regional_collapse_gate": (
                "IF Sat-Rahu conjunction in Capricorn THEN Major_Regime_Change_Middle_East = TRUE "
                "(e.g., 1991 Gulf War: Sun, Saturn, Moon, Rahu met within 1° in Capricorn)."
            ),
            "atomic_veto":          (
                "IF Sat-Rahu conjunction in Gemini (sign of USA and technology) "
                "THEN 'Global Shift in Military Technology / Nuclear Escalation and Birth of New Sovereign States'."
            ),
            "national_humiliation_gate": (
                "IF Sat-Rahu conjunction falls in 8th or 12th house of a nation's foundation chart "
                "THEN 'National Setback / Loss of Prestige' alert."
            ),
        },
        "saturn_mars_conjunction": {
            "signification_mars":  ["Armed Forces", "Generals", "Violence", "Fire", "Assassinations", "Explosions"],
            "diagnostic_status":   "Highly Inauspicious and feared by rulers.",
            "primary_result":      "Mass massacres, internal military operations, 'Black Days' in history.",
            "internal_security_trigger": (
                "IF Sat-Mars conjunction in 6th House of national chart "
                "THEN Internal_Military_Action = TRUE (e.g., Operation Blue Star 1984)."
            ),
            "massacre_condition":  (
                "IF Sat-Mars conjunction in Dual Sign AND 6th from India's Makar Lagna "
                "THEN General_Massacre = TRUE (e.g., Nadir Shah 1739)."
            ),
            "natural_disaster_gate": (
                "IF Sat-Mars conjunction in Watery Sign (Cancer / Scorpio / Pisces) "
                "THEN Critical Tsunami / Maritime Flood Risk "
                "(e.g., 2004 Asian Tsunami — Saturn-Mars in Cancer)."
            ),
        },
        "mars_jupiter_conjunction_opposition": {
            "primary_result":      "Determines establishing of global supremacy or victory in decisive battles.",
            "historical_impact":   "Establishment of British supremacy in India (Battle of Buxar 1764).",
            "jupiter_protection_rule": (
                "IF a configuration looks like a disaster BUT Jupiter is well-placed, "
                "veto 'Total Defeat' and predict 'Victory for the Allied Force' instead."
            ),
        },
        "mars_rahu_ketu_ignition": {
            "signification_ketu":  ["Secret Plots", "Intrigues", "Assassinations", "Self-immolation", "Sudden success/failure"],
            "primary_result":      "High-intensity terrorism, suicide attacks, and coups.",
            "terrorism_gate":      (
                "IF Mars conjunct Ketu in Fiery Sign / Fiery Nakshatra "
                "THEN Extreme_Terrorist_Event = TRUE "
                "(e.g., 9/11 WTC — Mars-Ketu in Sagittarius/Moola opposing Jupiter in Gemini)."
            ),
            "explosive_logic":     "Ketu acts like Mars in secrecy; Rahu acts like Saturn with violence.",
        },
    },
    "ignition_rule": (
        "Saturn and Jupiter set the 'Hour Hand' of an era; Mars acts as the 'Minute Hand'. "
        "No prediction of war or revolution is authorized unless Mars triggers the conjunction degree "
        "by transit or aspect. Do NOT predict the event AT the moment of conjunction — "
        "wait for Mars to conjoin or aspect the conjunction degree."
    ),
    "orb_sensitivity": (
        "Apply 1-degree orb. If planets are within 1° (as in 1991 Gulf War: "
        "Sun, Saturn, Moon, Rahu within 1° in Capricorn), "
        "the diagnostic weight for 'Catastrophic Event' is TRIPLED."
    ),
    "historical_benchmark_matrix": [
        {
            "event_template":   "High-Intensity Terrorist Strike",
            "historical_anchor": "9/11 World Trade Centre (2001)",
            "core_geometry":    "Mars conjunct Ketu in Fiery Sign (Sagittarius/Moola) opposing Jupiter in Gemini (USA's sign)",
            "trigger_logic":    "Mars-Ketu within 1° in war-like nakshatra (Moola); 1-degree orb rule applies.",
        },
        {
            "event_template":   "Maritime Disaster / Tsunami",
            "historical_anchor": "2004 Asian Tsunami",
            "core_geometry":    "Saturn and Mars in mutual Kendra connection in Watery Signs (Cancer/Scorpio)",
            "trigger_logic":    "Mars afflicting Moon in watery sign while heavy planets in Graha Yuddha (planetary war).",
        },
        {
            "event_template":   "Internal Military Operation / Massacre",
            "historical_anchor": "Nadir Shah (1739) & Operation Blue Star (1984)",
            "core_geometry":    "Saturn-Mars conjunction in 6th house of national chart or in Dual Sign",
            "trigger_logic":    "'Black Day' configuration — Mars and Saturn meeting in sensitive national house.",
        },
        {
            "event_template":   "Collapse of Imperialism / Atomic Breakthrough",
            "historical_anchor": "1945 Hiroshima & Birth of New Nations",
            "core_geometry":    "Saturn-Rahu conjunction in Gemini (Sign of Air/Technology)",
            "trigger_logic":    "Conjunction acts as 'Discharge Point' for high-energy military technology.",
        },
        {
            "event_template":   "Sudden Economic Paradigm Shift",
            "historical_anchor": "1991 Gulf War & Indian Gold Crisis",
            "core_geometry":    "Multi-planet meeting (Sun, Saturn, Moon, Rahu) within 1° in fixed/earthy sign (Capricorn)",
            "trigger_logic":    "Extreme energy concentration in house of National Exchequer (2nd) or Governance (10th).",
        },
    ],
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 2: Gaur Ch 10 — Sun + Moon Transit Price Matrix
# ============================================================

GAUR_CH10_SUN_MOON_TRANSIT = {
    "spec_id":        "gaur-ch10-sun-moon-transit-price-matrix",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "transit_price_lookup",
    "title":          "Transit Price Matrix — Sun (12 Signs + 27 Constellations + Weekday Ingress + Muhurti) & Moon (12 Signs + 27 Constellations)",
    "source_chapter": "Gaur/AIFAS Ch 10",
    "description": (
        "Granular lookup tables for commodity price fluctuations driven by Sun and Moon transits. "
        "Sun results materialize 14-15 days after entry. "
        "Solar Ingress (Sankranti) is filtered by: (1) Weekday of entry, (2) Muhurti duration. "
        "Moon acts as the final 'ignition trigger' for short-term market shifts."
    ),
    "temporal_materialization": {
        "sun_constellation_entry": "14-15 day delay for result manifestation.",
        "sun_priority_rule":       "In any month where Sun transits are malefic but Moon transits are benefic, prioritize the Sun as the 'Hour Hand'.",
    },
    "transit_sun_sign_results": {
        "aries":       {"expensive": ["Gold", "Silver", "Gur", "Sugar", "Fruits", "Dry fruits", "Til", "Oil", "Ghee", "Thread"], "cheap": ["Wheat", "Pulses"]},
        "taurus":      {"expensive": ["Gold", "Silver", "Gur", "Sugar", "Juicy materials", "Til", "Oil materials", "Dry fruits"], "cheap": ["Gram", "Barley", "Grains", "Pulses"]},
        "gemini":      {"expensive": ["Gold", "Silver", "Gur", "Sugar", "Juicy materials", "Til", "Oils", "Jute materials", "Thread", "Wheat", "Gram", "Pulses"]},
        "cancer":      {"expensive": ["Gold", "Silver", "Metals", "Gur", "Sugar", "Khand", "Fruits", "Dry fruits"], "cheap": ["Wheat", "Gram", "Barley", "Pulses", "Moong", "Moth", "Arhar", "Urad"]},
        "leo":         {"expensive": ["Gold", "Silver", "Gur", "Khand", "Sugar", "Juicy materials", "Til", "Oils", "Red coloured things", "Gems"], "cheap": ["Grains", "Pulses"]},
        "virgo":       {"expensive": ["Til", "Oil materials", "Cotton", "Coconut"], "cheap": ["Cotton"]},
        "libra":       {"expensive": ["Wheat", "Wood apple", "Barley", "Gram", "Gold", "Copper", "Red sandal", "Betelnut"], "cheap": ["Cotton", "Silver"]},
        "scorpio":     {"expensive": ["Gold", "Silver", "Copper", "Cotton"], "cheap": ["Red colour things"]},
        "sagittarius": {"expensive": ["Gold", "Silver", "Cotton", "Thread", "Til", "Oil materials"], "cheap": ["Wheat", "Gram", "Barley", "Grains"]},
        "capricorn":   {"expensive": ["Gur", "Khand", "Sugar", "Juicy materials", "Cotton", "Thread", "Oil", "Ghee"], "cheap": ["Wheat", "Gram", "Jute materials"]},
        "aquarius":    {"expensive": ["Gur", "Khand", "Jute materials", "Til", "Oil materials", "Ghee", "Ground nut"], "cheap": ["Wheat", "Gram"]},
        "pisces":      {"expensive": ["Sesame", "Oils", "Oil materials", "Juicy materials", "Gur", "Khand", "Cotton", "Thread", "Gold"], "cheap": ["Grains", "Pulses"]},
    },
    "transit_sun_constellation_results": {
        "logic":           "Results materialize within 14-15 days of entry.",
        "ashwini":         {"expensive": ["Gold", "Silver", "Copper", "Iron", "Til", "Oils", "Red sandal", "Cotton cloth", "Clove", "Cardamom", "Grains"], "cheap": ["Cotton"]},
        "bharani":         {"expensive": ["Gold", "Silver", "Copper", "Metals", "Brass utensils", "Wheat", "Barley", "Gram", "Juicy materials", "Gur", "Khand", "Ghee", "Oil materials"], "cheap": ["Cotton"]},
        "krittika":        {"expensive": ["Gold", "Silver", "Wheat", "Barley", "Gram", "Moong", "Moth", "Oil materials", "Ghee"]},
        "rohini":          {"expensive": ["Wheat", "Barley", "Gram", "Gur", "Khand", "Oils", "Oil materials", "Ghee", "Woolen clothes", "Cotton clothes", "Chillies"], "cheap": ["Silver"]},
        "mrigshira":       {"expensive": ["Gold", "Silver", "Moong", "Moth", "Urad", "Pulses", "Gram", "Millet", "Water-cultivated materials"]},
        "ardra":           {"expensive": ["Wheat", "Gram", "Rice", "Barley", "Silver", "Cotton", "Oil cake"], "cheap": ["Gold"]},
        "punarvasu":       {"expensive": ["Gur", "Khand", "Cotton", "Thread", "Til", "Oil materials", "Pulses", "Grocery materials"]},
        "pushya":          {"expensive": ["Wheat", "Barley", "Gram", "Rice", "Til", "Oils", "Oil materials", "Gold", "Silver", "Woolen clothes"], "cheap": ["Cotton", "Thread"]},
        "ashlesha":        {"expensive": ["Wheat", "Rice", "Gram", "Urad", "Moong", "Gold", "Silver", "Oils", "Ghee", "Chillies"]},
        "magha":           {"expensive": ["Til", "Oil materials", "Moong", "Silver"]},
        "poorvaphalguni":  {"expensive": ["Wheat", "Gur", "Khand", "Oils", "Oil materials", "Ghee", "Woolen clothes", "Cotton clothes", "Gold"], "cheap": ["Silver"]},
        "uttaraphalguni":  {"expensive": ["Gold", "Silver", "Iron", "Til", "Oil materials", "Ghee", "Rice", "Urad", "Cotton"]},
        "hast":            {"expensive": ["Barley", "Wheat", "Gur", "Khand", "Turmeric", "Coriander"]},
        "chitra":          {"expensive": ["Gold", "Silver", "Gram", "Pulses", "Yarn", "Red clothes", "Gur", "Khand"]},
        "swati":           {"expensive": ["Gold", "Silver", "Gur", "Khand", "Oil materials", "Perfumes", "Yarn", "Silk clothes"]},
        "vishakha":        {"expensive": ["Wheat", "Rice", "Barley", "Pulses", "Til", "Oil materials", "Gur", "Khand"], "cheap": ["Silver"]},
        "anuradha":        {"expensive": ["Wheat", "Barley", "Woollen clothes"], "cheap": ["Wheat", "Gold", "Silver"]},
        "jyeshtha":        {"expensive": ["Gold", "Silver", "Wheat", "Barley", "Gram", "Rice", "Oil materials", "Perfumes", "Gur", "Khand"], "cheap": ["Cotton"]},
        "mool":            {"cheap": ["Gold", "Silver", "Cotton", "Yarn"]},
        "poorvashadh":     {"expensive": ["Gur", "Khand", "Woolen clothes", "Silver", "Til", "Oil materials"]},
        "uttarashadh":     {"expensive": ["Wheat", "Gram", "Rice", "Moong", "Urad", "Gur", "Khand", "Oil materials", "Jute goods"]},
        "shravan":         {"expensive": ["Wheat", "Barley", "Rice", "Gur", "Khand", "Gold", "Silver", "Yarn"]},
        "dhanishtha":      {"expensive": ["Wheat", "Pulses", "Gold", "Silver", "Gems", "Cotton", "Yarn"]},
        "shatbhisha":      {"expensive": ["Wheat", "Til", "Oil materials", "Gur", "Gold", "Silver", "Cotton clothes", "Perfumery"]},
        "poorvabhadrapad": {"expensive": ["Wheat", "Gram", "Pulses", "Gur", "Khand", "Oils", "Oil materials", "Ghee", "Gold", "Silver", "Clothes"]},
        "uttarabhadrapad": {"expensive": ["Wheat", "Rice", "Gur", "Khand", "Oils"]},
        "revati":          {"expensive": ["Wheat", "Gram", "Rice", "Oil materials", "Peanuts", "Cotton"]},
    },
    "transit_sun_weekday_ingress_filter": {
        "aries_ingress":      {"sun_tue_sat": ["Wheat", "Gram", "Barley", "Majeeth", "Saffron expensive"], "mon": ["Gur", "Khand", "Oils", "Oil materials", "Cotton expensive"], "thu": "Grains cheap", "wed_fri": ["Grains cheap", "White things cheap", "Sugar cheap"]},
        "taurus_ingress":     {"sun_tue_sat": ["Grains", "Gur", "Khand", "Dry fruits", "Grocery expensive"], "mon": "Grains expensive", "wed_thu_fri": ["Grains cheap", "Oils", "Oil materials", "Cotton", "White things", "Sugar expensive"]},
        "gemini_ingress":     {"sun_tue_sat": ["Grains expensive"], "wed": ["Gems expensive"], "mon_thu_fri": ["Grains expensive", "Yarn expensive"]},
        "cancer_ingress":     {"sun_tue": ["Wheat", "Gram", "Gur", "Khand", "Ghee expensive"], "mon_thu_fri": "Grains cheap", "wed": "Trees break due to high winds; birds destroyed", "sat": ["Grains expensive", "Gold", "Silver", "Copper cheap"]},
        "leo_ingress":        {"sun_tue_sat": ["Pulses (Moong, Moth, Urad) expensive"], "thu": ["Rains more frequent", "Ghee cheap", "Oils and oil materials expensive", "Gur and khand expensive"], "mon_wed_fri": ["Grains cheap"]},
        "virgo_ingress":      {"sun": ["Grains expensive", "Gold and silver expensive", "Gur and sugar expensive"], "mon": ["Grains and pulses expensive", "Oil materials and gur expensive", "Silver and khand cheap"], "tue": ["Pulses and wheat expensive", "Cuminseed and spices expensive"], "wed": ["Ghee cheap", "Silver cheap"], "thu": ["Wheat cheap", "Gold cheap"], "fri": ["Grains cheap"], "sat": ["Ghee, gur, and khand expensive", "Cotton cheap", "Gold and silver medium"]},
        "libra_ingress":      {"sun": ["Grains expensive", "Spices expensive", "Pulses cheap"], "mon": ["Grains medium", "Gur and khand expensive", "Silver, rice, and pulses cheap"], "tue": ["Grains, chillies, spices, gold, and silver medium", "Arhar expensive", "Rice and cattle cheap"], "wed": ["Wheat and rice cheap", "White things cheap", "Oils and oil materials expensive"], "thu": ["Grains and pulses cheap", "Oil materials and gold expensive"], "fri": ["Grains cheap", "Gur, khand, and gold expensive"], "sat": ["Wheat, rice, gram, gur, khand, ghee, and oil materials expensive", "Cotton and silver cheap"]},
        "scorpio_ingress":    {"sun": ["Grains, oils, gold, silver, turmeric, chillies expensive"], "mon": ["Grains, silver, and ghee cheap", "Gold, iron, and oil materials expensive"], "tue": ["Grains, pulses, gur, and khand cheap"], "wed": ["Gur, khand, rice, silver, and cotton cheap", "Clothes and red colour goods expensive"], "thu": ["Gur, khand, oils, and red colour goods expensive", "Pulses, gold, silver cheap"], "fri": ["Grains and oils expensive", "Gold and silver initially expensive then cheap"], "sat": ["Grains cheap after fluctuations", "Iron, brass, and millet high prices"]},
        "sagittarius_ingress": {"sun": ["Grains, gold, oils, gur, khand medium price", "Grocery materials expensive"], "mon": ["Wheat, rice, and silver cheap", "Oils, iron, and red colour things expensive"], "tue": ["Grains, oils, ghee, cotton, silver expensive", "Pulses cheap"], "wed": ["Pulses, dry fruits, and spices cheap"], "thu": ["Grains cheap", "Moong, urad, silver expensive"], "fri": ["Gold and silver expensive", "Gur, oils cheap with fluctuations"], "sat": ["Grains, gold, silver, cotton expensive", "Ghee and rice cheap"]},
        "capricorn_ingress":  {"sun": ["Grains, gur, oil, arhar, and spices expensive"], "mon": ["Grocery, gur, khand, gold, cotton, silver, rice, ghee, oil cheap", "Pulses medium"], "tue": ["Grains, gur, khand, and oils expensive", "Ghee and pulses cheap"], "wed": ["Dry fruits expensive", "Gold, silver, and yarn cheap", "Ghee and rice cheap"], "thu": ["Grains, gur, khand, and ghee cheap"], "fri": ["Wheat, gram, gur, and khand cheap"], "sat": ["Grains expensive after fluctuations", "Gur, khand, oil cheap", "Gold expensive", "Silver cheap"]},
        "aquarius_ingress":   {"sun": ["Grains expensive", "Gur, khand, maize, cotton clothes, oil materials cheap"], "mon": ["Wheat, barley, gram, gold, silver cheap", "Moong, urad, oils expensive"], "tue": ["Wheat, gram, and pulses expensive", "Gold, silver, brass, zinc cheap"], "wed": ["Wheat, barley, gram, peas, and spices cheap", "Moong, urad, tuar expensive"], "thu": ["Moong, moth, rice, millet, gold, silver, copper, dry fruits, oils cheap", "Wheat, barley, silk expensive"], "fri": ["Millet and maize cheap", "Wheat and gram expensive with fluctuations", "Grocery, gur, khand, sugar expensive"], "sat": ["Wheat, gram, salt, chillies, ghee, and milk expensive", "Moong, moth, and urad cheap"]},
        "pisces_ingress":     {"sun": ["Gold and silver cheap", "Fluctuations in wheat, gram, ghee, oil, gur"], "mon": ["Wheat, gram, oils, mustard, cotton, ghee, milk expensive"], "tue": ["Wheat, gram, cotton, moong, urad, masoor, gold, milk expensive", "Ghee cheap"], "wed": ["Wheat, barley, gram, milk, and perfumes medium price"], "thu": ["Grains cheap", "Moong, urad, spices, oils, cotton, copper expensive", "Gold, silver, dry fruits cheap"], "fri": ["Gold, silver, gur, khand, sugar, wheat, salt, and chillies expensive"], "sat": ["Wheat, gram, barley, oils, gur, khand, sugar medium", "Red colour things expensive"]},
    },
    "transit_sun_muhurti_filter": {
        "15_muhurti": {
            "stars":  ["Bharani", "Ardra", "Ashlesha", "Jyeshtha", "Shatbhisha"],
            "result": "Grains and juicy materials expensive; rains less.",
        },
        "30_muhurti": {
            "stars":  ["Ashwini", "Krittika", "Mrigshira", "Pushya", "Magha", "Poorvaphalguni", "Hast", "Chitra", "Anuradha", "Mool", "Poorvashadh", "Shravan", "Dhanishtha", "Poorvabhadrapad", "Revati"],
            "result": "Grains, grass, and juicy materials at medium price.",
        },
        "45_muhurti": {
            "stars":  ["Rohini", "Punarvasu", "Uttaraphalguni", "Vishakha", "Uttarashadh", "Uttarabhadrapad"],
            "result": "Good rains; grains, ghee, oil, and cotton cheap. Muhurti logic OVERRIDES general sign/star results.",
        },
        "muhurti_overrule_principle": (
            "Prioritize Muhurti Logic over general Sign/Star logic. "
            "IF ingress is 45 Muhurtis, return 'Good Rainfall' even if planets are in dry constellations."
        ),
    },
    "transit_moon_sign_results": {
        "aries":       {"expensive": ["Wheat", "Gram", "Barley"], "cheap": ["Gold", "Silver"]},
        "taurus":      {"expensive": ["Wheat", "Urad", "Peanut", "Cotton", "Silver"], "cheap": ["Cattle"]},
        "gemini":      {"expensive": ["Wheat", "Gram", "Cotton", "Yarn"]},
        "cancer":      {"cheap": ["Gold", "Silver", "Cotton", "Yarn"]},
        "leo":         {"expensive": ["Gold", "Silver", "Cotton"]},
        "virgo":       {"expensive": ["Gold", "Silver"], "cheap": ["Cotton"]},
        "libra":       {"cheap": ["Gold", "Silver", "Rice", "Ghee", "Cotton"]},
        "scorpio":     {"cheap": ["Gold", "Silver", "Cotton"]},
        "sagittarius": {"cheap": ["Cotton", "Yarn", "Oils"]},
        "capricorn":   {"expensive": ["Gold", "Silver", "Clothes", "Fruits"]},
        "aquarius":    {"cheap": ["Gold", "Silver", "Cotton", "Yarn"], "expensive": ["Oils"]},
        "pisces":      {"expensive": ["Gold", "Oil materials"], "cheap": ["Silver"]},
    },
    "transit_moon_rise_in_constellations": {
        "ashwini":         {"cheap": ["Gold", "Silver", "Cotton"]},
        "bharani":         {"cheap": ["Silver", "Cotton", "Salt"]},
        "krittika":        {"cheap": ["Silver"], "expensive": ["Cotton"]},
        "rohini":          {"expensive": ["Wheat", "Gram", "Gur", "Khand"]},
        "mrigshira":       {"cheap": ["Gold", "Silver", "Cotton"]},
        "ardra":           {"expensive": ["Gold", "Silver", "Copper", "Gur", "Khand"]},
        "punarvasu":       {"cheap": ["Gold", "Silver", "Wheat", "Gram", "Moong", "Urad"]},
        "pushya":          {"cheap": ["Gold", "Silver", "Gur", "Khand", "Cotton", "Wheat"]},
        "ashlesha":        {"cheap": ["Gold", "Silver", "Cotton"]},
        "magha":           "Prices of gold, silver, and cotton fluctuate",
        "poorvaphalguni":  {"cheap": ["Silver", "Wheat", "Gram", "Gur", "Khand"]},
        "uttaraphalguni":  {"cheap": ["Gold", "Silver", "Copper"]},
        "hast":            {"cheap": ["Gold", "Silver", "Copper"], "expensive": ["Oil materials"]},
        "chitra":          {"expensive": ["Gold", "Silver", "Wheat", "Gram", "Moong"]},
        "swati":           {"cheap": ["Gold", "Silver", "Cotton"]},
        "vishakha":        {"expensive": ["Gold", "Silver", "Cotton", "Yarn"], "cheap": ["Oils"]},
        "anuradha":        {"cheap": ["Gold", "Silver"], "expensive": ["Wool"]},
        "jyeshtha":        {"cheap": ["Silver", "Cotton", "Yarn"]},
        "mool":            {"expensive": ["Silver", "Cotton", "White clothes"]},
        "poorvashadh":     {"cheap": ["Gold", "Brass", "Gur", "Khand"]},
        "uttarashadh":     {"cheap": ["Gold", "Silver", "Gur", "Khand", "Salt", "Fruits"]},
        "shravan":         {"cheap": ["Gold", "Silver", "Grains"]},
        "dhanishtha":      {"expensive": ["Gold", "Silver"], "cheap": ["Gur", "Khand"]},
        "shatbhisha":      {"cheap": ["Gold"], "expensive": ["Silver"]},
        "poorvabhadrapad": {"cheap": ["Gold", "Silver", "Cotton", "Grains"]},
        "uttarabhadrapad": {"cheap": ["Gold", "Silver", "Cotton", "Clothes"]},
        "revati":          {"cheap": ["Gold", "Silver", "Fruits"]},
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 3: Gaur Ch 10 — Saturn Transit Price Matrix
# ============================================================

GAUR_CH10_SATURN_TRANSIT = {
    "spec_id":        "gaur-ch10-saturn-transit-price-matrix",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "transit_price_lookup",
    "title":          "Transit Price Matrix — Saturn (12 Signs w/ Navamsh + 27 Constellations w/ Pad + Direct/Retrograde Logic)",
    "source_chapter": "Gaur/AIFAS Ch 10",
    "description": (
        "Saturn is the ultimate arbiter of long-term commodity cycles — "
        "its transit is measured by Navamshas (3°20' segments) within a sign and Pads within a constellation. "
        "Direct vs. Retrograde motion produces opposite price results. "
        "Special retrograde re-entry triggers (Uttarashadh→Poorvashadh) activate famine protocol."
    ),
    "metadata": {
        "planet":           "Saturn",
        "nature":           "Cold / Contracting / Chronic",
        "primary_significations": ["Farmers", "Laborers", "Mines", "Coal", "Oils", "Iron", "Machinery", "Famines", "Diseases"],
        "duration_logic":   {
            "sign_entry":           "~2.5 years per sign",
            "retrograde_to_direct": "Oils, chillies, asafetida expensive for 2 months.",
            "direct_to_retrograde": "Oils, grains, and ghee become expensive.",
        },
    },
    "transit_sign_results_with_navamsh": {
        "aries":       {"expensive": ["Oils", "Juicy materials", "Gold", "Silver", "Copper", "Gems", "Machinery", "Hardware"], "critical_threshold": "At 28-29°: sharp price decline for hardware, gems, metals."},
        "taurus":      {"expensive": ["Grains", "Oils", "Oil materials", "Jute products", "Gur", "Khand"], "navamsh_logic": "Less influential in 1st Navamsh; cheap results in last 2 Navamshas."},
        "gemini":      {"expensive": ["Oils", "Grains", "Juicy materials", "Iron machine parts"], "navamsh_logic": "Prices gradually decrease as Saturn passes through each Navamsh."},
        "cancer":      {"expensive": ["Oils", "Oil materials", "Gold", "Silver", "Cotton"], "navamsh_logic": "High prices in first 3 and last 3 Navamshas; low prices in middle 3 Navamshas."},
        "leo":         {"expensive": ["Oil materials", "Juicy materials", "Grains", "Pulses"], "navamsh_logic": "Peak high prices specifically in the 3rd Navamsh."},
        "virgo":       {"cheap": ["Gold", "Silver", "Gems", "Gur", "Khand"], "navamsh_logic": "1st Navamsh makes juices particularly cheap; later Navamshas make grains expensive."},
        "libra":       {"expensive": ["Grains", "Pulses", "Juicy materials"], "price_pivot": "Oils become cheap after Saturn passes 15°."},
        "scorpio":     {"expensive": ["Oils", "Oil materials", "Grains", "Silver"], "benefic_veto": "Prices fall if Saturn is under benefic influence."},
        "sagittarius": {"expensive": ["Grains", "Juicy materials", "Wood", "Wooden materials", "Iron machine parts"], "benefic_veto": "Benefic influence makes grains cheap."},
        "capricorn":   {"result": "All commodities become unstable."},
        "aquarius":    {"cheap": ["Grains"]},
        "pisces":      {"expensive": ["Grains"]},
    },
    "transit_constellation_pad_results": {
        "ashwini":         "Oils, grains, yarn, red chillies, and ghee expensive up to 1°; cheap thereafter. Cotton cheap up to 1°, expensive thereafter.",
        "bharani":         {"3rd_pad": "Oils, ghee, gur, and khand expensive."},
        "krittika":        {"general": "Metals (gold/silver) expensive; grains cheap.", "3rd_4th_pad": "Oils expensive."},
        "rohini":          {"1st_3rd_pad": "Grains and pulses cheap; gold and silver expensive.", "2nd_4th_pad": "Grains and pulses expensive; gold and silver cheap."},
        "mrigshira":       {"1st_3rd_pad": "Grains and pulses cheap; gold and silver fluctuate.", "2nd_pad": "Grains and pulses expensive.", "4th_pad": "Grains, pulses, oils, and juicy materials expensive."},
        "ardra":           {"1st_pad": "Grains, juices, oils, ghee cheap.", "2nd_pad": "Grains and pulses expensive.", "3rd_4th_pad": "Grains and pulses cheap."},
        "punarvasu":       {"expensive": ["Grains", "Cotton"], "cheap": ["Oils", "Machinery parts"]},
        "pushya":          {"1st_pad": "Grains cheap; gur and khand expensive.", "2nd_3rd_pad": "Grains expensive; ghee, gur, khand cheap.", "4th_pad": "Grains cheap; ghee and gur expensive."},
        "ashlesha":        {"1st_pad": "Grains, til, oil materials, iron machinery cheap.", "remaining_pads": "All above become expensive."},
        "magha":           {"1st_pad": "Oils, ghee, gur, khand expensive.", "2nd_pad": "Oils/ghee/juices cheap; dry fruits, perfumes expensive.", "3rd_pad": "All materials expensive.", "4th_pad": "All cheap; ghee expensive."},
        "swati":           {"1st_pad": "Grains cheap.", "2nd_pad": "Grains/Oils/Iron expensive.", "4th_pad": "Juices/Ghee expensive."},
        "mool":            {"expensive": ["Grains", "Oils", "Silver"], "4th_pad": "Prices become low."},
        "poorvashadh":     {"cheap": ["Grains"], "1st_pad": "Oils and grocery cheap."},
        "shravan":         {"1st_3rd_pad": "Grains expensive.", "2nd_4th_pad": "Grains cheap."},
        "shatbhisha":      {"1st_2nd_pad": "Grains/Pulses/Juices cheap.", "3rd_4th_pad": "Expensive."},
        "revati":          {"cheap": ["Gold", "Silver"], "expensive": ["Grains", "Oils", "Pulses"], "4th_pad": "Juices expensive."},
    },
    "direct_motion_sign_ingress": {
        "aries":       "Grains expensive",
        "taurus":      "Metals cheap",
        "gemini":      "Ghee / Silver / Cotton cheap",
        "cancer":      "Red chillies / Oils cheap",
        "leo":         "Grocery cheap",
        "virgo":       "Oils / Juices cheap",
        "libra":       "Silver expensive",
        "scorpio":     "Chillies expensive; Coriander cheap",
        "sagittarius": "Grains expensive; Oils cheap",
        "aquarius":    "Grains cheap",
        "pisces":      "Grains expensive",
    },
    "retrograde_motion_sign_entry": {
        "aries":       "Oils expensive",
        "taurus":      "Grains / Peanuts expensive",
        "gemini":      "Wheat / Pulses expensive",
        "cancer":      "Chillies / Oils expensive",
        "leo":         "Grocery expensive",
        "virgo":       "Grains / Juices expensive",
        "libra":       "Silver cheap",
        "scorpio":     "Spices cheap",
        "sagittarius": "Juices expensive; Oils cheap",
        "aquarius":    "Grains expensive",
        "pisces":      "Grains cheap",
    },
    "motion_and_luminous_logic": {
        "change_to_direct":    "Oils, chillies, and asafetida expensive for 2 months.",
        "change_to_retrograde": "Oils, grains, and ghee become expensive.",
        "rising_state":        "Mustard oil, peanuts, and cotton cheap for 1 month; Iron, gur, and khand expensive.",
        "combusted_state":     "Gold etc. cheap; Grains expensive.",
    },
    "special_retrograde_triggers": {
        "famine_gate":  "IF Saturn retrograde in Uttarashadha re-enters Poorvashadh THEN 'Severe Drought and Grain Crisis' — 12-year famine protocol.",
        "market_spike": "IF Saturn retrograde in Magha re-enters Ashlesha THEN 'Wheat and Ghee become expensive'.",
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 4: Gaur Ch 10 — Transit Timing & Methodology
# ============================================================

GAUR_CH10_TRANSIT_METHODOLOGY = {
    "spec_id":        "gaur-ch10-transit-timing-methodology",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "operational_framework",
    "title":          "Transit Timing Rules and Diagnostic Methodology — Materialization Offsets, Retrograde Vetoes, Grahayudha",
    "source_chapter": "Gaur/AIFAS Ch 10",
    "description": (
        "Operational rules governing HOW transit results manifest — timing delays, motion-state vetoes, "
        "planetary war (Grahayudha) effects, and the composite diagnostic gate combining weekday + muhurti. "
        "Applies to all planetary transit queries."
    ),
    "temporal_materialization_rules": {
        "sun_constellation_entry":    "14-15 day delay for result manifestation.",
        "mars_sign_impact_duration":  "15 days to 1 month.",
        "mars_constellation_duration": "12-24 days.",
        "mars_rise_impact":           "5 day delay for price rise manifestation.",
        "saturn_rise_impact":         "1 month duration for price shifts.",
        "saturn_sign_duration":       "~2.5 years per sign.",
    },
    "composite_diagnostic_gate": (
        "For any Solar Ingress query: "
        "(1) Identify the Weekday of entry — sets the commodity pivot for that month; "
        "(2) THEN apply Muhurti filter — if 45 Muhurtis, override all dry-sign results with 'Good Rainfall'; "
        "(3) THEN apply general sign/star results; "
        "(4) Sun's trend takes priority over Moon's trend ('Hour Hand' rule)."
    ),
    "grahayudha_audit": (
        "IF Mercury, Mars, Jupiter, or Saturn are involved in a transit, "
        "audit for Grahayudha (closeness in degrees). "
        "The 'loser' of the planetary war indicates a sudden market crash for its ruled commodities."
    ),
    "direct_retrograde_veto": (
        "ALWAYS check motion state before applying sign/constellation results. "
        "Direct and Retrograde motion produce OPPOSITE effects for Saturn (and often Mars). "
        "Example: Direct Saturn in Aries = Grains expensive; Retrograde Saturn in Aries = Oils expensive."
    ),
    "drought_ingress_alert": (
        "IF Sun enters any sign on Sunday / Tuesday / Saturday AND ingress is 15 Muhurtis "
        "THEN 'Critical Water Scarcity and Food Inflation Alert'."
    ),
    "mars_sun_overtake_trigger": (
        "IF Mars is ahead of the Sun during the rainy season (Sun in Gemini/Cancer) "
        "THEN 'Monsoon Failure: Rains will be obstructed or delayed'."
    ),
    "mercury_venus_break_monitor": (
        "IF Sun is positioned between Mercury and Venus during transit "
        "THEN 'Dry Spell Warning' for the agricultural sector."
    ),
    "working_class_veto": (
        "IF Saturn is afflicted in the 6th or 10th house of the national chart "
        "THEN 'National Alert: Widespread strikes, labor discontent, and industrial stagnation'."
    ),
    "28_degree_aries_marker": (
        "When Saturn reaches 28–29° Aries, trigger 'Bearish Market Correction Alert' "
        "for hardware, gems, and metals."
    ),
    "2_month_inflation_trigger": (
        "When Saturn changes from retrograde to direct, output: "
        "'Price Spike Warning: Oils and Spices (Asafetida/Chillies) expensive for the next 60 days'."
    ),
    "first_letter_routing": (
        "For commodities not in the master list, determine the zodiac sign by the first letter of the commodity name "
        "(e.g., items starting with 'A' → Aries lookup). "
        "Apply the relevant sign-level price vector."
    ),
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
ALL_SPECS = [
    MEHTA_CH10_MACRO_CONJUNCTION,
    GAUR_CH10_SUN_MOON_TRANSIT,
    GAUR_CH10_SATURN_TRANSIT,
    GAUR_CH10_TRANSIT_METHODOLOGY,
]

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_SPECS)} engine specs from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        for s in ALL_SPECS:
            print(f"  {s['spec_id']}")
        print(f"\nTotal: {len(ALL_SPECS)}\nDry run complete.")
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
