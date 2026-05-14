"""
Mundane Astrology — Engine Specs INGEST v16
===========================================
Batch : mundane-engine-v16-20260506
Collection : mundane_engine_specs
Science    : mundane_jyotish

Chapters encoded:
  Gaur Ch 5  — Ardra Entry / Monsoon Engine (tithi × 16, weekday × 7,
               Moon nakshatra × 27, Nitya Yoga × 27, time-of-entry × 7)
               + Rohini / Samudra Chakra spatial grid
  Gaur Ch 6  — Weather Engine:
               Snake Trinadi (Heaven / Earth / Patal, 9 nakshatras each, 8 rules)
               Constellation ownership (Sun/Moon) + gender (male/female/eunuch)
               Saptnadi precipitation engine (7 nadis × 28 constellations + Vedha rules)
               Planetary rain combinations (20 technical rules)
  Gaur Ch 7  — Sasya Jatak crop engine (10 yield yogas + inverse pricing rule)
  Gaur Ch 8  — Material & Commodity database
               (planetary governance, zodiac signification,
                nakshatra precision mapping 28 rows, nomenclature rule)
  Gaur Ch 9  — Sarvatobhadra trade engine
               (motion logic, 28-row constellation Vedha impact matrix)

DRY_RUN = True  →  set False (or use run_mundane_ingest.py) to write to MongoDB.
"""

import asyncio
import os
import sys
import types
from datetime import datetime, timezone

# ── motor stub (fires only when motor is absent) ──────────────────────────────
if "motor" not in sys.modules:
    _motor     = types.ModuleType("motor")
    _motor_asy = types.ModuleType("motor.motor_asyncio")
    class _FakeClient:
        def __getitem__(self, k): return self
        def __getattr__(self, k): return self
        async def update_one(self, *a, **kw): pass
    _motor_asy.AsyncIOMotorClient = _FakeClient
    sys.modules["motor"]                  = _motor
    sys.modules["motor.motor_asyncio"]    = _motor_asy

from motor.motor_asyncio import AsyncIOMotorClient   # noqa: E402

# ── config ────────────────────────────────────────────────────────────────────
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.environ.get("DB_NAME",  "horoscope_db")
DRY_RUN   = True

_BATCH = "mundane-engine-v16-20260506"
_NOW   = datetime.now(timezone.utc).isoformat()

def _spec(spec_id, spec_type, title, source, description, **fields):
    doc = {
        "spec_id":    spec_id,
        "spec_type":  spec_type,
        "science_id": "mundane_jyotish",
        "batch_id":   _BATCH,
        "title":      title,
        "source":     source,
        "description": description,
        "created_at": _NOW,
    }
    doc.update(fields)
    return doc

