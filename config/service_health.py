"""
Service Health Check and Synchronization for Test Environments

Provides health check utilities and service synchronization patterns
to ensure reliable test execution across the ApexSigma ecosystem.
"""

import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import requests

from .test_settings import get_test_settings

logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Service status enumeration."""

    UNKNOWN = "unknown"
    STARTING = "starting"
    READY = "ready"
    DEGRADED = "degraded"
    FAILED = "failed"


@dataclass
class HealthCheckResult:
    """Result of a service health check."""

    service_name: str
    status: ServiceStatus
    response_time: float
    details: Dict[str, Any]
    timestamp: float
    error: Optional[str] = None


@dataclass
class ServiceConfig:
    """Configuration for a service health check."""

    name: str
    health_url: str
    port: int
    timeout: int = 10
    expected_status_code: int = 200
    required_dependencies: List[str] = None

    def __post_init__(self):
        if self.required_dependencies is None:
            self.required_dependencies = []


class ServiceHealthChecker:
    """Manages health checks for ApexSigma services."""

    def __init__(self):
        self.settings = get_test_settings()
        self.services = self._get_service_configs()
        self._health_cache: Dict[str, HealthCheckResult] = {}
        self._cache_ttl = 5  # Cache results for 5 seconds

    def _get_service_configs(self) -> Dict[str, ServiceConfig]:
        """Get service configurations for health checks."""
        return {
            "postgres": ServiceConfig(
                name="postgres",
                health_url="postgresql://connection_test",
                port=5432,
                timeout=5,
            ),
            "redis": ServiceConfig(
                name="redis", health_url="redis://ping", port=6379, timeout=5
            ),
            "memos": ServiceConfig(
                name="memos.as",
                health_url="http://localhost:8090/health",
                port=8090,
                required_dependencies=["postgres", "redis"],
            ),
            "tools": ServiceConfig(
                name="tools.as",
                health_url="http://localhost:8000/health",
                port=8000,
                required_dependencies=["postgres"],
            ),
            "devenviro": ServiceConfig(
                name="devenviro.as",
                health_url="http://localhost:8000/health",
                port=8000,
                required_dependencies=["postgres"],
            ),
            "ingest": ServiceConfig(
                name="InGest-LLM.as",
                health_url="http://localhost:8000/health",
                port=8000,
                required_dependencies=["postgres", "redis"],
            ),
        }

    def check_service_health(self, service_name: str) -> HealthCheckResult:
        """
        Check health of a specific service.

        Args:
            service_name: Name of the service to check

        Returns:
            HealthCheckResult with service status information
        """
        # Check cache first
        if service_name in self._health_cache:
            cached_result = self._health_cache[service_name]
            if time.time() - cached_result.timestamp < self._cache_ttl:
                return cached_result

        service_config = self.services.get(service_name)
        if not service_config:
            return HealthCheckResult(
                service_name=service_name,
                status=ServiceStatus.UNKNOWN,
                response_time=0.0,
                details={"error": "Unknown service"},
                timestamp=time.time(),
                error="Service not configured",
            )

        start_time = time.time()

        try:
            if service_name == "postgres":
                result = self._check_postgres_health(service_config)
            elif service_name == "redis":
                result = self._check_redis_health(service_config)
            else:
                result = self._check_http_health(service_config)

            result.response_time = time.time() - start_time

        except Exception as e:
            result = HealthCheckResult(
                service_name=service_name,
                status=ServiceStatus.FAILED,
                response_time=time.time() - start_time,
                details={"error": str(e)},
                timestamp=time.time(),
                error=str(e),
            )

        # Cache result
        self._health_cache[service_name] = result
        return result

    def _check_postgres_health(self, config: ServiceConfig) -> HealthCheckResult:
        """Check PostgreSQL database health."""
        try:
            from sqlalchemy import create_engine, text

            # Use test database URL for health check
            engine = create_engine(
                self.settings.test_database_url,
                pool_timeout=config.timeout,
                pool_pre_ping=True,
            )

            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()

            engine.dispose()

            return HealthCheckResult(
                service_name=config.name,
                status=ServiceStatus.READY,
                response_time=0.0,
                details={"connection": "successful"},
                timestamp=time.time(),
            )

        except Exception as e:
            return HealthCheckResult(
                service_name=config.name,
                status=ServiceStatus.FAILED,
                response_time=0.0,
                details={"connection": "failed", "error": str(e)},
                timestamp=time.time(),
                error=str(e),
            )

    def _check_redis_health(self, config: ServiceConfig) -> HealthCheckResult:
        """Check Redis health."""
        try:
            import redis

            client = redis.Redis(
                host=(
                    self.settings.REDIS_HOST
                    if hasattr(self.settings, "REDIS_HOST")
                    else "localhost"
                ),
                port=6379,
                socket_timeout=config.timeout,
                socket_connect_timeout=config.timeout,
            )

            # Simple ping test
            client.ping()
            client.close()

            return HealthCheckResult(
                service_name=config.name,
                status=ServiceStatus.READY,
                response_time=0.0,
                details={"ping": "successful"},
                timestamp=time.time(),
            )

        except Exception as e:
            return HealthCheckResult(
                service_name=config.name,
                status=ServiceStatus.FAILED,
                response_time=0.0,
                details={"ping": "failed", "error": str(e)},
                timestamp=time.time(),
                error=str(e),
            )

    def _check_http_health(self, config: ServiceConfig) -> HealthCheckResult:
        """Check HTTP service health."""
        try:
            response = requests.get(
                config.health_url,
                timeout=config.timeout,
                headers={"Accept": "application/json"},
            )

            if response.status_code == config.expected_status_code:
                status = ServiceStatus.READY
            else:
                status = ServiceStatus.DEGRADED

            details = {
                "status_code": response.status_code,
                "response_size": len(response.content),
            }

            # Try to parse JSON response for additional details
            try:
                details.update(response.json())
            except:
                details["response_text"] = response.text[:200]

            return HealthCheckResult(
                service_name=config.name,
                status=status,
                response_time=0.0,
                details=details,
                timestamp=time.time(),
            )

        except requests.exceptions.ConnectionError:
            return HealthCheckResult(
                service_name=config.name,
                status=ServiceStatus.FAILED,
                response_time=0.0,
                details={"connection": "refused"},
                timestamp=time.time(),
                error="Connection refused",
            )
        except requests.exceptions.Timeout:
            return HealthCheckResult(
                service_name=config.name,
                status=ServiceStatus.FAILED,
                response_time=0.0,
                details={"timeout": config.timeout},
                timestamp=time.time(),
                error="Request timeout",
            )
        except Exception as e:
            return HealthCheckResult(
                service_name=config.name,
                status=ServiceStatus.FAILED,
                response_time=0.0,
                details={"error": str(e)},
                timestamp=time.time(),
                error=str(e),
            )

    def check_all_services(self) -> Dict[str, HealthCheckResult]:
        """Check health of all configured services."""
        results = {}

        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_service = {
                executor.submit(self.check_service_health, service_name): service_name
                for service_name in self.services.keys()
            }

            for future in future_to_service:
                service_name = future_to_service[future]
                try:
                    result = future.result(timeout=30)
                    results[service_name] = result
                except FutureTimeoutError:
                    results[service_name] = HealthCheckResult(
                        service_name=service_name,
                        status=ServiceStatus.FAILED,
                        response_time=30.0,
                        details={"error": "Health check timeout"},
                        timestamp=time.time(),
                        error="Timeout",
                    )
                except Exception as e:
                    results[service_name] = HealthCheckResult(
                        service_name=service_name,
                        status=ServiceStatus.FAILED,
                        response_time=0.0,
                        details={"error": str(e)},
                        timestamp=time.time(),
                        error=str(e),
                    )

        return results

    def wait_for_service_ready(self, service_name: str, timeout: int = None) -> bool:
        """
        Wait for a service to be ready.

        Args:
            service_name: Name of the service to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            True if service becomes ready, False if timeout
        """
        timeout = timeout or self.settings.SERVICE_STARTUP_TIMEOUT
        start_time = time.time()

        while time.time() - start_time < timeout:
            result = self.check_service_health(service_name)

            if result.status == ServiceStatus.READY:
                logger.info(f"✅ {service_name} is ready")
                return True
            elif result.status == ServiceStatus.FAILED:
                logger.warning(f"⚠️ {service_name} health check failed: {result.error}")

            time.sleep(self.settings.HEALTH_CHECK_INTERVAL)

        logger.error(f"❌ {service_name} not ready after {timeout}s timeout")
        return False

    def wait_for_services_ready(
        self, service_names: List[str], timeout: int = None
    ) -> Dict[str, bool]:
        """
        Wait for multiple services to be ready.

        Args:
            service_names: List of service names to wait for
            timeout: Maximum time to wait for each service

        Returns:
            Dictionary mapping service names to ready status
        """
        results = {}

        for service_name in service_names:
            results[service_name] = self.wait_for_service_ready(service_name, timeout)

        return results


class TestSynchronizer:
    """Synchronization utilities for coordinated test execution."""

    def __init__(self):
        self.settings = get_test_settings()
        self.health_checker = ServiceHealthChecker()
        self._barriers: Dict[str, asyncio.Barrier] = {}

    def ensure_test_prerequisites(self, required_services: List[str] = None) -> bool:
        """
        Ensure all test prerequisites are met.

        Args:
            required_services: List of services that must be ready

        Returns:
            True if all prerequisites are met
        """
        required_services = required_services or ["postgres"]

        logger.info(f"🔍 Checking test prerequisites: {required_services}")

        # Check service health
        results = self.health_checker.wait_for_services_ready(required_services)

        if not all(results.values()):
            failed_services = [name for name, ready in results.items() if not ready]
            logger.error(
                f"❌ Test prerequisites not met. Failed services: {failed_services}"
            )
            return False

        logger.info("✅ All test prerequisites met")
        return True

    async def coordinate_test_execution(
        self, test_groups: List[List[str]], max_concurrent: int = None
    ) -> Dict[str, Any]:
        """
        Coordinate execution of test groups with proper synchronization.

        Args:
            test_groups: List of test groups to execute in sequence
            max_concurrent: Maximum concurrent tests per group

        Returns:
            Execution results and timing information
        """
        max_concurrent = max_concurrent or self.settings.PARALLEL_TEST_WORKERS
        results = {"groups": [], "total_time": 0, "success": True}

        start_time = time.time()

        for group_idx, test_group in enumerate(test_groups):
            group_start = time.time()
            logger.info(f"🚀 Executing test group {group_idx + 1}: {test_group}")

            # Create semaphore for concurrency control
            semaphore = asyncio.Semaphore(min(max_concurrent, len(test_group)))

            async def run_test(test_name: str) -> Dict[str, Any]:
                async with semaphore:
                    # Simulate test execution
                    test_start = time.time()
                    await asyncio.sleep(0.1)  # Simulate test work
                    test_duration = time.time() - test_start

                    return {
                        "test_name": test_name,
                        "duration": test_duration,
                        "success": True,
                    }

            # Execute tests in group concurrently
            group_tasks = [run_test(test_name) for test_name in test_group]
            group_results = await asyncio.gather(*group_tasks, return_exceptions=True)

            group_duration = time.time() - group_start
            group_success = all(
                isinstance(result, dict) and result.get("success", False)
                for result in group_results
            )

            results["groups"].append(
                {
                    "group_index": group_idx,
                    "tests": test_group,
                    "results": group_results,
                    "duration": group_duration,
                    "success": group_success,
                }
            )

            if not group_success:
                results["success"] = False
                logger.error(f"❌ Test group {group_idx + 1} failed")
            else:
                logger.info(
                    f"✅ Test group {group_idx + 1} completed in {group_duration:.2f}s"
                )

        results["total_time"] = time.time() - start_time
        return results

    def create_test_barrier(self, barrier_name: str, parties: int) -> asyncio.Barrier:
        """
        Create a named barrier for test synchronization.

        Args:
            barrier_name: Name of the barrier
            parties: Number of parties that must reach the barrier

        Returns:
            Asyncio barrier for synchronization
        """
        barrier = asyncio.Barrier(parties)
        self._barriers[barrier_name] = barrier
        logger.debug(f"🚧 Created test barrier '{barrier_name}' for {parties} parties")
        return barrier

    def get_test_barrier(self, barrier_name: str) -> Optional[asyncio.Barrier]:
        """Get existing test barrier by name."""
        return self._barriers.get(barrier_name)


# Global instances
_health_checker: Optional[ServiceHealthChecker] = None
_test_synchronizer: Optional[TestSynchronizer] = None


def get_health_checker() -> ServiceHealthChecker:
    """Get global service health checker instance."""
    global _health_checker
    if _health_checker is None:
        _health_checker = ServiceHealthChecker()
    return _health_checker


def get_test_synchronizer() -> TestSynchronizer:
    """Get global test synchronizer instance."""
    global _test_synchronizer
    if _test_synchronizer is None:
        _test_synchronizer = TestSynchronizer()
    return _test_synchronizer


# Convenience functions for common operations
def ensure_database_ready(timeout: int = 30) -> bool:
    """Ensure test database is ready for use."""
    return get_health_checker().wait_for_service_ready("postgres", timeout)


def ensure_services_ready(services: List[str], timeout: int = 30) -> bool:
    """Ensure specified services are ready for testing."""
    results = get_health_checker().wait_for_services_ready(services, timeout)
    return all(results.values())


async def wait_for_test_sync(barrier_name: str, timeout: int = 60) -> bool:
    """Wait for test synchronization barrier."""
    synchronizer = get_test_synchronizer()
    barrier = synchronizer.get_test_barrier(barrier_name)

    if not barrier:
        logger.warning(f"⚠️ Test barrier '{barrier_name}' not found")
        return False

    try:
        await asyncio.wait_for(barrier.wait(), timeout=timeout)
        logger.debug(f"🔓 Test barrier '{barrier_name}' released")
        return True
    except asyncio.TimeoutError:
        logger.error(f"❌ Test barrier '{barrier_name}' timeout after {timeout}s")
        return False
