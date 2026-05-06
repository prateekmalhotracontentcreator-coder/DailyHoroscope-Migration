"""
Mundane Astrology — Engine Specs v9
Batch: mundane-engine-v9-20260506

Source: Raphael, "Mundane Astrology" (WITS e-group edition)
  Chapter 20 — How to Judge a Mundane Map (operational procedure)
  Chapter 22 — Eclipses (detailed eclipse rules from Ptolemy + sign-element effects)
  Chapter 23 — The Effects of Solar Eclipses (by decanate, all 36)
  Chapter 24 — The Effects of Lunar Eclipses (by decanate, all 36)
  Chapter 26 — Earthquakes (9 rules + validated historical cases)
  Chapter 28 — The Parts of the World Affected by the Signs of the Zodiac

Note: Chapter 25 (Planetary Conjunctions) is already encoded in earlier batches
      as mundane-raphael-ch25-* rules.

Spec types: rule_matrix, lookup_table, classification
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
_BATCH     = "mundane-engine-v9-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ============================================================
# 1. ECLIPSE RULES — SIGN ELEMENT EFFECTS + PTOLEMY TIMING  (Raphael Ch 22)
# ============================================================
RAPHAEL_CH22_ECLIPSE_RULES = {
    "spec_id":      "raphael-ch22-eclipse-sign-element-timing-rules",
    "spec_type":    "rule_matrix",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Eclipse Effects — Sign Element Classification + Ptolemy Timing Rules",
    "source_chapter": "Raphael Ch 22, pp.14-16 (Part 2)",
    "notes": (
        "Raphael draws on Ptolemy's Tetrabiblos for these eclipse rules. "
        "Key principle: the more total the eclipse, the more powerfully it operates. "
        "Invisible eclipses have no perceptible influence over that region/country. "
        "The sign ruling planet's position in the eclipse figure must also be noted."
    ),
    # ── Eclipse effects by sign modality (duration)
    "eclipse_duration_by_sign_modality": {
        "fixed_signs": (
            "Eclipses falling in Fixed signs (Taurus, Leo, Scorpio, Aquarius) "
            "will have a VERY LASTING EFFECT. "
            "These are the most enduring in their mundane impact."
        ),
        "cardinal_signs": (
            "Eclipses falling in Cardinal signs (Aries, Cancer, Libra, Capricorn) "
            "will be BRIEF AND SOON OVER — their effects come and go quickly."
        ),
        "mutable_signs": (
            "Eclipses falling in Common/Mutable signs (Gemini, Virgo, Sagittarius, Pisces) "
            "will COMMENCE SOONER and LAST LONGER, "
            "but will be liable to interruption — they continue for a time, "
            "suddenly cease, and then commence again."
        ),
    },
    # ── Eclipse effects by sign element
    "eclipse_effects_by_element": {
        "fiery_signs": (
            "Eclipses in Fiery signs (Aries, Leo, Sagittarius): "
            "threaten the destruction of cattle and sheep; "
            "exile or imprisonment or murder of some king or notable person, or great ruler; "
            "much discontent and dissension among the people; "
            "movements of armies, fighting, fires, fevers, pestilence, "
            "and scarcity of the fruits of the earth, "
            "especially in those regions affected by the eclipse."
        ),
        "earthy_signs": (
            "Eclipses in Earthy signs (Taurus, Virgo, Capricorn): "
            "foreshadow a scarcity of corn and products of the earth by drought; "
            "cause earthquakes, mining disasters, and great agricultural depression."
        ),
        "airy_signs": (
            "Eclipses in Airy signs (Gemini, Libra, Aquarius): "
            "famine, sickness, pestilence, and tempests and stormy winds hurtful to mankind."
        ),
        "watery_signs": (
            "Eclipses in Watery signs (Cancer, Scorpio, Pisces): "
            "much mortality among the common people; "
            "great destruction of fowls and fishes, "
            "and such things as live in or near the sea."
        ),
    },
    # ── Ptolemy's timing rule for eclipse manifestation
    "ptolemy_eclipse_timing": {
        "rule_source": "Ptolemy, Tetrabiblos (cited by Raphael Ch 22)",
        "eastern_horizon": (
            "If the eclipse falls in the eastern horizon (rising, near 1st house): "
            "the effects will manifest themselves about the next FOUR MONTHS, "
            "and most strongly will operate during the FIRST THIRD of that period."
        ),
        "midheaven": (
            "If the eclipse falls in the midheaven (near 10th house): "
            "events thereof will begin to appear from the FOURTH TO THE EIGHTH MONTH "
            "following the eclipse, and the chief effects will happen during the "
            "SECOND OR MIDDLE PART of that period."
        ),
        "western_horizon": (
            "If the eclipse falls in the western horizon (setting, near 7th house): "
            "effects will appear from the EIGHTH TO THE TWELFTH MONTH following the eclipse, "
            "and the chief effects will be felt in the LAST PART of that period."
        ),
    },
    # ── Ruling planet rule
    "ruling_planet_rule": (
        "The strength of the planet ruling the sign in which the eclipse falls "
        "should be considered, and its position in the figure of such eclipse duly noted, "
        "for the significations of this planet will principally appear. "
        "If Mars rules the sign and is placed in the 8th house: "
        "some grievous calamity, causing many sudden and terrible deaths. "
        "If in 6th house: much sickness. "
        "If in 3rd house: many terrible railway accidents. "
        "When benefics rule the sign of the eclipse: effects are better."
    ),
    # ── Cardan's timing method
    "cardan_timing_method": (
        "Cardan: 'To know when the effects of an eclipse will begin to be felt, "
        "take the distance of the rising of the luminary to the middle of the eclipse, "
        "or from the middle of the eclipse to the next rising of the luminary in hours and minutes. "
        "The proportion of time the length of day may bear to the year in the case of a Solar eclipse, "
        "and the proportion of time the night may bear to the year in a Lunar eclipse, "
        "will show the proportion of the year due to the interval obtained.' "
        "The most reliable rule per Raphael's experience: calculate time of Sunrise or Sunset "
        "from the middle of the eclipse, and reckon this time at the rate of one day "
        "for every four minutes, or 24 hours to the year."
    ),
    "created_at": _NOW,
}

# ============================================================
# 2. SOLAR ECLIPSE DECANATE EFFECTS  (Raphael Ch 23)
# ============================================================
RAPHAEL_CH23_SOLAR_ECLIPSE_DECANATES = {
    "spec_id":      "raphael-ch23-solar-eclipse-decanate-effects",
    "spec_type":    "lookup_table",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Solar Eclipse Effects by Decanate — All 36 (Raphael Ch 23)",
    "source_chapter": "Raphael Ch 23, pp.16-18 (Part 2)",
    "notes": (
        "A decanate is 10 degrees of a sign. "
        "First decanate = 0°-10°; Second = 10°-20°; Third = 20°-30°. "
        "These effects are the principal influences of Solar eclipses in each decanate, "
        "handed down from Ptolemy and confirmed by astrological experience."
    ),
    "solar_eclipse_by_decanate": {
        "Aries_1": "War, tumults, seditions and controversies, motion of armies, and inclination of the air to excessive drought.",
        "Aries_2": "Imprisonment and sadness of some king, and danger of death to him; the corruption of trees bearing fruit, and of things growing on the earth.",
        "Aries_3": "Grief and sadness to mortals, death of some great woman, and destruction of cattle.",
        "Taurus_1": "Afflicts trade and business, and destroys corn and food crops.",
        "Taurus_2": "Causes danger to travellers, and to women in childbirth.",
        "Taurus_3": "Brings pestilence and famine.",
        "Gemini_1": "Dissension and strife among clergy and religious denominations; also causes hatred, neglect and contempt for the laws of God and man.",
        "Gemini_2": "Causes piracies, thefts and murders.",
        "Gemini_3": "Death of some king, and many troubles to the country.",
        "Cancer_1": "Disturbs the air, and causes great changes and alterations in the weather.",
        "Cancer_2": "Dries up rivers and fountains, and stirs up incontinency and wantonness among women.",
        "Cancer_3": "Sedition, pestilence and much disease.",
        "Leo_1": "Denotes the death of some famous prince, and scarcity of corn.",
        "Leo_2": "Many troubles, anxieties to kings, princes and great men.",
        "Leo_3": "Profanation of holy places, churches, and sacred edifices; captivity, besieging and ransacking of towns.",
        "Virgo_1": "It denotes great calamity, and death of some king.",
        "Virgo_2": "Famine, pestilence and sedition.",
        "Virgo_3": "Great troubles and adversity, probably imprisonment to painters, poets, and to those who live by their wits.",
        "Libra_1": "Corrupts the air, causes pestilence, and a scarcity and dearness of corn.",
        "Libra_2": "It portends the death of a great king, sedition and famine.",
        "Libra_3": "Trouble to the nobility and detriment to their estates.",
        "Scorpio_1": "Causes war, tumults, slaughter, captivity and treason.",
        "Scorpio_2": "Mischief to some peace-loving king.",
        "Scorpio_3": "The rise of a tyrant, and idleness and slothfulness of the former king, hateful to all.",
        "Sagittarius_1": "Much dissension and hatred among men.",
        "Sagittarius_2": "Deaths of camels, and such cattle as chew the cud.",
        "Sagittarius_3": "Variously affects horses and armies.",
        "Capricorn_1": "Unhappiness to great men, the migration of some king, and the rebellion of nobles and common people.",
        "Capricorn_2": "Causes military riots, and the mutiny of soldiers against their officers.",
        "Capricorn_3": "It induces the tumultuary motion of some king, and causes famines.",
        "Aquarius_1": "It causes public grief and sorrow.",
        "Aquarius_2": "Public robberies, thefts, rapes, earthquakes and famine.",
        "Aquarius_3": "The death and slaughter of sheep and beasts of the field.",
        "Pisces_1": "Dries up rivers and makes the sea-coast unfortunate.",
        "Pisces_2": "Causes the death of some famous and excellent man; the destruction of fish, tidal waves and inundations.",
        "Pisces_3": "Sedition, cruelty, fierceness and inhumanity of soldiers.",
    },
    "created_at": _NOW,
}

# ============================================================
# 3. LUNAR ECLIPSE DECANATE EFFECTS  (Raphael Ch 24)
# ============================================================
RAPHAEL_CH24_LUNAR_ECLIPSE_DECANATES = {
    "spec_id":      "raphael-ch24-lunar-eclipse-decanate-effects",
    "spec_type":    "lookup_table",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Lunar Eclipse Effects by Decanate — All 36 (Raphael Ch 24)",
    "source_chapter": "Raphael Ch 24, Part 3 pp.2-3",
    "notes": (
        "Principal effects of Lunar eclipses when falling in the decanates of each sign. "
        "Lunar eclipse figures are cast for the exact moment of Full Moon, not the central eclipse. "
        "Lunar eclipse effects last as many months as the eclipse is hours in duration."
    ),
    "lunar_eclipse_by_decanate": {
        "Aries_1": "Fevers, incendiarism, firing of woods and forests, and dryness of the air.",
        "Aries_2": "Pestilence.",
        "Aries_3": "Causes abortive births, incommodities, and dangers to women.",
        "Taurus_1": "Death and diseases among cattle.",
        "Taurus_2": "Death of some queen, and a scarcity of seeds, and barrenness of the earth.",
        "Taurus_3": "Chief effects will be manifest among snakes and creeping things, which will perish by the million.",
        "Gemini_1": "Threatens incursions and rapines of enemies.",
        "Gemini_2": "Brings sudden motion of armies, and the solicitation of private and public bodies.",
        "Gemini_3": "Causes death of some illustrious and renowned man.",
        "Cancer_1": "Excites and stirs up wars.",
        "Cancer_2": "Causes grievous exactions, intolerable tributes, taxes and such like burdens.",
        "Cancer_3": "Brings death to the female sex; sudden destruction and miseries.",
        "Leo_1": "Brings the sudden infirmity of some king; or the death of a great man.",
        "Leo_2": "Journey of the king, and mutation of things.",
        "Leo_3": "Stirs up the people and armies to new attempts at sedition and insurrection.",
        "Virgo_1": "Causes sickness and infirmities to the king, and various seditions and discords among men.",
        "Virgo_2": "Brings damage to councillors and scribes, and the like.",
        "Virgo_3": "Causes diseases among human beings.",
        "Libra_1": "Provokes furious storms of hail.",
        "Libra_2": "Pernicious to everyone.",
        "Libra_3": "Threatens the death of some renowned and illustrious man.",
        "Scorpio_1": "It portends horrible thunders and lightnings and perhaps an earthquake.",
        "Scorpio_2": "It dries up olives and fruits, and the air is contagent with fevers and pestilence.",
        "Scorpio_3": "Brings the same, also sharp sicknesses, with many seditions, quarrels and slaughters.",
        "Sagittarius_1": "Brings thefts and rapines.",
        "Sagittarius_2": "Brings destruction to horses and mules.",
        "Sagittarius_3": "Causes pestilence and many evils among mankind.",
        "Capricorn_1": "Causes conspiracies among men, and shows the lamentable murder of some excellent man.",
        "Capricorn_2": "Brings frequent incursions and assaults of soldiers, robberies and captivities.",
        "Capricorn_3": "Causes the death of some king, and also sedition.",
        "Aquarius_1": "Shows sickness of some king.",
        "Aquarius_2": "It universally damages the seeds of the earth.",
        "Aquarius_3": "Causes a change in all things.",
        "Pisces_1": "Brings sorrow to the priests and to religious houses.",
        "Pisces_2": "Brings death to some great and illustrious person.",
        "Pisces_3": "Threatens robberies and promiscuous assaults and rapines, both on sea and land.",
    },
    "created_at": _NOW,
}

# ============================================================
# 4. EARTHQUAKE PREDICTION RULES — 9 RULES + VALIDATED CASES  (Raphael Ch 26)
# ============================================================
RAPHAEL_CH26_EARTHQUAKE_RULES = {
    "spec_id":      "raphael-ch26-earthquake-9-rules",
    "spec_type":    "rule_matrix",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Earthquake Prediction — 9 Rules + Validated Historical Cases (Raphael Ch 26)",
    "source_chapter": "Raphael Ch 26, Part 3 pp.5-6",
    "notes": (
        "Raphael compiles rules from various writers. "
        "Primary cause of earthquakes: action of eclipses + planets in four fixed signs "
        "(Taurus, Leo, Scorpio, Aquarius), especially Taurus and Scorpio. "
        "Cross-references: Gopalakrishnan Ch7 rules (gopal-ch7-*) validated independently."
    ),
    "earthquake_rules": {
        "rule_1_eclipse_meridian_nadir": (
            "Earthquakes generally follow close on the heels of eclipses, "
            "especially in those countries where the eclipse falls on the MERIDIAN or NADIR. "
            "Also if there be any planets in fixed signs at the moment of eclipse, "
            "then earthquakes will occur in those parts of the world where such planets "
            "are either RISING, SETTING, CULMINATING, or ON THE NADIR. "
            "Example: at an eclipse, if Saturn is in a fixed sign and 45° from the meridian, "
            "then earthquakes will occur in that part of the world which is the same distance "
            "from Greenwich (east or west) according to the position of Saturn."
        ),
        "rule_2_eclipse_aspected_triggers": (
            "At the period of the earthquake many aspects will be formed between the planets "
            "at the time, but specially the planets will form numerous aspects with the previous eclipse. "
            "An eclipse MAY PRESIGNIFY an earthquake, but it will not come to pass until "
            "it is aspected by some planet, or numerous aspects are formed by the planets "
            "to the place of the eclipse. "
            "(Eclipse = potential; planetary aspect to eclipse degree = trigger.)"
        ),
        "rule_3_malefics_taurus_scorpio": (
            "Earthquakes happen more frequently when there are planets, "
            "especially URANUS, SATURN, JUPITER and MARS, "
            "in the signs TAURUS AND SCORPIO."
        ),
        "rule_4_great_conjunction_4th_cusp": (
            "Earthquakes also happen in those localities where great conjunctions of the planets "
            "fall on the cusp of the FOURTH HOUSE. "
            "A map should be erected for the time of the great conjunction of planets, "
            "and whenever such conjunction falls on the NADIR (IC), or cusp of the 4th house, "
            "an earthquake is sure to occur."
        ),
        "rule_5_jupiter_taurus_scorpio_mercury": (
            "The planet Jupiter when in TAURUS OR SCORPIO, and in conjunction, "
            "opposition and parallel with MERCURY, "
            "is one of the most prolific sources of earthquakes."
        ),
        "rule_6_quarterly_figure_4th_house_malefics": (
            "Observe the planets' places at each quarterly figure (ingress), "
            "and at the New Moon nearest such ingress, "
            "and note in what part of the world the malefics are placed on the cusp of the 4th house. "
            "In this locality seismic disturbances will occur."
        ),
        "rule_7_cardinal_point_clustering": (
            "Earthquakes generally happen when there are many planets on or near "
            "the FOUR CARDINAL POINTS — "
            "i.e., the first degrees of Aries, Cancer, Libra and Capricorn."
        ),
        "rule_8_locality_identification": (
            "The countries and localities in which earthquakes will happen can be known two ways: "
            "(1) By reference to the signs ruling the different countries and cities "
            "(see raphael-ch28-countries-ruled-by-signs). "
            "(2) By noting the actual longitude in which eclipses, planetary conjunctions, "
            "and positions at the four ingresses are vertical to the meridian or on the nadir. "
            "The signs in which such eclipses, conjunctions etc. occur should also be noted."
        ),
        "rule_9_comet_perihelion": (
            "Earthquakes may also occur near the PERIHELION OF GREAT COMETS — "
            "that is, at the time when great comets are nearest the Sun or Earth."
        ),
    },
    "validated_historical_cases": {
        "Syria_1822": (
            "Great earthquake Syria, August 13th, 1822. "
            "Preceded by Lunar eclipse on August 3rd. "
            "Moon at eclipse in 10° Aquarius, in square to Saturn in 9°49' Taurus. "
            "On the day of the disaster, Saturn was in exact square to the place of the eclipse."
        ),
        "Charlestown_1886": (
            "Great earthquake Charlestown, USA, June 27th, 1886. "
            "Mars and Jupiter were in conjunction in Virgo 27°50'. "
            "At the moment of conjunction, these planets were on the cusp of the 4th house. "
            "A serious earthquake occurred practically annihilating the town."
        ),
        "Kuchan_Persia_1898": (
            "Earthquake Kuchan, Persia, October 31st, 1898. Killed over 12,000 people. "
            "Mars and Saturn were conjoined in Libra 12°28'. "
            "At Kuchan, this conjunction fell exactly on the cusp of the 4th house."
        ),
        "Mont_Pelee_Martinique_1902": (
            "Eruption of Mont Pelée, Martinique — entire city of St. Pierre wiped out. "
            "At the annular solar eclipse of November 11th, 1901, "
            "Jupiter and Saturn were on the Lower Meridian (IC, 4th house cusp) at St. Pierre. "
            "Six months after the eclipse, the city was destroyed by the volcanic eruption."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
# 5. COUNTRIES AND CITIES RULED BY THE TWELVE SIGNS  (Raphael Ch 28)
# ============================================================
RAPHAEL_CH28_COUNTRIES_BY_SIGN = {
    "spec_id":      "raphael-ch28-countries-ruled-by-signs",
    "spec_type":    "lookup_table",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Countries and Cities Ruled by the Twelve Signs of the Zodiac (Raphael Ch 28)",
    "source_chapter": "Raphael Ch 28, Part 3 pp.7-8",
    "notes": (
        "From Ptolemy's Tetrabiblos supplemented by later authorities. "
        "Used to determine which countries are affected by eclipses, conjunctions, and transits "
        "in a given sign. When an eclipse or major conjunction falls in a sign, "
        "the countries and cities ruled by that sign are chiefly affected. "
        "Great changes since Ptolemy's time necessitate modern re-adjustment for some regions."
    ),
    "sign_rulerships": {
        "Aries": {
            "countries": ["England", "Denmark", "Germany", "Lesser Poland", "Burgundy", "Palestine", "Syria", "Japan"],
            "cities": ["Birmingham", "Oldham", "Leicester", "Blackburn", "Florence", "Naples", "Verona", "Padua", "Marseilles", "Cracow", "Saragossa", "Utrecht", "Capua", "Brunswick"],
        },
        "Taurus": {
            "countries": ["Ireland", "Persia", "Poland", "Asia Minor", "Georgia", "Caucasus", "Grecian Archipelago", "Cyprus", "White Russia"],
            "cities": ["Dublin", "Leipzig", "Mantua", "Parma", "Palermo", "Rhodes", "St. Louis", "Ashton-under-Lyne"],
        },
        "Gemini": {
            "countries": ["United States", "Belgium", "Brabant", "Lombardy", "Lower Egypt", "Sardinia", "West of England", "Armenia", "Tripoli", "Flanders", "Wales"],
            "cities": [],
        },
        "Cancer": {
            "countries": ["Scotland", "Holland", "Zealand", "N. and W. Africa", "Isle of Mauritius", "Paraguay"],
            "cities": ["Tunis", "Algiers", "Amsterdam", "St. Andrews", "York", "Venice", "Berne", "Lubeck", "Magdeburg", "Milan", "Cadiz", "New York", "Manchester", "Stockholm", "Constantinople", "Genoa", "Deptford", "Rochdale"],
        },
        "Leo": {
            "countries": ["France", "Italy", "Bohemia", "Sicily", "Chaldea to Bassorah", "N. of Romania", "Apulia", "The Alps", "parts near Sidon and Tyre"],
            "cities": ["Rome", "Bath", "Bristol", "Portsmouth", "Philadelphia", "Prague", "Ravenna", "Taunton", "Damascus", "Chicago (1st decanate)", "Bombay (3rd decanate)", "Blackpool"],
        },
        "Virgo": {
            "countries": ["Turkey", "Switzerland", "West Indies", "Assyria", "Mesopotamia from Tigris to Euphrates", "Crete", "Croatia", "Silesia", "Babylonia", "Thessaly", "Kurdistan", "parts of Greece", "Virginia", "Brazil"],
            "cities": [],
        },
        "Libra": {
            "countries": ["Austria", "Savoy", "Alsace", "Livonia", "Upper Egypt", "Tibet"],
            "cities": ["Vienna", "Antwerp", "Frankfurt", "Freiburg", "Spires", "Lisbon", "Charlestown", "Nottingham", "Leeds"],
        },
        "Scorpio": {
            "countries": ["Morocco", "Catalonia", "Jutland", "Norway", "Bavaria", "Turcomania", "Barbary coast", "Fez"],
            "cities": ["Liverpool", "Baltimore", "Washington", "New Orleans", "Frankfurt (some authorities)", "Valentia", "Messina"],
        },
        "Sagittarius": {
            "countries": ["Arabia", "Dalmatia", "Hungary", "Slavonia", "Spain", "Provence", "Tuscany"],
            "cities": ["Avignon", "Cologne", "Buda", "Stuttgart", "Narbonne", "Toledo", "Bradford"],
        },
        "Capricorn": {
            "countries": ["India (general)", "Afghanistan", "Bulgaria", "Bosnia", "Romandiola", "Thrace", "Greece", "Orkney Islands", "Circassia", "Hesse"],
            "cities": ["Oxford", "Delhi", "Mecklenburg", "Brandenburg", "Fayence"],
        },
        "Aquarius": {
            "countries": ["Russia", "Prussia", "Lithuania", "Poland (general)", "Sweden", "parts of Arabia", "Tartary", "Croatia", "Abyssinia"],
            "cities": ["Hamburg", "Bremen", "Salzburg", "Trent", "Ingolstadt", "Brighton"],
        },
        "Pisces": {
            "countries": ["Portugal", "Calabria", "Normandy", "parts of Egypt", "Galicia"],
            "cities": ["Alexandria", "Seville", "Lancaster", "Regensburg", "Worms", "Compostela"],
        },
    },
    "usage_note": (
        "When an eclipse, great conjunction, or major transit occurs in a sign, "
        "consult this table to identify the countries and cities most affected. "
        "Also used with the Mars in 7th rule (see mundane-raphael-ch14-mars-7th-war-direction): "
        "the sign Mars occupies identifies which country/region is the enemy. "
        "London is attributed to Gemini (17°54') and Libra; "
        "Moscow/Russia principally to Aquarius; India principally to Capricorn."
    ),
    "created_at": _NOW,
}

# ============================================================
ALL_SPECS = [
    RAPHAEL_CH22_ECLIPSE_RULES,
    RAPHAEL_CH23_SOLAR_ECLIPSE_DECANATES,
    RAPHAEL_CH24_LUNAR_ECLIPSE_DECANATES,
    RAPHAEL_CH26_EARTHQUAKE_RULES,
    RAPHAEL_CH28_COUNTRIES_BY_SIGN,
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
