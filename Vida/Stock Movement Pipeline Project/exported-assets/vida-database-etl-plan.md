# Vida Stock Movement Analysis Project: Database and ETL Pipeline Design Plan

## Executive Summary

This comprehensive plan outlines the design and implementation strategy for building a robust database and ETL pipeline system for Vida e Caffe's stock movement analysis project. The system will consolidate data from multiple sources including daily operational reports, monthly digistics exports, GRV records, and recipe components to provide accurate Cost of Sales (COS) analysis and operational intelligence.

## 1. Project Overview

### 1.1 Business Objectives
- **Automated Stock Analysis**: Replace manual Excel-based COS calculations with automated, auditable processes
- **Data Consolidation**: Unify fragmented data sources into a single source of truth
- **Real-time Intelligence**: Enable timely decision-making through automated reporting and anomaly detection
- **Operational Efficiency**: Reduce time spent on data preparation and increase focus on analysis
- **Scalability**: Build architecture that can grow with business expansion

### 1.2 Key Challenges Addressed
- **Data Source Fragmentation**: Multiple Excel files with inconsistent naming and formats
- **Manual Processing**: Time-consuming manual data consolidation and validation
- **Error-Prone Calculations**: Risk of human error in complex COS calculations
- **Limited Historical Analysis**: Difficulty in tracking trends and patterns over time
- **Lack of Real-time Insights**: Delayed discovery of operational issues and opportunities

## 2. Technical Architecture

### 2.1 Database Design Strategy

#### Core Database Selection: SQLite
**Rationale**: SQLite provides the optimal balance of simplicity, performance, and functionality for this use case:
- **Zero Configuration**: No server setup or maintenance overhead
- **Single File Storage**: Easy backup, deployment, and portability
- **ACID Compliance**: Full transactional integrity with WAL mode
- **Excellent Performance**: Superior read performance for analytical workloads under 10,000 connections
- **Cross-Platform**: Runs identically across Windows, Linux, and macOS

#### Schema Architecture
The database follows a three-tier design pattern:

**1. Reference Layer (Master Data)**
- `store_registry`: Canonical store information with identifier reconciliation
- `item_registry`: Unified product catalog with VE, GAAP, and PLU code mapping
- `menu_items`: Menu catalog with pricing and categorization
- `recipe_components`: Ingredient breakdown for theoretical cost calculations
- `working_dates`: Calendar dimension for time-based analysis

**2. Transactional Layer (Operational Data)**
- `purchases`: Daily supplier purchases by store and item
- `transfers`: Inter-store inventory movements
- `sales`: Sales transactions with quantity and revenue details
- `wastage`: Stock loss tracking with reason codes
- `closing_stock`: Daily inventory positions with negative value protection
- `grv_records`: Goods received vouchers for compliance tracking

**3. Analytical Layer (Derived Intelligence)**
- `monthly_sales_summary`: Aggregated sales metrics for trend analysis
- `cos_summary`: Comprehensive Cost of Sales calculations with GP analysis
- `anomaly_flags`: Exception tracking and alerting
- `audit_log`: Complete data lineage and change tracking

### 2.2 Data Model Design Principles

#### Normalization Strategy
- **Third Normal Form (3NF)** for reference tables to eliminate redundancy
- **Selective Denormalization** in analytical tables for query performance
- **Surrogate Keys** (UUIDs) for all primary keys to ensure global uniqueness
- **Natural Keys** preserved for business reference and debugging

#### Data Quality Framework
- **Completeness**: Required field validation and null value handling
- **Accuracy**: Data type validation and range checking
- **Consistency**: Cross-reference validation and duplicate detection
- **Timeliness**: Data freshness monitoring and sequence validation

#### Audit and Traceability
- **Full Data Lineage**: Track data from source file to final calculation
- **Change Tracking**: Log all modifications with timestamp and user context
- **Exception Handling**: Comprehensive error logging and recovery procedures
- **Business Rule Documentation**: Embedded logic documentation in database

## 3. ETL Pipeline Architecture

### 3.1 Processing Framework

#### Multi-Stage Processing Pipeline
**Stage 1: Ingestion**
- Automated email attachment detection and download
- File format validation and standardization
- Duplicate detection and handling
- Raw data archival for compliance

