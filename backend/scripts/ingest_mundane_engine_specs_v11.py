"""
Mundane Astrology — Engine Specs v11
Batch: mundane-engine-v11-20260506

Source: Dr. Jagdamba Prasad Gaur, "Mundane Astrology" (AIFAS, 2nd ed. 2010)
  Chapter 1 — Samvatsar (pp. 3-7, Part 1: Samvatsar Vichar)
    § 1. Names of Samvatsars and Their Lords (complete 60-year table)
    § 2. The Method of Knowing Samvatsar (two calculation methods)
    § 3. Results of Samvatsars and Their Lords (lords 1-12 of 12)
      NOTE: Samvatsar #1-12 cover all 12 possible planetary lords.
            Samvatsars 13-60 cycle back through the same 12 lords.
            Pages 1-20 contain complete lord-result data.

GROUP_1: 3 engine specs — Gaur Ch 1 Samvatsar lookup tables

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
_BATCH     = "mundane-engine-v11-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ============================================================
# SPEC 1 — Complete 60-Samvatsar lookup table
# ============================================================
GAUR_CH1_60_SAMVATSARS = {
    "spec_id":       "gaur-ch1-60-samvatsars-lookup",
    "spec_type":     "lookup_table",
    "science_id":    "mundane_jyotish",
    "batch_id":      _BATCH,
    "title":         "The 60 Samvatsars — Names, Lords, and Group (Gaur Ch 1)",
    "source_chapter": "Gaur Ch 1, p. 3",
    "notes": (
        "A Samvatsar is the period of Jupiter's transit through one zodiac sign (~1 year). "
        "There are 60 Samvatsars in total, cycling in order. "
        "Each Samvatsar has a unique name and one of 12 planetary lords "
        "(Brahma, Vishnu, Shiv, Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu). "
        "GROUP OWNERSHIP: "
        "  First 20 (Prabhav to Vyaya) belong to Brahma-group. "
        "  Middle 20 (Sarvjat to Parabhav) belong to Vishnu-group. "
        "  Last 20 (Plavang to Kshaya) belong to Shiv-group. "
        "The lord of the Samvatsar modifies events throughout that year."
    ),
    "samvatsars": [
        # first 20 — Brahma group
        {"number": 1,  "name": "Prabhav",      "lord": "Brahma",   "group": "Brahma"},
        {"number": 2,  "name": "Vibhav",        "lord": "Vishnu",   "group": "Brahma"},
        {"number": 3,  "name": "Shukla",        "lord": "Shiv",     "group": "Brahma"},
        {"number": 4,  "name": "Pramod",        "lord": "Sun",      "group": "Brahma"},
        {"number": 5,  "name": "Prajapati",     "lord": "Moon",     "group": "Brahma"},
        {"number": 6,  "name": "Angira",        "lord": "Mars",     "group": "Brahma"},
        {"number": 7,  "name": "Shree Mukh",    "lord": "Mercury",  "group": "Brahma"},
        {"number": 8,  "name": "Bhav",          "lord": "Jupiter",  "group": "Brahma"},
        {"number": 9,  "name": "Yuva",          "lord": "Venus",    "group": "Brahma"},
        {"number": 10, "name": "Dhata",         "lord": "Saturn",   "group": "Brahma"},
        {"number": 11, "name": "Eashwar",       "lord": "Rahu",     "group": "Brahma"},
        {"number": 12, "name": "Bahudhanya",    "lord": "Ketu",     "group": "Brahma"},
        {"number": 13, "name": "Pramathi",      "lord": "Sun",      "group": "Brahma"},
        {"number": 14, "name": "Vikram",        "lord": "Moon",     "group": "Brahma"},
        {"number": 15, "name": "Vrish",         "lord": "Mars",     "group": "Brahma"},
        {"number": 16, "name": "Chitrabhanu",   "lord": "Mercury",  "group": "Brahma"},
        {"number": 17, "name": "Subhanu",       "lord": "Jupiter",  "group": "Brahma"},
        {"number": 18, "name": "Taran",         "lord": "Venus",    "group": "Brahma"},
        {"number": 19, "name": "Parthiv",       "lord": "Saturn",   "group": "Brahma"},
        {"number": 20, "name": "Vyaya",         "lord": "Rahu",     "group": "Brahma"},
        # middle 20 — Vishnu group
        {"number": 21, "name": "Sarvjat",       "lord": "Brahma",   "group": "Vishnu"},
        {"number": 22, "name": "Sarvdhari",     "lord": "Vishnu",   "group": "Vishnu"},
        {"number": 23, "name": "Virodhi",       "lord": "Shiv",     "group": "Vishnu"},
        {"number": 24, "name": "Vikriti",       "lord": "Sun",      "group": "Vishnu"},
        {"number": 25, "name": "Khar",          "lord": "Moon",     "group": "Vishnu"},
        {"number": 26, "name": "Nandan",        "lord": "Mars",     "group": "Vishnu"},
        {"number": 27, "name": "Vijai",         "lord": "Mercury",  "group": "Vishnu"},
        {"number": 28, "name": "Jai",           "lord": "Jupiter",  "group": "Vishnu"},
        {"number": 29, "name": "Manmath",       "lord": "Venus",    "group": "Vishnu"},
        {"number": 30, "name": "Durmukh",       "lord": "Saturn",   "group": "Vishnu"},
        {"number": 31, "name": "Hamelambi",     "lord": "Rahu",     "group": "Vishnu"},
        {"number": 32, "name": "Vilambi",       "lord": "Ketu",     "group": "Vishnu"},
        {"number": 33, "name": "Vikari",        "lord": "Moon",     "group": "Vishnu"},
        {"number": 34, "name": "Sharbari",      "lord": "Mars",     "group": "Vishnu"},
        {"number": 35, "name": "Plav",          "lord": "Mercury",  "group": "Vishnu"},
        {"number": 36, "name": "Shubhkrit",     "lord": "Jupiter",  "group": "Vishnu"},
        {"number": 37, "name": "Shobhan",       "lord": "Venus",    "group": "Vishnu"},
        {"number": 38, "name": "Krodhi",        "lord": "Saturn",   "group": "Vishnu"},
        {"number": 39, "name": "Vishvavasu",    "lord": "Rahu",     "group": "Vishnu"},
        {"number": 40, "name": "Parabhav",      "lord": "Ketu",     "group": "Vishnu"},
        # last 20 — Shiv group
        {"number": 41, "name": "Plavang",       "lord": "Brahma",   "group": "Shiv"},
        {"number": 42, "name": "Keelak",        "lord": "Vishnu",   "group": "Shiv"},
        {"number": 43, "name": "Saumya",        "lord": "Shiv",     "group": "Shiv"},
        {"number": 44, "name": "Sadharan",      "lord": "Sun",      "group": "Shiv"},
        {"number": 45, "name": "Virodhkrit",    "lord": "Moon",     "group": "Shiv"},
        {"number": 46, "name": "Paridhavi",     "lord": "Mars",     "group": "Shiv"},
        {"number": 47, "name": "Pramadi",       "lord": "Mercury",  "group": "Shiv"},
        {"number": 48, "name": "Anand",         "lord": "Jupiter",  "group": "Shiv"},
        {"number": 49, "name": "Rakshas",       "lord": "Venus",    "group": "Shiv"},
        {"number": 50, "name": "Nal",           "lord": "Saturn",   "group": "Shiv"},
        {"number": 51, "name": "Pingal",        "lord": "Rahu",     "group": "Shiv"},
        {"number": 52, "name": "Kaal Yukta",    "lord": "Ketu",     "group": "Shiv"},
        {"number": 53, "name": "Siddharthi",    "lord": "Sun",      "group": "Shiv"},
        {"number": 54, "name": "Raudra",        "lord": "Moon",     "group": "Shiv"},
        {"number": 55, "name": "Durmati",       "lord": "Mars",     "group": "Shiv"},
        {"number": 56, "name": "Dundubhi",      "lord": "Mercury",  "group": "Shiv"},
        {"number": 57, "name": "Rudhirodgari",  "lord": "Jupiter",  "group": "Shiv"},
        {"number": 58, "name": "Raktaksha",     "lord": "Venus",    "group": "Shiv"},
        {"number": 59, "name": "Krodhan",       "lord": "Saturn",   "group": "Shiv"},
        {"number": 60, "name": "Kshaya",        "lord": "Rahu",     "group": "Shiv"},
    ],
    "created_at": _NOW,
}

# ============================================================
# SPEC 2 — Samvatsar calculation method
# ============================================================
GAUR_CH1_SAMVATSAR_CALCULATION = {
    "spec_id":       "gaur-ch1-samvatsar-calculation-method",
    "spec_type":     "calculation_method",
    "science_id":    "mundane_jyotish",
    "batch_id":      _BATCH,
    "title":         "Method to Calculate Current Samvatsar from Vikrami Samvat (Gaur Ch 1)",
    "source_chapter": "Gaur Ch 1, p. 4",
    "notes": (
        "Two methods are given — a precise tabular method and a simple shortcut. "
        "Both use the Vikrami Samvat (Hindu solar year), not the Gregorian year. "
        "Vikrami Samvat = Gregorian year + 57 (approx, valid for Jan-Mar) "
        "or Gregorian year + 56 (valid for Apr-Dec)."
    ),
    "method_1_tabular": {
        "description": (
            "Precise calculation using Quotient and Remainder tables. "
            "Step 1: Note the Vikrami Samvat. "
            "Step 2: Subtract 1927. "
            "Step 3: Divide the remainder by 10. "
            "Step 4: Note the quotient and the remainder. "
            "Step 5: From the Quotient Table, read Years/Months/Day/Ghari/Pal for that quotient. "
            "Step 6: From the Remainder Table, read Years/Months/Day/Ghari/Pal for that remainder. "
            "Step 7: Add the two rows — the first number = samvatsar ordinal (1-60), rest = elapsed time within it."
        ),
        "quotient_table": {
            "1":  {"year": 10, "month": 1,  "day": 12, "ghari": 14, "pal": 24},
            "2":  {"year": 20, "month": 2,  "day": 24, "ghari": 28, "pal": 48},
            "3":  {"year": 30, "month": 4,  "day": 6,  "ghari": 43, "pal": 12},
            "4":  {"year": 40, "month": 5,  "day": 18, "ghari": 57, "pal": 36},
            "5":  {"year": 50, "month": 7,  "day": 1,  "ghari": 12, "pal": 0},
            "6":  {"year": 0,  "month": 8,  "day": 13, "ghari": 26, "pal": 24},
            "7":  {"year": 10, "month": 9,  "day": 25, "ghari": 40, "pal": 48},
            "8":  {"year": 20, "month": 11, "day": 7,  "ghari": 55, "pal": 12},
            "9":  {"year": 31, "month": 0,  "day": 20, "ghari": 9,  "pal": 36},
            "10": {"year": 41, "month": 2,  "day": 2,  "ghari": 24, "pal": 00},
            "11": {"year": 51, "month": 3,  "day": 14, "ghari": 38, "pal": 24},
            "12": {"year": 1,  "month": 4,  "day": 26, "ghari": 52, "pal": 48},
            "13": {"year": 11, "month": 6,  "day": 9,  "ghari": 7,  "pal": 12},
            "14": {"year": 21, "month": 7,  "day": 21, "ghari": 21, "pal": 36},
        },
        "remainder_table": {
            "0": {"year": 15, "month": 3,  "day": 23, "ghari": 16, "pal": 48},
            "1": {"year": 16, "month": 3,  "day": 27, "ghari": 30, "pal": 14},
            "2": {"year": 17, "month": 4,  "day": 1,  "ghari": 43, "pal": 40},
            "3": {"year": 18, "month": 4,  "day": 5,  "ghari": 57, "pal": 7},
            "4": {"year": 19, "month": 4,  "day": 10, "ghari": 10, "pal": 33},
            "5": {"year": 20, "month": 4,  "day": 14, "ghari": 24, "pal": 0},
            "6": {"year": 21, "month": 4,  "day": 18, "ghari": 37, "pal": 26},
            "7": {"year": 22, "month": 4,  "day": 22, "ghari": 50, "pal": 52},
            "8": {"year": 23, "month": 4,  "day": 27, "ghari": 4,  "pal": 19},
            "9": {"year": 24, "month": 5,  "day": 1,  "ghari": 17, "pal": 45},
        },
        "example": (
            "Vikrami Samvat 2059: 2059 - 1927 = 132. "
            "132 / 10 = quotient 13, remainder 2. "
            "Quotient 13 row: 11-6-9-7-12. Remainder 2 row: 17-4-1-43-40. "
            "Sum: 28-10-10-50-52. "
            "28th samvatsar = Manmath (lord: Venus). "
            "10 months, 10 days, 50 ghari, 52 pal have elapsed."
        ),
    },
    "method_2_simple": {
        "description": (
            "Add 9 to the Vikrami Samvat. Divide by 60. "
            "The remainder gives the current samvatsar number (1-60). "
            "A remainder of 0 means the 60th samvatsar (Kshaya)."
        ),
        "example": (
            "Vikrami Samvat 2059: 2059 + 9 = 2068. 2068 / 60 = 34 remainder 28. "
            "28th samvatsar = Manmath (lord: Venus)."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
# SPEC 3 — Samvatsar Lord Monthly Effects (all 12 lords)
# ============================================================
GAUR_CH1_SAMVATSAR_LORD_EFFECTS = {
    "spec_id":       "gaur-ch1-samvatsar-lord-monthly-effects",
    "spec_type":     "lookup_table",
    "science_id":    "mundane_jyotish",
    "batch_id":      _BATCH,
    "title":         "Samvatsar Lord Monthly Effects — All 12 Lords (Gaur Ch 1)",
    "source_chapter": "Gaur Ch 1, pp. 5-7",
    "notes": (
        "The lord of the current Samvatsar determines seasonal and monthly effects for the year. "
        "Each of the 12 lords cycles through 5 Samvatsars over the 60-year cycle. "
        "The month names are Hindu (Vedic) lunar months: "
        "Chaitra (Mar-Apr), Baisakh (Apr-May), Jyeshtha (May-Jun), Aashadh (Jun-Jul), "
        "Shravan (Jul-Aug), Bhadrapad (Aug-Sep), Ashwin (Sep-Oct), Kartik (Oct-Nov), "
        "Margsheersh (Nov-Dec), Paush (Dec-Jan), Maagh (Jan-Feb), Phalgun (Feb-Mar). "
        "Effects cover: grain prices, rainfall intensity, disease prevalence, political climate."
    ),
    "lord_effects": {
        "Brahma": {
            "samvatsars": [1, 21, 41],
            "general": (
                "Rulers, cabinet ministers, senior officers remain pleased. "
                "Increase in people's luxuries and comforts. "
                "Crop is good due to absence of disease or loss in plants."
            ),
            "monthly": {
                "Chaitra":     "Lucky, things cheap.",
                "Baisakh":     "Lucky, things cheap.",
                "Jyeshtha":    "Grains costly.",
                "Aashadh":     "Grains costly.",
                "Shravan":     "Grains costly.",
                "Bhadrapad":   "Lucky.",
                "Ashwin":      "Grains dearer, diseases cause agony.",
                "Kartik":      "Normal.",
                "Margsheersh": "Normal.",
                "Paush":       "Normal.",
                "Maagh":       "Normal.",
                "Phalgun":     "Normal.",
            },
        },
        "Vishnu": {
            "samvatsars": [2, 22, 42],
            "general": (
                "Rulers and senior officers take stern measures to maintain law and order. "
                "Common people forget differences and live with peace and happiness. "
                "Rains and crops are good. Many diseases prevalent."
            ),
            "monthly": {
                "Chaitra":     "Juicy materials costly.",
                "Baisakh":     "Juicy materials costly.",
                "Jyeshtha":    "Juicy materials costly.",
                "Aashadh":     "Rains plentiful.",
                "Shravan":     "Rains plentiful.",
                "Bhadrapad":   "Rains plentiful.",
                "Ashwin":      "Juices costly but cheap later.",
                "Kartik":      "Grains cheap.",
                "Margsheersh": "Grains cheap.",
                "Paush":       "Grains cheap.",
                "Maagh":       "Grains cheap.",
                "Phalgun":     "Grains cheap.",
            },
            "notes": "Hilly areas experience more difficulties and agonies.",
        },
        "Shiv": {
            "samvatsars": [3, 23, 43],
            "general": (
                "People live with relatives happily. "
                "Friction between rulers and opposition parties. "
                "Rulers of many places lose their throne; president's rule may be imposed."
            ),
            "monthly": {
                "Chaitra":     "Normal.",
                "Baisakh":     "Normal.",
                "Jyeshtha":    "Normal.",
                "Aashadh":     "Heavy rains.",
                "Shravan":     "Heavy rains.",
                "Bhadrapad":   "Heavy rains.",
                "Ashwin":      "Spread of diseases, all things dearer but Ghee is cheap.",
                "Kartik":      "Costly initially then cheap.",
                "Margsheersh": "Costly initially then cheap.",
                "Paush":       "Costly initially then cheap.",
                "Maagh":       "Costly initially then cheap.",
                "Phalgun":     "Full of difficulties and agony.",
            },
        },
        "Sun": {
            "samvatsars": [4, 24, 44],
            "general": (
                "Rulers and people remain pleased but masses are free of disease, turmoils. "
                "Rains are less. Insurgencies in the country encourage violence. "
                "Persons of lower class remain in anxiety. Throne changed at few places. "
                "Conflict between rulers and businessmen."
            ),
            "monthly": {
                "Chaitra":     "Goods become costlier.",
                "Baisakh":     "Goods become costlier.",
                "Jyeshtha":    "Diseases cause agony.",
                "Aashadh":     "Rains scanty.",
                "Shravan":     "Rains scanty.",
                "Bhadrapad":   "Rains scanty.",
                "Ashwin":      "Rain harms crops.",
                "Kartik":      "Juicy materials dearer.",
                "Margsheersh": "Juicy materials dearer.",
                "Paush":       "Juicy materials dearer.",
                "Maagh":       "Juicy materials dearer.",
                "Phalgun":     "Medium.",
            },
        },
        "Moon": {
            "samvatsars": [5, 25, 45],
            "general": (
                "All people leave their path. Rains are plentiful, grains are cheap. "
                "All 12 months are excellent. Rains could be deficient at few places."
            ),
            "monthly": {
                "Chaitra":     "Excellent.",
                "Baisakh":     "Excellent.",
                "Jyeshtha":    "Excellent.",
                "Aashadh":     "Excellent.",
                "Shravan":     "Excellent.",
                "Bhadrapad":   "Excellent.",
                "Ashwin":      "Diseases more, grains costlier.",
                "Kartik":      "Things cheap.",
                "Margsheersh": "Things cheap.",
                "Paush":       "Natural calamities cause losses.",
                "Maagh":       "Natural calamities cause losses.",
                "Phalgun":     "Natural calamities cause losses.",
            },
        },
        "Mars": {
            "samvatsars": [6, 26, 46],
            "general": (
                "Grains are plentiful. Rulers remain engaged in conflicts. "
                "The peace of world is breached by wars."
            ),
            "monthly": {
                "Chaitra":     "Grains cheap.",
                "Baisakh":     "Grains cheap.",
                "Jyeshtha":    "Storms.",
                "Aashadh":     "Heavy rains, floods.",
                "Shravan":     "Disease widespread.",
                "Bhadrapad":   "Disease widespread.",
                "Ashwin":      "Disease widespread.",
                "Kartik":      "Grains costly.",
                "Margsheersh": "Normal.",
                "Paush":       "Normal.",
                "Maagh":       "Normal.",
                "Phalgun":     "Normal.",
            },
        },
        "Mercury": {
            "samvatsars": [7, 27, 47],
            "general": (
                "Produce of grains is good, rains are satisfactory. "
                "Farmers get good returns for their crops. "
                "People have less conflicts and more harmony. "
                "Brahmins remain busy in religious practices; people inclined towards noble deeds. "
                "Diseases are removed."
            ),
            "monthly": {},
            "notes": (
                "No specific monthly breakdown given for Mercury years — "
                "general benefic quality applies throughout."
            ),
        },
        "Jupiter": {
            "samvatsars": [8, 28, 48],
            "general": (
                "Diseases are excessive. Grain production is medium. "
                "Though rulers engage in wars the people have a feeling of security. "
                "Rains are excessive; cattles give more milk. All things are dear."
            ),
            "monthly": {
                "Chaitra":     "Medium.",
                "Baisakh":     "Food materials costly.",
                "Jyeshtha":    "Normal (implied from context).",
                "Aashadh":     "Rains normal.",
                "Shravan":     "Rains normal.",
                "Bhadrapad":   "Rains excessive.",
                "Ashwin":      "Excessive disease.",
                "Kartik":      "Beneficial.",
                "Margsheersh": "Grains cheap.",
                "Paush":       "Grains cheap.",
                "Maagh":       "Grains cheap.",
                "Phalgun":     "Grains cheap.",
            },
        },
        "Venus": {
            "samvatsars": [9, 29, 49],
            "general": (
                "Milk production is good. Rains are excessive. "
                "Ladies remain engaged in activities of all types. Young people want luxuries. "
                "All people live comfortably. Supremacy of females is established. "
                "Earthquakes and other natural calamities cause agony."
            ),
            "monthly": {
                "Chaitra":     "Natural calamities.",
                "Baisakh":     "Natural calamities.",
                "Jyeshtha":    "Disease.",
                "Aashadh":     "Rains.",
                "Shravan":     "Winds. Grains become costly.",
                "Bhadrapad":   "Floods cause loss.",
                "Ashwin":      "Beneficial.",
                "Margsheersh": "Beneficial.",
                "Paush":       "Medium.",
                "Maagh":       "Medium.",
                "Phalgun":     "Trouble.",
            },
        },
        "Saturn": {
            "samvatsars": [10, 30, 50],
            "general": (
                "Rulers create atmosphere for war due to their diplomatic actions. "
                "People remain fearful. Crops are good. Widespread rains also cause losses."
            ),
            "monthly": {
                "Chaitra":     "Grains costlier.",
                "Baisakh":     "Grains costlier.",
                "Jyeshtha":    "Normal.",
                "Aashadh":     "Rains less; oils and ghee costlier.",
                "Shravan":     "Normal (implied).",
                "Bhadrapad":   "Normal (implied).",
                "Ashwin":      "Juicy materials and metals costly.",
                "Kartik":      "Grains cheap.",
                "Margsheersh": "Normal (implied).",
                "Paush":       "Normal (implied).",
                "Maagh":       "Normal (implied).",
                "Phalgun":     "Normal (implied).",
            },
        },
        "Rahu": {
            "samvatsars": [11, 31, 51],
            "general": (
                "All people live happily. Crops of fruits and grains are good. "
                "GEOGRAPHICAL EFFECTS: Drought in North, floods in East, war in West."
            ),
            "monthly": {
                "Chaitra":     "Things costly.",
                "Baisakh":     "Things costly.",
                "Jyeshtha":    "Rains less.",
                "Aashadh":     "Rains less.",
                "Shravan":     "Rains more.",
                "Bhadrapad":   "Rains more.",
                "Ashwin":      "Normal (implied).",
                "Kartik":      "Drought; essential goods costly.",
                "Margsheersh": "Goods costly; lives lost to riots.",
                "Paush":       "Goods costly; lives lost to riots.",
                "Maagh":       "Goods costly; lives lost to riots.",
                "Phalgun":     "Goods costly; lives lost to riots.",
            },
        },
        "Ketu": {
            "samvatsars": [12, 32, 52],
            "general": (
                "Plentiful rains. Grains available abundantly. "
                "People have increased tendency of loose character and conduct."
            ),
            "monthly": {
                "Chaitra":     "Grains expensive.",
                "Baisakh":     "Grains expensive.",
                "Jyeshtha":    "Grains expensive.",
                "Aashadh":     "Sufficient rains; grains become cheap.",
                "Shravan":     "Sufficient rains; grains become cheap.",
                "Bhadrapad":   "Sufficient rains; grains become cheap.",
                "Ashwin":      "Normal (implied).",
                "Kartik":      "Normal (implied).",
                "Margsheersh": "Normal (implied).",
                "Paush":       "Normal (implied).",
                "Maagh":       "Normal (implied).",
                "Phalgun":     "Normal (implied).",
            },
        },
    },
    "usage_note": (
        "To use: (1) Determine current Samvatsar number using spec gaur-ch1-samvatsar-calculation-method. "
        "(2) Look up the lord of that Samvatsar in spec gaur-ch1-60-samvatsars-lookup. "
        "(3) Apply the lord_effects for that lord to get annual and monthly predictions. "
        "(4) The group (Brahma/Vishnu/Shiv) provides a secondary modifier for overall year quality."
    ),
    "created_at": _NOW,
}

# ============================================================
ALL_SPECS = [
    GAUR_CH1_60_SAMVATSARS,
    GAUR_CH1_SAMVATSAR_CALCULATION,
    GAUR_CH1_SAMVATSAR_LORD_EFFECTS,
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
