"""Core data models for the ApexSigma ecosystem."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class AgentPersona(BaseModel):
    """Represents the persona of an agent.

    Attributes:
        name: The name of the agent persona.
        description: A description of the agent persona.
        capabilities: A list of capabilities possessed by the agent.
    """
    name: str
    description: str
    capabilities: List[str]

class Task(BaseModel):
    """Represents a task to be executed.

    Attributes:
        id: The unique identifier for the task.
        title: The title of the task.
        description: A detailed description of the task.
        priority: The priority of the task.
        dependencies: A list of task IDs that this task depends on.
        status: The current status of the task.
        subtasks: A list of subtasks for this task.
    """
    id: str
    title: str
    description: str
    priority: str
    dependencies: List[str] = Field(default_factory=list)
    status: str
    subtasks: List['Task'] = Field(default_factory=list)

class StoreRequest(BaseModel):
    """Represents a request to store content in the memory store.

    Attributes:
        content: The content to be stored.
        metadata: Optional metadata associated with the content.
        agent_id: The ID of the agent making the request.
        expires_at: An optional expiration timestamp for the stored content.
    """
    content: str
    metadata: Optional[Dict[str, Any]] = None
    agent_id: Optional[str] = "default_agent"
    expires_at: Optional[datetime] = None

class QueryRequest(BaseModel):
    """Represents a request to query the memory store.

    Attributes:
        query: The query string.
        top_k: The number of results to return.
        agent_id: The ID of the agent making the request.
    """
    query: str
    top_k: Optional[int] = 5
    agent_id: Optional[str] = "default_agent"
