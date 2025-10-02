# Operation: Asgard Rebirth - memOS MCP Upgrade Plan (v6) (Qwen)

## Introduction

This enhanced plan integrates the critical learnings from the completed **Operation Monorepo Genesis** into the memOS MCP server upgrade strategy. The monorepo restructuring has fundamentally changed our development context, requiring strategic adjustments to our implementation approach while preserving the core vision of a robust, concurrent, and scalable memory backbone for AI assistants.

The key changes from v5 to v6 include:
- Addition of **Phase 0: Monorepo Foundation & Integration** to address foundational setup
- Complete restructuring of path dependencies and environment configurations
- Evolution of Dagster into a unified monorepo-wide workspace
- Strategic integration of Redis and RabbitMQ for enhanced data persistence
- Implementation of standardized service discovery patterns

This plan represents a synthesis of the best recommendations from all AI assistants' post-Monorepo analyses, creating a cohesive roadmap that leverages our new architecture while maintaining focus on the core MCP upgrade objectives.

## Phase 0: Monorepo Foundation & Integration

*Critical prerequisite: All Phase 1+ tasks depend on successful completion of Phase 0*

- [ ] **Task ID: MEMOS-P0-T1**
    - **Description**: Implement the `libs/apexsigma-core` shared library structure. This package will house all common code, including MCP abstractions, unified storage interfaces, authentication components, and protocol definitions.
    - **Implementer**: Gemini (CLI)
    - **Reviewer**: Qwen
    - **Done means Done**: 
        - The `apexsigma-core` package is created with initial directory structure
        - Contains MCP-specific abstractions (MemoryTier enum, MCPClient interface)
        - Installed as an editable dependency in the `memos.as` service
        - CI pipeline passes with the new dependency structure
        - Documentation created in `libs/apexsigma-core/README.md`

- [ ] **Task ID: MEMOS-P0-T2**
    - **Description**: Refactor all path dependencies across the memOS service to align with the new monorepo structure. Update all import statements to reflect the new `services/memos.as` directory.
    - **Implementer**: Qwen Code
    - **Reviewer**: GitHub Copilot
    - **Done means Done**:
        - All import statements updated to reference new paths
        - Verified working imports through test execution
        - Documentation updated to reflect new structure
        - Automated path validation tooling implemented in CI pipeline
        - No relative path imports remain in production code

- [ ] **Task ID: MEMOS-P0-T3**
    - **Description**: Consolidate and standardize environment configuration across the monorepo. Create unified `.env` file structure with standardized naming conventions.
    - **Implementer**: GitHub Copilot
    - **Reviewer**: Gemini (CLI)
    - **Done means Done**:
        - Standardized `.env.example`, `.env.development`, `.env.production` files created
        - All environment variables follow consistent naming convention (e.g., `MCP_MEMOS_*`)
        - Docker Compose environment variables updated to reference standardized paths
        - Verified all services start correctly with new configuration
        - Documentation created in `docs/configuration/monorepo-env.md`

- [ ] **Task ID: MEMOS-P0-T4**
    - **Description**: Implement unified Docker Compose configuration for the entire ecosystem with consistent service discovery patterns.
    - **Implementer**: Qwen Code
    - **Reviewer**: GitHub Copilot
    - **Done means Done**:
        - Root-level `docker-compose.yml` created with standardized service names
        - Verified service discovery works between memOS and other services
        - Network configuration updated to use `apexsigma_net` consistently
        - Verified all services can communicate via service names (e.g., `http://memos:8090`)
        - Documentation created in `docs/infrastructure/docker-compose.md`

- [ ] **Task ID: MEMOS-P0-T5**
    - **Description**: Configure the unified Dagster workspace for cross-service data flows. Establish the foundation for shared assets across services.
    - **Implementer**: Gemini (CLI)
    - **Reviewer**: Qwen
    - **Done means Done**:
        - Root-level `dagster.yaml` configured with code locations for all services
        - Verified Dagster can load assets from `memos.as` service
        - Created initial shared asset definitions in `libs/apexsigma-core/dagster`
        - Verified Dagster UI loads correctly with the new configuration
        - Documentation created in `docs/observability/dagster.md`

