# Create the mermaid diagram for Vida Stock ETL Pipeline Architecture
diagram_code = """
flowchart LR
    subgraph DS ["Data Sources"]
        A1["Daily Excel<br/>Reports<br/>(Daily)"]
        A2["Monthly<br/>Reports<br/>(Monthly)"]
        A3["Master Data<br/>(Static)"]
        A4["Email<br/>Attachments<br/>(Daily)"]
    end
    
    subgraph IL ["Ingestion Layer"]
        B1["File Detection<br/>& Validation"]
        B2["Email Scraper<br/>Service"]
        B3["Format<br/>Standard"]
        B4["Data Quality<br/>Checks"]
    end
    
    subgraph PL ["Processing Layer"]
        C1["Extract<br/>(Parse Files)"]
        C2["Transform<br/>(Clean/Norm)"]
        C3["Load<br/>(DB Ops)"]
        C4["Reference<br/>Reconcile"]
        C5["Business<br/>Rules Engine"]
    end
    
    subgraph SL ["Storage Layer"]
        D1["SQLite<br/>Database"]
        D2["Raw Data<br/>Archive"]
        D3["Processed<br/>Tables"]
        D4["Metadata &<br/>Audit Logs"]
    end
    
    subgraph OL ["Output Layer"]
        E1["COS Analysis<br/>Views"]
        E2["Reporting<br/>APIs"]
        E3["Business<br/>Intelligence"]
        E4["Anomaly<br/>Detection"]
        E5["Automated<br/>Reports"]
    end
    
    subgraph EH ["Error Handling"]
        F1["Error Logs"]
        F2["Retry Logic"]
        F3["Alerts"]
    end
    
    %% Data Flow Arrows
    A1 --> B1
    A1 --> B3
    A2 --> B1
    A2 --> B3
    A3 --> B1
    A4 --> B2
    
    B1 --> C1
    B2 --> C1
    B3 --> C1
    B4 --> C2
    
    C1 --> C2
    C2 --> C3
    C3 --> D1
    C3 --> D2
    C4 --> C2
    C5 --> C2
    
    D1 --> D3
    D2 --> D4
    D3 --> E1
    D3 --> E2
    D1 --> E3
    D1 --> E4
    D3 --> E5
    
    %% Error Handling Paths
    B1 --> F1
    B4 --> F2
    C2 --> F1
    C3 --> F3
    
    %% Styling
    classDef dataSource fill:#B3E5EC,stroke:#1FB8CD,stroke-width:2px
    classDef ingestion fill:#FFCDD2,stroke:#DB4545,stroke-width:2px
    classDef processing fill:#A5D6A7,stroke:#2E8B57,stroke-width:2px
    classDef storage fill:#9FA8B0,stroke:#5D878F,stroke-width:2px
    classDef output fill:#FFEB8A,stroke:#D2BA4C,stroke-width:2px
    classDef error fill:#F5F5F5,stroke:#B4413C,stroke-width:2px
    
    class A1,A2,A3,A4 dataSource
    class B1,B2,B3,B4 ingestion
    class C1,C2,C3,C4,C5 processing
    class D1,D2,D3,D4 storage
    class E1,E2,E3,E4,E5 output
    class F1,F2,F3 error
"""

# Create the diagram and save as both PNG and SVG
png_path, svg_path = create_mermaid_diagram(diagram_code, 'vida_etl_pipeline.png', 'vida_etl_pipeline.svg', width=1400, height=900)

print(f"Diagram saved as PNG: {png_path}")
print(f"Diagram saved as SVG: {svg_path}")