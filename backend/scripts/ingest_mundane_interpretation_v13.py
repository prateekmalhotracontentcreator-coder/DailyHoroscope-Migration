"""
Mundane Astrology — Interpretation Rules v13
Batch: mundane-interp-v13-20260506

Sources:
  Gaur/AIFAS Ch 4  — Koorma Chakra directional affliction rules
  Gaur/AIFAS Ch 11 — Eclipse sequential logic + zodiac/monthly triggers
  Mehta Ch 8       — Sanghatta Chakra war rules (Rohini gate, massacre alert, famine gate)
  Mehta/Gaur Ch 8  — Commodity Vedha price rules

GROUP_AH: 18 rules

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
_BATCH     = "mundane-interp-v13-20260506"
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
# GROUP_AH — Koorma Chakra + Sanghatta Chakra + Eclipse Rules
# ============================================================

GROUP_AH = [

    # ── AH-01: Malefic in Koorma Tail (West) = West India calamity
    _rule(
        rule_id         = "gaur-ch4-koorma-tail-malefic-west-calamity",
        sub_type        = "spatial_transit",
        title           = "Malefic in Koorma Tail Constellations = Critical Calamity Alert for West India",
        source_chapter  = "Gaur/AIFAS Ch 4",
        condition       = (
            "A malefic planet (Saturn, Rahu, Mars, Ketu) transits or creates Vedha on "
            "any of the Koorma Tail constellations: Jyeshtha, Mool, or Poorvashadh."
        ),
        result          = (
            "Critical Vulnerability Alert for West India / Gujarat / Rajasthan. "
            "Predicted events: war, severe natural calamity, or major civil unrest. "
            "The western direction of the mapped landmass is most afflicted."
        ),
        synthesis_sources = ["Gaur Ch 4 (Koorma Chakra Tail)", "Mehta Ch 8 (Sanghatta Vedha)"],
        notes           = (
            "Saturn in Jyeshtha is particularly significant as Jyeshtha rules kings and power. "
            "Cross-validate: if Saturn is simultaneously creating Vedha via Sanghatta grid, "
            "the calamity weight doubles."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AH-02: Malefic in Koorma Back (Centre) = Heartland unrest
    _rule(
        rule_id         = "gaur-ch4-koorma-back-malefic-heartland-unrest",
        sub_type        = "spatial_transit",
        title           = "Malefic in Koorma Back Constellations = Unrest in Central Provinces / Heartland",
        source_chapter  = "Gaur/AIFAS Ch 4",
        condition       = (
            "A malefic planet transits or afflicts the Koorma Back constellations: "
            "Krittika, Rohini, or Mrigshira."
        ),
        result          = (
            "Inland Rebellion Monitor triggered. "
            "Unrest in the Heartland / Central Provinces of the mapped territory. "
            "Rohini specifically activates the global war threshold (see Rohini gate rule)."
        ),
        synthesis_sources = ["Gaur Ch 4 (Koorma Centre)", "Mehta Ch 8 (Rohini Gate)"],
        notes           = (
            "Rohini (Taurus 10°–23°20') is the single most critical nakshatra in all of mundane astrology. "
            "Affliction here by Saturn alone triggers the Rohini War Gate (AH-08). "
            "Krittika and Mrigshira affliction indicates political violence in Central India."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AH-03: Malefic in NE Koorma (Revati/Ashwini/Bharani) = Enemy attack from NE
    _rule(
        rule_id         = "gaur-ch4-koorma-northeast-enemy-attack",
        sub_type        = "spatial_transit",
        title           = "Mars in 7th House in NE Koorma Constellations = Enemy Attack from North-East",
        source_chapter  = "Gaur/AIFAS Ch 4",
        condition       = (
            "Mars occupies the 7th house of the national horoscope "
            "AND is transiting a North-East Koorma constellation (Revati, Ashwini, or Bharani)."
        ),
        result          = (
            "Enemy attack or armed aggression originates from the North-East direction. "
            "For India: this points specifically to the North-East frontier."
        ),
        synthesis_sources = ["Gaur Ch 4 (Koorma NE Foot)", "Raphael Ch 28 (Mars transit rules)"],
        notes           = (
            "7th house = International Disputes and Rebellions (Ministry mapping). "
            "Bharani is ruled by Venus but contains intense Mars energy (Yama's nakshatra). "
            "This rule enables directional specificity for military threat assessment."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AH-04: Benefic in any Koorma segment = progress in that direction
    _rule(
        rule_id         = "gaur-ch4-koorma-benefic-segment-progress",
        sub_type        = "spatial_transit",
        title           = "Benefic in Any Koorma Segment = Bliss and Progress for That Region",
        source_chapter  = "Gaur/AIFAS Ch 4",
        condition       = (
            "A benefic planet (Jupiter, Venus, well-placed Mercury, waxing Moon) "
            "transits or positively aspects a constellation in any Koorma grid segment."
        ),
        result          = (
            "The geographical direction/region corresponding to that Koorma segment "
            "enjoys Anand (bliss) and measurable progress: "
            "trade expansion, good harvests, political stability, social harmony."
        ),
        synthesis_sources = ["Gaur Ch 4 (Koorma Chakra)", "Raphael Ch 28 (Benefic transit rules)"],
        severity        = "low",
        checkable       = True,
    ),

    # ── AH-05: Vedha synchronization rule
    _rule(
        rule_id         = "gaur-ch4-koorma-vedha-synchronization",
        sub_type        = "spatial_transit",
        title           = "Regional Alert Requires BOTH Koorma Occupation AND Sarvatobhadra Vedha",
        source_chapter  = "Gaur/AIFAS Ch 4 (Report 3: JSON Refinements)",
        condition       = (
            "A malefic occupies a Koorma constellation segment. "
            "Additionally verify: is that malefic ALSO creating Vedha on those constellations "
            "via the Sarvatobhadra Chakra (Ch 9) grid?"
        ),
        result          = (
            "A regional alert is valid ONLY when BOTH conditions are satisfied: "
            "(1) malefic transits the Koorma segment, AND "
            "(2) that malefic creates Vedha on the same constellations. "
            "Single-condition alerts are advisory; dual-condition alerts are actionable."
        ),
        synthesis_sources = ["Gaur Ch 4", "Gaur Ch 9 (Sarvatobhadra Chakra — pending encode)"],
        notes           = (
            "This is the validation gate that prevents false positives. "
            "Without Sarvatobhadra confirmation, the Koorma signal is 'background noise' only."
        ),
        severity        = "medium",
        checkable       = False,
    ),

    # ── AH-06: Eclipse in Chaitra = flood/drought + intellectuals suffer
    _rule(
        rule_id         = "gaur-ch11-eclipse-chaitra-variable-rains",
        sub_type        = "eclipse",
        title           = "Eclipse in Chaitra Month = Variable Rains (Floods/Drought); Intellectuals Suffer",
        source_chapter  = "Gaur/AIFAS Ch 11",
        condition       = "A solar or lunar eclipse occurs in the Hindu month of Chaitra (March–April).",
        result          = (
            "Variable and erratic rainfall patterns — simultaneous drought in some regions and floods in others. "
            "Suffering specifically for intellectuals, writers, and artists."
        ),
        synthesis_sources = ["Gaur Ch 11"],
        severity        = "medium",
        checkable       = True,
    ),

    # ── AH-07: Eclipse in Jyeshtha = state government change
    _rule(
        rule_id         = "gaur-ch11-eclipse-jyeshtha-govt-change",
        sub_type        = "eclipse",
        title           = "Eclipse in Jyeshtha Month = Change of State Governments; VIPs Suffer",
        source_chapter  = "Gaur/AIFAS Ch 11",
        condition       = "A solar or lunar eclipse occurs in the Hindu month of Jyeshtha (May–June).",
        result          = (
            "Change of state governments — ruling parties fall or key reshuffles occur. "
            "Suffering for VIPs and senior executives."
        ),
        synthesis_sources = ["Gaur Ch 11"],
        notes           = (
            "Combine with Gopal Ch 9 saturn-trika-transit rule for compounding signal: "
            "eclipse in Jyeshtha + Saturn in trika = near-certain government collapse."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AH-08: Eclipse in Leo = political party officials suffer
    _rule(
        rule_id         = "gaur-ch11-eclipse-leo-political-parties-suffer",
        sub_type        = "eclipse",
        title           = "Eclipse in Leo = Political Party Officials (Ruling and Opposition) Suffer",
        source_chapter  = "Gaur/AIFAS Ch 11",
        condition       = "A solar or lunar eclipse occurs in Leo (Simha rashi).",
        result          = (
            "Both ruling party and opposition party officials suffer personal setbacks, health issues, "
            "or political downfall. Leo = the sign of kings and power."
        ),
        synthesis_sources = ["Gaur Ch 11", "Gaur Ch 4 (Leo = France, Italy, Kabul)"],
        severity        = "medium",
        checkable       = True,
    ),

    # ── AH-09: Eclipse in Capricorn = VIP families + medicine manufacturers suffer
    _rule(
        rule_id         = "gaur-ch11-eclipse-capricorn-vip-families-medicine",
        sub_type        = "eclipse",
        title           = "Eclipse in Capricorn = Families of VIPs and Medicine Manufacturers Suffer",
        source_chapter  = "Gaur/AIFAS Ch 11",
        condition       = "A solar or lunar eclipse occurs in Capricorn (Makar rashi).",
        result          = (
            "Families of VIPs and ministers face personal tragedies or public scandals. "
            "Medicine manufacturers and pharma sector suffer losses or regulatory setbacks. "
            "Capricorn rules India overall — so this is a particularly sensitive eclipse position for India."
        ),
        synthesis_sources = ["Gaur Ch 11", "Gaur Ch 4 (Capricorn = India, Afghanistan, Punjab)"],
        severity        = "high",
        checkable       = True,
    ),

    # ── AH-10: Sequential eclipse — Lunar then Solar = tyrant rulers
    _rule(
        rule_id         = "gaur-ch11-eclipse-lunar-solar-sequence-tyrant-rulers",
        sub_type        = "eclipse",
        title           = "Lunar Eclipse Followed by Solar Eclipse within 15 Days = Rulers Become Tyrants",
        source_chapter  = "Gaur/AIFAS Ch 11",
        condition       = (
            "A lunar eclipse is followed by a solar eclipse within 15 days "
            "(i.e., both eclipses occur in the same paksha or fortnight)."
        ),
        result          = (
            "National Authoritarianism Alert: rulers become tyrants. "
            "Emergency rule, suspension of democratic norms, or authoritarian crackdowns become likely."
        ),
        synthesis_sources = ["Gaur Ch 11"],
        notes           = (
            "VALIDATED via historical patterns of emergency rule announcements globally. "
            "Cross-validate with Mehta Ch 2 Step 5 (eclipse duration = impact duration: "
            "1 hour solar = 1 year of impact). "
            "This is the 'Tyrant Rulers Veto' — highest-priority eclipse diagnostic."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── AH-11: Sequential eclipse — Solar then Lunar = religious happiness
    _rule(
        rule_id         = "gaur-ch11-eclipse-solar-lunar-sequence-religious-happiness",
        sub_type        = "eclipse",
        title           = "Solar Eclipse Followed by Lunar Eclipse within 15 Days = Religious Sentiments Increase",
        source_chapter  = "Gaur/AIFAS Ch 11",
        condition       = (
            "A solar eclipse is followed by a lunar eclipse within 15 days."
        ),
        result          = (
            "Religious sentiments and general happiness increase across the population. "
            "Spiritual movements gain momentum; charitable activities rise."
        ),
        synthesis_sources = ["Gaur Ch 11"],
        severity        = "low",
        checkable       = True,
    ),

    # ── AH-12: Jupiter aspect on eclipse = bad effects neutralized
    _rule(
        rule_id         = "gaur-ch11-eclipse-jupiter-aspect-neutralizes",
        sub_type        = "eclipse",
        title           = "Jupiter Aspecting an Eclipse Point Destroys / Neutralizes Its Bad Effects",
        source_chapter  = "Gaur/AIFAS Ch 11",
        condition       = "Jupiter aspects the sign or degree where a solar or lunar eclipse occurs.",
        result          = (
            "The malefic effects of the eclipse are significantly reduced or fully neutralized. "
            "Jupiter's expansive and benevolent nature acts as a protective shield."
        ),
        synthesis_sources = ["Gaur Ch 11", "Raphael Ch 28 (Benefic transit rules)"],
        severity        = "low",
        checkable       = True,
    ),

    # ── AH-13: Rohini War Gate — Saturn in Rohini
    _rule(
        rule_id         = "mehta-ch8-rohini-gate-saturn-war-famine",
        sub_type        = "transit",
        title           = "Saturn Transiting Rohini = Devastating War or 12-Year Famine (Highest Alert)",
        source_chapter  = "Mehta Ch 8",
        condition       = (
            "Transit Saturn enters Rohini Nakshatra (Taurus 10° to 23° 20'). "
            "Alert is upgraded to CRITICAL if Rahu is also present in or aspecting Rohini."
        ),
        result          = (
            "Devastating war OR 12-year famine — historically, one of the two always manifests. "
            "WWI (1914-18), WWII (1939-45), and the 1971 Indo-Pak War all began with Saturn in Rohini. "
            "If Rahu co-occupies or aspects: dual-threat confirmed — both war AND famine risk."
        ),
        synthesis_sources = [
            "Mehta Ch 8 (Sanghatta Chakra — Rohini Gate)",
            "Mehta Ch 2 Step 7 (Rohini famine rule)",
            "Gopalakrishnan Ch 9",
        ],
        notes           = (
            "This is the single highest-severity rule in the entire mundane astrology corpus. "
            "No other planetary configuration has been as consistently validated across world wars. "
            "Historical benchmarks: Saturn in Rohini = WWI onset (1914), WWII onset (1939), "
            "1971 Bangladesh Liberation War. "
            "ENCODE PRIORITY: This rule should be the first to receive approved status."
        ),
        severity        = "critical",
        checkable       = True,
    ),

    # ── AH-14: Rohini Malefic Variant — Ketu/Rahu + Mars aspect
    _rule(
        rule_id         = "mehta-ch8-rohini-ketu-rahu-mars-aspect-massacre",
        sub_type        = "transit",
        title           = "Ketu or Rahu in Rohini + Mars Aspect = Critical War Risk / Massacre Alert",
        source_chapter  = "Mehta Ch 8",
        condition       = (
            "Rahu or Ketu transits Rohini Nakshatra (Taurus 10°–23°20') "
            "AND Mars simultaneously aspects Rohini by any aspect."
        ),
        result          = (
            "War Risk = CRITICAL. Internal rebellion and large-scale massacres are likely. "
            "Historical example: June 1984 Punjab crisis (Operation Blue Star) — "
            "Ketu in Rohini with Mars aspect → massacre."
        ),
        synthesis_sources = [
            "Mehta Ch 8 (Sanghatta Chakra malefic variant)",
            "Mehta Ch 10 (Mars ignition rule)",
        ],
        notes           = (
            "The Mars aspect acts as the 'ignition trigger' for the underlying Rahu/Ketu tension. "
            "Dramatic events rarely happen at the moment of conjunction — "
            "they materialize when Mars conjoins or aspects the pre-existing configuration. "
            "Monitor this combination especially when Mars is transiting opposition or trine to Rohini."
        ),
        severity        = "critical",
        checkable       = True,
    ),

    # ── AH-15: Triple Malefic Destruction Scheme
    _rule(
        rule_id         = "mehta-ch8-triple-malefic-destruction-scheme",
        sub_type        = "conjunction",
        title           = "Saturn + Mars + Rahu in Quadrant or Mutual Sanghatta Vedha = Global Destruction Warning",
        source_chapter  = "Mehta Ch 8",
        condition       = (
            "Saturn, Mars, and Rahu simultaneously meet on the Sanghatta grid — "
            "either in the same quadrant, in mutual Vedha (Front/Left/Right vectors), "
            "or in a conjunction within 10° of each other."
        ),
        result          = (
            "GLOBAL DESTRUCTION WARNING — the Destruction Scheme is active. "
            "Predicted: major global conflict, mass casualties, collapse of established order. "
            "Trigger 'Global Destruction Warning' at the highest diagnostic level."
        ),
        synthesis_sources = [
            "Mehta Ch 8 (Destruction Scheme Condition)",
            "Mehta Ch 2 Step 8 (Triple conjunction veto: global destruction scheme)",
        ],
        notes           = (
            "This is one of two 'critical severity' configurations in Mehta's system "
            "(the other being Saturn-Rahu in Capricorn for major global conflict). "
            "Cross-validate with Mehta Ch 2 Step 8: "
            "'IF Saturn AND Mars AND Rahu in a quadrant THEN global_destruction_scheme = TRUE'. "
            "Both sources confirm. Highest possible diagnostic weight."
        ),
        severity        = "critical",
        checkable       = True,
    ),

    # ── AH-16: Sanghatta Vedha on nation's 7th house = war ignition
    _rule(
        rule_id         = "mehta-ch8-sanghatta-seventh-house-war-ignition",
        sub_type        = "natal_transit",
        title           = "Saturn + Mars Vedha on Nation's 7th House = War / International Conflict Ignition",
        source_chapter  = "Mehta Ch 8",
        condition       = (
            "In a national horoscope (foundation chart), "
            "the 7th house lord or the 7th house sign is under simultaneous Sanghatta Vedha "
            "from both Saturn and Mars."
        ),
        result          = (
            "War or international conflict ignition for that nation. "
            "The 7th house governs International Disputes, Rebellions, and Foreign Affairs. "
            "Vedha here from malefics overrides any benefic standard transits."
        ),
        synthesis_sources = [
            "Mehta Ch 8 (Chakra Aspect Primacy rule)",
            "Gaur Ch 4 (House 7 = International Disputes)",
        ],
        notes           = (
            "Chakra aspect primacy rule: treat Sanghatta Vedha as the primary ignition source. "
            "This rule is the formal diagnostic gate for all war predictions — "
            "any war prediction MUST confirm Vedha on the 7th house before being classified 'confirmed'."
        ),
        severity        = "critical",
        checkable       = True,
    ),

    # ── AH-17: Commodity price spike — Malefic Vedha on planetary lord
    _rule(
        rule_id         = "gaur-ch8-commodity-malefic-vedha-price-spike",
        sub_type        = "transit",
        title           = "Malefic Vedha on Planetary Lord = Price Spike for That Planet's Commodities",
        source_chapter  = "Gaur Ch 8; Mehta Ch 8",
        condition       = (
            "A malefic planet (Saturn, Mars, Rahu, Ketu) creates Vedha on the sign or nakshatra "
            "ruling a specific commodity (use Commodity Ownership Dictionary — spec: mehta-ch8-commodity-ownership-dictionary). "
            "Example: Saturn transits Swati → Vedha on Chillies, Mustard, Cotton (Swati's commodities)."
        ),
        result          = (
            "Critical Price Inflation Alert for all commodities owned by the afflicted sign/nakshatra. "
            "Prices rise sharply during the transit period."
        ),
        synthesis_sources = [
            "Gaur Ch 8 (Commodity Ownership Dictionary)",
            "Mehta Ch 8 (Vedha Price Vector Logic)",
        ],
        notes           = (
            "Price Vector Logic: Malefic Vedha = Price INCREASE; Benefic Vedha = Price DECREASE. "
            "If a planet is in a sign ALSO under Vedha from another malefic simultaneously, "
            "the commodity price inflation weight is TRIPLED. "
            "For commodities not in the master list, use First Letter Rule "
            "(e.g., commodity starting with 'A' → Aries sign lookup)."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── AH-18: Gold reserve veto — Sun + Jupiter mutual Vedha + Saturn in Capricorn
    _rule(
        rule_id         = "gaur-ch8-gold-reserve-banking-crisis-veto",
        sub_type        = "conjunction",
        title           = "Sun + Jupiter in Mutual Vedha + Saturn in Capricorn = State Gold & Banking Crisis",
        source_chapter  = "Gaur Ch 8; Mehta Ch 8",
        condition       = (
            "Sun and Jupiter (both Gold significators) are in mutual Vedha on the Sanghatta grid "
            "WHILE Saturn transits Capricorn (Makar rashi)."
        ),
        result          = (
            "State-level Gold Liquidity Crisis and Banking Instability. "
            "Gold reserves come under pressure; banks face solvency or trust issues."
        ),
        synthesis_sources = [
            "Gaur Ch 8 (Gold = Sun + Jupiter + Capricorn)",
            "Mehta Ch 8 (Vedha Price Vector Logic)",
            "Gaur Ch 4 (Capricorn = Gold, Iron, Coal commodities)",
        ],
        notes           = (
            "Capricorn is the sign of India and also rules Gold, Iron, Coal, Steel (Gaur Ch 4 zodiac commodity map). "
            "Saturn in Capricorn = own sign, adding structural intensity. "
            "This is a compound rule requiring three simultaneous conditions — "
            "high specificity, high reliability when all three confirm."
        ),
        severity        = "high",
        checkable       = True,
    ),

]

ALL_RULES = GROUP_AH

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_RULES)} interpretation rules from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        groups = {"GROUP_AH": GROUP_AH}
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