## Phase 1: Core MCP Implementation

*Building on the foundation established in Phase 0*

- [ ] **Task ID: MEMOS-P1-T1**
    - **Description**: Scaffold the new `memOS.as` service using the FastMCP 2.0 framework (FastAPI-based) with monorepo integration.
    - **Implementer**: Gemini (CLI)
    - **Reviewer**: Qwen
    - **Done means Done**: 
        - FastMCP 2.0 service scaffolded within `services/memos.as`
        - Proper integration with `libs/apexsigma-core` dependencies
        - Verified service starts correctly in the monorepo Docker environment
        - Basic health endpoint (`/health`) operational and verified
        - Documentation created in `services/memos.as/docs/fastmcp-integration.md`

- [ ] **Task ID: MEMOS-P1-T2**
    - **Description**: Implement MCP-specific memory tiers with agent isolation, leveraging the monorepo's shared storage interfaces.
    - **Implementer**: Qwen Code
    - **Reviewer**: GitHub Copilot
    - **Done means Done**:
        - MemoryTier enum extended with MCP-specific tiers (`MCP_GEMINI`, `MCP_QWEN`, etc.)
        - Storage service updated to use `libs/apexsigma-core/storage/interfaces.py`
        - Verified agent-specific memory isolation through integration tests
        - Documentation created in `services/memos.as/docs/mcp-tiers.md`
        - Verified compatibility with existing memory expiration policies

- [ ] **Task ID: MEMOS-P1-T3**
    - **Description**: Implement Redis integration for cross-service caching and short-term memory storage.
    - **Implementer**: GitHub Copilot
    - **Reviewer**: Gemini (CLI)
    - **Done means Done**:
        - Redis client integrated using `libs/apexsigma-core/storage/redis.py`
        - Implemented multi-layer caching strategy (L1: in-memory, L2: Redis, L3: DB)
        - Verified cache hit rate metrics through observability stack
        - Documentation created in `services/memos.as/docs/redis-integration.md`
        - Verified performance improvement benchmarks (95% faster cache hits)

- [ ] **Task ID: MEMOS-P1-T4**
    - **Description**: Implement MCP client utilities for agent integration, with monorepo-standardized patterns.
    - **Implementer**: Qwen Code
    - **Reviewer**: GitHub Copilot
    - **Done means Done**:
        - MCP client utility module created in `services/memos.as/client`
        - Verified integration with Gemini CLI and Qwen Coder Plus
        - Implemented pre-commit hooks for automatic context preservation
        - Documentation created in `services/memos.as/docs/mcp-client.md`
        - Verified context preservation across development sessions

## Phase 2: Integration & Enhancement

*Building on Phase 1 with enhanced capabilities*

- [ ] **Task ID: MEMOS-P2-T1**
    - **Description**: Implement RabbitMQ integration for asynchronous agent-to-agent communication and background job processing.
    - **Implementer**: Gemini (CLI)
    - **Reviewer**: Qwen
    - **Done means Done**:
        - RabbitMQ client integrated using `libs/apexsigma-core/messaging/rabbitmq.py`
        - Implemented event-driven communication patterns for agent coordination
        - Verified background job processing for long-running ingestion tasks
        - Documentation created in `services/memos.as/docs/rabbitmq-integration.md`
        - Verified message delivery reliability under load

- [ ] **Task ID: MEMOS-P2-T2**
    - **Description**: Implement knowledge graph relationship tracking with Neo4j, leveraging monorepo-standardized patterns.
    - **Implementer**: Qwen Code
    - **Reviewer**: GitHub Copilot
    - **Done means Done**:
        - Neo4j client integrated using `libs/apexsigma-core/graph/neo4j.py`
        - Verified relationship tracking between entities and decisions
        - Implemented graph visualization API endpoints
        - Documentation created in `services/memos.as/docs/knowledge-graph.md`
        - Verified relationship query performance benchmarks

