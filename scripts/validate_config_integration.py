#!/usr/bin/env python3
"""
Configuration Integration Validation Script

Tests that all services can successfully import and use centralized settings.
This script validates Step 2 of OVS-WO-001-EO implementation.
"""

import sys
import os
from pathlib import Path

# Add repo root to Python path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

def test_centralized_config():
    """Test centralized configuration loading"""
    print("[TEST] Testing centralized configuration...")
    
    try:
        from config.settings import settings
        print("[PASS] Centralized settings loaded successfully")
        print(f"   Database: {settings.POSTGRES_DB}")
        print(f"   Host: {settings.POSTGRES_HOST}")
        print(f"   User: {settings.POSTGRES_USER}")
        print(f"   Database URL: {settings.database_url}")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to load centralized settings: {e}")
        return False

def test_memos_service_config():
    """Test memos.as service configuration"""
    print("\n[TEST] Testing memos.as service configuration...")
    
    try:
        # Add memos service to path
        memos_path = repo_root / "services" / "memos.as"
        sys.path.insert(0, str(memos_path))
        
        from app.services.postgres_client import PostgresClient
        
        # Try to create client (this will test the configuration loading)
        client = PostgresClient()
        print("[PASS] Memos.as PostgreSQL client initialized successfully")
        print(f"   Database URL configured: {bool(client.database_url)}")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to initialize memos.as client: {e}")
        return False

def test_tools_service_config():
    """Test tools.as service configuration"""
    print("\n[TEST] Testing tools.as service configuration...")
    
    try:
        # Add tools service to path
        tools_path = repo_root / "services" / "tools.as"
        sys.path.insert(0, str(tools_path))
        
        from app.database import DATABASE_URL, engine
        
        print("[PASS] Tools.as database configuration loaded successfully")
        print(f"   Database URL: {DATABASE_URL}")
        print(f"   Engine configured: {bool(engine)}")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to load tools.as database config: {e}")
        return False

def test_devenviro_service_config():
    """Test devenviro.as service configuration"""
    print("\n[TEST] Testing devenviro.as service configuration...")
    
    try:
        # Add devenviro service to path
        devenviro_path = repo_root / "services" / "devenviro.as" / "app"
        sys.path.insert(0, str(devenviro_path))
        
        from src.core.database import get_db_connection
        
        print("[PASS] DevEnviro.as database module loaded successfully")
        print("   Database connection function available")
        # Note: Not testing actual connection as it requires running database
        return True
    except Exception as e:
        print(f"[FAIL] Failed to load devenviro.as database config: {e}")
        return False

def test_ingest_service_config():
    """Test InGest-LLM.as service configuration"""
    print("\n[TEST] Testing InGest-LLM.as service configuration...")
    
    try:
        # Add ingest service to path
        ingest_path = repo_root / "services" / "InGest-LLM.as" / "src"
        sys.path.insert(0, str(ingest_path))
        
        from ingest_llm_as.config import settings as ingest_settings
        
        print("[PASS] InGest-LLM.as settings loaded successfully")
        print(f"   Database: {ingest_settings.postgres_db}")
        print(f"   Host: {ingest_settings.postgres_host}")
        print(f"   User: {ingest_settings.postgres_user}")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to load InGest-LLM.as config: {e}")
        return False

def main():
    """Run all configuration validation tests"""
    print("STARTING Configuration Integration Validation")
    print("=" * 50)
    
    tests = [
        test_centralized_config,
        test_memos_service_config,
        test_tools_service_config, 
        test_devenviro_service_config,
        test_ingest_service_config
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"[FAIL] Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print(f"[PASS] Passed: {sum(results)}/{len(results)} tests")
    
    if all(results):
        print("[SUCCESS] ALL CONFIGURATION INTEGRATION TESTS PASSED!")
        print("   Ready for database connectivity testing")
        return True
    else:
        print("[WARNING] Some configuration tests failed")
        print("   Review service configuration imports")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
