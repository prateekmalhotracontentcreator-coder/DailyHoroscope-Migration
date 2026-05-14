"""
Mundane Astrology — Engine Specs v13
Batch: mundane-engine-v13-20260506

Sources:
  Gaur/AIFAS Ch 4  — Koorma Chakra (Tortoise Chart spatial grid)
  Gaur/AIFAS Ch 4  — Zodiac → Country/Region geographical mapping
  Gaur/AIFAS Ch 4  — 12-House → Government Ministry cabinet
  Gaur/AIFAS Ch 4  — Planetary elemental nature (incl. Uranus/Neptune/Pluto)
  Gaur/AIFAS Ch 11 — Eclipse engine (monthly + zodiac triggers)
  Mehta Ch 8       — Sanghatta Chakra grid mechanics + war logic
  Mehta/Gaur Ch 8  — Sanghatta Vedha Vector Matrix (Rashi + Nakshatra)
  Mehta/Gaur Ch 8  — Commodity Ownership Dictionary (planetary + zodiac + nakshatra)

8 engine specs in this batch.

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
_BATCH     = "mundane-engine-v13-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ============================================================
# SPEC 1: Koorma Chakra — 9-Direction Grid
# ============================================================

GAUR_CH4_KOORMA_GRID = {
    "spec_id":        "gaur-ch4-koorma-chakra-grid",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "spatial_diagnostic_grid",
    "title":          "Koorma Chakra — 9-Direction Tortoise Grid (27 Nakshatras mapped to Directions)",
    "source_chapter": "Gaur/AIFAS Ch 4",
    "description": (
        "The Koorma Chakra imagines a landmass as a tortoise. "
        "The 27 nakshatras are mapped to nine specific tortoise body parts "
        "corresponding to the eight cardinal/inter-cardinal directions plus the centre. "
        "Malefic occupation, aspect, or Vedha on a nakshatra afflicts the corresponding region."
    ),
    "koorma_chakra_grid": {
        "center_back": {
            "constellations": ["Krittika", "Rohini", "Mrigshira"],
            "direction":      "Central India / Interior Heartland",
        },
        "mouth_east": {
            "constellations": ["Ardra", "Punarvasu", "Pushya"],
            "direction":      "East",
        },
        "front_right_foot_southeast": {
            "constellations": ["Ashlesha", "Magha", "Poorvaphalguni"],
            "direction":      "South-East",
        },
        "right_stomach_south": {
            "constellations": ["Uttaraphalguni", "Hast", "Chitra"],
            "direction":      "South",
        },
        "back_right_foot_southwest": {
            "constellations": ["Swati", "Anuradha", "Vishakha"],
            "direction":      "South-West",
        },
        "tail_west": {
            "constellations": ["Jyeshtha", "Mool", "Poorvashadh"],
            "direction":      "West",
        },
        "back_left_foot_northwest": {
            "constellations": ["Uttarashadh", "Shravan", "Dhanishtha"],
            "direction":      "North-West",
        },
        "left_stomach_north": {
            "constellations": ["Shatbhisha", "Poorvabhadrapad", "Uttarabhadrapad"],
            "direction":      "North",
        },
        "front_left_foot_northeast": {
            "constellations": ["Revati", "Ashwini", "Bharani"],
            "direction":      "North-East",
        },
    },
    "suffering_logic": (
        "IF malefic planet occupies, aspects, or creates Vedha on a nakshatra in a grid segment, "
        "the corresponding geographical direction/region suffers calamities, downfalls, or lack of progress."
    ),
    "prosperity_logic": (
        "IF benefic planet influences a nakshatra in a grid segment, "
        "the corresponding region enjoys Anand (bliss) and progress."
    ),
    "diagnostic_alerts": {
        "west_coast_alert": (
            "IF Saturn or Rahu transits Tail constellations (Jyeshtha, Mool, Poorvashadh) "
            "THEN Critical Vulnerability Alert for West India / Gujarat / Rajasthan for war or natural calamity."
        ),
        "inland_rebellion_monitor": (
            "IF malefic afflicts Back constellations (Krittika, Rohini, Mrigshira) "
            "THEN Unrest in Heartland / Central Provinces alert."
        ),
        "northeast_enemy_attack": (
            "IF Mars is in the 7th house in a Front Foot constellation (e.g., Revati) "
            "THEN enemy attack from North-East direction is predicted."
        ),
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 2: Koorma Fractal Scaling
# ============================================================

GAUR_CH4_KOORMA_FRACTAL = {
    "spec_id":        "gaur-ch4-koorma-fractal-scaling",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "operational_framework",
    "title":          "Koorma Chakra — Fractal Scaling (5 Resolution Levels)",
    "source_chapter": "Gaur/AIFAS Ch 4",
    "description": (
        "The Koorma Chakra is a fractal spatial tool. "
        "The same tortoise grid is superimposed at five different levels of geographical resolution, "
        "allowing the engine to pinpoint suffering or prosperity down to village level."
    ),
    "fractal_scales": [
        "1. Map of the World",
        "2. Map of the Country",
        "3. Map of the Province / State",
        "4. Map of the District or City",
        "5. Map of the Village or piece of land",
    ],
    "resolution_logic": (
        "The engine must identify the Resolution Level of a query. "
        "If a user asks about 'South India', use the Country-level Koorma Chakra (Taurus/Virgo/Leo focus). "
        "If the user asks about 'Chennai', use the City-level Koorma Chakra superimposed on that city's map."
    ),
    "diagnostic_trigger": (
        "Affliction (Vedha) or direct aspect by malefics on a specific constellation "
        "causes suffering in the corresponding geographical area AT THE QUERIED RESOLUTION LEVEL."
    ),
    "vedha_synchronization": (
        "A regional alert is only valid if a malefic is BOTH transiting the Koorma segment "
        "AND creating a Vedha on those specific constellations (links to Sarvatobhadra Chakra, Ch 9)."
    ),
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 3: Zodiac → Geographical Mapping
# ============================================================

GAUR_CH4_ZODIAC_GEO_MAP = {
    "spec_id":        "gaur-ch4-zodiac-geographical-mapping",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "lookup_table",
    "title":          "Zodiac Sign → Country / Region Geographical Mapping",
    "source_chapter": "Gaur/AIFAS Ch 4 (expanded; cross-validated with Raphael Ch 28)",
    "description": (
        "Maps each zodiac sign to the countries, regions, and Indian states it governs. "
        "Used to route planetary transit alerts to specific geographies."
    ),
    "zodiac_geographical_mapping": {
        "aries":       ["England", "Denmark", "Germany", "Poland", "Palestine", "Syria",
                        "Japan", "Madras (Chennai)", "Nepal", "Sri Lanka"],
        "taurus":      ["Ireland", "Iran", "Poland", "Georgia", "Cyprus", "White Russia",
                        "Madhya Pradesh", "Australia", "Germany"],
        "gemini":      ["USA (North)", "Belgium", "Norway", "Lower Egypt", "Western Britain",
                        "Armenia", "Tripoli", "Wales", "Africa", "Jaipur", "Haryana"],
        "cancer":      ["Scotland", "Holland", "New Zealand", "West Africa", "Mauritius",
                        "Sindh", "China", "Canada"],
        "leo":         ["France", "Italy", "Bohemia", "Sicily", "Northern Romania",
                        "Alps", "Kabul", "Vindhyachal"],
        "virgo":       ["Turkey", "West Indies", "Switzerland", "Greece", "Virginia",
                        "Brazil", "Malwa", "Pakistan", "Baghdad"],
        "libra":       ["Austria", "Indo-China", "China", "Tibet", "Caspian", "Upper Egypt",
                        "Myanmar", "Argentina", "Kashmir", "Marwar", "Japan", "USA", "Australia"],
        "scorpio":     ["Algeria", "Morocco", "Norway", "North Syria", "Queensland",
                        "Surat", "Brazil", "Washington"],
        "sagittarius": ["Arab countries", "Australia", "Hungary", "Spain",
                        "France (Provinces)", "Madagascar", "Toronto", "Uttar Pradesh"],
        "capricorn":   ["India (Overall)", "Afghanistan", "Albania", "Greece", "Syria",
                        "Mexico", "Punjab", "Bangladesh", "West Bengal"],
        "aquarius":    ["Arab countries", "Prussia", "Russia", "Poland", "Sweden", "Abyssinia"],
        "pisces":      ["Portugal", "Normandy", "Sahara Desert", "Himachal Pradesh", "Egypt"],
    },
    "routing_rule": (
        "IF malefic transits a sign THEN route the calamity alert to ALL countries mapped to that sign. "
        "IF benefic transits THEN route the prosperity signal to those same countries. "
        "Cross-validate with Raphael Ch 28 sign–country table for confirmation."
    ),
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 4: 12-House → Government Ministry Cabinet
# ============================================================

GAUR_CH4_HOUSE_MINISTRY = {
    "spec_id":        "gaur-ch4-mundane-house-ministry-cabinet",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "lookup_table",
    "title":          "12-House → Government Department / Ministry Mapping",
    "source_chapter": "Gaur/AIFAS Ch 4",
    "description": (
        "Maps each of the 12 houses in a mundane horoscope to the corresponding government department. "
        "Used as the primary administrative diagnostic layer."
    ),
    "mundane_house_ministry_cabinet": {
        "house_1":  "Home Ministry, Common People, National Health, Climate",
        "house_2":  "National Treasure, Banking, Share Market, Revenue, Import-Export",
        "house_3":  "Post & Telegraph, Railways, Telephone, Transport, Press",
        "house_4":  "Agriculture Dept, Water, Mines, Opposition Parties, Education",
        "house_5":  "Birth Rate, Education Dept, Entertainment, Administrative Wisdom",
        "house_6":  "Navy, Army, Mass Diseases, Labour Force, Health Ministry",
        "house_7":  "International Trade, Foreign Affairs, International Disputes, Rebellions",
        "house_8":  "Natural Calamities, Suicides, Accidents, Mortality Rate",
        "house_9":  "Courts, Judges, Religious Institutions, Air Force, Science/Tech",
        "house_10": "President of the Country, Ruling Party, Power to Rule, Discipline",
        "house_11": "Parliament, Prime Minister, Law & Order System, National Revenue",
        "house_12": "Jails, Intelligence Department, Secret Service, Foreign Attack",
    },
    "diagnostic_rules": {
        "home_ministry_audit": (
            "IF malefic (Saturn, Rahu, Uranus) transits the 1st House "
            "THEN trigger 'Public Health Crisis and National Mood Instability' alert."
        ),
        "parliament_audit": (
            "IF planet transits the 11th House "
            "THEN specifically audit for Prime Minister and Parliamentary Law impacts."
        ),
        "science_discovery_trigger": (
            "IF Pluto is well-aspected in the 9th House "
            "THEN predict 'Major Breakthroughs in Science and Technology' for the nation."
        ),
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 5: Planetary Elemental Nature (incl. Uranus/Neptune/Pluto)
# ============================================================

GAUR_CH4_PLANETARY_NATURE = {
    "spec_id":        "gaur-ch4-planetary-elemental-nature",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "lookup_table",
    "title":          "Planetary Elemental Nature and Mundane Significations (incl. Outer Planets)",
    "source_chapter": "Gaur/AIFAS Ch 4",
    "description": (
        "Defines each planet's element and mundane domain. "
        "Includes Uranus, Neptune, and Pluto for infrastructure/corruption/explosion queries. "
        "Used for elemental overlap analysis (e.g., Saturn-Ether + Pisces-Water = flood intensity)."
    ),
    "planetary_elemental_nature": {
        "sun": {
            "element":   "Fire",
            "role":      "Lord of planets",
            "signifies": "Kings, presidents, administrators, ministers, judges, forests, medicines",
        },
        "moon": {
            "element":   "Water",
            "nature":    "Placid",
            "signifies": "Common people, females, foods, crops, plantations",
        },
        "mars": {
            "element":   "Fire",
            "signifies": "Generals, army chiefs, armed forces, weapons, fires, surgery, accidents, wars",
        },
        "mercury": {
            "element":   "Earth",
            "signifies": "Ambassadors, trade, newspapers, literature, mental work, sports, air pollution",
        },
        "jupiter": {
            "element":   "Ether / Airy",
            "signifies": "Business management, bank employees, teachers, jurists, lawyers, religion",
        },
        "venus": {
            "element":   "Water",
            "signifies": "Females, singers, artists, birth rate, population, beauty",
        },
        "saturn": {
            "element":   "Ether",
            "signifies": "Farmers, workers, mineral producers, agriculturists, diseases, miseries",
        },
        "rahu": {
            "nature":    "Destructive",
            "signifies": "Sudden accidents, loss of cattle, anti-social elements",
        },
        "ketu": {
            "nature":    "Completion",
            "signifies": "Results similar to Rahu; takes incidents to their final conclusion",
        },
        "uranus": {
            "signifies": "Public institutions, social organizations, gas/water supplies, riots, infrastructure sabotage",
        },
        "neptune": {
            "signifies": "Rebellions, cheating, fake companies, corruption, scandals",
        },
        "pluto": {
            "signifies": "Scientific discoveries, explosions, plane piloting, mass rebellions",
        },
    },
    "elemental_overlap_rule": (
        "For environmental queries, cross-reference Planetary Element (e.g., Saturn-Ether, Venus-Water) "
        "with the Rashi Content (e.g., Pisces = 100% Water) to determine intensity of weather phenomena."
    ),
    "outer_planet_priority": (
        "Prioritize Uranus for sudden explosions and infrastructure sabotage; "
        "Neptune for corruption scandals; Pluto for scientific breakthroughs and mass upheaval."
    ),
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 6: Gaur Ch 11 — Eclipse Engine
# ============================================================

GAUR_CH11_ECLIPSE_ENGINE = {
    "spec_id":        "gaur-ch11-eclipse-monthly-zodiac-engine",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "trigger_table",
    "title":          "Eclipse Engine — Monthly and Zodiac Impact Tables (Gaur Ch 11)",
    "source_chapter": "Gaur/AIFAS Ch 11",
    "description": (
        "Eclipses are categorized as temporal triggers. "
        "Impact depends on (a) the Hindu calendar month in which the eclipse occurs "
        "and (b) the zodiac sign the eclipse falls in. "
        "Sequential order of eclipse pairs (Lunar→Solar vs Solar→Lunar) further modulates outcome."
    ),
    "monthly_eclipse_impact": {
        "chaitra":     "Variable rains (floods vs drought); suffering for intellectuals, writers, and artists",
        "baisakh":     "Good crops follow; however, armed forces experience suffering",
        "jyeshtha":    "Change of state governments; suffering for VIPs and senior executives",
        "ashadh":      "Scanty rains; rivers change course; water scarcity",
        "shravan":     "General peace, except in specific regions (Kashmir, Bhutan, Nagaland, MP)",
        "bhadrapad":   "Suffering for ladies in Saurashtra and Bangladesh",
        "ashwin":      "Surgeons and medical practitioners suffer",
        "kartik":      "Fire-workers (goldsmiths) and people of Bihar / UP suffer",
        "margsheersh": "Good crops; suffering for religious persons and border stability issues",
        "paush":       "Scanty rains; suffering for scholars and generals",
        "maagh":       "Difficult days for students and scholars",
        "phalgun":     "Hardships for actors, artists, musicians, and yogis",
    },
    "zodiac_eclipse_results": {
        "aries":       "Suffering for fire-related jobs and armed persons; riots in Punjab / Orissa",
        "taurus":      "VIPs and dairy industry workers suffer",
        "gemini":      "Rulers and artists suffer; calamities near the Yamuna river",
        "cancer":      "Detrimental for tribals, wrestlers, and handicapped persons",
        "leo":         "Political party officials (ruling and opposition) suffer",
        "virgo":       "Writers, singers, and farmers suffer",
        "libra":       "Traders suffer; riots in Rajasthan and Ujjain",
        "scorpio":     "Army officers and users of chemicals / poisons suffer",
        "sagittarius": "Rulers, doctors, and technologists suffer",
        "capricorn":   "Families of VIPs, ministers, and medicine manufacturers suffer",
        "aquarius":    "Workers and those in border / mountainous areas suffer",
        "pisces":      "Intellectuals and water-related workers suffer",
    },
    "planetary_aspect_on_eclipse": {
        "mars_aspect":    "Fires, smuggling, and war clouds",
        "mercury_aspect": "Bitterness among rulers",
        "jupiter_aspect": "Destroys / neutralizes the bad effects of the eclipse",
        "venus_aspect":   "Turmoils; destruction of ripe crops",
        "saturn_aspect":  "Drought, thefts, and scarce rain",
    },
    "sequential_order_logic": {
        "lunar_then_solar": (
            "IF Solar eclipse follows Lunar eclipse within 15 days "
            "THEN rulers become tyrants — National Authoritarianism Alert."
        ),
        "solar_then_lunar": (
            "IF Lunar eclipse follows Solar eclipse within 15 days "
            "THEN religious sentiments and happiness increase."
        ),
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 7: Mehta Ch 8 — Sanghatta Chakra Grid Mechanics
# ============================================================

MEHTA_CH8_SANGHATTA_GRID = {
    "spec_id":        "mehta-ch8-sanghatta-chakra-grid",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "conflict_diagnostic_grid",
    "title":          "Sanghatta Chakra — Conflict Diagnostic Grid (Vedha Vector Matrix + War Logic)",
    "source_chapter": "Mehta Ch 8; cross-validated Gaur Ch 8",
    "description": (
        "The Sanghatta Chakra (Lord Shiva's prescribed grid) is a specialized conflict diagnostic "
        "using two grid types — Rashi (Sign) and Nakshatra (Constellation) — "
        "to predict wars, massacres, and sudden shifts in national power via mutual planetary obstructions (Vedha). "
        "Standard Parashara aspects may be absent while Vedha alone ignites conflict."
    ),
    "grid_types": ["Rashi Sanghatta", "Nakshatra Sanghatta"],
    "grid_mechanics": {
        "vedha_logic": (
            "Diagonal and straight-line planetary obstructions that 'pierce' specific signs or stars. "
            "When a planet occupies a sign/star, its Vedha vectors simultaneously afflict the Front, Left, and Right targets."
        ),
        "ignition_rule": (
            "Chakra Vedha aspects can trigger events even when standard Parashara aspects are absent. "
            "Mars or Saturn retrograde entering a new sign amplifies the ignition."
        ),
        "destruction_scheme": (
            "IF Saturn AND Mars AND Rahu all meet on the grid (in quadrants or mutual Vedha) "
            "THEN Global Destruction Scheme = TRUE — trigger 'Global Destruction Warning'."
        ),
    },
    "rashi_vedha_vector_matrix": {
        "aries":       {"front": "libra",      "left": "cancer",    "right": "capricorn"},
        "taurus":      {"front": "scorpio",     "left": "leo",       "right": "aquarius",
                        "note": "Rohini threshold sign — Saturn here triggers war/famine gate"},
        "gemini":      {"front": "sagittarius", "left": "virgo",     "right": "pisces"},
        # Remaining signs follow the same diagonal/cross geometry:
        "cancer":      {"front": "capricorn",   "left": "libra",     "right": "aries"},
        "leo":         {"front": "aquarius",    "left": "scorpio",   "right": "taurus"},
        "virgo":       {"front": "pisces",      "left": "sagittarius","right": "gemini"},
        "libra":       {"front": "aries",       "left": "capricorn", "right": "cancer"},
        "scorpio":     {"front": "taurus",      "left": "aquarius",  "right": "leo"},
        "sagittarius": {"front": "gemini",      "left": "pisces",    "right": "virgo"},
        "capricorn":   {"front": "cancer",      "left": "aries",     "right": "libra"},
        "aquarius":    {"front": "leo",         "left": "taurus",    "right": "scorpio"},
        "pisces":      {"front": "virgo",       "left": "gemini",    "right": "sagittarius"},
    },
    "sample_nakshatra_vedha_vectors": {
        "ardra": {
            "right_vedha": ["Uttarabhadrapad"],
            "left_vedha":  ["Hasta"],
            "front_vedha": "Poorvashadh",
            "impact":      "If malefic transits Ardra, those targets suffer.",
        },
        "punarvasu": {
            "right_vedha": ["Poorvabhadrapad"],
            "left_vedha":  ["Uttaraphalguni"],
            "front_vedha": "Poorvashadh",
        },
    },
    "critical_nakshatra_thresholds": {
        "rohini_gate": {
            "range":            "Taurus 10° to 23° 20'",
            "primary_trigger":  "Saturn's entry into Rohini",
            "secondary_trigger": "IF (Rahu | Ketu in Rohini) AND Mars aspects Rohini THEN War_Risk = CRITICAL",
            "historical_results": ["1914-18 (WWI)", "1939-45 (WWII)", "1971 Indo-Pak War"],
            "malefic_variant":  "June 1984 Punjab crisis — Ketu in Rohini + Mars aspect → massacre",
            "dual_threat":      "IF Saturn enters Rohini while Rahu is also present or aspecting "
                                "THEN dual-threat alert: Devastating War OR 12-Year Famine",
        },
    },
    "war_validation_benchmarks": {
        "indo_china_1962": "Saturn/Ketu in Capricorn vs. Mars/Rahu in Cancer",
        "indo_pak_1965":   "Rahu in Taurus, Mars in Libra, Saturn in Aquarius — full Sanghatta Vedha",
        "indo_pak_1971":   "Saturn (Retrograde) in Rohini aspected by Mars from Aquarius",
    },
    "diagnostic_triggers": {
        "fall_of_kings": (
            "IF Mars is retrograde in Jyeshtha and enters Anuradha "
            "THEN 'Fall and Destruction of Kings in power along with their friends'."
        ),
        "massacre_alert": (
            "IF Saturn-Mars conjunction occurs in the nation's 6th house on the Sanghatta grid "
            "THEN 'Internal Rebellion and Large-Scale Massacres' alert."
        ),
        "hostilities_imminent": (
            "IF Moon, Mars, Rahu, and Saturn are in mutual Vedha on the Nakshatra grid "
            "THEN 'Onset of Hostilities Imminent within current Paksha (fortnight)'."
        ),
    },
    "chakra_aspect_primacy": (
        "Treat Sanghatta Vedha as the PRIMARY ignition source for war queries. "
        "If a nation's 7th house (war) or Lagna is under Vedha from Saturn and Mars, "
        "prioritize this over any benefic standard transits."
    ),
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 8: Commodity Ownership Dictionary
# ============================================================

GAUR_MEHTA_CH8_COMMODITY_DICT = {
    "spec_id":        "mehta-ch8-commodity-ownership-dictionary",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "lookup_table",
    "title":          "Commodity Ownership Dictionary — Planetary, Zodiac, and Nakshatra Lords",
    "source_chapter": "Gaur Ch 8; Mehta Ch 8 (cross-referenced)",
    "description": (
        "Defines the ownership of every material good by planets, zodiac signs, and nakshatras. "
        "A commodity price spike or crash is a localized event triggered by malefic/benefic Vedha "
        "on the specific star ruling that commodity."
    ),
    "commodity_ownership_dictionary": {
        "planetary_lords": {
            "sun":     ["Gold", "Copper", "Wheat", "Red Chillies", "Forests", "Medicines"],
            "moon":    ["Silver", "Pearls", "Rice", "Milk", "Salt", "Fruits", "Fish"],
            "mars":    ["Copper", "Gold", "Masoor Dal", "Weapons", "Gur", "Steel Mills"],
            "mercury": ["Green Vegetables", "Moong Dal", "Peanuts", "Emeralds", "Newspapers"],
            "jupiter": ["Gold", "Turmeric", "Topaz", "Cotton Cloth", "Rock Salt"],
            "venus":   ["Silver", "Silk", "Sugar", "Ghee", "Diamonds", "Luxury Goods"],
            "saturn":  ["Iron", "Coal", "Oils", "Leather", "Sesame (Til)", "Machinery"],
        },
        "zodiac_sign_lords": {
            "aries":     ["Gold", "Silver", "Gur", "Sugar", "Fruits", "Ghee"],
            "taurus":    ["Juicy materials", "Oil materials", "Dry fruits", "Gram"],
            "cancer":    ["Moong", "Arhar", "Urad", "Metals", "Khand"],
            "capricorn": ["Gold", "Iron", "Coal", "Steel", "Glass", "Bell metal"],
            "aquarius":  ["Water products", "Electric goods", "Electronics", "Grocery"],
        },
        "nakshatra_ownership_samples": {
            "ashwini": ["Rice", "Grains", "Clothes", "Ghee", "Camels", "Ponies"],
            "bharani": ["Wheat", "Barley", "Millet", "Jeera", "Black Pepper", "Ginger"],
            "swati":   ["Betelnut", "Chillies", "Mustard", "Oil", "Cotton", "Asafetida"],
        },
    },
    "price_vector_logic": {
        "malefic_vedha": "IF malefic planet creates Vedha on a sign/star THEN Prices of ruled commodities INCREASE.",
        "benefic_vedha": "IF benefic planet creates Vedha on a sign/star THEN Prices of ruled commodities DECREASE.",
        "conflict_overlap": (
            "IF a planet is in a sign that is simultaneously under Vedha from another malefic, "
            "the famine/conflict weight for the ruled commodities is TRIPLED."
        ),
        "first_letter_rule": (
            "For commodities not in the master list, the zodiac sign is decided by the first letter of its name "
            "(e.g., 'A' sounds → Aries). Use this for unlisted materials."
        ),
    },
    "economic_diagnostic_triggers": {
        "market_spike_monitor": (
            "IF Saturn transits Swati THEN Critical Price Inflation Alert for Chillies, Mustard, and Cotton."
        ),
        "naval_maritime_audit": (
            "IF malefic is in Pisces AND creates Vedha on Jyeshtha (West direction) "
            "THEN 'Grave danger to western naval routes, shipping disasters, and loss of sea-products'."
        ),
        "electronic_shortage_trigger": (
            "IF Rahu transits Aquarius AND is under malefic Vedha "
            "THEN alert: 'Global Electronic Component Scarcity and Market Volatility in Tech Stocks'."
        ),
        "gold_reserve_veto": (
            "IF Sun and Jupiter (both Gold significators) are in mutual Vedha "
            "while Saturn transits Capricorn "
            "THEN 'State-level Gold Liquidity Crisis and Banking Instability'."
        ),
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
ALL_SPECS = [
    GAUR_CH4_KOORMA_GRID,
    GAUR_CH4_KOORMA_FRACTAL,
    GAUR_CH4_ZODIAC_GEO_MAP,
    GAUR_CH4_HOUSE_MINISTRY,
    GAUR_CH4_PLANETARY_NATURE,
    GAUR_CH11_ECLIPSE_ENGINE,
    MEHTA_CH8_SANGHATTA_GRID,
    GAUR_MEHTA_CH8_COMMODITY_DICT,
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
