#!/bin/bash

# Remove all traces of "context_portal" from the monorepo
# Usage: ./remove_context_portal.sh

LOG_FILE="remove_context_portal_log.txt"
ROOT_DIR="$(pwd)"
SKIP_DIRS=("_archive" ".git" "node_modules")

echo "Starting removal of 'context_portal' in $ROOT_DIR at $(date)" > "$LOG_FILE"

# Find and process files containing "context_portal"
grep -r "context_portal" "$ROOT_DIR" --exclude-dir="${SKIP_DIRS[@]}" | while IFS=: read -r file line; do
    echo "Found in: $file" >> "$LOG_FILE"
    # Remove lines containing "context_portal"
    sed -i "/context_portal/d" "$file"
    echo "Removed from: $file" >> "$LOG_FILE"
done

echo "Removal completed at $(date). Log saved to $LOG_FILE" | tee -a "$LOG_FILE"
