"""
ingest_mundane_engine_specs_v20.py
=====================================
Batch:      mundane-engine-v20-20260508
Collection: mundane_engine_specs
Science:    mundane_jyotish
Source:     Gopalakrishnan Ch 10 — Predicting Sports Events

SCOPE — WHAT IS NEW vs v7
--------------------------
v7 already ingested the NATAL/CAREER side of Gopal Ch10:
  - gopal-ch10-sports-career-indicators  (Saturn 8th rule + Mars perigee)
  - interpretation rules: saturn-8th-dasa-lord-career-fall, mars-perigee-leadership-change

v20 adds the MATCH PREDICTION side — fully distinct content:
  - Dual-Team Matrix engine (1st/7th house framework, 10th/4th lord comparison)
  - Cricket event-to-house mapping (granular in-match event routing)
  - Tennis + Football event-to-house mapping
  - Reduced Vimshottari Timer methodology
  - Validated case studies (India vs West Indies ODIs, May 2006)

NEW SPECS (3):
  gopal-ch10-sports-dual-team-engine
  gopal-ch10-cricket-event-house-map
  gopal-ch10-tennis-football-event-house-map
"""

import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.environ.get("DB_NAME",   "horoscope_db")
_BATCH    = "mundane-engine-v20-20260508"
DRY_RUN   = True

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 1 — SPORTS DUAL-TEAM PREDICTION ENGINE
# ─────────────────────────────────────────────────────────────────────────────
SPORTS_DUAL_TEAM_ENGINE = {
    "spec_id":        "gopal-ch10-sports-dual-team-engine",
    "spec_type":      "prediction_framework",
    "science_id":     "mundane_jyotish",
    "title":          "Sports Dual-Team Prediction Engine — Gopal Ch10",
    "source":         "gopal_modern_ch10",
    "source_chapter": "Gopalakrishnan Ch 10 — Predicting Sports Events (pp.741–763)",
    "description": (
        "The foundational prediction framework for competitive sports in mundane astrology. "
        "A match chart is cast for the exact moment of match start (or toss). "
        "The 1st house represents Team A (toss winner / home team); "
        "the 7th house represents Team B (toss loser / visiting team). "
        "Victory is determined by comparing the strength of the 10th lord (Team A's "
        "victory significator) against the 4th lord (Team B's victory significator, "
        "being the 10th from the 7th). The stronger lord's team wins. "
        "A Reduced Vimshottari Dasha compresses planetary periods into the match duration "
        "to time momentum shifts within the game."
    ),

    # ── Team assignment ────────────────────────────────────────────────────────
    "team_assignment": {
        "team_a":       "Lagna / 1st House — Team winning the toss (or home team)",
        "team_b":       "7th House — Team losing the toss (or visiting team)",
        "pre_toss_rule": (
            "If prediction is requested before the toss: output "
            "'Awaiting Toss — outcome depends on 1st/7th house assignment. "
            "Re-run after toss is known.' Do not generate a winner prediction "
            "without toss information."
        ),
    },

    # ── Victory determination logic ────────────────────────────────────────────
    "victory_logic": {
        "team_a_win":   "IF 10th lord from Lagna is stronger than 4th lord THEN Team A wins",
        "team_b_win":   "IF 4th lord (= 10th from 7th) is stronger than 10th lord THEN Team B wins",
        "strength_triage": [
            "Check from Lagna, Chandra Lagna, and Karkamsha Lagna",
            "Exaltation > Own sign > Friendly sign > Neutral > Debilitation",
            "Retrograde planet: downgrade strength by one level",
            "Combust planet: treat as severely weakened",
            "Trikona placement (1st/5th/9th) adds strength weight",
        ],
        "tiebreaker": (
            "If 10th lord and 4th lord are equal strength: "
            "check if 8th lord is in a Dual sign (Gemini/Virgo/Sagittarius/Pisces). "
            "If yes → extremely close finish, result decided in final overs/moments."
        ),
    },

    # ── Captain's Lagna Filter ─────────────────────────────────────────────────
    "captain_lagna_filter": {
        "rule": (
            "Per the 9th house logic (Captains / Umpires): if the Captain's individual "
            "natal chart is strong during the match's transits, add +0.15 to that "
            "team's victory probability weight. Check: Captain's Dasha planet strong "
            "from natal Lagna and Chandra Lagna during match window."
        ),
        "application": "Apply after base 10th/4th lord comparison as a secondary modifier",
    },

    # ── Reduced Vimshottari Dasha Timer ───────────────────────────────────────
    "reduced_vimshottari_timer": {
        "purpose": (
            "Compress the standard Vimshottari 120-year period into the duration of "
            "a single match to identify which planetary period governs each phase of play."
        ),
        "cricket_formula": (
            "Divide total overs (e.g., 50 overs) by 12 zodiac signs = ~4.17 overs per sign. "
            "The planetary ruler of each sign-segment governs that phase of the match. "
            "Malefic-ruled segment = fall of wickets / run-rate drop likely."
        ),
        "momentum_rule": (
            "IF the current 4-over sign-segment is ruled by a malefic (Saturn/Mars/Rahu/Ketu) "
            "THEN output: 'Momentum Shift Alert: high probability of wickets falling or "
            "run-rate slowing in this segment.'"
        ),
        "tennis_formula": "Divide by sets or games — malefic segment = double faults / unforced errors",
        "football_formula": "Divide 90 minutes by 12 = ~7.5 min per sign-segment",
    },

    # ── Validated case studies ─────────────────────────────────────────────────
    "validated_case_studies": [
        {
            "match":    "India vs West Indies — 1st ODI",
            "date":     "18 May 2006",
            "location": "Jamaica",
            "lagna":    "Virgo 7°30' (India = Team A / toss winner)",
            "team_a_victory_lord": {
                "planet":    "Mercury (10th lord from Virgo Lagna)",
                "placement": "9th house (Taurus) — Trikona",
                "strength":  "High — Trikona placement",
            },
            "team_b_victory_lord": {
                "planet":    "Jupiter (4th lord from Virgo Lagna)",
                "placement": "2nd house (Libra)",
                "strength":  "Moderate — Retrograde (downgraded)",
            },
            "actual_result":    "India won by 5 wickets (India 254/5 beat WI 251/6)",
            "engine_verdict":   "10th lord Mercury > 4th lord Jupiter ✅ Validated",
        },
        {
            "match":    "India vs West Indies — 3rd ODI",
            "date":     "23 May 2006",
            "location": "St. Kitts",
            "lagna":    "Virgo 11°49'",
            "team_a_victory_lord": "Mercury (10th lord) in 9th house — Trikona strength",
            "team_b_victory_lord": "Jupiter (4th lord) in 2nd house — Retrograde",
            "reduced_dasha_note": (
                "Reduced Vimshottari applied to match duration. "
                "Mercury's Trikona placement maintained dominance throughout — "
                "momentum consistently favoured India (Team A)."
            ),
            "engine_verdict": "10th lord Mercury > 4th lord Jupiter ✅ Validated",
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 2 — CRICKET EVENT-TO-HOUSE MAPPING
# ─────────────────────────────────────────────────────────────────────────────
CRICKET_EVENT_HOUSE_MAP = {
    "spec_id":        "gopal-ch10-cricket-event-house-map",
    "spec_type":      "event_house_mapping",
    "science_id":     "mundane_jyotish",
    "title":          "Cricket In-Match Event House Mapping — Gopal Ch10",
    "source":         "gopal_modern_ch10",
    "source_chapter": "Gopalakrishnan Ch 10 — Cricket House Classification (pp.741–744)",
    "description": (
        "Granular mapping of cricket match events to mundane houses. "
        "Used by the Dual-Team Engine to identify which planetary transits / "
        "Reduced Dasha periods govern specific match phases and event types. "
        "Houses are read from the match Lagna (not natal or national chart)."
    ),

    "cricket_house_map": {
        "house_1": {
            "governs": "Start of match, toss, opening batting, first 5 overs",
            "diagnostic": (
                "Strong 1st lord + benefic in Lagna = confident opening stand; "
                "malefic in Lagna = early loss of wickets in powerplay"
            ),
        },
        "house_3": {
            "governs": "Running between wickets, boundaries (4s and 6s), dressing rooms, team communication",
            "diagnostic": (
                "Afflicted 3rd lord or Mars in 3rd = running out risk and boundary drought; "
                "strong 3rd lord = aggressive stroke play and active running"
            ),
        },
        "house_5": {
            "governs": "Luck, catches, century stands, coaching staff input",
            "diagnostic": (
                "Jupiter or Venus in 5th = lucky breaks, catches held, partnership centuries; "
                "malefic in 5th = dropped catches, missed chances"
            ),
        },
        "house_6": {
            "governs": "Fall of wickets, run-outs, injuries, bad umpire decisions, team conflicts",
            "diagnostic": (
                "Mars or Rahu in 6th = high-wicket-fall period, injury risk, controversy; "
                "strong 6th lord = opponent's bowling attack effective"
            ),
        },
        "house_9": {
            "governs": "Umpires, third-umpire decisions, captain and vice-captain",
            "diagnostic": (
                "Afflicted 9th = poor officiating decisions, DRS controversy; "
                "strong 9th lord = fair officiating and captain performing well"
            ),
        },
        "house_11": {
            "governs": "Prize money, Man of the Match, crowd strength, team's collective gains",
            "diagnostic": (
                "Jupiter in 11th = Man of the Match is a team standout; "
                "malefic in 11th = crowd trouble or prize controversy"
            ),
        },
        "house_12": {
            "governs": "End of match, last over, 12th man, prize distribution, post-match ceremony",
            "diagnostic": (
                "Saturn in 12th of match chart = match drags to final over; "
                "strong 12th lord for Team B = last-over heist"
            ),
        },
    },

    "alert_combinations": {
        "match_fixing_alert": (
            "IF Mars + Rahu conjunct in 6th house of match chart THEN output: "
            "'Match Integrity Alert: High risk of controversial umpire decisions, "
            "match-fixing allegations, or disciplinary incidents.'"
        ),
        "rain_alert": (
            "IF 4th house of match chart contains Moon + Venus (watery planets) "
            "AND 4th lord is in a watery sign (Cancer/Scorpio/Pisces) THEN output: "
            "'Weather Warning: High probability of match interruption due to rain.'"
        ),
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# SPEC 3 — TENNIS + FOOTBALL EVENT-TO-HOUSE MAPPING
# ─────────────────────────────────────────────────────────────────────────────
TENNIS_FOOTBALL_HOUSE_MAP = {
    "spec_id":        "gopal-ch10-tennis-football-event-house-map",
    "spec_type":      "event_house_mapping",
    "science_id":     "mundane_jyotish",
    "title":          "Tennis and Football In-Match Event House Mapping — Gopal Ch10",
    "source":         "gopal_modern_ch10",
    "source_chapter": "Gopalakrishnan Ch 10 — Tennis / Football House Classification (pp.745–750)",
    "description": (
        "Granular mapping of tennis and football match events to mundane houses. "
        "Complements the Cricket Event House Map. Same Dual-Team Matrix (1st/7th, "
        "10th/4th lord comparison) applies across all sports — only the in-match "
        "event-to-house assignments differ by sport type."
    ),

    "tennis_house_map": {
        "house_3": {
            "governs": "Stamina, serve speed, running between nets and baselines, footwork",
            "diagnostic": (
                "Mars strong in 3rd = powerful serve and aggressive baseline play; "
                "afflicted 3rd = stamina drop in later sets"
            ),
        },
        "house_6": {
            "governs": "Double faults, unforced errors, 'just miss' shots, injury",
            "diagnostic": (
                "Mars or Saturn in 6th = double-fault clusters, unforced errors; "
                "Rahu in 6th = controversial line calls"
            ),
        },
        "house_10": {
            "governs": "Winning the match, momentum swings, defining break-of-serve moments",
            "diagnostic": (
                "Strong 10th lord = player converts break points and closes out sets; "
                "weak 10th lord = multiple missed match points"
            ),
        },
        "notes": (
            "The same 1st/7th (Player A/B) and 10th/4th lord comparison governs overall "
            "match outcome. Houses 3/6/10 above are used to time specific events within "
            "the match via Reduced Vimshottari segments."
        ),
    },

    "football_house_map": {
        "house_1": {
            "governs": "First kick, centre forward, initial team confidence and momentum",
            "diagnostic": (
                "Benefic in 1st = strong opening pressure from Team A; "
                "malefic in 1st = nervous start, early defensive shape"
            ),
        },
        "house_3": {
            "governs": "Passes, dribbles, player connectivity and combination play",
            "diagnostic": (
                "Mercury strong = crisp passing; Mars in 3rd = direct long-ball play "
                "and physical tackling battles"
            ),
        },
        "house_5": {
            "governs": "Dream goals, player intuition, mid-fielders' creative spark",
            "diagnostic": (
                "Jupiter in 5th = spectacular goal or midfield genius moment; "
                "afflicted 5th = missed golden chances"
            ),
        },
        "house_8": {
            "governs": "Sudden death, penalty shoot-outs, post-game analysis, injury time",
            "diagnostic": (
                "Saturn in 8th = shoot-out or match dragging into extra time; "
                "strong 8th lord for Team B = comeback from dead"
            ),
        },
        "house_9": {
            "governs": "Referees, off-side rules, VAR reviews, 'Hand of God' moments",
            "diagnostic": (
                "Afflicted 9th = red cards, controversial VAR overturns; "
                "strong 9th = clean refereeing"
            ),
        },
        "notes": (
            "Football uses 90-minute match divided by 12 signs (~7.5 min per segment) "
            "for Reduced Vimshottari. Penalty shoot-out phase governed by 8th house — "
            "the team whose 8th lord is stronger has better shoot-out probability."
        ),
    },

    "cross_sport_constants": {
        "dual_team_matrix": "1st house = Team A (toss winner), 7th house = Team B — same for all sports",
        "victory_axis":     "10th lord (Team A win) vs 4th lord (Team B win) — same for all sports",
        "captain_filter":   "+0.15 weight if captain's natal chart is transitorily strong — same for all sports",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# COMBINE
# ─────────────────────────────────────────────────────────────────────────────
ALL_SPECS = [
    SPORTS_DUAL_TEAM_ENGINE,
    CRICKET_EVENT_HOUSE_MAP,
    TENNIS_FOOTBALL_HOUSE_MAP,
]


async def run():
    now = datetime.now(timezone.utc)
    for spec in ALL_SPECS:
        spec["batch_id"]   = _BATCH
        spec["created_at"] = now.isoformat()

    if DRY_RUN:
        print(f"\nBuilt {len(ALL_SPECS)} specs for batch {_BATCH}")
        print(f"Collection: mundane_engine_specs  |  science: mundane_jyotish\n")
        print("Specs:")
        for s in ALL_SPECS:
            print(f"  {s['spec_id']}")
        print("\nNo overlap with v7 (gopal-ch10-sports-career-indicators).")
        print("v7 = natal/career rules. v20 = match prediction framework.")
        print("\nDry run complete.")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    col    = client[DB_NAME]["mundane_engine_specs"]
    inserted = updated = 0
    for spec in ALL_SPECS:
        result = await col.update_one(
            {"spec_id": spec["spec_id"]},
            {"$set": spec},
            upsert=True,
        )
        if result.upserted_id:
            inserted += 1
            print(f"  INS {spec['spec_id']}")
        else:
            updated += 1
            print(f"  UPD {spec['spec_id']}")
    print(f"\nInserted {inserted} / Updated {updated} specs → horoscope_db.mundane_engine_specs")
    client.close()


if __name__ == "__main__":
    asyncio.run(run())
