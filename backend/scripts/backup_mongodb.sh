#!/usr/bin/env bash
# =============================================================================
# EverydayHoroscope — MongoDB Backup Script
# =============================================================================
# Usage:
#   ./backend/scripts/backup_mongodb.sh              # full backup
#   ./backend/scripts/backup_mongodb.sh --critical   # critical collections only
#   ./backend/scripts/backup_mongodb.sh --list       # list what would be backed up
#
# Requirements:
#   - mongodump (brew install mongodb-database-tools)
#   - $MONGO_URL exported in shell
#
# Output:
#   backend/scripts/backup/horoscope_db_<timestamp>.gz        (full)
#   backend/scripts/backup/horoscope_critical_<timestamp>.gz  (critical only)
# =============================================================================

# Note: intentionally NOT using "set -e" — mongodump warns (non-zero exit) when
# a listed collection doesn't exist yet (e.g. numerology_reports before any
# reports are generated). We handle errors explicitly below instead.

MONGO_URL="${MONGO_URL:-}"
DB_NAME="${DB_NAME:-horoscope_db}"
BACKUP_DIR="$(cd "$(dirname "$0")" && pwd)/backup"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
MODE="full"

# ── Parse args ────────────────────────────────────────────────────────────────
for arg in "$@"; do
  case $arg in
    --critical) MODE="critical" ;;
    --list)     MODE="list" ;;
  esac
done

# ── Validate ──────────────────────────────────────────────────────────────────
if [[ -z "$MONGO_URL" ]]; then
  echo "ERROR: MONGO_URL is not set."
  echo "  export MONGO_URL='mongodb+srv://...'"
  exit 1
fi

mkdir -p "$BACKUP_DIR"

# ── Collection tiers ─────────────────────────────────────────────────────────
# CRITICAL — irreplaceable user/config data (back these up)
CRITICAL_COLLECTIONS=(
  "users"
  "subscribers"
  "scheduled_notifications"
  "notification_logs"
  "social_post_logs"
  "app_settings"
  "payments"
  "tarot_history"
  "numerology_reports"
)

# REGENERATABLE — recreated by re-running ingest scripts (git IS the backup)
REGENERATABLE_COLLECTIONS=(
  "interpretation_rules"
  "mundane_engine_specs"
  "mundane_geo_entities"
)

# ── List mode ─────────────────────────────────────────────────────────────────
if [[ "$MODE" == "list" ]]; then
  echo ""
  echo "CRITICAL (will be backed up):"
  for c in "${CRITICAL_COLLECTIONS[@]}"; do echo "  ✓ $c"; done
  echo ""
  echo "REGENERATABLE (ingest scripts in git = the backup — zero Atlas cost to restore):"
  for c in "${REGENERATABLE_COLLECTIONS[@]}"; do echo "  ↺ $c"; done
  echo ""
  exit 0
fi

# ── Critical-only backup ─────────────────────────────────────────────────────
# Strategy: full DB dump with --excludeCollection for regeneratable collections.
# This avoids "collection does not exist" errors entirely — mongodump only
# touches what's actually in the DB and skips nothing unexpectedly.
if [[ "$MODE" == "critical" ]]; then
  OUTFILE="$BACKUP_DIR/horoscope_critical_${TIMESTAMP}.gz"
  echo ""
  echo "▶ Critical-only backup → $OUTFILE"
  echo "  (full dump minus regeneratable collections)"
  echo ""

  mongodump \
    --uri="$MONGO_URL" \
    --db="$DB_NAME" \
    --excludeCollection="interpretation_rules" \
    --excludeCollection="mundane_engine_specs" \
    --excludeCollection="mundane_geo_entities" \
    --gzip \
    --archive="$OUTFILE"

  if [[ -f "$OUTFILE" ]]; then
    SIZE=$(du -sh "$OUTFILE" | cut -f1)
    echo ""
    echo "✓ Critical backup complete"
    echo "  File : $OUTFILE"
    echo "  Size : $SIZE"
    echo ""
    echo "Excluded (regeneratable from git):"
    for c in "${REGENERATABLE_COLLECTIONS[@]}"; do echo "  ↺ $c"; done
    echo ""
    echo "To restore:"
    echo "  mongorestore --uri=\"\$MONGO_URL\" --db=$DB_NAME --gzip --archive=$OUTFILE"
  else
    echo ""
    echo "ERROR: Backup file was not created. Check your MONGO_URL and connection."
    exit 1
  fi

  # Prune — keep last 14 critical backups
  ls -t "$BACKUP_DIR"/horoscope_critical_*.gz 2>/dev/null | tail -n +15 | xargs rm -f 2>/dev/null
  exit 0
fi

# ── Full backup ───────────────────────────────────────────────────────────────
OUTFILE="$BACKUP_DIR/horoscope_db_${TIMESTAMP}.gz"
echo ""
echo "▶ Full database backup → $OUTFILE"
echo ""

# Full dump — no collection filter, so no missing-collection warnings
mongodump \
  --uri="$MONGO_URL" \
  --db="$DB_NAME" \
  --gzip \
  --archive="$OUTFILE" || true

if [[ -f "$OUTFILE" ]]; then
  SIZE=$(du -sh "$OUTFILE" | cut -f1)
  echo ""
  echo "✓ Full backup complete"
  echo "  File : $OUTFILE"
  echo "  Size : $SIZE"
  echo ""
  echo "To restore:"
  echo "  mongorestore --uri=\"\$MONGO_URL\" --db=$DB_NAME --gzip --archive=$OUTFILE"
else
  echo ""
  echo "ERROR: Backup file was not created. Check your MONGO_URL and connection."
  exit 1
fi

# Prune — keep last 7 full backups
echo ""
echo "Pruning old backups (keeping 7 most recent full, 14 most recent critical)..."
ls -t "$BACKUP_DIR"/horoscope_db_*.gz 2>/dev/null | tail -n +8 | xargs rm -f 2>/dev/null
ls -t "$BACKUP_DIR"/horoscope_critical_*.gz 2>/dev/null | tail -n +15 | xargs rm -f 2>/dev/null
echo "Done."