**Stage 2: Extraction** 
- Excel/CSV parsing with error handling
- Schema validation against expected formats
- Data type conversion and standardization
- Source system reconciliation

**Stage 3: Transformation**
- Business rule application and calculation
- Data cleansing and normalization
- Reference data lookup and enrichment
- Aggregation and derived metric calculation

**Stage 4: Loading**
- Transactional loading with rollback capability
- Duplicate prevention and conflict resolution
- Index maintenance and optimization
- Data quality reporting and alerting

### 3.2 Data Flow Management

#### Batch Processing Strategy
- **Daily Processing**: Core operational data (purchases, sales, transfers, closing stock)
- **Weekly Processing**: Summary calculations and trend analysis
- **Monthly Processing**: GRV reconciliation and compliance reporting
- **On-Demand Processing**: Ad-hoc analysis and historical data migration

#### Error Handling and Recovery
- **Validation Errors**: Quarantine invalid records with detailed error reporting
- **System Errors**: Automatic retry with exponential backoff
- **Data Anomalies**: Business rule violation flagging and manual review queue
- **Recovery Procedures**: Point-in-time recovery and rollback capabilities

#### Performance Optimization
- **Incremental Loading**: Process only new or changed data
- **Parallel Processing**: Multi-threaded execution for large datasets
- **Index Optimization**: Strategic indexing for query performance
- **Memory Management**: Efficient batch sizing and resource utilization

## 4. Implementation Roadmap

### Phase 1: Foundation and Planning (14 days)
**Week 1-2: Requirements and Architecture**
- Requirements analysis and stakeholder alignment
- Data source inventory and mapping
- Technical architecture design and approval
- Development environment setup

**Key Deliverables:**
- Comprehensive requirements document
- Data flow diagrams and technical specifications
- Development environment and version control setup

### Phase 2: Database Design and Setup (17 days)
**Week 3-5: Core Infrastructure**
- Physical database schema implementation
- Reference data structure creation and population
- Index and constraint definition for performance
- Security configuration and backup strategy

**Key Deliverables:**
- Fully normalized database schema
- Populated reference tables with clean master data
- Optimized indexes and data integrity constraints
- Secure backup and recovery procedures

### Phase 3: ETL Development (35 days)
**Week 5-10: Pipeline Development**
- Email scraper development for automated file collection
- Data parser and validator creation
- Business logic and transformation engine implementation
- Comprehensive error handling and logging

**Key Deliverables:**
- Automated email processing system
- Robust data parsing and validation engine
- Complete business rule implementation
- Full audit trail and error recovery system

### Phase 4: Integration and Testing (29 days)
**Week 10-14: Quality Assurance**
- End-to-end pipeline testing
- Data quality validation and metric establishment
- Historical data migration and validation
- Performance optimization and tuning

**Key Deliverables:**
- Fully tested ETL pipeline
- Validated historical data migration
- Performance benchmarks met
- Comprehensive test documentation

### Phase 5: Analytics and Reporting (25 days)
**Week 14-18: Business Intelligence**
- COS calculation views and logic implementation
- Standard business intelligence reports
- Anomaly detection rules and alerting
- Interactive dashboard development

**Key Deliverables:**
- Accurate COS calculation engine
- Executive and operational dashboards
- Proactive anomaly detection system
- Self-service reporting capabilities

### Phase 6: Deployment and Optimization (15 days)
**Week 18-20: Production Launch**
- Production system deployment
- Monitoring and alerting system setup
- User training and documentation
- Go-live support and optimization

**Key Deliverables:**
- Stable production system
- Comprehensive monitoring and alerting
- Trained users with complete documentation
- Operational business value realization

## 5. Data Sources Integration

### 5.1 Daily Operational Reports
**Source Systems**: Digistics ERP system
**File Formats**: Excel (.xlsx) with standardized naming conventions
**Processing Frequency**: Daily, typically received by 13:00
**Data Types**:
- Purchase transactions with supplier details
- Inter-store transfer records
- Sales transactions by item and store
- Closing stock positions with quantities and values
- Wastage records with reason classification

### 5.2 Monthly Compliance Reports
**Source Systems**: GRV export system
**File Formats**: CSV files with monthly aggregation
**Processing Frequency**: Monthly, processed within 5 days of month-end
**Data Types**:
- Goods received vouchers by supplier
- Compliance tracking and validation
- Purchase order reconciliation