# ═════════════════════════════════════════════════════════════════════════════
# SPEC 1 — Gaur Ch 5: Ardra Entry Monsoon Engine
# ═════════════════════════════════════════════════════════════════════════════
GAUR_CH5_ARDRA_MONSOON_ENGINE = _spec(
    spec_id   = "gaur-ch5-ardra-monsoon-engine",
    spec_type = "multi_factor_lookup",
    title     = "Ardra Entry Monsoon Engine — Tithi × Weekday × Nakshatra × Yoga × Time",
    source    = "gaur_aifas_ch5",
    description = (
        "The Sun's entry into Ardra nakshatra (~June) marks the astrological 'birth' "
        "of the Indian monsoon. Five independent filters — Tithi, Weekday, Moon's "
        "nakshatra at entry, Nitya Yoga, and Time of Entry — are combined to forecast "
        "rainfall volume, agricultural yield, social outcomes, and public health for "
        "the entire rainy season."
    ),
    ardra_entry_tithi_results = {
        "pratipada":   "Lucky and auspicious.",
        "dviteeya":    "Grains will be abundant.",
        "triteeya":    "Warning: Increased riots.",
        "chaturthi":   "Unlucky results.",
        "panchmi":     "Highly beneficial for the nation.",
        "shashthi":    "Good for all creatures.",
        "saptami":     "Lucky.",
        "ashtami":     "High grain production.",
        "navami":      "Fear of unrest.",
        "dashmi":      "Good results.",
        "ekadashi":    "Grains will be cheap.",
        "dwadashi":    "Lucky.",
        "triyodashi":  "Good rains.",
        "chaturdashi": "Grains and clothes expensive.",
        "poornamasi":  "Desires fulfilled.",
        "amavasya":    "Crops damaged; unlucky for rulers.",
    },
    ardra_entry_weekday_results = {
        "sunday":    "Harmful for cattle.",
        "monday":    "Good crops; prices drop.",
        "tuesday":   "Rulers suffer.",
        "wednesday": "Cheap prices; excellent crops.",
        "thursday":  "Prosperous season.",
        "friday":    "Peace prevails across the land.",
        "saturday":  "Unlucky: probability of disease and epidemics.",
    },
    moon_nakshatra_at_entry_27_rows = {
        "ashwini":         "Cattle increase; dangers also increase.",
        "bharani":         "Unlucky; more diseases.",
        "krithika":        "Fire risk; deficient rain.",
        "rohini":          "High grain output; satisfaction.",
        "mrigshira":       "High output; low prices.",
        "ardra":           "Unlucky; violence increases.",
        "punarvasu":       "Abundant grains.",
        "pushya":          "Maximum rain; national bumper harvest.",
        "ashlesha":        "Unlucky; comforts minimized; poor rain.",
        "magha":           "Rains and crops below average.",
        "poorvaphalguni":  "Fame of rulers spreads.",
        "uttaraphalguni":  "Grains enhanced; population growth.",
        "hast":            "Comforts of people increase.",
        "chitra":          "High pulse/grain yield; lucky.",
        "swati":           "Grains enhanced.",
        "vishakha":        "Diseases wiped out.",
        "anuradha":        "National satisfaction.",
        "jyeshtha":        "Public fear.",
        "mool":            "Public fear; disease increase.",
        "poorvashadh":     "Opposition amongst rulers.",
        "uttarashadh":     "Fortunate; busy and productive population.",
        "shravan":         "Lucky; wealth accumulation.",
        "dhanishtha":      "Lucky and auspicious.",
        "shatbhisha":      "Heavy rainfall.",
        "poorvabhadrapad": "Unlucky; loss of comfort.",
        "uttarabhadrapad": "Success in all endeavors.",
        "revti":           "Unlucky; troublesome for rulers.",
    },
    nitya_yoga_diagnostics_27_rows = {
        "vishkumbh":  "Lucky for crops.",
        "preeti":     "Increased rainfall.",
        "aayushman":  "Good character in rulers.",
        "saubhagya":  "Good health and fortune.",
        "shobhan":    "Noble deeds in population.",
        "atigand":    "Opposition in rulers.",
        "sukarma":    "Religious and noble boost.",
        "dhriti":     "Low prices; free availability.",
        "shool":      "Disease increase.",
        "gand":       "Lucky and auspicious.",
        "vriddhi":    "Religious growth; population increase.",
        "dhruv":      "Disenchantment with rulers.",
        "vyaghat":    "CRITICAL: Drought and high prices.",
        "harshan":    "Cheap grains; increased comfort.",
        "vajra":      "Bitterness among rulers.",
        "siddhi":     "High production but disease spread.",
        "vyatipat":   "Wealth destruction.",
        "variyan":    "Poor rain and crops.",
        "parigh":     "Rulers suffer; values and wealth reduced.",
        "shiv":       "Harmony and prosperity.",
        "siddha":     "New inventions; national success.",
        "sadhya":     "Stalled projects completed.",
        "shubh":      "More rain; higher comfort.",
        "shukla":     "Good rain and crops.",
        "brahma":     "Medium rains.",
        "endra":      "Sufficient rains.",
        "vaidhriti":  "Disease increase.",
    },
    time_of_entry_results = {
        "sunrise":           "High incidence of disease.",
        "2_hours_post_sunrise": "Increased conflicts.",
        "afternoon":         "Poor crops; expensive grains.",
        "sunset":            "Good crops; cheap grains.",
        "night":             "People live with comforts.",
        "midnight":          "All diseases increase.",
        "after_midnight":    "First half lucky; second half bad.",
    },
    ardra_entry_horoscope_diagnostic = {
        "preparation_method": "Cast horoscope for the precise moment Sun enters Ardra.",
        "high_yield_gate":    (
            "IF (Sun AND Moon in quadrants 1/4/7/10 OR trines 5/9) AND "
            "(Moon in Watery Sign) AND (Benefic Aspects) THEN Result = 'Excellent Grain Production'."
        ),
        "crop_failure_veto":  (
            "IF (Malefic Aspects dominate Sun/Moon) THEN Result = 'Crop Destruction/Loss'."
        ),
        "case_study_2059_2002": {
            "moon_placement":    "Scorpio (Watery) in 5th House (Trine) with Ketu.",
            "aspect_audit":      "Aspected by Mercury, Saturn, and Rahu (Malefics).",
            "sun_status":        "In 12th House with Mars and Jupiter.",
            "prediction_outcome": (
                "Sufficient rain BUT losses expected due to floods/droughts in localized regions."
            ),
        },
    },
    logic_gates = {
        "pushya_ardra_multiplier": (
            "IF (Moon in Pushya during Ardra Entry) THEN Agricultural_Yield_Weight += 0.6 "
            "(national bumper harvest signal)."
        ),
        "afternoon_entry_veto": (
            "Afternoon entry overrides positive Yogas → Market Scarcity Alert for grains."
        ),
        "rohini_mountain_alert": (
            "IF Rohini resides in Mountain sector THEN trigger Hydrological Stress warning "
            "regardless of weekday result."
        ),
    },
)

# ═════════════════════════════════════════════════════════════════════════════
# SPEC 2 — Gaur Ch 5: Rohini / Samudra Chakra Spatial Grid
# ═════════════════════════════════════════════════════════════════════════════
GAUR_CH5_ROHINI_SAMUDRA_CHAKRA = _spec(
    spec_id   = "gaur-ch5-rohini-samudra-chakra",
    spec_type = "spatial_grid",
    title     = "Rohini / Samudra Chakra — Annual Moisture Residence Grid",
    source    = "gaur_aifas_ch5",
    description = (
        "Locates where the year's moisture 'resides' (Sea, Shore, Mountain, or Junction) "
        "by mapping all 28 constellations (including Abhijit) outward from the Aries Ingress "
        "nakshatra using a repeating 7-point Sea-Shore-Mountain-Junction cycle. "
        "The residence determines rainfall volume and the socio-economic 'Residence of Time'."
    ),
    initialization_logic = (
        "Starting from the constellation active at Aries (solar) Ingress, assign 28 "
        "constellations in the repeating cycle below."
    ),
    spatial_mapping_cycle = {
        "positions_1_2": "Sea (Samudra)   — maximum moisture",
        "positions_3_4": "Shore (Tata)    — sufficient moisture",
        "position_5":    "Mountain (Parvat) — drought risk",
        "positions_6_7": "Junction (Sandhi) — erratic moisture",
        "note":          "The 7-point cycle repeats 4× to cover all 28 constellations.",
    },
    rohini_residence_results = {
        "sea":    "Maximum rains; sufficient crop production; Gardener's house residence.",
        "shore":  "Sufficient rains; accumulation of grains; Washerman's house residence.",
        "sandhi": "Less rains; crops do not suffer significantly; Trader's house residence.",
        "mountain": "Scanty rains; acute crop suffering (drought); Potter's house residence.",
    },
    residence_of_time = {
        "sea_residence":    "Time resides at the Gardener's house — lush prosperity.",
        "shore_residence":  "Time resides at the Washerman's house — stable economy.",
        "sandhi_residence": "Time resides at the Trader's house — moderate conditions.",
        "mountain_residence": "Time resides at the Potter's house — fragile economy, scarcity.",
    },
    example_2059_2002 = {
        "aries_ingress_nakshatra": "Ashwini",
        "cycle_assignment": {
            "ashwini_bharani":    "Sea",
            "krithika_rohini":    "Shore",
        },
        "rohini_residence": "Shore",
        "result": "Sufficient rains; accumulation of grains.",
    },
    samudra_cycle_automation = (
        "Rule of 7: identify Aries Ingress Nakshatra, place Rohini (4th nakshatra) "
        "into its correct slot automatically."
    ),
    watery_trine_modifier = (
        "IF (Ardra Horoscope watery sign in 1st or 5th house) THEN Flood_Risk_Weight += 0.4 "
        "even when rain volume is normal."
    ),
)

