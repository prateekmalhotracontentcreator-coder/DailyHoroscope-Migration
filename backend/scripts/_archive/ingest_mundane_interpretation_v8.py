"""
Mundane Astrology — Interpretation Rules v8
Batch: mundane-interp-v8-20260506

Source: Raphael, "Mundane Astrology" (WITS e-group edition)
  Chapter 6  — The Mundane Maps (eclipse/ingress duration rules)
  Chapter 8  — First House planets
  Chapter 9  — Second House planets (finance / stock markets)
  Chapter 11 — Fourth House planets (earthquakes, weather, agriculture)
  Chapter 13 — Sixth House planets (public health, army/navy)
  Chapter 14 — Seventh House planets (war, foreign affairs)
  Chapter 15 — Eighth House planets (mortality, death-rate)

GROUP_AC: 11 rules from Raphael pages 1-20

Rule types: transit, ingress, lunation, eclipse
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
_BATCH     = "mundane-interp-v8-20260506"
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
# GROUP_AC — RAPHAEL CORE RULES (Ch 6 + Ch 8-15)
# ============================================================

GROUP_AC = [

    # ── Rule AC-01: Solar eclipse duration = hours as years
    _rule(
        rule_id         = "mundane-raphael-ch6-solar-eclipse-duration-hours-years",
        sub_type        = "eclipse",
        title           = "Solar Eclipse Duration Rule — Hours of Eclipse = Years of Influence",
        source_chapter  = "Raphael Ch 6, p.8",
        condition       = (
            "A Solar eclipse (figure cast for the exact moment of New Moon) occurs. "
            "Measure the duration of the eclipse in hours."
        ),
        result          = (
            "The Solar eclipse has a specific influence of its own lasting for AS MANY YEARS "
            "as the eclipse is HOURS IN LENGTH. "
            "Example: a 3-hour solar eclipse → 3 years of influence in affected countries. "
            "Effects are strongest: (1) where the eclipse is visible, "
            "(2) in countries and cities ruled by the zodiac sign in which the eclipse falls."
        ),
        synthesis_sources = ["Raphael Ch 6"],
        notes           = (
            "This is Raphael's unique duration formula for solar eclipses. "
            "A total solar eclipse can last up to ~7.5 minutes of totality but the entire "
            "umbral/partial event can last 2-4 hours. "
            "Partial solar eclipses typically last 2-3 hours = 2-3 years of mundane influence. "
            "Contrast: Lunar eclipses = months (not years). "
            "The figure should be cast for the exact New Moon moment, not the central maximum."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AC-02: Lunar eclipse duration = hours as months
    _rule(
        rule_id         = "mundane-raphael-ch6-lunar-eclipse-duration-hours-months",
        sub_type        = "eclipse",
        title           = "Lunar Eclipse Duration Rule — Hours of Eclipse = Months of Influence",
        source_chapter  = "Raphael Ch 6, p.8",
        condition       = (
            "A Lunar eclipse (figure cast for the exact moment of Full Moon) occurs. "
            "Measure the duration of the eclipse in hours."
        ),
        result          = (
            "The Lunar eclipse has a period of action extending over AS MANY MONTHS "
            "as the eclipse is HOURS IN DURATION. "
            "Example: a 2-hour lunar eclipse → 2 months of influence. "
            "Lunar eclipses are important but less powerful than Solar eclipses "
            "(years vs months). "
            "Effects chiefly where visible and in countries ruled by the sign of the eclipse."
        ),
        synthesis_sources = ["Raphael Ch 6"],
        notes           = (
            "Pair with solar eclipse rule (AC-01). "
            "A total lunar eclipse can last ~1.5-3 hours in totality but partial phases "
            "can extend the duration to 3-4 hours. "
            "The figure is cast for the exact Full Moon moment."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── Rule AC-03: Ingress rising sign determines duration of influence
    _rule(
        rule_id         = "mundane-raphael-ch6-ingress-rising-sign-duration",
        sub_type        = "ingress",
        title           = "Ingress Rising Sign Determines Duration — Cardinal 3mo / Fixed 12mo / Mutable 6mo",
        source_chapter  = "Raphael Ch 6, p.7",
        condition       = (
            "A Solar Ingress chart is cast for the moment the Sun enters Aries, Cancer, Libra, or Capricorn. "
            "Note the rising sign (Ascendant sign) of the ingress chart for the location in question."
        ),
        result          = (
            "CARDINAL sign rising (Aries, Cancer, Libra, Capricorn): "
            "ingress figure has rule for THREE MONTHS only — cast the next ingress immediately. "
            "FIXED sign rising (Taurus, Leo, Scorpio, Aquarius): "
            "ingress figure influences the WHOLE of the twelve months following. "
            "MUTABLE/COMMON sign rising (Gemini, Virgo, Sagittarius, Pisces): "
            "ingress figure has influence for the ensuing SIX MONTHS."
        ),
        synthesis_sources = ["Raphael Ch 6"],
        notes           = (
            "This rule determines how many ingress charts need to be cast and consulted "
            "for a given year and location. "
            "A fixed sign rising at the Aries ingress means only ONE chart rules the entire year. "
            "A cardinal sign rising means each quarterly ingress must be separately cast. "
            "The Aries ingress (Spring Equinox, ~March 20-21) is the primary annual chart. "
            "Other ingresses (Cancer, Libra, Capricorn) supplement when cardinal sign rises at Aries."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AC-04: Lunation on fixed 4th cusp = disastrous earthquake
    _rule(
        rule_id         = "mundane-raphael-ch11-lunation-4th-cusp-fixed-earthquake",
        sub_type        = "lunation",
        title           = "Lunation in Fixed Sign on 4th House Cusp = Disastrous Earthquake",
        source_chapter  = "Raphael Ch 11, Part 2 p.2",
        condition       = (
            "A New Moon or Full Moon (Lunation) falls: "
            "(1) IN a fixed sign (Taurus, Leo, Scorpio, Aquarius), AND "
            "(2) EXACTLY ON the cusp of the fourth house of the mundane map."
        ),
        result          = (
            "This is a sign of a DISASTROUS EARTHQUAKE in whatever part of the world "
            "this position may occur. "
            "The location is determined by which geographic area has this lunation "
            "falling exactly on their 4th house cusp."
        ),
        synthesis_sources = ["Raphael Ch 11", "Gopalakrishnan Ch 7 (Saturn fixed signs)"],
        notes           = (
            "Cross-validates with Gopalakrishnan's earthquake rules: "
            "both authors emphasize fixed signs as earthquake triggers (see gopal-ch7-saturn-fixed-signs-primary). "
            "Raphael's rule specifically combines fixed sign + 4th house cusp + lunation timing. "
            "The 4th house cusp (IC) governs land, earth, and geological matters in mundane charts. "
            "This is one of Raphael's most specific earthquake indicators."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AC-05: Mars in 7th house = war + direction of enemy
    _rule(
        rule_id         = "mundane-raphael-ch14-mars-7th-war-direction",
        sub_type        = "ingress",
        title           = "Mars in 7th House = War Danger + Cardinal Direction of Enemy",
        source_chapter  = "Raphael Ch 14, Part 2 pp.5-6",
        condition       = (
            "At the time of a Solar Ingress, Lunation, or Eclipse: "
            "Mars is placed in the seventh house of the mundane map."
        ),
        result          = (
            "Grave danger of international disputes, disagreement with other Powers, "
            "unsatisfactory condition of foreign relations, and DANGER OF WAR. "
            "DIRECTION OF ENEMY: the cardinal direction from which the enemy will come "
            "is shown by the sign Mars occupies — "
            "Mars in Aries = enemy from EAST; "
            "Mars in Cancer = enemy from NORTH; "
            "Mars in Libra = enemy from WEST; "
            "Mars in Capricorn = enemy from SOUTH. "
            "Signs between the four cardinals point to intermediate compass directions. "
            "The sign in which Mars is placed also shows WHICH COUNTRY is opposed to the nation "
            "(according to the country or region ruled by that sign)."
        ),
        synthesis_sources = ["Raphael Ch 14", "Raphael Ch 28 (countries ruled by signs)"],
        notes           = (
            "Mars is the most powerful malefic in the 7th house. "
            "Next most malefic in foreign affairs: Saturn in 7th. "
            "This rule applies to ingress, lunation, and eclipse charts for any nation. "
            "The direction indicator (Aries=East etc.) applies specifically to cardinal signs of Mars. "
            "Cross-reference with Gopalakrishnan's war rules (ch8) for Vedic frame confirmation."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AC-06: Malefic in 1st house = national troubles, health crises
    _rule(
        rule_id         = "mundane-raphael-ch8-malefic-1st-national-troubles",
        sub_type        = "ingress",
        title           = "Malefic in 1st House of Mundane Map = National Troubles and Public Ill-Health",
        source_chapter  = "Raphael Ch 8, p.11",
        condition       = (
            "At a Solar Ingress, Lunation, or Eclipse: "
            "a malefic planet (Mars, Saturn, Uranus, Neptune) is placed in the first house "
            "of the mundane map, especially if afflicted by other planets."
        ),
        result          = (
            "Much trouble is shown in the country; things will be unsettled; health of the people bad. "
            "MARS in 1st: discontent, strikes, riots, fires, crime and ill-health. "
            "SATURN in 1st: distress, discontent, want of work, loss of trade, poverty, general ill-health. "
            "URANUS in 1st: strikes, rioting, violence, anarchy, turbulence, outrages against authority. "
            "NEPTUNE in 1st: agitation, secret propaganda, socialism, vice, crime, suicides, "
            "fraud and swindling. "
            "If the malefic is itself afflicted by other planets, the evil is more marked."
        ),
        synthesis_sources = ["Raphael Ch 8"],
        notes           = (
            "The 1st house in mundane astrology represents the general population and national health. "
            "If no planet is in 1st, judge by the ruler of the rising sign and its aspects. "
            "Well-aspected malefics are somewhat mitigated. "
            "A benefic (Jupiter, Venus, well-aspected Sun/Moon) in 1st = good general condition."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AC-07: Saturn in 2nd house = financial stagnation, securities depression
    _rule(
        rule_id         = "mundane-raphael-ch9-saturn-2nd-financial-stagnation",
        sub_type        = "transit",
        title           = "Saturn in 2nd House = Financial Stagnation, Securities Depression, Revenue Decrease",
        source_chapter  = "Raphael Ch 9, p.13",
        condition       = (
            "At a Solar Ingress, Lunation, or in transit: "
            "Saturn is placed in the second house of the national mundane map."
        ),
        result          = (
            "Very evil for national finances: poor revenue, decrease of receipts, "
            "financial stagnation, depression in securities and financial circles, "
            "general want of activity in all money matters. "
            "If Saturn is afflicted: heavy depreciation of securities (market crash). "
            "If Saturn is well aspected: gives a steadying tone to the money market "
            "(stabilising effect, but still does not produce prosperity)."
        ),
        synthesis_sources = ["Raphael Ch 9"],
        notes           = (
            "Saturn in 2nd is the most consistently negative planetary position for national finance. "
            "Compare: Mars in 2nd = sudden panics/crashes; Saturn in 2nd = prolonged stagnation. "
            "Jupiter in 2nd well aspected is the best position for national financial prosperity. "
            "One of the worst aspects in financial affairs: Jupiter square or opposition Mars (in 2nd)."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AC-08: Mars in 2nd house = stock exchange panic, bank failures
    _rule(
        rule_id         = "mundane-raphael-ch9-mars-2nd-stock-panic",
        sub_type        = "transit",
        title           = "Mars in 2nd House = Stock Exchange Panic, Bank Failures, Military Expenditure",
        source_chapter  = "Raphael Ch 9, p.13",
        condition       = (
            "At a Solar Ingress, Lunation, or in transit: "
            "Mars is placed in the second house of the national mundane map."
        ),
        result          = (
            "Losses on the Stock Exchange, panics, bank failures. "
            "Enormous expenditure and waste of public money. "
            "Military affairs will require large amounts of money — "
            "the revenue will be seriously affected by military/defence spending. "
            "Note: does not necessarily denote a diminution of national revenue per se, "
            "but rather enormous expenditure that strains it."
        ),
        synthesis_sources = ["Raphael Ch 9"],
        notes           = (
            "Mars in 2nd is particularly negative for stock markets and banking. "
            "Different from Saturn in 2nd (stagnation/depression) — "
            "Mars in 2nd indicates sudden violent financial events: panics, crashes, failures. "
            "The military expenditure note links to Mars's signification as ruler of soldiers/war."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AC-09: Saturn in 6th house = public health crisis
    _rule(
        rule_id         = "mundane-raphael-ch13-saturn-6th-public-illness",
        sub_type        = "ingress",
        title           = "Saturn in 6th House = Widespread Public Ill-Health of Nature Shown by Sign",
        source_chapter  = "Raphael Ch 13, Part 2 pp.4-5",
        condition       = (
            "At a Solar Ingress, Lunation, or in transit: "
            "Saturn is placed in the sixth house of the national mundane map."
        ),
        result          = (
            "Very evil position: much ill-health among the populace. "
            "The NATURE of the sickness is shown by the SIGN Saturn occupies — "
            "e.g., Saturn in a water sign: lung/fluid conditions; "
            "Saturn in an earth sign: chronic/wasting diseases; "
            "Saturn in a fire sign: fevers with exhaustion. "
            "Also: discontent and dissatisfaction among the lower classes and in the Navy. "
            "If afflicted: evils are more prominent and severe."
        ),
        synthesis_sources = ["Raphael Ch 13", "Gopalakrishnan Ch 6 (epidemic indicators)"],
        notes           = (
            "Cross-validates Gopalakrishnan's epidemic triad (see gopal-ch6-epidemic-triad): "
            "both sources emphasize Saturn in 6th-related positions as epidemic indicators. "
            "Raphael adds the refinement that the SIGN of Saturn indicates the TYPE of illness. "
            "See also: gopal-ch6-mass-death-national-chart for Saturn+Rahu combinations."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AC-10: Mars in 6th house = feverish disease + warship accidents
    _rule(
        rule_id         = "mundane-raphael-ch13-mars-6th-feverish-disease-warships",
        sub_type        = "ingress",
        title           = "Mars in 6th House = Feverish Inflammatory Disease + Naval Fires and Accidents",
        source_chapter  = "Raphael Ch 13, Part 2 p.5",
        condition       = (
            "At a Solar Ingress, Lunation, or in transit: "
            "Mars is placed in the sixth house of the national mundane map."
        ),
        result          = (
            "Very evil position: feverish and inflammatory disease among the people, "
            "according to the nature of the sign in which Mars is placed. "
            "Also denotes fires and accidents on warships, and insubordination among sailors. "
            "If well aspected: effects are mitigated; "
            "may denote some naval demonstration or naval review rather than actual accidents."
        ),
        synthesis_sources = ["Raphael Ch 13"],
        notes           = (
            "Mars in 6th indicates inflammatory/fever-type disease (vs Saturn in 6th = chronic wasting). "
            "The dual effect (disease + naval accidents) follows from Mars's significations "
            "(soldiers, naval men, fire, incendiarism). "
            "The sign of Mars refines the type: fire sign = literal fires; water sign = naval events "
            "and blood/fluid-related inflammation."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AC-11: Saturn in 4th house = earthquakes, mining disasters, bad crops
    _rule(
        rule_id         = "mundane-raphael-ch11-saturn-4th-earthquakes-bad-weather",
        sub_type        = "ingress",
        title           = "Saturn in 4th House = Earthquakes, Mining Disasters, Bad Weather, Crop Failure",
        source_chapter  = "Raphael Ch 11, Part 2 p.2",
        condition       = (
            "At a Solar Ingress, Lunation, or in transit: "
            "Saturn is placed in the fourth house of the national mundane map."
        ),
        result          = (
            "Obstacles and difficulties to the Government; national affairs will not proceed smoothly. "
            "Causes bad weather for crops; adversely affects agricultural matters. "
            "Denotes mining disasters, EARTHQUAKES, depreciates the value of land, disturbs property. "
            "If afflicted: evil very considerably increased. "
            "Government faces loss of prestige and electoral difficulties."
        ),
        synthesis_sources = [
            "Raphael Ch 11",
            "Gopalakrishnan Ch 7 (Saturn fixed signs earthquake primary rule)",
        ],
        notes           = (
            "Cross-validates Gopalakrishnan's earthquake rule: "
            "gopal-ch7-saturn-fixed-signs-primary specifies Saturn in FIXED signs as primary earthquake signal; "
            "Raphael's rule adds the 4th house placement as a key mundane chart indicator. "
            "Combined rule: Saturn in fixed sign AND in 4th house = highest earthquake risk. "
            "The 4th house cusp (IC) is specifically taken into account for earthquake prognostications."
        ),
        severity        = "high",
        checkable       = True,
    ),

]

ALL_RULES = GROUP_AC

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_RULES)} interpretation rules from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        groups = {"GROUP_AC": GROUP_AC}
        for gname, grp in groups.items():
            print(f"  {gname} ({len(grp)} rules):")
            for r in grp:
                print(f"    {r['rule_id']}")
        print(f"\nTotal: {len(ALL_RULES)}\n\nDry run complete.")
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
