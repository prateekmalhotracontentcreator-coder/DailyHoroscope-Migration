"""
Mundane Astrology — Interpretation Rules INGEST v16
====================================================
Batch : mundane-interp-v16-20260506
Collection : interpretation_rules
Science    : mundane_jyotish

Rule groups:
  GROUP_AK — Gaur Ch 5: Monsoon & Ardra Entry rules          (8 rules)
  GROUP_AL — Gaur Ch 6: Weather / Atmospheric rules           (8 rules)
  GROUP_AM — Gaur Ch 7: Crop Yield & Inverse Pricing rules    (6 rules)
  GROUP_AN — Gaur Ch 8/9: Commodity & Sarvatobhadra Trade     (7 rules)

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

# ── config ────────────────────────────────────────────────────────────────────
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.environ.get("DB_NAME",  "horoscope_db")
DRY_RUN   = True

_BATCH = "mundane-interp-v16-20260506"
_NOW   = datetime.now(timezone.utc).isoformat()

def _rule(rule_id, sub_type, title, source_chapter, condition, result,
          synthesis_sources, notes="", severity=None, checkable=False):
    d = {
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
        "created_at":       _NOW,
    }
    if notes:    d["notes"]    = notes
    if severity: d["severity"] = severity
    return d

# ═════════════════════════════════════════════════════════════════════════════
# GROUP AK — Gaur Ch 5: Monsoon & Ardra Entry Rules
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AK = [

    _rule(
        rule_id          = "mundane-gaur-ch5-ardra-bumper-harvest",
        sub_type         = "monsoon_forecast",
        title            = "Ardra Entry Bumper Harvest — Triyodashi + Pushya + Sea Residence",
        source_chapter   = "Gaur Ch 5 — Ardra Entry & Rohini Chart",
        condition        = (
            "Ardra Entry Tithi = Triyodashi AND Moon in Pushya at Entry AND "
            "Rohini Samudra Chakra Residence = Sea"
        ),
        result           = (
            "OPTIMAL MONSOON: Record grain production confirmed. Gardener's House residence "
            "signals a lush, prosperous year. Grain prices to drop significantly. "
            "National food security high."
        ),
        synthesis_sources = ["gaur-ch5-ardra-monsoon-engine", "gaur-ch5-rohini-samudra-chakra"],
        notes            = (
            "Triple convergence of best Tithi + best Moon nakshatra + Sea residence. "
            "All three must be present for maximum confidence."
        ),
        severity         = "high",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch5-ardra-drought-riot",
        sub_type         = "monsoon_forecast",
        title            = "Ardra Entry Drought & Civil Unrest — Triteeya + Vyaghat Yoga",
        source_chapter   = "Gaur Ch 5 — Ardra Entry & Rohini Chart",
        condition        = (
            "Ardra Entry Tithi = Triteeya AND Nitya Yoga at Entry = Vyaghat"
        ),
        result           = (
            "CRITICAL WARNING: Severe drought followed by civil unrest and high commodity prices. "
            "Grain production will fail; riots and public disorder expected during the rainy season."
        ),
        synthesis_sources = ["gaur-ch5-ardra-monsoon-engine"],
        severity         = "critical",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch5-rohini-mountain-drought",
        sub_type         = "monsoon_forecast",
        title            = "Rohini Mountain Residence — Guaranteed Drought Signal",
        source_chapter   = "Gaur Ch 5 — Rohini Chart (Samudra Chakra)",
        condition        = (
            "Rohini Samudra Chakra Residence = Mountain (Parvat)"
        ),
        result           = (
            "DROUGHT CONFIRMED: Scanty rains; acute crop suffering. Potter's House residence "
            "indicates fragile agricultural economy for the year. Hydrological Stress flag active "
            "regardless of Ardra Entry weekday result."
        ),
        synthesis_sources = ["gaur-ch5-rohini-samudra-chakra"],
        notes            = (
            "Mountain residence overrides positive weekday/tithi signals — "
            "it is the strongest standalone drought indicator in this system."
        ),
        severity         = "critical",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch5-ardra-saturday-disease",
        sub_type         = "public_health_forecast",
        title            = "Ardra Entry Saturday + Midnight — Epidemic & Civil Unrest",
        source_chapter   = "Gaur Ch 5 — Ardra Entry",
        condition        = (
            "Ardra Entry Weekday = Saturday AND Time of Entry = Midnight"
        ),
        result           = (
            "PUBLIC HEALTH WARNING: High risk of widespread epidemics and civil unrest "
            "throughout the rainy season. Disease incidence at peak; social stability threatened."
        ),
        synthesis_sources = ["gaur-ch5-ardra-monsoon-engine"],
        severity         = "high",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch5-ardra-krithika-fire",
        sub_type         = "weather_forecast",
        title            = "Moon in Krithika at Ardra Entry — Fire Risk & Rain Deficiency",
        source_chapter   = "Gaur Ch 5 — Ardra Entry Moon Nakshatra",
        condition        = (
            "Moon in Krithika at moment of Ardra Entry"
        ),
        result           = (
            "EMERGENCY ALERT: High risk of accidental fires and heatwaves. "
            "Moisture deficiency confirmed. Rain will be deficient for the season; "
            "fire hazard to crops and rural infrastructure elevated."
        ),
        synthesis_sources = ["gaur-ch5-ardra-monsoon-engine"],
        severity         = "high",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch5-ardra-afternoon-entry",
        sub_type         = "monsoon_forecast",
        title            = "Ardra Entry in Afternoon — Grain Scarcity Override",
        source_chapter   = "Gaur Ch 5 — Ardra Entry Time Logic",
        condition        = (
            "Time of Ardra Entry = Afternoon (between 12:00 and sunset)"
        ),
        result           = (
            "MARKET SCARCITY ALERT: Afternoon entry overrides all positive Tithi/Yoga signals. "
            "Poor crops expected; grain prices will rise. "
            "Agriculture sector under stress for the season."
        ),
        synthesis_sources = ["gaur-ch5-ardra-monsoon-engine"],
        notes            = "Afternoon entry is a hard veto — positive yogas cannot neutralize it.",
        severity         = "medium",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch5-ardra-wednesday-prosperity",
        sub_type         = "monsoon_forecast",
        title            = "Ardra Entry Wednesday or Thursday — National Prosperity Signal",
        source_chapter   = "Gaur Ch 5 — Ardra Entry Weekday",
        condition        = (
            "Ardra Entry Weekday = Wednesday OR Thursday "
            "AND Nitya Yoga IN (Shubh, Sukarma, Vriddhi, Preeti)"
        ),
        result           = (
            "OPTIMAL MONSOON: Excellent crops and cheap prices (Wednesday) / "
            "Prosperous season (Thursday). When combined with auspicious Yoga, "
            "national food security is high and low inflation predicted for the year."
        ),
        synthesis_sources = ["gaur-ch5-ardra-monsoon-engine"],
        severity         = "medium",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch5-rohini-sea-flash-flood",
        sub_type         = "weather_forecast",
        title            = "Rohini Sea Residence + Watery 12th House — Flash Flood Risk",
        source_chapter   = "Gaur Ch 5 — Ardra Entry Horoscope + Rohini Chart",
        condition        = (
            "Rohini Samudra Chakra Residence = Sea AND "
            "Ardra Entry Horoscope Sun in 12th House AND Moon in Watery Sign"
        ),
        result           = (
            "REGIONAL RISK ALERT: Overall rains are sufficient (Sea residence confirms), "
            "but high probability of localized flood-related crop loss. "
            "Flood_Risk_Weight +0.4 applied. Infrastructure in low-lying areas at risk."
        ),
        synthesis_sources = ["gaur-ch5-rohini-samudra-chakra", "gaur-ch5-ardra-monsoon-engine"],
        severity         = "high",
        checkable        = True,
    ),

]

# ═════════════════════════════════════════════════════════════════════════════
# GROUP AL — Gaur Ch 6: Weather & Atmospheric Rules
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AL = [

    _rule(
        rule_id          = "mundane-gaur-ch6-trinadi-no-rain-veto",
        sub_type         = "weather_forecast",
        title            = "Trinadi Rule 8 — Malefics in Patal + Benefics in Heaven = No Rain",
        source_chapter   = "Gaur Ch 6 — Snake Trinadi Chart",
        condition        = (
            "Malefic planets (Sun, Mars, Saturn, Rahu, Ketu) concentrated in Patal Nadi "
            "AND Benefic planets (Moon, Mercury, Jupiter, Venus) concentrated in Heaven Nadi"
        ),
        result           = (
            "CRITICAL RAINFALL FAILURE: Strict veto — no rains whatsoever. "
            "Atmospheric Inversion confirmed. Moisture delivery completely blocked. "
            "Drought monitoring protocol activated."
        ),
        synthesis_sources = ["gaur-ch6-snake-trinadi-weather-engine"],
        severity         = "critical",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch6-trinadi-catastrophic-flood",
        sub_type         = "weather_forecast",
        title            = "All Male Planets in One Nadi — Destructive Rain Alert",
        source_chapter   = "Gaur Ch 6 — Snake Trinadi Chart",
        condition        = (
            "All male planets (Sun, Mars, Saturn, Rahu, Ketu) occupy one Trinadi Nadi"
        ),
        result           = (
            "EMERGENCY ALERT: High probability of excessive and destructive rains. "
            "Flash flood risk elevated. Agricultural and infrastructure damage expected."
        ),
        synthesis_sources = ["gaur-ch6-snake-trinadi-weather-engine"],
        severity         = "critical",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch6-trinadi-hail-storm",
        sub_type         = "weather_forecast",
        title            = "Female + Eunuch Planets Bundled — Hail Storm Hazard",
        source_chapter   = "Gaur Ch 6 — Snake Trinadi Chart",
        condition        = (
            "Female planets (Moon, Venus) AND Eunuch planet (Mercury) "
            "all concentrated in one Trinadi Nadi"
        ),
        result           = (
            "AVIATION & AGRICULTURE WARNING: High probability of damaging hail storms. "
            "Severe hazard to standing crops and exposed infrastructure."
        ),
        synthesis_sources = ["gaur-ch6-snake-trinadi-weather-engine"],
        severity         = "high",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch6-saptnadi-amrita-rain",
        sub_type         = "weather_forecast",
        title            = "Saptnadi Amrita Nadi Vedha — Continuous 1–7 Day Rain",
        source_chapter   = "Gaur Ch 6 — Saptnadi Chart",
        condition        = (
            "Gentle (benefic) AND Cruel (malefic) planets both present in Amrita Nadi "
            "(Ashlesha, Magha, Shravan, Dhanishtha) AND Moon also present"
        ),
        result           = (
            "METEOROLOGICAL ALERT: Continuous rainfall predicted for 1 to 7 days "
            "(may recur multiple times). Moon is lord of Amrita Nadi — "
            "its presence is the primary rain trigger. High confidence forecast."
        ),
        synthesis_sources = ["gaur-ch6-saptnadi-precipitation-engine"],
        severity         = "medium",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch6-saptnadi-jala-36hrs",
        sub_type         = "weather_forecast",
        title            = "Saptnadi Jala Nadi Vedha — 36–72 Hour Sustained Rain",
        source_chapter   = "Gaur Ch 6 — Saptnadi Chart",
        condition        = (
            "Gentle AND Cruel planets bundled in Jala Nadi "
            "(Pushya, Poorvaphalguni, Abhijit, Shatbhisha)"
        ),
        result           = (
            "METEOROLOGICAL ALERT: Continuous precipitation predicted for next "
            "36 to 72 hours. Excessive rain; flood monitoring recommended for low-lying areas."
        ),
        synthesis_sources = ["gaur-ch6-saptnadi-precipitation-engine"],
        severity         = "medium",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch6-ownership-rain-confirm",
        sub_type         = "weather_forecast",
        title            = "Sun/Moon Cross-Ownership — Rain Certainty Confirmation",
        source_chapter   = "Gaur Ch 6 — Constellation Ownership",
        condition        = (
            "Sun occupies a Moon-owned star AND Moon occupies a Sun-owned star simultaneously "
            "(cross-ownership swap)"
        ),
        result           = (
            "RAIN CERTAINTY: Both planetary ownership indicators confirm precipitation. "
            "Combined with Female-Male gender interaction = Optimal Rainfall Forecast. "
            "High confidence for rainfall within 24–48 hours."
        ),
        synthesis_sources = ["gaur-ch6-constellation-gender-weather-engine"],
        severity         = "medium",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch6-mars-venus-jupiter-catastrophic",
        sub_type         = "weather_forecast",
        title            = "Mars 7th from Venus + Jupiter 7th from Saturn — Annihilating Floods",
        source_chapter   = "Gaur Ch 6 — Planetary Rain Combinations",
        condition        = (
            "Mars in 7th house from Venus AND Jupiter in 7th house from Saturn"
        ),
        result           = (
            "CATASTROPHIC WEATHER ALERT: Annihilating floods imminent. "
            "Highest severity weather event in the Gaur rain combination system. "
            "National disaster-level flooding expected."
        ),
        synthesis_sources = ["gaur-ch6-saptnadi-precipitation-engine"],
        severity         = "critical",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch6-saptnadi-dahan-fire",
        sub_type         = "weather_forecast",
        title            = "Saptnadi Dahan Nadi Vedha — Fire on Earth Alert",
        source_chapter   = "Gaur Ch 6 — Saptnadi Chart",
        condition        = (
            "Two or more planets concentrated in Dahan Nadi "
            "(Mrigshira, Chitra, Moola, Revti) — Vedha triggered"
        ),
        result           = (
            "FIRE HAZARD: High risk of fires on earth — forest fires, industrial fires, "
            "or military conflagration. Dahan (combustion) Nadi lord is Mars. "
            "Drought conditions likely to co-occur."
        ),
        synthesis_sources = ["gaur-ch6-saptnadi-precipitation-engine"],
        severity         = "high",
        checkable        = True,
    ),

]

# ═════════════════════════════════════════════════════════════════════════════
# GROUP AM — Gaur Ch 7: Crop Yield & Inverse Pricing Rules
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AM = [

    _rule(
        rule_id          = "mundane-gaur-ch7-bumper-harvest-yoga-i",
        sub_type         = "agricultural_forecast",
        title            = "Crop Yoga I — Benefics in Quadrants = Bumper Harvest + Cheap Grains",
        source_chapter   = "Gaur Ch 7 — Sasya Jatak Crop Yogas",
        condition        = (
            "Benefic planets (Jupiter, Venus, Mercury, Moon) occupy quadrant houses "
            "(1st, 4th, 7th, 10th) from the transiting Sun OR Sun is aspected by strong benefics "
            "in the seasonal ingress chart"
        ),
        result           = (
            "BUMPER HARVEST: Produce = High. Inverse Pricing Rule triggers Bearish trend "
            "for grain commodities. Grain prices to drop significantly. "
            "Trade module must flag 'Bearish/Low Price' for all grain categories."
        ),
        synthesis_sources = ["gaur-ch7-sasya-jatak-crop-engine"],
        severity         = "medium",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch7-sprouting-failure-yoga-viii",
        sub_type         = "agricultural_forecast",
        title            = "Crop Yoga VIII — Malefic in 2nd from Sun = Sprouting Failure",
        source_chapter   = "Gaur Ch 7 — Sasya Jatak Crop Yogas",
        condition        = (
            "Malefic planet in 2nd house from the Sun in seasonal ingress chart "
            "AND Sun lacks any benefic aspect"
        ),
        result           = (
            "AGRICULTURAL CRISIS: Crop destroyed soon after sprouting. "
            "Reseeding required — farmers must prepare for high-cost second sowing. "
            "Initial market supply will be severely disrupted; grain prices spike early in season."
        ),
        synthesis_sources = ["gaur-ch7-sasya-jatak-crop-engine"],
        severity         = "critical",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch7-total-crop-failure-yoga-ix",
        sub_type         = "agricultural_forecast",
        title            = "Crop Yoga IX — Malefics in 7th + 1st/4th/10th = Total Crop Failure",
        source_chapter   = "Gaur Ch 7 — Sasya Jatak Crop Yogas",
        condition        = (
            "Saturn OR Mars in 7th house from Sun AND another malefic in 1st, 4th, or 10th house "
            "from Sun in seasonal ingress chart AND no benefic aspects on these malefics"
        ),
        result           = (
            "TOTAL CROP FAILURE: Complete agricultural collapse predicted. "
            "Grain prices will spike to extreme highs. "
            "If benefics aspect the malefics → Partial/Localized destruction only. "
            "National food security critical."
        ),
        synthesis_sources = ["gaur-ch7-sasya-jatak-crop-engine"],
        severity         = "critical",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch7-malefic-interference-yoga-vii",
        sub_type         = "agricultural_forecast",
        title            = "Crop Yoga VII — Sun Between Mars & Saturn = Crop Destroyed",
        source_chapter   = "Gaur Ch 7 — Sasya Jatak Crop Yogas",
        condition        = (
            "Sun positioned between Mars AND Saturn (Mars one side, Saturn the other) "
            "OR Mars AND Saturn together in 7th house from Sun"
        ),
        result           = (
            "CROP DESTRUCTION: Produce = Destroyed/Poor. Grains = Expensive. "
            "Inverse Pricing Rule triggers Bullish trend for grain commodities. "
            "Extended period of elevated grain prices expected."
        ),
        synthesis_sources = ["gaur-ch7-sasya-jatak-crop-engine"],
        severity         = "high",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch7-conspiracy-yoga-vi",
        sub_type         = "agricultural_forecast",
        title            = "Crop Yoga VI — Jupiter Aquarius + Moon Taurus + Mars/Saturn Capricorn",
        source_chapter   = "Gaur Ch 7 — Sasya Jatak Crop Yogas",
        condition        = (
            "Jupiter in Aquarius AND Moon in Taurus AND "
            "Saturn AND Mars both in Capricorn simultaneously"
        ),
        result           = (
            "COMPLEX HARVEST: Produce = Good (high yields) BUT Status = "
            "'National Conspiracy and Disease Alert'. High yields will be overshadowed by "
            "national health crises and political plots. Markets disrupted despite good supply."
        ),
        synthesis_sources = ["gaur-ch7-sasya-jatak-crop-engine"],
        severity         = "high",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch7-food-security-gate",
        sub_type         = "agricultural_forecast",
        title            = "Food Security Gate — Strong Lagna + Jupiter Aspects 4th House",
        source_chapter   = "Gaur Ch 7 — Sasya Jatak Diagnostics",
        condition        = (
            "Crop Horoscope Lagna = Strong (no malefic influence) "
            "AND Jupiter aspects the 4th House of the seasonal ingress chart"
        ),
        result           = (
            "BUMPER HARVEST: National food security high. Grain prices to drop significantly. "
            "Inverse Pricing: Trade module flags all grain/pulse categories as Bearish. "
            "Dairy (if Jupiter in 10th) also Abundant."
        ),
        synthesis_sources = ["gaur-ch7-sasya-jatak-crop-engine"],
        severity         = "medium",
        checkable        = True,
    ),

]

# ═════════════════════════════════════════════════════════════════════════════
# GROUP AN — Gaur Ch 8/9: Commodity Database & Sarvatobhadra Trade Rules
# ═════════════════════════════════════════════════════════════════════════════

GROUP_AN = [

    _rule(
        rule_id          = "mundane-gaur-ch8-gold-silver-bullion-gate",
        sub_type         = "commodity_price_forecast",
        title            = "Bullion Gate — Jupiter transits Pushya + Sun in Aries",
        source_chapter   = "Gaur Ch 8 — Material Database / Ch 9 — Sarvatobhadra",
        condition        = (
            "Jupiter transiting Pushya nakshatra AND Sun in Aries sign simultaneously"
        ),
        result           = (
            "BULLISH PRECIOUS METALS: Massive price surge for Gold and Silver expected. "
            "Multi-vector pressure confirmed — Pushya governs Gold/Silver (nakshatra ownership) "
            "and Aries governs them (planetary ownership via Sun). "
            "Gold/Silver at seasonal highs."
        ),
        synthesis_sources = [
            "gaur-ch8-material-commodity-database",
            "gaur-ch9-sarvatobhadra-trade-engine",
        ],
        severity         = "high",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch9-sarvatobhadra-currency-spike",
        sub_type         = "commodity_price_forecast",
        title            = "Sarvatobhadra Dhanishtha Malefic Vedha — Currency & Metal Spike",
        source_chapter   = "Gaur Ch 9 — Sarvatobhadra Trade Engine",
        condition        = (
            "Saturn OR Rahu transiting Dhanishtha nakshatra (malefic) "
            "OR Mars has Right Vedha on Krittika"
        ),
        result           = (
            "CRITICAL METAL ALERT: Rapid price increase for Gold, Silver, All Currencies, "
            "Ruby, and Pearl predicted. Dhanishtha governs all currencies — "
            "malefic Vedha here signals financial market stress."
        ),
        synthesis_sources = ["gaur-ch9-sarvatobhadra-trade-engine"],
        severity         = "high",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch9-sarvatobhadra-textile-shortage",
        sub_type         = "commodity_price_forecast",
        title            = "Sarvatobhadra Punarvasu Malefic Vedha — Cotton & Textile Shortage",
        source_chapter   = "Gaur Ch 9 — Sarvatobhadra Trade Engine",
        condition        = (
            "Mars transiting Punarvasu AND Mars has Front Vedha on Poorvashadh"
        ),
        result           = (
            "INDUSTRY WARNING: High volatility in cotton, jute, and silken goods. "
            "Supply chain disruption for textiles expected. "
            "Punarvasu governs cotton and millet — malefic obstruction raises prices sharply."
        ),
        synthesis_sources = ["gaur-ch9-sarvatobhadra-trade-engine"],
        severity         = "medium",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch8-saturn-retrograde-industrial",
        sub_type         = "commodity_price_forecast",
        title            = "Saturn Retrograde — Steel & Industrial Production Slowdown",
        source_chapter   = "Gaur Ch 8 — Material Database (Saturn-Factory Veto)",
        condition        = (
            "Saturn is Retrograde in any sign"
        ),
        result           = (
            "PRODUCTION SLOWDOWN ALERT: Steel mills and heavy factories face output reduction. "
            "Saturn governs Steel, Iron, Machinery, Chemicals, and Foreign Capital. "
            "Retrograde motion signals supply contraction → steel and iron prices rise."
        ),
        synthesis_sources = ["gaur-ch8-material-commodity-database"],
        severity         = "medium",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch8-saturn-mars-capricorn-chemical",
        sub_type         = "commodity_price_forecast",
        title            = "Saturn + Mars in Capricorn — Industrial Accident & Chemical Price Spike",
        source_chapter   = "Gaur Ch 8 — Material Database Diagnostics",
        condition        = (
            "Saturn aspected by Mars in Capricorn sign"
        ),
        result           = (
            "INDUSTRIAL WARNING: High risk of accidents in steel mills or chemical leaks. "
            "Heavy hardware prices to fluctuate sharply. "
            "Capricorn governs Iron, Coal, Steel, Glass — malefic conjunction here amplifies risk."
        ),
        synthesis_sources = ["gaur-ch8-material-commodity-database"],
        severity         = "high",
        checkable        = True,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch8-dual-mapping-volatility",
        sub_type         = "commodity_price_forecast",
        title            = "Dual-Mapping Conflict — Sign Bullish vs Nakshatra Bearish = Choppy Markets",
        source_chapter   = "Gaur Ch 8 — Material Database (Dual-Mapping Filter)",
        condition        = (
            "A commodity's governing Zodiac Sign indicates Bullish trend "
            "AND its governing Nakshatra indicates Bearish trend simultaneously "
            "(or vice versa) — example: Gold via Aries = Bullish, Gold via Pushya = Bearish"
        ),
        result           = (
            "MARKET VOLATILITY: Choppy trading in the conflicted commodity. "
            "No clean directional trend — price oscillates. "
            "Engine outputs 'Dual-Signal Conflict' flag; position sizing should be reduced."
        ),
        synthesis_sources = ["gaur-ch8-material-commodity-database"],
        severity         = "medium",
        checkable        = False,
    ),

    _rule(
        rule_id          = "mundane-gaur-ch9-sarvatobhadra-market-sentiment",
        sub_type         = "commodity_price_forecast",
        title            = "Sarvatobhadra Majority Vedha — Overall Market Sentiment Signal",
        source_chapter   = "Gaur Ch 9 — Sarvatobhadra Trade Engine",
        condition        = (
            "Count of Benefic Vedha points (Moon, Mercury, Jupiter, Venus active on constellation) "
            "> Count of Malefic Vedha points (Sun, Mars, Saturn, Rahu, Ketu active on constellation)"
        ),
        result           = (
            "BEARISH MARKET SENTIMENT: Prices are likely to soften as goods become easily available. "
            "Accumulation recommended as prices dip. "
            "Reverse (Malefic > Benefic) → Bullish overall market: prices rising across commodities."
        ),
        synthesis_sources = ["gaur-ch9-sarvatobhadra-trade-engine"],
        severity         = "medium",
        checkable        = True,
    ),

]

# ═════════════════════════════════════════════════════════════════════════════
# Master list
# ═════════════════════════════════════════════════════════════════════════════
RULES = GROUP_AK + GROUP_AL + GROUP_AM + GROUP_AN

# ═════════════════════════════════════════════════════════════════════════════
# Runner
# ═════════════════════════════════════════════════════════════════════════════
async def run():
    if DRY_RUN:
        print(f"[DRY RUN] Would upsert {len(RULES)} rules into interpretation_rules.")
        for r in RULES:
            print(f"  would upsert: {r['rule_id']}")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    db     = client[DB_NAME]
    coll   = db["interpretation_rules"]
    ok = 0
    for r in RULES:
        await coll.update_one(
            {"rule_id": r["rule_id"]},
            {"$set": r},
            upsert=True,
        )
        ok += 1
    client.close()
    print(f"Upserted {ok} rules into interpretation_rules.")

if __name__ == "__main__":
    asyncio.run(run())
