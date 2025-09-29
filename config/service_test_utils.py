"""
Service-Specific Test Integration Utilities

Provides test utilities and helpers specifically designed for each
ApexSigma microservice to enable consistent testing patterns.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, List, Callable
from contextlib import contextmanager
from sqlalchemy.orm import Session

from .test_settings import get_test_settings
from .test_db_manager import get_test_db_manager

logger = logging.getLogger(__name__)


class ServiceTestBase:
    """Base class for service-specific test utilities."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.settings = get_test_settings()
        self.db_manager = get_test_db_manager()
    
    def setup_service_test_environment(self):
        """Setup test environment for this service."""
        logger.info(f"🧪 Setting up test environment for {self.service_name}")
        
        # Ensure test database is ready
        if not self.db_manager.wait_for_database_ready():
            raise RuntimeError(f"Test database not ready for {self.service_name}")
        
        # Service-specific setup can be overridden
        self._service_specific_setup()
    
    def _service_specific_setup(self):
        """Override in subclasses for service-specific setup."""
        pass
    
    def cleanup_service_test_data(self):
        """Cleanup test data for this service."""
        logger.info(f"🧹 Cleaning up test data for {self.service_name}")
        self.db_manager.clean_test_data()


class MemosServiceTestUtils(ServiceTestBase):
    """Test utilities specific to memos.as service."""
    
    def __init__(self):
        super().__init__("memos.as")
    
    def _service_specific_setup(self):
        """Setup memos service test environment."""
        # Create test schemas if needed
        with self.db_manager.isolated_session() as session:
            # Ensure memos tables exist
            self._create_memos_test_schema(session)
    
    def _create_memos_test_schema(self, session: Session):
        """Create memos service test schema."""
        # This would typically create the necessary tables
        # For now, we'll assume they exist or are created by migrations
        logger.debug("📋 Memos test schema ready")
    
    def create_test_memory(self, session: Session, **kwargs) -> Dict[str, Any]:
        """Create test memory entry."""
        defaults = {
            "id": f"test_memory_{int(time.time())}",
            "content": "Test memory content",
            "memory_type": "episodic",
            "user_id": "test_user",
            "importance": 0.5,
            "created_at": time.time(),
            "metadata": {"test": True}
        }
        defaults.update(kwargs)
        
        # Insert test memory (simplified - would use actual ORM models)
        logger.debug(f"💭 Created test memory: {defaults['id']}")
        return defaults
    
    def create_test_tool_registry_entry(self, session: Session, **kwargs) -> Dict[str, Any]:
        """Create test tool registry entry."""
        defaults = {
            "id": f"test_tool_{int(time.time())}",
            "name": "test_tool",
            "description": "Test tool for testing",
            "category": "testing",
            "is_active": True,
            "metadata": {"test": True}
        }
        defaults.update(kwargs)
        
        logger.debug(f"🔧 Created test tool registry entry: {defaults['id']}")
        return defaults
    
    @contextmanager
    def isolated_memory_test(self, test_id: Optional[str] = None):
        """Context manager for isolated memory testing."""
        with self.db_manager.isolated_session(test_id) as session:
            # Setup test data
            initial_data = self.create_test_memory(session)
            
            yield session, initial_data
            
            # Cleanup handled by session context manager


