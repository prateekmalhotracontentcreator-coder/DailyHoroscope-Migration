"""
Mundane Astrology — Interpretation Rules INGEST v3
Batch: mundane-interp-v3-20260506
Collection: interpretation_rules
Science: mundane_jyotish

New rule groups from direct PDF source reads:
  GROUP_P: Gaur Ch 2 — Celestial Council composite outcome rules (10 rules, 1 per official)
  GROUP_Q: Gaur Ch 2 — Cloud + Snake auxiliary forecast rules (2 rules)
  GROUP_R: Mehta Ch 13 — Eclipse effects by sign element + special cases (6 rules)
  GROUP_S: Mehta Ch 20 — Terrorism astrological parameters + case validations (5 rules)
  GROUP_T: Mehta Ch 26 — Political party dasha framework + historical cases (4 rules)

DRY_RUN = True  →  set False to write to MongoDB.
"""

import asyncio
from datetime import datetime, timezone

DRY_RUN = True

_NOW = datetime.now(timezone.utc).isoformat()
_BATCH = "mundane-interp-v3-20260506"

def _rule(rule_id, sub_type, title, source_chapter, condition, result,
          synthesis_sources, notes="", severity=None, checkable=False):
    d = {
        "rule_id": rule_id,
        "batch_id": _BATCH,
        "science_id": "mundane_jyotish",
        "sub_type": sub_type,
        "title": title,
        "source_chapter": source_chapter,
        "condition": condition,
        "result": result,
        "synthesis_sources": synthesis_sources,
        "checkable": checkable,
        "approval_status": "pending_review",
        "created_at": _NOW,
    }
    if notes:
        d["notes"] = notes
    if severity:
        d["severity"] = severity
    return d

# ═════════════════════════════════════════════════════════════════════════════
# GROUP P — Gaur Ch 2: Celestial Council Official Outcome Rules
# ═════════════════════════════════════════════════════════════════════════════
# One composite rule per official. Each rule contains the full planet_outcomes
# dict as a nested object within condition, allowing the engine to look up the
# planet and retrieve the textual prediction for that official's domain.

