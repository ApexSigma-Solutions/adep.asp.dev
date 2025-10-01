# Project Summary

## Overall Goal
Create and maintain the ApexSigma ecosystem, a unified development environment featuring a Society of Agents architecture for intelligent automation and content management with four interconnected microservices.

## Key Knowledge
- **Technology Stack**: Python 3.13 (primary), FastAPI, Docker Compose, PostgreSQL, Redis, Qdrant, Neo4j, RabbitMQ
- **Architecture**: Monorepo with four main services: devenviro.as (agent orchestration), InGest-LLM.as (content ingestion), memos.as (knowledge management), tools.as (utilities)
- **Infrastructure**: Unified Docker Compose deployment with 17+ services including comprehensive observability stack (Langfuse, Jaeger, Prometheus, Grafana, Loki)
- **Directories**: Services in `/services/`, shared libs in `/libs/`, documentation in `/docs/`, agents in `/agents/`
- **Quality Assurance**: Trunk CLI for automation, pytest with coverage, Ruff/mypy for code quality
- **Protected Services**: memOS API (172.26.0.13), Neo4j Knowledge Graph (172.26.0.14), PostgreSQL Main (172.26.0.2), InGest-LLM API (172.26.0.12)
- **OMEGA INGEST Protocol**: Mandatory dual verification before code changes, context retrieval from InGest-LLM and memOS required before making changes

## Recent Actions
- Created comprehensive QWEN.md file for the ApexSigmaProjects.Dev directory based on project analysis
- Identified directory structure with main services, configuration files, and infrastructure components
- Determined that the ecosystem is currently operational with 17+ hour stable uptime
- Recognized that individual service QWEN.md files exist in each service directory but the main directory had an empty QWEN.md file
- Successfully created a detailed QWEN.md file with architecture overview, deployment instructions, and service descriptions

## Current Plan
- [DONE] Analyze the project structure and create a comprehensive QWEN.md file for the main directory
- [IN PROGRESS] Maintain awareness of the complex multi-service architecture for future interactions
- [TODO] Follow OMEGA INGEST protocols requiring context retrieval and dual verification before any code changes
- [TODO] Ensure future modifications adhere to the established architecture and conventions
- [TODO] Integrate with existing observability systems (Langfuse, Jaeger, etc.) as needed for future development tasks

---

## Summary Metadata
**Update time**: 2025-09-29T11:40:33.628Z 
