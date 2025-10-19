#!/usr/bin/env python3
"""
Integrity Check Wrapper - Python wrapper for integrity-check.sh
Validates git submodules, Poetry lockfiles, and Docker build contexts
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Tuple


def run_integrity_check(verbose: bool = False) -> Tuple[bool, str]:
    """
    Run the integrity check bash script.
    
    Args:
        verbose: Enable verbose output
        
    Returns:
        Tuple of (success: bool, output: str)
    """
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    integrity_script = script_dir / "integrity-check.sh"
    
    if not integrity_script.exists():
        return False, f"ERROR: Integrity check script not found at {integrity_script}"
    
    try:
        # Run the bash script
        result = subprocess.run(
            ["bash", str(integrity_script)],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        output = result.stdout + result.stderr
        
        if verbose or result.returncode != 0:
            print(output)
        
        return result.returncode == 0, output
        
    except subprocess.TimeoutExpired:
        return False, "ERROR: Integrity check timed out after 5 minutes"
    except Exception as e:
        return False, f"ERROR: Failed to run integrity check: {e}"


if __name__ == "__main__":
    # Can be run standalone for testing
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    success, output = run_integrity_check(verbose=verbose)
    
    if success:
        print("\n✅ Integrity check PASSED")
        sys.exit(0)
    else:
        print("\n❌ Integrity check FAILED")
        print(output)
        sys.exit(1)
