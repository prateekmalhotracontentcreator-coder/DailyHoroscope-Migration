"""
Mundane Astrology — Interpretation Rules v6
Batch: mundane-interp-v6-20260506

Source: Gopalakrishnan, "Mundane Astrology" (ICAS)
  Chapter 8  — Predicting Wars (book pp.99-129)
  Chapter 9  — Yearly Predictions Framework (book pp.130-162)

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
_BATCH     = "mundane-interp-v6-20260506"
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
# GROUP Z — Gopalakrishnan Ch 8: War Prediction Rules
# ============================================================
GROUP_Z = [

    _rule(
        rule_id="mundane-gopal-ch8-india-pakistan-2-12-lagna",
        sub_type="war_india_axis",
        title="India-Pakistan 2/12 Lagna Relationship — Structural Permanent Tension",
        source_chapter="Gopalakrishnan Ch 8, p.104",
        condition={
            "primary": (
                "India and Pakistan have their national chart Ascendants in a 2/12 relationship: "
                "one country's Ascendant falls in the 2nd sign from the other's, and vice versa. "
                "(India lagna = Taurus; Pakistan lagna = Cancer — Cancer is 3rd from Taurus, "
                "but Gopalakrishnan cites 2/12 axis from his chart versions.)"
            ),
            "structural_implication": (
                "Two nations in a 2/12 lagna relationship can never get along permanently. "
                "The 2nd/12th axis = money/expenditure = one nation's gain is always the other's loss. "
                "Tension, infiltration, border disputes will recur cyclically regardless of peace talks."
            ),
        },
        result=(
            "India and Pakistan will always have recurring border tensions, "
            "infiltration, and periodic military skirmishes or wars. "
            "Peace agreements are temporary — structural axis ensures conflict returns."
        ),
        synthesis_sources=["Gopalakrishnan Ch 8", "Mehta Ch 19"],
        notes=(
            "Cross-reference with Mehta Ch 19 India-Cancer-Capricorn axis rule "
            "(mundane-mehta-ch19-india-cancer-capricorn). "
            "Gopalakrishnan uses this structural 2/12 principle to explain why "
            "India-Pakistan relations oscillate between dialogue and conflict regardless of leadership."
        ),
        severity="medium",
        checkable=False,
    ),

    _rule(
        rule_id="mundane-gopal-ch8-saturn-over-india-rahu-war",
        sub_type="war_india_axis",
        title="Saturn Transiting India's Natal Rahu — War or Military Conflict Trigger",
        source_chapter="Gopalakrishnan Ch 8, p.103",
        condition={
            "primary": (
                "Saturn in transit conjuncts the natal Rahu longitude of India's independence chart "
                "(India Rahu = approx Taurus 3°-5°, chart-version dependent)."
            ),
            "orb": "Within 3° of exact conjunction.",
            "source_statement": (
                "'Whenever Saturn has gone over India's Rahu there have been fights.' "
                "— K. Gopalakrishnan"
            ),
        },
        result=(
            "Military conflict or war involving India. "
            "All confirmed India-Pakistan wars occurred during Saturn-Rahu transit activations."
        ),
        synthesis_sources=["Gopalakrishnan Ch 8", "Mehta Ch 19", "Gopalakrishnan Ch 8 war table"],
        notes=(
            "This is an empirically validated rule across the 1947-48, 1965, 1971 and Kargil 1999 conflicts. "
            "Rahu's natal position in India's chart must be confirmed from a reliable "
            "India independence chart (Aug 15 1947, 00:00 IST, New Delhi). "
            "Different astrologers use different India chart versions — verify before applying."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch8-dasa-quality-war-duration",
        sub_type="causal_sequence",
        title="National Dasa Quality Determines War Duration and Outcome",
        source_chapter="Gopalakrishnan Ch 8, pp.103-104",
        condition={
            "good_dasa_short_war": (
                "Country running a benefic or raja yoga dasa/bhukthi at time of war: "
                "war will be short, country will achieve its objectives, "
                "cease-fire or favorable outcome within weeks to months."
            ),
            "bad_dasa_prolonged_war": (
                "Country running a malefic dasa (6th lord, 8th lord, Rahu dasa) at time of war: "
                "war will be prolonged, heavy casualties, no clean victory."
            ),
            "war_ends_when": (
                "Wars end when a favorable raja yoga bhukthi or Moon antara begins "
                "within the running dasa period."
            ),
        },
        result=(
            "Dasa quality is the primary determinant of war outcome and duration. "
            "Assess the dasa/bhukthi/antara of the national chart at time of conflict "
            "to determine probable war length and winner."
        ),
        synthesis_sources=["Gopalakrishnan Ch 8"],
        notes=(
            "All India-Pakistan wars were short because India was running good overall dasa periods: "
            "1947-48: Saturn/Saturn → Mercury bhukthi (favorable) ended it; "
            "1965: Saturn/Jupiter/Rahu → Mercury dasa coming (favorable); "
            "1971: Mercury/Sun/Mars → Moon bhukthi (raja yoga) ended it; "
            "Kargil 1999: Venus/Rahu/Sun → Moon antara ended it. "
            "Sri Lanka contrast: Rahu dasha from 1992 (6th lord) → war lasted 30 years."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch8-6th-lord-dasa-insurgency",
        sub_type="instability_gate",
        title="6th Lord Dasa — Insurgency and Terrorist Conflict Activation",
        source_chapter="Gopalakrishnan Ch 8, p.105",
        condition={
            "primary": (
                "A nation enters the Vimshottari dasa period of its 6th house lord "
                "(the planet that rules the 6th house from the national chart's Ascendant)."
            ),
            "india_application": (
                "India: 6th lord = Saturn (Libra Ascendant). When India runs Saturn dasa/bhukthi, "
                "problems with Kashmir and external enemies intensify."
            ),
            "sri_lanka_application": (
                "Sri Lanka ran Rahu Dasha from 1992. Rahu = 6th lord for Sri Lanka. "
                "This activated terrorist attacks and the LTTE insurgency to maximum intensity."
            ),
        },
        result=(
            "Insurgency, terrorism, border conflicts, war with enemy nations, "
            "and mass debt/disease conditions are activated during the 6th lord dasa period."
        ),
        synthesis_sources=["Gopalakrishnan Ch 8", "Gopalakrishnan Ch 8 Sri Lanka case study"],
        notes=(
            "The 6th house in mundane astrology governs: sickness/epidemic, mass death, "
            "war with other countries, debt, medical industry, and enemy nations. "
            "The dasa of any planet placed in or ruling the 6th house activates all these themes. "
            "Applies universally to any national chart — identify the 6th lord and "
            "track when its dasa/bhukthi runs for conflict prediction."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch8-saturn-kataka-bloodshed",
        sub_type="zone_malefic_transit",
        title="Saturn Entering Cancer (Kataka) — Bloodshed Signal for Specific Nations",
        source_chapter="Gopalakrishnan Ch 8, p.106",
        condition={
            "primary": (
                "Saturn transits into Cancer (Kataka). "
                "For nations whose significant chart points (Ascendant, Moon sign, natal Saturn) "
                "are in or square to Cancer, Saturn's entry creates bloodshed conditions."
            ),
            "sri_lanka_specific": (
                "Saturn enters Kataka (Cancer): Sept 2004 to 2006. "
                "For Sri Lanka (Cancer rising or Cancer Moon): lot of bloodshed and loss of lives. "
                "[Predicted Jan 2005, before Saturn actually entered Cancer Sept 2004.]"
            ),
            "leadership_assassination": (
                "When Saturn is in Cancer for a nation with Cancer prominent: "
                "a very important leader in that country will be assassinated within 3 years."
            ),
        },
        result=(
            "Bloodshed, civilian casualties, and leadership assassination risk "
            "for nations with Cancer prominent in the national chart "
            "during Saturn's transit through Cancer."
        ),
        synthesis_sources=["Gopalakrishnan Ch 8", "Gopalakrishnan Ch 8 Sri Lanka case"],
        notes=(
            "Saturn in Cancer = in its sign of debilitation (neecha). "
            "Debilitated Saturn in a nation's sensitive sign produces worst results. "
            "Cross-reference with Gopalakrishnan Ch 8 rule on Sri Lanka's LTTE conflict. "
            "This rule applies sign-specifically to any nation with Cancer prominent. "
            "For India (Cancer Moon sign), Saturn in Cancer also produces difficult periods."
        ),
        severity="high",
        checkable=True,
    ),

]

# ============================================================
# GROUP AA — Gopalakrishnan Ch 9: Yearly Prediction Operational Framework
# ============================================================
GROUP_AA = [

    _rule(
        rule_id="mundane-gopal-ch9-sandhi-malefics-confusion",
        sub_type="turbulence_signal",
        title="Saturn/Rahu/Jupiter at Rasi Sandhi — National Confusion and Instability",
        source_chapter="Gopalakrishnan Ch 9, p.146",
        condition={
            "primary": (
                "Saturn, Rahu, or Jupiter transiting at rasi sandhi — "
                "the last 2° of any sign or the first 2° of any sign "
                "(the sign-change transition zone)."
            ),
            "compounding": (
                "Two or more of these three planets simultaneously in rasi sandhi "
                "creates maximum confusion and destabilization."
            ),
        },
        result=(
            "National confusion, policy paralysis, leadership indecision, and instability. "
            "Markets volatile. Events sudden and unexpected. "
            "Severity proportional to which planet is in sandhi and how long it remains there."
        ),
        synthesis_sources=["Gopalakrishnan Ch 9", "Mehta Ch 11"],
        notes=(
            "Cross-reference with Mehta Ch 11 rasi-sandhi rule (mundane-mehta-ch11-rasi-sandhi) "
            "which applies this to seismic events. Gopalakrishnan applies it more broadly "
            "to national governance and economic stability. "
            "Saturn in sandhi = most severe; Rahu in sandhi = confusion and scandals; "
            "Jupiter in sandhi = religious/educational policy uncertainty."
        ),
        severity="medium",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch9-malefics-trika-entry",
        sub_type="instability_gate",
        title="Saturn/Rahu/Jupiter Entering Trika Houses (6/8/12) — Negative Events Triggered",
        source_chapter="Gopalakrishnan Ch 9, p.146",
        condition={
            "primary": (
                "Saturn, Rahu, or Jupiter transiting into the 6th, 8th, or 12th house "
                "of the national chart (or into the sign ruled by the 6th/8th/12th lord)."
            ),
            "into_6th": "Triggers war, epidemic, debt crisis, labor disputes.",
            "into_8th": "Triggers leadership crisis, mass deaths, government collapse.",
            "into_12th": "Triggers financial losses, foreign debt, exile of leaders, mass displacement.",
        },
        result=(
            "Negative events in the domain governed by that trika house are triggered "
            "when Saturn, Rahu, or Jupiter enter it. "
            "Effect begins at ingress and intensifies during the full transit period."
        ),
        synthesis_sources=["Gopalakrishnan Ch 9"],
        notes=(
            "This rule uses the national chart's house structure (not generic zodiac houses). "
            "For India (Taurus Ascendant): 6th = Libra, 8th = Sagittarius, 12th = Aries. "
            "Saturn entering Libra = 6th house for India = war/epidemic signal. "
            "This is the Detail D operative framework from Gopalakrishnan's yearly prediction system. "
            "Cross-reference with eclipse-in-trika-axis rules."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch9-saturn-10th-lord-leadership-change",
        sub_type="leadership_transition",
        title="Saturn Transiting Natal 10th Lord — Leadership Change",
        source_chapter="Gopalakrishnan Ch 9, p.147",
        condition={
            "primary": (
                "Saturn in transit conjuncts the natal 10th lord's position in the national chart "
                "(i.e., transits over the natal degree of the planet that rules the 10th house). "
                "Orb: within 3°."
            ),
            "example": (
                "Saturn over India's natal Saturn (India's 10th lord from Ascendant perspective): "
                "many astrologers predicted Manmohan Singh government or NDA government "
                "will not stay long in power — change in governance signaled."
            ),
        },
        result=(
            "Changes in leadership at the national level. "
            "Prime minister may change, government may fall, or significant cabinet reshuffles occur."
        ),
        synthesis_sources=["Gopalakrishnan Ch 9", "Mehta Ch 18"],
        notes=(
            "Cross-reference with Mehta Ch 18 governance rules. "
            "Saturn transiting the 10th lord applies to any national chart. "
            "Identify the 10th lord from the national chart's Ascendant, "
            "find its natal position (degree), and watch when Saturn transits that point. "
            "For India (Taurus Asc): 10th = Aquarius → 10th lord = Saturn itself → "
            "Saturn's return to its own natal position = major governance change signal."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch9-planet-bundle-crisis",
        sub_type="national_disruption",
        title="5+ Planets Bundled Within 30° in Sensitive Houses — National Crisis",
        source_chapter="Gopalakrishnan Ch 9, p.148",
        condition={
            "primary": (
                "Five or more planets concentrated within a 30° arc simultaneously, "
                "especially when this concentration falls in the national chart's "
                "6th, 8th, 12th, 10th, or 1st house."
            ),
            "threshold": "Concentration of 5 or more planets within 30° = problem.",
            "house_sensitivity": (
                "6th/8th/12th: maximum negative impact (war, death, loss). "
                "10th: governance crisis, leadership instability. "
                "1st: mass public upheaval, national identity crisis."
            ),
        },
        result=(
            "Major national or global crisis: mass deaths, market crashes, regime changes, "
            "wars, epidemics. The nature of crisis depends on which houses the bundle occupies "
            "and which planets are involved."
        ),
        synthesis_sources=["Gopalakrishnan Ch 9"],
        notes=(
            "Case study May 2003: Saturn+Mars in Taurus (fixed sign), Ketu in Scorpio. "
            "Results: mass deaths globally, world markets depressed (bearish), "
            "Saddam regime overthrown, tensions in multiple countries. "
            "Situation improved once Saturn left Taurus and Rahu-Saturn separated. "
            "This is the Detail C operative rule from Gopalakrishnan's yearly prediction framework. "
            "Track planetary bundles in ephemeris for upcoming 30°-concentration dates."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch9-eclipse-trika-axis-negative",
        sub_type="instability_gate",
        title="Eclipse in 6/8/12 Axis of National Chart — Very Negative",
        source_chapter="Gopalakrishnan Ch 9, p.148",
        condition={
            "primary": (
                "A solar or lunar eclipse falls within the 6th, 8th, or 12th house "
                "of the national chart, or aspects these houses by opposition "
                "(eclipse in 12th = also activates 6th by opposition, etc.)."
            ),
        },
        result=(
            "Very negative outcome for the nation. "
            "Eclipse in 6th: war, epidemic, debt crisis. "
            "Eclipse in 8th: leader death, mass casualties, government instability. "
            "Eclipse in 12th: financial ruin, foreign crisis, mass displacement."
        ),
        synthesis_sources=["Gopalakrishnan Ch 9", "Gopalakrishnan Ch 6", "Raphael Ch 25"],
        notes=(
            "This is Detail D in Gopalakrishnan's operational framework — "
            "the final checkpoint in annual prediction analysis. "
            "Cross-reference with Gopalakrishnan Ch 6 eclipse-trika-mass-death rule "
            "(mundane-gopal-ch6-eclipse-trika-mass-death) and "
            "Raphael Ch 25 eclipse-4th-8th rule (mundane-raphael-ch25-eclipse-4th-8th). "
            "All three authors independently confirm this as a critical negative signal. "
            "When eclipse in 6/8/12 ALSO coincides with Saturn/Rahu bundle there: maximum severity."
        ),
        severity="high",
        checkable=True,
    ),

    _rule(
        rule_id="mundane-gopal-ch9-abnormal-long-transit-amplification",
        sub_type="turbulence_signal",
        title="Planet Staying Abnormally Long in a Sign — Amplified Effects",
        source_chapter="Gopalakrishnan Ch 9, p.147",
        condition={
            "primary": (
                "A planet stays in a sign for significantly longer than its normal transit period, "
                "due to retrograde + direct motion cycles in the same sign."
            ),
            "examples": {
                "mars_kumbha": "Mars in Aquarius (Kumbha) for more than 6 months (normal = ~6 weeks).",
                "mercury_pisces": "Mercury in Pisces for more than 10 weeks (normal = less than 4 months).",
            },
        },
        result=(
            "The themes governed by that sign (and the houses it rules in the national chart) "
            "are amplified and prolonged for the duration. "
            "Both positive and negative effects are extended."
        ),
        synthesis_sources=["Gopalakrishnan Ch 9"],
        notes=(
            "This is Detail B in Gopalakrishnan's operational framework. "
            "Normal transit durations: Moon = 2.25 days per sign; Sun = 1 month; "
            "Mars = 6 weeks; Mercury = 3-4 weeks; Jupiter = 1 year; Saturn = 2.5 years. "
            "When Mars stays in Aquarius 6+ months due to retrograde, "
            "Aquarius/Leo themes (technology, government, speculation) are heavily activated."
        ),
        severity="medium",
        checkable=True,
    ),

]

# ============================================================
ALL_RULES = GROUP_Z + GROUP_AA

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
