# ADEP Documentation

## Architecture Overview

The Autonomous DevEx Pipeline (ADEP) is a microservices-based system designed to automate and streamline the software development experience. It consists of several core services that work together to provide a comprehensive development pipeline.

## Core Services

### 1. API Gateway (Port 8080)
- **Purpose**: Entry point for all external requests
- **Features**: Rate limiting, routing, authentication
- **Endpoints**: Routes to all microservices

### 2. Pipeline Orchestrator (Port 8081)
- **Purpose**: Manages and orchestrates development pipelines
- **Features**: Pipeline creation, execution, monitoring
- **Dependencies**: Redis, PostgreSQL

### 3. Code Analyzer (Port 8082)
- **Purpose**: Analyzes code quality and provides insights
- **Features**: Static analysis, metrics calculation, recommendations
- **Capabilities**: Multi-language support, file upload analysis

### 4. Deployment Manager (Port 8083)
- **Purpose**: Handles application deployments
- **Features**: Container deployment, scaling, rollbacks
- **Technologies**: Docker, Kubernetes integration

### 5. Agent Coordinator (Port 8084)
- **Purpose**: Coordinates autonomous agents
- **Features**: Agent registration, task assignment, WebSocket communication
- **Dependencies**: Redis for persistence

## Infrastructure Services

- **Redis**: Caching and message queuing
- **PostgreSQL**: Persistent data storage
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards

## Getting Started

1. Clone the repository
2. Copy `.env.example` to `.env` and configure
3. Run `./scripts/start.sh` to start all services
4. Access the API Gateway at http://localhost:8080

## API Endpoints

### API Gateway
- `GET /health` - Health check
- `POST /api/pipeline/*` - Pipeline operations
- `POST /api/analyze/*` - Code analysis
- `POST /api/deploy/*` - Deployment operations
- `POST /api/agents/*` - Agent coordination

### Individual Services
Each service exposes its own `/health` endpoint and specific functionality endpoints.

## Development

To develop individual services:
1. Navigate to the service directory
2. Install dependencies: `npm install`
3. Start in development mode: `npm run dev`

## Monitoring

- Prometheus metrics: http://localhost:9090
- Grafana dashboards: http://localhost:3000 (admin/admin)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request