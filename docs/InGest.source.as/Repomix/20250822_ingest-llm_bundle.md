# InGest-LLM.as Production Bundle - 2025-08-22
## Architecture
Repository ingestion and analysis system with FastAPI, observability stack (Langfuse/OpenTelemetry), memOS integration, and Python AST parsing.
## Core Files
**src/ingest_llm_as/config.py**
```python
from pydantic import BaseSettings
from typing import Optional, List
class Settings(BaseSettings):
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[str] = None
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    MEMOS_API_URL: str = "http://localhost:8090"
    OTEL_ENABLED: bool = True
    OTEL_SERVICE_NAME: str = "ingest-llm-as"
    JAEGER_ENDPOINT: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True
    LOG_LEVEL: str = "INFO"
    class Config:
        env_file = ".env"
settings = Settings()
```
**src/ingest_llm_as/main.py**
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .observability.setup import setup_observability
from .api import analysis, ecosystem, ingestion, repository
from .observability.logging import get_logger
logger = get_logger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting InGest-LLM.as application")
    observability = setup_observability(app)
    yield
    logger.info("Shutting down InGest-LLM.as application")
app = FastAPI(
    title="InGest-LLM.as",
    description="Repository ingestion and analysis service for ApexSigma ecosystem",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(analysis.router)
app.include_router(ecosystem.router)
app.include_router(ingestion.router)
app.include_router(repository.router)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ingest-llm-as"}
@app.get("/")
async def root():
    return {"message": "InGest-LLM.as Repository Analysis Service"}
```
**src/ingest_llm_as/models.py**
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
from uuid import UUID
class ProcessingStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"
class RepositoryIngestionRequest(BaseModel):
    source_type: str = Field(..., description="Type of source: 'local', 'git', 'github'")
    source_path: str = Field(..., description="Path or URL to repository")
    include_patterns: List[str] = Field(default=["**/*.py"], description="File patterns to include")
    exclude_patterns: List[str] = Field(default=["**/__pycache__/**", "**/.*"], description="File patterns to exclude")
    max_file_size: int = Field(default=1048576, description="Maximum file size in bytes")
    generate_embeddings: bool = Field(default=True, description="Whether to generate embeddings")
    store_in_memos: bool = Field(default=True, description="Whether to store in memOS.as")
class FileProcessingResult(BaseModel):
    relative_path: str
    file_size: int
    status: ProcessingStatus
    elements_extracted: int
    error_message: Optional[str] = None
    processing_time_ms: int
class RepositoryIngestionResponse(BaseModel):
    ingestion_id: str
    status: ProcessingStatus
    message: str
    timestamp: str
    source_info: Dict[str, Any]
    files_to_process: int
    files_processed: List[FileProcessingResult]
    processing_summary: Dict[str, Any]
    embeddings_generated: int
    memos_entries_created: int
    total_processing_time_ms: int
class RepositoryAnalysisRequest(BaseModel):
    ingestion_id: UUID
    analysis_type: str = Field(default="comprehensive", description="Type of analysis")
    include_metrics: bool = Field(default=True, description="Include code metrics")
    include_suggestions: bool = Field(default=True, description="Include optimization suggestions")
class RepositoryAnalysisResponse(BaseModel):
    analysis_id: str
    repository_metrics: Dict[str, Any]
    code_quality_score: float
    suggestions: List[str]
    refactoring_opportunities: List[str]
```
**src/ingest_llm_as/services/repository_processor.py**
```python
import asyncio
import time
from pathlib import Path
from typing import List, Dict, Any
from ..models import RepositoryIngestionRequest, RepositoryIngestionResponse, FileProcessingResult, ProcessingStatus
from ..parsers.python_ast_parser import PythonASTParser
from ..services.vectorizer import get_vectorizer
from ..services.memos_client import get_memos_client
from ..observability.logging import get_logger
from ..observability.langfuse_client import trace_ingestion_operation
logger = get_logger(__name__)
class RepositoryProcessor:
    def __init__(self):
        self.ast_parser = PythonASTParser()
        self.vectorizer = get_vectorizer()
        self.memos_client = get_memos_client()
    @trace_ingestion_operation("repository")
    async def process_repository(self, request: RepositoryIngestionRequest) -> RepositoryIngestionResponse:
        start_time = time.time()
        ingestion_id = f"repo_{int(start_time)}"
        try:
            source_path = Path(request.source_path)
            if not source_path.exists():
                raise ValueError(f"Source path does not exist: {source_path}")
            files_to_process = self._discover_files(source_path, request.include_patterns, request.exclude_patterns)
            files_processed = []
            embeddings_generated = 0
            memos_entries_created = 0
            for file_path in files_to_process:
                try:
                    result = await self._process_file(file_path, source_path, request)
                    files_processed.append(result)
                    if result.status == ProcessingStatus.COMPLETED:
                        embeddings_generated += 1
                        if request.store_in_memos:
                            memos_entries_created += 1
                except Exception as e:
                    logger.error(f"Failed to process file {file_path}: {e}")
                    files_processed.append(FileProcessingResult(
                        relative_path=str(file_path.relative_to(source_path)),
                        file_size=file_path.stat().st_size if file_path.exists() else 0,
                        status=ProcessingStatus.FAILED,
                        elements_extracted=0,
                        error_message=str(e),
                        processing_time_ms=0
                    ))
            total_time = int((time.time() - start_time) * 1000)
            processing_summary = {
                "total_files": len(files_to_process),
                "successful_files": len([f for f in files_processed if f.status == ProcessingStatus.COMPLETED]),
                "failed_files": len([f for f in files_processed if f.status == ProcessingStatus.FAILED]),
                "total_size_bytes": sum(f.file_size for f in files_processed),
                "largest_files": sorted([{"path": f.relative_path, "size": f.file_size} for f in files_processed], key=lambda x: x["size"], reverse=True)[:5]
            }
            return RepositoryIngestionResponse(
                ingestion_id=ingestion_id,
                status=ProcessingStatus.COMPLETED,
                message="Repository processed successfully",
                timestamp=str(datetime.now()),
                source_info={"type": request.source_type, "path": request.source_path},
                files_to_process=len(files_to_process),
                files_processed=files_processed,
                processing_summary=processing_summary,
                embeddings_generated=embeddings_generated,
                memos_entries_created=memos_entries_created,
                total_processing_time_ms=total_time
            )
        except Exception as e:
            logger.error(f"Repository processing failed: {e}")
            return RepositoryIngestionResponse(
                ingestion_id=ingestion_id,
                status=ProcessingStatus.FAILED,
                message=f"Processing failed: {str(e)}",
                timestamp=str(datetime.now()),
                source_info={"type": request.source_type, "path": request.source_path},
                files_to_process=0,
                files_processed=[],
                processing_summary={},
                embeddings_generated=0,
                memos_entries_created=0,
                total_processing_time_ms=int((time.time() - start_time) * 1000)
            )
    def _discover_files(self, source_path: Path, include_patterns: List[str], exclude_patterns: List[str]) -> List[Path]:
        import fnmatch
        all_files = []
        for pattern in include_patterns:
            all_files.extend(source_path.rglob(pattern.replace("**/", "")))
        filtered_files = []
        for file_path in all_files:
            relative_path = str(file_path.relative_to(source_path))
            excluded = any(fnmatch.fnmatch(relative_path, pattern.replace("**/", "")) for pattern in exclude_patterns)
            if not excluded and file_path.is_file():
                filtered_files.append(file_path)
        return filtered_files
    async def _process_file(self, file_path: Path, source_root: Path, request: RepositoryIngestionRequest) -> FileProcessingResult:
        start_time = time.time()
        try:
            if file_path.stat().st_size > request.max_file_size:
                return FileProcessingResult(
                    relative_path=str(file_path.relative_to(source_root)),
                    file_size=file_path.stat().st_size,
                    status=ProcessingStatus.FAILED,
                    elements_extracted=0,
                    error_message="File size exceeds maximum limit",
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            elements_extracted = 0
            if file_path.suffix == '.py':
                elements = self.ast_parser.parse_file(str(file_path), content)
                elements_extracted = len(elements)
                if request.generate_embeddings:
                    for element in elements:
                        embedding = await self.vectorizer.generate_embedding(element.to_searchable_content())
                        if request.store_in_memos:
                            await self.memos_client.store_code_element(element, embedding)
            return FileProcessingResult(
                relative_path=str(file_path.relative_to(source_root)),
                file_size=file_path.stat().st_size,
                status=ProcessingStatus.COMPLETED,
                elements_extracted=elements_extracted,
                processing_time_ms=int((time.time() - start_time) * 1000)
            )
        except Exception as e:
            return FileProcessingResult(
                relative_path=str(file_path.relative_to(source_root)),
                file_size=file_path.stat().st_size if file_path.exists() else 0,
                status=ProcessingStatus.FAILED,
                elements_extracted=0,
                error_message=str(e),
                processing_time_ms=int((time.time() - start_time) * 1000)
            )
_repository_processor = None
def get_repository_processor() -> RepositoryProcessor:
    global _repository_processor
    if _repository_processor is None:
        _repository_processor = RepositoryProcessor()
    return _repository_processor
```
**src/ingest_llm_as/services/vectorizer.py**
```python
import asyncio
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from ..observability.logging import get_logger
from ..observability.langfuse_client import trace_content_processing
logger = get_logger(__name__)
class Vectorizer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    def _load_model(self):
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    @trace_content_processing("embedding_generation")
    async def generate_embedding(self, text: str) -> List[float]:
        if not self.model:
            raise RuntimeError("Embedding model not loaded")
        try:
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(None, self._encode_text, text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise
    def _encode_text(self, text: str) -> np.ndarray:
        return self.model.encode(text, convert_to_tensor=False)
    @trace_content_processing("batch_embedding_generation")
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        if not self.model:
            raise RuntimeError("Embedding model not loaded")
        try:
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(None, self._encode_texts_batch, texts)
            return [embedding.tolist() for embedding in embeddings]
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise
    def _encode_texts_batch(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_tensor=False)
    def get_embedding_dimension(self) -> int:
        if not self.model:
            return 384  # Default dimension for all-MiniLM-L6-v2
        return self.model.get_sentence_embedding_dimension()
_vectorizer = None
def get_vectorizer() -> Vectorizer:
    global _vectorizer
    if _vectorizer is None:
        _vectorizer = Vectorizer()
    return _vectorizer
```
**src/ingest_llm_as/services/memos_client.py**
```python
import httpx
from typing import Dict, Any, List, Optional
from ..models import ProcessingStatus
from ..parsers.python_ast_parser import CodeElement
from ..observability.logging import get_logger
from ..observability.langfuse_client import trace_memos_interaction
from ..config import settings
logger = get_logger(__name__)
class MemosClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.MEMOS_API_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    @trace_memos_interaction("/store", "POST")
    async def store_code_element(self, element: CodeElement, embedding: List[float]) -> bool:
        try:
            payload = {
                "type": "code_element",
                "content": element.to_searchable_content(),
                "metadata": {
                    "element_type": element.element_type,
                    "name": element.name,
                    "qualified_name": element.qualified_name,
                    "file_path": element.file_path,
                    "line_start": element.line_start,
                    "line_end": element.line_end,
                    "complexity_score": element.complexity_score,
                    "dependencies": element.dependencies,
                    "decorators": element.decorators,
                    "content_hash": element.content_hash
                },
                "embedding": embedding,
                "tags": list(element.tags)
            }
            response = await self.client.post(f"{self.base_url}/store", json=payload)
            response.raise_for_status()
            logger.info(f"Stored code element: {element.qualified_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to store code element {element.qualified_name}: {e}")
            return False
    @trace_memos_interaction("/search", "GET")
    async def search_similar_code(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            params = {"query": query, "limit": limit, "type": "code_element"}
            response = await self.client.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            logger.error(f"Failed to search similar code: {e}")
            return []
    @trace_memos_interaction("/health", "GET")
    async def health_check(self) -> bool:
        try:
            response = await self.client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json().get("status") == "healthy"
        except Exception as e:
            logger.error(f"memOS.as health check failed: {e}")
            return False
    async def close(self):
        await self.client.aclose()
_memos_client = None
def get_memos_client() -> MemosClient:
    global _memos_client
    if _memos_client is None:
        _memos_client = MemosClient()
    return _memos_client
```
**pyproject.toml**
```toml
[project]
name = "ingest-llm-as"
version = "1.0.0"
description = "Repository ingestion and analysis service for ApexSigma ecosystem"
authors = [{name = "ApexSigma Solutions"}]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
    "httpx>=0.25.0",
    "sentence-transformers>=2.2.0",
    "langfuse>=2.20.0",
    "opentelemetry-api>=1.21.0",
    "opentelemetry-sdk>=1.21.0",
    "opentelemetry-instrumentation-fastapi>=0.42b0",
    "opentelemetry-instrumentation-httpx>=0.42b0",
    "opentelemetry-exporter-jaeger>=1.21.0",
    "prometheus-client>=0.19.0",
    "prometheus-fastapi-instrumentator>=6.1.0",
    "structlog>=23.2.0",
    "numpy>=1.24.0"
]
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```
