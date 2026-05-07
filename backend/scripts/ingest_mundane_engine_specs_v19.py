"""
Mundane Astrology — Engine Specs INGEST v19
===========================================
Batch : mundane-engine-v19-20260507
Collection : mundane_engine_specs
Science    : mundane_jyotish

Chapters encoded:
  Gopal Ch 4  — How to Predict for Elections
                Tri-Lagna Comparative Engine (Lagna / Chandra / Karkamsha)
                Data Authenticity Protocol
                Spoiler Logic (Rasi Sandhi veto, 6th lord nexus, 8th house Saturn)
                Dasha/Bhukti Timing Vectors (11th house surge, winning/losing lords)
                Auxiliary Campaign Timing Charts (announcement, nomination, manifesto)
                Election Case Studies (Bush/Gore 2000, Bush/Kerry 2004, Vajpayee/Sonia 2004)

  Mehta Ch 22/23 — Yearly Governance Engine
                   10-Portfolio Celestial Cabinet (complete 7-planet result matrix)
                   Lord of Year qualitative results (all 7 planets as Raja)
                   Governance Portfolio Results (Mantri, Sasyesh, Rasesh, Neersesh,
                   Dhanyesh, Meghesh, Phalesh, Dhanesh, Durgesh — all 7 planets)
                   Modernization mapping (Mercury=IT, Jupiter=Banking, Venus=Telecom)

Note: Mehta Ch 19-21 (War / Terrorism / Assassinations) were encoded in v5–v11.
      Ch 22/23 expands the v3 Celestial Council spec with the full 7-planet
      qualitative result matrix for each portfolio (v3 had only role assignments).

DRY_RUN = True  →  set False (or use run_mundane_ingest.py) to write to MongoDB.
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

_BATCH = "mundane-engine-v19-20260507"
_NOW   = datetime.now(timezone.utc).isoformat()

def _spec(spec_id, spec_type, title, source, description, **fields):
    doc = {
        "spec_id":    spec_id,
        "spec_type":  spec_type,
        "science_id": "mundane_jyotish",
        "batch_id":   _BATCH,
        "title":      title,
        "source":     source,
        "description": description,
        "created_at": _NOW,
    }
    doc.update(fields)
    return doc


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 1 — Gopal Ch 4: Tri-Lagna Comparative Election Engine
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH4_TRI_LAGNA_ENGINE = _spec(
    spec_id   = "gopal-ch4-tri-lagna-election-engine",
    spec_type = "comparative_analysis_engine",
    title     = "Tri-Lagna Election Engine — Gopalakrishnan Ch 4",
    source    = "gopalakrishnan_ch4",
    description = (
        "Gopalakrishnan Ch 4 establishes the primary technical framework for election "
        "prediction: comparing the 10th lord strength of two competing candidates across "
        "three distinct Lagna reference points. The candidate with the higher frequency of "
        "strong 10th lords across Lagna, Chandra Lagna, and Karkamsha Lagna wins. "
        "This triangulated approach accounts for physical power, public perception, and "
        "destiny/soul-mandate — compensating for the frequent inaccuracy of birth data."
    ),
    tri_lagna_reference_points = {
        "lagna_ascendant": (
            "Measures the candidate's executive capability, party organisation support, "
            "and ability to project physical authority and administrative competence."
        ),
        "chandra_lagna_moon_sign": (
            "Measures public swing, popular appeal, and how the candidate is perceived "
            "by the electorate in opinion polls and ground-level sentiment."
        ),
        "karkamsha_lagna_soul_point": (
            "Measures the ultimate destiny and fate of the candidate — the 'divine mandate' "
            "dimension. The strongest Karkamsha 10th lord indicates the candidate marked "
            "by fate for high office, regardless of immediate political conditions."
        ),
    },
    tenth_lord_strength_metrics = {
        "strong_placements": [
            "Exaltation (Uchcha)",
            "Own sign (Swa Rashi)",
            "11th house (Gains / Labha)",
            "9th house (Trikona / Fortune)",
            "1st house (Lagna / Self — if aspecting 10th)",
            "Vargottama (same sign in Navamsha)",
        ],
        "weak_placements": [
            "Debilitation (Neecha)",
            "6th house (enemies / disease)",
            "8th house (obstruction / hidden forces)",
            "12th house (loss / hidden)",
            "3rd house (effort / valour — indicates fighting but not winning)",
            "Rasi Sandhi (0° or 29° of sign — full spoiler veto)",
        ],
        "strength_coefficients": {
            "raja_yoga_presence": 0.40,
            "tenth_lord_in_eleventh": 0.35,
            "tenth_lord_in_trikona": 0.25,
        },
    },
    winning_condition = (
        "Candidate with the HIGHER FREQUENCY of strong 10th lords across 2 or more of the "
        "three reference points is the predicted winner. "
        "Tie-breaker: Karkamsha Lagna 10th lord quality takes precedence as the destiny indicator."
    ),
    data_authenticity_protocol = (
        "Before any election prediction is run, the candidate's chart must be verified against "
        "3 major life events (career peaks, setbacks, family milestones). "
        "If Dasha/Bhukti does not match known events, the chart must be rejected: "
        "'Data Unreliable — Birth-time rectification required before prediction.' "
        "Source notes that 8 out of 10 celebrity horoscopes in published books contain "
        "incorrect birth data. The 80% error rate makes authenticity verification mandatory."
    ),
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 2 — Gopal Ch 4: Spoiler Logic (Vetoes and Failure Triggers)
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH4_SPOILER_LOGIC = _spec(
    spec_id   = "gopal-ch4-election-spoiler-logic",
    spec_type = "veto_logic_engine",
    title     = "Election Spoiler Logic — Rasi Sandhi, 6th Lord Nexus, 8th Saturn",
    source    = "gopalakrishnan_ch4",
    description = (
        "Even a candidate with a strong 10th lord can lose through specific spoiler "
        "configurations. Gopalakrishnan Ch 4 identifies three critical failure triggers that "
        "override normal strength calculations. Each is an automatic veto that signals "
        "defeat regardless of the Tri-Lagna comparative score."
    ),
    spoiler_vetoes = {
        "01_rasi_sandhi_veto": {
            "definition": (
                "10th lord placed at 0° or 29° of a sign (Rasi Sandhi / sign junction). "
                "The planet is 'between worlds' — unable to deliver its significations effectively."
            ),
            "trigger_rule": "IF 10th Lord Degree < 1° OR > 29° THEN Veto = 'Critical Failure Warning'",
            "effect": (
                "Negates even a strong 10th lord placement. The candidate has the capability "
                "to win but a structural fault prevents them from 'crossing the finish line.' "
                "High probability of losing a close contest, narrow margin defeat, or technical "
                "disqualification."
            ),
            "validation": "Kerry 2004 — 10th lord in 2nd house at Rasi Sandhi; lost despite strong Lagna placement.",
        },
        "02_sixth_lord_nexus": {
            "definition": (
                "10th lord conjunct or aspected by the 6th lord (enemies, opposition, obstacles). "
                "The career/authority indicator is contaminated by the house of opposition."
            ),
            "trigger_rule": "IF 10th Lord is conjunct 6th Lord OR receives 6th Lord aspect THEN Veto = 'Defeat by Opposition Intrigue'",
            "effect": (
                "Candidate loses power through opposition manoeuvring, legal challenges, "
                "or internal party betrayal. The defeat is NOT a direct electoral loss — "
                "it is engineered by adversaries exploiting a structural weakness in the "
                "candidate's chart."
            ),
        },
        "03_eighth_house_saturn": {
            "definition": (
                "Saturn in the 8th house at the time of the election cycle "
                "(either natal or by transit over natal 8th house)."
            ),
            "trigger_rule": "IF Saturn occupies 8th house during election cycle THEN Veto = 'Sudden Fall or Unexpected Withdrawal'",
            "effect": (
                "Indicates a sudden, unexpected reversal: health crisis, scandal, forced "
                "withdrawal, or an unforeseen event that removes the candidate from contention. "
                "The fall arrives from an entirely unanticipated direction — not from the "
                "visible political opponent."
            ),
        },
    },
    incumbent_vulnerability_trigger = {
        "rule": (
            "IF (Running Dasha == 8th Lord) AND (10th Lord is in 3rd house) "
            "THEN 'Incumbency Warning: High risk of being ousted by a new political force'."
        ),
        "logic": (
            "The 8th lord Dasha signifies hidden transformation and upheaval. "
            "When the 10th lord (career) is simultaneously in the 3rd house (effort, valour), "
            "the incumbent is fighting hard but without the structural backing of a strong "
            "10th house. A new 'star' in the opposition will outshine them."
        ),
        "validation": "TDP 2004 case — incumbent running 8th lord Dasha with 10th lord in 3rd; lost to new wave.",
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 3 — Gopal Ch 4: Dasha/Bhukti Timing Vectors
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH4_DASHA_TIMING = _spec(
    spec_id   = "gopal-ch4-election-dasha-timing",
    spec_type = "timing_engine",
    title     = "Election Dasha/Bhukti Timing Vectors — Winning and Losing Period Lords",
    source    = "gopalakrishnan_ch4",
    description = (
        "Gopalakrishnan Ch 4 provides Dasha/Bhukti fine-tuning vectors that function as "
        "secondary confirmations after the Tri-Lagna comparison. The period lords running "
        "at the time of polling provide the final swing factor — a strong Tri-Lagna score "
        "can be neutralised by a losing Dasha, and a moderate score can be elevated by a "
        "Raja Yoga Dasha."
    ),
    winning_dasha_vectors = [
        "Dasha/Bhukti of a planet in the 11th house (Labha/Gains) from Lagna or Moon — "
        "'Winning Momentum' coefficient = 0.90. Validated: Bush Saturn/Rahu — Rahu in 11th.",
        "Dasha/Bhukti of a planet involved in a Raja Yoga (mutual aspect/conjunction of "
        "Kendra and Trikona lords).",
        "Dasha/Bhukti of the exalted 10th lord.",
        "Antara (sub-sub-period) of a planet in the 9th or 11th house — 'Raja Yoga Antara' "
        "gives final victory in a close race.",
    ],
    losing_dasha_vectors = [
        "Dasha/Bhukti of the 6th, 8th, or 12th lords.",
        "Dasha/Bhukti of a debilitated planet.",
        "Dasha/Bhukti of a planet in Rasi Sandhi.",
        "Dasha/Bhukti of the 3rd lord (effort without reward — fighting but not winning).",
    ],
    saturn_transit_veto = {
        "rule_1": (
            "IF Saturn transits natal Saturn position (Saturn Return) → "
            "'Major political change / regime end'. Career transformation — not necessarily defeat."
        ),
        "rule_2": (
            "IF Saturn transits 8th house from natal Moon or Lagna → "
            "'Defeat Likely'. The 8th transit of Saturn is the classical Ashtama Shani "
            "— maximum obstruction and exhaustion of vitality."
        ),
        "rule_3": (
            "IF Saturn transits natal 10th house from Moon → "
            "'Incumbency Test'. The government or leader is being judged. Benefic Saturn "
            "dispositor = survives. Malefic Saturn dispositor = voted out."
        ),
    },
    destiny_anchor_rule = {
        "rule": (
            "IF the 10th Lord is conjunct or aspected by a Trikona lord (1st/5th/9th) "
            "in the Karkamsha Lagna THEN 'Destiny Alert: Candidate is marked for high office by fate'."
        ),
        "weight_modifier": "+0.30 to overall strength coefficient",
        "logic": (
            "The Karkamsha is the soul-point Lagna — it shows destiny at the deepest level. "
            "A Trikona connection with the 10th lord here indicates that the divine mandate "
            "for leadership is present regardless of immediate transits or opposition strength."
        ),
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 4 — Gopal Ch 4: Auxiliary Campaign Timing Charts
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH4_CAMPAIGN_CHARTS = _spec(
    spec_id   = "gopal-ch4-auxiliary-campaign-charts",
    spec_type = "event_chart_engine",
    title     = "Auxiliary Campaign Event Charts — Announcement, Nomination, Manifesto",
    source    = "gopalakrishnan_ch4",
    description = (
        "Gopalakrishnan Ch 4 introduces a multi-event timing matrix where the exact moment "
        "of key campaign events acts as a 'birth chart' for that specific dimension of the "
        "candidate's electoral quest. These auxiliary charts are used as transit filters over "
        "the candidate's natal chart and the Tri-Lagna engine output."
    ),
    campaign_event_charts = {
        "election_announcement_time": {
            "description": (
                "The moment the election commission or head of state announces the election date. "
                "Sets the general public mood and overall reception of the entire election cycle."
            ),
            "key_indicators": [
                "Lagna lord dignity — strong = engaged electorate, weak = voter apathy",
                "Moon sign at announcement — public enthusiasm vs. cynicism",
                "2nd/11th lord connection — financial interest in the outcome",
                "Malefics in 1st/7th axis — polarised, divisive election cycle",
            ],
        },
        "nomination_filing_time": {
            "description": (
                "The exact time a candidate files their nomination papers. "
                "The 'birth chart' of the individual candidate's quest for office. "
                "Indicates if the candidacy will face disqualification, legal hurdles, "
                "or a smooth passage to the ballot."
            ),
            "key_indicators": [
                "8th house empty = no technical obstacles to candidacy",
                "2+ planets in Rasi Sandhi = volatile candidacy prone to sudden collapse",
                "Lagna lord in 11th = candidacy accepted; strong electoral position",
                "6th lord prominent = candidacy contested; court challenges expected",
            ],
            "rasi_sandhi_veto_threshold": (
                "IF 2+ planets at 0°/29° in nomination chart → "
                "'Volatile: Prone to sudden collapse or technical disqualification'."
            ),
        },
        "manifesto_unveiling_time": {
            "description": (
                "The time the political party releases its election manifesto / platform. "
                "Determines the persuasive power and long-term impact of the party's promises. "
                "A strong manifesto chart generates 'news cycle dominance'."
            ),
            "key_indicators": [
                "2nd + 3rd lord connection = high persuasive communication impact",
                "Mercury strong = manifesto dominates intellectual debate",
                "Jupiter prominent = credibility and public trust in promises",
                "Saturn afflicted = manifesto seen as unrealistic or undeliverable",
            ],
            "manifesto_impact_rule": (
                "IF 2nd lord and 3rd lord are connected (conjunction/aspect) in manifesto chart → "
                "'Campaign Sentiment: High persuasive impact; manifesto dominates news cycle'."
            ),
        },
    },
    synthesis_note = (
        "No campaign prediction is complete without cross-referencing all three auxiliary "
        "charts with the candidate's natal Tri-Lagna engine output. "
        "A strong natal score + weak nomination chart = win probable but contested. "
        "A weak natal score + strong manifesto chart = public buzz without victory."
    ),
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 5 — Gopal Ch 4: Election Case Studies
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH4_CASE_STUDIES = _spec(
    spec_id   = "gopal-ch4-election-case-studies",
    spec_type = "historical_validation_database",
    title     = "Election Case Studies — Bush/Gore 2000, Bush/Kerry 2004, Vajpayee/Sonia 2004",
    source    = "gopalakrishnan_ch4",
    description = (
        "Gopalakrishnan Ch 4 provides three validated election case studies that establish "
        "the empirical foundation for the Tri-Lagna engine and spoiler logic. Each case "
        "demonstrates a specific pattern that generalises to future predictions."
    ),
    case_studies = {
        "usa_2000_bush_vs_gore": {
            "context": "US Presidential Election, November 2000",
            "george_bush_analysis": {
                "lagna_10th_lord": "11th house — Strong (Labha/Gains position)",
                "moon_10th_lord": "11th house — Raja Yoga (double 11th confirmation)",
                "karkamsha_10th_lord": "7th house with Trikona lord — Raja Yoga",
                "dasha_at_election": "Saturn/Rahu — Rahu in 11th from Lagna (Winning Momentum 0.90)",
                "tri_lagna_score": "3/3 reference points strong",
                "result": "Winner (confirmed)",
            },
            "al_gore_analysis": {
                "lagna_10th_lord": "3rd house — Weak (effort without executive backing)",
                "moon_10th_lord": "6th house — Debilitated (Neecha)",
                "tri_lagna_score": "0/2 reference points strong",
                "result": "Loser (confirmed)",
            },
            "generalised_rule": (
                "Candidate with 10th lord in 11th house across BOTH Lagna and Chandra Lagna "
                "simultaneously — especially when the concurrent Dasha lord is also in 11th — "
                "has near-certain electoral victory."
            ),
        },
        "usa_2004_bush_vs_kerry": {
            "context": "US Presidential Election, November 2004",
            "john_kerry_analysis": {
                "lagna_10th_lord": "1st house — Adequate (self-focused, not outward-winning)",
                "moon_10th_lord": "2nd house at RASI SANDHI — Spoiler triggered",
                "karkamsha_10th_lord": "4th house with 6th lord — Weakness (opposition contamination)",
                "tri_lagna_score": "0/3 effective (Rasi Sandhi negates 1st house placement)",
                "result": "Loser (confirmed)",
            },
            "generalised_rule": (
                "The Rasi Sandhi Spoiler Veto applies even when the 10th lord is in a "
                "nominally acceptable house. Kerry's 10th lord in 2nd appeared workable, "
                "but its Sandhi position nullified the placement entirely. "
                "Always check degree before assessing house placement."
            ),
        },
        "india_2004_vajpayee_vs_sonia": {
            "context": "Indian General Election, April-May 2004",
            "vajpayee_analysis": {
                "10th_lord_in_3rd": "Indicates valour and effort — the fight is on — but not executive victory",
                "8th_house_saturn": "Saturn in 8th at election time = sudden unexpected reversal",
                "dasha_period": "Running 8th lord Dasha (obstruction/transformation period)",
                "result": "Lost unexpectedly despite pre-election projections of victory",
            },
            "sonia_gandhi_stability_trigger": {
                "rule": (
                    "Saturn transiting Cancer + Sonia Gandhi has Cancer Lagna → "
                    "'Dramatic Change Alert: Most powerful office will see a dramatic transition "
                    "before Saturn leaves Cancer'."
                ),
                "result": "BJP ousted; Congress-led UPA formed (Saturn in Cancer confirmed transition)",
            },
            "generalised_rule": (
                "8th house Saturn in an election chart is a near-certain sudden-reversal signal "
                "for the candidate with that placement, regardless of pre-election polling leads. "
                "The fall arrives from an unanticipated direction."
            ),
        },
    },
    indian_political_lagna_bias = {
        "favourable_lagnas_for_indian_pm": ["Cancer", "Taurus", "Scorpio", "Leo"],
        "weight_modifier": "+0.1 to overall strength coefficient for Indian national elections",
        "rationale": (
            "Historical pattern from Indian political analysis: most successful Indian national "
            "leaders (PMs with full terms and significant legacies) have had these four Lagnas. "
            "Cancer (Moon-ruled, people-oriented), Taurus (Venus-stability), "
            "Scorpio (power, transformation), Leo (executive authority)."
        ),
        "widowhood_rule_india": {
            "rule": (
                "For the Indian Prime Minister's seat specifically, Saturn as 10th lord "
                "favours candidates without spouses (widowed, unmarried, or living apart). "
                "Apply +0.2 weight modifier for unmarried/widowed candidates in Indian PM contests."
            ),
            "validation": "Nehru (widower), Vajpayee (unmarried), Modi (separated) — Saturn as 10th lord common thread.",
        },
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 6 — Mehta Ch 22: Yearly Cabinet Portfolios (Complete 7-Planet Matrix)
# ═════════════════════════════════════════════════════════════════════════════
MEHTA_CH22_CABINET_PORTFOLIOS = _spec(
    spec_id   = "mehta-ch22-yearly-cabinet-portfolios",
    spec_type = "multi_factor_lookup",
    title     = "Yearly Celestial Cabinet — 10 Portfolios × 7 Planets (Mehta Ch 22)",
    source    = "mehta_ch22",
    description = (
        "Mehta Ch 22 provides the complete Celestial Cabinet matrix: 10 governance portfolios "
        "with their selection rules (which weekday lord at which solar/lunar event) and "
        "the qualitative results for all 7 planets in each role. "
        "This expands the v3 Celestial Council spec (which encoded role assignments only) "
        "with the full 7-planet qualitative result matrix for each portfolio."
    ),
    portfolio_selection_rules = {
        "01_raja_king": {
            "selection": "Weekday lord when Chaitra Shukla Pratipada (1st Tithi of Hindu New Year) begins",
            "controversy_veto": "If Tithi and weekday overlap, use lord of the moment the Tithi begins",
            "governs": "National destiny — the year's primary macro tone",
        },
        "02_mantri_minister": {
            "selection": "Weekday lord at exact moment of Solar Ingress into Aries",
            "governs": "Administrative implementation and policy execution",
        },
        "03_sasyesh_summer_crops": {
            "selection": "Weekday lord at Sun's entry into Cancer",
            "governs": "Summer grain productivity and livestock health",
        },
        "04_durgesh_defense": {
            "selection": "Weekday lord at Sun's entry into Leo",
            "governs": "National security, forts, army, and internal law enforcement",
        },
        "05_dhanesh_treasury": {
            "selection": "Weekday lord at Sun's entry into Virgo",
            "governs": "National exchequer, commercial trade, financial reserves",
        },
        "06_dhanyesh_winter_crops": {
            "selection": "Weekday lord at Sun's entry into Sagittarius",
            "governs": "Winter grain reserves and livestock stability",
        },
        "07_ardhapati_prices": {
            "selection": "Weekday lord at Sun's entry into Gemini",
            "governs": "Market price levels (high-low commodity indices)",
        },
        "08_meghesh_rain": {
            "selection": "Weekday lord at Sun's entry into Ardra Nakshatra",
            "governs": "Rainfall, monsoon quality, water resources",
        },
        "09_rasesh_juices": {
            "selection": "Weekday lord at Sun's entry into Libra",
            "governs": "Dairy, juices, sweet substances, pharmaceutical fluids",
        },
        "10_phalesh_fruits": {
            "selection": "Weekday lord at Sun's entry into Pisces",
            "governs": "Fruits, flowers, horticulture, and luxury food produce",
        },
    },
    cabinet_result_matrix = {
        "raja_king": {
            "sun":     "Insufficient rain; danger of theft; death of a senior leader; poor produce.",
            "moon":    "Good crops; harmony; prestige for rulers; effective health measures.",
            "mars":    "Wars, fire accidents, increased theft, and bilious diseases. Year of the Sword.",
            "mercury": "Justice, intellectual growth, media prominence, and administrative clarity.",
            "jupiter": "Universal prosperity, banking stability, legal welfare, and religious activities.",
            "venus":   "Bumper sugarcane/rice harvest; victory in battle; cultural and film world boom.",
            "saturn":  "Poor rain, famine, robber activity, and general societal misery.",
        },
        "mantri_minister": {
            "sun":     "Bitterness among rulers; high-level corruption exposés; scarcity of harvest.",
            "moon":    "Development projects completed; prosperity; general well-being and health.",
            "mars":    "Rise in unrighteous acts; milk scarcity; trouble by weapons or fire.",
            "mercury": "Improved living conditions; family harmony; but distress from storms.",
            "jupiter": "Rulers busy in welfare; excellent crops; universal joy.",
            "venus":   "Female supremacy established; celebrity marriages; expensive grains.",
            "saturn":  "Cruel behavior of rulers; dissatisfaction among the masses.",
        },
        "sasyesh_summer_crops": {
            "sun":     "Expensive summer grains; short cattle fodder supply; incidents of theft.",
            "moon":    "Sufficient rain; abundant milk and wealth; general comfort.",
            "mars":    "Summer crops (barley/wheat) damaged; animal diseases; irregular rain.",
            "mercury": "Excellent crop yield; sufficient rain; infrastructure projects thrive.",
            "jupiter": "Timely rains; summer crops, juices, milk, and ghee freely available.",
            "venus":   "Bumper wheat, rice, and sugarcane; flowers and fruits abundant.",
            "saturn":  "Loss of ripe crops; expensive goods; masses in useless disputes.",
        },
        "durgesh_defense": {
            "sun":     "Honest administration; justice upheld; moderate security climate.",
            "moon":    "Luxuries increase; dairy abundant; armed forces satisfied.",
            "mars":    "Traders operate in fear; military aggression elevated; fire risk.",
            "mercury": "Navy and communication intelligence strengthened; strategic clarity.",
            "jupiter": "Efficient law enforcement; military strong; national protection.",
            "venus":   "Senior administrators comfortable; diplomatic success.",
            "saturn":  "Humiliation by enemies; risk of territorial loss; defense under-resourced.",
        },
        "dhanesh_treasury": {
            "sun":     "Cattle traders profit; government income from traditional sectors.",
            "moon":    "Trade profits; rulers comfortable; import/export balanced.",
            "mars":    "Trade unstable; oppressive financial laws; market volatility.",
            "mercury": "Farmers earn well; IT and publishing boom; financial rituals observed.",
            "jupiter": "Rich and religious people prosper; luxury and banking stable.",
            "venus":   "Honest rulers; traders happy; consumer goods plentiful.",
            "saturn":  "Paucity of national funds; scholars and accountants suffer.",
        },
        "dhanyesh_winter_crops": {
            "sun":     "Crops destroyed; ruler strife; widespread fever.",
            "moon":    "Winter crops excellent; milk freely available; population well-fed.",
            "mars":    "Sugarcane and ghee expensive; fire risk in storage areas.",
            "mercury": "Good winter crops; rainfall sufficient; communication infrastructure good.",
            "jupiter": "Wheat and rice plentiful; religious activities increase.",
            "venus":   "Fodder and grains expensive; dairy reduced.",
            "saturn":  "National treasury depleted; war risk; essential goods scarce.",
        },
        "meghesh_rain": {
            "sun":     "Less rain than average; high theft activity; political rift.",
            "moon":    "Copious rain; social harmony; public amenities increase.",
            "mars":    "Irregular and unpredictable rain; people gloomy; fire risk during dry spells.",
            "mercury": "Heavy rain; religious activities; infrastructure investments.",
            "jupiter": "Timely and excellent rain; universal prosperity.",
            "venus":   "Satisfied public; rain sufficient; efficient governance.",
            "saturn":  "Scanty rain below seasonal average; disease fear; drought risk.",
        },
        "rasesh_juices": {
            "sun":     "Insufficient rain; shortage of dairy, oils, and cloth; honey/sweets expensive.",
            "moon":    "Adequate sugar and juices; increased wealth; good general health.",
            "mars":    "Short supply of juices and sugar; expensive goods; danger of fires.",
            "mercury": "Abundant juices, grains, milk, and ghee; national security maintained.",
            "jupiter": "Luxurious living; excellent lotus and juicy crops.",
            "venus":   "Celebrations and religious rituals; good sugar and gur production.",
            "saturn":  "Scanty rain; juice crops suffer; risk of epidemics and starvation.",
        },
        "phalesh_fruits": {
            "sun":     "Lush earth; sufficient rain; fruit production adequate.",
            "moon":    "Good crops; efficient rulers; fruit and flower markets thrive.",
            "mars":    "Poor fruit production; ruler tension; agricultural disputes.",
            "mercury": "Lush grass; people comfortable; horticulture sector expands.",
            "jupiter": "Religious rituals; good plants and flowering; bumper garden produce.",
            "venus":   "Delicious food; noble deeds; luxury produce sector booms.",
            "saturn":  "Crops damaged; snowfall and frost losses; severe horticulture disruption.",
        },
    },
    governance_tone_vetoes = {
        "royal_planets_veto": (
            "If Sun or Moon do NOT become King (Raja) in a given year cycle: "
            "'Executive Instability Alert: Royalty and top leadership will suffer.' "
            "The executive loses its solar/lunar dignity and struggles to project authority."
        ),
        "commander_veto": (
            "If Mars does NOT become Commander (Sasyesh or Durgesh): "
            "'Military and Naval Weakness Alert: Army and Navy suffer from inadequate leadership.'"
        ),
        "king_minister_enemy_rule": (
            "IF the Raja (King) and Mantri (Minister) planets are natural enemies "
            "(e.g., Sun-Saturn, Moon-Rahu, Jupiter-Mercury adversarial pairs): "
            "'Administrative Alert: High probability of policy deadlock and cabinet bickering.' "
            "The executive and implementation layers are working against each other."
        ),
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 7 — Mehta Ch 22/23: Lord of Year — Qualitative Engine
# ═════════════════════════════════════════════════════════════════════════════
MEHTA_CH22_LORD_OF_YEAR = _spec(
    spec_id   = "mehta-ch22-lord-of-year-engine",
    spec_type = "classification_engine",
    title     = "Lord of the Year (Raja) Quality Engine — Benefic/Malefic Annual Tone",
    source    = "mehta_ch22_ch23",
    description = (
        "Mehta Ch 22/23 establishes the qualitative macro-governance tone for each year "
        "based on its planetary ruler (Raja/King). Benefic Kings promote prosperity and "
        "rainfall; their results are modified by Affliction Vetoes and modern sector mapping. "
        "Malefic Kings trigger the Hazard Module — war, fire, and structural instability. "
        "This spec provides the high-resolution 21st-century calibration layer."
    ),
    lord_of_year_results = {
        "sun_as_raja": {
            "classical_outcomes": (
                "Mentally disturbed rulers; danger by fire and theft; unusual heat; "
                "scarce food; destructive wars; poor harvest; death of a senior leader."
            ),
            "modern_sector_notes": "High-level government corruption exposés; institutional collapse.",
            "validation_2001": (
                "Year of the Sun — Gujarat Earthquake, Tehelka corruption scandal, "
                "collapse of US-64 mutual fund scheme. All three align with classical Sun-King outcomes."
            ),
            "affliction_multiplier": "If Sun is combust or loses in Grahayudha, all beneficial results reversed to Calamitous.",
        },
        "moon_as_raja": {
            "classical_outcomes": (
                "Plenty of rain and food; joy and mirth; flourishing vegetation; "
                "prosperous and happy citizenry; health measures succeed."
            ),
            "modern_sector_notes": "Social harmony; healthcare systems strengthen; water infrastructure investments.",
            "affliction_monitor": (
                "If Moon is afflicted, triggers 'National Pain': internal insurgencies, "
                "naxalism, separatist movements, or mass mental health crises."
            ),
        },
        "mars_as_raja": {
            "classical_outcomes": (
                "Fighting between rulers; forest fires; robberies; "
                "widespread bilious diseases; military aggression elevated."
            ),
            "modern_sector_notes": (
                "Year of the Sword: increased global terrorism, property destruction, "
                "military confrontations, and fire-related disasters."
            ),
            "year_of_sword_trigger": (
                "IF Raja == Mars OR Mantri == Mars THEN 'Security Forecast: "
                "Fear of war, fire accidents, and military assertiveness confirmed.'"
            ),
        },
        "mercury_as_raja": {
            "classical_outcomes": (
                "Plentiful rain; flourishing stock markets; prosperity for artists; "
                "administrative justice; intellectual and media growth."
            ),
            "modern_sector_notes": (
                "IT and communications sector surge. Mercury rules 21st-century media; "
                "affliction leads to storms and press distortion/fake news spread."
            ),
        },
        "jupiter_as_raja": {
            "classical_outcomes": (
                "Excellent crops; religious rituals; universal prosperity; "
                "plenty of milk, honey, and riches; legal welfare."
            ),
            "modern_sector_notes": "Jupiter governs banks — exceptional banking/financial system year.",
            "affliction_veto": (
                "IF Jupiter is afflicted as Raja THEN 'Fiscal Stability Warning: "
                "High probability of a banking crisis or collapse of major financial institutions.'"
            ),
            "prosperity_gate": (
                "IF Raja == Jupiter AND Mantri == Venus THEN "
                "'Golden Year Forecast: Exceptional national wealth, bumper output, societal peace.'"
            ),
            "golden_year_variant": (
                "IF Raja == Jupiter AND Mantri == Mercury THEN "
                "'National Forecast: Exceptional year for justice, education, and economic expansion.'"
            ),
        },
        "venus_as_raja": {
            "classical_outcomes": (
                "Abundant rice and sugarcane; full lakes and rivers; "
                "beautiful and prosperous citizenry; victory over enemies."
            ),
            "modern_sector_notes": (
                "Telecom and media growth year. Venus years influence the glamour and film world; "
                "morals of society undergo radical change (positive or negative)."
            ),
        },
        "saturn_as_raja": {
            "classical_outcomes": (
                "Poor rainfall; robber activity; sinful and corrupt acts; "
                "destruction of crops; general societal misery."
            ),
            "modern_sector_notes": "Strikes, food shortages, administrative frustration, and austerity measures.",
            "validation_1991": (
                "Year of Saturn King — massive strikes, food shortages, and administrative "
                "frustration confirmed. India's 1991 economic crisis occurred under Saturn Raja."
            ),
            "civil_strife_trigger": (
                "IF Raja == Saturn AND Mars conjuncts Saturn THEN "
                "'Governance Disaster Alert: Theft, epidemics, and violent leadership transitions predicted.'"
            ),
        },
    },
    combustion_veto = (
        "Universal axiom: If the Raja planet is combust (within 8° of Sun) or loses in "
        "Grahayudha (Planetary War) during its term as King, ALL beneficial results are "
        "reversed to their calamitous opposites. A combust Jupiter King produces bank failures "
        "rather than banking prosperity."
    ),
    sovereign_survival_rule = (
        "IF Sun or Moon do NOT become the King in a given cycle → "
        "'Executive Alert: Royalty and top leadership will suffer instability.' "
        "This is a foundational governance hazard signal — the natural luminaries of authority "
        "are absent from the throne."
    ),
    modern_sector_cross_mapping = {
        "mercury_portfolios": "Maps to IT, BPO, publishing, and communications sectors.",
        "jupiter_portfolios": "Maps to banking, judiciary, education, and religious institutions.",
        "venus_portfolios":   "Maps to telecom, media, entertainment, luxury goods, and fashion.",
        "saturn_portfolios":  "Maps to mining, heavy industry, labour, and infrastructure.",
        "mars_portfolios":    "Maps to defence, police, fire services, and metals/weapons.",
        "sun_portfolios":     "Maps to government leadership, power generation, and gold.",
        "moon_portfolios":    "Maps to agriculture, dairy, water management, and healthcare.",
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 8 — Mehta Ch 22: Governance Portfolio Synthesis Rules
# ═════════════════════════════════════════════════════════════════════════════
MEHTA_CH22_PORTFOLIO_SYNTHESIS = _spec(
    spec_id   = "mehta-ch22-governance-portfolio-synthesis",
    spec_type = "synthesis_engine",
    title     = "Governance Portfolio Synthesis Rules — Cabinet Pair Logic & Sector Diagnostics",
    source    = "mehta_ch22_ch23",
    description = (
        "Mehta Ch 22/23 provides synthesis rules for combining cabinet portfolio appointments "
        "into compound governance forecasts. No single portfolio prediction is complete without "
        "cross-referencing related portfolios and applying the mandatory synthesis requirement: "
        "all cabinet results must be combined with Chaitra Shukla Pratipada, Surya Veedhi, "
        "and the fortnightly lunation chart."
    ),
    synthesis_requirement = (
        "MANDATORY: No cabinet prediction is finalised until cross-referenced with: "
        "(1) Hindu New Year chart (Chaitra Shukla Pratipada), "
        "(2) Surya Veedhi (Sun's zodiac path chart), "
        "(3) Fortnightly Paksha Kundali (lunation chart). "
        "Cabinet portfolios are the structural skeleton — these three charts provide the flesh."
    ),
    compound_cabinet_rules = {
        "prosperity_gate": {
            "condition": "IF Raja == Jupiter AND Mantri == Venus",
            "result": "Golden Year Forecast: Exceptional national wealth, bumper agricultural output, societal peace.",
        },
        "golden_year_variant": {
            "condition": "IF Raja == Jupiter AND Mantri == Mercury",
            "result": "National Forecast: Exceptional year for justice, education, and economic expansion.",
        },
        "year_of_sword": {
            "condition": "IF Raja == Mars OR Mantri == Mars",
            "result": "Security Forecast: Fear of war, fire accidents, and elevated military assertiveness.",
        },
        "anarchy_gate": {
            "condition": "IF Raja == Sun AND Mantri == Saturn",
            "result": "Systemic Instability Warning: Cruel administrative behavior and high-level leader mortality predicted.",
        },
        "treasury_depletion": {
            "condition": "IF Dhanesh == Saturn AND Dhanesh is aspected by Mars",
            "result": "Fiscal Stability Warning: Paucity of national funds; scholars and accountants suffer.",
        },
        "defense_vulnerability": {
            "condition": "IF Durgesh == Saturn AND Saturn is in 12th house",
            "result": "Critical Defense Alert: Risk of national humiliation by enemies and territorial loss.",
        },
        "commodity_fire_alert": {
            "condition": "IF Rasesh == Mars AND Neersesh == Sun",
            "result": "Commodity Alert: Rapid rise in prices of gold, sweets, and oils; danger of urban fires.",
        },
        "winter_prosperity": {
            "condition": "IF Dhanyesh == Jupiter AND Meghesh == Moon",
            "result": "National Forecast: Exceptional winter harvest and abundant water resources.",
        },
        "development_forecast": {
            "condition": "IF Mantri == Moon OR Sasyesh == Mercury",
            "result": "Prosperity Forecast: Major infrastructure projects likely completed on schedule.",
        },
        "economic_collapse_alert": {
            "condition": "IF Raja == Jupiter AND Jupiter is afflicted",
            "result": "Fiscal Stability Warning: High probability of banking crisis or collapse of major financial institutions.",
        },
    },
    modernization_heuristics = {
        "rule_1": "All textual meanings from classical sources are templates requiring 21st-century re-mapping.",
        "rule_2": "Agricultural yield portfolios must be mapped to specific industries and commodity metals.",
        "rule_3": "Planetary roles should be interpreted as indicators for modern professional classes.",
        "rule_4": "Mercury Dhanesh = IT and Publishing boom. Venus Durgesh = Diplomatic success. Saturn Durgesh = Defense humiliation.",
        "industrial_shift": {
            "mercury_dhanesh": "Information Technology and Publishing sector boom.",
            "mercury_durgesh": "Naval and Communication Intelligence strengthening.",
            "jupiter_dhanesh": "Banking stability and institutional wealth growth.",
            "venus_phalesh":   "Luxury and cosmetics sector expansion.",
            "saturn_dhanesh":  "Paucity of funds; heavy industry and labour sector stressed.",
        },
    },
)


# ─────────────────────────────────────────────────────────────────────────────
ALL_SPECS = [
    GOPAL_CH4_TRI_LAGNA_ENGINE,
    GOPAL_CH4_SPOILER_LOGIC,
    GOPAL_CH4_DASHA_TIMING,
    GOPAL_CH4_CAMPAIGN_CHARTS,
    GOPAL_CH4_CASE_STUDIES,
    MEHTA_CH22_CABINET_PORTFOLIOS,
    MEHTA_CH22_LORD_OF_YEAR,
    MEHTA_CH22_PORTFOLIO_SYNTHESIS,
]
# ─────────────────────────────────────────────────────────────────────────────


async def run():
    if DRY_RUN:
        print(f"[DRY RUN] Would upsert {len(ALL_SPECS)} specs into mundane_engine_specs")
        for s in ALL_SPECS:
            print(f"  • {s['spec_id']}")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    col    = client[DB_NAME]["mundane_engine_specs"]
    ok = 0
    for spec in ALL_SPECS:
        await col.update_one(
            {"spec_id": spec["spec_id"]},
            {"$set": spec},
            upsert=True,
        )
        ok += 1
    client.close()
    print(f"[v19 specs] Upserted {ok}/{len(ALL_SPECS)} specs → mundane_engine_specs ✓")


if __name__ == "__main__":
    asyncio.run(run())