GROUP_P = [

    _rule(
        rule_id="mundane-gaur-ch2-king-outcome-matrix",
        sub_type="celestial_council_king",
        title="King (Raja) Planet Outcome Matrix — 7 Planets × Governance Domain",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "official": "King (Raja / Samvatsar King)",
            "appointment_formula": "Lord of the weekday on Chaitra Shukla Pratipada (first day of Vikram Samvat)",
            "domain": "Governance, war/peace, overall prosperity of the year",
            "planet_outcomes": {
                "Sun":     "Rains insufficient. Danger of diseases to people and cattle. Poor produce of fruits and grains. Danger of theft. Loss of lives and wealth due to fires. A senior ruler or leader dies.",
                "Moon":    "More celebrations and auspicious ceremonies. Good rains and crops. Harmony and goodwill in masses. Prestige of rulers increased. Effective measures for better health and peace.",
                "Mars":    "Many events of loss of lives and wealth due to fires. People suffer due to thieves and robbers. Fear prevails due to wars triggered by rulers. Rains insufficient at many places.",
                "Mercury": "Rains excessive. Danger of loss due to floods. Many celebrations like marriages. Comforts and wealth of people increased. Rulers and people enjoy and live happily. Number of cows increases.",
                "Jupiter": "Rains sufficient and timely. Nourishing materials like milk abundant. Many religious rituals and all people take part in celebrations.",
                "Venus":   "Rains sufficient, production of grains high. Good produce of fruits and flowers. Wealth and prosperity of rulers augmented. People devote more time for entertainment. Powers of ladies increase.",
                "Saturn":  "Rains less. People suffer due to various diseases. Differences of politicians intensified. Rulers create atmosphere of wars. Turmoils due to disease, thieves and riots. At few places people leave home due to drought."
            }
        },
        result=(
            "Identify the planetary lord (weekday ruler on Chaitra Shukla Pratipada). "
            "Look up that planet's outcome above. Cross-reference with Samvatsar lord for confirmation. "
            "Assess the planet's strength (exaltation/debilitation, combustion, retrograde, aspect) "
            "to calibrate outcome: strong planet → better version of the result; afflicted → worse version."
        ),
        synthesis_sources=["gaur_aifas_ch2", "mehta_rao_ch22"],
        notes="The King role in Gaur Ch 2 and the Raja/Lord of Year in Mehta Ch 22 are the same concept — cross-reference both books for synthesis.",
        checkable=False
    ),

    _rule(
        rule_id="mundane-gaur-ch2-minister-outcome-matrix",
        sub_type="celestial_council_minister",
        title="Minister (Mantri) Planet Outcome Matrix — 7 Planets × Administration Domain",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "official": "Minister (Mantri)",
            "appointment_formula": "Lord of the weekday on Aries ingress (Mesha Sankranti)",
            "domain": "Administration, law and order, ministerial conduct",
            "planet_outcomes": {
                "Sun":     "Bitterness amongst rulers increased. Fear due to disease and theft. Prosperity and food supply increased. Juicy materials such as gur expensive.",
                "Moon":    "Rains sufficient, crops and grains excellent. Development projects completed. Prosperity and celebrations prevail.",
                "Mars":    "Immoral acts like theft and robbery increase. People suffer due to diseases. Scarcity of milk. Learned scholars remain disturbed due to wrong deeds.",
                "Mercury": "Living conditions improved. Harmony and love in families. Wealth and grains increased. Good rains. Barley, gram, lentils expensive.",
                "Jupiter": "All crops excellent. Rains good. Joys and prosperity prevail. Rulers busy in welfare activities.",
                "Venus":   "Crops damaged by locusts and rats. All grains expensive. Excessive rains and danger of floods. Supremacy of females established. More wind and sex-related diseases.",
                "Saturn":  "Cruel behaviours of rulers and administrators cause sufferings and dissatisfaction amongst people."
            }
        },
        result=(
            "Identify the lord of the weekday on Aries ingress. Look up that planet's outcome above. "
            "Minister's affliction (combust, debilitated, with malefics) indicates administrative breakdown and cruelty."
        ),
        synthesis_sources=["gaur_aifas_ch2"],
        checkable=False
    ),

    _rule(
        rule_id="mundane-gaur-ch2-sasyesh-outcome-matrix",
        sub_type="celestial_council_sasyesh",
        title="Sasyesh (Lord of 4-Month / Summer Crops) Planet Outcome Matrix",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "official": "Sasyesh — Lord of Summer/4-Month Crops",
            "appointment_formula": "Lord of the weekday on Cancer ingress (Karka Sankranti)",
            "domain": "Summer crops: barley, wheat, rice, sugarcane (Kharif season)",
            "associated_horoscope": "Sasyesh Horoscope — cast for the moment of Sun's entry into Cancer",
            "planet_outcomes": {
                "Sun":     "Summer grains expensive. Increase in theft and robberies. Wars among rulers. Cattle fodder in short supply despite good rains. Milk available in sufficient quantity.",
                "Moon":    "Comforts of people increase. Sufficient rains. Milk available in sufficient quantities. Rulers and upper class worship gods and honour scholars. Wealth and grains abundant.",
                "Mars":    "Crops of summer grains barley and wheat damaged. Rains excessive at few places, scanty at others. Many diseases in animals such as elephants, horses, cows and ox.",
                "Mercury": "Crops of grains, wheat, rice, sugarcane good. Rains sufficient. Development projects and amenities excellent. Brahmins and scholars inclined towards religious deeds.",
                "Jupiter": "Crops of summer good. Juicy materials, milk and ghee freely available. Rains good. Feeling of duty and love in minds of people.",
                "Venus":   "Rains timely and sufficient. Wheat, rice, sugarcane sufficient. Flowers and fruits grow abundantly. Atmosphere full of joys.",
                "Saturn":  "Loss of ripe crops such as wheat, rice, barley. Goods expensive. Behaviour of rulers rude. Masses remain entangled in useless disputes."
            }
        },
        result=(
            "Identify the lord of the weekday on Cancer ingress. Look up that planet's outcome above. "
            "Combined with Meghesh (monsoon lord) — if both are malefics the summer crop failure is severe."
        ),
        synthesis_sources=["gaur_aifas_ch2"],
        checkable=False
    ),

    _rule(
        rule_id="mundane-gaur-ch2-dhanyesh-outcome-matrix",
        sub_type="celestial_council_dhanyesh",
        title="Dhanyesh (Lord of Winter Crops) Planet Outcome Matrix",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "official": "Dhanyesh — Lord of Winter Crops",
            "appointment_formula": "Lord of the weekday on Sagittarius ingress (Dhanu Sankranti)",
            "domain": "Winter crops (Rabi season): Moong, Moth/lentil, Millet, Mustard, Wheat",
            "associated_horoscope": "Dhanyesh Horoscope — cast for Sun's entry into Sagittarius",
            "planet_outcomes": {
                "Sun":     "Winter crops Moong, Moth (lentil), Millet destroyed. Goods expensive. Rulers inclined towards fighting and wars. Diseases such as fever. Grains costly.",
                "Moon":    "Winter crops Moong, Moth, Millet, Mustard good. Milk freely available and population increases.",
                "Mars":    "Summer season Millet, Moong, Moth, Rice and Maize available in sufficient quantities. Sugarcane, ghee and oils expensive. People suffer due to fires.",
                "Mercury": "Winter crops good. Rains sufficient except in Sindh and Punjab.",
                "Jupiter": "Crops of Barley, Wheat, Rice good. Religious persons remain busy in religious acts.",
                "Venus":   "Produce of winter crops Moong, Moth, Millet not good. Wheat, cattle fodder and vegetables costly. Rains less and milk insufficient.",
                "Saturn":  "Produce less. Crops of grains, Moong, Moth and Millet suffer due to diseases. National treasure reduced. Wars at few places. Rains not sufficient and timely. Farmers remain worried."
            }
        },
        result=(
            "Identify the lord of the weekday on Sagittarius ingress. Look up that planet's outcome. "
            "Venus and Saturn as Dhanyesh both indicate winter crop losses — critical overlap signal."
        ),
        synthesis_sources=["gaur_aifas_ch2"],
        checkable=False
    ),

    _rule(
        rule_id="mundane-gaur-ch2-meghesh-outcome-matrix",
        sub_type="celestial_council_meghesh",
        title="Meghesh (Lord of Weather and Rains) Planet Outcome Matrix",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "official": "Meghesh — Lord of Weather and Rains",
            "appointment_formula": "Lord of the weekday when Sun enters Ardra nakshatra",
            "domain": "Monsoon quality, rainfall quantity, weather patterns for the year",
            "associated_horoscope": "Meghesh Horoscope — cast for moment of Sun's entry into Ardra nakshatra",
            "planet_outcomes": {
                "Sun":     "Rains less, prices high, politicians have differences. Danger of thefts and robberies. Crops of gram, barley, sugarcane and rice good despite low rain.",
                "Moon":    "Rains in sufficient quantities. Crops of grains and flowers/fruits excellent. Production of milk and ghee good. Rulers live in harmony with other rulers. Amenities of people improved.",
                "Mars":    "All persons forget the path of religious faith. Rains good at some places and insufficient at other locations. People suffer and remain gloomy.",
                "Mercury": "Rains more. Crops of wheat, barley and other grains good. Brahmins remain busy in noble activities. Improvements in all comforts.",
                "Jupiter": "Rains excellent and timely. Crops of juicy materials good. People live comfortably and rulers follow the path of religion.",
                "Venus":   "Rains good. All religious persons live comfortably. People satisfied by conduct of rulers.",
                "Saturn":  "Rains insufficient at few parts of earth. Rulers remain disenchanted. Fear of diseases in the masses."
            }
        },
        result=(
            "Meghesh is the primary rainfall forecaster. Identify the lord of the weekday when Sun enters "
            "Ardra nakshatra. Cross-reference with Gaur Ch 10 Saturn-in-Ardra rule and Rohini protection rule "
            "for monsoon synthesis. Sun or Saturn as Meghesh → drought alert."
        ),
        synthesis_sources=["gaur_aifas_ch2", "gaur_aifas_ch10"],
        checkable=False
    ),

    _rule(
        rule_id="mundane-gaur-ch2-rasesh-outcome-matrix",
        sub_type="celestial_council_rasesh",
        title="Rasesh (Lord of Juicy Materials) Planet Outcome Matrix",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "official": "Rasesh — Lord of Gur (Jaggery), Sugar and Juices",
            "appointment_formula": "Lord of the weekday on Libra ingress (Tula Sankranti)",
            "domain": "Sugar, jaggery, ghee, oils, dairy, juicy commodities",
            "associated_horoscope": "Rasesh Horoscope — cast for Sun's entry into Libra",
            "planet_outcomes": {
                "Sun":     "Rains insufficient. Production of juicy materials like Gur less. Shortage of milk, ghee, oils and clothes. Rulers remain worried due to many problems.",
                "Moon":    "Rains sufficient. Gur-Khand (Sugar) produced adequately. Wealth and grains increased. Young persons remain busy in new methods of entertainment.",
                "Mars":    "Rains insufficient. Juicy materials like Gur and Sugar in short supply. Goods expensive. People dissatisfied by conduct of rulers.",
                "Mercury": "Rains sufficient and timely. All juicy materials and grains available abundantly. Milk and ghee adequate. Rulers run administration well. Security of country maintained.",
                "Jupiter": "People live with luxuries and comforts. Crops of juicy materials good. Learned scholars honoured. Rulers have many vehicles and cattle.",
                "Venus":   "Many celebrations and religious rituals. Rains less in many provinces but production of juicy materials such as Gur and Sugar good. People live comfortably.",
                "Saturn":  "Rains scanty. Crops of juicy materials suffer. Cattle too catch diseases."
            }
        },
        result=(
            "Identify the lord of weekday on Libra ingress. Look up planet outcome for sugar/jaggery/oil "
            "price and supply forecast. Combined with Neersesh (metals) for commodity market analysis."
        ),
        synthesis_sources=["gaur_aifas_ch2"],
        checkable=False
    ),

    _rule(
        rule_id="mundane-gaur-ch2-neersesh-outcome-matrix",
        sub_type="celestial_council_neersesh",
        title="Neersesh (Lord of Metals and Trade) Planet Outcome Matrix",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "official": "Neersesh — Lord of all trades such as metals",
            "appointment_formula": "Lord of the weekday on Capricorn ingress (Makara Sankranti)",
            "domain": "Metals, gemstones, trade, commerce, manufacturing",
            "associated_horoscope": "Neersesh Horoscope — cast for Sun's entry into Capricorn",
            "planet_outcomes": {
                "Sun":     "Gold, copper, silver, ruby, pearl become expensive.",
                "Moon":    "White things, silver, pearl and clothes become expensive.",
                "Mars":    "Gold, brass, copper, red sandal, gems such as coral and red colored things become expensive.",
                "Mercury": "Readymade clothes, hosiery materials, conch shell (Shankh), sandal, metals and gems become expensive.",
                "Jupiter": "Gold, yellow clothes, turmeric and other yellow materials become expensive.",
                "Venus":   "Gold, pearl, diamond and gems, readymade clothes, perfumery and cosmetics become costly.",
                "Saturn":  "Hardware materials, iron, machinery, black clothes and black materials become expensive."
            }
        },
        result=(
            "Use for commodity price forecasting. The Neersesh planet determines which category of metals/goods "
            "faces price pressure. Malefic aspects on the Neersesh planet intensify price rises."
        ),
        synthesis_sources=["gaur_aifas_ch2", "gaur_aifas_ch8"],
        checkable=False
    ),

    _rule(
        rule_id="mundane-gaur-ch2-phalesh-outcome-matrix",
        sub_type="celestial_council_phalesh",
        title="Phalesh (Lord of Fruits and Flowers) Planet Outcome Matrix",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "official": "Phalesh — Lord of Fruits and Flowers",
            "appointment_formula": "Lord of the weekday on Pisces ingress (Meena Sankranti)",
            "domain": "Horticulture: fruits, flowers, vegetables, ornamental plants",
            "associated_horoscope": "Phalesh Horoscope — cast for Sun's entry into Pisces",
            "planet_outcomes": {
                "Sun":     "Earth lush and decorated with fruits and flowers of all types. Rains also sufficient.",
                "Moon":    "Crops good. Fruits and flowers produced in sufficient amounts. Scholars inclined towards entertainment. Rulers efficient.",
                "Mars":    "Production of flowers and fruits poor. Diseases cause sufferings. Tension among rulers.",
                "Mercury": "Production of fruits very good. Rains sufficient. Grass and flowers adequate. People live with comforts and happiness.",
                "Jupiter": "Production of fruits and plants good. All people remain busy in religious rituals.",
                "Venus":   "Crops of grass, vegetables, fruits and flowers good. Administrators get delicious food products. Religious persons devote more time in noble activities.",
                "Saturn":  "Crops of fruits damaged. Flowers of trees do not develop. Losses in winter due to snowfall. Incidents of theft more and people suffer due to diseases."
            }
        },
        result=(
            "Identify the lord of weekday on Pisces ingress. Mars or Saturn as Phalesh → horticultural loss. "
            "Jupiter or Venus as Phalesh → exceptional fruit and flower production."
        ),
        synthesis_sources=["gaur_aifas_ch2"],
        checkable=False
    ),

    _rule(
        rule_id="mundane-gaur-ch2-dhanesh-outcome-matrix",
        sub_type="celestial_council_dhanesh",
        title="Dhanesh (Lord of Wealth and Treasure) Planet Outcome Matrix",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "official": "Dhanesh — Lord of Wealth and Treasure",
            "appointment_formula": "Lord of the weekday on Virgo ingress (Kanya Sankranti)",
            "domain": "Wealth accumulation, trade profits, economic prosperity, treasury",
            "associated_horoscope": "Dhanesh Horoscope — cast for Sun's entry into Virgo",
            "planet_outcomes": {
                "Sun":     "Businessmen earn good profits in trade. Traders of cows, buffalos, horses earn very well.",
                "Moon":    "Wealth accumulated by buying and selling. More profits in trade. Traders of clothes, rice, ghee, oils, juices and perfumes earn well particularly. Rulers equipped with means of comforts.",
                "Mars":    "Rains untimely. Crops of wheat and gram damaged. Trades remain unstable. People suffer due to oppressive policies of administration. Selling of goods profitable in Margsheersh.",
                "Mercury": "Accumulation of goods profitable. Farmers earn well. Religious persons remain busy in religious rituals.",
                "Jupiter": "Businessmen live with comforts. Produce of fruits and flowers good. People are rich, comfortable and religious.",
                "Venus":   "All people blessed with money and goods. Traders have satisfaction. Rulers perform their duties honestly.",
                "Saturn":  "Rulers remain worried and ill. Traders and farmers have paucity of funds. Scholars too have many problems."
            }
        },
        result=(
            "Identify the lord of weekday on Virgo ingress. Mercury, Jupiter or Venus as Dhanesh → strong "
            "trade year. Mars or Saturn → trade disruption and economic stress. Cross-reference with King "
            "planet for overall economic picture."
        ),
        synthesis_sources=["gaur_aifas_ch2"],
        checkable=False
    ),

    _rule(
        rule_id="mundane-gaur-ch2-durgesh-outcome-matrix",
        sub_type="celestial_council_durgesh",
        title="Durgesh (Lord of Defence and Security) Planet Outcome Matrix",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "official": "Durgesh — Lord of Security and Defence",
            "appointment_formula": "Lord of the weekday on Leo ingress (Simha Sankranti)",
            "domain": "Defence, military, law enforcement, national security",
            "associated_horoscope": (
                "Durgesh Horoscope — cast for Sun's entry into Leo. "
                "If benefic planets in ascendant or aspecting it: administration efficient. "
                "If malefics on ascendant: adverse and oppressive rule."
            ),
            "planet_outcomes": {
                "Sun":     "Rulers improve legal system and general administration. Justice available to everyone in royal court. Administrators work honestly.",
                "Moon":    "Rulers rule with ethics. Comforts and luxuries of people increase. Sugarcane and dairy products abundant. Diseases less. However bitterness between rulers and senior officials.",
                "Mars":    "People suffer due to wrong conduct of rulers or national calamities. Traders operate under fear due to government policies and do not earn profits due to oppressive laws.",
                "Mercury": "People have happiness-sorrows together. Land army and navy strengthened. People have safety in journeys. Incidents of theft and robberies less. Rulers use diplomacy.",
                "Jupiter": "Rulers maintain law and administration efficiently. Cities and villages have general amenities. Armed forces strengthened.",
                "Venus":   "Senior administrators have comforts and amenities. Traders and important persons live lavishly.",
                "Saturn":  "People have to leave their homes due to war. Suffer due to humiliations meted out by enemies. Ripe crops damaged by locusts and rats."
            }
        },
        result=(
            "Identify the lord of weekday on Leo ingress. Mars or Saturn as Durgesh → national security "
            "crises, oppressive administration. Jupiter or Mercury → strong defence with diplomacy. "
            "When both King and Durgesh are malefics — war scenario heightened."
        ),
        synthesis_sources=["gaur_aifas_ch2"],
        checkable=False
    ),
]