# ═════════════════════════════════════════════════════════════════════════════
# SPEC 3 — Gaur Ch 6: Snake Trinadi Weather Engine
# ═════════════════════════════════════════════════════════════════════════════
GAUR_CH6_TRINADI_WEATHER_ENGINE = _spec(
    spec_id   = "gaur-ch6-snake-trinadi-weather-engine",
    spec_type = "atmospheric_grid",
    title     = "Snake Shaped Trinadi Weather Engine — Heaven / Earth / Patal",
    source    = "gaur_aifas_ch6",
    description = (
        "Maps all 27 nakshatras into three vertical realms (Heaven, Earth, Patal). "
        "Planetary concentration within a single Nadi triggers specific weather outcomes "
        "from continuous heavy rain to total drought. Eight exhaustive rules govern the "
        "interaction of malefics and benefics across these realms."
    ),
    trinadi_nakshatra_mapping = {
        "heaven_beginning": [
            "Ashwini", "Ardra", "Punarvasu", "Uttaraphalguni",
            "Hast", "Jyeshtha", "Moola", "Shatbhisha", "Poorvabhadrapad",
        ],
        "earth_middle": [
            "Bharani", "Mrigshira", "Pushya", "Poorvaphalguni",
            "Chitra", "Anuradha", "Poorvashadh", "Dhanishtha", "Uttarabhadrapad",
        ],
        "patal_infinity": [
            "Krittika", "Rohini", "Ashlesha", "Magha",
            "Swati", "Vishakha", "Uttarashadha", "Shravan", "Revati",
        ],
    },
    trinadi_logic_rules = {
        "rule_1_universal_concentration": {
            "condition": "IF (All benefic AND malefic planets occupy one Nadi)",
            "result":    "Maximum precipitation; rains continue until planets exit the Nadi.",
        },
        "rule_2_royal_conjunction": {
            "condition": "IF (Strong Sun AND Jupiter occupy one Nadi)",
            "result":    "Good and auspicious rainfall.",
        },
        "rule_3_male_concentration": {
            "condition": "IF (All male planets occupy one Nadi)",
            "result":    "Danger of excessive and destructive rains.",
        },
        "rule_4_female_eunuch_concentration": {
            "condition": "IF (Female AND Eunuch planets occupy one Nadi)",
            "result":    "Severe hazard: danger of hail storms.",
        },
        "rule_5_heavenly_mix": {
            "condition": "IF (Malefics AND benefics together in Heaven Nadi)",
            "result":    "Heavy rainfall.",
        },
        "rule_6_heaven_earth_mix": {
            "condition": "IF (Malefics in Heaven AND benefics in Earth Nadi)",
            "result":    "Rainfall occurs.",
        },
        "rule_7_heaven_patal_split": {
            "condition": "IF (Malefics in Heaven AND benefics in Patal Nadi)",
            "result":    "Scarcity of rains; impending drought.",
        },
        "rule_8_patal_heaven_split": {
            "condition": "IF (Malefics in Patal AND benefics in Heaven Nadi)",
            "result":    "STRICT VETO: No rains whatsoever.",
        },
    },
    planet_gender_classification = {
        "male_planets":   ["Sun", "Mars", "Saturn", "Rahu", "Ketu"],
        "female_planets": ["Moon", "Venus"],
        "eunuch_planets": ["Mercury"],
    },
)

# ═════════════════════════════════════════════════════════════════════════════
# SPEC 4 — Gaur Ch 6: Constellation Ownership & Gender Weather Engine
# ═════════════════════════════════════════════════════════════════════════════
GAUR_CH6_CONSTELLATION_GENDER_ENGINE = _spec(
    spec_id   = "gaur-ch6-constellation-gender-weather-engine",
    spec_type = "atmospheric_lookup",
    title     = "Constellation Ownership & Gender Weather Engine",
    source    = "gaur_aifas_ch6",
    description = (
        "Two secondary atmospheric filters: (1) Sun/Moon ownership of nakshatras — "
        "when both luminaries occupy each other's stars, rain is confirmed; "
        "(2) Male/Female/Eunuch gender classification — determines airflow, temperature, "
        "and precipitation based on gender interaction of the two luminaries."
    ),
    constellation_ownership_map = {
        "sun_owned_stars": [
            "Rohini", "Mrigshira", "Poorvaphalguni", "Uttaraphalguni", "Hast",
            "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mool",
            "Shatbhisha", "Poorvabhadrapad",
        ],
        "moon_owned_stars": [
            "Ashwini", "Bharani", "Krithika", "Ardra", "Punarvasu", "Pushya",
            "Ashlesha", "Magha", "Poorvashadh", "Uttarashadh", "Shravan",
            "Dhanishtha", "Uttarabhadrapad", "Revti",
        ],
    },
    ownership_weather_rules = {
        "sun_in_sun_star":   "Atmospheric result: Air will flow; dry conditions.",
        "moon_in_moon_star": "STRICT VETO: No rains whatsoever.",
        "cross_ownership":   "IF Sun in Moon star AND Moon in Sun star THEN rains confirmed.",
        "example": (
            "Sun in Punarvasu (Moon star) + Moon in Mrigshira (Sun star) = Rain."
        ),
    },
    gender_classification_matrix = {
        "male_constellations": [
            "Ashwini", "Bharani", "Krithika", "Rohini", "Mrigshira", "Mool",
            "Poorvashadh", "Uttarashadh", "Shravan", "Dhanishtha", "Shatbhisha",
            "Poorvabhadrapad", "Uttarabhadrapad", "Revti",
        ],
        "female_constellations": [
            "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
            "Poorvaphalguni", "Uttaraphalguni", "Hast", "Chitra", "Swati",
        ],
        "eunuch_constellations": ["Vishakha", "Anuradha", "Jyeshtha"],
    },
    gender_interaction_results = {
        "male_male":          "The sky remains clear.",
        "female_female":      "Good airflow or sky becomes clouded (rain not guaranteed).",
        "female_male":        "Good rains.",
        "eunuch_eunuch":      "Airflow good; high atmospheric temperature.",
        "male_female_eunuch": "Light rains.",
        "example": (
            "Sun in Punarvasu (Female) + Moon in Revti (Male) = Good rains."
        ),
    },
    logic_gates = {
        "cross_ownership_multiplier":
            "Sun and Moon in swapped stars triggers Rain Certainty diagnostic.",
        "eunuch_heat_filter":
            "If both luminaries in Eunuch stars → Heatwave Warning: high temperatures, dry winds.",
        "clear_sky_veto":
            "Both planets in Male stars overrides minor moisture indicators → Clear Horizon.",
    },
)

