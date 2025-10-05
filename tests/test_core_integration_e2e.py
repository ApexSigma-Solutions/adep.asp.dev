"""
Core Integration Testing Suite for InGest-LLM.as and memOS.as

This test suite validates the complete workflow between the two services,
ensuring that data ingestion, processing, and memory storage work correctly.
This fulfills the P1-CC-02 task requirement for establishing the core 
integration testing suite.
"""

import asyncio
import json
import time
from typing import Dict, List, Optional
import pytest
import httpx
from pathlib import Path

# Service Configuration
INGEST_SERVICE_URL = "http://localhost:8000"
MEMOS_SERVICE_URL = "http://localhost:8091"
REQUEST_TIMEOUT = 60  # Increased for complex operations
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

# Test Data Templates
TEST_PROJECT_CONTEXT = {
    "project_name": "ApexSigma Integration Test",
    "source": "integration_test_suite",
    "environment": "test",
    "timestamp": None  # Will be set during test
}

class IntegrationTestError(Exception):
    """Custom exception for integration test failures"""
    pass

class ServiceValidator:
    """Helper class for validating service responses and states"""
    
    @staticmethod
    async def wait_for_service_ready(url: str, service_name: str, max_attempts: int = 10) -> bool:
        """Wait for a service to become ready with detailed logging."""
        print(f"\n🔍 Checking {service_name} service readiness...")
        
        for attempt in range(max_attempts):
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    response = await client.get(f"{url}/health")
                    
                    if response.status_code == 200:
                        health_data = response.json()
                        print(f"✅ {service_name} is ready: {health_data.get('status', 'running')}")
                        return True
                    else:
                        print(f"⚠️  {service_name} health check returned {response.status_code}")
                        
            except Exception as e:
                print(f"❌ {service_name} not ready (attempt {attempt + 1}/{max_attempts}): {e}")
            
            if attempt < max_attempts - 1:
                await asyncio.sleep(RETRY_DELAY)
        
        print(f"💥 {service_name} failed to become ready after {max_attempts} attempts")
        return False
    
    @staticmethod
    def validate_ingestion_response(response_data: Dict) -> None:
        """Validate the structure of an ingestion response."""
        required_fields = ["ingestion_id", "status", "total_chunks", "results"]
        missing_fields = [field for field in required_fields if field not in response_data]
        
        if missing_fields:
            raise IntegrationTestError(f"Missing required fields in ingestion response: {missing_fields}")
        
        if response_data["status"] not in ["completed", "pending", "processing"]:
            raise IntegrationTestError(f"Invalid ingestion status: {response_data['status']}")
        
        if response_data["total_chunks"] <= 0:
            raise IntegrationTestError("Total chunks must be greater than 0")
        
        # Validate each result chunk
        for i, result in enumerate(response_data["results"]):
            required_result_fields = ["memory_id", "status", "memory_tier"]
            missing_result_fields = [field for field in required_result_fields if field not in result]
            
            if missing_result_fields:
                raise IntegrationTestError(
                    f"Missing fields in result {i}: {missing_result_fields}"
                )
    
    @staticmethod
    def validate_memory_response(response_data: Dict, expected_memory_id: Optional[int] = None) -> None:
        """Validate the structure of a memory response."""
        if expected_memory_id and response_data.get("id") != expected_memory_id:
            raise IntegrationTestError(
                f"Memory ID mismatch. Expected: {expected_memory_id}, Got: {response_data.get('id')}"
            )
        
        required_fields = ["id", "content", "created_at"]
        missing_fields = [field for field in required_fields if field not in response_data]
        
        if missing_fields:
            raise IntegrationTestError(f"Missing required fields in memory response: {missing_fields}")

@pytest.fixture(scope="session")
async def service_health_check():
    """Ensure both services are healthy before running tests."""
    print("\n🚀 = CORE INTEGRATION TEST SUITE STARTING =")
    print("Validating service health before running integration tests...")
    
    # Check InGest-LLM.as service
    ingest_ready = await ServiceValidator.wait_for_service_ready(
        INGEST_SERVICE_URL, "InGest-LLM.as"
    )
    
    # Check memOS.as service
    memos_ready = await ServiceValidator.wait_for_service_ready(
        MEMOS_SERVICE_URL, "memOS.as"
    )
    
    if not ingest_ready:
        pytest.skip("InGest-LLM.as service is not available")
    
    if not memos_ready:
        pytest.skip("memOS.as service is not available")
    
    print("✅ Both services are ready for integration testing")
    return True

