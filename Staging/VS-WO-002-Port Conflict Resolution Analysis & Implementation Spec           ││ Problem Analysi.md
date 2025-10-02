  VS-WO-002: Port Conflict Resolution Analysis & Implementation Spec           │
│ Problem Analysis                                                              │
│                                                                               │
│ Root Cause Identified                                                         │
│                                                                               │
│ The port 8080 conflict exists between two services that both want to use this │
│  port:                                                                        │
│                                                                               │
│                                                                               │
│ 1. Dagster Webserver in docker-compose.unified.yml:                           │
│   •  Command: ["dagster-webserver", "-h", "0.0.0.0", "-p", "8080", ...]       │
│   •  No external port mapping - runs internally on 8080                       │
│                                                                               │
│ 2. DevEnviro.as service in docker-compose.yml:                                │
│   •  Port mapping: "8080:8080"                                                │
│   •  Has external port mapping - exposes 8080 to host                         │
│ Current Grafana Configuration Status                                          │
│                                                                               │
│ •  Grafana service exists in docker-compose.unified.yml but has NO port       │
│    mappings                                                                   │
│ •  Grafana config shows it runs on port 3000 internally (grafana.ini)         │
│ •  Legacy docker-compose.yml shows Grafana with "3000:3000" port mapping      │
│ •  Issue: Grafana in unified compose has no external access due to missing    │
│    port mapping                                                               │
│ Architecture Conflicts                                                        │
│                                                                               │
│ •  docker-compose.yml (legacy) vs docker-compose.unified.yml (current)        │
│ •  Multiple services compete for port 8080                                    │
│    Missing port mappings prevent external access to observability stack       │
│ Implementation Strategy                                                       │
│                                                                               │
│ Phase 1: Port Mapping Standardization (15 minutes)                            │
│                                                                               │
│ Objective: Establish consistent port mappings across all services in unified  │
│ compose                                                                       │
│                                                                               │
│ Changes to `docker-compose.unified.yml`:                                      │
│                                                                               │
│ 1. Add Missing Port Mappings for observability stack:                         │
│    ```yaml                                                                    │
│    grafana:                                                                   │
│      ports:                                                                   │
│ •  "3000:3000"  # Standard Grafana port                                       │
│                                                                               │
│    prometheus:                                                                │
│      ports:                                                                   │
│ •  "9090:9090"  # Standard Prometheus port                                    │
│                                                                               │
│    jaeger:                                                                    │
│      ports:                                                                   │
│ •  "16686:16686"  # Standard Jaeger UI port                                   │
│    ```                                                                        │
│                                                                               │
│ 2. Resolve Dagster Port Conflict:                                             │
│    ```yaml                                                                    │
│    dagster-webserver:                                                         │
│      ports:                                                                   │
│ •  "3080:8080"  # Map external 3080 to internal 8080                          │
│      command: ["dagster-webserver", "-h", "0.0.0.0", "-p", "8080", ...]       │
│    ```                                                                        │
│                                                                               │
│ 3. Add Service Port Mappings for API access:                                  │
│    ```yaml                                                                    │
│    devenviro-api:                                                             │
│      ports:                                                                   │
│    "8001:8000"  # DevEnviro API                                               │
│    memos-api:                                                                 │
│      ports:                                                                   │
│                                                                               │
│    "8090:8090"  # Memos API (consistent with legacy)                          │
│    ingest-llm-api:                                                            │
│      ports:                                                                   │
│                                                                               │
│    "8002:8000"  # InGest-LLM API                                              │
│    tools-api:                                                                 │
│      ports:                                                                   │
│                                                                               │
│    ```03:8000"  # Tools API                                                   │
│                                                                               │
│ Phase 2: Environment Configuration Updates (10 minutes)                       │
│                                                                               │
│ Objective: Update environment variables to reflect new port mappings          │
│                                                                               │
│ Updates to `.env.example`:                                                    │
│                                                                               │
│                                                                               │
│ bash                                                                          │
│   GRAFANA_PORT=3000ts (External Access) ===                                   │
│   PROMETHEUS_PORT=9090                                                        │
│   JAEGER_PORT=16686                                                           │
│   DAGSTER_PORT=3080                                                           │
│                                                                               │
│   # === API Service Ports ===                                                 │
│   DEVENVIRO_API_PORT=8001                                                     │
│   MEMOS_API_PORT=8090                                                         │
│   INGEST_LLM_API_PORT=8002                                                    │
│   TOOLS_API_PORT=8003                                                         │
│                                                                               │
│ Phase 3: Service Interconnection Updates (10 minutes)                         │
│                                                                               │
│ Objective: Update service-to-service communication to use internal Docker     │
│ network                                                                       │
│                                                                               │
│ Internal Communication Pattern:                                               │
│ •  Services communicate via container names (e.g., grafana:3000,              │
│    prometheus:9090)                                                           │
│ •  External access via mapped ports (e.g., localhost:3000, localhost:9090)    │
│                                                                               │
│ Configuration Updates:                                                        │
│ 1. Update any hardcoded localhost references in service configs               │
│ 2. Ensure health checks use internal ports                                    │
│ 3. Update service discovery configurations                                    │
│                                                                               │
│ Phase 4: Validation & Testing (10 minutes)                                    │
│                                                                               │
│ Objective: Verify all services start and are accessible                       │
│                                                                               │
│ Testing Checklist:                                                            │
│ 1. Port Conflict Resolution:                                                  │
│    ```bash                                                                    │
│    docker-compose -f docker-compose.unified.yml up -d                         │
│    netstat -tlnp | grep :8080  # Should show no conflicts                     │
│    ```                                                                        │
│                                                                               │
│ 2. Service Accessibility:                                                     │
│    ```bash                                                                    │
│    curl http://localhost:3000    # Grafana UI                                 │
│    curl http://localhost:9090    # Prometheus UI                              │
│    curl http://localhost:16686   # Jaeger UI                                  │
│    curl http://localhost:3080    # Dagster UI                                 │
│    ```                                                                        │
│                                                                               │
│    ```bashpoints:                                                             │
│    curl http://localhost:8090/health  # Memos API                             │
│    curl http://localhost:8001/health  # DevEnviro API                         │
│    curl http://localhost:8002/health  # InGest-LLM API                        │
│    curl http://localhost:8003/docs    # Tools API                             │
│    ```                                                                        │
│                                                                               │
│ Expected Outcomes                                                             │
│                                                                               │
│ Immediate Benefits                                                            │
│                                                                               │
│ •  ✅ Port 8080 conflict resolved - Dagster accessible on 3080                 │
│ •  ✅ Grafana accessible on standard port 3000                                 │
│ •  ✅ Complete observability stack online (Grafana, Prometheus, Jaeger)        │
│    ✅ All services externally accessible via distinct ports                    │
│ Service Port Map (Post-Implementation)                                        │
│                                                                               │
│ | Service | External Port | Internal Port | Access URL |                      │
│ |---------|---------------|---------------|------------|                      │
│ | Grafana | 3000 | 3000 | http://localhost:3000 |                             │
│ | Prometheus | 9090 | 9090 | http://localhost:9090 |                          │
│ | Jaeger | 16686 | 16686 | http://localhost:16686 |                           │
│ | Dagster | 3080 | 8080 | http://localhost:3080 |                             │
│ | Memos API | 8090 | 8090 | http://localhost:8090 |                           │
│ | DevEnviro API | 8001 | 8000 | http://localhost:8001 |                       │
│ | InGest-LLM API | 8002 | 8000 | http://localhost:8002 |                      │
│ | Tools API | 8003 | 8000 | http://localhost:8003 |                           │
│                                                                               │
│ Architecture Improvements                                                     │
│                                                                               │
│ •  Consistent port mapping strategy across all services                       │
│ •  No port conflicts between services                                         │
│ •  External accessibility for all UI and API endpoints                        │
│    Internal network optimization for service-to-service communication         │
│ Valhalla Shield Compliance                                                    │
│ •  ✅ Observability requirement met - Grafana dashboard accessible             │
│ •  ✅ Service monitoring enabled - Prometheus metrics collection               │
│ •  ✅ Distributed tracing ready - Jaeger UI available                          │
│ •  ✅ Workflow orchestration accessible - Dagster UI on dedicated port         │
│                                                                               │
│ Risk Assessment                                                               │
│                                                                               │
│ Low Risk Changes                                                              │
│ •  Adding port mappings (non-breaking)                                        │
│ •  Environment variable additions (backwards compatible)                      │
│ •  Internal service communication updates (isolated)                          │
│                                                                               │
│ Mitigation Strategies                                                         │
│ •  Backup current configuration before changes                                │
│ •  Gradual rollout - test each service individually                           │
│ •  Rollback plan - revert to current docker-compose.unified.yml if issues     │
│                                                                               │
│ Implementation Priority                                                       │
│ 1. High: Grafana port mapping (enables observability)                         │
│ 2. High: Dagster port resolution (resolves main conflict)                     │
│ 3. Medium: API service port mappings (improves accessibility)                 │
│ 4. Medium: Environment variable updates (documentation)                       │
│                                                                               │
│ This implementation resolves the core port conflict while establishing a      │
│ robust, accessible service architecture that meets all Valhalla Shield        │
│ observability requirements.