# ═════════════════════════════════════════════════════════════════════════════
# SPEC 5 — Gaur Ch 6: Saptnadi Precipitation Engine
# ═════════════════════════════════════════════════════════════════════════════
GAUR_CH6_SAPTNADI_ENGINE = _spec(
    spec_id   = "gaur-ch6-saptnadi-precipitation-engine",
    spec_type = "atmospheric_grid",
    title     = "Saptnadi Precipitation Engine — 7 Elemental Atmospheric Channels",
    source    = "gaur_aifas_ch6",
    description = (
        "Maps 28 constellations (including Abhijit) into seven atmospheric Nadis: "
        "Chanda, Vayu, Dahan, Saumya, Neera, Jala, Amrita. Vedha (two or more planets "
        "in one Nadi) triggers specific weather — from firestorms (Dahan) to continuous "
        "rain for 7 days (Amrita). Duration is controlled by Moon-degree precision logic."
    ),
    saptnadi_constellation_mapping = {
        "chanda_nadi": {
            "stars":  ["Krithika", "Vishakha", "Anuradha", "Bharani"],
            "lord":   "Saturn",
            "gender": "Neutral/Eunuch",
            "result": "Vedha = Winds and Storms (malefics) or Strong Winds.",
        },
        "vayu_nadi": {
            "stars":  ["Rohini", "Swati", "Jyeshtha", "Ashwini"],
            "lord":   "Sun",
            "gender": "Male",
            "result": "Vedha = High Velocity Airflow.",
        },
        "dahan_nadi": {
            "stars":  ["Mrigshira", "Chitra", "Moola", "Revti"],
            "lord":   "Mars",
            "gender": "Male",
            "result": "Vedha = Fires on Earth.",
        },
        "saumya_nadi": {
            "stars":  ["Ardra", "Hast", "Poorvashadh", "Uttarabhadrapad"],
            "lord":   "Jupiter",
            "gender": "Male",
            "result": "Vedha = Lucky and Auspicious conditions.",
        },
        "neera_nadi": {
            "stars":  ["Punarvasu", "Uttaraphalguni", "Uttarashadh", "Poorvabhadrapad"],
            "lord":   "Venus",
            "gender": "Female",
            "result": "Vedha = Light Rains.",
        },
        "jala_nadi": {
            "stars":  ["Pushya", "Poorvaphalguni", "Abhijit", "Shatbhisha"],
            "lord":   "Mercury",
            "gender": "Male",
            "result": "Vedha = Excessive Rains; rain for 36–72 hours.",
        },
        "amrita_nadi": {
            "stars":  ["Ashlesha", "Magha", "Shravan", "Dhanishtha"],
            "lord":   "Moon",
            "gender": "Female",
            "result": "Vedha = Good Rains; rain 1–7 days (Moon is lord of this Nadi).",
        },
    },
    vedha_definition = "IF (Count of planets in Nadi >= 2) THEN Vedha (Obstruction) triggered.",
    residence_and_degree_logic = {
        "point_1_conjunction":   "Moon + Cruel + Gentle in 1 star in Nadi → Rain that day.",
        "point_2_longitudinal":  "Cruel + Gentle on star + Planet_Degree == Moon_Degree → Heavy Rain.",
        "point_3_homogeneity":   "Only Gentle OR Only Cruel in Nadi + Moon present → Light Rain/Clouds.",
        "point_4_lord_presence": "Nadi Lord in Nadi + Weak Moon present → Rain occurs.",
        "point_5_duration":      (
            "Gentle + Cruel in Amrita + Moon → Rain 1–7 days (multiple times). "
            "In Jala Nadi → Rain 36–72 hours."
        ),
    },
    gender_vedha_results = {
        "two_males":   "Air flows in all directions.",
        "male_female": "There will be rains.",
        "two_eunuchs": "Dust storms.",
    },
    planetary_rain_combinations_20 = {
        "bullish_rain_triggers": [
            "Mercury + Jupiter in one sign",
            "Mars + Venus + Saturn aspected by Jupiter",
            "Retrograde Gentle planets",
            "Sun in Cancer aspected by Jupiter",
            "Mars in 7th from Venus AND Jupiter in 7th from Saturn = Catastrophic floods",
            "Moon + Cruel + Gentle planets together in Amrita Nadi = Rain 1-7 days",
            "All planets in one Nadi = Continuous heavy rain until planets exit",
        ],
        "dryness_veto": [
            "Mercury + Venus in one sign with cruel planets (No Rain)",
            "Venus + Saturn in one sign (Scanty Rain)",
            "Mars ahead of Sun (Monsoon delayed or deficient)",
            "Moon in Moon-owned star and Sun in Sun-owned star (strict no-rain veto)",
        ],
    },
    rain_table_temporal_correlation = {
        "logic":   "Winter rain dates (Dec–Apr) mirror summer monsoon dates (Jul–Nov).",
        "example": "Rain in Ludhiana on Dec 7 (Winter) predicts Rain on Jun 30 (Summer).",
        "rohini_hurdle_delay": (
            "If rain occurs on May 25 (Sun in Rohini), add 72-day delay before next "
            "major rainfall event is predicted."
        ),
    },
    nadi_lord_synergy = {
        "logic":   "A planet is highly benefic when it resides in the Nadi it rules.",
        "example": "Moon (Lord of Amrita) in Amrita Nadi = primary rain trigger.",
    },
    localization_protocol = {
        "axiom":  "Rainfall varies by location; generic transit results must be localized.",
        "method": [
            "1. Identify active constellations for the specific place or province.",
            "2. Cross-reference those constellations with the Saptnadi Chart.",
            "3. Apply Vedha rules to the localized constellation set.",
        ],
    },
)

