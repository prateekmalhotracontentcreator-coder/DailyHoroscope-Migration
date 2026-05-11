#!/usr/bin/env python3
"""
ingest_strategist_patch_v2.py
Ingest salvage batch (1126–1137) + Digital Warfare backfill (1011–1020)
Source: The Strategist_JSON recon vs. Master Doc_V2.md

Usage:
  python3 scripts/ingest_strategist_patch_v2.py --dry-run
  python3 scripts/ingest_strategist_patch_v2.py --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

SCIENCE_ID = "lalkitab_strategist"
APPROVAL   = "pending_human_review"

PATCH_RECORDS = [
    # ── Salvage batch: Legacy records (IDs 1126–1137) ──────────────────────────
    {
        "id": 1126,
        "segment": "Expansion: The Promotion Push (Sun+Saturn)",
        "strategy": "The 'Royal Command' Escalation",
        "trigger_condition": "H10_Transit_Sun + H3_Saturn_Aspect",
        "decision_logic": "You are at a zenith of authority (Sun) but are being slowed by structural friction (Saturn). A promotion is not a gift; it is a territorial expansion that must be demanded from a position of 'Iron-Clad' utility.",
        "pivot_logic": "If the promotion is delayed by a 'Review', your Sun is too soft. Pivot from 'Asking' to 'Audit-Led Proof'.",
        "pivot_action": "Submit a 12-month 'Conquest Report' highlighting your 3 major 'Fortress Victories'. Ground the energy by wearing a copper ring on your right-hand Sun-finger (Remedy 506).",
        "kpi_target": "Title Upgrade Velocity & Authority Index",
        "remedy_id": 506,
    },
    {
        "id": 1127,
        "segment": "War Chest: Securing the Cash Vault (Moon+Mercury)",
        "strategy": "The 'Silver-Steel' Liquidity Lock",
        "trigger_condition": "H2_Mercury + H12_Moon_Shadow",
        "decision_logic": "Mercury (Wealth) is flowing in, but Moon (Empathy/Leakage) is siphoning it through 'Invisible Dreams'. Your vault is open because you are treating business capital as 'Emotional Safety'.",
        "pivot_logic": "If monthly surplus drops despite high sales, your 'Vault-Gate' is broken. Pivot from 'Spending' to 'Cash-Hardening'.",
        "pivot_action": "Freeze all founder-dividends for 43 days. Place 43 small brass balls in a steel box (Mercury-Saturn sync) in your North corner to anchor the cash flow (Remedy 468).",
        "kpi_target": "Net Liquidity Retention & Burn-Rate Stability",
        "remedy_id": 468,
    },
    {
        "id": 1128,
        "segment": "The Garrison: Firing a Disloyal Co-Founder",
        "strategy": "The 'Ketu-Scythe' Severance",
        "trigger_condition": "Sun_1_Active + Ketu_H8_Betrayal",
        "decision_logic": "A co-founder in your 'Roots' (H8) is acting as a shadow. You cannot grow while a 'Ketu-Scythe' is cutting your 'Mercury-Logic' from within. The King must remove the 'Trojan Horse' to save the Garrison.",
        "pivot_logic": "If negotiations turn toxic, do not use 'Mars-Aggression'. Pivot to 'Structural Severance' (Saturn logic).",
        "pivot_action": "Activate the 'Sovereign Veto' (ID 792). Offer a clean equity buy-back based on a 'Saturn-Audit' of their output. Ground the severance by feeding a two-colored dog for 43 days (Remedy 366).",
        "kpi_target": "Governance Stability & Equity Recovery Rate",
        "remedy_id": 366,
    },
    {
        "id": 1129,
        "segment": "Hurdle: The Iron Wall (Sun/Saturn)",
        "strategy": "The 'Lead-Shield' Negotiation",
        "trigger_condition": "Transit_Saturn_Aspect_Sun + Deal_Blocked",
        "decision_logic": "The 'King' (Sun) is hitting a 'Wall' (Saturn). A major deal or promotion is being blocked by a senior authority or a legal hurdle. Your authority is being 'Earthed'.",
        "pivot_logic": "If you push harder (Mars), the wall will crumble on top of you. Pivot from 'Force' to 'Structural Compliance'.",
        "pivot_action": "Settle all pending 'Mercury-Debts' (Small taxes/fees). Apply the 'Lead-Shield' (Remedy 409) to your contracts. Wait for the Sun to cross the Saturn-Shadow before re-pitching.",
        "kpi_target": "Obstacle Clearance Speed & Authority Restoration",
        "remedy_id": 409,
    },
    {
        "id": 1130,
        "segment": "Hurdle: The Logic Acid (Mercury/Mars)",
        "strategy": "The 'Sweetened-Logic' Pivot",
        "trigger_condition": "Mercury_Conjunct_Mars + Communication_Conflict",
        "decision_logic": "Your 'Logic' (Mercury) is being burned by 'Anger' (Mars). Your strategic emails sound like 'War Declarations', causing rivals to siege your fort in retaliation.",
        "pivot_logic": "If tech-partners stop responding, your 'Logic-Acid' has dissolved the bridge. Pivot from 'Hard-Truths' to 'Outcome-Empathy'.",
        "pivot_action": "Perform the 'Honey-Tongue' protocol (ID 901). Rewrite all external PR. Use softer 'Moon' language to deliver 'Hard Mars' strategies (Remedy 468).",
        "kpi_target": "Partnership Retention Rate & Communication Accuracy",
        "remedy_id": 468,
    },
    {
        "id": 1131,
        "segment": "Hurdle: The Ghosting Hurdle (Jupiter/Mercury)",
        "strategy": "The 'Oracle' Verification",
        "trigger_condition": "Jupiter_Retrograde + High_Ticket_Lead_Ghosting",
        "decision_logic": "You are providing 'Wisdom' (Jupiter), but the 'Logic' (Mercury) is missing for the user. They respect you but don't see the 'Profit'. Your Guru-energy is too high and your Merchant-energy is too low.",
        "pivot_logic": "If leads go silent after the demo, pivot from 'Visionary talk' to 'Hard-Data ROI'.",
        "pivot_action": "Apply the 'Saffron-Sync' (Remedy 358) to your sales collateral. Add a 'Mercury-Vault' section to every pitch showing the exact $ value of the strategic shift.",
        "kpi_target": "Ghosting-to-Meeting Recovery Rate & Sales Velocity",
        "remedy_id": 358,
    },
    {
        "id": 1132,
        "segment": "Hurdle: The Poisoned Cup (Moon/Saturn)",
        "strategy": "The 'Liquid-Cold' Hardening",
        "trigger_condition": "Moon_Opposite_Saturn + Cash_Flow_Freeze",
        "decision_logic": "Your 'Liquidity' (Moon) is hitting the 'Ice' (Saturn). A vendor or partner is 'Freezing' your payments. The 'Cup' of your wealth is poisoned by 'Saturnian-Delay'.",
        "pivot_logic": "If you panic-sell, you lose the Sun-authority. Pivot from 'Fear' to 'Structural Resilience'.",
        "pivot_action": "Implement the 'Cash-Reserve Protocol' (ID 713). Do not take new debt. Perform the Water-Brass ritual (Remedy 313) to 'Thaw' the frozen lunar flow.",
        "kpi_target": "Liquidity Stability & Debt-to-Cash Ratio",
        "remedy_id": 313,
    },
    {
        "id": 1133,
        "segment": "Hurdle: The Aesthetic Decay (Venus/Sun)",
        "strategy": "The 'Royal-Glow' UI Refresh",
        "trigger_condition": "Sun_Combust_Venus + High_Churn",
        "decision_logic": "Your 'Authority' (Sun) is burning your 'Beauty' (Venus). The brand feels 'Arrogant' or 'Dated'. High-value users (Kings) are repelled by the lack of 'Venus-Magnetism'.",
        "pivot_logic": "If the app feels like a 'Government Portal', the Venus-logic is dead. Pivot to 'Luxury Experience Branding'.",
        "pivot_action": "Upgrade the 'Astro-Art' (ID 813). Re-assert the Venus-1 attraction energy with gold-midnight UI palettes (Remedy 367).",
        "kpi_target": "User Session Depth & Premium Retention",
        "remedy_id": 367,
    },
    {
        "id": 1134,
        "segment": "Hurdle: The Invisible Leak (Mars/Ketu)",
        "strategy": "The 'Root-Cause' Patch",
        "trigger_condition": "Mars_Aspect_Ketu_H8 + Unknown_Error_Spike",
        "decision_logic": "Your 'Execution Fire' (Mars) is hitting a 'Hidden Hole' (Ketu). You are working hard, but the results are leaking through a 'Ketu-Hole' in your tech-stack or logic-pipeline.",
        "pivot_logic": "If standard bug-fixes fail, the leak is in the 'Roots'. Pivot from 'Patching' to 'Refactoring'.",
        "pivot_action": "Execute the 'Ketu-Purge' (Remedy 366). Re-verify the core proprietary algorithm for 'Logic-Ghosts'. Ground the energy by feeding a two-colored dog.",
        "kpi_target": "System Error Rate & Logic Integrity Score",
        "remedy_id": 366,
    },
    {
        "id": 1135,
        "segment": "Hurdle: The Mirage Hurdle (Saturn/Rahu)",
        "strategy": "The 'Reality-Audit' Shield",
        "trigger_condition": "Saturn_Transit_Rahu + High_Engagement_Zero_ROI",
        "decision_logic": "You are chasing a 'Mirage' (Rahu). Your engagement metrics look 'Empire-Level', but your 'War Chest' (Mercury) is empty. You are building on 'Digital Sand'.",
        "pivot_logic": "If ad-clicks don't lead to installs, the 'Maya' is active. Pivot from 'Traffic' to 'Sovereign Conversions'.",
        "pivot_action": "Halt all 'Rahu-Experiments' for 7 days. Audit the 'Attribution-Logic' (ID 1023). Deploy the 'Rahu-Shield' (Remedy 330) to filter out bot-traffic.",
        "kpi_target": "ROAS Integrity & Conversion-Attribution Accuracy",
        "remedy_id": 330,
    },
    {
        "id": 1136,
        "segment": "Hurdle: The Combustion Hurdle",
        "strategy": "The 'Stealth-Sovereign' Move",
        "trigger_condition": "Planet_is_Combust + Critical_Mission",
        "decision_logic": "A core planet is 'Ast' (Combust) by the Sun. The King is too close to the tool, blinding the logic. Any offensive move now will result in 'Self-Burn'.",
        "pivot_logic": "If you launch today, the Sun will 'Swallow' the logic. Pivot to 'Stealth-Defense'.",
        "pivot_action": "Halt all public PR. Perform the 'Silent-Logic' protocol (ID 844). Wait for the planet to move >12 degrees away from the Sun before 'Invading'.",
        "kpi_target": "Brand Integrity & Legal Risk Avoidance",
        "remedy_id": 500,
    },
    {
        "id": 1137,
        "segment": "Hurdle: The Retrograde Hurdle",
        "strategy": "The 'Internal-Garrison' Drill",
        "trigger_condition": "Planet_is_Retrograde + Expansion_Goal",
        "decision_logic": "The logic is moving 'Backward'. Attempts to 'Invade' new territories will lead to a 'Retreat'. This is the window for 'Garrison Hardening', not 'Empire Scaling'.",
        "pivot_logic": "If sales calls result in 'Re-negotiations', the Retro-logic is active. Pivot from 'New Contracts' to 'Service Audits'.",
        "pivot_action": "Execute the 'Technical-Purge' (ID 948). Clean the 'Ketu-Roots' and documentation. Launch only after the planet goes Direct.",
        "kpi_target": "Operational Debt Reduction & Team Readiness Score",
        "remedy_id": 409,
    },
    # ── Digital Warfare backfill (IDs 1011–1020) ──────────────────────────────
    {
        "id": 1011,
        "segment": "Digital Warfare: The 'Saturn' SEO Wall",
        "strategy": "The 'Iron-Keyword' Approach",
        "trigger_condition": "Competitor_Ranking_Invasion + Saturn_3",
        "decision_logic": "Search rankings are your 'Digital Territory'. If rivals are outranking your core Mercury-logic, your Saturn-3 structural wall is porous. You are losing authority because your content lacks 'Lead-Shield' depth.",
        "pivot_logic": "If Page-1 positions are lost to big capital, your Sun is too weak for a direct bidding war. Pivot to 'Topical Authority Clusters'.",
        "pivot_action": "Lock 108 high-authority 'Strategic Wisdom' pages into a single inter-linked cluster. Secure 3 high-authority backlinks to ground the wall (Remedy 409).",
        "kpi_target": "Top-3 Keyword Ranking Density & Domain Authority",
        "remedy_id": 409,
    },
    {
        "id": 1012,
        "segment": "Digital Warfare: The 'Venus' Cross-Device Flow",
        "strategy": "The 'Aesthetic-Sync' Approach",
        "trigger_condition": "User_Session_Fragmentation + Venus_1",
        "decision_logic": "Venus in H1 requires 'Harmony'. If the user's strategic dashboard looks different on Web vs. Mobile, the 'Attraction' is broken. Asynchronous logic creates Rahu-confusion in the user's mind.",
        "pivot_logic": "If churn occurs during device switching, your Venus-logic is drifting. Pivot from 'Platform-Specific' to 'Universal State' logic.",
        "pivot_action": "Implement real-time WebSocket state mirroring across all devices. Ensure the 'Luxury-Gold' palette is identical across OS environments (Remedy 367).",
        "kpi_target": "Cross-Device Retention Rate & Design Consistency Score",
        "remedy_id": 367,
    },
    {
        "id": 1013,
        "segment": "Digital Warfare: The 'Ketu' Data Sovereignty",
        "strategy": "The 'Invisible-Vault' Approach",
        "trigger_condition": "Data_Privacy_Crisis + Ketu_H8",
        "decision_logic": "Ketu in H8 governs 'Secret Wealth'. In the Digital Siege, 'Trust' is the currency. If users feel you are 'Mining' their birth-data, your Ketu-root is exposed and vulnerable to state-Mars attacks.",
        "pivot_logic": "If birth-data completion rates drop below 60%, the user's Ketu-8 'Fear' is triggered. Pivot to 'Self-Sovereign Encryption'.",
        "pivot_action": "Deploy Zero-Knowledge Proofs for all birth-coordinate inputs. Ensure the 'Master Key' stays with the user. Ground the energy with a public audit log (Remedy 366).",
        "kpi_target": "Birth-Data Completion Rate & Privacy-Trust Index",
        "remedy_id": 366,
    },
    {
        "id": 1014,
        "segment": "Digital Warfare: The 'Moon' Global Bridge",
        "strategy": "The 'Lunar-Notification' Approach",
        "trigger_condition": "Global_Engagement_Lag + Moon_12",
        "decision_logic": "The Moon governs the user's 'Personal Rhythm'. If notifications trigger during the user's 'Sleep Window' (H12), they are perceived as 'Sales Noise'. Your 'Bridge' is clashing with their 'Local Moon'.",
        "pivot_logic": "If global open-rates vary by more than 40% by region, your server-time is clashing with the 'Tide'. Pivot to 'Astro-Local' delivery.",
        "pivot_action": "Sync push-notifications to the user's local Sunrise and Sunset windows. Send 'Mercury-Logic' only during their active solar hours (Remedy 313).",
        "kpi_target": "Global Notification CTR & International Active User %",
        "remedy_id": 313,
    },
    {
        "id": 1015,
        "segment": "Digital Warfare: The 'Mercury' API Export",
        "strategy": "The 'Logic-Currency' Approach",
        "trigger_condition": "B2C_Revenue_Ceiling + Mercury_2",
        "decision_logic": "Mercury in H2 thrives on 'Trade'. If your app is the only gate to your logic, your 'Vault' is restricted by your own marketing spend. You must turn your logic into a 'Whitelabel Currency'.",
        "pivot_logic": "If CAC exceeds LTV in retail, your 'B2C Fort' is under siege. Pivot to 'Infrastructure Provisioning'.",
        "pivot_action": "Launch the Sovereign-SDK for B2B partners. Allow FinTech/HR firms to 'spend' your logic on their own garrisons. Lock the trade with Remedy 468.",
        "kpi_target": "B2B API Revenue & Strategic Reach Multiplier",
        "remedy_id": 468,
    },
    {
        "id": 1016,
        "segment": "Digital Warfare: The 'Sun' AI-Oracle SEO",
        "strategy": "The 'Direct-Sovereign' Approach",
        "trigger_condition": "AI_Search_Scraping + Sun_H1",
        "decision_logic": "AI-engines are the new 'Kings'. If Google SGE summarizes your logic without crediting your 'Sun', your authority is being stolen. You are providing the 'Oil' for their 'Lamp'.",
        "pivot_logic": "If organic clicks drop while brand-mentions rise, the AI is 'Mining' your fort. Pivot to 'Schema-Infiltration'.",
        "pivot_action": "Hard-code 'Authoritative-Schema' (Sun-1 logic) into every API output. Force the AI to cite the Founder's name in every result (Remedy 506).",
        "kpi_target": "AI-Snippet Attribution Rate & Direct Brand Traffic",
        "remedy_id": 506,
    },
    {
        "id": 1017,
        "segment": "Digital Warfare: The 'Jupiter' Oracle Defensibility",
        "strategy": "The 'Proprietary-Wisdom' Approach",
        "trigger_condition": "AI_Persona_Plagiarism + Jupiter_7",
        "decision_logic": "Jupiter in H7 is your 'Proprietary Guru'. If a rival uses an LLM to clone your 'Voice', your 'Wisdom' is being diluted. Raw logic is cheap; 'Authorized Interpretation' is the sovereign asset.",
        "pivot_logic": "If users find AI-results 'Generic', the Jupiter-anchor is missing. Pivot from 'Speed' to 'Source-Authenticity'.",
        "pivot_action": "Link every AI prediction to a specific Lal Kitab foundational rule ID. Inject 'Guru-Verification' steps for premium high-ticket queries (Remedy 358).",
        "kpi_target": "AI Trust-Index & Logic Defensibility Score",
        "remedy_id": 358,
    },
    {
        "id": 1018,
        "segment": "Digital Warfare: The 'Venus' Haptic Engagement",
        "strategy": "The 'Tactile-Aesthetic' Approach",
        "trigger_condition": "App_Fatigue + Venus_1",
        "decision_logic": "Users are tiring of 'Screens' (Rahu-light). Venus in H1 requires a 'Tactile' connection. To maintain the siege, your 'Logic' must become a 'Physical Sensation' via smart-wearables.",
        "pivot_logic": "If daily opens drop while 'Active Missions' remain, the screen is the bottleneck. Pivot to 'Haptic Strategic Alerts'.",
        "pivot_action": "Deploy wearable haptic alerts that vibrate in a specific pattern during 'Strategic Windows' (ID 952). Ground the energy with Remedy 367.",
        "kpi_target": "Haptic Engagement Rate & Ritual Completion %",
        "remedy_id": 367,
    },
    {
        "id": 1019,
        "segment": "Digital Warfare: The 'Ketu' Distress SEO",
        "strategy": "The 'Shadow-Intent' Approach",
        "trigger_condition": "High_CAC_on_Volume_Keywords + Ketu_H8",
        "decision_logic": "Rivals own the 'Sun' (High-volume) keywords. Ketu in H8 governs the 'Subconscious Distress'. You must capture users in their 'Crisis-Shadows' when they search for failure and betrayal.",
        "pivot_logic": "If direct ad ROI is negative, the market is too 'Polite'. Pivot to 'Negative-Sentiment' SEO.",
        "pivot_action": "Identify 108 distress-keywords (e.g. 'Business Liquidation Help'). Build 'Rescue-Fort' pages offering the Ketu-8 solution (Remedy 366).",
        "kpi_target": "Blue-Ocean ROI & Distress-Query Conversion Rate",
        "remedy_id": 366,
    },
    {
        "id": 1020,
        "segment": "Digital Warfare: The 'Mars' Disruptive Blitz",
        "strategy": "The 'Market-Absorption' Approach",
        "trigger_condition": "Rival_Market_Monopoly + Mars_1",
        "decision_logic": "A rival 'King' is blocking your Sun. Mars in H1 demands a 'Shock'. You must launch a 'Mercury-Logic' so disruptive it forces their 'Garrison' (Users) to defect to your fort instantly.",
        "pivot_logic": "If a frontal assault (Ads) fails, use 'Rahu-Shadow' tactics on their churn-points. Pivot to 'Aggressive Amnesty'.",
        "pivot_action": "Launch the 'Great Migration' campaign. Offer a 3-month 'Premium Amnesty' for any user defecting from a rival. Apply the Mars-fire (Remedy 310).",
        "kpi_target": "Rival-to-Empire Migration % & Market Share Delta",
        "remedy_id": 310,
    },
]


def _stamp(r: dict) -> dict:
    r["science_id"]      = SCIENCE_ID
    r["approval_status"] = APPROVAL
    r["ingested_at"]     = datetime.now(timezone.utc).isoformat()
    return r


def main():
    parser = argparse.ArgumentParser(description="Strategist patch v2: IDs 1011-1020 + 1126-1137")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL", ""))
    parser.add_argument("--db-name",   default=os.environ.get("DB_NAME", "horoscope_db"))
    parser.add_argument("--dry-run",   action="store_true", default=False)
    args = parser.parse_args()

    records = [_stamp(dict(r)) for r in PATCH_RECORDS]
    print(f"[INFO] Patch records: {len(records)}")
    for r in records:
        print(f"  ID {r['id']:4d}  {r['segment'][:60]}")

    if args.dry_run:
        print(f"\n[DRY-RUN] Would upsert {len(records)} records into knowledge_rules")
        print("[DRY-RUN] Sample (first record):")
        print(json.dumps(records[0], indent=2, default=str))
        return

    if not args.mongo_url:
        print("[ERROR] --mongo-url required", file=sys.stderr)
        sys.exit(1)

    from pymongo import MongoClient, UpdateOne

    client = MongoClient(args.mongo_url)
    db     = client[args.db_name]
    coll   = db.knowledge_rules

    ops = [
        UpdateOne(
            {"id": r["id"], "science_id": SCIENCE_ID},
            {"$set": r},
            upsert=True,
        )
        for r in records
    ]
    result = coll.bulk_write(ops, ordered=False)
    print(f"[OK] Upserted {result.upserted_count} new, modified {result.modified_count} existing")
    client.close()


if __name__ == "__main__":
    main()
