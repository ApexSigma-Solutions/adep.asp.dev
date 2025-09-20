#!/bin/bash

# ADEP Start Script
echo "Starting Autonomous DevEx Pipeline..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your configuration before running again."
    exit 1
fi

# Build and start services
echo "Building and starting services..."
docker-compose up --build -d

# Check service health
echo "Checking service health..."
sleep 10

services=("api-gateway:8080" "pipeline-orchestrator:8081" "code-analyzer:8082" "deployment-manager:8083" "agent-coordinator:8084")

for service in "${services[@]}"; do
    name=$(echo $service | cut -d':' -f1)
    port=$(echo $service | cut -d':' -f2)
    
    if curl -s http://localhost:$port/health > /dev/null; then
        echo "✅ $name is healthy"
    else
        echo "❌ $name is not responding"
    fi
done

echo ""
echo "🚀 ADEP is running!"
echo "📊 API Gateway: http://localhost:8080"
echo "📈 Prometheus: http://localhost:9090"
echo "📊 Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "To stop: docker-compose down"
echo "To view logs: docker-compose logs -f"