### 5.3 Master Data Sources
**Source Systems**: Product and store management systems
**File Formats**: Excel and CSV exports
**Processing Frequency**: Weekly or on-change basis
**Data Types**:
- Store registry with location details
- Item catalog with product specifications
- Recipe components and menu definitions
- Supplier information and pricing

### 5.4 Email Integration
**Automated Processing**: Python-based email scraper
**File Detection**: Intelligent parsing of attachment names and content
**Error Handling**: Duplicate detection and missing file alerts
**Archive Strategy**: Organized file storage with retention policies

## 6. Cost of Sales (COS) Calculation Framework

### 6.1 Calculation Methodology
The COS calculation follows standard retail accounting principles:

```sql
COS = Opening Stock + Purchases + Transfers In - Transfers Out - Closing Stock + Wastage
Gross Profit = Sales Revenue - COS
GP Percentage = (Gross Profit / Sales Revenue) × 100
```

### 6.2 Theoretical vs Actual Analysis
**Theoretical Cost Calculation**:
- Based on recipe components and menu item sales
- Uses standard ingredient costs and yield factors
- Provides baseline for performance measurement

**Actual Cost Tracking**:
- Based on physical stock movements and purchases
- Includes wastage and transfer adjustments
- Reflects real operational performance

**Variance Analysis**:
- Systematic comparison of theoretical vs actual costs
- Exception reporting for significant variances
- Trend analysis for continuous improvement

### 6.3 Advanced Analytics
**Shrinkage Analysis**: Identification of stock loss patterns and causes
**Supplier Performance**: Cost variance tracking by supplier and product
**Store Comparison**: Benchmarking across locations for best practices
**Seasonal Trends**: Historical pattern analysis for forecasting

## 7. Data Quality and Governance

### 7.1 Data Quality Framework
**Completeness Checks**: Ensure all required fields are populated
**Accuracy Validation**: Range checks and format validation
**Consistency Rules**: Cross-reference validation between related data
**Timeliness Monitoring**: Data freshness and sequence validation

### 7.2 Business Rules Engine
**Negative Stock Policy**: Automatic zeroing of negative closing stock values
**Date Validation**: Logical sequence and business day validation
**Price Reasonableness**: Statistical outlier detection and flagging
**Quantity Validation**: Reasonable range checking for all quantity fields

### 7.3 Exception Management
**Automated Alerts**: Real-time notification of data quality issues
**Manual Review Queue**: Systematic handling of exceptions requiring human judgment
**Resolution Tracking**: Complete audit trail of exception handling decisions
**Continuous Improvement**: Pattern analysis for proactive rule enhancement

## 8. Security and Compliance

### 8.1 Data Protection
**Access Control**: File system permissions and application-level security
**Encryption**: SQLCipher for sensitive data at rest
**Network Security**: TLS encryption for all data transmission
**Backup Encryption**: Secure storage of backup files

### 8.2 Audit and Compliance
**Complete Audit Trail**: All database operations logged with user context
**Data Lineage**: Full traceability from source to final calculation
**Retention Policies**: Automated data lifecycle management
**Regulatory Compliance**: SOX-style controls for financial data integrity

### 8.3 Disaster Recovery
**Recovery Time Objective (RTO)**: 2 hours maximum downtime
**Recovery Point Objective (RPO)**: 24 hours maximum data loss
**Backup Strategy**: Daily incremental, weekly full backups
**Geographic Distribution**: Multi-location backup storage

## 9. Performance and Scalability

### 9.1 Performance Optimization
**Query Optimization**: Strategic indexing and query plan analysis
**Memory Management**: Efficient caching and resource utilization
**I/O Optimization**: WAL mode and batch processing strategies
**Monitoring**: Continuous performance metric collection and analysis

### 9.2 Scalability Planning
**Data Growth**: 20% annual increase in transaction volume
**User Expansion**: Multi-user access with role-based security
**Geographic Growth**: Architecture supports multi-region deployment
**Feature Enhancement**: Extensible design for future requirements

### 9.3 Capacity Planning
**Storage Requirements**: 50-100GB annually with 7-year retention
**Processing Capacity**: Batch processing within 2-hour windows
**Concurrent Users**: Support for 10-50 simultaneous analytical users
**Network Bandwidth**: Optimized for typical business broadband connections