# ═════════════════════════════════════════════════════════════════════════════
# GROUP Q — Gaur Ch 2: Cloud and Snake Auxiliary Forecast Rules
# ═════════════════════════════════════════════════════════════════════════════
GROUP_Q = [

    _rule(
        rule_id="mundane-gaur-ch2-nava-megha-cloud-forecast",
        sub_type="rainfall_auxiliary",
        title="Nava Megha (Nine Clouds) — Auxiliary Rainfall Forecast",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "formula": "Multiply Shak Samvat by 8, divide by 9. Remainder = cloud type (1–9).",
            "cloud_types": {
                "1_Aavart":  "Rains less. Crops of wheat, barley, rice, cotton damaged.",
                "2_Samvart": "Rains sufficient. Winds in East. Immoral acts more.",
                "3_Pushkar": "Rains less. People suffer due to diseases. Fruits and vegetables insufficient.",
                "4_Dron":    "Rains good and timely. All persons flourish. Government treasures full.",
                "5_Kaal":    "Rains insufficient. Affluent people comfortable. Rulers have acrimony.",
                "6_Neel":    "Rains good and sufficient. People rich and satisfied. Crops of cotton good.",
                "7_Varun":   "Rains good and timely. Amenities of people good. Religious persons respected.",
                "8_Vayu":    "Rains less. All crops of grains damaged. Accumulated grains get depleted.",
                "9_Tam":     "Rains less and diseases more. Produce of crops reduced. People suffer."
            },
            "good_rain_signal": "Clouds 2, 4, 6, 7 → adequate to good rainfall",
            "poor_rain_signal": "Clouds 1, 3, 5, 8, 9 → below-average to poor rainfall"
        },
        result=(
            "Use as auxiliary cross-check alongside Meghesh planet forecast. If both Meghesh "
            "and cloud type indicate poor rain — drought signal confirmed. If both indicate good "
            "rain — abundant monsoon signal."
        ),
        synthesis_sources=["gaur_aifas_ch2"],
        notes="Engine spec gaur-ch2-nine-clouds holds the full lookup table.",
        checkable=False
    ),

    _rule(
        rule_id="mundane-gaur-ch2-dvadasha-sarpa-snake-forecast",
        sub_type="rainfall_auxiliary",
        title="Dvadasha Sarpa (Twelve Snakes) — Auxiliary Rainfall and Security Forecast",
        source_chapter="Gaur Ch 2 — The Celestial Council",
        condition={
            "formula": "Add 2 to Shak Samvat, divide by 12. Remainder = snake type (1–12).",
            "notable_signals": {
                "3_Kakotak":  "Rains less. Mourning due to death of a senior ruler — leader mortality signal.",
                "6_Takshak":  "Rains medium. Friction between two countries creates hostile atmosphere — war signal.",
                "7_Kambal":   "Rains and crops poor.",
                "8_Ashwatar": "Rains scanty and drought.",
                "2_Nandsari": "Rains more. People enjoy more comforts and luxuries.",
                "5_Vasuki":   "Rains good. Crops good.",
                "9_Hemamali": "Rains more and grains produced more.",
                "10_Narendra":"Rains sufficient and timely at all places — universal abundance."
            },
            "good_rain_snakes": [2, 5, 9, 10],
            "poor_rain_snakes": [3, 4, 7, 8, 11, 12]
        },
        result=(
            "Use as third auxiliary check alongside Meghesh planet and Cloud type. Three-way "
            "convergence (Meghesh + Cloud + Snake all indicating poor rain) = strong drought "
            "alert. Kakotak (3) or Takshak (6) years need enhanced political monitoring."
        ),
        synthesis_sources=["gaur_aifas_ch2"],
        notes="Engine spec gaur-ch2-twelve-snakes holds the full lookup table.",
        checkable=False
    ),
]

