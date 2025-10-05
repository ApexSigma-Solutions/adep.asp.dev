from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: Optional[str] = None
    redis_url: Optional[str] = None
    qdrant_url: Optional[str] = None
    neo4j_url: Optional[str] = None

    # Pydantic v2 config: use model_config only (avoid defining Config and model_config together)
    model_config = {
        "extra": "ignore",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


# Only initialize settings when needed, not at import time
settings = None


def get_settings():
    global settings
    if settings is None:
        settings = Settings()
    return settings
