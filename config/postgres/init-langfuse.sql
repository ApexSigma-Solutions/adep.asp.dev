-- Create dedicated Langfuse database
CREATE DATABASE langfuse_db;

-- Create dedicated Langfuse user
CREATE USER langfuse_user WITH PASSWORD 'Apexsigma123_';

-- Grant full privileges to Langfuse user on langfuse_db
GRANT ALL PRIVILEGES ON DATABASE langfuse_db TO langfuse_user;

-- Allow schema creation
ALTER DATABASE langfuse_db OWNER TO langfuse_user;