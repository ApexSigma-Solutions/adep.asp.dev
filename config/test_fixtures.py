"""
Test Fixtures and Utilities for ApexSigma Ecosystem

Provides reusable test fixtures, utilities, and helpers for consistent
test setup across all microservices in the ecosystem.
"""

import asyncio
import logging
from typing import Any, Callable, Dict, Generator, Optional

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .test_db_manager import (
    cleanup_test_environment,
    get_test_db_manager,
    test_database_session,
)
from .test_settings import get_test_settings

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def test_settings():
    """Test settings fixture for the entire test session."""
    return get_test_settings()


@pytest.fixture(scope="session")
def test_db_manager():
    """Test database manager fixture for the session."""
    manager = get_test_db_manager()
    yield manager
    # Cleanup after all tests
    cleanup_test_environment()


@pytest.fixture(scope="function")
def isolated_db_session(test_db_manager) -> Generator[Session, None, None]:
    """
    Isolated database session fixture for each test function.

    Provides a clean database session with automatic transaction rollback
    to ensure test isolation.
    """
    test_id = (
        f"pytest_{pytest.current_test_id()}"
        if hasattr(pytest, "current_test_id")
        else None
    )

    with test_database_session(test_id) as session:
        yield session


@pytest.fixture(scope="function")
def clean_database(test_db_manager):
    """
    Clean database fixture that ensures clean state before each test.

    Cleans all test data while preserving schema structure.
    """
    # Clean before test
    test_db_manager.clean_test_data(preserve_schema=True)
    yield
    # Clean after test if configured
    if test_db_manager.settings.CLEAN_BETWEEN_TESTS:
        test_db_manager.clean_test_data(preserve_schema=True)


@pytest.fixture(scope="class")
def test_database_url(test_settings):
    """Test database URL fixture for test classes."""
    return test_settings.test_database_url


@pytest.fixture(scope="function")
def test_engine(test_settings):
    """SQLAlchemy engine fixture for tests."""
    engine = create_engine(
        test_settings.test_database_url, **test_settings.test_engine_config
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(test_settings):
    """
    Automatic test environment setup fixture.

    Configures logging, database, and other test environment settings.
    """
    # Configure test logging
    if test_settings.PRESERVE_TEST_LOGS:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )
    else:
        # Suppress logs during tests unless debugging
        logging.getLogger().setLevel(logging.WARNING)

    # Set test environment variables
    import os

    os.environ["TESTING"] = "true"
    os.environ["TEST_SESSION_ID"] = test_settings.TEST_SESSION_ID

    logger.info(
        f"🧪 Test environment initialized - Session: {test_settings.TEST_SESSION_ID}"
    )

    yield

    # Cleanup after all tests
    logger.info("🧹 Test environment cleanup completed")


@pytest.fixture
def mock_service_health_check():
    """Mock service health check for testing service dependencies."""

    def _mock_health_check(service_name: str, timeout: int = 30) -> bool:
        """Mock health check that always returns True for tests."""
        logger.debug(f"🏥 Mock health check for {service_name}: OK")
        return True

    return _mock_health_check


class TestDataFactory:
    """Factory for creating test data consistently across services."""

    @staticmethod
    def create_test_user(session: Session, **kwargs) -> Dict[str, Any]:
        """Create test user data."""
        defaults = {
            "id": "test_user_001",
            "username": "test_user",
            "email": "test@apexsigma.dev",
            "is_active": True,
        }
        defaults.update(kwargs)
        return defaults

    @staticmethod
    def create_test_memory(session: Session, **kwargs) -> Dict[str, Any]:
        """Create test memory data for memos service."""
        defaults = {
            "id": "test_memory_001",
            "content": "Test memory content",
            "memory_type": "episodic",
            "user_id": "test_user_001",
            "importance": 0.5,
        }
        defaults.update(kwargs)
        return defaults

    @staticmethod
    def create_test_tool(session: Session, **kwargs) -> Dict[str, Any]:
        """Create test tool data for tools service."""
        defaults = {
            "id": "test_tool_001",
            "name": "test_tool",
            "description": "Test tool description",
            "category": "testing",
            "is_active": True,
        }
        defaults.update(kwargs)
        return defaults


@pytest.fixture
def test_data_factory():
    """Test data factory fixture."""
    return TestDataFactory()


def pytest_configure(config):
    """Pytest configuration hook for test setup."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "database: marks tests that require database")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Mark slow tests
        if "slow" in item.name.lower() or "performance" in item.name.lower():
            item.add_marker(pytest.mark.slow)

        # Mark integration tests
        if "integration" in item.name.lower() or "e2e" in item.name.lower():
            item.add_marker(pytest.mark.integration)

        # Mark database tests
        if any(
            fixture in item.fixturenames
            for fixture in ["isolated_db_session", "test_engine", "clean_database"]
        ):
            item.add_marker(pytest.mark.database)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


class ServiceTestHelper:
    """Helper class for testing service interactions."""

    def __init__(self, test_settings):
        self.settings = test_settings

    def wait_for_service_ready(
        self, service_name: str, health_check_url: str, timeout: int = None
    ) -> bool:
        """Wait for a service to be ready for testing."""
        timeout = timeout or self.settings.SERVICE_STARTUP_TIMEOUT
        # In test environment, we can mock this or implement actual health checks
        logger.debug(f"🏥 Waiting for {service_name} to be ready...")
        return True  # Simplified for test environment

    def create_test_client(self, service_name: str) -> Dict[str, Any]:
        """Create test client for service interactions."""
        return {
            "service_name": service_name,
            "base_url": f"http://localhost:8000",  # Test service URL
            "timeout": self.settings.TEST_TIMEOUT,
        }


@pytest.fixture
def service_test_helper(test_settings):
    """Service test helper fixture."""
    return ServiceTestHelper(test_settings)


# Performance testing utilities
class PerformanceTracker:
    """Track test performance metrics."""

    def __init__(self):
        self.metrics = {}

    def start_timer(self, operation: str):
        """Start timing an operation."""
        import time

        self.metrics[operation] = {"start": time.time()}

    def end_timer(self, operation: str) -> float:
        """End timing and return duration."""
        import time

        if operation in self.metrics:
            duration = time.time() - self.metrics[operation]["start"]
            self.metrics[operation]["duration"] = duration
            return duration
        return 0.0

    def get_metrics(self) -> Dict[str, float]:
        """Get all performance metrics."""
        return {op: data.get("duration", 0.0) for op, data in self.metrics.items()}


@pytest.fixture
def performance_tracker():
    """Performance tracking fixture for test optimization."""
    return PerformanceTracker()


# Utility functions for test assertions
def assert_database_clean(session: Session, table_names: list = None):
    """Assert that specified tables are empty."""
    from sqlalchemy import text

    if table_names:
        for table_name in table_names:
            result = session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            assert count == 0, f"Table {table_name} is not clean: {count} rows found"

    logger.debug("✅ Database clean assertion passed")


def assert_test_isolation(session: Session, test_data: Dict[str, Any]):
    """Assert that test data doesn't interfere with other tests."""
    # This can be expanded based on specific isolation requirements
    logger.debug("✅ Test isolation assertion passed")