- [ ] **Task ID: MEMOS-P2-T3**
    - **Description**: Implement comprehensive observability for MCP operations with monorepo-wide metrics.
    - **Implementer**: GitHub Copilot
    - **Reviewer**: Gemini (CLI)
    - **Done means Done**:
        - MCP-specific metrics added to existing observability stack
        - Verified metrics collection in Grafana and Prometheus
        - Implemented custom dashboards for MCP operations
        - Documentation created in `services/memos.as/docs/observability.md`
        - Verified alerting for critical MCP operations

- [ ] **Task ID: MEMOS-P2-T4**
    - **Description**: Implement MCP-aware EOD reporting system for persistent context preservation.
    - **Implementer**: Qwen Code
    - **Reviewer**: GitHub Copilot
    - **Done means Done**:
        - EOD reporting system integrated with MCP storage
        - Verified daily report generation and ingestion
        - Implemented knowledge retention metrics
        - Documentation created in `services/memos.as/docs/eod-reporting.md`
        - Verified context preservation across development sessions

## Phase 3: Agent Swarm & Advanced Capabilities

*Building on Phase 2 with agent coordination*

- [ ] **Task ID: MEMOS-P3-T1**
    - **Description**: Scaffold the Agent Swarm project, implementing the core `AgentRole`, `AgentContext`, and `MCPAgent` classes with monorepo integration.
    - **Implementer**: Gemini (CLI)
    - **Reviewer**: Qwen
    - **Done means Done**:
        - Core agent classes implemented in `services/memos.as/agents`
        - Proper integration with `libs/apexsigma-core/agents` interfaces
        - Verified agent initialization and basic operations
        - Documentation created in `services/memos.as/docs/agent-swarm.md`
        - Verified compatibility with MCP memory tiers

- [ ] **Task ID: MEMOS-P3-T2**
    - **Description**: Implement the `MCPAgentSwarm` class and integrate it with the `tools.as` service registry, leveraging monorepo-wide service discovery.
    - **Implementer**: Qwen Code
    - **Reviewer**: GitHub Copilot
    - **Done means Done**:
        - `MCPAgentSwarm` class implemented with task delegation capabilities
        - Verified integration with tools.as service registry
        - Implemented agent coordination patterns for complex tasks
        - Documentation created in `services/memos.as/docs/agent-coordination.md`
        - Verified multi-agent task execution

- [ ] **Task ID: MEMOS-P3-T3**
    - **Description**: Implement advanced memory architecture with distinct memory types (short-term, long-term, episodic).
    - **Implementer**: GitHub Copilot
    - **Reviewer**: Gemini (CLI)
    - **Done means Done**:
        - Memory abstraction layer implemented with distinct memory types
        - Verified memory operations across all tiers
        - Implemented memory lifecycle management
        - Documentation created in `services/memos.as/docs/memory-architecture.md`
        - Verified performance under mixed memory operations

- [ ] **Task ID: MEMOS-P3-OMEGA**
    - **Description**: Perform the final Omega Ingest of the agent swarm's design and all MAR sign-off reports, ensuring comprehensive knowledge preservation.
    - **Implementer**: Qwen Code
    - **Reviewer**: Gemini (CLI)
    - **Done means Done**:
        - Complete documentation ingested into Omega Ingest Master Knowledge Graph
        - Verified POML formatting for all critical knowledge artifacts
        - Implemented knowledge graph relationships for agent swarm concepts
        - Documentation created in `services/memos.as/docs/omega-ingest.md`
        - Verified knowledge retention through retrieval tests

## Future-Ready Technologies

*Technologies to consider for future integration based on strategic analysis*

