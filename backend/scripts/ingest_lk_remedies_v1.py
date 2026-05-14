#!/usr/bin/env python3
"""
ingest_lk_remedies_v1.py -- Lal Kitab Remedies (IDs 308-668)

361 rules, science_id = "jyotish_lk_remedies"
Collection: horoscope_db.knowledge_rules

Architecture:
  Two source files merged with LAST OCCURRENCE WINS for duplicate IDs.
  Processing order: original file first → gap fill file second.
  Gap fill file's version of any ID overwrites the original.

Sub-ID Renumbering (decimal → integer):
  357.1→656, 357.2→657, 382.1→658, 382.2→659, 407.1→660,
  525.1→661, 525.2→662, 525.3→663, 525.4→664, 525.5→665,
  615.1→666, 615.2→667, 615.3→668
  All renumbered records get:  record_type = "supplementary", parent_id = <integer>

Conflict Gates (IDs 616-625):
  conflict_rule + safety_interlock → folded into ke_inference
  Format: "⚠️ SAFETY GATE: {safety_interlock}. {conflict_rule}."
  Extra field: record_type = "conflict_gate"
  NOT surfaced as standalone remedies in UI.

Destructive Merge (Version 2 wins):
  503-507  → Success Compass / Strategic Anchors (discard Inheritance Lock v1)
  484      → Emotional Peace / Matru Rin (keep v1 as anchor)
  485-499  → Reconciled Logic / Rin Matrix (discard Blood Collective v1)
  505-525  → Directional Realignment (discard Karmic/Ancestral v1)
  382.1→658, 382.2→659 → last occurrence only

Schema: 18-dimension LK grid
  id, focus_area, primary_planet, house, shadbala_threshold,
  strength_modifier, artificial_planet_fix, trigger_blind_planet,
  trigger_dormant, physical_object, ritual_act, prohibited_act,
  blood_relation_target, substitute_item, start_day, muhurta_rule,
  frequency_days, severity_scale, ke_inference

Standard workflow:
  python3 scripts/ingest_lk_remedies_v1.py --dry-run --save scripts/lk_remedies.json
  python3 scripts/ingest_lk_remedies_v1.py --upload scripts/lk_remedies.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

Post-ingest verification (run after --upload):
  See backend/scripts/LK_REMEDIES_TEST_PLAN.md -- Section 7

Sources:
  /Users/apple/Documents/Knowledge Engine_eBooks/
    Remedies + The Strategist/6. Lal Kitab_Remedies_JSON.md         (original)
    Remedies + The Strategist/Lal Kitab_Remedies_Gap Fill_Update from GAI.md (gap fill)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCIENCE_ID  = "jyotish_lk_remedies"
BOOK        = "Lal Kitab Remedies -- Knowledge Engine Library"
BOOK_ID     = "lk_remedies_v1"
CHAP_NAME   = "Lal Kitab Planetary Remedies"
BATCH_ID    = f"lk-remedies-v1-{datetime.now().strftime('%Y%m%d')}"
COLLECTION  = "knowledge_rules"   # NOT interpretation_rules -- LK uses its own collection

SOURCE_ORIGINAL = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/6. Lal Kitab_Remedies_JSON.md"
)
SOURCE_GAP_FILL = Path(
    "/Users/apple/Documents/Knowledge Engine_eBooks/"
    "Remedies + The Strategist/Lal Kitab_Remedies_Gap Fill_Update from GAI.md"
)

EXPECTED_TOTAL  = 361
EXPECTED_ID_MIN = 308
EXPECTED_ID_MAX = 668

# ─────────────────────────────────────────────────────────────────────────────
# SUB-ID RENUMBERING  (decimal → integer)
# ─────────────────────────────────────────────────────────────────────────────
# Maps string representation of decimal ID → new integer ID
SUB_ID_MAP: dict[str, int] = {
    "357.1": 656, "357.2": 657,
    "382.1": 658, "382.2": 659,
    "407.1": 660,
    "525.1": 661, "525.2": 662, "525.3": 663, "525.4": 664, "525.5": 665,
    "615.1": 666, "615.2": 667, "615.3": 668,
}

PARENT_ID_MAP: dict[int, int] = {
    656: 357, 657: 357,
    658: 382, 659: 382,
    660: 407,
    661: 525, 662: 525, 663: 525, 664: 525, 665: 525,
    666: 615, 667: 615, 668: 615,
}

SUPPLEMENTARY_IDS = set(PARENT_ID_MAP.keys())   # 656-668

# ─────────────────────────────────────────────────────────────────────────────
# CONFLICT GATE IDs  (616-625)
# ─────────────────────────────────────────────────────────────────────────────
CONFLICT_GATE_IDS = set(range(616, 626))   # 616, 617, ..., 625

# ─────────────────────────────────────────────────────────────────────────────
# IDs 611-615 -- HARDCODED (Q5 upgrade -- full 18-dim, injected at highest priority)
#
# Why hardcoded: The original LK source file has IDs 610-615 in an OLD schema
# (fields: ke_logic_trigger, trigger_logic, living_relative, collective_ritual, etc.)
# The gap fill file also skips these IDs. The authoritative 18-dim versions came
# from the GAI Q5 structural query response -- a third document not in the ingest
# pipeline. Hardcoding follows the same pattern as ingest_remedies_v1.py → ID 45.
#
# Source refs:
#   611-614: Lal Kitab Remedies_Claude Code 5 Structural Query Responses_GAI.md
#   615:     Provided by user 2026-05-09 (GAI Q5 equivalent for Karmic Rin parent)
# ─────────────────────────────────────────────────────────────────────────────
IDS_611_614_UPGRADED: list[dict] = [
    {
        "id": 611, "focus_area": "Ancestral Debt: The Priest's Curse",
        "primary_planet": "Jupiter", "house": 2,
        "shadbala_threshold": "< 300 Rupas", "strength_modifier": "Spiritual Bankruptcy",
        "artificial_planet_fix": "Sun + Moon",
        "trigger_blind_planet": False, "trigger_dormant": True,
        "physical_object": "Saffron + Yellow Cloth",
        "ritual_act": "Donate yellow sweets and saffron to a learned priest; apologize to elders",
        "prohibited_act": "Entering religious sites with leather items; disrespecting family Guru",
        "blood_relation_target": "Grandfather", "substitute_item": "Gram dal in a yellow pouch",
        "start_day": "Thursday", "muhurta_rule": "Morning",
        "frequency_days": 11, "severity_scale": 5,
        "ke_inference": ("Corrects 'The Priest's Curse' (H9 Mercury) causing lack of "
                         "internal wisdom and financial stagnation."),
    },
    {
        "id": 612, "focus_area": "Debt of Blood: The Brother's Curse",
        "primary_planet": "Mars", "house": 3,
        "shadbala_threshold": "< 360 Rupas", "strength_modifier": "Courage Collapse",
        "artificial_planet_fix": "Sun + Mercury",
        "trigger_blind_planet": False, "trigger_dormant": False,
        "physical_object": "Honey / Red Lentils",
        "ritual_act": "Gift honey and red lentils to a brother; drop red flowers in a cemetery",
        "prohibited_act": "Arguing over ancestral land or family weapons",
        "blood_relation_target": "Brother", "substitute_item": "Sweet bread distribution",
        "start_day": "Tuesday", "muhurta_rule": "Noon",
        "frequency_days": 1, "severity_scale": 4,
        "ke_inference": ("Caused by Saturn/Rahu in H3. Native lacks initiative and "
                         "suffers from chronic vitality issues."),
    },
    {
        "id": 613, "focus_area": "Debt of Land: The Earth's Rin",
        "primary_planet": "Saturn", "house": 4,
        "shadbala_threshold": "< 320 Rupas", "strength_modifier": "Vastu Debt",
        "artificial_planet_fix": "Mars + Mercury",
        "trigger_blind_planet": False, "trigger_dormant": True,
        "physical_object": "Almonds / Iron Nails",
        "ritual_act": "Bury 10 almonds in a dark corner of the home; do not consume them",
        "prohibited_act": "Keeping a South-facing entrance in a state of disrepair",
        "blood_relation_target": "Laborers", "substitute_item": "Mustard oil lamp under a Peepal tree",
        "start_day": "Saturday", "muhurta_rule": "After Sunset",
        "frequency_days": 43, "severity_scale": 4,
        "ke_inference": ("Caused by Rahu/Ketu in H4. Manifests as a stagnant home "
                         "where assets never grow."),
    },
    {
        "id": 614, "focus_area": "Debt of Speech: The Echo",
        "primary_planet": "Mercury", "house": 2,
        "shadbala_threshold": "< 310 Rupas", "strength_modifier": "Word Malfunction",
        "artificial_planet_fix": "Jupiter + Rahu",
        "trigger_blind_planet": False, "trigger_dormant": False,
        "physical_object": "Copper Coin with a Hole",
        "ritual_act": "Wear copper coin in a white thread; maintain silence for 2 hours daily",
        "prohibited_act": "Lying or using abusive language during family meal times",
        "blood_relation_target": "Sister / Daughter", "substitute_item": "Feeding whole Moong to birds",
        "start_day": "Wednesday", "muhurta_rule": "Morning",
        "frequency_days": 43, "severity_scale": 2,
        "ke_inference": ("Caused by Ketu in H2. Family members constantly misunderstand "
                         "each other; wealth drains through lawsuits."),
    },
    {
        "id": 615,
        "focus_area": "Karmic Debt: The Master Fallback (Proxy Shield)",
        "primary_planet": "Sun + Jupiter",
        "house": 1,
        "shadbala_threshold": "N/A",
        "strength_modifier": "General Protection",
        "artificial_planet_fix": "Artificial Moon Formation",
        "trigger_blind_planet": False,
        "trigger_dormant": True,
        "physical_object": "Silver Square + Gold Dot",
        "ritual_act": ("Wear a square piece of silver with a small gold dot in the center; "
                       "visit a generic ancestral shrine or old temple"),
        "prohibited_act": ("Denying food or water to a guest or traveler at your doorstep "
                           "during the cycle"),
        "blood_relation_target": "Father / Paternal Grandfather",
        "substitute_item": "Apply a mix of raw milk and saffron to the forehead daily",
        "start_day": "Sunday or Thursday",
        "muhurta_rule": "Sunrise",
        "frequency_days": 1,
        "severity_scale": 3,
        "ke_inference": ("The universal remedy to 'pause' active debts. By combining Sun (Gold) "
                         "and Moon (Silver), it creates a spiritual buffer allowing the native "
                         "to build strength for specific lineage rituals."),
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 18 MANDATORY SCHEMA FIELDS
# ─────────────────────────────────────────────────────────────────────────────
MANDATORY_18 = [
    "id", "focus_area", "primary_planet", "house", "shadbala_threshold",
    "strength_modifier", "artificial_planet_fix", "trigger_blind_planet",
    "trigger_dormant", "physical_object", "ritual_act", "prohibited_act",
    "blood_relation_target", "substitute_item", "start_day", "muhurta_rule",
    "frequency_days", "severity_scale", "ke_inference",
]


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE PARSER
# ─────────────────────────────────────────────────────────────────────────────

def _unescape_md(text: str) -> str:
    """Remove markdown formatting and fix invalid JSON escape sequences."""
    text = re.sub(r'\*+', '', text)
    text = (text
            .replace('\\[', '[').replace('\\]', ']')
            .replace('\\_', '_').replace('\\{', '{').replace('\\}', '}'))
    # Remove invalid JSON escapes (\< \> etc.)
    text = re.sub(r'\\(?!["\\/bfnrtu])', '', text)
    return text


def _normalize_id(raw_id) -> int | None:
    """Convert raw id (int, float, or string) to integer, applying SUB_ID_MAP for decimals.

    Returns None if the id cannot be resolved.
    """
    if isinstance(raw_id, int):
        return raw_id

    # Handle float like 357.1
    if isinstance(raw_id, float):
        key = f"{raw_id:.10g}"           # "357.1"
        # Truncate trailing zeros: "357.1000" → "357.1"
        key = key.rstrip('0').rstrip('.')
        if key in SUB_ID_MAP:
            return SUB_ID_MAP[key]
        # Plain integer stored as float (e.g., 400.0)
        if raw_id == int(raw_id):
            return int(raw_id)
        return None

    # Handle string like "357.1" or "357"
    if isinstance(raw_id, str):
        raw_id = raw_id.strip()
        if raw_id in SUB_ID_MAP:
            return SUB_ID_MAP[raw_id]
        try:
            f = float(raw_id)
            if f == int(f):
                return int(f)
            key = f"{f:.10g}".rstrip('0').rstrip('.')
            if key in SUB_ID_MAP:
                return SUB_ID_MAP[key]
        except ValueError:
            pass
    return None


def _to_bool(value) -> bool:
    """Normalize trigger_blind_planet / trigger_dormant to Python bool."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ('true', '1', 'yes')
    return bool(value)


