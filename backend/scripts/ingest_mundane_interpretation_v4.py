"""
Mundane Astrology — Interpretation Rules v4
Batch: mundane-interp-v4-20260506

Source: Gaur, "Mundane Astrology" (AIFAS)
  Chapter 10 — Transit of Planets (pp. 85-110)
  Chapter 11 — Results of Eclipse (pp. 111-116)

All rules: approval_status = "pending_review"
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
_BATCH     = "mundane-interp-v4-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ---------------------------------------------------------------------------
def _rule(rule_id, sub_type, title, source_chapter, condition, result,
          synthesis_sources, notes="", severity=None, checkable=False):
    d = {
        "rule_id":          rule_id,
        "batch_id":         _BATCH,
        "science_id":       "mundane_jyotish",
        "sub_type":         sub_type,
        "title":            title,
        "source_chapter":   source_chapter,
        "condition":        condition,
        "result":           result,
        "synthesis_sources": synthesis_sources,
        "checkable":        checkable,
        "approval_status":  "pending_review",
        "created_at":       _NOW,
    }
    if notes:    d["notes"]    = notes
    if severity: d["severity"] = severity
    return d

# ============================================================
# GROUP U — Planet Motion State Differentials (Gaur Ch 10)
# ============================================================
GROUP_U = [

    _rule(
        rule_id="mundane-gaur-ch10-mars-motion-differentials",
        sub_type="planet_motion_commodity",
        title="Mars Motion State Commodity Differentials",
        source_chapter="Gaur Ch 10, pp.95-96",
        condition={
            "direct_motion":   "Mars in direct motion causes fall in cotton prices after 3 days. Keeps oils and silver expensive.",
            "retrograde":      "Retrograde Mars keeps gold, silver, wheat, red things and goods influenced by own signs expensive. Effect: prices elevated 12-24 days after nakshatra entry.",
            "rising":          "When Mars rises: grains cheap, oils and oil materials expensive. Price rise occurs after 5 days.",
            "combusted":       "When Mars is combusted: grains (wheat and gram) and gur are expensive.",
            "conjunction_rule":"Conjunction or aspect with benefic planet causes fall in prices of goods ruled by Mars. Malefic conjunction elevates prices.",
        },
        result="Use motion state to determine whether Mars's sign/nakshatra price signals are amplified (retrograde, combusted) or dampened (direct, benefic aspect).",
        synthesis_sources=["Gaur Ch 10"],
        notes="Mars influence lasts 15 days to 1 month per sign. Retrograde Mars is more sinister for commodities.",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch10-mercury-motion-differentials",
        sub_type="planet_motion_commodity",
        title="Mercury Motion State Commodity Differentials",
        source_chapter="Gaur Ch 10, pp.98",
        condition={
            "direct_motion":   "Mercury direct: grains expensive. Silver and cotton undergo fluctuations initially, later expensive. Gur and perfumes also expensive.",
            "retrograde":      "Mercury retrograde: juicy materials (gur/khand) expensive. Grains cheap.",
            "rising":          "Mercury rises: wheat and gram expensive.",
            "combusted":       "Mercury combusted: wheat, gram, ghee cheap.",
        },
        result="Mercury's motion state reverses grain vs gur price signals. Direct = grains up, gur/khand up. Retrograde = grains down, gur/khand up. Combusted = grains down.",
        synthesis_sources=["Gaur Ch 10"],
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch10-jupiter-motion-differentials",
        sub_type="planet_motion_commodity",
        title="Jupiter Motion State Commodity Differentials",
        source_chapter="Gaur Ch 10, p.101",
        condition={
            "direct_motion":   "When Jupiter comes in direct motion: grains, metals and pulses are cheap.",
            "retrograde":      "Jupiter retrograde: brings down prices of grains, ELEVATES metals such as gold and silver.",
            "rising":          "When Jupiter rises: gold is cheap, silver is expensive.",
            "combusted":       "When Jupiter is combusted: gold, silver and grains become cheap.",
        },
        result="Jupiter retrograde is the key signal for precious metals (gold, silver) price elevation. Direct Jupiter benefits all grains and pulses (prices fall). Combusted Jupiter depresses everything.",
        synthesis_sources=["Gaur Ch 10"],
        notes="Jupiter's retrograde period is an important window for gold/silver price monitoring.",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch10-venus-motion-differentials",
        sub_type="planet_motion_commodity",
        title="Venus Motion State Commodity Differentials",
        source_chapter="Gaur Ch 10, p.104",
        condition={
            "direct_motion":   "Venus direct: grains, gur, ghee, gold, silver and gems expensive. Cotton cheap.",
            "retrograde":      "Venus retrograde: grains (wheat, gur, khand, ghee, oils) expensive.",
            "combusted":       "Venus combusted: gold and silver expensive. Grains expensive initially then cheap later on.",
            "rising":          "Venus rises: gold, silver, yarn, clothes, rice expensive. Ghee and khand cheap.",
        },
        result="Both direct and retrograde Venus tend to raise commodity prices (different categories). Rising Venus is the key signal for gold, silver, rice, and textile price elevation.",
        synthesis_sources=["Gaur Ch 10"],
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch10-saturn-motion-differentials",
        sub_type="planet_motion_commodity",
        title="Saturn Motion State Commodity Differentials",
        source_chapter="Gaur Ch 10, pp.107-108",
        condition={
            "direct_change":   "Saturn changes to direct motion: oil materials, chillies and asafoetida expensive for 2 months.",
            "retrograde_change": "Saturn changes to retrograde motion: oils, grains, ghee become expensive.",
            "rising":          "Saturn rises: mustard oil, peanuts and cotton cheap for 1 month; iron, gur, khand expensive.",
            "combusted":       "Saturn combusted: gold cheap, grains expensive.",
            "retrograde_nakshatra_drought_1": "Saturn retrograde in Uttarashadh moving back into Poorvashadh: drought signal, grains become expensive.",
            "retrograde_nakshatra_drought_2": "Saturn retrograde in Magha moving back into Ashlesha: wheat and ghee expensive.",
            "saturn_at_28_29_aries": "When Saturn is at 28-29° in Aries, prices go down despite general expensive trend.",
        },
        result="Saturn retrograde periods signal grain and oil price increases. The specific nakshatra retrograde patterns (Uttarashadh→Poorvashadh; Magha→Ashlesha) are drought/price triggers.",
        synthesis_sources=["Gaur Ch 10"],
        severity="high",
        checkable=True,
    ),

]

# ============================================================
# GROUP V — Rainfall and Drought Signals (Gaur Ch 10)
# ============================================================
GROUP_V = [

    _rule(
        rule_id="mundane-gaur-ch10-rahu-drought-aries-libra",
        sub_type="drought_signal",
        title="Rahu in Aries or Libra — Drought Signal",
        source_chapter="Gaur Ch 10, p.109",
        condition={
            "primary": "Rahu transiting through Aries OR Libra (both axis signs of the Aries-Libra axis).",
            "effect":  "Drought due to lack of rains. Grains expensive.",
        },
        result="Rahu in Aries or Libra is a recurring drought indicator. Grains become expensive. Cross-check with Meghesh planet and Nava Megha cloud type for convergence.",
        synthesis_sources=["Gaur Ch 10"],
        notes="Ketu is simultaneously in the opposite sign (Libra or Aries). Both nodes on the Aries-Libra axis = dual drought indicator.",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch10-sun-ingress-muhurti-tier",
        sub_type="rainfall_forecast",
        title="Sun Ingress Muhurti Tier — Rainfall and Price Forecast",
        source_chapter="Gaur Ch 10, p.91",
        condition={
            "15_muhurti_nakshatras": "If nakshatra at time of Sun ingress (Sankranti) is one of: Bharani, Ardra, Ashlesha, Jyeshtha, Shatbhisha → ingress is 15 muhurti.",
            "30_muhurti_nakshatras": "If nakshatra at ingress is: Ashwini, Krithika, Mrigshira, Pushya, Magha, Poorvaphalguni, Hast, Chitra, Anuradha, Mool, Poorvashadh, Shravan, Dhanishtha, Poorvabhadrapad, Revti → ingress is 30 muhurti.",
            "45_muhurti_nakshatras": "If nakshatra at ingress is: Rohini, Punarvasu, Uttaraphalguni, Vishakha, Uttarashadh, Uttarabhadrapad → ingress is 45 muhurti.",
        },
        result={
            "15_muhurti": "Grains and juicy materials expensive. Rains less.",
            "30_muhurti": "Grains, grass, juicy materials etc medium.",
            "45_muhurti": "Rains good. Grains, ghee, oil, cotton cheap.",
        },
        synthesis_sources=["Gaur Ch 10"],
        notes="Ingress = Sun moving from one zodiac sign to the next (Sankranti). Check nakshatra at precise moment of ingress. This gives a broad forecast for that solar month.",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch10-transit-synthesis-methodology",
        sub_type="commodity_forecast_synthesis",
        title="Transit Synthesis Methodology — Multi-Planet Commodity Forecast",
        source_chapter="Gaur Ch 10, pp.109-110",
        condition={
            "method": "To forecast prices of grains, metals etc for a period: (1) Find the sign and nakshatra of each planet from ephemeris. (2) Note direct/retrograde/accelerated motion. (3) Evaluate obstruction results in Sarvatobhadra chakra. (4) Find which materials are expensive/cheap from each planet's sign + nakshatra + motion state. (5) Aggregate results — majority signal wins.",
            "example": "August 2002: Sun in Pushya/Ashlesha/Magha → grains expensive. Mars in Ashlesha/Magha → grains expensive. Mercury in Ashlesha/Magha → high prices, but Mercury enters Poorvaphalguni on 10th Aug (grains cheap). Jupiter in Pushya → prices high. Venus in Uttaraphalguni (fluctuates) then Hast (prices fall). Saturn in 3rd pad Mrigshira → prices fall; 4th pad → prices rise. Net forecast for August 2002: grains expensive overall, but Mercury entry into Poorvaphalguni and Venus entry into Hast on 11th Aug will bring prices down. Leo ingress on 17th Aug on Friday = 15 muhurti → low grain prices confirmed.",
        },
        result="Composite multi-planet transit signal: cross all 7-9 planet nakshatra/sign positions + motion states to derive net commodity price direction. Convergence of 5+ planets on expensive signal = strong bullish forecast for that commodity.",
        synthesis_sources=["Gaur Ch 10"],
        notes="This is the core methodology of Gaur Ch 10. Not a single rule but the aggregation framework. Use lookup specs gaur-ch10-*-transit for individual planet signals.",
    ),

]

# ============================================================
# GROUP W — Eclipse Rules: Gaur Ch 11 (Commodity Focus)
# ============================================================
GROUP_W = [

    _rule(
        rule_id="mundane-gaur-ch11-eclipse-severity-duration",
        sub_type="eclipse_commodity_severity",
        title="Eclipse Coverage Percentage → Effect Duration",
        source_chapter="Gaur Ch 11, p.113-114",
        condition={
            "100_percent": "Full eclipse (totality): commodity effects materialise within 20 days.",
            "75_percent":  "75% coverage: effects felt within 1 month.",
            "50_percent":  "50% coverage: effects felt within 2 months.",
            "33_percent":  "33% coverage: effects felt within 3 months.",
            "25_percent":  "25% coverage: effects felt within 4 months.",
            "rise_or_setting": "If rise or setting occurs during solar/lunar eclipse: commercial goods become expensive particularly.",
            "rain_modifier": "If rains fall after eclipse: intensity of undesired commodity results is reduced.",
        },
        result="Eclipse magnitude directly controls how quickly and strongly commodity price effects manifest. Full eclipse = immediate 20-day effect window. Partial eclipse = delayed effect by months.",
        synthesis_sources=["Gaur Ch 11"],
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch11-two-eclipses-fortnight-calamity",
        sub_type="eclipse_double_calamity",
        title="Two Eclipses Within 15 Days — Turmoil and Grain Price Surge",
        source_chapter="Gaur Ch 11, p.113",
        condition={
            "trigger": "Two eclipses (solar + lunar) occurring within a 15-day fortnight.",
            "sequence_note": "If lunar eclipse 15 days AFTER solar eclipse: beneficial outcome.",
            "inverse": "If solar eclipse comes AFTER lunar eclipse: results undesired and detrimental.",
        },
        result="Two eclipses in a fortnight → turmoils or natural calamities in the world, resulting in loss of money and lives. Grains become expensive. The sequence (solar first vs lunar first) determines whether outcome is harmful or beneficial.",
        synthesis_sources=["Gaur Ch 11", "Mehta Ch 13"],
        notes="Cross-reference with Mehta Ch 13 rule: two eclipses in fortnight also signals war risk at geopolitical level.",
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch11-saturn-in-eclipse-sign",
        sub_type="eclipse_saturn_metals",
        title="Saturn Residing in Eclipse Sign — Metals Expensive",
        source_chapter="Gaur Ch 11, p.113",
        condition={
            "primary": "Saturn is also transiting through the sign in which the solar or lunar eclipse occurs.",
        },
        result="When Saturn is in the eclipse sign: metals (gold, silver, iron) become expensive.",
        synthesis_sources=["Gaur Ch 11"],
        notes="Compound signal: eclipse sign's commodity effects + Saturn's malefic amplification of metal prices.",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch11-jupiter-aspect-eclipse-benefic",
        sub_type="eclipse_jupiter_benefic",
        title="Jupiter Full Aspect on Eclipse — Reduces Malefic Effects",
        source_chapter="Gaur Ch 11, p.116",
        condition={
            "primary": "Jupiter's full (7th house) aspect falls on the eclipse point (solar or lunar).",
        },
        result="Jupiter's full aspect on eclipse reduces the above undesired results; peace and prosperity prevail. This is the primary mitigating factor for eclipse maleficence.",
        synthesis_sources=["Gaur Ch 11"],
        notes="Other planetary aspects on eclipse: Mars = red things expensive; Mercury = ghee/oils/maize/gold/brass expensive; Venus = silver/white clothes expensive; Saturn = black things/iron/urad/black grains expensive.",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch11-eclipse-solar-commodity-by-month",
        sub_type="eclipse_commodity_month",
        title="Solar Eclipse in Each Hindu Month — Commodity Price Effects",
        source_chapter="Gaur Ch 11, pp.111",
        condition={
            "Chaitra":     "Solar eclipse in Chaitra month.",
            "Vaishakh":    "Solar eclipse in Vaishakh month.",
            "Jyeshtha":    "Solar eclipse in Jyeshtha month.",
            "Aashadh":     "Solar eclipse in Aashadh month.",
            "Shravan":     "Solar eclipse in Shravan month.",
            "Bhadrapad":   "Solar eclipse in Bhadrapad month.",
            "Ashwin":      "Solar eclipse in Ashwin month.",
            "Kartik":      "Solar eclipse in Kartik month.",
            "Margsheersh": "Solar eclipse in Margsheersh month.",
            "Paush":       "Solar eclipse in Paush month.",
            "Maagh":       "Solar eclipse in Maagh month.",
            "Phalgun":     "Solar eclipse in Phalgun month.",
        },
        result={
            "Chaitra":     "Gold and grains become expensive quickly.",
            "Vaishakh":    "Til, oil materials, moong, cotton cloth, yarn, cotton and wheat expensive.",
            "Jyeshtha":    "Gold and grains cheap.",
            "Aashadh":     "Grains expensive. Drought.",
            "Shravan":     "Grains cheap but juicy materials expensive.",
            "Bhadrapad":   "Grains cheap. Other goods also cheap.",
            "Ashwin":      "Grains cheap but oil materials and ghee slightly expensive.",
            "Kartik":      "All grains, ghee, cotton, clothes become cheap.",
            "Margsheersh": "Grains, gur, khand, oil materials, ghee expensive.",
            "Paush":       "All grains expensive.",
            "Maagh":       "Grains cheap, ghee expensive. Rains sufficient.",
            "Phalgun":     "All grains, oil, gur, khand, juicy materials, ghee expensive.",
        },
        synthesis_sources=["Gaur Ch 11"],
        notes="See gaur-ch11-eclipse-commodity-tables engine spec for complete lookup table including lunar eclipse by month.",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch11-eclipse-aashadh-drought",
        sub_type="drought_signal",
        title="Solar Eclipse in Aashadh — Drought Signal",
        source_chapter="Gaur Ch 11, p.111",
        condition={
            "primary": "Solar eclipse occurs during Aashadh (Hindu month, ~June-July).",
        },
        result="Grains become expensive. Drought signal — lack of sufficient rainfall in that agricultural season.",
        synthesis_sources=["Gaur Ch 11"],
        notes="Scorpio sign eclipse also independently signals drought (see eclipse_by_sign table). Convergence of Aashadh solar eclipse + Scorpio placement = strong drought indicator.",
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gaur-ch11-eclipse-scorpio-drought",
        sub_type="drought_signal",
        title="Eclipse in Scorpio — Drought Causing Agony to Masses",
        source_chapter="Gaur Ch 11, p.113",
        condition={
            "primary": "Solar or lunar eclipse occurs while the Sun/Moon is in Scorpio rashi.",
        },
        result="Drought causing agony to masses.",
        synthesis_sources=["Gaur Ch 11"],
        notes="Distinct from Gaur Ch 10 Rahu-in-Aries/Libra drought rule. This is eclipse-specific. Cross-reference with Mehta seismic/geopolitical rules for Scorpio-Taurus axis.",
        severity="high",
        checkable=True,
    ),

]

# ============================================================
ALL_RULES = GROUP_U + GROUP_V + GROUP_W

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_RULES)} rules from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")

        sub_types = {}
        for r in ALL_RULES:
            st = r["sub_type"]
            sub_types[st] = sub_types.get(st, 0) + 1

        print("Breakdown by sub_type:")
        for st, cnt in sorted(sub_types.items()):
            print(f"  {st:<45}: {cnt}")

        print(f"\nTotal: {len(ALL_RULES)}\n\nRule IDs:")
        for r in ALL_RULES:
            print(f"  {r['rule_id']}")

        print("\nDry run complete.")
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
