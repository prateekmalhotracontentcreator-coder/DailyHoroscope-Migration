"""
Mundane Astrology — Engine Specs INGEST v18
===========================================
Batch : mundane-engine-v18-20260507
Collection : mundane_engine_specs
Science    : mundane_jyotish

Chapters encoded:
  Gopal Ch 5  — Oath Taking Charts
                12-House Mundane Classification (all 12 houses)
                Jaimini Ayurdaya tenure longevity logic
                Oath chart stability vetoes (Rasi Sandhi, Graha Yuddha)
                Case studies: Manmohan Singh 2004, Oommen Chandy 2004

  Mehta Ch 18 — Importance of Muhurta in Oath Taking
                11-Point Lagna Selection Protocol
                Luminaries vetting (Sun 4pts + Moon 7pts)
                Nakshatra vetting (6pts) + Tithi vetting (7pts) + 4 Muhurta factors
                5-Year Compressed Vimshottari Dasha Timer (all 9 planets, values in days)
                Simhasan Chakra — Tri-Simhasan (Narapati/Gajapati/Ashwapati)
                  complete 27-nakshatra mapping to 5 Nadi levels + 8 operational rules
                Leadership Autopsy Database
                  (Shastri 1964, Chandrashekhar 1990, Narasimha Rao 1991,
                   Mulayam Singh 1993, Vajpayee 1996, Manmohan Singh 2004)

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

_BATCH = "mundane-engine-v18-20260507"
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
# SPEC 1 — Gopal Ch 5: 12-House Mundane Grid for Oath Charts
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH5_OATH_12_HOUSE_GRID = _spec(
    spec_id   = "gopal-ch5-oath-chart-12-house-grid",
    spec_type = "house_signification_table",
    title     = "Oath Chart 12-House Mundane Classification — Gopalakrishnan Ch 5",
    source    = "gopalakrishnan_ch5",
    description = (
        "Gopalakrishnan Ch 5 defines the Oath Taking Chart as the actual 'birth chart' "
        "of an administration. This spec contains the complete 12-house functional grid "
        "specific to oath/swearing-in horoscopes — distinct from the standard mundane "
        "house classifications. Each house governs a specific governance sector, "
        "ministerial performance, or stability metric."
    ),
    oath_house_significations = {
        "house_01": (
            "Leader's personality, the first 100 days of rule, "
            "success in projecting a positive image, and the ability to outwit political opponents."
        ),
        "house_02": (
            "State finances, the leader's communication style, "
            "ability to manage close confidants, and influence over mass media."
        ),
        "house_03": (
            "Relationships with the party cadre, courage in decision-making, "
            "approval of new policies, and interstate travel."
        ),
        "house_04": (
            "Agricultural output, rainfall, educational policies, "
            "vehicle/infrastructure, and support from women and the 'High Command'."
        ),
        "house_05": (
            "Leader's intuition and luck, future-oriented policies, "
            "mass deaths of children, and survival of assassination attempts."
        ),
        "house_06": (
            "Policy failures, exposure of scams, pressure from the political High Command, "
            "state debts, and the leader's health/policing."
        ),
        "house_07": (
            "Foreign travel, strength and nature of the political opposition, "
            "and success in trade negotiations."
        ),
        "house_08": (
            "Functional longevity of the government, mass deaths, "
            "scams emerging at end of tenure, and unforeseen natural calamities."
        ),
        "house_09": (
            "The Judiciary, judges, religious values, the rule of law, "
            "and the influence of main party leaders (High Command)."
        ),
        "house_10": (
            "Overall administrative success, mass appeal, "
            "and the functional longevity of the government's power."
        ),
        "house_11": (
            "Government income and revenue streams, "
            "implementation of financially rewarding policies."
        ),
        "house_12": (
            "Government losses, the 'last days' of an administration, "
            "the transition to the next government, and financial mismanagement."
        ),
    },
    critical_monitoring_points = {
        "8th_house_veto": (
            "The 8th house controls functional longevity. Malefics here signal severe "
            "governance trouble or the leader's death in office."
        ),
        "11th_in_8th_market_rule": (
            "If the 11th lord (revenue/gains) is placed in the 8th house, "
            "foreign reserves and stock market performance will be lower than the "
            "preceding administration."
        ),
        "6th_9th_synergy": (
            "If the 6th lord (High Command pressure) is stronger than the 9th lord "
            "(Judiciary), the government is paralysed by internal party dictates."
        ),
        "12th_in_10th_terminal": (
            "If the 12th lord is in the 10th house, the administration is already "
            "entering its final phase — focus has shifted to the next election."
        ),
        "5th_jupiter_protection": (
            "If Jupiter aspects the 5th house, the leader has high ability to survive "
            "physical threats and assassination attempts."
        ),
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 2 — Gopal Ch 5: Jaimini Ayurdaya Tenure Longevity
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH5_JAIMINI_TENURE = _spec(
    spec_id   = "gopal-ch5-jaimini-tenure-longevity",
    spec_type = "calculation_engine",
    title     = "Jaimini Ayurdaya Tenure Longevity — Oath Chart Sign-Type Comparison",
    source    = "gopalakrishnan_ch5",
    description = (
        "The Jaimini Ayurdaya method determines whether a government will complete its "
        "full mandate by comparing the sign types (Moving/Fixed/Dual) of the Lagna lord "
        "and the 8th lord in the oath-taking chart. The Hora Lagna provides an additional "
        "fixed-sign veto. A government's survival depends more on this mathematical "
        "configuration than on its parliamentary majority."
    ),
    jaimini_calculation_method = "Compare sign type of Lagna Lord vs sign type of 8th Lord",
    sign_type_reference = {
        "moving_chara": ["Aries", "Cancer", "Libra", "Capricorn"],
        "fixed_sthira": ["Taurus", "Leo", "Scorpio", "Aquarius"],
        "dual_dwiswabhava": ["Gemini", "Virgo", "Sagittarius", "Pisces"],
    },
    longevity_gates = {
        "full_term_long_life": {
            "condition": "Both lords in Moving signs OR one in Fixed and one in Dual sign",
            "result": "Government likely to complete full 5-year mandate with stability.",
            "validation": "Vajpayee 1998 oath — completed full term.",
        },
        "medium_life": {
            "condition": "Both lords in Dual signs OR one in Moving and one in Fixed sign",
            "result": "Failure to complete full mandate; likely collapse around 3 years.",
            "validation": "Manmohan Singh 2004 — predicted medium life; did not complete cleanly.",
        },
        "short_life_exit": {
            "condition": "Both lords in Fixed signs OR one in Moving and one in Dual sign",
            "result": "Early collapse or resignation within first 1–2 years.",
            "validation": "Oommen Chandy 2004 — both Fixed → predicted early exit, confirmed.",
        },
    },
    hora_lagna_veto = (
        "If BOTH Lagna AND Hora Lagna are in Fixed signs, the 'Survival Probability' "
        "is reduced to 0.10 — this is a terminal early-exit configuration."
    ),
    rasi_sandhi_coefficient = (
        "If 4+ planets are in Rasi Sandhi (0° or 29°), the 'Effective Governance' "
        "coefficient is reduced to 0.20. Triggers: 'Stability Alert: Administrative "
        "paralysis predicted due to planetary sandhi'."
    ),
    graha_yuddha_veto = (
        "Planets in Graha Yuddha (Planetary War) in the oath chart act as terminal "
        "Stability Vetoes — the government cannot rule peacefully regardless of majority. "
        "Validation: Saturn-Venus Graha Yuddha in Oommen Chandy 2004 chart confirmed early exit."
    ),
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 3 — Gopal Ch 5: Oath Chart Case Study Validation Database
# ═════════════════════════════════════════════════════════════════════════════
GOPAL_CH5_OATH_CASE_STUDIES = _spec(
    spec_id   = "gopal-ch5-oath-case-studies",
    spec_type = "case_study_database",
    title     = "Oath Chart Case Studies — Manmohan Singh 2004 + Oommen Chandy 2004",
    source    = "gopalakrishnan_ch5",
    description = (
        "Empirically validated oath-chart case studies from Gopalakrishnan Ch 5. "
        "These provide the 'Truth Anchor' calibration for the Tenure Engine, proving "
        "that structural flaws in the swearing-in chart override parliamentary majorities."
    ),
    case_studies = {
        "manmohan_singh_2004": {
            "oath_timestamp": "2004-05-22T17:34:08",
            "longevity_audit": {
                "lagna_type": "Moving (Libra)",
                "hora_lagna_type": "Fixed (Scorpio)",
                "calculated_tenure": "Medium Life — predicted ~3 years or failure to complete full mandate",
                "structural_weakness": "Lagna lord and 8th lord both in dual signs from Moon lagna",
            },
            "governance_diagnostics": {
                "administrative_freedom": (
                    "9th house saturation (many planets) = 'many bosses'; "
                    "High Command pressure constrains decision-making."
                ),
                "coalition_friction": (
                    "Moon, Mars, and Mercury in close degrees = intense partnership bickering."
                ),
                "market_seed": (
                    "11th lord in 8th house = lower foreign reserves and less impressive "
                    "stock performance than the preceding regime."
                ),
            },
            "universal_rules_extracted": [
                "IF (11th lord in 8th) THEN 'Economic underperformance vs prior admin'",
                "IF (9th house has 3+ planets) THEN 'Many Bosses governance constraint'",
                "IF (Moon/Mars/Mercury within 3° of each other) THEN 'Partner bickering'",
            ],
        },
        "oommen_chandy_2004": {
            "oath_timestamp": "2004-08-31T12:31:23",
            "longevity_audit": {
                "lagna_type": "Fixed (Scorpio)",
                "hora_lagna_type": "Fixed (Aquarius)",
                "calculated_tenure": "Short Life — predicted early collapse; failure to survive until next election",
            },
            "rasi_sandhi_failure": {
                "sandhi_cluster": "Four planets (Venus, Jupiter, Moon, Saturn) in Rasi Sandhi (0° or 29°)",
                "planetary_war": "Saturn and Venus in Graha Yuddha depleting structural integrity",
                "eighth_house_hit": "Saturn in 8th house — traditional marker for severe governance problems",
            },
            "universal_rules_extracted": [
                "IF (4+ planets in Rasi Sandhi) AND (Lagna + Hora Lagna both Fixed) THEN 'Early collapse guaranteed'",
                "IF (Saturn in 8th AND in Graha Yuddha) THEN 'Terminal instability'",
            ],
        },
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 4 — Mehta Ch 18: 11-Point Lagna Selection Protocol
# ═════════════════════════════════════════════════════════════════════════════
MEHTA_CH18_LAGNA_SELECTION = _spec(
    spec_id   = "mehta-ch18-lagna-selection-11-points",
    spec_type = "muhurta_protocol",
    title     = "Mehta Ch 18 — 11-Point Oath-Taking Lagna Selection Protocol",
    source    = "mehta_ch18",
    description = (
        "Mehta Ch 18 establishes that the Muhurta (auspicious timing) of an oath-taking "
        "ceremony is the administration's 'Destiny Seed'. This spec contains the "
        "complete 11-point protocol for selecting the correct Lagna for any "
        "coronation or swearing-in ceremony, followed by 4 core longevity gates."
    ),
    lagna_selection_11_points = {
        "01_shirshodaya_preference": (
            "Prefer Shirshodaya signs: Gemini, Leo, Virgo, Libra, Scorpio, Aquarius. "
            "Aries and Pisces are also acceptable."
        ),
        "02_lagna_lord_self_aspect": (
            "Ideally the Lagna should be associated with or aspected by its own lord."
        ),
        "03_lunar_relative_position": (
            "The rising sign should fall in the 3rd, 6th, or 11th position from the leader's natal Moon."
        ),
        "04_benefic_presence": (
            "Lagna lord or benefics must occupy the Lagna. "
            "Malefics in the Lagna cause cabinet bickering and government unpopularity."
        ),
        "05_papakatari_veto": (
            "The Lagna must NOT be hemmed in by malefics on both sides (Papakatari Yoga)."
        ),
        "06_dispositor_strength": (
            "Lagna lord and its dispositor must be strong — not in 6th, 8th, or 12th; "
            "lord should not be combust or squared by malefics."
        ),
        "07_raman_libra_rule": (
            "Libra Lagna with an aspect from Jupiter is considered ideal for the election "
            "of a Head of State (B.V. Raman rule)."
        ),
        "08_coalition_lord_harmony": (
            "In coalition governments: Lagna lord and 7th lord must NOT be mutual enemies "
            "or placed in 6th/8th/12th from each other."
        ),
        "09_longevity_mathematics": (
            "8th house should receive benefic aspects; Lagna lord must be mathematically "
            "stronger than the 8th lord."
        ),
        "10_royal_coalition_risk": (
            "Rising Cancer or Leo Lagna = 'Partner Discord Alert' — Saturn becomes the 7th lord, "
            "creating constant coalition bickering."
        ),
        "11_capricorn_exclusion": (
            "Capricorn is generally NOT recommended — it is a Chara (movable) rashi with "
            "inherent enmity between its lord (Saturn) and 7th lord (Moon)."
        ),
    },
    core_longevity_gates = {
        "fixed_sign_stability": (
            "Fixed signs (Taurus, Leo, Scorpio, Aquarius) are mandatory for longevity. "
            "Moving signs indicate a short-lived cabinet."
        ),
        "eighth_house_vacancy": (
            "The 8th house MUST be vacant. Malefics in the 8th (especially Mars) "
            "signal severe governance trouble or the leader's death in office."
        ),
        "lagna_lord_dominance": (
            "Lagna lord must be stronger than the 8th lord and situated in a Kendra or Trikona."
        ),
        "papakatari_check": (
            "Lagna should not be hemmed in by malefics — causes unpopularity and inter-party bickering."
        ),
    },
    raman_democratic_lagnas = {
        "aquarius_with_saturn": "Aquarius rising with Saturn in Lagna — ideal for democratic rule",
        "libra_with_jupiter": "Libra aspected by Jupiter/Venus — optimal for democratic Head of State",
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 5 — Mehta Ch 18: Luminaries + Nakshatra + Tithi Vetting
# ═════════════════════════════════════════════════════════════════════════════
MEHTA_CH18_LUMINARIES_VETTING = _spec(
    spec_id   = "mehta-ch18-luminaries-nakshatra-tithi-vetting",
    spec_type = "muhurta_vetting_checklist",
    title     = "Mehta Ch 18 — Luminaries, Nakshatra & Tithi Vetting for Oath Ceremony",
    source    = "mehta_ch18",
    description = (
        "Detailed vetting checklist for the Sun (4 points), Moon (7 points), "
        "Nakshatras (6 points), and Tithis (7 points) in the oath-taking Muhurta, "
        "plus the 4 final Muhurta judgment factors. "
        "These filters are applied after the Lagna is selected."
    ),
    sun_strength_4_points = {
        "01_ideal_placement": "Placement in own sign Leo or exaltation Aries; best if aspected by Jupiter.",
        "02_house_priority": "Posited in 3rd (Valour), 10th (Directional Strength), or 6th/11th (Upchayya/Growth).",
        "03_uttarayana_veto": "Traditional rule: Coronation should occur when Sun is in Uttarayana (Capricorn to Gemini).",
        "04_avoidance_zones": (
            "Avoid Sun in Pisces and during Rikta Tithis (4th, 9th, 14th lunar days). "
            "Note: Astrologers often work within constitutional limits (India's July presidency, "
            "US Jan 20th) — choice is frequently constrained by convention."
        ),
    },
    moon_strength_7_points = {
        "01_dignity": "Moon in own sign Cancer, preferably aspected by Jupiter.",
        "02_longevity_check": "Placement in 6th, 8th, or 12th house is negative for government's lifespan.",
        "03_tara_shuddhi": "Must verify strength in transit relative to the leader's natal Moon.",
        "04_administrative_power": "10th house must be strong for long-term government durability.",
        "05_benefic_angularity": "Benefics should occupy Kendras or Trikonas.",
        "06_malefic_containment": "Malefics are ideally contained in houses 3, 6, or 11.",
        "07_eighth_house_vacancy": "The 8th house must remain vacant for structural stability.",
        "note": "Requires the correct horoscope of the leader — often unavailable/disputed in modern politics.",
    },
    nakshatra_6_points = {
        "01_short_extolled": "Short constellations (Hasta, Ashwini, Pushya) and Abhijit are ideal.",
        "02_friendly_stars": "Mrigshira, Revati, Chitra, and Anuradha are considered auspicious.",
        "03_fixed_foundation": "Fixed stars (U.Phalguni, U.Ashadha, U.Bhadrapada, Rohini) are preferred.",
        "04_movable_sharp_rule": "Shravana (movable) and Jyeshtha (sharp) are acceptable — avoid last part of Jyeshtha.",
        "05_yama_agni_exclusion": "Avoid Bharani (Yama's star) and Krittika (Agni) for coronation ceremonies.",
        "06_terminal_sandhi_veto": "Avoid the final segments (Gandanta) of Ashlesha, Jyeshtha, and Revati.",
    },
    tithi_7_points = {
        "01_rikta_avoidance": "Exclude 4th, 9th, and 14th lunar days (Rikta/Empty Tithis).",
        "02_preferred_weekdays": "Sunday, Monday, Thursday, and Friday are optimal swearing-in days.",
        "03_dasha_compression": "Check sequence using the compressed 5-year Vimshottari cycle.",
        "04_bright_half_preference": "All lunar days in the bright half (except 9th) are good; 2nd and 10th specifically recommended.",
        "05_raman_stability_lagna": "Aquarius rising with Saturn in Lagna or Libra aspected by Jupiter/Venus — for democratic rule.",
        "06_janma_exception": "Unlike general elections, Janma Nakshatra is considered FAVORABLE for a coronation.",
        "07_varga_audit": "Malefics should not be strong in Shadhvargas.",
        "additional_veto": "Mars should NOT be in 8th house even if exalted or in own sign.",
    },
    muhurta_judgment_4_factors = [
        "Rising of an auspicious Lagna",
        "Selection of a good lunar day (Tithi)",
        "Selection of a good week day",
        "Panchak consideration (avoid the last 5 nakshatras)",
    ],
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 6 — Mehta Ch 18: 5-Year Compressed Vimshottari Dasha Timer
# ═════════════════════════════════════════════════════════════════════════════
MEHTA_CH18_COMPRESSED_DASHA = _spec(
    spec_id   = "mehta-ch18-compressed-dasha-5yr-timer",
    spec_type = "calculation_table",
    title     = "Mehta Ch 18 — 5-Year Compressed Vimshottari Dasha for Government Mandates",
    source    = "mehta_ch18",
    description = (
        "Mehta Ch 18 introduces the 5-Year Governance Dasha: a mathematical compression "
        "of the 120-year Vimshottari cycle into a standard 5-year government mandate. "
        "This allows the Mundane Engine to time specific policy periods, market shifts, "
        "war windows, and administrative collapses within any government's term using "
        "the sequence of Dasha lords from the oath-taking chart."
    ),
    formula = "Compressed_Days = (Planet_Vimshottari_Years * 5) / 120",
    compressed_dasha_table_days = {
        "ketu":    {"vimshottari_years": 7,  "compressed_days": 106},
        "venus":   {"vimshottari_years": 20, "compressed_days": 304},
        "sun":     {"vimshottari_years": 6,  "compressed_days": 91},
        "moon":    {"vimshottari_years": 10, "compressed_days": 152},
        "mars":    {"vimshottari_years": 7,  "compressed_days": 106},
        "rahu":    {"vimshottari_years": 18, "compressed_days": 274},
        "jupiter": {"vimshottari_years": 16, "compressed_days": 244},
        "saturn":  {"vimshottari_years": 19, "compressed_days": 289},
        "mercury": {"vimshottari_years": 17, "compressed_days": 259},
    },
    usage_examples = {
        "military_assertion": (
            "If the government is in Sun-Mars sub-period (~15 days in compressed scale) "
            "during a border clash, the 'Military Assertion' coefficient is set to 0.95 "
            "(Highly Aggressive)."
        ),
        "economic_policy_window": (
            "Venus period (304 days) is the longest and governs economic reforms, "
            "foreign investment, and luxury-sector growth."
        ),
        "collapse_risk_window": (
            "Saturn period (289 days) combined with a malefic 8th house in the oath chart "
            "signals the maximum 'Administrative Collapse' risk window."
        ),
    },
    note = (
        "The sequence of Dashas starts from the Dasha lord active at the exact time "
        "of the oath-taking ceremony. Run through all 9 periods sequentially, "
        "wrapping back to the start after Mercury."
    ),
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 7 — Mehta Ch 18: Simhasan Chakra (Complete Tri-Simhasan)
# ═════════════════════════════════════════════════════════════════════════════
MEHTA_CH18_SIMHASAN_CHAKRA = _spec(
    spec_id   = "mehta-ch18-simhasan-chakra-complete",
    spec_type = "nakshatra_authority_grid",
    title     = "Mehta Ch 18 — Simhasan Chakra (Panch Nadi) — Complete 27-Nakshatra Throne Map",
    source    = "mehta_ch18",
    description = (
        "The Simhasan Chakra (also known as Panch Nadi Chakra) maps all 27 Nakshatras "
        "into five hierarchical authority levels, ranging from Aadhaar (Public Base) "
        "to Simhasan (Absolute Throne). The 27 stars are divided into three Tri-Simhasan "
        "groups (Narapati / Gajapati / Ashwapati). The Moon's placement in this grid "
        "overrides standard house analysis for determining a leader's authority and "
        "the government's durability."
    ),
    tri_simhasan_classification = {
        "simhasan_I_narapati": "Nakshatras 1–9 (Ashwini to Ashlesha) — Lord of Men / civilian base",
        "simhasan_II_gajapati": "Nakshatras 10–18 (Magha to Jyeshtha) — Lord of Elephants / institutional strength",
        "simhasan_III_ashwapati": "Nakshatras 19–27 (Moola to Revati) — Lord of Horses / executive mobility",
    },
    nadi_power_levels = {
        "05_simhasan_throne": {
            "authority": "Peak / Absolute power — the King's throne",
            "lord": "Mars",
            "stars": ["Mrigshira (5)", "Chitra (14)", "Dhanishtha (23)"],
            "nakshatra_count": 3,
        },
        "04_simha_royalty": {
            "authority": "The Executive — Prime Minister and Core Cabinet",
            "lords": ["Moon", "Rahu"],
            "stars": ["Rohini (4)", "Aridra (6)", "Hasta (13)", "Swati (15)", "Shravana (22)", "Shatbhisha (24)"],
            "nakshatra_count": 6,
        },
        "03_patta_ministers": {
            "authority": "Council of Ministers / Limited or moderate power",
            "lords": ["Sun", "Jupiter"],
            "stars": ["Krittika (3)", "Punarvasu (7)", "U.Phalguni (12)", "Vishakha (16)", "U.Ashadha (21)", "P.Bhadrapada (25)"],
            "nakshatra_count": 6,
        },
        "02_aasan_bureaucracy": {
            "authority": "Civil Service and Administration — the support layer",
            "lords": ["Venus", "Saturn"],
            "stars": ["Bharani (2)", "Pushya (8)", "P.Phalguni (11)", "Anuradha (17)", "P.Ashadha (20)", "U.Bhadrapada (26)"],
            "nakshatra_count": 6,
        },
        "01_aadhaar_public": {
            "authority": "General Public Base — foundation of the administration",
            "lords": ["Ketu", "Mercury"],
            "stars": ["Ashwini (1)", "Ashlesha (9)", "Magha (10)", "Jyeshtha (18)", "Moola (19)", "Revati (27)"],
            "nakshatra_count": 6,
        },
    },
    operational_rules_8_points = {
        "01_chart_foundation": "Establish the oath horoscope and map all planets into Nadi levels.",
        "02_lunar_veto": "Moon is the primary anchor — strong Moon in Simhasan = longevity; afflicted = fragility.",
        "03_power_pedestal_audit": "Moon in Simhasan = Absolute Power; Simha = Executive; Aadhaar = Public-Dependent.",
        "04_ministerial_tiers": "Moon in Patta = Limited Authority, characterised by a weak council of ministers.",
        "05_saturnine_sabotage": "Saturn must NOT afflict Moon, Lagna, or 10th house — represents democratic destruction.",
        "06_stellar_affinity": "Saturn is prohibited from occupying malefic nakshatras within executive Nadis.",
        "07_terminal_aasan_hit": "Saturn in Aasan Nadi (esp. retrograde or with malefics) = Terminal Veto destroying rule.",
        "08_jupiter_protection": "Jupiter in Aasan Nadi = protective shield; leader receives bureaucratic adoration regardless of malefics.",
    },
    interpretive_heuristics = {
        "moon_authority_rule": "Moon in Simhasan = Absolute Power; Moon in Aadhaar = Reduced/Dependent Power",
        "martial_king_marker": "Moon in Simha Nadi conjunct Mars = leader is like a lion and leads nation into war (Shastri 1965)",
        "jupiter_protection": "Jupiter in Aasan Nadi = protective shield against administrative evil or collapse",
        "terminal_saturn": "Saturn in Aasan Nadi (especially retrograde) + malefics = destroys the administration",
        "dasha_lord_affinity": "If Dasha Lord of oath chart == Nadi Level Lord (e.g., Mars Dasha + Moon in Simhasan), power index × 2.0",
    },
    royal_title_trigger = {
        "simhasan_I_narapati": "Civilian mandate — administration draws power from the masses",
        "simhasan_II_gajapati": "Institutional mandate — draws power from established institutions",
        "simhasan_III_ashwapati": "Executive mobility — administration will prioritize swift action and military movement",
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# SPEC 8 — Mehta Ch 18: Leadership Autopsy Database (6 Case Studies)
# ═════════════════════════════════════════════════════════════════════════════
MEHTA_CH18_LEADERSHIP_AUTOPSIES = _spec(
    spec_id   = "mehta-ch18-leadership-autopsy-database",
    spec_type = "case_study_database",
    title     = "Mehta Ch 18 — Leadership Autopsy Database (6 Oath-Chart Case Studies)",
    source    = "mehta_ch18",
    description = (
        "Six empirically validated oath-chart autopsies from Mehta Ch 18, providing "
        "the calibration data for the Governance Stability Engine. Each case maps "
        "specific structural flaws (adverse features) or strengths to actual governance "
        "outcomes, proving that the 'Destiny Seed' planted at oath-taking time overrides "
        "parliamentary strength."
    ),
    case_studies = {
        "lal_bahadur_shastri_1964": {
            "oath_timestamp": "1964-06-09T11:20:00",
            "longevity_actual": "~1 Year (Died in office 11.01.1966)",
            "adverse_features_9": {
                "01": "Lagna lord Sun afflicted by Mars and squared by Saturn",
                "02": "10th house contains dark Moon (12th lord) afflicted by Mars/Saturn",
                "03": "Lagna directly afflicted by both Saturn and Mars",
                "04": "10th lord Venus posited within the Rahu-Ketu axis",
                "05": "Jupiter afflicted by the aspect of Saturn",
                "06": "Mercury joined with malefics — lost its benefic character",
                "07": "Total absence of benefic planets in Kendras (quadrants)",
                "08": "No favorable Tajik yogas; 10th lord Venus retrograde in 'Radda' yoga with Saturn",
                "09": "Lagna/10th have low Ashtakvarga points (24/26); Venus only 4 points in Bhinnashtak",
            },
            "simhasan_pattern": "Moon in Simha Nadi conjunct Mars = Martial King (led 1965 war successfully). Physical vulnerability pattern: Moon close to Sun/Mars depleted physical luster.",
        },
        "chandrashekhar_1990": {
            "oath_timestamp": "1990-11-10T11:00:00",
            "longevity_actual": "Short-lived transitionary government",
            "adverse_features_5": {
                "01": "Moon in Ketu's nakshatra and afflicted by Mars",
                "02": "Malefic Saturn occupies Lagna — heavy burdens and short tenure",
                "03": "Direct affliction of Lagna by Mars",
                "04": "Lagna lord Jupiter in 8th house within the Rahu-Ketu axis",
                "05": "10th lord Mercury displaced to 12th house (Loss)",
            },
            "universal_rule": "IF (Lagna lord in 8th) AND (10th lord in 12th) THEN 'Early collapse within 12 months'",
        },
        "pv_narasimha_rao_1991": {
            "oath_timestamp": "1991-06-21T12:52:00",
            "longevity_actual": "Full Term (inherited bankrupted economy, achieved liberalisation)",
            "positive_features_7": {
                "01": "Strong Lagna and 10th lord in 10th in own rashi with Sun (Directional Strength)",
                "02": "11th lord in 2nd house = national economic prosperity",
                "03": "Jupiter aspects 10th house + exalted 9th lord",
                "04": "Mars in Neechbhanga (cancellation of debilitation) = economic rebirth",
                "05": "Guru-Souri Yoga: Saturn in own house aspected by Jupiter",
                "06": "2nd-5th-11th lord connection = Liberalisation Dhana Yoga",
                "07": "Venus afflicted by debilitated Mars + 6th lord Saturn = bribery/Urea scandals",
            },
            "universal_rule": "IF (2nd, 5th, 11th lords connect) THEN 'Economic Liberalisation Signal — foreign investment influx'",
        },
        "mulayam_singh_yadav_1993": {
            "oath_timestamp": "1993-12-14T11:34:00",
            "longevity_actual": "~1.5 Years (Replaced by Mayawati 03.06.1995)",
            "adverse_features_8": {
                "01": "Lagna lord and 7th lord are mutual enemies — coalition stability critically low",
                "02": "7th lord (Coalition Partner Sun) afflicted by Saturn, Mars, and 8th lord Mercury",
                "03": "10th lord Venus under influence of Rahu, Mars, Sun, and 12th lord Saturn",
                "04": "Lagna lord Saturn and 10th lord Mars lack favorable Tajik yogas",
                "05": "Dasha lord Mercury poorly placed in vargas; in Papakatari yoga",
                "06": "Fixed lagna with Saturn in dignity but aspected by weak (debilitated navamsha) Jupiter",
                "07": "Malefic nakshatra Ashlesha with Saturn in kendra; all benefics weak",
                "08": "8th lord Mercury (5 bindus) stronger than lagna lord Saturn (3 bindus) = early collapse",
            },
            "ashtakvarga_rule": "IF (8th lord bindus > lagna lord bindus in Bhinnashtak) THEN 'Early governance collapse'",
        },
        "vajpayee_1996": {
            "oath_timestamp": "1996-05-16T12:03:00",
            "longevity_actual": "13 Days (shortest government in Indian history)",
            "adverse_features_8": {
                "01": "Swearing-in in Rasi Sandhi in Magha nakshatra (Ketu) — extreme instability",
                "02": "Moon in Bharani nakshatra (Yama/God of Death) — unsuitable for muhurta",
                "03": "Lagna lord Sun has directional strength but occupies 'Mrityubhag' (death degree)",
                "04": "Sun in enemy's sign (Venus) afflicted by Saturn and Rahu",
                "05": "Moon conjunct Mercury (2nd/11th lord) acting as maraka for this lagna",
                "06": "Saturn with Ketu in 8th house = 'Balarishta' (early death) chart",
                "07": "Total absence of benefic planets in Kendras",
                "08": "Jupiter in 6th house moving toward debilitation — saviour was too weak",
            },
            "sandhi_bharani_rule": (
                "IF (Oath in Rasi Sandhi) AND (Moon in Bharani) THEN 'Longevity Index = 0.05 (Critically Short)'"
            ),
        },
        "manmohan_singh_2004_mehta": {
            "oath_timestamp": "2004-05-22T17:34:00",
            "longevity_actual": "Medium — completed with severe constraints (K.N. Rao JOAS Jul-Sep 2004 audit)",
            "diagnostic_features_15": {
                "01": "Ketu/Rahu axis in close proximity to the Lagna",
                "02": "Malefic Rahu in 7th house (Partners/Coalition)",
                "03": "Royal planet Sun displaced to 8th house of destruction",
                "04": "Retrograde Venus in Gemini with Saturn and Mars — Gemini Venus causes Central Govt crises",
                "05": "India's lagna lord Venus retrograde (associated with 9th lord Moon)",
                "06": "Saturn acts as primary yogakaraka for the administration",
                "07": "7th lord Mars in 9th — unwelcome for coalition alliances",
                "08": "Saturn-Mars conjunct aspected by Ketu = destructive communal situations",
                "09": "Afflicted 7th house/lord prevents major foreign policy breakthroughs",
                "10": "Excessive Sundays, Tuesdays, Saturdays in the lunar month = instability",
                "11": "10th lord Moon in 9th (12th from own sign) with malefics = lack of decision-making power",
                "12": "Mercury in 7th with Rahu = manipulative partners; Mercury as 12th lord is harmful",
                "13": "Rahu rules leftist forces — strong leftist influence on government policy",
                "14": "Jupiter's aspect on 7th house = sole protective shield",
                "15": "Malefics concentrated in Kendras — prevents peaceful or long life",
            },
            "many_bosses_rule": "IF (10th lord in 9th with malefics) AND (Rahu in 7th) THEN 'Many Bosses: leader lacks executive autonomy'",
        },
    },
)


# ═════════════════════════════════════════════════════════════════════════════
# RUNNER
# ═════════════════════════════════════════════════════════════════════════════
ALL_SPECS = [
    GOPAL_CH5_OATH_12_HOUSE_GRID,
    GOPAL_CH5_JAIMINI_TENURE,
    GOPAL_CH5_OATH_CASE_STUDIES,
    MEHTA_CH18_LAGNA_SELECTION,
    MEHTA_CH18_LUMINARIES_VETTING,
    MEHTA_CH18_COMPRESSED_DASHA,
    MEHTA_CH18_SIMHASAN_CHAKRA,
    MEHTA_CH18_LEADERSHIP_AUTOPSIES,
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
