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
#   backend/scripts/backup/horoscope_db_<timestamp>.gz   (full)
#   backend/scripts/backup/horoscope_critical_<timestamp>.gz   (critical only)
# =============================================================================

set -euo pipefail

MONGO_URL="${MONGO_URL:-}"
DB_NAME="${DB_NAME:-horoscope_db}"
BACKUP_DIR="$(dirname "$0")/backup"
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
# CRITICAL — irreplaceable user/config data
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

# REGENERATABLE — can be recreated by re-running ingest scripts in git
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
  echo "REGENERATABLE (ingest scripts in git = backup):"
  for c in "${REGENERATABLE_COLLECTIONS[@]}"; do echo "  ↺ $c"; done
  echo ""
  exit 0
fi

# ── Critical-only backup ─────────────────────────────────────────────────────
if [[ "$MODE" == "critical" ]]; then
  OUTFILE="$BACKUP_DIR/horoscope_critical_${TIMESTAMP}.gz"
  echo ""
  echo "▶ Critical-only backup → $OUTFILE"
  echo ""

  # Build --collection flags
  COL_FLAGS=()
  for c in "${CRITICAL_COLLECTIONS[@]}"; do
    COL_FLAGS+=(--collection "$c")
  done

  mongodump \
    --uri="$MONGO_URL" \
    --db="$DB_NAME" \
    "${COL_FLAGS[@]}" \
    --gzip \
    --archive="$OUTFILE"

  SIZE=$(du -sh "$OUTFILE" | cut -f1)
  echo ""
  echo "✓ Critical backup complete"
  echo "  File : $OUTFILE"
  echo "  Size : $SIZE"
  echo ""
  echo "Collections backed up:"
  for c in "${CRITICAL_COLLECTIONS[@]}"; do echo "  • $c"; done
  exit 0
fi

# ── Full backup ───────────────────────────────────────────────────────────────
OUTFILE="$BACKUP_DIR/horoscope_db_${TIMESTAMP}.gz"
echo ""
echo "▶ Full database backup → $OUTFILE"
echo ""

mongodump \
  --uri="$MONGO_URL" \
  --db="$DB_NAME" \
  --gzip \
  --archive="$OUTFILE"

SIZE=$(du -sh "$OUTFILE" | cut -f1)
echo ""
echo "✓ Full backup complete"
echo "  File : $OUTFILE"
echo "  Size : $SIZE"
echo ""
echo "To restore:"
echo "  mongorestore --uri=\"\$MONGO_URL\" --db=$DB_NAME --gzip --archive=$OUTFILE"
echo ""

# ── Prune old backups (keep last 7 full, last 14 critical) ────────────────────
echo "Pruning old backups..."
ls -t "$BACKUP_DIR"/horoscope_db_*.gz 2>/dev/null | tail -n +8 | xargs rm -f
ls -t "$BACKUP_DIR"/horoscope_critical_*.gz 2>/dev/null | tail -n +15 | xargs rm -f
echo "  Kept: 7 most recent full backups, 14 most recent critical backups"
