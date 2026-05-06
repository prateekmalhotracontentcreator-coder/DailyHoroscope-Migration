"""
Mundane Astrology — Interpretation Rules v15
Batch: mundane-interp-v15-20260506

Sources:
  Gaur Ch 10  — Mars/Mercury/Jupiter/Venus/Rahu transit diagnostic rules
  Gaur Ch 10  — Synthesis methodology rules
  Mehta Ch 7  — Koorma reconciliation rules (Regime Collapse kill-switch,
                tribal insurgency, triple-directional audit, Saturn-West amplifier)

GROUP_AJ: 14 rules

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
_BATCH     = "mundane-interp-v15-20260506"
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
# GROUP_AJ — Transit diagnostic rules + Koorma reconciliation rules
# ============================================================

GROUP_AJ = [

    # ── AJ-01: Mars retrograde = gold/silver/wheat/red items stay expensive
    _rule(
        rule_id         = "gaur-ch10-mars-retrograde-gold-silver-expensive",
        sub_type        = "transit",
        title           = "Retrograde Mars = Gold, Silver, Wheat, and Red Items Remain Expensive",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = "Mars is in retrograde motion in any sign.",
        result          = (
            "Gold, silver, wheat, red things, and goods influenced by Mars's own signs remain expensive. "
            "This holds regardless of the sign Mars occupies."
        ),
        synthesis_sources = ["Gaur Ch 10 (Mars motion state logic)"],
        severity        = "medium",
        checkable       = True,
    ),

    # ── AJ-02: Mars in Gemini = sudden extreme price spike or crash
    _rule(
        rule_id         = "gaur-ch10-mars-gemini-sudden-price-volatility",
        sub_type        = "transit",
        title           = "Mars Transiting Gemini = Sudden Extreme Price Spike or Crash (Market Shock)",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = "Transit Mars enters Gemini (Mithuna rashi).",
        result          = (
            "Materials become very costly or cheap suddenly — market shock event. "
            "When Mars goes Direct in Gemini, this extreme volatility triggers immediately. "
            "When Mars enters Gemini Retrograde, goods become expensive or cheap gradually."
        ),
        synthesis_sources = ["Gaur Ch 10 (Mars in Gemini sign result)"],
        notes           = (
            "Gemini is the sign of USA and communications/trade. "
            "Mars in Gemini produces the most volatile price environment of all sign transits. "
            "Monitor for compounding effect: if Rahu or Saturn also aspect Gemini, extreme scenario confirmed."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── AJ-03: Mars armed forces mutiny alert
    _rule(
        rule_id         = "gaur-ch10-mars-12th-lord-afflicted-military-insubordination",
        sub_type        = "natal_transit",
        title           = "Mars = 12th House Lord and Afflicted in Transit = Risk of Military Insubordination / Coup",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = (
            "In the national horoscope, Mars is the lord of the 12th house (house of foreign attack, secret enemies). "
            "Mars is simultaneously afflicted in transit by Saturn, Rahu, or Ketu."
        ),
        result          = (
            "'Risk of Military Insubordination or Coup' alert. "
            "Internal forces act against the established authority."
        ),
        synthesis_sources = [
            "Gaur Ch 10 (Mars Armed Forces Mutiny Alert)",
            "Gaur Ch 4 (House 12 = Intelligence Department, Foreign Attack)",
        ],
        severity        = "high",
        checkable       = True,
    ),

    # ── AJ-04: Mercury weather pivot
    _rule(
        rule_id         = "gaur-ch10-mercury-sign-ingress-weather-disturbance",
        sub_type        = "transit",
        title           = "Mercury Crossing Any Sign Boundary = Weather Disturbance Alert",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = "Mercury transits from one zodiac sign to another (any sign ingress).",
        result          = (
            "'Weather Disturbance Alert' — noticeable atmospheric changes occur. "
            "This includes sudden temperature shifts, unexpected rain or dry spells, or wind changes."
        ),
        synthesis_sources = ["Gaur Ch 10 (Mercury weather pivot rule)"],
        severity        = "low",
        checkable       = True,
    ),

    # ── AJ-05: Mercury retrograde in Gemini = vegetables cheap + education scandal
    _rule(
        rule_id         = "gaur-ch10-mercury-retrograde-gemini-education-scandal",
        sub_type        = "transit",
        title           = "Mercury Retrograde Entering Gemini = Vegetables Cheap + Education Scandal Risk",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = "Mercury enters Gemini in Retrograde motion.",
        result          = (
            "Vegetables become cheap. "
            "Cross-reference with House 5 (Education Ministry) — "
            "'Potential scams and scandals in educational institutions' alert triggered."
        ),
        synthesis_sources = [
            "Gaur Ch 10 (Mercury retrograde in Gemini)",
            "Gaur Ch 4 (House 5 = Education Dept)",
        ],
        notes           = (
            "Mercury retrograde in its own sign amplifies the House 5 effect. "
            "Mercury rules Gemini and Virgo — retrograde here disrupts Mercurial functions: "
            "trade, communications, education, media."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── AJ-06: Mercury combusted in Leo = stock market decline
    _rule(
        rule_id         = "gaur-ch10-mercury-combust-leo-stock-market-crash",
        sub_type        = "transit",
        title           = "Mercury Combusted and Afflicted in Leo = Stock Market Decline and Textile Bearishness",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = "Mercury is combusted (within 15° of the Sun) AND afflicted while transiting Leo.",
        result          = (
            "'Sudden decline in Stock Market values and Textile/Jute sector bearishness' alert. "
            "Leo is the sign of rulers and the stock exchange. Combustion kills Mercury's trading function."
        ),
        synthesis_sources = [
            "Gaur Ch 10 (Mercury combustion + Leo sign result)",
            "Gaur Ch 4 (House 2 = Share Market)",
        ],
        severity        = "medium",
        checkable       = True,
    ),

    # ── AJ-07: Jupiter in Capricorn afflicted = banking crisis
    _rule(
        rule_id         = "gaur-ch10-jupiter-capricorn-afflicted-banking-crisis",
        sub_type        = "transit",
        title           = "Jupiter Afflicted in Capricorn = Banking Scandal and Interest Rate Hikes",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = "Jupiter transits Capricorn AND is afflicted by Saturn, Rahu, or Mars.",
        result          = (
            "'Critical Alert: Instability in national treasury, banking scandals, "
            "and high-interest rate hikes.' "
            "Capricorn is Jupiter's sign of debilitation — affliction here damages financial systems directly."
        ),
        synthesis_sources = [
            "Gaur Ch 10 (Jupiter Capricorn banking trigger)",
            "Gaur Ch 4 (House 2 = Banking, National Treasure)",
        ],
        severity        = "high",
        checkable       = True,
    ),

    # ── AJ-08: Jupiter exaltation + Sun aspect = establishment of supremacy
    _rule(
        rule_id         = "gaur-ch10-jupiter-cancer-sun-aspect-supremacy",
        sub_type        = "transit",
        title           = "Jupiter in Cancer (Exaltation) Aspected by Sun = Establishment of Global Supremacy",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = (
            "Jupiter transits Cancer (its exaltation sign) "
            "AND the Sun aspects Jupiter by conjunction or trine."
        ),
        result          = (
            "'Establishment of Global Supremacy and victory in international treaties' for the relevant nation. "
            "Treaties are signed; international cooperation peaks; the nation's position on the world stage is elevated."
        ),
        synthesis_sources = [
            "Gaur Ch 10 (Jupiter sovereignty marker)",
            "Mehta Ch 10 (Jupiter protection rule — victory for allied force)",
        ],
        severity        = "low",
        checkable       = True,
    ),

    # ── AJ-09: Venus direct station = gold/gems luxury spike + cotton bearish
    _rule(
        rule_id         = "gaur-ch10-venus-direct-station-luxury-spike",
        sub_type        = "transit",
        title           = "Venus Turning Direct = Price Spike in Gold, Gems, and Fine Silks; Cotton Bearish",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = "Venus changes motion from Retrograde to Direct (Venus Stationary-Direct).",
        result          = (
            "'Luxury Market Inflation Alert': Gold, gems, silks, ghee, silver, and gur become expensive. "
            "Cotton sector enters bearish trend (cotton cheap)."
        ),
        synthesis_sources = ["Gaur Ch 10 (Venus change to direct motion)"],
        severity        = "medium",
        checkable       = True,
    ),

    # ── AJ-10: Rahu in Libra = drought veto
    _rule(
        rule_id         = "gaur-ch10-rahu-libra-drought-veto",
        sub_type        = "transit",
        title           = "Rahu in Libra = Drought Veto — Agricultural Failure Even If Other Planets Promise Rain",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = "Rahu transits Libra (Tula rashi). Duration: ~18 months.",
        result          = (
            "'Drought Veto' activated — agricultural failure and grain price inflation are predicted "
            "even if other planetary configurations suggest rainfall. "
            "Grains become expensive throughout this transit."
        ),
        synthesis_sources = ["Gaur Ch 10 (Rahu Libra drought veto)"],
        notes           = (
            "Libra rules Austria, Tibet, Kashmir, and parts of USA/Japan. "
            "This is a 1.5-year 'Vulnerability Window' for water scarcity in these regions. "
            "Cross-validate with Koorma Chakra for Anarta (Gujarat/Saurashtra) — Libra's Indian correlation."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AJ-11: Regime collapse kill-switch
    _rule(
        rule_id         = "mehta-ch7-koorma-regime-collapse-kill-switch",
        sub_type        = "spatial_transit",
        title           = "Malefic Afflicting Koorma Star Cluster = Regime Collapse Risk for Corresponding Territory",
        source_chapter  = "Mehta/Rao Ch 7",
        condition       = (
            "A malefic planet (Saturn, Mars, Rahu, Ketu) occupies, aspects, or creates Vedha on "
            "any of the 9 Koorma directional star clusters. "
            "Use the Regime Collapse Kill-Switch table "
            "(spec: mehta-ch7-koorma-chakra-reconciled) to identify the at-risk territory."
        ),
        result          = (
            "'Regime Stability Crisis' alert for the mapped territory. "
            "The ruler or ruling party of that region faces high risk of collapse, removal, or defeat. "
            "Example: Malefic in Ardra/Punarvasu/Pushya cluster → 'Regime Crisis in Magadha (Bihar)'."
        ),
        synthesis_sources = [
            "Mehta Ch 7 (Destruction of Kings kill-switch)",
            "Varahamihira's Brihat Samhita (original source)",
        ],
        notes           = (
            "This is a BINARY logic gate — the kill-switch fires regardless of standard yearly benefic trends. "
            "Retrograde malefic in the cluster = maximum severity. "
            "Cross-validate with national 10th house (Ruling Party) for confirmation."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AJ-12: Triple directional audit = critical confidence
    _rule(
        rule_id         = "mehta-ch7-koorma-triple-directional-audit",
        sub_type        = "spatial_transit",
        title           = "Triple Directional Audit (Koorma + Planet + 7th House) All Agree = Critical Conflict Confidence",
        source_chapter  = "Mehta/Rao Ch 7",
        condition       = (
            "For a war or major conflict prediction, audit three directional signals: "
            "(1) Koorma Chakra: which direction is the afflicted nakshatra cluster mapped to? "
            "(2) Planet's Direction: which compass point does the afflicting planet rule "
            "(Sun=East, Moon=NW, Mars=South, Mercury=North, Jupiter=NE, Venus=SE, Saturn=West, Rahu/Ketu=South/West)? "
            "(3) 7th House Direction: Mars in Aries=East, Cancer=North, Libra=West, Capricorn=South."
        ),
        result          = (
            "IF all three directional signals agree on the same direction: "
            "prediction confidence for conflict in that direction = CRITICAL. "
            "Example: Saturn (West) in Jyeshtha (West sector) with 7th house Mars in Libra (West) "
            "= Critical conflict alert for Baluchistan/West Punjab corridor."
        ),
        synthesis_sources = [
            "Mehta Ch 7 (Triple Directional Audit rule)",
            "Gaur Ch 4 (Koorma grid + planetary directions)",
        ],
        notes           = (
            "This is the validation gate that transforms a single-signal alert into a confirmed prediction. "
            "Two signals agreeing = high confidence. All three agreeing = critical/confirmed."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AJ-13: Saturn-West sector triple alignment = industrial triple weight
    _rule(
        rule_id         = "mehta-ch7-koorma-saturn-west-triple-amplifier",
        sub_type        = "spatial_transit",
        title           = "Saturn in Western Sign + Western Koorma Sector = Malefic Impact on Industry TRIPLED",
        source_chapter  = "Mehta/Rao Ch 7",
        condition       = (
            "Saturn is transiting a Western zodiac sign (Libra or Capricorn) "
            "AND is occupying the Western Koorma sector constellations "
            "(Jyeshtha, Moola, Poorvashadh — the Tail / West sector)."
        ),
        result          = (
            "The malefic impact on heavy industry and labor is TRIPLED. "
            "Severe industrial stagnation, labor strikes, and commodity shortages for the West direction. "
            "For India: impact concentrated on Western Maharashtra, Baluchistan, West Punjab."
        ),
        synthesis_sources = [
            "Mehta Ch 7 (Planetary Alignment Audit — Saturn West amplifier)",
            "Gaur Ch 10 (Saturn sign transit results)",
        ],
        severity        = "high",
        checkable       = True,
    ),

    # ── AJ-14: North West cluster affliction = Afghanistan/Oxus corridor insurgency
    _rule(
        rule_id         = "mehta-ch7-koorma-northwest-affliction-tribal-insurgency",
        sub_type        = "spatial_transit",
        title           = "Malefic in NW Koorma Cluster = Tribal Unrest and Instability in Afghanistan / Oxus Corridor",
        source_chapter  = "Mehta/Rao Ch 7",
        condition       = (
            "A malefic planet transits or creates Vedha on the North-West Koorma constellations: "
            "Uttarashadh, Sravana, or Dhanishtha."
        ),
        result          = (
            "'Tribal unrest and instability in the Oxus Valley / Afghanistan corridor' alert. "
            "Specific regions: North Pakistan, Afghanistan, Northern Kashmir, Jodhpur. "
            "Ancient correlation: Madra (Sialkot/West Punjab) regime collapse risk."
        ),
        synthesis_sources = [
            "Mehta Ch 7 (North-West sector ethnic insurgency marker)",
            "Gaur Ch 4 (Koorma NW foot)",
        ],
        notes           = (
            "Dhanishtha is particularly sensitive as it sits on the NW-North boundary. "
            "Saturn retrograde in Dhanishtha = maximum unrest signal for this corridor. "
            "Cross-validate with Capricorn sign afflictions "
            "(Capricorn = India/Afghanistan in the zodiac-geography map)."
        ),
        severity        = "high",
        checkable       = True,
    ),

]

ALL_RULES = GROUP_AJ

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_RULES)} interpretation rules from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        groups = {"GROUP_AJ": GROUP_AJ}
        for gname, grp in groups.items():
            print(f"  {gname} ({len(grp)} rules):")
            for r in grp:
                print(f"    {r['rule_id']}")
        print(f"\nTotal: {len(ALL_RULES)}\nDry run complete.")
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
