"""
Mundane Astrology — Engine Specs v15
Batch: mundane-engine-v15-20260506

Sources:
  Gaur Ch 10 — Transit Price Matrix: Mars (12 signs + 27 constellations + motion states)
  Gaur Ch 10 — Transit Price Matrix: Mercury (12 signs + 27 constellations + motion states)
  Gaur Ch 10 — Transit Price Matrix: Jupiter (12 signs + 27 constellations + motion states)
  Gaur Ch 10 — Transit Price Matrix: Venus (12 signs + motion states + direct ingress)
  Gaur Ch 10 — Transit Price Matrix: Rahu (12 signs)
  Gaur Ch 10 — Synthesis Engine (Step 4 — weighted majority-vote methodology)
  Mehta Ch 7  — Koorma Chakra reconciliation (tribal/modern geography granularity +
                Destruction of Kings kill-switch + planetary directional vectors)

7 engine specs in this batch.

science_id: mundane_jyotish
Collection: mundane_engine_specs

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
COLLECTION = "mundane_engine_specs"
_BATCH     = "mundane-engine-v15-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True

# ============================================================
# SPEC 1: Mars Transit Price Matrix
# ============================================================

GAUR_CH10_MARS_TRANSIT = {
    "spec_id":        "gaur-ch10-mars-transit-price-matrix",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "transit_price_lookup",
    "title":          "Transit Price Matrix — Mars (12 Signs + 27 Constellations + Motion States)",
    "source_chapter": "Gaur/AIFAS Ch 10",
    "description": (
        "Mars is the 'Minute Hand' of mundane events — the igniter of wars, fires, and sudden price spikes. "
        "Sign transit: 15 days to 1 month. Constellation: 12–24 days. "
        "Direct vs. Retrograde produce opposite effects."
    ),
    "metadata": {
        "planet":          "Mars",
        "nature":          "Fiery / Violent / Disruptive",
        "primary_significations": ["Armed Forces", "War", "Fires", "Assassinations", "Explosions", "Surgery", "Copper", "Red Chillies", "Masoor Dal"],
        "sign_duration":   "15 days to 1 month",
        "constellation_duration": "12 to 24 days",
        "price_rise_offset": "5 days after Mars rises",
    },
    "transit_sign_results": {
        "aries":       {"expensive": ["Gold", "Silver", "Gems", "Jute products", "Cotton clothes", "Woolen clothes"], "cheap": ["Grains"]},
        "taurus":      {"expensive": ["Grains", "Red colour goods", "Clothes", "Gold", "Silver", "Copper", "Metals", "Oils"]},
        "gemini":      {"expensive": ["Gur", "Khand", "Copper", "Red things"], "logic": "Benefic conjunction lowers prices; Malefic conjunction elevates prices."},
        "cancer":      {"cheap": ["Grains", "Gur", "Khand", "Oils", "Oil materials"]},
        "leo":         {"expensive": ["Grains", "Gur", "Khand", "Gold", "Silver", "Red things", "Red clothes"]},
        "virgo":       {"expensive": ["Wheat", "Gram", "Red things", "Gold"]},
        "libra":       {"expensive": ["Grains", "Pulses", "Jute", "Cotton", "Yarn"]},
        "scorpio":     {"expensive": ["Grains", "Gur", "Khand", "Metals", "Gold", "Silver"]},
        "sagittarius": {"expensive": ["Grains", "Metals", "Gold", "Silver", "Oil materials", "Ghee"]},
        "capricorn":   {"expensive": ["Gur", "Khand", "Ghee", "Oil materials", "Metals", "Gold", "Silver"], "cheap": ["Grains"]},
        "aquarius":    {"expensive": ["Grains", "Gur", "Khand", "Gold"], "cheap": ["Cotton", "Silver"]},
    },
    "transit_constellation_results": {
        "ashwini":        {"expensive": ["Grains", "Gur", "Khand", "Sugar"], "cheap": ["Gold", "Silver"]},
        "bharani":        {"expensive": ["Grains", "Gold", "Silver", "Metals"]},
        "krittika":       {"expensive": ["Grains", "Moong", "Moth", "Pulses", "Ghee", "Silver"]},
        "rohini":         {"expensive": ["Oils", "Oil materials", "Red things", "Red chillies"]},
        "mrigshira":      {"expensive": ["Til (Sesame)", "Silver"], "cheap": ["Grains", "Pulses"]},
        "ardra":          {"expensive": ["Sesame", "Oil materials", "Gur", "Khand", "Cotton", "Salt"], "cheap": ["Silver"]},
        "punarvasu":      {"expensive": ["Oils", "Oil materials", "Silver", "Cotton", "Khand"]},
        "pushya":         {"expensive": ["Gold"], "cheap": ["Silver"]},
        "ashlesha":       {"expensive": ["Grains"], "cheap": ["Silver", "Cotton"], "special": "4th pad makes silver very cheap."},
        "magha":          {"expensive": ["Grains", "Pulses", "Oil materials"]},
        "poorvaphalguni": {"expensive": ["Oils", "Oil materials", "Gur", "Khand"]},
        "uttaraphalguni": {"expensive": ["Gur", "Khand", "Transport cattle"]},
        "hast":           {"expensive": ["Gur", "Khand", "Ghee", "Salt"]},
        "chitra":         {"expensive": ["Gold", "Silver", "Grains"]},
        "swati":          {"expensive": ["Wheat", "Oils", "Oil materials", "Woolen clothes"], "cheap": ["Gold"]},
        "vishakha":       {"expensive": ["Wheat", "Cotton", "Clothes"]},
        "anuradha":       {"expensive": ["Grains", "Red things", "Clothes"]},
        "jyeshtha":       {"expensive": ["Gold", "Grains"], "cheap": ["Silver"]},
        "mool":           {"expensive": ["Wheat", "Barley", "Gram", "Pulses", "Gold", "Silver"]},
        "poorvashadh":    {"expensive": ["Gold", "Silver", "Oils", "Oil materials", "Ghee"], "cheap": ["Grains"]},
        "revati":         {"expensive": ["Silver"], "cheap": ["Grains", "Pulses", "Gold"]},
    },
    "motion_state_logic": {
        "direct_motion":   "Fall in prices of cotton after 3 days; keeps oils and silver expensive.",
        "retrograde_motion": "Keeps gold, silver, wheat, red things, and goods influenced by own signs expensive.",
        "combusted_state": "Wheat, gram, and gur become expensive.",
        "rise_state":      "Grains become cheap; oils and oil materials become expensive after 5 days.",
    },
    "direct_ingress_by_sign": {
        "aries":       "Grains cheap",
        "taurus":      "Red things expensive",
        "gemini":      "Materials become very costly or cheap suddenly",
        "cancer":      "Herbs and vegetables expensive",
        "leo":         "Grains expensive",
        "virgo":       "Oils, oil materials, and wheat expensive",
        "libra":       "Grains expensive in West and South provinces",
        "scorpio":     "Harmful for cattle",
        "sagittarius": "Grains cheap",
        "capricorn":   "Grains medium; electronic goods cheap",
        "aquarius":    "Grains expensive",
        "pisces":      "Grains and ghee cheap",
    },
    "retrograde_entry_by_sign": {
        "aries":       "Grains expensive",
        "taurus":      "Red things expensive",
        "gemini":      "All goods become expensive or cheap gradually",
        "cancer":      "Grains fluctuate; herbs cheap",
        "leo":         "Grains cheap",
        "virgo":       "Wheat, oils, and oil materials cheap",
        "libra":       "Grains cheap",
        "scorpio":     "Cattle increase",
        "sagittarius": "Grains and ghee expensive",
        "capricorn":   "Wheat, electrical, and electronic goods expensive",
        "aquarius":    "Grains etc. cheap",
        "pisces":      "Grains and ghee expensive",
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 2: Mercury Transit Price Matrix
# ============================================================

GAUR_CH10_MERCURY_TRANSIT = {
    "spec_id":        "gaur-ch10-mercury-transit-price-matrix",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "transit_price_lookup",
    "title":          "Transit Price Matrix — Mercury (12 Signs + 27 Constellations + Motion States)",
    "source_chapter": "Gaur/AIFAS Ch 10",
    "description": (
        "Mercury governs trade, media, and communications. "
        "Malefic conjunctions give inauspicious results; benefic conjunctions give good results. "
        "'Noticeable changes occur in weather when Mercury changes signs/nakshatras'."
    ),
    "metadata": {
        "planet":          "Mercury",
        "nature":          "Intellectual / Commercial / Volatile",
        "primary_significations": ["Ambassadors", "Trade", "Newspapers", "Literature", "Sports", "Air Pollution", "Media", "Telecommunications"],
        "dual_nature_rule": "Malefic conjunction = inauspicious results; Benefic conjunction = good results.",
        "weather_pivot":    "Trigger 'Weather Disturbance Alert' whenever Mercury crosses a sign boundary.",
    },
    "transit_sign_results": {
        "aries":       {"cheap": ["Gur", "Khand", "Gram", "Oils", "Oil materials", "Gold", "Silver", "Gems"]},
        "taurus":      {"expensive": ["Grains", "Pulses", "Til", "Oils"]},
        "gemini":      {"cheap": ["Gold", "Silver"], "fluctuating": ["Oil materials"], "expensive": ["Cattle"]},
        "cancer":      {"medium": ["Grains"], "expensive": ["Gur", "Oils", "Oil materials"], "cheap": ["Silver", "White things"]},
        "leo":         {"medium": ["Grains"], "cheap": ["Gold", "Silver", "Gur", "Khand"]},
        "virgo":       {"expensive": ["Grains", "Gur", "Sugar"], "cheap": ["Silver"]},
        "libra":       {"expensive": ["Juicy materials", "Gur", "Khand", "Gold"], "cheap": ["Oil materials"]},
        "scorpio":     {"cheap": ["Grains"], "expensive": ["Oils", "Oil materials", "Ghee", "Silver"]},
        "sagittarius": {"cheap": ["Silver", "Cotton", "Yarn", "Clothes"]},
        "capricorn":   {"medium": ["Grains"], "expensive": ["Gold", "Silver"]},
        "aquarius":    {"expensive": ["Gur", "Khand", "Oils", "Ghee"], "cheap": ["Silver", "Cotton"]},
        "pisces":      {"cheap": ["Juicy materials", "Gur", "Khand", "Grains"]},
    },
    "transit_constellation_results": {
        "ashwini":         {"expensive": ["Wheat", "Gram", "Millet", "Pulses"], "cheap": ["Gur", "Khand", "Til", "Oil materials", "Silver"]},
        "bharani":         {"expensive": ["Wheat", "Rice"]},
        "krittika":        {"expensive": ["Grains", "Cotton"], "cheap": ["Silver"]},
        "rohini":          {"expensive": ["Oils", "Oil materials", "Gur", "Khand", "Cotton"], "cheap": ["Woolen and Silk clothes"]},
        "ardra":           {"cheap": ["Grains", "Til", "Moong", "Moth", "Pulses"]},
        "punarvasu":       {"cheap": ["Silver", "Cotton", "Yarn"]},
        "pushya":          {"cheap": ["Gold", "Silver"], "expensive": ["Gems", "Woolen clothes"]},
        "ashlesha":        {"expensive": ["Oils", "Oil materials", "Gur", "Khand", "Moong"]},
        "magha":           {"expensive": ["Wheat", "Gram", "Barley", "Yarn", "Clothes"]},
        "poorvaphalguni":  {"cheap": ["Grains", "Gur", "Khand"]},
        "uttaraphalguni":  {"expensive": ["Pulses"], "cheap": ["Cotton", "Silver"]},
        "hast":            {"cheap": ["Grains"]},
        "chitra":          {"expensive": ["Grains (slightly)"], "unstable": ["Cotton", "Silver"]},
        "swati":           {"cheap": ["Cotton"]},
        "vishakha":        {"cheap": ["Grains", "Cotton"]},
        "anuradha":        {"cheap": ["Gold", "Silver"], "medium": ["Grains"]},
        "jyeshtha":        {"expensive": ["Gur", "Khand", "Ghee", "Rice"]},
        "mool":            {"cheap": ["Grains", "Gold", "Silver"]},
        "poorvashadh":     {"cheap": ["Grains", "Gold", "Silver"]},
        "uttarashadh":     {"cheap": ["Grains"]},
        "shravan":         {"expensive": ["Gur", "Khand", "Rice", "Wheat"]},
        "dhanishtha":      {"cheap": ["Gold", "Silver"], "expensive": ["Grains", "Rice"]},
        "shatbhisha":      {"expensive": ["Grains"], "cheap": ["Gold", "Silver"]},
        "poorvabhadrapad": {"cheap": ["Grains", "Gold", "Copper", "Silver"]},
        "uttarabhadrapad": {"medium": ["Grains", "Gur", "Khand"]},
        "revati":          {"cheap": ["Juicy materials", "Gur", "Khand", "Oil materials", "Ghee", "Silver", "Red chillies"]},
    },
    "motion_and_luminous_logic": {
        "change_to_direct":   {"expensive": ["Grains", "Gur", "Perfumes"], "fluctuation": "Silver and cotton fluctuate then become expensive."},
        "retrograde_state":   {"expensive": ["Juicy materials", "Gur", "Khand"], "cheap": ["Grains"]},
        "rising_state":       {"expensive": ["Wheat", "Gram"]},
        "combusted_state":    {"cheap": ["Wheat", "Gram", "Ghee"]},
    },
    "direct_ingress_by_sign": {
        "aries":       "Cattle cheap",
        "taurus":      "Yarn, clothes, wheat, silver, sugar cheap",
        "gemini":      "Pulses cheap",
        "cancer":      "Silver, yarn, rice cheap; water-grown materials expensive",
        "leo":         "Cotton, jute, shares cheap",
        "virgo":       "Dry fruits expensive",
        "libra":       "Ghee, sugar, herbs expensive",
        "scorpio":     "Oil materials expensive",
        "sagittarius": "Gur, khand, rice expensive",
        "capricorn":   "Mustard cheap",
        "aquarius":    "Gold, leather expensive",
        "pisces":      "Gur, khand, oil materials cheap",
    },
    "retrograde_ingress_by_sign": {
        "aries":       "Grocery materials expensive",
        "taurus":      "Silver expensive",
        "gemini":      "Vegetables cheap",
        "cancer":      "Grains cheap",
        "leo":         "Grains, metals expensive",
        "virgo":       "Grains cheap",
        "libra":       "Gold expensive",
        "scorpio":     "Gur expensive",
        "sagittarius": "Dry fruits expensive",
        "capricorn":   "Oils and oil materials expensive",
        "aquarius":    "Gur, khand expensive",
        "pisces":      "Rice, ghee expensive",
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 3: Jupiter Transit Price Matrix
# ============================================================

GAUR_CH10_JUPITER_TRANSIT = {
    "spec_id":        "gaur-ch10-jupiter-transit-price-matrix",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "transit_price_lookup",
    "title":          "Transit Price Matrix — Jupiter (12 Signs + 27 Constellations + Motion States + Direct Sign Stay)",
    "source_chapter": "Gaur/AIFAS Ch 10",
    "description": (
        "Jupiter governs national wealth, treasury, and the judiciary. "
        "Transit determines macro-cycles of commodity abundance and the 'Establishment of Supremacy'. "
        "~1 year per sign."
    ),
    "metadata": {
        "planet":          "Jupiter",
        "nature":          "Expansive / Benevolent / Structural",
        "primary_significations": ["Religion", "Judiciary", "Finances", "International Cooperation", "Birth Rate", "Constitutional Governments"],
        "duration":        "~1 year per sign",
    },
    "transit_sign_results": {
        "aries":       {"expensive": ["Grains", "Oils", "Oil materials", "Ghee", "Metals"], "cheap": ["Grains (initially)"]},
        "taurus":      {"expensive": ["Grains", "Oils", "Metals (Gold/Silver)", "Cotton", "Ghee"]},
        "gemini":      {"expensive": ["Grains", "Oils", "Cotton", "Metals"]},
        "cancer":      {"expensive": ["Grains", "Gur", "Khand", "Ghee", "Cotton"]},
        "leo":         {"expensive": ["Grains", "Ghee"], "cheap": ["Gold", "Silver", "Copper"]},
        "virgo":       {"expensive": ["Grains", "Pulses", "Oils", "Oil materials", "Ghee"], "cheap": ["Cotton", "Silver", "Woolen clothes", "Metals"]},
        "libra":       {"expensive": ["Gold", "Cotton", "Coconut", "Gur", "Khand"], "cheap": ["Oils", "Oil materials", "Ghee"]},
        "scorpio":     {"expensive": ["Gold", "Silver", "Copper", "Oils", "Oil materials", "Ghee", "Gur", "White things"]},
        "sagittarius": {"cheap": ["Juicy materials", "Gur", "Khand", "Grains", "Oils", "Oil materials", "Ghee", "Gold", "Silver"]},
        "capricorn":   {"expensive": ["Grains", "Metals", "Peanuts"]},
        "aquarius":    {"cheap": ["Gold", "Silver", "White things (first 3 months)"], "expensive": ["Gold", "Silver (thereafter)"]},
        "pisces":      {"expensive": ["Juicy materials", "Gur", "Khand", "Pulses", "Til", "Oil materials", "Ghee"]},
    },
    "transit_constellation_results": {
        "ashwini":         {"cheap": ["Grains", "Gold", "Silver"]},
        "bharani":         {"cheap": ["Gold", "Silver", "Gems", "Grains", "Pulses"]},
        "krittika":        {"expensive": ["Gold", "Silver", "Copper", "Ghee", "Oils"]},
        "rohini":          {"expensive": ["Grains", "Gold", "Silver", "Ghee", "Oils", "Cotton"]},
        "mrigshira":       {"expensive": ["Grains", "Cotton", "Gold", "Silver"]},
        "ardra":           {"expensive": ["Grains", "Oils", "Gold", "Silver"]},
        "punarvasu":       {"expensive": ["Grains", "Cotton", "Silver", "Gold"]},
        "pushya":          {"expensive": ["Grains", "Oils", "Ghee", "Gold", "Silver"]},
        "ashlesha":        {"expensive": ["Grains", "Ghee", "Gold", "Silver"]},
        "magha":           {"expensive": ["Grains", "Gold", "Silver", "Ghee", "Cotton"]},
        "poorvaphalguni":  {"expensive": ["Grains", "Gold", "Silver", "Ghee", "Oils"]},
        "uttaraphalguni":  {"expensive": ["Grains", "Gold", "Silver", "Ghee", "Oils"]},
        "hast":            {"expensive": ["Grains", "Gold", "Silver", "Ghee", "Oils", "Cotton"]},
        "chitra":          {"expensive": ["Grains", "Gold", "Silver", "Ghee", "Oils"]},
        "swati":           {"expensive": ["Grains", "Gold", "Silver", "Ghee", "Oils"]},
        "vishakha":        {"expensive": ["Grains", "Juicy materials", "Gur", "Khand", "Pulses"], "cheap": ["Cotton"]},
        "anuradha":        {"cheap": ["Grains", "Gold", "Silver", "Juicy materials"]},
        "jyeshtha":        {"fluctuating": ["Grains"], "cheap": ["Silver"]},
        "mool":            {"cheap": ["Pulses", "Grains", "Gold", "Silver"]},
        "poorvashadh":     {"cheap": ["Grains", "Gold", "Silver", "Cotton", "Gur", "Khand"]},
        "shravan":         {"cheap": ["Grains", "Gur", "Khand", "Gold", "Silver"]},
        "dhanishtha":      {"expensive": ["Gold", "Silver", "Juicy materials"], "cheap": ["Wheat", "Rice", "Barley", "Gram", "Pulses", "Cotton"]},
        "shatbhisha":      {"cheap": ["Grains", "Gold", "Turmeric", "Saffron"], "expensive": ["Silver", "White things"]},
        "poorvabhadrapad": {"expensive": ["Grains", "Gold", "Silver", "Cotton clothes", "Gur"]},
        "uttarabhadrapad": {"expensive": ["Grains", "Gold", "Pulses", "Ghee"]},
        "revati":          {"expensive": ["Gold"], "cheap": ["Grains", "Silver"]},
    },
    "motion_and_luminous_logic": {
        "direct_motion":    "Grains, metals, and pulses are cheap.",
        "retrograde_motion": "Brings down prices of grains; elevates gold and silver.",
        "rising_state":     "Gold cheap; silver expensive.",
        "combusted_state":  "Gold, silver, and grains become cheap.",
    },
    "direct_motion_sign_stay": {
        "aries":       "Ghee, oils, juicy materials cheap",
        "taurus":      "Gold, rice, cotton clothes, yarn cheap",
        "gemini":      "Grains cheap",
        "cancer":      "Water-grown materials cheap",
        "leo":         "Rice, ghee, cotton, silver expensive",
        "virgo":       "Silver cheap",
        "libra":       "Grains, jute products, brass cheap",
        "scorpio":     "Gur, khand cheap",
        "sagittarius": "Oils, oil materials, ghee, grains cheap",
        "capricorn":   "Grains expensive",
        "aquarius":    "All materials expensive",
        "pisces":      "Grains, oils, ghee, gur, khand, jute cheap",
    },
    "diagnostics": {
        "banking_crisis_trigger":  "IF Jupiter afflicted in Capricorn THEN 'Critical: Banking scandals and high-interest rate hikes'.",
        "sovereignty_marker":      "IF Jupiter in Cancer (exaltation) aspected by Sun THEN 'Establishment of Global Supremacy and victory in international treaties'.",
        "tech_boom_trigger":       "IF Jupiter in Sagittarius AND Rahu in Aries THEN 'Significant boom in technology infrastructure and electronics manufacturing'.",
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 4: Venus + Rahu Transit Price Matrix
# ============================================================

GAUR_CH10_VENUS_RAHU_TRANSIT = {
    "spec_id":        "gaur-ch10-venus-rahu-transit-price-matrix",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "transit_price_lookup",
    "title":          "Transit Price Matrix — Venus (12 Signs + Motion) & Rahu (12 Signs)",
    "source_chapter": "Gaur/AIFAS Ch 10",
    "description": (
        "Venus governs luxury goods, silken clothes, entertainment, and population. "
        "Transit through Gemini = 'cataclysmic changes' for India (India's Lagna lord). "
        "Rahu represents foreign influence and electronics; 1.5-year 'Vulnerability Window' per sign."
    ),
    "transit_venus_sign_results": {
        "aries":       {"expensive": ["Grains", "Metals (Gold/Silver)"]},
        "taurus":      {"expensive": ["Grains", "Oils", "Metals"]},
        "gemini":      {"expensive": ["Wheat", "Gram", "Barley", "Grains"], "cheap": ["Oils", "Oil materials", "Jute", "Yarn", "Clothes"]},
        "cancer":      {"expensive": ["Gur", "Khand", "Oils", "Ghee"], "cheap": ["Wheat", "Barley", "Gram", "Peas", "Arhar"]},
        "leo":         {"expensive": ["Grains", "Gold", "Copper", "Red things", "Ghee", "Juices"]},
        "virgo":       {"expensive": ["Grains", "Gur", "Khand", "Wood", "Silken clothes"]},
        "libra":       {"expensive": ["Juicy materials", "Gur", "Khand"], "benefic_veto": "Grains cheap if benefics aspect; expensive if malefics aspect."},
        "scorpio":     {"expensive": ["Gur (fluctuating)"], "cheap": ["Wheat", "Barley", "Pulses (if benefic aspect)"]},
        "sagittarius": {"expensive": ["Grains", "Gold", "Silver", "Clothes", "Shares"]},
        "capricorn":   {"expensive": ["Grains", "Gur", "Khand", "Ghee", "Cotton (after fluctuations)", "Silver (after fluctuations)"]},
        "aquarius":    {"cheap": ["Grains", "Pulses", "White things", "Gur", "Khand", "Silver"]},
        "pisces":      {"cheap": ["Grains", "Oils", "Oil materials", "Gur", "Khand"], "malefic_veto": "If malefic aspect, Silver is expensive."},
    },
    "transit_venus_motion_logic": {
        "change_to_direct":    "Grains, gur, ghee, gold, silver, and gems expensive; cotton cheap.",
        "change_to_retrograde": "Wheat, gur, khand, ghee, and oils expensive.",
        "combusted_state":     "Gold and silver expensive; grains expensive initially then cheap.",
        "rising_state":        "Gold, silver, yarn, clothes, and rice expensive; ghee and khand cheap.",
    },
    "transit_venus_direct_ingress": {
        "aries":       "Til, oils, juicy materials cheap",
        "taurus":      "Juicy materials, ghee, and rice expensive",
        "gemini":      "Cotton, cotton clothes cheap",
        "cancer":      "Cattle cheap",
        "leo":         "Food materials and grains expensive",
        "virgo":       "Silver, juicy materials, and rice cheap",
        "libra":       "Ghee, rice, and yarn expensive",
        "scorpio":     "Grains expensive",
        "sagittarius": "Cotton and yarn cheap",
        "capricorn":   "Juicy materials, gur, and khand cheap",
        "aquarius":    "Yarn, silver, and clothes expensive",
        "pisces":      "All grains and things cheap",
    },
    "venus_india_specific": (
        "IF Venus (afflicted) transits Gemini (India's Lagna = Capricorn but Mercury/Gemini is Lagna lord) "
        "THEN 'National Instability Alert' affecting the central government. "
        "Gemini Venus transit = cataclysmic changes for Indian affairs."
    ),
    "transit_rahu_sign_results": {
        "aries":       "Unstable/Expensive for all commodities.",
        "taurus":      "Juicy materials, gur, khand, oils, and grocery goods expensive.",
        "gemini":      "Grains and ghee expensive for first 9 months, cheap later; Gold and silver cheap initially, costly later.",
        "cancer":      "Grains expensive; metals (gold/silver/iron) cheap.",
        "leo":         "Grains cheap; spices and grocery materials expensive.",
        "virgo":       "Oils and oil materials cheap; cotton expensive.",
        "libra":       "Grains expensive; drought risk due to lack of rains.",
        "scorpio":     "Grains and oils cheap; cotton and woolen clothes expensive.",
        "sagittarius": "Wheat, gram, and ghee cheap; gold and silver expensive.",
        "capricorn":   "Metals (gold/silver/copper) cheap; grains and grocery expensive.",
        "aquarius":    "Oils and grains expensive; juicy materials cheap.",
        "pisces":      "Grains, gold, and silver cheap.",
    },
    "rahu_diagnostics": {
        "drought_veto_libra":    "IF Rahu in Libra THEN 'Drought Veto': agricultural failure even if other planets suggest rain.",
        "9_month_rahu_pivot":    "IF Rahu in Gemini THEN: first 9 months = grains expensive; after 9 months = grains cheap.",
        "electronic_surge":      "IF Jupiter in Sagittarius AND Rahu in Aries THEN 'Boom in technology infrastructure and electronics'.",
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 5: Transit Synthesis Engine (Step 4 Methodology)
# ============================================================

GAUR_CH10_SYNTHESIS_ENGINE = {
    "spec_id":        "gaur-ch10-transit-synthesis-engine",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "operational_framework",
    "title":          "Transit Synthesis Engine — Weighted Majority-Vote Methodology (Gaur Ch 10 Step 4)",
    "source_chapter": "Gaur/AIFAS Ch 10",
    "description": (
        "The 'Brain' of the Mundane Transit Engine — instructing how to synthesize hundreds of individual "
        "planetary lookup results into a single weighted monthly forecast. "
        "Uses 'Majority-Weighting' protocol (validated via August 2002 case study)."
    ),
    "weighting_protocol": {
        "primary_weights":      ["Sun", "Mars", "Jupiter", "Saturn", "Rahu"],
        "secondary_modifiers":  ["Mercury", "Venus", "Moon"],
        "verdict_logic":        "IF Primary_Majority == 'Expensive' THEN Final_Verdict = 'High Prices' ELSE 'Market Correction'.",
    },
    "diagnostic_steps": {
        "step_1_vector_aggregation": "Scan all 9 transiting planets for their Sign, Constellation, and Pad/Navamsh results.",
        "step_2_weighting":          "Apply Primary/Secondary weighting; primary planets override secondary modifiers.",
        "step_3_temporal_refinement": "Apply 14-15 day delay for Sun results; 5-day delay for Mars-Rise results.",
    },
    "synthesis_case_study": {
        "historical_anchor": "August 2002 Grain Forecast",
        "planetary_input_vectors": {
            "sun":     {"stars": ["Pushya", "Ashlesha", "Magha"], "result": "Expensive"},
            "mars":    {"stars": ["Ashlesha", "Magha"], "result": "Expensive"},
            "jupiter": {"star": "Pushya", "result": "Expensive"},
            "mercury": {"stars": ["Ashlesha", "Magha"], "result": "Expensive", "modifier": "P.Phalguni entry = Low prices later"},
            "venus":   {"stars": ["U.Phalguni", "Hast"], "result": "Fluctuation to Cheap"},
            "saturn":  {"star_pads": ["Mrigshira_3rd_Pad", "Mrigshira_4th_Pad"], "result": "Low to High shift"},
        },
        "final_synthesized_diagnostic": "Sun, Mars, and Jupiter all indicate 'Expensive' → month will see high grain prices despite Venusian fluctuations.",
    },
    "automated_conflict_vetoes": {
        "drought_override": "IF Mars is ahead of Sun in Gemini/Cancer THEN Verdict = 'Monsoon Failure' REGARDLESS of other benefic transits.",
        "famine_gate":      "IF Saturn Retrograde in Uttarashadha enters Poorvashadh THEN Verdict = 'Critical 12-Year Famine Alert'.",
        "regional_scaling": "Synthesis must be performed per province. If Saturn in Vayu Nadi in Koorma Punjab sector, prioritize 'Drought' for Punjab specifically.",
        "retrograde_inversion": "If a planet changes motion during the synthesis month, invert its commodity result for the duration of the retrograde stay.",
    },
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
# SPEC 6: Mehta Ch 7 — Koorma Chakra Reconciliation
# ============================================================

MEHTA_CH7_KOORMA_RECONCILED = {
    "spec_id":        "mehta-ch7-koorma-chakra-reconciled",
    "batch_id":       _BATCH,
    "science_id":     "mundane_jyotish",
    "spec_type":      "spatial_diagnostic_grid",
    "title":          "Koorma Chakra Reconciled — Mehta Ch 7 + Gaur Ch 4 Synthesis (Tribal Granularity + Destruction of Kings Kill-Switch)",
    "source_chapter": "Mehta/Rao Ch 7; reconciled against Gaur Ch 4",
    "description": (
        "Upgrades the Spatial Diagnostic Grid with two critical layers absent from Gaur Ch 4: "
        "(1) Tribal precision — specific ethnic groups and ancient clans per direction for civil/border unrest auditing; "
        "(2) Destruction of Kings kill-switch — binary veto triggering Regime Collapse Alert when malefics afflict specific star clusters."
    ),
    "conceptual_foundation": {
        "symbolic_basis":   "Bhu Mandal (Earth) as a tortoise holding the world, fixed on Shesha Naag's forehead.",
        "source_authority": "Narapati Jay Charya and Varahamihira's Brihat Samhita.",
        "operational_rule": "Superimpose 27 Nakshatras onto 9 directional blocks (3 stars per unit).",
    },
    "directional_entity_mapping": {
        "central_region": {
            "nakshatras":     ["Krittika", "Rohini", "Mrigsira"],
            "modern_geography": ["Rajasthan", "Haryana", "Western UP", "Delhi", "Western Maharashtra", "Pathankot", "Gurdaspur", "Alwar", "Kaithal", "Mathura", "Kanpur"],
            "ancient_entities": ["Vatsa", "Ghosa", "Matsaya (Virata)", "Madhyamika (Chitor)", "Surasena (Mathura)", "Panchala", "Udumbara", "Kapisthala", "Hastinapur", "Pandu", "Kuru", "Saketa (Ayodhya)"],
            "destruction_of_kings_risk": "Panchala (Punjab/Haryana)",
        },
        "eastern_india": {
            "nakshatras":     ["Ardra", "Punarvasu", "Pushya"],
            "modern_geography": ["Bihar", "Jharkhand", "Bangladesh", "Assam", "Nagaland", "Manipur", "Mizoram", "Tripura", "Patna", "North Bengal", "Murshidabad"],
            "ancient_entities": ["Magadha (Patna/Gaya)", "Mithila", "Samatata (Nagaon/Kamrupa)", "Pragjyotish (Gauhati)", "Paundra (North Bengal)", "Gaudaka (Murshidabad)", "Utkala (Orissa)"],
            "destruction_of_kings_risk": "Magadha (Bihar)",
        },
        "south_east": {
            "nakshatras":     ["Ashlesha", "Magha", "P.Phalguni"],
            "modern_geography": ["Southern West Bengal", "Orissa", "Andhra Pradesh", "Pondicherry", "Jabalpur", "Puri", "Ganjam"],
            "ancient_entities": ["Kalinga (Puri/Ganjam)", "Vanga (Ganga/Brahmaputra Delta)", "Vidarbha (Berar)", "Cedi (Baghelkhand)", "Kiskinda (Hampi/Vijayanagar)", "Nisadas (Bhils)"],
            "destruction_of_kings_risk": "Kalinga (Orissa/Bengal)",
        },
        "south_direction": {
            "nakshatras":     ["U.Phalguni", "Hasta", "Chitra"],
            "modern_geography": ["Tamil Nadu", "Kerala", "Karnataka", "Sri Lanka", "Konkan", "Nasik"],
            "ancient_entities": ["Simhala (Ceylon)", "Dardura (Nilgiris/Palini Hills)", "Malaya Mountains (Western Ghats)", "Cholas", "Dandakaryan", "Kanchi"],
            "destruction_of_kings_risk": "Avanti (Ujjain/Malwa)",
        },
        "south_west": {
            "nakshatras":     ["Swati", "Vishakha", "Anuradha"],
            "modern_geography": ["Kamboja (South Kashmir to Kafiristan)", "Sindh Sagar Doab", "Western Rajputana", "Kathiawad Peninsula"],
            "tribes":         ["Pahlavas (Parthians)", "Sindhu Sauvira (Jhelum/Indus)", "Sudras (Abhiras)", "Saurashtra", "Dravida (Brahui tribes of Baluchistan)"],
            "destruction_of_kings_risk": "Anarta (Gujarat/Saurashtra)",
        },
        "west_direction": {
            "nakshatras":     ["Jyeshtha", "Moola", "P.Ashadha"],
            "modern_geography": ["Western Maharashtra", "Travancore", "Baluchistan", "West Punjab (Pakistan)"],
            "tribes":         ["Sakas (Scythians)", "Haihayas (Yadav tribe)", "Mlecchas (Foreigners/Arabs/Greeks)", "Vokkana (Wakhan)", "Ramatha (Ghazni)"],
            "destruction_of_kings_risk": "Sindhu-Sauvira (Pakistan/Sindh)",
        },
        "north_west": {
            "nakshatras":     ["U.Ashadha", "Sravana", "Dhanishtha"],
            "modern_geography": ["North Pakistan", "Afghanistan", "Northern Kashmir", "Jodhpur"],
            "territories":    ["Madra (Ravi to Jhelum)", "Asmaka (Swat/Buner)", "Kulutta (Kulu)", "Upper Oxus Valley (Balkh/Badakshan)"],
            "destruction_of_kings_risk": "Harahaura (Indus/Jhelum regions)",
        },
        "north_direction": {
            "nakshatras":     ["Shatabhisha", "P.Bhadrapad", "U.Bhadrapad"],
            "modern_geography": ["Central Asia", "Kashmir", "Punjab", "Haryana", "Uttaranchal", "Northern UP"],
            "territories":    ["Kailasha", "Uttara Kuru (Kashmir)", "Trigarta (Jullundur)", "Gandhara (Kabul/Taxila/Peshawar)", "Yaudheyas (Eastern Punjab)"],
            "destruction_of_kings_risk": "Madra (Sialkot/West Punjab)",
        },
        "north_east": {
            "nakshatras":     ["Revati", "Ashwini", "Bharani"],
            "modern_geography": ["Nepal", "Sikkim", "Bhutan", "Arunachal Pradesh", "Tibet", "China", "Burma"],
            "entities":       ["Abhisaras (Jhelum/Chenab)", "Darada (Gilgit)", "Cinarattha (Chinese beyond Himalayas)", "Suvarnabhu (Irawadi Delta/Malaysia)"],
            "destruction_of_kings_risk": "Kuninda (Himalayan foothills)",
        },
    },
    "planetary_directional_vectors": {
        "sun":      "East",
        "moon":     "North-West",
        "mars":     "South",
        "mercury":  "North",
        "jupiter":  "North-East",
        "venus":    "South-East",
        "saturn":   "West",
        "rahu_ketu": "South / West",
    },
    "planetary_territorial_rulership": {
        "sun":     ["Eastern Narmada", "Orissa", "Bengal", "Bihar", "Kambhoja", "Eastern Tamil Nadu"],
        "moon":    ["Kosala", "Broach"],
        "mars":    ["Narmada", "Sindhu", "Mahanandi River", "Dravida", "Konkan", "Vindhya"],
        "mercury": ["Ganga", "Saryu", "Himalayan States", "Surashtra"],
        "jupiter": ["Eastern Punjab", "Western UP", "Satabru"],
        "venus":   ["Taxila", "Gandhara", "Malva", "Vitasta", "Iravati"],
        "saturn":  ["Saurashtra", "Vidisa", "Rajasthan"],
        "rahu":    ["Suleka", "Kinnars"],
        "ketu":    ["Iran", "Hunas", "Afghanistan", "China", "Cholas"],
    },
    "regime_collapse_kill_switch": {
        "logic":        "IF malefics afflict Star Cluster THEN Prediction = Destruction of King/Ruler in Country_Affected.",
        "kill_switch_table": [
            {"stars": ["Krittika", "Rohini", "Mrigsira"],    "regime_at_risk": "Panchala (Punjab/Haryana)"},
            {"stars": ["Ardra", "Punarvasu", "Pushya"],      "regime_at_risk": "Magadha (Bihar)"},
            {"stars": ["Ashlesha", "Magha", "P.Phalguni"],   "regime_at_risk": "Kalinga (Orissa/Bengal)"},
            {"stars": ["U.Phalguni", "Hasta", "Chitra"],     "regime_at_risk": "Avanti (Ujjain/Malwa)"},
            {"stars": ["Swati", "Vishakha", "Anuradha"],     "regime_at_risk": "Anarta (Gujarat/Saurashtra)"},
            {"stars": ["Jyeshtha", "Moola", "P.Ashadha"],   "regime_at_risk": "Sindhu-Sauvira (Pakistan/Sindh)"},
            {"stars": ["U.Ashadha", "Sravana", "Dhanishtha"], "regime_at_risk": "Harahaura (Indus/Jhelum regions)"},
            {"stars": ["Shatbhisha", "P.Bhadra", "U.Bhadra"], "regime_at_risk": "Madra (Sialkot/West Punjab)"},
            {"stars": ["Revati", "Ashwini", "Bharani"],      "regime_at_risk": "Kuninda (Himalayan foothills)"},
        ],
    },
    "triple_directional_audit": (
        "When a mundane event is predicted (e.g., war), cross-reference: "
        "(1) Koorma Direction (afflicted star's sector); "
        "(2) Planet's Direction (e.g., Saturn = West); "
        "(3) 7th House Direction (e.g., Mars in Aries = East). "
        "If all three point to the same direction: prediction confidence = CRITICAL."
    ),
    "triple_alignment_amplifier": (
        "IF Saturn transiting a Western sign AND placed in the Western Koorma sector: "
        "malefic impact on heavy industry and labor is TRIPLED."
    ),
    "approval_status": "pending_review",
    "created_at":      _NOW,
}

# ============================================================
ALL_SPECS = [
    GAUR_CH10_MARS_TRANSIT,
    GAUR_CH10_MERCURY_TRANSIT,
    GAUR_CH10_JUPITER_TRANSIT,
    GAUR_CH10_VENUS_RAHU_TRANSIT,
    GAUR_CH10_SYNTHESIS_ENGINE,
    MEHTA_CH7_KOORMA_RECONCILED,
]

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_SPECS)} engine specs from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        for s in ALL_SPECS:
            print(f"  {s['spec_id']}")
        print(f"\nTotal: {len(ALL_SPECS)}\nDry run complete.")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    col = db[COLLECTION]
    upserted = 0
    for spec in ALL_SPECS:
        await col.update_one(
            {"spec_id": spec["spec_id"]},
            {"$set": spec},
            upsert=True,
        )
        upserted += 1
    print(f"Upserted {upserted} specs into {COLLECTION}.")
    client.close()

if __name__ == "__main__":
    asyncio.run(run())
