"""
Test Database Manager for ApexSigma Ecosystem

Handles test database isolation, creation, cleanup, and transaction management
to eliminate flaky tests caused by database state interference.
"""

import asyncio
import contextlib
import logging
import time
from typing import Optional, Generator, AsyncGenerator, Dict, Any
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError, ProgrammingError

from .test_settings import get_test_settings, TestSettings

logger = logging.getLogger(__name__)


class TestDatabaseManager:
    """
    Manages test database lifecycle for isolated testing.
    
    Provides database creation, cleanup, transaction management,
    and test isolation to eliminate flaky tests.
    """
    
    def __init__(self, settings: Optional[TestSettings] = None):
        self.settings = settings or get_test_settings()
        self._admin_engine: Optional[Engine] = None
        self._test_engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        self._active_sessions: Dict[str, Session] = {}
        
    @property
    def admin_engine(self) -> Engine:
        """Get administrative engine for database management operations."""
        if self._admin_engine is None:
            # Connect to postgres database for administrative operations
            admin_url = (
                f"postgresql://{self.settings.TEST_POSTGRES_USER}:{self.settings.TEST_POSTGRES_PASSWORD}@"
                f"{self.settings.TEST_POSTGRES_HOST}:{self.settings.TEST_POSTGRES_PORT}/postgres"
            )
            self._admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
        return self._admin_engine
    
    @property
    def test_engine(self) -> Engine:
        """Get test database engine with optimized configuration."""
        if self._test_engine is None:
            self._test_engine = create_engine(
                self.settings.test_database_url,
                **self.settings.test_engine_config
            )
        return self._test_engine
    
    @property
    def session_factory(self) -> sessionmaker:
        """Get session factory for test database."""
        if self._session_factory is None:
            self._session_factory = sessionmaker(
                bind=self.test_engine,
                autocommit=False,
                autoflush=False
            )
        return self._session_factory
    
    def create_test_database(self, test_id: Optional[str] = None) -> str:
        """
        Create isolated test database.
        
        Args:
            test_id: Optional test identifier for maximum isolation
            
        Returns:
            Name of created test database
        """
        db_name = f"{self.settings.TEST_POSTGRES_DB}"
        if test_id:
            db_name = f"{db_name}_{test_id}"
            
        try:
            with self.admin_engine.connect() as conn:
                # Check if database exists
                result = conn.execute(
                    text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                    {"db_name": db_name}
                )
                
                if not result.fetchone():
                    # Create test database
                    conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                    logger.info(f"✅ Created test database: {db_name}")
                else:
                    logger.info(f"📁 Test database already exists: {db_name}")
                    
        except OperationalError as e:
            logger.warning(f"⚠️ Could not create test database {db_name}: {e}")
            # Continue with existing database
            
        return db_name
    
    def drop_test_database(self, test_id: Optional[str] = None) -> bool:
        """
        Drop test database for cleanup.
        
        Args:
            test_id: Optional test identifier
            
        Returns:
            True if database was dropped successfully
        """
        db_name = f"{self.settings.TEST_POSTGRES_DB}"
        if test_id:
            db_name = f"{db_name}_{test_id}"
            
        try:
            with self.admin_engine.connect() as conn:
                # Terminate active connections to the test database
                conn.execute(
                    text("""
                        SELECT pg_terminate_backend(pid)
                        FROM pg_stat_activity
                        WHERE datname = :db_name AND pid <> pg_backend_pid()
                    """),
                    {"db_name": db_name}
                )
                
                # Drop the database
                conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}"'))
                logger.info(f"🗑️ Dropped test database: {db_name}")
                return True
                
        except (OperationalError, ProgrammingError) as e:
            logger.warning(f"⚠️ Could not drop test database {db_name}: {e}")
            return False
    
    def clean_test_data(self, preserve_schema: bool = True) -> bool:
        """
        Clean test data while preserving schema structure.
        
        Args:
            preserve_schema: If True, only delete data, keep tables
            
        Returns:
            True if cleanup was successful
        """
        try:
            with self.test_engine.connect() as conn:
                if preserve_schema:
                    # Get all table names
                    metadata = MetaData()
                    metadata.reflect(bind=conn)
                    
                    # Delete data from all tables
                    with conn.begin():
                        for table in reversed(metadata.sorted_tables):
                            conn.execute(table.delete())
                    
                    logger.info(f"🧹 Cleaned test data from {len(metadata.tables)} tables")
                else:
                    # Drop all tables
                    metadata = MetaData()
                    metadata.reflect(bind=conn)
                    metadata.drop_all(bind=conn)
                    
                    logger.info(f"🗑️ Dropped all test tables")
                    
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to clean test data: {e}")
            return False
    
    @contextlib.contextmanager
    def isolated_session(self, test_id: Optional[str] = None) -> Generator[Session, None, None]:
        """
        Context manager for isolated test sessions with automatic cleanup.
        
        Args:
            test_id: Optional test identifier for session tracking
            
        Yields:
            SQLAlchemy session with automatic transaction management
        """
        session_id = test_id or f"test_{int(time.time())}"
        session = self.session_factory()
        self._active_sessions[session_id] = session
        
        try:
            if self.settings.USE_TRANSACTIONS:
                # Start transaction for isolation
                session.begin()
                
            yield session
            
            if self.settings.USE_TRANSACTIONS and self.settings.AUTO_ROLLBACK:
                # Rollback transaction for cleanup
                session.rollback()
                logger.debug(f"🔄 Rolled back test transaction for {session_id}")
            else:
                # Commit if not using auto-rollback
                session.commit()
                
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Test session error for {session_id}: {e}")
            raise
        finally:
            session.close()
            self._active_sessions.pop(session_id, None)
            logger.debug(f"🔒 Closed test session: {session_id}")
    
    def wait_for_database_ready(self, timeout: int = 30) -> bool:
        """
        Wait for test database to be ready for connections.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if database is ready, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                with self.test_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                logger.info(f"✅ Test database ready")
                return True
                
            except OperationalError:
                time.sleep(self.settings.HEALTH_CHECK_INTERVAL)
                continue
                
        logger.error(f"❌ Test database not ready after {timeout}s timeout")
        return False
    
    def cleanup_all_test_databases(self, pattern: str = "apexsigma_test_") -> int:
        """
        Cleanup all test databases matching pattern.
        
        Args:
            pattern: Database name pattern to match for cleanup
            
        Returns:
            Number of databases cleaned up
        """
        cleaned_count = 0
        
        try:
            with self.admin_engine.connect() as conn:
                # Find all test databases
                result = conn.execute(
                    text("SELECT datname FROM pg_database WHERE datname LIKE :pattern"),
                    {"pattern": f"{pattern}%"}
                )
                
                test_databases = [row[0] for row in result.fetchall()]
                
                for db_name in test_databases:
                    if self.drop_test_database(db_name.split("_")[-1]):
                        cleaned_count += 1
                        
                logger.info(f"🧹 Cleaned up {cleaned_count} test databases")
                
        except Exception as e:
            logger.error(f"❌ Failed to cleanup test databases: {e}")
            
        return cleaned_count
    
    def close(self):
        """Close all database connections and cleanup resources."""
        # Close active sessions
        for session_id, session in self._active_sessions.items():
            try:
                session.close()
                logger.debug(f"🔒 Closed active session: {session_id}")
            except Exception as e:
                logger.warning(f"⚠️ Error closing session {session_id}: {e}")
        
        self._active_sessions.clear()
        
        # Close engines
        if self._test_engine:
            self._test_engine.dispose()
            self._test_engine = None
            
        if self._admin_engine:
            self._admin_engine.dispose()
            self._admin_engine = None
            
        logger.info("🔒 Test database manager closed")


# Global test database manager instance
_test_db_manager: Optional[TestDatabaseManager] = None


def get_test_db_manager() -> TestDatabaseManager:
    """Get global test database manager instance."""
    global _test_db_manager
    if _test_db_manager is None:
        _test_db_manager = TestDatabaseManager()
    return _test_db_manager


def cleanup_test_environment():
    """Cleanup test environment and close all connections."""
    global _test_db_manager
    if _test_db_manager:
        _test_db_manager.cleanup_all_test_databases()
        _test_db_manager.close()
        _test_db_manager = None


# Context managers for easy test usage
@contextlib.contextmanager
def test_database_session(test_id: Optional[str] = None) -> Generator[Session, None, None]:
    """
    Convenient context manager for test database sessions.
    
    Args:
        test_id: Optional test identifier
        
    Yields:
        Isolated database session with automatic cleanup
    """
    manager = get_test_db_manager()
    with manager.isolated_session(test_id) as session:
        yield session


@contextlib.contextmanager
def isolated_test_database(test_id: Optional[str] = None) -> Generator[str, None, None]:
    """
    Context manager for completely isolated test database.
    
    Args:
        test_id: Optional test identifier
        
    Yields:
        Test database name with automatic cleanup
    """
    manager = get_test_db_manager()
    db_name = manager.create_test_database(test_id)
    
    try:
        # Wait for database to be ready
        if manager.wait_for_database_ready():
            yield db_name
        else:
            raise RuntimeError(f"Test database {db_name} not ready")
    finally:
        # Cleanup database
        manager.drop_test_database(test_id)
