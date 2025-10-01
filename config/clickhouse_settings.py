"""
ClickHouse Configuration Settings for ApexSigma Ecosystem
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv

# Load environment variables
_env_file = find_dotenv(usecwd=True)
if _env_file:
    load_dotenv(_env_file)


class ClickHouseSettings(BaseSettings):
    """ClickHouse-specific settings"""
    
    # === ClickHouse OLAP Database ===
    CLICKHOUSE_HOST: str = Field("clickhouse", description="ClickHouse host")
    CLICKHOUSE_PORT: int = Field(8123, description="ClickHouse HTTP port")
    CLICKHOUSE_NATIVE_PORT: int = Field(9000, description="ClickHouse native TCP port")
    CLICKHOUSE_USER: str = Field("clickhouse_user", description="ClickHouse username")
    CLICKHOUSE_PASSWORD: Optional[str] = Field("change_me_securely", description="ClickHouse password")
    CLICKHOUSE_DB: str = Field("apexsigma_observability", description="ClickHouse database")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @property
    def clickhouse_url(self) -> str:
        """Generate ClickHouse HTTP connection URL"""
        return f"http://{self.CLICKHOUSE_HOST}:{self.CLICKHOUSE_PORT}"

    @property
    def clickhouse_native_url(self) -> str:
        """Generate ClickHouse native TCP connection URL"""
        return f"clickhouse://{self.CLICKHOUSE_USER}:{self.CLICKHOUSE_PASSWORD}@{self.CLICKHOUSE_HOST}:{self.CLICKHOUSE_NATIVE_PORT}/{self.CLICKHOUSE_DB}"
    
    @property
    def clickhouse_connection_params(self) -> dict:
        """Get ClickHouse connection parameters for client libraries"""
        return {
            "host": self.CLICKHOUSE_HOST,
            "port": self.CLICKHOUSE_PORT,
            "user": self.CLICKHOUSE_USER,
            "password": self.CLICKHOUSE_PASSWORD,
            "database": self.CLICKHOUSE_DB,
        }


# Global ClickHouse settings instance
clickhouse_settings = ClickHouseSettings()


def get_clickhouse_settings() -> ClickHouseSettings:
    """Get global ClickHouse settings instance"""
    return clickhouse_settings
