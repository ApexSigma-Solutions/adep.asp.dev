# ApexSigma Projects Development Environment

## Overview
This is the unified development environment for the ApexSigma ecosystem, featuring a Society of Agents architecture for intelligent automation and content management.

## Active Projects

### 🤖 devenviro.as
**DevEnviro Society of Agents**
- Agent orchestration and management platform
- Multi-agent collaboration with Claude, Gemini, and Gemma agents
- RabbitMQ-based messaging and communication
- Real-time observability with Langfuse integration
- **Status**: ✅ Agent foundation operational, CLI integration pending

### 📥 InGest-LLM.as  
**Intelligent Content Ingestion Engine**
- Automated repository analysis and documentation
- Ecosystem-wide content processing and vectorization
- Integration with Memos knowledge management
- Multi-model LLM analysis and summarization
- **Status**: ✅ Core ingestion pipeline operational

### 📝 memos.as
**Knowledge Management System**
- Centralized content storage and retrieval
- Progress tracking and session management
- Integration hub for ecosystem components
- Enhanced search and analysis capabilities
- **Status**: ✅ Production-ready with progress logging

### 🔧 tools.as
**Development Utilities and APIs**
- Shared tooling and utilities across projects
- API endpoints for cross-project integration
- Development and testing frameworks
- **Status**: ✅ Core functionality operational

## Infrastructure

### 🐳 Unified Docker Stack
- **File**: `docker-compose.unified.yml`
- **Services**: 17+ integrated services
- **Uptime**: 17+ hours stable deployment
- **Monitoring**: Grafana, Prometheus, Jaeger, Loki

### 🔍 Observability
- **Langfuse**: 347+ traces active
- **Health Monitoring**: Service status tracking
- **Logging**: Centralized log aggregation
- **Metrics**: Performance and usage analytics

### 🎯 Agent Infrastructure
- **DevEnviro API**: Agent orchestration
- **Gemini CLI Listener**: HEALTHY
- **RabbitMQ**: Message bus operational
- **Database Layer**: PostgreSQL, Redis, Qdrant

## Directory Structure

```
ApexSigmaProjects.Dev/
├── devenviro.as/          # Agent orchestration platform
├── InGest-LLM.as/         # Content ingestion engine
├── memos.as/              # Knowledge management
├── tools.as/              # Development utilities
├── archive/               # Archived/legacy projects
├── docs/                  # Project documentation
├── logs/                  # Session and progress logs
├── scripts/               # Utility scripts
├── tests/                 # Integration tests
├── DevTools/              # Development tools and diagrams
└── docker-compose.unified.yml  # Infrastructure definition
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Git

### Quick Start
```bash
# Start the unified infrastructure
docker-compose -f docker-compose.unified.yml up -d

# Check service health
docker-compose -f docker-compose.unified.yml ps

# View Langfuse observability
# Open http://localhost:3000
```

### Development Workflow
1. **Infrastructure**: All services run in unified Docker stack
2. **Agents**: DevEnviro orchestrates Claude/Gemini agents
3. **Content**: InGest-LLM processes and analyzes code/docs
4. **Knowledge**: Memos stores and manages insights
5. **Tools**: Shared utilities support all projects

## Recent Achievements (Aug 25, 2025)

### ✅ Completed
- **Agent Foundation**: DevEnviro agent infrastructure operational
- **Infrastructure**: Unified Docker stack with 17+ services
- **Database**: Fixed psycopg2.pool import errors
- **Observability**: Langfuse active with 347+ traces
- **Documentation**: Comprehensive reference docs across all projects
- **Cache Cleanup**: Removed all Python cache files from repositories

### 🔄 In Progress  
- **A2A Bridge**: Import error fixes for external agent communication
- **CLI Integration**: Replace simulation commands with real Claude/Gemini CLI
- **Health Checks**: Fix DevEnviro API health status
- **Qdrant Service**: Resolve unhealthy status

### 🎯 Next Steps
1. Enable production Claude/Gemini CLI integration
2. Complete A2A bridge for external agent APIs
3. Implement advanced agent collaboration patterns
4. Scale ecosystem for production deployment

## Support & Documentation

- **Project Docs**: Each project has comprehensive MkDocs documentation
- **API Reference**: Available in each project's `docs/reference/` directory
- **Session Logs**: Progress tracking in `logs/` directory
- **Health Status**: Monitor via unified Docker stack

---

**Last Updated**: August 25, 2025  
**Ecosystem Status**: ✅ Operational - Ready for agent CLI integration  
**Infrastructure**: 17+ services, 17+ hour stable uptime