# ═════════════════════════════════════════════════════════════════════════════
# GROUP R — Mehta Ch 13: Eclipse Interpretation Rules
# ═════════════════════════════════════════════════════════════════════════════
GROUP_R = [

    _rule(
        rule_id="mundane-mehta-ch13-eclipse-fiery-signs",
        sub_type="eclipse_rashi_effect",
        title="Eclipse in Fiery Signs — Political and Military Effects",
        source_chapter="Mehta/Rao Ch 13 — Eclipses",
        condition={
            "trigger": "Solar or lunar eclipse occurring in a fiery sign (Aries, Leo, Sagittarius)",
            "aries": "People of Panchala, Kalinga, Suraswna, Kambojas (modern Orissa), hunters, warriors, those who work on fire will come to grief.",
            "leo": "Destroys tribe of hunters, people inhabiting Mekala mountains, heroic persons, rulers or their equals as well as people in forests. Leo is also animal sign — danger to animals, zoo, wildlife sanctuaries.",
            "sagittarius": "Destroys chief ministers, horses, people of Videhas, Panchalas, physicians, merchants, those rough and tough who wield weapons. Sagittarius is war like sign — brings trouble to some notable personality or ruler (may be his death or murder). Fires, diseases, shortage of food, movement of armies, discontentment among people."
        },
        result=(
            "Eclipse in Aries → Orissa/North India military/civil conflict. "
            "Eclipse in Leo → rulers, forest regions, wildlife at risk; leadership crisis. "
            "Eclipse in Sagittarius → death or serious trouble to key leader/minister; fire disasters; food shortage."
        ),
        synthesis_sources=["mehta_rao_ch13", "raphael_west_ch23"],
        severity="high",
        checkable=True
    ),

    _rule(
        rule_id="mundane-mehta-ch13-eclipse-earthy-signs",
        sub_type="eclipse_rashi_effect",
        title="Eclipse in Earthy Signs — Agricultural and Economic Effects",
        source_chapter="Mehta/Rao Ch 13 — Eclipses",
        condition={
            "trigger": "Solar or lunar eclipse occurring in an earthy sign (Taurus, Virgo, Capricorn)",
            "taurus": "Trouble to shepherds, cattle, owners of large herds; men who have risen to prominence will suffer.",
            "virgo": "Afflict crops, poets, writers, musicians, people of Asmaka region as well as countries abounding in paddy fields. Virgo is 6th sign (natural house of disease) — eclipses here would cause diseases, accidents, epidemics and matters related to public health and labour disputes.",
            "capricorn": "Affect fishes, ministers and their families, men of low classes, those skilled in charms, those who are old and infirm, those who live by weapons. Droughts, famines, earthquakes and mining disasters."
        },
        result=(
            "Eclipse in Taurus → cattle/livestock crisis; India's lagna sign — heightened national significance; "
            "established personalities lose prominence. "
            "Eclipse in Virgo → crop failure, public health crisis, labour unrest. "
            "Eclipse in Capricorn → drought, famine, earthquake, mining disaster; ministerial crisis."
        ),
        synthesis_sources=["mehta_rao_ch13"],
        severity="high",
        notes="Taurus eclipse has special significance for India as Taurus is India's traditional lagna.",
        checkable=True
    ),

    _rule(
        rule_id="mundane-mehta-ch13-eclipse-airy-watery-signs",
        sub_type="eclipse_rashi_effect",
        title="Eclipse in Airy and Watery Signs — Social and Maritime Effects",
        source_chapter="Mehta/Rao Ch 13 — Eclipses",
        condition={
            "trigger": "Solar or lunar eclipse occurring in an airy or watery sign",
            "gemini":    "High class women, kings and powerful ministers, persons proficient in arts, people living on banks of Yamuna, people of Balkh, Viratas and Suhmas would be affected.",
            "libra":     "People of Avanti and Apranta region (western borders near Sahya mountains), virtuous persons, traders, inhabitants of Dasarna country, Maru and Kacchaps regions will come to grief.",
            "aquarius":  "Harm people living on mountains and in west, bearers of burden, thieves, herdsmen, noblemen, residents of Simhapura and Barbaras. Wind storms, famines, sickness, destruction of cattle and sheep.",
            "cancer":    "Abhiras, Sabaras, Pallavas, Matsayas, Kurus, Sakas, Panchalas will suffer.",
            "scorpio":   "People of Udumbars, Madra and Chola, Yudheya tribes fighters and trees will be destroyed.",
            "pisces":    "Effect shores of ocean, pearls, sea bed, foresters, scholars; destruction of fish and sea food; much mortality among common people; trouble for people living around sea."
        },
        result=(
            "Airy sign eclipses → affect communication, trade routes, arts community, western borders. "
            "Watery sign eclipses → maritime disasters, fishing industry, coastal populations, epidemic risk. "
            "Eclipse in Satabhisha nakshatra (regardless of sign) → affects ministers, scientists, "
            "laboratories, stock exchanges, traders, factories and air travel."
        ),
        synthesis_sources=["mehta_rao_ch13"],
        severity="medium",
        checkable=True
    ),

    _rule(
        rule_id="mundane-mehta-ch13-eclipse-lord-placement",
        sub_type="eclipse_lord_rule",
        title="Eclipse Sign Lord Placement — Amplification Rule",
        source_chapter="Mehta/Rao Ch 13 — Eclipses",
        condition={
            "rule": "Study the lord of the sign in which the eclipse occurs.",
            "8th_house_placement": "Eclipse sign lord in 8th house → serious deaths and accidents.",
            "6th_house_placement": "Eclipse sign lord in 6th house → may cause diseases.",
            "3rd_house_placement": "Eclipse sign lord in 3rd house → rail, road and air accidents or strikes in railways.",
            "malefic_lord": "Malefic lord of eclipse sign → worse trouble.",
            "benefic_lord": "Benefic lord of eclipse sign → lesser problems.",
            "total_eclipse_with_malefic_aspect": "If eclipse is total AND the eclipsed orb is aspected by malefics — famine and pestilence all over the country."
        },
        result=(
            "After identifying eclipse sign, check its lord's natal house position in the national "
            "horoscope. 8th placement = death/accident signal. 3rd placement = transport crisis. "
            "Total eclipse + malefic aspect = national famine/pestilence trigger."
        ),
        synthesis_sources=["mehta_rao_ch13"],
        severity="high",
        checkable=True
    ),

    _rule(
        rule_id="mundane-mehta-ch13-eclipse-ruler-royalty",
        sub_type="eclipse_leader_effect",
        title="Eclipse Effects on Rulers and Royalty — Positive and Negative Outcomes",
        source_chapter="Mehta/Rao Ch 13 — Eclipses",
        condition={
            "timing": "Events may happen within 4 months of solar eclipse and a week of lunar eclipse. Events may happen prior to eclipse also.",
            "auspicious_rule": "Eclipse on or in opposition to natal Sun, Moon or ascendant of a ruler → mostly auspicious; elevation to power or good fortune.",
            "auspicious_examples": [
                "Duke of York: natal Sun fell on eclipse 13 Dec 1936 → became King George VI",
                "Frank Roosevelt: solar eclipse on ascendant Aug 1932 → elected President Nov 1932",
                "Harry Truman: solar eclipse on natal Sun 9 May 1948 → elected President Nov 1948"
            ],
            "inauspicious_rule": "Eclipse afflicted by BOTH Mars and Saturn → ominous for causing death by assassination.",
            "inauspicious_examples": [
                "Mahatma Gandhi: assassinated 30 Jan 1948 following solar eclipse on his natal Mars on 12 Nov 1947",
                "Indira Gandhi: solar eclipse 25 May 1984 in Taurus opposite natal Sun; ecliptic point aspected by retrograde Mars conjunct retrograde Saturn in Libra; ecliptic point in Rohini nakshatra — assassinated 31 Oct 1984",
                "Abraham Lincoln: lunar eclipse 11 Apr 1865 fell on natal Mars; solar eclipse 19 Oct 1865 — shot dead 14 Apr 1865",
                "JFK: solar eclipse on natal 4/10 axis; explosive Mars on ecliptic point — assassinated four months later"
            ],
            "opposition_principle": "Eclipse on natal Moon → sometimes gives opposite result (fall from power). Morarji Desai: eclipse on natal Moon Jan 1979 → fell from power as PM Aug 1979.",
            "nations_rule": "Two eclipses within a fortnight → means war."
        },
        result=(
            "For any ruling leader: check if current eclipse falls on/opposite natal Sun, Moon or ascendant. "
            "If ON these points AND aspected by both Mars and Saturn → assassination or death in office signal. "
            "If only in opposition with benefic involvement → elevation. Two eclipses in 15 days → war imminent."
        ),
        synthesis_sources=["mehta_rao_ch13", "raphael_west_ch25"],
        severity="critical",
        checkable=True
    ),

    _rule(
        rule_id="mundane-mehta-ch13-eclipse-national-validation",
        sub_type="eclipse_empirical_case",
        title="Eclipse National Impact — India Empirical Validations (Mehta/Rao)",
        source_chapter="Mehta/Rao Ch 13 — Eclipses",
        condition={
            "india_1983_rule": (
                "Solar eclipse 11 June 1983 in Taurus sign with Mars in it — "
                "eclipse falling on India's ruling Taurus lagna sign shows grave political developments, "
                "affliction to cattle, loss of agriculture, pest attack, scanty rainfall. "
                "1983-84 was worst period for India: Punjab communal situation, Bhindrawale insurgency."
            ),
            "india_1995_rule": (
                "Solar eclipse 24 Oct 1995 07:22 in Libra — 10th house from Capricorn (India's traditional rashi). "
                "Result: delayed monsoon Kharif 1995, shortfall of food grains to 180.4 million tonnes, "
                "shortfall in wheat production by 3 million tonnes. General election May 1996 total chaos — "
                "no government could form majority."
            ),
            "nepal_2001_rule": (
                "Lunar eclipse 10 Jan 2001 at 00:12 AM fell on 4/10 axis of Nepal's coronation horoscope (24 Feb 1975). "
                "10th lord Jupiter with retrograde Saturn aspected by retrograde Mars from Libra. "
                "Retrograde malefics cause blood-curdling events. "
                "King Birendra and family brutally murdered by own son Dipendra — 1 June 2001."
            ),
            "sanjay_gandhi_rule": "Eclipse falling in 8th house whether solar or lunar generally causes disaster — Sanjay Gandhi died in aircrash 23 June 1980."
        },
        result=(
            "Eclipse in India's lagna sign Taurus or 10th from traditional Capricorn rashi → "
            "major political disruption + agricultural crisis for India. "
            "Eclipse on 4/10 axis of any nation's horoscope with retrograde malefics → "
            "leadership assassination or violent regime change."
        ),
        synthesis_sources=["mehta_rao_ch13"],
        severity="critical",
        checkable=True
    ),
]

