#!/usr/bin/env python3
"""
generate_lk_phr_review.py

Generates co-founder + GAI/NLM review report for all LK interpretation_rules
with approval_status = 'pending_human_review'.

Output: backend/scripts/reports/lk_phr_review_YYYYMMDD.md

Usage:
  python3 backend/scripts/generate_lk_phr_review.py
  python3 backend/scripts/generate_lk_phr_review.py --mongo-url "mongodb+srv://..."
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPORT_DIR  = Path(__file__).resolve().parent / "reports"
SCIENCE_ID  = "jyotish"
COLLECTION  = "interpretation_rules"
TRUNC       = 320

FLAG_CATEGORY_MAP = {
    "truncation": "Cat-1: Truncation False Flag (bulk approve)",
    "schema":     "Cat-2: Schema Precision Issue (structure fix needed)",
    "folk":       "Cat-3: Content Validity — Folk/Physiognomy Teaching",
    "varshaph":   "Cat-4: Varshaphalam Mechanic (LK-specific, non-classical frame)",
    "other":      "Cat-5: Other / Unknown",
}

CATEGORY_GUIDANCE = {
    "Cat-1: Truncation False Flag (bulk approve)": (
        "These were flagged because the validator received text cut off mid-word "
        "(buffer artifact during ingestion). Content is complete and source-confirmed. "
        "**Action: Bulk approve — no GAI/NLM consultation needed.**"
    ),
    "Cat-2: Schema Precision Issue (structure fix needed)": (
        "Content is source-faithful but the condition field is structurally imprecise "
        "(OR-logic not separated, ambiguous house ref, physiognomy mixed with planetary "
        "condition, duplicate entries, missing planet in planets_involved). "
        "**GAI/NLM question: How should this condition be expressed precisely?**"
    ),
    "Cat-3: Content Validity — Folk/Physiognomy Teaching": (
        "Validator (Haiku model) disputes these as 'non-classical Vedic'. They ARE extracted "
        "from LK source material. LK blends folk observation and physiognomy with astrology. "
        "**GAI/NLM question: Is this teaching present in the LK chapter source? Yes → Approve.**"
    ),
    "Cat-4: Varshaphalam Mechanic (LK-specific, non-classical frame)": (
        "Validator applied classical Vedic frame to LK's Varshaphalam-specific mechanics. "
        "These propagation rules are explicitly documented in Ch 28 source. "
        "**GAI/NLM question: Confirm mechanic is in Ch 28 source → Approve.**"
    ),
    "Cat-5: Other / Unknown": (
        "Flagged for reasons not matching the above categories. "
        "**GAI/NLM question: Review flag_reason and decide approve / rewrite / reject.**"
    ),
}


def _classify(flag_reason: str) -> str:
    r = (flag_reason or "").lower()
    if "truncat" in r:
        return "Cat-1: Truncation False Flag (bulk approve)"
    if any(k in r for k in ("schema", "precision", "or-logic", "ambiguous", "physiognomy mixed",
                             "planets_involved", "duplicate", "condition field")):
        return "Cat-2: Schema Precision Issue (structure fix needed)"
    if any(k in r for k in ("folk", "physiognomy", "mortality", "debilitation-clock",
                             "folk observation", "content validity", "source-fidelity",
                             "source-confidence", "classical attribution")):
        return "Cat-3: Content Validity — Folk/Physiognomy Teaching"
    if any(k in r for k in ("varshaphalam", "propagation", "influence priority",
                             "natal house", "enemy planet", "annual chart")):
        return "Cat-4: Varshaphalam Mechanic (LK-specific, non-classical frame)"
    return "Cat-5: Other / Unknown"


def trunc(s: str, n: int = TRUNC) -> str:
    s = (s or "").strip()
    return s[:n] + "…" if len(s) > n else s


def chapter_from_rule(rule_id: str) -> str:
    parts = rule_id.split("-")
    for i, p in enumerate(parts):
        if p.startswith("ch") and p[2:].isdigit():
            return p.upper()
    return "Unknown"


def rule_block(r: dict) -> str:
    rid     = r.get("rule_id", "?")
    chapter = chapter_from_rule(rid)
    summary = r.get("interpretation", {}).get("summary", "") or ""
    cond    = r.get("condition", {})
    cond_str = ""
    if isinstance(cond, dict):
        parts = []
        if cond.get("planet"):    parts.append(f"Planet: {cond['planet']}")
        if cond.get("house"):     parts.append(f"House: {cond['house']}")
        if cond.get("sign"):      parts.append(f"Sign: {cond['sign']}")
        if cond.get("strength"):  parts.append(f"Strength: {cond['strength']}")
        cond_str = " | ".join(parts) if parts else str(cond)[:120]
    elif isinstance(cond, str):
        cond_str = cond[:120]
    flag    = trunc(r.get("validation", {}).get("flag_reason", "n/a"), 280)
    lines = [
        f"#### `{rid}`  _{chapter}_",
        f"**Summary:** {trunc(summary, 200)}",
    ]
    if cond_str:
        lines.append(f"**Condition:** {cond_str}")
    lines += [
        f"**Flag reason:** {flag}",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate LK PHR review report")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL", ""))
    parser.add_argument("--db-name",   default=os.environ.get("DB_NAME", "horoscope_db"))
    parser.add_argument("--output",    default="")
    args = parser.parse_args()

    if not args.mongo_url:
        print("[ERROR] --mongo-url required (or set MONGO_URL env var)", file=sys.stderr)
        sys.exit(1)

    from pymongo import MongoClient
    client = MongoClient(args.mongo_url)
    col    = client[args.db_name][COLLECTION]

    rules = list(col.find(
        {
            "science_id": SCIENCE_ID,
            "approval_status": "pending_human_review",
            "source.batch_id": {"$regex": "^lalkitab-"},
        },
        {"_id": 0},
    ).sort("rule_id", 1))

    if not rules:
        print("[INFO] No pending_human_review rules found for science_id=jyotish_lk")
        client.close()
        return

    print(f"[INFO] {len(rules)} rules fetched")

    # ── Group by category then chapter ──────────────────────────────────────
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for r in rules:
        flag   = r.get("validation", {}).get("flag_reason", "")
        cat    = _classify(flag)
        by_cat[cat].append(r)

    # ── Build report ─────────────────────────────────────────────────────────
    now = datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC")
    lines: list[str] = [
        "# LK Interpretation Rules — PHR Review Report",
        f"Generated: {now}  ",
        f"Total rules: **{len(rules)}**  ",
        f"Collection: `{COLLECTION}` | `science_id: {SCIENCE_ID}` (Lal Kitab chapters)",
        "",
        "---",
        "",
        "## Quick Summary",
        "",
        "| Category | Count | Action |",
        "|---|---|---|",
    ]
    cat_order = list(FLAG_CATEGORY_MAP.values())
    for cat in cat_order:
        count = len(by_cat.get(cat, []))
        if count == 0:
            continue
        action = "Bulk approve" if "Cat-1" in cat else ("Schema fix" if "Cat-2" in cat else "GAI/NLM confirm")
        lines.append(f"| {cat} | {count} | {action} |")

    lines += ["", "---", ""]

    # ── Per-category sections ─────────────────────────────────────────────────
    for cat in cat_order:
        rules_in_cat = by_cat.get(cat, [])
        if not rules_in_cat:
            continue

        # Sub-group by chapter
        by_chapter: dict[str, list[dict]] = defaultdict(list)
        for r in rules_in_cat:
            by_chapter[chapter_from_rule(r.get("rule_id", ""))].append(r)

        lines += [
            f"## {cat}",
            f"**Count:** {len(rules_in_cat)}  ",
            "",
            f"> {CATEGORY_GUIDANCE[cat]}",
            "",
        ]

        for chapter in sorted(by_chapter.keys()):
            ch_rules = by_chapter[chapter]
            lines.append(f"### {chapter} ({len(ch_rules)} rules)")
            lines.append("")
            for r in ch_rules:
                lines.append(rule_block(r))

        lines.append("---")
        lines.append("")

    # ── Write file ────────────────────────────────────────────────────────────
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = Path(args.output) if args.output else REPORT_DIR / f"lk_phr_review_{date_str}.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Report written → {out_path}")
    client.close()


if __name__ == "__main__":
    main()
