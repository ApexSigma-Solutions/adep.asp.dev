# Create the ApexSigma Autonomous DevEx Pipeline workflow diagram
diagram_code = """
flowchart TD
    %% Hardware Layer (purple)
    HW["`**Hardware Layer**
    AMD ROCm | Ryzen 9
    28GB RAM | M780 GPU
    Vulkan Support`"]
    style HW fill:#9966CC,stroke:#663399,color:#fff
    
    %% External Systems (cloud shapes)
    GH["`**GitHub**
    Source Control`"]
    LIN["`**Linear**
    Issue Tracking`"]
    style GH fill:#E6F3FF,stroke:#0066CC
    style LIN fill:#E6F3FF,stroke:#0066CC
    
    %% Locally Hosted LLM (blue rectangle)
    LLM["`**LLM Orchestrator**
    Qwen 3 / Mistral / Codellama
    Quantized Python LLM`"]
    style LLM fill:#4A90E2,stroke:#2E5BBA,color:#fff
    
    %% Embedding Agent (orange rectangle)  
    EMB["`**Embedding Agent**
    Vector Embeddings
    Qdrant Ingestion`"]
    style EMB fill:#FF8C42,stroke:#E6762A,color:#fff
    
    %% Dagster Orchestrator (green diamond)
    DAG{"`**Dagster Orchestrator**
    Pipeline Assets:
    • Knowledge Graph
    • Vector DB
    • Graph DB
    • Ingest Pipeline`"}
    style DAG fill:#2ECC71,stroke:#27AE60,color:#fff
    
    %% Core Services (hexagons)
    DEV["`**devenviro.as**
    :8000
    /api/orchestration
    /api/agents`"]
    MEM["`**memos.as**
    :8001
    /api/knowledge
    /api/graph
    /api/search`"]
    ING["`**ingest-llm.as**
    :8002
    /api/ingestion
    /api/analysis`"]
    TOO["`**tools.as**
    :8003
    /api/tools
    /api/registry`"]
    
    style DEV fill:#3498DB,stroke:#2980B9,color:#fff
    style MEM fill:#3498DB,stroke:#2980B9,color:#fff
    style ING fill:#3498DB,stroke:#2980B9,color:#fff
    style TOO fill:#3498DB,stroke:#2980B9,color:#fff
    
    %% Infrastructure (cylinders)
    PG[("`**PostgreSQL**
    :5432
    postgres_data`")]
    NEO[("`**Neo4j**
    :7474,:7687
    neo4j_data`")]
    QDR[("`**Qdrant**
    :6333,:6334
    qdrant_data`")]
    RED[("`**Redis**
    :6379
    redis_data`")]
    
    style PG fill:#95A5A6,stroke:#7F8C8D,color:#fff
    style NEO fill:#95A5A6,stroke:#7F8C8D,color:#fff
    style QDR fill:#95A5A6,stroke:#7F8C8D,color:#fff
    style RED fill:#95A5A6,stroke:#7F8C8D,color:#fff
    
    %% Observability (diamonds)
    LANG{"`**Langfuse**
    :3000`"}
    JAEG{"`**Jaeger**
    :16686,:14268`"}
    PROM{"`**Prometheus**
    :9090`"}
    GRAF{"`**Grafana**
    :3001`"}
    
    style LANG fill:#F39C12,stroke:#E67E22,color:#fff
    style JAEG fill:#F39C12,stroke:#E67E22,color:#fff
    style PROM fill:#F39C12,stroke:#E67E22,color:#fff
    style GRAF fill:#F39C12,stroke:#E67E22,color:#fff
    
    %% Data Volumes (folders)
    VOL["`**Data Volumes**
    postgres_data
    neo4j_data
    qdrant_data
    redis_data
    langfuse_data
    grafana_data`"]
    style VOL fill:#F1C40F,stroke:#F39C12,color:#000
    
    %% Network Infrastructure
    NET["`**Docker Network**
    apexsigma-network
    Bridge: 172.20.0.0/16
    Gateway: 172.20.0.1`"]
    style NET fill:#8E44AD,stroke:#7D3C98,color:#fff
    
    %% Workflow Connections
    GH -->|"Trigger: PR/Issue/Task"| LLM
    LIN -->|"Issue Updates"| LLM
    LLM -->|"Task/Asset Coordination"| DAG
    
    DAG -->|"Run/Update Assets"| DEV
    DAG -->|"Run/Update Assets"| MEM  
    DAG -->|"Run/Update Assets"| ING
    DAG -->|"Run/Update Assets"| TOO
    
    ING -->|"Extract Embeddings"| EMB
    EMB -->|"Store Vectors"| QDR
    QDR -->|"Vector Search & Recall"| NEO
    NEO -->|"Semantic Graph Sync"| MEM
    
    %% Infrastructure Dependencies
    DEV -.-> PG
    MEM -.-> NEO
    MEM -.-> QDR
    ING -.-> RED
    TOO -.-> PG
    
    %% Observability Connections  
    DEV -->|"Metrics/Tracing"| LANG
    MEM -->|"Metrics/Tracing"| JAEG
    ING -->|"Metrics/Tracing"| PROM
    TOO -->|"Metrics/Tracing"| GRAF
    
    %% Hardware Dependencies
    HW -.-> LLM
    HW -.-> EMB
    HW -.-> NET
    
    %% Volume Dependencies
    PG -.-> VOL
    NEO -.-> VOL
    QDR -.-> VOL
    RED -.-> VOL
    LANG -.-> VOL
    GRAF -.-> VOL
    
    %% Network containment
    NET -.-> DEV
    NET -.-> MEM
    NET -.-> ING
    NET -.-> TOO
    NET -.-> PG
    NET -.-> NEO
    NET -.-> QDR
    NET -.-> RED
    NET -.-> LANG
    NET -.-> JAEG
    NET -.-> PROM
    NET -.-> GRAF
"""

# Create the mermaid diagram
png_path, svg_path = create_mermaid_diagram(
    diagram_code, 
    'apexsigma_devex_pipeline.png', 
    'apexsigma_devex_pipeline.svg',
    width=1600,
    height=1200
)

print(f"Mermaid diagram saved to: {png_path} and {svg_path}")