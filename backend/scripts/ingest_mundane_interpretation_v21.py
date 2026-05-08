#!/usr/bin/env python3
"""
ingest_mundane_interpretation_v21.py

Interpretation rules for Gopal Chapter 11 — How to Predict Rains
Batch: mundane-interp-v21-20260508
Group T — Rainfall Forecasting (8 rules)

Complementary layer to Gaur Ch5/6 (v16, mundane-interp-v16-20260507):
  - Gaur Ch5: Ardra Entry chart (tithi/nakshatra/weekday/time-of-day level)
  - Gaur Ch6: Trinadi + Saptnadi (nadi-vedha level)
  - Gopal Ch11: Seasonal/annual macro level (Rahu transit veto, Tajika
    ingress chart, Prasna Marga balance, Dhana Chakra, 2002 case study)
  Zero overlap confirmed before authoring.

Usage:
  # Dry run (default):
  python3 backend/scripts/ingest_mundane_interpretation_v21.py

  # Live upload:
  python3 -c "
  import asyncio, os
  exec(open('backend/scripts/ingest_mundane_interpretation_v21.py').read().replace('DRY_RUN   = True', 'DRY_RUN   = False'))
  asyncio.run(run())
  "
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME   = "horoscope_db"
BATCH_ID  = "mundane-interp-v21-20260508"
DRY_RUN   = True

NOW = datetime.now(timezone.utc).isoformat()


def _rule(
    rule_id:          str,
    sub_type:         str,
    title:            str,
    source_chapter:   str,
    condition:        str,
    result:           str,
    severity:         str,
    checkable:        bool,
    synthesis_sources: list[str],
    notes:            str,
    weight:           float = 1.0,
) -> dict:
    return {
        "rule_id":          rule_id,
        "batch_id":         BATCH_ID,
        "science_id":       "mundane_jyotish",
        "sub_type":         sub_type,
        "title":            title,
        "source_chapter":   source_chapter,
        "source":           {
            "book":    "Mundane Astrology by Gopalakrishnan",
            "chapter": source_chapter,
        },
        "condition":        condition,
        "result":           result,
        "severity":         severity,
        "weight":           weight,
        "checkable":        checkable,
        "synthesis_sources": synthesis_sources,
        "notes":            notes,
        "approval_status":  "pending_review",
        "created_at":       NOW,
        "updated_at":       NOW,
    }


# ── GROUP T — Rainfall Forecasting (Gopal Ch11) ───────────────────────────────

GROUP_T = [

    # T-01 — Rahu Taurus Critical Alert (validated 2002)
    _rule(
        rule_id        = "mundane-gopal-ch11-rains-rahu-taurus-critical",
        sub_type       = "rainfall_forecast",
        title          = "Rahu Transit Taurus — Critical National Rainfall Alert (2002 Validated)",
        source_chapter = "Gopal Ch 11 — Rahu Transit Veto & 2002 Drought Case Study",
        condition      = (
            "IF Rahu is transiting Taurus (Rishabha)"
        ),
        result         = (
            "CRITICAL RAINFALL ALERT: High probability of hydrological drought. "
            "Taurus is the highest-priority disruptive sign for India's water cycle "
            "per Gopalakrishnan. Validated against the 2002 national drought: "
            "Rahu in Taurus + Saturn/Mercury in 10th of June 15 ingress chart → "
            "29 of 35 meteorological subdivisions below normal. "
            "Activate Dhana Chakra moisture check and Tajika 4th-house audit "
            "for the nearest SW or NE monsoon ingress date."
        ),
        severity       = "critical",
        checkable      = True,
        weight         = 1.0,
        synthesis_sources = ["gopal-ch11-rain-forecasting-engine"],
        notes          = (
            "Rank 1 of 4 in the Rahu Transit Veto. Rahu completes a nodal cycle "
            "every ~18 years; last Taurus transit was 2022–2023. Highest confidence "
            "drought signal in Gopal's modernized Vedic meteorology system. "
            "Cross-check against Gaur Ch5 Ardra Entry chart for the same season — "
            "convergence of Rahu-Taurus + Rohini Mountain residence = near-certain drought."
        ),
    ),

    # T-02 — Rahu Scorpio Severe Alert
    _rule(
        rule_id        = "mundane-gopal-ch11-rains-rahu-scorpio-severe",
        sub_type       = "rainfall_forecast",
        title          = "Rahu Transit Scorpio — Severe NE Monsoon Disruption Alert",
        source_chapter = "Gopal Ch 11 — Rahu Transit Veto",
        condition      = (
            "IF Rahu is transiting Scorpio (Vrichika)"
        ),
        result         = (
            "SEVERE RAINFALL ALERT: Scorpio is the mirror axis of Taurus in the "
            "Rahu Transit Veto system. High probability of NE monsoon disruption "
            "and drought risk in southern India (Tamil Nadu, coastal Andhra, Kerala). "
            "The SW monsoon may be adequate nationally while the NE monsoon fails. "
            "Run Tajika ingress audit for the October Sun-ingress chart."
        ),
        severity       = "high",
        checkable      = True,
        weight         = 0.85,
        synthesis_sources = ["gopal-ch11-rain-forecasting-engine"],
        notes          = (
            "Rank 2 of 4 in the Rahu Transit Veto. Scorpio is a fixed water sign — "
            "Rahu's transit here disrupts the NE monsoon more than the SW. "
            "Rahu transits Taurus and Scorpio alternately every ~9 years."
        ),
    ),

    # T-03 — Rahu Leo Moderate Alert
    _rule(
        rule_id        = "mundane-gopal-ch11-rains-rahu-leo-moderate",
        sub_type       = "rainfall_forecast",
        title          = "Rahu Transit Leo — SW Monsoon Onset Delay Alert",
        source_chapter = "Gopal Ch 11 — Rahu Transit Veto",
        condition      = (
            "IF Rahu is transiting Leo (Simha)"
        ),
        result         = (
            "MODERATE RAINFALL ALERT: Leo is a fixed fire sign. Rahu's transit "
            "here generates excess heat in the planetary environment, reducing cloud "
            "formation capacity and potentially delaying the SW monsoon onset by "
            "1–3 weeks. Overall seasonal total may be adequate but the delayed onset "
            "causes agricultural stress in Kharif-dependent regions."
        ),
        severity       = "medium",
        checkable      = True,
        weight         = 0.65,
        synthesis_sources = ["gopal-ch11-rain-forecasting-engine"],
        notes          = (
            "Rank 3 of 4 in the Rahu Transit Veto. Leo is the natural 5th house "
            "(speculation, heat) — Rahu amplifies the fire element. Monitor SW "
            "monsoon onset date vs. IMD climatological average (June 1 Kerala) "
            "during Rahu-Leo transit years."
        ),
    ),

    # T-04 — Rahu Capricorn Moderate Alert
    _rule(
        rule_id        = "mundane-gopal-ch11-rains-rahu-capricorn-moderate",
        sub_type       = "rainfall_forecast",
        title          = "Rahu Transit Capricorn — NE Monsoon / Himalayan Watershed Stress",
        source_chapter = "Gopal Ch 11 — Rahu Transit Veto",
        condition      = (
            "IF Rahu is transiting Capricorn (Makara)"
        ),
        result         = (
            "MODERATE RAINFALL ALERT: Capricorn is a fixed earth sign. Rahu's "
            "transit here creates cold disruption of the NE monsoon and stress on "
            "Himalayan watersheds. River flow in the Gangetic plain may reduce "
            "during the winter season. Snowfall patterns in J&K and Himachal may "
            "be erratic."
        ),
        severity       = "medium",
        checkable      = True,
        weight         = 0.60,
        synthesis_sources = ["gopal-ch11-rain-forecasting-engine"],
        notes          = (
            "Rank 4 of 4 in the Rahu Transit Veto. Capricorn is Saturn's own sign — "
            "Rahu + Saturn energy combines to produce cold/dry disruption. "
            "Most relevant for North India winter crop (Rabi) and Himalayan hydrology."
        ),
    ),

    # T-05 — Rahu Scorpio/Taurus + Saturn Bhukti = Critical SW Monsoon Failure
    _rule(
        rule_id        = "mundane-gopal-ch11-rains-rahu-saturn-bhukti-monsoon-failure",
        sub_type       = "rainfall_forecast",
        title          = "Rahu in Taurus/Scorpio + Saturn Bhukti — Critical SW Monsoon Failure Gate",
        source_chapter = "Gopal Ch 11 — Rahu Transit Veto (Amplifier Rule)",
        condition      = (
            "IF Rahu is transiting Taurus OR Scorpio "
            "AND the current India National Dasha/Bhukti lord is Saturn"
        ),
        result         = (
            "CRITICAL RAINFALL ALERT — ELEVATED: Saturn is the amplifier of "
            "Rahu's disruptive effect on the water cycle. When both conditions "
            "converge, the probability of a severe South-West Monsoon failure "
            "rises to near-certain. This is the compound gate described by "
            "Gopalakrishnan as the signature of Pan-India drought years. "
            "Activate all four drought classification monitors: meteorological, "
            "hydrological, and agricultural stress protocols simultaneously."
        ),
        severity       = "critical",
        checkable      = True,
        weight         = 1.0,
        synthesis_sources = ["gopal-ch11-rain-forecasting-engine"],
        notes          = (
            "This compound rule combines Rahu Transit Veto (T-01 or T-02) with "
            "the Saturn Bhukti amplifier. India's national Dasha sequence must be "
            "computed from the Independence chart (Aug 15, 1947). "
            "Do not apply to charts other than the India Independence horoscope."
        ),
    ),

    # T-06 — Tajika 4th House Watery = Positive Rainfall
    _rule(
        rule_id        = "mundane-gopal-ch11-rains-tajika-4th-watery-positive",
        sub_type       = "rainfall_forecast",
        title          = "Tajika Ingress 4th House Watery — Positive Seasonal Rainfall Forecast",
        source_chapter = "Gopal Ch 11 — Tajika / Monthly Ingress Technique (Technique 3)",
        condition      = (
            "IF in the Sun ingress chart (Gemini for SW monsoon, Libra for NE monsoon) "
            "the 4th house contains Moon OR Venus, "
            "OR the 4th lord is placed in a watery sign (Cancer, Scorpio, or Pisces), "
            "OR an unafflicted Jupiter aspects the 4th house by trine or conjunction"
        ),
        result         = (
            "POSITIVE RAINFALL FORECAST: The 4th house is the house of moisture, "
            "agricultural land, and groundwater in mundane charts. Watery planets "
            "or watery lord placement confirms adequate seasonal rainfall. "
            "Jupiter's aspect adds the 'blessing of timely distribution' — rains "
            "arrive when crops need them. Expected result: normal to above-normal "
            "precipitation for that monsoon window."
        ),
        severity       = "low",
        checkable      = True,
        weight         = 0.80,
        synthesis_sources = ["gopal-ch11-rain-forecasting-engine"],
        notes          = (
            "Cast ingress chart for New Delhi (national capital) for Indian forecasts. "
            "Check Moon and Venus — both are watery planets in Vedic meteorology. "
            "Jupiter's unafflicted aspect overrides minor malefic placements in 4th. "
            "Convergence with Gaur Ch5 'Rohini Sea Residence' in same season = "
            "high-confidence good monsoon signal."
        ),
    ),

    # T-07 — Prasna Marga Rainfall Balance Negative
    _rule(
        rule_id        = "mundane-gopal-ch11-rains-prasna-balance-negative",
        sub_type       = "rainfall_forecast",
        title          = "Prasna Marga Rainfall Balance — Evaporation Exceeds Precipitation Gate",
        source_chapter = "Gopal Ch 11 — Economic Analogy Technique (Technique 4, Prasna Marga)",
        condition      = (
            "IF in the Sun ingress chart (SW or NE monsoon onset) "
            "the malefic strength in the 12th house (Evaporation/Loss/Expense) "
            "exceeds the benefic strength in the 2nd house (Rain Income/Cloud formation capacity)"
        ),
        result         = (
            "NEGATIVE RAINFALL BALANCE: Following Prasna Marga's income-vs-expense "
            "economic analogy, when the 'expense' of evaporation and moisture loss "
            "exceeds the 'income' of cloud formation, the seasonal rainfall budget "
            "is in deficit. Result: below-normal total precipitation even if rains "
            "arrive on schedule. The deficit is not necessarily a drought — it means "
            "rains will fail to meet crop and reservoir demand by end of season."
        ),
        severity       = "medium",
        checkable      = True,
        weight         = 0.70,
        synthesis_sources = ["gopal-ch11-rain-forecasting-engine"],
        notes          = (
            "Strength comparison uses natural benefic/malefic classification: "
            "Benefics = Jupiter, Venus, unafflicted Mercury, waxing Moon. "
            "Malefics = Saturn, Mars, Rahu, Ketu, Sun, afflicted Mercury. "
            "A 12th house with Saturn + Rahu vs a 2nd house with Mercury alone = "
            "strongly negative balance. Apply as a modifier to Rahu Transit Veto "
            "rules — convergence of both elevates severity."
        ),
    ),

    # T-08 — Agricultural Stress (Mars 4th + 12th Lord in 1st)
    _rule(
        rule_id        = "mundane-gopal-ch11-rains-mars-4th-agri-stress",
        sub_type       = "rainfall_forecast",
        title          = "Mars in 4th of Ingress + 12th Lord in 1st — Agricultural Stress & Famine Alert",
        source_chapter = "Gopal Ch 11 — Tajika Ingress Chart Diagnostics (Agricultural Stress Trigger)",
        condition      = (
            "IF in the Sun ingress chart (SW or NE monsoon onset) "
            "Mars is placed in the 4th house "
            "AND the 12th lord is placed in the 1st house"
        ),
        result         = (
            "SOCIO-ECONOMIC ALERT: Mars in the 4th house burns agricultural land "
            "and groundwater reserves — the 4th house signifies soil moisture and "
            "crop fields in mundane charts. The 12th lord in the 1st house brings "
            "'loss to the nation's body' — expenses and losses affect the national "
            "identity and visible prosperity. Combined: significant crop stress is "
            "likely for the season; in years with Rahu veto convergence, this "
            "elevates to famine-like conditions in rain-dependent agrarian states."
        ),
        severity       = "high",
        checkable      = True,
        weight         = 0.85,
        synthesis_sources = ["gopal-ch11-rain-forecasting-engine"],
        notes          = (
            "Mars in 4th is a standalone malefic signal for the land. The additional "
            "condition (12th lord in 1st) confirms the loss manifests publicly. "
            "This trigger is most dangerous when Rahu is simultaneously in Taurus "
            "or Scorpio — the three-factor convergence (Rahu veto + Mars 4th + "
            "12th lord in 1st) was the signature of the 2002 drought's agricultural "
            "impact on Bihar, UP, and Rajasthan."
        ),
    ),
]

RULES = GROUP_T


async def run() -> None:
    mongo_url = MONGO_URL
    import os
    if os.environ.get("MONGO_URL"):
        mongo_url = os.environ["MONGO_URL"]

    client = AsyncIOMotorClient(mongo_url)
    col    = client[DB_NAME]["interpretation_rules"]

    inserted = updated = 0
    for r in RULES:
        if DRY_RUN:
            print(f"  DRY  {r['rule_id']}")
            continue
        result = await col.update_one(
            {"rule_id": r["rule_id"]},
            {"$set":    r},
            upsert=True,
        )
        if result.upserted_id:
            print(f"  INS  {r['rule_id']}")
            inserted += 1
        else:
            print(f"  UPD  {r['rule_id']}")
            updated += 1

    if DRY_RUN:
        print(f"\nDRY RUN complete — {len(RULES)} rule(s) would be upserted")
    else:
        print(f"\nInserted {inserted} / Updated {updated} rules → {DB_NAME}.interpretation_rules")

    client.close()


if __name__ == "__main__":
    asyncio.run(run())
