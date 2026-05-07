"""
Mundane Astrology — Interpretation Rules INGEST v17
====================================================
Batch : mundane-interp-v17-20260507
Collection : interpretation_rules
Science    : mundane_jyotish

Rule groups:
  GROUP_AO — Celebrity/Leadership Authenticity (8 rules)
  GROUP_AP — Saturn Market + Real Estate + Commodity (6 rules)
  GROUP_AQ — Mars Perigee + Regional Leadership (4 rules)
  GROUP_AR — Nadi Transit + Career Timing (5 rules)
  GROUP_AS — Industrial Sector Forecasting (5 rules)

Total: 28 rules
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

_BATCH = "mundane-interp-v17-20260507"
_NOW   = datetime.now(timezone.utc).isoformat()

def _rule(rule_id, sub_type, title, source_chapter,
          condition, result, severity="medium",
          synthesis_sources=None, checkable=True):
    return {
        "rule_id":          rule_id,
        "batch_id":         _BATCH,
        "science_id":       "mundane_jyotish",
        "sub_type":         sub_type,
        "title":            title,
        "source_chapter":   source_chapter,
        "condition":        condition,
        "result":           result,
        "synthesis_sources": synthesis_sources or [],
        "checkable":        checkable,
        "approval_status":  "pending_review",
        "severity":         severity,
        "created_at":       _NOW,
    }


# ════════════════════════════════════════════════════════════════════════════
# GROUP AO — Celebrity / Leadership Authenticity  (8 rules)
# ════════════════════════════════════════════════════════════════════════════

AO_1 = _rule(
    rule_id        = "mundane-gopal-ch3-triple-check-fail",
    sub_type       = "celebrity_authentication",
    title          = "Celebrity Triple Check Failure — Chart Rejected",
    source_chapter = "Gopalakrishnan Ch 3 — Celebrity Horoscope Analysis",
    condition      = (
        "IF (10th lord is NOT strong from at least 2 of: Lagna, Chandra Lagna, "
        "Karkamsha Lagna) — i.e., Strength Coefficient < 0.60"
    ),
    result         = (
        "Chart Rejected: 'Data Unreliable — perform birth rectification before "
        "processing any governance, election, or career query for this native'. "
        "Engine processing halted."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch3-celebrity-authenticity-engine"],
)

AO_2 = _rule(
    rule_id        = "mundane-gopal-ch3-triple-check-pass",
    sub_type       = "celebrity_authentication",
    title          = "Celebrity Triple Check Pass — Leadership Coefficient Established",
    source_chapter = "Gopalakrishnan Ch 3 — Celebrity Horoscope Analysis",
    condition      = (
        "IF (10th lord is strong from all 3 reference points: "
        "Lagna, Chandra Lagna, and Karkamsha Lagna)"
    ),
    result         = (
        "Destiny Alert: 'Native is mathematically marked for global greatness and "
        "pinnacle career success'. Leadership Coefficient set to 1.0. "
        "Proceed with full governance analysis."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch3-celebrity-authenticity-engine", "gopal-ch3-celebrity-truth-anchors"],
)

AO_3 = _rule(
    rule_id        = "mundane-gopal-ch3-national-trika-lagna",
    sub_type       = "leadership_alignment",
    title          = "Politician's Lagna in National Trika — Limited Success Alert",
    source_chapter = "Gopalakrishnan Ch 3 — Celebrity Horoscope Analysis",
    condition      = (
        "IF (Politician's Lagna falls in the 6th, 8th, or 12th house from "
        "the National Foundation Chart Lagna) — "
        "e.g., for India (Taurus Lagna): Libra (6th), Sagittarius (8th), or Aries (12th)"
    ),
    result         = (
        "Limited Success Alert: 'Native will face systemic opposition from the national "
        "establishment. Career advancement in national politics is structurally obstructed "
        "by the nation's own astrological geometry'."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch3-celebrity-authenticity-engine"],
)

AO_4 = _rule(
    rule_id        = "mundane-gopal-ch3-widow-pm-multiplier",
    sub_type       = "leadership_alignment",
    title          = "Widow/Unmarried Candidate — Indian PM Longevity Multiplier",
    source_chapter = "Gopalakrishnan Ch 3 — Celebrity Horoscope Analysis",
    condition      = (
        "IF (Saturn is the 10th lord in candidate's chart) "
        "AND (candidate is unmarried or widowed) "
        "AND (Query context is Indian Prime Minister seat)"
    ),
    result         = (
        "Longevity Bonus: +0.2 weight multiplier applied to this candidate's "
        "'Duration of Government' forecast. "
        "Historical basis: Nehru, Indira Gandhi, Vajpayee, Modi — all unmarried/widowed "
        "or ascetic by nature, all held PM seat for extended durations."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch3-celebrity-authenticity-engine"],
)

AO_5 = _rule(
    rule_id        = "mundane-gopal-ch3-rasi-sandhi-spoiler",
    sub_type       = "election_prediction",
    title          = "Rasi Sandhi 10th Lord — Automatic Election Spoiler",
    source_chapter = "Gopalakrishnan Ch 3 — Celebrity Horoscope Analysis",
    condition      = (
        "IF (10th lord is in Rasi Sandhi: 0° or 29° of any sign) "
        "— even if the candidate appears strong in polls or media analysis"
    ),
    result         = (
        "Margin Warning: 'Significant risk of losing a close race due to technicalities, "
        "sudden vote-splits, or administrative disqualification. "
        "Rasi Sandhi acts as an automatic Spoiler — nullifying apparent strength'."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch3-celebrity-authenticity-engine"],
)

AO_6 = _rule(
    rule_id        = "mundane-gopal-ch3-struggle-to-success",
    sub_type       = "career_pattern",
    title          = "Raja Yoga in 8th House — Struggle-to-Success Career Pattern",
    source_chapter = "Gopalakrishnan Ch 3 — Celebrity Horoscope Analysis",
    condition      = (
        "IF (Raja Yogas — two or more Trikona/Kendra lords conjoined — "
        "occur in the 8th House of the native's chart)"
    ),
    result         = (
        "Career Pattern Alert: 'Significant early struggle, breaks, and reversals "
        "followed by a phenomenal rise and eventual iconic status'. "
        "The obstacles ARE the path — do not interpret 8th house placements as failure'. "
        "Validation: Amitabh Bachchan — 10th lord in 8th, Saturn Dasha triggered iconic career."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch3-celebrity-truth-anchors"],
)

AO_7 = _rule(
    rule_id        = "mundane-gopal-ch3-trikona-trikona-billionaire",
    sub_type       = "wealth_forecast",
    title          = "Trikona-Trikona Raja Yoga — Billionaire-Level Wealth",
    source_chapter = "Gopalakrishnan Ch 3 — Celebrity Horoscope Analysis",
    condition      = (
        "IF (Two Trikona lords — lords of 1st, 5th, and 9th houses — "
        "combine in a Trikona house)"
    ),
    result         = (
        "Wealth Forecast: 'Native will achieve wealth at unheard-of levels — "
        "Billionaire calibre. The high-order Trikona-Trikona Raja Yoga is the most "
        "powerful wealth combination in Vedic astrology'. "
        "Validation: Bill Gates — 5th and 9th lords combined in 5th house."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch3-celebrity-truth-anchors"],
)

AO_8 = _rule(
    rule_id        = "mundane-gopal-ch3-10th-in-3rd-innovator",
    sub_type       = "career_pattern",
    title          = "10th Lord in 3rd House — Author/Innovator/Technology Career",
    source_chapter = "Gopalakrishnan Ch 3 — Celebrity Horoscope Analysis",
    condition      = (
        "IF (10th lord is placed in the 3rd house of the native's chart)"
    ),
    result         = (
        "Career Signature: 'Native will dominate in communication-based fields — "
        "Writing, Authorship, Information Technology, Software innovation, or Media. "
        "The 3rd house connection gives the career a distinctly intellectual and "
        "communication-driven flavour'. "
        "Validation: Bill Gates — 10th lord in 3rd → software/technology dominance."
    ),
    severity       = "low",
    synthesis_sources = ["gopal-ch3-celebrity-truth-anchors"],
)


# ════════════════════════════════════════════════════════════════════════════
# GROUP AP — Saturn Market + Real Estate + Commodity  (6 rules)
# ════════════════════════════════════════════════════════════════════════════

AP_1 = _rule(
    rule_id        = "mundane-gopal-ch14-saturn-pushya-bull-run",
    sub_type       = "market_forecast",
    title          = "Saturn in Pushya Nakshatra — Exceptional Stock Market Bull Run",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Saturn transits Pushya Nakshatra, within Cancer/Kataka) "
        "AND (Nation in Raja Yoga Dasha/Bhukti — Rahu/Mercury/Venus for India)"
    ),
    result         = (
        "Exceptional Bull Run: 'Expect 50–100% growth in national stock index values. "
        "Sector winners: Banking, FMCG, IT, and Telecom. "
        "Validation: 2006 India — Sensex moved from 6,000 to 10,000+ (peak 12,000+)'. "
        "Ignore media correction warnings during this transit — the bull run will persist."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch14-saturn-market-engine"],
    checkable      = True,
)

AP_2 = _rule(
    rule_id        = "mundane-gopal-ch14-saturn-leo-real-estate",
    sub_type       = "real_estate_forecast",
    title          = "Saturn Enters Leo — 100% Real Estate Growth Phase",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Saturn transits Simha/Leo)"
    ),
    result         = (
        "Real Estate Alert: 'Property prices and builder stocks will achieve 100% value "
        "gains during this transit. Middle-class obsession with home ownership peaks — "
        "record mortgage demand despite rising interest rates. "
        "Engineering, construction, and builder stocks enter explosive growth phase'. "
        "Validation: 2006–2008 India real estate boom in all major metros."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch14-saturn-market-engine"],
    checkable      = True,
)

AP_3 = _rule(
    rule_id        = "mundane-gopal-ch14-saturn-ketu-leo-oil",
    sub_type       = "commodity_forecast",
    title          = "Saturn-Ketu Conjunction in Leo — Oil Price Spike",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Saturn and Ketu are conjunct in Leo/Simha)"
    ),
    result         = (
        "Commodity Alert: 'Oil prices likely to touch $70+/barrel due to proxy war "
        "pressures and energy sector disruptions. "
        "Simultaneously: gold prices peak, then correct, then establish new highs'. "
        "Validation: 2006 oil price spike to $70/barrel confirmed."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-saturn-market-engine"],
    checkable      = True,
)

AP_4 = _rule(
    rule_id        = "mundane-gopal-ch14-cluster-boss-coalition-stability",
    sub_type       = "governance_forecast",
    title          = "9th House Cluster in Oath Chart — Coalition Stability via Compromise",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (3 or more planets occupy the 9th house of the oath-taking chart)"
    ),
    result         = (
        "Governance Pattern: 'Leader will recognise multiple bosses and lack full autonomy. "
        "Despite apparent weakness, government achieves surprising stability through "
        "compromise and coalition management. "
        "Do not forecast early collapse — the multi-boss constraint IS the stabiliser'. "
        "Validation: Manmohan Singh UPA 2004–2009 government audit."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-saturn-market-engine"],
)

AP_5 = _rule(
    rule_id        = "mundane-gopal-ch14-saturn-kataka-bloodshed",
    sub_type       = "geopolitical_forecast",
    title          = "Saturn in Cancer — 3-Year Window of Conflict and Assassinations",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Saturn transits Kataka/Cancer) "
        "AND (Nation is in 6th or 8th lord Dasha)"
    ),
    result         = (
        "Conflict Escalation Alert: '3-year window of intensified hostilities, "
        "high-profile assassinations, and leadership-level casualties for nations "
        "with Cancer prominently placed in their Foundation Chart or Varsha chart'. "
        "Validation: Sri Lanka civil war escalated sharply during Saturn-in-Cancer transit."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch14-geopolitical-validation-nodes"],
)

AP_6 = _rule(
    rule_id        = "mundane-gopal-ch14-decentralised-terror",
    sub_type       = "security_forecast",
    title          = "Saturn in 12th of Coronation Chart — Decentralised Terror Active",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Saturn transits the 12th house of a nation's Coronation/Oath-taking Chart)"
    ),
    result         = (
        "Security Alert: 'Decentralised terror doctrine is active. Security agencies must "
        "monitor cellular/autonomous threat cells — not a conventional standing army. "
        "Disrupting the command head will NOT stop attacks. "
        "Each cell operates independently — intelligence-based approach required'. "
        "Doctrine validated: Bin Laden cellular model adopted globally post-2001."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch14-geopolitical-validation-nodes"],
)


# ════════════════════════════════════════════════════════════════════════════
# GROUP AQ — Mars Perigee + Regional Leadership  (4 rules)
# ════════════════════════════════════════════════════════════════════════════

AQ_1 = _rule(
    rule_id        = "mundane-gopal-ch14-mars-perigee-south-cm",
    sub_type       = "regional_leadership",
    title          = "Mars Perigee in Fixed Sign — Multiple Regional Leaders Replaced",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Mars is at perigee — closest point to Earth) "
        "AND (Mars occupies a Fixed Sign)"
    ),
    result         = (
        "Leadership Alert: 'High probability of multiple Chief Ministers or regional "
        "leaders being simultaneously replaced in the geographic direction represented "
        "by the sign Mars occupies (Mars = South direction). "
        "Incumbents in that region face structural electoral veto from the cosmos'. "
        "Validation: 2006 South India — Jayalalitha (Tamil Nadu), Chandy (Kerala), "
        "and Dharam Singh (Karnataka) all lost power in the same cycle."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch14-mars-perigee-regional-engine"],
    checkable      = True,
)

AQ_2 = _rule(
    rule_id        = "mundane-gopal-ch14-mars-perigee-manufacturing",
    sub_type       = "industrial_forecast",
    title          = "Mars Perigee — Manufacturing and Electrical Sector Efficiency Surge",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Mars is at perigee/closest to Earth)"
    ),
    result         = (
        "Manufacturing Boost: 'High efficiency in manufacturing units and electrical "
        "components. Automotive, medical equipment, and metal sectors achieve 1.5× "
        "normal growth. Auto ancillaries turn into export-oriented profit centres'. "
        "Note: Same transit also correlates with increased risk of fire accidents, "
        "blasts, and political violence."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-mars-perigee-regional-engine", "gopal-ch14-industrial-sector-engine"],
)

AQ_3 = _rule(
    rule_id        = "mundane-gopal-ch14-mars-proximity-children",
    sub_type       = "mass_death_forecast",
    title          = "Mars Proximity to Earth — Mass Death Risk for Children",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Mars proximity to Earth is observed — coming within 60 million km)"
    ),
    result         = (
        "Severe Warning: 'High risk of mass casualties among children via epidemic or "
        "violence. Surgical costs and paediatric healthcare costs surge. "
        "Simultaneously: manufacturing and fire incidents increase. "
        "One major mass-death event is expected during the Mars proximity window'. "
        "Validation: July 2003 Mars at 55.8M km — closest in 73,000 years."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch14-mars-perigee-regional-engine"],
)

AQ_4 = _rule(
    rule_id        = "mundane-gopal-ch14-regional-direction-leadership",
    sub_type       = "regional_leadership",
    title          = "Malefic Transit in Directional Sign — Regional Incumbency Failure",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Malefic planet — Mars, Saturn, or Rahu — transits a sign strongly "
        "associated with a geographic direction) "
        "AND (That malefic is afflicted or in close proximity to Earth)"
    ),
    result         = (
        "Regional Stability Alert: 'High probability of incumbency failure for "
        "leaders in the geographic direction associated with that sign/planet. "
        "Apply directional mapping: Sun→East, Venus→South-East, Mars→South, "
        "Saturn→West, Moon→North-West, Mercury→North'."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-mars-perigee-regional-engine"],
)


# ════════════════════════════════════════════════════════════════════════════
# GROUP AR — Nadi Transit + Career Timing  (5 rules)
# ════════════════════════════════════════════════════════════════════════════

AR_1 = _rule(
    rule_id        = "mundane-gopal-ch14-nadi-saturn-8th-from-jupiter",
    sub_type       = "nadi_career_timing",
    title          = "Saturn 8th from Natal Jupiter — Elite Career Break (Nadi Rule)",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Transiting Saturn enters the sign that is 8th from the native's Natal Jupiter)"
    ),
    result         = (
        "Individual Performance Alert: 'Sudden and sustained poor form or career break "
        "for the elite native. The 8th house from Jupiter is the zone of maximum "
        "Jupiterian obstruction — expansion is blocked, luck withdraws, and performance "
        "collapses despite apparent talent'. "
        "Validation: Sourav Ganguly 2006 — Saturn 8th from his natal Jupiter → "
        "exit from Indian cricket captaincy and prolonged poor form."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch14-nadi-transit-rules"],
    checkable      = True,
)

AR_2 = _rule(
    rule_id        = "mundane-gopal-ch14-mercury-bhukti-epidemic-recovery",
    sub_type       = "health_market_timing",
    title          = "Mercury Direct Motion in Bhukti — Epidemic/Crisis Normalisation",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Current Bhukti Lord is Mercury) "
        "AND (Mercury resumes direct motion after a retrograde period)"
    ),
    result         = (
        "Crisis Normalisation: 'Agriculture and livestock industries will return to "
        "normalcy within 60 days of Mercury going direct. "
        "Food-related scares, poultry epidemics, and market panics will dissipate. "
        "Sector recovery is predictable and should be used as an entry point'. "
        "Validation: 2006 Bird Flu crisis — Mercury Bhukti exit triggered poultry "
        "sector recovery on schedule."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-nadi-transit-rules"],
)

AR_3 = _rule(
    rule_id        = "mundane-gopal-ch14-saturn-3rd-it-backbone",
    sub_type       = "sector_forecast",
    title          = "Saturn in 3rd from National Lagna — IT/BPO National Backbone",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Saturn transits the 3rd house from the National Independence Chart Lagna)"
    ),
    result         = (
        "Contrarian IT Alert: 'Ignore media skepticism about BPO collapse. "
        "India becomes and remains the global backbone for information technology "
        "and back-office processing during this transit. "
        "BPO recruitment will treble. Internet penetration surges. "
        "IT/software exports reach record highs'. "
        "Validation: 2004–2006 India IT boom — all media skeptics were proven wrong."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-nadi-transit-rules", "gopal-ch14-industrial-sector-engine"],
)

AR_4 = _rule(
    rule_id        = "mundane-gopal-ch14-saturn-8th-defeat",
    sub_type       = "leadership_timing",
    title          = "Saturn 8th from Natal Moon or Lagna — Defeat Predicted",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Transiting Saturn enters the sign 8th from the native's Natal Moon "
        "OR 8th from the native's Natal Lagna)"
    ),
    result         = (
        "Defeat Likely: 'The native enters a period of maximum obstruction, loss, "
        "and humiliation. Political leaders in this transit face electoral defeat or "
        "forced resignation. Businesses face insolvency risk. "
        "For nations: incumbent government at high risk of collapse'."
    ),
    severity       = "high",
    synthesis_sources = ["gopal-ch14-nadi-transit-rules"],
)

AR_5 = _rule(
    rule_id        = "mundane-gopal-ch14-mercury-jupiter-banking",
    sub_type       = "sector_forecast",
    title          = "Mercury Bhukti + Jupiter in 2nd House — Banking Computerisation",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Mercury Bhukti is active in national chart) "
        "AND (Jupiter is placed in or transiting the 2nd house)"
    ),
    result         = (
        "Banking Forecast: 'Massive computerisation of the banking sector and introduction "
        "of new revenue models (online banking, mobile wallets, investment products). "
        "Banking stocks enter a sustained bull run'. "
        "Validation: 2003–2006 Indian banking transformation confirmed."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-nadi-transit-rules"],
)


# ════════════════════════════════════════════════════════════════════════════
# GROUP AS — Industrial Sector Forecasting  (5 rules)
# ════════════════════════════════════════════════════════════════════════════

AS_1 = _rule(
    rule_id        = "mundane-gopal-ch14-mall-culture-venus-rahu",
    sub_type       = "retail_forecast",
    title          = "Venus-Rahu Axis — Mall Culture Explosion in Metropolis",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Venus as Lagna lord is in Rahu-Ketu axis — i.e., Venus conjunct or "
        "opposite Rahu/Ketu in the national or annual chart)"
    ),
    result         = (
        "Retail Boom: 'Explosion of Malls, Hyper-marts, and new retail formats in "
        "major metropolis areas. Organised retail replaces traditional kirana stores "
        "at an accelerated pace. Mall construction stocks and retail chains in explosive "
        "growth phase'. "
        "Validation: 2006 India — mall culture launched simultaneously in 12+ metros."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-industrial-sector-engine"],
)

AS_2 = _rule(
    rule_id        = "mundane-gopal-ch14-6th-lord-pharma-wealth",
    sub_type       = "sector_forecast",
    title          = "6th Lord in 11th House or Dhana Yoga — Pharma Dream Run",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (6th lord is placed in the 11th house) "
        "OR (6th lord participates in a Dhana Yoga — combination with 2nd or 11th lord)"
    ),
    result         = (
        "Industry Alert: 'Pharmaceutical and Healthcare sectors will achieve exceptional "
        "profitability — record exports and R&D breakthroughs. "
        "Hospital chains enter a growth phase. Medical stocks outperform the broader index'. "
        "Validation: 2006 India pharma dream run confirmed in source audit."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-industrial-sector-engine"],
)

AS_3 = _rule(
    rule_id        = "mundane-gopal-ch14-4th-venus-car-buyers",
    sub_type       = "automotive_forecast",
    title          = "Strong 4th House + Well-Placed Venus — Record Car Buyers",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (4th house is strong — Lord in own sign, exalted, or with benefics) "
        "AND (Venus is well-placed — exalted, own sign, or in Kendra/Trikona)"
    ),
    result         = (
        "Market Forecast: 'Record level of first-time car buyers. "
        "Volume auto brands (entry-level and mid-segment) achieve all-time sales highs. "
        "Lower-end segments significantly outperform luxury segments due to "
        "first-time buyer demographics entering the market'. "
        "Validation: 2006 Maruti, Bajaj bull run confirmed."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-industrial-sector-engine"],
)

AS_4 = _rule(
    rule_id        = "mundane-gopal-ch14-mars-upchayya-auto-exports",
    sub_type       = "automotive_forecast",
    title          = "Mars in Upchayya from Lagna — Auto Ancillary Export Boom",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Mars is transiting an Upchayya house — 3rd, 6th, 10th, or 11th — "
        "from the National Lagna in the Annual/Varsha Chart)"
    ),
    result         = (
        "Auto Sector Forecast: 'Auto ancillary companies become export-oriented profit "
        "centres. Manufacturing efficiency peaks — electrical components, metal parts, "
        "and precision engineering sub-sectors lead the rally'. "
        "Note: Upchayya houses improve with time — Mars here is progressively stronger."
    ),
    severity       = "low",
    synthesis_sources = ["gopal-ch14-industrial-sector-engine"],
)

AS_5 = _rule(
    rule_id        = "mundane-gopal-ch14-bpo-contrarian-gate",
    sub_type       = "sector_forecast",
    title          = "BPO/IT Contrarian Gate — Ignore Media Collapse Predictions",
    source_chapter = "Gopalakrishnan Ch 14 — Hits of 2006 Validation Audit",
    condition      = (
        "IF (Media/analysts predict BPO or IT sector collapse or saturation) "
        "AND (Saturn is transiting the 3rd house of the National Independence Chart)"
    ),
    result         = (
        "Contrarian Alert: 'Override media skepticism entirely. "
        "BPO/IT sector will treble recruitment and set new export records. "
        "The Saturn-3rd-house transit structurally guarantees the knowledge-sector "
        "boom regardless of short-term noise. "
        "This is the single most reliable sectoral forecast from the 2006 audit'. "
        "Validation: Every media outlet predicted BPO slowdown in 2004–2005. "
        "Actual result: BPO sector set all-time records."
    ),
    severity       = "medium",
    synthesis_sources = ["gopal-ch14-nadi-transit-rules", "gopal-ch14-industrial-sector-engine"],
)


# ════════════════════════════════════════════════════════════════════════════
# MASTER LIST
# ════════════════════════════════════════════════════════════════════════════
ALL_RULES = [
    # GROUP AO
    AO_1, AO_2, AO_3, AO_4, AO_5, AO_6, AO_7, AO_8,
    # GROUP AP
    AP_1, AP_2, AP_3, AP_4, AP_5, AP_6,
    # GROUP AQ
    AQ_1, AQ_2, AQ_3, AQ_4,
    # GROUP AR
    AR_1, AR_2, AR_3, AR_4, AR_5,
    # GROUP AS
    AS_1, AS_2, AS_3, AS_4, AS_5,
]


async def run():
    if DRY_RUN:
        print(f"[DRY RUN] Would upsert {len(ALL_RULES)} rules into interpretation_rules.")
        by_group = {}
        for r in ALL_RULES:
            g = r["rule_id"].split("-")[3].upper() if len(r["rule_id"].split("-")) > 3 else "?"
            by_group.setdefault(g, []).append(r["rule_id"])
        for g, ids in sorted(by_group.items()):
            print(f"  GROUP {g}: {len(ids)} rules")
            for rid in ids:
                print(f"    {rid}")
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
        print(f"  ✓ {rule['rule_id']}")
    client.close()
    print(f"\nUpserted {ok} rules into interpretation_rules.")


if __name__ == "__main__":
    asyncio.run(run())
