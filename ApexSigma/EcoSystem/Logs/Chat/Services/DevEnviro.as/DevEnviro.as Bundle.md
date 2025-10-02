---
title: DevEnviro.as Bundle
date created: Sunday, September 21st 2025, 2:56:11 pm
date modified: Sunday, September 21st 2025, 3:03:39 pm
---

# DevEnviro.as Bundle

DevEnviro.as Production Bundle - 2025-08-22

Architecture

Society of Agents system with RabbitMQ communication, PostgreSQL persistence, agent registry, task orchestration, and multi-model CLI integration.

Core Files

app/config.py

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

app/src/core/schemas.py

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

app/src/core/database_manager.py

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

app/src/core/communications_manager.py

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

app/src/core/agent_registry.py

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

app/src/core/orchestrator.py

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

	def handle_message(self, message: Agen
