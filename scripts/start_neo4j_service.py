#!/usr/bin/env python3
"""
Neo4j Service Starter for Integration Tests

This script ensures Neo4j is running for integration tests between
InGest-LLM.as and memOS.as services.
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_docker_running():
    """Check if Docker is running."""
    try:
        result = subprocess.run(['docker', 'version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker Desktop.")
        return False

def check_neo4j_running():
    """Check if Neo4j container is running."""
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=devenviro_neo4j', '--format', '{{.Names}}'],
            capture_output=True, text=True
        )
        return 'devenviro_neo4j' in result.stdout
    except:
        return False

def start_neo4j_service():
    """Start Neo4j service using docker-compose."""
    devenviro_path = Path(__file__).parent.parent / "devenviro.as"
    
    if not devenviro_path.exists():
        print(f"❌ DevEnviro path not found: {devenviro_path}")
        return False
        
    print("🚀 Starting Neo4j service...")
    
    try:
        # Create network if it doesn't exist
        subprocess.run([
            'docker', 'network', 'create', 'apexsigma_net'
        ], capture_output=True)
        
        # Start only Neo4j service
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.yml', 
            'up', '-d', 'neo4j'
        ], cwd=devenviro_path, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Failed to start Neo4j: {result.stderr}")
            return False
            
        print("✅ Neo4j service started successfully")
        
        # Wait for Neo4j to be ready
        print("⏳ Waiting for Neo4j to be ready...")
        for i in range(30):
            try:
                import requests
                response = requests.get('http://localhost:7474', timeout=2)
                if response.status_code == 200:
                    print("✅ Neo4j is ready!")
                    return True
            except:
                pass
            time.sleep(2)
            print(f"   Attempt {i+1}/30...")
            
        print("⚠️  Neo4j started but may not be fully ready")
        return True
        
    except Exception as e:
        print(f"❌ Error starting Neo4j: {e}")
        return False

def main():
    """Main function to ensure Neo4j is running."""
    print("🔍 Checking Neo4j service for integration tests...")
    print("=" * 50)
    
    # Check Docker
    if not check_docker_running():
        print("💥 Cannot start Neo4j without Docker")
        return False
    
    print("✅ Docker is running")
    
    # Check if Neo4j is already running
    if check_neo4j_running():
        print("✅ Neo4j is already running")
        return True
    
    # Start Neo4j
    if start_neo4j_service():
        print("\n🎉 Neo4j service is ready for integration tests!")
        print("🌐 Neo4j Browser: http://localhost:7474")
        print("🔌 Bolt URL: bolt://localhost:7687")
        print("🔐 Default credentials: neo4j/password")
        return True
    else:
        print("\n💥 Failed to start Neo4j service")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)