@pytest.fixture
def test_context():
    """Provide test context with unique identifiers."""
    timestamp = str(int(time.time()))
    context = TEST_PROJECT_CONTEXT.copy()
    context["timestamp"] = timestamp
    context["test_id"] = f"integration_test_{timestamp}"
    return context

@pytest.fixture
def sample_technical_content():
    """Provide technical content for testing code ingestion."""
    return """
# Integration Test Code Sample

class MemoryManager:
    '''Manages memory operations in the ApexSigma ecosystem'''
    
    def __init__(self, config):
        self.config = config
        self.connections = {}
    
    def store_memory(self, content, metadata):
        '''Store content in appropriate memory tier'''
        memory_tier = self._determine_tier(content, metadata)
        
        if memory_tier == 'procedural':
            return self._store_procedural(content, metadata)
        elif memory_tier == 'episodic':
            return self._store_episodic(content, metadata)
        else:
            return self._store_semantic(content, metadata)
    
    def _determine_tier(self, content, metadata):
        # Logic to determine appropriate memory tier
        content_type = metadata.get('content_type', 'text')
        
        if content_type == 'code':
            return 'procedural'
        elif 'task' in metadata.get('tags', []):
            return 'episodic'  
        else:
            return 'semantic'

# Integration patterns for agent collaboration
def create_agent_workflow(agents, task):
    '''Create collaborative workflow between agents'''
    workflow_steps = []
    
    for agent in agents:
        step = {
            'agent_id': agent.id,
            'capabilities': agent.get_capabilities(),
            'dependencies': agent.get_dependencies(),
            'task_context': task.context
        }
        workflow_steps.append(step)
    
    return workflow_steps
"""

@pytest.fixture  
def sample_documentation_content():
    """Provide documentation content for testing text ingestion."""
    return """
# ApexSigma Integration Documentation

## Overview
The ApexSigma ecosystem implements a Society of Agents architecture where specialized AI agents collaborate on complex development tasks. This integration testing suite validates the core workflow between InGest-LLM.as and memOS.as services.

## Architecture Components

### InGest-LLM.as Service
- **Purpose**: Data ingestion and preprocessing
- **Port**: 8000
- **Key Features**:
  - Text chunking and processing
  - Content type detection
  - Async processing capabilities
  - Integration with memOS.as for storage

### memOS.as Service  
- **Purpose**: Multi-tiered memory management
- **Port**: 8091
- **Memory Tiers**:
  1. **Tier 1 (Redis)**: Working memory and cache
  2. **Tier 2 (PostgreSQL + Qdrant)**: Episodic and procedural memory
  3. **Tier 3 (Neo4j)**: Semantic knowledge graph

## Integration Workflow
1. Content arrives at InGest-LLM.as via API
2. Content is analyzed and chunked appropriately
3. Memory tier is determined based on content type and metadata
4. Content is forwarded to memOS.as for storage
5. Storage confirmation is returned to the client

## Quality Assurance
This integration test suite ensures:
- Service health and connectivity
- End-to-end data flow
- Memory tier selection accuracy
- Error handling and recovery
- Performance under load

## Troubleshooting
If integration tests fail, check:
- Service availability and health
- Network connectivity between services
- Database connections (PostgreSQL, Redis, Qdrant, Neo4j)
- Configuration alignment between services
"""

class TestServiceConnectivity:
    """Test basic service connectivity and health."""
    
    @pytest.mark.asyncio
    async def test_ingest_service_detailed_health(self, service_health_check):
        """Test InGest-LLM.as detailed health check."""
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(f"{INGEST_SERVICE_URL}/health")
            
            assert response.status_code == 200
            health_data = response.json()
            
            # Validate health response structure
            assert "service" in health_data
            assert health_data["service"] == "InGest-LLM.as"
            assert "version" in health_data
            assert "dependencies" in health_data
            
            print(f"✅ InGest-LLM.as health: {json.dumps(health_data, indent=2)}")
    
    @pytest.mark.asyncio
    async def test_memos_service_detailed_health(self, service_health_check):
        """Test memOS.as detailed health check."""
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(f"{MEMOS_SERVICE_URL}/health")
            
            assert response.status_code == 200
            health_data = response.json()
            
            # Validate health response structure  
            assert "services" in health_data
            
            # Check database connectivity
            services = health_data["services"]
            expected_services = ["postgres", "qdrant", "redis"]
            
            for service_name in expected_services:
                assert service_name in services
                status = services[service_name]
                print(f"  📊 {service_name}: {status}")
                
            print(f"✅ memOS.as health: {json.dumps(health_data, indent=2)}")

