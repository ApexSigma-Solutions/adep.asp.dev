# Create a comprehensive database schema diagram for Vida Stock Movement Analysis
diagram_code = '''
erDiagram
    %% Reference Tables (Light Blue)
    store_registry {
        uuid store_id PK
        string store_name
        string vid_code
        string gaap_code
        string region
        string status
    }
    
    item_registry {
        uuid item_id PK
        string ve_code
        string gaap_code
        string plu_code
        string description
        decimal pack_size
        string supplier
        string status
    }
    
    menu_items {
        string plu_code PK
        string menu_name
        string category
        decimal price
    }
    
    recipe_components {
        string plu_code
        uuid item_id
        decimal quantity
        string unit
        decimal yield_factor
    }
    
    working_dates {
        date report_date
        uuid store_id
        string day_of_week
        string month
        boolean is_month_end
    }

    %% Transactional Tables (Light Green)
    purchases {
        uuid purchase_id PK
        uuid store_id FK
        uuid item_id FK
        date report_date
        string supplier
        decimal quantity
        decimal unit_cost
        decimal total_cost
    }
    
    transfers {
        uuid transfer_id PK
        uuid store_id_from FK
        uuid store_id_to FK
        uuid item_id FK
        date report_date
        decimal quantity
        decimal unit_cost
        decimal total_cost
    }
    
    sales {
        uuid sale_id PK
        uuid store_id FK
        uuid item_id FK
        date report_date
        decimal quantity_sold
        decimal unit_price
        decimal total_revenue
    }
    
    wastage {
        uuid wastage_id PK
        uuid store_id FK
        uuid item_id FK
        date report_date
        decimal quantity_wasted
        decimal unit_cost
        decimal total_cost
        string reason
    }
    
    closing_stock {
        uuid stock_id PK
        uuid store_id FK
        uuid item_id FK
        date report_date
        decimal closing_quantity
        decimal unit_cost
        decimal closing_value
        decimal raw_closing_quantity
    }
    
    grv_records {
        uuid grv_id PK
        uuid store_id FK
        uuid item_id FK
        date report_date
        string supplier
        decimal quantity_received
        decimal unit_cost
        decimal total_cost
    }

    %% Derived Tables (Light Yellow)
    monthly_sales_summary {
        uuid summary_id PK
        uuid store_id FK
        uuid item_id FK
        string month_year
        decimal total_quantity
        decimal total_revenue
        decimal avg_price
    }
    
    cos_summary {
        uuid cos_id PK
        uuid store_id FK
        date report_date
        decimal total_sales
        decimal total_purchases
        decimal total_transfers_in
        decimal total_transfers_out
        decimal total_wastage
        decimal closing_stock_value
        decimal theoretical_cost
        decimal actual_cost
        decimal gross_profit
        decimal gp_percentage
        decimal shrinkage_value
        decimal shrinkage_percentage
    }

    %% Relationships
    store_registry ||--o{ purchases : "has"
    store_registry ||--o{ transfers : "from"
    store_registry ||--o{ transfers : "to"
    store_registry ||--o{ sales : "has"
    store_registry ||--o{ wastage : "has"
    store_registry ||--o{ closing_stock : "has"
    store_registry ||--o{ grv_records : "has"
    store_registry ||--o{ working_dates : "has"
    store_registry ||--o{ monthly_sales_summary : "has"
    store_registry ||--o{ cos_summary : "has"
    
    item_registry ||--o{ purchases : "contains"
    item_registry ||--o{ transfers : "contains"
    item_registry ||--o{ sales : "contains"
    item_registry ||--o{ wastage : "contains"
    item_registry ||--o{ closing_stock : "contains"
    item_registry ||--o{ grv_records : "contains"
    item_registry ||--o{ recipe_components : "used_in"
    item_registry ||--o{ monthly_sales_summary : "contains"
    
    menu_items ||--o{ recipe_components : "requires"
'''

# Create the mermaid diagram and save as both PNG and SVG
png_path, svg_path = create_mermaid_diagram(diagram_code, 'vida_schema.png', 'vida_schema.svg', width=1400, height=1000)

print(f"Database schema diagram saved to: {png_path} and {svg_path}")