#!/usr/bin/env python3
"""inspect_bphs_vol2_phase1_flagged.py

Inspects and triages BPHS Vol 2 Phase 1 rules (Ch47, Ch53-58).
These rules were migrated from EverydayHoroscope → horoscope_db and have
confirmed batch IDs. Rule IDs use the R-BPHS[chapter]-* scheme.

  Ch47  bphs-ch47-dasha-20260416   R-BPHS47-*   (Sun MD + Antardasas)
  Ch53  bphs-ch53-dasha-20260417   R-BPHS53-*   (Moon MD + Antardasas)
  Ch54  bphs-ch54-dasha-20260417   R-BPHS54-*   (Mars MD + Antardasas)
  Ch55  bphs-ch55-dasha-20260417   R-BPHS55-*   (Rahu MD + Antardasas)
  Ch56  bphs-ch56-dasha-20260418   R-BPHS56-*   (Jupiter MD + Antardasas)
  Ch57  bphs-ch57-dasha-20260419   R-BPHS57-*   (Saturn MD + Antardasas)
  Ch58  bphs-ch58-dasha-20260419   R-BPHS58-*   (Mercury MD + Antardasas)

Excludes: deprecated rules (superseded by re-ingest passes).
Total active: ~1,400 rules.

Three-bucket triage:
  Bucket A -- Truncation artifact only (summary short, detailed OK)
              → patch to auto_approved
  Bucket B -- Validator doctrinal error (validator applied wrong standard)
              → patch to PHR + validator_error:true
  Bucket C -- Genuine issue (fabrication, formula conflict, factual error,
              extreme outcome, real contradiction)
              → API validator re-run, then PDF read or GAI if needed

Optional API validator re-run on Bucket C (--validate-bucket-c):
  Uses claude-haiku-4-5 (fast + cheap) to get fresh validation opinion
  on each Bucket C rule before deciding PDF-read vs GAI queue.
  Requires ANTHROPIC_API_KEY env var.

Usage:
  # Inspect only (no API calls):
  MONGO_URL=<url> python3 backend/scripts/inspect_bphs_vol2_phase1_flagged.py

  # Inspect + API validator on Bucket C:
  MONGO_URL=<url> python3 backend/scripts/inspect_bphs_vol2_phase1_flagged.py \\
    --validate-bucket-c

  # Limit API validation to first N Bucket C rules (cost control):
  MONGO_URL=<url> python3 backend/scripts/inspect_bphs_vol2_phase1_flagged.py \\
    --validate-bucket-c --validate-limit 30

  # Override mongo url via CLI (optional, env var preferred):
  python3 backend/scripts/inspect_bphs_vol2_phase1_flagged.py \\
    --mongo-url "$MONGO_URL"
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# ── Target batches (migrated from EverydayHoroscope → horoscope_db) ──────────
BATCH_IDS = [
    "bphs-ch47-dasha-20260416",
    "bphs-ch53-dasha-20260417",
    "bphs-ch54-dasha-20260417",
    "bphs-ch55-dasha-20260417",
    "bphs-ch56-dasha-20260418",
    "bphs-ch57-dasha-20260419",
    "bphs-ch58-dasha-20260419",
]

CHAPTER_LABELS = {
    "bphs-ch47-dasha-20260416": "Ch47 (Sun MD)",
    "bphs-ch53-dasha-20260417": "Ch53 (Moon MD)",
    "bphs-ch54-dasha-20260417": "Ch54 (Mars MD)",
    "bphs-ch55-dasha-20260417": "Ch55 (Rahu MD)",
    "bphs-ch56-dasha-20260418": "Ch56 (Jupiter MD)",
    "bphs-ch57-dasha-20260419": "Ch57 (Saturn MD)",
    "bphs-ch58-dasha-20260419": "Ch58 (Mercury MD)",
}

LOG_DIR = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")

# ── Bucket B patterns (known validator doctrinal errors) ──────────────────────
BUCKET_B_PATTERNS = [
    "natural malefic",
    "natural benefic",
    "upachaya",
    "moon in cancer",
    "sun in leo",
    "moolatrikona",
    "moola trikona",
    "exalt",
    "debili",
    "yogakaraka",
    "yoga karaka",
    "kalachakra",
    "chara dasa",
    "vimshottari",
    "antardasas",
    "dasa lord",
]

# ── Bucket C patterns (likely genuine issues) ─────────────────────────────────
BUCKET_C_PATTERNS = [
    "fabricat",
    "invented",
    "not found in source",
    "no source",
    "extreme",
    "death",
    "formula conflict",
    "factual error",
    "non-standard",
    "contradicts",
    "contradiction",
    "not standard",
    "unverified",
]

# ── API validator prompt ───────────────────────────────────────────────────────
VALIDATOR_SYSTEM = """You are an expert Vedic astrology knowledge validator specialising in BPHS (Brihat Parashara Hora Shastra), specifically the Santhanam English translation Vol 2 (Chapters 47-60).

