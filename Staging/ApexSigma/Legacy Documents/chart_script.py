# Create a simplified and cleaner Mermaid flowchart addressing the feedback
diagram_code = """
flowchart TD
    %% Agent Hierarchy Layer
    subgraph "Agent Hierarchy"
        SD[SigmaDev11<br/>Strategic Leader]
        G((Gemini<br/>MAR Guardian))
        GC((Gemini CLI<br/>DevOps Agent))
        QC((Qwen Coder<br/>Config Agent))
    end
    
    %% Core Services Layer  
    subgraph "Core Services"
        DE{{devenviro:8000<br/>Orchestrator}}
        MM{{memos:8001<br/>Knowledge}}
        IL{{ingest:8002<br/>Documents}}
        TL{{tools:8003<br/>Registry}}
    end
    
    %% Data Layer
    subgraph "Data Infrastructure" 
        PG[(PostgreSQL:5432)]
        N4[(Neo4j:7474/7687)]
        QD[(Qdrant:6333/6334)]
        RD[(Redis:6379)]
    end
    
    %% Monitoring Layer
    subgraph "Observability"
        LF{Langfuse:3000}
        JG{Jaeger:16686}
        PM{Prometheus:9090}
        GR{Grafana:3001}
    end
    
    %% External Systems
    subgraph "External"
        GH[("GitHub")]
        LIN[("Linear")]
    end
    
    %% Primary Command Flow
    SD ==> DE
    SD ==> G
    G ==> GC
    G ==> QC
    
    %% Service Interactions
    DE --> MM
    DE --> IL  
    DE --> TL
    
    %% Data Connections
    DE -.-> PG
    MM -.-> PG
    MM -.-> N4
    IL -.-> QD
    TL -.-> RD
    
    %% External Integration
    GH --> DE
    DE --> GH
    LIN --> DE
    
    %% Monitoring
    DE --> LF
    MM --> JG
    IL --> PM
    PM --> GR
    
    %% Key Workflows
    GH -->|MAR Protocol| G
    G -->|Execute| DE
    IL -->|Process| MM
    MM -->|Store| N4
"""

# Create the simplified Mermaid diagram
png_file, svg_file = create_mermaid_diagram(
    diagram_code, 
    'apexsigma_pipeline_clean.png',
    'apexsigma_pipeline_clean.svg',
    width=1200,
    height=800
)

print(f"Clean diagram saved as: {png_file} and {svg_file}")