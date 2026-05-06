"""
Mundane Astrology — Engine Specs v6
Batch: mundane-engine-v6-20260506

Source: Gopalakrishnan, "Mundane Astrology" (ICAS)
  Chapter 8  — Predicting Wars (book pp.99-129)
  Chapter 9  — Yearly Predictions Framework (book pp.130-162)

Spec types: lookup_table, rule_matrix, classification
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
_BATCH     = "mundane-engine-v6-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ============================================================
# 1. WAR PREDICTION FRAMEWORK — DASA/BHUKTHI METHOD  (Gopalakrishnan Ch 8)
# ============================================================
GOPAL_CH8_WAR_PREDICTION_FRAMEWORK = {
    "spec_id":      "gopal-ch8-war-prediction-framework",
    "spec_type":    "rule_matrix",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "War Prediction — Dasa/Bhukthi Framework + India-Pakistan Case Table",
    "source_chapter": "Gopalakrishnan Ch 8, pp.99-129",
    "notes": (
        "Gopalakrishnan's primary war-prediction methodology uses the national chart's "
        "Vimshottari dasa/bhukthi/antara running at the time of the conflict. "
        "The quality of the dasa (benefic/malefic, 6th-lord involvement) determines "
        "whether war starts, how long it lasts, and whether the country wins or loses."
    ),
    # ── Core war-trigger rules
    "war_trigger_rules": {
        "6th_lord_dasa_activation": (
            "When a country runs the dasa of its 6th house lord: "
            "insurgency, border conflicts, terrorism, and open war are activated. "
            "E.g., Sri Lanka ran Rahu Dasha from 1992; Rahu = 6th lord → insurgency (LTTE) peaked."
        ),
        "saturn_transiting_natal_rahu": (
            "Saturn transiting over the country's natal Rahu position: "
            "war or military skirmishes with neighbouring states. "
            "Rule specific to India's chart: 'Whenever Saturn has gone over India's Rahu, "
            "there have been fights.'"
        ),
        "india_pakistan_2_12_lagna_axis": (
            "India and Pakistan have their natal lagnas (Ascendants) in a 2/12 relationship "
            "(one nation's lagna falls in the 2nd from the other's, and vice versa). "
            "This structural tension means they can never get along permanently — "
            "border tension, infiltration, and conflict will recur cyclically."
        ),
        "malefic_bhukthi_antara_during_6th_dasa": (
            "War breaks out when a malefic planet's bhukthi or antara runs within the 6th lord dasa. "
            "E.g., India 1965 war: Saturn dasa / Jupiter bhukthi / Rahu antara."
        ),
    },
    # ── War duration rule
    "war_duration_rule": (
        "Indian wars were all short because India was running good overall dasa periods "
        "(Venus dasa, Mercury dasa) during the conflicts. "
        "Wars end when a favorable raja yoga bhukthi or moon antara begins. "
        "Had India run a long malefic dasa (like Sri Lanka's prolonged Rahu dasa from 1992), "
        "wars would have been prolonged with heavy bloodshed."
    ),
    # ── India-Pakistan war historical table
    "india_pakistan_war_table": {
        "1947-48_partition_war": {
            "period": "1947 – 1 Jan 1949",
            "dasa": "Saturn", "bhukthi": "Saturn", "antara": "Mercury → Rahu",
            "outcome": "Mercury bhukthi favourable for India — war contained.",
        },
        "1965_war": {
            "period": "Apr 1965 – 1 Jan 1966",
            "dasa": "Saturn", "bhukthi": "Jupiter", "antara": "Rahu",
            "outcome": "Mercury dasa and bhukthi favourable for India — ceasefire Sep 23.",
            "note": (
                "Indian gains led to Pakistani counterattack Sep 1. UN ceasefire Sep 20. "
                "India accepted Sep 21, Pakistan Sep 22, war ended Sep 23. "
                "Tashkent Declaration Jan 10 1966."
            ),
        },
        "1971_war": {
            "period": "6 Dec 1971 – 1972",
            "dasa": "Mercury", "bhukthi": "Sun", "antara": "Mars",
            "outcome": "Moon bhukthi (raja yoga) started → war came to end. India decisive victory.",
        },
        "kargil_1999": {
            "period": "Apr 1999 – Jun 1999",
            "dasa": "Venus", "bhukthi": "Rahu", "antara": "Sun",
            "outcome": "Got ended in Moon antara — India recaptured positions.",
        },
    },
    # ── Sri Lanka case study
    "sri_lanka_case_study": {
        "chart_details": (
            "Sri Lanka lagna lord = Sun; 6th lord = Saturn; 10th lord from lagna in 11th house with Mars; "
            "10th lord from Moon in 8th house; 10th lord from Karakamsa in 12th house. "
            "Implication: 'the government can NEVER function in peace.'"
        ),
        "rahu_dasha_1992": (
            "Sri Lanka ran Rahu Dasha from 1992. In mundane astrology, 6th lord dasha = "
            "problems related to terrorist attacks and insurgency. "
            "Rahu = 6th lord for Sri Lanka → LTTE insurgency intensified."
        ),
        "saturn_in_kataka": (
            "When Saturn enters Kataka (Cancer) for Sri Lanka: "
            "Sept 2004 to 2006 — lot of bloodshed and loss of lives. "
            "A very important leader will be assassinated in the next 3 years [predicted 2005]."
        ),
        "venus_bhukthi_peace": (
            "Venus Bhukthi = very good: Venus is 3rd and 10th lord in 11th house from lagna; "
            "1st and 8th lord in 9th house from Karakamsa; 2nd and 9th lord in 10th house from Chandra. "
            "Peace process possible but slow and back-and-forth."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
# 2. 12-HOUSE CLASSIFICATION FOR NATIONAL CHART ANALYSIS  (Gopalakrishnan Ch 9)
# ============================================================
GOPAL_CH9_NATIONAL_CHART_12_HOUSES = {
    "spec_id":      "gopal-ch9-national-chart-12-house-classification",
    "spec_type":    "classification",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "12-House Significance for National Chart Analysis — Gopalakrishnan Classification",
    "source_chapter": "Gopalakrishnan Ch 9, pp.130-145",
    "notes": (
        "This classification is used for national/country chart interpretation. "
        "The house lord's strength and any afflictions determine the outcome in that domain. "
        "Key trika houses for negative events: 6th (sickness/war), 8th (death/crisis), "
        "12th (loss/expenses). Eclipse or malefic clustering in these houses = crises."
    ),
    "house_significance": {
        "1": (
            "Attitude, confidence, and identity of the country and nation. "
            "Plans and their execution style. "
            "Rahu in 1st house: confusion, irritation, and mass upheavals in the country."
        ),
        "2": (
            "Speech of the people; parliamentary proceedings; "
            "the food industry; banks. "
            "The money position: GDP, inflation of the country."
        ),
        "3": (
            "IT sector; infrastructure; travel and tourism. "
            "The sports persons of the country. Communication industries."
        ),
        "4": (
            "Rains and agriculture outputs; car and vehicle industry; "
            "construction and housing industry. Land matters."
        ),
        "5": (
            "Educational policy; children; religious institutions. "
            "Speculative markets (stock market short-term)."
        ),
        "6": (
            "Sickness or epidemic; mass death; war with other countries; "
            "the debts position; the medical and hospital industry. "
            "Enemy nations, labour disputes."
        ),
        "7": (
            "Trade with other countries; world trade organization; "
            "bilateral trade and relationships with neighbours and partners. "
            "Foreign trade, treaties, open enemies."
        ),
        "8": (
            "Death of people/leader; tensions in the country; mass deaths. "
            "Longevity of the nation/government. Calamities."
        ),
        "9": (
            "Judiciary and politicians; rules and corruption; "
            "higher education policies. Religion, long-distance travel, exports."
        ),
        "10": (
            "How the country is ruled; economic growth; "
            "stock market performance. Government in power, ruling party strength."
        ),
        "11": (
            "Income and trade of the country. "
            "Profits, allies, imports, earnings from exports."
        ),
        "12": (
            "Expenses and foreign trade of the country. "
            "Losses, imports, expenditure, foreign debt, exile."
        ),
    },
    "trika_houses_warning": (
        "Houses 6, 8, and 12 are the trika (malefic) houses for national charts. "
        "Eclipse or malefic clustering in these houses = crises in the corresponding domain. "
        "Eclipse in 6/8/12 axis = very negative per Detail D framework."
    ),
    "created_at": _NOW,
}

# ============================================================
# 3. YEARLY PREDICTION — 14 METHODS + OPERATIONAL FRAMEWORK  (Gopalakrishnan Ch 9)
# ============================================================
GOPAL_CH9_YEARLY_PREDICTION_METHODS = {
    "spec_id":      "gopal-ch9-yearly-prediction-14-methods",
    "spec_type":    "lookup_table",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Yearly Prediction — 14 Methods + Details A-D Operational Framework",
    "source_chapter": "Gopalakrishnan Ch 9, pp.145-162",
    "notes": (
        "Gopalakrishnan enumerates 14 methods for yearly predictions, "
        "then provides a detailed 4-step operational framework (Details A-D) "
        "for extracting the most important signals. "
        "He personally uses Tajika chart + Dasa/Bhukthi/Antara as primary tools."
    ),
    # ── 14 methods
    "yearly_prediction_methods": {
        "1_rama_navami_chart": (
            "Cast chart for Rama Navami day. Followed as tradition by many astrologers "
            "because Lord Rama is considered the real ruler of the country. "
            "Many panchagas follow this method."
        ),
        "2_tajika_independence_chart": (
            "Use the Tajika (solar return) chart of India's independence horoscope. "
            "Gopalakrishnan's preferred primary method."
        ),
        "3_republican_chart": "Use the Republican chart of the country.",
        "4_pm_coronation_chart": "Use the coronation chart of the Prime Minister.",
        "5_governor_coronation_chart": (
            "Use the coronation chart of the Governor or Chief Minister. "
            "Applicable to most American states for state-level predictions."
        ),
        "6_chakras": "Use chakras: Rasi Sangatthi Chakra and Sarvato Bhadra Chakra.",
        "7_dasa_bhukthi_antara": (
            "Use the Dasa and Bhukthi of the country's national chart. "
            "Predictions given for each antara. "
            "Example: India's Mercury dasa → Mercury antara, then Ketu, then Venus, etc. "
            "Predictions made based on each antara period."
        ),
        "8_transit_movements": (
            "Use transit movements of the smaller and big planets. "
            "Note the time Jupiter enters the next sign, calculate lagna, and predict."
        ),
        "9_monthly_pravesh": (
            "Monthly pravesh — note the date on which the Sun enters the next sign "
            "and accordingly give predictions. Sum of all 12 months = yearly prediction."
        ),
        "10_snapshot_predictions": (
            "Snapshot predictions like Kandaya Palan — "
            "for gain, loss, happiness and unhappiness values."
        ),
        "11_year_deity_panchaga": "Use the year deity from the Panchaga for predictions.",
        "12_modern_methods": "Some predict with modern methods: runes, tarot cards, and numerology.",
        "13_diwali_amavasaya": "Use the Diwali Amavasaya for stock market predictions and yearly chart for other events.",
        "14_nimitta": "Some are very good at intuition and use Nimitta for predictions.",
    },
    # ── Three main areas of interest for yearly predictions
    "three_main_areas": {
        "economy": "How will the economy perform? GDP, trade, markets, inflation.",
        "rains_agriculture": "How will the rain pattern be? Directly affects agriculture.",
        "political_stability": "How will political stability be? Government survival, elections, coalitions.",
    },
    # ── Details A-D: Operational framework for annual prediction
    "operational_framework": {
        "detail_A_major_planet_movements": {
            "description": "See the major movements of Saturn, Rahu, and Jupiter.",
            "rasi_sandhi": (
                "These planets in rasi sandhi (sign boundary) give lot of confusion and instability. "
                "Saturn/Rahu/Jupiter at 29°-0° of a sign = turbulent transition period."
            ),
            "trika_house_entry": (
                "See if these planets are going into 6th, 8th, or 12th lords or houses. "
                "This will trigger a lot of negative events."
            ),
            "saturn_over_10th_lord": (
                "Saturn over the natal 10th lord (by transit conjunction): changes in leadership. "
                "E.g., Saturn over India's natal Saturn → many astrologers predicted Manmohan Singh "
                "or NDA government will not stay long in power."
            ),
        },
        "detail_B_abnormal_long_transit": (
            "See whether any planet abnormally stays in a sign for a long period of time. "
            "Example: Mars in Kumbha (Aquarius) for more than 6 months; "
            "Mercury in Pisces for more than 10 weeks (normally less than 4 months). "
            "Abnormally long transits amplify that sign's mundane effects significantly."
        ),
        "detail_C_planetary_bundle": {
            "description": (
                "See whether planets bundle up together. Normally Sun, Venus and Mercury will be together. "
                "Sometimes they get joined by Jupiter, Rahu, and Saturn. "
                "Concentration of 5 or more planets within 30° is a problem."
            ),
            "sensitive_house_positions": (
                "If this bundling happens in the country's 6th, 8th, 12th, 10th, or 1st houses "
                "— there are serious problems."
            ),
            "case_study_may_2003": (
                "May 2003: Saturn+Mars in Taurus, Ketu+Mars in Scorpio. Predictions: "
                "mass deaths globally; world markets depressed; Saddam regime overthrown; "
                "tension in South Korea, North Korea, Czech Republic, US, Iraq, India, Pakistan; "
                "Coffee sector suffers; Industries face worst problems."
            ),
        },
        "detail_D_eclipse_trika": (
            "See if there is an eclipse in the 6/8/12 axis. It is very negative. "
            "Eclipse in these houses of the national chart = significant negative events "
            "in the domains governed by those houses."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
ALL_SPECS = [
    GOPAL_CH8_WAR_PREDICTION_FRAMEWORK,
    GOPAL_CH9_NATIONAL_CHART_12_HOUSES,
    GOPAL_CH9_YEARLY_PREDICTION_METHODS,
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
