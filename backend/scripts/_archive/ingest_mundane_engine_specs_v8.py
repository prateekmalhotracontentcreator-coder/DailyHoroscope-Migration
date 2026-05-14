"""
Mundane Astrology — Engine Specs v8
Batch: mundane-engine-v8-20260506

Source: Raphael, "Mundane Astrology" (WITS e-group edition)
  Chapter 3  — The Twelve Mundane Houses, Their Power and Significations (pp.4-5)
  Chapter 4  — The Significations of the Planets (pp.5-6)
  Chapter 6  — The Mundane Maps (pp.7-8)
  Chapter 8  — Concerning the First House and the Planets Therein (pp.10-11)
  Chapter 9  — Concerning the Second House and the Planets Therein (pp.12-13)
  Chapter 10 — Concerning the Third House and the Planets Therein (pp.13-14)
  Chapter 11 — Concerning the Fourth House and the Planets Therein (Part 2, pp.2-3)
  Chapter 12 — Concerning the Fifth House and the Planets Therein (Part 2, pp.3-4)
  Chapter 13 — Concerning the Sixth House and the Planets Therein (Part 2, pp.4-5)
  Chapter 14 — Concerning the Seventh House and the Planets Therein (Part 2, pp.5-6)
  Chapter 15 — Concerning the Eighth House and the Planets Therein (Part 2, p.6)

Spec types: classification, lookup_table, rule_matrix
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
_BATCH     = "mundane-engine-v8-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ============================================================
# 1. TWELVE MUNDANE HOUSES — RAPHAEL WESTERN CLASSIFICATION  (Raphael Ch 3)
# ============================================================
RAPHAEL_CH3_12_MUNDANE_HOUSES = {
    "spec_id":      "raphael-ch3-12-mundane-houses-classification",
    "spec_type":    "classification",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "The Twelve Mundane Houses — Raphael Western Classification",
    "source_chapter": "Raphael Ch 3, pp.4-5",
    "notes": (
        "Raphael's Western mundane house classification. "
        "Note differences from Gopalakrishnan's Indian version (see gopal-ch9-national-chart-12-house-classification): "
        "Raphael's 3rd = Railways/Telegraph (not IT); 4th = Opposition party (not vehicles); "
        "10th = King/Royalty not just economic growth; 11th = Parliament/Legislation; "
        "12th = Prisons/Crime/Secret Foes (not just expenses). "
        "The strongest houses are the 1st, 10th, 7th and 4th (angular), then 2nd, 5th, 8th, 11th, "
        "then 3rd, 6th, 9th, 12th. The first, third and ninth are intellectual houses."
    ),
    "house_significance": {
        "1": (
            "The common people, public health, general conditions of the country, "
            "and state of home affairs generally. "
            "Represents the minds and general mood of the populace."
        ),
        "2": (
            "National Exchequer, Revenue, Stock Exchange, Banks, "
            "Commercial affairs and trade. "
            "The financial condition and wealth of the nation."
        ),
        "3": (
            "Railways and matters to do with them, traffic returns, stocks and shares; "
            "telegraph, telephone and postal affairs, locomotions and means of transit, "
            "motors, omnibuses; Books, newspapers and literary concerns. "
            "(In modern context: all communications infrastructure and media.)"
        ),
        "4": (
            "The weather, agriculture, crops and landed interest; "
            "mines, public buildings; and the Opposition party to the Government. "
            "The cusp of this house is taken specially into account in making prognostications "
            "regarding earthquakes, volcanic eruptions, etc."
        ),
        "5": (
            "Theatres, music halls and places of amusement, children, education, "
            "birth-rate, schools, morals and betting. "
            "Speculative ventures and entertainment industries."
        ),
        "6": (
            "Sickness, public health, Army and Navy, Warships; "
            "Working classes generally. "
            "The nature of the sickness affecting the country generally can be deduced "
            "from the planets in this house."
        ),
        "7": (
            "Foreign affairs, and relations with other Powers. "
            "War and international disputes. "
            "Marriages, divorces, foreign trade. "
            "Open enemies of the nation."
        ),
        "8": (
            "Mortality, death-rate, suicides. Privy Council. "
            "Deaths among notable people; national loss and grief."
        ),
        "9": (
            "Law courts, judges, clergy, religion, Colonial trade and affairs, "
            "Commercial powers, Science, Shipping, and matters to do therewith. "
            "Higher courts and long-distance/overseas matters."
        ),
        "10": (
            "The King, Royalty, Government, Ruling Powers, Aristocracy, "
            "Nobility and Society. "
            "The ruling administration and its prestige."
        ),
        "11": (
            "Parliament, House of Commons, Legislation. "
            "Legislative body and the making of laws."
        ),
        "12": (
            "Prisons, Workhouses, Hospitals, Asylums, Reformatories, "
            "Charitable Institutions; Crime, Murders, Criminals, Spies and Secret Foes. "
            "Hidden dangers, covert enemies, institutionalised suffering."
        ),
    },
    "house_strength_order": (
        "Strongest (angular): 1st, 10th, 7th, 4th. "
        "Succedent: 2nd, 5th, 8th, 11th. "
        "Cadent (weakest): 3rd, 6th, 9th, 12th. "
        "Intellectual houses: 1st, 3rd, 9th."
    ),
    "cusp_rule": (
        "If a planet is in a house, its position and aspects should be carefully noted. "
        "If no planet is placed therein, then the position and aspects of the ruler of the "
        "sign on the cusp of the house should be considered. This applies to all twelve houses."
    ),
    "created_at": _NOW,
}

# ============================================================
# 2. PLANETARY SIGNIFICATIONS — RAPHAEL WESTERN CLASSIFICATION  (Raphael Ch 4)
# ============================================================
RAPHAEL_CH4_PLANETARY_SIGNIFICATIONS = {
    "spec_id":      "raphael-ch4-planetary-significations-lookup",
    "spec_type":    "lookup_table",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Planetary Significations in Mundane Astrology — Raphael Classification",
    "source_chapter": "Raphael Ch 4, pp.5-6",
    "notes": (
        "In mundane astrology planets represent classes of people and domains of national life. "
        "The house position of the planet must be taken into chief account when judging. "
        "Example: Neptune in 10th = socialistic agitation against the King/Government; "
        "Neptune in 12th = scandals and unpleasant events connected with Institutions."
    ),
    "planet_significations": {
        "Sun": (
            "The King, Nobles, magistrates, judges and all persons in Authority and of Distinction, "
            "Cabinet ministers, and the like. Heads of state and government leaders."
        ),
        "Moon": (
            "The common people, women generally, crowds, "
            "and all matters of a common or public nature. "
            "Mass mood, popular sentiment, the ordinary citizenry."
        ),
        "Mercury": (
            "The literary world, newspapers, publishers, ambassadors, "
            "trade and commerce, and the intellectual world. "
            "Media, communication, diplomacy, and business."
        ),
        "Venus": (
            "The female sex, artists, musicians, marriage, children, and births. "
            "Social harmony, arts, entertainment, and birth-related matters."
        ),
        "Mars": (
            "Soldiers, surgeons, noted military and naval men, war, "
            "disputes, fire and incendiarism. "
            "Military action, aggression, violence, and emergency services."
        ),
        "Jupiter": (
            "The religious and judicial world, divines, judges, lawyers, "
            "bankers, merchants, etc. "
            "Prosperity, expansion, law, religion, and commerce."
        ),
        "Saturn": (
            "Elderly people, landowners, farmers, mines, coal, "
            "and the produce of the earth. "
            "Agriculture, resources, elderly population, and conservative institutions."
        ),
        "Uranus": (
            "Railways, societies and associations, gas and water companies, civic bodies, "
            "strikes, rioting, and the like. Aerial navigation and scientific discoveries. "
            "Also explosions, anarchy and nihilism. "
            "Sudden disruptions, modern technology, and revolutionary movements."
        ),
        "Neptune": (
            "Socialism, suffragettes, the smart set, plots, sedition, fraud and swindling, "
            "all illicit undertakings, bogus companies, and all the lower and more "
            "degrading forms of vice and wickedness. "
            "Deception, covert operations, drugs, and dissolution of norms."
        ),
    },
    "general_note": (
        "The particular house position of the planets must be taken into chief account. "
        "The house influence and planetary influence must be combined for accurate judgment. "
        "A planet in a house represents both the class of people signified by that planet "
        "and the affairs of the house in which it is placed."
    ),
    "created_at": _NOW,
}

# ============================================================
# 3. MUNDANE MAPS FRAMEWORK — INGRESS / LUNATION / ECLIPSE TYPES  (Raphael Ch 6)
# ============================================================
RAPHAEL_CH6_MUNDANE_MAPS_FRAMEWORK = {
    "spec_id":      "raphael-ch6-mundane-maps-framework",
    "spec_type":    "rule_matrix",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Mundane Maps Framework — Ingress / Lunation / Eclipse / Conjunction Rules",
    "source_chapter": "Raphael Ch 6, pp.7-8",
    "notes": (
        "Raphael enumerates 5 types of mundane maps (horoscopes). "
        "Each type has different duration of influence and area of application. "
        "Ingresses are the primary framework; lunations are subordinate (minute hand); "
        "eclipses are separately powerful and long-lasting; great conjunctions are most important of all."
    ),
    # ── Map type 1: Quarterly Ingresses
    "type_1_quarterly_ingresses": {
        "definition": (
            "Figures erected for the times of the Sun's entry into the four cardinal signs: "
            "Aries, Cancer, Libra, and Capricorn. These are called 'Ingresses.' "
            "The Aries ingress (Spring Equinox) is the most important — it is the basis "
            "or groundwork for all yearly predictions."
        ),
        "duration_by_rising_sign": {
            "cardinal_rising": (
                "If a Cardinal sign (Aries, Cancer, Libra, Capricorn) rises at the moment "
                "of the Sun's ingress: the figure has rule for THREE MONTHS only."
            ),
            "fixed_rising": (
                "If a Fixed sign (Taurus, Leo, Scorpio, Aquarius) rises: "
                "the figure influences the WHOLE of the entire twelve months following."
            ),
            "mutable_rising": (
                "If a Common/Mutable sign (Gemini, Virgo, Sagittarius, Pisces) rises: "
                "the figure has influence for the ensuing SIX MONTHS."
            ),
        },
        "application": (
            "Also cast for Sun's entry into Cancer, Libra, Capricorn to cover subsequent quarters. "
            "The Cancer ingress covers summer; Libra covers autumn; Capricorn covers winter."
        ),
    },
    # ── Map type 2: Lunations (New and Full Moons)
    "type_2_lunations": {
        "definition": (
            "Figures of the heavens erected for each New and Full Moon during the year. "
            "Judged two ways: "
            "(1) According to the planetary positions and aspects in the lunation figure itself. "
            "(2) By referring the planetary positions at the moment of each New and Full Moon "
            "to the previous quarterly ingress figure."
        ),
        "analogy": (
            "The quarterly figures are, as it were, the hour hand of the clock, "
            "while the lunations act as the minute hand."
        ),
        "new_vs_full_moon": (
            "If a New Moon falls nearest to the Sun's entry into Aries, then each succeeding "
            "New Moon during the year is considered. "
            "If a Full Moon falls nearest to this particular ingress, then the succeeding Full Moons "
            "should have preference. Their period of influence is only one month."
        ),
        "period": "One month per lunation figure.",
    },
    # ── Map type 3: Solar Eclipses
    "type_3_solar_eclipses": {
        "definition": (
            "Figures erected for the time of New Moon at any particular Solar eclipse. "
            "Should be calculated for the exact moment of New Moon, "
            "NOT for the time of Central eclipse."
        ),
        "duration_rule": (
            "KEY RULE: A Solar eclipse has a specific influence of its own "
            "lasting for AS MANY YEARS as the eclipse is HOURS IN LENGTH. "
            "E.g., a 3-hour solar eclipse has influence lasting 3 years."
        ),
        "area_of_effect": (
            "Effects are most powerful: "
            "(1) In those countries where the eclipse is actually visible. "
            "(2) In countries and cities ruled over by the sign in which the eclipse falls."
        ),
        "decanate_effects": (
            "Certain specific effects are attributed to the action of Solar eclipses "
            "in the thirty-six decanates of the Zodiac "
            "(detailed in a later chapter of Raphael's text)."
        ),
    },
    # ── Map type 4: Lunar Eclipses
    "type_4_lunar_eclipses": {
        "definition": (
            "Figures erected for the time of Lunar eclipses, which are in reality Full Moons. "
            "The exact moment of Full Moon is taken, not that of the middle of the eclipse."
        ),
        "duration_rule": (
            "KEY RULE: Lunar eclipses have a period of action extending over "
            "AS MANY MONTHS as the eclipse is HOURS IN DURATION. "
            "E.g., a 2-hour lunar eclipse has influence for 2 months."
        ),
        "strength_comparison": (
            "Lunar eclipses are important, but LESS SO than Solar eclipses. "
            "Solar eclipses last years; Lunar eclipses last months."
        ),
        "area_of_effect": (
            "Effects like Solar eclipses: chiefly observed in countries where the eclipse "
            "is visible, and in those places ruled by the sign in which the eclipse falls."
        ),
    },
    # ── Map type 5: Conjunctions and Oppositions of Major Planets
    "type_5_great_conjunctions_oppositions": {
        "definition": (
            "Figures erected for the time of conjunctions and oppositions of the planets "
            "Mars, Saturn, Jupiter, Uranus, and Neptune. "
            "The house and sign position of such conjunctions and oppositions are to be noted."
        ),
        "importance": (
            "These are extremely important configurations. "
            "Their effects are very pronounced and lasting. "
            "Great conjunctions (especially Jupiter-Saturn, Saturn-Uranus, Saturn-Neptune) "
            "are the most powerful mundane indicators of all."
        ),
        "subsidiary_note": (
            "Some of these are subsidiary to the Ingresses — the figures for the Sun's entry "
            "into the four cardinal signs are called Ingresses — but the Eclipses and great "
            "conjunctions have a very powerful and important influence on the destinies of Nations."
        ),
    },
    # ── Aspect orb rules
    "aspect_orbs": {
        "major_aspects": (
            "For planets (Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune) "
            "forming major aspects (conjunction, sextile, square, trine, opposition): "
            "orb = 5 degrees. "
            "Aspect begins when within 5 degrees and lasts until 5 degrees past exact."
        ),
        "sun_moon_orbs": "Sun and Moon: orb = 8 degrees for major aspects.",
        "minor_aspects": (
            "For minor aspects (semi-square, sesquiquadrate): "
            "Planets = 2 degrees; Sun and Moon = 3 degrees."
        ),
        "parallel": "Parallel: one degree either way for Sun, Moon, and Planets.",
        "aspect_strength_order": (
            "Conjunction and opposition are most powerful, then parallel, "
            "followed by square, then trine and sextile of about equal power, "
            "then semi-square and sesquiquadrate."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
# 4. PLANET-IN-HOUSE EFFECTS — HOUSES 1-8, KEY COMBINATIONS  (Raphael Ch 8-15)
# ============================================================
RAPHAEL_CH8_15_PLANET_IN_HOUSE_MATRIX = {
    "spec_id":      "raphael-ch8-15-planet-in-house-key-matrix",
    "spec_type":    "rule_matrix",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Planet-in-House Effects Matrix — Houses 1-8, Key Combinations (Raphael Ch 8-15)",
    "source_chapter": "Raphael Ch 8-15, Part 1 pp.10-14, Part 2 pp.2-6",
    "notes": (
        "For each house: when no planet is present, judge by the ruler of the sign on the cusp. "
        "Well-aspected planets mitigate malefic effects; afflicted planets amplify them. "
        "The house from which affliction comes shows the domain through which problems manifest. "
        "This matrix covers the key malefic and most actionable planet-house combinations."
    ),
    # ── FIRST HOUSE
    "house_1_general": "Represents common people, public health, general condition of country, state of home affairs.",
    "house_1_planets": {
        "benefic_general": (
            "Any benefic (Jupiter, Venus, well-aspected Sun/Moon) in 1st: "
            "general condition of the country and people will be good; "
            "affairs will improve; internal condition satisfactory."
        ),
        "malefic_general": (
            "Any malefic (Mars, Saturn, Uranus, Neptune) in 1st: "
            "much trouble in the country; things unsettled; health of people bad. "
            "If afflicted by other planets the evil is more marked."
        ),
        "Sun_well": "Sun well aspected in 1st: prosperous time for country; many benefits to people; improvement in affairs.",
        "Sun_afflicted": "Sun afflicted in 1st: disturbances between master and man; afflicts health of community.",
        "Moon_well": "Moon well aspected in 1st: activity and changes among the people; improvements to women and children; slight benefits of a public nature.",
        "Moon_afflicted": "Moon much afflicted in 1st: illness, unrest, and discontent.",
        "Mercury_well": "Mercury well aspected in 1st: much activity, increase of trade and work, new enterprises, intellectual gain to the community.",
        "Mercury_afflicted": "Mercury afflicted in 1st: much discontent, personal attacks, libel actions, much recrimination in popular press.",
        "Venus_well": "Venus well aspected in 1st: peaceful time; content and success in country; improvement in work connected with female sex.",
        "Venus_afflicted": "Venus badly aspected in 1st: want, vice and misery; trouble to feminine part of community; crimes against women and children.",
        "Mars_general": (
            "Mars in 1st: generally evil; discontent among the people, strikes, riots, "
            "fires and incendiarism, crime and ill-health. "
            "If well aspected: military activity, warlike tone among people, forceful/aggressive tendency."
        ),
        "Jupiter_well": "Jupiter well aspected in 1st: prosperity and success in the land; plenty of work; good for trade; numerous benefits to community.",
        "Jupiter_afflicted": "Jupiter afflicted in 1st: not so good; affects interests of people according to position of afflicting planet.",
        "Saturn_general": (
            "Saturn in 1st: very evil unless favourably aspected; much distress, discontent, "
            "want of work, loss of trade, poverty and general ill-health. "
            "If well aspected: steady, progressive attitude among the people — but rarely produces much good."
        ),
        "Uranus_general": (
            "Uranus in 1st: evil influence; strikes, rioting, violence, anarchy, turbulence, "
            "outrages against authority; assassinations, risings against authority, "
            "violent disturbances of the peace. "
            "Well aspected: inquiring attitude among people, desire for reforms."
        ),
        "Neptune_general": (
            "Neptune in 1st: unpleasant; much agitation among people, secret propaganda, "
            "socialism, vice, crime, suicides. "
            "Effects of turning things upside down, underhand/treacherous behaviour. "
            "Afflicted: fraud, swindling, vice and immorality."
        ),
        "new_moon_in_1st": (
            "New Moon falling in the ascendant: many changes in the country, much activity. "
            "Well aspected: many benefits to public at large. "
            "Afflicted: much unrest and discontent, ill-health among the people, affairs unsatisfactory."
        ),
    },
    # ── SECOND HOUSE
    "house_2_general": "National Exchequer, revenue, stock exchange, banks, commerce and trade.",
    "house_2_planets": {
        "Sun_well": "Sun well aspected in 2nd: favourable for revenue; increase of receipts; brighter outlook for money market.",
        "Sun_afflicted": "Sun afflicted in 2nd: great waste of public revenue; increase of taxation; heavy expenditure.",
        "Moon": "Moon in 2nd: great fluctuation in revenue and money market, stocks and shares. Well aspected: increase of receipts, improvement in financial conditions.",
        "Mercury_well": "Mercury well aspected in 2nd: gains in trade and commerce, benefits to revenue.",
        "Mercury_afflicted": "Mercury badly aspected in 2nd: losses through fraud and theft; sharp practice in money market.",
        "Venus_well": "Venus well aspected in 2nd: many benefits to nation in financial way; increase of receipts.",
        "Venus_afflicted": "Venus evilly aspected in 2nd: heavy losses, waste of national finances, bad for banks and commercial affairs.",
        "Mars": (
            "Mars in 2nd: losses on Stock Exchange, panics, bank failures; "
            "enormous expenditure and waste of public money. "
            "Military affairs will require large amounts of money — revenue seriously affected."
        ),
        "Jupiter_well": "Jupiter well aspected in 2nd: best influence; large increase of receipts, improvement in national finances, success in banking/commercial operations, may denote lessening of taxation.",
        "Jupiter_afflicted": "Jupiter afflicted in 2nd: heavy expenditure, bank failures, panics on Stock Exchange. One of the worst aspects to Jupiter is a square or opposition of Mars, especially in financial affairs.",
        "Saturn": (
            "Saturn in 2nd: very evil; poor revenue, decrease of receipts, financial stagnation, "
            "depression in securities and financial circles, general want of activity in all money matters. "
            "Afflicted: heavy depreciation of securities. Well aspected: gives a steadying tone to the money market."
        ),
        "Uranus": (
            "Uranus in 2nd: unexpected losses and equally unexpected gains to national revenue. "
            "Financial crashes, strange and unlooked-for occurrences in stock and share market, "
            "much uneasiness generally in financial circles."
        ),
        "Neptune": (
            "Neptune in 2nd: fraud and dishonesty, losses to revenue through illicit undertakings, "
            "theft, sharp practices, and everything underhand and secret. "
            "Evilly aspected: acts more forcibly."
        ),
        "lunation_well": "Lunation well aspected in 2nd: increased revenue, improvement in national exchequer, more prosperous time for stocks and shares, especially gilt-edged securities.",
        "lunation_afflicted": "Lunation evilly aspected in 2nd: heavy national expenditure, financial and bank failures, losses on Stock Exchange.",
    },
    # ── THIRD HOUSE
    "house_3_general": "Railways, postal/telegraph/telephone, locomotion, books, newspapers, literary concerns.",
    "house_3_planets": {
        "Mars": (
            "Mars in 3rd: particular relation to railways; accidents and fires; "
            "heavy expenses, losses, depreciation of railway securities. "
            "Much afflicted: causes discontent and agitation among employees, "
            "serious accidents not only on railways but also in other forms of locomotion. "
            "Adversely affects publishing concerns."
        ),
        "Saturn": (
            "Saturn in 3rd: much discontent among employees, depreciation of trade, "
            "falling off of receipts in railways and postal matters, accidents. "
            "General unsatisfactory state of affairs in all third house matters. "
            "Sure to cause illness and death among prominent people connected with publishing or literary affairs."
        ),
        "Uranus": (
            "Uranus in 3rd: particular reference to railways, telephonic and telegraphic affairs, motors. "
            "Accidents on railways, explosions, extraordinary occurrences. "
            "Strikes and insubordination among employees, thefts and disputes. "
            "Many troubles in postal matters."
        ),
        "Jupiter": "Jupiter in 3rd: favourable for railways; traffic returns will increase; wages and conditions of workers will improve; many improvements in postal affairs.",
        "Neptune": "Neptune in 3rd: much agitation among employees, plots and secret movements, socialistic projects, crime and fraud, losses in trade, falling off of returns. Cases of fraud and swindling will come to light.",
    },
    # ── FOURTH HOUSE
    "house_4_general": "Weather, agriculture, crops, mines, minerals, landed interest, Opposition party. 4th cusp = earthquakes/volcanic eruptions.",
    "house_4_planets": {
        "lunation_fixed_4th_cusp": (
            "EARTHQUAKE RULE: A Lunation falling in a fixed sign exactly on the cusp of the "
            "fourth house is a sign of a DISASTROUS EARTHQUAKE in whatever part of the world "
            "this position may occur."
        ),
        "Mars": (
            "Mars in 4th: troubles for the Government; fires in public buildings; "
            "mining disasters and earthquakes. "
            "Adversely affects land and agriculture generally. "
            "Building operations and property market will suffer. "
            "Much afflicted: evil greatly augmented."
        ),
        "Saturn": (
            "Saturn in 4th: obstacles and difficulties to the Government; "
            "affairs of the nation will not proceed smoothly. "
            "Causes bad weather for crops; adversely affects agricultural matters. "
            "Denotes mining disasters, EARTHQUAKES, depreciates value of land, disturbs property. "
            "Afflicted: evil very considerably increased."
        ),
        "Uranus": (
            "Uranus in 4th: especially evil; serious trouble to water companies; "
            "mining disasters and explosions in public buildings. "
            "Evil for the Government, bringing difficulties to them. "
            "Land, mining royalties, and taxation of land values — source of much trouble."
        ),
        "Jupiter_afflicted_fixed": (
            "Jupiter in 4th if much afflicted and in a fixed sign: "
            "may cause mining disasters and earthquakes, especially in those places "
            "where it is exactly on the cusp of the fourth house."
        ),
        "Neptune": (
            "Neptune in 4th: doubtful influence but being malefic will cause trouble. "
            "Special reference to all forms of socialistic agitation in respect to taxation "
            "of landlords, ground values, mining royalties. "
            "Much afflicted: considerable trouble to the Government."
        ),
        "Sun_well": "Sun well aspected in 4th: favourable for landed interest; benefits to agriculture.",
        "Sun_afflicted": "Sun afflicted in 4th: much trouble to the Government; loss of elections; difficult questions; evil for agriculture and land.",
        "Venus": "Venus in 4th: favourable; denoting fine weather, good crops, success in agricultural matters. Afflicted: damp and unseasonable weather, adverse effect on crops.",
        "lunation_well": "Lunation well aspected in 4th: strengthens hands of Opposition; Government will lose by-elections; benefits agriculture, crops, and landed interest.",
        "lunation_afflicted": "Lunation evilly aspected in 4th: bad weather, shortage of crops, much trouble in agricultural matters.",
    },
    # ── SIXTH HOUSE
    "house_6_general": "Public health, working classes, Army and Navy, Warships, Soldiers and Sailors. Nature of national sickness deduced from planets here.",
    "house_6_planets": {
        "Mars": (
            "Mars in 6th: very evil; feverish and inflammatory disease among the people, "
            "according to the nature of the sign in which Mars is placed. "
            "Also denotes fires and accidents on warships, and insubordination among sailors. "
            "Well aspected: effects mitigated; denotes some naval demonstration or naval review."
        ),
        "Saturn": (
            "Saturn in 6th: very evil; much ill-health among the populace, "
            "of the nature shown by the sign occupied by Saturn. "
            "Discontent and dissatisfaction among the lower classes and in the Navy. "
            "Afflicted: evils more prominent and severe."
        ),
        "Uranus": (
            "Uranus in 6th: many peculiar disorders among the people, according to the sign; "
            "explosions on warships, insubordination among sailors, mutiny. "
            "Serious accidents, explosions attended with loss of life and limb."
        ),
        "Neptune": (
            "Neptune in 6th: much vice and immorality among lower classes; "
            "socialistic propaganda. Affects Navy in same seditious manner; "
            "much unrest among sailors. Affects community health through "
            "increase of illicit habits, drug-taking, opium-smoking. "
            "Tends to produce scandals in naval and military circles."
        ),
        "Jupiter": "Jupiter in 6th: benefits public health, improves condition of working classes, shows benefits to the Navy. Afflicted: heavy expenditure in naval and military affairs.",
        "Venus": "Venus in 6th: favourable for lower classes and the Navy, improves their condition. Afflicted: much vice, want and misery; causes much illness.",
        "Moon": "Moon in 6th: shows much sickness among the populace, discontent and dissatisfaction. Causes disorder in the Navy; unless well aspected is not a good position.",
        "lunation_well": "Lunation well aspected in 6th: augurs well for affairs of this house.",
        "lunation_afflicted": "Lunation evilly aspected in 6th: health of people will suffer; much discontent among working classes.",
    },
    # ── SEVENTH HOUSE
    "house_7_general": "Foreign affairs, relations with other Powers, war and international disputes, marriages, divorces, foreign trade.",
    "house_7_planets": {
        "Mars": (
            "Mars in 7th: very powerful; grave danger of international disputes, "
            "disagreement with other Powers, unsatisfactory foreign relations, and DANGER OF WAR. "
            "DIRECTION OF ENEMY: the direction from which the enemy will come is shown "
            "from the position of Mars — Aries=East, Cancer=North, Libra=West, Capricorn=South. "
            "The sign in which Mars is placed shows which country is opposed to the nation "
            "(according to the country ruled by that sign)."
        ),
        "Saturn": (
            "Saturn in 7th: very unfavourable for foreign affairs; presages much trouble and "
            "difficulty in dealings with other Powers. Depression in foreign trade. "
            "If Venus afflicts: scandals, divorces, crimes against women. "
            "Next to Mars, most evil influence in relation to international affairs. "
            "Sure to cause long and grievous difficulties in relations with other countries, "
            "especially those ruled by the sign in which Saturn is placed."
        ),
        "Uranus": (
            "Uranus in 7th: awkward and unexpected complications of serious nature in foreign affairs. "
            "Much agitation against the country. "
            "If afflicted by Venus: crop of unsavoury scandals, divorces and law-suits."
        ),
        "Neptune": (
            "Neptune in 7th: treachery and double-dealing on part of Foreign Powers. "
            "Warns nation to be on guard against plots, schemes, secret attacks. "
            "Denotes scandals, divorces, crime and immorality in married life, "
            "unpleasant/disgusting episodes in law-courts."
        ),
        "Jupiter": "Jupiter in 7th: favourable for foreign relations and all 7th house matters; marriage rate will increase; many notable alliances. Afflicted: disputes with other Powers in connection with financial and trade questions.",
        "Venus": "Venus in 7th: peace and prosperity in foreign trade; increases marriage rate; many marriages in high life. Badly aspected: public scandals, divorces, crime against women.",
        "Moon": "Moon in 7th: favourable; increase in marriage rate, public ceremonies, honours to women. Afflicted: trouble in foreign affairs, scandals in home life, divorces.",
        "lunation_well": "Lunation well aspected in 7th: better relations with Foreign Powers.",
        "lunation_afflicted": "Lunation evilly aspected in 7th: disputes and complications with Foreign Powers.",
    },
    # ── EIGHTH HOUSE
    "house_8_general": "Mortality, death-rate, suicides, Privy Council. Deaths among notable people.",
    "house_8_planets": {
        "Sun": "Sun in 8th: denotes deaths among important people, Royalty, nobility, and the upper ten. If well aspected, success to the nation.",
        "Moon": "Moon in 8th: shows much mortality among common people, especially women. Much afflicted: panics, resulting in many deaths.",
        "Mercury_afflicted": "Mercury afflicted in 8th: deaths in literary and publishing circles, among children and young people. Shows activity and changes in the Privy Council.",
        "Venus": "Venus in 8th: gains to the Exchequer through death duties, but if afflicted will cause many deaths among females, artistic and musical people, notable ladies of the land.",
        "lunation_evilly": "Lunation evilly aspected in 8th: denotes deaths in high circles and amongst notable people, especially females.",
        "lunation_well": "Lunation well aspected in 8th: signifies gains to the nation through death duties.",
        "Mars_in_8th": (
            "Mars in 8th: deaths through violence, accidents and fire; "
            "high mortality rate especially in military/naval engagements. "
            "Changes or crises in the Privy Council."
        ),
        "Saturn_in_8th": (
            "Saturn in 8th: high mortality rate, epidemics, deaths among elderly and landowners. "
            "Oppressive measures relating to death duties and taxation. "
            "National grief and gloom."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
ALL_SPECS = [
    RAPHAEL_CH3_12_MUNDANE_HOUSES,
    RAPHAEL_CH4_PLANETARY_SIGNIFICATIONS,
    RAPHAEL_CH6_MUNDANE_MAPS_FRAMEWORK,
    RAPHAEL_CH8_15_PLANET_IN_HOUSE_MATRIX,
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