# ═════════════════════════════════════════════════════════════════════════════
# GROUP S — Mehta Ch 20: Terrorism Astrological Parameters
# ═════════════════════════════════════════════════════════════════════════════
GROUP_S = [

    _rule(
        rule_id="mundane-mehta-ch20-terrorism-ten-parameters",
        sub_type="terrorism_composite_gate",
        title="Terrorism Astrological Gate — 10 Parameters (K.N. Rao)",
        source_chapter="Mehta/Rao Ch 20 — Terrorism: An Astrological Explanation",
        condition={
            "source_article": "K.N. Rao in Journal of Astrology, July-September 2002",
            "parameter_1": "Combination of Mars with Rahu/Ketu — together, in opposition, or in kendras from each other.",
            "parameter_2": "Combination of Saturn-Rahu conjunction, opposition or in square. 'When Saturn and Rahu join together, anarchical conditions and nihilistic philosophy gets accepted. Religious fundamentalism of extreme form gets noticed.'",
            "parameter_3": "Combination of Saturn and Mars conjunction, opposition or in square. 'Saturn or Mars opposition few months before or during Saturn-Rahu conjunction, Mars ignites it all.'",
            "parameter_4": "Affliction to Sun.",
            "parameter_5": "Affliction to Moon. When under influence of Saturn and Rahu — signal acceptance of nihilistic philosophy, slogans and actions of extreme cruelty. When all four Rahu, Saturn, Sun and Moon join together in a rashi — society or country becomes aware of their presence. When other planets join them chaos is immense.",
            "parameter_6": "Saturn or Rahu in Rohini nakshatra OR alternatively in Taurus rashi.",
            "parameter_7": "Benefic planets like Jupiter, Venus or Mercury relegated to secondary role with no power to provide protective shield. 'It is generally noticed that around the time terrorist activities become explosive, Jupiter the planet of idealism gets afflicted or even a guru-chandal yoga is formed showing eclipse of idealism.'",
            "parameter_8": "Retrograde Mars and Saturn become more sinister and deadly and provide maximum damage. 'Special study is to be done of retrograde Mars, this is a precursor of evil events. Whenever wars take place or break out Mars has been found to be retrograde — seems to be pre-condition to outbreak of war.'",
            "parameter_9": "Role of eclipses to be watched as these last for a long time. Timing of affliction of eclipse point should be carefully noted.",
            "parameter_10": "Degrees of closeness of planets should be clearly observed — degree-wise proximity magnifies effects.",
            "activation_threshold": "Minimum 4 parameters active simultaneously for serious terrorist event alert. 6+ parameters = catastrophic event signal."
        },
        result=(
            "When 4+ parameters are simultaneously active in any national or world chart, "
            "increased terrorist activity is indicated. When 6+ parameters converge with an eclipse "
            "active within 4 months — catastrophic multi-casualty event risk. Parameters 1+2+3+6 "
            "together constitute the core terror quartet. When parameter 8 (retrograde Mars) is also "
            "active, the event is likely to involve military-grade coordination and mass casualties."
        ),
        synthesis_sources=["mehta_rao_ch20", "mehta_rao_ch19", "gopal_modern_ch8"],
        severity="critical",
        checkable=True
    ),

    _rule(
        rule_id="mundane-mehta-ch20-nine-eleven-validation",
        sub_type="terrorism_empirical_case",
        title="9/11 WTC New York — Astrological Validation (11 Sept 2001, 9:00 AM)",
        source_chapter="Mehta/Rao Ch 20 — Terrorism",
        condition={
            "event": "September 11, 2001 suicide planes attack on World Trade Centre and Pentagon, New York, 9:00 AM",
            "chart_features": {
                "saturn_rohini": "Saturn in Rohini Nakshatra — evil position causing wars, riots, strife, earthquakes (Parameter 6 ✓)",
                "mars_ketu_sagittarius": "Two explosive planets Mars and Ketu together in Sagittarius (4th house — property, buildings). Mars and Ketu bringing fire and destruction. Very close to each other degree wise. Sagittarius is war-like rashi (Parameter 1 ✓)",
                "ketu_secrecy": "Ketu is planet of secrecy and is a spy — conspiracy hatched in secrecy.",
                "rahu_aspect_4th": "Rahu aspects 4th house from above combination; Rahu is Muslim, with Jupiter becomes fundamentalist. Rahu is also air — attack coming from air (Parameter 2 partial ✓)",
                "rahu_mars_ketu_moon": "Rahu, Mars and Ketu are afflicting luminary Moon (Parameter 5 ✓)",
                "jupiter_afflicted": "Jupiter afflicted by Rahu and Mars; great benefic in 6th enemy house (Parameter 7 ✓)",
                "sun_12th_saturn": "Sun in 12th house squared by Saturn; degree wise Sun and Saturn very close (Parameter 4 ✓)",
                "usa_gemini_lagna": "If taking Gemini as lagna of USA — totally afflicted with Saturn in 12th house",
                "full_moon_2_sep_2001": "Full Moon 2.9.2001 17:45 Washington: 12th house has Mars and Ketu — terrorists have entered country to inflict damage; lord of 4th house gone to 12 with two fiery planets for destruction"
            },
            "parameters_active": [1, 2, 4, 5, 6, 7],
            "parameter_count": 6
        },
        result=(
            "6 of 10 terrorism parameters were active simultaneously. Saturn in Rohini + Mars-Ketu in "
            "Sagittarius 4th house + Rahu affliction of Moon + Jupiter in 6th with Rahu = full terrorism "
            "gate activated. Historical validation: 9/11 WTC attack confirmed this parameter set as "
            "catastrophic event trigger. Also validated: Saturn-Rohini nakshatra = wars, riots, earthquakes."
        ),
        synthesis_sources=["mehta_rao_ch20", "gopal_modern_ch8"],
        severity="critical",
        checkable=True
    ),

    _rule(
        rule_id="mundane-mehta-ch20-madrid-london-validation",
        sub_type="terrorism_empirical_case",
        title="Madrid (11.03.2004) and London (07.07.2005) — Transport Terror Validation",
        source_chapter="Mehta/Rao Ch 20 — Terrorism",
        condition={
            "madrid_11_03_2004": {
                "features": [
                    "Conjunction of Mars and Rahu in 3rd house (rail and communication) — Parameter 1 ✓",
                    "Ketu and Moon in 9th house of religion",
                    "4th lord of vehicles Venus is with Rahu",
                    "Moon in house of religion afflicted from Ketu (spies/fundamentalists) as well as Mars and Rahu — Parameter 5 ✓",
                    "Jupiter retrograde and afflicted by Saturn — Parameter 7 ✓",
                    "Venus (planet of vehicles) under affliction by Mars and Rahu",
                    "Mercury debilitated and under affliction from Saturn"
                ],
                "result_correlation": "Train bombings at Atocha station — 191 people killed, more than 1800 wounded in simultaneous explosions at three Madrid stations. Mars-Rahu in 3rd house (railways) = railway bomb attack."
            },
            "london_07_07_2005": {
                "features": [
                    "Conjunction of Rahu and Mars in 8th house, almost at the same degree — Parameter 1+3 ✓",
                    "Cluster of four planets in 12th house; Venus and Mercury at same degree",
                    "Saturn afflicting Moon, Venus, Mercury as well as Jupiter — Parameter 3 partial ✓",
                    "Jupiter under heavy affliction of Ketu, Mars, Rahu and Saturn — Parameter 7 ✓",
                    "Sun afflicted by Mars from 8th house — Parameter 4 ✓",
                    "Mars (lord of 4th house vehicles) in 8th afflicted by Rahu (Muslim-Terrorist)",
                    "Venus (lord of 3rd — communication, rail) in 12th afflicted by Saturn"
                ],
                "new_moon_06_07": "Mars and Rahu in 7th house of death, degrees very close (Mars 22°, Rahu 24°); Mercury, Venus, Jupiter all at 16° — three planets at same degree; Rahu combination = Mercury (communication) + Venus (vehicles) + Saturn (death) = communication/vehicle death combination",
                "result_correlation": "Underground train and bus bombings 7 July 2005. Striking similarity to Madrid: both at morning rush hour for maximum damage. Mars-Rahu in 8th house (death) through vehicles confirmed."
            },
            "transport_terror_signature": "Mars-Rahu/Ketu in or aspecting the 3rd house (communication/transport) or 4th lord afflicted by Rahu-Mars = transport system terror attack signature."
        },
        result=(
            "Transport terror signature: Mars + Rahu/Ketu in 3rd house or aspecting 3rd/4th lord of vehicles = "
            "train/bus/air vehicle attack. When Saturn also afflicts communication houses (3rd, 12th) "
            "simultaneously with Mars-Rahu = mass casualty transport attack. Both Madrid and London "
            "validated this parameter constellation."
        ),
        synthesis_sources=["mehta_rao_ch20"],
        severity="critical",
        checkable=True
    ),

    _rule(
        rule_id="mundane-mehta-ch20-india-temple-attack-signature",
        sub_type="terrorism_empirical_case",
        title="India Temple/Religious Site Attack Signature (Ayodhya 5 July 2005)",
        source_chapter="Mehta/Rao Ch 20 — Terrorism",
        condition={
            "trigger_pattern": {
                "Jupiter_affliction": "Planet of religion Jupiter under heavy affliction from Ketu (secret spies), Rahu (Islamic extremists), Mars (violence) and Saturn (death and outcasts) — Parameter 7 ✓",
                "9th_house_affliction": "9th house of religion afflicted by Saturn — Parameter 3 partial ✓",
                "mars_8th_with_rahu_ketu": "Lord of 4th and 9th (religious place) Mars in house of accidents and death (8th) with Rahu and Ketu — Parameter 1 ✓",
                "saturn_12th": "Saturn in 12th house → terrorists have entered the country from outside India",
                "sun_moon_mars": "Sun and Moon under affliction by Mars — Parameters 4 and 5 ✓"
            },
            "navamsha_protection": (
                "Answer in navamsha, if lagna is very strong with Jupiter in lagna and directional strength, "
                "with aspect of three benefics, and no affliction to Sun or Moon in navamsha — the attack "
                "may fail or cause less damage than intended. Saturn with Ketu in 4th aspected by Rahu "
                "still does damage to the psyche of the nation even if attack partially foiled."
            ),
            "event": "Ayodhya Ram Janam Bhoomi temple attack, 5 July 2005, 8:46 AM"
        },
        result=(
            "Religious site attack signature: Jupiter heavily afflicted by all four malefics (Rahu, Ketu, Mars, "
            "Saturn) + 9th house Saturn affliction + Mars in 8th with nodes = high risk of temple/mosque/religious "
            "site attack. Saturn in 12th = foreign-origin terrorists infiltrated. Strong navamsha lagna may "
            "partially protect. Cross-reference with Mehta Ch 21 (religious leader hazard) rules."
        ),
        synthesis_sources=["mehta_rao_ch20", "mehta_rao_ch21"],
        severity="critical",
        checkable=True
    ),

    _rule(
        rule_id="mundane-mehta-ch20-delhi-bombs-national-affliction",
        sub_type="terrorism_empirical_case",
        title="Delhi Bomb Blasts (13.09.2008) — India National Chart Affliction Pattern",
        source_chapter="Mehta/Rao Ch 20 — Terrorism",
        condition={
            "event": "Serial bombing in Delhi 13.09.2008 18:10",
            "observations": {
                "saturn_afflicts_india_lagna": "Saturn afflicting Sun, Moon and Taurus lagna of independent India — direct attack on India's core",
                "simha_papkartari": "Simha rashi (responsible for bringing down fortress of Delhi) afflicted and in Papkartari yoga",
                "capricorn_rahu": "Capricorn rashi of India afflicted by Rahu",
                "benefics_mars_afflicted": "Benefic planets Mercury, Venus and Jupiter all afflicted by Mars — complete protective shield collapsed",
                "grah_yudha": "Mars, Mercury and Venus in grah yudha (planetary war at same degree 22-23°)",
                "saturn_jupiter_close": "Saturn and Jupiter also close degree wise — macro-conjunction active"
            },
            "india_signature": (
                "When Saturn simultaneously afflicts India's Taurus lagna + afflicts Sun and Moon "
                "in India's chart + Capricorn rashi (traditional sign of India) gets Rahu affliction "
                "+ all three benefics simultaneously afflicted by Mars = maximum national vulnerability "
                "window for major terror attack on India's capital."
            )
        },
        result=(
            "India national attack trigger: Saturn on Taurus lagna AND Rahu on Capricorn rashi AND "
            "all benefics (Mercury, Venus, Jupiter) simultaneously afflicted by Mars in grah yudha "
            "= maximum national vulnerability window. Capital (Delhi) under direct attack risk when "
            "Simha rashi is in Papkartari yoga."
        ),
        synthesis_sources=["mehta_rao_ch20"],
        severity="critical",
        checkable=True
    ),
]

