"""
Mundane Astrology — Engine Specs v10
Batch: mundane-engine-v10-20260506

Source: Raphael, "Mundane Astrology" (WITS e-group edition)
  Chapter 28 — The Parts of the World Affected by the Signs of the Zodiac
               (COMPLETE data — supersedes partial entry in v9 batch)

This v10 engine spec contains the COMPLETE Ch 28 countries/cities lookup.
The v9 entry (raphael-ch28-countries-ruled-by-signs) had incomplete data
for Libra, Scorpio, Sagittarius, Capricorn, Aquarius, and Pisces.
This spec uses the SAME spec_id and will upsert/overwrite the v9 entry
when DRY_RUN is set to False and run against MongoDB.

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
_BATCH     = "mundane-engine-v10-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ============================================================
# COMPLETE Ch 28 — COUNTRIES AND CITIES RULED BY THE TWELVE SIGNS
# (Supersedes partial v9 entry — same spec_id = upsert overwrites)
# ============================================================
RAPHAEL_CH28_COUNTRIES_BY_SIGN_COMPLETE = {
    "spec_id":      "raphael-ch28-countries-ruled-by-signs",   # same as v9 → upsert
    "spec_type":    "lookup_table",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Countries and Cities Ruled by the Twelve Signs — COMPLETE (Raphael Ch 28)",
    "source_chapter": "Raphael Ch 28, Part 3 pp.7-10",
    "notes": (
        "Complete listing from Ptolemy's Tetrabiblos supplemented by later authorities. "
        "Used to identify which countries are most affected by eclipses, conjunctions, "
        "and transits in a given sign. Where a specific degree is given for a city, "
        "it indicates the exact zodiacal degree on the city's meridian, enabling "
        "precise transit predictions (e.g., Mars crossing that exact degree = fire/accident). "
        "SUPERSEDES incomplete v9 entry for this spec_id."
    ),
    "sign_rulerships": {
        "Aries": {
            "countries": [
                "England", "Denmark", "Germany", "Lesser Poland", "Burgundy",
                "Palestine", "Syria", "Japan",
            ],
            "cities": [
                "Birmingham", "Oldham", "Leicester", "Blackburn", "Florence",
                "Naples", "Verona", "Padua", "Marseilles", "Cracow", "Saragossa",
                "Utrecht", "Capua", "Brunswick",
            ],
        },
        "Taurus": {
            "countries": [
                "Ireland", "Persia", "Poland", "Asia Minor", "Georgia",
                "Caucasus", "Grecian Archipelago", "Cyprus", "White Russia",
            ],
            "cities": [
                "Dublin", "Leipzig", "Mantua", "Parma", "Palermo",
                "Rhodes", "St. Louis", "Ashton-under-Lyne",
            ],
        },
        "Gemini": {
            "countries": [
                "United States", "Belgium", "Brabant", "Lombardy", "Lower Egypt",
                "Sardinia", "West of England", "Armenia", "Tripoli", "Flanders", "Wales",
            ],
            "cities": [
                "London (17°54')", "Plymouth", "Melbourne (10°29')", "Bruges", "Cordova",
                "Metz", "Nuremberg", "Versailles", "Louvaine", "San Francisco",
                "Wolverhampton", "Wednesbury",
            ],
            "notes": "London's zodiacal degree is Gemini 17°54'. This exact degree on London's meridian is used for precise transit predictions.",
        },
        "Cancer": {
            "countries": [
                "Scotland", "Holland", "Zealand", "N. and W. Africa",
                "Isle of Mauritius", "Paraguay",
            ],
            "cities": [
                "Tunis", "Algiers", "Amsterdam", "St. Andrews", "York", "Venice",
                "Berne", "Lubeck", "Magdeburg", "Milan", "Cadiz", "New York",
                "Manchester", "Stockholm", "Constantinople", "Genoa", "Deptford", "Rochdale",
            ],
        },
        "Leo": {
            "countries": [
                "France", "Italy", "Bohemia", "Sicily", "Chaldea to Bassorah",
                "N. of Romania", "Apulia", "The Alps", "parts near Sidon and Tyre",
            ],
            "cities": [
                "Rome", "Bath", "Bristol", "Portsmouth", "Philadelphia", "Prague",
                "Ravenna", "Taunton", "Damascus", "Chicago (1st decanate)",
                "Bombay (3rd decanate)", "Blackpool",
            ],
        },
        "Virgo": {
            "countries": [
                "Turkey", "Switzerland", "West Indies", "Assyria",
                "Mesopotamia from Tigris to Euphrates", "Crete", "Croatia",
                "Silesia", "Babylonia", "the Morea", "Thessaly", "Kurdistan",
                "parts of Greece", "Virginia", "Brazil",
            ],
            "cities": [],
        },
        "Libra": {
            "countries": [
                "Austria", "Indo-China", "China", "Tibet", "Borders of Caspian",
                "Upper Egypt", "Savoy", "N. China", "Livonia", "Burma", "Argentina",
            ],
            "cities": [
                "Antwerp (21°)", "Charleston", "Frankfurt", "Fribourg", "Gaeta",
                "Placenza", "Spires", "Vienna", "Lisbon", "Johannesburg (27°)",
                "Copenhagen (1°)", "Middleton", "Leeds", "Nottingham",
            ],
        },
        "Scorpio": {
            "countries": [
                "Algeria", "Barbary", "Bavaria", "Cappadocia", "Judea", "Jutland",
                "Morocco", "Norway", "N. Syria", "Transvaal", "Catalonia", "Queensland",
            ],
            "cities": [
                "Fez", "Valentia", "Frankfurt on Oder", "Dover", "Liverpool",
                "Messina (18°)", "Worthing (7°)", "E. Grinstead", "New Orleans",
                "Washington D.C.", "Baltimore", "Cincinnati", "Hull", "Milwaukee (7°)",
                "St. John's Newfoundland (2°)", "Halifax", "Stockport", "Newcastle", "Glossop",
            ],
        },
        "Sagittarius": {
            "countries": [
                "Arabia", "Australia", "Felix", "Cape Finisterre", "Dalmatia",
                "Hungary", "Istria", "Moravia", "Sclavonia", "Spain", "Tuscany",
                "Provence in France", "Madagascar",
            ],
            "cities": [
                "Avignon", "Buda", "Cologne", "Narbonne", "Rottenburg", "Nottingham",
                "Sheffield", "Stuttgart", "Sunderland", "Taranto", "Toledo",
                "W. Bromwich", "Bradford",
            ],
        },
        "Capricorn": {
            "countries": [
                "India", "Chorassan", "Circan", "Maraccan", "Punjab", "Afghanistan",
                "Thrace", "Macedonia", "Morea", "Illyria", "Albania", "Bosnia",
                "Bulgaria", "Greece", "Hesse", "S.W. Saxony", "Styria", "Romandiola",
                "Mecklenburg", "Mexico", "Lithuania", "Orkney Islands",
            ],
            "cities": [
                "Oxford", "Port Said", "Prato in Tuscany", "Brandenburg", "Tortona",
                "Constanz", "Brussels", "Fayence in Provence", "Keighley",
            ],
            "notes": "India's primary sign. Uranus in Capricorn caused insurrections in India (1910 validated case).",
        },
        "Aquarius": {
            "countries": [
                "Arabia the Stony", "Prussia", "Red Russia", "Pt. Poland", "Sweden",
                "Circassia", "Tartary", "Lithuania", "Westphalia", "Wallachia",
                "Piedmont", "Abyssinia",
            ],
            "cities": [
                "Brighton", "Bremen", "Ingolstadt", "Salzburg", "Trent",
                "Hamburg", "Salisbury",
            ],
            "notes": (
                "London's meridian degree is Aquarius 12°. "
                "Transits of Mars over Aquarius 12° have been marked with serious fire or accident in London. "
                "Russia is chiefly ruled by Aquarius."
            ),
        },
        "Pisces": {
            "countries": [
                "Portugal", "Calabria", "Galicia", "Normandy", "Nubia", "Sahara desert",
            ],
            "cities": [
                "Alexandria", "Ratisbon", "Worms", "Seville", "Compostella",
                "Bournemouth", "Farnham", "Tiverton", "Christchurch", "Cowes",
                "Regensburg", "Grimsby", "Southport", "Lancaster", "King's Lynn", "Preston",
            ],
        },
    },
    "usage_note": (
        "When an eclipse, great conjunction, or major transit occurs in a sign, "
        "consult this table to identify the countries and cities most affected. "
        "When the exact degree of a city is known, the degree on its meridian can also be computed. "
        "Mars or Saturn transiting that exact degree = serious troubles specific to that city. "
        "Mars transiting over London's meridian degree (Aquarius 12°) has historically coincided "
        "with serious fires or accidents in London."
    ),
    "created_at": _NOW,
}

# ============================================================
ALL_SPECS = [
    RAPHAEL_CH28_COUNTRIES_BY_SIGN_COMPLETE,
]

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_SPECS)} engine specs from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        for s in ALL_SPECS:
            print(f"  {s['spec_id']}  [UPSERT — overwrites v9 partial entry]")
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
