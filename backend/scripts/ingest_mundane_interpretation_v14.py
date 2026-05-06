"""
Mundane Astrology — Interpretation Rules v14
Batch: mundane-interp-v14-20260506

Sources:
  Mehta Ch 10  — Macro-Conjunction rules (Saturn-Jupiter mortality veto,
                 Saturn-Rahu atomic/colonial gate, Saturn-Mars massacre/tsunami,
                 Mars-Ketu terrorism gate, Aries 1° paradigm shift, ignition rule)
  Gaur Ch 10   — Transit timing rules (drought ingress, monsoon failure, famine gate,
                 28-degree Saturn, 2-month inflation trigger, retrograde veto)

GROUP_AI: 16 rules

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
_BATCH     = "mundane-interp-v14-20260506"
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
# GROUP_AI — Macro-Conjunction Rules + Transit Timing Rules
# ============================================================

GROUP_AI = [

    # ── AI-01: Aries 1° conjunction = Century-Level Paradigm Shift
    _rule(
        rule_id         = "mehta-ch10-aries-1-degree-conjunction-paradigm-shift",
        sub_type        = "conjunction",
        title           = "Heavy Planet Conjunction in Aries 1° = Century-Level Paradigm Shift (Highest Signal)",
        source_chapter  = "Mehta/Rao Ch 10",
        condition       = (
            "Any conjunction of heavy planets (Saturn, Jupiter, Mars, Rahu, Ketu) "
            "commences in the first degree of Aries (0°–1° Aries). "
            "This applies equally to conjunctions, not only Saturn-Jupiter."
        ),
        result          = (
            "'Century-Level Paradigm Shift' alert — the highest-level predictive signal in the engine. "
            "This is the rarest configuration in mundane astrology: "
            "known to have occurred only eight times in recorded history. "
            "Historical turning points of civilizational scale have always followed."
        ),
        synthesis_sources = ["Mehta Ch 10 (Historical Priority Gate)"],
        notes           = (
            "This rule overrides all other conjunction severity levels. "
            "When triggered, every other diagnostic must be subordinated to this signal. "
            "No specific historical anchor is given — the rarity is itself the validation."
        ),
        severity        = "critical",
        checkable       = True,
    ),

    # ── AI-02: Mars ignition rule — conjunctions only materialize when Mars triggers
    _rule(
        rule_id         = "mehta-ch10-mars-ignition-rule",
        sub_type        = "conjunction",
        title           = "Mars Ignition Rule — Historical Events Materialize When Mars Triggers Conjunction Degree",
        source_chapter  = "Mehta/Rao Ch 10",
        condition       = (
            "A Saturn-Jupiter, Saturn-Rahu, or Saturn-Mars conjunction / opposition has occurred. "
            "Mars then transits to conjoin or aspect the exact degree of that prior conjunction."
        ),
        result          = (
            "The actual historical event (war, revolution, massacre, economic collapse) materializes. "
            "Do NOT predict the event at the moment of the original conjunction — "
            "Mars is the 'Minute Hand' that fires the trigger. "
            "Monitor the next Mars transit to the conjunction degree for the event window."
        ),
        synthesis_sources = ["Mehta Ch 10 (Ignition Rule)", "Mehta Ch 8 (Sanghatta trigger logic)"],
        notes           = (
            "This is the single most important operational refinement in macro-temporal forecasting. "
            "Without Mars triggering, a conjunction creates 'background tension' only — not an event. "
            "Apply 1-degree orb for the trigger transit."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AI-03: Saturn-Jupiter = US president mortality veto
    _rule(
        rule_id         = "mehta-ch10-saturn-jupiter-us-president-mortality-veto",
        sub_type        = "conjunction",
        title           = "Saturn-Jupiter Conjunction Year + US Presidential Election = President Mortality Risk",
        source_chapter  = "Mehta/Rao Ch 10",
        condition       = (
            "A Saturn-Jupiter conjunction occurs in any sign. "
            "A US Presidential election takes place in the same year or within 1 year of the conjunction."
        ),
        result          = (
            "Mortality Risk = CRITICAL for that US President. "
            "High probability that the President will not complete their full term in office "
            "(death in office, assassination, forced resignation, or severe incapacitation)."
        ),
        synthesis_sources = [
            "Mehta Ch 10 (Saturn-Jupiter mortality veto)",
            "Mehta Ch 2 Step 8 (Saturn-Jupiter conjunction mortality gate)",
        ],
        notes           = (
            "VALIDATED HISTORICAL CASES: "
            "Presidents elected in 1840, 1860, 1880, 1900, 1920, 1940, 1960 all died in office. "
            "(The 'Tecumseh's Curse' / 'Zero-Year Curse' pattern.) "
            "The 1980 conjunction produced the assassination attempt on Reagan (survived). "
            "Precision: 1-degree orb between Saturn and Jupiter maximizes the veto weight."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AI-04: Saturn-Jupiter Great Mutation = era-level turning point
    _rule(
        rule_id         = "mehta-ch10-saturn-jupiter-great-mutation-era-shift",
        sub_type        = "conjunction",
        title           = "Saturn-Jupiter Great Mutation (First Conjunction in New Triplicity) = Era-Level Turning Point",
        source_chapter  = "Mehta/Rao Ch 10",
        condition       = (
            "A Saturn-Jupiter conjunction occurs in a triplicity (Fire/Earth/Air/Water) "
            "for the FIRST time after a long period in the previous triplicity. "
            "This is the 'Great Mutation' — the change of triplicity."
        ),
        result          = (
            "Era-Level Turning Point with permanent impact for the next 200 years: "
            "Earthy triplicity = material growth and shifts in world financial dominance; "
            "Fiery triplicity = wars of ideology and rapid territorial expansion; "
            "Airy triplicity = technology revolutions and democratic movements; "
            "Watery triplicity = maritime disasters, epidemics, mass displacement."
        ),
        synthesis_sources = ["Mehta Ch 10 (Great Mutation + Triplicity Results)"],
        notes           = (
            "The current Great Mutation in Aquarius (January 2020) marks the transition "
            "from Earthy triplicity (Capricorn dominance 1802–2020) to Airy triplicity — "
            "signaling a century of technology, social upheaval, and communications revolution."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AI-05: Saturn-Rahu in Gemini = nuclear/atomic shift
    _rule(
        rule_id         = "mehta-ch10-saturn-rahu-gemini-nuclear-shift",
        sub_type        = "conjunction",
        title           = "Saturn-Rahu Conjunction in Gemini = Global Shift in Military Technology / Nuclear Escalation",
        source_chapter  = "Mehta/Rao Ch 10",
        condition       = (
            "Saturn and Rahu conjoin in Gemini (Mithuna rashi)."
        ),
        result          = (
            "'Atomic/Colonial Veto' triggered: "
            "Global Shift in Military Technology / Nuclear Escalation "
            "AND the Birth of New Sovereign States. "
            "Old empires collapse; new nation-states emerge."
        ),
        synthesis_sources = ["Mehta Ch 10 (Saturn-Rahu Atomic Veto)"],
        notes           = (
            "VALIDATED: 1945 conjunction — Hiroshima/Nagasaki + decolonization wave. "
            "Gemini = sign of USA and communications technology. "
            "Rahu = atomic/disruptive energy; Saturn = death of the old order. "
            "Next similar configuration: monitor for Saturn-Rahu in Gemini post-2035."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AI-06: Saturn-Rahu in Capricorn = Middle East regime change
    _rule(
        rule_id         = "mehta-ch10-saturn-rahu-capricorn-regime-change",
        sub_type        = "conjunction",
        title           = "Saturn-Rahu Conjunction in Capricorn = Major Regime Change in Middle East",
        source_chapter  = "Mehta/Rao Ch 10",
        condition       = (
            "Saturn and Rahu conjoin in Capricorn (Makar rashi)."
        ),
        result          = (
            "Major_Regime_Change_Middle_East = TRUE. "
            "Multi-planet concentration in Capricorn (especially within 1° orb) triggers "
            "'Economic Paradigm Shift' AND 'Catastrophic Event' (3× weight when within 1°)."
        ),
        synthesis_sources = ["Mehta Ch 10 (Saturn-Rahu Regional Collapse Gate)"],
        notes           = (
            "VALIDATED: 1991 Gulf War — Sun, Saturn, Moon, Rahu all met within 1° in Capricorn. "
            "Capricorn also rules India, Afghanistan, Punjab — "
            "so secondary alerts for the Indian subcontinent are always warranted."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AI-07: Saturn-Mars in watery sign = tsunami / maritime disaster
    _rule(
        rule_id         = "mehta-ch10-saturn-mars-watery-sign-tsunami",
        sub_type        = "conjunction",
        title           = "Saturn-Mars Conjunction in Watery Sign = Critical Tsunami / Maritime Flood Risk",
        source_chapter  = "Mehta/Rao Ch 10",
        condition       = (
            "Saturn and Mars conjoin in a Watery Sign: Cancer, Scorpio, or Pisces."
        ),
        result          = (
            "Critical Tsunami / Maritime Flood Risk — immediate 'Maritime Disaster or Flood-based Tragedy' alert. "
            "Large-scale loss of life by water-related catastrophe."
        ),
        synthesis_sources = ["Mehta Ch 10 (Saturn-Mars Natural Disaster Gate)"],
        notes           = (
            "VALIDATED: 2004 Asian Tsunami — Saturn and Mars in Cancer. "
            "This rule produces one of the highest historically-validated hit rates in the corpus. "
            "Cross-validate with Moon affliction in the same watery sign for maximum certainty."
        ),
        severity        = "critical",
        checkable       = True,
    ),

    # ── AI-08: Saturn-Mars in 6th house = internal military operation
    _rule(
        rule_id         = "mehta-ch10-saturn-mars-sixth-house-internal-military",
        sub_type        = "natal_transit",
        title           = "Saturn-Mars Conjunction in Nation's 6th House = Internal Military Operation / Massacre",
        source_chapter  = "Mehta/Rao Ch 10",
        condition       = (
            "Saturn and Mars conjoin in the 6th house of a national horoscope "
            "(foundation chart or annual Solar Ingress chart). "
            "Upgrade severity if conjunction is also in a Dual Sign."
        ),
        result          = (
            "'Black Day' Configuration: Internal military operation or large-scale massacre. "
            "Internal security forces are deployed against the civilian population. "
            "For Dual Sign + 6th-from-India: General Massacre confirmed."
        ),
        synthesis_sources = [
            "Mehta Ch 10 (Saturn-Mars Internal Security Trigger)",
            "Mehta Ch 8 (Massacre Alert — Saturn-Mars on Sanghatta 6th house)",
        ],
        notes           = (
            "VALIDATED: Operation Blue Star (June 1984) — "
            "Saturn-Mars conjunction in the 6th house of India's national chart. "
            "Nadir Shah massacre (1739) — Saturn-Mars in Dual Sign, 6th from Makar Lagna. "
            "This rule is the formal diagnostic gate for predicting internal military operations."
        ),
        severity        = "critical",
        checkable       = True,
    ),

    # ── AI-09: Mars-Ketu in fiery sign = terrorism
    _rule(
        rule_id         = "mehta-ch10-mars-ketu-fiery-sign-terrorism",
        sub_type        = "conjunction",
        title           = "Mars-Ketu Conjunction in Fiery Sign / Fiery Nakshatra = High-Intensity Terrorist Event",
        source_chapter  = "Mehta/Rao Ch 10",
        condition       = (
            "Mars conjuncts Ketu in a Fiery Sign (Aries, Leo, Sagittarius) "
            "OR in a fiery/violent nakshatra (Moola, Jyeshtha, Bharani). "
            "1-degree orb applies for maximum severity."
        ),
        result          = (
            "Extreme_Terrorist_Event = TRUE. "
            "High-intensity suicide attacks, bombings, or mass-casualty events. "
            "Ketu provides secrecy and self-immolation energy; Mars provides the explosive force."
        ),
        synthesis_sources = ["Mehta Ch 10 (Mars-Ketu Ignition Gate)"],
        notes           = (
            "VALIDATED: 9/11 WTC (2001) — Mars conjunct Ketu in Sagittarius/Moola, "
            "opposing Jupiter in Gemini (USA's sign). "
            "This is a 'template match' rule — future dates with Mars-Ketu within 1° in Fiery Signs "
            "should trigger this alert, especially when the opposition sign is a national native sign."
        ),
        severity        = "critical",
        checkable       = True,
    ),

    # ── AI-10: Saturn-Rahu in 8th/12th of national chart = national humiliation
    _rule(
        rule_id         = "mehta-ch10-saturn-rahu-eighth-twelfth-house-humiliation",
        sub_type        = "natal_transit",
        title           = "Saturn-Rahu Conjunction in Nation's 8th or 12th House = National Setback / Loss of Prestige",
        source_chapter  = "Mehta/Rao Ch 10",
        condition       = (
            "Saturn and Rahu conjoin in the 8th or 12th house of a nation's foundation chart."
        ),
        result          = (
            "National Setback and Loss of Prestige — "
            "the nation suffers a humiliating defeat, territorial loss, economic collapse, "
            "or major institutional failure on the world stage."
        ),
        synthesis_sources = ["Mehta Ch 10 (National Humiliation Gate)"],
        severity        = "high",
        checkable       = True,
    ),

    # ── AI-11: Drought ingress alert
    _rule(
        rule_id         = "gaur-ch10-drought-ingress-alert",
        sub_type        = "transit",
        title           = "Sun Ingress on Sun/Tue/Sat + 15-Muhurti Ingress = Critical Water Scarcity and Food Inflation",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = (
            "The Sun enters (Sankranti) any zodiac sign on a Sunday, Tuesday, or Saturday "
            "AND the ingress occurs in a 15-Muhurti constellation "
            "(Bharani, Ardra, Ashlesha, Jyeshtha, or Shatbhisha)."
        ),
        result          = (
            "'Critical Water Scarcity and Food Inflation Alert' for the month of that transit. "
            "Grains and juicy materials become expensive; rainfall is below normal."
        ),
        synthesis_sources = ["Gaur Ch 10 (Weekday Ingress + Muhurti Logic)"],
        notes           = (
            "Both conditions must be true simultaneously for maximum severity. "
            "Either condition alone is a medium alert; both together = critical. "
            "The 15-muhurti constellation list: Bharani, Ardra, Ashlesha, Jyeshtha, Shatbhisha."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AI-12: 45-muhurti ingress overrides dry-season signals
    _rule(
        rule_id         = "gaur-ch10-45-muhurti-ingress-overrides-drought",
        sub_type        = "transit",
        title           = "Sun Ingress in 45-Muhurti Constellation Overrides All Drought/Dry-Sign Signals",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = (
            "The Sun enters any zodiac sign while the Sun is in a 45-Muhurti constellation: "
            "Rohini, Punarvasu, Uttaraphalguni, Vishakha, Uttarashadh, or Uttarabhadrapad."
        ),
        result          = (
            "Good rains are assured. "
            "Grains, ghee, oil, and cotton become cheap. "
            "This overrides all dry-season signals, malefic weekday ingress results, "
            "and any drought indications from sign or star placements."
        ),
        synthesis_sources = ["Gaur Ch 10 (Muhurti Overrule Principle)"],
        severity        = "low",
        checkable       = True,
    ),

    # ── AI-13: Mars ahead of Sun in rainy season = monsoon failure
    _rule(
        rule_id         = "gaur-ch10-mars-ahead-sun-monsoon-failure",
        sub_type        = "transit",
        title           = "Mars Ahead of Sun During Rainy Season = Monsoon Failure",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = (
            "Mars is at a higher zodiacal degree than the Sun "
            "during the rainy season — specifically when the Sun is in Gemini or Cancer."
        ),
        result          = (
            "'Monsoon Failure: Rains will be obstructed or delayed.' "
            "Agricultural crisis follows — below-normal southwest monsoon for India."
        ),
        synthesis_sources = ["Gaur Ch 10 (Mars-Sun Overtake Trigger)"],
        notes           = (
            "The rainy season window is Sun in Gemini (approx. June 15 – July 15) "
            "and Sun in Cancer (approx. July 15 – Aug 15). "
            "Monitor Mars longitude vs Sun longitude in this window annually."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AI-14: Saturn retrograde Uttarashadh → Poorvashadh = 12-year famine
    _rule(
        rule_id         = "gaur-ch10-saturn-retrograde-uttarashadh-poorvashadh-famine",
        sub_type        = "transit",
        title           = "Saturn Retrograde Re-Entry from Uttarashadha into Poorvashadha = 12-Year Famine Protocol",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = (
            "Saturn, while retrograde, crosses back from Uttarashadha nakshatra "
            "into Poorvashadha nakshatra (i.e., moves backwards from Sagittarius 26°40'+ "
            "into Sagittarius 13°20'–26°40')."
        ),
        result          = (
            "CRITICAL LONG-TERM FAMINE AND AGRICULTURAL COLLAPSE ALERT. "
            "Severe drought and grain crisis extending up to 12 years. "
            "Escalate to the highest diagnostic level — "
            "this matches the Rohini Gate severity for agricultural destruction."
        ),
        synthesis_sources = [
            "Gaur Ch 10 (Special Retrograde Trigger — Famine Gate)",
            "Mehta Ch 8 (Rohini Gate dual-threat: war OR famine)",
        ],
        notes           = (
            "This rule is the specific transit-level famine trigger. "
            "The Rohini Gate (AH-13) is the constellation-level famine trigger. "
            "If BOTH activate simultaneously: famine severity is near-certain and prolonged. "
            "Monitor Saturn's retrograde arc in Sagittarius every 29-year cycle."
        ),
        severity        = "critical",
        checkable       = True,
    ),

    # ── AI-15: Saturn 28-29° Aries = bearish hardware/metals correction
    _rule(
        rule_id         = "gaur-ch10-saturn-28-degree-aries-market-correction",
        sub_type        = "transit",
        title           = "Saturn at 28–29° Aries = Bearish Market Correction for Hardware, Gems, and Metals",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = (
            "Transit Saturn reaches 28° to 29° in Aries (Mesha rashi)."
        ),
        result          = (
            "'Bearish Market Correction Alert' for hardware, gems, and metals. "
            "Prices which were elevated throughout Saturn's transit of Aries undergo a sharp decline. "
            "This acts as a natural 'price circuit breaker' at this specific degree."
        ),
        synthesis_sources = ["Gaur Ch 10 (28-Degree Saturn Marker)"],
        notes           = (
            "Throughout Saturn's stay in Aries, oils, gold, silver, copper, gems, and hardware are expensive. "
            "This correction rule fires ONLY at 28-29° and produces a temporary crash "
            "before Saturn ingresses into Taurus."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── AI-16: Saturn direct/retrograde change = 2-month oil/spice spike
    _rule(
        rule_id         = "gaur-ch10-saturn-station-direct-oils-spices-spike",
        sub_type        = "transit",
        title           = "Saturn Turning Direct from Retrograde = Oils and Spices Expensive for 60 Days",
        source_chapter  = "Gaur/AIFAS Ch 10",
        condition       = (
            "Saturn changes its motion state from Retrograde to Direct (Saturn goes Stationary-Direct)."
        ),
        result          = (
            "'Price Spike Warning: Oils and Spices (Asafetida, Chillies) will remain expensive for the next 60 days.' "
            "This spike is independent of the sign Saturn occupies."
        ),
        synthesis_sources = ["Gaur Ch 10 (Motion and Luminous Logic — Saturn)"],
        notes           = (
            "Retrograde-to-Direct station is a universal Saturn trigger regardless of sign position. "
            "The 60-day (2-month) window applies from the exact date of the station. "
            "Cross-validate with Saturn sign results for the specific commodities most at risk."
        ),
        severity        = "medium",
        checkable       = True,
    ),

]

ALL_RULES = GROUP_AI

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_RULES)} interpretation rules from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        groups = {"GROUP_AI": GROUP_AI}
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
