"""
ingest_mundane_interpretation_v20.py
=====================================
Batch:      mundane-interp-v20-20260508
Collection: interpretation_rules
Science:    mundane_jyotish
Source:     Gopalakrishnan Ch 10 — Predicting Sports Events

SCOPE — WHAT IS NEW vs v7
--------------------------
v7 already ingested the NATAL/CAREER side of Gopal Ch10:
  mundane-gopal-ch10-saturn-8th-dasa-lord-career-fall
  mundane-gopal-ch10-mars-perigee-leadership-change

v20 adds the MATCH PREDICTION side — 9 IF-THEN diagnostic rules:

NEW RULES (9):
  Group S — Sports Match Prediction (9 rules)
    mundane-gopal-ch10-sports-toss-winner-victory-gate
    mundane-gopal-ch10-sports-chasing-victory-trigger
    mundane-gopal-ch10-sports-batting-first-winner-gate
    mundane-gopal-ch10-sports-close-finish-trigger
    mundane-gopal-ch10-sports-rain-delay-monitor
    mundane-gopal-ch10-sports-injury-scandal-alert
    mundane-gopal-ch10-sports-umpire-conflict-filter
    mundane-gopal-ch10-sports-captain-lagna-boost
    mundane-gopal-ch10-sports-match-longevity-gate

Engine specs: gopal-ch10-sports-dual-team-engine,
              gopal-ch10-cricket-event-house-map,
              gopal-ch10-tennis-football-event-house-map
"""

import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.environ.get("DB_NAME",   "horoscope_db")
BATCH_ID  = "mundane-interp-v20-20260508"
DRY_RUN   = True