# ═════════════════════════════════════════════════════════════════════════════
# SPEC 6 — Gaur Ch 7: Sasya Jatak Crop Engine
# ═════════════════════════════════════════════════════════════════════════════
GAUR_CH7_CROP_ENGINE = _spec(
    spec_id   = "gaur-ch7-sasya-jatak-crop-engine",
    spec_type = "agricultural_lookup",
    title     = "Sasya Jatak Crop Engine — 10 Yield Yogas + Inverse Pricing Rule",
    source    = "gaur_aifas_ch7",
    description = (
        "Attributed to Maharshi Vadnarayan. Treats seasonal crops as 'living entities' "
        "with a birth chart cast at the solar ingress for each season. "
        "Ten planetary yogas determine yield (high/low) and the Inverse Pricing Rule "
        "automatically translates yield into market price direction. "
        "Two seasonal types: Winter (Rabi) and Summer (Kharif)."
    ),
    framework = {
        "system_name": "Sasya Jatak",
        "origin":      "Maharshi Vadnarayan",
        "purpose":     "Predicting yield, quality, and price of seasonal crops",
    },
    seasonal_horoscope_types = {
        "winter_crop_rabi": {
            "timing_logic":  "Cast based on solar ingress for the winter season (Scorpio/Taurus ingress).",
            "primary_crops": ["Wheat", "Barley", "Gram", "Lentils"],
        },
        "summer_crop_kharif": {
            "timing_logic":  "Cast based on solar ingress for the summer/monsoon season.",
            "primary_crops": ["Rice", "Millets", "Cotton", "Sugarcane"],
        },
    },
    yield_price_inverse_rule = {
        "axiom":             "In all combinations: when produce is good prices are low; when output is low prices are high.",
        "condition_high_yield": (
            "IF (Benefics occupy Kendras 1/4/7/10 OR Trikonas 5/9) "
            "THEN Produce = High AND Market_Price = Low."
        ),
        "condition_low_yield": (
            "IF (Malefics afflict 4th/8th house OR Lord of Crops) "
            "THEN Produce = Low AND Market_Price = High."
        ),
        "market_price_flip": (
            "A 'Good' harvest result must trigger Bearish Trend for that commodity in the trade module."
        ),
        "cross_reference":   "Apply to both Summer (Scorpio Ingress) and Winter (Taurus Ingress) charts.",
    },
    crop_yield_yogas_10 = {
        "yoga_i_quadrant_benefics": {
            "condition": "IF (Benefics in quadrants 1-4-7-10 from transiting Sun) OR (Sun aspected by strong benefics)",
            "result":    "Produce = High; Grains = Cheap.",
        },
        "yoga_ii_jupiter_moon_axis": {
            "condition": "IF (Jupiter in Aquarius AND Moon in Leo) OR (Jupiter in Leo AND Moon in Aquarius)",
            "result":    "Produce = High; Grains = Cheap.",
        },
        "yoga_iii_benefic_flanking": {
            "condition": "IF (Mercury OR Venus in 2nd or 12th from Sun)",
            "modifier":  "IF (Sun also aspected by Jupiter) THEN Produce = 'Excellent'.",
            "result":    "Produce = Sufficient; Grains = Stable.",
        },
        "yoga_iv_seventh_house_strength": {
            "condition": "IF (Jupiter AND Moon in 7th from Sun) AND (Benefics between Mercury and Venus)",
            "result":    "Produce = Good.",
        },
        "yoga_v_eleventh_house_gains": {
            "condition": "IF (Venus OR Moon in 11th from Sun) AND (Mercury in 2nd from Sun)",
            "modifier":  "IF (Jupiter in 10th) THEN Produce = 'Excellent' AND Dairy = 'Abundant'.",
            "result":    "Produce = Good.",
        },
        "yoga_vi_sat_mar_capricorn_veto": {
            "condition": "IF (Jupiter in Aquarius, Moon in Taurus, Saturn AND Mars in Capricorn)",
            "result":    "Produce = Good BUT Status = 'National Conspiracy and Disease Alert'.",
        },
        "yoga_vii_malefic_interference": {
            "condition": "IF (Sun between Mars AND Saturn) OR (Mars AND Saturn in 7th from Sun)",
            "result":    "Produce = Destroyed/Poor; Grains = Expensive.",
        },
        "yoga_viii_sprouting_failure": {
            "condition": "IF (Malefic in 2nd from Sun) AND (Sun lacks benefic aspect)",
            "result":    "CRITICAL: Crop destroyed soon after sprouting; reseeding required.",
        },
        "yoga_ix_aspected_destruction": {
            "condition": "IF (Saturn OR Mars in 7th from Sun) AND (Other malefic in 1st/4th/10th)",
            "modifier":  "IF (Benefics aspect malefics) THEN Partial Destruction ELSE Total Failure.",
            "result":    "Crop Failure Alert.",
        },
        "yoga_x_malefic_split_logic": {
            "condition": "IF (One malefic in 7th AND another in 6th from Sun)",
            "result":    "Produce = Good; Cost = Low.",
        },
    },
    planetary_influence_modifiers = {
        "jupiter_influence": "Ensures high quality and abundance of grains.",
        "mars_influence":    "Indicates damage via fire, heat, or pestilence.",
        "saturn_influence":  "Indicates drought-related failure or stunted growth.",
    },
    logic_gates = {
        "sowing_veto":       "IF 4th house aspected by benefic THEN Yield_Weight += 0.3.",
        "malefic_ingress_alert": (
            "IF solar ingress shows Mars or Saturn in 7th house THEN flag "
            "'Crop Destruction Warning: high risk to ripe crops near harvest time'."
        ),
        "reseeding_alert":   "IF Yoga_VIII THEN Agricultural Crisis: initial sowing will fail.",
        "conspiracy_modifier": (
            "IF Yoga_VI THEN Complex Harvest: high yields overshadowed by national "
            "health issues and political plots."
        ),
    },
)

