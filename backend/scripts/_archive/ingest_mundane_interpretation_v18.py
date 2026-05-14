"""
Mundane Astrology — Interpretation Rules INGEST v18
====================================================
Batch : mundane-interp-v18-20260507
Collection : interpretation_rules
Science    : mundane_jyotish

Chapters encoded:
  Gopal Ch 5  — Oath Taking Charts
                Jaimini Ayurdaya tenure longevity rules
                Hora Lagna, Rasi Sandhi, Graha Yuddha vetoes
                11th-in-8th market rule, 6th/9th synergy, 5th Jupiter protection

  Mehta Ch 18 — Importance of Muhurta in Oath Taking
                Lagna selection rules (11-point protocol)
                Luminaries / Nakshatra / Tithi vetting rules
                Simhasan Chakra — Nadi level interpretations
                Leadership Autopsy patterns (Shastri/Chandrashekhar/Rao/Vajpayee/Mulayam)

DRY_RUN = True  →  set False (or use run_mundane_ingest.py) to write to MongoDB.

Groups:
  AT — Oath Chart Tenure Logic          (7 rules)
  AU — Muhurta Lagna Selection          (6 rules)
  AV — Simhasan Chakra Interpretations  (6 rules)
  AW — Leadership Autopsy Patterns      (8 rules)
  Total: 27 rules
"""

import asyncio
import os
import sys
import types
from datetime import datetime, timezone

# ── motor stub ────────────────────────────────────────────────────────────────
if "motor" not in sys.modules:
    _motor     = types.ModuleType("motor")
    _motor_asy = types.ModuleType("motor.motor_asyncio")
    class _FakeClient:
        def __getitem__(self, k): return self
        def __getattr__(self, k): return self
        async def update_one(self, *a, **kw): pass
    _motor_asy.AsyncIOMotorClient = _FakeClient
    sys.modules["motor"]               = _motor
    sys.modules["motor.motor_asyncio"] = _motor_asy

from motor.motor_asyncio import AsyncIOMotorClient   # noqa: E402

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.environ.get("DB_NAME",  "horoscope_db")
DRY_RUN   = True

_BATCH = "mundane-interp-v18-20260507"
_NOW   = datetime.now(timezone.utc).isoformat()

def _rule(rule_id, sub_type, title, source_chapter,
          condition, result, synthesis_sources,
          checkable=True, severity="medium"):
    return {
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
        "severity":         severity,
        "created_at":       _NOW,
    }


