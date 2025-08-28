#!/usr/bin/env python3
"""
Test Langfuse integration across ApexSigma ecosystem
"""

import asyncio
import httpx
import json

async def test_langfuse_ecosystem():
    """Test Langfuse observability across all services"""
    
    print("TESTING LANGFUSE ECOSYSTEM INTEGRATION")
    print("=" * 50)
    
    services = {
        "InGest-LLM.as": "http://localhost:8002",
        "DevEnviro.as": "http://localhost:8090", 
        "MemOS.as": "http://localhost:8091"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        for service_name, base_url in services.items():
            print(f"\nTesting {service_name}")
            print("-" * 30)
            
            try:
                # Test health endpoint
                health_response = await client.get(f"{base_url}/health")
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    print(f"SUCCESS: Health check: {health_data.get('status', 'ok')}")
                    
                    # Check for observability info
                    if 'observability' in health_data:
                        obs = health_data['observability']
                        print(f"   Metrics: {'ENABLED' if obs.get('metrics_enabled') else 'DISABLED'}")
                        print(f"   Tracing: {'ENABLED' if obs.get('tracing_enabled') else 'DISABLED'}")
                        print(f"   Logging: {'ENABLED' if obs.get('logging_structured') else 'DISABLED'}")
                    
                    # Check for integrations
                    if 'integrations' in health_data:
                        integ = health_data['integrations']
                        print(f"   Langfuse: {'CONNECTED' if integ.get('langfuse') else 'NOT_CONNECTED'}")
                        print(f"   Prometheus: {'CONNECTED' if integ.get('prometheus') else 'NOT_CONNECTED'}")
                        print(f"   Jaeger: {'CONNECTED' if integ.get('jaeger') else 'NOT_CONNECTED'}")
                        
                else:
                    print(f"WARNING: Health check failed: {health_response.status_code}")
                    
            except Exception as e:
                print(f"ERROR: Connection failed: {e}")
                
        # Test a simple ingestion to trigger LLM tracing
        print(f"\nTesting LLM Trace Generation")
        print("-" * 30)
        
        try:
            test_payload = {
                "content": "Test content for Langfuse tracing verification",
                "metadata": {
                    "source": "langfuse_test",
                    "content_type": "text",
                    "tags": ["test", "observability"]
                },
                "chunk_size": 100,
                "process_async": False
            }
            
            ingest_response = await client.post(
                f"{services['InGest-LLM.as']}/ingest/text",
                json=test_payload
            )
            
            if ingest_response.status_code == 200:
                result = ingest_response.json()
                print(f"SUCCESS: Ingestion successful: {result.get('status', 'unknown')}")
                print(f"   Ingestion ID: {result.get('ingestion_id', 'N/A')}")
                print("TARGET: Check Langfuse dashboard for traces!")
            else:
                print(f"WARNING: Ingestion failed: {ingest_response.status_code}")
                print(f"   Response: {ingest_response.text[:200]}...")
                
        except Exception as e:
            print(f"ERROR: Ingestion test failed: {e}")
    
    print(f"\nNEXT STEPS:")
    print("1. Check Langfuse dashboard: https://cloud.langfuse.com")
    print("2. Look for traces from 'InGest-LLM.as' service")
    print("3. Verify trace data includes proper metadata")
    print("4. Confirm LLM calls are being captured")

if __name__ == "__main__":
    asyncio.run(test_langfuse_ecosystem())