#!/usr/bin/env python3
"""
validate_remedies_batches.py
-----------------------------
Runs validate_rules.py for each of the 5 Remedies pending_review batches
in sequence. All output is logged to a timestamped file.

Batches (311 rules total):
  remedies-dhana-v1-20260510       100 rules
  remedies-crystals-v1-20260510    100 rules
  remedies-gemstones-v1-20260510    98 rules
  remedies-chakra-v1-20260510        7 rules
  remedies-mantras-v1-20260504       5 rules
  tba-ch15-v1-20260424               1 rule  (Text-Book of Astrology, correct format)

Usage (run from repo root):
    python3 backend/scripts/validate_remedies_batches.py

Requires:
    MONGO_URL env var set
    ANTHROPIC_API_KEY env var set (used by validate_rules.py → knowledge_validator)

Each batch produces its own log in KE_TEXTBOOK_DECODE/Dedup_Reports/.
This runner also saves a consolidated summary log in backend/scripts/logs/.
"""

from __future__ import annotations
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Log file setup
# ---------------------------------------------------------------------------
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
log_path = LOG_DIR / f"validate_remedies_batches_{timestamp}.log"

class Tee:
    def __init__(self, filepath: Path):
        self._file = open(filepath, "w", encoding="utf-8")
    def write(self, data: str):
        sys.__stdout__.write(data)
        self._file.write(data)
    def flush(self):
        sys.__stdout__.flush()
        self._file.flush()
    def close(self):
        self._file.close()

tee = Tee(log_path)
sys.stdout = tee

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  validate_remedies_batches.py")
print(f"  Run timestamp : {timestamp} UTC")
print(f"  Log file      : {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")
print()

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
MONGO_URL = os.environ.get("MONGO_URL")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not MONGO_URL:
    print("❌ MONGO_URL not set. Abort.")
    sys.exit(1)
if not ANTHROPIC_KEY:
    print("❌ ANTHROPIC_API_KEY not set. The validator will fail. Abort.")
    sys.exit(1)

print("✅ MONGO_URL        : set")
print("✅ ANTHROPIC_API_KEY: set")
print()

# ---------------------------------------------------------------------------
# Batches to validate -- in priority order (largest first)
# ---------------------------------------------------------------------------
BATCHES = [
    {"batch_id": "remedies-dhana-v1-20260510",    "expected_rules": 100, "science_id": "jyotish_remedies_dhana"},
    {"batch_id": "remedies-crystals-v1-20260510", "expected_rules": 100, "science_id": "jyotish_remedies_crystals"},
    {"batch_id": "remedies-gemstones-v1-20260510","expected_rules": 98,  "science_id": "jyotish_remedies_gemstones"},
    {"batch_id": "remedies-chakra-v1-20260510",   "expected_rules": 7,   "science_id": "jyotish_remedies_chakra"},
    {"batch_id": "remedies-mantras-v1-20260504",  "expected_rules": 5,   "science_id": "jyotish_remedies_mantras"},
    {"batch_id": "tba-ch15-v1-20260424",          "expected_rules": 1,   "science_id": "vedic_astrology"},
]
total_expected = sum(b["expected_rules"] for b in BATCHES)

print(f"Batches to validate: {len(BATCHES)}  |  Total rules: {total_expected}")
print()

# ---------------------------------------------------------------------------
# Run validate_rules.py for each batch
# ---------------------------------------------------------------------------
VALIDATOR = Path(__file__).parent / "validate_rules.py"
results: list[dict] = []

for i, batch in enumerate(BATCHES, 1):
    bid = batch["batch_id"]
    expected = batch["expected_rules"]

    print("─" * 60)
    print(f"  [{i}/{len(BATCHES)}] {bid}")
    print(f"  Expected: {expected} rules")
    print("─" * 60)

    cmd = [
        sys.executable,
        str(VALIDATOR),
        "--mongo-url", MONGO_URL,
        "--db-name", "horoscope_db",
        "--batch-id", bid,
        "--batch-size", "10",
    ]

    start = datetime.now(timezone.utc)
    # Capture both streams so they flow through the Tee (appear in log + terminal)
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env={**os.environ},
    )
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()

    # Route captured output through Tee so it lands in the log file
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print("--- stderr ---")
        print(proc.stderr, end="")
        print("--- end stderr ---")

    status = "✅ OK" if proc.returncode == 0 else f"❌ FAILED (exit {proc.returncode})"
    results.append({
        "batch_id": bid,
        "exit_code": proc.returncode,
        "elapsed_s": round(elapsed, 1),
    })

    print()
    print(f"  {status}  |  {elapsed:.0f}s")
    print()

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("═" * 60)
print("  SUMMARY")
print("═" * 60)
ok = sum(1 for r in results if r["exit_code"] == 0)
fail = len(results) - ok
print(f"  Batches run    : {len(results)}")
print(f"  Succeeded      : {ok}")
print(f"  Failed         : {fail}")
print()
for r in results:
    icon = "✅" if r["exit_code"] == 0 else "❌"
    print(f"  {icon}  {r['batch_id']:<40}  {r['elapsed_s']}s")
print()

if fail == 0:
    print("  All 6 batches validated. Run db_status_check.py to")
    print("  confirm the 311 pending_review rules have moved status.")
else:
    print("  Some batches failed. Check output above for errors.")
    print("  Re-run the failed batch individually:")
    for r in results:
        if r["exit_code"] != 0:
            print(f"    python3 backend/scripts/validate_rules.py \\")
            print(f"      --mongo-url \"$MONGO_URL\" \\")
            print(f"      --db-name horoscope_db \\")
            print(f"      --batch-id \"{r['batch_id']}\"")
            print()

print(f"╔══════════════════════════════════════════════════════════════╗")
print(f"  ✅ Runner complete")
print(f"  Log saved → {log_path}")
print(f"╚══════════════════════════════════════════════════════════════╝")

sys.stdout = sys.__stdout__
tee.close()
