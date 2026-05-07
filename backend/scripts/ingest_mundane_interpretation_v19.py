"""
Mundane Astrology — Interpretation Rules INGEST v19
====================================================
Batch : mundane-interp-v19-20260507
Collection : interpretation_rules
Science    : mundane_jyotish

Chapters encoded:
  Gopal Ch 4  — How to Predict for Elections
                Election winner/loser logic rules
                Spoiler vetoes (Rasi Sandhi, 6th lord nexus, 8th Saturn)
                Dasha timing vectors and Indian political context

  Mehta Ch 22/23 — Yearly Governance Engine
                   Lord of Year qualitative rules (all 7 planets as Raja)
                   Cabinet portfolio pair diagnostics

DRY_RUN = True  →  set False (or use run_mundane_ingest.py) to write to MongoDB.

Groups:
  AX — Election Winner/Loser Logic       (8 rules)
  AY — Indian Political Context          (4 rules)
  AZ — Lord of Year Quality              (7 rules)
  BA — Cabinet Pair Diagnostics          (7 rules)
  Total: 26 rules
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

_BATCH = "mundane-interp-v19-20260507"
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
# GROUP AX — Election Winner / Loser Logic (Gopal Ch 4)
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AX = [

    _rule(
        rule_id  = "mundane-gopal-ch4-tri-lagna-sweep-winner",
        sub_type = "election_prediction",
        title    = "Tri-Lagna Sweep — 10th Lord Strong in 2+ Reference Points = Victory",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF Candidate A's 10th lord is STRONG (in 11th, 9th, exalted, Vargottama, or Raja Yoga) "
            "in 2 or more of the three Tri-Lagna reference points (Lagna / Chandra Lagna / Karkamsha Lagna) "
            "AND Candidate B's 10th lord scores 0–1 strong reference points "
            "→ Tri-Lagna Sweep triggered for Candidate A"
        ),
        result = (
            "Prediction: Candidate A is the projected election winner. "
            "The higher the frequency of strong 10th lord placements, the higher the "
            "victory margin. A 3/3 sweep (all three reference points strong) indicates "
            "a landslide; a 2/3 score indicates a comfortable majority. "
            "Validated: Bush 2000 (3/3 sweep) vs. Gore (0/2) — decisive result confirmed."
        ),
        synthesis_sources = [
            "gopal-ch4-tri-lagna-election-engine",
            "gopal-ch4-election-case-studies",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch4-rasi-sandhi-10th-lord-spoiler",
        sub_type = "election_prediction",
        title    = "Rasi Sandhi Spoiler — 10th Lord at 0°/29° Negates Apparent Strength",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF a candidate's 10th lord is placed at 0° or 29° of any sign "
            "(Rasi Sandhi — sign junction point) in ANY of the Tri-Lagna reference charts "
            "→ Rasi Sandhi Spoiler veto triggered for that reference point"
        ),
        result = (
            "The Rasi Sandhi placement NEGATES the house-based strength of the 10th lord. "
            "A 10th lord in the 11th house that is at 29° is treated as WEAK, not strong, "
            "for the purposes of the Tri-Lagna comparison. "
            "Even a candidate who appears to have a strong 10th lord position will fail "
            "to 'cross the finish line' — the Sandhi position creates an invisible structural fault. "
            "High probability of losing a close contest or failing through technicalities. "
            "Validated: Kerry 2004 — 10th lord at Rasi Sandhi in 2nd house; lost despite poll leads."
        ),
        synthesis_sources = [
            "gopal-ch4-election-spoiler-logic",
            "gopal-ch4-election-case-studies",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch4-sixth-lord-nexus-defeat",
        sub_type = "election_prediction",
        title    = "6th Lord Nexus — 10th Lord Contaminated by Opposition = Defeat by Intrigue",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF a candidate's 10th lord is conjunct the 6th lord "
            "OR receives a direct aspect from the 6th lord "
            "in the natal chart (from any of the three Tri-Lagna reference points) "
            "→ 6th Lord Nexus defeat signal triggered"
        ),
        result = (
            "The candidate's authority/career indicator (10th lord) is contaminated by the "
            "house of enemies, obstacles, and opposition (6th lord). "
            "This candidate will lose power through opposition manoeuvring, legal challenges, "
            "internal party betrayal, or engineered political scandal. "
            "The defeat is NOT a clean electoral loss — it is constructed by adversaries "
            "exploiting a structural vulnerability. "
            "Even a strong 10th lord placement cannot overcome 6th lord contamination."
        ),
        synthesis_sources = [
            "gopal-ch4-election-spoiler-logic",
            "gopal-ch4-tri-lagna-election-engine",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch4-eighth-saturn-sudden-reversal",
        sub_type = "election_prediction",
        title    = "8th House Saturn — Sudden Unexpected Electoral Reversal",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF Saturn is natally placed in the 8th house of a candidate's chart "
            "OR Saturn is transiting the 8th house from the candidate's natal Lagna or Moon "
            "at the time of the election cycle "
            "→ 8th house Saturn sudden-reversal signal triggered"
        ),
        result = (
            "Indicates a sudden, unexpected reversal of electoral fortune. "
            "The fall arrives from an entirely unanticipated direction — NOT from the "
            "visible political opponent or from standard electoral arithmetic. "
            "Can manifest as: health crisis, sudden scandal, forced withdrawal from candidacy, "
            "or an unforeseen event that removes the candidate from contention at the last moment. "
            "Validated: Vajpayee 2004 — Saturn in 8th; lost unexpectedly despite pre-election "
            "projections showing BJP ahead."
        ),
        synthesis_sources = [
            "gopal-ch4-election-spoiler-logic",
            "gopal-ch4-election-case-studies",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch4-eleventh-house-dasha-surge",
        sub_type = "election_prediction",
        title    = "11th House Dasha Surge — Winning Momentum Coefficient 0.90",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF the candidate's active Dasha or Bhukti lord at the time of polling "
            "is placed in the 11th house (Labha/Gains) from the Lagna OR from the Moon "
            "→ 11th House Dasha Surge winning momentum triggered"
        ),
        result = (
            "Winning Momentum coefficient = 0.90. "
            "The 11th house is the house of gains, fulfillment of desires, and electoral victory. "
            "A Dasha/Bhukti whose period lord occupies the 11th house from either key Lagna "
            "provides the decisive timing push for electoral victory. "
            "This is the single most reliable Dasha-level confirmation of a win. "
            "Validated: Bush 2000 — Saturn/Rahu Dasha with Rahu in 11th from Lagna. "
            "A candidate with a moderate Tri-Lagna score but 11th house Dasha lord "
            "can still win a close race."
        ),
        synthesis_sources = [
            "gopal-ch4-election-dasha-timing",
            "gopal-ch4-election-case-studies",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch4-incumbent-vulnerability-trigger",
        sub_type = "election_prediction",
        title    = "Incumbent Vulnerability — 8th Lord Dasha + 10th Lord in 3rd = Regime Shift",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF the incumbent candidate/government is running a Dasha of the 8th lord "
            "(obstruction / hidden transformation period) "
            "AND the 10th lord (executive authority) is placed in the 3rd house "
            "(effort / valour — fighting without structural executive backing) "
            "→ Incumbent Vulnerability trigger fired"
        ),
        result = (
            "Incumbency Warning: High risk of the incumbent being voted out by an emerging "
            "new political force or 'star' in the opposition. "
            "The 8th lord Dasha signals hidden upheaval approaching from beneath. "
            "The 10th lord in 3rd means the incumbent is fighting hard but lacks the "
            "structural elevation of a 10th-house executive mandate. "
            "A new challenger with a clean 10th lord will outshine the incumbent. "
            "Validated: TDP 2004 case (incumbent running 8th lord Dasha with 10th in 3rd; "
            "lost to Rajasekhara Reddy's Congress wave in Andhra Pradesh)."
        ),
        synthesis_sources = [
            "gopal-ch4-election-spoiler-logic",
            "gopal-ch4-election-dasha-timing",
            "gopal-ch4-election-case-studies",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch4-destiny-anchor-karkamsha",
        sub_type = "election_prediction",
        title    = "Destiny Anchor — Karkamsha 10th Lord + Trikona Lord = Marked for High Office",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF the 10th lord in the Karkamsha Lagna chart is conjunct or aspected by "
            "a Trikona lord (1st/5th/9th house lords) in the Karkamsha Lagna "
            "→ Destiny Anchor triggered — candidate is marked by fate for high office"
        ),
        result = (
            "Destiny Alert: This candidate has a soul-level mandate for high political office. "
            "The Karkamsha represents the deepest destiny blueprint of the individual. "
            "A Trikona connection to the 10th lord here indicates that leadership is fated — "
            "the divine mandate for governance is present regardless of immediate transit "
            "conditions or opposition strength. "
            "Weight modifier: +0.30 to overall Tri-Lagna strength coefficient. "
            "A candidate with this configuration should never be written off, even when "
            "external political conditions appear unfavourable."
        ),
        synthesis_sources = [
            "gopal-ch4-tri-lagna-election-engine",
            "gopal-ch4-election-dasha-timing",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch4-saturn-transit-defeat-veto",
        sub_type = "election_prediction",
        title    = "Saturn Ashtama Transit — 8th from Moon/Lagna = Defeat Likely",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF Saturn is transiting the 8th house from the candidate's natal Moon "
            "OR 8th house from the natal Lagna (Ashtama Shani) at the time of the election "
            "→ Saturn Ashtama Transit defeat signal triggered"
        ),
        result = (
            "Defeat Likely under Ashtama Shani. "
            "The 8th transit of Saturn from Moon or Lagna is the classical maximum-obstruction "
            "period — exhaustion of vitality, cumulative burdens reaching a peak, "
            "and the inability to project forward momentum. "
            "In an election context: the candidate cannot sustain the campaign energy required "
            "to close out a victory. Resources, stamina, and public support all erode "
            "during Ashtama Shani. "
            "Exception: if Jupiter simultaneously aspects the natal Moon or Lagna, "
            "the obstruction is partially mitigated and the defeat may instead manifest "
            "as a narrow loss or a pyrrhic victory."
        ),
        synthesis_sources = [
            "gopal-ch4-election-dasha-timing",
            "gopal-ch4-election-spoiler-logic",
        ],
        severity  = "high",
        checkable = True,
    ),

]  # end GROUP_AX


# ═════════════════════════════════════════════════════════════════════════════
# GROUP AY — Indian Political Context (Gopal Ch 4)
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AY = [

    _rule(
        rule_id  = "mundane-gopal-ch4-indian-pm-lagna-bias",
        sub_type = "election_prediction",
        title    = "Indian PM Lagna Bias — Cancer/Taurus/Scorpio/Leo Historical Pattern",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF predicting the Indian national PM election "
            "AND a candidate has Lagna in Cancer, Taurus, Scorpio, or Leo "
            "→ Indian PM Lagna Bias modifier applied"
        ),
        result = (
            "Historical pattern: most successful Indian PMs with full terms and significant "
            "governance legacies have had Cancer, Taurus, Scorpio, or Leo as their Lagna. "
            "Apply +0.1 weight modifier to the overall Tri-Lagna strength coefficient "
            "for Indian national elections only. "
            "This is a contextual modifier, not a decisive factor — it tips the balance "
            "in very close comparative scores. "
            "Cancer: people-oriented, emotionally connected leadership. "
            "Taurus: stable, determined, land-connected. "
            "Scorpio: transformative, secretive, powerful. "
            "Leo: executive, authoritative, dramatic."
        ),
        synthesis_sources = [
            "gopal-ch4-election-case-studies",
            "gopal-ch4-tri-lagna-election-engine",
        ],
        severity  = "low",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch4-indian-pm-widowhood-rule",
        sub_type = "election_prediction",
        title    = "Indian PM Widowhood Rule — Saturn 10th Lord Favours Single/Widowed Candidates",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF predicting the Indian national PM election "
            "AND Saturn is the candidate's 10th lord (from any Tri-Lagna reference point) "
            "AND the candidate is widowed, unmarried, or living apart from spouse "
            "→ Indian PM Widowhood modifier applied"
        ),
        result = (
            "Weight modifier: +0.2 to overall Tri-Lagna strength coefficient for this "
            "candidate in Indian PM contests specifically. "
            "Gopalakrishnan identifies that Saturn as 10th lord in Indian politics historically "
            "favours candidates without active marital partnerships. "
            "Saturn demands sacrifice of personal/domestic life for public duty — "
            "candidates who have already made this sacrifice carry the saturnine mandate more fully. "
            "Validated: Nehru (widower from 1936), Vajpayee (never married), "
            "Modi (separated from wife before political career). "
            "This modifier applies ONLY to the Indian PM seat, not to state-level elections."
        ),
        synthesis_sources = [
            "gopal-ch4-election-case-studies",
            "gopal-ch4-tri-lagna-election-engine",
        ],
        severity  = "low",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch4-sonia-dramatic-change-trigger",
        sub_type = "election_prediction",
        title    = "Sonia Gandhi Dramatic Change Trigger — Saturn in Cancer + Cancer Lagna",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF Saturn is transiting Cancer "
            "AND the election frontrunner or incoming leader has Cancer as their natal Lagna "
            "→ Sonia Gandhi Dramatic Change Alert triggered"
        ),
        result = (
            "Dramatic Change Alert: The most powerful political office will see a dramatic "
            "transition before Saturn completes its transit through Cancer. "
            "This pattern — Saturn in Cancer + Cancer-Lagna candidate — signals a major "
            "regime shift that overturns pre-election expectations. "
            "Validated: 2004 Indian General Election — Saturn transiting Cancer, "
            "Sonia Gandhi (Cancer Lagna) became the pivot of a UPA coalition that "
            "unexpectedly ousted the Vajpayee BJP government despite pre-election BJP leads. "
            "Note: the Cancer-Lagna individual does not necessarily take the top office personally "
            "but acts as the catalyst for the transition."
        ),
        synthesis_sources = [
            "gopal-ch4-election-case-studies",
            "gopal-ch4-election-spoiler-logic",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-gopal-ch4-volatile-nomination-chart",
        sub_type = "election_prediction",
        title    = "Volatile Nomination Chart — 2+ Rasi Sandhi Planets = Candidacy Collapse Risk",
        source_chapter = "Gopal Ch 4 — How to Predict for Elections",
        condition = (
            "IF the nomination filing time chart (the moment a candidate files their nomination papers) "
            "has 2 or more planets at 0° or 29° of any sign (Rasi Sandhi) "
            "→ Volatile Nomination Chart flag triggered"
        ),
        result = (
            "Volatile: This candidacy is prone to sudden collapse or technical disqualification. "
            "The nomination chart acts as the 'birth chart' of the individual candidate's "
            "electoral quest. With 2+ planets at Rasi Sandhi (between worlds), "
            "the campaign lacks structural grounding. "
            "Risk manifestations: nomination rejected on technical grounds, legal challenge, "
            "party withdraws support before polling day, unexpected health event, "
            "or dramatic last-minute withdrawal. "
            "The candidacy may start strongly but carries an invisible fault line "
            "that will manifest at the worst possible moment."
        ),
        synthesis_sources = [
            "gopal-ch4-auxiliary-campaign-charts",
            "gopal-ch4-election-spoiler-logic",
        ],
        severity  = "medium",
        checkable = True,
    ),

]  # end GROUP_AY


# ═════════════════════════════════════════════════════════════════════════════
# GROUP AZ — Lord of Year Quality (Mehta Ch 22/23)
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AZ = [

    _rule(
        rule_id  = "mundane-mehta-ch22-mars-raja-year-of-sword",
        sub_type = "yearly_governance",
        title    = "Mars as Raja — Year of the Sword (War / Fire / Terrorism)",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF the weekday lord at Chaitra Shukla Pratipada (Hindu New Year) is Mars "
            "→ Mars is the Raja (King) for the year "
            "OR IF the weekday lord at Solar Ingress into Aries is Mars "
            "→ Mars is the Mantri (Minister) for the year"
        ),
        result = (
            "Year of the Sword declared. "
            "Classical outcomes: fighting between rulers, forest and urban fires, robberies, "
            "widespread bilious diseases, military aggression elevated. "
            "Modern calibration: significant global terrorism incidents, property destruction "
            "by fire, military confrontations, and armed conflict between nations. "
            "Security services will be stretched. Commodity prices for iron, copper, "
            "gold, and weapons will increase. "
            "All other cabinet forecasts this year are filtered through a Mars-hazard overlay."
        ),
        synthesis_sources = [
            "mehta-ch22-lord-of-year-engine",
            "mehta-ch22-yearly-cabinet-portfolios",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-jupiter-raja-golden-year",
        sub_type = "yearly_governance",
        title    = "Jupiter as Raja — Golden Year (Prosperity / Banking / Legal Welfare)",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Mars is the Raja for the year (unafflicted, not combust, not in Grahayudha) "
            "→ Jupiter prosperity activation "
            "IF Jupiter is also unafflicted in the Hindu New Year chart"
        ),
        result = (
            "Golden Year declared for banking, agriculture, and national prosperity. "
            "Classical outcomes: excellent crops, religious rituals, universal prosperity, "
            "abundant milk and honey, legal welfare, effective judiciary. "
            "Modern calibration: Banking and financial systems strengthen; "
            "Jupiter is the Karaka for banks — an unafflicted Jupiter Raja produces "
            "institutional financial stability. "
            "Exception/Veto: IF Jupiter is afflicted (combust/Grahayudha/debilitated) as Raja "
            "→ Fiscal Stability Warning: High probability of banking crisis or collapse "
            "of major financial institutions (reversed result)."
        ),
        synthesis_sources = [
            "mehta-ch22-lord-of-year-engine",
            "mehta-ch22-governance-portfolio-synthesis",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-jupiter-raja-afflicted-banking-crisis",
        sub_type = "yearly_governance",
        title    = "Afflicted Jupiter Raja — Banking Crisis / Institutional Collapse Warning",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Jupiter is the Raja (King) for the year "
            "AND Jupiter is afflicted (combust / debilitated / losing in Grahayudha "
            "/ aspected by Saturn or Mars without benefic protection) "
            "in the Hindu New Year chart "
            "→ Afflicted Jupiter Raja veto triggered"
        ),
        result = (
            "Fiscal Stability Warning: High probability of a banking crisis or collapse "
            "of a major financial institution during this year. "
            "Jupiter governs banks, judges, and the treasury in mundane analysis. "
            "When afflicted as the Raja, all beneficial Jupiter outcomes reverse: "
            "prosperity becomes financial distress, legal welfare becomes judicial corruption, "
            "crops become failures. "
            "Monitor for: bank runs, NBFC collapses, sovereign debt crises, "
            "major insurance fraud, or collapse of a prominent financial institution. "
            "Cross-check with Dhanesh (treasury portfolio holder) for confirmation."
        ),
        synthesis_sources = [
            "mehta-ch22-lord-of-year-engine",
            "mehta-ch22-governance-portfolio-synthesis",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-saturn-raja-famine-misery",
        sub_type = "yearly_governance",
        title    = "Saturn as Raja — Famine, Scarcity, and Societal Misery Year",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Saturn is the Raja (King) for the year "
            "→ Saturn governance tone year declared"
        ),
        result = (
            "Difficult year declared. "
            "Classical outcomes: poor rainfall, robber and criminal activity elevated, "
            "sinful and corrupt acts normalized, destruction of crops, general societal misery. "
            "Modern calibration: mass strikes, austerity measures, food shortages, "
            "administrative frustration, heavy industry and labour unrest. "
            "Validated: 1991 India (Saturn Raja year) — massive strikes, "
            "food shortages, economic austerity (IMF bailout), administrative paralysis. "
            "Amplifier: IF Mars also conjuncts Saturn in the New Year chart → "
            "'Governance Disaster Alert: Theft, epidemics, and violent leadership transitions.' "
            "The Saturn Raja is the most consistently negative of the malefic King signals "
            "due to Saturn's grinding, long-duration affliction pattern."
        ),
        synthesis_sources = [
            "mehta-ch22-lord-of-year-engine",
            "mehta-ch22-yearly-cabinet-portfolios",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-sun-raja-2001-validation",
        sub_type = "yearly_governance",
        title    = "Sun as Raja — Corruption Exposés / Fire Disaster / Institutional Failure",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Sun is the Raja (King) for the year "
            "→ Sun governance tone year declared"
        ),
        result = (
            "Mixed/hazardous year declared. "
            "Classical outcomes: mentally disturbed rulers, danger by fire and theft, "
            "unusual heat, scarce food, destructive wars, death of a senior leader. "
            "Modern calibration: high-level government corruption exposés, "
            "institutional/financial scheme collapses, major fire or heat disasters. "
            "Validated: 2001 India (Sun Raja year): "
            "(1) Gujarat Earthquake — massive death toll, "
            "(2) Tehelka sting operation — government corruption scandal, "
            "(3) US-64 mutual fund scheme collapse — institutional financial failure. "
            "All three outcomes align precisely with classical Sun-Raja predictions. "
            "Combustion veto applies: if Sun is combust (any planet within 8°) — impossible here "
            "as Sun cannot be combust to itself, but if Sun is afflicted by Saturn/Rahu in the "
            "New Year chart, severity escalates."
        ),
        synthesis_sources = [
            "mehta-ch22-lord-of-year-engine",
            "mehta-ch22-yearly-cabinet-portfolios",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-moon-raja-prosperity-affliction",
        sub_type = "yearly_governance",
        title    = "Moon as Raja — Prosperity or National Pain (Depends on Moon Condition)",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Moon is the Raja (King) for the year "
            "→ check Moon's condition in the Hindu New Year chart: "
            "Unafflicted Moon = Prosperity gate; Afflicted Moon = National Pain gate"
        ),
        result = (
            "UNAFFLICTED Moon Raja: Prosperity declared — "
            "plenty of rain and food, joy and mirth, flourishing vegetation, "
            "prosperous and happy citizenry, healthcare measures succeed. "
            "Social harmony is the year's dominant tone. "
            "AFFLICTED Moon Raja (aspected by Saturn/Rahu/Mars, or combust, or in Grahayudha): "
            "National Pain declared — "
            "internal insurgencies elevated, naxalism or separatist activity rises, "
            "mass public mental health crises, emotional trauma at national scale "
            "(floods, displacement, family breakdown). "
            "The Moon's condition in the New Year chart is the decisive switch between "
            "the year's two possible outcomes — always verify before forecasting."
        ),
        synthesis_sources = [
            "mehta-ch22-lord-of-year-engine",
            "mehta-ch22-yearly-cabinet-portfolios",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-combustion-veto-reversal",
        sub_type = "yearly_governance",
        title    = "Combustion Veto — Combust or Grahayudha-Lost Raja Reverses All Benefic Results",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF the Raja (King) planet for the year is combust "
            "(within 8° of Sun for planets other than Sun itself) "
            "OR loses in Grahayudha (Planetary War — within 1° of another planet, "
            "the losing planet has a lower degree) "
            "in the Hindu New Year chart "
            "→ Combustion Veto triggered"
        ),
        result = (
            "All beneficial results for this planet's Raja year are REVERSED to their "
            "calamitous opposites. "
            "Jupiter combust as Raja → banking failures instead of banking prosperity. "
            "Venus combust as Raja → luxury inflation instead of abundance. "
            "Mercury combust as Raja → media chaos and misinformation instead of clarity. "
            "Moon combust as Raja → triggers automatic National Pain gate (see Moon Raja rule). "
            "This is the most powerful single veto in the Yearly Cabinet system — "
            "a combust Raja poisons the entire year's governance forecast. "
            "Cross-check in the Hindu New Year chart before finalising any annual forecast."
        ),
        synthesis_sources = [
            "mehta-ch22-lord-of-year-engine",
            "mehta-ch22-governance-portfolio-synthesis",
        ],
        severity  = "critical",
        checkable = True,
    ),

]  # end GROUP_AZ


# ═════════════════════════════════════════════════════════════════════════════
# GROUP BA — Cabinet Pair Diagnostics (Mehta Ch 22/23)
# ═════════════════════════════════════════════════════════════════════════════

GROUP_BA = [

    _rule(
        rule_id  = "mundane-mehta-ch22-raja-mantri-enemy-deadlock",
        sub_type = "yearly_governance",
        title    = "Raja-Mantri Enemy Pair — Administrative Policy Deadlock",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF the Raja (King) and Mantri (Minister) for the year are natural planetary enemies "
            "(Sun-Saturn, Moon-Rahu, Mars-Mercury, Jupiter-Mercury adversarial pairing, "
            "or Venus-Jupiter tension pair) "
            "→ Raja-Mantri enemy configuration triggered"
        ),
        result = (
            "Administrative Alert: High probability of policy deadlock and cabinet bickering "
            "throughout the year. "
            "The executive (Raja) and the implementation layer (Mantri) are working against "
            "each other at a fundamental level. "
            "Governance appears active on the surface but produces little durable output. "
            "Key bills are stalled, projects are announced but not executed, "
            "and the ruling coalition expends energy in internal disputes. "
            "Public perception: ineffective government despite claimed effort. "
            "Severity elevated if the enemy pair also aspect each other in the New Year chart."
        ),
        synthesis_sources = [
            "mehta-ch22-yearly-cabinet-portfolios",
            "mehta-ch22-governance-portfolio-synthesis",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-golden-year-jupiter-venus",
        sub_type = "yearly_governance",
        title    = "Jupiter Raja + Venus Mantri — Golden Year National Prosperity",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Raja (King) for the year is Jupiter "
            "AND Mantri (Minister) for the year is Venus "
            "AND Jupiter is unafflicted in the Hindu New Year chart "
            "→ Golden Year compound signal triggered"
        ),
        result = (
            "Golden Year Forecast: Exceptional national wealth, bumper agricultural output, "
            "and societal peace predicted for the year. "
            "Jupiter-Venus is the most auspicious Raja-Mantri pairing in the Celestial Cabinet. "
            "Jupiter (prosperity, justice, religion) governs the year's destiny; "
            "Venus (abundance, culture, luxury) implements it at the administrative level. "
            "Expected outcomes: record crop yields, strong financial markets, "
            "diplomatic successes, cultural and arts boom, positive balance of payments. "
            "Caveat: Combustion Veto applies — if either planet becomes combust in the "
            "New Year chart, the golden forecast is partially or fully cancelled."
        ),
        synthesis_sources = [
            "mehta-ch22-governance-portfolio-synthesis",
            "mehta-ch22-lord-of-year-engine",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-saturn-dhanesh-treasury-depletion",
        sub_type = "yearly_governance",
        title    = "Saturn as Dhanesh + Mars Aspect — National Treasury Depletion",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Saturn is the Dhanesh (Lord of Treasury, appointed at Sun's entry into Virgo) "
            "AND Mars aspects Saturn in the New Year chart (or within the Dhanesh appointment chart) "
            "→ Treasury Depletion alert triggered"
        ),
        result = (
            "Fiscal Stability Warning: Paucity of national funds predicted for the year. "
            "Scholars, accountants, and financial sector workers suffer. "
            "Saturn as treasury lord already produces conservative, restricted, slow-moving "
            "national finances. Mars's aspect adds aggressive expenditure pressure — "
            "specifically military spending, fire-related infrastructure damage, "
            "or forced crisis spending that depletes reserves. "
            "The combination of Saturn's contraction and Mars's aggressive drain creates "
            "a treasury under maximum pressure. "
            "Monitor: government bond yields, fiscal deficit widening, sovereign ratings action."
        ),
        synthesis_sources = [
            "mehta-ch22-governance-portfolio-synthesis",
            "mehta-ch22-yearly-cabinet-portfolios",
        ],
        severity  = "high",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-saturn-durgesh-defense-humiliation",
        sub_type = "yearly_governance",
        title    = "Saturn as Durgesh in 12th — National Defense Humiliation / Territorial Loss",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Saturn is the Durgesh (Lord of Defense, appointed at Sun's entry into Leo) "
            "AND Saturn is placed in the 12th house of the Hindu New Year chart "
            "→ Defense Vulnerability critical alert triggered"
        ),
        result = (
            "Critical Defense Alert: Risk of national humiliation by enemies "
            "and potential loss of territorial integrity. "
            "Durgesh governs the national security apparatus — army, navy, police, "
            "border security, and fortress defense. "
            "Saturn in the 12th house directs the defense portfolio toward 'loss, "
            "expenditure without return, and hidden enemies.' "
            "The combined signal: the nation's defensive capacity is being eroded from within "
            "or from concealed adversaries. "
            "This is the strongest defense-failure signal in the annual cabinet system. "
            "Validate against current geopolitical context before publishing."
        ),
        synthesis_sources = [
            "mehta-ch22-governance-portfolio-synthesis",
            "mehta-ch22-yearly-cabinet-portfolios",
        ],
        severity  = "critical",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-anarchy-gate-sun-raja-saturn-mantri",
        sub_type = "yearly_governance",
        title    = "Anarchy Gate — Sun Raja + Saturn Mantri = High-Level Leadership Mortality",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Raja (King) for the year is Sun "
            "AND Mantri (Minister) for the year is Saturn "
            "→ Anarchy Gate triggered"
        ),
        result = (
            "Systemic Instability Warning: Cruel administrative behavior and "
            "high-level leader mortality predicted for this year. "
            "The Sun-Saturn combination at the Raja-Mantri level is the most dangerous "
            "executive configuration in the annual cabinet system. "
            "Sun represents the head of state; Saturn represents obstruction, mortality, "
            "and structural breakdown. When Saturn implements the Sun's executive mandate, "
            "it does so with cruelty, bureaucratic rigidity, and ultimately — "
            "in extreme cases — physical harm to the leadership itself. "
            "Historical pattern: years with this configuration have seen assassination attempts, "
            "sudden deaths of sitting leaders, or abrupt forced removal from power."
        ),
        synthesis_sources = [
            "mehta-ch22-governance-portfolio-synthesis",
            "mehta-ch22-lord-of-year-engine",
        ],
        severity  = "critical",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-mercury-dhanesh-it-boom",
        sub_type = "yearly_governance",
        title    = "Mercury as Dhanesh — IT, BPO, and Publishing Sector Boom",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Mercury is the Dhanesh (Lord of Treasury/Commerce, appointed at Sun's entry into Virgo) "
            "AND Mercury is unafflicted in the Dhanesh appointment chart "
            "→ Mercury Dhanesh IT boom signal triggered"
        ),
        result = (
            "Information Technology and Publishing Sector Boom declared for this year. "
            "Classical Dhanesh-Mercury outcomes: farmers earn well, business rituals observed, "
            "financial markets stable. "
            "Modern 21st-century calibration (Mehta modernization override): "
            "Mercury as treasury lord maps to IT, BPO, communications, and publishing industries. "
            "These sectors will outperform the broad market during this annual cycle. "
            "Additionally: Mercury Durgesh (defense lord) = Naval and Communication Intelligence "
            "strengthening — cyber-defense and signal intelligence investments increase. "
            "Use for sector rotation guidance in equity market analysis."
        ),
        synthesis_sources = [
            "mehta-ch22-governance-portfolio-synthesis",
            "mehta-ch22-yearly-cabinet-portfolios",
        ],
        severity  = "medium",
        checkable = True,
    ),

    _rule(
        rule_id  = "mundane-mehta-ch22-winter-prosperity-dhanyesh-meghesh",
        sub_type = "yearly_governance",
        title    = "Jupiter Dhanyesh + Moon Meghesh — Exceptional Winter Harvest and Rain",
        source_chapter = "Mehta Ch 22 — Yearly Governance Engine",
        condition = (
            "IF Jupiter is the Dhanyesh (Lord of Winter Crops, appointed at Sun's entry into Sagittarius) "
            "AND Moon is the Meghesh (Lord of Rain/Clouds, appointed at Sun's entry into Ardra Nakshatra) "
            "AND both are unafflicted "
            "→ Winter Prosperity compound signal triggered"
        ),
        result = (
            "National Forecast: Exceptional winter harvest and abundant water resources predicted. "
            "Jupiter as Dhanyesh: wheat and rice plentiful, religious activities increase, "
            "winter grains freely available. "
            "Moon as Meghesh: copious and timely rain, social harmony, public amenities increase. "
            "Together: this is the strongest agricultural prosperity signal in the annual "
            "cabinet system — adequate water + bumper winter grains + societal contentment. "
            "India specifically benefits from a strong Rabi (winter) crop with this combination. "
            "Monitor: food inflation will likely decrease; rural income and consumption "
            "will increase; water-intensive industries (hydropower, beverages) benefit."
        ),
        synthesis_sources = [
            "mehta-ch22-governance-portfolio-synthesis",
            "mehta-ch22-yearly-cabinet-portfolios",
        ],
        severity  = "medium",
        checkable = True,
    ),

]  # end GROUP_BA


# ─────────────────────────────────────────────────────────────────────────────
ALL_RULES = GROUP_AX + GROUP_AY + GROUP_AZ + GROUP_BA
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
    print(f"[v19 interp] Upserted {ok}/{len(ALL_RULES)} rules → interpretation_rules ✓")


if __name__ == "__main__":
    asyncio.run(run())