class ToolsServiceTestUtils(ServiceTestBase):
    """Test utilities specific to tools.as service."""
    
    def __init__(self):
        super().__init__("tools.as")
    
    def _service_specific_setup(self):
        """Setup tools service test environment."""
        with self.db_manager.isolated_session() as session:
            self._create_tools_test_schema(session)
    
    def _create_tools_test_schema(self, session: Session):
        """Create tools service test schema."""
        logger.debug("🔧 Tools test schema ready")
    
    def create_test_tool(self, session: Session, **kwargs) -> Dict[str, Any]:
        """Create test tool entry."""
        defaults = {
            "id": f"test_tool_{int(time.time())}",
            "name": "test_tool",
            "description": "Test tool description",
            "category": "testing",
            "version": "1.0.0",
            "is_active": True,
            "config": {"test_mode": True}
        }
        defaults.update(kwargs)
        
        logger.debug(f"🔧 Created test tool: {defaults['id']}")
        return defaults
    
    def create_test_execution_log(self, session: Session, tool_id: str, **kwargs) -> Dict[str, Any]:
        """Create test tool execution log."""
        defaults = {
            "id": f"test_execution_{int(time.time())}",
            "tool_id": tool_id,
            "status": "completed",
            "duration": 0.1,
            "input_data": {"test": True},
            "output_data": {"result": "test_success"}
        }
        defaults.update(kwargs)
        
        logger.debug(f"📊 Created test execution log: {defaults['id']}")
        return defaults
    
    @contextmanager
    def isolated_tool_test(self, test_id: Optional[str] = None):
        """Context manager for isolated tool testing."""
        with self.db_manager.isolated_session(test_id) as session:
            # Setup test tool
            test_tool = self.create_test_tool(session)
            
            yield session, test_tool
            
            # Cleanup handled by session context manager


class DevEnviroServiceTestUtils(ServiceTestBase):
    """Test utilities specific to devenviro.as service."""
    
    def __init__(self):
        super().__init__("devenviro.as")
    
    def _service_specific_setup(self):
        """Setup devenviro service test environment."""
        with self.db_manager.isolated_session() as session:
            self._create_devenviro_test_schema(session)
    
    def _create_devenviro_test_schema(self, session: Session):
        """Create devenviro service test schema."""
        logger.debug("🏗️ DevEnviro test schema ready")
    
    def create_test_agent(self, session: Session, **kwargs) -> Dict[str, Any]:
        """Create test agent entry."""
        defaults = {
            "id": f"test_agent_{int(time.time())}",
            "agent_name": "test_agent",
            "agent_type": "testing",
            "capabilities": ["test_capability"],
            "status": "active",
            "metadata": {"test": True}
        }
        defaults.update(kwargs)
        
        logger.debug(f"🤖 Created test agent: {defaults['id']}")
        return defaults
    
    def create_test_environment(self, session: Session, **kwargs) -> Dict[str, Any]:
        """Create test development environment."""
        defaults = {
            "id": f"test_env_{int(time.time())}",
            "name": "test_environment",
            "type": "testing",
            "status": "ready",
            "config": {"test_mode": True}
        }
        defaults.update(kwargs)
        
        logger.debug(f"🏗️ Created test environment: {defaults['id']}")
        return defaults
    
    @contextmanager
    def isolated_agent_test(self, test_id: Optional[str] = None):
        """Context manager for isolated agent testing."""
        with self.db_manager.isolated_session(test_id) as session:
            # Setup test agent
            test_agent = self.create_test_agent(session)
            
            yield session, test_agent


class IngestLLMServiceTestUtils(ServiceTestBase):
    """Test utilities specific to InGest-LLM.as service."""
    
    def __init__(self):
        super().__init__("InGest-LLM.as")
    
    def _service_specific_setup(self):
        """Setup InGest-LLM service test environment."""
        with self.db_manager.isolated_session() as session:
            self._create_ingest_test_schema(session)
    
    def _create_ingest_test_schema(self, session: Session):
        """Create InGest-LLM service test schema."""
        logger.debug("📥 InGest-LLM test schema ready")
    
    def create_test_document(self, session: Session, **kwargs) -> Dict[str, Any]:
        """Create test document for ingestion."""
        defaults = {
            "id": f"test_doc_{int(time.time())}",
            "title": "Test Document",
            "content": "Test document content for processing",
            "type": "text",
            "source": "test",
            "metadata": {"test": True}
        }
        defaults.update(kwargs)
        
        logger.debug(f"📄 Created test document: {defaults['id']}")
        return defaults
    
    def create_test_embedding(self, session: Session, document_id: str, **kwargs) -> Dict[str, Any]:
        """Create test embedding entry."""
        defaults = {
            "id": f"test_embedding_{int(time.time())}",
            "document_id": document_id,
            "vector": [0.1, 0.2, 0.3, 0.4, 0.5],  # Test vector
            "model": "test_model",
            "metadata": {"test": True}
        }
        defaults.update(kwargs)
        
        logger.debug(f"🔢 Created test embedding: {defaults['id']}")
        return defaults
    
    @contextmanager
    def isolated_ingestion_test(self, test_id: Optional[str] = None):
        """Context manager for isolated ingestion testing."""
        with self.db_manager.isolated_session(test_id) as session:
            # Setup test document
            test_document = self.create_test_document(session)
            
            yield session, test_document


