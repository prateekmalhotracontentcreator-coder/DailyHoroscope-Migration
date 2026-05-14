"""
Mundane Astrology — Engine Specs INGEST v3
Batch: mundane-engine-v3-20260506
Collection: mundane_engine_specs
Science: mundane_jyotish

New specs from direct PDF source reads:
  - Gaur Ch 2: 10-official Celestial Council planet-outcome matrix
  - Gaur Ch 2: 9 Clouds formula + results
  - Gaur Ch 2: 12 Snakes formula + results
  - Gaur Ch 8: Planet commodity ownership (7 planets + Rahu/Ketu)
  - Gaur Ch 8: Sign commodity ownership (12 signs)
  - Gaur Ch 8: Nakshatra commodity ownership (27+1 nakshatras)
  - Mehta Ch 7: Koorma geographic mapping (9 zones → modern states/countries)
  - Mehta Ch 7: Planet → direction + country rulership
  - Mehta Ch 7: Nakshatra-affliction → country/region affected (Brihat Samhita)
  - Mehta Ch 22: Planetary Cabinet domain lords — determination + per-planet outcomes

DRY_RUN = True  →  set False to write to MongoDB.
"""

import asyncio
from datetime import datetime, timezone

DRY_RUN = True

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 1 — Gaur Ch 2: Celestial Council — 10 Officials × 7 Planet Outcomes
# ─────────────────────────────────────────────────────────────────────────────
GAUR_CH2_CELESTIAL_COUNCIL_OUTCOMES = {
    "spec_id": "gaur-ch2-celestial-council-outcomes",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": "mundane-engine-v3-20260506",
    "title": "Celestial Council — 10 Officials × 7 Planet Outcome Matrix",
    "source": "gaur_aifas_ch2",
    "description": (
        "For each Vikram Samvat year the Celestial Council comprises 10 officials, each "
        "appointed by the planetary lord of a specific solar ingress day. The outcome of "
        "the year in that official's domain depends on which planet holds the post."
    ),
    "officials": {
        "I_King": {
            "sanskrit_name": "Raja / Samvatsar King",
            "appointment": "Lord of the day (weekday ruler) falling on Chaitra Shukla Pratipada — first day of Vikram Samvat",
            "domain": "Governance, war/peace, overall prosperity of the year",
            "planet_outcomes": {
                "Sun": (
                    "Rains insufficient. Danger of diseases to people and cattle. "
                    "Produce of fruits and grains comparatively poor. Danger of theft. "
                    "Loss of lives and wealth due to fires. A senior ruler or leader dies."
                ),
                "Moon": (
                    "More celebrations and auspicious ceremonies. Rains and crops good. "
                    "Harmony and goodwill in masses. Prestige of rulers increased. "
                    "Effective measures taken for better health, elimination of disease and "
                    "for peace amongst the people."
                ),
                "Mars": (
                    "Many events of loss of lives and wealth due to fires. People suffer due "
                    "to thieves and robbers. Fear prevails in atmosphere due to wars triggered "
                    "by rulers. Rains insufficient at many places."
                ),
                "Mercury": (
                    "Rains excessive. Danger of loss due to floods. Many celebrations like "
                    "marriages. Comforts and wealth of people increased. Rulers and people "
                    "enjoy and live happily. Number of cows increases."
                ),
                "Jupiter": (
                    "Rains sufficient and timely. Nourishing materials like milk abundant. "
                    "Many religious rituals and all people take part in celebrations."
                ),
                "Venus": (
                    "Rains sufficient, production of grains high. Produce of fruits and "
                    "flowers good. Wealth and prosperity of rulers augmented. People devote "
                    "more time for entertainment. Powers of ladies increase."
                ),
                "Saturn": (
                    "Rains less. People suffer due to various diseases. Differences of "
                    "politicians get intensified. Rulers create atmosphere of wars. Turmoils "
                    "due to disease, thieves and riots. At few places people have to leave "
                    "their home due to drought."
                )
            }
        },
        "II_Minister": {
            "sanskrit_name": "Mantri",
            "appointment": "Lord of the day falling on Aries ingress (Mesha Sankranti)",
            "domain": "Administration, law and order, ministerial conduct",
            "planet_outcomes": {
                "Sun": (
                    "Bitterness amongst rulers increased. Fear due to disease and theft. "
                    "Prosperity and food supply increased. Juicy materials such as gur expensive."
                ),
                "Moon": (
                    "Rains sufficient, crops and grains excellent. Development projects "
                    "completed. Prosperity and celebrations prevail."
                ),
                "Mars": (
                    "Immoral acts like theft and robbery increase. People suffer due to "
                    "diseases. Scarcity of milk. Learned scholars remain disturbed due to "
                    "wrong deeds."
                ),
                "Mercury": (
                    "Living conditions of people improved. Harmony and love in families. "
                    "Wealth and grains increased. Rains good. Barley, gram, lentils expensive."
                ),
                "Jupiter": (
                    "All crops excellent. Rains good. Joys and prosperity prevail. "
                    "Rulers remain busy in welfare activities."
                ),
                "Venus": (
                    "Crops damaged by locusts and rats. All grains expensive. Rains excessive "
                    "and danger of floods. Supremacy of females established. More wind and "
                    "sex-related diseases."
                ),
                "Saturn": (
                    "Cruel behaviours of rulers and administrators cause sufferings and "
                    "dissatisfaction amongst people."
                )
            }
        },
        "III_Sasyesh": {
            "sanskrit_name": "Sasyesh",
            "appointment": "Lord of the day falling on Cancer ingress (Karka Sankranti)",
            "domain": "Summer / 4-month crops (barley, wheat, rice, sugarcane)",
            "note": "Sasyesh Horoscope = horoscope cast for the moment of Sun's entry into Cancer",
            "planet_outcomes": {
                "Sun": (
                    "Grains of summer expensive. Increase in incidents of theft and robberies. "
                    "Wars among rulers. Cattle fodder in short supply despite good rains. "
                    "Milk available in sufficient quantity."
                ),
                "Moon": (
                    "Comforts of people increase. Rains sufficient. Milk available in "
                    "sufficient quantities. Rulers and upper class worship gods and honour "
                    "scholars. Wealth and grains abundant."
                ),
                "Mars": (
                    "Crops of summer grains barley and wheat damaged. Rains excessive at few "
                    "places and scanty at other locations. Many diseases in animals such as "
                    "elephants, horses, cows and ox."
                ),
                "Mercury": (
                    "Crops of grains, wheat, rice, sugarcane good. Rains sufficient. "
                    "Development projects and amenities excellent. Brahmins and scholars "
                    "inclined towards religious deeds."
                ),
                "Jupiter": (
                    "Crops of summer good. Juicy materials, milk and ghee freely available. "
                    "Rains good. Feeling of duty and love in minds of people."
                ),
                "Venus": (
                    "Rains timely and sufficient. Wheat, rice, sugarcane sufficient. "
                    "Flowers and fruits grow abundantly. Atmosphere full of joys."
                ),
                "Saturn": (
                    "Loss of ripe crops such as wheat, rice, barley. Goods expensive. "
                    "Behaviour of rulers rude. Masses remain entangled in useless disputes."
                )
            }
        },
        "IV_Dhanyesh": {
            "sanskrit_name": "Dhanyesh",
            "appointment": "Lord of the day falling on Sagittarius ingress (Dhanu Sankranti)",
            "domain": "Winter crops (Moong, Moth/lentil, Millet, Mustard, Wheat)",
            "note": "Dhanyesh Horoscope = horoscope cast for Sun's entry into Sagittarius",
            "planet_outcomes": {
                "Sun": (
                    "Winter crops Moong, Moth (lentil), Millet destroyed. Goods expensive. "
                    "Rulers inclined towards fighting and wars. Diseases such as fever cause "
                    "suffering. Grains costly."
                ),
                "Moon": (
                    "Winter crops Moong, Moth (lentils), Millet, Mustard good. Milk freely "
                    "available and population increases."
                ),
                "Mars": (
                    "Grains of summer season Millet, Moong, Moth, Rice and Maize available "
                    "in sufficient quantities. Sugarcane, ghee and oils expensive. People "
                    "suffer due to fires."
                ),
                "Mercury": (
                    "Winter crops good. Rains sufficient except in Sindh and Punjab."
                ),
                "Jupiter": (
                    "Crops of Barley, Wheat, Rice good. All religious persons remain busy "
                    "in religious acts."
                ),
                "Venus": (
                    "Produce of winter crops Moong, Moth, Millet not good. Wheat, cattle "
                    "fodder and vegetables costly. Rains less and milk insufficient."
                ),
                "Saturn": (
                    "Produce less. Crops of grains, Moong, Moth and Millet suffer due to "
                    "diseases. National treasure reduced. Wars at few places. Rains not "
                    "sufficient and timely. Farmers remain worried."
                )
            }
        },
        "V_Meghesh": {
            "sanskrit_name": "Meghesh",
            "appointment": "Lord of the day when Sun enters Ardra constellation (nakshatra)",
            "domain": "Weather, rainfall, monsoon quality",
            "note": "Meghesh Horoscope = horoscope cast for the moment of Sun's entry into Ardra nakshatra",
            "planet_outcomes": {
                "Sun": (
                    "Rains less, prices high, politicians have differences. Danger of thefts "
                    "and robberies. Crops of gram, barley, sugarcane and rice good."
                ),
                "Moon": (
                    "Rains in sufficient quantities. Crops of grains and flowers/fruits "
                    "excellent. Production of milk and ghee good. Rulers live in harmony "
                    "with other rulers. Amenities of people improved."
                ),
                "Mars": (
                    "All persons forget the path of religious faith. Rains good at some "
                    "places and insufficient at other locations. People suffer and remain gloomy."
                ),
                "Mercury": (
                    "Rains more. Crops of wheat, barley and other grains good. All religious "
                    "persons like brahmins remain busy in noble activities. Improvements in "
                    "all comforts."
                ),
                "Jupiter": (
                    "Rains excellent and timely. Crops of juicy materials good. People live "
                    "comfortably and rulers follow the path of religion."
                ),
                "Venus": (
                    "Rains good. All religious persons live comfortably. People satisfied by "
                    "conduct of rulers."
                ),
                "Saturn": (
                    "Rains insufficient at few parts of earth. Rulers remain disenchanted. "
                    "Fear of diseases in the masses."
                )
            }
        },
        "VI_Rasesh": {
            "sanskrit_name": "Rasesh",
            "appointment": "Lord of the day falling on Libra ingress (Tula Sankranti)",
            "domain": "Juicy materials — Gur (jaggery), Sugar, Sweet substances, Juices",
            "note": "Rasesh Horoscope = horoscope cast for Sun's entry into Libra",
            "planet_outcomes": {
                "Sun": (
                    "Rains insufficient. Production of juicy materials like Gur less. Shortage "
                    "of milk, ghee, oils and clothes. Rulers remain worried due to many problems."
                ),
                "Moon": (
                    "Rains sufficient. Gur-Khand (Sugar) produced adequately. Wealth and "
                    "grains increased. Young persons remain busy in new methods of entertainment."
                ),
                "Mars": (
                    "Rains insufficient. Juicy materials like Gur and Sugar in short supply. "
                    "Goods expensive. People dissatisfied by conduct of rulers."
                ),
                "Mercury": (
                    "Rains sufficient and timely. All juicy materials and grains available "
                    "abundantly. Milk and ghee adequate. Rulers run administration well. "
                    "Security of country maintained."
                ),
                "Jupiter": (
                    "People live with luxuries and comforts. Crops of juicy materials like "
                    "lotus good. Learned scholars honoured by citizens. Rulers have many "
                    "vehicles and cattle."
                ),
                "Venus": (
                    "Many celebrations and religious rituals. Rains less in many provinces. "
                    "Production of juicy materials such as Gur and Sugar good. People live "
                    "comfortably. Rulers run administration efficiently."
                ),
                "Saturn": (
                    "Rains scanty. Crops of juicy materials suffer. Cattle too catch diseases."
                )
            }
        },
        "VII_Neersesh": {
            "sanskrit_name": "Neersesh",
            "appointment": "Lord of the day falling on Capricorn ingress (Makara Sankranti)",
            "domain": "Metals, trade, commerce",
            "note": "Neersesh Horoscope = horoscope cast for Sun's entry into Capricorn",
            "planet_outcomes": {
                "Sun": "Gold, copper, silver, ruby, pearl become expensive.",
                "Moon": "White things, silver, pearl and clothes become expensive.",
                "Mars": "Gold, brass, copper, red sandal, gems such as coral and red colored things become expensive.",
                "Mercury": "Readymade clothes, hosiery materials, conch shell (Shankh), sandal, metals and gems become expensive.",
                "Jupiter": "Gold, yellow clothes, turmeric and other yellow materials become expensive.",
                "Venus": "Gold, pearl, diamond and gems, readymade clothes, perfumery and cosmetics become costly.",
                "Saturn": "Hardware materials, iron, machinery, black clothes and black materials become expensive."
            }
        },
        "VIII_Phalesh": {
            "sanskrit_name": "Phalesh",
            "appointment": "Lord of the day falling on Pisces ingress (Meena Sankranti)",
            "domain": "Fruits, flowers, horticulture",
            "note": "Phalesh Horoscope = horoscope cast for Sun's entry into Pisces",
            "planet_outcomes": {
                "Sun": (
                    "Earth lush and decorated with fruits and flowers of all types. "
                    "Rains also sufficient."
                ),
                "Moon": (
                    "Crops good. Fruits and flowers produced in sufficient amounts. "
                    "Scholars inclined towards entertainment. Rulers efficient."
                ),
                "Mars": (
                    "Production of flowers and fruits poor. Diseases cause sufferings. "
                    "Tension among rulers."
                ),
                "Mercury": (
                    "Production of fruits very good. Rains sufficient. Grass and flowers "
                    "also adequate. People live with comforts and happiness."
                ),
                "Jupiter": (
                    "Production of fruits and plants good. All people remain busy in "
                    "religious rituals."
                ),
                "Venus": (
                    "Crops of grass, vegetables, fruits and flowers good. Administrators get "
                    "delicious food products. Religious persons devote more time in noble activities."
                ),
                "Saturn": (
                    "Crops of fruits damaged. Flowers of trees do not develop. Losses in "
                    "winter due to snowfall. Incidents of theft more and people suffer due "
                    "to diseases."
                )
            }
        },
        "IX_Dhanesh": {
            "sanskrit_name": "Dhanesh",
            "appointment": "Lord of the day falling on Virgo ingress (Kanya Sankranti)",
            "domain": "Wealth, treasure, trade profits",
            "note": "Dhanesh Horoscope = horoscope cast for Sun's entry into Virgo",
            "planet_outcomes": {
                "Sun": (
                    "Businessmen earn good profits in trade. Traders of cows, buffalos, "
                    "horses earn very well."
                ),
                "Moon": (
                    "Wealth accumulated by buying and selling. More profits in trade. "
                    "Traders of clothes, rice, ghee, oils, juices and perfumes earn well "
                    "particularly. Rulers equipped with means of comforts."
                ),
                "Mars": (
                    "Rains untimely. Crops of wheat and gram damaged. Trades remain unstable. "
                    "People suffer due to oppressive policies of administration. Selling of "
                    "goods profitable in Margsheersh."
                ),
                "Mercury": (
                    "Accumulation of goods profitable. Farmers earn well. Religious persons "
                    "remain busy in religious rituals."
                ),
                "Jupiter": (
                    "Businessmen live with comforts. Produce of fruits and flowers good. "
                    "People are rich, comfortable and religious."
                ),
                "Venus": (
                    "All people blessed with money and goods. Traders have satisfaction. "
                    "Rulers perform their duties honestly."
                ),
                "Saturn": (
                    "Rulers remain worried and ill. Traders and farmers have paucity of funds. "
                    "Scholars too have many problems."
                )
            }
        },
        "X_Durgesh": {
            "sanskrit_name": "Durgesh",
            "appointment": "Lord of the day falling on Leo ingress (Simha Sankranti)",
            "domain": "Defence, security, military, law enforcement",
            "note": (
                "Durgesh Horoscope = horoscope cast for Sun's entry into Leo. "
                "If benefic planets in ascendant or aspecting it — administration efficient; "
                "if malefics on ascendant — adverse and oppressive rule."
            ),
            "planet_outcomes": {
                "Sun": (
                    "Rulers improve legal system and general administration. Justice available "
                    "to everyone in royal court. Administrators work honestly."
                ),
                "Moon": (
                    "Rulers rule with ethics. Comforts and luxuries of people increase. "
                    "Sugarcane and dairy products available abundantly. Diseases less. "
                    "However bitterness between rulers and senior officials."
                ),
                "Mars": (
                    "People suffer due to wrong conduct of rulers or national calamities. "
                    "Traders operate under fear due to government policies and do not earn "
                    "profits due to oppressive laws."
                ),
                "Mercury": (
                    "People have happiness-sorrows together. Land army and navy strengthened. "
                    "People have safety in journeys. Incidents of theft and robberies less. "
                    "Rulers use diplomacy."
                ),
                "Jupiter": (
                    "Rulers maintain law and administration efficiently. Cities and villages "
                    "have general amenities. Armed forces strengthened."
                ),
                "Venus": (
                    "Senior administrators have comforts and amenities. Traders and important "
                    "persons live lavishly."
                ),
                "Saturn": (
                    "People have to leave their homes due to war. Suffer due to humiliations "
                    "meted out by enemies. Ripe crops damaged by locusts and rats."
                )
            }
        }
    },
    "interpretation_note": (
        "Results must be synthesized across all 10 officials. First assess each official "
        "independently, then combine. Afflicted officials (combust, debilitated, aspected by "
        "malefics) produce worse outcomes. Strong officials (exalted, own sign, benefic aspect) "
        "produce better outcomes. Cross-reference with Samvatsar lord result for confirmation."
    ),
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approval_status": "pending_review"
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 2 — Gaur Ch 2: Nine Clouds (Nava Megha)
# ─────────────────────────────────────────────────────────────────────────────
GAUR_CH2_NINE_CLOUDS = {
    "spec_id": "gaur-ch2-nine-clouds",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": "mundane-engine-v3-20260506",
    "title": "Nine Clouds (Nava Megha) — Formula and Results",
    "source": "gaur_aifas_ch2",
    "formula": "Multiply Shak Samvat by 8, divide by 9. The remainder (1–9) indicates the cloud type.",
    "formula_example": "Year 2002: Shak Samvat = 1924. 1924 × 8 = 15392. 15392 ÷ 9 = remainder 2 → Cloud = Samvart",
    "clouds": [
        {"id": 1, "name": "Aavart",  "result": "Rains less. Crops of wheat, barley, rice, cotton damaged."},
        {"id": 2, "name": "Samvart", "result": "Rains sufficient. Winds in East. Sexual immoral acts more. People take less interest in religious noble acts."},
        {"id": 3, "name": "Pushkar", "result": "Rains less. People suffer due to diseases. Immoral acts increase. Vegetables and fruits grown insufficiently."},
        {"id": 4, "name": "Dron",    "result": "Rains good and timely. All persons flourish and have money. Government treasures also full."},
        {"id": 5, "name": "Kaal",    "result": "Rains insufficient. Affluent people devoid of disease and suffering. Rulers have mutual acrimony."},
        {"id": 6, "name": "Neel",    "result": "Rains good and sufficient. People rich and satisfied. Milk available freely. Crops of cotton good."},
        {"id": 7, "name": "Varun",   "result": "Rains good and timely. Amenities of people good. Religious persons respected by society."},
        {"id": 8, "name": "Vayu",    "result": "Rains less. All crops of grains damaged. Accumulated grains get depleted."},
        {"id": 9, "name": "Tam",     "result": "Rains less and diseases more. Produce of crops reduced. People suffer due to various reasons."}
    ],
    "rainfall_signal": {
        "good_rain_clouds": [2, 4, 6, 7],
        "poor_rain_clouds": [1, 3, 5, 8, 9]
    },
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approval_status": "pending_review"
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 3 — Gaur Ch 2: Twelve Snakes (Dvadasha Sarpa)
# ─────────────────────────────────────────────────────────────────────────────
GAUR_CH2_TWELVE_SNAKES = {
    "spec_id": "gaur-ch2-twelve-snakes",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": "mundane-engine-v3-20260506",
    "title": "Twelve Snakes (Dvadasha Sarpa) — Formula and Results",
    "source": "gaur_aifas_ch2",
    "formula": "Add 2 in Shak Samvat, divide by 12. The remainder (1–12) indicates the snake type.",
    "formula_example": "Year 2002: Shak Samvat = 1924. 1924 + 2 = 1926. 1926 ÷ 12 = remainder 6 → Snake = Takshak",
    "snakes": [
        {"id": 1,  "name": "Sunughn",      "result": "Rains medium. People remain engaged in noble activities."},
        {"id": 2,  "name": "Nandsari",     "result": "Rains more. People enjoy more comforts and luxuries."},
        {"id": 3,  "name": "Kakotak",      "result": "Rains less. Rulers pass through difficulties. Mourning due to death of a senior ruler."},
        {"id": 4,  "name": "Prithushrav",  "result": "Rains less and crops of grains are damaged."},
        {"id": 5,  "name": "Vasuki",       "result": "Rains good. Crops good."},
        {"id": 6,  "name": "Takshak",      "result": "Rains medium. Friction between two countries creates hostile atmosphere."},
        {"id": 7,  "name": "Kambal",       "result": "Rains and crops poor."},
        {"id": 8,  "name": "Ashwatar",     "result": "Rains scanty and drought. Crops damaged."},
        {"id": 9,  "name": "Hemamali",     "result": "Rains more and grains produced more."},
        {"id": 10, "name": "Narendra",     "result": "Rains sufficient and timely at all places."},
        {"id": 11, "name": "Vajradanshtra","result": "Rains scarce. Crops damaged."},
        {"id": 12, "name": "Vrish",        "result": "Rains medium. Production of grains less."}
    ],
    "rainfall_signal": {
        "good_rain_snakes": [2, 5, 9, 10],
        "poor_rain_snakes": [3, 4, 7, 8, 11, 12]
    },
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approval_status": "pending_review"
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 4 — Gaur Ch 8: Planet Commodity Ownership
# ─────────────────────────────────────────────────────────────────────────────
GAUR_CH8_PLANET_COMMODITY = {
    "spec_id": "gaur-ch8-planet-commodity-ownership",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": "mundane-engine-v3-20260506",
    "title": "Planet Commodity Ownership — Materials and Goods Owned by Each Planet",
    "source": "gaur_aifas_ch8",
    "usage": (
        "When forecasting production/price of a commodity, identify its planetary ruler. "
        "Assess that planet's strength, aspects and transit position. Exalted/strong = "
        "abundant and cheap; debilitated/afflicted = scarce and expensive."
    ),
    "planets": {
        "Sun": {
            "commodities": ["Gold", "Copper", "Grains", "Wheat", "Mustard", "Perfumery",
                           "Red colour things", "Silk", "Leather goods"],
            "significator": "Sun"
        },
        "Moon": {
            "commodities": ["Silver", "Rice", "Wheat", "Barley", "Materials produced out of water",
                           "Salt", "Juicy materials", "Sugarcane", "Pearl", "Shells", "Honey"],
            "significator": "Moon"
        },
        "Mars": {
            "commodities": ["Copper", "Gur (jaggery)", "Red things", "Coral", "Mensil",
                           "Red flowers", "Red fruits", "Arms and weapons"],
            "significator": "Mars"
        },
        "Mercury": {
            "commodities": ["Green things", "Vegetables", "Green clothes", "Moong (lentil)",
                           "Arhar (lentil)", "Peas", "Plants", "Peanuts", "Perfumery",
                           "Rise and fall in business"],
            "significator": "Mercury"
        },
        "Jupiter": {
            "commodities": ["Turmeric", "Gold", "Yellow materials", "Things grown on climbing plants",
                           "Topaz", "Cotton cloth", "Rock salt (Saindha Namak)"],
            "significator": "Jupiter"
        },
        "Venus": {
            "commodities": ["Silver", "Silken clothes", "Ghee", "Hoziery goods", "Sugar",
                           "White things", "Materials of luxury"],
            "significator": "Venus"
        },
        "Saturn": {
            "commodities": ["Hot (peppery/acrid) things", "Big factories", "Steel mills",
                           "Leather goods", "Blue and black clothes", "Til (sesame)",
                           "Urad (lentil)", "Gram", "Peas", "Machinery", "Chemicals",
                           "Foreign capital"],
            "significator": "Saturn"
        },
        "Rahu_Ketu": {
            "commodities": ["Agate (Gomed)", "Goat", "Donkey", "Camel", "Onions", "Garlic",
                           "Foul smelling things"],
            "significator": "Rahu/Ketu"
        }
    },
    "interpretation_note": (
        "Increase-decrease in production of above goods is forecast by exaltation-debilitation, "
        "retrogression, direct motion, rise, combustion, malefic-benefic situation or aspect of "
        "significator planets."
    ),
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approval_status": "pending_review"
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 5 — Gaur Ch 8: Sign Commodity Ownership
# ─────────────────────────────────────────────────────────────────────────────
GAUR_CH8_SIGN_COMMODITY = {
    "spec_id": "gaur-ch8-sign-commodity-ownership",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": "mundane-engine-v3-20260506",
    "title": "Zodiac Sign Commodity Ownership — Naturally Signifying Materials",
    "source": "gaur_aifas_ch8",
    "note": "The zodiac sign of a material is decided by the first letter of its name.",
    "signs": {
        "Aries":       ["Red wheat", "Barley", "Red colour things", "Red sandal", "Cloth", "Silk",
                        "Woolen clothes", "Pashmeena wool", "Turmeric", "Gums", "Gold", "Silver",
                        "Herbs", "Masoor (lentil)"],
        "Taurus":      ["Ghee", "Milk", "Cotton thread", "Cotton clothes", "White things",
                        "Sugar", "Salt", "Aniseed"],
        "Gemini":      ["Millet", "Maize", "Cotton seed", "Yarn", "Jute and its materials",
                        "Cotton", "Rice"],
        "Cancer":      ["Silver", "Grocery materials", "Banana", "Grass", "Cinnamon", "Onion",
                        "Cassia", "Orange", "Lemon", "Tea", "Spices"],
        "Leo":         ["Gram", "Grains covered by straw", "Gur", "All juicy materials", "Leather"],
        "Virgo":       ["Millet", "Arhar (lentil)", "Peas", "Moong (lentil)", "Moth (lentil)",
                        "Wheat", "Green clothes", "Khand", "Sugar", "Linseed", "Rajma"],
        "Libra":       ["Urad (horse bean)", "Wheat", "Barley", "Coconut", "Arhar (lentil)",
                        "Mustard", "Peas"],
        "Scorpio":     ["Gur", "Khand", "Sweets", "Perfumery", "Til (sesame)", "Black things"],
        "Sagittarius": ["Juicy materials", "Potato", "Alkaline materials", "White grains",
                        "Roots", "Sea-products", "Salt"],
        "Capricorn":   ["Gold", "Iron", "Coal", "Steel", "Glass", "Bell metal", "Trees"],
        "Aquarius":    ["Water products", "Urad (horse bean)", "Til (sesame)", "Oils",
                        "Grocery material", "Electric goods", "Electronic materials"],
        "Pisces":      ["Ghee", "Oil", "Fish", "War materials"]
    },
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approval_status": "pending_review"
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 6 — Gaur Ch 8: Nakshatra Commodity Ownership
# ─────────────────────────────────────────────────────────────────────────────
GAUR_CH8_NAKSHATRA_COMMODITY = {
    "spec_id": "gaur-ch8-nakshatra-commodity-ownership",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": "mundane-engine-v3-20260506",
    "title": "Nakshatra Commodity Ownership — Materials Governed by Constellations",
    "source": "gaur_aifas_ch8",
    "nakshatras": {
        "Ashwini":        ["Rice", "Edible powder (churna)", "Grains of all types", "Clothes",
                           "Ghee", "Camel", "Pony and similar animals"],
        "Bharani":        ["Husky grains", "Millet", "Chillies", "All herbs"],
        "Krithika":       ["Rice", "Barley", "Metals", "Til (sesame)", "Ruby", "Diamond"],
        "Rohini":         ["All grains", "All juices", "All metals", "Woolen clothes", "Old blankets"],
        "Mrigshira":      ["Horses", "Buffalo", "Cows and similar animals", "Lac", "Koda",
                           "Grains", "Donkey", "Tuar (lentil)", "Gems"],
        "Ardra":          ["Salt", "Oil", "All alkalies", "All juices", "Aromatic things like sandal"],
        "Punarvasu":      ["Gold", "Silver", "Cotton", "Millet", "Kushumbh", "Black silken cloth"],
        "Pushya":         ["Gold", "Silver", "Ghee", "Rice", "Rock salt", "Asafoetida",
                           "Oil", "Mustard", "Vegetables"],
        "Aashlesha":      ["Majeeth (madaar)", "Gur", "Khand (sugar)", "Wheat", "Dry ginger",
                           "Chillies", "Koda", "Grains", "Rice"],
        "Magha":          ["Til (sesame)", "Oil", "Ghee", "Coral", "Gram", "Linseed", "Gur"],
        "Poorva_Phalguni":["Wool", "Blanket", "Millet", "Oil", "Silver items"],
        "Uttara_Phalguni":["Urad (horse bean)", "Moong (kidney bean)", "Rice", "Koda",
                           "Rock salt", "Garlic", "Vegetables"],
        "Hast":           ["Sandal", "Camphor", "Pine", "Aloes", "Red sandal", "Roots"],
        "Chitra":         ["Gold", "Gems", "Moong (kidney bean)", "Urad (horse bean)", "Rice",
                           "Gur", "Horse", "Vehicle"],
        "Swati":          ["Betelnut", "Chillies", "Mustard oil", "Asafoetida", "Dates"],
        "Vishakha":       ["Barley", "Wheat", "Rice", "Moong (kidney bean)", "Masoor (lentil)",
                           "Moth (lentil)", "Grains"],
        "Anuradha":       ["Tuar (lentil)", "All grains except pulses", "Rice", "Moth", "Gram"],
        "Jyeshtha":       ["Guggul", "Gur", "Lac", "Camphor", "Mercury (element)",
                           "Asafoetida", "Kalsi"],
        "Mool":           ["White things", "Juices", "Grains", "Rock salt", "Salts", "Cotton"],
        "Poorvashadh":    ["Collyrium (surma)", "Husk", "Grains", "Ghee", "Roots (kandmool)",
                           "Joorna", "Rice"],
        "Uttarashadh":    ["Horse", "Ox", "Elephant", "Iron goods", "All alkalies", "Ghee"],
        "Abhijit":        ["Grapes", "Dates", "Betelnuts", "Cardamom", "Moong (kidney bean)",
                           "Nutmeg", "Horse"],
        "Shravan":        ["Chestnut", "Chironji", "Pippal", "Betelnut", "Husk", "Grains"],
        "Dhanishtha":     ["Gold", "Silver", "Currencies", "Ruby", "Pearl", "Gems"],
        "Shatbhisha":     ["Oil", "Koda", "Wine", "Aanwla (fruit)", "Roots of plants with "
                           "extractable materials", "Sheet made of bark"],
        "Poorva_Bhadrapad":["Priyangu root", "Mace", "All grains", "All herbs", "Pine"],
        "Uttara_Bhadrapad":["Gur", "Khand", "Sugar", "Oilcake", "Rice", "Ghee", "Ruby", "Pearl"],
        "Revti":          ["All materials of grocery", "Ruby", "Pearl", "Coconut", "Betelnut"]
    },
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approval_status": "pending_review"
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 7 — Mehta Ch 7: Koorma Chakra — Modern Geographic Mapping
# ─────────────────────────────────────────────────────────────────────────────
MEHTA_CH7_KOORMA_GEO_MODERN = {
    "spec_id": "mehta-ch7-koorma-geo-modern",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": "mundane-engine-v3-20260506",
    "title": "Koorma Chakra — Modern Geographic Mapping (Mehta/Rao Version)",
    "source": "mehta_rao_ch7",
    "description": (
        "The Koorma (Tortoise) Chakra divides the world into 9 zones, each governed by a "
        "nakshatra group. When malefic planets transit through a zone's nakshatras, the "
        "corresponding geographic region faces trouble. Mehta/Rao adds modern state/country "
        "identifications to Varahamihira's ancient regional names."
    ),
    "zones": {
        "Center_North": {
            "direction": "Center / North",
            "nakshatras": ["Kritika (3)", "Mrigshira (4)", "Rohini (5)"],
            "nakshatra_numbers": [3, 4, 5],
            "modern_regions": [
                "Central India",
                "Parts of Maharashtra",
                "Punjab (Gurdaspur)",
                "Pathankot and Karnal in Haryana",
                "Hastinapur",
                "Kuru and Ayodhiya"
            ],
            "ancient_names": ["Madhyadesa", "Panchala", "Matsaya", "Surasena", "Pandu"]
        },
        "East": {
            "direction": "East (Head of Tortoise)",
            "nakshatras": ["Ardra (6)", "Punarvasu (7)", "Pushya (8)"],
            "nakshatra_numbers": [6, 7, 8],
            "modern_regions": [
                "Bihar", "Jharkhand", "Bangladesh",
                "Meghalaya", "Assam", "Nagaland",
                "Manipur", "Mizoram", "Tripura"
            ],
            "ancient_names": ["Magadha", "Vanga", "Pragjyotish", "Paundra", "Burdwan"]
        },
        "South_East": {
            "direction": "South East",
            "nakshatras": ["Ashlesha (9)", "Magha (10)", "Purva Phalguni (11)"],
            "nakshatra_numbers": [9, 10, 11],
            "modern_regions": [
                "Southern part of West Bengal",
                "Orissa",
                "Andhra Pradesh",
                "Pondicherry",
                "Parts near Jabalpur"
            ],
            "ancient_names": ["Kalinga", "Kosala", "Vanga (south)", "Upavanga"]
        },
        "South": {
            "direction": "South",
            "nakshatras": ["Uttarphalguni (12)", "Hasta (13)", "Chitra (14)"],
            "nakshatra_numbers": [12, 13, 14],
            "modern_regions": [
                "Sri Lanka", "Tamil Nadu", "Konkan",
                "Kerala", "Part of Karnataka",
                "Nasik", "Kanchi"
            ],
            "ancient_names": ["Simhala", "Lanka", "Dravida", "Chola", "Kerala", "Konkan"]
        },
        "South_West": {
            "direction": "South West",
            "nakshatras": ["Swati (15)", "Vishakha (16)", "Anuradha (17)"],
            "nakshatra_numbers": [15, 16, 17],
            "modern_regions": [
                "Goa",
                "Karnataka",
                "Part of South West Maharashtra",
                "Pallava region",
                "Kambhoja (South of Kashmir extended to Kafirstan)",
                "Sindhu-Sauveera"
            ],
            "ancient_names": ["Anarta", "Sindhu", "Saurashtra", "Kambhoja"]
        },
        "West": {
            "direction": "West",
            "nakshatras": ["Jyeshtha (18)", "Moola (19)", "Purvashadha (20)"],
            "nakshatra_numbers": [18, 19, 20],
            "modern_regions": [
                "West Maharashtra",
                "Travancore",
                "Punjab (including West Punjab of Pakistan)",
                "Baluchistan"
            ],
            "ancient_names": ["Sindhu-Sauvira", "Sakas", "Malechas"]
        },
        "North_West": {
            "direction": "North West",
            "nakshatras": ["Uttarashada (21)", "Sravana (22)", "Dhanistha (23)"],
            "nakshatra_numbers": [21, 22, 23],
            "modern_regions": [
                "North Pakistan",
                "Afghanistan",
                "Northern part of Kashmir",
                "Part of Rajasthan (near Jodhpur)",
                "Upper Oxus Valley including Balkh and Badakshan"
            ],
            "ancient_names": ["Harahaura (between Indus and Jhelum)", "Gandhara", "Taxila"]
        },
        "North": {
            "direction": "North",
            "nakshatras": ["Satabhisha (24)", "Poorvabhadra (25)", "Uttarbhadra (26)"],
            "nakshatra_numbers": [24, 25, 26],
            "modern_regions": [
                "Central Asia",
                "North West India and Pakistan",
                "Part of Kashmir",
                "Some parts of Punjab, Haryana",
                "Uttar Anchal",
                "Part of northern UP"
            ],
            "ancient_names": ["Uttara Kuru", "Kailasha", "Himavat"]
        },
        "North_East": {
            "direction": "North East",
            "nakshatras": ["Revati (27)", "Ashvini (1)", "Bharni (2)"],
            "nakshatra_numbers": [27, 1, 2],
            "modern_regions": [
                "Nepal", "Sikkim", "Bhutan",
                "Arunachal Pradesh", "Tibet", "China", "Burma"
            ],
            "ancient_names": ["Brahmapura", "Darva", "Cinarattha (China)"]
        }
    },
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approval_status": "pending_review"
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 8 — Mehta Ch 7: Planet Direction and Country Rulership
# ─────────────────────────────────────────────────────────────────────────────
MEHTA_CH7_PLANET_DIRECTION_COUNTRY = {
    "spec_id": "mehta-ch7-planet-direction-country",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": "mundane-engine-v3-20260506",
    "title": "Planet Direction and Country Rulership (Koorma Chakra Extension)",
    "source": "mehta_rao_ch7",
    "planet_directions": {
        "Sun":      "East",
        "Moon":     "North-West",
        "Mars":     "South",
        "Mercury":  "North",
        "Jupiter":  "North-East",
        "Venus":    "South-East",
        "Saturn":   "West",
        "Rahu_Ketu":"South, West"
    },
    "planet_country_rulership": {
        "Sun":     ["Eastern half of Narmada", "Orissa", "Bengal", "Bihar",
                    "Kambhoja", "Eastern Tamil Nadu", "Kausambhi"],
        "Moon":    ["Kosala", "Broach"],
        "Mars":    ["Narmada", "Sindhu", "Mahanandi", "Bhimrataha", "Shipra River",
                    "Malya", "Chola", "Dravida", "Andhra", "Konkan", "Vihar", "Vindhya"],
        "Mercury": ["Ganga", "Saryu", "Himalayan States", "Surashtra"],
        "Jupiter": ["Eastern Punjab", "Western UP", "Satabru"],
        "Venus":   ["Taxila", "Gandhara", "Malva", "Vitasta", "Iravati"],
        "Saturn":  ["Saurashtra", "Vidisa", "Rajasthan"],
        "Rahu":    ["Suleka", "Kinnars"],
        "Ketu":    ["Iran", "Hunas", "Afghanistan", "China", "Cholas"]
    },
    "usage": (
        "When a planet is afflicted by transit malefics, the country/region it rules faces "
        "trouble. Cross-reference with Koorma zone of afflicting planet's nakshatra position "
        "to pinpoint the affected geographic area."
    ),
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approval_status": "pending_review"
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 9 — Mehta Ch 7: Nakshatra Affliction → Country (Brihat Samhita Table)
# ─────────────────────────────────────────────────────────────────────────────
MEHTA_CH7_NAKSHATRA_COUNTRY_AFFLICTION = {
    "spec_id": "mehta-ch7-nakshatra-country-affliction",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": "mundane-engine-v3-20260506",
    "title": "Nakshatra Affliction → Country Destroyed (Brihat Samhita Table)",
    "source": "mehta_rao_ch7",
    "description": (
        "According to Brihat Samhita, when the following nakshatras are afflicted by malefics, "
        "the kings of the corresponding countries are destroyed."
    ),
    "table": [
        {"nakshatras": ["Krittika", "Rohini", "Mrigsira"],             "countries_affected": ["Panchala"]},
        {"nakshatras": ["Ardra", "Punarvasu", "Pushyami"],             "countries_affected": ["Magadha"]},
        {"nakshatras": ["Ashlesha", "Magha", "Puravphalguni"],         "countries_affected": ["Kalinga"]},
        {"nakshatras": ["Uttarphalguni", "Hast", "Chitra"],            "countries_affected": ["Avanti"]},
        {"nakshatras": ["Swati", "Vishakha", "Anuradha"],              "countries_affected": ["Anarta"]},
        {"nakshatras": ["Jyeshtha", "Moola", "Purvaasadha"],           "countries_affected": ["Sindhu-Sauvira"]},
        {"nakshatras": ["Uttarashada", "Sravan", "Dhanishtha"],        "countries_affected": ["Harahaura (between Indus and Jhelum)"]},
        {"nakshatras": ["Satabhisha", "Poorvabhadra", "Uttarbhadra", "Revati"], "countries_affected": ["Madra"]},
        {"nakshatras": ["Ashvini", "Bharni"],                          "countries_affected": ["Kuninda"]}
    ],
    "modern_interpretation": (
        "Apply to modern geopolitics: Panchala = Haryana/UP corridor; Magadha = Bihar/Bangladesh; "
        "Kalinga = Orissa/Andhra coast; Sindhu-Sauvira = Pakistan/Sindh; "
        "Harahaura = Afghanistan/NW Pakistan border zone."
    ),
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approval_status": "pending_review"
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 10 — Mehta Ch 22: Planetary Cabinet — Domain Lords + Per-Planet Outcomes
# ─────────────────────────────────────────────────────────────────────────────
MEHTA_CH22_PLANETARY_CABINET = {
    "spec_id": "mehta-ch22-planetary-cabinet-domain-lords",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": "mundane-engine-v3-20260506",
    "title": "Planetary Cabinet — Domain Lord Determination + Per-Planet Results (Mehta/Rao)",
    "source": "mehta_rao_ch22",
    "description": (
        "According to Kalaparkashika and classical texts, a year's outcomes are determined by "
        "the planetary lords holding 7 key portfolios. Each portfolio-lord is the planet ruling "
        "the weekday of a specific solar ingress. Results are general and must be combined with "
        "national horoscope, chaitra shukla pratipada, and lunar charts."
    ),
    "portfolio_determination": {
        "King_Raja": {
            "appointment": "Planet ruling the day of Chaitra Shukla Pratipada (Hindu New Year). Majority of astrologers decide it on the basis of the lord of the day on which the Hindu new year starts.",
            "domain": "Overall governance, war/peace, general fate of the year"
        },
        "Lord_of_Paddy_Crops": {
            "appointment": "Planet ruling the day when Sun enters first point of Cancer",
            "domain": "Paddy, rice, kharif crops"
        },
        "Lord_of_Fruits_Vegetation": {
            "appointment": "Planet ruling the day when Sun enters first point of Libra",
            "domain": "Fruits, vegetables, horticulture"
        },
        "Lord_of_Mineral_Kingdom": {
            "appointment": "Planet ruling the day when Sun enters first point of Capricorn",
            "domain": "Minerals, metals, mining"
        },
        "Lord_of_Clouds": {
            "appointment": "Planet ruling the day when Sun enters first point of Ardra nakshatra",
            "domain": "Monsoon, rainfall, cloud formation"
        },
        "Lord_of_Corns": {
            "appointment": "Planet ruling the day when Sun enters first point of Sagittarius",
            "domain": "Winter grains (rabi crops)"
        },
        "Lord_of_Fluids": {
            "appointment": "Planet ruling the day when Sun enters first point of Gemini",
            "domain": "Liquids, water, ghee, oils, dairy"
        }
    },
    "lord_of_year_results": {
        "Sun": {
            "as_King": (
                "Kings would be mentally disturbed. Danger by fire and thieves. Unexpected "
                "misfortune will befall rulers and prominent personalities. Prosperity for "
                "dishonest traders and distress to common persons. The year will be unusually "
                "hot. There will be little rains and food will be scarce. Kings will be in "
                "bad temper. There will be destructive attacks and invasions and mindless "
                "violence. Rulers will go about destroying countries in war. "
                "According to Varahamihira: 'Earth will yield very little crops, there will be "
                "very little water in the rivers and medicines will not have their potency. Even "
                "in winter Sun will be extremely warm, clouds will not pour down sufficient "
                "rain... kings will go about destroying countries in war.'"
            ),
            "as_Prime_Minister": "Discontentment amongst kings, poor rainfall, scanty harvest, unrighteous acts.",
            "as_Agricultural_Growth": "Good yield of white grains and grains having colour of conch.",
            "as_Fluids": "Rise of price of ghee, oil, honey and sweet substances.",
            "as_Metals_Minerals": "Gold, lead, zinc, musk and sapphire become prominent.",
            "as_Grains": "Scanty rains, period of shortage, slight fall in prices, growth of unhealthy or poisonous grains, period of anxiety."
        },
        "Moon": {
            "as_King": (
                "Plenty of rains and abundance of all kinds of crops and vegetation and milk. "
                "People will be happy, prosperous and religiously inclined. There will be less "
                "crime and justice will be administered properly. "
                "Note: What happens if Moon is afflicted is a matter of research — there is "
                "national pain caused by the conflagration of some known or feared problem during "
                "the year, like the naxalite movement in India."
            ),
            "as_Prime_Minister": "Good rainfalls, luxuriant growth, health, general well being and prosperity, contentment to the people.",
            "as_Agricultural_Growth": "Good vegetation, thick growth of trees and all kind of good crops.",
            "as_Fluids": "Rise in price of ghee, oil, honey, sugar, milk, curd and candy; general health becomes good.",
            "as_Metals_Minerals": "Increase of camphor, sandal, white clothes, pearls, saffron-powder and flowers.",
            "as_Grains": "Good rainfall, general prosperity, plenty of milk, peace of mind and freedom from disease."
        },
        "Mars": {
            "as_King": (
                "Fighting amongst the kings, trouble by thieves. There will be plenty of fires "
                "in forests and other places, robberies will take place, life and property will "
                "not be safe. There will be less of food crops and people will be unhappy, "
                "crimes will increase. "
                "Note: Mars needs to be studied for our further research more and more these days "
                "in view of increasing terrorist activities all over the world as it involves "
                "destruction of property as signified by Mars."
            ),
            "as_Prime_Minister": "Unrighteous kings, little rain, less trade, trouble to people by weapon or fire.",
            "as_Agricultural_Growth": "Abundance of red paddy and grams of all sorts. The planet favors cultivation of gravel soil. Sudden increase in prices of dal, jawar, ghee, jaggery, rice and sugar. Southwest monsoon accompanied by lot of thunder.",
            "as_Fluids": "Rise in price of black mustard, salt, ghee, sesame, oil and sugar. Danger by fire.",
            "as_Metals_Minerals": "Rise in price of black mustard, salt, ghee, sesame, oil and sugar; danger by fire in villages, sandalwood and conch become scarce.",
            "as_Grains": "Poor yield, high prices, bad corn, fertility of red soil."
        },
        "Mercury": {
            "as_King": (
                "There will be peace and prosperity, rains will be plentiful, stock markets will "
                "flourish. It will be good year for artists and publishing industry. Country will "
                "have good relations with others. People will be truthful and crimes will decrease. "
                "According to Brihat Samhita: writers, artists, musicians and warriors would "
                "prosper. There will be much socializing and exchange of gifts. Good year for animal "
                "husbandry, trade and commerce. Vedic studies will be pursued and justice will be "
                "dispensed. Rulers will care for the ruled. Studies of yoga and spiritual sciences "
                "will be pursued vigorously."
                "Note: The modern significations of Mercury like media, communications also come "
                "into prominence in a good or bad way depending on the condition of Mercury."
            ),
            "as_Prime_Minister": "Ill feeling among kings, distress by storms, average rainfall and agriculture.",
            "as_Agricultural_Growth": "Poor and light rainfall, scanty agricultural growth. People will be very anxious.",
            "as_Fluids": "Plenty of cow's milk, just rulers, plenty of corn.",
            "as_Metals_Minerals": "Plenty of milk of cows and all kinds of corns.",
            "as_Grains": "Meager rain, poor growth of corn and fruit and that too in some places."
        },
        "Jupiter": {
            "as_King": (
                "Crops will be excellent, food will be plenty and gods will be happy. There will "
                "be chanting of Vedic hymns and performance of sacrifices, animals and vegetable "
                "kingdom will prosper. Rains will be plenty and prosperity will be all around. "
                "Rule of law will prevail."
                "Note: Take the modern significations which represents banks. If Jupiter is "
                "afflicted the banking system collapses. Tragedy may befall dignitaries."
            ),
            "as_Prime_Minister": "Happiness, plenty of corn and vegetation, contentment, good cattle and plenty of milk.",
            "as_Agricultural_Growth": "Luxuriant growth, impartial administration of justice, good milk yield, good rainfall and prosperity to livestock.",
            "as_Fluids": "Plenty of rain and milk as well as vegetation.",
            "as_Metals_Minerals": "Plenty of rain, vegetation and milk.",
            "as_Grains": "Universal rain, fertility, plenty of milk."
        },
        "Venus": {
            "as_King": (
                "There will be victory and prosperity all round with plenty of good crops and "
                "rains. Artists will thrive, people will enjoy. There will be plenty of merry "
                "making. Life would be fun with all types of entertainment. Soldiers will be "
                "victorious in battle. New treaties and agreements will be signed. "
                "Note: It is worth noting that in the age in which we live in with the television "
                "and newspapers pandering to people in the world of glamour at the cost of more "
                "important national figures, good or bad, Venus makes a world of difference to "
                "the morals of the society."
            ),
            "as_Prime_Minister": "Celebrity marriages, plenty of corn and milk, prosperity.",
            "as_Agricultural_Growth": "Fertility and plenty of grain.",
            "as_Fluids": "Plenty of food and rainfall.",
            "as_Metals_Minerals": "Good rainfall and plenty of sweet products.",
            "as_Grains": "Plenty of rain and prosperity, immunity from illness."
        },
        "Saturn": {
            "as_King": (
                "Band of robbers will roam about. People will be deprived of their lives, "
                "property and wealth. Hunger and disease will stalk the land, there will be no "
                "rains, earth will be parched, lakes and tanks will dry up, crops will perish, "
                "rain god will yield but little rain, destruction and misery will be everywhere. "
                "Sun and Moon will lose their luster. "
                "Saturn became raja or king in the year 1991. Chaitra pratipada 16 March 1991, "
                "13:42, the year was full of strikes, discontentment, shortage of food and rainfalls."
            ),
            "as_Prime_Minister": "Poor rainfall and bad agricultural yield, not a very good time for people and cattle, but good for foreigners and outcasts.",
            "as_Agricultural_Growth": "Favours black soil and growth of sesame and black gram.",
            "as_Fluids": "Poor rains, poor crops and scanty growth of juicy products, grain and corn. Destruction of crops due to heavy rain and less yield. Outbreak of epidemics, starvation and malnutrition of people. Malechas will come to prominence.",
            "as_Metals_Minerals": "Poor rainfall and crops, shortage of juicy products, grain and corn, malecha will come into prominence.",
            "as_Grains": "Scanty rain, famine, anxiety, black soil proves fertile."
        }
    },
    "lord_of_year_varahamihira": {
        "description": "Results of the Various Planets becoming Lord of the Year per Varahamihira (Brihat Samhita) — Chapter XXIII of Mehta",
        "Sun": "Very little crops and little rain. Rivers dry. Scarcity of food for men and animals. Even in winter Sun will be very warm. Kings will embark on destructive path of wars by destroying other countries.",
        "Moon": "Plenty of rain and food. Joy and mirth will prevail. Plenty of vegetation and flowers. Women will be happy, well adorned and in amorous mood. Lakes and rivers will be full of water. People will perform religious duties and sacrifices and be happy.",
        "Mars": "Bad year for food and crops. Very little rain. Fires all around, robberies. Kings will not be interested in governing properly. Bilious diseases will be rampant. People will be afflicted with many calamities.",
        "Mercury": "Good year for people having profession in magic, mines, hypnotism and jugglery as well as for musicians, townsmen, mathematicians, painters, accountants and fighters. Agriculture and trade will thrive. Justice will be administered by the king. Vedic and scientific studies will prevail. Plantations and herbs will be in plenty.",
        "Jupiter": "Crops will be excellent, food will be plenty and gods will be happy. Chanting of Vedic hymns and performance of sacrifices. Animals and vegetable kingdom will prosper. Rains will be plenty and prosperity will be all around. Rule of law will prevail.",
        "Venus": "Rains plentiful, lakes full. Abundant crops of rice and sugar cane. Flowers will give pleasant fragrance. Women will look beautiful and amorous. Kings will be victorious over their enemies. Virtuous people will thrive and wicked will be destroyed. Young persons will enjoy drinks and make merry, music and songs will rend the earth and make it a beautiful place to live in. Year of victory to Goddess of love and beauty.",
        "Saturn": "Band of robbers will roam about. People will be deprived of their lives, property and wealth. Hunger and disease will stalk the land, there will be no rains, earth will be parched, lakes and tanks will dry up, crops will perish, rain god will yield but little rain, destruction and misery will be everywhere. Sun and Moon will lose their luster."
    },
    "general_notes": [
        "Results given above are of a general nature and should not be taken literally. These are just only guidelines.",
        "Planets have been used mostly and mainly for agricultural and horticultural yield and not for various industries and metals which they represent in our age of science and technology.",
        "Planets represent new class of professions unknown in the times when these books were written — determine which professions would do well in a given year.",
        "All these are to be combined with synthesized readings of annual horoscopes based on national horoscopes, chaitra shukla pratipada horoscope and the soorya veedhi and fortnightly lunar charts."
    ],
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approval_status": "pending_review"
}

# ─────────────────────────────────────────────────────────────────────────────
# MASTER LIST
# ─────────────────────────────────────────────────────────────────────────────
ALL_SPECS = [
    GAUR_CH2_CELESTIAL_COUNCIL_OUTCOMES,
    GAUR_CH2_NINE_CLOUDS,
    GAUR_CH2_TWELVE_SNAKES,
    GAUR_CH8_PLANET_COMMODITY,
    GAUR_CH8_SIGN_COMMODITY,
    GAUR_CH8_NAKSHATRA_COMMODITY,
    MEHTA_CH7_KOORMA_GEO_MODERN,
    MEHTA_CH7_PLANET_DIRECTION_COUNTRY,
    MEHTA_CH7_NAKSHATRA_COUNTRY_AFFLICTION,
    MEHTA_CH22_PLANETARY_CABINET,
]

# ─────────────────────────────────────────────────────────────────────────────
# RUNNER
# ─────────────────────────────────────────────────────────────────────────────
async def main():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_SPECS)} engine specs from batch mundane-engine-v3-20260506")
        print(f"Collection: mundane_engine_specs  |  science: mundane_jyotish\n")
        for spec in ALL_SPECS:
            print(f"  {spec['spec_id']}")
        print(f"\nTotal: {len(ALL_SPECS)}")
        print("\nDry run complete.")
        return

    import motor.motor_asyncio
    import os
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ.get("DB_NAME", "horoscope_db")]
    col = db["mundane_engine_specs"]

    ok = 0
    for spec in ALL_SPECS:
        result = await col.update_one(
            {"spec_id": spec["spec_id"]},
            {"$set": spec},
            upsert=True
        )
        ok += 1
        print(f"  upserted: {spec['spec_id']}")
    print(f"\nDone. {ok}/{len(ALL_SPECS)} upserted.")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
