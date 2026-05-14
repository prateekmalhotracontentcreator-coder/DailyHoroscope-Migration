"""
Mundane Astrology — Engine Specs INGEST v17
===========================================
Batch : mundane-engine-v17-20260507
Collection : mundane_engine_specs
Science    : mundane_jyotish

Chapters encoded:
  Gopal Ch 3  — Celebrity / Leadership Authenticity Engine
                (Triple 10th Lord Check, Leadership Lagna Signatures,
                 National Native Alignment Veto, Widow/Unmarried PM Multiplier)
                Yogi Karve Birth-Time Rectification
                (Month Number Grid, Lagna Number Grid, 3-step formula)
                Celebrity Truth Anchors
                (Amitabh Bachchan, Bill Gates, Sonia Gandhi case signatures)

  Gopal Ch 14 — Hits of 2006 — Real-World Validation Audit
                Saturn-Pushya Bull Run + Saturn-Leo Real Estate Engine
                Mars Perigee Regional Leadership Veto
                Nadi Transit Rules (Saturn 8th from Jupiter career fall)
                Industrial Sector Transit Matrix
                  (Automotive, IT/BPO, Pharma, Retail/FMCG)
                Geopolitical Validation Nodes
                  (Sri Lanka, Iran-US, decentralized terror, oil commodity)

DRY_RUN = True  →  set False (or use run_mundane_ingest.py) to write to MongoDB.
"""

import asyncio
import os
import sys
import types
from datetime import datetime, timezone

# ── motor stub (fires only when motor is absent) ──────────────────────────────
if "motor" not in sys.modules:
    _motor     = types.ModuleType("motor")
    _motor_asy = types.ModuleType("motor.motor_asyncio")
    class _FakeClient:
        def __getitem__(self, k): return self
        def __getattr__(self, k): return self
        async def update_one(self, *a, **kw): pass
    _motor_asy.AsyncIOMotorClient = _FakeClient
    sys.modules["motor"]                  = _motor
    sys.modules["motor.motor_asyncio"]    = _motor_asy

from motor.motor_asyncio import AsyncIOMotorClient   # noqa: E402

# ── config ────────────────────────────────────────────────────────────────────
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.environ.get("DB_NAME",  "horoscope_db")
DRY_RUN   = True

