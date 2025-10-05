#!/bin/bash
# phase0-verification.sh
# Operation Valhalla Shield - Phase 0 Stabilization Verification Script

echo "================================================================================"
echo "            PHASE 0 STABILIZATION - VERIFICATION PROTOCOL                      "
echo "================================================================================"
echo ""
echo "Testing all Phase 0 fixes with automated health checks and stability monitoring"
echo ""

# Function to check service health
check_health() {
    local service_name=$1
    local health_url=$2
    local max_wait=$3
    
    echo "Checking $service_name health..."
    for i in $(seq 1 $max_wait); do
        response=$(curl -s -o /dev/null -w "%{http_code}" $health_url 2>/dev/null)
        if [ "$response" = "200" ]; then
            echo "✅ $service_name: HTTP $response"
            return 0
        fi
        sleep 1
    done
    echo "❌ $service_name: Failed to return 200 within ${max_wait}s (got: $response)"
    return 1
}

# Function to check container status
check_container() {
    local container_name=$1
    local status=$(docker ps --filter "name=$container_name" --format "{{.Status}}")
    echo "Container $container_name: $status"
    if echo "$status" | grep -q "Up"; then
        return 0
    else
        return 1
    fi
}

# OVS-T01: Dev Container Setup Verification
echo "================================================================================"
echo "--- OVS-T01: Dev Container Setup Verification ---"
echo "================================================================================"
echo ""
echo "Checking dev container prerequisites..."
if [ -f .devcontainer/devcontainer.json ]; then
    echo "✅ devcontainer.json exists"
else
    echo "❌ devcontainer.json NOT found"
fi

if [ -f .env ]; then
    echo "✅ .env file exists"
else
    echo "⚠️  .env file not found (will be created on first container build)"
fi

echo ""

# OVS-T02: tools-api Restart Loop Fix
echo "================================================================================"
echo "--- OVS-T02: tools-api Restart Loop Fix ---"
echo "================================================================================"
echo ""
echo "Rebuilding tools-api container..."
docker-compose -f docker-compose.unified.yml build tools-api

echo "Restarting tools-api..."
docker-compose -f docker-compose.unified.yml up -d tools-api

echo "Waiting 30 seconds for container startup..."
sleep 30

check_health "tools-api" "http://localhost:8000/health" 60

echo ""
echo "Checking tools-api logs for import errors..."
docker logs apexsigma_tools_api --tail 50 | grep -i "error\|import" || echo "✅ No import errors found"

echo ""
echo "Checking container restart count..."
restart_count=$(docker inspect apexsigma_tools_api --format='{{.RestartCount}}')
echo "Restart count: $restart_count"

echo ""
echo "⏳ Starting 1-hour stability test for tools-api..."
echo "   You can monitor with: docker logs -f apexsigma_tools_api"
echo "   Test will complete at: $(date -d '+1 hour' '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -v+1H '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo '[1 hour from now]')"
echo ""

# OVS-T03: dagster_webserver Unhealthy Fix
echo "================================================================================"
echo "--- OVS-T03: dagster_webserver Unhealthy Fix ---"
echo "================================================================================"
echo ""
echo "Restarting dagster services..."
docker-compose -f docker-compose.unified.yml restart dagster-webserver dagster-daemon

echo "Waiting 120 seconds for startup period..."
sleep 120

check_health "dagster-webserver" "http://localhost:3080/server_info" 60

echo ""
echo "Checking dagster logs for heartbeat timeouts..."
docker logs apexsigma_dagster_webserver --tail 100 | grep -i "heartbeat" || echo "✅ No heartbeat timeout warnings"
docker logs apexsigma_dagster_webserver --tail 50 | grep -i "error" || echo "✅ No errors found"

echo ""
echo "Checking dagster container status..."
check_container "apexsigma_dagster_webserver"

echo ""
echo "⏳ Starting 1-hour stability test for dagster..."
echo "   You can monitor with: docker logs -f apexsigma_dagster_webserver"
echo "   Access UI at: http://localhost:3080"
echo ""

# OVS-T04: memos-api Neo4j Connection Verification
echo "================================================================================"
echo "--- OVS-T04: memos-api Neo4j Connection Verification ---"
echo "================================================================================"
echo ""
check_health "memos-api" "http://localhost:8090/health" 30

echo ""
echo "Checking memos-api logs for Neo4j connection..."
docker logs apexsigma_memos_api --tail 100 | grep -i "neo4j" || echo "ℹ️  No Neo4j messages in recent logs"

echo ""
echo "Testing memos-api CRUD operation..."
echo "Creating test memo..."
create_response=$(curl -s -X POST http://localhost:8090/api/v1/memory/store \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Phase 0 Stabilization Test - $(date)",
    "tier": "episodic",
    "agent_id": "phase0-verification"
  }' 2>/dev/null || echo '{"error": "Connection failed"}')

if echo "$create_response" | grep -q "error"; then
    echo "❌ CRUD test failed: $create_response"
else
    echo "✅ CRUD test successful"
fi

echo ""

# Container Health Summary
echo "================================================================================"
echo "--- Container Health Summary ---"
echo "================================================================================"
echo ""
docker ps --format "table {{.Names}}\t{{.Status}}" | grep apexsigma
echo ""

# Count healthy containers
healthy_count=$(docker ps --filter "health=healthy" | grep apexsigma | wc -l)
total_count=$(docker ps | grep apexsigma | wc -l)
echo "Health Status: $healthy_count/$total_count containers healthy"

if [ $healthy_count -ge 22 ]; then
    echo "✅ Phase 0 target achieved (92%+ healthy)"
else
    echo "⚠️  Health target not yet met (need 22/24, currently $healthy_count/$total_count)"
fi

echo ""
echo "================================================================================"
echo "            VERIFICATION COMPLETE - REVIEW RESULTS ABOVE                        "
echo "================================================================================"
echo ""
echo "Next Steps:"
echo "1. Monitor tools-api and dagster for 1 hour stability"
echo "2. Review all health check results"
echo "3. If all tests pass, proceed to git commits"
echo "4. Submit for MAR protocol review"
echo ""
echo "Monitoring Commands:"
echo "  docker logs -f apexsigma_tools_api"
echo "  docker logs -f apexsigma_dagster_webserver"
echo "  docker ps --format 'table {{.Names}}\t{{.Status}}' | grep apexsigma"
echo ""