def _to_int(value, default: int = 0) -> int:
    """Normalize frequency_days / severity_scale to int."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _extract_objects_from_text(raw: str) -> list[dict]:
    """Robust object-by-object scan. Handles broken arrays, bold formatting, last-occurrence wins.

    Returns records in file order (order matters for last-occurrence rule).
    """
    raw_entries: list[dict] = []
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(raw):
        obj_start = raw.find('{', pos)
        if obj_start == -1:
            break
        try:
            obj, end = decoder.raw_decode(raw, obj_start)
            if isinstance(obj, dict) and 'id' in obj:
                raw_entries.append(obj)
            pos = end
        except (json.JSONDecodeError, ValueError):
            pos = obj_start + 1
    return raw_entries


def _parse_file(path: Path) -> list[dict]:
    """Read and parse a source markdown file, normalizing IDs."""
    if not path.exists():
        print(f"  ⚠️  Source file not found: {path}")
        return []
    raw = path.read_text(encoding='utf-8', errors='replace')
    raw = _unescape_md(raw)
    return _extract_objects_from_text(raw)


def _load_and_merge() -> dict[int, dict]:
    """Load source files with priority order. Last occurrence wins.

    Priority (lowest → highest):
      1. Original file:      6. Lal Kitab_Remedies_JSON.md
      2. Gap fill file:      Lal Kitab_Remedies_Gap Fill_Update from GAI.md
      3. Hardcoded IDs 611-614: Q5 upgrade -- always wins (injected last)

    Returns: {normalized_id: entry_dict}
    """
    merged: dict[int, dict] = {}

    for source_path in [SOURCE_ORIGINAL, SOURCE_GAP_FILL]:
        raw_entries = _parse_file(source_path)
        for rec in raw_entries:
            raw_id  = rec.get('id')
            norm_id = _normalize_id(raw_id)
            if norm_id is None:
                continue
            rec = dict(rec)
            rec['id'] = norm_id
            merged[norm_id] = rec    # last occurrence wins

    # Inject hardcoded 611-614 Q5 upgrade LAST (highest priority)
    for rec in IDS_611_614_UPGRADED:
        merged[rec['id']] = dict(rec)

    return merged


# ─────────────────────────────────────────────────────────────────────────────
# CONFLICT GATE TRANSFORMATION
# ─────────────────────────────────────────────────────────────────────────────

def _transform_conflict_gate(entry: dict) -> dict:
    """Fold conflict_rule + safety_interlock into ke_inference for IDs 616-625."""
    entry = dict(entry)
    conflict_rule    = entry.pop('conflict_rule', '').strip()
    safety_interlock = entry.pop('safety_interlock', '').strip()

    # Build the composite ke_inference
    if safety_interlock and conflict_rule:
        ke = f"⚠️ SAFETY GATE: {safety_interlock}. {conflict_rule}."
    elif safety_interlock:
        ke = f"⚠️ SAFETY GATE: {safety_interlock}."
    elif conflict_rule:
        ke = f"⚠️ SAFETY GATE: {conflict_rule}."
    else:
        ke = entry.get('ke_inference', '⚠️ SAFETY GATE: See record for details.')

    entry['ke_inference'] = ke
    entry['record_type']  = "conflict_gate"
    return entry


# ─────────────────────────────────────────────────────────────────────────────
# SCHEMA VALIDATOR
# ─────────────────────────────────────────────────────────────────────────────

# Fields that conflict gates (616-625) are exempt from.
# Conflict gates encode procedural logic / safety interlocks -- they don't prescribe
# physical remedies, so all remedy-specific fields are not applicable.
# Only id, focus_area, primary_planet, triggers, severity_scale, ke_inference required.
CONFLICT_GATE_EXEMPT_FIELDS = {
    "house", "shadbala_threshold", "strength_modifier", "artificial_planet_fix",
    "physical_object", "ritual_act", "prohibited_act", "blood_relation_target",
    "substitute_item", "start_day", "muhurta_rule", "frequency_days",
}


def _validate_entry(entry: dict) -> list[str]:
    """Return list of validation errors. Empty list = valid.

    Conflict gates (616-625) are exempt from CONFLICT_GATE_EXEMPT_FIELDS
    because they encode logic/safety rules, not planetary prescriptions.
    """
    errors: list[str] = []
    rid = entry.get('id', '?')
    is_conflict_gate = rid in CONFLICT_GATE_IDS

    # 1. All 18 mandatory fields present (with conflict gate exemptions)
    for field in MANDATORY_18:
        if is_conflict_gate and field in CONFLICT_GATE_EXEMPT_FIELDS:
            continue
        if field not in entry:
            errors.append(f"ID {rid}: missing field '{field}'")

    # 2. id is integer
    if not isinstance(entry.get('id'), int):
        errors.append(f"ID {rid}: 'id' is not integer ({type(entry.get('id')).__name__})")

    # 3. id in expected range
    actual_id = entry.get('id')
    if isinstance(actual_id, int) and not (EXPECTED_ID_MIN <= actual_id <= EXPECTED_ID_MAX):
        errors.append(f"ID {rid}: out of range {EXPECTED_ID_MIN}-{EXPECTED_ID_MAX}")

    # 4. trigger_blind_planet must be bool
    if not isinstance(entry.get('trigger_blind_planet'), bool):
        errors.append(f"ID {rid}: 'trigger_blind_planet' must be bool")

    # 5. trigger_dormant must be bool
    if not isinstance(entry.get('trigger_dormant'), bool):
        errors.append(f"ID {rid}: 'trigger_dormant' must be bool")

    # 6. severity_scale must be int 1-5
    ss = entry.get('severity_scale')
    if not isinstance(ss, int) or not (1 <= ss <= 5):
        errors.append(f"ID {rid}: 'severity_scale' must be int 1-5 (got {ss!r})")

    # 7. frequency_days must be int
    if not isinstance(entry.get('frequency_days'), int):
        errors.append(f"ID {rid}: 'frequency_days' must be int")

    return errors


# ─────────────────────────────────────────────────────────────────────────────
# BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def _build_records() -> tuple[list[dict], list[str]]:
    """Build finalized MongoDB records. Returns (records, validation_errors)."""
    merged   = _load_and_merge()
    now      = datetime.now(timezone.utc).isoformat()
    records: list[dict] = []
    all_errors: list[str] = []

    for norm_id, entry in sorted(merged.items()):
        # ── Step 1: Conflict gate transformation ────────────────────────────
        if norm_id in CONFLICT_GATE_IDS:
            entry = _transform_conflict_gate(entry)

        # ── Step 2: Normalize boolean fields ────────────────────────────────
        entry['trigger_blind_planet'] = _to_bool(entry.get('trigger_blind_planet', False))
        entry['trigger_dormant']      = _to_bool(entry.get('trigger_dormant', False))

        # ── Step 3: Normalize numeric fields ────────────────────────────────
        entry['frequency_days'] = _to_int(entry.get('frequency_days', 0))
        entry['severity_scale'] = _to_int(entry.get('severity_scale', 1))
        # Clamp severity_scale to 1-5
        entry['severity_scale'] = max(1, min(5, entry['severity_scale']))

        # ── Step 4: Supplementary record tagging ────────────────────────────
        if norm_id in SUPPLEMENTARY_IDS:
            entry['record_type'] = "supplementary"
            entry['parent_id']   = PARENT_ID_MAP[norm_id]
        elif norm_id not in CONFLICT_GATE_IDS:
            entry.setdefault('record_type', "remedy")

        # ── Step 5: Schema validation ────────────────────────────────────────
        errors = _validate_entry(entry)
        all_errors.extend(errors)

        # ── Step 6: Assemble final MongoDB document ──────────────────────────
        record: dict = {
            # Core LK fields (18-dimension grid)
            "id":                    norm_id,
            "science_id":            SCIENCE_ID,
            "focus_area":            entry.get('focus_area', ''),
            "primary_planet":        entry.get('primary_planet', ''),
            "house":                 entry.get('house', 0),
            "shadbala_threshold":    entry.get('shadbala_threshold', ''),
            "strength_modifier":     entry.get('strength_modifier', ''),
            "artificial_planet_fix": entry.get('artificial_planet_fix', ''),
            "trigger_blind_planet":  entry['trigger_blind_planet'],
            "trigger_dormant":       entry['trigger_dormant'],
            "physical_object":       entry.get('physical_object', ''),
            "ritual_act":            entry.get('ritual_act', ''),
            "prohibited_act":        entry.get('prohibited_act', ''),
            "blood_relation_target": entry.get('blood_relation_target', ''),
            "substitute_item":       entry.get('substitute_item', ''),
            "start_day":             entry.get('start_day', ''),
            "muhurta_rule":          entry.get('muhurta_rule', ''),
            "frequency_days":        entry['frequency_days'],
            "severity_scale":        entry['severity_scale'],
            "ke_inference":          entry.get('ke_inference', ''),
            # Record type
            "record_type":           entry.get('record_type', 'remedy'),
            # Metadata
            "approval_status":       "pending_human_review",
            "batch_id":              BATCH_ID,
            "source": {
                "book":       BOOK,
                "book_id":    BOOK_ID,
                "batch_id":   BATCH_ID,
            },
            "created_at": now,
            "updated_at": now,
        }

        # Supplementary: add parent_id
        if norm_id in SUPPLEMENTARY_IDS:
            record['parent_id'] = PARENT_ID_MAP[norm_id]

        records.append(record)

    return records, all_errors


# ─────────────────────────────────────────────────────────────────────────────
# POST-INGEST VERIFICATION QUERIES  (printed after upload)
# ─────────────────────────────────────────────────────────────────────────────

VERIFY_QUERIES = """
Post-Ingest Verification Queries (run in MongoDB shell):

  // 1. Total count
  db.knowledge_rules.countDocuments({"science_id": "jyotish_lk_remedies"})
  // Expected: 361

  // 2. No decimal IDs
  db.knowledge_rules.find({"science_id": "jyotish_lk_remedies", "id": {$type: "double"}}).count()
  // Expected: 0

  // 3. No duplicate IDs
  db.knowledge_rules.aggregate([
    {$match: {"science_id": "jyotish_lk_remedies"}},
    {$group: {_id: "$id", count: {$sum: 1}}},
    {$match: {count: {$gt: 1}}}
  ])
  // Expected: []

  // 4. Conflict gates tagged
  db.knowledge_rules.countDocuments({"science_id": "jyotish_lk_remedies", "record_type": "conflict_gate"})
  // Expected: 10 (IDs 616-625)

  // 5. Supplementary records
  db.knowledge_rules.countDocuments({"science_id": "jyotish_lk_remedies", "id": {$gte: 656, $lte: 668}})
  // Expected: 13

  // 6. Destructive merge check -- ID 505 must be Directional, NOT Inheritance
  db.knowledge_rules.findOne({"science_id": "jyotish_lk_remedies", "id": 505}, {"focus_area": 1})
  // Expected: focus_area contains "Directional" -- FAIL if "Inheritance"

  // 7. Building ban conflict gate
  db.knowledge_rules.findOne({"science_id": "jyotish_lk_remedies", "id": 622}, {"record_type": 1, "ke_inference": 1})
  // Expected: record_type = "conflict_gate", ke_inference starts with "⚠️ SAFETY GATE"

  // 8. Mercury Solitary H10 supplementary record
  db.knowledge_rules.findOne({"science_id": "jyotish_lk_remedies", "id": 659})
  // Expected: primary_planet = "Mercury", house = 10, parent_id = 382
