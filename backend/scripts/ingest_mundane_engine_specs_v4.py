"""
Mundane Astrology — Engine Specs v4
Batch: mundane-engine-v4-20260506

Source: Gaur, "Mundane Astrology" (AIFAS)
  Chapter 10 — Transit of Planets (pp. 85-110)
  Chapter 11 — Results of Eclipse (pp. 111-116)

Spec types: lookup_table
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
_BATCH     = "mundane-engine-v4-20260506"
_NOW       = datetime.now(timezone.utc)
DRY_RUN    = True
# ---------------------------------------------------------------------------

# ============================================================
# 1. SUN TRANSIT — 12 SIGNS  (Gaur Ch 10, pp. 85-87)
# ============================================================
GAUR_CH10_SUN_TRANSIT_SIGNS = {
    "spec_id": "gaur-ch10-sun-transit-signs",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Sun Transit Through 12 Signs — Commodity Price Effects",
    "source_chapter": "Gaur Ch 10, p.85",
    "note": "Sun results materialize in 14-15 days after nakshatra entry.",
    "transit_by_sign": {
        "Aries":       "Gold, silver, gur, sugar, fruits, dry fruits, til, oil, ghee, thread expensive. Wheat and pulses cheap.",
        "Taurus":      "Gold, silver, gur, sugar, juicy materials, til, other oil materials, dry fruits expensive. Gram, barley, pulses cheap.",
        "Gemini":      "Gold, silver, gur, sugar, juicy materials, til, oils, jute materials, thread, grains (wheat/gram) expensive. Pulses expensive.",
        "Cancer":      "Wheat, gram, barley, pulses (moong, moth, arhar, urad) cheap. Gold, silver, gur, sugar, khand, fruits, dry fruits expensive.",
        "Leo":         "Gold, silver, gur, khand, sugar, juicy materials, til, oils, red-coloured things, gems expensive. Grains and pulses cheap.",
        "Virgo":       "Cotton cheap. Til and other oil materials, cotton, coconut expensive.",
        "Libra":       "Wheat, wood apple, barley, gram, gold, copper, red sandal, betelnut expensive. Cotton and silver cheap.",
        "Scorpio":     "Gold, silver, copper, cotton expensive. Red colour things cheap.",
        "Sagittarius": "Wheat, gram, barley cheap. Gold, silver, cotton, thread, til, oil materials expensive.",
        "Capricorn":   "Wheat, gram, jute cheap. Gur, khand, sugar, juicy materials, cotton, thread, oil, ghee expensive.",
        "Aquarius":    "Wheat, gram cheap. Gur, khand, jute, til, oil, ghee, ground nut expensive.",
        "Pisces":      "Sesame, oils, juicy materials (gur/khand), cotton, thread, gold expensive. Grains and pulses cheap.",
    },
    "transit_nakshatra_by_sign_note": "See spec gaur-ch10-sun-transit-nakshatras for per-nakshatra effects.",
    "created_at": _NOW,
}

# ============================================================
# 2. SUN TRANSIT — 28 NAKSHATRAS  (Gaur Ch 10, pp. 86-87)
# ============================================================
GAUR_CH10_SUN_TRANSIT_NAKSHATRAS = {
    "spec_id": "gaur-ch10-sun-transit-nakshatras",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Sun Transit in Various Constellations — Commodity Price Effects",
    "source_chapter": "Gaur Ch 10, pp.86-87",
    "note": "Results materialize in 14-15 days.",
    "transit_by_nakshatra": {
        "Ashwini":       "Gold, silver, copper, iron, til, oils, red sandal, cotton cloth, clove, cardamom and grains expensive. Cotton cheap.",
        "Bharani":       "Gold, silver, copper metals, brass utensils, wheat, barley, gram, juicy materials (gur/khand), ghee and oil materials expensive. Cotton cheap.",
        "Krithika":      "Gold, silver, wheat, barley, gram grains, pulses (moong/moth), oil materials and ghee expensive.",
        "Rohini":        "Wheat, barley, gram grains, juicy materials (gur/khand), oils, oil materials, ghee, woolen and cotton clothes, chillies expensive. Silver cheap.",
        "Mrigshira":     "Gold, silver, moong, moth, urad, pulses, gram millet and materials cultivated in water expensive.",
        "Ardra":         "Wheat, gram, rice, barley grains, silver, cotton, oil cake expensive. Gold becomes cheap.",
        "Punarvasu":     "Gur, khand juicy materials, cotton, thread, til, oil materials, pulses and grocery materials expensive.",
        "Pushya":        "Wheat, barley, gram, rice grains, til, oils, gold, silver metals and woolen clothes expensive. Cotton and thread cheap.",
        "Ashlesha":      "Wheat, rice, gram grains, pulses (urad/moong), gold, silver metals, oils, ghee and chillies expensive.",
        "Magha":         "Til, oil materials, pulses such as moong, silver expensive.",
        "Poorvaphalguni":"Wheat grains, gur, khand, oils and oil materials, ghee, woolen and cotton clothes expensive. Silver cheap.",
        "Uttaraphalguni":"Gold, silver, iron metals, til, oil materials, ghee, rice, urad, cotton expensive.",
        "Hast":          "Barley, wheat grains, gur, khand juicy materials, spices such as turmeric, coriander expensive.",
        "Chitra":        "Gold, silver metals, grains such as gram, pulses, yarn, red clothes, gur and khand expensive.",
        "Swati":         "Gold, silver metals, gur, khand, oil materials, perfumes, yarn and silk clothes expensive.",
        "Vishakha":      "Wheat, rice, barley grains, pulses, til, oil materials, gur and khand expensive. Silver cheap.",
        "Anuradha":      "Grains such as wheat, barley; woollen clothes expensive. Wheat, gold, silver cheap.",
        "Jyeshtha":      "Gold, silver metals, wheat, barley, gram, rice, oil materials, perfumes, gur and khand expensive. Cotton cheap.",
        "Mool":          "Gold, silver, cotton, yarn cheap.",
        "Poorvashadh":   "Gur, khand, woollen clothes, silver, til, oil materials expensive.",
        "Uttarashadh":   "Wheat, gram, rice grains, pulses (moong/urad), gur, khand juicy materials, oil materials and jute goods expensive.",
        "Shravan":       "Wheat, barley, rice grains, gur, khand, gold, silver and yarn expensive.",
        "Dhanishtha":    "Wheat grains, pulses, gold, silver, gems, cotton and yarn expensive.",
        "Shatbhisha":    "Grains such as wheat, til and other oil materials, gur, gold, silver, cotton clothes, perfumery expensive.",
        "Poorvabhadrapad": "Wheat, gram grains, pulses, gur, khand, oils, oil materials, ghee, gold, silver metals, clothes expensive.",
        "Uttarabhadrapad": "Wheat, rice, gur, khand juicy materials and oils expensive.",
        "Revti":         "Wheat, gram, rice grains, oil materials, peanuts, cotton expensive.",
        "Abhijit":       "(Sub-nakshatra) — refer Uttarashadh results.",
    },
    "created_at": _NOW,
}

# ============================================================
# 3. SUN INGRESS — WEEKDAY × SIGN + MUHURTI TIER  (Gaur Ch 10, pp.87-91)
# ============================================================
GAUR_CH10_SUN_INGRESS_WEEKDAY = {
    "spec_id": "gaur-ch10-sun-ingress-weekday",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Sun Ingress — Weekday × Sign Commodity Effects + Muhurti Tier Framework",
    "source_chapter": "Gaur Ch 10, pp.87-91",
    "note": "Ingress = Sun's entry from one zodiac sign to next (Sankranti). Above results are broad; for minute results consider zodiac signs of planets, constellations etc.",
    "ingress_by_sign_weekday": {
        "Aries": {
            "Sun_Tue_Sat": "Wheat, gram, barley, majeeth (madder), saffron expensive.",
            "Mon":         "Gur, khand, oils, oil materials, cotton, cotton clothes expensive.",
            "Thu":         "Grains are cheap.",
            "Wed_Fri":     "Grains cheap. White things and sugar cheap.",
        },
        "Taurus": {
            "Sun_Tue_Sat": "Grains, gur and khand, dry fruits and grocery materials expensive.",
            "Mon":         "Grains expensive.",
            "Wed_Thu_Fri": "Grains cheap. Oils, oil materials, cotton, cotton clothes, white things and sugar expensive.",
        },
        "Gemini": {
            "Sun_Tue_Sat": "Grains expensive.",
            "Wed":         "Gems expensive.",
            "Mon_Thu_Fri": "Grains and yarn expensive.",
        },
        "Cancer": {
            "Sun_Tue":     "Grains such as wheat, gram, gur, khand and ghee expensive.",
            "Mon_Thu_Fri": "Grains cheap.",
            "Wed":         "Trees break down due to high velocity winds; birds destroyed.",
            "Sat":         "Grains expensive, gold/silver/copper cheap.",
        },
        "Leo": {
            "Sun_Tue_Sat": "Pulses such as moong, moth, urad expensive.",
            "Thu":         "Rains more, ghee cheap. Oils and juicy materials (gur/khand) expensive.",
            "Mon_Wed_Thu_Fri": "Grains cheap.",
        },
        "Virgo": {
            "Sun":     "Grains, gold, silver metals, gur, sugar expensive. Fluctuations in oils, ghee.",
            "Mon":     "Grains, pulses, oil materials, gur expensive. Silver and khand cheap.",
            "Tue":     "Pulses, wheat, cuminseed, spices expensive.",
            "Wed":     "Ghee and silver cheap.",
            "Thu":     "Wheat, gold cheap.",
            "Fri":     "Grains cheap.",
            "Sat":     "Ghee, gur, khand expensive. Cotton cheap. Gold, silver medium.",
        },
        "Libra": {
            "Sun":     "Grains, spices expensive. Pulses cheap.",
            "Mon":     "Grains medium. Gur, khand expensive. Gold/copper fluctuate; silver, rice, pulses cheap.",
            "Tue":     "Grains, chillies, spices, gold, silver, pulses medium. Arhar expensive. Ghee/oils fluctuate. Rice, cattles cheap.",
            "Wed":     "Grains such as wheat/rice and white things cheap. Oils expensive.",
            "Thu":     "Grains, pulses cheap. Oil materials and metals such as gold expensive.",
            "Fri":     "Grains cheap. Gur, khand and gold expensive. Oils, pulses medium.",
            "Sat":     "Wheat, rice, gram, gur, khand, ghee and oil materials expensive. Cotton and silver cheap.",
        },
        "Scorpio": {
            "Sun":     "Grains, oils, gold, silver metals, turmeric, chillies, spices expensive.",
            "Mon":     "Grains, silver, ghee cheap. Gold, iron, oil materials expensive.",
            "Tue":     "Grains, pulses, gur and khand cheap.",
            "Wed":     "Gur, khand, rice, silver, cotton cheap. Red colour goods expensive.",
            "Thu":     "Gur, khand, oils, red goods expensive. Pulses, gold, silver, oils cheap.",
            "Fri":     "Grains and oils expensive. Pulses medium. Gold/silver initially expensive then cheap.",
            "Sat":     "Grains fluctuate then cheap. Oil materials medium. Iron, brass, millet high.",
        },
        "Sagittarius": {
            "Sun":     "Grains, gold, oils, gur, khand medium. Grocery expensive.",
            "Mon":     "Wheat, rice, silver cheap. Oils, red colour, iron expensive.",
            "Tue":     "Grains, oils, ghee, cotton, silver, rice, red colour clothes expensive. Pulses cheap.",
            "Wed":     "Pulses, cattlefeed, dry fruits, spices cheap. Oils medium.",
            "Thu":     "Grains cheap. Moong, urad, silver, juicy materials expensive.",
            "Fri":     "Grains, cotton medium. Gold/silver expensive. Gur, oils cheap with some fluctuations.",
            "Sat":     "Grains, gold, silver, metals, cotton, white things expensive. Ghee, rice cheap.",
        },
        "Capricorn": {
            "Sun":     "Grains, gur, oil, arhar, spices undergo fluctuations but expensive.",
            "Mon":     "Grocery, gur, khand, gold, cotton, silver, rice, ghee, oil cheap. Pulses medium.",
            "Tue":     "Grains, gur, khand, oils expensive. Gold/silver/grocery fluctuate. Ghee, pulses cheap.",
            "Wed":     "Dry fruits expensive. Gold, silver, yarn cheap. Arhar, turmeric, spices expensive. Ghee, rice cheap.",
            "Thu":     "Grains, gur, khand, ghee cheap. Gold/silver/grocery fluctuate.",
            "Fri":     "Wheat, gram, gur, khand cheap. Gold fluctuates. Grocery cheap.",
            "Sat":     "Grains expensive after fluctuations. Gur, khand, oils cheap. Gold expensive, silver cheap.",
        },
        "Aquarius": {
            "Sun":     "Grains expensive. Gur, khand, maize, cotton clothes, oil materials cheap.",
            "Mon":     "Wheat, barley, gram, gold, silver cheap. Moong, urad, oils expensive.",
            "Tue":     "Wheat, gram, pulses expensive. Gold, silver, brass, zinc, coins cheap.",
            "Wed":     "Wheat, barley, gram, peas, spices cheap. Moong, urad, tuar expensive.",
            "Thu":     "Moong, moth, maize, rice, millet, gold, silver, copper, brass, dry fruits, oils cheap. Wheat, barley, silk expensive.",
            "Fri":     "Millet, maize cheap. Wheat, gram expensive with fluctuations. Til, oils, grocery, gur, khand, sugar expensive.",
            "Sat":     "Wheat, gram, salt, chillies, ghee, milk expensive. Moong, moth, urad cheap.",
        },
        "Pisces": {
            "Sun":     "Gold, silver cheap. Fluctuations in wheat, gram, maize, masoor, perfumes, ghee, oil, gur, khand, urad.",
            "Mon":     "Wheat, gram, oils, mustard, cotton, ghee, milk expensive.",
            "Tue":     "Wheat, gram, cotton, yarn, moong, urad, masoor, gold, milk expensive. Ghee cheap.",
            "Wed":     "Wheat, barley, gram, milk, perfumes medium.",
            "Thu":     "Grains cheap. Moong, urad, spices, oils, cotton, copper expensive. Gold, silver, dry fruits cheap.",
            "Fri":     "Gold, silver, gur, khand, sugar, wheat, barley, salt, chillies expensive.",
            "Sat":     "Wheat, gram, barley, oils, gur, khand, sugar medium. Red colour things expensive.",
        },
    },
    "muhurti_tier": {
        "15_muhurti": {
            "nakshatras": ["Bharani", "Ardra", "Ashlesha", "Jyeshtha", "Shatbhisha"],
            "effect": "Grains and juicy materials are expensive. Rains are less.",
        },
        "30_muhurti": {
            "nakshatras": ["Ashwini", "Krithika", "Mrigshira", "Pushya", "Magha",
                           "Poorvaphalguni", "Hast", "Chitra", "Anuradha", "Mool",
                           "Poorvashadh", "Shravan", "Dhanishtha", "Poorvabhadrapad", "Revti"],
            "effect": "Grains, grass, juicy materials etc are medium.",
        },
        "45_muhurti": {
            "nakshatras": ["Rohini", "Punarvasu", "Uttaraphalguni", "Vishakha",
                           "Uttarashadh", "Uttarabhadrapad"],
            "effect": "Rains are good. Grains, ghee, oil, cotton etc are cheap.",
        },
    },
    "created_at": _NOW,
}

# ============================================================
# 4. MOON TRANSIT — 12 SIGNS + 28 NAKSHATRAS  (Gaur Ch 10, pp. 92-93)
# ============================================================
GAUR_CH10_MOON_TRANSIT = {
    "spec_id": "gaur-ch10-moon-transit",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Moon Transit — 12 Signs + 28 Nakshatras Commodity Effects",
    "source_chapter": "Gaur Ch 10, pp.92-93",
    "note": "Moon is fast-moving; stays ~2.25 days per sign, ~1 day per nakshatra. Minor but real influence on commodity prices.",
    "transit_by_sign": {
        "Aries":       "Wheat, gram, barley expensive. Gold and silver cheap.",
        "Taurus":      "Wheat, urad (horsebean), peanut, cotton and silver expensive. Cattles cheap.",
        "Gemini":      "Wheat, gram, cotton and yarn expensive.",
        "Cancer":      "Gold, silver, cotton and yarn cheap.",
        "Leo":         "Gold, silver and cotton expensive.",
        "Virgo":       "Metals such as gold and silver expensive. Cotton cheap.",
        "Libra":       "Gold, silver, rice, ghee and cotton cheap.",
        "Scorpio":     "Gold, silver, cotton cheap.",
        "Sagittarius": "Cotton, yarn and oils cheap.",
        "Capricorn":   "Metals such as gold and silver, clothes and fruits expensive.",
        "Aquarius":    "Gold, silver, cotton and yarn cheap. Oils expensive.",
        "Pisces":      "Gold and oil materials expensive. Silver cheap.",
    },
    "transit_by_nakshatra": {
        "Ashwini":         "Gold, silver and cotton cheap.",
        "Bharani":         "Silver, cotton and salt cheap.",
        "Krithika":        "Silver cheap but cotton expensive.",
        "Rohini":          "Wheat, gram, gur and khand expensive.",
        "Mrigshira":       "Gold, silver and cotton cheap.",
        "Ardra":           "Gold, silver, copper, gur and khand expensive.",
        "Punarvasu":       "Gold, silver, wheat, gram, moong and urad cheap.",
        "Pushya":          "Gold, silver, gur, khand, cotton and wheat cheap.",
        "Ashlesha":        "Gold, silver and cotton cheap.",
        "Magha":           "Prices of gold, silver and cotton fluctuate.",
        "Poorvaphalguni":  "Silver, wheat, gram, gur and khand cheap.",
        "Uttaraphalguni":  "Gold, silver, copper metals cheap.",
        "Hast":            "Gold, silver, copper cheap. Oil materials expensive.",
        "Chitra":          "Gold, silver, wheat, gram and moong expensive.",
        "Swati":           "Gold, silver and cotton cheap.",
        "Vishakha":        "Gold, silver, cotton, yarn expensive. Oils cheap.",
        "Anuradha":        "Gold, silver cheap. Wool expensive.",
        "Jyeshtha":        "Silver, cotton and yarn cheap.",
        "Mool":            "Silver, cotton and white clothes expensive.",
        "Poorvashadh":     "Gold, brass, gur and khand cheap.",
        "Uttarashadh":     "Gold, silver, gur, khand, salt and fruits cheap.",
        "Shravan":         "Gold, silver and grains cheap.",
        "Dhanishtha":      "Gold and silver expensive. Gur and khand cheap.",
        "Shatbhisha":      "Gold cheap but silver expensive.",
        "Poorvabhadrapad": "Gold, silver, cotton and grains cheap.",
        "Uttarabhadrapad": "Gold, silver, cotton and clothes cheap.",
        "Revti":           "Gold, silver and fruits cheap.",
        "Abhijit":         "(Sub-nakshatra) — refer Uttarashadh results.",
    },
    "created_at": _NOW,
}

# ============================================================
# 5. MARS TRANSIT — 12 SIGNS + 28 NAKSHATRAS + MOTION STATES  (Gaur Ch 10, pp.93-96)
# ============================================================
GAUR_CH10_MARS_TRANSIT = {
    "spec_id": "gaur-ch10-mars-transit",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Mars Transit — 12 Signs + 28 Nakshatras + Direct/Retrograde Effects",
    "source_chapter": "Gaur Ch 10, pp.93-96",
    "notes": {
        "influence_duration": "15 days to 1 month in a sign.",
        "conjunction_rule": "Conjunction/aspect with benefic planet: price fall. With malefic planet: price rise.",
        "constellation_duration": "Effect persists 12-24 days after nakshatra entry.",
        "direct_motion": "Direct Mars causes fall in cotton prices after 3 days. Keeps oils and silver expensive.",
        "retrograde_motion": "Retrograde Mars keeps gold, silver, wheat, red things and goods influenced by own signs expensive.",
        "rising": "When Mars rises: grains cheap, oils and oil materials expensive. Effect after 5 days.",
        "combusted": "When Mars combusted: grains (wheat/gram) and gur expensive.",
    },
    "transit_by_sign": {
        "Aries":       "Grains cheap. Gold, silver metals, gems, jute products, cotton and woolen clothes expensive.",
        "Taurus":      "Grains, red colour goods, clothes, gold, silver, copper metals and oils expensive.",
        "Gemini":      "Juicy materials (gur/khand), copper and red things expensive. Benefic with Mars: prices down. Malefic with Mars: prices elevated.",
        "Cancer":      "Grains, gur, khand, juicy materials, oils and oil materials cheap.",
        "Leo":         "Grains, gur, khand, gold, silver, red things and red clothes expensive.",
        "Virgo":       "Wheat, gram, red things and gold expensive.",
        "Libra":       "Grains, pulses, jute, cotton and yarn expensive.",
        "Scorpio":     "Grains, gur, khand juicy materials, metals such as gold and silver expensive.",
        "Sagittarius": "Grains, metals such as gold and silver, oil materials and ghee expensive.",
        "Capricorn":   "Grains cheap. Gur, khand, ghee, oil materials, metals such as gold and silver expensive.",
        "Aquarius":    "Grains, gur, khand and gold expensive. Cotton and silver cheap.",
        "Pisces":      "(refer results similar to water signs)",
    },
    "transit_by_nakshatra": {
        "Ashwini":        "Grains, gur, khand and sugar expensive. Gold and silver cheap.",
        "Bharani":        "Grains, metals such as gold and silver expensive.",
        "Krithika":       "Grains, moong, moth, pulses, ghee and silver expensive.",
        "Rohini":         "Oils, oil materials, red things and chillies expensive.",
        "Mrigshira":      "Til (sesame) and silver expensive. Grains and pulses cheap.",
        "Ardra":          "Sesame, oil materials, gur, khand, cotton and salt expensive. Silver cheap.",
        "Punarvasu":      "Oils, oil materials, silver, cotton and khand expensive.",
        "Pushya":         "Gold expensive. Silver remains cheap.",
        "Ashlesha":       "Grains expensive. Silver and cotton cheap. In fourth pad of Ashlesha, silver very cheap.",
        "Magha":          "Grains, pulses and oil materials expensive.",
        "Poorvaphalguni": "Oils, oil materials, gur and khand expensive.",
        "Uttaraphalguni": "Juicy materials (gur/khand), transport cattles expensive.",
        "Hast":           "Juicy materials (gur/khand), ghee and salt expensive.",
        "Chitra":         "Metals such as gold and silver, grains expensive.",
        "Swati":          "Wheat, oils, oil materials, woolen clothes expensive. Gold cheap.",
        "Vishakha":       "Wheat, cotton and clothes expensive.",
        "Anuradha":       "Grains, red things and clothes expensive.",
        "Jyeshtha":       "Silver cheap. Gold and grains expensive.",
        "Mool":           "Grains such as wheat, barley and gram, pulses, gold and silver expensive.",
        "Poorvashadh":    "Grains cheap. Metals (gold/silver), oils, oil materials, ghee expensive.",
        "Uttarashadh":    "Oils, oil materials and cotton expensive.",
        "Shravan":        "Grains, metals such as gold and silver expensive.",
        "Dhanishtha":     "Metals (gold/silver) expensive. Gur, khand, ghee and grains cheap.",
        "Shatbhisha":     "Grains cheap. Gold and silver too cheap.",
        "Poorvabhadrapad":"Metals (gold/silver), oils, oil materials, cotton expensive.",
        "Uttarabhadrapad":"Grains (wheat/barley/gram), metals (gold/silver), red things, perfumes expensive.",
        "Revti":          "Grains, pulses, gold cheap. Silver expensive.",
        "Abhijit":        "(Sub-nakshatra) — refer Uttarashadh results.",
    },
    "direct_motion_by_sign": {
        "Aries": "Grains cheap.", "Taurus": "Red things expensive.",
        "Gemini": "All materials may become very costly or very cheap suddenly.",
        "Cancer": "Herbs and vegetables expensive.", "Leo": "Grains expensive.",
        "Virgo": "Oils, oil materials and wheat expensive.", "Libra": "Grains expensive in W and S provinces.",
        "Scorpio": "Harmful for cattles.", "Sagittarius": "Grains cheap.",
        "Capricorn": "Grain prices medium. Electronic goods cheap.",
        "Aquarius": "Grains expensive.", "Pisces": "Grains and ghee cheap.",
    },
    "retrograde_entry_by_sign": {
        "Aries": "Grains expensive.", "Taurus": "Red things expensive.",
        "Gemini": "All goods become expensive or cheap gradually.",
        "Cancer": "Grains fluctuate, herbs cheap.", "Leo": "Grains cheap.",
        "Virgo": "Wheat, oils and oil materials cheap.", "Libra": "Grains cheap.",
        "Scorpio": "Cattles increase.", "Sagittarius": "Grains and ghee expensive.",
        "Capricorn": "Wheat, electrical/electronic goods expensive.",
        "Aquarius": "Grains cheap.", "Pisces": "Grains and ghee expensive.",
    },
    "created_at": _NOW,
}

# ============================================================
# 6. MERCURY TRANSIT — 12 SIGNS + 28 NAKSHATRAS + MOTION STATES  (Gaur Ch 10, pp.96-99)
# ============================================================
GAUR_CH10_MERCURY_TRANSIT = {
    "spec_id": "gaur-ch10-mercury-transit",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Mercury Transit — 12 Signs + 28 Nakshatras + Motion State Effects",
    "source_chapter": "Gaur Ch 10, pp.96-99",
    "notes": {
        "direct_motion_general":   "Grains expensive. Silver and cotton undergo fluctuations initially, later expensive. Gur and perfumes also expensive.",
        "retrograde_general":      "Juicy materials (gur/khand) expensive. Grains cheap.",
        "rising":                  "Wheat and gram expensive.",
        "combusted":               "Wheat, gram, ghee cheap.",
    },
    "transit_by_sign": {
        "Aries":       "Gur, khand, gram, oils, gold, silver metals, gems cheap.",
        "Taurus":      "Grains, pulses, til (sesame) and oils expensive.",
        "Gemini":      "Gold and silver cheap. Fluctuation in oil materials. Cattles expensive.",
        "Cancer":      "Grains medium. Gur, oils and oil materials expensive. Silver and white things cheap.",
        "Leo":         "Grains medium. Metals (gold/silver), gur, khand cheap.",
        "Virgo":       "Grains, gur and sugar expensive. Silver cheap.",
        "Libra":       "Juicy materials (gur/khand) and gold expensive. Oil materials cheap.",
        "Scorpio":     "Grains cheap. Oils, oil materials, ghee and silver expensive.",
        "Sagittarius": "Silver, cotton, yarn and clothes cheap.",
        "Capricorn":   "Grains medium. Gold and silver expensive.",
        "Aquarius":    "Gur, khand, oils and ghee expensive. Silver and cotton cheap.",
        "Pisces":      "Juicy materials (gur/khand), grains cheap.",
    },
    "transit_by_nakshatra": {
        "Ashwini":        "Grains (wheat/gram/millet), pulses expensive. Gur, khand, til, oil materials and silver cheap.",
        "Bharani":        "Wheat, rice expensive.",
        "Krithika":       "Grains and cotton expensive. Silver cheap.",
        "Rohini":         "Oils, oil materials, gur, khand expensive. Woolen and silk clothes cheap. Cotton cheap.",
        "Ardra":          "Grains, til, moong, moth, pulses cheap.",
        "Punarvasu":      "Silver, cotton and yarn cheap.",
        "Pushya":         "Gold and silver cheap. Gems and woolen clothes expensive.",
        "Ashlesha":       "Oils, oil materials, gur, khand, moong expensive.",
        "Magha":          "Grains (wheat/gram/barley), yarn and clothes expensive.",
        "Poorvaphalguni": "Grains, gur, khand cheap.",
        "Uttaraphalguni": "Pulses expensive. Cotton and silver cheap.",
        "Hast":           "Grains cheap.",
        "Chitra":         "Grains slightly expensive. Cotton and silver unstable.",
        "Swati":          "Cotton cheap.",
        "Vishakha":       "Grains and cotton cheap.",
        "Anuradha":       "Gold and silver cheap. Grains medium.",
        "Jyeshtha":       "Gur, khand, ghee and rice expensive.",
        "Mool":           "All grains, gold, silver cheap.",
        "Poorvashadh":    "All grains, gold, silver cheap.",
        "Uttarashadh":    "All grains cheap.",
        "Shravan":        "Gur, khand, rice, wheat expensive.",
        "Dhanishtha":     "Gold and silver cheap. Grains and rice expensive.",
        "Shatbhisha":     "All grains expensive. Gold and silver cheap.",
        "Poorvabhadrapad":"Grains, gold, copper, silver cheap.",
        "Uttarabhadrapad":"Grains, gur, khand medium.",
        "Revti":          "Juicy materials (gur/khand), oil materials, ghee, silver, red chillies cheap.",
        "Abhijit":        "(Sub-nakshatra) — refer Uttarashadh results.",
        "Mrigshira":      "Grains, til (sesame), moong, moth, pulses cheap.",
    },
    "direct_motion_by_sign": {
        "Aries": "Cattles cheap.", "Taurus": "Yarn, clothes, wheat, silver, sugar cheap.",
        "Gemini": "Pulses cheap.", "Cancer": "Silver, yarn, rice cheap. Water-grown materials expensive.",
        "Leo": "Cotton, jute materials and shares cheap.", "Virgo": "Dry fruits expensive.",
        "Libra": "Ghee, sugar, herbs expensive.", "Scorpio": "Oil materials expensive.",
        "Sagittarius": "Gur, khand, rice expensive.", "Capricorn": "Mustard cheap.",
        "Aquarius": "Gold and leather expensive.", "Pisces": "Gur, khand and oil materials cheap.",
    },
    "retrograde_entry_by_sign": {
        "Aries": "Grocery materials expensive.", "Taurus": "Silver expensive.",
        "Gemini": "Vegetables cheap.", "Cancer": "Grains cheap.",
        "Leo": "Grains and metals expensive.", "Virgo": "Grains cheap.",
        "Libra": "Gold expensive.", "Scorpio": "Juicy materials (gur) expensive.",
        "Sagittarius": "Dry fruits expensive.", "Capricorn": "Oils and oil materials expensive.",
        "Aquarius": "Juicy materials (gur/khand) expensive.", "Pisces": "Rice, ghee expensive.",
    },
    "created_at": _NOW,
}

# ============================================================
# 7. JUPITER TRANSIT — 12 SIGNS + 28 NAKSHATRAS + MOTION STATES  (Gaur Ch 10, pp.99-101)
# ============================================================
GAUR_CH10_JUPITER_TRANSIT = {
    "spec_id": "gaur-ch10-jupiter-transit",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Jupiter Transit — 12 Signs + 28 Nakshatras + Direct/Retrograde Effects",
    "source_chapter": "Gaur Ch 10, pp.99-101",
    "notes": {
        "direct_motion_general":  "When Jupiter comes in direct motion: grains, metals and pulses are cheap.",
        "retrograde_general":     "Jupiter retrograde: brings down prices of grains, elevates metals such as gold and silver.",
        "rising":                 "When Jupiter rises: gold is cheap, silver is expensive.",
        "combusted":              "When Jupiter is combusted: gold, silver and grains become cheap.",
    },
    "transit_by_sign": {
        "Aries":       "Gold, silver, copper, gur cheap.",
        "Taurus":      "Grains and silver expensive. Coral, pearl, red clothes cheap. During Chaitra month: oils/ghee expensive. During Shravan: gram expensive.",
        "Gemini":      "Metals (gold/silver/copper), cotton clothes, oil materials, ghee expensive. Goods cheap after Margsheersh.",
        "Cancer":      "Grains, gur, khand, ghee and cotton expensive.",
        "Leo":         "Grains and ghee expensive. Metals (gold/silver/copper) cheap.",
        "Virgo":       "Grains, pulses, oils, ghee expensive. Cotton, silver, woolen clothes and metals cheap.",
        "Libra":       "Gold, cotton, coconut, gur, khand expensive. Oils, oil materials and ghee cheap.",
        "Scorpio":     "Metals (gold/silver/copper), oils, oil materials, ghee, gur and white things expensive.",
        "Sagittarius": "Gur, khand juicy materials very cheap. Grains, oils, ghee, gold, silver cheap.",
        "Capricorn":   "Grains, metals and peanuts expensive.",
        "Aquarius":    "Metals (gold/silver/white things) cheap first 3 months, then expensive.",
        "Pisces":      "Gur, khand, pulses, til, oil materials and ghee expensive.",
    },
    "transit_by_nakshatra": {
        "Ashwini":        "Grains, gold, silver cheap.",
        "Bharani":        "Metals (gold/silver), gems, grains, pulses cheap.",
        "Krithika":       "Grains and cotton cheap. Gur, khand and metals fluctuate.",
        "Rohini":         "Gold, silver, gur, khand cheap. In 2nd pad: grains/silver expensive, gur/khand/dry fruits/spices fluctuate. In 3rd pad: grains/gur/khand/ghee/til/oils expensive. In 4th pad: grains/oils/gur/khand/ghee cheap.",
        "Mrigshira":      "Ghee and silver cheap. In 1st pad: til/cotton; 2nd pad: root vegetables/til/rice; 3rd-4th pad: grains expensive.",
        "Ardra":          "Cotton cheap. 1st-2nd pad: metals/gems/perfumery/juicy expensive. 3rd pad: gold/silver/oils expensive. 4th pad: grains/perfumes/juices cheap.",
        "Punarvasu":      "Grains, pulses and metals expensive. 1st-2nd pad: silver and cotton cheap.",
        "Pushya":         "Grains, gold, silver, oils, ghee and cotton expensive.",
        "Ashlesha":       "Grains, metals (gold/silver), oil materials and ghee expensive.",
        "Magha":          "Grains, gold, silver, gur, khand cheap.",
        "Poorvaphalguni": "Grains, juicy materials, metals (gold/silver) cheap.",
        "Uttaraphalguni": "Grains, gur, khand, metals cheap. In 1st pad: silver and white things very cheap.",
        "Hast":           "Wheat, gram, turmeric, gold, silver, oils, ghee, gur, khand and cotton cheap.",
        "Chitra":         "Grains, silver, gur and khand cheap. In 3rd-4th pad: these things expensive.",
        "Swati":          "Grains, gold, silver and juicy materials cheap.",
        "Vishakha":       "Grains, juicy materials (gur/khand) and pulses expensive. Cotton cheap.",
        "Anuradha":       "Grains, metals (gold/silver), juicy materials cheap.",
        "Jyeshtha":       "Fluctuations in grains. Silver cheap.",
        "Mool":           "Pulses, grains, gold and silver cheap.",
        "Poorvashadh":    "Grains, metals (gold/silver), cotton, gur, khand cheap.",
        "Uttarashadh":    "(refer Poorvashadh pattern)",
        "Shravan":        "Grains, gur, khand, gold, silver cheap.",
        "Dhanishtha":     "Wheat, rice, barley, gram, other grains, pulses and cotton cheap. Metals (gold/silver) and juicy expensive.",
        "Shatbhisha":     "Grains, gold, turmeric, saffron cheap. Silver and white things expensive.",
        "Poorvabhadrapad":"Grains, gold, silver, cotton clothes, gur expensive.",
        "Uttarabhadrapad":"Grains, gold, pulses, ghee expensive.",
        "Revti":          "Grains and silver cheap. Gold expensive.",
        "Abhijit":        "(Sub-nakshatra) — refer Uttarashadh results.",
    },
    "direct_motion_by_sign": {
        "Aries": "Ghee, oils, juicy cheap.", "Taurus": "Gold, rice, cotton, yarn cheap.",
        "Gemini": "Grains cheap.", "Cancer": "Water-grown materials cheap.",
        "Leo": "Rice, ghee, cotton, silver expensive.", "Virgo": "Silver cheap.",
        "Libra": "Grains, jute, brass cheap.", "Scorpio": "Gur, khand cheap.",
        "Sagittarius": "Oils, ghee, grains cheap.", "Capricorn": "Grains expensive.",
        "Aquarius": "All materials expensive.", "Pisces": "Grains, oils, ghee, gur, khand, jute cheap.",
    },
    "retrograde_by_sign": {
        "Aries": "Til, oils, perfumes expensive.", "Taurus": "Gold, ghee, oils expensive.",
        "Gemini": "All grocery materials and brass expensive.", "Cancer": "Oils, ghee, gur expensive.",
        "Leo": "Gold, silver cheap but grains expensive.", "Virgo": "Gur, all grains and oils cheap.",
        "Libra": "Oils, ghee, perfumes expensive.", "Scorpio": "All grains and ghee expensive.",
        "Sagittarius": "Juicy materials, oils, ghee and grains expensive.",
        "Capricorn": "All grains cheap.", "Aquarius": "Ghee and oil materials expensive.",
        "Pisces": "Cotton, gur, khand, oil, ghee expensive.",
    },
    "created_at": _NOW,
}

# ============================================================
# 8. VENUS TRANSIT — 12 SIGNS + 28 NAKSHATRAS + MOTION STATES  (Gaur Ch 10, pp.102-104)
# ============================================================
GAUR_CH10_VENUS_TRANSIT = {
    "spec_id": "gaur-ch10-venus-transit",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Venus Transit — 12 Signs + 28 Nakshatras + Direct/Retrograde Effects",
    "source_chapter": "Gaur Ch 10, pp.102-104",
    "notes": {
        "direct_motion_general": "Venus direct: grains, gur, ghee, gold, silver and gems expensive. Cotton cheap.",
        "retrograde_general":    "Venus retrograde: grains (wheat, gur, khand, ghee, oils) expensive.",
        "combusted":             "Venus combusted: gold, silver expensive. Grains expensive initially then cheap later.",
        "rising":                "Venus rises: gold, silver, yarn, clothes, rice expensive. Ghee and khand cheap.",
    },
    "transit_by_sign": {
        "Aries":       "Grains, ghee, gold, silver, gur, khand expensive. Oils and oil materials cheap.",
        "Taurus":      "Grains, cotton cheap. Gold and silver expensive after fluctuations.",
        "Gemini":      "Wheat, gram, barley expensive. Oils, jute fabrics, yarn and clothes cheap.",
        "Cancer":      "Wheat, barley, gram, peas, arhar cheap. Juicy materials (gur/khand), oils and ghee expensive.",
        "Leo":         "Grains, gold, copper, red things, ghee and juices expensive.",
        "Virgo":       "Grains, gur, khand, wood and silken clothes expensive.",
        "Libra":       "Gur, khand expensive. Grains cheap if benefics influence; expensive if malefics aspect or join Venus.",
        "Scorpio":     "Grains, pulses cheap if benefics influence. Gur fluctuates. Malefics cause high prices.",
        "Sagittarius": "Grains, gold, silver metals, clothes and shares expensive.",
        "Capricorn":   "Grains, gur, khand and ghee expensive. Cotton and silver expensive after fluctuations.",
        "Aquarius":    "Grains, pulses, white things, gur, khand, silver cheap.",
        "Pisces":      "Grains, oils, gur, khand cheap. If Venus joined/aspected by malefic: silver expensive. Benefic brings prices down.",
    },
    "transit_by_nakshatra": {
        "Ashwini":        "Grains, pulses, oils, gold, gur and khand cheap.",
        "Bharani":        "Gold, silver, oils, ghee cheap. Grains and pulses expensive.",
        "Krithika":       "Oil, oil materials, gold, silver, gems, rice cheap.",
        "Rohini":         "Metals (gold/silver), oils, gur, khand, dry fruits cheap.",
        "Mrigshira":      "Grains cheap. Juicy materials (gur/khand) expensive.",
        "Ardra":          "Grains, pulses and ghee cheap.",
        "Punarvasu":      "Grains expensive. Metals (gold/silver), yarn cheap.",
        "Pushya":         "Grains, woolen and silken clothes expensive. Juicy materials (gur/khand) cheap.",
        "Ashlesha":       "Rice, tuar grains cheap.",
        "Magha":          "Grains such as wheat expensive.",
        "Poorvaphalguni": "Grains and pulses cheap.",
        "Uttaraphalguni": "Grains and cotton expensive. Metals (gold) fluctuate.",
        "Hast":           "Gold and silver expensive. Wheat cheap. Gur and khand fluctuate.",
        "Chitra":         "Grains and metals have medium prices.",
        "Swati":          "Grains cheap. Gur, khand expensive.",
        "Vishakha":       "Grains expensive.",
        "Anuradha":       "Gur, khand, rice, salt cheap.",
        "Jyeshtha":       "Grains expensive. Metals (gold/silver), til, oils cheap.",
        "Mool":           "Grains and cotton expensive. Gold unstable.",
        "Poorvashadh":    "Oils, oil materials, pulses and salt cheap.",
        "Uttarashadh":    "Grains expensive. Metals (gold/silver), juicy materials cheap.",
        "Shravan":        "Grains, pulses, gold, silver, gur, sugar cheap. Til and oils expensive.",
        "Dhanishtha":     "Grains cheap. Pulses, rice, gold, silver, cotton expensive.",
        "Shatbhisha":     "Grains, metals (gold/silver), oil materials, ghee, gur, khand expensive.",
        "Poorvabhadrapad":"Grains cheap. Cotton expensive.",
        "Uttarabhadrapad":"White things, rice, pearl, salt, khand, cotton cheap. Seasonal/dry fruits expensive.",
        "Revti":          "Juicy materials (gur/khand), white things, silver and gems cheap.",
        "Abhijit":        "(Sub-nakshatra) — refer Uttarashadh results.",
    },
    "direct_motion_by_sign": {
        "Aries": "Til, oils, juicy materials (gur) cheap.", "Taurus": "Gur, ghee and rice expensive.",
        "Gemini": "Cotton, cotton clothes cheap.", "Cancer": "Cattles cheap.",
        "Leo": "Food materials and grains expensive.", "Virgo": "Silver, juicy materials and rice cheap.",
        "Libra": "Ghee, rice and yarn expensive.", "Scorpio": "Grains expensive.",
        "Sagittarius": "Cotton and yarn cheap.", "Capricorn": "Juicy materials (gur/khand) cheap.",
        "Aquarius": "Yarn, silver and clothes expensive.", "Pisces": "All grains and things cheap.",
    },
    "retrograde_by_sign": {
        "Aries": "All trades sluggish.", "Taurus": "Sugar and khand expensive.",
        "Gemini": "Cotton and yarn expensive.", "Cancer": "Cotton and yarn expensive.",
        "Leo": "Metals and cattles expensive.", "Virgo": "Rice, yarn and ghee expensive.",
        "Libra": "Rice and juicy materials expensive.", "Scorpio": "All grains cheap.",
        "Sagittarius": "Spices and cotton cheap.", "Capricorn": "Prices undergo changes.",
        "Aquarius": "Prices undergo changes.", "Pisces": "Cotton, yarn and cloth cheap.",
    },
    "created_at": _NOW,
}

# ============================================================
# 9. SATURN TRANSIT — 12 SIGNS + 28 NAKSHATRAS + MOTION STATES  (Gaur Ch 10, pp.105-108)
# ============================================================
GAUR_CH10_SATURN_TRANSIT = {
    "spec_id": "gaur-ch10-saturn-transit",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Saturn Transit — 12 Signs (with Navmansh detail) + 28 Nakshatras + Direct/Retrograde",
    "source_chapter": "Gaur Ch 10, pp.105-108",
    "notes": {
        "direct_change": "Saturn changes to direct motion: oil materials, chillies and asafoetida expensive for 2 months. Saturn changes to retrograde: oils, grains, ghee become expensive.",
        "rising":        "Saturn rises: mustard oil, peanuts and cotton cheap for 1 month; iron, gur, khand expensive. Saturn combusted: gold cheap, grains expensive.",
        "retrograde_nakshatra_1": "Saturn retrograde in Uttarashadh moving into Poorvashadh: drought, grains become expensive.",
        "retrograde_nakshatra_2": "Saturn retrograde in Magha moving into Ashlesha: wheat and ghee expensive.",
    },
    "transit_by_sign": {
        "Aries":       "Oils, juicy materials (gur/khand), gold, silver, copper, gems, machineries, hardwares expensive. When Saturn is at 28-29°, prices go down.",
        "Taurus":      "Grains, oils, jute products, gur, khand expensive. Less influential in first navmansh; in last 2 navmansh above things cheap.",
        "Gemini":      "Oils, grains, gur, khand, machine parts from iron expensive. Gradually after each navmansh prices may go down.",
        "Cancer":      "Oils, gold, silver, cotton expensive. High prices in first 3 and last 3 navmanshes; low in middle 3 navmanshes.",
        "Leo":         "Oil materials, juicy materials, grains and pulses expensive. Particularly in 3rd navmansh, prices high.",
        "Virgo":       "Gold, silver, gems, gur cheap. In first navmansh: gur, khand cheap particularly. Malefic influence on Saturn makes grains expensive.",
        "Libra":       "Grains, pulses and juicy materials expensive. Oils cheap after 15°.",
        "Scorpio":     "Oils, oil materials, grains and silver expensive. Benefic influence on Saturn: prices fall.",
        "Sagittarius": "Grains, juicy materials, wood, wooden materials, iron machine parts expensive. Benefics make grains cheap.",
        "Capricorn":   "Grains, metals (gold/silver), cotton expensive. Prices change after 15°. Machinery expensive.",
        "Aquarius":    "Grains, gold, silver metals, oils expensive in first 10°. Prices low between 10-20°.",
        "Pisces":      "Grains, gur, khand, ghee expensive in first 6°, cheap in next 6°. Cycle continues. Gold follows same pattern.",
    },
    "transit_by_nakshatra": {
        "Ashwini":        "Oils, oil materials, grains, yarn, red chillies, ghee expensive (up to 1°). Cotton cheap up to 1° then expensive.",
        "Bharani":        "Oils, ghee, gur, khand expensive in 3rd pad.",
        "Krithika":       "Metals (gold/silver) expensive; grains cheap. Oils expensive in 3rd and 4th pad.",
        "Rohini":         "Grains/pulses cheap in 1st-3rd pad, expensive in 2nd-4th pad. Metals expensive in 1st-3rd pad, cheap in 2nd-4th pad.",
        "Mrigshira":      "Grains/pulses cheap in 1st-3rd pad, expensive in 2nd-4th pad. Metals fluctuate. Oils/juicy expensive in 4th pad.",
        "Ardra":          "Grains/juicy/oils cheap in 1st pad. Grains/pulses expensive in 2nd pad, cheap in 3rd-4th pad.",
        "Punarvasu":      "Grains and cotton expensive. Oils, machinery parts cheap.",
        "Pushya":         "1st pad: grains/pulses cheap, gur/khand expensive. 2nd-3rd pad: grains expensive, ghee/gur/khand cheap. 4th pad: grains cheap again, ghee/gur expensive.",
        "Ashlesha":       "1st pad: grains/til/oils/iron parts cheap. Remaining 3 pads: these materials expensive.",
        "Magha":          "Oils/ghee/gur/khand expensive in 1st pad, cheap in 2nd. Dry fruits/perfumes expensive in 2nd pad. 3rd pad: expensive. 4th pad: cheap (but ghee expensive).",
        "Poorvaphalguni": "Oils/grains/pulses unstable in 1st pad. 2nd pad: these expensive.",
        "Uttaraphalguni": "1st pad: oils/ghee/cotton/sugar expensive. 2nd pad: juicy/grains expensive. 3rd pad: grains expensive. 4th pad: metals expensive.",
        "Hast":           "Grains/pulses expensive. 1st pad: cattles expensive. 2nd-3rd pad: gur/khand expensive. 4th pad: grocery costly.",
        "Chitra":         "1st pad: grains expensive, silver/ghee cheap. Remaining 3 pads: malefics make grains/gur/khand expensive; benefics make cheap.",
        "Swati":          "1st pad: grains/pulses cheap. 2nd pad: grains/oils/iron parts expensive. 4th pad: gur/khand/ghee expensive.",
        "Vishakha":       "Grains, pulses, oils, iron, machinery expensive.",
        "Anuradha":       "Grocery and grains expensive. 4th pad: cotton expensive.",
        "Jyeshtha":       "Grains, gold, silver expensive.",
        "Mool":           "All grains, oils and silver expensive. 4th pad: prices low.",
        "Poorvashadh":    "Grains cheap. Oils and grocery cheap in 1st pad.",
        "Uttarashadh":    "Grains, machinery, iron parts and dry fruits expensive.",
        "Shravan":        "Grains expensive in 1st pad, cheap in 2nd, expensive in 3rd, cheap in 4th.",
        "Dhanishtha":     "Grains, pulses and grocery expensive. Gur/khand and iron parts cheap.",
        "Shatbhisha":     "Grains/pulses/gur/khand/grocery cheap in 1st-2nd pad, expensive in 3rd-4th pad.",
        "Poorvabhadrapad":"Grains, oil materials and pulses expensive.",
        "Uttarabhadrapad":"Grains, pulses, oil materials and metals expensive.",
        "Revti":          "Metals (gold/silver) cheap. Grains, oils, pulses expensive. Juicy materials expensive in 4th pad.",
        "Abhijit":        "(Sub-nakshatra) — refer Uttarashadh results.",
    },
    "direct_motion_by_sign": {
        "Aries": "Grains expensive.", "Taurus": "Iron, copper metals cheap.",
        "Gemini": "Ghee, silver, cotton cheap.", "Cancer": "Red chillies and oils cheap.",
        "Leo": "Grocery cheap.", "Virgo": "Oils and juicy materials cheap.",
        "Libra": "Silver expensive.", "Scorpio": "Chillies expensive. Coriander cheap.",
        "Sagittarius": "Grains expensive but oils cheap.", "Capricorn": "All commodities unstable.",
        "Aquarius": "Grains cheap.", "Pisces": "Grains expensive.",
    },
    "retrograde_by_sign": {
        "Aries": "Oils expensive.", "Taurus": "Grains, peanuts expensive.",
        "Gemini": "Wheat, pulses expensive.", "Cancer": "Red chillies and oils expensive.",
        "Leo": "Grocery expensive.", "Virgo": "Grains and juicy materials expensive.",
        "Libra": "Silver cheap.", "Scorpio": "Spices cheap.",
        "Sagittarius": "Gur-khand expensive, oils cheap.", "Capricorn": "Prices of all commodities stable.",
        "Aquarius": "Grains expensive.", "Pisces": "Grains cheap.",
    },
    "created_at": _NOW,
}

# ============================================================
# 10. RAHU TRANSIT — 12 SIGNS  (Gaur Ch 10, pp.109)
# ============================================================
GAUR_CH10_RAHU_TRANSIT = {
    "spec_id": "gaur-ch10-rahu-transit-signs",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Rahu Transit in 12 Signs — Commodity Price and Rainfall Effects",
    "source_chapter": "Gaur Ch 10, p.109",
    "note": "Ketu results are generally inverse of Rahu. Rahu/Ketu always retrograde (mean motion). Drought signal when in Aries or Libra.",
    "transit_by_sign": {
        "Aries":       "Grains expensive. Drought due to lack of rains.",
        "Taurus":      "Juicy materials (gur/khand), oils, oil materials and grocery goods expensive.",
        "Gemini":      "Grains and ghee expensive for first 9 months, cheap later. Gold/silver cheap initially, costly later on.",
        "Cancer":      "Grains expensive but metals (gold/silver/iron) cheap.",
        "Leo":         "Grains cheap but spices and other grocery materials expensive.",
        "Virgo":       "Oils and oil materials cheap. Cotton expensive.",
        "Libra":       "Grains expensive. Drought due to lack of rains.",
        "Scorpio":     "Metals (gold/silver), grains unstable with fluctuations.",
        "Sagittarius": "Grains, cotton and yarn cheap.",
        "Capricorn":   "Grains (wheat/gram/barley) cheap. Metals (gold/silver) expensive.",
        "Aquarius":    "Grains and grocery materials expensive.",
        "Pisces":      "Grains initially expensive, cheap later. Metals (gold/silver) cheap.",
    },
    "created_at": _NOW,
}

# ============================================================
# 11. ECLIPSE COMMODITY TABLES — GAUR CH 11  (pp.111-116)
# ============================================================
GAUR_CH11_ECLIPSE_COMMODITY = {
    "spec_id": "gaur-ch11-eclipse-commodity-tables",
    "spec_type": "lookup_table",
    "science_id": "mundane_jyotish",
    "batch_id": _BATCH,
    "title": "Eclipse Commodity Effects — Monthly, Sign, Nakshatra, Weekday Tables (Gaur)",
    "source_chapter": "Gaur Ch 11, pp.111-116",
    "note": "These are Gaur's commodity-price focused eclipse rules, distinct from Mehta Ch 13's political/leader eclipse rules.",
    "general_rules": [
        "When a sign has an eclipse, things related to that sign or their names become expensive.",
        "Two eclipses within 15 days: turmoils or natural calamities, loss of money and lives, grains expensive.",
        "Saturn also residing in eclipse sign: metals become expensive.",
        "Results of full (100%) eclipse effective in 20 days.",
        "Results of 75% eclipse effective in 1 month.",
        "Results of 50% eclipse effective in 2 months.",
        "Results of 33% eclipse effective in 3 months.",
        "Results of 25% eclipse effective in 4 months.",
        "If rains after eclipse: intensity of undesired results reduced.",
        "If lunar eclipse, 15 days after solar eclipse: beneficial.",
        "If solar eclipse after lunar eclipse: results undesired and detrimental.",
        "If rise or setting during solar/lunar eclipse: commercial goods expensive particularly.",
    ],
    "solar_eclipse_by_hindu_month": {
        "Chaitra":     "Gold and grains become expensive quickly.",
        "Vaishakh":    "Til, oil materials, moong, cotton cloth, yarn, cotton and wheat expensive.",
        "Jyeshtha":    "Gold and grains cheap.",
        "Aashadh":     "Grains expensive. Drought.",
        "Shravan":     "Grains cheap but juicy materials expensive.",
        "Bhadrapad":   "Grains cheap. Other goods also cheap.",
        "Ashwin":      "Grains cheap but oil materials and ghee slightly expensive.",
        "Kartik":      "All grains, ghee, cotton, clothes become cheap.",
        "Margsheersh": "Grains, gur, khand, oil materials, ghee expensive.",
        "Paush":       "All grains expensive.",
        "Maagh":       "Grains cheap, ghee expensive. Rains sufficient.",
        "Phalgun":     "All grains, oil, gur, khand, juicy materials, ghee expensive.",
    },
    "lunar_eclipse_by_hindu_month": {
        "Chaitra":     "Grains expensive in coming months.",
        "Baisakh":     "Grains cheap, ghee expensive, rains sufficient.",
        "Jyeshtha":    "Grains, oils, gur, khand cheap.",
        "Aashadh":     "Grains, ghee, oil materials, gur, khand, cotton and yarn expensive.",
        "Shravan":     "Grains expensive but juicy materials cheap.",
        "Bhadrapad":   "Grains cheap. Gur, khand, ghee and oil materials expensive.",
        "Ashwin":      "Grains and cotton expensive.",
        "Kartik":      "Grains cheap and easily available.",
        "Margsheersh": "Grains expensive in coming months.",
        "Paush":       "Grains (wheat/gram), ghee, oil materials, gur, khand expensive.",
        "Maagh":       "Grains, ghee, oil materials, gur, khand expensive.",
        "Phalgun":     "Grains expensive initially, cheap later. Ghee, oils, gur, khand expensive.",
    },
    "solar_eclipse_weekday": {
        "Sunday":    "Grains, pulses, gur, khand expensive after 2.5 months.",
        "Monday":    "Oil materials, oils, ghee, moong, urad, other pulses expensive.",
        "Tuesday":   "Cotton clothes, cotton, ghee, gur, sugar, grains expensive between 2-4 months.",
        "Wednesday": "Grains, yarn, cotton and steel expensive after 2 months.",
        "Thursday":  "Yellow things, til, oil materials, dry fruits, perfumes expensive.",
        "Friday":    "Grains cheap but yarn, cotton, ghee expensive.",
        "Saturday":  "Til, oil materials, red and yellow things, copper, tobacco expensive after 2 months.",
    },
    "lunar_eclipse_weekday": {
        "Sunday":    "Silver cheap. Wheat, linseed, cotton, red things expensive.",
        "Monday":    "Ghee, oils, oil materials expensive. Cotton and yarn expensive after 2 months.",
        "Tuesday":   "Wheat, linseed grains expensive quickly. Cotton, yarn also expensive. Mustard, methi expensive after 4 months.",
        "Wednesday": "Metals (gold/silver/copper) expensive.",
        "Thursday":  "Ghee, oils, oil materials expensive but cotton and yarn cheap.",
        "Friday":    "Cotton and yarn cheap but prices high after 3 months.",
        "Saturday":  "Mustard, til, oil materials, iron, steel, black clothes expensive after 6 months.",
    },
    "eclipse_by_sign": {
        "Aries":       "Solar eclipse: grocery expensive. Lunar eclipse: gold, silver, sugar, juicy materials, woolen yarn expensive.",
        "Taurus":      "Solar or lunar: commercial and grocery goods expensive.",
        "Gemini":      "Solar: grains, juicy materials expensive after 2 months. Lunar: grocery goods expensive.",
        "Cancer":      "Solar and lunar: grains, gur, khand, oil, ghee, milk expensive after 2 months.",
        "Leo":         "Solar or lunar: grains, til, oil materials, cotton and yarn expensive.",
        "Virgo":       "Solar or lunar: gold, silver, copper, brass unstable but later expensive.",
        "Libra":       "Solar/lunar: saints, holy persons suffer.",
        "Scorpio":     "Solar/lunar: drought causing agony to masses.",
        "Sagittarius": "Solar/lunar: all herbs and grasses expensive.",
        "Capricorn":   "Solar/lunar: metals (gold/silver) and gems expensive.",
        "Aquarius":    "Solar/lunar: oil materials, oils and peanuts rise in price.",
        "Pisces":      "Solar/lunar: gur, khand, juicy materials and water-produced things expensive.",
    },
    "eclipse_by_nakshatra": {
        "Ashwini":        "Solar: ghee, oils, gur, khand, moong expensive. Lunar: gur, khand cheap.",
        "Bharani":        "Solar: gold, silver, copper, grains, jute, cotton expensive. Juicy materials, white clothes expensive after 3 months.",
        "Krithika":       "Solar: gold, silver, gems expensive after 9 months. Shares, juicy materials expensive. Lunar: above things cheap.",
        "Rohini":         "Solar: til, oils, grocery, grains, pulses, gur, khand, jute, cotton, yarn expensive. Lunar: above goods cheap.",
        "Mrigshira":      "Solar: oil materials, ghee, gur, khand, grains, gold expensive. Lunar: above cheap.",
        "Ardra":          "Til, oil materials, ghee, steel and iron expensive.",
        "Punarvasu":      "Grains, cotton, arhar expensive after 3 months. Oils expensive after 5 months.",
        "Pushya":         "Metals (gold/silver/copper), gur, khand and shares expensive. Grains expensive after 3 months.",
        "Ashlesha":       "Metals (gold/silver/copper), gur-khand, turmeric, corianders, cuminseed expensive. Moong expensive after 5 months.",
        "Magha":          "Rice and gram expensive (solar or lunar).",
        "Poorvaphalguni": "Til, oil materials, cotton, yarn, cotton clothes expensive.",
        "Uttaraphalguni": "Rice, gram, oil materials, cotton, yarn expensive (solar or lunar).",
        "Hast":           "Same as Uttaraphalguni.",
        "Chitra":         "Solar or lunar: grains such as millets expensive after 2 months.",
        "Swati":          "Wheat, gram, barley, pulses expensive.",
        "Vishakha":       "Urad, juicy materials and red clothes expensive. Kulthi expensive after 6 months.",
        "Anuradha":       "Solar or lunar: grains expensive after 9 months. Millets/til expensive but rice cheaper.",
        "Jyeshtha":       "Gur, khand, sugar expensive after 5 months. Ghee, copper, gold expensive.",
        "Mool":           "Sugar, gur, khand, millets expensive. Rice expensive after 5 months.",
        "Poorvashadh":    "White things and clothes expensive after 5 months.",
        "Uttarashadh":    "Coconuts, coconut oil, grocery expensive after 5 months.",
        "Shravan":        "Transport animals (horses, elephants, camels) and pulses expensive.",
        "Dhanishtha":     "Pulses (moong/moth/masoor) expensive.",
        "Shatbhisha":     "Grains (wheat/barley/gram) expensive.",
        "Poorvabhadrapad":"Til, oil materials and gram expensive.",
        "Uttarabhadrapad":"Salt and other alkaline things expensive.",
        "Revti":          "Pulses (moong/urad) expensive.",
        "Abhijit":        "(Sub-nakshatra) — refer Uttarashadh results.",
    },
    "planetary_aspect_on_eclipse": {
        "Mars":    "Aspect on eclipse: red things expensive.",
        "Mercury": "Full aspect: ghee, oils, maize, gold, brass and other yellow goods expensive.",
        "Venus":   "Full aspect: white things such as silver, white clothes expensive.",
        "Saturn":  "Full aspect: black things such as iron, urad, black grains, clothes expensive.",
        "Jupiter": "Full aspect on eclipse: reduces undesired results; peace and prosperity prevail.",
    },
    "created_at": _NOW,
}

# ============================================================
ALL_SPECS = [
    GAUR_CH10_SUN_TRANSIT_SIGNS,
    GAUR_CH10_SUN_TRANSIT_NAKSHATRAS,
    GAUR_CH10_SUN_INGRESS_WEEKDAY,
    GAUR_CH10_MOON_TRANSIT,
    GAUR_CH10_MARS_TRANSIT,
    GAUR_CH10_MERCURY_TRANSIT,
    GAUR_CH10_JUPITER_TRANSIT,
    GAUR_CH10_VENUS_TRANSIT,
    GAUR_CH10_SATURN_TRANSIT,
    GAUR_CH10_RAHU_TRANSIT,
    GAUR_CH11_ECLIPSE_COMMODITY,
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
