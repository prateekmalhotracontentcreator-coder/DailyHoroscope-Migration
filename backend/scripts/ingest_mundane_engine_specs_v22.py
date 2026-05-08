#!/usr/bin/env python3
"""
ingest_mundane_engine_specs_v22.py

Engine spec for Gopal Chapter 12 — Why India is What it is
Batch: mundane-engine-v22-20260508

1 spec:
  gopal-ch12-india-native-profile-engine
    India's foundational "Native Profile" based on the Independence chart
    (Aug 15, 1947, 12:01 AM, New Delhi — Taurus Lagna). Covers national
    psyche markers, regional economic weights, structural governance flaws,
    neighbor-friction framework, wealth architecture, and sector destiny.

    Functions as a LOOKUP TABLE for India-specific query routing:
    any mundane engine query tagged india_context=True is cross-referenced
    against this profile before returning a forecast.

Usage:
  # Dry run (default):
  python3 backend/scripts/ingest_mundane_engine_specs_v22.py

  # Live upload:
  python3 -c "
  import asyncio, os
  exec(open('backend/scripts/ingest_mundane_engine_specs_v22.py').read().replace('DRY_RUN   = True', 'DRY_RUN   = False'))
  asyncio.run(run())
  "
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME   = "horoscope_db"
BATCH_ID  = "mundane-engine-v22-20260508"
DRY_RUN   = True

NOW = datetime.now(timezone.utc).isoformat()

SPECS = [
    {
        "spec_id":    "gopal-ch12-india-native-profile-engine",
        "batch_id":   BATCH_ID,
        "source":     "Gopalakrishnan — Mundane Astrology, Chapter 12: Why India is What it is",
        "scope":      "india_national_profile",
        "created_at": NOW,
        "updated_at": NOW,

        "engine_role": (
            "FOUNDATIONAL LOOKUP TABLE for India-specific query routing. "
            "Any mundane engine forecast tagged india_context=True is cross-referenced "
            "against this profile before returning a result. The profile is derived "
            "from the India Independence chart (Aug 15, 1947, 12:01 AM, New Delhi) "
            "and reflects structural planetary placements — not transits."
        ),

        # ── Independence Chart Foundation ─────────────────────────────────
        "india_independence_chart": {
            "date":           "15 August 1947",
            "time":           "12:01 AM IST",
            "location":       "New Delhi (28.6°N, 77.2°E)",
            "lagna":          "Taurus (Rishabha)",
            "lagna_lord":     "Venus",
            "lagna_note":     "Fixed earth sign — provides national stability, agricultural identity, conservative value system.",
            "key_placements": {
                "rahu_in_lagna": (
                    "Rahu conjoins the Lagna → national psyche oriented toward "
                    "foreign culture, imitation of the West, 'pseudo-secularism'."
                ),
                "venus_moon_conjunction": (
                    "Venus (Lagna lord) and Moon (3rd lord) are combined → "
                    "national obsession with communication-based sports, particularly cricket."
                ),
                "jupiter_in_6th": (
                    "Jupiter (Dharma planet) placed in the 6th house (Service/Debt/Litigation) → "
                    "merit is bypassed by the system; judiciary is slow or corrupted; "
                    "traditional priestly/intellectual class displaced through caste-reservation politics."
                ),
                "mercury_venus_in_3rd": (
                    "Mercury and Venus cluster in the 3rd house (Communication/Neighbors) → "
                    "India is destined to lead in knowledge-based services and back-office processing; "
                    "also signals a strong voice in South Asian neighborhood diplomacy."
                ),
                "saturn_as_10th_lord": (
                    "Saturn rules the 10th house (Authority/Government/Industry) → "
                    "heavy industry and manufacturing form the backbone of western India "
                    "(Gujarat/Maharashtra), and national governance trends toward slow, "
                    "bureaucratic authority structures."
                ),
                "mars_7th_lord_in_2nd": (
                    "Mars (7th lord — Foreign Relations/War) placed in the 2nd house (Wealth) → "
                    "India's wealth and revenue are structurally tied to international trade, "
                    "foreign partnerships, and defense spending."
                ),
            },
        },

        # ── National Psyche Markers ────────────────────────────────────────
        "national_psyche_markers": {
            "lagna_profile": (
                "Taurus Lagna — patient, stable, agriculturally rooted, conservative, "
                "resistant to rapid change. The nation's fundamental character is one of "
                "endurance and accumulation rather than aggressive expansion."
            ),
            "sports_obsession": {
                "trigger": "Venus (Lagna lord) + Moon (3rd lord) combined",
                "mechanism": (
                    "3rd house governs sports, communication, and short-distance travel. "
                    "Its lord (Moon) conjoining the Lagna lord (Venus) creates a mass-level "
                    "emotional identification with competitive sports."
                ),
                "result": "Cricket is the national obsession; any cricket outcome has socio-economic ripple effects.",
            },
            "western_imitation_tendency": {
                "trigger": "Rahu in Lagna",
                "mechanism": (
                    "Rahu amplifies the desire for what is foreign or out of reach. "
                    "In the Lagna, this makes the national identity itself oriented toward "
                    "external validation and mimicry of Western systems."
                ),
                "result": "India consistently adopts Western frameworks (legal, academic, economic) over indigenous ones.",
            },
        },

        # ── Regional Economic Weights ──────────────────────────────────────
        "regional_economic_weights": {
            "south_india_it_boom": {
                "astrological_marker": "Cancer (Kataka) — 3rd house from Taurus Lagna; direction = South",
                "planetary_backing":   "Mercury + Venus cluster in 3rd house",
                "sector":              "Information Technology, BPO, Knowledge Services",
                "geography":           "Tamil Nadu, Karnataka, Telangana, Kerala, Andhra Pradesh",
                "weight":              "+0.50 for all India IT/BPO growth queries",
                "result": (
                    "India is structurally destined to remain the global backbone of "
                    "back-office processing and IT services. This is not a temporary trend "
                    "but a natal promise of the Independence chart."
                ),
                "transit_trigger": (
                    "Whenever Saturn or Jupiter transits Cancer or the 3rd house of India, "
                    "the IT/BPO sector experiences a significant surge or structural shift."
                ),
            },
            "west_india_industrial_giants": {
                "astrological_marker": "Saturn as 10th lord; direction = West",
                "sector":              "Heavy Industry, Manufacturing, Petrochemicals, Banking",
                "geography":           "Gujarat (Ahmedabad, Surat), Maharashtra (Mumbai, Pune)",
                "result": (
                    "The largest Indian conglomerates (industrial, petrochemical, banking) "
                    "are structurally anchored in western India. Saturn as 10th lord gives "
                    "these sectors longevity and resilience but also slowness."
                ),
            },
            "east_india_services_bpo": {
                "astrological_marker": "Mercury + Venus in 3rd house; direction = East",
                "sector":              "Skill-based services, BPO, neighborhood diplomacy",
                "geography":           "West Bengal, Bihar, Odisha",
                "result": (
                    "Strong voice in South Asian neighborhood relations and emerging "
                    "skill-based service sector presence. However, Mercury-Venus in "
                    "the 3rd also indicates the East struggles with political instability "
                    "(3rd = short-duration, unstable partnerships)."
                ),
            },
        },

        # ── Structural Governance Flaws ────────────────────────────────────
        "structural_governance_flaws": {
            "judicial_corruption_marker": {
                "placement": "Jupiter in the 6th house of the Independence chart",
                "mechanism": (
                    "Jupiter = Dharma, justice, wisdom. In the 6th house (conflict, litigation, "
                    "service, debt), Jupiter's dharmic quality is deployed in a house of friction. "
                    "Result: the judiciary is active but slow; merit is frequently bypassed "
                    "by political influence and seniority."
                ),
                "secondary_effect": (
                    "The traditional intellectual/priestly class (represented by Jupiter) is "
                    "structurally displaced through caste-based reservation politics — a "
                    "persistent national tension."
                ),
            },
            "bureaucratic_inertia": {
                "placement": "Saturn as 10th lord",
                "mechanism": (
                    "Saturn governs governance structures, discipline, and hierarchies. "
                    "As 10th lord, it ensures institutions are built to last but also "
                    "makes them resistant to rapid reform."
                ),
                "result": "Structural reforms in government take disproportionately long.",
            },
        },

        # ── Neighbor Friction Framework ────────────────────────────────────
        "neighbor_friction_framework": {
            "pakistan_2_12_veto": {
                "india_lagna":    "Taurus (Rishabha)",
                "pakistan_lagna": "Aries (Mesha) — 12th sign from Taurus",
                "relationship":   "12th house from India = Pakistan (Loss/Isolation/Hidden Enemies)",
                "alternative":    "If Pakistan Lagna is Gemini, it is 2nd from Taurus = neighbor in permanent financial/resource competition",
                "geometric_law": (
                    "The 2/12 Lagna relationship between neighboring nations creates "
                    "irreconcilable structural tension. The 12th house signifies loss, "
                    "foreign enemies, and expenditure — Pakistan literally occupies India's "
                    "house of loss in the zodiacal geometry."
                ),
                "result": (
                    "PERMANENT FRICTION: Lasting peace between India and Pakistan is "
                    "astrologically impossible under this geometric law. Any peace accord "
                    "will be temporary and will break down at the next Saturn transit "
                    "over the Taurus-Scorpio axis or Aries-Libra axis."
                ),
                "forecast_rule": (
                    "All India-Pakistan relations queries must return a base-level "
                    "'Structural Friction Warning' before any transit analysis."
                ),
            },
            "general_neighbor_logic": (
                "Nations whose Lagna is 6th, 8th, or 12th from India's Taurus Lagna "
                "are structurally adversarial. Nations whose Lagna is 1st, 4th, 5th, "
                "7th, 9th, or 11th are potentially cooperative but not unconflicted."
            ),
        },

        # ── Wealth Architecture ────────────────────────────────────────────
        "wealth_architecture": {
            "2nd_lord": "Mercury — governs domestic wealth, trade, and financial communication",
            "7th_lord": "Mars — placed in the 2nd house",
            "mechanism": (
                "Mars (7th lord = foreign relations, partnerships, and war) placed in the "
                "2nd house (national wealth) creates a permanent linkage: India's prosperity "
                "is tied to international trade, defense expenditure, and foreign partnerships. "
                "When India's foreign relations are strong, the 2nd house (wealth) benefits. "
                "When foreign relations are strained, the 2nd house suffers."
            ),
            "forecast_application": (
                "For any India economic forecast: cross-reference the state of the 7th lord "
                "(Mars) by transit or Dasha before projecting national wealth trends. "
                "A Mars-afflicted period (e.g., Mars Dasha + malefic transit) = economic "
                "strain despite domestic activity."
            ),
        },
    }
]


async def run() -> None:
    mongo_url = MONGO_URL
    import os
    if os.environ.get("MONGO_URL"):
        mongo_url = os.environ["MONGO_URL"]

    client = AsyncIOMotorClient(mongo_url)
    col    = client[DB_NAME]["mundane_engine_specs"]

    inserted = updated = 0
    for spec in SPECS:
        if DRY_RUN:
            print(f"  DRY  {spec['spec_id']}")
            continue
        result = await col.update_one(
            {"spec_id": spec["spec_id"]},
            {"$set":    spec},
            upsert=True,
        )
        if result.upserted_id:
            print(f"  INS  {spec['spec_id']}")
            inserted += 1
        else:
            print(f"  UPD  {spec['spec_id']}")
            updated += 1

    if DRY_RUN:
        print(f"\nDRY RUN complete — {len(SPECS)} spec(s) would be upserted")
    else:
        print(f"\nInserted {inserted} / Updated {updated} specs → {DB_NAME}.mundane_engine_specs")

    client.close()


if __name__ == "__main__":
    asyncio.run(run())