## 10. Monitoring and Maintenance

### 10.1 System Monitoring
**Performance Metrics**: Query execution time, database size, resource utilization
**Data Quality Metrics**: Completeness scores, anomaly detection rates
**Business Metrics**: Transaction volumes, processing success rates
**System Health**: Disk usage, memory consumption, process status

### 10.2 Alerting Strategy
**Critical Alerts**: System failures, data corruption, security breaches
**Warning Alerts**: Performance degradation, data anomalies, capacity issues
**Information Alerts**: Successful batch completions, scheduled maintenance

### 10.3 Maintenance Procedures
**Routine Maintenance**: Database optimization, index rebuilding, statistics updates
**Capacity Management**: Storage cleanup, archival procedures, growth monitoring
**Security Updates**: Regular patching and vulnerability assessment
**Performance Tuning**: Continuous optimization based on usage patterns

## 11. Success Metrics and KPIs

### 11.1 Technical Success Metrics
- **Data Processing Time**: 95% of daily batches completed within 2 hours
- **Data Quality**: 99.5% of records pass all validation checks
- **System Availability**: 99.9% uptime during business hours
- **Query Performance**: 95% of analytical queries complete within 5 seconds

### 11.2 Business Success Metrics
- **Time Savings**: 80% reduction in manual data processing time
- **Accuracy Improvement**: Elimination of manual calculation errors
- **Insight Generation**: Daily availability of COS analysis (vs. weekly manual)
- **Decision Support**: Real-time anomaly detection and alerting

### 11.3 User Adoption Metrics
- **User Satisfaction**: >90% satisfaction score from stakeholder surveys
- **Feature Utilization**: >80% of available reports accessed monthly
- **Self-Service Adoption**: >70% of routine queries handled without IT support
- **Training Effectiveness**: <2 hours average time to productivity for new users

## 12. Risk Management

### 12.1 Technical Risks
**Data Quality Issues**: Mitigation through comprehensive validation and exception handling
**System Performance**: Mitigation through optimization and capacity planning
**Integration Complexity**: Mitigation through modular design and thorough testing
**Technology Obsolescence**: Mitigation through standard technologies and upgrade planning

### 12.2 Business Risks
**User Adoption**: Mitigation through training and change management
**Requirement Changes**: Mitigation through agile methodology and stakeholder engagement
**Resource Availability**: Mitigation through cross-training and documentation
**Timeline Delays**: Mitigation through realistic planning and risk buffers

### 12.3 Operational Risks
**Data Loss**: Mitigation through robust backup and recovery procedures
**Security Breaches**: Mitigation through comprehensive security measures
**Compliance Violations**: Mitigation through automated controls and audit trails
**Vendor Dependencies**: Mitigation through standard technologies and multiple suppliers

## 13. Future Enhancements

### 13.1 Advanced Analytics
**Predictive Modeling**: Machine learning for demand forecasting and inventory optimization
**Real-time Processing**: Stream processing for immediate anomaly detection
**Advanced Visualization**: Interactive dashboards with drill-down capabilities
**Mobile Access**: Mobile-optimized reporting for field management

### 13.2 Integration Expansion
**ERP Integration**: Direct API integration with source systems
**Financial System Integration**: Automated GL posting and reconciliation
**Supply Chain Integration**: Supplier portal and automated ordering
**Business Intelligence Platform**: Integration with enterprise BI tools

### 13.3 Automation Enhancement
**Intelligent Anomaly Detection**: AI-powered pattern recognition
**Automated Reconciliation**: Self-healing data quality processes
**Dynamic Optimization**: Self-tuning performance optimization
**Predictive Maintenance**: Proactive system health management

## Conclusion

This comprehensive plan provides a robust foundation for building Vida e Caffe's stock movement analysis system. The combination of SQLite's simplicity and performance, comprehensive ETL capabilities, and business-focused analytics will deliver significant operational improvements while establishing a scalable platform for future growth.

The phased implementation approach ensures manageable risk while delivering value incrementally. The emphasis on data quality, security, and maintainability ensures long-term sustainability and reliability.

Success will be measured not only by technical performance but by the business value delivered through improved decision-making, operational efficiency, and strategic insights that drive competitive advantage in the retail food service industry.