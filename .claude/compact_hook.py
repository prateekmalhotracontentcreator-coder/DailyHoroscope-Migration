"""
PostCompact hook -- runs after every compaction cycle.
1. Appends new timestamped entry to COMPACTION_LOG.md
2. Immediately rotates: keeps last 3 entries live, archives everything older
   (rotation happens every cycle -- no line threshold needed)
"""
import sys, json, datetime, os

BASE         = "/Users/apple/DailyHoroscope-Migration/.claude"
LOG          = f"{BASE}/COMPACTION_LOG.md"
ARCH         = f"{BASE}/_archive"
KEEP_ENTRIES = 3

try:
    data    = json.load(sys.stdin)
    summary = data.get("summary", "").strip()
except Exception:
    summary = ""

if not summary:
    sys.exit(0)

now   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
ym    = datetime.datetime.now().strftime("%Y-%m")
entry = f"\n---\n## Compaction -- {now}\n{summary}\n"

# 1. Append new entry
with open(LOG, "a") as f:
    f.write(entry)

# 2. Rotate every cycle -- always keep only last 3 entries live
with open(LOG, "r") as f:
    content = f.read()

parts   = content.split("\n---\n")
header  = parts[0]                                     # file header block
entries = [p for p in parts[1:] if p.strip()]          # all log entries

if len(entries) > KEEP_ENTRIES:
    to_archive = entries[:-KEEP_ENTRIES]
    to_keep    = entries[-KEEP_ENTRIES:]

    # Archive older entries (append -- monthly file accumulates)
    os.makedirs(ARCH, exist_ok=True)
    arch_file = f"{ARCH}/COMPACTION_LOG_{ym}.md"
    with open(arch_file, "a") as f:
        f.write("\n---\n".join(to_archive) + "\n")

    # Rewrite live log: fixed header + last 3 entries only
    fixed_header = (
        "# COMPACTION_LOG.md\n"
        "> Last 3 compaction cycles shown. Older entries → _archive/COMPACTION_LOG_" + ym + ".md\n"
        "> Never read at session start. Read only when preparing full handover.\n"
    )
    with open(LOG, "w") as f:
        f.write(fixed_header)
        for e in to_keep:
            f.write("\n---\n" + e)

    print(f'{{"systemMessage": "Compaction logged [{now}]. {len(to_archive)} older entr{"y" if len(to_archive)==1 else "ies"} archived. Live log: last 3 only."}}')
else:
    print(f'{{"systemMessage": "Compaction logged [{now}]. Live log: {len(entries)} of {KEEP_ENTRIES} slots used."}}')
