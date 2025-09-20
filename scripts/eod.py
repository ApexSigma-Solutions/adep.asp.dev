#!/usr/bin/env python3
"""
EOD (End of Day) Command - Wrapper Script
Quick alias for the EOD command protocol
"""

import sys
from pathlib import Path

# Add the scripts directory to the path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

# Import and run the EOD command
from eod_command import main

if __name__ == "__main__":
    main()