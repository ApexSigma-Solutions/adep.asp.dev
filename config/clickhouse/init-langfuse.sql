-- Create dedicated Langfuse analytics database
CREATE DATABASE IF NOT EXISTS langfuse_analytics;

-- Note: User permissions are defined in users.xml, not granted via SQL

-- Switch to Langfuse database
USE langfuse_analytics;

-- Langfuse will create its own tables via migrations
-- Schema reference: https://langfuse.com/self-hosting/deployment/infrastructure/clickhouse