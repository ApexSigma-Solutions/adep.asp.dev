"""Configuration management for the ApexSigma ecosystem."""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Defines the application settings, loaded from environment variables.

    Attributes:
        database_url: The URL for the primary database.
        redis_url: The URL for the Redis cache.
        qdrant_url: The URL for the Qdrant vector database.
        neo4j_url: The URL for the Neo4j graph database.
    """
    database_url: str
    redis_url: str
    qdrant_url: str
    neo4j_url: str

    class Config:
        """Pydantic configuration class.

        Specifies that settings should be loaded from a .env file.
        """
        env_file = ".env"

settings = Settings()
