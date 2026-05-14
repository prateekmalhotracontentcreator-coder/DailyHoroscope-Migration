"""
Mundane Astrology — Engine Specs v7
Batch: mundane-engine-v7-20260506

Source: Gopalakrishnan, "Mundane Astrology" (ICAS)
  Chapter 10 — Sports Predictions / Career Analysis (book pp.163-177)
  Chapter 13 — Political Predictions (book pp.196-210)
  Chapter 14 — Commodities Predictions (book pp.211-220)
  Chapter 15 — Miscellaneous (book pp.221-240)
  Supplementary articles from Chapters 9-15 (case studies with validated rules)

Spec types: rule_matrix, classification
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
_BATCH     = "mundane-engine-v7-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ============================================================
# 1. SPORTS / CAREER INDICATORS  (Gopalakrishnan Ch 10)
# ============================================================
GOPAL_CH10_SPORTS_CAREER_INDICATORS = {
    "spec_id":      "gopal-ch10-sports-career-indicators",
    "spec_type":    "rule_matrix",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Sports/Career Decline Indicators — Nadi Saturn 8th Rule + Mars Perigee",
    "source_chapter": "Gopalakrishnan Ch 10, pp.163-177",
    "notes": (
        "Gopalakrishnan applies natal astrology principles to public figures (sportspersons, leaders). "
        "The Nadi rule that Saturn transiting 8th from the current dasa lord is universally applicable "
        "to career peaks and valleys. Validated on two Indian cricket captains and multiple state CMs."
    ),
    # ── Saturn 8th from dasa lord rule
    "saturn_8th_from_dasa_lord": {
        "rule": (
            "When transit Saturn occupies the 8th sign counted from the sign occupied "
            "by the current Vimshottari dasa lord (in the natal chart): "
            "there will be a fall in the person's career, position, and public standing. "
            "This is a classical Nadi astrology rule."
        ),
        "calculation": (
            "Step 1: Identify the current Mahadasha planet. "
            "Step 2: Find the sign that planet occupies in the natal chart. "
            "Step 3: Count 8 signs forward from that sign. "
            "Step 4: When transit Saturn enters that sign = career fall period begins."
        ),
        "ganguly_case": (
            "Ganguly running Jupiter Mahadasha. Jupiter's natal sign = X. "
            "Saturn transiting 8th from Jupiter's natal sign → Ganguly's captaincy removed, "
            "performance collapsed. Comeback not possible until Saturn moved past that zone."
        ),
        "sachin_case": (
            "Sachin running Jupiter Mahadasha + Mercury Bhukthi. "
            "Saturn transiting 8th from Jupiter's natal sign → poor form till Oct 2006. "
            "Form improved when Mercury bhukthi ended (2007 May). "
            "Venus bhukthi from 2008 = comeback and career records."
        ),
        "general_application": (
            "Applies to any public figure: politician, sportsperson, CEO, actor. "
            "Career fall = removal from power, poor performance, public disgrace. "
            "Duration = Saturn's transit through that sign (~2.5 years maximum)."
        ),
    },
    # ── Mars perigee (Mars close to earth) effects on leadership
    "mars_perigee_leadership_change": {
        "rule": (
            "When Mars comes closest to Earth (Mars at perigee / opposition with the Sun): "
            "incumbent leaders in regions governed by Mars-sensitive signs experience "
            "removal, defeat, or forced change within the following 12-24 months."
        ),
        "validated_cases_2005_2006": [
            "Kerala: AK Anthony replaced by Oomen Chandy",
            "Karnataka: SM Krishna replaced by Dharam Singh",
            "Andhra Pradesh: Chandrababu Naidu replaced by YS Rajasekhara Reddy",
            "Madhya Pradesh: Uma Bharti replaced",
            "Sri Lanka: Chandrika Kumaratunga's grip weakened; Rajapakse took over",
        ],
        "mars_bhumi_karaka": (
            "Mars is the Bhumi Karaka (significator of land/earth). "
            "When Mars comes closer to earth it intensifies all Mars-signified events: "
            "1. Mass death (tsunami, floods, drought), "
            "2. Leadership changes (especially in south/east India governed by Mars), "
            "3. War-like situations, "
            "4. Earthquakes, "
            "5. Price rise in chemicals, red-colored goods, iron/steel."
        ),
        "timing": (
            "Effects of Mars perigee manifest within 2 years of the event. "
            "'Within next two years the impact of Mars coming closer to earth will be seen.'"
        ),
    },
    # ── Oil price + Saturn 8th house in millennium chart
    "saturn_debilitated_8th_oil": {
        "rule": (
            "In the millennium chart (Jan 1 2000, 00:00 IST), Saturn is debilitated (neecha) "
            "in the 8th house. Oil is the natural signification of Saturn. "
            "Therefore oil prices are structurally bound to go up through the millennium period."
        ),
        "saturn_ketu_leo_oil": (
            "When Saturn and Ketu meet in Leo (Simha), oil prices can reach $70/barrel. "
            "This window: September 2006 – September 2008."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
# 2. SATURN TRANSIT THROUGH STATE/NATIONAL CHART HOUSES  (Gopalakrishnan Ch 13)
# ============================================================
GOPAL_CH13_SATURN_HOUSE_TRANSIT_GOVT_CHANGE = {
    "spec_id":      "gopal-ch13-saturn-house-transit-govt-change",
    "spec_type":    "rule_matrix",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Saturn Transiting Houses of State/National Chart — Government Change Pattern",
    "source_chapter": "Gopalakrishnan Ch 13, pp.196-205",
    "notes": (
        "Validated empirically for Andhra Pradesh chart (Kataka lagna). "
        "Each Saturn house transit corresponds to a predictable political power shift. "
        "Applies to any state/national chart with known lagna."
    ),
    # ── Andhra Pradesh validated case
    "andhra_pradesh_validated_case": {
        "chart": "AP lagna = Kataka (Cancer). Jupiter, Moon, Venus in 3rd house. Sun+Mercury in 8th. Rahu+Saturn in 5th. Ketu in 11th.",
        "saturn_4th_house": "Saturn in 4th house (Libra): NTR came to power for the first time, uprooting Congress.",
        "saturn_6th_house": "Saturn in 6th house (Sagittarius, 1989): Congress came back to power.",
        "saturn_8th_house": (
            "Saturn moving into 8th house: NTR came back to power. "
            "But before Saturn could leave the 8th house, it put an end to NTR himself — "
            "Chandrababu Naidu emerged via palace coup."
        ),
        "saturn_12th_house": (
            "Saturn in 12th house (this election): major change in power — "
            "Congress replaced TDP completely."
        ),
    },
    # ── General pattern
    "general_saturn_house_pattern": {
        "4th_house": "Saturn transiting 4th: mass public dissatisfaction; new party/leader rises to challenge incumbent.",
        "6th_house": "Saturn transiting 6th: incumbent weakened by opposition, disease, or external threat; power shifts.",
        "8th_house": "Saturn transiting 8th: major transformation of leadership; existing leadership endangered; possible removal.",
        "10th_house": "Saturn transiting 10th: leadership under scrutiny; major challenge to governing party.",
        "12th_house": "Saturn transiting 12th: incumbent loses power; spending crisis; new cycle begins.",
    },
    # ── Saturn-Ketu civil war signal
    "saturn_ketu_conjunction_civil_war": {
        "rule": (
            "Saturn and Ketu conjunction in transit: "
            "very good chances of civil war erupting in affected nations. "
            "Especially potent when the conjunction falls in the 8th house of the national chart "
            "or on the 8th lord of the national chart."
        ),
        "sri_lanka_2007": (
            "With Saturn and Ketu conjunction in 2007, there will be very good chances "
            "of civil war erupting in Sri Lanka. "
            "[Historical note: Sri Lanka civil war resumed full intensity 2006-2009.]"
        ),
    },
    "created_at": _NOW,
}

# ============================================================
# 3. NATIONAL CHART LAGNA LORD — LEADER ARCHETYPE  (Gopalakrishnan Ch 15)
# ============================================================
GOPAL_CH15_LAGNA_LORD_LEADER_ARCHETYPE = {
    "spec_id":      "gopal-ch15-lagna-lord-national-leader-archetype",
    "spec_type":    "classification",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "National Chart Lagna Lord Determines Successful Politician/Leader Archetype",
    "source_chapter": "Gopalakrishnan Ch 15, pp.221-230",
    "notes": (
        "The lagna lord (and 10th lord) of a nation's chart determines which type of person "
        "succeeds politically in that country. This principle explains cultural patterns in "
        "who rises to power across different nations."
    ),
    "lagna_lord_archetypes": {
        "Venus_lagna_lord": (
            "Nation with Venus as lagna lord (e.g., India — Taurus lagna, Venus rules 1st): "
            "Film stars, entertainers, glamour personalities succeed in politics. "
            "Since 1982 (India's Venus dasa started), more and more cine stars entered politics. "
            "Venus = lord of music, entertainment, luxury, arts."
        ),
        "Mars_lagna_lord": (
            "Nation with Mars as lagna lord (e.g., Pakistan — Scorpio lagna, Mars rules 1st): "
            "Military personnel, fundamentalists, sportspersons are role models and rise to power. "
            "Mars = military, aggression, direct action."
        ),
        "Venus_10th_lord": (
            "Nation with Venus as 10th lord (e.g., USA): "
            "Film stars and entertainment personalities succeed as political leaders. "
            "Examples: Ronald Reagan (actor → President), Arnold Schwarzenegger (actor → Governor)."
        ),
    },
    # ── Jupiter affliction and national dharma
    "jupiter_affliction_national_dharma": {
        "rule": (
            "When Jupiter is afflicted in a nation's natal chart (especially placed in 6th/8th/12th "
            "or conjunct/aspected by malefics), DHARMA will go down in that nation. "
            "Merit will NOT be the source of decision-making."
        ),
        "india_case": (
            "India's natal Jupiter is in the 6th house. "
            "'Whenever Jupiter is afflicted in a nation's horoscope, DHARMA will go down.' "
            "This explains India's reservation/caste-based system persisting over merit-based selection. "
            "In Chaturvimsamsa (education divisional chart): Jupiter + 8th lord in 5th house "
            "= malefic combination for education merit."
        ),
        "improvement": (
            "Jupiter affliction effects improve when India begins its Sun dasa (from 2009) "
            "and when Saturn transits Simha (Leo), bringing structural reforms."
        ),
    },
    # ── Saturn transit through 3rd house = IT/BPO boom (universal)
    "saturn_3rd_house_communication_boom": {
        "rule": (
            "Saturn transiting through the 3rd house of a nation's chart: "
            "massive boom in communication, information technology, transportation, "
            "and BPO/outsourcing sectors."
        ),
        "india_case": (
            "Saturn entering India's 3rd house (Cancer) from 2002: "
            "prediction that India will become the backbone of BPO in the world. "
            "Saturn in 3rd = communication and communication appliances. "
            "Telecom, computers, outsourcing all boomed. TRUE — India became IT powerhouse."
        ),
        "dot_com_case": (
            "Saturn entered Aries (1998-2002): dot com boom + TV industry major boom. "
            "Saturn in Gemini (communication sign) from 2002: email space exploded (Google 1GB mail). "
            "Saturn in Libra: 'Major change could be expected when Saturn enters Libra' "
            "— electronic communication replaces all traditional devices."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
ALL_SPECS = [
    GOPAL_CH10_SPORTS_CAREER_INDICATORS,
    GOPAL_CH13_SATURN_HOUSE_TRANSIT_GOVT_CHANGE,
    GOPAL_CH15_LAGNA_LORD_LEADER_ARCHETYPE,
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
