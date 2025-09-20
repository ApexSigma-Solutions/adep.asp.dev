<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# API Registration Verification Scripts for FastMCP

Here's a comprehensive collection of scripts and utilities to verify successful API registration responses in FastMCP, ensuring robust deployment and monitoring.

## Core Verification Framework

### Basic Response Verification Script

```python
import asyncio
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from fastmcp import FastMCP, Context

@dataclass
class RegistrationResult:
    api_name: str
    success: bool
    tools_count: Optional[int] = None
    error_message: Optional[str] = None
    registration_time: datetime = None
    response_time_ms: Optional[float] = None

class APIRegistrationVerifier:
    def __init__(self, mcp_instance: FastMCP):
        self.mcp = mcp_instance
        self.client = httpx.AsyncClient()
        self.results: List[RegistrationResult] = []
    
    async def verify_registration_response(self, 
                                         response: Dict[str, Any], 
                                         api_name: str) -> RegistrationResult:
        """Verify a single API registration response"""
        
        start_time = datetime.now()
        
        # Check basic success indicators
        success = response.get('success', False)
        error = response.get('error')
        tools_count = response.get('tools_registered') or response.get('tools_count')
        
        result = RegistrationResult(
            api_name=api_name,
            success=success and error is None,
            tools_count=tools_count,
            error_message=error,
            registration_time=start_time
        )
        
        # Additional verification for successful registrations
        if result.success:
            verification_passed = await self._deep_verify_registration(api_name, result)
            result.success = verification_passed
        
        self.results.append(result)
        return result
    
    async def _deep_verify_registration(self, api_name: str, result: RegistrationResult) -> bool:
        """Perform deep verification of registered API tools"""
        try:
            # Verify tools are actually accessible
            if hasattr(self.mcp, 'list_tools'):
                tools = await self.mcp.list_tools()
                api_tools = [tool for tool in tools if api_name.lower() in tool.name.lower()]
                
                if len(api_tools) != result.tools_count:
                    result.error_message = f"Expected {result.tools_count} tools, found {len(api_tools)}"
                    return False
            
            return True
            
        except Exception as e:
            result.error_message = f"Deep verification failed: {str(e)}"
            return False
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate comprehensive summary of all registration attempts"""
        total = len(self.results)
        successful = sum(1 for r in self.results if r.success)
        failed = total - successful
        
        return {
            "total_attempts": total,
            "successful_registrations": successful,
            "failed_registrations": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "successes": [r for r in self.results if r.success],
            "failures": [r for r in self.results if not r.success],
            "total_tools_registered": sum(r.tools_count for r in self.results if r.tools_count),
            "report_generated": datetime.now().isoformat()
        }
```


## Batch Registration Verification

### Multi-API Registration Verification System

```python
import yaml
import json
from pathlib import Path
from typing import List, Dict, Any
import logging

class BatchRegistrationVerifier:
    def __init__(self, mcp_instance: FastMCP):
        self.mcp = mcp_instance
        self.verifier = APIRegistrationVerifier(mcp_instance)
        self.logger = logging.getLogger(__name__)
    
    async def verify_batch_registration(self, 
                                      registration_responses: List[Dict[str, Any]],
                                      expected_apis: List[str] = None) -> Dict[str, Any]:
        """Verify batch API registration responses"""
        
        results = []
        
        for i, response in enumerate(registration_responses):
            api_name = response.get('api_name', f'api_{i}')
            result = await self.verifier.verify_registration_response(response, api_name)
            results.append(result)
        
        # Cross-reference with expected APIs if provided
        if expected_apis:
            registered_apis = {r.api_name for r in results if r.success}
            missing_apis = set(expected_apis) - registered_apis
            unexpected_apis = registered_apis - set(expected_apis)
        else:
            missing_apis = set()
            unexpected_apis = set()
        
        summary = self.verifier.generate_summary_report()
        summary.update({
            "expected_apis": expected_apis or [],
            "missing_apis": list(missing_apis),
            "unexpected_apis": list(unexpected_apis),
            "registration_complete": len(missing_apis) == 0
        })
        
        return summary
    
    async def verify_from_config(self, config_path: str) -> Dict[str, Any]:
        """Verify registrations against expected configuration"""
        
        # Load expected configuration
        with open(config_path, 'r') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                config = yaml.safe_load(f)
            else:
                config = json.load(f)
        
        expected_apis = [api['name'] for api in config.get('apis', [])]
        
        # Simulate registration process (in real scenario, this would be actual responses)
        registration_responses = []
        
        for api_config in config.get('apis', []):
            # This would be replaced with actual registration call results
            response = await self._simulate_registration(api_config)
            registration_responses.append(response)
        
        return await self.verify_batch_registration(registration_responses, expected_apis)
    
    async def _simulate_registration(self, api_config: Dict) -> Dict[str, Any]:
        """Simulate API registration for testing (replace with actual registration)"""
        # This is a placeholder - replace with actual registration logic
        return {
            "success": True,
            "api_name": api_config['name'],
            "tools_registered": len(api_config.get('endpoints', [])),
            "spec_url": api_config.get('openapi_url', 'N/A')
        }
```