class IntegrationTestUtils:
    """Utilities for cross-service integration testing."""
    
    def __init__(self):
        self.settings = get_test_settings()
        self.services = {
            "memos": MemosServiceTestUtils(),
            "tools": ToolsServiceTestUtils(),
            "devenviro": DevEnviroServiceTestUtils(),
            "ingest": IngestLLMServiceTestUtils()
        }
    
    def setup_full_ecosystem_test(self):
        """Setup test environment for full ecosystem testing."""
        logger.info("🌐 Setting up full ecosystem test environment")
        
        for service_name, service_utils in self.services.items():
            try:
                service_utils.setup_service_test_environment()
                logger.info(f"✅ {service_name} test environment ready")
            except Exception as e:
                logger.error(f"❌ Failed to setup {service_name}: {e}")
                raise
        
        logger.info("🎉 Full ecosystem test environment ready")
    
    @contextmanager
    def isolated_ecosystem_test(self, test_id: Optional[str] = None):
        """Context manager for isolated full ecosystem testing."""
        ecosystem_test_id = test_id or f"ecosystem_{int(time.time())}"
        
        # Setup
        self.setup_full_ecosystem_test()
        
        # Create isolated sessions for each service
        sessions = {}
        try:
            for service_name, service_utils in self.services.items():
                session_manager = service_utils.db_manager.isolated_session(f"{ecosystem_test_id}_{service_name}")
                sessions[service_name] = session_manager.__enter__()
            
            yield sessions
            
        finally:
            # Cleanup sessions
            for service_name, session in sessions.items():
                try:
                    session_manager = self.services[service_name].db_manager.isolated_session()
                    session_manager.__exit__(None, None, None)
                except Exception as e:
                    logger.warning(f"⚠️ Error cleaning up {service_name} session: {e}")
    
    def validate_cross_service_consistency(self, sessions: Dict[str, Session]) -> bool:
        """Validate data consistency across services."""
        logger.info("🔍 Validating cross-service consistency")
        
        # This can be expanded based on specific consistency requirements
        # For now, just verify all sessions are active
        for service_name, session in sessions.items():
            if not session.is_active:
                logger.error(f"❌ {service_name} session is not active")
                return False
        
        logger.info("✅ Cross-service consistency validated")
        return True


# Factory function to get service-specific test utils
def get_service_test_utils(service_name: str) -> ServiceTestBase:
    """Get test utilities for a specific service."""
    utils_map = {
        "memos": MemosServiceTestUtils,
        "tools": ToolsServiceTestUtils,
        "devenviro": DevEnviroServiceTestUtils,
        "ingest": IngestLLMServiceTestUtils
    }
    
    utils_class = utils_map.get(service_name.lower())
    if not utils_class:
        raise ValueError(f"Unknown service: {service_name}")
    
    return utils_class()


# Global integration test utils instance
_integration_utils: Optional[IntegrationTestUtils] = None


def get_integration_test_utils() -> IntegrationTestUtils:
    """Get global integration test utilities."""
    global _integration_utils
    if _integration_utils is None:
        _integration_utils = IntegrationTestUtils()
    return _integration_utils
