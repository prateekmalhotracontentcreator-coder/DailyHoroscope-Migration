#!/usr/bin/env bash
# =============================================================================
# EverydayHoroscope — MongoDB Backup Script
# =============================================================================
# Usage:
#   ./backend/scripts/backup_mongodb.sh        # full dump of everything
#
# Requirements:
#   - mongodump  (brew install mongodb-database-tools)
#   - $MONGO_URL exported in shell
#
# Output:
#   backend/scripts/backup/horoscope_db_<timestamp>.gz
# =============================================================================

MONGO_URL="${MONGO_URL:-}"
DB_NAME="${DB_NAME:-horoscope_db}"
BACKUP_DIR="$(cd "$(dirname "$0")" && pwd)/backup"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

if [[ -z "$MONGO_URL" ]]; then
  echo "ERROR: MONGO_URL is not set.  export MONGO_URL='mongodb+srv://...'"
  exit 1
fi

mkdir -p "$BACKUP_DIR"
OUTFILE="$BACKUP_DIR/horoscope_db_${TIMESTAMP}.gz"

echo ""
echo "▶ Full backup → $OUTFILE"
echo ""

mongodump \
  --uri="$MONGO_URL" \
  --db="$DB_NAME" \
  --gzip \
  --archive="$OUTFILE"

if [[ -f "$OUTFILE" ]]; then
  SIZE=$(du -sh "$OUTFILE" | cut -f1)
  echo ""
  echo "✓ Backup complete"
  echo "  File : $OUTFILE"
  echo "  Size : $SIZE"
  echo ""
  echo "To restore:"
  echo "  mongorestore --uri=\"\$MONGO_URL\" --db=$DB_NAME --gzip --archive=$OUTFILE"
  echo ""
  # Keep last 14 backups, delete older ones
  ls -t "$BACKUP_DIR"/horoscope_db_*.gz 2>/dev/null | tail -n +15 | xargs rm -f 2>/dev/null
  echo "  (older backups pruned — keeping 14 most recent)"
else
  echo ""
  echo "ERROR: Backup file was not created. Check MONGO_URL and connection."
  exit 1
fi
