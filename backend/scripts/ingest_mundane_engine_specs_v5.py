"""
Mundane Astrology — Engine Specs v5
Batch: mundane-engine-v5-20260506

Source: Gopalakrishnan, "Mundane Astrology" (ICAS)
  Chapter 6 — Predicting Mass Death (book pp.79-90)
  Chapter 7 — Earthquakes (book pp.91-98)

Spec types: lookup_table, rule_matrix
science_id: mundane_jyotish
Collection: mundane_engine_specs

Run with DRY_RUN = True to verify, then set False to write to MongoDB.
"""

import asyncio
from datetime import datetime, timezone
import sys
import types

# ---------------------------------------------------------------------------
# Motor stub for local dry-run
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

# ---------------------------------------------------------------------------
MONGO_URL  = "mongodb://localhost:27017"
DB_NAME    = "horoscope_db"
COLLECTION = "mundane_engine_specs"
_BATCH     = "mundane-engine-v5-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True
# ---------------------------------------------------------------------------

# ============================================================
# 1. MASS DEATH — NATIONAL CHART PARAMETERS  (Gopalakrishnan Ch 6)
# ============================================================
GOPAL_CH6_MASS_DEATH_SPEC = {
    "spec_id":      "gopal-ch6-mass-death-national-chart",
    "spec_type":    "rule_matrix",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Mass Death Indicators from National Chart — Eclipse, 8th House, Epidemic",
    "source_chapter": "Gopalakrishnan Ch 6, pp.79-90",
    "notes": (
        "All indicators assessed against the national horoscope of the relevant country. "
        "Eclipse house positions calculated relative to the country's natal Ascendant or "
        "Aries Ingress chart Ascendant for that year. "
        "Severity escalates with convergence of multiple triggers."
    ),
    # ── Eclipse falling on trika / sensitive houses
    "eclipse_on_house_of_national_chart": {
        "4":  "Eclipse on 4th house (home/masses): mass death, suffering among the general population.",
        "8":  "Eclipse on 8th house (death/longevity): mass death, war casualties, epidemics.",
        "12": "Eclipse on 12th house (loss/exile): mass death, large-scale displacement, hospitals overwhelmed.",
    },
    # ── Eclipse conjunct natal planets of national chart
    "eclipse_on_natal_planet": {
        "Ascendant": "Eclipse on national Ascendant: danger to head of state / national identity crisis.",
        "Sun":       "Eclipse conjunct natal Sun of nation: danger to the leader / king / prime minister.",
        "Moon":      "Eclipse conjunct natal Moon of nation: danger to the leader; mass public grief.",
    },
    # ── 8th house death-zone combinations (transit chart)
    "eighth_house_death_zone": {
        "saturn_rahu_8th":         "Saturn + Rahu/Ketu conjunction in 8th house = mass death signal. Most dangerous when eclipse also afflicts 8th.",
        "mars_in_8th_eclipse":     "Mars transiting 8th house during an eclipse = war-related mass death.",
        "three_malefics_in_8th":   "Three or more malefic planets in 8th house simultaneously = severe death zone. Malefics: Sun, Mars, Saturn, Rahu, Ketu.",
        "8th_lord_triple_affliction": "Lord of 8th house afflicted by three or more malefic planets by conjunction or opposition = mass casualty risk.",
    },
    # ── Mars in gandanta nakshatras (junctional zones between water and fire signs)
    "mars_gandanta_nakshatras": {
        "Ardra":    "Mars in Ardra (Gemini end / Cancer junction): mass accidents, sudden casualties.",
        "Ashlesha": "Mars in Ashlesha (Cancer end / Leo junction): mass accidents, epidemics.",
        "Jyeshtha": "Mars in Jyeshtha (Scorpio end / Sagittarius junction): mass accidents, violent upheaval.",
        "Mool":     "Mars in Mool (Sagittarius start): mass accidents, natural calamities.",
        "note":     "Gandanta = last 3°20' of water sign + first 3°20' of fire sign. Mool covers Sagittarius 0°-3°20'.",
    },
    # ── Epidemic indicators
    "epidemic_indicators": {
        "saturn_6th_from_country_moon": (
            "Saturn transiting the 6th sign from the country's natal Moon sign: "
            "outbreak of disease and epidemic conditions. "
            "E.g., if country Moon = Cancer, Saturn in Sagittarius triggers epidemic."
        ),
        "rahu_in_country_natal_moon_sign": (
            "Rahu transiting through the sign occupied by the country's natal Moon: "
            "epidemic/pandemic conditions, mysterious illnesses, mass public fear."
        ),
        "venus_saturn_conjunction": (
            "Venus and Saturn in the same sign: disease spread through food, water, or sexual transmission. "
            "Especially potent when in 6th or 8th house of national chart."
        ),
    },
    # ── Historical case validations cited by Gopalakrishnan
    "historical_validations": {
        "1918_spanish_flu": (
            "Spanish Flu 1918: Saturn+Jupiter conjunction; Rahu in Gemini (transit through India's Moon sign area); "
            "Venus-Saturn aspects in play. ~50M deaths globally."
        ),
        "bhopal_1984": (
            "Bhopal Gas Tragedy Dec 1984: Solar eclipse in Scorpio (8th sign from Taurus, India's Asc); "
            "Saturn in Scorpio; Mars in Scorpio — triple 8th-house affliction. ~15,000+ deaths."
        ),
        "tsunami_2004": (
            "Indian Ocean Tsunami Dec 26 2004: Solar eclipse Dec 2004 in Sagittarius; "
            "Saturn retrograde in Cancer (opposing Capricorn, 8th from India's Gemini?); "
            "Mars+Rahu conjunction active. ~227,000 deaths across 14 countries."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
# 2. EARTHQUAKE INDICATORS  (Gopalakrishnan Ch 7)
# ============================================================
GOPAL_CH7_EARTHQUAKE_SPEC = {
    "spec_id":      "gopal-ch7-earthquake-indicators",
    "spec_type":    "rule_matrix",
    "science_id":   "mundane_jyotish",
    "batch_id":     _BATCH,
    "title":        "Earthquake Prediction Indicators — Fixed Signs, Eclipse Points, Rahu/Ketu Axis",
    "source_chapter": "Gopalakrishnan Ch 7, pp.91-98",
    "notes": (
        "Seismic prediction requires convergence of at least 2-3 indicators. "
        "Single indicator = watch; two indicators = alert; three+ = high probability window. "
        "Geographic zone is determined by the Ascendant/IC of the regional chart or "
        "Aries Ingress chart for the territory in question."
    ),
    # ── Primary seismic indicators
    "primary_indicators": {
        "saturn_fixed_sign_direct": (
            "Saturn transiting a fixed sign (Taurus, Leo, Scorpio, Aquarius): "
            "elevated baseline seismic risk for regions governed by that sign."
        ),
        "saturn_fixed_sign_retrograde": (
            "Saturn retrograde in a fixed sign: strongest primary seismic indicator. "
            "Retrograde amplifies the earth-disruption energy of Saturn in fixed signs. "
            "Especially dangerous when Saturn is also in Scorpio or Aquarius."
        ),
    },
    # ── Trigger indicators (activate the primary condition)
    "trigger_indicators": {
        "mars_transits_eclipse_point": (
            "Mars transiting over the longitude of a recent solar or lunar eclipse: "
            "seismic trigger window of 3 days either side of the exact conjunction. "
            "Effect is strongest when primary Saturn condition is also active."
        ),
        "new_moon_fixed_sign_malefic": (
            "New Moon forming a conjunction with Saturn or Mars while both are in a fixed sign: "
            "seismic risk window of 7-10 days around the New Moon date."
        ),
    },
    # ── Axis / angular indicators
    "axis_indicators": {
        "rahu_ketu_ic_mc_alignment": (
            "Rahu/Ketu nodal axis aligning within 5° of the IC/MC (4th/10th house cusp) "
            "of a regional chart or Aries Ingress chart for a territory: "
            "major seismic event possible in that territory within 3-6 months."
        ),
        "eclipse_on_ic": (
            "Solar or lunar eclipse occurring on or within 5° of the IC (4th house cusp) "
            "of a regional chart: seismic event near the geographic center of that territory."
        ),
    },
    # ── Stellium / clustering indicators
    "stellium_indicators": {
        "cardinal_sign_stellium": (
            "Three or more planets clustering in cardinal signs (Aries, Cancer, Libra, Capricorn): "
            "signals geopolitical upheaval, leadership crises, sudden large-scale events. "
            "Not a direct seismic indicator but often precedes or coincides with major geophysical events."
        ),
        "sandhi_degree_clustering": (
            "Two or more planets within 2° of a sign boundary (sandhi / gandanta) simultaneously: "
            "earthquake signal. Sign boundaries at 0°/30° of each sign are unstable zones. "
            "Most sensitive boundaries: Pisces-Aries, Cancer-Leo, Scorpio-Sagittarius (gandanta points)."
        ),
    },
    # ── Sign-based seismic affinity
    "fixed_signs_seismic_affinity": {
        "Taurus":    "Earthquakes in South Asia, Mediterranean, Indian subcontinent.",
        "Leo":       "Earthquakes in central/southern Asia, mid-latitudes.",
        "Scorpio":   "Earthquakes in Middle East, Himalayan zone, Pacific Ring of Fire (western arm).",
        "Aquarius":  "Earthquakes in East Asia, Japan, Pacific Ring of Fire (eastern arm).",
    },
    # ── Historical case validations cited by Gopalakrishnan
    "historical_validations": {
        "gujarat_bhuj_2001": (
            "Gujarat/Bhuj Earthquake Jan 26 2001: Saturn retrograde in Taurus (fixed sign); "
            "Mars recently transited eclipse point; Rahu-Ketu axis on Gemini-Sagittarius "
            "near India's IC/MC. Magnitude 7.7, ~20,000 deaths."
        ),
        "turkey_marmara_1999": (
            "Turkey Marmara Earthquake Aug 17 1999: Saturn in Taurus (fixed); "
            "solar eclipse Aug 11 1999 at 18° Leo (fixed); Mars transited eclipse point within days. "
            "Magnitude 7.6, ~17,000 deaths."
        ),
        "kobe_1995": (
            "Kobe Japan Earthquake Jan 17 1995: Saturn in Aquarius (fixed); "
            "lunar eclipse Jan 5 1995; Mars-Saturn aspect active. "
            "Magnitude 6.9, ~6,400 deaths."
        ),
        "san_francisco_1906": (
            "San Francisco Earthquake Apr 18 1906: Saturn in Aquarius (fixed, retrograde); "
            "sandhi clustering noted at sign boundaries. "
            "Magnitude 7.9, ~3,000 deaths."
        ),
    },
    "created_at": _NOW,
}

# ============================================================
ALL_SPECS = [
    GOPAL_CH6_MASS_DEATH_SPEC,
    GOPAL_CH7_EARTHQUAKE_SPEC,
]

# ============================================================
async def run():
    if DRY_RUN:
        print(f"DRY RUN — {len(ALL_SPECS)} engine specs from batch {_BATCH}")
        print(f"Collection: {COLLECTION}  |  science: mundane_jyotish\n")
        for s in ALL_SPECS:
            print(f"  {s['spec_id']}")
        print(f"\nTotal: {len(ALL_SPECS)}\n\nDry run complete.")
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
