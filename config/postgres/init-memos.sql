-- memOS.as Database Initialization Script
-- This script creates the necessary tables for memOS.as with proper constraints
-- It is designed to be idempotent - safe to run multiple times

-- Create memOS database if it doesn't exist
SELECT 'CREATE DATABASE apexsigma_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'apexsigma_db')\gexec

-- Connect to the memOS database
\c apexsigma_db

-- Create extensions if they don't exist
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create memories table for episodic memory storage
CREATE TABLE IF NOT EXISTS memories (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    tier VARCHAR(255) NOT NULL DEFAULT 'default',
    memory_metadata JSONB,
    embedding_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Create index on memories table for performance
CREATE INDEX IF NOT EXISTS idx_memories_tier ON memories(tier);
CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at);
CREATE INDEX IF NOT EXISTS idx_memories_embedding_id ON memories(embedding_id);
CREATE INDEX IF NOT EXISTS idx_memories_expires_at ON memories(expires_at);

-- Create registered_tools table for tool registry
CREATE TABLE IF NOT EXISTS registered_tools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    usage TEXT NOT NULL,
    tags JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on tools table
CREATE INDEX IF NOT EXISTS idx_tools_name ON registered_tools(name);
CREATE INDEX IF NOT EXISTS idx_tools_tags ON registered_tools USING GIN(tags);

-- Create knowledge_share_requests table for inter-agent knowledge sharing
CREATE TABLE IF NOT EXISTS knowledge_share_requests (
    id SERIAL PRIMARY KEY,
    requester_agent_id VARCHAR(255) NOT NULL,
    target_agent_id VARCHAR(255) NOT NULL,
    query TEXT NOT NULL,
    confidence_threshold FLOAT NOT NULL,
    sharing_policy VARCHAR(255) NOT NULL DEFAULT 'high_confidence_only',
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create knowledge_share_offers table for knowledge sharing responses
CREATE TABLE IF NOT EXISTS knowledge_share_offers (
    id SERIAL PRIMARY KEY,
    request_id INTEGER NOT NULL REFERENCES knowledge_share_requests(id),
    offering_agent_id VARCHAR(255) NOT NULL,
    memory_id INTEGER NOT NULL REFERENCES memories(id),
    confidence_score FLOAT NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for knowledge sharing tables
CREATE INDEX IF NOT EXISTS idx_share_requests_target ON knowledge_share_requests(target_agent_id);
CREATE INDEX IF NOT EXISTS idx_share_requests_status ON knowledge_share_requests(status);
CREATE INDEX IF NOT EXISTS idx_share_offers_request ON knowledge_share_offers(request_id);
CREATE INDEX IF NOT EXISTS idx_share_offers_memory ON knowledge_share_offers(memory_id);

-- Create or update function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for automatic timestamp updates
DROP TRIGGER IF EXISTS update_memories_updated_at ON memories;
CREATE TRIGGER update_memories_updated_at 
    BEFORE UPDATE ON memories 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_tools_updated_at ON registered_tools;
CREATE TRIGGER update_tools_updated_at 
    BEFORE UPDATE ON registered_tools 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert some default tools if they don't exist
INSERT INTO registered_tools (name, description, usage, tags)
VALUES 
    ('memory_store', 'Store episodic memories in the memOS system', 'POST /memory/store with content and metadata', '["memory", "storage", "episodic"]'),
    ('memory_query', 'Query stored memories by content or semantic search', 'GET /memory/query with search parameters', '["memory", "search", "query"]'),
    ('tool_register', 'Register new tools in the tool registry', 'POST /tools/register with tool details', '["tools", "registry", "discovery"]'),
    ('knowledge_share', 'Share knowledge between agents', 'POST /knowledge/share with sharing parameters', '["knowledge", "sharing", "agents"]')
ON CONFLICT (name) DO NOTHING;

-- Grant permissions to the apexsigma_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO apexsigma_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO apexsigma_user;

-- Create memOS user if it doesn't exist and grant permissions
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'memos_user') THEN

      CREATE ROLE memos_user LOGIN PASSWORD 'Apexsigma123_';
   END IF;
END
$do$;

GRANT CONNECT ON DATABASE apexsigma_db TO memos_user;
GRANT USAGE ON SCHEMA public TO memos_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO memos_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO memos_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO memos_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO memos_user;

-- Output completion message
DO $$
BEGIN
    RAISE NOTICE 'memOS.as database initialization completed successfully';
    RAISE NOTICE 'Tables created: memories, registered_tools, knowledge_share_requests, knowledge_share_offers';
    RAISE NOTICE 'Default tools inserted and permissions granted';
END $$;