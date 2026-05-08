#!/usr/bin/env python3
"""
ingest_mundane_interpretation_v22.py

Interpretation rules for Gopal Chapter 12 — Why India is What it is
Batch: mundane-interp-v22-20260508
Group U — India Native Profile (7 rules)

These are structural rules derived from fixed planetary placements in the
India Independence chart (Aug 15, 1947, Taurus Lagna). Unlike transit-based
rules, most are evergreen conditions — they apply to every India forecast
unless a specific transit actively overrides them.

Usage:
  # Dry run (default):
  python3 backend/scripts/ingest_mundane_interpretation_v22.py

  # Live upload:
  python3 -c "
  import asyncio, os
  exec(open('backend/scripts/ingest_mundane_interpretation_v22.py').read().replace('DRY_RUN   = True', 'DRY_RUN   = False'))
  asyncio.run(run())
  "
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME   = "horoscope_db"
BATCH_ID  = "mundane-interp-v22-20260508"
DRY_RUN   = True

NOW = datetime.now(timezone.utc).isoformat()


def _rule(
    rule_id:           str,
    sub_type:          str,
    title:             str,
    source_chapter:    str,
    condition:         str,
    result:            str,
    severity:          str,
    checkable:         bool,
    synthesis_sources: list[str],
    notes:             str,
    weight:            float = 1.0,
) -> dict:
    return {
        "rule_id":           rule_id,
        "batch_id":          BATCH_ID,
        "science_id":        "mundane_jyotish",
        "sub_type":          sub_type,
        "title":             title,
        "source_chapter":    source_chapter,
        "source":            {
            "book":    "Mundane Astrology by Gopalakrishnan",
            "chapter": source_chapter,
        },
        "condition":         condition,
        "result":            result,
        "severity":          severity,
        "weight":            weight,
        "checkable":         checkable,
        "synthesis_sources": synthesis_sources,
        "notes":             notes,
        "approval_status":   "pending_review",
        "created_at":        NOW,
        "updated_at":        NOW,
    }


# ── GROUP U — India Native Profile (Gopal Ch12) ───────────────────────────────

GROUP_U = [

    # U-01 — Rahu in Lagna → Western Imitation (Structural / Evergreen)
    _rule(
        rule_id        = "mundane-gopal-ch12-india-rahu-lagna-western-imitation",
        sub_type       = "india_national_profile",
        title          = "India Rahu in Lagna — Structural Western Imitation Tendency",
        source_chapter = "Gopal Ch 12 — India Native Profile (National Psyche Markers)",
        condition      = (
            "IF the query context is India AND the reference chart is the "
            "Independence chart (Aug 15, 1947, Taurus Lagna) "
            "AND Rahu is natally placed in the Lagna"
        ),
        result         = (
            "STRUCTURAL NATIONAL TRAIT — EVERGREEN: Rahu in the Lagna of India's "
            "Independence chart creates a permanent national psyche oriented toward "
            "foreign cultures, Western systems, and external validation. "
            "India consistently adopts foreign frameworks (legal, academic, economic, "
            "technological) over indigenous ones — not due to rational choice but due "
            "to a structural natal imprint. This is described as 'pseudo-secularism' "
            "by Gopalakrishnan: the tendency to privilege Western-style secularism "
            "over India's own pluralistic traditions. "
            "This trait does not change with transits — it is a permanent national character marker."
        ),
        severity       = "medium",
        checkable      = False,
        weight         = 0.70,
        synthesis_sources = ["gopal-ch12-india-native-profile-engine"],
        notes          = (
            "Structural rule — applies to every India-context forecast as a base modifier. "
            "Rahu's transit through the Lagna by progression does not change this; the natal "
            "placement is permanent. Use as a background modifier when forecasting India's "
            "response to global trends: default assumption is India will follow rather than lead."
        ),
    ),

    # U-02 — Venus + Moon → Cricket/Sports National Obsession (Structural)
    _rule(
        rule_id        = "mundane-gopal-ch12-india-venus-moon-sports-obsession",
        sub_type       = "india_national_profile",
        title          = "India Venus + Moon Conjunction — National Sports Obsession (Cricket)",
        source_chapter = "Gopal Ch 12 — India Native Profile (National Psyche Markers)",
        condition      = (
            "IF the query context is India AND the reference chart is the "
            "Independence chart (Aug 15, 1947, Taurus Lagna) "
            "AND Venus (Lagna lord) and Moon (3rd lord) are natally combined"
        ),
        result         = (
            "STRUCTURAL NATIONAL TRAIT — EVERGREEN: The conjunction of Venus "
            "(Lagna lord = national identity) and Moon (3rd lord = communication, "
            "sports, competitive activities) creates a mass-level emotional identification "
            "with competitive sports. Cricket is the primary manifestation. "
            "Any major cricket outcome — India victory or defeat — triggers "
            "measurable socio-economic ripple effects: market sentiment, retail sales, "
            "public mood. This also implies that sports predictions for India have "
            "outsized national consequence compared to other countries."
        ),
        severity       = "low",
        checkable      = False,
        weight         = 0.60,
        synthesis_sources = ["gopal-ch12-india-native-profile-engine"],
        notes          = (
            "Combined with the v20 Ch10 Sports rules (mundane-interp-v20 batch), "
            "this rule provides the India-specific background weight for cricket match "
            "predictions. A sport prediction for India carries +0.20 national significance "
            "modifier vs the same prediction for another country."
        ),
    ),

    # U-03 — Jupiter in 6th → Judicial Corruption (Structural)
    _rule(
        rule_id        = "mundane-gopal-ch12-india-jupiter-6th-judicial-corruption",
        sub_type       = "india_national_profile",
        title          = "India Jupiter in 6th — Structural Judicial Corruption & Merit Bypass",
        source_chapter = "Gopal Ch 12 — India Native Profile (Structural Governance Flaws)",
        condition      = (
            "IF the query context is India governance, judiciary, or merit-based institutions "
            "AND the reference chart is the Independence chart (Aug 15, 1947, Taurus Lagna) "
            "AND Jupiter is natally in the 6th house"
        ),
        result         = (
            "STRUCTURAL GOVERNANCE FLAW — EVERGREEN: Jupiter (planet of Dharma, wisdom, "
            "and justice) placed in the 6th house (service, debt, conflict, litigation) "
            "creates a permanent structural tension in India's judiciary and merit systems. "
            "Merit is consistently bypassed in favor of political influence, seniority, "
            "and reservation quotas. The judicial system is active but slow — Jupiter "
            "ensures justice eventually arrives but the 6th house delays it through "
            "procedural conflict. Additionally, the traditional intellectual/priestly "
            "class is structurally displaced through caste-based reservation politics — "
            "a recurrent national tension that cannot be resolved through transit-level "
            "interventions alone."
        ),
        severity       = "medium",
        checkable      = False,
        weight         = 0.75,
        synthesis_sources = ["gopal-ch12-india-native-profile-engine"],
        notes          = (
            "This is a structural diagnostic — use it when forecasting outcomes of "
            "judicial reforms, anti-corruption drives, or meritocracy debates in India. "
            "The base forecast is: reform efforts will face systemic resistance and "
            "take longer than expected. Jupiter Dasha periods for India may bring "
            "temporary judicial improvements but the structural problem persists."
        ),
    ),

    # U-04 — Cancer Transits → South India IT Impact
    _rule(
        rule_id        = "mundane-gopal-ch12-india-cancer-transit-south-it",
        sub_type       = "india_national_profile",
        title          = "Cancer Sign Transits — South India IT Sector Economic Impact",
        source_chapter = "Gopal Ch 12 — Regional Economic Weights (South India IT Boom)",
        condition      = (
            "IF a major planet (Saturn, Jupiter, or Rahu/Ketu) transits Cancer (Kataka) "
            "AND the query context is India's IT, BPO, or knowledge-services sector"
        ),
        result         = (
            "REGIONAL SECTOR ALERT: Cancer is the 3rd house from India's Taurus Lagna "
            "and is associated with the southern direction. The planetary cluster in "
            "India's natal 3rd house (Mercury + Venus) creates a permanent IT/BPO "
            "destiny for southern India (Karnataka, Tamil Nadu, Telangana, Andhra, Kerala). "
            "When a major planet transits Cancer: "
            "Saturn transit Cancer → Structural stress/contraction in South India IT (slowdown, "
            "layoffs, regulatory burden). "
            "Jupiter transit Cancer → Expansion, hiring surge, new sector emergence in South IT. "
            "Rahu transit Cancer → Disruptive innovation, foreign-investment surge, outsourcing boom. "
            "Ketu transit Cancer → Withdrawal, cost-cutting, automation-driven displacement."
        ),
        severity       = "medium",
        checkable      = True,
        weight         = 0.80,
        synthesis_sources = ["gopal-ch12-india-native-profile-engine"],
        notes          = (
            "Checkable: verify against India IT sector performance during historical Cancer transits. "
            "Saturn in Cancer (2003-2005): India IT/BPO boom despite initial caution. "
            "Jupiter in Cancer (2014-2015): Start-up ecosystem surge, Modi wave economic confidence. "
            "Rahu in Cancer (2017-2019): Fintech explosion, digital India push, record FDI in IT."
        ),
    ),

    # U-05 — Pakistan 2/12 Permanent Friction Veto
    _rule(
        rule_id        = "mundane-gopal-ch12-india-pakistan-2-12-friction-veto",
        sub_type       = "india_national_profile",
        title          = "India-Pakistan 2/12 Lagna Veto — Permanent Structural Friction Gate",
        source_chapter = "Gopal Ch 12 — Neighbor Friction Framework (2/12 Lagna Veto)",
        condition      = (
            "IF the query context is India-Pakistan relations, "
            "peace negotiations, or bilateral trade agreements"
        ),
        result         = (
            "STRUCTURAL WARNING — PERMANENT: Pakistan's Lagna (Aries/Mesha) is the "
            "12th sign from India's Lagna (Taurus/Rishabha). The 12th house represents "
            "loss, foreign enemies, hidden adversaries, and expenditure in mundane charts. "
            "Pakistan literally occupies India's house of loss in zodiacal geometry. "
            "This is a GEOMETRIC LAW — it applies regardless of current transit conditions. "
            "Any peace accord or normalization attempt will be temporary: structural "
            "friction will reassert itself at the next Saturn or Rahu transit over the "
            "Taurus-Scorpio or Aries-Libra axis. "
            "Forecast baseline for all India-Pakistan queries: 'Structural Friction — "
            "Temporary improvements possible, lasting peace astrologically impossible.' "
            "Override requires both nations to simultaneously run a Jupiter-governed Dasha."
        ),
        severity       = "high",
        checkable      = True,
        weight         = 1.0,
        synthesis_sources = ["gopal-ch12-india-native-profile-engine"],
        notes          = (
            "Checkable: every India-Pakistan peace initiative since 1947 has broken down. "
            "Validated instances: 1966 Tashkent (failed after Shastri death), 1972 Simla "
            "(partial implementation), 1999 Lahore (Kargil war within months), 2015 "
            "Modi Lahore visit (followed by Pathankot attack). "
            "The 2/12 veto is the strongest structural constraint in India's mundane chart."
        ),
    ),

    # U-06 — India BPO/IT Natal Destiny (Structural / 3rd House)
    _rule(
        rule_id        = "mundane-gopal-ch12-india-bpo-destiny-3rd-house",
        sub_type       = "india_national_profile",
        title          = "India 3rd House Cluster — BPO/IT Global Backbone Destiny",
        source_chapter = "Gopal Ch 12 — Regional Economic Weights (BPO Destiny Modifier)",
        condition      = (
            "IF the query context is India's long-term economic trajectory, "
            "global competitiveness, or knowledge-economy forecasts"
        ),
        result         = (
            "STRUCTURAL DESTINY — EVERGREEN: The cluster of Mercury (communication, "
            "trade, data) and Venus (services, aesthetics, relational skills) in the "
            "3rd house of India's Independence chart creates a natal promise: India is "
            "structurally destined to remain the global backbone of IT, BPO, and "
            "back-office processing. This is not a temporary trend driven by cost "
            "arbitrage — it is a planetary mandate. "
            "Forecast modifier: +0.50 positive weight for all India IT/BPO/knowledge "
            "economy growth queries. Even in periods of global IT downturn, India's "
            "share of global outsourcing will remain disproportionately high. "
            "The 3rd house also governs neighbors and short-distance connectivity — "
            "India's geographic and cultural proximity to the English-speaking world "
            "is a structural advantage, not a coincidence."
        ),
        severity       = "low",
        checkable      = False,
        weight         = 0.85,
        synthesis_sources = ["gopal-ch12-india-native-profile-engine"],
        notes          = (
            "This rule applies a permanent positive modifier to India IT/BPO forecasts. "
            "It does NOT override short-term negative transit signals (e.g., Saturn in "
            "Cancer → sector stress), but it sets the recovery trajectory: even after "
            "a bad transit, the sector returns to structural dominance. "
            "Cross-reference with Ch11's Dhana Chakra moisture score — an India with "
            "good rainfall + strong 3rd house = national confidence and IT-sector hiring."
        ),
    ),

    # U-07 — India Wealth-Foreign Trade Linkage (Mars 7th lord in 2nd)
    _rule(
        rule_id        = "mundane-gopal-ch12-india-mars-7th-2nd-wealth-trade",
        sub_type       = "india_national_profile",
        title          = "India Mars (7th Lord) in 2nd — Wealth Tied to Foreign Trade & Defense",
        source_chapter = "Gopal Ch 12 — Wealth Architecture (Mars 7th Lord in 2nd House)",
        condition      = (
            "IF the query context is India's national economic performance, "
            "trade balance, defense budget, or foreign investment climate"
        ),
        result         = (
            "STRUCTURAL WEALTH LOGIC — EVERGREEN: Mars (7th lord = Foreign Relations, "
            "War, Partnerships) is placed in India's 2nd house (National Wealth, Revenue, "
            "Resources). This creates a permanent structural linkage: India's prosperity "
            "is tied to the health of its foreign relationships. "
            "When foreign relations are strong → 2nd house (wealth) benefits: FDI inflows, "
            "export growth, defense cooperation dividends. "
            "When foreign relations are strained → 2nd house (wealth) suffers: capital "
            "outflows, trade disruptions, defense expenditure drag. "
            "Forecast application: for India economic outlook queries, always audit "
            "the state of Mars by transit or Dasha BEFORE projecting national wealth trends. "
            "Mars-afflicted periods (Mars Retrograde, Mars in debilitation in Cancer, or "
            "Mars Dasha with malefic aspects) = economic strain despite domestic activity."
        ),
        severity       = "medium",
        checkable      = True,
        weight         = 0.75,
        synthesis_sources = ["gopal-ch12-india-native-profile-engine"],
        notes          = (
            "Checkable: India's worst economic periods correlate with foreign relations crises. "
            "1971 (Bangladesh war → economic strain), 1991 (Gulf War + BoP crisis → IMF bailout), "
            "2016 (demonetization + US election uncertainty → FDI hesitancy). "
            "Conversely, India's best growth decades (2003–2008, 2014–2019) coincided with "
            "strong foreign investment climate and active diplomatic outreach."
        ),
    ),
]

RULES = GROUP_U


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
