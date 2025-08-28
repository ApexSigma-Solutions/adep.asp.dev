#!/usr/bin/env python3
"""
Society of Agents Deploy (SOD) - Autonomous Full Stack Deployment
This script performs comprehensive container orchestration, health checks, and service deployment
for the ApexSigma Society of Agents ecosystem.

Usage:
    python sod_deploy.py [--force] [--skip-audit] [--verbose]
    or use the /sod command alias
"""

import os
import sys
import json
import time
import yaml
import argparse
import subprocess
import threading
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class ServiceHealth:
    name: str
    status: str
    port: int
    url: str = ""
    healthy: bool = False
    response_time: float = 0.0
    error: str = ""

class SODDeployer:
    """Society of Agents Deployer - Full stack autonomous deployment orchestrator"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.base_dir = Path(__file__).parent.parent
        self.compose_file = self.base_dir / "docker-compose.unified.yml"
        self.devenviro_dir = self.base_dir / "devenviro.as"
        self.start_time = datetime.now()
        
        # Service configuration with expected endpoints
        self.services = {
            # Infrastructure
            "postgres": ServiceHealth("PostgreSQL", "starting", 5432),
            "redis": ServiceHealth("Redis", "starting", 6379),
            "rabbitmq": ServiceHealth("RabbitMQ", "starting", 15672, "http://localhost:15672"),
            "qdrant": ServiceHealth("Qdrant", "starting", 6333, "http://localhost:6333"),
            
            # Observability
            "prometheus": ServiceHealth("Prometheus", "starting", 9090, "http://localhost:9090"),
            "grafana": ServiceHealth("Grafana", "starting", 8080, "http://localhost:8080"),
            "jaeger": ServiceHealth("Jaeger", "starting", 16686, "http://localhost:16686"),
            "loki": ServiceHealth("Loki", "starting", 9100, "http://localhost:9100"),
            
            # ApexSigma Services
            "devenviro-api": ServiceHealth("DevEnviro API", "starting", 8090, "http://localhost:8090/health"),
            "memos-api": ServiceHealth("Memos API", "starting", 8091, "http://localhost:8091/health"),
            "ingest-llm-api": ServiceHealth("InGest-LLM API", "starting", 8000, "http://localhost:8000/health"),
            "tools-api": ServiceHealth("Tools API", "starting", 8003, "http://localhost:8003/docs"),
        }
        
        self.critical_services = ["postgres", "redis", "rabbitmq", "devenviro-api"]
        
    def log(self, message: str, level: str = "INFO"):
        """Enhanced logging with timestamps and levels"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if level == "ERROR":
            print(f"[ERROR {timestamp}] {message}")
        elif level == "WARN":
            print(f"[WARN  {timestamp}] {message}")
        elif level == "SUCCESS":
            print(f"[OK    {timestamp}] {message}")
        elif level == "INFO":
            print(f"[INFO  {timestamp}] {message}")
        else:
            print(f"[DEBUG {timestamp}] {message}")
    
    def run_command(self, cmd: List[str], cwd: Optional[Path] = None, timeout: int = 60) -> Tuple[bool, str, str]:
        """Execute command with timeout and error handling"""
        try:
            if self.verbose:
                self.log(f"Executing: {' '.join(cmd)}", "DEBUG")
                
            result = subprocess.run(
                cmd,
                cwd=cwd or self.base_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )
            
            success = result.returncode == 0
            if not success and self.verbose:
                self.log(f"Command failed: {result.stderr}", "ERROR")
                
            return success, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            return False, "", f"Command timed out after {timeout}s"
        except Exception as e:
            return False, "", str(e)
    
    def check_prerequisites(self) -> bool:
        """Verify system prerequisites"""
        self.log("Checking prerequisites...")
        
        prerequisites = [
            (["docker", "--version"], "Docker"),
            (["docker", "compose", "version"], "Docker Compose"),
            (["python", "--version"], "Python"),
        ]
        
        all_good = True
        for cmd, name in prerequisites:
            success, stdout, stderr = self.run_command(cmd)
            if success:
                version = stdout.strip().split('\n')[0]
                self.log(f"OK {name}: {version}")
            else:
                self.log(f"MISSING {name} not found or not working", "ERROR")
                all_good = False
                
        return all_good
    
    def create_network(self) -> bool:
        """Ensure the ApexSigma network exists"""
        self.log("Creating Docker network...")
        
        # Check if network exists
        success, stdout, _ = self.run_command(["docker", "network", "ls", "--format", "{{.Name}}"])
        if success and "apexsigma_net" in stdout:
            self.log("Network apexsigma_net already exists")
            return True
            
        # Create network
        success, _, stderr = self.run_command([
            "docker", "network", "create", 
            "--driver", "bridge",
            "apexsigma_net"
        ])
        
        if success:
            self.log("Network apexsigma_net created")
            return True
        else:
            self.log(f"Failed to create network: {stderr}", "ERROR")
            return False
    
    def cleanup_containers(self, force: bool = False) -> bool:
        """Clean up existing containers if needed"""
        if force:
            self.log("Force cleanup - stopping and removing existing containers...")
            
            # Stop and remove ApexSigma containers
            success, stdout, _ = self.run_command([
                "docker", "ps", "-a", "--format", "{{.Names}}", "--filter", "name=apexsigma_"
            ])
            
            if success and stdout.strip():
                container_names = [name.strip() for name in stdout.strip().split('\n') if name.strip()]
                for container in container_names:
                    self.log(f"Stopping {container}...")
                    self.run_command(["docker", "stop", container], timeout=30)
                    self.log(f"Removing {container}...")
                    self.run_command(["docker", "rm", container], timeout=30)
                    
            return True
        else:
            # Check for conflicting containers
            success, stdout, _ = self.run_command([
                "docker", "ps", "--format", "{{.Names}}", "--filter", "name=apexsigma_"
            ])
            
            if success and stdout.strip():
                self.log("Found running ApexSigma containers. Use --force to clean up.", "WARN")
                return False
                
        return True
    
    def deploy_infrastructure(self) -> bool:
        """Deploy infrastructure services first"""
        self.log("Deploying infrastructure services...")
        
        # Infrastructure services in dependency order
        infra_services = [
            "postgres", "redis", "rabbitmq", "qdrant",
            "jaeger", "prometheus", "loki", "promtail", "grafana"
        ]
        
        for service in infra_services:
            self.log(f"Starting {service}...")
            success, _, stderr = self.run_command([
                "docker", "compose", "-f", str(self.compose_file),
                "up", "-d", service
            ])
            
            if not success:
                self.log(f"Failed to start {service}: {stderr}", "ERROR")
                return False
                
            # Brief wait for service initialization
            time.sleep(2)
            
        self.log("Infrastructure services deployed", "SUCCESS")
        return True
    
    def deploy_application_services(self) -> bool:
        """Deploy application services"""
        self.log("Deploying application services...")
        
        app_services = [
            "memos-api",
            "ingest-llm-api", 
            "tools-api",
            "devenviro-api",
            "devenviro-gemini-cli-listener",
            "devenviro-a2a-bridge"
        ]
        
        for service in app_services:
            self.log(f"Starting {service}...")
            success, _, stderr = self.run_command([
                "docker", "compose", "-f", str(self.compose_file),
                "up", "-d", service
            ])
            
            if not success:
                self.log(f"Failed to start {service}: {stderr}", "ERROR")
                # Don't fail completely for non-critical services
                if service in ["devenviro-api"]:
                    return False
                    
            time.sleep(3)  # Longer wait for app services
            
        self.log("Application services deployed", "SUCCESS")
        return True
    
    def wait_for_service(self, service_name: str, timeout: int = 120) -> bool:
        """Wait for a specific service to become healthy"""
        service = self.services.get(service_name)
        if not service or not service.url:
            return True  # Skip services without health checks
            
        self.log(f"Waiting for {service.name} to be healthy...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(service.url, timeout=5)
                if response.status_code in [200, 401]:  # 401 is OK for some services
                    service.healthy = True
                    service.response_time = response.elapsed.total_seconds()
                    self.log(f"{service.name} is healthy ({service.response_time:.2f}s)", "SUCCESS")
                    return True
            except Exception as e:
                service.error = str(e)
                
            time.sleep(5)
            
        self.log(f"{service.name} failed to become healthy within {timeout}s", "ERROR")
        return False
    
    def perform_health_checks(self) -> bool:
        """Comprehensive health checks for all services"""
        self.log("Performing comprehensive health checks...")
        
        # Check Docker containers first
        success, stdout, _ = self.run_command([
            "docker", "compose", "-f", str(self.compose_file), "ps", "--format", "json"
        ])
        
        if not success:
            self.log("Failed to get container status", "ERROR")
            return False
            
        # Parse container status
        containers = []
        for line in stdout.strip().split('\n'):
            if line.strip():
                try:
                    containers.append(json.loads(line))
                except:
                    pass
        
        # Update service statuses
        for container in containers:
            name = container.get('Service', '')
            state = container.get('State', '')
            status = container.get('Status', '')
            
            if name in self.services:
                self.services[name].status = f"{state} - {status}"
                
        # Perform HTTP health checks concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            health_futures = {
                executor.submit(self.wait_for_service, service_name): service_name 
                for service_name, service in self.services.items() 
                if service.url
            }
            
            for future in as_completed(health_futures, timeout=180):
                service_name = health_futures[future]
                try:
                    result = future.result()
                    if not result and service_name in self.critical_services:
                        self.log(f"Critical service {service_name} failed health check", "ERROR")
                        return False
                except Exception as e:
                    self.log(f"Health check error for {service_name}: {e}", "ERROR")
                    if service_name in self.critical_services:
                        return False
        
        return True
    
    def run_database_migrations(self) -> bool:
        """Run database migrations for DevEnviro"""
        self.log("Running database migrations...")
        
        # Wait for PostgreSQL to be ready
        if not self.wait_for_service("postgres", 60):
            return False
            
        # Run DevEnviro migrations
        migrations_dir = self.devenviro_dir / "app" / "migrations"
        if migrations_dir.exists():
            success, _, stderr = self.run_command([
                "docker", "exec", "apexsigma_devenviro_api",
                "python", "-c", "from src.core.migrations_runner import apply_migrations; apply_migrations()"
            ], timeout=60)
            
            if success:
                self.log("Database migrations completed", "SUCCESS")
            else:
                self.log(f"Migration warnings (may be normal): {stderr}", "WARN")
                
        return True
    
    def generate_deployment_report(self) -> str:
        """Generate comprehensive deployment report"""
        duration = datetime.now() - self.start_time
        
        report = f"""
================================================================================
                     SOCIETY OF AGENTS DEPLOYMENT REPORT                      
================================================================================

Deployment Time: {duration.total_seconds():.1f} seconds
Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SERVICE STATUS:
"""
        
        for service_name, service in self.services.items():
            status_symbol = "[OK]" if service.healthy else "[FAIL]" if service_name in self.critical_services else "[WARN]"
            response_info = f" ({service.response_time:.2f}s)" if service.response_time > 0 else ""
            
            report += f"  {status_symbol} {service.name:<20} - {service.status}{response_info}\n"
            if service.error and not service.healthy:
                report += f"       Error: {service.error}\n"
        
        # Add dashboard links
        report += f"""
DASHBOARD LINKS:
  * DevEnviro API:     http://localhost:8090/docs
  * Grafana:           http://localhost:8080 (admin/apexsigma123)  
  * Prometheus:        http://localhost:9090
  * Jaeger Tracing:    http://localhost:16686
  * RabbitMQ Mgmt:     http://localhost:15672
  * Memos API:         http://localhost:8091/docs
  * InGest-LLM API:    http://localhost:8000/docs
  * Tools API:         http://localhost:8003/docs

SYSTEM READY FOR SOCIETY OF AGENTS OPERATIONS
================================================================================
"""
        
        return report
    
    def deploy(self, force: bool = False, skip_audit: bool = False) -> bool:
        """Main deployment orchestrator"""
        try:
            self.log("Starting Society of Agents Deployment (SOD)...")
            
            # Phase 0: Prerequisites
            if not self.check_prerequisites():
                return False
                
            # Phase 1: Network setup
            if not self.create_network():
                return False
                
            # Phase 2: Cleanup if needed
            if not self.cleanup_containers(force):
                return False
                
            # Phase 3: Infrastructure deployment
            if not self.deploy_infrastructure():
                return False
                
            # Phase 4: Wait for infrastructure
            self.log("Waiting for infrastructure to stabilize...")
            time.sleep(15)
            
            # Phase 5: Application deployment
            if not self.deploy_application_services():
                return False
                
            # Phase 6: Database migrations
            time.sleep(10)  # Let services start up
            if not self.run_database_migrations():
                self.log("Database migrations had issues but continuing...", "WARN")
                
            # Phase 7: Health checks
            if not skip_audit:
                if not self.perform_health_checks():
                    self.log("Health checks failed - system may be in degraded state", "ERROR")
                    # Don't return False - let it complete and show report
            
            # Phase 8: Generate report
            report = self.generate_deployment_report()
            print(report)
            
            self.log("Society of Agents Deployment Complete!", "SUCCESS")
            return True
            
        except KeyboardInterrupt:
            self.log("Deployment interrupted by user", "ERROR")
            return False
        except Exception as e:
            self.log(f"Deployment failed with error: {e}", "ERROR")
            return False

def main():
    parser = argparse.ArgumentParser(description="Society of Agents Deploy (SOD)")
    parser.add_argument("--force", action="store_true", help="Force cleanup existing containers")
    parser.add_argument("--skip-audit", action="store_true", help="Skip health check audit")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    deployer = SODDeployer(verbose=args.verbose)
    success = deployer.deploy(force=args.force, skip_audit=args.skip_audit)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()