# ═════════════════════════════════════════════════════════════════════════════
# SPEC 7 — Gaur Ch 8: Material & Commodity Database
# ═════════════════════════════════════════════════════════════════════════════
GAUR_CH8_MATERIAL_DATABASE = _spec(
    spec_id   = "gaur-ch8-material-commodity-database",
    spec_type = "lookup_table",
    title     = "Material & Commodity Database — Planetary, Zodiac, Nakshatra Ownership",
    source    = "gaur_aifas_ch8",
    description = (
        "Exhaustive 'Material Lookup Table' mapping the world's commodities to three "
        "overlapping hierarchies: Planetary Ownership (9 planets), Zodiac Signification "
        "(12 signs with full row data), and Constellation Governance (28 nakshatras "
        "including Abhijit). The Nomenclature Rule classifies any unlisted material "
        "by phonetic first letter. Planetary dignity modifiers drive the price vector."
    ),
    planetary_governance = {
        "sun":      ["Gold", "Copper", "Grains", "Wheat", "Mustard", "Perfumery", "Silk", "Leather"],
        "moon":     ["Silver", "Rice", "Barley", "Sugarcane", "Pearl", "Honey", "Salt"],
        "mars":     ["Copper", "Gur", "Coral", "Red fruits", "Arms/Ammunition"],
        "mercury":  ["Green vegetables", "Lentils (Moong/Arhar)", "Peas", "Peanuts", "Perfumery"],
        "jupiter":  ["Turmeric", "Gold", "Topaz", "Cotton cloth", "Rock salt", "Creepers"],
        "venus":    ["Silver", "Silk", "Ghee", "Hosiery", "Sugar", "Luxury goods"],
        "saturn":   ["Steel", "Iron", "Machinery", "Chemicals", "Sesame (Til)", "Leather", "Foreign Capital"],
        "rahu_ketu": ["Agate", "Goat", "Donkey", "Camel", "Onion", "Garlic"],
    },
    zodiac_sign_material_rows = {
        "1_aries":       "Red wheat, barley, red sandal, cloth, silk, woolen clothes, pashmina, turmeric, gums, gold, silver, herbs, masoor",
        "2_taurus":      "Ghee, milk, cotton thread, cotton clothes, white things, sugar, salt, aniseed",
        "3_gemini":      "Millet, maize, cotton seed, yarn, jute, cotton, rice",
        "4_cancer":      "Silver, grocery, banana, grass, cinnamon, onion, orange, lemon, tea, spices",
        "5_leo":         "Gram, grains covered by straw, gur, juicy materials, leather",
        "6_virgo":       "Millet, arhar, peas, moong, moth, wheat, green clothes, khand, sugar, linseed, rajma",
        "7_libra":       "Urad (horse bean), wheat, barley, coconut, arhar, mustard, peas",
        "8_scorpio":     "Gur, khand, sweets, perfumery, til (sesame), black things",
        "9_sagittarius": "Juicy materials, potato, alkaline materials, white grains, roots, sea-products, salt",
        "10_capricorn":  "Iron, coal, steel, glass, trees",
        "11_aquarius":   "Water products, electric/electronic goods, oils",
        "12_pisces":     "Fish, war materials, ghee, oils",
    },
    nakshatra_material_28_rows = {
        "1_ashwini":          "Rice, edible powder (churna), grains, clothes, ghee, camel, pony",
        "2_bharani":          "Husky grains, millet, chillies, all herbs",
        "3_krithika":         "Rice, barley, metals, til (sesame), ruby, diamond",
        "4_rohini":           "All grains, all juices, all metals, woolen clothes, old blankets",
        "5_mrigshira":        "Horses, buffalo, cows, lac, koda, grains, donkey, tuar, gems",
        "6_ardra":            "Salt, oil, all alkalies, all juices, aromatic things like sandal",
        "7_punarvasu":        "Gold, silver, cotton, millet, kushumbh, black silken cloth",
        "8_pushya":           "Gold, silver, ghee, rice, rock salt, asafoetida, oil, mustard, vegetables",
        "9_ashlesha":         "Majeeth, gur, sugar, wheat, dry ginger, chillies, koda, grains, rice",
        "10_magha":           "Til (sesame), oil, ghee, coral, gram, linseed, gur",
        "11_poorvaphalguni":  "Wool, blanket, millet, oil, silver items",
        "12_uttaraphalguni":  "Urad, moong, rice, koda, rock salt, garlic, vegetables",
        "13_hast":            "Sandal, camphor, pine, aloes, red sandal, roots",
        "14_chitra":          "Gold, gems, moong, urad, rice, gur, horse, vehicle",
        "15_swati":           "Betelnut, chillies, mustard oil, asafoetida, dates",
        "16_vishakha":        "Barley, wheat, rice, moong, masoor, moth, grains",
        "17_anuradha":        "Tuar, all grains except pulses, rice, moth, gram",
        "18_jyeshtha":        "Guggul, gur, lac, camphor, mercury, asafoetida, kalsi",
        "19_mool":            "White things, juices, grains, rock salt, salts, cotton",
        "20_poorvashadh":     "Surma, husk, grains, ghee, roots (kandmool), joorna, rice",
        "21_uttarashadh":     "Horse, ox, elephant, iron goods, all alkalies, ghee",
        "22_abhijit":         "Grapes, dates, betelnuts, cardamom, moong, nutmeg, horse",
        "23_shravan":         "Chestnut, chironji, pippala, betelnut, husk, grains",
        "24_dhanishtha":      "Gold, silver, all currencies, ruby, pearl",
        "25_shatbhisha":      "Oils, liquor, roots, bark, extracts (aonla)",
        "26_poorvabhadrapad": "All metals, herbs, all grains, pine, priyongu roots",
        "27_uttarabhadrapad": "Gur, sugar, til, mustard, oilcake, rice, ruby, pearl",
        "28_revti":           "Coconut, betelnut, all grocery, ruby, pearl",
    },
    nomenclature_rule = {
        "axiom":       "The zodiac sign of any material is determined by the phonetic first letter of its name.",
        "application": "Enables classification of modern materials (e.g., Titanium → Taurus logic).",
    },
    dignity_modifier = {
        "retrograde_or_exalted": "Significator Retrograde OR Exalted → Stock Accumulation probability high.",
        "combust":               "Significator Combust → Scarcity Alert.",
        "price_volatility":      "Debilitated OR Combust significator → Price_Volatility_Weight += 0.4.",
    },
    dual_mapping_filter = (
        "For materials listed in BOTH zodiac AND nakshatra tables (e.g., Gold): "
        "cross-reference both. Conflict (Sign=Bullish, Nakshatra=Bearish) → "
        "'Market Volatility: Choppy Trading' diagnostic."
    ),
    saturn_factory_veto = (
        "For industrial queries, prioritize Saturn. "
        "IF Saturn Retrograde THEN trigger 'Production Slowdown Alert' for steel mills and big factories."
    ),
)

