"""
Test-specific configuration settings for ApexSigma Ecosystem

This module provides test environment configuration that extends the centralized
settings system with test-specific overrides for database isolation and cleanup.
"""

import os
import uuid
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

from .settings import Settings as BaseSettings


class TestSettings(BaseSettings):
    """Test-specific configuration that extends base settings with test isolation."""
    
    # Test environment detection
    TESTING: bool = Field(default=False, description="Enable test mode")
    TEST_SESSION_ID: str = Field(default_factory=lambda: str(uuid.uuid4())[:8], description="Unique test session identifier")
    
    # Test database configuration - isolated from production
    TEST_POSTGRES_DB: str = Field(default="apexsigma_test_db", description="Test database name")
    TEST_POSTGRES_HOST: str = Field(default="apexsigma_postgres", description="Test database host")
    TEST_POSTGRES_PORT: int = Field(default=5432, description="Test database port")
    TEST_POSTGRES_USER: str = Field(default="apexsigma_test_user", description="Test database user")
    TEST_POSTGRES_PASSWORD: str = Field(default="test_password_secure", description="Test database password")
    
    # Test-specific connection pooling (smaller pools for tests)
    TEST_POOL_SIZE: int = Field(default=5, description="Test connection pool size")
    TEST_MAX_OVERFLOW: int = Field(default=10, description="Test max overflow connections")
    TEST_POOL_TIMEOUT: int = Field(default=10, description="Test pool timeout in seconds")
    TEST_POOL_RECYCLE: int = Field(default=300, description="Test connection recycle time in seconds")
    
    # Test isolation configuration
    USE_TRANSACTIONS: bool = Field(default=True, description="Use transactions for test isolation")
    AUTO_ROLLBACK: bool = Field(default=True, description="Automatically rollback test transactions")
    CLEAN_BETWEEN_TESTS: bool = Field(default=True, description="Clean data between tests")
    
    # Test data management
    TEST_DATA_RETENTION: int = Field(default=0, description="Hours to retain test data (0 = immediate cleanup)")
    PRESERVE_TEST_LOGS: bool = Field(default=False, description="Preserve test execution logs")
    
    # Service synchronization for tests
    SERVICE_STARTUP_TIMEOUT: int = Field(default=30, description="Service startup timeout in seconds")
    HEALTH_CHECK_INTERVAL: int = Field(default=1, description="Health check interval in seconds")
    HEALTH_CHECK_RETRIES: int = Field(default=10, description="Number of health check retries")
    
    # Test performance optimization
    PARALLEL_TEST_WORKERS: int = Field(default=4, description="Number of parallel test workers")
    TEST_TIMEOUT: int = Field(default=60, description="Individual test timeout in seconds")
    FAST_TEST_MODE: bool = Field(default=False, description="Enable fast test mode (reduced waits)")
    
    @property
    def test_database_url(self) -> str:
        """Generate test database URL for isolated testing."""
        if self.TESTING:
            return (
                f"postgresql://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@"
                f"{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"
            )
        else:
            # Fallback to base settings if not in test mode
            base_settings = BaseSettings()
            return base_settings.database_url
    
    @property
    def test_database_url_with_session(self) -> str:
        """Generate session-specific test database URL for maximum isolation."""
        if self.TESTING:
            session_db = f"{self.TEST_POSTGRES_DB}_{self.TEST_SESSION_ID}"
            return (
                f"postgresql://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@"
                f"{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{session_db}"
            )
        else:
            return self.test_database_url
    
    @property
    def test_engine_config(self) -> dict:
        """Get test-optimized SQLAlchemy engine configuration."""
        return {
            "pool_size": self.TEST_POOL_SIZE,
            "max_overflow": self.TEST_MAX_OVERFLOW,
            "pool_timeout": self.TEST_POOL_TIMEOUT,
            "pool_recycle": self.TEST_POOL_RECYCLE,
            "pool_pre_ping": True,
            "echo": False,  # Disable SQL logging in tests by default
            # Test-specific optimizations
            "connect_args": {
                "connect_timeout": 10,
                "application_name": f"apexsigma_test_{self.TEST_SESSION_ID}"
            }
        }
    
    class Config:
        env_file = ".env.test"
        env_prefix = "TEST_"
        extra = "ignore"


def get_test_settings() -> TestSettings:
    """
    Get test settings instance.
    
    This function automatically detects test environment and configures
    appropriate settings for test isolation.
    """
    # Auto-detect test environment
    is_testing = (
        os.getenv("TESTING", "").lower() in ("true", "1", "yes") or
        os.getenv("PYTEST_CURRENT_TEST") is not None or
        "pytest" in os.getenv("_", "") or
        "test" in os.getenv("_", "").lower()
    )
    
    settings = TestSettings(TESTING=is_testing)
    
    if is_testing:
        print(f"🧪 Test environment detected - Session ID: {settings.TEST_SESSION_ID}")
        print(f"   Test database: {settings.TEST_POSTGRES_DB}")
        print(f"   Connection pool: {settings.TEST_POOL_SIZE} base, {settings.TEST_MAX_OVERFLOW} overflow")
    
    return settings


def create_test_database_url(test_id: Optional[str] = None) -> str:
    """
    Create isolated test database URL.
    
    Args:
        test_id: Optional specific test identifier for maximum isolation
        
    Returns:
        Database URL for isolated test database
    """
    settings = get_test_settings()
    
    if test_id:
        # Create test-specific database name
        test_db = f"{settings.TEST_POSTGRES_DB}_{test_id}"
        return (
            f"postgresql://{settings.TEST_POSTGRES_USER}:{settings.TEST_POSTGRES_PASSWORD}@"
            f"{settings.TEST_POSTGRES_HOST}:{settings.TEST_POSTGRES_PORT}/{test_db}"
        )
    
    return settings.test_database_url


# For backward compatibility and easy import
test_settings = get_test_settings()
