-- ClickHouse Database Initialization for ApexSigma Observability
-- This script creates the database schema for unified observability

-- Create the main observability database
CREATE DATABASE IF NOT EXISTS apexsigma_observability;
USE apexsigma_observability;

-- ==================================================
-- LANGFUSE TRACES TABLE
-- ==================================================
CREATE TABLE IF NOT EXISTS langfuse_traces (
    id UUID,
    timestamp DateTime64(3) DEFAULT now64(),
    project_id String,
    session_id String,
    user_id String,
    trace_name String,
    input String,
    output String,
    metadata String,
    tags Array(String),
    model String,
    model_parameters String,
    usage_prompt_tokens UInt32 DEFAULT 0,
    usage_completion_tokens UInt32 DEFAULT 0,
    usage_total_tokens UInt32 DEFAULT 0,
    latency_ms UInt32 DEFAULT 0,
    cost_usd Float64 DEFAULT 0.0,
    level String DEFAULT 'DEFAULT',
    status_message String DEFAULT '',
    version String DEFAULT '',
    created_at DateTime64(3) DEFAULT now64(),
    updated_at DateTime64(3) DEFAULT now64()
) ENGINE = MergeTree()
ORDER BY (project_id, timestamp, id)
PARTITION BY toYYYYMM(timestamp)
TTL toDateTime(timestamp) + INTERVAL 90 DAY
SETTINGS index_granularity = 8192;

-- ==================================================
-- SYSTEM LOGS TABLE (for Vector pipeline)
-- ==================================================
CREATE TABLE IF NOT EXISTS logs (
    timestamp DateTime64(3),
    level String,
    service String,
    container_name String DEFAULT '',
    message String,
    metadata String DEFAULT '{}',
    source String DEFAULT 'unknown',
    host String DEFAULT '',
    labels Map(String, String)
) ENGINE = MergeTree()
ORDER BY (service, timestamp)
PARTITION BY toYYYYMMDD(timestamp)
TTL toDateTime(timestamp) + INTERVAL 30 DAY
SETTINGS index_granularity = 8192;

-- ==================================================
-- PROMETHEUS METRICS TABLE
-- ==================================================
CREATE TABLE IF NOT EXISTS prometheus_metrics (
    metric_name String,
    timestamp DateTime64(3),
    value Float64,
    labels Map(String, String),
    source String DEFAULT 'prometheus',
    job String DEFAULT '',
    instance String DEFAULT ''
) ENGINE = MergeTree()
ORDER BY (metric_name, timestamp)
PARTITION BY toYYYYMM(timestamp)
TTL toDateTime(timestamp) + INTERVAL 90 DAY
SETTINGS index_granularity = 8192;

-- ==================================================
-- JAEGER SPANS TABLE
-- ==================================================
CREATE TABLE IF NOT EXISTS jaeger_spans (
    trace_id String,
    span_id String,
    parent_span_id String DEFAULT '',
    operation_name String,
    start_time DateTime64(6),
    duration_microseconds UInt64,
    tags Map(String, String),
    logs Array(Map(String, String)),
    process_service_name String,
    process_tags Map(String, String)
) ENGINE = MergeTree()
ORDER BY (trace_id, start_time)
PARTITION BY toYYYYMMDD(start_time)
TTL toDateTime(start_time) + INTERVAL 30 DAY
SETTINGS index_granularity = 8192;

-- ==================================================
-- MATERIALIZED VIEWS FOR AGGREGATIONS
-- ==================================================

-- Service health metrics aggregated by minute
CREATE MATERIALIZED VIEW IF NOT EXISTS service_health_minutely
ENGINE = SummingMergeTree()
ORDER BY (service, timestamp_minute)
PARTITION BY toYYYYMM(timestamp_minute) AS
SELECT
    service,
    toStartOfMinute(timestamp) as timestamp_minute,
    count() as log_count,
    countIf(level = 'ERROR') as error_count,
    countIf(level = 'WARN') as warning_count,
    countIf(level = 'INFO') as info_count
FROM logs
GROUP BY service, timestamp_minute;

-- Langfuse usage metrics by hour
CREATE MATERIALIZED VIEW IF NOT EXISTS langfuse_usage_hourly
ENGINE = SummingMergeTree()
ORDER BY (project_id, timestamp_hour)
PARTITION BY toYYYYMM(timestamp_hour) AS
SELECT
    project_id,
    toStartOfHour(timestamp) as timestamp_hour,
    count() as trace_count,
    sum(usage_total_tokens) as total_tokens,
    sum(cost_usd) as total_cost_usd,
    avg(latency_ms) as avg_latency_ms,
    countIf(level = 'ERROR') as error_count
FROM langfuse_traces
GROUP BY project_id, timestamp_hour;

-- ==================================================
-- INDEXES FOR PERFORMANCE
-- ==================================================

-- Index for fast service filtering
ALTER TABLE logs ADD INDEX IF NOT EXISTS idx_service service TYPE bloom_filter(0.01) GRANULARITY 1;

-- Index for fast level filtering  
ALTER TABLE logs ADD INDEX IF NOT EXISTS idx_level level TYPE set(100) GRANULARITY 1;

-- Index for fast metric name filtering
ALTER TABLE prometheus_metrics ADD INDEX IF NOT EXISTS idx_metric_name metric_name TYPE bloom_filter(0.01) GRANULARITY 1;

-- Index for fast trace filtering
ALTER TABLE langfuse_traces ADD INDEX IF NOT EXISTS idx_project_id project_id TYPE bloom_filter(0.01) GRANULARITY 1;

-- ==================================================
-- SAMPLE QUERIES FOR TESTING
-- ==================================================

-- Test data insertion (will be removed in production)
-- Temporarily disabled due to database context issues
-- INSERT INTO logs (timestamp, level, service, message) VALUES
--     (now64(), 'INFO', 'test-service', 'ClickHouse initialization complete'),
--     (now64(), 'INFO', 'clickhouse', 'Database schema created successfully');

-- Validate table creation
SELECT
    name,
    engine,
    total_rows,
    total_bytes
FROM system.tables
WHERE database = 'apexsigma_observability'
ORDER BY name;

-- ==================================================
-- LANGFUSE ANALYTICS DATABASE INITIALIZATION
-- ==================================================

-- Execute Langfuse-specific initialization
SOURCE /docker-entrypoint-initdb.d/init-langfuse.sql;
