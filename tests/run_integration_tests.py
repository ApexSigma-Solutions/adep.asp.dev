#!/usr/bin/env python3
"""
Integration Test Runner for ApexSigma Core Services

This script provides a convenient way to run the core integration test suite
between InGest-LLM.as and memOS.as services. It includes service health checks,
test execution, and detailed reporting.
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional
import httpx

# Service Configuration
INGEST_SERVICE_URL = "http://localhost:8000"
MEMOS_SERVICE_URL = "http://localhost:8091"
DEVENVIRO_SERVICE_URL = "http://localhost:8090"

class TestRunner:
    """Main test runner class."""
    
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.results = {}
        
    async def check_service_health(self, url: str, service_name: str) -> Dict:
        """Check if a service is healthy and return status info."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{url}/health")
                
                if response.status_code == 200:
                    health_data = response.json()
                    return {
                        "status": "healthy",
                        "service": service_name,
                        "url": url,
                        "data": health_data
                    }
                else:
                    return {
                        "status": "unhealthy", 
                        "service": service_name,
                        "url": url,
                        "error": f"HTTP {response.status_code}"
                    }
                    
        except Exception as e:
            return {
                "status": "unreachable",
                "service": service_name, 
                "url": url,
                "error": str(e)
            }
    
    async def validate_service_ecosystem(self) -> bool:
        """Validate that all required services are available."""
        print("🔍 Validating ApexSigma service ecosystem...")
        print("=" * 50)
        
        services = [
            (INGEST_SERVICE_URL, "InGest-LLM.as"),
            (MEMOS_SERVICE_URL, "memOS.as"),
            (DEVENVIRO_SERVICE_URL, "DevEnviro.as")
        ]
        
        all_healthy = True
        health_results = {}
        
        for url, service_name in services:
            health_info = await self.check_service_health(url, service_name)
            health_results[service_name] = health_info
            
            status = health_info["status"]
            if status == "healthy":
                print(f"✅ {service_name:15} : {status:10} - {url}")
            elif status == "unhealthy":
                print(f"⚠️  {service_name:15} : {status:10} - {url} ({health_info['error']})")
                # Mark as not critical for integration tests if it's DevEnviro
                if service_name != "DevEnviro.as":
                    all_healthy = False
            else:
                print(f"❌ {service_name:15} : {status:10} - {url} ({health_info['error']})")
                # Mark as not critical for integration tests if it's DevEnviro
                if service_name != "DevEnviro.as":
                    all_healthy = False
        
        print()
        
        if all_healthy:
            print("✅ Core services (InGest-LLM.as, memOS.as) are ready for integration testing")
        else:
            print("❌ Some core services are not available - integration tests may fail")
            
        # Show detailed health info for available services
        for service_name, health_info in health_results.items():
            if health_info["status"] == "healthy" and "data" in health_info:
                data = health_info["data"]
                print(f"\n📊 {service_name} Details:")
                
                if service_name == "memOS.as" and "services" in data:
                    for db_name, db_status in data["services"].items():
                        print(f"   📦 {db_name}: {db_status}")
                        
                if "version" in data:
                    print(f"   🔖 Version: {data['version']}")
                    
        print("\n" + "=" * 50)
        return all_healthy
    
    def run_pytest_command(self, test_pattern: Optional[str] = None, verbose: bool = True) -> subprocess.CompletedProcess:
        """Run pytest with specified parameters."""
        cmd = ["python", "-m", "pytest"]
        
        if test_pattern:
            cmd.extend(["-k", test_pattern])
        
        if verbose:
            cmd.extend(["-v", "-s"])
        
        # Add the test file
        test_file = self.test_dir / "test_core_integration_e2e.py"
        cmd.append(str(test_file))
        
        # Add markers for better output
        cmd.extend(["--tb=short", "--no-header"])
        
        print(f"🚀 Running command: {' '.join(cmd)}")
        print()
        
        return subprocess.run(cmd, cwd=self.test_dir, capture_output=False)
    
    def generate_test_report(self, results: Dict) -> None:
        """Generate a summary test report."""
        print("\n" + "=" * 60)
        print("📋 INTEGRATION TEST SUMMARY REPORT")
        print("=" * 60)
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("passed", False))
        failed_tests = total_tests - passed_tests
        
        print(f"📊 Test Results:")
        print(f"   Total Tests:  {total_tests}")
        print(f"   Passed:       {passed_tests}")
        print(f"   Failed:       {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "   Success Rate: N/A")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for test_name, result in results.items():
                if not result.get("passed", False):
                    print(f"   - {test_name}: {result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 60)
    
    async def run_integration_tests(self, test_category: Optional[str] = None) -> bool:
        """Run the complete integration test suite."""
        print("🚀 APEXSIGMA CORE INTEGRATION TEST RUNNER")
        print("Testing InGest-LLM.as ↔ memOS.as Integration")
        print("=" * 60)
        
        # Step 1: Validate service ecosystem
        services_ready = await self.validate_service_ecosystem()
        
        if not services_ready:
            print("⚠️  Some core services are not ready. Proceeding with available services...")
            print("   Integration tests may fail or be skipped.")
        
        print(f"⏰ Starting integration tests at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Step 2: Run pytest with appropriate filters
        if test_category:
            print(f"🎯 Running {test_category} tests only...")
            result = self.run_pytest_command(test_pattern=test_category)
        else:
            print("🧪 Running complete integration test suite...")
            result = self.run_pytest_command()
        
        # Step 3: Report results
        success = result.returncode == 0
        
        if success:
            print("\n🎉 Integration tests completed successfully!")
            print("✅ InGest-LLM.as ↔ memOS.as integration is working correctly")
        else:
            print("\n💥 Some integration tests failed!")
            print("❌ Check the output above for details")
        
        return success

def main():
    """Main entry point for the test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run ApexSigma core integration tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_integration_tests.py                    # Run all tests
  python run_integration_tests.py --category workflow # Run workflow tests only
  python run_integration_tests.py --category error   # Run error handling tests
  python run_integration_tests.py --category performance # Run performance tests
        """
    )
    
    parser.add_argument(
        "--category", 
        choices=["connectivity", "workflow", "error", "performance"],
        help="Run only tests in the specified category"
    )
    
    parser.add_argument(
        "--no-health-check",
        action="store_true",
        help="Skip initial service health checks"
    )
    
    args = parser.parse_args()
    
    # Create and run test runner
    runner = TestRunner()
    
    try:
        success = asyncio.run(runner.run_integration_tests(test_category=args.category))
        
        if success:
            print("\n🏆 All integration tests passed!")
            print("The ApexSigma core integration is ready for production use.")
            sys.exit(0)
        else:
            print("\n🔧 Integration tests revealed issues that need attention.")
            print("Please review the test output and fix any failing tests.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Test runner encountered an error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()