#!/bin/bash

# safe-delete.sh
#
# This script provides a safe alternative to the 'rm' command by moving
# files to a trash directory instead of permanently deleting them.

TRASH_DIR="$(git rev-parse --show-toplevel)/_archive/trash"

function safe_rm() {
    # Create the trash directory if it doesn't exist
    mkdir -p "$TRASH_DIR"

    if [ $# -eq 0 ]; then
        echo "safe_rm: missing operand"
        echo "Try 'safe_rm --help' for more information."
        return 1
    fi

    for item in "$@"; do
        if [ ! -e "$item" ]; then
            echo "safe_rm: cannot remove '$item': No such file or directory" >&2
            continue
        fi
        
        # Generate a unique name for the moved item
        timestamp=$(date +%Y%m%d%H%M%S)
        base_name=$(basename "$item")
        mv -f "$item" "$TRASH_DIR/${base_name}_${timestamp}"
        echo "Moved '$item' to trash."
    done
}

# To use this, add the following to your .bashrc or .zshrc:
#
# source /path/to/your/project/scripts/utils/safe-delete.sh
# alias rm='safe_rm'
