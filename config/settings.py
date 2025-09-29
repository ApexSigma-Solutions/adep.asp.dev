"""
Centralized Pydantic Settings for ApexSigma Ecosystem

This module provides a single source of truth for all configuration values
across the ApexSigma microservices ecosystem. It loads from .env files and
provides type-safe access to environment variables.
"""

from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv
from typing import Optional

# Load environment variables from .env file in repo root
_env_file = find_dotenv(usecwd=True)
if _env_file:
    load_dotenv(_env_file)


class Settings(BaseSettings):
    """Centralized settings for ApexSigma services"""
    
    # === Database Configuration ===
    POSTGRES_HOST: str = Field("apexsigma_postgres", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(5432, description="PostgreSQL port")
    POSTGRES_DB: str = Field("apexsigma_db", description="PostgreSQL database name")
    POSTGRES_USER: str = Field("apexsigma_user", description="PostgreSQL username")
    POSTGRES_PASSWORD: Optional[str] = Field(None, description="PostgreSQL password")
    
    # === Redis Configuration ===
    REDIS_HOST: str = Field("apexsigma_redis", description="Redis host")
    REDIS_PORT: int = Field(6379, description="Redis port")
    
    # === Qdrant Vector Database ===
    QDRANT_HOST: str = Field("apexsigma_qdrant", description="Qdrant host")
    QDRANT_PORT: int = Field(6333, description="Qdrant port")
    
    # === Neo4j Graph Database ===
    NEO4J_HOST: str = Field("apexsigma_neo4j", description="Neo4j host")
    NEO4J_PORT: int = Field(7687, description="Neo4j port")
    NEO4J_AUTH: str = Field("neo4j/apexsigma_neo4j_password", description="Neo4j authentication")
    
    # === RabbitMQ Message Queue ===
    RABBITMQ_HOST: str = Field("apexsigma_rabbitmq", description="RabbitMQ host")
    RABBITMQ_PORT: int = Field(5672, description="RabbitMQ port")
    RABBITMQ_USER: str = Field("apexsigma_user", description="RabbitMQ username")
    RABBITMQ_PASSWORD: str = Field("apexsigma_pass", description="RabbitMQ password")
    
    # === Service Configuration ===
    DEVENVIRO_API_PORT: int = Field(8000, description="DevEnviro API port")
    MEMOS_API_PORT: int = Field(8090, description="Memos API port")
    INGEST_LLM_API_PORT: int = Field(8000, description="InGest-LLM API port")
    TOOLS_API_PORT: int = Field(8000, description="Tools API port")
    DAGSTER_WEBSERVER_PORT: int = Field(8080, description="Dagster webserver port")
    
    # === External Services ===
    LANGFUSE_HOST: str = Field("https://cloud.langfuse.com", description="Langfuse host")
    LANGFUSE_PUBLIC_KEY: Optional[str] = Field(None, description="Langfuse public key")
    LANGFUSE_SECRET_KEY: Optional[str] = Field(None, description="Langfuse secret key")
    SERPER_API_KEY: Optional[str] = Field(None, description="Serper API key for web search")
    TRUNK_API_TOKEN: Optional[str] = Field(None, description="Trunk API token")
    
    # === Environment Settings ===
    ENVIRONMENT: str = Field("development", description="Environment name")
    LOG_LEVEL: str = Field("INFO", description="Logging level")
    
    # === Test Configuration ===
    TEST_DATABASE_URL: Optional[str] = Field(None, description="Test database URL")
    
    # === Docker Compose ===
    COMPOSE_PROJECT_NAME: str = Field("apexsigma", description="Docker Compose project name")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @property
    def database_url(self) -> str:
        """Generate PostgreSQL connection URL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def redis_url(self) -> str:
        """Generate Redis connection URL"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    
    @property
    def qdrant_url(self) -> str:
        """Generate Qdrant connection URL"""
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"
    
    @property
    def neo4j_url(self) -> str:
        """Generate Neo4j connection URL"""
        return f"bolt://{self.NEO4J_HOST}:{self.NEO4J_PORT}"
    
    @property
    def rabbitmq_url(self) -> str:
        """Generate RabbitMQ connection URL"""
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get global settings instance.
    
    Provides backwards compatibility with Step 2 implementations.
    """
    return settings
