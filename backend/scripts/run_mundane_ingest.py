"""
Mundane Astrology — Staged Ingest Runner
=========================================
Runs all clean motor-schema ingest scripts (v3–v15) in order against MongoDB.

Usage:
    MONGO_URL="mongodb+srv://<user>:<pass>@<cluster>/horoscope_db?retryWrites=true&w=majority" \
    python3 backend/scripts/run_mundane_ingest.py

    # Dry-run check only (default when MONGO_URL not set):
    python3 backend/scripts/run_mundane_ingest.py

Notes:
    - v1 and v2 use the old pymongo schema and are EXCLUDED from this runner.
      They require a separate migration decision.
    - All scripts use upsert — re-running is fully idempotent (safe to run multiple times).
    - MONGO_URL is read from the environment; falls back to localhost for local testing.
    - DB_NAME defaults to "horoscope_db" (matches production).
"""

import asyncio
import importlib
import importlib.util
import os
import sys
import types
from pathlib import Path

# Pre-import motor so the "if motor not in sys.modules" stub inside each
# ingest script never fires — without this, FakeClient silently absorbs all
# writes and nothing reaches MongoDB.
try:
    import motor.motor_asyncio as _motor_preload  # noqa: F401
except ImportError:
    print("ERROR: motor is not installed.  Run: pip3 install motor")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.environ.get("DB_NAME",   "horoscope_db")

SCRIPTS_DIR = Path(__file__).parent

# v3–v15 in order, both spec and interpretation files per version
SCRIPT_PAIRS = [
    ("ingest_mundane_engine_specs_v3.py",         "ingest_mundane_interpretation_v3.py"),
    ("ingest_mundane_engine_specs_v4.py",         "ingest_mundane_interpretation_v4.py"),
    ("ingest_mundane_engine_specs_v5.py",         "ingest_mundane_interpretation_v5.py"),
    ("ingest_mundane_engine_specs_v6.py",         "ingest_mundane_interpretation_v6.py"),
    ("ingest_mundane_engine_specs_v7.py",         "ingest_mundane_interpretation_v7.py"),
    ("ingest_mundane_engine_specs_v8.py",         "ingest_mundane_interpretation_v8.py"),
    ("ingest_mundane_engine_specs_v9.py",         "ingest_mundane_interpretation_v9.py"),
    ("ingest_mundane_engine_specs_v10.py",        "ingest_mundane_interpretation_v10.py"),
    ("ingest_mundane_engine_specs_v11.py",        "ingest_mundane_interpretation_v11.py"),
    ("ingest_mundane_engine_specs_v12.py",        "ingest_mundane_interpretation_v12.py"),
    ("ingest_mundane_engine_specs_v13.py",        "ingest_mundane_interpretation_v13.py"),
    ("ingest_mundane_engine_specs_v14.py",        "ingest_mundane_interpretation_v14.py"),
    ("ingest_mundane_engine_specs_v15.py",        "ingest_mundane_interpretation_v15.py"),
    ("ingest_mundane_engine_specs_v16.py",        "ingest_mundane_interpretation_v16.py"),
]

# Flatten to a single ordered list
ALL_SCRIPTS = [s for pair in SCRIPT_PAIRS for s in pair if s]

# ---------------------------------------------------------------------------

def load_and_patch(script_name: str) -> types.ModuleType:
    """
    Load a script as a module and patch its MONGO_URL, DB_NAME, and DRY_RUN
    globals before execution.
    """
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    spec = importlib.util.spec_from_file_location(script_name, script_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Override connection settings and disable dry-run
    mod.MONGO_URL = MONGO_URL
    mod.DB_NAME   = DB_NAME
    mod.DRY_RUN   = False

    return mod


async def run_all():
    found    = []
    missing  = []

    for name in ALL_SCRIPTS:
        path = SCRIPTS_DIR / name
        if path.exists():
            found.append(name)
        else:
            missing.append(name)

    if missing:
        print(f"\n⚠️  {len(missing)} script(s) not yet written (will be skipped):")
        for m in missing:
            print(f"    {m}")

    print(f"\n{'='*60}")
    print(f"Mundane Astrology Staged Ingest Runner")
    print(f"MONGO_URL : {MONGO_URL[:40]}{'...' if len(MONGO_URL) > 40 else ''}")
    print(f"DB_NAME   : {DB_NAME}")
    print(f"Scripts   : {len(found)} found, {len(missing)} pending")
    print(f"DRY_RUN   : False  (live write)")
    print(f"{'='*60}\n")

    confirm = input("Proceed with live write to MongoDB? [yes/N]: ").strip().lower()
    if confirm != "yes":
        print("Aborted.")
        return

    # Expose MONGO_URL / DB_NAME as environment variables so that v3-style
    # scripts that read os.environ["MONGO_URL"] directly also pick up the
    # correct connection string.
    os.environ["MONGO_URL"] = MONGO_URL
    os.environ["DB_NAME"]   = DB_NAME

    total_ok    = 0
    total_err   = 0
    skipped     = 0

    for name in ALL_SCRIPTS:
        path = SCRIPTS_DIR / name
        if not path.exists():
            print(f"  SKIP  {name}  (file not yet created)")
            skipped += 1
            continue

        print(f"  RUN   {name} ...", end=" ", flush=True)
        try:
            mod = load_and_patch(name)
            # v3-era scripts expose main(); v4+ expose run()
            entry = getattr(mod, "run", None) or getattr(mod, "main", None)
            if entry is None:
                raise AttributeError("script has no run() or main() function")
            await entry()
            print("✓")
            total_ok += 1
        except Exception as e:
            print(f"✗  ERROR: {e}")
            total_err += 1

    print(f"\n{'='*60}")
    print(f"Done.  OK: {total_ok}  |  Errors: {total_err}  |  Skipped: {skipped}")
    print(f"{'='*60}")

    if total_err:
        print("\nCheck error output above and re-run failed scripts individually.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_all())