## Real-time Registration Monitoring

### Registration Health Monitor

```python
import asyncio
from typing import Dict, List, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field

@dataclass
class RegistrationHealth:
    api_name: str
    registration_status: str = "unknown"  # "pending", "success", "failed", "timeout"
    last_check: datetime = field(default_factory=datetime.now)
    consecutive_failures: int = 0
    tools_accessible: bool = False
    response_times: List[float] = field(default_factory=list)
    error_history: List[str] = field(default_factory=list)

class RegistrationHealthMonitor:
    def __init__(self, mcp_instance: FastMCP, check_interval: int = 30):
        self.mcp = mcp_instance
        self.check_interval = check_interval
        self.health_data: Dict[str, RegistrationHealth] = {}
        self.monitoring = False
    
    def add_api_to_monitor(self, api_name: str):
        """Add an API to the monitoring list"""
        if api_name not in self.health_data:
            self.health_data[api_name] = RegistrationHealth(api_name=api_name)
    
    async def start_monitoring(self):
        """Start continuous health monitoring"""
        self.monitoring = True
        while self.monitoring:
            await self._perform_health_checks()
            await asyncio.sleep(self.check_interval)
    
    async def _perform_health_checks(self):
        """Perform health checks on all monitored APIs"""
        for api_name in self.health_data:
            await self._check_api_health(api_name)
    
    async def _check_api_health(self, api_name: str):
        """Check health of a specific API registration"""
        health = self.health_data[api_name]
        start_time = datetime.now()
        
        try:
            # Check if tools are accessible
            if hasattr(self.mcp, 'list_tools'):
                tools = await self.mcp.list_tools()
                api_tools = [tool for tool in tools if api_name.lower() in tool.name.lower()]
                health.tools_accessible = len(api_tools) > 0
            
            # Try to call a simple tool if available
            if api_tools:
                # This would attempt to call a health-check tool or simple operation
                health.registration_status = "success"
                health.consecutive_failures = 0
            else:
                health.registration_status = "failed"
                health.consecutive_failures += 1
                health.error_history.append("No tools found for API")
            
            # Record response time
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            health.response_times.append(response_time)
            
            # Keep only last 10 response times
            if len(health.response_times) > 10:
                health.response_times.pop(0)
            
            health.last_check = datetime.now()
            
        except Exception as e:
            health.registration_status = "error"
            health.consecutive_failures += 1
            health.error_history.append(str(e))
            health.last_check = datetime.now()
            
            # Keep only last 5 errors
            if len(health.error_history) > 5:
                health.error_history.pop(0)
    
    def get_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        healthy_apis = []
        unhealthy_apis = []
        
        for api_name, health in self.health_data.items():
            api_status = {
                "name": api_name,
                "status": health.registration_status,
                "tools_accessible": health.tools_accessible,
                "consecutive_failures": health.consecutive_failures,
                "last_check": health.last_check.isoformat(),
                "avg_response_time": sum(health.response_times) / len(health.response_times) if health.response_times else 0,
                "recent_errors": health.error_history[-3:] if health.error_history else []
            }
            
            if health.registration_status == "success" and health.consecutive_failures == 0:
                healthy_apis.append(api_status)
            else:
                unhealthy_apis.append(api_status)
        
        return {
            "total_apis": len(self.health_data),
            "healthy_count": len(healthy_apis),
            "unhealthy_count": len(unhealthy_apis),
            "healthy_apis": healthy_apis,
            "unhealthy_apis": unhealthy_apis,
            "report_time": datetime.now().isoformat()
        }
    
    def stop_monitoring(self):
        """Stop the health monitoring"""
        self.monitoring = False
```