# ═════════════════════════════════════════════════════════════════════════════
# GROUP T — Mehta Ch 26: Political Party Dasha Framework
# ═════════════════════════════════════════════════════════════════════════════
GROUP_T = [

    _rule(
        rule_id="mundane-mehta-ch26-party-dasha-framework",
        sub_type="political_party_dasha",
        title="Political Party Horoscope — Vimshottari Dasha Analysis Framework",
        source_chapter="Mehta/Rao Ch 26 — Political Parties of India",
        condition={
            "method": "Cast horoscope for exact founding date, time and place of the political party. Apply Vimshottari dasha system.",
            "key_houses": {
                "10th": "Power and governance — strength here = ability to form government",
                "8th": "Transformation, death, loss — afflictions here = loss of power, scandal",
                "2nd_7th": "Marka houses — marka dasha lords can cause party's decline or leadership death",
                "5th": "Intelligence and strategy",
                "11th": "Parliament seats and alliances",
                "12th": "Hidden enemies, losses, expenditure"
            },
            "dasha_principles": {
                "debilitated_dasha_lord": "Debilitated planet as dasha lord brings setbacks in that house's domain",
                "retrograde_malefic": "Retrograde malefic as dasha lord becomes more evil — retrograde Mars caused Indira Gandhi's murder",
                "rahu_ketu_dasha": "Rahu/Ketu dashas = unpredictable, foreign connections, violent events for the party",
                "saturn_12th_from_maha": "If Saturn is 12th from Mahadasha lord → party loses power during that antardasha",
                "jupiter_own_10th": "Jupiter aspecting its own 10th house = retained political power even if truncated",
                "rajayoga_indicators": "Jupiter as both lord of 9th and 10th in kendra = rajayoga for the party"
            },
            "cross_reference": "Always combine party chart with national horoscope and the ruling leader's personal chart"
        },
        result=(
            "Apply full Vimshottari dasha analysis to party's founding chart. Dasha lord in 8th or "
            "marka role → leadership crisis or loss of power. Retrograde malefic dasha = internal party "
            "violence, leader assassination risk. Jupiter aspecting own 10th = party retains relevance "
            "even in opposition. Saturn 12th from Mahadasha lord = power loss in that sub-period."
        ),
        synthesis_sources=["mehta_rao_ch26"],
        checkable=False
    ),

    _rule(
        rule_id="mundane-mehta-ch26-congress-i-dasha-history",
        sub_type="political_party_empirical",
        title="Indian National Congress-I — Dasha-Event Historical Validation",
        source_chapter="Mehta/Rao Ch 26 — Political Parties of India",
        condition={
            "party_birth": "Congress-I (Indira Congress): 2 January 1978, Lagna 15°01'",
            "balance_at_birth": "Moon Mahadasha",
            "key_correlations": {
                "Moon_dasha": "Elections Jan 1980 — won 351 of 524 seats (landslide). But tragedy too: Sanjay Gandhi's death 23 June 1980 in air accident. Moon 9th lord in 7th-10th from 10th house (padh prapti yoga). Mercury 6th lord (antardasha) aspects its own 11th house (gains).",
                "Mars_dasha_1984_1991": "Mars debilitated in 5th house (10th from 8th). Indira Gandhi brutally murdered 31 October 1984 by own bodyguards. Mars planet of violence and lord of marka house. Being retrograde becomes more evil. Murderers were fanatic Sikhs — Mars also represents southern direction.",
                "Rahu_dasha_1991_2009": "Rahu in Virgo (sometimes used for signs of India). Both good and bad period. On 21.05.1991 in Rahu/Rahu chidra dasha, Congress lost leader Rajiv Gandhi who was assassinated — violent death to leader when Rahu is with Moon in 7th (marka house). From 1996 Saturn (12th from Rahu) dasha: Congress lost power. Jupiter dasha 2009 — Jupiter aspects own 10th house, assured political power though truncated.",
                "Venus_antardasha_signaling": "Venus as 3rd lord (karka of satellites) in 10th with Sun (directional strength) = India space age and nuclear test 1974 under Moon/Venus period"
            }
        },
        result=(
            "Congress-I empirical model confirms: retrograde malefic (Mars R) as Mahadasha lord = "
            "founder's violent assassination (Indira Gandhi 1984). Rahu chidra dasha = second leadership "
            "assassination (Rajiv Gandhi 1991). Saturn 12th from Mahadasha lord = loss of government power. "
            "Jupiter aspect on own 10th = sustained political relevance despite coalition dependency."
        ),
        synthesis_sources=["mehta_rao_ch26"],
        severity="high",
        checkable=False
    ),

    _rule(
        rule_id="mundane-mehta-ch26-bjp-dasha-history",
        sub_type="political_party_empirical",
        title="Bhartiya Janata Party (BJP) — Dasha-Event Historical Validation",
        source_chapter="Mehta/Rao Ch 26 — Political Parties of India",
        condition={
            "party_birth": "BJP: 6 April 1980, 11:45, Delhi. Lagna 23°36'.",
            "key_correlations": {
                "Mercury_Saturn_antardasha_1984": "BJP obtained only 2 seats of 543 in 1984 elections. Mercury (lagna lord) in Rahu/Ketu axis, aspected by malefics Mars and Saturn. Mercury/Saturn antardasha — Mercury lagna lord with Ketu; Saturn is 8th and 9th lord afflicted by Mars.",
                "Ketu_Jupiter_1989": "BJP won 88 seats. Ketu in 9th house with lagna lord Mercury while Jupiter is 10th lord. Ketu/Jupiter antardasha — 9th and 10th lords active.",
                "Venus_Sun_1996": "BJP became single largest party. Venus/Sun — Sun in 10th house but dispositor Jupiter badly afflicted in 3rd by Saturn; Jupiter also placed in 6th from Sun. Vajpayee resigned after 13 days.",
                "Venus_Mars_Venus_Rahu_1998_2002": "NDA simple majority. Nuclear tests at Pokhran 1998 — Mars and Rahu in 10th house raised India's stature. Parliament attack and Tehelka scam (Rahu represents Muslims, foreigner; Mars in 10th with Rahu = violence against Parliament).",
                "Venus_Jupiter_2004": "Elections 2004, BJP and allies won only 185 vs 217 by Congress — lost mandate. Jupiter is 8th and 11th lord from Venus, hence malefic for Venus.",
                "Venus_Saturn_2005_2008": "Revival period. Venus forming mahapurush yoga (malviya yoga) from Moon. Saturn is 10th lord from Venus — Saturn aspects own 10th from Venus, creating another rajayoga."
            }
        },
        result=(
            "BJP empirical model confirms: lagna lord in Rahu/Ketu axis with malefic aspect = minimal "
            "electoral performance. Ketu/Jupiter antardasha with 9th-10th lords = electoral breakthrough. "
            "Antardasha lord as 8th lord from Mahadasha = electoral loss. Rajayoga (malviya yoga from Moon "
            "+ Saturn aspecting own 10th) = political revival. Mars-Rahu in 10th = military action + scandal."
        ),
        synthesis_sources=["mehta_rao_ch26"],
        severity="high",
        checkable=False
    ),

    _rule(
        rule_id="mundane-mehta-ch26-retrograde-malefic-dasha-crisis",
        sub_type="political_leadership_death",
        title="Retrograde Malefic Dasha → Political Leader Assassination / Violent Death",
        source_chapter="Mehta/Rao Ch 26 — Political Parties of India",
        condition={
            "primary_rule": (
                "When a retrograde malefic planet (Mars R, Saturn R, Rahu — always retrograde) "
                "is the active Mahadasha or Antardasha lord in a political party's chart or "
                "a national leader's personal chart, it becomes MORE evil than a direct malefic "
                "and can cause violent death of the party's founding leader."
            ),
            "mars_retrograde_rule": (
                "Mars retrograde as Mahadasha lord: Mars is planet of violence and lord of marka "
                "house. Being retrograde it becomes more evil. If also debilitated — maximum danger. "
                "Indira Gandhi murder: Congress-I chart Mars R in 5th (10th from 8th, marka placement). "
                "Murderers carried out revenge — Mars directional signification of south confirmed."
            ),
            "rahu_chidra_dasha_rule": (
                "Rahu chidra dasha (Rahu/Rahu sub-period) is the transition antardasha before Rahu "
                "Mahadasha ends. If Rahu is with Moon in a marka house (2nd or 7th), the chidra "
                "dasha period carries violent death risk for the party leader. "
                "Rajiv Gandhi assassination: Rahu/Rahu chidra dasha, Rahu with Moon in 7th (marka) — "
                "Rajiv Gandhi assassinated 21.05.1991 in suicidal attack."
            ),
            "compound_signal": (
                "If BOTH the Mahadasha lord is retrograde malefic AND the party's 8th house (or "
                "marka lords 2nd/7th) is afflicted in the national horoscope simultaneously → "
                "leadership assassination risk window."
            )
        },
        result=(
            "Monitor: (1) Is the current Mahadasha lord of the party chart a retrograde malefic? "
            "(2) Is the leader's personal chart also showing marka dasha? (3) Is India's national "
            "chart simultaneously showing 8th lord activation or Rahu-marka-house conjunction? "
            "Triple convergence = very high risk of leader assassination or sudden violent death. "
            "Single signal alone = heightened vigilance only."
        ),
        synthesis_sources=["mehta_rao_ch26", "mehta_rao_ch21"],
        severity="critical",
        checkable=False
    ),
]