# ─────────────────────────────────────────────────────────────────────────────
# GROUP S — SPORTS MATCH PREDICTION RULES (9 rules)
# ─────────────────────────────────────────────────────────────────────────────
GROUP_S = [
    {
        "rule_id":        "mundane-gopal-ch10-sports-toss-winner-victory-gate",
        "sub_type":       "sports_match_prediction",
        "title":          "Gopal Ch10 — Toss Winner Victory Gate (10th Lord vs 4th Lord)",
        "source_chapter": "Gopalakrishnan Ch 10 — Predicting Sports Events (pp.741–744)",
        "condition": (
            "IF the 10th lord from the match Lagna is stronger than the 4th lord "
            "(assessed from Lagna, Chandra Lagna, and Karkamsha Lagna) — where strength "
            "is ranked as: Exaltation > Own sign > Friendly sign > Neutral > Debilitation, "
            "and Retrograde reduces strength by one tier, Combust planet is treated as "
            "severely weakened — THEN Team A (toss winner / 1st house team) wins the match; "
            "IF the 4th lord is stronger than the 10th lord THEN Team B (7th house team) wins; "
            "IF the match chart is requested before the toss is complete THEN withhold prediction: "
            "'Awaiting Toss — team assignment (1st vs 7th house) not yet fixed'"
        ),
        "result": (
            "Team A Victory (toss winner wins): 10th lord dominance confirmed — "
            "the team assigned to Lagna/1st house will win the match. "
            "Team B Victory (toss loser wins): 4th lord dominance confirmed — "
            "the team assigned to the 7th house will win the match. "
            "Validated: India vs West Indies 1st ODI (Jamaica, 18 May 2006) — "
            "Mercury (10th lord, Trikona) stronger than Jupiter (4th lord, Retrograde) "
            "→ India won by 5 wickets. India vs WI 3rd ODI (St. Kitts, 23 May 2006) "
            "→ same Mercury dominance → India won again."
        ),
        "severity":       "high",
        "checkable":      True,
        "synthesis_sources": [
            "gopal-ch10-sports-dual-team-engine",
        ],
    },
    {
        "rule_id":        "mundane-gopal-ch10-sports-chasing-victory-trigger",
        "sub_type":       "sports_match_prediction",
        "title":          "Gopal Ch10 — Chasing Victory Trigger (4th Lord Exalted or Vargottam)",
        "source_chapter": "Gopalakrishnan Ch 10 — Predicting Sports Events (pp.744–746)",
        "condition": (
            "IF the 4th lord (Team B's victory significator — the 10th from the 7th) "
            "is Exalted or Vargottam (same sign in Rasi and Navamsa) at match start, "
            "THEN Team B will successfully chase any target set by Team A — "
            "this override applies even when the 10th lord appears moderately strong; "
            "the Exaltation/Vargottam of the 4th lord adds +0.30 to Team B's chase "
            "probability weight before the base 10th/4th comparison"
        ),
        "result": (
            "Team B Chase Victory confirmed: the team batting second will successfully "
            "overhaul the target set by Team A. Even a strong Team A innings does not "
            "prevent this if the 4th lord is Exalted or Vargottam. "
            "Apply as a primary modifier before the standard Toss Winner Victory Gate."
        ),
        "severity":       "high",
        "checkable":      True,
        "synthesis_sources": [
            "gopal-ch10-sports-dual-team-engine",
        ],
    },
    {
        "rule_id":        "mundane-gopal-ch10-sports-batting-first-winner-gate",
        "sub_type":       "sports_match_prediction",
        "title":          "Gopal Ch10 — Batting First Winner Gate (10th Lord Trikona + Non-Retrograde)",
        "source_chapter": "Gopalakrishnan Ch 10 — Predicting Sports Events (pp.743–744)",
        "condition": (
            "IF the 10th lord from the match Lagna is placed in a Trikona house "
            "(1st, 5th, or 9th house) AND is not Retrograde THEN the team batting "
            "first (Team A) has a high probability of winning — "
            "Trikona placement amplifies the 10th lord's victory signal; "
            "Retrograde negates this advantage even if Trikona-placed"
        ),
        "result": (
            "Team batting first (Team A) will dominate the match and defend their total. "
            "Trikona placement of the 10th lord is the strongest single indicator of "
            "a comfortable Team A batting-first victory. "
            "Validated: India vs WI 2006 series — Mercury (10th lord) in 9th house "
            "(Trikona), non-Retrograde → India successfully defended twice."
        ),
        "severity":       "high",
        "checkable":      True,
        "synthesis_sources": [
            "gopal-ch10-sports-dual-team-engine",
            "gopal-ch10-cricket-event-house-map",
        ],
    },
    {
        "rule_id":        "mundane-gopal-ch10-sports-close-finish-trigger",
        "sub_type":       "sports_match_prediction",
        "title":          "Gopal Ch10 — Close Finish Trigger (Equal Lords + 8th Lord in Dual Sign)",
        "source_chapter": "Gopalakrishnan Ch 10 — Predicting Sports Events (pp.744–745)",
        "condition": (
            "IF the 10th lord and the 4th lord are assessed as equal in strength "
            "(neither clearly dominant after full triage from Lagna, Chandra Lagna, "
            "and Karkamsha) AND the 8th lord of the match chart is placed in a Dual "
            "sign (Gemini, Virgo, Sagittarius, or Pisces) THEN the match will be "
            "extremely competitive and the outcome decided in the final overs, sets, "
            "or minutes with no clear early indicator of a winner"
        ),
        "result": (
            "Match Alert: Highly competitive finish — result decided in final "
            "overs/last set/penalty shoot-out. No decisive winner predicted from "
            "chart alone. Monitor Reduced Vimshottari segments for the final "
            "phase to identify which team has planetary support in the closing stages."
        ),
        "severity":       "medium",
        "checkable":      True,
        "synthesis_sources": [
            "gopal-ch10-sports-dual-team-engine",
        ],
    },
    {
        "rule_id":        "mundane-gopal-ch10-sports-rain-delay-monitor",
        "sub_type":       "sports_match_prediction",
        "title":          "Gopal Ch10 — Rain Delay Monitor (Watery 4th House + 4th Lord in Watery Sign)",
        "source_chapter": "Gopalakrishnan Ch 10 — Predicting Sports Events (pp.744–745)",
        "condition": (
            "IF the 4th house of the match chart contains watery planets (Moon or Venus) "
            "AND the 4th lord is simultaneously placed in a watery sign "
            "(Cancer, Scorpio, or Pisces) THEN there is a high probability of match "
            "interruption or abandonment due to rain — "
            "the 4th house governs atmospheric conditions; "
            "the dual watery activation (planet + lord both watery) is the threshold trigger"
        ),
        "result": (
            "Weather Warning: High probability of rain delay or match interruption. "
            "In limited-overs cricket, apply DLS method probability. "
            "In tennis, expect play suspension. In football, expect waterlogged pitch risk. "
            "The actual result remains pending until match is completed — "
            "do not project a winner until interrupted play resumes."
        ),
        "severity":       "medium",
        "checkable":      True,
        "synthesis_sources": [
            "gopal-ch10-sports-dual-team-engine",
            "gopal-ch10-cricket-event-house-map",
        ],
    },
    {
        "rule_id":        "mundane-gopal-ch10-sports-injury-scandal-alert",
        "sub_type":       "sports_match_prediction",
        "title":          "Gopal Ch10 — Injury and Scandal Alert (Mars or Rahu in 6th House)",
        "source_chapter": "Gopalakrishnan Ch 10 — Predicting Sports Events (pp.743–744)",
        "condition": (
            "IF Mars or Rahu occupies the 6th house of the match chart "
            "(the 6th house governs fall of wickets, injuries, run-outs, and controversies) "
            "THEN output a Match Integrity Alert — "
            "Mars in 6th = physical injury to a key player or aggressive confrontation; "
            "Rahu in 6th = match-fixing allegations, controversial umpiring, "
            "or disciplinary incidents that overshadow the result"
        ),
        "result": (
            "Match Alert: High risk of player injury (Mars) or match-fixing / "
            "controversial umpire decisions / disciplinary incident (Rahu). "
            "The match result may be disputed or overshadowed by off-field events. "
            "Mars + Rahu conjunct in 6th = highest-severity integrity alert — "
            "flag for post-match investigation monitoring."
        ),
        "severity":       "medium",
        "checkable":      True,
        "synthesis_sources": [
            "gopal-ch10-cricket-event-house-map",
            "gopal-ch10-tennis-football-event-house-map",
        ],
    },
    {
        "rule_id":        "mundane-gopal-ch10-sports-umpire-conflict-filter",
        "sub_type":       "sports_match_prediction",
        "title":          "Gopal Ch10 — Umpire Conflict Filter (Mars or Rahu in 9th House)",
        "source_chapter": "Gopalakrishnan Ch 10 — Predicting Sports Events (pp.743–746)",
        "condition": (
            "IF Mars or Rahu occupies the 9th house of the match chart "
            "(the 9th house governs umpires, referees, third-umpire decisions, "
            "and the captain/vice-captain) THEN the match will be marred by "
            "officiating controversy — "
            "Mars in 9th = aggressive captain behaviour or confrontation with officials; "
            "Rahu in 9th = VAR/DRS controversy, off-side disputes, or "
            "'Hand of God'-type illegal incidents that affect the result"
        ),
        "result": (
            "Judgment Alert: Match likely marred by poor officiating, controversial "
            "third-umpire / VAR decisions, or captain-referee confrontation. "
            "The decisive moment of the match may hinge on an officiating call "
            "rather than pure play quality. "
            "Flag this match for referee conduct review regardless of final result."
        ),
        "severity":       "medium",
        "checkable":      True,
        "synthesis_sources": [
            "gopal-ch10-cricket-event-house-map",
            "gopal-ch10-tennis-football-event-house-map",
        ],
    },
    {
        "rule_id":        "mundane-gopal-ch10-sports-captain-lagna-boost",
        "sub_type":       "sports_match_prediction",
        "title":          "Gopal Ch10 — Captain's Lagna Boost (+0.15 Victory Weight)",
        "source_chapter": "Gopalakrishnan Ch 10 — Predicting Sports Events (pp.743–745)",
        "condition": (
            "IF the captain's individual natal chart is strong during the match window — "
            "specifically, the captain's Dasha and Antardasha planets are strong from "
            "both natal Lagna and natal Chandra Lagna during the match date — "
            "THEN add +0.15 to that team's victory probability weight "
            "after the base 10th lord vs 4th lord comparison is completed; "
            "apply this as a secondary modifier only — it does not override a "
            "decisive 10th/4th lord strength difference"
        ),
        "result": (
            "Captain's natal strength confirmed during match window — "
            "add +0.15 to the team's base victory probability. "
            "This modifier can tip close matches (equal-strength 10th/4th lords) "
            "toward the team with the stronger captain. "
            "Do not apply if captain's natal data is unavailable or unverified."
        ),
        "severity":       "medium",
        "checkable":      True,
        "synthesis_sources": [
            "gopal-ch10-sports-dual-team-engine",
        ],
    },
    {
        "rule_id":        "mundane-gopal-ch10-sports-match-longevity-gate",
        "sub_type":       "sports_match_prediction",
        "title":          "Gopal Ch10 — Match Longevity Gate (8th Lord in Fixed Sign)",
        "source_chapter": "Gopalakrishnan Ch 10 — Predicting Sports Events (pp.744–746)",
        "condition": (
            "IF the 8th lord of the match chart is placed in a Fixed sign "
            "(Taurus, Leo, Scorpio, or Aquarius) THEN the match will go to its "
            "full scheduled duration — no early finish, no sudden collapse; "
            "in cricket: match goes to final over / all 10 wickets fall; "
            "in football: match goes to full 90 minutes / extra time; "
            "in tennis: match goes to full sets with no retirements; "
            "Fixed sign rigidity of the 8th lord locks in the full match arc"
        ),
        "result": (
            "Longevity Alert: Match goes to full duration — no early finish. "
            "Cricket: expect close contest decided in final overs, all wickets used. "
            "Football: 90 minutes minimum, possible extra time or penalties. "
            "Tennis: full sets played, no retirement injury likely. "
            "Combine with Close Finish Trigger (equal lords + 8th lord in Dual sign) "
            "to distinguish: Fixed sign = full duration but decisive; "
            "Dual sign = full duration AND genuinely uncertain outcome."
        ),
        "severity":       "low",
        "checkable":      True,
        "synthesis_sources": [
            "gopal-ch10-sports-dual-team-engine",
            "gopal-ch10-cricket-event-house-map",
            "gopal-ch10-tennis-football-event-house-map",
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# COMBINE
# ─────────────────────────────────────────────────────────────────────────────
ALL_RULES = GROUP_S


async def run():
    now = datetime.now(timezone.utc)
    for rule in ALL_RULES:
        rule["batch_id"]        = BATCH_ID
        rule["science_id"]      = "mundane_jyotish"
        rule["collection"]      = "interpretation_rules"
        rule["rule_type"]       = "interpretation"
        rule["approval_status"] = "pending_review"
        rule["ingested_at"]     = now
        if "synthesis_sources" not in rule:
            rule["synthesis_sources"] = []

    if DRY_RUN:
        print(f"\nBuilt {len(ALL_RULES)} rules for batch {BATCH_ID}")
        print(f"Collection: interpretation_rules  |  science: mundane_jyotish\n")
        print("Breakdown:")
        print(f"  Group S — Sports Match Prediction: {len(GROUP_S)}")
        print(f"\nTotal: {len(ALL_RULES)}")
        print("\nRule IDs:")
        for r in ALL_RULES:
            print(f"  {r['rule_id']}")
        print("\nNo overlap with v7:")
        print("  v7 rules: saturn-8th-dasa-lord-career-fall, mars-perigee-leadership-change")
        print("  v20 rules: match-prediction domain (toss/lords/alerts/filters)")
        print("\nDry run complete.")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    col    = client[DB_NAME]["interpretation_rules"]
    inserted = updated = 0
    for rule in ALL_RULES:
        result = await col.update_one(
            {"rule_id": rule["rule_id"]},
            {"$set": rule},
            upsert=True,
        )
        if result.upserted_id:
            inserted += 1
            print(f"  INS {rule['rule_id']}")
        else:
            updated += 1
            print(f"  UPD {rule['rule_id']}")
    print(f"\nInserted {inserted} / Updated {updated} rules → horoscope_db.interpretation_rules")
    client.close()


if __name__ == "__main__":
    asyncio.run(run())
