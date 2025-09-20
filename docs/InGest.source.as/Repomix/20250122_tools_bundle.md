# tools.as Production Bundle - 2025-01-22

**Architecture**: Standalone microservice providing essential tools for Society of Agents ecosystem
**Framework**: FastAPI with SQLAlchemy ORM and dual database support (SQLite/PostgreSQL)
**Purpose**: Centralized toolkit service for web search, task management, and agent scratchpad

## Core Production Components

### Database Configuration
```python
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./toolkit.db")

if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Database Models
```python
class TodoList(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_agent_id = Column(String, index=True, nullable=False)
    items = relationship("TodoItem", back_populates="list", cascade="all, delete-orphan")

class TodoItem(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    is_completed = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey("lists.id"))
    list = relationship("TodoList", back_populates="items")

class Scratchpad(Base):
    __tablename__ = "scratchpads"
    owner_agent_id = Column(String, primary_key=True, index=True)
    content = Column(Text, default="")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### Pydantic Schemas
```python
class TodoItemBase(BaseModel):
    content: str
    is_completed: bool = False

class TodoItemCreate(TodoItemBase):
    pass

class TodoItem(TodoItemBase):
    id: int
    list_id: int
    
    class Config:
        from_attributes = True

class TodoListBase(BaseModel):
    name: str

class TodoListCreate(TodoListBase):
    pass

class TodoList(TodoListBase):
    id: int
    owner_agent_id: str
    items: List[TodoItem] = []
    
    class Config:
        from_attributes = True

class ScratchpadBase(BaseModel):
    content: str

class Scratchpad(ScratchpadBase):
    owner_agent_id: str
    updated_at: datetime
    
    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
```

### Application Configuration
```python
class Settings(BaseSettings):
    serper_api_key: str = Field(..., alias="SERPER_API_KEY")
    
    model_config = {"env_file": ".env", "extra": "ignore"}

app = FastAPI(
    title="Tools as a Service",
    description="A standalone microservice providing essential tools for Society of Agents ecosystem",
    version="0.2.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_settings():
    return Settings()
```

### Web Search Tool
```python
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The search query.")

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str

@app.post("/search", response_model=List[SearchResult], tags=["Web Search"])
def search_web(
    search_request: SearchRequest,
    settings: Settings = Depends(get_settings)
):
    search_url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": settings.serper_api_key, "Content-Type": "application/json"}
    payload = {"q": search_request.query}
    
    try:
        response = requests.post(search_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        results = response.json().get("organic", [])
        processed_results = [
            SearchResult(
                title=result.get("title", ""),
                link=result.get("link", ""),
                snippet=result.get("snippet", "")
            )
            for result in results[:10]
        ]
        return processed_results
    
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Search service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
```

### To-Do List Management
```python
@app.post("/agents/{agent_id}/todo-lists", response_model=models.TodoList, tags=["To-Do Lists"])
def create_todo_list(
    agent_id: str,
    todo_list: schemas.TodoListCreate,
    db: Session = Depends(get_db)
):
    db_list = models.TodoList(**todo_list.model_dump(), owner_agent_id=agent_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@app.get("/agents/{agent_id}/todo-lists", response_model=List[models.TodoList], tags=["To-Do Lists"])
def get_agent_todo_lists(agent_id: str, db: Session = Depends(get_db)):
    return db.query(models.TodoList).filter(models.TodoList.owner_agent_id == agent_id).all()

@app.post("/todo-lists/{list_id}/items", response_model=models.TodoItem, tags=["To-Do Items"])
def create_todo_item(
    list_id: int,
    item: schemas.TodoItemCreate,
    db: Session = Depends(get_db)
):
    db_list = db.query(models.TodoList).filter(models.TodoList.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Todo list not found")
    
    db_item = models.TodoItem(**item.model_dump(), list_id=list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

### Agent Scratchpad
```python
@app.get("/scratchpad/{agent_id}", response_model=schemas.Scratchpad, tags=["Scratch Pad"])
def read_scratchpad(agent_id: str, db: Session = Depends(get_db)):
    db_scratchpad = (
        db.query(models.Scratchpad)
        .filter(models.Scratchpad.owner_agent_id == agent_id)
        .first()
    )
    
    if not db_scratchpad:
        # Create empty scratchpad if it doesn't exist
        db_scratchpad = models.Scratchpad(owner_agent_id=agent_id, content="")
        db.add(db_scratchpad)
        db.commit()
        db.refresh(db_scratchpad)
    
    return db_scratchpad

@app.post("/scratchpad/{agent_id}", response_model=schemas.Scratchpad, tags=["Scratch Pad"])
def update_scratchpad(
    agent_id: str,
    scratchpad_data: schemas.ScratchpadBase,
    db: Session = Depends(get_db)
):
    db_scratchpad = (
        db.query(models.Scratchpad)
        .filter(models.Scratchpad.owner_agent_id == agent_id)
        .first()
    )
    
    if db_scratchpad:
        db_scratchpad.content = scratchpad_data.content
    else:
        db_scratchpad = models.Scratchpad(
            owner_agent_id=agent_id,
            content=scratchpad_data.content
        )
        db.add(db_scratchpad)
    
    db.commit()
    db.refresh(db_scratchpad)
    return db_scratchpad

@app.delete("/scratchpad/{agent_id}", status_code=204, tags=["Scratch Pad"])
def clear_scratchpad(agent_id: str, db: Session = Depends(get_db)):
    db_scratchpad = (
        db.query(models.Scratchpad)
        .filter(models.Scratchpad.owner_agent_id == agent_id)
        .first()
    )
    
    if db_scratchpad:
        db.delete(db_scratchpad)
        db.commit()
    
    return {"message": "Scratchpad cleared"}
```

### Project Configuration
```toml
[tool.poetry]
name = "tools-as"
version = "0.1.0"
description = "A standalone microservice providing essential tools for Society of Agents ecosystem"
readme = ".md/README.md"
authors = ["ApexSigma <dev@apexsigma.dev>"]
package-mode = false

[tool.poetry.dependencies]
python = "^3.13"
fastapi = {extras = ["all"], version = "*"}
pydantic-settings = "*"
requests = "*"
sqlalchemy = "*"
alembic = "*"
psycopg2-binary = "*"

[tool.poetry.group.dev.dependencies]
ruff = "*"
pytest = "*"

[tool.ruff]
line-length = 88
target-version = "py313"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "ARG", "SIM"]
ignore = ["B008"]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ARG", "S101"]
```

**Key Features**: Web search integration, multi-agent task management, persistent scratchpad, dual database support, RESTful API design, agent-specific data isolation
