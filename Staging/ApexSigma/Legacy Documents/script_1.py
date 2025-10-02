# Create detailed workflow mapping CSV for the ecosystem
import pandas as pd

# Create workflow entry points mapping
workflow_data = {
    "Component": [
        "SigmaDev11 (Human)",
        "Gemini (MAR Guardian)", 
        "Gemini CLI (DevOps)",
        "Qwen 3 Coder Plus (Config)",
        "devenviro.as",
        "memos.as",
        "ingest-llm.as", 
        "tools.as",
        "GitHub Actions",
        "Linear Integration"
    ],
    "Entry Point": [
        "Strategic Direction & Approval Authority",
        "MAR Protocol Review & Quality Gates",
        "Infrastructure Implementation & Docker Orchestration",
        "Code Generation & Configuration Management",
        "/api/orchestration, /api/agents - Task Distribution Hub",
        "/api/knowledge, /api/memory, /api/graph - Knowledge Management",
        "/api/ingestion, /api/processing - Document Gateway",
        "/api/tools, /api/registry - Utility Services",
        "Webhook Triggers from Repository Events",
        "Task Synchronization & Agent Assignment"
    ],
    "Container/Port": [
        "N/A (Human Interface)",
        "N/A (AI Agent Interface)",
        "N/A (AI Agent Interface)",
        "N/A (AI Agent Interface)", 
        "devenviro-as:8000",
        "memos-as:8001",
        "ingest-llm-as:8002",
        "tools-as:8003",
        "External Platform",
        "External Platform"
    ],
    "Primary Dependencies": [
        "All Services (Admin Access)",
        "devenviro.as, memos.as, GitHub",
        "Docker Network, Infrastructure Services",
        "Configuration APIs, Testing Frameworks",
        "postgres, redis, langfuse, jaeger",
        "postgres, neo4j, qdrant, redis, langfuse",
        "qdrant, memos.as, langfuse",
        "postgres, langfuse",
        "devenviro.as webhooks",
        "devenviro.as API"
    ],
    "Data Flow Direction": [
        "Bidirectional (Command & Status)",
        "Inbound Review → Outbound Approval",
        "Outbound Implementation → Inbound Status",
        "Outbound Generation → Inbound Validation",
        "Hub (All Directions - Orchestration)",
        "Inbound Storage → Outbound Retrieval",
        "Inbound Processing → Outbound Results",
        "Bidirectional (Tool Access)",
        "Inbound Events → Outbound Updates",
        "Bidirectional (Task Sync)"
    ]
}

# Create infrastructure mapping
infrastructure_data = {
    "Service": [
        "postgres", "neo4j", "qdrant", "redis",
        "langfuse", "jaeger", "prometheus", "grafana"
    ],
    "Container Name": [
        "postgres", "neo4j", "qdrant", "redis",
        "langfuse", "jaeger", "prometheus", "grafana"
    ],
    "Port Mapping": [
        "5432:5432", "7474:7474, 7687:7687", "6333:6333, 6334:6334", "6379:6379",
        "3000:3000", "16686:16686, 14268:14268", "9090:9090", "3001:3000"
    ],
    "Data Storage Type": [
        "Relational (Agent Registry, Sessions, Config)",
        "Graph (Knowledge Relationships, Dependencies)",
        "Vector (Document Embeddings, Semantic Search)",
        "Cache (Session State, Agent Status, Queues)",
        "Observability (LLM Traces, Performance Metrics)",
        "Tracing (Request Traces, Service Dependencies)",
        "Metrics (System & Application Metrics)",
        "Visualization (Dashboards, Health Monitoring)"
    ],
    "Volume Mount": [
        "postgres_data:/var/lib/postgresql/data",
        "neo4j_data:/data, neo4j_logs:/logs",
        "qdrant_data:/qdrant/storage",
        "redis_data:/data",
        "langfuse_data:/app/data",
        "N/A (Ephemeral)",
        "./config/prometheus.yml:/etc/prometheus/prometheus.yml",
        "grafana_data:/var/lib/grafana, ./config/grafana:/etc/grafana/provisioning"
    ],
    "Network Dependencies": [
        "Core Hub - All services connect",
        "memos.as primary connection",
        "ingest-llm.as, memos.as primary connections",
        "All services for caching",
        "All services for tracing",
        "All services for distributed tracing",
        "All services for metrics collection", 
        "prometheus, langfuse for data sources"
    ]
}

# Create workflow patterns mapping
workflow_patterns_data = {
    "Workflow Pattern": [
        "MAR Protocol Flow",
        "Omega Ingest Flow", 
        "Agent Coordination Flow",
        "CI/CD Pipeline Flow",
        "Knowledge Graph Update Flow",
        "Error Handling & Recovery Flow"
    ],
    "Trigger Event": [
        "Code/Config change in GitHub",
        "Knowledge update required",
        "Task assignment from SigmaDev11",
        "Pull Request or Push to Alpha branch",
        "Document ingestion or analysis",
        "Service failure or error condition"
    ],
    "Entry Point": [
        "GitHub → devenviro.as webhook",
        "Source → ingest-llm.as API",
        "SigmaDev11 → devenviro.as orchestration",
        "GitHub Actions → devenviro.as webhook",
        "ingest-llm.as → memos.as API",
        "Service Health Check → devenviro.as"
    ],
    "Processing Path": [
        "devenviro.as → Gemini Review → Agent Implementation → Deployment",
        "ingest-llm.as → Processing → memos.as → Knowledge Graph Update",
        "devenviro.as → Agent Assignment → Task Execution → Review → Completion",
        "GitHub → devenviro.as → CI Tests → Staging → Production",
        "Document → Vectorization → Storage → Graph Relationships",
        "Error Detection → Escalation → Recovery Action → Verification"
    ],
    "Quality Checkpoints": [
        "Initial review, Implementation review, Deployment approval",
        "Data validation, Processing verification, Graph integration",
        "Task creation, Agent assignment, Implementation, Quality review",
        "Code quality, Security scan, Integration tests, Deployment verification",
        "Document validation, Vector quality, Graph consistency",
        "Error classification, Recovery validation, System health verification"
    ],
    "End State": [
        "Code deployed to production with MAR approval",
        "Knowledge successfully integrated into graph",
        "Task completed with agent sign-off",
        "Feature deployed with full CI/CD validation",
        "Knowledge accessible via semantic search",
        "System restored to healthy state"
    ]
}

# Create DataFrames
workflow_df = pd.DataFrame(workflow_data)
infrastructure_df = pd.DataFrame(infrastructure_data)
workflow_patterns_df = pd.DataFrame(workflow_patterns_data)

# Save to CSV files
workflow_df.to_csv("workflow_entry_points.csv", index=False)
infrastructure_df.to_csv("infrastructure_services.csv", index=False)
workflow_patterns_df.to_csv("workflow_patterns.csv", index=False)

print("=== WORKFLOW ENTRY POINTS & NETWORK MAPPING ===")
print(workflow_df.to_string(index=False))
print("\n=== INFRASTRUCTURE SERVICES MAPPING ===")
print(infrastructure_df.to_string(index=False))
print("\n=== WORKFLOW PATTERNS MAPPING ===") 
print(workflow_patterns_df.to_string(index=False))

print(f"\n✅ Detailed ecosystem mapping saved to:")
print(f"  - workflow_entry_points.csv")
print(f"  - infrastructure_services.csv")
print(f"  - workflow_patterns.csv")