#!/usr/bin/env python3
"""
Integration Services Startup Script

This script ensures all required services are running for the P1-CC-02 
integration tests between InGest-LLM.as and memOS.as.
"""

import subprocess
import sys
import time
import os
import json
from pathlib import Path

def run_command(cmd, cwd=None, capture=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            capture_output=capture, 
            text=True,
            shell=True if isinstance(cmd, str) else False
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_service_health(url, service_name, timeout=10):
    """Check if a service is healthy."""
    try:
        import requests
        response = requests.get(f"{url}/health", timeout=timeout)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}

def start_core_services():
    """Start core services required for integration tests."""
    print("🚀 Starting core integration services...")
    print("=" * 60)
    
    devenviro_path = Path(__file__).parent.parent / "devenviro.as"
    
    if not devenviro_path.exists():
        print(f"❌ DevEnviro path not found: {devenviro_path}")
        return False
    
    # Create network if it doesn't exist
    print("🌐 Ensuring Docker network exists...")
    success, stdout, stderr = run_command([
        'docker', 'network', 'create', 'apexsigma_net'
    ])
    if success or "already exists" in stderr:
        print("✅ Docker network ready")
    else:
        print(f"⚠️  Network creation issue: {stderr}")
    
    # Start essential services for integration tests
    essential_services = ['postgres', 'qdrant', 'redis', 'neo4j']
    
    print(f"\n🔧 Starting essential services: {', '.join(essential_services)}")
    
    success, stdout, stderr = run_command([
        'docker-compose', '-f', 'docker-compose.yml',
        'up', '-d'
    ] + essential_services, cwd=devenviro_path)
    
    if not success:
        print(f"❌ Failed to start services: {stderr}")
        return False
    
    print("✅ Services started successfully")
    
    # Wait for services to be ready
    print("\n⏳ Waiting for services to be ready...")
    
    service_checks = {
        'PostgreSQL': ('localhost:5432', None),
        'Qdrant': ('http://localhost:6333', '/'),
        'Redis': ('localhost:6379', None),
        'Neo4j': ('http://localhost:7474', '/')
    }
    
    ready_services = {}
    
    for service, (url, endpoint) in service_checks.items():
        print(f"   🔍 Checking {service}...")
        
        if service == 'PostgreSQL':
            # Check PostgreSQL with pg_isready
            success, _, _ = run_command([
                'docker', 'exec', 'devenviro_postgres', 
                'pg_isready', '-h', 'localhost', '-p', '5432'
            ])
            ready_services[service] = success
        elif service == 'Redis':
            # Check Redis with ping
            success, _, _ = run_command([
                'docker', 'exec', 'devenviro_redis',
                'redis-cli', 'ping'
            ])
            ready_services[service] = success
        else:
            # HTTP-based checks
            for attempt in range(15):  # 30 seconds total
                try:
                    import requests
                    response = requests.get(url + (endpoint or ''), timeout=2)
                    if response.status_code in [200, 404]:  # Neo4j returns 404 for root
                        ready_services[service] = True
                        break
                except:
                    pass
                time.sleep(2)
            else:
                ready_services[service] = False
    
    # Report service status
    print("\n📊 Service Status:")
    all_ready = True
    for service, is_ready in ready_services.items():
        status = "✅ Ready" if is_ready else "❌ Not Ready"
        print(f"   {service:12} : {status}")
        if not is_ready:
            all_ready = False
    
    if all_ready:
        print("\n🎉 All services are ready for integration testing!")
    else:
        print("\n⚠️  Some services are not ready. Tests may fail.")
    
    return all_ready

def verify_integration_endpoints():
    """Verify that integration endpoints are accessible."""
    print("\n🔍 Verifying integration endpoints...")
    
    endpoints = {
        'InGest-LLM.as': 'http://localhost:8000',
        'memOS.as': 'http://localhost:8091'
    }
    
    endpoint_status = {}
    
    for service, url in endpoints.items():
        print(f"   📡 Checking {service}...")
        is_ready, health_data = check_service_health(url, service)
        endpoint_status[service] = is_ready
        
        if is_ready:
            print(f"      ✅ {service} is healthy")
            if 'integration_ready' in health_data:
                integration_ready = health_data['integration_ready']
                ready_icon = "✅" if integration_ready else "⚠️ "
                print(f"      {ready_icon} Integration ready: {integration_ready}")
        else:
            print(f"      ❌ {service} not responding")
    
    return endpoint_status

def main():
    """Main function to start all integration services."""
    print("🚀 APEXSIGMA INTEGRATION SERVICES STARTUP")
    print("Preparing for P1-CC-02 Integration Tests")
    print("=" * 60)
    
    # Check Docker
    print("🔍 Checking Docker availability...")
    docker_ok, _, _ = run_command(['docker', 'version'])
    if not docker_ok:
        print("❌ Docker is not available. Please start Docker Desktop.")
        return False
    print("✅ Docker is running")
    
    # Start core services
    if not start_core_services():
        print("\n💥 Failed to start core services")
        return False
    
    # Give services extra time to initialize
    print("\n⏳ Allowing services additional startup time...")
    time.sleep(10)
    
    # Verify integration endpoints (if services are running)
    endpoint_status = verify_integration_endpoints()
    
    # Final status
    print("\n" + "=" * 60)
    print("📋 INTEGRATION SERVICES STARTUP SUMMARY")
    print("=" * 60)
    
    services_ready = all(endpoint_status.values()) if endpoint_status else False
    
    if services_ready:
        print("🎉 All integration services are ready!")
        print("\n🧪 You can now run the integration tests:")
        print("   cd InGest-LLM.as")
        print("   python scripts/run_core_integration_tests.py")
        print("\n🌐 Service URLs:")
        print("   - InGest-LLM.as: http://localhost:8000/health")
        print("   - memOS.as: http://localhost:8091/health")
        print("   - Neo4j Browser: http://localhost:7474")
    else:
        print("⚠️  Not all services are ready for integration testing")
        print("\n🔧 Manual startup commands:")
        print("   cd devenviro.as")
        print("   docker-compose up -d postgres qdrant redis neo4j")
        print("   cd ../InGest-LLM.as")
        print("   poetry run uvicorn src.ingest_llm_as.main:app --reload")
        print("   cd ../memos.as")
        print("   uvicorn app.main:app --port 8091 --reload")
    
    return services_ready

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)