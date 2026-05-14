#!/usr/bin/env python3
"""
generate_signoff_review.py

Generates a co-founder sign-off review file for all mundane_jyotish rules
in auto_approved and pending_human_review status.

Output: backend/scripts/reports/mundane_signoff_review.md

Sections:
  Part A -- AUTO_APPROVED (~120+ rules)
    These are ready for immediate promotion to 'approved'.
    Co-founder reviews and confirms. No rewrites needed.

  Part B -- PENDING_HUMAN_REVIEW (~200+ rules)
    These need a specific decision per rule (language, source fidelity,
    deterministic framing, etc.). The PHR reason is shown for each.

  Part C -- FLAGGED (1 genuine open flag)
    mehta-ch10-aries-1-degree-conjunction-paradigm-shift
    Needs Mehta Ch10 source verification before decision.

Usage:
  python3 backend/scripts/generate_signoff_review.py --mongo-url "$MONGO_URL"

  Output file: backend/scripts/reports/mundane_signoff_review.md
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient

REPORT_PATH = "backend/scripts/reports/mundane_signoff_review.md"

BATCH_LABELS = {
    "mundane-interp-v1-20260505":       "v1  -- Gaur Ch1-5/10 + Raphael Ch23-25 + Mehta Ch11/19/21 + Gopal Ch4/5/8/14",
    "mundane-interp-v2-novel-20260508": "v2n -- Gopal Ch2 + Mehta Ch6 + Raphael Ch3 (novel rules only)",
    "mundane-interp-v3-20260506":       "v3  -- Gaur Ch2 (Celestial Council) + Mehta Ch13/20/26",
    "mundane-interp-v4-20260506":       "v4  -- Gaur Ch10 (price differentials) + Gaur Ch11 (eclipse)",
    "mundane-interp-v5-20260506":       "v5  -- Gopal Ch6 (mass death) + Gopal Ch7 (earthquakes)",
    "mundane-interp-v6-20260506":       "v6  -- Gopal Ch8 (war) + Gopal Ch9 (civil unrest)",
    "mundane-interp-v7-20260506":       "v7  -- Gopal Ch10/13/15 (career/governance/economy)",
    "mundane-interp-v8-20260506":       "v8  -- Eclipse severity/commodity rules",
    "mundane-interp-v9-20260506":       "v9  -- Sun/Moon transit + Solar ingress rules",
    "mundane-interp-v10-20260506":      "v10 -- Raphael western eclipse decanate",
    "mundane-interp-v11-20260506":      "v11 -- Historical validation / benchmark cases",
    "mundane-interp-v12-20260506":      "v12 -- Saturn transit price matrix",
    "mundane-interp-v13-20260506":      "v13 -- Koorma directional + Sanghatta Chakra + war gates",
    "mundane-interp-v14-20260506":      "v14 -- Macro-conjunctions + transit timing",
    "mundane-interp-v15-20260506":      "v15 -- Mars/Mercury/Jupiter/Venus/Rahu transits + Koorma kill-switch",
    "mundane-interp-v16-20260506":      "v16 -- Gaur Ch5/6/7 monsoon + crop + Sarvatobhadra trade",
    "mundane-interp-v17-20260507":      "v17 -- Gopal Ch3 (leadership auth) + Gopal Ch14 (markets)",
    "mundane-interp-v18-20260507":      "v18 -- Gopal Ch5 (oath chart) + Mehta Ch18 (election lagna)",
    "mundane-interp-v19-20260507":      "v19 -- Gopal Ch4 (election engine) + Mehta Ch22/23 (cabinet)",
    "mundane-interp-v20-20260508":      "v20 -- Gopal Ch10 (sports predictions)",
    "mundane-interp-v21-20260508":      "v21 -- Gopal Ch11 (rainfall / monsoon forecast)",
    "mundane-interp-v22-20260508":      "v22 -- Gopal Ch12 (India native profile)",
}

TRUNC = 300   # chars shown for condition / result in review


def trunc(s: str, n: int = TRUNC) -> str:
    s = (s or "").strip()
    return s[:n] + "..." if len(s) > n else s


def rule_block(r: dict, show_phr_reason: bool = False) -> str:
    lines = []
    lines.append(f"#### `{r['rule_id']}`")
    lines.append(f"**Title:** {r.get('title','')}")
    lines.append(f"**Source:** {r.get('source_chapter','')}")
    lines.append(f"**Severity:** {r.get('severity','?')} | **Checkable:** {r.get('checkable', False)} | **Weight:** {r.get('weight', 1.0)}")
    lines.append(f"**Condition:** {trunc(r.get('condition',''))}")
    lines.append(f"**Result:** {trunc(r.get('result',''))}")
    if r.get('notes'):
        lines.append(f"**Notes:** {trunc(r.get('notes',''), 200)}")
    if show_phr_reason:
        phr = r.get('validation', {}).get('flag_reason', '')
        if phr:
            lines.append(f"**PHR Reason:** {trunc(phr, 400)}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--output",    default=REPORT_PATH)
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC")

    # Fetch all mundane rules by status
    auto_approved = list(col.find(
        {"science_id": "mundane_jyotish", "approval_status": "auto_approved"},
        {"_id": 0}
    ).sort([("batch_id", 1), ("rule_id", 1)]))

    phr = list(col.find(
        {"science_id": "mundane_jyotish", "approval_status": "pending_human_review"},
        {"_id": 0}
    ).sort([("batch_id", 1), ("rule_id", 1)]))

    flagged = list(col.find(
        {"science_id": "mundane_jyotish", "approval_status": "flagged"},
        {"_id": 0}
    ).sort([("batch_id", 1), ("rule_id", 1)]))

    print(f"Auto-approved : {len(auto_approved)}")
    print(f"PHR           : {len(phr)}")
    print(f"Flagged       : {len(flagged)}")
    print(f"Writing → {args.output}")

    lines: list[str] = []

    # ── Header ────────────────────────────────────────────────────────────────
    lines += [
        "# Mundane Astrology -- Co-Founder Sign-Off Review",
        f"**Generated:** {now}",
        f"**Scope:** All `mundane_jyotish` rules requiring decision",
        "",
        "---",
        "",
        "## How to Use This File",
        "",
        "| Section | Rules | Action needed |",
        "|---|---|---|",
        f"| **Part A -- Auto-Approved** | {len(auto_approved)} | Confirm → promote to `approved` (or flag any concern) |",
        f"| **Part B -- Pending Human Review** | {len(phr)} | Read PHR reason → approve / rewrite / discard |",
        f"| **Part C -- Flagged** | {len(flagged)} | Source check needed before decision |",
        "",
        "**Promotion command** (after co-founder confirms a rule_id):",
        "```python",
        "col.update_one({'rule_id': 'RULE_ID'}, {'$set': {'approval_status': 'approved'}})",
        "```",
        "",
        "---",
        "",
    ]

    # ── Part A -- Auto-Approved ────────────────────────────────────────────────
    lines += [
        "# PART A -- Auto-Approved Rules",
        f"*{len(auto_approved)} rules passed all 3 validation stages without flags.*",
        "*Co-founder confirms → promote to `approved` → live to users.*",
        "",
    ]

    current_batch = None
    for r in auto_approved:
        bid = r.get("batch_id", "unknown")
        if bid != current_batch:
            current_batch = bid
            label = BATCH_LABELS.get(bid, bid)
            lines += [f"## {label}", ""]
        lines.append(rule_block(r, show_phr_reason=False))

    # ── Part B -- PHR ──────────────────────────────────────────────────────────
    lines += [
        "---",
        "",
        "# PART B -- Pending Human Review",
        f"*{len(phr)} rules escalated for co-founder decision.*",
        "*Each rule shows the PHR reason -- the specific concern that needs resolution.*",
        "",
        "**Decision options per rule:**",
        "- ✅ Approve as-is → `approved`",
        "- ✏️  Rewrite condition/result → resubmit for validation",
        "- ❌ Discard → `rejected`",
        "",
    ]

    current_batch = None
    for r in phr:
        bid = r.get("batch_id", "unknown")
        if bid != current_batch:
            current_batch = bid
            label = BATCH_LABELS.get(bid, bid)
            lines += [f"## {label}", ""]
        lines.append(rule_block(r, show_phr_reason=True))

    # ── Part C -- Flagged ──────────────────────────────────────────────────────
    lines += [
        "---",
        "",
        "# PART C -- Flagged (Genuine Open Issues)",
        f"*{len(flagged)} rule(s) with unresolved content flags.*",
        "",
    ]

    for r in flagged:
        flag_reason = r.get('validation', {}).get('flag_reason', 'n/a')
        lines.append(f"#### `{r['rule_id']}`")
        lines.append(f"**Title:** {r.get('title','')}")
        lines.append(f"**Source:** {r.get('source_chapter','')}")
        lines.append(f"**Flag:** {trunc(flag_reason, 500)}")
        lines.append(f"**Condition:** {trunc(r.get('condition',''))}")
        lines.append(f"**Result:** {trunc(r.get('result',''))}")
        lines.append("")

    # ── Footer ────────────────────────────────────────────────────────────────
    lines += [
        "---",
        "",
        "## Summary Counts",
        "",
        f"| Status | Count |",
        f"|---|---|",
        f"| auto_approved (ready to promote) | {len(auto_approved)} |",
        f"| pending_human_review | {len(phr)} |",
        f"| flagged (open) | {len(flagged)} |",
        f"| **Total under review** | **{len(auto_approved)+len(phr)+len(flagged)}** |",
        "",
        "*No rules reach live users until explicitly set to `approval_status: approved` via co-founder sign-off.*",
    ]

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n✅ Report written → {args.output}")
    print(f"   Part A: {len(auto_approved)} auto_approved")
    print(f"   Part B: {len(phr)} pending_human_review")
    print(f"   Part C: {len(flagged)} flagged")
    client.close()


if __name__ == "__main__":
    main()
