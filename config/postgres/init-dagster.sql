-- Dagster Database Initialization Script
-- This script creates the necessary tables for Dagster workflow orchestration
-- It is designed to be idempotent - safe to run multiple times

-- Create Dagster database if it doesn't exist
SELECT 'CREATE DATABASE dagster_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'dagster_db')\gexec

-- Connect to the Dagster database
\c dagster_db

-- Create extensions if they don't exist
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create Dagster core tables for instance management
CREATE TABLE IF NOT EXISTS instance_info (
    instance_name VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert default instance info if it doesn't exist
INSERT INTO instance_info (instance_name)
VALUES ('apexsigma_dagster_instance')
ON CONFLICT (instance_name) DO NOTHING;

-- Create daemon_heartbeats table for Dagster daemon monitoring
CREATE TABLE IF NOT EXISTS daemon_heartbeats (
    id SERIAL PRIMARY KEY,
    daemon_type VARCHAR(255) NOT NULL,
    daemon_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    heartbeat_data JSONB,
    UNIQUE(daemon_type, daemon_id)
);

-- Create index on daemon_heartbeats for performance
CREATE INDEX IF NOT EXISTS idx_daemon_heartbeats_type ON daemon_heartbeats(daemon_type);
CREATE INDEX IF NOT EXISTS idx_daemon_heartbeats_timestamp ON daemon_heartbeats(timestamp);

-- Create kvs (key-value store) table for Dagster instance storage
CREATE TABLE IF NOT EXISTS kvs (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) NOT NULL UNIQUE,
    value JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on kvs for performance
CREATE INDEX IF NOT EXISTS idx_kvs_key ON kvs(key);

-- Create or update function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for automatic timestamp updates
DROP TRIGGER IF EXISTS update_instance_updated_at ON instance_info;
CREATE TRIGGER update_instance_updated_at 
    BEFORE UPDATE ON instance_info 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_kvs_updated_at ON kvs;
CREATE TRIGGER update_kvs_updated_at 
    BEFORE UPDATE ON kvs 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create runs table for Dagster run tracking
CREATE TABLE IF NOT EXISTS runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id VARCHAR(255) NOT NULL UNIQUE,
    pipeline_name VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'QUEUED',
    run_body JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on runs for performance
CREATE INDEX IF NOT EXISTS idx_runs_pipeline ON runs(pipeline_name);
CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status);
CREATE INDEX IF NOT EXISTS idx_runs_created_at ON runs(created_at);

-- Create trigger for runs table
DROP TRIGGER IF EXISTS update_runs_updated_at ON runs;
CREATE TRIGGER update_runs_updated_at 
    BEFORE UPDATE ON runs 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default KVS entries for Dagster configuration
INSERT INTO kvs (key, value)
VALUES 
    ('dagster-instance-config', '{"storage": {"postgresql": {"postgres_url": "postgresql://apexsigma_user:Apexsigma123_@apexsigma_postgres:5432/dagster_db"}}}'),
    ('scheduler-config', '{"scheduler": {"module": "dagster.core.scheduler", "class": "DagsterDaemonScheduler"}}'),
    ('run-coordinator-config', '{"run_coordinator": {"module": "dagster.core.run_coordinator", "class": "DefaultRunCoordinator"}}')
ON CONFLICT (key) DO NOTHING;

-- Create sample daemon heartbeat entry
INSERT INTO daemon_heartbeats (daemon_type, daemon_id, heartbeat_data)
VALUES 
    ('scheduler', 'default-scheduler', '{"status": "running", "last_heartbeat": "' || CURRENT_TIMESTAMP || '"}'),
    ('run-coordinator', 'default-coordinator', '{"status": "running", "last_heartbeat": "' || CURRENT_TIMESTAMP || '"}')
ON CONFLICT (daemon_type, daemon_id) DO UPDATE SET
    timestamp = CURRENT_TIMESTAMP,
    heartbeat_data = EXCLUDED.heartbeat_data;

-- Grant permissions to the apexsigma_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO apexsigma_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO apexsigma_user;

-- Create Dagster user if it doesn't exist and grant permissions
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'dagster_user') THEN

      CREATE ROLE dagster_user LOGIN PASSWORD 'Apexsigma123_';
   END IF;
END
$do$;

GRANT CONNECT ON DATABASE dagster_db TO dagster_user;
GRANT USAGE ON SCHEMA public TO dagster_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO dagster_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO dagster_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dagster_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO dagster_user;

-- Output completion message
DO $$
BEGIN
    RAISE NOTICE 'Dagster database initialization completed successfully';
    RAISE NOTICE 'Tables created: instance_info, daemon_heartbeats, kvs, runs';
    RAISE NOTICE 'Default configuration inserted and permissions granted';
END $$;