Your task: evaluate whether a KE rule accurately reflects BPHS doctrine.

Respond ONLY with valid JSON:
{
  "verdict": "valid" | "validator_error" | "genuine_issue" | "uncertain",
  "confidence": 0.0-1.0,
  "reason": "one concise sentence",
  "bucket": "B" | "C" | "?"
}

verdict meanings:
  valid          - rule content matches BPHS doctrine; original flag was a validator error
  validator_error - rule content is correct BPHS but validator applied wrong standard (→ Bucket B)
  genuine_issue  - rule content appears to be fabricated, wrong, or not in BPHS source (→ Bucket C)
  uncertain      - cannot determine without the physical text; recommend PDF read"""

VALIDATOR_USER_TEMPLATE = """BPHS Vol 2 rule from Chapter {chapter}:

rule_id: {rule_id}
summary: {summary}
detailed: {detailed}
condition: {condition}
original_flag: {flag_reason}

Is this rule content consistent with BPHS Vol 2 Santhanam translation?"""


class _Tee:
    def __init__(self, log_path: Path):
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log = open(log_path, "w", encoding="utf-8")
        self._stdout = sys.__stdout__

    def write(self, data: str) -> None:
        self._stdout.write(data); self._stdout.flush()
        self._log.write(data); self._log.flush()

    def flush(self) -> None:
        self._stdout.flush(); self._log.flush()

    def close(self) -> None:
        self._log.close()


def _flag_text(rule: dict) -> str:
    """Extract all flag text from a rule into a single lowercased string."""
    parts = []
    val = rule.get("validation") or {}
    if isinstance(val, dict):
        for k in ("flag_reason", "flag_note", "issues", "note", "quality_note"):
            parts.append(str(val.get(k, "") or ""))
    parts.append(str(rule.get("flag_reason", "") or ""))
    parts.append(str(rule.get("flag_note", "") or ""))
    return " ".join(parts).lower()


def classify(rule: dict) -> str:
    """Return 'A', 'B', or 'C' bucket classification."""
    combined = _flag_text(rule)
    interp   = rule.get("interpretation") or {}
    detailed = str(interp.get("detailed", "") or "")
    summary  = str(interp.get("summary", "") or "")

    # Bucket A: summary very short, detailed OK, no issue signals
    if (len(summary) < 30 and len(detailed) > 80
            and not any(p in combined for p in BUCKET_C_PATTERNS)
            and not any(p in combined for p in BUCKET_B_PATTERNS)):
        return "A"

    # Bucket B: validator doctrinal error signals
    if any(p in combined for p in BUCKET_B_PATTERNS):
        return "B"

    return "C"


def call_validator(client, rule: dict) -> dict:
    """Call claude-haiku-4-5 to validate a Bucket C rule. Returns verdict dict."""
    interp   = rule.get("interpretation") or {}
    val      = rule.get("validation") or {}
    flag_txt = (val.get("flag_reason") or val.get("flag_note") or
                val.get("quality_note") or rule.get("flag_reason") or "")
    chapter  = rule.get("source_chapter", rule.get("rule_id", "?").split("-")[1]
                        if "-" in rule.get("rule_id", "") else "?")

    prompt = VALIDATOR_USER_TEMPLATE.format(
        chapter    = chapter,
        rule_id    = rule.get("rule_id", "?"),
        summary    = str(interp.get("summary", "") or "")[:400],
        detailed   = str(interp.get("detailed", "") or "")[:800],
        condition  = json.dumps(rule.get("condition", {}), ensure_ascii=False)[:300],
        flag_reason = str(flag_txt)[:400],
    )

    try:
        resp = client.messages.create(
            model      = "claude-haiku-4-5",
            max_tokens = 256,
            system     = VALIDATOR_SYSTEM,
            messages   = [{"role": "user", "content": prompt}],
        )
        text = resp.content[0].text.strip()
        # Extract JSON from response (may be wrapped in ```json ... ```)
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)
    except Exception as exc:
        return {"verdict": "uncertain", "confidence": 0.0,
                "reason": f"API error: {exc}", "bucket": "?"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url",        default=os.environ.get("MONGO_URL", ""),
                        help="MongoDB URL (default: MONGO_URL env var)")
    parser.add_argument("--db-name",          default="horoscope_db")
    parser.add_argument("--validate-bucket-c", action="store_true",
                        help="Run API validator on Bucket C rules")
    parser.add_argument("--validate-limit",   type=int, default=0,
                        help="Max Bucket C rules to validate (0=all)")
    parser.add_argument("--api-key",          default=os.environ.get("ANTHROPIC_API_KEY", ""))
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: MONGO_URL env var not set and --mongo-url not provided.")
        raise SystemExit(1)

    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"inspect_bphs_vol2_phase1_flagged_{ts}.log"
    tee      = _Tee(log_path)
    sys.stdout = tee

    print("=" * 70)
    print(f"  LOG FILE: {log_path}")
    print("=" * 70)
    print()
    print("BPHS Vol 2 Phase 1 -- Flagged Rules Inspect & Triage")
    print(f"Target  : {len(BATCH_IDS)} batches (Ch47, Ch53-58) in horoscope_db")
    print(f"Excludes: deprecated rules (superseded by re-ingest passes)")
    print(f"API val : {'YES (Bucket C)' if args.validate_bucket_c else 'NO'}")
    print()

    try:
        from pymongo import MongoClient
    except ImportError:
        print("pymongo required."); raise SystemExit(1)

    client_mongo = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)
    col = client_mongo[args.db_name]["interpretation_rules"]

    # ── Base query: known batch IDs, excluding deprecated ─────────────────────
    base_query = {
        "source.batch_id": {"$in": BATCH_IDS},
        "approval_status": {"$ne": "deprecated"},
    }

    # ── Overall status breakdown ──────────────────────────────────────────────
    print("── BPHS Vol 2 Phase 1 -- Active Rules by Status ─────────────────────")
    total_active = col.count_documents(base_query)
    print(f"  Total active rules (excl. deprecated) : {total_active}")
    print()
    for status in ["auto_approved", "pending_human_review", "pending_review",
                   "flagged", "rejected"]:
        n = col.count_documents({**base_query, "approval_status": status})
        marker = "  ← triage target" if status == "flagged" and n > 0 else ""
        print(f"  {status:<30} {n}{marker}")

    # Deprecated count (info only)
    depr_total = col.count_documents({"source.batch_id": {"$in": BATCH_IDS},
                                      "approval_status": "deprecated"})
    print(f"  {'deprecated (excl.)':<30} {depr_total}  (not triaged)")
    print()

    # ── Per-batch breakdown ────────────────────────────────────────────────────
    print("── Per-Batch Active Breakdown ────────────────────────────────────────")
    print(f"  {'Batch':<40} {'Active':<7} {'AA':<6} {'PHR':<6} {'FLAG':<6}")
    print("  " + "─" * 60)
    for bid in BATCH_IDS:
        q_bid = {"source.batch_id": bid, "approval_status": {"$ne": "deprecated"}}
        tot   = col.count_documents(q_bid)
        aa    = col.count_documents({**q_bid, "approval_status": "auto_approved"})
        phr   = col.count_documents({**q_bid, "approval_status": "pending_human_review"})
        fl    = col.count_documents({**q_bid, "approval_status": "flagged"})
        label = CHAPTER_LABELS.get(bid, bid)
        marker = " ⚠️" if fl > 0 else ""
        print(f"  {label:<40} {tot:<7} {aa:<6} {phr:<6} {fl:<6}{marker}")
    print()

    # ── Chapter breakdown ─────────────────────────────────────────────────────
    print("── Chapter Breakdown (flagged only) ─────────────────────────────────")
    flagged_query = {**base_query, "approval_status": "flagged"}
    flagged_all   = list(col.find(
        flagged_query,
        {"rule_id": 1, "source_chapter": 1, "source": 1, "validation": 1,
         "flag_reason": 1, "flag_note": 1,
         "interpretation.detailed": 1, "interpretation.summary": 1,
         "interpretation.tags": 1, "condition": 1, "_id": 0},
    ).sort("rule_id", 1))

    print(f"  Total flagged : {len(flagged_all)}")
    print()

    # Chapter distribution (use batch_id → label)
    chapter_counts: dict[str, int] = {}
    for r in flagged_all:
        bid = (r.get("source") or {}).get("batch_id", "") or r.get("source_chapter", "unknown")
        ch  = CHAPTER_LABELS.get(bid, bid)
        chapter_counts[ch] = chapter_counts.get(ch, 0) + 1
    for ch, n in sorted(chapter_counts.items()):
        print(f"    {ch:<35} {n} flagged")
    print()

    # ── Triage classification ─────────────────────────────────────────────────
    buckets: dict[str, list[dict]] = {"A": [], "B": [], "C": []}
    for rule in flagged_all:
        b = classify(rule)
        buckets[b].append(rule)

    print("── Triage Summary ───────────────────────────────────────────────────")
    print(f"  Bucket A (truncation → auto_approved) : {len(buckets['A'])}")
    print(f"  Bucket B (validator error → PHR)      : {len(buckets['B'])}")
    print(f"  Bucket C (genuine issue → validate)   : {len(buckets['C'])}")
    print()

    # ── Bucket A detail ───────────────────────────────────────────────────────
    if buckets["A"]:
        print("─" * 70)
        print("BUCKET A -- Truncation artifacts (auto_approved)")
        print("─" * 70)
        for r in buckets["A"]:
            interp = r.get("interpretation") or {}
            print(f"  {r['rule_id']}")
            print(f"    summary  : {str(interp.get('summary',''))[:100]}")
            print(f"    detailed : {str(interp.get('detailed',''))[:100]}")
            print()

    # ── Bucket B detail ───────────────────────────────────────────────────────
    if buckets["B"]:
        print("─" * 70)
        print("BUCKET B -- Validator doctrinal errors (PHR + validator_error:true)")
        print("─" * 70)
        for r in buckets["B"]:
            interp = r.get("interpretation") or {}
            val    = r.get("validation") or {}
            note   = (val.get("flag_reason") or val.get("flag_note") or
                      val.get("quality_note") or r.get("flag_reason") or "")
            print(f"  {r['rule_id']}")
            print(f"    summary  : {str(interp.get('summary',''))[:120]}")
            if note:
                print(f"    flag     : {str(note)[:200]}")
            print()

    # ── Bucket C detail ───────────────────────────────────────────────────────
    if buckets["C"]:
        print("─" * 70)
        print("BUCKET C -- Genuine issues (API validator → PDF/GAI queue)")
        print("─" * 70)
        for r in buckets["C"]:
            interp = r.get("interpretation") or {}
            val    = r.get("validation") or {}
            note   = (val.get("flag_reason") or val.get("flag_note") or
                      val.get("quality_note") or r.get("flag_reason") or "")
            print(f"  {r['rule_id']}")
            print(f"    summary  : {str(interp.get('summary',''))[:130]}")
            print(f"    detailed : {str(interp.get('detailed',''))[:130]}")
            if note:
                print(f"    flag     : {str(note)[:250]}")
            print()

    # ── API Validator pass on Bucket C ────────────────────────────────────────
    api_results: list[dict] = []
    if args.validate_bucket_c and buckets["C"]:
        if not args.api_key:
            print("── API Validator: SKIPPED (no ANTHROPIC_API_KEY) ────────────────────")
        else:
            try:
                import anthropic
                client_ai = anthropic.Anthropic(api_key=args.api_key)
            except ImportError:
                print("── API Validator: SKIPPED (anthropic SDK not installed) ─────────────")
                client_ai = None

            if client_ai:
                to_validate = buckets["C"]
                if args.validate_limit > 0:
                    to_validate = to_validate[:args.validate_limit]

                print("─" * 70)
                print(f"API VALIDATOR -- claude-haiku-4-5 on {len(to_validate)} Bucket C rules")
                if args.validate_limit and args.validate_limit < len(buckets["C"]):
                    print(f"  (limited to first {args.validate_limit} of {len(buckets['C'])})")
                print("─" * 70)

                b_upgrade = 0   # Bucket C → B (validator error confirmed by AI)
                c_genuine = 0   # Bucket C stays C (genuine issue)
                uncertain = 0

                for i, rule in enumerate(to_validate, 1):
                    rule_id = rule.get("rule_id", "?")
                    result  = call_validator(client_ai, rule)
                    verdict = result.get("verdict", "uncertain")
                    conf    = result.get("confidence", 0.0)
                    reason  = result.get("reason", "")
                    ai_bucket = result.get("bucket", "?")

                    api_results.append({
                        "rule_id":    rule_id,
                        "verdict":    verdict,
                        "confidence": conf,
                        "reason":     reason,
                        "ai_bucket":  ai_bucket,
                    })

                    if verdict in ("valid", "validator_error"):
                        status_tag = "→ B (validator error)"
                        b_upgrade += 1
                    elif verdict == "genuine_issue":
                        status_tag = "→ C GENUINE"
                        c_genuine += 1
                    else:
                        status_tag = "→ UNCERTAIN (PDF/GAI)"
                        uncertain += 1

                    print(f"  [{i:03d}] {rule_id}")
                    print(f"         verdict={verdict} conf={conf:.2f}  {status_tag}")
                    print(f"         {reason}")
                    print()

                    # Rate limit: 1 req/s to stay well within limits
                    if i < len(to_validate):
                        time.sleep(1.0)

                print("─" * 70)
                print(f"API Validator summary:")
                print(f"  Validator errors (→ B)    : {b_upgrade}")
                print(f"  Genuine issues (→ C)      : {c_genuine}")
                print(f"  Uncertain (PDF/GAI queue) : {uncertain}")
                print()

    # ── Export Bucket C JSON ──────────────────────────────────────────────────
    if buckets["C"]:
        gai_path = LOG_DIR / f"bphs_vol2_phase1_bucket_c_{ts}.json"
        export   = []
        api_map  = {r["rule_id"]: r for r in api_results}
        for r in buckets["C"]:
            interp = r.get("interpretation") or {}
            val    = r.get("validation") or {}
            entry  = {
                "rule_id":    r["rule_id"],
                "chapter":    r.get("source_chapter", ""),
                "summary":    str(interp.get("summary", "") or ""),
                "detailed":   str(interp.get("detailed", "") or ""),
                "flag_reason": (val.get("flag_reason") or val.get("flag_note") or
                                val.get("quality_note") or r.get("flag_reason") or ""),
                "condition":  r.get("condition", {}),
                "tags":       interp.get("tags", []),
            }
            if r["rule_id"] in api_map:
                entry["api_verdict"] = api_map[r["rule_id"]]
            export.append(entry)

        gai_path.write_text(
            json.dumps(export, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"Bucket C JSON export: {gai_path}")
        print(f"  {len(export)} rules -- use for PDF read or GAI review")
        print()

    # ── Next steps ────────────────────────────────────────────────────────────
    print("=" * 70)
    print("NEXT STEPS:")
    if buckets["A"]:
        print(f"  1. Patch {len(buckets['A'])} Bucket A rules → auto_approved")
        print(f"     (build patch_bphs_vol2_phase1_bucket_a.py)")
    if buckets["B"]:
        print(f"  2. Patch {len(buckets['B'])} Bucket B rules → PHR + validator_error:true")
        print(f"     (build patch_bphs_vol2_phase1_bucket_b.py)")
    if buckets["C"]:
        b_upgrade_ids = [r["rule_id"] for r in api_results
                         if r.get("verdict") in ("valid", "validator_error")]
        c_genuine_ids = [r["rule_id"] for r in api_results
                         if r.get("verdict") == "genuine_issue"]
        uncertain_ids = [r["rule_id"] for r in api_results
                         if r.get("verdict") not in ("valid", "validator_error", "genuine_issue")]

        if b_upgrade_ids:
            print(f"  3a. {len(b_upgrade_ids)} Bucket C upgraded to B by API validator:")
            for rid in b_upgrade_ids[:10]:
                print(f"      {rid}")
            if len(b_upgrade_ids) > 10:
                print(f"      ... and {len(b_upgrade_ids)-10} more")
        if c_genuine_ids:
            print(f"  3b. {len(c_genuine_ids)} Bucket C confirmed genuine → PDF read:")
            for rid in c_genuine_ids[:10]:
                print(f"      {rid}")
        if uncertain_ids:
            print(f"  3c. {len(uncertain_ids)} uncertain → PDF read required")
        if not api_results:
            print(f"  3. Review {len(buckets['C'])} Bucket C rules via API validator,")
            print(f"     then PDF read or GAI for remaining genuine issues.")
            print(f"     Run with --validate-bucket-c to start API validation.")
    print()
    print(f"Log saved: {log_path}")

    client_mongo.close()


if __name__ == "__main__":
    main()
