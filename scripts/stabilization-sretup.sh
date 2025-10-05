#!/bin/bash

# OVS Phase 0: Stabilization Setup Script
# This script's sole purpose is to create a stable environment for fixing critical work orders.
# It prioritizes stability and diagnostics over feature completeness.
# Exit immediately if a command exits with a non-zero status.
set -e

echo "================================================================================"
echo "                   PHASE 0 STABILIZATION SETUP SCRIPT                          "
echo "================================================================================"
echo ""
echo "--- Starting Phase 0 Stabilization Setup ---"

# Determine script location and navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "✅ Project root: $PROJECT_ROOT"

# 1. Ensure .env file exists
# If no .env file is present, create one from the template. This is a critical first step.
if [ ! -f .env ]; then
    echo "--- .env file not found in project root. Creating from .env.example. ---"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created in project root. PLEASE POPULATE IT with correct values before running 'docker-compose up' manually."
    else
        echo "🚨 ERROR: .env.example not found. Cannot create .env file."
        exit 1
    fi
else
    echo "--- .env file found in project root. Proceeding. ---"
fi

# 2. Grant Docker permissions to the vscode user (if running in devcontainer)
# This allows running Docker commands without sudo.
if [ -n "$REMOTE_CONTAINERS" ] || [ -n "$CODESPACES" ]; then
    echo "--- Dev container detected. Granting Docker permissions to vscode user. ---"
    sudo usermod -aG docker vscode 2>/dev/null || echo "⚠️  User already in docker group or command unavailable"
    echo "✅ Docker permissions configured."
else
    echo "--- Running outside dev container. Skipping user permission changes. ---"
fi

# 3. Verify Docker Compose exists
if ! command -v docker-compose &> /dev/null
then
    echo "🚨 Docker Compose could not be found. This is a critical failure. Aborting."
    exit 1
fi
echo "✅ Docker Compose verified."

# 4. Bring up the core ecosystem services
# We assume a docker-compose.unified.yml file exists in the project root.
echo "🚀 Docker Compose available. Ready for manual ecosystem deployment."
echo ""
echo "To start services, run:"
echo "  docker-compose -f docker-compose.unified.yml up -d"
echo ""
echo "To view service health:"
echo "  docker-compose -f docker-compose.unified.yml ps"
echo ""

# 5. Display service health check endpoints
# This provides quick reference for manual validation
echo "--- Service Health Check Endpoints ---"
echo "Dagster Webserver:  http://localhost:3080"
echo "Dagster Health:     curl http://localhost:3080/server_info"
echo "Tools API:          curl http://localhost:8000/health"
echo "Memos API:          curl http://localhost:8090/health"
echo "Grafana:            http://localhost:3000 (admin/apexsigma123)"
echo "Prometheus:         http://localhost:9090"
echo "Jaeger:             http://localhost:16686"
echo "RabbitMQ:           http://localhost:15672"
echo ""
echo "================================================================================"
echo "                   PHASE 0 STABILIZATION SETUP COMPLETE                        "
echo "================================================================================"
echo ""
echo "✅ Dev container is ready for Phase 0 stabilization work!"
echo ""
echo "Next Steps:"
echo "  1. Review .env file and populate secrets"
echo "  2. Start services: docker-compose -f docker-compose.unified.yml up -d"
echo "  3. Apply OVS-T02 (tools-api fix)"
echo "  4. Apply OVS-T03 (dagster fix)"
echo "  5. Verify OVS-T04 (memos-api Neo4j)"
echo ""

exit 0