# ═════════════════════════════════════════════════════════════════════════════
# SPEC 8 — Gaur Ch 9: Sarvatobhadra Trade Engine
# ═════════════════════════════════════════════════════════════════════════════
GAUR_CH9_SARVATOBHADRA_ENGINE = _spec(
    spec_id   = "gaur-ch9-sarvatobhadra-trade-engine",
    spec_type = "trade_grid",
    title     = "Sarvatobhadra Trade Engine — Vedha Motion Logic + 28-Row Commodity Matrix",
    source    = "gaur_aifas_ch9",
    description = (
        "Derived from Maharshi Narapati's Jaycharya. Uses Vedha (Obstruction) where "
        "planets exert influence in three directions (Front/Left/Right) depending on "
        "their motion state. Benefic Vedha lowers prices; Malefic Vedha raises them. "
        "Full 28-row constellation-commodity impact matrix included."
    ),
    core_system = {
        "name":            "Sarvatobhadra Chakra",
        "author":          "Maharshi Narapati (Jaycharya)",
        "logic_mechanism": "Vedha (Obstruction)",
        "aspect_types":    ["Front", "Right", "Left"],
    },
    planetary_motion_logic = {
        "retrograde_motion":           "Obstructs Right side constellations, signs, and letters.",
        "accelerated_motion_atichari": "Obstructs Left side constellations, signs, and letters.",
        "medium_motion_normal":        "Obstructs only the constellation in Front.",
        "fixed_motion_rules": {
            "sun_moon":  "Always Accelerated; aspect all three sides (Left, Right, Front).",
            "rahu_ketu": "Always Retrograde; aspect all three sides (Left, Right, Front).",
        },
    },
    economic_logic_gates = {
        "benefic_vedha_impact": {
            "planets": ["Moon", "Mercury", "Jupiter", "Venus"],
            "result":  "Market Prices = Bearish/Decrease",
        },
        "malefic_vedha_impact": {
            "planets": ["Sun", "Mars", "Saturn", "Rahu", "Ketu"],
            "result":  "Market Prices = Bullish/Increase",
        },
        "mercury_modifier": "Mercury's result is dictated by its conjunction: Benefic = Good, Malefic = Inauspicious.",
    },
    constellation_vedha_impact_28_rows = {
        "1_ashwini":          {"obstruction": "Jyeshtha, Sagittarius",        "bullish_malefic": "Rice, all grains, grasses, ghee, transport animals",                    "bearish_benefic": "Price drop in all Ashwini materials"},
        "2_bharani":          {"obstruction": "Anuradha, Aries, Scorpio",     "bullish_malefic": "Wheat, rice, barley, gram, spices (cumin, pepper)",                    "bearish_benefic": "Spices and grains become cheap"},
        "3_krithika":         {"obstruction": "Vishakha, Taurus, Libra",      "bullish_malefic": "Oils, grains, precious gems (ruby, diamond), gold, silver",            "bearish_benefic": "Metals and gems become cheap"},
        "4_rohini":           {"obstruction": "Ashwini, Cancer, Leo",         "bullish_malefic": "All grains, all metals, juices, blankets, woolen clothes",             "bearish_benefic": "Grains and woolens become cheap"},
        "5_mrigshira":        {"obstruction": "Revti, Cancer, Leo",           "bullish_malefic": "Koda, tuar (lentils), liquids, cattle, lac, ruby",                     "bearish_benefic": "Lentils and liquids become cheap"},
        "6_ardra":            {"obstruction": "Uttarabhadrapad",              "bullish_malefic": "Oils, salt, all salty things, juicy materials, sandal",                 "bearish_benefic": "Oils and salt become cheap"},
        "7_punarvasu":        {"obstruction": "Poorvabhadrapad, Aries, Taurus", "bullish_malefic": "Millet, cotton, jute, black silken clothes, gold, silver",           "bearish_benefic": "Textiles and metals become cheap"},
        "8_pushya":           {"obstruction": "Shatbhisha, Gemini, Pisces",   "bullish_malefic": "Gold, silver, rice, ghee, rock salt, asafoetida, mustard oil",         "bearish_benefic": "Ghee and mustard oil prices drop"},
        "9_ashlesha":         {"obstruction": "Dhanishtha, Cancer, Aquarius", "bullish_malefic": "Wheat, rice, masoor, dry ginger, sugar, chillies",                     "bearish_benefic": "Ginger and sugar become cheap"},
        "10_magha":           {"obstruction": "Ashlesha, Shravan, Leo, Capricorn", "bullish_malefic": "Oils, sesame, ghee, moong, gram, gur, coral",                    "bearish_benefic": "Pulses and ghee become cheap"},
        "11_poorvaphalguni":  {"obstruction": "Pushya, Abhijit, Virgo, Sagittarius", "bullish_malefic": "Clothes, wool, blankets, millet, til, silver items",            "bearish_benefic": "Wool and silver become cheap"},
        "12_uttaraphalguni":  {"obstruction": "Punarvasu, Uttarashadh, Libra, Scorpio", "bullish_malefic": "Pulses (urad, moong), rice, rock salt, garlic, vegetables",  "bearish_benefic": "Pulses and vegetables become cheap"},
        "13_hast":            {"obstruction": "Ardra, Poorvashadh",           "bullish_malefic": "Camphor, sandal, pine, beet roots, aloe wood (agar)",                  "bearish_benefic": "Sandal and aromatic woods become cheap"},
        "14_chitra":          {"obstruction": "Mrigshira, Mool, Cancer, Leo", "bullish_malefic": "Gold, silver, grains, yarn, red clothes, gur, sugar",                 "bearish_benefic": "Metals and yarn become cheap"},
        "15_swati":           {"obstruction": "Rohini, Gemini, Virgo",        "bullish_malefic": "Betelnut, chillies, mustard oil, cotton, asafoetida, dates",           "bearish_benefic": "Grocery and dates become cheap"},
        "16_vishakha":        {"obstruction": "Krithika, Taurus, Libra",      "bullish_malefic": "Wheat, rice, barley, moong, masoor, cotton",                           "bearish_benefic": "Wheat and cotton become cheap"},
        "17_anuradha":        {"obstruction": "Vishakha, Bharani, Aries, Scorpio", "bullish_malefic": "All pulses (tuar, moth, gram), rice",                             "bearish_benefic": "Rice and grains become cheap"},
        "18_jyeshtha":        {"obstruction": "Swati, Ashwini, Sagittarius, Pisces", "bullish_malefic": "Gur, lac, camphor, mercury, asafoetida, bell metal",            "bearish_benefic": "Mercury and bell metal become cheap"},
        "19_mool":            {"obstruction": "Chitra, Revti, Capricorn, Aquarius", "bullish_malefic": "All white things, juices, grains, rock salt, cotton thread",     "bearish_benefic": "White goods and thread become cheap"},
        "20_poorvashadh":     {"obstruction": "Hast, Uttarabhadrapad",        "bullish_malefic": "Surma (collyrium), husky grains, root vegetables, fruits, rice",       "bearish_benefic": "Root vegetables and fruits become cheap"},
        "21_uttarashadh":     {"obstruction": "Uttaraphalguni, Uttarabhadrapad, Scorpio", "bullish_malefic": "Ghee, horses, ox, iron, all vehicles",                     "bearish_benefic": "Vehicles and ghee become cheap"},
        "22_abhijit":         {"obstruction": "Poorvaphalguni, Shatbhisha, Virgo, Sagittarius", "bullish_malefic": "Grapes, dates, cardamom, nutmeg, betelnut, moong",   "bearish_benefic": "Dry fruits and moong become cheap"},
        "23_shravan":         {"obstruction": "Magha, Dhanishtha, Leo, Capricorn", "bullish_malefic": "Chestnut, chironji, pippali, betelnut, grains",                   "bearish_benefic": "Grains and chestnuts become cheap"},
        "24_dhanishtha":      {"obstruction": "Shravan, Ashlesha, Cancer, Aquarius", "bullish_malefic": "Gold, silver, all currencies, ruby, pearl",                     "bearish_benefic": "Currencies and metals depreciate"},
        "25_shatbhisha":      {"obstruction": "Abhijit, Pushya, Gemini, Pisces", "bullish_malefic": "Oils, liquor, roots, bark, extracts (aonla)",                       "bearish_benefic": "Oils and bark products become cheap"},
        "26_poorvabhadrapad": {"obstruction": "Uttarashadh, Punarvasu, Aries, Taurus", "bullish_malefic": "All metals, herbs, all grains, pine, priyongu roots",         "bearish_benefic": "Metals and grains become cheap"},
        "27_uttarabhadrapad": {"obstruction": "Poorvashadh, Ardra",           "bullish_malefic": "Gur, sugar, til, mustard, oilcake, rice, ruby, pearl",                 "bearish_benefic": "Sugar and rice become cheap"},
        "28_revti":           {"obstruction": "Mool, Mrigshira, Capricorn, Aquarius", "bullish_malefic": "Coconut, betelnut, all grocery, ruby, pearl",                  "bearish_benefic": "Grocery and coconut become cheap"},
    },
    logic_gates = {
        "luminaries_triple_vedha": (
            "Sun and Moon always Accelerated → Vedha applies to all three sides regardless of speed."
        ),
        "rahu_ketu_veto": (
            "Nodes always Retrograde → Vedha applies to all three sides → escalates market volatility."
        ),
        "letter_sign_cross_reference": (
            "If city's first letter matches obstructed letter → "
            "'Local Alert: Market stress/incident predicted for this region'."
        ),
        "motion_shift_alert": (
            "If planet changes to Retrograde or Accelerated → "
            "'Motion Shift Alert: Obstruction points revised due to planetary retrogression'."
        ),
        "market_sentiment_rule": (
            "IF Benefic_Vedha_Count > Malefic_Vedha_Count THEN "
            "Status = 'Market Sentiment: Bearish; prices likely to soften'."
        ),
    },
)

