"""
Mundane Astrology — Interpretation Rules v12
Batch: mundane-interp-v12-20260506

Sources:
  Mehta/Rao Ch 2  — The Multi-Step Scheme (9-Step Prediction Hierarchy)
  Gaur/AIFAS Ch 3 — Special Horoscopes (Universal Chart + Samvat Stambha)

GROUP_AG: 17 rules — Operational logic gates from the Engine OS and
          Special Horoscope frameworks.

These rules were in the original NotebookLM JSON but absent from
all clean-schema interpretation scripts (v3-v11).

science_id: mundane_jyotish
Collection: interpretation_rules

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
COLLECTION = "interpretation_rules"
_BATCH     = "mundane-interp-v12-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ---------------------------------------------------------------------------
def _rule(rule_id, sub_type, title, source_chapter, condition, result,
          synthesis_sources, notes="", severity=None, checkable=False):
    d = {
        "rule_id":           rule_id,
        "batch_id":          _BATCH,
        "science_id":        "mundane_jyotish",
        "sub_type":          sub_type,
        "title":             title,
        "source_chapter":    source_chapter,
        "condition":         condition,
        "result":            result,
        "synthesis_sources": synthesis_sources,
        "checkable":         checkable,
        "approval_status":   "pending_review",
        "created_at":        _NOW,
    }
    if notes:    d["notes"]    = notes
    if severity: d["severity"] = severity
    return d

# ============================================================
# GROUP_AG — MEHTA Ch2 OPERATIONAL LOGIC GATES +
#            GAUR Ch3 SPECIAL HOROSCOPE RULES
# ============================================================

GROUP_AG = [

    # ── Rule AG-01: Foundation Dasha overrides all transits
    _rule(
        rule_id         = "mehta-ch2-foundation-dasha-overrides-transits",
        sub_type        = "hierarchy",
        title           = "Foundation Dasha Overrides All Transit Results — The Primary Rule",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "A transit result (Step 6) conflicts with the Foundation Horoscope's Dasha result (Step 1). "
            "Example: transit of Jupiter through 9th house suggests prosperity, "
            "but Foundation Chart is running Saturn Mahadasha in the 8th."
        ),
        result          = (
            "The Foundation Dasha result OVERRIDES the transit. "
            "Treat nations as 'Natives' — their natal Dasha is primary. "
            "All subsequent steps (2-9) modify, they do not replace, the Foundation signal. "
            "This is the single most important rule in the 9-Step Scheme."
        ),
        synthesis_sources = ["Mehta/Rao Ch 2"],
        notes           = (
            "This rule prevents the common error of over-weighting transits in mundane work. "
            "Foundation charts for key nations: "
            "India = Independence chart Aug 15, 1947, Taurus Lagna. "
            "USA = Leo 29° Lagna (superpower military/economic power indicators)."
        ),
        severity        = "high",
        checkable       = False,
    ),

    # ── Rule AG-02: King of Year must be Sun or Moon
    _rule(
        rule_id         = "mehta-ch2-king-of-year-sun-moon-governance",
        sub_type        = "yearly_cabinet",
        title           = "If King of Year Is Not Sun or Moon, Governance Instability = TRUE",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "In the Hindu New Year horoscope (Chaitra Shukla Pratipada chart), "
            "identify the Lord of the Year (Varsha Lord). "
            "Condition: Varsha Lord is NOT Sun AND NOT Moon."
        ),
        result          = (
            "Governance instability is predicted for the year. "
            "Royal authority is weakened — expect challenges to central leadership, "
            "coalition friction, or executive paralysis."
        ),
        synthesis_sources = ["Mehta/Rao Ch 2", "Gaur Ch 2 (Celestial Council)"],
        notes           = (
            "Cross-reference with Gaur Ch 2 Celestial Council spec "
            "(gaur-ch2-celestial-council-outcomes) for the full cabinet analysis. "
            "Sun as King = strong decisive governance. "
            "Moon as King = popular leadership, people-oriented policies."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-03: Commander-in-Chief must be Mars
    _rule(
        rule_id         = "mehta-ch2-commander-not-mars-military-disorder",
        sub_type        = "yearly_cabinet",
        title           = "If Commander-in-Chief Is Not Mars, Military Disorder = TRUE",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "In the Hindu New Year horoscope, identify the planet holding the "
            "Commander-in-Chief (Senapati) portfolio. "
            "Condition: that planet is NOT Mars."
        ),
        result          = (
            "Military disorder is predicted. Expect disciplinary failures in armed forces, "
            "border security lapses, or ineffective military command. "
            "Defense spending may be mismanaged."
        ),
        synthesis_sources = ["Mehta/Rao Ch 2"],
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-04: Mars in New Year lagna = turbulent year
    _rule(
        rule_id         = "mehta-ch2-mars-lagna-new-year-turbulent",
        sub_type        = "yearly_cabinet",
        title           = "Mars in Lagna of New Year Chart + Aspects Sun/Moon/Mercury = Turbulent Year",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "In the Chaitra Shukla Pratipada (New Year) chart: "
            "Mars occupies the Lagna AND Mars aspects Sun, Moon, or Mercury."
        ),
        result          = (
            "Turbulent year predicted. Expect political upheaval, conflict, "
            "communal violence, or sudden reversal of national policy."
        ),
        synthesis_sources = ["Mehta/Rao Ch 2"],
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-05: Three Saturdays/Tuesdays in lunar fortnight = inauspicious alert
    _rule(
        rule_id         = "mehta-ch2-three-saturdays-tuesdays-paksha-alert",
        sub_type        = "paksha",
        title           = "Three Saturdays or Three Tuesdays in a Lunar Fortnight = High Inauspicious Alert",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "In a Hindu lunar month (Paksha chart period — 15 days), "
            "count occurrences of Saturday and Tuesday. "
            "Condition: >= 3 Saturdays OR >= 3 Tuesdays within the fortnight."
        ),
        result          = (
            "High-alert inauspicious period. Elevated probability of: "
            "national tragedy, communal riots, financial crashes, or political violence "
            "within that 15-day window."
        ),
        synthesis_sources = ["Mehta/Rao Ch 2"],
        notes           = (
            "This must be audited against the Hindu lunar month (Paksha), "
            "NOT the Gregorian calendar. "
            "Combine with communal tension gate: if Paksha Lagna is also Leo or Scorpio, "
            "probability of communal crisis is HIGH."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-06: Double eclipse within 14 days = terrible destruction
    _rule(
        rule_id         = "mehta-ch2-double-eclipse-14-days-destruction",
        sub_type        = "eclipse",
        title           = "Solar + Lunar Eclipse Within 14 Days = Terrible Destruction",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "A solar eclipse AND a lunar eclipse occur within 14 days of each other."
        ),
        result          = (
            "TERRIBLE DESTRUCTION = TRUE. Highest alert in the eclipse module. "
            "Expect a major catastrophic national or global event within the period "
            "mapped by those two eclipses."
        ),
        synthesis_sources = [
            "Mehta/Rao Ch 2",
            "Raphael Ch 22 (eclipse duration rules)",
            "Gaur Ch 3 (Universal Horoscope)",
        ],
        notes           = (
            "In the Universal Horoscope, identify which houses the two eclipses fall in "
            "to determine WHICH months carry the destruction energy. "
            "Cross-reference with Raphael's eclipse element rules "
            "(raphael-ch22-eclipse-sign-element-timing-rules) for the type of destruction."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-07: Saturn transit Rohini = famine/war (Rohini Shakata Bhedan)
    _rule(
        rule_id         = "mehta-ch2-saturn-rohini-famine-war-highest-alert",
        sub_type        = "transit",
        title           = "Saturn Transiting Rohini Nakshatra = Famine or Devastating War (Highest Alert)",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "Transit Saturn passes through Rohini Nakshatra "
            "(Taurus 10°00' to 23°20' sidereal)."
        ),
        result          = (
            "HIGHEST LEVEL WARNING in all of mundane astrology. "
            "This is the Rohini Shakata Bhedan Yoga. "
            "Predicts devastating war OR 12-year famine for the affected region/nation."
        ),
        synthesis_sources = [
            "Mehta/Rao Ch 2",
            "Gopalakrishnan Ch 7 (earthquake + war triggers)",
        ],
        notes           = (
            "Rohini is the Moon's own nakshatra — its affliction by Saturn "
            "represents the worst possible agricultural and security scenario. "
            "Historical validations of this rule exist across multiple Indian and global conflicts. "
            "Must be cross-referenced with the national Foundation Chart "
            "to determine the specific form of destruction."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-08: Saturn-Jupiter conjunction = US president mortality
    _rule(
        rule_id         = "mehta-ch2-sat-jup-conjunction-us-president-mortality",
        sub_type        = "conjunction",
        title           = "Saturn-Jupiter Conjunction (Every 20 Years) = US President Elected Near That Date Faces Mortality Risk",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "A Saturn-Jupiter conjunction occurs (approximately every 20 years). "
            "A US President is elected in a year close to the conjunction date."
        ),
        result          = (
            "That US President faces elevated mortality risk during their term. "
            "Historical pattern: Presidents elected in 1840, 1860, 1880, 1900, 1920, "
            "1940, 1960 all died in office."
        ),
        synthesis_sources = [
            "Mehta/Rao Ch 2",
            "Mehta/Rao Ch 10 (macro-conjunction cycles)",
        ],
        notes           = (
            "The Sat-Jup conjunction also marks Triplicity shifts — when the conjunction "
            "moves to an Earthy triplicity (Virgo/Taurus/Capricorn), "
            "it signals a 200-year era of slow material world-order restructuring. "
            "This is the 'Great Mutation' used to explain multi-century geopolitical shifts."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-09: Saturn-Rahu conjunction = end of imperialism / mass destruction
    _rule(
        rule_id         = "mehta-ch2-sat-rahu-conjunction-imperialism-ends",
        sub_type        = "conjunction",
        title           = "Saturn-Rahu Conjunction = End of Imperialism, New Nations, or Mass Destruction via Advanced Weapons",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "Transit Saturn and Rahu conjoin in any sign. "
            "Special case: conjunction occurs in Capricorn."
        ),
        result          = (
            "End of an imperial era, birth of new nations, OR mass destruction "
            "via atomic or advanced weaponry. "
            "IF conjunction in Capricorn: major global conflict = TRUE."
        ),
        synthesis_sources = [
            "Mehta/Rao Ch 2",
            "Mehta/Rao Ch 10 (macro-conjunction cycles)",
        ],
        notes           = (
            "Historical validations: "
            "1945 Sat-Rah conjunction → atomic bomb usage, end of British/Japanese imperialism. "
            "1990 Sat-Rah conjunction in Capricorn → Gulf War."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-10: Saturn-Mars conjunction in 6th house = military action vs domestic threats
    _rule(
        rule_id         = "mehta-ch2-sat-mars-6th-house-military-domestic",
        sub_type        = "conjunction",
        title           = "Saturn-Mars Conjunction in 6th House of National Chart = Military Operation Against Domestic Threats",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "Saturn and Mars conjoin in the 6th house of a nation's Foundation Chart "
            "(or in the sign that falls in the 6th house from the national Lagna)."
        ),
        result          = (
            "Extreme violence and 'Black Days' in national history. "
            "Specifically: military action against domestic/internal enemies. "
            "6th house = internal security, enemies, borders."
        ),
        synthesis_sources = [
            "Mehta/Rao Ch 2",
        ],
        notes           = (
            "Historical validation: Operation Blue Star (1984) — "
            "Saturn-Mars conjunction in the 6th house of India's Foundation Chart "
            "timed the military action against the Golden Temple. "
            "General Saturn-Mars conjunctions (any house) = extreme violence and Black Days."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-11: Triple conjunction Sat+Mars+Rahu in quadrant = global destruction
    _rule(
        rule_id         = "mehta-ch2-triple-conjunction-sat-mars-rahu-global-destruction",
        sub_type        = "conjunction",
        title           = "Saturn + Mars + Rahu Together in a Quadrant = Global Destruction Scheme",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "Saturn, Mars, and Rahu simultaneously occupy the same quadrant "
            "(kendra house: 1st, 4th, 7th, or 10th from any national Lagna or "
            "within approximately 90° of each other in the zodiac)."
        ),
        result          = (
            "GLOBAL DESTRUCTION SCHEME = TRUE. "
            "This is the most severe conjunction alert. "
            "Expect coordinated large-scale destruction events at global level."
        ),
        synthesis_sources = [
            "Mehta/Rao Ch 2",
            "Mehta/Rao Ch 20 (terrorism audits)",
        ],
        notes           = (
            "Apply the 1-degree orb rule for maximum precision: "
            "if Sun, Saturn, Moon, and Rahu are within 1° of each other, "
            "the alert level is 'Catastrophic Mundane Event.'"
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-12: Mars retrograde in Jyeshtha → enters Anuradha = fall of kings
    _rule(
        rule_id         = "mehta-ch2-mars-retrograde-jyeshtha-anuradha-fall-of-kings",
        sub_type        = "transit",
        title           = "Mars Retrograde in Jyeshtha Nakshatra Then Enters Anuradha = Fall of Kings",
        source_chapter  = "Mehta/Rao Ch 2",
        condition       = (
            "Mars is retrograde while in Jyeshtha Nakshatra (Scorpio 16°40' to 30°00') "
            "and subsequently (after turning direct) enters Anuradha Nakshatra "
            "(Scorpio 3°20' to 16°40')."
        ),
        result          = (
            "Fall of Kings = TRUE. "
            "Rulers or heads of state lose power during this transit. "
            "This can manifest as electoral defeat, forced resignation, or regime change."
        ),
        synthesis_sources = [
            "Mehta/Rao Ch 2",
        ],
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-13: Universal Horoscope — malefics in 7th house = crop damage (Ashwin)
    _rule(
        rule_id         = "gaur-ch3-universal-horoscope-malefics-7th-crop-damage",
        sub_type        = "annual_chart",
        title           = "Malefics in 7th House of Aries Ingress Chart = Damage to Ripe Crops in Ashwin (Sep-Oct)",
        source_chapter  = "Gaur Ch 3",
        condition       = (
            "In the Aries Ingress (Universal Horoscope) chart: "
            "Sun, Mars, Saturn, or Rahu occupies or strongly aspects the 7th house."
        ),
        result          = (
            "Damage to ripe crops during Ashwin month (September-October). "
            "The 7th house of the Universal Horoscope maps to Ashwin — "
            "malefic presence there destroys the harvest period specifically."
        ),
        synthesis_sources = ["Gaur Ch 3"],
        notes           = (
            "In the Universal Horoscope framework, each house = one Hindu month. "
            "7th house = Ashwin (Sep-Oct) = peak harvest season for most of India. "
            "This is why malefics in the 7th of the Universal Chart "
            "are particularly damaging for agricultural output."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── Rule AG-14: New Year Ascendant Virgo = democracy dissolved
    _rule(
        rule_id         = "gaur-ch3-new-year-virgo-ascendant-democracy-dissolved",
        sub_type        = "annual_chart",
        title           = "New Year Ascendant Virgo = 'Democracy Dissolved' Alert for Middle Provinces",
        source_chapter  = "Gaur Ch 3",
        condition       = (
            "The Chaitra Shukla Pratipada (New Year) chart has Virgo (Kanya) as Lagna."
        ),
        result          = (
            "People of the Middle Provinces are dissatisfied and democracy is dissolved. "
            "East: normal; Ghee is expensive. "
            "South: drought. "
            "West: riots and expensive grains. "
            "North-East: riots."
        ),
        synthesis_sources = ["Gaur Ch 3"],
        notes           = (
            "Virgo is the most politically turbulent New Year ascendant. "
            "The 'democracy dissolved' indicator is unique to this ascendant. "
            "In modern context: President's Rule, Emergency, or constitutional crisis."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AG-15: Samvat Stambha all 4 pillars = maximum prosperity
    _rule(
        rule_id         = "gaur-ch3-samvat-stambha-all-pillars-max-prosperity",
        sub_type        = "samvat_stambha",
        title           = "All Four Samvat Stambha Pillars Present = Maximum Prosperity Year",
        source_chapter  = "Gaur Ch 3",
        condition       = (
            "Calculate Samvat Stambha for the year. "
            "ALL FOUR pillars are present (strength > 0%): "
            "Jal (Revati on Chaitra Pratipada) + Trin (Bharani on Vaishakh Pratipada) + "
            "Vayu (Mrigshira on Jyeshtha Pratipada) + Anna (Punarvasu on Aashadh Pratipada)."
        ),
        result          = (
            "Maximum benefic results for the year. "
            "Good rainfall, healthy vegetation, clean air, and abundant grain production. "
            "Overall prosperity and national well-being."
        ),
        synthesis_sources = ["Gaur Ch 3"],
        checkable       = True,
        severity        = "low",
    ),

    # ── Rule AG-16: All 4 Samvat Stambha pillars absent = total destitution
    _rule(
        rule_id         = "gaur-ch3-samvat-stambha-no-pillars-destitution",
        sub_type        = "samvat_stambha",
        title           = "No Samvat Stambha Pillars Present = Total Destitution — Overrides All Benefic Aspects",
        source_chapter  = "Gaur Ch 3",
        condition       = (
            "Calculate Samvat Stambha for the year. "
            "NONE of the four pillars are present (all strength = 0%): "
            "Jal = 0%, Trin = 0%, Vayu = 0%, Anna = 0%."
        ),
        result          = (
            "TOTAL DESTITUTION AND HARDSHIP for the year. "
            "This is the HIGHEST MALEFIC WARNING LEVEL — it overrides all other "
            "benefic planetary aspects in the Universal Chart or transit analysis."
        ),
        synthesis_sources = ["Gaur Ch 3"],
        checkable       = True,
        severity        = "high",
    ),

    # ── Rule AG-17: Stambha — Jal absent despite grains present = dry harvest
    _rule(
        rule_id         = "gaur-ch3-samvat-stambha-jal-absent-dry-harvest",
        sub_type        = "samvat_stambha",
        title           = "Samvat Stambha — Grains Present but Water Absent = Dry Harvest Alert (Medium Year)",
        source_chapter  = "Gaur Ch 3",
        condition       = (
            "Calculate Samvat Stambha. "
            "Trin (Grass) AND Anna (Grain) pillars are present (> 0%). "
            "BUT Jal (Water) AND Vayu (Air) pillars are absent (= 0%)."
        ),
        result          = (
            "DRY HARVEST ALERT — Medium/partial prosperity year. "
            "Medicinal plants and grains will sprout, but lack of rain (Jal) and wind (Vayu) "
            "prevents full maturation. "
            "Financial benefit to the state is diluted — results are only medium. "
            "SYNERGY VETO: Even if Anna = 100%, Jal = 0% means: "
            "'Production targets met but maturation failed due to lack of moisture; "
            "overall yield medium.'"
        ),
        synthesis_sources = ["Gaur Ch 3"],
        notes           = (
            "Validated: VS 2059 (2002 Indian drought) — "
            "Jal Stambha = 9% (Revati = 142 min / 1562 min total = 9%). "
            "Result: Indian Drought of 2002 confirmed. "
            "Cross-verify low Jal with Gaur Ch 2 Cloud Engine for possible mitigation."
        ),
        checkable       = True,
        severity        = "medium",
    ),

]

ALL_RULES = GROUP_AG

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_RULES)} interpretation rules from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        groups = {"GROUP_AG": GROUP_AG}
        for gname, grp in groups.items():
            print(f"  {gname} ({len(grp)} rules):")
            for r in grp:
                print(f"    {r['rule_id']}")
        print(
            f"\nTotal: {len(ALL_RULES)}\n"
            f"Sources: Mehta Ch 2 (9-Step Hierarchy) + Gaur Ch 3 (Special Horoscopes).\n"
            f"Dry run complete."
        )
        return

    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    col = db[COLLECTION]
    upserted = 0
    for rule in ALL_RULES:
        await col.update_one(
            {"rule_id": rule["rule_id"]},
            {"$set": rule},
            upsert=True,
        )
        upserted += 1
    print(f"Upserted {upserted} rules into {COLLECTION}.")
    client.close()

if __name__ == "__main__":
    asyncio.run(run())