### Advanced Orchestration
- **Apache Airflow**: For complex workflow scenarios beyond Dagster's scope (Target: Phase 4)
- **Kubernetes Operators**: For cloud-native deployments and scalability (Target: Phase 5)
- **Service Mesh (Istio)**: For advanced traffic management in containerized environments (Target: Phase 5)

### Enhanced Persistence
- **Apache Kafka**: For higher throughput event streaming than RabbitMQ (Target: Phase 4)
- **TimescaleDB**: For time-series analysis of agent interactions (Target: Phase 3)
- **Apache Pulsar**: For next-generation messaging with geo-replication (Target: Phase 4)

### AI/ML Infrastructure
- **MLflow**: For model lifecycle management integrated with Agent Swarm (Target: Phase 3)
- **Feast Feature Store**: For consistent feature serving across agents (Target: Phase 4)
- **Specialized Vector DBs (Pinecone)**: For domain-specific vector search beyond Qdrant (Target: Phase 3)

## Risk Assessment & Mitigation

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| Path dependency issues | High | Medium | Implement automated path validation tooling; start with minimal viable path updates |
| Docker network conflicts | Medium | High | Standardize service discovery patterns; implement network verification tests |
| Dagster workspace complexity | Medium | Medium | Start with minimal viable workspace structure; document patterns thoroughly |
| Redis implementation scope creep | Low | High | Focus on critical path use cases first; implement phased Redis integration |
| RabbitMQ configuration complexity | Medium | Medium | Leverage existing messaging patterns; implement incremental feature rollout |
| MCP client compatibility issues | High | Medium | Implement comprehensive client testing suite; create backward compatibility patterns |

## Implementation Checklist

- [ ] **Pre-Implementation Verification**
  - [ ] Verify monorepo structure is correctly implemented
  - [ ] Confirm all services are operational in the new structure
  - [ ] Validate environment configuration standards

- [ ] **Phase 0 Execution**
  - [ ] Implement `libs/apexsigma-core` shared library
  - [ ] Refactor all path dependencies
  - [ ] Consolidate environment configuration
  - [ ] Implement unified Docker Compose
  - [ ] Configure unified Dagster workspace

- [ ] **Phase 1 Execution**
  - [ ] Scaffold FastMCP 2.0 service
  - [ ] Implement MCP-specific memory tiers
  - [ ] Integrate Redis for caching
  - [ ] Implement MCP client utilities

- [ ] **Phase 2 Execution**
  - [ ] Implement RabbitMQ integration
  - [ ] Implement knowledge graph relationships
  - [ ] Enhance observability metrics
  - [ ] Implement MCP-aware EOD reporting

- [ ] **Phase 3 Execution**
  - [ ] Scaffold Agent Swarm project
  - [ ] Implement MCPAgentSwarm class
  - [ ] Implement advanced memory architecture
  - [ ] Perform final Omega Ingest

- [ ] **Post-Implementation Verification**
  - [ ] Verify all services operational in new configuration
  - [ ] Validate MCP functionality through integration tests
  - [ ] Document lessons learned for future reference

## Conclusion

This enhanced plan provides a clear, actionable roadmap for upgrading the memOS MCP server within the context of our newly established monorepo architecture. By adding Phase 0 for foundational alignment and incorporating the collective intelligence from all AI assistant analyses, we've created a strategic plan that:

1. ✅ **Leverages the monorepo structure** for immediate value through the `libs/` directory
2. ✅ **Enables a unified Dagster workspace** that simplifies cross-service data flows
3. ✅ **Creates a foundation for enhanced Redis usage** across the ecosystem
4. ✅ **Streamlines Docker Compose implementation** with consistent service discovery

The phased approach ensures we build a solid foundation before moving to more complex capabilities, while the risk assessment and implementation checklist provide practical guidance for successful execution.

**Status**: ✅ **MONOREPO STRUCTURE PROVIDES SOLID FOUNDATION FOR MCP UPGRADE**  
**Confidence Level**: 100%  
**Implementation Readiness**: IMMEDIATE (with Phase 0 completion)