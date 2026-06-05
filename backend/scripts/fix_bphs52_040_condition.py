#!/usr/bin/env python3
"""
Inspect and fix R-BPHS52-040 condition text encoding error.
Finds which field contains 'own sign' and corrects it to 'debilitation sign'.

Usage:
  python3 backend/scripts/fix_bphs52_040_condition.py          # inspect only
  python3 backend/scripts/fix_bphs52_040_condition.py --live   # apply fix
"""

import sys
import json
from datetime import datetime, timezone
from db_connect import get_collection

DRY_RUN  = "--live" not in sys.argv
RULE_ID  = "R-BPHS52-040"
FIND     = "own sign"
REPLACE  = "debilitation sign"
FIND2    = "his own sign"
REPLACE2 = "his sign of debilitation"

def scan_fields(doc, prefix=""):
    """Recursively scan all string fields for FIND text."""
    hits = []
    for k, v in doc.items():
        path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, str) and FIND in v:
            hits.append((path, v))
        elif isinstance(v, dict):
            hits.extend(scan_fields(v, path))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, str) and FIND in item:
                    hits.append((f"{path}[{i}]", item))
                elif isinstance(item, dict):
                    hits.extend(scan_fields(item, f"{path}[{i}]"))
    return hits

col = get_collection("interpretation_rules")
rule = col.find_one({"rule_id": RULE_ID})

if not rule:
    print(f"ERROR: {RULE_ID} not found in interpretation_rules.")
    sys.exit(1)

print(f"Rule found: {RULE_ID}")
print(f"approval_status: {rule.get('approval_status')}")
print()

# Scan every field for the target text
hits = scan_fields({k: v for k, v in rule.items() if k != "_id"})

# Exclude validation.* fields -- those are audit trail records documenting
# the original error and must not be altered.
EXCLUDE_PREFIXES = ("validation.",)

content_hits = [(p, v) for p, v in hits if not any(p.startswith(x) for x in EXCLUDE_PREFIXES)]
skipped_hits  = [(p, v) for p, v in hits if     any(p.startswith(x) for x in EXCLUDE_PREFIXES)]

if not hits:
    print(f"No fields contain '{FIND}' -- dumping full condition and interpretation blocks:")
    print()
    print("condition block:")
    print(json.dumps(rule.get("condition", {}), indent=2, default=str))
    print()
    print("interpretation block:")
    print(json.dumps(rule.get("interpretation", {}), indent=2, default=str))
    sys.exit(0)

print(f"Fields containing '{FIND}':")
for path, val in hits:
    tag = "  [SKIP -- audit trail]" if any(path.startswith(x) for x in EXCLUDE_PREFIXES) else ""
    print(f"  {path}:{tag}")
    print(f"    {repr(val[:200])}")
print()

if DRY_RUN:
    print("DRY RUN -- corrections that would be applied:")
    for path, val in content_hits:
        print(f"  ✅ {path}: '{FIND}' → '{REPLACE}'")
    for path, _ in skipped_hits:
        print(f"  ⏭️  {path}: SKIPPED (audit trail -- do not modify)")
    print()
    print("Re-run with --live to apply.")
else:
    now_str = datetime.now(timezone.utc).isoformat()
    update_dict = {"updated_at": now_str}

    for path, val in content_hits:
        new_val = val.replace(FIND2, REPLACE2).replace(FIND, REPLACE)
        mongo_key = path.replace("[", ".").replace("]", "")
        update_dict[mongo_key] = new_val

    result = col.update_one({"rule_id": RULE_ID}, {"$set": update_dict})
    if result.modified_count == 1:
        print(f"✅ PATCHED {RULE_ID} -- {len(content_hits)} content field(s) corrected:")
        for path, _ in content_hits:
            print(f"   {path}: '{FIND}' → '{REPLACE}'")
        print()
        print(f"⏭️  {len(skipped_hits)} audit trail field(s) intentionally left unchanged:")
        for path, _ in skipped_hits:
            print(f"   {path}")
    else:
        print(f"⚠️  No change applied (modified_count=0). Rule may already be correct.")
