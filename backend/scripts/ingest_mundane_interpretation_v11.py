"""
Mundane Astrology — Interpretation Rules v11
Batch: mundane-interp-v11-20260506

Source: Dr. Jagdamba Prasad Gaur, "Mundane Astrology" (AIFAS, 2nd ed. 2010)
  Chapter 1 — Samvatsar (pp. 3-7, Part 1: Samvatsar Vichar)

GROUP_AF: 14 rules — Gaur Ch 1 Samvatsar lord annual effects
  AF-01 through AF-12: one rule per Samvatsar lord (12 lords)
  AF-13: Samvatsar group modifier (Brahma/Vishnu/Shiv group quality)
  AF-14: Venus as Samvatsar lord = earthquakes and natural calamities

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
_BATCH     = "mundane-interp-v11-20260506"
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
# GROUP_AF — GAUR Ch 1 SAMVATSAR ANNUAL EFFECTS BY LORD
# ============================================================

GROUP_AF = [

    # ── Rule AF-01: Brahma as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-brahma-lord-rulers-pleased",
        sub_type        = "samvatsar",
        title           = "Brahma as Samvatsar Lord = Rulers Pleased, Luxury Increases, Good Crops",
        source_chapter  = "Gaur Ch 1, p. 5",
        condition       = (
            "The current Samvatsar has Brahma as its lord. "
            "Brahma-lord Samvatsars: #1 Prabhav, #21 Sarvjat, #41 Plavang."
        ),
        result          = (
            "Rulers, cabinet ministers, and senior officers remain pleased. "
            "Increase in people's luxuries and comforts. "
            "Crop is good due to absence of disease or loss in plants. "
            "MONTHLY PATTERN: Chaitra and Baisakh are lucky with cheap things. "
            "Jyeshtha, Aashadh, Shravan: grains costly. "
            "Bhadrapad: lucky. "
            "Ashwin: grains dearer, diseases cause agony. "
            "Kartik through Phalgun: normal."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Brahma-lord years are generally auspicious for governance and agriculture. "
            "The mid-year (monsoon months) may see price rises despite good crops overall."
        ),
        severity        = "low",
        checkable       = True,
    ),

    # ── Rule AF-02: Vishnu as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-vishnu-lord-law-order-diseases",
        sub_type        = "samvatsar",
        title           = "Vishnu as Samvatsar Lord = Law and Order Enforced, Many Diseases, Plentiful Rains",
        source_chapter  = "Gaur Ch 1, p. 5",
        condition       = (
            "The current Samvatsar has Vishnu as its lord. "
            "Vishnu-lord Samvatsars: #2 Vibhav, #22 Sarvdhari, #42 Keelak."
        ),
        result          = (
            "Rulers and senior officers take stern measures to maintain law and order. "
            "Common people forget differences and live with peace and happiness. "
            "Rains and crops are good. Many diseases are prevalent throughout the year. "
            "Hilly areas experience more difficulties and agonies. "
            "MONTHLY PATTERN: Chaitra/Baisakh/Jyeshtha — juicy materials costly. "
            "Aashadh/Shravan/Bhadrapad — plentiful rains. "
            "Ashwin — juices costly but become cheap later. "
            "Kartik through Phalgun — grains cheap."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Vishnu years balance political order with widespread disease. "
            "The second half of the year (Kartik onwards) is economically favourable."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── Rule AF-03: Shiv as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-shiv-lord-rulers-overthrown",
        sub_type        = "samvatsar",
        title           = "Shiv as Samvatsar Lord = Rulers Overthrown, President's Rule, Heavy Rains Mid-Year",
        source_chapter  = "Gaur Ch 1, p. 5",
        condition       = (
            "The current Samvatsar has Shiv as its lord. "
            "Shiv-lord Samvatsars: #3 Shukla, #23 Virodhi, #43 Saumya."
        ),
        result          = (
            "People live with relatives happily but there is friction between "
            "rulers and opposition parties. "
            "Rulers of many places lose their throne; president's or emergency rule may be imposed. "
            "MONTHLY PATTERN: Chaitra/Baisakh/Jyeshtha — normal. "
            "Aashadh/Shravan/Bhadrapad — heavy rains. "
            "Ashwin — spread of diseases, all things dearer but Ghee is cheap. "
            "Kartik through Maagh — initially costly then cheap. "
            "Phalgun — full of difficulties and agony."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Shiv years are politically turbulent. "
            "The year-end (Phalgun) is particularly difficult. "
            "Validates political instability indicators in national charts."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AF-04: Sun as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-sun-lord-less-rain-insurgency",
        sub_type        = "samvatsar",
        title           = "Sun as Samvatsar Lord = Less Rain, Insurgencies, Violence, Throne Changes",
        source_chapter  = "Gaur Ch 1, p. 5",
        condition       = (
            "The current Samvatsar has Sun as its lord. "
            "Sun-lord Samvatsars: #4 Pramod, #24 Vikriti, #44 Sadharan, #13 Pramathi, #53 Siddharthi."
        ),
        result          = (
            "Rains are less. Insurgencies in the country encourage violence. "
            "Persons of lower class remain in anxiety. The throne is changed at few places. "
            "Conflict between rulers and businessmen. "
            "MONTHLY PATTERN: Chaitra/Baisakh — goods become costlier. "
            "Jyeshtha — diseases cause agony. "
            "Aashadh/Shravan/Bhadrapad — rains scanty. "
            "Ashwin — rain harms crops. "
            "Kartik/Margsheersh/Paush/Magh — juicy materials dearer. "
            "Phalgun — medium."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Sun years are dry and politically unstable. "
            "Agriculture suffers due to scanty monsoon. "
            "Cross-reference: Raphael Mars transit rules for insurgency timing within the year."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AF-05: Moon as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-moon-lord-all-months-excellent",
        sub_type        = "samvatsar",
        title           = "Moon as Samvatsar Lord = All 12 Months Excellent, Plentiful Rains, Cheap Grains",
        source_chapter  = "Gaur Ch 1, p. 6",
        condition       = (
            "The current Samvatsar has Moon as its lord. "
            "Moon-lord Samvatsars: #5 Prajapati, #25 Khar, #45 Virodhkrit, #14 Vikram, #54 Raudra."
        ),
        result          = (
            "All people leave their rivalries. Rains are plentiful. Grains are cheap. "
            "All 12 months are excellent. Rains could be deficient at few places. "
            "MONTHLY PATTERN: Chaitra through Bhadrapad — excellent. "
            "Ashwin — diseases more prevalent, grains costlier. "
            "Kartik/Margsheersh — things cheap. "
            "Paush/Magh/Phalgun — natural calamities cause losses."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Moon years are the most broadly auspicious — 'all 12 months excellent' is unique to Moon. "
            "The year-end (Paush-Phalgun) carries natural calamity risk despite overall prosperity."
        ),
        severity        = "low",
        checkable       = True,
    ),

    # ── Rule AF-06: Mars as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-mars-lord-plentiful-grains-wars",
        sub_type        = "samvatsar",
        title           = "Mars as Samvatsar Lord = Plentiful Grains but Rulers in Conflicts, World Peace Breached",
        source_chapter  = "Gaur Ch 1, p. 6",
        condition       = (
            "The current Samvatsar has Mars as its lord. "
            "Mars-lord Samvatsars: #6 Angira, #26 Nandan, #46 Paridhavi, #15 Vrish, #55 Durmati."
        ),
        result          = (
            "Grains are plentiful. Rulers remain engaged in conflicts. "
            "The peace of world is breached by wars. "
            "MONTHLY PATTERN: Chaitra/Baisakh — grains cheap. "
            "Jyeshtha — storms. "
            "Aashadh — heavy rains and floods. "
            "Shravan/Bhadrapad/Ashwin — disease widespread. "
            "Kartik — grains costly. "
            "Margsheersh/Paush/Magh/Phalgun — normal."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Mars years show an interesting paradox: good grain production but political violence. "
            "Flood risk in Aashadh (Jul); disease peak in monsoon end (Shravan-Ashwin). "
            "Aligns with Mars as karaka for wars and disputes."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── Rule AF-07: Mercury as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-mercury-lord-harmony-good-produce",
        sub_type        = "samvatsar",
        title           = "Mercury as Samvatsar Lord = Good Produce, Satisfactory Rains, Harmony, Diseases Removed",
        source_chapter  = "Gaur Ch 1, p. 6",
        condition       = (
            "The current Samvatsar has Mercury as its lord. "
            "Mercury-lord Samvatsars: #7 Shree Mukh, #27 Vijai, #47 Pramadi, #16 Chitrabhanu, #56 Dundubhi."
        ),
        result          = (
            "Produce of grains is good. Rains are satisfactory. "
            "Farmers get good returns for their crops. "
            "People have less conflicts and more harmony. "
            "Brahmins remain busy in religious practices; people inclined towards noble deeds. "
            "Diseases are removed. No specific adverse monthly pattern noted."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Mercury years are generally benefic across all domains: agriculture, health, social harmony. "
            "No monthly breakdown given — the benefic quality is uniform throughout the year. "
            "The most straightforwardly positive of all Samvatsar lords after Moon."
        ),
        severity        = "low",
        checkable       = True,
    ),

    # ── Rule AF-08: Jupiter as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-jupiter-lord-excessive-rains-disease",
        sub_type        = "samvatsar",
        title           = "Jupiter as Samvatsar Lord = Excessive Rains, High Prices, Excessive Disease but People Feel Secure",
        source_chapter  = "Gaur Ch 1, p. 6-7",
        condition       = (
            "The current Samvatsar has Jupiter as its lord. "
            "Jupiter-lord Samvatsars: #8 Bhav, #28 Jai, #48 Anand, #17 Subhanu, #57 Rudhirodgari."
        ),
        result          = (
            "Diseases are excessive. Grain production is medium. "
            "Though rulers engage in wars, people have a feeling of security. "
            "Rains are excessive; cattle give more milk. All things are dear (high prices). "
            "MONTHLY PATTERN: Chaitra — medium. Baisakh — food materials costly. "
            "Aashadh/Shravan — rains normal. Bhadrapad — excessive rains. "
            "Ashwin — excessive disease. Kartik — beneficial. "
            "Margsheersh/Paush/Magh/Phalgun — grains cheap."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Jupiter years show high prices and disease despite political security. "
            "The excessive rain pattern leads to flooding and crop damage despite high yield cattle. "
            "Year-end (Kartik onwards) corrects grain prices towards cheap."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── Rule AF-09: Venus as Samvatsar lord (split into general rule + earthquake rule)
    _rule(
        rule_id         = "gaur-ch1-samvatsar-venus-lord-natural-calamities",
        sub_type        = "samvatsar",
        title           = "Venus as Samvatsar Lord = Earthquakes and Natural Calamities, Female Supremacy, Excessive Rains",
        source_chapter  = "Gaur Ch 1, p. 7",
        condition       = (
            "The current Samvatsar has Venus as its lord. "
            "Venus-lord Samvatsars: #9 Yuva, #29 Manmath, #49 Rakshas, #18 Taran, #58 Raktaksha."
        ),
        result          = (
            "Milk production is good. Rains are excessive. "
            "Ladies remain engaged in activities of all types. Young people want luxuries. "
            "All people live comfortably. Supremacy of females is established. "
            "EARTHQUAKE AND CALAMITY RISK throughout the year. "
            "MONTHLY PATTERN: Chaitra/Baisakh — natural calamities. "
            "Jyeshtha — disease. Aashadh — rains. Shravan — winds, grains become costly. "
            "Bhadrapad — floods cause loss. "
            "Ashwin/Margsheersh — beneficial. Paush/Magh — medium. Phalgun — trouble."
        ),
        synthesis_sources = [
            "Gaur Ch 1",
            "Raphael Ch 26 (earthquake rules: Venus/malefics in fixed signs)",
        ],
        notes           = (
            "Venus years have a dual character: social prosperity and luxury on one side, "
            "earthquake/calamity risk on the other. "
            "Cross-validate with Raphael Ch 26 earthquake rules (malefics in Taurus/Scorpio) "
            "to assess earthquake risk in a specific Venus samvatsar year."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AF-10: Saturn as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-saturn-lord-war-atmosphere-fearful",
        sub_type        = "samvatsar",
        title           = "Saturn as Samvatsar Lord = War Atmosphere, People Fearful, Good Crops but Flood Losses",
        source_chapter  = "Gaur Ch 1, p. 7",
        condition       = (
            "The current Samvatsar has Saturn as its lord. "
            "Saturn-lord Samvatsars: #10 Dhata, #30 Durmukh, #50 Nal, #19 Parthiv, #59 Krodhan."
        ),
        result          = (
            "Rulers create atmosphere for war due to their diplomatic actions. "
            "People remain fearful. Crops are good. Widespread rains also cause losses. "
            "MONTHLY PATTERN: Chaitra/Baisakh — grains costlier. "
            "Jyeshtha — normal. Aashadh — rains less, oils and ghee costlier. "
            "Ashwin — juicy materials and metals costly. Kartik — grains cheap."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Saturn years create geopolitical tension even when agriculture is good. "
            "Fear and insecurity are the dominant social themes. "
            "Validates Saturn transit rules from Raphael (chronic troubles in countries ruled by sign)."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AF-11: Rahu as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-rahu-lord-drought-north-floods-east",
        sub_type        = "samvatsar",
        title           = "Rahu as Samvatsar Lord = Drought in North, Floods in East, War in West, Riots Year-End",
        source_chapter  = "Gaur Ch 1, p. 7",
        condition       = (
            "The current Samvatsar has Rahu as its lord. "
            "Rahu-lord Samvatsars: #11 Eashwar, #31 Hamelambi, #51 Pingal, #20 Vyaya, #60 Kshaya."
        ),
        result          = (
            "Superficially: all people live happily and fruits and grains are good. "
            "But GEOGRAPHIC EFFECTS are severe and directional: "
            "DROUGHT in the North; FLOODS in the East; WAR in the West. "
            "MONTHLY PATTERN: Chaitra/Baisakh — things costly. "
            "Jyeshtha/Aashadh — rains less. Shravan/Bhadrapad — rains more. "
            "Kartik — drought, essential goods costly. "
            "Margsheersh/Paush/Magh/Phalgun — goods costly; lives lost to riots."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Rahu years show a deceptive surface calm ('all people live happily') "
            "masking severe regional imbalances. "
            "The directional specification (North/East/West) is a unique Jyotish mapping tool "
            "linking Rahu's shadowy nature to geographical displacement effects. "
            "Year-end riot risk (Margsheersh-Phalgun) is significant."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AF-12: Ketu as Samvatsar lord
    _rule(
        rule_id         = "gaur-ch1-samvatsar-ketu-lord-plentiful-rains-loose-morals",
        sub_type        = "samvatsar",
        title           = "Ketu as Samvatsar Lord = Plentiful Rains, Abundant Grains, Loose Social Conduct",
        source_chapter  = "Gaur Ch 1, p. 7",
        condition       = (
            "The current Samvatsar has Ketu as its lord. "
            "Ketu-lord Samvatsars: #12 Bahudhanya, #32 Vilambi, #52 Kaal Yukta, #40 Parabhav."
        ),
        result          = (
            "Plentiful rains. Grains available abundantly. "
            "People have increased tendency of loose character and conduct. "
            "MONTHLY PATTERN: Chaitra/Baisakh/Jyeshtha — grains expensive (pre-monsoon scarcity). "
            "Aashadh/Shravan/Bhadrapad — sufficient rains, grains become cheap."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "Ketu years combine agricultural abundance with social/moral deterioration. "
            "The pre-monsoon period sees high prices that sharply reverse once rains arrive. "
            "Ketu as a moksha karaka produces both spiritual inclinations and social dissolution."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── Rule AF-13: Samvatsar group modifier (Brahma/Vishnu/Shiv)
    _rule(
        rule_id         = "gaur-ch1-samvatsar-group-quality-modifier",
        sub_type        = "samvatsar",
        title           = "Samvatsar Group (Brahma/Vishnu/Shiv) as Secondary Quality Modifier",
        source_chapter  = "Gaur Ch 1, p. 4",
        condition       = (
            "Any Samvatsar is active. Identify its group: "
            "Brahma-group: #1-20 (Prabhav to Vyaya); "
            "Vishnu-group: #21-40 (Sarvjat to Parabhav); "
            "Shiv-group: #41-60 (Plavang to Kshaya)."
        ),
        result          = (
            "The group ownership provides a background quality modifying the lord's results: "
            "BRAHMA GROUP (1-20): Generally auspicious undertone — creation and abundance energy. "
            "VISHNU GROUP (21-40): Preservation and order undertone — maintenance of status quo. "
            "SHIV GROUP (41-60): Dissolution and transformation undertone — endings and changes. "
            "The lord's specific effects are primary; the group is a secondary background modifier."
        ),
        synthesis_sources = ["Gaur Ch 1"],
        notes           = (
            "This tripartite division mirrors the Hindu cosmic trinity (Brahma/Vishnu/Shiva) "
            "mapping onto the 60-year Jupiter cycle. "
            "In practice: a Shiv-group year with a benefic lord (e.g., Mercury) will still show "
            "some dissolution/change undercurrent despite Mercury's harmony-producing effects."
        ),
        severity        = "low",
        checkable       = False,
    ),

    # ── Rule AF-14: Venus Samvatsar = specific earthquake rule (derived from lord description)
    _rule(
        rule_id         = "gaur-ch1-samvatsar-venus-year-earthquake-calamity-specific",
        sub_type        = "samvatsar",
        title           = "Venus Samvatsar Year = Earthquakes and Natural Calamities Are Specifically Indicated",
        source_chapter  = "Gaur Ch 1, p. 7",
        condition       = (
            "The current Samvatsar has Venus as its lord (Samvatsars: #9 Yuva, #18 Taran, "
            "#29 Manmath, #37 Shobhan, #49 Rakshas, #58 Raktaksha). "
            "This rule activates the FULL year, not just specific months."
        ),
        result          = (
            "During a Venus Samvatsar, earthquakes and other natural calamities cause agony. "
            "This is a year-level risk — not restricted to Chaitra/Baisakh alone. "
            "The Chaitra and Baisakh months specifically show natural calamity manifestation. "
            "Floods in Bhadrapad are also part of this pattern."
        ),
        synthesis_sources = [
            "Gaur Ch 1",
            "Raphael Ch 26 (earthquake rules)",
            "Gopalakrishnan Ch 13 (Venus in national chart effects)",
        ],
        notes           = (
            "This rule provides the ANNUAL-LEVEL earthquake signal from the Samvatsar cycle. "
            "It should be combined with Raphael Ch 26 earthquake rules (eclipse on meridian/nadir, "
            "malefics in Taurus/Scorpio, great conjunction on 4th cusp) for confirmation. "
            "When both a Venus Samvatsar AND Raphael earthquake conditions co-occur, "
            "earthquake risk for that year is elevated."
        ),
        severity        = "high",
        checkable       = True,
    ),

]

ALL_RULES = GROUP_AF

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_RULES)} interpretation rules from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        groups = {"GROUP_AF": GROUP_AF}
        for gname, grp in groups.items():
            print(f"  {gname} ({len(grp)} rules):")
            for r in grp:
                print(f"    {r['rule_id']}")
        print(
            f"\nTotal: {len(ALL_RULES)}\n"
            f"Source: Gaur Ch 1 (Samvatsar). Pages 21+ needed for Samvatsars 13-60 individual results,\n"
            f"Chapter 2 (Celestial Council), Chapter 3 (Special Horoscopes), etc.\n"
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
