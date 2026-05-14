"""
ingest_mundane_engine_specs_v2.py
==================================
Batch: mundane-engine-v2-20260505
Collection: mundane_engine_specs
Science: mundane_jyotish

NEW DOCUMENTS (5):
  1. mehta-ch5-planetary-significations  — Full planet→role→entities dictionary (Mehta Ch 5)
  2. mehta-ch6-house-ministry-mapping    — 12-house Ministry Mapping grid (Mehta Ch 6 + Gaur Ch 4.4)
  3. raphael-ch3-western-houses          — Western house refinements + Intellectual Triad (Raphael Ch 3)
  4. gaur-ch1-60-samvatsars              — All 60 Samvatsar names/lords/results lookup (Gaur Ch 1 §3)
  5. gaur-ch1-samvatsar-body             — Anatomical constellation mapping + body-part logic (Gaur Ch 1 §4)

Upsert key: spec_id
"""

import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os, json

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.environ.get("DB_NAME",   "horoscope_db")
BATCH_ID  = "mundane-engine-v2-20260505"
DRY_RUN   = True   # set False to write to MongoDB

# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT 1 — MEHTA CH 5: PLANETARY SIGNIFICATIONS
# ─────────────────────────────────────────────────────────────────────────────
MEHTA_CH5_PLANETARY_SIGNIFICATIONS = {
    "spec_id": "mehta-ch5-planetary-significations",
    "batch_id": BATCH_ID,
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "title": "Mehta/Rao Ch 5 — Comprehensive Planetary Significations",
    "description": (
        "Master dictionary of mundane entities governed by each planet. "
        "Maps planets to national roles, social classes, sectors, minerals, and commodities. "
        "Used as the primary significator index when auditing transits or afflictions."
    ),
    "synthesis_sources": [
        {"book": "mehta_rao", "chapter": "Ch 5", "label": "Signification of Planets"}
    ],
    "planets": {
        "sun": {
            "role": "The King / Rulers",
            "mundane_entities": [
                "Heads of State", "Prime Ministers", "Cabinet Ministers", "Persons in Authority",
                "Kings", "Nobles", "Magistrates", "Judges", "Bureaucracy", "Employers",
                "Influential Businessmen", "Big Commercial Firms", "New Undertakings",
                "Public Undertakings", "Temples", "Religious Places", "Top Religious Leaders",
                "National Prestige", "Fame and Reputation", "National Health and Vitality"
            ],
            "minerals": ["Gold", "Copper"],
            "commodities": ["Wheat", "Red Chillies"],
            "diagnostic_alert": "Affliction causes the nation to become arrogant, morally debased, despotic, and prone to national humiliation.",
            "dueling_significator_note": "Sun-Gold = State Reserve/Prestige (vs Jupiter-Gold = Banking/Personal Wealth). Sun-Chillies = State Commodities (vs Mars-Chillies = Trade Spikes)."
        },
        "moon": {
            "role": "The Public / Common Man",
            "mundane_entities": [
                "Common People", "Women generally", "Matters of Public Interest", "Public Opinion",
                "National Mood", "General Welfare", "Infant Mortality", "Nursing Profession",
                "Air Hostesses", "Social Service Workers", "Crops", "Plantations", "Agriculture",
                "Dairy Farms", "Liquids", "Milk", "Groceries", "Fishing Industry", "Navigation",
                "Sailing", "Yachting", "Water Transport", "Ships", "Seaports", "Oceans", "Rivers",
                "Textile Industry", "Merchants", "Travel Agencies", "Innkeepers", "Eating Places"
            ],
            "minerals": ["Silver", "Pearls"],
            "commodities": ["Rice", "Milk", "Honey", "Salt", "Fruits", "Flowers"],
            "diagnostic_alert": "Heavily afflicted Moon serves as the 'igniter' for major calamities like war and earthquakes."
        },
        "mars": {
            "role": "The Commander-in-Chief",
            "mundane_entities": [
                "Armed Forces", "Army Chief", "Soldiers", "Generals", "Military/Naval Men",
                "Police", "Fire-fighters", "Surgeons", "Dentists", "Butchers", "Engineers",
                "Manufacturing", "Iron and Steel Works", "Armaments", "War and Strife",
                "Armed Conflicts", "Coup d'etat", "Assassinations", "Terrorism", "Proxy War",
                "Infiltration", "Secret Enemies", "Abduction", "Rape", "Militancy", "Riots",
                "Rebellions", "Sedition", "Criminals", "Dacoity", "Burglary", "Theft", "Arson",
                "Explosions", "Accidents", "Air/Train Crashes", "Volcanoes", "Lava",
                "Hurricanes", "Typhoons"
            ],
            "minerals": ["Copper", "Gold"],
            "commodities": ["Masoor Dal", "Red Chillies", "Weapons", "Gur"],
            "diagnostic_alert": "Closest approach to Earth (perigee) always triggers major global conflicts."
        },
        "mercury": {
            "role": "The Intellectual Caliber",
            "mundane_entities": [
                "Media", "Press", "Newspapers", "Magazines", "Editors", "Publishers",
                "Booksellers", "Literary World", "Scientific Organizations", "Intellectual World",
                "Computer Programmers", "Internet", "Communication Systems", "Telecommunications",
                "Radio", "Television Anchors", "Ambassadors", "Envoys", "Treaties",
                "Written Documents", "Trade and Commerce", "General Industry",
                "Transport Vehicles", "Trains", "Weather Changes"
            ],
            "minerals": ["Emerald"],
            "commodities": ["Peas", "Green Vegetables", "Moong Dal"],
            "diagnostic_alert": "Mercury crossing Rashi or Nakshatra boundaries signals noticeable changes in weather."
        },
        "jupiter": {
            "role": "Judiciary, Finance & Religion",
            "mundane_entities": [
                "Banks", "National Treasury", "Revenue", "Finance", "Capitalism", "Business",
                "Wealth and Prosperity", "Loans", "Lotteries", "Judiciary", "Lawyers",
                "Advocates", "Judges", "Arbitration", "Treaties", "Foreign Affairs",
                "Foreign Trade", "Diplomats", "Long Travel", "Education", "Institutions",
                "Teachers", "Scholars", "Teaching", "Preaching", "Divines",
                "Religious Institutions", "Charitable Institutions", "Birth Rate",
                "Children", "General Happiness"
            ],
            "minerals": ["Gold"],
            "commodities": ["Turmeric", "Creeping Vegetables", "Cows"],
            "diagnostic_alert": "Affliction leads to banking collapses, over-optimism, and wasteful national extravagance.",
            "dueling_significator_note": "Jupiter-Gold = Banking/Personal Wealth (vs Sun-Gold = State Reserve/Prestige)."
        },
        "venus": {
            "role": "Arts & National Pleasure",
            "mundane_entities": [
                "Female Sex", "Women in High Places", "Artists", "Musicians", "Singers",
                "Cinema", "Entertainment Industry", "Theaters", "Music Halls",
                "Social Functions", "Fashion", "Cosmetics", "Perfumes", "Scents",
                "Ornaments", "Jewels", "Luxury Goods", "Vehicles", "National Wealth",
                "Currency Value", "Marriage Rate", "Births", "Peace Treaties",
                "Cessation of Hostilities", "Flowers", "Fine Arts"
            ],
            "minerals": ["Diamond", "Silver", "Jewelry"],
            "commodities": ["Coriander", "Masalas", "Fine Cotton", "Silk"],
            "diagnostic_alert": "Affliction by Mars denotes war; strong Venus denotes victory or signing of peace treaties."
        },
        "saturn": {
            "role": "Labor & Democratic Institutions",
            "mundane_entities": [
                "Democracy", "Democratic Institutions", "Municipal Elections", "Common People",
                "Labor Class", "Labor Unions", "Strikes", "Working Classes", "Underprivileged",
                "Farmers", "Farm Lands", "Agriculture", "Land and Real Estate", "Landowners",
                "Mines", "Coal", "Oil Ore", "Iron Ore", "Underground Wealth", "Old People",
                "Death of Prominent Leaders", "National Mourning", "Rebellion", "Revolution",
                "Overthrow of Rulers", "Prisons", "Prisoners", "Martyrs", "Secret Enemies",
                "Deceit", "Falsehood", "Judges", "Judicial System", "Civil Engineers",
                "Civil Service", "Bankruptcy", "Stagnation", "Economic Decline",
                "Nationalization", "Heavy Taxes", "Famines", "Droughts",
                "National Calamities", "Earthquakes", "Floods",
                "Skin and Leather Industry"
            ],
            "minerals": ["Iron", "Oils"],
            "commodities": ["Til (Sesame)", "Wool", "Leather"],
            "diagnostic_alert": (
                "Saturn governs gain or loss of national territory during war. "
                "Primary significator of contraction and economic depression. "
                "Saturn as 10th lord for India — longevity of leaders linked to marital status (Gopal Ch 2 refinement)."
            )
        },
        "rahu": {
            "role": "The Shadowy Aggressor",
            "mundane_entities": [
                "Crimes", "Violence", "War", "Rebellion", "Mutiny", "Aggressiveness",
                "Riots", "Strikes", "Mobs", "Foreigners", "Muslims", "Immigration",
                "Spies", "Political Plots", "Imprisonment", "Slavery",
                "Death by Suffocation", "Electronics", "Radio", "Aerial Navigation",
                "Poisonous Gases", "Poisoning", "Poisonous Snakes", "Sudden Accidents",
                "Epidemics", "Plague", "Cancer", "Skin Diseases", "Eczema",
                "Robbery", "Jealousy", "Falsehood", "Anti-Religious Forces",
                "Anti-Social Elements"
            ],
            "minerals": ["Glass", "Gomedh"],
            "commodities": ["Groundnut", "Cotton Seed", "Cigarettes", "Tobacco"],
            "diagnostic_alert": "Rahu is most deadly when conjunct Saturn or Mars in houses 6, 8, or 12.",
            "it_bpo_tracking": "For IT and Communications sectors, track Mercury (Logic) + Rahu (Electronics) + Ketu (Computers) simultaneously."
        },
        "ketu": {
            "role": "Secretive Destruction",
            "mundane_entities": [
                "Secret Plots", "Conspiracies", "Intrigues", "Espionage", "Treachery",
                "Assassinations", "Murders", "Spies", "Strife", "War",
                "Death in Battlefield", "Self-Immolation", "Suicide", "Dacoits",
                "Destruction", "Bankruptcies", "Computers", "Television",
                "Ready-made Clothes", "Watches", "Clocks", "Timepieces",
                "Foreign Languages", "Liquors", "Drugs", "Non-Hindus", "Sikhs",
                "Epidemics (Leprosy, Cancer, Plague, Skin Eruptions)",
                "Spiritual Salvation (Moksha)"
            ],
            "diagnostic_alert": "Ketu acts like Mars but operates through secrecy and sudden, unpredictable success or failure."
        }
    },
    "moon_ignition_rule": (
        "Moon is the 'igniter' for major calamities. Even if a war configuration (Mars-Saturn) "
        "exists, the event may not materialize until the Moon makes a relevant transit."
    ),
    "weather_timing_rule": (
        "Mercury is the primary planet for identifying the TIMING of weather shifts "
        "based on sign and star changes."
    )
}

# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT 2 — MEHTA CH 6: HOUSE MINISTRY MAPPING
# ─────────────────────────────────────────────────────────────────────────────
MEHTA_CH6_HOUSE_MINISTRY = {
    "spec_id": "mehta-ch6-house-ministry-mapping",
    "batch_id": BATCH_ID,
    "spec_type": "lookup_grid",
    "science_id": "mundane_jyotish",
    "title": "Mehta/Rao Ch 6 + Gaur Ch 4.4 — Comprehensive House-Ministry Mapping Grid",
    "description": (
        "Transforms the 12 astrological houses into the Twelve Departments of State. "
        "Each house maps to a primary ministry, list of governed entities, and specific "
        "benefic/malefic diagnostic conditions. PM Office split: 10th = Executive Authority, "
        "11th = Leader as Parliamentarian/Legislator."
    ),
    "synthesis_sources": [
        {"book": "mehta_rao", "chapter": "Ch 6", "label": "Houses and their Signification"},
        {"book": "gaur_aifas", "chapter": "Ch 4.4", "label": "Administrative Ministry Mapping"}
    ],
    "intensity_scaling_rule": (
        "A Lunation (New/Full Moon) in any house acts as 'Minute Hand' that materializes "
        "trends set by the 'Hour Hand' of the Quarterly Solar Ingress."
    ),
    "houses": [
        {
            "house": 1,
            "primary_ministry": "Ministry of Home Affairs",
            "entities": [
                "The nation as a whole", "Common people", "Public health", "National mood",
                "General condition of the country", "Internal affairs",
                "General character of the populace", "National objectives",
                "Domestic considerations", "Behavior in emergencies",
                "National disasters response"
            ],
            "benefic_results": "Good health for the people, national happiness, overall prosperity, and a satisfactory internal state of affairs.",
            "malefic_alert": "Triggers national discontent, restlessness, and internal disasters. In the cabinet, it indicates dissensions, shuffles, or reallocation of portfolios."
        },
        {
            "house": 2,
            "primary_ministry": "Ministry of Finance & Commerce",
            "entities": [
                "National exchequer", "Revenue", "National wealth", "Purchasing power",
                "Banks", "National treasury", "Currency and national debt",
                "Gross National Product (GNP)", "Taxation", "Interest rates",
                "Stock market and exchanges", "Stocks and bonds investment",
                "Commercial affairs and trade", "Import and Export",
                "Financial transactions", "Allies"
            ],
            "benefic_results": "Increased revenue, improvement in the national exchequer, positive trade balance, and prosperous times for stocks.",
            "malefic_alert": "Heavily afflicted Saturn denotes a severe drain on national resources. Other impacts: bank failures, financial chaos, and falling exports.",
            "special_note": "Lunation in 2nd afflicted → Market Panic and Financial Chaos for that month."
        },
        {
            "house": 3,
            "primary_ministry": "Ministry of Communication, I&B, and Transport",
            "entities": [
                "Posts & Telegraph", "Telephones", "Radio", "Television",
                "Satellite communications", "Internet", "The Press", "Newspapers",
                "Advertising", "Magazines and literature", "Railways", "Aviation",
                "Automobiles", "Traffic and travel", "Neighbouring countries",
                "Border clashes", "Trade within the country",
                "Mental attitude of the people", "Public opinion",
                "Signed documents and written agreements"
            ],
            "benefic_results": "Successful new communication enterprises, increased income from postal affairs.",
            "malefic_alert": "Rail, air, and road accidents. Disruptions in communication networks, publishing failures, and strikes in transport departments.",
            "raphael_refinement": "Part of the Intellectual Triad (Houses 1+3+9) representing 'The Press'."
        },
        {
            "house": 4,
            "primary_ministry": "Ministry of Agriculture, Infrastructure & The Opposition",
            "entities": [
                "Landed interests", "Agriculture and crop industry", "Mining and minerals",
                "Real estate", "Slum areas", "Hotel industry", "Weather conditions",
                "Homeland and patriotism", "Forests and forest fires", "Volcanoes",
                "Earthquakes and floods", "Landslides",
                "Schools and educational institutions", "The Throne of the King",
                "Opposition Parties", "Democratic movements",
                "Municipal politics", "General happiness of the nation"
            ],
            "benefic_results": "Bumper crops, government popularity, national unity through patriotism.",
            "malefic_alert": "Shortage of food, loss of prestige for the government, and threats to the leadership. If malefics are in fixed signs: disastrous earthquakes or mining catastrophes."
        },
        {
            "house": 5,
            "primary_ministry": "Ministry of Education & National Entertainment",
            "entities": [
                "Children and the birth rate", "Primary education",
                "Educational facilities in arts", "National pleasures and enjoyment",
                "Theatres", "Cinema halls", "Sports", "Community parks",
                "Actors and actresses", "Artistic activity", "Speculation",
                "Stock exchange", "Morals and scandals",
                "Crimes related to immorality",
                "Upper House (Rajya Sabha / House of Lords)",
                "Foreign ambassadors and diplomats",
                "Danger to the ruler (8th from the 10th)"
            ],
            "benefic_results": "Honours for prominent artists, increased birth rates, healthy growth in education and sports sectors.",
            "malefic_alert": "Political plots against the ruler, terrorist attacks on prominent actors or officials, and corruption of the younger generation."
        },
        {
            "house": 6,
            "primary_ministry": "Ministry of Defense, Public Service & Health",
            "entities": [
                "Armed forces (Army and Navy)", "Warships",
                "Territorial attacks and war conditions",
                "Labor classes and unions", "Strikes", "State loans and debts",
                "Service class and servants", "Medical services",
                "Doctors and nurses", "Hospitals", "Mass diseases and epidemics",
                "Public health generally", "National food supplies",
                "Animal husbandry", "Record keeping", "Computers"
            ],
            "benefic_results": "Victory in war (if 11th lord involved), improved public health, and welfare for the labor class.",
            "malefic_alert": "Mutiny or insubordination in the armed forces. If Mars is lord of both 6th and 7th, open war is a certainty. Saturn-Mars conjunction here triggers mass murders."
        },
        {
            "house": 7,
            "primary_ministry": "Ministry of Foreign Affairs",
            "entities": [
                "International relations", "Foreign countries",
                "International affairs and trade", "Treaties", "Alliances",
                "Foreign national disputes", "Wars and open warfare",
                "Enemies", "Dacoits and robbers",
                "Marriage and divorce rates", "Immorality in the country",
                "Infant mortality", "Anti-social elements vs. government cooperators"
            ],
            "benefic_results": "Diplomatic success, signing of peace treaties, and prosperity in foreign trade.",
            "malefic_alert": "Grave danger of international disputes and war. Direction of enemy is indicated by sign position of Mars in this house."
        },
        {
            "house": 8,
            "primary_ministry": "Ministry of Mortality, Hidden Assets & Research",
            "entities": [
                "Death rate", "Mortality in high circles",
                "Death of national rulers (PM/President)",
                "Assassinations of leaders", "Setbacks to the cabinet",
                "National mourning", "End of government",
                "Scientific discoveries and investment",
                "Underground wealth and hidden things",
                "Capital gains", "Taxes and death duties", "Pensions",
                "Mass tragedies", "Famines and epidemics",
                "Suicides", "Earthquakes and volcanoes"
            ],
            "benefic_results": "Gains to the national exchequer through death duties. Significant scientific breakthroughs or discovery of hidden mineral wealth.",
            "malefic_alert": "Panic among the people, mass tragedies, and the sudden overthrow of the government through death or destruction of the ruling elite."
        },
        {
            "house": 9,
            "primary_ministry": "Ministry of Law, Justice & Religion",
            "entities": [
                "Supreme Court", "Judiciary and litigation", "Law courts",
                "International law", "Ministry of Foreign Affairs (Diplomacy)",
                "United Nations and world organizations",
                "Religion (Temples, mosques, churches)", "Sacred books",
                "Higher thought", "Institutions of higher studies",
                "Scientific societies", "Publishing and advertising",
                "Immigration", "Navy and naval affairs", "Sea voyages",
                "Tourism", "Air Force",
                "Long-distance communications (Cables, Radio, TV)"
            ],
            "benefic_results": "Beneficial changes in foreign policy, strong judiciary, and prosperity for scientific and religious institutions.",
            "malefic_alert": "Religious disputes and communal riots. Accidents in shipping. If Rahu heavily afflicted: conspiracies to invade the country.",
            "raphael_refinement": "Part of the Intellectual Triad (Houses 1+3+9) representing 'Religious Attitude and Higher Thought'."
        },
        {
            "house": 10,
            "primary_ministry": "The Executive (Prime Minister & Authority)",
            "entities": [
                "The Ruler", "President", "Prime Minister", "Nobility",
                "The Ruling Party", "Top authority in the state",
                "National prestige and honour", "Status and reputation",
                "National celebrities", "National aims and gains",
                "Parliament", "Politics and politicians",
                "The power to rule", "Discipline", "Lawlessness (if afflicted)"
            ],
            "benefic_results": "Stability and prosperity for the government, national honours, and a high international reputation for the leader.",
            "malefic_alert": "An eclipse here is a sign of defeat or overthrow of the government. Affliction indicates disgrace, scandals, and illness/death among royalty.",
            "pm_authority_note": "10th = Executive Authority (the Office). 11th = PM as Parliamentarian/Legislator. Both must be audited for full PM analysis."
        },
        {
            "house": 11,
            "primary_ministry": "Ministry of Parliamentary Legislation",
            "entities": [
                "Legislative bodies", "Parliament", "Members of Parliament",
                "National aims and goals", "National plans",
                "Treaties and alliances", "Contracts with foreign governments",
                "Ambassadors sent out", "Vice-President",
                "National mint and treasures", "Election victory",
                "National revenue", "Cooperative societies",
                "Gain from foreign trade"
            ],
            "benefic_results": "Smooth passage of beneficial legislation, gainful international contracts, and recognition for state policies.",
            "malefic_alert": "Chaos in parliamentary procedure, loss to the exchequer, and bickering between the cabinet and the ruler. Sickness among members."
        },
        {
            "house": 12,
            "primary_ministry": "Ministry of Security & External Threats",
            "entities": [
                "Secret service and intelligence", "Secret forces and spies",
                "Terrorists", "Foreign spies and infiltration",
                "Conspiracies and secret plots", "Saboteurs",
                "Prisons and jails", "Labor camps",
                "Hospitals and asylums", "War losses",
                "Extravagance and squandering of public money", "Miseries",
                "Financial mismanagement", "Crime, murder, and arson",
                "Smuggling", "Kidnappers",
                "Life in foreign places", "Foreign investments"
            ],
            "benefic_results": "Success in prison reforms, effective charitable institutions, and a flourishing tourism industry.",
            "malefic_alert": "National betrayal by spies. Infiltration of dangerous foreign elements and mass tragedies through epidemics. Rahu here: extreme chaos."
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT 3 — RAPHAEL CH 3: WESTERN HOUSE REFINEMENTS
# ─────────────────────────────────────────────────────────────────────────────
RAPHAEL_CH3_WESTERN_HOUSES = {
    "spec_id": "raphael-ch3-western-houses",
    "batch_id": BATCH_ID,
    "spec_type": "lookup_grid",
    "science_id": "mundane_jyotish",
    "title": "Raphael Ch 3 — Western House Refinements + Intellectual Triad",
    "description": (
        "Western granular layer for mundane house interpretation. Adds institutional specificity "
        "(Privy Council in 8th, Colonial Trade in 9th, Reformatories in 12th) beyond Vedic. "
        "Introduces the Intellectual Triad (Houses 1+3+9) and house strength tiering (Angular > Succedent > Cadent)."
    ),
    "synthesis_sources": [
        {"book": "raphael_west", "chapter": "Ch 3", "label": "The Twelve Mundane Houses"}
    ],
    "strength_tiering": {
        "tier_1_angular": {
            "houses": [1, 10, 7, 4],
            "weighting": "Strongest Impact",
            "description": "Primary centers of national activity and power."
        },
        "tier_2_succedent": {
            "houses": [2, 5, 8, 11],
            "weighting": "Medium Impact",
            "description": "Secondary support structures and resources."
        },
        "tier_3_cadent": {
            "houses": [3, 6, 9, 12],
            "weighting": "Weakest Impact",
            "description": "Tertiary concerns and background influences."
        }
    },
    "intellectual_triad": {
        "house_1": "The collective minds and mental state of the people.",
        "house_3": "The Press, newspapers, and general literary concerns.",
        "house_9": "The religious attitude and higher thought of the populace.",
        "synchrony_rule": (
            "For queries involving National Mood or Propaganda, audit Houses 1+3+9 "
            "as a single synchronized triad."
        )
    },
    "western_refinements": {
        "house_1": ["The common people", "Public health", "Internal state of affairs"],
        "house_2": ["National exchequer", "Revenue", "Stock exchange", "Banks", "Commerce and trade"],
        "house_3": ["Railways", "Traffic returns", "Postal affairs", "Telegraph and telephone", "Locomotion", "Newspapers"],
        "house_4": ["Weather", "Agriculture", "Landed interests", "Mines", "Public buildings", "The Opposition party"],
        "house_5": ["Theatres", "Music halls", "Places of amusement", "Children", "Schools", "Birth-rate", "Morals", "Betting"],
        "house_6": ["Sickness and public health", "Army and Navy", "Warships", "Working classes generally"],
        "house_7": ["Foreign affairs", "Relations with other Powers", "War and international disputes", "Marriages and divorces", "Foreign trade"],
        "house_8": ["Mortality and death-rate", "Suicides", "The Privy Council"],
        "house_9": ["Law courts and judges", "The Clergy and religion", "Colonial trade and affairs", "Science", "Shipping"],
        "house_10": ["The King", "Royalty", "The Government", "Ruling powers", "Aristocracy", "Nobility", "Society"],
        "house_11": ["Parliament", "The House of Commons", "Legislation"],
        "house_12": ["Prisons", "Workhouses", "Hospitals", "Asylums", "Reformatories", "Charitable institutions", "Crime", "Spies", "Secret foes"]
    },
    "strength_application_rule": (
        "A malefic in an Angular house (e.g., 4th) must trigger a higher 'Calamity Warning' "
        "than the same malefic in a Cadent house (e.g., 3rd). Apply power multiplier accordingly."
    ),
    "vulnerability_veto": (
        "Any planet placed within 5 degrees of a house cusp in a mundane chart is "
        "'Accidentally Dignified' — its results are significantly amplified."
    )
}

# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT 4 — GAUR CH 1: 60 SAMVATSARS LOOKUP TABLE
# ─────────────────────────────────────────────────────────────────────────────
GAUR_CH1_60_SAMVATSARS = {
    "spec_id": "gaur-ch1-60-samvatsars",
    "batch_id": BATCH_ID,
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "title": "Gaur/AIFAS Ch 1 §3 — All 60 Samvatsars: Names, Lords, General Results & Monthly Variations",
    "description": (
        "Complete 60-year Jupiter cycle lookup. Each Samvatsar has a name, presiding lord, "
        "general annual result, and month-specific price/weather/political conditions. "
        "Trinity grouping: IDs 1-20 = Brahma (Creation), 21-40 = Vishnu (Maintenance/Disease), "
        "41-60 = Shiv (Destruction/Conflicts)."
    ),
    "synthesis_sources": [
        {"book": "gaur_aifas", "chapter": "Ch 1", "label": "Samvatsar — Names and Lords"}
    ],
    "calculation_method": {
        "input": "Vikrami Samvat year",
        "step_1": "Subtract 1927 from the Vikrami Samvat",
        "step_2": "Divide result by 10 → get Quotient and Remainder",
        "step_3": "Look up Quotient Number Table and Remainder Number Table",
        "step_4": "Add values (Year, Month, Day, Ghari, Pal) from both tables",
        "step_5": "First number = passed Samvatsars; next index = current Samvatsar",
        "practical_note": "For practical purposes the same Samvatsar is accepted for the whole year despite precise changeover moment.",
        "vikrami_offset": "Add approximately 57 years to current AD year to get Vikrami Samvat."
    },
    "trinity_grouping": {
        "brahma_creation": {"ids": "1-20", "macro_theme": "Creation, establishment, prosperity"},
        "vishnu_maintenance": {"ids": "21-40", "macro_theme": "Maintenance, disease cycles, political transitions"},
        "shiv_destruction": {"ids": "41-60", "macro_theme": "Destruction, conflicts, border wars"}
    },
    "samvatsars": [
        {"id": 1,  "name": "Prabhav",       "lord": "Brahma",  "trinity": "Brahma",
         "general_result": "Rulers, ministers, senior officers pleased. Luxuries increase. Crops good, absence of disease.",
         "key_signals": {"lucky_months": ["Chaitra","Baisakh","Bhadrapad"], "costly_months": ["Jyeshtha","Aashadh","Shravan"], "disease_alert": "Ashwin"}},
        {"id": 2,  "name": "Vibhav",        "lord": "Vishnu",  "trinity": "Brahma",
         "general_result": "Rulers take stern measures for law and order. Peace and happiness. Rains and crops good.",
         "key_signals": {"health_alert": "Many diseases present", "plentiful_rains": ["Aashadh","Shravan","Bhadrapad"], "cheap_grains": ["Kartik","Margsheersh","Paush","Magh","Phalgun"]}},
        {"id": 3,  "name": "Shukla",        "lord": "Shiv",    "trinity": "Brahma",
         "general_result": "People live happily with relatives. Friction between rulers and opposition parties.",
         "key_signals": {"political_risk": "Rulers of many places lose throne; President's rule frequently imposed", "heavy_rains": ["Aashadh","Shravan","Bhadrapad"], "failure_alert": "Phalgun full of difficulties"}},
        {"id": 4,  "name": "Pramod",        "lord": "Sun",     "trinity": "Brahma",
         "general_result": "Rulers and people pleased. Masses free of disease, turmoils, and enemies.",
         "key_signals": {"rain_note": "Rains less; scanty in Aashadh/Shravan/Bhadrapad", "political_instability": "Insurgency encourages violence; conflict between rulers and businessmen"}},
        {"id": 5,  "name": "Prajapati",     "lord": "Moon",    "trinity": "Brahma",
         "general_result": "All people follow their path. Rains plentiful and grains cheap.",
         "key_signals": {"outlook": "All 12 months excellent", "disaster_alert": "Natural calamities in Paush/Maagh/Phalgun"}},
        {"id": 6,  "name": "Angira",        "lord": "Mars",    "trinity": "Brahma",
         "general_result": "Grains plentiful but rulers engaged in conflicts. World peace breached by wars.",
         "key_signals": {"weather": "Storms in Jyeshtha; heavy rains/floods in Aashadh", "epidemic_alert": "Disease widespread in Shravan/Bhadrapad/Ashwin"}},
        {"id": 7,  "name": "Shree Mukh",    "lord": "Mercury", "trinity": "Brahma",
         "general_result": "Grains good; rains satisfactory. Farmers get good returns. High harmony, less conflict. Diseases removed.",
         "key_signals": {}},
        {"id": 8,  "name": "Bhav",          "lord": "Jupiter", "trinity": "Brahma",
         "general_result": "Diseases excessive. Grain production medium. Rulers engage in wars but people feel secure.",
         "key_signals": {"high_prices": "All things generally dear", "cheap_grains": ["Margsheersh","Paush","Maagh","Phalgun"]}},
        {"id": 9,  "name": "Yuva",          "lord": "Venus",   "trinity": "Brahma",
         "general_result": "Milk production good; rains excessive. Young people seek luxury. Supremacy of females established.",
         "key_signals": {"calamity_alert": "Earthquakes and natural calamities in Chaitra/Baisakh", "price_impact": "Grains become costly"}},
        {"id": 10, "name": "Dhata",         "lord": "Saturn",  "trinity": "Brahma",
         "general_result": "Rulers create war atmosphere via diplomacy. People remain fearful. Crops good.",
         "key_signals": {"costly_grains": ["Chaitra","Baisakh"], "costly_oils": ["Aashadh"], "costly_metals": ["Ashwin"]}},
        {"id": 11, "name": "Eashwar",       "lord": "Rahu",    "trinity": "Brahma",
         "general_result": "People live happily; crops of fruits and grains good. Rahu lord brings conflict.",
         "key_signals": {"geopolitical": "Drought in North, floods in East, war in West", "riot_alert": "Loss of lives due to riots in final four months"}},
        {"id": 12, "name": "Bahudhanya",    "lord": "Ketu",    "trinity": "Brahma",
         "general_result": "Plentiful rains and abundant grains. People tend toward loose character.",
         "key_signals": {"cheap_grains": ["Aashadh","Shravan","Bhadrapad"], "heavy_rains": "Ashwin"}},
        {"id": 13, "name": "Pramathi",      "lord": "Sun",     "trinity": "Brahma",
         "general_result": "No excessive rains; rains normal everywhere.",
         "key_signals": {"high_prices": "All grains and juicy materials expensive in final 5 months"}},
        {"id": 14, "name": "Vikram",        "lord": "Moon",    "trinity": "Brahma",
         "general_result": "Rulers brave and good. Rains experienced everywhere.",
         "key_signals": {"calamity": "Earthquakes at end of Baisakh cause loss of life/wealth", "drought": "Droughts in Jyeshtha"}},
        {"id": 15, "name": "Vrish",         "lord": "Mars",    "trinity": "Brahma",
         "general_result": "Differences among rulers and political hurdles. War clouds prevail.",
         "key_signals": {"political_risk": "Usurping of thrones; friction and tussles", "security_alert": "Riots in Margsheersh; senior positions become vacant"}},
        {"id": 16, "name": "Chitrabhanu",   "lord": "Mercury", "trinity": "Brahma",
         "general_result": "Untimely/scanty rains in some places; excessive in others. Earth full of grains, fruits, grass.",
         "key_signals": {"epidemic_alert": "Fear of epidemic in Kartik", "cheap_months": ["Maagh","Phalgun"]}},
        {"id": 17, "name": "Subhanu",       "lord": "Jupiter", "trinity": "Brahma",
         "general_result": "Conflicts between governments cause fear and war. Rice crops good.",
         "key_signals": {"political_alert": "Rulers in conflict; people restless in Paush/Maagh/Phalgun"}},
        {"id": 18, "name": "Taaran",        "lord": "Venus",   "trinity": "Brahma",
         "general_result": "People leave homes due to danger, wars, or violence. Move to peaceful areas.",
         "key_signals": {"meteorological_hazard": "Too many storms", "war_atmosphere": ["Margsheersh","Paush"]}},
        {"id": 19, "name": "Paarthiv",      "lord": "Saturn",  "trinity": "Brahma",
         "general_result": "Ruling class and common people live happily with luxuries. Crops and rains good.",
         "key_signals": {"riot_alert": "Fear of riots; goods expensive in Chaitra/Baisakh/Aashadh/Ashwin", "weather": "High speed winds cause losses; storms in Bhadrapad"}},
        {"id": 20, "name": "Vyaya",         "lord": "Rahu",    "trinity": "Brahma",
         "general_result": "Rulers worried and disturbed; must strengthen army. Border disputes. People spend wastefully.",
         "key_signals": {"rain_imbalance": "Too little or too much rains cause losses", "regional": "Drought in Shravan; disharmony in middle provinces"}},
        {"id": 21, "name": "Sarvjeet",      "lord": "Brahma",  "trinity": "Vishnu",
         "general_result": "People live with comforts. Rulers develop conflicts and war atmosphere. Rains good; crops sufficient.",
         "key_signals": {"cheap_months": ["Chaitra","Baisakh","Jyeshtha","Ashwin","Kartik"], "weather": "Excessive rains in last 5 days of Bhadrapad"}},
        {"id": 22, "name": "Sarvdhari",     "lord": "Vishnu",  "trinity": "Vishnu",
         "general_result": "Rulers forget conflicts and provide comforts. Peace, greenery, and sufficient rains everywhere.",
         "key_signals": {"calamity_alert": "Danger of natural calamities in Jyeshtha", "blissful_months": ["Margsheersh","Paush","Maagh","Phalgun"]}},
        {"id": 23, "name": "Virodhi",       "lord": "Shiv",    "trinity": "Vishnu",
         "general_result": "Conflicts based on caste, religion, and community. Theft high. Cow milk reduced.",
         "key_signals": {"health_alert": "Children suffer from smallpox; blood/wind diseases multiply", "regional": "Grains expensive in Gujarat and Rajasthan in final four months"}},
        {"id": 24, "name": "Vikrit",        "lord": "Sun",     "trinity": "Vishnu",
         "general_result": "Immoral acts excessive. Loss of life/wealth via disease and natural calamities (earthquakes, volcanoes).",
         "key_signals": {"rain_note": "Droughts in deserts like Rajasthan", "political_risk": "Change of rule in some places during Ashwin"}},
        {"id": 25, "name": "Khar",          "lord": "Moon",    "trinity": "Vishnu",
         "general_result": "Rulers in conflict; fires of war kindled. Senior leader dies; thrones changed. Rains less; crops poor.",
         "key_signals": {"warning": "Senior leader death / throne change", "cheap_months": ["Chaitra to Aashadh","Kartik to Phalgun"]}},
        {"id": 26, "name": "Nandan",        "lord": "Mars",    "trinity": "Vishnu",
         "general_result": "People live with comforts/pleasures; free from disease. Grains and wealth abundant.",
         "key_signals": {"weather": "High velocity winds; excessive rains in Aashadh and Bhadrapad"}},
        {"id": 27, "name": "Vijai",         "lord": "Mercury", "trinity": "Vishnu",
         "general_result": "Rulers inclined toward war. Wealth destroyed. Droughts damage crops. Mourning increases.",
         "key_signals": {"war_impact": "Some parts of country suffer due to war; cattle suffer"}},
        {"id": 28, "name": "Jai",           "lord": "Jupiter", "trinity": "Vishnu",
         "general_result": "Celebrations on earth. Comforts increase. Rulers and army chiefs determine to be victorious.",
         "key_signals": {"cheap_months": ["Baisakh","Jyeshtha","Aashadh"], "political_risk": "Change of throne at few places; metals expensive"}},
        {"id": 29, "name": "Manmath",       "lord": "Venus",   "trinity": "Vishnu",
         "general_result": "Suffering due to scoundrels. Earth full of grains like barley and wheat.",
         "key_signals": {"calamity": "Earthquakes in Chaitra", "regional_suffering": "People of eastern countries suffer"}},
        {"id": 30, "name": "Durmukh",       "lord": "Saturn",  "trinity": "Vishnu",
         "general_result": "Rains ordinary. Suffering due to evil persons and thieves. Enmity between rulers and army chiefs.",
         "key_signals": {"regional": "Drought in North; good crops in East", "health_alert": "Disease in Phalgun"}},
        {"id": 31, "name": "Hemlumb",       "lord": "Rahu",    "trinity": "Vishnu",
         "general_result": "Crops medium. Rulers oppose each other. Lightning in sky; rains less.",
         "key_signals": {"calamity": "Earthquakes cause agony", "war_danger": "Danger of war between two nations"}},
        {"id": 32, "name": "Vilamb",        "lord": "Sun",     "trinity": "Vishnu",
         "general_result": "People suffer due to differences among rulers. Prosperity and peace maintained.",
         "key_signals": {"excessive_rains": "21 days of rain in Bhadrapad cause loss", "regional": "Administration of western countries disturbed"}},
        {"id": 33, "name": "Vikari",        "lord": "Moon",    "trinity": "Vishnu",
         "general_result": "People suffer due to disease, floods, and drought. Wheat, barley, and fruits less.",
         "key_signals": {"astronomical_sign": "Comet sighted in Ashwin"}},
        {"id": 34, "name": "Sharbari",      "lord": "Mars",    "trinity": "Vishnu",
         "general_result": "Rulers have differences. Rains sufficient; crops excellent. People comfortable.",
         "key_signals": {"regional": "Drought in West; good crops in East during Ashwin"}},
        {"id": 35, "name": "Plav",          "lord": "Mercury", "trinity": "Vishnu",
         "general_result": "Rains more. People suffer due to diseases and lusts.",
         "key_signals": {"weather": "High speed winds in Aashadh with fear of disease; floods in Bhadrapad", "cheap_months": ["Jyeshtha","Bhadrapad","Kartik to Phalgun"]}},
        {"id": 36, "name": "Shubhkrit",     "lord": "Jupiter", "trinity": "Vishnu",
         "general_result": "Celebrations occur. Danger from terrorists and thieves. Rulers inclined toward war.",
         "key_signals": {"cheap": "Most months are cheap", "regional_alert": "Danger of fires in North"}},
        {"id": 37, "name": "Shobhan",       "lord": "Venus",   "trinity": "Vishnu",
         "general_result": "Grains abundantly produced. Rains good despite danger of disease and death.",
         "key_signals": {"cheap_months": ["Chaitra","Baisakh","Jyeshtha","Ashwin"], "danger": "Atmosphere of natural calamities and violence in final months"}},
        {"id": 38, "name": "Krodh",         "lord": "Saturn",  "trinity": "Vishnu",
         "general_result": "People suffer due to anger, lust, and selfishness. Rains and crops insufficient.",
         "key_signals": {"health_alert": "Fatal diseases strike", "commerce": "Commerce remains unstable"}},
        {"id": 39, "name": "Vishvavasu",    "lord": "Rahu",    "trinity": "Vishnu",
         "general_result": "Administration unstable. Rains and crops insufficient. People burdened by taxes.",
         "key_signals": {"costly_months": "Chaitra to Ashwin", "price_impact": "High prices of cattle in Ashwin; gold is cheap"}},
        {"id": 40, "name": "Parabhav",      "lord": "Ketu",    "trinity": "Vishnu",
         "general_result": "Kings inclined toward wars. Widespread diseases. Rains and crops insufficient.",
         "key_signals": {"weather": "Fearsome winds, thunder, lightning in Chaitra/Baisakh", "cheap": "Metals cheap in Ashwin"}},
        {"id": 41, "name": "Plavang",       "lord": "Brahma",  "trinity": "Shiv",
         "general_result": "Rains less. People suffer from disease and theft. Border disputes lead to war.",
         "key_signals": {"calamity": "Earthquakes in Aashadh", "political_risk": "Jyeshtha unlucky for rulers"}},
        {"id": 42, "name": "Keelak",        "lord": "Vishnu",  "trinity": "Shiv",
         "general_result": "Grains cheap due to sufficient rains. Prosperity increases. Danger of interstate war.",
         "key_signals": {"regional_alert": "Drought in desert areas in Baisakh"}},
        {"id": 43, "name": "Saumya",        "lord": "Shiv",    "trinity": "Shiv",
         "general_result": "Differences among rulers minimized. Rains normal; all grains produced.",
         "key_signals": {"war_impact": "Rulers fight and people suffer in Ashwin"}},
        {"id": 44, "name": "Sadharan",      "lord": "Sun",     "trinity": "Shiv",
         "general_result": "Rulers live peacefully; people devoid of conflict. Rains less but danger minimized.",
         "key_signals": {"calamity_alert": "Earthquakes in Baisakh and Jyeshtha", "war_risk": "War may start suddenly in Kartik/Margsheersh"}},
        {"id": 45, "name": "Virodh",        "lord": "Moon",    "trinity": "Shiv",
         "general_result": "Masses and rulers develop differences. Rains less; crops damaged.",
         "key_signals": {"political_risk": "Opposition rises in the country during Phalgun"}},
        {"id": 46, "name": "Paridhavi",     "lord": "Mars",    "trinity": "Shiv",
         "general_result": "Atmosphere of war. Many diseases; crops medium. General worry and suffering.",
         "key_signals": {"cheap_materials": "All metals cheap in Shravan/Bhadrapad", "health_alert": "Cattle suffer from diseases"}},
        {"id": 47, "name": "Pramadi",       "lord": "Mercury", "trinity": "Shiv",
         "general_result": "Rains and crops medium. People suffer from disease. Rulers kind-hearted.",
         "key_signals": {"grains": "Accumulated in Vaishakh and Jyeshtha"}},
        {"id": 48, "name": "Anand",         "lord": "Jupiter", "trinity": "Shiv",
         "general_result": "Rulers and people live with comforts. Crops good; rains sufficient.",
         "key_signals": {"cheap_months": ["Chaitra","Baisakh","Ashwin","Paush","Maagh"], "danger": "Sudden emergence of danger in Kartik"}},
        {"id": 49, "name": "Rakshas",       "lord": "Venus",   "trinity": "Shiv",
         "general_result": "People become cruel and leave kindness. Grains, crops, and rains medium.",
         "key_signals": {"note": "People accumulate grains"}},
        {"id": 50, "name": "Nal",           "lord": "Saturn",  "trinity": "Shiv",
         "general_result": "Crops medium. Rulers unhappy. Fear due to terrorists, thieves, and smugglers.",
         "key_signals": {"regional_alert": "Drought in North", "health_alert": "Children's diseases spread widely in Phalgun"}},
        {"id": 51, "name": "Pingal",        "lord": "Rahu",    "trinity": "Shiv",
         "general_result": "Crops poor. Rulers use military might to usurp enemy land.",
         "key_signals": {"cheap_materials": "Metals cheap"}},
        {"id": 52, "name": "Kaalyukta",     "lord": "Ketu",    "trinity": "Shiv",
         "general_result": "People live happily. Grains excellent. New diseases cause suffering.",
         "key_signals": {"cheap_materials": "Juicy materials and metals cheap in Ashwin", "political_alert": "Rulers develop conflict; cattle suffer in final months"}},
        {"id": 53, "name": "Siddharthi",    "lord": "Sun",     "trinity": "Shiv",
         "general_result": "Knowledge increases; spirit of celibacy strong. Crops/rains good. Joys and celebrations everywhere.",
         "key_signals": {"weather": "Heavy rains 3 days in Shravan; strong winds in Jyeshtha/Aashadh", "political_risk": "Unrest in final four months"}},
        {"id": 54, "name": "Raudra",        "lord": "Moon",    "trinity": "Shiv",
         "general_result": "Rulers have conflicts and bitterness. Rains and crops medium.",
         "key_signals": {"global_tension": "Global tension is high"}},
        {"id": 55, "name": "Durmati",       "lord": "Mars",    "trinity": "Shiv",
         "general_result": "Brains of rulers misguided. Mutual opposition creates war atmosphere. People remain comfortable.",
         "key_signals": {"weather": "Too many winds and storms in Aashadh"}},
        {"id": 56, "name": "Dundubhi",      "lord": "Mercury", "trinity": "Shiv",
         "general_result": "Crops excellent. Rulers provide facilities. Unlucky events in East. Rains good; grains cheap.",
         "key_signals": {"health_alert": "Diseases more in Ashwin"}},
        {"id": 57, "name": "Rudhirodgari",  "lord": "Jupiter", "trinity": "Shiv",
         "general_result": "Rulers damage lives/wealth by starting wars. People suffer fear and disease.",
         "key_signals": {"regional": "Drought in North; South is well off", "note": "Grains must be imported"}},
        {"id": 58, "name": "Raktakshi",     "lord": "Venus",   "trinity": "Shiv",
         "general_result": "Rains and crops good. Rulers look at each other with anger. War-oriented atmosphere.",
         "key_signals": {"cheap_months": ["Chaitra","Baisakh","Jyeshtha","Aashadh","Ashwin"]}},
        {"id": 59, "name": "Krodhan",       "lord": "Saturn",  "trinity": "Shiv",
         "general_result": "Enmity among rulers. Violence excessive. In East, rains are more.",
         "key_signals": {"trader_alert": "Traders suffer in Paush"}},
        {"id": 60, "name": "Kshaya",        "lord": "Rahu",    "trinity": "Shiv",
         "general_result": "Crops of cotton, sugarcane, and oils destroyed. People are weak and thin.",
         "key_signals": {"riot_alert": "Riots in Chaitra and Baisakh", "health_alert": "Children's diseases in Jyeshtha/Aashadh; disease in Ashwin", "rain_note": "Bhadrapad devoid of rains; general rains less"}}
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT 5 — GAUR CH 1: SAMVATSAR BODY (ANATOMICAL CONSTELLATION MAPPING)
# ─────────────────────────────────────────────────────────────────────────────
GAUR_CH1_SAMVATSAR_BODY = {
    "spec_id": "gaur-ch1-samvatsar-body",
    "batch_id": BATCH_ID,
    "spec_type": "lookup_grid",
    "science_id": "mundane_jyotish",
    "title": "Gaur/AIFAS Ch 1 §4 — Samvatsar Body: Anatomical Constellation Mapping",
    "description": (
        "Maps 27 nakshatras to anatomical body parts of the Samvatsar figure (tortoise-like). "
        "Malefic affliction of these constellations at the start of a Samvatsar targets specific "
        "demographics and resources. Key trigger: Ashlesha (Heart) = Grain Supply Chain Risk; "
        "Magha (Flower/Hand) = children/entertainment; Ashadha nakshatras (Naval) = economic distress."
    ),
    "synthesis_sources": [
        {"book": "gaur_aifas", "chapter": "Ch 1", "label": "Parts of Samvatsars and Their Results"}
    ],
    "diagnostic_trigger": "Position of malefic planets (Sun, Mars, Saturn, Rahu, Ketu) at the moment of Samvatsar's commencement",
    "body_parts": [
        {
            "body_part": "Body (Trunk)",
            "constellations": ["Krittika", "Rohini"],
            "malefic_result": "Danger of wind (respiratory or atmospheric issues) to the people"
        },
        {
            "body_part": "Heart",
            "constellations": ["Ashlesha"],
            "malefic_result": "CRITICAL: Grain Supply Chain Risk — primary gate for agricultural and economic distress",
            "engine_note": "If a transit malefic occupies Ashlesha at Samvatsar start, flag 'Grain Supply Chain Risk' immediately."
        },
        {
            "body_part": "Navel",
            "constellations": ["Purva Ashadha", "Uttara Ashadha"],
            "malefic_result": "Economic distress at the centre of the nation; disruption to national financial core"
        },
        {
            "body_part": "Flower / Hand",
            "constellations": ["Magha"],
            "malefic_result": "Suffering among children, entertainers, and royalty; corruption of creative sectors"
        },
        {
            "body_part": "Head",
            "constellations": ["Ashwini", "Bharani"],
            "malefic_result": "Danger to heads of state, rulers, and military commanders"
        },
        {
            "body_part": "Eyes",
            "constellations": ["Punarvasu", "Pushya"],
            "malefic_result": "Blindness to public warnings; intelligence failures and misguided policy"
        },
        {
            "body_part": "Back / Rear",
            "constellations": ["Uttara Bhadrapada", "Purva Bhadrapada"],
            "malefic_result": "Danger to agricultural workers, the poor, and rural infrastructure"
        },
        {
            "body_part": "Legs / Feet",
            "constellations": ["Revati", "Shatabhisha"],
            "malefic_result": "Transport disruptions, border vulnerabilities, and pilgrim/travel hazards"
        }
    ],
    "polarized_outcome_rule": (
        "If the Samvatsar name implies prosperity (e.g., Eashwar) but the Lord's specific results "
        "show disaster (e.g., Rahu lord showing war and riots), the diagnostic should return a "
        "'Polarized Outcome': pockets of extreme wealth amidst regional violence."
    )
}

# ─────────────────────────────────────────────────────────────────────────────
# ALL DOCUMENTS
# ─────────────────────────────────────────────────────────────────────────────
ALL_SPECS = [
    MEHTA_CH5_PLANETARY_SIGNIFICATIONS,
    MEHTA_CH6_HOUSE_MINISTRY,
    RAPHAEL_CH3_WESTERN_HOUSES,
    GAUR_CH1_60_SAMVATSARS,
    GAUR_CH1_SAMVATSAR_BODY,
]

# ─────────────────────────────────────────────────────────────────────────────
# INGEST
# ─────────────────────────────────────────────────────────────────────────────
async def run():
    now = datetime.now(timezone.utc)
    for spec in ALL_SPECS:
        spec["ingested_at"] = now
        spec["approval_status"] = "pending_review"

    if DRY_RUN:
        print(f"\nBuilt {len(ALL_SPECS)} specs for batch {BATCH_ID}")
        print(f"Collection: mundane_engine_specs  |  science: mundane_jyotish\n")
        print("Spec IDs:")
        for s in ALL_SPECS:
            print(f"  {s['spec_id']}")
        print(f"\nTotal: {len(ALL_SPECS)}")
        print("\nDry run complete.")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    col = db["mundane_engine_specs"]
    inserted = updated = 0
    for spec in ALL_SPECS:
        result = await col.update_one(
            {"spec_id": spec["spec_id"]},
            {"$set": spec},
            upsert=True
        )
        if result.upserted_id:
            inserted += 1
        else:
            updated += 1
    client.close()
    print(f"Done. Inserted={inserted}  Updated={updated}  Batch={BATCH_ID}")

if __name__ == "__main__":
    asyncio.run(run())
