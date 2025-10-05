from apexsigma_core.models import AgentPersona, Task

def test_agent_persona():
    persona = AgentPersona(name="Test Agent", description="A test agent", capabilities=["testing"])
    assert persona.name == "Test Agent"
    assert persona.description == "A test agent"
    assert persona.capabilities == ["testing"]

def test_task():
    task = Task(id="1", title="Test Task", description="A test task", priority="high", status="pending")
    assert task.id == "1"
    assert task.title == "Test Task"
    assert task.description == "A test task"
    assert task.priority == "high"
    assert task.status == "pending"
    assert task.dependencies == []
    assert task.subtasks == []