class TestCoreIntegrationWorkflow:
    """Test the core integration workflow between services."""
    
    @pytest.mark.asyncio
    async def test_text_content_integration_flow(self, service_health_check, test_context, sample_documentation_content):
        """Test complete integration flow for text content."""
        print("\n📝 Testing text content integration flow...")
        
        # Prepare ingestion request
        ingestion_request = {
            "content": sample_documentation_content,
            "metadata": {
                **test_context,
                "content_type": "documentation",
                "title": "Integration Test Documentation",
                "tags": ["documentation", "integration", "test"],
                "author": "integration_test_suite"
            },
            "chunk_size": 800,
            "process_async": False
        }
        
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            print("  📤 Sending ingestion request to InGest-LLM.as...")
            
            # Step 1: Ingest content via InGest-LLM.as
            response = await client.post(
                f"{INGEST_SERVICE_URL}/ingest/text",
                json=ingestion_request
            )
            
            assert response.status_code == 200, f"Ingestion failed: {response.text}"
            ingestion_response = response.json()
            
            # Validate ingestion response
            ServiceValidator.validate_ingestion_response(ingestion_response)
            
            print(f"  ✅ Content ingested successfully")
            print(f"     - Ingestion ID: {ingestion_response['ingestion_id']}")
            print(f"     - Total chunks: {ingestion_response['total_chunks']}")
            print(f"     - Status: {ingestion_response['status']}")
            
            # Extract memory IDs for validation
            memory_ids = [result["memory_id"] for result in ingestion_response["results"]]
            memory_tiers = [result["memory_tier"] for result in ingestion_response["results"]]
            
            print(f"     - Memory IDs: {memory_ids}")
            print(f"     - Memory tiers: {memory_tiers}")
            
            # Wait for processing to complete
            await asyncio.sleep(3)
            
            # Step 2: Verify memories exist in memOS.as
            print("  🔍 Verifying memories in memOS.as...")
            
            verified_memories = []
            for memory_id in memory_ids:
                memory_response = await client.get(
                    f"{MEMOS_SERVICE_URL}/memories/{memory_id}"
                )
                
                if memory_response.status_code == 200:
                    memory_data = memory_response.json()
                    ServiceValidator.validate_memory_response(memory_data, memory_id)
                    verified_memories.append(memory_data)
                    print(f"     ✅ Memory {memory_id} verified in memOS.as")
                else:
                    raise IntegrationTestError(
                        f"Memory {memory_id} not found in memOS.as: {memory_response.status_code}"
                    )
            
            # Step 3: Test memory search functionality
            print("  🔍 Testing memory search functionality...")
            
            search_response = await client.get(
                f"{MEMOS_SERVICE_URL}/memory/search",
                params={"query": "integration test", "top_k": 10}
            )
            
            assert search_response.status_code == 200, f"Search failed: {search_response.text}"
            search_data = search_response.json()
            
            # Validate search found our content
            search_results = search_data.get("memories", {}).get("results", [])
            found_our_content = any(
                memory_id in [result.get("id") for result in search_results]
                for memory_id in memory_ids
            )
            
            assert found_our_content, "Ingested content not found in search results"
            print(f"     ✅ Search found {len(search_results)} relevant memories")
            
            return {
                "ingestion_response": ingestion_response,
                "verified_memories": verified_memories,
                "search_results": search_data
            }
    
    @pytest.mark.asyncio
    async def test_code_content_integration_flow(self, service_health_check, test_context, sample_technical_content):
        """Test complete integration flow for code content."""
        print("\n💻 Testing code content integration flow...")
        
        # Prepare ingestion request for code content
        ingestion_request = {
            "content": sample_technical_content,
            "metadata": {
                **test_context,
                "content_type": "code",
                "title": "Integration Test Code Sample", 
                "tags": ["code", "python", "integration", "test"],
                "author": "integration_test_suite",
                "language": "python"
            },
            "chunk_size": 600,
            "process_async": False
        }
        
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            print("  📤 Sending code ingestion request...")
            
            # Step 1: Ingest code content
            response = await client.post(
                f"{INGEST_SERVICE_URL}/ingest/text",
                json=ingestion_request
            )
            
            assert response.status_code == 200, f"Code ingestion failed: {response.text}"
            ingestion_response = response.json()
            
            ServiceValidator.validate_ingestion_response(ingestion_response)
            
            # Validate that code content uses procedural memory tier
            memory_tiers = [result["memory_tier"] for result in ingestion_response["results"]]
            assert all(tier == "procedural" for tier in memory_tiers), \
                f"Code content should use procedural memory tier, got: {memory_tiers}"
            
            print(f"  ✅ Code content stored in procedural memory tier")
            print(f"     - Total chunks: {ingestion_response['total_chunks']}")
            
            # Step 2: Verify procedural memory storage
            memory_ids = [result["memory_id"] for result in ingestion_response["results"]]
            
            for memory_id in memory_ids:
                memory_response = await client.get(
                    f"{MEMOS_SERVICE_URL}/memories/{memory_id}"
                )
                
                assert memory_response.status_code == 200, \
                    f"Code memory {memory_id} not found: {memory_response.status_code}"
                
                memory_data = memory_response.json()
                # Validate that this is indeed code content
                content = memory_data.get("content", "")
                assert "class" in content or "def" in content, \
                    "Stored content doesn't appear to be code"
                
                print(f"     ✅ Code memory {memory_id} verified")
            
            return ingestion_response
    
    @pytest.mark.asyncio 
    async def test_concurrent_ingestion_workflow(self, service_health_check, test_context):
        """Test concurrent ingestion requests to validate system stability."""
        print("\n🔄 Testing concurrent ingestion workflow...")
        
        async def single_concurrent_ingestion(session_id: int):
            """Single ingestion task for concurrent testing."""
            content = f"""
            Session {session_id} Integration Test Content
            
            This is test content for concurrent ingestion validation.
            Each session should be processed independently and stored correctly.
            
            Session details:
            - Session ID: {session_id}
            - Test Type: Concurrent Integration
            - Content Type: Text
            
            This content helps validate that the integration between 
            InGest-LLM.as and memOS.as can handle multiple simultaneous requests
            without data corruption or processing conflicts.
            """
            
            session_metadata = {
                **test_context,
                "content_type": "text",
                "title": f"Concurrent Test Session {session_id}",
                "tags": ["concurrent", "integration", "test", f"session_{session_id}"],
                "session_id": session_id
            }
            
            ingestion_request = {
                "content": content,
                "metadata": session_metadata,
                "chunk_size": 400,
                "process_async": False
            }
            
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                response = await client.post(
                    f"{INGEST_SERVICE_URL}/ingest/text",
                    json=ingestion_request
                )
                
                if response.status_code != 200:
                    raise IntegrationTestError(
                        f"Session {session_id} ingestion failed: {response.text}"
                    )
                
                return session_id, response.json()
        
        # Run 5 concurrent ingestion tasks
        print("  🚀 Starting 5 concurrent ingestion sessions...")
        
        tasks = [single_concurrent_ingestion(i) for i in range(1, 6)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Validate all sessions succeeded
        successful_sessions = []
        for result in results:
            if isinstance(result, Exception):
                raise IntegrationTestError(f"Concurrent session failed: {result}")
            
            session_id, response_data = result
            ServiceValidator.validate_ingestion_response(response_data)
            successful_sessions.append(session_id)
            print(f"     ✅ Session {session_id} completed successfully")
        
        print(f"  ✅ All {len(successful_sessions)} concurrent sessions completed")
        return successful_sessions

class TestErrorHandlingAndRecovery:
    """Test error handling and recovery scenarios."""
    
    @pytest.mark.asyncio
    async def test_malformed_content_handling(self, service_health_check, test_context):
        """Test how the system handles malformed or problematic content."""
        print("\n⚠️  Testing malformed content handling...")
        
        # Test empty content
        empty_request = {
            "content": "",
            "metadata": {**test_context, "content_type": "text", "title": "Empty Test"}
        }
        
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{INGEST_SERVICE_URL}/ingest/text",
                json=empty_request
            )
            
            # Should reject empty content
            assert response.status_code == 422, \
                f"Empty content should be rejected, got: {response.status_code}"
            print("     ✅ Empty content correctly rejected")
        
        # Test invalid content type
        invalid_request = {
            "content": "Test content",
            "metadata": {
                **test_context,
                "content_type": "invalid_type",
                "title": "Invalid Type Test"
            }
        }
        
        response = await client.post(
            f"{INGEST_SERVICE_URL}/ingest/text",
            json=invalid_request
        )
        
        # Should handle gracefully
        assert response.status_code in [422, 400], \
            f"Invalid content type should be rejected, got: {response.status_code}"
        print("     ✅ Invalid content type correctly handled")
    
    @pytest.mark.asyncio
    async def test_service_recovery_simulation(self, service_health_check):
        """Test how the system behaves when services are temporarily unavailable."""
        print("\n🔧 Testing service recovery scenarios...")
        
        # This test would ideally simulate service downtime
        # For now, we test timeout handling with very short timeouts
        
        async with httpx.AsyncClient(timeout=1) as client:  # Very short timeout
            try:
                response = await client.get(f"{INGEST_SERVICE_URL}/health")
                print("     ⚠️  Service responded faster than expected timeout")
            except httpx.TimeoutException:
                print("     ✅ Timeout handling working correctly")
            except Exception as e:
                print(f"     ℹ️  Other exception during timeout test: {e}")

