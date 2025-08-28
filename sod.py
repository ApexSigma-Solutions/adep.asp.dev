#!/usr/bin/env python3
"""
/sod - Society of Agents Deploy Command
Quick alias for the full SOD deployment script
"""

import sys
from pathlib import Path

# Add the scripts directory to the path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

# Import and run the SOD deployer
from sod_deploy import main

if __name__ == "__main__":
    main()