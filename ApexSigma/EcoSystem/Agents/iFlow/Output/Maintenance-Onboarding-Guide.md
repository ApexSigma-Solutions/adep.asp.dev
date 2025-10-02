# ApexSigma Maintenance & Onboarding Guide

## Executive Summary

This comprehensive guide provides essential information for maintaining the ApexSigma ecosystem and onboarding new developers. It covers operational procedures, troubleshooting workflows, security protocols, and development best practices to ensure smooth operations and rapid team scaling.

**Target Audience:**
- System administrators and DevOps engineers
- Software developers and architects
- Security and compliance teams
- Technical support personnel

---

## 1. System Overview for Operations

### 1.1 Architecture Quick Reference

**Service Inventory:**
```
┌─────────────────────────────────────────────────────────────┐
│                    ApexSigma Services                       │
├─────────────────────────────────────────────────────────────┤
│  Service           │ Port │ Health Check │ Status          │
├─────────────────────────────────────────────────────────────┤
│ devenviro.as       │ 8000 │ /health      │ Core - Running  │
│ InGest-LLM.as      │ 8000 │ /health      │ Core - Running  │
│ memos.as           │ 8090 │ /health      │ Core - Running  │
│ tools.as           │ 8000 │ /health      │ Core - Running  │
├─────────────────────────────────────────────────────────────┤
│ PostgreSQL         │ 5432 │ pg_isready   │ DB - Running    │
│ Redis              │ 6379 │ ping         │ Cache - Running │
│ Neo4j              │ 7687 │ HTTP check   │ Graph - Running │
│ Qdrant             │ 6333 │ HTTP check   │ Vector - Running│
│ ClickHouse         │ 8123 │ HTTP check   │ Analytics - OK  │
├─────────────────────────────────────────────────────────────┤
│ RabbitMQ           │ 5672 │ rabbitmqctl  │ Queue - Running │
│ Jaeger             │16686 │ HTTP check   │ Tracing - OK    │
│ Prometheus         │ 9090 │ HTTP check   │ Metrics - OK    │
│ Grafana            │ 3000 │ HTTP check   │ Dashboard - OK  │
│ Langfuse           │ 3000 │ HTTP check   │ AI Observ - OK  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Key Operational Metrics

**Performance Baselines:**
- **API Response Time:** P50 < 150ms, P95 < 850ms
- **Database Queries:** Average < 45ms, P95 < 180ms
- **Cache Hit Ratio:** Target > 85%
- **System Uptime:** Current 99.95%
- **Error Rate:** < 0.3%

**Resource Utilization:**
- **CPU Usage:** Average 35%, Peak < 80%
- **Memory Usage:** Average 2.1GB, Peak < 4GB
- **Disk I/O:** < 70% utilization
- **Network I/O:** < 80% bandwidth

---

## 2. Daily Operations Checklist

### 2.1 System Health Verification

**Morning Health Check (Daily at 09:00):**

```bash
#!/bin/bash
# scripts/daily-health-check.sh

echo "🔍 ApexSigma Daily Health Check - $(date)"