_BATCH = "mundane-engine-v17-20260507"
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
# SPEC 1 — Gopal Ch 3: Celebrity / Leadership Authenticity Engine
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH3_CELEBRITY_AUTHENTICITY = _spec(
    spec_id   = "gopal-ch3-celebrity-authenticity-engine",
    spec_type = "heuristic_filter",
    title     = "Celebrity & Leadership Authenticity Engine — Triple 10th Lord Check",
    source    = "gopalakrishnan_ch3",
    description = (
        "Gopalakrishnan Ch 3 addresses the crisis of unreliable celebrity birth data. "
        "A 'Great Native' must have a 10th lord (Power/Career) that is strong from at "
        "least two of three primary reference points: Lagna, Chandra Lagna, and Karkamsha "
        "Lagna. If the Strength Coefficient falls below 0.60, the chart is rejected as "
        "unreliable. Additional filters: preferred leadership Lagnas, national native "
        "alignment veto (politician's Lagna in 6/8/12 from national Lagna = Limited "
        "Success), and the Widow/Unmarried PM Multiplier for Indian political queries."
    ),
    triple_check_rule = (
        "10th lord must be strong (Exalted, Vargottam, own sign, or in 11th house / "
        "Trikona) from at least 2 of: Lagna, Chandra Lagna, Karkamsha Lagna. "
        "Strength Coefficient = (count of strong reference points) / 3. "
        "If < 0.60 → chart rejected: 'Data Unreliable — perform birth rectification'."
    ),
    leadership_lagna_preference = ["Cancer", "Taurus", "Scorpio", "Leo"],
    leadership_lagna_note = (
        "Most successful Indian political figures are born with Cancer (Karka) or "
        "Taurus (Vrisha) Lagnas. Engine assigns +0.1 weight modifier to these signs "
        "for Indian national context queries."
    ),
    national_native_alignment = {
        "rule": (
            "Cross-reference the candidate's Lagna against the National Foundation Chart. "
            "If candidate's Lagna falls in the 6th, 8th, or 12th house from national Lagna "
            "(e.g., for India: Libra, Sagittarius, or Aries), flag 'Limited Success Alert: "
            "Native will face systemic opposition from the national establishment'."
        ),
        "india_trika_positions": ["Libra (6th)", "Sagittarius (8th)", "Aries (12th)"],
    },
    widow_unmarried_pm_multiplier = {
        "rule": (
            "For Indian Prime Minister seat queries: if Saturn is the 10th lord AND "
            "the candidate is unmarried or widowed, apply +0.2 weight multiplier. "
            "Historical basis: Nehru, Indira Gandhi, Vajpayee, Modi."
        ),
        "rationale": "Saturn as 10th lord favors ascetic/solitary commitment to governance.",
    },
    rasi_sandhi_veto = (
        "If the 10th lord is in Rasi Sandhi (0° or 29°), it acts as an automatic "
        "'Spoiler' — predicting a loss even if the candidate appears strong in polls."
    ),
    data_authenticity_note = (
        "Per source: 8 out of 10 celebrity horoscopes in published books are historically "
        "incorrect. Engine must reject any chart failing the Triple Check before processing."
    ),
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 2 — Gopal Ch 3: Yogi Karve Birth-Time Rectification
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH3_YOGI_KARVE_RECTIFICATION = _spec(
    spec_id   = "gopal-ch3-yogi-karve-rectification",
    spec_type = "calculation_table",
    title     = "Yogi Karve Birth-Time Rectification — Month + Lagna Number Grid",
    source    = "gopalakrishnan_ch3",
    description = (
        "The Yogi Karve method provides a mathematical protocol using birth minutes "
        "to verify the correct rising sign. If the calculated Lagna range does not "
        "match the observed Lagna, the birth time is mathematically incorrect and "
        "requires rectification before the chart can be used in governance/election queries."
    ),
    formula = (
        "Step 1: Calculate = (Day_of_Birth × 4) + Month_Number + Birth_Minutes_from_Midnight. "
        "Step 2: If total > 1440, subtract 1440. "
        "Step 3: Match remainder against Lagna Number Grid below to identify calculated Lagna. "
        "If calculated Lagna ≠ observed Lagna → birth time is incorrect."
    ),
    month_number_table = {
        "january":   726,
        "february":  850,
        "march":     996,
        "april":    1086,
        "may":      1208,
        "june":     1327,
        "july":        6,
        "august":    127,
        "september": 250,
        "october":   366,
        "november":  491,
        "december":  604,
    },
    lagna_number_grid = {
        "mesha_aries":        "76–181",
        "vrisha_taurus":      "181–302",
        "mithuna_gemini":     "302–434",
        "karka_cancer":       "434–566",
        "simha_leo":          "566–691",
        "kanya_virgo":        "691–818",
        "tula_libra":         "818–949",
        "vrischik_scorpio":   "949–1083",
        "dhanu_sagittarius":  "1083–1208",
        "makara_capricorn":   "1208–1319",
        "kumbha_aquarius":    "1319–1419",
        "meena_pisces":       "1419–1440 (and 0–76)",
    },
    engine_note = (
        "This table allows automated birth sign verification for heads of state and "
        "high-profile entities. Engine must run this check before processing any "
        "political or governance query."
    ),
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 3 — Gopal Ch 3: Celebrity Truth Anchors (Validated Case Signatures)
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH3_CELEBRITY_TRUTH_ANCHORS = _spec(
    spec_id   = "gopal-ch3-celebrity-truth-anchors",
    spec_type = "case_study_database",
    title     = "Celebrity Truth Anchors — Validated Astrological Signatures",
    source    = "gopalakrishnan_ch3",
    description = (
        "Empirically validated chart signatures for notable personalities, "
        "used as 'Truth Anchors' to calibrate the leadership authenticity engine. "
        "Each case confirms a specific pattern: Career house placement, Dasha trigger, "
        "Raja Yoga configuration."
    ),
    truth_anchors = {
        "amitabh_bachchan": {
            "technical_signature": (
                "10th lord placed in 8th house (breaks/struggle) associated with "
                "functional benefics → produces massive 11th house gains after delay."
            ),
            "dasha_trigger": "Phenomenal success triggered during Saturn Dasha (1971–1990).",
            "universal_rule": (
                "IF (Raja Yogas occur in the 8th House) THEN 'Career Pattern: "
                "Significant early struggle or breaks followed by a phenomenal rise'."
            ),
        },
        "bill_gates": {
            "technical_signature": (
                "5th lord and 9th lord combined in 5th house = High Order Trikona-Trikona "
                "Raja Yoga. 10th lord in 3rd house (Writing/Software/Communication)."
            ),
            "sector_link": "10th lord in 3rd = Technology authorship and software dominance.",
            "universal_rule": (
                "IF (Two Trikona lords combine in a Trikona) THEN 'Wealth Forecast: "
                "Native will achieve wealth at unheard-of levels'."
            ),
        },
        "sonia_gandhi": {
            "technical_signature": (
                "Cancer Lagna; Darakaraka in 6th house signals premature loss of partner. "
                "Career shift decoded via Kalachakra Dasa of Kumbha. Jupiter aspecting "
                "10th lord and 10th house in Sagittarius = major career shifts."
            ),
            "universal_rule": (
                "IF (Darakaraka is in 6th House) THEN "
                "'Premature Loss of Partner' risk for the political native."
            ),
        },
    },
    diagnostic_patterns = {
        "greatness_gate": (
            "IF (10th lord strong from all 3 reference points) THEN "
            "'Destiny Alert: Native is mathematically marked for global greatness'."
        ),
        "struggle_to_success": (
            "IF (Raja Yogas in 8th House) THEN "
            "'Career Pattern: Early struggle → phenomenal rise after delay'."
        ),
        "billionaire_yoga": (
            "IF (Two Trikona lords in a Trikona house) THEN "
            "'Extraordinary wealth formation — Billionaire calibre'."
        ),
        "author_innovator": (
            "IF (10th lord in 3rd house) THEN "
            "'Author/Innovator role — dominance in communication-based fields'."
        ),
        "tech_sector_link": (
            "10th lord in 3rd = Writing, Software, IT innovation. "
            "10th lord in 6th = Medical/Service sector dominance."
        ),
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 4 — Gopal Ch 14: Saturn-Pushya Bull Run + Saturn-Leo Real Estate Engine
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH14_SATURN_MARKET_ENGINE = _spec(
    spec_id   = "gopal-ch14-saturn-market-engine",
    spec_type = "market_forecast_engine",
    title     = "Saturn-Pushya Bull Run + Saturn-Leo Real Estate Engine (2006 Validation)",
    source    = "gopalakrishnan_ch14",
    description = (
        "Empirically validated from the 2006 India audit. Saturn transiting Pushya "
        "Nakshatra (within Cancer) triggered an exceptional stock market bull run "
        "(Sensex 6,000 → 12,000+). Saturn entering Leo subsequently triggered a 100% "
        "real estate growth phase. Saturn-Ketu conjunction in Leo drove oil to $70/barrel. "
        "Mercury Bhukti (2nd lord, India's chart) provided the macro-Raja Yoga backdrop."
    ),
    saturn_pushya_bull_run = {
        "trigger": "Saturn transiting Pushya Nakshatra (Cancer sign)",
        "national_dasha_backdrop": "India in Rahu/Mercury/Venus Bhukti during this period",
        "market_result": (
            "Exceptional bull run: expect 50–100% growth in index values. "
            "Validation: 2006 Sensex moved from 6,000 to 10,000+ (peak 12,000+)."
        ),
        "sector_winners": ["Banking", "FMCG", "IT", "Telecom (Bharti Tele)"],
        "logic_gate": (
            "IF (Saturn transits Pushya Nakshatra) AND "
            "(India in Rahu/Mercury/Venus Dasha) THEN "
            "'Exceptional Bull Run: 50–100% index growth expected'."
        ),
    },
    saturn_leo_real_estate = {
        "trigger": "Saturn enters Simha (Leo)",
        "result": (
            "100% growth in property prices and builder stocks. "
            "Middle-class obsession with home ownership peaks. "
            "Validation: Chennai and all major metros saw massive price surges 2006–2008."
        ),
        "logic_gate": (
            "IF (Saturn transits Leo/Simha) THEN "
            "'Real Estate Alert: 100% value gains in property markets; "
            "engineering/builder stocks in explosive growth phase'."
        ),
    },
    saturn_ketu_leo_oil = {
        "trigger": "Saturn-Ketu conjunction in Leo",
        "result": "Oil prices touch $70/barrel due to proxy war pressures.",
        "logic_gate": (
            "IF (Saturn-Ketu conjunction in Leo) THEN "
            "'Commodity Alert: Oil prices likely to touch $70+/barrel'."
        ),
    },
    gold_price_logic = (
        "Saturn-Ketu configuration triggers gold price peak followed by correction, "
        "eventually establishing new highs in gold retailing."
    ),
    cluster_boss_coalition_stability = {
        "rule": (
            "IF (Oath-taking chart has 3+ planets in 9th house) THEN "
            "'Governance Pattern: Leader recognises multiple bosses and lacks full autonomy, "
            "leading to surprising stability via compromise'."
        ),
        "validation": "Manmohan Singh UPA government 2004–2009.",
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 5 — Gopal Ch 14: Mars Perigee Regional Leadership Veto
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH14_MARS_PERIGEE_ENGINE = _spec(
    spec_id   = "gopal-ch14-mars-perigee-regional-engine",
    spec_type = "planetary_proximity_trigger",
    title     = "Mars Perigee Regional Leadership Veto + Manufacturing Boost Engine",
    source    = "gopalakrishnan_ch14",
    description = (
        "When Mars approaches perigee (closest to Earth), it triggers two distinct effects: "
        "(1) A regional incumbency failure veto — all major leaders in the geographic "
        "direction represented by the sign Mars occupies face high probability of removal. "
        "(2) A manufacturing and industrial boost — Mars proximity energises mechanical and "
        "electrical manufacturing sectors. "
        "Validation: All major South Indian CMs (Jayalalitha, Chandy, Dharam Singh) were "
        "simultaneously replaced in 2006 when Mars was at perigee."
    ),
    mars_perigee_leadership_veto = {
        "trigger": "Mars at perigee (closest point to Earth)",
        "mechanism": (
            "Mars represents the South direction in Vedic astrology. "
            "When Mars is closest to Earth, it amplifies political transitions in "
            "the geographical direction of the sign Mars occupies at perigee."
        ),
        "logic_gate": (
            "IF (Mars Proximity == Perigee) THEN "
            "'Regional Stability Alert: High probability of incumbency failure for "
            "leaders in the direction represented by the current sign'. "
            "IF (Mars in Fixed Sign at Perigee) THEN "
            "'Multiple simultaneous leadership replacements in that direction'."
        ),
        "validation": (
            "2006: Mars at perigee in a southward sign → "
            "Jayalalitha (Tamil Nadu), Oommen Chandy (Kerala), and Dharam Singh "
            "(Karnataka) all lost power within the same election cycle."
        ),
    },
    mars_perigee_manufacturing_boost = {
        "logic_gate": (
            "IF (Mars is at perigee/closest to Earth) THEN "
            "'High efficiency in manufacturing units and electrical components — "
            "1.5× growth multiplier for Automotive and Medical Equipment sectors'."
        ),
        "demographic_casualties": (
            "Mars proximity also correlates with mass death of children "
            "and increased risk of fire accidents, blasts, and terrorist events."
        ),
    },
    directional_sign_mapping = {
        "south": ["Mars-ruled signs and signs where Mars is strong"],
        "note": (
            "Full directional mapping: Sun→East, Venus→South-East, Mars→South, "
            "Saturn→West, Moon→North-West, Mercury→North."
        ),
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 6 — Gopal Ch 14: Nadi Transit Rules (Saturn 8th from Jupiter)
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH14_NADI_TRANSIT_RULES = _spec(
    spec_id   = "gopal-ch14-nadi-transit-rules",
    spec_type = "nadi_timing_engine",
    title     = "Nadi Transit Rules — Individual Career/Health Timing from 2006 Validation",
    source    = "gopalakrishnan_ch14",
    description = (
        "High-precision Nadi rules validated against real individuals in the 2006 audit. "
        "These rules cross-reference individual natal charts with transiting planets to "
        "time career falls, health crises, and professional peaks. The Saturn-8th-from-Jupiter "
        "rule is the cornerstone, validated via Sourav Ganguly's exit from cricket captaincy."
    ),
    nadi_career_fall_rule = {
        "rule": (
            "IF (Saturn transits the sign 8th from Natal Jupiter) THEN "
            "'Individual Performance Alert: Sudden and sustained poor form / career break "
            "for the elite native'."
        ),
        "validation": (
            "Sourav Ganguly 2006: Saturn transited 8th from his natal Jupiter → "
            "exit from Indian cricket captaincy, sustained poor form."
        ),
        "also_applies_to": (
            "Sachin Tendulkar audit in same period confirmed similar transit pressure. "
            "Rule is universal for any high-performing individual in their peak career."
        ),
    },
    mercury_bhukti_epidemic_recovery = {
        "rule": (
            "IF (Bhukti Lord is Mercury) AND (Direct Motion resumes after retrograde) THEN "
            "'Crisis Normalization: Agriculture and livestock industries return to "
            "normalcy within 60 days of Mercury going direct'."
        ),
        "validation": (
            "2006 Bird Flu crisis: Mercury Bhukti (2nd lord) with Saturn retrograde near "
            "April 15 triggered the crisis. Recovery confirmed post Mercury direct motion."
        ),
    },
    saturn_3rd_national_it_boom = {
        "rule": (
            "IF (Saturn transits the 3rd house from National Lagna) THEN "
            "'IT/BPO Forecast: Massive boom in software and back-office processing. "
            "India becomes the global backbone of information processing'. "
            "Contrarian Alert: Ignore media skepticism — BPO recruitment will treble."
        ),
        "validation": "2004–2006 India IT boom confirmed during Saturn's transit of 3rd from Taurus Lagna.",
    },
    mercury_jupiter_banking = {
        "rule": (
            "IF (Mercury Bhukti is active) AND (Jupiter in 2nd House) THEN "
            "'Banking Forecast: Massive computerisation and introduction of new revenue models'."
        ),
        "validation": "2003–2006 Indian banking computerisation and growth phase.",
    },
    saturn_8th_from_moon_defeat = (
        "IF (Saturn transits 8th from Moon OR Lagna) THEN 'Defeat Likely' — "
        "applies to both individuals and national leaders."
    ),
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 7 — Gopal Ch 14: Industrial Sector Transit Matrix
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH14_INDUSTRIAL_SECTOR_ENGINE = _spec(
    spec_id   = "gopal-ch14-industrial-sector-engine",
    spec_type = "sector_forecast_matrix",
    title     = "Industrial Sector Transit Matrix — Automotive / IT / Pharma / Retail (2006)",
    source    = "gopalakrishnan_ch14",
    description = (
        "The 2006 audit established that individual industrial sector performance follows "
        "the Transit-to-House Mapping of the National Foundation Chart. While national Raja "
        "Yogas provide macro momentum, specific sectors are ignited by targeted planetary "
        "transits. This matrix provides the logic gates for sector forecasting."
    ),
    automotive_and_mechanical = {
        "governing_planets": ["Mars (Energy/Steel)", "4th House (Vehicles)"],
        "conditions": {
            "manufacturing_boost": (
                "IF (Mars is at perigee) THEN "
                "'High efficiency in manufacturing and electrical components'."
            ),
            "segment_split": (
                "IF (4th lord is strong but aspected by Saturn) THEN "
                "'Lower-end/Entry-level segments outperform luxury segments'."
            ),
            "ancillary_export_boom": (
                "IF (Mars in Upchayya transit — 3rd/6th/10th/11th from Lagna) THEN "
                "'Auto ancillaries become export-oriented profit centres'."
            ),
        },
        "validation": "2006 Indian auto sector: record first-time buyers, Maruti/Bajaj bull run.",
    },
    information_technology_bpo = {
        "governing_planets": ["Mercury (Communication)", "3rd House (Networks/Writing)"],
        "conditions": {
            "it_backbone_rule": (
                "IF (Saturn transits 3rd house from National Lagna) THEN "
                "'India becomes the global backbone for back-office processing — "
                "BPO recruitment trebles despite media skepticism'."
            ),
            "bpo_specialisation": (
                "IF (Mercury is in direct motion in Airy signs) THEN "
                "'BPO enters specialisation phase (KPO, LPO, analytics)'."
            ),
            "connectivity_surge": (
                "IF (3rd lord conjoins 11th lord) THEN "
                "'Exponential growth in Internet penetration and PC ownership'."
            ),
        },
        "validation": "2006: IT sector set records — Infosys, Wipro, TCS all-time highs.",
    },
    pharmaceuticals_and_healthcare = {
        "governing_planets": ["6th House (Service/Diseases)", "Mercury (analysis)"],
        "conditions": {
            "export_dominance": (
                "IF (6th lord in 10th or 11th house) THEN "
                "'Indian pharma companies establish record exports and R&D breakthroughs'."
            ),
            "hospital_chain_growth": (
                "IF (Jupiter aspects 6th house) THEN "
                "'Large-scale hospital chains see imaginative growth and international recognition'."
            ),
        },
        "validation": "2006 India pharma dream run validated in source audit.",
    },
    retail_and_fmcg = {
        "governing_planets": ["2nd House (Food/Speech)", "11th House (Gains)", "Venus (Luxury)"],
        "conditions": {
            "mall_culture_trigger": (
                "IF (Venus as Lagna lord is in Rahu axis) THEN "
                "'Explosion of Malls, Hyper-marts, and new retail formats in metropolis'."
            ),
            "rural_market_penetration": (
                "IF (Mars in 2nd house of Varsha Pravesh / Annual chart) THEN "
                "'FMCG rural markets see better volume growth than urban markets'."
            ),
            "pharma_wealth_gate": (
                "IF (6th lord in Dhana Yoga or placed in 11th house) THEN "
                "'Pharmaceutical and Healthcare sectors achieve exceptional profitability'."
            ),
        },
        "validation": "2006 retail boom: mall culture explosion across Indian metros confirmed.",
    },
    textile_niche_veto = (
        "IF (Moon is in a female sign) THEN India loses in textile volume (to China) "
        "but wins in niche/high-end segments."
    ),
    car_buyer_gate = (
        "IF (4th House is strong) AND (Venus is well-placed) THEN "
        "'Record level of first-time car buyers; bullish run for volume auto brands'."
    ),
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 8 — Gopal Ch 14: Geopolitical Validation Nodes
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH14_GEOPOLITICAL_NODES = _spec(
    spec_id   = "gopal-ch14-geopolitical-validation-nodes",
    spec_type = "geopolitical_forecast_engine",
    title     = "Geopolitical Validation Nodes — 2006 International Audit",
    source    = "gopalakrishnan_ch14",
    description = (
        "Geopolitical predictions validated against real 2006 international events. "
        "Covers Sri Lanka civil war timing, Iran-US standoff trajectory, decentralised "
        "terror doctrine, and commodity price forecasts. Provides the 'macro geopolitical "
        "stress test' layer for the mundane engine."
    ),
    sri_lanka_bloodshed = {
        "trigger": "Saturn entering Kataka (Cancer)",
        "prediction": (
            "Predicted 3-year window for high-profile assassinations and mass bloodshed "
            "when Saturn enters Cancer — applied to Sri Lanka civil conflict."
        ),
        "logic_gate": (
            "IF (Saturn transits Cancer/Kataka) AND (Nation in 6th/8th lord Dasha) THEN "
            "'Conflict Escalation Alert: 3-year window of intensified hostilities and "
            "leadership-level casualties'."
        ),
        "validation": "Sri Lanka civil war escalated sharply during Saturn-in-Cancer transit.",
    },
    iran_us_standoff = {
        "conflict_window": "April 1, 2007 onwards",
        "prediction": "US vulnerability to multiple simultaneous small-scale attacks.",
        "logic_gate": (
            "IF (Aggressor nation in 6th lord Dasha) AND (Target has Saturn in 12th of "
            "Coronation Chart) THEN 'Security Alert: Decentralised attacks from secret "
            "foes rather than standing army confrontation'."
        ),
    },
    decentralised_terror_doctrine = {
        "rule": (
            "When Saturn is in the 12th house of a nation's Coronation Chart, "
            "security agencies must look for 'spies and secret foes' rather than "
            "conventional military threats."
        ),
        "doctrine": (
            "Terrorism transitions from 'Chain of Command' to 'Cellular Operations' — "
            "the Bin Laden decentralised model. Each cell is independent; disrupting "
            "the head does not stop attacks."
        ),
        "astrological_marker": "Saturn in 12th of Coronation Chart = decentralised threat active.",
    },
    political_stability_audit = {
        "upa_survival_2006": (
            "Predicted survival of UPA coalition despite internal bickering. "
            "Manmohan Singh's 9th house 'cluster of bosses' identified as stabiliser."
        ),
        "bjp_transition": (
            "Predicted shift to younger BJP leadership and internal disarray during transition."
        ),
    },
    macro_economic_hits_2006 = {
        "foreign_reserves": "Predicted peak in India's foreign exchange reserves.",
        "interest_rates": "Predicted rise in interest rates not dampening housing demand.",
        "gold_correction_then_new_high": (
            "Gold predicted to peak, then correct, then ultimately reach new highs."
        ),
        "oil_at_70": "Saturn-Ketu in Leo → Oil $70/barrel via proxy war escalation.",
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# RUNNER
# ═════════════════════════════════════════════════════════════════════════════
ALL_SPECS = [
    GOPAL_CH3_CELEBRITY_AUTHENTICITY,
    GOPAL_CH3_YOGI_KARVE_RECTIFICATION,
    GOPAL_CH3_CELEBRITY_TRUTH_ANCHORS,
    GOPAL_CH14_SATURN_MARKET_ENGINE,
    GOPAL_CH14_MARS_PERIGEE_ENGINE,
    GOPAL_CH14_NADI_TRANSIT_RULES,
    GOPAL_CH14_INDUSTRIAL_SECTOR_ENGINE,
    GOPAL_CH14_GEOPOLITICAL_NODES,
]


async def run():
    if DRY_RUN:
        print(f"[DRY RUN] Would upsert {len(ALL_SPECS)} specs into mundane_engine_specs.")
        for s in ALL_SPECS:
            print(f"  {s['spec_id']}")
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
        print(f"  ✓ {spec['spec_id']}")
    client.close()
    print(f"\nUpserted {ok} specs into mundane_engine_specs.")


if __name__ == "__main__":
    asyncio.run(run())
