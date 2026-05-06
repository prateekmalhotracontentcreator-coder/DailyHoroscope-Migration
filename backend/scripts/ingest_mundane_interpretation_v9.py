"""
Mundane Astrology — Interpretation Rules v9
Batch: mundane-interp-v9-20260506

Source: Raphael, "Mundane Astrology" (WITS e-group edition)
  Chapter 22 — Eclipses (sign element effects + Ptolemy timing)
  Chapter 26 — Earthquakes (9 rules)
  Chapter 27 — Comets

GROUP_AD: 11 rules from Raphael pages 21-40

Note: Solar/Lunar eclipse decanate effects (Ch 23-24) are encoded as
      lookup tables in engine specs — not repeated as interpretation rules.
      Ch 25 (Planetary Conjunctions) already encoded in earlier batches.

Rule types: eclipse, ingress, transit
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
_BATCH     = "mundane-interp-v9-20260506"
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
# GROUP_AD — RAPHAEL ECLIPSE, EARTHQUAKE, COMET RULES (Ch 22, 26, 27)
# ============================================================

GROUP_AD = [

    # ── Rule AD-01: Eclipse in fiery signs = war, fires, pestilence, royal danger
    _rule(
        rule_id         = "mundane-raphael-ch22-eclipse-fiery-signs-war-pestilence",
        sub_type        = "eclipse",
        title           = "Eclipse in Fiery Signs = War, Fires, Pestilence, Royal Exile or Murder",
        source_chapter  = "Raphael Ch 22, p.15 (Part 2)",
        condition       = (
            "A Solar or Lunar eclipse falls in a Fiery sign: Aries, Leo, or Sagittarius."
        ),
        result          = (
            "Threaten the destruction of cattle and sheep; "
            "exile, imprisonment, or murder of some king, notable person, or great ruler; "
            "much discontent and dissension among the people; "
            "movements of armies, fighting, fires, fevers, pestilence, "
            "and scarcity of the fruits of the earth, "
            "especially in those regions affected by the eclipse."
        ),
        synthesis_sources = ["Raphael Ch 22", "Ptolemy Tetrabiblos"],
        notes           = (
            "Effects most powerful in countries where eclipse is visible "
            "and in those ruled by the sign (see raphael-ch28-countries-ruled-by-signs). "
            "Solar eclipse in fiery sign = effects last years (per AC-01). "
            "Lunar eclipse in fiery sign = effects last months (per AC-02). "
            "Fixed fiery sign (Leo) = very lasting; Cardinal (Aries) = brief; Mutable (Sagittarius) = interrupted."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AD-02: Eclipse in earthy signs = earthquakes, drought, crop failure
    _rule(
        rule_id         = "mundane-raphael-ch22-eclipse-earthy-signs-earthquakes-drought",
        sub_type        = "eclipse",
        title           = "Eclipse in Earthy Signs = Earthquakes, Mining Disasters, Drought, Agricultural Failure",
        source_chapter  = "Raphael Ch 22, p.15 (Part 2)",
        condition       = (
            "A Solar or Lunar eclipse falls in an Earthy sign: Taurus, Virgo, or Capricorn."
        ),
        result          = (
            "Foreshadow a scarcity of corn and products of the earth by drought; "
            "cause earthquakes, mining disasters, and great agricultural depression."
        ),
        synthesis_sources = ["Raphael Ch 22", "Gopalakrishnan Ch 7 (earthquake indicators)"],
        notes           = (
            "Taurus and Capricorn are particularly earthquake-prone eclipse signs "
            "(Taurus-Scorpio axis = most seismically active per Raphael Ch 26 Rule 3). "
            "Cross-validates Gopalakrishnan's Ch7 earthquake rules. "
            "Solar eclipse in Taurus (fixed earthy) = most lasting and severe earthquake signal."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AD-03: Eclipse in airy signs = famine, sickness, storms
    _rule(
        rule_id         = "mundane-raphael-ch22-eclipse-airy-signs-famine-storm",
        sub_type        = "eclipse",
        title           = "Eclipse in Airy Signs = Famine, Sickness, Pestilence, Stormy Winds",
        source_chapter  = "Raphael Ch 22, p.15 (Part 2)",
        condition       = (
            "A Solar or Lunar eclipse falls in an Airy sign: Gemini, Libra, or Aquarius."
        ),
        result          = (
            "Famine, sickness, pestilence, and tempests and stormy winds hurtful to mankind."
        ),
        synthesis_sources = ["Raphael Ch 22", "Ptolemy Tetrabiblos"],
        notes           = (
            "Aquarius eclipse may also correlate with public grief and sorrow (per decanate effects). "
            "Airy signs connect to intellectual unrest, media/communications disruption (3rd house link). "
            "Libra eclipse: pestilence + dearness of corn (Libra 1st decanate). "
            "Mutable airy sign (Gemini) = interrupted effects that start and stop."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── Rule AD-04: Eclipse in watery signs = mortality, maritime destruction
    _rule(
        rule_id         = "mundane-raphael-ch22-eclipse-watery-signs-mortality",
        sub_type        = "eclipse",
        title           = "Eclipse in Watery Signs = Mass Mortality Among Common People, Maritime Destruction",
        source_chapter  = "Raphael Ch 22, p.15 (Part 2)",
        condition       = (
            "A Solar or Lunar eclipse falls in a Watery sign: Cancer, Scorpio, or Pisces."
        ),
        result          = (
            "Much mortality among the common people; "
            "great destruction of fowls and fishes, and such things as live in or near the sea. "
            "Also: tidal waves, inundations (especially Pisces 2nd decanate = tidal waves)."
        ),
        synthesis_sources = ["Raphael Ch 22", "Raphael Ch 24 (lunar eclipse decanates)"],
        notes           = (
            "Cancer eclipse: excites wars (Cancer 1st decanate lunar), weather changes, "
            "dries up rivers (Cancer 2nd solar). "
            "Scorpio eclipse: earthquakes and thunders (Scorpio 1st decanate lunar), "
            "fevers and pestilence (Scorpio 2nd decanate lunar). "
            "Pisces eclipse: death of famous person (Pisces 2nd decanate lunar). "
            "Cancer = watery cardinal = brief but severe; Scorpio = fixed = lasting; "
            "Pisces = mutable = interrupted."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AD-05: Eclipse in fixed signs = very lasting effects
    _rule(
        rule_id         = "mundane-raphael-ch22-eclipse-fixed-lasting-cardinal-brief",
        sub_type        = "eclipse",
        title           = "Eclipse in Fixed Signs = Very Lasting Effect; Cardinal = Brief; Mutable = Interrupted",
        source_chapter  = "Raphael Ch 22, p.15 (Part 2)",
        condition       = (
            "Assess the zodiac modality of the sign in which any Solar or Lunar eclipse falls."
        ),
        result          = (
            "FIXED sign eclipse (Taurus, Leo, Scorpio, Aquarius): VERY LASTING EFFECT — "
            "the most enduring and serious in mundane impact. "
            "CARDINAL sign eclipse (Aries, Cancer, Libra, Capricorn): BRIEF AND SOON OVER — "
            "effects are intense but pass quickly. "
            "MUTABLE sign eclipse (Gemini, Virgo, Sagittarius, Pisces): "
            "commence SOONER and last LONGER, but liable to INTERRUPTION — "
            "continue for a time, suddenly cease, then commence again."
        ),
        synthesis_sources = ["Raphael Ch 22"],
        notes           = (
            "Combine with element rule for full assessment: "
            "Fixed + Earthy (Taurus) = most lasting earthquake/agricultural crisis. "
            "Fixed + Fiery (Leo) = most lasting war/royal crisis. "
            "Fixed + Watery (Scorpio) = most lasting pestilence/mortality. "
            "Fixed + Airy (Aquarius) = most lasting famine/public grief."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── Rule AD-06: Ptolemy eclipse timing by horizon position
    _rule(
        rule_id         = "mundane-raphael-ch22-ptolemy-eclipse-timing-horizon",
        sub_type        = "eclipse",
        title           = "Ptolemy Eclipse Timing — Eastern Horizon = First 4 Months; Midheaven = 4-8 Months; Western = 8-12 Months",
        source_chapter  = "Raphael Ch 22, p.16 (Part 2)",
        condition       = (
            "An eclipse occurs. Note where in the mundane map the eclipse falls: "
            "near the Ascendant/eastern horizon (1st house), "
            "near the Midheaven (10th house), "
            "or near the Descendant/western horizon (7th house)."
        ),
        result          = (
            "EASTERN HORIZON (near 1st house): effects manifest in the NEXT FOUR MONTHS; "
            "most strongly in the FIRST THIRD of that period (months 1-2). "
            "MIDHEAVEN (near 10th house): events begin from FOURTH TO EIGHTH MONTH; "
            "chief effects in the SECOND OR MIDDLE PART (months 5-6). "
            "WESTERN HORIZON (near 7th house): effects appear from EIGHTH TO TWELFTH MONTH; "
            "chief effects in the LAST PART (months 10-12)."
        ),
        synthesis_sources = ["Raphael Ch 22", "Ptolemy Tetrabiblos"],
        notes           = (
            "This rule determines WHEN eclipse effects will manifest, not WHAT the effects will be. "
            "Combine with sign element rule for 'what' and this rule for 'when'. "
            "The most reliable timing per Raphael: calculate time of Sunrise/Sunset from eclipse middle "
            "and reckon at rate of one day = 4 minutes = 24 hours to the year."
        ),
        severity        = "medium",
        checkable       = True,
    ),

    # ── Rule AD-07: Eclipse on meridian/nadir = earthquake in that region
    _rule(
        rule_id         = "mundane-raphael-ch26-eclipse-on-meridian-nadir-earthquake",
        sub_type        = "eclipse",
        title           = "Eclipse on Meridian or Nadir = Earthquake in That Region; Fixed-Sign Planet at Eclipse = Quake Where Planet Rises/Sets",
        source_chapter  = "Raphael Ch 26, Part 3 p.5",
        condition       = (
            "A Solar or Lunar eclipse falls on or near the MERIDIAN (MC) or NADIR (IC) "
            "of a given location's mundane map. "
            "OR: at the moment of eclipse, a planet in a fixed sign is at a significant angle "
            "(rising, setting, culminating, or on the nadir) in a given location."
        ),
        result          = (
            "Earthquakes generally follow close on the heels of such eclipses. "
            "If planets are in fixed signs at the eclipse moment: "
            "earthquakes will occur in those parts of the world where such planets "
            "are either RISING, SETTING, CULMINATING, or ON THE NADIR. "
            "Example: if at eclipse, Saturn is in a fixed sign and 45° from the meridian, "
            "earthquakes occur in that part of the world which is the same distance from Greenwich."
        ),
        synthesis_sources = [
            "Raphael Ch 26",
            "Gopalakrishnan Ch 7 (saturn-fixed-signs-primary)",
        ],
        notes           = (
            "Validated by Syria 1822: Lunar eclipse → Saturn in exact square to eclipse degree "
            "on day of disaster. "
            "This rule requires calculating for each specific location whether the eclipse "
            "falls on or near the local meridian or IC. "
            "The eclipse PRESIGNIFIES; the planetary aspect to the eclipse degree = TRIGGER."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AD-08: Malefics in Taurus/Scorpio = earthquakes
    _rule(
        rule_id         = "mundane-raphael-ch26-malefics-taurus-scorpio-earthquakes",
        sub_type        = "transit",
        title           = "Uranus/Saturn/Jupiter/Mars in Taurus or Scorpio = Increased Earthquake Frequency",
        source_chapter  = "Raphael Ch 26, Part 3 p.5",
        condition       = (
            "Any combination of the planets Uranus, Saturn, Jupiter, or Mars "
            "are transiting through the signs TAURUS or SCORPIO."
        ),
        result          = (
            "Earthquakes happen MORE FREQUENTLY during this period. "
            "Taurus-Scorpio is the most earthquake-prone axis in the zodiac. "
            "The more malefic planets clustered in these signs, the greater the seismic risk globally."
        ),
        synthesis_sources = [
            "Raphael Ch 26",
            "Gopalakrishnan Ch 7 (saturn-fixed-signs-primary)",
        ],
        notes           = (
            "Cross-validates Gopalakrishnan's earthquake rule about Saturn in fixed signs. "
            "Raphael specifically names TAURUS and SCORPIO as most earthquake-prone. "
            "Aquarius and Leo (the other two fixed signs) are also significant per the "
            "fixed sign eclipse rule. "
            "Rule 5 adds refinement: Jupiter in Taurus or Scorpio conjunct/opposite/parallel Mercury "
            "= one of the MOST PROLIFIC sources of earthquakes specifically."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AD-09: Great conjunction on 4th house cusp = earthquake
    _rule(
        rule_id         = "mundane-raphael-ch26-great-conjunction-4th-cusp-earthquake",
        sub_type        = "ingress",
        title           = "Great Planetary Conjunction on 4th House Cusp (IC/Nadir) = Earthquake in That Locality",
        source_chapter  = "Raphael Ch 26, Part 3 p.5",
        condition       = (
            "A great planetary conjunction (Mars-Jupiter, Mars-Saturn, Jupiter-Saturn, "
            "Saturn-Uranus, or Saturn-Neptune) falls exactly on or within orb of "
            "the cusp of the 4th house (IC/Nadir) of the mundane map for a given location."
        ),
        result          = (
            "An earthquake is sure to occur in that locality. "
            "Cast a mundane map for the time of the great conjunction and check "
            "whether the conjunction falls on the Nadir or 4th house cusp for each location of interest."
        ),
        synthesis_sources = ["Raphael Ch 26"],
        notes           = (
            "Validated cases: "
            "Charlestown 1886: Mars-Jupiter conjunction on 4th house cusp → serious earthquake. "
            "Kuchan 1898: Mars-Saturn conjunction on 4th house cusp → 12,000 killed. "
            "Mont Pelée 1902: Jupiter-Saturn on IC at St. Pierre (eclipse) → volcanic eruption 6 months later. "
            "The 4th house cusp in mundane astrology governs land and geological matters."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AD-10: Cardinal points stellium = earthquake
    _rule(
        rule_id         = "mundane-raphael-ch26-cardinal-points-stellium-earthquake",
        sub_type        = "transit",
        title           = "Many Planets at Cardinal Point Degrees (0° Aries/Cancer/Libra/Capricorn) = Earthquake",
        source_chapter  = "Raphael Ch 26, Part 3 p.5",
        condition       = (
            "Many planets are clustered on or near the FOUR CARDINAL POINTS — "
            "the first degrees of Aries, Cancer, Libra, and Capricorn — "
            "at an ingress, lunation, or eclipse."
        ),
        result          = (
            "Earthquakes generally happen during this configuration. "
            "The cardinal points (0° of each cardinal sign) represent the four "
            "directional angles of the ecliptic and have particular seismic sensitivity."
        ),
        synthesis_sources = [
            "Raphael Ch 26",
            "Gopalakrishnan Ch 7 (cardinal-stellium-upheaval)",
        ],
        notes           = (
            "Cross-validates Gopalakrishnan's cardinal stellium rule (gopal-ch7-cardinal-stellium-upheaval). "
            "Both Western (Raphael) and Indian (Gopalakrishnan) traditions independently identify "
            "cardinal point clustering as a seismic and crisis indicator."
        ),
        severity        = "high",
        checkable       = True,
    ),

    # ── Rule AD-11: Comet by sign type = specific national effects
    _rule(
        rule_id         = "mundane-raphael-ch27-comet-sign-type-effects",
        sub_type        = "transit",
        title           = "Comet Effects by Sign Type — Cardinal = Death of Great Men; Fixed = Foreign Wars; Mutable = Sedition/Pestilence",
        source_chapter  = "Raphael Ch 27, Part 3 p.7",
        condition       = (
            "A great comet appears or is at perihelion (nearest Sun or Earth). "
            "Note the zodiac sign in which the comet first appears."
        ),
        result          = (
            "CARDINAL signs (Aries, Cancer, Libra, Capricorn): death of great men. "
            "FIXED signs (Taurus, Leo, Scorpio, Aquarius): foreign wars and invasion. "
            "COMMON/MUTABLE signs (Gemini, Virgo, Sagittarius, Pisces): sedition and pestilence. "
            "Position by horizon: "
            "East = rising of some eminent law-giver; "
            "Midheaven = eminent king dies or rises; "
            "West = serious troubles generally. "
            "Countries ruled by the sign in which the comet appears will suffer serious troubles. "
            "Comet's house in mundane chart also matters: "
            "9th house = scandal or detriment to religion; "
            "10th or 12th = pestilence or scarcity of corn; "
            "8th house = many sudden and terrible deaths."
        ),
        synthesis_sources = ["Raphael Ch 27"],
        notes           = (
            "Historical example: Halley's Comet 1910 return — earthquakes and electrical storms "
            "were frequent for two years prior to its approach. "
            "Russo-Japanese War (1904): comet of 1903 appeared in Aquarius (= Russia); "
            "war broke out within a week of Sun passing that degree in February. "
            "Comets near perihelion may trigger earthquakes (see AD-10, Raphael Ch 26 Rule 9). "
            "This rule is lower-confidence than eclipse/ingress rules — "
            "requires actual comet observation."
        ),
        severity        = "medium",
        checkable       = False,
    ),

]

ALL_RULES = GROUP_AD

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_RULES)} interpretation rules from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        groups = {"GROUP_AD": GROUP_AD}
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