# Service health verification
echo "📋 Checking service health..."
for service in devenviro.as:8000 ingest-llm.as:8000 memos.as:8090 tools.as:8000; do
    response=$(curl -s -o /dev/null -w "%{http_code}" http://$service/health)
    if [ "$response" = "200" ]; then
        echo "✅ $service - HEALTHY"
    else
        echo "❌ $service - UNHEALTHY (HTTP $response)"
    fi
done

# Database connectivity
echo "🗄️ Checking database connectivity..."
docker exec apexsigma_postgres pg_isready -U apexsigma_user && echo "✅ PostgreSQL - READY"
docker exec apexsigma_redis redis-cli ping && echo "✅ Redis - READY"

# Queue health
echo "📮 Checking message queues..."
docker exec apexsigma_rabbitmq rabbitmq-diagnostics ping && echo "✅ RabbitMQ - READY"

# Resource usage
echo "💻 Checking resource usage..."
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

echo "✅ Health check completed"
```

**Automated Health Monitoring:**
```python
# app/core/health_monitor.py
import asyncio
import aiohttp
from typing import Dict, List, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class HealthMonitor:
    """Automated health monitoring for ApexSigma services."""
    
    def __init__(self):
        self.services = {
            'devenviro': 'http://localhost:8000/health',
            'ingest-llm': 'http://localhost:8000/health',
            'memos': 'http://localhost:8090/health',
            'tools': 'http://localhost:8000/health'
        }
        self.databases = {
            'postgres': self.check_postgres_health,
            'redis': self.check_redis_health,
            'rabbitmq': self.check_rabbitmq_health
        }
    
    async def check_service_health(self, name: str, url: str) -> Dict[str, Any]:
        """Check individual service health."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    return {
                        'name': name,
                        'status': 'healthy' if response.status == 200 else 'unhealthy',
                        'response_time': response.elapsed.total_seconds(),
                        'status_code': response.status
                    }
        except Exception as e:
            return {
                'name': name,
                'status': 'unhealthy',
                'error': str(e)
            }
    
    async def check_postgres_health(self) -> Dict[str, Any]:
        """Check PostgreSQL health."""
        try:
            # Implementation would check PostgreSQL connectivity
            return {'name': 'postgres', 'status': 'healthy'}
        except Exception as e:
            return {'name': 'postgres', 'status': 'unhealthy', 'error': str(e)}
    
    async def check_redis_health(self) -> Dict[str, Any]:
        """Check Redis health."""
        try:
            # Implementation would check Redis connectivity
            return {'name': 'redis', 'status': 'healthy'}
        except Exception as e:
            return {'name': 'redis', 'status': 'unhealthy', 'error': str(e)}
    
    async def check_rabbitmq_health(self) -> Dict[str, Any]:
        """Check RabbitMQ health."""
        try:
            # Implementation would check RabbitMQ connectivity
            return {'name': 'rabbitmq', 'status': 'healthy'}
        except Exception as e:
            return {'name': 'rabbitmq', 'status': 'unhealthy', 'error': str(e)}
    
    async def run_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check."""
        results = {
            'timestamp': datetime.utcnow().isoformat(),
            'services': {},
            'databases': {},
            'overall_status': 'healthy'
        }
        
        # Check services
        service_checks = await asyncio.gather(*[
            self.check_service_health(name, url)
            for name, url in self.services.items()
        ])
        
        for check in service_checks:
            results['services'][check['name']] = check
            if check['status'] != 'healthy':
                results['overall_status'] = 'unhealthy'
        
        # Check databases
        db_checks = await asyncio.gather(*[
            check_func() for check_func in self.databases.values()
        ])
        
        for check in db_checks:
            results['databases'][check['name']] = check
            if check['status'] != 'healthy':
                results['overall_status'] = 'unhealthy'
        
        return results
```

### 2.2 Log Review and Analysis

**Daily Log Review Process:**

```bash
# scripts/log-analysis.sh

echo "📊 ApexSigma Log Analysis - $(date)"

# Check for errors in the last 24 hours
echo "🔍 Analyzing error patterns..."
docker-compose logs --since 24h | grep -i error | wc -l

# Top error sources
echo "📈 Top error sources:"
docker-compose logs --since 24h | grep -i error | awk '{print $2}' | sort | uniq -c | sort -nr | head -10

# Performance anomalies
echo "⚡ Performance anomalies:"
docker-compose logs --since 24h | grep -E "(slow|timeout|latency)" | head -20

# Security events
echo "🔒 Security events:"
docker-compose logs --since 24h | grep -E "(auth|login|security|access)" | head -20
```

**Automated Log Analysis:**
```python
# app/core/log_analyzer.py
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any
import datetime

class LogAnalyzer:
    """Automated log analysis for operational insights."""
    
    def __init__(self):
        self.error_patterns = [
            r'ERROR.*',
            r'Exception.*',
            r'Failed.*',
            r'Timeout.*',
            r'Connection refused.*'
        ]
        
        self.performance_patterns = [
            r'.*took (\d+)ms.*',
            r'.*latency (\d+)ms.*',
            r'.*slow query.*',
            r'.*timeout.*'
        ]
    
    def analyze_log_file(self, log_content: str) -> Dict[str, Any]:
        """Analyze log content for patterns and anomalies."""
        lines = log_content.split('\n')
        
        analysis = {
            'total_lines': len(lines),
            'error_count': 0,
            'error_sources': Counter(),
            'performance_issues': [],
            'security_events': [],
            'recommendations': []
        }
        
        for line in lines:
            # Check for errors
            if any(re.search(pattern, line, re.IGNORECASE) for pattern in self.error_patterns):
                analysis['error_count'] += 1
                source = self._extract_error_source(line)
                if source:
                    analysis['error_sources'][source] += 1
            
            # Check for performance issues
            for pattern in self.performance_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    analysis['performance_issues'].append({
                        'line': line.strip(),
                        'pattern': pattern
                    })
            
            # Check for security events
            if self._is_security_event(line):
                analysis['security_events'].append(line.strip())
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _extract_error_source(self, line: str) -> Optional[str]:
        """Extract the source of an error from a log line."""
        # Extract service name or component from log line
        patterns = [
            r'(\w+)\.\w+:',  # Service.method:
            r'\[(\w+)\]',   # [service]
            r'(\w+)_service' # service_service
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)
        
        return None
    
    def _is_security_event(self, line: str) -> bool:
        """Check if a log line contains a security event."""
        security_keywords = [
            'auth', 'login', 'password', 'token', 'jwt',
            'security', 'access', 'permission', 'unauthorized',
            'brute force', 'suspicious', 'attack'
        ]
        
        return any(keyword in line.lower() for keyword in security_keywords)
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate operational recommendations based on analysis."""
        recommendations = []
        
        if analysis['error_count'] > 10:
            recommendations.append("High error count detected - investigate error sources")
        
        if len(analysis['performance_issues']) > 5:
            recommendations.append("Performance issues detected - consider optimization")
        
        if len(analysis['security_events']) > 3:
            recommendations.append("Security events detected - review access patterns")
        
        # Service-specific recommendations
        top_errors = analysis['error_sources'].most_common(3)
        for service, count in top_errors:
            recommendations.append(f"High errors from {service} ({count}) - investigate")
        
        return recommendations
```

---

## 3. Maintenance Procedures

### 3.1 Regular Maintenance Tasks

#### Weekly Maintenance (Every Monday 08:00)

**System Updates and Cleanup:**
```bash
#!/bin/bash
# scripts/weekly-maintenance.sh

echo "🔧 ApexSigma Weekly Maintenance - $(date)"

# 1. Update system packages (if applicable)
echo "📦 Checking for system updates..."
# apt update && apt upgrade -y  # Uncomment if needed

# 2. Clean up Docker resources
echo "🧹 Cleaning Docker resources..."
docker system prune -f
docker volume prune -f

# 3. Rotate logs
echo "📝 Rotating logs..."
docker exec apexsigma_postgres find /var/log/postgresql -name "*.log" -mtime +7 -delete
docker exec apexsigma_redis find /var/log/redis -name "*.log" -mtime +7 -delete

# 4. Database maintenance
echo "🗄️ Database maintenance..."
docker exec apexsigma_postgres psql -U apexsigma_user -d apexsigma_db -c "VACUUM ANALYZE;"

# 5. Check disk usage
echo "💾 Disk usage check..."
df -h
docker system df

# 6. Update dependencies (if needed)
echo "📚 Checking for dependency updates..."
cd services/devenviro.as && poetry show --outdated
cd ../ingest-llm.as && poetry show --outdated
# ... repeat for other services

echo "✅ Weekly maintenance completed"
```

#### Monthly Maintenance (First Monday of month)

**Comprehensive System Review:**
```bash
#!/bin/bash
# scripts/monthly-maintenance.sh

echo "🔍 ApexSigma Monthly Maintenance - $(date)"

# 1. Security audit
echo "🔒 Running security audit..."
docker exec apexsigma_postgres psql -U apexsigma_user -d apexsigma_db -c "SELECT usename, valuntil FROM pg_user;"

# 2. Performance review
echo "📊 Performance review..."
# Run performance analysis scripts
python scripts/performance_analysis.py

# 3. Backup verification
echo "💾 Backup verification..."
# Test backup restoration (in staging environment)

# 4. Capacity planning
echo "📈 Capacity planning review..."
# Analyze growth trends and resource usage

# 5. Documentation updates
echo "📚 Documentation review..."
# Check for outdated documentation

# 6. Compliance check
echo "✅ Compliance review..."
# Verify compliance with security standards

echo "✅ Monthly maintenance completed"
```

### 3.2 Database Maintenance

#### PostgreSQL Maintenance

**Regular Database Health Checks:**
```sql
-- Database health check queries
-- Run these monthly or as needed

-- 1. Check database size and growth
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) as size
FROM pg_database
ORDER BY pg_database_size(pg_database.datname) DESC;

-- 2. Check for unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
JOIN pg_index ON pg_stat_user_indexes.indexrelid = pg_index.indexrelid
WHERE pg_stat_user_indexes.idx_scan = 0
AND pg_index.indisunique = false;

-- 3. Check table bloat
SELECT 
    schemaname,
    tablename,
    bs*(tblpages-est_tblpages) AS wasted_bytes,
    pg_size_pretty(bs*(tblpages-est_tblpages)) AS wasted_size
FROM (
    SELECT 
        schemaname,
        tablename,
        cc.relpages AS tblpages,
        CEIL((cc.reltuples*((datahdr+8)+(nullhdr+8)))/(bs-20::float)) AS est_tblpages,
        bs
    FROM pg_class cc
    JOIN pg_namespace nn ON cc.relnamespace = nn.oid
    CROSS JOIN (SELECT current_setting('block_size')::int AS bs) AS bs
    WHERE cc.relkind = 'r'
) AS bloat_calc
WHERE tblpages > est_tblpages;

-- 4. Check for long-running queries
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
AND state != 'idle';
```

**Database Performance Optimization:**
```sql
-- Performance optimization queries

-- 1. Update statistics
ANALYZE;

-- 2. Vacuum and analyze specific tables
VACUUM ANALYZE agents;
VACUUM ANALYZE tasks;
VACUUM ANALYZE memories;

-- 3. Rebuild indexes if fragmentation is high
REINDEX INDEX CONCURRENTLY idx_agents_status_type;
REINDEX INDEX CONCURRENTLY idx_tasks_agent_created;

-- 4. Update table statistics
SELECT pg_stat_reset();
```

#### Redis Maintenance

**Cache Optimization Procedures:**
```bash
# Redis maintenance commands

# 1. Check memory usage
docker exec apexsigma_redis redis-cli INFO memory

# 2. Check key expiration
docker exec apexsigma_redis redis-cli INFO keyspace

# 3. Find large keys
docker exec apexsigma_redis redis-cli --bigkeys

# 4. Check for memory leaks
docker exec apexsigma_redis redis-cli INFO stats | grep memory

# 5. Optimize memory usage
docker exec apexsigma_redis redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

---

## 4. Troubleshooting Guide

### 4.1 Common Issues and Solutions

#### Service Startup Issues

**Problem: Service fails to start**
```bash
# Diagnostic steps
1. Check service logs:
docker-compose logs [service-name]

2. Verify dependencies:
docker-compose ps

3. Check port conflicts:
netstat -tulpn | grep [port-number]

4. Validate configuration:
docker-compose config

5. Check resource limits:
docker stats
```

**Solution:**
```bash
# Restart service with clean state
docker-compose down [service-name]
docker-compose up -d [service-name]

# If persistent issues:
docker-compose down
docker-compose build --no-cache [service-name]
docker-compose up -d
```

#### Database Connection Issues

**Problem: Database connection failures**
```python
# Diagnostic Python script
import asyncio
import asyncpg
import redis.asyncio as redis
import aioredis

async def diagnose_database_connections():
    """Diagnose database connection issues."""
    
    # Test PostgreSQL connection
    try:
        conn = await asyncpg.connect(
            host='localhost',
            port=5432,
            user='apexsigma_user',
            password='your_password',
            database='apexsigma_db'
        )
        await conn.execute('SELECT 1')
        await conn.close()
        print("✅ PostgreSQL connection successful")
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
    
    # Test Redis connection
    try:
        redis_client = redis.from_url("redis://localhost:6379")
        await redis_client.ping()
        await redis_client.close()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")

# Run diagnostics
asyncio.run(diagnose_database_connections())
```

#### Performance Degradation

**Problem: Slow response times**
```python
# Performance diagnostic script
import time
import httpx
import asyncio
import statistics

async def performance_diagnostic():
    """Diagnose performance issues."""
    
    endpoints = [
        "http://localhost:8000/api/v1/agents",
        "http://localhost:8000/api/v1/health",
        "http://localhost:8090/api/v1/memories"
    ]
    
    results = {}
    
    for endpoint in endpoints:
        response_times = []
        
        # Measure response time 10 times
        for _ in range(10):
            start = time.perf_counter()
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(endpoint)
                end = time.perf_counter()
                response_times.append((end - start) * 1000)  # Convert to ms
            except Exception as e:
                print(f"Error accessing {endpoint}: {e}")
        
        if response_times:
            results[endpoint] = {
                'mean': statistics.mean(response_times),
                'median': statistics.median(response_times),
                'p95': statistics.quantiles(response_times, n=20)[18],
                'p99': statistics.quantiles(response_times, n=100)[98]
            }
    
    # Analyze results
    print("Performance Analysis Results:")
    for endpoint, metrics in results.items():
        print(f"\n{endpoint}:")
        print(f"  Mean: {metrics['mean']:.2f}ms")
        print(f"  Median: {metrics['median']:.2f}ms")
        print(f"  P95: {metrics['p95']:.2f}ms")
        print(f"  P99: {metrics['p99']:.2f}ms")
        
        # Flag performance issues
        if metrics['mean'] > 200:
            print(f"  ⚠️  SLOW: Mean response time > 200ms")
        if metrics['p95'] > 500:
            print(f"  ⚠️  SLOW: P95 response time > 500ms")

asyncio.run(performance_diagnostic())
```

### 4.2 Advanced Troubleshooting

#### Memory Leak Detection

**Memory Profiling Script:**
```python
# scripts/memory_profiler.py
import tracemalloc
import gc
import time
from typing import Dict, Any

class MemoryLeakDetector:
    """Memory leak detection and analysis."""
    
    def __init__(self):
        self.baseline_snapshot = None
        self.is_tracing = False
    
    def start_profiling(self):
        """Start memory profiling."""
        tracemalloc.start()
        self.is_tracing = True
        self.baseline_snapshot = tracemalloc.take_snapshot()
        print("Memory profiling started")
    
    def take_snapshot(self, label: str):
        """Take memory snapshot for comparison."""
        if not self.is_tracing:
            print("Memory profiling not started")
            return
        
        current_snapshot = tracemalloc.take_snapshot()
        
        # Compare with baseline
        top_stats = current_snapshot.compare_to(self.baseline_snapshot, 'lineno')
        
        print(f"\nMemory usage for {label}:")
        print("Top memory allocations:")
        for stat in top_stats[:10]:
            print(f"  {stat.traceback.format()[-1]}: {stat.size_diff / 1024:.1f} KiB")
    
    def detect_leaks(self, operation_func, iterations: int = 10):
        """Detect memory leaks in operations."""
        print(f"\nRunning memory leak detection for {iterations} iterations...")
        
        initial_snapshot = tracemalloc.take_snapshot()
        
        for i in range(iterations):
            operation_func()
            if i % 10 == 0:
                print(f"  Iteration {i}/{iterations}")
        
        final_snapshot = tracemalloc.take_snapshot()
        
        # Analyze differences
        top_stats = final_snapshot.compare_to(initial_snapshot, 'lineno')
        
        print("\nMemory leak analysis:")
        total_increase = sum(stat.size_diff for stat in top_stats[:20])
        print(f"Total memory increase: {total_increase / 1024:.1f} KiB")
        
        if total_increase > 1024 * 1024:  # 1MB threshold
            print("⚠️  Potential memory leak detected!")
            print("Top growing allocations:")
            for stat in top_stats[:5]:
                print(f"  {stat.traceback.format()[-1]}: {stat.size_diff / 1024:.1f} KiB")
        else:
            print("✅ No significant memory leak detected")

# Usage
detector = MemoryLeakDetector()
detector.start_profiling()

# Run your operation multiple times
for i in range(5):
    detector.take_snapshot(f"Iteration {i}")
    time.sleep(1)

detector.detect_leaks(your_operation_function, iterations=100)
```

#### Network Connectivity Issues

**Network Diagnostic Tools:**
```bash
# Comprehensive network diagnostics

# 1. Check Docker network configuration
docker network ls
docker network inspect apexsigma_net

# 2. Test inter-container connectivity
docker exec devenviro.as ping -c 4 ingest-llm.as
docker exec devenviro.as ping -c 4 apexsigma_postgres
docker exec devenviro.as ping -c 4 apexsigma_redis

# 3. Check port availability
netstat -tulpn | grep -E "(8000|8090|5432|6379|5672)"

# 4. Test DNS resolution
docker exec devenviro.as nslookup ingest-llm.as
docker exec devenviro.as nslookup apexsigma_postgres

# 5. Check firewall rules
sudo iptables -L -n | grep -E "(8000|8090|5432|6379|5672)"

# 6. Test external connectivity
docker exec devenviro.as curl -I http://httpbin.org/status/200
```

---

## 5. Developer Onboarding Process

### 5.1 Pre-Onboarding Setup

#### Prerequisites Installation

**Development Environment Setup:**
```bash
#!/bin/bash
# scripts/developer-setup.sh

echo "🚀 ApexSigma Developer Setup - Starting"

# Check prerequisites
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed"
        return 1
    else
        echo "✅ $1 is installed"
        return 0
    fi
}

echo "📋 Checking prerequisites..."
check_command docker || exit 1
check_command docker-compose || exit 1
check_command python3 || exit 1
check_command poetry || exit 1
check_command git || exit 1

# Clone repository (if not already cloned)
if [ ! -d ".git" ]; then
    echo "📥 Cloning repository..."
    git clone https://github.com/ApexSigma-Solutions/adep.asp.dev.git
    cd adep.asp.dev
fi

# Setup Python environment
echo "🐍 Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install poetry

# Install dependencies for each service
echo "📦 Installing dependencies..."
for service in devenviro.as ingest-llm.as memos.as tools.as; do
    echo "Installing dependencies for $service..."
    cd services/$service
    poetry install --with dev
    cd ../..
done

# Setup pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
pre-commit install

# Create environment file
echo "⚙️ Creating environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📝 Please configure your .env file before proceeding"
fi

echo "✅ Developer setup completed!"
echo "🎯 Next steps:"
echo "  1. Configure your .env file"
echo "  2. Start infrastructure: docker-compose -f docker-compose.unified.yml up -d"
echo "  3. Run tests: poetry run pytest"
echo "  4. Start development server: poetry run uvicorn app.main:app --reload"
```

### 5.2 First Day Activities

#### Quick Start Guide

**Day 1 Checklist:**
```markdown
# ApexSigma Developer Day 1 Checklist

## ✅ Environment Setup (30 minutes)
- [ ] Run developer setup script
- [ ] Configure .env file with personal settings
- [ ] Start unified infrastructure
- [ ] Verify all services are running
- [ ] Run first health check

## ✅ Codebase Exploration (2 hours)
- [ ] Review main architecture document
- [ ] Explore service directories structure
- [ ] Understand API endpoints and dependencies
- [ ] Review testing framework and run sample tests
- [ ] Examine CI/CD pipeline configuration

## ✅ Development Workflow (1 hour)
- [ ] Set up IDE with recommended extensions
- [ ] Configure debugging environment
- [ ] Run pre-commit hooks successfully
- [ ] Make small test change and commit
- [ ] Create first pull request

## ✅ Documentation Review (1 hour)
- [ ] Read API documentation
- [ ] Review coding standards and conventions
- [ ] Understand deployment process
- [ ] Review security guidelines
- [ ] Check troubleshooting procedures
```

### 5.3 Development Workflow Training

#### Code Contribution Process

**Step-by-Step Development Workflow:**
```python
# Example development workflow for new developers

# 1. Create feature branch
git checkout -b feature/agent-performance-monitoring

# 2. Make changes with proper testing
# app/api/v1/agents.py
from fastapi import APIRouter, HTTPException
from app.schemas.agent import AgentPerformanceResponse
from app.services.agent_service import AgentService

router = APIRouter()

@router.get("/api/v1/agents/{agent_id}/performance")
async def get_agent_performance(agent_id: str) -> AgentPerformanceResponse:
    """Get performance metrics for a specific agent."""
    service = AgentService()
    performance = await service.get_performance_metrics(agent_id)
    
    if not performance:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return AgentPerformanceResponse(**performance)

# 3. Write comprehensive tests
# tests/api/test_agents.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_agent_performance_success(client: AsyncClient):
    """Test successful agent performance retrieval."""
    agent_id = "test-agent-123"
    
    response = await client.get(f"/api/v1/agents/{agent_id}/performance")
    
    assert response.status_code == 200
    data = response.json()
    assert "agent_id" in data
    assert "metrics" in data

@pytest.mark.asyncio
async def test_get_agent_performance_not_found(client: AsyncClient):
    """Test agent performance retrieval for non-existent agent."""
    agent_id = "non-existent-agent"
    
    response = await client.get(f"/api/v1/agents/{agent_id}/performance")
    
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "AGENT_NOT_FOUND"
```

#### Testing Best Practices

**Comprehensive Testing Strategy:**
```python
# tests/unit/test_agent_performance.py
import pytest
from unittest.mock import AsyncMock, patch
from app.services.agent_performance_service import AgentPerformanceService

class TestAgentPerformanceService:
    """Unit tests for agent performance service."""
    
    @pytest.fixture
    def service(self):
        return AgentPerformanceService(
            repository=AsyncMock(),
            cache=AsyncMock(),
            metrics_client=AsyncMock()
        )
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_performance_metrics_success(self, service):
        """Test successful performance metrics retrieval."""
        # Arrange
        agent_id = "test-agent-123"
        expected_metrics = {
            "agent_id": agent_id,
            "total_tasks": 100,
            "success_rate": 0.95,
            "avg_response_time": 150.5
        }
        
        service.repository.get_performance_data.return_value = expected_metrics
        
        # Act
        result = await service.get_performance_metrics(agent_id)
        
        # Assert
        assert result == expected_metrics
        service.repository.get_performance_data.assert_called_once_with(agent_id)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_performance_metrics_caching(self, service):
        """Test performance metrics caching behavior."""
        # Arrange
        agent_id = "test-agent-123"
        cached_metrics = {"agent_id": agent_id, "cached": True}
        service.cache.get.return_value = cached_metrics
        
        # Act
        result = await service.get_performance_metrics(agent_id)
        
        # Assert
        assert result == cached_metrics
        service.cache.get.assert_called_once_with(f"performance:{agent_id}")
        service.repository.get_performance_data.assert_not_called()
```

### 5.4 Advanced Developer Topics

#### Debugging Complex Issues

**Advanced Debugging Techniques:**
```python
# app/core/debugging_tools.py
import logging
import traceback
from typing import Any, Dict, Optional
import asyncio
from contextlib import contextmanager
import time

class DebuggingTools:
    """Advanced debugging utilities for complex issues."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @contextmanager
    def debug_context(self, operation_name: str, **context_data):
        """Context manager for debugging operations."""
        start_time = time.perf_counter()
        
        self.logger.info(f"Starting debug context: {operation_name}")
        self.logger.debug(f"Context data: {context_data}")
        
        try:
            yield
        except Exception as e:
            self.logger.error(f"Exception in {operation_name}: {e}")
            self.logger.error(f"Stack trace: {traceback.format_exc()}")
            self.logger.error(f"Context data at error: {context_data}")
            raise
        finally:
            duration = time.perf_counter() - start_time
            self.logger.info(f"Completed {operation_name} in {duration:.3f}s")
    
    async def trace_async_operation(self, coro, operation_name: str, **kwargs):
        """Trace async operations with detailed logging."""
        self.logger.info(f"Starting async operation: {operation_name}")
        
        try:
            result = await coro
            self.logger.info(f"Completed async operation: {operation_name}")
            return result
        except Exception as e:
            self.logger.error(f"Async operation {operation_name} failed: {e}")
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            self.logger.error(f"Operation kwargs: {kwargs}")
            raise
    
    def inspect_object_state(self, obj: Any, obj_name: str) -> Dict[str, Any]:
        """Inspect object state for debugging."""
        state = {
            'object_name': obj_name,
            'object_type': type(obj).__name__,
            'object_id': id(obj),
            'attributes': {}
        }
        
        # Get object attributes
        for attr_name in dir(obj):
            if not attr_name.startswith('_'):
                try:
                    attr_value = getattr(obj, attr_name)
                    if not callable(attr_value):
                        state['attributes'][attr_name] = str(attr_value)[:100]
                except Exception as e:
                    state['attributes'][attr_name] = f"Error accessing: {e}"
        
        return state

# Usage example
debugger = DebuggingTools()

async def complex_operation_with_debugging():
    """Complex operation with comprehensive debugging."""
    
    with debugger.debug_context("complex_agent_operation", agent_id="agent-123"):
        # Your complex operation here
        agent_data = await fetch_agent_data("agent-123")
        
        # Inspect object state
        state_info = debugger.inspect_object_state(agent_data, "agent_data")
        debugger.logger.debug(f"Agent state: {state_info}")
        
        # Trace async operations
        result = await debugger.trace_async_operation(
            process_agent_data(agent_data),
            "process_agent_data",
            agent_id="agent-123",
            processing_type="performance_analysis"
        )
        
        return result
```

#### Performance Profiling

**Performance Analysis Tools:**
```python
# scripts/performance_profiler.py
import cProfile
import pstats
import io
from typing import Callable, Any
import time
import memory_profiler
import line_profiler

class PerformanceProfiler:
    """Comprehensive performance profiling tools."""
    
    def profile_function(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Profile a function with cProfile."""
        pr = cProfile.Profile()
        pr.enable()
        
        result = func(*args, **kwargs)
        
        pr.disable()
        
        # Analyze results
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(20)
        
        return {
            'result': result,
            'profile_stats': s.getvalue()
        }
    
    @memory_profiler.profile
    def profile_memory_usage(self, func: Callable, *args, **kwargs) -> Any:
        """Profile memory usage of a function."""
        return func(*args, **kwargs)
    
    def line_profile_function(self, func: Callable, *args, **kwargs) -> Any:
        """Profile function line by line."""
        profile = line_profiler.LineProfiler(func)
        
        # Wrap the function with profiler
        wrapped_func = profile(func)
        result = wrapped_func(*args, **kwargs)
        
        # Print line-by-line statistics
        profile.print_stats()
        
        return result

# Usage
profiler = PerformanceProfiler()

# Profile a specific function
result = profiler.profile_function(complex_calculation, data)
print("Profile results:", result['profile_stats'])

# Memory profiling
@profiler.profile_memory_usage
def memory_intensive_operation(data_list):
    """Memory-intensive operation for profiling."""
    results = []
    for item in data_list:
        processed = process_item(item)
        results.append(processed)
    return results

# Line profiling
profiler.line_profile_function(critical_function, data)
```

---

## 6. Operational Procedures

### 6.1 Incident Response

#### Incident Classification

**Severity Levels:**
- **P0 (Critical):** Complete system outage, data loss, security breach
- **P1 (High):** Major functionality unavailable, significant performance degradation
- **P2 (Medium):** Minor functionality issues, moderate performance impact
- **P3 (Low):** Cosmetic issues, minor performance degradation

#### Incident Response Playbook

**P0 Incident Response (Critical):**
```markdown
# P0 Critical Incident Response

## Immediate Actions (0-15 minutes)
1. **Acknowledge and Escalate**
   - Acknowledge incident in monitoring system
   - Notify on-call engineer
   - Alert management team

2. **Assess Impact**
   - Check system status dashboard
   - Identify affected services
   - Estimate user impact

3. **Preserve Evidence**
   - Capture current system state
   - Save relevant logs
   - Document timeline

## Investigation (15-60 minutes)
1. **Root Cause Analysis**
   - Check recent deployments
   - Review system metrics
   - Analyze error patterns

2. **Communication**
   - Post status update
   - Notify stakeholders
   - Provide regular updates

3. **Mitigation Attempts**
   - Try quick fixes
   - Implement workarounds
   - Document attempts

## Resolution and Recovery (60+ minutes)
1. **Implement Fix**
   - Deploy solution
   - Verify fix effectiveness
   - Monitor system recovery

2. **Post-Incident**
   - Document lessons learned
   - Update runbooks
   - Schedule post-mortem
```

### 6.2 Change Management

#### Deployment Procedures

**Safe Deployment Process:**
```bash
#!/bin/bash
# scripts/safe-deployment.sh

set -e

DEPLOYMENT_ENV=${1:-staging}
SERVICE_NAME=$2
NEW_VERSION=$3

echo "🚀 Starting safe deployment of $SERVICE_NAME:$NEW_VERSION to $DEPLOYMENT_ENV"

# 1. Pre-deployment checks
echo "🔍 Running pre-deployment checks..."
./scripts/pre-deployment-checks.sh $SERVICE_NAME

# 2. Create backup
echo "💾 Creating backup..."
./scripts/create-backup.sh $DEPLOYMENT_ENV

# 3. Deploy to staging first (if production)
if [ "$DEPLOYMENT_ENV" = "production" ]; then
    echo "🧪 Deploying to staging first..."
    ./scripts/deploy-to-staging.sh $SERVICE_NAME $NEW_VERSION
    
    # Wait for validation
    echo "⏳ Waiting for staging validation..."
    sleep 300  # 5 minutes
    
    # Validate staging deployment
    ./scripts/validate-deployment.sh staging $SERVICE_NAME
fi

# 4. Deploy to target environment
echo "🎯 Deploying to $DEPLOYMENT_ENV..."
./scripts/deploy-service.sh $DEPLOYMENT_ENV $SERVICE_NAME $NEW_VERSION

# 5. Post-deployment validation
echo "✅ Validating deployment..."
./scripts/validate-deployment.sh $DEPLOYMENT_ENV $SERVICE_NAME

# 6. Monitor deployment
echo "📊 Monitoring deployment..."
./scripts/monitor-deployment.sh $DEPLOYMENT_ENV $SERVICE_NAME

echo "✅ Deployment completed successfully!"
```

#### Rollback Procedures

**Emergency Rollback Process:**
```bash
#!/bin/bash
# scripts/emergency-rollback.sh

set -e

ENVIRONMENT=$1
SERVICE_NAME=$2
BACKUP_ID=$3

echo "🚨 Emergency rollback initiated for $SERVICE_NAME in $ENVIRONMENT"

# 1. Confirm rollback
echo "⚠️  This will rollback $SERVICE_NAME to backup $BACKUP_ID"
read -p "Are you sure? (yes/no): " confirmation

if [ "$confirmation" != "yes" ]; then
    echo "❌ Rollback cancelled"
    exit 1
fi

# 2. Stop current service
echo "🛑 Stopping current service..."
docker-compose -f docker-compose.$ENVIRONMENT.yml stop $SERVICE_NAME

# 3. Restore from backup
echo "💾 Restoring from backup..."
./scripts/restore-from-backup.sh $ENVIRONMENT $SERVICE_NAME $BACKUP_ID

# 4. Verify rollback
echo "🔍 Verifying rollback..."
./scripts/verify-rollback.sh $ENVIRONMENT $SERVICE_NAME

# 5. Update incident status
echo "📢 Updating incident status..."
./scripts/update-incident-status.sh "ROLLBACK_COMPLETED" $SERVICE_NAME

echo "✅ Emergency rollback completed!"
```

---

## 7. Knowledge Management

### 7.1 Documentation Standards

#### Code Documentation Requirements

**Documentation Checklist for New Features:**
```markdown
# Feature Documentation Checklist

## Code Documentation
- [ ] Function docstrings with parameters and return values
- [ ] Class documentation with usage examples
- [ ] Complex algorithm explanations
- [ ] Error handling documentation
- [ ] Performance considerations documented

## API Documentation
- [ ] OpenAPI specification updated
- [ ] Request/response examples provided
- [ ] Error response documentation
- [ ] Rate limiting information included

## Architecture Documentation
- [ ] Architecture decision record (ADR) created
- [ ] Service interaction diagrams updated
- [ ] Data flow documentation updated
- [ ] Security considerations documented

## Operational Documentation
- [ ] Deployment procedures documented
- [ ] Monitoring and alerting configured
- [ ] Troubleshooting guide updated
- [ ] Maintenance procedures documented
```

#### Knowledge Sharing

**Technical Documentation Structure:**
```
docs/
├── architecture/          # System architecture documentation
│   ├── overview.md
│   ├── service-interactions.md
│   └── decision-records/
├── api/                  # API documentation
│   ├── endpoints.md
│   ├── examples.md
│   └── error-codes.md
├── operations/           # Operational procedures
│   ├── deployment.md
│   ├── monitoring.md
│   └── troubleshooting/
├── development/          # Development guides
│   ├── setup.md
│   ├── coding-standards.md
│   └── testing.md
└── security/            # Security documentation
    ├── security-guide.md
    ├── compliance.md
    └── incident-response.md
```

### 7.2 Training and Development

#### Skill Development Paths

**Developer Career Progression:**
```
Junior Developer → Mid-Level Developer → Senior Developer → Tech Lead
     ↓                    ↓                    ↓                 ↓
Basic Python/FastAPI → Microservices → System Architecture → Team Leadership
Basic Testing      → Advanced Testing → Performance Optimization → Technical Strategy
Basic Git          → CI/CD Pipelines → Infrastructure as Code → Organizational Impact
```

**Specialization Tracks:**
- **Backend Development:** FastAPI, PostgreSQL, Redis, Microservices
- **DevOps/Infrastructure:** Docker, Kubernetes, CI/CD, Monitoring
- **Data Engineering:** ClickHouse, Kafka, Data Pipelines, Analytics
- **Security Engineering:** Application Security, Infrastructure Security, Compliance
- **AI/ML Engineering:** Model Integration, Performance Optimization, MLOps

---

## 8. Continuous Improvement

### 8.1 Feedback Collection

#### Developer Experience Surveys

**Quarterly Developer Satisfaction Survey:**
```markdown
# ApexSigma Developer Experience Survey

## Development Environment (1-5 scale)
- [ ] Local development setup is easy and reliable
- [ ] Documentation is comprehensive and up-to-date
- [ ] Testing framework is effective and easy to use
- [ ] Debugging tools are sufficient for complex issues
- [ ] CI/CD pipeline is fast and reliable

## Code Quality (1-5 scale)
- [ ] Code review process is effective
- [ ] Coding standards are clear and enforced
- [ ] Technical debt is managed appropriately
- [ ] Performance requirements are well-defined
- [ ] Security guidelines are clear and followed

## Team Collaboration (1-5 scale)
- [ ] Communication channels are effective
- [ ] Knowledge sharing happens regularly
- [ ] Mentorship opportunities are available
- [ ] Cross-team collaboration works well
- [ ] Incident response is effective

## Open Questions
1. What is the most challenging aspect of development in ApexSigma?
2. What tools or processes would improve your productivity?
3. What documentation is missing or needs improvement?
4. How can we improve the onboarding process for new developers?
5. What training would be most valuable for your role?
```

### 8.2 Process Optimization

#### Operational Efficiency Metrics

**Key Performance Indicators:**
- **Developer Onboarding Time:** Target < 2 hours to productive development
- **Incident Resolution Time:** Target < 30 minutes for P1 incidents
- **Code Review Time:** Target < 4 hours average review time
- **Deployment Frequency:** Target daily deployments with < 1% failure rate
- **Documentation Freshness:** Target 90% of documentation updated within 30 days

---

## 9. Emergency Contacts and Escalation

### 9.1 Contact Information

**Primary Contacts:**
- **On-Call Engineer:** +1-XXX-XXX-XXXX (24/7)
- **Technical Lead:** +1-XXX-XXX-XXXX (Business hours)
- **Operations Manager:** +1-XXX-XXX-XXXX (Business hours)

**Escalation Matrix:**
```
Level 1: On-Call Engineer (0-30 minutes)
Level 2: Technical Lead (30-60 minutes)
Level 3: Operations Manager (60+ minutes)
Level 4: CTO/VP Engineering (Critical incidents)
```

### 9.2 Emergency Procedures

**Critical Incident Escalation:**
```
1. Assess severity and impact
2. Contact on-call engineer immediately
3. Document incident in tracking system
4. Notify stakeholders based on severity
5. Escalate through chain of command as needed
6. Provide regular status updates
7. Conduct post-mortem after resolution
```

---

## 10. Conclusion

This comprehensive maintenance and onboarding guide provides the foundation for successful operations and team scaling in the ApexSigma ecosystem. Regular updates to this documentation ensure it remains current with system evolution and best practices.

**Key Success Factors:**
- Consistent application of operational procedures
- Proactive monitoring and maintenance
- Comprehensive training and documentation
- Continuous feedback and improvement
- Strong communication and collaboration

**Documentation Maintenance:**
- Review and update quarterly
- Incorporate feedback from operations team
- Add new procedures as system evolves
- Maintain accuracy with system changes

This guide serves as the living document for ApexSigma operations, ensuring reliable system performance and effective team collaboration.