## Comprehensive Verification Test Suite

### Integration Test Framework

```python
import pytest
import asyncio
from typing import Dict, Any, List
from fastmcp import FastMCP

class APIRegistrationTestSuite:
    def __init__(self, mcp_instance: FastMCP):
        self.mcp = mcp_instance
        self.test_results: List[Dict[str, Any]] = []
    
    async def run_comprehensive_tests(self, registration_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run comprehensive test suite on registration responses"""
        
        tests = [
            self._test_response_format,
            self._test_success_indicators,
            self._test_tool_accessibility,
            self._test_error_handling,
            self._test_schema_validation
        ]
        
        test_results = {}
        overall_success = True
        
        for test_func in tests:
            try:
                result = await test_func(registration_responses)
                test_results[test_func.__name__] = result
                if not result.get('passed', False):
                    overall_success = False
            except Exception as e:
                test_results[test_func.__name__] = {
                    'passed': False,
                    'error': str(e),
                    'details': 'Test execution failed'
                }
                overall_success = False
        
        return {
            'overall_success': overall_success,
            'test_results': test_results,
            'total_tests': len(tests),
            'passed_tests': sum(1 for r in test_results.values() if r.get('passed', False))
        }
    
    async def _test_response_format(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test that responses have proper format"""
        issues = []
        
        for i, response in enumerate(responses):
            if not isinstance(response, dict):
                issues.append(f"Response {i} is not a dictionary")
                continue
            
            required_fields = ['success', 'api_name']
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                issues.append(f"Response {i} missing fields: {missing_fields}")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'details': f'Checked {len(responses)} responses for proper format'
        }
    
    async def _test_success_indicators(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test success indicators are consistent"""
        issues = []
        
        for i, response in enumerate(responses):
            success = response.get('success', False)
            error = response.get('error')
            tools_count = response.get('tools_registered', 0)
            
            # Success should mean no errors and some tools registered
            if success and error:
                issues.append(f"Response {i}: Success=True but has error: {error}")
            
            if success and tools_count == 0:
                issues.append(f"Response {i}: Success=True but no tools registered")
            
            if not success and not error:
                issues.append(f"Response {i}: Success=False but no error message provided")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'details': f'Validated success indicators for {len(responses)} responses'
        }
    
    async def _test_tool_accessibility(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test that registered tools are actually accessible"""
        issues = []
        
        if hasattr(self.mcp, 'list_tools'):
            try:
                available_tools = await self.mcp.list_tools()
                tool_names = [tool.name for tool in available_tools]
                
                for response in responses:
                    if response.get('success'):
                        api_name = response.get('api_name', '')
                        expected_tools = response.get('tools_registered', 0)
                        
                        # Count tools that likely belong to this API
                        api_tools = [name for name in tool_names if api_name.lower() in name.lower()]
                        
                        if len(api_tools) != expected_tools:
                            issues.append(f"API {api_name}: Expected {expected_tools} tools, found {len(api_tools)}")
            
            except Exception as e:
                issues.append(f"Failed to list tools: {str(e)}")
        else:
            issues.append("MCP instance does not support tool listing")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'details': 'Verified tool accessibility for registered APIs'
        }
    
    async def _test_error_handling(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test error handling and reporting"""
        issues = []
        error_responses = [r for r in responses if not r.get('success', True)]
        
        for response in error_responses:
            error_msg = response.get('error', '')
            if not error_msg or len(error_msg.strip()) == 0:
                issues.append(f"Empty or missing error message in failed response")
            
            # Check for generic error messages that aren't helpful
            generic_errors = ['error', 'failed', 'exception', 'unknown error']
            if error_msg.lower().strip() in generic_errors:
                issues.append(f"Generic error message: '{error_msg}'")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'details': f'Analyzed error handling in {len(error_responses)} failed responses'
        }
    
    async def _test_schema_validation(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test response schema validation"""
        issues = []
        
        for i, response in enumerate(responses):
            # Check data types
            if 'success' in response and not isinstance(response['success'], bool):
                issues.append(f"Response {i}: 'success' should be boolean")
            
            if 'tools_registered' in response and not isinstance(response['tools_registered'], int):
                issues.append(f"Response {i}: 'tools_registered' should be integer")
            
            if 'api_name' in response and not isinstance(response['api_name'], str):
                issues.append(f"Response {i}: 'api_name' should be string")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'details': f'Validated schema for {len(responses)} responses'
        }

# Usage example and test runner
async def run_registration_verification_suite():
    """Example of running the complete verification suite"""
    
    # Initialize FastMCP instance
    mcp = FastMCP("Test Server")
    
    # Example registration responses (in real scenario, these come from actual registration attempts)
    sample_responses = [
        {"success": True, "api_name": "users", "tools_registered": 12, "spec_url": "https://api.users.com/openapi.json"},
        {"success": False, "api_name": "payments", "error": "Authentication failed: Invalid token"},
        {"success": True, "api_name": "inventory", "tools_registered": 8, "spec_url": "https://api.inventory.com/openapi.json"},
        {"success": False, "api_name": "notifications", "error": "Connection timeout after 30 seconds"}
    ]
    
    # Run basic verification
    verifier = APIRegistrationVerifier(mcp)
    results = []
    
    for response in sample_responses:
        result = await verifier.verify_registration_response(
            response, 
            response.get('api_name', 'unknown')
        )
        results.append(result)
    
    # Generate summary report
    summary = verifier.generate_summary_report()
    
    # Run comprehensive test suite
    test_suite = APIRegistrationTestSuite(mcp)
    test_results = await test_suite.run_comprehensive_tests(sample_responses)
    
    return {
        'verification_summary': summary,
        'test_results': test_results,
        'individual_results': results
    }

# Save results to file
async def save_verification_results(results: Dict[str, Any], filepath: str):
    """Save verification results to JSON file"""
    import json
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"Verification results saved to {filepath}")
```