# ═════════════════════════════════════════════════════════════════════════════
# MASTER RULE LIST
# ═════════════════════════════════════════════════════════════════════════════
ALL_RULES = GROUP_P + GROUP_Q + GROUP_R + GROUP_S + GROUP_T

# ─────────────────────────────────────────────────────────────────────────────
# RUNNER
# ─────────────────────────────────────────────────────────────────────────────
async def main():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_RULES)} rules from batch {_BATCH}")
        print(f"Collection: interpretation_rules  |  science: mundane_jyotish\n")
        breakdown = {}
        for r in ALL_RULES:
            st = r["sub_type"]
            breakdown[st] = breakdown.get(st, 0) + 1
        print("Breakdown by sub_type:")
        for st, n in sorted(breakdown.items()):
            print(f"  {st:<45}: {n}")
        print(f"\nTotal: {len(ALL_RULES)}\n")
        print("Rule IDs:")
        for r in ALL_RULES:
            print(f"  {r['rule_id']}")
        print("\nDry run complete.")
        return

    import motor.motor_asyncio
    import os
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ.get("DB_NAME", "horoscope_db")]
    col = db["interpretation_rules"]

    ok = 0
    for rule in ALL_RULES:
        result = await col.update_one(
            {"rule_id": rule["rule_id"]},
            {"$set": rule},
            upsert=True
        )
        ok += 1
        print(f"  upserted: {rule['rule_id']}")
    print(f"\nDone. {ok}/{len(ALL_RULES)} upserted.")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