"""


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Ingest Lal Kitab Remedies (IDs 308-668) into MongoDB knowledge_rules.\n"
            "Gate 0: Schema validation runs automatically -- blocks upload on failure.\n\n"
            "  Step 1: python3 ingest_lk_remedies_v1.py --dry-run --save lk_remedies.json\n"
            "  Step 2: python3 ingest_lk_remedies_v1.py --upload lk_remedies.json "
            "--mongo-url $MONGO_URL"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--dry-run",    action="store_true",
                        help="Build and validate records; print report; do NOT touch MongoDB")
    parser.add_argument("--save",       metavar="FILE",
                        help="Save built records to JSON file (use with --dry-run)")
    parser.add_argument("--upload",     metavar="FILE",
                        help="Upload saved JSON file to MongoDB")
    parser.add_argument("--mongo-url",  default="", metavar="URL")
    parser.add_argument("--db-name",    default="horoscope_db")
    parser.add_argument("--force",      action="store_true",
                        help="Upload even if schema validation has warnings (never skip errors)")
    args = parser.parse_args()

    if not args.dry_run and not args.upload:
        parser.print_help()
        sys.exit(1)

    # ── DRY RUN ──────────────────────────────────────────────────────────────
    if args.dry_run:
        print(f"\n{'='*65}")
        print(f"  Lal Kitab Remedies -- Dry Run")
        print(f"  Batch ID:   {BATCH_ID}")
        print(f"  Science ID: {SCIENCE_ID}")
        print(f"  Collection: {COLLECTION}")
        print(f"{'='*65}")

        print("\n  Loading source files...")
        records, errors = _build_records()

        # ── ID range stats ──────────────────────────────────────────────────
        all_ids        = sorted(r['id'] for r in records)
        core_ids       = [i for i in all_ids if EXPECTED_ID_MIN <= i <= 615]
        conflict_ids   = [i for i in all_ids if 616 <= i <= 625]
        extended_ids   = [i for i in all_ids if 626 <= i <= 655]
        suppl_ids      = [i for i in all_ids if 656 <= i <= 668]

        print(f"\n  Record counts:")
        print(f"    Total:          {len(records):4d}  (expected {EXPECTED_TOTAL})")
        print(f"    Core 308-615:   {len(core_ids):4d}")
        print(f"    Conflict 616-625:{len(conflict_ids):4d}  (expected 10)")
        print(f"    Extended 626-655:{len(extended_ids):4d}  (expected 30)")
        print(f"    Suppl 656-668:  {len(suppl_ids):4d}  (expected 13)")

        # ── Record type breakdown ───────────────────────────────────────────
        from collections import Counter
        types: Counter = Counter(r['record_type'] for r in records)
        print(f"\n  By record_type:")
        for rt, cnt in sorted(types.items()):
            print(f"    {cnt:4d}  {rt}")

        # ── Boolean field check ─────────────────────────────────────────────
        non_bool_blind    = [r['id'] for r in records if not isinstance(r['trigger_blind_planet'], bool)]
        non_bool_dormant  = [r['id'] for r in records if not isinstance(r['trigger_dormant'], bool)]
        if non_bool_blind:
            print(f"\n  ⚠️  trigger_blind_planet non-bool: {non_bool_blind[:10]}")
        if non_bool_dormant:
            print(f"\n  ⚠️  trigger_dormant non-bool: {non_bool_dormant[:10]}")

        # ── Conflict gate check ─────────────────────────────────────────────
        cg_records = [r for r in records if r['id'] in CONFLICT_GATE_IDS]
        cg_ok      = all(r['ke_inference'].startswith("⚠️ SAFETY GATE") for r in cg_records)
        print(f"\n  Conflict gates (616-625): {len(cg_records)} records")
        print(f"    ke_inference format:  {'✅ All start with ⚠️ SAFETY GATE' if cg_ok else '❌ Format error'}")

        # ── Supplementary parent_id check ───────────────────────────────────
        suppl_records   = [r for r in records if r['id'] in SUPPLEMENTARY_IDS]
        suppl_with_pid  = [r for r in suppl_records if 'parent_id' in r]
        print(f"\n  Supplementary (656-668): {len(suppl_records)} records")
        print(f"    With parent_id:       {len(suppl_with_pid)}")

        # ── Destructive merge spot-checks ───────────────────────────────────
        print(f"\n  Destructive merge spot-checks:")
        id_505 = next((r for r in records if r['id'] == 505), None)
        if id_505:
            fa_505 = id_505.get('focus_area', '')
            ok_505 = "Directional" in fa_505 or "Geographical" in fa_505
            status = "✅ PASS" if ok_505 else "❌ FAIL -- Version 1 not overwritten!"
            print(f"    ID 505 focus_area: '{fa_505[:60]}' → {status}")
        else:
            print(f"    ID 505: ❌ MISSING")

        id_659 = next((r for r in records if r['id'] == 659), None)
        if id_659:
            planet_ok = id_659.get('primary_planet', '') == 'Mercury'
            house_ok  = id_659.get('house') == 10
            status = "✅ PASS" if (planet_ok and house_ok) else "❌ Check primary_planet/house"
            print(f"    ID 659 (Mercury H10): planet={id_659.get('primary_planet')}, "
                  f"house={id_659.get('house')} → {status}")
        else:
            print(f"    ID 659: ❌ MISSING (Mercury Solitary H10 supplementary)")

        # ── Schema validation summary ────────────────────────────────────────
        print(f"\n  Schema validation (Gate 0):")
        if errors:
            print(f"    ❌ {len(errors)} error(s) found:")
            for e in errors[:20]:
                print(f"       {e}")
            if len(errors) > 20:
                print(f"       ... and {len(errors) - 20} more")
            print(f"\n  ⛔ BLOCKED -- fix schema errors before upload")
        else:
            print(f"    ✅ All records pass schema validation")

        # ── Missing from expected range ─────────────────────────────────────
        found_set     = set(all_ids)
        expected_full = set(range(EXPECTED_ID_MIN, EXPECTED_ID_MAX + 1)) - set(range(669, 701))
        # (669-700 is the reserved buffer -- intentionally absent)
        missing_ids   = sorted(expected_full - found_set - set(range(669, 701)))
        if missing_ids:
            print(f"\n  ⚠️  IDs in range but missing from merge: {missing_ids[:20]}")
        else:
            print(f"\n  ✅ No unexpected gaps in ID range")

        print()

        if args.save:
            out = Path(args.save)
            out.write_text(json.dumps(records, indent=2, ensure_ascii=False))
            print(f"  ✅ Saved {len(records)} records → {out}")
            if errors:
                print(f"  ⚠️  Saved WITH {len(errors)} schema error(s) -- do NOT upload until fixed\n")
        return

    # ── UPLOAD ───────────────────────────────────────────────────────────────
    if args.upload:
        src = Path(args.upload)
        if not src.exists():
            print(f"ERROR: {src} not found -- run --dry-run --save first")
            sys.exit(1)

        records = json.loads(src.read_text())

        # Gate 0: re-run schema validation before touching MongoDB
        print(f"\n  Running Gate 0 schema validation on {len(records)} records...")
        all_errors: list[str] = []
        for rec in records:
            all_errors.extend(_validate_entry(rec))

        if all_errors and not args.force:
            print(f"\n  ⛔ UPLOAD BLOCKED -- {len(all_errors)} schema error(s):")
            for e in all_errors[:10]:
                print(f"       {e}")
            print(f"\n  Fix errors and re-run --dry-run --save, then retry --upload.")
            print(f"  Use --force to override (NOT recommended for production).")
            sys.exit(1)

        if all_errors and args.force:
            print(f"  ⚠️  --force: uploading despite {len(all_errors)} schema error(s)")

        # Connect and upload
        try:
            from pymongo import MongoClient, UpdateOne
        except ImportError:
            print("ERROR: pymongo not installed")
            sys.exit(1)

        if not args.mongo_url:
            print("ERROR: --mongo-url required")
            sys.exit(1)

        client = MongoClient(args.mongo_url)
        col    = client[args.db_name][COLLECTION]

        ops = [
            UpdateOne({"id": r["id"], "science_id": SCIENCE_ID}, {"$set": r}, upsert=True)
            for r in records
        ]
        result = col.bulk_write(ops, ordered=False)
        print(f"\n  ✅ Inserted {result.upserted_count} / "
              f"Updated {result.modified_count} records "
              f"→ {args.db_name}.{COLLECTION}")
        print(VERIFY_QUERIES)
        client.close()


if __name__ == "__main__":
    main()