class TestPerformanceValidation:
    """Test performance characteristics of the integration."""
    
    @pytest.mark.asyncio
    async def test_large_content_processing(self, service_health_check, test_context):
        """Test processing of larger content chunks."""
        print("\n📈 Testing large content processing...")
        
        # Generate larger content (but within reasonable limits)
        large_content = "\n".join([
            f"Line {i}: This is a large content test for integration validation. "
            f"Each line contains unique content to test chunking and processing capabilities. "
            f"The system should handle this content efficiently and store it appropriately."
            for i in range(200)  # About 20KB of content
        ])
        
        large_content_request = {
            "content": large_content,
            "metadata": {
                **test_context,
                "content_type": "text",
                "title": "Large Content Integration Test",
                "tags": ["large", "performance", "integration"]
            },
            "chunk_size": 1000,  # Larger chunks
            "process_async": False
        }
        
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{INGEST_SERVICE_URL}/ingest/text",
                json=large_content_request
            )
            
            processing_time = time.time() - start_time
            
            assert response.status_code == 200, f"Large content processing failed: {response.text}"
            ingestion_response = response.json()
            
            ServiceValidator.validate_ingestion_response(ingestion_response)
            
            print(f"     ✅ Large content processed successfully")
            print(f"        - Content size: ~20KB")
            print(f"        - Processing time: {processing_time:.2f}s")
            print(f"        - Chunks created: {ingestion_response['total_chunks']}")
            print(f"        - Avg time per chunk: {processing_time/ingestion_response['total_chunks']:.3f}s")
            
            return processing_time, ingestion_response

# Test execution markers
pytestmark = [
    pytest.mark.integration,
    pytest.mark.e2e,
    pytest.mark.asyncio
]

if __name__ == "__main__":
    # Allow running tests directly with detailed output
    import sys
    
    print("🚀 Core Integration Test Suite - Direct Execution Mode")
    print("=" * 60)
    
    # This would run the tests if executed directly
    # In practice, use: pytest test_core_integration_e2e.py -v -s
    print("To run this test suite, use:")
    print("pytest test_core_integration_e2e.py -v -s")
    print("\nOr for specific test categories:")
    print("pytest test_core_integration_e2e.py -k 'connectivity' -v")
    print("pytest test_core_integration_e2e.py -k 'workflow' -v") 
    print("pytest test_core_integration_e2e.py -k 'error' -v")
    print("pytest test_core_integration_e2e.py -k 'performance' -v")