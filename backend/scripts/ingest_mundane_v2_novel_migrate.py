"""
ingest_mundane_v2_novel_migrate.py
====================================
Batch: mundane-interp-v2-novel-20260508
Collection: interpretation_rules
Science: mundane_jyotish

PURPOSE
-------
Migrates the 13 NOVEL rules from the original v2 script that are NOT covered
by any v3–v19 ingest. The 8 Mehta Ch10 rules from v2 are discarded — their
content is already captured in v14 under different rule_ids.

V2 MIGRATION DECISION (8 May 2026)
------------------------------------
v2 had 21 rules across 4 chapters:
  Group L — Gopal Ch 2 Heuristic Filters  (6 rules) → MIGRATE (novel)
  Group M — Mehta Ch 10 Macro-Conjunctions (8 rules) → DISCARD (covered by v14)
  Group N — Mehta Ch 6 Diagnostic Rules    (4 rules) → MIGRATE (novel)
  Group O — Raphael Ch 3 Diagnostic Rules  (3 rules) → MIGRATE (novel)

v1 MIGRATION DECISION (8 May 2026)
------------------------------------
v1 (152 rules) → DISCARD in full:
  - Uses pymongo synchronous driver (incompatible with motor-async stack)
  - Uses nested source.science schema (invisible to science_id query)
  - All 11 chapter areas are covered by v3–v19 content

KEY FIX vs v2 ORIGINAL
-----------------------
The original v2 condition fields were Python dicts (structured tables).
These are converted to prose IF-THEN-ELSE strings here so the validator
can process them through its standard text pipeline (not the matrix-dict route).

NOVEL RULES (13):
  Group L — Gopal Ch 2 Heuristic Filters (6 rules)
    mundane-gopal-ch2-10th-lord-triage
    mundane-gopal-ch2-india-lagna-filter
    mundane-gopal-ch2-governance-longevity
    mundane-gopal-ch2-celebrity-authentication
    mundane-gopal-ch2-election-comparative-audit
    mundane-gopal-ch2-saturn-transit-regime-cycle

  Group N — Mehta Ch 6 Diagnostic Rules (4 rules)
    mundane-mehta-ch6-sun-6th-border-war
    mundane-mehta-ch6-eclipse-10th-overthrow
    mundane-mehta-ch6-5th-malefic-assassination
    mundane-mehta-ch6-sat-10th-democracy

  Group O — Raphael Ch 3 Diagnostic Rules (3 rules)
    mundane-raphael-ch3-angular-multiplier
    mundane-raphael-ch3-intellectual-triad
    mundane-raphael-ch3-opposition-4th-trigger

Upsert key: rule_id
All rules: approval_status=pending_review, checkable=False
"""

import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.environ.get("DB_NAME",   "horoscope_db")
BATCH_ID  = "mundane-interp-v2-novel-20260508"
DRY_RUN   = True   # set False to write to MongoDB

