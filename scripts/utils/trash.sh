#!/bin/bash

# Safe delete script: Moves files to _archive/trash/ instead of deleting
# Usage: ./trash.sh <file_or_directory>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file_or_directory>"
    exit 1
fi

TARGET="$1"
TRASH_DIR="../_archive/trash"  # Relative path from scripts/utils/

if [ ! -d "$TRASH_DIR" ]; then
    mkdir -p "$TRASH_DIR"
fi

if [ -e "$TARGET" ]; then
    mv "$TARGET" "$TRASH_DIR/"
    echo "Moved $TARGET to $TRASH_DIR/"
else
    echo "Error: $TARGET does not exist"
fi
