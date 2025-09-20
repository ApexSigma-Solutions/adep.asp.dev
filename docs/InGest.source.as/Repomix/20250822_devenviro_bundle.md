# DevEnviro.as Production Bundle - 2025-08-22
## Architecture
Society of Agents system with RabbitMQ communication, PostgreSQL persistence, agent registry, task orchestration, and multi-model CLI integration.
## Core Files
**app/config.py**
```python
from pydantic import BaseSettings
from typing import List
class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str = "rabbitmq"
    GEMINI_API_KEYS: List[str]
settings = Settings()
```
**app/src/core/schemas.py**
```python
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
class PayloadType(str, Enum):
    CODE = "code"
    STATUS = "status"
    ERROR = "error"
    TASK_REQUEST = "task_request"
    TASK_RESULT = "task_result"
    DELEGATION = "delegation"
    HEARTBEAT = "heartbeat"
    SYSTEM = "system"
class MessagePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
class AgentStatus(str, Enum):
    INACTIVE = "inactive"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    BUSY = "busy"
    SHUTTING_DOWN = "shutting_down"
class AgentPersona(BaseModel):
    name: str = Field(..., description="Display name of the agent persona")
    description: str = Field(..., description="Brief description of the agent persona")
    agent_id: str = Field(..., description="Unique identifier for the agent")
    capabilities: List[str] = Field(default_factory=list, description="List of agent capabilities")
    system_prompt: str = Field(default="", description="System prompt for the agent")
    color: Optional[str] = Field(None, description="Optional color code for the agent")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    status: AgentStatus = Field(default=AgentStatus.INACTIVE, description="Current agent status")
    is_listening: bool = Field(default=False, description="Whether agent is listening for messages")
    last_activity: datetime = Field(default_factory=datetime.utcnow, description="Last activity timestamp")
    current_load: float = Field(default=0.0, ge=0, le=100, description="Current workload percentage")
    comm_manager: Optional[Any] = Field(None, exclude=True, description="Communication manager instance")
    db_synced: bool = Field(default=False, exclude=True, description="Whether agent is synced with database")
    def initialize_communication(self, comm_manager: 'CommunicationsManager'):
        self.comm_manager = comm_manager
    def handle_message(self, message: 'AgentMessage'):
        pass
    def send_message(self, recipient_id: str, payload_type: PayloadType, payload_data: Dict[str, Any], **kwargs) -> bool:
        message = create_message(self.agent_id, recipient_id, payload_type, payload_data, **kwargs)
        success = self.comm_manager.send_message(recipient_id, message)
        return success
    def update_status(self, status: AgentStatus, load_level: Optional[float] = None):
        self.status = status
        if load_level is not None:
            self.current_load = load_level
        self.last_activity = datetime.utcnow()
    def shutdown(self):
        self.is_listening = False
        self.status = AgentStatus.SHUTTING_DOWN
class AgentMessage(BaseModel):
    message_id: UUID = Field(default_factory=uuid4, description="Unique message identifier")
    task_id: Optional[UUID] = Field(None, description="Parent task ID for tracking task chains")
    sender_agent_id: str = Field(..., description="ID of the sending agent")
    recipient_agent_id: str = Field(..., description="ID of the target recipient agent")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message creation timestamp")
    payload_type: PayloadType = Field(..., description="Type of message payload")
    priority: MessagePriority = Field(default=MessagePriority.MEDIUM, description="Message processing priority")
    payload: Dict[str, Any] = Field(..., description="Message content and data")
    correlation_id: Optional[UUID] = Field(None, description="For request-response correlation")
    reply_to: Optional[str] = Field(None, description="Queue name for reply messages")
    ttl: Optional[int] = Field(None, description="Time-to-live in seconds")
def create_message(sender_id: str, recipient_id: str, payload_type: PayloadType, payload_data: Dict[str, Any], task_id: Optional[UUID] = None, priority: MessagePriority = MessagePriority.MEDIUM, **kwargs) -> AgentMessage:
    if hasattr(payload_data, 'dict'):
        payload_data = payload_data.dict()
    return AgentMessage(sender_agent_id=sender_id, recipient_agent_id=recipient_id, payload_type=payload_type, payload=payload_data, task_id=task_id, priority=priority, **kwargs)
```
**app/src/core/database_manager.py**
```python
import psycopg2
import os
import time
import threading
from typing import Optional, Dict, Any, List
class DatabaseManager:
    _instance = None
    _pool = None
    _lock = threading.Lock()
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, host: Optional[str] = None):
        if hasattr(self, '_initialized'):
            return
        db_name = os.getenv("POSTGRES_DB")
        db_user = os.getenv("POSTGRES_USER")
        db_password = os.getenv("POSTGRES_PASSWORD")
        db_host = host or os.getenv("POSTGRES_HOST", "localhost")
        db_port = int(os.getenv("POSTGRES_PORT", 5432))
        self.connection_params = {
            "database": db_name,
            "user": db_user,
            "password": db_password,
            "host": db_host,
            "port": db_port
        }
        self._initialized = True
    def get_connection(self):
        max_retries = 10
        for attempt in range(max_retries):
            try:
                conn = psycopg2.connect(**self.connection_params)
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                return conn
            except Exception:
                sleep_time = 2 ** attempt
                time.sleep(sleep_time)
        raise ConnectionError("Failed to connect to database after retries")
    def execute_query(self, query: str, params: tuple = None) -> int:
        return self._execute(query, params)
    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        return self._execute(query, params, fetch='one')
    def fetch_all(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        return self._execute(query, params, fetch='all')
    def _execute(self, query: str, params: tuple = None, fetch: Optional[str] = None) -> Any:
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch == 'one':
                result = cursor.fetchone()
                return dict(zip([desc[0] for desc in cursor.description], result)) if result else None
            elif fetch == 'all':
                results = cursor.fetchall()
                return [dict(zip([desc[0] for desc in cursor.description], row)) for row in results]
            else:
                conn.commit()
                return cursor.rowcount
        except Exception:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
_db_manager_instance = None
_db_manager_lock = threading.Lock()
def get_database_manager(host: Optional[str] = None) -> DatabaseManager:
    global _db_manager_instance
    if _db_manager_instance is None:
        with _db_manager_lock:
            if _db_manager_instance is None:
                _db_manager_instance = DatabaseManager(host=host)
    return _db_manager_instance
```
**app/src/core/communications_manager.py**
```python
import pika
import json
import logging
import threading
import time
import psycopg2
from contextlib import contextmanager
from typing import Dict, Any, Callable, Optional
from .schemas import AgentMessage, MessagePriority, PayloadType, create_message
from .observability import get_observability
class CommunicationsManager:
    def __init__(self, rabbitmq_url: str = None, exchange_name: str = None):
        self.rabbitmq_url = rabbitmq_url or os.getenv('RABBITMQ_URL', 'amqp://myuser:mypassword@localhost:5672/')
        self.exchange_name = exchange_name or os.getenv('RABBITMQ_EXCHANGE', 'agent_exchange')
        self.retry_delay = 2
        self.max_retries = 5
        self.listeners = {}
        self.agent_callbacks = {}
        self._setup_logging()
    def _setup_logging(self):
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    def _connect_with_retry(self) -> pika.BlockingConnection:
        for attempt in range(self.max_retries):
            try:
                parameters = pika.URLParameters(self.rabbitmq_url)
                connection = pika.BlockingConnection(parameters)
                return connection
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))
                else:
                    raise
    def wait_for_rabbitmq_ready(self, timeout: int = 60) -> bool:
        start_time = time.time()
        attempt = 0
        while time.time() - start_time < timeout:
            try:
                connection = self._connect_with_retry()
                channel = connection.channel()
                channel.exchange_declare(exchange='test', exchange_type='direct', passive=True)
                connection.close()
                return True
            except Exception:
                attempt += 1
                time.sleep(2)
        return False
    @contextmanager
    def get_connection_and_channel(self):
        connection = None
        channel = None
        try:
            connection = self._connect_with_retry()
            channel = connection.channel()
            yield connection, channel
        finally:
            if channel:
                channel.close()
            if connection:
                connection.close()
    def setup_exchange(self):
        with self.get_connection_and_channel() as (connection, channel):
            channel.exchange_declare(exchange=self.exchange_name, exchange_type='topic', durable=True)
    def _log_message_to_postgres(self, message_dict: Dict[str, Any]):
        try:
            conn = psycopg2.connect(
                host=os.getenv('POSTGRES_HOST', 'localhost'),
                database=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD')
            )
            cursor = conn.cursor()
            query = """INSERT INTO agent_communications (sender_id, recipient_id, payload_type, payload, timestamp) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                message_dict.get('sender_agent_id'),
                message_dict.get('recipient_agent_id'),
                message_dict.get('payload_type'),
                json.dumps(message_dict.get('payload', {})),
                message_dict.get('timestamp')
            ))
            conn.commit()
            conn.close()
        except Exception:
            pass
    def send_message(self, recipient_agent_id: str, message: Any, routing_key: Optional[str] = None) -> bool:
        try:
            if isinstance(message, dict):
                message = AgentMessage(**message)
            if routing_key is None:
                routing_key = f"agent.{recipient_agent_id}"
            message_body = message.json()
            obs = get_observability()
            with self.get_connection_and_channel() as (connection, channel):
                self.setup_exchange()
                properties = pika.BasicProperties(
                    priority=self._get_priority_value(message.priority),
                    delivery_mode=2,
                    message_id=str(message.message_id),
                    timestamp=int(message.timestamp.timestamp())
                )
                channel.basic_publish(
                    exchange=self.exchange_name,
                    routing_key=routing_key,
                    body=message_body,
                    properties=properties
                )
                message_dict = json.loads(message_body)
                self._log_message_to_postgres(message_dict)
                return True
        except Exception:
            return False
    def start_listening(self, agent_id: str, callback_function: Callable, queue_name: Optional[str] = None) -> bool:
        try:
            if queue_name is None:
                queue_name = f"queue.{agent_id}"
            self.agent_callbacks[agent_id] = callback_function
            listen_thread = threading.Thread(
                target=self._listen_worker,
                args=(agent_id, queue_name),
                daemon=True
            )
            listen_thread.start()
            self.listeners[agent_id] = listen_thread
            return True
        except Exception:
            return False
    def _listen_worker(self, agent_id: str, queue_name: str):
        with self.get_connection_and_channel() as (connection, channel):
            channel.queue_declare(queue=queue_name, durable=True)
            routing_key = f"agent.{agent_id}"
            channel.queue_bind(exchange=self.exchange_name, queue=queue_name, routing_key=routing_key)
            channel.queue_bind(exchange=self.exchange_name, queue=queue_name, routing_key="broadcast.*")
            channel.basic_qos(prefetch_count=1)
            def message_handler(ch, method, properties, body):
                try:
                    message_data = json.loads(body.decode('utf-8'))
                    message = AgentMessage(**message_data)
                    callback = self.agent_callbacks.get(agent_id)
                    if callback:
                        callback(message)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            channel.basic_consume(queue=queue_name, on_message_callback=message_handler)
            channel.start_consuming()
    def _get_priority_value(self, priority: MessagePriority) -> int:
        priority_map = {
            MessagePriority.LOW: 1,
            MessagePriority.MEDIUM: 5,
            MessagePriority.HIGH: 8,
            MessagePriority.CRITICAL: 10
        }
        return priority_map.get(priority, 5)
```
**app/src/core/agent_registry.py**
```python
import hashlib
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from .schemas import AgentPersona, AgentStatus
logger = logging.getLogger(__name__)
def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
class AgentRegistry:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.live_agents: Dict[str, AgentPersona] = {}
        self._agent_tokens: Dict[str, str] = {}
    def register_agent_in_db(self, agent_id: str, persona: str, capabilities: List[str], token: str) -> Optional[Dict[str, Any]]:
        token_hash = _hash_token(token)
        query = """INSERT INTO agents (agent_id, persona, capabilities, token_hash) VALUES (%s, %s, %s, %s) ON CONFLICT (agent_id) DO UPDATE SET persona = EXCLUDED.persona, capabilities = EXCLUDED.capabilities, token_hash = EXCLUDED.token_hash RETURNING *"""
        params = (agent_id, persona, capabilities, token_hash)
        return self.db_manager.fetch_one(query, params)
    def get_agent_record(self, agent_id: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM agents WHERE agent_id = %s"
        return self.db_manager.fetch_one(query, (agent_id,))
    def get_all_agent_records(self) -> List[Dict[str, Any]]:
        query = "SELECT * FROM agents"
        return self.db_manager.fetch_all(query)
    def get_live_agent(self, agent_id: str) -> Optional[AgentPersona]:
        return self.live_agents.get(agent_id)
    def get_all_live_agents(self) -> List[AgentPersona]:
        return list(self.live_agents.values())
    def get_active_live_agents(self) -> List[AgentPersona]:
        return [agent for agent in self.live_agents.values() if agent.is_listening]
    def register_live_agent(self, agent: AgentPersona, token: str, sync_to_db: bool = True) -> bool:
        try:
            self.live_agents[agent.agent_id] = agent
            self._agent_tokens[agent.agent_id] = token
            if sync_to_db:
                db_record = self.register_agent_in_db(
                    agent.agent_id,
                    agent.name,
                    agent.capabilities,
                    token
                )
                agent.db_synced = db_record is not None
            return True
        except Exception:
            return False
    def find_best_agent(self, requirements: Dict[str, Any]) -> Optional[AgentPersona]:
        required_specialty = requirements.get("agent_specialty")
        required_capabilities = set(requirements.get("capabilities", []))
        active_agents = self.get_active_live_agents()
        if not active_agents:
            return None
        best_agent = None
        highest_score = -1
        for agent in active_agents:
            score = 0
            if required_specialty and required_specialty.lower() in agent.name.lower():
                score += 10
            matched_capabilities = len(required_capabilities.intersection(set(agent.capabilities)))
            score += matched_capabilities * 2
            if score > highest_score:
                highest_score = score
                best_agent = agent
        return best_agent or active_agents[0]
```
**app/src/core/orchestrator.py**
```python
import logging
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict, Any, Optional, List
from .schemas import AgentPersona, AgentMessage, PayloadType, TaskRequest, TaskResult, DelegationPayload, create_message
from .agent_registry import AgentRegistry
from .communications_manager import CommunicationsManager
from .workflow_definitions import WorkflowPlan, TaskNode, TaskStatus
from .observability import get_observability, track_llm
logger = logging.getLogger(__name__)
class Orchestrator(AgentPersona):
    def __init__(self):
        super().__init__(
            name="orchestrator",
            description="Master orchestrator for task decomposition and delegation",
            agent_id="orchestrator_001",
            capabilities=["task_decomposition", "agent_coordination", "workflow_management"]
        )
        self.agent_registry: Optional[AgentRegistry] = None
        self.active_workflows: Dict[UUID, WorkflowPlan] = {}
        self.task_templates: Dict[str, Dict[str, Any]] = {}
        self.performance_stats = {
            "tasks_delegated": 0,
            "workflows_completed": 0,
            "average_completion_time": 0.0
        }
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    def initialize(self, comm_manager: CommunicationsManager, agent_registry: AgentRegistry):
        self.initialize_communication(comm_manager)
        self.agent_registry = agent_registry
    def handle_message(self, message: AgentMessage):
        try:
            if message.payload_type == PayloadType.TASK_REQUEST:
                self._handle_task_request(message)
            elif message.payload_type == PayloadType.TASK_RESULT:
                self._handle_task_result(message)
            elif message.payload_type == PayloadType.STATUS:
                self._handle_status_update(message)
            elif message.payload_type == PayloadType.ERROR:
                self._handle_error_message(message)
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
    @track_llm("orchestrator_process_user_request")
    def process_user_request(self, user_request: str, context: Dict[str, Any] = None) -> UUID:
        workflow_id = uuid4()
        context = context or {}
        workflow_plan = self._decompose_request(workflow_id, user_request, context)
        self.active_workflows[workflow_id] = workflow_plan
        self._execute_workflow(workflow_plan)
        obs = get_observability()
        obs.set_trace_attribute("workflow_id", str(workflow_id))
        obs.set_trace_attribute("request_type", self._classify_request_type(user_request.lower()))
        return workflow_id
    def _decompose_request(self, workflow_id: UUID, user_request: str, context: Dict[str, Any]) -> WorkflowPlan:
        workflow_plan = WorkflowPlan(workflow_id, "User Request Workflow", user_request)
        request_lower = user_request.lower()
        if any(keyword in request_lower for keyword in ["api", "endpoint", "rest", "service"]):
            self._create_api_workflow(workflow_plan, user_request, context)
        else:
            self._create_generic_workflow(workflow_plan, user_request, context)
        obs = get_observability()
        obs.set_trace_attribute("tasks_created", len(workflow_plan.tasks))
        return workflow_plan
    def _create_generic_workflow(self, workflow: WorkflowPlan, request: str, context: Dict[str, Any]):
        task = TaskNode(
            task_id=uuid4(),
            task_type="general_analysis",
            description=f"Analyze and implement: {request}",
            requirements={"capabilities": ["analysis", "implementation"]},
            context=context,
            estimated_duration=60
        )
        workflow.add_task(task)
    def _execute_workflow(self, workflow: WorkflowPlan):
        self._delegate_ready_tasks(workflow)
    def _delegate_ready_tasks(self, workflow: WorkflowPlan):
        ready_tasks = workflow.get_ready_tasks()
        for task in ready_tasks:
            agent = self._select_agent_for_task(task)
            if agent:
                self._delegate_task_to_agent(task, agent, workflow.workflow_id)
    def _select_agent_for_task(self, task: TaskNode) -> Optional[AgentPersona]:
        if not self.agent_registry:
            return None
        return self.agent_registry.find_best_agent(task.requirements)
    def _delegate_task_to_agent(self, task: TaskNode, agent: AgentPersona, workflow_id: UUID):
        try:
            task_request = TaskRequest(
                task_id=task.task_id,
                task_type=task.task_type,
                description=task.description,
                requirements=task.requirements,
                context=task.context,
                deadline=task.deadline
            )
            delegation_payload = DelegationPayload(
                orchestrator_id=self.agent_id,
                task_request=task_request,
                callback_queue=f"orchestrator.{workflow_id}"
            )
            success = self.send_message(
                agent.agent_id,
                PayloadType.DELEGATION,
                delegation_payload.dict(),
                task_id=task.task_id
            )
            if success:
                task.status = TaskStatus.IN_PROGRESS
                task.assigned_agent_id = agent.agent_id
                task.started_at = datetime.utcnow()
                self.performance_stats["tasks_delegated"] += 1
                self.logger.info(f"Delegated task {task.task_id} to agent {agent.name}")
            else:
                self.logger.error(f"Failed to delegate task {task.task_id}")
        except Exception as e:
            self.logger.error(f"Error delegating task: {e}")
    def _handle_task_result(self, message: AgentMessage):
        try:
            task_result = TaskResult(**message.payload)
            task_id = task_result.task_id
            workflow = None
            for wf in self.active_workflows.values():
                if task_id in wf.tasks:
                    workflow = wf
                    break
            if not workflow:
                self.logger.warning(f"No workflow found for task {task_id}")
                return
            task = workflow.tasks[task_id]
            if task_result.status == TaskStatus.COMPLETED:
                task.status = TaskStatus.COMPLETED
                task.result = task_result.result
                task.completed_at = datetime.utcnow()
                self.logger.info(f"Task {task_id} completed successfully")
                self._delegate_ready_tasks(workflow)
                if workflow.is_complete():
                    self._complete_workflow(workflow)
            else:
                task.status = TaskStatus.FAILED
                task.error_message = task_result.error_message
                self.logger.error(f"Task {task_id} failed: {task_result.error_message}")
                self._handle_task_failure(task, workflow)
        except Exception as e:
            self.logger.error(f"Error handling task result: {e}")
    def _complete_workflow(self, workflow: WorkflowPlan):
        workflow.status = "completed"
        workflow.completed_at = datetime.utcnow()
        results = {str(task_id): task.result for task_id, task in workflow.tasks.items() if task.result}
        self.performance_stats["workflows_completed"] += 1
        self.logger.info(f"Workflow {workflow.workflow_id} completed with {len(results)} results")
    def get_workflow_status(self, workflow_id: UUID) -> Optional[Dict[str, Any]]:
        workflow = self.active_workflows.get(workflow_id)
        if not workflow:
            return None
        return {
            "workflow_id": str(workflow_id),
            "status": workflow.status,
            "tasks": len(workflow.tasks),
            "completed_tasks": len([t for t in workflow.tasks.values() if t.status == TaskStatus.COMPLETED]),
            "failed_tasks": len([t for t in workflow.tasks.values() if t.status == TaskStatus.FAILED])
        }
```
**app/src/main.py**
```python
from fastapi import FastAPI
from pathlib import Path
import logging
from .core.enhanced_initialization_manager import EnhancedInitializationManager
from .core.migrations_runner import apply_migrations
from .core.seed_knowledge import seed_knowledge_base
from .core.orchestrator import Orchestrator
from .core.observability import DevEnviroObservability, instrument_fastapi_app
from .Workflows.author_reviewer_workflow import demo_author_reviewer_workflow
project_root = Path(__file__).parent.parent
observability = DevEnviroObservability()
observability.initialize_observability()
app = FastAPI()
instrument_fastapi_app(app)
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.getLogger("pika").setLevel(logging.WARNING)
@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("DevEnviro")
    setup_logging()
    try:
        apply_migrations()
        seed_knowledge_base()
        init_manager = EnhancedInitializationManager(project_root=project_root)
        init_manager.initialize_all_services()
        comm_manager = init_manager.get_communications_manager()
        agent_registry = init_manager.get_agent_registry()
        orchestrator = Orchestrator()
        orchestrator.initialize(comm_manager, agent_registry)
        agent_registry.register_live_agent(orchestrator, "orchestrator_token")
        demo_workflow_id = demo_author_reviewer_workflow()
        logger.info(f"Demo workflow started: {demo_workflow_id}")
        logger.info("DevEnviro startup completed successfully")
    except Exception as e:
        logger.error(f"Critical error during startup: {e}")
        raise
@app.get("/")
async def root():
    return {"message": "DevEnviro Society of Agents API is running"}
```
**pyproject.toml**
```toml
[project]
name = "devenviro-as"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "psycopg[binary] (>=3.2.9,<4.0.0)"
]
[[tool.poetry.packages]]
include = "app"
```
