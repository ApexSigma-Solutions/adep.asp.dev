
│                                                                                                        │
│ Dedicated Database Architecture for Langfuse                                                           │
│                                                                                                        │
│ Problem Analysis                                                                                       │
│                                                                                                        │
│ Current Issue: Langfuse is failing with PostgreSQL migration error "database schema is not empty"      │
│ because it's trying to use the shared apexsigma_db database that already contains tables from          │
│ memos-api, ingest-llm-api, and other services.                                                         │
│                                                                                                        │
│ Root Cause: Langfuse v3 uses a dual-backend architecture:                                              │
│ 1. PostgreSQL - Operational data (projects, users, sessions, prompts, API keys)                        │
│ 2. ClickHouse - Analytics data (traces, observations, scores, metrics)                                 │
│                                                                                                        │
│ Both backends are required and Langfuse expects to own the entire PostgreSQL database for Prisma       │
│ migrations.                                                                                            │
│                                                                                                        │
│ Architecture Design                                                                                    │
│                                                                                                        │
│ Database Separation Strategy                                                                           │
│                                                                                                        │
│ We'll implement database-level isolation within existing database instances (not separate containers): │
│                                                                                                        │
│ PostgreSQL Instance (apexsigma_postgres):                                                              │
│ •  apexsigma_db - Shared database for memos-api, ingest-llm-api, devenviro-api                         │
│ •  langfuse_db - NEW Dedicated database for Langfuse operational data                                  │
│                                                                                                        │
│ ClickHouse Instance (apexsigma_clickhouse):                                                            │
│ •  apexsigma_observability - Observability metrics (Loki, Prometheus, Jaeger, Vector)                  │
│ •  langfuse_analytics - NEW Dedicated database for Langfuse analytics (traces, observations, scores)   │
│                                                                                                        │
│ Benefits                                                                                               │
│                                                                                                        │
│ ✅ Complete Isolation: Langfuse has full control over its databases                                     │
│ ✅ Resource Efficiency: Single ClickHouse instance, multiple databases                                  │
│ ✅ Security: Separate users with granular database-level permissions                                    │
│ ✅ Maintainability: Clear separation of concerns                                                        │
│ ✅ Scalability: Can scale ClickHouse instance for both workloads                                        │
│                                                                                                        │
│ Implementation Plan                                                                                    │
│                                                                                                        │
│ Phase 1: PostgreSQL Configuration (Fixes immediate issue)                                              │
│                                                                                                        │
│ 1.1 Create Init Script - config/postgres/init-langfuse.sql:                                            │
│                                                                                                        │
│ sql                                                                                                    │
│   -- Create dedicated Langfuse database                                                                │
│   CREATE DATABASE langfuse_db;                                                                         │
│                                                                                                        │
│   -- Create dedicated Langfuse user                                                                    │
│   CREATE USER langfuse_user WITH PASSWORD 'Apexsigma123_';                                             │
│                                                                                                        │
│   -- Grant full privileges to Langfuse user on langfuse_db                                             │
│   GRANT ALL PRIVILEGES ON DATABASE langfuse_db TO langfuse_user;                                       │
│                                                                                                        │
│   -- Allow schema creation                                                                             │
│   ALTER DATABASE langfuse_db OWNER TO langfuse_user;                                                   │
│                                                                                                        │
│ 1.2 Update PostgreSQL Service - Mount init script:                                                     │
│                                                                                                        │
│ yaml                                                                                                   │
│   postgres:                                                                                            │
│     volumes:                                                                                           │
│       - postgres_data:/var/lib/postgresql/data                                                         │
│       - ./config/postgres/init-langfuse.sql:/docker-entrypoint-initdb.d/init-langfuse.sql:ro  # NEW    │
│                                                                                                        │
│ Phase 2: ClickHouse Configuration                                                                      │
│                                                                                                        │
│ 2.1 Create Langfuse ClickHouse Schema - config/clickhouse/init-langfuse.sql:                           │
│                                                                                                        │
│ sql                                                                                                    │
│   -- Create dedicated Langfuse analytics database                                                      │
│   CREATE DATABASE IF NOT EXISTS langfuse_analytics;                                                    │
│                                                                                                        │
│   -- Grant permissions to Langfuse user                                                                │
│   GRANT ALL ON langfuse_analytics.* TO langfuse_user;                                                  │
│                                                                                                        │
│   -- Switch to Langfuse database                                                                       │
│   USE langfuse_analytics;                                                                              │
│                                                                                                        │
│   -- Langfuse will create its own tables via migrations                                                │
│   -- Schema reference: https://langfuse.com/self-hosting/deployment/infrastructure/clickhouse          │
│                                                                                                        │
│ 2.2 Update ClickHouse Users - config/clickhouse/users.xml:                                             │
│                                                                                                        │
│ xml                                                                                                    │
│   <users>                                                                                              │
│     <!-- Existing default and clickhouse_user -->                                                      │
│                                                                                                        │
│     <!-- NEW: Dedicated Langfuse user -->                                                              │
│     <langfuse_user>                                                                                    │
│       <password>Apexsigma123_</password>                                                               │
│       <networks>                                                                                       │
│         <ip>172.26.0.0/16</ip>  <!-- ApexSigma network only -->                                        │
│       </networks>                                                                                      │
│       <profile>default</profile>                                                                       │
│       <quota>default</quota>                                                                           │
│       <databases>                                                                                      │
│         <database>langfuse_analytics</database>  <!-- Restricted to this database -->                  │
│       </databases>                                                                                     │
│     </langfuse_user>                                                                                   │
│                                                                                                        │
│     <!-- Observability user (for Prometheus/Loki/Jaeger) -->                                           │
│     <observability_user>                                                                               │
│       <password>Apexsigma123_</password>                                                               │
│       <networks>                                                                                       │
│         <ip>172.26.0.0/16</ip>                                                                         │
│       </networks>                                                                                      │
│       <profile>default</profile>                                                                       │
│       <quota>default</quota>                                                                           │
│       <databases>                                                                                      │
│         <database>apexsigma_observability</database>                                                   │
│       </databases>                                                                                     │
│     </observability_user>                                                                              │
│   </users>                                                                                             │
│                                                                                                        │
│ 2.3 Update ClickHouse Init Script - Add to existing config/clickhouse/init.sql:                        │
│                                                                                                        │
│ sql                                                                                                    │
│   -- Execute Langfuse-specific initialization                                                          │
│   SOURCE /docker-entrypoint-initdb.d/init-langfuse.sql;                                                │
│                                                                                                        │
│ 2.4 Mount Langfuse Init Script - Update ClickHouse service:                                            │
│                                                                                                        │
│ yaml                                                                                                   │
│   clickhouse:                                                                                          │
│     volumes:                                                                                           │
│       - clickhouse_data:/var/lib/clickhouse                                                            │
│       - clickhouse_logs:/var/log/clickhouse-server                                                     │
│       - ./config/clickhouse/config.xml:/etc/clickhouse-server/config.d/custom.xml:ro                   │
│       - ./config/clickhouse/users.xml:/etc/clickhouse-server/users.d/custom.xml:ro                     │
│       - ./config/clickhouse/init.sql:/docker-entrypoint-initdb.d/init.sql:ro  # Existing               │
│       - ./config/clickhouse/init-langfuse.sql:/docker-entrypoint-initdb.d/init-langfuse.sql:ro  # NEW  │
│                                                                                                        │
│ Phase 3: Langfuse Service Configuration                                                                │
│                                                                                                        │
│ 3.1 Update Langfuse Environment Variables:                                                             │
│                                                                                                        │
│ yaml                                                                                                   │
│   langfuse:                                                                                            │
│     environment:                                                                                       │
│       # PostgreSQL - Dedicated database                                                                │
│       DATABASE_URL: "postgresql://langfuse_user:Apexsigma123_@postgres:5432/langfuse_db"  # CHANGED    │
│                                                                                                        │
│       # ClickHouse - Dedicated database                                                                │
│       CLICKHOUSE_URL: "clickhouse://langfuse_user:Apexsigma123_@clickhouse:9000/langfuse_analytics"  # │
│   CHANGED                                                                                              │
│       LANGFUSE_CLICKHOUSE_ENABLED: "true"                                                              │
│       LANGFUSE_CLICKHOUSE_MIGRATION_TARGET: "latest"                                                   │
│                                                                                                        │
│       # Auth & Security (existing)                                                                     │
│       NEXTAUTH_URL: "http://localhost:3001"                                                            │
│       NEXTAUTH_SECRET: "${LANGFUSE_NEXTAUTH_SECRET}"                                                   │
│       SALT: "${LANGFUSE_SALT}"                                                                         │
│                                                                                                        │
│ Phase 4: Environment Variables                                                                         │
│                                                                                                        │
│ 4.1 Update `.env` file:                                                                                │
│                                                                                                        │
│ bash                                                                                                   │
│   # === Langfuse Dedicated Configuration ===                                                           │
│   LANGFUSE_POSTGRES_DB=langfuse_db                                                                     │
│   LANGFUSE_POSTGRES_USER=langfuse_user                                                                 │
│   LANGFUSE_POSTGRES_PASSWORD=Apexsigma123_                                                             │
│                                                                                                        │
│   LANGFUSE_CLICKHOUSE_DB=langfuse_analytics                                                            │
│   LANGFUSE_CLICKHOUSE_USER=langfuse_user                                                               │
│   LANGFUSE_CLICKHOUSE_PASSWORD=Apexsigma123_                                                           │
│                                                                                                        │
│   # Security                                                                                           │
│   LANGFUSE_NEXTAUTH_SECRET=<generate_secure_secret>                                                    │
│   LANGFUSE_SALT=<generate_secure_salt>                                                                 │
│                                                                                                        │
│ Phase 5: Observability Stack Updates                                                                   │
│                                                                                                        │
│ 5.1 Update Prometheus/Loki/Jaeger - Use dedicated observability user:                                  │
│                                                                                                        │
│ yaml                                                                                                   │
│   # In future when implementing ClickHouse backends for these services                                 │
│   CLICKHOUSE_USER: observability_user                                                                  │
│   CLICKHOUSE_PASSWORD: Apexsigma123_                                                                   │
│   CLICKHOUSE_DATABASE: apexsigma_observability                                                         │
│                                                                                                        │
│ Deployment Steps                                                                                       │
│                                                                                                        │
│ 1. Create configuration files:                                                                         │
│   •  config/postgres/init-langfuse.sql                                                                 │
│   •  config/clickhouse/init-langfuse.sql                                                               │
│   •  Update config/clickhouse/users.xml                                                                │
│                                                                                                        │
│ 2. Update `.env` with new Langfuse variables                                                           │
│                                                                                                        │
│ 3. Recreate PostgreSQL container (to execute init script):                                             │
│    ```bash                                                                                             │
│    docker-compose -f docker-compose.unified.yml stop postgres langfuse                                 │
│    docker volume rm apexsigma_postgres_data  # WARNING: Loses existing data                            │
│    docker-compose -f docker-compose.unified.yml up -d postgres                                         │
│    ```                                                                                                 │
│                                                                                                        │
│ 4. Recreate ClickHouse container (to execute Langfuse init script):                                    │
│    ```bash                                                                                             │
│    docker-compose -f docker-compose.unified.yml stop clickhouse langfuse                               │
│    docker volume rm apexsigma_clickhouse_data  # WARNING: Loses existing data                          │
│    docker-compose -f docker-compose.unified.yml up -d clickhouse                                       │
│    ```                                                                                                 │
│                                                                                                        │
│ 5. Start Langfuse:                                                                                     │
│    ```bash                                                                                             │
│    docker-compose -f docker-compose.unified.yml up -d langfuse                                         │
│    ```                                                                                                 │
│                                                                                                        │
│ 6. Verify:                                                                                             │
│    ```bash                                                                                             │
│    # Check PostgreSQL database creation                                                                │
│    docker exec -it apexsigma_postgres psql -U langfuse_user -d langfuse_db -c "dt"                     │
│                                                                                                        │
│    # Check ClickHouse database creation                                                                │
│    docker exec -it apexsigma_clickhouse clickhouse-client --user langfuse_user --password Apexsigma123_│
│  --query "SHOW DATABASES"                                                                              │
│                                                                                                        │
│    # Check Langfuse health                                                                             │
│    curl http://localhost:3001/api/public/health                                                        │
│                                                                                                        │
│    # Check Langfuse logs                                                                               │
│    docker logs apexsigma_langfuse                                                                      │
│    ```                                                                                                 │
│                                                                                                        │
│ Success Criteria                                                                                       │
│                                                                                                        │
│ ✅ PostgreSQL:                                                                                          │
│ •  langfuse_db database created with langfuse_user as owner                                            │
│ •  Langfuse Prisma migrations execute successfully                                                     │
│ •  No schema conflicts with shared apexsigma_db                                                        │
│                                                                                                        │
│ ✅ ClickHouse:                                                                                          │
│ •  langfuse_analytics database created                                                                 │
│ •  langfuse_user has access to langfuse_analytics only                                                 │
│ •  observability_user has access to apexsigma_observability only                                       │
│ •  Clear separation between Langfuse analytics and observability metrics                               │
│                                                                                                        │
│ ✅ Langfuse Service:                                                                                    │
│ •  Container starts without errors                                                                     │
│ •  Health endpoint returns 200 OK                                                                      │
│ •  Traces are written to ClickHouse langfuse_analytics database                                        │
│ •  Web UI accessible at http://localhost:3001                                                          │
│                                                                                                        │
│ ✅ Observability Stack:                                                                                 │
│ •  Prometheus/Loki/Jaeger continue using apexsigma_observability database                              │
│ •  No cross-contamination of metrics/logs/traces between stacks                                        │
│                                                                                                        │
│ Migration Considerations                                                                               │
│                                                                                                        │
│ ⚠️ Data Loss Warning: Recreating volumes will delete existing data. If preservation is required:       │
│                                                                                                        │
│ Alternative: Manual Database Creation (preserves existing data):                                       │
│                                                                                                        │
│ bash                                                                                                   │
│   # PostgreSQL                                                                                         │
│   docker exec -it apexsigma_postgres psql -U apexsigma_user -d postgres -f                             │
│   /docker-entrypoint-initdb.d/init-langfuse.sql                                                        │
│                                                                                                        │
│   # ClickHouse                                                                                         │
│   docker exec -it apexsigma_clickhouse clickhouse-client --multiquery <                                │
│   config/clickhouse/init-langfuse.sql                                                                  │
│                                                                                                        │
│ Security Hardening (Post-Implementation)                                                               │
│                                                                                                        │
│ 1. Generate unique secrets for NEXTAUTH_SECRET and SALT                                                │
│ 2. Rotate default Apexsigma123_ passwords                                                              │
│ 3. Implement least-privilege access for observability_user                                             │
│ 4. Add audit logging for ClickHouse access                                                             │
│ 5. Configure backup strategy for both databases                                                        │
╰───────────────────────────────────────────────────────