# ═════════════════════════════════════════════════════════════════════════════
# GROUP AT — Oath Chart Tenure Logic (Gopal Ch 5)
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AT = [

    _rule(
        rule_id  = "mundane-gopal-ch5-jaimini-long-tenure",
        sub_type = "oath_chart_tenure",
        title    = "Jaimini Ayurdaya: Long Tenure Gate — Moving + Moving Sign Types",
        source_chapter = "Gopal Ch 5 — Oath Taking Charts",
        condition = (
            "IF Lagna Lord of oath chart is in a Moving/Chara sign (Aries/Cancer/Libra/Capricorn) "
            "AND 8th Lord of oath chart is in a Moving/Chara sign "
            "→ Jaimini Ayurdaya classification = Long Life"
        ),
        result = (
            "Government has HIGH probability of completing its full mandate. "
            "Administration projects energy and adaptability. Long governance tenure indicated. "
            "Prognosis: administration likely goes the full term without premature collapse."
        ),
        synthesis_sources = [
            "gopal-ch5-jaimini-tenure-longevity",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch5-jaimini-medium-tenure",
        sub_type = "oath_chart_tenure",
        title    = "Jaimini Ayurdaya: Medium Tenure Gate — Dual + Dual Sign Types",
        source_chapter = "Gopal Ch 5 — Oath Taking Charts",
        condition = (
            "IF Lagna Lord of oath chart is in a Dual/Dwiswabhava sign (Gemini/Virgo/Sagittarius/Pisces) "
            "AND 8th Lord of oath chart is in a Dual/Dwiswabhava sign "
            "→ Jaimini Ayurdaya classification = Medium Life"
        ),
        result = (
            "Government will likely complete its mandate but may face mid-term crises, "
            "reshuffles, or a significantly weakened second half. Dual-sign energy produces "
            "an administration that pivots policy direction at least once. "
            "Prognosis: term completed but not without significant internal transitions."
        ),
        synthesis_sources = [
            "gopal-ch5-jaimini-tenure-longevity",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch5-jaimini-short-tenure",
        sub_type = "oath_chart_tenure",
        title    = "Jaimini Ayurdaya: Short Tenure Gate — Fixed + Fixed Sign Types",
        source_chapter = "Gopal Ch 5 — Oath Taking Charts",
        condition = (
            "IF Lagna Lord of oath chart is in a Fixed/Sthira sign (Taurus/Leo/Scorpio/Aquarius) "
            "AND 8th Lord of oath chart is in a Fixed/Sthira sign "
            "→ Jaimini Ayurdaya classification = Short Life"
        ),
        result = (
            "Government has HIGH RISK of premature fall, collapse of coalition, or forced "
            "early exit before the full mandate is completed. Fixed-sign rigidity in the "
            "8th house signals functional longevity problems. "
            "Prognosis: government unlikely to reach full term. Validate against Vajpayee 1996 "
            "(13-day government) where this pattern was confirmed."
        ),
        synthesis_sources = [
            "gopal-ch5-jaimini-tenure-longevity",
            "gopal-ch5-oath-chart-12-house-grid",
            "mehta-ch18-leadership-autopsy-database",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch5-hora-lagna-fixed-veto",
        sub_type = "oath_chart_tenure",
        title    = "Hora Lagna Double-Fixed Veto — Terminal Governance Signal",
        source_chapter = "Gopal Ch 5 — Oath Taking Charts",
        condition = (
            "IF Lagna of oath chart is in a Fixed sign (Taurus/Leo/Scorpio/Aquarius) "
            "AND Hora Lagna of oath chart is also in a Fixed sign "
            "→ Hora Lagna Double-Fixed Veto triggered"
        ),
        result = (
            "Survival Probability coefficient = 0.10 (terminal). "
            "This is the most dangerous configuration in oath chart analysis — "
            "the rigidity of both Lagna and Hora Lagna in Fixed signs signals "
            "near-certain premature collapse regardless of parliamentary majority. "
            "No amount of beneficial planetary support can override this structural veto. "
            "Government will not complete its mandate. Cross-check Jaimini Ayurdaya for confirmation."
        ),
        synthesis_sources = [
            "gopal-ch5-jaimini-tenure-longevity",
            "gopal-ch5-oath-case-studies",
        ],
        severity  = "critical",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch5-rasi-sandhi-veto",
        sub_type = "oath_chart_tenure",
        title    = "Rasi Sandhi Coefficient — Effective Governance Collapse",
        source_chapter = "Gopal Ch 5 — Oath Taking Charts",
        condition = (
            "IF 4 or more planets in the oath chart are placed at 0° or 29° of their sign "
            "(Rasi Sandhi — sign cusp / junction point) "
            "→ Rasi Sandhi veto triggered"
        ),
        result = (
            "Effective Governance coefficient = 0.20. "
            "Planets at Rasi Sandhi are in a 'between worlds' state — they cannot express "
            "their natural significations reliably. An oath chart with 4+ planets at the "
            "cusp becomes structurally incapable of coherent governance. "
            "Administration will be marked by policy paralysis, indecision, and inability "
            "to execute on any significant agenda. Government may technically survive its "
            "term but will be functionally hollow."
        ),
        synthesis_sources = [
            "gopal-ch5-jaimini-tenure-longevity",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch5-graha-yuddha-veto",
        sub_type = "oath_chart_tenure",
        title    = "Graha Yuddha in Oath Chart — Terminal Stability Veto",
        source_chapter = "Gopal Ch 5 — Oath Taking Charts",
        condition = (
            "IF two planets (excluding Sun and Moon) are within 1° of each other "
            "(Graha Yuddha / Planetary War) in the oath taking chart "
            "→ Graha Yuddha veto triggered"
        ),
        result = (
            "Terminal stability veto: the government cannot rule peacefully regardless of "
            "its parliamentary majority or popular mandate. "
            "The losing planet in the war (lower degree = loser) represents a critical "
            "governance sector that is permanently compromised. "
            "Administration is marked by continuous internal conflict, coalition friction, "
            "and the inability to project unified authority. "
            "Severity escalates if warring planets are chart lords (Lagna Lord or 10th Lord)."
        ),
        synthesis_sources = [
            "gopal-ch5-jaimini-tenure-longevity",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch5-11th-in-8th-market-rule",
        sub_type = "oath_chart_finance",
        title    = "11th Lord in 8th House — Stock Market Below Prior Administration",
        source_chapter = "Gopal Ch 5 — Oath Taking Charts",
        condition = (
            "IF the 11th lord (house of government gains, revenue, stock market) "
            "is placed in the 8th house (house of functional longevity, mass deaths, scams) "
            "in the oath taking chart"
        ),
        result = (
            "Foreign reserves and stock market performance will be LOWER at the end of this "
            "administration's tenure than at its start, and lower than the preceding government's "
            "market performance. The 8th house placement of the income lord directs gains "
            "into the house of obstruction and hidden matters. "
            "Economic policy may appear active but net financial outcomes will disappoint. "
            "Cross-reference with 2nd house (state finances) for severity."
        ),
        synthesis_sources = [
            "gopal-ch5-oath-chart-12-house-grid",
            "gopal-ch5-oath-case-studies",
        ],
        severity  = "medium",
        checkable = True,
    ),

]  # end GROUP_AT


# ═════════════════════════════════════════════════════════════════════════════
# GROUP AU — Muhurta Lagna Selection (Mehta Ch 18)
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AU = [

    _rule(
        rule_id  = "mundane-mehta-ch18-raman-democratic-lagnas",
        sub_type = "oath_muhurta_selection",
        title    = "Raman Democratic Lagna Rule — Aquarius and Libra for Oath Taking",
        source_chapter = "Mehta Ch 18 — Importance of Muhurta in Oath Taking",
        condition = (
            "IF Muhurta chart for oath taking has Aquarius or Libra as Lagna "
            "→ Raman's preferred democratic governance Lagnas"
        ),
        result = (
            "Aquarius (Saturn-ruled, democratic, people-oriented) and Libra (Venus-ruled, "
            "justice, balance) are B.V. Raman's recommended Lagnas for democratic oath-taking "
            "ceremonies. Both signs project an image of governance for the masses. "
            "Aquarius particularly favours long-term constitutional stability. "
            "Libra favours diplomatic success and judicial credibility. "
            "Selection of either Lagna, when free of affliction, is auspicious."
        ),
        synthesis_sources = [
            "mehta-ch18-lagna-selection-11-points",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-cancer-leo-partner-discord",
        sub_type = "oath_muhurta_selection",
        title    = "Cancer/Leo Lagna — Coalition Partner Discord in Oath Charts",
        source_chapter = "Mehta Ch 18 — Importance of Muhurta in Oath Taking",
        condition = (
            "IF Muhurta chart for oath taking has Cancer or Leo as Lagna "
            "AND Saturn or Mars aspects the Lagna or Lagna Lord"
        ),
        result = (
            "Cancer and Leo Lagnas in oath charts produce discord with coalition partners. "
            "Cancer (Moon-ruled) creates over-sensitivity and dependency on external support; "
            "Leo (Sun-ruled) creates ego conflicts within the ruling alliance. "
            "When additionally afflicted by Saturn or Mars, the administration will be "
            "characterised by continuous friction with allies, defection threats, and "
            "an inability to maintain a stable governing majority."
        ),
        synthesis_sources = [
            "mehta-ch18-lagna-selection-11-points",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-capricorn-lagna-exclusion",
        sub_type = "oath_muhurta_selection",
        title    = "Capricorn Lagna Exclusion — Mehta's Governance Anti-Pattern",
        source_chapter = "Mehta Ch 18 — Importance of Muhurta in Oath Taking",
        condition = (
            "IF Muhurta chart for oath taking has Capricorn as Lagna "
            "→ Mehta's Capricorn governance anti-pattern triggered"
        ),
        result = (
            "Capricorn Lagna is specifically identified by Mehta as unsuitable for democratic "
            "oath-taking ceremonies. Saturn's cold, slow, obstructive nature as Lagna ruler "
            "creates an administration that is bureaucratically paralysed, slow to execute, "
            "and perceived by the public as cold or out-of-touch. "
            "Leadership will struggle to project warmth, accessibility, or public connection. "
            "Exclude Capricorn from Muhurta selection when choosing oath chart timing."
        ),
        synthesis_sources = [
            "mehta-ch18-lagna-selection-11-points",
        ],
        severity  = "medium",
        checkable = False,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-8th-house-vacancy-rule",
        sub_type = "oath_muhurta_selection",
        title    = "8th House Vacancy Requirement — Core Longevity Gate",
        source_chapter = "Mehta Ch 18 — Importance of Muhurta in Oath Taking",
        condition = (
            "IF the 8th house of the Muhurta chart contains any planet at time of oath taking "
            "→ 8th house vacancy rule violated"
        ),
        result = (
            "The 8th house MUST be empty of all planets in the oath-taking Muhurta chart. "
            "Any planet in the 8th house at the moment of oath taking directly compromises "
            "the functional longevity of the administration. "
            "Malefics (Saturn/Mars/Rahu/Ketu) in the 8th = severe threat to government survival. "
            "Even benefics (Jupiter/Venus) in the 8th delay and obstruct the full expression "
            "of the government's productive mandate. "
            "This is a non-negotiable requirement in Muhurta selection — "
            "any competent astrologer must veto an oath time with an occupied 8th house."
        ),
        synthesis_sources = [
            "mehta-ch18-lagna-selection-11-points",
            "gopal-ch5-jaimini-tenure-longevity",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-papakatari-discord",
        sub_type = "oath_muhurta_selection",
        title    = "Papakatari Yoga on Lagna — Continuous Bickering Administration",
        source_chapter = "Mehta Ch 18 — Importance of Muhurta in Oath Taking",
        condition = (
            "IF both the 12th house AND the 2nd house from Lagna in the Muhurta chart "
            "are occupied by malefic planets (Saturn/Mars/Rahu/Ketu/Sun) "
            "→ Papakatari Yoga on Lagna formed"
        ),
        result = (
            "Papakatari Yoga on the Lagna hemmed between two malefics creates an "
            "administration characterised by: "
            "(1) Continuous bickering and infighting within the Cabinet; "
            "(2) Public perception of a fractious, uncoordinated government; "
            "(3) Communication failures — government cannot deliver a clear message (2nd lord afflicted); "
            "(4) Losses and expenditure exceeding projections (12th lord activated). "
            "Leadership will expend most of its energy managing internal party friction "
            "rather than delivering on policy agenda."
        ),
        synthesis_sources = [
            "mehta-ch18-lagna-selection-11-points",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-nakshatra-tithi-veto-combo",
        sub_type = "oath_muhurta_selection",
        title    = "Rikta Tithi + Malefic Nakshatra Combo — Double Muhurta Veto",
        source_chapter = "Mehta Ch 18 — Importance of Muhurta in Oath Taking",
        condition = (
            "IF the oath is taken on a Rikta Tithi (4th/9th/14th lunar day) "
            "AND the Moon is in a malefic nakshatra (Ashlesha/Jyeshtha/Moola/Magha/Mrigshira/Ardra) "
            "→ Double Muhurta veto triggered"
        ),
        result = (
            "Rikta (empty/void) Tithis combined with a malefic Moon nakshatra create a "
            "double-veto in Muhurta analysis. "
            "Rikta Tithis signify emptiness and lack of fructification — plans do not reach "
            "completion. Malefic Moon nakshatra adds emotional instability, public antipathy, "
            "and adversarial media coverage to the administration. "
            "Together: government projects that appear to start well will fail to materialise, "
            "and public trust will erode faster than in any single-veto scenario. "
            "Both conditions must be avoided in selecting oath-taking Muhurta."
        ),
        synthesis_sources = [
            "mehta-ch18-luminaries-nakshatra-tithi-vetting",
            "mehta-ch18-lagna-selection-11-points",
        ],
        severity  = "high",
        checkable = True,
    ),

]  # end GROUP_AU


# ═════════════════════════════════════════════════════════════════════════════
# GROUP AV — Simhasan Chakra Interpretations (Mehta Ch 18)
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AV = [

    _rule(
        rule_id  = "mundane-mehta-ch18-simhasan-moon-absolute-power",
        sub_type = "simhasan_chakra",
        title    = "Moon in Simhasan Nakshatra — Absolute Political Authority",
        source_chapter = "Mehta Ch 18 — Simhasan Chakra (Panch Nadi)",
        condition = (
            "IF Moon in the oath chart is in a Simhasan-level nakshatra "
            "(Mrigshira/Chitra/Dhanishtha — the throne-level nakshatras governed by Mars) "
            "→ Moon occupies the Simhasan (throne) position in the Panch Nadi grid"
        ),
        result = (
            "The leader sits on the metaphorical throne — occupying a position of absolute "
            "political authority and dominance. "
            "Administration projects unquestioned command. The leader's will is the "
            "government's direction. No effective political opposition can challenge the "
            "ruling position during this administration. "
            "The Moon's placement here overrides standard house analysis — even a weak "
            "Lagna or afflicted 10th house is substantially mitigated by Simhasan Moon. "
            "This is the strongest possible Simhasan Chakra signal for political power."
        ),
        synthesis_sources = [
            "mehta-ch18-simhasan-chakra-complete",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-simhasan-jupiter-protection",
        sub_type = "simhasan_chakra",
        title    = "Moon in Patta Nakshatra — Constitutional Protection and Judicial Shield",
        source_chapter = "Mehta Ch 18 — Simhasan Chakra (Panch Nadi)",
        condition = (
            "IF Moon in the oath chart is in a Patta-level nakshatra "
            "(Krittika/Punarvasu/U.Phalguni/Vishakha/U.Ashadha/P.Bhadrapada — "
            "governed by Sun and Jupiter) "
            "→ Moon occupies the Patta (canopy/umbrella) position in the Panch Nadi grid"
        ),
        result = (
            "The leader is sheltered under the protective umbrella of constitutional and "
            "judicial authority. "
            "Sun/Jupiter's governance of this level indicates: strong Rajya Sabha support, "
            "legal victories when challenged, Supreme Court rulings in the government's favour, "
            "and the ability to withstand no-confidence motions through procedural means. "
            "The administration may not be the most popular but will prove constitutionally "
            "durable and resistant to judicial removal."
        ),
        synthesis_sources = [
            "mehta-ch18-simhasan-chakra-complete",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-simhasan-aasan-saturn-terminal",
        sub_type = "simhasan_chakra",
        title    = "Moon in Aasan Nakshatra — Dependency Governance (Terminal if Saturn)",
        source_chapter = "Mehta Ch 18 — Simhasan Chakra (Panch Nadi)",
        condition = (
            "IF Moon in the oath chart is in an Aasan-level nakshatra "
            "(Bharani/Pushya/P.Phalguni/Anuradha/P.Ashadha/U.Bhadrapada — "
            "governed by Venus and Saturn) "
            "AND the Dasha lord at oath time is Saturn "
            "→ Aasan-Saturn terminal configuration"
        ),
        result = (
            "Moon in Aasan indicates the leader governs from a 'supported chair' — "
            "dependent on coalition partners, allies, or a High Command for survival. "
            "When the Dasha lord is also Saturn (which governs half of the Aasan nakshatras): "
            "the dependency becomes acute and terminal — the administration is entirely "
            "at the mercy of external power brokers. "
            "Prognosis: government completes its term but the leader has no independent agency. "
            "Every major decision requires approval from a force outside the formal Cabinet. "
            "Manmohan Singh 2004 (Moon in Aasan, governed by external coalition + High Command) "
            "is the validated case study for this pattern."
        ),
        synthesis_sources = [
            "mehta-ch18-simhasan-chakra-complete",
            "mehta-ch18-leadership-autopsy-database",
            "gopal-ch5-oath-case-studies",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-simhasan-martial-king",
        sub_type = "simhasan_chakra",
        title    = "Moon in Simhasan + Mars Dasha Lord — Martial King Pattern",
        source_chapter = "Mehta Ch 18 — Simhasan Chakra (Panch Nadi)",
        condition = (
            "IF Moon in the oath chart is in a Simhasan nakshatra (Mrigshira/Chitra/Dhanishtha) "
            "AND the Dasha lord at the time of oath taking is Mars "
            "→ Moon-Simhasan + Mars Dasha affinity confirmed (both Mars-governed)"
        ),
        result = (
            "The Martial King Pattern: Simhasan nakshatras are Mars-governed, and when the "
            "Dasha lord is also Mars, the Simhasan Chakra affinity rule produces a doubled "
            "martial signal. "
            "Administration will be characterised by: decisive executive action, willingness "
            "to use state force when challenged, strong border security posture, "
            "and confrontational approach to political opponents. "
            "The leader will be perceived as aggressive, decisive, and potentially authoritarian. "
            "High probability of military engagement or border tension during this tenure. "
            "This is Mehta's 'Martial King' archetype — strong, confrontational governance."
        ),
        synthesis_sources = [
            "mehta-ch18-simhasan-chakra-complete",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-aadhaar-dependency-governance",
        sub_type = "simhasan_chakra",
        title    = "Moon in Aadhaar Nakshatra — Foundation-Level Governance (Weakest)",
        source_chapter = "Mehta Ch 18 — Simhasan Chakra (Panch Nadi)",
        condition = (
            "IF Moon in the oath chart is in an Aadhaar-level nakshatra "
            "(Ashwini/Ashlesha/Magha/Jyeshtha/Moola/Revati — governed by Ketu and Mercury) "
            "→ Moon occupies the Aadhaar (foundation) position — lowest authority level"
        ),
        result = (
            "Aadhaar (foundation) represents the weakest position in the Panch Nadi hierarchy. "
            "The leader governs from the ground floor — the administration lacks the elevated "
            "authority to project power effectively. "
            "Governance is reactive rather than proactive. "
            "The government will be perceived as unstable, inexperienced, or unable to rise "
            "above immediate crises to execute a strategic agenda. "
            "Ketu-ruled Aadhaar nakshatras (Ashwini/Magha/Moola) add a sudden-break quality — "
            "the administration may end abruptly or through an unexpected trigger. "
            "Mercury-ruled Aadhaar (Ashlesha/Jyeshtha/Revati) adds communicative weakness."
        ),
        synthesis_sources = [
            "mehta-ch18-simhasan-chakra-complete",
            "gopal-ch5-jaimini-tenure-longevity",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-simha-moon-rahu-dasha",
        sub_type = "simhasan_chakra",
        title    = "Moon in Simha Nakshatra + Rahu Dasha — Shadow Authority Pattern",
        source_chapter = "Mehta Ch 18 — Simhasan Chakra (Panch Nadi)",
        condition = (
            "IF Moon in the oath chart is in a Simha-level nakshatra "
            "(Rohini/Aridra/Hasta/Swati/Shravana/Shatbhisha — governed by Moon and Rahu) "
            "AND the Dasha lord at oath time is Rahu "
            "→ Simha-Rahu shadow authority configuration"
        ),
        result = (
            "Simha (lion, seat of lions) is the second tier in the Panch Nadi hierarchy, "
            "just below the throne. When Rahu (the shadow) is also the Dasha lord, "
            "the Simhasan Chakra affinity rule (Dasha lord matching the Nadi level lord) fires: "
            "the administration operates with significant behind-the-scenes power but "
            "projects ambiguity to the public. "
            "Leadership will be effective but controversial — perceived as opaque, "
            "operating through hidden channels. "
            "Rahu's nature amplifies: media scrutiny, perception of irregularities, "
            "and governance through unconventional means. "
            "The government achieves its objectives but at a reputational cost."
        ),
        synthesis_sources = [
            "mehta-ch18-simhasan-chakra-complete",
        ],
        severity  = "medium",
        checkable = True,
    ),

]  # end GROUP_AV


# ═════════════════════════════════════════════════════════════════════════════
# GROUP AW — Leadership Autopsy Patterns (Mehta Ch 18)
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AW = [

    _rule(
        rule_id  = "mundane-mehta-ch18-shastri-terminal-leadership",
        sub_type = "leadership_autopsy",
        title    = "Shastri 1964 Pattern — Terminal Leadership (Death in Office)",
        source_chapter = "Mehta Ch 18 — Leadership Autopsy Database",
        condition = (
            "IF oath chart shows 5+ of the following adverse features simultaneously: "
            "(1) Lagna Lord in 8th house, "
            "(2) 8th Lord in Lagna or aspecting Lagna, "
            "(3) Saturn in the 1st or 8th house, "
            "(4) Moon in a Kendra (1/4/7/10) and afflicted by malefics, "
            "(5) Jupiter (karaka for life) debilitated or combust, "
            "(6) 5th house afflicted (assassination survival compromised), "
            "(7) Sandhi nakshatras in critical positions, "
            "(8) No benefic aspect on Lagna or Lagna Lord, "
            "(9) Graha Yuddha involving the Lagna Lord "
            "→ Shastri Terminal Leadership Pattern triggered"
        ),
        result = (
            "Lal Bahadur Shastri (oath: 9 June 1964) — 9 adverse features present in his "
            "oath chart. He died in office on 11 January 1966 in Tashkent under mysterious "
            "circumstances just after signing the Tashkent Declaration. "
            "Pattern indicates: administration ends with the leader's death in office, "
            "not through electoral defeat or political collapse. "
            "The higher the adverse feature count above 5, the greater the risk of "
            "in-office death vs. mere non-completion of mandate."
        ),
        synthesis_sources = [
            "mehta-ch18-leadership-autopsy-database",
            "gopal-ch5-jaimini-tenure-longevity",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "critical",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-vajpayee-balarishta-pattern",
        sub_type = "leadership_autopsy",
        title    = "Vajpayee 1996 — 13-Day Balarishta Government Pattern",
        source_chapter = "Mehta Ch 18 — Leadership Autopsy Database",
        condition = (
            "IF oath chart shows ALL of the following simultaneously: "
            "(1) Jaimini Ayurdaya = Short Life (Fixed + Fixed sign types for Lagna/8th lords), "
            "(2) 10th lord weak (debilitated, combust, or in 6th/8th/12th), "
            "(3) Lagna lord not aspecting Lagna, "
            "(4) Moon afflicted by 2+ malefics simultaneously, "
            "(5) No majority coalition (verified externally — not from chart alone) "
            "→ Balarishta (infant death) government pattern triggered"
        ),
        result = (
            "Atal Bihari Vajpayee (oath: 16 May 1996) — 8 adverse features, including "
            "Jaimini Short Life configuration. Government lasted only 13 days before a "
            "floor test defeat. This is the fastest government collapse in Indian history. "
            "Pattern indicates: government will not last more than a few weeks. "
            "The term 'Balarishta' (death in infancy) from classical longevity analysis "
            "applies here — the administration is stillborn at the governance level. "
            "Any government with this chart configuration should not be expected to "
            "survive the first no-confidence vote."
        ),
        synthesis_sources = [
            "mehta-ch18-leadership-autopsy-database",
            "gopal-ch5-jaimini-tenure-longevity",
        ],
        severity  = "critical",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-sandhi-bharani-lethality",
        sub_type = "leadership_autopsy",
        title    = "Sandhi-Bharani Lethality Rule — Bharani at Sign Junction = Maximum Death Signal",
        source_chapter = "Mehta Ch 18 — Leadership Autopsy Database",
        condition = (
            "IF the Moon in the oath chart is in Bharani nakshatra (ruled by Venus, "
            "nakshatra of Yama/death) AND is simultaneously at a Rasi Sandhi (0° or 29° "
            "of a sign) — placing it at the most vulnerable junction point "
            "→ Sandhi-Bharani lethality configuration triggered"
        ),
        result = (
            "Bharani is the nakshatra of Yama (god of death) — it governs endings, "
            "transition, and irreversible finality. When placed at a Rasi Sandhi, "
            "the death-oriented quality of Bharani is amplified to its maximum. "
            "In an oath chart: the administration's end will be sudden, final, and marked "
            "by events of irreversible consequence. "
            "In severe cases (additional 8th house affliction): literal death of the leader. "
            "In moderate cases: the administration ends so decisively that all its policies "
            "are immediately reversed by the successor — a complete governance discontinuity. "
            "Validate against Shastri (Bharani prominent in his 1964 chart)."
        ),
        synthesis_sources = [
            "mehta-ch18-leadership-autopsy-database",
            "mehta-ch18-luminaries-nakshatra-tithi-vetting",
            "gopal-ch5-jaimini-tenure-longevity",
        ],
        severity  = "critical",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-narasimha-rao-liberalisation-dhana",
        sub_type = "leadership_autopsy",
        title    = "Narasimha Rao 1991 — Liberalisation Dhana Yoga Pattern",
        source_chapter = "Mehta Ch 18 — Leadership Autopsy Database",
        condition = (
            "IF oath chart shows 5+ of the following positive features: "
            "(1) Lagna Lord in Kendra or Trikona with no severe affliction, "
            "(2) 2nd and 11th lords connected by aspect or conjunction (Dhana Yoga), "
            "(3) Jupiter in angle or trine, "
            "(4) Moon waxing (Shukla Paksha) at time of oath, "
            "(5) 10th lord strong and unafflicted, "
            "(6) Saturn placed favourably (3rd/6th/11th from Lagna), "
            "(7) No malefics in the 8th house "
            "→ Liberalisation Dhana Yoga pattern triggered"
        ),
        result = (
            "P.V. Narasimha Rao (oath: 21 June 1991) — 7 positive features including "
            "strong Dhana Yoga. His administration oversaw India's 1991 economic liberalisation "
            "(the most transformative economic shift in post-independence India). "
            "Pattern indicates: administration will preside over significant economic "
            "expansion, structural reforms, or a major economic transformation. "
            "The Dhana Yoga link between 2nd and 11th lords is the critical indicator of "
            "historic wealth generation under this government."
        ),
        synthesis_sources = [
            "mehta-ch18-leadership-autopsy-database",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-many-bosses-constraint",
        sub_type = "leadership_autopsy",
        title    = "Many Bosses Constraint — Multi-Lord Oath Chart Configuration",
        source_chapter = "Mehta Ch 18 — Leadership Autopsy Database",
        condition = (
            "IF the oath chart shows 3+ of the following simultaneously: "
            "(1) Lagna Lord in the sign or nakshatra of another planet (parivartana or dependency), "
            "(2) 10th Lord under aspect of 3+ other planets, "
            "(3) Sun (natural karaka of leadership) conjunct or aspected by 2+ planets, "
            "(4) Moon in Aasan-level nakshatra (Venus/Saturn governed — dependency nakshatras), "
            "(5) 9th lord (High Command) stronger than 10th lord (executive) "
            "→ Many Bosses Constraint triggered"
        ),
        result = (
            "Manmohan Singh 2004 (oath: 22 May 2004) — 15 features including multiple "
            "indicators of constrained authority. Manmohan Singh governed effectively but "
            "was publicly acknowledged as operating under the authority of the Congress "
            "High Command (Sonia Gandhi). "
            "Pattern indicates: the nominal leader does not hold real power. "
            "Policy decisions are made outside the formal Cabinet structure. "
            "The leader is an implementer of others' vision, not an independent architect. "
            "Administration can still achieve significant results but the leader's personal "
            "agency is structurally limited throughout the tenure."
        ),
        synthesis_sources = [
            "mehta-ch18-leadership-autopsy-database",
            "gopal-ch5-oath-case-studies",
            "mehta-ch18-simhasan-chakra-complete",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-enemy-lord-coalition",
        sub_type = "leadership_autopsy",
        title    = "Enemy Lord Coalition Rule — Hostile Alliance Signs Imminent Collapse",
        source_chapter = "Mehta Ch 18 — Leadership Autopsy Database",
        condition = (
            "IF in the oath chart the Lagna lord and the 7th lord (natural enemies by sign) "
            "are conjunct OR in mutual aspect (paap-kartari between them) "
            "AND the 10th lord is simultaneously weak "
            "→ Enemy Lord Coalition rule triggered"
        ),
        result = (
            "A government formed from a coalition of natural political enemies — parties or "
            "leaders whose fundamental agendas are opposed — cannot sustain itself. "
            "The Lagna lord (administration's identity) in conflict with the 7th lord "
            "(the opposition) while the 10th lord (executive authority) is weak indicates "
            "that the government's survival depends entirely on preventing its own coalition "
            "from collapsing. "
            "Administration will spend more time managing coalition partners than governing. "
            "Chandrashekhar 1990 (oath: 10 November 1990) is the validated case: his "
            "coalition rested on Congress (I) outside support — the moment Congress withdrew, "
            "the government collapsed. Lasted 7 months."
        ),
        synthesis_sources = [
            "mehta-ch18-leadership-autopsy-database",
            "gopal-ch5-jaimini-tenure-longevity",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-ashtakvarga-8th-lord-stronger",
        sub_type = "leadership_autopsy",
        title    = "Ashtakvarga 8th Lord Stronger Than Lagna Lord — Collapse Indicator",
        source_chapter = "Mehta Ch 18 — Leadership Autopsy Database",
        condition = (
            "IF in the oath chart the Ashtakvarga bindus (benefic points) of the 8th Lord "
            "exceed the Ashtakvarga bindus of the Lagna Lord "
            "→ Ashtakvarga 8th-lord-stronger collapse indicator triggered"
        ),
        result = (
            "When the 8th lord (obstruction, longevity challenge, hidden destruction) "
            "is stronger than the Lagna lord (administration's fundamental vitality) "
            "in the Ashtakvarga point count, the destructive force within the administration "
            "exceeds its constructive capacity. "
            "This is Mulayam Singh Yadav's 1993 pattern (oath: 4 December 1993) — "
            "8th lord Ashtakvarga score exceeded Lagna lord score by 3+ bindus. "
            "The administration was unable to overcome its structural internal contradictions. "
            "Prognosis: government completes its term but is progressively weakened by "
            "its own contradictions until it is a shell of its original mandate. "
            "Use as a secondary confirmation alongside Jaimini Ayurdaya."
        ),
        synthesis_sources = [
            "mehta-ch18-leadership-autopsy-database",
            "gopal-ch5-jaimini-tenure-longevity",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch18-chandrashekhar-collapse-pattern",
        sub_type = "leadership_autopsy",
        title    = "Chandrashekhar 1990 — Transitionary Collapse Pattern",
        source_chapter = "Mehta Ch 18 — Leadership Autopsy Database",
        condition = (
            "IF oath chart shows ALL of the following: "
            "(1) No independent parliamentary majority (externally verified), "
            "(2) 7th lord (opposition) stronger than 10th lord (executive), "
            "(3) 4th house (domestic stability / High Command support) afflicted or empty of benefics, "
            "(4) Moon in the last degrees (27°-29°) of a sign (transition / instability nakshatra section), "
            "(5) Jaimini classification = Short or Medium Life "
            "→ Transitionary Collapse Pattern triggered"
        ),
        result = (
            "Chandrashekhar (oath: 10 November 1990) — 5 adverse features. "
            "His government was entirely dependent on Congress (I) outside support. "
            "When that support was withdrawn (March 1991), the government fell with 7 months "
            "of tenure completed. "
            "Pattern indicates: the administration is structurally transitionary — "
            "it exists only to fill a gap between two more substantive governments. "
            "The leader is a caretaker, not an architect. "
            "Administration may achieve one landmark act (Chandrashekhar's legacy: managed "
            "the 1991 economic crisis until a stable government could be formed) "
            "but cannot pursue a sustained agenda. "
            "Historically: transitionary governments often enable the NEXT government's "
            "transformative opportunity."
        ),
        synthesis_sources = [
            "mehta-ch18-leadership-autopsy-database",
            "gopal-ch5-jaimini-tenure-longevity",
            "gopal-ch5-oath-chart-12-house-grid",
        ],
        severity  = "medium",
        checkable = True,
    ),

]  # end GROUP_AW


# ─────────────────────────────────────────────────────────────────────────────
ALL_RULES = GROUP_AT + GROUP_AU + GROUP_AV + GROUP_AW
# ─────────────────────────────────────────────────────────────────────────────


async def run():
    if DRY_RUN:
        print(f"[DRY RUN] Would upsert {len(ALL_RULES)} rules into interpretation_rules")
        for r in ALL_RULES:
            print(f"  • {r['rule_id']}  [{r['severity']}]")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    col    = client[DB_NAME]["interpretation_rules"]
    ok = 0
    for rule in ALL_RULES:
        await col.update_one(
            {"rule_id": rule["rule_id"]},
            {"$set": rule},
            upsert=True,
        )
        ok += 1
    client.close()
    print(f"[v18 interp] Upserted {ok}/{len(ALL_RULES)} rules → interpretation_rules ✓")


if __name__ == "__main__":
    asyncio.run(run())