# ═════════════════════════════════════════════════════════════════════════════
# Master list
# ═════════════════════════════════════════════════════════════════════════════
SPECS = [
    GAUR_CH5_ARDRA_MONSOON_ENGINE,
    GAUR_CH5_ROHINI_SAMUDRA_CHAKRA,
    GAUR_CH6_TRINADI_WEATHER_ENGINE,
    GAUR_CH6_CONSTELLATION_GENDER_ENGINE,
    GAUR_CH6_SAPTNADI_ENGINE,
    GAUR_CH7_CROP_ENGINE,
    GAUR_CH8_MATERIAL_DATABASE,
    GAUR_CH9_SARVATOBHADRA_ENGINE,
]

# ═════════════════════════════════════════════════════════════════════════════
# Runner
# ═════════════════════════════════════════════════════════════════════════════
async def run():
    if DRY_RUN:
        print(f"[DRY RUN] Would upsert {len(SPECS)} specs into mundane_engine_specs.")
        for s in SPECS:
            print(f"  would upsert: {s['spec_id']}")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    db     = client[DB_NAME]
    coll   = db["mundane_engine_specs"]
    ok = 0
    for s in SPECS:
        await coll.update_one(
            {"spec_id": s["spec_id"]},
            {"$set": s},
            upsert=True,
        )
        ok += 1
    client.close()
    print(f"Upserted {ok} specs into mundane_engine_specs.")

if __name__ == "__main__":
    asyncio.run(run())
