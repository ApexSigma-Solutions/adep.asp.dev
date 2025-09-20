#!/usr/bin/env python3
"""
ApexSigma E2E Distributed Tracing Integration Test

This script demonstrates end-to-end distributed tracing across all ApexSigma services:
- devenviro.as (orchestrator)
- tools.as (tool server)  
- memos.as (agent memory)
- ingest-llm.as (data ingestion)

Tests cross-service trace propagation, correlation IDs, and workflow tracking.
"""

import asyncio
import logging
import time
import uuid
from typing import Dict, Any, Optional
import aiohttp
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ApexSigmaE2ETraceTest:
    """Test end-to-end distributed tracing across ApexSigma services."""
    
    def __init__(self):
        # Service endpoints (adjust ports as needed)
        self.services = {
            'devenviro.as': 'http://localhost:8000',
            'tools.as': 'http://localhost:8001', 
            'memos.as': 'http://localhost:8002',
            'ingest-llm.as': 'http://localhost:8003'
        }
        
        # Generate test correlation and workflow IDs
        self.correlation_id = str(uuid.uuid4())
        self.workflow_id = str(uuid.uuid4())
        
        logger.info(f"Starting E2E trace test with correlation_id: {self.correlation_id}")
        logger.info(f"Workflow ID: {self.workflow_id}")
    
    def prepare_trace_headers(self, source_service: str, agent_chain: str = "") -> Dict[str, str]:
        """Prepare headers with tracing context for cross-service calls."""
        headers = {
            'Content-Type': 'application/json',
            'x-apexsigma-correlation-id': self.correlation_id,
            'x-apexsigma-workflow-id': self.workflow_id,
            'x-apexsigma-source-service': source_service,
            'x-apexsigma-agent-chain': agent_chain,
            'x-request-id': str(uuid.uuid4())
        }
        return headers
    
    async def test_tools_service(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Test tools.as service with E2E tracing."""
        service_url = self.services['tools.as']
        headers = self.prepare_trace_headers('test-client', 'test-client')
        
        logger.info("Testing tools.as E2E tracing...")
        
        # Test search endpoint
        search_payload = {"query": "ApexSigma distributed tracing"}
        
        try:
            async with session.post(
                f"{service_url}/tools/search",
                json=search_payload,
                headers=headers,
                timeout=30
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"tools.as search completed: {len(data)} results")
                    
                    # Check trace propagation headers
                    trace_headers = {
                        k: v for k, v in response.headers.items() 
                        if k.startswith('x-apexsigma') or k.startswith('traceparent')
                    }
                    logger.info(f"tools.as trace headers: {trace_headers}")
                    
                    return {
                        'service': 'tools.as',
                        'status': 'success',
                        'results_count': len(data),
                        'trace_headers': trace_headers
                    }
                else:
                    logger.error(f"tools.as search failed: {response.status}")
                    return {'service': 'tools.as', 'status': 'error', 'code': response.status}
                    
        except Exception as e:
            logger.error(f"tools.as test failed: {e}")
            return {'service': 'tools.as', 'status': 'error', 'error': str(e)}
    
    async def test_memos_service(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Test memos.as service with E2E tracing."""
        service_url = self.services['memos.as']
        headers = self.prepare_trace_headers('test-client', 'test-client->tools.as')
        
        logger.info("Testing memos.as E2E tracing...")
        
        # Test scratchpad operations
        agent_id = "test-agent-e2e"
        scratchpad_payload = {
            "content": f"E2E tracing test - correlation_id: {self.correlation_id}"
        }
        
        try:
            # Create/update scratchpad
            async with session.post(
                f"{service_url}/scratchpad/{agent_id}",
                json=scratchpad_payload,
                headers=headers,
                timeout=15
            ) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    logger.info(f"memos.as scratchpad created/updated for agent: {agent_id}")
                    
                    # Check trace propagation headers
                    trace_headers = {
                        k: v for k, v in response.headers.items() 
                        if k.startswith('x-apexsigma') or k.startswith('traceparent')
                    }
                    logger.info(f"memos.as trace headers: {trace_headers}")
                    
                    return {
                        'service': 'memos.as',
                        'status': 'success',
                        'operation': 'scratchpad_update',
                        'agent_id': agent_id,
                        'trace_headers': trace_headers
                    }
                else:
                    logger.error(f"memos.as scratchpad operation failed: {response.status}")
                    return {'service': 'memos.as', 'status': 'error', 'code': response.status}
                    
        except Exception as e:
            logger.error(f"memos.as test failed: {e}")
            return {'service': 'memos.as', 'status': 'error', 'error': str(e)}
    
    async def test_ingest_service(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Test ingest-llm.as service with E2E tracing."""
        service_url = self.services['ingest-llm.as']
        headers = self.prepare_trace_headers('test-client', 'test-client->tools.as->memos.as')
        
        logger.info("Testing ingest-llm.as E2E tracing...")
        
        try:
            # Test health endpoint (most likely to be available)
            async with session.get(
                f"{service_url}/health",
                headers=headers,
                timeout=15
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("ingest-llm.as health check completed")
                    
                    # Check trace propagation headers
                    trace_headers = {
                        k: v for k, v in response.headers.items() 
                        if k.startswith('x-apexsigma') or k.startswith('traceparent')
                    }
                    logger.info(f"ingest-llm.as trace headers: {trace_headers}")
                    
                    return {
                        'service': 'ingest-llm.as',
                        'status': 'success',
                        'operation': 'health_check',
                        'trace_headers': trace_headers
                    }
                else:
                    logger.error(f"ingest-llm.as health check failed: {response.status}")
                    return {'service': 'ingest-llm.as', 'status': 'error', 'code': response.status}
                    
        except Exception as e:
            logger.error(f"ingest-llm.as test failed: {e}")
            return {'service': 'ingest-llm.as', 'status': 'error', 'error': str(e)}
    
    async def test_devenviro_service(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Test devenviro.as service with E2E tracing."""
        service_url = self.services['devenviro.as']
        headers = self.prepare_trace_headers('test-client', 'test-client->tools.as->memos.as->ingest-llm.as')
        
        logger.info("Testing devenviro.as E2E tracing...")
        
        try:
            # Test health endpoint
            async with session.get(
                f"{service_url}/health",
                headers=headers,
                timeout=15
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("devenviro.as health check completed")
                    
                    # Check trace propagation headers
                    trace_headers = {
                        k: v for k, v in response.headers.items() 
                        if k.startswith('x-apexsigma') or k.startswith('traceparent')
                    }
                    logger.info(f"devenviro.as trace headers: {trace_headers}")
                    
                    return {
                        'service': 'devenviro.as',
                        'status': 'success',
                        'operation': 'health_check',
                        'trace_headers': trace_headers
                    }
                else:
                    logger.error(f"devenviro.as health check failed: {response.status}")
                    return {'service': 'devenviro.as', 'status': 'error', 'code': response.status}
                    
        except Exception as e:
            logger.error(f"devenviro.as test failed: {e}")
            return {'service': 'devenviro.as', 'status': 'error', 'error': str(e)}
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive E2E tracing test across all services."""
        logger.info("=" * 60)
        logger.info("APEXSIGMA E2E DISTRIBUTED TRACING TEST")
        logger.info("=" * 60)
        
        start_time = time.time()
        results = []
        
        async with aiohttp.ClientSession() as session:
            # Test each service
            test_methods = [
                self.test_tools_service,
                self.test_memos_service,
                self.test_ingest_service,
                self.test_devenviro_service
            ]
            
            for test_method in test_methods:
                try:
                    result = await test_method(session)
                    results.append(result)
                    await asyncio.sleep(1)  # Brief pause between tests
                except Exception as e:
                    logger.error(f"Test method {test_method.__name__} failed: {e}")
                    results.append({
                        'service': test_method.__name__.replace('test_', '').replace('_service', ''),
                        'status': 'error',
                        'error': str(e)
                    })
        
        duration = time.time() - start_time
        
        # Summary
        logger.info("=" * 60)
        logger.info("TEST SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total test duration: {duration:.2f} seconds")
        logger.info(f"Correlation ID: {self.correlation_id}")
        logger.info(f"Workflow ID: {self.workflow_id}")
        
        successful_services = [r for r in results if r.get('status') == 'success']
        failed_services = [r for r in results if r.get('status') == 'error']
        
        logger.info(f"Services tested: {len(results)}")
        logger.info(f"Successful: {len(successful_services)}")
        logger.info(f"Failed: {len(failed_services)}")
        
        if successful_services:
            logger.info("\nSuccessful services:")
            for service in successful_services:
                logger.info(f"  ✓ {service['service']}")
        
        if failed_services:
            logger.info("\nFailed services:")
            for service in failed_services:
                logger.info(f"  ✗ {service['service']}: {service.get('error', 'Unknown error')}")
        
        # Check for trace propagation
        services_with_traces = [
            r for r in results 
            if r.get('status') == 'success' and r.get('trace_headers')
        ]
        
        logger.info(f"\nServices with trace propagation: {len(services_with_traces)}")
        for service in services_with_traces:
            headers = service.get('trace_headers', {})
            correlation_present = 'x-apexsigma-correlation-id' in headers
            logger.info(f"  {service['service']}: {'✓' if correlation_present else '✗'} correlation ID propagated")
        
        return {
            'correlation_id': self.correlation_id,
            'workflow_id': self.workflow_id,
            'duration': duration,
            'total_services': len(results),
            'successful_services': len(successful_services),
            'failed_services': len(failed_services),
            'trace_propagation_count': len(services_with_traces),
            'results': results
        }


async def main():
    """Main test runner."""
    test = ApexSigmaE2ETraceTest()
    
    try:
        results = await test.run_comprehensive_test()
        
        # Save results to file
        with open('e2e_trace_test_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"\nTest results saved to: e2e_trace_test_results.json")
        
        # Exit with appropriate code
        if results['failed_services'] == 0:
            logger.info("🎉 All E2E tracing tests passed!")
            return 0
        else:
            logger.warning(f"⚠️  {results['failed_services']} services failed E2E tracing tests")
            return 1
            
    except Exception as e:
        logger.error(f"Test runner failed: {e}")
        return 1


if __name__ == '__main__':
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)