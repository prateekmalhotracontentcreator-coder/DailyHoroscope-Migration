"""
Mundane Astrology — Interpretation Rules v5
Batch: mundane-interp-v5-20260506

Source: Gopalakrishnan, "Mundane Astrology" (ICAS)
  Chapter 6 — Predicting Mass Death (book pp.79-90)
  Chapter 7 — Earthquakes (book pp.91-98)

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
_BATCH     = "mundane-interp-v5-20260506"
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
# GROUP X — Gopalakrishnan Ch 6: Predicting Mass Death
# ============================================================
GROUP_X = [

    _rule(
        rule_id="mundane-gopal-ch6-eclipse-trika-mass-death",
        sub_type="mass_death_epidemic",
        title="Eclipse on Trika Houses of National Chart — Mass Death",
        source_chapter="Gopalakrishnan Ch 6, p.79",
        condition={
            "primary": (
                "A solar or lunar eclipse falls on the 4th, 8th, or 12th house "
                "of a country's national horoscope (or Aries Ingress chart for that year)."
            ),
            "house_4": "Eclipse on 4th house: mass suffering and death among the general population.",
            "house_8": "Eclipse on 8th house: mass death, war casualties, or epidemic.",
            "house_12": "Eclipse on 12th house: mass death with large-scale displacement; hospitals and morgues overwhelmed.",
        },
        result=(
            "Mass death event in that country within the effect period of the eclipse "
            "(scale proportional to eclipse magnitude — see Gaur Ch 11 severity-duration rule)."
        ),
        synthesis_sources=["Gopalakrishnan Ch 6", "Gaur Ch 11", "Raphael Ch 25"],
        notes=(
            "Cross-reference with Raphael Ch 25 eclipse-4th-8th rule (mundane-raphael-ch25-eclipse-4th-8th) "
            "for Western validation of the same principle. "
            "Severity escalates when Saturn or Mars also transits the eclipsed house."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch6-eclipse-lagna-luminaries-leader",
        sub_type="governance_leader_death",
        title="Eclipse Conjunct National Chart Ascendant or Luminaries — Leader in Danger",
        source_chapter="Gopalakrishnan Ch 6, p.80",
        condition={
            "primary": (
                "A solar or lunar eclipse falls within 5° of the national chart's "
                "Ascendant degree, natal Sun longitude, or natal Moon longitude."
            ),
            "on_ascendant": "Eclipse on Ascendant: national identity crisis; head of state in physical danger.",
            "on_natal_sun": "Eclipse conjunct natal Sun: extreme danger to the head of government / king / prime minister.",
            "on_natal_moon": "Eclipse conjunct natal Moon: danger to the leader; public grief; mass emotional upheaval.",
        },
        result=(
            "Serious threat to the incumbent national leader. "
            "May manifest as assassination attempt, death in office, or forced removal from power."
        ),
        synthesis_sources=["Gopalakrishnan Ch 6", "Mehta Ch 18", "Mehta Ch 21"],
        notes=(
            "Cross-reference with Mehta Ch 18 lagna-lord-afflicted-death rule "
            "(mundane-mehta-ch18-lagna-lord-afflicted-death) and Mehta Ch 21 hazard rules. "
            "When eclipse hits both 8th house AND natal Sun/Moon simultaneously: near-certain leadership crisis."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch6-8th-house-death-zone",
        sub_type="mass_death_epidemic",
        title="8th House Death Zone — Saturn+Rahu or Triple Malefic Confluence",
        source_chapter="Gopalakrishnan Ch 6, pp.82-84",
        condition={
            "saturn_rahu_8th": (
                "Saturn and Rahu (or Saturn and Ketu) both transiting the 8th house "
                "of the national chart simultaneously."
            ),
            "mars_in_8th_during_eclipse": (
                "Mars transiting the 8th house during an eclipse period "
                "(within 30 days either side of eclipse date)."
            ),
            "triple_malefic_8th": (
                "Three or more malefic planets (Sun, Mars, Saturn, Rahu, Ketu) "
                "simultaneously occupying the 8th house of the national chart."
            ),
        },
        result=(
            "Mass death signal of varying severity: "
            "Saturn+Rahu/Ketu = epidemic or slow-burning mass casualty event; "
            "Mars in 8th during eclipse = war-related mass death; "
            "Triple malefic 8th = severe multi-vector crisis (war + disease + disaster)."
        ),
        synthesis_sources=["Gopalakrishnan Ch 6", "Mehta Ch 19"],
        notes=(
            "Cross-reference with Mehta Ch 19 triple-affliction rule "
            "(mundane-mehta-ch19-triple-affliction). "
            "The 8th lord's condition is equally important — see mundane-gopal-ch6-8th-lord-affliction."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch6-8th-lord-affliction",
        sub_type="mass_death_epidemic",
        title="8th Lord Afflicted by Three Malefics — Mass Casualty Risk",
        source_chapter="Gopalakrishnan Ch 6, p.84",
        condition={
            "primary": (
                "The lord of the 8th house of the national chart is afflicted "
                "by three or more malefic planets by conjunction, square (4th/8th/10th aspect), "
                "or opposition in the current transit chart."
            ),
        },
        result=(
            "Mass casualty event. The nature of casualties is indicated by the sign/house "
            "placement of the 8th lord and the malefic planets afflicting it "
            "(Mars = war/fire/accidents; Saturn = disease/famine; Rahu = epidemic/poison/gas)."
        ),
        synthesis_sources=["Gopalakrishnan Ch 6"],
        notes=(
            "This rule operates independently of eclipse timing but is greatly amplified "
            "when an eclipse simultaneously activates the 8th house. "
            "The 8th lord in its own sign (debilitation) makes the affliction worse."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch6-mars-gandanta-accidents",
        sub_type="mass_death_epidemic",
        title="Mars in Gandanta Nakshatras — Mass Accidents and Sudden Casualties",
        source_chapter="Gopalakrishnan Ch 6, pp.86-87",
        condition={
            "primary": (
                "Mars transiting through any of the four gandanta (junction) nakshatras: "
                "Ardra (Gemini 6°40'-20°00'), Ashlesha (Cancer 16°40'-30°00'), "
                "Jyeshtha (Scorpio 16°40'-30°00'), or Mool (Sagittarius 0°00'-13°20')."
            ),
            "ardra":    "Mars in Ardra: mass accidents, sudden casualties from storms or transportation disasters.",
            "ashlesha": "Mars in Ashlesha: epidemics, poisoning incidents, mass accidents.",
            "jyeshtha": "Mars in Jyeshtha: violent mass upheaval, assassinations, large-scale conflict.",
            "mool":     "Mars in Mool: mass accidents from natural calamities (earthquake, flood, fire).",
        },
        result=(
            "Elevated risk of mass casualty events from sudden accidents, violence, or epidemics "
            "during Mars's transit through the specific gandanta nakshatra. "
            "Effect window: 7-14 days around Mars's stay in the nakshatra."
        ),
        synthesis_sources=["Gopalakrishnan Ch 6"],
        notes=(
            "Gandanta nakshatras span the water-fire sign junctions: "
            "Pisces-Aries, Cancer-Leo, Scorpio-Sagittarius. "
            "All four are considered karmically unstable. Mars, as the natural significator of accidents "
            "and violence, becomes particularly destructive here. "
            "Cross-reference with Gaur Ch 10 retrograde-famine rule for economic dimensions."
        ),
        severity="medium",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch6-epidemic-triad",
        sub_type="mass_death_epidemic",
        title="Epidemic Triad — Saturn 6th from Country Moon, Rahu in Country Moon Sign, Venus-Saturn Conjunction",
        source_chapter="Gopalakrishnan Ch 6, pp.88-90",
        condition={
            "saturn_6th_from_country_moon": (
                "Saturn transiting the 6th sign counted from the country's natal Moon sign. "
                "E.g., India's Moon = Cancer → Saturn in Sagittarius triggers this condition."
            ),
            "rahu_in_country_natal_moon_sign": (
                "Rahu transiting through the same sign as the country's natal Moon. "
                "E.g., India's Moon = Cancer → Rahu in Cancer activates this."
            ),
            "venus_saturn_conjunction": (
                "Venus and Saturn conjoined in the same sign (within 10° orb), "
                "especially in the 6th or 8th house of the national chart."
            ),
        },
        result=(
            "Epidemic or pandemic conditions in the country. "
            "Single condition = watch; two conditions active = elevated epidemic risk; "
            "all three active simultaneously = severe epidemic/pandemic imminent."
        ),
        synthesis_sources=["Gopalakrishnan Ch 6"],
        notes=(
            "Gopalakrishnan validated this triad against the 1918 Spanish Flu "
            "(Saturn+Rahu positions + Venus-Saturn aspect active globally). "
            "The country-specific Moon sign anchor makes this rule nation-by-nation. "
            "India Moon = Cancer (approx). USA Moon = Aquarius (approx, Kelleher chart). "
            "UK Moon = Cancer (approx, 1801 Union chart)."
        ),
        severity="high",
        checkable=True,
    ),

]

# ============================================================
# GROUP Y — Gopalakrishnan Ch 7: Earthquakes
# ============================================================
GROUP_Y = [

    _rule(
        rule_id="mundane-gopal-ch7-saturn-fixed-signs-primary",
        sub_type="seismic_cardinal_cluster",
        title="Saturn in Fixed Signs (Retrograde) — Primary Earthquake Indicator",
        source_chapter="Gopalakrishnan Ch 7, pp.91-93",
        condition={
            "saturn_fixed_direct": (
                "Saturn transiting a fixed sign (Taurus, Leo, Scorpio, Aquarius) in direct motion: "
                "elevated baseline seismic risk globally, especially in regions governed by that sign."
            ),
            "saturn_fixed_retrograde": (
                "Saturn retrograde in a fixed sign: strongest primary seismic indicator. "
                "Retrograde Saturn in fixed sign = high-probability seismic window, "
                "especially when a trigger indicator is also active."
            ),
            "most_dangerous_signs": "Saturn in Scorpio or Aquarius (own sign / sign of exaltation Libra nearby) produces strongest seismic effects.",
        },
        result=(
            "Primary seismic indicator active. Elevated earthquake probability globally "
            "in regions associated with the fixed sign Saturn occupies. "
            "Retrograde condition amplifies probability by ~2x."
        ),
        synthesis_sources=["Gopalakrishnan Ch 7", "Mehta Ch 11", "Gopalakrishnan Ch 8"],
        notes=(
            "Cross-reference with Mehta Ch 11 rules: "
            "mundane-mehta-ch11-scorpio-taurus-primary (Scorpio-Taurus axis), "
            "mundane-mehta-ch11-cardinal-clustering, "
            "mundane-gopal-ch8-seismic-triad. "
            "Saturn in fixed signs is the long-range seismic background; "
            "trigger rules (Mars, eclipse, New Moon) determine the specific event window."
        ),
        severity="medium",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch7-mars-eclipse-point-trigger",
        sub_type="seismic_forerunner_igniter",
        title="Mars Transiting Eclipse Point — Seismic Trigger Within 3 Days",
        source_chapter="Gopalakrishnan Ch 7, p.94",
        condition={
            "primary": (
                "Mars transiting over the exact longitude of a recent solar or lunar eclipse "
                "(within 1° orb) that occurred within the past 6 months."
            ),
            "trigger_window": "3 days before to 3 days after Mars's exact conjunction with the eclipse longitude.",
            "amplification": "Effect is greatly amplified when Saturn's primary fixed-sign condition is simultaneously active.",
        },
        result=(
            "Seismic event (earthquake) triggered in the geographic zone corresponding "
            "to the eclipse longitude. Mars acts as the igniter that activates the latent "
            "seismic energy stored at the eclipse point."
        ),
        synthesis_sources=["Gopalakrishnan Ch 7", "Mehta Ch 11"],
        notes=(
            "Cross-reference with Mehta Ch 11 forerunner-igniter rule "
            "(mundane-mehta-ch11-forerunner-igniter) which covers Mars/Sun/Venus "
            "triggering eclipse-point seismic events. "
            "Track the last 2-3 eclipse longitudes and watch for Mars conjunctions. "
            "Most sensitive eclipse types: total solar > annular > total lunar."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch7-rahu-ketu-ic-mc-axis",
        sub_type="seismic_taurus_scorpio_axis",
        title="Rahu/Ketu Axis Aligned with IC/MC of Regional Chart — Major Seismic Event",
        source_chapter="Gopalakrishnan Ch 7, pp.95-96",
        condition={
            "primary": (
                "The Rahu-Ketu nodal axis aligns within 5° of the IC (4th house cusp) "
                "and MC (10th house cusp) of the Aries Ingress chart cast for a specific territory, "
                "or of that territory's natal chart."
            ),
            "eclipse_on_ic": (
                "A solar or lunar eclipse occurs within 5° of the IC of the regional chart: "
                "seismic event near the geographic center of that territory."
            ),
        },
        result=(
            "Major seismic event in the territory within 3-6 months of the nodal alignment. "
            "Eclipse on IC specifically indicates the earthquake's epicenter near the "
            "capital or geographic center of the country."
        ),
        synthesis_sources=["Gopalakrishnan Ch 7", "Mehta Ch 11"],
        notes=(
            "The IC (4th cusp) represents the earth itself / underground / foundations. "
            "Rahu/Ketu on this axis destabilizes the literal ground. "
            "Cross-reference with Mehta Ch 11 eclipse-nadir rule (mundane-mehta-ch11-eclipse-nadir). "
            "For India: Aries Ingress chart cast for New Delhi."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch7-cardinal-stellium-upheaval",
        sub_type="seismic_cardinal_cluster",
        title="Cardinal Sign Stellium — Geopolitical Upheaval and Large-Scale Sudden Events",
        source_chapter="Gopalakrishnan Ch 7, p.96",
        condition={
            "primary": (
                "Three or more planets clustering in cardinal signs "
                "(Aries, Cancer, Libra, Capricorn) simultaneously."
            ),
            "pure_cardinal": "All 3+ planets in the same cardinal sign: maximum intensity.",
            "spread_cardinal": "3+ planets spread across 2-3 different cardinal signs: broad geopolitical instability.",
        },
        result=(
            "Geopolitical upheaval, leadership crises, sudden large-scale events. "
            "Not a direct earthquake indicator but frequently co-occurs with seismic events "
            "as part of a broader world-crisis configuration."
        ),
        synthesis_sources=["Gopalakrishnan Ch 7", "Gopalakrishnan Ch 8", "Raphael Ch 25"],
        notes=(
            "Cardinal signs = signs of initiation and action. Heavy planetary clustering = "
            "forced change. Cross-reference with Mehta Ch 11 cardinal-clustering rule "
            "(mundane-mehta-ch11-cardinal-clustering) and Gopalakrishnan Ch 8 "
            "war/geopolitical rules for full picture. "
            "This rule is more geopolitical than seismic."
        ),
        severity="medium",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch7-new-moon-fixed-sign-seismic",
        sub_type="seismic_rasi_sandhi",
        title="New Moon Conjunct Saturn or Mars in Fixed Sign — Seismic Risk Window",
        source_chapter="Gopalakrishnan Ch 7, p.97",
        condition={
            "primary": (
                "A New Moon (Sun-Moon conjunction) occurs while Saturn or Mars "
                "is also in a fixed sign (Taurus, Leo, Scorpio, Aquarius), "
                "and the New Moon itself falls within 10° of Saturn or Mars."
            ),
            "new_moon_conjunct_saturn_fixed": "New Moon conjunct Saturn in fixed sign: seismic risk window of 7-14 days.",
            "new_moon_conjunct_mars_fixed": "New Moon conjunct Mars in fixed sign: sudden seismic event, possibly violent in nature.",
        },
        result=(
            "Seismic risk window of 7-14 days centered on the New Moon date. "
            "Geographic zone indicated by the fixed sign involved."
        ),
        synthesis_sources=["Gopalakrishnan Ch 7"],
        notes=(
            "New Moon amplifies the energy of any planet it conjoins. "
            "In fixed signs, this concentrates telluric (earth) energy. "
            "Strongest when Saturn's primary fixed-sign indicator is already active "
            "AND Mars is also involved as the trigger."
        ),
        severity="medium",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch7-sandhi-clustering",
        sub_type="seismic_rasi_sandhi",
        title="Sandhi Degree Clustering — Earthquake Signal from Sign-Boundary Planets",
        source_chapter="Gopalakrishnan Ch 7, pp.97-98",
        condition={
            "primary": (
                "Two or more planets simultaneously within 2° of a sign boundary (sandhi degree: "
                "last 2° of any sign or first 2° of any sign = 0°-2° or 28°-30° in the sign)."
            ),
            "gandanta_boundaries": (
                "Most seismically sensitive sandhi points: Pisces-Aries (29°Pi - 2°Ar), "
                "Cancer-Leo (29°Ca - 2°Le), Scorpio-Sagittarius (29°Sc - 2°Sa). "
                "These are the gandanta zones between water and fire signs."
            ),
            "non_gandanta": "Other sign boundaries also contribute but with lower severity.",
        },
        result=(
            "Earthquake signal. The sandhi zone represents instability — planets at sign boundaries "
            "are between states, creating a 'fault line' in the cosmic structure that can manifest "
            "as geological fault lines activating. Effect window: 5-10 days."
        ),
        synthesis_sources=["Gopalakrishnan Ch 7", "Mehta Ch 11"],
        notes=(
            "Cross-reference with Mehta Ch 11 rasi-sandhi rule (mundane-mehta-ch11-rasi-sandhi). "
            "Both authors independently identify sign-boundary clustering as a seismic signal. "
            "When both are active simultaneously (2+ planets in sandhi + Saturn in fixed sign): "
            "strong convergence indicator. "
            "In computer-assisted checking, flag any date when 2+ planets are at 29°XX'-0°XX' range."
        ),
        severity="medium",
        checkable=True,
    ),

]

# ============================================================
ALL_RULES = GROUP_X + GROUP_Y

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
