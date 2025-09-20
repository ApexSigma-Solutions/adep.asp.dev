#!/bin/bash

# Cleanup script for monorepo: Removes temporary files and caches
# Usage: ./cleanup.sh [dry-run]
# Options: dry-run to preview without deleting

LOG_FILE="cleanup_log.txt"
ROOT_DIR="$(pwd)"
DRY_RUN=false

if [ "$1" = "dry-run" ]; then
    DRY_RUN=true
    echo "DRY RUN MODE: No files will be deleted."
fi

echo "Starting cleanup in $ROOT_DIR at $(date)" > "$LOG_FILE"

# Function to remove files/directories safely
remove_item() {
    local item="$1"
    if [ "$DRY_RUN" = true ]; then
        echo "Would remove: $item" | tee -a "$LOG_FILE"
    else
        rm -rf "$item" && echo "Removed: $item" >> "$LOG_FILE"
    fi
}

# Skip protected directories
SKIP_DIRS=("_archive" ".git" "node_modules")

# Remove __pycache__ directories
find "$ROOT_DIR" -type d -name "__pycache__" | while read -r dir; do
    skip=false
    for skip_dir in "${SKIP_DIRS[@]}"; do
        if [[ "$dir" == *"/$skip_dir/"* ]]; then
            skip=true
            break
        fi
    done
    if [ "$skip" = false ]; then
        remove_item "$dir"
    fi
done

# Remove other cache directories
for cache in ".pytest_cache" ".ruff_cache" ".mypy_cache" ".coverage"; do
    find "$ROOT_DIR" -type d -name "$cache" | while read -r dir; do
        skip=false
        for skip_dir in "${SKIP_DIRS[@]}"; do
            if [[ "$dir" == *"/$skip_dir/"* ]]; then
                skip=true
                break
            fi
        done
        if [ "$skip" = false ]; then
            remove_item "$dir"
        fi
    done
done

# Remove Python compiled files
find "$ROOT_DIR" -type f \( -name "*.pyc" -o -name "*.pyo" -o -name "*.pyd" \) | while read -r file; do
    skip=false
    for skip_dir in "${SKIP_DIRS[@]}"; do
        if [[ "$file" == *"/$skip_dir/"* ]]; then
            skip=true
            break
        fi
    done
    if [ "$skip" = false ]; then
        remove_item "$file"
    fi
done

# Remove old log files (older than 7 days)
find "$ROOT_DIR" -type f -name "*.log" -mtime +7 | while read -r file; do
    skip=false
    for skip_dir in "${SKIP_DIRS[@]}"; do
        if [[ "$file" == *"/$skip_dir/"* ]]; then
            skip=true
            break
        fi
    done
    if [ "$skip" = false ]; then
        remove_item "$file"
    fi
done

# Remove temporary files
find "$ROOT_DIR" -type f \( -name "*.tmp" -o -name "*.temp" -o -name "*~" \) | while read -r file; do
    skip=false
    for skip_dir in "${SKIP_DIRS[@]}"; do
        if [[ "$file" == *"/$skip_dir/"* ]]; then
            skip=true
            break
        fi
    done
    if [ "$skip" = false ]; then
        remove_item "$file"
    fi
done

echo "Cleanup completed at $(date). Log saved to $LOG_FILE" | tee -a "$LOG_FILE"
if [ "$DRY_RUN" = true ]; then
    echo "Review $LOG_FILE for what would be removed."
else
    echo "Cleanup log: $LOG_FILE"
fi