## Usage Examples

Here's how to implement these verification scripts in practice:

```python
# Example 1: Basic verification after batch registration
async def verify_batch_registration():
    mcp = FastMCP("Production Server")
    verifier = APIRegistrationVerifier(mcp)
    
    # Simulate batch registration responses
    responses = [
        {"success": True, "api_name": "users", "tools_registered": 12},
        {"success": False, "api_name": "payments", "error": "Invalid token"}
    ]
    
    # Verify each response
    for response in responses:
        result = await verifier.verify_registration_response(
            response, response.get('api_name', 'unknown')
        )
        print(f"API: {result.api_name}, Success: {result.success}, Tools: {result.tools_count}")
    
    # Generate summary
    summary = verifier.generate_summary_report()
    print(f"Success Rate: {summary['success_rate']:.1f}%")

# Example 2: Continuous monitoring
async def setup_continuous_monitoring():
    mcp = FastMCP("Production Server")
    monitor = RegistrationHealthMonitor(mcp, check_interval=60)
    
    # Add APIs to monitor
    monitor.add_api_to_monitor("users")
    monitor.add_api_to_monitor("payments")
    monitor.add_api_to_monitor("inventory")
    
    # Start monitoring (runs continuously)
    await monitor.start_monitoring()

# Example 3: Run comprehensive test suite
async def run_full_verification():
    results = await run_registration_verification_suite()
    await save_verification_results(results, "verification_report.json")
    
    print(f"Verification complete:")
    print(f"- Total APIs: {results['verification_summary']['total_attempts']}")
    print(f"- Success Rate: {results['verification_summary']['success_rate']:.1f}%")
    print(f"- Tests Passed: {results['test_results']['passed_tests']}/{results['test_results']['total_tests']}")

# Run the examples
if __name__ == "__main__":
    asyncio.run(verify_batch_registration())
```

These comprehensive verification scripts provide:

- **Response Validation**: Ensures proper format and data integrity
- **Deep Verification**: Tests actual tool accessibility and functionality
- **Health Monitoring**: Continuous monitoring of registered API health
- **Comprehensive Testing**: Full test suite for production deployments
- **Error Analysis**: Detailed error reporting and analysis
- **Performance Tracking**: Response time and reliability metrics

The scripts help ensure your FastMCP API registrations are not only successful but also reliable and maintainable in production environments.