# ─────────────────────────────────────────────────────────────────────────────
# GROUP L — GOPALAKRISHNAN CH 2: HEURISTIC FILTERS (6 rules)
# ─────────────────────────────────────────────────────────────────────────────
GROUP_L = [
    {
        "rule_id":        "mundane-gopal-ch2-10th-lord-triage",
        "sub_type":       "chart_authentication",
        "title":          "Gopal Ch 2 — 10th Lord Triage (Chart Authenticity Veto)",
        "source_chapter": "Gopal Ch 2 — How to Become a Very Good Mundane Astrologer",
        "condition": (
            "IF the 10th lord is NOT strong from at least 2 of [Lagna, Chandra Lagna, "
            "Karkamsha Lagna] THEN flag chart as 'Potentially Inauthentic — verify birth "
            "data before analysis'; IF the 10th house is vacant AND unaspected THEN "
            "reinforce the flag regardless of other factors"
        ),
        "result": (
            "Chart flagged as 'Potentially Inauthentic' — stop analysis and verify birth "
            "data. Apply as a mandatory first gate before any deep mundane analysis. "
            "Example: Advani chart with 10th lord weak in 12th → rejected as likely "
            "incorrect birth data."
        ),
        "severity":       "high",
        "synthesis_sources": ["gopal-ch2-heuristic-engine"],
    },
    {
        "rule_id":        "mundane-gopal-ch2-india-lagna-filter",
        "sub_type":       "india_leadership_filter",
        "title":          "Gopal Ch 2 — India Alignment Lagna Filter for National Leaders",
        "source_chapter": "Gopal Ch 2 — Indian Political Lagna Filter",
        "condition": (
            "IF Indian national leader's Lagna is Cancer or Taurus THEN Tier 1 success "
            "alignment (harmonious with India's Taurus Independence Lagna); "
            "IF Lagna is Scorpio or Leo THEN Tier 2 success alignment; "
            "IF Lagna is Libra (6th from Taurus), Sagittarius (8th from Taurus), or "
            "Aries (12th from Taurus) THEN veto — candidate faces structural disadvantage "
            "in reaching sustained national power in India"
        ),
        "result": (
            "Tier 1 Lagnas (Cancer, Taurus) → highest probability of sustained national "
            "power in India. Tier 2 Lagnas (Scorpio, Leo) → moderate success probability. "
            "Veto Lagnas (Libra, Sagittarius, Aries) → significantly lower probability of "
            "sustained Indian national leadership — apply as disqualification flag."
        ),
        "severity":       "medium",
        "synthesis_sources": ["gopal-ch2-heuristic-engine"],
    },
    {
        "rule_id":        "mundane-gopal-ch2-governance-longevity",
        "sub_type":       "governance_longevity_math",
        "title":          "Gopal Ch 2 — Saturnine Longevity Rule for Indian PM",
        "source_chapter": "Gopal Ch 2 — Saturnine Power Gate",
        "condition": (
            "IF an Indian PM is unmarried or widowed AND Saturn is the 10th lord of India "
            "(Taurus Lagna chart) THEN long tenure predicted — Saturn (asceticism, solitude) "
            "is naturally empowered by the leader's renunciation of domestic life; "
            "IF the Indian PM has a living spouse THEN shorter tenure predicted"
        ),
        "result": (
            "Long-tenure gate: Nehru (widower), Indira Gandhi (widow), Vajpayee (bachelor) "
            "all validated as long-tenure PMs under this rule. "
            "Short-tenure examples: Rajiv Gandhi, Lal Bahadur Shastri, V.P. Singh. "
            "This is the 'Law of Saturn as 10th Lord' — domestic renunciation amplifies "
            "executive staying power for India's leadership chart."
        ),
        "severity":       "medium",
        "synthesis_sources": ["gopal-ch2-heuristic-engine"],
    },
    {
        "rule_id":        "mundane-gopal-ch2-celebrity-authentication",
        "sub_type":       "chart_authentication",
        "title":          "Gopal Ch 2 — Celebrity / Leader Chart Authentication Rule",
        "source_chapter": "Gopal Ch 2 — 10th House Verification",
        "condition": (
            "IF the 10th lord is NOT strong from at least 2 of [Lagna, Chandra Lagna, "
            "Karkamsha Lagna] THEN reject chart (Gate 1 failure); "
            "IF the 10th house is vacant AND unaspected by any planet THEN reject chart "
            "(Gate 2 failure); "
            "Apply Gate 1 then Gate 2 as the FIRST check before any analysis of any "
            "celebrity or national leader chart"
        ),
        "result": (
            "Chart passes authentication: proceed with full analysis. "
            "Chart fails Gate 1 or Gate 2: output 'Chart Rejected — Potentially Inauthentic "
            "Birth Data' and halt. Do not apply any further planetary or dasha analysis "
            "until birth data is verified against public records."
        ),
        "severity":       "high",
        "synthesis_sources": ["gopal-ch2-heuristic-engine"],
    },
    {
        "rule_id":        "mundane-gopal-ch2-election-comparative-audit",
        "sub_type":       "election_winner_logic",
        "title":          "Gopal Ch 2 — Election Winner Comparative Strength Audit",
        "source_chapter": "Gopal Ch 2 — Election Winner Logic",
        "condition": (
            "IF comparing two election candidates: "
            "Step 1 — compare 10th lord strength from Lagna, Chandra Lagna, and Karkamsha "
            "for both candidates; "
            "Step 2 — identify who is running a Raja Yoga Dasha period (Kendra/Trikona "
            "lord as Mahadasha or Antardasha lord); "
            "Step 3 — veto any candidate currently running a 6th, 8th, or 12th lord Dasha "
            "(Dusthana Dasha = near-certain electoral defeat); "
            "Step 4 — apply India Alignment Lagna Filter for national Indian elections "
            "(Libra/Sagittarius/Aries Lagna candidates face structural disadvantage)"
        ),
        "result": (
            "Candidate with stronger 10th lord + active Raja Yoga Dasha + non-Dusthana "
            "period + favorable Lagna alignment wins. "
            "Any candidate failing Step 3 (active Dusthana Dasha) is near-certainly "
            "eliminated regardless of other chart strengths."
        ),
        "severity":       "high",
        "synthesis_sources": ["gopal-ch2-heuristic-engine"],
    },
    {
        "rule_id":        "mundane-gopal-ch2-saturn-transit-regime-cycle",
        "sub_type":       "governance_longevity_math",
        "title":          "Gopal Ch 2 — Saturn Transit Regime Cycle (4th/8th/12th House Trigger)",
        "source_chapter": "Gopal Ch 2 — Law of Karma in Office",
        "condition": (
            "IF Saturn transits through the 4th, 8th, or 12th house from a political "
            "leader's natal Moon THEN regime change, electoral defeat, or loss of power "
            "is triggered — this is the 'Law of Karma in Office'; "
            "the veto applies even when the leader has strong administrative or technological "
            "achievements, as Saturn's 7.5-year transit cycle overrides performance-based outcomes"
        ),
        "result": (
            "High probability of regime change, electoral defeat, or loss of power for "
            "the leader during Saturn's transit through 4th, 8th, or 12th from natal Moon. "
            "Case study: Chandra Babu Naidu's political downfall despite major IT and "
            "infrastructure achievements — Saturn's transit through 4th/8th/12th overrode "
            "all positive governance metrics."
        ),
        "severity":       "high",
        "synthesis_sources": ["gopal-ch2-heuristic-engine"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# GROUP N — MEHTA CH 6: DIAGNOSTIC RULES (4 rules)
# ─────────────────────────────────────────────────────────────────────────────
GROUP_N = [
    {
        "rule_id":        "mundane-mehta-ch6-sun-6th-border-war",
        "sub_type":       "hazard_border_conflict",
        "title":          "Mehta Ch 6 — Sun in 6th House with Malefic: Border Clash Alert",
        "source_chapter": "Mehta Ch 6 — Houses and their Signification",
        "condition": (
            "IF the Sun is in the 6th house of a national chart (6th = Ministry of Defense, "
            "Armed Forces) AND is conjunct a malefic (Saturn, Mars, or Rahu) THEN trigger "
            "'Serious Border Clash Alert' — the 6th house governs territorial defense and "
            "military combativeness; Sun + malefic here energizes leadership with an "
            "aggressive, combative national disposition; "
            "IF Mars additionally lords both the 6th AND the 7th house THEN open war is "
            "near-certain"
        ),
        "result": (
            "Serious Border Clash Alert: military escalation, territorial skirmishes, or "
            "armed conflict is imminent. "
            "Mars lords 6th + 7th simultaneously: Open War = CERTAIN — escalate to "
            "Critical War Warning regardless of other chart factors."
        ),
        "severity":       "critical",
        "synthesis_sources": ["mehta-ch6-house-diagnostics"],
    },
    {
        "rule_id":        "mundane-mehta-ch6-eclipse-10th-overthrow",
        "sub_type":       "governance_8th_house_veto",
        "title":          "Mehta Ch 6 — Eclipse / Malefic in 10th House: Government Overthrow Sign",
        "source_chapter": "Mehta Ch 6 — Houses and their Signification",
        "condition": (
            "IF a solar or lunar eclipse falls on the 10th house of a national chart THEN "
            "direct sign of defeat or overthrow of the government; "
            "IF a malefic (Saturn, Rahu, Mars) is stationed or transiting the 10th house "
            "THEN disgrace, scandal, or illness/death among the head of state; "
            "IF a lunation (New Moon or Full Moon) also falls in the 10th house THEN it "
            "acts as the Minute Hand materializing the eclipse trend into a concrete event"
        ),
        "result": (
            "Government Defeat / Overthrow / Disgrace of Head of State. "
            "Eclipse in 10th = highest-severity governance warning in the mundane chart. "
            "Nearest lunation in 10th marks the event timing window."
        ),
        "severity":       "critical",
        "synthesis_sources": ["mehta-ch6-house-diagnostics"],
    },
    {
        "rule_id":        "mundane-mehta-ch6-5th-malefic-assassination",
        "sub_type":       "hazard_pm_jeopardy",
        "title":          "Mehta Ch 6 — 5th House Malefics + 10th Lord Afflicted: Assassination / Danger to Ruler",
        "source_chapter": "Mehta Ch 6 — Houses and their Signification",
        "condition": (
            "IF the 5th house (which is the 8th from the 10th — the Danger to the Ruler "
            "position) contains one or more malefics (Saturn, Mars, Rahu) AND the 10th "
            "lord is simultaneously afflicted by malefic aspect, combustion, or debilitation "
            "THEN trigger 'Critical Danger to Ruler' — the dual affliction of Ruler's "
            "Danger zone (5th) and Ruler's power significator (10th lord) produces the "
            "highest assassination / political elimination risk"
        ),
        "result": (
            "Critical Danger to Ruler: Assassination risk, terrorist attacks on officials, "
            "or sudden political elimination of the head of state. "
            "Both conditions (5th house malefic + 10th lord afflicted) must be present "
            "simultaneously — single-factor affliction alone does not trigger this rule."
        ),
        "severity":       "critical",
        "synthesis_sources": ["mehta-ch6-house-diagnostics"],
    },
    {
        "rule_id":        "mundane-mehta-ch6-sat-10th-democracy",
        "sub_type":       "governance_fixed_lagna",
        "title":          "Mehta Ch 6 — Saturn in 10th House: Democracy vs. Dictator Diagnostic",
        "source_chapter": "Mehta Ch 6 — Houses and their Signification",
        "condition": (
            "IF Saturn is in the 10th house of a Republic or Democracy national chart THEN "
            "BENEFIC — Saturn strengthens democratic institutions, rule of law, and long-term "
            "stable governance (Saturn as natural significator of the common people and labor "
            "is empowered in a democratically-elected government's 10th house); "
            "IF Saturn is in the 10th house of a Coup-based or Autocratic national chart "
            "THEN FATAL — Saturn's energy of mass opposition and resistance undermines the "
            "dictator's authority, causing internal dissent, labor revolts, and eventual "
            "overthrow of the autocratic regime"
        ),
        "result": (
            "Democracy chart: Saturn in 10th → stable democratic governance, long-term "
            "institutional strengthening. "
            "Autocratic chart: Saturn in 10th → internal revolt, labor strikes, "
            "eventual regime collapse. "
            "Diagnosis requires first classifying the national chart as democratic vs. "
            "autocratic before applying the result."
        ),
        "severity":       "high",
        "synthesis_sources": ["mehta-ch6-house-diagnostics"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# GROUP O — RAPHAEL CH 3: DIAGNOSTIC RULES (3 rules)
# ─────────────────────────────────────────────────────────────────────────────
GROUP_O = [
    {
        "rule_id":        "mundane-raphael-ch3-angular-multiplier",
        "sub_type":       "house_strength_weighting",
        "title":          "Raphael Ch 3 — Angular House Power Multiplier",
        "source_chapter": "Raphael Ch 3 — Twelve Mundane Houses",
        "condition": (
            "IF a diagnostic planet occupies an Angular house (1, 4, 7, 10) THEN apply "
            "FULL diagnostic weight (1.0×) to its effects; "
            "IF planet occupies a Succedent house (2, 5, 8, 11) THEN apply 0.7× weight; "
            "IF planet occupies a Cadent house (3, 6, 9, 12) THEN apply 0.4× weight; "
            "IF planet is within 5 degrees of any house cusp THEN classify as 'Accidentally "
            "Dignified' — effects significantly amplified regardless of base house type"
        ),
        "result": (
            "All mundane diagnoses must weight planetary signals by house type before "
            "producing output. A critical malefic in the 4th house (Angular, 1.0×) carries "
            "far greater Calamity Warning weight than the same malefic in the 3rd house "
            "(Cadent, 0.4×). Accidentally Dignified planets override the base house weight "
            "and should be treated as Angular-strength regardless of cadent/succedent placement."
        ),
        "severity":       "medium",
        "synthesis_sources": ["raphael-ch3-twelve-houses"],
    },
    {
        "rule_id":        "mundane-raphael-ch3-intellectual-triad",
        "sub_type":       "national_mindset_audit",
        "title":          "Raphael Ch 3 — Intellectual Triad (Houses 1+3+9): National Mind Synchrony",
        "source_chapter": "Raphael Ch 3 — Twelve Mundane Houses",
        "condition": (
            "IF a query concerns National Mood, Press Freedom, Propaganda, Religious Harmony, "
            "or Public Opinion THEN audit Houses 1, 3, and 9 together as the Intellectual "
            "Triad (House 1 = Collective mental state; House 3 = Press and newspapers; "
            "House 9 = Religious attitude and higher thought); "
            "IF benefics occupy or strongly aspect all three houses THEN output national "
            "intellectual flourishing result; "
            "IF malefics afflict all three houses THEN output national intellectual crisis "
            "result; "
            "IF malefic is specifically in the 9th house THEN also trigger disruption in "
            "international shipping and scientific setbacks"
        ),
        "result": (
            "Benefic Triad (Houses 1+3+9 benefic): 'Nation entering period of intellectual "
            "growth, press freedom, and religious harmony.' "
            "Malefic Triad (all three afflicted): 'National intellectual crisis — press "
            "censorship, misinformation campaigns, and religious conflict.' "
            "Isolated 9th house malefic: international shipping disruption + scientific "
            "institution setbacks (secondary flag alongside main result)."
        ),
        "severity":       "medium",
        "synthesis_sources": ["raphael-ch3-twelve-houses"],
    },
    {
        "rule_id":        "mundane-raphael-ch3-opposition-4th-trigger",
        "sub_type":       "governance_coalition_discord",
        "title":          "Raphael Ch 3 — 4th House Opposition Rise Trigger",
        "source_chapter": "Raphael Ch 3 — Twelve Mundane Houses",
        "condition": (
            "IF the 4th house lord is strong AND aspected by Jupiter AND the 10th house "
            "(Government seat) is simultaneously afflicted by malefics THEN trigger "
            "'Opposition Party Rise Alert'; "
            "NOTE: the 4th house in mundane astrology governs both (a) the political "
            "Opposition party and (b) agriculture, weather, and crops — the same malefic "
            "transits that trigger agricultural crisis simultaneously trigger opposition "
            "political surge (dual activation of one house)"
        ),
        "result": (
            "Opposition Rise Alert: high probability of Opposition party gaining significant "
            "influence, electoral momentum, or winning public favor. "
            "Dual 4th house activation: the same transit that signals agricultural crop "
            "crisis simultaneously signals political opposition surge — report both outcomes "
            "when the 4th house is strongly activated by malefics."
        ),
        "severity":       "medium",
        "synthesis_sources": ["raphael-ch3-twelve-houses"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# COMBINE NOVEL GROUPS (Group M — Mehta Ch10 — intentionally excluded)
# ─────────────────────────────────────────────────────────────────────────────
ALL_RULES = GROUP_L + GROUP_N + GROUP_O


# ─────────────────────────────────────────────────────────────────────────────
# INGEST
# ─────────────────────────────────────────────────────────────────────────────
async def run():
    now = datetime.now(timezone.utc)
    for rule in ALL_RULES:
        rule["batch_id"]        = BATCH_ID
        rule["science_id"]      = "mundane_jyotish"
        rule["collection"]      = "interpretation_rules"
        rule["rule_type"]       = rule.get("rule_type", "interpretation")
        rule["approval_status"] = "pending_review"
        rule["checkable"]       = False
        rule["ingested_at"]     = now
        if "synthesis_sources" not in rule:
            rule["synthesis_sources"] = []

    if DRY_RUN:
        print(f"\nBuilt {len(ALL_RULES)} rules for batch {BATCH_ID}")
        print(f"Collection: interpretation_rules  |  science: mundane_jyotish\n")
        print("Breakdown by group:")
        print(f"  Group L — Gopal Ch 2 Heuristic Filters  : {len(GROUP_L)}")
        print(f"  Group N — Mehta Ch 6 Diagnostic Rules    : {len(GROUP_N)}")
        print(f"  Group O — Raphael Ch 3 Diagnostic Rules  : {len(GROUP_O)}")
        print(f"\nTotal: {len(ALL_RULES)}")
        print("\nRule IDs:")
        for r in ALL_RULES:
            print(f"  {r['rule_id']}")
        print("\nNOTE: Group M (Mehta Ch10, 8 rules) intentionally excluded —")
        print("      content covered by v14 (mehta-ch10-* rule_ids).")
        print("\nDry run complete.")
        return

    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    col = db["interpretation_rules"]
    inserted = updated = 0
    for rule in ALL_RULES:
        result = await col.update_one(
            {"rule_id": rule["rule_id"]},
            {"$set": rule},
            upsert=True,
        )
        if result.upserted_id:
            inserted += 1
        else:
            updated += 1
        print(f"  {'INS' if result.upserted_id else 'UPD'} {rule['rule_id']}")

    print(f"\nInserted {inserted} / Updated {updated} rules → horoscope_db.interpretation_rules")
    client.close()


if __name__ == "__main__":
    asyncio.run(run())
